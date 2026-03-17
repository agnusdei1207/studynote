+++
title = "721. 클린 아키텍처 Usecase Interactor 설계"
date = "2026-03-15"
weight = 721
[extra]
categories = ["Software Engineering"]
tags = ["Architecture", "Clean Architecture", "Uncle Bob", "UseCase", "Interactor", "Dependency Rule", "Decoupling"]
+++

# 721. 클린 아키텍처 Usecase Interactor 설계

### # 핵심 인사이트 (3줄 요약)
> 1. **본질**: Robert C. Martin(Uncle Bob)이 정립한 **클린 아키텍처 (Clean Architecture)**의 핵심 컴포넌트인 **인터랙터 (Interactor)**는, UI, DB, 프레임워크 등 외부 인프라의 변화로부터 **비즈니스 로직 (Business Logic)**을 철저히 보호하는 의존성 역전의 요새입니다.
> 2. **메커니즘**: **SOLID 원칙 (SOLID Principles)** 중 **SRP (Single Responsibility Principle, 단일 책임 원칙)**와 **DIP (Dependency Inversion Principle, 의존성 역전 원칙)**를 기반으로, 특정 유스케이스(Use Case)의 실행 순서를 오케스트레이션(Orchestration)하며 데이터를 변형하지 않고 흐름을 제어합니다.
> 3. **가치**: 도메인 로직에 대한 단위 테스트(Unit Test)의 용이성을 극대화하고, 기술 스택의 교체나 마이그레이션 시 **재사용 가능한(Reusable)** 애플리케이션 코어를 형성하여 시스템의 수명을 연장합니다.

---

### Ⅰ. 개요 (Context & Background)

**클린 아키텍처 (Clean Architecture)**는 소프트웨어의 복잡도를 관리하기 위해 계층(Layer)을 분리하고 의존성의 방향을 제어하는 설계 패러다임입니다. 전통적인 **계층형 아키텍처 (Layered Architecture)**나 **N-Tier 아키텍처**가 상위 계층이 하위 계층(주로 데이터베이스)을 의존함으로써 데이터 중심의 설계로 퇴보하기 쉬운 반면, 클린 아키텍처는 비즈니스의 핵심 규칙인 **엔티티 (Entity)**와 **유스케이스 (Use Case)**가 가장 내부에 위치하며, 외부 요소(UI, Framework, DB)가 이 내부 계층을 의존하도록 조작합니다.

이 설계의 핵심 목적은 **"프레임워크의 종속성에서 벗어나는 것"**입니다. Spring, Django, React와 같은 특정 프레임워크나 도구는 도구일 뿐이며, 도구가 바뀐다고 해서 비즈니스의 본질이 바뀌어서는 안 됩니다. 이를 위해 아키텍처는 **의존성 규칙 (Dependency Rule)**을 엄격히 준수하여, 소스 코드 의존성은 반드시 안쪽(고수준 정책)으로만 향하도록 강제합니다.

```text
      [ 전통적인 계층형 아키텍처의 딜레마 ]
      
      UI Layer ──▶ Business Logic ──▶ Data Access Layer ──▶ Database
          │              │                   │
          └── 의존성 ────┴──── 의존성 ────────┘
      
      (문제) Business Logic이 Data Access Layer를 의존하므로,
            DB 스키마가 바뀌면 비즈니스 로직까지 수정해야 하는 'Domino Effect' 발생.
      
      [ 클린 아키텍처의 해결책 ]
      
      Frameworks ──▶  Interface Adapter  ──▶  Use Cases (Interactor)  ──▶  Entities
         (Detail)      (Boundary)            (Application Business)      (Enterprise)
      
      (해결) 화살표(의존성)가 안쪽으로만 향함.
            DB나 UI가 바뀌어도 Interactor와 Entity는 영향을 받지 않음 (Zero Side-Effect).
```

이 구조에서 **인터랙터 (Interactor)**는 애플리케이션의 **"행동의 중재자"**로서, 구체적인 기술 구현체(DTO, DB Model)가 아닌 인터페이스(Port)를 통해 대화합니다.

**📢 섹션 요약 비유:** 마치 건물을 지을 때, 전기 배선이나 파이프(인프라)가 바뀌더라도 건물의 구조 설계도(아키텍처)나 거주 목적(비즈니스)은 바뀌지 않아야 하듯이, 소프트웨어 또한 **'살아있는 유기체'처럼 내부 장기(비즈니스 로직)를 보호하는 피부와 근육(어댑터)으로 감싸야 하는 것과 같습니다.**

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석 (Component Table)

클린 아키텍처의 유스케이스 계층은 주로 **인터랙터(Interactor)**로 구현됩니다. 이를 둘러싼 주요 구성 요소와의 상호작용은 다음과 같습니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/형식 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Input Boundary (Input Port)** | 유스케이스의 진입점 인터페이스 | Controller로부터 요청을 받는 계약(Contract) 역할 | Interface Method | 은행 창구의 접수 창구 |
| **Interactor** | **유스케이스 구현체 (Core)** | 비즈니스 흐름 제어, Entity 조작, 유효성 검사 수행 | Class (implements Input Port) | **집행 관료** (실무 처리자) |
| **Output Boundary (Output Port)** | 결과 전달 인터페이스 | Interactor가 계산한 결과를 외부(Presenter)로 전달 | Interface (Callback/Publisher) | 결과 통지서 발송부 |
| **Entity** | 핵심 비즈니스 규칙 | Interactor의 요청에 따라 스스로 상태를 변경하거나 검증 | Plain Object (POJO/POCO) | 법률/규정 (교과서) |
| **Repository (Impl)** | 데이터 접근 어댑터 (DIP 적용) | Output Boundary를 구현하여 실제 DB I/O를 수행 | Class (implements Output Port) | 창고지기 (DB 담당) |

#### 2. 인터랙터 (Interactor)의 의존성 역전 메커니즘

인터랙터가 "외부로부터 독립적"이기 위해서는 구체적인 클래스가 아닌 **추상화(Abstraction)**에 의존해야 합니다. 이를 위해 **REQ-RES 모델 (Request-Response Model)**을 사용합니다. 이 모델은 프레임워크의 모델(HttpRequest, JPA Entity 등)가 아닌, 순수한 데이터 구조체(POJO)를 사용하여 계층 간의 결합도를 제거합니다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                   [ Interactor Dependency Flow Diagram ]                     │
│                                                                              │
│   ┌──────────────┐         Use Case Specific          ┌──────────────┐      │
│   │ Controller   │   (Input Boundary Interface)       │ Presenter    │      │
│   │  (Driver)    │◀──────────────────────────────────▶│  (Display)   │      │
│   └──────┬───────┘                                     └──────▲───────┘      │
│          │ Request Model (POJO)                           │ Response Model   │
│          │                                               │ (POJO)           │
│          ▼                                               │                  │
│   ┌───────────────────────────────────────────────────────────────────┐     │
│   │                    [ INTERACTOR (Use Case) ]                       │     │
│   │   ┌────────────────────────────────────────────────────────────┐   │     │
│   │   │  1. Validate Input Data (Input Boundary 인터페이스 확인)      │   │     │
│   │   │  2. Call Repository (Output Boundary 인터페이스 통해 조회)  │   │     │
│   │   │  3. Execute Business Logic (Entity 메서드 호출 및 규칙 적용)  │   │     │
│   │   │  4. Prepare Result (결과를 Response Model로 변환)            │   │     │
│   │   │  5. Call Output Port (Presenter/DB로 결과 전송)              │   │     │
│   │   └────────────────────────────────────────────────────────────┘   │     │
│   └───────────────────────────────────────────────────────────────────┘     │
│          │ ^                                           │ ^                │
│          │ | Dependency (DIP)                          | |                │
│          ▼ | (Interactor depends on Interfaces, not Impl)│                │
│   ┌───────┴────────────────────────────────────────────┴───────┐          │
│   │          [ Interface Adapters (Repositories ) ]            │          │
│   │  (Implement Output Boundary / Called by Interactor)        │          │
│   └────────────────────────────────────────────────────────────┘          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**[해설]**:
위 다이어그램에서 화살표(의존성)는 Interactor에서 외부로 향하지만, 실제 소스 코드 상의 의존성(Import 문)은 반대입니다. Interactor는 `InputPort`와 `OutputPort`라는 인터페이스만 바라보며, 구체적인 `DbRepository`나 `JsonPresenter`를 모릅니다. 이로써 **"무엇을(What)"** 하는지는 Interactor가 결정하고, **"어떻게(How)"** 처리하는지는 외부 구현체에 위임하는 관계가 성립됩니다.

#### 3. 핵심 코드 구현 예시 (Pseudo Java)

```java
// 1. Input Boundary (Interface) - 외부로부터 들어오는 계약
public interface RegisterMemberInputPort {
    void registerMember(RegisterMemberRequest request);
}

// 2. Output Boundary (Interface) - 내부에서 외부로 나가는 계약
public interface RegisterMemberOutputPort {
    void presentSuccess(MemberResponse response);
    void presentError(ErrorMessage error);
}

// 3. Interactor - 순수 비즈니스 로직 구현
public class RegisterMemberInteractor implements RegisterMemberInputPort {
    private final MemberRepository memberRepo; // Interface (DIP)
    private final RegisterMemberOutputPort presenter; // Interface (DIP)
    private final MemberFactory memberFactory; // Domain Logic

    @Override
    public void registerMember(RegisterMemberRequest request) {
        // ① 데이터 정합성 검사 (Validation)
        if (request.getEmail() == null || !request.getEmail().contains("@")) {
            presenter.presentError(new ErrorMessage("Invalid Email"));
            return;
        }

        // ② 중복 확인 (Domain Rule)
        if (memberRepo.existsByEmail(request.getEmail())) {
            presenter.presentError(new ErrorMessage("Duplicate Email"));
            return;
        }

        // ③ 엔티티 생성 및 비즈니스 로직 수행
        Member newMember = memberFactory.create(request.getName(), request.getEmail());
        
        // ④ 영속화 (Interface를 통한 호출)
        memberRepo.save(newMember);

        // ⑤ 결과 전달 (Interface를 통한 호출)
        presenter.presentSuccess(new MemberResponse(newMember.getId()));
    }
}
```

**📢 섹션 요약 비유:** 인터랙터는 **"요리사(Chef)"**와 같습니다. 손님(Controller)의 주문을 받으면, 냉장고(Repository)에서 식재료를 꺼내지만 냉장고의 제조사가 어딘지는 관심 없습니다. 레시피(비즈니스 규칙)에 따라 요리한 뒤, 그릇에 담아 웨이터(Presenter)에게 내어놓기만 하면 됩니다. 주방 설계가 어떻든, 요리사의 실력(코드)만 있다면 어디서든 맛있는 음식을 만들 수 있듯이, 인터랙터는 어느 환경에서도 동작할 수 있어야 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 아키텍처 패턴 심층 비교 (Comparison Matrix)

| 구분 | MVC (Model-View-Controller) | 전통적인 N-Tier / Layered | **Clean Architecture (UseCase)** |
|:---|:---|:---|:---|
| **의존성 방향** | Triadic (양방향 의존 가능) | Top-down (위→아래) | **Inside-out (안쪽←바깥쪽)** |
| **비즈니스 로직 위치** | Model에 산재 (Anemic Domain Model 위험) | Service Layer (DB에 의존 가능성 높음) | **Interactor (완전 고립)** |
| **테스트 용이성** | 프레임워크 컨텍스트 필요 | DB Mocking 등 복잡한 설정 필요 | **순수 로직 테스트 가능 (Mock 용이)** |
| **관심사 분리** | Controller에 로직 침투 가능 | Service가 God Object화 될 위험 | **단일 책임(SRP) 준수, 1개의 Interactor = 1개의 행동** |
| **변경 비용** | UI 변경 시 Model 영향 가능 | DB 변경 시 Service/Domain 영향 | **UI/Framework 교체 시 Interactor 재사용 100%** |

#### 2. 타 기술 영역과의 융합 시너지

**1) DDD (Domain-Driven Design)와의 결합**
클린 아키텍처의 Interactor는 DDD의 **애플리케이션 서비스 (Application Service)** 계층에 정확히 대응합니다. **엔티티 (Entity)**와 **값 객체 (Value Object)**는 도메인의 본질을 담고 있고, 인터랙터는 이들을 조합하여 유스케이스를 완성합니다. 이때 **유비쿼터스 언어 (Ubiquitous Language)**를 사용하여 Interactor의 메서드명을 정의하면(예: `placeOrder`, `reserveStock`), 코드가 곧 문서가 되는 효과를 낳습니다.

**2) 테스트 주도 개발 (TDD)과의 시너지**
인터랙터는 **순수 자바/코틀린 코드**로 작성됩니다. 즉, Spring Context나 Web Server 없이도 **JUnit**만으로 실행 속도가 0.1초 이내인 단위 테스트를 작성할 수 있습니다. 이는 개발 생산성을 극대화하고, 리팩토링 시 안전망이 됩니다.

**3) 마이크로서비스 아키텍처 (MSA)로의 확장**
규모가 커질 경우 Interactor는 **Bounded Context (한계 문맥)** 경계가 됩니다. Interactor의 `OutputPort`를 HTTP Client로 구현하면, 자연스럽게 다른 서비스와의 통신 로직으로 변환되어 MSA로의 전이가 매끄러워집니다.

**📢 섹션 요약 비유:** 기존 레고 블록(모놀리식)은 위에 하나만 붙이면 아래가 무너질까 두려워 계산해야 하지만, 클린 아키텍처는 **"자기장에 뜨는 독립된 모듈"**들을 조립하는 것과 같습니다. 각 모듈(Interactor)은 독립된 발전기를 가지고 있어 전력 공급(의존성)이 끊겨도 혼자서 작동할 수 있는 자급자족 시스템과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 도입 체크