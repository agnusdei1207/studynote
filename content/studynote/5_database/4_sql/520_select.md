+++
title = "SELECT 문"
description = "SQL SELECT 문의 기본 구조와 사용법"
date = 2026-03-26
weight = 20

[taxonomies]
tags = ["database", "sql", "select", "query"]
+++

# SELECT 문

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SELECT 문은 관계형 데이터베이스에서 데이터를 조회하는 핵심 SQL 명령으로, 관계 대수의 프로젝션 (π), 선택 (σ), 결합 (⋈) 등의 연산을 实现한다.
> 2. **가치**: SELECT 문을 통해 필요한 데이터만 필터링하고, 정렬하며, 집계할 수 있어 효율적인 데이터 분석과 응용 程序開発가 가능하다.
> 3. **융합**: 윈도우 함수 (Window Function), CTE (Common Table Expression), 피벗 등의 고급 기능과 결합하여 복잡한 분석查询를 지원한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

SELECT 문은 **데이터베이스에서 데이터를 조회하고 결과 집합을 반환하는 SQL 명령**이다. 관계형 모델의 관계 대수 연산에 대응한다.

### SELECT 문 기본 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SELECT 문 기본 구조                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   SELECT [ALL | DISTINCT] 열1, 열2, ...                             │
│   FROM 테이블1                                                        │
│       [INNER | LEFT | RIGHT | FULL OUTER] JOIN 테이블2              │
│       ON 조인 조건                                                    │
│   WHERE 조건                                                          │
│       [AND | OR] 조건                                                │
│   GROUP BY 열1, 열2, ...                                             │
│   HAVING 그룹 조건                                                    │
│   ORDER BY 열1 [ASC | DESC], 열2 [ASC | DESC], ...                   │
│   LIMIT 개수 [OFFSET 시작위치];                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 비유

SELECT 문은 **도서관 검색 시스템**과 같다. "어떤 조건에 맞는 책"을 찾고 (WHERE), "어떤 항목"을 보고 싶고 (SELECT), "어떤 순서"로 정렬할지 (ORDER BY) 지정할 수 있다.

- **📢 섹션 요약 비유:**카페에서 "메뉴판에서 (FROM) 아메리카노만 (WHERE) 이름과 가격만 (SELECT) 보여줘"라는 요청과 같습니다.

---

## Ⅱ. 기본 사용법

### 1. 전체 열 조회

```sql
-- customers 테이블의 모든 열 조회
SELECT *
FROM customers;
```

### 2. 특정 열 조회

```sql
-- 고객 이름과 도시만 조회
SELECT customer_name, city
FROM customers;
```

### 3. 중복 제거 (DISTINCT)

```sql
-- 고객이 있는 도시 목록 (중복 없이)
SELECT DISTINCT city
FROM customers;
```

### 4. WHERE 조건

```sql
-- 서울에 사는 고객 조회
SELECT customer_name, city
FROM customers
WHERE city = '서울';
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WHERE 조건 예시                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   비교 연산자: =, <>, <, >, <=, >=                                  │
│   예: WHERE age >= 20                                               │
│                                                                     │
│   논리 연산자: AND, OR, NOT                                         │
│   예: WHERE age >= 20 AND city = '서울'                             │
│                                                                     │
│   범위: BETWEEN ... AND ...                                         │
│   예: WHERE age BETWEEN 20 AND 30                                    │
│                                                                     │
│   목록: IN (...)                                                     │
│   예: WHERE city IN ('서울', '부산', '인천')                        │
│                                                                     │
│   패턴 매칭: LIKE                                                    │
│   예: WHERE name LIKE '김%'                                         │
│   (%는 0자 이상 문자, _는 1자)                                       │
│                                                                     │
│   NULL: IS NULL, IS NOT NULL                                        │
│   예: WHERE phone IS NOT NULL                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 5. ORDER BY (정렬)

```sql
-- 나이순으로 오름차순 정렬
SELECT customer_name, age
FROM customers
ORDER BY age ASC;

-- 나이순 내림차순, 나이 같으면 이름순
SELECT customer_name, age
FROM customers
ORDER BY age DESC, customer_name ASC;
```

### 6. LIMIT (결과 제한)

```sql
-- 상위 10명 조회
SELECT customer_name, age
FROM customers
ORDER BY age DESC
LIMIT 10;

-- OFFSET 활용 (페이지네이션)
SELECT customer_name, age
FROM customers
ORDER BY customer_id
LIMIT 10 OFFSET 20;  -- 21번째부터 10개
```

---

## Ⅲ. 집계 함수

### 주요 집계 함수

| 함수 | 설명 | 예시 |
|:---|:---|:---|
| **COUNT()** | 행의 수 | SELECT COUNT(*) FROM customers |
| **SUM()** | 합계 | SELECT SUM(amount) FROM orders |
| **AVG()** | 평균 | SELECT AVG(age) FROM customers |
| **MAX()** | 최대값 | SELECT MAX(price) FROM products |
| **MIN()** | 최소값 | SELECT MIN(price) FROM products |

### GROUP BY (그룹화)

```sql
-- 도시별 고객 수
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
HAVING COUNT(*) >= 2;
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GROUP BY 동작 예시                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   customers 테이블:                                                  │
│   ┌────────┬────────┬────────┐                                    │
│   │ 고객ID  │ 이름    │ 도시   │                                    │
│   ├────────┼────────┼────────┤                                    │
│   │ C001   │ 김철수  │ 서울   │                                    │
│   │ C002   │ 이영희  │ 부산   │                                    │
│   │ C003   │ 박민수  │ 서울   │                                    │
│   │ C004   │ 최지수  │ 부산   │                                    │
│   └────────┴────────┴────────┘                                    │
│                                                                     │
│   Query:                                                            │
│   SELECT city, COUNT(*) FROM customers GROUP BY city;              │
│                                                                     │
│   Result:                                                           │
│   ┌────────┬──────────────┐                                        │
│   │ 도시   │ COUNT(*)     │                                        │
│   ├────────┼──────────────┤                                        │
│   │ 서울   │ 2            │                                        │
│   │ 부산   │ 2            │                                        │
│   └────────┴──────────────┘                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### HAVING vs WHERE

| 구분 | WHERE | HAVING |
|:---|:---|:---|
| **적용 시점** | 그룹화 전 필터링 | 그룹화 후 필터링 |
| **집계 함수 사용** | 불가 | 가능 |
| **예시** | 도시가 '서울'인 행만 선택 | 도시별 COUNT >= 2인 것만 선택 |

```sql
-- 올바른 예: WHERE로 먼저 필터링, THEN 그룹화
SELECT city, COUNT(*) as cnt
FROM customers
WHERE city IS NOT NULL
GROUP BY city;

-- HAVING으로 그룹 결과 필터링
SELECT city, COUNT(*) as cnt
FROM customers
GROUP BY city
HAVING cnt >= 2;
```

---

## Ⅳ. JOIN (테이블 결합)

### INNER JOIN

```sql
-- 고객과 주문 정보를 결합
SELECT c.customer_id, c.name, o.order_date, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INNER JOIN 결과                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   customers:                          orders:                       │
│   ┌────────┬──────┐                 ┌────────┬────────┐          │
│   │ C001   │ 김철수│                 │ O001   │ C001   │          │
│   │ C002   │ 이영희│                 │ O002   │ C002   │          │
│   │ C003   │ 박민수│                 │ O003   │ C001   │          │
│   └────────┴──────┘                 └────────┴────────┘          │
│                                                                     │
│   INNER JOIN 결과:                                                  │
│   ┌────────┬──────┬────────┬────────┐                            │
│   │ C001   │ 김철수│ O001   │ 50000  │                            │
│   │ C001   │ 김철수│ O003   │ 30000  │                            │
│   │ C002   │ 이영희│ O002   │ 70000  │                            │
│   │ C003   │ 박민수│ (주문없음) │  -    │ → 결과에 포함 안 됨       │
│   └────────┴──────┴────────┴────────┘                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### LEFT JOIN

```sql
-- 모든 고객과, 있으면 주문 정보
SELECT c.customer_id, c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```

LEFT JOIN은 왼쪽 테이블 (customers)의 모든 행이 결과에 포함되며, 오른쪽 테이블에 매칭되는 행이 없으면 NULL로 채워진다.

---

## Ⅴ. 서브쿼리 (Subquery)

```sql
-- 평균 나이보다 나이 많은 고객
SELECT name, age
FROM customers
WHERE age > (SELECT AVG(age) FROM customers);
```

### 스칼라 서브쿼리

```sql
-- 각 고객과 평균 나이 비교
SELECT name, age,
    (SELECT AVG(age) FROM customers) as avg_age
FROM customers;
```

### EXISTS 활용

```sql
-- 주문이 있는 고객만
SELECT name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **관계 대수** | SELECT 문은 관계 대수의 σ (선택), π (투영), ⋈ (결합) 연산에 대응한다. |
| **GROUP BY** | 투플을 그룹화하여 집계 함수와 함께 사용한다. |
| **JOIN** | 외래 키를 기반으로 여러 테이블의 데이터를 결합한다. |
| **서브쿼리** | SELECT 문 내에 중첩된 SELECT 문으로, 복잡한 查询条件을 표현한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. SELECT 문은 **음식점 주문**과 같아요. "메뉴판에서 (FROM) 좋아하는 것만 (WHERE) 골라서 (SELECT) 맛있는 순으로 (ORDER BY) 보여줘요."
2. GROUP BY는 같은 종류별로 묶어달라는 것이에요. "과자별로 과자 봉지를 묶어줘"와 같아요.
3. JOIN은 여러 표에서 관련 있는 항목을 함께 보여주는 거예요. "고객 명단과 주문 내역을 함께 보여줘"라는 것처럼요!
