---
layout: default
title: "QAgent: A modular Search Agent with Interactive Query Understanding"
---


- **ArXiv URL**: http://arxiv.org/abs/2510.08383v1

- **Author**: Wenbo Su; Lei Shen; Bo Zheng; Sendong Zhao; Yi Jiang

- **Publishing Organization**: Alibaba

---

## TL;DR
This paper proposes QAgent, a unified Agentic RAG framework that performs interactive query understanding and adaptive retrieval through a modular search intelligent agent trained with a two-stage reinforcement learning strategy, thereby improving retrieval quality for complex questions and its generalization as a plug-and-play module.

## Key Definitions
*   **QAgent**: The unified Agentic RAG framework proposed in this paper. Its core is a modular search intelligent agent that optimizes understanding of complex queries through multi-turn interactive reasoning and retrieval, with the goal of being deployed as a plug-and-play module in complex systems.
*   **Agentic RAG**: An extension of the traditional retrieve-then-read paradigm. It models the search process as a sequential decision-making problem, where the intelligent agent decides when and what to retrieve through multi-step dynamic reasoning and interaction with the environment.
*   **End-to-End RL Training**: The first-stage training strategy of QAgent. In this stage, the training objective of the intelligent agent is to maximize end-to-end rewards based on the correctness of the final answer. This method jointly optimizes the intelligent agent’s information retrieval and information utilization capabilities.
*   **Generalized RL Training**: The second-stage training strategy of QAgent. To improve the intelligent agent’s generalization as a “submodule,” this stage uses a fixed (frozen) generator to produce answers and computes rewards based on that generator’s responses. This forces the intelligent agent to focus on improving the quality of the retrieved information itself rather than its own ability to use information, thereby avoiding the reward hacking problem.
*   **Multi-Turn Query Optimation Loop**: The core workflow of the QAgent intelligent agent. In a plan-search-information-reflect loop, the intelligent agent autonomously generates, executes, and evaluates retrieval actions, progressively deepening its understanding of complex user intent through multi-turn interaction and constructing an accurate search path.

## Related Work
At present, large language models face challenges such as outdated knowledge and hallucination when handling knowledge-intensive tasks. Retrieval-Augmented Generation (RAG) alleviates these issues by introducing external knowledge, but the traditional retrieve-then-read workflow is too rigid to handle complex queries that require multi-step reasoning.

To improve flexibility, recent work has introduced methods such as query optimization, planning, reflection, and iterative retrieval, forming the prototype of Agentic RAG. However, most of these methods lack effective feedback and continuous optimization mechanisms. Reinforcement Learning (RL)-based search intelligent agents (such as Search-R1) have demonstrated strong autonomous reasoning and decision-making abilities, but they still face two major bottlenecks in practical applications:
1.  **Insufficient understanding of complex queries**: Directly using the original query for retrieval often fails to obtain useful information.
2.  **Limited generalization ability**: Existing RL training methods usually optimize retrieval and generation end to end, causing the intelligent agent to overfit the “information utilization” stage rather than focusing on improving the core “information retrieval” capability, which leads to performance degradation when deployed as an independent submodule.

This paper aims to address the above issues, with the core objectives of:
1.  Designing a search intelligent agent that can understand and decompose complex queries to bridge the gap between user intent and retriever capability.
2.  Proposing a training strategy that ensures the intelligent agent has strong generalization when used as a plug-and-play submodule, focusing on providing high-quality information for downstream tasks.

## Method
This paper proposes a unified intelligent agent framework called QAgent, whose core is a search intelligent agent that performs reasoning and retrieval through a multi-turn interaction loop, and is optimized with an innovative two-stage training strategy.

![](acl_latex/imgs/framework.png)

### Innovations
The core innovation of this method lies in its **two-stage training strategy designed to improve generalization**, which explicitly positions the search intelligent agent as an independent module focused on “information retrieval” rather than an end-to-end question answering system.

#### Multi-Turn Query Optimation Loop
The workflow of QAgent is modeled as a sequential decision process, in which the intelligent agent interacts with the retrieval system over multiple turns in a loop.
![](acl_latex/imgs/query.png)

At each turn $t$, the intelligent agent follows these steps:
1.  **Plan ($I^{pre}\_{t}$)**: Plan based on historical information and the original query $q$.
2.  **Generate search queries ($S\_t$)**: Generate a set of optimized queries $\{q\_{t,1}, \dots, q\_{t,m\_t}\}$.
3.  **Retrieve and integrate ($C\_t$)**: Execute the search and aggregate the documents returned by all queries to form the context $C\_t = \oplus\_{j=1}^{m\_i} \mathcal{R}(q\_{ij})$.
4.  **Reflect ($I^{post}\_{t}$)**: Evaluate whether the currently accumulated information is sufficient to answer the question, and decide whether to continue to the next round of interaction or stop.

The entire process forms a trajectory $\tau=(q,I^{pre}\_{1},S\_{1},\mathcal{C}\_{1},I^{post}\_{1},\dots,\mathcal{C}\_{T},I^{post}\_{T},\hat{A})$. This flexible interaction pattern allows the intelligent agent to dynamically adjust its search strategy according to context, addressing different types of complex queries.

#### Two-Stage Reinforcement Learning Training Strategy

To address the problem of insufficient generalization in existing RL training of intelligent agents, this paper designs a two-stage training process.

**Stage 1: End-to-End Reinforcement Learning Training**

The goal of this stage is to enable the intelligent agent to initially learn how to solve problems through search. Training is conducted in an end-to-end manner, and the reward function is directly tied to the correctness of the final answer $\hat{A}$:


{% raw %}$$
R(\tau)=\mathbb{I}\{r_{\mathrm{fmt}}(\tau)=1\}\cdot\mathrm{EM\_{s}}(A^{\*},\hat{A}).
$${% endraw %}


where $A^\*$ is the ground-truth answer, and $\mathrm{EM\_s}$ denotes strict exact match. This approach can improve both the intelligent agent’s information retrieval and information utilization capabilities. However, the paper finds that in the later stages of training, the model tends to “hack” the reward by improving its own “information utilization” ability rather than continuing to optimize “information retrieval,” which harms its generalization as a general retrieval module.

![](acl_latex/imgs/case_SearchR1.png)


**Stage 2: Generalized Reinforcement Learning Training**

This is the core of the paper’s method, aimed at training the intelligent agent into a “submodule” focused on information retrieval. Its key design is to **decouple retrieval from generation**:
1.  The intelligent agent performs search and collects a document set $\mathcal{K}$.
2.  A **fixed (frozen)** generator $\mathcal{G}$, independent of the intelligent agent, is used to generate an answer based on $\mathcal{K}$ and the original query $q$: $\tilde{A} = \mathcal{G}(q, \mathcal{K})$.
3.  The reward function is computed based on the external generator’s answer $\tilde{A}$, rather than the intelligent agent’s own answer:


{% raw %}$$
R(\tau)=\mathrm{EM}(A^{\*},\tilde{A})+0.5*Hit(\tau,A^{\*})
$${% endraw %}


where EM is non-strict exact match, and Hit indicates whether the ground-truth answer appears in the intelligent agent’s complete trajectory.

**Advantages**

The core advantages of this two-stage design are:
*   **Improved generalization**: Since the reward depends entirely on whether the retrieved information enables a **general, fixed** generator to produce the correct answer, the intelligent agent is forced to focus on improving the quality and completeness of the retrieved content, rather than learning how to cleverly use imperfect information to piece together an answer. This allows the trained intelligent agent to function as a plug-and-play module that efficiently serves different downstream generators.
*   **Mitigating reward hacking**: By introducing an external fixed generator as the “judge,” the tendency of the intelligent agent to over-optimize its own information utilization ability in end-to-end training to obtain higher rewards is effectively avoided.
*   **Modularity and practicality**: The trained QAgent is a lightweight search module that can be flexibly combined with generators of different sizes and capabilities, meeting the deployment needs of real-world complex systems.

## Experimental Conclusions

Experiments were conducted on multiple open-domain question answering datasets, including both multi-hop and single-hop settings, validating QAgent’s performance and generalization ability.

### Main Results

**1. End-to-End QA Performance**

As shown in the table below, QAgent performs excellently on end-to-end question answering tasks. Compared with Search-R1, which is also trained based on RL, it improves the average EM and F1 scores by 0.52% and 2.66%, respectively. This demonstrates the overall effectiveness of the QAgent framework.

<br>


| Method | 2WikiMHQ | HotpotQA | Musique | NQ | TQA | Avg |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
|      | EM/F1    | EM/F1    | EM/F1   | EM/F1  | EM/F1 | EM/F1  |
| Vanilla | 12.0/20.8 | 13.0/22.4 | 4.8/10.0 | 22.8/30.3 | 25.6/31.0 | 15.6/22.9 |
| Naive RAG | 23.4/31.3 | 47.0/59.6 | 13.0/20.2 | 34.4/43.6 | 45.4/52.5 | 32.6/41.4 |
| Search-o1 | 37.0/49.4 | 48.2/60.8 | **27.6**/**36.7** | 51.6/60.3 | 49.8/57.9 | 42.8/53.0 |
| ZeroSearch | 30.6/43.8 | 39.4/52.9 | 20.6/30.1 | 48.0/59.3 | 43.8/54.5 | 36.5/48.1 |
| Search-R1 | 41.2/54.2 | 51.2/64.2 | 26.8/35.0 | 52.6/62.3 | **54.0**/62.4 | 45.2/55.6 |
| **QAgent (this paper)** | **42.2**/**55.4** | **52.6**/**66.1** | 27.2/35.8 | **52.8**/**63.8** | 53.6/**63.1** | **45.7**/**56.8** |

<br>

**2. Performance as a Submodule (Generalization Ability)**

This is the core of the experiment. As shown in the table below, when the agents trained by different methods are used as independent retrieval modules and paired with a fixed generator, QAgent’s advantage becomes extremely clear. Its average EM score is 4.59% higher than Search-R1 and 5.35% higher than Naive RAG. This strongly demonstrates the success of the **second-stage generalization training**. QAgent has excellent generalization ability and can serve as an efficient plug-and-play module.

<br>


| Method | Generator | 2WikiMHQ | HotpotQA | Musique | NQ | TQA | Avg |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
|      |        | EM       | EM       | EM      | EM   | EM  | EM     |
| Naive RAG | 3B | 23.4 | 47.0 | 13.0 | 34.4 | 45.4 | 32.6 |
| ReRank | 3B | 30.4 | 49.2 | 16.4 | 39.0 | 47.2 | 36.4 |
| Search-o1 | 3B | 31.6 | 46.8 | 17.6 | 36.2 | 43.6 | 35.2 |
| ZeroSearch | 3B | 27.6 | 41.6 | 14.8 | 39.4 | 41.2 | 32.9 |
| Search-R1 | 3B | 29.8 | 46.0 | 15.8 | 36.0 | 45.0 | 34.5 |
| **QAgent (this paper)** | 3B | **35.0** | **49.8** | **18.2** | **40.4** | **49.2** | **38.5** |
| QAgent (this paper) | 7B | **40.8** | **55.4** | **23.2** | **49.2** | **57.4** | **45.2** |

<br>

### Analysis and Insights
*   **Ablation study**: This confirms the necessity of two-stage training. Stage one (end-to-end) brings significant gains, while stage two (generalization training) plays a decisive role in improving the model’s generalization ability, especially on out-of-distribution datasets.

<br>


| Training Stage | 2WikiMHQ | HotpotQA | Musique | NQ | TQA |
| :--- | :--- | :--- | :--- | :--- | :--- |
|      | EM/F1    | EM/F1    | EM/F1   | EM/F1  | EM/F1 |
| No training | 37.0/49.4 | 48.2/60.8 | **27.6**/**36.7** | 51.6/60.3 | 49.8/57.9 |
| Stage one | 41.0/53.5 | 50.8/63.6 | 26.6/34.9 | 52.4/62.2 | 53.4/61.9 |
| **Stage two (QAgent)** | **42.2**/**55.4** | **52.6**/**66.1** | 27.2/35.8 | **52.8**/**63.8** | **53.6**/**63.1** |

<br>

*   **Combined gain analysis**: The experiments show that through multi-turn query optimization by the agent, QAgent can achieve “combined gains” that go beyond the traditional RAG paradigm, even when the number of retrieved documents is increased, effectively breaking through the upper limit of a single retriever’s capability.
![](acl_latex/imgs/upper_gain_v3.png)


*   **Information utilization analysis**: This validates the core motivation of the paper. The model trained end-to-end has the strongest information utilization ability, but this ability declines after generalization training. This precisely shows that generalization training successfully shifts the model’s optimization objective from “using information” to “retrieving information,” thereby improving its generalization as a retrieval module.
![](acl_latex/imgs/info.png)

### Summary
The experimental results fully demonstrate that QAgent, through its innovative two-stage training strategy, successfully trains a modular search agent that performs excellently on complex question answering tasks and has strong generalization ability. It not only achieves leading results on end-to-end tasks, but more importantly, it can be efficiently integrated into large systems as a plug-and-play component, providing a reliable solution for real-world RAG applications.