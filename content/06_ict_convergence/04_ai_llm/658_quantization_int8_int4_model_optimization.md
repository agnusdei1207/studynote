---
title: "Quantization INT8 INT4 Model Optimization"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 658
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM/딥러닝 모델의 가중치(Weight)와 활성화값(Activation)을 FP32/FP16에서 **INT8(8비트 정수)** 또는 **INT4(4비트 정수)**로 매핑하여 메모리 점유와 연산 비용을 줄이는 **수치 정밀도 축소(Numeric Precision Reduction)** 기법으로, Affine 변환(`q = round(r/S) + Z`)과 Calibration을 통해 양자화 오차(Quantization Error)를 제어한다.
> 2. **가치**: INT8 양자화 시 **모델 크기 75% 절감**(FP32->INT8), **메모리 대역폭 4배 감소**, **추론 지연 시간 2~4배 단축**을 달성하며, INT4(GPTQ/AWQ/NF4) 적용 시 추가로 87.5% 크기 절감(FP32->INT4)으로 **70B 파라미터 모델을 단일 24GB GPU(예: RTX 4090)에서도 추론 가능**하게 만든다.
> 3. **판단 포인트**: PTQ(Post-Training Quantization) vs QAT(Quantization-Aware Training), Symmetric vs Asymmetric, Per-tensor vs Per-channel/Per-group, **Outlier 채널 존재 시 SmoothQuant/AWQ의 channel-wise scaling 적용 여부**, 그리고 4-bit의 경우 GPTQ(Optimal Brain Quantization Hessian 기반) vs AWQ(Activation-aware Weight Quantization) vs NF4(NormalFloat) 중 데이터 특성과 허용 정확도 손실(typically 0.5~2%)에 따른 알고리즘 선택이 핵심 결정 포인트다.

---

## Ⅰ. 개요 및 필요성

GPT/LLaMA 계열 대규모 언어 모델(LLM)이 7B -> 70B -> 405B로 파라미터 수가 폭증하면서, FP16 기준으로 70B 모델은 **140GB VRAM**, FP32는 **280GB**가 필요해 H100 80GB GPU 2~4장이 필수적이다. 동시에 **메모리 대역폭 병목(Memory-Bound Problem)**이 두드러지는데, 디코딩 단계에서 생성 토큰당 모든 가중치를 VRAM->레지스터로 로드해야 하므로 GPU의 HBM 대역폭(예: H100 3.35TB/s)이 추론 속도의 결정적 병목점이 된다. 양자화는 이 두 가지 문제—**① 모델 크기로 인한 VRAM 부족, ② 메모리 대역폭 한계**—를 동시에 해결하는 가장 효과적인 추론 최적화(LLM Inference Optimization) 기법이다.

기존의 **가지치기(Pruning)**는 정확도 손실을 예측하기 어렵고, **지식 증류(Knowledge Distillation)**는 별도의 teacher 모델 훈련이 필요하며, **LoRA/QLoRA**는 fine-tuning에 특화되어 있다. 반면 양자화는 **사후 적용 가능(PTQ)**, **하드웨어 가속(INT8 Tensor Core, TensorRT-LLM)**, **프레임워크 생태계(TensorRT, ONNX, llama.cpp, vLLM, TGI) 성숙도** 측면에서 가장 실용적인 1차 최적화 수단으로 자리잡았다.

```text
[ FP32 LLM 추론의 메모리 병목 구조 ]

   +-----------------------------+
   |   Pre-trained FP16/FP32 Model |  <- 70B -> 140GB (FP16)
   +----------+------------------+
              |  Load all weights per token
              v
   +-----------------------------+
   |       HBM (VRAM)            |  <- H100 80GB / A100 80GB
   |   [Weight Memory: 140GB]    |     대역폭: 3.35TB/s
   +----------+------------------+
              |  Bandwidth-bound
              v
   +-----------------------------+
   |  GPU SM (Compute Units)     |  <- TFLOPS는 남지만 활용도 v
   |  [Decoding Latency: 30ms/t] |     (Memory Wall 문제)
   +----------+------------------+
              |
              v
         Token Output

   ⚠ 문제 1: VRAM 부족 -> 양자화로 weight 메모리 1/4~1/8 축소
   ⚠ 문제 2: 대역폭 병목 -> INT8/INT4 = bandwidth 요구량 1/4~1/8
```

**기존 패러다임 vs 양자화 패러다임 비교**

| 구분 | 기존(Full Precision) | 양자화(INT8/INT4) |
|:---|:---|:---|
| **메모리** | FP16: 14GB (7B) / 140GB (70B) | INT8: 7GB (7B) / 70GB (70B), INT4: 3.5GB (7B) / 35GB (70B) |
| **하드웨어** | H100/A100 다중 GPU 필수 | 단일 RTX 4090(24GB)에서도 70B INT4 추론 가능 |
| **추론 지연** | FP16 baseline | INT8: ~2~3배 v, INT4 (with fused kernel): ~3~5배 v |
| **개발 비용** | GPU 메모리 구매/임대 비용 | 알고리즘(GPTQ/AWQ) + Calibration 데이터 10~1000개 샘플 |
| **정확도** | Baseline (100%) | INT8: 0.1~0.5% 손실, INT4: 0.5~2.0% 손실 |

- **📢 섹션 요약 비유**: 양자화는 **고해상도 사진(FP32)을 그대로 들고 다니는 것**을 **압축된 JPG(INT8/INT4)**로 바꿔서 주머니에 가볍게 넣고 다니는 것과 같다. 화질은 조금 떨어져도(정확도 손실) 어디든 가지고 다닐 수 있고(단일 GPU), 빠르게 꺼내 볼 수 있다(대역폭 절약).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 양자화의 수학적 정의

**Affine(비대칭) 양자화**의 핵심 수식은 다음과 같다:

```
Quantization:  q = clamp(round(r / S) + Z, q_min, q_max)
Dequantization: r ≈ S × (q - Z)

여기서,
  r : 실수값 (FP32 real value)
  q : 양자화된 정수값
  S : Scale factor (Δ, 스케일)  = (r_max - r_min) / (q_max - q_min)
  Z : Zero-point (영점 오프셋)   = round(q_min - r_min / S)
  q_min, q_max : INT8 -> -128, 127 / INT4 -> -8, 7
```

**Symmetric(대칭) 양자화**는 Z=0으로 고정하여 zero-point 연산을 제거한 형태로, 하드웨어 구현이 단순해진다. LLM에서는 **per-channel symmetric quantization**이 일반적이며, LLaMA/TensorRT-LLM은 **W8A8(weight 8bit, activation 8bit)** 또는 **W4A16(weight 4bit, activation 16bit)** 구조를 채택한다.

### 2) Calibration과 양자화 스케일 결정 방식

실제 활성화값의 분포는 **Calibration Dataset**(통상 10~512개 샘플)을 GPU에 forward pass하여 관측하고, 그 통계량으로 scale factor를 결정한다:

- **Min-Max Calibration**: 가장 단순, outlier에 취약(outlier 1개가 전체 범위를 왜곡)
- **Percentile Calibration**: 99.9% percentile로 clip -> outlier robust
- **Entropy(KL-divergence) Calibration**: TensorRT 기본, FP32와 INT8 출력의 KL divergence 최소화
- **MSE Calibration**: 양자화 오차의 평균제곱오차 최소화

### 3) INT4 고급 알고리즘 3대 핵심

```text
[ LLM INT4 양자화 알고리즘 동작 흐름 비교 ]

   +----------------------------------------------------------+
   |                  ① GPTQ (OBD 기반)                       |
   |  • Hessian matrix H = 2·X·X^T 계산                      |
   |  • Optimal Brain Quantization 공식:                      |
   |      w_q = argmin ||w - w_q||²_H                        |
   |      δ = - (w_q_err) / (H⁻¹_ii) · H⁻¹_i                |
   |  • Layer-wise & column-wise 순차 처리                    |
   |  • 약 80~180GB VRAM + 1~3시간 (70B 기준, group_size=128)|
   +----------------------------------------------------------+

   +----------------------------------------------------------+
   |                  ② AWQ (Activation-aware)                |
   |  • 핵심 통찰: "1% salient weight가 99% activation을 결정"|
   |  • Activation magnitude로 채널별 중요도 s 계산           |
   |  • Channel-wise scaling: w' = w · s, x' = x / s          |
   |  • s = |mean(x)| ^ α  (α≈0.5)                           |
   |  • Salient 채널(상위 0.1~1%)만 FP16 유지 (mixed prec)   |
   |  • Reference: MIT-Han Lab 2023                          |
   +----------------------------------------------------------+

   +----------------------------------------------------------+
   |              ③ NF4 / FP4 (NormalFloat)                    |
   |  • QLoRA(Dettmers 2023)에서 제안                         |
   |  • 사전 학습된 normal distribution quantile로 16개 level  |
   |  • Non-uniform: 입력 분포에 최적화된 비대칭 레벨         |
   |  • Double Quant: 양자화된 scale factor를 다시 양자화     |
   |  • 4-bit 시점에서 가장 적은 정확도 손실(특히 fine-tuning)|
   +----------------------------------------------------------+
```

### 4) Layer-wise 파이프라인 (실제 적용 흐름)

```text
[ PTQ(Post-Training Quantization) End-to-End Pipeline ]

   +-----------------+
   | ① Pre-trained   |  FP16/FP32 model
   |    Model        |  (e.g., LLaMA-3-70B)
   +--------+--------+
            |
            v
   +-----------------+
   | ② Calibration   |  • C=128~512 samples
   |    Data 준비    |  • WikiText-2, C4, Pile 일부
   +--------+--------+
            |  Forward pass (no grad)
            v
   +-------------------------------------+
   | ③ Activation Statistics 수집       |
   |  • per-tensor min/max, histogram    |
   |  • per-channel scale factor 계산    |
   |  • Outlier 채널 식별 (ratio > 6σ)   |
   +--------+----------------------------+
            |
            v
   +-------------------------------------+
   | ④ Weight Quantization              |
   |  • INT8: per-channel symmetric      |
   |  • INT4: GPTQ group_size=32/64/128  |
   |          or AWQ with scaling        |
   |  • Outlier 보호: FP16 fallback      |
   +--------+----------------------------+
            |
            v
   +-----------------+
   | ⑤ Quantized     |  • TensorRT engine
   |    Model Export  |  • ONNX + quantized operators
   +--------+--------+  • GGUF (llama.cpp)
            |           • AWQ checkpoint (.awq)
            v
   +-----------------+
   | ⑥ Inference     |  vLLM / TGI / TensorRT-LLM
   |    Serving      |  llama.cpp / exllamav2
   +-----------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Quantization Granularity** | 양자화 단위 결정 | Per-tensor(전체 1개 scale, 단순) / Per-channel(채널별 scale, 정확) / Per-group(group_size=32/64/128, GPTQ 기본) — group이 작을수록 정확도 ^, 메모리 overhead ^ |
| **Scale Factor(S)** | 실수->정수 매핑 비율 | INT8: S = (max-min)/254 (asymmetric) / 2·max|x|/127 (symmetric), INT4: S = max\|x\|/7. 정보 보존의 핵심 |
| **Zero Point(Z)** | 비대칭 보정 | Asymmetric에서 0이 INT8의 128에 매핑되도록 보정. Z=0이면 symmetric(LLM W8A8에서 주로 사용) |
| **Calibration Module** | 활성화 분포 관측 | TensorRT의 `IInt8Calibrator` 인터페이스 구현, MinMax/Entropy/Percentile 알고리즘 선택, 캐시 파일로 재사용 |
| **QAT(Quantization-Aware Training) Hook** | 학습 중 양자화 시뮬레이션 | Straight-Through Estimator(STE)로 backward pass에서 ∂L/∂w ≈ ∂L/∂w_q, fake quant 노드 삽입 |
| **Dequantize Fusion** | 런타임 연산 통합 | `MatMul(Dequant(W), Dequant(X))` -> `MatMul_INT8(INT8_W, INT8_X)` + bias, TensorRT/LLM의 커널 fusion으로 메모리 I/O 최소화 |
| **Outlier Detector** | FP16 fallback 결정 | 채널별 activation ratio = max\|x\| / mean\|x\| > 6~10σ 시 outlier, SmoothQuant는 s = max\|x\|^α로 channel-wise rescale하여 outlier를 weight로 이전 |

### 5) Mixed Precision 구성 (W4A16, W8A8, W4A8)

실무에서는 단순히 전체를 동일 bit로 양자화하지 않고 다음과 같이 혼합한다:

- **W8A8 (Weight 8bit + Activation 8bit)**: 가장 보편적, INT8 Tensor Core 활용, 정확도 손실 < 0.5%
- **W4A16 (Weight 4bit + Activation 16bit)**: GPTQ/AWQ 기본값, weight만 INT4로 줄이고 activation은 FP16 유지 -> 정확도 손실 1~2%, 메모리 이득 큼
- **W4A8 (Weight 4bit + Activation 8bit)**: SmoothQuant + GPTQ 조합, FP16보다 ~4배 작고 INT8보다 정확
- **FP8 (E4M3 / E5M2)**: H100 native support, 양자화/역양자화 변환 비용 최소, NVIDIA Transformer Engine 활용

- **📢 섹션 요약 비유**: 양자화 알고리즘은 **옷장 정리**와 같다. **Min-Max 방식**은 가장 크고 작은 옷 기준으로 옷장 칸을 만들지만(특대형 코트 하나에 공간 다 차지), **Percentile 방식**은 일반적인 옷 99% 기준으로 칸을 만들고(코트는 접어서 별도 보관), **AWQ**는 "이 채널의 옷이 99% 사용된다"고 미리 알아채고 중요한 옷은 다른 곳에 정성껏 보관(scaling)하는 똑똑한 방식이다.

---

## Ⅲ. 비교 및 연결

### 1) INT8 vs INT4 vs FP8 vs FP16 비교

| 구분 | FP16 (Baseline) | INT8 | INT4 (GPTQ/AWQ) | FP8 (E4M3) |
|:---|:---|:---|:---|:---|
| **비트 수** | 16 bit | 8 bit (1/2) | 4 bit (1/4) | 8 bit (1/2) |
| **메모리 (70B)** | 140 GB | 70 GB | **35 GB** | 70 GB |
| **표현 가능 값 수** | 65,536 | 256 | 16 | 256 (비선형) |
| **Dynamic Range** | 6.5×10⁴ (지수) | 제한적(256 level) | 매우 제한(16 level) | FP16과 유사 (지수) |
| **Tensor Core 지원** | Volta+ (FP16) | Turing+ (INT8) | Hopper (INT4 TC 일부) | Hopper H100 (E4M3) |
| **정확도 손실 (per