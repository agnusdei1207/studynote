---
title: "Transformer Architecture Attention Mechanism"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 641
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜스포머 어텐션은 입력 토큰의 Query·Key·Value 벡터 간 내적(QK^T/√d_k) 후 softmax 가중합으로 모든 위치 간 동적 연관성을 O(1) 거리로 포착하는 셀프 어텐션(Self-Attention) 메커니즘이며, 인코더-디코더·크로스·마스크드·멀티헤드 등 변형이 BERT·GPT·ViT·TTS 등 전 영역을 지배한다.
> 2. **가치**: 시퀀스 길이 n에 대해 시간 복잡도가 레이어당 O(n²·d)이나 **시퀀스 내 완전 병렬화(parallelism)**로 GPU/TPU utilization 90% 이상 달성, RNN 대비 학습 속도 10~100배, 장의존성(long-range dependency) 손실 0, GPT-4·Claude·Gemini 등 1T+ 파라미터 LLM의 전제 조건.
> 3. **판단 포인트**: n² 메모리 폭증 -> FlashAttention·PagedAttention·Sliding Window·Linear Attention 트레이드오프, 헤드 수 h와 d_k=64 표준, KV Cache로 추론 latency 개선 vs 메모리, RoPE·ALiBi 등 위치 인코딩 선택이 외삽 길이 결정.

---

## Ⅰ. 개요 및 필요성

2017년 Vaswani et al.의 "Attention Is All You Need" 이전, NLP의 주류는 RNN/LSTM 기반 seq2seq였다. 인코더는 가변 길이 입력을 **고정 크기 context vector**에 압축(정보 병목)했고, 디코더는 이를 순차적으로 풀어가며 기울기 소실(vanishing gradient)로 인해 실효 문맥 거리가 200~500 토큰에 불과했다. Bahdanau Attention(2014)이 가변 가중합으로 이를 일부 해소했으나, RNN 본체는 여전히 **순차적(sequential)**이라 분산 학습과 장문 처리 모두 곤란했다.

트랜스포머는 **"순환(Recurrence)을 완전히 제거하고 Attention만으로 시퀀스를 모델링한다"**는 대전제 하에, 모든 토큰 쌍 간의 관계를 행렬 연산 한 번에 계산한다. 이로써 (1) 시퀀스 길이 방향 병렬화, (2) 임의 거리 토큰 직접 연결(감쇠 없음), (3) 미분 시 그래프 깊이 O(1) 역전파가 가능해졌고, 8년 만에 LLM·Vision·Speech·Code·Multi-modal 전 영역의 de facto 표준이 되었다.

```text
[ RNN/LSTM vs Transformer: 정보 흐름 비교 ]

  (기존) RNN Seq2Seq with Fixed Context Vector
  ---------------------------------------------
   x1 -►+
   x2 -►+--► [Encoder RNN] --► h_enc --► [Decoder RNN] --► y
   x3 -►+  (sequential)        (병목)     (sequential)
                                |
                                +- 길이 길수록 정보 손실 큼
                                    기울기 소실 위험

  (트랜스포머) Self-Attention: 전 토큰 완전 연결
  ---------------------------------------------
   x1 --►+
   x2 --►+-► [Self-Attention × L] --► [FFN × L] --► Output
   x3 --►+  (모든 쌍을 한 번에 행렬 계산, GPU 병렬화)
           +-- QKᵀ/√dₖ --► softmax --► 가중합 V
               +---+ +---+ +---+
               |Q₁K₁| |Q₁K₂| |Q₁K₃|   <- 토큰1이 2,3번에 주목
               |Q₂K₁| |Q₂K₂| |Q₂K₃|   <- 토큰2가 1,3번에 주목
               |Q₃K₁| |Q₃K₂| |Q₃K₃|   <- 토큰3이 1,2번에 주목
               +---+ +---+ +---+
               ②Q, K, V는 같은 입력에서 X·W^Q, X·W^K, X·W^V로 생성
```

**왜 반드시 필요한가?**
- **RNN의 O(n) 순차 의존성**은 8xA100 NVLink 환경에서도 8K 토큰 학습에 수십 일이 걸린다. Self-Attention은 O(n²)이지만 **레이어 내부 완전 병렬화**로 wall-clock 기준 압도적 우위.
- **CNN은 receptive field를 깊이·dilated로 키우나** 절대 거리 의존성이 누적 손실. Attention은 거리 무관.
- **장기 의존성(Long-range dependency)**: LLaMA-3 8K, Claude 200K, Gemini 1.5 1M 토큰 컨텍스트는 어텐션 없이는 불가능.

- **📢 섹션 요약 비유**: RNN이 "줄서서 한 명씩 손에 쪽지를 전달하는 게임"이라면, 트랜스포머는 "모든 학생이 동시에 서로의 이름표를 확인하고 관련 있는 친구에게 점수를 주는 시험"이다. 한꺼번에 보기 때문에 거리와 무관하게 공정한 평가를 받는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

트랜스포머의 어텐션 메커니즘은 **Scaled Dot-Product Attention**을 기본 빌딩 블록으로, 이를 **Multi-Head**로 확장하고, 인코더·디코더·크로스 등 다양한 변형으로 조합한다. 핵심 수식은 다음과 같다.

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1,\dots,\text{head}_h)\,W^O$$
$$\text{head}_i = \text{Attention}(QW_i^Q,\, KW_i^K,\, VW_i^V)$$

여기서 √d_k로 스케일링하는 이유는 d_k 증가에 따른 QK^T 분산 증가로 softmax가 극단(gradient 0)을 향해 saturate되는 현상을 방지하기 위함이다. d_k=64일 때 분산 ≈ 64, sqrt(64)=8로 나누면 표준편차 1로 안정화된다.

```text
[ 트랜스포머 어텐션 상세 아키텍처 (인코더-디코더 + Self/Cross/Masked Attention) ]

  +------------------- Encoder Stack (N=6~96 layers) ---------------------+
  |                                                                       |
  |  Input Embedding + PosEnc(x)                                          |
  |         |                                                             |
  |         v                                                             |
  |  +- Multi-Head Self-Attention (Bi-directional, no mask) -+            |
  |  |   Q = K = V = x·W^Q,K,V   <- 동일 입력에서 3개 투사   |            |
  |  |   attn = softmax(QK^T/√d_k) V                         |            |
  |  |   Concat(head_1..head_h) W^O                          |            |
  |  +--------------------------------------------------------+            |
  |         | Add & LayerNorm (Pre-Norm: LN(x+Sublayer(x)) 현대 표준)    |
  |         v                                                             |
  |  Position-wise FFN: FFN(z) = max(0, zW1+b1)W2+b2  (d_ff = 4·d_model) |
  |         | Add & LayerNorm                                             |
  |         v  (× N layers)                                               |
  +-----------------------------------------------------------------------+

  +------------------- Decoder Stack (N layers, mirror) ------------------+
  |                                                                       |
  |  Output Embedding + PosEnc(y)                                         |
  |         |                                                             |
  |         v                                                             |
  |  +- Masked Self-Attention (Causal mask: 미래 토큰 -∞) --+             |
  |  |   mask = upper triangular(-inf) -> softmax 시 0      |             |
  |  +------------------------------------------------------+             |
  |         | Add & LayerNorm                                             |
  |         v                                                             |
  |  +- Cross-Attention (Encoder-Decoder) --------------------+           |
  |  |   Q from Decoder, K·V from Encoder output              |           |
  |  |   Attention(Q_dec, K_enc, V_enc) -> context             |           |
  |  +--------------------------------------------------------+           |
  |         | Add & LayerNorm                                             |
  |         v                                                             |
  |  Position-wise FFN + LayerNorm (× N)                                  |
  |         v                                                             |
  |  Linear(vocab) -> Softmax -> next token                                 |
  +-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Scaled Dot-Product Attention** | 단일 어텐션 연산 단위 | `QK^T/√d_k`로 (n×d_k)·(d_k×n) = (n×n) 어텐션 행렬 계산 -> softmax -> (n×n)·(n×d_v) = (n×d_v). d_k=64 표준, FLOPs: O(n²·d). |
| **Multi-Head Attention (MHA)** | 서로 다른 표현 부분공간 병렬 학습 | h=8~128개의 head를 독립 attention 후 concat·W^O 투사. h·d_k = d_model (예: d=512, h=8, d_k=64). 각 head는 문법·의미·장거리 참조 등 **다른 관계** 학습. |
| **Causal / Masked Attention** | 자기회귀(autoregressive) 생성을 위한 미래 마스킹 | `mask = -1e9`를 미래 위치에 더해 softmax->0. GPT·LLaMA 계열 핵심. KV Cache로 추론 시 O(n²) 재계산 회피. |
| **Cross-Attention** | 인코더-디코더 정보 전달 | Q는 디코더, K·V는 인코더 출력. 번역·TTS·OCR 등 (source, target) 길이 다른 task에 필수. |
| **Positional Encoding (PE)** | 순서 정보 주입 (Attention 자체는 순서 무관) | Sinusoidal(원본), Learned(불안정), **RoPE(Rotary Position Embedding)** – LLaMA·GPT-NeoX 채택, 회전 행렬로 상대 위치·길이 외삽 우수, **ALiBi** – 선형 편향 attention, BLOOM 채택. |
| **LayerNorm 위치** | 학습 안정화 | Post-LN(원본, 깊어지면 불안정) vs **Pre-LN**(현대 LLM 표준, GPT-3·LLaMA) vs RMSNorm(LLaMA·Gemma, LN 단순화). |
| **KV Cache** | 추론 시 디코더 attention 재계산 제거 | 과거 K·V를 메모리에 누적 -> 새 토큰 생성 시 attention 연산을 O(n²) -> O(n)으로 감소. 4-bit·Paged KV(GPU 메모리 단편화 해결, vLLM) 등으로 최적화. |

**복잡도 심화 분석**
- **Self-Attention FLOPs**: 2·n²·d (QK^T와 AV 각각)
- **메모리**: Attention 행렬 n×n이 dominant -> **n=2048, h=32, fp16 시 1GB** (배치·헤드 곱)
- **Long-context(N=128K) 시 1M 셀** -> FlashAttention이 이를 **HBM↔SRAM tiling**으로 IO 최적화(메모리 10×v, 속도 2~4×^)
- **선형 attention** (Performer, Linformer): Kernel φ(Q)·φ(K)^T로 n²->n·k(k≪n) 단조소실, 정확도 트레이드오프

- **📢 섹션 요약 비유**: Multi-Head Attention은 "8명의 심사위원이 각자 다른 기준(문법·의미·대명사·어조 등)으로 답안지를 채점하고, 마지막에 종합 점수를 매기는 것"이다. 단일 attention이 "한 명의 독선적 심사위원"이라면, multi-head는 "다양한 시각의 합의".

---

## Ⅲ. 비교 및 연결

| 구분 | **Self-Attention (Transformer)** | **RNN / LSTM** | **CNN (1D Conv)** | **State Space Model (Mamba)** |
| :--- | :--- | :--- | :--- | :--- |
| **시간 복잡도 (per layer)** | O(n²·d) | O(n·d²) | O(n·k·d) (k=kernel) | O(n·d) (선형) |
| **순차 의존성** | 없음 (완전 병렬) | 있음 (필수 순차) | 부분 (국소) | 없음 (병렬) |
| **장기 의존성** | O(1) 거리 직접 연결 | O(n) 경로, 기울기 소실 | O(log n) (dilated) | O(1) (선형 recurrent) |
| **메모리 (활성화)** | O(n²) 어텐션 행렬 | O(n·d) hidden | O(n·k·d) | O(d) (선형) |
| **Inductive bias** | 약함 (data-hungry) | 강함 (순서) | 강함 (locality·translation) | 약~중 |
| **추론 latency** | O(n²) (KV Cache 시 O(n) per token) | O(n) (병렬 불가) | O(n) | O(1) per token |
| **주 사용 모델** | GPT·BERT·ViT·Whisper | 초기 seq2seq, time-series | 초기 text CNN, WaveNet | Mamba·Mamba-2 (state space) |
| **장문 처리** | FlashAttn·PagedAttn 필요 (수백K까지) | 수천 토큰 한계 | 수만 토큰 가능 | 1M+ 가능 (실험적) |
| **학습 안정성** | Pre-LN·RMSNorm·Warmup 필수 | BPTT·gradient clip | 안정 | 비교적 안정 |

**연결 통합 포인트**
- **Encoder-only (BERT 계열)