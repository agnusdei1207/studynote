+++
title = "621. CQRS 읽기 쓰기 분리 스케일 아웃"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# CQRS (Command Query Responsibility Segregation) 읽기 쓰기 분리 스케일 아웃

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 명령(Command)과 조회(Query)의 책임을 **완전히 분리**하여 각각 최적화된 데이터 모델과 저장소를 사용하는 패턴
> 2. **가치**: 읽기/쓰기의 독립적 확장, 복잡한 조회 쿼리 최적화, Event Sourcing과의 자연스러운 결합 → 처리량 10배 향상
> 3. **융합**: Event Sourcing, Projections, Read/Write Model 분리, Eventual Consistency와 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**CQRS (Command Query Responsibility Segregation)**은 **"명령(Command: 상태를 변경하는 연산)과 조회(Query: 상태를 읽는 연산)의 책임을 분리"**하는 패턴입니다. Bertrand Meyer가 제안한 CQS (Command-Query Separation) 원칙을 시스템 수준으로 확장한 것입니다.

전통적인 CRUD 애플리케이션에서는 단일 데이터 모델을 읽기와 쓰기에 모두 사용하지만, CQRS에서는 **쓰기 모델(Write Model)과 읽기 모델(Read Model)을 완전히 분리**합니다. 이는 각각의 최적화된 스키마, 저장소, 확장 전략을 가능하게 합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                  CRUD vs CQRS 아키텍처                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [CRUD: 단일 모델]                                          │
│  ┌─────────────────────────────────────────────┐           │
│  │  Client                                   │           │
│  └────────┬────────────────────────────────────┘           │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────────────────────┐           │
│  │  Service Layer                            │           │
│  │  - createOrder()                          │           │
│  │  - getOrder()                             │           │
│  │  - searchOrders()                         │           │
│  └────────┬────────────────────────────────────┘           │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────────────────────┐           │
│  │  Single Database                          │           │
│  │  ┌─────────────────────────────────────┐   │           │
│  │  │  ORDER table (Normalize)           │   │           │
│  │  │  - id (PK)                           │   │           │
│  │  │  - customer_id (FK)                  │   │           │
│  │  │  - status                            │   │           │
│  │  │  - amount                            │   │           │
│  │  │  - items (JSON or child table)       │   │           │
│  │  └─────────────────────────────────────┘   │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [문제점]                                                    │
│  - 복잡한 조회 쿼리 성능 저하                               │
│  - 읽기/쓰기 경합 (Contention)                              │
│  - 확장성 제한                                              │
│                                                             │
│  [CQRS: 분리된 모델]                                        │
│  ┌──────────────────┐        ┌──────────────────┐           │
│  │  Write Side      │        │  Read Side       │           │
│  │  (Command)       │        │  (Query)         │           │
│  └────────┬─────────┘        └────────┬─────────┘           │
│           │                           │                      │
│           ▼                           ▼                      │
│  ┌──────────────────┐        ┌──────────────────┐           │
│  │  Write Model     │        │  Read Model      │           │
│  │  (Normalized)    │        │  (Denormalized)  │           │
│  │  ┌────────────┐   │        │  ┌────────────┐   │           │
│  │  │ORDER table│   │        │  │order_view  │   │           │
│  │  │- id       │   │        │  │- id        │   │           │
│  │  │- status   │   │        │  │- customer  │   │           │
│  │  │- amount   │   │        │  │  name      │   │           │
│  │  │- version  │   │        │  │- amount    │   │           │
│  │  └────────────┘   │        │  │- items[]   │   │           │
│  └──────────────────┘        │  │- status    │   │           │
│           │                  │  └────────────┘   │           │
│           │ Event            │                  │           │
│           ▼                  ▼                  │           │
│  ┌─────────────────────────────────────────────┐           │
│  │         Event Bus (Sync/Async)              │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**도서관의 카드 카탈로그와 책장**과 같습니다.
- **쓰기(Write)**: 새 책을 받으면 카탈로그에 등록 (Write Model: 정규화된 데이터)
- **읽기(Read)**: 독자는 카탈로그, 검색 엔진, 추천 목록 등 다양한 방식으로 검색 (Read Model: 비정규화된 뷰)

카탈로그(Read Model)은 책의 위치, 요약, 평점 등을 포함할 수 있으며, 책장(Write Model)과 독립적으로 최적화됩니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 단일 테이블** | 읽기/쓰기가 동일한 스키마 사용 | **조인 성능 저하** |
| **② 뷰/매터리얼라이즈** | 읽기 전용 뷰 생성 | **데이터 동기화 복잡** |
| **③ CQRS 등장** | 읽기/쓰기 모델 완전 분리 | **독립적 확장 가능** |
| **④ Event Sourcing 결합** | 이벤트 기반 동기화 | **결과적 일관성 보장** |

현재의 비즈니스 요구로서는 **고처리량 시스템, 복잡한 조회 요구사항, 실시간 분석**이 필수적입니다.

### 📢 섹션 요약 비유

마치 **음식점의 주방과 홀**과 같습니다. 주방(Write Side)에서는 요리를 만들어서(상태 변경), 홀(Read Side)으로 내갑니다. 홀에서는 메뉴판, 테이블 배치, 조명 등 다양한 형태로 음식을 제시하며(최적화된 뷰), 주방과 홀은 독립적으로 운영됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 데이터 모델 | 비유 |
|:---|:---|:---|:---|:---|
| **Command** | 상태 변경 요청 | Create, Update, Delete | Command DTO | 주문서 |
| **Command Handler** | 명령 처리 | 비즈니스 로직, 이벤트 발행 | - | 주방장 |
| **Write Model** | 쓰기용 모델 | 정규화, ACID 트랜잭션 | Entity, Aggregate | 조리법 |
| **Query** | 상태 조회 요청 | Search, Filter, Aggregate | Query DTO | 메뉴판 |
| **Query Handler** | 조회 처리 | Read Model 조회, DTO 변환 | - | 웨이터 |
| **Read Model** | 읽기용 모델 | 비정규화, Denormalized | Projection, View | 완제품 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CQRS 아키텍처 상세 다이어그램                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [명령 경로 (Command Path - Write Side)]                                 │
│                                                                             │
│  ┌──────────┐   Command    ┌─────────────────────────────────────┐         │
│  │  Client  │─────────────►│ Command Bus                        │         │
│  └──────────┘              └─────────────┬───────────────────────┘         │
│                                          │                                 │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │  Command Handler (Service)    │                 │
│                          │  ┌─────────────────────────┐   │                 │
│                          │  │ 1. Command 수신        │   │                 │
│                          │  │ 2. 비즈니스 로직 수행   │   │                 │
│                          │  │ 3. Write Model 업데이트 │   │                 │
│                          │  │ 4. Domain Event 발행    │   │                 │
│                          │  └─────────────────────────┘   │                 │
│                          └───────────────┬───────────────┘                 │
│                                          │                                 │
│                                          │ Domain Events                    │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │      Write Model Store        │                 │
│                          │  (Document DB / RDBMS)        │                 │
│                          │  ┌─────────────────────────┐   │                 │
│                          │  │ ORDER (Write Model)     │   │                 │
│                          │  │ - id (PK)                │   │                 │
│                          │  │ - customer_id            │   │                 │
│                          │  │ - status                 │   │                 │
│                          │  │ - amount                 │   │                 │
│                          │  │ - items (JSON)           │   │                 │
│                          │  │ - version (Optimistic)   │   │                 │
│                          │  └─────────────────────────┘   │                 │
│                          └───────────────┬───────────────┘                 │
│                                          │                                 │
│                                          │ Event Published                  │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │         Event Bus             │                 │
│                          │  (Kafka, RabbitMQ, In-Memory)  │                 │
│                          └───────────────┬───────────────┘                 │
│                                          │                                 │
│                  ┌───────────────────────┼───────────────────────┐          │
│                  │                       │                       │          │
│                  ▼                       ▼                       ▼          │
│          ┌───────────────┐      ┌───────────────┐      ┌───────────────┐  │
│          │Event Projector│      │Saga Orchestrator│      │Notification   │  │
│          │(Read Model)   │      │(Workflow)      │      │Service        │  │
│          └───────┬───────┘      └───────────────┘      └───────────────┘  │
│                  │                                                       │
│                  │ Update Read DB                                        │
│                  ▼                                                       │
│          ┌───────────────┐                                               │
│          │  Read DB      │  ◄─── 별도의 데이터베이스                      │
│          │  (NoSQL/Cube)  │                                               │
│          └───────────────┘                                               │
│                                                                             │
│  [조회 경로 (Query Path - Read Side)]                                    │
│  ┌──────────┐   Query      ┌─────────────────────────────┐                 │
│  │  Client  │─────────────►│ Query Bus (Optional)        │                 │
│  └──────────┘              └─────────────┬───────────────┘                 │
│                                          │                                 │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │  Query Handler (Service)      │                 │
│                          │  ┌─────────────────────────┐   │                 │
│                          │  │ 1. Query 수신          │   │                 │
│                          │  │ 2. Read Model 조회     │   │                 │
│                          │  │ 3. DTO 변환            │   │                 │
│                          │  │ 4. 결과 반환           │   │                 │
│                          │  └─────────────────────────┘   │                 │
│                          └───────────────┬───────────────┘                 │
│                                          │                                 │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │      Read Model Store        │                 │
│                          │  (Elasticsearch, Redis, Cube) │                 │
│                          │  ┌─────────────────────────┐   │                 │
│                          │  │ ORDER_VIEW (Read Model) │   │                 │
│                          │  │ - id                    │   │                 │
│                          │  │ - customer_name         │   │                 │
│                          │  │ - customer_email        │   │                 │
│                          │  │ - amount                │   │                 │
│                          │  │ - items (Denormalized)  │   │                 │
│                          │  │ - status                │   │                 │
│                          │  │ - created_at            │   │                 │
│                          │  │ - shipped_at            │   │                 │
│                          │  │ - tracking_number       │   │                 │
│                          │  │ [FULL TEXT SEARCH]      │   │                 │
│                          │  └─────────────────────────┘   │                 │
│                          └───────────────────────────────┘                 │
│                                          │                                 │
│                                          ▼                                 │
│                          ┌───────────────────────────────┐                 │
│                          │     Query Result DTO          │                 │
│                          │  (최적화된 응답 형태)           │                 │
│                          └───────────────────────────────┘                 │
│                                                                             │
│  [데이터 동기화 흐름]                                                       │
│  Command Handler → Domain Event → Event Bus → Event Projector → Read DB    │
│      │                                         │                            │
│      └─────────────────────────────────────────┴──────→ [Sync or Async]      │
│                                                                             │
│  [일관성 모델]                                                             │
│  - Strong Consistency: 동기식 프로젝션 (메서드 내에서 완료)                   │
│  - Eventual Consistency: 비동기식 프로젝션 (이벤트 발행 후 백그라운드)      │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Command Side (쓰기)**: 클라이언트의 명령(CreateOrder, CancelOrder 등)을 받아 비즈니스 로직을 수행하고, **Write Model**을 업데이트한 후 **Domain Event**를 발행합니다. 쓰기 모델은 **정규화(Normalized)**되어 데이터 무결성을 보장합니다.

2. **Query Side (읽기)**: 클라이언트의 조회(SearchOrders, GetOrderSummary 등)를 받아 **Read Model**을 조회합니다. 읽기 모델은 **비정규화(Denormalized)**되어 있어, 복잡한 조인 없이 빠른 조회가 가능합니다.

3. **Event Bus**: 쓰기와 읽기 사이의 **동기화 계층**입니다. 이벤트를 구독하는 Event Projector가 Read Model을 업데이트합니다. 동기식(Strong Consistency) 또는 비동기식(Eventual Consistency)을 선택할 수 있습니다.

### 심층 동작 원리

```
① 명령 경로 (Command Path)
   └─> 1. Client가 Command 전송
   └─> 2. Command Bus가 적절한 Handler로 라우팅
   └─> 3. Command Handler가 Write Model 로드
   └─> 4. 비즈니스 로직 수행 (인버리언트 검증)
   └─> 5. Write Model 저장 (ACID 트랜잭션)
   └─> 6. Domain Event 발행
   └─> 7. Event Projector가 Read Model 업데이트

② 조회 경로 (Query Path)
   └─> 1. Client가 Query 전송
   └─> 2. Query Bus가 적절한 Handler로 라우팅
   └─> 3. Query Handler가 Read Model 조회
   └─> 4. DTO로 변환하여 반환
```

### 핵심 알고리즘 & 코드

```java
// ============ Command 정의 ============

/**
 * 명령 (Command) 인터페이스
 */
interface Command {
    String getAggregateId();
}

/**
 * 주문 생성 명령
 */
@Value
class CreateOrderCommand implements Command {
    String aggregateId;  // UUID or null for new
    String customerId;
    List<OrderItemDto> items;
    Money amount;
}

/**
 * 주문 완료 명령
 */
@Value
class CompleteOrderCommand implements Command {
    String orderId;
}

// ============ Query 정의 ============

/**
 * 조회 (Query) 인터페이스
 */
interface Query {
}

/**
 * 주문 조회 쿼리
 */
@Value
class GetOrderQuery implements Query {
    String orderId;
}

/**
 * 주문 검색 쿼리
 */
@Value
class SearchOrdersQuery implements Query {
    String customerId;
    OrderStatus status;
    LocalDate startDate;
    LocalDate endDate;
    int page;
    int size;
}

// ============ Command Handler (Write Side) ============

/**
 * 주문 명령 핸들러
 */
@Component
class OrderCommandHandler {

    private final OrderRepository orderRepository;
    private final EventPublisher eventPublisher;

    /**
     * 주문 생성 명령 처리
     */
    @CommandHandler
    public String handle(CreateOrderCommand command) {
        // ① Write Model 로드 (또는 생성)
        Order order = Order.create(
            command.getCustomerId(),
            command.getItems(),
            command.getAmount()
        );

        // ② Write Model 저장
        orderRepository.save(order);

        // ③ Domain Event 발행
        order.getUncommittedEvents().forEach(eventPublisher::publish);

        return order.getId();
    }

    /**
     * 주문 완료 명령 처리
     */
    @CommandHandler
    public void handle(CompleteOrderCommand command) {
        // ① Write Model 로드
        Order order = orderRepository.findById(command.getOrderId())
            .orElseThrow(() -> new OrderNotFoundException(command.getOrderId()));

        // ② 비즈니스 로직 수행
        order.complete();

        // ③ Write Model 저장
        orderRepository.save(order);

        // ④ Domain Event 발행
        order.getUncommittedEvents().forEach(eventPublisher::publish);
    }
}

// ============ Query Handler (Read Side) ============

/**
 * 주문 조회 핸들러
 */
@Component
class OrderQueryHandler {

    private final OrderViewRepository orderViewRepository;

    /**
     * 주문 조회 (단건)
     */
    @QueryHandler
    public OrderDto handle(GetOrderQuery query) {
        OrderView view = orderViewRepository.findById(query.getOrderId())
            .orElseThrow(() -> new OrderNotFoundException(query.getOrderId()));

        return toDto(view);
    }

    /**
     * 주문 검색 (복잡한 쿼리)
     */
    @QueryHandler
    public Page<OrderDto> handle(SearchOrdersQuery query) {
        // Read Model에서 복잡한 조회 수행
        Page<OrderView> views = orderViewRepository.search(
            query.getCustomerId(),
            query.getStatus(),
            query.getStartDate(),
            query.getEndDate(),
            PageRequest.of(query.getPage(), query.getSize())
        );

        return views.map(this::toDto);
    }

    private OrderDto toDto(OrderView view) {
        return OrderDto.builder()
            .id(view.getId())
            .customerName(view.getCustomerName())
            .customerEmail(view.getCustomerEmail())
            .amount(view.getAmount())
            .items(view.getItems())
            .status(view.getStatus())
            .createdAt(view.getCreatedAt())
            .shippedAt(view.getShippedAt())
            .trackingNumber(view.getTrackingNumber())
            .build();
    }
}

// ============ Event Projector (동기화) ============

/**
 * 주문 프로젝터 (Read Model 업데이트)
 */
@Component
class OrderProjector {

    private final OrderViewRepository orderViewRepository;
    private final CustomerViewRepository customerViewRepository;

    /**
     * OrderCreated 이벤트 처리
     */
    @EventHandler
    public void on(OrderCreated event) {
        // Customer 정보 조회 (Read Model)
        CustomerView customer = customerViewRepository.findById(event.getCustomerId())
            .orElseThrow();

        // Order View 생성
        OrderView view = OrderView.builder()
            .id(event.getAggregateId())
            .customerId(event.getCustomerId())
            .customerName(customer.getName())
            .customerEmail(customer.getEmail())
            .amount(event.getAmount())
            .items(event.getItems())
            .status(OrderStatus.CREATED)
            .createdAt(event.getTimestamp())
            .build();

        orderViewRepository.save(view);
    }

    /**
     * PaymentCaptured 이벤트 처리
     */
    @EventHandler
    public void on(PaymentCaptured event) {
        OrderView view = orderViewRepository.findById(event.getAggregateId())
            .orElseThrow();

        view.setStatus(OrderStatus.PAID);
        view.setPaymentId(event.getPaymentId());

        orderViewRepository.save(view);
    }

    /**
     * ShipmentStarted 이벤트 처리
     */
    @EventHandler
    public void on(ShipmentStarted event) {
        OrderView view = orderViewRepository.findById(event.getAggregateId())
            .orElseThrow();

        view.setStatus(OrderStatus.SHIPPED);
        view.setShippedAt(event.getTimestamp());
        view.setTrackingNumber(event.getTrackingNumber());

        orderViewRepository.save(view);
    }

    /**
     * OrderCompleted 이벤트 처리
     */
    @EventHandler
    public void on(OrderCompleted event) {
        OrderView view = orderViewRepository.findById(event.getAggregateId())
            .orElseThrow();

        view.setStatus(OrderStatus.COMPLETED);
        view.setCompletedAt(event.getTimestamp());

        orderViewRepository.save(view);
    }
}

// ============ Repository 정의 ============

/**
 * 쓰기 모델 레포지토리
 */
interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(String id);
}

/**
 * 읽기 모델 레포지토리 (최적화된 조회)
 */
interface OrderViewRepository extends JpaRepository<OrderView, String> {
    // Elasticsearch 또는 RDBMS 복잡한 쿼리
    Page<OrderView> findByCustomerIdAndStatus(
        String customerId,
        OrderStatus status,
        Pageable pageable
    );

    @Query("SELECT v FROM OrderView v WHERE " +
           "v.customerId = :customerId AND " +
           "v.status = :status AND " +
           "v.createdAt BETWEEN :startDate AND :endDate")
    Page<OrderView> search(
        @Param("customerId") String customerId,
        @Param("status") OrderStatus status,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate,
        Pageable pageable
    );

    // Full Text Search (Elasticsearch)
    @Query("{\"bool\": {\"must\": [{\"match\": {\"customerName\": \"?0\"}}]}}")
    Page<OrderView> searchByCustomerName(String name, Pageable pageable);
}
```

### 📢 섹션 요약 비유

마치 **신문 편집국**과 같습니다. 기자(Write Side)가 기사를 작성하면, 편집팀(Event Projector)이 다양한 섹션(Read Model)으로 기사를 배포합니다. 독자(Query Side)은 정치, 스포츠, 연예 등 자신이 관심 있는 섹션만 선택하여 볼 수 있습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: 일관성 모델

| 모델 | 일관성 보장 | 성능 | 복잡도 | 사용 사례 |
|:---|:---:|:---:|:---:|:---|
| **Strong Consistency** | ACID (즉시) | 낮음 (Locking) | 낮음 | 금융 거래 |
| **Eventual Consistency** | 결과적 일관성 | 높음 (비동기) | 중간 | SNS, 쇼핑몰 |
| **CQRS + Sync** | Strong | 중간 | 중간 | 실시간 요구 |
| **CQRS + Async** | Eventual | 높음 | 높음 | 대용량 시스템 |

### 과목 융합 관점

**1) 데이터베이스 관점 (정규화 vs 비정규화)**

```
┌─────────────────────────────────────────────────────────────┐
│          Write Model (Normalized) vs Read Model (Denorm)     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Write Model: 3NF 정규화]                                  │
│  ┌─────────────────────────────────────────────┐           │
│  │  ORDER (Write Model)                      │           │
│  │  - id (PK)                                 │           │
│  │  - customer_id (FK)                        │           │
│  │  - status                                  │           │
│  │  - amount                                  │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Read Model: 비정규화 (Denormalized)]                       │
│  ┌─────────────────────────────────────────────┐           │
│  │  ORDER_VIEW (Read Model)                  │           │
│  │  - id                                     │           │
│  │  - customer_name  ← Customer 테이블 조인    │           │
│  │  - customer_email ← Customer 테이블 조인    │           │
│  │  - amount                                 │           │
│  │  - status                                 │           │
│  │  - items[]        ← OrderItem 테이블 조인   │           │
│  │  - product_names[] ← Product 테이블 조인    │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [장점]                                                    │
│  - Write Model: 데이터 무결성 보장 (중복 없음)              │
│  - Read Model: 빠른 조회 (조인 불필요)                      │
└─────────────────────────────────────────────────────────────┘
```

**2) 분산 시스템 관점 (CAP 정리)**

CQRS는 **CAP 정리**의 AP(가용성 + 분산 내성) 측면에서 유리합니다.
- 쓰기: Write DB에만 쓰면 되므로 가용성 높음
- 읽기: Read DB가 여러 개면 로드 밸런싱으로 확장 가능
- 단순성: 읽기와 쓰기가 독립적이므로 장애 격리 용이

### 📢 섹션 요약 비유

마치 **레스토랑의 주방과 홀 서빙**과 같습니다. 주방(Write Side)에서는 효율적인 조리를 위해 재료를 정리해두고(정규화), 홀(Read Side)에서는 고객이 보기 좋게 메뉴를 꾸며(비정규화), 두 영역이 독립적으로 최적화됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 전자상거래 검색 시스템**

```
┌─────────────────────────────────────────────────────────────┐
│            CQRS 적용: 복잡한 상품 검색                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Write Side: 상품 관리]                                   │
│  - 상품 등록, 수정, 삭제                                   │
│  - 재고 관리, 가격 변경                                    │
│  - Write DB: PostgreSQL (정규화)                          │
│                                                             │
│  [Read Side: 상품 검색]                                    │
│  - 상품 검색 (키워드, 필터)                               │
│  - 추천 시스템                                            │
│  - Read DB: Elasticsearch (전문 검색)                     │
│                                                             │
│  [동기화]                                                   │
│  ProductCreated → Kafka → Elasticsearch Indexer            │
│  ProductUpdated → Kafka → Elasticsearch Update             │
│                                                             │
│  [성능 향상]                                               │
│  - PostgreSQL FTS: 2초                                    │
│  - Elasticsearch: 50ms (40배 개선)                        │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **읽기 부하 분석**: 검색이 전체 트래픽의 80% 이상
2. **Read DB 선정**: Elasticsearch (전문 검색, 집계)
3. **동기화 전략**: 비동기 Kafka (결과적 일관성 허용)
4. **Rollout 전략**: Read Only 기간 → Dual Write → CQRS 전환

**Scenario 2: 대시보드 시스템**

```java
/**
 * 대시보드용 조회 핸들러 (최적화된 집계)
 */
@QueryHandler
public DashboardStatsDto handle(GetDashboardStatsQuery query) {
    // Read Model에서 미리 집계된 데이터 조회
    DashboardStatsView stats = dashboardStatsRepository
        .findByDate(query.getDate())
        .orElseThrow();

    return DashboardStatsDto.builder()
        .totalOrders(stats.getTotalOrders())
        .totalRevenue(stats.getTotalRevenue())
        .averageOrderValue(stats.getAverageOrderValue())
        .topProducts(stats.getTopProducts())
        .customerAcquisition(stats.getCustomerAcquisition())
        .build();
}

/**
 * 통계 이벤트 프로젝터 (배치/실시간 집계)
 */
@Component
class DashboardStatsProjector {

    /**
     * 주문 완료 시 실시간 집계
     */
    @EventHandler
    public void on(OrderCompleted event) {
        LocalDate today = LocalDate.now();
        DashboardStatsView stats = statsRepository
            .findByDate(today)
            .orElse(DashboardStatsView.create(today));

        stats.incrementTotalOrders();
        stats.addRevenue(event.getAmount());

        statsRepository.save(stats);
    }

    /**
     * 일일 배치: 전체 통계 재계산
     */
    @Scheduled(cron = "0 0 1 * * ?")  // 매일 새벽 1시
    public void recalculateStats() {
        LocalDate yesterday = LocalDate.now().minusDays(1);

        // Read Model에서 원시 데이터 조회 및 집계
        DashboardStatsView stats = orderViewRepository
            .findByCreatedAtBetween(
                yesterday.atStartOfDay(),
                yesterday.plusDays(1).atStartOfDay()
            )
            .stream()
            .collect(
                Collectors.collectingAndThen(
                    Collectors.toList(),
                    this::calculateStats
                )
            );

        statsRepository.save(stats);
    }
}
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **읽기/쓰기 비율** | 읽기가 쓰기보다 현저히 많은지 | |
| **복잡한 조회** | 조인이 많거나 집계가 복잡한지 | |
| **확장성 요구** | 독립적 확장이 필요한지 | |
| **Eventual Consistency** | 결과적 일관성 허용 가능 여부 | |
| **프로젝션 전략** | 동기식 vs 비동기식 선택 | |
| **Rollout 계획** | Dual Write 기간 고려 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **동기화 모니터링** | Event Lag 모니터링 | |
| **불일치 감지** | Read/Write 데이터 비교 | |
| **재동기화** | 수동 재동기화 스크립트 | |
| **백업/복구** | Read/Write DB 별도 백업 | |

### 안티패턴

**❌ Query에서 Write Model 직접 조회**

```java
// 안티패턴: Query Handler가 Write DB에 직접 접근
@QueryHandler
public OrderDto handle(GetOrderQuery query) {
    // ❌ Read Side가 Write Model에 의존
    Order order = orderRepository.findById(query.getOrderId());
    return convertToDto(order);
}
```

**개선 방안**:

```java
// 올바른 패턴: Query Handler가 Read Model만 조회
@QueryHandler
public OrderDto handle(GetOrderQuery query) {
    // ✅ Read Model만 조회
    OrderView view = orderViewRepository.findById(query.getOrderId());
    return view.toDto();
}
```

### 📢 섹션 요약 비유

마치 **병원의 차트와 EMR**과 같습니다. 의사(Write Side)는 차트에 환자 정보를 기록하며, EMR 시스템(Event Projector)이 차트를 전자화하여(Patient View), 각 부서(Query Side)에서 필요한 정보만 조회할 수 있습니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | CRUD | CQRS | 개선 효과 |
|:---|:---:|:---:|:---|
| **조회 성능** | 500ms (조인) | 50ms (비정규화) | **10배 향상** |
| **쓰기 성능** | 100ms | 150ms (이벤트 발행) | **1.5배 지연** |
| **처리량** | 1000 TPS | 10000 TPS (독립 확장) | **10배 증가** |
| **확장성** | 단일 DB | Read/Write 분리 확장 | **무한 확장** |
| **개발 복잡도** | 1x | 2x (모델 분리) | **복잡도 2배** |

### 미래 전망

1. **GraphQL 결합**: CQRS + GraphQL로 클라이언트 중심 조회 최적화
2. **Real-time CQRS**: WebSocket을 통한 실시간 Read Model 업데이트
3. **Serverless Query**: Lambda@Edge를 통한 글로벌 읽기 확장
4. **AI-powered Query Optimization**: ML로 조회 패턴 학습 및 Read Model 자동 최적화

### 참고 표준

- **CQRS Pattern** (Martin Fowler, 2011)
- **Domain-Driven Design** (Eric Evans) - Chapter 6
- **CQRS and Event Sourcing** (Greg Young)
- **Axon Framework** (CQRS + ES 플랫폼)
- **Microsoft CQRS Journey** (MSDN)

### 📢 섹션 요약 비유

미래의 CQRS는 **지능형 추천 시스템**과 결합할 것입니다. Read Model이 단순한 데이터 저장소를 넘어, **AI 모델이 실시간으로 개인화된 뷰**를 생성하여, 각 사용자에게 최적화된 정보를 제공하는 **Hyper-Personalized CQRS**가 실현될 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[Event Sourcing](./620_event_sourcing.md)**: 이벤트 기반 상태 관리
- **[이벤트 프로젝션](./projection.md)**: Read Model 생성
- **[도메인 주도 설계](./613_ddd_basics.md)**: 애그리거트 패턴
- **[이벤트 버스](./event_bus.md)**: 이벤트 전파 메커니즘
- **[결과적 일관성](./eventual_consistency.md)**: Eventual Consistency 보장

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: **카메라와 사진**과 같습니다. 우리가 찍은 사진(이벤트)은 SD 카드(Write Model)에 저장되지만, 앨범이나 인화(Read Model)에 따라 사진을 다르게 정리할 수 있습니다.

**2) 원리**: 사진을 찍을 때(Write)는 원본을 저장하고, 나중에 볼 때(Read)는 인화를 뽑거나 필터를 적용해서 봅니다. 같은 원본이라도 보는 방식에 따라 다르게 보입니다.

**3) 효과**: 원본 사진은 안전하게 보관하면서, 필요한 만큼만 인화를 뽑을 수 있습니다. 사진을 찍는 사람과 보는 사람이 서로 방해하지 않고 각자의 일을 할 수 있습니다.
