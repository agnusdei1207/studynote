+++
title = "220. 엄격한 2단계 락킹 (Strict 2PL) - 무결성 수호의 표준"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 220
+++

# 220. 엄격한 2단계 락킹 (Strict 2PL) - 무결성 수호의 표준

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Strict 2PL (Strict Two-Phase Locking)은 기본적인 2PL 프로토콜의 확장 단계(Shrinking Phase)를 트랜잭션 종료 시점(Commit/Abort)으로 지연시켜, **배타적 잠금(X-Lock)의 해제를 최종 완료 시점까지만 허용하는 강력한 동시성 제어 프로토콜**이다.
> 2. **가치**: 데이터베이스 회복성(Recoverability)을 보장하는 핵심 기제로, **연쇄 복귀(Cascading Rollback)**를 근본적으로 차단하여 시스템의 안정성을 확보하고 데이터 무결성(Integrity)을 물리적으로 보장한다.
> 3. **융합**: 고가용성(HA)이 요구되는 분산 DB 환경과 RDBMS(Relational DBMS)의 기본 트랜잭션 격리 수준(Repeatable Read, Serializable) 구현의 기반이 되며, 높은 동시 요청(Concurrency) 처리와 무결성 사이의 균형을 맞추는 아키텍처적 표준이다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
Strict 2PL (Strict Two-Phase Locking)은 트랜잭션의 모든 Lock 획득이 끝난 시점(Lock Point) 이후에는 어떠한 Lock도 해제하지 않다가, 트랜잭션이 최종적으로 Commit(커밋)되거나 Abort(중단)되는 순간에 보유하고 있던 모든 Lock을 **원자적(Atomic)으로 해제**하는 방식입니다.
일반적인 2PL (Conservative 2PL 등)은 Growing Phase(잠금 획득) 이후 Shrinking Phase(잠금 해제)가 바로 시작되어, 트랜잭션 진행 중간에 배타적 Lock(X-Lock)이 풀리는 순간이 존재합니다. 반면, Strict 2PL은 이 Shrinking Phase의 시작점을 트랜잭션의 수명(Lifetime) 끝으로 미루는 것이 핵심 차이점입니다.

**2. 등장 배경 및 문맥 (Context)**
① **기존 한계**: 기존 2PL 프로토콜 하에서는 트랜잭션 A가 데이터를 수정하고 Lock을 해제한 시점부터 트랜잭션 A가 Commit 되기 전까지, 다른 트랜잭션 B가 그 더러운 데이터(Dirty Data)를 읽을 위험이 존재했습니다.
② **혁신적 패러다임**: 이를 해결하기 위해 "내가 아직 확정 짓지 않은 데이터는 끝까지 접근을 막아라"는 철학이 도입되었습니다. 이는 **Serializability (직렬 가능성)** 보다는 **Recoverability (회복 가능성)**에 중점을 둔 전략입니다.
③ **비즈니스 요구**: 금융 결제나 재고 관리 시스템에서 하나의 실패가 도미노처럼 번지는 '연쇄 복귀'는 치명적입니다. Strict 2PL은 성능의 일부 손실을 감수하고서라도 데이터의 안전한 확정을 최우선으로 하는 현대 RDBMS의 표준이 되었습니다.

```text
      [2PL vs Strict 2PL의 구분 차이]

      🔓 2PL (Basic/Conservative)            🔒 Strict 2PL
      ──────────────────────                 ──────────────────────
      
      Growing Phase │ Shrinking Phase       Growing Phase │ Shrinking Phase
      (Lock Acquire)│ (Lock Release)        (Lock Acquire)│ (Lock Release)
                    │                                    │
      ① Get S/X     │ ③ Release X/Lock     ① Get S/X     │ ③ No Release
      ② ...         │ ④ ...                ② ...         │ ④ ...
                    │ (Risk: Dirty Read)                  │ (Safe: Hold till end)
                    │                                    │
                  Commit/Abort                          Commit/Abort
                         │                                    │
                         ▼                                    ▼
                   [End of Trans]                      [All Release]
```
*해설: 일반 2PL은 중간에 Lock이 해제되어 다른 트랜잭션의 중간 데이터 참조를 허용하지만(연쇄 롤백 위험), Strict 2PL은 끝까지 Lock을 쥐고 있어 타 트랜잭션의 접근을 물리적으로 차단합니다.*

**💡 비유**
일반적인 2PL은 식당 주방에서 요리를 하다가 도중에 접시 문을 열어 다른 사람이 반찬을 집어가게 두는 것과 같습니다. Strict 2PL은 요리가 완성되어 손님에게 내어주기 전까지는 주방 출입구에 '절대 출입 금지' 팻말을 걸어두는 것입니다.

**📢 섹션 요약 비유**: Strict 2PL의 도입은 마치 **'고속도로 터널 입구에서 사고 차량이 완전히 견인될 때까지 진입을 통제하는 관제 시스템'**과 같습니다. 중간에 터널을 열면 안으로 진입한 차량들이 연쇄적으로 정체(롤백)되지만, 끝까지 막고 있으면 밖의 차량들은 깔끔하게 우회하거나 대기하면 되므로 혼잡을 방지할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 (표)**
Strict 2PL을 구현하기 위한 DBMS(DataBase Management System)의 주요 모듈 및 요소는 다음과 같습니다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---:|:---|:---|:---|
| **Lock Manager (LM)** | 락 할당 및 해제 관리자 | 트랜잭션의 Lock 요청(Lock Table 참조)을 승인하거나 대기큐(Wait-for Graph)에 넣음 | 주방장의 수행비서 |
| **X-Lock (Exclusive Lock)** | 쓰기 잠금 | Read/Write 모두 차단. 트랜잭션 종료 시점까지 점유 유지. | '예약 완료' 푯맽 |
| **S-Lock (Shared Lock)** | 읽기 잠금 | 공유 가능하나, Strict 모드에서는 보통 X-Lock에 종속되어 동작 | '서성거림 허용' |
| **Transaction Agent** | 트랜잭션 수행자 | SQL을 실행하며 LM에 Lock을 요청하고 Commit/Rollback을 시도 | 요리사 |
| **Recovery Manager (RM)** | 복구 관리자 | 장애 시 Undo/Redo 로그를 통해 미확정 트랜잭션을 처리 | 청소반 |

**2. 상세 동작 매커니즘 (State Transition)**
Strict 2PL의 트랜잭션 수명 주기(Transaction Lifecycle)는 다음과 같이 3단계로 세분화됩니다.

```text
[Strict 2PL Transaction Lifecycle]

  Status
    ▲
    │
[ACTIVE] ────────────────────────────> [PARTIALLY COMMITTED] ───> [COMMITTED]
    │                                      │
    │  1. Growing Phase (Acquire)          │  2. Strict Hold Phase (No Release)
    │     - LOCK-S(item)                   │     - 계속해서 Lock 유지
    │     - LOCK-X(item)                   │     - 다른 Tx의 접근 차단
    │     ...                              │
    │                                      │
    │                                      │  3. Atomic Release
    │                                      │     - RELEASE ALL LOCKS()
    │                                      ▼
    └──────────────────────────────────> [ABORTED]
               (System Failure / User Cancel)
```

*해설:*
1. **Growing Phase**: 트랜잭션이 시작하여 데이터를 읽거나 쓸 때 필요한 Lock을 획득하는 구간입니다.
2. **Strict Hold Phase (The Key)**: 일반 2PL과 달리, 모든 작업이 끝났더라도 Commit 전까지는 자원을 놓지 않습니다. 이 구간에서 다른 트랜잭션은 기다려야 합니다.
3. **Atomic Release**: Commit 명령과 함께 Log Buffer를 Disk로 Flushing하고, 보유한 모든 Lock을 동시에 해제하여 다른 트랜잭션이 접근하게 합니다.

**3. 핵심 알고리즘 및 로직 (Pseudo-code)**
Strict 2PL의 핵심은 Lock 해제 시점의 제어입니다.

```sql
-- [Pseudo-code: Transaction Execution under Strict 2PL]

BEGIN TRANSACTION;

-- Phase 1: Operations (Implicit Lock Acquisition)
UPDATE Account SET balance = balance - 100 WHERE user_id = 1;
-- [Implicity: LOCK_X(Account#1) granted by Lock Manager]

-- Phase 2: Strict Protocol Enforcement
-- (System waits here if other TX holds locks, but holds own locks forever)
-- NOTE: No UNLOCK happens here.

-- Phase 3: Commit / Atomic Release
IF (Commit_Command) THEN
    -- 1. Write Commit Log to Disk (Durability)
    FLUSH_LOG(); 
    
    -- 2. Release ALL Locks Atomically
    FOR each lock IN Lock_Table.held_locks DO
        RELEASE(lock);
    END FOR;
END IF;

-- If Abort occurs, ROLLBACK happens first, THEN locks are released.
```

**4. 수학적 성질 (Serializability & Recoverability)**
Strict 2PL은 **Conflict Serializability(충돌 직렬 가능성)**를 만족하며, 더 나아가 **Strict Schedule(엄격한 스케줄)**의 조건을 만족합니다.
*   *Strict Schedule Condition*: 트랜잭션 $T_i$가 쓴 데이터 항목 $Q$에 대해, $T_i$가 종료(Commit/Abort)하기 전까지 다른 트랜잭션 $T_j$가 $Q$에 쓰거나 읽을 수 없다.
    *   이 조건은 $T_j$가 $T_i$의 Dirty Read를 읽거나 Overwrite하는 것을 방지합니다.

**📢 섹션 요약 비유**: Strict 2PL의 동작 원리는 **'이사 트럭의 짐 싣기'**와 같습니다. 짐을 다 싣고 이동을 완료할 때까지(Commit)는 트럭의 문을 절대 열지 않습니다. 도중에 문을 열어 짐을 빼거나(Lock Release) 다른 짐을 넣으려 하면(Other TX), 짐이 떨어지거나 분실되어 전부 다시 싣어야(Cascading Rollback) 할 수 있기 때문입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교표 (Strict 2PL vs Rigorous 2PL vs Basic 2PL)**
동시성 제어 기법의 성격과 보장 범위를 정량적으로 비교합니다.

| 구분 | Basic 2PL (Basic 2PL) | Strict 2PL (Strict 2PL) | Rigorous 2PL (Rigorous 2PL) |
|:---:|:---|:---|:---|
| **X-Lock 해제 시점** | Growing Phase 종료 후 즉시 해제 가능 | Commit/Abort 시점에 해제 | **모든 Lock(S/X)**을 Commit 시점에 해제 |
| **S-Lock 해제 시점** | Lock 획득 후 필요 없으면 해제 가능 | Commit 전 (X-Lock보다 일찍 가능) | Commit 시점 (X-Lock과 동일) |
| **연쇄 복귀 방지** | ❌ 방지 불가 (가능성 있음) | ✅ 완벽 방지 | ✅ 완벽 방지 |
| **Write Skew 방지** | ⚠️ 불가능 (Isolation Level에 따름) | ⚠️ 불가능 (Snapshot 등 필요) | ⚠️ 불가능 |
| **동시성(Concurrency)** | ⭐⭐⭐⭐⭐ (Lock 빨리 풀림) | ⭐⭐⭐ (Hold 시간 길음) | ⭐⭐ (S-Lock까지 유지) |
| **주요 사용처** | 단순한 시스템, 성능 우선 | **일반적인 상용 DB (Oracle, MySQL(InnoDB))** | 특수한 요구사항이 있는 시스템 |

**2. 과목 융합 관점 (OS 및 네트워크와의 시너지)**
*   **운영체제 (OS)와의 연관성**: DB의 Strict 2PL은 OS 커널의 Mutex나 Semaphore와 개념은 유사하지만, **"복구 가능성"**을 보장한다는 점에서 결정적 차이가 있습니다. OS의 Lock은 프로세스가 죽으면 커널이 자원을 회수하지만, DB 트랜잭션은 롤백(Rollback)이라는 논리적 작업이 수반되어야 하므로, Lock을 끝까지 쥐고 있어야 합니다.
*   **네트워크 (Network)와의 연관성**: 분산 트랜잭션 처리(2PC, Two-Phase Commit) 환경에서 Strict 2PL은 필수적입니다. 네트워크 지연으로 인한 준비 단계(Prepare Phase) 시간이 길어질 때, 중간에 Lock을 풀어버리면 분산된 노드 간의 데이터 일관성이 깨지기 때문입니다.

**3. 성능 및 지표 분석 (Metrics)**
*   **Lock Hold Time (락 유지 시간)**: 일반 2PL 대비 Strict 2PL은 Lock Hold Time이 트랜잭션 전체 길이로 늘어납니다. 이는 **응답 시간(Latency) 증가**와 **처리량(Throughput) 감소**로 이어집니다.
*   **Deadlock Probability (교착상태 확률)**: Lock을 오래 쥐고 있으므로, 다른 트랜잭션이 대기하는 시간이 길어지고 교착상태(Deadlock) 발생 빈도가 약간 증가할 수 있습니다. 하지만 회복 로직의 복잡도는 급격히 낮아집니다.

**📢 섹션 요약 비유**: Strict 2PL과 다른 방식의 차이는 **'도서관 좌석 이용 시스템'**과 같습니다.
*   *Basic 2PL*: 화장실 갈 때 자리에 물건을 두지 않고 갔다가(자리 해제), 오면 누군가 앉아 있어서 싸움 날 수 있음.
*   *Strict 2PL*: 화장실 갈 때 자리에 물건을 두고 가서(Lock 유지), 내가 다시 올 때까지 아무도 앉지 못하게 함.
*   *Rigorous 2PL*: 물건 두고 갈 뿐만 아니라, 책 읽는 중에도 옆 사람이 책만 못 보게 깐깐하게 방어함.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**
데이터베이스 아키텍트는 다음과 같은 상황에서 Strict 2PL의 도입 및 튜닝 여부를 결정해야 합니다.

*   **시나리오 A: 금융 결제 시스템 (Banking Transfer)**
    *   *상황*: 계좌 이체 도중 장애 발생 시 잔액이 이상해지면 안 됨.
    *   *판단*: **Strict 2PL 필수 적용**