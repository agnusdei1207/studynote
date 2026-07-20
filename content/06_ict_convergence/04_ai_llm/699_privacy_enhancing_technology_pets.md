---
title: "Privacy Enhancing Technology PETs"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 699
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PETs(Privacy Enhancing Technologies)와 연합 분석(Federated Analysis)의 결합은 **"원천 데이터 비노출 + 다자간 협업 연산 + 수학적 프라이버시 보장"**을 동시에 달성하는 기술 스택으로, 차등 프라이버시(DP), 동형 암호(HE), 보안 다자간 계산(SMPC), 영지식 증명(ZKP), 신뢰 실행 환경(TEE), 연합 학습(FL)이 7대 축을 형성하며, 데이터 주권·규제 준수·가치 추출의 트릴레마를 해소한다.
> 2. **가치**: 의료(NIH 36개 기관 COVID-19 FL 모델 AUC 0.85+), 금융(글로벌 12개 은행 이상거래 탐지 F1 0.78), 산업(제조사 예지 정비 정확도 23%^) 등 30% 이상의 데이터 부족 문제 해결과 약 70% 개인정보 처리 부담 경감, GDPR/EU AI Act/PIPA 등 글로벌 규제 컴플라이언스 동시 충족이라는 정량적 가치를 제공한다.
> 3. **판단 포인트**: **프라이버시-유용성-성능(통신/연산)-신뢰 가정의 4차원 트레이드오프**가 핵심 의사결정 변수이며, 데이터 민감도·참여자 수·연산 빈도·규제 등급에 따라 DP ε값(ε≤1 강력, 1~5 보통, 5~10 약함), HE 스킴(BFV/BGV/CKKS/TFHE), 동기/비동기 FL 토폴로지, TEE(Intel SGX/AMD SEV/ARM CCA) 배치 등 하이브리드 아키텍처 설계가 실무자의 핵심 판단 영역이다.

---

## Ⅰ. 개요 및 필요성

데이터 3법(2020. 8. 시행), EU 데이터법(2024. 9. 시행), EU AI Act(2024. 8. 시행), 미국 AI 행정명령(14091호) 등 글로벌 규제 환경이 **"데이터 이동성(Mobility) + 사용 통제(Control) + 프라이버시 보장(Privacy)"**을 동시에 요구하면서, 전통적 **"데이터 통합(Data Lake/Warehouse) -> 중앙 분석"** 패러다임은 법적·기술적 한계에 부딪혔다. 특히 **재식별 위험(Re-identification Risk)**, **상관관계 공격(Correlation Attack)**, **모델 역전 공격(Model Inversion Attack)** 등 단일 마스킹/가명처리로는 방어 불가능한 위협이 증가하면서, **원본 데이터가 이동하지 않고도 다자간 협업 연산이 가능한** PETs 기반 연합 분석이 차세대 데이터 거버넌스의 핵심 패러다임으로 부상했다.

NIST SP 800-188(2023), ENISA PETs Guidance(2023), ISO/IEC 27400:2022(Privacy Engineering), IEEE P3117(2024. 9. FDIS), W3C Federated Learning Community Group 등 국제 표준화 움직임이 빠르게 진행되며, OECD는 2023년 PETs 가이드라인을, UN AI High-Level Advisory Body는 2024년 최종 권고안에서 "Privacy-Preserving Federated Systems"를 핵심 거버넌스 도구로 채택했다.

```text
+--------------------------------------------------------------------------+
|        PETs 기반 연합 분석의 패러다임 전환 (Data-Centric -> Privacy-Centric) |
+--------------------------------------------------------------------------+

  [구 패러다임] 중앙 집중형 분석                  [신 패러다임] PETs 연합 분석
  ------------------------------                ------------------------------
   A사 데이터 --+                                 A사 --+
                |                                           |
   B사 데이터 --+--► [중앙 서버/데이터레이크] --► 분석     |   암호화/노이즈/
                |       (원본 노출, 재식별 위험)            |   익명화/보안 채널
   C사 데이터 --+                                           |
                                                            v
                                                [공통 모델/통계 산출]
                                                (원본은 각자 보유)
                                                +---------+---------+
                                                v         v         v
                                              A사 모델  B사 모델  C사 모델
                                              (지역 보존)

  법적 리스크  ●●●●●  (데이터 이동 = 처리)        법적 리스크  ●●○○○  (원본 비이동)
  프라이버시  ●○○○○  (단일 마스킹 취약)          프라이버시  ●●●●○  (수학적 보장)
  활용 가치  ●●●●○  (집계 정확)                 활용 가치  ●●●○○  (약간의 정확도 손실)
```

**구 패러다임의 한계**:
- 데이터 이동 시 **통제력 상실(Loss of Control)** -> 유출 시 사후 대응 불가
- 단일 가명처리는 **k-익명성, l-다양성** 등의 **Background Knowledge Attack**에 취약 (Sweeney, 2002; Narayanan & Shmatikov, 2006)
- 중앙 집중형은 **단일 장애점(SPOF)** 및 **내부자 위협(Insider Threat)** 표면화
- AI 학습 데이터는 **모델 자체로 원본 정보 누설** (Membership Inference, Carlini et al., 2023)

**신 패러다임의 등장 배경**:
- 2016년 Google Gboard가 **Federated Learning** 최초 상용화
- 2019년 Microsoft SEAL 오픈소스 공개, **동형 암호 실용화 가속**
- 2020년 GDPR·CCPA 강화, **법적 처리 근거 한정**
- 2021년 OpenMined PySyft, FATE v1.5 등 **개발자 도구 폭증**
- 2023년 ChatGPT 이후 **데이터 고립(AI Silo)** 현상 심화, 연합 분석 수요 폭증
- 2024년 NVIDIA FLARE 2.4, Flower 1.10 등 **대규모 프로덕션용 프레임워크** 등장
- 2025년 EU Data Act, 한국 데이터 산업법 본격 시행으로 **데이터 거래소·클린룸 의무화**

- **📢 섹션 요약 비유**: 데이터를 모래(원본)라 할 때, 옛 방식은 모든 모래를 한 항아리에 모아 유리병에 넣어 보는 것이었고, PETs 연합 분석은 각자 자기 항아리 안의 모래를 절대 꺼내지 않으면서도, "이 모래들의 평균 입자 크기는?" 이라는 질문에 정확히 답할 수 있는 **마법의 측정 도구**를 빌려주는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PETs 연합 분석은 크게 **3계층(데이터 평면/연산 평면/조정 평면) × 7대 핵심 기술**의 매트릭스로 구성된다. 각 기술은 단독 사용도 가능하지만, 실무에서는 **하이브리드 구성**이 일반적이다(예: FL + DP + HE, TEE + MPC + DP).

```text
+-----------------------------------------------------------------------------+
|             PETs 연합 분석 3계층 하이브리드 아키텍처 (Reference Architecture)|
+-----------------------------------------------------------------------------+

  [조정 평면 / Orchestration Layer] ------------------------------------------
   +----------------------------------------------------------------------+
   | Coordinator / Aggregator (신뢰 최소화: TEE 내부 배치 또는 MPC화)     |
   |  - 글로벌 모델/통계 조립    - 라운드/에폭 스케줄링                     |
   |  - 참여자 인증(DP ID)        - 감사 로그(ZKP 기반)                     |
   |  - 차등 프라이버시 노이즈 주입 (Gaussian/Laplace Mechanism)            |
   +----------------------------------------------------------------------+
                                    ^
                                    | (암호화된 그라디언트/연산 결과만 송수신)
                                    |  - HE 암호문 / 비밀 분배 / 영지식 증명
                                    v
  [연산 평면 / Computation Layer] --------------------------------------------
   +----------------------------------------------------------------------+
   |  참여 노드 (Participant): 병원, 은행, 공장, 공공기관, 디바이스       |
   |  +------------------+  +------------------+  +------------------+   |
   |  |  로컬 학습/연산   |  |  로컬 학습/연산   |  |  로컬 학습/연산   |   |
   |  |  + DP-SGD        |  |  + DP-SGD        |  |  + DP-SGD        |   |
   |  |  + HE 암호화     |  |  + HE 암호화     |  |  + HE 암호화     |   |
   |  |  + TEE Enclave   |  |  + TEE Enclave   |  |  + TEE Enclave   |   |
   |  +------------------+  +------------------+  +------------------+   |
   +----------------------------------------------------------------------+
                                    ^
                                    | (로컬 학습/연산은 로컬에서만 수행)
                                    v
  [데이터 평면 / Data Layer] ------------------------------------------------
   +----------------------------------------------------------------------+
   |  분산된 원천 데이터 (이동 X, 단독 처리)                               |
   |  - EHR/PACS, 거래로그, IoT 센서, 공공데이터, 디바이스 로그             |
   |  - 가명/비식별화 + Secure Enclave 내부에서만 평문 처리                 |
   +----------------------------------------------------------------------+

  ※ 보안 채널: TLS 1.3 + mTLS (상호 인증), QUIC 프로토콜, ToR onion routing 옵션
  ※ 연합 분석 변형: Federated Learning, Federated Analytics, Data Clean Room, FL+HE
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **차등 프라이버시(Differential Privacy, DP)** | **수학적 프라이버시 보장** | `M(D) ≈ M(D')` (인접 데이터셋 간 확률 분포 차이 ≤ exp(ε)). **Laplace Mechanism**(L1 민감도 기반), **Gaussian Mechanism**(L2 민감도, (ε,δ)-DP), **DP-SGD**(Abadi et al., 2016, gradient clipping L2 norm ≤ C, Gaussian noise σ = C·√(2·log(1.25/δ))/ε), **Rényi DP**(ε-order Rényi divergence로 tighter composition), **Local DP / Central DP / Shuffle Model** 3계층 모델 |
| **동형 암호(Homomorphic Encryption, HE)** | **암호문 상태 연산** | **FHE(완전동형)**: TFHE(부트스트래핑 13ms), CKKS(부동소수점 근사, ML 친화), BFV/BGV(정수). **PHE(부분동형)**: Paillier(합), ElGamal(곱). **LWE/RLWE** 기반 lattice crypto, **post-quantum 안전성**. Microsoft SEAL, OpenFHE, Zama TFHE-rs, PALISADE, Lattigo, HElib |
| **보안 다자간 계산(Secure Multi-Party Computation, SMPC)** | **다자간 비밀 분할 연산** | **비밀 분할(Secret Sharing)**: Shamir (k,n)-threshold, Replicated/Additive SS. **야 GARBLED Circuit**(Yao, 1986), **GMW 프로토콜**, **SPDZ 프로토콜**(2012, Beaver triples로 malicious 보안), **ABY/ABY2.0**(혼합 회로), **Cerebro, CrypTen, MP-SPDZ, SecretFlow(Secret Note)**, **OT(oblivious transfer) 확장** |
| **영지식 증명(Zero-Knowledge Proof, ZKP)** | **사실 증명·정보 비공개** | **zk-SNARK**(Groth16, PLONK, trusted setup 필요), **zk-STARK**(post-quantum, transparent setup, 해시 기반), **Bulletproofs**(range proof, 설정 불요), **Halo2**(recursive), **Plonky2/3**(zkEVM), **Merkle Patricia Trie + zk**. 사용처: 모델 무결성, 라운드 정확성, 클라이언트 자격 증명 |
| **신뢰 실행 환경(TEE, Enclave)** | **하드웨어 격리 보호** | **Intel SGX 2.0**(EPC 최대 1TB, FLC, Flexible Launch Control), **AMD SEV-SNP**(메모리 암호화, CC), **ARM CCA**(Realm Management Monitor), **NVIDIA H100 Confidential Computing**(GPU + TEE), **Intel TDX**, **Apple Secure Enclave**. 원격 인증(Remote Attestation) + 메모리 암호화 + 측채널 완화(_constant-time 코드, fence.t_). **Asylo, Open Enclave SDK, Confidential Containers (CoCo)** |
| **연합 학습/분석(Federated Learning/Analytics)** | **분산 모델 학습/통계** | **FL 알고리즘**: FedAvg(McMahan et al., 2017), FedProx(Li et al., 2020, proximal term μ), FedNova(wang et al., 2020, 사합 가중), FedOpt(서버 Adam/Yogi), FedBN(배치 정규화 보존), SCAFFOLD(제어 변수로 분산 완화). **분석