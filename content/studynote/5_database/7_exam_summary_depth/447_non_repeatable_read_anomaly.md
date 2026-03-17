+++
title = "447. 비반복 읽기(Non-Repeatable Read) - 변덕스러운 데이터"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 447
+++

# 447. 비반복 읽기(Non-Repeatable Read) - 변덕스러운 데이터

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비반복 읽기(Non-Repeatable Read)는 단일 트랜잭션(Transaction) 내에서 **동일한 레코드를 두 번 이상 조회 시, 중간에 다른 트랜잭션이 데이터를 수정(Modify) 및 커밋(Commit)하여 결과값이 상이하게 나타나는 현상**을 의미합니다.
> 2. **가치**: 데이터 일관성(Consistency)이 깨지는 대표적인 동시성 제어 문제로, 재고 확보, 금융 결산 등 데이터의 '상태'가 시간 축상에서 변하면 안 되는 비즈니스 로직에서 치명적인 논리적 오류(Anomaly)를 유발합니다.
> 3. **융합**: DBMS의 트랜잭션 격리 수준(Transaction Isolation Level) 중 `Read Committed` 수준에서 발생하며, 이를 방지하기 위해 `Repeatable Read` 격리 수준 또는 MVCC(Multi-Version Concurrency Control) 기반의 스냅샷(Snapshot) 기술이 필수적으로 융합됩니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의 및 철학**
비반복 읽기(Non-Repeatable Read)는 데이터베이스 트랜잭션의 원자성(Atomicity)과 고립성(Isolation)이 침해되는 현상 중 하나입니다. 구체적으로, 어떤 트랜잭션 T1이 특정 데이터를 읽은 후, 트랜잭션을 종료(Commit/Rollback)하기 전까지 동일한 질의(Query)를 다시 수행했을 때, 중간에 개입한 트랜잭션 T2가 데이터를 변경하고 커밋함으로써 T1이 서로 다른 데이터 값을 관찰하는 상황을 말합니다. 이는 "내가 보고 있는 데이터는 나의 트랜잭션이 끝날 때까지 세상의 다른 변화로부터 보호받아야 한다"는 데이터베이스 일관성의 철학에 위배됩니다.

**💡 비유: 움직이는 사다리**
높은 곳의 물건을 바꾸기 위해 사다리를 올라갔습니다(데이터 조회). 잠시 내려와서 다른 도구를 가져오는 사이에, 누군가가 와서 그 사다리를 1m 옮겨 버렸습니다(데이터 수정). 다시 올라가려 하던 당신은 허공을 밟고 떨어지게 됩니다. 사다리(데이터)의 위치가 조회 시점과 재조회 시점이 달라졌기 때문입니다.

**등장 배경 및 비즈니스 임팩트**
1.  **기존 한계**: 초기 데이터베이스 시스템은 성능을 위해 데이터를 읽을 때 잠금(Lock)을 최소화하고, 단순히 커밋된 데이터만 읽는(`Read Committed`) 방식을 선호했습니다. 이는 동시 처리량(Throughput)은 높였으나, 데이터의 '상태'가 시간에 따라 변동성을 가지는 문제를 안고 있었습니다.
2.  **혁신적 패러다임**: 금융, 재무 회계, 재고 관리 등 분야에서는 "한 번 읽은 데이터는 트랜잭션이 끝날 때까지 변하면 안 된다"는 요구가 강력하게 제기되었습니다. 이에 따라 더욱 엄격한 격리 수준(Repeatable Read, Serializable)과 비잠금 읽기(Non-locking Read)를 위한 MVCC 기술이 도입되었습니다.
3.  **현재의 비즈니스 요구**: 실시간 분석(OLAP)과 거래(OLTP)가 혼재하는 환경에서, 비반복 읽기는 리포트의 신뢰성을 떨어뜨리고 '신뢰할 수 없는 읽기'를 통해 잘못된 의사결정을 내리게 만드는 주원인이 됩니다.

**📢 섹션 요약 비유**
> 비반복 읽기는 **"사진을 찍기 위해 카메라 렌즈를 초점을 맞췄는데, 셔터를 누르는 사이에 피사체가 옆으로 이동해버려서 완성된 사진이 엉뚱하게 나오는 상황"**과 같습니다. 촬영자(트랜잭션)는 초점(데이터)이 고정되기를 기대했으나, 외부의 간섭으로 인해 엉뚱한 결과를 얻게 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (Component Analysis)**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/메커니즘 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **TX-Manager (Transaction Manager)** | 트랜잭션의 생명주기 관리 | Begin, Commit, Rollback 명령을 관리하고 트랜잭션 ID를 할당 | ACID 보장 | **건물 관리인** |
| **Lock Manager (Latch/Lock)** | 데이터 동시 접근 제어 | 읽기(S-Lock), 쓰기(X-Lock) 요청을 관리하고 충돌 시 대기 큐(Wait Queue)에 할당 | 2PL (Two-Phase Locking) | **열쇠 관리실** |
| **Buffer Pool (Cache)** | 디스크 I/O 최소화 및 데이터 버전 관리 | 데이터 페이지를 메모리에 로딩하며, MVCC 환경에서는 Undo Log를 통해 이전 버전 유지 | LRU Algorithm | **작업 대기 테이블** |
| **Undo Log (Rollback Segment)** | 변경 전 데이터 보관 | T2가 데이터를 변경하기 전, T1이 읽고 있던 원본 데이터를 백업 (MVCC 핵심) | Write-Ahead Logging | **수정 전 원본 보관함** |
| **Isolation Level Validator** | 질의 실행 계획 수립 | `SELECT` 시점에 Lock을 걸 것인지, 혹은 Snapshot을 읽을지 결정 | Read Committed vs Repeatable Read | **규칙 집** |

**ASCII 구조 다이어그램: 트랜잭션 메모리 레이아웃 및 흐름**

```text
[ Transaction Memory Layout & Flow ]

┌─────────────────────────────────────────────────────────────────────┐
│                          DB STORAGE (Disk)                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Data Page: User_ID='A' | Score = 100                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Load
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       BUFFER POOL (Memory)                          │
│  ┌───────────────┐          ┌────────────────────────────────────┐ │
│  │ Buffer Frame  │          │ Undo Log Chain (MVCC Versions)     │ │
│  │ ───────────── │          │                                    │ │
│  │ Val: 200      │◀─────────│ Ptr 1 ──▶ [Ver 1: 100] (T1 view)  │ │
│  │ (Current)     │  Update  │         [Ver 2: 200] (T2 commit)  │ │
│  └───────────────┘          └────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
        │                       ▲
        │ X-Lock (Write)        │ S-Lock / Snap
        ▼                       │
┌───────────────────────┐  ┌───────────────────────┐
│  Transaction T2       │  │  Transaction T1       │
│  (UPDATE Score=200)   │  │  (SELECT Score)       │
│                       │  │                       │
│  1. Acquire X-Lock    │  │  1. Read Ver 1 (100)  │
│  2. Write Buffer      │  │  2. Processing...     │
│  3. Write Undo Log    │  │  3. Read again:       │
│  4. COMMIT            │  │     → Refetch?        │
│     (Visible to All)  │  │     → Ver 2 (200)?    │
└───────────────────────┘  └───────────────────────┘
   ▲                                    │
   │                                    │
   └────── If Isolation = READ_COMMITTED ──▶ T1 sees '200' (Non-Repeatable)
```

**심층 동작 원리 (Deep Dive Mechanics)**
1.  **Phase 1 (최초 읽기)**: T1이 `SELECT Score FROM User WHERE ID='A'`를 실행합니다. `Read Committed` 수준에서는 데이터 페이지에 Shared Lock(S-Lock)을 걸었다가 즉시 해제할 수 있습니다(T2의 수정을 막지 않음). T1은 값 100을 가져옵니다.
2.  **Phase 2 (간섭 및 수정)**: T2가 해당 레코드에 대해 Exclusive Lock(X-Lock)을 획득하고 값을 200으로 수정합니다. T2가 `COMMIT`을 수행하면 변경 사항이 영구화되어 DB Buffer의 최신 값이 됩니다.
3.  **Phase 3 (재조회 및 Anomaly 발생)**: T1이 다시 `SELECT Score...`를 실행합니다. `Read Committed`는 "커밋된 가장 최신 데이터"를 읽는 것이 원칙이므로, T2가 변경하고 커밋한 200을 읽어옵니다.
4.  **결과**: T1 입장에서 트랜잭션 시작 시 100점이었던 점수가 200점이 되었습니다. 이는 T1의 논리적 흐름(예: 100점 기준 혜택 제공)을 깨뜨립니다.

**핵심 알고리즘 및 모델**
```sql
-- Scenario Demonstration

-- Time t1: T1 starts transaction
BEGIN TRANSACTION T1;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Time t2: T1 reads score (Expected: 100)
SELECT Score FROM Users WHERE ID = 'A'; 
-- Result: 100

-- Time t3: T2 starts and modifies data (Concurrently)
BEGIN TRANSACTION T2;
UPDATE Users SET Score = 200 WHERE ID = 'A';
COMMIT T2; -- Changes are now permanent and visible to others

-- Time t4: T1 reads again (Expecting 100, but getting...)
SELECT Score FROM Users WHERE ID = 'A';
-- Result: 200 ⚠️ NON-REPEATABLE READ DETECTED!

COMMIT T1;
```

**📢 섹션 요약 비유**
> **"규칙이 바뀌는 시합"**과 같습니다. 야구 게임에서 1회 말에 타석에 들어섰을 때는 '스트라이크 존이 넓었다'(Score=100)고 판단했는데, 2회초에 규칙 위원회가 존을 좁히고(T2=Update), 다시 내 타석이 돌아왔을 때 '스트라이크 존이 좁아져서'(Score=200) 혼란이 오는 것과 같습니다. 게임(트랜잭션) 도중 규칙이 바뀌면 정확한 플레이(로직 수행)가 불가능해집니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: Anomaly 유형별 분석**

| 비교 항목 | 비반복 읽기 (Non-Repeatable Read) | 더티 읽기 (Dirty Read) | 팬텀 읽기 (Phantom Read) |
|:---|:---|:---|:---|
| **정의** | **수정(Modify)**된 데이터의 재조회 시 값 변경 | 커밋되지 **않은(Uncommitted)** 데이터 읽기 | 검색 결과의 **범위(Range)** 내 새로운 행(Row)의 출현/소멸 |
| **발생 원인** | T2의 UPDATE + COMMIT | T2의 UPDATE + **NO COMMIT** (Rollback 가능성) | T2의 INSERT/DELETE + COMMIT |
| **발생 격리 수준** | `Read Committed` | `Read Uncommitted` | `Read Committed`, `Repeatable Read` |
| **해결 방안** | `Repeatable Read` (Lock 또는 MVCC) | `Read Committed` 이상 | `Serializable` (Range Lock) 또는 Next-Key Lock |
| **비즈니스 영향도** | **중고도**: 데이터 정합성 오류로 인한 계산 오류 | **고위험도**: Rollback 시 데이터 사라짐 (폐기) | **중위험도**: 집계 함수(COUNT, SUM) 오류 |
| **순수 기술적 관점**| 논리적(Logical) 불일치 발생 | 물리적(Physical) 불일치 발생 | 집합(Set) 기반 불일치 발생 |

**과목 융합 관점 (Convergence)**

1.  **운영체제(OS)와의 융합: Lock Manager & Semaphores**
    *   데이터베이스의 잠금(Lock) 메커니즘은 운영체제의 세마포어(Semaphore)나 뮤텍스(Mutex)와 본질적으로 같습니다. 비반복 읽기를 방지하기 위해 행(Row) 수준의 잠금을 유지하는 것은, 운영체제가 프로세스 간의 공유 자원 접근을 제어하는 `CS(临界区, Critical Section)` 문제 해결과 직결됩니다. 단, DB는 더 복잡한 계층 구조(Table -> Page -> Row)와 호환성 매트릭스(S-Lock vs X-Lock)를 가집니다.

2.  **네트워크와의 융합: Consistency Model**
    *   분산 데이터베이스 환경에서 비반복 읽기는 네트워크 지연(Latency)과 복제(Replication) 지연과 연결됩니다. RDBMS의 트랜잭션은 '강한 일관성(Strong Consistency)'을 보장하려 하지만, NoSQL 등 최신 시스템은 비반복 읽기를 허용하여 성능을 확보하는 '결국 일관성(Eventual Consistency)' 모델을 채택하기도 합니다. 즉, 비반복 읽기 허용 여부는 시스템의 **CAP 정리(Consistency, Availability, Partition tolerance)**에서의 'Trade-off' 결정 사항입니다.

**📢 섹션 요약 비유**
> **"스마트폰 vs 엽서"**의 차이와 같습니다. 비반복 읽기가 허용되는 것은 엽서를 보낸 것과 같습니다. 보내는 도중(Commit 전)에 내용이 바뀌어도 이미 도착한 엽서는 확인할 수 없습니다(Dirty Read 유사성 포함). 반면, 비반복 읽기가 허용되지 않는 것은 실시간 화상 통화와 같습니다. 내가 말하는 도중 상대방이 자리를 비우면, 내가 보는 화면은 멈추거나(잠금) 또는 마지막 모습을 계속 보여줍니다(MVCC). 데이터의 신선함(Freshness)과 안정성(Stability) 사이의 선택입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정 프로세스**

*   **시나리오 A: 은행 이체 시스템 (Financial Core Banking)**
    *   **상황**: 고객이 계�