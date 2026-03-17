+++
title = "543. 양자 내성 암호 가속기 (PQC Accelerator)"
date = "2026-03-14"
weight = 543
+++

# 543. 양자 내성 암호 가속기 (PQC Accelerator)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **PQC (Post-Quantum Cryptography)** 알고리즘은 그 수학적 복잡도(격자 기반 다항식 연산 등)로 인해 기존 범용 **CPU (Central Processing Unit)**로는 처리하기 불가능에 가까운 오버헤드를 유발합니다. 이를 해결하기 위해 SoC 내부에 PQC 연산만을 전담하는 하드웨어 가속 **IP (Intellectual Property)**를 탑재하여, 양자 컴퓨터 시대에도 안전한 암호 통신을 실시간으로 수행하는 아키텍처입니다.
> 2. **가치**: **SNDL (Store Now, Decrypt Later)** 공격에 대비하여 기존 **RSA (Rivest-Shamir-Adleman)**나 **ECC (Elliptic Curve Cryptography)**를 대체해야 하지만, PQC의 키 크기는 킬로바이트(KB) 단위이고 연산량은 기존 대비 100배 이상입니다. PQC 가속기는 이러한 **NTT (Number Theoretic Transform)**와 다항식 연산을 **ASIC (Application-Specific Integrated Circuit)** 레벨에서 처리하여 **지연 시간(Latency)**을 µs(마이크로초) 단위로 줄이고 에너지 효율을 극대화합니다.
> 3. **융합**: 단순한 암호화 하드웨어를 넘어, 네트워크(하이브리드 키 교환), 보안(HSM, Secure Enclave), 그리고 미래의 **QPU (Quantum Processing Unit)**와의 연동까지 고려해야 하는 차세대 보안 인프라의 핵심 심장부입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**PQC (Post-Quantum Cryptography) 가속기**란, 양자 컴퓨터의 **쇼어 알고리즘(Shor's Algorithm)**과 같은 양자 알고리즘에 의해 기존 공개키 암호 체계가 붕괴하는 것에 대비하여, NIST가 표준화한 새로운 암호 알고리즘(격자 기반, 코드 기반, 다변량 등)의 처리 속도를 획기적으로 높이기 위해 설계된 전용 하드웨어 모듈입니다. 이는 소프트웨어적인 최적화를 넘어, 명령어 세트 아키텍처(ISA) 레벨에서부터 연산 유닛을 재정의하는 **하드웨어 가속(Hardware Acceleration)** 기술입니다.

#### 2. 등장 배경: Y2Q와 알고리즘 대전환
인터넷 보안의 근간이던 RSA와 ECC는 양자 컴퓨터 앞에서 무력화합니다. 이에 대응하고자 미국 **NIST (National Institute of Standards and Technology)**는 2016년부터 **PQC 표준화 경쟁**을 주도했으며, 2022년~2024년에 걸쳐 격자 기반 알고리즘인 **Kyber**와 **Dilithium** 등을 표준으로 채택했습니다. 그러나 이 알고리즘들은 기존 대비 키 크기가 10~100배 더 크고(수 KB), 모듈러 곱셈이 아닌 고차원 다항식 곱셈을 요구합니다. 이를 일반 CPU에서 소프트웨어로 구현할 경우 **TPS (Transactions Per Second)**가 급감하고 **전력 소모(Power Consumption)**가 폭증하여, 사물 인터넷(IoT)이나 모바일 기기에서의 사용이 사실상 불가능해졌습니다. 따라서 암호화 연산을 CPU에서 분리(Offloading)하여 전담 처리하는 전용 가속기의 도입이 필수적인 상황이 되었습니다.

#### 3. 기술적 요구사항의 변화
기존 암호 가속기(Coprocessor)가 1024비트나 2048비트 정수의 모듈러 지수 연산에 최적화되어 있었다면, PQC 가속기는 수천 개의 계수(Coefficient)를 가진 다항식의 합성곱(Convolution) 연산과 매트릭스 연산에 최적화되어야 합니다. 또한, **Crypto-Agility(암호 유연성)**를 확보하여, 향후 새로운 알고리즘이나 표준이 변경되더라도 펌웨어 업데이트만으로 대응할 수 있는 **FPGA (Field-Programmable Gate Array)** 혼합 구조나 마이크로코드 방식이 요구됩니다.

> **📢 섹션 요약 비유**: 마치 옛날 화살을 막기 위해 만든 얇은 판금 갑옷(RSA)가 돌려쓰는 소총탄(양자 컴퓨터) 앞에서는 종잇장처럼 찢겨버리는 것과 같습니다. 이를 막기 위해 우리는 두꺼운 강철과 흙섞은 벽돌로 요새(PQC)를 새로 지어야 하지만, 무게가 너무 무거워 사람이 직접 성문을 여닫을 수 없게 되었습니다. 그래서 설치한 것이 "이 거대한 성문을 전기로 0.1초 만에 열어주는 자동 문 opener(PQC 가속기)"입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. PQC 가속기의 내부 구조 및 주요 파라미터
PQC 가속기는 단순한 수학 연산기가 아니라, 대용량 데이터를 버스(Bus) 병목 없이 처리하기 위한 메모리 통합형 아키텍처를 가집니다. 특히 **NIST PQC** 표준인 Kyber(Dilithium)는 격자(Lattice) 기반 **LWE (Learning With Errors)** 문제를 기반으로 하므로, 이를 효율적으로 계산하는 것이 핵심입니다.

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 주요 프로토콜/특징 | 비유 |
|:---|:---|:---|:---|:---|
| **NTT Engine** | Number Theoretic Transform Unit | 다항식 곱셈의 복잡도를 $O(N^2)$에서 $O(N log N)$으로 줄이는 핵심 가속부. FFT와 유사한 나비(Butterfly) 연산 수행. | Modular Arithmetic (mod q) | 수천 개의 숫자 더하기를 한 방에 처리하는 병렬 계산기 |
| **Vector ALU** | Vector Arithmetic Logic Unit | PQC 키 생성 시 필요한 벡터 덧셈, 스칼라 곱셈 및 노이즈(Error) 주입 연산 담당. | SIMD (Single Instruction Multiple Data) | 거대한 미로 벽을 동시에 여러 개가 건설하는 건설 로봇 팔 |
| **Keccak Core** | SHA-3 / Keccak Sponge Function | 암호문의 무결성 검증, XOF (Extendable-Output Function)를 통한 키 스트림 생성 및 난수 재료 제공. | FIPS 202 | 바다를 휘저어 물결(난수)을 만드는 믹서기 |
| **CSPRNG** | Cryptographically Secure Pseudo-RNG | **TRNG (True Random Number Generator)**와 연동하여 예측 불가능한 시드(Seed) 생성 및 에러(Error) 샘플링. | NIST SP 800-90A | 주사위를 던질 때 나오는 무작위 눈금 생성기 |
| **Local Memory** | Multi-Banked SRAM / L1 Cache | 키 크기가 KB 단위이므로 외부 **DRAM (Dynamic RAM)** 접근을 최소화하기 위한 내부 버퍼. | High Bandwidth Memory (HBM) 기술 적용 | 주방장이 재료를 꺼내 쓰기 쉽게 옆에 둔 넓은 도마 |

#### 2. 아키텍처 데이터 흐름도 (Data Flow Diagram)

PQC 가속기의 연산 과정은 **"KeyGen -> Encaps/Decaps"** 또는 **"Sign -> Verify"**의 흐름을 따르며, 이 과정에서 CPU와의 인터랙션이 발생합니다.

```text
      [ Host CPU (ARM/x86) ]               [ PQC Accelerator IP (SoC) ]
             │                                   │
      1. 요청(REQ)                          2. 명령 디코딩
      (Plain Text, PubKey)        ──────────────▶  (Control Logic)
             │                                   │
             │                                   ▼
             │                          ┌──────────────────────┐
             │                          │  Internal Memory Bus │
             │                          └───────────┬──────────┘
             │                                      │
             │           ┌──────────────────────────┼──────────────────────┐
             │           │                          │                      │
             │           ▼                          ▼                      ▼
             │    ┌─────────────┐          ┌──────────────┐      ┌───────────────┐
             │    │   NTT Unit  │          │  Vector ALU  │      │  Keccak/SHA3  │
             │    │ (Fast Poly  │◀─▶       │  (Mat/Vec    │      │  (Hash/PRNG)  │
             │    │   Multiply) │          │   Ops)       │      │               │
             │    └──────┬──────┘          └──────┬───────┘      └───────┬───────┘
             │           │                        │                      │
             │           └────────────────────────┼──────────────────────┘
             │                                    │
             │                           3. 하드웨어 연산 수행 (Pipeline)
             │                           * Poly Mul * Matrix Ops * Hashing
             │                                    │
             │                                    ▼
             │                           ┌──────────────────────┐
             │                           │ Result FIFO / Buffer │
             │                           └───────────┬──────────┘
             │                                        │
             ◀─────────────────────────────────────────┘
     6. 인터럽트(IRQ) / 결과 확인
        (Cipher Text / Signature)
```

**[다이어그램 해설]**
위 다이어그램은 **CPU-Coaccelerator** 구조를 보여줍니다.
1.  **명령 전달**: CPU는 시스템 버스(예: **AXI (Advanced eXtensible Interface)**)를 통해 평문(Plain Text)과 공개키(Public Key)를 가속기의 내부 메모리로 전송하고 "연산 시작" 명령을 뱉습니다.
2.  **독립 연산**: 가속기는 CPU의 개입 없이 **NTT 유닛**에서 다항식을 주파수 영역으로 변환하여 곱셈을 수행하고, **Keccak 코어**에서 암호학적 해시를 생성하여 결과값을 섞습니다. 이때 내부 **SRAM**을 활용하므로 외부 메모리 대역폭을 낭비하지 않습니다.
3.  **결회 회신**: 연산이 완료되면 CPU에게 인터럽트(Interrupt)를 발생시키거나, 메모리 맵드 I/O(MMIO) 레지스터 플래그를 세워 완료를 알립니다. CPU는 단순히 결과만 가져가서 네트워크 카드(NIC)로 전송하면 됩니다.

#### 3. 핵심 알고리즘: NTT (Number Theoretic Transform) 동작 원리
PQC의 성능을 결정짓는 가장 중요한 요소는 다항식 곱셈의 속도입니다. 이를 위해 **NTT**를 사용합니다.

$$ C(x) = A(x) \cdot B(x) \pmod{x^n-1, q} $$

위와 같은 다항식 곱셈을 직접 수행하면 $O(N^2)$의 시간이 걸리지만, NTT를 통해 점별 곱셈(Point-wise Multiplication)으로 변환하면 $O(N \log N)$에 수행할 수 있습니다.

```text
[ 일반 곱셈 vs NTT 가속 곱셈 ]

Input: 다항식 A(x)와 B(x) (차수 n=256)

CASE 1: Schoolbook Multiplication (CPU Software Loop)
- 연산: 이중 루프 (256 * 256) = 65,536 회의 곱셈과 모듈러 연산
- 병목: 느린 속도, CPU 파이프라인 스톨(Stall) 유발

CASE 2: NTT Based (Hardware Accelerator)
Step 1. NTT(A) -> A' (Frequency Domain)
Step 2. NTT(B) -> B'
Step 3. C'[i] = A'[i] * B'[i] mod q  (Vector 곱셈 256회)
Step 4. INTT(C') -> C (Polynomial Domain)
- 병목: 거의 없음. 하드웨어 스테이지 파이프라이닝으로 처리.
```

> **📢 섹션 요약 비유**: 마치 레고 블록 수십 개를 하나하나 맞춰 탑을 쌓는 대신(일반 연산), 레고 탑을 통째로 뒤집어서 필요한 부분만 교체하고 다시 뒤집는 방식(NTT 변환)을 사용하여 작업 시간을 획기적으로 단축하는 것과 같습니다. 가속기는 이 뒤집고(변환) 붙이고(곱셈) 다시 뒤집는(역변환) 과정을 로봇 팔이 순식간에 처리하도록 설계된 공장입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 암호 체계 기술 비교 분석표

PQC 가속기 도입의 당위성을 확인하기 위해 기존 방식과의 기술적/정량적 차이를 분석합니다.

| 비교 항목 | 기존 공개키 암호 (RSA/ECC) | 양자 내성 암호 (Lattice-based PQC) | 가속기 설계 시 영향 |
|:---|:---|:---|:---|
| **수학적 기반** | 소인수분해 문제, 이산로그 문제 | **LWE (Learning With Errors)**, 격자(Lattice) 벡터 문제 | 정수 곱셈 유닛 → **다항식/벡터 곱셈 유닛**으로 교체 필요 |
| **키 사이즈** | 공개키: 256~4096 bit (매우 작음) | **공개키: 800 Bytes ~ 3 KB (매우 큼)** | **On-Chip SRAM** 크기 대폭 확보 필수 (캐시 적중률 중요) |
| **연산 복잡도** | 모듈러 지수 연산 ($M^e \pmod N$) | 다항식 곱셈, 행렬 곱셈, 샘플링 연산 | 병렬 처리 가능한 **SIMD** 아키텍처가 필수적 |
| **양자 내성** | **취약함** (쇼어 알고리즘으로 O(log N) 해독) | **안전함** (단사(SIS) 문제 등으로 NP-hard 문제와 연관) | 새로운 수학적 구조를 하드웨어로 원천 지원해야 함 |

#### 2. 타 기술 영역과의 융합 (Synergy)

**1) 네트워크 (Network Security): 하이브리드 키 교환 (Hybrid Key Exchange)**
PQC 가속기는 단독으로 쓰이기보다 기존의 **