+++
title = "3. DBMS 언어 (DDL, DML, DCL, TCL)"
date = 2026-03-05
categories = ["studynotes-database"]
tags = ["DDL", "DML", "DCL", "TCL", "SQL", "Database-Language"]
draft = false
+++

# DBMS 언어 (DDL, DML, DCL, TCL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL(Structured Query Language)은 관계형 데이터베이스의 국제 표준 언어로, 데이터 정의(DDL), 조작(DML), 제어(DCL), 트랜잭션 제어(TCL)의 4가지 범주로 구성된 데이터베이스 운영의 인터페이스이다.
> 2. **가치**: 선언적(Declarative) 언어로 "어떻게(How)"가 아닌 "무엇을(What)" 원하는지 명시하여 옵티마이저가 최적의 실행 계획을 수립하게 하며, 데이터 독립성과 이식성을 보장한다.
> 3. **융합**: 응용 프로그램 개발(ORM), 데이터 분석(SQL 기반), 데이터 엔지니어링(ETL), 보안(접근 제어)의 기초이며, NoSQL의 쿼리 언어와 현대적 쿼리 엔진(Fluent, LINQ, JPA Criteria)의 모델이 되었다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
DBMS 언어는 데이터베이스를 정의, 조작, 제어하기 위한 언어 체계이다. 가장 대표적인 **SQL(Structured Query Language)**은 1974년 IBM 연구소에서 개발된 SEQUEL(Structured English QUEry Language)에서 유래했다.

### 💡 비유
DBMS 언어는 **"건물의 설계, 시공, 사용, 관리를 위한 언어"**와 같다.
- **DDL(정의 언어)**: 건축 도면, 설계서 작성 (CREATE, ALTER, DROP)
- **DML(조작 언어)**: 짐을 나르고, 정리하고, 찾기 (SELECT, INSERT, UPDATE, DELETE)
- **DCL(제어 언어어)**: 키 주고, 출입 통제 (GRANT, REVOKE)
- **TCL(트랜잭션 제어)**: 작업 확정, 취소 (COMMIT, ROLLBACK, SAVEPOINT)

### 등장 배경 및 발전 과정

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         SQL 표준화 역사                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

1970년대: E.F. Codd, 관계형 모델 제안
         ↓
1974년: IBM SEQUEL (Structured English QUEry Language) 개발
         ↓
1979년: Oracle V2 (상용 SQL DBMS 최초)
         ↓
1986년: ANSI SQL-86 (첫 표준)
         ↓
1989년: ANSI SQL-89 (기본 기능)
         ↓
1992년: ANSI SQL-92 (확장 기능, 현재 가장 널리 사용)
         ↓
1999년: ANSI SQL-99 (저장프로시저, 트리거 등)
         ↓
2003년: ANSI SQL:2003 (XML, 윈도우 함수)
         ↓
2008년: ANSI SQL:2008 (TRUNCATE, 향상된 기능)
         ↓
2011년: ANSI SQL:2011 (임시 DB, temporal 기능)
         ↓
2016년: ANSI SQL:2016 (JSON, 행 패턴 매칭)
         ↓
2023년: ANSI SQL:2023 (JSON 제약, 마이그레이션)
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4대 언어 범주

| 범주 | 영문 명칭 | 설명 | 주요 명령어 | 비유 |
|------|----------|------|------------|------|
| **DDL** | Data Definition Language | 데이터 구조 정의 | CREATE, ALTER, DROP, TRUNCATE | 건축 설계 |
| **DML** | Data Manipulation Language | 데이터 조작 | SELECT, INSERT, UPDATE, DELETE | 물건 이동 |
| **DCL** | Data Control Language | 데이터 제어(권한) | GRANT, REVOKE | 출입 통제 |
| **TCL** | Transaction Control Language | 트랜잭션 제어 | COMMIT, ROLLBACK, SAVEPOINT | 확정/취소 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         SQL 4대 언어 계층 구조                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [사용자/응용 프로그램]
              │
              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            SQL 명령어                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │  [DDL: Data Definition Language] - 데이터 구조 정의                          │  │
│  │                                                                              │  │
│  │  CREATE TABLE employees (                                                   │  │
│  │    id INT PRIMARY KEY,                                                      │  │
│  │    name VARCHAR(100) NOT NULL,                                              │  │
│  │    salary DECIMAL(10,2)                                                    │  │
│  │  );                                                                        │  │
│  │                                                                              │  │
│  │  ALTER TABLE employees ADD COLUMN dept_id INT;                              │  │
│  │  DROP TABLE old_employees;                                                  │  │
│  │  TRUNCATE TABLE temp_data;  ← 롤백 불가, DDL/DML 경계                       │  │
│  │                                                                              │  │
│  │  특징: 자동 커밋(Auto-commit)되며, 롤백 불가                                │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │  [DML: Data Manipulation Language] - 데이터 조작                            │  │
│  │                                                                              │  │
│  │  -- 조회 (Query)                                                            │  │
│  │  SELECT id, name, salary FROM employees WHERE salary > 50000;                │  │
│  │                                                                              │  │
│  │  -- 삽입 (Insert)                                                           │  │
│  │  INSERT INTO employees (id, name, salary) VALUES (1, '홍길동', 60000);      │  │
│  │                                                                              │  │
│  │  -- 갱신 (Update)                                                           │  │
│  │  UPDATE employees SET salary = salary * 1.1 WHERE dept_id = 10;              │  │
│  │                                                                              │  │
│  │  -- 삭제 (Delete)                                                           │  │
│  │  DELETE FROM employees WHERE id = 999;                                      │  │
│  │                                                                              │  │
│  │  특징: 트랜잭션 내에서 실행, 롤백 가능                                       │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │  [DCL: Data Control Language] - 데이터 제어 (권한)                          │  │
│  │                                                                              │  │
│  │  -- 권한 부여                                                              │  │
│  │  GRANT SELECT, INSERT ON employees TO user_app;                              │  │
│  │  GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';                          │  │
│  │                                                                              │  │
│  │  -- 권한 회수                                                              │  │
│  │  REVOKE DELETE ON employees FROM user_temp;                                  │  │
│  │                                                                              │  │
│  │  특징: DDL과 유사하게 자동 커밋                                             │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │  [TCL: Transaction Control Language] - 트랜잭션 제어                        │  │
│  │                                                                              │  │
│  │  BEGIN TRANSACTION;  -- 또는 START TRANSACTION                              │  │
│  │                                                                              │  │
│  │  UPDATE accounts SET balance = balance - 1000 WHERE id = 1;                  │  │
│  │  UPDATE accounts SET balance = balance + 1000 WHERE id = 2;                  │  │
│  │                                                                              │  │
│  │  COMMIT;  -- 트랜잭션 확정, 영구 반영                                       │  │
│  │  -- 또는 --                                                                │  │
│  │  ROLLBACK;  -- 트랜잭션 취소, 이전 상태로 복원                                │  │
│  │                                                                              │  │
│  │  SAVEPOINT sp1;  -- 중간 저장점 설정                                         │  │
│  │  ROLLBACK TO sp1;  -- 저장점까지 롤백                                      │  │
│  │                                                                              │  │
│  │  특징: ACID 트랜잭션 보장의 핵심                                             │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
              │
              ▼
    [DBMS 엔진 처리]
    ┌──────────────────────────────────────────────────────────────────────────────┐
    │  파서(Parser) → 옵티마이저(Optimizer) → 실행기(Executor) → 스토리지 엔진       │
    │                                                                              │
    │  DDL: 데이터 딕셔너리 갱신, 스키마 잠금                                   │
    │  DML: 트랜잭션 관리자, 버퍼 풀, 실행 계획                                  │
    │  DCL: 보안 관리자, 권한 테이블 확인                                         │
    │  TCL: 트랜잭션 관리자, WAL 로그, 커밋/롤백                                  │
    └──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### 1. DDL (Data Definition Language)

**특징**:
- 스키마(데이터 구조)를 정의/수정/삭제
- **자동 커밋(Auto-commit)**: 실행 즉시 영구 반영
- **롤백 불가**: DDL은 트랜잭션으로 묶을 수 없음 (대부분 DBMS)
- **데이터 딕셔너리 갱신**: 메타데이터 수정

**DDL 명령어 실행 과정**:
```text
DDL: CREATE TABLE employees (...)
    ↓
[1] 파서: SQL 구문 분석
    ↓
[2] 시스템 카탈로그 확인: 이름 중복 검사
    ↓
[3] 스키마 락(Lock) 획득
    ↓
[4] 공간 할당: 테이블스페이스에 extent 할당
    ↓
[5] 데이터 딕셔너리 갱신: SYS.TABLES, SYS.COLUMNS 등
    ↓
[6] 자동 커밋
    ↓
[7] 락 해제
```

**TRUNCATE vs DELETE**:
| 비교 항목 | TRUNCATE | DELETE |
|----------|----------|--------|
| **형식** | DDL | DML |
| **속도** | 빠름 (페이지/extent 해제만) | 느림 (행 단위 삭제) |
| **롤백** | 불가능 | 가능 |
| **트리거** | 발생 안 함 | 발생 |
| **로그** | 최소 로그 | 전체 로그 |
| **WHERE** | 불가능 | 가능 |

#### 2. DML (Data Manipulation Language)

**SELECT 질의 처리 과정**:
```text
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.id
WHERE e.salary > 50000
ORDER BY e.name;

    ↓
[1] 파싱: SQL 구문 트리 생성
    ↓
[2] 바인딩: 변수, 타입 확인
    ↓
[3] 최적화: 실행 계획 생성
    - 조인 순서 결정
    - 인덱스 사용 여부
    - 조인 알고리즘 선택 (NL, SortMerge, Hash)
    ↓
[4] 실행: 실행 계획에 따라 데이터 추출
    ↓
[5] 결과 반환: 클라이언트에 전달
```

#### 3. TCL (Transaction Control Language)

**트랜잭션 경계**:
```text
    ┌─────────────────────────────────────────────────────────┐
    │  TCL: 트랜잭션 경계                                   │
    │                                                        │
    │  BEGIN TRANSACTION;  ← 트랜잭션 시작 (묵시적 시작)    │
    │  ┌─────────────────────────────────────────────┐       │
    │  │  [트랜잭션 내 DML 명령어]                    │       │
    │  │  INSERT ...                                   │       │
    │  │  UPDATE ...                                   │       │
    │  │  DELETE ...                                   │       │
    │  │                                               │       │
    │  │  아직 커밋 안 됨 (미확정 상태)                │       │
    │  └─────────────────────────────────────────────┘       │
    │         │                                              │
    │         ▼                                              │
    │  COMMIT;  ────→  영구 반영 (확정)                    │
    │  또는                                                │
    │  ROLLBACK; ───→  모든 변경 사항 취소 (원복)            │
    │                                                        │
    └─────────────────────────────────────────────────────────┘
```

**COMMIT과 ROLLBACK의 차이**:
- **COMMIT**: 모든 변경사항을 영구적으로 DB에 반영
  - Redo 로그를 디스크에 플러시 (WAL)
  - 잠금 해제
  - 다른 트랜잭션에서 변경사항 보임
- **ROLLBACK**: 트랜잭션 시작 이전 상태로 복원
  - Undo 로그를 이용한 복구
  - 잠금 해제
  - 변경사항 폐기

---

## Ⅲ. 융합 비교 및 다각도 분석

### SQL vs 절차적 언어

| 비교 항목 | SQL (선언적) | 절차적 언어 (C, Java) |
|----------|-------------|---------------------|
| **지정 방식** | 무엇을(What) 원하는지 | 어떻게(How) 할지 |
| **최적화** | 옵티마이저가 자동 | 개발자가 직접 |
| **이식성** | 높음 (DBMS 독립적) | 낮음 (플랫폼 의존) |
| **복잡도** | 단순한 질의 | 복잡한 알고리즘 구현 |
| **예시** | `SELECT * FROM users` | `for (i=0; i<n; i++) { ... }` |

### 과목 융합 관점 분석

#### 1. 소프트웨어 공학 ↔ SQL
- **ORM(Object-Relational Mapping)**: 객체지향 언어와 SQL 간의 임피던스 불일치 해결
- **SQL Injection**: 동적 SQL 조립 시 보안 취약점 → Prepared Statement 해결

#### 2. 보안 ↔ DCL
- **최소 권한 원칙**: GRANT로 필요한 권한만 부여
- **역할 기반 접근 제어(RBAC)**: ROLE로 권한 묶어서 관리

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 대용량 DELETE 최적화
**상황**: 1억 건의 이력 데이터에서 1년 이상된 데이터 5000만 건 삭제 필요
**판단**:
1. **DELETE 사용 시**: 너무 느리고, 트랜잭션 로그 과다, 롤백 세그먼트 폭발
2. **TRUNCATE는 불가**: 전체 삭제만 가능
3. **최적 해결책**:
   - 파티션 테이블 사용: `ALTER TABLE DROP PARTITION old_data`
   - 배치 DELETE: 1만 건 단위로 커밋
   - CTAS(Create Table As Select): 신규 테이블 생성 후 교체

### 도입 시 고려사항 (체크리스트)

**기술적**:
- [ ] DDL 자동 커밋에 따른 스키마 변경 롤백 방안
- [ ] TCL 트랜잭션 경계 명확화 (롱 트랜잭션 방지)
- [ ] DCL 권한 정책: 최소 권한, 역할 분리

**운영적**:
- [ ] 운영 환경 DDL 실행 절차 (사전 검토, 테스트)
- [ ] 장기간 트랜잭션 모니터링

---

## Ⅴ. 기대효과 및 결론

### SQL 기반 데이터베이스 운영의 이점

| 이점 | 설명 | 효과 |
|------|------|------|
| **선언적 언어** | "무엇을" 원하는지 명시 | 개발 생산성 향상 |
| **데이터 독립성** | 응용 프로그램과 데이터 구조 분리 | 유지보수성 향상 |
| **표준화** | ANSI/ISO 표준 | 이식성 보장 |
| **세트 기반 처리** | 행 단위가 아닌 집합 단위 | 대량 데이터 처리 효율 |

### 미래 전망

1. **SQL의 진화**: NoSQL 쿼리 언어도 SQL 표준 따르는 추세 (SQL++
2. **자연어 질의(NLQ)**: LLM 기반 자연어를 SQL로 변환
3. **스트림 SQL**: 실시간 데이터 처리 (KSQL, Flink SQL)

### ※ 참고 표준/가이드
- **ANSI/ISO SQL Standard**: SQL-92, SQL-99, SQL:2016
- **JDBC/ODBC**: SQL API 표준

---

## 📌 관련 개념 맵

- [스키마](./4_schema.md) - DDL로 정의
- [트랜잭션](../4_transaction/) - TCL로 제어
- [접근 제어](../9_security/) - DCL로 관리
- [SQL 튜닝](./5_sql_optimizer.md) - DML 성능 최적화
