+++
title = "205-211. 주요 아키텍처 패턴 (Layered, MVC, MVVM)"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 205
+++

# 205-211. 주요 아키텍처 패턴 (Layered, MVC, MVVM)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어의 복잡도를 통제하기 위해 **관심사의 분리 (Separation of Concerns)** 원칙을 아키텍처 수준으로 구현한 패턴들입니다.
> 2. **가치**: 계층형 아키텍처는 수평적 분리를 통해 **의존성 역전**을 실현하고, MVC/MVVM은 UI 로직의 **수직적 분리**를 통해 단위 테스트 가능성과 재사용성을 극대화합니다.
> 3. **융합**: 현대 MSA (Microservice Architecture)와 SPA (Single Page Application)의 기반이 되며, 클라우드 네이티브(Cloud Native) 환경에서 모듈 경계를 명확히 하는 필수 설계 전략입니다.

---

### Ⅰ. 개요 (Context & Background)

**아키텍처 패턴(Architecture Pattern)**이란 소프트웨어 시스템의 구조를 결정하는 구조적인 틀로, 단순한 코드 스타일을 넘어 시스템의 전체적인 뼈대와 조직 원칙을 정의합니다. 소프트웨어 공학의 역사는 **모듈화(Modularity)**와 **추상화(Abstraction)**를 통해 복잡성을 관리해 온 과정이며, 이를 실현하는 대표적인 수단이 바로 계층형 아키텍처와 UI 디자인 패턴입니다.

과거의 단일형(Monolithic) 애플리케이션은 UI, 로직, 데이터가 한데 얽혀 있어, 작은 변경 사항이 시스템 전체에 **파급 효과(Side Effect)**를 미쳤습니다. 이를 해결하기 위해 **N-tier 아키텍처**가 등장하여 수평적 분리를 이루었고, 동시에 인터랙티브한 데스크톱 및 웹 애플리케이션의 발전과 함께 MVC(Model-View-Controller) 패턴이 탄생하여 UI와 비즈니스 로직의 수직적 분리를 이끌어냈습니다. 현재는 MVVM(Model-View-ViewModel)과 같은 데이터 바인딩(Data Binding) 기반 패턴이 리액티브(Reactive) 프로그래밍과 결합하여 주류를 이루고 있습니다.

> **💡 비유**: 건물을 지을 때, **계층형 아키텍처**는 지하층(인프라), 1층(로비), 2층(사무실)으로 기능을 분리하여 배관과 전기를 정리하는 것이고, **MVC/MVVM**은 식당에서 주방(데이터), 홀(화면), 주문 직원(제어)의 역할을 나누어 혼선 없이 서빙하는 것과 같습니다.

**📢 섹션 요약 비유**: 고층 빌딩을 지을 때 기능별 층을 구분하여 배관을 정리하는 것(계층형)과, 대형 식당에서 주방과 서빙 직원의 역할을 철저히 분리하여 혼선을 막는 것(MVC)이 아키텍처 패턴의 핵심입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

아키텍처 패턴은 크게 시스템 전체를 수평적으로 자르는 **레이어드 아키텍처(Layered Architecture)**와 UI 계층을 세밀하게 다루는 **MVC 계열 패턴**으로 나눌 수 있습니다.

#### 1. 구성 요소 및 비교

| 구분 | 요소명 | 역할 | 내부 동작 | 주요 프로토콜/기술 | 비유 |
|:---:|:---|:---|:---|:---|:---|
| **Layered** | Presentation Layer | 사용자 인터페이스 및 사용자 입력 처리 | HTTP 요청 수신, 입력 값 검증(Validation) | HTTP/JSON, HTML | 건물의 입구/로비 |
| | Business Logic Layer | 핵심 비즈니스 규칙 및 처리 | 데이터 가공, 트랜잭션 처리, workflow 제어 | Java Service, C# Class | 건물의 사무실/관리실 |
| | Persistence Layer | 데이터 영속화 | DB CRUD(Create, Read, Update, Delete) 연산 | SQL, JPA, ORM | 건물의 창고/금고 |
| **MVC** | Model | 데이터와 상태 | Domain Logic, DB 쿼리 결과 담음 | Plain Object(DB Entity) | 식재료와 레시피 |
| | View | 시각적 표현 | Model 데이터를 렌더링, 화면 갱신 | HTML/CSS, JSX, SwiftUI | 손님 앞에 놓인 완성된 요리 |
| | Controller | 입력 처리 및 흐름 제어 | 이벤트 수신 → Model 갱신 → View 선택 | Servlet, Router | 주문을 받아 주방에 전달하는 웨이터 |
| **MVVM** | ViewModel | View를 위한 데이터 변환 및 상태 관리 | Model 데이터를 View 표현용으로 변환(Observable) | LiveData, Combine, Observable | 주방의 모니터링 시스템(실시간 주문 현황) |

#### 2. 레이어드 아키텍처 (N-Tier)

가장 대중적인 패턴으로, **관심사의 분리(Seperation of Concerns)**를 통해 상위 계층이 하위 계층에만 의존하는 구조입니다. 하지만 이로 인해 하위 계층의 변경이 상위 계층에 영향을 미치는 문제가 있어, 현대에서는 **포트와 어댑터(Ports and Adapters)** 또는 **헥사고날 아키텍처(Hexagonal Architecture)** 등으로 발전하기도 합니다.

```ascii
[계층형 아키텍처의 의존성 방향 및 데이터 흐름]

   (User Request)
        │
        ▼
  +---------------------------+
  │ Presentation Layer (UI)   │  <-- API Gateway, Controller
  +---------------------------+
        │  ──(의존)───────┐
        ▼                 │
  +---------------------------+   Dependencies Flow
  │ Business Logic Layer      │  ───────────────────►
  │ (Domain Logic)            │
  +---------------------------+
        │  ──(의존)───────┐
        ▼                 │
  +---------------------------+   Dependencies Flow
  │ Data Access Layer         │  ───────────────────►
  │ (Persistence)             │
  +---------------------------+
        │
        ▼
    [Database]
```

**해설**:
위 다이어그램과 같이 요청은 최상위 계층으로 들어와 하위 계층으로 전달됩니다.
1. **Presentation Layer**: 사용자의 HTTP 요청을 받아 JSON 형태 등으로 파싱합니다.
2. **Business Layer**: 실제 업무 로직(예: "재고가 10개 미만이면 주문 불가")을 수행합니다.
3. **Data Access Layer**: DB와 직접 통신하여 SQL을 실행합니다.
이 구조의 핵심은 하위 계층(Persistence)이 상위 계층(Presentation)을 몰라야 한다는 점입니다. 만약 DB가 Oracle에서 MySQL로 바뀌더라도 로직 계층은 변하지 않아야 합니다.

#### 3. UI 패턴의 상세 메커니즘

##### A. MVC (Model-View-Controller)
가장 고전적이나, 구현 방식에 따라 느슨한 결합(Passive View)과 강한 결합(Active View)으로 나뉩니다. 웹(Spring MVC)은 주로 Passive View 방식입니다.

##### B. MVVM (Model-View-ViewModel)
데이터 바인딩을 통해 View와 ViewModel 사이의 의존성을 제거합니다.

```ascii
[MVC vs MVVM 데이터 흐름 비교]

  1. MVC (User Action driven)
  ---------------------------
  User Input  ──▶ [Controller] ──▶ Update [Model]
       ▲                          │
       │                          │
       └────── [View] Update ◀────┘
       (Model Change Event)
       * View가 Model을 직접 참조하거나, Controller가 View를 갱신함.

  2. MVVM (Data Binding driven)
  -----------------------------
  User Input  ──▶ [ViewModel] (Logic)
       ▲            │
       │            ▼
  [View] ◀───── (Data Binding / Observable)
       * 자동 동기화: View의 Input이 ViewModel로, ViewModel의 State가 View로 자동 반영
```

**심층 해설**:
MVVM의 핵심은 **Observable 패턴**입니다.
1. **ViewModel**은 View가 필요로하는 데이터를 형식화하여 가지고 있습니다.
2. **View**는 ViewModel의 특정 속성(Property)을 구독(Subscribe)합니다.
3. 사용자가 입력을 하면 View는 즉시 ViewModel의 Command를 호출하고, ViewModel 내부 상태가 변경되면 바인딩된 View 속성이 자동으로 업데이트됩니다.
이 과정에서 UI 업데이트를 위한 복잡한 `findViewById()`나 `setText()` 같은 코드가 사라지게 됩니다.

**핵심 코드 스니펫 (MVVM 개념)**:
```javascript
// [ViewModel] (Vue.js 예시)
export default {
  data() { return { count: 0 } }, // Model of View
  methods: {
    increment() { this.count++; } // Logic
  }
}

// [View] (Template)
<!-- Data Binding -->
<button @click="increment">Count is: {{ count }}</button>
<!-- 개발자가 직접 버튼 클릭 시 텍스트를 변경하는 코드를 짤 필요가 없음 -->
```

**📢 섹션 요약 비유**: MVC는 전화 교환원(Controller)이 송수화자(Model)를 연결해주는 구식 전화망이라면, MVVM은 스마트폰의 동기화 기능처럼, 내가 주소록(Model)을 수정하자마자 상대방의 화면(View)에 자동으로 업데이트되는 '구글 드라이브'와 같은 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: MVC vs MVP vs MVVM

| 특징 | MVC (Model-View-Controller) | MVP (Model-View-Presenter) | MVVM (Model-View-ViewModel) |
|:---|:---|:---|:---|
| **View-Model 의존성** | View가 Model을 직접 참조 (양방향 의존 가능성 높음) | View가 Model을 인지 못함 (완전 분리) | View가 ViewModel을 바인딩 (약한 결합) |
| **업데이트 주체** | Controller가 View를 갱신하거나 Model이 View를 옵저빙 | Presenter가 View의 인터페이스를 통해 갱신 명령 | Data Binding 프레임워크가 자동 갱신 |
| **단위 테스트** | 어려움 (View 로직 포함 경우) | 쉬움 (Presenter는 UI 프레임워크 독립적) | 매우 쉬움 (ViewModel은 순수 로직 객체) |
| **대표 플랫폼** | Ruby on Rails, Spring MVC, ASP.NET MVC | Windows Forms, GWT, Legacy Android | React, Vue.js, Angular, SwiftUI, Jetpack Compose |

#### 2. 타 과목 융합 관점

**① 컴퓨터 구조 (OS) 관점 - 인터럽트와 이벤트 루프**
UI 패턴은 결국 **이벤트 드리븐 아키텍처(Event-Driven Architecture)**입니다. 사용자의 마우스 클릭(하드웨어 인터럽트)이 OS의 이벤트 큐(Event Queue)에 담기고, 이가 UI 메시지 루프에 의해 Dispatcher(Controller/ViewModel)로 전달되는 과정은 컴퓨터 구조의 인터럽트 처리 핸들러와 동일한 메커니즘을 가집니다.

**② 네트워크 (OSI 7 Layer) 관점 - 캡슐화**
계층형 아키텍처는 네트워크의 **OSI 7계층**과 유사합니다. 데이터링크 계층이 물리 계층의 세부 사항을 모르고 통신하듯이, 비즈니스 계층은 DB의 스키마(Row, Column)가 어떻게 생겼는지 몰라도(DTO 등으로 변환하여 받아서) 로직을 수행합니다. 이는 **인터페이스 기반 프로그래밍**과 **캡슐화**가 주는 강력한 추상화 효과입니다.

**📢 섹션 요약 비유**: MVC는 목수가 벽돌을 직접 보고 설계하는 것(밀착형)이고, MVVM은 목수가 설계도면(ViewModel)을 보면서 현장 관리자(View)에게 작업을 지시하는 것(중계형)입니다. 설계도면만 바꿔도 현장 작업이 바뀌므로 유연성이 훨씬 높습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정

**[시나리오 1] 대규모 엔터프라이즈 ERP 시스템 구축**
- **상황**: 수천 개의 비즈니스 룰과 복잡한 데이터 무결성이 중요한 금융/결제 시스템.
- **의사결정**: **Layered Architecture + MVC**.
- **이유**: 안정성이 최우선이며, 트랜잭션 관리가 명확해야 함. 프레임워크의 강력한 컨벤션(Spring, JPA 등)을 따르는 것이 유지보수에 유리함. 과도한 ViewModel 로직은 숨은 버그를 유발할 수 있음.

**[시나리오 2] 사용자 인터랙션이 많은 모바일 핀테크 앱**
- **상황**: 실시간 계좌 잔고 변동, 애니메이션 효과가 중요한 iOS/Android 앱.
- **의사결정**: **MVVM**.
- **이유**: View와 로직의 철저한 분리로 UI 팀(디자이너)과 로직 팀(백엔드 연동)의 병렬 작업이 가능해야 함. 또한 ViewModel을 단위 테스트하여 로직 오류(잔고 계산 등)를 사전에 차단해야 함.

#### 2. 도입 체크리스트

**[기술적 검사항목]**
- [ ] **단방향 데이터 흐름 확보**: 데이터가 예측 가능한 방향(하향식 또는 상태 기반)으로 흐르는가?
- [ ] **바인딩 오버헤드**: Data Binding으로 인한 메모리 누수(Memory Leak)나 성능 저하(Lag)가 없는가?
- [ ] **DTO 활용**: 레이어 간 통신 시 Domain Model 대신 **DTO (Data Transfer Object)**를 사용하여 의존성을 차단했는가?

**[운영·보안적 검사항목]**
- [ ] **입력 검증의 위치**: 사용자 입력은 View나 Controller가 아닌 **Business Layer(도메인 모델)**에서 격증되어야 함.
- [ ] **예외 전파**: 각 계층의 예외를 Catch하여 사용자에게 노출되지 않도록 Wrapper 했는