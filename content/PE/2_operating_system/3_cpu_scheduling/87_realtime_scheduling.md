+++
title = "87. Real-time 스케줄링 (Real-time Scheduling)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Real-time-Scheduling", "Rate-Monotonic", "EDF", "Deadline", "Priority-Inversion"]
draft = false
+++

# Real-time 스케줄링 (Real-time Scheduling)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Real-time 스케줄링은 **"작업(Task)의 Deadline(마감 시간)을 준수하는 것을 최우선으로 하는 스케줄링"**으로, **Hard Real-time(생명/재해 위험)**과 **Soft Real-time(성능 저하)**으로 구분된다.
> 2. **가치**: **Rate Monotonic(RM)**과 **Earliest Deadline First(EDF)**이 대표적이며, **RM**은 **주기(Period)**이 짧을수록 **높은 우선순위**를 부여하는 **정적 우선순위(Static Priority)** 방식이고, **EDF**는 **마감 시간**이 가장 이른 작업을 우선하는 **동적 우선순위(Dynamic Priority)** 방식이다.
> 3. **융합**: **RTOS(Real-Time OS)**의 **VxWorks**, **QNX**, **RT-Linux**에 구현되며, **Priority Inheritance(우선순위 상속)**으로 **Mars Pathfinder**의 Priority Inversion 문제를 해결하고, **자동차(ISO 26262)**, **항공우주(DO-178C)**, **의료기기(IEC 62304)**의 **Safety-critical System**에 필수적이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
Real-time 스케줄링은 **"작업이 Deadline을 준수하도록 CPU를 할당하는 스케줄링"**이다.

**Real-time의 정의**:
- **Correctness**: 기능적 정확성 + 시간적 정확성(Timing)
- **Deadline**: 작업이 완료되어야 하는 시간
- **Response Time**: 요청부터 응답까지의 시간

### 💡 비유
Real-time 스케줄링은 **"응급실"**과 같다.
- **Hard**: 심폐소생기 (늦으면 생명 위험)
- **Soft**: 웹 로딩 (늦으면 사용자 경험 저하)

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Real-time 스케줄링의 필요성                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

일반 스케줄링 (Throughput 중심):
    • 평균 응답 시간
    • 처리량 최대화
    • Deadline 보장 없음
         ↓
실시간 요구 등장 (1960년대):
    • Apollo Guidance Computer
    • 미사일, 항공기 제어
    • Deadline 필수
         ↓
Real-time 스케줄링 (1970년대):
    • Liu & Layland (1973): Rate Monotonic
    • EDF (Earliest Deadline First)
    • Utilization Bound 분석
         ↓
현대 RTOS (2000년대~):
    • VxWorks, QNX Neutrino
    • RT-Linux (PREEMPT_RT)
    • AUTOSAR (자동차)
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### Hard vs Soft Real-time

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Hard vs Soft Real-time                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Hard Real-time]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  정의: Deadline을 어겨나 Miss 시 치명적인 결과                                                   │
    │                                                                                         │
    │  예시:                                                                                   │
    │  • 심폐소생기 (Heartbeat: 1s, Deadline Miss → 생명 위험)                                     │
    │  │  자동차 에어백 (Brake: 100ms, Miss → 사고)                                             │
    │  │  항공기 플라이바이워 (Control: 10ms, Miss → 추락)                                      │
    │  │  발전소 터빈 (Shutdown: 10ms, Miss → 폭발)                                            │
    │                                                                                         │
    │  특징:                                                                                   │
    │  • Deadline Miss Rate: 0% (완전히 보장)                                                   │
    │  │  최악의 경우(Worst Case) 분석                                                           │
    │  │  Deterministic(결정론적) 보장                                                           │
    │  │  Safety-critical                                                                      │
    │                                                                                         │
    │  OS: VxWorks, QNX, RT-Linux PREEMPT_RT                                                   │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Soft Real-time]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  정의: Deadline을 어겨도 시스템은 계속 동작하지만 성능 저하                                       │
    │                                                                                         │
    │  예시:                                                                                   │
    │  • 멀티미디어 플레이어 (Frame: 33ms, Miss → 프레임 드롭, 재생 가능)                           │
    │  │  웹 브라우저 (Page Load: 3s, Miss → 사용자 불만, 재시도 가능)                            │
    │  │  온라인 게임 (Network: 50ms, Miss → 랙, 재접속 가능)                                   │
    │  │  스포츠 경기 (Score: Real-time, Miss → TV 중계 약간 지연)                             │
    │                                                                                         │
    │  특징:                                                                                   │
    │  • Deadline Miss Rate: 낮게 유지 (예: 5% 미만)                                          │
    │  │  평균 경우(Average Case) 분석                                                          │
    │  │  Best-Effort                                                                          │
    │  │  Quality of Service (QoS)                                                             │
    │                                                                                         │
    │  OS: Windows, Linux (CFS), macOS                                                         │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Rate Monotonic (RM) 스케줄링

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Rate Monotonic 스케줄링                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [정의]

    주기(Period)가 짧을수록 높은 우선순위 부여
    → Static Priority (고정 우선순위)

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Task    │ Period (T) │ Execution (C) │ Utilization │ Priority │                     │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  T1      │    50ms    │      20ms      │    0.40     │   High   │                     │
    │  T2      │   100ms    │      30ms      │    0.30     │   Medium │                     │
    │  T3      │   200ms    │      40ms      │    0.20     │   Low    │                     │
    │                                                                                         │
    │  Total Utilization = 0.40 + 0.30 + 0.20 = 0.90                                            │
    │                                                                                         │
    │  Priority: T1(50ms) > T2(100ms) > T3(200ms)                                                │
    │           (Period이 짧을수록 높은 우선순위)                                              │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [간트 차트]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  T1: Period=50, Execution=20                                                             │
    │  T2: Period=100, Execution=30                                                            │
    │  T3: Period=200, Execution=40                                                            │
    │                                                                                         │
    │  Time  0~200ms Timeline                                                                  │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │ T1(20) T1(20) T1(20) T1(20)                                                         │  │
    │  │ └─────┘ └─────┘ └─────┘ └─────┘                                                       │  │
    │  │ 0      50     100    150    200                                                    │  │
    │  │                                                                                      │  │
    │  │       T2(30)       T2(30)                                                            │  │
    │  │       └──────┘     └──────┘                                                            │  │
    │  │       50            150                                                           │  │
    │  │                                                                                      │  │
    │  │              T3(40)                                                                │  │
    │  │              └──────┘                                                               │  │
    │  │              100                                                                   │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │
    │  → 모든 Task이 Deadline 내에 완료                                                          │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Utilization Bound Analysis]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  RM 스케줄러가 모든 Task를 스케줄링 가능한 최대 Utilization                                           │
    │                                                                                         │
    │  U(n) = n × (2^(1/n) - 1)                                                                │
    │                                                                                         │
    │  n=1: U(1) = 1.0 = 100%                                                                  │
    │  n=2: U(2) = 0.828 = 82.8%                                                               │
    │  n=3: U(3) = 0.779 = 77.9%                                                               │
    │  n→∞: U(∞) = ln(2) ≈ 0.693 = 69.3%                                                      │
    │                                                                                         │
    │  예: 3개 Task → Utilization ≤ 77.9%이면 Deadline 보장                                        │
    │      90% > 77.9% → Deadline Miss 가능                                                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### EDF (Earliest Deadline First) 스케줄링

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         EDF (Earliest Deadline First)                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [정의]

    마감 시간(Deadline)이 가장 이른 Task 우선
    → Dynamic Priority (동적 우선순위)

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Task    │ Period (T) │ Execution (C) │ Deadline          │                     │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  T1      │    50ms    │      20ms      │ 50, 100, 150, ...  │                     │
    │  T2      │   100ms    │      30ms      │ 100, 200, 300, ...  │                     │
    │  T3      │   200ms    │      40ms      │ 200, 400, 600, ...  │                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Time 0]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  T1: Deadline=50, T2: Deadline=100, T3: Deadline=200                                       │
    │  → T1 우선 (Deadline 50이 가장 이름)                                                         │
    │                                                                                         │
    │  Time 0~20: T1 실행                                                                      │
    │  • T1 남은 실행: 0                                                                       │
    │  • T1 새로운 Deadline: 50 (Period 50)                                                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Time 20]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Ready Queue: T2(Deadline=100), T3(Deadline=200), T1(Deadline=50)                               │
    │  → T1 우선 (Deadline 50가 가장 이름)                                                         │
    │                                                                                         │
    │  Time 20~40: T1 실행                                                                      │
    │  • T1 남은 실행: 0                                                                       │
    │  • T1 새로운 Deadline: 100 (Period 50, 50+50)                                             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Time 40]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Ready Queue: T2(Deadline=100), T3(Deadline=200), T1(Deadline=100)                               │
    │  → T2, T1 동일 Deadline=100 (T2 먼저 도착 가정)                                                │
    │                                                                                         │
    │  Time 40~70: T2 실행                                                                      │
    │  • T2 남은 실행: 0                                                                       │
    │  • T2 새로운 Deadline: 200                                                                │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Utilization Bound]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  EDF의 최대 Utilization Bound: 100% (단, Preemptive, 단일 프로세서)                              │
    │                                                                                         │
    │  단, 실제로는 Task 동기화, Context Switch 오버헤드로 인해                                 │
    │  약 90~95% Utilization 실용                                                              │
    │                                                                                         │
    │  장점:                                                                                   │
    │  • RM보다 높은 Utilization 가능                                                           │
    │  │  Period과 무관하게 Deadline만 보면 됨                                                   │
    │  │  최적의 Dynamic Priority Algorithm                                                     │
    │                                                                                         │
    │  단점:                                                                                   │
    │  • 실행 시마다 우선순위 재계산 (오버헤드)                                                   │
    │  │  단일 프로세서에서만 최적                                                              │
    │  │  예측 불가능(Deterministic하지 않음)                                                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### RM vs EDF 비교

| 항목 | Rate Monotonic (RM) | EDF (Earliest Deadline First) |
|------|---------------------|-------------------------------|
| **우선순위** | Static (고정) | Dynamic (동적) |
| **기준** | Period (주기) | Deadline (마감 시간) |
| **Optimal** | 단일 프로세서에서만 | 단일 프로세서에서만 |
| **Utilization Bound** | 69% (n→∞) | 100% (이론적) |
| **예측 가능성** | 높음 | 낮음 |
| **오버헤드** | 낮음 | 높음 (매번 계산) |

### 과목 융합 관점 분석

#### 1. 컴퓨터 구조 ↔ Real-time
- **Interrupt Latency**: 인터럽트 지연
- **Cache Miss**: 예측 불가능한 지연
- **DMA**: CPU 개입 없는 전송

#### 2. 제어 이론 ↔ Real-time
- **Feedback Control**: 제어 루프 시간
- **Stability**: Deadline 보장 시 안정성

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 자동차 엔진 ECU (Electronic Control Unit)
**상황**: Hard Real-time, Safety-critical
**판단**:
1. **Task 분석**:
   - Sensor Read: Period=1ms, Execution=0.1ms
   - Control Loop: Period=10ms, Execution=2ms
   - Diagnosis: Period=100ms, Execution=5ms
2. **스케줄링**: Rate Monotonic (안정성)
3. **Safety**: ISO 26262 ASIL-D (Automotive Safety Integrity Level)

```c
// AUTOSAR OS (OSEK/VDX 표준)
Task_Sensor_Read() {
    // Period=1ms, Priority=High (가장 짧은 주기)
    Read_Sensor_Data();
    Activate_Task(Control_Loop);
}

Task_Control_Loop() {
    // Period=10ms, Priority=Medium
    Control_Computation();
    Actuate_Output();
}

Task_Diagnosis() {
    // Period=100ms, Priority=Low
    Run_Diagnostics();
    Check_Fault_Codes();
}
```

---

## Ⅴ. 기대효과 및 결론

### Real-time 스케줄링 기대 효과

| 시스템 유형 | 추천 알고리즘 | 이유 |
|----------|-------------|------|
| **Safety-critical** | Rate Monotonic | 안정성, 예측 가능 |
| **Multimedia** | EDF | 높은 Utilization |
| **Embedded** | Fixed Priority | 구현 단순 |
| **General** | CFS + Real-time class | 유연성 |

### 미래 전망

1. **Mixed-criticality**: 다양한 우선순위 혼합
2. **Energy-aware**: 전력 소모 최소화 스케줄링
3. **AI-based**: Workload 예측 기반 스케줄링

### ※ 참고 표준/가이드
- **ISO 26262**: Automotive Safety
- **DO-178C**: Avionics
- **IEC 61508**: Functional Safety

---

## 📌 관련 개념 맵

- [스케줄러](./84_scheduler.md) - 스케줄링 기반
- [스케줄링 알고리즘](./85_scheduling_algorithms.md) - 일반 알고리즘
- [데드락](../../2_process_thread/84_deadlock.md) - 동기화 문제
- [RTOS](../8_realtime/) - 실시간 OS 상세
