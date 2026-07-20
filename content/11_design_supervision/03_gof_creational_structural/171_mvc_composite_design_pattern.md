---
title: "MVC Composite Design Pattern"
date: "2026-04-21"
tags:
  - "studynote-design-supervision"
weight: 171
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MVC (Model-View-Controller)는 단순히 클래스를 3개로 나누는 규칙이 아니라, 상태 관리·표현·입력 조정을 분리하는 아키텍처이며 실제 구현에서는 옵저버 (Observer), 전략 (Strategy), 커맨드 (Command), 컴포지트 (Composite) 같은 GoF (Gang of Four) 패턴의 복합체로 동작한다.
> 2. **가치**: 변경의 영향 범위를 역할별로 가두기 때문에 화면 변경, 도메인 규칙 변경, 입력 흐름 변경을 서로 다른 계층에서 처리할 수 있어 유지보수성과 테스트성이 좋아진다.
> 3. **판단 포인트**: MVC를 적용할 때는 "View가 Model을 직접 관찰하는가", "Controller가 얼마나 비대해지는가", "웹/데스크톱/단일 페이지 애플리케이션 (SPA, Single Page Application) 중 어떤 실행 문맥인가"를 기준으로 MVP (Model-View-Presenter)나 MVVM (Model-View-ViewModel) 같은 변형과 비교해야 한다.

---

## Ⅰ. 개요 및 필요성

MVC는 사용자 인터페이스를 가진 시스템에서 관심사 분리 (SoC, Separation of Concerns)를 달성하기 위한 대표 아키텍처다. 초기 GUI (Graphical User Interface) 프로그램과 전통적 웹 애플리케이션에서는 이벤트 핸들러 하나가 화면 읽기, 입력 검증, 비즈니스 로직, 데이터베이스 호출, 화면 갱신을 모두 담당하는 경우가 많았다. 이런 구조는 작은 데모에서는 빠르지만, 요구사항이 커질수록 수정 범위와 결함 전파 범위가 함께 폭발한다.

MVC가 필요한 이유는 "변화의 종류"가 서로 다르기 때문이다. 화면 배치는 자주 바뀌지만 핵심 비즈니스 규칙은 상대적으로 안정적일 수 있고, 사용자 입력 흐름은 기획이나 채널 변화에 따라 다시 설계될 수 있다. 이 서로 다른 변경 축을 한 메서드에 묶어 두면, 화면 버튼 이름 하나 바꾸는 일도 서비스 규칙 수정과 충돌하게 된다.

아래 그림은 MVC가 해결하려는 문제를 보여 준다.

```text
+----------------------------------------------------------------------+
| Before MVC vs After MVC                                              |
+-------------------------------+--------------------------------------+
| One event handler             | Model / View / Controller            |
| - reads user input            | - Model: state + business rule       |
| - updates domain state        | - View : rendering                   |
| - queries DB                  | - Controller: input coordination     |
| - renders screen              | - changes isolated by responsibility  |
+-------------------------------+--------------------------------------+
```

즉 MVC는 미학적 분리보다 <strong>변화의 지역화(Locality of Change)</strong>를 목적으로 한다. 역할을 나누는 이유는 코드가 예뻐 보여서가 아니라, 화면 변경이 도메인 규칙을 흔들지 않게 하고 입력 흐름 수정이 렌더링 로직 전체를 오염시키지 않게 하려는 것이다.

- **📢 섹션 요약 비유**: 식당에서 주문받는 사람, 요리하는 사람, 진열하는 사람이 한 명이면 바쁠 때 실수가 커진다. MVC는 주문, 조리, 진열을 나눠서 일이 꼬일 범위를 줄이는 운영 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MVC의 핵심은 세 역할의 경계를 만드는 것이다. Model은 상태와 규칙을 담고, View는 그 상태를 표현하며, Controller는 사용자 의도를 해석해 Model 변경이나 View 전환을 조정한다. 그런데 실무 구현을 들여다보면 이것이 하나의 패턴이 아니라 여러 패턴의 결합임을 알 수 있다.

| MVC 요소 | 주된 책임 | 자주 결합되는 패턴 | 이유 |
| :--- | :--- | :--- | :--- |
| Model | 상태 보관, 비즈니스 규칙, 검증 | Observer, Domain Model | 상태 변경을 여러 View에 통지 |
| View | 렌더링, 입력 이벤트 발생 | Composite, Template Method | 화면 요소를 트리로 구성하고 렌더링 규칙 재사용 |
| Controller | 입력 해석, 흐름 제어, Model 호출 | Strategy, Command, Front Controller | 요청별 처리 흐름을 교체·중앙화 |

아래 그림은 MVC를 "복합 디자인 패턴"으로 보는 관점을 보여 준다.

```text
+----------------------------------------------------------------------+
| MVC as a composite of patterns                                       |
+----------------------------------------------------------------------+
| User input                                                           |
|    |                                                                 |
|    v                                                                 |
| Controller -- Strategy / Command --> Model                           |
|    |                                   |                             |
|    |                                   +- Observer notify -------+   |
|    v                                                            v   |
| View selection                                            View update |
|                                                                  |    |
|                                                          Composite UI |
+----------------------------------------------------------------------+
```

이 구조에서 중요한 점은 Model이 View를 "예쁘게 그리는 법"을 몰라야 하고, View가 도메인 규칙을 스스로 바꾸지 말아야 하며, Controller가 데이터 저장 세부 구현을 다 떠안지 않아야 한다는 것이다. 특히 View 트리는 버튼, 패널, 리스트, 폼 같은 구성요소가 중첩되므로 GoF의 컴포지트 패턴이 자연스럽게 녹아든다.

또한 데스크톱 MVC와 웹 MVC는 같은 이름을 쓰더라도 결합 방향이 조금 다르다. 데스크톱 환경에서는 View가 Model 상태를 직접 관찰하는 전통적 MVC가 많고, 서버사이드 웹 MVC는 Controller가 요청마다 Model 데이터를 준비해 View 템플릿에 전달하는 형태가 많다. 즉 MVC는 고정 공식이 아니라, <strong>실행 환경에 맞게 패턴 조합을 바꾸는 설계 프레임</strong>이다.

- **📢 섹션 요약 비유**: MVC는 레고 3조각만 맞추는 장난감이 아니라, 기본 뼈대 위에 힌지, 기어, 바퀴를 상황에 맞게 끼우는 조립 세트다. 이름은 같아도 어떤 부품을 같이 쓰느냐에 따라 움직임이 달라진다.

---

## Ⅲ. 비교 및 연결

MVC를 정확히 말하려면 MVP, MVVM과의 경계를 분명히 해야 한다. 세 구조 모두 화면과 로직을 분리하려 하지만, "누가 누구를 알고 있는가"에서 차이가 난다.

| 패턴 | Model과 View 관계 | 입력/중재자 | 장점 | 약점 |
| :--- | :--- | :--- | :--- | :--- |
| MVC | View가 Model을 직접 읽거나 관찰 가능 | Controller | 전통적 GUI·웹에 익숙함, 다중 View 구성 쉬움 | 결합 방향이 흐려지면 책임 경계가 모호해짐 |
| MVP | View는 인터페이스 뒤에 숨고 Model 직접 접근 최소화 | Presenter | 테스트가 쉬움, View 수동성 높음 | Presenter 비대화 위험 |
| MVVM | View와 ViewModel이 데이터 바인딩으로 연결 | ViewModel | 상태 동기화 자동화, 프런트엔드 프레임워크와 궁합 좋음 | 바인딩 복잡도와 디버깅 난도 |

MVC는 특히 웹 프레임워크에서 Front Controller 패턴과 자주 연결된다. 예를 들어 Spring MVC에서는 `DispatcherServlet`이 모든 요청을 받고, 실제 Controller 메서드에 위임한 뒤, View Resolver가 템플릿이나 JSON (JavaScript Object Notation) 응답을 선택한다. 이때 Model은 꼭 UI 모델만이 아니라 도메인 서비스, 엔티티, DTO (Data Transfer Object) 계층과 연결된다.

또 하나 자주 헷갈리는 지점은 제목의 "복합"이 GoF의 컴포지트 패턴만을 뜻하지 않는다는 점이다. MVC에는 실제로 View 트리에서 컴포지트 패턴이 들어가지만, 더 큰 의미에서는 <strong>여러 패턴이 조합된 composite architecture</strong>라는 뜻으로 읽는 것이 맞다. 즉 MVC를 단일 GoF 패턴으로 외우면 반쪽 이해가 된다.

- **📢 섹션 요약 비유**: MVC는 기본형 세단이고, MVP는 운전석과 조수석 역할을 더 엄격히 나눈 차량, MVVM은 자동변속과 센서 보조가 들어간 차량에 가깝다. 모두 자동차지만 조작 방식과 부품 배치가 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무에서는 MVC라는 이름보다 "어디까지를 Controller에 둘 것인가"가 더 중요하다. 작은 서비스는 Controller가 요청 파싱과 응답 선택을 동시에 담당해도 괜찮지만, 비즈니스 규칙까지 몰리면 곧 Fat Controller가 된다. 반대로 Model을 너무 빈약한 데이터 구조로만 두면 Anemic Domain Model이 되어 서비스 계층이나 Controller가 규칙을 대신 떠안는다.

아래 그림은 서버사이드 웹에서 자주 보는 MVC 흐름이다.

```text
+----------------------------------------------------------------------+
| Typical Web MVC request flow                                         |
+----------------------------------------------------------------------+
| HTTP Request                                                         |
|      |                                                               |
|      v                                                               |
| Front Controller -> Controller -> Service / Domain Model             |
|      |                                   |                           |
|      +-------------- Model data <--------+                           |
|                              |                                       |
|                              v                                       |
|                     View template / JSON response                    |
+----------------------------------------------------------------------+
```

### 실무 판단 체크리스트

1. Controller가 흐름 제어만 담당하는가, 아니면 비즈니스 규칙까지 삼키고 있는가?
2. View가 Domain Model 내부 구조에 과도하게 의존하지 않도록 DTO나 ViewModel이 필요한가?
3. 동일한 Model을 여러 View(웹 화면, 응용 프로그램 인터페이스 (API, Application Programming Interface), 관리 화면)가 공유해야 하는가?
4. 실시간 양방향 UI 동기화가 중요하다면 MVC보다 MVVM이나 reactive architecture가 더 적합하지 않은가?
5. 테스트 전략상 Controller 단위 테스트와 Model 단위 테스트를 분리할 수 있는가?

### 자주 발생하는 안티패턴

- Controller에 검증, 트랜잭션, 변환, 화면 분기, 외부 연동을 모두 몰아넣는 것
- View가 Domain Entity를 직접 수정해 책임 경계를 흐리는 것
- Model이 UI 라이브러리 의존성을 가져 화면 기술에 종속되는 것
- "MVC 썼다"고 말하지만 실제로는 화면 코드와 서비스 코드가 한 파일에 뒤섞여 있는 것

학습 정리에서는 MVC를 단순한 3계층 슬로건으로 쓰기보다, "Observer로 상태 통지, Composite로 UI 구성, Front Controller로 요청 집중"처럼 실제 패턴 연결까지 보여 주는 편이 설득력이 높다. 또한 웹 MVC와 리치 클라이언트 MVC의 차이를 언급하면 적용 문맥을 읽는 답안이 된다.

- **📢 섹션 요약 비유**: 도로 위 교통정리를 경찰이 해야지, 전광판이 직접 신호를 바꾸고 자동차 엔진까지 고치기 시작하면 곧 혼란이 온다. MVC의 실무 핵심은 각 역할이 자기 차선만 지키게 만드는 데 있다.

---

## Ⅴ. 기대효과 및 결론

MVC의 가장 큰 효과는 변경 가능성을 구조 안에 미리 접어 넣는다는 데 있다. 화면 스킨이 바뀌어도 핵심 규칙은 유지되고, 입력 방식이 웹에서 모바일로 바뀌어도 Model은 재사용될 수 있다. 또한 같은 Model을 여러 View에서 공유할 수 있어 관리 화면, API 응답, 사용자 화면을 비교적 일관되게 설계할 수 있다.

물론 MVC가 항상 정답은 아니다. 화면 상태 동기화가 매우 복잡하면 MVVM이 더 자연스럽고, 단순 CRUD 서비스에서는 과도한 추상화로 느껴질 수 있다. 중요한 것은 MVC를 교조적으로 따르는 것이 아니라, <strong>변화의 방향과 테스트 전략에 맞게 패턴 조합을 고르는 것</strong>이다.

결론적으로 MVC는 "Model·View·Controller 세 단어"보다, <strong>여러 패턴을 조합해 변화의 영향을 역할별로 가두는 복합 설계 원리</strong>로 기억하는 것이 정확하다. 이 관점을 잡으면 왜 현대 웹 프레임워크와 UI 프레임워크가 서로 다른 변형을 택하는지도 자연스럽게 이해된다.

- **📢 섹션 요약 비유**: 좋은 공연은 배우, 무대, 연출이 서로 맡은 일을 지킬 때 완성된다. MVC도 마찬가지로, 각 파트가 자신의 역할에 집중할수록 전체 시스템이 더 안정적으로 돌아간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Observer Pattern | Model 상태 변경을 View에 알리는 대표 연결 방식 |
| Composite Pattern | View가 위젯 트리 구조를 갖는 이유를 설명 |
| Strategy / Command Pattern | Controller가 입력 처리 방식을 교체 가능한 형태로 갖게 함 |
| Front Controller Pattern | 웹 MVC에서 단일 진입점으로 요청을 집중시키는 구조 |
| MVP / MVVM | MVC와 비교할 대표적인 UI 아키텍처 변형 |
| SoC (Separation of Concerns) | MVC가 지키려는 가장 핵심적인 설계 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
Monolithic UI code
        |
        v
MVC separation
        |
        +- Observer for state update
        +- Composite for view tree
        +- Strategy / Command for input flow
        |
        v
Web MVC + Front Controller
        |
        v
MVP / MVVM / reactive UI architectures
```

이 흐름은 화면 코드의 분리 요구가 MVC를 낳았고, 이후 실행 환경과 테스트 요구에 따라 다양한 패턴 조합으로 확장됐음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MVC는 장난감 가게에서 계산하는 사람, 장난감을 만드는 사람, 진열하는 사람을 따로 두는 것과 같아요.
2. 진열대를 바꿔도 장난감 만드는 법은 그대로 두고, 주문받는 방법만 따로 고칠 수 있어요.
3. 그래서 가게가 커져도 일이 한곳에 엉켜서 망가지지 않아요.
