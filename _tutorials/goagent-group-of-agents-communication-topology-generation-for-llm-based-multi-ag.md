---
layout: default
title: "GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems"
---
## GoAgent: Teaching AI Agents to “Band Together,” 93.8% Accuracy, 17% Lower Token Cost

<img src="/images/2603.19677v1/A__title.jpg" alt="" style="width:90%; max-width:700px; margin:auto; display:block;">

Even the most capable single AI Agent can struggle with complex tasks. As a result, **Multi-Agent Systems** (**MAS**) have emerged, solving problems through the collaboration of multiple Agents. But this also introduces a core challenge: how should these Agents be organized for maximum efficiency?

> ArXiv URL：http://arxiv.org/abs/2603.19677v1

At present, most methods are like recruiting people one by one and then deciding, pair by pair, who should talk to whom. This “node-centric” approach often leads to chaotic collaboration workflows and high communication costs.

Now, a paper called GoAgent proposes a disruptive idea: stop connecting individual nodes one by one—just work in “groups” directly! The study uses predefined “collaboration groups” as the basic building blocks, not only significantly improving performance on complex tasks, but also reducing Token consumption by about 17%.

### From “Solo Combat” to “Team Collaboration”: GoAgent’s New Paradigm

When traditional methods build communication networks, they consider only one Agent at a time; this is known as the **node-centric** paradigm. The drawbacks are obvious: it cannot capture the collaboration structure required by the task from a macro perspective, easily leads to unnecessary communication, and can even result in missing key roles.

<img src="/images/2603.19677v1/x1.jpg" alt="Refer to caption" style="width:85%; max-width:450px; margin:auto; display:block;">

*Figure 1: (a) Node-centric paradigm vs. (b) GoAgent’s group-centric paradigm*

GoAgent pioneers a new **group-centric** paradigm. It no longer treats individual Agents as atomic units, but instead uses “collaboration groups” as the basic unit for building communication topologies.

A group may include a “problem decomposer,” a “code implementer,” and a “code reviewer,” already forming an efficient workflow internally. The model only needs to decide which groups are needed for the current task and how information should flow between them.

This approach has two major advantages:

1.  **Ensures internal cohesion**: The collaboration pattern within each group is predefined, ensuring efficient execution of subtasks.

2.  **Simplifies macro-level coordination**: The model only needs to focus on higher-level dependencies between groups, greatly reducing construction complexity.

<img src="/images/2603.19677v1/x2.jpg" alt="Refer to caption" style="width:85%; max-width:600px; margin:auto; display:block;">

*Figure 2: Overview of GoAgent’s overall architecture*

GoAgent’s entire workflow can be divided into several key steps: first, it encodes the task and discovers candidate collaboration groups; then, it selects and connects these groups step by step in an autoregressive manner; finally, it uses a clever mechanism to compress noise in communication.

### How Does GoAgent Build an “Elite Team”?

The process by which GoAgent generates a communication topology is like a smart project manager assembling a team.

#### 1. Collaboration Group Discovery

First, the researchers use large language models such as GPT-4 to pre-generate a series of candidate “expert groups” based on the needs of specific domains, such as code generation and mathematical reasoning.

Each group has a clear definition, including:

- **Name**: such as “code debugging team”

- **Expertise**: identifying and fixing logical errors in code

- **Roles**: Agents such as “code reviewer,” “syntax checker,” and “logic validator”

- **Internal topology**: defines how Agents within the group collaborate, such as a “sequential pipeline” or “fully connected discussion”

These candidate groups form a “talent pool” waiting to be called upon.

#### 2. Autoregressive Group Generation

Next, GoAgent’s core generation model gets to work. It incrementally builds the final communication graph:

At each step $t$, the model does two things:

- **Group prediction**: based on the current task requirements and the generated graph structure $\mathcal{G}\_{<t}$, it selects the next most suitable group $M\_t$ from the “talent pool.”

- **Connection prediction**: it determines from which existing groups $M\_i$ the newly added group $M\_t$ should receive information, thereby establishing cross-group communication links.

This process is **autoregressive**, meaning each decision depends on the previous state, until the model generates a special $$END$$ token indicating that graph construction is complete.

### Rejecting “Too Many Voices”: Compressing Communication with an Information Bottleneck

As the collaboration graph continues to grow, the historical dialogue between Agents becomes increasingly verbose, inevitably containing a large amount of “noise” unrelated to the current decision. If this noise is allowed to spread, it not only increases Token consumption but may also interfere with the judgment of subsequent Agents.

To address this problem, GoAgent introduces a key mechanism: the **Conditional Information Bottleneck** (**CIB**).

You can think of it as an intelligent filter. Before each group or connection prediction, the historical information first passes through the CIB layer. The goal of CIB is to:

- **Preserve**: information most relevant to the current task (Condition).

- **Compress**: redundant historical noise that is unrelated to the task.

Its optimization objective can be expressed as:




{% raw %}$$ \min\mathcal{L}_{\text{CIB}}=-I(\mathbf{c};y \mid \mathbf{z}_{\mathcal{Q}})+\beta I(\mathbf{x};\mathbf{c} \mid \mathbf{z}_{\mathcal{Q}}) $${% endraw %}


Here, $y$ is the prediction target (the next group or connection), $\mathbf{x}$ is the original historical information, $\mathbf{c}$ is the compressed essential information, and $\mathbf{z}\_{\mathcal{Q}}$ is the representation of the task itself.

The first term (Predictive Term) ensures that the compressed information is sufficient for accurate prediction, while the second term (Compression Term) is responsible for discarding irrelevant information as much as possible. In this way, GoAgent ensures that every decision is based on the most refined and relevant signals, thereby improving the efficiency and robustness of the entire system.

### Experimental Results: More Accurate, More Efficient

GoAgent performs exceptionally well on six mainstream benchmarks, including MMLU, GSM8K, and HumanEval, demonstrating its effectiveness.

**1. Leading Accuracy Across the Board**

As shown in the summary table below, GoAgent achieves SOTA performance on all tasks, with an average accuracy of 93.84%. Its advantage is even more pronounced on more complex tasks such as MMLU (commonsense reasoning) and HumanEval (code generation), where it improves by 1.96% and 2.47%, respectively, over the previous SOTA methods.

This confirms the study’s core hypothesis: building at the group level can form a more coherent and specialized collaboration flow, thereby better solving complex problems.

**2. Significantly Lower Token Consumption**

Efficiency is another key metric for evaluating the quality of a multi-agent system. As shown in the figure below, while achieving higher accuracy, GoAgent also successfully reduced Token consumption by about 17%.

<img src="/images/2603.19677v1/x3.jpg" alt="Refer to caption" style="width:85%; max-width:450px; margin:auto; display:block;">

*Figure 3: Token consumption comparison*

This is mainly due to two factors: first, the group-based structure avoids a large amount of redundant point-to-point communication; second, the CIB mechanism effectively filters historical noise, reducing the context length passed to the LLM.

Ablation experiments further confirm that both the “group-centric” design and the “CIB” mechanism are crucial to the final performance improvement, and neither can be omitted.

### Conclusion

The introduction of GoAgent opens up a new path for designing efficient and powerful multi-agent systems. It successfully elevates the construction paradigm from the chaotic “node-centric” approach to an orderly “group-centric” one, simulating real-world team collaboration and teaching AI Agents to work in “bands.”

More accurate and more economical, GoAgent proves that good top-level design is more important than simply stacking Agent capabilities. In the future, we may see more AI collaboration systems emerge based on this kind of “organizational architecture” thinking.