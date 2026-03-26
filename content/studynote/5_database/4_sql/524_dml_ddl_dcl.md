+++
title = "DML, DDL, DCL"
description = "SQL의 세 가지 하위 언어 분류"
date = 2026-03-26
weight = 24

[taxonomies]
tags = ["database", "sql", "dml", "ddl", "dcl"]
+++

# DML, DDL, DCL

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL은 목적에 따라 DML (데이터 조작), DDL (데이터 정의), DCL (데이터 제어)로 분류되며, 이 세 가지가 상호 보완적으로 작동하여 데이터베이스를 관리한다.
> 2. **가치**: DML로 데이터CRUD를, DDL로 스키마를 정의하며, DCL로 보안을 관리하여 체계적인 데이터베이스 운영이 가능하다.
> 3. **융합**: DevOps에서 DDL은 마이그레이션 도구 (Flyway, Liquibase)로 관리되고, DML은 ORM 프레임워크에서自動生成되어 사용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### SQL의 분류

SQL (Structured Query Language)는 데이터베이스를 操作하는 언어로서, 크게 세 가지 하위 언어로 분류된다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SQL의 세 가지 하위 언어                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                         SQL                                  │  │
│   │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐  │  │
│   │  │      DDL        │ │      DML        │ │     DCL     │  │  │
│   │  │ (데이터 정의)    │ │ (데이터 조작)    │ │  (데이터 제어) │  │  │
│   │  │                 │ │                 │ │              │  │  │
│   │  │ • CREATE        │ │ • SELECT        │ │ • GRANT     │  │  │
│   │  │ • ALTER         │ │ • INSERT        │ │ • REVOKE    │  │  │
│   │  │ • DROP          │ │ • UPDATE        │ │              │  │  │
│   │  │ • TRUNCATE      │ │ • DELETE       │ │              │  │  │
│   │  └─────────────────┘ └─────────────────┘ └─────────────┘  │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DDL (Data Definition Language)은 테이블, 인덱스, 뷰 등 데이터베이스의 구조 (스키마)를 정의한다. DML (Data Manipulation Language)은 데이터의 조회와增删改查 (CRUD)를 수행한다. DCL (Data Control Language)은 사용자 권한과 보안을 관리한다. 이 세 가지는 서로 다른 역할을担當하며, 함께 사용될 때 비로소 데이터베이스를 체계적으로 管理할 수 있다.

### 비유

SQL의 세 가지 하위 언어는 **도서관 관리 시스템**과 같다. DDL은 도서관의 구조 (서가 배치, 분류 체계)를 정의하고, DML은 책의 대출/반납/조회를 수행하며, DCL은 사서와 이용자의 권한 (어떤 자료를 열람할 수 있는지)을 관리한다.

- **📢 섹션 요약 비유:**建築에서 설계도 (DDL), 실제 건축 작업 (DML), 안전 검사 및 허가 (DCL)로 역할이 나누어져 있듯이, SQL도 정의/조작/제어로 역할이分工되어 있습니다.

---

## Ⅱ. DDL (Data Definition Language)

DDL은 **데이터베이스 객체의 구조를 정의**하는 언어다.

### 주요 DDL 명령어

| 명령어 | 설명 | 예시 |
|:---|:---|:---|
| **CREATE** | 객체 생성 | CREATE TABLE customers (...) |
| **ALTER** | 객체 수정 | ALTER TABLE customers ADD email VARCHAR(100) |
| **DROP** | 객체 삭제 | DROP TABLE customers |
| **TRUNCATE** | 데이터만 전체 삭제 | TRUNCATE TABLE customers |
| **RENAME** | 객체 이름 변경 | RENAME TABLE customers TO clients |

### CREATE TABLE 예시

```sql
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(20) DEFAULT '서울',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ALTER TABLE 예시

```sql
-- 열 추가
ALTER TABLE customers ADD phone VARCHAR(20);

-- 열 수정
ALTER TABLE customers MODIFY email VARCHAR(200) NOT NULL;

-- 열 삭제
ALTER TABLE customers DROP COLUMN phone;

-- 제약조건 추가
ALTER TABLE customers ADD CONSTRAINT chk_email
    CHECK (email LIKE '%@%');
```

### DROP vs TRUNCATE

| 명령어 | 동작 | 롤백 | 초기화 여부 |
|:---|:---|:---|:---|
| **DROP** | 테이블 자체 삭제 | 불가 (COMMIT 필요) | 테이블 삭제 |
| **TRUNCATE** | 데이터만 삭제 | 불가 (DLL) | 테이블 구조는 유지 |

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DDL 명령어의 특성                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   DDL vs DML의 핵심 차이:                                            │
│                                                                     │
│   DDL (CREATE, ALTER, DROP):                                          │
│   • AUTO COMMIT (실행 즉시 확정)                                      │
│   • 롤백 불가                                                        │
│   • 시스템 카탈로그 자동 갱신                                         │
│                                                                     │
│   DML (INSERT, UPDATE, DELETE):                                       │
│   • 명시적 COMMIT 필요                                              │
│   • 롤백 가능                                                        │
│   • 데이터 변경のみ                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. DML (Data Manipulation Language)

DML은 **데이터를 조작**하는 언어다.

### 주요 DML 명령어

| 명령어 | 설명 | 예시 |
|:---|:---|:---|
| **SELECT** | 데이터 조회 | SELECT * FROM customers |
| **INSERT** | 데이터 삽입 | INSERT INTO customers VALUES (...) |
| **UPDATE** | 데이터 수정 | UPDATE customers SET city='부산' WHERE ... |
| **DELETE** | 데이터 삭제 | DELETE FROM customers WHERE ... |

### INSERT 예시

```sql
-- 방법 1: 모든 열에 값 삽입
INSERT INTO customers VALUES ('C001', '김철수', 'kim@test.com', '서울');

-- 방법 2: 열 목록과 함께
INSERT INTO customers (customer_id, name, email, city)
VALUES ('C002', '이영희', 'lee@test.com', '부산');

-- 방법 3: 서브쿼리로부터 삽입
INSERT INTO customers (customer_id, name, city)
SELECT supplier_id, supplier_name, '서울'
FROM suppliers;
```

### UPDATE 예시

```sql
-- 조건부 수정
UPDATE customers
SET city = '인천', email = 'newemail@test.com'
WHERE customer_id = 'C001';
```

### DELETE vs TRUNCATE

| 명령어 | 동작 | 롤백 | 성능 |
|:---|:---|:---|:---|
| **DELETE** | 조건에 맞는 행만 삭제 | 가능 (COMMIT前) | 상대적으로 느림 (로깅) |
| **TRUNCATE** | 전체 데이터 삭제 | 불가 | 상대적으로 빠름 (alloc解除) |

---

## Ⅳ. DCL (Data Control Language)

DCL은 **데이터베이스의 접근 권한과 보안을 관리**하는 언어다.

### 주요 DCL 명령어

| 명령어 | 설명 | 예시 |
|:---|:---|:---|
| **GRANT** | 권한 부여 | GRANT SELECT ON customers TO user1 |
| **REVOKE** | 권한 취소 | REVOKE SELECT ON customers FROM user1 |

### GRANT 예시

```sql
-- SELECT 권한 부여
GRANT SELECT ON customers TO user1;

-- 여러 권한 부여
GRANT SELECT, INSERT, UPDATE ON customers TO user2;

-- 모든 권한 부여 (DBA)
GRANT ALL PRIVILEGES ON customers TO admin1;

-- WITH GRANT OPTION (다른 사용자에게도 부여 가능)
GRANT SELECT ON customers TO user3 WITH GRANT OPTION;
```

### REVOKE 예시

```sql
-- 권한 취소
REVOKE SELECT ON customers FROM user1;

-- GRANT OPTION만 취소
REVOKE GRANT OPTION FOR SELECT ON customers FROM user3;
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                    권한 계층 구조                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                      DBA (전체 관리자)                         │  │
│   │  • 모든 테이블에 대한 모든 권한                                 │  │
│   │  • 사용자 생성/삭제                                             │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              │                                        │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                      응용 程序 계정                             │  │
│   │  • 업무에 필요한 테이블에 대한 CRUD 권한                       │  │
│   │  • DDL 권한은 없음 (스키마 변경 불가)                          │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              │                                        │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                      읽기 전용 계정                            │  │
│   │  • SELECT 권한만 부여                                          │  │
│   │  • INSERT/UPDATE/DELETE 권한 없음                            │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. TCL (Transaction Control Language)

보통 DCL과 함께 언급되는 TCL은 **트랜잭션을 관리**하는 언어다.

| 명령어 | 설명 |
|:---|:---|
| **COMMIT** | 트랜잭션 완료 확정 |
| **ROLLBACK** | 트랜잭션 취소 |
| **SAVEPOINT** | 트랜잭션 내 중간 저장점 |

```sql
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 10000 WHERE account_id = 'A';
UPDATE accounts SET balance = balance + 10000 WHERE account_id = 'B';

-- 둘 다 성공하면 확정
COMMIT;

-- 문제 발생 시 모두 취소
-- ROLLBACK;
```

- **📢 섹션 요약 비유:**편집장에서 작성 (DML) 후 저장 (COMMIT)하거나, 保存취소 (ROLLBACK)하는 것과 같습니다. 설계도 변경 (DDL)은 저장 없이 바로 적용됩니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **COMMIT** | DML의 결과를 영구적으로 저장하는 TCL 명령이다. |
| **ROLLBACK** | DML의 변경을 취소하는 TCL 명령이다. |
| **스키마** | DDL로 정의되는 데이터베이스 구조다. |
| **권한** | DCL로 관리되는 사용자별 접근 제어다. |
| **트랜잭션** | DML 연산의 논리적 단위로, TCL로 관리된다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. DDL은 **玩具설명서**와 같아요. "이 부품은 이렇게 만들고, 저 부품은 이렇게组装해"라는指示예요.
2. DML은 **玩具로 놀이**하는 것과 같아요. 부품을 붙이고 (INSERT), 빼고 (DELETE), 바꿔 (UPDATE)游乐场에서 놀이하는 거예요.
3. DCL은 **놀이터 규칙**과 같아요. "이 놀이기는 누구나 탈 수 있고 (GRANT), 여기는小孩子만 탈 수 있어" (REVOKE)라는 규칙이에요.
