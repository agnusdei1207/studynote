+++
title = "[OS] 184. 큐 간 스케줄링 (Inter-queue Scheduling)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Multi-level Queue", "Inter-queue Scheduling", "Fixed Priority", "Time Slice"]
+++

# 큐 간 스케줄링 (Inter-queue Scheduling)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **다단계 큐 (Multi-level Queue)** 환경에서 이질적인 작업 그룹 간의 **CPU (Central Processing Unit)** 자원 할당 순서와 할당량을 결정하는 상위 계층 스케줄링 메커니즘입니다.
> 2. **가치**: 시스템 응답성(Response Time)과 처리량(Throughput)의 균형을 최적화하며, 우선순위 기반 서비스 제공 시 발생하는 **기아 현상(Starvation)**을 방지하는 정교한 자원 분배 전략을 구현합니다.
> 3. **융합**: 실시간 시스템의 **Hard/Soft Real-time** 요구사항과 범용 **OS (Operating System)**의 공정성을 동시에 충족시키기 위해 **우선순위 역전(Priority Inversion)** 방지 및 **Aging** 기법과 결합하여 고도화됩니다.

+++

### Ⅰ. 개요 (Context & Background)

**큐 간 스케줄링 (Inter-queue Scheduling)**은 다단계 큐 스케줄링 아키텍처에서, 서로 다른 실행 특성(예: I/O Bound vs CPU Bound)을 가진 여러 개의 준비 큐(Ready Queue) 중 **어느 큐에 CPU 자원을 먼저 배정할 것인가**를 결정하는 포괄적인 제어 정책입니다. 단일 큐 내의 프로세스 순서를 결정하는 '큐 내 스케줄링(Intra-queue Scheduling)'과는 대조적으로, 시스템 전체의 자원 분배 철학을 정의하는 거시적 관리 기법입니다.

현대 OS의 **다단계 피드백 큐 (Multi-level Feedback Queue, MLFQ)** 환경에서는 시스템 프로세스, 대화형 프로세스(Interactive), 배치 프로세스(Batch) 등이 분리된 큐에서 대기합니다. 이때 단순히 우선순위가 높은 큐만 무조건 처리하면 하위 큐의 작업이 영원히 연기되는 기아 현상이 발생하므로, 각 큐에 적절한 CPU 시간 할당(Time Slice)과 순환 순서를 부여하는 전략이 필수적입니다.

**💡 개념 비유**
이는 병원 응급실의 **분료(Triage) 및 진료 순서 시스템**과 유사합니다. 심정지 환자(Real-time)가 오면 즉시 수술실로 들어가지만, 모든 자원을 그에게만 쏟을 수는 없습니다. 의료진은 경증 환자(Batch)도 방치하지 않도록 의사를 순회시키거나, 특정 시간대에는 예방 진료를 실시하는 룰을 정해야 합니다. 큐 간 스케줄링은 이 '자원 배분 룰'을 시스템 차원에서 설계하는 것입니다.

**등장 배경**
1.  **기존 한계**: 단일 큐 방식(FIFO, Round Robin)에서는 I/O Burst와 CPU Burst가 섞여 있어 **캐시 지역성(Cache Locality)**이 저하되고, 대화형 작업의 응답 속도가 보장되지 않는 문제가 존재했습니다.
2.  **혁신적 패러다임**: 작업의 특성별로 큐를 물리적으로 분리(Multi-level)하여 **문맥 교환(Context Switching)** 오버헤드를 줄이고, 각 워크로드에 최적화된 알고리즘(예: 상위 큐는 FCFS, 하위 큐는 RR)을 적용하는 유연한 아키텍처가 도입되었습니다.
3.  **현재의 비즈니스 요구**: 클라우드 가상화 및 컨테이너 환경에서 **SLA (Service Level Agreement)**를 준수하기 위해, '보장된 리소스(Reservation)'와 '최적 리소스(Utilization)' 사이의 균형을 맞추는 **QoS (Quality of Service)** 제어가 필수적인 요구로 대두되었습니다.

**📢 섹션 요약 비유**
> 마치 고속도로 톨게이트에 **하이패스 차선(시스템/우선순위 큐)**과 **현금 결제 차선(일반/배치 큐)**을 따로 설치해두되, 하이패스 차선이 너무 병목되지 않도록 입구를 통제하는 교통 정책과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

큐 간 스케줄링의 핵심은 **'어떤 큐를 선택할 것인가(Scheduling Logic)'**와 **'얼마나 오래 실행할 것인가(Time Quantum)'**를 설정하는 것입니다. 본 섹션에서는 시스템의 동작 원리와 구조를 깊이 있게 분석합니다.

#### 1. 구성 요소 상세 분석표

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 (Internal Mechanism) | 주요 프로토콜/속성 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **Ready Queues (준비 큐들)** | 워크로드 분류 수용 | 프로세스의 특성(길이, I/O 빈도)에 따라 분리되어 저장됨. 각 큐는 독립적인 데이터 구조(연결 리스트 등) 유지. | FIFO, RR (Round Robin), Priority | 대기실 구역 (응급, 외래, 입원) |
| **Inter-queue Scheduler** | 큐 선택 및 자원 분배 | 각 큐의 상태를 모니터링하며, 정책(Priority, Time Slice)에 따라 다음 실행할 큐를 지정. 디스패처(Dispatcher)에 제어권 넘김. | Fixed Priority, Time Slicing | 교통 통제 센터 |
| **Priority Levels (우선순위)** | 서비스 순위 결정 | 정적(Static)으로 고정된 순위나, 동적(Dynamic)으로 부하에 따라 변동될 수 있음. | 0(Highest) ~ N(Lowest) | 차선 등급 (1급 도로 vs 지방도) |
| **Time Quantum / Slice** | 자원 할당량 제어 | 각 큐가 CPU를 선점할 수 있는 최대 시간. 이를 초과하면 다른 큐로 기회가 넘어감(Preemption). | 10ms ~ 100ms | 신호 대기 시간 (초록불 지속 시간) |
| **Aging Mechanism** | 기아 현상(Starvation) 방지 | 대기 시간이 길어진 하위 큐의 프로세스 우선순위를 일시적으로 상향 조정하여 서비스 기회 부여. | `Priority = Base + (WaitTime / Constant)` | 대기 승객 우선 탑승권 발급 |

#### 2. ASCII 구조 다이어그램: 시스템 아키텍처
아래는 **MLFQ (Multi-level Feedback Queue)**를 기반으로 한 큐 간 스케줄링의 논리적 흐름과 데이터 구조를 도식화한 것입니다.

```text
      +-------------------------------------------------------+
      |           Inter-queue Scheduling Logic (Kernel)       |
      |   [ Decision Matrix: Priority Check vs Time Slice ]   |
      +--------------------------+----------------------------+
                                 |
                Timer Interrupt (Clock Tick)
                                 |
            +--------------------+--------------------+
            |                    |                    |
            v                    v                    v
    +---------------+    +---------------+    +---------------+
    |   Queue 0     |    |   Queue 1     |    |   Queue 2     |
    | (System/I-O)  |    | (Interactive) |    |   (Batch)     |
    | High Priority |    |   Mid Priority|    |  Low Priority |
    +---------------+    +---------------+    +---------------+
    | Intra: FIFO   |    | Intra: RR     |    | Intra: FCFS   |
    +-------+-------+    +-------+-------+    +-------+-------+
            |                    |                    |
      [Head: P_System]     [Head: P_Interactive]  [Head: P_Batch]
            |                    |                    |
            +------+  Preemption Control  +----------+
                   |                      |
                   v                      v
                 CPU CORE
            (Execution Context)
```

**[도해 상세 설명]**
1.  **다층적 큐 구조**: 시스템은 세 개의 준비 큐(Queue 0, 1, 2)를 가지며, 번호가 낮을수록 높은 우선순위를 가집니다. 각 큐 내부(Intra-queue)에서도 서로 다른 스케줄링 알고리즘(예: 시스템 큐는 FIFO, 대화형 큐는 RR)을 운영할 수 있습니다.
2.  **스케줄러 로직(Decision Matrix)**: 인터럽트가 발생하면 스케줄러는 가장 높은 우선순위의 큐(Queue 0)부터 검사합니다. 만약 Queue 0에 프로세스가 있다면, 하위 큐(Queue 1, 2)에 실행 중인 프로세스가 있더라도 이를 즉시 선점(Preemption)하고 Queue 0의 작업을 수행합니다.
3.  **자원 분배**: 상위 큐가 지속적으로 존재하면 하위 큐는 실행되지 않으므로, 시스템은 주기적으로 혹은 누적 시간에 따라 하위 큐에 기회를 부여하는 로직(Aging 등)을 수행해야 합니다.

#### 3. 심층 동작 원리 (Step-by-Step)

1.  **큐 할당 (Queue Assignment)**:
    프로세스가 생성되거나 I/O 작업을 완료하여 준비(Ready) 상태가 되면, 스케줄러는 해당 프로세스의 특성(프로세서 사용 시간, 캐릭터 등)을 분석하여 적절한 큐에 삽입합니다.
2.  **상위 우선순위 검사 (Priority Check)**:
    **CPU (Central Processing Unit)**가 한 프로세스를 실행 중일 때, 타이머 인터럽트나 높은 우선순위의 프로세스 도착(Wake up) 이벤트가 발생하면, 스케줄러는 현재 실행 중인 큐보다 상위 큐에 작업이 있는지 즉시 스캔합니다.
3.  **의사결정 및 디스패칭 (Decision & Dispatch)**:
    상위 큐에 작업이 존재한다면, **문맥 교환(Context Switching)**을 통해 현재 프로세스를 내쫓고(Precise Preemption), 상위 큐의 프로세스를 실행합니다. 이때 오버헤드를 줄이기 위해 캐시 플러시 등의 하드웨어적 최적화가 수반됩니다.
4.  **시간 할당 및 순환 (Time Slicing & Round Robin)**:
    만약 상위 큐가 비어있다면, 현재 큐의 **Time Slice (Time Quantum)**를 소진할 때까지 실행합니다. 소진 시 하위 큐로 넘어가거나, 같은 큐 내의 다음 프로세스로 넘어갑니다.

#### 4. 핵심 알고리즘 및 의사코드 (Pseudo Code)
아래는 간단한 큐 간 스케줄링과 기아 현상 방지(Aging)를 구현한 C-style 의사코드입니다.

```c
#define NUM_QUEUES 3
#define AGING_THRESHOLD 100 // Time units

struct Process {
    int pid;
    int priority;       // 0 (High) ~ 2 (Low)
    int wait_time;
};

// Ready Queues for each level
struct Queue ready_queues[NUM_QUEUES];

void inter_queue_scheduler() {
    while (true) {
        // 1. Aging Logic: Boost priorities of starving processes in lower queues
        for (int q = 1; q < NUM_QUEUES; q++) {
            for each process in ready_queues[q] {
                process.wait_time++;
                if (process.wait_time > AGING_THRESHOLD) {
                    // Move process to a higher priority queue (q-1)
                    move_to_queue(process, ready_queues[q-1]);
                    process.wait_time = 0;
                    print("Priority Boosted for PID: %d", process.pid);
                }
            }
        }

        // 2. Inter-queue Scheduling: Select highest non-empty queue
        int selected_queue = -1;
        for (int q = 0; q < NUM_QUEUES; q++) {
            if (!is_empty(ready_queues[q])) {
                selected_queue = q;
                break; // Stop at the highest priority queue
            }
        }

        // 3. Dispatch or Idle
        if (selected_queue != -1) {
            Process *p = dequeue(ready_queues[selected_queue]);
            dispatch(p); // Run process
        } else {
            idle(); // System Idle
        }
    }
}
```

**📢 섹션 요약 비유**
> 마치 기업 내에서 이사회(시스템 큐)의 긴급 결재가 들어오면 말단 직원(배치 큐)의 단순 작업이 아무리 중요해도 즉시 중단(선점)되고 보고를 올려야 하지만, 공장 관리자(대화형 큐)가 생산 라인을 점검하는 시간에는 사장님도 방해하지 않는 것과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

본 섹션에서는 큐 간 스케줄링의 다양한 접근 방식을 비교하고, 네트워크 및 컴퓨터 구조 등 타 분야와의 융합 관점을 분석합니다.

#### 1. 심층 기술 비교표: 큐 간 스케줄링 전략

| 구분 | 고정 우선순위 선점 (Fixed Priority Preemptive) | 시간 할당 (Time Slicing / Round Robin) |
|:---|:---|:---|
| **정의** | 상위 큐가 항상 하위 큐에 대해 우선권을 가짐. | 각 큐에 CPU 시간을 일정 비율(%)로 할당하여 순환. |
| **동작 메커니즘** | 상위 큐에 프로세스 도착 시 즉시 **Context Switching** 발생. | 타이머 만료 시 강제로 다른 큐로 제어권 이전(Turn-taking). |
| **장점 (Pros)** | **응답성(Response Time)**이 우수함. <br> Hard Real-time 시스템에 적합. | **공정성(Fairness)**이 보장됨. <br> 기아 현상(Starvation)이 발생하지 않음. |
| **단점 (Cons)** | 하위 큐의 **Starvation** 가능성이 매우 높음. <br> 우선순위 역전(Priority Inversion) 위험. | 상위 큐 작업의 **대기 시간(Waiting Time)**이 길어질 수 있음. |
| **지표 (Metrics)** | Deterministic Latency 보장. | Average Waiting Time 최소화에 유리. |

#### 2. 융합 분석: 타 기술 영역과의 시너지

**A. 운영체제 & 네트워크 (QoS와의 연계)**
*   네트워크 패킷 스케줄링의 **QoS (Quality of Service)** 기술과 직접적으로 연결됩니다.
*   **DiffServ (Differentiated Services)** 모델에서는 패킷 헤더의 **DSCP (Differentiated Services Code Point)** 값에 따라 큐를 분리하고, 큐 간 스케줄링(