+++
title = "214. 공유 락 (Shared Lock / Read Lock, S-Lock)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 214
+++

# 214. 공유 락 (Shared Lock / Read Lock, S-Lock)
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 공유 락(Shared Lock)은 데이터베이스의 동시성 제어 메커니즘에서 **읽기 일관성(Read Consistency)**을 보장하기 위해 다중 트랜잭션이 동일한 데이터를 동시에 읽을 수 있게 허용하는 잠금 모드입니다.
> 2. **가치**: 데이터 변경을 방지하여 'Non-Repeatable Read'나 'Dirty Read'를 방지함으로써 데이터 무결성을 유지하면서도, 읽기 작업 간 병렬 처리를 통해 시스템의 **처리량(Throughput)**을 극대화합니다.
> 3. **융합**: 배타 락(Exclusive Lock)과의 상호 배제적 원칙에 기반하며, 현대의 MVCC(Multi-Version Concurrency Control) 환경에서는 잠금 경쟁(Lock Contention)을 최소화하는 보조 전략으로 활용됩니다.
+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**S-Lock (Shared Lock)**, 또는 **Read Lock**은 트랜잭션이 데이터베이스의 레코드나 테이블을 조회(Read)할 때, 다른 트랜잭션의 수정(Write) 작업으로부터 해당 데이터를 보호하기 위해 요청하는 잠금입니다.
RDBMS(Relational Database Management System)의 격리 수준(Isolation Level) 중 **Read Committed** 이상에서 데이터의 일관성을 보장하는 핵심 수단으로 작용합니다. 기본적으로 **"여러 명의 독자는 동시에 책을 읽을 수 있지만, 독자가 있는 상태에서는 저자가 내용을 수정할 수 없다"**는 철학을 따릅니다.

**등장 배경 및 필요성**
초기의 데이터베이스나 파일 시스템에서는 데이터를 읽는 순간에도 쓰기 작업을 전면 차단하여 데이터 무결성을 유지했습니다. 하지만 대규모 서비스로 전환되며 **읽기(Read) 비중이 쓰기(Write)보다 압도적으로 높은 워크로드**가 일반화되었습니다. 이에 따라 읽기 작업 간의 불필요한 대기 시간을 제거하고 동시성을 높이기 위해, '읽기는 읽기끼리 공유 가능'하다는 논리를 도입하여 S-Lock이 정립되었습니다.

**기술적 특성**
1.  **공유성 (Compatibility)**: 다른 S-Lock과 호환되어 동시 접근을 허용합니다.
2.  **배타성 (Exclusivity)**: **X-Lock (Exclusive Lock)**, 즉 쓰기 잠금과는 상호 배타적입니다. S-Lock이 걸린 데이터에 X-Lock을 요청하면 대기 큐(Wait Queue)에서 대기해야 합니다.

> **📢 섹션 요약 비유**: 공유 락은 **'도서관의 참고 서적'**과 같습니다. 여러 학생들이 동시에 같은 책을 펴놓고 내용을 읽는 것(공유)은 가능하지만, 누군가 읽고 있는 동안에는 사서가 해당 책의 페이지를 찢거나 수정하려(배타) 해도 반드시 읽기가 끝날 때까지 기다려야 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 및 상세 동작**

S-Lock의 내부 메커니즘은 **Lock Manager (잠금 관리자)**에 의해 제어됩니다. 주요 구성 요소와 프로토콜은 다음과 같습니다.

| 구성 요소 | 역할 | 내부 동작 및 프로토콜 |
|:---|:---|:---|
| **Lock Request (잠금 요청)** | 트랜잭션이 데이터 읽기 시 Lock Manager에게 S-Lock 요청 전송 | `SELECT ... FOR SHARE` 또는 기본 `SELECT` (격리 수준 따름) |
| **Grant (허가)** | 요청이 현재 리소스와 호환될 경우 잠금 부여 | S-Lock 큐(Queue)에 트랜잭션 ID 추가 |
| **Block/Waits (대기)** | 호환되지 않는 잠금(X-Lock)이 존재할 경우 대기 상태 진입 | 세마포어(Semaphore) 또는 Mutex 기반의 Block 상태로 전환 |
| **Lock Table (잠금 테이블)** | 메모리상에서 데이터별 잠금 상태를 관리하는 해시 테이블 | Key: Data ID, Value: Lock Mode + Holding TXN List |
| **Unlock (해제)** | 트랜잭션 종료(Commit/Rollback) 시 잠금 반납 | 대기 중이던 다른 트랜잭션에게 Wakeup 신호 전송 |

**ASCII 구조 다이어그램: Lock Manager 내부 동작**

아래 다이어그램은 트랜잭션 T1과 T2가 S-Lock을 획득하고, T3가 X-Lock을 요청할 때의 메모리 상태와 흐름을 도식화한 것입니다.

```text
      [ Transaction Manager ]
            │      │
    ┌───────▼──────▼─────┐
    │   Transaction 1    │
    │  (Read Request)    │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────────────────────────────┐
    │          Lock Manager (Memory)             │
    │  ┌──────────────────────────────────────┐  │
    │  │  Lock Table Entry for Row #105       │  │
    │  │  ┌────────────────────────────────┐  │  │
    │  │  │ Lock Mode: SHARED (S)          │  │  │
    │  │  │ Holders: [ T1, T2 ]            │  │  │
    │  │  │ Waiters: [ T3 (Waiting X) ]    │  │  │
    │  │  └────────────────────────────────┘  │  │
    │  └──────────────────────────────────────┘  │
    └─────────────┬───────────────┬───────────────┘
                  │               │
       S-Lock     │               │ X-Lock Request
      Granted     │               │ (BLOCKED)
      to T2       │               │
                  ▼               ▼
        ┌──────────────┐   ┌──────────────┐
        │ Transaction 2│   │ Transaction 3│
        │  (Reading)   │   │ (Waiting...) │
        └──────────────┘   └──────────────┘
```

**다이어그램 해설**
1.  **Lock Table Entry**: 시스템은 데이터 행(Row #105)에 대한 잠금 정보를 유지합니다. 현재 상태는 **S-Lock**이 설정되어 있습니다.
2.  **Holders (T1, T2)**: T1이 먼저 S-Lock을 획득한 후, T2가 S-Lock을 요청하면 호환성(Compatibility) 검사를 통과하여 즉시 잠금을 획득하고 `Holders` 목록에 추가됩니다. 이때 두 트랜잭션은 서로 방해하지 않고 데이터를 읽습니다.
3.  **Waiters (T3)**: T3가 데이터를 수정하기 위해 **X-Lock (Exclusive Lock)**을 요청합니다. Lock Manager는 'S-Lock과 X-Lock은 상충됨'을 확인하고, T3를 `Waiters` 큐에 넣어 블록(Block)시킵니다. T1과 T2가 모두 Lock을 해제(Release)해야만 T3가 깨어나(Wake up) 잠금을 획득합니다.

**핵심 알고리즘 및 코드**

트랜잭션의 수명 주기 동안 S-Lock이 관리되는 의사 코드(Pseudo-code)입니다.

```sql
-- [Database SQL Syntax Example]
-- 트랜잭션 시작
BEGIN;

-- 데이터 조회와 함께 S-Lock 획득 (명시적 잠금)
-- 일반 SELECT는 격리 수준에 따라 다르지만, FOR SHARE는 명시적으로 S-Lock 요청
SELECT * FROM products WHERE id = 100 FOR SHARE;

-- ... 데이터 읽기 및 비즈니스 로직 처리 ...

-- 트랜잭션 종료 시 자동으로 S-Lock 해제 (Release)
COMMIT;
```

> **📢 섹션 요약 비유**: S-Lock의 동작은 **'스키장 리프트'**와 유사합니다. 한 명이 탄 후에도 다른 사람이 바로 탈 수 있지만(S-Lock 호환), 이미 탄 사람들이 모두 내릴 때까지 리프트를 멈추고 정비하려는 직원(X-Lock)은 대기해야 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: S-Lock vs X-Lock vs Intent Lock**

| 구분 | S-Lock (Shared) | X-Lock (Exclusive) | Note |
|:---|:---:|:---:|:---|
| **목적** | 데이터 읽기 (Read) | 데이터 쓰기 (Write/Update/Delete) | |
| **동시 허용** | 여러 트랜잭션 동시 가능 | 오직 하나의 트랜잭션만 가능 | |
| **호환성** | S-Lock과 호환 | 모든 잠금과 배타 | |
| **Lock Escalation** | 발생하지 않음 | 갯수가 많아지면 테이블 락으로 변환 가능 | |

**과목 융합 관점 (OS & Architecture)**

1.  **OS와의 연계 (Readers-Writers Problem)**:
    데이터베이스의 S-Lock은 운영체제 커널의 **Readers-Writers Lock** 소프트웨어 패턴을 구현한 것입니다. OS 관점에서 S-Lock은 스레드 간 데이터 경쟁(Race Condition)을 방지하면서도 읽기 병렬성을 높이는 세마포어(Semaphore)의 일종으로 볼 수 있습니다.

2.  **MVCC (Multi-Version Concurrency Control)와의 시너지/오버헤드**:
    -   **전통적 Locking (Locking Based)**: S-Lock을 건다. 단순하지만, 읽기가 많아도 쓰기가 막히면 병목이 발생할 수 있음.
    -   **MVCC (Oracle, PostgreSQL 등)**: 읽기 작업 시 S-Lock을 걸지 않고 **Undo Log**를 이용해 이전 버전의 스냅샷(Snapshot)을 읽음.
    -   **융합**: 최신 DBMS는 S-Lock과 MVCC를 혼합 사용합니다. 예를 들어, `FOR UPDATE` 구문을 사용할 때는 명시적으로 X-Lock을, 일반 조회는 MVCC를 사용하여 S-Lock 오버헤드를 제거합니다. 하지만 **Foreign Key Constraint 검사** 등에서는 여전히 S-Lock이 내부적으로 사용되어 무결성을 보장합니다.

> **📢 섹션 요약 비유**: S-Lock과 MVCC의 관계는 **'생방송(Full Locking)'과 '녹화 방송(MVCC)'**의 차이와 같습니다. 생방송(전통적 S-Lock)은 실시간 상황을 보장하지만, 진행자가 수정할 때는 시청자들이 기다려야 합니다. 녹화 방송(MVCC)는 시청자가 지난 회차(스냅샷)를 볼 수 있어 방송(쓰기)에 방해를 받지 않습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **결제 금액 누적 조회 (금융권)**
    -   **상황**: 계좌의 잔액을 조회하여 총 자산을 계산하는 배치 작업 중.
    -   **문제**: S-Lock을 걸지 않고 조회(Repeatable Read 미보장)하면, 조회 도중 다른 트랜잭션이 잔액을 변경하여 **Phantom Read**나 부정합이 발생할 수 있습니다.
    -   **판단**: 데이터 정합성이 생명인 금융 거래에서는 **S-Lock을 명시적으로 사용(`WITH (HOLDLOCK, ROWLOCK)` 등)**하여 조회 시점의 데이터를 고정锁(Pinning)해야 합니다.

2.  **대시보드 통계 쿼리 (웹 서비스)**
    -   **상황**: 수만 건의 주문 테이블을 읽어 실시간 통계를 보여주는 대시보드.
    -   **문제**: 이때 S-Lock을 걸면, 주문 발생(쓰기)이 차단되어 전체 서비스 장애로 이어질 수 있습니다.
    -   **판단**: **NoLock** 힌트를 주거나 MVCC를 활용하여 과거 데이터를 읽음으로써, 쓰기 트랜잭션을 방해하지 않는 전략을 택해야 합니다. 즉, "약간의 오차를 감수하고 성능을 취한다"는 기술사적 판단이 필요합니다.

**도입 체크리스트**

| 구분 | 체크 항목 | 비고 |
|:---|:---|:---|
|**기술적**| S-Lock 대기 시간 초과(Timeout) 설정 여부 | 무한 대기 방지 |
|**운영적**| Lock Escalation(테이블 락 승격) 발생 빈도 모니터링 | 메모리 부족 시 발생 |
|**보안적**| 민감 데이터 조회 시 로그 및 감사(Audit) 남김 | S-Lock 획득 시도 기록 |

**안티패턴 (Antipattern)**
-   **락 승격(Lock Promotion) 과정에서의 교착상태(Deadlock)**:
    T1이 S-Lock을 가진 상태에서 X-Lock으로 업그레이드를 시도하는 동안, T2가 S-Lock을 획득하려 하면 서로가 서로를 기다리는 **Deadlock**이 발생합니다.
    > **해결**: 처음부터 X-Lock을 획득하거나, 애초에 S-Lock을 사용하지 않고 Optimistic Locking(Version Column)을 사용합니다.

> **📢 섹션 요약 비유**: S-Lock을 잘못 사용하는 것은 **'좁은 골목에서의 양보하기 싸움'**과 같습니다. 서로 양보(공유)하려다 꼬여서(Circular Dependency) 아무도 못 가는 교통 체증(Deadlock)이 발생할 수 있으니, 골목 진입 전에 "내가 그냥 빠르게 지나갈지(Skip Lock), 아니면 확실히 차단하고 들어갈지(Pessimistic)"를 미리 결정해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

S-Lock을 올바르게 구현하고 활용했을 때의 기대 효과는 다음과 같습니다.

| 항목 | 도입 전 (Lock 미사용) | 도입 후 (S-Lock 활용) | 기대 효과 |
|:---|:---|:---|:---|
| **데이터 정합성** | Dirty Read 발생 가능 | Read Committed/Repeatable Read 보장 | 데이터 신뢰도 100% 확보 |
| **동시성(Concurrency)** | 쓰기 시 모든 읽기 차단 (낮은 TPS) | 읽기 작업 병렬 처리 (높은 T