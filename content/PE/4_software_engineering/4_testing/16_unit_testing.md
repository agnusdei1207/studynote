+++
title = "16. 단위 테스트 (Unit Testing)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Unit-Testing", "TDD", "Test-Double", "Mock", "Stub", "JUnit", "Pytest"]
draft = false
+++

# 단위 테스트 (Unit Testing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단위 테스트는 **"코드의 **최소 단위(함수, 메서드, 클래스)**를 **격리된 환경**에서 **검증하는 테스트"**로, **Mock, Stub, Spy** 같은 **Test Double**을 활용하여 **외부 의존성을 제거**하고 **단일 책임**을 검증한다.
> 2. **가치**: **버그 조기 발견(Early Bug Detection)**으로 **비용 감소**, **리팩토링 안정성(Refactoring Safety)** 보장, **Live Documentation(실시간 문서)** 역할, **회귀 테스트(Regression Test)** 자동화를 제공한다.
> 3. **융합**: **TDD(Test-Driven Development)**는 **Red-Green-Refactor** 사이클로 **테스트 주도 개발**을 하며, **JUnit(Java)**, **pytest(Python)**, **Jest(JavaScript)**, **Go testing**이 대표적인 **프레임워크**이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
단위 테스트는 **"코드의 가장 작은 단위를 테스트하는 방법"**이다.

**단위 테스트의 특징**:
- **격리성**: 다른 코드와 독립
- **신속성**: 빠른 실행 (ms 단위)
- **반복성**: 환경无关 同 결과

### 💡 비유
단위 테스트는 **"부품 검사"**와 같다.
- **부품**: 함수/클래스
- **검사**: 테스트
- **조립 전**: 통합 전

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         단위 테스트의 발전                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

초기 개발:
    • 수동 테스트
    • 디버깅으로 검증
         ↓
단위 테스트 등장 (1970년대):
    • Smalltalk (SUnit)
    • JUnit (1999, Kent Beck)
    • xUnit 계열 보급
         ↓
TDD 등장:
    • Test First
    • Red-Green-Refactor
    • Agile과 결합
         ↓
현대:
    • TDD, BDD
    • CI/CD 통합
    • Mutation Testing
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 단위 테스트 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         AAA 패턴 (Arrange-Act-Assert)                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  [Given (Arrange)]                                                                     │
    │  • 테스트 환경 설정                                                                      │
    │  │  • 입력 데이터 준비                                                                   │
    │  │  • Mock 객체 설정                                                                     │
    │                                                                                         │
    │  [When (Act)]                                                                            │
    │  • 테스트 대상 실행                                                                       │
    │  │  • 함수/메서드 호출                                                                   │
    │                                                                                         │
    │  [Then (Assert)]                                                                         │
    │  • 결과 검증                                                                             │
    │  │  • 기대값 vs 실제값                                                                    │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [예시: Calculator 테스트]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  @Test                                                                                  │
    │  void testAddition() {                                                                  │
    │      // Given (Arrange)                                                                 │
    │      Calculator calc = new Calculator();                                                │
    │      int a = 10, b = 20;                                                                │
    │                                                                                         │
    │      // When (Act)                                                                       │
    │      int result = calc.add(a, b);                                                       │
    │                                                                                         │
    │      // Then (Assert)                                                                    │
    │      assertEquals(30, result);  // 기대값, 실제값                                         │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Test Double

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Test Double 종류                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Dummy]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 전달만 하고 실제로 사용 안 함                                                           │
    │                                                                                         │
    │  예:                                                                                    │
    │  class DummyDatabase implements Database {                                              │
    │      void connect() {}  // 빈 구현                                                      │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Stub]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 미리 정의된 값 반환                                                                   │
    │                                                                                         │
    │  예:                                                                                    │
    │  class StubDatabase implements Database {                                               │
    │      User getUser(int id) {                                                             │
    │          return new User(1, "Test User");  // 항상 같은 값                             │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Spy]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 호출 정보 기록 (호출 여부, 횟수, 인자)                                                   │
    │                                                                                         │
    │  예:                                                                                    │
    │  class SpyDatabase implements Database {                                                 │
    │      int callCount = 0;                                                                 │
    │      User getUser(int id) {                                                             │
    │          callCount++;                                                                  │
    │          return new User(id, "User" + id);                                              │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Mock]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 기대 행동(Expectation) 설정 및 검증                                                     │
    │                                                                                         │
    │  예 (Mockito):                                                                          │
    │  Database mockDB = mock(Database.class);                                                 │
    │  when(mockDB.getUser(1)).thenReturn(new User(1, "Alice"));                               │
    │  verify(mockDB).getUser(1);  // 호출 검증                                                │
    │                                                                                         │
    │  예 (unittest.mock):                                                                    │
    │  @patch.object('module.Database')                                                         │
    │  def test_get_user(mock_db):                                                            │
    │      mock_db.return_value = User(1, "Alice")                                             │
    │      # test...                                                                          │
    │      mock_db.assert_called_once_with(1)                                                 │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Fake]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 실제 동작하는 가짜 구현 (In-Memory)                                                    │
    │                                                                                         │
    │  예:                                                                                    │
    │  class InMemoryDatabase implements Database {                                            │
    │      Map<Integer, User> users = new HashMap<>();                                       │
    │      User getUser(int id) { return users.get(id); }                                      │
    │      void save(User user) { users.put(user.id, user); }                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### TDD (Test-Driven Development)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         TDD 사이클: Red-Green-Refactor                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌─────────┐     ┌─────────┐     ┌───────────┐     ┌─────────┐                       │
    │  │   Red   │ ───→ │  Green  │ ───→ │ Refactor  │ ───→ │   Red   │ ...              │
    │  │ 실패   │     │  통과  │     │   재구성  │     │  다음  │                       │
    │  └─────────┘     └─────────┘     └───────────┘     └─────────┘                       │
    │       │               │               │               │                              │
    │       ▼               ▼               ▼               ▼                              │
    │  ┌─────────┐     ┌─────────┐     ┌───────────┐     ┌─────────┐                       │
    │  │테스트작성│     │ 최소구현│     │  코드   │     │새테스트│                       │
    │  │ (실패) │     │ (통과) │     │ 개선  │     │ 추가  │                       │
    │  └─────────┘     └─────────┘     └───────────┘     └─────────┘                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [TDD 예시]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // 1. Red: 실패하는 테스트 작성                                                         │
    │  @Test                                                                                  │
    │  void testAdd() {                                                                      │
    │      Calculator calc = new Calculator();                                                │
    │      assertEquals(5, calc.add(2, 3));  // 구현 안 함 → 실패                            │
    │  }                                                                                      │
    │                                                                                         │
    │  // 2. Green: 최소 구현으로 통과                                                         │
    │  class Calculator {                                                                     │
    │      int add(int a, int b) { return 5; }  // 하드코딩으로 통과                            │
    │  }                                                                                      │
    │                                                                                         │
    │  // 3. Refactor: 일반적 구현으로 개선                                                   │
    │  class Calculator {                                                                     │
    │      int add(int a, int b) { return a + b; }  // 올바른 구현                             │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 테스트 피라미드

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         테스트 피라미드                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │                                       E2E Tests (10%)                                 │
    │                                     ────────────────────────                              │
    │                                   Integration Tests (20%)                             │
    │                                 ──────────────────────────────                           │
    │                              Unit Tests (70%)                                        │
    │                            ─────────────────────────────────────────                    │
    │                                                                                         │
    │  • 단위 테스트: 빠름, 많음, 저렴                                                         │
    │  • 통합 테스트: 느림, 적음, 비쌈                                                           │
    │  • E2E 테스트: 가장 느림, 가장 적음, 가장 비쌈                                                │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 단위 테스트 프레임워크

| 언어 | 프레임워크 | 특징 |
|------|----------|------|
| **Java** | JUnit, TestNG | Annotation 기반 |
| **Python** | pytest, unittest | fixture, parametrize |
| **JavaScript** | Jest, Mocha | describe/it BDD |
| **Go** | testing | builtin, table-driven |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 단위 테스트 도입
**상황**: 레거시 코드 테스트
**판단**:

```python
# pytest 예시

import pytest
from unittest.mock import Mock, patch

# 테스트 대상
class UserService:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        return self.db.find_user(user_id)

# Test Stub
class StubDatabase:
    def find_user(self, user_id):
        return User(id=user_id, name=f"User{user_id}")

# Test
def test_get_user():
    stub_db = StubDatabase()
    service = UserService(stub_db)

    user = service.get_user(1)

    assert user.id == 1
    assert user.name == "User1"

# Mock 사용
@patch('module.Database')
def test_get_user_with_mock(mock_db):
    mock_db.find_user.return_value = User(id=1, name="Alice")

    service = UserService(mock_db)
    user = service.get_user(1)

    mock_db.find_user.assert_called_once_with(1)
    assert user.name == "Alice"

# Parametrize (매개변수화)
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected
```

---

## Ⅴ. 기대효과 및 결론

### 단위 테스트 기대 효과

| 효과 | 단위 테스트 없을 시 | 단위 테스트 있을 시 |
|------|-----------------|------------------|
| **버그 발견** | 늦음 (운영 중) | 빠름 (개발 중) |
| **리팩토링** | 위험 | 안전 |
| **문서화** | 별도 필요 | 코드가 문서 |
| **CI/CD** | 어려움 | 자동화 |

### 미래 전망

1. **AI 테스트 생성**: GPT 기반
2. **Mutation Testing**: 테스트 품질 측정
3. **Property-Based Testing**: Hypothesis, QuickCheck

### ※ 참고 표준/가이드
- **Kent Beck**: TDD by Example
- **Martin Fowler**: Unit Testing
- **JUnit**: Best Practices

---

## 📌 관련 개념 맵

- [TDD](../3_agile/17_tdd.md) - 테스트 주도 개발
- [통합 테스트](./17_integration_testing.md) - 통합 테스트
- [CI/CD](./19_ci_cd.md) - 지속 통합
- [테스트 전략](./20_test_strategy.md) - 전체 전략
