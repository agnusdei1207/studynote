+++
title = "20. ACID (ACID Properties)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["ACID", "Atomicity", "Consistency", "Isolation", "Durability", "Transaction"]
draft = false
+++

# ACID (ACID Properties)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ACID는 **"트랜잭션이 만족해야 하는 **4가지 필수 특성"**으로, **A(Atomicity, 원자성)**는 **All-or-Nothing 실행**, **C(Consistency, 일관성)**는 **데이터 무결성 유지**, **I(Isolation, 격리성)**는 **동시 실행 트랜잭션 간 독립성**, **D(Durability, 지속성)**는 **Commit된 데이터 영구 보존**을 보장한다.
> 2. **가치**: **데이터 무결성(Data Integrity)**을 보장하고 **동시성 제어(Concurrency Control)**로 **이상 현상(Anomaly)**을 방지하며 **장애 복구(Recovery)**로 **시스템 장애** 발생 시에도 **데이터 손실**을 방지한다.
> 3. **융합**: **RDBMS**(Oracle, MySQL, PostgreSQL)는 **ACID를 엄격하게 준수**하며, **NoSQL**(MongoDB, Cassandra)는 **BASE**(Basically Available, Soft state, Eventual consistency) 모델로 **ACID를 완화**하여 **분산 환경**에서의 **확장성**과 **성능**을 우선한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
ACID는 **"트랜잭션이 안전하게 실행되기 위해 만족해야 하는 4가지 특성"**이다.

**ACID의 유래**:
- **1970년대**: System R (IBM)에서 개념 정립
- **1983년**: Härder & Reuter가 ACID 용어 정립

### 💡 비유
ACID는 **"계약 조건"**과 같다.
- **A**: 모든 조건 이행 또는 전무 취소
- **C**: 규정 위반 금지
- **I**: 타 계약과 독립
- **D**: 계약 영구 보존

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         ACID의 필요성                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

초기 파일 시스템:
    • 데이터 중복, 불일치
    • 장애 시 복구 불가
         ↓
ACID 개념 등장:
    • Atomicity: All-or-Nothing
    • Consistency: 무결성 보장
    • Isolation: 동시성 제어
    • Durability: 영구 저장
         ↓
현대 RDBMS:
    • WAL(Write-Ahead Logging)
    • MVCC(Multi-Version Concurrency Control)
    • 2PL(Two-Phase Locking)
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### Atomicity (원자성)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Atomicity: All-or-Nothing                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 트랜잭션의 모든 연산은 **반드시 전부 실행**되거나 **전부 실행되지 않아야 함**                           │
    │  │  • 중간 상태는 시스템에서 볼 수 없음                                                        │
    │                                                                                         │
    │  [이체 예시]                                                                              │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  BEGIN TRANSACTION;                                                                   │  │
    │  │  UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';  -- ① 출금           │  │
    │  │  UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';  -- ② 입금           │  │
    │  │  COMMIT;  -- 둘 다 성공 → 원자적 완료                                                │  │
    │  │                                                                                      │  │
    │  │  또는                                                                                  │  │
    │  │  ROLLBACK;  -- 하나라도 실패 → 전체 취소                                               │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │
    │  [구현 방법]                                                                             │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  • WAL (Write-Ahead Logging): 변경 사항 먼저 기록                                    │  │
    │  │  • Undo Log: ROLLBACK을 위한 변경 전 값                                               │  │
    │  │  • Redo Log: COMMIT 후 디스크 반영을 위한 변경 후 값                                    │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Consistency (일관성)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Consistency: 데이터 무결성                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 트랜잭션 실행 전후에 **데이터베이스는 일관된 상태**를 유지해야 함                                   │
    │  │  • 모든 제약 조건(Constraint)과 규칙(Rule)을 준수                                            │
    │                                                                                         │
    │  [일관성 요소]                                                                           │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  1. 도메인 무결성 (Domain Integrity):                                                 │  │
    │  │     • 데이터 타입, 길이, 형식                                                         │  │
    │  │     • 예: AGE > 0, NAME NOT NULL                                                     │  │
    │  │                                                                                      │  │
    │  │  2. 개체 무결성 (Entity Integrity):                                                   │  │
    │  │     • Primary Key 고유                                                               │  │
    │  │     • 예: ID는 중복 불가                                                             │  │
    │  │                                                                                      │  │
    │  │  3. 참조 무결성 (Referential Integrity):                                              │  │
    │  │     • Foreign Key 제약                                                                │  │
    │  │     • 예: 주문의 고객 ID는 고객 테이블에 존재                                              │  │
    │  │                                                                                      │  │
    │  │  4. 사용자 정의 무결성 (User-defined Integrity):                                        │  │
    │  │     • CHECK 제약, TRIGGER                                                              │  │
    │  │     • 예: 잔고 >= 0                                                                   │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │
    │  [위배 시 처리]                                                                           │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  BEGIN TRANSACTION;                                                                   │  │
    │  │  INSERT INTO orders (qty) VALUES (-5);  -- CHECK 제약 위배                            │  │
    │  │  → 자동 ROLLBACK (일관성 위배로 트랜잭션 취소)                                        │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Isolation (격리성)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Isolation: 동시 실행 제어                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 동시 실행 트랜잭션 간 **서로 간섭하지 않아야 함**                                           │
    │  │  • 각 트랜잭션은 독립적으로 실행되는 것처럼 동작                                            │
    │  │  • Isolation Level로 격리 수준 제어                                                      │
    │                                                                                         │
    │  [격리성 위반 현상]                                                                       │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  1. Dirty Read (더티 읽기):                                                           │  │
    │  │     • Commit 안 된 데이터 읽기                                                         │  │
    │  │                                                                                      │  │
    │  │  2. Non-repeatable Read (반복 불가능 읽기):                                          │  │
    │  │     • 한 트랜잭션 내 같은 데이터를 읽을 때 값이 다름                                      │  │
    │  │                                                                                      │  │
    │  │  3. Phantom Read (팬텀 읽기):                                                         │  │
    │  │     • 같은 쿼리의 결과 행 수가 다름                                                     │  │
    │  │                                                                                      │  │
    │  │  4. Lost Update (갱신 분실):                                                          │  │
    │  │     • 두 트랜잭션이 같은 데이터를 동시에 갱신하여 하나의 갱신이 분실                            │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │
    │  [Isolation Level]                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Level              │  Dirty Read  │  Non-repeatable  │  Phantom  │  Lock          │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────  │  │
    │  │  READ UNCOMMITTED  │  O           │  O               │  O        │  없음          │  │
    │  │  READ COMMITTED    │  X           │  O               │  O        │  갱신 Lock     │  │
    │  │  REPEATABLE READ   │  X           │  X               │  O        │  공유 Lock     │  │
    │  │  SERIALIZABLE      │  X           │  X               │  X        │  범위 Lock     │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Durability (지속성)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Durability: 영구 보존                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Commit된 트랜잭션은 **영구적으로 저장**되어야 함                                            │
    │  │  • 시스템 장애(정전, 충돌) 발생해도 Commit된 내용은 보존                                      │
    │  │  • WAL(Write-Ahead Logging)로 구현                                                    │
    │                                                                                         │
    │  [WAL (Write-Ahead Logging)]                                                            │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  [트랜잭션 실행 순서]                                                                   │  │
    │  │  1. WAL Log Buffer에 기록                                                           │  │
    │  │  2. DB Page Buffer에 변경                                                            │  │
    │  │  3. WAL Log File로 fsync() (디스크에 기록)                                             │  │
    │  │  4. Commit 완료 응답                                                                 │  │
    │  │  5. 나중에 DB Page를 디스크에 기록 (Checkpoint)                                       │  │
    │  │                                                                                      │  │
    │  │  [장애 복구 시나리오]                                                                   │  │
    │  │  1. 시스템이 WAL 기록 후 DB Page 기록 전 다운                                            │  │
    │  │  2. 재시작 후 WAL 확인                                                               │  │
    │  │  3. WAL에 기록된 트랜잭션 다시 실행 (Redo)                                            │  │
    │  │  4. DB 복구 완료                                                                      │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │
    │  [물리적 보장]                                                                           │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  • RAID (Redundant Array of Independent Disks):                                      │  │
    │  │  • 전원 공급 장비 (UPS):                                                              │  │
    │  │  • 데이터베이스 복제 (Replication)                                                     │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### ACID vs BASE

| 구분 | ACID (RDBMS) | BASE (NoSQL) |
|------|--------------|--------------|
| **Atomicity** | 강함 | 약함 |
| **Consistency** | 강함 (Immediate) | 약함 (Eventual) |
| **Isolation** | 강함 | 약함 |
| **Durability** | 강함 | 가변 |
| **확장성** | 제한적 | 높음 |

### 과목 융합 관점 분석

#### 1. 운영체제 ↔ ACID
- **WAL**: ARIES Recovery Algorithm
- **Locking**: 2PL Protocol
- **MVCC**: Snapshot Isolation

#### 2. 분산 시스템 ↔ ACID
- **CAP 정리**: ACID + Partition Tolerance Trade-off
- **2PC**: 분산 트랜잭션

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: ACID 보장 설계
**상황**: 금융 이체 시스템
**판단**:

```sql
-- ACID 보장을 위한 테이블 설계

-- 1. Consistency: 제약 조건
CREATE TABLE accounts (
    id VARCHAR(20) PRIMARY KEY,
    balance DECIMAL(15,2) NOT NULL CHECK (balance >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Isolation: SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 3. Atomicity & Durability: 트랜잭션 처리
CREATE PROCEDURE transfer(
    p_from VARCHAR(20),
    p_to VARCHAR(20),
    p_amount DECIMAL(15,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Transfer failed';
    END;

    START TRANSACTION;

    -- 잔고 확인
    SELECT balance INTO @bal FROM accounts WHERE id = p_from FOR UPDATE;
    IF @bal < p_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient balance';
    END IF;

    -- 출금
    UPDATE accounts SET balance = balance - p_amount WHERE id = p_from;

    -- 입금
    UPDATE accounts SET balance = balance + p_amount WHERE id = p_to;

    -- 이체 내역
    INSERT INTO transfers (from_account, to_account, amount, timestamp)
    VALUES (p_from, p_to, p_amount, NOW());

    COMMIT;
END;
```

---

## Ⅴ. 기대효과 및 결론

### ACID 기대 효과

| 특성 | ACID 미준수 | ACID 준수 |
|------|----------|----------|
| **데이터 정확성** | 오류 가능 | 보장 |
| **장애 복구** | 불가능 | 가능 |
| **동시성 제어** | 이상 발생 | 제어 |
| **성능** | 높음 | 낮음 (Lock) |

### 미래 전망

1. **NewSQL**: ACID + Scale-out
2. **Spanner**: TrueTime
3. **Distributed Transaction**: Saga Pattern

### ※ 참고 표준/가이드
- **Härder & Reuter 1983**: ACID 정의
- **Gray & Reuter**: Transaction Processing
- **ANSI SQL-92**: Isolation Levels

---

## 📌 관련 개념 맵

- [트랜잭션](./7_transaction.md) - 기본 개념
- [동시성 제어](./9_concurrency_control.md) - Isolation
- [회복](./10_recovery.md) - Durability
- [분산 트랜잭션](./11_distributed_transaction.md) - 확장 ACID
