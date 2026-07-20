---
title: "Google Pubsub"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 92
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Google Cloud Pub/Sub (구글 클라우드 펍섭)는 완전 관리형 비동기 메시지 서비스로, 명시적 파티셔닝 없이 글로벌 분산 처리를 지원하며 Pub/Sub 의 발행-구독(Publish-Subscribe) 패턴으로 느슨한 결합(Loose Coupling) 아키텍처를 구현한다.
- **가치**: Kafka나 Kinesis와 달리 파티션/샤드 수를 사전 계획하지 않아도 되며, 트래픽에 따라 자동으로 확장되므로 GCP 생태계(Dataflow, BigQuery, Cloud Run)에서 최단 시간으로 스트리밍 파이프라인을 구축할 수 있다.
- **판단 포인트**: Pub/Sub는 At-Least-Once 배달을 기본 제공하며 Exactly-Once는 Dataflow와 함께 구현해야 한다. 또한 메시지 순서 보장(Ordering)이 기본이 아니므로, 순서가 중요한 워크로드는 Ordering Key 설정이 필요하다.

---

## Ⅰ. 개요 및 필요성

### 1. Pub/Sub 기본 개념

```
발행자 (Publisher)  ->  토픽 (Topic)  ->  구독 (Subscription)  ->  구독자 (Subscriber)

메시지 흐름:
  Publisher A ----> topic: "orders" ----> subscription: "order-processor" ----> Consumer
                                     +---> subscription: "audit-log"      ----> Consumer
                                     +---> subscription: "analytics"       ----> Consumer

-> 하나의 토픽에서 여러 구독(Subscription)으로 팬아웃(Fan-Out) 지원
-> 각 Subscription은 독립적으로 메시지를 처리
```

### 2. Pub/Sub vs Kafka vs Kinesis

| 항목 | Google Pub/Sub | Apache Kafka | Amazon Kinesis |
|:---|:---|:---|:---|
| 파티션 관리 | 없음 (자동) | 수동 설정 | 샤드 수동 |
| 순서 보장 | Ordering Key 사용 시 | 파티션 내 보장 | 샤드 내 보장 |
| 배달 보장 | At-Least-Once (기본) | At-Least-Once | At-Least-Once |
| 보존 기간 | 최대 7일 (기본 7일) | 무제한 | 24h~365일 |
| 글로벌 분산 | ✅ 기본 | 별도 설정 필요 | 리전별 독립 |
| 운영 방식 | 완전 관리형 | 자체 운영/MSK | 완전 관리형 |

**📢 섹션 요약 비유**
> Pub/Sub는 "라디오 방송국(Topic)과 청취자(Subscription)"와 같다. 방송국은 신호를 보내고, 원하는 청취자 누구든 채널(구독)을 맞추면 들을 수 있다. 청취자가 늘어도 방송국은 더 많은 장비를 설치할 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Pub/Sub 내부 아키텍처

```
+-------------------------------------------------------------+
|  Google Pub/Sub 글로벌 인프라                                |
|                                                             |
|  Publisher ---> Frontend 서버 (수신) ---> 메시지 스토리지      |
|                                         (전 세계 복제)       |
|                                              |              |
|                                              v              |
|  구독자가 Pull:  Subscriber <--- Pull API <--- 구독 레이어    |
|  Push 모드:      구독 레이어 ---- HTTP/gRPC 푸시 ---> 엔드포인트|
+-------------------------------------------------------------+
```

### 2. Push vs Pull 모드

| 모드 | 동작 | 사용 상황 |
|:---|:---|:---|
| Pull | Subscriber가 능동적으로 메시지 요청 | 처리 속도 조절 필요, 백엔드 서비스 |
| Push | Pub/Sub가 엔드포인트로 HTTP 전송 | 서버리스(Cloud Run/Functions), 웹훅 |

```python
# Pull 모드 Python 예시
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("project-id", "subscription-name")

def callback(message):
    print(f"수신: {message.data}")
    message.ack()  # 처리 완료 확인 (Ack)

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
```

### 3. Ordering Key (순서 보장)

```python
# 순서 보장이 필요한 경우: Ordering Key 사용
publisher = pubsub_v1.PublisherClient(
    client_options={"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
)

# 같은 ordering_key의 메시지는 순서 보장
future = publisher.publish(
    topic_path,
    data=b"order event",
    ordering_key="user-001"   # 이 키로 전달되는 메시지는 순서 보장
)
```

**📢 섹션 요약 비유**
> Pull 모드는 "뷔페 식당(원하는 만큼 가져옴)", Push 모드는 "코스 요리(정해진 시간에 요리가 나옴)"다. 배가 부를 때(처리 느림) 뷔페는 기다리면 되지만, 코스는 요리가 계속 나온다.

---

## Ⅲ. 비교 및 연결

### 1. GCP Dataflow와의 통합

Pub/Sub는 Apache Beam 기반의 GCP Dataflow (구글 데이터플로)와 함께 사용할 때 Exactly-Once 처리가 가능하다.

```
Pub/Sub -> Dataflow (Apache Beam) -> BigQuery / GCS / Bigtable

특징:
  - Dataflow가 Pub/Sub 오프셋을 관리하여 Exactly-Once 보장
  - 자동 스케일링: 메시지 양에 따라 워커 자동 증감
  - 통합 모니터링: Cloud Monitoring
```

### 2. Pub/Sub Lite vs Pub/Sub

| 항목 | Pub/Sub | Pub/Sub Lite |
|:---|:---|:---|
| 비용 | 높음 (글로벌 분산) | 낮음 (단일 존) |
| 순서 보장 | Ordering Key | 파티션 내 보장 |
| 보존 기간 | 최대 7일 | 무제한 (스토리지 비용) |
| 사용 사례 | 범용, 고가용성 | 비용 최적화, Kafka 대체 |

**📢 섹션 요약 비유**
> Dataflow + Pub/Sub는 "공항 입국 심사대(Dataflow)"가 모든 승객(메시지)을 정확히 한 번 검사하는 것과 같다. 심사관이 없으면 같은 승객이 두 번 들어올 수 있다(At-Least-Once).

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Pub/Sub 설계 체크리스트

- [ ] 순서 보장 필요 시 `ordering_key` 설정 + `enable_message_ordering` 구독 설정
- [ ] Ack Deadline 설정: 처리 시간 + 여유 (기본 10초, 최대 600초)
- [ ] Dead Letter Topic (DLT) 설정: 일정 횟수 Ack 실패 시 DLT로 이동
- [ ] Subscription Filter: 토픽에서 일부 메시지만 받을 때 사용
- [ ] 메시지 보존 기간 = 최대 소비 지연 + 여유

### 2. Exactly-Once 보장 방법

```
방법 1: Dataflow 파이프라인 사용
  Pub/Sub -> Dataflow -> BigQuery
  Dataflow가 checkpoint 기반으로 Exactly-Once 보장

방법 2: 멱등적 Consumer
  Consumer에서 message_id 기반 중복 처리 방지
  Cloud Spanner/Firestore에 처리 이력 저장
```

**📢 섹션 요약 비유**
> Pub/Sub의 DLT(Dead Letter Topic)는 "반품 창고"와 같다. 처리 실패한 메시지(반품 물건)를 무한히 재시도하지 않고 별도 창고(DLT)에 모아 나중에 수동으로 처리한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 운영 단순화 | 파티션 관리 없이 자동 확장 |
| GCP 통합 | Dataflow/BigQuery/Cloud Run 네이티브 연동 |
| 글로벌 분산 | 단일 설정으로 다중 리전 고가용성 |

### 2. 결론

Google Pub/Sub는 GCP 생태계에서 <strong>운영 부담이 최소화된 완전 관리형 메시지 서비스</strong>다. 학습 정리에서는 명시적 파티션 없는 자동 스케일링, Push/Pull 모드 차이, Ordering Key를 통한 순서 보장, Dataflow와의 Exactly-Once 연계를 서술하면 된다.

**📢 섹션 요약 비유**
> Pub/Sub는 GCP의 "우편 시스템"이다. 보내는 사람(Publisher)은 주소(토픽)에 편지를 넣기만 하고, 받는 사람(Subscriber)은 구독을 통해 편지를 가져간다. 우편 배달부(GCP 인프라)는 보이지 않지만 항상 신뢰할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Apache Kafka | 비교 대상 | 오픈소스 대안, 더 세밀한 제어 |
| Amazon Kinesis | 경쟁 서비스 | AWS 생태계의 동등 포지션 서비스 |
| GCP Dataflow | 통합 처리 | Exactly-Once 보장을 위한 파트너 서비스 |
| Apache Beam | 연산 모델 | Dataflow의 프로그래밍 모델 |
| Dead Letter Topic | 운영 패턴 | 처리 실패 메시지 격리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 메시지 큐 (MQ, Message Queue) — FIFO 브로커, 단일 소비자, 확장성 제한]
    |
    v
[발행-구독 패턴 (Pub/Sub Pattern) — 토픽 기반 다수 구독자 분리, 비동기 이벤트]
    |
    v
[Google Pub/Sub — 글로벌 분산 관리형 메시지 서비스, 99.99% SLA, 자동 확장]
    |
    v
[Apache Kafka — 오프셋 기반 영속 로그, 스트림 재처리 지원, 자체 운영 필요]
    |
    v
[Dataflow (Apache Beam) — Pub/Sub 연동 서버리스 스트림 처리, 자동 파이프라인]
    |
    v
[BigQuery Streaming Insert — Pub/Sub->Dataflow->BigQuery 실시간 분석 파이프라인]
```
이 흐름은 전통 메시지 큐의 확장성 한계를 Pub/Sub 패턴으로 극복하고, GCP 관리형 서비스와 서버리스 스트림 처리로 연결되는 실시간 이벤트 파이프라인 아키텍처의 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

Google Pub/Sub는 학교 방송부(토픽)와 같아요. 방송부(Publisher)가 마이크에 대고 말하면(메시지 발행), 귀를 기울이고 있는 친구들(Subscriber)이 모두 듣는 구독 시스템이에요. 듣는 친구가 10명이든 1000명이든 방송부는 마이크 하나로 충분하고, 방송 시스템(GCP)이 알아서 신호를 전달해줘요!
