+++
title = "258-265. GoF 디자인 패턴: 구조 패턴"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 258
+++

# 258-265. GoF 디자인 패턴: 구조 패턴 (Structural Patterns)

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: 구조 패턴(Structural Patterns)은 상속(Inheritance)과 합성(Composition)을 통해 클래스나 객체를 조합하여 더 큰 구조를 설계하는 패턴으로, 시스템의 인터페이스 불일치를 해소하고 복잡성을 관리하며 메모리 및 구조적 효율성을 극대화하는 것을 목적으로 한다.
> 2. **가치**: 시스템의 결합도(Coupling)를 낮추고 유연성을 제공하여, 요구사항 변경 시 기존 코드 수정 없이 새로운 구조를 확장할 수 있는 유지보수성(Maintainability)을 확보하고, 대규모 시스템에서의 구조적 복잡도를 낮춘다.
> 3. **융합**: GoF (Gang of Four)의 23가지 디자인 패턴 중 생성 패턴(Creational)과 행위 패턴(Behavioral) 사이의 가교 역할을 하며, MSA (Microservice Architecture)의 API Gateway, ORM (Object-Relational Mapping)의 로딩 전략, UI 컴포넌트 트리 구조 등 현대 소프트웨어 아키텍처의 근간을 이룬다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
구조 패턴(Structural Patterns)은 소프트웨어 공학에서 시스템의 구조를 설계하기 위해 클래스와 객체를 어떻게 조합하고, 합성(Composition)하고, 상속(Inheritance)할 것인가를 다루는 디자인 패턴입니다. 단순히 라이브러리를 사용하는 것을 넘어, 작은 인터페이스들이 어떻게 연결되어 거대한 시스템을 이루는지에 대한 '구조적 청사진'을 제공합니다.

**💡 비유**
이해를 돕기 위해 건축물을 짓는 과정에 비유해 보겠습니다.
*   **Adapter (어댑터)**: 서로 다른 규격의 파이프를 연결하는 '이음새(커넥터)' 역할입니다.
*   **Facade (퍼사드)**: 건물 내부의 복잡한 배선과 기계실을 숨기고, 사용자에게는 편리한 '제어판' 하나만 보여주는 역할입니다.
*   **Composite (컴포지트)**: 벽돌(단일 객체)과 벽돌로 쌓은 벽(복합 객체)을 모두 '건축 자재'라는 동일한 단위로 다루는 것입니다.

**등장 배경**
1.  **기존 한계**: 소프트웨어 규모가 커지면서 모듈 간 인터페이스가 불일치하거나, 상속(Inheritance)의 과도한 사용导致的 클래스 폭발(Class Explosion) 문제가 발생했습니다. 또한, 수천 개의 객체를 생성할 때 메모리 낭비가 심각했습니다.
2.  **혁신적 패러다임**: '구조' 자체를 변경하지 않고도 인터페이스를 변환하거나(Adapter), 객체 간의 연결 구조를 트리 형태(Composite)로 재귀적으로 처리하거나, 기능을 동적으로 확장(Decorator)하는 패러다임이 도입되었습니다.
3.  **현재의 비즈니스 요구**: 현재의 MSA (Microservice Architecture) 환경에서는 레거시 시스템의 인터페이스를 변환하거나, 복잡한 클라우드 리소스를 추상화하는 데 핵심적으로 사용됩니다.

**📢 섹션 요약 비유**
구조 패턴은 **서로 다른 모양의 레고 블록들을 끼워 맞추기 위해 특수한 커넥터(어댑터)를 만들거나, 수천 개의 블록을 하나의 큰 모델처럼 다루기 위해 묶음(컴포지트)으로 관리하는 '조립식 설계 도구'**와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 7가지 패턴 분석**
구조 패턴은 크게 클래스 간 구조를 다루는 패턴(상속 이용)과 객체 간 구조를 다루는 패턴(객체 합성 이용)으로 나뉩니다. 대표적인 7가지 패턴의 상세 분석입니다.

| 패턴명 (영문) | 핵심 역할 | 내부 동작 메커니즘 | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Adapter (어댑터)** | 인터페이스 변환 | 기존 클래스(Client)와 필요한 인터페이스(Target) 사이의 중개역. 상속(Inheritance) 또는 합성(Composition) 사용 | 클래스 어댑터 vs 객체 어댑터 | 돼지코 (220V $\to$ 110V) |
| **Bridge (브리지)** | 추상과 구현 분리 | 기능 계층(Abstraction)과 구현 계층(Implementation)을 분리하여 독립적으로 확장 가능. 합성(Composition) 활용 | JDBC (Java Database Connectivity) | 리모컨(기능)과 건전지(구현) 분리 |
| **Composite (컴포지트)** | 트리 구조 관리 | 개별 객체(Leaf)와 복합 객체(Composite)를 동일한 인터페이스(Component)로 처리. 재귀(Recursive) 호출 | DOM (Document Object Model) Tree | 파일(단일)과 폴더(복합) 관리 |
| **Decorator (데코레이터)** | 동적 책임 추가 | 상속 없이 객체에 기능을 '래핑(Wrapping)'하여 추가. 런타임에 유연한 기능 조합 가능 | Java I/O Stream (`new BufferedReader`) | 커피에 시럽, 휘핑크림 추가 |
| **Facade (퍼사드)** | 단순화된 창구 제공 | 복잡한 서브시스템들의 연결 로직을 하나의 고수준 인터페이스로 캡슐화 | Spring MVC `DispatcherServlet` | PC 전원 버튼 (내부 복잡함 은폐) |
| **Flyweight (플라이웨이트)** | 메모리 최적화 | 객체의 내부 상태(Intrinsic)는 공유하고, 외부 상태(Extrinsic)는 별도 관리하여 메모리 절약 | String Constant Pool, 글자 폰트 | 공용 문자 활판 인쇄 |
| **Proxy (프록시)** | 접근 제어 및 대리 | 실제 객체(RealSubject)에 대한 대리인으로 접근 제어, 지연 로딩(Lazy Loading), 로깅 등 수행 | Spring AOP (Aspect-Oriented Programming) | 스타 대신 매니저가 일정 조율 |

**2. 심층 동작 원리: 클래스 구조 vs 객체 구조**

```ascii
      [ 상속 (Inheritance) 기반 구조 ]      [ 합성 (Composition) 기반 구조 ]
           (컴파일 타임에 결정)                  (런타임에 유연하게 결정)

   +------------+                      +------------+       uses
   |   Target   | <------------------- |  Adapter   | ------------> +-------------+
   +------------+                      +------------+                |  Adaptee    |
        ^                                 (Wrapper)                  +-------------+
        |                                                            (Legacy)
   +------------+
   | ConcreteTarget|
   +------------+

   vs. Composite Pattern (Object Composition)

   +-------------------------+
   |      Component          | <--- Abstract / Interface
   +-------------------------+
   ^          ^
   |          | inherits
   |          +------------------------------------------+
   |                                                     |
+----------------+                              +------------------+
|      Leaf      |                              |     Composite    | <--- has list of Components
| (Primitive)    |                              +------------------+
+----------------+                                        ^
       |                                                /   \
       +----------------------------------------------+     +---> [Leaf]
                Recursive Structure (Tree)
```

**해설**:
위 다이어그램은 구조 패턴의 두 가지 접근 방식을 보여줍니다.
1.  **좌측 (상속/Adapter)**: 컴파일 타임에 관계가 고정됩니다. 강력한 결합을 가지며, Adapter처럼 단순히 인터페이스를 변환하는 데 유리합니다.
2.  **우측 (합성/Composite)**: `Composite` 클래스가 `Component` 인터페이스를 구현하면서 동시에 `Component`들의 목록(List)을 가지는 구조입니다. 이를 통해 '부분(Part)과 전체(Whole)'의 계층 구조를 표현합니다. 파일 시스템에서 폴더가 폴더를 포함하고 파일을 포함하는 방식이 대표적입니다. 이 방식은 런타임에 객체 그룹을 동적으로 구성할 수 있어 유연성이 훨씬 높습니다.

**3. 핵심 코드 스니펫: 데코레이터 패턴 (Decorator Pattern)**
데코레이터는 상속을 피하고 조합(Composition)을 통해 기능을 확장하는 대표적인 예입니다.

```java
// 1. 공통 인터페이스
public interface Beverage {
    String getDescription();
    double cost();
}

// 2. 기본 구현체 (Concrete Component)
public class Espresso implements Beverage {
    public String getDescription() { return "에스프레소"; }
    public double cost() { return 2.5; }
}

// 3. 추상 데코레이터 (Component와 동일한 인터페이스 상속)
public abstract class CondimentDecorator implements Beverage {
    // 감싸고 있는 객체(Component)를 합성(Composition)으로 가짐
    protected Beverage beverage; 
}

// 4. 구체적 데코레이터 (Concrete Decorator)
public class Mocha extends CondimentDecorator {
    public Mocha(Beverage beverage) {
        this.beverage = beverage; // 런타임에 객체를 주입받아 감쌈
    }

    public String getDescription() {
        return beverage.getDescription() + ", 모카"; // 책임 위임 + 기능 추가
    }

    public double cost() {
        return beverage.cost() + 0.5; // 가격 추가
    }
}

// Client Usage
Beverage drink = new Espresso();
drink = new Mocha(drink); // 실행 중에 동적으로 기능 확장
drink = new Whip(drink);  // 또 다른 데코레이터로 확장 가능
```

**해설**:
위 코드는 `Open-Closed Principle (OCP)`을 완벽하게 따릅니다. `Espresso` 클래스의 코드를 수정하지 않고도, `Mocha`나 `Whip` 같은 데코레이터 클래스를 통해 런타임에 새로운 기능을 추가할 수 있습니다. 만약 상속을 사용했다면, "에스프레소+모카", "에스프레소+모카+휘핑", "디카페인+모카" 등 조합의 수만큼 클래스가 기하급수적으로 늘어나는 문제(Class Explosion)를 해결합니다.

**📢 섹션 요약 비유**
이 구조는 **자동차 조립 라인**과 같습니다. **브리지(Bridge)**는 차체와 엔진을 분리하여 어떤 엔진이든 어떤 차체에도 장착하게 하고, **데코레이터(Decorator)**는 기본 차량에 썬루프, 네비게이션을 옵션으로 덧붙이는 것입니다. **컴포지트(Composite)**는 자동차 부품 하나를 주문하든, 완성차를 주문하든 '주문'이라는 동일한 프로세스로 관리하는 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 구조 패턴의 비교 분석 (정량적/구조적 관점)**

| 비교 항목 | Adapter Pattern | Decorator Pattern | Proxy Pattern | Facade Pattern |
|:---|:---|:---|:---|:---|
| **목적** | 인터페이스 불일치 해소 | 객체의 기능(책임) 동적 확장 | 접근 제어, 성능 최적화 | 복잡한 서브시스템 단순화 |
| **구조** | One-to-One (1:1 매핑) | One-to-Many (래핑 체인) | One-to-One (대리 행위) | One-to-Many (통합 창구) |
| **시점** | 설계 시 또는 통합 시 | 런타임(Run-time) | 런타임(Run-time) | 설계 시 주로 구현 |
| **대상 변경** | 변경 불가능한 인터페이스를 감쌈 | 핵심 기능에 부가 기능을 덧씀 | 실제 객체의 참조를 보유 | 여러 클래스의 메서드를 통합 |
| **성능 영향** | 거의 없음 (단순 호출 위임) | 메서드 호출 깊이 증가로 인한 미세 오버헤드 | 초기 접근 지연 가능(Lazy Init) | 서브시스템 호출 구조에 따라 다름 |

**2. 타 영역 융합 분석**

*   **시스템 엔지니어링 & 아키텍처 (MVC / MVP / MVVM)**
    *   **Facade Pattern**은 Spring Framework와 같은 웹 애플리케이션의 **Front Controller (e.g., `DispatcherServlet`)** 핵심 원리입니다. 사용자의 요청을 받아 내부의 복잡한 컨트롤러, 서비스, DAO 계층으로 라우팅하는 '단일 진입점(Single Entry Point)' 역할을 수행하여 시스템의 결합도를 낮춥니다.
    *   **Composite Pattern**은 UI 개발(Android, iOS, Web)에서 필수적입니다. 화면을 구성하는 버튼, 텍스트 상자 같은 기본 컴포넌트(Leaf)와 이들을 담는 패널, 레이아웃(Composite)이 동일한 `draw()`나 `render()` 메서드를 가지도록 설계되어, 화면 전체를 재귀적으로 그리는 로직을 단순화합니다.

*   **데이터베이스 및 ORM (Object-Relational Mapping)**
    *   **Proxy Pattern**은 JPA (Java Persistence API)나 Hibernate에서 **지연 로딩(Lazy Loading)**을 구현하는 핵심 메커니즘입니다. 실제 데이터베이스에 쿼리를 날리는 무거운 엔티티 객체를 즉시 로드하는 대신, 가벼운 프록시 객체를 먼저 반환하고, 실제 데이터가 필요한 시점에야 로드를 수행하여 성능을 최적화합니다.
    *   **Flyweight Pattern**은 데이터베이스의 **Connection Pool** 개념과 연결됩니다. 모든 사용자가 매번 새로운 Connection 객체를 생성하면 자원이 고갈되므로, 생성된 Connection(내부 상태)을 공유하고 사용 상태(외부 상태)만 관리하여 자원을 재사용합니다.

**📢 섹션 요약 비유**
이러한 비교는 **집짓기와 전자기기 관리**의 차이와 같습니다. **어댑터**는 110V 가전제품을 220V 콘센트에 꽂는 '해결사' 역할이고, **데코레이터**는 스마트폰 케이스