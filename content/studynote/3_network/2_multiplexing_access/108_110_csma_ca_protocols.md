+++
title = "108-110. 무선 LAN 매체 제어: CSMA/CA와 히든 노드 문제"
date = "2026-03-14"
[extra]
category = "Physical & MAC Layer"
id = 108
+++

# 108-110. 무선 LAN 매체 제어: CSMA/CA와 히든 노드 문제

> **1. 본질**: 유선 LAN의 CSMA/CD는 충돌을 감지하지만, 무선 환경(WLAN)에서는 신호 감쇠와 '근거리 문제(Near/Far Problem)'로 인해 Collision Detection이 불가능하므로, 사전에 충돌 확률을 최소화하는 CSMA/CA (Collision Avoidance) 방식을 사용합니다.
> **2. 가치**: 무선 매체의 효율성을 극대화하여 데이터 손실률을 낮추고, RTS/CTS (Request To Send/Clear To Send) 핸드셰이크를 통해 은닉 노드 문제를 해결하여 네트워크의 안정성과 처리량(Throughput)을 보장합니다.
> **3. 융합**: OSI 7계층 중 물리(Physical) 계층의 RF 특성과 MAC 계층의 프로토콜이 결합된 기술로, 최근 Wi-Fi 6/7 표준에서는 OFDMA 기술과 결합하여 더욱 정교한 자원 관리로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

무선 LAN (Wireless Local Area Network) 환경에서의 데이터 통신은 유선과 근본적으로 다른 물리적 제약이 있습니다. 유선 이더넷(Ethernet)은 UTP 케이블을 통해 전압 레벨을 모니터링하여 충돌(Collision) 발생을 즉시 감지할 수 있지만, 무선 환경은 전파의 도달 거리 한계와 감쇠(Attenuation)로 인해 자신의 신호를 송신하는 동안에는 다른 노드의 신호를 감지할 수 없습니다. 이를 **'하프 듀플렉스(Half-Duplex)'** 환경의 근본적인 문제라고 합니다.

이러한 물리적 한계를 극복하기 위해 IEEE 802.11 표준은 **CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)**를 채택했습니다. 이는 "충돌이 발생한 후에 대처(CD)"하는 것이 아니라, "충돌이 발생하지 않도록 사전에 예방(CA)"하는 철학을 기반으로 합니다. 단순히 채널이 비어있는지 확인하는 것을 넘어, **이중 모드(Dual Mode)** 감지(물리적/가상 캐리어 감지)와 확률적 백오프(Backoff) 알고리즘을 도입하여 무선 매체라는 열악한 환경에서도 신뢰성 있는 통신을 제공합니다.

📢 **섹션 요약 비유**: 유선 LAN은 수화기를 들고 상대방 말이 끝나는지 확인하며 대화하는 것이지만, 무선 LAN은 소음이 심한 시장에서 눈을 가리고 대화하는 것과 같습니다. 따라서 말을 하기 전에 "내가 지금 말할 테니 기다려라"라고 주변에 충분히 알리고(Reservation), 대답을 들은 후에야 본론을 꺼내는 식의 예의(Protocol)가 필요합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CSMA/CA의 핵심은 충돌 회피를 위해 **DIFS (Distributed Inter-Frame Space)** 대기와 **이진 지수 백오프(Binary Exponential Backoff)** 알고리즘을 결합하는 것입니다. 송신 노드는 데이터 프레임 전송 전에 반드시 채널 상태를 감지(Sense)하며, 이때 물리적 채널의 에너지 레벨을 측정하는 **Physical Carrier Sensing**과, 다른 노드의 NAV(Network Allocation Vector) 타이머 정보를 확인하는 **Virtual Carrier Sensing**을 동시에 수행합니다.

### 1. CSMA/CA 핸드셰이크 및 파라미터 분석

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 비유 |
|:---|:---|:---|:---|
| **DIFS** | Distributed Inter-Frame Space | 데이터 프레임 전송을 위한 최소 대기 시간. 우선순위가 가장 낮은 매체 접근 지연 시간으로, 채널이 idle 상태로 유지되어야만 카운트다운 시작. | 신호등이 파란불로 바뀐 후, 출발하기 전 잠깐 멈춰서 좌우를 확인하는 시간. |
| **SIFS** | Short Inter-Frame Space | 가장 짧은 대기 시간. ACK, CTS 등 제어 프레임 간의 간격으로, 데이터 전송 흐름을 끊기지 않게 유지하는 우선순위. | 대화 중에 상대방이 "어", "그렇구나" 하고 받아주는 짧은 쉼. |
| **CW** | Contention Window | 경쟁 윈도우. 슬롯 시간의 배수로 설정된 랜덤 대기 범위 (`[0, CW]`)로, 충돌 확률을 낮추기 위해 무작위 시간만큼 추가 대기. | 여러 사람이 동시에 일어나지 않도록 정해진 구간 내에서 랜덤하게 시간을 두고 일어서는 규칙. |
| **NAV** | Network Allocation Vector | 가상 감지 도구. RTS/CTS 프레임에 포함된 '예약 시간 정보'를 읽어, 자신이 전송 가능할 때까지 타이머를 설정하여 대기. | 회의실 예약 시스템에서 '이 시간까지 사용 중'이라는 문구가 떠 있으면 기다리는 것. |

### 2. 상세 동작 타이밍 및 알고리즘

CSMA/CA는 무작위성을 도입하여 시스템 안정성을 확보하지만, 효율성을 위해 **PCF (Point Coordination Function)**와 같은 폴링 방식과 혼용되기도 합니다. 일반적인 DCF(Distributed Coordination Function) 모드의 데이터 전송 과정은 다음과 같습니다.

1.  **채널 감지 (Carrier Sense)**: 매체가 Idle인지 확인합니다.
2.  **DIFS 대기**: 매체가 Idle이면 DIFS 시간 동안 기다립니다.
3.  **백오프 (Random Backoff)**: `0 ~ 2^k - 1` (슬롯 수) 범위 내에서 랜덤 값을 선택하고, 슬롯 시간만큼 카운트다운합니다. (매 슬롯마다 채널 감지)
4.  **데이터 전송**: 카운트가 0이 되면 데이터 프레임을 송신합니다.
5.  **ACK 확인**: 수신측은 SIFS 후에 ACK를 응답합니다. ACK가 없으면 재전송 절차(CW 증가)를 밟습니다.

```ascii
         [CSMA/CA Backoff Process Logic]

   Sender Node                    Channel State
      |                                 |
      | (1. Data to Send)               |
      v                                 |
   [Check Medium] ------------> (Busy)  | <-- 다른 노드 전송 중
      |                                 |
      |<-- (Wait until Idle) ------------|
      v                                 |
   [Start DIFS] ******> (Idle)          |
      |                                 |
   [Start Backoff]                     |
      | [Slot # ]...[Slot #1] [Slot #0] <-- 랜덤 카운트다운
      |                                 |
      | (중간에 채널이 Busy되면 정지 후 재개)  |
      v                                 |
   [Count = 0] --> (Transmit Frame) --->|
      |                                 |
      |<-- (SIFS) -- [ACK Receiver] ----|
      v                                 |
   [Success]                           |
```

**심층 해설**:
위 다이어그램에서 볼 수 있듯이, CSMA/CA는 단순한 "대기 후 전송"이 아닙니다. **백오프 카운터**가 0이 되는 순간까지 경쟁이 계속됩니다. 만약 두 노드가 동일한 백오프 값을 가지면 충돌(Collision)이 발생합니다. 이 경우 수신자로부터 ACK가 오지 않으므로, 송신자는 **CW(Contention Window)** 크기를 2배로 늘려(Binary Exponential Backoff), 다음번 경쟁에서 충돌 확률을 낮추는 자기 조절 능력을 발휘합니다.

📢 **섹션 요약 비유**: 교차로에서 신호등이 없을 때, 모든 차량이 동시에 출발하면 사고가 납니다. CSMA/CA는 신호등이 켜지면(DIFS), 각 운전자가 마음속으로 1초부터 5초 사이의 숫자를 하나 정하고(Backoff), 그 시간이 다 됐을 때만 출발하는 규칙입니다. 만약 출발했다가 브레이크를 밟는 차가 있으면(ACK 수신 실패), 다음 번에는 더 넓은 범위의 숫자를 선택하여 조심스럽게 나아가는 방식입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

무선 네트워크의 가장 큰 성능 저하 요인은 **'은닉 노드(Hidden Node)'**와 **'노출 노드(Exposed Node)'** 문제입니다. 이는 MAC 계층의 설계 결함이 아니라, 전파의 물리적 특성(감쇠, 거리)에서 기인합니다. 이를 해결하기 위해 CSMA/CA에 가상 예약 메커니즘을 결합한 **RTS/CTS (Request To Send/Clear To Send)**가 제안되었습니다.

### 1. 은닉 노드 vs 노출 노드 기술 비교

| 구분 | 은닉 노드 (Hidden Node) | 노출 노드 (Exposed Node) |
|:---|:---|:---|
| **정의** | 서로의 신호가 도달하지 않아 상대방의 존재를 모르는 상태에서 동시 송신, **AP에서 충돌** 발생. | 송신자에게는 신호가 도달하나, 수신자에게는 영향이 없음에도 불구하고 채널이 사용 중이라 착각하여 **전송 유보**, 효율성 저하. |
| **원인** | 노드 간 거리가 전파 도달 거리를 초과할 때 발생. | 노드 간 거리는 가깝지만, 의도한 수신자가 멀리 있을 때 발생. |
| **해결책** | **RTS/CTS** 핸드셰이크로 채널 예약. RTS를 듣지 못한 은닉 노드라도 AP의 CTS를 들으면 NAV를 설정하여 양보. | RTS/CTS로 어느 정도 완화 가능하나, 근본적 해결은 어려움. IEEE 802.11 표준에서는 CTS 수신 시에도 전송을 시도하지 않도록 설계되어 있어 여전히 비효율 존재. |
| **영향** | **Critical**: 데이터 손실 및 재전송으로 인한 처리량(Throughput) 급격히 하락. | **Moderate**: 불필요한 대기로 인한 대역폭 낭비 발생. |

### 2. RTS/CTS 다이어그램 및 해결 메커니즘

RTS/CTS는 프레임 간 충돌이 발생하더라도 짧은 제어 프레임(RTS)끼리 충돌하므로 시간 낭비가 적다는 점에서 효율적입니다.

```ascii
      [Hidden Node Resolution via RTS/CTS]

 Node A (Hidden)          AP (Center)           Node C (Sender)           Node D (Recv)
      |                      |                      |                         |
      | (1) RTS (Data Req)-->|                      |                         |
      |                      |<----- (2) CTS (Burst)------------------------------>|
      |<----- (3) CTS (Grant)----------------------|                         |
      | [NAV SET: WAIT]     |                      | (4) Data Tx ------------>| (No Collision!)
      | [Wait...]          |                      |<---- (5) ACK ------------|
      |                      |                      |                         |
```

**심층 해설**:
1.  **Step 1**: C가 D에게 데이터를 보내려고 AP에 **RTS (Request To Send)**를 브로드캐스트합니다.
2.  **Step 2**: AP는 채널이 사용 가능하면 **CTS (Clear To Send)**를 전체 노드에 브로드캐스트합니다. 이 CTS 프레임 내부에는 **'NAV (Network Allocation Vector)'** 값이 포함되어 있습니다.
3.  **Step 3 (해결의 핵심)**: A는 C의 RTS를 못 들었지만(거리가 멀어서), AP의 CTS는 들을 수 있습니다. A는 CTS를 수신하면, "아, 누군가가 예약했구나" 판단하여 자신의 NAV 타이머를 작동시키고 잠입(Silent)합니다.
4.  **결과**: 물리적으로 C의 전파가 A에 닿지 않더라도, AP를 경유한 제어 신호(CTS)가 A의 입을 막아주어 충돌이 방지됩니다.

### 3. 기술적 융합 및 분석 (OSI & Protocol)

*   **과목 융합 (네트워크 & 컴퓨터 구조)**:
    *   **TCP 혼잡 제어와의 시너지**: 무선 LAN의 상위 프로토콜인 TCP는 패킷 손실을 혼잡으로 간주하여 전송 속도를 낮춥니다. CSMA/CA와 RTS/CTS가 MAC 계층에서 충돌을 최소화하여 재전송을 줄여야, TCP가 불필요하게 윈도우 크기를 축소하는 것을 방지할 수 있습니다.
    *   **전력 관제(Power Save)**: RTS/CTS는 단순한 충돌 방지를 넘어, 노드가 Sleep 모드에 들어갈 타이밍을 조절하는 전력 절약 프로토콜과 연동됩니다.

*   **정량적 의사결정 (Decision Matrix)**:
    *   **RTS Threshold**: RTS/CTS는 항상 사용하는 것이 아닙니다. 작은 프레임에 RTS/CTS를 매번 사용하면 오히려 오버헤드(Overhead)가 큽니다.
        *   *Small Frame (e.g., 50 Byte)*: RTS(20Byte) + CTS(14Byte) + ... 오버헤드가 데이터보다 커짐.
        *   *Large Frame (e.g., 1500 Byte)*: 충돌 시 재전송 비용이 크므로 RTS/CTS 사용이 유리함.
    *   따라서 실무에서는 **RTS Threshold (보통 500~2347 Byte)** 설정을 통해, 이보다 큰 프레임에만 RTS/CTS를 자동으로 적용하도록 설정합니다.

📢 **섹션 요약 비유**: 은닉 노드는 투명한 벽 너머에 있는 사람과 동시에 중앙 현관을 통과하려는 상황입니다. 서로 못 보니 충돌합니다. 이때 중앙 관리인(AP)이 "지금 C가 나가니까 A는 잠깐만!"(CTS)이라고 소리치면, 벽 너머의 A는