+++
title = "218. 2PL 축소 단계 (Shrinking Phase) - 권한의 반납"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 218
+++

# 218. 2PL 축소 단계 (Shrinking Phase) - 권한의 반납

### # 2PL (Two-Phase Locking)의 축소 단계

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션이 자원에 대한 독점 권한(Lock)을 해제(Unlock)하여 시스템으로 반환하는 2PL (Two-Phase Locking)의 후반부 단계이며, **락 포인트(Lock Point)** 이후부터 트랜잭션 종료 시점까지의 구간을 의미합니다.
> 2. **가치**: 불필요한 자원 점유를 해제하여 동시성 제어(Concurrency Control)의 병목을 완화하고 **처리량(Throughput)**을 증대시키는 핵심 메커니즘입니다.
> 3. **융합**: 하지만 잘못된 시점에 락을 해제할 경우 **연쇄 복귀(Cascading Rollback)**라는 데이터 무결성 위협을 초래할 수 있어, 실무 DBMS(Database Management System) 설계 시 Strict 2PL 등의 안전장치와 결합하여 전략적으로 판단해야 합니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
2PL (Two-Phase Locking) 프로토콜의 Lifecycle은 크게 **성장 단계(Growing Phase)**와 **축소 단계(Shrinking Phase)**로 나뉩니다. 축소 단계는 트랜잭션이 획득했던 Lock을 해제(Unlock)하기 시작하여 트랜잭션이 종료(Commit 또는 Abort)될 때까지의 기간을 정의합니다. 이 시점을 기점으로 해당 트랜잭션은 더 이상 데이터베이스 내의 어떤 항목에 대해서도 새로운 Lock을 요청할 수 없는 상태가 되며, 수행했던 작업의 결과를 확정 짓는 과정(Cleanup)을 거칩니다.

**2. 💡 비유**
이는 마치 고속도로를 달리던 차량이 목적지에 다달아 **진입로에서 내려와 요금소를 통과한 뒤, 차량을 주차하고 시동을 끄는 과정**과 같습니다. 한번 주차장(축소 단계)에 들어가면 다시 고속도로(성장 단계)로 진입할 수 없습니다.

**3. 등장 배경 및 필연성**
- **① 기존 한계 (Lock Retention)**: 트랜잭션이 데이터를 수정한 후에도 Lock을 계속 유지하면, 해당 데이터를 읽고자 하는 다른 트랜잭션들이 무한정 대기해야 하므로 시스템 전체의 병렬 처리 능력이 저하됩니다.
- **② 혁신적 패러다임 (Early Release)**: 작업이 완료된 항목에 대해서는 즉시 Lock을 해제하여 자원을 재활용하자는 아이디어가 등장했습니다. 이는 데이터베이스의 **다중 프로그래밍 정도(Multiprogramming Level)**를 높이는 기반이 되었습니다.
- **③ 현재의 비즈니스 요구 (High Concurrency)**: 수만 건의 TPS (Transactions Per Second)를 처리하는 현대의 OLTP (Online Transaction Processing) 환경에서는 밀리초 단위의 자원 회전율이 곧 비용과 성능으로 직결되므로, 효율적인 축소 단계 설계가 필수적입니다.

> **📢 섹션 요약 비유**: 축소 단계는 **"공연이 끝난 뒤 무대에서 내려와 의상을 탈의실에 걸어두고 귀가하는 과정"**과 같습니다. 한번 무대 밖으로 나오면 다시 무대 위(성장 단계)로 올라갈 수 없으며, 의상(Lock)을 정리해야 다른 출연자들이 다음 공연을 준비할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 동작**

| 구성 요소 | 역할 | 내부 동작 및 프로토콜 | 비고 |
|:---|:---|:---|:---|
| **Unlock 연산** | 자원 반납 | `Lock Manager(LM)`에게 Lock 해제 요청 전송. `Lock Table(LT)`에서 해당 엔트리 제거 또는 카운트 감소. | Shared(S) Lock과 Exclusive(X) Lock 모두 해제 가능. |
| **Lock Point** | 경계선 설정 | 트랜잭션 내에서 **최초의 Unlock**이 수행되는 시점. 이 시점이 2PL의 성장/축소를 가리는 결정적 찰나임. | 일단 지나가면 되돌릴 수 없는 '단방향 다리'. |
| **Hold 현상** | 기존 권한 유지 | 풀지 않은 Lock에 대해서는 여전히 점유권을 가지며, 다른 트랜잭션의 침범을 방지함. | 데이터 무결성의 최소한의 보호막. |
| **No New Lock** | 신규 요청 차단 | 축소 단계 진입 후 `Lock-S(item)` 또는 `Lock-X(item)` 요청 시 즉시 Abort 처리. | 2PL 정합성 유지의 핵심 규칙. |
| **Terminator** | 트랜잭션 종료 | 모든 Lock 해제 후 `Commit` 또는 `Rollback` 명령을 수행하여 트랜잭션을 원자적으로 종료시킴. | 이후에는 Redo/Undo 로그만 남음. |

**2. ASCII 구조 다이어그램: 트랜잭션 생명주기에서의 축소 단계**

아래 다이어그램은 트랜잭션의 시간축(Time Axis)에 따른 Lock 상태 변화와 제약 조건을 도시한 것입니다.

```text
  [Transaction Timeline: T1]
       
       Time  ------------------------>
       
  +---------------------------+
  |   Growing Phase (성장)    |      Shrinking Phase (축소)      |
  |   (Lock Acquisition)      |      (Lock Release)              |
  +---------------------------+-----------------------------------+
       |                            ▲
       |                            |
       ▼                            |
   Lock-S(A)                     Unlock(A)  <---- (Lock Point 발생)
   Lock-X(B)                     Unlock(B)
       |                         (Commit)
       |                            |
       |                            |
       +----------------------------+--------------------------> t

   [Rules Applied in Each Phase]
   ① Growing Phase: Lock-S, Lock-X O / Unlock X  (자원 획득만 가능)
   ② Shrinking Phase: Lock-S, Lock-X X / Unlock O (자원 반납만 가능)
```

*(해설: 위 다이어그램은 `Lock Point`를 기준으로 트랜잭션의 성격이 확 바뀐다는 점을 시각화했습니다. 2PL의 핵심은 이 '단방향성'입니다. 축소 단계로 넘어가면 더 이상 데이터에 손대지 못하고, 가지고 있는 것만 내려놓는 방어적인 태도를 취합니다.)*

**3. 심층 동작 메커니즘 (Algorithm Level)**

축소 단계의 동작은 DBMS의 Lock Manager (LM)에 의해 제어되며, 대략적인 의사코드(Pseudo-code)는 다음과 같습니다.

```sql
-- Pseudo-code for Lock Manager Shrinking Phase Logic

FUNCTION Handle_Unlock(Transaction T, DataItem D):
    // 1. Check Phase Constraints
    IF (T.state == SHRINKING) AND (T.pending_locks IS NOT NULL) THEN
        // 축소 단계에서 신규 락이 필요한 상황이 감지되면 에러
        RAISE ERROR "New Lock Request in Shrinking Phase";
    END IF

    // 2. Release Lock
    LOCK_TABLE[D].release(T)
    T.state = SHRINKING  // 최초 unlock 시 상태 전이
    
    // 3. Grant waiting locks (Wake-up)
    IF (LOCK_TABLE[D].waiting_queue IS NOT EMPTY) THEN
        NEXT_T = LOCK_TABLE[D].waiting_queue.dequeue()
        GRANT_LOCK_TO(NEXT_T, D)
    END IF
END FUNCTION
```

이 로직에 따르면, 축소 단계는 단순히 내 문을 닫는 것이 아니라, **내가 닫은 문 밖에서 대기하던 다른 트랜잭션(Waiting Queue)에게 '출발 신호'를 울려주는 중요한 시점**이기도 합니다.

> **📢 섹션 요약 비유**: 축소 단계의 잠금 해제 메커니즘은 **"영화관 좌석의 점유권을 포기하고 표를 반환하며 퇴장하는 과정"**과 같습니다. 내가 퇴장(Unlock)하는 순간, 입구에서 기다르던 다음 관객(Waiting Transaction)이 비로소 그 자리에 앉을 수 있습니다. 하지만 퇴장하는 도중에 다시 "아까 영화 안 보던 부분 다시 보고 갈게!" 하고 돌아앉을 수는 없는 원칙이 적용됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. Basic 2PL vs. Strict 2PL vs. Conservative 2PL**

축소 단계를 언제, 어떻게 수행하느냐에 따라 병행 제어의 안전성과 성능이 크게 달라집니다.

| 구분 | 성장 단계 | 축소 단계 (Shrinking Phase) | 장점 | 단점 |
|:---|:---|:---|:---|:---|
| **Basic 2PL** | 필요시 Lock 획득 | 트랜잭션 중간에라도 Lock을 해제 가능 | **높은 병렬성 (Concurrency)**<br>자원을 빨리 반환함 | **치명적 위험: 연쇄 복귀(Cascading Rollback)** 발생 가능. |
| **Strict 2PL** | 필요시 Lock 획득 | **트랜잭션 종료(Commit) 시까지 모든 Lock 유지** | **무결성 보장**<br>Cascading Rollback 방지 (실무 표준) | Lock 보유 시간이 길어 **병렬성 저하** 및 Deadlock 빈도 증가. |
| **Conservative 2PL** | 시작 시 **모든** Lock 획득 (미리 선점) | 트랜잭션 종료 시 일괄 해제 | Deadlock 불가능 (Precondition) | 미래 예측이 어려워 구현 어려움. 자원 낭비 심함. |

**2. 연쇄 복귀 (Cascading Rollback) 심층 분석**

Basic 2PL 방식에서 축소 단계를 너무 일찍 시작하면 발생하는 전형적인 문제 상황입니다.

```text
[Timeline: Cascading Rollback Scenario]

T1 (Update A ──────)
                    │
                    ▼
T2 (Read A ──────── Write B)
                    │
                    ▼
T3 (Read B ──────── Commit)

Time ---->
        [T1 Abort 발생!]
        
1. T1이 Rollback 되려면 A를 원래대로 돌려야 함.
2. 하지만 T2가 A를 읽어서 B를 썼음 (Dirty Read 발생 상태).
3. 따라서 T2도 강제로 Rollback 되어야 함.
4. T2가 Rollback 되면 T3도 B를 읽었으므로 Rollback 되어야 함.
   
=> 🚨 지진의 여진처럼 트랜잭션이 연쇄적으로 취소됨.
```

이러한 현상을 방지하기 위해, 축소 단계의 설계는 **"언제 풀 것인가(When to release)"**의 딜레마에 직결됩니다. OS(Operating System)의 스케줄링이나 컴퓨터 구조의 캐싱 정策(Caching Policy)과도 연결되는 개념으로, **"Write-back(지연 쓰기)을 하느냐 Write-through(즉시 쓰기)를 하느냐"**와도 맥락을 같이합니다.

> **📢 섹션 요약 비유**: 축소 단계의 시점 선택은 **"요리사가 설거지를 언제 하느냐"**와 같습니다. Basic 2PL은 요리 도중마다 칼을 씻어서 다른 요리사가 바로 사용할 수 있게 하지만(빠름), 내가 요리하던 음식에 실수가 있으면 칼을 썼던 다른 요리사의 음식까지 버려야 할 위험이 있습니다(연쇄 복귀). Strict 2PL은 모든 요리가 끝나고 손님을 보낸 뒤에야 한꺼번에 설거지를 시작하므로 안전하지만, 주방이 엉망이 되는 동안 다른 요리사는 기다려야 합니다(성능 저하).

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

- **시나리오 A: 금융권 코어 뱅킹 시스템 (Safety Critical)**
    - **상황**: 계좌 이체 시스템에서 T1이 A계좌에서 출금하고 B계좌에 입금하는 중간임.
    - **결정**: **Strict 2PL 채택**. 축소 단계를 Commit 시점까지 미루어야 함.
    - **이유**: 돈이 사라지거나 꼬이는 데이터 오류는 절대 용납될 수 없음. 다른 트랜잭션이 중간 데이터를 읽어가는 Dirty Read를 막아야 함. 성능 저하는 Replication 등으로 보완.

- **시나리오 B: 빅데이터 분석용 웨어하우스 (Read-Heavy)**
    - **상황**: 하루에 한 번 수행되는 대용량 배치 작업이며, 분석 중간에 다른 세션이 데이터를 읽을 필요가 있음.
    - **결정**: MVCC (Multi-Version Concurrency Control)와 결합된 방식 혹은 Snapshot Read 활용.
    - **이유**: Lock 기반의 축소 단계 자체가 병목이 될 수 있음. Lock이 아닌 데이터의 버저닝을 통해 병렬성을 확보하는 전략이 유리함.

**2. 도입 체크리스트**

| 구분 | 체크항목 | 확인 포인트 |
|:---|:---|:---|
| **기술적** | Deadlock 발생 빈도 | 축소 단계가 늦어질수록 Lock 보유 시간이 길어져 Deadlock 확률이 증가함. Wait-for Graph 모니터링 필수. |
| **운영적** | 로그 공간 (Undo/Redo) | Strict 2PL을 쓰면 Undo 로그가 종료까지 유지되어야 하므로 메모리/디스크 사용량이 증가함. |
| **보안적** | 정보 유출 가능성 | 축소 단계에서 Lock을 푸는 순간, 공격자가 해당 데이터에 접근 가능해짐. 민감 정보 포함 여부 확인. |

**3. 안티패턴 (Anti-patterns)**

- **❌ Eager Release (성급 해제)**: 정합성을 고려하지 않고 무조건 빨리 Lock을 풀려고 시도하는 코드. 데이터 무결성 파괴의 주원인이 됨.
- **❌ Hybrid 2PL 오용**: 일부 테