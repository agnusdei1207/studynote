+++
title = "266-276. GoF 디자인 패턴: 행위 패턴"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 266
+++

# 266-276. GoF 디자인 패턴: 행위 패턴

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 객체의 책임 분산과 상호작용의 효율성을 극대화하기 위해 알고리즘과 객체 간 통신 메커니즘을 캡슐화하는 소프트웨어 아키텍처 설계 철학.
> 2. **가치**: 런타임에 알고리즘을 교체(Strategy)하거나 복잡한 의존성을 decoupling(Observer, Mediator)하여 유지보수성(Maintainability)을 40% 이상 향상시키고 시스템 확장성을 확보함.
> 3. **융합**: 분산 처리(Microservices의 Event-Driven Architecture), UI 프레임워크(MVC/Publisher-Subscriber), 상태 머신(State Machine) 구현의 핵심 기반이 됨.

---

### Ⅰ. 개요 (Context & Background)

**디자인 패턴(Design Pattern)** 중 **행위 패턴(Behavioral Pattern)**은 객체 간의 책임을 분담하고, 객체들이 어떻게 소통하며 협력하는지에 초점을 맞춘다. 생성 패턴(Creational)이 객체의 생성 시점을, 구조 패턴(Structural)이 클래스의 구성을 다룬다면, 행위 패턴은 **실행 흐름(Run-time Flow Control)**과 **알고리즘의 교체**를 다룬다.

전통적인 절차적 프로그래밍(Procedural Programming)에서는 거대한 `if-else`나 `switch` 문으로 행동을 제어하여, 새로운 요구사항이 발생할 때마다 기존 코드를 수정해야 하는 위험이 있다. 행위 패턴은 이러한 **하드코딩된 제어 흐름을 객체 간의 통신 패턴**으로 전환하여, OOP(객체 지향 프로그래밍)의 다형성(Polymorphism)을 극대화한다.

예를 들어, **옵저버(Observer)** 패턴은 데이터 소스와 UI의 강한 결합을 제거하여, 데이터 변경 시 UI를 자동으로 갱신하는 메커니즘을 제공한다. 이는 단순히 코드를 줄이는 것이 아니라, 시스템의 반응성(Responsiveness)과 모듈화(Modularity)를 달성하는 핵심 전략이다.

#### ASCII: 행위 패턴의 분류 및 목적

```ascii
[ 행위 패턴 (Behavioral Patterns) 의 세계 ]

┌─────────────────────────────────────────────────────────────────────┐
│  목표: 캡슐화를 통해 알고리즘의 변화에 대응하고 복잡한 상호작용 단순화  │
└─────────────────────────────────────────────────────────────────────┘
         │
         ├─── [ 1. 변화의 캡슐화 (Encapsulation of Variation) ]
         │    . 알고리즘의 교체 가능성                -> Strategy (전략)
         │    . 실행 단계의 정의와 구현 분리          -> Template Method (템플릿 메서드)
         │    . 상태에 따른 행동 변경                 -> State (상태)
         │
         ├─── [ 2. 통신과 분산 (Communication & Decoupling) ]
         │    . 일 대 다 알림                        -> Observer (옵저버)
         │    . 다 대 다 복잡성 단순화                -> Mediator (중재자)
         │    . 요청 처리자 순회                     -> Chain of Responsibility (책임 연쇄)
         │    . 데이터 구조와 연산 분리               -> Visitor (방문자)
         │
         └─── [ 3. 실행 기록 및 제어 (Execution Control) ]
              . 요청의 객체화 및 큐잉                 -> Command (커맨드)
              . 내부 상태의 스냅샷 및 복구             -> Memento (메멘토)
              . 컬렉션의 순회 로직 캡슐화              -> Iterator (이터레이터)
              . NULL 객체 처리                        -> Null Object (널 객체)
```

**해설**:
위 도표는 행위 패턴이 해결하고자 하는 문제의 성격을 세 가지 축으로 분류한 것이다.
1. **변화의 캡슐화**: 비즈니스 로직(알고리즘)이 자주 바뀔 수 있는 환경에서, 코드 수정 없이 전략을 바꾸는 패턴들이다.
2. **통신과 분산**: MSA(Microservices Architecture)나 이벤트 드리븐 아키텍처(EDA)의 근간이 되며, 객체 간 결합도를 낮추는 데 필수적이다.
3. **실행 제어**: 트랜잭션 관리, 실행 취소(Undo), 시스템 복구 등 고도화된 제어 로직을 지원한다.

> **💡 비유**: 도시 교통 체계에 비유할 수 있습니다. 전략 패턴은 차량이 `고속도로`와 `일반 도로`를 상황에 따라 선택하는 것이고, 옵저버 패턴은 교통 상황정보(CCTV)가 변할 때 네비게이션 앱들로 자동 신호를 보내는 것입니다. 중재자 패턴은 교차로의 신호등이 모든 차량의 흐름을 통제하는 것과 같습니다.
> **📢 섹션 요약 비유**: 행위 패턴은 **교통 정리 및 운전 전략**과 같습니다. 차량(객체)이 서로 충돌하지 않고 효율적으로 목적지로 이동하도록 신호등(중재자), 내비게이션 경로(전략), 교통 소식(옵저버)을 체계화하는 규칙입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

행위 패턴의 핵심은 **'무엇(What)'을 수행할지와 '어떻게(How)'를 수행할지의 분리**에 있다. 여기서는 3가지 대표적인 패턴(Strategy, Observer, Command)의 구조를 깊이 있게 분석한다.

#### 1. 구성 요소 상세 분석 (Component Analysis)

| Pattern | Component (구성 요소) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/특징 |
|:---:|:---|:---|:---|:---|
| **Strategy** | **Context** | 전략을 사용하는 클라이언트 | `Strategy` 인터페이스를 통해 요청을 위임 | 상태를 가질 수 있음 |
| | **Strategy (I/F)** | 알고리즘의 공통 인터페이스 | `algorithmInterface()` 선언 | 인터페이스나 추상 클래스 |
| | **ConcreteStrategy** | 구체적인 알고리즘 구현 | `execute()` 메서드 내 실제 로직 수행 | 교체 가능한 모듈 |
| **Observer** | **Subject** | 관찰 대상 (발행자) | 상태 변경 시 `notifyObservers()` 호출 | List<Observer> 유지 |
| | **Observer** | 관찰자 (구독자) | `update()` 인터페이스 구현 | 데이터 수신 및 처리 |
| **Command** | **Invoker** | 요청자 (호출자) | `Command` 객체의 `execute()` 호출 | GUI 버튼, 스케줄러 |
| | **Receiver** | 수신자 (실제 행위자) | 비즈니스 로직을 실제로 수행 | 비즈니스 로직 핵심 |
| | **Command** | 명령 객체 | Receiver와 Action을 캡슐화 | `execute()`, `undo()` |

#### 2. 전략 패턴 (Strategy Pattern) 다이어그램 및 심층 분석

전략 패턴은 **알고리즘군(Algorithm Families)**을 정의하고, 각각을 캡슐화하여 교체해서 사용할 수 있게 만든다. 클라이언트와 알고리즘 간의 강한 결합을 제거한다.

```ascii
[ 전략 패턴 (Strategy Pattern) 구조 ]

      Client (User)
         │
         │ uses
         ▼
┌─────────────────┐         ┌────────────────────────────────┐
│     Context     │────────>│   <<interface>> Strategy       │
├─────────────────┤         ├────────────────────────────────┤
│ - strategy: I/F │         │ + algorithmInterface(): void   │
├─────────────────┤         └────────────────────────────────┘
│ + contextInterface()│                   ▲
└─────────────────┘         ┌─────────────┴─────────────┐
                            │                           │
            ┌───────────────┴───────┐    ┌──────────────┴───────────┐
            │ ConcreteStrategyA     │    │ ConcreteStrategyB         │
            ├───────────────────────┤    ├───────────────────────────┤
            │ + algorithmInterface()│    │ + algorithmInterface()    │
            │ { Quick Sort Logic }  │    │ { Merge Sort Logic }      │
            └───────────────────────┘    └───────────────────────────┘
```

**해설**:
1. **Context**는 `ConcreteStrategy`를 구체적으로 알지 못한다. 오직 `Strategy` 인터페이스만 알고 있으므로, **런타임(Runtime)**에 `setStrategy(new StrategyB())`와 같이 전략을 변경할 수 있다.
2. 이는 **OCP (Open/Closed Principle)**를 만족한다. 기능 확장(새로운 전략 추가)에는 열려 있고, 코드 수정(Context 변경)에는 닫혀 있다.
3. 코드 예시 (Java Style):
```java
// 전략 인터페이스
public interface PaymentStrategy {
    void pay(int amount);
}

// 구체적 전략: 카카오페이
public class KakaoPayStrategy implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("KakaoPay로 " + amount + "원 결제.");
    }
}

// 문맥: 쇼핑카트
public class ShoppingCart {
    private PaymentStrategy strategy; // 약한 결합
    
    public void setStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void checkout(int amount) {
        strategy.pay(amount); // 위임 (Delegation)
    }
}
```

#### 3. 옵저버 패턴 (Observer Pattern) 다이어그램

옵저버 패턴은 일대다(1:N) 의존성을 정의하여, 한 객체의 상태가 변하면 의존적인 모든 객체에 자동으로 알림을 보내고 내용을 갱신하는 패턴이다. **Pub-Sub(Publisher-Subscriber)** 모델의 기초다.

```ascii
[ 옵저버 패턴 (Observer Pattern) 흐름 ]

   Subject (Publisher)                    Observer (Subscribers)
┌─────────────────────┐
│   Change State()    │───────┐
└─────────────────────┘       │
                              │
       [State Changes]        │   1. Notify( )
                              │      │
                              ▼      ▼
┌──────────────────────┐   ┌───────────────────────────────────────┐
│ Subject              │   │  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│ - state              │   │  │ ObserverA│  │ ObserverB│  │ ...  │ │
│ - observers: List<>  │   │  │ update() │  │ update() │  │ ...  │ │
├──────────────────────┤   │  └──────────┘  └──────────┘  └──────┘ │
│ + attach(Observer)   │───┴───────────────────────────────────────│
│ + detach(Observer)   │         Pull (Get Data) or Push (Send Data)│
│ + notify()           │───┐   ──────────────────────────────────────┤
└──────────────────────┘   │                                       │
                           ▼                                       │
                    ┌──────────────────────────────────────────────┤
                    │ observers.forEach(o -> o.update(this))      │
                    └──────────────────────────────────────────────┘
```

**해설**:
- **Decoupling (결합도 제거)**: Subject는 Observer가 누구인지(구체적인 클래스) 몰라도 된다. 단지 `Observer` 인터페이스를 구현했다는 사실만 안다.
- **Update Trigger**: Subject의 상태가 변경되면 `notify()` 메서드가 호출되고, 이는 등록된 모든 Observer들의 `update()` 메서드를 트리거한다.
- **Push vs Pull**: 데이터를 보낼 때 매개변수로 보내느냐(Push), Observer가 Getter를 호출해가느냐(Pull)에 따라 구현이 나뉜다.

#### 4. 핵심 알고리즘 및 메커니즘

행위 패턴은 흐름 제어(Flow Control)를 위임(Delegation)한다는 점에서 유사하다.
- **Strategy**: 알고리즘 수행 자체를 위임.
- **Template Method**: 알고리즘의 단계(Structure)는 고정하고, 세부 단계(Step)의 구현을 하위 클래스로 위임. (`final method`로 골격 정의, `abstract method`로 확장 포인트 제공)
- **Chain of Responsibility**: 요청을 처리할 수 있는 수신자(Handler)를 체인(Linked List)으로 연결하여, 누가 처리할지 모르는 상태에서 요청을 전달. 필터링 로직에 적합.

```java
// 책임 연쇄 예시
public abstract class Handler {
    protected Handler next; // 다음 처리자
    
    public void setNext(Handler next) { this.next = next; }
    
    public void handle(Request req) {
        if (canHandle(req)) { // 내가 처리할 수 있는가?
            process(req);
        } else if (next != null) {
            next.handle(req); // 못하면 다음에게 넘김
        }
    }
    
    protected abstract boolean canHandle(Request req);
    protected abstract void process(Request req);
}
```

> **📢 섹션 요약 비유**: **전략 패턴**은 GPS 네비게이션에서 '최단 거리'와 '무료 도로' 옵션을 실시간으로 토글하는 것이고, **옵저버 패턴**은 유튜브의 '알림 구독' 설정입니다. **커맨드 패턴**은 복잡한 전자기기 리모컨에 '시청 목록(녹화)' 버튼을 하나 추가하여, 나중에 그 명령을 다시 실행(Undo/Redo)할 수 있게 만드는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

행위 패턴은 단독으로 쓰이기보다 다른 패턴이나 아키텍처 스타일과 결합하여 시너지를 낸다. 특히 분산 시스템(Distributed Systems)과 UI 설계에서 필수적이다.

#### 1. 심층 기술 비교 (Behavioral Patterns Matrix)

| 구분 | Strategy Pattern | State Pattern | Template Method Pattern |
|:---|:---|:---|:---|
| **의도 (Intent)** | **알고리즘의 교체** | **상태에 따른 행동 변화** | **알고리즘 구조의 재사용** |
| **결합도 (Coupling)** | Context와 Algorithm 낮음 | Context와 State 높음 (밀접) | Super/Sub Class 간 결합 높음 |
| **런타임 교체** | **가능 (Instance 교체)** | **가능 (State 객체 교체)** | **불