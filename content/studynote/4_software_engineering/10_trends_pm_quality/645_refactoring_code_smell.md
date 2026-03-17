+++
title = "645. 리팩토링 악취(Code Smell) 제거"
date = "2026-03-15"
weight = 645
[extra]
categories = ["Software Engineering"]
tags = ["Refactoring", "Code Smell", "Clean Code", "Maintainability", "Software Quality"]
+++

# 645. 리팩토링 악취(Code Smell) 제거

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어의 **외부 동작(External Behavior)**은 유지하면서, 내부 구조(Internal Structure)를 개선하여 가독성을 높이고 유지보수 비용을 줄이는 **엔지니어링 활동**이다.
> 2. **진단**: 단순한 오류가 아닌, **기술 부채(Technical Debt)**를 유발하는 잠재적 위험 요소인 **코드 스멜(Code Smell)**을 정의하고 식별하는 것이 핵심 전략이다.
> 3. **실무**: **테스트 주도 개발(TDD: Test Driven Development)** 및 **CI/CD(Continuous Integration/Continuous Deployment)** 파이프라인과 결합하여, 안전하게 소프트웨어의 부패(Software Rot)를 방지하고 시스템 수명을 연장한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 리팩토링(Refactoring)의 기술적 정의
리팩토링은 마틴 파울러(Martin Fowler)가 정의한 바와 같이 "소프트웨어의 겉으로 드러나는 기능은 바꾸지 않으면서, 내부 구조를 재구성하여 더 이해하기 쉽고 수정하기 쉽게 만드는 활동"입니다. 여기서 핵심은 **행동의 보존(Behavior Preservation)**입니다. 기능적 요구사항(Functional Requirement)을 변경하지 않고, 비기능적 요구사항(Non-functional Requirement)인 가독성, 유지보수성, 확장성을 획기적으로 개선하는 엔지니어링 기법입니다.

### 2. 등장 배경: 소프트웨어 엔트로피(Software Entropy) 증가
소프트웨어는 개발될수록 복잡도가 증가하는 '엔트로피 법칙'을 따릅니다.
- **① 전통적 개발의 한계**: 기능 추가 시 일정 압박으로 인해 임시방편(Patch) 코드가 추가되며 스파게티 코드(Spaghetti Code)화됨.
- **② 패러다임 변화**: 코드는 쓰는 시간보다 읽고 수정하는 시간이 압도적으로 많음(유지보수 비용이 전체 비용의 80% 이상 차지)을 인식.
- **③ 현대적 요구**: 애자일(Agile) 환경에서의 지속적인 변경을 감당하기 위해 유연한 아키텍처의 필요성 대두.

### 3. 코드 스멜(Code Smell)의 정의
**코드 스멜**은 시스템의 심각한 결함(Bug)은 아니지만, 깊은 냄새를 풍겨 개발자들이 우려하게 만드는 코드의 특성을 의미합니다. 이는 시스템 내부의 **기술 부채**가 임계점에 다다랐음을 시 signaling하는 지표입니다.

### 💡 비유: 방 청소와 가구 재배치

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [Refactoring 비유]                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Current State - Before]                                                   │
│  살고 있는 집(코드)이 점점 지저분해짐.                                        │
│  - 침대 밑에 쓰레기가 묻혀 있고(중복 코드),                                   │
│  - 가구 배치가 동선을 막아 방을 돌아다니기 불편함(복잡한 제어문).               │
│  → 당장 집이 무너지는 건 아니지만(런타임 에러 없음), 살기 불편하고 쥐가           │
│    나올 것 같은 냄새가 남(Code Smell).                                       │
│                                                                             │
│  [Refactoring Process]                                                      │
│  1. 쓰레기를 치우고(Dead Code 제거),                                         │
│  2. 자주 쓰는 물건은 손에 닿는 곳으로 둔 뒤(Accessibility 개선),              │
│  3. 가구 배치를 효율적으로 재배치함(구조 재설계).                              │
│                                                                             │
│  [Result - After]                                                          │
│  집의 크기(기능)는 그대로지만, 훨씬 쾌적하고 다음 청소가 쉬워짐.                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유
리팩토링은 **"집을 새로 짓는 것이 아니라, 쓰레기를 치우고 가구 배치를 바꿔서 주거 공간의 효율성을 극대화하는 '인테리어 리모델링' 과정"**과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 스멜 분류 (Taxonomy)
리팩토링 대상인 코드 스멜은 크게 구조, 데이터 혹은 API 수준에서 발생합니다. 이를 시스템적으로 분류하면 다음과 같습니다.

| 구분 | 요소명 (Component Name) | 내부 동작 (Internal Behavior) | 대응 리팩토링 기법 (Refactoring Technique) |
|:---:|:---|:---|:---|
| **구조적 스멜** | 중복 코드 (Duplicated Code) | 동일 로직이 복사/붙여넣기 됨 | Extract Method (메서드 추출) |
| | 긴 메서드 (Long Method) | 메서드의 Cyclomatic Complexity가 높음 | Decompose Conditional |
| | 기능 욕심 (Feature Envy) | 다른 클래스의 내부 데이터를 과도히 탐색 | Move Method |
| **데이터 스멜** | 거대 클래스 (Large Class) | 단일 클래스가 너무 많은 책임(Life & Death) | Extract Class |
| | 기본형 집착 (Primitive Obsession) | 기본형 변수만 사용하여 정보 누락 | Introduce Parameter Object |
| | 긴 파라미터 (Long Parameter) | 파라미터 리스트가 5개 이상 | Parameter Object |
| **API 스멜** | 산탄대수 수정 (Shotgun Surgery) | 변경 시 여러 파일을 동시에 수정해야 함 | Move Field, Inline Class |

### 2. 리팩토링 수행 절차 및 메커니즘 (Mechanism)
리팩토링은 위험한 작업이므로, 엄격한 **회귀 테스트(Regression Test)** 안전장치 하에 진행되어야 합니다.

```text
   [Step 1]                    [Step 2]                    [Step 3]
   ┌───────────┐              ┌───────────┐              ┌───────────┐
   │  Build    │              │   Detec   │              │   Apply   │
   │ SafetyNet │─────────────▶│  Target   │─────────────▶│  Changes  │
   │           │              │           │              │           │
   └───────────┘              └───────────┘              └───────────┘
        │                            │                            │
        │                            │                            ▼
        │                            │                     ┌─────────────┐
        │                            │                     │ Small Step  │
        ▼                            ▼                     │  Refactor   │
   ┌───────────────┐        ┌─────────────┐               └──────┬──────┘
   │ Unit Tests    │        │ Code Smell  │                      │
   │ (Red/Green)   │        │ Analysis    │                      ▼
   └───────────────┘        └─────────────┘               ┌─────────────┐
   (테스트가 통과된            (정적 분석 도구,               │  Compile    │
    상태임을 보장)             Code Review)                 │  & Test     │
                                                          └──────┬──────┘
                                                                 │
                           [Step 4: Verification]               │
                                                                 ▼
                                                           ┌─────────────┐
                                                           │ Regression  │
                                                           │   Check     │
                                                           └──────┬──────┘
                                                                  │
                                                         (Fail? ──▶ Rollback)
                                                                  │
                                                        (Pass ──▶ Commit)
```

**해설**:
1.  **Build SafetyNet (단위 테스트 확인)**: 리팩토링의 전제 조건은 견고한 테스트 스위트(Test Suite)입니다. "테스트가 없는 리팩토링은 그저 코드 수정일 뿐이다."
2.  **Detec Target (스멀 탐지)**: IDE(Integrated Development Environment)의 경고, SonarQube 등의 정적 분석 툴, 혹은 동료 개발자의 Code Review를 통해 불필요한 복잡도를 식별합니다.
3.  **Apply Changes (변경 적용)**: 시스템이 무너지지 않도록 아주 작은 단계(Micro-step)로 코드를 수정합니다. 예: 변수명 변경, 메서드 추출 등.
4.  **Verification (검증)**: 변경 후 즉시 테스트를 수행하여 회귀 오류(Regression Error)가 없는지 확인합니다. 실패 시 즉시 되돌립니다(Rollback).

### 3. 심층 동작 원리: 코드 스멜의 제거 프로세스
**롱 메서드(Long Method)** 스멜을 제거하는 과정을 통해 내부를 분석해 봅시다. 긴 메서드는 이해하기 어렵고 재사용이 불가능합니다.

**Before (Code Snippet):**
```java
// 💡 Anti-Pattern
public void printOwing() {
    double outstanding = 0.0;
    
    // 배너 출력
    System.out.println("*************************");
    System.out.println("**** Customer Owes ******");
    System.out.println("*************************");

    // 외상 합계 계산 (중복 로직)
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }

    // 세부 사항 출력
    System.out.println("name: " + _name);
    System.out.println("amount: " + outstanding);
}
```

**After (Refactoring via Extract Method):**
```java
// ✅ Refactored Pattern
public void printOwing() {
    double outstanding = getOutstanding(); // 1. 로직 분리
    printBanner();                         // 2. 시각 요소 분리
    printDetails(outstanding);             // 3. 데이터 출력 분리
}

private double getOutstanding() {
    double result = 0.0;
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        result += each.getAmount();
    }
    return result;
}
```

**변화의 핵심**: 500줄짜리 메서드를 여러 개의 **5~10줄짜리 의도(Intent)를 가진 메서드**로 쪼개면, 코드의 **추상화 레벨(Abstraction Level)**이 일치되어 가독성이 극대화됩니다.

### 📢 섹션 요약 비유
이 과정은 **"복잡한 실험실 장비를 하나의 거대한 기계로 만드는 대신, 목적별로 분리된 모듈(센서, 증폭기, 디스플레이)로 조립하여 문제가 생겼을 때 해당 모듈만 교체할 수 있도록 만드는 것"**과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 리팩토링 vs 기능 추가 vs 성능 최적화 (Optimization)

| 비교 항목 (Criteria) | 리팩토링 (Refactoring) | 기능 추가 (Feature Addition) | 성능 최적화 (Performance Tuning) |
|:---|:---|:---|:---|
| **주 목적 (Goal)** | 구조 개선 (Structure) | 사용자 가치 제공 (Value) | 속도/자원 효율 (Speed/Resource) |
| **외부 관찰 (Observability)** | 변화 없음 (No Change) | 변화 있음 (Visible) | 변화 있음 (Faster/Less Memory) |
| **코드 범위 (Scope)** | 기존 코드 변경 | 신규 코드 추가 | 기존 코드 수정 (Algorithm chg) |
| **위험도 (Risk)** | 중간 (테스트 의존적) | 높음 (새 버그 유발) | 높음 (Trade-off 발생) |

### 2. 융합 관점: TDD 및 CI/CD와의 시너지
리팩토링은 **TDD(Test Driven Development)** 사이클의 핵심 구성 요소입니다.
- **Red-Green-Refactor**: 실패하는 테스트를 작성하고(Red), 테스트를 통과하게 만든 뒤(Green), 그때 발생한 코드 스멜을 제거하기 위해 리팩토링(Refactor)을 수행합니다.
- **CI/CD 파이프라인**: 자동화된 빌드 및 테스트 환경이 구축되어 있지 않다면, 리팩토링은 "무모한 행위"가 됩니다. **CD(Continuous Deployment)** 과정에서의 정적 분석(SonarQube)은 리팩토링이 필요한 지점(Hotspot)을 자동으로 산출해 줍니다.

### 3. 정량적 의사결정 메트릭 (Metrics)
리팩토링 여부를 판단하기 위해 **코드 복잡도(Code Complexity)** 지표를 활용합니다.
- **CC(Cyclomatic Complexity) = E - N + 2P** (E: Edge, N: Node, P: Connected Components)
    - 일반적으로 CC > 10 인 경우 리팩토링 대상으로 간주.
- **LCOM(Lack of Cohesion of Methods)**: 클래스 내 메서드 간의 응집도가 낮을수록 리팩토링 필요.

### 📢 섹션 요약 비유
리팩토링은 **"자동차의 엔진을 교체(성능 최적화)하거나 터보를 장착(기능 추가)하는 것이 아니라, 엔진 룸 내의 배선을 정리하고 오일을 교체하여 엔진이 더 오래, 그리고 원활하게 돌아가게 하는 '오버홀(Overhaul)' 과정"**과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 제어 흐름 복잡도 해소 (Resolve Complexity)
- **상황**: 보험료 계산 시스템. 고객 등급(골드, 실버, 브론즈), 나이, 가입 기간에 따라 10단계 이상의 `if-else-if`가 중첩된 `calculatePremium()` 메서드가 존재함. 수정 시 Side Effect 발생 빈도 높음.
- **의사결정 프로세스**:
    1.  **진단**: McCabe의 복잡도 지수가 45를 초과함 (기준치는 보통 10~15).
    2.  **전략 수립**: **Replace Conditional with Polymorphism** 기법 적용. 각 등급별 로직을 독립된 클래스(`GoldRateCalculator`, `SilverRateCalculator`)로 분리.
    3.  **실행**: 추상 클래스 `RateCalculator`를 상속받아 구체적 전략을 구현.
- **결과**: 신규 등급 추가 시 기존 코드를 수정할 필요 없이 새로운 클래스만 추가하면 됨(OCP, Open/Closed Principle 준수). 단