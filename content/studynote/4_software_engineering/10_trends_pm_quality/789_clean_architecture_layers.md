+++
title = "789. 클린 아키텍처 엔티티 유스케이스 프레젠테이션 계층 분리"
date = "2026-03-15"
weight = 789
[extra]
categories = ["Software Engineering"]
tags = ["Architecture", "Clean Architecture", "Entity", "Use Case", "Presentation", "Dependency Rule", "Design Pattern"]
+++

# 789. 클린 아키텍처 엔티티 유스케이스 프레젠테이션 계층 분리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어의 수명을 결정짓는 핵심 비즈니스 로직(Enterprise Business Rules)을 외부의 변덕스러운 환경(UI, DB, Framework)으로부터 **격리(Isolation)**하여, 시스템의 본질적인 가치를 보존하는 성벽과 같은 내부 구조를 설계하는 전략이다.
> 2. **의존성 규칙 (Dependency Rule)**: 모든 소스 코드 의존성은 반드시 저수준의 구체적 세부 사항(DB, Web Framework)에서 고수준의 추상화된 정책(Policy) 방향으로만 향하도록 강제하며, 이는 **DIP (Dependency Inversion Principle, 의존성 역전 원칙)**을 아키텍처적 차원으로 확장한 것이다.
> 3. **가치**: 프레임워크의 라이프사이클이 종료되거나 UI가 모노리스(Monolithic)에서 MSA (Microservices Architecture)로 전환되더라도, 순수 비즈니스 로직은 단 한 줄의 수정도 없이 재사용됨으로써 시스템의 유지보수성(Maintainability)과 테스트 용이성(Testability)을 극대화한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 정의 및 철학
**클린 아키텍처 (Clean Architecture)**는 로버트 C. 마틴(Robert C. Martin)이 제창한 소프트웨어 설계 철학으로, 관심사의 분리(Separation of Concerns)를 가장 radical하게 수행하는 패러다임입니다. 여기서 '계층'의 핵심은 단순한 수평적 분리가 아니라, **'의존성의 방향 제어'**입니다. 전통적인 **N-Tier 아키텍처 (N-Layer Architecture)**가 계층 간의 느슨한 결합을 꾀하지만 여전히 상위 계층이 하위 계층(DB, Util)을 바라보는 수직적 구조를 가진 반면, 클린 아키텍처는 의존성이 내부로 향하는 동심원 구조를 가집니다.

### 2. 등장 배경: 스파게티 코드와 기술 부채의 위기
① **기존 한계**: 비즈니스 로직이 SQL (Structured Query Language) 쿼리나 HTTP (Hypertext Transfer Protocol) 요청 처리 로직과 뒤엉켜 있어, UI 변경 시 DB 로직까지 영향을 받는 '바람직 않은 결합'이 발생했습니다.
② **혁신적 패러다임**: 프로그램의 **"주인(UI, DB)"**과 **"배우(Business Logic)"**을 분리하여, 배우(핵심 로직)가 무대(UI)나 소품(DB)이 바뀌어도 연기(로직)를 유지할 수 있도록 만드는 **'Plug-in Architecture'** 개념이 도입되었습니다.
③ **현재 비즈니스 요구**: 도메인 주도 설계(DDD, Domain-Driven Design)와 MSA 환경에서는 도메인 로직의 순수성이 생존이 걸린 문제이며, 클린 아키텍처는 이를 보장하는 표준적인 구조적 틀로 자리 잡았습니다.

### 3. ASCII 다이어그램: 관심사의 분리와 의존성 방향

```text
       [Source Code Dependencies Direction ( ---> )]

      +---------------------------------------------------------------------+
      |                          WEB/DATABASE LAYER                          |
      |  (UI, DB, Frameworks, Devices - Most volatile details)               |
      |                                                                       |
      |    +------------------------------------------------------------+    |
      |    |                  INTERFACE ADAPTERS LAYER                   |    |
      |    |   (Controllers, Presenters, Gateways - Data conversion)     |    |
      |    |                                                            |    |
      |    |    +-------------------------------------------------+    |    |
      |    |    |           USE CASES LAYER (Application)           |    |    |
      |    |    |  (Specific Business Rules for Application)        |    |    |
      |    |    |                                                 |    |    |
      |    |    |    +---------------------------------------+    |    |    |
      |    |    |    |        ENTITIES LAYER (Core)          |    |    |    |
      |    |    |    |  (General Enterprise Business Rules)   |    |    |    |
      |    |    |    |                                       |    |    |    |
      |    |    |    +---------------------------------------+    |    |    |
      |    |    |                   ^   ^   ^   ^   ^   ^   |    |    |    |
      |    |    |                   |   |   |   |   |   |   |    |    |    |
      |    |    +-------------------|---|---|---|---|---|---|----+    |    |
      |    |                        |   |   |   |   |   |   |         |    |
      |    +------------------------|---|---|---|---|---|---|---------+    |
      |                             |   |   |   |   |   |   |              |
      +-----------------------------|---|---|---|---|---|---|--------------+
                                    |   |   |   |   |   |   |
                                    v   v   v   v   v   v   v
                          "Dependency Rule: Source code dependencies 
                           can only point inwards."
```
> **해설**: 위 다이어그램은 소스 코드 의존성의 흐름을 시각화한 것입니다. 가장 바깥쪽의 상세한 기술 요소(UI, DB)들이 안쪽의 추상화된 비즈니스 규칙을 의존합니다. 이 화살표가 역전되는 순간(예: Entity가 DB 클래스를 Import), 아키텍처는 무너지고 기술 부채가 발생합니다.

### 📢 섹션 요약 비유
> "마치 스마트폰을 바꿀 때마다(앱/OS 변경) 우리의 연락처, 사진, 메모(데이터/로직)가 클라우드에 안전하게 백업되어 있어서, 기계만 교체하면 동기화되는 것과 같습니다. 앱의 껍데기(Presentation)가 바뀌더라도 생명 정보(Entities)는 변하지 않아야 합니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석 (Deep Component Analysis)

| 구성 요소 (Component) | 계층 | 내부 동작 및 역할 | 주요 프로토콜/포맷 | 대표적 모듈 예시 |
|:---:|:---:|:---|:---:|:---|
| **Entities** | Core | **전사적 핵심 규칙**. 애플리케이션에 독립적인 순수한 객체. 'VO (Value Object)'나 독립적인 'Domain Model'로 존재하며, 외부 상태에 의존하지 않는 고유의 로직 수행. | Java/Kotlin Class, JSON Schema | `User`, `Order`, `Account` |
| **Use Cases** | App | **애플리케이션별 흐름 제어**. Entities를 조합하여 특정 유스케이스(예: "결제하기")를 수행하는 Orchestrator 역할. 입력 데이터 검증 및 출력 포맷 결정. | DTO (Data Transfer Object) | `CreateOrderInteractor`, `RegisterUser` |
| **Presenters/Controllers** | Interface | **데이터 변환 및 중계**. 외부(혹은 내부)의 데이터 포맷을 변환. Use Case에서 나온 결과를 UI가 이해할 수 있는 **ViewModel**로 변환하는 역할. | JSON, XML, View Models | `OrderPresenter`, `OrderController` |
| **Frameworks & Drivers** | Outer | **기술적 세부 사항**. DB 엔진, Web Framework(UI), Queue 등 실무적인 통신을 담당. 추상화된 인터페이스(Interface)를 구현(Implement)한다. | SQL, HTML, REST, gRPC | `HibernateImpl`, `SpringController` |

### 2. 심층 동작 원리: 요청의 흐름 (Crossing the Boundaries)
시스템의 동작은 외부의 요청이 내부의 규칙을 건드린 뒤 다시 외부로 나가는 **'Round-trip'** 과정입니다.

1.  **① Request (요청)**: 사용자가 웹 브라우저(Presentation)에서 '주문하기' 버튼 클릭.
2.  **② Input Boundary (입력 경계)**: `Controller`는 HTTP 요청을 수신하여 JSON을 `Input Data` 객체로 변환하고, `Use Case Input Port` 인터페이스의 `execute()` 메서드를 호출.
3.  **③ Use Case Execution (유스케이스 수행)**: `Interactor`는 입력 유효성을 검사하고, `Entity`의 상태를 변경하거나 조회. (이때 DB에 직접 접근하지 않고 `Gateway` 인터페이스 사용).
4.  **④ Entity Logic (엔티티 로직)**: `Entity`는 재고 확인, 주문 생성 등의 핵심 비즈니스 규칙 수행.
5.  **⑤ Output Boundary (출력 경계)**: `Interactor`는 결과를 `Output Data` 포맷에 담아 `Presenter` 인터페이스로 반환.
6.  **⑥ Response (응답)**: `Presenter`는 데이터를 ViewModel로 변환하여 `View`에게 렌더링 지시.

### 3. 핵심 알고리즘 및 코드 스니펫 (The Interactor Pattern)
아래는 **Java**를 사용한 유스케이스 계층과 엔티티 계층의 상호작용 예시입니다. 의존성 역전이 코드 수준에서 어떻게 적용되는지 보여줍니다.

```java
// [Use Case Layer]
// 비즈니 로직은 Interface에만 의존합니다. (DIP 적용)
public class OrderInteractor implements InputBoundary {
    private final OutputBoundary outputBoundary; // Presenter 인터페이스
    private final EntityGateway orderGateway;    // DB 접근 추상화
    private final UserGateway userGateway;

    public OrderInteractor(OutputBoundary ob, EntityGateway og, UserGateway ug) {
        this.outputBoundary = ob;
        this.orderGateway = og;
        this.userGateway = ug;
    }

    @Override
    public void execute(OrderRequestData request) {
        // 1. 데이터 로드 (Gateway 통해 접근)
        User user = userGateway.getUser(request.getUserId());
        
        // 2. Entity 로직 수행 (핵심 규칙)
        // Entity 내부에 복잡한 주문 가능 여부 로직이 캡슐화됨.
        Order newOrder = user.createOrder(request.getItems()); 
        
        // 3. 결과 저장
        orderGateway.save(newOrder);

        // 4. Presenter로 전달 (상세 구현은 모름)
        outputBoundary.present(new OrderResponseData(newOrder.getId(), "SUCCESS"));
    }
}

// [Entity Layer]
// 외부 무관한 순수 자바 객체 (POJO)
public class User {
    private UserId id;
    private boolean isBlacklisted;

    // 비즈니스 핵심 규칙
    public Order createOrder(List<Item> items) {
        if (this.isBlacklisted) {
            throw new IllegalStateException("Blacklisted users cannot create orders.");
        }
        // 할인율 적용 로직 등 고도화된 도메인 로직이 여기에 위치.
        return new Order(this.id, items);
    }
}
```

### 4. ASCII 다이어그램: 데이터 흐름 및 경계 횡단 (Data Flow & Boundary Crossing)

```text
      +------------------+          +-------------------------+          +------------------+
      |   UI / FRAMEWORK |          |    USE CASE LAYER       |          |    ENTITY LAYER  |
      | (Controller/View)|          |  (Interactor / Orchestrator)     |  (Domain Model)   |
      +------------------+          +-------------------------+          +------------------+
              |                                |                              |
   ① Request  |   DTO / Primitive              |                              |
   (JSON)     |------------------------------> |                              |
              |                                |                              |
              |                                |   ② Call Domain Logic        |
              |                                |---------------------------->|
              |                                |                              |
              |                                |   ③ Return Result           |
              |                                |<----------------------------|
              |                                |                              |
              |   ViewModel / Response         |                              |
   ④ Display | <------------------------------|                              |
   (HTML/JSON)|                                |                              |
```

> **해설**: 이 다이어그램은 사용자의 요청이 외부 계층에서 내부의 유스케이스와 엔티티를 거쳐 다시 외부로 나가는 흐름을 보여줍니다. 중요한 점은 **Entity가 Use Case를**, **Use Case가 Presenter를** 알지 못한다는 것입니다. 모든 의존성은 화살표의 반대 방향, 즉 안쪽으로 향해 있습니다.

### 📢 섹션 요약 비유
> "햄버거 프랜차이즈의 **'매뉴얼(Entities)'**은 세계 어디서나 똑같습니다. 점장(Use Case)이 바뀌거나, 키오스크(Presentation)가 도입되거나, 조리 기구(Framework)가 바뀌어도 **'패티 굽는 시간과 소스 레시피'**는 변하지 않습니다. 본질을 둘러싼 겉포장들이 어떻게 바뀌든 본질을 지키는 것이 핵심입니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: Traditional Layered vs Clean Architecture

| 비교 항목 | **전통적 계층형 아키텍처 (Traditional Layered)** | **클린 아키텍처 (Clean Architecture)** |
|:---|:---|:---|
| **의존성 방향** | **상위 -> 하위 (Presentation -> Business -> Data)**<br>비즈니스 계층이 데이터 접근 계층(DAO)을 직접 호출/의존. | **하위 -> 상위 (Outer -> Inner)**<br>의존성 역전(DIP)을 통해 모든 의존성이 Core를 향함. |
| **DB의 관점** | **핵심 구성 요소**: DB 스키마가 도메인 모델을 지배함 (Anemic Domain Model). | **세부 사항(Detail)**: DB는 단순한 저장소이며, 도메인 로직과 무관하게 교체 가능. |
| **테스트 용이성** | 낮음. DB 연결 없이는 비즈니스 로직 테스트가 어려움 (Mocking 복잡). | 극대화. 인터페이스만 있으면 순수 자바/파이썬 객체로 유닛 테스트 가능. |
| **프레임워크 종속성** | 강함. Spring, EJB 등 프레임워크의 라이프사이클에 종속됨. | 최소화. 핵심 로직은 `main()` 함수만으로도 실행 가능해야 함. |

### 2. 과목 융합 관점 (Convergence)
클린 아키텍처는 단순한 소프트웨어 공학 이론을 넘어 타 영역과의 시너지를 창출합니다.

1.  **DB/컴퓨터 구조 (Database & System Architecture)**
    -   **퍼시스턴스 무시 (Persistence Ignorance)**: 엔티티 계층은 데이터가 메모리(RAM)에 있는지, 디스크(RDBMS)에 있는지, NoSQL에 있는지 전혀 알지 못해야 합니다. 이는 **OS의 가상 메모리(Virtual Memory)** 개념과 유사합니다. 프로세스는 물리적 메모리 주소를 몰라도 논리적 주소로 접근하듯, 비즈니스 로직은 물리적 저장소를 몰라도 논리적 도메인 모델로 접근해야 합니다.
    -   **성능 고려