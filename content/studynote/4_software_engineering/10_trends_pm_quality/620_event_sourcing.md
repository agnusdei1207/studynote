+++
title = "620. 이벤트 소싱 (Event Sourcing) 상태 재생 가능성 보장"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 이벤트 소싱 (Event Sourcing) 상태 재생 가능성 보장

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 상태(State)를 저장하는 대신 **상태 변경 이벤트(Event)를 순차적으로 저장**하여, 언제든지 과거 시점으로 상태를 재생(Replay) 가능하게 하는 패턴
> 2. **가치**: 감사 가능한Audit Trail, 시간 여행(Debugging), CQRS와의 자연스러운 결합 → 복잡한 비즈니스 로직 투명화
> 3. **융합**: CQRS, Event Store, Projections, Saga Pattern과 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**이벤트 소싱 (Event Sourcing)**은 Martin Fowler가 정의한 패턴으로, **"애플리케이션의 상태를 저장하는 대신, 상태를 변경시킨 이벤트의 순차적인 로그를 저장"**하는 방식입니다.

전통적인 CRUD 방식에서는 현재 상태(Current State)를 데이터베이스에 저장하지만, 이벤트 소싱에서는 **상태 변경 이벤트(State Transition Event)**를 불변 로그(Immutable Log)로 저장합니다. 필요할 때 이벤트를 **재생(Replay)**하여 현재 상태를 도출합니다.

```
┌─────────────────────────────────────────────────────────────┐
│            CRUD vs Event Sourcing 비교                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [CRUD 방식 - 현재 상태 저장]                              │
│  ┌─────────────────────────────────────────────┐           │
│  │  Database                                 │           │
│  │  ┌─────────────────────────────────────┐   │           │
│  │  │  ORDER table                         │   │           │
│  │  │  ┌────┬──────┬───────┬──────────┐  │   │           │
│  │  │  │ id │status│amount│updated_at│  │   │           │
│  │  │  ├────┼──────┼───────┼──────────┤  │   │           │
│  │  │  │ 1  │PAID  │10000 │2024-01-15│  │   │           │
│  │  │  └────┴──────┴───────┴──────────┘  │   │           │
│  │  └─────────────────────────────────────┘   │           │
│  │  [문제점] 과거 이력 추적 불가, 덮어쓰기           │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Event Sourcing - 이벤트 로그 저장]                       │
│  ┌─────────────────────────────────────────────┐           │
│  │  Event Store (Immutable Log)              │           │
│  │  ┌─────────────────────────────────────┐   │           │
│  │  │  ORDER-123 events                   │   │           │
│  │  │  1. OrderCreated (amount: 10000)    │   │           │
│  │  │  2. PaymentCaptured (pg_id: ABC)   │   │           │
│  │  │  3. ShipmentStarted (tracking: ...) │   │           │
│  │  │  4. OrderCompleted                  │   │           │
│  │  └─────────────────────────────────────┘   │           │
│  │  [장점] 완전한 이력 추적, 상태 재생 가능          │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [상태 재생 예시]                                            │
│  OrderCreated → PaymentCaptured → ShipmentStarted → OrderCompleted│
│       │              │                  │               │    │
│       ▼              ▼                  ▼               ▼    │
│   status=CREATED → status=PAID → status=SHIPPED → status=COMPLETED│
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**의료 기록(Health Record)**과 같습니다. 의사는 환자의 현재 상태만 보는 것이 아니라, **진료 기록(이벤트)**을 통해 병력을 추적합니다. 언제든지 진료 기록을 다시 보면서(Replay) 현재 상태를 도출할 수 있습니다. 과거에 어떤 치료를 했는지 알면, 부작용의 원인을 찾을 수도 있습니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 파일 시스템** | 로그 파일이 분산되어 분석 어려움 | **중앙화된 로그 저장 필요** |
| **② RDBMS CRUD** | 현재 상태만 저장, 과거 이력 소실 | **Audit Trail 불가** |
| **③ Event Sourcing 등장** | 모든 상태 변경을 이벤트로 기록 | **시간 여행(Time Travel) 가능** |
| **④ Event Store 확장** | 분산 이벤트 스트리밍, 재생 최적화 | **CQRS, Projections 지원** |

현재의 비즈니스 요구로서는 **불변 장부(Immutable Ledger), 규정 준수(Audit), 복잡한 도메인 로직 디버깅**이 필수적입니다.

### 📢 섹션 요약 비유

마치 **비디오 녹화**와 같습니다. 실시간 방송은 지나간 순간을 다시 볼 수 없지만(CRUD), 녹화된 비디오(이벤트 로그)는 언제든지 되감거나(Event Replay), 특정 장면으로 이동(Temporal Query)할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 저장소 | 비유 |
|:---|:---|:---|:---|:---|
| **Event Store** | 불변 이벤트 로그 | Append-only, Versioning | Kafka, EventStoreDB | 블록체인 |
| **Aggregate** | 일관성 경계 | 이벤트 적용, 상태 도출 | 메모리/캐시 | 애그리게이트 루트 |
| **Command Handler** | 명령 처리 | 비즈니스 로직, 이벤트 발행 | - | 서비스 계층 |
| **Event Projector** | 읽기 모델 생성 | 프로젝션(Projection) 유지 | Read DB | 뷰 생성 |
| **Snapshot** | 성능 최적화 | 중간 상태 체크포인트 | Snapshot Store | 저장 게임 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    이벤트 소싱 아키텍처                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [쓰기 경로 (Command Side)]                                                │
│                                                                             │
│  ┌──────────┐   Command    ┌─────────────────────────────────────┐         │
│  │  Client  │─────────────►│ Command Bus                        │         │
│  └──────────┘              └─────────────┬───────────────────────┘         │
│                                          │                                 │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │  Command Handler (Service)    │                 │
│                          │  ┌─────────────────────────┐   │                 │
│                          │  │ 1. 비즈니스 로직 수행    │   │                 │
│                          │  │ 2. 이벤트 생성          │   │                 │
│                          │  │ 3. Event Store에 저장   │   │                 │
│                          │  └─────────────────────────┘   │                 │
│                          └───────────────┬───────────────┘                 │
│                                          │                                 │
│                                          │ Domain Events                    │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │      Event Store             │                 │
│                          │  (Immutable Log)              │                 │
│                          │  ┌─────────────────────────┐   │                 │
│                          │  │ ORDER-123:              │   │                 │
│                          │  │ v1: OrderCreated        │   │                 │
│                          │  │ v2: PaymentCaptured     │   │                 │
│                          │  │ v3: ShipmentStarted      │   │                 │
│                          │  │ v4: OrderCompleted       │   │                 │
│                          │  └─────────────────────────┘   │                 │
│                          └───────────────┬───────────────┘                 │
│                                          │                                 │
│                                          │ Event Published                  │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │      Event Bus               │                 │
│                          │  (Kafka, RabbitMQ)           │                 │
│                          └───────────────────────────────┘                 │
│                                          │                                 │
│                  ┌───────────────────────┼───────────────────────┐          │
│                  │                       │                       │          │
│                  ▼                       ▼                       ▼          │
│          ┌───────────────┐      ┌───────────────┐      ┌───────────────┐  │
│          │Event Projector│      │Event Projector│      │Saga Orchestrator│ │
│          │(Read Model)   │      │(Notification) │      │(Workflow)      │  │
│          └───────┬───────┘      └───────────────┘      └───────────────┘  │
│                  │                                                       │
│                  │ Update Read DB                                        │
│                  ▼                                                       │
│          ┌───────────────┐                                               │
│          │  Read Model   │  ◄─── Query Side (CQRS)                        │
│          │  (Projection) │                                               │
│          └───────────────┘                                               │
│                                                                             │
│  [읽기 경로 (Query Side)]                                                  │
│  ┌──────────┐   Query    ┌───────────────┐                                 │
│  │  Client  │────────────►│  Read Model   │                                 │
│  └──────────┘             │  (Query API)  │                                 │
│                           └───────────────┘                                 │
│                                                                             │
│  [상태 재생 (Replay)]                                                       │
│  ┌───────────────────────────────────────────────────────────────────┐    │
│  │  Event Store → Event Replay → State Reconstruction              │    │
│  │  [v1, v2, v3, v4] → Apply Events → Current State                 │    │
│  │                                                                 │    │
│  │  Snapshot 최적화:                                                 │    │
│  │  ┌─────────┐        Events        ┌─────────┐                   │    │
│  │  │Snapshot │─────────────────────►│Current  │                   │    │
│  │  │(v1000)  │   (v1001 ~ v1005)    │State    │                   │    │
│  │  └─────────┘                      └─────────┘                   │    │
│  └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  [이벤트 예시]                                                              │
│  {                                                                            │
│    "eventType": "OrderCreated",                                             │
│    "aggregateId": "ORDER-123",                                              │
│    "version": 1,                                                            │
│    "timestamp": "2024-01-15T10:00:00Z",                                     │
│    "payload": {                                                             │
│      "customerId": "CUST-456",                                              │
│      "amount": 10000,                                                       │
│      "items": [...]                                                        │
│    }                                                                        │
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Command Bus**: 클라이언트의 명령(CreateOrder, CancelOrder 등)을 적절한 Command Handler로 라우팅합니다.

2. **Command Handler**: 비즈니스 로직을 수행하고, 결과적으로 **도메인 이벤트(Domain Event)**를 생성합니다. 예: `OrderCreated`, `PaymentCaptured`

3. **Event Store**: 이벤트를 **불변(Immutable) 로그**로 저장합니다. 기존 이벤트는 절대 수정되지 않으며, 새로운 이벤트만 추가(Append-only)됩니다.

4. **Event Projector**: 이벤트를 구독하여 **읽기 모델(Read Model)**을 생성하고 유지합니다. CQRS 패턴의 Query Side입니다.

5. **Snapshot**: 성능 최적화를 위해 일정 버전 간격으로 중간 상태를 저장합니다. 재생 시 스냅샷부터 시작합니다.

### 심층 동작 원리

```
① 명령 수신 (Command Received)
   └─> Command Bus가 적절한 핸들러로 라우팅
   └─> 예: CreateOrderCommand → OrderCommandHandler

② 애그리게이트 로드 (Load Aggregate)
   └─> Event Store에서 이벤트 로드
   └─> 스냅샷이 있다면 스냅샷 + 이후 이벤트 로드
   └─> 이벤트를 재생하여 현재 상태 도출

③ 비즈니스 로직 실행 (Execute Business Logic)
   └─> 애그리게이트 메서드 호출
   └─> 인버리언트 검증
   └─> 새로운 이벤트 생성

④ 이벤트 저장 (Persist Events)
   └─> Event Store에 이벤트 추가 (Append)
   └─> 낙관적 동시성 제어 (Optimistic Locking with Version)
   └─> 저장 성공 시 이벤트 발행

⑤ 프로젝션 업데이트 (Update Projections)
   └─> Event Projector가 이벤트 구독
   └─> 읽기 모델 업데이트
   └─> Saga Orchestrator가 워크플로우 진행
```

### 핵심 알고리즘 & 코드

```java
// ============ 도메인 이벤트 정의 ============

import java.time.Instant;

/**
 * 도메인 이벤트 기본 인터페이스
 */
interface DomainEvent {
    String getAggregateId();
    long getVersion();
    Instant getTimestamp();
}

/**
 * 주문 생성 이벤트
 */
@Value
class OrderCreated implements DomainEvent {
    String aggregateId;
    long version;
    Instant timestamp;
    String customerId;
    Money amount;
    List<OrderItem> items;

    @JsonCreator
    static OrderCreated fromJson(String json) {
        return objectMapper.readValue(json, OrderCreated.class);
    }
}

/**
 * 결제 캡처 이벤트
 */
@Value
class PaymentCaptured implements DomainEvent {
    String aggregateId;
    long version;
    Instant timestamp;
    String paymentId;
    Money amount;
}

/**
 * 주문 완료 이벤트
 */
@Value
class OrderCompleted implements DomainEvent {
    String aggregateId;
    long version;
    Instant timestamp;
}

// ============ 애그리게이트 (이벤트 적용) ============

/**
 * 주문 애그리게이트
 * 이벤트를 적용(apply)하여 상태를 도출
 */
class Order {
    private String id;
    private OrderStatus status;
    private Money amount;
    private List<OrderItem> items;
    private String paymentId;
    private long version;  // Event Version
    private final List<DomainEvent> newEvents = new ArrayList<>();

    /**
     * 빈 애그리게이트 생성 (Repository용)
     */
    private Order() {}

    /**
     * 새 주문 생성 (팩토리 메서드)
     */
    static Order create(String customerId, List<OrderItem> items) {
        Order order = new Order();
        Money total = calculateTotal(items);

        // 이벤트 생성
        OrderCreated event = new OrderCreated(
            UUID.randomUUID().toString(),
            0,  // initial version
            Instant.now(),
            customerId,
            total,
            items
        );

        // 이벤트 적용
        order.apply(event);
        order.newEvents.add(event);

        return order;
    }

    /**
     * 결제 캡처
     */
    void capturePayment(String paymentId, Money amount) {
        if (this.status != OrderStatus.CREATED) {
            throw new IllegalStateException("Order not in CREATED state");
        }
        if (!this.amount.equals(amount)) {
            throw new IllegalArgumentException("Amount mismatch");
        }

        PaymentCaptured event = new PaymentCaptured(
            this.id,
            this.version + 1,
            Instant.now(),
            paymentId,
            amount
        );

        this.apply(event);
        this.newEvents.add(event);
    }

    /**
     * 주문 완료
     */
    void complete() {
        if (this.status != OrderStatus.PAID) {
            throw new IllegalStateException("Order not in PAID state");
        }

        OrderCompleted event = new OrderCompleted(
            this.id,
            this.version + 1,
            Instant.now()
        );

        this.apply(event);
        this.newEvents.add(event);
    }

    /**
     * 이벤트 적용 (상태 변경)
     */
    @SuppressWarnings("unchecked")
    private void apply(DomainEvent event) {
        // Visitor Pattern으로 이벤트 타입별 처리
        if (event instanceof OrderCreated) {
            apply((OrderCreated) event);
        } else if (event instanceof PaymentCaptured) {
            apply((PaymentCaptured) event);
        } else if (event instanceof OrderCompleted) {
            apply((OrderCompleted) event);
        }

        this.version++;
    }

    private void apply(OrderCreated event) {
        this.id = event.getAggregateId();
        this.status = OrderStatus.CREATED;
        this.amount = event.getAmount();
        this.items = event.getItems();
    }

    private void apply(PaymentCaptured event) {
        this.status = OrderStatus.PAID;
        this.paymentId = event.getPaymentId();
    }

    private void apply(OrderCompleted event) {
        this.status = OrderStatus.COMPLETED;
    }

    /**
     * 새로운 이벤트 조회 및 초기화
     */
    List<DomainEvent> getUncommittedEvents() {
        return List.copyOf(newEvents);
    }

    void markEventsAsCommitted() {
        newEvents.clear();
    }
}

// ============ Event Store Repository ============

/**
 * 이벤트 소스 레포지토리
 */
interface EventStoreRepository {
    void save(String aggregateId, List<DomainEvent> events);
    List<DomainEvent> getEvents(String aggregateId);
    Optional<Snapshot> getLatestSnapshot(String aggregateId);
}

/**
 * 주문 레포지토리 구현
 */
class OrderRepository {

    private final EventStoreRepository eventStore;
    private final SnapshotStore snapshotStore;

    /**
     * 애그리게이트 저장 (이벤트 추가)
     */
    void save(Order order) {
        List<DomainEvent> newEvents = order.getUncommittedEvents();

        // ① 낙관적 동시성 제어 (버전 검증)
        List<DomainEvent> existingEvents = eventStore.getEvents(order.getId());
        if (!existingEvents.isEmpty()) {
            long currentVersion = existingEvents.get(existingEvents.size() - 1).getVersion();
            if (currentVersion != order.getVersion() - newEvents.size()) {
                throw new ConcurrentModificationException(
                    "Version conflict: expected=" + currentVersion +
                    ", actual=" + order.getVersion()
                );
            }
        }

        // ② 이벤트 저장
        eventStore.save(order.getId(), newEvents);

        // ③ 커밋 마크
        order.markEventsAsCommitted();
    }

    /**
     * 애그리게이트 로드 (이벤트 재생)
     */
    Order load(String orderId) {
        // ① 스냅샷 로드
        Optional<Snapshot> snapshot = snapshotStore.getLatestSnapshot(orderId);

        // ② 이벤트 로드
        List<DomainEvent> events = eventStore.getEvents(orderId);
        List<DomainEvent> eventsToApply = events;

        // ③ 스냅샷이 있다면 스냅샷부터 시작
        if (snapshot.isPresent()) {
            Order order = snapshot.get().restore();
            eventsToApply = events.stream()
                .filter(e -> e.getVersion() > snapshot.get().getVersion())
                .collect(Collectors.toList());

            // 이벤트 재생
            eventsToApply.forEach(order::apply);
            return order;
        } else {
            // ④ 빈 애그리게이트에 모든 이벤트 재생
            Order order = new Order();
            events.forEach(order::apply);
            return order;
        }
    }
}

// ============ Event Store (Kafka 기반) ============

/*
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecord;

class KafkaEventStore implements EventStoreRepository {

    private final Producer<String, String> producer;
    private final Consumer<String, String> consumer;
    private final String topicPrefix = "events-";

    @Override
    public void save(String aggregateId, List<DomainEvent> events) {
        for (DomainEvent event : events) {
            String key = aggregateId;
            String value = serializeEvent(event);

            ProducerRecord<String, String> record = new ProducerRecord<>(
                topicPrefix + event.getClass().getSimpleName(),
                key,
                value
            );

            // Kafka는 Append-only 로그
            producer.send(record);
        }
    }

    @Override
    public List<DomainEvent> getEvents(String aggregateId) {
        String topic = topicPrefix + "*";  // 모든 이벤트 토픽
        consumer.subscribe(Pattern.compile(topic));

        List<DomainEvent> events = new ArrayList<>();
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));

        for (ConsumerRecord<String, String> record : records) {
            if (record.key().equals(aggregateId)) {
                DomainEvent event = deserializeEvent(record.value());
                events.add(event);
            }
        }

        return events.stream()
            .sorted(Comparator.comparing(DomainEvent::getVersion))
            .collect(Collectors.toList());
    }
}
*/

// ============ Snapshot (성능 최적화) ============

/**
 * 스냅샷
 */
@Value
class Snapshot {
    String aggregateId;
    long version;
    String state;  // 직렬화된 애그리게이트 상태
    Instant timestamp;
}

/**
 * 스냅샷 저장소
 */
interface SnapshotStore {
    void save(Snapshot snapshot);
    Optional<Snapshot> getLatestSnapshot(String aggregateId);
}

/**
 * 스냅샷 생성 정책
 */
class SnapshotPolicy {
    private static final int SNAPSHOT_INTERVAL = 100;  // 100개 이벤트마다

    public boolean shouldCreateSnapshot(Aggregate aggregate) {
        return aggregate.getVersion() % SNAPSHOT_INTERVAL == 0;
    }
}
```

### 📢 섹션 요약 비유

마치 **블록체인의 원장(Ledger)**과 같습니다. 모든 거래(이벤트)을 순차적으로 기록하며, 한번 기록된 거래는 변경되지 않습니다(Immutable). 언제든지 원장을 처음부터 다시 읽으면(Replay), 현재 잔고(상태)를 정확히 계산할 수 있습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: CRUD vs Event Sourcing

| 비교 항목 | CRUD | Event Sourcing |
|:---|:---|:---|
| **저장 방식** | 현재 상태 | 이벤트 로그 |
| **이력 추적** | 불가능 (또는 별도 Audit 테이블) | 자동으로 모든 이력 보존 |
| **디버깅** | 현재 상태만 확인 가능 | 과거 시점으로 Time Travel |
| **성능** | 단순 조회 빠름 | 상태 도출에 비용 |
| **확장성** | 수직적 확장 | 이벤트 스트림으로 수평적 확장 |
| **복잡도** | 낮음 | 높음 (이벤트 버전 관리) |
| **일관성** | ACID | 결과적 일관성 (Eventual Consistency) |
| **CQRS 연계** | 선택 사항 | 자연스러운 결합 |

### 과목 융합 관점

**1) 데이터베이스 관점 (Append-only Log)**

이벤트 소싱은 **Write-Ahead Log (WAL)**와 유사한 원리를 공유합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                WAL (Write-Ahead Log) vs Event Store         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [WAL - RDBMS]                                             │
│  ┌─────────────────────────────────────────────┐           │
│  │  Transaction Log                           │           │
│  │  LSN 101: BEGIN TX                         │           │
│  │  LSN 102: UPDATE accounts SET ...          │           │
│  │  LSN 103: INSERT INTO audit ...            │           │
│  │  LSN 104: COMMIT                           │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Event Store - Event Sourcing]                             │
│  ┌─────────────────────────────────────────────┐           │
│  │  Event Stream                              │           │
│  │  v1: OrderCreated                          │           │
│  │  v2: PaymentCaptured                       │           │
│  │  v3: ShipmentStarted                        │           │
│  │  v4: OrderCompleted                         │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [공통점]                                                   │
│  - Append-only: 새로운 레코드만 추가                        │
│  - Sequential: 순차적 할당 (LSN, Version)                  │
│  - Recovery: 로그를 통한 복구 가능                          │
│                                                             │
│  [차이점]                                                   │
│  - WAL: 내부적인 복구용, 비즈니스 의미 없음                │
│  - Event Store: 도메인 이벤트, 비즈니스 의미 있음          │
└─────────────────────────────────────────────────────────────┘
```

**2) 분산 시스템 관점 (Event Streaming)**

이벤트 소싱은 Kafka와 같은 **이벤트 스트리밍 플랫폼**과 자연스럽게 결합합니다.

- **Producer**: Command Handler가 이벤트를 생성
- **Topic**: 애그리게이트 ID로 파티셔닝
- **Consumer**: Projector, Saga Orchestrator가 구독
- **Offset**: 이벤트 버전과 매핑

### 📢 섹션 요약 비유

마치 **동영상 스트리밍**과 같습니다. 크리에이터가 영상(이벤트)을 올리면, 구독자들은 실시간으로 시청합니다(Projector). 시청자는 언제든지 영상을 처음부터 다시 볼 수 있으며(Replay), 특정 장면으로 이동할 수 있습니다(Temporal Query).

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 금융 거래 시스템**

```
┌─────────────────────────────────────────────────────────────┐
│              이벤트 소싱 적용: 계좌 이체                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [애그리게이트: Account]                                    │
│  - AccountOpened (초기 잔액: 0)                            │
│  - MoneyDeposited (금액: +10000, 잔액: 10000)              │
│  - MoneyWithdrawn (금액: -5000, 잔액: 5000)                │
│  - TransferCompleted (금액: -3000, 잔액: 2000)             │
│                                                             │
│  [이벤트 재생]                                              │
│  AccountOpened → MoneyDeposited → MoneyWithdrawn → TransferCompleted│
│       │              │               │               │        │
│       ▼              ▼               ▼               ▼        │
│   balance=0    balance=10000   balance=5000    balance=2000 │
│                                                             │
│  [감사(Audit)]                                              │
│  - 언제, 누가, 얼마를 입금/출금했는지 모든 이력 추적      │
│  - 규정 준수(Compliance) 보고서 자동 생성                    │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **애그리게이트 식별**: Account, Transaction, Customer
2. **이벤트 정의**: AccountOpened, MoneyDeposited, MoneyWithdrawn
3. **프로젝션 설계**: 현재 잔고 뷰, 거래 내역 뷰, 규정 보고서 뷰

**Scenario 2: 전자상거래 주문**

```java
/**
 * 주문 프로젝션 (읽기 모델)
 */
@ProjectedAggregate(aggregateType = "Order")
class OrderProjection {

    private final JdbcTemplate jdbcTemplate;

    /**
     * OrderCreated 이벤트 처리
     */
    @EventHandler
    public void on(OrderCreated event) {
        jdbcTemplate.update(
            "INSERT INTO order_summary (id, customer_id, amount, status, created_at) VALUES (?, ?, ?, ?, ?)",
            event.getAggregateId(),
            event.getCustomerId(),
            event.getAmount().getValue(),
            "CREATED",
            event.getTimestamp()
        );
    }

    /**
     * PaymentCaptured 이벤트 처리
     */
    @EventHandler
    public void on(PaymentCaptured event) {
        jdbcTemplate.update(
            "UPDATE order_summary SET status = ?, payment_id = ? WHERE id = ?",
            "PAID",
            event.getPaymentId(),
            event.getAggregateId()
        );
    }

    /**
     * OrderCompleted 이벤트 처리
     */
    @EventHandler
    public void on(OrderCompleted event) {
        jdbcTemplate.update(
            "UPDATE order_summary SET status = ?, completed_at = ? WHERE id = ?",
            "COMPLETED",
            event.getTimestamp(),
            event.getAggregateId()
        );
    }
}
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **애그리거 식별** | 명확한 경계와 일관성 보장 | |
| **이벤트 버전 관리** | 이벤트 스키마 진화 전략 | |
| **Event Store** | Kafka, EventStoreDB, DB 선택 | |
| **스냅샷 정책** | 성능 최적화를 위한 주기 결정 | |
| **프로젝션 동기화** | 이벤트 처리 순서 보장 | |
| **재시도 로직** | 실패한 프로젝션 재처리 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **감사 로그** | 모든 이벤트 불변성 보장 | |
| **암호화** | 민감 데이터 이벤트 암호화 | |
│ **액세스 제어** | Event Store 접근 권한 분리 | |
│ **백업/복구** | 이벤트 로그 백업 전략 | |

### 안티패턴

**❌ 이벤트에 상태 포함**

```java
// 안티패턴: 이벤트에 전체 상태 포함
@Value
class OrderUpdated implements DomainEvent {
    String aggregateId;
    Order order;  // ❌ 전체 상태를 포함하는 것은 안티패턴!
}
```

**개선 방안**:

```java
// 올바른 패턴: 상태 변경의 차이만 포함
@Value
class OrderItemAdded implements DomainEvent {
    String aggregateId;
    String productId;  // ✅ 변경된 부분만 포함
    int quantity;
    Money price;
}
```

### 📢 섹션 요약 비유

마치 **회계 장부**와 같습니다. 모든 거래(이벤트)을 기록하며, 잔고(상태)는 장부를 계산해서 도출합니다. 장부에 기록된 거래는 절대 수정할 수 없으며(Immutable), 오류가 있으면 정정 거래(Compensating Event)를 추가해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | CRUD | Event Sourcing | 개선 효과 |
|:---|:---:|:---:|:---|
| **감사 가능성** | Audit 테이블 별도 구현 | 자동으로 모든 이력 | **100% 커버리지** |
| **디버깅 시간** | 과거 상태 재구축 어려움 | Time Travel로 원인 분석 | **90% 단축** |
| **읽기 성능** | 단순 조회 (10ms) | 프로젝션 필요 (50ms) | **5배 지연** |
| **쓰기 성능** | 단일 테이블 업데이트 | 이벤트 추가 (100ms) | **10배 지연** |
| **스토리지** | 현재 상태만 | 모든 이력 (10배 증가) | **용량 +1000%** |

### 미래 전망

1. **Event Sourcing as a Service**: AWS EventBridge, Azure Event Grid
2. **GraphQL Subscriptions**: 이벤트 소싱 기반 실시간 쿼리
3. **AI 기반 이벤트 분석**: ML을 통한 이상 탐지 및 패턴 발견
4. **Quantum-Safe Events**: 양자 내성 서명을 활용한 불변성 강화

### 참고 표준

- **Event Sourcing (Martin Fowler, 2005)**
- **Domain-Driven Design** (Eric Evans, 2003) - Chapter 6
- **CQRS and Event Sourcing** (Greg Young)
- **Event Store Platform**
- **Apache Kafka** (Distributed Event Streaming)

### 📢 섹션 요약 비유

미래의 이벤트 소싱은 **디지털 트윈(Digital Twin)**과 결합하여 더욱 강력해질 것입니다. 물리적 자산의 모든 상태 변경을 이벤트로 기록하여, **가상 공간에서 완벽하게 복제**하고, 시뮬레이션을 통해 미래를 예측할 수 있게 될 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[CQRS](./621_cqrs.md)**: 명령/조회 책임 분리
- **[Saga 패턴](./619_saga_pattern.md)**: 분산 트랜잭션
- **[도메인 주도 설계](./613_ddd_basics.md)**: 애그리거트 패턴
- **[Event Store](./event_store.md)**: 이벤트 저장소
- **[Projector](./projection.md)**: 읽기 모델 생성

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: 일기장을 쓰는 것과 같습니다. 오늘의 기분만 적는 것이 아니라(CRUD), 매일매일의 일을 순서대로 적어서(Event Log), 언제든지 일기를 다시 읽으면 그때의 상황을 모두 떠올릴 수 있습니다.

**2) 원리**: "아이스크림을 먹었다"는 이벤트와 "배탈이 났다"는 이벤트를 순서대로 적으면, 나중에 "왜 배탈이 났지?"라는 질문에 "아이스크림을 먹었기 때문이다"라고 답할 수 있습니다.

**3) 효과**: 모든 기록이 남아 있어서, 언제든지 과거로 돌아가서 무엇이 잘못되었는지 찾을 수 있고, 다시 처음부터 시작해도 똑같은 상태로 되돌릴 수 있습니다.
