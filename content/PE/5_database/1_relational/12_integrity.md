+++
title = "12. 무결성 제약 (Integrity Constraints)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["Integrity-Constraints", "Entity-Integrity", "Referential-Integrity", "Domain-Integrity", "ACID"]
draft = false
+++

# 무결성 제약 (Integrity Constraints)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 무결성 제약은 **"데이터베이스에 저장된 데이터의 정확성(Accuracy), 일관성(Consistency), 신뢰성(Reliability)을 보장하는 규칙"**으로, **개체 무결성(Entity Integrity)**, **참조 무결성(Referential Integrity)**, **도메인 무결성(Domain Integrity)**, **사용자 정의 무결성(User-defined Integrity)**으로 구분된다.
> 2. **가치**: **무결성 제약조건(Integrity Constraint)**을 통해 **데이터 이상(Data Anomaly)**을 방지하고, **기본키(PK)**와 **외래키(FK)**로 **개체 간 관계**를 보장하며, **트랜잭션(Transaction)**의 **ACID 속성** 중 **Consistency(일관성)**를 실현한다.
> 3. **융합**: **정규화(Normalization)**의 목표를 실현하는 수단으로 **함수적 종속(Functional Dependency)**를 기반으로 제1정규형~제5정규형까지의 무결성 보장을 하며, **ORM 매핑**, **REST API**의 **데이터 검증(Validation)**, **마이크로서비스**의 **분산 트랜잭션(Distributed Transaction)**의 기초가 된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
무결성 제약(Integrity Constraints)은 **"데이터베이스의 데이터가 항상 올바르고 일관되게 유지되도록 보장하는 규칙"**이다.

**무결성의 정의 (Codd, 1985)**:
- 데이터 무결성: 저장된 데이터가 정확하고 일관되어야 함
- 제약조건: 데이터 조작 시 위반 여부 검사 규칙

### 💡 비유
무결성 제약은 **"게임 규칙"**과 같다.
- **바둑**: 두 번 둔 곳은 다시 둘 수 없음
- **데이터**: 중복 주민번호 없음, 부서 없는 사원 없음

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         무결성 제약의 필요성                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

파일 시스템:
    • 데이터 중복, 불일치
    • 프로그램이 검증 책임
    • 오류 데이터 삽입 용이
         ↓
관계형 모델 (1970년):
    • 개체 무결성: PK 무결성
    • 참조 무결성: FK 무결성
    • DBMS가 자동 검증
         ↓
SQL 표준 (SQL-92):
    • PRIMARY KEY, FOREIGN KEY
    • UNIQUE, CHECK, NOT NULL
    • 제약조건 정의 표준화
         ↓
현대 데이터베이스:
    • 복합 제약조건
    • 트리거(Trigger) 기반 무결성
    • 분산 트랜잭션 (2PC)
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4대 무결성 제약

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         데이터 무결성 4대 제약                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. 개체 무결성 (Entity Integrity)                                                     │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  정의: 릴레이션 내 각 튜플은 유일하게 식별 가능해야 함                               │  │
    │  │                                                                                     │  │
    │  │  [PRIMARY KEY 제약조건]                                                             │  │
    │  │  CREATE TABLE employees (                                                          │  │
    │  │      employee_id INT PRIMARY KEY,  -- 개체 무결성 보장                               │  │
    │  │      name VARCHAR(100),                                                            │  │
    │  │      ...                                                                            │  │
    │  │  );                                                                                 │  │
    │  │                                                                                     │  │
    │  │  [무결성 규칙]                                                                       │  │
    │  │  • NULL 값 불가: PK 컬럼은 NULL 불가                                                │  │
    │  │  • 유일성: PK 값은 중복 불가                                                        │  │
    │  │  • 예시: employee_id = 101, 102, 103 (각각 유일)                                    │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
    │  2. 참조 무결성 (Referential Integrity)                                                 │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  정의: 외래키는 참조하는 릴레이션의 존재하는 튜플만 가리켜야 함                         │  │
    │  │                                                                                     │  │
    │  │  [FOREIGN KEY 제약조건]                                                             │  │
    │  │  CREATE TABLE orders (                                                             │  │
    │  │      order_id INT PRIMARY KEY,                                                     │  │
    │  │      customer_id INT,                                                              │  │
    │  │      FOREIGN KEY (customer_id)                                                     │  │
    │  │          REFERENCES customers(id)                                                  │  │
    │  │          ON DELETE CASCADE                                                         │  │
    │  │          ON UPDATE CASCADE                                                         │  │
    │  │  );                                                                                 │  │
    │  │                                                                                     │  │
    │  │  [무결성 규칙]                                                                       │  │
    │  │  • 참조 무결성: orders.customer_id는 customers.id에 존재해야 함                      │  │
    │  │  • NULL 허용: FK는 NULL일 수 있음 (미참조)                                          │  │
    │  │  • 연쇄 동작: ON DELETE/UPDATE 시 CASCADE, SET NULL, RESTRICT                        │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
    │  3. 도메인 무결성 (Domain Integrity)                                                   │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  정의: 속성값은 정의된 도메인(값의 허용 범위)에 속해야 함                              │  │
    │  │                                                                                     │  │
    │  │  [CHECK, NOT NULL, DEFAULT 제약조건]                                                │  │
    │  │  CREATE TABLE products (                                                           │  │
    │  │      product_id INT PRIMARY KEY,                                                   │  │
    │  │      price DECIMAL(10,2) CHECK (price >= 0),      -- 가격은 0 이상                    │  │
    │  │      quantity INT NOT NULL,                        -- 수량은 NULL 불가               │  │
    │  │      category VARCHAR(50) DEFAULT 'general',        -- 기본값 설정                    │  │
    │  │      email VARCHAR(255) CHECK (email LIKE '%@%')   -- 이메일 형식                     │  │
    │  │  );                                                                                 │  │
    │  │                                                                                     │  │
    │  │  [무결성 규칙]                                                                       │  │
    │  │  • 타입 검사: INT, VARCHAR, DATE 등                                                  │  │
    │  │  • 길이 제한: VARCHAR(n)                                                             │  │
    │  │  • 값 범위: CHECK 제약조건                                                           │  │
    │  │  • NULL 허용: NOT NULL 제약                                                          │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
    │  4. 사용자 정의 무결성 (User-defined Integrity)                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  정의: 비즈니스 규칙에 따른 특정 제약조건                                             │  │
    │  │                                                                                     │  │
    │  │  [복합 CHECK 제약조건]                                                              │  │
    │  │  CREATE TABLE employees (                                                          │  │
    │  │      employee_id INT PRIMARY KEY,                                                   │  │
    │  │      birth_date DATE,                                                              │  │
    │  │      hire_date DATE,                                                               │  │
    │  │      salary DECIMAL(10,2),                                                         │  │
    │  │      CHECK (hire_date >= birth_date + INTERVAL '18 years'),  -- 입사 나이 제한      │  │
    │  │      CHECK (salary > 0)                                                            │  │
    │  │  );                                                                                 │  │
    │  │                                                                                     │  │
    │  │  [TRIGGER 기반 무결성]                                                              │  │
    │  │  CREATE TRIGGER update_salary_before                                                │  │
    │  │      BEFORE UPDATE ON employees                                                     │  │
    │  │      FOR EACH ROW                                                                   │  │
    │  │  BEGIN                                                                              │  │
    │  │      IF NEW.salary < OLD.salary THEN                                                │  │
    │  │          SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary cannot decrease';       │  │
    │  │      END IF;                                                                        │  │
    │  │  END;                                                                               │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 정교한 무결성 제약 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         제약조건 위반 시 동작                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [삽입 연산 시 무결성 검사]

    INSERT INTO orders (order_id, customer_id) VALUES (1001, 999);
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  DBMS 무결성 검사 엔진                                                                   │
    │                                                                                         │
    │  1. 개체 무결성 검사                                                                     │
    │     • order_id = 1001 → PK 중복 여부 확인                                                │
    │     • 1001이 기존 orders에 없음 → ✓                                                     │
    │                                                                                         │
    │  2. 참조 무결성 검사                                                                     │
    │     • customer_id = 999 → customers 테이블에 존재 여부 확인                              │
    │     • customers.id = 999 없음 → ✗ 참조 무결성 위반                                       │
    │                                                                                         │
    │  3. 도메인 무결성 검사                                                                   │
    │     • customer_id 타입: INT → ✓                                                         │
    │     • customer_id NULL 여부: NOT NULL 제약 없음 → ✓                                      │
    │                                                                                         │
    │  4. 사용자 정의 무결성 검사                                                              │
    │     • CHECK 제약조건: 없음 → ✓                                                           │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  결과: 참조 무결성 위반으로 INSERT 거부                                                  │
    │  • Error: Foreign key constraint failed                                                │
    │  • Message: Cannot add or update a child row: foreign key constraint fails             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [삭제 연산 시 무결성 검사와 CASCADE]

    DELETE FROM customers WHERE id = 10;
                      │
                      ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  참조 무결성 검사                                                                         │
    │                                                                                         │
    │  • orders 테이블에서 customer_id = 10 인 행 존재 여부 확인                                │
    │                                                                                         │
    │  [ON DELETE CASCADE 설정 시]                                                            │
    │  1. orders에서 customer_id = 10인 모든 행 삭제                                          │
    │  2. customers에서 id = 10인 행 삭제                                                     │
    │  3. ✓ 참조 무결성 유지                                                                   │
    │                                                                                         │
    │  [ON DELETE RESTRICT 설정 시]                                                           │
    │  1. 참조하는 행 존재 → 삭제 거부                                                          │
    │  2. ✗ Error: Cannot delete parent row                                                   │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 외래키 동작 옵션

| 옵션 | 설명 | 사용 사례 |
|------|------|----------|
| **CASCADE** | 참조 행 함께 삭제/갱신 | 주문-주문항목 |
| **SET NULL** | FK를 NULL로 설정 | 선택적 참조 |
| **SET DEFAULT** | FK를 기본값으로 설정 | 기본 부서 지정 |
| **RESTRICT/NO ACTION** | 삭제/갱신 금지 | 중요 데이터 |

---

## Ⅲ. 융합 비교 및 다각도 분석

### DBMS별 무결성 제약 구현

| DBMS | DECLARE CONSTRAINT | TRIGGER | CHECK 제약 |
|------|-------------------|---------|------------|
| **PostgreSQL** | ✓ | ✓ | ✓ (복합 가능) |
| **MySQL** | ✓ | ✓ | ✓ (제한적) |
| **Oracle** | ✓ | ✓ | ✓ |
| **SQL Server** | ✓ | ✓ | ✓ |

### 과목 융합 관점 분석

#### 1. 정규화 ↔ 무결성 제약
- **2NF**: 부분적 함수 종속 제거 → 개체 무결성
- **3NF**: 이행적 함수 종속 제거 → 참조 무결성
- **BCNF**: 모든 결정자가 후보키

#### 2. 트랜잭션 ↔ 무결성
- **Consistency**: 무결성 제약 준수
- **Isolation**: 동시성 제어로 무결성 보호
- **Durability**: 커밋 후 무결성 영속

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 전자상거래 주문 무결성 설계
**상황**: 주문, 고객, 상품, 재고 관리
**판단**:
1. **개체 무결성**: 각 테이블 PK 정의
2. **참조 무결성**: FK로 테이블 간 관계 보장
3. **비즈니스 무결성**: 재고 ≤ 주문 수량 제약

```sql
-- 주문 테이블
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 주문 항목 테이블 (복합 무결성)
CREATE TABLE order_items (
    order_id INT,
    item_seq INT,
    product_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, item_seq),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 재고 무결성 (트리거)
CREATE TRIGGER check_inventory
BEFORE INSERT ON order_items
FOR EACH ROW
BEGIN
    DECLARE available INT;
    SELECT quantity INTO available FROM inventory WHERE product_id = NEW.product_id;
    IF available < NEW.quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient inventory';
    END IF;
END;
```

---

## Ⅴ. 기대효과 및 결론

### 무결성 제약 기대 효과

| 무결성 유형 | 위반 시 영향 | 보장 시 효과 |
|-----------|-------------|-------------|
| **개체 무결성** | 중복 데이터, 식별 불가 | 유일 식별 보장 |
| **참조 무결성** | 고아 레코드, 불일치 | 관계 일관성 |
| **도메인 무결성** | 잘못된 데이터 | 데이터 타입 보장 |
| **사용자 정의** | 비즈니스 위반 | 규칙 준수 |

### 미래 전망

1. **선언적 무결성**: SQL 제약조건 확장
2. **애플리케이션 검증**: API Gateway에서 검증
3. **분산 무결성**: Saga 패턴, 2PC

### ※ 참고 표준/가이드
- **SQL-92**: Integrity constraints
- **Codd's 12 Rules**: Rule 6-View, Rule 7-High-level Insert
- **ACID**: Transaction properties

---

## 📌 관련 개념 맵

- [키](./11_key.md) - 무결성 보장의 기본
- [스키마](./5_schema.md) - 제약조건 정의
- [정규화](../2_relational/) - 무결성 기반 설계
- [트랜잭션](../3_transaction/) - 무결성 유지 메커니즘
