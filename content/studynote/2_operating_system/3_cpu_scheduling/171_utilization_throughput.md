+++
title = "[OS] 171. CPU 이용률 (Utilization) 및 처리량 (Throughput)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["CPU Utilization", "Throughput", "Scheduling Criteria"]
+++

# [OS] 171. CPU 이용률 (Utilization) 및 처리량 (Throughput)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **CPU 이용률 (CPU Utilization)**은 컴퓨팅 자원의 낭비를 최소화하는 '효율성(Efficiency)' 지표이며, **처리량 (Throughput)**은 시스템이 단위 시간당 처리하는 일의 양을 의미하는 '생산성(Productivity)' 지표임. 두 지표는 상호 의존적이면서도 Trade-off 관계를 형성함.
> 2. **가치**: **멀티프로그래밍 (Multiprogramming)** 환경에서 CPU를 유휴 상태(Idling)로 두지 않고 최대한 가동하여 서비스 수준 계약(SLA)을 준수하고, 서버 수용력(Capacity) 계산의 근거가 되어 투자 대비(ROI) 성과를 극대화함.
> 3. **융합**: 단순한 OS 지표를 넘어 클라우드 오토스케일링(Auto-scaling) 정책의 트리거, 성능 테스트(Stress Test)의 병목 식별 기준, 그리고 비용 절감을 위한 리소스 라이선싱(Right-sizing)의 핵심 데이터로 활용됨.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 1. 개념 및 철학
운영체제(OS)의 가장 핵심적인 자원인 **CPU (Central Processing Unit)**의 성능을 평가하기 위해서는 단순한 클럭 속도(Clock Speed)와 같은 물리적 속성뿐만 아니라, 자원이 시스템 운영 관점에서 얼마나 효율적으로 사용되고 있는지를 측정하는 논리적 척도가 필요합니다. 이를 위해 시스템 중향(System-oriented) 관점에서 **CPU 이용률**과 **처리량**이라는 두 가지 지표를 정의합니다.

**CPU 이용률**은 전체 가용 시간 중 CPU가 실제로 유용한 일(User/System Mode 실행)을 처리한 시간의 비율을 나타내는 '효율성' 척도입니다. 반면, **처리량**은 단위 시간당 완료된 프로세스(Process)의 수를 의미하는 '생산성' 척도입니다. 이 두 지표는 시스템의 목적에 따라 상충(Trade-off) 또는 상승 효과(Synergy)를 가질 수 있습니다.

**💡 비유**
자동차 생산 공장의 로봇 팔(CPU)이 하루 종일 멈추지 않고 움직이는 비율이 **이용률**이며, 하루에 완성되어 나온 자동차의 대수가 **처리량**입니다.

#### 2. 등장 배경 및 진화
과거 단일 프로그래밍(Uni-programming) 환경이나 초기 일괄 처리(Batch Processing) 시스템에서는 입출력(I/O) 작업 시 CPU가 반드시 대기(Polling)해야 했으므로, CPU가 놀고 있는 시간이 많아 이용률이 낮았습니다. 이는 비싼 하드웨어 자원의 낭비로 이어졌습니다.

이를 극복하기 위해 **시분할 시스템 (Time-sharing System)**과 **선점형 멀티태스킹 (Preemptive Multitasking)** 기술이 도입되었습니다. 한 프로세스가 I/O를 요청하여 대기(Block)하는 동안, 운영체제의 **스케줄러 (Scheduler)**는 즉시 CPU를 다른 준비된(Ready) 프로세스에게 할당합니다. 이를 통해 CPU의 '구멍'을 메워 이용률을 100%에 가깝게 끌어올리는 것이 현대 OS의 핵심 과제가 되었습니다.

#### 3. 비즈니스적 요구
오늘날 클라우드 컴퓨팅 환경에서는 **CPU 이용률**을 기반으로 한 '종량제 과금'과 '오토스케일링'이 비즈니스의 직접적인 비용(Cost)과 연결됩니다. 이용률이 너무 낮으면 비용 낭비이며, 너무 높으면 **쓰레싱 (Thrashing)** 현상이 발생하여 **처리량**이 급격히 떨어지고 사용자 경험(UX)이 저하되므로, 이 두 지표의 균형 잡힌 제어가 필수적입니다.

**📢 섹션 요약 비유: 고속도로 톨게이트 관제소**
CPU 스케줄링의 이용률과 처리량 관리는, **복잡한 고속도로 톨게이트에서 8개 차로를 모두 24시간 내내 가동(CPU Utilization 극대화)시켜 차량이 멈추지 않게 하면서도, 1시간당 통과시키는 차량 대수(Throughput 극대화)를 최대화하는 것과 같습니다. 차로(CPU)가 비어 있으면 국고 손실(이용률 저하)이지만, 차량이 너무 몰려들어 아예 못 움직이면(혼잡) 처리량 자체가 0이 되어버립니다.**

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

#### 1. 구성 요소 상세 분석표

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 주요 프로토콜/메커니즘 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **CPU (Central Processing Unit)** | 연산 수행 자원 | 명령어 사이클(Instruction Cycle) 반복: Fetch → Decode → Execute | 인터럽트(Interrupt), 클럭 신호 | 요리사 |
| **OS Scheduler (Dispatcher)** | 자원 분배 관리자 | Ready Queue에서 프로세스 선정 → Context Switch 수행 | 스케줄링 알고리즘(MLFQ, RR 등) | 주방장/주문 접수원 |
| **Ready Queue** | 대기 공간 | CPU 할당을 기다리는 프로세스의 PCB(Process Control Block) 연결 리스트 | FIFO, Priority Queue | 주문 대기열 |
| **I/O Device** | 경쟁/병렬 수행 요소 | 프로세스의 I/O 요청 처리 중 CPU는 다른 작업 수행 가능 | DMA (Direct Memory Access), Polling | 재료 정리 보조 요리사 |
| **Idle Process** | 빈자원 채움 | Ready Queue에 프로세스가 없을 때 실행되며, HLT(Halt) 명령으로 전력 절약 | System Idle Task | 청소 하며 기다림 |

#### 2. 정의 및 수학적 모델

**1) CPU 이용률 (CPU Utilization)**
CPU가 전체 시간 중 '바쁜(Busy)' 상태에 있는 시간의 백분율입니다.
- **수식**: 
$$ U = \frac{T_{busy}}{T_{busy} + T_{idle}} \times 100 (\%) $$
  - 여기서 $T_{busy}$는 사용자(User) 및 커널(Kernel) 모드에서의 실행 시간이며, $T_{idle}$은 유휴(Idle) 루프나 대기(Wait) 상태 시간입니다.
- **실무 목표치**:
  - **범용 서버**: 40~70% (트래픽 스파이크 대비 여유 필요)
  - **배치 서버**: 90%+ (종료 시간 최소화가 목표)
  - **임계점 (Critical Point)**: 보통 80%를 넘어서면 지연 시간(Latency)이 급격히 증가하기 시작합니다.

**2) 처리량 (Throughput)**
단위 시간당 완료된 프로세스의 평균 개수입니다. 작업(Work)의 완성도를 나타냅니다.
- **수식**: 
$$ Th = \frac{N_{completed}}{T_{total}} $$
  - 단위: 보통 **TPS (Transactions Per Second)**, **RPS (Requests Per Second)** 또은 Jobs/hour를 사용합니다.
- **최대 처리량 (Max Throughput)**: 시스템이 포화(Saturation) 상태에 도달했을 때의 처리량으로, 이 이상으로 부하를 주면 처리량이 오히려 감소하거나 응답하지 않습니다.

#### 3. 시스템 상태 및 데이터 흐름 (ASCII)

다음은 **멀티프로그래밍 환경**에서 프로세스의 상태 전이에 따른 CPU 자원 사용과 처리량 생성 과정을 도식화한 것입니다. **컨텍스트 스위칭 (Context Switching)** 비용을 감안하면서도 CPU를 계속 바쁘게 만드는 메커니즘을 확인하십시오.

```text
   [Process State Transition & CPU Utilization View]

      (High Level Overview)         (Microscopic View - Execution)
   
  New Process                                 Terminated
      |                                           ^
      v                                           | (Job Done)
+-------------+       Ready Queue        +------------------+
|  Admission  | -------------------->   |                  |  <-----+
|  (Long Term |  [PCB1][PCB2][PCB3]...  |   Short Term     |        |
|  Scheduler) |       (Waiting)         |   Scheduler      |        |
+-------------+                          | (Dispatcher)     |        |
                                         +-------+----------+        |
                                                 | Dispatch        |
                                                 v                 |
  [CPU Utilization Accumulator]         +------------------+        |
                                         |     CPU Core     |        |
      T_busy: Execution  +-------------> | [Running State]  |        |
      T_idle: Idle Loop   |              | [Registers/PC]   |        |
                         |              +------------------+        |
                         |                   ^      |               |
                   Timer Expire         I/O Req   | Interrupt      |
                         |                   |      v               |
                         |              +------------------+        |
                         +--------------|      I/O Device  |-------+
                                        | (Disk/Network)   |
                                        +------------------+
                                               |
                                               v
                                        (Blocked/Wait State)
```

**[다이어그램 해설]**
위 다이어그램은 운영체제 커널이 CPU 자원을 평가하는 두 가지 핵심 관점을 보여줍니다.
1.  **거시적 관점 (Macro View)**: **장기 스케줄러 (Long Term Scheduler)**는 메모리에 올릴 프로세스의 양(**Degree of Multiprogramming**)을 조절합니다. 프로세스가 너무 적으면 CPU가 놀게 되어 **이용률**이 떨어지고, 너무 많으면 **Ready Queue**가 길어져 **Context Switching** 오버헤드가 발생합니다.
2.  **미시적 관점 (Micro View)**: **단기 스케줄러 (Short Term Scheduler)**는 **Dispatcher**를 통해 CPU를 누구에게 줄지 결정합니다. 프로세스가 I/O 요청으로 **Blocked** 상태로 가는 순간, CPU는 즉시 Ready Queue의 다른 프로세스를 실행하여 **Idle Time**을 최소화합니다. 이 과정에서 실제 프로그램 카운터(Program Counter)가 움직인 시간을 합산한 것이 $T_{busy}$이며, 이것이 전체 시간에서 차지하는 비중이 바로 **CPU 이용률**입니다.
3.  **처리량 발생점**: 프로세스가 `Running` -> `Terminated` 상태로 넘어가는 지점이 바로 **처리량(Throughput)**이 카운트되는 순간입니다. 이 그래프가 평탄할수록(지속적으로 Terminated로 감) 처리량이 높은 것입니다.

#### 4. 심층 동작 원리 및 핵심 알고리즘
CPU 이용률과 처리량을 최적화하기 위해 현대 OS는 다음과 같은 단계를 거칩니다.
1.  **탐지 (Detection)**: **APIC (Advanced Programmable Interrupt Controller)** 타이머 인터럽트 발생.
2.  **판단 (Decision)**: 현재 프로세스의 Time Slice가 소진되었는지, 혹은 I/O로 Block 되었는지 확인.
3.  **선점 (Preemption)**: 현재 프로세스의 **PCB (Process Control Block)**에 레지스터 상태를 저장(Context Save).
4.  **스케줄링 (Scheduling)**: Ready Queue에서 다음 우선순위 프로세스 선출.
5.  **디스패칭 (Dispatching)**: 새 프로세스의 PCB 정보를 레지스터에 로드(Context Restore)하고 실행 모드 전환.

이때 `③→④→⑤` 과정(Context Switch) 자체도 CPU를 사용하므로, 지나친 빈번한 스위칭은 오히려 이용률을 높이는 데 기여하지만, **실제 사용자 작업을 처리하는 비율(User Effective Utilization)**은 낮출 수 있습니다.

```c
// Pseudo-code: CPU Utilization Calculation in Kernel
unsigned long total_ticks = 0;
unsigned long idle_ticks = 0;

void timer_interrupt_handler() {
    total_ticks++;
    if (current_process == IDLE_PROCESS) {
        idle_ticks++;
    }
    // Trigger Scheduler if time quantum expired
    schedule();
}

double get_cpu_utilization() {
    return (1.0 - ((double)idle_ticks / total_ticks)) * 100.0;
}
```

**📢 섹션 요약 비유: 피자 가게 주방 라인**
CPU는 피자 굽는 오븐이자 요리사입니다. 이용률을 높이려면 요리사가 도을 깎거나 청소하는 동안(Idling) 다른 주문을 받아서 채워야 합니다. 하지만 무조건 주문만 받아대면(Ready Queue 길어짐) 주방이 혼잡해져 오히려 피자 구워 나가는 속도(처리량)가 느려집니다. 재료를 손질하는 시간(I/O)과 굽는 시간(CPU Burst)이 섞인 주문들을 잘 섞어서 오븐이 돌아가는 시간을 채우는 것이 핵심입니다.**

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 심층 기술 비교: Utilization vs. Throughput vs. Turnaround Time

| 구분 | CPU 이용률 (Utilization) | 처리량 (Throughput) | 반환 시간 (Turnaround Time) |
|:---:|:---|:---|:---|
| **정의** | 자원의 활용 비율 (%) | 단위 시간당 작업 완료 건수 | 프로세스 생성부터 종료까지 총 시간 |
| **수식** | $Busy / (Busy + Idle)$ | $Completed / Time$ | $Completion - Arrival$ |
| **관점** | **제공자 (Provider)** <br> (자원 효율, 비용) | **공급자/사용자 (System/User)** <br> (성과량) | **사용자 (Customer)** <br> (대기 시간 포함 경험) |
| **최적화 전략** | Time-sharing (I/O 시간 활용) | Batch Processing (단위 작업 최소화) | Shortest Job First (SJF) |
| **Trade-off** | 너무 높으면 응답 시간 악화 | 너무 높으면 품질(QoS) 저하 가능성 | 최소화하려면 이용률 희생 필요 |

#### 2. 타 과목 융합 분석

**1) 컴퓨터 아키텍처 (Computer Architecture) - 파이프라이닝 (Pipelining) & 캐시 (Cache)