+++
title = "619. 사가 (Saga) 패턴 2PC 한계 극복 분산 트랜잭션"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 사가 (Saga) 패턴 - 2PC 한계 극복 분산 트랜잭션

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이크로서비스 환경에서 ACID 트랜잭션을 **로컬 트랜잭션들의 체인으로 분해**하고, **보상 트랜잭션(Compensating Transaction)**으로 롤백하는 패턴
> 2. **가치**: 2PC의 성능 문제/단일 장애점(SPOF) 해결, 장기 실행 트랜잭션 지원 → 가용성 99.99% + 결과적 일관성(Eventual Consistency)
> 3. **융합**: Choreography(이벤트 기반) vs Orchestration(중앙 코디네이터), Event Sourcing, CQRS와 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**사가 (Saga) 패턴**은 마이크로서비스 환경에서 **분산 트랜잭션(Distributed Transaction)을 관리**하기 위한 패턴입니다. 1987년 Hector Garcia-Molina와 Kenneth Salem이 제안한 개념으로, **"긴 트랜잭션(Long Lived Transaction)을 하위 트랜잭션들의 시퀀스로 분해"**합니다.

핵심 아이디어는 각 서비스가 **자신의 로컬 트랜잭션을 커밋**하고, 전체 체인이 실패하면 **이미 완료된 트랜잭션을 취소하는 보상 트랜잭션(Compensating Transaction)**을 순차적으로 실행하는 것입니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    사가 패턴 개념                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [2PC (Two-Phase Commit) 문제]                              │
│  ┌────────┐  ┌────────┐  ┌────────┐                        │
│  │Service │  │Service │  │Service │                        │
│  │   A    │  │   B    │  │   C    │                        │
│  └───┬────┘  └───┬────┘  └───┬────┘                        │
│      │           │           │                            │
│      │    ┌──────▼──────────▼───┐                          │
│      │    │  Coordinator (2PC)  │                          │
│      │    │  1. Prepare (전부 준비?)│                        │
│      │    │  2. Commit (전부 커밋)│                        │
│      │    └──────────────────────┘                          │
│      │           │                                          │
│      │           ▼                                          │
│    [문제점]                                                  │
│    - Locking으로 성능 저하                                   │
│    - Coordinator SPOF                                       │
│    - 마이크로서비스에 부적합                                 │
│                                                             │
│  [Saga 패턴 해결]                                            │
│  ┌────────┐  ┌────────┐  ┌────────┐                        │
│  │Service │  │Service │  │Service │                        │
│  │   A    │  │   B    │  │   C    │                        │
│  └───┬────┘  └───┬────┘  └───┬────┘                        │
│      │  TX1     │  TX2      │  TX3                         │
│      ▼          ▼          ▼                               │
│   [Commit]  →  [Commit]  →  [Commit]                       │
│      │          │          │                               │
│      │          │       실패!                               │
│      │          │          ▼                               │
│      │          │   [Compensate TX3]                        │
│      │          │          │                               │
│      │          │       [Compensate TX2]                     │
│      │          │          │                               │
│      │       [Compensate TX1]                               │
│      │          │          │                               │
│      ▼          ▼          ▼                               │
│   [Rollback] [Rollback] [Rollback]                          │
│                                                             │
│   [장점]                                                    │
│   - 각 서비스가 자신의 DB에만 접근 (Locking 없음)             │
│   - 부분 실패 가능 (결과적 일관성)                          │
│   - 확장성 높음                                              │
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**여행 예약 시나리오**를 생각해보세요.
1. 항공편 예약
2. 호텔 예약
3. 렌터카 예약

만약 렌터카 예약이 실패하면, 항공편과 호텔 예약을 **취소(보상)**해야 합니다. 각 예약은 독립적으로 확정되지만, 전체 여행이 성공하려면 모두 완료되어야 합니다. 사가 패턴은 이러한 **보상 로직**을 자동화합니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 로컬 ACID** | 단일 데이터베이스에서만 강한 일관성 | **분산 환경에서는 부족** |
| **② 2PC (XA)** | 전체 시스템 Locking, Coordinator SPOF | **마이크로서비스에 비실용적** |
| **③ Saga 등장** | 로컬 트랜잭션 + 보상 트랜잭션 | **결과적 일관성 + 높은 가용성** |
| **④ Event Sourcing** | 상태 대신 이벤트 저장 | **Saga와 결합하여 재생 가능** |

현재의 비즈니스 요구로서는 **글로벌 분산 시스템, 멀티 리전 트랜잭션, 장기 실행 비즈니스 프로세스**가 필수적입니다.

### 📢 섹션 요약 비유

마치 **연쇄 식당 예약**과 같습니다. 식당 A, B, C를 순서대로 예약하다가 C가 만석이면, B와 A의 예약을 순서대로 취소합니다. 각 식당은 독립적으로 예약/취소하지만, 전체 예약이 성공해야만 "모든 식당 예약 완료" 상태가 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 프로토콜/기법 | 비유 |
|:---|:---|:---|:---|:---|
| **Saga Participant** | 개별 서비스 | 로컬 트랜잭션 + 보상 로직 | Compensatable, Pivot | 연쇄 식당 |
| **Saga Orchestrator** | 중앙 코디네이터 | 상태 기계(State Machine) 관리 | BPMN, State Machine | 여행사 |
| **Event Bus** | 이벤트 전파 | 메시지 큐, Pub/Sub | Kafka, RabbitMQ | 우편 시스템 |
| **Saga Log** | 실행 이력 | 상태 저장 및 재시작 | Event Sourcing | 여행 일지 |
| **Compensating TX** | 보상 트랜잭션 | 이전 상태로 복원 | Undo 로직 | 예약 취소 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    사가 패턴: Choreography vs Orchestration                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Choreography (코레오그래피) - 이벤트 기반 분산 조율]                      │
│                                                                             │
│    ┌──────────────┐                                                         │
│    │Order Service │                                                         │
│    └──────┬───────┘                                                         │
│           │ ① OrderCreated 이벤트 발행                                       │
│           ▼                                                                 │
│    ┌─────────────────────────────────────────────────────┐                 │
│    │              Event Bus (Kafka)                      │                 │
│    │  Topic: order-events                                │                 │
│    └────┬─────────────────────────────────────────┬───────┘                 │
│         │                                         │                          │
│         │ ② OrderCreated                          │                          │
│         ▼                                         │                          │
│    ┌──────────────┐    ┌──────────────┐            │                          │
│    │Payment       │    │Inventory     │            │                          │
│    │Service       │    │Service       │            │                          │
│    └──────┬───────┘    └──────┬───────┘            │                          │
│           │                   │                      │                          │
│           │ ③ PaymentCaptured │                      │                          │
│           │───────────────────┼──────────────────────┤                          │
│           │                   │                      │                          │
│           │                   │ ④ StockReserved     │                          │
│           │                   │                      │                          │
│           │           ┌───────▼──────────┐          │                          │
│           │           │ Shipping Service │          │                          │
│           │           └───────┬──────────┘          │                          │
│           │                   │                      │                          │
│           │                   │ ⑤ ShipmentCreated    │                          │
│           │                   │                      │                          │
│           │    ┌──────────────▼──────────┐           │                          │
│           │    │   Order Service (완료)  │           │                          │
│           │    └─────────────────────────┘           │                          │
│           │                                               │                       │
│           │ [장애 시]                                     │                       │
│           │ ② PaymentFailed → ④ StockReleased → ① OrderCancelled│              │
│                                                                             │
│                                                                             │
│  [Orchestration (오케스트레이션) - 중앙 코디네이터]                        │
│                                                                             │
│    ┌───────────────────────────────────────────────────────────┐            │
│    │              Saga Orchestrator Service                   │            │
│    │  ┌─────────────────────────────────────────────────┐     │            │
│    │  │  State Machine (상태 기계)                       │     │            │
│    │  │                                                  │     │            │
│    │  │  ┌──────────┐    ┌──────────┐    ┌──────────┐ │     │            │
│    │  │  │  START   │───►│ PAYMENT  │───►│INVENTORY │ │     │            │
│    │  │  └──────────┘    └──────────┘    └──────────┘ │     │            │
│    │  │       │                │                │       │     │            │
│    │  │       │                │                ▼       │     │            │
│    │  │       │                │          ┌──────────┐ │     │            │
│    │  │       │                │          │SHIPPING  │ │     │            │
│    │  │       │                │          └──────────┘ │     │            │
│    │  │       │                │                │       │     │            │
│    │  │       │                │                ▼       │     │            │
│    │  │       │                │          ┌──────────┐ │     │            │
│    │  │       │                └───────────►│COMPLETED │ │     │            │
│    │  │       │                           └──────────┘ │     │            │
│    │  │       │                                        │     │            │
│    │  │       │ [장애 시 보상 트랜잭션]                  │     │            │
│    │  │       │  ┌──────────┐    ┌──────────┐          │     │            │
│    │  │       └──►COMPENSATE│◄───►COMPENSATE│          │     │            │
│    │  │          │SHIPPING   │    │INVENTORY  │          │     │            │
│    │  │          └──────────┘    └──────────┘          │     │            │
│    │  │                  │                               │     │            │
│    │  │                  ▼                               │     │            │
│    │  │          ┌──────────┐                           │     │            │
│    │  │          │COMPENSATE│                           │     │            │
│    │  │          │PAYMENT   │                           │     │            │
│    │  │          └──────────┘                           │     │            │
│    │  │                  │                               │     │            │
│    │  │                  ▼                               │     │            │
│    │  │          ┌──────────┐                           │     │            │
│    │  │          │CANCELLED │                           │     │            │
│    │  │          └──────────┘                           │     │            │
│    │  └─────────────────────────────────────────────────┘     │            │
│    └───────────────────────────────────────────────────────────┘            │
│           │                │                │                             │
│           ▼                ▼                ▼                             │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐                         │
│    │Payment   │    │Inventory │    │Shipping  │                         │
│    │Service   │    │Service   │    │Service   │                         │
│    └──────────┘    └──────────┘    └──────────┘                         │
│                                                                             │
│  [비교]                                                                     │
│  ┌─────────────────┬──────────────────┬───────────────────┐                │
│  │    특징         │  Choreography    │  Orchestration    │                │
│  ├─────────────────┼──────────────────┼───────────────────┤                │
│  │  복잡도          │ 낮음 (분산)      │ 높음 (중앙화)    │                │
│  │  가시성          │ 낮음 (이벤트 흐름)│ 높음 (상태 기계) │                │
│  │  결합도          │ 낮음            │ 높음             │                │
│  │  장애 격리       │ 높음            │ 낮음 (SPOF)      │                │
│  │  사용 사례       │ 단순 워크플로우   │ 복잡한 비즈니스   │                │
│  └─────────────────┴──────────────────┴───────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Choreography (코레오그래피)**: 각 서비스가 이벤트를 구독하고, 이벤트를 발행하여 느슨하게 결합된 워크플로우를 형성합니다. 춤과 같이 각 참여자가 자신의 파트를 수행하며, **중앙 코디네이터가 없습니다**.

2. **Orchestration (오케스트레이션)**: 중앙 오케스트레이터가 상태 기계(State Machine)을 관리하며, 각 참여자에게 명령을 내립니다. 지휘자가 오케스트라를 지휘하는 것과 같습니다.

### 심층 동작 원리

```
① 사가 시작 (Start)
   └─> 비즈니스 트랜잭션 ID 생성
   └─> Saga Log에 시작 이벤트 기록

② 로컬 트랜잭션 실행 (Execute Local Transaction)
   └─> 각 참여자가 자신의 DB에 트랜잭션 커밋
   └─> 완료 이벤트 발행

③ 성공 시 다음 단계 진행 (Continue)
   └─> 순차적으로 다음 참여자 호출

④ 실패 시 보상 트랜잭션 실행 (Compensate)
   └─> 완료된 역순으로 보상 트랜잭션 실행
   └─> 이전 상태로 복원

⑤ 사가 완료 (Complete/Cancelled)
   └─> 최종 상태 기록
   └─> Saga Log에 완료 이벤트 기록
```

### 핵심 알고리즘 & 코드

```java
// ============ 사가 오케스트레이터 (Spring State Machine) ============

import org.springframework.statemachine.StateMachine;
import org.springframework.statemachine.config.StateMachineBuilder;

/*
--- 사가 상태 정의 ---
enum SagaState {
    START,
    PAYMENT_PENDING,
    PAYMENT_COMPLETED,
    INVENTORY_PENDING,
    INVENTORY_COMPLETED,
    SHIPPING_PENDING,
    COMPLETED,
    COMPENSATING_PAYMENT,
    COMPENSATING_INVENTORY,
    CANCELLED
}
*/

@Component
public class OrderSagaOrchestrator {

    private final StateMachine<SagaState, SagaEvent> stateMachine;
    private final SagaLogRepository sagaLogRepository;

    /**
     * 사가 상태 기계 초기화
     */
    public OrderSagaOrchestrator() throws Exception {
        StateMachineBuilder.Builder<SagaState, SagaEvent> builder =
            StateMachineBuilder.builder();

        // 상태 정의
        builder.configureStates()
            .withStates()
                .initial(SagaState.START)
                .states(EnumSet.allOf(SagaState.class))
                .end(SagaState.COMPLETED)
                .end(SagaState.CANCELLED);

        // 상태 전이 정의
        builder.configureTransitions()
            // 정상 흐름
            .withExternal()
                .source(SagaState.START).target(SagaState.PAYMENT_PENDING)
                .event(SagaEvent.START_PAYMENT)
                .action(paymentAction())
            .and()
            .withExternal()
                .source(SagaState.PAYMENT_PENDING).target(SagaState.PAYMENT_COMPLETED)
                .event(SagaEvent.PAYMENT_SUCCESS)
            .and()
            .withExternal()
                .source(SagaState.PAYMENT_COMPLETED).target(SagaState.INVENTORY_PENDING)
                .event(SagaEvent.START_INVENTORY)
                .action(inventoryAction())
            .and()
            .withExternal()
                .source(SagaState.INVENTORY_PENDING).target(SagaState.INVENTORY_COMPLETED)
                .event(SagaEvent.INVENTORY_SUCCESS)
            .and()
            .withExternal()
                .source(SagaState.INVENTORY_COMPLETED).target(SagaState.COMPLETED)
                .event(SagaEvent.COMPLETE_SAGA)
            // 보상 흐름
            .and()
            .withExternal()
                .source(SagaState.INVENTORY_PENDING).target(SagaState.COMPENSATING_PAYMENT)
                .event(SagaEvent.INVENTORY_FAILED)
                .action(compensatePaymentAction())
            .and()
            .withExternal()
                .source(SagaState.COMPENSATING_PAYMENT).target(SagaState.CANCELLED)
                .event(SagaEvent.PAYMENT_COMPENSATED);

        this.stateMachine = builder.build();
    }

    /**
     * 결제 로컬 트랜잭션 액션
     */
    private Action<SagaState, SagaEvent> paymentAction() {
        return context -> {
            String sagaId = (String) context.getMessageHeader("SAGA_ID");
            Order order = (Order) context.getMessageHeader("ORDER");

            try {
                // 결제 서비스 호출
                Payment payment = paymentService.processPayment(
                    new PaymentRequest(order.getAmount(), order.getPaymentMethod())
                );

                // Saga Log 기록
                sagaLogRepository.save(SagaLog.builder()
                    .sagaId(sagaId)
                    .state(SagaState.PAYMENT_COMPLETED)
                    .payload(payment)
                    .build());

                // 다음 상태로 전이
                stateMachine.sendEvent(SagaEvent.PAYMENT_SUCCESS);

            } catch (PaymentException e) {
                // 실패 시 보상 트랜잭션 트리거
                stateMachine.sendEvent(SagaEvent.PAYMENT_FAILED);
            }
        };
    }

    /**
     * 결제 보상 트랜잭션 액션
     */
    private Action<SagaState, SagaEvent> compensatePaymentAction() {
        return context -> {
            String sagaId = (String) context.getMessageHeader("SAGA_ID");

            // Saga Log에서 이전 상태 조회
            SagaLog paymentLog = sagaLogRepository
                .findFirstBySagaIdOrderByTimestampDesc(sagaId)
                .orElseThrow();

            // 보상 트랜잭션 실행
            Payment payment = paymentLog.getPayload();
            paymentService.refundPayment(payment.getId());

            // Saga Log 기록
            sagaLogRepository.save(SagaLog.builder()
                .sagaId(sagaId)
                .state(SagaState.COMPENSATING_PAYMENT)
                .payload("Payment compensated: " + payment.getId())
                .build());

            // 다음 상태로 전이
            stateMachine.sendEvent(SagaEvent.PAYMENT_COMPENSATED);
        };
    }

    /**
     * 사가 시작
     */
    public String startSaga(Order order) {
        String sagaId = UUID.randomUUID().toString();

        // Saga Log에 시작 기록
        sagaLogRepository.save(SagaLog.builder()
            .sagaId(sagaId)
            .state(SagaState.START)
            .payload("Saga started for order: " + order.getId())
            .build());

        // 상태 기계에 메시지 전송
        Message<SagaEvent> message = MessageBuilder
            .withPayload(SagaEvent.START_PAYMENT)
            .setHeader("SAGA_ID", sagaId)
            .setHeader("ORDER", order)
            .build();

        stateMachine.sendEvent(message);

        return sagaId;
    }
}

// ============ Saga Log (Event Sourcing 기반) ============

@Entity
@Table(name = "saga_log")
@Data
@Builder
class SagaLog {
    @Id
    private String id;

    @Column(nullable = false)
    private String sagaId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaState state;

    @Column(columnDefinition = "TEXT")
    private String payload;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @Column(nullable = false)
    @Version
    private Long version;  // Optimistic Locking
}

// ============ Saga 참여자 서비스 예시 ============

@Service
class PaymentService {

    @Transactional
    public Payment processPayment(PaymentRequest request) {
        // ① 로컬 트랜잭션 시작
        Payment payment = Payment.builder()
            .id(UUID.randomUUID().toString())
            .amount(request.getAmount())
            .status(PaymentStatus.PENDING)
            .build();

        paymentRepository.save(payment);

        // ② 외부 PG사 호출
        try {
            PGResponse pgResponse = pgClient.charge(
                request.getAmount(),
                request.getPaymentMethod()
            );

            // ③ 로컬 트랜잭션 커밋
            payment.setStatus(PaymentStatus.COMPLETED);
            payment.setPgTransactionId(pgResponse.getTransactionId());
            paymentRepository.save(payment);

            return payment;

        } catch (PGException e) {
            // 실패 시 로컬에서만 롤백
            payment.setStatus(PaymentStatus.FAILED);
            payment.setErrorMessage(e.getMessage());
            paymentRepository.save(payment);
            throw new PaymentException("Payment failed", e);
        }
    }

    @Transactional
    public void refundPayment(String paymentId) {
        // 보상 트랜잭션
        Payment payment = paymentRepository.findById(paymentId)
            .orElseThrow();

        if (payment.getStatus() == PaymentStatus.COMPLETED) {
            // PG사 환불 요청
            pgClient.refund(payment.getPgTransactionId());

            // 상태 업데이트
            payment.setStatus(PaymentStatus.REFUNDED);
            paymentRepository.save(payment);
        }
    }
}

// ============ 코레오그래피 패턴 (이벤트 기반) ============

/*
@Service
class OrderService {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Transactional
    public void createOrder(Order order) {
        // ① 주문 생성
        orderRepository.save(order);

        // ② OrderCreated 이벤트 발행
        OrderEvent event = OrderEvent.builder()
            .eventType("OrderCreated")
            .orderId(order.getId())
            .amount(order.getAmount())
            .build();

        kafkaTemplate.send("order-events", order.getId(), event);
    }
}

@Service
@KafkaListener(topics = "order-events")
class PaymentService {

    @KafkaListener
    @Transactional
    public void handleOrderCreated(OrderEvent event) {
        try {
            // 결제 처리
            Payment payment = processPayment(event);

            // PaymentCaptured 이벤트 발행
            kafkaTemplate.send("payment-events", event.getOrderId(),
                PaymentEvent.builder()
                    .eventType("PaymentCaptured")
                    .orderId(event.getOrderId())
                    .paymentId(payment.getId())
                    .build()
            );

        } catch (PaymentException e) {
            // PaymentFailed 이벤트 발행
            kafkaTemplate.send("payment-events", event.getOrderId(),
                PaymentEvent.builder()
                    .eventType("PaymentFailed")
                    .orderId(event.getOrderId())
                    .errorMessage(e.getMessage())
                    .build()
            );
        }
    }
}

@Service
@KafkaListener(topics = "payment-events")
class InventoryService {

    @KafkaListener
    @Transactional
    public void handlePaymentCaptured(PaymentEvent event) {
        try {
            // 재고 확보
            reserveStock(event);

            // StockReserved 이벤트 발행
            kafkaTemplate.send("inventory-events", event.getOrderId(),
                InventoryEvent.builder()
                    .eventType("StockReserved")
                    .orderId(event.getOrderId())
                    .build()
            );

        } catch (InsufficientStockException e) {
            // StockReservationFailed 이벤트 발행
            kafkaTemplate.send("inventory-events", event.getOrderId(),
                InventoryEvent.builder()
                    .eventType("StockReservationFailed")
                    .orderId(event.getOrderId())
                    .build()
            );
        }
    }

    @KafkaListener
    @Transactional
    public void handlePaymentFailed(PaymentEvent event) {
        // 결제 실패 시 재수행 불필요
        log.info("Payment failed for order: {}", event.getOrderId());
    }
}

@Service
@KafkaListener(topics = "inventory-events")
class ShippingService {

    @KafkaListener
    @Transactional
    public void handleStockReserved(InventoryEvent event) {
        // 배송 시작
        Shipment shipment = startShipping(event);

        // ShipmentCreated 이벤트 발행
        kafkaTemplate.send("shipping-events", event.getOrderId(),
            ShippingEvent.builder()
                .eventType("ShipmentCreated")
                .orderId(event.getOrderId())
                .shipmentId(shipment.getId())
                .build()
        );
    }
}
*/
```

### 📢 섹션 요약 비유

마치 **도미노**와 같습니다. 도미노를 순서대로 세우다가(정상 흐름), 중간에 넘어지면(장애), 이미 세워진 도미노를 역순으로 치워서(보상 트랜잭션) 원래 상태로 복원합니다. 오케스트레이터는 도미노를 세우는 사람, 코레오그래피는 각 도미노가 스스로 다음 도미노를 넘어뜨리는 것과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: 트랜잭션 관리 패턴

| 패턴 | 일관성 | 가용성 | 성능 | 복잡도 | 사용 사례 |
|:---|:---:|:---:|:---:|:---:|:---|
| **2PC (XA)** | Strong | Low | Locking | 낮음 | 단일 DB 환경 |
| **Saga (Choreography)** | Eventual | High | 빠름 | 중간 | 단순 워크플로우 |
| **Saga (Orchestration)** | Eventual | Medium | 중간 | 높음 | 복잡한 비즈니스 |
| **Event Sourcing** | Eventual | High | 중간 | 매우 높음 | 재생 필요 시스템 |
| **Local-only TX** | Weak | High | 매우 빠름 | 매우 낮음 | 일관성 불필요 |

### 과목 융합 관점

**1) 데이터베이스 관점 (트랜잭션 격리 수준)**

사가 패턴은 **결과적 일관성(Eventual Consistency)**을 보장합니다.

```
┌─────────────────────────────────────────────────────────────┐
│               ACID vs BASE (Saga)                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [ACID (2PC)]                                              │
│  - Atomicity: 모두 성공 또는 모두 실패                       │
│  - Consistency: 강한 일관성                                │
│  - Isolation: Locking으로 격리                             │
│  - Durability: 영구 저장                                    │
│                                                             │
│  [BASE (Saga)]                                             │
│  - Basically Available: 기본적으로 가용                    │
│  - Soft state: 결과적 일관성 허용                          │
│  - Eventually consistent: 최종적으로 일치                   │
│                                                             │
│  [예시: 주문 → 결제 → 재고]                                 │
│  Time 0: Order Created (Pending)                           │
│  Time 1: Payment Captured (Partially Completed)            │
│  Time 2: Stock Reserved (Partially Completed)              │
│  Time 3: Shipment Created (Completed)  ◄──── 일관성 도달   │
└─────────────────────────────────────────────────────────────┘
```

**2) 분산 시스템 관점 (CAP 정리)**

사가 패턴은 **AP (Availability + Partition Tolerance)** 시스템입니다.

- **가용성 우선**: 각 서비스가 자신의 로컬 트랜잭션을 커밋하므로, 시스템 전체가 Locking되지 않음
- **결과적 일관성**: 최종적으로 모든 상태가 동기화됨을 보장하지만, 중간 단계에서는 불일치 가능
- **네트워크 분격 내성**: 파티셔닝 발생 시 Saga Log를 통해 재시도 가능

### 📢 섹션 요약 비유

마치 **연쇄 우편(Chain Letter)**과 같습니다. 각 수신자는 이전 수신자로부터 편지를 받고(이벤트 수신), 다음 수신자에게 편지를 보냅니다(이벤트 발행). 중간에 누군가 편지를 잃어버리면(장애), 이전 수신자들은 편지를 회수할 수 있습니다(보상). 최종적으로 모든 사람이 편지를 받으면 완성입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 여행 예약 시스템**

```
┌─────────────────────────────────────────────────────────────┐
│                  여행 예약 사가 예시                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [참여자]                                                   │
│  - AirlineService: 항공편 예약/취소                         │
│  - HotelService: 호텔 예약/취소                             │
│  - CarRentalService: 렌터카 예약/취소                       │
│                                                             │
│  [정상 흐름]                                                │
│  1. BookFlight (TX1) ──────────────────────┐               │
│     └─> Compensate: CancelFlight          │               │
│                                           │               │
│  2. BookHotel (TX2) ──────────────────────┤               │
│     └─> Compensate: CancelHotel          │               │
│                                           │               │
│  3. BookCar (TX3) ────────────────────────┤               │
│     └─> Compensate: CancelCar            │               │
│                                           │               │
│  4. SendConfirmation (TX4) ◄─────────────┘               │
│     └─> Compensate: SendCancellation                    │
│                                                             │
│  [장애 시나리오: TX3 실패]                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │TX1: OK  │───►│TX2: OK  │───►│TX3: FAIL│                │
│  └────┬────┘    └────┬────┘    └────┬────┘                │
│       │              │              │                      │
│       │              │         [Compensate]               │
│       │              │              ▼                      │
│       │              │         CancelCar                 │
│       │              │              │                      │
│       │         [Compensate]       │                      │
│       │              ▼              ▼                      │
│       │         CancelHotel      (완료)                   │
│       │              │                                     │
│       │         [Compensate]                              │
│       │              ▼                                     │
│       │         CancelFlight                              │
│       │              │                                     │
│       ▼              ▼                                     │
│    (완료)         (완료)                                  │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **사가 유형 선택**: Choreography (단순) vs Orchestration (복잡한 의사결정 필요)
2. **보상 트랜잭션 설계**: 각 TX의 Undo 로직 정의
3. **Saga Log 저장소**: Event Store (Kafka) vs Database (PostgreSQL)

**Scenario 2: 핀테크 계좌 이체**

```java
@Service
class MoneyTransferSaga {

    /**
     * 계좌 이체 사가 실행
     */
    public String transferMoney(TransferRequest request) {
        String sagaId = UUID.randomUUID().toString();

        // ① 출금 계좌에서 인출
        Transaction debitTx = accountService.debit(
            request.getFromAccount(),
            request.getAmount()
        );

        sagaLogRepository.save(SagaLog.builder()
            .sagaId(sagaId)
            .state("DEBIT_COMPLETED")
            .transactionId(debitTx.getId())
            .build());

        try {
            // ② 입금 계좌에 입금
            Transaction creditTx = accountService.credit(
                request.getToAccount(),
                request.getAmount()
            );

            // ③ 사가 완료
            sagaLogRepository.save(SagaLog.builder()
                .sagaId(sagaId)
                .state("COMPLETED")
                .build());

            return sagaId;

        } catch (CreditFailedException e) {
            // 보상 트랜잭션: 인출 취소
            accountService.refund(debitTx.getId());

            sagaLogRepository.save(SagaLog.builder()
                .sagaId(sagaId)
                .state("CANCELLED")
                .errorMessage("Credit failed: " + e.getMessage())
                .build());

            throw new MoneyTransferException("Transfer failed", e);
        }
    }
}
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **사가 유형** | Choreography vs Orchestration 결정 | |
| **보상 트랜잭션** | 모든 로컬 TX에 대한 Undo 로직 | |
| **Saga Log** | 상태 영속화 및 재시도 가능성 | |
| **이벤트 버전** | 이벤트 스키마 진화 전략 | |
| **재시도 정책** | Exponential Backoff 적용 | |
| **모니터링** | 사가 상태 추적 대시보드 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **멱등성** | 중복 이벤트 처리 방지 | |
| **중복 방지** | Saga ID 기반 중복 실행 방지 | |
| **감사 로그** | 모든 상태 변경 기록 | |
| **롤백 정책** | 수동 보상 트리거 스크립트 | |

### 안티패턴

**❌ 보상 불가능한 트랜잭션**

```java
// 안티패턴: 보상 불가능한 외부 효과
@SagaOrchestration
public void processOrder(Order order) {
    // ① 이메일 발송 (보상 불가!)
    emailService.sendOrderConfirmation(order);

    // ② SMS 발송 (보상 불가!)
    smsService.sendShippingNotification(order);

    // ③ 배송 시작
    shippingService.startShipping(order);
}
```

**개선 방안**:

```java
// 올바른 패턴: 보상 가능한 트랜잭션 후에 외부 효과 실행
@SagaOrchestration
public void processOrder(Order order) {
    // ① 재고 확보 (보상 가능: 재고 반환)
    inventoryService.reserveStock(order);

    // ② 결제 승인 (보상 가능: 환불)
    paymentService.authorizePayment(order);

    // ③ 배송 시작 (보상 가능: 배송 취소)
    shippingService.startShipping(order);

    // ④ 사가 완료 후 외부 효과 실행 (보상 불필요)
    sagaCompletionHandler.onCompleted(() -> {
        emailService.sendOrderConfirmation(order);
        smsService.sendShippingNotification(order);
    });
}
```

### 📢 섹션 요약 비유

마치 **연쇄 식당 예약**과 같습니다. 식당 A, B, C를 순서대로 예약하다가 C가 만석이면, B와 A의 예약을 역순으로 취소합니다. 이때, "이미 보낸 초대장"은 취소할 수 없으므로(보상 불가), 모든 예약이 완료된 후에 초대장을 보내야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | 2PC | Saga | 개선 효과 |
|:---|:---:|:---:|:---|
| **가용성** | 99% (Coordinator SPOF) | 99.99% | **+0.99%** |
| **응답 시간** | 5초 (Locking 대기) | 500ms (비동기) | **90% 단축** |
| **확장성** | 낮음 (Locking) | 높음 (분산) | **10배 이상** |
| **복잡도** | 낮음 | 중간 (보상 로직) | **개발 노력 +30%** |
| **일관성** | Strong | Eventual | **용도에 따라 선택** |

### 미래 전망

1. **AI 기반 사가 최적화**: ML로 최적의 보상 순서 및 타이밍 결정
2. **분산 사가 조율**: DLT(Distributed Ledger Technology)를 활용한 불변 로그
3. **자가 치유 사가**: 장애를 자동으로 감지하고 재시도하는 Intelligent Saga
4. **Quantum-Safe Saga**: 양자 내성 암호화를 활용한 안전한 사가 로그

### 참고 표준

- **Saga Paper** (Garcia-Molina, Salem, 1987)
- **Microservices Patterns** (Chris Richardson, 2018)
- **Spring Cloud Saga** (Seata)
- **NTransactions Saga** (Netflix)
- **Axon Framework** (Event Sourcing + Saga)

### 📢 섹션 요약 비유

미래의 사가 패턴은 **스마트 계약(Smart contract)**과 결합하여 더욱 강력해질 것입니다. 블록체인에 사가 로그를 기록하여, **불변의 추적성**과 **자동 실행**을 동시에 확보하는 분산 트랜잭션 시스템이 실현될 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[마이크로서비스 아키텍처](./556_msa.md)**: MSA 전체 패턴
- **[바운디드 컨텍스트](./614_bounded_context_microservices.md)**: 서비스 분리 기준
- **[이벤트 소싱](./620_event_sourcing.md)**: 상태 재생 패턴
- **[CQRS](./621_cqrs.md)**: 명령/조회 분리
- **[애그리게이트 루트](./615_aggregate_root.md)**: 트랜잭션 경계

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: 여행을 갈 때 **비행기, 호텔, 렌터카**를 모두 예약해야 완성되는 것처럼, 컴퓨터 시스템도 여러 서비스가 모두 성공해야 완료되는 작업이 많습니다.

**2) 원리**: 렌터카 예약이 실패하면, 이미 예약한 호텔과 비행기를 취소해야 합니다. 사가 패턴은 이 **취소 과정(보상)**을 자동으로 처리해줍니다.

**3) 효과**: 각 서비스가 독립적으로 작동하면서도, 전체가 하나의 큰 작업처럼 완료되거나 취소될 수 있습니다. 마치 연쇄 식당 예약을 한 번에 관리할 수 있는 것과 같습니다.
