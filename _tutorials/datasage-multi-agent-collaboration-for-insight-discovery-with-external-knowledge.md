---
layout: default
title: "DataSage: Multi-agent Collaboration for Insight Discovery with External Knowledge Retrieval, Multi-role Debating, and Multi-path Reasoning"
---
## The AI analyst squad is here! ByteDance’s DataSage introduces a debating mechanism, boosting insight by 13.9%

<img src="/images/2511.14299v1/A__title.jpg" alt="" style="width:90%; max-width:700px; margin:auto; display:block;">

AI data analysts sound cool, but in practice they often end up being a headache. They either lack domain-specific background knowledge and make jokes like “the sales drop during the Spring Festival is just random fluctuation,” or they only ask superficial, inconsequential questions, with analysis depth that leaves much to be desired; not to mention the bug-ridden code they churn out all the time that simply won’t run.

> **Paper Title**: DataSage: Multi-agent Collaboration for Insight Discovery with External Knowledge Retrieval, Multi-role Debating, and Multi-path Reasoning
> **ArXiv URL**：http://arxiv.org/abs/2511.14299v1

Faced with these dilemmas, we can’t help but ask: is AI really only capable of being an “intern-level” analyst?

ByteDance’s latest research, DataSage, gives a resounding answer: No! They have built an “analyst squad” composed of multiple AI智能体, and by introducing external knowledge retrieval, multi-role debating, and multi-path reasoning, they have achieved a qualitative leap in AI’s data insight capabilities.

<img src="/images/2511.14299v1/x2.jpg" alt="DataSage框架图" style="width:85%; max-width:450px; margin:auto; display:block;">
*Figure 1: Overview of the DataSage multi-agent framework*

This work directly tackles the three core pain points of current data智能体, making AI analysts truly reliable, insightful, and intelligent.

### Three major “hard problems” of existing data智能体

Before DataSage proposed its solution, let’s first look at the common problems in existing AI data analysis tools:

1.  **Lack of domain knowledge**: The model relies only on its internal knowledge and cannot understand industry-specific context. For example, if it doesn’t know about the external event of the “Spring Festival,” it may incorrectly attribute the drop in holiday sales to product issues.
2.  **Insufficient analytical depth**: Most tools use a one-shot question-asking mode, and the questions they generate tend to stay on the surface, lacking the ability to dig step by step into root causes like human experts do.
3.  **Frequent code errors**: The “hallucination” problem in LLM-generated code still persists. A tiny coding mistake can throw the entire analysis off course, seriously affecting decision-making.

<img src="/images/2511.14299v1/x1.jpg" alt="当前数据智能体的三大局限" style="width:90%; max-width:700px; margin:auto; display:block;">
*Figure 2: Three major limitations of existing data智能体*

It is precisely these issues that limit AI’s use in serious, complex business decision-making scenarios.

### DataSage: an “analyst squad” that can think and debate

To address these pain points, DataSage designed a collaborative workflow with four core modules, using an iterative question-answering (QA) loop to uncover data insights.

It is no longer a lone Agent working by itself, but a team where each member has a clear role and works closely together.

At the heart of the framework are three major innovations, which can be seen as the “secret weapons” that transform AI analysts from the ground up.

### DataSage’s three “secret weapons”

#### 1. External knowledge base: Retrieval-Augmented Knowledge Generation (RAKG)

When faced with a question that may require domain knowledge, DataSage does not just guess blindly.

Its **Retrieval-Augmented Knowledge Generation** (**Retrieval-Augmented Knowledge Generation, RAKG**) module is triggered automatically. It first determines whether external knowledge is needed, then generates search terms, retrieves information through search engines such as Google, and finally integrates the information into structured knowledge to provide crucial context for subsequent analysis.

It is like equipping the AI analyst with an “external brain” that can consult industry reports and background materials at any time.

#### 2. Brainstorming: Multi-role Debating

To improve analytical depth, DataSage introduces a “debating” mechanism in the question-asking stage.

It dynamically designs multiple Agent roles with different perspectives, such as an “optimistic strategist,” a “cautious risk officer,” and a “detail-oriented operations expert.” These roles then engage in a round of “divergent” brainstorming from their own angles, proposing a large number of analytical questions.

Next, a “judge” Agent steps in to perform “convergent” filtering on this pool of questions, selecting the most valuable and insightful ones for the next stage of analysis.

This **Multi-role Debating** mechanism perfectly simulates the collaborative mode of a human expert team, ensuring both breadth and depth in the analysis.

#### 3. Triple safeguard: Multi-path Reasoning and code refinement

To address code generation errors, DataSage adopts a “multi-path reasoning” strategy.

Instead of betting everything on a single code generation attempt, it generates multiple versions of the code at the same time. Then, a dedicated “code review” Agent evaluates and scores these codes, even checking the aesthetics and readability of the generated charts.

If problems are found, a “code repair” Agent performs multiple rounds of modifications until the code quality meets the standard. Finally, the system selects the best code to execute.

This rigorous process greatly improves code accuracy and the reliability of the final insights.

### Experimental results: a comprehensive win, especially on hard tasks

The proof is in the pudding. On the authoritative data insight benchmark InsightBench, DataSage’s performance is truly impressive.


| Model | Insight Score | Summary Score |
| :--- | :---: | :---: |
| GPT-4o only | 45.4 | 43.1 |
| AgentPoirot (SOTA) | 52.3 | 48.1 |
| **DataSage (Ours)** | **56.2** | **54.8** |
| *Improvement* | *+7.5%* | *+13.9%* |

*Table 1: DataSage outperforms the current best model on InsightBench*

The experimental results show:
*   **Overall lead**: DataSage significantly outperforms the previous SOTA model AgentPoirot in both insight score and summary score, with the summary score improving by as much as **+13.9%**.
*   **Excels at hard problems**: On the “hard” dataset, DataSage’s performance advantage is even more pronounced, with the insight score improving by **+9.3%**, demonstrating stronger capability in handling complex problems.
*   **Better charts**: Thanks to the code refinement stage, the data visualization charts generated by DataSage far surpass the baseline model in readability, aesthetics, and accuracy.

<img src="/images/2511.14299v1/x3.jpg" alt="图表质量对比" style="width:85%; max-width:450px; margin:auto; display:block;">
*Figure 3: DataSage generates significantly higher-quality charts*

Ablation studies further confirm that the three components—RAKG, multi-role debating, and multi-path reasoning—are all indispensable, with the **RAKG module** contributing the most to performance, once again highlighting the central role of domain knowledge in data analysis.

### Conclusion

The emergence of DataSage paints a new blueprint for the field of automated data analysis. It shows that by building a multi-agent system that knows how to collaborate, debate, and reflect, we can transform AI from a simple tool executor into a true “data sage” (DataSage) with deep thinking ability.

This research is not only a technical breakthrough; more importantly, it points to a direction for the future development of AI Agent: moving from individual intelligence to collective intelligence, allowing AI to work together like a human expert team. Perhaps the AI analyst squad that can provide us with deep business insights 24/7 is already not far away.