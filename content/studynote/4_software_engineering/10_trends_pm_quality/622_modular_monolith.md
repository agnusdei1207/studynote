+++
title = "622. 모듈러 모놀리스 (Modular Monolith) MSA 대안적 접근"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 모듈러 모놀리스 (Modular Monolith) MSA 대안적 접근

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 논리적으로는 모듈화되었지만 물리적으로는 단일 애플리케이션으로 배포되는 **"MSA로의 가교 전략"**
> 2. **가치**: MSA의 복잡도를 회피하면서 모듈성 확보, 향후 MSA로의 원활한 마이그레이션 → 개발 효율 50% 향상
> 3. **융합**: Clear Architecture, DDD, 모듈화 경계, 의존성 주입과 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**모듈러 모놀리스 (Modular Monolith)**는 **단일 배포 단위(단일 프로세스/단일 데이터베이스)**를 유지하면서, 내부를 **느슨하게 결합된 모듈(Loosely Coupled Modules)**로 구성하는 아키텍처입니다. Martin Fowler가 정의한 이 패턴은 **MSA의 선행 단계** 또는 **MSA의 부작용을 회피하는 대안**으로 널리 사용됩니다.

핵심 원칙은 **"모듈 간 통신은 잘 정의된 인터페이스를 통해서만 허용"**하며, **"모듈 간 직접적인 데이터베이스 접근을 금지"**합니다. 이는 각 모듈이 독립적으로 개발/테스트될 수 있게 하며, 향후 필요시 별도의 서비스로 분리(Extract Service)할 수 있게 합니다.

```
┌─────────────────────────────────────────────────────────────┐
│              Monolith vs Modular Monolith vs MSA            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [전통적 Monolith - 강결합]                                │
│  ┌─────────────────────────────────────────────┐           │
│  │  Monolithic Application                   │           │
│  │  ┌─────────────────────────────────────┐   │           │
│  │  │                                 │   │           │
│  │  │  Package A ────┐                  │   │           │
│  │  │               │                  │   │           │
│  │  │  Package B ────┼───►             │   │           │
│  │  │               │    Direct Access │   │           │
│  │  │  Package C ────┘                  │   │           │
│  │  │                                 │   │           │
│  │  └─────────────────────────────────────┘   │           │
│  │  [문제점] 강결합, 경계 불명확                    │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Modular Monolith - 느슨한 결합]                         │
│  ┌─────────────────────────────────────────────┐           │
│  │  Modular Monolith                        │           │
│  │  ┌─────────────┐  ┌─────────────┐         │           │
│  │  │   Module A  │  │   Module B  │         │           │
│  │  │ (Order)     │  │ (Inventory) │         │           │
│  │  │             │  │             │         │           │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │         │           │
│  │  │ │Service  │ │  │ │Service  │ │         │           │
│  │  │ │Repository│ │  │ │Repository│ │         │           │
│  │  │ │Domain   │ │  │ │Domain   │ │         │           │
│  │  │ └─────────┘ │  │ └─────────┘ │         │           │
│  │  │             │  │             │         │           │
│  │  └─────────────┘  └─────────────┘         │           │
│  │          │                │                 │           │
│  │          │ Interface Call │               │           │
│  │          ▼                ▼                 │           │
│  │  ┌─────────────────────────────────────┐   │           │
│  │  │   Shared Kernel (Common)           │   │           │
│  │  │  - Infrastructure               │   │           │
│  │  │  - Configuration                │   │           │
│  │  │  - Logging                     │   │           │
│  │  └─────────────────────────────────────┘   │           │
│  │  [장점] 모듈 간 격리, 인터페이스 기반 통신         │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [MSA - 물리적 분리]                                          │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐           │
│  │Service A  │    │Service B  │    │Service C  │           │
│  │(Order)    │    │(Inventory)│    │(Shipping) │           │
│  └─────┬─────┘    └─────┬─────┘    └─────┬─────┘           │
│        │                │                │                 │
│        │    HTTP/RPC    │    Message Queue                 │
│        ▼                ▼                ▼                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              API Gateway / Service Mesh              ││
│  └─────────────────────────────────────────────────────────┘│
│  [장점] 독립적 배포, [단점] 운영 복잡도 높음                │
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**아파트 단지**와 같습니다.
- **Monolith**: 모든 방이 연통된 원룸 오픈스형 (강결합)
- **Modular Monolith**: 벽으로 구분된 방이 있지만, 한 건물에 거주 (논리적 분리)
- **MSA**: 각 독립된 주택으로 분리되어 이사 가능 (물리적 분리)

Modular Monolith는 **"이사 준비를 한 아파트"**와 같습니다. 방을 구분해두었기에 필요시 언제든지 독립 주택(MSA)으로 분리할 수 있습니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 전통 Monolith** | 코드베이스 전체가 강결합 | **변경 영향도 파악 어려움** |
| **② MSA 선풍** | 인프라 복잡도, 분산 트랜잭션 | **운영 오버헤드 과도** |
| **③ Modular Monolith** | 모듈성 + 단순 배포 | **"가교 전략" 실현** |
| **④ Extract Module** | 필요시 MSA로 점진적 분리 | **리스크 최소화** |

현재의 비즈니스 요구로서는 **MSA의 복잡도를 감당할 인력/조직 미달, 단일 팀 규모, 빠른 시장 진입**이 필수적입니다.

### 📢 섹션 요약 비유

마치 **닭장의 계란 분리**와 같습니다. 계란을 완전히 분리하기 전에(Extract Service), 먼저 닭장 안에서 마크를 해두어(Modular Monolith), 나중에 분리할 때 혼란 없이 꺼낼 수 있게 준비합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 구분 | 비유 |
|:---|:---|:---|:---|:---|
| **Module** | 독립적 기능 단위 | 인터페이스 기반 통신 | Order, Inventory | 방 |
| **Public API** | 모듈 간 통신 계약 | 명시적 인터페이스 | Interface, DTO | 방문 계약 |
| **Internal Implementation** | 모듈 내부 구현 | Service, Repository | Private | 방 내부 |
| **Shared Kernel** | 공통 코드 | 최소한의 공유 기능 | Infra, Config | 공용 시설 |
| **Dependency Rule** | 의존성 방향 | 단방향 의존 | Module → Module | 일방통행 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    모듈러 모놀리스 상세 구조                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │                    Modular Monolith Application              │   │
│  │                                                                   │   │
│  │  ┌─────────────────────────────────────────────────────────┐     │   │
│  │  │                  Shared Kernel                        │     │   │
│  │  │  ┌─────────────────────────────────────────────────┐   │     │   │
│  │  │  │  - Configuration Properties                       │   │     │   │
│  │  │  │  - Infrastructure (Logging, Metrics)              │   │     │   │
│  │  │  │  - Common Utilities (DateUtils, Validators)       │   │     │   │
│  │  │  │  - Domain Primitives (Money, Email)              │   │     │   │
│  │  │  └─────────────────────────────────────────────────┘   │     │   │
│  │  └─────────────────────────────────────────────────────────┘     │   │
│  │                                                                   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐ │   │
│  │  │  Order Module    │  │ Inventory Module │  │   Payment  │ │   │
│  │  │                  │  │                  │  │   Module   │ │   │
│  │  │  ┌────────────┐  │  │  ┌────────────┐ │  │ ┌────────┐ │   │
│  │  │  │ Public API │  │  │  │ Public API │ │  │ │Public  │ │   │
│  │  │  │  Interface│◄─┼──┼──►│  Interface│ │  │ │ API    │ │   │
│  │  │  └────────────┘  │  │  └────────────┘ │  │ └────────┘ │   │
│  │  │       │         │  │       │         │  │     │       │   │
│  │  │  ▼             │  │  ▼             │  │  ▼             │   │
│  │  │  ┌────────────┐  │  │  ┌────────────┐ │  │  ┌────────┐ │   │
│  │  │  │ Domain     │  │  │  │ Domain     │ │  │  │ Domain │ │   │
│  │  │  │ Service    │  │  │  │ Service    │ │  │  │ Service│ │   │
│  │  │  │ (Private)  │  │  │  │ (Private)  │  │  │ │(Private)│   │
│  │  │  └────────────┘  │  │  └────────────┘ │  │  └────────┘ │   │
│  │  │       │         │  │       │         │  │     │       │   │
│  │  │  ▼             │  │  ▼             │  │  ▼             │   │
│  │  │  ┌────────────┐  │  │  ┌────────────┐ │  │  ┌────────┐ │   │
│  │  │  │ Repository │  │  │  │ Repository │ │  │  │Repository│   │
│  │  │  │ (Private)  │  │  │  │ (Private)  │ │  │  │(Private)│   │
│  │  │  └────────────┘  │  │  └────────────┘ │  │  └────────┘ │   │
│  │  │       │         │  │       │         │  │     │       │   │
│  │  │  ▼             │  │  ▼             │  │  ▼             │   │
│  │  │  ┌────────────┐  │  │  ┌────────────┐ │  │  ┌────────┐ │   │
│  │  │  │   Domain   │  │  │  │   Domain   │ │  │  │  Domain│ │   │
│  │  │  │  Model     │  │  │  │  Model     │ │  │  │  Model│ │   │
│  │  │  │ (Entity,VO)│  │  │  │ (Entity,VO)│ │  │  │(Entity)│ │   │
│  │  │  └────────────┘  │  │  └────────────┘ │  │  └────────┘ │   │
│  │  │                  │  │                  │  │              │   │
│  │  │  [Module DB]      │  │  [Module DB]      │  │  [Module DB] │   │
│  │  │  - order_table   │  │  - inventory_table│  │  - payment_tbl│   │
│  │  │  - order_item    │  │  - stock         │  │  - transaction│   │
│  │  └──────────────────┘  └──────────────────┘  └────────────┘ │   │
│  │                                                                   │   │
│  │  [통신 규칙]                                                       │   │
│  │  - 모듈 간 통신은 Public API 인터페이스로만                  │   │
│  │  - 다른 모듈의 Internal Implementation에 직접 접근 금지     │   │
│  │  - 의존성 방향: Order → Inventory → Payment (단방향)          │   │
│  │                                                                   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [의존성 규칙 (Dependency Rule)]                                          │
│  ┌─────────────────────────────────────────────────────────────┐         │
│  │                 ┌──────────────┐                          │         │
│  │                 │  Core Layer  │                          │         │
│  │                 │  (Domain)     │  ◄───谁도依赖               │         │
│  │                 └───────┬──────┘                          │         │
│  │                         │                                 │         │
│  │          ┌────────────────┼────────────────┐               │         │
│  │          ▼                ▼                ▼               │         │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │         │
│  │  │ Adapter     │  │ Port        │  │ Application │        │         │
│  │  │ (Interface) │  │ (Interface) │  │ (Service)   │        │         │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │         │
│  │       ▲                ▲                ▲                  │         │
│  │       └────────────────┴────────────────┘                  │         │
│  │                 ┌──────────────┐                          │         │
│  │                 │ Infrastructure│                          │         │
│  │                 │  (Framework)  │                          │         │
│  │                 └──────────────┘                          │         │
│  └─────────────────────────────────────────────────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Module 경계**: 각 모듈(Order, Inventory, Payment)은 자신만의 **Domain Layer**, **Service Layer**, **Repository Layer**를 가지며, 독립적으로 개발/테스트될 수 있습니다.

2. **Public API**: 각 모듈은 명시적인 **인터페이스(Java Interface, TypeScript Protocol)**를 노출하며, 이를 통해서만 다른 모듈과 통신합니다. 내부 구현은 **Private**으로 숨겨져 있습니다.

3. **Shared Kernel**: 모든 모듈이 공유하는 최소한의 코드입니다. 단순 유틸리티, 인프라스트럭처, 도메인 프리미티브(Money, Email)가 포함됩니다. **공유를 최소화**하여 모듈 간 결합도를 낮춥니다.

4. **의존성 규칙**: Clean Architecture의 **Dependency Rule**을 따라, **내부 계층(Core)이 외부 계층(Infrastructure)를 의존하지 않도록** 합니다.

### 심층 동작 원리

```
① 모듈 정의 (Module Definition)
   └─> 패키지 구조로 물리적 분리
   └─> OrderModule, InventoryModule, PaymentModule

② 인터페이스 정의 (Public API)
   └─> OrderService, InventoryService 인터페이스
   └─> 메서드 시그니처만 노출

③ 의존성 주입 (Dependency Injection)
   └─> 구현체를 Spring/@Injectable 등으로 등록
   └─> 모듈 간 참조는 인터페이스로만

④ 모듈 간 통신 (Inter-Module Communication)
   └─> 인터페이스 통한 메서드 호출
   └─> 동기식 (In-Process) 또는 비동기식 (Event Bus)

⑤ 모듈 분리 (Extract Module)
   └─> 필요시 모듈을 독립 애플리케이션으로 분리
   └─> HTTP/gRPC로 통신하도록 변환
```

### 핵심 알고리즘 & 코드

```java
// ============ 모듈 경계 정의 (Spring Boot) ============

/**
 * 주문 모듈 패키지 구조
 *
 * com.company.app
 * ├── shared/                 [Shared Kernel]
 * │   ├── config/
 * │   ├── infrastructure/
 * │   └── domain/
 * ├── order/                  [Order Module]
 * │   ├── OrderApplication.java  [Public API]
 * │   ├── domain/
 * │   │   ├── OrderService.java   [Private Implementation]
 * │   │   ├── Order.java
 * │   │   └── OrderRepository.java
 * │   └── persistence/
 * │       └── OrderRepositoryImpl.java
 * ├── inventory/              [Inventory Module]
 * │   ├── InventoryApplication.java
 * │   ├── domain/
 * │   │   ├── InventoryService.java
 * │   │   └── InventoryRepository.java
 * │   └── persistence/
 * │       └── InventoryRepositoryImpl.java
 * └── payment/                [Payment Module]
 *     ├── PaymentApplication.java
 *     ├── domain/
 *     │   ├── PaymentService.java
 *     │   └── PaymentRepository.java
 *     └── persistence/
 *         └── PaymentRepositoryImpl.java
 */

// ============ 모듈 공용 API (Public Interface) ============

/**
 * 주문 모듈의 공용 인터페이스
 */
public interface OrderService {
    Order createOrder(CreateOrderRequest request);
    Order getOrder(String orderId);
    void cancelOrder(String orderId);
    List<Order> getCustomerOrders(String customerId);
}

/**
 * 재고 모듈의 공용 인터페이스
 */
public interface InventoryService {
    void reserveStock(ReserveStockCommand command);
    void releaseStock(ReleaseStockCommand command);
    int getAvailableQuantity(String productId);
}

/**
 * 결제 모듈의 공용 인터페이스
 */
public interface PaymentService {
    PaymentResult processPayment(PaymentRequest request);
    void refundPayment(String paymentId);
}

// ============ 모듈 내부 구현 (Private) ============

/**
 * 주문 모듈 내부 서비스 구현
 * 패키지 private으로 외부에서 직접 접근 방지
 */
@Service
@PackageScoped  // 커스텀 애너테이션으로 모듈 경계 강제
class OrderServiceImpl implements OrderService {

    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;  // 모듈 간 참조
    private final PaymentService paymentService;        // 모듈 간 참조
    private final OrderEventPublisher eventPublisher;

    /**
     * 주문 생성 (모듈 간 조율)
     */
    @Override
    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        // ① 도메인 로직 수행
        Order order = Order.create(
            request.getCustomerId(),
            request.getItems()
        );

        // ② 주문 저장
        orderRepository.save(order);

        // ③ 이벤트 발행 (선택 사항)
        eventPublisher.publish(new OrderCreatedEvent(order.getId()));

        return order;
    }

    /**
     * 주문 취소 (모듈 간 통신)
     */
    @Override
    @Transactional
    public void cancelOrder(String orderId) {
        // ① 주문 로드
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        // ② 비즈니스 로직
        order.cancel();

        // ③ 재고 모듈 호출 (인터페이스 통해서만)
        inventoryService.releaseStock(
            new ReleaseStockCommand(order.getItems())
        );

        // ④ 결제 모듈 호출 (인터페이스 통해서만)
        if (order.getPaymentId() != null) {
            paymentService.refundPayment(order.getPaymentId());
        }

        // ⑤ 저장
        orderRepository.save(order);
    }
}

// ============ 모듈 경계 강제 (Arch Unit Test) ============

/**
 * 아키텍처 규칙 테스트
 * 모듈 간 의존성을 강제하는 정적 분석
 */
@AnalyzeClasses(packages = "com.company.app")
public class ModularMonolithArchitectureTest {

    @ArchTest
    static final ArchRules order_module_rules = defineArchitecture()
        // 주문 모듈은 재고 모듈의 구현체에 직접 의존하면 안 됨
        .noClasses()
            .that().resideInAPackage("..order..")
            .should().dependOnClassesThat()
            .resideInAPackage("..inventory..persistence..")
            .because("Order module should only depend on Inventory's public API")
        // 주문 모듈은 결제 모듈의 구현체에 직접 의존하면 안 됨
        .and()
        .noClasses()
            .that().resideInAPackage("..order..")
            .should().dependOnClassesThat()
            .resideInAPackage("..payment..persistence..")
        // 모듈은 Shared Kernel에만 의존 가능
        .and()
        .classes()
            .that().resideOutsideOfPackage("..shared..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("..order..", "..inventory..", "..payment..", "..shared..");
}

// ============ 의존성 주입 구성 (Spring) ============

/**
 * 모듈별 Bean 구성
 */
@Configuration
class OrderModuleConfiguration {

    @Bean
    public OrderService orderService(
        OrderRepository orderRepository,
        InventoryService inventoryService,  // 인터페이스로만 참조
        PaymentService paymentService        // 인터페이스로만 참조
    ) {
        return new OrderServiceImpl(orderRepository, inventoryService, paymentService);
    }
}

@Configuration
class InventoryModuleConfiguration {

    @Bean
    public InventoryService inventoryService(InventoryRepository repository) {
        return new InventoryServiceImpl(repository);
    }
}

@Configuration
class PaymentModuleConfiguration {

    @Bean
    public PaymentService paymentService(PaymentRepository repository) {
        return new PaymentServiceImpl(repository);
    }
}

// ============ 이벤트 기반 모듈 간 통신 (선택 사항) ============

/**
 * 이벤트 발행기 (Spring Event)
 */
@Component
class OrderEventPublisher {

    private final ApplicationEventPublisher eventPublisher;

    public void publish(OrderCreatedEvent event) {
        eventPublisher.publishEvent(event);
    }
}

/**
 * 이벤트 구독자 (다른 모듈에서)
 */
@Component
class InventoryEventSubscriber {

    private final InventoryService inventoryService;

    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 비동기적으로 재고 확보
        inventoryService.reserveStock(
            new ReserveStockCommand(event.getOrderItems())
        );
    }
}

// ============ 모듈 분리 준비 (Extract Module) ============

/**
 * 모듈을 독립 서비스로 분리하기 위한 준비
 * 향후 MSA로 전환 시 이 인터페이스를 REST/gRPC로 변경
 */
public interface OrderServiceV2 {  // 향후 분리를 위한 버전 2 인터페이스
    @GetMapping("/api/orders/{id}")
    ResponseEntity<OrderDto> getOrder(@PathVariable String id);

    @PostMapping("/api/orders")
    ResponseEntity<OrderDto> createOrder(@RequestBody CreateOrderRequest request);

    @DeleteMapping("/api/orders/{id}")
    ResponseEntity<Void> cancelOrder(@PathVariable String id);
}
```

### 📢 섹션 요약 비유

마치 **연립된 부서**와 같습니다. 각 부서(Order, Inventory, Payment)는 자신의 업무(Private Implementation)를 독립적으로 수행하지만, 부서 간 협업은 **공문서(Public API)**를 통해서만 진행합니다. 이렇게 하면 나중에 부서를 다른 건물로 이사(MSA)시켜도 협업 방식에 큰 변화가 없습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: Monolith vs Modular Monolith vs MSA

| 비교 항목 | Monolith | Modular Monolith | MSA |
|:---|:---|:---|:---|
| **배포 단위** | 단일 애플리케이션 | 단일 애플리케이션 | 여러 서비스 |
| **코드 경계** | 패키지 (형식적) | 모듈 (명시적 인터페이스) | 서비스 (물리적 분리) |
| **데이터 저장소** | 단일 DB | 단일 DB (스키마 분리) | Database per Service |
| **통신 방식** | 인프로세스 메서드 | 인프로세스 인터페이스 | HTTP/gRPC/Message Queue |
| **확장성** | 수직적 확장만 | 수직적 확장만 | 수평적 확장 가능 |
| **운영 복잡도** | 낮음 | 중간 | 높음 |
| **마이그레이션** | 해당 | MSA로 전환 용이 | 해당 |
| **팀 자율성** | 낮음 | 중간 | 높음 |

### 과목 융합 관점

**1) 소프트웨어 공학 관점 (모듈화)**

Modular Monolith는 **정보 은닉(Information Hiding)**과 **인터페이스 분리 원칙(Interface Segregation)**을 시스템 수준으로 적용한 것입니다.

```
┌─────────────────────────────────────────────────────────────┐
│         모듈화 원칙 (Modularization Principles)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [High Cohesion]                                             │
│  - 모듈 내부 구성요소는 밀접하게 연관                    │
│  - Order Module: 주문 관련 모든 로직 포함                   │
│                                                             │
│  [Low Coupling]                                              │
│  - 모듈 간 의존 최소화                                    │
│  - 인터페이스를 통해서만 통신                              │
│                                                             │
│  [Encapsulation]                                            │
│  - 내부 구현을 숨기고 Public API만 노출                    │
│  - OrderServiceImpl는 Private                                │
└─────────────────────────────────────────────────────────────┘
```

**2) 아키텍처 관점 (Layered vs Modular)**

```
┌─────────────────────────────────────────────────────────────┐
│       Layered Architecture vs Modular Architecture             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Layered - 수직 계층]                                     │
│  ┌─────────────────────────────────────────────┐           │
│  │  Presentation Layer                    │           │
│  │  (Controller, View)                     │           │
│  └──────────────┬──────────────────────────────┘           │
│                 │                                            │
│  ┌──────────────▼──────────────────────────────┘           │
│  │  Business Logic Layer                  │           │
│  │  (Service, Manager)                    │           │
│  └──────────────┬──────────────────────────────┘           │
│                 │                                            │
│  ┌──────────────▼──────────────────────────────┘           │
│  │  Data Access Layer                     │           │
│  │  (Repository, DAO)                     │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Modular - 수평 모듈]                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐              │
│  │  Order    │  │Inventory  │  │  Payment  │              │
│  │  Module   │  │  Module   │  │  Module   │              │
│  │           │  │           │  │           │              │
│  │ ┌─────────┐│  │┌─────────┐│  │┌─────────┐│             │
│  │ │Domain  ││  ││Domain  ││  ││Domain  ││             │
│  │ ├─────────┤│  │├─────────┤│  │├─────────┤│             │
│  │ │Service ││  ││Service ││  ││Service ││             │
│  │ ├─────────┤│  │├─────────┤│  │├─────────┤│             │
│  │ │Repo    ││  ││Repo    ││  ││Repo    ││             │
│  │ └─────────┘│  │└─────────┘│  │└─────────┘│             │
│  └───────────┘  └───────────┘  └───────────┘              │
│                                                             │
│  [결합형: Modular + Layered]                               │
│  각 모듈 내부는 계층형으로 구조화                           │
└─────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

마치 **자동차의 모듈형 설계**와 같습니다. 자동차를 하나의 덩어리(Monolith)로 만들 수도 있지만, 모듈(Modular)로 설계하면 엔진, 변속기, 서스펜션을 독립적으로 교체할 수 있습니다. Modular Monolith는 이 모듈들이 아직 한 차체에 통합되어 있지만, 언제든지 분리할 수 있는 상태입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 전자상거래 플랫폼�**

```
┌─────────────────────────────────────────────────────────────┐
│           Modular Monolith 적용: 이커머스                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [모듈 구성]                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Catalog     │  │  Cart        │  │  Order       │        │
│  │ Module      │  │  Module      │  │  Module      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                             │
│  [Phase 1: 단일 애플리케이션으로 시작]                       │
│  - 모든 모듈이 단일 Jar/실행 파일                             │
│  - 단일 데이터베이스 (스키마 분리)                           │
│  - 단일 CI/CD 파이프라인                                   │
│                                                             │
│  [Phase 2: 병목 모듈 식별]                                 │
│  - Cart 모듈이 트래픽의 60% 차지                           │
│  - Cart 모듈을 독립 서비스로 분리 계획                       │
│                                                             │
│  [Phase 3: Extract Module]                                  │
│  - Cart Service를 마이크로서비스로 분리                     │
│  - 공통 API를 REST/gRPC로 변경                             │
│  - 다른 모듈은 HTTP 통신으로 연결                          │
│                                                             │
│  [Phase 4: 점진적 MSA 전환]                                │
│  - Order → Payment → Shipping 순차 분리                    │
│  - Catalog 검색 엔진 분리                                  │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **모듈 식별**: DDD의 바운디드 컨텍스트 기반 모듈 경계
2. **인터페이스 정의**: 각 모듈의 Public API를 명시적 인터페이스로 정의
3. **Arch Unit Test**: 모듈 간 의존성을 강제하는 정적 분석 테스트
4. **Extract Strategy** : 가장 병목이거나 변경이 잦은 모듈부터 분리

**Scenario 2: 핀테크 결제 시스템**

```java
/**
 * 결제 모듈의 공용 API
 */
public interface PaymentService {
    PaymentResult authorize(PaymentAuthorizeRequest request);
    PaymentResult capture(String paymentId, Money amount);
    void refund(String paymentId, Money amount);
}

/**
 * 결제 모듈 내부 구현
 */
@Service
class PaymentServiceImpl implements PaymentService {

    private final PaymentRepository paymentRepository;
    private final List<PaymentGateway> paymentGateways;  // 전략 패턴

    @Override
    @Transactional
    public PaymentResult authorize(PaymentAuthorizeRequest request) {
        // ① 결제 생성
        Payment payment = Payment.authorize(request.getAmount(), request.getMethod());

        // ② PG사 호출 (전략 패턴으로 라우팅)
        PaymentGateway gateway = selectGateway(request.getMethod());
        PGResponse pgResponse = gateway.authorize(request.getAmount(), request.getPaymentToken());

        // ③ 결과 처리
        if (pgResponse.isApproved()) {
            payment.approve(pgResponse.getTransactionId());
        } else {
            payment.decline(pgResponse.getErrorCode());
        }

        paymentRepository.save(payment);
        return toResult(payment);
    }

    private PaymentGateway selectGateway(PaymentMethod method) {
        return paymentGateways.stream()
            .filter(gw -> gw.supports(method))
            .findFirst()
            .orElseThrow(() -> new PaymentGatewayNotFoundException(method));
    }
}
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **모듈 경계** | 명시적인 인터페이스 정의 | |
| **의존성 방향** | 단방향 의존 준수 (A→B→C) | |
| **공유 커널** | 최소화된 공유 코드 | |
| **패키지 구조** | 물리적 경계로 분리 | |
| **Arch Test** | 의존성 규칙 강제 테스트 | |
| **Extract Plan** | MSA 전환 로드맵 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **배포 파이프라인** | 단일 Jar로 통합 배포 | |
| **모니터링** | 모듈별 메트릭 식별 | |
| **롤아웃 전략** | 모듈 단위 롤백 계획 | |
| **트래픽 분리** | 모듈 간 트래픽 모니터링 | |

### 안티패턴

**❌ 모듈 간 직접적인 DB 접근**

```java
// 안티패턴: Order 모듈이 Inventory 모듈의 DB에 직접 접근
@Service
class OrderServiceImpl {

    @Autowired
    private InventoryRepository inventoryRepository;  // ❌ 다른 모듈의 Repository

    public void createOrder(Order order) {
        // 다른 모듈의 테이블을 직접 조작 (모듈 경계 위반)
        inventoryRepository.updateStock(order.getProductId(), -order.getQuantity());
    }
}
```

**개선 방안**:

```java
// 올바른 패턴: Public API를 통해서만 통신
@Service
class OrderServiceImpl {

    private final InventoryService inventoryService;  // ✅ 인터페이스로만 참조

    public void createOrder(Order order) {
        // Public API를 통한 통신 (모듈 경계 준수)
        inventoryService.reserveStock(
            new ReserveStockCommand(order.getProductId(), order.getQuantity())
        );
    }
}
```

### 📢 섹션 요약 비유

마치 **아파트의 입주자 전용 주차장**과 같습니다. 각 입주자(모듈)는 자신의 주차 공간(Private Implementation)을 가지지만, 공용 도로(Shared Kernel)를 통해 이동합니다. 하지만 다른 입주자의 주차 공간에 함부로 주차할 수 없습니다(모듈 경계 준수). 이렇게 하면 나중에 각 입주자가 독립된 주택(MSA)으로 이사해도 큰 문제가 없습니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | Monolith | Modular Monolith | MSA |
|:---|:---:|:---:|:---|
| **개발 속도** | 빠름 (1x) | 빠름 (1x) | 느림 (0.5x) |
| **배포 복잡도** | 낮음 (1개) | 낮음 (1개) | 높음 (N개) |
| **확장성** | 낮음 | 중간 (향후 MSA로) | 높음 |
| **팀 자율성** | 낮음 | 중간 (모듈별 팀) | 높음 |
| **MSA 전환 기간** | 6개월+ | 2주~1개월/모듈 | 해당 |
| **운영 오버헤드** | 낮음 | 낮음 | 높음 |

### 미래 전망

1. **AI 기반 모듈 식별**: ML로 코드베이스 분석하여 모듈 경계 자동 추천
2. **Dynamic Module Loading**: 런타임에 모듈을 로드/언로드
3. **Modular Serverless**: 서버리스 함수 단위로 모듈 분리
4. **Visual Architecture Modeling**: 모듈 간 의존성을 시각화하는 도구

### 참고 표준

- **Modular Monolith** (Martin Fowler, 2024)
- **Domain-Driven Design** (Eric Evans) - Bounded Context
- **Clean Architecture** (Robert C. Martin)
- **ArchUnit** (ArchUnit Library)
- **Spring Boot Modulith** (Spring Framework)

### 📢 섹션 요약 비유

미래의 Modular Monolith는 **LEGO 블록**과 같이 발전할 것입니다. 각 모듈은 표준화된 인터페이스(LEGO의 결합 홈)를 통해 **필요할 때마다 조립/분리**가능한 **Plug-in Architecture**로 진화할 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[마이크로서비스 아키텍처](./556_msa.md)**: MSA 전체 패턴
- **[바운디드 컨텍스트](./614_bounded_context_microservices.md)**: 모듈 경계 식별
- **[클린 아키텍처](./611_clean_architecture.md)**: 의존성 규칙
- **[DDD](./613_ddd_basics.md)**: 도메인 주도 설계
- **[Extract Module](./extract_module.md)**: 모듈 분리 전략

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: **장난감함**과 같습니다. 모든 장난감이 한 상자에 뒤섞여 있는 대신, 각 장난감별로 정리된 상자에 넣어두면(모듈화), 필요한 장난감만 꺼내서 놀 수 있습니다.

**2) 원리**: 각 상자(모듈)에는 라벨이 붙어 있어서, 무엇이 들어있는지 알 수 있습니다(공용 API). 상자 안의 장난감은 숨겨져 있지만(Private), 상자 전체를 옮길 수 있습니다.

**3) 효과**: 장난감을 찾기가 쉽고, 나중에 각 상자를 다른 방으로 옮길 수도 있습니다. 모든 것을 한 상자에 넣는 것보다 훨씬 정리되어 있습니다.
