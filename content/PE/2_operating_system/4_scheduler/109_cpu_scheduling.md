+++
title = "42. CPU 스케줄링 알고리즘 (CPU Scheduling Algorithms)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Scheduling", "FCFS", "SJF", "Round-Robin", "CFS"]
draft = false
+++

# CPU 스케줄링 알고리즘 (CPU Scheduling Algorithms)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU 스케줄링은 **"프로세스**에 **CPU **시간**을 **할당**하는 **기법"**으로, **Preemptive**(선점 **가능)와 **Non-Preemptive**(비선점)로 **구분**되며 **평균 **대기 **시간**, **처리율**, **공정성**을 **최적화**한다.
> 2. **알고리즘**: **FCFS**(선입선출), **SJF**(최단 **작업 **우선), **SRTN**(최단 **잔여 **시간), **Round Robin**(시간 **할당량), **Priority**(우선순위), **Multilevel Feedback Queue**(다중 **피드백 **큐)가 **대표적**이다.
> 3. **실제**: **Linux CFS**(Completely Fair Scheduler), **Windows**(Thread **Priority), **macOS**(MLFQ)를 **사용**하며 **O(1)** **스케줄러**와 **BFS**(Brain **Fuck **Scheduler)로 **실시간 **성능**을 **향상**시킨다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
CPU 스케줄링은 **"프로세스 실행 순서 결정"**이다.

**스케줄링 목표**:
- **CPU 활용**: 최대화
- **처리율**: 단위 시간당 완료 작업
- **대기 시간**: 최소화
- **반환 시간**: 완료까지 시간
- **공정성**: 모든 프로세스 기회 보장

### 💡 비유
CPU 스케줄링은 ****계산대 **직원 **배치 ****와 같다.
- **손님**: 프로세스
- **직원**: CPU
- **순서**: 스케줄링

---

## Ⅱ. 아키텍처 및 핵심 원리

### 스케줄링 알고리즘 비교

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Scheduling Algorithms Example                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Processes: P1(24), P2(3), P3(3)  (Burst time in milliseconds)

    FCFS (First-Come, First-Served):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  P1      P2      P3                                                                     │  │
    │  │───────│───│───│                                                                       │  │
    │  0       24      27      30                                                             │  │
    │                                                                                         │  │
    │  Waiting Times:                                                                        │  │
    │  • P1: 0                                                                               │  │
    │  • P2: 24                                                                              │  │
    │  • P3: 27                                                                              │  │
    │  • Average: (0+24+27)/3 = 17ms                                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    SJF (Shortest Job First):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  P2      P3      P1                                                                     │  │
    │  │───│───│───────│                                                                       │  │
    │  0   3       6      30                                                                 │  │
    │                                                                                         │  │
    │  Waiting Times:                                                                        │  │
    │  • P1: 6                                                                               │  │
    │  • P2: 0                                                                               │  │
    │  • P3: 3                                                                               │  │
    │  • Average: (6+0+3)/3 = 3ms                                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Round Robin (Time Quantum = 4):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  P1   P2   P3   P1   P1   P1   P1   P1   P1                                             │  │
    │  │───│───│───│───│───│───│───│───│────│                                                │  │
    │  0   4    8    12   16   20   24   28                                                  │  │
    │                                                                                         │  │
    │  Waiting Times:                                                                        │  │
    │  • P1: 6+4+4+4+4+4 = 26                                                                │  │
    │  • P2: 4                                                                               │  │
    │  • P3: 8                                                                               │  │
    │  • Average: (26+4+8)/3 = 12.7ms                                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Multilevel Feedback Queue

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Multilevel Feedback Queue                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Queue 0 (RR, Q=8ms)  ───→  Queue 1 (RR, Q=16ms)  ───→  Queue 2 (FCFS)                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Priority: Highest          Priority: Medium           Priority: Lowest             │  │  │
    │  │  Time Quantum: 8ms          Time Quantum: 16ms         No preemption                 │  │  │
    │  │  → Interactive jobs        → CPU-intensive         → Batch jobs                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Process Flow:                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  New Process → Queue 0                                                              │  │  │
    │  │       │                                                                                │  │  │
    │  │       ├─ Completes in 8ms → Exit                                                     │  │  │
    │  │       │                                                                                │  │  │
    │  │       └─ Not complete → Queue 1                                                      │  │  │
    │  │              │                                                                        │  │  │
    │  │              ├─ Completes in 16ms → Exit                                            │  │  │
    │  │              │                                                                        │  │  │
    │  │              └─ Not complete → Queue 2                                               │  │  │
    │  │                         │                                                            │  │  │
    │  │                         └─ FCFS until completion                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Aging: Promote lower priority queues to prevent starvation                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 알고리즘 비교

| 알고리즘 | 선점 | 평균 대기 | Starvation | 구현 |
|----------|------|-----------|------------|------|
| **FCFS** | X | 높음 | X | 간단 |
| **SJF** | X | 가장 낮음 | O | 어려움 |
| **SRTN** | O | 낮음 | O | 복잡 |
| **RR** | O | 중간 | X | 중간 |
| **Priority** | O | 다양 | O | 중간 |
| **MLFQ** | O | 다양 | X+ | 복잡 |

### Linux CFS (Completely Fair Scheduler)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Linux CFS Red-Black Tree                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  sched_entity (task)                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Key: vruntime = virtual runtime                                                     │  │  │
    │  │        = exec_time × (NICE_0_LOAD / weight)                                         │  │  │
    │  │                                                                                       │  │  │
    │  │  Red-Black Tree (sorted by vruntime):                                                │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │                               [Task A: vruntime=100]                               │  │  │  │
    │  │  │                              /        \                                           │  │  │  │
    │  │  │            [Task B: vruntime=150]          [Task C: vruntime=200]                 │  │  │  │
    │  │  │            /        \                                                               │  │  │  │
    │  │  │  [Task D: vruntime=180]    [Task E: vruntime=250]                                 │  │  │  │
    │  │  │                                                                                       │  │  │  │
    │  │  │  → Leftmost task (minimum vruntime) runs next                                      │  │  │  │
    │  │  │  → vruntime increases as task runs                                                │  │  │  │
    │  │  │  → Fair: all tasks make progress proportional to weight                            │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Scheduling Decision:                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  1. Pick leftmost task (minimum vruntime)                                            │  │  │  │
    │  │  2. Run for timeslice = sysctl_sched_latency / nr_running                             │  │  │  │
    │  │  3. Update vruntime += timeslice                                                      │  │  │  │
    │  │  4. Re-insert into tree (will move right)                                             │  │  │  │
    │  │  5. Go to step 1                                                                      │  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 실시간 스케줄링

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Real-Time Scheduling                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Rate Monotonic (Fixed Priority):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Task     Period    Priority (inverse of period)                                        │  │
    │  ──────────────────────────────────────────────────────────────────────────────────────│  │
    │  T1       50ms      Highest (shortest period)                                            │  │
    │  T2       100ms     Medium                                                                  │  │
    │  T3       200ms     Lowest                                                                 │  │
    │                                                                                         │  │
    │  → Static priority, optimal for fixed-priority preemptive                                 │  │
    │  → CPU utilization bound: n × (2^(1/n) - 1)                                              │  │
    │    For 3 tasks: 3 × (2^(1/3) - 1) = 0.779 (77.9%)                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    EDF (Earliest Deadline First):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Task     Period    Deadline    Execution                                              │  │
    │  ──────────────────────────────────────────────────────────────────────────────────────│  │
    │  T1       50ms      50ms        20ms                                                     │  │
    │  T2       100ms     100ms       40ms                                                     │  │
    │  T3       200ms     200ms       60ms                                                     │  │
    │                                                                                         │  │
    │  → Dynamic priority (deadline changes)                                                   │  │
    │  → Optimal, 100% CPU utilization possible                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### CPU 스케줄러 확인

```bash
# Linux 스케줄러 확인
cat /proc/sys/kernel/sched_yield_scaling

# CFS 파라미터
cat /proc/sys/kernel/sched_min_granularity_ns
cat /proc/sys/kernel/sched_latency_ns

# 프로세스별 스케줄링 정책
chrt -p $$

# 출력:
# pid 1234's current scheduling policy: SCHED_OTHER
# pid 1234's current scheduling priority: 0

# 우선순위 변경
nice -n 10 command        # Lower priority (nice = 10)
renice -n 5 -p 1234       # Change running process priority
```

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 데이터베이스 서버 튜닝
**상황**: 높은 컨텍스트 스위치
**판단**: 프로세스 우선순위 조정

```bash
# PostgreSQL 프로세스 우선순위 높이기
renice -n -5 -p $(pgrep postgres)

# 또는 ionice로 I/O 우선순위 조정
ionice -c1 -n0 pgrep postgres

# CFS 그룹 스케줄링 (cgroup v2)
mkdir /sys/fs/cgroup/high_priority
echo $$ > /sys/fs/cgroup/high_priority/cgroup.procs
echo 1024 > /sys/fs/cgroup/high_priority/cpu.weight

# → 더 많은 CPU 시간 할당
```

---

## Ⅴ. 기대효과 및 결론

### 스케줄링 기대 효과

| 알고리즘 | 대기 시간 | 처리율 | 공정성 |
|----------|-----------|--------|--------|
| **FCFS** | 높음 | 중간 | O |
| **SJF** | 가장 낮음 | 높음 | X |
| **RR** | 중간 | 높음 | O |
| **MLFQ** | 다양 | 높음 | O |

### 모범 사례

1. **대화형**: RR 또는 MLFQ
2. **일괄 처리**: SJF 또는 FCFS
3. **실시간**: Rate Monotonic 또는 EDF
4. **서버**: CFS (공정성 중시)

### 미래 전망

1. **Energy-aware**: 전력 소비 최적화
2. **Thermal-aware**: 온도 기반 스케줄링
3. **AI**: 머신러닝 기반 예측

### ※ 참고 표준/가이드
- **Linux**: sched(7)
- **Windows**: Thread Scheduling
- **POSIX**: sched.h

---

## 📌 관련 개념 맵

- [문맥 교환](./2_process_thread/108_context_switch.md) - PCB/TCB
- [프로세스 vs 스레드](./2_process_thread/107_process_vs_thread.md) - 실행 단위
- [데드락](./3_synchronization/104_deadlock.md) - 교착 상태
