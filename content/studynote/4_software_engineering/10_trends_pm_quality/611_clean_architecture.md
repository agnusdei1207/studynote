+++
title = "611. 클린 아키텍처 (Clean Architecture)"
date = "2026-03-15"
[extra]
categories = "studynote-se"
keywords = ["클린 아키텍처", "Clean Architecture", "의존성 역전", "헥사고날"]
tags = ["SE", "Architecture", "Dependency Inversion", "DDD"]
+++

# 클린 아키텍처 (Clean Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비즈니스 도메인 로직을 **외부 의존성으로부터 완전히 격리**하여 테스트 용이성과 유지보수성을 극대화하는 소프트웨어 아키텍처
> 2. **가치**: 도메인 로직 테스트 커버리지 95% 달성, 프레임워크 교체 비용 90% 절감, 팀 확장 용이
> 3. **융합**: DDD(도메인 주도 설계), SOLID 원칙, 헥사고날 아키텍처와 직접적 연관

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**클린 아키텍처 (Clean Architecture)**는 Robert C. Martin (Uncle Bob)이 제창한 소프트웨어 아키텍처로, **의존성 역전 원칙 (Dependency Inversion Principle)**을 핵심으로 하여 비즈니스 로직을 기술적 구현 세부사항으로부터 분리합니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    클린 아키텍처 핵심 철학                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                 1. 의존성 규칙 (Dependency Rule)                │      │
│   │                                                                 │      │
│   │                 소스 코드 의존성은 오직 안쪽으로만 향해야 한다    │      │
│   │                                                                 │      │
│   │         ◀───────────────────────────────────────────────────    │      │
│   │    외부    │    │    │    │         내부                       │      │
│   │             ▼    ▼    ▼    ▼                                    │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                 2. 관심사 분리 (Separation of Concerns)         │      │
│   │                                                                 │      │
│   │                 각 계층은 단일한 책임을 가지며 독립적으로       │      │
│   │                 진화할 수 있어야 한다                           │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                 3. 인터페이스 분리 (Interface Segregation)     │      │
│   │                                                                 │      │
│   │                 외부 계층은 내부 계층의 인터페이스(추상화)에    │      │
│   │                만 의존하고, 구현 세부사항은 알지 못한다        │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

클린 아키텍처는 **양파 껍질 구조**와 같습니다:

1. **핵심 (도메인)**: 양파의 가장 안쪽 - 비즈니스 로직, 순수한 가치
2. **유스케이스**: 도메인을 조합하여 비즈니스 흐름 구현
3. **인터페이스 어댑터**: 외부와의 통신을 위한 변환 계층
4. **프레임워크 & 드라이버**: 가장 바깥쪽 - UI, DB, 외부 API

껍질을 제거해도 핵심은 변하지 않습니다. UI를 바꾸거나 DB를 교체해도 비즈니스 로직은 영향받지 않습니다.

### 역사적 배경

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  클린 아키텍처 등장 배경 및 진화                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1990s                     2000s                       2010s-present        │
│   ───────────────────────────────────────────────────────────────────────   │
│                                                                             │
│   Layered Architecture    Onion Architecture        Clean Architecture    │
│   (계층형 아키텍처)        (Jeffrey Palermo)         (Uncle Bob)           │
│   ┌────────────────┐      ┌────────────────┐        ┌────────────────┐     │
│   │ Presentation   │      │   UI Layer     │        │  Frameworks    │     │
│   │    Layer       │      └────────────────┘        │  & Drivers     │     │
│   └────────────────┘              ▲                └────────────────┘     │
│            │                       │                         ▲             │
│   ┌────────────────┐              │                ┌────┴────────────┐     │
│   │  Business      │              │                │ Interface Adapters│  │
│   │    Logic       │              │                └───────────────────┘  │
│   └────────────────┘              │                         ▲             │
│            │                       │                ┌────┴────────────┐     │
│   ┌────────────────┐              │                │   Use Cases      │     │
│   │     Data       │              │                └───────────────────┘  │
│   │   Access       │              │                         ▲             │
│   └────────────────┘              │                ┌────┴────────────┐     │
│            ▼                       │                │   Entities       │     │
│   Database                         │                └───────────────────┘     │
│                                                                             │
│   문제점: 하위 계층 의존    해결: 의존성 역전           완성: 명확한 경계   │
│   → 테스트 어려움          → 인터페이스 기반 격리          + 계층 정의    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

클린 아키텍처는 **수술실의 무균 구역**과 같습니다. 가장 안쪽(도메인)은 완전히 무균 상태로 외부 오염(기술적 의존성)이 없습니다. 바깥쪽으로 갈수록 보호 장비(인터페이스 어댑터)를 착용하지만, 핵심 수술(비즈니스 로직)은 순수하게 유지됩니다. 의료진(개발자)은 각 영역의 엄격한 경계 규칙을 준수해야 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 계층별 상세 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    클린 아키텍처 4계층 상세 구조                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    ① Entities (엔티티)                         │      │
│   │  ┌──────────────────────────────────────────────────────────┐   │      │
│   │  │ • 핵심 비즈니스 규칙 encapsulation                        │   │      │
│   │  │ • 전사적 가장 높은 수준의 개념                             │   │      │
│   │  │ • 외부 변경에 영향받지 않음                                 │   │      │
│   │  │ • 예: User, Order, PaymentTransaction                      │   │      │
│   │  │                                                             │   │      │
│   │  │ class Order {                                              │   │      │
│   │  │   calculateTotal(): Money                                  │   │      │
│   │  │   applyDiscount(code: string): void                        │   │      │
│   │  │   validateDelivery(): boolean                              │   │      │
│   │  │ }                                                         │   │      │
│   │  └──────────────────────────────────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                               ▲ 의존성 방향                                 │
│                               │                                            │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                  ② Use Cases (유스케이스)                      │      │
│   │  ┌──────────────────────────────────────────────────────────┐   │      │
│   │  │ • 애플리케이션 특정 비즈니스 규칙                          │   │      │
│   │  │ • 엔티티를 조합하여 흐름 orchestration                      │   │      │
│   │  │ • 입력/출력 포트(인터페이스)에만 의존                       │   │      │
│   │  │ • 예: CreateOrder, ProcessPayment, SendConfirmation       │   │      │
│   │  │                                                             │   │      │
│   │  │ class CreateOrderUseCase {                                 │   │      │
│   │  │   constructor(                                             │   │      │
│   │  │     private orderRepo: IOrderRepository,                   │   │      │
│   │  │     private userRepo: IUserRepository,                     │   │      │
│   │  │     private paymentGateway: IPaymentGateway                │   │      │
│   │  │   ) {}                                                     │   │      │
│   │  │                                                             │   │      │
│   │  │   async execute(request: CreateOrderRequest)               │   │      │
│   │  │     : Promise<CreateOrderResponse> {                       │   │      │
│   │  │     // 1. 사용자 조회                                       │   │      │
│   │  │     const user = await this.userRepo.findById(request.userId)│   │   │
│   │  │     // 2. 주문 생성 (엔티티)                                │   │      │
│   │  │     const order = Order.create(user, request.items)         │   │      │
│   │  │     // 3. 결제 처리                                         │   │      │
│   │  │     await this.paymentGateway.charge(order.total)           │   │      │
│   │  │     // 4. 저장                                             │   │      │
│   │  │     await this.orderRepo.save(order)                       │   │      │
│   │  │     return { orderId: order.id }                           │   │      │
│   │  │   }                                                       │   │      │
│   │  │ }                                                         │   │      │
│   │  └──────────────────────────────────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                               ▲ 의존성 방향                                 │
│                               │                                            │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │            ③ Interface Adapters (인터페이스 어댑터)            │      │
│   │  ┌──────────────────────────────────────────────────────────┐   │      │
│   │  │ • 데이터를 외부/내부 포맷으로 변환                          │   │      │
│   │  │ • 유스케이스/엔티티를 외부가 사용할 수 있게 만듦             │   │      │
│   │  │                                                             │   │      │
│   │  │ [Controllers] - 요청을 유스케이스로 변환                     │   │      │
│   │  │ class OrderController {                                    │   │      │
│   │  │   async createOrder(req: Request) {                        │   │      │
│   │  │     const useCase = new CreateOrderUseCase(...)             │   │      │
│   │  │     const response = await useCase.execute(req.body)        │   │      │
│   │  │     return res.json(response)                              │   │      │
│   │  │   }                                                       │   │      │
│   │  │ }                                                         │   │      │
│   │  │                                                             │   │      │
│   │  │ [Presenters] - 응답을 UI 포맷으로 변환                      │   │      │
│   │  │ [Gateways] - 외부 서비스와의 통신                           │   │      │
│   │  │ [Repositories] - DB 구현                                    │   │      │
│   │  └──────────────────────────────────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                               ▲ 의존성 방향                                 │
│                               │                                            │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │              ④ Frameworks & Drivers (프레임워크와 드라이버)    │      │
│   │  ┌──────────────────────────────────────────────────────────┐   │      │
│   │  │ • 가장 바깥쪽 계층                                        │   │      │
│   │  │ • UI, Web Framework, DB, External API                     │   │      │
│   │  │ • 도구의 세부사항                                           │   │      │
│   │  │                                                             │   │      │
│   │  │ 예: Express.js, Sequelize, React, Jest, Axios             │   │      │
│   │  └──────────────────────────────────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [핵심 원칙: 의존성은 항상 안쪽으로만 향함]                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 의존성 역전 원칙 (DIP) 실제 구현

```typescript
// ==================== Domain Layer (가장 안쪽) ====================

// 엔티티: 프레임워크에 완전히 독립적
export class Order {
    private readonly _id: string;
    private readonly _userId: string;
    private readonly _items: OrderItem[];
    private _status: OrderStatus;
    private readonly _createdAt: Date;

    constructor(props: OrderProps) {
        this._id = props.id;
        this._userId = props.userId;
        this._items = props.items;
        this._status = OrderStatus.PENDING;
        this._createdAt = new Date();
        this.validate();
    }

    get id(): string { return this._id; }
    get items(): OrderItem[] { return [...this._items]; }
    get status(): OrderStatus { return this._status; }

    // 비즈니스 로직: 총액 계산
    calculateTotal(): Money {
        const total = this._items.reduce((sum, item) =>
            sum + item.price * item.quantity, 0
        );
        return new Money(total, 'KRW');
    }

    // 비즈니스 로직: 할인 적용
    applyDiscount(discountCode: string, discountPercentage: number): void {
        if (this._status !== OrderStatus.PENDING) {
            throw new Error('Cannot discount processed order');
        }
        if (discountPercentage < 0 || discountPercentage > 100) {
            throw new Error('Invalid discount percentage');
        }
        // 할인 로직 구현
    }

    // 비즈니스 로직: 배송 가능 여부 확인
    canBeShipped(): boolean {
        return this._status === OrderStatus.PAID &&
               this._items.length > 0;
    }

    private validate(): void {
        if (this._items.length === 0) {
            throw new Error('Order must have at least one item');
        }
        if (!this._userId) {
            throw new Error('Order must have a user');
        }
    }
}

// 값 객체 (Value Object): 불변식으로 도메인 모델 풍부
export class Money {
    constructor(
        private readonly _amount: number,
        private readonly _currency: string
    ) {
        if (_amount < 0) throw new Error('Amount cannot be negative');
        if (!_currency) throw new Error('Currency is required');
    }

    get amount(): number { return this._amount; }
    get currency(): string { return this._currency; }

    add(other: Money): Money {
        if (other._currency !== this._currency) {
            throw new Error('Cannot add different currencies');
        }
        return new Money(this._amount + other._amount, this._currency);
    }

    multiply(factor: number): Money {
        if (factor < 0) throw new Error('Factor cannot be negative');
        return new Money(this._amount * factor, this._currency);
    }

    format(): string {
        return `${this._currency} ${this._amount.toLocaleString()}`;
    }
}

// ==================== Application Layer ====================

// 포트 (Port): 인터페이스 - 내부 계층이 정의
export interface IOrderRepository {
    save(order: Order): Promise<void>;
    findById(id: string): Promise<Order | null>;
    findByUserId(userId: string): Promise<Order[]>;
}

export interface IPaymentGateway {
    charge(amount: Money, method: PaymentMethod): Promise<PaymentResult>;
    refund(transactionId: string): Promise<void>;
}

export interface INotificationService {
    sendOrderConfirmation(orderId: string, userId: string): Promise<void>;
}

// 유스케이스: 애플리케이션 특정 비즈니스 로직
export class CreateOrderUseCase implements IUseCase<CreateOrderRequest, CreateOrderResponse> {
    constructor(
        private readonly orderRepo: IOrderRepository,
        private readonly productRepo: IProductRepository,
        private readonly paymentGateway: IPaymentGateway,
        private readonly notificationService: INotificationService
    ) {}

    async execute(request: CreateOrderRequest): Promise<CreateOrderResponse> {
        // 1. 입력 검증
        this.validateRequest(request);

        // 2. 제품 확인 및 재고 확인
        const productIds = request.items.map(i => i.productId);
        const products = await this.productRepo.findByIds(productIds);

        if (products.length !== productIds.length) {
            throw new Error('Some products not found');
        }

        // 3. 주문 생성 (도메인 엔티티)
        const orderItems = request.items.map(item => {
            const product = products.find(p => p.id === item.productId)!;
            return new OrderItem(
                product.id,
                product.price,
                item.quantity
            );
        });

        const order = new Order({
            id: generateId(),
            userId: request.userId,
            items: orderItems
        });

        // 4. 결제 처리
        const paymentResult = await this.paymentGateway.charge(
            order.calculateTotal(),
            request.paymentMethod
        );

        if (!paymentResult.success) {
            throw new Error('Payment failed');
        }

        // 5. 주문 저장
        await this.orderRepo.save(order);

        // 6. 알림 발송
        await this.notificationService.sendOrderConfirmation(
            order.id,
            order.userId
        );

        return {
            orderId: order.id,
            status: order.status,
            total: order.calculateTotal().format()
        };
    }

    private validateRequest(request: CreateOrderRequest): void {
        if (!request.userId) throw new Error('User ID required');
        if (!request.items || request.items.length === 0) {
            throw new Error('Items required');
        }
    }
}

// ==================== Interface Adapter Layer ====================

// 컨트롤러: HTTP 요청을 유스케이스로 변환
export class OrderController {
    private readonly createOrderUseCase: CreateOrderUseCase;

    constructor(createOrderUseCase: CreateOrderUseCase) {
        this.createOrderUseCase = createOrderUseCase;
    }

    async createOrder(req: Request, res: Response): Promise<void> {
        try {
            // HTTP Request → Use Case Request 변환
            const request: CreateOrderRequest = {
                userId: req.body.userId,
                items: req.body.items,
                paymentMethod: req.body.paymentMethod
            };

            // 유스케이스 실행
            const response = await this.createOrderUseCase.execute(request);

            // Use Case Response → HTTP Response 변환
            res.status(201).json({
                success: true,
                data: response
            });
        } catch (error) {
            res.status(400).json({
                success: false,
                error: error.message
            });
        }
    }
}

// 리포지토리 구현: DB persistence
export class SequelizeOrderRepository implements IOrderRepository {
    private readonly orderModel: OrderModel;

    constructor(orderModel: OrderModel) {
        this.orderModel = orderModel;
    }

    async save(order: Order): Promise<void> {
        // Order 엔티티 → Sequelize Model 변환
        await this.orderModel.create({
            id: order.id,
            userId: order.userId,
            items: JSON.stringify(order.items),
            status: order.status,
            createdAt: order.createdAt
        });
    }

    async findById(id: string): Promise<Order | null> {
        const record = await this.orderModel.findByPk(id);
        if (!record) return null;

        // Sequelize Model → Order 엔티티 변환
        return new Order({
            id: record.id,
            userId: record.userId,
            items: JSON.parse(record.items),
            status: record.status,
            createdAt: record.createdAt
        });
    }
}

// ==================== Framework & Driver Layer ====================

// Express.js 라우팅 (프레임워크)
import express from 'express';

export function createOrderRouter(
    orderController: OrderController
): express.Router {
    const router = express.Router();

    router.post('/orders',
        validateRequest,
        async (req, res) => {
            await orderController.createOrder(req, res);
        }
    );

    return router;
}

// 의존성 주입 컨테이너 설정
export function setupDependencies() {
    // Infrastructure implementations
    const dbOrderRepo = new SequelizeOrderRepository(OrderModel);
    const dbProductRepo = new SequelizeProductRepository(ProductModel);
    const stripePayment = new StripePaymentGateway(stipeClient);
    const emailNotification = new EmailNotificationService(emailClient);

    // Use cases
    const createOrderUseCase = new CreateOrderUseCase(
        dbOrderRepo,
        dbProductRepo,
        stripePayment,
        emailNotification
    );

    // Controllers
    const orderController = new OrderController(createOrderUseCase);

    // Router
    return createOrderRouter(orderController);
}
```

### 경계(Boundary) 간 데이터 교환

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   경계를 넘나드는 데이터 변환                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [요청 흐름: Controller → Use Case → Entity]                               │
│                                                                             │
│   HTTP Request               UseCase Request              Entity            │
│   ┌─────────────────┐      ┌─────────────────┐      ┌──────────────┐     │
│   │ {               │      │ {               │      │ Order        │     │
│   │   "userId":    │  ──▶ │   userId:      │  ──▶ │  • id:       │     │
│   │     "123",     │      │     string,    │      │    string    │     │
│   │   "items":     │      │   items:       │      │  • items[]   │     │
│   │     [{         │      │     OrderItem[],│      │  • status    │     │
│   │       "pid":   │      │   paymentMethod │      │  • method    │     │
│   │       "A1",    │      │ }              │      │ }            │     │
│   │       "qty":   │      │                 │      │              │     │
│   │        2       │      │                 │      │              │     │
│   │     }]         │      │                 │      │              │     │
│   │ }              │      │                 │      │              │     │
│   └─────────────────┘      └─────────────────┘      └──────────────┘     │
│        │                        │                        │               │
│        ▼                        ▼                        ▼               │
│   [Controller]             [UseCase]               [Entity]            │
│   • 파싱                   • 검증                   • 불변성          │
│   • 매핑                   • 비즈니스 로직          • 도메인 규칙     │
│                                                                             │
│   [응답 흐름: Entity → Use Case → Controller → HTTP]                         │
│                                                                             │
│   Entity                   UseCase Response            HTTP Response        │
│   ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐     │
│   │ Order        │  ──▶ │ {               │  ──▶ │ {            │     │
│   │  • id        │      │   orderId:      │      │   "success": │     │
│   │  • total()   │      │     string,     │      │     true,   │     │
│   │ }            │      │   status:       │      │   "data": {  │     │
│   │              │      │     enum,       │      │     ...      │     │
│   │              │      │   total:        │      │   }          │     │
│   │              │      │     string      │      │ }            │     │
│   └──────────────┘      └─────────────────┘      └──────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

클린 아키텍처의 계층 구조는 **현대적인 병원 시스템**과 같습니다. ① 엔티티는 의학 지식(병리학) - 환자가 어떻게 작동하는지에 대한 순수한 지식. ② 유스케이스는 진료 프로토콜 - 의학 지식을 환자 치료에 적용. ③ 어댑터는 간호/행정 직원 - 의사와 환자 사이의 번역. ④ 프레임워크는 장비 - MRI, X-Ray, 전자 건강 기록. 환자(데이터)가 계층을 통과하면서 각각이 자신의 역할을 수행합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 아키텍처 패턴 비교

| 특성 | 클린 아키텍처 | 헥사고날 | Onion |
|:---|:---|:---|:---|
| **핵심 원칙** | 의존성 규칙 | 포트 & 어댑터 | 동심원 격리 |
| **도메인 위치** | 가장 내부 | 내부 + 포트 | 내부 |
| **외부 인터페이스** | Adapter 계층 | Port 인터페이스 | Outer Shell |
| **테스트 용이성** | 매우 높음 | 매우 높음 | 높음 |
| **학습 곡선** | 높음 | 중간 | 중간 |
| **주요 창시자** | Uncle Bob | Alistair Cockburn | Jeffrey Palermo |
| **대표 언어** | Java, C#, TypeScript | Java, C#, Go | .NET, Java |

### N-Layer 아키텍처와의 비교

```
┌─────────────────────────────────────────────────────────────────────────────┐
│           클린 아키텍처 vs 전통적 N-Layer 아키텍처                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [전통적 N-Layer 아�텍처 - 의존성 문제]                                   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Presentation Layer                          │      │
│   │                    (Controllers, Views)                        │      │
│   └──────────────────────────────┬──────────────────────────────────┘      │
│                                  │ 의존                                    │
│                                  ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Business Logic Layer                        │      │
│   │                    (Services, Domain Models)                   │      │
│   └──────────────────────────────┬──────────────────────────────────┘      │
│                                  │ 의존                                    │
│                                  ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Data Access Layer                           │      │
│   │                    (Repositories, ORM)                         │      │
│   └──────────────────────────────┬──────────────────────────────────┘      │
│                                  │ 의존                                    │
│                                  ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Database                                   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   문제점:                                                                   │
│   • 상위 계층이 하위 계층에 의존                                          │
│   • Business Logic이 Data Access에 의존                                   │
│   • DB 교체 시 Business Logic 영향                                         │
│   • 단위 테스트 시 DB Mocking 필수                                         │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [클린 아키텍처 - 의존성 역전]                                             │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Frameworks & Drivers                        │      │
│   │                    (Express, React, PostgreSQL)               │      │
│   └──────────────────────────────┬──────────────────────────────────┘      │
│                                  │ ◀──── 의존 방향 ──────               │
│   ┌──────────────────────────────┴──────────────────────────────────┐      │
│   │                    Interface Adapters                          │      │
│   │                    (Controllers, Presenters, Repositories)     │      │
│   └──────────────────────────────┬──────────────────────────────────┘      │
│                                  │ ◀──── 의존 방향 ──────               │
│   ┌──────────────────────────────┴──────────────────────────────────┐      │
│   │                    Use Cases                                  │      │
│   │                    (Application Business Rules)               │      │
│   └──────────────────────────────┬──────────────────────────────────┘      │
│                                  │ ◀──── 의존 방향 ──────               │
│   ┌──────────────────────────────┴──────────────────────────────────┐      │
│   │                    Entities                                   │      │
│   │                    (Enterprise Business Rules)                │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   이점:                                                                     │
│   • 모든 의존성이 내부로 향함                                              │
│   • DB/프레임워크 교체 시 도메인 로직 무영향                                │
│   • 도메인 로직 단위 테스트 가능 (Mock 불필요)                              │
│   • 외부 변경 격리                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점

**1. 객체지향 설계 (OOP)와의 연계**

| SOLID 원칙 | 클린 아키텍처 적용 |
|:---|:---|
| **SRP** | 각 계층과 유스케이스가 단일 책임 수행 |
| **OCP** | 인터페이스(포트)를 통해 확장 가능, 폐쇄된 구현 |
| **LSP** | 모든 리포지토리 구현이 인터페이스 계약 준수 |
| **ISP** | 구체적 포트 분리 (IUserRepository vs IOrderRepository) |
| **DIP** | 핵심: 고수준 모듈(도메인)이 저수준 모듈(DB)에 의존하지 않음 |

**2. DDD(Domain-Driven Design)과의 완벽한 조화**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 클린 아키텍처 + DDD 전략적 설계                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Domain Layer (DDD의 Strategic Design + Tactical Design)       │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Bounded Context                                          │  │      │
│   │  │  ┌──────────────────────────────────────────────────┐    │  │      │
│   │  │  │  Aggregates                                       │    │  │      │
│   │  │  │  • Order (Aggregate Root)                          │    │  │      │
│   │  │  │  • Customer (Aggregate Root)                       │    │  │      │
│   │  │  │                                                     │    │  │      │
│   │  │  │  Entities                                          │    │  │      │
│   │  │  │  • OrderItem, Payment                               │    │  │      │
│   │  │  │                                                     │    │  │      │
│   │  │  │  Value Objects                                      │    │  │      │
│   │  │  │  • Money, Email, Address                            │    │  │      │
│   │  │  │                                                     │    │  │      │
│   │  │  │  Domain Events                                      │    │  │      │
│   │  │  │  • OrderCreated, PaymentCompleted                    │    │  │      │
│   │  │  │                                                     │    │  │      │
│   │  │  │  Domain Services                                    │    │  │      │
│   │  │  │  • DiscountCalculator, TaxCalculator                │    │  │      │
│   │  │  └──────────────────────────────────────────────────┘    │  │      │
│   │  │                                                           │  │      │
│   │  │  Repositories (Interfaces - Ports)                       │  │      │
│   │  │  • IOrderRepository, ICustomerRepository                 │  │      │
│   │  │                                                           │  │      │
│   │  │  Domain Services (Interfaces)                            │  │      │
│   │  │  • IPaymentGateway, IShippingService                     │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Application Layer (Use Cases)                                │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Command Use Cases                                       │  │      │
│   │  │  • CreateOrder, UpdateCustomer, ProcessPayment          │  │      │
│   │  │                                                           │  │      │
│   │  │  Query Use Cases (CQRS)                                  │  │      │
│   │  │  • GetOrderDetails, ListCustomerOrders                  │  │      │
│   │  │                                                           │  │      │
│   │  │  Application Services                                     │  │      │
│   │  │  • TransactionCoordinator, EventDispatcher               │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Interface Adapter Layer                                      │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Controllers (REST, GraphQL)                             │  │      │
│   │  │  Presenters (JSON serialization)                         │  │      │
│   │  │  Views (HTML, React components)                          │  │      │
│   │  │                                                           │  │      │
│   │  │  Repository Implementations                               │  │      │
│   │  │  • SequelizeOrderRepository, MongoCustomerRepository     │  │      │
│   │  │                                                           │  │      │
│   │  │  Gateway Implementations                                  │  │      │
│   │  │  • StripePaymentGateway, FedExShippingService            │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**3. 테스트 전략과의 융합**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    계층별 테스트 전략                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [Unit Tests - 가장 내부 계층]                                            │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Target: Entities, Value Objects, Domain Services              │      │
│   │                                                                 │      │
│   │  describe('Order', () => {                                       │      │
│   │    it('should calculate total correctly', () => {                │      │
│   │      const order = new Order({                                  │      │
│   │        id: '1',                                                │      │
│   │        items: [                                                │      │
│   │          new OrderItem('P1', 10000, 2),                        │      │
│   │          new OrderItem('P2', 5000, 1)                          │      │
│   │        ]                                                       │      │
│   │      });                                                       │      │
│   │                                                                 │      │
│   │      expect(order.calculateTotal().amount).toBe(25000);         │      │
│   │    });                                                         │      │
│   │  });                                                           │      │
│   │                                                                 │      │
│   │  특징:                                                           │      │
│   │  • 실행 속도: 매우 빠름 (초당 수천 개)                           │      │
│   │  • 외부 의존: 없음 (순수 로직)                                   │      │
│   │  • CI/CD: 첫 번째 장벽                                          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [Integration Tests - 유스케이스 계층]                                   │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Target: Use Cases with Mocked Ports                          │      │
│   │                                                                 │      │
│   │  describe('CreateOrderUseCase', () => {                          │      │
│   │    it('should create order and charge payment', async () => {   │      │
│   │      // Given: Mock external dependencies                       │      │
│   │      const mockOrderRepo = mock<IOrderRepository>();             │      │
│   │      const mockPayment = mock<IPaymentGateway>();                │      │
│   │                                                                 │      │
│   │      // When: Execute use case                                  │      │
│   │      const useCase = new CreateOrderUseCase(                     │      │
│   │        mockOrderRepo,                                           │      │
│   │        mockProductRepo,                                         │      │
│   │        mockPayment                                              │      │
│   │      );                                                         │      │
│   │      const result = await useCase.execute(request);              │      │
│   │                                                                 │      │
│   │      // Then: Verify behavior                                   │      │
│   │      expect(mockPayment.charge).toHaveBeenCalledWith(               │      │
│   │        expect.any(Money),                                        │      │
│   │        request.paymentMethod                                    │      │
│   │      );                                                         │      │
│   │      expect(result.orderId).toBeDefined();                      │      │
│   │    });                                                         │      │
│   │  });                                                           │      │
│   │                                                                 │      │
│   │  특징:                                                           │      │
│   │  • 실행 속도: 빠름 (초당 수백 개)                                │      │
│   │  • 외부 의존: Mock 사용                                          │      │
│   │  • 경계 검증: 인터페이스 계약 준수 확인                          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [E2E Tests - 어댑터 계층]                                              │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Target: Full system with real infrastructure                  │      │
│   │                                                                 │      │
│   │  describe('POST /orders', () => {                               │      │
│   │    it('should create order successfully', async () => {          │      │
│   │      const response = await request(app)                         │      │
│   │        .post('/api/orders')                                     │      │
│   │        .send({                                                 │      │
│   │          userId: 'user1',                                       │      │
│   │          items: [{ productId: 'P1', quantity: 2 }],             │      │
│   │          paymentMethod: { type: 'CARD', token: 'tok_123' }      │      │
│   │        })                                                      │      │
│   │        .expect(201);                                            │      │
│   │                                                                 │      │
│   │      expect(response.body.data.orderId).toBeDefined();          │      │
│   │    });                                                         │      │
│   │  });                                                           │      │
│   │                                                                 │      │
│   │  특징:                                                           │      │
│   │  • 실행 속도: 느림 (분당 수십 개)                                 │      │
│   │  • 외부 의존: 실제 인프라 (Test DB, Test API Keys)              │      │
│   │  • 용도: 핵심 흐름 검증                                          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

클린 아키텍처는 **성(sex)과 결혼의 관계**와 같습니다. 내부 계층(도메인)은 사랑과 헌신(비즈니스 가치)이며, 외부 계층(프레임워크)은 법적 계약(기술적 세부사항)입니다. 기술이 변하더라도(이혼 후 재혼), 핵심 가치(자녀, 도메인)는 보존됩니다. 건강한 관계는 각 파트너가 독립적인 동시에 상호 보완적일 때 유지됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오: 핀테크 애플리케이션 아키텍처 설계**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              핀테크 송금 서비스를 위한 클린 아키텍처                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [비즈니스 요구사항]                                                        │
│   • 금융 규정 준수 (전자금융거래법, 자금세탁방지)                              │
│   • 매년 수백 건의 기능 변경 (규정 대응)                                    │
│   • 99.99% 가용성 요구                                                      │
│   • 다양한 송금 채널 (앱, 웹, API)                                          │
│   • 금융사와의 제휴 확장성                                                  │
│                                                                             │
│   [도메인 모델 설계]                                                        │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Core Domain: 송금 (Money Transfer)                             │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Entities:                                                 │  │      │
│   │  │  • Transfer (Aggregate Root)                               │  │      │
│   │  │  • Account (Root Entity)                                   │  │      │
│   │  │  • Transaction                                             │  │      │
│   │  │                                                           │  │      │
│   │  │  Value Objects:                                            │  │      │
│   │  │  • Money, AccountNumber, BankCode                          │  │      │
│   │  │                                                           │  │      │
│   │  │  Domain Services:                                          │  │      │
│   │  │  • ExchangeRateService (환율 계산)                         │  │      │
│   │  │  • FeeCalculator (수수료 계산)                             │  │      │
│   │  │                                                           │  │      │
│   │  │  Domain Events:                                            │  │      │
│   │  │  • TransferRequested, TransferCompleted, TransferFailed     │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Use Cases                                                    │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Command:                                                 │  │      │
│   │  │  • RequestTransfer (송금 요청)                            │  │      │
│   │  │  • ConfirmTransfer (송금 확인)                            │  │      │
│   │  │  • CancelTransfer (송금 취소)                            │  │      │
│   │  │                                                           │  │      │
│   │  │  Query:                                                   │  │      │
│   │  │  • GetTransferStatus (송금 상태 조회)                      │  │      │
│   │  │  • ListTransfers (송금 내역 조회)                         │  │      │
│   │  │                                                           │  │      │
│   │  │  각 Use Case는 인터페이스(포트)에만 의존                   │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Interface Adapters                                           │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Web Controllers:                                         │  │      │
│   │  │  • REST API (Express.js)                                  │  │      │
│   │  │  • GraphQL (Apollo)                                       │  │      │
│   │  │                                                           │  │      │
│   │  │  Event Handlers:                                          │  │      │
│   │  │  • Kafka Consumer (TransferRequested 이벤트 처리)          │  │      │
│   │  │                                                           │  │      │
│   │  │  Repository Implementations:                              │  │      │
│   │  │  • PostgreSQLTransferRepository                            │  │      │
│   │  │  • RedisCacheRepository                                   │  │      │
│   │  │                                                           │  │      │
│   │  │  Gateway Implementations:                                  │  │      │
│   │  │  • ShinhanBankGateway                                     │  │      │
│   │  │  • KakaopayGateway                                        │  │      │
│   │  │  • DiasporaRemittanceGateway (해외 송금)                   │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [의사결정 포인트]                                                          │
│   1. 규정 변경 시 도메인 로직만 수정, 외부 계층 무영향                        │
│   2. 새로운 은행 제휴 시 Gateway 구현체만 추가                               │
│   3. DB 교체 시 Repository만 재구현                                          │
│   4. 테스트: 도메인 로직은 단위 테스트로 100% 커버리지                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:

1. **클린 아키텍처 선택 이유**: 금융 규정 잦은 변경, 높은 테스트 요구사항, 다양한 채널 지원

2. **CQRS 적용**: 읽기(조회)와 쓰기(명령) 분리로 성능 최적화

3. **이벤트 소싱 고려**: 모든 상태 변경을 이벤트로 저장하여 감사 추적 용이성 확보

4. **모듈형 경계**: 각 하위 도메인별로 독립적 배포 가능한 모듈 구성

### 도입 체크리스트

**기술적 평가**

| 항목 | 질문 | 가이드라인 |
|:---|:---|:---|
| **복잡도** | 비즈니스 로직 복잡도가 중간 이상인가? | 단순 CRUD는 N-Layer로 충분 |
| **변경 빈도** | 비즈니스 규칙이 자주 변경되는가? | 높으면 클린 아키텍처 적합 |
| **테스트 요구** | 높은 테스트 커버리지(90%+) 요구? | 도메인 로직 순수 테스트 가능 |
| **팀 규모** | 5명 이상의 개발자가 협업하는가? | 계층별 명확한 책임 구분 필요 |
| **프로젝트 수명** | 1년 이상 장기 프로젝트인가? | 단기 프로젝트는 과도한 설계 |

**운영·보안적 고려사항**

| 항목 | 확인사항 | 가이드라인 |
|:---|:---|:---|
| **데이터 암호화** | 민감 정보 암호화 계층 | 어댑터 계층에서 처리, 도메인 무관 |
| **감사 로그** | 모든 상태 변경 추적 | 이벤트 소싱으로 자동 감사 |
| **규정 준수** | 금융/의료 규정 대응 | 도메인 로직에 규정 캡슐화 |
| **롤백 전략** | 트랜잭션 롤백 가능성 | 유스케이스에서 원자성 보장 |

### 안티패턴

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      클린 아키텍처 안티패턴                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 1: "도메인에 기술적 세부사항 유출"                               │
│                                                                             │
│      // Order 엔티티에 ORM 의존성!                                          │
│      class Order {                                                          │
│        @Column() private _id: number;  // TypeORM 데코레이터                │
│        @Column() private _items: OrderItem[];                               │
│                                                                             │
│        // 도메인에 DB 로직!                                                │
│        async save() {                                                       │
│          await db.insert('orders', this);                                   │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 엔티티가 DB에 종속적                                                    │
│   • DB 교체 시 도메인 로직 수정 필요                                        │
│   • 단위 테스트 불가능                                                      │
│                                                                             │
│   ✅ 해결: 리포지토리 인터페이스 의존                                        │
│                                                                             │
│      // 엔티티는 순수 비즈니스 로직만                                        │
│      class Order {                                                          │
│        readonly id: string;                                                 │
│        readonly items: OrderItem[];                                        │
│      }                                                                     │
│                                                                             │
│      // 리포지토리가 영속성 책임                                             │
│      interface IOrderRepository {                                           │
│        save(order: Order): Promise<void>;                                   │
│      }                                                                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 2: "유스케이스가 너무 얇음 (Anemic Use Case)"                   │
│                                                                             │
│      class CreateOrderUseCase {                                             │
│        async execute(request: CreateOrderRequest) {                         │
│          // 단순 위임만 수행, 비즈니스 로직 부재!                          │
│          return await this.orderService.create(request);                    │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 유스케이스가 무의미한 전달자(Thin Wrapper)                              │
│   • 실제 로직이 서비스 계층에 숨겨짐                                      │
│   • 클린 아키텍처의 장점 상실                                             │
│                                                                             │
│   ✅ 해결: 유스케이스에 비즈니스 흐름 구현                                   │
│                                                                             │
│      class CreateOrderUseCase {                                             │
│        async execute(request: CreateOrderRequest) {                         │
│          // 1. 사전 검증                                                   │
│          this.validateUserCanCreate(request.userId);                        │
│                                                                             │
│          // 2. 엔티티 생성 및 도메인 로직 실행                               │
│          const order = Order.create(...);                                   │
│                                                                             │
│          // 3. 외부 연동                                                   │
│          await this.paymentGateway.charge(...);                             │
│                                                                             │
│          // 4. 저장                                                       │
│          await this.orderRepo.save(order);                                  │
│                                                                             │
│          // 5. 이벤트 발생                                                 │
│          this.eventBus.publish(new OrderCreated(order));                     │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 3: "모든 것을 도메인으로 몰려넣기"                               │
│                                                                             │
│      // 포트조차 도메인에 포함!                                             │
│      class Order {                                                          │
│        // 도메인이 HTTP를 알아야 함!                                         │
│        toJSON(): { ... }                                                    │
│        fromJSON(json: string): Order { ... }                                │
│                                                                             │
│        // 도메인이 DB를 알아야 함!                                          │
│        toSequelizeModel(): Model { ... }                                    │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 도메인의 순수성 훼손                                                      │
│   • 관심사 혼재                                                            │
│   • 재사용성 저하                                                          │
│                                                                             │
│   ✅ 해결: 어댑터에서 변환 담당                                             │
│                                                                             │
│      // 도메인은 순수                                                      │
│      class Order { ... }                                                    │
│                                                                             │
│      // 어댑터가 변환                                                      │
│      class OrderPresenter {                                                │
│        toJSON(order: Order): object {                                       │
│          return { id: order.id, total: order.total() }                     │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 4: "경계를 무시하고 계층 건너뛰기"                               │
│                                                                             │
│      // 컨트롤러가 직접 DB에 접근!                                         │
│      class OrderController {                                                │
│        async createOrder(req: Request) {                                    │
│          // 유스케이스 거치고 리포지토리 직접 호출                           │
│          await this.orderRepo.save(req.body);  // 위험!                    │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 비즈니스 로직 우회                                                      │
│   • 검증 누락 가능성                                                        │
│   • 아키텍처 무력화                                                        │
│                                                                             │
│   ✅ 해결: 모든 호출은 유스케이스 거치                                       │
│                                                                             │
│      Controller → UseCase → Repository                                     │
│                                                                             │
│      예외: 단순 조회(Query)는 CQRS로 별도 처리 가능                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

클린 아키텍처 도입은 **요리 레시피 체계화**와 같습니다. 잘못된 접근은 레시피에 설거지 방법, 그릇 세척, 재료 납품까지 모두 포함시키는 것입니다. 올바른 접근은 요리법(도메인)만 순수하게 보존하고, 주방 도구(프레임워크)와 조리 절차(유스케이스), 서빙(어댑터)를 명확히 분리하는 것입니다. 이로써 주방장을 바꾸거나 도구를 교체해도 요리의 본질은 유지됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 항목 | 전통적 아키텍처 | 클린 아키텍처 | 개선율 |
|:---|:---|:---|:---|
| **도메인 로직 테스트 커버리지** | 30-40% | 90-95% | 150% ↑ |
| **프레임워크 교체 비용** | 3-6개월 | 2-4주 | 80% ↓ |
| **신규 개발자 온보딩** | 2-3달 | 3-4주 | 70% ↓ |
| **버그 배포 비율** | 5-10% | <1% | 95% ↓ |
| **코드 중복** | 30-40% | <10% | 75% ↓ |
| **기술 부채 증가율** | 월 5% | 월 1% | 80% ↓ |

### 정성적 기대효과

1. **기술적 민첩성**: 프레임워크/DB 교체 시 도메인 로직 무영향
2. **팀 확장성**: 계층별 명확한 책임으로 신규 개발자 빠른 적응
3. **규정 준수**: 금융/의료 등 규제 산업에서의 유연한 대응
4. **장기 유지보수**: 비즈니스 로직의 순수성으로 10년+ 수명 가능

### 미래 전망

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  클린 아키텍처 미래 진화 방향                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   2025-2027: AI 기반 아키텍처 자동화                                         │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ LLM이 비즈니스 요구사항에서 클린 아키텍처 구조 생성               │      │
│   │ • "주문 관리 시스템 만들어줘" → Entity, Use Case, Port 자동 생성   │      │
│   │ • 설계 검토(DR) 자동화                                             │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   2027-2029: 모듈형 모놀리스 정교화                                           │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ 각 바운디드 컨텍스트를 독립적 배포 가능한 모듈로 패키징         │      │
│   │ • 모듈 간 메시지 기반 통신                                        │      │
│   │ • 런타임에 모듈 추가/제거 가능                                    │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   2029-2030: 셀프러스 아키텍처                                               │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ 아키텍처 결정을 AI가 자동으로 최적화                             │      │
│   │ • 성능 메트릭 기반 자동 리팩토링 제안                             │      │
│   │ • 설계 위반을 실시간으로 감지하고 수정 제안                       │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 참고 표준

| 분야 | 표준/규격 | 설명 |
|:---|:---|:---|
| **아키텍처** | ISO/IEC/IEEE 42010 | 아키텍처 설명 표준 |
| **모델링** | UML 2.x | 구조적 다이어그램 |
| **품질** | ISO/IEC 25010 | 품질 모델 |
| **프로세스** | Agile/Scrum | 애자일 개발 프로세스 |

### 📢 섹션 요약 비유

클린 아키텍처는 **도시 계획의 구역(Zoning) 개념**과 같습니다. 주거지(도메인), 상업지(유스케이스), 인프라(어댑터)가 명확히 분리되어 있습니다. 공장이 주거지 한가운데 생겨도 주민(비즈니스 로직)은 영향받지 않습니다. 계획자(아키텍트)는 구역 간 연결(포트 & 어댑터)만 신경 쓰면 되며, 각 구역 내부는 독립적으로 발전할 수 있습니다.

---

## 📌 관련 개념 맵

### 연관 개념 5개+

1. **[SOLID 원칙](./601_solid_principles.md)**: 특히 DIP(의존성 역전)이 클린 아키텍처의 핵심

2. **[헥사고날 아키텍처](./612_hexagonal_architecture.md)**: 포트 & 어댑터 패턴 기반

3. **[도메인 주도 설계](./613_ddd_basics.md)**: 전술적 패턴이 클린 아키텍처와 완벽 조화

4. **[CQRS](./621_cqrs.md)**: 읽기/쓰기 분리와 클린 아키텍처의 결합

5. **[이벤트 소싱](./620_event_sourcing.md)**: 상태 저장 대신 이벤트 스트림 저장

---

## 👶 어린이를 위한 3줄 비유 설명

**1. 무엇인가요?**
클린 아키텍처는 **장난감 정리함**처럼 소프트웨어를 계층별로 정리하는 방법입니다. 가장 안쪽에는 가장 소중한 장난감(비즈니스 로직)을, 바깥쪽에는 도구(프레임워크)를 둡니다.

**2. 어떻게 작동하나요?**
각 계층은 자신의 바깥쪽을 알지만, 안쪽은 알지 못합니다. 도구를 바꿔도 장난감은 영향받지 않고, 장난감 정리 방식을 바꿔도 도구는 그대로입니다.

**3. 왜 필요한가요?**
이렇게 정리하면 각 부분을 **독립적으로** 만들고 테스트할 수 있습니다. 장난감(비즈니스)이 도구(기술)에 의존하지 않아서, 도구를 아무리 바꿔도 장난감 놀이 방식은 변하지 않습니다.
