---
title: "Multimodal AI Vision Language Model"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 649
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티모달 비전-언어 모델(VLM)은 **Vision Encoder(ViT/SigLIP/DINOv2) + Modality Projection(MLP/Q-Former/Cross-Attention) + LLM Backbone(LLaMA/Qwen/InternLM)**의 3단 구조로, 이미지를 시각 토큰(Visual Tokens)으로 변환하여 텍스트 토큰과 동일 컨텍스트에서 자기회귀 생성(autoregressive generation)을 수행하는 아키텍처이다.
> 2. **가치**: 단일 모델로 **VQA, Image Captioning, OCR, Document Understanding, Visual Reasoning, Video Understanding**을 통합 처리하여 기존 CNN+OCR+NLP 파이프라인 대비 **추론 지연 3~10배 절감, 시스템 복잡도 70% 감소, 신규 태스크에 대한 제로샷 일반화**가 가능하며, GPT-4V 기준 도큐먼트 VQA에서 GPT-4 텍스트+OCR 파이프라인 대비 정확도 15~25%p 우위를 보인다.
> 3. **판단 포인트**: **①Vision Encoder 선정**(CLIP vs SigLIP vs DINOv2), **②해상도·토큰 전략**(Naive 336px vs AnyRes vs Dynamic), **③Projection 방식**(경량 Linear/MLP vs Q-Former), **④LLM 크기**(1B~72B) 간의 **정확도-지연시간-메모리** 트레이드오프, **⑤Instruction Tuning 데이터 품질과 양**이 성능을 결정한다.

---

## Ⅰ. 개요 및 필요성

기존 LLM은 텍스트 모달리티에 한정되어 산업 현장의 **비정형 데이터(영수증, 도면, 차트, CCTV 영상, 의료 영상 등)**를 직접 이해하지 못한다. 이를 우회하기 위해 전통적 방식은 **①OCR(예: Tesseract, PaddleOCR) -> ②텍스트 정규화 -> ③LLM 추론**의 다단계 파이프라인을 구성했으나, 다음의 구조적 한계가 존재했다.

1. **정보 손실**: 표·차트·도식 등 시각 구조(visual layout)와 공간 관계(spatial relationship)가 텍스트 직렬화 과정에서 손실된다.
2. **오류 전파(error propagation)**: OCR 단계의 1% 인식 오류가 후속 추론 단계를 붕괴시키며, 손글씨·저해상도·다국어에서 치명적이다.
3. **모달리티 갭(modality gap)**: "이 차트에서 2023년 4분기의 YoY 증가율은?"과 같은 질문은 텍스트만으로는 본질적으로 답할 수 없다.
4. **도메인 일반화 부재**: 파이프라인의 각 모듈이 독립 학습되어 도메인(의료·법률·제조) 전환 시 재학습 비용이 선형적으로 증가한다.

멀티모달 VLM은 **이미지·비디오를 1차원 토큰 시퀀스로 임베딩**하여 LLM의 자기회귀 생성 프레임워크에 통합함으로써, **end-to-end 학습**으로 위 한계를 동시 해결한다. **2021년 OpenAI CLIP**의 contrastive learning이 비전-언어 정렬(alignment)의 토대를 마련했고, **2022년 BLIP-2(Q-Former), Flamingo(Perceiver Resampler)**가 LLM과의 결합을, **2023년 LLaVA(Linear Projection), GPT-4V(Native Multimodal)**가 실용화 전환점을 만들었다.

```text
+-------------------- 전통 파이프라인 (Pre-VLM Era) --------------------+
|                                                                         |
|  [Image] ---> [OCR Engine] ---> [Text Norm] ---> [LayoutLM/BERT] ---> [LLM]|
|              (Tesseract)       (Regex)         (Doc NLP)       (GPT)   |
|                                                                         |
|  ✗ 단계별 오류 누적    ✗ 시각구조 손실    ✗ 4개 모델 관리 비용           |
+-------------------------------------------------------------------------+

                              v  패러다임 전환 (2021~)

+------------------ End-to-End 멀티모달 VLM -------------------+
|                                                                 |
|  [Image]--+                                                     |
|           +--> [Single VLM] ---> [Direct Answer]                 |
|  [Text] --+    (Image+Text Joint Reasoning)                    |
|                                                                 |
|  ✓ 단계 통합    ✓ 시각구조 보존    ✓ 단일 모델 운영              |
+-----------------------------------------------------------------+
```

추가로, **Anthropic, OpenAI, Google**의 **Agentic Workflow**가 확산되면서 VLM은 **GUI 자동화(Computer Use), 스크린샷 기반 디버깅, 차트 기반 의사결정**의 핵심 인터페이스로 자리매김했으며, **2024년 GPT-4o(omni), Gemini 1.5 Pro(1M 컨텍스트)**는 오디오·비디오까지 통합한 **네이티브 멀티모달(Native Multimodal)** 시대를 열었다.

- **📢 섹션 요약 비유**: 기존 파이프라인이 **"외국인에게 번역가->통역사->교수"를 거쳐 대화**하는 것이라면, VLM은 **"이중 언어 사용자와 직접 대화"**하는 것과 같다. 중간 단계의 왜곡 없이 한 번에 이해한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

VLM의 표준 아키텍처는 **3-Stage Encoder-Projection-LLM** 구조이며, 각 단계가 성능과 비용의 트레이드오프를 결정한다.

```text
                        [VLM 표준 아키텍처]
-------------------------------------------------------------------

[1] Vision Encoder
   Image (H×W×3) -> Split into Patches (P×P) -> Linear Patch Embed
   -> [CLS] + N patch tokens -> Transformer (L_v layers)
   -> Output: {v_1, v_2, ..., v_N} ∈ R^{N×d_v}
   +----------------------------------------------+
   | 예: ViT-L/14 (OpenAI CLIP) -> 256 tokens, 1024d|
   |     SigLIP-L/16 -> 256 tokens, 1024d           |
   |     DINOv2-G/14 -> 256 tokens, 1536d           |
   |     InternViT-6B -> 1024~4096 tokens (dynamic) |
   +----------------------------------------------+
                              |
                              v  시각 토큰 (Visual Tokens)
                              | N ≈ 256 ~ 4096개
                              | d_v (예: 1024)
                              v
[2] Modality Projection / Bridge
   +--------------------------------------------+
   | Option A: Linear/MLP Projection (LLaVA)    | <- 가장 가벼움
   |   2-layer MLP: R^{d_v} -> R^{d_l}          |
   |   파라미터 ~10M, 학습 <1시간               |
   |                                            |
   | Option B: Q-Former (BLIP-2)                | <- 중간 복잡도
   |   188M learnable queries ↔ Vision         |
   |   Cross-Attention으로 K=32~256 visual      |
   |   tokens로 압축                            |
   |                                            |
   | Option C: Perceiver Resampler (Flamingo)   | <- 다중 이미지용
   |   Latent queries로 arbitrary N -> 고정 K    |
   |   Interleaved image+text few-shot에 강점   |
   |                                            |
   | Option D: Cross-Attention Layers (Flamingo)| <- LLM 동결
   |   LLM 본체는 frozen, gating된 cross-attn   |
   |   layer만 학습 (~6.7B)                     |
   +--------------------------------------------+
                              |
                              v  LLM 차원 정렬된 시각 토큰
                              | K개 (보통 64~576)
                              | d_l (예: 4096 for LLaMA-3)
                              v
[3] Multimodal LLM Backbone
   Input Embedding = [Visual Tok × K] ⊕ [Text Tok × T]
   -> LLM Transformer (L layers, e.g., 32~80)
   -> Autoregressive Decoding -> Output Text
   +--------------------------------------------+
   | Base Models: LLaMA-2/3, Qwen-2, Mistral,  |
   |   Phi-3, InternLM-2.5, Gemma-2             |
   | Sizes: 1B / 3B / 7B / 13B / 34B / 72B      |
   +--------------------------------------------+

-------------------------------------------------------------------
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Vision Encoder** | 이미지를 시각 토큰 시퀀스로 변환 | • **CLIP ViT**: 400M image-text pair contrastive 사전학습, 텍스트 의미 정렬 우수<br>• **SigLIP**: Sigmoid loss로 batch size 비의존, 효율적 학습, zero-shot ImageNet 84.5%<br>• **DINOv2**: Self-distillation, dense prediction(segmentation·depth)에 강점<br>• **InternViT**: 6B 파라미터, dynamic resolution·multi-crop 지원 |
| **Modality Projection** | 시각 토큰을 LLM 입력 공간에 정렬 | • **Linear/MLP(LLaVA)**: 1~2-layer MLP, 빠른 학습·배포, 성능 충분<br>• **Q-Former(BLIP-2)**: 32~256 learnable queries와 cross-attn, 압축률 높음<br>• **Perceiver Resampler(Flamingo)**: N개 visual token -> 고정 K(latent array)<br>• **Native Fusion(GPT-4o)**: 별도 projection 없이 통합 토크나이저 |
| **LLM Backbone** | 통합 토큰 시퀀스의 자기회귀 추론 | • **LLaMA-3.1-8B/70B**, **Qwen2-7B/72B**, **InternLM2.5-20B**<br>• **RoPE** 위치 인코딩, **GQA(Grouped Query Attention)**, **Flash Attention 2**<br>• **Token 한계**: 시각 토큰 K가 길수록 컨텍스트 윈도우 점유(예: 1K vis token = 4K text) |
| **Output Decoder** | 다음 토큰 확률 분포 -> 텍스트