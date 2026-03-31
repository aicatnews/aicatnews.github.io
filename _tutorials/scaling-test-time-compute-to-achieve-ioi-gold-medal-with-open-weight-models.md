---
layout: default
title: "Scaling Test-Time Compute to Achieve IOI Gold Medal with Open-Weight Models"
---


- **ArXiv URL**: http://arxiv.org/abs/2510.14232v1

- **Authors**: Mehrzad Samadi; Aleksander Ficek; Boris Ginsburg; Sean Narenthiran; Somshubra Majumdar; Wasi Uddin Ahmad; Siddhartha Jain

- **Publisher**: NVIDIA

---

## TL;DR
This paper shows that by applying large-scale test-time search to open-source code large language models, such as Code Llama-70B, it is possible to reach gold-medal performance on algorithmic problems at the International Olympiad in Informatics (IOI) level—a feat previously thought to be achievable only by top-tier proprietary models.

## Key Definitions
The core method in this paper is built on AlphaCode 2 and applies it to open-source models. The key definitions are as follows:

1.  **Test-Time Compute/Search**: Refers to investing substantial compute during the model inference stage, rather than during training. In this paper, it specifically denotes a multi-step process: first generating a massive number of candidate code solutions from the model (up to one million), then intelligently selecting the best solution from the huge sample space through a series of filtering, clustering, and reranking steps.
2.  **AlphaCode 2-style search**: A powerful test-time search algorithm whose workflow mainly includes: (1) **Large-scale sampling**: generating a large amount of diverse code. (2) **Filtering**: using the public test cases provided in the problem statement to eliminate incorrect code. (3) **Clustering**: grouping the filtered code by the underlying algorithmic logic to identify distinct solutions. (4) **Reranking**: using an independent scoring model to evaluate representative code from each cluster and select the final answer most likely to be correct on hidden test cases.
3.  **Scoring Model**: A specially trained, smaller language model. Its task is not to generate code, but to estimate the probability that a given code solution is correct for a specific problem statement. In this paper, a 7B-parameter model is used as the scorer to evaluate and rank the clustered candidate solutions.

## Related Work
In prior research, using large language models (LLMs) to solve competition-level programming problems has made significant progress. Early methods relied on simple beam search or a small number of samples ($$pass@k$$). Later, DeepMind’s AlphaCode first introduced the paradigm of large-scale sampling and search, greatly improving problem-solving ability by generating millions of samples and filtering them.

However, the field’s highest performance has long been held by systems based on top-tier proprietary models, such as Google’s Gemini, like AlphaCode 2. These systems have demonstrated capabilities on platforms such as Codeforces that approach or even surpass those of the best human competitors. This raises a key question: **there is a huge performance gap between open-source models and these top proprietary models, and it remains unclear whether open-source models have the potential to reach the same level.**

This paper aims to address this question by exploring whether combining powerful test-time compute strategies with the strongest existing open-source code models can close this performance gap and achieve world-class algorithmic problem-solving ability without relying on next-generation proprietary models.

## Method
The core of this paper is a search-enhanced LLM system based on open-source models. The system borrows from and improves upon the design of AlphaCode 2, demonstrating that by scaling test-time compute, a powerful publicly available model (Code Llama-70B) can also reach elite-level performance. The method mainly consists of the following steps:

### Core Idea: Search Instead of Single-Shot Generation
Unlike traditional one-shot or few-shot code generation, the core of this method is breadth-first exploration. The system first generates a huge, diverse pool of solutions, then gradually converges on the single most likely correct solution through a series of intelligent filtering and selection mechanisms. This approach acknowledges that the correctness rate of any single sample may be low, but believes that among enough samples, the correct solution exists and can be identified by subsequent steps.

### Step 1: Ultra-Large-Scale Code Sampling
The system is built on an instruction-tuned Code Llama-70B model. For each programming problem, it samples with a relatively high temperature $$T$$ (for example, $$T=1.2$$), generating up to one million ($$N = 10^6$$) candidate Python code solutions. The high temperature is used to ensure diversity among the generated samples, thereby covering more possible algorithmic ideas.

### Step 2: Filtering Based on Public Test Cases
This is the most efficient screening stage. Each programming problem usually provides a few simple public test cases. The system executes all $$N$$ generated code samples and runs them on these public test cases. Any code that fails to pass all public test cases is discarded immediately. This step filters out the vast majority of code with syntax errors, logical flaws, or a failure to understand the basic requirements of the problem, reducing the number of candidate solutions from the million scale to thousands or even hundreds.

### Step 3: Behavior-Based Clustering
Although the filtered code behaves consistently on the public test cases, the underlying algorithmic logic may be completely different. To identify these fundamentally distinct solutions, the system uses a behavior-based clustering method. It generates some new, simple inputs and observes the output of each code sample on those inputs. Code with the same behavior (i.e., the same input-output pairs) is grouped into one cluster. The purpose of clustering is deduplication, ensuring that each cluster represents a unique algorithmic implementation and avoiding repeated evaluation of the same logic due to minor differences in variable names or coding style.

### Step 4: Reranking and Selection Based on the Scoring Model
After clustering, the system selects one representative sample from each cluster. At this point, the number of candidate solutions has been greatly reduced, and each one represents a unique algorithm that has passed the public tests. The final step is to decide which one is the “best” answer.

To do this, the system uses a specially trained, smaller **scoring model** (a 7B-parameter Llama model). The model takes the problem description and candidate code as input and outputs a score between 0 and 1, representing the probability that the code is fully correct on the hidden test cases. The system uses this scoring model to score the representative code from each cluster and ultimately selects the one with the highest score as the final submission.

### Innovation
The innovation of this paper is not in proposing a brand-new model architecture, but in **systematically validating the feasibility and huge potential of applying large-scale test-time search strategies to the strongest existing open-source models**. It shows that models like Code Llama-70B already contain the ability to solve complex algorithmic problems, but this ability needs to be “mined” and “refined” through a powerful search process. This work shifts the field’s focus from “we must rely on larger, stronger proprietary models” to “applying smarter, larger-scale search algorithms to sufficiently good open-source models is also a viable path to SOTA.”

## Experimental Conclusions
Through experiments on two highly challenging competitive programming datasets, this paper strongly validates the effectiveness of its method.

### Key Experimental Results
1.  **International Olympiad in Informatics (IOI) Dataset**: In an evaluation containing recent IOI contest problems, the system in this paper (based on Code Llama-70B, with sampling $$N=1M$$) achieved an average score of 29.8 points on 40 problems. This score already reaches the level required to win a **gold medal** in an actual IOI competition. This is the first demonstration that an open-source model system can compete with elite human contestants in the world’s top algorithmic competition.

2.  **CodeContests Dataset**: On the benchmark dataset used by DeepMind to evaluate AlphaCode, the system in this paper solved an average of 10.6 out of 13.9 problems. This result is very close to the performance of the original AlphaCode 2 (based on the more powerful proprietary Gemini model) and significantly surpasses all previous methods based on public models.

### Advantages of Verification
*   **Open-source models have enormous potential**: The experimental results most strongly demonstrate that, by scaling up test-time computation, open-source models can achieve performance comparable to top-tier proprietary models. A model’s “potential” can be effectively unlocked through search algorithms.
*   **Trading compute scale for performance**: The study shows a clear log-linear relationship between the model’s final performance (solve rate) and the number of samples $$N$$. In other words, the more computational resources invested in sampling search, the more significant the return in performance improvement, up to the saturation point.
*   **Every stage of the search pipeline is indispensable**: Through ablation studies, this paper proves that each step in its method pipeline—filtering, clustering, and reranking—is crucial. Simply increasing the number of samples without intelligent selection yields only very limited performance gains. In particular, reranking with a scoring model plays a decisive role in determining whether the correct solution can ultimately be selected.

### Final Conclusion
The conclusion of this paper is clear and compelling: by combining large-scale test-time search algorithms with today’s state-of-the-art open-source code models, it is possible to reach world-class performance on competitive programming tasks, which are regarded as a “litmus test” for algorithmic reasoning ability. This finding suggests that future breakthroughs on complex reasoning tasks can be achieved not only by developing larger foundation models, but also by designing and scaling more efficient and intelligent search algorithms. This work opens up a new path for the open-source community to leverage existing models to tackle more difficult AI tasks.