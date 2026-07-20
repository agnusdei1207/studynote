---
title: "Knowledge Distillation Model Pruning Compression"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 657
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 거대 Teacher 네트워크(예: ResNet-152, BERT-Large)의 사후확률 분포(soft label, temperature-scaled softmax)와 중간特征(feature map, attention map)을 Student 네트워크로 전이(KL-divergence + CE loss)하여, 가중치·필터·채널 단위의 구조적/비구조적 프루닝(magnitude/Taylor/Lottery Ticket)과 결합해 동일 정확도 대비 파라미터 수 10~100×, FLOPs 5~50×, 추론 지연(latency) 2~10×를 절감하는 경량화 통합 기법이다.
> 2. **가치**: 모바일·엣지 디바이스 환경(저전력 SoC, NPU, MCU)에서의 실시간 추론을 가능하게 하며, 통신비용·메모리 footprint·서버 추론 비용을 동시에 절감한다. BERT-Base를 DistilBERT로 증류 시 40% 적은 파라미터, 60% 빠른 추론, 97% 성능 유지가 대표적 정량 지표이다.
> 3. **판단 포인트**: Teacher-Student capacity gap이 클수록 증류 효율 저하(soft label 모호성), 프루닝 비율·sparsity 패턴·fine-tuning 회복 곡선 간의 trade-off, 그리고 hard label(GT) 손실과 soft label 손실의 가중치(α)·temperature(T)·feature transfer layer 설계가 성능을 결정하며, 이는 도메인·하드웨어 타깃(Edge GPU vs Mobile NPU vs MCU)에 따라 달라지는 실무자 핵심 판단 포인트이다.

---

## Ⅰ. 개요 및 필요성

딥러닝 모델은 2012년 AlexNet(60M params) 이후로 5년 주기로 10배씩 성장해왔으며, GPT-3(175B), PaLM(540B), LLaMA-2(70B) 같은 LLM, 그리고 Vision Transformer(ViT-L/16: 304M), SwinV2-G(3B) 등 비전 모델까지 수십~수천억 파라미터급으로 확장되었다. 그러나 실제 운영 환경(Production)에서는 (1) **클라우드 추론 비용** (e.g., GPT-3 추론 1회당 약 $0.0003~$0.02, GPU A100 시간당 약 $2~$4), (2) **모바일·엣지 디바이스의 제한된 자원** (메모리 4~12GB, NPU 5~15 TOPS, 배터리), (3) **실시간 응답 요구사항** (자율주행 10~30ms, 산업 비전 50ms, 음성인식 100ms) 때문에 그대로 배포가 불가능하다.

특히 한국·일본·유럽의 **AI 윤리·개인정보보호 규제**(EU AI Act, 국내 AI기본법, 개인정보보호법)의 강화로 **온디바이스(On-device) 추론**이 강제되는 추세이며, 의료·금융·제조·국방 도메인에서는 네트워크 단절 환경에서의 AI 가 필수이다. 또한 2024년 기준 글로벌 MLOps 시장에서 **모델 경량화(model compression) 시장은 연평균 34.8% 성장**(MarketsandMarkets 2024)하며, NVIDIA TensorRT, Qualcomm SNPE, Apple CoreML, Google TFLite, Intel OpenVINO 등 모든 추론 엔진이 INT8/FP16 양자화를 표준으로 채택하고 있다.

```text
+--------------------------------------------------------------------------+
|        거대 모델의 현실적 배포 한계 (왜 경량화가 필수인가?)              |
+--------------------------------------------------------------------------+
|                                                                          |
|   +--------------+         +------------------+         +-------------+  |
|   |  Teacher     | --유지--->|  배포 환경         |         |  한계 요소  |  |
|   |  (100B+ FLOPs)|         |  제약 조건        |         |             |  |
|   +--------------+         +------------------+         +-------------+  |
|        |                            |                            |      |
|        v                            v                            v      |
|   GPT-4 1.76T FLOPS          모바일: 6GB RAM, 15W         추론 비용     |
|   LLaMA-65B 1.4TB            MCU: 512KB SRAM, 100mW       latency      |
|   ViT-L 304M params          Edge TPU: 4MB 캐시           정확도 손실  |
|   v                          v                            v             |
|   +------------------------------------------------------------------+  |
|   |   경량화 3대 축 (Knowledge Distillation × Pruning × Quant)     |  |
|   |                                                                  |  |
|   |   ① Knowledge Distillation (지식 증류)                          |  |
|   |      Teacher -> Student로 soft label + feature 전이              |  |
|   |                                                                  |  |
|   |   ② Pruning (가지치기)                                           |  |
|   |      중요하지 않은 weight/channel/filter 제거                     |  |
|   |                                                                  |  |
|   |   ③ Quantization (양자화) <- 본 주제 보완 개념                    |  |
|   |      FP32 -> FP16/INT8/Binary 변환                                |  |
|   +------------------------------------------------------------------+  |
|                                                                          |
|   [배포 타깃별 목표]                                                    |
|   • 모바일 NPU   : 100MBv, INT8, 30msv                                 |
|   • 엣지 GPU     : 500MBv, FP16, 10msv                                 |
|   • MCU/임베디드  : 1MBv, INT4, 100msv (TinyML)                        |
|   • 브라우저 WASM : 50MBv, FP16, 200msv                                |
+--------------------------------------------------------------------------+
```

기존의 **단순 네트워크 압축**(weight quantization, low-rank factorization)은 정확도 손실이 3~10% 수준으로 컸으나, **Hinton(2015)의 Knowledge Distillation**이 제안된 이후로 정확도 손실을 0.5~2% 수준으로 줄이면서도 **90% 이상의 파라미터 감소**가 가능해졌다. 이후 **프루닝**(LeCun 1989 Optimal Brain Damage, Han 2015 Deep Compression, Frankle & Carlin 2019 Lottery Ticket Hypothesis)이 다시 조명받으면서, **증류 × 프루닝 × 양자화의 통합 파이프라인**이 현재의 표준 경량화 전략이 되었다.

- **📢 섹션 요약 비유**: 거대한 백과사전(Teacher) 전체를 학생(Student)에게 통째로 외우게 하는 대신, 선생님이 **"이 문제가 나오면 보통 A안이 60%, B안이 30%, C안이 10% 좋다"**라고 **soft hint(soft label)**를 주면서 공부시키면, 학생은 정답(A안)뿐 아니라 **오답들의 분포까지 학습**하여 비슷한 실력에 훨씬 적은 분량으로 도달하는 것과 같다. 프루닝은 백과사전에서 **절대 안 나오는 페이지들을 잘라내어**(가중치 sparsity) 부피를 줄이는 것이고, 양자화는 **글씨 크기를 줄여 인쇄**(FP32->INT8)하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) Knowledge Distillation (지식 증류) 상세 메커니즘

**Hinton et al. (2015, "Distilling the Knowledge in a Neural Network", NeurIPS Deep Learning Workshop)**의 핵심 아이디어는 분류 문제의 **hard label**(one-hot ground truth) 대신, **temperature-scaled softmax 분포**를 soft label로 활용하는 것이다.

$$q_i = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}$$

여기서 T(temperature)는 보통 3~20 사이의 값을 가지며, T가 클수록 **확률 분포가 평탄해져**(smoother) 클래스 간 관계 정보(dark knowledge)가 드러난다. Teacher와 Student의 distillation loss는 **KL-Divergence**로 정의된다:

$$L_{KD} = \alpha \cdot T^2 \cdot \text{KL}\big(\text{Softmax}(z^T/T) \,\|\, \text{Softmax}(z^S/T)\big) + (1-\alpha) \cdot \text{CE}(y_{true}, \text{Softmax}(z^S))$$

여기서 α는 두 손실의 가중치(보통 0.5~0.9)이고, $T^2$은 gradient magnitude 보정항이다. Hinton의 원 논문에서 **T=20, α=0.7**이 MNIST/음성 인식 실험에서 가장 좋은 결과를 보였다.

```text
+---------------------------------------------------------------------+
|     Knowledge Distillation 상세 아키텍처 (Feature + Logit 증류)    |
+---------------------------------------------------------------------+
|                                                                     |
|   +----------------------------------------------------------+    |
|   |  Teacher Network (frozen, pre-trained)                    |    |
|   |  +---------+  +---------+  +---------+  +---------+     |    |
|   |  | Conv1   |-->| Conv2   |-->| Conv3   |-->| Conv4   |     |    |
|   |  | F1^T    |  | F2^T    |  | F3^T    |  | F4^T    |     |    |
|   |  +---------+  +---------+  +---------+  +---------+     |    |
|   |       |             |             |             |         |    |
|   |       v             v             v             v         |    |
|   |     Hint1         Hint2         Hint3         Logit z^T   |    |
|   +------------------------+---------------------------------+    |
|                            |                                       |
|              +-------------+-------------+                         |
|              |  Hint Loss  |  Logit Loss | (FitNets + Hinton)      |
|              |  (MSE)      |  (KL-Div)   |                         |
|              +-------------+-------------+                         |
|                            v                                       |
|   +----------------------------------------------------------+    |
|   |  Student Network (trainable)                             |    |
|   |  +---------+  +---------+  +---------+  +---------+     |    |
|   |  | Conv1   |-->| Conv2   |-->| Conv3   |-->| Conv4   |     |    |
|   |  | F1^S    |  | F2^S    |  | F3^S    |  | F4^S    |     |    |
|   |  +---------+  +---------+  +---------+  +---------+     |    |
|   |       |             |             |             |         |    |
|   |       |             |             |             v         |    |
|   |       |             |             |         Logit z^S     |    |
|   |       |             |             |             |         |    |
|   |   Regression   Regression   Regression      Softmax      |    |
|   |   (hint layer  (hint layer  (hint layer    (T-scaled)   |    |
|   |    matching)    matching)    matching)                   |    |
|   |       |             |             |             |         |    |
|   |       +-------------+-------------+-------------+         |    |
|   |                            |                             |    |
|   |                            v                             |    |
|   |                   Total Loss = L_hint + L_KD + L_CE      |    |
|   +----------------------------------------------------------+    |
|                                                                     |
|   증류 Loss 분해:                                                    |
|   +------------------------------------------------------------+   |
|   | L_total = λ₁·L_hint(F^S, F^T) + λ₂·L_KD(z^S, z^T, T)   |   |
|   |          + (1-λ₁-λ₂)·L_CE(y_true, z^S)                  |   |
|   |                                                            |   |
|   | • L_hint: FitNets (Romero 2015), PKT, FSP, AT             |   |
|   | • L_KD: Hinton KD, DKD (Decoupled KD, CVPR 2022)         |   |
|   | • L_CE: hard label cross-entropy                          |   |
|   +------------------------------------------------------------+   |
+---------------------------------------------------------------------+
```

### 2) 증류 방법론 계열 (Feature/Attention/Relation-based)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Logit-based KD** (Hinton 2015) | 최종 출력층의 class probability 분포 전이 | Temperature-scaled softmax (T=3~20) + KL-Divergence. Soft label이 dark knowledge(비-target class 간 관계)를 포함. 단순·안정적이며 가장 널리 쓰임. |
| **FitNets / Hint-based** (Romero 2015) | 중간 hidden layer의 feature map 직접 매칭 | Teacher의 hint layer와 Student의 guided layer 사이에 **regressor conv layer** 추가, MSE loss로 정렬. 얕은 Student 학습에 유리, channel 수 차이를 regressor로 흡수. |
| **Attention Transfer (AT)** (Zagoruyko 2017) | Channel/ spatial attention map 전이 | $\mathcal{L}_{AT} = \left\| \frac{F^T}{\|F^T\|_2} - \frac{F^S}{\|F^S\|_2} \right\|_2^2$ 형태의 attention map 정규화 매칭. CNN 기반 모델에 효과적. |
| **FSP (Flow of Solution Procedure)** (Yim 2017) | Layer 간 Gram matrix (feature 관계) 전이 | 두 feature map의 내적 $F_i^T \cdot F_{j+1}^T$를 Student로 전달. Feature 자체보다 **layer 간 관계**를 학습시켜 일반화 우수. |
| **PKT (Probabilistic Knowledge Transfer)** (Passalis 2020) | Feature 분포를 확률적으로 매칭 | Feature map을 **Gaussian/MMD 거리**로 매칭. 매니폴드 정보 보존에 강함. |
| **DKD (Decoupled KD)** (Zhao 2022, CVPR Best Paper) | Logit KD를 target class / non-target class로 분리 | $L_{KD} = \alpha \cdot L_{TCKD} + \beta \cdot L_{NCKD}$. Non-target class 분포(bird knowledge) 학습이 핵심임을 증명. |
| **Self-Distillation** (Zhang 2019) | 동일 네트워크의 deep layer가 teacher 역할 | 같은 모델의 deep layer -> shallow layer로 증류. Noisy Student (Xie 2020)는 pseudo-label과 결합. |
| **Born-Again Networks (BAN)** (Furlanello 2018) | 동일 구조 student를 teacher로 반복 증류 | 동일 capacity student를 여러 세대 증류하면 teacher보다 성능 향상 가능. Ensemble distillation과 결합 시 SOTA. |

### 3) Pruning (가지치기) 상세 메커니즘

