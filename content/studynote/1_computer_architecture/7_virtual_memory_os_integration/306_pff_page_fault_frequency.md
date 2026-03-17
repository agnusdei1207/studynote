+++
title = "PFF (Page Fault Frequency)"
date = "2026-03-14"
weight = 306
+++

# # PFF (Page Fault Frequency) 기술 백서

#### 핵심 인사이트 (3줄 요약)
> 1.  **본질**: 다중 프로그래밍 환경에서 프로세스의 **페이지 부재 빈도(Page Fault Frequency, PFF)** 를 실시간 모니터링하여, 물리 메모리 프레임(Frame) 할당량을 동적으로 조절하는 피드백 제어 알고리즘이다.
> 2.  **가치**: **스래싱(Thrashing)** 발생 시 프레임을 추가 할당하여 CPU 이용률을 급격히 회복시키고, 유휴 자원은 즉시 회수하여 메모리 낭비를 방지하는 시스템 안정화 기술이다.
> 3.  **융합**: 가상 메모리 관리자와 **중기 스케줄러(Medium-term Scheduler)** 가 연동하여 다중 프로그래밍 정도(Degree of Multiprogramming)를 자동으로 조절하는 선제적 자원 관리의 핵심이다.

---

### Ⅰ. 개요 (Context & Background)

**PFF (Page Fault Frequency)** 는 가변 분할(Variable Partitioning) 및 가상 메모리(Virtual Memory) 환경에서, 각 프로세스에 할당된 물리 메모리의 양이 적절한지를 판단하는 지표로서 **'페이지 폴트 발생 빈도'** 를 활용하는 기술이다.

컴퓨터 시스템의 메모리 관리 전략은 크게 '프로세스에게 프레임을 얼마나 줄 것인가'에 대한 할당(Allocation) 문제와 '프레임이 부족할 때 어떤 페이지를 내쫓을 것인가'에 대한 교체(Replacement) 문제로 나뉜다. 초기에는 모든 프로세스에 동일한 수의 프레임을 주는 **균등 할당(Equal Allocation)** 방식이나, 프로세스 크기에 비례하여 할당하는 **비례 할당(Proportional Allocation)** 방식이 사용되었다. 그러나 이러한 정적(Static) 할당 방식은 프로세스의 실행 단계(Phase)마다 필요로 하는 메모리 양(Locality)이 급격히 변한다는 사실을 반영하지 못했다.

프로세스에 필요한 최소한의 프레임 수보다 적게 할당되면, 페이지 교체(Page Replacement)가 빈번하게 발생하여 시스템은 디스크 I/O에만 매몰되고 실제 연산은 수행하지 못하는 **스래싱(Thrashing)** 상태에 빠진다. 반대로 메모리를 과도하게 많이 주면 다른 프로세스가 실행될 공간이 부족해져 다중 프로그래밍의 효율성이 떨어진다. PFF는 이러한 딜레마를 해결하기 위해, 페이지 폴트라는 명확한 하드웨어 인터럽트를 지표로 삼아 운영체제가 개입하는 시점을 결정하는 **동적 할당(Dynamic Allocation)** 정책의 대표주자다.

> 📢 **섹션 요약 비유**
> 전체 직원에게 사무실 책상을 무조건 똑같은 크기로 배치해주는 고정 계획经济 대신, 직원이 "자료가 없어서 자주 파일 Cabinet을 뒤져야 해요(페이지 폴트)"라고 호소하는 횟수를 체크하여, 불평이 잦으면 책상을 넓혀주고 조용하면 책상을 줄여주는 **'실시간 민원 기반 유연한 공간 관리'** 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

PFF 알고리즘은 두 개의 임계값(Threshold)인 **상한선(Upper Bound)** 과 **하한선(Lower Bound)** 을 기준으로 동작하는 부정 제어(Negative Feedback) 시스템이다. 운영체제 커널의 메모리 관리 부분은 주기적 혹은 인터럽트 기반으로 각 프로세스의 PFF를 계산하고, 이를 설정된 임계값과 비교하여 페이지 프레임의 할당量和을 조절한다.

#### 1. 구성 요소 및 상세 동작

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/수식 (Protocol) |
|:---|:---|:---|:---|
| **PFF Monitor** | 페이지 폴트 빈도 측정 | 각 페이지 폴트 발생 시점 간의 시간 간격($\Delta t$)을 측정하여 빈도($1/\Delta t$) 계산 | $PFF = \frac{\text{Number of Faults}}{\text{Time Unit}}$ |
| **Upper Bound** | 스래싱 감지 임계값 | PFF가 이 값 초과 시 **메모리 부족(Memory Starvation)** 간주 및 프레임 추가 | If $PFF > U_{bound}$ $\rightarrow$ **Allocate Frame** |
| **Lower Bound** | 메모리 낭비 감지 임계값 | PFF가 이 값 미만 시 **과잉 할당(Over-allocation)** 간주 및 프레임 회수 | If $PFF < L_{bound}$ $\rightarrow$ **Deallocate Frame** |
| **Free Frame Pool** | 가용 물리 메모리 공간 | 회수된 프레임 또는 새로 확보된 프레임을 보관하는 전역 공간 | Global LRU List or Buddy System |
| **Suspender (Swapper)** | 강제 프로세스 퇴거 | 가용 프레임이 없을 때 일부 프로세스를 **Swap-out** 시켜 공간 확보 | **Medium-Term Scheduler** Invocation |

#### 2. PFF 제어 루프 및 상태 천이 다이어그램

PFF 알고리즘은 시스템의 부하(Load)에 따라 프로세스의 상태를 동적으로 변화시킨다. 아래 다이어그램은 페이지 폴트율에 따른 운영체제의 개입 로직을 도식화한 것이다.

```text
+-----------------------------------------------------------------------+
|                   PFF (Page Fault Frequency) Control Loop             |
+-----------------------------------------------------------------------+

    Page Fault Rate (Faults / sec)
        ^
        |                                            [ DANGER ZONE ]
 Upper  | +------------------------------------------+  (Thrashing Imminent)
 Bound  | | Page Fault occurs too frequently (High Δ)|  => Action: ADD Frame
 (U)    +-+------------------------------------------+-------------------+
        | |                                          |                   |
        | |   [ SAFETY ZONE ]                        |   [ WASTE ZONE ]  |
        | |   Fault rate is acceptable               |   Process has too |
        | |   (Moderate Δ)                           |   much memory     |
        | |   => Action: NO OP                       |   (Low Δ)         |
        | |                                          |   => Action: REMOVE|
 Lower  +-+------------------------------------------+---Frame            |
 Bound  |                                          |                   |
 (L)    +------------------------------------------+-------------------+
        |
        +----------------------------------------------------------> Time

  [Process State Transition Diagram]

  (High PFF)           (Normal PFF)                 (Low PFF)
  High Overhead      Stable Execution           Low Overhead
+-----------+     +-------------+           +-------------+
|   NEED    |     |   STABLE    |           |   WASTE     |
|   MORE    | <-- |   STATE     | -------> |   MEMORY    |
|  MEMORY   |     |             |           |             |
+-----------+     +-------------+           +-------------+
      ^                 |                         |
      |                 |                         |
      |                 v                         v
 (Add Frames)    (Maintain Frames)         (Reclaim Frames)
```

**다이어그램 해설:**
1.  **상한선 초과 (Upper Bound Exceeded):** 페이지 폴트 발생 간격($\Delta t$)이 짧아져 전체 빈도가 상한선(U)을 넘어서면, 해당 프로세스는 고통 스레스하는 상태로 간주된다. 운영체제는 즉시 **Free Frame Pool**에서 프레임을 가져와 할당한다. 만약 풀이 비어있다면, 시스템 전체의 안정을 위해 다른 프로세스를 강제로 Sleep(Swap-out) 시키고 그 프레임을 뺏어온다.
2.  **하한선 미달 (Lower Bound Undershot):** 페이지 폴트가 매우 드물게 발생($\Delta t$가 길어짐)하면, 해당 프로세스가 현재 할당받은 프레임을 모두 사용하지 않고 있다는 뜻이다. 운영체제는 이를 낭비로 간주하여, 해당 프로세스의 페이지 중 가장 최근에 참조되지 않은 페이지(LRU 등)를 선정하여 물리 메모리에서 해제(Evict)시키고 Free Frame Pool로 반환한다.
3.  **허용 구간 (Acceptable Zone):** 하한선과 상한선 사이에 위치한 경우, 프로세스가 지역성(Locality) 집합을 적절히 유지하고 있다고 판단하여 개입하지 않는다.

#### 3. 핵심 알고리즘 및 의사결정 로직

다음은 PFF 알고리즘의 핵심 로직을 C 스타일 의사 코드(Pseudo-code)로 구현한 것이다.

```c
// PFF Algorithm Logic
#define UPPER_BOUND 100 // Faults per second threshold (High limit)
#define LOWER_BOUND 20  // Faults per second threshold (Low limit)

void pff_handler(Process* proc) {
    // Time difference since last page fault
    double time_diff = current_time() - proc->last_fault_time; 
    double current_pff = 1.0 / time_diff; 

    if (current_pff > UPPER_BOUND) {
        // CASE 1: Thrashing Risk detected
        if (free_frame_count > 0) {
            // Allocate a free frame to this process
            allocate_frame(proc);
        } else {
            // Critical: System-wide memory shortage
            // Invoke Medium-Term Scheduler to swap out a victim process
            swap_out_victim_process(); 
            allocate_frame(proc); // Grab the freed frame
        }
        log("Process %d: Frame Added (PFF=%.2f)", proc->id, current_pff);

    } else if (current_pff < LOWER_BOUND) {
        // CASE 2: Memory Wastage detected
        // Remove a frame from the process (Working Set reduction)
        page* victim = select_victim_page(proc); // e.g., LRU page
        free_frame(victim);
        log("Process %d: Frame Removed (PFF=%.2f)", proc->id, current_pff);

    } else {
        // CASE 3: Stable State - Do nothing
        proc->last_fault_time = current_time();
    }
}
```

> 📢 **섹션 요약 비유**
> 자동차의 **크루즈 컨트롤(Cruise Control)** 시스템과 유사합니다. 운전자(프로세스)가 설정 속도(적정 메모리)를 유지하도록, 속도가 너무 느려지면(페이지 폴트 증가) 엑셀(프레임 추가)을 밟고, 속도가 너무 빨라지면(메모리 낭비) 브레이크(프레임 회수)를 밟아 항상 최적의 주행 상태를 유지해주는 자동 조절 장치입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

PFF는 가변 할당 정책의 일종으로, 다른 메모리 관리 기법들과는 구조적, 철학적으로 차이가 있다. 특히 워킹 셋(Working Set) 모델과의 비교는 운영체제 이론에서 매우 중요하다.

#### 1. 심층 기술 비교표: PFF vs Working Set Model

| 비교 항목 (Criteria) | 워킹 셋 모델 (Working Set Model) | PFF 알고리즘 (Page Fault Freq.) |
|:---|:---|:---|
| **정의 (Definition)** | 과거 $\Delta$ 시간 동안 참조된 페이지들의 집합 ($W(t, \Delta)$) | 단위 시간당 발생한 페이지 폴트의 횟수 |
| **핵심 철학 (Philosophy)** | **"과거의 참조 패턴이 미래를 보장한다"** (Locality Principle) | **"현재의 고통(Pain) 지표가 자원 필요량을 대변한다"** |
| **구현 복잡도 (Complexity)** | **极高 (High)**: 매 메모리 참조마다 타임스탬프 갱신 필요 | **중간 (Medium)**: 페이지 폴트 발생 시에만 계산 |
| **오버헤드 (Overhead)** | Context Switch나 메모리 참조 시 막대한 소모 | 페이지 폴트 핸들러에서의 계산만 부과 |
| **반응 속도 (Response)** | 지역성 변화에 상당히 민감하게 반응함 | 지역성 변화에 다소 둔감하나(Heuristic), 안정적임 |
| **주요 용도 (Use Case)** | 이론적 모델링, 미래 예측 기반 스케줄링 | 실용적인 시스템 구현, 클라우드 오토스케일링 |

#### 2. 메모리 할당 전략 비교 다이어그램

```text
       [Memory Allocation Strategy Comparison]

  Fixed Allocation (Proportional)        Variable Allocation (PFF)
  +---------------------------+          +---------------------------+
  | Process A: [====]         |          | Process A: [==]      (+)   |
  | Process B: [======]       |   VS     | Process B: [========] (-)  |
  | Process C: [===]          |          | Process C: [=]       (+)   |
  +---------------------------+          +---------------------------+
        (Static Size)                        (Dynamic Sizing)

   Issue: Thrashing (B)                Solution: Auto-balancing
   Issue: Wastage (A, C)               Based on Fault Frequency
```

**해설:**
고정 할당(Fixed Allocation)은 프로세스의 메모리 요구량이 변해도 할당량을 바꾸지 않아, 프로세스 B가 스래싱에 빠져도 도와줄 수 없고 A, C는 메모리를 낭비한다. 반면 PFF 기반의 가변 할당은 B가 고통받으면(폴트 증가) 프레임을 몰아주고, A/C가 여유로우면 프레임을 회수하여 전체 효율을 높인다.

#### 3. 과목 융합 관점 (OS vs Network vs AI)
-   **OS (Operating System)**: PFF는 커널의 **페이저(Pager)** 와 **스와퍼(Swapper)** 를 연결하는 가교 역할을 한다.
-   **네트워크 (Network)**: TCP 혼잡 제어(Congestion Control)의 **AIMD (Additive Increase Multiplicative Decrease)** 기법과 논리적으로 동일하다. 패킷 손실(페이지 폴트)이 감지되면 윈도우 크기(할당 프레임)를 줄이는 피드백 루프 구조가 같다.
-   **AI (Machine Learning)**: 최신의 **강화 학습(Reinforcement Learning)** 기반 메모리 관리자는 PFF를 상태(State) 입력값으로 사용하여 더 정교한 스케줄링 정책을 학습한다.

> 📢 **섹션 요약 비유**
> 워킹 셋 모델이 학생의 10분 전 공부 기록을 들춰보며 "너는 지금 수학을 하고 있구나"라고 미리 예측하는 **예측형 튜터**라면, PFF는 학생이 틀리는 문제(페이지 폴트)가 나올 때마다 바로 체크하여 "너 지금 공부하려는 책이 부족한가 보네" 하고 바로 개입하는 **현장형 보조 교사**에 비유할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 시스템 설계 시 P