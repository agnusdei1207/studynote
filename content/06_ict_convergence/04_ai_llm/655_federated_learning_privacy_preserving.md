---
title: "Federated Learning Privacy Preserving"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 655
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 연합 학습(Federated Learning, FL)은 로컬 데이터가 클라이언트 디바이스를 떠나지 않은 채 모델 그래디언트(gradient)·로컬 파라미터만 공유하여 협업 학습을 수행하는 분산 학습 패러다임이며, 여기에 차등 프라이버시(Differential Privacy, DP), 보안 집계(Secure Aggregation, SecAgg), 동형 암호(Homomorphic Encryption, HE), 신뢰 실행 환경(Trusted Execution Environment, TEE)을 결합해 모델 자체로부터 원본 데이터를 역추론하려는 공격(모델 반전·멤버십 추론)을 수학적으로 차단하는 것이 프라이버시 보존 연합 학습의 본질이다.
> 2. **가치**: 클라이언트 단의 학습 정확도 손실을 1~3% 이내로 유지하면서 ε-DP(ε ≤ 8) 수준의 정량적 프라이버시 예산을 보장하고, GDPR·PIPC(개인정보보호법)·HIPAA의 데이터 최소 수집 원칙과 가명처리 의무를 기술적으로 충족하며, 중앙 서버 공격 시 피해 반경을 "단일 모델"이 아닌 "노이즈가 첨가된 파라미터 집합"으로 한정해 데이터 브로커·내부자 위협(insider threat)에 대한 컴플라이언스 비용을 60% 이상 절감한다.
> 3. **판단 포인트**: (a) IID(독립 동일 분포) 가정이 깨지는 Non-IID 환경에서의 수렴성–공정성–프라이버시 트레이드오프, (b) DP 노이즈 추가에 따른 모델 정확도 손실과 클라이언트 라운드 수의 함수 관계, (c) SecAgg/HE 적용 시 통신 오버헤드(SecAgg 2~3배, HE 10~100배)와 양자내성암호(PQC)로의 전환 시점, (d) 크로스실(cross-silo, 2~100 기관) vs 크로스디바이스(cross-device, 1억+ 모바일) 시나리오의 아키텍처 선택, (e) 신뢰 경계(trust boundary)를 어디에 그을 것인가(TEE vs MPC vs HE) — 이 다섯 가지가 학습 정리에서 반드시 명시되어야 할 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 중앙 집중형 머신러닝(Centralized ML)은 "데이터가 왕(data is the new oil)"이라는 명제 하에, 다수의 클라이언트·기관·디바이스로부터 원본 데이터를 수집하여 단일 데이터센터에 적재하고, 그곳에서 모델을 학습시키는 파이프라인을 채택해왔다. 그러나 2018년 GDPR(일반데이터보호규정) 시행, 2020년 미국 CCPA, 2023년 한국 개인정보보호법 개정(가명정보 도입), 2024년 EU AI Act 발효로 인해 의료·금융·제조 분야의 민감 데이터(PII, PHI, PFI)는 **법적으로 클라이언트 외부 반출이 금지**되는 영역이 확대되었다. 동시에, Google Gboard(2017, FedAvg 최초 적용), Apple QuickType·Siri(2019, DP-FedAvg), NVIDIA Clara FL(의료 영상, 2020), WeBank FATE(금융 크로스실, 2019) 등 산업계 적용 사례가 누적되면서 "데이터를 움직이지 않고 모델을 움직이는(Data stays put, models move)" 패러다임이 실증되었다.

그러나 연합 학습이 본질적으로 제공하는 것은 **입력 데이터 비공개(input privacy)**일 뿐, **출력 모델의 프라이버시(output privacy)**는 자동 보장되지 않는다. Frederikson et al.(2015)의 **모델 반전 공격(Model Inversion Attack)**, Shokri et al.(2017)의 **멤버십 추론 공격(Membership Inference Attack, MIA)**, Melis et al.(2019)의 **속성 추론 공격(Property Inference)**은 공유된 그래디언트만으로도 학습 데이터의 속성·개별 샘플의 포함 여부·심지어 원본 이미지(얼굴 복원)를 복원할 수 있음을 보였다. 따라서 **프라이버시 보존 연합 학습(PPFL, Privacy-Preserving Federated Learning)**은 선택이 아닌, 법적·기술적 필수 요건이 되었다.

```text
+------------------------------------------------------------------+
|   중앙 집중형 ML vs 연합 학습(FL) vs 프라이버시 보존 FL(PPFL)    |
+------------------------------------------------------------------+

  [전통적 중앙 집중형]              [단순 연합 학습(FL)]            [프라이버시 보존 FL(PPFL)]
  +----------+                    +----------+                  +------------------+
  | Client A |---원본 데이터----->|           |                  | Client A(노이즈+암호)|
  +----------+   ^               | Aggregator|                  +--------+---------+
  +----------+   |  원본 데이터   |  (서버)   |     그래디언트        |
  | Client B |---+--------------->|           |<----노이즈 없음-----+ Client B(노이즈+암호)|
  +----------+   |               +----------+                  +--------+---------+
  +----------+   |                                                |
  | Client C |---+                                                |
  +----------+                                                    |
       v                                  v                       v
  +----------+                        +----------+            +--------------+
  |데이터센터|                        | 단일 모델 |            | DP+SecAgg+HE  |
  |   단일   |                        |  노출 시  |            | 적용 차등     |
  | 데이터셋 |                        | 그래디언트|            | 보호 모델     |
  +----------+                        | 로 복원   |            +--------------+
       |                                  |                          |
   <----------------->                  <----------------->         <----------------->
   원본 데이터 직접 반출        입력 비공개, 출력 노출         입력·출력·계산 모두 보호
   GDPR 위반 / 침해 시 대규모     MIA, Model Inversion         GDPR·HIPAA·AI Act 준수
   침해 피해                       가능                         양자내성 대응 가능
```

**왜 필요한가?** 첫째, **규제 준수(Regulatory Compliance)** — GDPR 제25조(데이터 보호 기본 설계), PIPC 제29조(안전조치의무) 준수. 둘째, **데이터 주권(Data Sovereignty)** — EU 데이터가 EU 외부로 이동하지 않으면서도 글로벌 모델 학습에 참여. 셋째, **데이터 사일로(Data Silo) 해소** — 병원·은행·공장 간 데이터 공유 불가 문제를 "가치 추출"로 우회. 넷째, **공격 표면(Attack Surface) 축소** — 중앙 데이터베이스 단일 실패점(SPOF) 제거. 다섯째, **엣지-클라우드 협업** — IoT·자율주행·모바일의 1.4조 대 디바이스에서 생성되는 에지 데이터의 즉시 학습.

- **📢 섹션 요약 비유**: 중앙집중형 ML이 "학생들을 한 교실에 모아 비밀일기를 공개적으로 읽게 하는 것"이라면, 단순 FL은 "일기를 봉투에 넣어 제출"하는 것이고, PPFL은 "봉투 안의 글자를 일부분 지워(노이즈) 여러 봉투를 함께 섞어(보안 집계) 우체국 직원이 봉투 안을 볼 수 없게(암호화) 제출하는 것"입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

프라이버시 보존 연합 학습의 4계층 아키텍처는 **① 클라이언트(데이터 보유자) ② 집계자(Aggregator/Coordinator) ③ 프라이버시 메커니즘 계층(DP/SecAgg/HE/TEE) ④ 글로벌 모델 저장소**로 구성된다. 핵심 알고리즘은 Google의 **FedAvg(McMahan et al., 2017)**를 기저로, **DP-SGD(Abadi et al., 2016)**, **SecAgg(Bonawitz et al., 2017)**, **FedProx(Li et al., 2018, Non-IID 대응)**, **FedNova(Wang et al., 2020, 이질적 로컬 epoch 보정)**, **SCAFFOLD(Karimireddy et al., 2020, 제어 변량)** 등이 있다.

```text
+----------------------------------------------------------------------+
|            PPFL 라운드 프로토콜 (Round t, Secure Aggregation 기반)   |
+----------------------------------------------------------------------+

  Coordinator/Server                  Client k (k=1..K)              Privacy Layer
  ------------------                  ----------------               -------------
  [1] 글로벌 모델 w_t 브로드캐스트
        |  w_t  +  공개 키(HE/TEE)                                    <------ TEE/HE
        |                                                               Enclave
        v                                                               (Intel SGX)
  [2]                                              w_t 수신, 로컬 초기화
                                                  로컬 데이터 D_k (비공개)
        |
        |                                       [3] for epoch=1..E:
                                                  θ = w_t
                                                  g_k = ∇L(θ; B)            <------ DP-SGD
                                                  g_k <- clip(‖g_k‖≤C)        (Gradient Clipping)
                                                  g_k <- g_k + N(0, σ²C²I)    (Gaussian Noise)
        |
  [4]        ^------------------- 암호화된 g_k 송신 -------------------|
            |   +-----------------------------------------+
            |   | SecAgg 프로토콜 (Bonawitz 2017)         |
            |   |  - Pairwise Mask 생성 (Shamir 3-of-K)   |
            |   |  - Dropout-tolerance: k-2 생존 보장    |
            |   |  - 4-round handshake:                   |
            |   |      R1: 공유 키 합의                   |
            |   |      R2: 마스크 배포                    |
            |   |      R3: 암호문 업로드                  |
            |   |      R4: 집계값 복호화                  |
            |   +-----------------------------------------+
  [5] w_{t+1} = w_t - η·(1/K)Σg_k     <-- HE 동형 집계 (CKKS/BFV)
        |     (노이즈가 합산되어 분산은 σ²/K 로 축소 -> Central Limit)
        |
  [6] w_{t+1} 재브로드캐스트
        v
  [반복: T rounds, 수렴까지]
        |
        v
  [7] 감사 로그: ε 누적 예산, 라운드 수, 클라이언트 참여율
        |
        v
  [8] MIA 방어 검증: Shadow Model 기반 공격 성공률 < 60%
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **클라이언트(Participant/Worker)** | 로컬 데이터 보유, 로컬 학습, 그래디언트 업로드 | FedAvg/FedProx 실행, DP-SGD 적용 시 (a) **Gradient Clipping**: `g <- g·min(1, C/‖g‖)` 로 샘플별 영향력 상한 (b) **Gaussian Mechanism**: `g̃ = g + N(0, σ²I)` (c) **Local DP / User-level DP** 선택 (d) Secure RNG 기반 마스크 생성 |
| **Aggregator(FL Server)** | 글로벌 모델 집계, 라운드 조율, 클라이언트 샘플링 | (a) **FedAvg**: `w <- Σ(n_k/n)·w_k` (b) **FedProx**: 근사항 `(μ/2)‖w−w_t‖²` 추가해 이질적 클라이언트 수렴 보장 (c) **FedNova**: `w <- w_t − τ_k·(1/Στ_k)Σg_k` (d) 클라이언트 신뢰 점수, Krum/Multi-Krum으로 Byzantine 공격 방어 |
| **프라이버시 메커니즘 계층** | DP·SecAgg·HE·TEE의 조합 | (a) **DP**: Moments Accountant(RDP 기반, Abadi 2016)로 (ε, δ) 누적 예산 추적 (b) **SecAgg**: Shamir 비밀분할(2-of-K 또는 3-of-K) + Pairwise Mask, 클라이언트 dropout 33% 허용 (c) **HE**: CKKS(부동소수점, ML 친화), BFV/BGV(정수), TFHE(부트스트랩) (d) **TEE**: Intel SGX/TDX, ARM TrustZone, AMD SEV-SNP에서 Enclave 내부 평문 처리 |
| **감사·컴플라이언스(Governance)** | 프라이버시 예산 소진 추적, 라운드 메타데이터 기록 | (a) **RDP Composition Theorem**: (ε, δ)-DP 합성 시 sub-additive (b) **Federated Audit Log**: (timestamp, client_id_hash, ε_spent, noise_scale) (c) **Model Card + Datasheet for Datasets** (Gebru 2021) (d) GDPR DPO 보고용 KPI |

**핵심 수학적 보장**:

1. **차등 프라이버시(Differential Privacy)**: 인접 데이터셋 D, D′ (한 샘플 차이)에 대해 알고리즘 M이 `(∀S) Pr[M(D)∈S] ≤ e^ε·Pr[M(D′)∈S] + δ`를 만족하면 M은 (ε, δ)-DP. ε이 작을수록(통상 0.1~8) 프라이버시 강도^, 노이즈^, 정확도v. **민감도(Sensitivity, Δf) = max‖f(D)−f(D′)‖₁ = C**(클리핑 노름).

2. **보안 집계(Secure Aggregation)의 보안성**: TTP 없는 2-round handshake에서 K−f명의 클라이언트 dropout 시에도 정확한 합집계 복원, 시뮬레이터 기반 UC-security 증명. **통신 복잡도 O(K²)**, **계산 복잡도 O(K)**.

3. **동형 암호(Homomorphic Encryption)**: `Enc(m₁) ⊕ Enc(m₂) = Enc(m₁+m₂)`, `Enc(m₁) ⊗ c = Enc(c·m₁)`. CKKS 스킴은 rescaling을 통한 근사 실수 연산 지원, 다항식 근사 활성화 함수(ReLU², Chebyshev).

4. **글로벌 모델 정확도 손실(DP-SGD 적용 시)**: Rényi Divergence 기반 분석에서 `E[L(w_T)] − L* = O( √(p·log(1/δ)/(K·T·ε²)) + ... )`. -> 클라이언트 수 K^, 라운드 수 T^일수록 정확도 회복.

5. **Non