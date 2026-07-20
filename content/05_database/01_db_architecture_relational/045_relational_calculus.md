---
title: "Relational Calculus"
date: "2026-04-05"
tags:
  - "studynote-database"
weight: 45
---
> **핵심 인사이트**
> 1. 관계 해석(Relational Calculus)은 "무엇을(What)" 원하는지를 선언적으로 기술하는 비절차적 질의 언어 — 관계 대수(Relational Algebra)가 "어떻게(How)" 검색할지 절차를 기술하는 것과 대비되며, SQL은 관계 해석의 정신을 계승한 선언적 언어다.
> 2. 관계 해석에는 튜플 관계 해석(TRC)과 도메인 관계 해석(DRC) 두 종류 — TRC는 튜플(행)을 변수로 사용해 조건을 기술하고, DRC는 속성 값을 변수로 사용하며, SQL은 TRC에 더 가깝다.
> 3. 관계 해석의 표현력은 관계 대수와 동등(Relationally Complete) — Codd의 관계 완전성(Relational Completeness) 기준으로 두 언어는 동등한 표현력을 가지며, SQL은 이 기준을 충족한다.

---

## Ⅰ. 관계 해석 vs 관계 대수

```
관계 해석 vs 관계 대수:

관계 대수 (Relational Algebra):
  절차적 (Procedural)
  어떻게 결과를 얻는지 기술

  예: 직원 테이블에서 개발팀 직원 이름 조회
  σ_부서='개발'(직원) -> π_이름(결과)

  연산: σ(선택), π(투영), ⋈(조인), ∪, ∩, -

관계 해석 (Relational Calculus):
  비절차적 (Non-Procedural, Declarative)
  무엇을 원하는지 조건으로 기술

  예: TRC
  { t.이름 | EMPLOYEE(t) ∧ t.부서='개발' }
  "직원 튜플 t에서, t가 직원 테이블에 있고
   t의 부서가 '개발'인 것들의 이름"

SQL의 계보:
  SELECT 이름
  FROM 직원
  WHERE 부서 = '개발'

  -> 관계 해석의 선언적 정신 계승
  -> 내부 실행 계획은 관계 대수로 변환

관계 완전성 (Relational Completeness):
  관계 대수로 표현 가능한 모든 것 = 관계 해석도 표현 가능
  TRC ≡ DRC ≡ 관계 대수 (표현력 동등)
```

> 📢 **섹션 요약 비유**: 관계 해석 vs 대수는 레스토랑 주문 방식 — 해석은 "스테이크 미디엄으로 주세요(결과 명시)", 대수는 "소고기 꺼내서 120+C 20분 굽고..."(과정 명시)!

---

## Ⅱ. 튜플 관계 해석 (TRC)

```
TRC (Tuple Relational Calculus):
  형식: { t | P(t) }
  t: 튜플 변수
  P(t): t가 만족해야 할 조건(술어)

기본 구성 요소:
  원자 공식 (Atomic Formula):
  - R(t): 튜플 t가 관계 R에 속함
  - t.A θ s.B: 속성 비교 (θ: =, ≠, <, >, ≤, ≥)
  - t.A θ 상수: 상수 비교

  연결사:
  - ∧ (AND), ∨ (OR), + (NOT)

  정량자 (Quantifier):
  - ∃ (존재 정량자, Existential): "어떤 ... 가 존재한다"
  - ∀ (전체 정량자, Universal): "모든 ... 에 대해"

예제:

예1: 개발팀 직원 이름
{ t.이름 | EMPLOYEE(t) ∧ t.부서='개발' }

예2: 프로젝트에 참여하는 직원 이름 (조인)
{ t.이름 | EMPLOYEE(t) ∧
  ∃s (WORKS_ON(s) ∧ s.직원번호=t.직원번호) }

예3: 모든 프로젝트에 참여하는 직원 (전체 정량자)
{ t.이름 | EMPLOYEE(t) ∧
  ∀p (PROJECT(p) ->
  ∃w (WORKS_ON(w) ∧ w.직원번호=t.직원번호
       ∧ w.프로젝트번호=p.번호)) }

안전한 식 (Safe Expression):
  결과 튜플이 모두 원래 관계에 속해야 함
  무한 결과 방지 조건
```

> 📢 **섹션 요약 비유**: TRC는 조건 체크리스트 — "이 사람이 직원 명단에 있고(R(t)), 부서가 개발이고(조건)... 맞으면 이름 뽑아요(t.이름)!"

---

## Ⅲ. 도메인 관계 해석 (DRC)

```
DRC (Domain Relational Calculus):
  형식: { <d1, d2, ..., dn> | P(d1, d2, ..., dn) }
  d: 도메인(속성 값) 변수
  P: 조건

  특징: 튜플이 아닌 개별 속성 값을 변수로 사용

예제:

예1: 개발팀 직원 이름
{ <이름> | ∃부서 ∃번호 (EMPLOYEE(번호, 이름, 부서)
            ∧ 부서='개발') }

예2: QBE (Query By Example) — DRC의 실용적 구현
  IBM 1970년대 개발한 시각적 질의 언어

  테이블 형태 인터페이스:
  EMPLOYEE | 직원번호 | 이름    | 부서
           | _번호   | P._이름 | 개발

  _: 변수 표시
  P.: 출력(Print) 표시

  Access 쿼리 디자인 뷰 = QBE의 후손

TRC vs DRC 비교:
  TRC: 튜플 단위 처리 -> SQL에 더 가까움
  DRC: 속성값 단위 처리 -> QBE에 더 가까움
  표현력: 동등 (Codd의 관계 완전성)

실제 SQL과 매핑:
  TRC: SELECT, FROM, WHERE의 직접 대응
  DRC: 덜 직접적이나 동등 표현 가능
```

> 📢 **섹션 요약 비유**: DRC는 빈칸 채우기 — 표에 조건 빈칸 채우면 "이 조건 맞는 행 찾아줘!" QBE(엑셀 필터)가 DRC의 친구!

---

## Ⅳ. SQL과의 관계

```
SQL = TRC의 실용적 구현:

TRC 식:
{ t.이름, t.급여 | EMPLOYEE(t) ∧ t.급여 > 5000
  ∧ ∃d (DEPT(d) ∧ d.번호=t.부서번호 ∧ d.이름='개발') }

SQL 대응:
SELECT e.이름, e.급여
FROM EMPLOYEE e
WHERE e.급여 > 5000
  AND EXISTS (
    SELECT 1 FROM DEPT d
    WHERE d.번호 = e.부서번호
      AND d.이름 = '개발'
  );

관계:
  ∃ -> EXISTS / IN
  ∀ -> NOT EXISTS + 부정 또는 ALL
  ∧ -> AND
  ∨ -> OR
  + -> NOT

전체 정량자(∀) SQL 변환:
  "모든 부서에 참여한 직원"

  TRC: ∀d (DEPT(d) -> ∃w (WORKS_ON(w) ∧ ...))

  SQL (이중 부정):
  SELECT 이름 FROM EMPLOYEE e
  WHERE NOT EXISTS (
    SELECT * FROM DEPT d
    WHERE NOT EXISTS (
      SELECT * FROM WORKS_ON w
      WHERE w.직원번호 = e.직원번호
        AND w.부서번호 = d.번호
    )
  );

  "존재하지 않는 부서를 가진 직원을 제외"

DBMS 내부:
  SQL -> 관계 해석 파싱 -> 관계 대수 변환
  -> 쿼리 최적화 -> 실행 계획
```

> 📢 **섹션 요약 비유**: SQL은 관계 해석의 한국어판 — 수학적 기호({ t | ...})를 사람이 읽기 쉬운 SELECT-FROM-WHERE로 번역한 것!

---

## Ⅴ. 실무 시나리오 — 복잡 쿼리 이해

```
인사 DB 복잡 쿼리 분석:

테이블:
  EMPLOYEE(empno, name, dept, salary, mgr)
  DEPT(deptno, dname, location)
  PROJECT(projno, pname, budget)
  WORKS_ON(empno, projno, hours)

요구사항: "모든 프로젝트에 참여한 직원 목록"

관계 해석 사고:
  { t.name | EMPLOYEE(t) ∧
    ∀p (PROJECT(p) ->
      ∃w (WORKS_ON(w) ∧ w.empno=t.empno
           ∧ w.projno=p.projno)) }

이중 부정 SQL:
  SELECT e.name
  FROM EMPLOYEE e
  WHERE NOT EXISTS (
    -- 이 직원이 참여하지 않은 프로젝트가 없어야 함
    SELECT 1 FROM PROJECT p
    WHERE NOT EXISTS (
      SELECT 1 FROM WORKS_ON w
      WHERE w.empno = e.empno
        AND w.projno = p.projno
    )
  );

쿼리 최적화기 작동:
  1. SQL 파싱 -> TRC 형태 내부 표현
  2. 관계 대수 트리로 변환:
     σ_조건(EMPLOYEE ⋈ WORKS_ON ⋈ PROJECT)
  3. 조인 순서 최적화 (통계 기반)
  4. 인덱스 활용 계획 수립
  5. 실행

이해의 핵심:
  복잡한 NOT EXISTS 쿼리를 이해하려면
  관계 해석의 전체 정량자(∀) 개념 필수
  "이 직원이 참여 안 한 프로젝트가 없다"
  = "모든 프로젝트에 참여했다"
```

> 📢 **섹션 요약 비유**: 이중 부정 쿼리는 "이 학생이 빠진 수업이 없는가?" — 모든 수업에 출석한 학생 찾기. NOT EXISTS(빠진 수업 없음)으로 "모든 수업 참여" 표현!

---

## 📌 관련 개념 맵

```
관계 해석 (Relational Calculus)
+-- 종류
|   +-- TRC (튜플 기반) -> SQL
|   +-- DRC (도메인 기반) -> QBE
+-- 비교
|   +-- 관계 대수 (절차적)
|   +-- 관계 완전성 (동등 표현력)
+-- 구성
|   +-- 원자 공식
|   +-- 정량자 (∃, ∀)
|   +-- 연결사 (∧, ∨, +)
+-- 활용
    +-- SQL 변환 (EXISTS, NOT EXISTS)
    +-- DBMS 내부 쿼리 처리
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Codd의 관계 모델 (1970)]
관계 대수 + 관계 해석 제안
관계 완전성 기준 정의
      |
      v
[SEQUEL/SQL (1974)]
IBM System R
TRC 기반 선언적 SQL
      |
      v
[QBE (1975)]
IBM Zloof
DRC 기반 시각적 질의
      |
      v
[SQL 표준화 (1986~)]
ANSI SQL 표준
EXISTS, 서브쿼리 정형화
      |
      v
[현재]
SQL:2023 표준
관계 해석은 이론적 기반으로 지속
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 관계 해석은 결과 주문서 — "이런 조건 맞는 것들 주세요!"라고 선언. 어떻게 찾는지는 DB가 알아서 해요!
2. ∃(존재)는 "적어도 하나" — "이 학생이 참여한 프로젝트가 하나라도 있으면 OK!"
3. ∀(모두)는 이중 부정으로 — "모든 프로젝트에 참여"는 "빠진 프로젝트가 없음"으로 표현. SQL의 NOT EXISTS가 이것!
