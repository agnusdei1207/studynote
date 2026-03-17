+++
title = "40. 디자인 패턴 (Design Patterns)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Design-Patterns", "GoF", "SOLID", "Refactoring", "Clean-Code"]
draft = false
+++

# 디자인 패턴 (Design Patterns)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디자인 패턴은 **"반복 **되는 **소프트웨어 **문제**에 **대한 **재사용 **가능**한 **해결 **책\"**으로, **GoF**(Gang of Four)**가 **23개 **패턴**을 **정의**하고 **SOLID**, **DRY**(Don't Repeat Yourself)**가 **기본 **원칙**이다.
> 2. **유형**: **Creational**(객체 **생성: **Singleton**, **Factory**, **Builder)**, **Structural**(구조 **구성: **Adapter**, **Decorator**, **Facade)**, **Behavioral**(객체 **상호작용: **Observer**, **Strategy**, **Command)**으로 **분류**된다.
> 3. **적용**: **중간 **규모 **프로젝트**에서 **가장 **유용**하며 **Over-engineering**을 **방지**하기 **위해 **YAGNI**(You Aren't Gonna Need It)**를 **준수**하고 **리팩토링**으로 **점진적 **도입**이 **권장**된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
디자인 패턴은 **"베스트 프랙티스 템플릿"**이다.

**GoF 23패턴**:
| 유형 | 패턴 수 | 대표 패턴 |
|------|---------|----------|
| **Creational** | 5 | Singleton, Factory, Builder |
| **Structural** | 7 | Adapter, Decorator, Proxy |
| **Behavioral** | 11 | Observer, Strategy, Command |

### 💡 비유
디자인 패턴은 ****건축 **도면 ****과 같다.
- **문제**: 기능 요구
- **패턴**: 설계 솔루션
- **구현**: 실제 코드

---

## Ⅱ. 아키텍처 및 핵심 원리

### SOLID 원칙

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         SOLID Principles                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    S - Single Responsibility Principle (SRP):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Bad: User class handles data, validation, persistence, notification                 │  │
    │  │  Good: Separate User, UserValidator, UserRepository, EmailService                     │  │
    │  │                                                                                       │  │
    │  │  class User:                                                                          │  │
    │  │      def __init__(self, name, email):                                                │  │
    │  │          self.name = name                                                            │  │
    │  │          self.email = email                                                          │  │
    │  │                                                                                       │  │
    │  │  class UserValidator:                                                                 │  │
    │  │      def validate(self, user): return user.email.contains('@')                        │  │
    │  │                                                                                       │  │
    │  │  class UserRepository:                                                                │  │
    │  │      def save(self, user): pass  # DB save                                           │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘  │

    O - Open/Closed Principle (OCP):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Open for extension, closed for modification                                         │  │
    │  │                                                                                       │  │
    │  │  # Bad: Modify class for new shape                                                   │  │
    │  │  def calculate_area(shape):                                                           │  │
    │  │      if shape.type == "circle": return 3.14 * shape.r ** 2                            │  │
    │  │      elif shape.type == "rectangle": return shape.w * shape.h                          │  │
    │  │                                                                                       │  │
    │  │  # Good: Each shape implements area()                                                 │  │
    │  │  class Shape:                                                                          │  │
    │  │      def area(self): raise NotImplementedError                                         │  │
    │  │  class Circle(Shape):                                                                 │  │
    │  │      def __init__(self, r): self.r = r                                                │  │
    │  │      def area(self): return 3.14 * self.r ** 2                                        │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    L - Liskov Substitution Principle (LSP):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Subtypes must be substitutable for base types                                       │  │
    │  │                                                                                       │  │
    │  │  # Bad: Square breaks Rectangle behavior                                              │  │
    │  │  class Square(Rectangle):                                                             │  │
    │  │      def __init__(self, s):                                                           │  │
    │  │          super().__init__(s, s)  # But set_width() doesn't work as expected            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    I - Interface Segregation Principle (ISP):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Clients shouldn't depend on interfaces they don't use                               │  │
    │  │                                                                                       │  │
    │  │  # Bad: Fat interface                                                                 │  │
    │  │  class Worker(ABC):                                                                   │  │
    │  │      @abstractmethod                                                                  │  │
    │  │      def work(self): pass                                                             │  │
    │  │      @abstractmethod                                                                  │  │
    │  │      def eat(self): pass    # Not all workers need eat()                              │  │
    │  │                                                                                       │  │
    │  │  # Good: Separate interfaces                                                          │  │
    │  │  class Workable(ABC):                                                                 │  │
    │  │      @abstractmethod                                                                  │  │
    │  │      def work(self): pass                                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    D - Dependency Inversion Principle (DIP):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Depend on abstractions, not concretions                                              │  │
    │  │                                                                                       │  │
    │  │  # Bad: Direct dependency on implementation                                           │  │
    │  │  class LightSwitch:                                                                   │  │
    │  │      def __init__(self):                                                              │  │
    │  │          self.bulb = IncandescentBulb()    # Hard-coded                               │  │
    │  │                                                                                       │  │
    │  │  # Good: Depend on abstraction                                                        │  │
    │  │  class Switch:                                                                         │  │
    │  │      def __init__(self, device): self.device = device                                 │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘  │
```

### Creational Patterns

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Singleton Pattern                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Ensure only one instance exists
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  class Database:                                                                        │  │
    │      _instance = None                                                                    │  │
    │                                                                                         │  │
    │      def __new__(cls):                                                                  │  │
    │          if cls._instance is None:                                                       │  │
    │              cls._instance = super().__new__(cls)                                        │  │
    │          return cls._instance                                                            │  │
    │                                                                                         │  │
    │  # Usage                                                                                │  │
    │  db1 = Database()  # Same instance                                                      │  │
    │  db2 = Database()  # Same instance                                                      │  │
    │  assert db1 is db2                                                                       │  │
    │                                                                                         │  │
    │  → Use for: DB connection, Logger, Configuration                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Builder Pattern:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  class SQLQueryBuilder:                                                                  │  │
    │      def __init__(self):                                                                 │  │
    │          self.query = ""                                                                 │  │
    │                                                                                         │  │
    │      def select(self, columns):                                                          │  │
    │          self.query += f"SELECT {', '.join(columns)} "                                   │  │
    │          return self  # Fluent interface                                                 │  │
    │                                                                                         │  │
    │      def from_table(self, table):                                                        │  │
    │          self.query += f"FROM {table} "                                                  │  │
    │          return self                                                                     │  │
    │                                                                                         │  │
    │      def where(self, condition):                                                         │  │
    │          self.query += f"WHERE {condition} "                                             │  │
    │          return self                                                                     │  │
    │                                                                                         │  │
    │  # Usage: Fluent chaining                                                                │  │
    │  query = (SQLQueryBuilder()                                                              │  │
    │      .select(["name", "email"])                                                          │  │
    │      .from_table("users")                                                                │  │
    │      .where("age > 18")                                                                 │  │
    │      .build())                                                                           │  │
    │  # Result: "SELECT name, email FROM users WHERE age > 18"                                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Structural Patterns

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Adapter Pattern                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Incompatible interfaces
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Existing interface                                                                   │  │
    │  class EuropeanSocket:                                                                 │  │
    │      def voltage(self): return 230                                                      │  │
    │                                                                                         │  │
    │  # Target interface                                                                    │  │
    │  class USDevice:                                                                        │  │
    │      def plug_in(self, voltage):                                                        │  │
    │          if voltage != 110: raise Exception("Wrong voltage")                             │  │
    │                                                                                         │  │
    │  # Adapter                                                                              │  │
    │  class TravelAdapter:                                                                   │  │
    │      def __init__(self, socket):                                                        │  │
    │          self.socket = socket                                                            │  │
    │                                                                                         │  │
    │      def voltage(self):                                                                 │  │
    │          return 110  # Converts 230V to 110V                                            │  │
    │                                                                                         │  │
    │  # Usage                                                                                │  │
    │  eu_socket = EuropeanSocket()                                                           │  │
    │  adapter = TravelAdapter(eu_socket)                                                     │  │
    │  us_device = USDevice()                                                                 │  │
    │  us_device.plug_in(adapter.voltage())  # Works!                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Decorator Pattern:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Base component                                                                       │  │
    │  class Coffee:                                                                           │  │
    │      def cost(self): return 2.0                                                         │  │
    │      def description(self): return "Coffee"                                              │  │
    │                                                                                         │  │
    │  # Decorator                                                                             │  │
    │  class CoffeeDecorator:                                                                  │  │
    │      def __init__(self, coffee):                                                         │  │
    │          self._coffee = coffee                                                           │  │
    │                                                                                         │  │
    │  # Concrete decorators                                                                   │  │
    │  class Milk(CoffeeDecorator):                                                            │  │
    │      def cost(self): return self._coffee.cost() + 0.5                                    │  │
    │      def description(self): return self._coffee.description() + ", Milk"                 │  │
    │                                                                                         │  │
    │  class Mocha(CoffeeDecorator):                                                            │  │
    │      def cost(self): return self._coffee.cost() + 1.0                                    │  │
    │      def description(self): return self._coffee.description() + ", Mocha"                │  │
    │                                                                                         │  │
    │  # Usage: Layered decorators                                                             │  │
    │  coffee = Coffee()                                                                       │  │
    │  coffee = Milk(coffee)     # Coffee + Milk                                              │  │
    │  coffee = Mocha(coffee)    # Coffee + Milk + Mocha                                      │  │
    │  print(coffee.cost())       # 3.5                                                        │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Behavioral Patterns

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Observer Pattern                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Notify multiple objects of state changes
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Subject (Observable)                                                                 │  │
    │  class YouTubeChannel:                                                                  │  │
    │      def __init__(self):                                                                 │  │
    │          self._subscribers = []                                                          │  │
    │                                                                                         │  │
    │      def subscribe(self, observer):                                                      │  │
    │          self._subscribers.append(observer)                                              │  │
    │                                                                                         │  │
    │      def unsubscribe(self, observer):                                                   │  │
    │          self._subscribers.remove(observer)                                              │  │
    │                                                                                         │  │
    │      def notify(self, video):                                                            │  │
    │          for subscriber in self._subscribers:                                            │  │
    │              subscriber.update(video)                                                     │  │
    │                                                                                         │  │
    │  # Observer (Subscriber)                                                                │  │
    │  class Subscriber:                                                                       │  │
    │      def update(self, video):                                                            │  │
    │          print(f"New video: {video}")                                                     │  │
    │                                                                                         │  │
    │  # Usage                                                                                │  │
    │  channel = YouTubeChannel()                                                              │  │
    │  alice = Subscriber()                                                                    │  │
    │  bob = Subscriber()                                                                      │  │
    │  channel.subscribe(alice)                                                                │  │
    │  channel.subscribe(bob)                                                                  │  │
    │  channel.notify("Design Patterns Tutorial")  # Both notified                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Strategy Pattern:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Strategy interface                                                                    │  │
    │  class PaymentStrategy(ABC):                                                             │  │
    │      @abstractmethod                                                                     │  │
    │      def pay(self, amount): pass                                                         │  │
    │                                                                                         │  │
    │  # Concrete strategies                                                                   │  │
    │  class CreditCard(PaymentStrategy):                                                      │  │
    │      def pay(self, amount): print(f"Paid ${amount} with Credit Card")                     │  │
    │                                                                                         │  │
    │  class PayPal(PaymentStrategy):                                                          │  │
    │      def pay(self, amount): print(f"Paid ${amount} with PayPal")                          │  │
    │                                                                                         │  │
    │  # Context                                                                              │  │
    │  class ShoppingCart:                                                                     │  │
    │      def __init__(self, strategy):                                                        │  │
    │          self.strategy = strategy                                                        │  │
    │                                                                                         │  │
    │      def checkout(self, amount):                                                         │  │
    │          self.strategy.pay(amount)                                                        │  │
    │                                                                                         │  │
    │  # Usage: Runtime strategy selection                                                     │  │
    │  cart = ShoppingCart(CreditCard())                                                       │  │
    │  cart.checkout(100)  # Paid $100 with Credit Card                                        │  │
    │  cart.strategy = PayPal()                                                                │  │
    │  cart.checkout(50)   # Paid $50 with PayPal                                              │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 패턴 비교

| 패턴 | 문제 | 해결 | 예시 |
|------|------|------|------|
| **Singleton** | 다중 인스턴스 | 단일 인스턴스 | DB 커넥션 |
| **Factory** | 객체 생성 복잡 | 생성 위임 | UI 컴포넌트 |
| **Observer** | 상태 변경 알림 | 구독-발행 | 이벤트 |
| **Strategy** | 알고리즘 선택 | 인터페이스 | 정렬, 결제 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 로깅 시스템 설계
**상황**: 다양한 로그 출력 대상
**판단**: Strategy + Observer

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Logging System Design                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Multiple outputs: Console, File, Remote server                                      │  │
    │  • Different formats: JSON, Plain text                                                 │  │
    │  • Log levels: DEBUG, INFO, WARNING, ERROR                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution: Strategy + Observer
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Strategy: Log formatter                                                              │  │
    │  class LogFormatter(ABC):                                                               │  │
    │      @abstractmethod                                                                     │  │
    │      def format(self, level, message): pass                                             │  │
    │                                                                                         │  │
    │  class JSONFormatter(LogFormatter):                                                     │  │
    │      def format(self, level, message):                                                  │  │
    │          return json.dumps({"level": level, "message": message, "timestamp": time.time()})│  │
    │                                                                                         │  │
    │  # Observer: Log appender                                                               │  │
    │  class LogAppender(ABC):                                                                │  │
    │      @abstractmethod                                                                     │  │
    │      def write(self, formatted_message): pass                                           │  │
    │                                                                                         │  │
    │  class ConsoleAppender(LogAppender):                                                     │  │
    │      def write(self, formatted_message): print(formatted_message)                        │  │
    │                                                                                         │  │
    │  class FileAppender(LogAppender):                                                        │  │
    │      def __init__(self, filename):                                                       │  │
    │          self.file = open(filename, 'a')                                                 │  │
    │      def write(self, formatted_message):                                                 │  │
    │          self.file.write(formatted_message + '\n')                                       │  │
    │                                                                                         │  │
    │  # Context (Subject)                                                                     │  │
    │  class Logger:                                                                           │  │
    │      def __init__(self, formatter):                                                      │  │
    │          self.formatter = formatter                                                      │  │
    │          self.appenders = []                                                             │  │
    │                                                                                         │  │
    │      def add_appender(self, appender):                                                   │  │
    │          self.appenders.append(appender)                                                 │  │
    │                                                                                         │  │
    │      def log(self, level, message):                                                      │  │
    │          formatted = self.formatter.format(level, message)                                │  │
    │          for appender in self.appenders:                                                  │  │
    │              appender.write(formatted)                                                    │  │
    │                                                                                         │  │
    │  # Usage                                                                                │  │
    │  logger = Logger(JSONFormatter())                                                        │  │
    │  logger.add_appender(ConsoleAppender())                                                  │  │
    │  logger.add_appender(FileAppender("app.log"))                                            │  │
    │  logger.log("INFO", "Application started")                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 디자인 패턴 기대 효과

| 효과 | 패턴 없음 | 패턴 사용 |
|------|----------|----------|
| **유지보수** | 어려움 | 쉬움 |
| **재사용** | 낮음 | 높음 |
| **커뮤니케이션** | 모호함 | 명확함 |
| **복잡도** | 낮음 | 높음 |

### 모범 사례

1. **필요시**: 실제 문제에
2. **단순**: 간단하게
3. **리팩토링**: 점진적 도입
4. **문서화**: 왜 사용?

### 미래 전망

1. **함수형**: Functional patterns
2. **비동기**: Async/Await patterns
3. **리액티브**: Rx patterns
4. **클라우드**: Cloud-native patterns

### ※ 참고 표준/가이드
- **GoF**: Design Patterns (1994)
- **Refactoring**: Martin Fowler
- **Clean Code**: Robert C. Martin

---

## 📌 관련 개념 맵

- [아키텍처 패턴](./13_architecture/39_microservices.md) - 시스템 수준
- [리팩토링](./8_refactoring/33_refactoring.md) - 코드 개선
- [SOLID](./7_object_design/32_solid.md) - 설계 원칙

