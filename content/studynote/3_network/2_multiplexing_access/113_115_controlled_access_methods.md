+++
title = "113-115. 통제된 접근(Controlled Access) 매체 제어 방식"
date = "2026-03-14"
[extra]
category = "Physical & MAC Layer"
id = 113
+++

# 113-115. 통제된 접근 매체 제어 방식

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**= 통제된 접근(Controlled Access)은 매체(Medium)에 대한 단말(Node)의 접근을 중앙 집중형 혹은 분산형 알고리즘으로 순서화(Collison-free)하여 충돌(Collision)을 근원적으로 차단하는 MAC (Medium Access Control) 계층 프로토콜입니다.
> 2. **가치**= 임의 접(Random Access) 방식(CSMA/CD 등)이 가진 고부하 시의 효율 급격 저하(Jam, Decay) 문제를 해결하여, **결정적(Deterministic)인 지연 시간 보장**과 높은 채널 활용도를 제공합니다.
> 3. **융합**= 산업용 제어 네트워크(Fieldbus) 및 QoS(Quality of Service)가 중요한 실시간 통신망(IEEE 802.11 PCF, Bluetooth 등)의 핵심 메커니즘으로 활용됩니다.

+++

## Ⅰ. 개요 (Context & Background)

### 개념 및 정의
**통제된 접근(Controlled Access)**은 다중 접속(Multiple Access) 환경에서 단말들이 경쟁(Contention) 없이 매체를 사용할 권한을 부여받는 방식입니다. CSMA/CD (Carrier Sense Multiple Access with Collision Detection)와 같은 경쟁 방식이 "선착순"이라면, 통제된 접근은 "차례대로 발언권을 부여받는 회의"와 같습니다. 이 방식은 단말이 데이터를 전송하기 전에 반드시 승인(Authorization) 과정을 거치도록 하여, 채널 내의 충돌(Collision)을 물리적으로 불가능하게 만듭니다.

### 💡 비유
이는 **고속도로 톨게이트의 하이패스 차선과 같습니다.** 모든 차량(데이터)이 동시에 진입하려는 경쟁을 벌이는 것이 아니라, 진입권을 부여받은 차량만이 순서대로 통과하므로 진입로(채널)에서의 교착이나 사고(충돌)가 발생하지 않습니다.

### 등장 배경 및 기술적 필요성
1.  **CSMA/CD의 한계**: 이더넷(Ethernet) 환경에서 트래픽이 폭주할 경우, 충돌 발생 빈도가 증가하고 재전송(Retry)으로 인해 네트워크 대역폭 낭비가 심화되는 **쓰루풋(Throughput) 붕괴 현상**이 발생했습니다.
2.  **결정성(Determinism)의 요구**: 공장 자동화(FA)나 실시간 제어 시스템은 "언제 데이터가 도착할지 모르는" 환경을 용납할 수 없습니다. 최대 지연 시간(Max Latency)이 보장되는 예측 가능한 네트워크가 필요했습니다.
3.  **무선 매체의 히든 노드 문제**: 무선 네트워크에서는 CSMA만으로는 감지되지 않는 충돌(Hidden Node Problem)이 발생하기 때문에, 명시적인 제어 신호로 송신 시점을 조율해야 할 필요가 있었습니다.

### 📢 섹션 요약 비유
마치 **회의 시간에 사회자 없이 모두가 동시에 떠들어 본잣장이 되는 것(임의 접근)을 막기 위해, 사회자가 지명한 사람만 순서대로 의견을 개진하도록 규칙을 정한 것과 같습니다.**

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

통제된 접근의 구현은 크게 '중앙 통제형(Polling)'과 '분산 예약형(Reservation, Token Passing)'으로 나뉩니다. 각 방식의 구성 요소와 동원되는 주요 프로토콜 파라미터를 분석합니다.

### 1. 구성 요소 및 프로토콜 (표)

| 구분 | Reservation (예약) | Polling (폴링) | Token Passing (토큰 패싱) |
| :--- | :--- | :--- | :--- |
| **제어 주체** | 분산 (스케줄러/시간) | 중앙 집중 (Primary Station) | 분산 (논리적 링 구성원) |
| **핵심 객체** | 미니 슬롯 (Mini-slot) | Poll/Select 프레임 | 토큰 (Token Frame) |
| **제어 매커니즘** | 경쟁 없는 예약 비트 세팅 | 주종 관계 (Master-Slave) | 토큰 소유권 이동 |
| **주요 프로토콜** | IEEE 802.11 PCF (일부) | Bluetooth, IBM SDLC | IEEE 802.4 (Bus), 802.5 (Ring) |
| **SPOF (단일 장애점)** | 없음 | 존재 (Primary 고장 시) | 토큰 소실/복구 로직 |
| **주요 용도** | 위성 통신, 케이블 모빌 | 허브-스포크 구조 | 권역 네트워크 (MAN) |

### 2. 통제된 접근 프로토콜 상세 동작 (ASCII 다이어그램)

아래 다이어그램은 세 가지 방식이 시간 축(Time Axis) 상에서 매체를 점유하는 방식의 차이를 시각화한 것입니다.

```ascii
[시간 흐름에 따른 매체 점유 방식 비교]

1. Reservation (예약 방식)
   +-------+-------+-------+-------+-------+-------+
   | Minislots      | Data Slots (Only for Reserved) |
   +-------+-------+-------+-------+-------+-------+
   | [1][2][3][N]  | [Data A]     | [Data C]     |
   |  ^   ^   ^           (A 예약 성공)  (C 예약 성공)
   |  |   |   +-- N번: Idle
   |  |   +------ 2번: Idle
   |  +---------- 1번: 예약 요청 (Reservation Bit Set)
   >> 예약 단계에서 '나 쓸게'라고 표시하고, 데이터 단계에서 실제 전송

2. Polling (폴링 방식)
   Primary  ----->  A   ----->  B   ----->  C   ----->  Primary
   (Controller)     (Node)      (Node)      (Node)
     | Poll           | Data       | No Data    | ACK
     |<---------------|            |<-----------|
     | Select         |            |            |
     |---------------------------->| Data       |
     |<-----------------------------------------|
   >> Primary가 주도하여 A에게 "보내라(Poll)" 하고, B에게 "받아라(Select)" 함

3. Token Passing (토큰 패싱 - 링 구조)
   [A] --(Free Token)--> [B] --(Seize & Data)--> [C] --(Free Token)--> [D]
     ^                       |                        |
     |                       v                        |
     <-----------------(Data Ack/Strip)---------------|
   >> 토큰을 가진 노드만 발언권을 가짐. 논리적으로 고리 모양 순환
```

### 3. 심층 동작 원리 및 알고리즘

#### A. 예약 방식 (Reservation Access)
이 방식은 **TDMA (Time Division Multiple Access)**의 변형으로 볼 수 있습니다. 시간 프레임은 예약을 위한 작은 슬롯(Mini-slot)들의 집합과 실제 데이터 전송을 위한 정보 슬롯으로 나뉩니다.
-   **알고리즘**:
    1.  각 노드는 자신에게 할당된 미니 슬롯 시간에 '1(On)' 또는 '0(Off)' 신호를 보냅니다.
    2.  모든 노드는 채널을 감지(Listen)하여 누가 예약했는지 파악합니다.
    3.  예약 기간이 종료되면, 예약한 노드들이 할당된 순서대로 데이터를 전송합니다.
-   **오버헤드**: 데이터가 없더라도 예약 슬롯 $N$개는 항상 소모됩니다. $N$이 너무 크면 비효율적입니다.

#### B. 폴링 방식 (Polling Access)
**주국(Primary)**과 **종국(Secondary)**의 계층 구조를 가집니다.
-   **Poll Function**: Primary가 Secondary에게 송신 권한(Send Permission)을 위임하는 과정. `Poll(Polling List Address)`을 보내면 Secondary는 `Data(Info)` 혹은 `NAK(No Data)`로 응답합니다.
-   **Select Function**: Primary가 Secondary에게 수신 준비를 명령하는 과정. `Select(Addr)`을 보내면 Secondary가 `ACK(Ready)`를 보내면 Primary가 `Data`를 전송합니다.
-   **Point-to-Point Protocol (PPP)의 역할**: 이 방식은 본질적으로 1:1 연결의 집합입니다. N개의 노드를 처리하는 시간은 $N \times \text{(Round Trip Time)}$에 비례합니다.

#### C. 토큰 패싱 (Token Passing)
물리적 배치와 무관하게 논리적인 순서(Logical Ring)를 형성합니다.
-   **Logical Ring**: 물리적으로 버스(Bus)라도, 소프트웨어적으로 누가 다음 토큰을 받을지(Next Station) 주소를 가지고 있습니다.
-   **Token**: 3바이트 정도의 특수한 프레임입니다.
    1.  **Source Stripping**: 송신자가 자신이 보낸 데이터가 한 바퀴 돌아와서 회수하고 토큰을 해제함.
    2.  **Destination Stripping**: 수신자가 데이터를 가져가고 나머지 뒷부분을 송신자가 회수함 (IEEE 802.5 Ring).
-   **지연 시간**: 노드 수 $N$과 토큰 순회 시간(Rotation Time)이 곱해져 최대 대기 시간이 됩니다. 토큰 분실 시 MAC 계층에서 자동으로 토큰을 재생성하는 복구 절차가 필수적입니다.

### 4. 핵심 수식 및 코드 스니펫
토큰 링의 효율성 계산 (Single Token Mode 가정):
$$ \eta = \frac{T_{frame}}{T_{frame} + T_{overhead} + N \times T_{prop}} $$
여기서 $T_{frame}$은 프레임 전송 시간, $T_{prop}$는 노드 간 전파 지연, $N$은 노드 수입니다.

```c
// Conceptual Logic for Token Passing (Pseudo-code)
typedef struct {
    bool hasToken;
    int nextStationId;
} TokenManager;

void pass_token(TokenManager* tm, Station* stations) {
    if (tm->hasToken) {
        if (hasDataToSend()) {
            transmit_data();
            // Wait for Acknowledgment/Stripping
        }
        // Token Passing Logic
        Station* next = &stations[tm->nextStationId];
        send_frame(FRAME_TOKEN, next->id);
        tm->hasToken = false;
    }
}
```

### 📢 섹션 요약 비유
마치 **고래의 이동 경로를 통제하는 것과 같습니다.**
*   **예약 방식**: "나 지나갈게"라고 사전 신고서를 내고, 승인된 고래들만 특정 시간에 통과합니다.
*   **폴링 방식**: 교통 관제소가 각 배에 individually "지금 나와라", "너는 멈춰라"라고 지시합니다.
*   **토큰 패싱**: 오직 '통행 허가 패(토큰)'를 손에 쥐고 있는 배만이 항로에 진입할 수 있고, 통과 후에는 뒤따르는 배에게 패를 건네줍니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교 분석표

| 비교 항목 | CSMA/CD (임의 접근) | Polling (폴링) | Token Passing (토큰 패싱) |
| :--- | :--- | :--- | :--- |
| **충돌(Collision)** | 발생함 (Load $\uparrow$ $\to$ Jitter $\uparrow\uparrow$) | 발생 안 함 (No Collision) | 발생 안 함 (Collision Free) |
| **지연 시간 특성** | 비결정적 (Probabilistic) | 결정적이지만 대기 시간 길 수 있음 | 결정적 (bounded) |
| **구현 복잡도** | Low (단순 감지) | Medium (Master Logic 필요) | High (Token Mgmt, Recovery) |
| **확장성(Scalability)** | 노드 증가 시 효율 급감 | Master에 과부하 (Polling $O(N)$) | 노드 증가 시 Token 순회 시간 증가 |
| **장애 내성** | High (분산형) | **Low** (SPOF 취약) | Medium (Token 복구 로직 필요) |
| **대표적 사례** | Ethernet (Legacy) | Bluetooth, Controller Area Net | IEEE 802.5 (Token Ring), FDDI |

### 2. 과목 융합 관점 분석

#### A. 네트워크 vs 운영체제 (OS) - 락(Lock)과 폴링의 상관관계
**Polling 방식**은 네트워크 MAC 계층에서만 쓰이는 것이 아니라, **OS의 입출력(I/O) 처리 방식**과도 밀접한 관련이 있습니다.
-   **Programmed I/O (Busy Waiting)**: CPU가 직접 장치의 상태를 계속 체크하는 것(Loop)은 네트워크에서 "Polling message를 계속 보내는 것"과 유사하여 CPU 자원을 낭비합니다.
-   **Interrupt-Driven I/O**: 장치가 준비되면 CPU에게 알리는 것은 네트워크의 **Interrupt 기반 통신**과 유사합니다.
-   **DMA (Direct Memory Access)**: 이는 데이터 전송 주체가 CPU가 아닌 Controller로 넘어가는 것으로, 네트워크의 **Smart Hub/Switch**가 데이터 전송을 중재하는 것과 같습니다. 폴링 방식은 이러한 하드웨어 지원이 없는 구시스템에 적합했습니다.

#### B. 데이터통신 vs 데이터베이스 (DB) - 동시성 제어(Concurrency)
**Token Passing**의 개념은 DBMS의 **트랜잭션 동시성 제어**와 같은 철학을 공유합니다.
-   **Lock Mechanism**: DB에서 데이터 행(Row)을 수정하기 위해 Lock을 거는 것은, 네트워크에서 Token을 잡고 패킷을 보내는 것과 동일한 **Mutual Exclusion (상호 배제)** 메커니즘입니다.
-   **Deadlock**: 분산 환경의 Token Passing에서 토큰이 소실되어 모든 노드가 대기 상태에 빠지는 것은 DB의 교착상태(Deadlock)와 유사하며, 이를 해결하기 위해 **Timeout**이나 **Token Monitor** 같은 감시자가 필요