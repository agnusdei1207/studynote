+++
title = "디자인 패턴 (Design Pattern)"
date = 2025-03-01

[extra]
categories = "pe_exam-software_engineering-design"
+++

# 디자인 패턴 (Design Pattern)

## 핵심 인사이트 (3줄 요약)
> **소프트웨어 설계에서 반복되는 문제의 검증된 해결책 템플릿**으로, GoF 23종 패턴이 생성·구조·행위로 분류된다. 재사용성, 확장성, 유지보수성을 동시에 확보한다. 기술사 시험에서는 각 패턴의 구조, 적용 시나리오, SOLID 원칙과의 연관성을 묻는다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 디자인 패턴(Design Pattern)은 **소프트웨어 설계에서 자주 발생하는 문제에 대한 재사용 가능한 해결책**으로, 검증된 모범 사례를 정형화한 설계 템플릿이다. 1994년 GoF(Gang of Four)가 체계화했다.

> 💡 **비유**: 디자인 패턴은 **"요리 레시피의 정석"** 같아요. 수많은 요리사가 실험 끝에 찾아낸 최적의 조리법을 정리해둔 것이죠. "파스타 만들기"를 처음 해도 레시피대로 하면 실패 확률이 줄어들어요!

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점 - 반복되는 설계 오류**: 개발자들이 같은 문제에 대해 저마다 다른(그리고 종종 잘못된) 해결책을 만듦. 설계 지식의 파편화

2. **기술적 필요성 - 지식 공유**: 1994년 GoF(Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides)가 23가지 패턴을 체계화하여 설계 지식의 재사용성 확보. 공통 어휘 확립

3. **시장/산업 요구 - 유지보수 비용**: 소프트웨어 수명 주기 중 유지보수 비용이 60~80% 차지. 확장 가능한 설계 필수. 기술 부채 최소화

**핵심 목적**: **검증된 설계 솔루션의 재사용으로 품질·생산성·의사소통 효율화**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**GoF 패턴 분류 체계** (필수: 23종 전체):

| 구성 요소 | 카테고리 | 역할/기능 | 특징 | 비유 |
|----------|---------|----------|------|------|
| **싱글톤 (Singleton)** | 생성 | 인스턴스 유일성 보장 | 전역 접근점 | 대통령 |
| **팩토리 메서드 (Factory)** | 생성 | 서브클래스에 생성 위임 | OCP 준수 | 공장 |
| **추상 팩토리 (Abstract Factory)** | 생성 | 관련 객체군 일괄 생성 | 일관성 보장 | 가구 세트 |
| **빌더 (Builder)** | 생성 | 복잡한 객체 단계별 생성 | 가독성 향상 | 햄버거 조립 |
| **프로토타입 (Prototype)** | 생성 | 복제를 통한 객체 생성 | 비용 절감 | 3D 프린터 |
| **어댑터 (Adapter)** | 구조 | 인터페이스 호환성 변환 | 레거시 통합 | 독->플러그 |
| **브리지 (Bridge)** | 구조 | 구현과 추상화 분리 | 독립적 확장 | 리모컨/TV |
| **컴포지트 (Composite)** | 구조 | 트리 구조로 객체 구성 | 재귀적 처리 | 폴더 구조 |
| **데코레이터 (Decorator)** | 구조 | 동적으로 책임 추가 | 상속 대체 | 옷 입히기 |
| **퍼사드 (Facade)** | 구조 | 복잡한 서브시스템 단순화 | 진입점 제공 | 리셉션 |
| **플라이웨이트 (Flyweight)** | 구조 | 공유로 메모리 최소화 | 세밀한 객체 | 폰트 캐시 |
| **프록시 (Proxy)** | 구조 | 접근 제어 및 지연 로딩 | 대리인 | 비서 |
| **옵저버 (Observer)** | 행위 | 상태 변화 알림 | 느슨한 결합 | 유튜브 구독 |
| **전략 (Strategy)** | 행위 | 알고리즘 캡슐화 및 교체 | 런타임 교체 | 내비게이션 |
| **커맨드 (Command)** | 행위 | 요청을 객체로 캡슐화 | 실행 취소 가능 | 주문서 |
| **이터레이터 (Iterator)** | 행위 | 순차 접근 | 내부 구조 숨김 | MP3 플레이어 |
| **템플릿 메서드 (Template)** | 행위 | 알고리즘 골격 정의 |Hook 메서드 | 족보 |
| **상태 (State)** | 행위 | 상태별 동작 캡슐화 | 조건문 제거 | 신호등 |
| **책임 연쇄 (Chain of Resp.)** | 행위 | 요청 처리 연쇄 | 순차 처리 | 결재 라인 |
| **미디에이터 (Mediator)** | 행위 | 객체 간 상호작용 중재 | N:N → 1:N | 관제탑 |
| **메멘토 (Memento)** | 행위 | 상태 저장 및 복원 | 실행 취소 | 세이브 파일 |
| **비지터 (Visitor)** | 행위 | 구조와 연산 분리 | 새 연산 추가 용이 | 세무사 |
| **인터프리터 (Interpreter)** | 행위 | 언어 해석기 구현 | DSL 구현 | SQL 파서 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GoF 23 디자인 패턴 분류                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─ 생성 패턴 (Creational) ──────────────────────────────────────────┐ │
│  │ 목적: 객체 생성 로직 캡슐화 → 유연성 확보                           │ │
│  │                                                                     │ │
│  │  ① 싱글톤      - 인스턴스 유일성 보장                               │ │
│  │  ② 팩토리 메서드 - 서브클래스에 생성 위임                           │ │
│  │  ③ 추상 팩토리   - 관련 객체군 일괄 생성                           │ │
│  │  ④ 빌더         - 복잡한 객체 단계별 생성                          │ │
│  │  ⑤ 프로토타입   - 복제를 통한 객체 생성                            │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌─ 구조 패턴 (Structural) ──────────────────────────────────────────┐ │
│  │ 목적: 클래스/객체 간 구조적 관계 정의 → 유연한 구조 설계            │ │
│  │                                                                     │ │
│  │  ⑥ 어댑터       - 인터페이스 호환성 변환                           │ │
│  │  ⑦ 브리지       - 구현과 추상화 분리                               │ │
│  │  ⑧ 컴포지트     - 트리 구조로 객체 구성                            │ │
│  │  ⑨ 데코레이터   - 동적으로 책임 추가                               │ │
│  │  ⑩ 퍼사드       - 복잡한 서브시스템 단순화                         │ │
│  │  ⑪ 플라이웨이트 - 공유로 메모리 최소화                             │ │
│  │  ⑫ 프록시       - 접근 제어 및 지연 로딩                           │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌─ 행위 패턴 (Behavioral) ──────────────────────────────────────────┐ │
│  │ 목적: 객체 간 상호작용과 책임 분배 → 유연한 협력 구조               │ │
│  │                                                                     │ │
│  │  ⑬ 옵저버       - 상태 변화 알림                                   │ │
│  │  ⑭ 전략         - 알고리즘 캡슐화 및 교체                          │ │
│  │  ⑮ 커맨드       - 요청을 객체로 캡슐화                             │ │
│  │  ⑯ 이터레이터   - 순차 접근                                        │ │
│  │  ⑰ 템플릿 메서드 - 알고리즘 골격 정의                              │ │
│  │  ⑱ 상태         - 상태별 동작 캡슐화                               │ │
│  │  ⑲ 책임 연쇄     - 요청 처리 연쇄                                  │ │
│  │  ⑳ 미디에이터   - 객체 간 상호작용 중재                            │ │
│  │  ㉑ 메멘토       - 상태 저장 및 복원                               │ │
│  │  ㉒ 비지터       - 구조와 연산 분리                                 │ │
│  │  ㉓ 인터프리터   - 언어 해석기 구현                                 │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    싱글톤 (Singleton) 패턴                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────┐                                      │
│   │       Singleton             │                                      │
│   ├─────────────────────────────┤                                      │
│   │ - instance: Singleton       │ ← 정적 필드 (유일 인스턴스)          │
│   ├─────────────────────────────┤                                      │
│   │ - Singleton()               │ ← private 생성자 (외부 생성 차단)    │
│   │ + getInstance(): Singleton  │ ← 정적 메서드 (전역 접근점)          │
│   └─────────────────────────────┘                                      │
│                                                                         │
│   스레드 안전 구현: Double-Checked Locking, Enum                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    옵저버 (Observer) 패턴                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────┐           ┌───────────────┐                        │
│   │   Subject     │──────────→│   Observer    │<<interface>>           │
│   ├───────────────┤  attaches ├───────────────┤                        │
│   │ - observers   │           │ + update()    │                        │
│   │ + attach()    │           └───────┬───────┘                        │
│   │ + detach()    │                   │                                │
│   │ + notify()    │           ┌───────┴───────┐                        │
│   └───────┬───────┘           │               │                        │
│           │           ┌───────┴─────┐ ┌───────┴─────┐                  │
│   ┌───────┴───────┐   │ConcreteObs1 │ │ConcreteObs2 │                  │
│   │ConcreteSubject│   │ + update()  │ │ + update()  │                  │
│   │ + getState()  │   └─────────────┘ └─────────────┘                  │
│   └───────────────┘                                                      │
│                                                                         │
│   상태 변경 시 모든 Observer에게 notify() 전파                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    전략 (Strategy) 패턴                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────┐           ┌───────────────┐                        │
│   │   Context     │──────────→│   Strategy    │<<interface>>           │
│   ├───────────────┤  uses     ├───────────────┤                        │
│   │ - strategy    │           │ + execute()   │                        │
│   │ + setStrategy()│          └───────┬───────┘                        │
│   └───────────────┘           ┌───────┴───────┐                        │
│                      ┌────────┴─────┐ ┌───────┴──────┐                 │
│                      │ConcreteStratA│ │ConcreteStratB│                 │
│                      │ + execute()  │ │ + execute()  │                 │
│                      └──────────────┘ └──────────────┘                 │
│                                                                         │
│   런타임에 알고리즘 교체 가능 (OCP 준수)                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 패턴 선택 → ② 구조 설계 → ③ 코드 구현 → ④ 테스트 검증 → ⑤ 리팩토링
```

- **1단계 (패턴 선택)**: 문제 분석 후 적합한 패턴 식별 (생성/구조/행위 분류 기반)
- **2단계 (구조 설계)**: UML 클래스 다이어그램으로 참여 클래스/인터페이스 정의
- **3단계 (코드 구현)**: 언어별 특성 고려하여 구현 (Python 데코레이터 활용 등)
- **4단계 (테스트 검증)**: 단위 테스트로 패턴 동작 검증
- **5단계 (리팩토링)**: 과도한 패턴 적용 시 단순화 (YAGNI 원칙)

**핵심 알고리즘/공식**:

```
[패턴 선택 결정 트리]

객체 생성이 복잡한가?
├─ Yes → 인스턴스가 하나만 필요한가?
│        ├─ Yes → 싱글톤 (Singleton)
│        └─ No → 생성 과정이 단계적인가?
│                 ├─ Yes → 빌더 (Builder)
│                 └─ No → 팩토리 메서드 (Factory Method)
└─ No → (생성 패턴 검토)

인터페이스 호환성 문제인가?
├─ Yes → 어댑터 (Adapter)
└─ No → 기능을 동적으로 추가해야 하는가?
         ├─ Yes → 데코레이터 (Decorator)
         └─ No → 복잡한 서브시스템을 단순화해야 하는가?
                  ├─ Yes → 퍼사드 (Facade)
                  └─ No → (구조 패턴 검토)

알고리즘이 런타임에 교체되어야 하는가?
├─ Yes → 전략 (Strategy)
└─ No → 상태 변화를 다른 객체에 알려야 하는가?
         ├─ Yes → 옵저버 (Observer)
         └─ No → (행위 패턴 검토)

[SOLID 원칙과 패턴 매핑]

S - Single Responsibility:
    팩토리(생성 책임 분리), 커맨드(요청 책임 캡슐화)

O - Open/Closed:
    전략(확장 가능), 데코레이터(수정 없이 추가)

L - Liskov Substitution:
    상태 패턴(상태 객체 교체 가능)

I - Interface Segregation:
    이터레이터(최소 인터페이스)

D - Dependency Inversion:
    의존성 주입 + 팩토리 조합
```

**코드 예시** (필수: Python 구현):

```python
"""
디자인 패턴 핵심 구현 - GoF 23종 중 8개 대표 패턴
- 생성: 싱글톤, 팩토리, 빌더
- 구조: 어댑터, 데코레이터
- 행위: 옵저버, 전략, 커맨드
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from threading import Lock
import copy

# ============================================================
# 1. 싱글톤 (Singleton) - 스레드 안전 구현
# ============================================================

class SingletonMeta(type):
    """스레드 안전 싱글톤 메타클래스"""
    _instances: Dict[type, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """데이터베이스 연결 풀 - 싱글톤 예시"""
    def __init__(self, connection_string: str = "default"):
        self.connection_string = connection_string
        self._connected = False

    def connect(self) -> bool:
        if not self._connected:
            self._connected = True
            print(f"[Singleton] DB 연결 성공: {self.connection_string}")
        return self._connected

    def execute(self, query: str) -> List[Dict]:
        if not self._connected:
            raise RuntimeError("DB 미연결")
        print(f"[Singleton] 쿼리 실행: {query[:30]}...")
        return [{"id": 1, "data": "result"}]


# ============================================================
# 2. 팩토리 메서드 (Factory Method)
# ============================================================

class PaymentMethod(ABC):
    """결제 방식 인터페이스"""
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        print(f"[Factory] 신용카드 {amount:,}원 결제 완료")
        return True


class KakaoPayPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        print(f"[Factory] 카카오페이 {amount:,}원 결제 완료")
        return True


class PaymentFactory:
    """결제 방식 팩토리"""
    _registry: Dict[str, type] = {
        "credit": CreditCardPayment,
        "kakao": KakaoPayPayment,
    }

    @classmethod
    def create(cls, payment_type: str) -> PaymentMethod:
        if payment_type not in cls._registry:
            raise ValueError(f"미지원 결제: {payment_type}")
        return cls._registry[payment_type]()

    @classmethod
    def register(cls, name: str, payment_class: type) -> None:
        """새 결제 방식 동적 등록 (OCP)"""
        cls._registry[name] = payment_class


# ============================================================
# 3. 빌더 (Builder)
# ============================================================

@dataclass
class Computer:
    """복잡한 객체"""
    cpu: str = ""
    ram: int = 0
    storage: str = ""
    gpu: str = ""


class ComputerBuilder:
    """컴퓨터 빌더 - Fluent Interface"""
    def __init__(self):
        self._computer = Computer()

    def cpu(self, cpu: str) -> 'ComputerBuilder':
        self._computer.cpu = cpu
        return self

    def ram(self, gb: int) -> 'ComputerBuilder':
        self._computer.ram = gb
        return self

    def storage(self, storage: str) -> 'ComputerBuilder':
        self._computer.storage = storage
        return self

    def gpu(self, gpu: str) -> 'ComputerBuilder':
        self._computer.gpu = gpu
        return self

    def build(self) -> Computer:
        if not self._computer.cpu:
            raise ValueError("CPU 필수")
        return self._computer


# ============================================================
# 4. 옵저버 (Observer)
# ============================================================

class Observer(ABC):
    @abstractmethod
    def update(self, subject: 'Subject', data: Any) -> None:
        pass


class Subject:
    """관찰 대상"""
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, data: Any = None) -> None:
        for observer in self._observers:
            observer.update(self, data)


class NewsAgency(Subject):
    """뉴스 에이전시"""
    def broadcast(self, news: str) -> None:
        print(f"\n[Observer] 뉴스 송출: {news}")
        self.notify(news)


class NewsChannel(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, subject: Subject, data: Any) -> None:
        print(f"  → [{self.name}] 수신: {data}")


# ============================================================
# 5. 전략 (Strategy)
# ============================================================

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


class QuickSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("[Strategy] 퀵 정렬 사용")
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class BubbleSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("[Strategy] 버블 정렬 사용")
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class Sorter:
    """정렬 컨텍스트"""
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)


# ============================================================
# 6. 데코레이터 (Decorator)
# ============================================================

class Coffee(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class SimpleCoffee(Coffee):
    def get_description(self) -> str:
        return "기본 커피"

    def get_cost(self) -> float:
        return 3000.0


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class MilkDecorator(CoffeeDecorator):
    def get_description(self) -> str:
        return self._coffee.get_description() + " + 우유"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 500.0


class MochaDecorator(CoffeeDecorator):
    def get_description(self) -> str:
        return self._coffee.get_description() + " + 모카"

    def get_cost(self) -> float:
        return self._coffee.get_cost() + 800.0


# ============================================================
# 7. 어댑터 (Adapter)
# ============================================================

class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str) -> None:
        pass


class MP3Player(MediaPlayer):
    def play(self, filename: str) -> None:
        print(f"[Adapter] MP3 재생: {filename}")


class VLCPlayer:
    """외부 라이브러리 (인터페이스 다름)"""
    def play_video(self, video_file: str) -> None:
        print(f"[Adapter] VLC 비디오: {video_file}")


class VLCAdapter(MediaPlayer):
    """VLC 어댑터"""
    def __init__(self):
        self._vlc = VLCPlayer()

    def play(self, filename: str) -> None:
        self._vlc.play_video(filename)


# ============================================================
# 8. 커맨드 (Command)
# ============================================================

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    """리시버"""
    def on(self) -> None:
        print("[Command] 전등 ON")

    def off(self) -> None:
        print("[Command] 전등 OFF")


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.on()

    def undo(self) -> None:
        self._light.off()


class RemoteControl:
    """인보커"""
    def __init__(self):
        self._commands: Dict[str, Command] = {}
        self._history: List[Command] = []

    def set_command(self, slot: str, command: Command) -> None:
        self._commands[slot] = command

    def press(self, slot: str) -> None:
        if slot in self._commands:
            command = self._commands[slot]
            command.execute()
            self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            self._history.pop().undo()


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("1. 싱글톤 패턴")
    print("=" * 50)
    db1 = DatabaseConnection("mysql://localhost")
    db2 = DatabaseConnection("mysql://localhost")
    print(f"동일 인스턴스? {db1 is db2}")
    db1.connect()

    print("\n" + "=" * 50)
    print("2. 팩토리 메서드 패턴")
    print("=" * 50)
    payment = PaymentFactory.create("kakao")
    payment.pay(50000)

    print("\n" + "=" * 50)
    print("3. 빌더 패턴")
    print("=" * 50)
    gaming_pc = (ComputerBuilder()
                 .cpu("Intel i9-13900K")
                 .ram(64)
                 .storage("2TB NVMe")
                 .gpu("RTX 4090")
                 .build())
    print(f"사양: {gaming_pc}")

    print("\n" + "=" * 50)
    print("4. 옵저버 패턴")
    print("=" * 50)
    agency = NewsAgency()
    agency.attach(NewsChannel("KBS"))
    agency.attach(NewsChannel("MBC"))
    agency.broadcast("속보: AI 기술 혁신!")

    print("\n" + "=" * 50)
    print("5. 전략 패턴")
    print("=" * 50)
    data = [64, 34, 25, 12, 22, 11, 90]
    sorter = Sorter(BubbleSortStrategy())
    print(f"정렬 결과: {sorter.sort(data)}")

    print("\n" + "=" * 50)
    print("6. 데코레이터 패턴")
    print("=" * 50)
    coffee = SimpleCoffee()
    coffee = MilkDecorator(coffee)
    coffee = MochaDecorator(coffee)
    print(f"{coffee.get_description()}: {coffee.get_cost():,}원")

    print("\n" + "=" * 50)
    print("7. 어댑터 패턴")
    print("=" * 50)
    players: List[MediaPlayer] = [MP3Player(), VLCAdapter()]
    for player in players:
        player.play("movie.mp4")

    print("\n" + "=" * 50)
    print("8. 커맨드 패턴")
    print("=" * 50)
    light = Light()
    remote = RemoteControl()
    remote.set_command("ON", LightOnCommand(light))
    remote.press("ON")
    remote.undo_last()
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| **재사용성**: 검증된 솔루션으로 개발 시간 단축 | **복잡성 증가**: 과도한 추상화로 코드 이해도 저하 |
| **의사소통**: "옵저버 쓰자" → 팀원 모두 동일 이해 | **학습 비용**: 23종 패턴 숙지에 상당한 시간 필요 |
| **확장성**: OCP 준수로 기존 코드 수정 없이 확장 | **오버엔지니어링**: 간단한 문제에 복잡한 패턴 적용 |
| **품질 보장**: 검증된 구조로 결함 감소 | **성능 오버헤드**: 추가 추상화 계층으로 인한 비용 |

**카테고리별 패턴 비교**:

| 비교 항목 | 생성 패턴 | 구조 패턴 | 행위 패턴 |
|---------|----------|----------|----------|
| **핵심 목적** | 객체 생성 캡슐화 | 객체 간 관계 구성 | 객체 간 협력 정의 |
| **대표 패턴** | 싱글톤, 팩토리, 빌더 | 어댑터, 데코레이터 | 옵저버, 전략, 커맨드 |
| **해결 문제** | new 키워드 직접 사용 | 인터페이스 불일치 | if-else 남용, 하드코딩 |
| **적용 시점** | 초기 설계, DI 컨테이너 | 레거시 통합, 기능 확장 | 상태 관리, 알고리즘 교체 |
| **Spring 예시** | @Bean, @Component | @Adapter, @Proxy | @EventListener |

**대안 기술 비교** (필수: 최소 2개 대안):

| 비교 항목 | 디자인 패턴 | 함수형 프로그래밍 | 메타프로그래밍 |
|---------|----------|----------|----------|
| **핵심 특성** | ★ 객체 지향 설계 템플릿 | 순수 함수, 불변성 | 코드 생성 코드 |
| **상태 관리** | 가변 객체, 캡슐화 | 불변 데이터 | 컴파일 타임 생성 |
| **복잡도** | 중간 (클래스 구조) | 낮음 (함수 조합) | 높음 (매크로/리플렉션) |
| **적합 환경** | ★ 엔터프라이즈 Java/C# | 데이터 처리, 동시성 | 프레임워크/라이브러리 |
| **학습 곡선** | 중간 | 높음 (패러다임 전환) | 높음 |

> **★ 선택 기준**: 엔터프라이즈 애플리케이션은 디자인 패턴, 데이터 파이프라인은 함수형, 프레임워크 개발은 메타프로그래밍 고려. 현대 언어는 여러 패러다임 혼합 가능

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **프레임워크 개발** | 싱글톤+팩토리+전략 조합으로 플러그인 아키텍처 | 확장성 200% 향상, 신규 기능 추가 시간 50% 단축 |
| **레거시 통합** | 어댑터+퍼사드로 기존 시스템 래핑 후 점진적 마이그레이션 | 통합 리스크 70% 감소 |
| **마이크로서비스** | 옵저버+커맨드로 이벤트 소싱 아키텍처 | 서비스 간 결합도 60% 감소 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Spring Framework** - IoC 컨테이너가 팩토리 패턴, 빈은 싱글톤(기본), AOP는 프록시 패턴으로 구현. 전 세계 Java 개발자 90% 사용

- **사례 2: React 상태관리** - Redux는 옵저버 패턴(store → subscribers), Flux 아키텍처는 디스패처(미디에이터) 활용. 페이스북 개발

- **사례 3: Django ORM** - 활성 레코드 패턴(컴포지트 변형)으로 DB 추상화. 인스타그램, 핀터레스트 초기 버전에서 사용

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: 언어/플랫폼 지원 여부 (Python 데코레이터 언어 레벨 지원, Java 어노테이션)
2. **운영적**: DI 컨테이너(Spring) 도입 시 런타임 디버깅 난이도 증가
3. **보안적**: 싱글톤은 전역 상태로 인한 스레드 안전성 이슈, 프록시는 권한 검증 필수
4. **경제적**: 초기 학습 비용 vs 장기 유지보수 비용 절감 (ROI 2~3년 관점)

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **안티패턴: God Singleton**: 싱글톤에 모든 상태를 몰아넣어 전역 변수처럼 남용 → 테스트 불가, 결합도 급증
- ❌ **오버엔지니어링**: "Hello World"에도 팩토리, 빌더, 전략 패턴 적용 → YAGNI 원칙 위반
- ❌ **패턴 숭배**: "이 문제는 반드시 이 패턴으로 해결해야 한다"는 고집 → 상황에 맞는 단순한 해결책 무시

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  디자인 패턴 핵심 연관 개념 맵                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [SOLID 원칙] ←──────→ [디자인 패턴] ←──────→ [리팩토링]       │
│        ↓                      ↓                    ↓            │
│   [클린 아키텍처]       [DDD(도메인 주도)]    [TDD]             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| SOLID 원칙 | 선행 개념 | 디자인 패턴의 이론적 기반 | `[software_design](./software_design.md)` |
| 리팩토링 | 후속 개념 | 패턴 적용을 통한 코드 개선 | `[software_quality](../quality/software_quality.md)` |
| 아키텍처 패턴 | 확장 개념 | 패턴의 대규모 적용 | `[software_architecture](./software_architecture.md)` |
| 의존성 주입(DI) | 구현 기술 | 패턴 구현을 위한 프레임워크 | `[devsecops](../methodology/devsecops.md)` |
| UML | 표현 도구 | 패턴 구조 시각화 | `[uml](./uml.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **코드 재사용** | 검증된 패턴 적용으로 개발 시간 단축 | 개발 기간 30% 단축 |
| **유지보수** | OCP 준수로 변경 영향 최소화 | 변경 비용 50% 절감 |
| **의사소통** | 패턴 이름만으로 설계 의도 전달 | 코드 리뷰 시간 40% 단축 |
| **테스트 용이성** | DI 기반 테스트 가능 구조 | 테스트 커버리지 80% 이상 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AI 코파일럿(GitHub Copilot, Claude)이 상황에 맞는 패턴 자동 제안. 패턴 적용 코드 자동 생성

2. **시장 트렌드**: 함수형 프로그래밍과 객체지향 패턴의 융합 (Kotlin, Scala, Rust). 불변성 중심 설계로 전환

3. **후속 기술**: 언어 레벨 패턴 지원 확대 (Python 데코레이터, Rust trait, Go interface). 메타프로그래밍으로 패턴 자동화

> **결론**: 디자인 패턴은 30년간 검증된 소프트웨어 설계의 정석이다. 패턴 자체보다 **"왜 이 패턴이 필요한가"를 이해**하는 것이 핵심이며, 현대 언어와 AI 도구를 활용해 적절히 적용할 때 진정한 가치를 발휘한다.

> **※ 참고 표준**: GoF "Design Patterns" (1994), POSA (Pattern-Oriented Software Architecture), ISO/IEC 25010(SQuaRE)

---

## 어린이를 위한 종합 설명

디자인 패턴은 마치 **"레고 조립 설명서"** 같아요!

레고로 성을 만들 때, 매번 처음부터 "어떻게 쌓지?" 고민하지 않죠. 이미 검증된 조립법이 있어요. "기둥은 이렇게 세우고, 지붕은 저렇게 올린다"는 식으로요.

디자인 패턴도 똑같아요. 수많은 프로그래머들이 30년 동안 고민하며 찾아낸 **"프로그램 짜는 좋은 방법들"**을 정리해둔 것이에요.

**첫 번째 이야기: 싱글톤 (혼자만 있기)**

학교에 교무실이 하나만 있으면 좋겠죠? 선생님들이 여러 교무실에 흩어져 있으면 찾기 힘드니까요. 싱글톤은 "이 건물은 딱 하나만 만들자!"라는 약속이에요.

**두 번째 이야기: 옵저버 (소문내기)**

유튜버가 새 영상을 올리면 구독자들에게 알림이 가요. 유튜버는 "누가 구독했는지" 목록을 가지고 있고, 새 영상이 올라오면 모두에게 "영상 나왔어!" 하고 알려주죠. 이게 옵저버 패턴이에요!

**세 번째 이야기: 전략 (게임 캐릭터 교체)**

롤 게임에서 챔피언을 바꾸면 스킬도 바뀌죠? 전략 패턴도 이와 같아요. "어떤 방식으로 공격할지"를 언제든 바꿀 수 있어요.

이렇게 디자인 패턴은 **"자주 생기는 문제를 해결하는 좋은 방법"**을 정리해둔 레시피북이에요! 🍳
