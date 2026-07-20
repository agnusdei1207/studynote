---
title: "Synthetic Data Privacy Preserving Generation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 755
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VAE/GAN/Diffusion 계열 생성 모델이 학습한 통계적 결합 분포 $P_\theta(X)$ 에 DP-SGD(Differentially Private Stochastic Gradient Descent), PATE(Private Aggregation of Teachers Ensemble) 등 차등 프라이버시 메커니즘을 결합하여, 원본 레코드 $x_i$ 와 합성 레코드 $\tilde{x}$ 간 1:1 매핑이 수학적으로 불가능(near-zero reconstruction probability)하면서도 다운스트림 ML task의 utility 손실을 ε 이내로 억제하는 데이터 합성 패러다임이다.
> 2. **가치**: GDPR Art.4(5) 익명처리·Recital 26 완전 익명 요건, 한국 개인정보보호법 제3조 가명정보, NIST SP 800-188, EU AI Act 부속서 IV 훈련데이터 투명성 의무를 동시에 충족하며, 실측 데이터 공유·외부 반출 시 발생하는 마스킹·합의 절차 비용(업계 평균 40~60% 절감)과 cold-start 학습데이터 부족 문제를 동시 해결한다.
> 3. **판단 포인트**: (ε, δ) privacy budget ↔ downstream 모델 F1/AUC 손실의 trade-off, 생성 모델 family 선택(Tabular->CTGAN/TabDDPM, Image->DP-Diffusion, Text->DP-LLM), Membership Inference Attack(MIA)·Attribute Inference Attack(AIA) 저항성 정량 검증(MIA AUC ≤ 0.55 권고), 합성-실측 데이터 간 marginal/conditional distribution 거리(WD, KS-stat) 임계치 운영.

---

## Ⅰ. 개요 및 필요성

전통적 데이터 비식별화(De-identification)는 마스킹·가명처리·k-익명성·T-클로즈니스 등 **속성 단위 보호**에 집중했으나, 2013년 Sweeney의 NYC taxi 재식별 사건, 2017년 DNN 기반 model inversion attack, 2019년 Yeom의 Membership Inference Attack(MIA) 등장으로 "속성을 가려도 통계적 흔적으로 개인이 복원된다"는 한계가 학계·규제기관에서 공식 인정되었다. 특히 헬스케어(EMR·유전체), 금융(신용·거래), 공공(마이데이터) 영역은 학습·검증·오픈데이터 개방 시점에서 **원본의 결합 분포를 보존한 합성 데이터**가 유일한 해법으로 부상했다.

기존 접근법은 (1) 통계적 샘플링(여러분포 평활화 -> 차원 저주 발생), (2) Copula 기반 다변량 샘플링(연속 변수 위주), (3) IP-guard 기반 tokenization(유틸리티 손실 큼)의 한계가 있었고, 2018년 이후 DNN 생성 모델(GAN, VAE, Diffusion)에 차등 프라이버시를 결합한 **Privacy-Preserving Synthetic Data Generation(PPSDG)**이 새로운 표준으로 자리잡았다. 이는 ① 통계적 1순위 속성(1st-order marginal), ② 2순위·고차원 결합(2nd-order·joint), ③ 시계열 자기상관까지 보존하면서도 ④ DP 경계를 만족시키는 것이 핵심이다.

```text
 +----------------------------------------------------------------------+
 |        Real Data D = {x_i} (N records, d-dim)                        |
 |  +---------+ +---------+ +---------+ +---------+ +---------+         |
 |  | Patient | | Patient | | Patient | | Patient | | Patient | ...     |
 |  |  ID=001 | |  ID=002 | |  ID=003 | |  ID=004 | |  ID=005 |         |
 |  | age=42  | | age=35  | | age=58  | | age=29  | | age=67  |         |
 |  | dx=E11  | | dx=I10  | | dx=C50  | | dx=J45  | | dx=M17  |         |
 |  +----+----+ +----+----+ +----+----+ +----+----+ +----+----+         |
 |       |            |            |            |            |            |
 |       +------------+------------+------------+------------+            |
 |                                 v                                     |
 |            +----------------------------------+                       |
 |            |  Differential Privacy Layer     |  <- Privacy Accountant  |
 |            |  • per-sample grad clipping C   |     tracks (ε, δ)      |
 |            |  • Gaussian noise N(0, σ²I)     |     via RDP / zCDP     |
 |            |  • composition theorem          |     moments accountant  |
 |            +--------------+-------------------+                       |
 |                           v                                            |
 |            +----------------------------------+                       |
 |            |  Generative Model  G_θ           |                       |
 |            |  +----------+  +----------+     |   Statistics learned  |
 |            |  | Encoder  |-> | Decoder  |     |   P_θ(X) approximating  |
 |            |  | q(z|x)   |  | p(x|z)   |     |   true P(X)             |
 |            |  +----------+  +----------+     |                       |
 |            |  + Discriminator D_φ (GAN형)    |                       |
 |            |  + ε-DP noise injected to ∇L     |                       |
 |            +--------------+-------------------+                       |
 |                           v                                            |
 |  +--------------------------------------------------------------+    |
 |  |  Synthetic Data D' = {x̃_j} (M records, d-dim)               |    |
 |  |  x̃_1 = [age=43, dx=E11]   <- 원본과 다르지만 분포는 동일      |    |
 |  |  x̃_2 = [age=36, dx=I10]   <- MIA로 1:1 매핑 불가              |    |
 |  |  x̃_3 = [age=57, dx=C50]   <- Attribute Inference 저항        |    |
 |  |  ...                                                            |    |
 |  +--------------------------------------------------------------+    |
 |         |                                                              |
 |         v                                                              |
 |  Downstream Tasks: ML 학습 / 통계 분석 / 오픈데이터 개방 / 외부 반출   |
 +----------------------------------------------------------------------+
```

**왜 필요한가 (구 vs 신 패러다임)**:
- **구(Old)**: 원본 100만 건 -> k-익명성(quasi-identifier 마스킹) -> 80만 건 效用 -> 유출 시 재식별 위험 잔존
- **신(New)**: 원본 100만 건 -> DP(ε=1, δ=1e-5) 보장 생성 모델 -> 합성 100만 건 -> 다운스트림 모델 F1 손실 2~5% -> 재식별·MIA·AIA에 수학적 상한 제공

- **📢 섹션 요약 비유**: 기존 비식별화가 "주민등록번호를 ●●●으로 가리는" 얇은 필름이었다면, PPSDG는 "원본 환자 100만 명의 진단 패턴을 통계적으로 모방한 새로운 100만 명을 창조해내는" 완전한 복제-각본-재연출 행위와 같다. 각본(통계)은 본떴지만 배우(개인)는 모두 새로운 사람이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PPSDG의 핵심 아키텍처는 **(A) 생성 모델 패밀리 + (B) 차등 프라이버시 메커니즘 + (C) 프라이버시 회계사(Privacy Accountant) + (D) 유틸리티·프라이버시 평가 모듈** 4개 레이어로 구성된다.

```text
 +----------------------------------------------------------------------+
 |  Tier 1: Generative Model Family  (선택지가 도메인별로 분화)         |
 |                                                                      |
 |   Tabular          Time-Series         Image            Text         |
 |   +--------+      +--------+         +--------+       +--------+  |
 |   | CTGAN  |      | DGAN   |         | DP-    |       | DP-    |  |
 |   | TVAE   |      | TimeVAE|         | GAN    |       | GPT    |  |
 |   | TabDDPM|      | TimeGAN|         | DP-    |       | DP-    |  |
 |   |       |      |ForGAN  |         |Diffusion|       | LoRA   |  |
 |   +---+----+      +---+----+         +---+----+       +---+----+  |
 |       |               |                  |                |        |
 |       +---------------+------+-----------+----------------+        |
 |                              v                                       |
 |  Tier 2: DP Mechanism  (Gradient/Output-level noise injection)      |
 |  +-------------------------------------------------------------+    |
 |  | ① DP-SGD (Abadi et al., 2016)                              |    |
 |    - per-sample gradient clipping: ḡ_t(x_i) = g_t(x_i)/max(1, |    |
 |                            ||g_t(x_i)||_2 / C)                  |    |
 |    - Gaussian noise: g̃_t = (1/L) Σ ḡ_t(x_i) + N(0, σ²C²I)     |    |
 |    - Privacy amplification via Poisson sampling                  |    |
 |  | ② PATE (Papernot et al., 2017)                              |    |
 |    - n_teacher models -> vote -> Laplace/Gaussian noise -> student |    |
 |  | ③ Output Perturbation (sensitivity-bounded)                 |    |
 |  +------------------------+------------------------------------+    |
 |                           v                                          |
 |  Tier 3: Privacy Accountant  (총 (ε, δ) 누적 추적)                    |
 |  +-------------------------------------------------------------+    |
 |  |  Moments Accountant (Abadi) | RDP (Mironov) | zCDP (Bun)    |    |
 |  |  PRV Accountant | subsampled Gaussian Analytic              |    |
 |  |  -> 매 T step 마다 ε 누적, 종료 시점 (ε_T, δ) 보고           |    |
 |  +------------------------+------------------------------------+    |
 |                           v                                          |
 |  Tier 4: Evaluation & Release Gate                                    |
 |  +-------------------------------------------------------------+    |
 |  |  Utility:  F1/AUC gap ≤ 5%, WD/KS distance ≤ threshold     |    |
 |  |  Privacy:  MIA AUC ≤ 0.55, AIA precision ≤ 0.6             |    |
 |  |  Fidelity: column-wise TVD ≤ 0.1, pair-wise correlation ±5% |    |
 |  |  -> Gate 통과 시에만 D' release, 실패 시 ε 하향 or epochs ^  |    |
 |  +-------------------------------------------------------------+    |
 +----------------------------------------------------------------------+
```

### 핵심 알고리즘: DP-SGD 기반 생성 모델 학습 Pseudocode

```
Input: dataset D = {x_1, ..., x_N}, epochs T, lotto size L,
       clip C, noise multiplier σ, target (ε, δ)
Initialize: θ_0 (generator + discriminator)
for t = 1 to T do
    Sample mini-batch B_t via Poisson sampling with prob L/N
    For each x_i in B_t:
        Compute per-sample gradient g_t(x_i) = ∇L_θ(x_i)
        Clip: ḡ_t(x_i) = g_t(x_i) / max(1, ||g_t(x_i)||_2 / C)
    Aggregate: g̃_t = (1/L)[ Σ ḡ_t(x_i) + N(0, σ²C²I) ]
    Update: θ_t = θ_{t-1} - η_t · g̃_t
    Update privacy accountant: accumulate (ε_t, δ)
end for
Output: ε_T ≤ ε_target -> release G_θ
        else -> early stop or reduce σ
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **생성 모델 G_θ** | 실측 분포 $P(X)$ 를 모사하는 합성 데이터 생성 | Tabular: CTGAN(cGAN + mode-specific normalization), TabDDPM(forward/reverse Markov diffusion with Gaussian noise), TabSyn(VAE + diffusion hybrid); Time-series: TimeGAN(임베딩+RNN+GAN joint), Fourier-flow-based ForGAN; Image: DP-Diffusion(SDEdit, DPSGD with P3 splitter); Text: DP-LLM(Opacus+LoRA on GPT) |
| **차등 프라이버시 메커니즘** | 모델 출력·그래디언트에 캘리브레이션된 노이즈 주입 | DP-SGD(per-sample clip C=1.0, Gaussian σ=1.1 권고), PATE(teacher ensemble + confident-Gaussian aggregation, mode collapse 시 teacher vote 정밀도 < 0.5이면 라벨 폐기), 출력 섭동(output perturbation on trained model with sensitivity Δf·√(2ln(1.25/δ))/ε) |
| **프라이버시 회계사(Accountant)** | 누적 (ε, δ) 추적 및 정지 조건 | Moments Accountant(MA): $\alpha$-Rényi divergence 누적 -> tight bound, RDP(zCDP 포함): $(\alpha, \varepsilon(\alpha))$ 변환 -> (ε, δ) 변환, PRV Accountant: 가장 엄격, Subsampled Gaussian Analytic: subsampling amplification 정확 반영. T=100 epoch, L=512, N=100k, σ=1.1, δ=1e-5 시 ε≈1.0~2.0 |
| **유틸리티 평가기** | 다운스트림 ML 성능·분포 충실도 측정 | Train-on-Synthetic Test-on-Real(TSTR): XGBoost/LightGBM 학습 -> 원본 test F1/AUC 비교, marginal fidelity: column-wise TVD(Total Variation Distance) ≤ 0.1, pair-wise correlation: PCC(±5%), KS-stat(연속), χ²(범주) |
| **프라이버시 공격 평가기** | MIA/AIA/Singling-out 저항성 측정 | Membership Inference: shadow model 16~64개 학습 -> attack model AUC ≤ 0.55(Gaussian null 0.5), Attribute Inference: 합성 데이터에서 원본·합성 구분 정확도, Singling-out: 특정 합성 레코드와 매핑되는 원본 존재 확률 ≤ 1/N |
| **유틸리티-프라이버시 트레이드오프 컨트롤러** | ε 자동 튜닝 | ε sweep: {0.1, 0.5, 1.0, 3.0, 8.0} 별 utility gap 그래프, Pareto frontier 추