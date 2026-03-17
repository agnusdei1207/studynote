+++
title = "난수 생성기 (TRNG, True Random Number Generator)"
date = "2026-03-14"
weight = 486
+++

# 난수 생성기 (TRNG, True Random Number Generator)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TRNG (True Random Number Generator, 진짜 난수 생성기)는 열 잡음(Thermal Noise), 샷 노이즈(Shot Noise), 클럭 지터(Jitter) 등 예측 불가능한 물리적 엔트로피(Entropy) 소스를 활용하여 비결정론적(Non-deterministic) 난수를 생성하는 하드웨어 모듈이다.
> 2. **가치**: 수학적 알고리즘에 기반한 PRNG(Pseudo-Random Number Generator)의 결정론적 한계와 주기성(Periodicity) 문제를 근본적으로 해결하여, 암호 키 생성, 디지털 서명, IV(Initialization Vector) 생성 등 보안의 '기밀성(Confidentiality)'과 '무결성(Integrity)'을 수학적으로 증명 가능한 수준으로 보장한다.
> 3. **융합**: SoC(System on Chip) 설계, HSM(Hardware Security Module), IoT(Internet of Things) 보안, 그리고 포스트 양자 암호(Post-Quantum Cryptography) 시스템의 핵심 루트 오브 트러스트(Root of Trust) 요소로 작용하며, 소프트웨어적 난수 생성기의 시드(Seed) 값을 공급하는 하부 구조로 융합된다.

---

### Ⅰ. 개요 (Context & Background)

**난수 생성기(Random Number Generator, RNG)**는 컴퓨터 시스템에서 불확실성을 구현하는 유일한 수단이다. 그러나 현대의 디지털 컴퓨팅 아키텍처는 기본적으로 **결정론적(Deterministic)** 머신으로, 동일한 입력과 초기 상태(State)에 대해 항상 동일한 결과를 도출한다. 이러한 환경에서 순수한 소프트웨어적 알고리즘만으로는 '진짜 무작위성'을 구현할 수 없으며, 이는 `PRNG (Pseudo-Random Number Generator, 의사 난수 생성기)`가 가진 근본적인 취약점이다.

`TRNG (True Random Number Generator, 진짜 난수 생성기)`는 이러한 논리적 회로의 한계를 극복하기 위해 자연계의 **물리적 현상(Physical Phenomena)**을 관측함으로써, 외부에서 예측 불가능한 비트열을 생성하는 하드웨어 장치이다. 이는 단순히 '복잡한 수학식'이 아니라 '물리적 불확실성'을 바이너리 데이터로 사상(Mapping)하는 과정이므로, 이론적으로 역추적(Reverse Engineering)이 불가능하다는 것이 핵심 차별점이다.

**💡 비유 (Analogy)**:
PRNG는 거대한 전화번호부를 암기하고 적당히 페이지를 넘기며 번호를 읊조리는 '계산기'라면, TRNG는 주사위 눈의 미세한 홈, 바람의 흐름, 던지는 손의 떨림 등 모든 물리적 변수를 그대로 반영하여 실제로 주사위를 굴리는 '물리적 사건' 그 자체와 같다. 전자는 패턴을 파악하면 다음 숫자를 맞출 수 있지만, 후자는 우주의 상태를 완벽히 알지 못하는 한 다음 결과를 알 수 없다.

**등장 배경 (Background)**:
1.  **보안 사고의 근본적 원인**: 초기 웹 서버나 암호화 시스템은 시스템 시간(System Timestamp)이나 프로세스 ID 등을 PRNG의 시드(Seed)로 사용했으나, 이는 공격자에게 추정 가능한 범위 내에 있어 수많은 SSL/TLS 보안 취약점(Debian OpenSSL 사건 등)을 야기함.
2.  **고도화된 공격 기법**: 공격자가 난수의 상태(State)를 복구하면 과거 및 미래의 모든 암호 키가 유출되는 상태 복구(State Recovery) 공격이 등장함에 따라, 내부 상태를 유추할 수 없는 비결정론적 엔트로피의 필요성 대두.
3.  **국제 보안 표준의 강화**: NIST(미국 국립표준기술연구소)의 SP 800-90B나 FIPS 140-2(Federal Information Processing Standard)와 같은 인증 기준에서 엔트로피 소스의 품질과 물리적 무작위성 검증을 의무화함.

📢 **섹션 요약 비유**: 마치 지구상의 날씨를 예측하기 위해 복잡한 수식을 사용하는 것이 아니라(결정론적), 실제 대기의 난류를 관측하여 데이터를 수집하는 것(비결정론적)과 같습니다. 규칙이 존재하지 않는 자연 그 자체를 데이터화하는 것이 핵심입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

`TRNG`는 단순한 센서가 아니라, **'엔트로피 수집 → 정제 → 검증'**의 3단계 파이프라인을 갖는 정교한 하드웨어 시스템이다. 일반적으로 아날로그 물리 현상을 디지털 신호로 변환하고, 이 신호의 편향(Bias)을 제거하며, 최종적으로 통계적 검증을 거쳐 난수를 출력한다.

#### 1. TRNG 구성 요소 상세 분석

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 핵심 기술 (Protocol/Tech) | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **Entropy Source** | 무작위성의 근원 공급 | 반도체의 열적 요동(Thermal Noise), 광전 효과, 양자 터널링 등 아날로그 신호 발생 | 저항기 잡음, 아발란치 다이오드 | 거칠게 요동치는 파도 |
| **Digitizer (ADC)** | 아날로그-디지털 변환 | 연속적인 아날로그 신호를 `Comparator`를 통해 0 또는 1의 디지털 비트로 샘플링 | Sampling Theory, Schmitt Trigger | 파도의 높이를 '높음/낮음'으로 기록 |
| **Entropy Accumulator** | 엔트로피 풀링(Pooling) | 생성된 비트를 LFSR(Linear Feedback Shift Register)이나 해시 함수를 이용해 축적 | XOR Operation, Buffer Management | 여러 개의 작은 물통을 모아 큰 저수지 |
| **Post-Processor** | 편향성 제거 (Debiasing) | 물리적 오차로 인한 0/1 비대칭을 교정 (Von Neumann Corrector, Hashing) | Von Neumann Method, SHA-256 | 찌그러진 주사위를 던져서 공정하게 보정 |
| **Health Monitor** | 실시간 품질 관리 | 출력 비트의 연속성, 반복 패턴을 감시하고 공격 여부나 노후화 탐지 | NIST SP 800-90B Tests | 식품 검사관이 위생 상태를 실시간 점검 |

#### 2. 시스템 아키텍처 및 데이터 흐름

아래 다이어그램은 물리적 노이즈가 최종 난수 비트로 변환되는 과정을 도식화한 것이다.

```text
  [ Physical Entropy Source ]
   ( e.g., Thermal Noise in Resistor )
             |
             v
  +-----------------------------+
  |  Analog Signal Conditioning |  <-- 증폭기(Amp) 및 필터(Filter)
  +-----------------------------+
             |
             v
  +-----------------------------+
  |  Sampling & Digitization    |  <-- 고속 클럭에 의한 샘플링 (ADC)
  |  (Unconditioned Bits)       |      (0과 1의 비율이 불균형할 수 있음)
  +-----------------------------+
             |
             v
  [   Entropy Accumulator Pool  ]  <-- LFSR 등을 통해 비트열 혼합
             |
             v
  [   Post-Processing Module    ]  <-- Von Neumann or Cryptographic Hash
  |  (Conditioning Component)   |      (편향 제거 및 재분배)
  +-----------------------------+
             |
             v
  [   Self-Test / FIPS 140 Test ]  <-- Continuous Random Number Generator Test
             |
             v
  [       TRNG Output Port      ]  <-- OS Kernel Random Pool (/dev/random)
```

**다이어그램 해설**:
1.  **물리적 수집**: 엔트로피 소스는 매우 미세한 아날로그 신호를 생성하므로, 이를 증폭하고 고주파 노이즈를 필터링하여 전기적인 신호로 정제한다.
2.  **디지털화(Quantization)**: `ADC (Analog-to-Digital Converter)`는 기준 전압(Vref)과 비교하여 순간적인 전압 레벨을 0과 1로 판별한다. 이 단계에서 나온 비트(Raw Bits)는 물리적 특성상 1이 많거나 0이 많은 편향(Bias)을 가질 수 있다.
3.  **후처리(Post-Processing)**: Von Neumann 방식(연속된 두 비트가 01이면 0, 10이면 1, 00이나 11은 폐기)을 사용하거나 암호학적 해시 함수(SHA-2 등)를 적용하여 입력 비트열의 엔트로피를 최대화하고 출력을 균일하게 분포시킨다. 이 과정은 시스템의 엔트로피를 '증강'하는 효과를 가진다.
4.  **건전성 검증(Health Check)**: `FIPS 140-2` 표준에 따라, 생성된 난수가 연속된 0이나 1이 너무 많이 나오는지 등을 실시간으로 모니터링한다. 실패 시 즉시 난수 생성을 중단하고 시스템에 경고를 발생한다.

#### 3. 핵심 동작 알고리즘 (Von Neumann Extractor)

물리적 소스에서 추출한 비트 $X_1, X_2$가 있다고 가정할 때, 편향을 제거하는 대표적인 코드 로직은 다음과 같다.

```python
# Von Neumann Corrector Example
# Input: biased_bitstream (from ADC)
# Output: debiased_bitstream

def extract_bits(bitstream):
    output_buffer = []
    i = 0
    while i < len(bitstream) - 1:
        b1 = bitstream[i]
        b2 = bitstream[i+1]
        
        if b1 != b2:  # 01 또는 10인 경우만 채택 (확률 50:50 보장)
            output_buffer.append(b1) # 01 -> 0, 10 -> 1
        
        # 00 또는 11인 경우에는 폐기 (편향 제거)
        i += 2
    
    return output_buffer
```
이 알고리즘은 입력 비트가 0일 확률이 $p \neq 0.5$라고 하더라도, 연속된 두 비트가 다를 확률은 $2p(1-p)$로 계산되며, 이때 0과 1이 나올 확률이 정확히 1/2로 수렴한다는 수학적 원리를 이용한다.

📢 **섹션 요약 비유**: 시끄러운 시장의 소음(엔트로피 소스)을 녹음하여 디지털 파일(비트)로 변환하고, 노이즈 캔슬링 기술(포스트 프로세서)을 통해 특정 소리만 걸러내거나 음량을 균일하게 조정한 뒤, 마지막으로 음질이 손상되지 않았는지 검사하는(헬스 모니터) 고성능 오디오 장비와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

난수 생성 기술은 시스템의 보안 요구 사항(Security Requirement)과 성능 요구 사항(Performance Requirement)에 따라 `PRNG`와 `TRNG`가 상호 보완적으로 융합되어 사용된다.

#### 1. 난수 생성 방식 심층 기술 비교

| 구분 (Criteria) | PRNG (Pseudo-RNG) | TRNG (True-RNG) | Hybrid (DRBG) |
|:---:|:---|:---|:---|
| **엔트로피 소스** | 수학적 알고리즘 (AES, SHA 등) | 물리적 현상 (열, 광, 양자) | TRNG Seed + 알고리즘 |
| **결정론성 (Determinism)** | 결정론적 (Seed값에 종속) | **비결정론적 (Non-deterministic)** | 결정론적 (재현 가능 시) |
| **속도/성능 (TPS)** | 매우 빠름 (GB/s급 가능) | 느림 (수 ~ 수백 kb/s) | 빠름 (PRNG에 가깝) |
| **주기성 (Periodicity)** | 존재함 ($2^{n}$ 후 반복) | **없음 (Infinite)** | Seed 갱신 주기에 따름 |
| **주요 용도** | 시뮬레이션, 게임, 일반 암호화 | **마스터 키 생성, 인증서, Nonce** | TLS 세션 키, 일반 보안 통신 |
| **공격 취약점** | State Recovery, Seed Prediction | **(이론적) 물리적 감청 및 노이즈 조작** | Seed 탈취 시 PRNG와 동일 |

#### 2. 과목 융합 분석 (Interdisciplinary Synergy)

**A. 하드웨어 보안 (Hardware Security) & PUF (Physical Unclonable Function)**
- **상관관계**: `PUF`는 칩 제조 공정의 미세한 물리적 편차를 이용해 고유한 ID를 생성하는 기술이다. TRNG와 마찬가지로 물리적 불확실성을 활용하지만, TRNG가 '무작위성(Randomness)'에 집중한다면, PUF는 '고유성(Uniqueness)'과 '복제 불가능성(Unclonability)'에 집중한다.
- **융합 효과**: PUF에서 생성된 응답(Response)을 TRNG의 시드(Seed)나 엔트로피 소스로 활용하여, 하드웨어 마다 고유하고 예측 불가능한 난수 시스템을 구축할 수 있다.

**B. 통신 네트워크 (Communication Network) & SSL/TLS**
- **상관관계**: SSL/TLS 핸드셰이크 과정에서 클라이언트와 서버는 `Random`(난수)을 교환하여 Pre-Master Secret을 생성한다. 이때 난수의 예측 가능성(Predictability)은 전체 세션의 보안을 무력화시킨다.
- **융합 효과**: 서버의 `/dev/random`(Linux)은 TRNG를 기반으로 충분한 엔트로피가 확보되지 않으면 Blocking 되거나 PRNG로 Fallback 되는데, 고성능 TRNG는 웹 서버의 세션 생성 지연(Latency)을 줄이면서도 보안성을 보장하는 핵심 인프라가 된다.

**C. 양자 암호 (Quantum Cryptography)**
- **상관관계**: `QRNG (Quantum RNG)`는 광자의 편광 상태나 빔 스플리터를 통과한 경로 선택 등 양자적 불확정성(Heisenberg Uncertainty Principle)을 이용한다.
- **융합 효과**: 이는 고전역학적 TRNG(열 잡음 등