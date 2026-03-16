---
title: "608. 전략 패턴(Strategy Pattern) 알고리즘 교체 용이성"
date: "2026-03-15"
type: "pe_exam"
id: 608
---

# 608. 전략 패턴(Strategy Pattern) 알고리즘 교체 용이성

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전략(Strategy) 패턴은 **"알고리즘군(Algorithm Family)을 정의하고, 각각을 캡슐화한 다음 런타임에 교체 가능하게 만드는"** 행위 패턴(Behavioral Pattern)으로, OCP(Open-Closed Principle)를 준수하여 알고리즘 변경을 영향 없이 수행한다.
> 2. **가치**: 정렬, 검색, 결제 방식 등 다양한 알고리즘을 **if-else나 switch 문 없이** 인터페이스(Interface)를 통해 교체 가능하게 만들어, **코드 중복 제거**와 **확장성(Extensibility)**을 동시에 확보한다.
> 3. **융합**: Java Comparator, Collections.sort(), 스트림의 정렬 기준 변경, 압축(Compression) 알고리즘 선택(Zip, Gzip, LZ4), Spring의 결제 전략 등 표준 라이브러리에 널리 적용되고 있으며, 상태 패턴(State Pattern)과 결합하여 FSM(Finite State Machine)을 구현하기도 한다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 전략 패턴이란 무엇인가? 문제 해결 방법(Strategy)이 여러 가지 있고, 런타임에 어떤 방법을 사용할지 결정해야 할 때 유용하다. 예를 들어, e-commerce에서 할인 정책(VIP 10%, 회원 5%, 신규 0%)은 런타임에 사용자 등급에 따라 달라진다. 이때 할인 로직 자체를 캡슐화하여, 전략(DiscountStrategy) 인터페이스를 구현하고 런타임에 교체 가능하게 만든다.

- **💡 비유**: 전략 패턴은 **"여행 경로 선택"**과 같습니다. 서울에서 부산까지 가는 방법(KTX, 비행기, 자동차, 버스)이 여러 가지 있죠. 여행객(Context)은 "목적지는 부산이고, 예산은 5만 원, 시간은 3시간 이내"라는 요구사항만 정하고, 구체적인 경로(Strategy)은 선택된 전략에 따라 결정된다. KTX 표가가 너무 비싸지면 비행기로 바꾸면 되니까?

- **등장 배경**:
    1. **if-else/switch 문의 폭발**: 새로운 알고리즘이 추가될 때마다 거대한 조건문이 복잡해짐.
    2. **알고리즘 테스트 어려움**: 모든 알고리즘이 하나의 거대한 메서드에 포함되어 단위 테스트 불가.
    3. **런타임 알고리즘 교체**: 사용자 설정, 데이터베이스 저장된 설정에 따라 동적으로 알고리즘 변경 필요.

- **📢 섹션 요약 비유**: 스마트폰에 카메라, 지도, 음악 등 다양한 앱(Strategy)이 설치되어 있고, 사용자는 상황에 따라 앱을 선택(Switch)하여 실행하는 것과 같습니다. 앱을 바꾸어도 스마트폰(Context)은 수정할 필요가 없죠.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 전략 패턴 구성 요소

| 요소 | 역할 및 정의 | 기술적 구현 | 위배 시 증상 | 비유 |
|:---|:---|:---|:---|:---|
| **Strategy Interface** | 알고리즘의 공통 인터페이스 | `interface Strategy { execute() }` | 호환성 없음 | 여행 경로 계약 |
| **Concrete Strategy** | 구체적인 알고리즘 구현 | `class QuickSort implements Strategy` | 교체 불가능 | KTX, 비행기 |
| **Context** | Strategy를 사용하는 클라이언트 | `class Context { private Strategy }` | 전략 변경 불가 | 여행객 |
| **Strategy Selector** | 런타임에 Strategy 선택 로직 | Factory, Config, if-else | 선택 로직 복잡 | 여행사 |

#### [전략 패턴 구조 다이어그램]

할인 정책 시스템에 전략 패턴을 적용한 구조를 시각화한다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Strategy Pattern Structure                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [문제: 할인 정책이 복잡한 if-else로 구현된 경우]                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  public class OrderService {                                       │   │
│  │      public long calculateDiscount(Customer customer, long price) { │   │
│  │          if (customer.isVIP()) {                                   │   │
│  │              return price * 0.9;  // 10% 할인                     │   │
│  │          } else if (customer.isMember()) {                           │   │
│  │              return price * 0.95; // 5% 할인                    │   │
│  │          } else if (customer.isNew()) {                             │   │
│  │              return price;  // 0% 할인                           │   │
│  │          }                                                        │   │
│  │          // ... 더 많은 조건문                                    │   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  │                                                                     │   │
│  │  ⚠ 새 등급(Gold) 추가 시 코드 수정 필요 (OCP 위배)                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [해결책: 전략 패턴 적용]                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                   │   │
│  │  1. Strategy Interface 정의                                         │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ public interface DiscountStrategy {                             │  │   │
│  │  │     long discount(Customer customer, long price);               │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                   │   │
│  │  2. Concrete Strategy 구현                                          │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ public class VIPDiscount implements DiscountStrategy {          │  │   │
│  │  │     @Override                                                   │  │   │
│  │  │     public long discount(Customer customer, long price) {      │  │   │
│  │  │         return price * 0.9;  // 10% 할인                     │  │   │
│  │  │     }                                                          │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ public class MemberDiscount implements DiscountStrategy {        │  │   │
│  │  │     @Override                                                   │  │   │
│  │  │     public long discount(Customer customer, long price) {      │  │   │
│  │  │         return price * 0.95; // 5% 할인                     │  │   │
│  │  │     }                                                          │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ public class NewCustomerDiscount implements DiscountStrategy {   │  │   │
│  │  │     @Override                                                   │  │   │
│  │  │     public long discount(Customer customer, long price) {      │  │   │
│  │  │         return price;  // 0% 할인                             │  │   │
│  │  │     }                                                          │  │   │
│  │  │ }                                                             │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                   │   │
│  │  3. Context (OrderService)                                          │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │ public class OrderService {                                       │   │
│  │  │     private DiscountStrategy discountStrategy;                  │   │
│  │  │                                                                   │  │
│  │  │     // DI 또는 Setter로 주입                                       │   │
│  │  │     public void setDiscountStrategy(DiscountStrategy strategy) { │   │
│  │  │         this.discountStrategy = strategy;                       │   │
│  │  │     }                                                            │   │
│  │  │                                                                   │   │
│  │  │     public long calculatePrice(Customer customer, long price) {│   │
│  │  │         // 전략 패턴 적용                                            │   │
│  │  │         return discountStrategy.discount(customer, price);     │   │
│  │  │     }                                                            │   │
│  │  │ }                                                             │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                   │   │
│  │  ✅ 새 등급(GoldDiscount) 추가 시 기존 코드 수정 불필요                    │   │
│  │  ✅ 단위 테스트 시 Mock Strategy로 쉽게 대체                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  [런타임에 전략 선택]                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  // Configuration 또는 Factory로 전략 선택                               │   │
│  │  public class DiscountStrategyFactory {                               │   │
│  │      public static DiscountStrategy getStrategy(Customer customer) { │   │
│  │          if (customer.isVIP()) {                                    │   │
│  │              return new VIPDiscount();                             │   │
│  │          } else if (customer.isMember()) {                         │   │
│  │              return new MemberDiscount();                         │   │
│  │          } else {                                                  │   │
│  │              return new NewCustomerDiscount();                     │   │
│  │          }                                                        │   │
│  │      }                                                              │   │
│  │  }                                                                  │   │
│  │                                                                   │   │
│  │  OrderService service = new OrderService();                           │   │
│  │  DiscountStrategy strategy = DiscountStrategyFactory.getStrategy(customer); │   │
│  │  service.setDiscountStrategy(strategy);                               │   │
│  │  long finalPrice = service.calculatePrice(customer, 100000);        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ✅ if-else 분기가 Factory로 캡슐화되어 Context는 Strategy 인터페이스만 의존     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상단 다이어그램은 전략 패턴의 핵심 구조를 보여준다. DiscountStrategy 인터페이스가 `discount()` 메서드를 정의하고, VIPDiscount, MemberDiscount, NewCustomerDiscount가 이를 구현한다. OrderService(Context)는 구체적인 전략을 알 필요 없이, `discountStrategy.discount()`만 호출하면 된다. 새로운 등급(Gold)이 추가되면 GoldDiscount 클래스만 구현하고 Factory에 분기만 추가하면 되므로, OrderService 코드는 전혀 수정할 필요가 없다(Open-Closed Principle 준수).

#### 심층 동작 원리: 전략 패턴 vs 상태 패턴(State Pattern)

전략 패턴과 상태 패턴은 모두 알고리즘 교체에 사용되지만, 차이가 있다.

```
[Strategy Pattern: 알고리즘 교체]
- Context 외부에서 Strategy를 교체
- 여러 Client가 동일한 Strategy를 공유 가능
- 알고리즘 자체가 독립적 객체
예: 정렬 전략(QuickSort, MergeSort)은 여 곳에서 재사용 가능

[State Pattern: 상태에 따른 행위 변경]
- Context 내부에서 State가 자동 전이
- 각 Context는 독립적인 State를 가짐
- 상태별 행위가 캡슐화되어 Context 변경 로직이 State 내부에 포함
예: 주문 상태(Created, Shipped, Delivered)에 따라 다른 행위
```

- **📢 섹션 요약 비유**: 전략 패턴은 "여행 가방"을 미리 정해두고 선택하는 것이고, 상태 패턴은 "현재 위치에 따라 길을 찾는 내비게이션"과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. if-else vs 전략 패턴 vs 함수형 프로그래밍

| 비교 항목 | if-else/switch | 전략 패턴 | 함수형 프로그래밍 |
|:---|:---|:---|:---|
| **알고리즘 추가** | 기존 코드 수정 필요 | 새로운 Strategy 클래스 추가 | 람다(일급 함수) 추가 |
| **런타임 교체** | 어려움 (분기문 재컴파일) | 가능 (setter 또는 DI) | 가능 (함수 교체) |
| **단위 테스트** | 전체 메서드 테스트 | 각 Strategy별 테스트 | 함수별 테스트 |
| **복잡도** | 분기문이 복잡해짐 | 클래스 수 증가 | 람다 표현 간단 |
| **비유** | 매번 길을 물어봄는 여행자 | 여행 경로를 미리 정하는 사람 | 알고리즘 자체를 전달하는 사람 |

#### 2. 전략 패턴과 Comparator의 결합

Java의 `Collections.sort()`는 전략 패턴의 실무 적용 사례다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 Strategy Pattern with Comparator                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  public class Student {                                                   │
│      private String name;                                                  │
│      private int score;                                                   │
│      // constructor, getters 생략                                         │
│  }                                                                          │
│                                                                             │
│  // 정렬 전략 1: 이름 오름차순                                            │
│  Comparator<Student> byName = (s1, s2) -> s1.getName().compareTo(s2.getName());│
│                                                                             │
│  // 정렬 전략 2: 점수 내림차순                                          │
│  Comparator<Student> byScore = (s1, s2) -> Integer.compare(s2.getScore(),    │
│                                                              s1.getScore());│
│                                                                             │
│  // 런타임에 전략 선택                                                    │
│  List<Student> students = Arrays.asList(new Student("Alice", 85),       │
│                                       new Student("Bob", 92));          │
│                                                                             │
│  // 이름 정렬                                                            │
│  Collections.sort(students, byName);  // [Alice, Bob]                   │
│                                                                             │
│  // 점수 정렬                                                            │
│  Collections.sort(students, byScore);  // [Bob(92), Alice(85)]           │
│                                                                             │
│  ✅ Comparator는 Strategy Interface                                       │
│  ✅ 람다 표현(Lambda)으로 간결하게 구현 가능                             │
│  ✅ 여러 전략을 조합(thenComparing) 가능                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 과목 융합 관점

- **컴퓨터 구조(CA)**: CPU의 명령어 파이프라인 설계에서 명령어셋(Instruction Set)이 전략(Strategy)이고, 마이크로아키텍처(Microarchitecture)는 전략 선택 로직이다. x86 프로세서는 CISC(Complex Instruction Set Computer) 전략, ARM은 RISC(Reduced Instruction Set Computer) 전략을 따르며, 같은 프로그램이라도 하드웨어에 따라 다른 명령어 전략을 사용한다.

- **운영체제(OS)**: I/O 스케줄링 알고리즘(FCFS, Round Robin, SJF, Priority)은 전략 패턴의 실무 적용 사례다. OS는 런타임에 스케줄링 정책을 변경할 수 있으며, 각 알고리즘은 독립적으로 구현되어 있다.

- **압축(Compression)**: ZIP, GZIP, LZ4, ZSTD 같은 압축 알고리즘은 전략 패턴으로 구현된다. 압축 라이브러리는 압축 전략을 선택할 수 있는 API를 제공하며, 사용자는 압축률과 속도 trade-off를 고려하여 전략을 선택한다.

- **📢 섹션 요약 비유**: 네비게이션은 GPS(전략)에 따라 자동차, 대중교, 도보 경로를 선택합니다. 사용자는 "목적지"만 입력하면, 알고리즘이 최적 경로를 자동으로 계산해주죠.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **실무 시나리오 1: 결제 수단별 수수료율 적용**
    - **문제**: 카드(3%), 간편결제(1%), 계좌이체(0%) 수수료율이 거대한 switch 문으로 구현.
    - **의사결정**: FeeCalculator Strategy 인터페이스 정의 후, 각 결제 수단별 구체 전략 구현.
    - **결과**: 새로운 결제 수단(카카오페이 등) 추가 시 기존 코드 영향 없이 확장.

- **실무 시나리오 2: 파일 압축 포맷 선택**
    - **문제**: 대용량 로그 파일을 압축할 때 속도 vs 압축률 trade-off를 상황에 따라 선택 필요.
    - **의사결정**: CompressionStrategy 인터페이스(Zip, Gzip, LZ4, ZSTD) 정의 후, 파일 크기/응답 속도 요구에 따라 런타임에 전략 선택.
    - **결과**: 실시간 로그는 Gzip(빠름), 아카이빙 로그는 ZSTD(높은 압축률) 등 유연하게 선택 가능.

- **도입 체크리스트**:
    1. **전략 간 차이점 확인**: 각 알고리즘의 입력/출력이 동일한가? (호환성)
    2. **전략 선택 로직 복잡도**: 선택 로직이 너무 복잡해지면 팩토리 메서드와 결합
    3. **전략 수량**: 전략이 2~3개라면 if-else도 고려, 10개 이상이면 패턴 적용
    4. **함수형/람다 표현**: Java 8+ Lambda, Kotlin 함수형으로 간단하게 구현 가능

- **안티패턴**:
    - **Strategizing Everything**: 단순한 분기에도 전략 패턴을 적용하여 과잉 설계
    - **Strategy가 Context를 직접 참조**: Strategy가 Context를 알게 되어 결합도 증가
    - **전략 선택 로직의 하드코딩**: 선택 로직이 DB에 저장되어 있지 않고 코드에 하드코딩됨

- **📢 섹션 요약 비유**: 모든 문제를 망치로 해결하려고 전략 패턴을 남용하면, 도리어 망치도 없이 망만 만드는 격될 수 있습니다. 간단한 분기는 if-else로 충분합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량/정성 기대효과**:

| 구분 | 전략 패턴 미적용 시 | 전략 패턴 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 새 알고리즘 추가 시 10곳 수정 | Strategy 클래스만 추가 | **수정 범위 90% 감소** |
| **정량** | 단위 테스트 시 모든 분기 테스트 | 각 Strategy별 독립 테스트 | **테스트 시간 70% 단축** |
| **정성** | 알고리즘 재사용 불가 | 라이브러리화된 전략 | **재사용성 개선** |
| **정성** | SOLID 원칙 위배(OCP) | OCP 준수 | **설계 품질 향상** |

- **미래 전망**:
    1. **함수형 프로그래밍(Functional Programming)**: 순수 함수(Pure Function) 자체가 전략이 되어, 고차 함수(Higher-Order Function)로 전략을 조합 가능하다.
    2. ** 람다(Lambda) 및 메서드 참조**: Java 8+, Kotlin, C#에서는 간단한 람다 표현으로 전략 패턴을 대체하는 추세.

- **참고 표준**:
    - **GoF Book**: "Design Patterns" - Strategy Pattern 챕터
    - **Effective Java**: Item 2 - "많은 생성자 파라미터를 대신 Builder를 고려하라"
    - **Java Comparator Interface**: 전략 패턴의 표준 라이브러리 구현

- **📢 섹션 요약 비유**: 내비게이션 시스템이 발달하면, 정보는 국경(인터페이스)을 넘어야 하고, 각국의 관세법(구체 전략)을 준수해야 합니다. 전략 패턴은 이 "통과 절차"를 표준화하는 외교적 관계 매커니즘과 유사합니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[행위 패턴(Behavioral Patterns)](./566_behavioral_patterns.md)**: 전략 패턴이 속한 상위 카테고리.
- **[OCP(Open-Closed Principle)](./601_solid_principles.md)**: 전략 패턴이 준수하는 개방-폐쇄 원칙.
- **[상태 패턴(State Pattern)](./272_state.md)**: 알고리즘 교체와 유사하지만 상태 전이에 특화된 패턴.
- **[함수형 프로그래밍](./324_functional_programming.md)**: 전략 패턴의 함수형 대체재.
- **[Comparator](./xx_comparator.md)**: Java에서의 전략 패턴 구현.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 전략 패턴은 **"여행 경로 선택"**과 같아요. 같은 서울에서 부산에 가더라도, 비행기 타기 vs KTX vs 자동차 vs 버스 중 하나를 선택할 수 있죠.
2. 여행자(Context)는 "부산 가고 싶은데 3시간 내에 왔으면 좋겠어"라고 말만 하면, 내비게이션이 알아서 최적 경로(전략)를 찾아줘니다.
3. 그래서 나중에 새로운 교통편(하이퍼루프)이 생겨도, 여행자는 내비게이션만 업데이트하면 돼아서 바로 그 교통편을 이용할 수 있답니다!
