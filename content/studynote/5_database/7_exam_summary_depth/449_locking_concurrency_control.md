+++
+++
title = "449. 동시성 제어 잠금(Locking) - 읽기와 쓰기의 교통정리"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 449
+++

# 449. 동시성 제어 잠금(Locking) - 읽기와 쓰기의 교통정리

## # 동시성 제어 잠금 (Locking)

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: DBMS의 트랜잭션 관리자(Transaction Manager, TM)가 제공하는 **상호 배제(Mutual Exclusion)** 메커니즘으로, 공유 데이터에 대한 접근을 직렬화(Serializability)하여 데이터의 무결성(Integrity)을 물리적으로 보장하는 장치이다.
> 2. **가치**: 읽기(Read) 연산의 병렬성을 극대화하면서 쓰기(Write) 연산의 원자성을 보장하여, 다중 사용자 환경에서 **TPS (Transactions Per Second)**를 저하시키지 않고 데이터 정합성을 유지하는 핵심 트레이드오프(Trade-off) 수단이다.
> 3. **융합**: OS의 세마포어(Semaphore)나 커널 레벨 뮤텍스(Mutex)와 동일한 동시성 제어 원리를 기반으로, 분산 데이터베이스 환경에서는 분산 락 매니저(Distributed Lock Manager)를 통해 2PC (Two-Phase Commit)와 연동하여 글로벌 트랜잭션의 일관성을 제어한다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
잠금(Locking)은 데이터베이스 관리 시스템(DBMS)에서 동시에 실행되는 여러 트랜잭션이 데이터를 서로 방해하지 않도록 제어하는 가장 기초적이고 강력한 동시성 제어(Concurrency Control) 기법이다. 트랜잭션은 데이터베이스의 논리적 작업 단위로, 원자성(Atomicity), 일관성(Consistency), 고립성(Isolation), 지속성(Durability)인 ACID 특성을 만족해야 한다. 잠금은 특히 이 중 '고립성'을 보장하기 위해, 특정 데이터 항목에 대해 트랜잭션이 접근 권한을 선점(Lock)하고 반환(Unlock)하는 생명 주기를 관리한다.

**2. 작동 근간 및 철학**
잠금의 철학은 "모든 트랜잭션은 데이터에 접근하기 전에 허가를 받아야 하며, 서로 충돌하는 작업은 순서대로 실행되어야 한다"는 것에 있다. 이를 위해 DBMS는 **Lock Manager (LM)**라는 별도의 모듈을 두어 락의 할당, 검사, 해제를 담당한다. 트랜잭션이 데이터를 읽을 때는 '공유(Shared)' 모드로, 쓸 때는 '배타(Exclusive)' 모드로 요청하며, LM은 요청 간의 충돌(Conflict) 여부를 판단하여 승인(Grant)하거나 대기(Wait)시킨다.

**3. 등장 배경 및 비즈니스 요구**
① **기존 한계**: 초기 파일 시스템이나 단순한 데이터베이스에서는 데이터를 읽는 중에 다른 프로그램이 수정하면 '더티 리드(Dirty Read)'나 '반복 불가능한 읽기(Non-repeatable Read)'가 발생하여 데이터 신뢰도가 떨어졌다.
② **혁신적 패러다임**: 1970년대 System R 프로젝트 등에서 정의된 엄격한 2단계 락킹(Strict 2PL) 프로토콜이 도입되면서, 논리적 스케줄러 없이도 물리적인 잠금 메커니즘만으로 직렬화 가능성(Serializability)을 보장할 수 있게 되었다.
③ **현재 비즈니스 요구**: 금융 거래, 재고 관리, 예약 시스템 등 수만~수백만 명의 사용자가 동시에 접속하는 환경에서, 미세한 데이터 오차도 용납할 수 없는 '엄격한 일관성(Strict Consistency)'이 요구됨에 따라 Locking은 가장 필수적인 기술로 자리 잡았다.

> **📢 섹션 요약 비유**: Locking 시스템의 도입은 **'혼잡한 도심의 교통정리를 인파 신호등과 교통경찰로 체계화한 것'**과 같습니다. 눈으로 길만 보는 것(읽기)은 허용하되, 길을 건너는 것(쓰기)은 신호를 받고 혼자만 건너가게 하여, 서로 부딪히거나(충돌) 길을 엉망으로 만드는(오염) 사고를 예방하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 분석**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|
| **Lock Table** | 현재 활성화된 락의 상태를 저장하는 메모리 구조 | 해시(Hash) 구조를 사용하여 데이터 객체(OID)별로 락 소유자와 대기 큐(Queue)를 관리 | `Insert`, `Delete`, `Find` | 관리 대장 |
| **Lock Manager (LM)** | 트랜잭션의 락 요청을 처리하고 판단하는 엔진 | 요청을 받으면 Lock Table을 조회하고, 호환성을 검사한 후 Grant 또는 Block을 결정 | `Lock-S()`, `Lock-X()`, `Unlock()` | 교통통제소 |
| **S-Lock (Shared)** | 데이터를 읽기(Select) 위한 잠금 | 다른 S-Lock과는 호환되지만, X-Lock을 배제한다. 트랜잭션 종료 시 해제. | `SELECT ... FOR SHARE` | 열람실 좌석 예약 |
| **X-Lock (Exclusive)** | 데이터를 갱신(Update/Delete/Insert) 위한 잠금 | 모든 Lock(S, X)과 호환되지 않으며, 유일하게 데이터 변경을 허용한다. | `SELECT ... FOR UPDATE` | 수리 공구 독점 사용 |
| **Wait-for Graph** | 교착 상태(Deadlock) 탐지를 위한 그래프 | 노드는 트랜잭션, 간선은 대기(Wait) 관계를 나타내며 사이클(Cycle) 생성 여부를 감시 | Cycle Detection Algorithm | 대기 관계도 |

**2. 아키텍처 및 데이터 흐름**
아래 다이어그램은 트랜잭션이 데이터를 요청할 때 Lock Manager와 데이터베이스 버퍼(Buffer) 사이의 상호작용을 도식화한 것이다.

```text
   [ Transaction Workflow: Lock Acquisition & Execution ]

   Transaction A              Transaction B
       |                           |
       | (1) Lock-S(Item)           | (3) Lock-X(Item) [Concurrent Req]
       |----------------->          |----------------->|
       |                           |                 |
       v                           v                 v
  +-----------------------------------------------------------+
  |                    Lock Manager (LM)                       |
  |  1. Lookup Lock Table                                     |
  |  2. Check Compatibility (S vs ?)                           |
  |  3. Grant to A (O) | Block B (Wait -> Queue)              |
  +-----------------------------------------------------------+
       |                                            |
       | (2) Grant Lock                             | (Wait...)
       v                                            |
  +------------------+                    +-------------------+
  | Data Buffer Pool |                    | Wait Queue        |
  | [Item] Read      | <--- (Shared)      | T-B: Waiting...   |
  +------------------+                    +-------------------+
       |
       | (4) Commit/Unlock
       |
       v
  [ Release Lock ] --> (5) Signal Waking T-B
```

**해설**:
1. 트랜잭션 A가 데이터 읽기를 위해 `Lock-S(Item)`을 요청한다.
2. LM은 Lock Table을 확인하고, 해당 아이템에 경쟁하는 락이 없으므로 A에게 **Grant(승인)**한다. A는 데이터를 읽을 수 있다.
3. 이때 트랜잭션 B가 동일한 데이터에 대해 쓰기를 위해 `Lock-X(Item)`을 요청한다.
4. LM은 S-Lock과 X-Lock이 상호 배제(Half-X) 관계임을 확인하고, B를 **대기 큐(Wait Queue)**에 넣어 Block 시킨다.
5. A가 작업을 마치고 `Unlock`을 수행하면, LM은 대기 중이던 B를 깨워(Wakeup) 락을 획득하게 한다.

**3. 핵심 알고리즘 및 호환성 매트릭스 (Compatibility Matrix)**

```text
[ Lock Compatibility Matrix ]

       Holder (Current Lock)
       ┌───────────┬───────────┐
       │   S-Lock  │  X-Lock   │
  ─────┼───────────┼───────────┤
  Re-  │  O (Yes)  │  X (No)   │  <-- S-Lock 요청 (Read)
  quest│ (Read-Read│(Read-Wait │
       │  공유 가능)│  대기 필요)│
  ─────┼───────────┼───────────┤
       │  X (No)   │  X (No)   │  <-- X-Lock 요청 (Write)
       │(Write-Wait│(Write-Wait│
       │  대기 필요)│  대기 필요)│
       └───────────┴───────────┘
```

**💡 코드: Pseudo-code for Lock Request**
```python
def lock_request(transaction, data_item, lock_mode):
    # 1. Check if transaction already holds a lock
    if transaction.has_lock(data_item):
        return "Grant" # Lock Promotion or Re-entry
    
    # 2. Check Compatibility
    conflicts = get_conflicting_locks(data_item, lock_mode)
    if not conflicts:
        grant_lock(transaction, data_item, lock_mode)
        return "Grant"
    else:
        # 3. Handle Conflict (Blocking)
        add_to_wait_queue(transaction, data_item, lock_mode)
        # Deadlock detection might trigger here
        return "Wait"
```

> **📢 섹션 요약 비유**: 락의 작동 원리는 **'화장실 칸막이 이용 시스템'**과 같습니다. 문을 잠그지 않고 들여다보는 것(읽기, S-Lock)은 여러 명이 동시에 해도 서로 방해가 되지 않지만, 일단 들어가서 문을 잠그고 바지를 내리는 것(쓰기, X-Lock)은 철저히 배타적이어야 합니다. X-Lock을 건 사람이 나올 때까지 밖에서 줄을 서서 기다려야(Wait) 하는 것이 원칙입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Locking vs. Optimistic Concurrency**

| 비교 항목 (Criteria) | 잠금 (Locking / Pessimistic) | 낙관적 동시성 제어 (OCC / Optimistic) |
|:---|:---|:---|
| **기본 철학** | 트랜잭션 간 **충돌이 빈번**하다고 가정 (비관적) | 트랜잭션 간 **충돌이 드물**다고 가정 (낙관적) |
| **작업 단계** | 트랜잭션 시작 시 락 획득 | 데이터를 임시로 수정 후 Commit 시 검증(Validation) |
| **주요 오버헤드** | 락 관리, 대기 큐 관리, Deadlock 감지 비용 | Conflict 발생 시 **Rollback** 및 재시작 비용 |
| **적합한 환경** | **쓰기(Write) 경쟁이 치열한** OLTP 환경 | **읽기(Read) 위주**이거나 충돌이 드문 분석(OLAP) 환경 |
| **성능 지표** | Lock Contention ↑ -> Throughput ↓ | Conflict Rate ↑ -> Retry ↑ |

**2. 과목 융합 관점**
- **운영체제(OS)와의 관계**: DBMS의 Locking은 OS 커널이 제공하는 **Mutex (Mutual Exclusion)**나 **Semaphore** 메커니즘을 기반으로 구현되지만, 사용자 레벨(User-Level)에서 DBMS가 직접 관리하는 LWLock(Lightweight Lock) 등을 사용하여 컨텍스트 스위칭(Context Switching) 오버헤드를 줄이는 최적화를 수행한다. 또한, Deadlock 해결을 위해 OS의 **Banker's Algorithm**과 유사한 교착 상태 회피 기법을 응용한다.
- **네트워크 분야와의 관계**: 분산 DB 환경에서는 **2PL (Two-Phase Locking)** 프로토콜이 네트워크 지연(Latency)에 민감하다. 로컬의 Lock Manager가 원격의 Lock Coordinator와 통신하여 글로벌 락(Global Lock)을 획득하는 과정에서 **RPC (Remote Procedure Call)** 지연이 발생하며, 이를 해결하기 위해 Distributed Lock Management (DLM) 기술이 요구된다.

> **📢 섹션 요약 비유**: Locking은 **'철저한 보안 검문대(체크포인트)'**와 같습니다. 모든 사람이 통과할 때마다 신분증을 확인하고 무기를 검사(잠금 획득)하여 사고를 미리 막는 방식(Pessimistic)이라면, 낙관적 제어는 **'개방식 이벤트장'**처럼 입장은 자유롭게 둔다가 나갈 때 문제가 있었는지 확인(Optimistic Validation)하는 방식입니다. 사람이 붐비는 시간에는 검문대가 더 안전하지만, 한산할 때는 개방식이 더 빠릅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**
- **시나리오 1: 금융 시스템의 잔액 수정 (Update)**
  - **문제**: 계좌 이체 시 A에서 돈을 빼고 B에 넣는 도중, 다른 트랜잭션이 A의 잔액을 조회하면 어떻게 될까?
  - **판단**: 반드시 **Strong Strict 2PL**을 적용하여 트랜잭션 수행 중 모든 Lock을 유지하고 Commit되는 순간에만 해제해야 한다. 이를 통해 '팬텀 리드(Phantom Read)'를 방지하고 A->B 간의 데이터 이동 중간 상태를 노출시키지 않는다.
  
- **시나리오 2: 대량의 배치 작업 (Batch Insert)**
  - **문제**: 밤마다 수천만 건의 데이터를 적재하는데 행(Row) 단위 Lock이 너무 많이 발생해 메모리가 부족하다.
  - **판단**: **Lock Escalation (락 에스컬레이션)** 전략을 사용한다. 특정 개수(예: 5000개) 이상의 행 락이 발생하면 DBMS가 자동으로 테이블 전체 락(Table Lock)으로 상향 조정하여 메모리 사용량을 최적화한다. 단, 이때 다른 사용자의 접근이 전면 차단되므로 시스템 부하가 적은 시간대에 스케줄링해야 한다.

**2. 도입 체크리스트**
- **[기술적]** 트랜잭션의 길이를 최소화하여 **Lock