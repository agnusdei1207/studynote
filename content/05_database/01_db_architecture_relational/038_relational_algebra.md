---
title: "Relational Algebra"
date: "2026-03-03"
tags:
  - "studynote-database"
weight: 38
---
> **핵심 인사이트**
> 1. 관계 대수(Relational Algebra)는 Edgar F. Codd가 정의한 관계형 데이터베이스의 이론적 기반으로, 테이블(릴레이션)에 적용하는 8개 연산자의 집합이며, SQL의 SELECT·FROM·WHERE·JOIN·GROUP BY가 모두 관계 대수 연산의 직접 구현이다.
> 2. 기본 연산(선택·사영·카티션 곱·합집합·차집합)만으로 모든 관계형 쿼리를 표현할 수 있으며, JOIN·교차·나누기는 이들로부터 유도된다 — 쿼리 최적화기(Query Optimizer)는 관계 대수 표현식을 변환해 최적 실행 계획을 탐색한다.
> 3. 관계 대수를 이해하면 SQL의 실행 순서(FROM->WHERE->GROUP BY->HAVING->SELECT->ORDER BY)와 인덱스 설계의 논리적 근거를 파악할 수 있으며, 쿼리 최적화 사고의 기반이 된다.

---

## I. 기본 연산 5가지

```
1. 선택 (Selection, σ): 행 필터링
   σ_(조건)(R)
   SQL: WHERE 절
   예: σ_(age > 20)(Student) -> 20세 초과 학생 행

2. 사영 (Projection, π): 열 선택
   π_(열목록)(R)
   SQL: SELECT 열 목록
   예: π_(name, age)(Student) -> 이름, 나이 열만

3. 카티션 곱 (Cartesian Product, ×):
   R × S -> 모든 행 조합
   SQL: FROM R, S (조인 조건 없음)
   |R|=n, |S|=m -> n×m 행

4. 합집합 (Union, ∪):
   R ∪ S -> 두 릴레이션의 모든 행 (중복 제거)
   SQL: UNION (호환 스키마 필요)

5. 차집합 (Difference, -):
   R - S -> R에 있지만 S에 없는 행
   SQL: EXCEPT (표준) / MINUS (Oracle)
```

> 📢 **섹션 요약 비유**: 선택=행 찢기, 사영=열 자르기, 카티션 곱=두 표의 모든 조합, 합집합=두 표 합치기, 차집합=한 표에서 다른 표 빼기.

---

## II. 유도 연산

```
6. 조인 (Join, ⋈):
   R ⋈_(조건) S = σ_(조건)(R × S)
   카티션 곱 후 조건으로 필터링
   SQL: JOIN ... ON 조건

   자연 조인: 공통 속성 자동 매칭
   세타 조인: 임의 조건 (=, <, > 등)

7. 교차 (Intersection, ∩):
   R ∩ S = R - (R - S)
   SQL: INTERSECT
   양쪽에 모두 있는 행만

8. 나누기 (Division, ÷):
   R ÷ S = {t | ∀s∈S: (t,s)∈R}
   "R에서 S의 모든 값과 매칭되는 행"
   SQL: NOT EXISTS + 집합 연산으로 구현
   예: "모든 과목을 수강한 학생"
```

| 연산    | 기호 | SQL 대응     | 의미              |
|-------|-----|------------|-----------------|
| 선택   | σ   | WHERE      | 행 필터           |
| 사영   | π   | SELECT (열) | 열 선택           |
| 조인   | ⋈   | JOIN ON    | 관련 테이블 결합   |
| 합집합 | ∪   | UNION      | 두 결과 합치기    |
| 차집합 | -   | EXCEPT     | 첫 번째에서 두 번째 제거|

> 📢 **섹션 요약 비유**: 관계 대수는 데이터 레고 — 기본 블록(5개 연산)으로 복잡한 구조(조인, 나누기)를 조립.

---

## III. 쿼리 최적화와 관계 대수

```
SQL -> 관계 대수 표현식 -> 최적화 -> 실행 계획

예시 SQL:
  SELECT s.name
  FROM Student s JOIN Enrollment e ON s.id = e.student_id
  WHERE s.gpa > 3.5 AND e.grade = 'A'

관계 대수 표현:
  π_(name)(σ_(gpa>3.5 AND grade='A')(Student ⋈ Enrollment))

최적화기 변환:
  먼저 σ 적용 (선택 먼저 = 조기 필터링):
  π_(name)(
    σ_(gpa>3.5)(Student) ⋈ σ_(grade='A')(Enrollment)
  )

  -> 조인 전에 각 테이블 크기 줄이기
  -> 인덱스 활용 가능성 증가
```

> 📢 **섹션 요약 비유**: 조인 전에 각 테이블을 먼저 필터링하는 것 — 10만 명을 조인하기 전에 "gpa>3.5"인 1천 명만 뽑아서 조인하면 100배 빠르다.

---

## IV. 관계 대수와 SQL 실행 순서

```
SQL 논리적 실행 순서 (관계 대수 관점):

1. FROM     -> 카티션 곱 / 조인 (릴레이션 선택)
2. WHERE    -> 선택 (σ) - 행 필터
3. GROUP BY -> 그룹화 (집계 준비)
4. HAVING   -> 그룹 선택 (σ_그룹)
5. SELECT   -> 사영 (π) - 열 선택
6. ORDER BY -> 정렬 (관계 대수 외, 순서 연산)
7. LIMIT    -> 잘라내기

별칭(Alias)을 WHERE에 못 쓰는 이유:
  SELECT name AS nm FROM t WHERE nm='x'  -> 오류!
  SELECT는 WHERE보다 나중에 실행 -> nm이 아직 없음!
```

> 📢 **섹션 요약 비유**: SQL은 작성 순서와 실행 순서가 다르다 — 이를 모르면 "왜 SELECT 별칭을 WHERE에서 못 쓰는지" 이해가 안 된다.

---

## V. 실무 시나리오 — 쿼리 최적화 사고

```
문제 쿼리 (느림):
  SELECT o.id, c.name, p.name
  FROM Orders o, Customers c, Products p
  WHERE o.customer_id = c.id
    AND o.product_id = p.id
    AND c.country = 'Korea'
    AND p.category = 'Electronics'

관계 대수 분석:
  카티션 곱: Orders × Customers × Products
  -> n1 × n2 × n3 행 생성 후 필터 -> 매우 느림!

최적화:
  1. 먼저 Customers 필터: σ_(country='Korea')(Customers)
  2. Orders와 조인 (줄어든 Customers와)
  3. Products 필터: σ_(category='Electronics')(Products)
  4. 위 결과와 조인

  인덱스:
  idx_customers_country (country)
  idx_products_category (category)
```

> 📢 **섹션 요약 비유**: 전국 배달 경로(Orders × C고객s × Products)를 계산하기 전에 "서울 고객"과 "전자제품"만 먼저 추려서 경우의 수를 줄이는 것.

---

## 📌 관련 개념 맵

```
관계 대수
+-- 기본 5연산
|   +-- 선택(σ), 사영(π)
|   +-- 카티션 곱(×), 합집합(∪), 차집합(-)
+-- 유도 연산
|   +-- 조인(⋈), 교차(∩), 나누기(÷)
+-- SQL 매핑
|   +-- 실행 순서: FROM->WHERE->GROUP->SELECT
+-- 쿼리 최적화
    +-- 선택 먼저 (Selection Pushdown)
    +-- 사영 먼저 (Projection Pushdown)
    +-- 조인 순서 최적화
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Edgar F. Codd 관계 모델 (1970)]
관계 대수 이론 정립
12개 규칙 제시
      |
      v
[SQL 등장 (IBM SEQUEL, 1974)]
관계 대수를 선언적 언어로 구현
SQL 표준화 (ANSI 1986)
      |
      v
[쿼리 최적화기 발전]
관계 대수 변환으로 실행 계획 탐색
비용 기반 최적화 (CBO)
      |
      v
[현재: 분산 쿼리 최적화]
Spark, Presto의 분산 관계 대수
Catalyst Optimizer, Velox
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 관계 대수는 데이터베이스 표를 가지고 할 수 있는 기본 연산들 — 행 고르기(선택), 열 고르기(사영), 두 표 결합하기(조인)예요.
2. SQL의 WHERE, SELECT, JOIN이 모두 이 수학 연산을 쉽게 쓸 수 있게 만든 거예요.
3. 컴퓨터가 SQL을 실행할 때 먼저 데이터를 많이 줄여놓고(선택 먼저) 합치는(조인 나중) 순서로 최적화해서 빠르게 처리해요!
