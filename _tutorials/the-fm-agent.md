---
layout: default
title: "The FM Agent"
---


- **ArXiv URL**: http://arxiv.org/abs/2510.26144v1

- **Author**: Dou Shen; Haobo Zhang; Annan Li; Dawei Yin; Chufan Wu; Jianmin Wu; Quan Sun; Yingying Sun; Rui Yang; Mengmeng Zhang

- **Publisher**: Baidu AI Cloud

---

## TL;DR
This paper proposes a general-purpose multi-agent framework called FM Agent, which innovatively combines the reasoning capabilities of large language models (LLM) with large-scale evolutionary search to automatically solve complex real-world challenges across multiple domains, including operations research, machine learning, GPU kernel optimization, and mathematical problems, achieving state-of-the-art (SOTA) results.

## Key Definitions
*   **FM Agent**: A novel, general-purpose multi-agent framework whose core is the combination of LLM-based reasoning and large-scale evolutionary search, aimed at autonomously solving complex scientific and engineering problems.
*   **Cold Start Stage**: The initial stage of the framework, which rapidly generates a diverse and high-quality population of initial solution candidates by integrating multiple generative agent and optional expert guidance, laying the foundation for subsequent evolution.
*   **Evolve Stage**: The core optimization stage of the framework, which adopts an island-based diverse population evolution strategy. In this stage, solution candidates are iteratively innovated and improved through operations such as mutation and crossover.
*   **Island Model**: A multi-population parallel evolution strategy used in the evolution stage. The solution population is split across multiple independent “islands” for parallel evolution, while allowing periodic exchange of individuals between islands (“idea” exchange) to maintain population diversity and avoid local optima.

## Related Work
At present, autonomous AI research agent driven by large language models (LLM) are developing rapidly, and one mainstream direction is to use multiple LLM agent, together with evolutionary or reinforcement-learning-style search loops, to solve complex open-ended problems. However, in industry, high-value domains such as combinatorial optimization, machine learning, and high-performance computing kernel tuning still largely rely on experts with deep domain knowledge to perform manual, project-based iterative optimization when searching for efficient solutions. This process is not only costly, but also difficult to fully automate. Some existing automation methods, such as AI compilers, lack generalization to new tasks because they depend on predefined rules.

The core problem this paper aims to solve is: how to build a general-purpose, scalable AI system that can autonomously solve complex cross-domain problems, thereby reducing dependence on human experts and accelerating scientific discovery and engineering innovation.

## Method
The FM Agent framework is designed as a two-stage autonomous discovery and optimization process, aiming to efficiently solve complex problems. It first generates a diverse pool of initial solutions through the “Cold Start Stage,” and then enters the “Evolve Stage” for large-scale iterative search and optimization. The entire framework is built on a high-performance distributed infrastructure to support large-scale parallel computation.

<img src="/images/2510.26144v1/main.jpg" alt="FM Agent framework overview" style="width:85%; max-width:600px; margin:auto; display:block;">
### Innovations
The core innovation of FM Agent lies in its architectural design, which seamlessly integrates the reasoning capabilities of LLM, the exploratory power of evolutionary computation, and a scalable distributed system.

#### Cold Start Stage
The goal of this stage is to build a highly diverse, high-quality initial population of solution candidates for the subsequent evolutionary search, thereby expanding the global search space and effectively preventing premature convergence.
*   **Parallel exploration by diverse agent**: The system integrates multiple types of generative agent, which can run in parallel with differentiated configurations to explore different generation strategies and optimization directions.
*   **Guided diversity**: By guiding agent to explore different regions of the target space, the coverage of the initial solution candidates is intentionally broadened, creating conditions for subsequent deep optimization.

#### Evolve Stage
The evolution module is the core of FM Agent, which innovates and improves the initial solution candidates through large-scale, population-based search. At its heart is an efficient evolutionary strategy.

<img src="/images/2510.26144v1/evolve-2.jpg" alt="Figure illustration" style="width:85%; max-width:600px; margin:auto; display:block;">

*   **Multi-island evolution**: The framework adopts a multi-island model, dividing solution candidates into multiple parallel “islands.” Most of the time, each island evolves independently, exploring different regions of the solution space; meanwhile, the framework facilitates periodic communication between islands to enable cross-fertilization of “ideas,” preventing the overall search from getting trapped in local optima.
*   **Efficient evolutionary strategy**: The framework uses an adaptive control system to guide evolution within each island. Its key component is a novel **cluster-based sampling strategy**, which dynamically adjusts selection pressure to balance exploration and exploitation based on real-time population diversity. At the same time, an elite pool retains the best-performing solution candidates to guide descendant evolution.
*   **Multi-dimensional evaluation**: To meet evaluation needs in different scenarios, the framework adopts a flexible multi-dimensional evaluation module. It not only provides traditional fitness scores and qualitative evaluation by LLM, but also offers domain-specific evaluation strategies for complex scenarios such as machine learning and kernel generation, such as jointly considering accuracy and latency, resource utilization, and more, ensuring that the evolution process is comprehensively guided by domain requirements.

<img src="/images/2510.26144v1/cluster.jpg" alt="Figure illustration" style="width:80%; max-width:300px; margin:auto; display:block;">

#### Distributed Infrastructure
The underlying layer of FM Agent is a scalable distributed infrastructure built for high-throughput evolutionary computation.
*   **Scalability**: Built on the Ray framework, the system can seamlessly scale from a single node to a large multi-node cluster, supporting concurrent execution of thousands of evolutionary processes.
*   **Asynchronous execution**: The two core tasks of program generation and program evaluation are executed asynchronously in separate, parallel worker pools. This separation ensures that compute-intensive tasks do not block one another, significantly improving system throughput and overall evolutionary efficiency.

#### Human-in-the-loop feedback module
This is an optional module designed to flexibly incorporate domain experts’ knowledge into the autonomous evolution process. It provides a visual interface that allows experts to monitor evolutionary metrics in real time, such as fitness changes and population diversity, and to guide the evolution direction through natural-language instructions or code-level interventions. In addition, this module supports building an expert knowledge base and uses RAG technology to automatically retrieve relevant knowledge when optimization hits a bottleneck, providing information for mutation and crossover operations and enhancing the rationality of the search.

## Experimental Results
This paper validates the effectiveness and generalization ability of FM Agent through experiments on authoritative benchmarks in three different domains: machine learning, combinatorial optimization, and GPU kernel generation. All experiments were completed autonomously by LLM, without human intervention.

### Machine Learning (MLE-Bench)
MLE-Bench is a complex real-world machine learning task benchmark based on Kaggle competitions.


| Metric | InternAgent | Auto-Agent | ML-Master | Human | **FM Agent (this paper)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Valid submission rate** | 98.67% | 93.33% | 85.33% | - | **98.67%** |
| **Above median human** | 48.44% | 40.00% | 44.90% | 50.00% | **65.33%** |
| **Any medal** | 20.31% | 22.86% | 23.44% | 22.00% | **29.33%** |
| **Gold medal** | 4.69% | 2.86% | 6.25% | 4.00% | **8.00%** |

*   **Robustness**: FM Agent achieved valid submissions on 98.67% of tasks, demonstrating extremely high reliability.
*   **Superior performance**: On 65.33% of tasks, its performance exceeded that of more than half of human submitters, significantly outperforming other agent.
*   **Top-tier performance**: FM Agent achieved the highest medal rate (29.33%) and gold medal rate (8.00%), especially excelling on **medium- and high-complexity tasks**, indicating its potential to surpass most human researchers in complex scenarios.

<img src="/images/2510.26144v1/mlebench_v2.jpg" alt="Figure illustration" style="width:85%; max-width:600px; margin:auto; display:block;">

### Combinatorial Optimization (ALE-Bench)
ALE-Bench is a goal-driven algorithm benchmark composed of computationally hard algorithmic competition problems.


| Method | Average Score | ≥400 | ≥1600 | ≥2000 (Yellow) |
| :--- | :--- | :--- | :--- | :--- |
| Self-Refine (baseline) | 1201.3 | 100.0% | 30.0% | 10.0% |
| ALE-Agent (SOTA) | 1879.3 | 100.0% | 70.0% | 30.0% |
| **FM Agent (this work)** | **1976.8** | **100.0%** | **80.0%** | **40.0%** |

*   **New SOTA**: FM Agent achieved an average score of 1976.8, setting a new SOTA record and outperforming the specially designed ALE-Agent by 5.2%.
*   **High-level reliability**: At the high-difficulty threshold (≥2000 points, expert “Yellow” level), FM Agent met the mark in 40% of tasks, significantly better than ALE-Agent’s 30%.
*   **Deep reasoning ability**: In **long contests** that require more complex and creative solutions, FM Agent performed especially well, indicating that its evolutionary approach is particularly effective on complex problems that demand deep reasoning and optimization.

<img src="/images/2510.26144v1/ale_tasks.jpg" alt="Figure illustration" style="width:85%; max-width:600px; margin:auto; display:block;">

### GPU Kernel Generation (KernelBench)
KernelBench is designed to evaluate an LLM’s ability to generate efficient GPU kernels. Experiments were conducted at the most difficult Level 3, with stricter numerical precision requirements.

<img src="/images/2510.26144v1/x1.jpg" alt="Figure illustration" style="width:85%; max-width:600px; margin:auto; display:block;">

Compared with previous SOTA methods (such as the agent-based AI CUDA Engineer and the reinforcement-learning-based CUDA-L1), FM Agent achieved **SOTA speedups ranging from 2x to 9x over the cuBLAS baseline** across multiple kernels while maintaining high numerical precision ($10^{-5}$), consistently outperforming the previous best results.

**Final conclusion**: The experimental results strongly demonstrate that FM Agent is a robust and general-purpose problem-solving framework. It can autonomously discover state-of-the-art solutions across multiple complex domains, including machine learning, combinatorial optimization, and systems optimization, validating the superiority of its architecture that combines LLM reasoning with large-scale evolutionary search.