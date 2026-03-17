+++
title = "42. 리팩토링 (Refactoring)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Refactoring", "Code-Smell", "Technical-Debt", "Clean-Code", "Martin-Fowler"]
draft = false
+++

# 리팩토링 (Refactoring)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리팩토링은 **"외부 **동작**을 **변경**하지 **않고 **내부 **구조**를 **개선**하는 **것\"**으로, **Code Smell**(나쁜 **코드 **냄새)**를 **제거**하고 **Technical Debt**(기술 **부채)**를 **상환**하며 **가독성**, **유지보수성**, **성능**을 **향상**시킨다.
> 2. **유형**: **Extract Method**(메서드 **추출), **Inline Method**(메서드 **인라인화)**, **Rename Variable**(변수 **이름 **변경)**, **Extract Class**(클래스 **추출)**, **Move Method**(메서드 **이동)**이 **있고 **Red-Green-Refactor**(TDD **주기)**로 **안전**하게 **진행**한다.
> 3. **도구**: **IDE**(IntelliJ, VS Code)**의 **Automated Refactor**, **Linters**(ESLint, **Pylint)**, **Static Analysis**(SonarQube, **CodeQL)**가 **도움**을 **주고 **Unit Tests**(단위 **테스트)**가 **회귀 **방지**를 **보장**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
리팩토링은 **"코드 구조 개선"**이다.

**리팩토링 vs 재작성**:
| 구분 | 리팩토링 | 재작성 |
|------|----------|--------|
| **범위** | 점진적 | 전체 |
| **위험** | 낮음 | 높음 |
| **테스트** | 필수 | 선택 |
| **기간** | 짧음 | 김 |

### 💡 비유
리팩토링은 ****집 **개조 ****와 같다.
- **외관**: 그대로
- **내부**: 강화
- **거주**: 불필요

---

## Ⅱ. 아키텍처 및 핵심 원리

### Code Smell 유형

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Common Code Smells                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Long Method:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Bad:                                                                         │  │
    │  │  def process_order(order):                                                     │  │  │
    │  │      validate_customer(order.customer)                                          │  │  │
    │  │      check_inventory(order.items)                                               │  │  │
    │  │      calculate_tax(order)                                                        │  │  │
    │  │      apply_discount(order)                                                      │  │  │
    │  │      save_to_db(order)                                                          │  │  │
    │  │      send_email(order)                                                          │  │  │
    │  │      update_shipment(order)                                                      │  │  │
    │  │      # ... 100 more lines                                                       │  │  │
    │  │                                                                                     │  │  │
    │  │  Good (Extract Method):                                                           │  │  │
    │  │  def process_order(order):                                                         │  │  │
    │  │      validate_customer(order.customer)                                             │  │  │
    │  │      reserve_inventory(order.items)                                               │  │  │
    │  │      charge_payment(order)                                                         │  │  │
    │  │      fulfill_order(order)                                                          │  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Duplicated Code:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Bad:                                                                         │  │
    │  │  # In User class                                                                 │  │  │
    │  │  def send_email(self, user):                                                      │  │  │
    │  │      smtp = smtplib.SMTP('smtp.example.com')                                       │  │  │
    │  │      smtp.sendmail(from, to, message)                                              │  │  │
    │  │                                                                                     │  │  │
    │  │  # In Order class                                                                 │  │  │
    │  │  def send_email(self, order):                                                    │  │  │
    │  │      smtp = smtplib.SMTP('smtp.example.com')  # DUPLICATE!                         │  │  │
    │  │      smtp.sendmail(from, to, message)                                              │  │  │
    │  │                                                                                     │  │  │
    │  │  Good (Extract Class):                                                            │  │  │
    │  │  class EmailService:                                                                │  │  │
    │  │      def send(self, from, to, message):                                              │  │  │
    │  │          smtp = smtplib.SMTP('smtp.example.com')                                    │  │  │
    │  │          smtp.sendmail(from, to, message)                                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Large Class:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Bad:                                                                         │  │
    │  │  class User:  # 2000 lines!                                                          │  │  │
    │  │      def validate(self)                                                             │  │  │
    │  │      def save(self)                                                                 │  │  │
    │  │      def send_email(self)                                                           │  │  │
    │  │      def calculate_discount(self)                                                    │  │  │
    │  │      def update_profile(self)                                                       │  │  │
    │  │      # ... many more unrelated methods                                                │  │  │
    │  │                                                                                     │  │  │
    │  │  Good (Extract Class):                                                            │  │  │
    │  │  class User:  # Core user logic                                                     │  │  │
    │  │      def validate(self)                                                             │  │  │
    │  │      def save(self)                                                                 │  │  │
    │  │                                                                                     │  │  │
    │  │  class EmailService:  # Email logic                                                  │  │  │
    │  │      def send_to_user(self, user, message)                                           │  │  │
    │  │                                                                                     │  │  │
    │  │  class DiscountService:  # Discount logic                                            │  │  │
    │  │      def calculate_for_user(self, user)                                               │  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 리팩토링 주기 (Red-Green-Refactor)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         TDD Refactoring Cycle                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. RED: Write failing test                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  test_calculate_discount():                                                          │  │  │
    │  │      user = User(tier="gold")                                                        │  │  │
    │  │      assert user.discount(100) == 20   # Expected 20% discount                     │  │  │
    │  │                                                                                     │  │  │
    │  │  Run: FAIL (no discount method)                                                      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  2. GREEN: Make test pass (minimal code)                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  class User:                                                                          │  │  │
    │  │      def discount(self, amount):                                                      │  │  │
    │  │          return amount * 0.2  # Hardcoded!                                           │  │  │
    │  │                                                                                     │  │  │
    │  │  Run: PASS                                                                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  3. REFACTOR: Improve code (tests still pass)                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  class User:                                                                          │  │  │
    │  │      def discount(self, amount):                                                      │  │  │
    │  │          discount_rates = {"gold": 0.2, "silver": 0.1, "bronze": 0.05}             │  │  │
    │  │          return amount * discount_rates.get(self.tier, 0)                              │  │  │
    │  │                                                                                     │  │  │
    │  │  Run: PASS (better code!)                                                             │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  Repeat for each requirement                                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 리팩토링 기법

| 기법 | 설명 | 예시 |
|------|------|------|
| **Extract Method** | 코드 블록을 메서드로 | 긴 함수 분해 |
| **Inline Method** | 메서드를 호출처럼 대체 | 간단한 메서드 |
| **Rename** | 이름을 명확하게 | 변수/함수 |
| **Extract Class** | 클래스 분리 | 대형 클래스 |
| **Move Method** | 메서드 이동 | 책임 이동 |

### Extract Method Example

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Extract: Before & After                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Before:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  def print_statement(self, order):                                                      │  │
    │      print("ORDER DETAILS")                                                              │  │
    │      print(f"Order ID: {order.id}")                                                      │  │
    │      print(f"Customer: {order.customer.name}")                                          │  │
    │      print(f"Total: ${order.total}")                                                     │  │
    │      outstanding = order.total - order.paid                                              │  │
    │      print(f"Outstanding: ${outstanding}")                                              │  │
    │      if outstanding > 0:                                                               │  │
    │          print("STATUS: UNPAID")                                                         │  │
    │      else:                                                                               │  │
    │          print("STATUS: PAID")                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    After:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  def print_statement(self, order):                                                      │  │
    │      print("ORDER DETAILS")                                                              │  │
    │      self._print_order_details(order)                                                   │  │
    │      self._print_payment_status(order)                                                   │  │
    │                                                                                         │  │
    │  def _print_order_details(self, order):  # Extracted                                     │  │
    │      print(f"Order ID: {order.id}")                                                      │  │
    │      print(f"Customer: {order.customer.name}")                                          │  │
    │      print(f"Total: ${order.total}")                                                     │  │
    │                                                                                         │  │
    │  def _print_payment_status(self, order):  # Extracted                                   │  │
    │      outstanding = order.total - order.paid                                              │  │
    │      print(f"Outstanding: ${outstanding}")                                              │  │
    │      if outstanding > 0:                                                               │  │
    │          print("STATUS: UNPAID")                                                         │  │
    │      else:                                                                               │  │
    │          print("STATUS: PAID")                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Legacy 코드 현대화
**상황**: 10년된 PHP 코드
**판단**: 점진적 리팩토링 + 테스트

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Legacy Modernization Strategy                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Approach: Strangler Fig Pattern
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Legacy System (Monolith)                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  ← Request ──> │  Legacy Controller ──> │  Legacy Model ──> │  DB │            │  │  │
    │  │  │              └─────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Add Facade/Proxy                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  ┌──────────────┐     ┌──────────────────────────────────────────────────────┐      │  │  │
    │  │  │  API Gateway  │ ──> │  Feature Flag Service                                    │      │  │  │
    │  │  └──────────────┘     │  ┌────────────────────────────────────────────────┐    │      │  │  │
    │  │                      │  │  feature: new_checkout (percent: 10%)    │    │      │  │  │
    │  │                      │  └────────────────────────────────────────────────┘    │      │  │  │
    │  │                      │       │                                                │      │  │  │
    │  │                      │       ├─ 10% → New Service                               │      │  │  │
    │  │                      │       └─ 90% → Legacy                                  │      │  │  │
    │  │                      │                                                        │      │  │  │
    │  │                      │  New Service (Microservice)                      │      │  │  │
    │  │                      │  ┌──────────────────────────────────────────────┐      │      │  │  │
    │  │                      │  │  Modern Checkout (Go/Python)               │      │      │  │  │
    │  │                      │  │  - Clean architecture                    │      │      │  │  │
    │  │                      │  │  - Unit tests, integration tests          │      │      │  │  │
    │  │                      │  │  - Observed metrics                       │      │      │  │  │
    │  │                      │  └──────────────────────────────────────────────┘      │      │  │  │
    │  │                      └─────────────────────────────────────────────────┘      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Process:                                                                               │  │
    │  1. Add tests around legacy code (characterization tests)                               │  │
    │  2. Create facade/router with feature flags                                              │  │
    │  3. Implement new service with tests                                                     │  │
    │  4. Gradually route traffic (10% → 50% → 100%)                                          │  │
    │  5. Deprecate legacy code                                                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 리팩토링 기대 효과

| 효과 | 리팩토링 전 | 후 |
|------|------------|------|
| **버그** | 15/KLOC | 5/KLOC |
| **속도** | 1줄/시간 | 5줄/시간 |
| **이해** | 어려움 | 쉬움 |
| **변경** | 위험 | 안전 |

### 모범 사례

1. **작게**: 커밋 단위
2. **테스트**: 회귀 방지
3. **이름**: 명확하게
4. **도구**: 자동화 활용

### 미래 전망

1. **AI**: Code refactoring
2. **Real-time**: IDE suggestions
3. **Metrics**: Technical debt
4. **Self-healing**: Auto-fix

### ※ 참고 표준/가이드
- **Fowler**: Refactoring (1999)
- **Clean Code**: Robert C. Martin
- **Working Effectively**: Kent Beck

---

## 📌 관련 개념 맵

- [디자인 패턴](./14_design_patterns/40_design_patterns.md) - 적용
- [코드 리뷰](./15_code_review/41_code_review.md) - 검토
- [TDD](./24_tdd/94_tdd.md) - Red-Green-Refactor
