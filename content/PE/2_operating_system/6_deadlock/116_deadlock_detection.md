+++
title = "49. 데드락 감지 (Deadlock Detection)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Deadlock", "Resource-Allocation-Graph", "Banker's-Algorithm", "Wait-Die", "Wound-Wait"]
draft = false
+++

# 데드락 감지 (Deadlock Detection)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데드락 감지는 **"교착 **상태**(Deadlock)**를 **발견**하고 **해결**하는 **기법\"**으로, **Resource Allocation Graph**(자원 **할당 **그래프)**로 **순환**(Cycle)**을 **검출**하고 **Victim**(피해 **프로세스)**를 **선정**하여 **회복**한다.
> 2. **감지**: **Wait-for Graph**(대기 **그래프)**에서 **Cycle**을 **찾고 **Banker's Algorithm**(은행가 **알고리즘)**으로 **안전 **상태**(Safe State)**를 **확인**하며 **O(n²)** **복잡도**의 **Detection Algorithm**으로 **순환 **탐지**를 **수행**한다.
> 3. **해결**: **Prevention**(예방: **Banker's**, **Hierarchical Lock)**, **Avoidance**(회피: **Safe State **유지)**, **Detection**(감지: **주기적 **검사)**, **Recovery**(복구: **Rollback**, **Kill)** 전략이 **있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
데드락 감지는 **"순환 대기 발견"**이다.

**데드락 4가지 조건**:
| 조건 | 설명 |
|------|------|
| **Mutual Exclusion** | 자원 상호 배제 |
| **Hold & Wait** | 자원 보유 대기 |
| **No Preemption** | 비선점 가능 |
| **Circular Wait** | 순환 대기 |

### 💡 비유
데드락은 ****교차로 ****정체 ****와 같다.
- **차량**: 프로세스
- **교차로**: 자원
- **정체**: 데드락

---

## Ⅱ. 아키텍처 및 핵심 원리

### Resource Allocation Graph

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Resource Allocation Graph                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Deadlocked State (Cycle):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Processes (P)  Resources (R)                                                            │  │
    │  ┌──────────┐   ┌──────────┐                                                             │  │
    │  │ P1       │   │ R1       │                                                             │  │
    │  └────┬─────┘   └────┬─────┘                                                             │  │
    │       │              │                                                                    │  │
    │       │ holds        │ request                                                           │  │
    │       ▼              ▼                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  P1 ──holds──→ R1 ──requested by──→ P2 ──holds──→ R2 ──requested by──→ P3 ──holds──→ R3 │  │  │
    │  │  ↑                                                                                  │  │  │
    │  │  └─────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │           requested by                                                                    │  │
    │  │           P3                                                                              │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Cycle: P1 → R1 → P2 → R2 → P3 → R3 → P1 (DEADLOCK!)                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Wait-for Graph Detection

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Deadlock Detection Algorithm                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Wait-for Graph:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  P1 → P2 (P1 waits for resource held by P2)                                        │  │  │
    │  │  P2 → P3 (P2 waits for resource held by P3)                                        │  │  │
    │  │  P3 → P1 (P3 waits for resource held by P1) ← CYCLE!                               │  │  │
    │  │  P4 → P2 (P4 waits for resource held by P2)                                         │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Detection Algorithm (DFS-based):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  function detect_deadlock(WaitForGraph):                                               │  │
    │      for each process p in WaitForGraph:                                                │  │
    │          visited = {}                                                                   │  │
    │          if dfs_cycle(p, visited, p):     // Start from p, look for cycle back to p     │  │
    │              return p                                                                  │  │
    │      return null                                                                        │  │
    │                                                                                         │  │
    │  function dfs_cycle(current, visited, start):                                           │  │
    │      visited[current] = true                                                            │  │
    │      for each neighbor n of WaitForGraph[current]:                                      │  │
    │          if n == start:                     // Found cycle back to start                    │  │
    │              return true                                                                 │  │
    │          if n not in visited and dfs_cycle(n, visited, start):                          │  │
    │              return true                                                                 │  │
    │      visited[current] = false   // Backtrack                                          │  │
    │      return false                                                                        │  │
    │                                                                                         │  │
    │  → O(V + E) complexity where V = processes, E = wait dependencies                        │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Banker's Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Banker's Algorithm (Safe State Check)                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    State:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  Process  │  Allocation  │  Max       │  Available  │  Need (= Max - Allocation)        │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  P0        │  0 1 0      │  7 5 3     │  3 3 2     │  7 4 3                          │  │
    │  │  P1        │  2 0 0      │  3 2 2     │            │  1 2 2                          │  │
    │  │  P2        │  3 0 2      │  9 0 2     │            │  6 0 0                          │  │
    │  │  P3        │  2 1 1      │  2 2 2     │            │  0 1 1                          │  │
    │  │  P4        │  0 0 2      │  4 3 3     │            │  4 3 1                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Safety Check:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  function is_safe_state():                                                                │  │
    │      work = Available                                                                    │  │
    │      finish[] = false for all processes                                                   │  │
    │                                                                                         │  │
    │      repeat:                                                                              │  │
    │          found = false                                                                   │  │
    │          for each process i where finish[i] == false:                                     │  │
    │              if Need[i] ≤ work:               // Process can complete                        │  │
    │                  work = work + Allocation[i]                                               │  │
    │                  finish[i] = true                                                         │  │
    │                  found = true                                                             │  │
    │                                                                                         │  │
    │      until not found                                                                     │  │
    │                                                                                         │  │
    │      return all(finish[i] == true)   // All processes can finish → SAFE                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Example:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Available = [3, 3, 2]                                                                   │  │
    │                                                                                         │  │
    │  Iteration 1: P3 can finish (Need=[0,1,1] ≤ [3,3,2])                                     │  │
    │  → work = [3,3,2] + [2,1,1] = [5,4,3], finish[3] = true                                     │  │
    │                                                                                         │  │
    │  Iteration 2: P1 can finish (Need=[1,2,2] ≤ [5,4,3])                                      │  │
    │  → work = [5,4,3] + [2,0,0] = [7,4,3], finish[1] = true                                      │  │
    │                                                                                         │  │
    │  Iteration 3: P0 can finish (Need=[7,4,3] ≤ [7,4,3])                                      │  │
    │  → work = [7,4,3] + [0,1,0] = [7,5,3], finish[0] = true                                      │  │
    │                                                                                         │  │
    │  Iteration 4: P2 can finish (Need=[6,0,0] ≤ [7,5,3])                                      │  │
    │  → work = [7,5,3] + [3,0,2] = [10,5,5], finish[2] = true                                     │  │
    │                                                                                         │  │
    │  Iteration 5: P4 can finish (Need=[4,3,1] ≤ [10,5,5])                                     │  │
    │  → work = [10,5,5] + [0,0,2] = [10,5,7], finish[4] = true                                    │  │
    │                                                                                         │  │
    │  → All finish[i] = true → SAFE STATE                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 데드락 처리 전략

| 전략 | 방법 | 장점 | 단점 |
|------|------|------|------|
| **Prevention** | 4조건 중 1개 제거 | 보장적 | 자원 낭비 |
| **Avoidance** | 안전 상태만 | 유연성 | 낮은 이용률 |
| **Detection** | 순환 탐지 | 높은 이용률 | 복구 비용 |
| **Recovery** | Rollback/Kill | 간단 | 데이터 손실 |

### 데드락 예방 (Prevention)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Deadlock Prevention Techniques                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Hold & Wait Prevention:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Rule: Process must request all resources at once                                     │  │
    │  → Starvation risk (waiting for all resources to be available)                        │  │
    │  → Low resource utilization                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Preemption:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Rule: If process waits for resource held by waiting process, preempt               │  │
    │  → "Take away" resource from one process                                               │  │
    │  → Complex rollback                                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Resource Ordering (Hierarchical Lock):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Rule: Acquire locks in predefined order                                                 │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  # Lock hierarchy                                                                     │  │  │
    │  │  LOCK_ORDER = {                                                                     │  │  │
    │  │      'account_mutex': 1,                                                            │  │  │
    │  │      'transaction_mutex': 2,                                                         │  │  │
    │  │      'log_mutex': 3                                                                 │  │  │
    │  │  }                                                                                  │  │  │
    │  │                                                                                     │  │  │
    │  │  def transfer(from_account, to_account):                                           │  │  │
    │  │      # Always acquire lower-order lock first                                        │  │  │
    │  │      first = min(from_account.lock, to_account.lock)                               │  │  │
    │  │      second = max(from_account.lock, to_account.lock)                              │  │  │
    │  │      lock(first)                                                                   │  │  │
    │  │      lock(second)                                                                  │  │  │
    │  │      # ... transfer ...                                                             │  │  │
    │  │      unlock(second)                                                                │  │  │
    │  │      unlock(first)                                                                 │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  → No circular wait → No deadlock                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 분산 DB 데드락
**상황**: 2단계 락 (2PL) 환경
**판단**: Wait-Die 또는 Wound-Wait

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Distributed Deadlock Prevention                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Wait-Die (Older process waits, younger dies):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Process P1 (timestamp: 100) requests lock held by P2 (timestamp: 50)                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  if (P1.timestamp > P2.timestamp):  # P1 is younger                                   │  │  │
    │  │      P1.abort()                   # Younger dies (restart with new timestamp)        │  │  │
    │  │  else:                            # P1 is older                                    │  │  │
    │  │      P1.wait()                    # Older waits                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → No circular wait (older process never waits for younger)                             │  │
    │  → Younger processes may restart multiple times                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Wound-Wait (Older wounds, younger waits):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Process P1 (timestamp: 100) requests lock held by P2 (timestamp: 50)                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  if (P1.timestamp < P2.timestamp):  # P1 is older                                    │  │  │
    │  │      P2.abort()                   # Older wounds younger (preempts)                    │  │  │
    │  │      P1.acquires_lock()                                                                │  │  │
    │  │  else:                            # P1 is younger                                   │  │  │
    │  │      P1.wait()                    # Younger waits                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → Fewer restarts than Wait-Die                                                         │  │
    │  → Older processes get priority (less starvation)                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 데드락 감지 기대 효과

| 방법 | 오버헤드 | 이용률 | 안전성 |
|------|----------|--------|--------|
| **Prevention** | 낮음 | 낮음 | 높음 |
| **Avoidance** | 중간 | 중간 | 높음 |
| **Detection** | 주기적 | 높음 | 낮음 |

### 모범 사례

1. **설계**: Lock hierarchy
2. **타임아웃**: try_lock 사용
3. **모니터링**: deadlock dump
4. **복구**: Graceful degradation

### 미래 전망

1. **Lock-free**: CAS, RCU
2. **Transactions**: STM
3. **Model checking**: Formal verification
4. **AI**: Deadlock prediction

### ※ 참고 표준/가이드
- **Tanenbaum**: Modern OS
- **Silberschatz**: OS Concepts
- **Linux**: lockdep

---

## 📌 관련 개념 맵

- [데드락 예방](./6_deadlock/111_deadlock_prevention.md) - Banker's
- [뮤텍스](./3_synchronization/116_mutex.md) - Lock
- [프로세스](./2_process_thread/107_process_vs_thread.md) - 스케줄링
