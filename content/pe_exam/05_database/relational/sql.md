+++
title = "SQL (Structured Query Language)"
date = 2026-03-02

[extra]
categories = "pe_exam-database"
+++

# SQL (Structured Query Language)

## 핵심 인사이트 (3줄 요약)
> **관계형 데이터베이스를 조작하는 표준 언어**. DDL(정의), DML(조작), DCL(제어), TCL(트랜잭션)로 분류. 조인, 서브쿼리, 윈도우 함수가 실무의 핵심이다.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"SQL (Structured Query Language)의 개념과 핵심 원리를 설명하고, 관련 기술과의 비교를 통해 데이터 관리 측면에서의 활용 방안을 논하시오."**

---

### Ⅰ. 개요

#### 1. 개념
SQL은 **관계형 데이터베이스에서 데이터를 정의, 조회, 수정, 제어하기 위한 표준 언어**다.

> 비유: "도서관 사서 언어" - 책(데이터)을 찾고, 추가하고, 삭제하는 요청 언어

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 2. SQL 분류
```
┌─────────────────────────────────────────────────────────┐
│                    SQL 4대 분류                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  DDL (Data Definition Language) - 데이터 정의           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  CREATE, ALTER, DROP, TRUNCATE, RENAME           │   │
│  │  → 테이블, 뷰, 인덱스 구조 정의                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  DML (Data Manipulation Language) - 데이터 조작         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  SELECT, INSERT, UPDATE, DELETE                  │   │
│  │  → 데이터 CRUD 작업                              │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  DCL (Data Control Language) - 데이터 제어              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  GRANT, REVOKE                                   │   │
│  │  → 권한 부여/회수                                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  TCL (Transaction Control Language) - 트랜잭션 제어     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  COMMIT, ROLLBACK, SAVEPOINT                     │   │
│  │  → 트랜잭션 제어                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 3. SELECT 기본 문법
```sql
-- 기본 SELECT 구조
SELECT   컬럼(들)                     -- 5. 조회할 열 선택
FROM     테이블(들)                   -- 1. 테이블 지정
WHERE    조건                          -- 2. 행 필터링
GROUP BY 그룹화 기준                   -- 3. 그룹화
HAVING   그룹 조건                     -- 4. 그룹 필터링
ORDER BY 정렬 기준                     -- 6. 정렬
LIMIT    N                             -- 7. 결과 제한

-- 실행 순서: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

#### 4. JOIN의 종류
```sql
-- 샘플 테이블
-- 직원: Employee (emp_id, name, dept_id, salary)
-- 부서: Department (dept_id, dept_name, location)

-- INNER JOIN: 양쪽 모두 존재하는 행
SELECT e.name, d.dept_name
FROM Employee e
INNER JOIN Department d ON e.dept_id = d.dept_id;

-- LEFT OUTER JOIN: 왼쪽 테이블 모두 + 오른쪽 매칭
SELECT e.name, d.dept_name
FROM Employee e
LEFT JOIN Department d ON e.dept_id = d.dept_id;
-- 부서 없는 직원도 포함 (dept_name = NULL)

-- RIGHT OUTER JOIN: 오른쪽 테이블 모두 + 왼쪽 매칭
SELECT e.name, d.dept_name
FROM Employee e
RIGHT JOIN Department d ON e.dept_id = d.dept_id;
-- 직원 없는 부서도 포함

-- FULL OUTER JOIN: 양쪽 모두
SELECT e.name, d.dept_name
FROM Employee e
FULL OUTER JOIN Department d ON e.dept_id = d.dept_id;

-- CROSS JOIN: 카티션 곱
SELECT e.name, d.dept_name
FROM Employee e
CROSS JOIN Department d;  -- 3 × 4 = 12행

-- SELF JOIN: 같은 테이블 조인
SELECT e.name AS 직원, m.name AS 상사
FROM Employee e
JOIN Employee m ON e.manager_id = m.emp_id;
```

#### 5. 서브쿼리 (Subquery)
```sql
-- 스칼라 서브쿼리 (단일 값 반환)
SELECT name,
       salary,
       (SELECT AVG(salary) FROM Employee) AS 평균급여
FROM Employee;

-- 인라인 뷰 (FROM 절 서브쿼리)
SELECT dept_name, avg_sal
FROM (
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM Employee
    GROUP BY dept_id
) AS dept_avg
JOIN Department d ON dept_avg.dept_id = d.dept_id;

-- WHERE 절 서브쿼리
-- 평균 급여 이상인 직원
SELECT name, salary
FROM Employee
WHERE salary >= (SELECT AVG(salary) FROM Employee);

-- EXISTS 서브쿼리
SELECT d.dept_name
FROM Department d
WHERE EXISTS (
    SELECT 1 FROM Employee e
    WHERE e.dept_id = d.dept_id
    AND e.salary > 5000000
);

-- IN 서브쿼리
SELECT name FROM Employee
WHERE dept_id IN (
    SELECT dept_id FROM Department
    WHERE location = '서울'
);
```

#### 6. 집계 함수와 GROUP BY
```sql
-- 집계 함수
SELECT
    dept_id,
    COUNT(*)          AS 인원수,
    SUM(salary)       AS 총급여,
    AVG(salary)       AS 평균급여,
    MAX(salary)       AS 최고급여,
    MIN(salary)       AS 최저급여,
    STDDEV(salary)    AS 급여표준편차
FROM Employee
GROUP BY dept_id
HAVING AVG(salary) >= 4000000  -- 평균 400만 이상 부서
ORDER BY 평균급여 DESC;
```

#### 7. 윈도우 함수 (Window Function)
```sql
-- 집계하되 행 그룹화하지 않는 고급 함수
SELECT
    name,
    dept_id,
    salary,
    -- 부서 내 급여 순위
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS 부서내순위,
    -- 전체 순위
    RANK() OVER (ORDER BY salary DESC) AS 전체순위,
    -- 부서 내 누적 합계
    SUM(salary) OVER (PARTITION BY dept_id) AS 부서총급여,
    -- 이동 평균 (현재 행 포함 이전 2행)
    AVG(salary) OVER (
        PARTITION BY dept_id
        ORDER BY emp_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS 이동평균급여,
    -- 행 번호
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS 행번호
FROM Employee;
```

#### 8. DDL 예시
```sql
-- 테이블 생성
CREATE TABLE Employee (
    emp_id      INT         PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL,
    dept_id     INT,
    salary      DECIMAL(10,2) DEFAULT 3000000,
    hire_date   DATE,
    email       VARCHAR(100) UNIQUE,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 인덱스 생성
CREATE INDEX idx_salary ON Employee(salary);
CREATE UNIQUE INDEX idx_email ON Employee(email);

-- 뷰 생성
CREATE VIEW HighSalaryEmployees AS
SELECT e.name, e.salary, d.dept_name
FROM Employee e
JOIN Department d ON e.dept_id = d.dept_id
WHERE e.salary >= 5000000;

-- 테이블 수정
ALTER TABLE Employee ADD COLUMN phone VARCHAR(20);
ALTER TABLE Employee MODIFY COLUMN salary DECIMAL(12,2);
ALTER TABLE Employee DROP COLUMN phone;
```

#### 9. 성능 최적화 기본
```sql
-- EXPLAIN으로 실행 계획 확인
EXPLAIN SELECT * FROM Employee WHERE salary > 4000000;

-- 인덱스 활용
-- 좋음: 인덱스 컬럼을 그대로 비교
WHERE salary > 4000000

-- 나쁨: 함수 적용 시 인덱스 무효화
WHERE YEAR(hire_date) = 2024  -- 풀 스캔
-- 대신:
WHERE hire_date >= '2024-01-01' AND hire_date < '2025-01-01'

-- 커버링 인덱스: SELECT 컬럼이 인덱스에 모두 포함
CREATE INDEX idx_cover ON Employee(dept_id, salary, name);
SELECT name, salary FROM Employee WHERE dept_id = 1;  -- 인덱스만 탐색
```

---

### Ⅲ. 기술 비교 분석

#### 10. 장단점
| 장점 | 단점 |
|-----|------|
| 표준 언어 (이식성) | 복잡한 쿼리 작성 어려움 |
| 선언적 (무엇을 가져올지만 명시) | 절차적 사고 전환 필요 |
| 강력한 집계/분석 | ORM과 N+1 문제 |
| 인덱스로 빠른 검색 | 비정형 데이터 처리 한계 |

---

### Ⅳ. 실무 적용 방안

#### 11. 실무에선? (기술사적 판단)
- **실행 계획 분석**: EXPLAIN으로 쿼리 병목 파악
- **인덱스 설계**: 카디날리티, 선택도 고려
- **쿼리 튜닝**: WHERE절, JOIN 순서, 서브쿼리→조인 변환
- **페이징**: LIMIT+OFFSET보다 Keyset 페이징
- **ORM**: 편의성 vs 세밀한 제어 트레이드오프

---

### Ⅴ. 기대 효과 및 결론


| 효과 영역 | 내용 | 정량적 목표 |
|---------|-----|-----------|
| **데이터 무결성** | ACID 트랜잭션·정규화로 데이터 정합성 보장 | 데이터 이상 현상(Anomaly) 100% 방지 |
| **쿼리 성능** | 인덱스·쿼리 최적화로 데이터 조회 속도 향상 | 응답 시간 90% 단축 |
| **확장성** | 분산 DB·NewSQL로 대용량 트래픽 수평 확장 | TPS 10배 이상 향상 |

#### 결론
> **SQL (Structured Query Language)**은(는) 데이터베이스는 HTAP(하이브리드 거래·분석 처리)와 AI 통합(벡터 DB, RAG 파이프라인)으로 진화하며, 단순 저장소를 넘어 비즈니스 인텔리전스의 핵심 엔진이 될 것이다.

> **※ 참고 표준**: IEEE 754, SQL:2023 표준, ISO/IEC 9075, MongoDB Atlas 아키텍처

---

## 어린이를 위한 종합 설명

**SQL를 쉽게 이해해보자!**

> 관계형 데이터베이스를 조작하는 표준 언어. DDL(정의), DML(조작), DCL(제어), TCL(트랜잭션)로 분류. 조인, 서브쿼리, 윈도우 함수가 실무의 핵심이다.

```
왜 필요할까?
  기존 방식의 한계를 넘기 위해

어떻게 동작하나?
  복잡한 문제 → SQL 적용 → 더 빠르고 안전한 결과!

핵심 한 줄:
  SQL = 똑똑하게 문제를 해결하는 방법
```

> **비유**: SQL은 마치 요리사가 레시피를 따르는 것과 같아.
> 혼란스러운 재료들을 정해진 순서대로 조합하면 → 맛있는 요리(최적 결과)가 나오지! 🍳

---
