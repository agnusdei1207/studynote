---
title: "Domain Event Outbox Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 231
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜잭션 경계 안에서 이벤트를 DB (Database) 에 먼저 저장하고, 별도 프로세스가 비동기로 메시지 브로커에 발행하여 이중 쓰기(Dual Write) 문제를 해결한다.
> 2. **가치**: 비즈니스 데이터 커밋과 이벤트 발행이 원자적으로 동작하므로 메시지 유실·중복 없이 Eventually Consistent(최종 일관성)를 보장한다.
> 3. **판단 포인트**: 메시지 브로커가 다운돼도 DB (Database) 에 이벤트가 남아 재발행이 가능하며, MSA (Microservices Architecture) 간 신뢰성 있는 통신의 표준 솔루션이다.

---

## Ⅰ. 개요 및 필요성
MSA (Microservices Architecture) 환경에서는 서비스 A가 트랜잭션을 커밋한 뒤 이벤트를 Kafka 같은 메시지 브로커에 발행해야 하는 상황이 매우 흔하다. 이때 전통적인 방식—비즈니스 로직 저장 -> 이벤트 발행—은 두 가지 위험을 내포한다.

1. **커밋 직후 브로커 발행 실패**: DB (Database) 에는 저장됐지만 브로커에는 도달하지 못해 이벤트가 사라진다.
2. <strong>발행 성공 후 롤백</strong>: 브로커에는 이벤트가 올라갔지만 비즈니스 트랜잭션이 롤백돼 데이터 불일치가 발생한다.

도메인 이벤트 아웃박스 패턴 (Domain Event Outbox Pattern) 은 이 두 가지 문제를 근본적으로 차단한다. 핵심 아이디어는 <strong>이벤트 발행을 비즈니스 트랜잭션과 같은 DB (Database) 트랜잭션 안에 포함시키는 것</strong>이다. 이벤트는 즉시 브로커로 가지 않고 `outbox` 테이블에 저장되며, 이후 릴레이(Relay) 프로세스나 CDC (Change Data Capture) 가 이를 읽어 브로커에 전달한다.

| 방식 | 원자성 | 유실 위험 | 중복 발행 |
|:---|:---:|:---:|:---:|
| 직접 발행 (Direct Publish) | ❌ | 높음 | 가능 |
| Outbox 패턴 | ✅ | 없음 | At-least-once (최소 1회) |
| Saga 패턴 단독 | 부분적 | 있음 | 가능 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 편지를 바로 우체통에 넣는 대신 먼저 수신함에 보관해 두고, 우편배달부가 정해진 시간에 가져가는 것과 같다. 편지(이벤트)는 절대 잃어버리지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+----------------------------------------------------------+
|                  Business Transaction                    |
|  +---------------+          +------------------------+   |
|  |  Domain Model | --저장--->|  Business Table (DB)   |   |
|  |  (비즈니스 객체)|          +------------------------+   |
|  |               | --저장--->+------------------------+   |
|  +---------------+          |  Outbox Table (DB)     |   |
|                             |  id / event_type       |   |
|                             |  payload / status      |   |
|                             +------------+-----------+   |
+------------------------------------------+---------------+
                                           | COMMIT 동시 반영
                     +---------------------v--------------+
                     |     Relay / CDC (Debezium 등)       |
                     |  미발행 row 폴링 or 변경 로그 캡처    |
                     +---------------------+--------------+
                                           | publish
                     +---------------------v--------------+
                     |     Message Broker (Kafka/RabbitMQ) |
                     +---------------------+--------------+
                                           | consume
                     +---------------------v--------------+
                     |         Consumer Service B          |
                     +------------------------------------+
```

```sql
CREATE TABLE outbox_events (
    id          UUID        PRIMARY KEY,
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id   VARCHAR(100) NOT NULL,
    event_type     VARCHAR(200) NOT NULL,
    payload        JSONB       NOT NULL,
    created_at     TIMESTAMP   NOT NULL DEFAULT NOW(),
    published_at   TIMESTAMP,
    status         VARCHAR(20) NOT NULL DEFAULT 'PENDING'
);
```

| 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| 폴링 (Polling) | 주기적으로 PENDING 행 조회 후 발행 | 구현 단순 | 지연 발생, DB 부하 |
| CDC (Change Data Capture) | Debezium 등으로 WAL (Write-Ahead Log) 변경 스트림 구독 | 실시간, DB 부하 최소 | 인프라 복잡도 증가 |

- **📢 섹션 요약 비유**: 우체국 직원이 수신함을 주기적으로 확인(폴링)하거나, CCTV(CDC)로 편지가 들어오는 순간 즉시 픽업하는 두 가지 방식의 차이다.

---

## Ⅲ. 비교 및 연결
| 패턴 | 목적 | 원자성 보장 | 복잡도 |
|:---|:---|:---:|:---:|
| Outbox Pattern | 이벤트 발행 신뢰성 | ✅ DB 트랜잭션 | 중간 |
| Saga Pattern (Choreography) | 분산 트랜잭션 조율 | 보상 트랜잭션 | 높음 |
| Transactional Messaging | MQ 내장 트랜잭션 | MQ 지원 시 ✅ | 낮음 |
| Event Sourcing | 상태를 이벤트 스트림으로 저장 | ✅ 이벤트가 원천 | 매우 높음 |

- **Outbox**: 송신 측에서 발행할 이벤트를 임시 저장
- **Inbox**: 수신 측에서 중복 수신을 방지하기 위한 멱등성 테이블 (Idempotency Store)

두 패턴을 결합하면 End-to-End (종단 간) 정확히 1번(Exactly-Once) 처리와 유사한 효과를 얻는다.

- **📢 섹션 요약 비유**: Outbox는 "보낼 편지함", Inbox는 "이미 받은 편지 목록"이다. 둘을 함께 쓰면 같은 편지를 두 번 처리하는 일이 없어진다.

---

## Ⅳ. 실무 적용 및 실무자 판단
1. <strong>주문 서비스</strong>: `ORDER_CREATED` 이벤트를 재고 서비스와 결제 서비스에 신뢰성 있게 전달
2. <strong>결제 서비스</strong>: `PAYMENT_COMPLETED` 이벤트가 유실되면 배송이 시작되지 않는 치명적 오류 -> Outbox 필수
3. <strong>알림 서비스</strong>: 선택적 이벤트이지만, 비용·UX를 위해 Outbox로 At-least-once 보장

- <strong>멱등성 처리</strong>: 릴레이가 같은 이벤트를 중복 발행할 수 있으므로 소비자 측에서 idempotent (멱등) 처리 필수
- **Outbox 테이블 정리**: 발행 완료된 행을 주기적으로 삭제하거나 아카이브하여 테이블 비대화 방지
- **모니터링**: PENDING 상태가 임계치 이상 지속되면 릴레이 장애 알림 설정

심화 학습에서 Outbox 패턴은 <strong>"MSA에서 데이터 일관성을 어떻게 보장하는가"</strong> 라는 논제와 연결된다. 2PC (Two-Phase Commit) 대비 성능 저하 없이 최종 일관성을 달성하는 실용적 해법으로 평가받는다.

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 중요한 계약서를 FedEx로 보내기 전에 복사본을 사무실 서랍에 넣어두는 것과 같다. 택배가 분실돼도 재발송할 수 있다.

---

## Ⅴ. 기대효과 및 결론
Outbox 패턴 도입의 정량적 효과:

- 이벤트 유실률 -> **0%** (DB 트랜잭션 보호)
- 장애 복구 시간 단축 -> 릴레이 재시작만으로 미발행 이벤트 자동 재처리
- 브로커 일시 다운 -> 서비스 운영에 영향 없음 (Outbox에 누적 후 발행)

MSA (Microservices Architecture) 의 분산 특성상 네트워크 장애, 브로커 재시작, 서비스 재배포는 피할 수 없다. Outbox 패턴은 이러한 <strong>불확실성을 DB 트랜잭션이라는 확실성으로 흡수</strong>하는 설계 전략이다. Event Sourcing (이벤트 소싱) 과 결합하면 시스템 전체의 감사 추적(Audit Trail)까지 완성된다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 인터넷이 끊겨도 로컬 드래프트에 저장된 이메일은 연결이 복구되면 자동으로 발송된다. Outbox는 그 드래프트 폴더다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | MSA (Microservices Architecture) | Outbox 패턴이 필요한 분산 환경 |
| 상위 개념 | Eventually Consistent (최종 일관성) | Outbox가 달성하는 일관성 모델 |
| 하위 개념 | CDC (Change Data Capture) | Outbox 릴레이의 실시간 구현체 |
| 하위 개념 | Idempotent Consumer (멱등 소비자) | Outbox의 중복 발행을 수신 측에서 처리 |
| 연관 개념 | Saga Pattern | 분산 트랜잭션 조율에 Outbox와 함께 사용 |
| 연관 개념 | Event Sourcing (이벤트 소싱) | 이벤트를 원천 데이터로 사용하는 심화 패턴 |

### 📈 관련 키워드 및 발전 흐름도
도메인 이벤트 -> 도메인 이벤트 아웃박스 패턴 -> CDC 기반 통합

### 👶 어린이를 위한 3줄 비유 설명
1. 엄마한테 쪽지를 보내고 싶을 때, 먼저 수첩에 쪽지를 적어 두는 거야.
2. 집배원 아저씨가 수첩을 보고 쪽지를 가져가서 엄마한테 전달해 줘.
3. 수첩에 적어뒀으니까 집배원이 잠깐 자리를 비워도 쪽지는 절대 안 없어져!
