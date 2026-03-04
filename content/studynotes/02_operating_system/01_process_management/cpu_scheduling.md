+++
title = "CPU 스케줄링 (CPU Scheduling)"
description = "운영체제의 핵심 기능인 CPU 스케줄링의 근본 원리, 다양한 알고리즘(FCFS, SJF, SRT, Round Robin, Multilevel Queue)과 선점/비선점 방식의 기술적 차이를 심도 있게 분석합니다."
date = 2024-05-20
[taxonomies]
tags = ["OS", "Process Management", "CPU Scheduling", "Context Switching", "Priority"]
+++

# CPU 스케줄링 (CPU Scheduling)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU 스케줄링은 다중 프로그래밍 환경에서 CPU 이용률을 극대화하기 위해 Ready Queue에 대기 중인 프로세스들 사이에서 CPU 할당 순서를 결정하는 OS 커널의 핵심 자원 관리 메커니즘입니다.
> 2. **가치**: 공정성(Fairness), 효율성(Efficiency), 응답 시간(Response Time)의 최적 균형을 통해 시스템의 전체 처리량(Throughput)을 높이고 사용자 체감 지연을 최소화하여 비즈니스 서비스의 안정성을 보장합니다.
> 3. **융합**: 현대의 스케줄링은 단순 단일 코어를 넘어 멀티코어 부하 분산(Load Balancing), 가상화 환경의 vCPU 스케줄링, 그리고 컨테이너 기반의 오케스트레이션(Kubernetes Scheduler) 등 클라우드 인프라 전반의 최적화 기술로 확장되고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

**개념**  
CPU 스케줄링(CPU Scheduling)이란, 운영체제의 커널 내부에 존재하는 스케줄러(Scheduler)가 Ready 상태에 있는 여러 프로세스 중 어느 프로세스에게 CPU를 할당할 것인지를 결정하는 의사결정 과정입니다. 이는 프로세스의 생명 주기 중 'Running' 상태로의 전이를 통제하며, 프로세스가 I/O 요청 등으로 인해 대기 상태(Wait)로 들어가거나 타이머 인터럽트에 의해 할당 시간(Time Quantum)이 만료될 때 발생합니다. 스케줄링의 궁극적인 목표는 CPU가 단 1ms도 쉬지 않고 유익한 작업을 수행하도록 하여 자원 활용도를 극대화하는 데 있습니다.

**💡 비유: 대형병원의 응급실 트리아지(Triage) 시스템**  
CPU를 응급실의 한정된 '수술실'과 '의사'라고 한다면, 프로세스는 '환자'입니다. 모든 환자가 먼저 온 순서대로 수술을 받는다면(FCFS), 가벼운 찰과상 환자가 수술실을 차지하는 동안 심장마비 환자가 사망할 수 있습니다. 따라서 병원은 환자의 위급도(우선순위), 수술 예상 시간(SJF), 환자의 상태 변화(선점형) 등을 고려하여 수술 순서를 끊임없이 재조정합니다. 스케줄러는 바로 이 응급실의 '수석 간호사' 역할을 수행하며, 전체 환자의 생존율(시스템 처리량)을 높이고 대기 시간(Waiting Time)을 최소화하기 위해 정교한 알고리즘에 따라 환자를 배치합니다.

**등장 배경 및 발전 과정**  
1. **기존 기술의 치명적 한계점**: 초기의 일괄 처리(Batch Processing) 시스템에서는 한 번에 하나의 작업만 수행되었으므로 스케줄링의 필요성이 낮았습니다. 그러나 프로세스가 I/O 작업을 수행하는 동안 CPU가 아무 일도 하지 않고 기다리는 '유휴 상태(Idle)'가 발생하여 값비싼 메인프레임 자원이 낭비되는 치명적인 효율성 문제가 대두되었습니다.
2. **혁신적 패러다임 변화**: 시분할 시스템(Time-Sharing System)의 등장과 함께, CPU를 아주 짧은 시간 단위로 쪼개어 여러 프로세스에게 번갈아 할당하는 '라운드 로빈(Round Robin)' 개념이 도입되었습니다. 이는 여러 사용자가 마치 자신만이 컴퓨터를 독점하고 있는 것과 같은 응답성(Responsiveness)을 제공하는 혁신을 일으켰습니다. 이후 대화형 시스템, 실시간 시스템(RTOS) 등 사용 목적에 따라 우선순위 스케줄링, 다단계 피드백 큐(MLFQ) 등 복잡한 알고리즘으로 진화해 왔습니다.
3. **비즈니스적 요구사항**: 현대의 클라우드 컴퓨팅과 마이크로서비스(MSA) 환경에서는 수만 개의 컨테이너가 CPU 자원을 경쟁합니다. 서비스 레벨 협약(SLA)을 준수하기 위해 특정 서비스에 CPU 할당량을 보장(CPU Limit/Request)하거나, 대규모 데이터 처리 시 처리량 중심의 스케줄링을 수행하는 등 비즈니스 로직과 결합된 고도의 자원 격리 및 할당 기술이 강제되고 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CPU 스케줄링은 하드웨어 인터럽트, 커널 자료구조, 그리고 정교한 알고리즘이 결합된 시스템의 엔진입니다.

**구성 요소 (OS 스케줄링 시스템)**

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 데이터 구조 | 비유 |
|---|---|---|---|---|
| **Short-term Scheduler (Dispatcher)** | Ready Queue에서 프로세스를 선택하여 실제 CPU를 할당 | 컨텍스트 스위칭을 수행하고 사용자 모드로 전환하여 실행 시작 | Ready Queue, PCB (Process Control Block) | 수술실로 환자를 밀고 들어가는 이송 요원 |
| **Ready Queue** | CPU 할당을 기다리는 Ready 상태의 프로세스들의 대기소 | 알고리즘에 따라 Linked List, Priority Queue, Red-Black Tree 등으로 구현 | `struct task_struct` (Linux) | 수술실 앞 대기 의자 |
| **Gantt Chart** | 프로세스별 CPU 할당 시간과 순서를 시각화하여 분석하는 도구 | 알고리즘의 성능(평균 대기 시간, 반환 시간)을 평가하는 척도 | 시간 축 기반의 타임라인 데이터 | 응급실 환자 배치 현황판 |
| **Context Switcher** | 실행 중인 프로세스의 상태를 저장하고 새 프로세스의 상태를 복원 | CPU 레지스터, 프로그램 카운터(PC), 스택 포인터 등을 PCB에 저장/로드 | 하드웨어 레지스터 세트, 커널 스택 | 의사가 환자를 바꿀 때 차트를 교체하고 손을 씻는 과정 |
| **Timer Interrupt** | 특정 시간(Time Quantum)이 지나면 CPU 권한을 강제로 커널로 회수 | 하드웨어 타이머가 주기적으로 인터럽트를 발생시켜 스케줄러 호출 | Programmable Interval Timer (PIT) | 수술실 사용 시간이 다 됐음을 알리는 알람 벨 |

**정교한 구조 다이어그램 (스케줄링 전이 및 데이터 흐름)**

```ascii
========================================================================================
[ 사용자 영역 (User Space) ]          [ 커널 영역 (Kernel Space) ]
========================================================================================
                                          │
    (1) New Process                       │ (2) Admitted
         │                                ▼
         │                      ┌──────────────────────┐
         └─────────────────────▶│    Ready Queue       │◀──────┐
                                └──────────────────────┘       │
                                          │                    │
                                          │ (3) Scheduler      │ (4) Time Quantum Expired
                                          │     Dispatch       │     (Preemption)
                                          ▼                    │
    ┌──────────────────────┐    ┌──────────────────────┐       │
    │   Waiting Queue      │◀───┤   Running (CPU)      │───────┘
    └──────────────────────┘    └──────────────────────┘
         ▲           │                    │
         │           └────────────────────┼────────────────────▶ (5) Exit / Terminated
         │      I/O or Event Wait         │
         └────────────────────────────────┘
                 I/O or Event Completion

[내부 동작 핵심]:
- Dispatcher는 Ready Queue에서 PCB를 꺼내 CPU의 PC(Program Counter)를 해당 프로세스의 코드로 점프시킴.
- 선점형(Preemptive) 스케줄링의 경우, Timer Interrupt가 (4)번 경로를 강제하여 CPU를 회수함.
========================================================================================
```

**심층 동작 원리 (Scheduling Decision Pipeline)**
① **스케줄링 이벤트 발생**: 실행 중인 프로세스가 I/O를 요청하거나(Wait), 할당된 시간이 만료되거나(Interrupt), 자식 프로세스를 생성하거나, 종료될 때 커널의 `schedule()` 함수가 호출됩니다.
② **상태 저장 (Context Save)**: 현재 CPU 레지스터 값(EAX, EBX, PC, SP 등)을 현재 실행 중인 프로세스의 PCB 내 `thread_struct`에 저장합니다.
③ **다음 프로세스 선택 (Selection)**: Ready Queue의 자료구조를 탐색합니다. Linux의 경우 Red-Black Tree 기반의 CFS(Completely Fair Scheduler)를 사용하여 가장 적게 실행된(vruntime이 낮은) 프로세스를 O(log N) 시간에 찾아냅니다.
④ **상태 복원 (Context Restore)**: 선택된 프로세스의 PCB에서 이전에 저장된 레지스터 값들을 CPU 하드웨어로 로드합니다. MMU(Memory Management Unit)의 페이지 테이블 베이스 레지스터(CR3)도 새 프로세스의 주소 공간으로 교체됩니다.
⑤ **사용자 모드 복귀 (Mode Switch)**: 특권 레지스터를 조작하여 커널 모드에서 사용자 모드로 전환하고, 저장되어 있던 PC(Program Counter) 값으로 점프하여 프로세스 실행을 재개합니다.

**핵심 알고리즘 실무 예시: Round Robin (RR) 스케줄러 시뮬레이션**
현대적인 시분할 시스템의 기초가 되는 RR 알고리즘을 파이썬으로 정교하게 모델링합니다.

```python
from collections import deque

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0

def round_robin_scheduling(processes, time_quantum):
    """
    Round Robin 스케줄링 시뮬레이터
    - 선점형 방식, 동일한 Time Quantum 할당
    """
    current_time = 0
    ready_queue = deque()
    completed_processes = []
    
    # 도착 시간 순으로 정렬
    processes.sort(key=lambda x: x.arrival_time)
    
    idx = 0
    while len(completed_processes) < len(processes):
        # 1. 현재 시간에 도착한 모든 프로세스를 Ready Queue에 삽입
        while idx < len(processes) and processes[idx].arrival_time <= current_time:
            ready_queue.append(processes[idx])
            idx += 1
            
        if not ready_queue:
            current_time += 1
            continue
            
        # 2. Queue에서 프로세스 꺼내기 (Dispatch)
        p = ready_queue.popleft()
        
        # 3. Time Quantum 또는 남은 시간 중 최소값만큼 실행
        execution_time = min(p.remaining_time, time_quantum)
        p.remaining_time -= execution_time
        current_time += execution_time
        
        # 4. 실행 도중 도착한 프로세스들을 먼저 Queue에 넣음 (공정성 유지)
        while idx < len(processes) and processes[idx].arrival_time <= current_time:
            ready_queue.append(processes[idx])
            idx += 1
            
        # 5. 프로세스가 남았다면 다시 Queue 끝으로 (Preemption)
        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed_processes.append(p)
            
    return completed_processes

# [실무 시나리오]
# P1(0초 도착, 5초 실행), P2(1초 도착, 3초 실행), P3(2초 도착, 1초 실행), Time Quantum = 2초
proc_list = [Process("P1", 0, 5), Process("P2", 1, 3), Process("P3", 2, 1)]
results = round_robin_scheduling(proc_list, 2)

print(f"{'Name':<5} | {'Wait':<5} | {'Turnaround':<10}")
for p in sorted(results, key=lambda x: x.name):
    print(f"{p.name:<5} | {p.waiting_time:<5} | {p.turnaround_time:<10}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: 주요 스케줄링 알고리즘 다각도 평가 매트릭스**

| 알고리즘 | 방식 | 선택 기준 | 장점 | 단점 (병목/이슈) | 주요 지표 (Avg Wait) |
|---|---|---|---|---|---|
| **FCFS** | 비선점 | 도착 순서 | 구현이 단순, 오버헤드 적음 | **Convoy Effect**: 긴 작업이 CPU 점유 시 짧은 작업 대기 폭증 | 매우 높음 |
| **SJF (Shortest Job First)** | 비선점 | CPU Burst 시간 짧은 순 | 평균 대기 시간 최소화 (수학적 증명) | **Starvation**: 긴 작업은 영원히 할당 못 받을 수 있음 | 가장 낮음 |
| **SRT (Shortest Remaining Time)** | 선점 | 남은 실행 시간 짧은 순 | SJF의 선점 버전, 응답성 향상 | 새로운 프로세스 도착 시마다 재스케줄링 오버헤드 | 매우 낮음 |
| **Round Robin** | 선점 | 할당 시간(Time Quantum) 만료 | 모든 프로세스에게 공평한 기회, 대화형 시스템에 최적 | Time Quantum이 너무 크면 FCFS와 같고, 너무 작으면 **Context Switch 오버헤드** 심각 | 중간 |
| **Priority Scheduling** | 둘 다 가능 | 우선순위 (내부/외부 정적/동적) | 중요 작업 우선 처리 (RTOS 필수) | **Indefinite Blocking**: 낮은 순위 프로세스의 무한 지연 | 중간 |
| **MLFQ (Multilevel Feedback Queue)** | 선점 | 실행 패턴 (I/O vs CPU bound) | 프로세스 특성에 따라 동적으로 우선순위 조정 (현대 OS 표준) | 설계 및 구현의 복잡성 극심 (Queue 개수, 피드백 규칙 등) | 낮음 |

**과목 융합 관점 분석 (OS × Architecture × Distributed System)**
1. **OS × Architecture (멀티코어 및 캐시 친화성)**: 현대의 스케줄러는 단순히 Ready Queue만 관리하지 않습니다. 특정 프로세스가 실행되던 코어에서 계속 실행되도록 유도하는 **'프로세서 친화성(Processor Affinity)'**을 고려합니다. 이는 L1/L2 캐시의 Hit Rate를 높여 성능을 극대화하기 위함입니다. 또한 코어 간 부하가 불균형할 때 수행하는 **'부하 분산(Load Balancing)'** 알고리즘(Push/Pull Migration)은 컴퓨터 구조론의 NUMA(Non-Uniform Memory Access) 구조와 긴밀하게 연계됩니다.
2. **OS × Distributed System (쿠버네티스 스케줄링)**: 클라우드 환경에서 쿠버네티스 스케줄러는 개별 OS의 스케줄링 개념을 노드(Node) 단위로 확장합니다. 특정 노드에 Pod(프로세스 집합)을 배치할 때, 자원 요구사항(Request/Limit), 노드 어피니티(Affinity), 테인트와 톨러레이션(Taints/Tolerations) 등을 고려합니다. 이는 단일 OS의 우선순위 스케줄링이 클라우드 규모의 자원 오케스트레이션으로 진화한 형태입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**기술사적 판단 (실무 시나리오)**
- **시나리오 1: 실시간 금융 트레이딩 시스템의 응답 지연 해결**
  - **문제 상황**: 주식 매매 체결 프로세스가 일반 로그 분석 프로세스에 밀려 수십 ms의 지연이 발생하며 큰 금전적 손실 유발.
  - **기술사적 의사결정**: 시스템을 **RTOS(Real-Time OS)** 기반으로 튜닝하거나, 리눅스 커널의 `SCHED_FIFO` 또는 `SCHED_RR` 실시간 스케줄링 정책을 매매 프로세스에 적용합니다. 또한 우선순위 역전(Priority Inversion) 방지를 위해 **우선순위 상속(Priority Inheritance) 프로토콜**을 활성화하여, 낮은 순위 프로세스가 락을 잡고 있어 높은 순위 프로세스가 대기하는 현상을 차단합니다.

- **시나리오 2: 대규모 웹 서버의 컨텍스트 스위칭 오버헤드 폭증**
  - **문제 상황**: 사용자가 급증하자 CPU 사용률은 100%인데 실제 비즈니스 처리량(TPS)은 바닥을 치는 현상 발생. 분석 결과 컨텍스트 스위칭 비용이 전체 CPU의 40%를 차지.
  - **기술사적 의사결정**: 프로세스/스레드 기반 모델에서 **이벤트 루프(Event-driven) 또는 코루틴(Coroutine) 기반 모델**로 아키텍처를 전환할 것을 권고합니다. 커널 스케줄러에 의존하지 않고 애플리케이션 레벨에서 실행 흐름을 제어하는 User-level 스케줄링(M:N Threading)을 통해 컨텍스트 스위칭 횟수를 획기적으로 줄여 처리량을 회복시킵니다.

**도입 시 고려사항 (체크리스트)**
- **기술적 고려사항 (Time Quantum 선정)**: 라운드 로빈에서 Time Quantum은 시스템 성격에 따라 신중히 결정해야 합니다. 대화형 웹 서버는 보통 10ms ~ 100ms 사이를 권장하며, 이를 넘어서면 사용자가 렉을 느끼고, 이보다 작으면 컨텍스트 스위칭 오버헤드가 CPU를 점유하게 됩니다.
- **운영적 고려사항 (Monitoring)**: `/proc/stat`이나 `vmstat` 명령어를 통해 초당 컨텍스트 스위치 횟수(cs)를 모니터링해야 합니다. 임계치를 초과할 경우 불필요한 스레드 풀(Thread Pool) 크기를 조정하거나 스케줄링 정책을 점검해야 합니다.
- **안티패턴 (Anti-patterns)**: CPU Bound 작업이 많은 시스템에서 과도하게 많은 우선순위 큐를 생성하는 것은 관리 오버헤드만 늘리는 안티패턴입니다. 또한 특정 프로세스에 과도하게 높은 우선순위를 부여하여 다른 프로세스들이 굶주리는(Starvation) 상태를 방치해서는 안 됩니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량적/정성적 기대효과**

| 지표 | 스케줄링 최적화 전 | 최적화 후 (MLFQ 및 Affinity 적용) | 개선 효과 |
|---|---|---|---|
| **평균 응답 시간 (Avg Response)** | 500ms | 50ms | **10배 향상 (사용자 경험 개선)** |
| **CPU 이용률 (Utilization)** | 60% (I/O 대기로 인한 유휴) | 95% 이상 | **자원 효율성 35% 증가** |
| **처리량 (Throughput)** | 1,000 TPS | 2,500 TPS | **서비스 수용량 150% 증대** |
| **캐시 히트율 (L2 Cache Hit)** | 70% | 85% | **하드웨어 성능 끌어올림** |

**미래 전망 및 진화 방향**
미래의 CPU 스케줄링은 하드웨어와 AI의 결합으로 진화할 것입니다. Intel의 Alder Lake와 같은 **Hybrid CPU 아키텍처(P-core와 E-core의 혼합)**에서는 프로세스의 특성을 실시간으로 파악하여 고성능 코어와 고효율 코어에 적절히 배분하는 하드웨어 가이드형 스케줄링이 핵심이 됩니다. 
또한 인공지능(AI)이 과거의 프로세스 실행 패턴을 학습하여 다음 CPU Burst 시간을 예측하고, 이를 바탕으로 최적의 알고리즘을 실시간으로 교체하는 **'자율 스케줄링(Autonomous Scheduling)'** 시스템이 도입될 전망입니다. 엣지 컴퓨팅(Edge Computing) 환경에서는 전력 소모를 최소화하면서 성능을 유지하는 **에너지 인지형 스케줄링(Energy-aware Scheduling)**이 표준으로 자리 잡을 것입니다.

**※ 참고 표준/가이드**
- **POSIX.1b (Real-time extensions)**: 실시간 스케줄링 인터페이스 표준.
- **IEEE 1003.1 (System Interfaces)**: 스케줄링 관련 API 정의.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [문맥 교환 (Context Switching)](@/studynotes/02_operating_system/01_process_management/_index.md): 스케줄링 결과에 따라 실제 CPU를 교체하는 저수준 메커니즘.
- [다단계 피드백 큐 (MLFQ)](@/studynotes/02_operating_system/01_process_management/_index.md): 현대 OS에서 가장 널리 쓰이는 동적 우선순위 스케줄링의 상세 구조.
- [우선순위 역전 (Priority Inversion)](@/studynotes/02_operating_system/01_process_management/_index.md): 스케줄링과 동기화 락이 얽혔을 때 발생하는 치명적 결함과 해결책.
- [기아 상태와 에이징 (Starvation & Aging)](@/studynotes/02_operating_system/01_process_management/_index.md): 스케줄링의 부작용인 불공평성을 해소하기 위한 기술적 보완책.
- [쿠버네티스 스케줄러](@/studynotes/02_operating_system/01_process_management/_index.md): OS 스케줄링 개념이 분산 환경으로 확장된 클라우드 네이티브 스케줄링.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **CPU 스케줄링이란?**: 학교 급식실에서 수많은 학생들이 줄을 서 있을 때, 배식 아주머니(운영체제)가 "누가 먼저 밥을 먹을지" 순서를 정해주는 규칙이에요.
2. **어떻게 정하나요?**: 빨리 먹고 공부해야 하는 학생을 먼저 보내주기도 하고(우선순위), 모든 학생에게 1분씩만 먹게 하고 다음 학생에게 넘겨주기도 하며(라운드 로빈) 공평하게 나누어줘요.
3. **왜 중요한가요?**: 순서를 엉터리로 정하면 어떤 학생은 배고파서 울고(기아 상태), 어떤 학생은 밥을 다 먹었는데도 식판을 안 치울 수 있기 때문에, 모두가 행복하고 빠르게 밥을 먹으려면 똑똑한 규칙이 필요하답니다!
