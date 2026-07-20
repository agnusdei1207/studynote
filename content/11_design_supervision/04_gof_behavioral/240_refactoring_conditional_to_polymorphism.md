---
title: "Replace Conditional with Polymorphism"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 240
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 타입에 따라 분기하는 if-else / switch 조건문 블록을 상태 패턴 (State Pattern) 이나 전략 패턴 (Strategy Pattern) 같은 다형성 (Polymorphism) 기반 클래스 계층으로 대체하여 OCP (Open/Closed Principle: 개방/폐쇄 원칙) 를 실현한다.
> 2. **가치**: 새 타입이 추가될 때 기존 조건문을 수정하는 대신 새 클래스를 추가하기만 하면 되어, 기존 코드 변경 없이 기능 확장이 가능해진다.
> 3. **판단 포인트**: 동일한 조건 블록이 여러 메서드에 반복되거나, 새 타입 추가 때마다 여러 곳을 수정해야 한다면 다형성으로 전환할 시점이다.

---

## Ⅰ. 개요 및 필요성
소프트웨어 개발 초기에는 간단한 if-else로 타입을 분기하는 코드가 자연스럽게 작성된다. 그러나 타입이 추가되고 조건이 복잡해지면 이 코드는 <strong>스위치 문 냄새 (Switch Statement Smell)</strong> 라는 안티 패턴이 된다.

마틴 파울러의 리팩토링 (Refactoring, 2018 2판) 에서 "Replace Conditional with Polymorphism" 은 가장 중요한 리팩토링 기법 중 하나로 다룬다. 핵심 직관은 다음과 같다:

> **"객체에게 자신이 무엇인지 물어보지 말고, 무엇을 해야 하는지 시켜라."**

이는 GoF (Gang of Four) 설계 원칙—<strong>'상속보다 구성 (Composition over Inheritance)'</strong>, <strong>OCP (Open/Closed Principle)</strong> —의 실천이다.

```java
// 안티패턴: 타입에 따른 switch 분기 (여러 메서드에 동일 패턴 반복)
double getShippingCost(String orderType) {
    switch (orderType) {
        case "EXPRESS":  return price * 0.1;
        case "STANDARD": return price * 0.05;
        case "ECONOMY":  return price * 0.02;
        default: throw new IllegalArgumentException();
    }
}

double getDeliveryDays(String orderType) {
    switch (orderType) {    // 같은 switch 반복!
        case "EXPRESS":  return 1;
        case "STANDARD": return 3;
        case "ECONOMY":  return 7;
        default: throw new IllegalArgumentException();
    }
}
```

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 매번 직원 유형(정규직/알바/계약직)을 물어보고 처우를 결정하는 것보다, 각 유형이 자신의 처우 계산법을 직접 알고 있는 게 훨씬 효율적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
[리팩토링 전: 조건문 분기]
+----------------------------------------------------------+
|  OrderService                                            |
|                                                          |
|  getShippingCost(type)                                   |
|    if EXPRESS  -> 10%                                     |
|    if STANDARD -> 5%          <- 새 타입 추가 시           |
|    if ECONOMY  -> 2%            여기를 수정해야 함 (OCP 위반)|
|                                                          |
|  getDeliveryDays(type)                                   |
|    if EXPRESS  -> 1일         <- 여기도 수정해야 함!        |
|    if STANDARD -> 3일                                     |
|    if ECONOMY  -> 7일                                     |
+----------------------------------------------------------+

[리팩토링 후: 다형성 기반]
+------------------------------------------------------------+
|  <<interface>> ShippingStrategy                            |
|  + getShippingCost(): double                               |
|  + getDeliveryDays(): int                                  |
+-----------------------+------------------------------------+
                        | implements
          +-------------+------------------+
          v             v                  v
+--------------+ +--------------+ +------------------+
|  Express     | |  Standard    | |  Economy         |
|  Shipping    | |  Shipping    | |  Shipping        |
|  cost: 10%   | |  cost: 5%    | |  cost: 2%        |
|  days: 1     | |  days: 3     | |  days: 7         |
+--------------+ +--------------+ +------------------+
                                          ^
                                          | 새 타입 추가 시
                               +----------------------+
                               |  SameDay Shipping    | <- 클래스만 추가!
                               |  cost: 20%           |   기존 코드 수정 없음
                               |  days: 0             |
                               +----------------------+
```

```java
// 전략 인터페이스
public interface ShippingStrategy {
    double calculateCost(double price);
    int getDeliveryDays();
}

// 구현체들
public class ExpressShipping implements ShippingStrategy {
    public double calculateCost(double price) { return price * 0.10; }
    public int getDeliveryDays() { return 1; }
}
public class StandardShipping implements ShippingStrategy {
    public double calculateCost(double price) { return price * 0.05; }
    public int getDeliveryDays() { return 3; }
}

// Context (사용 측)
public class Order {
    private ShippingStrategy strategy;

    public Order(ShippingStrategy strategy) {
        this.strategy = strategy;
    }
    public double getShippingCost() {
        return strategy.calculateCost(this.price);
    }
}
```

상태 패턴은 객체의 <strong>내부 상태</strong>가 바뀔 때 행동이 달라지는 경우에 적용한다:

| 패턴 | 사용 시기 | 상태 전환 |
|:---|:---|:---:|
| Strategy | 알고리즘 교체 (외부 주입) | 클라이언트가 선택 |
| State | 내부 상태 전이 | 상태 자신이 전환 |

- **📢 섹션 요약 비유**: 리모컨의 버튼마다 if-else를 쓰는 대신, TV·에어컨·오디오가 각자 "전원" 버튼을 어떻게 처리할지 알고 있는 것이다. 새 기기가 생겨도 리모컨 코드는 바꾸지 않는다.

---

## Ⅲ. 비교 및 연결
| 기법 | 목적 | 적용 조건 |
|:---|:---|:---|
| Replace Conditional with Polymorphism | 타입별 분기 제거 | 동일 switch가 여러 곳에 반복 |
| Replace Type Code with Subclass | 타입 코드를 서브클래스로 | 타입에 따라 동작이 다름 |
| Extract Method | 긴 메서드 분리 | 메서드가 너무 길 때 |
| Introduce Parameter Object | 매개변수 묶기 | 매개변수가 3개 이상 반복 |

```
Before (OCP 위반):
  신규 타입 추가 -> 기존 switch 문 수정 -> 기존 코드 변경 -> 회귀 버그 위험

After (OCP 준수):
  신규 타입 추가 -> 새 클래스 추가 -> 기존 코드 무변경 -> 안전
```

- **📢 섹션 요약 비유**: 조건문은 새 메뉴를 추가할 때마다 주방 레이아웃을 바꾸는 것이고, 다형성은 새 요리사를 고용하는 것이다. 주방은 그대로, 메뉴만 늘어난다.

---

## Ⅳ. 실무 적용 및 실무자 판단
1. **테스트 작성**: 기존 조건문 커버하는 단위 테스트 먼저 작성
2. **인터페이스 추출**: 공통 행동을 인터페이스로 정의
3. <strong>구현 클래스 생성</strong>: 각 분기를 별도 클래스로 분리
4. **조건문 교체**: if-else를 팩토리 메서드 또는 DI (Dependency Injection: 의존성 주입) 로 교체
5. **테스트 재실행**: 동일 결과 확인

모든 if-else를 다형성으로 전환하는 것은 오버엔지니어링이다:

```
적합한 경우:
  ✅ 동일 분기가 3개 이상 메서드에 반복
  ✅ 새 타입 추가 빈도가 높음
  ✅ 각 타입의 행동이 상당히 다름

부적합한 경우:
  ❌ 단순 null 체크
  ❌ 일회성 비즈니스 예외 처리
  ❌ 분기가 2개이고 확장 가능성 없음
```

"리팩토링의 목적은 무엇인가?" — 답은 **"동작 변경 없이 코드 구조를 개선하여 미래 변경 비용을 낮추는 것"** 이다. 조건문->다형성 전환은 그 대표 사례로, SOLID 원칙 중 OCP와 SRP (Single Responsibility Principle: 단일 책임 원칙) 를 동시에 실현한다.

### 판단 체크리스트
1. 변경 전 동작을 고정할 테스트가 준비되었는가?
2. 냄새의 원인이 구조 문제인지 일회성 구현인지 구분했는가?
3. 리팩토링 단위를 작게 나눠 롤백 가능하게 했는가?
4. 명명·모델·패키지 경계가 함께 개선되는가?

- **📢 섹션 요약 비유**: 스위스 아미 나이프(조건문)는 하나로 다 되지만 날이 무뎌지면 전체를 교체해야 한다. 전문 도구 세트(다형성)는 필요한 도구만 교체하거나 추가하면 된다.

---

## Ⅴ. 기대효과 및 결론
Replace Conditional with Polymorphism 리팩토링의 효과:

- <strong>OCP 달성</strong>: 새 타입 추가 시 기존 코드 변경 없음
- **코드 중복 제거**: 동일 switch 패턴이 여러 메서드에서 제거됨
- **테스트 용이성**: 각 타입별 독립 단위 테스트 가능
- <strong>가독성 향상</strong>: 각 클래스가 단일 타입의 행동만 담당 (SRP 준수)

GoF (Gang of Four) 패턴과의 연결:

| 리팩토링 기법 | 연결되는 GoF 패턴 |
|:---|:---|
| 알고리즘 교체 (외부 결정) | Strategy Pattern |
| 내부 상태 전이 | State Pattern |
| 객체 생성 분리 | Factory Method Pattern |
| 타입별 연산 추가 | Visitor Pattern |

심화 학습에서 이 리팩토링은 <strong>"기술 부채 해소와 설계 품질 향상을 동시에 달성하는 실천 기법"</strong> 으로 자주 출제된다. 코드 예시와 함께 전후를 비교 서술하면 높은 점수를 얻을 수 있다.

확장 방향은 ① 정적 분석 자동화, ② 아키텍처 적합성 검증, ③ 작은 단위의 상시 리팩토링 문화 정착이다.

- **📢 섹션 요약 비유**: 다형성으로의 전환은 회사 규정집(if-else)을 없애고 각 부서(클래스)가 자기 업무 방식을 자율적으로 처리하게 하는 것이다. 새 부서가 생겨도 규정집은 건드리지 않는다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Refactoring (리팩토링) | 동작 변경 없는 코드 구조 개선 |
| 상위 개념 | OCP (Open/Closed Principle) | 확장에 열리고 수정에 닫힌 원칙 |
| 연관 개념 | Strategy Pattern (전략 패턴) | 알고리즘을 교체 가능한 클래스로 분리 |
| 연관 개념 | State Pattern (상태 패턴) | 내부 상태 전이에 따른 행동 변화 |
| 연관 개념 | Factory Method | 타입에 맞는 구현체 생성 분리 |
| 하위 개념 | Polymorphism (다형성) | 동일 인터페이스로 다양한 구현 교체 |

### 📈 관련 키워드 및 발전 흐름도
조건문 냄새 -> 조건문을 다형성으로 전환 -> 전략/상속 분기 제거

### 👶 어린이를 위한 3줄 비유 설명
1. "강아지면 짖고, 고양이면 야옹하고, 새면 짹짹해"라고 매번 확인하는 대신, 동물에게 직접 "소리내봐!"라고 시키는 거야.
2. 새 동물(새 타입)이 생겨도 기존 코드는 바꾸지 않고, 그 동물만 "소리내봐" 방법을 알면 돼!
3. 이게 바로 다형성(Polymorphism)이야—"뭐야?"가 아니라 "해봐!"가 핵심이야.
