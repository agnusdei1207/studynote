+++
title = "735. 디자인 바이 컨트랙트 불변 조건"
date = "2026-03-15"
weight = 735
[extra]
categories = ["Software Engineering"]
tags = ["Programming", "Design by Contract", "DbC", "Invariant", "Software Correctness", "Formal Methods"]
+++

# 735. 디자인 바이 컨트랙트 불변 조건

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 버트런드 메이어(Bertrand Meyer)가 제안한 **디자인 바이 컨트랙트 (DbC, Design by Contract)**는 소프트웨어 모듈 간의 인터페이스를 법적 계약관계로 정의하여, 호출자(Client)의 의무와 공급자(Supplier)의 보장을 명확히 하는 소프트웨어 정합성(Correctness) 보장 패러다임이다.
> 2. **구조**: **불변 조건 (Invariant, 불변식)**을 중심으로, 메서드 진입 전의 **선행 조건 (Pre-condition)**과 종료 후의 **후행 조건 (Post-condition)**을 결합하여 객체의 상태 무결성을 수학적으로 명세하고 런타임에 검증한다.
> 3. **가치**: 모호한 주석(Comment) 대신 실행 가능한 명세(Specification)를 통해 시스템의 신뢰성을 획기적으로 높이며, 장애 발생 시 책임 소재(Blame)를 기계적으로 판단하여 디버깅 비용을 최소화한다.

---

### Ⅰ. 개요 (Context & Background)

소프트웨어 공학의 오랜 난제 중 하나는 "함께 동작하는 두 모듈 중 어느 쪽에서 버그가 발생했는가"입니다. **예방적 프로그래밍 (Defensive Programming)**은 모든 것을 의심하여 코드를 복잡하게 만들지만, **디자인 바이 컨트랙트 (DbC)**는 "계약"이라는 명확한 기준을 세워 각 모듈이 자신의 책임 범위 내에서만 완벽하게 동작하도록 강제합니다. 이는 Eiffel (Eiffel) 언어에서 시작되어 현재는 **JML (Java Modeling Language)**, **Code Contracts (.NET)** 등 다양한 형태로 확장되었습니다.

#### 1. 개념 정의 및 철학
DbC는 소프트웨어 요소(클래스, 메서드) 간의 관계를 **고객 (Client, 호출자)**과 **공급자 (Supplier, 제공자)**의 계약으로 모델링합니다.
- **의무 (Obligation)**: 클라이언트가 반드시 지켜야 할 선행 조건.
- **보장 (Benefit)**: 공급자가 반드시 제공해야 할 후행 조건.
- **유지 (Maintain)**: 객체의 생명주기 전체에 걸쳐 유지되어야 할 불변 조건.

#### 2. 등장 배경: 신뢰성의 위기와 형식적 방법론
절차적 프로그래밍에서 데이터와 로직의 분리로 인해 발생하는 **데이터 무결성 (Data Integrity)** 침해 문제를 해결하기 위해 제안되었습니다. 단순한 주석(Comment)은 개발자가 실수로 위반하기 쉽고, 컴파일러가 이를 검증할 수 없다는 한계가 있었습니다. DbC는 이러한 명세를 코드 안에 **단언 (Assertion)** 형태로 내장하여, 개발 단계와 테스트 단계에서 자동으로 검증되도록 설계되었습니다.

```text
[ Philosophy of DbC ]
┌─────────────────────────────────────────────────────────────────┐
│  Client (Caller)          Supplier (Callee / Class)             │
│     ┌──────┐                    ┌──────────────┐                │
│     │User  │                    │   Service    │                │
│     └──┬───┘                    └──────┬───────┘                │
│        │                               │                        │
│        │  ① Request + Data (Obligation)│                        │
│        ├──────────────────────────────▶│                        │
│        │    (Pre-condition Must be True)                       │
│        │                               │                        │
│        │                     ┌─────────▼─────────┐              │
│        │                     │   Execute Logic   │              │
│        │                     │  (Invariant Valid)│              │
│        │                     └─────────┬─────────┘              │
│        │                               │                        │
│        │  ③ Result + Guarantee (Benefit)│                       │
│        │◀──────────────────────────────┤                        │
│        │    (Post-condition Guaranteed)│                        │
│        │                               │                        │
│  [Rule]: If ① is valid, ③ must be valid.                      │
│  If not, the Supplier is in breach of contract.                │
└─────────────────────────────────────────────────────────────────┘
```

#### 📢 섹션 요약 비유
> 디자인 바이 컨트랙트는 **'무기 입장 계약서'**와 같습니다. 
> "상대방이 먼저 공격하지 않는다면(선행 조건), 나도 절대 공격하지 않겠다(후행 조건)"는 조약을 체결함으로써, 어느 한쪽이 계약을 어겼을 때 전쟁(시스템 오류)의 책임이 누구에게 있는지 명확히 하는 국제법 원칙과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

DbC를 구성하는 3대 핵심 요소는 **Assertion (단언)**을 통해 코드 레벨에서 구현됩니다.

#### 1. 구성 요소 상세 분석 (Table)

| 구성 요소 | 영문 명칭 | 정의 (Definition) | 책임 소재 | 실패 시 예외 (Exception) |
|:---:|:---|:---|:---:|:---:|
| **선행 조건** | **Pre-condition** | 메서드 진입 전 입력값(Input)과 시스템 상태가 만족해야 할 조건. `require` 블록에 정의. | **Client (호출자)** | `ArgumentError`, `PreconditionViolation` (사용자 요청 잘못) |
| **후행 조건** | **Post-condition** | 메서드 종료 후 반환값(Return) 및 시스템 상태가 보장해야 할 조건. `ensure` 블록에 정의. | **Supplier (공급자)** | `AssertionError`, `PostconditionViolation` (내부 로직 버그) |
| **불변 조건** | **Invariant (불변식)** | 클래스의 인스턴스 생성 직후부터 소멸 시까지 모든 퍼블릭 메서드 실행 전후에 **항상 참(True)**이어야 하는 논리식. | **Class 자체** | `ClassInvariantViolation` (객체 상태 오염) |

#### 2. 실행 메커니즘과 상태 전이 (ASCII)

DbC가 런타임에 어떻게 검증되는지 시각화한 다이어그램입니다. **Invariant**는 모든 퍼블릭 메서드의 사이클을 감싸는 보호막 역할을 합니다.

```text
   [ Lifecycle of a DbC Method Call ]

   Object Lifecycle (Invariant ──────────────────────────────────── TRUE)
        │
        │  [ 1. Object Creation ]
        │    ▼
        │  Constructor (Invariant check first)
        │    │
   ─────┼───────────────────────────────────────────────────────────────
        │
        │  [ 2. Method Invocation ]
        │    ▼
        │  ┌──────────────────────────────────────────────────┐
        │  │  Check Pre-condition (require)                   │
        │  │  "Is input valid?"                               │
        │  └───────┬──────────────────────────────────────────┘
        │          │
        │    Valid │ Invalid
        │          ▼
        │    ┌─────────────────────┐
        │    │  THROW EXCEPTION    │ (Client's Fault)
        │    │  (Caller Error)     │
        │    └─────────────────────┘
        │
        │  (Proceed)   ┌──────────────────────────────────────────────────┐
        │              │  [ Execution Body ]                              │
        │              │  - Change Internal State                         │
        │              │  - Perform Business Logic                        │
        │              │  (Invariant may be temporarily broken here)      │
        │              └──────────────────────┬───────────────────────────┘
        │                                     │
        │                                     ▼
        │  ┌──────────────────────────────────────────────────┐
        │  │  Check Post-condition (ensure)                   │
        │  │  "Is output/result valid?"                       │
        │  └───────┬──────────────────────────────────────────┘
        │          │
        │   Pass   │ Fail
        │          ▼
        │    ┌─────────────────────┐
        │    │  THROW EXCEPTION    │ (Supplier's Fault)
        │    │  (Callee Bug)       │
        │    └─────────────────────┘
        │
        │  (Success)  ┌──────────────────────────────────────────────────┐
        │              │  Check Invariant (again)                        │
        │              │  "Is object stable?"                            │
        │              └──────────────────────┬───────────────────────────┘
        │                                 │
        └─────────────────────────────────┘ (Return to Caller)
```

#### 3. 핵심 알고리즘: 불변 조건 (Invariant)의 내부 동작
불변 조건은 단순히 값이 변하지 않음(Immutable)을 의미하는 것이 아닙니다. "변수 A는 변수 B보다 항상 커야 한다"와 같이 **상태 간의 논리적 관계**를 정의합니다.
- **예시 (은행 계좌)**: `balance >= 0` (잔고는 음수일 수 없다).
- **구현 원리**: 객체의 상태를 변경하는 모든 메서드(Mutator)의 진입과 퇴출 시점에 자동으로 삽입되는 가상의 코드입니다.

#### 4. 코드 레벨 구현 예시 (Pseudo-Code)

```python
# Pseudocode illustrating DbC elements

class BankAccount:
    def __init__(self, initial_balance):
        # Post-condition of Constructor
        assert initial_balance >= 0, "Initial balance cannot be negative"
        self._balance = initial_balance
        # Invariant check (Implicitly done)
        self._check_invariant()

    # Invariant Definition
    def _check_invariant(self):
        assert self._balance >= 0, "Invariant Violated: Balance is negative"

    def withdraw(self, amount):
        # --- Pre-condition (Client's Responsibility) ---
        assert amount > 0, "Pre-condition Failed: Amount must be positive"
        assert self._balance >= amount, "Pre-condition Failed: Insufficient funds"

        # --- Logic Execution ---
        self._balance -= amount

        # --- Post-condition (Supplier's Responsibility) ---
        assert self._balance >= 0, "Post-condition Failed: Balance corrupted"
        
        # --- Invariant Re-check ---
        self._check_invariant()
```

#### 📢 섹션 요약 비유
> 불변 조건은 **'블록 쌓기 게임의 규칙'**과 같습니다. 블록을 옮기는 동안(Method 실행 중)에는 일시적으로 높은 곳에 블록이 떠 있을 수 있지만, 게임이 끝난 시점(메서드 종료 시)에는 모든 블록이 반드시 바닥에 안정적으로 놓여 있어야(Invariant = True) 합니다. 만약 바닥에 안 떨어진 채로 게임이 끝나면 타워가 무너지는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

DbC는 단순한 코딩 스타일이 아니라 소프트웨어의 품질을 보장하는 강력한 아키텍처 패턴으로, 다른 기술들과의 시너지와 비교 분석이 필요합니다.

#### 1. 심층 기술 비교: 방어적 프로그래밍 vs DbC

| 비교 항목 | **방어적 프로그래밍 (Defensive Programming)** | **디자인 바이 컨트랙트 (DbC)** |
|:---|:---|:---|
| **기본 철학** | "모든 입력은 의심한다" (Trust No One) | "계약된 약속은 신뢰한다" (Trust Contract) |
| **에러 처리** | 예외 처리(Exception Handling), 로깅, 기본값 반환 | **Assertion (단언)** 실패 시 즉시 프로그램 중단 (Fail-Fast) |
| **코드 복잡도** | 로직 내부에 `if error != null` 등의 검사 코드가 증가하여 가독성 하락 | 검사 코드가 명세(Pre/Post)로 분리되어 로직이 간결해짐 |
| **성능 오버헤드** | 상대적으로 낮음 (실무에서 항상 켬) | assertion 체크에 따른 오버헤드 존재 (보통 개발/테스트 환경에서만 활성화) |
| **결함 원인 규명** | 에러가 삼켜지거나(Eating errors), 잘못된 곳에서 터질 수 있음 | 계약 위반 지점에서 정확히 "누구의 잘못"인지 판명 |

#### 2. SOLID 원칙과의 융합: LSP (리스코프 치환 원칙)

DbC는 객체지향의 핵심 원칙인 **LSP (Liskov Substitution Principle, 리스코프 치환 원칙)**와 깊은 연관이 있습니다.
- **LSP 정의**: 상위 타입의 객체를 하위 타입의 객체로 치환해도 프로그램의 정합성이 깨지지 않아야 한다.
- **DbC와의 관계**:
    - 하위 클래스는 상위 클래스의 **선행 조건을 강화할 수 없다**. (같은 일을 하는데 더 까다로운 조건을 요구하면 치환 불가)
    - 하위 클래스는 상위 클래스의 **후행 조건을 약화할 수 없다**. (상위가 보장하는 기능을 하위에서 안 해주면 치환 불가)

```text
[ LSP & DbC Relationship ]
      Super Type Contract
  ┌─────────────────────────────┐
  │ Pre:  x > 0                 │
  │ Post: result > 0            │
  └─────────────────────────────┘
           ▲
           │ (Inheritance)
           │
      Sub Type Contract
  ┌─────────────────────────────┐
  │ Pre: x > 10  (❌ Violation!) │ ──▶ Client passing x=5 expects it to work
  │ Post: result > 10 (❌ OK)    │      based on Super, but Sub fails.
  └─────────────────────────────┘
```

#### 3. 정형 검증 (Formal Verification)과의 연계
DbC는 **정형 검증 (Formal Verification)**으로 가는 중요한 디딤돌입니다. 단순히 런타임에 에러를 잡는 것을 넘어, **정적 분석 도구 (Static Analyzer)**가 코드를 실행하지 않고도 수학적으로 증명(Proof)할 수 있는 명세를 제공합니다.

#### 📢 섹션 요약 비유
> 방어적 프로그래밍은 **'감옥'**을 짓는 것과 같아서 죄수(입력값) 하나하나를 수갑을 채우고 감시하지만, DbC는 **'고속도로 통행료 징수소'**와 같습니다. 계약된 차량(규칙을 지킨 데이터)은 멈추지 않고 통과시켜 속도(성능)를 높이고, 계약을 어긴 차량만 �