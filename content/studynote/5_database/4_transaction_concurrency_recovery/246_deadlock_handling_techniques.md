+++
title = "246. 데이터베이스 교착 상태 (Deadlock) 처리 기법"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 246
+++

# 246. 데이터베이스 교착 상태 (Deadlock) 처리 기법

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 교착 상태(Deadlock)는 두 개 이상의 트랜잭션(Transaction)이 상대방이 점유한 리소스(Resource)의 잠금(Lock)을 획득하기 위해 무한정 대기하며, 시스템 전체의 진행이 정지되는 순환 대기(Circular Wait) 상태를 의미한다.
> 2. **가치**: 대기 그래프(Wait-for Graph) 분석과 타임스탬프(Time-stamp) 기반 예방 기법 등을 통해 자원 경합의 병목을 능동적으로 해소하여, 데이터베이스 가용성(Availability)과 트랜잭션 처리량(TPS)을 극대화한다.
> 3. **융합**: 운영체제(OS)의 교착 상태 처리 이론을 데이터베이스 트랜잭션 무결성(Integrity) 보장을 위해 정교하게 이식한 사례이며, 분산 처리 환경에서는 2단계 커밋(2PC)과 결합하여 글로벌 데드락(Global Deadlock) 문제로 확장된다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**데드락(Deadlock)**은 다중 프로그래밍(Multi-programming) 환경에서 필연적으로 발생할 수 있는 동시성 제어(Concurrency Control)의 가장 근본적인 딜레마다. 데이터베이스 관리 시스템(DBMS)은 데이터의 무결성을 보장하기 위해 로킹(Locking) 기법을 사용하며, 이 과정에서 트랜잭션 간의 **상호 배제(Mutual Exclusion)**, **점유 대기(Hold and Wait)**, **비선점(No Preemption)**, **순환 대기(Circular Wait)**라는 4가지 조건이 동시에 충족될 때 시스템은 정지한다. 이를 해결하기 위해 예방(Prevention), 회피(Avoidance), 탐지 및 복구(Detection & Recovery)라는 세 가지宏观적인 접근 방식이 존재한다.

#### 2. 등장 배경 및 필요성
- **기존 한계**: 단순한 자원 할당 시 충돌 발생 시 일부 요청을 무조건 거부하거나 대기시키는 방식(Retry)은 트랜잭션 처리량(TPS) 급감과 응답 시간 지연(Latency)을 유발함.
- **혁신적 패러다임**: 운영체제의 세마포어(Semaphore) 및 모니터(Monitor) 개념을 넘어, 데이터베이스 특성에 맞는 *다중 그래뉼라(Multi-granularity)* locking과 타임아웃 기반 비선점형 기법 도입.
- **현재 요구**: 금융권 등 트랜잭션이 빈번하게 발생하는 환경에서는 *선점형 회귀(Rollback)* 비용을 최소화하면서 시스템 중단을 방지하는 지능적 기법이 필수적임.

#### 3. 대기 그래프(Wait-for Graph) 시각화

```text
      [ 트랜잭션 T1 ]         [ 트랜잭션 T2 ]
      (Lock: Row A)           (Lock: Row B)
           │                        │
           │ ▼ (Request B)          │ ▼ (Request A)
           └────────────┐    ┌─────────────
                        │    │
                    [ Deadlock State ]
```

**해설**:
위 다이어그램은 가장 단순한 형태의 교착 상태를 보여줍니다.
1. **T1**이 Row A를 점유한 상태에서 Row B를 요청하며 대기합니다.
2. **T2**가 Row B를 점유한 상태에서 Row A를 요청하며 대기합니다.
3. 두 트랜잭션 모두 상대방의 자원 해제를 기다리는 **순환 대기(Cycle)** 형태가 형성되어, 외부 개입(강제 종료)이 없으면 영원히 진행되지 않습니다.

> 📢 **섹션 요약 비유**: 교착 상태 관리는 **'비상사태 시의 교통 통제 제도'**와 같습니다. 사방이 막힌 교차로(Deadlock)를 해결하기 위해, 미리 진입을 통제하거나(예방), 진입 전 돌아갈 곳이 있는지 확인하며(회피), 막힌 후에는 구급차처럼 급한 차량을 먼저 통과시키기 위해 다른 차를 견인하는(회복) 방식으로 운영됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 교착 상태 처리 모듈 구성 (5가지 핵심 요소)

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Ops) | 프로토콜/특징 | 비유 |
|:---|:---|:---|:---|:---|
| **Lock Manager (LM)** | 자원 할당 및 상태 관리 | Lock Table을 조회하여 호환성 확인 및 대기열(Wait Queue) 관리 | 2PL(2-Phase Locking) 기반 | 주차 관리소 |
| **Wait-for Graph** | 의존 관계 모델링 | 트랜잭션의 점유 대기 관계를 Directed Graph로 표현 | 주기적 갱신 | 교통 흐름도 |
| **Deadlock Detector** | 사이클 탐지 | DFS(Depth First Search) 등을 이용해 그래프 내 순환 경로(Cycle) 존재 여부 확인 | 주기적 탐지 (Periodic) | 레이더 |
| **Victim Selector** | 희생자 선정 알고리즘 | 비용(Cost) 기반, 타임스탬프, 진행 정도 등을 고려하여 Rollback 대상 선정 | Rollback Minimization | 희생양 선정 |
| **Recovery Manager** | 원상 복구 | 선택된 트랜잭션을 Abort하고 수행했던 연산을 Undo 처리 | Write-ahead Log | 시간 여행 |

#### 2. 타임스탬프 기반 예방 기법 (Timestamp Ordering Methods)

이 기법은 트랜잭션 시작 시 시스템이 부여한 유일한 **타임스탬프(Timestamp)**를 기준으로 **늙은 트랜잭션(Old)**과 **젊은 트랜잭션(Young)** 간의 충돌을 해결한다.

```text
[A] Wait-Die Scheme (Non-preemptive)

   T_older (가진 자) ◀───┐
                         │ Data Item X Request
   T_younger (대기 중) ──┘
   [Rule]: T_younger는 기다리다(Wait) 실패하면 자살(Die).

        [트랜잭션 스케줄링 흐름]
        (TS(T1) < TS(T2) : T1이 T2보다 늙음)

   T1 ──▶ [Lock X] ──▶ (Processing)
                            ▲
                            │ Request X
   T2 ──▶ [Wait] ────────────┘
   (충돌 발생 시 T2가 늙지 않았으므로 Abort됨)

---------------------------------------------------------

[B] Wound-Wait Scheme (Preemptive)

   T_older (대기 중) ──┐
                      │ Data Item X Request
   T_younger (가진 자) ◀───┘
   [Rule]: T_younger는 상처 입고(Wound) 자원 반납. T_older는 기다림(Wait).

        [트랜잭션 스케줄링 흐름]

   T1 ──▶ [Request X] ──▶ (T2가 가지고 있음)
                            │
                            │ T1이 T2보다 늙음!
                            ▼
   T2 ──▶ [Abort] ──▶ [Rollback] (T1이 자원을 뺏음)
   T1 ──▶ [Lock X] ──▶ (Processing)
```

**해설**:
- **Wait-Die**: 오래된 트랜잭션은 기다림의 권리가 있고, 젊은 트랜잭션은 자원을 얻지 못하면 스스로 종료(Die)한다. 재시동 시에는 동일한 타임스탬프를 사용하여 기아 현상(Starvation)을 방지한다.
- **Wound-Wait**: 오래된 트랜잭션이 젊은 트랜잭션의 자원을 뺏는(Wound) 방식이다. 젊은 트랜잭션은 기다렸다가(Wait) 다시 시작한다.
- **차이점**: Wait-Die는 젊은 트랜잭션이 죽는 횟수가 많을 수 있지만, Wound-Wait는 오래된 트랜잭션이 롤백될 확률이 적어 *Rollback 비용*이 상대적으로 낮다.

#### 3. 핵심 알고리즘: 대기 그래프(Wait-for Graph) 탐지 코드

```python
# [Deadlock Detection Algorithm Pseudo-Code]
class Transaction:
    def __init__(self, tid, timestamp):
        self.tid = tid
        self.timestamp = timestamp

def detect_deadlock(wait_for_graph):
    """
    DFS(Depth First Search)를 이용하여 사이클을 탐지하는 함수
    wait_for_graph: { Tx: [Ty, Tz], ... } 형태의 인접 리스트
    """
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in wait_for_graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                # 순환 경로(Cycle) 발견 -> Deadlock!
                return True

        rec_stack.remove(node)
        return False

    # 모든 노드에 대해 DFS 수행
    for node in wait_for_graph:
        if node not in visited:
            if dfs(node):
                return True # Deadlock Detected
    return False
```

> 📢 **섹션 요약 비유**: 타임스탬프 기반 처리는 **'수양 대군의 서열 문화'**와 같습니다. 선배(늙은 트랜잭션)가 먼저 자리를 차지하고 있으면 후배(젊은 트랜잭션)가 양보하거나(Wait-Die), 선배가 필요하면 후배가 자리를 비켜주는(Wound-Wait) 방식으로, 서열에 따른 엄격한 규율로 시스템이 꼬이는 것을 방지합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기법별 심층 비교 분석표

| 구분 | 예방 (Prevention) | 회피 (Avoidance) | 탐지 및 복구 (Detection & Recovery) |
|:---|:---|:---|:---|
| **핵심 전략** | 4가지 필요 조건 중 하나를 부정 | *안전 상태(Safe State)*일 때만 자원 할당 | 주기적으로 탐지 후 *희생자(Victim)* 선정 |
| **대표 알고리즘** | Wait-Die, Wound-Wait | *은행원 알고리즘*(Banker's Algo) | Wait-for Graph Cycle Detection |
| **자원 이용률** | 낮음 (자원 낭비 유발) | 매우 낮음 (미래 예측으로 인한 보수적 할당) | **높음** (일단 실행하고 보기 때문) |
| **처리 오버헤드** | 낮음 (트랜잭션 시작 시점만 체크) | 매우 높음 (할당 때마다 계산 필요) | **중간** (탐지 주기에 따라 다름) |
| **실무 적용성** | 분산 DB에서 선호됨 | 거의 사용되지 않음 | **표준 DBMS의 주류 방식** |
| **장단점** | 구현 쉬우나 굶어 죽을 수 있음(Starvation) | 이론적이나 실제 효율이 나쁨 | 효율적이나 Rollback 비용 발생 |

#### 2. OS(운영체제)와의 융합 관점

```text
[OS Kernel vs DBMS Transaction Deadlock]

+-------------------+---------------------------+---------------------------+
| Feature           | OS Kernel (Resource)      | DBMS (Transaction)        |
+-------------------+---------------------------+---------------------------+
| Unit              | Process / Thread          | Transaction (Logical Unit)|
| Resource Type     | I/O Device, Memory, CPU   | Tuple, Page, Table (Data)|
| Preemption Cost   | Context Switch (Low)      | Rollback / REDO (Very High)|
| Granularity       | Coarse (Physical)         | Fine (Logical/Row Level)  |
| Typical Strategy  | Detection & Kill Process  | Detection & Rollback Tx   |
+-------------------+---------------------------+---------------------------+
```

**해설**:
- **OS**: 물리적 자원(I/O, 메모리)을 다루므로 문맥 교환(Context Switch) 비용이 상대적으로 적어 프로세스를 강제 종료(Kill)하는 것이 일반적이다.
- **DBMS**: 논리적 연산 단위인 트랜잭션을 다루며, 원자성(Atomicity)을 보장하기 위해 로그(Log)를 통한 롤백이 필요하므로 비용이 매우 크다. 따라서 DBMS는 **사전 예방(Prevention)**이나 **타임아웃(Timeout)** 설정이 OS보다 훨씬 중요한 파라미터로 작용한다.

> 📢 **섹션 요약 비유**: OS와 DBMS의 차이는 **'전구 교체'와 '하드 디스크 복구'의 차이**와 같습니다. OS는 전구가 나가면 새 것으로 갈아 끼우면 끝나지만(Preemption Easy), DBMS는 복잡한 데이터 정돈 상태를 원점으로 되돌려야 하므로(Rollback Expensive), 일이 틀어지지 않게 미리미리 신경을 써야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오별 의사결정 프로세스

**시나리오 A: 대기 그래프가 탐지되었을 때 (복구 전략)**
1. **진단**: `DBA_WAIT_GRAPH` 테이블을 분석하여 순환 경로(Cycle)를 식별.
2. **선정**: 희생자(Victim) 선정 로직 적성.
    - **규칙**: *진행 중인 작업량(Weight)*이 가장 적은 트랜잭션을 우선 선정 (최소한의 Rollback 비용).
    - **Lock Timeout**: 제한 시간(Timeout)을 초과한 트랜잭션 우선 제거.
3. **조치**: `ROLLBACK WORK;` 명령어로 희생자 트랜잭션을 종료하고 수행된 변경 사항을 Undo.
4. **재시도**: 희생자 트랜잭션을 자동으로 재시작(With 동일한 Timestamp 혹은 새로운 ID).

**시나리오 B: 금융권 초고속 트랜잭션 처리 시 (예방 전략)**
1. **상황**: 누락 불가능한 매매 체결 로직.
2. **접근**: 회복이 불가능하거나 치명적인 손실이 발생하므로 **Wait-Die** 기