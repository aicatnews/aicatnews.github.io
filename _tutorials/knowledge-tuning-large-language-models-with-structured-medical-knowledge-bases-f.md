---
layout: default
title: "Knowledge-tuning Large Language Models with Structured Medical Knowledge Bases for Reliable Response Generation in Chinese"
---
## Accuracy Soars to 86.7%! HIT Releases “Knowledge-tuning” to Tackle Medical LLMs That “Sound Serious While Talking Nonsense”

<img src="/images/2309.04175v1/A__title.jpg" alt="" style="width:90%; max-width:700px; margin:auto; display:block;">

When an AI large model was asked about drugs for treating “hepatic bile duct stones,” it recommended “rifampin,” a drug used to treat tuberculosis. This real case exposes a fatal problem: in specialized domains, especially in the life-and-death field of medicine, general-purpose large models may produce serious “hallucination.”

> ArXiv URL：http://arxiv.org/abs/2309.04175v1

How can we make AI doctors both knowledgeable and reliable?

Researchers at Harbin Institute of Technology gave a compelling answer. They proposed a new method called **Knowledge-tuning**, which teaches large models to act like experts: first consult authoritative sources, then give a rigorous answer.

### Why Do Medical Large Models “Make Mistakes”?

Large models are powerful, but their knowledge mainly comes from massive amounts of general internet text.

As a result, when faced with highly specialized medical questions, they often lack sufficient knowledge and may “go by intuition” to fabricate facts, which is what we commonly call “hallucination.”

Traditional methods, such as simple instruction fine-tuning, merely “feed” medical dialogue data to the model, but it is hard to ensure that the model truly digests and understands the knowledge, let alone eliminate the generation of incorrect information.

### “Knowledge-tuning”: Teaching Large Models to “Look Things Up”

To solve this problem, the research team proposed **Knowledge-tuning**, an innovative paradigm.

Its core idea is very clever: instead of forcing the model to “memorize” all medical knowledge, it teaches the model a more important skill—how to proactively and accurately query a structured medical knowledge base.

The whole process is divided into three stages, as shown below:

![知识调优流程图](images/page_3_Figure_2.jpg)

1.  **Understand the question and generate a query**: When the model receives a question (such as “What are the symptoms of cicatricial pyloric obstruction?”), it first predicts the core **medical entity** (such as “cicatricial pyloric obstruction”) and **attribute** (such as “clinical manifestations”).

2.  **Precisely retrieve knowledge**: Using the entity and attribute generated in the previous step, the model automatically queries the structured medical knowledge base to accurately find the relevant knowledge entries.

3.  **Refer to the knowledge and generate an answer**: Finally, based on the retrieved authoritative knowledge, the model generates an answer that is both natural and fluent while remaining faithful to the facts.

In this way, the model’s answers not only have a reliable knowledge source, but also greatly reduce the risk of hallucination.

### cMedKnowQA: The First Chinese Medical Knowledge Question-Answering Dataset

To train and evaluate the model, the research team also built and open-sourced the first Chinese medical knowledge question-answering dataset, **cMedKnowQA**.

The dataset contains 7,449 high-quality question-answer pairs, and each pair strictly corresponds to an entry in a structured medical knowledge base. This provides a valuable resource for future research on medical large models.

![cMedKnowQA数据集示例](images/page_3_Figure_0.jpg)

### How Effective Are the Experiments?

The proof of the pudding is in the eating. The researchers conducted experiments on mainstream models such as LLaMA and Bloom.

To evaluate the models more scientifically, they abandoned traditional metrics such as BLEU and introduced the **H2** (**Helpfulness & Harmlessness**) scoring system, judged by medical experts, to assess the models from two dimensions: helpfulness and harmlessness.

The results were impressive:

- **More accurate knowledge retrieval**: The knowledge-tuned model achieved an accuracy of **86.7%** in predicting medical entities, and **71.4%** in retrieving relevant knowledge, far surpassing traditional retrieval methods.

- **Higher answer quality**: In expert H2 evaluations, the knowledge-tuned model significantly outperformed baseline models in both helpfulness and harmlessness, proving that its answers are more professional and trustworthy.

![模型响应质量评估](images/page_6_Figure_10.jpg)

More importantly, Knowledge-tuning demonstrated strong few-shot learning and generalization capabilities.

Even with only a small amount of training data, the model could quickly learn knowledge retrieval skills.

![小样本学习能力](images/page_6_Figure_10.jpg)

At the same time, the model could transfer the learned ability to new diseases unseen during training, showing good generalization.

![对未见实体的泛化能力](images/page_6_Figure_15.jpg)

### Conclusion

The “Knowledge-tuning” method proposed in this study provides a clear and effective path to solving the problem of knowledge accuracy in large models for specialized domains.

By teaching the model how to “look up” information rather than “memorize it by rote,” it cleverly combines the language ability of large models with the accuracy of structured knowledge bases.

This not only paves the way for building more reliable Chinese medical large models, but also offers important insights for the deployment of large models in other specialized fields such as law and finance. Perhaps in the not-too-distant future, we will have a truly trustworthy AI family doctor.