---
title: "MQTT CoAP IoT Protocol Comparison"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 606
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MQTT는 IBM/OASIS 표준(ISO/IEC 20922)의 TCP 기반 Publish/Subscribe 메시지 브로커 프로토콜로, Broker(예: Mosquitto, EMQX, HiveMQ)를 중심으로 토픽 트리(topic tree)와 3단계 QoS(QoS 0/1/2)·LWT(Last Will and Testament)·Persistent Session으로 불안정한 링크에서도 메시지 전달을 보장하며, CoAP는 IETF RFC 7252 기반 UDP/RESTful 프로토콜로 Confirmable/Non-confirmable 메시지, Observe(리소스 구독, RFC 7641), Block-wise Transfer(RFC 7959), DTLS(RFC 6347) 4모드(NoSec/PreSharedKey/RawPublicKey/Certificate)를 통해 제약 노드(클래스 1, ~10KB RAM) 환경을 지원한다.
> 2. **가치**: MQTT는 2바이트 고정 헤더와 와일드카드(`+`, `#`) 토픽으로 수십만 클라이언트의 1:N 푸시·원격 측정·모바일 푸시(Facebook Messenger가 MQTT 사용) 시나리오에서 90% 이상의 대역폭 절감을 달성하고, CoAP는 HTTP의 의미론(GET/POST/PUT/DELETE)을 4바이트 CoAP 헤더로 변환하여 6LoWPAN·Thread·Zigbee IP·LwM2M 디바이스 관리에서 코덱·헤더 압축과 결합 시 70% 이상의 패킷 오버헤드를 절감한다.
> 3. **판단 포인트**: 손실 없는 메시지 전달과 모바일/광대역 환경이면 MQTT(특히 MQTT 5.0의 Shared Subscription, Message Expiry, Request/Response 패턴), 자원 제약 센서·mesh·요청-응답 모델·LwM2M 디바이스 관리·NAT 제약 환경이면 CoAP(Observe·Block-wise·CoAP over TCP RFC 8323) 선택이 정석이며, 결정 트리는 ①전송계층(TCP vs UDP 가용성) ②메시지 패턴(1:N 푸시 vs 1:1 REST) ③QoS 요건 ④보안(TLS vs DTLS, X.509 vs PSK) ⑤연결성(항상 연결 vs 간헐 연결) ⑥헤더 압축(6LoWPAN) ⑦브로커 운영 부담의 7가지 축으로 분기한다.

---

## Ⅰ. 개요 및 필요성

IoT는 전통적인 클라이언트-서버 인터넷과 근본적으로 다른 제약을 가진다. RFC 7228(2014)이 정의한 IoT 디바이스 클래스 2(클래스 2, ~50KB RAM, ~250KB Flash) 이하의 제약 노드는 IPv4/IPv6 풀스택, TLS 1.3 풀핸드셰이크, HTTP/2의 헤더 오버헤드(HTTP 평균 700~1,400바이트 헤더)를 그대로 수용하기 어렵다. 또한 2016년 Ericsson Mobility Report 기준 셀룰러 IoT(Cat-M1, NB-IoT)는 대역폭 200kbps~1Mbps, 지연 1~10초, 패킷 손실률 1~10% 수준으로, TCP의 3-way handshake조차 비효율적이다. 무엇보다 IoT는 *사람 간*(H2H) HTTP의 Request/Response 모델이 아닌 *기계 간*(M2M) 비대칭 Publish/Subscribe 모델(예: 1개 센서 -> 1,000개 액추에이터)이 대부분이므로, 새로운 응용 계층 프로토콜이 요구되었다.

이背景下에서 MQTT(1999, IBM Andy Stanford-Clark·Arlen Nipper 설계, OASIS 3.1.1 2014 -> ISO/IEC 20922:2016)와 CoAP(2010 IETF CoRE WG -> RFC 7252 2014)가 표준화되었다. 두 프로토콜은 IETF·OASIS·oneM2M·OCF 등 복수 SDO에서 상호보완적으로 채택되며 현대 IoT 스택의 양대 축으로 자리 잡았고, **심화 학습**에서는 "주어진 IoT 시나리오에서 두 프로토콜 중 어떤 것을 선택할 것인가"를 아키텍처 의사결정 기준으로 묻는 문제가 빈출한다.

```text
[IoT 응용 계층 프로토콜 진화 및 적용 영역]
  +-----------------------------------------------------------------+
  |                전통 인터닛 vs IoT 제약 환경                     |
  +-----------------------------------------------------------------+
  |                                                                 |
  |  [전통 인터넷]                       [IoT 제약 환경]            |
  |  • 1GB RAM, GHz CPU                 • 10~50KB RAM, MHz MCU    |
  |  • 유선/고속 LTE                    • 셀룰러 IoT/LoRa/저전력 WPAN|
  |  • HTTP/TCP/TLS 1.3                 • UDP 우선, 6LoWPAN 헤더압축|
  |  • 1:1 Request/Response             • 1:N Pub/Sub, M2M 통신    |
  |           |                                      |              |
  |           v                                      v              |
  |  +-----------------+                    +------------------+   |
  |  | HTTP/1.1, 2, 3  |                    | CoAP (UDP+REST)  |   |
  |  | • 평균 헤더 800B |                    | • 4B 헤더        |   |
  |  | • TCP 의존       |                    | • RFC 7252       |   |
  |  | • 풀 핸드셰이크   |                    | • Observe·Block  |   |
  |  +-----------------+                    +------------------+   |
  |           |                                      |              |
  |           v                                      v              |
  |  +---------------------------------------------------------+   |
  |  |      MQTT (TCP + Pub/Sub, Broker 중앙집중)              |   |
  |  |   • 2B 고정 헤더 • QoS 0/1/2 • Topic 와일드카드          |   |
  |  |   • LWT, Retain, Persistent Session • MQTT 5.0 (2019)   |   |
  |  +---------------------------------------------------------+   |
  |                          |                                      |
  |                          v                                      |
  |        +------------------------------+                        |
  |        |  oneM2M·OCF·LwM2M·Thread 등   |                        |
  |        |  통합 IoT 플랫폼 (다중 프로토콜)|                       |
  |        +------------------------------+                        |
  +-----------------------------------------------------------------+

[IoT 트래픽 특성 vs 전통 HTTP]
  +-----------------+--------------+--------------+----------------+
  | 항목            | HTTP/1.1     | MQTT 3.1.1   | CoAP           |
  +-----------------+--------------+--------------+----------------+
  | 연결당 최소 패킷| SYN+SYN+ACK  | CONNECT만 1회| CON/NON 0-RTT  |
  |                 |  +TLS 4-RTT  |  (TCP+TLS)   | (DTLS 1-RTT)   |
  | 헤더 크기       | 700~1400 B   | 2~4 B        | 4 B + 옵션     |
  | 푸시 모델       | X (Polling)  | O (Push)     | O (Observe)    |
  | 패킷 손실 회복  | TCP 자동     | QoS 1/2      | CON 재전송      |
  +-----------------+--------------+--------------+----------------+
```

**기존 방식(전통 HTTP) 대비 새로운 패러다임**:
- **전통 HTTP/HTTPS**: 요청-응답, 클라이언트-서버 1:1, 매 요청마다 헤더 700B+, Keep-Alive 없으면 매번 TCP 3-way handshake -> IoT에서 *Wake-of-Radio* 에너지 낭비, 배터리가 수 시간 내 소진.
- **MQTT**: 연결 1회 후 양방향 푸시, 헤더 2B, 토픽 구독으로 N:M 라우팅 -> 1:1,000 fan-out을 단일 TCP 연결로 처리, 3단계 QoS로 신뢰성·성능 트레이드오프 제어.
- **CoAP**: UDP 기반 0-RTT 시작, 4B 헤더, REST 시맨틱 유지로 HTTP 쉬운 마이그레이션 -> 웹 개발자가 학습 비용 없이 임베디드 환경 진입, Observe로 푸시 모델 구현.

- **📢 섹션 요약 비유**: HTTP는 매번 우체국에 가서 "○○동 123번지" 주소를 써야 하는 택배 서비스이고, MQTT는 한 번 우체국에 사서함을 등록해두면 배달부가 알아서 주소를 분류해 받는 사람들에게 던져주는 시스템이며, CoAP는 초인종을 누르면 1초 안에 응답이 오고 상대가 움직이면 자동으로 다시 알려주는 스마트 인터폰과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. MQTT 아키텍처

MQTT는 **3-Tier Publish/Subscribe** 구조를 가진다. Publisher(데이터 생산자), Subscriber(데이터 소비자), Broker(중개자)가 물리적으로 분리되어 있고, Publisher와 Subscriber는 서로의 IP·포트·식별자를 알 필요가 없다. 메시지는 **토픽**(slash로 구분된 UTF-8 문자열, 예: `factory/line3/sensor/temp`)으로 식별되며, Broker는 구독 테이블을 메모리/디스크에 유지하여 매칭 라우팅을 수행한다. MQTT 3.1.1은 OASIS, 5.0(2019년 5월)은 Shared Subscription(Consumer Group), Message Expiry Interval, Correlation Data, Response Information, Reason Code, Property Bag을 추가하여 요청-응답 패턴과 마이크로서비스 메시징 브로커(Kafka 대체) 영역으로 확장되었다.

```text
[MQTT 5.0 패킷 구조 및 메시지 흐름]
  +---------------------------------------------------------------------+
  |  Publisher --- PUBLISH(topic=payload) --->  Broker (HiveMQ/EMQX)  |
  |  +----------+                              +------------------+   |
  |  | CONNECT  | -- ClientID, KeepAlive=60s --> |  Subs Tree        |   |
  |  | CONNACK   | <-- SessionPresent, Reason --- |  factory/+/temp  |   |
  |  | SUBSCRIBE | -- PacketID=1, Topic="a/b/#"  |       v match     |   |
  |  | SUBACK    | <-- PacketID=1, Reason=0x00   |  fan-out 복제     |   |
  |  | PUBLISH   | <-- QoS=2, Topic, Payload     +------------------+   |
  |  | PUBREC    | -- PacketID=2 (4-way 핸드셰이크)         |           |
  |  | PUBREL    | -- PacketID=2                +----------v--------+  |
  |  | PUBCOMP   | <-- PacketID=2               |  Subscriber N개   |  |
  |  | DISCONNECT| -- Reason=0x00(normal)      |  (모바일/서버)    |  |
  |  +----------+                              +-------------------+  |
  +---------------------------------------------------------------------+

  [MQTT 5.0 PUBLISH 패킷 바이너리 구조]
  +---------+---------+---------+---------+------------+----------+
  | Fixed    | Variable | Topic   | Packet  | Properties | Payload  |
  | Header   | Length   | Name    | ID      | (가변)     | (앱 데이 |
  | 1~2B     | 1~4B     | 2B+N    | 0~4B    | 가변        |  터)     |
  +---------+---------+---------+---------+------------+----------+
  | Byte 0: [Control(4bit)|Type(4bit)]                              |
  |   Type 1=CONNECT, 3=PUBLISH, 8=SUBSCRIBE, 14=DISCONNECT       |
  | Byte 1+: Flags (DUP, QoS=0/1/2, RETAIN for PUBLISH)             |
  +----------------------------------------------------------------+

  [MQTT QoS 전달 보장 메커니즘]
  QoS 0 (At most once) : PUBLISH ------------------> 최대 1회 (fire-and-forget)
  QoS 1 (At least once): PUBLISH --> PUBACK <-------  최소 1회 (중복 가능)
  QoS 2 (Exactly once) : PUBLISH --> PUBREC --> PUBREL --> PUBCOMP  (정확히 1회)
                          ---------------------------------------
                          4-way 핸드셰이크, 디스크/DB 영속화 필요
```

### B. CoAP 아키텍처

CoAP는 **REST 아키텍처 스타일을 UDP에 매핑**한 프로토콜이다. 4바이트 고정 헤더 + 선택적 토큰(0~8B) + 옵션(Uri-Path, Uri-Query, Content-Format, Accept, ETag, If-Match 등 TLV 인코딩) + 페이로드(0~1,024B, 블록 전송 시 더 큼) 구조이며, 4가지 메시지 타입(CON: Confirmable, NON: Non-confirmable, ACK: Acknowledgement, RST: Reset)으로 UDP의 비신뢰성을 보완한다. CON은 지수 백오프(Exponential Backoff, RFC 7252 §4.2 기본 ACK_TIMEOUT=2초, 최대 4회 재전송)로 신뢰성을, NON은 부하 절감을, Observe(RFC 7641)는 리소스 변경 시 서버가 클라이언트에게 비동기 알림을 보내 푸시를 구현한다. 블록 전송(RFC 7959)은 16비트 블록 번호(0~1,023)와 SZX(블록 크기 16~2,048B)로 페이로드를 분할·재조립한다.

```text
[CoAP 메시지 구조 및 Confirmable 흐름]
  +------------------------------------------------------------------+
  |  CoAP Header (4 bytes 고정)                                     |
  |  +------+--------+--------+----------+----------+               |
  |  | Ver=1| Type   | TKL    | Code     | MID(16b) |               |
  |  | 2bit | 2bit   | 4bit   | 8bit     |          |               |
  |  |      | CON=0  | Token  | 0.01 GET | 0x7A3F   |               |
  |  |      | NON=1  | Length | 0.02 POST|          |               |
  |  |      | ACK=2  |        | 2.05 Cont|          |               |
  |  |