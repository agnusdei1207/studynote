---
title: "Post Quantum Cryptography PQC Migration"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 703
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 양자컴퓨터의 쇼어(Shor) 알고리즘이 RSA/ECC 기반 공개키암호를 다항식 시간에 해독함에 따라, NIST FIPS 203/204/205 표준(ML-KEM, ML-DSA, SLH-DSA)을 중심으로 격자(lattice), 해시(hash), 코드(code) 기반의 양자내성 알고리즘으로 전환하는 전사적 암호체계 모빌리티 전략이며, 본질은 "암호학적 민첩성(Crypto-Agility)" 확보이다.
> 2. **가치**: HNDL(Harvest Now, Decrypt Later) 공격으로 이미 저장된 암호문도 향후 양자컴퓨터로 해독될 수 있어, 10년 이상의 장기 기밀성을 가진 의료·군사·외교 데이터의 기밀성 보장과, TLS 1.3 핸드셰이크 시 인증서 체인 비대화(ML-DSA: 약 2.4KB vs ECDSA P-256: 약 64Byte)에 따른 패킷 오버헤드·HSM 펌웨어 교체 등 운영 리스크의 선제적 관리가 핵심 가치이다.
> 3. **판단 포인트**: ML-KEM 단독 vs. ECDH+ML-KEM 하이브리드 채택, ML-DSA(빠름·서명 큼) vs SLH-DSA(느림·서명 작음·해시 기반 안전성 입증) 간 전자서명 선택, CBOM(Cryptographic Bill of Materials) 기반 자산 가시성 확보 여부, 그리고 양자내성 마이그레이션 비용(전 세계 약 70억 달러, NIST IR 8413 추정)과 SLA 영향도 사이의 트레이드오프가 결정적 판단 포인트이다.

---

## Ⅰ. 개요 및 필요성

고전 공개키 암호(RSA-2048, ECDSA P-256, DH Group 14 등)의 안전성은 **소인수분해(IFP)**와 **이산대수(DLP)** 문제의 계산 복잡성에 기반한다. 그러나 1994년 피터 쇼어(Peter Shor)가 개발한 쇼어 알고리즘은 이 두 문제를 양자 푸리에 변환(QFT)을 통해 다항식 시간 $O((\log N)^3)$ 내에 해결할 수 있음을 증명했다. IBM Condor(1,121 큐비트, 2023년)와 같이 NISQ(Noise Intermediate-Scale Quantum) 시대를 거쳐, 2030년 이후 fault-tolerant quantum computer(FTQC)가 상용화될 경우, 현재 전 세계 HTTPS 트래픽의 약 95% 이상을 보호하는 RSA/ECC 기반 PKI 체계는 구조적으로 붕괴한다.

더욱 심각한 것은 **HNDL(Harvest Now, Decrypt Later)** 위협이다. 국가별 APT(Advanced Persistent Threat) 조직은 현재의 TLS/RSA 암호화된 통신을 대량 저장했다가, 향후 양자컴퓨터가 가용화되는 시점에 일괄 복호화할 수 있다. 이는 10~20년 이상의 장기 기밀성을 요구하는 국방 기밀, 의료 유전체 데이터, 외교 문서, 산업 스파이의 핵심 설계도 등에 대해 **즉각적 위협**이 된다. NSA는 2021년 CNSA 2.0(Commercial National Security Algorithm Suite 2.0)을 통해 양자컴퓨팅 위협이 "이론적이지 않고 현실적(imminent risk)"이라고 천명한 바 있다.

이에 2016년 NIST는 전 세계적으로 PQC 표준화 프로젝트를 개시하여 8년 여의 평가 끝에 2024년 8월 FIPS 203/204/205를 확정·공표했다. 마이그레이션은 단순 알고리즘 교체가 아니라 **인증서 체인, HSM, PKI, TLS 핸드셰이크, VPN, 코드서명, API 키 관리** 등 전체 암호 생태계의 재설계를 수반한다. KISA(한국인터넷진흥원)도 2023년 「양자내성암호 전환 가이드라인」을 발간하고, 과학기술정보통신부(MSIT) 주도로 2030년까지 공공·금융·국가기간시설의 단계적 전환을 추진 중이다.

```text
[PQC 전환 위협 인식 및 표준화 흐름]

  +------------------+         +--------------------------+
  |  Shor's Algorithm |         |  Harvest Now, Decrypt    |
  |  (1994)           | -------> |  Later (HNDL) 위협        |
  |  IFP/DLP -> P-time|         |  현재 암호문 저장 후       |
  +--------+---------+         |  미래 양자컴퓨터로 해독    |
           |                    +-------------+------------+
           v                                  v
  +--------------------------------------------------------+
  |  NISQ 시대 (2023~)                                     |
  |  +- IBM Condor 1,121 qubits / Google Willow 105 qubits |
  |  +- RSA-2048 직접 해독은 불가 (수백만 큐비트 필요)       |
  +------------------------+-------------------------------+
                           v
  +--------------------------------------------------------+
  |  PQC 표준화 완료 (2024. 8.)                             |
  |  +- FIPS 203 : ML-KEM  (Module-Lattice KEM)            |
  |  +- FIPS 204 : ML-DSA  (Module-Lattice Signature)      |
  |  +- FIPS 205 : SLH-DSA (Stateless Hash-based Sig.)     |
  |  +- FIPS 206 : FN-DSA  (FFT over NTRU, 발표예정)       |
  +------------------------+-------------------------------+
                           v
  +--------------------------------------------------------+
  |  전사적 Crypto-Agility 구축 및 마이그레이션 수행        |
  |  Inventory -> Risk Assessment -> Hybrid Pilot -> 전환 -> Legacy 폐기 |
  +--------------------------------------------------------+
```

**기존 패러다임 vs. 양자내성 패러다임 비교**

| 관점 | 기존 RSA/ECC 패러다임 | 양자내성 PQC 패러다임 |
|---|---|---|
| **수학적 안전성 근거** | IFP / DLP (지수 시간 난이도) | LWE, Module-LWE, Syndrome Decoding (최악의 경우 양자 회로 모델에서도 지수 시간) |
| **키/서명 크기** | RSA-2048: 256B, ECDSA P-256: 64B | ML-KEM-768: pk 1,184B / ct 1,088B, ML-DSA-65: sig 3,293B |
| **서명 검증 속도** | ECDSA 검증: ~0.1ms (x86) | ML-DSA-65 검증: ~0.05ms (더 빠름), SLH-DSA-SHA2-128s: ~수십 ms |
| **사용 알고리즘** | RSA-OAEP, ECDH, ECDSA, DH | ML-KEM(키캡슐화), ML-DSA(서명), SLH-DSA(보조 서명) |
| **유지보수 패러다임** | 알고리즘 교체 시 클라이언트·서버·CA·HSM 동시 갱신 어려움 | Cryptographic Agility + 알고리즘 식별자(OID/AlgorithmIdentifier) 추상화 |

- **📢 섹션 요약 비유**: 양자컴퓨터라는 "만능 자물쇠 해제 마스터키"가 등장하기 전에, 자물쇠 자체를 숫자조합이 아닌 "양자 회전톱날 구조(lattice)"로 바꿔치는 작업이 PQC 전환입니다. 문제는 자물쇠뿐 아니라 열쇠 구멍(키 길이), 문틀(인증서), 금고 안의 모든 것(HSM, VPN)도 함께 교체해야 한다는 점입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PQC 마이그레이션 아키텍처는 크게 **(A) 알고리즘 계층**, **(B) 프로토콜 통합 계층(TLS/IPsec/CMVP)**, **(C) PKI·자격증명 계층**, **(D) 운영 거버넌스(CBOM·HSM·라이프사이클)**의 4계층으로 구성된다.

### (A) 알고리즘 계층 - NIST PQC 3대 표준

**1) ML-KEM (Module Learning with Errors Key Encapsulation, FIPS 203)**
- **수학적 기반**: Module-LWE(Learning With Errors) 문제. 격자 $\mathbb{Z}_q^{n \times k}$ 상에서 $\mathbf{As} + \mathbf{e} = \mathbf{b}$에서 비밀 $\mathbf{s}$를 복원하는 것이 계산적으로 어려움.
- **파라미터 세트**:
  - ML-KEM-512: 1단계 보안(NIST Level 1, AES-128 brute force와 동급), pk 800B, ct 768B
  - ML-KEM-768: 3단계 보안(NIST Level 3, AES-192 동급), pk 1,184B, ct 1,088B -> **TLS 1.3 기본 권장**
  - ML-KEM-1024: 5단계 보안(NIST Level 5, AES-256 동급), pk 1,568B, ct 1,568B
- **동작 원리(IND-CCA2 안전)**:
  1. KeyGen(): 공개키 $\mathbf{pk}=(\mathbf{A}, \mathbf{b}=\mathbf{As}+\mathbf{e})$, 비밀키 $\mathbf{sk}=\mathbf{s}$
  2. Encaps(): $\mathbf{r}, \mathbf{e_1}, \mathbf{e_2}$ 샘플링 -> 임시 키 $K$ -> $(\mathbf{c_1}, \mathbf{c_2}, K)$ 반환
  3. Decaps(): $\mathbf{s}$로 $(\mathbf{c_1}, \mathbf{c_2})$ 복호화 -> 동일 $K$ 복원 (Fujisaki-Okamoto 변환 적용)

**2) ML-DSA (Module-Lattice Digital Signature Algorithm, FIPS 204)**
- **수학적 기반**: Module-LWE + Module-SIS(Short Integer Solution)의 결합. "비둘기집 원리"로 비밀 서명 벡터 $y$를 격자상에 은닉.
- **파라미터 세트**:
  - ML-DSA-44: 128-bit 보안, sig 2,420B
  - ML-DSA-65: 192-bit 보안, sig 3,293B -> **TLS 인증서 기본 권장**
  - ML-DSA-87: 256-bit 보안, sig 4,627B
- **Fiat-Shamir with Aborts**: 거부 샘플링(rejection sampling)을 통해 서명 분포가 비밀키에 의존하지 않도록 함.

**3) SLH-DSA (Stateless Hash-based Signature, FIPS 205)**
- **수학적 기반**: 충돌·2차 저항성 해시함수(SHA-2, SHAKE)만의 안전성. 양자내성 파라다임에서 **가장 보수적인 선택**.
- **구조**: WOTS+ (Winternitz One-Time Signature) + Merkle 트리(Hypertree) + FORS(Few-Time Signature)로 구성
- **파라미터**: SLH-DSA-SHA2-128f/s, SHA2-192f/s, SHA2-256f/s, SHAKE-128f/s, 192f/s, 256f/s
- **특징**: 서명 크기 7~50KB로 매우 크지만, 격자 기반 알고리즘이 향후 추가 분석에서 깨질 경우(예: 2022년 SIDH 깨짐) **백업 안전망** 역할

**4) FN-DSA (FALCON, FIPS 206 draft)**
- NTRU 격자 + FFT(고속 푸리에 변환) 기반. 서명 크기(666~1,280B)가 ML-DSA보다 훨씬 작아 **TLS 인증서 체인 비대화 완화에 유리**하나, 부동소수점 연산과 Gaussian sampler 구현 복잡도가 매우 높음. 양자 안전 Gaussian 샘플링이 핵심.

### (B) 프로토콜 통합 계층 - TLS 1.3 하이브리드

가장 중요한 적용 지점은 TLS 1.3(RFC 8446) 핸드셰이크다. 단일 알고리즘 채택의 리스크를 줄이기 위해 **하이브리드 키 합의(hybrid key agreement)**가 사실상 표준이 된다.

```text
[TLS 1.3 PQC 하이브리드 핸드셰이크 (X25519 + ML-KEM-768)]

  Client                                               Server
    |                                                    |
    |  ClientHello                                       |
    |  +- key_share:                                     |
    |  |   +- group: x25519        (기존 ECDH)          |
    |  |   +- group: X25519MLKEM768 (draft-ietf-tls-   |
    |  |                              hybrid-design)    |
    |  +- signature_algorithms:                          |
    |      +- ml_dsa_65, slh_dsa_sha2_128s              |
    |--------------------------------------------------->|
    |                                                    |
    |              ServerHello                           |
    |              +- key_share: X25519MLKEM768          |
    |              +- certificate: (PQC-signed by CA)    |
    |              +- certificate_verify: ML-DSA-65 sig  |
    |              +- finished: HMAC over transcript     |
    |<---------------------------------------------------|
    |                                                    |
    |  finished                                          |
    |--------------------------------------------------->|
    |                                                    |
    |   application data (AES-256-GCM or ChaCha20-Poly1305) |
    |  ※ 대칭키는 Grover 공격 대응으로 AES-256 유지       |
    |<---------------------------------------------------->|
```

**하이브리드 그룹 표준(2024년 기준)**:
- `X25519MLKEM768` (Cloudflare, Google Chrome 131+ 기본 활성화, 2024. 9.)
- `P256MLKEM768` (NIST P-256 + ML-KEM-768, FIPS 환경)
- `X25519Kyber768Draft00` (구 draft, 폐기)

`ClientHello` 패킷 크기 변화: 기존 ~512B -> 하이브리드 적용 시 **~1.5KB** (한 번의 패킷 손실 시 1-RTT 추가 발생 가능). QU