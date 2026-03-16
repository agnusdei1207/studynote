+++
title = "612. 헥사고날 아키텍처 (Hexagonal Architecture)"
date = "2026-03-15"
[extra]
categories = "studynote-se"
keywords = ["헥사고날", "Hexagonal Architecture", "포트와 어댑터", "Ports and Adapters"]
tags = ["SE", "Architecture", "DDD", "Microservices"]
+++

# 헥사고날 아키텍처 (Hexagonal Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 애플리케이션 **코어(도메인)를 외부 인프라(DB, UI, 외부 API)로부터 포트(Port)와 어댑터(Adapter)로 완전히 격리**하는 아키텍처
> 2. **가치**: 인프라 교체 시 코어 로직 변경 없음, 단위 테스트 가능성 100%, 기술 부채 최소화
> 3. **융합**: DDD, 클린 아키텍처, 마이크로서비스와 직접적 연관

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**헥사고날 아키텍처 (Hexagonal Architecture)**는 Alistair Cockburn이 2005년에 제창한 소프트웨어 아키텍처로, **포트(Port)와 어댑터(Adapter)** 패턴을 사용하여 애플리케이션 코어를 외부 세계로부터 격리합니다.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   헥사고날 아키텍처 핵심 구조                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                      ┌─────────────────────┐                               │
│                      │                     │          ◀────────────────     │
│                      │    Application      │                               │
│                      │       Core          │                               │
│                      │   (Hexagon)         │                               │
│                      │                     │          ────────────────▶     │
│                      └─────────────────────┘                               │
│                                │                                           │
│          ┌─────────────────────┼─────────────────────┐                    │
│          │                     │                     │                    │
│          ▼                     ▼                     ▼                    │
│   ┌──────────┐          ┌──────────┐          ┌──────────┐               │
│   │Driving  │          │Driving  │          │Driven   │               │
│   │ Adapters│          │ Adapters│          │ Adapters│               │
│   │(Primary)│          │(Primary)│          │(Secondary)│              │
│   └──────────┘          └──────────┘          └──────────┘               │
│      │                      │                      │                      │
│      ▼                      ▼                      ▼                      │
│   ┌──────────┐          ┌──────────┐          ┌──────────┐               │
│   │   UI     │          │  Tests   │          │ Database │              │
│   │  (Web)   │          │  (Unit)  │          │  (SQL)   │              │
│   └──────────┘          └──────────┘          └──────────┘               │
│                                                                             │
│   [Primary/Driving Adapters] = 애플리케이션을 구동(주도)하는 외부            │
│   [Secondary/Driven Adapters] = 애플리케이션이 사용하는 외부                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 💡 비유

헥사고날 아키텍처는 **현대적인 주택의 전기 시스템**과 같습니다:

1. **코어 (Application Core)**: 전력 소비 기구(전등, TV) - 실제 가치를 제공
2. **포트 (Ports)**: 전원 콘센트 - 표준화된 인터페이스 (110V/220V)
3. **어댑터 (Adapters)**: 플러그, 변환기 - 실제 세계와 연결

전기 회사(외부 시스템)를 바꿔도 가전제품(코어)은 영향받지 않습니다. 110V에서 220V로 바꾸려면 어댑터만 교체하면 됩니다.

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    헥사고날 아키텍처 등장 배경                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [문제: 전통적 계층형 아키텍처의 한계]                                    │
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
│   │                    (MySQL, PostgreSQL, etc.)                  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   문제점:                                                                   │
│   • Business Logic가 Database에 종속적                                    │
│   • DB 교체 시 비즈니스 로직 수정 필요                                     │
│   • 단위 테스트 시 DB mocking 필수                                        │
│   • 기술적 부채 누적                                                       │
│                                                                             │
│   [해결: 헥사고날 아키텍처의 의존성 역전]                                  │
│                                                                             │
│      ┌─────────────────────────────────────────────────────────┐          │
│      │                 Application Core                        │          │
│      │                 (Domain + Use Cases)                   │          │
│      │                                                           │          │
│      │  ┌───────────────────────────────────────────────────┐   │          │
│      │  │   Ports (Interfaces)                              │   │          │
│      │  │   • ICustomerRepository (드라이빙 포트)            │   │          │
│      │  │   • IOrderService (드라이빙 포트)                  │   │          │
│      │  │   • ICustomerController (드리븐 포트)              │   │          │
│      │  └───────────────────────────────────────────────────┘   │          │
│      └───────────────────────────────────────────────────────────┘          │
│                              ▲                                            │
│                              │                                            │
│                    ┌─────────┴─────────┐                                 │
│                    │                   │                                 │
│        ┌───────────▼───────────┐ ┌───▼───────────────┐                     │
│        │   Primary Adapters    │ │  Secondary Adapters│                    │
│        │  (드리븐/Driving)     │ │  (드리븐/Driven)    │                    │
│        │                       │ │                     │                    │
│        │  • REST Controllers   │ │  • PostgreSQL      │                    │
│        │  • CLI Commands       │ │  • MySQL           │                    │
│        │  • Unit Tests         │ │  • MongoDB         │                    │
│        │  • UI Presenters      │ │  • External API    │                    │
│        └───────────────────────┘ └─────────────────────┘                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

헥사고날 아키텍처는 **만능 리모컨**의 설계 원칙과 같습니다. 리모컨(코어)은 표준 적외선 포트(포트)를 통해 다양한 기기(어댑터)를 제어합니다. TV를 교체해도 리모컨은 그대로 작동합니다. 기기가 바뀌면 새로운 어댑터만 연결하면 됩니다. 이는 코드의 재사용성과 유연성을 극대화합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 포트(Port)와 어댑터(Adapter) 상세 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   포트와 어댑터의 상세 구조                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    APPLICATION CORE                           │      │
│   │                    (헥사곤 내부)                               │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │                                                           │  │      │
│   │  │  ┌───────────────────────────────────────────────────┐   │  │      │
│   │  │  │           Driving Ports (Primary)                   │   │  │      │
│   │  │  │           (드리븐 포트 / 인입구)                    │   │  │      │
│   │  │  │                                                       │   │  │      │
│   │  │  │  interface ICustomerController {                     │   │  │      │
│   │  │  │    createCustomer(request: CreateCustomerRequest)     │   │  │      │
│   │  │  │    getCustomer(id: string): CustomerResponse          │   │  │      │
│   │  │  │  }                                                      │   │  │      │
│   │  │  │                                                       │   │  │      │
│   │  │  │  interface IOrderController {                        │   │  │      │
│   │  │  │    createOrder(request: CreateOrderRequest)           │   │  │      │
│   │  │  │    cancelOrder(id: string): void                      │   │  │      │
│   │  │  │  }                                                      │   │  │      │
│   │  │  └───────────────────────────────────────────────────┘   │  │      │
│   │  │                                                           │  │      │
│   │  │  ┌───────────────────────────────────────────────────┐   │  │      │
│   │  │  │           Driven Ports (Secondary)                  │   │  │      │
│   │  │  │           (드리븐 포트 / 출입구)                    │   │  │      │
│   │  │  │                                                       │   │  │      │
│   │  │  │  interface ICustomerRepository {                     │   │  │      │
│   │  │  │    save(customer: Customer): Promise<void>            │   │  │      │
│   │  │  │    findById(id: string): Promise<Customer | null>     │   │  │      │
│   │  │  │  }                                                      │   │  │      │
│   │  │  │                                                       │   │  │      │
│   │  │  │  interface IEmailService {                           │   │  │      │
│   │  │  │    send(to: string, subject: string, body: string)    │   │  │      │
│   │  │  │  }                                                      │   │  │      │
│   │  │  └───────────────────────────────────────────────────┘   │  │      │
│   │  │                                                           │  │      │
│   │  │  ┌───────────────────────────────────────────────────┐   │  │      │
│   │  │  │           Domain Model                             │   │  │      │
│   │  │  │           (엔티티, 값 객체, 비즈니스 로직)          │   │  │      │
│   │  │  └───────────────────────────────────────────────────┘   │  │      │
│   │  │                                                           │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    ADAPTERS (외부)                              │      │
│   │                    (헥사곤 외부)                               │      │
│   │                                                                  │      │
│   │  [Primary/Driving Adapters] = 애플리케이션을 구동              │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  REST Controller Adapter                                 │  │      │
│   │  │  • Express.js, Spring MVC, FastAPI                      │  │      │
│   │  │  • HTTP 요청을 Driving Port로 변환                       │  │      │
│   │  │                                                           │  │      │
│   │  │  CLI Adapter                                              │  │      │
│   │  │  • Commander.js, argparse                                 │  │      │
│   │  │  • 명령행 인자를 Driving Port로 변환                      │  │      │
│   │  │                                                           │  │      │
│   │  │  Unit Test Adapter                                        │  │      │
│   │  │  • Jest, JUnit                                             │  │      │
│   │  │  • 테스트 코드가 Driving Port 구현                         │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   │                                                                  │      │
│   │  [Secondary/Driven Adapters] = 애플리케이션이 사용            │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Database Repository Adapter                              │  │      │
│   │  │  • SequelizeRepository, MongoDBRepository                │  │      │
│   │  │  • Driven Port(인터페이스)를 구현                         │  │      │
│   │  │                                                           │  │      │
│   │  │  External Service Adapter                                  │  │      │
│   │  │  • SendGridEmailService, StripePaymentService             │  │      │
│   │  │  • 외부 API 호출을 Driven Port로 매핑                     │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드 구현

```typescript
// ==================== APPLICATION CORE (헥사곤 내부) ====================

// 도메인 엔티티: 외부 의존성 없음
export class Customer {
    private readonly _id: string;
    private _name: string;
    private _email: string;
    private readonly _createdAt: Date;

    constructor(props: CustomerProps) {
        this._id = props.id;
        this._name = props.name;
        this._email = props.email;
        this._createdAt = new Date();
        this.validate();
    }

    get id(): string { return this._id; }
    get name(): string { return this._name; }
    get email(): string { return this._email; }

    updateName(name: string): void {
        if (!name || name.length < 2) {
            throw new Error('Invalid name');
        }
        this._name = name;
    }

    updateEmail(email: string): void {
        if (!this.isValidEmail(email)) {
            throw new Error('Invalid email');
        }
        this._email = email;
    }

    private validate(): void {
        if (!this._name || this._name.length < 2) {
            throw new Error('Invalid customer data');
        }
        if (!this.isValidEmail(this._email)) {
            throw new Error('Invalid email');
        }
    }

    private isValidEmail(email: string): boolean {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
}

// Driving Port (Primary): 애플리케이션 진입점 인터페이스
export interface ICustomerController {
    createCustomer(request: CreateCustomerRequest): Promise<CustomerResponse>;
    getCustomer(id: string): Promise<CustomerResponse>;
    updateCustomer(id: string, request: UpdateCustomerRequest): Promise<void>;
    deleteCustomer(id: string): Promise<void>;
}

// Driven Port (Secondary): 외부 의존성 인터페이스
export interface ICustomerRepository {
    save(customer: Customer): Promise<void>;
    findById(id: string): Promise<Customer | null>;
    findAll(): Promise<Customer[]>;
    delete(id: string): Promise<void>;
}

export interface IEmailService {
    sendWelcomeEmail(customerEmail: string, customerName: string): Promise<void>;
}

// 유스케이스: 애플리케이션 코어 비즈니스 로직
export class CreateCustomerUseCase {
    constructor(
        private readonly customerRepo: ICustomerRepository,
        private readonly emailService: IEmailService
    ) {}

    async execute(request: CreateCustomerRequest): Promise<CustomerResponse> {
        // 1. 비즈니스 로직: 이메일 중복 확인
        const existing = await this.customerRepo.findByEmail(request.email);
        if (existing) {
            throw new Error('Customer already exists');
        }

        // 2. 도메인 엔티티 생성
        const customer = new Customer({
            id: this.generateId(),
            name: request.name,
            email: request.email
        });

        // 3. 영속화
        await this.customerRepo.save(customer);

        // 4. 부수 효과 (Side Effect)
        await this.emailService.sendWelcomeEmail(
            customer.email,
            customer.name
        );

        return {
            id: customer.id,
            name: customer.name,
            email: customer.email,
            createdAt: customer._createdAt
        };
    }

    private generateId(): string {
        return `cust_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
}

// ==================== ADAPTERS (헥사곤 외부) ====================

// Primary Adapter: REST Controller (Driving Adapter)
export class RestCustomerController implements ICustomerController {
    private readonly createCustomerUseCase: CreateCustomerUseCase;

    constructor(createCustomerUseCase: CreateCustomerUseCase) {
        this.createCustomerUseCase = createCustomerUseCase;
    }

    async createCustomer(request: CreateCustomerRequest): Promise<CustomerResponse> {
        try {
            return await this.createCustomerUseCase.execute(request);
        } catch (error) {
            // HTTP 에러 변환
            if (error.message === 'Customer already exists') {
                throw new ConflictError(error.message);
            }
            throw new BadRequestError(error.message);
        }
    }

    async getCustomer(id: string): Promise<CustomerResponse> {
        const customer = await this.customerRepo.findById(id);
        if (!customer) {
            throw new NotFoundError('Customer not found');
        }
        return this.toResponse(customer);
    }

    // Express.js 라우터와 연동
    getRoutes(): express.Router {
        const router = express.Router();

        router.post('/customers',
            validateRequest,
            async (req, res) => {
                const response = await this.createCustomer(req.body);
                res.status(201).json(response);
            }
        );

        router.get('/customers/:id',
            async (req, res) => {
                const response = await this.getCustomer(req.params.id);
                res.json(response);
            }
        );

        return router;
    }
}

// Primary Adapter: CLI (Driving Adapter)
export class CliCustomerController implements ICustomerController {
    private readonly createCustomerUseCase: CreateCustomerUseCase;

    constructor(createCustomerUseCase: CreateCustomerUseCase) {
        this.createCustomerUseCase = createCustomerUseCase;
    }

    async createCustomer(request: CreateCustomerRequest): Promise<CustomerResponse> {
        const response = await this.createCustomerUseCase.execute(request);
        console.log(`Customer created: ${response.id}`);
        return response;
    }

    // Commander.js와 연동
    registerCommands(program: Command): void {
        program
            .command('customer:create')
            .requiredOption('-n, --name <name>')
            .requiredOption('-e, --email <email>')
            .action(async (options) => {
                await this.createCustomer({
                    name: options.name,
                    email: options.email
                });
            });
    }
}

// Primary Adapter: Unit Test (Driving Adapter)
class TestCustomerController implements ICustomerController {
    public lastCreatedCustomer: CustomerResponse | null = null;

    async createCustomer(request: CreateCustomerRequest): Promise<CustomerResponse> {
        const response = await this.createCustomerUseCase.execute(request);
        this.lastCreatedCustomer = response;
        return response;
    }

    // 테스트용 헬퍼 메서드
    getLastCreatedCustomer(): CustomerResponse | null {
        return this.lastCreatedCustomer;
    }
}

// Secondary Adapter: PostgreSQL Repository (Driven Adapter)
export class PostgresCustomerRepository implements ICustomerRepository {
    constructor(private readonly dbClient: Pool) {}

    async save(customer: Customer): Promise<void> {
        await this.dbClient.query(
            'INSERT INTO customers (id, name, email, created_at) VALUES ($1, $2, $3, $4)',
            [customer.id, customer.name, customer.email, customer._createdAt]
        );
    }

    async findById(id: string): Promise<Customer | null> {
        const result = await this.dbClient.query(
            'SELECT * FROM customers WHERE id = $1',
            [id]
        );

        if (result.rows.length === 0) {
            return null;
        }

        const row = result.rows[0];
        return new Customer({
            id: row.id,
            name: row.name,
            email: row.email
        });
    }
}

// Secondary Adapter: In-Memory Repository (Driven Adapter)
export class InMemoryCustomerRepository implements ICustomerRepository {
    private readonly customers = new Map<string, Customer>();

    async save(customer: Customer): Promise<void> {
        this.customers.set(customer.id, customer);
    }

    async findById(id: string): Promise<Customer | null> {
        return this.customers.get(id) || null;
    }
}

// Secondary Adapter: SendGrid Email Service (Driven Adapter)
export class SendGridEmailService implements IEmailService {
    constructor(private readonly sendGridClient: SendGrid) {}

    async sendWelcomeEmail(customerEmail: string, customerName: string): Promise<void> {
        await this.sendGridClient.send({
            to: customerEmail,
            from: 'noreply@example.com',
            subject: 'Welcome!',
            text: `Hello ${customerName}, welcome to our service!`
        });
    }
}

// Secondary Adapter: Mock Email Service (Driven Adapter for Testing)
export class MockEmailService implements IEmailService {
    public sentEmails: Array<{to: string, subject: string, body: string}> = [];

    async sendWelcomeEmail(customerEmail: string, customerName: string): Promise<void> {
        this.sentEmails.push({
            to: customerEmail,
            subject: 'Welcome!',
            body: `Hello ${customerName}!`
        });
    }

    getLastSentEmail(): {to: string, subject: string, body: string} | null {
        return this.sentEmails[this.sentEmails.length - 1] || null;
    }
}

// ==================== COMPOSITION (의존성 주입) ====================

export function createApplication(
    customerRepo: ICustomerRepository,
    emailService: IEmailService
) {
    // 유스케이스 생성
    const createCustomerUseCase = new CreateCustomerUseCase(
        customerRepo,
        emailService
    );

    // 어댑터 생성
    const restController = new RestCustomerController(createCustomerUseCase);
    const cliController = new CliCustomerController(createCustomerUseCase);
    const testController = new TestCustomerController(createCustomerUseCase);

    return {
        useCases: { createCustomer: createCustomerUseCase },
        controllers: {
            rest: restController,
            cli: cliController,
            test: testController
        }
    };
}

// ==================== USAGE EXAMPLES ====================

// 1. Production 환경 구성
const prodApp = createApplication(
    new PostgresCustomerRepository(pgPool),
    new SendGridEmailService(sendGridClient)
);

// Express.js 서버 시작
app.use('/api', prodApp.controllers.rest.getRoutes());

// 2. CLI 환경 구성
const cliApp = createApplication(
    new PostgresCustomerRepository(pgPool),
    new SendGridEmailService(sendGridClient)
);

// CLI 명령 등록
cliApp.controllers.cli.registerCommands(program);
program.parse(process.argv);

// 3. 단위 테스트 환경 구성
const testApp = createApplication(
    new InMemoryCustomerRepository(),
    new MockEmailService()
);

// 테스트 코드
describe('CreateCustomerUseCase', () => {
    it('should create customer successfully', async () => {
        // Given
        const controller = testApp.controllers.test;
        const request = {
            name: 'John Doe',
            email: 'john@example.com'
        };

        // When
        const response = await controller.createCustomer(request);

        // Then
        expect(response.id).toBeDefined();
        expect(response.name).toBe('John Doe');
        expect(response.email).toBe('john@example.com');
    });
});
```

### 데이터 흐름

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    헥사고날 아키텍처 데이터 흐름                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [요청(Request) 흐름 - Primary Side]                                      │
│                                                                             │
│   External System                                                           │
│        │                                                                   │
│        │ HTTP POST /customers                                              │
│        │ {                                                                 │
│        │   "name": "John Doe",                                            │
│        │   "email": "john@example.com"                                     │
│        │ }                                                                │
│        ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Primary Adapter (REST Controller)                              │      │
│   │  ┌──────────────────────────────────────────────────────────┐   │      │
│   │  │  1. HTTP Request 수신                                      │   │      │
│   │  │  2. Request Validation                                     │   │      │
│   │  │  3. HTTP → UseCase Request 변환                              │   │      │
│   │  │  4. Driving Port 호출                                        │   │      │
│   │  └──────────────────────────────────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│        │                                                                   │
│        │ createCustomer({ name, email })                                 │
│        ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Application Core (Hexagon)                                      │      │
│   │  ┌──────────────────────────────────────────────────────────┐   │      │
│   │  │  1. 비즈니스 로직 실행                                       │   │      │
│   │  │  2. 도메인 엔티티 생성                                       │   │      │
│   │  │  3. Driven Port 호출                                        │   │      │
│   │  └──────────────────────────────────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│        │                                                                   │
│        │ save(customer), sendWelcomeEmail(...)                          │
│        ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Secondary Adapters                                              │      │
│   │  ┌─────────────────────┐  ┌───────────────────────────────┐   │      │
│   │  │ PostgreSQL Repository│  │ SendGrid Email Service        │   │      │
│   │  │  • INSERT 쿼리 실행   │  │  • API 호출                   │   │      │
│   │  │  • 결과 반환         │  │  • 이메일 발송                 │   │      │
│   │  └─────────────────────┘  └───────────────────────────────┘   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│        │                                                                   │
│        │ CustomerResponse                                                │
│        ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Primary Adapter (REST Controller)                              │      │
│   │  • CustomerResponse → HTTP Response 변환                        │      │
│   │  • HTTP 201 + JSON                                             │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│        │                                                                   │
│        ▼                                                                   │
│   External System                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

헥사고날 아키텍처의 포트와 어댑터는 **전기 콘센트와 플러그** 시스템과 같습니다. 콘센트(포트)는 표준화된 인터페이스를 정의하고, 플러그(어댑터)는 그 인터페이스를 구현합니다. 110V 가전제품을 220V 콘센트에 꽂으려면 변환 어댑터만 있으면 됩니다. 기기(코어)를 바꿀 필요가 없습니다. 이로써 시스템의 **교체 가능성(Swappability)**이 극대화됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 아키텍처 패턴 비교

| 특성 | 헥사고날 아키텍처 | 클린 아키텍처 | 전통적 계층형 |
|:---|:---|:---|:---|
| **핵심 개념** | 포트 & 어댑터 | 의존성 규칙 | 계층 분리 |
| **도메인 격리** | 완전 격리 | 완전 격리 | 부분 격리 |
| **외부 의존성** | 인터페이스(포트) | 인터페이스(포트) | 직접 의존 |
| **테스트 용이성** | 매우 높음 | 매우 높음 | 중간 |
| **학습 곡선** | 중간 | 높음 | 낮음 |
| **주요 창시자** | Alistair Cockburn | Uncle Bob | 전통적 SE |
| **적용 분야** | DDD, MSA | 대형 엔터프라이즈 | 소규모 앱 |

### 마이크로서비스와의 결합

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              헥사고날 아키텍처 기반 마이크로서비스                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    API Gateway                                  │      │
│   │                    (외부 진입점)                                │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │              Order Service (마이크로서비스)                      │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │                  Primary Adapters                          │  │      │
│   │  │  ┌────────────────────────────────────────────────────┐  │  │      │
│   │  │  │  REST Controller (Express.js)                       │  │  │      │
│   │  │  │  GraphQL Resolver (Apollo)                           │  │  │      │
│   │  │  │  gRPC Server (Node.js gRPC)                          │  │  │      │
│   │  │  └────────────────────────────────────────────────────┘  │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   │                           │                                     │      │
│   │                           ▼                                     │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │                  Application Core                          │  │      │
│   │  │  ┌────────────────────────────────────────────────────┐  │  │      │
│   │  │  │  Domain: Order, Customer, Product                   │  │  │      │
│   │  │  │  Use Cases: CreateOrder, ProcessPayment             │  │  │      │
│   │  │  │  Ports: IOrderRepository, IInventoryService          │  │  │      │
│   │  │  └────────────────────────────────────────────────────┘  │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   │                           │                                     │      │
│   │                           ▼                                     │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │                  Secondary Adapters                        │  │      │
│   │  │  ┌────────────────────────────────────────────────────┐  │  │      │
│   │  │  │  PostgreSQL DB (Persistence)                       │  │  │      │
│   │  │  │  Redis Cache (Read Model)                           │  │  │      │
│   │  │  │  Kafka Event Bus (Integration)                      │  │  │      │
│   │  │  │  Inventory Service (HTTP Client)                     │  │  │      │
│   │  │  │  Payment Gateway (gRPC Client)                       │  │  │      │
│   │  │  └────────────────────────────────────────────────────┘  │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [마이크로서비스 간 통신]                                                   │
│                                                                             │
│   Order Service ──▶ Inventory Service (HTTP/gRPC)                           │
│        │                                                                   │
│        │ OrderCreated Event                                                │
│        ▼                                                                   │
│   Kafka ──▶ Shipping Service ──▶ Notification Service                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점

**1. SOLID 원칙과의 완벽한 조화**

| SOLID 원칙 | 헥사고날 적용 |
|:---|:---|
| **SRP** | 각 포트와 어댑터가 단일 책임 |
| **OCP** | 새로운 어댑터 추가로 기능 확장, 코어 수정 없음 |
| **LSP** | 모든 어댑터가 포트 인터페이스 계약 준수 |
| **ISP** | 구체적 포트 분리 (ICustomerRepository vs IOrderRepository) |
| **DIP** | 코어가 추상화(포트)에 의존, 구현(어댑터)은 모름 |

**2. DDD와의 연계**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 헥사고날 + DDD 전술적 패턴 매핑                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Application Core = DDD Domain Layer                            │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Aggregates (Aggregate Root)                               │  │      │
│   │  │  • Order, Customer, Product                               │  │      │
│   │  │                                                           │  │      │
│   │  │  Entities                                                 │  │      │
│   │  │  • OrderItem, Payment, Address                            │  │      │
│   │  │                                                           │  │      │
│   │  │  Value Objects                                            │  │      │
│   │  │  • Money, Email, Quantity                                 │  │      │
│   │  │                                                           │  │      │
│   │  │  Domain Services                                          │  │      │
│   │  │  • DiscountCalculator, TaxCalculator                      │  │      │
│   │  │                                                           │  │      │
│   │  │  Domain Events                                            │  │      │
│   │  │  • OrderCreated, PaymentCompleted                         │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   │                                                                  │      │
│   │  Use Cases = DDD Application Services                         │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  • CreateOrderUseCase                                     │  │      │
│   │  │  • ProcessPaymentUseCase                                  │  │      │
│   │  │  • CancelOrderUseCase                                     │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   Ports = DDD Repository/Service Interfaces                               │
│                                                                             │
│   Adapters = DDD Infrastructure Implementations                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**3. 테스트 주도 개발(TDD)과의 시너지**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  헥사고날 아키텍처와 TDD 시너지                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [Red: 실패하는 테스트 작성]                                              │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  describe('CreateCustomerUseCase', () => {                        │      │
│   │    it('should create customer', async () => {                     │      │
│   │      // Given: Test Adapters 사용                                │      │
│   │      const mockRepo = new InMemoryCustomerRepository();           │      │
│   │      const mockEmail = new MockEmailService();                   │      │
│   │      const useCase = new CreateCustomerUseCase(mockRepo, mockEmail);│     │
│   │                                                                 │      │
│   │      // When                                                    │      │
│   │      await useCase.execute({                                     │      │
│   │        name: 'John',                                            │      │
│   │        email: 'john@example.com'                                │      │
│   │      });                                                        │      │
│   │                                                                 │      │
│   │      // Then: 테스트 어댑터로 검증                             │      │
│   │      const customer = await mockRepo.findByEmail('john@example.com');│     │
│   │      expect(customer).toBeDefined();                             │      │
│   │      expect(mockEmail.getLastSentEmail()).toBeDefined();           │      │
│   │    });                                                          │      │
│   │  });                                                            │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [Green: 최소 구현으로 테스트 통과]                                        │
│   • 도메인 로직에만 집중                                                   │
│   • DB, 외부 API 고려 없음                                                 │
│   • 빠른 피드백 루프                                                       │
│                                                                             │
│   [Refactor: 코드 개선]                                                     │
│   • 도메인 로직 정교화                                                     │
│   • 아키텍처 경계 준수                                                     │
│   • 리팩토링 후 테스트 여전히 통과                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

헥사고날 아키텍처는 **레스토랑 주방의 파트너 시스템**과 같습니다. 주방(코어)은 조리법(비즈니스 로직)에 집중합니다. 식자재 공급업체(Secondary Adapter)나 서빙 직원(Primary Adapter)가 바뀌어도 주방은 영향받지 않습니다. 새로운 공급업체를 추가하려면 계약(Port)만 맺으면 됩니다. 이로써 레스토랑은 품질 일관성을 유지하며 외부 변화에 유연하게 대응할 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오: 핀테크 송금 서비스의 헥사고날 아키텍처**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              핀테크 송금 서비스 헥사고날 아키텍처 설계                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [비즈니스 요구사항]                                                        │
│   • 다양한 송금 채널 지원 (앱, 웹, API, 제휴사)                              │
│   • 은행 연동 시 잦은 변경 (규정, 수수료)                                   │
│   • 높은 트랜잭션 처리량                                                    │
│   • 금융 감사 요구 (모든 상태 변경 추적)                                    │
│                                                                             │
│   [Application Core 설계]                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Domain Layer                                                      │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Entities:                                                 │  │      │
│   │  │  • Transfer (Aggregate Root) - 핵심 도메인                 │  │      │
│   │  │  • Account (Root Entity)                                   │  │      │
│   │  │  • Transaction                                             │  │      │
│   │  │                                                           │  │      │
│   │  │  Value Objects:                                            │  │      │
│   │  │  • Money, AccountNumber, BankCode, ExchangeRate           │  │      │
│   │  │                                                           │  │      │
│   │  │  Domain Events:                                            │  │      │
│   │  │  • TransferRequested, TransferCompleted, TransferFailed   │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Ports (Interfaces)                                             │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Primary Ports (Driving):                                 │  │      │
│   │  │  • ITransferController - 송금 요청 인터페이스             │  │      │
│   │  │  • ITransferQuery - 조회 인터페이스                        │  │      │
│   │  │                                                           │  │      │
│   │  │  Secondary Ports (Driven):                                │  │      │
│   │  │  • ITransferRepository - 영속성 포트                       │  │      │
│   │  │  • IBankGateway - 은행 연동 포트                          │  │      │
│   │  │  • IExchangeRateService - 환율 조회 포트                   │  │      │
│   │  │  • IFeeCalculator - 수수료 계산 포트                       │  │      │
│   │  │  • IAntiFraudService - 사기 방지 포트                       │  │      │
│   │  │  • INotificationService - 알림 포트                        │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                           │                                                 │
│                           ▼                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  Adapters (Implementations)                                    │      │
│   │  ┌──────────────────────────────────────────────────────────┐  │      │
│   │  │  Primary Adapters:                                         │  │      │
│   │  │  • RestTransferController (Express.js)                    │  │      │
│   │  │  • GraphQLTransferResolver (Apollo)                       │  │      │
│   │  │  • GrpcTransferServer (gRPC)                              │  │      │
│   │  │  • CliTransferController (Commander.js)                   │  │      │
│   │  │  • PartnerApiAdapter (제휴사용 API)                       │  │      │
│   │  │                                                           │  │      │
│   │  │  Secondary Adapters:                                       │  │      │
│   │  │  • PostgresTransferRepository                             │  │      │
│   │  │  • RedisCacheRepository (성능 최적화)                     │  │      │
│   │  │  • ShinhanBankGateway                                     │  │      │
│   │  │  • KakaopayGateway                                       │  │      │
│   │  │  • KoreaExchangeRateService                               │  │      │
│   │  │  • RuleBasedFeeCalculator                                 │  │      │
│   │  │  • MLBasedAntiFraudService                                 │  │      │
│   │  │  • EmailNotificationService                                │  │      │
│   │  │  • SmsNotificationService                                 │  │      │
│   │  └──────────────────────────────────────────────────────────┘  │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   [의사결정 포인트]                                                          │
│   1. 새로운 은행 제휴 시 IBankGateway 구현체만 추가                          │
│   2. 환율 제공자 변경 시 IExchangeRateService 구현체만 교체                   │
│   3. 알림 채널 추가(IN알림, 카톡) 시 INotificationService 구현체 추가        │
│   4. 도메인 로직은 모든 변경으로부터 보호                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 도입 체크리스트

**기술적 평가**

| 항목 | 질문 | 가이드라인 |
|:---|:---|:---|
| **복잡도** | 외부 연동이 3개 이상인가? | 단순한 CRUD에는 과도한 설계 |
| **변경 빈도** | 인프라가 자주 변경되는가? | 높으면 헥사고날 적합 |
| **테스트 요구** | 단위 테스트 커버리지 목표 90%+? | 순수 도메인 로직 테스트 가능 |
| **다중 인터페이스** | 다양한 채널 지원 필요성? | REST, GraphQL, CLI 동시 지원 |
| **팀 규모** | 5인 이상 팀 협업? | 명확한 경계로 협업 용이 |

**운영·보안적 고려사항**

| 항목 | 확인사항 | 가이드라인 |
|:---|:---|:---|
| **데이터 암호화** | 민감 데이터 처리 계층 | Secondary Adapter에서 처리 |
| **감사 로그** | 모든 상태 변경 추적 | 도메인 이벤트 + Event Store |
| **회복 전략** | 어댑터 장애 시 대응 | Fallback Adapter 패턴 |
| **비용 최적화** | 외부 API 호출 비용 | Cache Adapter 적용 |

### 안티패턴

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      헥사고날 아키텍처 안티패턴                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 1: "헥사곤이 아닌 원형(Circle)"                                │
│                                                                             │
│      // 포트가 구현을 직접 알게 됨!                                         │
│      interface ICustomerRepository {                                       │
│        save(customer: Customer, dbClient: Pool): Promise<void>;  // DB 노출!│
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 포트의 목적(추상화) 무효화                                             │
│   • 코어가 외부 세부사항 노출                                               │
│   • 헥사고날의 장점 상실                                                   │
│                                                                             │
│   ✅ 해결: 포트는 순수 인터페이스                                            │
│                                                                             │
│      interface ICustomerRepository {                                       │
│        save(customer: Customer): Promise<void>;                           │
│      }                                                                     │
│                                                                             │
│      // 구현체만 DB 알음                                                   │
│      class PostgresCustomerRepository implements ICustomerRepository {       │
│        constructor(private dbClient: Pool) {}                              │
│        async save(customer: Customer) {                                    │
│          await this.dbClient.query(...);                                   │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 2: "모든 것을 하나의 헥사곤에"                                   │
│                                                                             │
│      // 하나의 거대한 헥사곤에 모든 것 포함                                  │
│      ┌───────────────────────────────────────────────────────────────┐     │
│      │          Monolithic Hexagon                                  │     │
│      │  • Order, Customer, Product, Inventory, Shipping...        │     │
│      │  • 모든 유스케이스                                            │     │
│      │  • 모든 포트와 어댑터                                        │     │
│      └───────────────────────────────────────────────────────────────┘     │
│                                                                             │
│   문제점:                                                                   │
│   • 배포 독립성 불가                                                      │
│   • 팀 확장 어려움                                                         │
│   • 변경 영향 범위 광범위                                                 │
│                                                                             │
│   ✅ 해결: 바운디드 컨텍스트별 헥사곤 분리                                 │
│                                                                             │
│      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│      │ Order Hexagon│  │ Customer    │  │ Inventory    │               │
│      │              │  │ Hexagon      │  │ Hexagon      │               │
│      └──────────────┘  └──────────────┘  └──────────────┘               │
│              │                  │                  │                    │
│              └──────────────────┴──────────────────┘                    │
│                                 ▼                                        │
│                         Event Bus (Kafka)                              │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ 안티패턴 3: "어댑터가 비즈니스 로직 포함"                                 │
│                                                                             │
│      // 어댑터에 비즈니스 로직이!                                            │
│      class PostgresCustomerRepository implements ICustomerRepository {       │
│        async save(customer: Customer) {                                    │
│          // DB 로직인데 이메일 전송?!                                      │
│          await this.emailService.sendWelcome(customer.email);              │
│          await this.dbClient.query(...);                                   │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
│   문제점:                                                                   │
│   • 비즈니스 로직이 어댑터에 누출                                         │
│   • 재사용 불가                                                           │
│   • 테스트 어려움                                                          │
│                                                                             │
│   ✅ 해결: 코어에서 비즈니스 로직, 어댑터는 기술적 구현만                   │
│                                                                             │
│      // 코어: 유스케이스에서 모든 비즈니스 로직                           │
│      class CreateCustomerUseCase {                                         │
│        async execute(request) {                                           │
│          const customer = new Customer(request);                           │
│          await this.repo.save(customer);                                   │
│          await this.emailService.sendWelcome(customer.email);  // 코어에!  │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
│      // 어댑터: 순수한 DB 연동만                                            │
│      class PostgresCustomerRepository implements ICustomerRepository {       │
│        async save(customer: Customer) {                                    │
│          await this.dbClient.query('INSERT...', customer);                 │
│        }                                                                   │
│      }                                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

헥사고날 아키텍터의 도입은 **집안 리모델링**과 같습니다. 잘못된 접근은 벽을 허물고 나서 전기 배선과 수관을 섞어서 모든 것을 다시 해야 합니다. 올바른 접근은 계획(포트)을 먼저 세우고, 전기, 수도, 가구(어댑터)를 독립적으로 설치하는 것입니다. 이로써 나중에 주방을 바꾸거나 가구를 교체해도 다른 부분에 영향이 없습니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 항목 | 전통적 아키텍처 | 헥사고날 | 개선율 |
|:---|:---|:---|:---|
| **단위 테스트 커버리지** | 30-50% | 90-95% | 100% ↑ |
| **인프라 교체 시간** | 2-4주 | 2-3일 | 90% ↓ |
| **신규 채널 추가** | 3-4주 | 3-5일 | 85% ↓ |
| **기술 부채 증가율** | 월 8% | 월 2% | 75% ↓ |
| **개발자 온보딩** | 4-8주 | 2-3주 | 60% ↓ |

### 정성적 기대효과

1. **기술적 민첩성**: 프레임워크, DB, 외부 API 교체 시 코어 무영향
2. **팀 자율성**: 각 바운디드 컨텍스트별 독립적 개발/배포
3. **장기 유지보수**: 도메인 로직의 순수성으로 10년+ 수명 가능
4. **리스크 분산**: 외부 의존성 최소화로 공급망 리스크 감소

### 미래 전망

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  헥사고날 아키텍처 미래 진화                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   2025-2027: 함수형 헥사고날                                                │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ 함수형 프로그래밍(FP)와 결합하여 불변성 강화                          │      │
│   │ • 순수 함수로 포트 정의                                            │      │
│   │ • 상태 관리 최소화                                                 │      │
│   │ • 부수 효과 명시적 표현                                            │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   2027-2029: 이벤트 소싱 헥사고날                                          │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ 모든 상태 변경을 이벤트 스트림으로 저장                             │      │
│   │ • 완전한 감사 추적성                                               │      │
│   │ • 시간 여행 가능(상태 재생)                                        │      │
│   │ • 분산 시스템에 최적화                                              │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   2029-2030: AI 기반 자동 조립                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │ LLM이 비즈니스 요구사항에서 포트/어댑터 구조 자동 생성               │      │
│   │ • "주문 관리 모듈 만들어줘" → 포트 인터페이스 자동 생성               │      │
│   │ • 구현체 후보 추천                                                 │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 참고 표준

| 분야 | 표준/규격 | 설명 |
|:---|:---|:---|
| **아키텍처** | IEEE 1471 | 아키텍처 설명 표준 |
| **UML** | UML 2.x | 컴포넌트 다이어그램 |
| **DDD** | DDD Reference | Eric Evans의 도메인 주도 설계 |

### 📢 섹션 요약 비유

헥사고날 아키텍처는 **현대적인 자동차의 모듈형 설계**와 같습니다. 엔진(도메인)은 표준화된 인터페이스(포트)를 통해 변속기, 서스펜션, 전자장비(어댑터)와 연결됩니다. 부품을 교체하거나 업그레이드해도 엔진은 그대로입니다. 이로써 자동차는 지속적으로 발전하면서도 핵심 성능을 유지할 수 있습니다. 소프트웨어도 같은 원리로 진화할 수 있습니다.

---

## 📌 관련 개념 맵

### 연관 개념 5개+

1. **[클린 아키텍처](./611_clean_architecture.md)**: 헥사고날의 발전형 형태

2. **[DDD 도메인 주도 설계](./613_ddd_basics.md)**: 헥사고날과 완벽 조화

3. **[마이크로서비스](./614_bounded_context.md)**: 각 서비스가 헥사고날 패턴 따름

4. **[CQRS](./621_cqrs.md)**: 읽기/쓰기 포트 분리와 헥사고날 결합

5. **[이벤트 소싱](./620_event_sourcing.md)**: 상태 저장 대신 이벤트 스트림

---

## 👶 어린이를 위한 3줄 비유 설명

**1. 무엇인가요?**
헥사고날 아키텍처는 **여섯 갈래 진입로가 있는 고성 반려견 우리**와 같습니다. 반려견(도메인 로직)은 안쪽에 있고, 여러 입구(포트)를 통해 다양한 방식(어댑터)으로 접근할 수 있습니다.

**2. 어떻게 작동하나요?**
진입로(포트)는 표준 규격으로 만들어져서 어떤 문(어댑터)으로든 열 수 있습니다. 웹브라우저, 모바일 앱, 명령행 도구 등 다양한 방식으로 같은 반려견에게 명령을 내릴 수 있습니다.

**3. 왜 필요한가요?**
이렇게 만들면 반려견(비즈니스 로직)을 바꾸지 않고도 입구(기술)를 마음껏 바꿀 수 있습니다. 웹사이트를 바꾸거나 데이터베이스를 교체해도 반려견이 하는 훈련(도메인 로직)은 그대로입니다.
