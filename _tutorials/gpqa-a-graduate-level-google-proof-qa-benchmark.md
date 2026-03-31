---
layout: default
title: "GPQA: A Graduate-Level Google-Proof Q&A Benchmark"
---


- **ArXiv URL**: http://arxiv.org/abs/2311.12022v1

- **Authors**: Asa Cooper Stickland; Richard Yuanzhe Pang; Julien Dirani; Jackson Petty; David Rein; Samuel R. Bowman; Julian Michael; Betty Li Hou

- **Publishing Organizations**: Anthropic; Cohere; New York University

---

## TL;DR
This paper introduces GPQA, a 448-question graduate-level multiple-choice dataset written by experts in biology, physics, and chemistry. It is designed to be “Google-Proof,” meaning it is extremely difficult even for skilled non-experts with unrestricted internet access, and is intended to provide a highly challenging benchmark for future research on scalable oversight for superhuman AI systems.

## Key Definitions
*   **GPQA**: A high-quality, high-difficulty question-answering benchmark dataset. It contains multiple-choice questions written by PhD-level experts in biology, physics, and chemistry.
*   **Google-Proof Questions**: Questions that are difficult to answer correctly even for highly skilled non-experts with ample time and unrestricted access to the internet. In GPQA, these non-experts (PhDs in other fields) spent over 30 minutes on average, but achieved only 34% accuracy.
*   **Scalable Oversight**: A core problem in AI safety that asks how humans with limited capability can effectively and reliably supervise AI systems that far exceed their own abilities, ensuring that AI outputs are truthful and beneficial, especially in scenarios such as exploring entirely new scientific knowledge where humans cannot independently verify the answers.
*   **Expert** and **Non-Expert**: In this paper, “expert” refers to an individual who holds or is pursuing a PhD in the field relevant to the question (e.g., organic chemistry). A “non-expert” is also highly skilled (holding or pursuing a PhD), but their field of expertise differs from the question’s domain (e.g., a physics expert answering a biology question).

## Related Work
Mainstream question-answering (QA) benchmark datasets are typically created either by crowdsourcing non-experts (e.g., SQuAD) or by curating existing resources (e.g., MMLU, TriviaQA). The answers to these datasets can usually be easily found and verified by skilled users through web search. As large language model (LLM) capabilities have advanced rapidly, they have gradually saturated these benchmarks, reducing the usefulness of these datasets for evaluating frontier models and studying more advanced human-AI collaboration, such as scalable oversight.

Research on scalable oversight requires a special kind of task: one whose correct answer is definitively known (determined by authoritative experts), yet is extremely difficult for the non-experts responsible for supervision to solve independently. Existing datasets either lack this “difficulty gap” or merely simulate a knowledge gap in an artificial way (for example, by distinguishing experts from non-experts based on familiarity with long articles).

This paper aims to address this issue by creating a benchmark of real-world expert-knowledge questions (GPQA) that pose major challenges to both non-experts and the strongest current AI models, thereby providing a realistic and meaningful testbed for studying how to supervise superhuman AI systems.

## Method
The core contribution of this paper lies in its distinctive and rigorous dataset construction and validation pipeline. The process is designed to systematically generate questions that are both objective (with clear answers) and highly difficult (Google-Proof).

<img src="/images/2311.12022v1/page_2_Figure_0.jpg" alt="Data creation flowchart" style="width:85%; max-width:450px; margin:auto; display:block;">
*Figure 1: The data creation process in this paper. First, one expert writes a question, and another expert in the same field answers it and provides revision suggestions. The writer then revises the question. The revised question is sent to a second expert in the same field and three non-expert validators.*

### Data Collection Pipeline
The entire process is divided into four main stages:

1.  **Question Writing**: Experts with or pursuing a PhD in the relevant field are invited to write difficult questions within their area of expertise. The requirement is that experts in the same field should be able to answer them correctly, but non-experts should find them difficult to answer even with internet access. The questions are designed so that they can be answered in free-response form even without options. In addition, the writer must provide detailed explanations for both the correct and incorrect options.

2.  **First Expert Validation**: The completed questions are given to another expert in the same field (the first validator) to answer and evaluate. The validator provides detailed feedback to ensure the questions’ accuracy, objectivity, and difficulty.

3.  **Question Revision**: The question writer revises the questions based on the first validator’s feedback.

4.  **Second Validation Phase**:
    *   **Second Expert Validation**: The revised questions are given to a third expert in the same field (the second validator) to answer, further testing their objectivity.
    *   **Non-Expert Validation**: At the same time, the questions are distributed to three non-experts (i.e., PhDs in other fields). They are allowed unrestricted use of all web resources except LLM assistants and are required to spend at least 15 minutes solving them. This step is key to verifying whether the questions are truly “Google-Proof.”

### Innovations
*   **Validation Design Centered on “Google-Proofing”**: Unlike traditional datasets, GPQA’s pipeline includes a crucial “non-expert validation” stage. This stage specifically tests whether highly skilled users can still fail to solve the questions in an open web environment. This ensures that the dataset’s difficulty is not merely a matter of information retrieval, but a genuine barrier of knowledge and reasoning.

*   **Multiple Expert Validations Ensure Objectivity**: By using a closed loop of “write-validate-revise-revalidate,” involving three independent domain experts (1 writer, 2 validators), the process greatly increases the likelihood that even extremely difficult questions have objective, uncontroversial ground-truth answers.

*   **Sophisticated Incentive Mechanism**: A quality-based bonus system is used to motivate all participants. The question writer’s bonus is directly tied to the “expert validation pass rate” (ensuring objectivity) and the “non-expert validation failure rate” (ensuring difficulty), effectively guiding them to produce high-quality questions.

### Dataset Splits
The final collected data are divided into three subsets to suit different research needs:


| Dataset Split | Count | Expert Accuracy (%) | Non-Expert Accuracy (%) | Proportion of Experts Who Considered It Sufficiently Specialized (%) |
| --- | --- | --- | --- | --- |
| GPQA Extended | 546 | 64.8 | 34.1 | 90.7 |
| GPQA (Main Set) | 448 | 71.9* | 30.4* | 93.5 |
| GPQA Diamond | 198 | 81.3* | 22.1* | 97.0 |


*Table 2: Statistics for the extended set, main set, and diamond set. The validator accuracies (*) on the main set and diamond set are biased due to selection effects.*

*   **GPQA Extended**: Contains all 546 valid questions collected.
*   **GPQA (Main Set)**: The core dataset, containing 448 questions. It excludes questions that experts generally answered incorrectly or non-experts generally answered correctly, using the criterion that at least half of the experts must agree and no more than two-thirds of the non-experts may answer correctly.
*   **GPQA Diamond**: The highest-quality subset, containing 198 questions. The selection criteria are stricter, requiring both experts to agree and at least two-thirds of non-experts to answer incorrectly.

### Coverage Areas
The questions cover the three major domains of biology, physics, and chemistry, and are further divided into subfields such as molecular biology, quantum mechanics, and organic chemistry.


| Domain | Count | Expert Accuracy (%) | Non-Expert Accuracy (%) | Gap (points) |
| --- | --- | --- | --- | --- |
| Biology | 105 | 66.7 | 43.2 | 23.5 |
| Physics | 227 | 57.3 | 32.5 | 24.8 |
| Chemistry | 214 | 72.0 | 31.4 | 40.6 |


*Table 3: Comparison of expert and non-expert accuracy across domains in the extended set; the “Gap” column shows the expertise gap between the two.*

## Experimental Conclusions
Through a series of analyses and baseline model tests, this paper validated the characteristics of the GPQA dataset and its effectiveness as a benchmark for scalable supervision research.

### Dataset Characteristic Validation
*   **High difficulty ("Google-proof")**: On the extended set, the average accuracy of non-expert validators was only **34.1%** (with random guessing at 25%), even though they spent an average of 37 minutes per question and were free to use the internet. This strongly demonstrates the dataset’s “Google-proof” nature.
*   **High objectivity**: The baseline accuracy of expert validators was **65%**. Through manual analysis of cases where experts answered incorrectly, it was found that in many instances, experts later admitted they had made a mistake rather than there being a problem with the question itself. After removing these obvious errors, the estimated objectivity of the questions (i.e., the proportion with an undisputed correct answer) could reach **74%**.

### Model Baseline Tests
This paper tested multiple LLMs in both closed-book (no internet access) and open-book (with internet access) settings.


| Evaluation Method and Model | Extended Set | Main Set | Diamond Set |
| --- | --- | --- | --- |
| | \multicolumn{3}{c|}{Accuracy on Each Subset (%)} |
| Few-Shot CoT GPT-4 | 38.7 | 39.7 | 38.8 |
| GPT-4 (with search) | 39.4 | 41.0 | 38.8 |
| **Human Expert Validators** | **65.4** | **72.5*** | **81.2*** |
| **Human Non-Expert Validators** | **33.9** | **30.5*** | **21.9*** |


*Table 5: Comparison of the performance of major baseline models and humans across the three datasets.*

*   **A challenge to SOTA models**: Even the current strongest model, GPT-4, achieved only about **39%** accuracy when using few-shot chain-of-thought (Few-Shot CoT) prompting.
*   **Limited benefit from web search**: After giving GPT-4 access to a search engine (open-book testing), its performance improved only marginally, with accuracy rising from 38.7% to **39.4%** (on the extended set). This shows that the questions are deeply challenging and cannot be solved by simple information retrieval.
*   **A key performance gap**: The strongest model, GPT-4, performed significantly below human experts (about 65%) but slightly above human non-experts (about 34%). This performance state, where the model sits between non-experts and experts, creates an ideal and non-trivial testbed for scalable supervision experiments—namely, non-experts supervising a model that is not fully reliable but may be more capable than themselves.

### Final Conclusion
This paper successfully constructed GPQA, a high-quality, graduate-level question-answering dataset. Through a rigorous multi-stage validation process involving both experts and non-experts, it ensures that the questions are both highly objective and highly difficult in a “Google-proof” sense. The experiments show that the dataset not only poses a major challenge to highly skilled non-experts, but also remains difficult for today’s most advanced AI models, while still exhibiting a substantial gap from domain experts. Therefore, GPQA provides a valuable and realistic benchmark for studying and evaluating scalable supervision methods for future superhuman AI systems.