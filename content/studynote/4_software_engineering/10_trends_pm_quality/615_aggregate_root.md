+++
title = "615. 애그리게이트 루트 트랜잭션 경계"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 애그리게이트 루트 (Aggregate Root) 트랜잭션 경계

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 애그리게이트는 데이터 일관성을 보장하는 최소 단위이며, 애그리게이트 루트는 유일한 진입점으로 외부 접근을 제어
> 2. **가치**: 트랜잭션 경계 명확화, 동시성 충돌 방지, 도메인 로직 캡슐화 → 데이터 무결성 99.9% 보장
> 3. **융합**: RDBMS 트랜잭션, 분산 시스템 Saga 패턴, ORM(Optimistic Locking)과 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**애그리게이트 (Aggregate)**는 도메인 주도 설계 (DDD, Domain-Driven Design)에서 데이터 변경의 단위가 되는 **연관된 객체들의 묶음**을 의미합니다. 에릭 에반스(Eric Evans)와 본 버논(Vaughn Vernon)이 정의한 이 패턴은 **"데이터 일관성을 보장하기 위해 함께 처리되어야 하는 객체들의 클러스터"**입니다.

**애그리게이트 루트 (Aggregate Root)**는 애그리게이트의 **유일한 진입점**으로, 외부에서 애그리게이트 내부의 객체에 직접 접근하는 것을 금지합니다. 모든 변경은 루트를 통해서만 이루어지며, 이는 **트랜잭션 경계(Transaction Boundary)**를 명확히 하여 데이터 무결성을 보장합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    애그리게이트 구조                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    ┌──────────────────────────────────────┐                │
│    │         애그리게이트 (Aggregate)      │                │
│    │  ┌────────────────────────────────┐  │                │
│    │  │   애그리게이트 루트 (Root)      │  │                │
│    │  │       (Order - 주문)           │  │                │
│    │  └────────┬───────────────────────┘  │                │
│    │           │                           │                │
│    │           │ 참조                      │                │
│    │      ┌────▼─────┐  ┌──────────────┐ │                │
│    │      │OrderItem │  │DeliveryInfo  │ │                │
│    │      │(주문항목) │  │(배송정보)     │ │                │
│    │      └──────────┘  └──────────────┘ │                │
│    └──────────────────────────────────────┘                │
│                                                             │
│  규칙: 외부는 Order(Root)을 통해서만 접근 가능              │
│       OrderItem에 직접 접근 ❌                             │
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**가족(애그리케이트)**과 **가장(루트)**을 생각해보세요. 가족 구성원(자녀, 배우자)을 대표하여 가장이 외부와 모든 거래를 합니다.

- 은행에서 대출을 받을 때: 가장(루트)이 서명
- 가족 구성원의 여권 발급: 가장이 신청
- 가족 간의 내부 일: 외부 개입 ❌

가장을 통하지 않고 자녀에게 직접 접근하는 것은 **사생활 침해(캡슐화 위배)**와 같습니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 테이블 중심** | 객체 간 참조로 무제한 수정 가능, 일관성 깨짐 위험 | **애노테이션 기반 자동 로딩** 오남용 |
| **② 무분별한 FK** | 전이 삭제(Cascade)로 연쇄 수정, 성능 저하 | **FK 제약조건**의 잠재적 위험 |
| **③ ACID 트랜잭션** | 로컬 트랜잭션으로는 한계, 분산 환경에서 문제 | **단일 애그리게이트 = 단일 트랜잭션** 원칙 |
| **④ 애그리게이트 등장** | 명확한 경계, 루트 기반 접근 제어 | **일관성 + 확장성** 동시 확보 |

현재의 비즈니스 요구로서는 **분산 마이크로서비스 환경에서의 데이터 일관성 보장, 동시성 충돌 방지, 대용량 트래픽 처리**가 필수적입니다.

### 📢 섹션 요약 비유

마치 **성곽(Castle)**과 같습니다. 성(애그리게이트) 안에 여러 건물(엔티티)이 있지만, 외부인은 성문(루트)을 통해서만 출입할 수 있습니다. 성문을 통하지 않고 담을 넘는 것은 **침입(불법 접근)**으로 간주합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 프로토콜/기법 | 비유 |
|:---|:---|:---|:---|:---|
| **Aggregate Root** | 유일한 진입점 | 외부 요청을 받아 내부 객체 조작 | Idempotency, Version | 가장 |
| **Entity** | 식별 가능한 객체 | ID로 구분, 상태 변화 가능 | Equality by ID | 주민등록 |
| **Value Object** | 값 자체를 의미 | 불변(Immutable), 식별자 없음 | Equals/HashCode 구현 | 주소, 돈 |
| **Repository** | 영속성 추상화 | 루트별로 독립적 저장소 | CRUD 인터페이스 | 창고 |
| **Domain Event** | 상태 변경 알림 | 애그리게이트 내부에서 발행 | Event Publisher | 소식지 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    애그리게이트 루트 트랜잭션 경계                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                    Order 애그리게이트                             │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  Order (애그리게이트 루트)                                  │  │      │
│  │  │  - id: UUID                                                 │  │      │
│  │  │  - orderItems: List<OrderItem>  [직접 접근 금지]            │  │      │
│  │  │  - deliveryInfo: DeliveryInfo    [직접 접근 금지]            │  │      │
│  │  │  - version: Long (Optimistic Lock)                          │  │      │
│  │  │                                                            │  │      │
│  │  │  + addItem(product, quantity): void                         │  │      │
│  │  │  + removeItem(itemId): void                                │  │      │
│  │  │  + updateDelivery(info): void                              │  │      │
│  │  │  + calculateTotal(): Money                                 │  │      │
│  │  │                                                            │  │      │
│  │  │  [인버리언트 보장]                                          │  │      │
│  │  │  - 주문 항목은 1개 이상                                      │  │      │
│  │  │  - 총 금액 = 항목별 금액의 합                                │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                               │                                   │      │
│  │          ┌────────────────────┼────────────────────┐              │      │
│  │          ▼                    ▼                    ▼              │      │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐        │      │
│  │  │  OrderItem   │    │OrderItem     │    │DeliveryInfo  │        │      │
│  │  │  (엔티티)     │    │  (엔티티)     │    │  (밸류 오브젝트)│       │      │
│  │  │  - id        │    │  - id        │    │  - address   │        │      │
│  │  │  - productId │    │  - productId │    │  - receiver  │        │      │
│  │  │  - quantity  │    │  - quantity  │    │  - phone     │        │      │
│  │  │  - price     │    │  - price     │    │  [불변]      │        │      │
│  │  │  (ID로 식별)  │    │  (ID로 식별)  │    │  (값으로 식별) │       │      │
│  │  └──────────────┘    └──────────────┘    └──────────────┘        │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  [접근 규칙]                                                                │
│  ✅ order.addItem(product, 2)       → 루트 통해 접근 (허용)                │
│  ❌ order.orderItems.get(0).quantity = 3  → 직접 접근 (금지)               │
│  ❌ order.deliveryInfo.address = "..."  → 직접 수정 (금지)                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **애그리게이트 루트(Order)**: 외부의 모든 접근은 Order의 공개 메서드(addItem, removeItem)를 통해서만 가능합니다. 이는 **캡슐화**를 강화하여 도메인 로직을 루트 내부에 보호합니다.

2. **내부 객체 숨기기**: orderItems와 deliveryInfo는 private 필드로 선언되어 있어, 외부에서 직접 접근할 수 없습니다. Java/C#에서는 **불변 컬렉션(Immutable Collection)**을 반환하여 방어적 복사를 수행합니다.

3. **인버리언트(Invariant) 보장**: 애그리게이트 내부의 비즈니스 규칙(인버리언트)을 항상 만족하도록 루트의 메서드 내에서 검증합니다. 예: "총 주문 금액 = 개별 항목 금액의 합"

4. **Optimistic Locking**: version 필드를 통해 동시성 충돌을 감지합니다. A 사용자와 B 사용자가 동시에 수정을 시도하면, 먼저 커밋한 사용자만 성공하고 나중에 커밋한 사용자는 OptimisticLockException을 받습니다.

### 심층 동작 원리

```
① 클라이언트 요청 수신
   └─> REST API /orders/{id}/items

② 애플리케이션 서비스 계층
   └─> 트랜잭션 시작 (@Transactional)
   └─> Repository로부터 Order(루트) 조회
   └─> order.addItem(product, quantity) 호출

③ 애그리게이트 루트 내부 로직 수행
   └─> 인버리언트 검증 (최대 주문 수량 등)
   └─> 도메인 이벤트 발행 (OrderItemAdded)
   └─> 상태 변경

④ 영속화
   └─> Repository.save(order)
   └─> 트랜잭션 커밋

⑤ 이벤트 핸들러 실행
   └─> 재고 서비스에 StockDecreaseRequested 이벤트 발행
```

### 핵심 알고리즘 & 코드

```typescript
// ============ 애그리게이트 루트 구현 (TypeScript) ============

/**
 * 주문 애그리게이트의 루트 엔티티
 * 모든 변경은 이 클래스를 통해서만 이루어져야 함
 */
class Order {
  // 상태 (private으로 직접 접근 방지)
  private readonly _id: string;
  private readonly _orderItems: OrderItem[] = [];
  private _deliveryInfo: DeliveryInfo | null = null;
  private _version: number = 0;  // Optimistic Locking
  private readonly _createdAt: Date;

  // 생성자 (팩토리 메서드 권장)
  private constructor(id: string, createdAt: Date) {
    this._id = id;
    this._createdAt = createdAt;
  }

  // 팩토리 메서드: 새 주문 생성
  static create(productId: string, quantity: number): Order {
    const order = new Order(crypto.randomUUID(), new Date());
    order.addItem(productId, quantity);  // 생성 시 최소 1개 항목
    return order;
  }

  // 비즈니스 로직: 주문 항목 추가
  addItem(productId: string, quantity: number): void {
    // 인버리언트 검증
    if (quantity <= 0) {
      throw new Error("수량은 1개 이상이어야 합니다.");
    }
    if (this._orderItems.length >= 10) {
      throw new Error("주문 항목은 최대 10개까지 가능합니다.");
    }

    // 이미 동일 상품이 있는 경우 수량 증가
    const existingItem = this._orderItems.find(item => item.productId === productId);
    if (existingItem) {
      existingItem.increaseQuantity(quantity);
    } else {
      this._orderItems.push(new OrderItem(productId, quantity));
    }

    // 도메인 이벤트 발행 (이벤트 소싱 고려)
    this.recordEvent(new OrderItemAddedEvent(this._id, productId, quantity));
  }

  // 비즈니스 로직: 주문 항목 제거
  removeItem(itemId: string): void {
    const index = this._orderItems.findIndex(item => item.id === itemId);
    if (index === -1) {
      throw new Error("주문 항목을 찾을 수 없습니다.");
    }
    if (this._orderItems.length === 1) {
      throw new Error("최소 1개의 주문 항목이 필요합니다.");
    }
    this._orderItems.splice(index, 1);
  }

  // 배송 정보 업데이트
  updateDelivery(info: DeliveryInfo): void {
    if (this._deliveryInfo) {
      throw new Error("이미 배송 정보가 등록되어 있습니다.");
    }
    this._deliveryInfo = info;
    this.recordEvent(new DeliveryInfoUpdatedEvent(this._id, info));
  }

  // 총 금액 계산 (불변 연산)
  calculateTotal(): Money {
    const total = this._orderItems.reduce(
      (sum, item) => sum + item.getAmount(),
      0
    );
    return new Money(total, "KRW");
  }

  // 방어적 복사: 내부 컬렉션을 보호하며 반환
  getOrderItems(): ReadonlyArray<OrderItem> {
    return Object.freeze([...this._orderItems]);
  }

  // ID 접근자
  get id(): string {
    return this._id;
  }

  // 버전 접근자 (Optimistic Locking용)
  get version(): number {
    return this._version;
  }

  // 도메인 이벤트 기록
  private recordedEvents: DomainEvent[] = [];
  protected recordEvent(event: DomainEvent): void {
    this.recordedEvents.push(event);
  }
  pullEvents(): DomainEvent[] {
    const events = [...this.recordedEvents];
    this.recordedEvents = [];
    return events;
  }
}

/**
 * 주문 항목 (애그리게이트 내부 엔티티)
 * ID로 식별되며, 상태를 가질 수 있음
 */
class OrderItem {
  private readonly _id: string;
  private readonly _productId: string;
  private _quantity: number;
  private readonly _unitPrice: number;

  constructor(productId: string, quantity: number, unitPrice: number = 0) {
    this._id = crypto.randomUUID();
    this._productId = productId;
    this._quantity = quantity;
    this._unitPrice = unitPrice;
  }

  increaseQuantity(amount: number): void {
    this._quantity += amount;
  }

  getAmount(): number {
    return this._quantity * this._unitPrice;
  }

  // ID로 동등성 비교
  equals(other: OrderItem): boolean {
    return this._id === other._id;
  }

  get id(): string { return this._id; }
  get productId(): string { return this._productId; }
  get quantity(): number { return this._quantity; }
}

/**
 * 배송 정보 (밸류 오브젝트)
 * ID 없이 값 자체로 식별, 불변(Immutable)
 */
class DeliveryInfo {
  readonly address: string;
  readonly receiver: string;
  readonly phone: string;

  constructor(address: string, receiver: string, phone: string) {
    this.address = address;
    this.receiver = receiver;
    this.phone = phone;
    Object.freeze(this);  // 불변 보장
  }

  // 값으로 동등성 비교
  equals(other: DeliveryInfo): boolean {
    return this.address === other.address &&
           this.receiver === other.receiver &&
           this.phone === other.phone;
  }
}

/**
 * 돈 (밸류 오브젝트)
 */
class Money {
  constructor(
    readonly amount: number,
    readonly currency: string
  ) {
    Object.freeze(this);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error("통화 단위가 다릅니다.");
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}

// ============ 레포지토리 인터페이스 ============

interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: string): Promise<Order | null>;
}

// ============ 애플리케이션 서비스 (트랜잭션 경계) ============

class OrderService {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly eventPublisher: EventPublisher
  ) {}

  @Transactional  // 트랜잭션 경계
  async addOrderItem(orderId: string, productId: string, quantity: number): Promise<void> {
    // 1. 애그리게이트 조회
    const order = await this.orderRepository.findById(orderId);
    if (!order) {
      throw new OrderNotFoundException(orderId);
    }

    // 2. 비즈니스 로직 수행 (루트 통해)
    order.addItem(productId, quantity);

    // 3. 영속화
    await this.orderRepository.save(order);

    // 4. 도메인 이벤트 발행 (트랜잭션 후)
    const events = order.pullEvents();
    for (const event of events) {
      await this.eventPublisher.publish(event);
    }
  }
}
```

### 📢 섹션 요약 비유

왕국에서 **왕(루트)**이 모든 국민(엔티티)을 대표하여 외국과 조약을 맺는 것과 같습니다. 외국은 왕을 통해서만 교류해야 하며, 국민 개개인에게 직접 접근하는 것은 **내정 간섭**으로 간주됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: 트랜잭션 관리 패턴

| 패턴 | 범위 | 일관성 보장 | 성능 | 복잡도 | 사용 사례 |
|:---|:---|:---|:---|:---|:---|
| **Single Aggregate TX** | 1개 애그리게이트 | Strong ACID | 높음 | 낮음 | 단일 트랜잭션 (예: 주문 생성) |
| **2PC (Two-Phase Commit)** | 여러 애그리게이트 | Strong ACID | 낮음 (Locking) | 높음 | 분산 트랜잭션 (예: 재고+결제) |
| **Saga (Choreography)** | 여러 애그리게이트 | Eventual Consistency | 높음 | 중간 | 비동기 이벤트 (예: 배송 시작) |
| **Saga (Orchestration)** | 여러 애그리게이트 | Eventual Consistency | 중간 | 높음 | 중앙 관제 (예: 여행 예약) |

### 과목 융합 관점

**1) 데이터베이스 관점 (트랜잭션 격리 수준)**

애그리게이트 루트는 **데이터베이스 트랜잭션의 자연스러운 경계**가 됩니다.

```sql
-- 단일 애그리게이트 내부에서만 ACID 보장
BEGIN TRANSACTION;

-- 1. 주문 루트 조회 (SELECT FOR UPDATE)
SELECT * FROM orders WHERE id = ? FOR UPDATE;

-- 2. 주문 항목 추가 (INSERT)
INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?);

-- 3. 주문 총액 업데이트 (UPDATE)
UPDATE orders SET total_amount = ?, version = version + 1 WHERE id = ?;

COMMIT;  -- 또는 ROLLBACK;
```

- **낙관적 락(Optimistic Lock)**: version 필드를 활용하여 마지막 커밋이 승리
- **비관적 락(Pessimistic Lock)**: SELECT FOR UPDATE로 명시적 락

**2) 분산 시스템 관점 (CAP 정리)**

애그리게이트 경계는 **분산 트랜잭션의 단위**가 됩니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    Saga 패턴 예시                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Order Aggregate: 주문 생성                              │
│     └─> OrderCreated 이벤트 발행                            │
│                                                             │
│  2. Inventory Aggregate: 재고 예약 (보상: 취소)             │
│     └─> StockReserved 이벤트 발행                           │
│                                                             │
│  3. Payment Aggregate: 결제 승인 (보상: 환불)              │
│     └─> PaymentApproved 이벤트 발행                         │
│                                                             │
│  [장애 시 보상 트랜잭션]                                    │
│  Payment 실패 → Refund(보상) → ReleaseStock(보상)           │
└─────────────────────────────────────────────────────────────┘
```

**결과적 일관성(Eventual Consistency)**: 각 애그리게이트는 로컬 트랜잭션으로 일관성을 보장하지만, 전체 시스템은 최종적으로 일치해야 합니다.

### 📢 섹션 요약 비유

연결된 **화차 열차**와 같습니다. 각 화차(애그리게이트)는 독립적으로 제동(트랜잭션)할 수 있지만, 전체 열차(시스템)가 안전하게 운행되려면 기관차(오케스트레이터)가 모든 화차의 상태를 조율해야 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 이커머스 주문/결제 애그리게이트 설계**

```
┌─────────────────────────────────────────────────────────────┐
│                 애그리게이트 분리 설계                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │  Order Aggregate │      │Payment Aggregate │            │
│  │  (주문)           │      │  (결제)           │            │
│  │  ┌────────────┐  │      │  ┌────────────┐  │            │
│  │  │Order (Root)│  │      │  │Payment(Root)│  │            │
│  │  │- orderItems│  │      │  │- txId      │  │            │
│  │  │- delivery  │  │      │  │- amount    │  │            │
│  │  └────────────┘  │      │  └────────────┘  │            │
│  │                  │      │                  │            │
│  │  [트랜잭션 경계]  │      │  [트랜잭션 경계]  │            │
│  │  단일 DB 트랜잭션 │      │  단일 DB 트랜잭션 │            │
│  └──────────────────┘      └──────────────────┘            │
│                                                             │
│  [상호작용]                                                 │
│  Order 생성 → Payment 생성 (비동기 이벤트)                  │
│  Payment 실패 → Order 취소 (보상)                           │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **애그리게이트 경계 식별**: 주문과 결제는 서로 다른 라이프사이클을 가짐 → 분리
2. **루트 간 통신 방식**: 동기(RPC) vs 비동기(이벤트) → 비동기 선택 (확장성)
3. **보상 트랜잭션 정의**: 결제 실패 시 주문 자동 취소 로직 구현

**Scenario 2: SNS 댓글 시스템**

```
┌─────────────────────────────────────────────────────────────┐
│                    애그리게이트 크기 결정                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [안티패턴] 너무 큰 애그리게이트                             │
│  ┌──────────────────────────────────────────────┐          │
│  │      Post Aggregate (너무 큼!)                │          │
│  │  - Post (루트)                               │          │
│  │  - Comments (수천 개)                        │          │
│  │  - Likes (수만 개)                           │          │
│  └──────────────────────────────────────────────┘          │
│  → 로딩 시간 증가, 동시성 충돌 빈발                          │
│                                                             │
│  [올바른 패턴] 애그리게이트 분리                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Post Aggregate│  │Comment       │  │Like Aggregate│     │
│  │              │  │Aggregate     │  │              │     │
│  │- 게시물 내용   │  │- 댓글 내용    │  │- 좋아요 정보  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  → 각각 독립적으로 로딩, 캐싱 가능                          │
└─────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **애그리게이트 식별** | 도메인 전문가와 함께 경계 식별 완료 | |
| **루트 지정** | 각 애그리게이트의 루트 명확히 지정 | |
| **인버리언트 정의** | 각 애그리게이트의 불변 조건 문서화 | |
| **접근 제어** | 루트 외부에서 내부 객체 직접 접근 방지 | |
| **동시성 제어** | Optimistic Locking 적용 (version 필드) | |
| **이벤트 발행** | 상태 변경 시 도메인 이벤트 발행 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **트랜잭션 격리** | 단일 애그리게이트 내에서만 트랜잭션 보장 | |
| **데이터 격리** | 애그리거트별 별도 테이블/스키마 | |
| **감사 로그** | 루트별 상태 변경 이력 기록 | |
| **롤백 정책** | Saga 보상 트랜잭션 정의 완료 | |

### 안티패턴

**❌ 거대한 애그리게이트 (God Aggregate)**

```typescript
// 안티패턴: 너무 많은 책임을 가진 루트
class Order {
  // 수천 개의 주문 항목
  private items: OrderItem[];

  // 수만 개의 변경 이력
  private history: OrderHistory[];

  // 관련된 모든 데이터를 포함 (안티패턴!)
  private customer: Customer;      // 다른 애그리게이트
  private products: Product[];     // 다른 애그리게이트
  private inventory: Stock[];      // 다른 애그리게이트

  // 성능 문제: 로딩 시간 10초+, 메모리 사용량 GB
}
```

**개선 방안**:

```typescript
// 올바른 패턴: 애그리게이트 분리
class Order {
  private items: OrderItem[];  // 최소한의 항목만 (예: 최근 10개)
  private customerRef: string;  // ID 참조만 유지
}

// 별도의 애그리게이트로 분리
class Customer { /* ... */ }
class Product { /* ... */ }
class Stock { /* ... */ }
```

### 📢 섹션 요약 비유

마치 **도서관의 분류 시스템**과 같습니다. 책(애그리게이트)은 서가별로 분류되어 있고, 사서(루트)를 통해서만 대여 가능합니다. 모든 책을 한 곳에 모아두면(거대 애그리게이트), 찾기도 힘들고 관리도 불가능합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **동시성 충돌** | 5회/일 (무분별한 Lock) | 0.1회/일 (Optimistic Lock) | **98% 감소** |
| **데이터 일관성** | 95% (부분 무결성) | 99.99% (애그리게이트 경계) | **+5% 향상** |
| **로딩 시간** | 5초 (N+1 Query) | 0.5초 (필요한 것만) | **90% 단축** |
| **버그 발생率** | 10건/월 (불일치) | 1건/월 (경계 보호) | **90% 감소** |
| **코드 가독성** | 복잡한 참조 관계 | 명확한 경계 | **개발 효율 30% 향상** |

### 미래 전망

1. **애그리게이트 자동 식별**: AI 기반 코드 분석으로 애그리게이트 후보 추천
2. **크래시 컨시스턴시(CRDT)**: 분산 애그리거트 간 충돌 없는 병합
3. **서버리스 애그리게이트**: FaaS 환경에서의 애그리게이트 자동 스케일링

### 참고 표준

- **Domain-Driven Design** (Eric Evans, 2003) - Chapter 6: Domain Life Cycle
- **Implementing Domain-Driven Design** (Vaughn Vernon, 2013) - Part 2: Strategic Design
- **Patterns of Distributed Systems** (Microsoft) - Aggregate Pattern
- **Spring Data documentation** - Aggregate Root support

### 📢 섹션 요약 비유

스마트폰의 **앱 샌드박스**와 같습니다. 각 앱(애그리게이트)은 독립된 공간에서 실행되며, 시스템(루트)을 통해서만 서로 통신할 수 있습니다. 이로 인해 하나의 앱이 고장 나도 다른 앱에 영향을 주지 않습니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[도메인 주도 설계 (DDD)](./613_ddd_basics.md)**: DDD 전술적 패턴 전체 개요
- **[바운디드 컨텍스트](./614_bounded_context_microservices.md)**: 애그리거트보다 상위 개념
- **[Entity와 Value Object](./613_ddd_basics.md)**: 애그리거트 내부 구성 요소
- **[Saga 패턴](./619_saga_pattern.md)**: 애그리거트 간 분산 트랜잭션
- **[Optimistic Locking](./618_optimistic_locking.md)**: 동시성 제어 메커니즘

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: 여러 장의 장난감 카드를 묶어서 한 묶음(애그리게이트)으로 만들고, 그 묶음을 관리하는 책임자(루트)를 정해두는 것입니다.

**2) 원리**: 친구들과 카드를 거래할 때 카드 묶음의 책임자를 통해서만 교환하고, 개별 카드를 함부로 빼내지 않도록 규칙을 정하는 것입니다. 이렇게 하면 카드가 잃어버리거나 바뀌는 것을 방지할 수 있습니다.

**3) 효과**: 각 카드 묶음이 독립적으로 관리되어서, 한 묶음에 문제가 생겨도 다른 묶음은 안전하게 보호되고, 여러 친구가 동시에 카드를 사용해도 충돌이 일어나지 않습니다.
