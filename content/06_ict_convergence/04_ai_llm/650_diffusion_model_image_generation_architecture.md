---
title: "Diffusion Model Image Generation Architecture"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 650
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 디퓨전 모델은 고정된 마르코프 체인(Forward Process)을 통해 점진적으로 가우시안 노이즈를 주입한 뒤, U-Net 기반 신경망으로 학습된 역방향 과정(Reverse Process) ε_θ(x_t, t)을 통해 노이즈를 복원하는 계층적 잠재 변수 생성 모델(Latent Hierarchical Generative Model)임.
> 2. **가치**: GAN 대비 모드 붕괴(Mode Collapse) 부재, FID/IS 기준 SOTA 품질(Stable Diffusion XL 기준 FID 6.0 이하), 텍스트·이미지·제어 신호(Canny, Depth, Pose) 등 다중 모달 컨디셔닝의 분기 없이 통합 가능.
> 3. **판단 포인트**: Latent vs Pixel 공간 연산, 샘플러(DDPM/DDIM/DPM-Solver/LCM), Classifier-Free Guidance Scale(w), 어텐션 백본(Cross/Self-Attention vs DiT) 선택이 품질·속도·메모리 간 트레이드오프의 핵심 결정 변수임.

---

## Ⅰ. 개요 및 필요성

기존 생성 모델 패러다임은 두 가지 명백한 한계를 지니고 있었다. **GAN(Generative Adversarial Network)**은 판별자와 생성자 간 미분 가능한 적대적 손실로 고해상도 합성(예: StyleGAN3, BigGAN)은 가능했으나, 학습 불안정성(Adversarial Instability)과 모드 붕괴 현상, 그리고 잠재 공간의 의미론적 분리 부족 문제를 안고 있었다. **VAE(Variational Autoencoder)**는 ELBO 기반의 안정적 학습이 가능했으나 생성 품질이 GAN 대비 현저히 낮고, **AR(Autoregressive) 모델**(PixelCNN, VQ-VAE-2, Parti)은 토큰 단위 자기회귀 생성을 통해 충실도는 확보했으나, 추론 지연이 토큰 수에 선형(또는 그 이상)으로 증가하여 1024×1024 해상도에서 실용적이지 못했다.

2020년 **DDPM(Denoising Diffusion Probabilistic Models, Ho et al.)**이 ImageNet 256×256에서 FID 3.17을 기록하며, 이 한계를 근본적으로 전환했다. 이후 **Score-based Model**(Song & Ermon, NeurIPS 2019)과 **Stochastic Differential Equation**(SDE, Song et al., ICLR 2021) 관점으로 일반화되었고, **Latent Diffusion Model(LDM, Rombach et al., CVPR 2022)**은 U-Net의 연산을 픽셀 공간이 아닌 사전 학습된 VAE의 잠재 공간(latent space, 일반적으로 8× 다운샘플링)으로 이동시켜 연산량을 약 48배(O(2^6)) 절감하면서도 동일 품질을 달성했다. 이것이 Stable Diffusion v1/v2/XL로 산업화되는 결정적 토대가 되었다.

근본적인 동기는 **"고해상도 이미지 합성을 안정적으로, 그리고 텍스트와 같은 의미론적 컨디셔닝과 통합"**하는 것이었다. 디퓨전은 본질적으로 denoising score matching을 통해 데이터 분포의 그래디언트(Stein Score ∇_x log p(x))를 학습하는 것이며, 이 점수 함수는 어떤 컨디셔닝 신호와도 conditioning network(CLIP Text Encoder, ControlNet, IP-Adapter)와 결합 가능한 모듈러 구조를 갖는다.

```text
+----------------------------------------------------------------------+
|           픽셀 공간(Pixel Space) vs 잠재 공간(Latent Space)          |
+----------------------------------------------------------------------+

   [Pixel Diffusion - e.g., Imagen, DALL·E 2 prior]               [Latent Diffusion - e.g., Stable Diffusion]
   +---------------+                                              +------------------+
   |  RGB Image    |                                              |  RGB Image       |
   |  H×W×3 (1024) |                                              |  H×W×3 (1024)   |
   |  3,145,728    |                                              |  3,145,728       |
   |  차원         |                                              |  차원            |
   +------+--------+                                              +--------+---------+
          | 직접 Diffusion (U-Net 연산량 폭증)                                | VAE Encoder v
          v                                                                  v
   +---------------+                                              +------------------+
   |  U-Net ε_θ    |                                              |  Latent z        |
   |  (메모리 폭증)|                                              |  H/8×W/8×4      |
   |               |                                              |  49,152 차원     |
   +---------------+                                              +--------+---------+
                                                                              | U-Net ε_θ (경량화)
                                                                              v
                                                                  +------------------+
                                                                  |  U-Net ε_θ       |
                                                                  |  (메모리 1/48)    |
                                                                  +--------+---------+
                                                                           | VAE Decoder ^
                                                                           v
                                                                  +------------------+
                                                                  |  RGB Image       |
                                                                  |  H×W×3 (1024)    |
                                                                  +------------------+
```

**기존 패러다임 대비 변화의 핵심**:
- **GAN의 적대적 학습 -> Likelihood 기반 Score Matching**: 손실 함수가 단순한 MSE(||ε - ε_θ(x_t, t)||²)로 환원되어 안정적.
- **잠재 공간 압축**: 8×8 다운샘플링으로 어텐션 연산의 시퀀스 길이가 1/64로 감소.
- **모듈화**: Text Encoder(CLIP/T5) + UNet + VAE Decoder로 분리되어 각 컴포넌트 독립 최적화/교체 가능.

- **📢 섹션 요약 비유**: 디퓨전 모델은 **"안개 낀 유리창에 적힌 글씨를 천천히 닦아내며 원래 그림을 복원하는 화가"**와 같다. 한 번에 그리지 않고 거친 노이즈에서 점진적으로 윤곽, 색채, 디테일을 순차적으로 복원하기 때문에 실수할 여지가 적고, 그 과정을 외부 가이드(텍스트·제어 신호)로 정밀하게 조종할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 수학적 기반: 순방향/역방향 마르코프 체인

**순방향 과정(Forward/Diffusion Process) q(x_t | x_{t-1})**은 사전 정의된 분산 스케줄 β_1, ..., β_T (T=1000)에 따라 원본 이미지 x_0에 가우시안 노이즈를 점진적으로 주입한다:

```
q(x_t | x_{t-1}) = N(x_t; √(1-β_t) x_{t-1}, β_t I)
q(x_t | x_0)   = N(x_t; √(ᾱ_t) x_0, (1-ᾱ_t) I),  where ᾱ_t = ∏_{s=1}^{t} α_s, α_s = 1-β_s
```

**역방향 과정(Reverse Process) p_θ(x_{t-1} | x_t)**은 신경망이 예측한 평균 μ_θ(x_t, t) 및 분산 Σ_θ(x_t, t)로 파라미터화된다. 학습 시 **단순화된 손실 함수(L_simple)**는 다음과 같다:

```
L_simple = E_{t, x_0, ε} [ ||ε - ε_θ(√ᾱ_t x_0 + √(1-ᾱ_t) ε, t)||² ]
```

즉, U-Net ε_θ는 t 시점에서 샘플링된 노이즈 ε ∈ N(0, I)을 직접 회귀하도록 학습된다. 이 단순화가 DDPM 성공의 비결로, 변분 하한(ELBO)의 KL 발산 항을 사실상 노이즈 예측 MSE로 근사한 것이다.

### 2. 아키텍처 다이어그램: Latent Diffusion Model (Stable Diffusion 계열)

```text
+----------------------------------------------------------------------------+
|                  Latent Diffusion Model (LDM) Inference Flow               |
+----------------------------------------------------------------------------+

  [Text Prompt: "A cyberpunk city at night, neon lights"]
                    |
                    v
  +--------------------------------+
  |  Text Encoder (Frozen)         |
  |  - CLIP ViT-L/14  (SD 1.5)    |   <- Token Embedding: (B, 77, 768)
  |  - OpenCLIP ViT-bigG (SDXL)   |   <- (B, 77, 1280)
  |  - T5-XXL        (SD3/Imagen) |   <- (B, 256, 4096)
  +--------------+-----------------+
                 | context c (B, L, d)
                 v
  +-------------------------------------------------------------------------+
  |                       U-Net (ε_θ) with Cross-Attention                 |
  |  +-----------------------------------------------------------------+   |
  |  | Input:  z_t ∈ R^(B, 4, 64, 64)  (latent)                       |   |
  |  | Time Embedding: t -> sinusoidal -> MLP -> (B, d_t)                |   |
  |  |                                                                 |   |
  |  |  +- Encoder Path (Downsample) ------------------------------+   |   |
  |  |  |  ResBlock(in, out) + CrossAttn(c) + SelfAttn + Down       |   |   |
  |  |  |  64×64  ->  32×32  ->  16×16  ->  8×8                       |   |   |
  |  |  +----------------------------------------------------------+   |   |
  |  |                          | Bottleneck                           |   |
  |  |  +- Decoder Path (Upsample) ------------------------------+   |   |
  |  |  |  ResBlock + CrossAttn(c) + SelfAttn + Up + Skip Concat |   |   |
  |  |  |  8×8  ->  16×16  ->  32×32  ->  64×64                       |   |   |
  |  |  +----------------------------------------------------------+   |   |
  |  |  Output: ε_pred ∈ R^(B, 4, 64, 64)  (predicted noise)          |   |
  |  +-----------------------------------------------------------------+   |
  +--------------------+----------------------------------------------------+
                       |
                       v
  +-------------------------------------------------------------------------+
  |                      Sampler (Denoising Loop)                           |
  |  - DDPM (1000 step, ancestral)                                          |
  |  - DDIM (50 step, deterministic, η=0)                                   |
  |  - DPM-Solver (20 step, 2nd-order ODE)                                  |
  |  - LCM (4-8 step, consistency model)                                    |
  |  - Euler / Heun (FlowMatch in SD3)                                      |
  |                                                                         |
  |  ε̃ = (1+w)·ε_θ(z_t, t, c) − w·ε_θ(z_t, t, ∅)   <- Classifier-Free     |
  |  (w: guidance scale, 일반적으로 5.0~12.0)                              |   Guidance
  +--------------------+----------------------------------------------------+
                       | z_0 (denoised latent)
                       v
  +--------------------------------+
  |  VAE Decoder (Frozen)          |  <- 픽셀 복원: z_0 ∈ R^(B,4,64,64)
  |  - 8× Upsample                 |     -> x_0 ∈ R^(B,3,512,512)
  +--------------+-----------------+
                 v
            [Generated Image]
```

### 3. 핵심 컴포넌트 비교표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **VAE Encoder/Decoder** | 잠재 공간 압축/복원 | KL-regularized Autoencoder. Encoder E: R^(3,H,W) -> R^(4,H/8,W/8), Decoder D: 역변환. SDXL의 경우 f8 변종과 f16 변종이 존재하며, f16은 디테일 보존 ^, f8은 추론 속도 ^. 사전학습 후 가중치를 freeze하고 U-Net만 학습(LDM의 핵심 trick). |
| **Text Encoder** | 텍스트를 의미론적 임베딩으로 변환 | SD 1.5/2.1: CLIP ViT-L/14 (77 토큰, 768 차원). SDXL: OpenCLIP ViT-bigG + CLIP ViT-L (dual text encoder, 1280+768 concat). SD3: T5-XXL + CLIP-L + CLIP-bigG (4096차원, 256 토큰으로 확장되어 인-컨텍스트 텍스트 이해력 ^). 모두 학습 중 freeze. |
| **U-Net (Denoiser ε_θ)** | 잠재 노이즈의 점수 함수 근사 | ResNet 블록 + Self-Attention + Cross-Attention (key/value = text embedding). 1.0B~2.6B 파라미터. Timestep t는 sinusoidal positional encoding -> MLP -> 각 ResBlock에 scale/shift로 주입(AdaGN, Adaptive Group Norm). Group Norm의 γ, β를 t 임베딩에서 예측. |
| **Noise Scheduler** | β_t 시퀀스 정의 | Linear(simple), Cosine(Nichol & Dhariwal, 2021, SD 계열 채택), Scaled Linear. Cosine은 t=0 근방에서 노이즈를 더 천천히 주입하여 저주파 정보 보존에 유리. SD3는 Rectified Flow 기반의 σ(t)=t 노이즈 스케줄 사용. |
| **Sampler (ODE/SDE Solver)** | z_T ~ N(0,I) -> z_0 역적분 | DDPM: 1000 step, ancestral sampling. DDIM: 50 step, deterministic. DPM-Solver(++): 10~20 step, 2nd/3rd order multistep. LCM: Latent Consistency Model로 4 step. FlowMatchEulerDiscrete: SD3 채택, OT(Optimal Transport) 경로. |

### 4. Classifier-Free Guidance (CFG)

**핵심 메커니즘**: 학습 시 10%의 확률로 텍스트 조건 c를 ∅(null token)으로 마스킹하여 unconditional 모델 ε_θ(z_t, t, ∅)을 동시에 학습한다. 추론 시 다음 식으로 가이던스를 적용:

```
ε̃_θ(z_t, t, c) = (1 + w) · ε_θ(z_t, t, c