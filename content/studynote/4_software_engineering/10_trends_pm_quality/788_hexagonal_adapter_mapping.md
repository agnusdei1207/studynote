+++
title = "788. 헥사고날 아키텍처 어댑터 포트 매핑 구조"
date = "2026-03-15"
weight = 788
[extra]
categories = ["Software Engineering"]
tags = ["Architecture", "Hexagonal Architecture", "Ports and Adapters", "Decoupling", "Dependency Inversion", "Clean Architecture"]
+++

# 788. 헥사고날 아키텍처 어댑터 포트 매핑 구조

### # 헥사고날 아키텍처
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 알리스테어 코번(Alistair Cockburn)이 제안한 **포트와 어댑터(Ports and Adapters)** 패턴으로, 비즈니스 도메인의 순수한 로직(Core)을 외부 인프라(UI, DB, 외부 API)로부터 물리적·논리적으로 완전히 격리하여 기술 종속성을 제거하는 아키텍처 패러다임입니다.
> 2. **구조**: 시스템을 **Driving(주도)** 방향(입력)과 **Driven(피동)** 방향(출력)으로 대칭적으로 구성하고, 그 사이를 인터페이스인 **포트(Port)**로 연결하며, 구체적 기술 구현체는 **어댑터(Adapter)**가 담당하는 **의존성 역전(Dependency Inversion Principle)** 구현입니다.
> 3. **가치**: 인프라 변경(RDBMS에서 NoSQL로의 전환, Monolith에서 MSA로의 전환 등)에 대해 비즈니스 로직의 수정을 최소화하여 유지보수성을 극대화하고, 외부 리소스 없이 동작하는 **단위 테스트(Unit Test)**의 용이성을 통해 시스템의 신뢰성을 보장합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
전통적인 **계층형 아키텍처(Layered Architecture)**에서는 상위 계층이 하위 계층(DB, UI 프레임워크)을 직접 호출하므로, 하위 기술이 변경되면 상위 비즈니스 로직에까지 '파급 효과(Ripple Effect)'가 발생합니다. **헥사고날 아키텍처(Hexagonal Architecture)** 또는 **포트와 어댑터(Ports and Adapters)** 아키텍처는 이를 해결하기 위해, 애플리케이션을 하나의 독립적인 '육각형(헥사곤)' 코어로 간주합니다. 외부 세계와의 모든 상호작용은 코어가 정의한 명세서(포트)를 통해서만 이루어지며, 외부의 복잡한 기술 세계는 이 명세서에 맞춰 변환되는(어댑터) 구조입니다. 즉, **"기술이 도메인을 지배하지 않고, 도메인이 기술을 지배하는"** 구조를 실현합니다.

### 2. 등장 배경 및 비즈니스 요구
- **① 기존 한계**: EJB(Entity Java Beans)나 초기 Spring Framework 시절의 DB 중심 설계로 인해, 테스트를 위해 무거운 서버나 DB를 반드시 띄워야 하는 '느린 피드백' 문제와 ORM(Object-Relational Mapping) 객체가 도메인 로직을 오염시키는 문제 발생.
- **② 혁신적 패러다임**: 도메인 주도 설계(DDD: Domain-Driven Design)가 대두됨에 따라, 도메인 모델의 순수성을 지키고 외부 인프라와의 결합도를 낮추는 **결합도 분리(Decoupling)** 필요성 대두.
- **③ 현재 요구**: 클라우드 네이티브(Cloud Native) 환경에서 다양한 클라이언트(Web, Mobile, IoT)와 프로토콜(HTTP, gRPC, Message Queue)에 유연하게 대응하고, 마이크로서비스(MSA: Microservices Architecture)로의 전환을 용이하게 하려는 기술적 요구.

### 3. 💡 비유: 범용 전자기기와 여행용 어댑터
가장 이해하기 쉬운 비유는 '전자기기(노트북)'와 '국가별 전원 어댑터'입니다.
- **코어 (Core)**: 노트북 본체입니다. 전기(데이터)를 소비하여 일(비즈니스 로직)을 처리합니다. 나라가 바뀌어도 본체 기능은 변하지 않습니다.
- **포트 (Port)**: 노트북의 충전 단자입니다. USB-C나 barrel jack 등으로 표준화되어 있습니다. "이렇게 생긴 전기만 들어오면 충전한다"라는 규격(인터페이스)입니다.
- **어댑터 (Adapter)**: 한국, 미국, 유럽 등 각기 다른 모양의 콘센트(인프라)를 노트북의 포트에 맞춰 변환해 주는 '돼지코'입니다.
- **효과**: 미국(인프라 변경)으로 여행을 가더라도 노트북(코어)를 바꿀 필요 없이, 어댑터만 갈아끼우면 됩니다.

#### 📢 섹션 요약 비유
> "마치 세계 어디서나 사용할 수 있는 **'만능 충전기 규격(Port)'**을 노트북에 장착해두고, 나라마다 다른 콘센트 모양은 **'변환 플러그(Adapter)'**로 해결하는 것과 같습니다. 이를 통해 전압(기술 환경)이 바뀌어도 기기(비즈니스)는 고장 나지 않습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석

헥사고날 아키텍처는 **도메인**, **포트**, **어댑터**의 3계층으로 구성되며, 상세한 모듈과 역할은 다음과 같습니다.

| 구분 | 요소명 (Component) | 역할 및 내부 동작 | 프로토콜/인터페이스 | 비유 |
|:---:|:---|:---|:---|:---|
| **Domain** | **Domain Core** | 순수 자바(또는 언어) 객체로 구성된 비즈니스 로직. 외부 기술(Spring, JPA 등)에 대한 import가 없어야 함. | N/A (순수 로직) | 엔진 |
| **Port** | **Driving (Input) Port** | 코어가 제공해야 할 서비스의 명세. 인터페이스(Interface)로 정의되며 외부가 코어를 호출하는 진입점. `useCase` 등의 메서드 선언. | `interface OrderUseCase` | 입력 단자 |
| | **Driven (Output) Port** | 코어가 외부 세계에 무엇을 필요로 하는지의 명세. `save()`, `sendEmail()` 등의 추상 메서드를 정의. | `interface OrderRepository` | 출력 단자 |
| **Adapter** | **Primary (Input) Adapter** | 외부의 요청(HTTP, CLI)을 받아 **Driving Port**의 호출 형식으로 변환하여 코어에 전달. (Controller 역할) | REST API, gRPC, GraphQL | 리모컨 |
| | **Secondary (Output) Adapter** | **Driven Port** 인터페이스를 구현하여 실제 외부 인프라(MySQL, Kafka)와 연동. | JDBC, JPA, SMTP SDK | 케이블 |

### 2. 핵심 메커니즘: 제어 흐름 vs 의존성 방향
이 아키텍처의 핵심은 **"제어의 흐름(Control Flow)"과 "의존성의 방향(Dependency Direction)"을 분리**하는 데 있습니다.

- **제어의 흐름 (Runtime)**: 사용자의 입력은 `Input Adapter` → `Input Port` → `Core` → `Output Port` → `Output Adapter`로 흐릅니다. 소위 'Driving'과 'Driven'이 만나는 지점입니다.
- **의존성의 방향 (Compile Time)**: 모든 의존성은 외부에서 내부로 향합니다. `Core`는 아무것도 의존하지 않으며, `Adapter`가 `Core`를 의존합니다. 이를 **DIP (Dependency Inversion Principle)** 라고 하며, 이를 통해 `Core`를 외부 기술 변화로부터 보호합니다.

### 3. ASCII 아키텍처 구조 다이어그램
아래 다이어그램은 시스템의 내부(코어)와 외부(액츄에이터/인프라)를 구분한 헥사고날 구조를 도식화한 것입니다. 육각형의 외곽선이 바로 **포트(Port)**이며, 그 바깥에 붙은 사각형들이 **어댑터(Adapter)**입니다.

```text
      [ Primary Adapters (Driving Side) ]                    [ Secondary Adapters (Driven Side) ]
      ┌──────────────────────────────────┐                  ┌──────────────────────────────────┐
      │   REST Controller (Spring Web)   │                  │   MySQL Repository (JPA/Hibernate) │
      │      GraphQL Resolver            │                  │   MongoDB Client                 │
      │      CLI Runner                  │                  │   Kafka Message Producer         │
      └──────────────┬───────────────────┘                  └───────────────┬──────────────────┘
                     │      ▲                                          ▲     │
                     │      │ (Dependency)                              │     │ (Dependency)
      ┌──────────────┴──────┴──────────────────────────────────────────┴─────┴───────────────────┐
      │                     ▲                          ▲                                          │
      │                     │ (Call)                   │ (Call)                                   │
      │  [   INPUT PORTS (Driving Interface)  ] [ OUTPUT PORTS (Driven Interface)  ]              │
      │ ┌───────────────────────────────────┐ ┌───────────────────────────────────┐              │
      │ │  UseCase Interface (e.g. Order)   │ │  Repository Interface (e.g. Save) │              │
      │ └───────────────────────────────────┘ └───────────────────────────────────┘              │
      │                                                                             │
      │                         [ DOMAIN CORE (Hexagon) ]                            │
      │                  ┌─────────────────────────────────────┐                    │
      │                  │    Business Logic & Entities        │                    │
      │                  │    (No Dependencies on Outer World) │                    │
      │                  └─────────────────────────────────────┘                    │
      └───────────────────────────────────────────────────────────────────────────────┘
```

#### 다이어그램 해설
1. **중앙 헥사곤 (Domain Core)**: 가장 내부에 위치하며, 순수 비즈니스 규칙만을 포함합니다. 외부 라이브러리(Spring, JPA 등)를 import하지 않아 테스트 속도가 매우 빠르고 로직이 견고합니다.
2. **포트 (Ports)**: 헥사곤의 외곽선 역할을 합니다. 인터페이스(Interface)로만 존재하며, 코어가 외부와 소통하기 위한 '약속'입니다. 이를 통해 코어는 실제 구현체(MySQL인지 Kafka인지)를 알 필요가 없어집니다.
3. **어댑터 (Adapters)**: 헥사곤 외부에 위치합니다. 왼쪽(Primary)은 사용자의 입력을 받아 포트에 전달하는 '주도' 역할을, 오른쪽(Secondary)은 포트의 요구사항을 실제 기술로 구현하는 '피동' 역할을 수행합니다. 이 구조를 통해 기술 스택 교체가 발생해도 헥사곤 내부는 전혀 손대지 않고 어댑터만 교체하면 됩니다.

### 4. 심층 동작 원리 및 코드 예시
입력과 출력이 어떻게 포트를 통해 역전되는지 실무적인 Java 코드와 매핑하여 분석합니다.

- **A. Primary Adapter (Input) -> Port -> Core**
    1. `Controller`는 HTTP 요청을 받아 DTO(Data Transfer Object)를 변환합니다.
    2. `Controller`는 `UseCaseInputPort` 인터페이스의 `execute()` 메서드를 호출합니다.
    3. 실제 구현체는 `Core` 모듈 내부에 존재하며(DI에 의해 주입됨), 비즈니스 로직을 수행합니다.

- **B. Core -> Port -> Secondary Adapter (Output)**
    1. `Core` 로직 수행 중 영구 저장이 필요하면 `OutputPort` 인터페이스(예: `saveOrder()`)를 호출합니다.
    2. 런타임 시 이 인터페이스는 `Secondary Adapter`(예: `JpaOrderRepository`)로 연결되어 실제 DB에 SQL을 날립니다.

```java
// [Port Interface]: Core 모듈에 정의 (Core가 외부를 향해 요구하는 사항)
public interface OrderPersistenceOutputPort {
    void save(Order order); // SQL 같은 구체적 기술 언급 금지
}

// [Secondary Adapter]: Infrastructure 모듈에 구현 (기술적 세부사항)
@Repository
public class JpaOrderRepositoryAdapter implements OrderPersistenceOutputPort {
    private final SpringDataJpaRepository repo; // 실제 기술 의존
    @Override
    public void save(Order order) {
        // 도메인 모델 order를 JPA 엔티티로 변환하여 저장하는 로직
        repo.save(mapToEntity(order));
    }
}

// [Core Application Service]: Use Case 구현
public class OrderService {
    private final OrderPersistenceOutputPort outputPort; // 인터페이스에만 의존 (DIP 성립)
    
    public void processOrder(OrderCommand cmd) {
        Order order = new Order(cmd); // 비즈니스 로직
        outputPort.save(order);       // 추상화된 포트 호출
    }
}
```

#### 📢 섹션 요약 비유
> "자동차 **'엔진(코어)'**은 연료가 어디서 오는지, 바퀴가 어느 회사 제품인지 알 필요가 없습니다. 단지 연료를 넣는 **'주입구(Input Port)'**와 힘을 전달하는 **'축(Output Port)'**만 있으면 됩니다. 어떤 연료 펌프나 타이어(어댑터)를 달아도 엔진은 동일한 방식으로 작동합니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 정량적·구조적 심층 비교표
헥사고날 아키텍처를 대표적인 아키텍처 패턴인 **N-계층 아키텍처(N-Layered Architecture)** 및 **클린 아키텍처(Clean Architecture)**와 비교 분석합니다.

| 구분 | N-Layered Architecture | **Hexagonal Architecture (Ports & Adapters)** | Clean Architecture |
|:---|:---|:---|:---|
| **의존성 방향**| 상위 → 하위 (예: Controller → Service → DAO → DB) | **내부(Core) ← 외부(Adapter)** (DIP 엄수) | **내부(Entity) ← 외부** (Rule에 의존) |
| **DB(데이터)의 위치**| 최하위 계층으로, 로직이 DB에 강하게 의존 (Database Driven) | **외부(Adapter)**로 취급. 코어는 DB를 모름. (Database Ignorant) | **외부(Frameowrk)**로 취급. 인터페이스로 격리. |
| **테스트 용이성**| DB, Mock 라이브러리 필수. 무거운 통합 테스트 위주 | **Core 로직만 순수 자바로 단위 테스트 가능**. 가벼움. | Hexagonal과 유사하게 매우 높음. |
| **UI/프레임워크 교체**| 상위 계층부터 하위까지 전반적 리팩토링 필요 | Adapter 교체만으로 가능. **유지보수 비용 ↓** | UseCase 교체로 가능. |
| **