---
title: "Homomorphic Encryption Secure Computation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 757
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동형 암호(Homomorphic Encryption, HE)는 평문 연산을 복호화 없이 암호문(ciphertext) 상태에서 직접 수행하는 공개키 암호 패러다임으로, LWE(Learning With Errors)/RLWE(Ring-LWE) 격자 난제에 기반한 BGV, BFV, CKKS, TFHE 등 4세대 FHE(Fully HE) 스킴이 핵심이며, `KeyGen -> Enc(pk, m) -> Eval(pk, f, c) -> Dec(sk, c') = f(m)`의 순서로 데이터 기밀성과 연산 동시성을 보장한다.
> 2. **가치**: Microsoft SEAL(128-bit security 기준) 기준 단순 덧셈은 μs 단위, 곱셈은 ms 단위, CKKS 자가 부트스트래핑은 수 초~수십 초 수준으로, 클라우드 환경에서 평문 미노출 상태로 AI 추론·의료 유전체 분석·금융 사기 탐지 등 0-Day 데이터 가치 활용을 가능케 하며, GDPR/개인정보보호법의 가명·익명 처리 의무를 충족하는 기술적 수단으로 부상한다.
> 3. **판단 포인트**: (a) 정확 산술(BGV/BFV, 정수형) vs 근사 산술(CKKS, 실수형 부동소수) 선택, (b) 부트스트래핑 깊이(L vs Q 모듈러스 체인) vs 노이즈 budget 트레이드오프, (c) GPU/TPU 가속(100~1000×) 적용 여부, (d) 동형 + MPC + ZKP 하이브리드 구성 시 신뢰 경계(trust boundary) 재설계, (e) 양자 내성(Post-Quantum Cryptography) 마이그레이션과 FHE의 동일 격자 가정 공유로 인한 시너지 검토가 핵심 결정 사안이다.

---

## Ⅰ. 개요 및 필요성

데이터 활용과 개인정보 보호 사이의 모순은 클라우드 컴퓨팅·빅데이터·AI 시대의 구조적 딜레마다. 전통적 암호화(AES-256, RSA-2048)는 **저장(At-Rest)**과 **전송(In-Transit)** 단계에서 데이터를 보호하지만, **사용(Use/In-Use)** 단계에서는 반드시 평문으로 복호화해야 하므로 클라우드 사업자·악의적 내부자·메모리 덤프 공격자에게 평문이 노출되는 근본적 한계가 존재한다.

이 문제를 해결하기 위해 1978년 Rivest, Adleman, Dertouzos가 "On Data Banks and Privacy Homomorphisms"에서 처음 개념을 제기한 이래, 2009년 Craig Gentry의 격자 기반 첫 FHE 구성(LWE 기반 이상 격자, ideal lattice)으로 비로소 실현 가능성이 입증되었다. 이후 BGV(2011, Brakerski-Gentry-Vaikuntanathan, 모듈러스 스위칭), BFV(2012, Fan-Vercauteren, Brakerski), GSW(2013, Gentry-Sahai-Waters, 부트스트래핑 단순화), CKKS(2017, Cheon-Kim-Kim-Song, 근사 실수 연산) 등으로 연산 효율성과 정확도가 비약적으로 발전했다.

특히 2023년 Google Transpiler(C++ -> HE IR), Microsoft Research의 FHE 다이어그램, DARPA DPRIVE 프로그램(2020~2024, 5,500만 달러 투자), HomomorphicEncryption.org의 표준화 활동(2024년 HE Bootstrapping/Key Switching 표준 초안)을 통해 산업 적용의 골든타임이 도래했다.

```text
+------------------- 동형 암호 패러다임 비교 -------------------+
|                                                                |
|  ① 전통적 암호화 (AES/RSA)                                      |
|  +-----+  평문   +------+  암호문   +------+  평문+연산  +-----+|
|  | Alice+-->[Encrypt]-->[   Cloud   ]<--[Decrypt]<--연산<--[  ] ||
|  +-----+                  |                  ^                 ||
|                           +- 평문 노출!! (메모리/버스/로그)    ||
|                                                                |
|  ② 동형 암호화 (FHE)                                            |
|  +-----+  평문   +------+  암호문(연산) +------+  평문        ||
|  | Alice+-->[Enc(pk)]-->[   Cloud   ]--->[Dec(sk)]<---[Bob]||
|  +-----+                  |            ^                     ||
|                           |            |                     ||
|                     (평문 접근 불가) (최종 결과만 복호)        ||
|                                                                |
|  ③ 하이브리드 (FHE + MPC + TEE + ZKP)                          |
|  +-----+  HE    +------+  MPC     +-----+  TEE                ||
|  | Alice+-->[Enc]-->[Cloud Eval]-->[Multi-Party]-->[Secure Enclave]||
|  +-----+                  ^          ^            ^          ||
|                    데이터 기밀성  다자 협력    무결성 증명     ||
+----------------------------------------------------------------+
```

**기존 vs 신규 패러다임 비교:**
- 기존: 암호화 -> 전송 -> 저장(At-Rest) -> 복호화 -> 평문 연산 -> 폐기 -> 침해 시 평문 유출(예: 2017년 Equifax 1.47억 명 평문 유출)
- 신규: 암호화 -> 전송 -> 저장 -> **암호문 상태 연산** -> 결과만 복호화 -> 평문은 메모리·로그에 미존재 (Zero-Leakage Computation)
- **법적 배경**: GDPR 제32조(적정 기술적 조치), 한국 개인정보보호법 제29조(안전조치의무), EU AI Act(2024) 고위험 AI의 데이터 보호 의무, HIPAA 의료 데이터 프라이버시

- **📢 섹션 요약 비유**: 동형 암호는 "**잠긴 유리 상자 안에서 장갑을 끼고 작업**"하는 것과 같다. 상자 안의 내용물(평문 데이터)은 절대 꺼내지 않으면서, 외부에서 장갑(연산 회로)을 통해 조립·계산·추론까지 모두 끝낸 뒤 **결과물만** 꺼내 열어보는 방식이다. 기존 암호화는 작업할 때마다 자물쇠를 풀어야 했던 것과 대조된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FHE의 수학적 토대는 **격자(Lattice) 기반 LWE 문제**다. 차원 n의 정수 격자 Λ에 대해, 오류 e가 추가된 선형방정식 `b = As + e (mod q)`로부터 비밀 s를 복원하는 것이 LWE 문제이며, 단축 차원(Shortest Vector Problem, SVP)이 NP-Hard로 알려진 격자 문제와 등치성을 갖는다. 이를 **Ring-LWE**로 승격하면 다항식 환 `R = Z[x]/(x^N + 1)` 위에서 `b = a·s + e (mod q)`로 표현되어 n² -> N개의 다항식 계수를 한 번에 처리하여 약 N배의 효율 향상을 얻는다.

```text
+---------- FHE 스킴 4세대 진화 계보도 ----------+
|                                                   |
|  1세대 (2009)      2세대 (2011-2012)             |
|  +----------+     +----------+ +----------+     |
|  | Gentry   | ---> |   BGV    | |   BFV    |     |
|  | 이상격자  |     | ModSwitch| | Brakerski|     |
|  | Ideal L  |     | 정수연산 | | 정수연산 |     |
|  +----------+     +----------+ +----------+     |
|       v                                            |
|  3세대 (2013-2017)   4세대 (2016-현재)             |
|  +----------+     +----------+ +----------+     |
|  |   GSW    | ---> |  FHEW    | |   CKKS   |     |
|  | Approx.  |     |  TFHE    | |  근사실수 |     |
|  | Bootstrp |     |  게이트  | |  AI/ML   |     |
|  +----------+     +----------+ +----------+     |
|       v                                            |
|  5세대 (2022-현재)                                 |
|  +----------+ +----------+ +----------+          |
|  |  MHEAAN  | | BGV/BFV  | | CKKS     |          |
|  | Multi-Key| | GPU 가속 | |  Bootstrp|          |
|  | Threshold| | (CUDA)   | |  가속화  |          |
|  +----------+ +----------+ +----------+          |
+---------------------------------------------------+
```

### 4세대 FHE 스킴의 핵심 비교

| 스킴 | 평문 도메인 | 노이즈 처리 | 대표 라이브러리 | 적합 워크로드 |
| :--- | :--- | :--- | :--- | :--- |
| **BGV** | 정수 Z_p (exact) | 모듈러스 스위칭(MS), 평탄화 | HElib, PALISADE | 정확한 DB 검색, 투표 |
| **BFV** | 정수 Z_p (exact) | 모듈러스 스위칭, Rescale | Microsoft SEAL, Lattigo, OpenFHE | 정수 통계, 암호 |
| **CKKS** | 복소수/실수 (approx) | Rescaling, 근사 부트스트래핑 | Microsoft SEAL, OpenFHE, Lattigo | AI/ML, 신호처리 |
| **FHEW/TFHE** | 이진 게이트 (Boolean) | 부트스트래핑 게이트 단위 | Concrete (Zama), TFHE-rs | 사적 검색(PIR), 결정트리 |

### FHE 5대 핵심 원리 (Operation Pipeline)

```text
+-- FHE 연산 파이프라인 (CKKS 기준) --------------------------+
|                                                               |
|  [1] KeyGen(λ)                                                |
|      +- 비밀키: sk ∈ R_q                                       |
|      +- 공개키: pk = (b, a) where b = -a·sk + e (mod q)        |
|      +- Evaluation Key: evk (재선형화/부트스트래핑용)          |
|      +- Galois Key: gk (회전/슬롯 연산용)                       |
|                                                               |
|  [2] Enc(pk, m) -> ct = (c0, c1) = (b·u + m + e0, a·u + e1)  |
|                                                               |
|  [3] Eval(ck, f, ct)                                          |
|      +- HomAdd:  c_add = ct1 + ct2 (동형 덧셈)                |
|      +- HomMult: c_mul = ct1 ⊗ ct2 (텐서 -> 재선형화)         |
|      |         L = c0·c0', c0·c1'+c1·c0', c1·c1'             |
|      |         -> relin(evk) -> 다시 2-component로 축약          |
|      +- Rescale: c' = c / p (p: 스케일링 인자)                 |
|      |         -> 노이즈 budget 환원, 정밀도 trade-off          |
|      +- Rotate: π(ck, ct) (슬롯 단위 회전 = SIMD)             |
|                                                               |
|  [4] Bootstrap(노이즈 회복)                                    |
|      +- 모듈러스 체인 끝에서 modulus를 다시 키우는             |
|         "디지털 배터리 충전" -> 무한 깊이 회로 평가 가능       |
|                                                               |
|  [5] Dec(sk, ct) -> m' (≈ m, CKKS의 경우 오차 존재)            |
+---------------------------------------------------------------+
```

### 6대 핵심 컴포넌트

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **암호문 다항식 (Ciphertext)** | 평문 슬롯들의 벡터를 단일 다항식으로 패킹 | `pt(x) = m0 + m1·x + ... + m_{N/2-1}·x^{N/2-1}` 형태, `N = 2^15~2^17` (power-of-two) |
| **모듈러스 체인 (Modulus Chain)** | 노이즈 관리용 다중 소수 q_0 < q_1 < ... < q_L | 각 곱셈 후 rescaling으로 한 단계씩 강등, 깊이 L 결정 = 곱셈 횟수 한계 |
| **노이즈 budget (B)** | 복호화 정합성 유지 한계 | `B = q_L / (||c||_∞·||sk||_∞·ε)`, 곱셈마다 poly(N)·B 만큼 소모 |
| **재선형화 (Relinearization)** | 곱셈 후 차수 증가(2->3->4...)를 2-component로 축약 | `decomp(q/p)` + 곱셈 + 키 스위칭, O(N²·log q) 비용 |
| **부트스트래핑 (Bootstrapping)** | 노이즈 budget 충전(거의 무한 깊이 회로) | ModRaise -> Dec(sk) in HE -> Enc -> 비교 결과, CKKS는 1-2초, TFHE는 10ms |
| **Galois 회전 (Rotation)** | SIMD 슬롯 단위 연산을 위한 다항식 회전 | `x^i·c(x) mod (x^N+1)` 회전 키(galois key)로 N개 슬롯을 1회 op로 처리 |

### 핵심 파라미터 선정 공식

보안 파라미터 λ (128-bit), 깊이 L, 다항식 차수 N, 모듈러스 비트 q_L, 오차 분포 σ는 다음의 동시 만족이 필수다:

```
1) LWE Hardness:    n ≥ (λ + 110) / 7.2         (BKZ 알고리즘 기준)
2) Noise Budget:    log(q_L) > L·log(p) + log(t) + log(N)·depth
3) Correctness:     N ≥ 2·(L+1)·log(q_L)/log(2)   (RLWE 표준)
4) Performance:     N ∈ {4096, 8192, 16384, 32768}, L ∈ {1, 2, ...}
```

**예시 (Microsoft SEAL CKKS 권장)**:
- N=16384, |q|=438 bits, L=18 level, log p=30 -> 약 6번 곱셈 + 부트스트래핑 가능
- 128-bit 보안, 1 슬롯 ≈ 32-bit 정수 / 30-bit 근사 실수 정밀도

- **📢 섹션 요약 비유**: 동형 암호는 "**수학의 노이즈 공학**"이다. 데이터에 의도적으로 미세한 정적 잡음(LWE error)을 섞어 가짜 평문으로 위장한 뒤, 연산할 때마다 잡음 측정값을 정확히 추적·관리한다. 잡음 budget이 떨어지면 **부트스트래핑**이라는 디지털 세탁기로 잡음을 다시 낮은 수준으로 되돌리며, 이는 마치 자동차 엔진 오일을 교체하며 무한 주행 거리를 확보하는 것과 같다.

---

## Ⅲ.