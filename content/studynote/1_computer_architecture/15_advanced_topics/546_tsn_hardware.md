+++
title = "546. 결정론적 이더넷 (TSN, Time-Sensitive Networking) 하드웨어"
date = "2026-03-14"
weight = 546
+++

# 546. 결정론적 이더넷 (TSN, Time-Sensitive Networking) 하드웨어

## # [결정론적 이더넷 (TSN) 하드웨어]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IEEE 802.1 표준 기반의 이더넷(Ethernet) MAC(Media Access Control) 계층에 **하드웨어 타임스탬핑(Hardware Timestamping)**과 **시간 인지 스케줄링(Time-Aware Scheduling)**을 통합하여, 불확실한 'Best-Effort' 네트워크를 마이크로초(µs) 단위의 '결정론적(Deterministic)' 전송망으로 진화시킨 아키텍처다.
> 2. **가치**: 자동차(Zonal Architecture)와 스마트 팩토리(Motion Control)에서 요구하는 **초저지연(Latency < 1ms)**과 **동기화 정밀도(Jitter < 1µs)**를 만족하면서도, 기가비트(Gbps) 급의 대역폭을 활용하여 IT(정보 기술)와 OT(운영 기술) 트래픽을 단일 물리망으로 융합한다.
> 3. **융합**: **gPTP (Generalized Precision Time Protocol)**를 통한 전역 시간 동기화와 **CNC (Centralized Network Configuration)**를 통한 SDN(Software Defined Networking) 기반의 통합 제어가 필수적이며, 5G URLLC와 결합하여 무선화가 진행 중인 미래 산업 네트워크의 핵심 인프라다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: TSN(Time-Sensitive Networking)은 기존 이더넷이 가진 비결정론적(Non-Deterministic) 한계를 극복하기 위해 IEEE 802.1 위원회에서 표준화한 일련의 기술 세트다. 기존의 CSMA/CD 방식이나 우선순위 큐(Priority Queue)만으로는 보장할 수 없었던 '최대 지연 시간(Worst-case Latency)'을 하드웨어 수준에서 수학적으로 보장한다. 이는 단순한 '속도'의 문제가 아니라 '예측 가능성(Predictability)'을 확보하는 것이 핵심이다.
- **💡 비유**: 일반 이더넷은 신호등 없고 혼잡한 **'시장 통로'**와 같다. 언제 막힐지 모르기 때문에 응급환자를 실은 앰뷸런스(제어 데이터)가 지나가긴 위험하다. TSN은 이 도로에 **'정밀하게 동기화된 신호등 시스템(Traffic Light Synchronization)'**과 **'앰뷸런스 전용 자동 차단봉(Gate Control)'**을 설치한 것이다. 모든 차량과 신호등이 나노초 단위로 시계를 맞추고 있어, 앰불런스는 아무도 없는 도로를 질주하듯 논스톱으로 통과한다.
- **등장 배경**:
  1. **기존 필드버스(Fieldbus)의 대역폭 한계**: CAN(Controller Area Network), PROFIBUS 등은 수 Mbps 수준의 대역폭으로 인해 고해상도 카메라나 LiDAR(Light Detection and Ranging) 센서 데이터를 처리하기에 역부족이었다.
  2. **이더넷의 Jitter 문제**: 일반 이더넷 스위치는 Store-and-Forward 방식과 큐잉 지연(Queuing Delay)으로 인해 패킷 도착 시간이 수백 µs~수 ms까지 들쭉날쭉(Jitter)했으며, 이는 로봇 팔의 미세한 제어를 불가능하게 만들었다.
  3. **AVB에서 TSN으로**: AVB(Audio Video Bridging) 기술을 시작으로, 산업용 제어의 엄격한 실시간 요구사항을 만족시키기 위해 시간 동기화(802.1AS), 스케줄링(802.1Qbv), 패킷 선점(802.1Qbu/802.3br) 등의 기능이 통합되어 TSN ecosystem이 형성되었다.

#### 📢 섹션 요약 비유
"마치 복잡한 철도 네트워크에 모든 열차의 위치를 실시간으로 추적하는 **중앙 제어 시스템**을 도입하여, 화물열차와 고속열차가 정확한 시간에 충돌 없이 교차 운행할 수 있도록 만든 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

TSN의 하드웨어적 실현은 크게 '시간 동기화', '트래픽 예약', '불러오기(Preemption)' 세 가지 축으로 이루어진다.

#### 1. TSN 핵심 구성 요소 상세 분석

| 구성 요소 (Module) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 주요 프로토콜/표준 |
|:---|:---|:---|:|
| **Clock Sync** | gPTP (Generalized Precision Time Protocol) | 네트워크 내 모든 노드(스위치, End-station)의 클럭 오차를 **1µs 이하**로 보정. 하드웨르 타임스탬프를 사용하여 소프트웨어 지연 제거 | IEEE 802.1AS |
| **Traffic Shaping** | TAS (Time-Aware Shaper) | gPTP로 동기화된 전역 시간을 기준으로, 특정 시간 윈도우(Gate Open Time)에만 특정 큐(Queue)가 전송되도록 하드웨어 게이트(Gate) 제어 | IEEE 802.1Qbv |
| **Preemption** | Frame Preemption | 대용량 프레임 전송 중 고우선순위 프레임 도착 시, 대용량 프레임을 **조각(Fragment)** 내어 전송을 멈추고 고우선순위 프레임을 먼저 전송 후 재개 | IEEE 802.1Qbu / 802.3br |
| **Reliability** | FR (Frame Replication and Elimination) | 동일한 스트림을 두 개의 경로로 복제 전송하여, 수신측에서 중복을 제거함으로써 경로 실패에도 무중단 서비스 보장 | IEEE 802.1CB |
| **Configuration** | CNC (Centralized User Configuration) | 네트워크 토폴로지와 트래픽 요구사항을 분석하여 모든 스위치의 TAS 스케줄(GCL)을 수학적으로 계산하고 배포하는 중앙 컨트롤러 | IEEE 802.1Qcc |

#### 2. 시간 인지 스케줄러 (TAS, 802.1Qbv) 동작 메커니즘

TAS는 일반적인 우선순위 큐(Priority Queue)와 달리, **시간(Time)**이라는 차원을 도입한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│               [Time-Aware Shaper (TAS) Gate Control Logic]                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  (Time Axis)          T0      T1      T2      T3      T4      T5      T6   │
│                     │       │       │       │       │       │       │     │
│  Global Clock ──────┴───────┴───────┴───────┴───────┴───────┴───────┴───> │
│                                                                             │
│  [Gate Control List (GCL) Loaded in HW]                                    │
│                                                                             │
│  Queue 7 (Highest)  [CLOSE]   [OPEN]   [CLOSE]   [CLOSE]   [OPEN] ...     │
│                             ▲                         ▲                     │
│  Queue 6 (High)     [CLOSE]   [CLOSE]   [OPEN]       [CLOSE] ...          │
│                                       ▲                                     │
│  Queue 0 (Low)      [OPEN]    [CLOSE]   [CLOSE]      [OPEN]  ...          │
│          ▲          ▲                                                           │
│                                                                             │
│  Transmission Link   ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼│
│                                                                             │
│   Interval 1       Interval 2     Interval 3     Interval 4                │
│   (Best-Effort)    (Critical Ctl) (Best-Effort) (Critical Ctl)             │
│                                                                             │
│  * Legend:                                                                 │
│    [OPEN]: Gate Open (Transmit Allowed)  --> Hardware Multiplexer ON       │
│    [CLOSE]: Gate Close (Transmit Blocked) --> Hardware Multiplexer OFF     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]**
이 다이어그램은 **TAS (Time-Aware Shaper)**의 핵심인 게이트 제어 리스트(GCL)가 하드웨어에서 어떻게 작동하는지를 보여준다.
1.  **동기화된 시계 기반**: 모든 스위치와 끝단 노드는 gPTP를 통해 T0, T1...라는 동일한 시간 축을 공유한다.
2.  **하드웨어 멀티플렉서(MUX) 제어**: 소프트웨어의 개입 없이, MAC 계층 내부의 하드웨어 MUX가 미리 정해진 GCL에 따라 큐(Queue)의 문을 열고 닫는다.
3.  **보호 대역(Guard Band)**: 고우선순위 큐(큐7)가 열리기 전후 약간의 시간을 닫아두어, 앞서 전송되던 저순위 패킷이 완전히 빠져나갈 때까지 시간을 확보한다. 이를 통해 고순위 패킷은 앞선 패킷의 잔여물에 의해 지연되는 것(HOL Blocking)을 완벽히 방지한다.
4.  **결과**: 네트워크 관리자는 `T1~T2` 구간을 "무조건 제어 신호만 사용"하도록 설정하여, 그 구간 내의 지연 시간(Jitter)을 사실상 0에 가깝게 만들 수 있다.

#### 3. 심층 동작: 프레임 선점 (Frame Preemption)

TAS는 훌륭하지만, '시간'을 기다리는 동안 선(Link)이 비는 문제가 있다. 이를 해결하기 위해 물리 계층 가까운 MAC에서 **'새치기'**를 허용한다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                 [Frame Preemption (IEEE 802.1Qbu) Mechanism]               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Scenario: A large "Best-Effort" packet is transmitting,                  │
│            and a "Critical" packet arrives.                                │
│                                                                            │
│  1. Normal Transmission Start                                              │
│     [BE Packet Header] ──▶ [BE Payload (1500 Bytes)] ──▶ [FCS]            │
│     ▲                                                                          │
│     └── (Currently Transmitting...)                                        │
│                                                                            │
│  2. Critical Packet Arrives (Interrupt!)                                   │
│     [Critical Packet] ▶ Urgent Request!                                    │
│                                                                            │
│  Action: MAC Layer splits the BE Packet immediately.                       │
│                                                                            │
│  3. Preemption & MD (Marker Insertion)                                     │
│     [BE Header] ──▶ [MD] ──▶ [BE Payload Remainder]            │
│                     ▲                                                       │
│                     └──> SENDING CRITICAL PACKET NOW!!! <──┐               │
│                                                            │               │
│  4. Link State                                             │               │
│     ┌──────────────┐      ┌───────────────────┐            │               │
│     │ BE Fragment  │ ───▶ │ CRITICAL FRAME    │ ───────▶  │               │
│     │ (Part 1)     │      │ (Express - 64B)   │            │               │
│     └──────────────┘      └───────────────────┘            │               │
│                                                            ▼               │
│     ┌─────────────────────────────────────────────────────┐                │
│     │ BE Fragment (Part 2) │ (Resume Transmission)       │                │
│     └─────────────────────────────────────────────────────┘                │
│                                                                            │
│  * Key Point: Receiver NIC recognizes 'MD' flag, buffers Fragment 1,       │
│    waits for Fragment 2, and reassembles them seamlessly.                 │
└────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]**
이 기술은 **802.3br (Interspersing Express Traffic)** 표준으로도 불리며, 네트워크 대역폭 효율성을 극대화한다.
1.  **MD (MAC Merge) 서브레이어**: 물리적 계층 위에 논리적인 '이음새' 계층을 두어, 패킷을 중간에 끊어도 수신측에서 이를 원래대로 다시 붙일 수 있게 한다.
2.  **Express vs. Preemptable**: 트래픽을 두 가지 클래스로 나눈다. 변경 불가능한 가장 중요한 패킷(Express)과, 쪼개질 수 있는 패킷(Preemptable)으로 분리하여 관리한다.
3.  **지연 최소화**: 긴 패킷(약 1200~1500바이트) 전송 시간은 기가비트 이더넷 기준 약 12µs 이상 소요된다. 선점(Preemption)을 사용하면 긴급 메시지는 최대 1µs 이내에 전송을 시작할 수 있어, 실질적인 반응 속도(Response Time)를 10배 이상 개선한다.

#### 4. 핵심 알고리즘: gPTP 시간 동기화 과정
결정론적 전송의 기본은 모든 참여자가 동일한 시간을 갖는 것이다. NTP(Network Time Protocol)가 밀리초(ms) 오차라면, gPTP는 하드웨어 스탬핑을 통해 나노초(ns) 오차를 맞춘다.

```text
Algorithm: Grandmaster -> Slave Synchronization

1. Master sends Sync Message (Timestamp t1)
   [ t1 ] ----------------------------------------------------> [ t2 ]
   
   * Hardware notes t1 at PHY layer (Wire time)
   * Slave receives and notes t2 at PHY layer

2. Master sends Follow_Up Message (contains t1 value)
   [ t1_correction ] -----------------------------------------> [Correction]
   
3. Slave sends Delay_Req Message
   [ t3 ] <---------------------------------------------------- [ t4 ]
   (Slave records t3, Master records t4)

4. Master sends Delay_Resp Message (contains t4 value)
   [ t4_value ] ---------------------------------------------> [Update]

5. Calculation (Offset Correction):
   Offset = (t2 - t1) - ( (t4 - t3) / 2 ) - PathDelayRatio
   
   -> Slave adjusts its local clock oscillator (VCXO) 
      to align with Master immediately.
```

#### 📢 섹션 요약 비유
"마치 고속도로에서 **VIP 행차를 위해 나중에 탄 승용차를 강제로 갓길로 밀어내고**, VIP가 지나간 뒤 그 승용차를 다시 도로로 진입시키는 **격렬한 교통 통제 시스템**과 같습니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 산업용