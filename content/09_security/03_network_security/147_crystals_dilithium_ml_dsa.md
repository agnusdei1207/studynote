---
title: "Crystals Dilithium Ml Dsa"
date: "2026-04-19"
tags:
  - "studynote-security"
weight: 147
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CRYSTALS-Dilithium(크리스탈스-딜리시움)은 격자(Lattice) 수학 문제의 어려움에 기반한 양자 내성(Post-Quantum, PQC) 디지털 서명 알고리즘으로, NIST(National Institute of Standards and Technology)가 2024년 ML-DSA(Module Lattice-Based Digital Signature Algorithm, FIPS 204)로 표준화했다.
> 2. **가치**: 양자 컴퓨터(Quantum Computer)가 RSA·ECDSA 기반 기존 디지털 서명을 수초 내에 파괴할 수 있는 시대를 대비해, <strong>양자 공격에 안전한 디지털 서명 표준</strong>으로 인터넷·PKI(Public Key Infrastructure) 인프라를 미래 보호한다.
> 3. **판단 포인트**: Dilithium은 RSA/ECDSA 대비 공개키·서명 크기가 크지만 서명 생성·검증 속도가 빠르고 구현이 단순하여, <strong>TLS 1.3·코드 서명·PKI 인증서 대체</strong>의 1순위 후보다.

---

## Ⅰ. 개요 및 필요성

디지털 서명은 메시지의 무결성과 발신자 인증을 보장하는 암호 기술이다. 현재 인터넷 보안의 근간인 RSA·ECDSA(Elliptic Curve Digital Signature Algorithm)는 소인수분해와 이산대수 문제의 어려움에 의존한다. 그러나 Shor 알고리즘을 구현한 양자 컴퓨터가 등장하면 이 두 문제 모두 다항 시간(Polynomial Time)에 풀린다.

NIST는 2016년 PQC 표준화 공모를 시작했고, CRYSTALS-Dilithium이 최종 선발되어 2024년 **FIPS 204(ML-DSA)** 로 발표됐다. 이는 TLS·SSH·코드 서명·PKI 인증서·스마트카드 전 영역에 영향을 미친다.

<strong>Dilithium 없으면(PQC 전환 없으면) 발생하는 위험</strong>:
- "지금 암호화, 나중에 해독(Harvest Now, Decrypt Later)" 공격 — 지금 수집한 암호문을 양자 컴퓨터 완성 후 해독
- 인터넷 PKI 기반 신뢰 체계 붕괴
- HTTPS, VPN, 코드 서명, 전자 계약 등 전면 무력화

- **📢 섹션 요약 비유**: CRYSTALS-Dilithium은 <strong>'양자 컴퓨터라는 만능 마스터키가 등장하기 전에 교체하는 새로운 자물쇠(디지털 서명 알고리즘)'</strong> 입니다. 기존 자물쇠(RSA/ECDSA)는 양자 드릴로 1초 만에 열리지만, 격자 수학으로 만든 새 자물쇠는 양자 드릴도 뚫지 못합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 격자(Lattice) 기반 보안의 기초

```text
격자(Lattice) 수학 개념

  격자: n차원 공간에서 기저 벡터의 정수 선형 결합으로 이루어진 점의 집합

  기저 벡터
  b1 = (1, 0)   b2 = (0, 1)

  격자 점: 모든 a·b1 + b·b2 (a, b ∈ 정수)

  어려운 문제:
  +----------------------------------------------+
  | SVP (Shortest Vector Problem):               |
  | 격자에서 가장 짧은 벡터 찾기                  |
  | -> 고차원일수록 고전+양자 컴퓨터도 어려움       |
  |                                              |
  | LWE (Learning With Errors):                  |
  | 선형 방정식에 노이즈를 추가 -> 역산 불가능      |
  | -> Dilithium의 보안 기반                       |
  +----------------------------------------------+
```

CRYSTALS-Dilithium은 <strong>Module-LWE(Module Learning With Errors)</strong> 와 <strong>Module-SIS(Module Short Integer Solution)</strong> 문제의 어려움에 기반한다.

### 2. Dilithium 키·서명 크기 비교

| 알고리즘 | 공개키 크기 | 서명 크기 | 보안 레벨 |
|:---|:---:|:---:|:---|
| RSA-2048 | 256 B | 256 B | 128-bit (양자에 취약) |
| ECDSA P-256 | 64 B | 64 B | 128-bit (양자에 취약) |
| **Dilithium2 (ML-DSA-44)** | **1,312 B** | **2,420 B** | 128-bit (양자 내성) |
| **Dilithium3 (ML-DSA-65)** | **1,952 B** | **3,293 B** | 192-bit (양자 내성) |
| **Dilithium5 (ML-DSA-87)** | **2,592 B** | **4,595 B** | 256-bit (양자 내성) |

### 3. Dilithium 서명 흐름

```text
키 생성: (공개키 pk, 비밀키 sk) <- KeyGen()
          |
          |  sk: 랜덤 행렬 + 작은 다항식 벡터
          |  pk: 행렬 A와 t = A·s1 + s2 (s1, s2 작은 벡터)

서명:     σ <- Sign(sk, 메시지 M)
          |  반복: 랜덤 y 생성 -> w = A·y -> c = H(pk, M, w) -> z = y + c·s1
          |  조건: z, r0 = w - c·s2 의 크기가 임계값 이내이면 서명 완성

검증:     Verify(pk, M, σ)
          |  z 크기 확인 + w' = A·z - c·t 재계산 -> H(pk, M, w') == c?
```

- **📢 섹션 요약 비유**: Dilithium 서명은 **'노이즈가 섞인 수학 퍼즐에 비밀열쇠로 도장 찍기'** 입니다. 도장(서명)을 찍으려면 비밀열쇠가 있어야 하고, 노이즈가 섞인 답이 올바른 범위 안에 들어오는지 확인합니다. 양자 컴퓨터도 노이즈 퍼즐은 못 풀어냅니다.

---

## Ⅲ. 비교 및 연결

### PQC 디지털 서명 후보군 비교

| 알고리즘 | 기반 | 장점 | 단점 |
|:---|:---|:---|:---|
| **ML-DSA (Dilithium)** | 격자(Lattice) | 빠른 서명·검증, 구현 단순 | 큰 서명 크기 |
| <strong>SLH-DSA (SPHINCS+)</strong> | 해시 함수 | 수학 가정 최소 (해시만 의존) | 매우 큰 서명 (수십 KB) |
| **FN-DSA (FALCON)** | 격자(NTRU) | 작은 서명 크기 | 구현 복잡(부채널 공격 취약) |
| <strong>ECDSA</strong> | 이산대수 | 작은 크기, 범용 지원 | 양자에 취약 |

### 연결 개념 흐름

RSA/ECDSA 취약점(양자 컴퓨터) -> PQC 필요성 -> NIST PQC 표준화 -> ML-DSA(Dilithium), ML-KEM(Kyber), SLH-DSA(SPHINCS+) -> 하이브리드 TLS(기존+PQC 병행) -> 완전 PQC 전환

- **📢 섹션 요약 비유**: PQC 서명 알고리즘 선택은 **'방탄 조끼 소재 선택'** 과 같습니다. ML-DSA(격자)는 무게(크기)는 좀 있지만 방탄 성능이 우수하고 착용이 쉽습니다. SLH-DSA(해시)는 신뢰성은 최고지만 너무 무겁습니다. FALCON은 가볍지만 제조(구현)가 까다롭습니다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 의사결정 체크리스트

| 상황 | 권장 알고리즘 | 이유 |
|:---|:---|:---|
| TLS 1.3 인증서·핸드셰이크 | ML-DSA (Dilithium3) | 속도·범용성 균형 |
| 코드 서명 (장기 유효성) | SLH-DSA (SPHINCS+) | 수학적 가정 최소 = 장기 신뢰 |
| 소형 IoT 디바이스 서명 | FALCON (FN-DSA) | 작은 크기 (리소스 제약) |
| 전환 기간 (현재~3년) | 하이브리드 (ECDSA + ML-DSA) | 호환성 유지 |

### 심화 학습 핵심 포인트

1. <strong>PQC(Post-Quantum Cryptography)</strong>: 양자 컴퓨터 공격에 안전한 암호 알고리즘의 총칭
2. **Harvest Now, Decrypt Later**: 현재의 암호문을 저장해 미래 양자 컴퓨터로 해독하는 장기 공격
3. **ML-DSA = FIPS 204 = Dilithium**: 동일 알고리즘의 세 가지 이름
4. **하이브리드 서명**: 전환 기간 중 ECDSA + ML-DSA를 병렬 서명·검증

### 안티패턴

<strong>PQC 전환을 "양자 컴퓨터 완성 후"로 미루기</strong>: "지금 수확, 나중 해독" 공격은 현재 진행 중이다. 국가 기밀, 금융 데이터는 지금 수집되어 양자 컴퓨터 완성 후 해독될 수 있다. 장기 민감 데이터는 <strong>지금 즉시 PQC 전환</strong>이 필요하다.

- **📢 섹션 요약 비유**: PQC 전환 지연은 **'도둑이 지금 금고를 통째로 가져가고, 나중에 열쇠를 구하면 열겠다고 기다리는 상황'** 입니다. 금고(암호화된 데이터)는 이미 도둑 손에 있고, 양자 컴퓨터(열쇠)만 기다리면 됩니다. 지금 바꾸지 않으면 미래의 자신이 당합니다.

---

## Ⅴ. 기대효과 및 결론

CRYSTALS-Dilithium(ML-DSA)은 NIST가 공식 채택한 PQC 디지털 서명 표준으로, 향후 10~20년 내 인터넷 보안 인프라의 서명 알고리즘 기반을 교체하는 대규모 전환의 핵심이다.

**한계**: RSA·ECDSA 대비 공개키와 서명 크기가 10~40배 크다. TLS 핸드셰이크 패킷 크기 증가, X.509 인증서 크기 증가, 메모리·대역폭 제약 환경에서의 제한이 존재한다. 경량 IoT 환경에서는 FALCON이나 해시 기반 서명이 더 적합할 수 있다.

**미래 방향**: ① IETF RFC를 통한 TLS 1.3 PQC 확장 표준화, ② X.509 PQC 인증서 프로파일 확정, ③ HSM(Hardware Security Module)·PKI 솔루션의 ML-DSA 지원 확산, ④ 양자 내성 암호(ML-KEM + ML-DSA) 풀 스택 전환.

ML-DSA는 "더 좋은 서명이 아니라, 살아남기 위한 필수 서명"이다 — 양자 시대를 대비한 인터넷 신뢰 체계의 재건이라는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: ML-DSA로의 전환은 **'내진 설계가 없는 건물에 내진 보강재를 추가하는 리노베이션'** 입니다. 지진(양자 컴퓨터)이 오기 전에 보강하지 않으면, 순식간에 무너집니다. 건물이 멀쩡해 보여도 내진 기준이 바뀌면 반드시 보강해야 합니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>PQC (Post-Quantum Cryptography)</strong> | Dilithium이 속한 양자 내성 암호 알고리즘 분류 |
| <strong>ML-KEM (CRYSTALS-Kyber)</strong> | PQC 키 캡슐화 메커니즘; Dilithium(서명)과 함께 NIST PQC 쌍둥이 표준 |
| **격자(Lattice) 암호** | SVP, LWE 등 수학 난제 기반; 현재 PQC의 주류 방향 |
| **FIPS 204** | NIST가 발행한 ML-DSA(Dilithium) 공식 표준 번호 |
| **Harvest Now, Decrypt Later** | 현재 암호문 수집 후 미래 양자 컴퓨터로 해독하는 위협 |

### 📈 관련 키워드 및 발전 흐름도

```text
RSA / ECDSA (고전 암호 디지털 서명)
    |
    v
양자 컴퓨터 위협 -> Shor 알고리즘 -> RSA/ECDSA 파괴 가능
    |
    v
NIST PQC 표준화 공모 (2016~2024)
    |
    +-► ML-DSA (Dilithium) — 격자 기반 서명 [FIPS 204]
    +-► SLH-DSA (SPHINCS+) — 해시 기반 서명 [FIPS 205]
    +-► FN-DSA (FALCON) — 격자(NTRU) 기반 서명
    |
    v
하이브리드 전환 (ECDSA + ML-DSA 병행)
    |
    v
완전 PQC 전환 — TLS, PKI, 코드 서명, IoT
```

### 👶 어린이를 위한 3줄 비유 설명

1. 인터넷의 도장(디지털 서명)은 RSA·ECDSA라는 자물쇠로 만들어졌는데, <strong>양자 컴퓨터가 등장하면 이 자물쇠를 1초 만에 열 수 있어요!</strong> 그래서 새로운 자물쇠가 필요해요.
2. CRYSTALS-Dilithium은 <strong>격자(Lattice)라는 수학 미로</strong>에 기반한 새 자물쇠예요. 이 미로는 양자 컴퓨터도 빠져나오지 못할 만큼 복잡하게 설계되어 있어요!
3. 크기가 기존보다 크지만(공개키·서명이 더 길지만), 미래에도 <strong>인터넷 도장의 신뢰를 지킬 수 있는 유일한 방법</strong>이랍니다!
