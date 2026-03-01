+++
title = "소프트웨어 설계 (Software Design)"
date = 2025-03-01

[extra]
categories = "software_engineering-design"
+++

# 소프트웨어 설계 (Software Design)

## 핵심 인사이트 (3줄 요약)
> **무엇을 어떻게 만들지 정의하는 과정**. 요구사항을 구현 가능한 구조로 변환. 추상화, 모듈화, 정보 은닉 등의 원칙을 적용하여 유지보수성과 재사용성을 확보.

## 1. 개념
소프트웨어 설계는 **요구사항을 만족하는 소프트웨어의 구조, 컴포넌트, 인터페이스, 특성을 정의하는 과정**이다.

> 비유: "건축 설계도" - 집을 짓기 전에 어떻게 지을지 도면을 그리는 것

## 2. 설계 단계

```
┌─────────────────────────────────────────────────────────┐
│                   설계 단계                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   요구사항 명세서 (SRS)                                 │
│         │                                               │
│         ▼                                               │
│   ┌─────────────────────────────────────────┐          │
│   │         아키텍처 설계 (상위 설계)         │          │
│   │  - 시스템 구조                          │          │
│   │  - 컴포넌트 식별                        │          │
│   │  - 인터페이스 정의                      │          │
│   └──────────────────┬──────────────────────┘          │
│                      │                                  │
│                      ▼                                  │
│   ┌─────────────────────────────────────────┐          │
│   │         상세 설계 (하위 설계)            │          │
│   │  - 모듈 내부 구조                       │          │
│   │  - 알고리즘 설계                        │          │
│   │  - 데이터 구조                         │          │
│   └──────────────────┬──────────────────────┘          │
│                      │                                  │
│                      ▼                                  │
│              설계 문서 (SDD)                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 3. 설계 원칙

### 3.1 기본 원칙
```
1. 추상화 (Abstraction)
   ┌─────────────────────────────────────┐
   │ 불필요한 세부사항을 숨기고          │
   │ 핵심 개념만 표현                    │
   │                                     │
   │ 종류:                               │
   │ - 과정 추상화 (Procedure)           │
   │ - 데이터 추상화 (Data)              │
   │ - 제어 추상화 (Control)             │
   └─────────────────────────────────────┘

   예: 자동차
   추상화 전: 엔진, 기어, 타이어, 배기구...
   추상화 후: 운전 (핸들, 페달, 기어)

2. 정보 은닉 (Information Hiding)
   ┌─────────────────────────────────────┐
   │ 모듈 내부 구현을 숨기고             │
   │ 인터페이스만 공개                   │
   │                                     │
   │ 효과:                               │
   │ - 변경 영향 최소화                  │
   │ - 결합도 감소                       │
   └─────────────────────────────────────┘

3. 모듈화 (Modularity)
   ┌─────────────────────────────────────┐
   │ 시스템을 독립적인 모듈로 분할       │
   │                                     │
   │ 장점:                               │
   │ - 병렬 개발 가능                    │
   │ - 재사용성 향상                     │
   │ - 유지보수 용이                     │
   └─────────────────────────────────────┘

4. 단계적 분해 (Stepwise Refinement)
   ┌─────────────────────────────────────┐
   │ 상위 수준에서 하위 수준으로         │
   │ 점진적으로 상세화                   │
   │                                     │
   │ Top-Down 접근                       │
   └─────────────────────────────────────┘

5. 구조적 분할 (Structured Partitioning)
   ┌─────────────────────────────────────┐
   │ 기능적 독립성 확보                  │
   │ - 높은 응집도                       │
   │ - 낮은 결합도                       │
   └─────────────────────────────────────┘
```

### 3.2 기능적 독립성
```
┌────────────────────────────────────────────────────────┐
│                  기능적 독립성                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│    ┌──────────────────┐      ┌──────────────────┐     │
│    │                  │      │                  │     │
│    │    응집도 ↑      │      │    결합도 ↓      │     │
│    │  (Cohesion)      │      │   (Coupling)     │     │
│    │                  │      │                  │     │
│    │  모듈 내부 요소   │      │  모듈 간 의존성   │     │
│    │  얼마나 관련있나   │      │  얼마나 의존하나   │     │
│    │                  │      │                  │     │
│    └──────────────────┘      └──────────────────┘     │
│                                                        │
│    좋은 설계: 높은 응집도 + 낮은 결합도                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 응집도 (Cohesion)

```
모듈 내부 구성요소 간의 관련성 정도
(높을수록 좋음)

┌─────────────────────────────────────────────────────┐
│              응집도 (높음 → 낮음)                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 기능적 응집도 (Functional)       ★★★★★        │
│     - 단일 기능 수행                                │
│     - 예: 제곱근 계산 함수                          │
│                                                     │
│  2. 순차적 응집도 (Sequential)       ★★★★☆        │
│     - 한 기능의 출력이 다른 기능의 입력             │
│     - 예: 입력 → 처리 → 출력                       │
│                                                     │
│  3. 교환적 응집도 (Communicational)  ★★★☆☆        │
│     - 같은 데이터 사용                              │
│     - 예: 같은 파일을 읽고 쓰기                     │
│                                                     │
│  4. 절차적 응집도 (Procedural)       ★★☆☆☆        │
│     - 실행 순서에 따른 관계                         │
│     - 예: 초기화 → 실행 → 종료                      │
│                                                     │
│  5. 시간적 응집도 (Temporal)         ★★☆☆☆        │
│     - 동시에 실행                                   │
│     - 예: 초기화 함수                               │
│                                                     │
│  6. 논리적 응집도 (Logical)          ★☆☆☆☆        │
│     - 논리적 유사성                                 │
│     - 예: 모든 입출력 함수                          │
│                                                     │
│  7. 우연적 응집도 (Coincidental)     ☆☆☆☆☆        │
│     - 관계 없음                                     │
│     - 예: 유틸리티 함수 모음                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 5. 결합도 (Coupling)

```
모듈 간의 의존성 정도
(낮을수록 좋음)

┌─────────────────────────────────────────────────────┐
│              결합도 (낮음 → 높음)                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 내용 결합도 (Content)           ★★★★★ 최악    │
│     - 다른 모듈의 내부 데이터 직접 접근            │
│                                                     │
│  2. 공통 결합도 (Common)            ★★★★☆         │
│     - 전역 데이터 공유                              │
│                                                     │
│  3. 외부 결합도 (External)          ★★★☆☆         │
│     - 외부 데이터 포맷, 프로토콜 공유               │
│                                                     │
│  4. 제어 결합도 (Control)           ★★☆☆☆         │
│     - 제어 정보 전달 (플래그)                       │
│                                                     │
│  5. 스탬프 결합도 (Stamp)           ★★☆☆☆         │
│     - 자료구조 일부 전달                            │
│                                                     │
│  6. 자료 결합도 (Data)              ★☆☆☆☆ 최선    │
│     - 단순 데이터만 전달                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 6. 객체지향 설계 원칙 (SOLID)

```
SOLID 원칙:

S - Single Responsibility (단일 책임)
    ┌─────────────────────────────────────┐
    │ 클래스는 하나의 책임만 가져야 함    │
    │ 예: User 클래스는 사용자 정보만     │
    │     이메일 발송은 EmailSender       │
    └─────────────────────────────────────┘

O - Open/Closed (개방-폐쇄)
    ┌─────────────────────────────────────┐
    │ 확장에는 열려 있고, 수정엔 닫혀 있음│
    │ 예: 인터페이스로 확장, 기존 코드    │
    │     수정 없이 새 기능 추가          │
    └─────────────────────────────────────┘

L - Liskov Substitution (리스코프 치환)
    ┌─────────────────────────────────────┐
    │ 자식은 부모를 대체할 수 있어야 함   │
    │ 예: Bird → Penguin은 날 수 없음    │
    │     → Flyable 인터페이스 분리       │
    └─────────────────────────────────────┘

I - Interface Segregation (인터페이스 분리)
    ┌─────────────────────────────────────┐
    │ 인터페이스를 작게 분리              │
    │ 예: Worker → Workable, Eatable     │
    └─────────────────────────────────────┘

D - Dependency Inversion (의존성 역전)
    ┌─────────────────────────────────────┐
    │ 추상화에 의존, 구체화에 의존하지 않음│
    │ 예: UserController → IUserService  │
    └─────────────────────────────────────┘
```

## 7. 코드 예시

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

# ===== 응집도 예시 =====

# 나쁜 예: 우연적 응집도
class BadUtility:
    """관련 없는 기능들이 섞여 있음"""
    def calculate_tax(self, price): ...
    def send_email(self, to, subject): ...
    def validate_phone(self, phone): ...

# 좋은 예: 기능적 응집도
class TaxCalculator:
    """단일 기능: 세금 계산"""
    def calculate(self, price: float, rate: float) -> float:
        return price * rate


# ===== 결합도 예시 =====

# 나쁜 예: 내용 결합도
class BadOrder:
    def __init__(self):
        self.customer_name = ""
        self.customer_address = ""

class BadShipping:
    def print_label(self, order: BadOrder):
        # Order 내부 데이터 직접 접근
        print(f"To: {order.customer_name}")
        print(f"Address: {order.customer_address}")

# 좋은 예: 자료 결합도
@dataclass
class ShippingInfo:
    name: str
    address: str

class Order:
    def get_shipping_info(self) -> ShippingInfo:
        return ShippingInfo(self.customer_name, self.customer_address)

class Shipping:
    def print_label(self, info: ShippingInfo):
        print(f"To: {info.name}")
        print(f"Address: {info.address}")


# ===== SOLID 원칙 예시 =====

# S: 단일 책임 원칙
class User:
    """사용자 정보만 관리"""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserRepository:
    """저장소 역할만"""
    def save(self, user: User):
        print(f"Saving user: {user.name}")

class EmailSender:
    """이메일 발송만"""
    def send(self, to: str, subject: str, body: str):
        print(f"Sending email to {to}: {subject}")

# O: 개방-폐쇄 원칙
class PaymentProcessor(ABC):
    """결제 처리 추상화"""
    @abstractmethod
    def process(self, amount: float):
        pass

class CreditCardPayment(PaymentProcessor):
    def process(self, amount: float):
        print(f"Processing credit card payment: ${amount}")

class PayPalPayment(PaymentProcessor):
    def process(self, amount: float):
        print(f"Processing PayPal payment: ${amount}")

# 새로운 결제 방식 추가 시 기존 코드 수정 없음
class KakaoPay(PaymentProcessor):
    def process(self, amount: float):
        print(f"Processing KakaoPay: ${amount}")

# L: 리스코프 치환 원칙
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        self.fly()

    def fly(self):
        print("Flying...")

class Penguin(Bird):
    def move(self):
        self.walk()

    def walk(self):
        print("Walking...")

# I: 인터페이스 분리 원칙
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class HumanWorker(Workable, Eatable):
    def work(self):
        print("Working...")

    def eat(self):
        print("Eating lunch...")

class RobotWorker(Workable):
    def work(self):
        print("Working...")

# D: 의존성 역전 원칙
class NotificationService(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class EmailNotification(NotificationService):
    def send(self, message: str):
        print(f"Email: {message}")

class SMSNotification(NotificationService):
    def send(self, message: str):
        print(f"SMS: {message}")

class UserService:
    """추상화에 의존"""
    def __init__(self, notification: NotificationService):
        self.notification = notification

    def notify_user(self, message: str):
        self.notification.send(message)


# ===== 설계 품질 분석기 =====
class DesignAnalyzer:
    """설계 품질 분석"""

    @staticmethod
    def analyze_cohesion(module_code: str) -> str:
        """응집도 분석 (간소화)"""
        # 실제로는 코드 분석 수행
        return "기능적 응집도"

    @staticmethod
    def analyze_coupling(class_a: type, class_b: type) -> str:
        """결합도 분석 (간소화)"""
        return "자료 결합도"

    @staticmethod
    def check_solid_principles(cls: type) -> Dict[str, bool]:
        """SOLID 원칙 체크"""
        return {
            "Single_Responsibility": True,
            "Open_Closed": True,
            "Liskov_Substitution": True,
            "Interface_Segregation": True,
            "Dependency_Inversion": True
        }


# 사용 예시
print("=== 설계 원칙 예시 ===\n")

# SOLID 예시
print("--- SOLID 원칙 ---")
email_notification = EmailNotification()
user_service = UserService(email_notification)
user_service.notify_user("회원가입을 환영합니다!")

# 새로운 알림 방식으로 교체 (의존성 역전)
sms_notification = SMSNotification()
user_service = UserService(sms_notification)
user_service.notify_user("인증번호: 123456")

# 결제 처리 (개방-폐쇄)
processors: List[PaymentProcessor] = [
    CreditCardPayment(),
    PayPalPayment(),
    KakaoPay()
]

print("\n--- 다양한 결제 방식 ---")
for processor in processors:
    processor.process(100.0)
```

## 8. 설계 품질 지표

```
1. 응집도 (Cohesion)
   - 높을수록 좋음
   - 모듈 내부 요소 간 관련성

2. 결합도 (Coupling)
   - 낮을수록 좋음
   - 모듈 간 의존성

3. 복잡도 (Complexity)
   - 낮을수록 좋음
   - 순환 복잡도 (Cyclomatic)

4. 팬인/팬아웃 (Fan-in/Fan-out)
   - 팬인: 이 모듈을 호출하는 수 (높으면 재사용성)
   - 팬아웃: 이 모듈이 호출하는 수 (높으면 복잡)

5. 크기 (Size)
   - 적당한 모듈 크기
   - 너무 크면 분할, 너무 작으면 통합
```

## 9. 장단점

### 좋은 설계의 장점
| 장점 | 설명 |
|-----|------|
| 유지보수성 | 변경 용이 |
| 재사용성 | 모듈 재사용 |
| 테스트 용이 | 독립적 테스트 |
| 이해성 | 구조 명확 |

### 과도한 설계의 단점
| 단점 | 설명 |
|-----|------|
| 복잡성 | 과도한 추상화 |
| 성능 | 오버헤드 |
| 시간 | 설계 시간 증가 |

## 10. 실무에선? (기술사적 판단)
- **실용적 설계**: 완벽보다 적절한 수준
- **YAGNI**: 필요 없는 기능은 미리 만들지 않음
- **KISS**: 단순하게 유지
- **DRY**: 반복하지 않음
- **리팩토링**: 점진적 개선

## 11. 관련 개념
- SOLID 원칙
- 디자인 패턴
- 아키텍처
- UML

---

## 어린이를 위한 종합 설명

**소프트웨어 설계는 "레고 설계도" 같아요!**

### 설계 원칙 📐
```
추상화: 중요한 것만 보기
  "자동차 → 운전대, 페달만"

정보 은닉: 속 감추기
  "TV 리모컨 → 버튼만, 속은 몰라"

모듈화: 조각내기
  "머리, 몸, 팔다리 따로 만들기"
```

### 응집도 vs 결합도 ⚖️
```
응집도: 한 조각 안에서 얼마나 관련있나?
  높을수록 좋아요! ⬆️

결합도: 조각끼리 얼마나 엮여있나?
  낮을수록 좋아요! ⬇️
```

### SOLID 원칙 🔷
```
S: 한 가지만 해요
O: 늘릴 수 있게 해요
L: 바꿔도 잘 작동해요
I: 작게 나눠요
D: 추상적으로 연결해요
```

**비밀**: 좋은 설계는 나중에 고생 안 해요! 🎯✨
