---
title: "Mqtt Protocol"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
weight: 118
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MQTT는 <strong>Pub/Sub(발행/구독) 기반 경량 메시징 프로토콜</strong>로, 대역폭이 제한된 IoT 환경에서 센서 데이터를 <strong>최소 2바이트 헤더</strong>로 전송할 수 있는 사실상 IoT 메시징 표준이다.
> 2. **가치**: HTTP는 헤더만 수백 바이트이지만, MQTT는 <strong>고정 헤더 2바이트 + 가변 헤더</strong>로 페이로드 대비 오버헤드가 극히 작아 저전력·저대역폭 디바이스에 최적이다.
> 3. **판단 포인트**: QoS 3단계(0: At most once, 1: At least once, 2: Exactly once)와 <strong>Retained Message·Last Will·Topic 계층 구조</strong>를 이해하고, MQTT 5.0의 Shared Subscription(로드밸런싱)을 숙지해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    MQTT Pub/Sub 아키텍처                               |
+-------------------------------------------------------+
|  [Publisher]                [Subscriber]               |
|   센서 --publish---> Broker --subscribe---> 서버       |
|   Topic: home/sensor/temp   Topic: home/sensor/#     |
|   Payload: {"temp": 25.3}                             |
|                                                       |
|  Broker (Mosquitto, EMQX): 메시지 중개·QoS 보장      |
|  Publisher는 Subscriber를 몰라도 됨 (느슨한 결합)    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: MQTT는 우체국(Broker) 시스템이다. 보내는 사람(Publisher)은 우편함(Topic)에 넣고, 받는 사람(Subscriber)은 원하는 우편함을 구독한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### QoS 3단계

| QoS | 보장 | 오버헤드 | 용도 |
|:---|:---|:---|:---|
| **0** | At most once (최선) | **최소** | 센서 주기 데이터 |
| **1** | At least once (최소 1회) | 중간 | 알림·이벤트 |
| **2** | Exactly once (정확히 1회) | **최대** | 결제·제어 명령 |

### MQTT vs HTTP

| 비교 | HTTP | MQTT |
|:---|:---|:---|
| **헤더** | 수백 바이트 | **2바이트~** |
| **패턴** | Request/Response | **Pub/Sub** |
| **연결** | 매번 새로 | **지속 연결 (Keep-alive)** |
| <strong>IoT 적합</strong> | 부적합 | **최적** |

- **📢 섹션 요약 비유**: HTTP는 매번 전화를 걸어야 하는 통화이고, MQTT는 한 번 연결한 무전기로 계속 대화하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | MQTT | CoAP | AMQP |
|:---|:---|:---|:---|
| **전송** | TCP | UDP | TCP |
| **패턴** | Pub/Sub | Req/Res | Pub/Sub + Queue |
| **헤더** | 2B | 4B | 8B+ |
| **용도** | <strong>IoT 센서</strong> | IoT 제어 | 엔터프라이즈 MQ |

---

## Ⅳ. 실무 적용 및 실무자 판단

### MQTT 5.0 주요 개선
- **Shared Subscription**: 같은 Topic을 여러 Subscriber가 분산 처리 (로드밸런싱).
- **Request/Response**: Pub/Sub 위에 RPC 패턴 구현.
- **Properties**: 메시지에 메타데이터(Content-Type, Correlation Data) 추가.

---

## Ⅴ. 기대효과 및 결론

| 지표 | HTTP 폴링 | MQTT | 개선 |
|:---|:---|:---|:---|
| 대역폭 | 높음 | <strong>1/10~1/100</strong> | 대폭 절감 |
| 배터리 | 빠른 소모 | **절약 (지속 연결)** | IoT 적합 |
| 실시간성 | 폴링 간격 | **즉시 Push** | 실시간 |

MQTT는 AWS IoT Core·Azure IoT Hub·Google Cloud IoT의 기본 프로토콜이며, MQTT over QUIC로 더욱 빠른 전송이 진행 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Pub/Sub** | MQTT의 핵심 메시징 패턴 |
| <strong>QoS</strong> | 메시지 전달 보장 수준 (0/1/2) |
| **Broker** | Mosquitto, EMQX 등 메시지 중개 서버 |
| **Topic** | 메시지 라우팅 경로 (계층 구조) |
| <strong>CoAP</strong> | UDP 기반 IoT 대안 프로토콜 |

### 📈 관련 키워드 및 발전 흐름도

```text
[MQTT v3.1 (1999, IBM) — IoT 경량 메시징 시작]
    |
    v
[OASIS 표준화 (2014) — MQTT 3.1.1]
    |
    v
[AWS IoT Core (2015~) — MQTT 클라우드 네이티브]
    |
    v
[MQTT 5.0 (2019) — Shared Sub, Properties]
    |
    v
[현재: MQTT over QUIC — 고속 전송·멀티플렉싱]
```

### 👶 어린이를 위한 3줄 비유 설명
1. MQTT는 **우체국(Broker)** 시스템이에요. 센서가 편지(데이터)를 우편함(Topic)에 넣어요.
2. 서버는 원하는 우편함을 <strong>구독</strong>해서 편지가 오면 바로 읽어요.
3. 편지 봉투(헤더)가 **아주 작아서(2바이트)** 작은 센서도 쉽게 보낼 수 있답니다!
