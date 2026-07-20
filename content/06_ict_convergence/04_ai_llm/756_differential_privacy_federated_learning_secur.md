---
title: "Differential Privacy Federated Learning Security"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 756
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 차등 프라이버시 연합 학습(DP-FL)은 **McMahan의 FedAvg 알고리즘** 위에서 **Dwork의 (ε, δ)-차등 프라이버시 정의**를 **클라이언트 수준(user-level)**으로 적용하여, **민감도 Δf 기반 가중치(w·∇L) L2-노름 클리핑(임계치 S)** 후 **가우시안/Gauss 메커니즘 노이즈 N(0, σ²S²I)**을 그래디언트 집계 단계에 주입하는 **DP-SGD-FedAvg(McMahan, Ramage, Talwar, Zhang 2018)** 구조이다. 노이즈 스케일 σ ≥ c·S·q·√(T·log(1/δ))/ε로 바운드되며, 이때 q는 샘플링 확률, T는 통신 라운드 수이다.
> 2. **가치**: Apple이 iOS 13부터 로컬 DP(LDP)로 사용, Google이 Gboard에서 Gboard-federated RNN으로 적용한 사례에서, **단일 사용자 데이터가 유출되지 않으면서도 글로벌 모델 정확도를 baseline 대비 95% 수준으로 유지**할 수 있음을 입증했다. **세컨드-오더 모멘트 어카운트(Moments Accountant)**를 사용 시 naive composition 대비 100~1000× 더 큰 ε 허용 -> 동일 프라이버시 예산에서 utility 손실 최소화 가능.
> 3. **판단 포인트**: 핵심 trade-off는 **(ε, δ, σ) 프라이버시 예산 ↔ 모델 수렴 속도/정확도**, **Local-DP vs Central-DP vs Distributed-DP**의 위협 모델 차이, **Gradient Inversion Attack(Geiping et al. 2020, Zhu et al. DLG 2019)** 대응을 위한 **Secure Aggregation(Bonawitz 2017, Shamir 3PC) + HE(Homomorphic Encryption) + TEE(Intel SGX)** 다층 방어 선택, 그리고 **Non-IID 데이터(클라이언트별 클래스 편향)** 하에서 DP 노이즈가 야기하는 **클라이언트 드리프트(client drift) 가속화** 문제다.

---

## Ⅰ. 개요 및 필요성

**연합 학습(Federated Learning, FL)**은 2016년 Google의 H. B. McMahan et al.이 "Communication-Efficient Learning of Deep Networks from Decentralized Data"에서 FedAvg를 제안한 이래, 데이터 비저장(stateless) 환경에서 분산 모델 학습의 표준 패러다임으로 자리잡았다. 하지만 **FL은 원시 데이터를 공유하지 않더라도 기울기(gradient) 그 자체가 PII(Personally Identifiable Information)를 누설**할 수 있다는 것이 Zhu et al.(Deep Leakage from Gradients, NeurIPS 2019) 및 Geiping et al.(Inverting Gradients, CVPR 2020)에 의해 입증되면서, **"gradient는 raw data의 linear projection이며, 단 한 번의 SGD step만으로도 batch 내 첫 번째 샘플의 픽셀 단위 복원이 가능하다"**는 충격적 사실이 밝혀졌다. 또한 Nasr et al.(Membership Inference Attacks, 2019), Melis et al.(Property Inference, USENIX 2019) 등 다양한 부채널 공격이 보고됨에 따라, **암호학적 보호(Secure Aggregation, HE)**만으로는 도청자(eavesdropper) 모델 및 **악의적 서버(semi-honest but curious server)** 모델에서 **후속 모델 인퍼런스 공격을 차단할 수 없음**이 명확해졌다.

이에 **Dwork & Roth(2014, "The Algorithmic Foundations of Differential Privacy")**의 차등 프라이버시(DP)를 FL에 결합하여 **수학적·정보이론적으로 정량화된 프라이버시 보장**을 제공하려는 시도가 급부상했다. DP는 **임의의 인접 데이터셋 D, D'(|D Δ D'| ≤ 1)**에 대해 알고리즘 M의 출력이 **exp(ε) + δ 배 이상** 차이 나지 않도록 함으로써, **재귀적·조합적 누설 누적 문제를 우아하게 해결**한다. 즉, 공격자가 무한한 부채널 지식을 갖더라도 **단일 클라이언트 데이터의 기여도가 ε-budget으로 캡(Clamp)된 후 누적**되므로, **전체 학습 라이프사이클 동안**의 프라이버시가 보장된다.

**기존 중앙집중식 ML -> 연합학습(FL) -> 차등 프라이버시 연합학습(DP-FL)**로의 진화는 **"데이터를 옮기지 않음 -> 데이터의 흔적(기울기)도 누설하지 않음"**으로의 신뢰 경계(trust boundary)의 점진적 이동을 의미한다. Apple과 Google이 2024년 기준 production LLM fine-tuning에 DP-FL을 도입한 것은, GDPR Art. 32 "appropriate technical measures" 및 한국 개인정보보호법 가명정보 처리 요건(제23조의2)을 기술적으로 충족하는 사실상 유일한 검증된 프레임워크이기 때문이다.

```text
[전통적 ML: 데이터 수집의 중앙화]
                     +--------------------------+
                     |   사용자 N개의 원시 데이터  |
                     |   (이미지/텍스트/클릭 로그)  |
                     +------------+-------------+
                                  | ① Raw data 이동
                                  v
   +------------------------------------------------------+
   |   클라우드 데이터센터 (단일 TCB, 고위험)                |
   |   - 외부 해킹 시 전체 DB 유출                          |
   |   - 내부 관리자 악용 가능                              |
   |   - 컴플라이언스: GDPR, APPI, PIPC 고비용               |
   +------------------------------------------------------+

[연합학습(FL): 모델은 이동, 데이터는 잔존]
   Client₁ -+                       +- Server(평균)
   Client₂ -+  ② Δw (gradient)      |
   Client₃ -+  ③ 모델 가중치          |
     ...   -+      ^ |               |
                    | +----- 집계(∑Δw/N) ---+
                    v
              ⚠️ 기울기로부터 raw data 복원 가능 (DLG/iDLG 2019-2020)
              ⚠️ 멤버십 인퍼런스 / 속성 인퍼런스 가능

[차등 프라이버시 연합학습(DP-FL): 노이즈 주입으로 수학적 보장]
   Client₁ -+
   Client₂ -+  ② Local SGD (full-batch 또는 mini-batch)
   Client₃ -+     +- Δw 클리핑: ‖Δw‖₂ ≤ S
     ...   -+     +- 가우시안 노이즈: 𝒩(0, σ²S²I/q²)
            |              v
            +----►  ③ Noisy gradient 송신 ---►  ④ Secure Aggregation
                                                       |
                                                       v
                                              ⑤ 프라이버시 예산 ε 누적 (Moments Accountant)
                                                       |
                                                       v
                                              ⑥ Global model: w <- w - η·(1/N)∑Δw̃
```

- **📢 섹션 요약 비유**: FL이 **"각 가게의 레시피만 본부에 보내고, 원재료는 가게에 두는 것"**이라면, DP-FL은 **"각 가게가 보낼 때 레시피에 일부러 약간의 자잘한 실수를 섞어 보내, 외부인이 어떤 가게의 원재료 비율을 정확히 역추적할 수 없게 만드는 것"**이다. 여기서 "실수의 양(노이즈 σ)"이 클수록 프라이버시는 강해지지만, 본부가 모은 레시피의 정확성(모델 정확도)은 떨어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

DP-FL의 **엔드-투-엔드 파이프라인**은 크게 **(1) 로컬 학습 -> (2) 클리핑 -> (3) 노이즈 주입 -> (4) 암호학적 집계 -> (5) 프라이버시 예산 누적 -> (6) 글로벌 업데이트**의 6단계로 구성된다. 각 단계는 모두 **수학적·프로토콜적 보장**을 제공해야 한다.

**1단계: 로컬 모델 학습(Per-Client SGD).** 각 클라이언트 k는 글로벌 모델 w_t를 다운로드한 뒤, 자신의 로컬 데이터 D_k에 대해 E(epoch) 횟수만큼 미니배치 SGD를 수행한다. 손실함수 ℓ(w; x, y)에 대해 누적 기울기 g_k = ∇ℓ_k(w_t; b)를 산출한다.

**2단계: 기울기 클리핑(Gradient Clipping).** L2 노름 기반 클리퍼를 적용: g_k <- g_k · min(1, S/‖g_k‖₂). 여기서 **민감도(sensitivity) S = Δ₂f = sup_{D∼D'} ‖g(D) - g(D')‖₂** 이다. McMahan et al.(2018)은 clip threshold S를 **C4->S**, **𝔸bdaUserLevelDP** 명명법으로 확립했다.

**3단계: 가우시안 노이즈 주입(Gaussian Mechanism).** 노이즈가 추가된 기울기: g̃_k = g_k + 𝒩(0, σ²S²I/q²). zCDP(Bun & Steinke 2016) 또는 **Moments Accountant(Abadi et al. 2016)**를 사용해 (ε, δ)-DP 보장을 산출한다. **노이즈 스케일 공식**: σ = c·S·q·√(T·log(1/δ))/ε (c는 상수, T는 라운드 수). 즉, **ε이 작을수록(강한 프라이버시) σ가 커져서(큰 노이즈) 정확도가 떨어진다**.

**4단계: 보안 집계(Secure Aggregation).** Bonawitz et al.(CCS 2017)의 프로토콜을 사용하면, **서버가 개별 클라이언트 기울기 g̃_k를 일절 보지 못한 채, 합산값 ∑g̃_k만 복원**할 수 있다. 이는 **Shamir 비밀 공유(비밀이 t-1차 다항식에 분산 저장, t-out-of-n 복원)** + **Diffie-Hellman 키 합의** + **이중 마스크(mask) 구조**로 구현된다. 결과적으로 **노이즈의 분산이 √N배 감소**되어 정확도 회복에 결정적 역할을 한다.

**5단계: 프라이버시 예산 누적(Privacy Budget Composition).** T 라운드 후 총 누적 ε_total은 **RDP(Rényi Differential Privacy, Mironov 2017)**를 사용해 산출: D_α(ℳ || σ) = α/(2σ²). **적응적 σ 스케줄링** (e.g., decreasing σ over rounds) 시 **tight composition**이 가능.

**6단계: 글로벌 모델 업데이트.** 중앙 서버는 FedAvg 규칙으로 w_{t+1} <- w_t - η·(∑g̃_k / N)을 적용한다.

```text
[DP-FL 라운드 t의 상세 데이터 흐름]
                       +-------------------------------------+
                       |   Central Server / Aggregator        |
                       |   w_t (global model, public)         |
                       +----------------+--------------------+
                                        | ① Broadcast w_t (TLS 1.3)
        +-------------------+-----------+--------+------------------+
        v                   v                    v                  v
   +---------+         +---------+          +---------+         +---------+
   |Client k₁|         |Client k₂|          |Client k₃|   ...   |Client kₙ|
   | D_k₁    |         | D_k₂    |          | D_k₃    |         | D_kₙ    |
   +----+----+         +----+----+          +----+----+         +----+----+
        |                   |                    |                   |
        | ② Local SGD      |                    |                   |
        |   g_k <- ∇ℓ_k(w_t)|                    |                   |
        |                   |                    |                   |
        | ③ Clipping       |                    |                   |
        |   ĝ_k <- g_k·min(1, S/‖g_k‖₂)          |                   |
        |                   |                    |                   |
        | ④ Noise          |                    |                   |
        |   g̃_k <- ĝ_k + 𝒩(0, σ²S²I)            |                   |
        |                   |                    |                   |
        +---------+---------+----------+---------+---------+---------+
                  |                    |                   |
                  | ⑤ Secure Aggregation (Shamir 3PC)       |
                  v                    v                   v
        +--------------------------------------------------------+
        |  서버 관점: 개별 g̃_k 를 알 수 없음, ∑g̃_k 만 복원 가능    |
        |  정확도 보너스: 노이즈 분산이 1/N 으로 감소              |
        +--------------------------------+-----------------------+
                                         | ⑥ w_{t+1} <- w_t - η·(∑g̃_k / N)
                                         v
                       +-------------------------------------+
                       |  ⑦ Moments Accountant:               |
                       |     ε_t = T·ε_per_round (tight)     |
                       |  총 ε ≤ (ε_target, δ_target) 인지 검증 |
                       +-------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **클라이언트 (Edge Device)** | 로컬 모델 학습, 기울기 계산, 클리핑·노이즈 주입 | PyTorch/TensorFlow on-device, DP-SGD-FedAvg 변형, **Abadi-style moments accountant**(Abadi et al. CCS 2016) |
| **중앙 서버 (Aggregator)** | 암호학적 집계, 글로벌 모델 분배 | **Bonawitz Secure Aggregation (CCS 2017)**, TLS 1.3, 옵션적 Trusted Execution Environment(Intel SGX/TDX) |
| **프라이버시 예산 관리자 (Privacy Accountant)** | ε, δ 누적 추적, 라운드당 ε_per-round 산출 | **Moments Accountant (T=1000, δ=10⁻⁵ -> ε≈2.0)**, **RDP (Rényi DP, Mironov 2017)**, **PRV Accountant (Gopi-Lee-Wutschitz 2021,