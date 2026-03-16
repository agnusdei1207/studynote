+++
title = "613. 도메인 주도 설계 (DDD) 기본 구성"
date = "2026-03-15"
[extra]
categories = "studynote-se"
keywords = ["DDD", "Domain-Driven Design", "엔티티", "값 객체", "리포지토리"]
tags = ["SE", "Architecture", "Domain Model", "Microservices"]
+++

# 도메인 주도 설계 (DDD) 기본 구성

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **복잡한 비즈니스 도메인의 지식을 소프트웨어 모델로 정제**하여 기술적 구현과 비즈니스 요구사항의 간극을 해소하는 설계 패러다임
> 2. **가치**: 도메인 전문가와 개발자의 **공통 언어(Ubiquitous Language)**로 커뮤니케이션 오류 70% 감소, 마이크로서비스 경계 설정의 핵심 가이드
> 3. **융합**: 클린 아키텍처, 헥사고날 아키텍처, 이벤트 소싱, CQRS와 직접적 연관

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**도메인 주도 설계 (Domain-Driven Design, DDD)**는 Eric Evans가 2003년 저서에서 정립한 소프트웨어 개발 방법론으로, **복잡한 비메니니셜 요구사항을 가진 소프트웨어**를 개발할 때 비즈니스 도메인의 본질적인 복잡성을 기술적 구현에 투영하는 접근법입니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DDD의 핵심 철학                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [전통적 접근: 기술 중심]                                                 │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                                                                 │      │
│   │   비즈니스 요구사항              기술적 구현                      │      │
│   │        │                              │                           │      │
│   │        ▼                              ▼                           │      │
│   │   "주문을 관리하고 싶어"     ┌──────────────────────┐          │      │
│   │                         │    Table: orders     │          │      │
│   │                         │    - id (INT)        │          │      │
│   │                         │    - customer_id     │          │      │
│   │                         │    - total (DECIMAL) │          │      │
│   │                         │    - created_at      │          │      │
│   │                         └──────────────────────┘          │      │
│   │                                                                 │      │
│   │   문제: 비즈니스 개념과 데이터 모델 간 괴리                         │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [DDD 접근: 도메인 중심]                                                 │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                                                                 │      │
│   │   비즈니스 도메인 ←→ 유비쿼터스 언어 → 소프트웨어 모델                │      │
│   │        │                              │                           │      │
│   │        ▼                              ▼                           │      │
│   │   "주문은 고객이 생성하며,   ┌──────────────────────┐          │      │
│   │    배송지 정보를 포함하고,  │  class Order {       │          │      │
│   │    결제 완료 후에만        │    customer: Customer│          │      │
│   │    배송될 수 있다"         │    items: OrderItem[]│          │      │
│   │                         │    status: OrderStatus│          │      │
│   │                         │    shipTo: Address   │          │      │
│   │                         │                         │          │      │
│   │                         │    canBeShipped(): boolean {      │          │
│   │                         │      return this.status.isPaid()│   │      │
│   │                         │    }                    │          │      │
│   │                         │  }                    │          │      │
│   │                         └──────────────────────┘          │      │
│   │                                                                 │      │
│   │   장점: 비즈니스 언어가 코드에 직접 반영                              │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

DDD는 **지도 제작(Map Making)**과 같습니다:

1. **도메인 전문가**는 실제 지형(비즈니스 현장)을 알고 있습니다
2. **개발자**는 지도 제작 기술(코딩)을 가지고 있습니다
3. **유비쿼터스 언어**는 두 사람이 함께 만드는 **축척된 기호법**

지도와 실제 지형이 일치할 때 길을 잃지 않습니다. DDD에서는 소프트웨어 모델과 비즈니스 도메인이 일치할 때 올바른 소프트웨어를 만들 수 있습니다.

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DDD 등장 배경 및 필요성                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [문제: 소프트웨어 개발의 본질적 복잡성]                                   │
│                                                                             │
│   1. 기술적 복잡성 (Essential Complexity)                                   │
│      ┌──────────────────────────────────────────────────────────┐        │
│      │  • 분산 시스템, 동시성, 데이터 무결성                            │        │
│      │  → 해결 가능: 패턴, 프레임워크, 도구                               │        │
│      └──────────────────────────────────────────────────────────┘        │
│                                                                             │
│   2. 본질적 복잡성 (Accidental Complexity)                                 │
│      ┌──────────────────────────────────────────────────────────┐        │
│      │  • 비즈니스 규칙, 프로세스, 용어, 관계                            │        │
│      │  → 해결 어려움: 도메인 전문가와 개발자 간 간극                    │        │
│      └──────────────────────────────────────────────────────────┘        │
│                                                                             │
│   [DDD의 접근: 본질적 복잡성 정면 돌파]                                   │
│                                                                             │
│   Strategy Pattern (전략적 패턴)                                          │
│   ┌──────────────────────────────────────────────────────────────────┐    │
│   │  Bounded Context (바운디드 컨텍스트)                               │    │
│   │  • 특정 하위 도메인을 모델링하는 경계                              │    │
│   │  • 각 컨텍스트 내에서 모델의 일관성 유지                            │    │
│   │                                                                 │    │
│   │  Ubiquitous Language (유비쿼터스 언어)                             │    │
│   │  • 도메인 전문가와 개발자가 공유하는 언어                          │    │
│   │  • 코드, 문서, 대화에서 동일한 용어 사용                           │    │
│   │                                                                 │    │
│   │  Context Mapping (컨텍스트 맵핑)                                   │    │
│   │  • 바운디드 컨텍스트 간 관계 정의                                 │    │
│   │                                                                 │    │
│   └──────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   Tactical Patterns (전술적 패턴)                                          │
│   ┌──────────────────────────────────────────────────────────────────┐    │
│   │  Entity, Value Object, Aggregate                                   │    │
│   │  Repository, Domain Service, Domain Event                         │    │
│   │  Factory                                                         │    │
│   └──────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

DDD는 **의학 용어의 표준화** 과정과 같습니다. 의사(도메인 전문가)는 환자 증상을 설명하고, 약사(개발자)는 처방전을 작성합니다. 공통된 의학 용어(유비쿼터스 언어)가 없으면 처방이 잘못될 수 있습니다. DDD는 이 공통 언어를 구축하여 "혈압 140/90"과 같은 정밀한 용어가 코드, 문서, 대화에서 동일하게 사용되도록 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 전술적 패턴 (Tactical Patterns)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   DDD 전술적 패턴 상세 구조                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                      VALUE OBJECT (값 객체)                       │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 식별자가 없고 속성 값으로 동일성 판단                    │  │      │
│   │  │ • 불변성 (Immutable)                                      │  │      │
│   │  │ • 교체 가능 (Substitutable)                                │  │      │
│   │  │                                                           │  │      │
│   │  │ 예시: Money, Address, Email, DateRange, Color             │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                       ENTITY (엔티티)                           │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 식별자(ID)로 동일성 판단                                 │  │      │
│   │  │ • 연속성 있는 생명주기                                       │  │      │
│   │  │ • 속성은 변할 수 있으나 ID는 불변                            │  │      │
│   │  │                                                           │  │      │
│   │  │ 예시: User, Order, Product, Customer                       │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    AGGREGATE (애그리거트)                         │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 일관성 경계(Consistency Boundary)                         │  │      │
│   │  │ • 하나의 루트 엔티티(Aggregate Root)를 통해서만 접근        │  │      │
│   │  │ • 트랜잭션 경계                                               │  │      │
│   │  │                                                           │  │      │
│   │  │  Order Aggregate:                                           │  │      │
│   │  │    ┌─────────────────────────────────────────────┐          │  │      │
│   │  │    │ Order (Root)                                        │          │  │      │
│   │  │    │  ├─ OrderItem[]                                     │          │  │      │
│   │  │    │  └─ DeliveryInfo                                    │          │  │      │
│   │  │    └─────────────────────────────────────────────┘          │  │      │
│   │  │                                                           │  │      │
│   │  │  규칙:                                                       │  │      │
│   │  │  • 외부에서 OrderItem 직접 수정 금지                         │  │      │
│   │  │  • Order을 통해서만 모든 조작                               │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                  REPOSITORY (리포지토리)                        │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 애그리거트 저장소 인터페이스                               │  │      │
│   │  │ • 도메인 영역에서 인프라를 감춤                              │  │      │
│   │  │ • 컬렉션처럼 사용                                           │  │      │
│   │  │                                                           │  │      │
│   │  │ interface IOrderRepository {                               │  │      │
│   │  │   save(order: Order): Promise<void>;                      │  │      │
│   │  │   findById(id: string): Promise<Order | null>;            │  │      │
│   │  │   findByCustomer(customerId: string): Promise<Order[]>;   │  │      │
│   │  │ }                                                          │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │              DOMAIN SERVICE (도메인 서비스)                       │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 특정 엔티티에 속하지 않는 비즈니스 로직                  │  │      │
│   │  │ • 무상태 (Stateless)                                       │  │      │
│   │  │                                                           │  │      │
│   │  │ 예시:                                                     │  │      │
│   │  │  • ExchangeRateService - 환율 계산                        │  │      │
│   │  │  • DiscountCalculator - 할인 계산                           │  │      │
│   │  │  • PaymentProcessor - 결제 처리                             │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │               DOMAIN EVENT (도메인 이벤트)                        │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 도메인 내에서 발생한 중요한 사건                           │  │      │
│   │  │ • 과거 시제 (Past Tense) 명명                               │  │      │
│   │  │                                                           │  │      │
│   │  │ 예시: OrderCreated, PaymentCompleted, OrderCancelled      │  │      │
│   │  │                                                           │  │      │
│   │  │ class OrderPlaced {                                        │  │      │
│   │  │   orderId: string;                                         │  │      │
│   │  │   customerId: string;                                      │  │      │
│   │  │   totalAmount: Money;                                      │  │      │
│   │  │   occurredAt: Date;                                        │  │      │
│   │  │ }                                                          │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                  FACTORY (팩토리)                               │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │ • 복잡한 객체 생성 로직 캡슐화                               │  │      │
│   │  │ • 애그리거트 생성 책임                                       │  │      │
│   │  │                                                           │  │      │
│   │  │ class OrderFactory {                                       │  │      │
│   │  │   createOrder(                                             │  │      │
│   │  │     customer: Customer,                                     │  │      │
│   │  │     items: OrderItem[]                                     │  │      │
│   │  │   ): Order {                                               │  │      │
│   │  │     const order = new Order(...);                          │  │      │
│   │  │     // 초기화 로직                                           │  │      │
│   │  │     order.applyDiscount(...);                               │  │      │
│   │  │     return order;                                           │  │      │
│   │  │   }                                                        │  │      │
│   │  │ }                                                          │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드 구현

```typescript
// ==================== VALUE OBJECTS (값 객체) ====================

/**
 * Money: 불변 값 객체
 * 특징:
 * - 식별자 없음, 속성 값으로 동일성 판단
 * - 불변성 (Immutable)
 * - 자가 검증 (Self-validation)
 */
export class Money {
    private readonly _amount: number;
    private readonly _currency: string;

    constructor(amount: number, currency: string) {
        if (amount < 0) {
            throw new Error('Amount cannot be negative');
        }
        if (!currency || currency.length !== 3) {
            throw new Error('Invalid currency code');
        }

        this._amount = amount;
        this._currency = currency;
    }

    get amount(): number { return this._amount; }
    get currency(): string { return this._currency; }

    // 값 객체는 새로운 인스턴스를 반환
    add(other: Money): Money {
        if (other._currency !== this._currency) {
            throw new Error('Cannot add different currencies');
        }
        return new Money(this._amount + other._amount, this._currency);
    }

    multiply(factor: number): Money {
        if (factor < 0) {
            throw new Error('Factor cannot be negative');
        }
        return new Money(this._amount * factor, this._currency);
    }

    // 동일성은 값으로 판단
    equals(other: Money): boolean {
        return this._amount === other._amount &&
               this._currency === other._currency;
    }

    format(locale: string = 'ko-KR'): string {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: this._currency
        }).format(this._amount);
    }
}

/**
 * Email: 값 객체
 * 이메일 형식 검증 로직 캡슐화
 */
export class Email {
    private readonly _value: string;

    constructor(value: string) {
        if (!this.isValidEmail(value)) {
            throw new Error('Invalid email format');
        }
        this._value = value.toLowerCase(); // 정규화
    }

    get value(): string { return this._value; }

    private isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    equals(other: Email): boolean {
        return this._value === other._value;
    }
}

/**
 * Address: 값 객체
 * 복합 값 객체 예시
 */
export class Address {
    constructor(
        public readonly street: string,
        public readonly city: string,
        public readonly zipCode: string,
        public readonly country: string
    ) {
        this.validate();
    }

    private validate(): void {
        if (!this.street || this.street.length < 5) {
            throw new Error('Invalid street address');
        }
        if (!this.city || this.city.length < 2) {
            throw new Error('Invalid city');
        }
        if (!/^\d{5}$/.test(this.zipCode)) {
            throw new Error('Invalid zip code format');
        }
    }

    equals(other: Address): boolean {
        return this.street === other.street &&
               this.city === other.city &&
               this.zipCode === other.zipCode &&
               this.country === other.country;
    }
}

// ==================== ENTITIES (엔티티) ====================

/**
 * Customer: 엔티티
 * 특징:
 * - ID로 식별
 * - 생명주기 가짐
 * - 속성은 변하지만 ID는 불변
 */
export class Customer {
    private readonly _id: string;
    private _name: string;
    private _email: Email;
    private readonly _createdAt: Date;
    private _status: CustomerStatus;

    constructor(props: CustomerProps) {
        this._id = props.id;
        this._name = props.name;
        this._email = new Email(props.email);
        this._createdAt = new Date();
        this._status = CustomerStatus.ACTIVE;
        this.validate();
    }

    // 엔티티는 ID로 동일성 판단
    equals(other: Customer): boolean {
        return this._id === other._id;
    }

    get id(): string { return this._id; }
    get name(): string { return this._name; }
    get email(): Email { return this._email; }
    get status(): CustomerStatus { return this._status; }

    // 상태 변경 메서드 (비즈니스 로직 포함)
    updateName(name: string): void {
        if (name.length < 2) {
            throw new Error('Name too short');
        }
        this._name = name;
    }

    updateEmail(email: string): void {
        this._email = new Email(email);
    }

    deactivate(): void {
        if (this.hasActiveOrders()) {
            throw new Error('Cannot deactivate customer with active orders');
        }
        this._status = CustomerStatus.INACTIVE;
    }

    private hasActiveOrders(): boolean {
        // 도메인 서비스 호출 또는 리포지토리 조회
        return false; // 간소화
    }

    private validate(): void {
        if (!this._id || this._id.length === 0) {
            throw new Error('Customer ID is required');
        }
    }
}

enum CustomerStatus {
    ACTIVE = 'ACTIVE',
    INACTIVE = 'INACTIVE',
    SUSPENDED = 'SUSPENDED'
}

// ==================== AGGREGATES (애그리거트) ====================

/**
 * OrderItem: 값 객체 (애그리거트의 일부)
 */
export class OrderItem {
    constructor(
        public readonly productId: string,
        public readonly price: Money,
        public readonly quantity: number
    ) {
        if (quantity <= 0) {
            throw new Error('Quantity must be positive');
        }
    }

    get total(): Money {
        return this.price.multiply(this.quantity);
    }
}

/**
 * DeliveryInfo: 값 객체 (애그리거트의 일부)
 */
export class DeliveryInfo {
    constructor(
        public readonly address: Address,
        public readonly recipientName: string,
        public readonly recipientPhone: string,
        public readonly requestedAt?: Date
    ) {}

    withScheduledDate(date: Date): DeliveryInfo {
        return new DeliveryInfo(
            this.address,
            this.recipientName,
            this.recipientPhone,
            date
        );
    }
}

/**
 * Order: 애그리거트 루트 (Aggregate Root)
 * 특징:
 * - 일관성 경계
 * - 외부에서 내부 객체 직접 접근 금지
 * - 모든 상태 변경은 루트를 통해서만
 */
export class Order {
    // 애그리거트 내부 상태
    private readonly _id: string;
    private readonly _customerId: string;
    private _items: OrderItem[];  // 내부 컬렉션 캡슐화
    private _status: OrderStatus;
    private readonly _createdAt: Date;
    private _deliveryInfo?: DeliveryInfo;
    private readonly _events: DomainEvent[] = [];  // 도메인 이벤트

    constructor(props: OrderProps) {
        this._id = props.id;
        this._customerId = props.customerId;
        this._items = props.items;
        this._status = OrderStatus.PENDING;
        this._createdAt = new Date();

        this.validate();
        this.recordEvent(new OrderCreated(this._id, this._customerId));
    }

    // 애그리거트 루트에만 공개된 메서드
    get id(): string { return this._id; }
    get customerId(): string { return this._customerId; }
    get status(): OrderStatus { return this._status; }

    // 불변식으로 외부에 노출
    get items(): ReadonlyArray<OrderItem> {
        return Object.freeze([...this._items]);
    }

    // 비즈니스 로직: 총액 계산
    calculateTotal(): Money {
        return this._items.reduce(
            (sum, item) => sum.add(item.total),
            new Money(0, 'KRW')
        );
    }

    // 비즈니스 로직: 아이템 추가 (일관성 유지)
    addItem(item: OrderItem): void {
        if (!this.canBeModified()) {
            throw new Error('Cannot modify order in current status');
        }

        const existingItemIndex = this._items.findIndex(
            i => i.productId === item.productId
        );

        if (existingItemIndex >= 0) {
            // 기존 아이템 수량 업데이트
            const existingItem = this._items[existingItemIndex];
            this._items[existingItemIndex] = new OrderItem(
                existingItem.productId,
                existingItem.price,
                existingItem.quantity + item.quantity
            );
        } else {
            this._items.push(item);
        }
    }

    // 비즈니스 로직: 배송 정보 설정
    setDeliveryInfo(info: DeliveryInfo): void {
        if (this._status !== OrderStatus.PENDING) {
            throw new Error('Cannot set delivery for non-pending order');
        }
        this._deliveryInfo = info;
    }

    // 비즈니스 로직: 주문 확정
    confirm(): void {
        if (this._status !== OrderStatus.PENDING) {
            throw new Error('Order already confirmed');
        }
        if (!this._deliveryInfo) {
            throw new Error('Delivery info required');
        }
        if (this._items.length === 0) {
            throw new Error('Order must have at least one item');
        }

        this._status = OrderStatus.CONFIRMED;
        this.recordEvent(new OrderConfirmed(this._id));
    }

    // 비즈니스 로직: 결제 완료
    markAsPaid(): void {
        if (this._status !== OrderStatus.CONFIRMED) {
            throw new Error('Only confirmed orders can be marked as paid');
        }

        this._status = OrderStatus.PAID;
        this.recordEvent(new OrderPaid(this._id, this.calculateTotal()));
    }

    // 비즈니스 로직: 배송 시작
    startShipping(): void {
        if (this._status !== OrderStatus.PAID) {
            throw new Error('Only paid orders can be shipped');
        }

        this._status = OrderStatus.SHIPPED;
        this.recordEvent(new OrderShipped(this._id, this._deliveryInfo!.address));
    }

    // 도메인 이벤트 수집
    pullDomainEvents(): DomainEvent[] {
        const events = [...this._events];
        this._events.length = 0;  // 이벤트 비우기
        return events;
    }

    private recordEvent(event: DomainEvent): void {
        this._events.push(event);
    }

    private canBeModified(): boolean {
        return this._status === OrderStatus.PENDING;
    }

    private validate(): void {
        if (!this._id || this._id.length === 0) {
            throw new Error('Order ID is required');
        }
        if (!this._customerId || this._customerId.length === 0) {
            throw new Error('Customer ID is required');
        }
        if (!this._items || this._items.length === 0) {
            throw new Error('Order must have at least one item');
        }
    }
}

enum OrderStatus {
    PENDING = 'PENDING',
    CONFIRMED = 'CONFIRMED',
    PAID = 'PAID',
    SHIPPED = 'SHIPPED',
    DELIVERED = 'DELIVERED',
    CANCELLED = 'CANCELLED'
}

// ==================== DOMAIN EVENTS (도메인 이벤트) ====================

/**
 * 도메인 이벤트 기반 인터페이스
 */
interface DomainEvent {
    occurredAt: Date;
}

class OrderCreated implements DomainEvent {
    occurredAt = new Date();

    constructor(
        public readonly orderId: string,
        public readonly customerId: string
    ) {}
}

class OrderConfirmed implements DomainEvent {
    occurredAt = new Date();

    constructor(
        public readonly orderId: string
    ) {}
}

class OrderPaid implements DomainEvent {
    occurredAt = new Date();

    constructor(
        public readonly orderId: string,
        public readonly amount: Money
    ) {}
}

class OrderShipped implements DomainEvent {
    occurredAt = new Date();

    constructor(
        public readonly orderId: string,
        public readonly shippingAddress: Address
    ) {}
}

// ==================== REPOSITORIES (리포지토리) ====================

/**
 * OrderRepository 인터페이스
 * 도메인 영역에 속하며, 인프라 구현을 감춤
 */
export interface IOrderRepository {
    save(order: Order): Promise<void>;
    findById(id: string): Promise<Order | null>;
    findByCustomer(customerId: string): Promise<Order[]>;
    nextId(): string;
}

/**
 * CustomerRepository 인터페이스
 */
export interface ICustomerRepository {
    save(customer: Customer): Promise<void>;
    findById(id: string): Promise<Customer | null>;
    findByEmail(email: string): Promise<Customer | null>;
}

// ==================== DOMAIN SERVICES (도메인 서비스) ====================

/**
 * DiscountCalculator: 도메인 서비스
 * 특정 엔티티에 속하지 않는 복잡한 비즈니스 로직
 */
export class DiscountCalculator {
    /**
     * 할인 계산 로직
     * @param order 주문
     * @param customer 고객 (할인 등급 확인용)
     * @param currentDate 현재 날짜 (시즌 할인 확인용)
     */
    calculate(
        order: Order,
        customer: Customer,
        currentDate: Date
    ): Money {
        let totalDiscount = new Money(0, 'KRW');

        // 고객 등급에 따른 할인
        const customerDiscount = this.calculateCustomerDiscount(customer);
        totalDiscount = totalDiscount.add(customerDiscount);

        // 시즌 할인
        const seasonalDiscount = this.calculateSeasonalDiscount(order, currentDate);
        totalDiscount = totalDiscount.add(seasonalDiscount);

        // 대량 주문 할인
        const bulkDiscount = this.calculateBulkDiscount(order);
        totalDiscount = totalDiscount.add(bulkDiscount);

        return totalDiscount;
    }

    private calculateCustomerDiscount(customer: Customer): Money {
        // VIP 고객 10% 할인 등
        return new Money(0, 'KRW');
    }

    private calculateSeasonalDiscount(order: Order, date: Date): Money {
        // 크리스마스 시즌 5% 할인 등
        return new Money(0, 'KRW');
    }

    private calculateBulkDiscount(order: Order): Money {
        // 10개 이상 주문 시 5% 할인 등
        if (order.items.length >= 10) {
            return order.calculateTotal().multiply(0.05);
        }
        return new Money(0, 'KRW');
    }
}

/**
 * ExchangeRateService: 도메인 서비스
 * 외부 시스템이지만 도메인 로직에 필수적
 */
export interface IExchangeRateService {
    getRate(from: string, to: string, date: Date): Promise<number>;
}

export class ExchangeRateService implements IExchangeRateService {
    async getRate(from: string, to: string, date: Date): Promise<number> {
        // 실제로는 외부 환율 API 호출
        if (from === to) return 1.0;
        if (from === 'USD' && to === 'KRW') return 1350.00;
        if (from === 'KRW' && to === 'USD') return 0.00074;
        throw new Error('Exchange rate not available');
    }
}

// ==================== FACTORIES (팩토리) ====================

/**
 * OrderFactory: 복잡한 객체 생성 캡슐화
 */
export class OrderFactory {
    constructor(
        private readonly customerRepo: ICustomerRepository,
        private readonly discountCalculator: DiscountCalculator
    ) {}

    async createOrder(request: CreateOrderRequest): Promise<Order> {
        // 1. 고객 조회
        const customer = await this.customerRepo.findById(request.customerId);
        if (!customer) {
            throw new Error('Customer not found');
        }

        // 2. 주문 아이템 생성
        const items = request.items.map(item =>
            new OrderItem(item.productId, item.price, item.quantity)
        );

        // 3. 주문 생성
        const order = new Order({
            id: this.generateOrderId(),
            customerId: customer.id,
            items
        });

        // 4. 초기 할인 적용
        const discount = await this.discountCalculator.calculate(
            order,
            customer,
            new Date()
        );

        // 할인이 적용된 새로운 Order 반환 (불변성 유지)
        return order;  // 실제로는 할인 정보를 별도 저장
    }

    private generateOrderId(): string {
        return `ORD_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
}
```

### 애그리거트 패턴 실전

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 애그리거트 패턴 일관성 경계 및 규칙                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [애그리거트 경계 규칙]                                                     │
│                                                                             │
│   1. 트랜잭션 경계                                                        │
│      ┌────────────────────────────────────────────────────────────┐        │
│      │  한 트랜잭션에서 하나의 애그리거트만 수정                      │        │
│      │  → 일관성 보장                                                   │        │
│      └────────────────────────────────────────────────────────────┘        │
│                                                                             │
│   2. 외부 참조 제어                                                        │
│      ┌────────────────────────────────────────────────────────────┐        │
│      │  다른 애그리거트는 ID로만 참조                                 │        │
│      │  Order → Order.customerId (string)                           │        │
│      │  NOT Order → Order.customer (Customer object)                │        │
│      └────────────────────────────────────────────────────────────┘        │
│                                                                             │
│   3. 최종 일관성 (Eventually Consistent)                                  │
│      ┌────────────────────────────────────────────────────────────┐        │
│      │  애그리거트 간 일관성은 도메인 이벤트로 조정                   │        │
│      │  OrderConfirmed → Inventory.reserveItems()                   │        │
│      └────────────────────────────────────────────────────────────┘        │
│                                                                             │
│   [잘못된 예: 애그리거트 경계 위반]                                          │
│                                                                             │
│   class Order {                                                           │
│     // 다른 애그리거트를 직접 참조하면 안 됨!                             │
│     customer: Customer;  // ✗                                           │
│                                                                             │
│     // 이 방식은 OK                                                      │
│     customerId: string;  // ✓                                            │
│   }                                                                       │
│                                                                             │
│   [외부에서의 애그리거트 조작 규칙]                                           │
│                                                                             │
│   ✗ 잘못됨:                                                              │
│   const order = await repo.findById(id);                                  │
│   order.items.push(newItem);  // 직접 내부 컬렉션 수정               │
│   await repo.save(order);                                               │
│                                                                             │
│   ✓ 올바름:                                                              │
│   const order = await repo.findById(id);                                  │
│   order.addItem(newItem);  // public 메서드를 통한 수정                  │
│   await repo.save(order);                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

DDD의 전술적 패턴은 **주방 체계처럼** 작동합니다. **값 객체**는 재료(소금, 계란)로 특정한 양과 품질을 가집니다. **엔티티**는 요리사로 각자의 고유 ID(사번)를 가지고 경력을 쌓습니다. **애그리케이트**는 특정 주방(파스타 담당)으로 조리 장비와 재료를 통제합니다. **리포지토리**는 창고로 재료를 보관하고, **도메인 서비스**는 특수 조리 기술(베이킹, 튀김)을 담당합니다. 이 모든 것이 **유비쿼터스 언어**(공통 조리 용어)로 소통됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 도메인 모델링 접근법 비교

| 특성 | DDD | Anemic Domain Model | Active Record |
|:---|:---|:---|:---|
| **도메인 로직 위치** | 엔티티/값 객체 | 서비스 계층 | 모델 자체 |
| **모델 풍부함** | 풍부한 도메인 모델 | 빈약한 도메인 모델 | DB 중심 |
| **테스트 용이성** | 높음 | 중간 | 낮음 |
| **복잡도** | 높음 | 낮음 | 중간 |
| **DB 독립성** | 완전 독립 | 부분 독립 | 강한 종속 |
| **학습 곡선** | 가파름 | 낮음 | 중간 |
| **적용 분야** | 복잡한 비즈니스 | 단순 CRUD | 단순 앱 |

### 아키텍처와의 조화

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              DDD와 클린/헥사고날 아키텍처 완벽 조화                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Architecture Layers                           │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Interface Adapters                           │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Controllers                                              │  │      │
│   │  │  Presenters                                               │  │      │
│   │  │  Repositories (Implementation)                             │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Application Layer                            │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Use Cases                                                │  │      │
│   │  │  Application Services                                     │  │      │
│   │  │  (여러 DDD 패턴 조합 및 오케스트레이션)                       │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Domain Layer (DDD Patterns)                   │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Entities (엔티티)                                         │  │      │
│   │  │  Value Objects (값 객체)                                  │  │      │
│   │  │  Aggregates (애그리거트)                                   │  │      │
│   │  │  Domain Services (도메인 서비스)                           │  │      │
│   │  │  Domain Events (도메인 이벤트)                             │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [DDD 패턴과 아키텍처 계층의 매핑]                                     │
│                                                                             │
│   DDD Pattern                    Architecture Layer                     │
│   ──────────────────────────────────────────────────────────────        │
│   Entity, Value Object        →    Domain Layer (Core)                  │
│   Aggregate Root             →    Domain Layer + Application Layer       │
│   Repository (Interface)      →    Domain Layer (Port)                 │
│   Repository (Implementation) →    Interface Adapter Layer            │
│   Domain Service             →    Domain or Application Layer           │
│   Factory                    →    Application Layer                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점

**1. 마이크로서비스와의 결합**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               DDD 바운디드 컨텍스트 = 마이크로서비스 경계                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   전사 도메인                                                                 │
│   │                          ┌──────────────────────┐                        │
│   │                          │                      │                        │
│   │         ┌─────────┬─────┼─────┬─────┬───────┤                        │
│   │         │         │     │     │         │                        │
│   │         ▼         ▼     ▼     ▼         ▼                        │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                     │
│   │  │  Order  │ │Customer│ │ Product │ │Inventory│                     │
│   │  │ Context │ │ Context │ │ Context │ │ Context │                     │
│   │  │         │ │         │ │         │ │         │                     │
│   │  │ 주문    │ │ 고객    │ │ 상품    │ │ 재고    │                     │
│   │  │ 관리    │ │ 관리    │ │ 관리    │ │ 관리    │                     │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘                     │
│   │      │           │           │           │                        │
│   │      │           │           │           │                        │
│   │      └───────────┴───────────┴───────────┘                        │
│   │                     ▼                                            │
│   │              Event Bus (Kafka)                                   │
│   │                                                                         │
│   │  각 컨텍스트 = 독립적 마이크로서비스                                   │
│   └──────────────────────────────────────────────────────────────┘        │
│                                                                             │
│   [바운디드 컨텍스트 식별 기준]                                            │
│   ┌──────────────────────────────────────────────────────────────┐       │
│   │  1. 하위 도메인 (Subdomain)별 분리                            │       │
│   │  2. 용어(Ubiquitous Language)의 차이                           │       │
│   │  3. 데이터 일관성 경계                                            │       │
│   │  4. 팀 조직 구조와 정렬(Conway's Law)                           │       │
│   │  5. 독립적 배포 가능성                                            │       │
│   └──────────────────────────────────────────────────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**2. 이벤트 소싱(Event Sourcing)과의 연계**

| DDD 개념 | 이벤트 소싱 적용 |
|:---|:---|
| **애그리거트** | 상태 대신 이벤트 스트림 저장 |
| **도메인 이벤트** | 상태 변경의 원천이 됨 |
| **리포지토리** | Event Store 구현 |
| **팩토리** | 이벤트 재생성을 통한 객체 복원 |

**3. CQRS와의 결합**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   DDD + CQRS 완벽 조합 패턴                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [Command Side (쓰기) - DDD 패턴 활용]                                   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Command Handler                                                  │      │
│   │       │                                                          │      │
│   │       ▼                                                          │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │     │
│   │  │  Aggregate Root (명령 실행)                                │  │     │
│   │  │   • 상태 변경                                               │  │     │
│   │  │   • 도메인 이벤트 발생                                     │  │     │
│   │  └──────────────────────────────────────────────────────────┘  │     │
│   │       │                                                          │      │
│   │       ▼                                                          │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │     │
│   │  │  Event Store (이벤트 저장)                                │  │     │
│   │  │   • OrderCreated                                          │  │     │
│   │  │   • OrderConfirmed                                        │  │     │
│   │  │   • OrderPaid                                             │  │     │
│   │  └──────────────────────────────────────────────────────────┘  │     │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [Query Side (읽기) - 독립적 모델]                                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Query Handler                                                    │      │
│   │       │                                                          │      │
│   │       ▼                                                          │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │     │
│   │  │  Read Model (최적화된 뷰 모델)                           │  │     │
│   │  │   • OrderSummaryView                                       │  │     │
│   │  │   • CustomerOrderHistoryView                               │  │     │
│   │  │   • OrderStatusView                                        │  │     │
│   │  └──────────────────────────────────────────────────────────┘  │     │
│   │       │                                                          │      │
│   │       ▼                                                          │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │     │
│   │  │  Read Database (전용 쿼리 DB)                            │  │     │
│   │  │   • NoSQL (MongoDB, DynamoDB)                             │  │     │
│   │  │   • Elasticsearch                                         │  │     │
│   │  │   • Read-optimized RDBMS schema                            │  │     │
│   │  └──────────────────────────────────────────────────────────┘  │     │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [이벤트 기반 동기화]                                                     │
│                                                                             │
│   Event Store ──▶ Event Projector ──▶ Read Model Update                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

DDD는 **여행 가이드북 작성**과 같습니다. **전략적 패턴**은 지역별 가이드북(바운디드 컨텍스트)을 구분하고, **전술적 패턴**은 각 지역의 상세 지도(엔티티, 값 객체)를 그립니다. **유비쿼터스 언어**는 현지인과 여행자가 모두 이해하는 공통 기호입니다. 이 모든 것이 어우러져 비즈니스라는 복잡한 지형을 소프트웨어라는 지도로 완벽하게 투영합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오: 전자상거래 주문 관리 시스템 DDD 적용**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                전자상거래 주문 컨텍스트 DDD 설계                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [하위 도메인 식별]                                                        │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Core (핵심): Order Management                                   │      │
│   │  • 주문 생성, 상태 변경, 배송 관리                                │      │
│   │  • 직접적인 수익 창출                                             │      │
│   │                                                                 │      │
│   │  Supporting (지원): Inventory, Product Catalog                  │      │
│   │  • 재고 관리, 상품 정보                                          │      │
│   │                                                                 │      │
│   │  Generic (일반): Customer Management                             │      │
│   │  • 회원가입, 프로필 관리                                        │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [Order Bounded Context - 유비쿼터스 언어]                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  용어 정의                                                        │      │
│   │  • Order (주문): 고객이 생성한 상품 구매 요청                      │      │
│   │  • OrderItem (주문 항목): 주문에 포함된 개별 상품                  │      │
│   │  • OrderStatus (주문 상태): PENDING, CONFIRMED, PAID, SHIPPED  │      │
│   │  • DeliveryInfo (배송 정보): 수령인, 주소, 배송 희망일           │      │
│   │  • OrderItemVO (주문 항목 뷰 모델): 뷰용 최적화된 값 객체          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [애그리게이트 경계 설계]                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Order Aggregate (일관성 경계)                                  │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │     │
│   │  │  Order (Root)                                             │  │     │
│   │  │    ├─ OrderItem[]                                         │  │     │
│   │  │    ├─ DeliveryInfo                                        │  │     │
│   │  │    └─ Payment (값 객체)                                   │  │     │
│   │  │                                                           │  │     │
│   │  │  인베리언트:                                                │  │     │
│   │  │  • OrderItem 수량은 0 이상                                  │  │     │
│   │  │  • PAID 상태에서만 SHIPPED로 변경 가능                       │  │     │
│   │  │  • 배송 정보는 CONFIRMED 이전에 설정                        │  │     │
│   │  └──────────────────────────────────────────────────────────┘  │     │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [도메인 이벤트 기반 컨텍스트 통합]                                     │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Order Context                                  Inventory Context│      │
│   │       │                                                     │      │
│   │       │ OrderConfirmed                                    │      │
│   │       ├─────────────────────────────────────────────────▶     │      │
│   │       │                                             Event Bus   │      │
│   │                                                             │      │
│   │  Inventory Context                                       │      │
│   │       │ handle(OrderConfirmed) {                           │      │
│   │       │   reserveItems(order.items);                         │      │
│   │       │ }                                                     │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [성과 지표]                                                               │
│   • 비즈니스 용어와 코드 간 간극 해소                                   │
│   • 도메인 전문가와 개발자 간 커뮤니케이션 효율 80% 향상             │
│   • 새로운 기능 추가 시 도메인 로직 수정 시간 50% 단축                 │
│   • 단위 테스트 커버리지 95% 달성                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**기술적 평가**

| 항목 | 질문 | 가이드라인 |
|:---|:---|:---|
| **도메인 복잡도** | 비즈니스 로직이 복잡한가? | 단순 CRUD에는 과도함 |
| **전문가 존재** | 도메인 전문가가 있는가? | 없으면 지식 추출 어려움 |
| **규칙 변경** | 비즈니스 규칙이 자주 변하는가? | 높으면 DDD 적합 |
| **팀 규모** | 5인 이상 개발팀? | 작은 팀에는 과도함 |
| **장기 프로젝트** | 6개월 이상 프로젝트? | 단기에는 투자 회수 어려움 |

**운영·보안적 고려사항**

| 항목 | 확인사항 | 가이드라인 |
|:---|:---|:---|
| **감사 추적** | 상태 변경 기록 필요? | 도메인 이벤트로 자동 감사 |
| **규정 준수** | 금융/의료 규정 대응? | 도메인 로직에 규정 캡슐화 |
| **데이터 보안** | 민감 정보 처리? | 값 객체로 보안 로직 캡슐화 |

### 안티패턴

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DDD 안티패턴                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 1: "Anemic Domain Model (빈약한 도메인 모델)"                     │
│                                                                             │
│      class Order {                                                         │
│        id: string;                                                         │
│        customerId: string;                                                 │
│        items: OrderItem[];                                                 │
│        status: string;                                                     │
│        // 비즈니스 로직 없음!                                             │
│      }                                                                     │
│                                                                             │
│      class OrderService {  // 모든 로직이 서비스로!                        │
│        calculateTotal(order: Order) { ... }                               │
│        confirmOrder(order: Order) { ... }                                  │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 도메인 모델이 데이터 그릇에 불과                                    │
│   • 객체지향의 장점 상실                                                │
│   • 절차적 발견 불가능                                                  │
│                                                                             │
│   ✅ 해결: 풍부한 도메인 모델                                              │
│                                                                             │
│      class Order {                                                         │
│        confirm() {                                                        │
│          if (!this.canBeConfirmed()) {                                     │
│            throw new Error('Cannot confirm');                             │
│          }                                                                │
│          this.status = OrderStatus.CONFIRMED;                             │
│        }                                                                  │
│        private canBeConfirmed(): boolean { ... }                          │
│      }                                                                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 2: "거대한 애그리거트 (God Aggregate)"                          │
│                                                                             │
│      // 모든 것을 하나의 애그리거트에!                                     │
│      class ECommerceAggregate {                                          │
│        order: Order;                                                      │
│        customer: Customer;                                                │
│        inventory: Inventory;                                              │
│        payment: Payment;                                                  │
│        shipping: Shipping;                                                │
│        // ... 100개 이상의 엔티티                                       │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 일관성 경계가 너무 넓어 성능 저하                                  │
│   • 동시성 문제 증가                                                    │
│   • 팀 협업 어려움                                                    │
│                                                                             │
│   ✅ 해결: 바운디드 컨텍스트별 애그리거트 분리                         │
│                                                                             │
│      Order Aggregate, Customer Aggregate, Inventory Aggregate               │
│      이벤트 기반 최종 일관성                                              │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 3: "기술적 관점을 모델링"                                     │
│                                                                             │
│      // DB 스키마를 그대로 모델링!                                        │
│      class Order {                                                         │
│        order_id: string;      // DB 컬럼명 그대로!                       │
│        customer_id: string;                                               │
│        created_at: Date;                                                   │
│        updated_at: Date;                                                   │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 비즈니스 언어가 아닌 기술 용어                                      │
│   • 유비쿼터스 언어 불가능                                              │
│   • DB 변경 시 모델 영향                                                 │
│                                                                             │
│   ✅ 해결: 비즈니스 언어로 모델링                                       │
│                                                                             │
│      class Order {                                                         │
│        id: string;           // 도메인 용어                            │
│        customerId: string;                                               │
│        createdAt: Date;                                                   │
│      }                                                                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 4: "무분별한 값 객체 사용"                                      │
│                                                                             │
│      // 모든 것을 값 객체로!                                              │
│      class Order {                                                         │
│        orderId: OrderId;     // 원시 타입조차 값 객체로!                │
│        status: OrderStatus;  // enum인데 값 객체로!                     │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 과도한 복잡도                                                       │
│   • 성능 저하                                                           │
│   • 실제 이득 없음                                                       │
│                                                                             │
│   ✅ 해결: 값 객체 사용 기준                                              │
│                                                                             │
│      값 객체 적용 기준:                                                   │
│      • 복합 속성 (Address, Money)                                       │
│      • 자가 검증 필요 (Email, PhoneNumber)                               │
│      • 불변성 중요                                                       │
│      • 도메인 의미 있음                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

DDD 도입은 **프로 야구장 설립**과 같습니다. 잘못된 접근은 그냥 야구장(데이터베이스)에 그물망(코드)을 치는 것입니다. 올바른 접근은 포지션 별로 전략(전략적 패턴)을 세우고, 각 포지션의 역할과 신호 체계(전술적 패턴)를 정의하며, 공통된 전술 용어(유비쿼터스 언어)로 팀 간 소통을 원활하게 하는 것입니다. 이로써 복잡한 게임(비즈니스)을 체계적으로 운영할 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 항목 | 전통적 접근 | DDD | 개선율 |
|:---|:---|:---|:---|
| **비즈니스-기술 간극** | 높음 | 거의 없음 | 90% ↓ |
| **도메인 로직 재사용** | 어려움 | 용이 | 80% ↑ |
| **규칙 변경 시간** | 2-4주 | 3-5일 | 80% ↓ |
| **전문가-개발자 소통** | 오류 잦음 | 원활 | 70% ↑ |
| **코드 이해도** | 3-6달 | 1-2주 | 60% ↓ |
| **마이크로서비스 분리** | 모호함 | 명확한 경계 | 명확함 |

### 정성적 기대효과

1. **지식 공유**: 유비쿼터스 언어로 조직 내 암묵지 지식 형성
2. **기술적 민첩성**: 도메인 중심 설계로 기술 교체 영향 최소화
3. **팀 자율성**: 바운디드 컨텍스트별 독립적 개발/배포
4. **장기 진화 가능성**: 복잡한 비즈니스 로직의 체계적 발전 지원

### 미래 전망

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DDD 미래 진화 방향                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   2025-2027: AI 기반 도메인 모델링                                         │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ LLM이 도메인 전문가와의 인터뷰에서 유비쿼터스 언어 추출      │      │
│   │ • "고객"이라는 용어의 의미 맵핑                                 │      │
│   │ • 비즈니스 규칙 자동 도출                                         │      │
│   │ • 초기 엔티티/값 객체 스캐폴딩                                   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   2027-2029: No-Code/Low-Code DDD                                       │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ 비개발자도 도메인 모델링 가능                                    │      │
│   │ • 시각적 모델링 도구                                             │      │
│   │ • 드래그앤드롭 애그리거트 설계                                    │      │
│   │ • 실시간 협업 모델링                                             │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   2029-2030: Living Documentation                                       │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ 코드와 문서의 실시간 동기화                                     │      │
│   │ • 코드에서 자동 생성되는 도메인 용어집                          │      │
│   │ • 변경 시 자동 업데이트되는 컨텍스트 맵                       │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 참고 표준

| 분야 | 표준/규격 | 설명 |
|:---|:---|:---|
| **UML** | UML 2.x | 클래스 다이어그램, 상태 다이어그램 |
| **사양** | IEEE 830 | 소프트웨어 요구사항 명세서 |
| **프로세스** | Scrum/Kanban | 애자일 개발 프로세스 |

### 📢 섹션 요약 비유

DDD는 **복잡한 법률 체계**를 정리하는 것과 같습니다. **전략적 패턴**은 민법, 형법, 행정법 같은 법 전체를 나누고, **전술적 패턴**은 각 법의 조항과 용어를 정의합니다. **유비쿼터스 언어**는 법률 전문가와 시민 모두가 이해하는 공통된 용어입니다. 이 체계가 갖춰지면 복잡한 사회 활동(비즈니스)을 원활하게 수행할 수 있습니다. 소프트웨어도 마찬가지입니다.

---

## 📌 관련 개념 맵

### 연관 개념 5개+

1. **[클린 아키텍처](./611_clean_architecture.md)**: DDD 패턴의 계층별 배치

2. **[헥사고날 아키텍처](./612_hexagonal_architecture.md)**: 포트와 어댑터를 통한 DDD 격리

3. **[바운디드 컨텍스트](./614_bounded_context.md)**: DDD 전략적 패턴 핵심

4. **[애그리게이트 루트](./615_aggregate_root.md)**: 일관성 경계 실전

5. **[이벤트 소싱](./620_event_sourcing.md)**: DDD와 결합한 상태 관리

---

## 👶 어린이를 위한 3줄 비유 설명

**1. 무엇인가요?**
DDD는 **복잡한 사업을 컴퓨터에 그대로 옮겨오는 방법**입니다. 음식점 사장님(도메인 전문가)이 "주문", "배송", "결제"라는 용어를 쓰면, 개발자도 똑같은 용어를 코드에 사용하여 서로 이해하는 것입니다.

**2. 어떻게 작동하나요?**
**값 객체**는 "1000원", "서울시 강남구"처럼 그 자체로 의미가 있는 데이터입니다. **엔티티**는 "고객 김철수(ID: 123)"처럼 식별자로 구분되고 시간이 지나도 변하는 것입니다. **애그리거트**는 "주문"이라는 관련된 것들을 한 묶음으로 묶어서 한 번에 관리합니다.

**3. 왜 필요한가요?**
이렇게 하면 **비즈니스 언어**와 **프로그래밍 언어**가 같아집니다. 사업 규칙이 바뀌면 도메인 전문가와 개발자가 같은 용어로 이야기하므로 빠르게 대응할 수 있습니다. 복잡한 비즈니스를 실수 없이 소프트웨어로 만들 수 있습니다.
