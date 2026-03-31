---
layout: default
title: "Group Representational Position Encoding"
---
## Group Representational Position Encoding (GRAPE): A Unified Theoretical Framework for RoPE and ALiBi

<img src="/images/2512.07805v1/A__title.jpg" alt="" style="width:90%; max-width:700px; margin:auto; display:block;">

The core of the Transformer architecture is the self-attention mechanism, but it cannot inherently perceive the order of tokens in a sequence, meaning it is **permutation-invariant**. To enable the model to understand that “word A comes before word B,” positional information must be introduced. This is the role of **Positional Encoding**.

> ArXiv URL：http://arxiv.org/abs/2512.07805v1

Positional encoding techniques have undergone several iterations. Early methods assigned each position a fixed or learnable **absolute positional encoding**. Later, researchers found that **relative positional encoding** was more effective, because it focuses on the relative distance between tokens rather than their absolute positions.

Among them, **Rotary Position Embedding (RoPE)** and **Attention with Linear Biases (ALiBi)** are two mainstream and highly effective approaches. RoPE encodes relative positions by rotating the Query and Key vectors, preserving vector norms. ALiBi, on the other hand, directly adds a penalty term proportional to relative distance to the attention scores, making it simple to implement and excellent at length extrapolation.

Although these methods have been very successful, they seem to stem from different design philosophies: one is a multiplicative geometric transformation, while the other is an additive bias. Is there a deeper connection between them? Can they be understood, or even improved, within a unified theoretical framework?

**Group Representational Position Encoding** (**Group Representational Position Encoding, GRAPE**) was proposed precisely to answer these questions. It uses the powerful mathematical tool of **Group Theory** to build a unified framework that encompasses seemingly unrelated methods such as RoPE and ALiBi as special cases.

The core idea of GRAPE is that positional information can be represented through a **Group Action**. Specifically, position $n$ corresponds to a group element $G(n)$, which is a matrix acting on word vectors. This group element is derived via the **Matrix Exponential** from a more fundamental **Generator** $L$: $G(n) = \exp(n\omega L)$.

![Figure illustration](images/page_1_Figure_0.jpg)

Figure: Overview of the GRAPE framework. On the left, multiplicative GRAPE unifies methods such as RoPE through rotation operations in the special orthogonal group SO(d). On the right, additive GRAPE unifies methods such as ALiBi and FoX through unipotent transformations in the general linear group GL.

This concise formula carries profound physical and mathematical meaning: it not only unifies existing methods, but also opens up a broad design space for creating new and more powerful positional encoding schemes.

### Core Idea: Group Theory and the Relativity of Position

Group theory is the branch of mathematics that studies symmetry. A **Group** consists of a set of elements and an operation that satisfies properties such as closure, associativity, the existence of an identity element, and inverses.

When applied to positional encoding, the most important feature of group theory is that it naturally expresses “relative” relationships. A **one-parameter subgroup** $G(t)$ has the property $G(t+s) = G(t)G(s)$. This property is perfect for positional encoding.

In attention computation, we want the interaction between the query vector at position $i$ and the key vector at position $j$ to depend only on their relative offset $j-i$. If we define the positional transformation as $G(n)$, then the transformations applied to the query and key can be written as:




{% raw %}$$ \widetilde{\mathbf{q}}_i = \mathbf{G}(i)\mathbf{q}_i, \qquad \widetilde{\mathbf{k}}_j = \mathbf{G}(j)\mathbf{k}_j $${% endraw %}



Their inner product, which is the core part of the attention score, becomes:




{% raw %}$$ \widetilde{\mathbf{q}}_i^{\top} \widetilde{\mathbf{k}}_j = (\mathbf{G}(i)\mathbf{q}_i)^{\top} (\mathbf{G}(j)\mathbf{k}_j) = \mathbf{q}_i^{\top} \mathbf{G}(i)^{\top} \mathbf{G}(j) \mathbf{k}_j $${% endraw %}



If $G(n)$ is an **Orthogonal Matrix**, satisfying $G(i)^\top = G(i)^{-1} = G(-i)$, then using the group property, the above expression can be simplified to:




{% raw %}$$ \mathbf{q}_i^{\top} \mathbf{G}(-i) \mathbf{G}(j) \mathbf{k}_j = \mathbf{q}_i^{\top} \mathbf{G}(j-i) \mathbf{k}_j $${% endraw %}



This result is elegant: the attention score depends only on the transformation matrix $G(j-i)$ for the relative position $j-i$, and is independent of the absolute positions $i$ and $j$. GRAPE is built on this principle and constructs two different types of group actions.

### Multiplicative GRAPE: The Art of Rotation

The first is **Multiplicative GRAPE** (**Multiplicative GRAPE, GRAPE-M**), which interprets positional encoding as a rotation operation. Here, the group is the **Special Orthogonal Group** (**Special Orthogonal Group, SO(d)**), whose elements are rotation matrices in $d$-dimensional space that preserve vector length and orientation.

#### Generators and the Rodrigues Formula

The generator $L$ of GRAPE-M is a **skew-symmetric matrix**, i.e., $L^\top = -L$. Such matrices belong to the Lie algebra $\mathfrak{so}(d)$. The simplest nontrivial generator is **rank-2**, defined by two vectors $a, b \in \mathbb{R}^d$:




{% raw %}$$ \mathbf{L}(\mathbf{a}, \mathbf{b}) = \mathbf{a} \mathbf{b}^{\top} - \mathbf{b} \mathbf{a}^{\top} $${% endraw %}



The rotation defined by this generator occurs within the two-dimensional plane spanned by vectors $a$ and $b$, and has no effect on vectors outside that plane.

Computing the matrix exponential $\exp(n\omega L)$ is usually complicated, but for this rank-2 generator there is an efficient **closed-form solution**, similar to **Rodrigues' formula**:




{% raw %}$$ \exp(\mathbf{L}) = \mathbf{I} + \frac{\sin s}{s} \mathbf{L} + \frac{1 - \cos s}{s^2} \mathbf{L}^2 $${% endraw %}



where $s$ is a scalar related to $a$ and $b$. This formula allows us to perform the rotation operation on a vector in linear time $O(d)$ without explicitly constructing a large rotation matrix, making it very efficient.

#### RoPE as a Special Case of Multiplicative GRAPE

One of the most striking results of multiplicative GRAPE is that it reveals the mathematical essence of RoPE. RoPE can be precisely viewed as a special case of multiplicative GRAPE.

In RoPE, the $d$-dimensional vector space is divided into $d/2$ independent two-dimensional coordinate planes. Positional encoding is applied independently as rotations in each of these planes. From the GRAPE perspective, this is equivalent to choosing a set of special, pairwise **orthogonal** and **commuting** rank-2 generators $\{L_i\}$. The total generator is the weighted sum of these generators:




{% raw %}$$ \mathbf{L}_{\text{RoPE}} = \sum_{i=1}^{d/2} \theta_i \mathbf{L}_i $${% endraw %}



Since each $L_i$ acts on a disjoint subspace, they commute with one another ($[L_i, L_j] = 0$), so the total rotation can be decomposed into a product of rotations in each subspace:




{% raw %}$$ \mathbf{G}(n) = \exp\left(n\mathbf{L}_{\text{RoPE}}\right) = \prod_{i=1}^{d/2} \exp(n\theta_i \mathbf{L}_i) $${% endraw %}



This is exactly the block-diagonal rotation-matrix form of RoPE. GRAPE not only explains RoPE, but also points to directions for extension: we can use **learned**, **non-orthogonal**, or even **non-commuting** generators to couple features across dimensions during the rotation process, potentially capturing more complex dependencies.

### Additive GRAPE: The Wisdom of Translation

The second is **Additive GRAPE** (**Additive GRAPE, GRAPE-A**), which explains the origin of additive biases such as ALiBi. This mechanism is more ingenious in spirit: it turns addition into multiplication by “lifting” the dimension.

#### Homogeneous Coordinates and Unipotent Transformations

To implement addition (translation) via matrix multiplication, GRAPE-A adopts the **homogeneous lift** commonly used in computer graphics. A $d$-dimensional vector $x$ is augmented into a $(d+1)$-dimensional vector $[x; 1]$.

At this point, the group of operations is no longer the rotation group $SO(d+1)$, but the more general **General Linear Group** (**General Linear Group, GL(d+1)**), whose elements are all invertible $(d+1) \times (d+1)$ matrices. Its generator $A$ is a special **nilpotent matrix** satisfying $A^2 = 0$. A typical generator has the following form:




{% raw %}$$ \mathbf{A} = \begin{bmatrix} \mathbf{0}_{d \times d} & \mathbf{u} \\ \mathbf{0}_{1 \times d} & 0 \end{bmatrix} $${% endraw %}



Since $A^2=0$, the Taylor expansion of its matrix exponential becomes exceptionally simple:




{% raw %}$$ \mathbf{G}_{\text{add}}(n) = \exp(n \omega \mathbf{A}) = \mathbf{I} + n \omega \mathbf{A} = \begin{bmatrix} \mathbf{I}_d & n \omega \mathbf{u} \\ \mathbf{0}^\top & 1 \end{bmatrix} $${% endraw %}



This is a **unipotent transformation**, and all of its eigenvalues are 1. When this transformation acts on query and key vectors in homogeneous coordinates, an additive term magically appears in the final attention score; it is linearly related to the relative position $j-i$ and can be gated by content (such as the key vector).

#### ALiBi and FoX as special cases of additive GRAPE

The most direct application of additive GRAPE is that it provides a rigorous theoretical foundation for ALiBi. ALiBi adds a content-independent bias term $\beta\_h(j-i)$ to the attention score.

By lifting vectors into a $d+2$-dimensional space and carefully designing the augmentation of queries and keys as well as the nilpotent generator $A\_h$, GRAPE-A can exactly derive the bias term of ALiBi:




{% raw %}$$ \widehat{\mathbf{q}}_i^{\top} \mathbf{G}_{\text{add},h}(j-i)^{-\top} \widehat{\mathbf{k}}_j = \mathbf{q}_i^{\top} \mathbf{k}_j \ - \ (j-i) \, \beta_h $${% endraw %}



This result shows that ALiBi is not a heuristic trick, but can be naturally derived from unipotent transformations in the general linear group. Likewise, the study proves that the forgetting bias in the **Forgetting Transformer** (**FoX**) can also be viewed as an instance of additive GRAPE.

### Path Integral Additive GRAPE

The GRAPE framework also introduces the concept of **Path Integral Additive GRAPE** (**GRAPE-AP**), further extending the flexibility of additive biases.

Traditional additive biases are usually only related to linear functions of the relative distance $j-i$. GRAPE-AP, however, allows the bias to be an accumulated sum of “costs” along the path from position $j$ to $t$:




{% raw %}$$ b_h(t,j) := \sum_{\ell=j+1}^t \psi_h(t,\ell) $${% endraw %}



Here, the cost at each step $\psi\_h(t,\ell)$ can be a dynamic value related to content. Mathematically, this mechanism corresponds to the product of a sequence of unipotent transformation matrices. Due to the special structure of these matrices, their product is ultimately equivalent to a simple additive bias, preserving computational efficiency. This provides a theoretical basis for designing more dynamic and content-aware distance penalty mechanisms.

### Experiments and Performance

To validate the effectiveness of the GRAPE framework, the researchers conducted a series of language modeling experiments based on the Llama architecture. The experiments were carried out on an educational web text dataset containing 50 billion tokens (FineWeb-Edu), with a model size of 355 million parameters and a context length of 4096.

The experiments compared the performance of GRAPE with baseline methods such as RoPE, ALiBi, and FoX.


| ![Figure: Training and validation loss curves of the medium-scale model (355M) on the FineWeb-Edu dataset](images/page_10_Figure_2.jpg) | ![Figure: Training and validation loss curves of the medium-scale model (355M) on the FineWeb-Edu dataset](images/page_10_Figure_4.jpg) |
| :---: | :---: |
| Figure: Training and validation loss curves of the medium-scale model (355M) on the FineWeb-Edu dataset |

From the training and validation loss curves, it can be seen that the GRAPE variants consistently maintained better performance than baseline methods such as RoPE and FoX throughout the entire training process.

More importantly, the experiments observed that models using RoPE exhibited a certain degree of instability during training, whereas the GRAPE models showed a continuously stable learning process. This practically confirms the theoretical stability advantage of the GRAPE framework.

### Conclusion

By introducing group theory, GRAPE provides a profound and unified perspective on the problem of positional encoding in Transformers. It elegantly unifies two mainstream positional encoding paradigms—the rotation-based multiplicative mechanism (such as RoPE) and the translation-based additive mechanism (such as ALiBi and FoX)—within the same mathematical framework.

- **Unification**: GRAPE proves that RoPE is a special case under the action of the special orthogonal group $SO(d)$, while ALiBi and FoX are special cases of unipotent transformations in the general linear group $GL(d)$.

- **Interpretability**: It provides a solid mathematical foundation for these seemingly empirical methods, explaining why they work.

- **Extensibility**: GRAPE is not limited to explaining existing methods; it also offers a principled design space. By exploring different groups, generators, and representations, one can systematically design new and potentially more powerful positional encoding schemes, such as using learnable, non-commutative rotations to capture more complex feature interactions.

In short, GRAPE is not only a theoretical synthesis, but also a blueprint guiding future research on positional encoding. It combines abstract mathematical theory with concrete model design, paving the way for building larger language models that are more stable, more powerful, and better at extrapolation.