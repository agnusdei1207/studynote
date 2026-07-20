---
title: "LLM Fine Tuning PEFT QLoRA Strategy"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 706
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: QLoRA는 4-bit NF4 양자화(NormalFloat) + Double Quantization + Paged Optimizers로 거대 LLM의 사전학습 가중치를 동결(Freeze)한 채, LoRA 어댑터(W_A∈R^(d×r), W_B∈R^(r×k))만 학습하여 65B 모델을 단일 48GB GPU에서 미세 조정 가능하게 만든 **메모리 효율 극대화형 PEFT(Parameter-Efficient Fine-Tuning)** 전략이다.
> 2. **가치**: Full Fine-Tuning 대비 학습 파라미터 수를 0.1% 이하(예: 65B 모델 기준 48M 파라미터)로 축소하고 GPU 메모리 사용량을 약 75% 절감(780GB -> 48GB)하면서도, 16-bit Full Fine-Tuning과 동등한 성능(SOLAR基准 benchmark)을 달성하여 학습 비용과 추론 지연(latency) 없이 도메인 적응이 가능하다.
> 3. **판단 포인트**: ① LoRA rank(r=8~64)·alpha(α=2r)·target_modules 선정(Attention-only vs All-Linear) ② bf16/fp16 mixed-precision 호환성(Ampere 이상 GPU) ③ 데이터셋 규모(<10K vs >100K)에 따른 epoch/learning rate 스케줄링 ④ 어댑터 병합(Merged Model) vs 분리 배포 ⑤ 베이스 모델 변동성(Base Model Drift) 대비 LoRA 버전 관리가 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

대규모 언어 모델(LLM, Large Language Model)의 파라미터 규모가 7B -> 70B -> 405B(GPT-4급 추정) -> 1T(추정)로 폭증함에 따라, **Full Fine-Tuning(Full-FT)** 방식은 엔터프라이즈 환경에서 현실적으로 불가능해졌다. Llama-2-70B 모델의 Full-FT는 Adam 옵티마이저 상태(8-byte), 그라디언트(2-byte), 마스터 가중치(4-byte)까지 포함해 단일 GPU 기준 **약 780GB의 VRAM**이 필요하며, 7B 모델조차도 Full-FT 시 약 60GB가 소요된다.

기존의 PEFT(Parameter-Efficient Fine-Tuning)인 **Adapter, Prefix-Tuning, Prompt-Tuning, IA³, LoRA** 등은 파라미터 수를 줄였으나 70B+ 모델에서는 베이스 가중치 자체를 fp16으로 로드해야 하므로 여전히 **메모리 병목**이 존재했다. **QLoRA(Dettmers et al., 2023, "QLoRA: Efficient Finetuning of Quantized LLMs", NeurIPS 2023)**는 이 문제를 ①4-bit NormalFloat(NF4) 양자화, ②Double Quantization, ③Paged Optimizers라는 세 가지 핵심 기법으로 해결하며 **단일 48GB GPU(A6000/RTX 6000 Ada)로 65B 모델 파인튜닝**을 가능하게 했다.

```text
[LLM 파인튜닝 패러다임의 진화: Full-FT -> LoRA -> QLoRA]

 Full Fine-Tuning          LoRA (2021)              QLoRA (2023)
 +--------------+         +--------------+         +--------------+
 |  W: fp16     |         |  W: fp16 ❄   |         |  W: NF4 ❄    |
 |  ΔW: fp16 🔥|         |  ΔW=W_A·W_B  |         |  ΔW=W_A·W_B  |
 |  모든 파라미터|         |  (r=4~64) 🔥|         |  (r=4~64) 🔥|
 +--------------+         +--------------+         +--------------+
 메모리: 780GB (65B)      메모리: ~150GB (65B)     메모리: ~48GB (65B)
 학습률: 1e-5              학습률: 3e-4              학습률: 2e-4
 파라미터: 100%            파라미터: ~0.5%          파라미터: ~0.1%
```

**Full Fine-Tuning 대비 QLoRA의 구조적 이점**:
- **메모리 효율**: 65B 모델 기준 780GB -> 48GB (16배 절감)
- **학습 속도**: 가중치 동결 + 4-bit dequantization은 forward pass에 오버헤드 0% (Dettmers et al., 2023 측정)
- **디스크 효율**: 어댑터 체크포인트 1개당 약 100~500MB(65B 모델 기준 32~256 rank)
- **멀티태스크**: 베이스 모델 1개 + N개 어댑터로 task switching (스토리지 1/N)

- **📢 섹션 요약 비유**: QLoRA는 마치 **"거대한 백과사전(베이스 모델)은 창고에 그대로 보관하되, 가장 필요한 페이지 몇 장(LoRA 어댑터)만 복사해서 사파리 연구원에게 지급"**하는 것과 같다. 연구원은 작은 노트로 답을 보완하고, 원본 백과사전은 절대 훼손하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

QLoRA의 핵심 메커니즘은 **"사전학습 가중치(W₀)는 4-bit NF4로 영구 동결, 학습 시점에만 on-the-fly dequantization하여 LoRA 어댑터의 forward/backward 계산"**이다. 이 메커니즘은 Hugging Face의 `peft` 라이브러리(v0.5.0+, 현재 v0.10+에서 `BitsAndBytesConfig` 통합)와 `bitsandbytes` 라이브러리(0.39.0+, 현재 0.43+)에 의해 구현된다.

```text
[QLoRA Forward Pass 상세 데이터 흐름]

  Input X (bf16, shape=[B, T, d])
        |
        v
  +-------------------------------------------------------------+
  |  Module: nn.Linear (QLoRA wrapped)                          |
  |                                                             |
  |  +--------------+        +----------------------------+    |
  |  | NF4 Storage  |        |   LoRA Adapter (trainable)  |    |
  |  | W₀ (frozen)  |        |                            |    |
  |  | shape:[d,k]  |        |   W_A ∈ ℝ^(d×r)  <- train  |    |
  |  | 4-bit/pack=8 |        |   W_B ∈ ℝ^(r×k)  <- train  |    |
  |  +------+-------+        |   α=16, r=8, init:A=Kaiming|    |
  |         |                |              B=zeros       |    |
  |         | dequant        +------------+---------------+    |
  |         v                              |                    |
  |  W₀_dequant (bf16) ---- X·W₀^T ---+   |                    |
  |                                    |   |                    |
  |                                    v   v                    |
  |                              X·(W₀ + (α/r)·W_B·W_A)^T       |
  |                              ---------------------          |
  |                              Y = bf16/fp16 output          |
  +-------------------------------------------------------------+
        |
        v
  Loss -> backward -> W_A, W_B만 gradient 업데이트
        W₀는 4-bit 그대로 유지 (gradient 계산 안 함)
```

### QLoRA 3대 핵심 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **4-bit NormalFloat (NF4)** | 베이스 가중치 양자화 | ① 입력 가중치를 정규분포 분위수(quantile) 기반 16-bin으로 매핑 ② dtype: `nf4` ③ fp4 대비 정보 손실 최소 (Dettmers 실험: perplexity 0.98% 손실) ④ block-wise quantization (block_size=64)으로 이상치(outlier)에 강건 |
| **Double Quantization (DQ)** | 양자화 상수의 재양자화 | ① 1차: W₀를 NF4로 양자화 (각 블록별 absmax scale factor `c₁` 필요, fp32) ② 2차: scale factor `c₁` 자체를 다시 8-bit fp8로 양자화하여 추가 `c₂` 저장 ③ 메모리 절감: 65B 모델 기준 약 **0.37GB/파라미터** 추가 절감 |
| **Paged Optimizers** | Optimizer 상태의 메모리 스왑 | ① Adam 옵티마이저의 momentum(v), variance(m²) 상태를 GPU VRAM ↔ CPU RAM ↔ NVMe 간 page-out ② `paged_adamw_32bit` 사용, OOM 방지 ③ `accelerate` 라이브러리와 통합, ZeRO-style offload |

### LoRA의 수학적 배경

원본 가중치 갱신: `W = W₀ + ΔW` (Full-FT)

LoRA 분해: `ΔW = (α/r) · W_B · W_A` where `W_A ∈ ℝ^(d×r)`, `W_B ∈ ℝ^(r×k)`

- **Rank `r`**: 병목 차원 (보통 4~64), r^ -> 표현력^, 파라미터수^
- **Alpha `α`**: 스케일링 계수, 보통 `α = 2r`로 설정 (LoRA 논문 권장)
- **Scaling factor**: `s = α / r`로 forward 시 곱해줌

파라미터 수 계산: `(d + k) × r` (예: d=4096, k=4096, r=8 -> 65,536 params per layer)

QLoRA 메모리 사용량 분해 (65B 모델 기준, batch=1, seq=512):
- **Model weights (NF4)**: 65B × 0.5 byte ≈ **32.5GB**
- **Double Quant scale (fp8)**: 65B × 0.125 byte ≈ **0.12GB** (8bit per block)
- **Activations + Buffers**: ~4GB
- **LoRA adapter (bf16)**: 48M × 2 byte ≈ **0.1GB**
- **Optimizer states (paged)**: 평소 0GB, peak 시 page-out
- **Total**: **~48GB** (vs Full-FT 780GB)

### Target Modules 선정 전략

| 모듈 범위 | 파라미터 비율 (7B 모델) | 적용 시나리오 | 권장 rank |
| :--- | :--- | :--- | :--- |
| Attention-only (`q_proj, v_proj`) | ~0.06% (LoRA 원논문) | 단순 instruction tuning | r=8 |
| Attention-all (`q, k, v, o_proj`) | ~0.12% | 일반 도메인 적응 | r=16 |
| All-Linear (Attention + MLP) | ~0.5% | 복잡한 추론, 코딩 | r=32~64 |
| Embeddings 포함 | ~1.2% | vocab 확장, 새로운 언어 | r=64+ |

- **📢 섹션 요약 비유**: QLoRA의 LoRA 어댑터는 **"대형 수도관에 끼우는 직경 8mm의 가는 보조 파이프"**와 같다. 물(정보)은 본관(W₀)을 그대로 흐르면서, 보조 파이프(W_A·W_B)만 통해 미세한 양을 더하거나 빼는 방식으로 전체 흐름을 조정한다. 본관은 절대 잘라내지 않는다.

---

## Ⅲ. 비교 및 연결

### PEFT 기법 간 상세 비교

| 구분 | Full Fine-Tuning | LoRA (2021) | QLoRA (2023) | Adapter (2019) | Prefix-Tuning (2021) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **학습 파라미터** | 100% | 0.5~1% | 0.1~0.5% | 3~5% | 0.1% |
| **베이스 가중치** | 업데이트 | 동결(fp16) | 동결(NF4) | 동결(fp16) | 동결(fp16) |
| **메모리 (65B)** | 780GB | ~150GB | ~48GB | ~160GB | ~145GB |
| **추론 latency** | 베이스 동일 | 0% (병합 시) | 0% (병합 시) | 5~20% (skip) | 10~30% |
| **병합 가능성** | N/A | ✅ `merge_and_unload()` | ✅ 동일 | ❌ 구조 변경 | ❌ |
| **성능 (MMLU)** | 100% (기준) | 99% | 99% | 95~97% | 92~95% |
| **학습 안정성** | 매우 높음 | 높음 | 높음 (bf16 권장) | 중간 | 낮음 (하이퍼파라미터 민감) |
| **멀티태스크** | 어려움 (모델 복제) | 쉬움 (어댑터 교체) | 쉬움 | 보통 | 보통 |

### 양자화 정밀도별 트레이드오프

| 정밀도 | 메모리/파라미터 (65B) | 상대 성능 | 주요 사용처 | 하드웨어 |
| :--- | :--- | :--- | :--- | :--- |
| **fp32** | 4 byte (260GB) | 100% (기준) | Full-FT (legacy) | V100/A100 |
| **fp16/bf16** | 2 byte (130GB) | ~99.9% | Full-FT, LoRA | A100/H100 |
| **int8 (LLM.int8())** | 1 byte (65GB) | ~99% | LoRA-INT8, 추론 | A100 |
| **NF4 (QLoRA)** | 0.5 byte (32.5GB) | ~98% | QLoRA 학습/추론 | A100+ 권장 |
| **int4 (GPTQ)** | 0.5 byte | ~96% | 추론 전용 (학습불가) | 모든 GPU |
| **int2 (AQLM)** | 0.25 byte | ~90% | 엣지 추론 | CPU 가능 |

### 통합 생태계 (Tech Stack)

```text
[QLoRA 실무 구현 스택]

  +-----------------------------------------+
  |   Hugging Face Transformers (4.36+)    |
  |   +------------------------------+      |
  |   |   PEFT Library (0.10+)       |      |
  |   |   + LoraConfig, get_peft_model|      |
  |   |   + prepare_model_for_kbit_  |      |
  |   |   |   training (4-bit)        |      |
  |   |   + Lora.merge_and_unload()   |      |
  |   +--------------+---------------+      |
  |                  |                       |
  |   +--------------v---------------+      |
  |   |   bitsandbytes (0.43+)       |      |
  |   |   + Linear4bit, Linear8bit   |      |
  |   |   + NF4, FP4 양자화          |      |
  |   |   + paged_adamw_32bit       |      |
  |   +--------------+---------------+      |
  |                  |                       |
  |   +--------------v---------------+      |
  |   |   Accelerate (0.25+)         |      |
  |   |   + DeepSpeed ZeRO-3 통합    |      |
  |   |   + CPU/NVMe offload         |      |
  |   |   + DDP + BF16 MixedPrec.   |      |
  |   +------------------------------+      |
  |                                          |
  |   [+ TRL (SFT/PPO/ORPO)                |
  |    + datasets + Wandb/Tensorboard]       |
  +-----------------------------------------+
```

### LoRA 변형 알고리즘 발전

