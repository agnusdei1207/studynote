+++
title = "206. 연쇄 복귀 (Cascading Rollback) - 장애의 도미노 현상"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 206
+++

# 206. 연쇄 복귀 (Cascading Rollback) - 장애의 도미노 현상

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 연쇄 복귀(Cascading Rollback)는 트랜잭션의 원자성(Atomicity)이 깨지는 위험 상황으로, 특정 트랜잭션의 **Rollback (Rollback)**이 해당 트랜잭션이 생성한 **Dirty Data (Uncommitted Data)**를 참조했던 다른 트랜잭션들의 강제 취소를 유발하여 시스템 전체의 안정성을 위협하는 현상이다.
> 2. **가치**: 데이터베이스의 회복(Recovery) 비용을 기하급수적으로 증가시키며, 이미 완료(Commit)된 작업을 취소해야 하므로 사용자 신뢰도 하락 및 서비스 중단(Undue Rollback)을 초래할 수 있는 심각한 성능 저하 요인이다.
> 3. **융합**: 트랜잭션 관리자(Transaction Manager, TM)와 병행 제어(Concurrency Control) 기술이 교차하는 핵심 지점이며, ACID 속성 중 특히 **Isolation (격리성)**과 **Atomicity (원자성)**를 보장하기 위해 **Strict 2PL (Strict Two-Phase Locking)** 등의 강력한 제어 기법이 요구된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**연쇄 복귀(Cascading Rollback)**란 데이터베이스 트랜잭션 처리 과정에서, 특정 트랜잭션(T1)이 장애나 오류로 인해 롤백(Rollback) 수행될 때, T1의 미확정 데이터(Dirty Read)를 참조하여 작업을 수행했던 다른 트랜잭션(T2, T3...)들이 논리적으로 잘못된 상태가 되어, T1뿐만 아니라 연관된 트랜잭션들까지 연쇄적으로 작업을 취소해야 하는 현상을 의미합니다.

이는 **ACID(Atomicity, Consistency, Isolation, Durability)** 속성 중 '원자성'을 보장하기 위한 불가피한 조치이지만, 시스템의 처리량(Throughput)을 급격히 떨어뜨리고 **Undo(취소)** 연산의 복잡도를 높이는 주요 원인이 됩니다.

#### 2. 등장 배경 및 기술적 한계
데이터베이스의 동시성 제어(Concurrency Control) 초기에는 성능 향상을 위해 트랜잭션이 커밋되지 않은 데이터를 다른 트랜잭션이 읽을 수 있도록 허용하는 경우가 많았습니다. 그러나 이는 다음과 같은 심각한 문제를 야실했습니다.
1.  **데이터 불일치**: 원본 트랜잭션이 취소되었음에도 불구하고, 그 데이터를 기반으로 연산을 마친 자식 트랜잭션이 유효한 것처럼 존재하게 되는 모순 발생.
2.  **복구 오버헤드**: 하나의 실패가 수많은 정상 작업들을 무효화시키면서, 시스템 전체의 자원(CPU, I/O)을 낭비하게 됨.

이를 해결하기 위해 현대의 DBMS는 격리 수준(Isolation Level)을 조절하거나 **Strict 2PL(Strict Two-Phase Locking)**과 같은 프로토콜을 도입하여 연쇄 복귀를 원천 차단하는 설계로 진화하고 있습니다.

#### 📢 섹션 요약 비유
연쇄 복귀는 **"완공되지 않은 모래성 위에 얹어 놓은 두 번째 성탑"**과 같습니다. 아래쪽 모래성(첫 번째 트랜잭션)이 무너지면, 그 위에 올려놓았던 두 번째 성탑(의존하는 트랜잭션)도 지탱할 곳을 잃고 함께 무너질 수밖에 없습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 분석
연쇄 복귀 발생 시 시스템 내부의 주요 구성 요소들이 어떻게 상호작용하는지 분석합니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 (Internal Logic) | 연관 프로토콜/기술 |
| :--- | :--- | :--- | :--- |
| **RM (Recovery Manager)** | 회복 관리자 | 트랜잭션 실패 감지 시 **Undo Log**를 분석하여 변경 전 데이터(Before Image)를 디스크에 다시 기록함. 연쇄 복귀 시 의존성 그래프(Dependency Graph)를 역추적하여 대상을 선정함. | ARIES, WAL(Write-Ahead Logging) |
| **Lock Table** | 락 관리 테이블 | 어떤 트랜잭션이 어떤 데이터 항목에 대한 **X-Lock (Exclusive Lock)**을 보유하고 있는지 추적. 연쇄 복귀 방지를 위해 커밋 전까지 락 해제를 지연시키는 정책 유지. | 2PL (Two-Phase Locking) |
| **Transaction T_i** | 문제 트랜잭션 | 원인 제공자. Abort 시 자신의 변경사항을 되돌림과 동시에, 자신의 데이터를 읽어간 T_j의 상태를 '취소 필요'로 마킹함. | Rollback Protocol |
| **Transaction T_j** | 피해 트랜잭션 | T_i의 Dirty Data를 Read함. T_i가 Rollback하면 자신의 결과가 무의미해지므로 강제로 Abort됨. | Victim Transaction |
| **Log Buffer** | 로그 버퍼 | 메모리 상에서 트랜잭션 간의 읽기/쓰기 순서를 기록. 연쇄 복귀 발생 시 어디까지 되돌려야 할지 판단하는 **LSN (Log Sequence Number)** 기준이 됨. | Buffer Management |

#### 2. 연쇄 복귀 발생 데이터 흐름 (ASCII Diagram)
아래는 비엄격한 스케줄(NON-Strict Schedule) 하에서 연쇄 복귀가 발생하는 구체적인 시나리오입니다. `T1`의 실패가 어떻게 `T2`의 취소를 강제하는지 시각화합니다.

```text
[연쇄 복귀 (Cascading Rollback) 실행 시나리오]

     Time │  Transaction 1 (T1)            │  Transaction 2 (T2)
   ────────┼───────────────────────────────┼───────────────────────────────
      t1   │  [LOCK-X] on Item A           │
      t2   │  WRITE(A: 50 -> 100)          │
            │  (Uncommitted Data in Buffer) │
      t3   │                               │  [LOCK-S] on Item A
      t4   │                               │  READ(A) --> Gets '100' (Dirty)
      t5   │                               │  [Processing based on 100...]
      t6   │  💥 SYSTEM FAILURE / ABORT    │
      t7   │  [UNDO] A: 100 -> 50          │  🔥 DETECTED! (Read Dirty Data)
      t8   │  (T1 Terminated)              │  [UNDO] T2 Operations Forced!
   ────────┴───────────────────────────────┴───────────────────────────────
   Legend: [LOCK-X] = Exclusive Lock, [LOCK-S] = Shared Lock
   Result: T2의 작업은 논리적으로 완료되었었으나, T1의 실패로 인해 모두 수포로 돌아감.
```

#### 3. 심층 동작 원리 및 의사결정 트리
연쇄 복귀는 **Transaction Dependency Graph**의 형성과 밀접한 관련이 있습니다.

1.  **의존성 형성 (Dependency Creation)**: T2가 T1의 데이터를 읽는 순간 `T2 -> T1`의 의존 관계가 형성됩니다. 이를 `T2`가 `T1`에 의존한다(Dependent)고 합니다.
2.  **실패 전파 (Failure Propagation)**: T1이 `ABORT`되면, 회복 관리자(RM)는 의존성 그래프를 검사하여 T1에 의존하는 모든 트랜잭션(T2, T3...)을 찾아냅니다.
3.  **재귀적 취소 (Recursive Abort)**: 찾아낸 트랜잭션들을 순차적으로(또는 동시에) `ABORT` 명령을 내리며, 이 과정에서 다시 그들이 의존하던 다른 트랜잭션들을 찾아 전이(Transitive Closure)합니다.
4.  **로그 기반 복구 (Log-based Recovery)**:
    *   **Undo List`: Rollback해야 할 트랜잭션 목록.
    *   `Redo List`: 재실행해야 할 트랜잭션 목록.
    *   T1이 실패하면 Undo List에 `T1` 추가. 이후 `T2`를 추가하고, T2의 로그를 역추적하여 변경 사항을 취소합니다.

#### 4. 핵심 알고리즘 및 제어 로직
연쇄 복귀를 관리하는 로직은 주로 트랜잭션 종료 처리부(Completion Handler)에 위치합니다.

```python
# Pseudo-code: Simplified Cascading Rollback Handler
def handle_transaction_abort(failed_tid):
    """
    failed_tid: 실패한 트랜잭션 ID
    """
    undo_list.add(failed_tid)
    
    # 연쇄적 의존성 처리 (DFS or BFS)
    dependents = find_dependent_transactions(failed_tid)
    
    for victim_tid in dependents:
        if victim_tid.status == 'COMMITTED':
            # 이미 커밋된 경우라면 회복 불가능한 상태(Irrecoverable)이거나
            # 로그 보정(Compensation)이 필요함 (이 PE 가이드에서는 편의상 Rollback 가정)
            pass 
        elif victim_tid.status == 'ACTIVE':
            # 강제 종료 처리
            force_rollback(victim_tid)
            undo_list.add(victim_tid)
            
            # 재귀적으로 피해 트랜잭션이 또 다른 트랜잭션에 의존하는지 확인
            handle_transaction_abort(victim_tid) 

    # 실제 디스크 복구 수행 (UNDO Phase)
    perform_undo(undo_list)
```

#### 📢 섹션 요약 비유
연쇄 복귀 메커니즘은 **"도미노 게임에서 앞쪽 도미노를 손으로 쓰러뜨리는 것"**과 같습니다. 하나를 쓰러뜨리면(T1 Abort), 뒤에 서 있는 모든 도미노(T2, T3...)는 제 몫을 다하고 서 있었음에도 불구하고 연결 고리에 의해 어쩔 수 없이 넘어지게 됩니다. 이를 막으려면 도미노 간격을 넓혀서(Strong Isolation) 서로 영향을 주지 않게 해야 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 스케줄링 전략 심층 비교
연쇄 복귀 문제를 해결하기 위해 데이터베이스는 다양한 스케줄링 전략을 제공합니다. 각 전략은 **복구 가능성(Recoverability)**과 **성능(Concurrency)** 사이의 트레이드오프(Trade-off)를 관리합니다.

| 비교 항목 | 비연쇄적 스케줄 (Cascadeless) | 엄격한 스케줄 (Strict) | 회복 가능 스케줄 (Recoverable) |
| :--- | :--- | :--- | :--- |
| **핵심 원리** | 트랜잭션은 커밋된 데이터만 읽을 수 있음. | 트랜잭션은 커밋된 데이터만 읽을 수 있음 + **쓰기 락 유지**. | 트랜잭션은 커밋된 데이터만 읽을 수 있음 + **의존하는 트랜잭션 먼저 커밋** 강제. |
| **연쇄 복귀 허용** | ❌ 불가 (차단) | ❌ 불가 (차단) | ⚠️ 조건부 허용 (의존성 순서 준수 시) |
| **동시성 정도** | 중상 (Locking 시간 증가) | **최하** (가장 보수적, Lock 유지 시간 최장) | 상 (Relaxed Locking) |
| **성능 비용** | Commit까지 대기 시간 소요 발생. | 병행 처리 성능 저하 가장 큼. | 관리 오버헤드 존재하나 유연함. |
| **실무 적용도** | 일반적인 트랜잭션 DBMS의 기준. | 금융권 등 강력한 무결성이 요구될 때 사용. | 고성능이 필요한 NoSQL 등에서 부분적 활용. |

#### 2. 과목 융합 관점: OS와 네트워크의 시선
연쇄 복귀는 데이터베이스 영역에 국한되지 않고 분산 시스템 전반의 문제입니다.

*   **OS (Operating System) - Deadlock과의 관계**:
    연쇄 복귀는 **Deadlock (교착 상태)** 해결 전략 중 하나인 'Victim Selection'과 맥락을 같이합니다. OS에서 데드락이 발생했을 때, 하나의 프로세스를 강제로 종료(Kill)시키면, 그 프로세스가 점유하던 자원을 기다리던 다른 프로세스들도 함께 영향을 받거나 재시작해야 할 수 있습니다. 차이점이라면 DB는 '데이터의 정합성'을 위해 명시적으로 Rollback하지만, OS는 '자원의 회수'에 집중한다는 점입니다.

*   **Network (Distributed Systems) - 2PC (Two-Phase Commit)**:
    분산 데이터베이스 환경에서 연쇄 복귀는 더욱 치명적입니다. **2PC (2-Phase Commit Protocol)** 프로토콜의 **Phase 1(Prepare)** 단계에서 참가자(Participant)들이 'Yes'를 응답했으나 코디네이터가 'Abort'를 결정하면, 모든 참여자가 자신의 변경사항을 롤백해야 합니다. 이 과정에서 네트워크 지연이 발생하면, 전체 분산 트랜잭션이 롤백 처리 중에 시스템 전체가 멈춘 듯한 **Global Blocking** 상태에 빠질 수 있습니다.

#### 📢 섹션 요약 비유
연쇄 복귀 방지 전략을 비교하자면, **"고속도로 차선 변경"**과 같습니다.
- **Cascadeless/Strict**: "절대 차선을 바꾸지 말고, 앞차가 완전히 통과한 뒤에 출발해라" (안전하지만 느림).
- **Recoverable**: "막 봐도 되지만, 앞차가 사고나면 너도 같이 꼬여서 뒤로