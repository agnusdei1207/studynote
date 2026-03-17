+++
title = "NW #13 대역폭 (Bandwidth) 및 대역폭-효율성 관계"
date = "2026-03-14"
[extra]
categories = "studynote-network"
+++

# NW #13 대역폭 (Bandwidth) 및 대역폭-효율성 관계

> **핵심 인사이트**
> 1. **본질**: 대역폭은 통신 채널의 **물리적 주파수 범위(Hz)**와 그에 따른 **정보 전송 용량(bps)**을 의미하며, 디지털 통신의 성능을 결정짓는 가장 기초적인 자원이다.
> 2. **가치**: 한정된 주파수 자원(스펙트럼) 내에서 최대 전송 속도를 높이기 위해 변조 방식과 **MIMO(Multiple-Input Multiple-Output)** 기술을 활용하여 **대역폭 효율성(Spectral Efficiency, bps/Hz)**을 극대화하는 것이 핵심 경쟁력이다.
> 3. **융합**: **Shannon-Hartley 정리**에 기반하여 신호 대 잡음비(**SNR**)와 대역폭의 상충 관계를 최적화하며, 이는 5G/6G 이동통신, Wi-Fi 7, 위성 통신 등 광대역 네트워크 설계의 근간이 된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념의 이중성과 정의
**대역폭 (Bandwidth)**은 통신 공학에서 가장 빈번하게 사용되면서도 오해를 불러일으키기 쉬운 용어다. 물리적 관점과 정보 이론적 관점에서 두 가지 의미를 가진다.

1.  **아날로그 대역폭 (Analog Bandwidth)**:
    신호가 포함하고 있는 주파수 성분의 범위를 나타내며, 단위는 **Hz (Hertz)**이다. 신호의 상한 주파수($f_{high}$)와 하한 주파수($f_{low}$)의 차이($B = f_{high} - f_{low}$)로 정의된다. 이는 **'도로의 물리적 폭(차선 수)'**에 해당한다.
2.  **디지털 대역폭 (Digital Bandwidth / Data Rate)**:
    단위 시간당 전송할 수 있는 데이터의 양을 의미하며, 단위는 **bps (bits per second)**이다. 이는 **'해당 도로를 1초 동안 통과할 수 있는 차량의 총 대수'**에 해당한다.

이 두 개념은 **Nyquist**와 **Shannon**의 이론에 의해 연결되며, 채널의 잡음 환경과 변조 기술에 따라 아날로그 대역폭 1Hz당 몇 비트를 전송할 수 있는지가 결정된다.

#### 2. 등장 배경과 진화
-   **유선 전화기 시대**: 음성 주파수 대역(300Hz~3400Hz)만으로도 아날로그 통신이 충분했으나, 모뎀(Modulator/Demodulator)의 등장으로 이 제한된 구리선(Copper Wire) 위에 디지털 데이터를 얹어야 하는 필요성이 대두되었다.
-   **무선 데이터 시대**: 스펙트럼(주파수 자원)은 한정되어 있고 데이터 요구량은 폭증함에 따라, 단순히 주파수 대역을 넓히는 것(물리적 확장)에 한계가 발생했다. 이에 따라 **'주파수 효율성(Spectral Efficiency)'**을 높이는 기술(변조, 다중화, MIMO)이 통신 기사(Engineer)들의 주된 연구 대상이 되었다.

#### 3. ASCII 다이어그램: 도메인별 대역폭 시각화

```ascii
[ 1. Analog Signal View (Frequency Domain) ]    [ 2. Digital Data View (Time Domain) ]
       Power (Amplitude)                               Data Rate
         ^                                              | 10110010 |
         |  Bandwidth (B = f2 - f1)                    |----------| 1 sec
         |      <------------->                        |  R bps   |
         |      ____________                           |          |
    -----+-----|            |-----+----> f(Hz)          +----------+
          f_low  (Signal)   f_high                     Capacity
              
    [ 3. Relationship: The Pipe Analogy ]
      
      Analog B (Hz) = Pipe Diameter (Physical Width)
      Digital R (bps) = Water Flow (Volume per second)
      Efficiency (bps/Hz) = Pressure / Fluid Viscosity
```
*(해설: 위 다이어그램은 아날로그 영역에서의 대역폭이 주파수 축상의 거리(Hz)임을 보여주고, 디지털 영역에서의 대역폭이 시간축 상의 비트 밀도(bps)임을 보여준다. 파이프 비유에서는 아날로그 대역폭이 파이프의 굵기를 결정하고, 효율성(압력)에 따라 유량(데이터 전송률)이 결정됨을 암시한다.)*

📢 **섹션 요약 비유**: 대역폭 확보는 마치 **복잡한 도심을 가로지르는 고가도로(高架道路)를 건설하는 것**과 같습니다. 도로를 물리적으로 넓게 내는 것(아날로그 대역폭 증가)도 중요하지만, 이미 건설된 도로에서 차량 간격을 좁혀 더 많은 차량이 통과하게 하는 스마트 신호 시스템(변조 및 효율성 기술)이 병목을 해결하는 핵심입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 대역폭 결정의 핵심 공식 및 구성 요소

대역폭과 전송 속도의 관계는 다음의 두 가지 핵심 이론으로 설명된다.

1.  **Nyquist 대역폭 공식 (잡음 없는 채널)**:
    $$C = 2 \times B \times \log_2(V)$$
    - $C$: 최대 데이터 전송률 (bps)
    - $B$: 대역폭 (Hz)
    - $V$: 신호 레벨 수 (변조 차원수, 예: 2진법이면 2)
    *=> 한계: 잡음이 없는 이상적인 환경 가정.*

2.  **Shannon-Hartley 정리 (잡음 있는 채널)**:
    $$C = B \times \log_2(1 + \text{SNR})$$
    - $\text{SNR}$: 신호 대 잡음비 (Signal-to-Noise Ratio)
    *=> 실무 통신 환경의 절대적인 물리적 한계를 규정.*

#### 2. 핵심 구성 요소 및 파라미터 비교

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Mechanism) | 관련 파라미터 (Metrics) |
|:---:|:---|:---|:---|
| **Symbol Rate** | 1초당 변조 신호의 변경 횟수 | **Baud Rate**라고도 하며, 대역폭 $B$에 비례 ($R_s \approx B$) | [Baud], Symbols/sec |
| **Modulation** | 비트를 심볼로 매핑 | 1개 심볼이 담는 비트 수($\log_2 V$)를 늘려 대역폭 효율 증대 | **QAM (Quadrature Amplitude Modulation)**, QPSK, 256QAM |
| **Noise ($N$)** | 신호 품질 저하 요인 | 열잡음(Thermal Noise), 간섭(Interference)으로 데이터 복원 방해 | $N_0$ (Noise Density), $\text{dBm}$ |
| **SNR** | 채널의 품질 지수 | $S/N$ 비율이 높을수록 고차 변조 가능, 전송 거리와 반비례 | **dB (Decibel)** |
| **Error Control** | 에러 복원 및 신뢰성 확보 | 전송 효율성을 희생하고 **FEC (Forward Error Correction)** 비트 추가 | BER (Bit Error Rate), Overhead % |

#### 3. 대역폭 효율성 (Spectral Efficiency) 심층 분석

**대역폭 효율성($\eta$)**은 단위 주파수당 전송 가능한 데이터량을 의미하며, 단위는 **bps/Hz**이다.
$$\eta = \frac{R}{B} \quad [\text{bps/Hz}]$$

이 효율성을 높이는 기술적 메커니즘은 다음과 같다.
① **고차 변조 (High-order Modulation)**: 1개 심볼이 2비트(QPSK)에서 8비트(256QAM), 10비트(1024QAM) 등을 담도록 위상(Phase)과 진폭(Amplitude)을 세분화한다.
② **다중 안테나 (MIMO)**: **Spatial Multiplexing(공간 다중화)**을 통해 동일한 주파수 자원을 공간적으로 분리하여 병렬 전송, 효율성을 안테나 수에 비례해 증대시킨다.
③ **Coding Gain**: 강력한 **LDPC (Low-Density Parity-Check)**나 **Polar Code**를 사용하여 낮은 SNR에서도 동작 가능하게 하여 유효 효율성을 높인다.

#### 4. ASCII 다이어그램: 변조 방식에 따른 비트 효율성 차이

```ascii
[ Concept: Symbol Packing per Hz ]

Case A: BPSK (Binary Phase Shift Keying) - Efficiency = 1 bps/Hz
Time  ---->  Symbol 1   Symbol 2   Symbol 3   Symbol 4
Bit    ---->   [ 0  ]    [ 1  ]    [ 1  ]    [ 0  ]
             (1 bit)    (1 bit)    (1 bit)    (1 bit)
             Total: 4 bits / 4 symbols = 1.0 bps/symbol

Case B: 256-QAM (High Efficiency) - Efficiency = 8 bps/Hz
Time  ---->  Symbol 1           Symbol 2
Bit    ---->   [ 00110110 ]      [ 11110001 ]
             (8 bits packed)    (8 bits packed)
             Total: 16 bits / 2 symbols = 8.0 bps/symbol

[ Visual Mapping: Constellation Diagram ]
        Q
   0100 | 0101  (Higher Density = Higher BER Risk)
 -------+------- I
   1100 | 1101
        Q
```
*(해설: BPSK는 1개 심볼당 1비트를 전송하는 반면, 256-QAM은 1개 심볼당 8비트를 전송하여 대역폭 효율이 8배 높다. 다만, 오른쪽 Constellation Diagram(성상도)에서 점들이 빽빽해지므로, 잡음(Noise)이 조금만 섞여도 점의 영역이 겹쳐 오해석(Inter-symbol Interference)이 발생할 확률이 높아진다. 이것이 바로 '효율성과 신뢰성의 트레이드오프'다.)*

📢 **섹션 요약 비유**: 대역폭 효율성을 높이는 것은 **한 대의 버스(심볼)에 태우는 승객(비트)의 수를 늘리는 것**과 같습니다. 버스 하나에 10명을 태우는 것(QPSK)보다 100명을 태우는 것(256QAM)이 더 효율적이지만, 버스가 너무 비좁아지면 승객끼리 부딪혀서 넘어지는 사고(에러)가 발생하기 쉬워진다는 위험 부담이 따릅니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 대역폭 vs. 처리량 (Throughput) vs. Goodput

많은 실무자가 대역폭과 처리량을 혼동하지만, 시스템 아키텍처 관점에서는 명확히 구분해야 한다.

| 구분 | 대역폭 (Bandwidth) | 처리량 (Throughput) | 유효 처리량 (Goodput) |
|:---:|:---|:---|:---|
| **정의** | 채널의 이론적 최대 전송 능력 (Layer 1/2) | 실제 네트워크 카드가 주고받는 속도 | 최종 애플리케이션 계층(Layer 7)에서 인지하는 속도 |
| **단위** | bps (Raw Bit Rate) | bps (Frame Rate) | MB/s, GB/s |
| **감소 요인** | - | **Overhead**(헤더, 토큰 버킷, 충돌), **Retransmission**(ARQ), **FEC**(정정 부호) | **Protocol Overhead**(TCP/IP Header), **Flow Control**(Window Size), 압축률 |
| **수식** | $R = B \times \log_2(1+\text{SNR})$ | $T = R \times (1 - P_{loss}) \times \text{Efficiency}$ | $G = T \times (1 - \text{ProtocolRatio})$ |

*   **실무 포인트**: 1Gbps 대역폭 포트를 가진다고 해서 1Gbps 파일 다운로드가 보장되지 않는다. TCP/IP 오버헤드(약 20~40%), 패킷 손실 및 재전송, Flow Control 제약 등으로 인해 실제 Goodput은 보통 대역폭의 60~80% 수준에 머문다.

#### 2. 기술 스택 융합 관점

-   **물리계층(L1)과의 관계**: OFDM(Orthogonal Frequency Division Multiplexing) 같은 변조 방식은 대역폭을 여러 개의 부반송파(Subcarrier)로 쪼개어 주파수 효율성을 극대화한다. 이는 **Wi-Fi 4/5/6/7**과 **LTE/5G**의 핵심 기술이다.
-   **MAC 계층(L2)과의 관계**: 대역폭이 넓어도 MAC 계층의 **CSMA/CA**(무선랜)나 **TDMA**(셀룰러) 방식에서 다른 사용자와의 경쟁이나 할당(Scheduling) 대기 시간이 길다면, 사용자가 체감하는 성능은 떨어진다. 따라서 **QoS(Quality of Service)** 스케줄링 기술이 융합되어야 대역폭의 가치가 실현된다.

#### 3. ASCII 다이어그램: Wi-Fi 채널 대역폭 비교 (20MHz vs 160MHz)

```ascii
[ Wi-Fi Channel Width Comparison (IEEE 802.11 Standard) ]

   20 MHz Channel (Wi-Fi 4/5 Basic)          160 MHz Channel (Wi-Fi 6/6E/7 High-End)
   +-------------+  5GHz                     +--------------------------------------------------+
   | 20 MHz Sub  |                           |           160 MHz Wide Block                      |
   |   Channel   |                           |  (2.4Ghz/5Ghz/6GHz Band)                         |
   +-------------+                           +--------------------------------------------------+
   Max: ~433 Mbps (1 stream)                 Max: ~1.2 Gbps+ (1 stream)
   
   [ Trade-off Analysis ]
   
   Wider Bandwidth (160MHz)
   -- [Benefit] --> Throughput x4 (Potential Speed)
   -- [Cost]    --> 
       1. Susceptibility to Interference x4 (Range of noise increases)
       2. Fewer available non-overlapping channels (Congestion Risk)
```
*(해설: 대역폭을 4배로 넓히면(20MHz -> 160MHz)