+++
title = "24. 트랜잭션 격리 (Transaction Isolation)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["Isolation", "Dirty-Read", "Phantom-Read", "MVCC", "Lock"]
draft = false
+++

# 트랜잭션 격리 (Transaction Isolation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션 격리는 **"동시 **트랜잭션 **간 **간섭**을 **제어**하는 **메커니즘"**으로, **ANSI SQL-92**에서 **4단계**(Read Uncommitted, Read Committed, Repeatable Read, Serializable)로 **정의**하며 **Isolation Level**로 **조정**한다.
> 2. **현상**: **Dirty Read**(커밋되지 않은 데이터 읽기), **Non-Repeatable Read**(같은 쿼리 결과 변경), **Phantom Read**(범위 쿼리에서 새 행 출현) **현상**이 **발생**하며 **Level**이 **높을수록 **현상**이 **줄어들지만 **성능**이 **저하**된다.
> 3. **구현**: **Lock-Based**(2PL, S/X Lock)와 **MVCC**(Multi-Version Concurrency Control)로 **구현**되며 **MySQL**(InnoDB: MVCC + Gap Lock), **PostgreSQL**(MVCC), **Oracle**(MVCC)가 **대표적**이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
트랜잭션 격리는 **"동시성 제어 수준"**이다.

**격리 목적**:
- **정확성**: 데이터 무결성 보장
- **일관성**: 직렬 실행과 동일한 결과
- **성능**: 격리 수준에 따른 트레이드오프

### 💡 비유
격리 수준은 **"화상 **회의 **채팅 ****과 같다.
- **Read Uncommitted**: 다른 사람 채팅 실시간 보임
- **Serializable**: 차례대로 한 명씩 발언

---

## Ⅱ. 아키텍처 및 핵심 원리

### 격리 수준별 현상

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Isolation Levels & Phenomena                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Isolation Level    │  Dirty Read  │  Non-Repeatable  │  Phantom Read  │  Performance │  │
    │  ──────────────────────────────────────────────────────────────────────────────────────│  │
    │  Read Uncommitted   │      O       │        O         │       O       │   Highest    │  │
    │  Read Committed     │      X       │        O         │       O       │    High      │  │
    │  Repeatable Read    │      X       │        X         │       O*      │    Medium    │  │
    │  Serializable       │      X       │        X         │       X       │    Low       │  │
    │                                                                                         │  │
    │  * MySQL InnoDB: X (Gap Lock으로 Phantom Read 방지)                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Dirty Read 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Dirty Read Scenario                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Time  │  Transaction 1                │  Transaction 2                                │  │
    │  ──────┼───────────────────────────────────────────────────────────────────────────────│  │
    │  T1    │  BEGIN;                       │                                               │  │
    │  T2    │  UPDATE accounts SET           │                                               │  │
    │        │    balance = balance - 1000    │                                               │  │
    │        │    WHERE id = 1;               │                                               │  │
    │  T3    │                               │  SELECT balance FROM accounts                   │  │
    │        │                               │    WHERE id = 1;                               │  │
    │        │                               │  → Returns 9000 (DIRTY!)                       │  │
    │  T4    │  ROLLBACK;                    │  → Transaction 1이 취소됨                       │  │
    │  T5    │                               │  → 실제 balance는 10000인데 9000으로 잘못 읽음   │  │
    │                                                                                         │  │
    │  → Read Committed 이상에서 방지                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Phantom Read 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Phantom Read Scenario                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Time  │  Transaction 1                │  Transaction 2                                │  │
    │  ──────┼───────────────────────────────────────────────────────────────────────────────│  │
    │  T1    │  BEGIN;                       │                                               │  │
    │  T2    │  SELECT COUNT(*) FROM          │                                               │  │
    │        │    users WHERE age > 20;       │                                               │  │
    │        │  → Returns: 5                  │                                               │  │
    │  T3    │                               │  INSERT INTO users (age) VALUES (25);          │  │
    │        │                               │  COMMIT;                                      │  │
    │  T4    │  SELECT COUNT(*) FROM          │                                               │  │
    │        │    users WHERE age > 20;       │                                               │  │
    │        │  → Returns: 6 (PHANTOM!)       │                                               │  │
    │  T5    │  COMMIT;                       │                                               │  │
    │                                                                                         │  │
    │  → Serializable에서 Gap Lock 또는 Predicate Lock으로 방지                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### DBMS별 기본 격리 수준

| DBMS | 기본 Level | 구현 방식 |
|------|-----------|-----------|
| **MySQL InnoDB** | Repeatable Read | MVCC + Gap Lock |
| **PostgreSQL** | Read Committed | MVCC |
| **Oracle** | Read Committed | MVCC |
| **SQL Server** | Read Committed | MVCC + Lock |

### MVCC (Multi-Version Concurrency Control)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         MVCC Architecture                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Table: accounts (id, balance)                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  id  │  balance  │  created_tx  │  expired_tx  │  ┌─────────────────────────────────┐  │  │  │
    │  │  ────┼───────────┼──────────────┼──────────────┼──┤  Row 1 (id=1)                  │  │  │  │
    │  │   1  │  10000    │     100      │      NULL    │  │  ┌─────────────────────────────┐  │  │  │  │
    │  │   1  │   9000    │     101      │      NULL    │  │  │  Version 1: 10000 (TX 100)  │  │  │  │  │
    │  │   2  │   5000    │      99      │      NULL    │  │  │  Version 2: 9000 (TX 101)   │  │  │  │  │
    │  │   3  │   3000    │      98      │      NULL    │  │  └─────────────────────────────┘  │  │  │  │
    │  │  ──────────────────────────────────────────────────└─────────────────────────────────┘  │  │  │
    │  │                                                                                         │  │  │
    │  │  TX 100 (Read Committed):                                                               │  │  │
    │  │    SELECT balance WHERE id = 1; → 10000 (TX 100 시작 시점)                             │  │  │
    │  │                                                                                         │  │  │
    │  │  TX 101 (Read Committed):                                                               │  │  │
    │  │    SELECT balance WHERE id = 1; → 9000 (TX 101 시작 후 커밋된 버전)                     │  │  │
    │  │                                                                                         │  │  │
    │  │  → Writer가 Reader를 차단하지 않음                                                      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Lock-Based (2PL - Two Phase Locking)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Two Phase Locking                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Phase 1: Growing Phase (Lock Acquisition)                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  T1: S-lock(A) → S-lock(B) → X-lock(C)                                               │  │  │
    │  │  T2: S-lock(D) → (wait for C)                                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Phase 2: Shrinking Phase (Lock Release)                                                 │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  T1: unlock(A) → unlock(B) → unlock(C)                                               │  │  │
    │  │  T2: → S-lock(C) 획득 가능                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Growing Phase에서는 Lock만 획득, Shrinking Phase에서는 Lock만 해제                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 격리 수준 설정

```sql
-- MySQL
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET GLOBAL tx_isolation = 'READ-COMMITTED';

-- PostgreSQL
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
ALTER DATABASE mydb SET default_transaction_isolation = 'read committed';

-- SQL Server
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Oracle (Read Committed만 지원, Statement-Level Consistency)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 금융 거래 (높은 격리 필요)
**상황**: 계좌 이체
**판단**: Serializable

```sql
-- Serializable 격리 수준
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN;

-- 1. 출금 계좌 Lock 확인
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- 2. 입금 계좌 Lock 확인
SELECT balance FROM accounts WHERE id = 2 FOR UPDATE;

-- 3. 이체 실행
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;

COMMIT;
```

#### 시나리오: 분석 쿼리 (성능 우선)
**상황**: 리포트 생성
**판단**: Read Committed

```sql
-- Read Committed (일반적)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

BEGIN;

-- Dirty Read 없이 빠르게 읽기
SELECT SUM(amount) FROM transactions WHERE date >= '2026-01-01';

COMMIT;
```

---

## Ⅴ. 기대효과 및 결론

### 격리 수준 기대 효과

| Level | 일관성 | 성능 | 사용처 |
|-------|--------|------|--------|
| **Read Uncommitted** | 최저 | 최고 | 로그 분석 |
| **Read Committed** | 중간 | 높음 | 일반 OLTP |
| **Repeatable Read** | 높음 | 중간 | 금융 (MySQL) |
| **Serializable** | 최고 | 낮음 | 금융 (Oracle/PG) |

### 모범 사례

1. **기본**: Read Committed
2. **금융**: Serializable
3. **배치**: Read Uncommitted 가능
4. **MySQL**: Repeatable Read 기본 (Phantom Read 방지)

### 미래 전망

1. **Adaptive Isolation**: 워크로드 기반 자동 조절
2. **SIs**: Serializable Isolation (Snapshot)
3. **Deterministic**: 결정적 격리

### ※ 참고 표준/가이드
- **ANSI SQL-92**: Isolation Levels
- **MySQL**: InnoDB Locking
- **PostgreSQL**: MVCC Documentation

---

## 📌 관련 개념 맵

- [ACID](./1_transaction.md) - 트랜잭션 속성
- [잠금](./2_locking.md) - Lock 기법
- [MVCC](./3_mvcc.md) - 다중 버전
