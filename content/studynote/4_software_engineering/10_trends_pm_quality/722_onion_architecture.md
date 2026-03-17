+++
title = "722. 어니언 아키텍처 도메인 코어 격리"
date = "2026-03-15"
weight = 722
[extra]
categories = ["Software Engineering"]
tags = ["Architecture", "Onion Architecture", "Domain Core", "Dependency Inversion", "DDD", "Software Design"]
+++

# 722. 어니언 아키텍처 도메인 코어 격리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 제프리 팔레르모(Jeffrey Palermo)가 제안한 아키텍처 패턴으로, 시스템의 중심에 **도메인 모델(Domain Model)**과 **도메인 서비스(Domain Service)**를 배치하고, 의존성 방향이 외부에서 내부로만 수렴하게 하여 **데이터베이스(DB), UI(User Interface), 프레임워크**와 같은 외부 인프라의 변화로부터 핵심 비즈니스 로직을 완벽히 격리하는 **의존성 역전(Dependency Inversion)** 기반의 격리 모델이다.
> 2. **가치**: 비즈니스 로직이 외부 기술 구현체에 의존하는 기존 계층형 아키텍처(Layered Architecture)의 한계를 극복하여, **유지보수성(Maintainability)**과 **테스트 용이성(Testability)**을 극대화하며, 기술 스택 교체 시 핵심 로직의 변경을 최소화하는 **높은 응집도(High Cohesion)**와 **낮은 결합도(Low Coupling)**를 실현한다.
> 3. **융합**: **DDD(Domain-Driven Design)**의 전술적 설계(Tactical Design)를 구조적으로 뒷받침하는 최적의 아키텍처 형태이며, SOLID 원칙 중 **OCP(Open-Closed Principle)**와 **DIP(Dependency Inversion Principle)**를 아키텍처 레벨에서 구현하는 표준으로, 마이크로서비스 아키텍처(MSA)의 내부 구조 설계에도 필수적으로 적용된다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**어니언 아키텍처 (Onion Architecture)**는 소프트웨어의 본질적인 가치인 '비즈니스 로직'이 특정 기술(데이터베이스, 웹 프레임워크 등)에 종속되는 것을 방지하기 위해 고안되었습니다. 전통적인 **N-티어 아키텍처(N-Tier Architecture)**에서는 상위 계층이 하위 계층(주로 DB)을 의존하게 되어, '데이터 중심 설계(Data-Oriented Design)'로 빠지기 쉽습니다. 반면, 어니언 아키텍처는 양파의 층처럼 가장 안쪽에 **도메인 코어(Domain Core)**를 위치시키고, 그外围를 인터페이스, 애플리케이션 서비스, 인프라스트럭처가 감싸는 형태를 취합니다. 이를 통해 '세부 구현(Infrastructure)'이 '핵심 추상화(Domain)'에 의존하도록 강제하여, 비즈니스 규칙의 순수성을 보장합니다.

### 2. 등장 배경 및 패러다임 변화
2008년경 제프리 팔레르모(Jeffrey Palermo)가 제시하며, 기존의 애플리케이션 개발이 데이터베이스 스키마(Database Schema) 설계에서 시작되는 안티패턴을 비판했습니다.
- **① 기존 한계**: 데이터베이스 테이블 구조가 엔티티를 결정하고, 비즈니스 로직이 저장 프로시저(Stored Procedure)로 묻히는 'DB-first' 방식은 비즈니스 변화에 둔감함.
- **② 혁신적 패러다임**: **DIP (Dependency Inversion Principle, 의존성 역전 원칙)**를 적용하여, 내부 계층(Core)이 인터페이스를 정의하고 외부 계층(Infrastructure)이 이를 구현함으로써 의존성의 방향을 뒤집음.
- **③ 비즈니스 요구**: 복잡한 도메인 로직을 처리하는 엔터프라이즈 애플리케이션에서, UI 변경이나 DB 교체가 핵심 로직에 영향을 주지 않아야 한다는 요구가 증대됨.

### 3. 구조적 비유 시각화

```text
                     [ Dependency Direction: Inward ↓ ]
      
      ┌─────────────────────────────────────────────────────────┐
      │    4. Infrastructure (UI, DB, External Services)        │  ← Outer Shell
      │    (Pluggable Details - 가장 자주 바뀌는 부분)           │
      │   ┌───────────────────────────────────────────────────┐ │
      │   │ 3. Application Services (Use Case Orchestrators)  │ │  ← Middle Shell
      │   │ (Workflow, Coordination - 담당자 역할)             │ │
      │   │ ┌─────────────────────────────────────────────┐   │ │
      │   │ │ 2. Domain Services Interfaces               │   │ │  ← Inner Shell
      │   │ │ (Business Contracts - 계약서)                │   │ │
      │   │ │ ┌─────────────────────────────────────┐     │   │ │
      │   │ │ │ 1. Domain Model (Entities, VOs)     │     │   │ │  ← Core Seed
      │   │ │ │ (Business Value - 진짜 가치)         │     │   │ │
      │   │ │ └─────────────────────────────────────┘     │   │ │
      │   │ └─────────────────────────────────────────────┘   │ │
      │   └───────────────────────────────────────────────────┘ │
      └─────────────────────────────────────────────────────────┘
```
*(도입 해설)*: 이 구조는 겉(Infrastructure)이 속(Core)을 알지만, 속(Core)은 겉을 알지 못합니다. 모든 의존성이 중심을 향해 뾰족하게 수렴하기 때문에, 중심의 변화는 최소화되고 외부의 변경이 중심에 영향을 줄 수 없습니다.

> **📢 섹션 요약 비유:**
> 마치 **수정 구슬(도메인 로직)**을 **비닐봉지(인터페이스)**에 넣고, 그 밖을 **신문지와 골판지(인프라)**로 겹겹이 감싼 뒤 테이프로 마무리하는 것과 같습니다. 겉포장(신문지, 골판지)이 찢어지거나 다른 재료로 바뀌어도 내용물인 수정 구슬은 언제나 깨끗하고 변하지 않은 상태로 유지됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 상세 구성 요소 (Component Breakdown)

어니언 아키텍처의 핵심은 '계층(Layer)'이 아닌 '원(Ring)'으로 이해하는 것입니다. 각 원은 서로 다른 책임과 수명 주기를 가집니다.

| 구성 요소 (Component) | 계층 위치 | 역할 (Role) | 내부 동작 및 특성 | 주요 프로토콜/요소 |
|:---|:---:|:---|:---|:---|
| **Domain Model** | **Center** | 비즈니스의 상태와 행위를 담는 **Entity** | **Data + Logic**. 기술적 독립성이 가장 강함. DB 컬럼과 1:1 매핑 금지. | 순수 POJO/POCO |
| **Domain Service Interface** | **Inner** | 도메인 모델에 속하기 애매한 로직 정의 | **Abstract Definition**. "무엇을 하는가(What)"만 정의. | 인터페이스 (Interface) |
| **Domain Service Implementation** | **Middle** | 도메인 서비스 인터페이스의 구현체 | **Concrete Logic**. 다만, 인프라 의존성을 여기서 주입받음. | 구현 클래스 (Class) |
| **Application Service** | **Middle** | 유스케이스(Use Case) 조율자 | **Orchestration**. 트랜잭션 경계 설정, 도메인 객체 간 협력 지휘. | Facade Pattern |
| **Infrastructure** | **Outer** | DB 접속, 외부 API 호출, 파일 I/O | **Details**. 구현체(RepositoryImpl)가 내부 인터페이스를 구현(DIP). | JDBC, REST API |

### 2. 의존성 역전(DIP)의 엄격한 적용

일반적인 **라이브러리 라이브러리(Library)** 관계와 달리, 어니언 아키텍처에서는 내부 모듈이 외부 모듈을 호출하지 않습니다. 대신 **제어의 역전(Inversion of Control, IoC)** 컨테이너(예: Spring Framework, .NET Core)를 통해 런타임에 의존성을 주입받습니다.

- **Source Code Snippet (Java Style)**:

```java
// 1. Core Domain Layer (가장 내부)
// 이 인터페이스는 DB에 대해 전혀 모릅니다.
public interface UserRepository {
    User findById(Long id);
    void save(User user);
}

// 2. Domain Entity
public class User {
    private String email;
    
    // 비즈니스 로직은 Entity 내부에
    public void changeEmail(String newEmail) {
        if (newEmail == null) throw new IllegalArgumentException("Email is required");
        this.email = newEmail;
    }
}

// 3. Infrastructure Layer (가장 외부)
// 내부의 인터페이스를 '구현(Implements)'함으로써 의존성이 역전됨.
@Repository // Spring Annotation
public class JpaUserRepositoryImpl implements UserRepository {
    @PersistenceContext
    private EntityManager em; // 기술적 세부사항 (Detail)

    @Override
    public User findById(Long id) {
        return em.find(User.class, id); // Hibernate/JPA 구현
    }
}
```

### 3. 데이터 흐름 및 상호작용 다이어그램

요청이 들어왔을 때, 데이터가 어떻게 흐르고 제어가 이동하는지 보여주는 상세 다이어그램입니다.

```text
    [ CLIENT (Browser/Mobile) ]
            │
            │ (1) HTTP Request (JSON)
            ↓
┌───────────────────────────────────────────────────────────────┐
│ OUTER RING: Infrastructure / UI                               │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ UserController (REST Controller)                          │ │
│ │ ▶ Endpoint: POST /users/{id}/email                       │ │
│ │ ▶ Deserialization: JSON → DTO                            │ │
│ └───────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
            │
            │ (2) Call Application Service
            ↓
┌───────────────────────────────────────────────────────────────┐
│ MIDDLE RING: Application Services                             │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ UserApplicationService                                    │ │
│ │ ▶ Transaction Management (@Transactional)                │ │
│ │ ▶ Validation (DTO → Domain Model Mapping)                │ │
│ │ ▶ Logic: user.changeEmail(newEmail);                     │ │
│ └───────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
            │
            │ (3) Invoke Domain Interface (Method Call)
            ↓
┌───────────────────────────────────────────────────────────────┐
│ INNER RING: Domain Services (Interfaces)                      │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ <<interface>> UserRepository                              │ │
│ │ ▶ Defines Contract: save(user)                           │ │
│ └───────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
            ▲
            │ (4) Concrete Implementation (Polymorphism)
            │
┌───────────────────────────────────────────────────────────────┐
│ OUTER RING: Infrastructure Implementation                     │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ JpaUserRepositoryImpl                                     │ │
│ │ ▶ INSERT INTO users ... (SQL Execution)                  │ │
│ └───────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```
*(도입 해설)*: 위 다이어그램에서 주목할 점은 `UserApplicationService`가 `JpaUserRepositoryImpl`을 직접 참조(`new` 키워드 사용)하지 않는다는 점입니다. `UserRepository` 인터페이스 타입 변수를 통해 간접적으로 참조하므로, 코드 레벨에서는 외부로 향하는 의존성 화살표가 존재하지 않습니다.

> **📢 섹션 요약 비유:**
> **식당 주방 시스템**과 같습니다. **고객(UI)**은 **웨이터(Application Service)**에게 주문합니다. 웨이터는 주방장(Domain Model)에게 "요리하라"고 지시합니다. 주방장은 레시피(Interface)에 따라 요리하지만, 그 레시피를 실행하는 주방 도구가 **믹서기(Infra-DB A)**이든 **칼(Infra-DB B)**이든 상관하지 않습니다. 웨이터와 주방장은 믹서기가 고장 나서 **블렌더로 교체**되어도 영향을 받지 않습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 경쟁/유사 아키텍처 심층 분석

어니언 아키텍처는 다른 유명한 아키텍처 패턴과 근본적으로 같은 뿌리를 공유하지만, 강조점에 미묘한 차이가 있습니다.

| 비교 항목 | **어니언 아키텍처 (Onion)** | **클린 아키텍처 (Clean)** | **헥사고날 아키텍처 (Hexagonal)** |
|:---|:---|:---|:---|
| **핵심 메타포** | **층위(Ring)의 집중** | **방사형 계층 & 경계** | **포트(Port) & 어댑터(Adapter)** |
| **강조점** | 도메인 모델과 엔티티의 **보호** | 엔티티를 중심으로 한 **규칙 격리** | 외부 연동의 **대칭성** (입력/출력) |
| **의존성 방향** | 안쪽으로 수렴 (Inside-In) | 안쪽으로 수렴 (Inside-In) | 바깥쪽 어댑터가 포트로 의존 (Inward) |
| **UI/DB 위치** | 가장 바깥쪽 껍질 (Detail) | 가장 바깥쪽 (Interface Adapters) | Infrastructure Adapter (Plugin) |
| **주요 사용처** | 전통적 웹 애플리케이션, 엔터프라이즈 | 복잡한 플러그인 시스템 | 독립적인 모듈형 시스템, MSA |

### 2. 타 과목 융합 및 시너지 (OS/네트워크/AI)

- **① 데이터베이스 (DB) 관점**: ORM(Object-Relational Mapping) 기술(JPA, Hibernate 등)이 필수적입니다. 도메인 객체가 DB 스키마와 1:1 대응되는 것을 방지하기 위해, **Lazy Loading(지연 로딩)** 전략과 영속성 컨텍스트(Persistence Context)의 라이프사이클을 아키텍처 경계 밖(Infrastructure)으로 캡슐화해야 합니다.
- **② 운영체제 (OS) 및 네트워크 관점**: 각 계층의 분리는 **프로세스간 통신(IPC)*