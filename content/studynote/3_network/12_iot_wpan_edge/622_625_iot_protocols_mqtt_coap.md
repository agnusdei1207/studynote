+++
title = "622-625. IoT 메시징 프로토콜: MQTT와 CoAP"
date = "2026-03-14"
[extra]
category = "IoT & Edge"
id = 622
+++

# 622-625. IoT 메시징 프로토콜: MQTT와 CoAP

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **MQTT (Message Queuing Telemetry Transport)**는 TCP 기반의 Pub/Sub 구조로 신뢰성을, **CoAP (Constrained Application Protocol)**는 UDP 기반의 REST 구조로 경량성을 극대화하여 IoT의 제약된 환경을 극복합니다.
> 2. **가치**: MQTT는 대규모 네트워크에서 메시지 라우팅 오버헤드를 획기적으로 줄여 **Scalability(확장성)**를 확보하며, CoAP는 IP 네트워크상에서 HTTP 계층의 무거움을 제거하여 **Low-latency(지연 시간 최소화)**를 실현합니다.
> 3. **융합**: MQTT는 빅데이터 파이프라인(Apache Kafka 등)과 연동하여 이기종 시스템 간 데이터 통합 버스로, CoAP는 웹 표준과의 호환성을 통해 M2M(Machine-to-Machine) 자동화 제어 계층으로 진화하고 있습니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
사물인터넷(IoT, Internet of Things) 환경은 전력, 대역폭, 연산 능력이 극도로 제약된 **Constrained Device(제약 장치)**들이 네트워크를 형성하는 영역입니다. 기존의 **HTTP (Hypertext Transfer Protocol)**는 헤더가 크고(Connection-oriented, Heavy text), 연결 유지에 드는 리소스가 많아 MCU(Micro Controller Unit) 수준의 임베디드 시스템에는 부담스러운 프로토콜입니다. 이를 해결하기 위해 등장한 것이 **MQTT**와 **CoAP**입니다. 두 프로토콜은 모두 "오버헤드 제거"라는 공통의 목적을 가지나, 접근 방식에서 결정적인 차이를 보입니다.

*   **MQTT**: "중앙 집중형 허브" 개념. 메시지를 라우팅하는 브로커(Broker)를 두어 발행자(Publisher)와 구독자(Subscriber)를 완전히 분리합니다.
*   **CoAP**: "분산형 클라이언트" 개념. 웹의 철학을 유지하되 헤더를 압축하고 UDP를 사용하여 단대단(End-to-End) 통신을 수행합니다.

#### 등장 배경 및 요구사항
1.  **기존 한계**: HTTP의 1회 요청당 1회 응답 모델과 무거운 TCP/IP 스택은 배터리 수명을 단축시키고 네트워크 트래픽을 증가시켰습니다.
2.  **혁신적 패러다임**: IoT에서는 'Pull 방식(내가 원할 때 가져옴)'보다 상태 변화를 즉시 알리는 'Push 방식(상태가 바뀌면 보냄)'이 더 효율적입니다. MQTT는 이를 Pub/Sub로, CoAP는 Observe(관찰) 기능으로 구현했습니다.
3.  **현재 비즈니스 요구**: 스마트 팩토리, 스마트 시티 등 수만 개의 센서가 실시간으로 연결되는 환경에서 **Message Queue(메시지 큐)** 기반의 비동기 통신과 낮은 지연 시간(Low Latency)의 제어 신호 전송이 필수적이 되었습니다.

```ascii
┌─────────────────────────────────────────────────────────────────────┐
│                      IoT Protocol Evolution                         │
├─────────────────────────────────────────────────────────────────────┤
│   [PC Era]              [Mobile Era]           [IoT Era]            │
│   HTTP / TCP            HTTP Keep-Alive        MQTT / CoAP          │
│  (Heavy, Full Stack)    (Optimized Web)        (Lightweight)        │
│                                                                     │
│  ────▶  데이터 양: GB 단위      ────▶  MB 단위      ────▶  Byte 단위 │
│  ────▶  전력: 상시 전력         ────▶  배터리 사용    ────▶  초저전력 │
└─────────────────────────────────────────────────────────────────────┘
```
*(도입 배경 다이어그램: 각 에포크별 프로토콜의 특성과 데이터/전력 트렌드를 도식화)*

📢 **섹션 요약 비유**: 마치 **택배 시스템**이 진화하는 것과 같습니다. 초기(PC 시대)에는 물건을 보낼 때마다 운전자가 직접 전화해주고 영수증을 받았다면, 모바일 시대에는 앱으로 추적했습니다. 이제 IoT 시대(MQTT/CoAP)는 소포 하나(Byte)를 보내도 배송비를 최대한 아끼고, 분류 센터(Broker)를 통해 수천 명에게 동시에 배송하거나, 옆 집에 택배를 던져주듯 즉시 전달(UDP)하는 초고효율 시스템이 필요해진 것입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 분석
| 구분 | 요소명 | 역할 및 내부 동작 | 프로토콜/포트 | 비유 |
|:---:|:---|:---|:---:|:---|
| **MQTT** | **Broker** | 메시지 허브. 발행된 메시지의 Topic(주제)을 구독하는 클라이언트에게 필터링하여 전송. QoS 처리 및 세션 관리 담당. | TCP / 1883 | **신문사 배달 센터** |
| | **Client** | Publisher(발행자)와 Subscriber(구독자)를 통칭. Broker에만 연결되면 되며 상대방을 알 필요가 없음. | TCP / 8883(SSL) | **기자 / 독자** |
| | **Topic** | 계층적 구조를 가진 메시지 주소 체계(예: `home/livingroom/temp`). 와일드카드(`+`, `#`) 사용 가능. | - | **신문면(섹션)** |
| **CoAP** | **Client** | 요청을 보내는 주체(GET/POST/PUT/DELETE). M2M 통신에서의 마스터(Master) 역할. | UDP / 5683 | **손님(주문자)** |
| | **Server** | 리소스(센서값 등)를 가진 노드. 요청을 처리하고 응답. Observe 서버로 동작 시 상태 푸시 가능. | UDP / 5684(DTLS) | **편의점 점원** |
| | **Resource** | URI로 식별되는 데이터(예: `coap://sensor/temp`). 웹의 URL과 유사한 구조. | - | **상품(진열대)** |

#### 2. MQTT: Pub/Sub 구조 및 QoS 메커니즘
MQTT의 핵심은 **비동기 메시징**입니다. 발행자는 브로커에게만 메시지를 보내고, 구독자는 브로커에게서만 메시지를 받습니다. 이 **Decoupling(결합도 제거)** 덕분에 네트워크 상태가 불안정하거나 장치가 켜지지 않아도 브로커가 메시지를 보관(QoS 1, 2)했다가 전송합니다.

*   **QoS (Quality of Service) Levels**: 네트워크 신뢰도에 따라 3단계로 선택 가능합니다.
    *   **QoS 0 (At most once)**: "Fire and Forget". 확인 절차 없이 보냄. 데이터가 소실되어도 상관없는 센서 데이터(예: 초당 1000회 전송하는 온도)에 사용.
    *   **QoS 1 (At least once)**: 메시지 중복은 허용하나 누락은 없음. Handshake(Message ID) 사용.
    *   **QoS 2 (Exactly once)**: 중복도 없고 누락도 없음. 4단계 핸드셰이크(PUBREC, PUBREL 등)로 완벽한 신뢰성 보장. 거래 데이터 등에 사용.

```ascii
    [Publisher A]           [Broker]            [Subscriber B]
         |                        |                     |
         |---(CONNECT)----------->|<---(CONNECT)--------|
         |                        |                     |
         |---(PUBLISH: temp/1)    |                     |
         |   [QoS 1: Packet ID=1]|                     |
         |   -------------------->|                     |
         |                       |--(Filter Match)---->|
         |                        |---(PUBLISH: temp/1)|
         |                        |   [QoS 1: ID=1]    |
         |                        |   ---------------->|
         |                        |                     |
         |<-(PUBACK: ID=1)--------|<---(PUBACK: ID=1)---|
         |    (Flow Complete)     |                     |
```
*(MQTT QoS 1 흐름도: 메시지 ID를 통한 확인 절차)*

#### 3. CoAP: RESTful 아키텍처 및 UDP 튜닝
CoAP는 **"Web Protocol for Constrained Nodes"** 설계 철학을 따릅니다. HTTP의 Method(GET, POST, PUT, DELETE)와 Response Code(2.05 Content, 4.04 Not Found 등)를 그대로 차용하되, 전송 계층을 UDP로 변경하여 **CoAP (Constrained Application Protocol)** 스스로 신뢰성 계층을 구현합니다.

*   **Message Format**: 4바이트의 고정 헤더와 토큰(Token), 옵션(Option), 페이로드로 구성. 기본 헤더만 4바이트로 압축.
*   **Confirmable (CON) vs Non-confirmable (NON)**:
    *   **CON 메시지**: 신뢰성이 필요한 경우. 전송 후 ACK를 기다림.
    *   **NON 메시지**: 단순 알림. ACK 없음.
*   **Observe (RFC 7641)**: HTTP의 Long-polling이나 WebSocket 없이 서버의 상태(Restate)가 변경될 때마다 클라이언트로 푸시(Push)할 수 있는 기능.

```ascii
    [CoAP Client]                       [CoAP Server]
         |                                     |
         |---(CON GET /temperature)---------->|
         |   [Token: 0x4a, Message ID: 0x01]  |
         |                                     |
         |                                     | (Process Request)
         |                                     |
         |<--(ACK 2.05 Content)---------------|
         |   [Token: 0x4a, Message ID: 0x01]  |
         |   [Payload: 25.5 C]                |
```
*(CoAP 기본 요청/응답 흐름: CON 메시지에 대한 piggybacked ACK)*

#### 4. 핵심 알고리즘 및 코드 스니펫 (Topic 구독 필터링)
MQTT Broker의 핵심은 트라이(Trie) 자료구조를 이용한 Topic 매칭 알고리즘입니다. 와일드카드 처리 로직 예시 (Python 스타일 의사코드):

```python
def match_subscription(topic, subscription):
    """
    MQTT Topic 와일드카드 매칭 로직
    :param topic: 발행된 주제 (e.g., "home/living/temp")
    :param subscription: 구독 패턴 (e.g., "home/+/temp")
    """
    topic_parts = topic.split('/')
    sub_parts = subscription.split('/')

    # 레벨별 매칭
    for i, part in enumerate(sub_parts):
        if part == '#':
            # '#'는 뒤에 오는 모든 것과 매칭 (Multi-level wildcard)
            return True
        if i >= len(topic_parts):
            return False
        if part == '+' or part == topic_parts[i]:
            # '+'는 단일 레벨 와일드카드 (Single-level wildcard)
            continue
        return False
        
    # 길이가 정확히 일치해야 함 (단, '#' 처리는 위에서 됨)
    return len(topic_parts) == len(sub_parts)
```

📢 **섹션 요약 비유**: **MQTT**는 '마이크(MIC)'와 '스피커(Speaker)'를 분리한 **라디오 방송국**입니다. 방송국(Broker)이 채널(Topic)을 관리하므로, 청취자(Subscriber)가 늘어나도 방송국 출력만 키우면 되는 구조입니다. 반면 **CoAP**는 '창구'를 거치지 않는 **무전기 통신**입니다. 상대방이 누군지 정확히 알고(Check) 호출을 하면, 즉시 응답(Roger)하는 구조로, 대화가 끊겨도 "왈!" 하고 다시 부르면 됩니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 (Matrix)

| 비교 항목 | MQTT (Message Queuing Telemetry Transport) | CoAP (Constrained Application Protocol) |
|:---|:---|:---|
| **전송 계층** | **TCP** (연결 지향형) | **UDP** (비연결형) |
| **통신 패러다임** | **Pub/Sub (N:N)** | **Request/Response (1:1)** |
| **헤더 오버헤드** | 2 Byte (최소) | 4 Byte (최소) |
| **신뢰성 메커니즘** | TCP의 신뢰성 + QoS 계층(0,1,2) 라우팅 | Application 레벨의 CON/NON 메시지 및 재전송 |
| **핸드셰이크 비용** | 3-Way Handshake (TCP) + MQTT Connect | 없음 (Connectionless) |
| **멀티캐스트 지원** | 브로커를 통한 논리적 멀티캐스트 | IP Multicast 지원 가능 (RFC 7390) |
| **보안** | TLS 기반 **MQTTS** (Port 8883) | DTLS 기반 **CoAPs** (Port 5684) |
| **주요 용도** | 대규모 데이터 수집, 제어령 분산, 네트워크 불안정 환경 | 리소스 제어, 상태 조회, 단순 액추에이터 제어 |

#### 2. 수학적 성능 분석 (오버헤드 관점)
*   **TCP 오버헤드 (MQTT)**: 연결 설정 시 $3 \times RTT$ (Round Trip Time) 소요. 연결을 유지해야 하므로 대기 장치가 많을 때 서버의 **File Descriptor (파일 디스크립터)** 소모가 큼. 하지만 일단 연결되면 Keep-Alive로 메시지 전송이 매우 가벼움.
*   **UDP 오버헤드 (CoAP)**: 연결 설정 비용 0. 하지만 신뢰성이 필요한 경우 매번 CON-ACK 과정이 필요하며, 패킷 손실이 잦은 네트워크에서는 재전송으로 인해 전체 대역폭 효율이 떨어질 수 있음.

#### 3. 타 과목 융합 분석
*   **네트워크 (Network)**: MQTT는 TCP의 혼잡 제어(Congestion Control)에 영향을 받아 급격한 트래픽 몰림(Thundering Herd)