---
title: "Time Series Forecasting Autoregressive Transformer"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 664
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시계열 데이터의 시간적·변량간(long-range, cross-variate) 의존성을 Multi-Head Self-Attention으로 포착하고, 자기회귀(Autoregressive) 디코더가 prior output을 컨텍스트로 재투영하여 multi-step 미래를 순차 생성하는 encoder-decoder 패러다임. 핵심 수식: $\hat{y}_{t+1}, \ldots, \hat{y}_{t+H} = \arg\max P(y_{t+1:H} \mid y_{t-L+1:t}; \theta)$을 step-by-step rollout으로 근사.
> 2. **가치**: ARIMA/Prophet 대비 다변량·비선형·계절성·휴일 효과 동시 흡수, LSTM/TCN 대비 5~10× 학습 가속(병렬 attention), M5/M4/Electricity 벤치마크에서 MAPE 15~30% 개선, lookback window L=512~2048으로 장주기 패턴까지 모델링 가능.
> 3. **판단 포인트**: ① Autoregressive(AR) vs Direct Multi-step(DMS, e.g., N-BEATS/PatchTST) trade-off ② O(L²) attention complexity -> Informer·PatchTST 등 sparse/patch 기법 선택 ③ Stationarity 역전(예: RevIN) 적용 여부 ④ Channel-Independent(ci) vs Channel-Dependent(cd) 임베딩 전략 ⑤ Quantile/Pinball loss 기반 probabilistic forecasting 채택.

---

## Ⅰ. 개요 및 필요성

전통 시계열 예측은 **ARIMA(p,d,q)**, **ETS(Error/Trend/Seasonality)**, **Prophet**(Facebook, 2017)이 주류였으나, (1) **다변량(multivariate) 상호작용** (예: 30개 매장 SKU 간 cannibalization), (2) **비선형 exogenous 변수**(날씨, 프로모션, 캘린더 이벤트), (3) **장주기 의존성**(연간 단위 seasonal lag) 처리에 한계가 있었다. RNN/LSTM 기반 DeepAR(Salinas 2020), N-BEATS(Oreshkin 2020) 등이 이를 보완했으나, **순차 처리로 인한 학습 병목**과 **장거리 그래디언트 소실**이 잔존했다.

Vaswani et al.의 **Transformer(2017)**가 NLP에서 입증한 self-attention의 **O(1) path length**는 시계열의 long-range dependency 해소에 이상적이며, 이를 시계열에 적용하는 흐름이 가속화되었다. 자기회귀 트랜스포머는 **encoder에 lookback window L**을, **decoder에 예측 horizon H**를 입력해 $P(y_{t+1:H} \mid y_{t-L+1:t})$를 점 또는 분포로 출력한다.

특히 **Autoregressive(AR) decoding**은 $\hat{y}_{t+k}$를 다시 디코더 입력에 주입하여 $k=1 \to H$까지 rollout하는 방식으로, 시계열의 **인과적(causal) 순서**를 자연스럽게 보존하고 **가변 길이 horizon**을 단일 모델로 처리할 수 있다는 강점이 있다.

```text
[Traditional vs Transformer-based Time Series Forecasting]

   과거 방식 (ARIMA / Prophet / LSTM)                Transformer 기반 자기회귀 예측
   +--------------------------+                  +----------------------------------+
   |  수동 feature engineering|                  |  End-to-End Representation       |
   |  (lag, fourier, holiday) |                  |  (값 + 위치 + 시간 임베딩)         |
   |           v              |                  |            v                     |
   |  선형/단순 비선형 모델     |                  |   Multi-Head Self-Attention       |
   |           v              |                  |            v                     |
   |  Point Forecast만 출력    |                  |  Probabilistic (Quantile/Student-t)|
   +--------------------------+                  +----------------------------------+
   문제: 변량 1~3개 적정, 장기 의존 약함,            해결: 변량 수십~수백개 처리, L=2048 장기 패턴,
         분산·신뢰구간 미제공                          조건부 분포 출력 (P10/P50/P90)
```

**기존 패러다임의 한계 vs 신규 패러다임**:
- *ARIMA*: 정상성(stationarity) 가정 필수, 비선형 exogenous 흡수 불가 -> 비정상·계절 변동 큰 도매/소매 데이터에서 잔차 자기상관 잔존.
- *LSTM(DeepAR)*: 시점 간 순차 처리로 $L=512$ 이상 시 학습 시간 급증, attention-free 구조로 long-range lag 직접 모델링 불가.
- *Prophet*: 가법 모형(additive) 기반이라 multiplicative seasonality, regime change(코로나 등) 처리에 약함.
- *Transformer-AR*: O(L²) 비용은 있으나 GPU 병렬화로 학습 가속, attention map으로 **어떤 과거 시점이 현재 예측에 기여했는지 해석 가능**(시계열 Attention interpretability), 그리고 conditional distribution $P(y_{t+1:H} \mid \mathbf{x}_{1:t})$ 직접 학습으로 **재고·리스크** 의사결정 지원.

- **📢 섹션 요약 비유**: 시계열 예측 자기회귀 트랜스포머는 **"과거 5년 치 신문을 한 번에 훑고, 다음 주 일기예보를 한 줄씩 이어 쓰는 경험 많은 기상 캐스터"**와 같다. AR 캐스터는 어제·지난주·작년 데이터를 동시에 참조(attention)하면서 오늘부터 내일까지 한 단어씩 이어 쓴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

시계열 자기회귀 트랜스포머는 **입력 임베딩 -> Encoder(N×) -> Decoder(M×) -> AR rollout -> 출력 프로젝션**의 5단계 파이프라인으로 구성된다. 핵심은 **시계열 특화 임베딩(temporal feature embedding)**과 **인과적 마스킹(causal masking) + lookback cross-attention** 결합이다.

```text
[Autoregressive Transformer for Time Series — Detailed Architecture]

                 Lookback Window (L=512)
  +-------------------------------------------------------------+
  | y_{t-L+1}, y_{t-L+2}, ..., y_{t-1}, y_t                   |  <- 과거 관측값
  +-------------------------------------------------------------+
                              |
       +----------------------+----------------------+
       v                      v                      v
  Value Embedding      Positional Encoding    Temporal Features
  (Linear projection  (sinusoidal or         (hour-of-day, day-of-week,
   d_model=512)        learned)               month, holiday, age,
                                             known_future=exog)
       +----------------------+----------------------+
                              v  (sum) -> Input Embedding Z ∈ ℝ^{L×d}

                              v
   +--------------- ENCODER STACK (N=3~6) ---------------+
   |  +---------------------------------------------+   |
   |  |  Multi-Head Self-Attention (h=8)            |   |  <- 시점 간 attention
   |  |  Q,K,V = Z·W^Q, Z·W^K, Z·W^V               |   |     O(L²) = 512²=262K
   |  |  Attn = softmax(QKᵀ/√d)·V                 |   |     log/source 기여도 가시화
   |  +---------------------------------------------+   |
   |                       v Add & LayerNorm             |
   |  +---------------------------------------------+   |
   |  |  Position-wise FFN (d_ff=2048, GELU)        |   |  <- 비선형 변환
   |  +---------------------------------------------+   |
   |                       v Add & LayerNorm             |
   +-----------------------------------------------------+
                              |  -> Memory K_enc, V_enc
                              v
   +--------------- DECODER STACK (M=3~6) ---------------+
   |   Step k=1: 입력 = [y_t ; known_future_{t+1}]      |
   |   Step k=2: 입력 = [ŷ_{t+1} ; known_future_{t+2}]  |  <- AR Rollout
   |   ...                                                |
   |   Step k=H: 입력 = [ŷ_{t+H-1} ; known_future_{t+H}]|
   |                                                       |
   |  +---------------------------------------------+   |
   |  |  Masked Self-Attention (causal mask)         |   |  <- 미래 leak 방지
   |  +---------------------------------------------+   |
   |                       v Add & LayerNorm             |
   |  +---------------------------------------------+   |
   |  |  Cross-Attention with Encoder Memory          |   |  <- lookback 참조
   |  |  Q = Z_dec, K/V = K_enc, V_enc               |   |
   |  +---------------------------------------------+   |
   |                       v Add & LayerNorm             |
   |  +---------------------------------------------+   |
   |  |  FFN -> Linear -> [μ̂, σ̂] or Quantiles        |   |  <- 출력 헤드
   |  +---------------------------------------------+   |
   +-----------------------------------------------------+
                              |
                              v
        ŷ_{t+1}, ŷ_{t+2}, ..., ŷ_{t+H}    (point or probabilistic)
        또는 P10/P50/P90 quantile forecasts
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Input Embedding Layer** | 시계열 -> 벡터 변환 | Value Embedding(`Linear(d_input -> d_model)`) + Learned/Sinusoidal Positional Encoding + Temporal Feature Embedding(categorical: hour/dow/month, continuous: age, known_future: promotional flag 등). **RevIN**(Reversible Instance Normalization, Kim 2021)으로 instance-wise normalization -> 안정적 학습 -> 역정규화. |
| **Encoder (N-layer)** | Lookback의 글로벌 컨텍스트 추출 | Multi-Head Self-Attention(h=8, d_head=64)으로 모든 시점 쌍의 유사도 계산. Long-context 모델은 **Sparse Attention**(Informer, ProbSparse $O(L\log L)$), **LogSparse/Local-global**(LogTrans), **Patching**(PatchTST, patch=16 stride=8 -> $\frac{L}{16}$ 토큰) 등으로 O(L²) 완화. |
| **Decoder (M-layer)** | 미래 시점별 조건부 분포 생성 | ① Masked Self-Attention으로 AR 순서 보장(causal mask) ② Cross-Attention으로 encoder memory 참조 ③ Position-wise FFN. **AR rollout**: $k$-step 예측 $\hat{y}_{t+k}$를 다음 입력의 `decoder_input`으로 주입. |
| **Output Head** | 시계열 값으로 투영 | (a) **Point**: Linear(d_model -> 1), MSE/MAE 손실. (b) **Probabilistic**: 7개 quantile(Q10/Q50/Q90) -> Quantile/Pinball loss 또는 Negative Binomial/Student-t 파라미터 출력. (c) **Mixture**: Gaussian Mixture (MGM, Multi-output GP). |
| **AR Inference Loop** | H-step 멀티스텝 예측 | Teacher Forcing(학습 시 ground-truth 주입) ↔ Scheduled Sampling(점진적 자기예측 주입) ↔ Free-Running(추론 시 완전 AR). **Exposure Bias** 완화를 위해 DAgger/Professor Forcing 적용 가능. |

**핵심 수식**:
1. Self-Attention: $\mathrm{Attn}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V$
2. Quantile Loss: $L_\tau(y,\hat{y}) = \tau \max(y-\hat{y}, 0) + (1-\tau)\max(\hat{y}-y, 0)$
3. AR rollout: $\hat{y}_{t+k} = f_\theta(\hat{y}_{t+k-1}, \ldots, \hat{y}_{t+1}, y_{t-L+1:t}, \mathbf{x}^{\mathrm{known}}_{t+1:t+k})$
4. RevIN: $\hat{y}^{(k)} = \gamma^{(k)}\!\left(f_\theta\!\left(\frac{y - \mu}{\sigma}\right)\right)\sigma + \mu$,  $\mu,\sigma$는 lookback instance 통계

**설계 하이퍼파라미터 실무 가이드**:
- `d_model` ∈ {64, 128, 256, 512}, `n_heads` = 8, `d_ff` = 4×d_model, N=M=3~6
- `lookback` L: 도메인 주기의 4~8배 (일별->주간 seasonality 시 L≥28, 분 단위->일주기 시 L≥1440)
- `horizon` H: 의사결정 주기와 일치 (재고보충 7~14일, 전력 24시간, 금융 1~5 tick)
- Optimizer: AdamW(lr=1e-3 ~ 5e-4), Cosine schedule, warmup