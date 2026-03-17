+++
title = "33. NewSQL (NewSQL Database)"
date = 2026-03-06
categories = ["studynotes-database"]
tags = ["NewSQL", "Spanner", "CockroachDB", "Distributed-SQL", "ACID"]
draft = false
+++

# NewSQL (NewSQL Database)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NewSQL은 **"관계형 **DB의 **ACID **보장**과 **NoSQL**의 **확장성**을 **동시**에 **제공**하는 **분산 **데이터베이스\"**로, **SQL **인터페이스**를 **유지**하면서 **수평 **확장**(Horizontal Scaling)**이 **가능**하다.
> 2. **기술**: **Google Spanner**(TrueTime **API), **CockroachDB**(Raft + **Hybrid Logical Clock)**, **FaunaDB**(Calvin **Protocol)**가 **대표적**이며 **Sharding**(자동 **분할)**, **Distributed Transactions**(2PC, **3PC)**, **Consistent Replication**(Quorum)**으로 **구현**된다.
> 3. **사용**: **OLTP**(Online Transaction Processing)**에 **최적화**되고 **Global **Database**(전 세계 **배포)**, **Microservices**(분산 **트랜잭션)**, **FinTech**(금융 **거래)**에 **사용**된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
NewSQL은 **"확장 가능한 관계형 DB"**이다.

**DBMS 비교**:
| 유형 | ACID | 확장성 | SQL | 예시 |
|------|------|--------|-----|------|
| **RDBMS** | O | X | O | MySQL |
| **NoSQL** | X | O | X | MongoDB |
| **NewSQL** | O | O | O | Spanner |

### 💡 비유
NewSQL은 ****글로벌 **은행 ****네트워크 ****와 같다.
- **지점**: Shard
- **본사**: Coordinator
- **ATM**: Client

---

## Ⅱ. 아키텍처 및 핵심 원리

### Google Spanner 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Google Spanner Architecture                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Global Spanner Instance                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Region: us-east1 (North America)                                                    │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Zone A (us-east1-a)          Zone B (us-east1-b)          Zone C (us-east1-c)    │  │  │  │
    │  │  │  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐          │  │  │  │
    │  │  │  │ Spanner Server│           │ Spanner Server│           │ Spanner Server│          │  │  │  │
    │  │  │  │ • 100s of    │           │ • 100s of    │           │ • 100s of    │          │  │  │  │
    │  │  │  │   tablets    │           │   tablets    │           │   tablets    │          │  │  │  │
    │  │  │  └──────────────┘           └──────────────┘           └──────────────┘          │  │  │  │
    │  │  │        │                        │                        │                         │  │  │  │
    │  │  │        └────────────────────────┴────────────────────────┘                         │  │  │  │
    │  │  │                    Synchronous replication (3 replicas)                             │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │                                                                                       │  │  │
    │  │  Region: europe-west1 (Europe)                                                         │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Zone D (europe-west1-b)    ... (async replication from us-east1)                   │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  TrueTime API                                                                         │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  • GPS + Atomic Clocks for time synchronization                                    │  │  │  │
    │  │  │  • Guarantees: ε < 10ms clock skew across all datacenters                          │  │  │  │
    │  │  │  • Exposes: TT.now() = [earliest, latest] timestamp interval                      │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │           │                                                                             │  │  │
    │  │           ▼                                                                             │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  External Consistency: Uses TrueTime to order transactions globally              │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Spanner Timestamp Ordering

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Spanner Transaction Ordering                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Global transaction ordering
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Transaction T1 (New York): Write balance = $100                                       │  │
    │  Transaction T2 (London): Read balance → Should see $100 or previous value?             │  │
    │                                                                                         │  │
    │  Without global clock: Impossible to guarantee ordering                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution: TrueTime-based ordering
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Client requests timestamp from TrueTime                                            │  │
    │     TT.now() = [10:00:00.010, 10:00:00.020]  (ε = 10ms)                              │  │
    │                                                                                         │  │
    │  2. Client assigns commit timestamp:                                                     │  │
    │     s = TT.now().latest + 1 = 10:00:00.021                                               │  │
    │                                                                                         │  │
    │  3. Wait for time to pass:                                                               │  │
    │     Wait until TT.now().earliest >= s                                                     │  │
    │     → Ensures no other transaction can have same timestamp                               │  │
    │                                                                                         │  │
    │  4. Commit transaction with timestamp s                                                  │  │
    │                                                                                         │  │
    │  5. Replica writes must wait until their local time >= s                                │  │
    │     → Guarantees all replicas apply transactions in same order                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### CockroachDB Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CockroachDB Architecture                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  SQL Layer                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  PostgreSQL-compatible SQL parser + optimizer                                        │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Key-Value Layer (Monotonic SQLified KV)                                            │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Data Model: /TableID/PrimaryKeyIndex → Value                                    │  │  │  │
    │  │  │  Example: /customer/1001 → {name: "Alice", balance: 1000}                         │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Range Sharding                                                                       │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Range 1: keys [0x00, 0x33) → Node A                                             │  │  │  │
    │  │  │  Range 2: keys [0x33, 0x66) → Node B                                             │  │  │  │
    │  │  │  Range 3: keys [0x66, 0xFF] → Node C                                             │  │  │  │
    │  │  │  → Automatic rebalancing when ranges grow or nodes join/leave                      │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Replication (Raft)                                                                   │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Range Replica Group (3 replicas)                                                  │  │  │  │
    │  │  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                   │  │  │  │
    │  │  │  │ Replica 1       │  │ Replica 2       │  │ Replica 3       │                   │  │  │  │
    │  │  │  │ (Leader)        │  │ (Follower)      │  │ (Follower)      │                   │  │  │  │
    │  │  │  └──────────────────┘  └──────────────────┘  └──────────────────┘                   │  │  │  │
    │  │  │         │                    │                    │                               │  │  │  │
    │  │  │         └────────────────────┴────────────────────┘                               │  │  │  │
    │  │  │                      Raft consensus log                                          │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### HLC (Hybrid Logical Clock)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Hybrid Logical Clock                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Distributed systems need global ordering without atomic clocks
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Logical Clock (Lamport):                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Increment on send/receive                                                         │  │  │
    │  │  • Total ordering but no relation to real time                                       │  │  │
    │  │  • Problem: Cannot implement "read 5 seconds ago"                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Physical Clock (NTP):                                                                  │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Actual wall-clock time                                                            │  │  │
    │  │  • Problem: Clock skew, can go backward                                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Hybrid Logical Clock (HLC):                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  struct HLC {                                                                         │  │  │
    │  │      uint64_t physical;   // Max node physical time                                 │  │  │
    │  │      uint64_t logical;    // Counter for tie-breaking                               │  │  │
    │  │  }                                                                                    │  │  │
    │  │                                                                                       │  │  │
    │  │  Properties:                                                                           │  │  │
    │  │  • Monotonic: Never goes backwards                                                    │  │  │
    │  │  • Close to physical time: bounded by max clock skew                                 │  │  │
    │  │  • Comparable: Can order events across nodes                                          │  │  │
    │  │                                                                                       │  │  │
    │  │  Update on event:                                                                     │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  hlc.send(event):                                                                   │  │  │  │
    │  │  │    hlc.physical = max(hlc.physical, node_physical_time)                            │  │  │  │
    │  │  │    if (old_physical == hlc.physical):                                              │  │  │  │
    │  │  │        hlc.logical++                                                               │  │  │  │
    │  │  │    else:                                                                           │  │  │  │
    │  │  │        hlc.logical = 0                                                              │  │  │  │
    │  │  │    return hlc                                                                      │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### NewSQL 비교

| DB | 특징 | 확장성 | 일관성 |
|----|------|--------|--------|
| **Spanner** | TrueTime | 글로벌 | Strong |
| **CockroachDB** | Raft, HLC | 글로벌 | Serializble |
| **FaunaDB** | Calvin | 글로벌 | Strong |
| **TiDB** | TiKV | 글로벌 | Serializble |

### 분산 트랜잭션

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Distributed Transaction (2PC)                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Scenario: Transfer $100 from account A (Node 1) to account B (Node 2)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Coordinator                           Participant Node 1        Participant Node 2          │  │
    │  ┌───────────────────────────────────┐ ┌──────────────────────────────────────────────┐ ┌──────────────────────────────────────────────┐
    │  │  1. Begin Transaction            │ │                                              │ │                                              │
    │  │  ──────────────────────────────────────────────────────────────────────────────────────> │ ──────────────────────────────────────────────> │
    │  │                                   │  2. Prepare: Debit A?    │ │  2. Prepare: Credit B?   │
    │  │  <───────────────────────────────────────────────────────────────────────────────────────│ <────────────────────────────────────────────── │
    │  │                                   │  Vote: YES             │ │  Vote: YES              │
    │  │  3. All voted YES → COMMIT         │                                              │ │                                              │
    │  │  ──────────────────────────────────────────────────────────────────────────────────────> │ ──────────────────────────────────────────────> │
    │  │                                   │  4. Commit: Apply      │ │  4. Commit: Apply      │
    │  │  <───────────────────────────────────────────────────────────────────────────────────────│ <────────────────────────────────────────────── │
    │  │                                   │  Ack                  │ │  Ack                    │
    │  │  5. Transaction Complete          │                                              │ │                                              │
    │  └───────────────────────────────────┘                                              │ │                                              │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 글로벌 Fintech 플랫폼
**상황**: 전 세계 거래 처리
**판단**: CockroachDB

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Global Fintech Platform                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • ACID transactions for financial data                                                 │  │
    │  • Low latency (< 100ms) globally                                                       │  │
    │  • High availability (99.99%)                                                            │  │
    │  • SQL interface for existing apps                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution: CockroachDB
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  -- Create table with regional partitioning                                              │  │
    │  CREATE TABLE accounts (                                                                 │  │
    │      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),                                     │  │
    │      user_id UUID NOT NULL,                                                              │  │
    │      balance DECIMAL(19,4) NOT NULL,                                                      │  │
    │      region STRING NOT NULL,                                                             │  │
    │      INDEX (region)                                                                     │  │
    │  ) PARTITION BY LIST (region) AUTO PARTITION;                                            │  │
    │                                                                                         │  │
    │  -- Configure regions                                                                    │  │
    │  ALTER PARTITION accounts CONFIGURE ZONE USING                                            │  │
    │      'constraints = "[+region=us-east]"';                                                │  │
    │  ALTER PARTITION accounts CONFIGURE ZONE USING                                            │  │
    │      'constraints = "[+region=europe-west]"';                                            │  │
    │  ALTER PARTITION accounts CONFIGURE ZONE USING                                            │  │
    │      'constraints = "[+region=asia-northeast]"';                                        │  │
    │                                                                                         │  │
    │  -- Transfer funds (distributed transaction)                                              │  │
    │  BEGIN;                                                                                  │  │
    │  UPDATE accounts SET balance = balance - 100                                             │  │
    │     WHERE id = 'user-alice-uuid' AND region = 'us-east';                                 │  │
    │  UPDATE accounts SET balance = balance + 100                                             │  │
    │     WHERE id = 'user-bob-uuid' AND region = 'europe-west';                               │  │
    │  COMMIT;  -- Auto-routed via gateway regions, replicated synchronously                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### NewSQL 기대 효과

| DB | 일관성 | 지연 | 복잡도 |
|----|--------|------|--------|
| **Spanner** | Strong | 50-200ms | 높음 |
| **CockroachDB** | Serializble | 20-100ms | 중간 |
| **RDBMS** | Strong | < 10ms | 낮음 |

### 모범 사례

1. **스키마**: Denormalize
2. **인덱스**: 지역 기반
3. **트랜잭션**: 짧게
4. **모니터링**: 지연 추적

### 미래 전망

1. **Serverless**: Aurora Serverless v2
2. **Edge**: 지역 분산
3. **Hybrid**: Cloud + On-prem
4. **ML**: 통합 예측

### ※ 참고 표준/가이드
- **Google**: Spanner Paper
- **CockroachLabs**: Architecture Docs
- **Fauna**: Calvin Protocol

---

## 📌 관련 개념 맵

- [분산 합의](./9_consensus/29_distributed_consensus.md) - Raft
- [NoSQL](./1_nosql/21_nosql_overview.md) - CAP 정리
- [ACID](./4_transaction/23_transaction.md) - 트랜잭션

