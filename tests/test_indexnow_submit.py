import tempfile
import unittest
from pathlib import Path


class IndexNowSubmitTests(unittest.TestCase):
    def test_build_payload_uses_host_key_and_urls(self):
        from scripts import indexnow_submit

        payload = indexnow_submit.build_payload(
            host="aicatnews.github.io",
            key="9392961acc734a38b55a177477c1df13",
            urls=["https://aicatnews.github.io/", "https://aicatnews.github.io/page/2/"],
        )

        self.assertEqual(payload["host"], "aicatnews.github.io")
        self.assertEqual(payload["key"], "9392961acc734a38b55a177477c1df13")
        self.assertEqual(
            payload["keyLocation"],
            "https://aicatnews.github.io/9392961acc734a38b55a177477c1df13.txt",
        )
        self.assertEqual(
            payload["urlList"],
            ["https://aicatnews.github.io/", "https://aicatnews.github.io/page/2/"],
        )

    def test_collect_sitemap_urls_returns_unique_locations(self):
        from scripts import indexnow_submit

        with tempfile.TemporaryDirectory() as tmpdir:
            sitemap = Path(tmpdir) / "sitemap.xml"
            sitemap.write_text(
                """
                <urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
                  <url><loc>https://aicatnews.github.io/</loc></url>
                  <url><loc>https://aicatnews.github.io/page/2/</loc></url>
                  <url><loc>https://aicatnews.github.io/</loc></url>
                </urlset>
                """,
                encoding="utf-8",
            )

            urls = indexnow_submit.collect_sitemap_urls(sitemap)

        self.assertEqual(
            urls,
            ["https://aicatnews.github.io/", "https://aicatnews.github.io/page/2/"],
        )

    def test_map_changed_files_to_urls_includes_home_and_tutorial_pages(self):
        from scripts import indexnow_submit

        urls = indexnow_submit.map_changed_files_to_urls(
            changed_files=[
                "_pages/tutorials.md",
                "_tutorials/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learnin.md",
                "assets/js/common.js",
            ],
            host="aicatnews.github.io",
        )

        self.assertIn("https://aicatnews.github.io/", urls)
        self.assertIn(
            "https://aicatnews.github.io/tutorials/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learnin/",
            urls,
        )
        self.assertEqual(urls.count("https://aicatnews.github.io/"), 1)

    def test_read_host_from_config_trims_inline_comment_whitespace(self):
        from scripts import indexnow_submit

        with tempfile.TemporaryDirectory() as tmpdir:
            config = Path(tmpdir) / "_config.yml"
            config.write_text(
                'url: https://aicatnews.github.io # the base hostname & protocol for your site\n',
                encoding="utf-8",
            )

            host = indexnow_submit.read_host_from_config(config)

        self.assertEqual(host, "aicatnews.github.io")


if __name__ == "__main__":
    unittest.main()
