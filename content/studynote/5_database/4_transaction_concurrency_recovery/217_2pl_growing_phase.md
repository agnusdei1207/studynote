+++
title = "217. 2PL 확장 단계 (Growing Phase) - 락 획득의 시간"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 217
+++

# 217. 2PL 확장 단계 (Growing Phase) - 락 획득의 시간
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2PL (Two-Phase Locking) 프로토콜의 첫 단계로, 트랜잭션이 데이터베이스 조작을 수행하기 위해 필요한 모든 Lock (자원 잠금)을 **획득(Acquisition)만 하고 절대 해제하지 않는 구간**이다.
> 2. **가치**: 트랜잭션의 직렬화 가능성(Serializability)을 보장하는 핵심 메커니즘이며, 이 단계에서의 정책이 DBMS (Database Management System) 전체의 동시성 처리량(Concurrency Throughput)과 교착 상태(Deadlock) 발생 빈도를 결정짓는다.
> 3. **융합**: OS의 뮤텍스(Mutex) 획득, 분산 시스템의 토큰 점유 등 다양한 동시성 제어 영역과 연결되며, 트랜잭션 스케줄링의 최적화 포인트이다.
+++

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 개념 및 정의
**2PL (Two-Phase Locking, 2단계 락킹)** 프로토콜은 트랜잭션의 직렬화 가능성을 보장하기 위해 제안된 가장 대표적인 동시성 제어 기법입니다. 그중 **확장 단계(Growing Phase, 성장 단계)**는 트랜잭션 실행의 초기 단계로, 트랜잭션이 **Read** 또는 **Write** 연산을 위해 필요한 데이터 항목에 대해 Lock을 요청(Request)하고 부여받는(Grant) 과정만 허용되는 구간을 의미합니다.

이 단계의 핵심 제약 조건은 **"락 해제(Unlock) 금지"**입니다. 한 번 획득한 Lock은 트랜잭션이 완료(Commit 또는 Abort)되거나 명시적인 축소 단계(Shrinking Phase) 진입 시점까지 절대 놓아서는 안 됩니다. 이를 통해 트랜잭션은 자신이 필요로 하는 모든 자원에 대한 독점적 혹은 공유적 권한을 완벽하게 확보하는 시간을 갖게 됩니다.

#### 💡 비유
이는 마치 **'비행기 출격前的 케이블 및 연료 장착'**과 같습니다. 비행기(트랜잭션)가 이륙(데이터 조작)하기 위해서는 무기, 연료, 통신 장비(Lock)를 하나하나 장착해야 합니다. 모든 장비가 장착되지 않은 상태에서 이륙하거나, 장착 중에 장비를 떼어버리면(Unlock) 임무 수행 중 추락(데이터 불일치)할 수 있기 때문입니다.

#### 등장 배경
1.  **기존 한계**: 초기의 단순한 Lock 기법에서는 트랜잭션이 실행 중 자원을 해제했다가 다시 요청할 수 있어, 실행 순서가 꼬여 "Non-Serializable(비직렬화 가능)"한 스케줄이 발생하여 데이터 무결성이 훼손되는 문제가 있었습니다.
2.  **혁신적 패러다임**: 트랜잭션의 생애 주기를 '락을 채워넣는 기간'과 '락을 풀어주는 기간'으로 엄격히 분리함으로써, 모든 트랜잭션 간의 충돌 관계를 **DAG (Directed Acyclic Graph, 방향성 비순환 그래프)** 형태로 만들어 무결성을 수학적으로 증명할 수 있게 되었습니다.
3.  **현재의 비즈니스 요구**: 대규모 분산 DB 환경에서 수천 TPS (Transaction Per Second)를 처리하기 위해, 이 확장 단계를 얼마나 빠르고 효율적으로 통과하느냐가 DBMS의 전체 성능을 좌우하는 핵심 병목 구간(Bottleneck)이 되었습니다.

#### 📢 섹션 요약 비유
확장 단계는 **"피겨 스케이팅 선수가 점프를 뛰기 전, 도움닫기를 하며 속도와 균형을 완벽하게 모으는 구간"**과 같습니다. 이 구간에서 모든 준비(Lock)가 갖춰지지 않으면, 화려한 회전(데이터 수정)은 시작조차 할 수 없으며 넘어질 위험이 있기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 1. 구성 요소 및 모듈 상세
확장 단계는 단순히 "Lock을 거는 것"이 아니라, DBMS의 동시성 제어 매니저가 개입하는 복잡한 메커니즘입니다.

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Lock Manager (LM)** | 락 상태 관리자 | 메모리상의 **Lock Table (Lock Table)**을 유지하며 트랜잭션의 `Lock-S`, `Lock-X` 요청을 큐(Queue)에 쌓음. | Wait-Die / Wound-Wait | 주차장 관리인 |
| **Lock Table (LT)** | 자원 상태 저장소 | 각 데이터 항목별로 현재 어떤 트랜잭션이 어떤 모드(S/X)로 점유 중인지, 누가 대기 중인지 저장하는 해시 테이블. | Hashing | 주차 요금표 및 현황판 |
| **Transaction (Tx)** | 자원 요청主体 | SQL 연산을 수행하며 데이터 접근 시 LM에게 `LockRequest()` 시스템 콜 호출. | 2PL Protocol | 주차하려는 차량 |
| **S-Lock (Shared)** | 읽기 공유 Lock | 다른 Tx의 S-Lock과 공유 가능하지만, X-Lock(쓰기)과는 배타적. | Read-Only | 카풀 승차권 |
| **X-Lock (Exclusive)** | 쓰기 배타 Lock | 가장 강력한 Lock. 어떠한 다른 Lock(S, X)과도 공유 불가. 무조건 대기 필요. | Read-Write | 전용 승용차 1인석 |

#### 2. ASCII 구조 다이어그램: 트랜잭션 상태 전이 (State Transition)

아래 다이어그램은 트랜잭션이 활성(Active) 상태에서 시작하여, 확장 단계를 거쳐 완료(Committed) 또는 중단(Aborted)되기까지의 상태 흐름을 도식화한 것입니다. 확장 단계는 `Active` 상태의 주된 부분을 차지하며, 자원 획득이 완료되는 시점이 중요합니다.

```text
 [2PL 트랜잭션 생애 주기 상태도]

       (Start)
        ↓
   +-----------------+
   |   ACTIVE        |  ← 트랜잭션 시작
   | (Executing)     |
   +-----------------+
        ↓
   +---------------------------------------+
   |    GROWING PHASE (확장 단계)           |
   |   [ 상세 동작 ]                        |
   |   1. Read(A)  → Lock-S(A) 요청        |
   |   2. Write(B) → Lock-X(B) 요청        |
   |   3. 충돌 발생 시 Wait Queue 진입     |
   |   4. 필요한 모든 Lock 획득             |
   +---------------------------------------+
        ↓
   [ ⚠️ LOCK POINT (락 포인트) ]
   "마지막 Lock 획득이 완료된 시점"
   ↓ (Lock 해제 조작이 일어나면)
   +---------------------------------------+
   |    SHRINKING PHASE (축소 단계)        |
   |   (Lock 해제 시작, 연산 수행 계속)     |
   +---------------------------------------+
        ↓
   +-----------------+        +-----------------+
   |   COMMITTED     |        |     ABORTED     |
   +-----------------+        +-----------------+
```

#### 3. 다이어그램 심층 해설
위 다이어그램에서 가장 중요한 지점은 **`LOCK POINT`**입니다.
- **확장 단계(Growing Phase)**: `ACTIVE` 상태의 트랜잭션이 첫 번째 `Unlock` 연산을 수행하기 직전까지의 구간입니다. 이 시점에서 트랜잭션은 독립적인 실행 단위로서 필요한 모든 권한을 완성해 나갑니다. 만약 `Lock-X(B)`를 획득해야 하는데 다른 트랜잭션이 이미 `Lock-S(B)`를 가지고 있다면, 현재 트랜잭션은 **Lock Wait(대기 상태)**로 전환되어 블로킹(Blocking)됩니다.
- **Lock Point의 의미**: 트랜잭션이 확장 단계를 마치고 축소 단계로 넘어가는 경계선입니다. 2PL의 변종인 **Strict 2PL**에서는 이 시점을 트랜잭션 종료(Commit)까지 미루어, 복구(Cascading Rollback) 문제를 해결합니다. 즉, 확장 단계가 길어질수록 병렬성은 떨어지지만 데이터 안정성은 극대화됩니다.

#### 4. 핵심 알고리즘 및 의사 코드 (Pseudo-Code)

다음은 DBMS 내부에서 Lock Manager가 획득 요청을 처리하는 로직의 일반적 형태입니다.

```sql
-- Pseudo-code: Lock Acquisition Request
FUNCTION RequestLock(Transaction T, DataItem D, LockMode Mode):
    /*
    Mode: S (Shared) or X (Exclusive)
    Rule: Growing Phase - No Unlock allowed implicitly
    */

    -- 1. Is the lock already compatible?
    IF CheckCompatibility(LockTable[D], Mode) THEN
        -- Compatible: Grant Lock
        Grant(T, D, Mode)
        T.LockSet.add(D)  -- Add to transaction's inventory
        RETURN SUCCESS
    ELSE
        -- Conflict Detected
        -- 2. Deadlock Prevention Check (e.g., Wait-Die)
        IF T.timestamp > LockHolder[D].timestamp THEN
            -- Younger transaction waits
            WaitFor(T, D, Mode)
            RETURN WAIT
        ELSE
            -- Older transaction aborts the younger one (Wound-Wait)
            Abort(T)
            RETURN ABORT
        END IF
    END IF
END FUNCTION
```

#### 📢 섹션 요약 비유
확장 단계의 내부 작동은 **"하이패스 차로 진입하기 전 요금소에서 병목을 겪는 과정"**과 같습니다. 모든 차량(트랜잭션)은 진입(락 획득)을 위해 순서를 기다려야 하며, 진입 후에는 다른 차량이 간섭할 수 없는 고속도로(잠긴 데이터 영역)를 질주하게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 확장 단계 vs. 축소 단계 (Shrinking Phase) 비교
2PL을 구성하는 두 단계는 대조적인 목적과 패턴을 가집니다.

| 비교 항목 (Criteria) | 확장 단계 (Growing Phase) | 축소 단계 (Shrinking Phase) |
|:---|:---|:---|
| **핵심 동작 (Action)** | `Lock-S`, `Lock-X` (획득만 수행) | `Unlock` (해제만 수행) |
| **자원 변화 (Resource)** | 점유하는 자원의 수가 **증가**함 | 점유하는 자원의 수가 **감소**함 |
| **트랜잭션 상태** | 활동적이나 대기 가능성 높음 | 종료(Commit)로 가는 마지막 단계 |
| **병렬성 (Concurrency)** | 낮음 (서로 자원을 선점하며 경쟁) | 높음 (자원을 풀어주며 타 트랜잭션 허용) |
| **주요 이슈 (Issues)** | **Deadlock (교착 상태)** 발생 위험 | **Cascading Rollback (연쇄 복귀)** 위험 (Basic 2PL) |
| **OS/컴퓨터 구조 연계** | 메모리 할당(Malloc), Mutex Lock | 메모리 해제(Free), Mutex Unlock |

#### 2. 2PL 유형별 확장 단계 특성 비교
표준 2PL 외에도 안전성을 높이기 위해 확장 단계의 끝을 조정하는 변종들이 있습니다.

| 구분 (Type) | 확장 단계 종료 시점 (End of Growing) | 장점 (Pros) | 단점 (Cons) |
|:---|:---|:---|:---|
| **Basic 2PL** | 첫 번째 `Unlock` 직전까지 | 구현 간단, 병렬성 상대적 높음 | 연쇄 복귀(Cascading Rollback) 발생 가능 |
| **Strict 2PL** | **트랜잭션 Commit/Abort 시점**까지 | 복구 용이성 극대화 (연쇄 복귀 방지) | Lock 보유 시간 최대화 → **병렬성 급격 저하** |
| **Rigorous 2PL** | 모든 Lock이 종료 시까지 유지되는 Strict와 동일 | 가장 강력한 격리 수준 제공 | Throughput(처리량)이 가장 낮음 |

#### 3. 과목 융합 관점
- **OS (Operating System)**: 확장 단계의 `Lock` 요청은 커널 레벨의 **Mutex** 또는 **Semaphore** P 연산과 동일합니다. 여기서 교착 상태(Deadlock)가 발생하면 OS는 프로세스를 선점하거나 종료해야 하며, 이는 DBMS가 트랜잭션을 Abort 시키는 메커니즘과 같습니다.
- **네트워크 (Network)**: 분산 DB 환경에서 확장 단계는 네트워크 지연(Latency)과 직결됩니다. 원격 노드에 Lock을 요청할 때 ACK가 오지 않으면 대기 상태에 빠지며, 이는 네트워크 병목이 DB 처리량으로 이어지는 현상입니다.

#### 📢 섹션 요약 비유
2PL의 확장과 축소는 **"수도꼭지를 여는 과정"**과 **"다시 닫는 과정"**입니다. 확장 단계는 물을 받기 위해 여러 곳의 밸브를 확인하고 여는(잠금 획득) 과정이므로 실수가 나면 물이 샐 수 있어(Deadlock) 가장 신중해야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

#### 1. 실무 시나리오: 대기열 시스템의 티켓 잔고 처리 (Ticketing System)
이벤트 티켓 예매와 같이 경쟁이 치열한 시스템에서 **확장 단계**의 설계는 성공과 실패를 가릅니다.

- **문제 상황**: 사용자 A가 10초 동안 좌석 선택 화면에서 머물며 `Lock-X`를 유지하는 동안, 다