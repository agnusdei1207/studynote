---
title: "MQTT CoAP IoT Lightweight Protocols"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 489
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MQTT(Message Queuing Telemetry Transport)와 CoAP(Constrained Application Protocol)은 제한된 IoT 환경을 위해 설계된 두 가지 경량 메시지 프로토콜로, MQTT는 TCP 기반 Pub/Sub 패턴, CoAP는 UDP 기반 RESTful 패턴을 사용한다.
> 2. **가치**: HTTP/WebSocket 대비 수십 배 낮은 오버헤드로 수백만 IoT 기기의 안정적·저전력 메시지 교환을 실현하며, 두 프로토콜의 특성 차이를 이해해야 올바른 IoT 아키텍처를 설계할 수 있다.
> 3. **판단 포인트**: 안정적인 이벤트 스트림·다수 구독자 시스템엔 MQTT, 자원 제약 기기의 단순 요청-응답·배터리 절약엔 CoAP가 적합하다. 두 프로토콜을 혼합하는 게이트웨이 패턴도 실무에서 자주 사용된다.

---

## Ⅰ. 개요 및 필요성

<strong>IoT 프로토콜의 필요성</strong>

HTTP는 헤더 오버헤드가 수백~수천 바이트에 달해, RAM이 수십 KB에 불과한 MCU(Micro Controller Unit)에서 동작하기 어렵다. IoT 환경에서는 아래 조건을 모두 만족하는 프로토콜이 필요하다.

- 패킷 크기: 수 바이트 수준의 최소 헤더
- 신뢰성: 불안정한 무선 환경에서도 전달 보장
- 저전력: 배터리 기기에서 수년간 동작
- 확장성: 수백만 기기 동시 접속

- **📢 섹션 요약 비유**: HTTP는 백과사전 편지다. 질문 하나에 표지·목차·각주까지 다 포함해서 보낸다. MQTT/CoAP는 엽서다. 핵심 내용 한 줄만 담아 가볍고 빠르게 전달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------+
|         MQTT Pub/Sub 구조 vs CoAP 요청-응답 구조 비교         |
+--------------------------+---------------------------------+
|         MQTT             |           CoAP                  |
|  [Publisher(발행자)]      |  [CoAP Client]                  |
|       |                  |       | GET/PUT/POST/DELETE      |
|       v  토픽(Topic)      |       v                         |
|  [Broker(브로커)]         |  [CoAP Server]                  |
|       |                  |  (자원 URI: /sensor/temp)        |
|       v  구독(Subscribe)  |                                 |
|  [Subscriber(구독자)]     |  [Observe 옵션]                  |
|  (다수의 클라이언트)        |  (변경 시 자동 알림 -> Push)       |
+--------------------------+---------------------------------+
```

### MQTT vs CoAP 핵심 비교표

| 항목 | MQTT | CoAP |
|:---:|:---:|:---:|
| 전송 계층 | TCP | UDP |
| 통신 패턴 | Pub/Sub (브로커 필수) | RESTful 요청-응답 |
| 헤더 크기 | 최소 2바이트 | 4바이트 |
| 신뢰성 | TCP 기반 보장 | CON(확인)/NON(비확인) 옵션 |
| 멀티캐스트 | 미지원 | 지원 (UDP 특성) |
| 브로커 | 필수 (Mosquitto, HiveMQ) | 불필요 (P2P 가능) |
| 보안 | TLS | DTLS |
| 적합 환경 | 안정적 네트워크, 다수 구독 | 제약적 기기, 저전력 |

<strong>MQTT QoS(Quality of Service) 3단계</strong>

- <strong>QoS 0 (At most once)</strong>: 전달 보장 없음. 손실 허용 센서 데이터.
- <strong>QoS 1 (At least once)</strong>: 최소 1회 전달. 중복 가능. 대부분의 IoT 이벤트.
- <strong>QoS 2 (Exactly once)</strong>: 정확히 1회 전달. 금융·의료 트랜잭션. 오버헤드 최대.

<strong>CoAP 특징</strong>

- **Observe 옵션**: 클라이언트가 서버 자원을 구독하면, 값 변경 시 서버가 자동으로 알림 전송. MQTT의 Push와 유사한 효과를 UDP로 구현.
- **CON/NON 메시지**: CON(Confirmable)은 ACK 수신까지 재전송. NON(Non-confirmable)은 단방향 전송, 저전력.

- **📢 섹션 요약 비유**: MQTT 브로커는 라디오 방송국이다. 기상청(Publisher)이 날씨를 방송하면, 수백만 라디오(Subscriber)가 동시에 수신한다. CoAP는 편의점 주문이다. 손님(Client)이 "콜라 주세요(GET)" 하면 직원(Server)이 바로 건네준다.

---

## Ⅲ. 비교 및 연결

<strong>MQTT와 CoAP 선택 기준</strong>

| 조건 | 선택 |
|:---|:---:|
| 다수의 구독자가 동일 데이터 필요 | MQTT |
| 기기가 초소형·배터리 극제약 | CoAP |
| 안정적인 TCP 네트워크 환경 | MQTT |
| 불안정한 무선 환경, 멀티캐스트 필요 | CoAP |
| 클라우드 IoT 플랫폼 연동 | MQTT (표준화 진행 중) |
| M2M(Machine-to-Machine) 직접 통신 | CoAP |

**혼합 아키텍처**: 현장 기기(CoAP) ↔ 엣지 게이트웨이(CoAP->MQTT 변환) ↔ 클라우드 MQTT 브로커. 제약 기기는 CoAP로 게이트웨이에 보내고, 게이트웨이가 MQTT로 변환해 클라우드에 전달.

- **📢 섹션 요약 비유**: MQTT와 CoAP를 함께 쓰는 것은 지역 버스(CoAP)와 고속버스(MQTT)를 환승하는 것이다. 마을에서 지역 버스(CoAP)로 나오고, 터미널(게이트웨이)에서 고속버스(MQTT)로 갈아탄다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>프로토콜 선택 시나리오</strong>

| 시나리오 | 프로토콜 | 이유 |
|:---|:---:|:---|
| 스마트홈 조명 상태 실시간 동기화 | MQTT | 다수 앱 구독, 안정 네트워크 |
| 초소형 온도 센서 (CR2032 배터리) | CoAP NON | 최소 전력, 단방향 |
| 공장 생산 라인 이벤트 스트림 | MQTT QoS 1 | 이벤트 유실 불가 |
| 설비 제어 명령 전송 (확인 필수) | MQTT QoS 2 / CoAP CON | 정확 1회 전달 |

**보안 포인트**: MQTT는 TLS 1.3, CoAP는 DTLS(Datagram TLS). 인증서 저장 불가 기기는 PSK(Pre-Shared Key) 방식 사용.

- **📢 섹션 요약 비유**: QoS 선택은 택배 보험 선택이다. 보험 없음(QoS 0)은 싸지만 분실 위험, 기본 보험(QoS 1)은 재배송은 하지만 중복 도착 가능, 풀 보험(QoS 2)은 정확하지만 수수료가 가장 비싸다.

---

## Ⅴ. 기대효과 및 결론

MQTT와 CoAP는 IoT 생태계의 메시지 교환 표준으로 자리 잡았다. AWS IoT Core·Azure IoT Hub 모두 MQTT를 네이티브 지원하며, CoAP는 LwM2M(Lightweight M2M) 디바이스 관리 프로토콜의 기반이다. 두 프로토콜의 특성과 트레이드오프를 명확히 이해하는 것이 IoT 아키텍처 설계의 기본기다.

- **📢 섹션 요약 비유**: MQTT와 CoAP는 IoT 세계의 한글과 영어다. 상황에 맞게 골라 쓰면 되고, 둘 다 알면 어떤 시스템도 설계할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| MQTT Broker | Mosquitto, HiveMQ, EMQ · 메시지 중계 서버 |
| QoS 3단계 | 0/1/2, 오버헤드 · 전달 보장 수준 |
| CoAP Observe | Push, UDP · 서버 자원 변경 자동 알림 |
| LwM2M | CoAP 기반 · OMA 기기 관리 프로토콜 |
| DTLS | CoAP 보안 · UDP 위 TLS 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Mosquitto · HiveMQ] -> [MQTT Pub · Sub] -> [CoAP 보안 · UDP 위 TLS 계층]
```

### 👶 어린이를 위한 3줄 비유 설명

1. MQTT는 학교 방송 시스템이에요. 선생님(Publisher)이 마이크(Broker)에 말하면 전교생(Subscriber)이 동시에 들을 수 있어요.
2. CoAP는 학생증 조회기예요. 카드 대면(요청)하면 즉시 결과(응답)를 알려줘요. 따로 방송국이 없어도 돼요.
3. QoS는 알림 설정이에요. 중요한 수업 알림(QoS 2)은 반드시 읽음 확인, 날씨 알림(QoS 0)은 그냥 와도 되고 없어져도 괜찮아요.
