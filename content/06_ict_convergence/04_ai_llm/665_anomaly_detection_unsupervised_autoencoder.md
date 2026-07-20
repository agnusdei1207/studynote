---
title: "Anomaly Detection Unsupervised Autoencoder"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 665
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오토인코더(Autoencoder)는 입력 $x \in \mathbb{R}^n$를 인코더 $f_\theta: \mathcal{X} \rightarrow \mathcal{Z}$로 잠재 공간(Latent Space) $z \in \mathbb{R}^d (d \ll n)$에 투영한 뒤, 디코더 $g_\phi: \mathcal{Z} \rightarrow \mathcal{X}$로 재구성하는 대칭적 신경망이며, 이상 탐지에서는 **재구성 오차(Reconstruction Error)** $\mathcal{L}(x, \hat{x}) = \|x - g_\phi(f_\theta(x))\|^2$가 통계적 임계치를 초과하는 샘플을 이상치(Anomaly)로 판정한다.
> 2. **가치**: 라벨링 비용이 사실상 0이며(Zero-label), 정상 패턴의 분포를 잠재 공간에서 압축 표현하므로 **미지의 제로데이(Zero-day) 공격·신종 사기·예측 불가능한 제조 불량**까지 탐지 가능한 **일반화 성능**을 제공한다. 운영 환경 기준 Precision@K 0.85~0.95, FPR 1~5% 수준 달성 가능.
> 3. **판단 포인트**: (1) 잠재 차원 $d$와 Bottleneck 용량 설계, (2) 정상 데이터의 **순도(Purity) 보장**, (3) 재구성 오차 분포에 기반한 **동적 임계치 산정(Percentile / EVT / GMM)**, (4) Variational / Denoising / Sparse / LSTM-AE 등 **변형 모델의 선택**, (5) 개념 드리프트(Concept Drift) 대응을 위한 **재학습 주기 및 Window 전략**이 핵심 의사결정 요소다.

---

## Ⅰ. 개요 및 필요성

전통적인 이상 탐지는 **(1) 통계 기반**(Z-Score, Grubbs' Test, Mahalanobis Distance), **(2) 규칙 기반**(Snort, YARA Signature), **(3) 지도학습 분류기**(XGBoost, Random Forest)의 세 가지 축으로 진화해왔다. 그러나 ① 사이버 공격의 변종 증가(Signature DB 한계), ② 라벨링된 이상 데이터 확보의 구조적 불가능성(공격 빈도 < 0.01%), ③ 정상 패턴 자체가 시시각각 변화(Concept Drift)하는 운영 환경의 특성 때문에 **라벨 없이 정상 분포만 학습하여 이상을 추정하는 비지도(Unsupervised) 방식**이 산업 현장의 핵심 요구로 부상했다.

오토인코더는 1986년 Rumelhart가 역전파 학습과 함께 개념을 정립했고, 2006년 Hinton의 Deep Belief Net 사전학습을 거쳐, 2014년 이후 GPU 연산과 ReLU 활성화 함수의 보편화로 **고차원 비선형 데이터의 압축 표현 학습**이 실용화되었다. AIOps·제조·금융·보안 4대 분야에서 라벨 없는 스트리밍 데이터로부터 이상 패턴을 추론하는 **사실상 표준(De-facto Standard)** 모델로 자리잡았다.

```text
       [기존 이상 탐지 패러다임 비교]

  +--------------+    +--------------+    +--------------------+
  | 통계 기반     |    | 규칙/시그니처  |    | 지도학습 분류기     |
  | (1950s~)      |    | (1990s~)      |    | (2010s~)           |
  | • Z-Score     |    | • Snort Rule  |    | • XGBoost          |
  | • IQR / MAD   |    | • YARA        |    | • Random Forest    |
  | • ARIMA       |    | • AV Pattern  |    | • DNN Classifier   |
  +------+-------+    +------+-------+    +---------+----------+
         | 라벨 불필요         | 라벨 기반             | 라벨 필수
         | 선형 가정 한계       | 미지 공격 무력        | 클래스 불균형
         |                    |                      | 고비용
         v                    v                      v
   +----------------------------------------------------------+
   |          ✅ Unsupervised Deep Autoencoder (현재)          |
   |   • 정상 데이터만으로 학습                                  |
   |   • 비선형 고차원 패턴 학습                                  |
   |   • 미지/제로데이 탐지 가능                                  |
   |   • 정상 패턴 변화에 적응적                                  |
   +----------------------------------------------------------+
```

**왜 필요한가?**
- **라벨링 불가능 문제**: 금융 사기·제조 불량은 정상 샘플 대비 0.001~0.1% 수준, 라벨링 인건비 막대
- **고차원 비선형성**: 네트워크 트래픽 100+ features, 로그 시계열, 이미지 센서 데이터는 Mahalanobis 거리로 포착 불가
- **적대적 진화**: 공격자는 시그니처 DB를 회피하도록 변형, 통계 모델은 정상 범위 내 회피 공격(Slow-rate DoS)에 무력
- **운영 자동화**: MTTD(Mean Time To Detect) 단축 — 사람이 임계치 룰을 계속 갱신해야 하는 한계 해소

- **📢 섹션 요약 비유**: 기존 방식이 "도난 경보기(시그니처)·CCTV 동작 감지(통계)"이라면, 오토인코더는 "우리 집 평소 생활 패턴을 외운 집사가, 갑자기 낯선 사람이 들어오면 '어, 이거 아닌데?'라며 경고를 울리는 것"과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

오토인코더는 **인코더(Encoder) - 잠재 벡터(Latent Vector) - 디코더(Decoder)**의 3단 비대칭 미러 구조로, 목표는 입력을 재구성하는 것이며, 학습이 안정화되면 **정상 샘플은 재구성 오차가 낮고, 이상 샘플은 재구성 오차가 높다**는 귀무 가설에 기반한다.

```text
[오토인코더 이상 탐지 시스템 아키텍처 (전체 흐름)]

  +--------------+      +-------------------------------------+
  | 정상 데이터   | ----> |  Pre-processing Pipeline            |
  | (Train set)  |      |  • 결측치 처리 (MICE / KNN-Impute)   |
  | X_normal     |      |  • 정규화 (RobustScaler / MinMax)    |
  |              |      |  • 노이즈 제거 (Wavelet / Kalman)    |
  +------+-------+      |  • 차원 축소 사전 검토 (PCA)         |
         |              +-------------+-----------------------+
         v                            v
  +----------------------------------------------------------+
  |             🔧 Training Phase (정상 데이터만)              |
  |                                                          |
  |   X (n)  --► [Encoder f_θ] --► z (d) --► [Decoder g_φ] --► X̂ |
  |   128         Dense-ReLU         8         Dense-ReLU       |
  |   128         Dense-ReLU                  Dense-Sigmoid    |
  |   64          Dense-ReLU                                   |
  |                                                          |
  |   Loss = (1/N) Σ ‖x_i − x̂_i‖²  +  β·KL(q(z|x)‖p(z))    |
  +----------------------+-----------------------------------+
                         v
              +---------------------+
              | 모델 가중치 저장 θ*,φ*|
              | + 임계치 τ 산정       | <--- 정상 데이터의 재구성
              |   τ = μ + k·σ       |     오차 분포에서 결정
              |   τ = 99th %ile     |
              +----------+----------+
                         v
  +--------------+      +-------------------------------------+
  |  추론 데이터  | ----> |  Inference Phase (실시간)            |
  |  X_infer     |      |                                     |
  |  (Stream)    |      |   s(x) = ‖x − g_φ(f_θ(x))‖²        |
  +--------------+      |      +-- s > τ ---> 🚨 Anomaly Alert |
                        |      +-- s ≤ τ ---> ✅ Normal        |
                        +-------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Encoder $f_\theta$** | 입력 $x$를 저차원 잠재 벡터 $z$로 매핑 (차원 축소 + 특징 추출) | MLP(CNN / LSTM / Transformer 변형 가능). `Dense(128)->ReLU->BatchNorm->Dropout(0.2)->Dense(64)->ReLU->Dense(d)` 구조. 정보 병목(Bottleneck) 효과로 핵심 패턴만 보존. |
| **Latent Space $\mathcal{Z}$** | 정상 데이터의 매니폴드를 표현하는 압축 공간 | $d = 8 \sim 32$ (입력 차원 $n$ 대비 $d/n \le 0.1$). 너무 크면 Identity Function이 되어 이상치도 재구성 -> Bottleneck Capacity Trade-off 발생. |
| **Decoder $g_\phi$** | 잠재 벡터 $z$를 원본 공간으로 복원 (생성기) | Encoder와 대칭 구조. 마지막 층 활성함수는 데이터 특성에 따라 `Sigmoid`(정규화 0~1) / `Linear`(로그/시계열) / `Tanh`(중심화 데이터). |
| **Loss & Score** | 재구성 품질 측정 및 이상 점수 산출 | 기본 MSE: $\mathcal{L} = \frac{1}{n}\sum(x_i - \hat{x}_i)^2$. 이상 탐지 점수 $s(x) = \|x - \hat{x}\|_2^2$ 또는 MAE / Cosine Distance. 임계치 $\tau$는 정상 데이터의 $s$ 분포에서 결정. |
| **Threshold Module** | 정상/이상 경계 결정 | 정적 임계치(99th Percentile), 동적 임계치(EVT-GPD: $\bar{F}(s) = (1 + \xi\frac{s-\mu}{\sigma})^{-1/\xi}$), GMM/Mixture 기반 소프트 경계, AUC-Youden J 인덱스 최적화. |
| **Drift Handler** | 개념 드리프트 감지 및 재학습 | ADWIN(Adaptive Windowing), Page-Hinkley Test로 $s$의 평균/분산 변화 감지 -> Trigger Retraining with Rolling Window (예: 7일). |

### 핵심 수식 및 알고리즘

**① 재구성 오차 (Reconstruction Error)**
$$\mathcal{L}_{\text{rec}}(x, \hat{x}) = \frac{1}{n}\sum_{i=1}^{n}(x_i - \hat{x}_i)^2$$

**② 손실 함수 (MSE + Regularization)**
$$\mathcal{L}_{\text{total}} = \underbrace{\frac{1}{N}\sum_{i=1}^{N}\|x_i - g_\phi(f_\theta(x_i))\|^2}_{\text{Reconstruction}} + \underbrace{\lambda \cdot \Omega(\theta, \phi)}_{\text{L2/Sparse/KL}}$$

**③ Variational Autoencoder (VAE) — 불확실성 정량화**
$$\mathcal{L}_{\text{VAE}} = -\mathbb{E}_{q_\phi(z|x)}[\log p_\theta(x|z)] + D_{\text{KL}}(q_\phi(z|x)\|p(z))$$
- 재구성 항 $-\mathbb{E}[\log p_\theta(x|z)]$ (복원 충실도)
- 정규화 항 $D_{\text{KL}}$ (잠재 분포를 $\mathcal{N}(0,I)$에 가깝게)

**④ Anomaly Score with EVT (Extreme Value Theory)**
$$\tau = F^{-1}(1-\epsilon) \quad \text{where } \epsilon = 0.01 \text{ (1% FPR)}$$
- 정상 데이터의 $s$ 분포에 GPD(Generalized Pareto Distribution) 피팅 -> 꼬리 부분 임계치 산정

**⑤ Sparse Autoencoder 제약 (희소성)**
$$\mathcal{L}_{\text{sparse}} = \mathcal{L}_{\text{rec}} + \beta \sum_{j=1}^{d} \text{KL}(\rho \| \hat{\rho}_j)$$
- $\rho = 0.05$ 목표 활성 비율, $\hat{\rho}_j$ 실제 활성 비율 -> 잠재 벡터가 희소해져 구분력^

### 변형 모델 비교 (Model Variants)

| 변형 모델 | 핵심 아이디어 | 적용 시나리오 | 한계 |
| :--- | :--- | :--- | :--- |
| **Vanilla AE** | 단순 대칭 MLP 구조 | 정형 tabular 데이터 베이스라인 | 고차원 이미지/시계열 표현력 부족 |
| **Denoising AE** | 입력에 노이즈 $\tilde{x} = x + \epsilon$ 추가 후 원본 $x$ 복원 | 잡음 많은 센서/로그 데이터 | 노이즈 비율 $\nu$ 튜닝 필요 |
| **Sparse AE** | 잠재 노드 활성에 희소성 제약 | 고차원 희소 feature (텍스트 TF-IDF) | $\beta$ 하이퍼파라미터 민감 |
| **Contractive AE** | Jacobian $\|J_f(x)\|^2$ 최소화 (국소 수축) | 매니폴드 학습·이상 탐지 | 학습 안정성 떨어짐 |
| **Variational AE** | 잠재 분포를 $\mathcal{N}(\mu, \sigma^2)$로 모델링, 샘플링 가능 | 이상 점수에 불확실성 결합 | 블러링된 재구성 -> 점수 분산 큼 |
| **Conv-AE** | Conv2D + MaxPool 인코더, Conv2DTranspose 디코더 | 이미지 결함·의료 영상·CCTV 프레임 | 평행이동/회전 불변성 부족 |
| **LSTM-AE / TCN-AE** | 시계열 순차 패턴 모델링, $h_t$ 잠재 압축 | 트래픽·로그·금융 시계열 | 장기 의존성 1000+ 스텝 한계 |
| **Transformer-AE** | Self-Attention으로 장거리 의존성 | 멀티모달 로그·대용량 IoT | 연산량 $O(n^2)$ 메모리 이슈 |
| **Graph-AE (GNN)** | 노드 임베딩 $z_v$ 재구성, 엣지 복원 | 네트워크 침입·사기 거래 그래프 | 스케일 수십만 노드 이상 어려움 |

- **📢 섹션 요약 비유**: 오토인코더는 "**압축 전문가(인코더)가 창고에 짐을 효율적으로 분류해 넣고, 풀어주는 전문가(디코더)가 꺼내 놓는 시스템**"인데, 평소 짐(정상 데이터)은 정확히 꺼내지만, 처음 보는 낯선 짐(이상 데이터)은 위치도 모르고, 꺼내도 엉뚱한 게 나오는 원리와 같다.

---

## Ⅲ. 비교 및 연결

### 이상 탐지 모델 패밀리 비교

| 구분 | **Autoencoder (AE)** | **Variational AE (VAE)** | **Isolation Forest** | **One-Class SVM** | **GAN-based (AnoGAN)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **학습 방식** | 비지도 (정상만) | 비지도 (정상만) | 비