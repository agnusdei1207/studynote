+++
title = "104-107. 임의 접근 매체 제어: CSMA와 CSMA/CD"
date = "2026-03-14"
[extra]
category = "Physical & MAC Layer"
id = 104
+++

# 104-107. 임의 접근 매체 제어: CSMA와 CSMA/CD

### # 임의 접근 매체 제어 및 충돌 관리 기술
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **CSMA (Carrier Sense Multiple Access)**는 "선 점유 후 전송"의 통제 방식으로, 무선 매체의 은닉 스테이션 문제 등을 완화하지만 전파 지연(Propagation Delay)으로 인한 충돌을 근본적으로 차단하지 못함.
> 2. **가치**: **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**는 유선 환경에서 '전송 중 감지'를 통해 불필요한 대기 시간을 제거하고, **이진 지수 백오프 (Binary Exponential Backoff)** 알고리즘으로 네트워크 혼잡도에 따른 적응형 재전송을 통해 효율성(Throughput)을 극대화함.
> 3. **융합**: OSI 7계층의 **MAC (Media Access Control)** 계층에 위치하며, 스위치(Switch) 기반의 **CSMA/CA (Collision Avoidance)** 방식과의 진화 및 TCP/IP 스택의 흐름 제어(Flow Control)와 연계됨.

---

## Ⅰ. 개요 (Context & Background) - 통제 없는 자유와 그 대가

### 개념 및 철학
**CSMA (Carrier Sense Multiple Access, 반송파 감지 다중 접속)**는 다중화(Multiplexing) 환경에서 중앙 통제 스테이션(Access Point) 없이, 각 노드(Node)가 자율적으로 채널 상태를 감지(Sense)하여 데이터를 전송하는 분산형 매체 접근 제어 프로토콜입니다. 이는 ALOHA 프로토콜의 단순성을 계승하되, '말하기 전에 경청하는(Listen Before Talk)' 예절을 도입하여 채널 효율을 획기적으로 개선한 방식입니다.

### 등장 배경 및 진화
1.  **ALOHA의 한계**: 초기 무선 데이터 통신(University of Hawaii)에서 사용된 순수 ALOHA 방식은 전송 의지만 생기면 즉시 데이터를 쏘았기 때문에, 트래픽이 증가할수록 충돌(Collision)로 인한 처리량(Throughput)이 급감하여 최대 18%의 효율만 보임.
2.  **CSMA의 혁신**: "반송파(Carrier, 전송 중인 신호)가 있는지 먼저 듣고(Look before you leap)", 비어 있을 때만 전송하여 전체 효율을 최대 80% 이상으로 끌어올림.
3.  **유선 환경의 최적화**: 유선 LAN(Wired Ethernet) 환경에서는 신호의 감쇄가 없고 전압 레벨을 정밀하게 모니터링할 수 있으므로, 충돌을 '감지(Detect)'하여 즉시 조치하는 **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)** 방식으로 발전함.

### 💡 핵심 비유
이는 수많은 차량이 교통정리 없이 교차로 통행을 시도하는 상황과 유사합니다. ALOHA 방식은 운전자가 앞을 보지 않고 교차로로 진입하여 사고가 나면 후회하는 방식이지만, CSMA는 진입 전 좌우를 확인하여, 다른 차가 지나가는지(Carrier Sense) 확인한 뒤 진입하는 안전 운전 수칙과 같습니다.

```ascii
      [통신 매체 사용 패러다임 변화]

    ALOHA (무관심)          CSMA (예절)             CSMA/CD (실무형)
  ----------->        ------------->         ------------------>
  [Transmit]           [Listen -> Send]       [Listen -> Send & Monitor]
                       |                     |
                       v                     v
                 충돌 확률 감소 (~80%)     충돌 감지 및 즉시 복구
```

### 📢 섹션 요약 비유
CSMA는 다인용 화장실 앞에서 문을 두드려 보고(Knocking/Sensing), 안에서 사람이 없는 것을 확인하고 들어가는 예의 바른 행동과 같습니다. 하지만 문을 두드리는 순간과 동시에 다른 사람이 열어버리면 충돌이 일어날 수 있는 구조적 한계가 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - 전략별 세부 메커니즘

CSMA는 채널이 사용 중(Busy)일 때, 노드가 어떻게 대기(Backoff)하고 재시도(Retry)할지에 따라 세 가지 세부 알고리즘으로 분류됩니다.

### 1. 지속(Persistent) 전략 비교

| 구분 | 1-Persistent CSMA | Non-Persistent CSMA | p-Persistent CSMA |
|:---|:---|:---|:---|
| **동작** | 채널이 빌 때까지 감지 후, **즉시(100%)** 전송 | 채널이 사용 중이면 **랜덤 시간 대기** 후 재감지 | 채널이 비면 **`p` 확률**로 전송, `1-p` 확률로 대기 |
| **장점** | 대기 시간 지연(Delay) 최소화 | 충돌 확률 최소화 | 지연과 충돌의 절충 (Trade-off) |
| **단점** | **채널이 해제되는 순간 다수 노드가 동시 전송** 시도 → 충돌 빈발 | 채널이 비어있어도 불필요하게 대기 → 효율 저하 | `p` 값 최적화가 어려움 (Slotted 시스템 필요) |
| **활용** | 유선 LAN (Ethernet) 표준 | 일반적인 무선 패킷 네트워크 | 슬롯형 무선 네트워크 (IEEE 802.11의 기반) |

### 2. CSMA/CD의 상세 동작 메커니즘 (유선 환경)

**CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**는 IEEE 802.3 표준 이더넷의 핵심입니다. 유선 케이블(Coaxial, Twisted Pair)은 신호 감쇠가 적고 전압을 정밀히 측정할 수 있으므로, 송신 중에도 수신 선을 감시하며 충돌 여부를 판단할 수 있습니다.

#### 심층 동작 단계 (Algorithm)
1.  **감지 (Sense)**: 전송할 데이터가 발생하면, 케이블에 반송파(Carrier)가 있는지 확인합니다.
2.  **전송 (Transmit)**: 채널이 유휴(Idle) 상태이면 즉시 전송을 시작합니다.
3.  **감시 (Monitor)**: 데이터를 보내는 동시에 **Collision Detection 회로**를 통해 자신이 보낸 신호와 케이블 상의 전압 레벨을 비교합니다.
4.  **충돌 판정 (Collision Detect)**:
    *   자신의 전압보다 높은 전압이 검출되면 충돌이 발생한 것으로 간주 (Two signals > Threshold).
    *   이더넷 규격상 **최소 프레임 크기(Minimum Frame Size)**는 64바이트여야 합니다. 이는 충돌이 발생했을 때, 송신 노드가 전송을 완료하기 전에 반드시 이 충돌 신호를 감지할 수 있도록 **왕복 전파 지연(Round-Trip Time, RTT)**을 보장하기 위함입니다.
    *   $T_{transmit} \ge 2 \times T_{prop}$
5.  **중단 및 잼 (Abort & Jam)**: 즉시 전송을 중단하고, 모든 노드에게 충돌을 알리는 **Jam Signal (32비트)**을 브로드캐스트합니다.

```ascii
[CSMA/CD 타이밍 및 충돌 감지 다이어그램]

Station A                               Station B
    |                                       |
    |--- Listen (Idle) -------------------> |
    |                                       |
    |--- Transmit Start -------------------->--- (Simultaneous Transmit Start)
    |                                       |
    | (Signal Propagation...)               | (Signal Propagation...)
    |                                       |
    |<---------- Collision Point ----------->|
    | (Signals overlap, Voltage spikes)     |
    |                                       |
    |--- Detect Collision! --------- Detect Collision! ---|
    |                                       |
    |--- Send JAM Signal ------------------->--- Send JAM Signal
    |                                       |
    |--- Stop Transmit ---------------------->--- Stop Transmit
    |                                       |
    |--- Random Backoff Wait (Binary Exp) --->--- Random Backoff Wait
```

### 핵심 알고리즘: 이진 지수 백오프 (Binary Exponential Backoff)
충돌 후 재전송 시점을 결정하는 알고리즘입니다. 충돌이 반복될수록 네트워크가 혼잡하다고 판단하여 대기 시간을 지수적으로 늘립니다.

**Python Pseudo-Code**:
```python
# BEB Algorithm Logic
# n: 충돌 횟수 (최대 10, 그 후 15번째 시도 시 포기)

import random

def calculate_backoff_slots(n):
    if n <= 10:
        max_slots = (2 ** n) - 1
    else:
        max_slots = (2 ** 10) - 1 # 1023 slots
    
    return random.randint(0, max_slots)

collision_count = 0
while collision_count < 16:
    if channel_idle():
        transmit()
        if collision_detected():
            collision_count += 1
            wait_time = calculate_backoff_slots(collision_count) * SLOT_TIME
            wait(wait_time)
        else:
            break # Success
else:
    print("Transmission Failure: Excess Collision")
```

### 📢 섹션 요약 비유
CSMA/CD는 빈방에 들어가려는 사람이 문을 열고 들어가는데, 들어가는 순간 반대편에서도 누군가 들어와 부딪힌 상황과 같습니다. 이때 "앗!" 하고 소리치며(Jam Signal) 멈춘 뒤, 1~2초 세었다가(Random Backoff) 다시 문을 여는 과정을 반복합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술 비교: CSMA vs. CSMA/CD vs. CSMA/CA

| 특징 | CSMA (기본) | CSMA/CD (유선) | CSMA/CA (무선) |
|:---|:---|:---|:---|
| **Full Name** | Carrier Sense Multiple Access | **CSMA with Collision Detection** | **CSMA with Collision Avoidance** |
| **매체** | 공유 케이블 (Legacy) | 유선 LAN (Twisted Pair) | 무선 LAN (IEEE 802.11 Wi-Fi) |
| **핵심 메커니즘** | 송신 전 감지 | **송신 중 감지 (Monitoring)** + 백오프 | **송신 전 예약 (RTS/CTS)** + 백오프 |
| **충돌 처리** | 수신 ACK 실패 시 재전송 | 전압 변화로 즉시 감지 및 즉시 조치 | 충돌 감지 불가능, **사전 회피** 위주 |
| **신뢰성** | 중간 | 높음 (물리적 신호 정확) | 낮음 (Noise, Fading, Hidden Node) |
| **효율성** | 낮음 (충돌 대기 시간 손실) | 높음 (불필요한 전송 중단) | 중간 (Overhead 큼) |

### 2. OSI 계층 및 타 영역과의 시너지

*   **물리 계층(Physical Layer)과의 연계**: MAC 계층의 "Carrier Sense"는 PHY 계층의 **PLL (Phase Locked Loop)**이나 **能量检测(Energy Detection)** 기능을 통해 물리적인 신호 강도(RSSI)를 측정하여 구현됩니다.
*   **네트워크 계층(L3 IP)과의 관계**: 이더넷 스위치(Switch)가 보급되면서 충돌 도메인(Collision Domain)이 포트별로 분리되었습니다. Full-Duplex 통신에서는 송신/수신 경로가 분리되어 있어 **CSMA/CD가 비활성화**되며, 흐름 제어(Flow Control)은 MAC Control Frame(Pause Frame)으로 대체되었습니다.
*   **운영체제(OS)**: 네트워크 인터페이스 카드(NIC)의 드라이버는 인터럽트(Interrupt)를 통해 충돌 발생을 OS 커널에 알리고, TCP/IP 스택은 이를 패킷 손실로 간주하여 재전송(Retransmission)을 수행할 수도 있습니다. (이중 구조)

### 📢 섹션 요약 비유
CSMA/CD는 전화 통화에서 상대방과 동시에 말하는 것을 즉시 알 수 있는 '유선 전화'와 같지만, CSMA/CA는 상대방이 말을 하는지 들리지 않아서, "말해도 되나요?"(RTS)라고 물어보고 "해"(CTS)를 들은 뒤에야 말을 시작하는 '무전기' 규약과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정 트리

**상황 A**: 기존 10Mbps/100Mbps **허브(Hub)** 기반 공유 미디어 네트워크에서 1Gbps 이더넷으로 업그레이드 고려.
*   **문제**: 허브는 모든 포트가 하나의 충돌 도메인을 공유하여 CSMA/CD에 의해 성능이 제한됨.
*   **해결**: 허브를 **스위치(Switching Hub)**로 교체.
*   **이유**: 스위치는 각 포트가 별도의 충돌 도메인을 가지며, **Store-and-Forward** 방식을 사용하여 CSMA/CD의 필요성을 제거(버퍼링 및 전이중 통신 지원)하고 처리량(TPS)을 획기적으로 증대시킴.

**상황 B**: 자동차 공장의 제어 네트워크 설계 (Real-time 제어).
*   **문제**: CSMA/CD의 '랜덤 백오프(Random Backoff)' 특성상, **지연 시간(Latency)**이 예측 불가능할 수 있음. 최악의 경우 n=10까지 대기할 수 있음.
*   **해결**: 우선순위 기반의 **토큰 링(Token Ring)**이나 **TDM (Time Division Multiplexing)** 방식 고려, 또는 스위치드 이더넷에서 **QoS (Quality of Service)** 우선순위 큐를 적용하여 CSMA/CD의 비결정성(Non-determinism)을 완화.

### 2. 안티패턴 (Anti-Pattern)

*   **Jam Signal 누락 설계**: 만약 CSMA/CD 구현 시 충돌 후 Jam Signal을 보내지 않으면, 물리적 거리가 먼 노드는 충돌이 발생했는지 모르고 계속 전송을 시