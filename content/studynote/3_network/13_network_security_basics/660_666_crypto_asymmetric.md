+++
title = "660-666. 공개키 암호화와 키 교환 (RSA, ECC, DH)"
date = "2026-03-14"
[extra]
category = "Network Security"
id = 660
+++

# 660-666. 공개키 암호화와 키 교환 (RSA, ECC, DH)

> **1. 본질**: 대칭키 암호의 근본적 결함인 **키 분배(Key Distribution)** 문제를 수학적 난제(NP-hard 문제)를 기반으로 한 비대칭 구조로 해결한 보안 체계이다.
> **2. 가치**: 별도의 비밀 채널 없이 공개망(Internet)에서 안전한 통신을 구축하며, 특히 **ECC (Elliptic Curve Cryptography)**는 한정된 리소스(대역폭, 연산력) 환경에서 **동일한 보안 강도를 가진 RSA 대비 키 크기를 약 1/10 수준으로 최적화**하여 성능을 극대화한다.
> **3. 융합**: 전자서명(무결성/부인 방지)과 TLS/SSL 핸드셰이크의 핵심이며, 블록체인(암호화폐 지갑) 및 메타버스 보안의 기반이 되는 결합도가 높은 기술이다.

+++

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
공개키 암호(Public Key Cryptography) 또는 비대칭 암호(Asymmetric Cryptography)는 암호화(Encryption)와 복호화(Decryption)에 사용하는 키(Key)가 서로 다른 쌍(Key Pair)으로 구성된 암호 시스템을 의미한다. 이 시스템의 철학은 "수학적으로 쉬운 문제(연산)와 매우 어려운 문제(역연산)의 비대칭성"을 이용하는 데 있다. 공개키는 누구나 알 수 있지만, 그로부터 개인키를 유추하는 것은 계산상 불가능하게 설계된다.

### 2. 배경 및 진화 (대칭키의 한계에서 비대칭키로)
1976년 Whitfield Diffie와 Martin Hellman이 제안하기 전까지는 대칭키(Symmetric Key) 방식(DES, AES 등)이 주류였다. 그러나 대칭키는 **$N(N-1)/2$**의 키 관리 복잡도와 송수신자 간의 안전한 채널 선행 필요 문제를 안고 있었다. 이를 해결하기 위해 비밀 채널 없이도 안전한 키 공유가 가능한 **PKI (Public Key Infrastructure)**의 기반이 마련되었다.

### 3. ASCII: 보안 모델의 진화
```ascii
[대칭키 암호의 한계]                  [비대칭키 암호의 해결]

   Alice ──── Key(1) ──── Bob            Alice ──── ▶ Public Key(bob) ────> Bob
      │            ▲                             │                           │
      │            │                            암호화(Ciphertext)          복호화
      ▼            │                             │                           ▲
   Eve(도청자)    Key(1)                     Eve(공개키 획득)           Private Key(bob)
       (Key 탈취 시 전체 보안 붕괴)            (공개키만으로는 복호 불가)

   [문제] 안전한 Key 전달 채널 필요           [해결] 공개망에서 안전한 통신 가능
```

> **해설**: 위 다이어그램과 같이 대칭키는 '비밀'을 공유하는 것이 목적이라 우편물을 보내기 전에 열쇠를 먼저 배달해야 하는 딜레마가 있다. 반면, 비대칭키는 모두에게 공개된 '잠금장치(공개키)'는 있으나, 그것을 풀 수 있는 '열쇠(개인키)'는 소유자만 가지고 있어 열쇠 배달의 위험을 원천 차단한다.

📢 **섹션 요약 비유**: 비대칭키 암호화는 **'누구나 주소를 알 수 있지만(공개키), 우편물에 적힌 주소로 집을 찾아가 문을 여는 열쇠(개인키)는 집주인만 갖고 있는 것'**과 같습니다. 도둑이 주소는 알아도 실제 문을 열 수 없는 원리입니다.

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 동작 메커니즘
비대칭키 시스템은 수학적 난제(Mathematical Hard Problem)에 기반한 알고리즘, 키 쌍 생성기, 그리고 패딩(Padding) schemes으로 구성된다.

| 구성 요소 | 역할 및 내부 동작 | 프로토콜/표준 | 비유 |
|:---|:---|:---|:---|
| **Key Pair (Keys)** | **공개키 ($K_{pub}$)**: 암호화 및 서명 검증용. 모두에게 공개.<br>**개인키 ($K_{priv}$)**: 복호화 및 서명 생성용. 절대 유출 금지. | PKCS#1, SEC1 | 공개: 자물쇠 / 개인: 열쇠 |
| **Encryption (암호화)** | $C = E(K_{pub}, M)$: 평문 $M$을 공개키로 변환. 수학적 역연산을 방지하기 위해 **Random Padding(OAEP 등)** 사용. | RSA-OAEP | 투명한 봉투에 넣고 자물쇠 |
| **Decryption (복호화)** | $M = D(K_{priv}, C)$: 개인키로만 원본 복원. 수학적 인수분해/이산대수의 어려움에 의존. | RSA-PKCS#1 | 자물쇠 연 열쇠로 개봉 |
| **Digital Signature (서명)** | $Sig = Sign(K_{priv}, M)$: 해시값 생성 $\rightarrow$ 개인키로 암호화. **무결성 및 인증** 제공. | ECDSA, RSA-PSS | 도장 찍는 행위 |
| **Verification (검증)** | $Verify(K_{pub}, M, Sig)$: 공개키로 서명 검증. 문서가 변경되지 않았음을 증명. | - | 도장이 진짜인지 확인 |

### 2. ASCII: RSA (Rivest–Shamir–Adleman) 내부 구조
RSA는 **소인수분해(Integer Factorization)**의 어려움을 이용한다. 두 개의 거대한 소수 $p, q$의 곱 $n(=pq)$은 공개하지만, $n$에서 $p, q$를 찾는 것은 현실적으로 불가능하다.

```ascii
[RSA Key Generation Process]

  1. 두 소수 선택 (p, q)           2. 모듈러 계산 (n)          3. 오일러 파이 함수 (phi)
  ┌──────────────┐              ┌──────────────┐            ┌──────────────┐
  │ p = 61 (비밀)│              │ n = p * q    │            │ φ(n) = (p-1) │
  │ q = 53 (비밀)│ ── 곱셈 ──>  │ n = 3233    │ ─── 계산 ─>  │      * (q-1) │
  └──────────────┘              └──────────────┘            │  = 60 * 52   │
                                                           │  = 3120     │
                                                           └──────────────┘

  4. 공개키 지수 (e) 선택          5. 개인키 지수 (d) 계산      6. 키 배포
  ┌──────────────┐              ┌───────────────────┐      ┌──────────────┐
  │ 1 < e < φ(n) │              │ d * e ≡ 1 (mod φ) │      │ Public Key:  │
  │ gcd(e, φ)=1  │ ── 모듈러 ─> │ d = e^-1 mod φ   │ ──>  │ (e, n)       │
  │ e = 17       │   역원 계산   │ d = 2753         │      │ Private Key: │
  └──────────────┘              └───────────────────┘      │ (d, n)       │
                                                           └──────────────┘

   * 암호화: C = M^e mod n
   * 복호화: M = C^d mod n  (M^17)^2753 mod 3233 = M
```

> **해설**: $M^e \pmod n$ 연산은 빠르지만, $C$만 가지고 $M$을 찾는 것은 $d$를 모르면 불가능하다. $d$를 구하려면 $\phi(n)$을 알아야 하고, $\phi(n)$을 알려면 $n$을 소인수분해해야 한다. 2048비트 키의 경우 약 2조 년이 걸린다.

### 3. 핵심 알고리즘: ECC (Elliptic Curve Cryptography)
ECC는 **타원 곡선 이산 대수 문제(ECDLP: Elliptic Curve Discrete Logarithm Problem)**를 기반으로 한다.
*   **수식**: $y^2 = x^3 + ax + b$ (예: $y^2 = x^3 + 7$)
*   **장점**: RSA 2048비트와 동일한 보안 강도를 ECC 256비트가 제공한다. 연산량이 적어 전력 소모가 적다.

```ascii
[ECC 곱셈 연산 (점 덧셈의 반복)]

          P (Starting Point)
           *
          / \
         /   \
        /     \
   2P   *      \
         \     \
          \     \
           \     \
            3P    * (R = k*P)
   
   k = Private Key (예: d)
   P = Generator Point (공개)
   R = Public Key

   공개키(R)과 시작점(P)는 알지만,
   곱셈 횟수(k)를 유추하는 것은 불가능에 가깝다.
```

### 4. 실무 코드 (Python Snippet)
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# RSA 키 생성 (Private Key & Public Key)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# 암호화 (Public Key 사용)
ciphertext = public_key.encrypt(
    b"Secret Data from PE Exam",
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 복호화 (Private Key 사용)
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

📢 **섹션 요약 비유**: RSA는 **'거대한 숫자 퍼즐(소인수분해)'**을 맞추는 것이라 퍼즐 조각(키 크기)이 너무 커야 하지만, ECC는 **'복잡한 곡선 미로 위에서 특정 위치를 찾는 문제'**라 훨씬 적은 정보로도 미로를 탈출하기 어렵게 만드는 것과 같습니다.

+++

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. RSA vs ECC: 기술적 의사결정 매트릭스
현대 시스템 설계 시 두 알고리즘의 선택은 성능과 호환성의 Trade-off이다.

| 지표 | RSA (2048-bit) | ECC (P-256, 256-bit) | 분석 및 시사점 |
|:---|:---:|:---:|:---|
| **보안 강도** | 112-bit (Security Level) | 128-bit (Security Level) | ECC가 동일 키 크기 대비 더 높은 보안 강도 제공 (Quantum Resistance 관점에서도 우수). |
| **키 크기** | ~256 Bytes | ~32 Bytes | **ECC 승**: 대역폭 제약이 있는 IoT, 모바일 환경에서 저장소/전송 효율 극대화. |
| **암호화 속도** | 상대적으로 느림 | 매우 빠름 | **ECC 승**: 적은 모듈러 연산량으로 전력 소모 절감 (Smart Card, Blockchain Wallet). |
| **서명 속도** | 검증(Verify) 빠름 | 서명(Sign) 빠름 | **RSA 승**: 서버 검증 위주 환경(CA 인증서)에서는 RSA 검증 속도가 여전히 유리함. |
| **구현 복잡도** | 단순함 (구현 용이) | 복잡함 (Side-channel Attack 취약) | **RSA 승**: Side-channel 공격 방어 구현 난이도가 ECC가 더 높음. |
| **주요 용도** | TLS 인증서, 전자서명 | SSL/TLS, Bitcoin, 암호화폐, IoT | 레거시 시스템은 RSA, 신규 고성능 시스템은 ECC로 이동 중. |

### 2. 타 과목 융합 관점
*   **네트워크 (NW)**: **TLS (Transport Layer Security)** 핸드셰이크 과정에서 RSA는 키 교환용으로, ECC/DH는 세션 키 생성용으로 결합하여 사용된다. ECDHE(Elliptic Curve Diffie-Hellman Ephemeral)는 완벽한 전방 비밀성(Perfect Forward Secrecy)을 제공한다.
*   **데이터베이스 (DB)**: DB 암호화(TDE) 시 마스터 키 암호화에 ECC를 사용하여 스토리지 오버헤드를 줄이고 성능을 개선한다.
*   **보안 (Security)**: **SSH** 프로토콜 v2에서는 키 교환을 위해 ECDH 방식을 주로 사용하며, 공격자가 패킷을 캡처해도 나중에 키가 노출되도 과거 통신을 복호화 못하게 하는 PFS(Perfect Forward Secrecy)를 보장한다.

### 3. ASCII: 효율성 비교 시각화
```ascii
[RSA vs ECC: 128-bit Security Level 기준 자원 소모]

   [RSA 3072-bit]          [ECC 256-bit]
   ┌─────────────┐         ┌───────────┐
   │ ███████████│         │ ██        │  (Key Size)
   │████████████│         │           │
   │████████████│  크기    │           │
   │████████████│ 12배    │           │  작음 (저장공간/전송량 절약)
   │████████████│         │           │
   │████████████│         │           │
   └─────────────┘         └───────────┘
   
   [연산 부하]
   RSA:  지수 연산 (Modular Exponentiation) - 무거움
   ECC:  스칼라 곱셈 (Point Multiplication) - 가벼움
```

📢 **섹션 요약 비유**: RSA는 **'무거운 강철 금고'**라 튼튼하지만 설치하고 이동하기가 무겁고 번거롭습니다. 반면 ECC는 **'복합 재질로 만든 초경량 안전 가방'**처럼 금고만큼 튼튼하면서 훨씬 가볍고 휴대가 간편하여 최신 기기에 잘 맞습니다