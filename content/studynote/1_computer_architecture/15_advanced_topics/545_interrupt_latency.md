+++
title = "545. 인터럽트 지연 시간 (Interrupt Latency) 최소화"
date = "2026-03-14"
weight = 545
+++

# 545. 인터럽트 지연 시간 (Interrupt Latency) 최소화

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인터럽트 지연 시간(Latency)은 외부 하드웨어 이벤트 발생 시점부터 CPU (Central Processing Unit)가 해당 이벤트를 처리하는 ISR (Interrupt Service Routine)의 첫 명령어를 실행할 때까지의 시간 간격을 의미하며, 이를 최소화하는 것은 시스템의 실시간성을 결정짓는 핵심 아키텍처 과제다.
> 2. **가치**: 자율주행, 산업용 제어 시스템, 의료기기 등 Hard Real-time 시스템에서 마이크로초(µs) 단위의 지연 최적화는 시스템의 안전성과 신뢰성을 직접적으로 보장하는 결정적인 성능 지표(KPI)로 작용한다.
> 3. **융합**: 하드웨어적인 NVIC (Nested Vectored Interrupt Controller)의 Tail-chaining 기법과 소프트웨어적인 Critical Section 최소화, 메모리 아키텍처(TCM 활용)가 융합되어 지연을 나노초(ns) 단위로 절감하는 최적화 생태계를 구축한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의 및 철학**
인터럽트 지연 시간(Interrupt Latency)이란 단순한 '대기 시간'이 아니라, 시스템이 외부 비동기 이벤트에 반응하는 **'민감도(Sensitivity)'**의 척도이다. 이는 `Interrupt Request (IRQ)` 신호가 Assertion 된 시점($t_0$)부터, CPU가 현재 명령어 파이프라인을 정리(Pipeline Flush)하고 Context를 Stack에 저장한 뒤, ISR의 주소로 점프하여 첫 명령어를 Fetch 하는 시점($t_1$)까지의 총 시간($\Delta t = t_1 - t_0$)으로 정의된다.
일반적으로 이 지연 시간은 $L_{max} = L_{hw} + L_{sw}$ 로 표현된다.
- $L_{hw}$ (Hardware Latency): 신호 동기화, 파이프라인 플러시, 벡터 주소 계산에 소요되는 고정 클럭.
- $L_{sw}$ (Software Latency): OS 커널이 인터럽트를 마스크(Mask)해둔 임계 구간(Critical Section) 내에서 대기하는 시간으로서, 최악의 경우(Worst Case Execution Time, WCET)를 기준으로 설계해야 한다.

**💡 직관적 이해를 위한 비유**
고속도로에서 주행 중인 레이싱 카(CPU)가 갑자기 발생한 돌발 상황(Interrupt)을 마주한 상황과 유사하다. 운전자가 상황을 인지하고, 브레이크를 밟고, 핸들을 조작하는 반응 속도가 늦으면 사고가 난다. **인터럽트 지연 최소화**란, 레이싱 카의 브레이크 시스템을 전자 제어로 바꾸고, 운전자의 반사 신경을 AI로 보완하여 돌발 상황 인지부터 제동까지의 틈을 0에 수렴하게 만드는 '자율 주행 기술'의 구현과 같다.

**등장 배경 및 기술적 패러다임 변화**
1. **초기 컴퓨팅 (Polling 방식)**: CPU가 주기적으로 장치의 상태를 물어보는 방식이었으나, 빈번한 폴링(Polling)으로 인한 리소스 낭비가 심각했다.
2. **인터럽트 기반 처리 도입**: 이벤트 중심(Event-driven)의 전환으로 유휴(Idle) 상태를 제거했으나, 멀티태스킹 환경에서 'Context Switching' 비용이 새로운 병목으로 떠올랐다.
3. **실시간성의 요청 (RTOS 시대)**: GPOS (General Purpose OS)의 'Throughput' 중심 철학에서 벗어나, RTOS (Real-Time OS)의 'Determinism(확정성)' 중심 철학으로 전환되며 인터럽트 지연 시간은 시스템 안전의 필수 요소가 되었다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                   [Interrupt Latency Decomposition]                 │
│                                                                     │
│  External Event                                                     │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────┐    ① Sync & Pipeline Flush                         │
│  │   Signal    │───────────────────────────────────┐                │
│  │   Detect    │                                    ▼                │
│  └─────────────┐    ② Interrupt Disable Wait       │                │
│                 │   (Software Latency Max)         │                │
│                 │   <-- [Critical Section] ────────┤                │
│                 │                                  │                │
│                 │                                  ▼                │
│                 │    ③ Context Save (Stack PUSH)   │                │
│                 │   (Registers: PC, CPSR, etc.)    │                │
│                 │                                  │                │
│                 ▼                                  │                │
│  ┌─────────────┐    ④ Vector Table Fetch          │                │
│  │    Jump     │───────────────────────────────────┘                │
│  │    to ISR   │                                                     │
│  └─────────────┘    ⑤ Fetch First Instruction                       │
│         ▲                                                           │
│         │                                                           │
└─────────│───────────────────────────────────────────────────────────┘
          │
          │ Total Latency (t1 - t0)
```
**[다이어그램 해설]**
위 다이어그램은 인터럽트 지연 시간을 구성하는 5가지 단계를 시계열로 도식화한 것이다.
- **① Sync & Flush**: 하드웨어적으로 신호를 안정화하고, 파이프라인 내의 명령어를 취소하는 단계로서, 일반적으로 수 클럭이 소요된다.
- **② Disable Wait**: 가장 변동성이 큰 구간이다. 소프트웨어가 `cli` (Clear Interrupt) 명령어로 인터럽트를 막고 있는 '임계 구간'에 진입해 있다면, 이 구간이 끝날 때까지 CPU는 인터럽트를 처리하지 못하고 기다려야 한다. 이 시간은 소프트웨어 설계에 따라 수십 나노초에서 수 밀리초까지 널뛸 수 있어 최적화의 핵심 타겟이 된다.
- **③~④ Context & Vector**: 레지스터를 저장하고 벡터 테이블을 참조하는 과정은 하드웨어 아키텍처에 의해 결정되며, 현대 MCU는 이 과정을 하드웨어적으로 가속화하여 오버헤드를 줄인다.

> **📢 섹션 요약 비유**: "화재 경보가 울렸을 때, 소방관(CPU)이 자신이 하던 일을 멈추고 장비를 갖춰 출동할 때까지의 시간이 곧 인터럽트 지연 시간입니다. 만약 소방관이 '안전 모두 규정'을 읽고 있는(Critical Section) 중이라면, 그 규정을 다 읽을 때까지 출동을 미뤄야 하므로 골든타임을 놓치게 됩니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (지연 시간의 3대 요인)**
인터럽트 지연 시간 최소화를 위해서는 하드웨어와 소프트웨어의 이해가 필수적이다.

| 요소 | 구분 | 상세 동작 메커니즘 (Internal Mechanism) | 비유 |
|:---:|:---:|:---|:---|
| **Interrupt Masking** | SW | OS가 데이터 무결성을 보장하기 위해 `spin_lock`이나 `cli` 명령어로 인터럽트를 차단하는 구간. 이 구간의 길이가 곧 최대 지연 시간($L_{max}$)을 결정함. | 전화기를 끄고 중요한 회의 중인 시간 |
| **Context Switching** | HW/SW | 현재 프로그램 카운터(PC), 범용 레지스터, 상태 레지스터(CPSR) 등을 메모리(Stack)에 저장(PUSH)하고 복원(POP)하는 과정. 메모리 접근 속도에 의존적임. | 게임 중간에 세이브하고 로딩하는 시간 |
| **Interrupt Controller** | HW | 여러 인터럽트 요청을 우선순위(Priority)에 따라 중재(Arbitration)하고, CPU에 단일 인터럽트 요청(IRQ)을 전달하는 로직. NVIC, GIC 등이 해당됨. | 회사 비서가 전화를 걸러온 순서대로 연결 |

**하드웨어 최적화 아키텍처: ARM NVIC (Nested Vectored Interrupt Controller)**
ARM Cortex-M 시리즈는 인터럽트 지연 최소화를 위해 하드웨어적인 자동화 기능을 도입했다. 이를 통해 소프트웨어의 개입 없이 클럭 단위의 처리가 가능하다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                  [Optimization: Tail-Chaining Process]              │
│                                                                     │
│   Scenario: Interrupt A (Lower Priority) is finishing.             │
│             Interrupt B (Higher Priority) is pending.               │
│                                                                     │
│  ┌─────────────────┐                                               │
│  │  MAIN PROGRAM   │                                               │
│  └────────┬────────┘                                               │
│           │                                                         │
│           │ 1. HW Auto Context Save (R0~R3, R12, LR, PC, xPSR)      │
│           ▼                                                         │
│  ┌─────────────────┐                                               │
│  │  ISR A RUNNING  │ (Handling Interrupt...)                       │
│  └────────┬────────┘                                               │
│           │                                                         │
│           │ [Event: ISR A finished]                                 │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                               │
│  │  CONVENTIONAL   │  [1] POP Context (Stack Restore)              │
│  │  PROCESSING     │  [2] Check Pending Interrupts                 │
│  │  (Slow Path)    │  [3] PUSH Context (for Interrupt B)           │
│  │                 │  [4] Jump to ISR B                             │
│  └─────────────────┘  >>> Total Overhead: PUSH + POP (2x Cost)     │
│                                                                     │
│ ────────────────────────────────────────────────────────────────── │
│                                                                     │
│  ┌─────────────────┐                                               │
│  │    ARM NVIC     │                                               │
│  │  TAIL-CHAINING  │                                               │
│  │   (Fast Path)   │                                               │
│  └────────┬────────┘                                               │
│           │                                                         │
│           │ [Event: ISR A finished, B is pending]                   │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                               │
│  │  OPTIMIZED HW   │  [1] Skip POP (Stack stays intact)            │
│  │     ACTION      │  [2] Skip PUSH (Reuse Stack frame)            │
│  │                 │  [3] Fetch Vector B directly                  │
│  │                 │  [4] Jump to ISR B                             │
│  └─────────────────┘  >>> Total Overhead: ~6 cycles only           │
│                                                                     │
│   Result: Eliminates redundant memory access, drastically reducing  │
│           the "gap" between interrupts.                             │
└─────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]**
이 다이어그램은 ARM 아키텍처의 핵심 최적화 기능인 **Tail-Chaining(꼬리 물기)**과 **Late-Arrival(늦은 도착)** 처리를 보여준다.
1.  **문제점**: 기존 방식(Conventional)에서는 ISR A가 끝나면 원래 실행 흐름(Main)으로 복귀해야 한다. 따라서 스택에서 레지스터를 복원(POP)해야 한다. 그런데 복귀 직후에 대기 중이던 ISR B가 있음을 확인하고, 다시 ISR B를 위해 레지스터를 저장(PUSH)해야 한다. 이중으로 스택을 접근하는 비효율이 발생한다.
2.  **솔루션**: NVIC는 ISR A가 종료되는 시점에 보류 중인 인터럽트(B)가 있음을 하드웨어적으로 감지한다. 그런 즉시, 메인 루프로 복귀하는 과정(POP)과 인터럽트 진입 과정(PUSH)을 생략하고, 스택 프레임을 그대로 둔 채로 PC(Program Counter)만 ISR B의 주소로 변경하여 뛰어든다. 이로 인해 발생하는 오버헤드는 단 6 클럭 사이클 수준으로 줄어들며, 인터럽트 간 간격(Interrupt Gap)이 사실상 사라진다.

**소프트웨어적 심층 최적화 기술**
하드웨어가 아무리 좋아도 소프트웨어가 인터럽트를 마스크(Masking)해버리면 지연 시간은 폭증한다.
```c
/* [안티패턴] 긴 Critical Section (지연 시간 악화) */
void bad_critical_section() {
    cli(); // 인터럽트 비활성화 (Clear Interrupt)
    
    // 매우 긴 계산 수행 (최악의 경우 수십 ms 소요)
    for(int i=0; i<1000000; i++) { 
        complex_calculation(); 
    }
    
    sti(); // 인터럽트 활성화
}

/* [최적화 패턴] OS Lock 및 세분화 */
void optimized_critical_section() {
    // 1. 인터럽트 전체가 아닌, 해당 스피락만 획득 (Spinlock)
    // 2. 최악의 실행 시간(WCET)이 1µs 이내인 코드만 락 내부에 배치
    // 3. Preemptible Kernel (선점형 커널) 기반 설계
    spin_lock(&my_lock);
    
    fast_register_update(); // 핵심 연산만 수행
    
    spin_unlock(&my_lock);
}
```
코드 레벨에서는 `cli`/`sti` 대신 `spin_lock_t`와 같은 세밀한 락(Lock) 메커니즘을 사용하여 인터럽트 비활성화 구간을 **시스템 틱(System Tick)의 1/10 수준(예: 10µs)** 이내로 억제하는 것이 필수적이다.

> **📢 섹션 요약 비유**: "주차장 톨게이트(인터럽트 처리)에서 차가 나갈 때 마다 바리케이드를 올렸다 내렸다(Context Saving/Restoring) 하면 굉장히 느립니다. 하이패스 차로(Tail-chaining)를 만들어, 바리케이드 조작 없이 텅 빈 차가 있으면 바로 통과시켜버리면 대기 시간이 사라지는 원리입니다."

---

### Ⅲ. 융합 비교 및 다각도 분석

**심층 기술 비교: GPOS vs RTOS**

| 비교 항목 | GPOS (General Purpose OS) <br> *예: Windows, Linux (Standard)* | RTOS (Real-Time OS) <br> *예: