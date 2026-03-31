---
layout: default
title: "Higher-order Linear Attention"
---


- **ArXiv URL**: http://arxiv.org/abs/2510.27258v1

- **Authors**: Zhen Qin; Quanquan Gu; Yifan Zhang

- **Published by**: Princeton University; University of California

---

## TL;DR
This paper proposes a new attention mechanism called Higher-order Linear Attention (HLA), which achieves higher-order interactions through compact prefix sufficient statistics while preserving linear-time complexity and streaming computation capability, thereby addressing the quadratic complexity bottleneck of standard attention mechanisms without sacrificing expressiveness.

## Key Definitions
*   **Higher-order Linear Attention (HLA)**: A generalized linear attention mechanism. It enhances model expressiveness by introducing higher-order interactions, such as second-order tensor products, while enabling streaming computation at each time step with linear time complexity and constant-size state by decomposing the computation into multiple lower-order moments (for example, the sum of outer products of key vectors).
*   **Prefix Summaries**: A set of statistics that can be updated in a streaming manner during sequence processing, with per-step update cost independent of sequence length. For second-order HLA, the core summaries include the second-order moment of keys $\mathbf{S}\_t^K$, the query-value accumulator $\mathbf{C}\_t^{QV}$, and the query mass $\mathbf{m}\_t^Q$.
*   **Associative Scans**: A parallel computation technique used to efficiently train HLA models. By defining an associative binary operation for HLA state updates, such as a monoid or semidirect product, scan computations can be performed in parallel over data blocks, producing exactly the same result as a serial loop and thereby addressing the inefficiency of recurrent neural network training.
*   **Asymmetric Higher-order Linear Attention (AHLA)**: A variant of HLA that computes the asymmetric cascaded product $\mathbf{AAV}$, where $\mathbf{A}=\mathbf{Q}\mathbf{K}^{\top}$, complementing the standard symmetric form $\mathbf{AA}^{\top}\mathbf{V}$. AHLA also supports strict causal streaming computation and has different computational costs and state composition.

## Related Work
The foundation of modern large language models (LLMs) is the Transformer architecture and its core component—scaled dot-product attention. However, its computational and memory complexity grows as $O(n^2)$ with sequence length $n$, which severely limits the use of these models in long-context settings.

To address this bottleneck, the field has seen a variety of efficient alternatives, including Linear Attention, modern recurrent neural networks (RNNs), and State Space Models (SSMs). These methods typically achieve linear-time complexity and $O(1)$ state updates at inference time. However, most of them are limited to first-order or kernel-based approximations, which may constrain model expressiveness.

The core problem this paper aims to solve is: how can we design a mechanism that has the data dependence and higher-order interaction capabilities of attention, while also achieving efficient streaming computation and parallel training like modern recurrent architectures?

## Method
The core contribution of this paper is Higher-order Linear Attention (HLA), which enables streaming computation of higher-order interactions through compact prefix summaries.

### Second-order HLA
As a starting point, the paper begins with second-order tensor attention:


{% raw %}$$
\mathbf{T}_{2} := (\mathbf{Q}\mathbf{K}^{\top})(\mathbf{Q}\mathbf{K}^{\top})^{\top} = \mathbf{Q}(\mathbf{K}^{\top}\mathbf{K})\mathbf{Q}^{\top} \in \mathbb{R}^{n \times n}
$${% endraw %}


The key is that it depends on the second-order moment of keys, $\mathbf{K}^{\top}\mathbf{K}$. This motivates streaming computation by maintaining prefix summaries. At time step $t$, the following summaries are maintained:
*   **Second-order moment of keys**: $\mathbf{S}\_{t}^{K} \coloneqq \sum\_{i\leq t}\mathbf{k}\_{i}\mathbf{k}\_{i}^{\top} \in \mathbb{R}^{d\times d}$
*   **Query-value accumulator**: $\mathbf{C}\_{t}^{QV} \coloneqq \sum\_{i\leq t}\mathbf{q}\_{i}\mathbf{v}\_{i}^{\top} \in \mathbb{R}^{d\times d\_v}$
*   **Query mass**: $\mathbf{m}\_{t}^{Q} \coloneqq \sum\_{i\leq t}\mathbf{q}\_{i} \in \mathbb{R}^{d}$

The update cost of these summaries is $O(d^2 + d d\_v)$, independent of sequence length.

Based on these summaries, the output of second-order HLA (by default in unnormalized form) at time step $t$ is defined as:


{% raw %}$$
\mathbf{o}_{t} \coloneqq \mathbf{q}_{t}^{\top}\mathbf{S}_{t}^{K}\mathbf{C}_{t}^{QV}
$${% endraw %}


Normalization is also possible:


{% raw %}$$
\mathbf{o}_{t} = \frac{\mathbf{q}_{t}^{\top}\mathbf{S}_{t}^{K}\mathbf{C}_{t}^{QV}}{\mathbf{q}_{t}^{\top}\mathbf{S}_{t}^{K}\mathbf{m}_{t}^{Q}+\varepsilon}
$${% endraw %}


Here, $\mathbf{S}\_t^K$ acts as a data-dependent, learnable metric matrix, enriching the model’s expressiveness. When $\mathbf{S}\_t^K = \mathbf{I}$, this form reduces to a linear attention mechanism.

### Innovation 1: Causal masking via extended summaries
Standard attention mechanisms require causal masking in computation to ensure that, in autoregressive tasks, the output at the current time step depends only on past information. Applying masking directly in HLA would break the factorized computation structure.

To solve this, the paper introduces two additional extended prefix summaries:


{% raw %}$$
\mathbf{G}_{t} \coloneqq \sum_{i\leq t}\left(\mathbf{k}_{i}\mathbf{k}_{i}^{\top}\right)\mathbf{C}_{i-1}^{QV} \in \mathbb{R}^{d\times d_v}
$${% endraw %}




{% raw %}$$
\mathbf{h}_{t} \coloneqq \sum_{i\leq t}\left(\mathbf{k}_{i}\mathbf{k}_{i}^{\top}\right)\mathbf{m}_{i-1}^{Q} \in \mathbb{R}^{d}
$${% endraw %}


With these correction terms, the strictly causal second-order HLA output can be computed exactly without materializing any $n \times n$ matrix. For example, the unnormalized causal output is:


{% raw %}$$
\mathbf{o}_{t} = \mathbf{q}_{t}^{\top}(\mathbf{S}_{t}^{K}\mathbf{C}_{t}^{QV} - \mathbf{G}_{t})
$${% endraw %}


All summaries, including $\mathbf{G}\_t$ and $\mathbf{h}\_t$, support constant-time online updates, preserving the efficiency of streaming computation.
*   **Update rules**:
    *   $\mathbf{G}\_{t} = \mathbf{G}\_{t-1}+\mathbf{k}\_{t}(\mathbf{k}\_{t}^{\top}\mathbf{C}\_{t-1}^{QV})$
    *   $\mathbf{h}\_{t} = \mathbf{h}\_{t-1}+\mathbf{k}\_{t}(\mathbf{k}\_{t}^{\top}\mathbf{m}\_{t-1}^{Q})$

### Innovation 2: Parallel training via associative scans
Purely recurrent models are inefficient to train on GPUs. To enable efficient parallel training, the paper defines an associative operator $$⊕$$ for HLA state updates and uses associative scans, such as Blelloch scan, to compute prefix sums.

*   **Unmasked case**: The merge of state $\mathcal{S}=(\mathbf{S},\mathbf{C},\mathbf{m})$ is simple addition, forming a monoid.
    

    {% raw %}$$
    (\mathbf{S}_{A},\mathbf{C}_{A},\mathbf{m}_{A}) \oplus (\mathbf{S}_{B},\mathbf{C}_{B},\mathbf{m}_{B}) = (\mathbf{S}_{A}{+}\mathbf{S}_{B},\,\mathbf{C}_{A}{+}\mathbf{C}_{B},\,\mathbf{m}_{A}{+}\mathbf{m}_{B})
    $${% endraw %}


*   **Masked case**: The merge of state $\mathcal{S}=(\mathbf{S},\mathbf{C},\mathbf{m},\mathbf{G},\mathbf{h})$ is more complex and forms a semidirect product structure, because cross-segment interaction terms must be taken into account.
    

    {% raw %}$$
    \begin{aligned}
    (\mathbf{S}_{A}, \mathbf{C}_{A}, \mathbf{m}_{A}, \mathbf{G}_{A}, \mathbf{h}_{A}) &\oplus (\mathbf{S}_{B}, \mathbf{C}_{B}, \mathbf{m}_{B}, \mathbf{G}_{B}, \mathbf{h}_{B}) = \\
    \big(\mathbf{S}_{A}{+}\mathbf{S}_{B},\; \mathbf{C}_{A}{+}\mathbf{C}_{B},\; &\mathbf{m}_{A}{+}\mathbf{m}_{B},\; \mathbf{G}_{A}{+}\mathbf{G}_{B}+\mathbf{S}_{B}\mathbf{C}_{A},\; \mathbf{h}_{A}{+}\mathbf{h}_{B}+\mathbf{S}_{B}\mathbf{m}_{A}\big)
    \end{aligned}
    $${% endraw %}


This method can partition the sequence into blocks and perform scans in parallel within and across blocks, producing activations exactly identical to those of a serial loop, thereby enabling efficient and exact parallel training. This framework can also be extended to the case with exponential decay $\gamma$.

![Masked (Second Order) HLA with Within-Chunk Scan](https://raw.githubusercontent.com/wylAImoreira/img-bed/main/202405231718919.png)

### Asymmetric Higher-Order Linear Attention (AHLA)
This paper also proposes a complementary variant called AHLA. It computes the left-cascaded product $\mathbf{Q}(\mathbf{K}^\top\mathbf{Q})(\mathbf{K}^\top\mathbf{V})$ instead of the symmetric form used in HLA. AHLA also supports streaming computation and causal masking, but uses different prefix summaries, for example:
*   $\mathbf{P}\_{t}^{KV} \coloneqq \sum\_{j\leq t}\mathbf{k}\_{j}\mathbf{v}\_{j}^{\top}$
*   $\mathbf{E}\_{t} \coloneqq \sum\_{i\leq t}\mathbf{k}\_{i}\big(\mathbf{q}\_{i}^{\top}\mathbf{P}\_{i}^{KV}\big)$

Its streaming output is $\mathbf{o}\_{t}^{\textsc{AHLA}} = \mathbf{q}\_{t}^{\top}\mathbf{E}\_{t}$. AHLA has a computational cost of $O(d d\_v)$, and in some cases is more efficient than HLA.

## Experimental Conclusions
This paper mainly focuses on the algorithmic structure and theoretical derivations, and does not provide specific experimental results or performance comparisons with other models.

**Summary**
This paper presents a complete, scalable attention framework—Higher-Order Linear Attention (HLA). Its main contributions and advantages are as follows:
*   **Strong expressiveness**: By introducing second-order and even higher-order interactions, HLA has stronger data-dependent mixing capability than standard linear attention.
*   **Computational efficiency**: HLA has linear time complexity at inference time (second order is $O(d^2 + d d\_v)$) and $O(1)$ state update cost, making it very suitable for long-context scenarios.
*   **Strict causality**: Through an innovative extended summary, HLA can precisely achieve the strict causal masking required for autoregressive tasks without sacrificing streaming efficiency.
*   **Parallel training**: With the associative scan technique, HLA training can be efficiently parallelized, and its results are exactly consistent with serial computation, avoiding the issues caused by approximate backpropagation.

In short, HLA, as a building block that can directly replace standard attention, cleverly combines the data-dependent weighting properties of attention with the high efficiency of modern recurrent architectures, providing a powerful and principled tool for building scalable long-context language models.