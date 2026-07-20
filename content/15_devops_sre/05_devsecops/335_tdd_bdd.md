---
title: "TDD BDD Acceptance Testing Mock Stub Spy Test Pyramid Red Green Refactor"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 335
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TDD (Test-Driven Development, 테스트 주도 개발)는 Red-Green-Refactor 사이클로 코드를 설계하는 방법론이다. BDD (Behavior-Driven Development, 행위 주도 개발)는 TDD를 확장해 비즈니스 언어(Given/When/Then)로 테스트를 기술하고 이해관계자와 소통한다.
> 2. **설계 효과**: TDD를 실천하면 테스트 가능한 코드가 자연스럽게 나온다. 테스트 불가능한 코드는 설계가 잘못된 신호다. SRP (Single Responsibility Principle), DI (Dependency Injection)이 자연스럽게 강제된다.
> 3. **판단 포인트**: 테스트 피라미드(Test Pyramid)에서 단위 테스트(Unit Test)가 기반이 되어야 한다. Mock/Stub/Spy로 외부 의존성을 격리해 단위 테스트를 빠르고 안정적으로 유지하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발에서 버그는 발견 시점이 늦을수록 수정 비용이 기하급수적으로 증가한다. IBM 연구에 따르면 프로덕션에서 발견된 버그는 설계 단계에서 발견된 것보다 100배 비용이 더 든다.

TDD는 이 문제를 코딩 시점에 해결한다. 테스트를 먼저 작성하면 구현 전에 요구사항을 명확히 정의하고, 구현 직후 테스트로 검증한다. 리그레션(Regression) 버그도 자동으로 잡힌다.

BDD는 TDD의 테스트가 너무 기술적이어서 비개발자가 이해하기 어렵다는 한계를 해결한다. Given/When/Then으로 시나리오를 기술하면 PO (Product Owner), QA, 개발자가 같은 문서를 공유한다.

> 📢 **섹션 요약 비유**: TDD는 집을 짓기 전에 설계도를 그리는 것이다. 집 완성 후 설계도를 그리면 이미 벽이 잘못된 위치에 있어도 고치기 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+--------------------------------------------------------+
|                TDD Red-Green-Refactor 사이클            |
+--------------------------------------------------------+
|                                                        |
|      +-------------------------------------------+    |
|      |              RED (실패)                   |    |
|      |  테스트 먼저 작성 -> 실행 -> 실패 확인    |    |
|      +---------------------+---------------------+    |
|                            |                          |
|                            v                          |
|      +-------------------------------------------+    |
|      |              GREEN (성공)                 |    |
|      |  테스트 통과하는 최소 코드 작성            |    |
|      +---------------------+---------------------+    |
|                            |                          |
|                            v                          |
|      +-------------------------------------------+    |
|      |           REFACTOR (개선)                 |    |
|      |  코드 품질 개선, 테스트는 계속 통과        |    |
|      +---------------------+---------------------+    |
|                            |                          |
|                            +--- 다음 테스트로 반복 -----+
+--------------------------------------------------------+

테스트 피라미드:
       ^
      /      /E2E\     (소수, 느림, 비용 높음)
    /-----   / 통합  \   (중간, 외부 시스템 필요)
  /--------- /  단위테스트 \ (다수, 빠름, 격리됨)
/-------------```

[[165_bdd_behavior_driven_development|BDD]] Given/When/Then 예시:

```gherkin
Feature: 사용자 로그인
  Scenario: 올바른 자격증명으로 로그인 성공
    Given 사용자 "alice"가 가입되어 있고
    When 사용자가 올바른 비밀번호로 로그인하면
    Then 대시보드 페이지로 이동한다
```

> 📢 **섹션 요약 비유**: [[165_bdd_behavior_driven_development|BDD]] 시나리오는 영화 대본이다. 개발자(감독), QA(스크립터), PO(작가)가 같은 대본으로 소통하고, 대본이 곧 자동화 테스트가 된다.

---

## Ⅲ. 비교 및 연결

### [[462_mock_test_double|Mock]] / [[460_stub_test_double|Stub]] / [[461_spy_test_double|Spy]] 비교

| 유형 | 목적 | 동작 |
|:---|:---|:---|
| [[462_mock_test_double|Mock]] | 호출 [[395_verification_process_review|검증]] | 어떻게 호출되었는지 기록하고 [[395_verification_process_review|검증]] |
| [[460_stub_test_double|Stub]] | 상태 제어 | 미리 정의된 값을 반환 |
| [[461_spy_test_double|Spy]] | 실제 동작 + 기록 | 실제 구현체를 감싸서 호출 기록 |
| [[463_fake_test_double|Fake]] | 단순 구현 대체 | 인메모리 DB 같은 경량 대체 구현 |

| 항목 | [[164_tdd_test_driven_development|TDD]] | [[165_bdd_behavior_driven_development|BDD]] |
|:---|:---|:---|
| 관점 | 개발자 관점 ([[397_unit_test|단위 테스트]]) | 비즈니스 관점 (시나리오 테스트) |
| 언어 | 프로그래밍 언어 | Gherkin (Given/When/Then) |
| 도구 | JUnit, pytest, Jest | Cucumber, Behave, SpecFlow |
| 소통 대상 | 개발팀 내부 | 개발팀 + PO + QA |

> �� **섹션 요약 비유**: Mock은 연습 상대 역할을 하는 스파링 파트너다. 실제 챔피언(외부 시스템) 없이도 연습(테스트)을 할 수 있게 해준다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 테스트 피라미드 비율 가이드

- **[[397_unit_test|단위 테스트]]**: 70% — 빠르고 저렴하며 피드백 즉각적
- **[[400_integration_testing|통합 테스트]]**: 20% — [[603_component_independent_deployment_unit|컴포넌트]] 간 상호작용 [[395_verification_process_review|검증]]
- **[[265_e2e_end_to_ui_selenium|E2E]] 테스트**: [[489_raid_10_hybrid|10]]% — 전체 플로우 [[395_verification_process_review|검증]], 느리고 취약함

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- **Ice Cream Cone**: [[397_unit_test|단위 테스트]] 없이 E2E만 많은 구조 — 느리고 불안정
- **[[462_mock_test_double|Mock]] 남용**: 모든 것을 Mock으로 대체 -> 실제 통합 문제를 놓침
- **테스트 없이 [[213_refactoring_cloud_native_rearchitecture|Refactor]]**: 회귀 버그 위험

### [[435_checklist_based_testing|체크리스트]]

1. [[397_unit_test|단위 테스트]] 커버리지가 80% 이상인가?
2. CI에서 [[397_unit_test|단위 테스트]]가 5분 내 완료되는가?
3. 외부 의존성(DB, [[014_api_posix|API]])이 [[462_mock_test_double|Mock]]/Stub으로 격리되어 오프라인에서도 실행 가능한가?
4. [[165_bdd_behavior_driven_development|BDD]] 시나리오가 PO/QA와 협의된 공식 [[165_acceptance_criteria_definition|인수 기준]]인가?

> 📢 **섹션 요약 비유**: 테스트 피라미드를 뒤집으면 Ice Cream Cone이 된다. 아이스크림 콘은 세우면 쓰러진다 — 불안정한 테스트 [[268_strategy_pattern|전략]]을 의미한다.

---

## Ⅴ. 기대효과 및 결론

[[164_tdd_test_driven_development|TDD]]/[[165_bdd_behavior_driven_development|BDD]] 실천 팀은 버그 수정 비용을 줄이고, 리팩터링에 대한 두려움이 없어진다. 테스트 스위트가 안전망이 되어 빠른 기능 개발이 가능해진다.

TDD의 핵심은 **"테스트가 설계를 주도한다"**는 것이다. 테스트 불가능한 코드는 설계 문제의 징후다. TDD를 통해 자연스럽게 좋은 설계([[243_srp_single_responsibility_principle|SRP]], [[190_enterprise_di_framework_lifecycle|DI]], 느슨한 결합)를 달성한다.

> 📢 **섹션 요약 비유**: [[164_tdd_test_driven_development|TDD]] 없는 개발은 안전망 없는 고공 줄타기다. 처음에는 빠르지만 실수하면 치명적이다. 테스트가 안전망이 되어야 빠르게 달릴 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[164_tdd_test_driven_development|TDD]] ([[411_process|Test-Driven Development]]) | Red-Green-[[213_refactoring_cloud_native_rearchitecture|Refactor]] 사이클 |
| [[165_bdd_behavior_driven_development|BDD]] ([[126_bdd_behavior_driven_development_given_when_then|Behavior-Driven Development]]) | Given/When/Then, 비즈니스 언어 테스트 |
| Test Pyramid | 단위(70%) > 통합(20%) > [[265_e2e_end_to_ui_selenium|E2E]]([[489_raid_10_hybrid|10]]%) |
| [[462_mock_test_double|Mock]] | 호출 [[395_verification_process_review|검증]] [[367_test_double_isolation|테스트 더블]] |
| [[460_stub_test_double|Stub]] | 상태 제어 [[367_test_double_isolation|테스트 더블]] |
| Gherkin | [[165_bdd_behavior_driven_development|BDD]] 시나리오 기술 언어 |
| Cucumber | Gherkin 기반 [[165_bdd_behavior_driven_development|BDD]] 자동화 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
테스트 후행 시대          TDD/BDD 등장               현대 테스트 자동화
-----------------   ----------------------   ------------------------
코딩 후 테스트     ->  TDD 방법론 (Kent Beck)    ->  BDD + 비즈니스 협업
수동 QA 중심            Extreme Programming         Cucumber/Behave
회귀 버그 방치           xUnit 테스트 프레임워크        Contract Testing (Pact)
                         JUnit, NUnit, pytest          AI 기반 테스트 생성
```

### 👶 어린이를 위한 3줄 비유 설명

1. TDD는 요리하기 전에 맛을 테스트할 방법을 먼저 정해두는 거예요. 이렇게 익으면 성공이라는 기준을 먼저 만들고 요리를 시작해요.
2. BDD는 요리사(개발자), 손님(PO), 식품 검사관(QA)이 다 함께 이 음식이 어떤 맛이어야 합격인가를 미리 약속하는 거예요.
3. Mock은 진짜 재료 대신 연습용 모형 재료로 조리 연습을 하는 거예요. 실제 재료 없이도 레시피를 완성할 수 있어요.
