---
title: "Tdd Bdd Test Driven Behavior Driven Development"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
weight: 44
---
> **핵심 인사이트**
> 1. TDD(Test-Driven Development)는 "테스트 먼저 작성 -> 최소 코드로 통과 -> 리팩토링"의 Red-Green-Refactor 사이클로 — 테스트가 설계 도구가 되어 과도한 설계(Over-엔진ering)를 방지하고, 변경에 안전한 코드베이스를 만드는 개발 방법론이다.
> 2. BDD(Behavior-Driven Development)는 TDD의 "무엇을 테스트할지 불명확함" 문제를 해결하기 위해 Dan North가 제안한 확장으로 — Gherkin 언어(Given-When-Then)로 비즈니스 시나리오를 자연어로 작성하여 비개발자와의 공통 언어를 확보한다.
> 3. TDD/BDD의 실질적 가치는 "버그를 코드 작성 시점에 잡는다"는 것으로 — 프로덕션 버그 1건을 수정하는 비용이 TDD로 테스트 작성하는 비용의 10~100배임을 감안할 때, CI/CD 파이프라인과 결합된 TDD는 장기적으로 개발 속도를 오히려 향상시킨다.

---

## Ⅰ. TDD 개념

```
TDD (Test-Driven Development):
  Kent Beck 창안, XP(eXtreme Programming) 핵심 실천법

Red-Green-Refactor 사이클:

  1. RED: 실패하는 테스트 작성
     아직 구현이 없으니 당연히 실패
     -> 테스트가 요구사항을 정의

  2. GREEN: 최소 코드로 테스트 통과
     통과만 하면 됨, 완벽하지 않아도 OK

  3. REFACTOR: 코드 개선
     테스트는 그린 상태 유지하며 코드 정리
     중복 제거, 가독성 향상

TDD 사이클 예시 (Python):

  # RED: 테스트 먼저
  def test_add():
      assert add(2, 3) == 5  # add 함수 없음 -> 실패

  # GREEN: 최소 구현
  def add(a, b):
      return a + b  # 테스트 통과

  # REFACTOR: 개선 (이 예시는 이미 단순)

TDD의 3 규칙 (Uncle Bob):
  1. 실패하는 유닛 테스트 없이 프로덕션 코드 작성 금지
  2. 실패를 확인하기에 충분한 테스트만 작성
  3. 현재 실패 테스트를 통과하기에 충분한 코드만 작성

테스트 유형:
  단위 테스트 (Unit): 함수/클래스 개별
  통합 테스트 (Integration): 모듈 간 연동
  E2E 테스트 (End-to-End): 사용자 시나리오 전체

  TDD: 주로 단위 테스트 중심
```

> 📢 **섹션 요약 비유**: TDD는 미래의 나에게 편지 먼저 쓰기 — "이 기능은 이렇게 동작해야 해"를 테스트로 먼저 정의하고, 그 편지 내용에 맞는 코드를 만들어가요.

---

## Ⅱ. BDD 개념

```
BDD (Behavior-Driven Development):
  Dan North, 2003년 제안
  TDD 확장: 비즈니스 행동 중심

문제 의식:
  TDD: "무엇을 테스트해야 하는가?" 불명확
  BDD: 비즈니스 시나리오로 테스트 범위 정의

Gherkin 언어 (자연어 테스트 시나리오):
  Feature: 쇼핑 카트
    Scenario: 상품 추가
      Given 빈 쇼핑 카트가 있다
      When 사용자가 상품 A를 카트에 추가한다
      Then 카트에 상품 A가 1개 있다
      And 카트 합계 금액이 10,000원이다

  Scenario: 재고 없는 상품 추가 시도
      Given 재고가 0인 상품 B가 있다
      When 사용자가 상품 B를 카트에 추가한다
      Then "품절" 오류 메시지가 표시된다

  Given: 사전 조건 (Pre-condition)
  When: 행동 (Action)
  Then: 기대 결과 (Expected Outcome)

BDD 도구:
  Cucumber (Java, Ruby, JavaScript):
    Gherkin 파일 -> 자동 테스트 실행

  Behave (Python):
    given, when, then 데코레이터

  SpecFlow (.NET):
    C# 통합

BDD의 가치:
  비개발자(PM, 기획자) 시나리오 작성 가능
  살아있는 문서 (Living Documentation)
  테스트 = 명세 = 문서
```

> 📢 **섹션 요약 비유**: BDD는 사용 설명서 먼저 쓰기 — 제품(코드)을 만들기 전에 "이렇게 사용합니다"를 먼저 작성. 기획자도 읽고 이해할 수 있는 테스트 명세서.

---

## Ⅲ. TDD 실천 패턴

```
TDD 실천 패턴:

테스트 더블 (Test Double):
  실제 의존성 대신 테스트용 대체물

  Mock: 호출 기대값 설정 + 검증
    mock_repo.find_by_id.return_value = user
    mock_repo.find_by_id.assert_called_once_with(123)

  Stub: 정해진 값만 반환
    stub_repo.find_by_id = lambda id: User(id=id, name="test")

  Spy: 실제 동작 + 호출 기록
  Fake: 간단한 실제 구현 (메모리 DB 등)

Python pytest 예시:
  import pytest
  from unittest.mock import Mock

  class UserService:
      def __init__(self, repo):
          self.repo = repo
      def get_user(self, user_id):
          return self.repo.find_by_id(user_id)

  def test_get_user_returns_user():
      # Arrange
      mock_repo = Mock()
      mock_repo.find_by_id.return_value = {"id": 1, "name": "Alice"}
      service = UserService(mock_repo)

      # Act
      result = service.get_user(1)

      # Assert
      assert result["name"] == "Alice"
      mock_repo.find_by_id.assert_called_once_with(1)

AAA 패턴 (Arrange-Act-Assert):
  Arrange: 테스트 환경 설정
  Act: 테스트 대상 실행
  Assert: 결과 검증

  = Given-When-Then의 코드 버전

테스트 커버리지:
  목표: 80% 이상 (단위 테스트 기준)
  100%는 오히려 과도할 수 있음 (Getter/Setter)

  도구: Istanbul (JS), Coverage.py, JaCoCo (Java)
```

> 📢 **섹션 요약 비유**: Mock은 테스트용 모조품 — 진짜 데이터베이스 대신 "요청하면 이 값 줘"라고 프로그래밍된 모조 DB. 실제 DB 없이도 빠르고 정확하게 테스트 가능.

---

## Ⅳ. TDD/BDD와 CI/CD 통합

```
TDD/BDD + CI/CD 파이프라인:

완전 자동화 흐름:
  1. 개발자: 로컬에서 TDD 사이클
     Red -> Green -> Refactor

  2. git push -> PR 생성

  3. CI 파이프라인 자동 실행:
     단위 테스트 -> 통합 테스트 -> E2E 테스트

  4. BDD 시나리오 자동 검증:
     Cucumber: .feature 파일 실행

  5. 테스트 커버리지 리포트 생성

  6. 품질 게이트: 커버리지 < 80% -> 머지 차단

  7. 모든 테스트 통과 -> 프로덕션 자동 배포

GitHub Actions 예시:
  name: Test
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Run tests
          run: pytest --cov=. --cov-fail-under=80
        - name: BDD
          run: behave features/

테스트 피라미드:
       /E2E\          <- 적게 (느림, 비용)
      /통합테스트\     <- 중간
     /단위테스트/      <- 많이 (빠름, 저렴)

  단위 70% + 통합 20% + E2E 10% 권장

TDD 도입 장벽과 극복:
  "시간이 없어요": 테스트 작성 시간 = 디버깅 시간 감소
  "테스트 작성 어려워요": 레거시는 테스트 가능 설계 먼저
  "100% 커버리지 요구": 80%로 시작, 점진적 개선

  XP의 실천: "테스트 없는 코드는 레거시 코드"
```

> 📢 **섹션 요약 비유**: TDD + CI/CD는 자동 품질 검사 컨베이어 — 코드(제품)가 컨베이어에 오르면 자동으로 테스트(품질 검사)를 통과해야 출하(배포). 불량품은 자동 반려.

---

## Ⅴ. 실무 시나리오 — API 개발 TDD+BDD

```
결제 API TDD+BDD 개발:

요구사항:
  POST /payments
  성공: 결제 완료, 주문 상태 업데이트
  실패: 잔액 부족 시 400 오류

BDD 시나리오 (Gherkin):
  Feature: 결제 처리

    Scenario: 정상 결제
      Given 사용자 A가 잔액 50,000원을 보유한다
      And 주문 금액이 30,000원이다
      When 사용자가 결제를 요청한다
      Then 결제가 성공한다
      And 사용자 잔액이 20,000원이 된다
      And 주문 상태가 "결제 완료"로 변경된다

    Scenario: 잔액 부족
      Given 사용자 B가 잔액 10,000원을 보유한다
      And 주문 금액이 30,000원이다
      When 사용자가 결제를 요청한다
      Then 400 오류가 반환된다
      And "잔액 부족" 메시지가 포함된다
      And 주문 상태는 변경되지 않는다

TDD 구현:
  # 1. 단위 테스트 먼저 (서비스 레이어)
  def test_process_payment_success():
      mock_user = Mock(balance=50000)
      mock_order = Mock(amount=30000)

      result = payment_service.process(mock_user, mock_order)

      assert result.success == True
      assert mock_user.balance == 20000

  def test_process_payment_insufficient_balance():
      mock_user = Mock(balance=10000)
      mock_order = Mock(amount=30000)

      with pytest.raises(InsufficientBalanceError):
          payment_service.process(mock_user, mock_order)

결과:
  TDD 비용: 테스트 작성 +30% 시간
  효과:
    프로덕션 버그: 70% 감소
    디버깅 시간: 60% 감소
    리팩토링 안전성: 대폭 향상

  ROI: 6개월 후 개발 속도 20% 향상
  (초기 속도 저하 후 리팩토링 가속)
```

> 📢 **섹션 요약 비유**: 결제 API TDD+BDD는 요리 레시피+시식 — BDD로 "이 요리가 이런 맛이어야 해" 먼저 정의하고, TDD로 재료(코드) 하나씩 만들면서 맛(테스트) 확인. 최종 요리는 항상 원하는 맛!

---

## 📌 관련 개념 맵

```
TDD & BDD
+-- TDD
|   +-- Red-Green-Refactor 사이클
|   +-- 테스트 더블 (Mock, Stub, Spy)
|   +-- AAA 패턴
+-- BDD
|   +-- Gherkin (Given-When-Then)
|   +-- Cucumber, Behave, SpecFlow
|   +-- 살아있는 문서
+-- CI/CD 통합
|   +-- 테스트 피라미드
|   +-- 품질 게이트 (커버리지 80%)
+-- 효과
|   +-- 버그 조기 발견
|   +-- 리팩토링 안전망
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[TDD 탄생 (1999)]
Kent Beck: XP 실천법으로 체계화
Red-Green-Refactor 사이클
      |
      v
[BDD 제안 (2003)]
Dan North: TDD + 비즈니스 언어
Gherkin/Cucumber 도구 탄생
      |
      v
[CI/CD 통합 (2010s)]
Jenkins -> Travis -> GitHub Actions
테스트 자동화 파이프라인 표준화
      |
      v
[테스트 문화 확산 (2015~)]
DevOps 운동과 결합
팀 전체 품질 책임 문화
      |
      v
[현재: AI 테스트 생성]
GitHub Copilot 테스트 코드 생성
AI 기반 엣지 케이스 자동 탐지
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. TDD는 편지 먼저 쓰기 — "이 기능은 이렇게 동작해야 해"를 테스트로 먼저 정의하고, 그 편지 내용에 맞게 코드를 만들어요!
2. BDD는 사용 설명서 먼저 — "사용자가 이렇게 하면 이렇게 돼야 해"를 기획자도 이해하는 자연어로 먼저 써요.
3. 테스트가 있으면 리팩토링이 안전 — 코드를 고쳐도 테스트가 통과하면 "잘 돼!" 확인 가능. 테스트 없이 고치면 뭔가 망가질까봐 두려워요!
