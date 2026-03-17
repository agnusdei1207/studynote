+++
title = "209. 직렬 스케줄 (Serial Schedule) - 완벽한 고립의 기준"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 209
+++

# 209. 직렬 스케줄 (Serial Schedule) - 완벽한 고립의 기준

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 직렬 스케줄은 다중 트랜잭션 환경에서 **트랜잭션 간의 연산(Instruction) 교차(Interleaving)를 철저히 차단**하고, 한 트랜잭션이 완전히 종료(Commit or Abort)된 후 다음 트랜잭션을 시작하는 순차적 실행 기법이다.
> 2. **가치**: 동시성 제어(Concurrency Control) 기법의 정당성을 판단하는 이론적 기준(Baseline)이 되며, 데이터베이스의 일관성(Consistency)을 100% 보장하는 '참(True)' 값으로 기능한다.
> 3. **융합**: OS의 프로세스 스케줄링(Non-preemptive)과 분산 시스템의 순차 합의(Sequential Consistency) 모델의 근간이 되며, 고립성이 절대적인 금융 결제 시스템 등에서 최후의 안전장치로 논의된다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**1. 개념 및 정의**
직렬 스케줄(Serial Schedule)이란 DBMS (Database Management System)에서 여러 트랜잭션이 존재할 때, 이들의 연산 순서를 섞지 않고 하나의 트랜잭션을 원자 단위로 묶어 순차적으로 실행하는 스케줄링 방식을 의미합니다. 수학적으로는 트랜잭션 집합 $\{T_1, T_2, \dots, T_n\}$에 대해 $T_i$의 모든 연산이 $T_j$의 모든 연산보다 앞서는($T_i < T_j$) 전순서(Total Order) 관계를 가집니다.

**2. 등장 배경 및 패러다임**
초기 데이터베이스 시스템은 자원의 한계와 복잡성 문제로 단순한 순차 처리를 수행했습니다. 그러나 데이터 양이 폭증함에 따라 **대기 시간(Latency)과 처리량(Throughput)의 trade-off** 문제가 대두되었습니다. 직렬 스케줄은 '정합성'이라는 절대 가치를 지키지만, 디스크 I/O나 Lock 대기 시간 동안 CPU가 놀게 되는 '유휴 자원(Idle Resource)' 문제를 안고 있습니다.

**3. 💡 비유: 좁은 돌다리**
한 번에 한 사람만 건널 수 있는 좁은 돌다리를 아무런 질서 없이 동시에 건너려 하면 낙상할 수 있습니다(충돌/오류). 직렬 스케줄은 줄을 서서 한 사람이 완전히 건너간 후 다음 사람이 건너도록 하는 것과 같습니다. 안전하지만, 줄이 길어질수록 뒤쪽 사람의 이동 속도는 극도로 느려집니다.

**4. 📢 섹션 요약 비유**
직렬 스케줄은 **'혼잡한 식당에서 주방장이 한 주문을 완성하고 서빙한 뒤, 다음 주문을 받기 시작하는 전통적인 방식'**과 같습니다. 주문이 섞여서 엉망이 되는 일(Non-Serializable)은 없지만, 손님의 대기 시간이 기하급수적으로 늘어나는 단점이 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**1. 구성 요소 및 동원 메커니즘**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/상태 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Transaction Manager** | 트랜잭션 생명주기 관리 | $T_1$이 Active 상태일 때, $T_2$의 시작 요청을 Block 시킴 | Begin/Commit | 교통 정경悟(경찰) |
| **Scheduler (Serial Enforcer)** | 연산 순서 배치 | $T_1$의 Read(A)/Write(B) 연산 큐를 $T_2$와 섞지 않음 | FIFO (Queue) | 표 발매소 |
| **Resource (Data Item)** | 접근 대상 객체 | Lock 모드가无关(무관), 시간적 배타성에 의해 보호됨 | X-Lock (Implicit) | 단일 화장실 칸 |
| **Log Manager** | 회복 관리 | Serial 실행 순서대로 REDO/UNDO 로그 기록 (순서 보장) | WAL (Write-Ahead Logging) | 블랙박스 |
| **CPU/Disk** | 실행 하드웨어 | Context Switching 비용은 거의 없으나 Busy Waiting 발생 | I/O Bound | 대기실 |

**2. ASCII 구조 다이어그램: 시간적 배타성 구조**

아래는 직렬 스케줄이 시간 축(Time Axis)을 어떻게 독점하는지 시각화한 도면입니다. $T_1$과 $T_2$의 수행 구간이 겹치는 지점(Overlap)이 전혀 없음을 확인할 수 있습니다.

```text
[직렬 스케줄 (Serial Schedule) 아키텍처 다이어그램]

   Time Axis ────────────────────────────────────────────────────────>
      
   [ Phase 1: T1 Execution Zone (Exclusive Lock) ]
   ┌──────────────────────────────────────────────────────────────────┐
   │  T1: Read(A) --> Process --> Write(B) --> Commit                  │
   │                                                                  │
   │  🔒 System Status: T2 is BLOCKED (Queued)                         │
   └──────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   [ Phase 2: Context Switch / Checkpoint ]
          (T1 종료 확인 및 T2 시작 준비)
                                        │
                                        ▼
   [ Phase 3: T2 Execution Zone (Exclusive Lock) ]
   ┌──────────────────────────────────────────────────────────────────┐
   │                           T2: Read(X) --> Write(Y) --> Commit    │
   │                                                                  │
   │  🔒 System Status: T3 (if exists) is BLOCKED                      │
   └──────────────────────────────────────────────────────────────────┘

   Legend:
   - No Interleaving: T1의 작업 영역과 T2의 작업 영역이 시간적으로 분리됨.
   - High Latency: T2는 T1이 끝날 때까지 기다려야 함 (Blocking Point).
```

**3. 다이어그램 심층 해설**
위 다이어그램에서 가장 중요한 점은 **'경계선(Boundary)'**입니다. 일반적인 병행 처리(Interleaved Schedule)에서는 T1이 I/O를 대기하는 동안 CPU가 T2를 처리하여 자원을 효율화합니다. 하지만 직렬 스케줄은 `Time Axis` 전체를 트랜잭션 하나가 독점합니다.
- **메커니즘**: 스케줄러는 $T_1$이 `Commit` 명령을 보내기 전까지 $T_2$의 첫 번째 명령(보통 `Read`)을 실행 계획에 넣지 않습니다.
- **성능 저하 요인**: 만약 $T_1$이 디스크에서 데이터를 읽어올 때 100ms가 소요된다면, CPU는 100ms 동안 아무것도 하지 않고 놀게 됩니다(Idle).
- **무결성 보장**: $T_1$이 $A=100$을 읽고 $A=50$으로 만드는 도중에 $T_2$가 끼어들 여지가 없으므로, Dirty Read나 Unrepeatable Read 같은 현상은 구조적으로 발생 불가능합니다.

**4. 핵심 알고리즘 및 수식**
직렬 스케줄의 판별은 단순합니다. 스케줄 $S$에 속한 모든 연산 쌍 $p, q$에 대해, $p \in T_i, q \in T_j$ ($i \neq j$)일 때, 다음 조건을 만족하면 직렬 스케줄입니다.

$$
\text{if } (p < q) \implies \text{all ops of } T_i < \text{all ops of } T_j
$$

**코드: 의사(Pseudo) 코드 레벨 직렬화**
```sql
-- 직렬 스케줄러의 논리 (개념적 표현)
FUNCTION SerialExecutor(Transactions T):
    FOR each transaction tx IN T:
        BEGIN TRANSACTION tx
        FOR each operation op IN tx:
            EXECUTE op  -- Block other transactions here
            IF op FAILS:
                ROLLBACK tx
                RETURN ERROR
        END FOR
        COMMIT tx  -- Release implicit lock
    END FOR
END FUNCTION
```

**5. 📢 섹션 요약 비유**
직렬 스케줄은 **'혼자서만 쓸 수 있는 전용 연구실을 사용하는 것'**과 같습니다. 내가 입실해서 퇴실할 때까지 문을 잠그고 열심히 실험(연산)을 하면 되므로 누가 방해하거나 실험 기구(데이터)를 망가뜨릴 걱정은 없지만, 다른 사람들은 문이 열릴 때까지 복도에서 기다려야 하는 비효율이 발생합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

**1. 심층 기술 비교표: Serial vs. Interleaved (Concurrency)**

| 비교 지표 (Metric) | 직렬 스케줄 (Serial Schedule) | 비직렬 스케줄 (Interleaved Schedule) |
|:---|:---|:---|
| **동시성 (Concurrency)** | None (0%) | High (Multi-programming) |
| **자원 활용도 (Utilization)** | Low (CPU/IO Idle Time 발생) | High (Overlap CPU & IO) |
| **데이터 무결성 (Integrity)** | 100% Guaranteed (No Concurrency) | Control Algorithm Required (Locking, etc.) |
| **처리량 (Throughput)** | Low (TPS 낮음) | High (TPS 높음) |
| **응답 시간 (Response Time)** | 매우 길음 (대기 시간 길음) | 짧음 (평균 대기 시간 감소) |
| **구현 복잡도 (Complexity)** | Low (단순 큐) | Very High (Deadlock detection needed) |
| **Serializability** | Always True | Conditionally True (Conflict Serializable) |

**2. 과목 융합 관점**
- **OS (Operating System)와의 관계**: OS의 **Non-Preemptive Scheduling (비선점형 스케줄링)**과 유사합니다. 프로세스가 자원을 사용하는 동안 인터럽트를 허용하지 않는 것처럼, 직렬 스케줄은 트랜잭션을 하나의 거대한 단위로 처리합니다.
- **Network와의 관계**: **Stop-and-Wait ARQ** 프로토콜과 유사합니다. 송신자가 하나의 패킷을 보내고 확인(ACK)을 받기 전까지 다음 패킷을 보내지 않는 순차적 방식은 네트워크 효율이 떨어지지만, 흐름 제어가 가장 확실합니다. 직렬 스케줄도 이와 같이 'Stop-and-Wait' 방식의 트랜잭션 처리라고 볼 수 있습니다.

**3. 📢 섹션 요약 비유**
직렬 스케줄과 비직렬 스케줄의 차이는 **'단선 철도(사용 불가 시 정지)'와 '복선 철도(교행 가능)'의 차이'**와 같습니다. 단선 철도(직렬)는 열차가 충돌할 위험이 없어 안전하지만, 대향 열차가 지나가려면 한쪽이 대피선에 들어가 기다려야 하므로 전체 운송 효율이 떨어집니다. 복선 철도(비직렬)는 양방향으로 달릴 수 있어 효율적이나, 신호 체계(동시성 제어)가 고장 나면 대형 사고가 발생합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**1. 실무 시나리오 및 의사결정**
실무에서 일반적인 OLTP(Online Transaction Processing) 환경에서 순수 직렬 스케줄을 사용하는 것은 자살 행위입니다. 그러나 특수한 상황에서는 전략적으로 선택되거나 시뮬레이션되어야 합니다.

*   **시나리오 A: 배치(Batch) 처리**
    *   **상황**: 매일 자정에 실행되는 일일 정산 배치 작업. 사용자의 실시간 조회가 없고, 데이터 양은 방대하며 무결성이 최우선입니다.
    *   **의사결정**: 마스터 테이블의 무결성을 위해 테이블 락(Table Lock)을 걸고 배치 작업을 직렬로 실행합니다.
    *   **이유**: 병행 처리로 인한 Lock Contention(경합)을 제거하여 배치 시간을 예측 가능하게 만들고, Deadlock 발생 확률을 0으로 만듭니다.

*   **시나리오 B: 디버깅 및 성능 벤치마크**
    *   **상황**: 특정 쿼리가 데이터 오류를 일으키는 원인을 파악할 때.
    *   **의사결정**: DBMS 설정을 변경하여 격리 수준(Isolation Level)을 `SERIALIZABLE`로 낮추거나, 단일 스레드 모드로 실행하여 재현 가능성을 높입니다.
    *   **이유**: 동시성 이슈(경쟁 조건)를 배제하고 로직 자체의 버그 여부를 판단하기 위함입니다.

*   **시나리오 C: 임계 영역(Critical Section) 보호**
    *   **상황**: 은행 계좌 이체 내역 집계 시스템.
    *   **의사결정**: 집계 함수가 실행되는 동안 해당 테이블의 쓰기 작업을 직렬화(Serializing)하여 집계 결과물이 '스냅샷'처럼 정확하도록 유지합니다.

**2. 도입 체크리스트**

| 구분 | 체크항목 | 설명 |
|:---|:---|:---|
| **기술적** | TPS (Transactions Per Sec) | 예상 TPS가 10 미만인가? (낮을 때만 고려) |
| | Lock Time | 트랜잭션 평균 수행 시간이 1초 미만인가? |
| **운영/보안적** | Data Integrity | 데이터 정합성이 0.001% 오류도 허용되지 않는가? |
| | User Experience | 사용자가 대기 시간을 견딜 수 있는가? (예: 배치) |

**3. 안티패턴 (Anti-Pattern)**
*   **Well-formed but Wrong**: 단순히 트랜잭션을 `SELECT` 후 `UPDATE` 하는 순서대로 코드를 짠다고 직렬성이 보장되지 않습니다. 코드 상의 순서가 아니라 **실제 실행 시점(Runtime Order)**에 의해 결정됩니다.
*   **Lock Conversion Hell**: