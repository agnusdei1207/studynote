---
title: "Transaction Script vs Domain Model"
date: "2026-05-06"
tags:
  - "studynote-design-supervision"
weight: 180
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Transaction Script는 유스케이스별 절차를 서비스 함수에 모아 처리하는 방식이고, Domain Model은 비즈니스 규칙과 상태 변화를 도메인 객체 안에 캡슐화하는 방식이다.
> 2. **가치**: 단순 CRUD (Create, Read, Update, Delete)와 짧은 수명의 업무에는 Transaction Script가 빠르지만, 규칙이 서로 얽히고 상태 전이가 복잡해질수록 Domain Model이 변경 비용과 테스트 비용을 크게 낮춘다.
> 3. **판단 포인트**: 선택 기준은 "객체지향이 멋져 보이는가"가 아니라, 비즈니스 규칙의 복잡도·변경 빈도·일관성 경계·팀의 설계 역량을 종합했을 때 어느 쪽이 더 단순해지는가에 있다.

---

## Ⅰ. 개요 및 필요성

Martin Fowler의 PoEAA (Patterns of Enterprise Application Architecture)는 엔터프라이즈 애플리케이션의 비즈니스 로직을 어떻게 조직할지에 대해 여러 패턴을 제시한다. 그중 Transaction Script와 Domain Model은 서로 대립하는 개념이라기보다, <strong>복잡도가 다른 문제에 대응하는 두 가지 방식</strong>으로 이해하는 것이 맞다.

Transaction Script는 가장 자연스러운 출발점이다. "주문 생성", "주문 취소", "회원 가입"처럼 요청 하나를 함수 하나로 구현하면 처음에는 매우 빠르다. 데이터베이스 접근, 검증, 계산, 저장, 이벤트 발행을 같은 서비스 메서드에 순서대로 적으면 되므로 작은 프로젝트나 관리 화면에서는 충분히 실용적이다.

그러나 규칙이 늘어나면 문제가 생긴다. 할인 정책, 상태 전이, 재고 예약, 결제 승인, 환불 제한처럼 서로 영향을 주는 규칙이 한 서비스 메서드와 여러 유사 메서드에 흩어진다. 이때부터 "한 기능 수정이 다른 기능을 깨는 구조"가 생기고, 왜곡된 중복과 God Service가 나타난다. Domain Model은 이런 지점에서 비즈니스 규칙을 객체의 책임 안으로 되돌리기 위해 등장한다.

- **📢 섹션 요약 비유**: Transaction Script는 해야 할 일을 한 장의 체크리스트에 적어 처리하는 방식이고, Domain Model은 각 역할을 맡은 전문가들이 자기 규칙을 알고 움직이게 만드는 팀 운영과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

두 패턴의 가장 큰 차이는 "규칙이 어디에 사는가"다. Transaction Script에서는 서비스가 데이터 조회, 검증, 계산, 저장을 직접 지휘한다. 반면 Domain Model에서는 Application Service가 흐름만 조율하고, 실제 규칙은 Order, Payment, Inventory 같은 도메인 객체가 스스로 수행한다.

| 항목 | Transaction Script | Domain Model |
| :--- | :--- | :--- |
| 비즈니스 규칙 위치 | Service / Use Case 함수 | Entity, Aggregate, Value Object, Domain Service |
| 데이터 접근 방식 | 함수 안에서 DAO (Data Access Object)·Repository 직접 호출 | Application Service가 Repository를 통해 객체를 로드 |
| 상태 변경 표현 | `service.cancelOrder(id)` 안에서 여러 if 처리 | `order.cancel()` 같은 행위 메서드 중심 |
| 테스트 단위 | 서비스 + 저장소 mocking 중심 | 순수 도메인 객체 단위 테스트 가능 |

아래 그림은 주문 생성 예시에서 두 방식의 구조 차이를 보여 준다.

```text
+----------------------------------------------------------------------+
| Business logic placement                                             |
+-------------------------------+--------------------------------------+
| Transaction Script            | Domain Model                         |
+-------------------------------+--------------------------------------+
| OrderService.placeOrder()     | OrderAppService.placeOrder()         |
|   - load customer             |   - load customer / products         |
|   - validate items            |   - create Order aggregate           |
|   - calculate discount        | Order aggregate                      |
|   - reserve stock             |   - validate items                   |
|   - save order                |   - calculate discount               |
|   - publish event             |   - reserve stock / change status    |
|                               |   - enforce invariants               |
| Logic concentrated in script  | Logic encapsulated in domain object  |
+-------------------------------+--------------------------------------+
```

Domain Model의 핵심은 객체를 데이터 상자처럼 두지 않는 것이다. 주문 객체가 주문 총액 계산, 상태 전이, 취소 가능 여부 판단을 직접 책임지면, 규칙은 주문이라는 개념 근처에 응집된다. 이때 Repository 패턴이 함께 쓰이면 도메인 객체는 저장 기술보다 비즈니스 의미에 집중할 수 있다.

반대로 Domain Model이라고 이름 붙였지만 실제로는 엔티티가 getter/setter만 있고 모든 규칙이 서비스에 남아 있으면 그것은 Anemic Domain Model에 가깝다. 즉 Domain Model의 가치는 클래스 수를 늘리는 데 있지 않고, **규칙을 객체의 행위로 이동시키는 데** 있다.

- **📢 섹션 요약 비유**: Transaction Script는 교실 한쪽에서 담임이 모든 학생 일을 일일이 지시하는 방식이고, Domain Model은 반장·서기·청소당번이 자기 규칙을 알고 움직이는 반 운영 방식과 같다.

---

## Ⅲ. 비교 및 연결

이 두 패턴은 우열 관계보다 적용 맥락이 다르다. 단순한 업무를 Domain Model로 과하게 감싸면 설계 비용만 늘고, 복잡한 업무를 Transaction Script로 밀어붙이면 규칙이 중복되고 변경 파급이 커진다. 결국 비교의 핵심은 "처음 빠른가"가 아니라, <strong>복잡도가 커질 때 어느 쪽이 더 단순함을 유지하는가</strong>다.

| 비교 축 | Transaction Script | Domain Model |
| :--- | :--- | :--- |
| 초기 개발 속도 | 빠름 | 상대적으로 느림 |
| 규칙 증가 시 유지보수 | 급격히 어려워짐 | 응집된 구조 덕분에 상대적으로 안정적 |
| 적합한 업무 | 단순 CRUD, 관리성 화면, 짧은 배치 | 주문, 결제, 정산, 보험 심사, 회원 등급 정책 |
| 저장 계층과의 결합 | 높아지기 쉬움 | Repository로 분리하기 좋음 |
| 팀 요구 역량 | 절차적 코딩 중심 | 모델링, 경계 설정, 테스트 역량 필요 |

또한 이 비교는 DDD (Domain-Driven Design), Repository, CQRS (Command Query Responsibility Segregation)와도 연결된다. Domain Model은 보통 쓰기 모델의 일관성 규칙이 중요할 때 빛난다. 반대로 조회 전용 화면이나 통계성 쿼리는 Transaction Script나 Query Service가 더 단순할 수 있다. 즉 한 시스템 안에서도 <strong>쓰기 쪽은 Domain Model, 읽기 쪽은 단순 스크립트</strong>처럼 혼합 전략이 가능하다.

Anemic Domain Model은 이 둘의 장점을 모두 잃는 대표 안티패턴이다. 클래스는 많아졌는데 규칙은 여전히 서비스에 있으므로, Transaction Script의 단순함도 없고 Domain Model의 응집도도 없다. 설계감리에서는 이런 "껍데기 객체"를 특히 경계해야 한다.

- **📢 섹션 요약 비유**: Transaction Script와 Domain Model의 차이는 가게 운영을 사장 혼자 메모로 돌릴지, 주방·홀·재고 담당이 역할과 규칙을 나눠 운영할지의 차이와 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

실무 판단에서 중요한 것은 규칙의 개수보다 <strong>규칙 간 결합도</strong>다. 할인 정책 하나만 있어도 배송비, 적립금, 쿠폰 중복, 회원 등급, 반품 규칙과 얽히기 시작하면 Transaction Script는 빠르게 비대해진다. 반대로 게시판 관리, 코드 테이블 유지, 내부 설정 API처럼 상태 전이가 단순한 업무는 Domain Model을 도입해도 이익이 작다.

| 시나리오 | 권장 방식 | 판단 이유 |
| :--- | :--- | :--- |
| 관리자 CRUD 화면, 단순 설정 API | Transaction Script | 흐름이 단순하고 모델링 비용이 과함 |
| 주문·결제·정산·보험 심사 | Domain Model | 규칙 간 결합과 상태 전이가 복잡함 |
| 레거시 시스템 점진 개선 | 혼합 전략 | 핫스팟 유스케이스만 Domain Model로 추출 가능 |
| 조회 중심 리포트 시스템 | Transaction Script 또는 Query Service | 복잡한 도메인 행위보다 조회 최적화가 중요 |

### 실무 체크리스트

1. 비즈니스 규칙이 여러 유스케이스에 반복 등장하는가?
2. 상태 전이와 불변식이 객체 내부에 있어야 안전한가?
3. 테스트가 데이터베이스 통합 테스트에 과하게 의존하고 있지는 않은가?
4. 팀이 Aggregate, Value Object, Repository 같은 개념을 유지할 역량이 있는가?
5. 단순 조회까지 모두 Domain Model로 끌어들여 과잉 설계하고 있지는 않은가?

### 자주 발생하는 안티패턴

- 모든 화면을 Domain Model로 만들겠다고 선언한 뒤, 실제로는 빈 엔티티와 거대한 서비스만 남는 구조
- 복잡한 업무인데도 "빨리 만든다"는 이유로 Transaction Script를 계속 덧대어 God Service로 키우는 구조
- Domain Model을 썼으면서도 상태 변경을 setter 공개로 열어 두어 불변식을 깨뜨리는 구현
- 읽기 모델과 쓰기 모델을 구분하지 않아 Domain Model에 리포팅 쿼리까지 몰아넣는 설계

학습 정리에서는 <strong>"Transaction Script는 단순 유스케이스를 빠르게 구현하는 데 적합하고, Domain Model은 복잡한 비즈니스 규칙과 상태 전이를 객체에 응집시켜 유지보수성과 테스트성을 높이는 구조이며, 선택 기준은 규칙 결합도와 변경 빈도"</strong>라고 정리하면 된다.

- **📢 섹션 요약 비유**: 작은 가게는 사장 한 명의 메모장으로도 돌아가지만, 백화점 규모가 되면 매장별 규칙과 책임을 나눠야 혼란이 줄어드는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

Transaction Script의 장점은 단순함이다. 적은 클래스 수, 빠른 구현, 낮은 진입 장벽 덕분에 작은 업무를 짧은 시간 안에 전달할 수 있다. 반면 Domain Model의 장점은 복잡한 규칙이 커질수록 더 선명해진다. 규칙이 객체 주변으로 모이고 테스트가 쉬워지며, 변경 영향이 예측 가능해진다.

하지만 어떤 패턴도 만능은 아니다. Domain Model은 학습 비용과 설계 비용이 있고, Transaction Script는 규모가 커질수록 빚이 쌓인다. 그래서 중요한 것은 특정 패턴을 신앙처럼 따르는 것이 아니라, <strong>현재 시스템의 복잡도와 앞으로의 변화 방향에 맞는 패턴을 선택하는 것</strong>이다.

결론적으로 기억할 문장은 이것이다. "비즈니스 규칙이 흩어질수록 Domain Model 쪽으로, 규칙이 단순하고 수명이 짧을수록 Transaction Script 쪽으로." 설계감리 관점에서는 이 균형을 얼마나 의식적으로 선택했는지가 좋은 아키텍처의 증거가 된다.

- **📢 섹션 요약 비유**: Transaction Script와 Domain Model은 자전거와 자동차처럼 둘 다 좋은 도구지만, 골목길과 고속도로에서 각각 더 빛나는 조건이 다르다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PoEAA (Patterns of Enterprise Application Architecture) | Transaction Script와 Domain Model을 체계화한 Martin Fowler의 패턴 카탈로그다. |
| DDD (Domain-Driven Design) | Domain Model을 더 깊게 발전시킨 분석·설계 접근법이다. |
| Repository Pattern | Domain Model을 저장 기술로부터 분리할 때 자주 결합되는 패턴이다. |
| DAO (Data Access Object) | Transaction Script에서 자주 함께 쓰이며 데이터 접근을 분리하는 구조다. |
| Anemic Domain Model | 객체는 많지만 규칙이 서비스에 남아 있는 대표적 안티패턴이다. |
| CQRS (Command Query Responsibility Segregation) | 읽기와 쓰기의 복잡도가 다를 때 두 패턴을 혼합 적용하는 단서를 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Simple CRUD use cases
        |
        v
Transaction Script for fast delivery
        |
        v
Rules increase and start to overlap
        |
        +- duplicated validation
        +- state transition complexity
        +- growing God Service
        |
        v
Domain Model + Repository + richer business encapsulation
```

이 흐름은 시스템이 단순 업무 처리에서 복잡한 규칙 중심 구조로 성장할 때, 비즈니스 로직 조직 방식도 함께 바뀌어야 함을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 간단한 심부름은 해야 할 일을 종이에 적어 두면 금방 끝낼 수 있어요.
2. 그런데 친구가 많아지고 규칙이 많아지면, 각자 맡은 일을 스스로 잘 아는 반장이 필요해져요.
3. 그래서 쉬운 일은 메모장으로, 복잡한 일은 똑똑한 역할 나누기로 관리하는 거예요.
