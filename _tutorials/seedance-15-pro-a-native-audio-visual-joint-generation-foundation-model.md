---
layout: default
title: "Seedance 1.5 pro: A Native Audio-Visual Joint Generation Foundation Model"
---
## ByteDance Seedance 1.5 pro Released: Native Audio-Visual Joint Generation, Inference Speedup of Over 10x

<img src="/images/2512.13507v2/A__title.jpg" alt="" style="width:90%; max-width:700px; margin:auto; display:block;">

The “arms race” in video generation has never slowed over the past year. From Sora to Kling to Veo, the realism of the visuals has become astonishing. Yet one long-overlooked pain point has remained: **the disconnect between sound and image**. Most existing solutions still treat video generation and audio generation as two separate steps, leading to frequent issues such as “lip movements not matching speech” and “audio out of sync with the visuals.”

> ArXiv URL：http://arxiv.org/abs/2512.13507v2

Recently, **Seedance 1.5 pro** released by ByteDance (Volcano Engine) officially took on this challenge. As a foundation model for **Native Audio-Visual Joint Generation**, it is no longer a simple “video + dubbing” splice, but instead uses a dual-branch diffusion Transformer architecture to generate visuals and sound in sync. Even more strikingly, through extreme engineering optimization, its inference speed has improved by more than 10x, making professional-grade content creation far less out of reach.

### Native Joint Generation: A Victory of Architecture

The core breakthrough of Seedance 1.5 pro lies in its architectural design. Traditional video generation often first produces a silent video and then adds dubbing through an “image-to-sound” model; this cascaded approach naturally creates semantic and temporal misalignment.

This work proposes a unified multimodal joint generation architecture based on **MMDiT**. This design allows the model to perform deep cross-modal interaction during generation. In simple terms, while the model is “conceiving” each frame of the visuals, the same neural network is also “conceiving” the corresponding audio waveform.

This mechanism brings two significant advantages:

1.  **Precise temporal synchronization**: Whether it is lip movements during speech or the sound of objects colliding, frame-level alignment can be achieved.

2.  **Semantic consistency**: The visual stream and auditory stream share semantic understanding, ensuring that the generated audio matches the video closely in emotion and atmosphere.

### Data and Training: Meticulous Refinement from SFT to RLHF

To train such a massive model, Seedance 1.5 pro built a comprehensive audio-visual data framework. This includes not only a multi-stage data cleaning pipeline, but also an advanced Captioning System that can provide rich, professional-grade descriptions for both video and audio modalities.

In the post-training stage, the research adopted an extremely rigorous optimization strategy:

*   **Supervised Fine-Tuning** (**Supervised Fine-Tuning, SFT**): Fine-tuning with high-quality audio-visual datasets to establish the model’s foundational capabilities.

*   **Reinforcement Learning from Human Feedback** (**Reinforcement Learning from Human Feedback, RLHF**): A key technique behind the success of large language models, now successfully transferred to the audio-visual generation domain. The research team designed multi-dimensional reward models specifically to score and optimize motion quality, visual aesthetics, and audio fidelity.

images/page_1_Figure_7.jpg

The figure above shows an overview of the training and inference pipeline of Seedance 1.5 pro. Notably, low-level optimizations for the RLHF workflow improved training speed by nearly 3x.

### Inference Acceleration: A Leap of More Than 10x in Efficiency

For generative models, inference cost is often the biggest barrier to real-world deployment. Seedance 1.5 pro introduces an efficient acceleration framework.

By optimizing the Multi-stage Distillation framework, the model greatly reduced the **Number of Function Evaluations** (**Number of Function Evaluations, NFE**) required during generation. Combined with infrastructure-level optimizations such as Quantization and Parallelism, the model achieved end-to-end inference acceleration of more than **10x** without sacrificing generation quality. This means that the time users need to wait to generate a high-quality audio-visual piece will be dramatically shortened.

### Core Capabilities: Not Just “Can Move,” but “Understands the Scene”

In practical applications, Seedance 1.5 pro demonstrates strong professional potential, especially in the following areas:

1.  **Extremely precise dialect lip-sync**: This is one of the model’s standout strengths. It not only supports multiple languages, but can also accurately capture the unique rhythm and emotional intensity of different dialects (such as regional Chinese dialects) and achieve precise lip matching. This is a huge boon for localized short dramas and film production.

2.  **Cinematic camera control**: The model has autonomous shot orchestration capabilities and can execute complex camera movements such as long takes and Dolly Zoom, combined with professional-grade color grading, greatly enhancing the dynamic tension of the video.

3.  **Narrative coherence**: With enhanced semantic understanding, the model can better analyze narrative context, ensuring that generated audio-visual clips remain coherent and unified in plot and emotion.

### Evaluation Results: Benchmarking Against Sora 2 and Kling

To validate the model’s performance, the research team built the **SeedVideoBench 1.5** benchmark, introducing evaluation metrics that better align with film and television production standards.

images/page_4_Figure_10.jpg

In comparisons with top models such as Kling 2.5/2.6, Veo 3.1, and Sora 2, Seedance 1.5 pro performed excellently in audio-visual synchronization, motion expressiveness, and narrative consistency. In particular, for audio expressiveness, while Sora 2 is extremely powerful in emotional intensity, Seedance 1.5 pro showed a more balanced and controllable character, avoiding excessive exaggeration and making it better suited for professional production scenarios that require a stable tone.

### Conclusion

The release of Seedance 1.5 pro marks video generation technology’s accelerated transition from the era of “silent films” to the era of “talkies.” Through its native joint generation architecture and extreme engineering optimization, it not only solves the long-standing problem of audio-visual synchronization, but also raises inference efficiency to a new level.

At present, Seedance 1.5 pro has already launched on Volcano Engine and is planned to be integrated into platforms such as Doubao and Jimeng by December 2025. For creators, this may mean that a new era of end-to-end AI-assisted creation has arrived.