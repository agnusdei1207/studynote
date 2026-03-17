+++
title = "213. 락킹 (Locking) 기법 - 상호 배제의 핵심"
date = "2026-03-14"
[extra]
title = "213. 락킹 (Locking) 기법 - 상호 배제의 핵심"
date = "2026-03-16"
categories = "studynote-database"
id = 213
+++

# 213. 락킹 (Locking) 기법 - 상호 배제의 핵심

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 락킹(Locking)은 동시성 제어(Concurrency Control)의 핵심 메커니즘으로, 트랜잭션(Transaction)이 데이터베이스 자원에 접근할 때 상호 배제(Mutual Exclusion)를 통해 데이터的无결성(Integrity)을 보장하는 논리적 잠금 장치이다.
> 2. **가치**: ACID(Atomicity, Consistency, Isolation, Durability) 특성 중 'I(Isolation)'를 물리적으로 구현하며, 비관적 동시성 제어(Pessimistic Concurrency Control)를 통해 충돌을 선제적으로 차단하여 데이터 정합성을 100% 보장한다.
> 3. **융합**: OS(Operating System)의 세마포어(Semaphore) 및 뮤텍스(Mutex) 개념과 논리적으로 동일하며, 분산 시스템 환경에서는 분산 락 매니저(Distributed Lock Manager)를 통해 클러스터링된 노드 간의 데이터 일관성을 유지한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
락킹(Locking)은 다중 트랜잭션 환경에서 데이터베이스의 일관성을 해치는 것을 방지하기 위해, 트랜잭션이 데이터를 접근하는 동안 다른 트랜잭션의 간섭을 차단하는 가장 보편적인 기법입니다. 이는 데이터베이스 관리 시스템(DBMS, Database Management System)이 제공하는 동시성 제어의 기초로서, 자원을 '잠금(Lock)'과 '해제(Unlock)' 상태로 관리함으로써 원자성(Atomicity)과 직렬 가능성(Serializability)을 보장합니다.

**💡 비유**
락킹은 마치 **'회의실 예약 시스템'**과 같습니다. 어떤 팀이 회의실을 예약하고 회의를 진행하는 동안(Lock), 다른 팀은 문이 잠겨 있어 들어가지 못하고 기다려야 합니다. 회의가 끝나야 비로소 다음 팀이 사용할 수 있습니다(Unlock).

**등장 배경: ① 기존 한계 → ② 혁신적 패러다임 → ③ 현재의 비즈니스 요구**
1.  **한계**: 초기 파일 시스템이나 트랜잭션 처리가 없는 DB 환경에서는 동시에 데이터를 수정할 경우 '갱신 손실(Lost Update)'이나 '모순성 읽기(Inconsistent Read)'가 발생하여 데이터 신뢰도가 급격히 떨어졌습니다.
2.  **혁신**: 트랜잭션 개념이 도입되면서, 연산의 묶음(Atomic Operation)을 보호할 논리적 경계선이 필요해졌고, 이를 해결하기 위해 2단계 락킹 규약(2PL, Two-Phase Locking)과 같은 엄격한 protocol이 정립되었습니다.
3.  **현재**: 클라우드 및 분산 DB 환경에서 수천 TPS(Transactions Per Second)를 처리해야 하는 현대 시스템에서, 락킹의 세밀한 튜닝(Granularity Tuning)은 성능 병목을 해결하는 핵심 이슈가 되었습니다.

**ASCII 다이어그램: 트랜잭션 충돌 시나리오**
```text
[시나리오: A와 B가 동시에 100만 원 잔고를 인출하는 경우]

Timeline ──────────────────────────────────────────────────────▶
         T1 (Transaction A)            T2 (Transaction B)
            │                              │
 1.  READ Balance (1000)                 │
            │                              │
 2.          │                    READ Balance (1000) 
            │          ────▶            (A가 아직 쓰지 않아 1000 조회)
            │                              │
 3.  UPDATE 900 (100-100)                 │
            │                              │
 4.  COMMIT                              │
            │          ────▶       UPDATE 900 (100-100)
            │                              │
 5.  (잔고: 900)                   COMMIT (잔고: 900)

  [결과]: 200원이 인출되었는데 잔고는 800원이 아닌 900원 남음 (Lost Update)
  [해결]: T1이 READ할 때 Lock을 걸면, T2는 T1이 끝날 때까지 대기해야 함.
```
**(해설)**
위 다이어그램은 락킹이 없을 때 발생하는 대표적인 데이터 무결성 침해 사례인 '갱신 손실(Lost Update)'을 보여줍니다. T1과 T2가 동시에 같은 데이터를 읽고, 서로의 쓰기 작업을 인지하지 못한 채 순차적으로 덮어쓰면서 결과적으로 하나의 인출만 반영되는 문제가 발생합니다. 이를 방지하기 위해 T1이 데이터를 읽는 시점부터 Lock을 걸어 T2의 접근을 물리적으로 차단해야 올바른 계산(800원)이 가능해집니다.

**📢 섹션 요약 비유**
> 마치 횡단보도 신호등과 같습니다. 초록색 신호(Lock 획득)를 받은 사람만 건널 수 있고, 뒤에 오는 사람들은 신호가 바뀔 때까지(Unlock) 대기해야 하여 서로 충돌 없이 안전하게 건너게(트랜잭션 완료) 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**
락킹 시스템은 DBMS의 커널(Kernel) 레벨에서 복잡한 자료구조를 통해 동작합니다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 주요 프로토콜/명령어 |
|:---|:---|:---|:---|
| **Lock Manager (LM)** | 락의 허가 및 대기열 관리 | 요청된 Lock이 Lock Table(Lock Table)의 Compatibility Matrix(호환성 매트릭스)를 검사하여 허가/대기 결정 | `LOCK-S()`, `LOCK-X()` |
| **Lock Table** | 락 상태 정보 저장 | 해시 테이블(Hash Table) 구조로 데이터 객체별로 현재 Lock을 보유한 트랜잭션 ID와 대기 큐(Waiting Queue) 유지 | Hash(PageID, RowID) |
| **Granularity** | 락의 단위 조절 | DB 전체에서 비트(Bit) 하나까지. 크기가 작을수록 동시성 증가 but 관리 비용 증가 | Database, Table, Page, Row |
| **2PL (Two-Phase Locking)** | 직렬 가능성 보장 | Growing Phase(잠금만 획득) → Shrinking Phase(잠금만 해제)의 엄격한 구분 | Conservative, Strict variants |
| **Timeout/Detection** | 교착 상태 해소 | 일정 시간 초과 시 Rollback 또한 Wait-for Graph 순환 탐지 | `SET LOCK_TIMEOUT`, `DEADLOCK_PRIORITY` |

**ASCII 구조 다이어그램: Lock Manager 아키텍처**
```text
+-------------------+      Request (Lock-S/X)      +---------------------+
| Transaction T1    | ───────────────────────────▶ │                     |
|                   │                               │  Lock Manager (LM)  │
+-------------------+                               │                     │
        ▲                                          │  ┌───────────────┐  |
        │                                          │  │ Lock Table    │  |
        │ Permission/Deny                          │  │ (Hash Map)    │  |
        │                                          │  │ Item: Row_A   │  |
        │                                          │  │ - Granted: T2 │  |
        │                                          │  │ - Wait: T1, T3│  |
+-------------------+      Status/Grant            │  └───────────────┘  |
| Transaction T2    | ◀─────────────────────────── │                     |
| (Running)         │                               +---------------------+
+-------------------+                                        ▲
        │                                                    │
        │                                                    │
        ▼                                                    ▼
+-------------------+                                +---------------------+
| Data Resource     │  Access Control               | System Resources    |
| (Table/Row/Page)  │ ◀───────────────────────────── │ (Memory/CPU)        |
+-------------------+                                +---------------------+
```
**(해설)**
이 아키텍처는 트랜잭션이 데이터에 직접 접근하기 전에 반드시 거쳐야 할 'Lock Manager'라는 관문을 보여줍니다.
1.  **요청**: T1이 데이터 조작을 시도하면 LM에게 Lock을 요청합니다.
2.  **검증**: LM은 메모리 상의 Lock Table을 조회하여, 현재 해당 자원을 다른 트랜잭션(T2)이 사용 중인지, 그리고 요청한 Lock 종류(S 또는 X)가 호환되는지 확인합니다.
3.  **판단**: 호환된다면 즉시 `Granted` 상태를 반환하고, 충돌한다면 `Wait` 큐에 넣어 T1을 Sleep 상태로 만듭니다.
4.  **통제**: 이 과정을 통해 논리적인 동시성 제어가 물리적인 자원 접근보다 선행되도록 설계되었습니다.

**심층 동작 원리: 락의 생애 주기와 호환성**
락킹의 핵심은 '공유 락(Shared Lock, S-Lock)'과 '배타 락(Exclusive Lock, X-Lock)'의 상호작용에 있습니다.

```text
[Lock Compatibility Matrix]
      ┌───────────── Current Lock Holder ─────────────┐
      │                  S-Lock         X-Lock        │
      │               (Read Mode)     (Write Mode)    │
  N ───┼──────────────────────────────────────────────│───────
  e ───┼──────────────────────────────────────────────│───────
  w    │  S-Lock      │    YES (O)     │    NO (X)    │
  R    │  (Read)      │  (동시 읽기)   │ (쓰기 차단)  │
  q    ├──────────────┼────────────────┼──────────────┤
  u    │  X-Lock      │    NO (X)      │    NO (X)    │
  e    │  (Write)     │ (읽기 차단)    │ (완전 독점)  │
  s ───┴──────────────┴────────────────┴──────────────┴───────
```

**핵심 알고리즘: 2단계 락킹 프로토콜 (2PL Protocol)**
직렬 가능성(Serializability)을 보장하기 위한 수학적 증명이 된 알고리즘입니다.
1.  **Growing Phase (확장 단계)**: 트랜잭션이 Lock을 획득하기만 하고, 해제하지 않는 단계입니다.
2.  **Shrinking Phase (축소 단계)**: 트랜잭션이 Lock을 해제하기만 하고, 새로운 Lock을 획득하지 않는 단계입니다.
*(코드: Pseudo-code for Lock Request)*
```python
def request_lock(transaction, resource, lock_mode):
    current_lock = get_lock_from_table(resource)
    
    # 1. 호환성 확인 (Compatibility Check)
    if is_compatible(current_lock, lock_mode):
        grant_lock(transaction, resource, lock_mode)
        log_status(f"{transaction} acquired {lock_mode} on {resource}")
    else:
        # 2. 충돌 시 대기 (Wait) 또는 Abort
        add_to_wait_queue(transaction, resource, lock_mode)
        block_transaction(transaction) 
        # 실무에서는 타임아웃 설정 필수
        if wait_time > TIMEOUT_THRESHOLD:
            raise DeadlockError()
```

**📢 섹션 요약 비유**
> 마치 **독서실 열람실 좌석**과 같습니다. 
> *   **S-Lock**: '혼자 공부 중' 표시. 옆 사람이 끼어들 수는 없지만, 옆에서 힐끔거리며 함께 볼 수는 있습니다(Read 공유).
> *   **X-Lock**: '칸막이 세우고 비밀 업무' 중. 누구도 내용을 볼 수도, 건드릴 수도 없습니다(Write 독점).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: Locking vs. Optimistic (MVCC)**
데이터베이스의 동시성 제어는 크게 비관적(Pessimistic) 락킹과 낙관적(Optimistic) 방식(MVCC 등)으로 나뉩니다.

| 비교 항목 | 락킹 (Locking) | MVCC (Multi-Version Concurrency Control) |
|:---|:---|:---|
| **기본 철학** | **비관적**: 충돌이 발생할 것이라 가정하고 선제적으로 차단 | **낙관적**: 충돌이 드물 것이라 가정하고 복사본(History) 제공 |
| **성능 특성** | 경쟁(Contention)이 심한 환경에서는 **Wait 비용**이 크나, 무결성은 즉시 보장됨 | **Read 작업이 Block되지 않음** (Non-blocking Read). 갱신 충돌 시 Rollback 비용 발생 |
| **주요 사용처** | 금융권, 재무 회계 (잔고 갱신 등 정합성이 절대적인 곳) | 웹 서비스, 포털, SNS (조회(Read)가 쓰기(Write)보다 압도적으로 많은 곳) |
| **구현 복잡도** | Lock Manager의 관리 오버헤드, Deadlock 탐지 로직 필요 | Undo/Redo Log, 버전 체이닝 관리 필요 |

**과목 융합 관점**
1.  **OS (운영체제)와의 융합**: 락킹은 OS의 `Semaphore`나 `Mutex`와 같은 **Critical Section(임계 영역) 문제**의 해결책입니다. 다만 DB 락은 단일 프로세스 내의 스레드 동기화가 아니라, **디스크 상의 데이터 레코드**를 대상으로 한 훨씬 복잡하고 무거운 자원 관리 메커니즘입니다.
2.  **네트워크와의 융합**: 분산 DB 환경(Distributed DB)에서는 2PL(2-Phase Locking)과 **2PC(2-Phase Commit)** 프로토콜이 필수적으로 결합됩니다. 락을 걸고 트랜잭션을 커밋할 때, 네트워크를 통해 연관된 모든 노드에게 '준비(Prepare)'와 '확정(Commit)' 신호를 보내 원자성을 보장합니다.

**ASCII 다이어그램: 시스템 성능 영향 분석**
```text
[Throughput(처리량) 그래프 분석]

Throughput
  ▲
  │     ┌───── Level (Table Lock)
  │     │    (낮은 동시성, 빠른 관리)
  │     │_____
  │           \.
  │            \.
  │             \..............━━━ (Row Lock)
  │                              (높은 동시성, 높은 관리 비용)
  │
  └────────────────────────────────────▶ Concurrency Level (동시 사용자 수)

  [Insight]:
  1. 소규모 사용자에서는 Row Lock의 오버헤드로 인해 Table Lock이 더 빠를 수 있음.
  2. 대�