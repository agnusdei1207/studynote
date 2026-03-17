+++
title = "[OS] 186. MLFQ 파라미터 (Multi-Level Feedback Queue Parameters)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["MLFQ", "Scheduling Parameters", "Priority", "Time Quantum"]
+++

# [OS] MLFQ 파라미터 (Multi-Level Feedback Queue Parameters)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: MLFQ (Multi-Level Feedback Queue)는 실행 시간을 미리 알 수 없는 환경에서, 프로세스의 **과거 행동(History Behavior)**을 기반으로 우선순위를 동적으로 재할당하는 **적응형 예측 스케줄링** 체계입니다.
> 2. **가치**: 5가지 핵심 파라미터(큐 개수, 알고리즘, 퀀텀, 강격/격하 규칙)의 세밀한 튜닝을 통해, 대화형 작업의 **Response Time (응답 시간)**과 배치 작업의 **Turnaround Time (반환 시간)**을 동시에 최적화합니다.
> 3. **융합**: 현대 커널의 **CFS (Completely Fair Scheduler)** 및 클라우드 Hypervisor의 **Credit Scheduler** 이론적 기반이며, TCP 혼잡 제어 및 네트워크 **QoS (Quality of Service)** 큐 관리와 동일한 피드백 루프 메커니즘을 공유합니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
스케줄링 이론의 성배는 'CPU Burst(집중 사용)'를 정확히 예측하는 것입니다. 전통적인 **SJF (Shortest Job First)**는 최적의 평균 반환 시간을 보장하지만, 실행 시간을 미리 알 수 없다는 치명적인 결함이 있습니다. 반면 **RR (Round Robin)**은 모든 프로세스를 동등하게 대우하여 대화형 작업에 유리하지만, 문맥 교환(Context Switching) 오버헤드가 크고 긴 작업의 처리량을 저하시킵니다.

**MLFQ**는 **"과거의 CPU 사용 패턴은 미래의 행동을 예측하는 지표이다"**라는 가설하에 탄생했습니다. 프로세스를 처음에는 '짧은 작업'으로 가정하고 최상위 우선순위 큐에 할당했다가, CPU 시간을 독점하려 하면 즉시 하위 큐로 격하(Demotion)시키는 방식입니다. 이는 별도의 사전 정보 없이도 시스템이 스스로 '긴 작업'과 '짧은 작업'을 분류해내는 **Self-Tuning (자가 튜닝)** 메커니즘입니다.

#### 2. 등장 배경 및 기술적 진화
① **기존 한계 (Pre-MLFQ)**: 고정된 우선순위를 사용하면 **Priority Inversion (우선순위 역전)**과 **Starvation (기아 현상)**이 발생하여 시스템 반응성이 저하됩니다.
② **혁신적 패러다임**: 피드백(Feedback) 루프를 도입하여, **Interactive Process (대화형 프로세스)**는 상위 큐에 유지시켜 반응성을 확보하고, **CPU-Bound Process (연산 중심 프로세스)**는 하위 큐로 이동시켜 시스템 자원을 독점하지 못하게 막습니다.
③ **현재 비즈니스 요구**: 클라우드 환경에서는 수천 개의 **VM (Virtual Machine)** 또는 컨테이너가 단일 호스트에서 경쟁하므로, MLFQ 파라미터를 튜닝하여 **SLA (Service Level Agreement)**를 준수하는 것이 필수적입니다.

#### 3. MLFQ 아키텍처 개관도

```text
      [Scheduler Core Policy]
              |
   +----------+----------+
   |  Priority Boosting | <--- Periodic Interrupt (e.g., every 1s)
   +----------+----------+       (Prevents Starvation)
              |
   +----------+----------+
   |  Multi-Level Queue  |
   +----------+----------+
   | Q0 | Q1 | Q2 | ... | Qn |
   +----+----+----+-----+----+
    |    |    |    |     |
  [RR] [RR] [RR]    |   [FCFS]
   |    |    |    |     |
   v    v    v    v     v
 [High]      [Medium]    [Low]
 (Interactive) (Mixed)   (Batch)
```

*(도해: 우선순위 부스팅 모듈이 주기적으로 하위 큐의 프로세스들을 상위 큐로 재배치하여 기아 현상을 방지하고, 각 큐 계층(Queue Hierarchy)은 서로 다른 스케줄링 알고리즘을 운영합니다.)*

**📢 섹션 요약 비유**:
마치 **공항의 심사대 우선 순위 라인**과 같습니다. 
마일리지가 높은 VIP(Q0)나 비즈니스석은 언제나 짧은 대기열로 바로 통과하지만, 일반석(Q2)은 줄이 길 수 있습니다. 그러나 공항은 주기적으로 '일반석' 승객 중에서 대기 시간이 너무 긴 승객을 발견하면 특별 진료 대기열(Aging)로 안내하여 영원히 기다리게 하지 않으려 노력합니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. MLFQ 구성 및 5가지 핵심 파라미터 (5 Key Parameters)
MLFQ는 단일 알고리즘이 아니라, 시스템 설계자가 의도에 따라 동작을 제어할 수 있는 **파라미터화된 프레임워크**입니다. 시스템의 성격을 결정짓는 5가지 핵심 설정값은 다음과 같습니다.

| 파라미터 (Parameter) | 상세 역할 및 내부 동작 (Role & Mechanism) | 주요 프로토콜/규칙 (Protocol/Rules) | 비유 (Analogy) |
|:---|:---|:---|:---|
| **1. 큐의 개수**<br>(Queue Count) | 우선순위 계층의 깊이를 결정함. | 너무 많으면(>256) 오버헤드 증가, 너무 적으면(<2) 구분력 상실.<br>일반적으로 **O(log N)** 스케줄링 효율을 고려하여 설정. | 건물의 엘리베이터 정차 층수 |
| **2. 큐별 알고리즘**<br>(Queue Algorithm) | 각 계층 내에서의 스케줄링 정책. | 상위 큐: **RR (Round Robin)** (Preemption 중요)<br>하위 큐: **FCFS (First Come, First Served)** (Throughput 중요) | 각 층의 호출 방식 (단순 대기/순환) |
| **3. 타임 슬라이스**<br>(Time Quantum) | 상위 큐일수록 짧게(빠른 응답), 하위 큐일수록 길게(오버헤드 감소). | 공비 등비수열(Exponential) 설정이 효율적.<br>예: Q0=10ms, Q1=20ms, Q2=40ms | 주어지는 휴식 시간의 길이 |
| **4. 격하 규칙**<br>(Demotion Rule) | 프로세스가 CPU를 독점하려 할 때 우선순위를 낮춤. | 할당된 Time Quantum을 모두 소진하면 즉시 하부 큐로 이동.<br>**Preemption (선점)**의 핵심 트리거. | 규정 위반 시 하위 부서로 좌천 |
| **5. 강격 규칙**<br>(Promotion Rule) | 오래 기다린 프로세스를 구제하여 Starvation 방지. | **Aging (에이징)**: 일정 주기(S)마다 모든 프로세스를 최상위 큐로 리셋.<br>또는 시스템 부하가 낮을 때 상위 큐로 이동. | 정기 인사 고과를 통한 승진 |

#### 2. 파라미터 기반 상태 전이 및 데이터 흐름

```text
                           [System Boot / Initialization]
                                    |
                                    v
                      +-----------------------------+
                      |   NEW PROCESS Arrives      |
                      +-----------------------------+
                          | (Rule: Priority Boost)
                          v
      +-------------------------------------------------------+
      |                 TOP PRIORITY (Q0)                     |
      |   Algorithm: RR (Quantum: 8ms)                       |
      |   Goal: Fast Response for Interactive Jobs           |
      +-------------------------------------------------------+
          |                       ^                       |
   (Y) Quantum Expired?    (X) I/O Request or      (Z) CPU
          |                  Short Burst             Released
          v                      | (Return to Q0)      |
      +-------------------------------------------------------+
      |               MEDIUM PRIORITY (Q1)                   |
      |   Algorithm: RR (Quantum: 16ms)                      |
      |   Goal: Balance for Standard Tasks                   |
      +-------------------------------------------------------+
          |                       ^
   (Y) Quantum Expired?    (Z) CPU Released
          v                      |
      +-------------------------------------------------------+
      |                LOW PRIORITY (Q2)                     |
      |   Algorithm: FCFS (Non-preemptive)                   |
      |   Goal: Maximize Throughput for Batch Jobs           |
      +-------------------------------------------------------+
          |
          v
                   [Process Termination / Exit]

   Legend:
   (Y) Yield/Demote: Time Quantum 초과로 인한 강등
   (Z) Yield/Coop: 자발적 CPU 반납 (I/O 대기 등)
```

**[다이어그램 심층 해설]**
이 다이어그램은 MLFQ의 **Dynamic Priority Adjustment (동적 우선순위 조정)** 과정을 도식화한 것입니다.
1. **진입 전략**: 모든 프로세스는 '낙관적(Optimistic)' 전략에 따라 최상위 **Q0**에서 시작합니다. 이는 모든 작업이 짧게 끝날 것이라는 가정에 기반합니다.
2. **격하 메커니즘 (Downward Flow)**: 만약 프로세스가 **Q0**의 8ms 슬라이스를 모두 소진(Consume)한다면, 스케줄러는 이를 "CPU를 독점하려 하는 긴 작업"으로 간주하여 즉시 **Q1**으로 강격(Demotion)합니다. **Q1**에서도 16ms를 소진하면 **Q2**로 떨어지는 식입니다.
3. **상향 복귀 메커니즘 (Upward Flow)**: 만약 프로세스가 I/O 요청과 같은 이유로 CPU를 먼저 반납(Yield)하면, 우선순위는 그대로 유지되거나 다시 스케줄링 됩니다. 또한, 주기적인 **Priority Boost (우선순위 부스팅)** 인터럽트가 발생하면 모든 큐의 프로세스가 **Q0**로 재집결되어 기아 현상(Starvation)이 해소됩니다.

#### 3. 핵심 알고리즘 및 의사 코드 (Pseudo-code)
MLFQ의 효율성은 **Context Switch (문맥 교환)** 비용을 얼마나 줄이느냐에 달려 있습니다. 실무 구현 시 큐 관리는 보통 **Linked List (연결 리스트)** 또는 **Bitmap Priority Queue**를 사용합니다.

```c
// MLFQ Scheduling Logic Pseudo-code
struct MLFQ {
    Queue queues[NUM_PRIORITY_LEVELS];
    int time_quantums[NUM_PRIORITY_LEVELS]; // {8, 16, 32, ...}
};

void schedule(struct MLFQ* mlfq) {
    while (system_active) {
        // 1. Priority Boost Rule (Aging)
        if (current_time >= last_boost_time + BOOST_INTERVAL) {
            move_all_processes_to_top_queue(mlfq);
            last_boost_time = current_time;
        }

        // 2. Select Highest Priority Non-empty Queue
        int q_idx = find_highest_non_empty_queue(mlfq);
        Process* proc = dequeue(&(mlfq->queues[q_idx]));

        // 3. Dispatch Process
        dispatch(proc);

        // 4. Wait for Interrupt (Timer or I/O)
        Event event = wait_for_interrupt();

        // 5. Demotion Logic (Deep Dive)
        if (event == TIMER_EXPIRED) {
            // Used full quantum -> Likely CPU Bound -> Demote
            if (q_idx < NUM_PRIORITY_LEVELS - 1) {
                enqueue(&(mlfq->queues[q_idx + 1]), proc);
                log_process(proc, "Demoted to Q", q_idx + 1);
            } else {
                enqueue(&(mlfq->queues[q_idx]), proc); // Stay in lowest
            }
        } else if (event == IO_REQUEST) {
            // Gave up CPU -> Keep Priority (Still Interactive)
            enqueue(&(mlfq->queues[q_idx]), proc); 
        }
    }
}
```

**📢 섹션 요약 비유**:
마치 **주식 투자의 리스크 관리 시스템**과 유사합니다.
신규 투자자(프로세스)는 처음에 '공격적 성장 포트폴리오(Q0)'에 배치되어 단기 수익을 노립니다. 그러나 시간이 지나도 수익이 나지 않고 잠만 자는(CPU를 독점하는) '값주买' 종목으로 판명되면, 시스템은 이를 '안전 자산 포트폴리오(Q2)'로 재분류하여 리스크를 격리합니다. 단, 시장이 폭락할 때(Priority Boost)는 모든 자산을 다시 현금화해 기회를 주는 것과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: MLFQ vs. Legacy Algorithms

| 비교 항목 | **MLFQ (Multi-Level Feedback Queue)** | **RR (Round Robin)** | **SJF (Shortest Job First)** |
|:---|:---|:---|:---|
| **우선순위 (Priority)** | **Adaptive (적응형)**<br>과거 행동에 따라 동적 변경 | **Static (고정형)**<br>모든 프로세스 동등 취급 | **Static (고정형)**<br>Burst 길이에 따라 고정 |
| **필요 정보 (Info Req)** | 없음 (관찰 기반 Learning) | 없음 | 실행 시간 선행 정보 필요 |
| **평균 반환 시간<br>(Avg. Turnaround)** | 양호 (짧은 작업 최적화) | 중립 (긴 작업과 짧은 작업 평균) | **최우수** (단, 정보가 정확할 시) |
| **응답 시간<br>(Response Time)** | **우수** (상위 큐의 짧은 Quantum) | 양호 (Quantum에 의존) | 불량 (긴 작업이 오면 지연) |
| **문맥 교환 오버헤드<br>(Context Switch)** | 발생함 (특히 상위 큐) | 빈번하게 발생 | 적음 |
| **기아 현상<br>(Starvation)** | 가능성 있음 (Aging으로 해결) | 없음 (Fairness 보장) | 긴 작업에 대해 발생 가능 |

#### 2. 과목 융합 관점 (OS, Architecture, Network)

1.  **OS & Architecture (Cache Locality & TLB)**:
    MLFQ의 하위 큐(FCFS)에 있는 프로세스는 긴 **CPU Burst** 특성을 가지므로, **L1/L2 Cache** 및 **TLB (Translation Lookaside Buffer)**의 지역성(Locality)을 활용하기 유리합니다. 반대로 상위 큐에서 짧은 **Time Quantum**으로 인해 빈번한 **Context Switching**이 발생하면, 캐시 워밍업(Cache Warm-up) 시간보다 교환 시간이 더 길어져 **Cache Thrashing**이 발생할 수 있습니다. 따라서 MLFQ �