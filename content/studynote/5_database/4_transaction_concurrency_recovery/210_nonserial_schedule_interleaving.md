+++
title = "210. 비직렬 스케줄 (Non-serial Schedule) - 병행 처리를 통한 성능 해방"
date = "2026-03-14"
[extra]
title = "210. 비직렬 스케줄 (Non-serial Schedule) - 병행 처리를 통한 성능 해방"
date = "2026-03-16"
categories = "studynote-database"
id = 210
+++

# 210. 비직렬 스케줄 (Non-serial Schedule) - 병행 처리를 통한 성능 해방

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션(Transaction)의 연산들을 시간축상에서 분리 및 교차 실행(Interleaving)하여, 단일 자원(CPU/Disk) 유휴 시간을 최소화하는 **병행 제어(Concurrency Control)의 기본 전제** 이다.
> 2. **가치**: I/O Burst와 CPU Burst를 중첩시켜 **처리량(Throughput)**을 비약적으로 향상시키며, **응답 시간(Response Time)**을 단축하여 다중 사용자 환경의 성능을 보장한다.
> 3. **융합**: OS의 스케줄링(Context Switching) 및 하드웨어의 인터럽트 메커니즘과 연결되며, **직렬 가능성(Serializability)** 이론을 통해 데이터 무결성과 성능의 균형을 맞춘다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

비직렬 스케줄이란 데이터베이스 관리 시스템(DBMS)에서 여러 트랜잭션을 동시에 실행하기 위해, 트랜잭션을 구성하는 개별 연산(Read, Write) 단위를 쪼개어 시간 순서대로 섞어서 실행하는 방식을 의미합니다. 전통적인 직렬 스케줄(Serial Schedule)이 트랜잭션 하나가 완전히 끝나야 다음 트랜잭션을 시작하는 순차적 방식인 반면, 비직렬 스케줄은 T1의 연산이 진행되는 도중에 T2의 연산을 삽입하는 인터리빙(Interleaving)을 허용합니다.

**💡 비유 및 등장 배경**
이 기술의 등장 배경에는 **'자원의 불균형적 활용'**이라는 근본적인 문제가 있습니다. 트랜잭션은 CPU 연산과 디스크 I/O가 반복되는 복합 작업입니다. 직렬 실행 시 T1이 디스크에서 데이터를 읽는 동안(I/O Wait) CPU는 놀게 됩니다. 이는 **'버스가 한 명의 승객을 태우고 이동하는 동안 다른 승객들은 정류장에서 기다려야 하는 상황'**과 같습니다. 이를 해결하기 위해 T1이 I/O를 대기하는 동안 T2에게 CPU를 넘겨주는 방식, 즉 **'고속도로 진입로에서 본선 차로로 합류하여 톨게이트 병목을 해소하는 것과 같은 논리'**로 비직렬 스케줄이 설계되었습니다.

**기술적 필요성**
대규모 온라인 트랜잭션 처리(OLTP) 환경에서는 초당 수천 건 이상의 요청이 발생합니다. 이를 직렬로 처리하기 위해서는 현저히 낮은 TPS(Transactions Per Second)로 인해 비즈니스 요구사항을 충족할 수 없습니다. 비직렬 스케줄은 이러한 병목을 해소하기 위한 필수적인 아키텍처 선택이며, 동시에 데이터 일관성을 유지하기 위해 **격리성(Isolation)** 수준을 조절하는 정교한 제어가 요구됩니다.

**📢 섹션 요약 비유**: 비직렬 스케줄링은 마치 **'주방에서 여러 셰프가 각자의 요리 순서를 기다리지 않고, 웍이 사용 가능할 때마다 번갈아 가며 볶음 요리를 하는 것'**과 같습니다. 한 명이 재료를 손질(CPU 작업)하는 동안 다른 한 명이 웍을 사용(I/O 작업)하여 주방 혼잡도를 줄이고 요리 완성 속도를 높이는 원리입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

비직렬 스케줄을 구현하기 위해서는 트랜잭션 관리자(Transaction Manager, TM)와 스케줄러(Scheduler)의 긴밀한 협조가 필요합니다. 스케줄러는 개별 연산(Read/Write)의 순서를 제어하여 시스템의 처리량을 극대화해야 합니다.

#### 1. 구성 요소 및 동작 메커니즘

비직렬 스케줄링을 지원하는 DBMS의 주요 구성 요소는 다음과 같습니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/기법 |
|:---|:---|:---|:---|
| **Transaction Manager** | 트랜잭션 생명주기 관리 | 사용자 요청을 연산 단위로 분해 및 시작/종료 제어 | BEGIN, COMMIT, ROLLBACK |
| **Scheduler (스케줄러)** | 연산 순서 결정 및 실행 | 현재 자원 상태(Lock) 확인 후 연산을 큐에 삽입 또는 차단 | 2PL (Two-Phase Locking), TO (Timestamp Ordering) |
| **Lock Manager (락 관리자)** | 동시성 제어 및 무결성 보장 | 데이터 항목에 대한 Lock(Shared/Exclusive) grant/wait 관리 | Lock Table, Wait-for Graph |
| **Buffer Manager** | 디스크 I/O 최소화 | 요청된 데이터 페이지가 메모리에 없을 때 디스크 로드 | LRU, MRU Replacement |
| **Recovery Manager** | 장애 복구 및 로깅 | 연산 전후 로그(Log) 기록을 통한 원자성 보장 | WAL (Write-Ahead Logging) |

#### 2. ASCII 구조 다이어그램: 연산 인터리빙 구조
아래는 T1과 T2가 비직렬 스케줄링에 의해 실행되는 과정을 시각화한 것입니다. 스케줄러는 T1의 I/O 대기 시간에 T2의 연산을 끼워 넣어 자원을 효율화합니다.

```text
       [ Non-serial Schedule Architecture: Interleaved Operations ]

   CPU Core (Active Processing)            Disk I/O (Waiting)
    ^                        ^             ^                      ^
    |  T1: Read(A)           |             |                      |
    |  [Buffer Miss] --------+------------>|  T1: Disk Read(A)    |
    |                        |             |                      |
    |  (Context Switch)      |             |                      |
    |  T2: Read(B)           |             |                      |
    |  T2: B = B * 2         |             |                      |
    |  T2: Write(B)          |             |                      |
    |                        |             |                      |
    |  T1: Resume (Return)   |             |                      |
    |  <-------(Data Loaded) |             |                      |
    |  T1: A = A + 10        |             |                      |
    |  T1: Write(A)          |             |                      |
    v                        v             v                      v

   Legend:
   ------
   T1 (Transaction 1): 스케줄러에 의해 연산이 분리됨
   T2 (Transaction 2): T1의 I/O Wait 동안 CPU를 점유하여 연산 수행
   Scheduler: T1의 Block 상태를 감지하고 T2를 Dispatch
```

**다이어그램 해설**:
위 다이어그램은 **시간적 중첩(Temporal Overlap)**을 보여줍니다.
1.  **t0-t1**: T1이 Read(A)를 요청하지만 데이터가 메모리에 없어 **I/O Wait(Blocking)** 상태로 진입합니다. 이때 CPU는 유휴 상태가 됩니다.
2.  **t1-t2**: 스케줄러는 즉시 제어권을 T2로 넘겨줍니다(Context Switch). T2는 CPU를 점유하여 Read(B), 연산, Write(B)를 수행합니다.
3.  **t3**: 디스크 I/O가 완료되면 인터럽트(Interrupt)가 발생하고, T1은 다시 CPU를 점유하여 남은 연산(A=A+10, Write)을 마무리합니다.
이러한 인터리빙을 통해 전체 실행 시간(Total Execution Time)은 직렬 실행일 때의 합(T1_time + T2_time)보다 훨씬 짧아집니다(Max(T1_time, T2_time)에 근접).

#### 3. 핵심 알고리즘 및 의사 코드 (Pseudo-code)

비직렬 스케줄링에서 가장 중요한 것은 **연산의 순서성(Conflict Serializability)**을 판단하는 것입니다. 아래는 충돌(Conflict) 기반의 스케줄링 로직입니다.

```python
# Non-serial Scheduler Logic with Conflict Checking
class Scheduler:
    def __init__(self):
        self.schedule_history = []

    def is_conflicting(self, op1, op2):
        # 두 연산이 같은 데이터 항목을 다루고, 적어도 하나가 Write인 경우
        if op1.item != op2.item:
            return False
        if op1.type == 'WRITE' or op2.type == 'WRITE':
            return True
        return False

    def execute(self, transaction_id, operation_type, data_item):
        current_op = Operation(transaction_id, operation_type, data_item)
        
        # 비직렬 스케줄의 핵심: 이전 연산들과의 충돌 검사
        for prev_op in reversed(self.schedule_history):
            if self.is_conflicting(current_op, prev_op):
                # 데이터 의존성(Dependency) 형성
                if prev_op.tx_id != current_op.tx_id:
                    # 순환 의존성(Cycle)이 발생하면 교착 상태(Deadlock) 가능성
                    self.check_deadlock_lock()
        
        # 실제 연산 수행
        self.schedule_history.append(current_op)
        self.perform_io_or_cpu_work(current_op)
```

**📢 섹션 요약 비유**: 비직렬 스케줄의 아키텍처는 **'복잡한 교차로에서 신호등과 교통정리관이 교통 흐름을 제어하는 시스템'**과 같습니다. 차량(연산)들은 서로 다른 방향(트랜잭션)에서 오지만, 신호등(스케줄러)은 한 방향의 차량이 통과할 때 다른 방향의 차량을 잠시 멈추거나, 충돌 없이 교차로 내부에 서로 다른 차량이 동시에 위치하도록 제어하여 전체적인 도로 혼잡을 해소합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

비직렬 스케줄은 무조건적인 병렬 처리가 아니라, **직렬 가능성(Serializability)**이라는 안전장치를 전제로 합니다.

#### 1. 심층 기술 비교: 직렬 vs 비직렬

| 비교 항목 | 직렬 스케줄 (Serial Schedule) | 비직렬 스케줄 (Non-serial Schedule) |
|:---|:---|:---|
| **실행 순서** | T1 -> T2 (순차적) | T1과 T2의 연산이 섞여서 실행 (Interleaved) |
| **자원 활용도** | 낮음 (I/O Wait 시 CPU 유휴) | 높음 (CPU와 I/O 중첩 가능) |
| **처리량(Throughput)** | 낮음 (단위 시간당 처리 건수 적음) | 높음 (시스템 리소스를 최대로 가동) |
| **데이터 일관성** | 항상 보장 (격리가 자연스럽게 이루어짐) | **충돌 직렬 가능성(Conflict Serializable) 조건 충족 시 보장** |
| **응답 시간** | 김 (대기열 길어짐) | 짧음 (적절한 CPU 시분할) |
| **오버헤드** | 매우 낮음 (제어 로직 불필요) | 높음 (Locking, Logging, Scheduler 오버헤드) |

#### 2. 과목 융합 분석: OS 및 네트워크와의 시너지

- **OS와의 융합 (CPU Scheduling)**:
    비직렬 스케줄링의 근간은 OS의 **CPU 스케줄링(CPU Scheduling)** 기법입니다. OS의 **선점형(Preemptive) 스케줄링(Round Robin, Multilevel Feedback Queue 등)**은 실행 중인 프로세스를 멈추고 다른 프로세스에 자원을 할당하는 기술인데, 이는 트랜잭션의 연산을 교차 실행하는 비직렬 스케줄과 동일한 맥락입니다. Context Switching 오버헤드를 줄이면서 동시성을 높이는 기술은 양쪽 영역의 공통 과제입니다.
    
- **네트워크와의 융합 (Packet Switching)**:
    네트워크의 **패킷 교환(Packet Switching)** 방식과 유사합니다. 전화 회선(Circuit Switching)이 한 사용자가 독점하는 것이라면, 패킷 교환은 데이터를 잘게 쪼개어(패킷) 여러 사용자의 데이터가 선로를 공유하여 전송하는 방식입니다. 비직렬 스케줄도 데이터 조각(연산)들을 섞어서 자원을 공유한다는 점에서 맥락을 같이합니다.

**📢 섹션 요약 비유**: 직렬과 비직렬의 차이는 **'단일 차로 도로와 다차로 고속도로'**의 차이와 같습니다. 단일 차로(직렬)는 사고가 없고 진입이 쉽지만, 교통체증(대기 시간)이 심각합니다. 다차로 고속도로(비직렬)는 진출입과 차로 변경(스케줄링)을 위한 복잡한 규칙과 신호 시스템(Lock, Protocol)이 필요하지만, 전체적인 흐름과 처리량은 훨씬 뛰어납니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

실무에서 비직렬 스케줄을 단순히 "빠르다"는 이유로 무분별하게 적용하면 데이터 파괴(Data Inconsistency)로 이어질 수 있습니다.

#### 1. 실무 시나리오 및 의사결정

**Scenario A: 금융권 계좌 이체 시스템**
- **상황**: A가 B에게 100만 원을 송금(T1)하는 동시에, B가 이자 수령으로 10만 원을 추가(T2)하려는 상황.
- **문제**: 비직렬 스케줄링을 제어 없이 수행하면 T1이 B의 잔액을 읽고(R), 갱신하기 전(W)에 T2가 끼어들어 B의 잔액을 읽고 갱신할 수 있습니다. 이 경우 **갱신 손실(Lost Update)** 발생.
- **결정**: 비직렬 스케줄을 사용하되, **Strict 2PL (Strict Two-Phase Locking)** 프로토콜을 적용하여 T1이 B의 데이터를 갱신하는 동안 T2가 해당 데이터를 읽지 못하도록 잠금(Lock)을 설정해야 함. 성능을 약간