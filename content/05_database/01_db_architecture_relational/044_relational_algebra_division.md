---
title: "Relational Algebra Division"
date: "2026-04-05"
tags:
  - "studynote-database"
weight: 44
---
> **핵심 인사이트**
> 1. 관계 대수의 나눗셈(Division, ÷) 연산은 "모든 조건을 만족하는 대상"을 구하는 연산으로 — "모든 과목을 수강한 학생", "모든 상품을 구매한 고객" 등 <strong>전체 집합 포함 여부</strong>를 묻는 쿼리에 사용된다.
> 2. 나눗셈 R÷S의 결과는 — R에서 S의 모든 투플과 조합될 수 있는 R의 속성값들로 구성되며, SQL에서는 직접 지원하지 않아 <strong>이중 NOT EXISTS</strong> 또는 COUNT 비교로 구현해야 한다.
> 3. 나눗셈은 관계 대수의 6개 기본 연산(선택, 투영, 합집합, 차집합, 카티전 곱, 이름 변경)으로 유도 가능한 파생 연산이지만 — "모든 X를 포함하는 Y"라는 쿼리 패턴에서 표현력이 매우 높아 개념적 이해가 중요하다.

---

## Ⅰ. 나눗셈 연산 정의

```
나눗셈 연산 (Division Operation):

표기: R ÷ S
  R: 피제수 릴레이션 (분자)
  S: 제수 릴레이션 (분모)

조건:
  Attr(S) ⊆ Attr(R)  (S의 속성은 R의 속성 포함)
  결과 속성 = Attr(R) - Attr(S)

정의:
  R ÷ S = {t | t ∈ πR-S(R) ∧ ∀s ∈ S, (t, s) ∈ R}

  즉, 결과 t는:
  1. R에서 S 속성을 제외한 투영값이며
  2. S의 모든 투플 s에 대해 (t, s)가 R에 존재해야 함

직관적 의미:
  "S의 모든 항목과 연결된 R의 값들"
  = "모든 Y를 포함하는 X를 찾아라"

예시:

수강 릴레이션 R:
  학번 | 과목코드
  101  | C001
  101  | C002
  101  | C003
  102  | C001
  102  | C002
  103  | C001

필수과목 릴레이션 S:
  과목코드
  C001
  C002

R ÷ S = ?
  각 학번별로 S의 모든 과목코드를 포함하는가?
  101: C001, C002, C003 ⊇ {C001, C002} -> 포함 ✓
  102: C001, C002 ⊇ {C001, C002} -> 포함 ✓
  103: C001 ⊉ {C001, C002} -> 미포함 ✗

  결과:
  학번
  101
  102
```

> 📢 **섹션 요약 비유**: 나눗셈은 "모두 선택" 검사 — 학생 중에서 필수 과목 전부를 들은 학생만 선택. 하나라도 빠지면 탈락. "전부 아니면 탈락"이 나눗셈의 본질.

---

## Ⅱ. 나눗셈 유도

```
나눗셈의 유도 (6개 기본 연산으로):

R ÷ S를 기본 연산으로 표현:

1. T = πR-S(R)
   R에서 S 속성 제외한 투영 = 모든 후보

2. U = T × S
   T와 S의 카티전 곱 = "후보들이 S 모두와 조합된 경우"

3. V = U - R
   U에는 있지만 R에 없는 조합 = "빠진 조합"

4. W = πR-S(V)
   V에서 S 제외 투영 = "빠진 조합이 있는 후보들"

5. 결과 = T - W
   전체 후보 - 빠진 후보 = "모든 S와 조합된 후보"

R ÷ S = πR-S(R) - πR-S((πR-S(R) × S) - R)

예시 검증:

T = {101, 102, 103}  (모든 학번)

U = T × S:
  101×C001, 101×C002
  102×C001, 102×C002
  103×C001, 103×C002

V = U - R:
  R에 있는 조합: (101,C001), (101,C002), (102,C001), (102,C002), (103,C001)
  없는 조합: (103, C002)
  V = {(103, C002)}

W = {103}  (빠진 조합이 있는 학번)

결과 = T - W = {101, 102, 103} - {103} = {101, 102} ✓
```

> 📢 **섹션 요약 비유**: 나눗셈 유도는 역방향 탐색 — "모두 가진 사람" 대신 "하나라도 없는 사람"을 찾아서 제거. 전체에서 불완전한 사람을 빼면 완전한 사람만 남아요.

---

## Ⅲ. SQL 구현

```
SQL에서 나눗셈 구현:

테이블:
  Enrollment(student_id, course_id)
  RequiredCourses(course_id)

방법 1: 이중 NOT EXISTS (Relational Division 표준)
  SELECT DISTINCT e1.student_id
  FROM Enrollment e1
  WHERE NOT EXISTS (
      SELECT * FROM RequiredCourses rc
      WHERE NOT EXISTS (
          SELECT * FROM Enrollment e2
          WHERE e2.student_id = e1.student_id
            AND e2.course_id = rc.course_id
      )
  );

  해석:
  "필수과목 중 해당 학생이 수강하지 않은 것이 하나도 없는 학생"
  = "모든 필수과목을 수강한 학생"

방법 2: COUNT 비교
  SELECT student_id
  FROM Enrollment
  WHERE course_id IN (SELECT course_id FROM RequiredCourses)
  GROUP BY student_id
  HAVING COUNT(DISTINCT course_id) = (SELECT COUNT(*) FROM RequiredCourses);

  해석:
  학생의 수강 과목 중 필수과목 수 = 전체 필수과목 수
  (단, 중복 없는 COUNT 사용)

방법 1 vs 2:
  이중 NOT EXISTS: 논리적으로 정확, 가독성 낮음
  COUNT: 가독성 높음, NULL 주의 필요

  실무: COUNT 방법이 더 직관적으로 자주 사용됨

확장 — 일정 비율 이상:
  모든 과목의 80% 이상 수강한 학생:
  HAVING COUNT(DISTINCT course_id) >=
      CEIL(0.8 × (SELECT COUNT(*) FROM RequiredCourses))
```

> 📢 **섹션 요약 비유**: 이중 NOT EXISTS는 이중 부정 확인 — "필수 과목 중에서, 이 학생이 안 들은 게 없는가?" 물어보는 것. "없다가 없다" = 있다! 논리적이지만 머리가 좀 복잡해요.

---

## Ⅳ. 나눗셈 응용 패턴

```
나눗셈 응용 패턴:

1. "모든 상품을 구매한 고객":
   Orders(customer_id, product_id) ÷ Products(product_id)

   SQL (COUNT):
   SELECT customer_id
   FROM Orders
   GROUP BY customer_id
   HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM Products);

2. "모든 기술을 보유한 직원":
   EmployeeSkills(emp_id, skill_id) ÷ RequiredSkills(skill_id)

   응용: 프로젝트 팀 적합 직원 선발

3. "모든 지역에 배송한 공급업체":
   Shipments(supplier_id, region) ÷ AllRegions(region)

   응용: 전국 배송 가능 공급업체 식별

4. "모든 테스트를 통과한 소프트웨어":
   TestResults(sw_id, test_id, result) where result='PASS'
   ÷ RequiredTests(test_id)

패턴 공통점:
  "모든 X에 대해 Y가 존재하는가?"
  = 전체 포함(Universal Quantification)
  = SQL의 NOT EXISTS(NOT EXISTS) 패턴

주의사항:
  1. S가 빈 집합(∅)이면 결과는 R의 전체 투영 (공집합 조건)
  2. 중복 데이터 처리: DISTINCT 주의
  3. NULL 처리: COUNT(DISTINCT) vs COUNT(*)
```

> 📢 **섹션 요약 비유**: 나눗셈 패턴은 "다 갖췄나?" 검사 — 직원 채용 면접에서 "필수 스킬 전부 보유한 지원자만 합격"처럼, 조건 리스트를 전부 충족해야 결과에 포함돼요.

---

## Ⅴ. 실무 시나리오 — 자격 요건 검사

```
프로젝트 팀원 자격 요건 검사 시스템:

테이블 구조:
  EmployeeSkills(emp_id, skill_name, proficiency)
  ProjectRequirements(project_id, skill_name, min_proficiency)

요구: 특정 프로젝트의 모든 기술 요건을 충족하는 직원 찾기

SQL:
  SELECT DISTINCT es.emp_id
  FROM EmployeeSkills es
  WHERE NOT EXISTS (
      SELECT 1 FROM ProjectRequirements pr
      WHERE pr.project_id = 'PRJ-001'
        AND NOT EXISTS (
            SELECT 1 FROM EmployeeSkills es2
            WHERE es2.emp_id = es.emp_id
              AND es2.skill_name = pr.skill_name
              AND es2.proficiency >= pr.min_proficiency
        )
  );

설명:
  "PRJ-001의 요건 중에서,
   이 직원이 충족하지 못하는 요건이 하나도 없는 직원"

성능 최적화:
  인덱스: (emp_id, skill_name), (project_id, skill_name)

  COUNT 방법 (더 빠를 수 있음):
  SELECT es.emp_id
  FROM EmployeeSkills es
  JOIN ProjectRequirements pr ON es.skill_name = pr.skill_name
    AND es.proficiency >= pr.min_proficiency
    AND pr.project_id = 'PRJ-001'
  GROUP BY es.emp_id
  HAVING COUNT(DISTINCT pr.skill_name) = (
      SELECT COUNT(*) FROM ProjectRequirements
      WHERE project_id = 'PRJ-001'
  );

실행 계획:
  Hash Aggregate -> Hash Join -> Index Scan
  -> 수백만 레코드에서도 수초 내 응답 가능

응용:
  채용 시스템: 자격증/스킬 전부 보유 지원자
  추천 시스템: 모든 선호 조건 충족 상품
  공급망: 모든 부품 보유 공급업체
```

> 📢 **섹션 요약 비유**: 프로젝트 팀원 선발 나눗셈 — "이 프로젝트에 필요한 스킬 목록 전부를 갖춘 사람만". 스킬 하나라도 없으면 탈락. SQL로 이것을 이중 NOT EXISTS로 표현해요!

---

## 📌 관련 개념 맵

```
관계 대수 나눗셈 (Division)
+-- 정의
|   +-- R ÷ S: S 전체와 조합 가능한 R의 투플
|   +-- 전체 포함 (Universal Quantification)
+-- 유도
|   +-- 6개 기본 연산으로 표현 가능
|   +-- πR-S(R) - πR-S((πR-S(R)×S) - R)
+-- SQL 구현
|   +-- 이중 NOT EXISTS
|   +-- COUNT 비교 방법
+-- 응용
|   +-- "모든 조건 충족" 쿼리
|   +-- 채용, 추천, 공급망
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Codd 관계 대수 (1970)]
6개 기본 연산 정의
나눗셈 파생 연산으로 추가
      |
      v
[SQL 표준화 (1986)]
SELECT/WHERE/GROUP BY
나눗셈 직접 미지원
      |
      v
[NOT EXISTS 패턴 확립]
이중 부정으로 전체 포함 표현
ORM에서도 동일 패턴
      |
      v
[현재: 쿼리 최적화]
COUNT vs NOT EXISTS 성능 비교
실행 계획 분석으로 최적 선택
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 나눗셈은 "다 갖췄나?" 검사 — 필수 과목 목록 전부를 수강한 학생만 뽑는 것처럼, 조건 리스트를 전부 충족해야 결과에 포함돼요!
2. 이중 NOT EXISTS는 이중 부정 — "없는 게 없다 = 다 있다"! 논리는 복잡하지만 결과는 정확해요.
3. COUNT 방법이 더 쉬워요 — "필수과목 수 = 내가 들은 필수과목 수"면 합격! 실무에서는 이 방법을 더 자주 써요.
