+++
title = "디자인 패턴 (Design Pattern)"
date = 2025-03-01

[extra]
categories = "software_engineering-design"
+++

# 디자인 패턴 (Design Pattern)

## 핵심 인사이트 (3줄 요약)
> **소프트웨어 설계에서 반복되는 문제의 해결책**. 생성, 구조, 행위 패턴으로 분류. GoF(Gang of Four)가 정리한 23가지 표준 패턴이 대표적.

## 1. 개념
디자인 패턴은 **소프트웨어 설계에서 자주 발생하는 문제에 대한 재사용 가능한 해결책**으로, 검증된 모범 사례를 정형화한 것이다.

> 비유: "요리 레시피" - 자주 만드는 요리의 표준 조리법

## 2. 디자인 패턴의 역사

```
1994년, GoF (Gang of Four)
- Erich Gamma
- Richard Helm
- Ralph Johnson
- John Vlissides

"Design Patterns: Elements of Reusable Object-Oriented Software"

23가지 패턴을 3가지 카테고리로 분류:
1. 생성 패턴 (Creational) - 5개
2. 구조 패턴 (Structural) - 7개
3. 행위 패턴 (Behavioral) - 11개
```

## 3. 패턴 분류

```
┌─────────────────────────────────────────────────────────┐
│                   디자인 패턴 분류                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  생성 패턴 (Creational)                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 객체 생성 방식을 다루는 패턴                     │   │
│  │ - 싱글톤 (Singleton)                            │   │
│  │ - 팩토리 메서드 (Factory Method)                │   │
│  │ - 추상 팩토리 (Abstract Factory)                │   │
│  │ - 빌더 (Builder)                                │   │
│  │ - 프로토타입 (Prototype)                        │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  구조 패턴 (Structural)                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 클래스/객체 간의 구조적 관계를 다루는 패턴       │   │
│  │ - 어댑터 (Adapter)                              │   │
│  │ - 브리지 (Bridge)                               │   │
│  │ - 컴포지트 (Composite)                          │   │
│  │ - 데코레이터 (Decorator)                        │   │
│  │ - 퍼사드 (Facade)                               │   │
│  │ - 플라이웨이트 (Flyweight)                      │   │
│  │ - 프록시 (Proxy)                                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  행위 패턴 (Behavioral)                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 객체 간의 상호작용과 책임 분배를 다루는 패턴      │   │
│  │ - 옵저버 (Observer)                             │   │
│  │ - 전략 (Strategy)                               │   │
│  │ - 커맨드 (Command)                              │   │
│  │ - 이터레이터 (Iterator)                         │   │
│  │ - 템플릿 메서드 (Template Method)               │   │
│  │ - 상태 (State)                                  │   │
│  │ - 책임 연쇄 (Chain of Responsibility)           │   │
│  │ - 미디에이터 (Mediator)                         │   │
│  │ - 메멘토 (Memento)                              │   │
│  │ - 비지터 (Visitor)                              │   │
│  │ - 인터프리터 (Interpreter)                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 4. 주요 패턴 상세

### 4.1 싱글톤 (Singleton)
```
목적: 인스턴스가 하나만 생성되도록 보장

구조:
┌─────────────────────────────────┐
│          Singleton              │
├─────────────────────────────────┤
│ - instance: Singleton           │
├─────────────────────────────────┤
│ - getInstance(): Singleton      │
│ - Singleton()                   │
└─────────────────────────────────┘

사용 시기:
- 설정 관리자
- 로거
- 데이터베이스 연결 풀
```

### 4.2 팩토리 메서드 (Factory Method)
```
목적: 객체 생성을 서브클래스에 위임

구조:
          ┌──────────┐
          │ Creator  │
          └────┬─────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌──────────┐    ┌──────────┐
│ConCreator│    │ConCreator│
│    A     │    │    B     │
└──────────┘    └──────────┘

사용 시기:
- 어떤 클래스를 생성할지 모를 때
- 확장 가능한 프레임워크
```

### 4.3 어댑터 (Adapter)
```
목적: 호환되지 않는 인터페이스를 연결

구조:
┌────────┐     ┌─────────┐     ┌────────┐
│ Client │────→│ Adapter │────→│ Adaptee│
└────────┘     └─────────┘     └────────┘
               (변환)

비유: 해외 여행 어댑터
```

### 4.4 데코레이터 (Decorator)
```
목적: 객체에 동적으로 기능 추가

구조:
┌────────────────────────────────────┐
│           Component                │
│         (interface)                │
└───────────────┬────────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
┌───────────┐    ┌───────────┐
│Concrete   │    │ Decorator │
│Component  │    └─────┬─────┘
└───────────┘          │
               ┌───────┴───────┐
               ▼               ▼
        ┌───────────┐   ┌───────────┐
        │  ConDec   │   │  ConDec   │
        │    A      │   │    B      │
        └───────────┘   └───────────┘

예: 자바 I/O
new BufferedReader(new FileReader("file.txt"))
```

### 4.5 옵저버 (Observer)
```
목적: 객체 상태 변화를 여러 객체에 알림

구조:
┌──────────────────┐
│    Subject       │
├──────────────────┤
│ - observers      │
│ + attach()       │
│ + detach()       │
│ + notify()       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    Observer      │
├──────────────────┤
│ + update()       │
└──────────────────┘

예:
- 이벤트 리스너
- 뉴스 구독
- 주식 시세
```

### 4.6 전략 (Strategy)
```
목적: 알고리즘을 캡슐화하여 교체 가능하게

구조:
┌──────────────────┐
│    Context       │
├──────────────────┤
│ - strategy       │
│ + execute()      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   <<interface>>  │
│    Strategy      │
├──────────────────┤
│ + algorithm()    │
└────────┬─────────┘
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│StratA │ │StratB │
└───────┘ └───────┘

예:
- 정렬 알고리즘 선택
- 결제 방식 선택
```

## 5. 코드 예시

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

# ===== 싱글톤 패턴 =====
class Singleton:
    """싱글톤 패턴"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = 0
        return cls._instance

# ===== 팩토리 메서드 패턴 =====
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "멍멍!"

class Cat(Animal):
    def speak(self) -> str:
        return "야옹!"

class AnimalFactory:
    """팩토리 메서드 패턴"""
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError(f"Unknown animal: {animal_type}")

# ===== 어댑터 패턴 =====
class EuropeanSocket:
    """유럽 소켓"""
    def voltage(self) -> int:
        return 230

class KoreanSocket:
    """한국 소켓"""
    def voltage(self) -> int:
        return 220

class SocketAdapter:
    """어댑터 패턴"""
    def __init__(self, socket):
        self.socket = socket

    def get_voltage(self) -> int:
        v = self.socket.voltage()
        return self._convert(v)

    def _convert(self, voltage: int) -> int:
        # 220V로 변환
        return 220

# ===== 데코레이터 패턴 =====
class Coffee:
    """기본 커피"""
    def cost(self) -> int:
        return 3000

    def description(self) -> str:
        return "커피"

class CoffeeDecorator(Coffee):
    """데코레이터 기본 클래스"""
    def __init__(self, coffee: Coffee):
        self.coffee = coffee

class MilkDecorator(CoffeeDecorator):
    """우유 추가"""
    def cost(self) -> int:
        return self.coffee.cost() + 500

    def description(self) -> str:
        return self.coffee.description() + " + 우유"

class WhipDecorator(CoffeeDecorator):
    """휘핑 추가"""
    def cost(self) -> int:
        return self.coffee.cost() + 700

    def description(self) -> str:
        return self.coffee.description() + " + 휘핑"

# ===== 옵저버 패턴 =====
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject:
    """옵저버 패턴 - Subject"""
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class NewsAgency(Subject):
    """뉴스 통신사"""
    def __init__(self):
        super().__init__()
        self._news = ""

    @property
    def news(self) -> str:
        return self._news

    @news.setter
    def news(self, value: str):
        self._news = value
        self.notify(value)

class NewsSubscriber(Observer):
    """뉴스 구독자"""
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str):
        print(f"[{self.name}] 뉴스 수신: {message}")

# ===== 전략 패턴 =====
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

class BubbleSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class QuickSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class Sorter:
    """전략 패턴 - Context"""
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self.strategy.sort(data)


# ===== 사용 예시 =====
print("=== 디자인 패턴 예시 ===\n")

# 싱글톤
print("--- 싱글톤 패턴 ---")
s1 = Singleton()
s2 = Singleton()
print(f"같은 인스턴스?: {s1 is s2}")

# 팩토리 메서드
print("\n--- 팩토리 메서드 패턴 ---")
dog = AnimalFactory.create_animal("dog")
cat = AnimalFactory.create_animal("cat")
print(f"강아지: {dog.speak()}")
print(f"고양이: {cat.speak()}")

# 데코레이터
print("\n--- 데코레이터 패턴 ---")
coffee = Coffee()
print(f"{coffee.description()}: {coffee.cost()}원")

milk_coffee = MilkDecorator(coffee)
print(f"{milk_coffee.description()}: {milk_coffee.cost()}원")

whip_milk_coffee = WhipDecorator(milk_coffee)
print(f"{whip_milk_coffee.description()}: {whip_milk_coffee.cost()}원")

# 옵저버
print("\n--- 옵저버 패턴 ---")
agency = NewsAgency()
subscriber1 = NewsSubscriber("구독자1")
subscriber2 = NewsSubscriber("구독자2")

agency.attach(subscriber1)
agency.attach(subscriber2)
agency.news = "속보: 새로운 디자인 패턴 발견!"

# 전략
print("\n--- 전략 패턴 ---")
data = [64, 34, 25, 12, 22, 11, 90]

sorter = Sorter(BubbleSort())
print(f"버블 정렬: {sorter.sort(data)}")

sorter.set_strategy(QuickSort())
print(f"퀵 정렬: {sorter.sort(data)}")
```

## 6. 패턴 선택 가이드

```
생성이 복잡할 때:
- 싱글톤: 하나만 필요할 때
- 팩토리: 어떤 클래스인지 모를 때
- 빌더: 복잡한 객체 생성

구조적 문제:
- 어댑터: 인터페이스 불일치
- 데코레이터: 기능 동적 추가
- 컴포지트: 트리 구조

행위 문제:
- 옵저버: 상태 변화 알림
- 전략: 알고리즘 교체
- 이터레이터: 순차 접근
```

## 7. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 재사용성 | 검증된 해결책 |
| 의사소통 | 공통 용어 |
| 유지보수 | 구조적 설계 |
| 확장성 | 유연한 구조 |

### 단점
| 단점 | 설명 |
|-----|------|
| 복잡성 | 과도한 추상화 |
| 학습 비용 | 패턴 이해 필요 |
| 남용 | 무조건 적용 |

## 8. 실무에선? (기술사적 판단)
- **프레임워크**: Spring, Django 등 이미 패턴 적용
- **적절한 사용**: 문제에 맞는 패턴 선택
- **안티패턴 주의**: 과도한 싱글톤, 깊은 상속
- **조합**: 여러 패턴 조합 사용
- **리팩토링**: 기존 코드에 패턴 적용

## 9. 관련 개념
- SOLID 원칙
- 아키텍처 패턴
- 리팩토링
- 안티패턴

---

## 어린이를 위한 종합 설명

**디자인 패턴은 "요리 레시피" 같아요!**

### 왜 필요할까요? 🍳
```
매번 새로 만들면:
- 시간이 많이 걸려요 ⏰
- 실수할 수 있어요 ❌

레시피를 쓰면:
- 빠르고 쉬워요 ✨
- 맛이 보장돼요 ✓
```

### 3가지 종류 📚
```
만들기 패턴 (생성):
- 어떻게 만들까요?

모양 패턴 (구조):
- 어떻게 연결할까요?

행동 패턴 (행위):
- 어떻게 작동할까요?
```

### 인기 패턴 🌟
```
싱글톤: 하나만 만들어요
  "학교 교장 선생님은 한 명!"

팩토리: 공장에서 만들어요
  "어떤 동물인지 말하면 만들어줘요"

옵저버: 소식을 전해줘요
  "유튜브 구독하면 새 영상 알림!"

전략: 방법을 바꿔요
  "정렬 방법을 골라요"
```

**비밀**: 개발자들도 레시피를 써요! 📖✨
