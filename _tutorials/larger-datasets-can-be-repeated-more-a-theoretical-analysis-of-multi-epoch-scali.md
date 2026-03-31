---
layout: default
title: "Larger Datasets Can Be Repeated More: A Theoretical Analysis of Multi-Epoch Scaling in Linear Regression"
---
## Data Shortage? Peking University and Tsinghua Find: The Larger the Dataset, the Greater the Benefit of Repeated Training, with Value Reaching logN Times

<img src="/images/2511.13421v1/A__title.jpg" alt="" style="width:85%; max-width:450px; margin:auto; display:block;">

The rapid development of AI is consuming the world’s high-quality data at an unprecedented pace, and some forecasts even suggest that we will run out of publicly available data by 2028. Faced with an increasingly severe data shortage, one seemingly straightforward solution is in front of all researchers: multi-epoch repeated training on a limited dataset.

> **Paper Title**: Larger Datasets Can Be Repeated More: A Theoretical Analysis of Multi-Epoch Scaling in Linear Regression

> **ArXiv URL**：http://arxiv.org/abs/2511.13421v1

But this raises a core question: to what extent can repeatedly “doing the same problems” replace “new problems”? Is training for 4 epochs on a 1TB dataset the same as training for 1 epoch on a brand-new 4TB dataset?

A recent study from Peking University, Peng Cheng Laboratory, and Tsinghua University provides a theoretically disruptive answer: **the effect of repeated training is closely tied to the size $N$ of the dataset you have.**

### The “Effectiveness” of Data Reuse

To quantify the value of data reuse, the researchers introduced a key metric: **Effective Reuse Rate** ($E(K, N)$).

Its definition is very intuitive: if you train for $K$ epochs on a dataset of size $N$, then to achieve the same model performance with only 1 epoch, how much new data would you need? The ratio of that new dataset size to the original size $N$ is $E(K, N)$.

If $E(4, N) \approx 4$, it means that training for 4 epochs on $N$ data points is almost equivalent to training for 1 epoch on $4N$ new data points, making data reuse highly efficient.

Previously, a widely discussed empirical study (Muennighoff et al., 2023) found that for large language models, when $K \le 4$, $E(K, N)$ is approximately equal to $K$, but as $K$ increases, the gains quickly saturate. However, their model ignored a key variable—the initial dataset size $N$.

### A New Theoretical Insight: Starting from Linear Regression

To precisely analyze the mechanism behind data reuse, this paper chose a “golden testbed” for theoretical analysis—**Linear Regression**. By rigorously deriving the training dynamics of stochastic gradient descent (SGD), the researchers obtained an exact characterization of $E(K, N)$.

The core findings show two distinctly different behaviors in two stages:

1.  **When the number of training epochs $K$ is small** (strictly speaking, $K=o(\log N)$):

The paper proves that $E(K, N) \approx K$.

This means that in the early stage of training, each repeated epoch is almost like using entirely new data, with linear and nearly lossless gains. This is consistent with previous empirical observations.

2.  **When the number of training epochs $K$ is large** ($K=\omega(\log N)$):

The growth of $E(K, N)$ slows down and approaches a plateau. But the key point is that this plateau is not a fixed constant; it is positively correlated with the dataset size $N$, specifically $\Theta(\log N)$.


<center>Figure 1: The trend of the effective reuse rate $E(K,N)$ as the number of training epochs $K$ changes. It grows linearly when $K$ is small, then enters a plateau, and the plateau height increases as the dataset size $N$ grows.</center>

### Core Conclusion: The Larger the Dataset, the More You Can “Live Off the Past”

This theoretical result brings an extremely important practical implication: **the larger the dataset, the more slowly the marginal benefit of repeated training declines, and the higher the upper bound of data reuse.**

In other words, a researcher with a 10TB dataset may still find significant gains from training for 8 or 10 epochs; whereas for a team with only a 1TB dataset, the effect may drop off sharply after 4 epochs.

This means that the old rough rule of thumb—“repeated training beyond 4 epochs is useless”—may need to be revised. The correct approach is to dynamically determine the optimal number of training epochs based on the dataset size $N$ you have. For organizations with massive amounts of data, they can more calmly “squeeze out” the value of the data by increasing the number of training epochs, achieving an equivalent data scale far beyond linear growth.

### From Theory to Empirical Results on LLMs

Although the above theoretical derivation is based on a simplified linear model, does its insight also apply to complex large language models?

To verify this, the research team conducted LLM pretraining experiments. The results were encouraging: **the actual performance of LLMs closely matches the theoretical predictions.**

The experiments confirmed that in LLM pretraining, for a fixed number of training epochs $K$, the effective reuse rate $E(K, N)$ does indeed increase monotonically as the dataset size $N$ grows. This provides strong empirical support for the core conclusion that “the larger the dataset, the more effectively it can be reused.”

### Summary and Takeaways

On the road toward stronger general artificial intelligence, the data bottleneck has become an unavoidable challenge. This study offers a new theoretical perspective for understanding and addressing that challenge.

It precisely reveals the scaling law of multi-epoch training and points out a key factor that has long been overlooked: the dataset size $N$.

For all AI practitioners and researchers, this work sends a clear signal: when planning compute resources and training strategies, we can no longer simply set a fixed upper limit on repeated training. Instead, we should recognize that **the more data we have, the more confidently we can reuse it, thereby leveraging model performance that exceeds the scale of the data itself in an era of limited data.**

Paper link: https://arxiv.org/abs/2405.18385