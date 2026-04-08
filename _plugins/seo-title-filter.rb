module Jekyll
  module SeoTitleFilter
    PHRASE_REPLACEMENTS = [
      [/\AA Concise Review of\s+/i, ''],
      [/\AA Survey on\s+/i, ''],
      [/\AAn Empirical Study of\s+/i, ''],
      [/\AThe 2025\s+/i, '2025 '],
      ['Large Language Models', 'LLMs'],
      ['Large Language Model', 'LLM'],
      ['Reinforcement Learning', 'RL'],
      ['Retrieval-Augmented Generation', 'RAG'],
      ['retrieval-augmented generation', 'RAG'],
      ['Multimodal Retrieval-Augmented Generation', 'Multimodal RAG'],
      ['Open Language Models', 'Open LMs'],
      ['Open Source', 'Open-Source'],
      ['Open source', 'Open-Source'],
      ['Open-Weight', 'Open-Weight'],
      ['Open weight', 'Open-Weight'],
      ['Multi-agent', 'Multi-Agent'],
      ['multi-agent', 'multi-agent'],
      ['Sensitive to the Motives Behind Communication', 'Sensitive to Communication Motives'],
      ['A Guide to Secure Plan-then-Execute Implementations', 'Secure Plan-then-Execute'],
      ['From Data-centric Perspectives', 'Data-Centric View'],
      ['their Mitigation', 'Mitigation'],
      ['through', 'via'],
      ['Through', 'Via'],
      [' and ', ' & ']
    ].freeze

    DELIMITERS = [':', ',', ' via ', ' with ', ' for ', ' from ', ' in ', ' on ', ' and ', ' & '].freeze
    TRAILING_STOPWORDS = %w[a an and as at by for from in of on or the to via with].freeze

    module_function

    def seo_title(title, max_length = 47)
      max_length = max_length.to_i
      return '' if title.nil?

      normalized = normalize(title)
      return normalized if normalized.length <= max_length

      replaced = apply_replacements(normalized)
      return replaced if replaced.length <= max_length

      if replaced.include?(':')
        prefix, subtitle = replaced.split(':', 2).map { |part| normalize(part) }
        best = prefix if prefix.length <= max_length

        subtitle_limit = max_length - prefix.length - 2
        if subtitle_limit > 8
          shortened_subtitle = shorten_subtitle(subtitle, subtitle_limit)
          combined = normalize("#{prefix}: #{shortened_subtitle}")
          if combined.length <= max_length && combined.length > (best || '').length
            best = combined
          end
        end

        return best unless best.nil? || best.empty?
      end

      trim_to_limit(replaced, max_length)
    end

    def shorten_subtitle(subtitle, max_length)
      subtitle = remove_leading_article(apply_replacements(normalize(subtitle)))
      candidates = [subtitle]

      DELIMITERS.each do |delimiter|
        next unless subtitle.include?(delimiter)

        candidates << subtitle.split(delimiter, 2).first
      end

      candidates.map! { |candidate| trim_to_limit(candidate, max_length) }
      candidates.reject!(&:empty?)
      candidates.select! { |candidate| candidate.length <= max_length }

      candidates.max_by(&:length) || trim_to_limit(subtitle, max_length)
    end

    def apply_replacements(text)
      updated = text.dup

      PHRASE_REPLACEMENTS.each do |source, target|
        updated = updated.gsub(source, target)
      end

      updated = updated.gsub(/\bLLM \(LLM\)\b/, 'LLM')
      updated = updated.gsub(/\bLLMs \(LLMs\)\b/, 'LLMs')
      normalize(updated)
    end

    def trim_to_limit(text, max_length)
      cleaned = normalize(text)
      return cleaned if cleaned.length <= max_length

      words = cleaned.split(' ')
      kept = []

      words.each do |word|
        candidate = (kept + [word]).join(' ')
        break if candidate.length > max_length

        kept << word
      end

      while kept.any? && TRAILING_STOPWORDS.include?(kept.last.downcase)
        kept.pop
      end

      result = normalize(kept.join(' '))
      result.empty? ? cleaned[0, max_length].strip : result
    end

    def remove_leading_article(text)
      text.sub(/\A(?:a|an|the)\s+/i, '')
    end

    def normalize(text)
      text.to_s.gsub(/\s+/, ' ').strip.gsub(/[\s:,-]+\z/, '')
    end
  end
end

Liquid::Template.register_filter(Jekyll::SeoTitleFilter)
