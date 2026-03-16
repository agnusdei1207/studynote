---
title: "607. 팩토리 메서드 vs 추상 팩토리(Abstract Factory)"
date: "2026-03-15"
type: "pe_exam"
id: 607
---

# 607. 팩토리 메서드 vs 추상 팩토리(Abstract Factory)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 팩토리 메서드(Factory Method)는 **"객체 생성을 서브클래스에 위임"**하여 생성 로직과 사용 로직을 분리하고, 추상 팩토리(Abstract Factory)는 **"관련 있는 객체 군(Family)을 생성하는 인터페이스"**를 제공하는 생성 패턴(Creational Pattern)이다.
> 2. **가치**: 구체 클래스(Class)에 의존하는 코드를 제거하여 DIP(Dependency Inversion Principle)를 준수하고, 생성 로직의 중복을 방지하며, 클라이언트는 구체적인 구현이 아닌 추상화(Factory)에만 의존하므로 변경에 유연하다.
> 3. **융합**: DAO(Data Access Object) 패턴, JDBC Driver 로딩, 스프링 @Bean 팩토리 등 현대 프레임워크의 핵심 메커니즘이며, 플러그인(Plugin) 아키텍처, 모듈러 모놀리식(Modular Monolith)의 서브도메인 분리에 적용된다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 팩토리 패턴이란 무엇인가? "new 클래스()"를 직접 호출하는 것은 구체 클래스에 강하게 결합(Tight Coupling)되는 것이다. 팩토리 패턴은 객체 생성을 전담하는 "공장(Factory)"을 만들어서, 클라이언트가 무엇을 만들지는 알 필요 없이, 그저 **"제품을 달라고 요청"**만 하게 만든다. 팩토리 메서드는 단일 객체 생성을 위임하고, 추상 팩토리는 관련 객체 군(예: Button + ScrollBar 같은 GUI 컴포넌트)을 생성한다.

- **💡 비유**: 팩토리 패턴은 **"자동차 공장"**과 같습니다. 고객이 "SUV 차량 1대 주문"하면, 공장은 어떤 부품을 조립하고 어떤 엔진을 탑재할지 알아서 완성차를 만들어줍니다. 고객은 생산 라인(Concrete Factory)이 어떻게 돌아가는지 알 필요 없이, 그저 모델명(Interface)만 주문하면 됩니다. 전기 모델에서 가손린 모델로 변경되어도 공장(Factory)만 교체하면 고객 코드는 변경 불필요하죠(OCP 준수).

- **등장 배경**:
    1. **생성 로직의 복잡도 증가**: DB 연결, 네트워크 소켓 등 복잡한 객체 생성 로직이 반복됨.
    2. **구체 클래스에 대한 의존성 문제**: `new MySQLConnection()`과 같은 코드는 특정 DB 벤더에 종속됨.
    3. **객체 Family의 일관성**: Windows 스타일의 Button + ScrollBar, macOS 스타일의 Button + ScrollBar처럼 관련 객체 군이 일관되게 생성되어야 할 때.

- **📢 섹션 요약 비유**: 피자 가게에서 고객이 "피자 주문"하면 피자 만드는 기계(Factory)가 도우, 토핑, 치즈, 크러스트를 조립하여 완성 피자를 내놓는 것과 같습니다. 고객은 조립 과정을 알 필요 없죠.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 팩토리 패턴 구성 요소

| 요소 | 팩토리 메서드(Factory Method) | 추상 팩토리(Abstract Factory) |
|:---|:---|:---|
| **의도** | 단일 객체 생성 지연 | 관련 객체군(Family) 생성 |
| **구조** | 생성자를 서브클래스로 위임 | 인터페이스와 구체 팩토리 분리 |
| **사용 시점** | 생성 타입이 미리 확정 | 제품군이 여러 family 존재 |
| **예시** | DAO, Repository 생성 | GUI 컴포넌트(JFX/Swing), DB Driver |
| **비유** | 공장장이 생산 라인 지정 | 부품 공급망( tire + engine) |

#### [팩토리 메서드 vs 추상 팩토리 비교 다이어그램]

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│           Factory Method vs Abstract Factory Comparison                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Factory Method Pattern] - 단일 객체 생성                                 │
│                                                                             │
│  문제: 클라이언트가 구체적 데이터베이스(MySQL)에 의존함                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  // ❌ Bad Code - 직접 생성                                        │   │
│  │  public class OrderService {                                       │   │
│  │      private DatabaseConnection db = new MySQLConnection();       │   │
│  │  }                                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  해결: 팩토리 메서드로 생성 캡슐화                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  // ✅ Good Code - Factory Method                                   │   │
│  │  public abstract class DatabaseFactory {                           │   │
│  │      // Factory Method                                              │   │
│  │      public abstract DatabaseConnection createConnection();       │   │
│  │  }                                                                │   │
│  │                                                                   │   │
│  │  public class MySQLFactory extends DatabaseFactory {              │   │
│  │      @Override                                                     │   │
│  │      public DatabaseConnection createConnection() {               │   │
│  │          return new MySQLConnection();                             │   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  │                                                                   │   │
│  │  public class OrderService {                                       │   │
│  │      private DatabaseFactory factory;                              │   │
│  │      // Constructor Injection                                       │   │
│  │      public OrderService(DatabaseFactory factory) {                │   │
│  │          this.factory = factory;                                   │   │
│  │      }                                                            │   │
│  │      public void process() {                                       │   │
│  │          DatabaseConnection db = factory.createConnection();       │   │
│  │          // MySQL, PostgreSQL, Oracle 등으로 교체 가능              │   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ✅ OCP 준수: 새 DB를 추가하려면 새로운 Factory만 구현                         │
│  ✅ DIP 준수: OrderService는 추상화(DatabaseFactory)에 의존                 │
│                                                                             │
│  [Abstract Factory Pattern] - 관련 객체군(Family) 생성                      │
│                                                                             │
│  문제: Windows 스타일 vs macOS 스타일 GUI 컴포넌트                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  // ❌ Bad Code - 클라이언트가 구체 클래스에 의존               │   │
│  │  public class UIFactory {                                         │   │
│  │      public Button createButton() {                               │   │
│  │          return new WindowsButton();  // Windows에 종속          │   │
│  │      }                                                            │   │
│  │      public ScrollBar createScrollBar() {                        │   │
│  │          return new WindowsScrollBar();                         │   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  해결: 추상 팩토리로 일관된 컴포넌트군 생성                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  // ✅ Good Code - Abstract Factory                                 │   │
│  │                                                                   │   │
│  │  // 추상 팩토리 (Abstract Factory)                                  │   │
│  │  public abstract class GUIFactory {                                 │   │
│  │      public abstract Button createButton();                         │   │
│  │      public abstract ScrollBar createScrollBar();                 │   │
│  │  }                                                                │   │
│  │                                                                   │   │
│  │  // 구체 팩토리 (Concrete Factory 1 - Windows)                       │   │
│  │  public class WindowsFactory extends GUIFactory {                   │   │
│  │      @Override                                                     │   │
│  │      public Button createButton() {                               │   │
│  │          return new WindowsButton();                               │   │
│  │      }                                                            │   │
│  │      @Override                                                     │   │
│  │      public ScrollBar createScrollBar() {                         │   │
│  │          return new WindowsScrollBar();                           │   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  │                                                                   │   │
│  │  // 구체 팩토리 (Concrete Factory 2 - macOS)                         │   │
│  │  public class MacFactory extends GUIFactory {                      │   │
│  │      @Override                                                     │   │
│  │      public Button createButton() {                               │   │
│  │          return new MacButton();                                   │   │
│  │      }                                                            │   │
│  │      @Override                                                     │   │
│  │      public ScrollBar createScrollBar() {                         │   │
│  │          return new MacScrollBar();                               │   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  │                                                                   │   │
│  │  // 클라이언트                                                      │   │
│  │  public class Application {                                        │   │
│  │      private GUIFactory factory;                                    │   │
│  │                                                                   │   │
│  │      public Application(GUIFactory factory) {                      │   │
│  │          this.factory = factory;                                    │   │
│  │      }                                                            │   │
│  │                                                                   │   │
│  │      public void createUI() {                                     │   │
│  │          Button button = factory.createButton();                  │   │
│  │          ScrollBar scrollBar = factory.createScrollBar();          │   │
│  │          // button과 scrollBar는 같은 Family(Windows 또는 Mac)│   │
│  │      }                                                            │   │
│  │  }                                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ✅ 일관된 컴포넌트군 보장 (Windows Button + Windows ScrollBar)               │
│  ✅ 새 플랫폼(Linux) 추가 시 LinuxFactory만 구현                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상단 다이어그램은 두 패턴의 근본적 차이를 보여준다. 팩토리 메서드는 **단일 객체(DatabaseConnection)** 생성을 서브클래스(MySQLFactory, PostgreSQLFactory)에 위임한다. 반면 추상 팩토리는 **관련 객체군(Button + ScrollBar)**을 생성하는 인터페이스를 제공한다. 추상 팩토리의 핵심은 **제품 Family가 서로 혼합되지 않도록 보장**하는 것이다. 예를 들어, WindowsFactory는 WindowsButton과 WindowsScrollBar만 생성하므로, Windows 스타일의 일관성이 보장된다.

#### 심층 동작 원리: Factory Method의 다형성(Polymorphism)

팩토리 메서드는 템플릿 메서드(Template Method) 패턴의 일종으로, 상위 클래스(Client)는 알고리즘의 뼈대를 정의하고, 하위 클래스(Concrete Factory)가 구체적인 생성 단계를 구현한다.

```
[Factory Method의 호출 흐름]

1. OrderService.process() 호출
   ↓
2. factory.createConnection() 호출 (Factory Method)
   ↓
3. 런타임에 MySQLFactory 또는 PostgreSQLFactory의 createConnection() 실행
   ↓
4. 구체적인 DatabaseConnection 인스턴스 반환

[Dependency Inversion 적용 전후]

적용 전: OrderService → MySQLConnection (구체적 의존)
적용 후: OrderService → DatabaseFactory → DatabaseConnection (추상화 의존)
```

이 구조에서 DIP(Dependency Inversion Principle)가 준수된다. OrderService는 DatabaseFactory(추상화)에만 의존하며, 구체적인 구현(MySQL, PostgreSQL)은 런타임에 결정된다.

- **📢 섹션 요약 비유**: 피자 가게에서 "고객이 피자 종류를 선택하면, 피자 만드는 기계(Factory)가 자동으로 해당 도우를 선택하여 조립하는 것과 같습니다. 고객은 기계 내부를 알 필요 없죠.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 생성 패턴 간 관계

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 Creational Patterns Relationship                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Factory Method를 활용하는 패턴들                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  ┌──────────────┐    uses    ┌──────────────┐                    │   │
│  │  │ Factory       │──────────▶│ Abstract      │                    │   │
│  │  │ Method        │           │ Factory       │                    │   │
│  │  └───────────────┘            └───────┬───────┘                    │   │
│  │                                      │ implements                 │   │
│  │                         ┌──────────────┴───────────────┐                  │   │
│  │                         ▼                              ▼                  │   │
│  │                  ┌───────────────────────────────┐                   │   │
│  │                  │ ConcreteFactory.createProduct() │◀─ Factory    │   │
│  │                  │ {                               │    Method       │   │
│  │                  │   return new ConcreteProduct(); │                   │   │
│  │                  │ }                               │                   │   │
│  │                  └───────────────────────────────┘                   │   │
│  │                             │ creates                              │   │
│  │                             ▼                                     │   │
│  │                  ┌───────────────────────────────┐                   │   │
│  │                  │ ConcreteProduct               │                   │   │
│  │                  └───────────────────────────────┘                   │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ✅ Abstract Factory가 내부적으로 Factory Method를 사용                     │
│  ✅ Builder가 생성 단계를 제어, Factory Method는 위임                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2. 실무 적용 사례: DAO & Repository 패턴

DAO(Data Access Object) 패턴은 Factory Method의 실무 적용 사례다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DAO/Repository with Factory Method                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [문제]                                                                   │
│  - OrderDAO, ProductDAO, CustomerDAO 등 각 DAO마다 DB 연결 로직 중복         │
│  - MySQL에서 PostgreSQL로 마이그레이션 시 모든 DAO 수정 필요              │
│                                                                             │
│  [해결책: 팩토리 메서드를 통한 추상화]                                   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  // 인터페이스                                                       │   │
│  │  public interface DatabaseFactory {                                   │   │
│  │      Connection createConnection();                                  │   │
│  │  }                                                                  │   │
│  │                                                                   │   │
│  │  // 구체 팩토리                                                       │   │
│  │  @Service                                                            │   │
│  │  public class PostgreSQLFactory implements DatabaseFactory {        │   │
│  │      @Override                                                       │   │
│  │      public Connection createConnection() {                          │   │
│  │          return DriverManager.getConnection("jdbc:postgresql://..."); │   │
│  │      }                                                              │   │
│  │  }                                                                  │   │
│  │                                                                   │   │
│  │  // Repository                                                       │   │
│  │  public class OrderRepository {                                     │   │
│  │      private DatabaseFactory factory;                                │   │
│  │                                                                   │   │
│  │      @Autowired                                                      │   │
│  │      public OrderRepository(DatabaseFactory factory) {               │   │
│  │          this.factory = factory;                                     │   │
│  │      }                                                              │   │
│  │                                                                   │   │
│  │      public Order findById(Long id) {                               │   │
│  │          Connection conn = factory.createConnection();             │   │
│  │          // JDBC 수행                                                │   │
│  │      }                                                              │   │
│  │  }                                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ✅ DB 변경 시 Factory만 교체하면 모든 Repository에 반영                   │
│  ✅ 테스트 시 TestDoubleFactory로 Mock DB 연결 쉽게 대체                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 과목 융합 관점

- **JDBC(Java Database Connectivity)**: `DriverManager.getConnection()`은 Factory Method 패턴의 실무 적용 사례다. 클라이언트는 URL(`jdbc:mysql://localhost`)만 제공하면, DriverManager 내부에서 등록된 JDBC Driver(Concrete Factory) 중 적합한 것을 찾아 Connection 객체를 생성한다.

- **스프링(Spring) 프레임워크**: `@Configuration` 클래스의 `@Bean` 메서드는 Factory Method 패턴의 구현이다. Spring 컨테이너가 빈(Bean) 생성 시점에 이 메서드를 호출하여 객체를 생성하고 싱글톤 레지스트리에 등록한다.

- **📢 섹션 요약 비유**: 부품 공장이 여러 부품(타이어, 엔진, 유리)을 일관되게 공급하는 것처럼, 추상 팩토리는 관련 객체군을 Family 단위로 생성하여 제품의 조합을 보장합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

- **실무 시나리오 1: 플러그인 아키텍처**
    - **문제**: 결제 모듈에 카드, 간편결제, 계좌이체 등 다양한 결제 수단이 지속 추가되어야 함.
    - **의사결정**: PaymentProcessorFactory 인터페이스를 정의하고, 각 결제 수단별 구체 팩토리 구현.
    - **결과**: 새 결제 수단 추가 시 기존 코드 영향 없이 팩토리만 등록하여 확장.

- **실무 시나리오 2: 멀티 테넌트 환경 설정**
    - **문제**: 개발(Dev), 스테이징(Staging), 프로덕션(Prod) 환경별로 다른 DB 연결 필요.
    - **의사결정**: 환경별 DatabaseFactory를 구현하고, 프로파일에 따라 적절한 Factory를 로딩.
    - **결과**: 환경별 코드 분기 제거, 설정 불일치 문제 해결.

- **도입 체크리스트**:
    1. **객체 Family 확인**: 생성되는 객체들이 서로 관련되어 있는가? (예: MySQL + MySQLDriver)
    2. **구체 클래스 의존성**: 클라이언트가 `new ConcreteClass()`를 직접 호출하는가?
    3. **팩토리 클래스 개수**: Family마다 별도의 팩토리가 필요한가? 아니면 범용 팩토리 가능한가?
    4. **리플렉션 활용**: 클래스가 늘어날 때마다 XML/JSON 설정 리플렉션보다 애너테이션(@Configuration)이 관리하기 쉬운가?

- **안티패턴**:
    - **God Factory**: 모든 객체 생성을 담당하는 거대한 팩토리 클래스(SRP 위배).
    - **Factory 순환 의존**: Factory A가 Factory B를 생성하고, Factory B가 Factory A를 생성하는 순환 의존.
    - **간단한 래퍼(Lambda) 남용**: 생성 로직이 단순할 때도 복잡한 Factory를 도입.

- **📢 섹션 요약 비유**: 피자 가게가 너무 많은 메뉴를 단일 메뉴판에 넣으면 혼란스러워지듯, 팩토리도 너무 많은 객체를 하나가 다 만들려고 하면 God Object가 되어 관리가 불가능해집니다. 적절한 분리가 필수적입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

- **정량/정성 기대효과**:

| 구분 | 팩토리 미적용 시 | 팩토리 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | DB 교체 시 50개 파일 수정 | Factory만 교체 | **수정 범위 98% 감소** |
| **정량** | 새 제품군 추가 시 20곳 수정 | Concrete Factory만 추가 | **확장 속도 10배 향상** |
| **정성** | 구체 클래스에 강한 결합 | 추상화에 의존 | **테스트 용이성 개선** |
| **정성** | 생성 로직 중복(DRY 위배) | 중앙화된 생성 | **코드 중복 제거** |

- **미래 전망**:
    1. **Dependency Injection(DI) 컨테이너**: Spring, Guice, Micronaut 등 현대 프레임워크는 팩토리 패턴을 DI 컨테이너로 자동화했다.
    2. **Service Mesh**: Istio, Linkerd는 서비스 디스커버리를 Factory로 추상화하여, 서비스 객체를 런타임에 동적으로 바인딩한다.

- **참고 표준**:
    - **GoF Book**: "Design Patterns" - Factory Method, Abstract Factory 챕터
    - **Effective Java**: Item 1 - "생성자 대신 정적 팩토리 메서드를 고려하라"
    - **Spring Documentation**: @Bean, @Configuration Factory 구현

- **📢 섹션 요약 비유**: 산업혁명이 1차 혁명(수공업)에서 2차 혁명(대량 생산)으로 넘어갈 때 공장(Factory)이 핵심이었듯, 소프트웨어도 반자동화된 팩토리와 DI 컨테이너가 핵심입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[생성 패턴(Creational Patterns)](./564_creational_patterns.md)**: 팩토리 메서드, 추상 팩토리가 속한 상위 카테고리.
- **[DI(Dependency Injection)](./337_dependency_injection.md)**: 팩토리 패턴을 자동화하는 현대적 접근.
- **[빌더 패턴(Builder)](./256_builder.md)**: 복잡한 객체 생성에 특화된 패턴.
- **[OCP(Open-Closed Principle)](./601_solid_principles.md)**: 팩토리 패턴이 준수하는 개방-폐쇄 원칙.
- **[DIP(Dependency Inversion)](./601_solid_principles.md)**: 팩토리가 달성하는 의존성 역전 원칙.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 팩토리 메서드는 **"주문하는 자동"**처럼, 고객이 무엇을 주문할지 말해주면 공장이 알아서 물건을 만들어주는 기계예요.
2. 추상 팩토리는 **"장난감 세트"**처럼, 자동차 장난감이면 바퀴와 바퀴, 핸들과 연결된 세트로 일관되게 만들어주는 거죠.
3. 이렇게 만들어진 장난감은 나중에도 **다른 공장에서도** 그대로 사용할 수 있어서, 아주 편리하고 재사용 가능하답니다!
