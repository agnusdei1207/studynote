+++
title = "319. 교착 상태 예방 메커니즘을 위한 타임아웃 (Timeout) 활용"
weight = 319
+++

# 319. 교착상태 모델링 (Deadlock Modeling)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 교착상태 발생 조건을 수학적으로 표현
> 2. **가치**: 교착상태 분석과 예측의 기반
> 3. **융합**: 자원 할당 그래프, 은행원 알고리즘과 연관

---

## Ⅰ. 개요

### 개념 정의

교착상태 모델링(Deadlock Modeling)은 **교착상태 발생 조건과 상황을 수학적/그래프적으로 표현하는 방법**이다. 시스템의 교착상태 가능성을 분석하고 예측한다.

### 💡 비유: 교통 시뮬레이션
교착상태 모델링은 **교통 시뮬레이션**과 같다. 어디서 막힐지 미리 계산해본다. 모델로 문제를 예측한다.

### 교착상태 모델링 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                교착상태 모델링 구조                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【모델링 방법】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  1. 그래프 모델:                                                      │ │
│  │     • 자원 할당 그래프                                                │ │
│  │     • 대기 그래프                                                     │ │
│  │                                                             │ │
│  │  2. 행렬 모델:                                                        │ │
│  │     • Available, Max, Allocation, Need 행렬                         │ │
│  │     • 은행원 알고리즘                                                  │ │
│  │                                                             │ │
│  │  3. 상태 모델:                                                        │ │
│  │     • 안전 상태 / 불안전 상태                                          │ │
│  │     • 상태 전이                                                       │ │
│  │                                                             │ │
│  │  4. 확률 모델:                                                        │ │
│  │     • 교착상태 발생 확률                                               │ │
│  │     • 마코프 체인                                                     │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【그래프 모델】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  자원 할당 그래프 (RAG):                                              │ │
│  │                                                             │ │
│  │       ┌───┐         ┌───┐                                         │ │
│  │       │ P1│ ──요청──►│ R1│                                         │ │
│  │       └───┘         └───┘                                         │ │
│  │         ▲               │                                         │ │
│  │         │               │ 할당                                    │ │
│  │         │               ▼                                         │ │
│  │       ┌───┐         ┌───┐                                         │ │
│  │       │ R2│ ◄──요청──│ P2│                                         │ │
│  │       └───┘         └───┘                                         │ │
│  │                                                             │ │
│  │  P = 프로세스 (원), R = 자원 (사각형)                                  │ │
│  │  간선: 요청 (P→R), 할당 (R→P)                                        │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【행렬 모델】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  Available: [3, 2, 1]  (각 자원의 가용 개수)                         │ │
│  │                                                             │ │
│  │       R1  R2  R3                                                   │ │
│  │  Max:   [7  5   3]    P0                                           │ │
│  │         [3  2   2]    P1                                           │ │
│  │         [9  0   2]    P2                                           │ │
│  │                                                             │ │
│  │  Allocation:                                                        │ │
│  │       R1  R2  R3                                                   │ │
│  │         [0  1   0]    P0                                           │ │
│  │         [2  0   0]    P1                                           │ │
│  │         [3  0   2]    P2                                           │ │
│  │                                                             │ │
│  │  Need = Max - Allocation                                            │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                교착상태 모델링 상세                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Coffman 조건】 (필요충분조건)                                         │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  교착상태 발생 필요조건 4가지:                                          │ │
│  │                                                             │ │
│  │  1. 상호 배제 (Mutual Exclusion)                                     │ │
│  │  2. 점유 대기 (Hold and Wait)                                        │ │
│  │  3. 비선점 (No Preemption)                                           │ │
│  │  4. 순환 대기 (Circular Wait)                                        │ │
│  │                                                             │ │
│  │  모두 만족 시 교착상태 가능 (필요조건)                                    │ │
│  │  순환 대기 = 교착상태 (단일 인스턴스 자원, 충분조건)                       │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【상태 전이 모델】                                                      │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  안전 상태 (Safe)              불안전 상태 (Unsafe)                    │ │
│  │  ┌─────────────┐              ┌─────────────┐                     │ │
│  │  │ 교착상태 X   │    요청/할당   │ 교착상태 가능│                     │ │
│  │  │ 안전 순서 존재│ ──────────► │ 안전 순서 없음│                     │ │
│  │  └─────────────┘              └──────┬──────┘                     │ │
│  │         ▲                            │                           │ │
│  │         │                            │ 추가 요청                  │ │
│  │         │                            ▼                           │ │
│  │         │                     ┌─────────────┐                     │ │
│  │         └─────────────────────│  교착상태    │                     │ │
│  │             자원 해제          │  (Deadlock) │                     │ │
│  │                               └─────────────┘                     │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【확률 모델】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  교착상태 발생 확률 = f(프로세스 수, 자원 수, 요청 패턴)                 │ │
│  │                                                             │ │
│  │  간단한 근사:                                                          │ │
│  │  P(deadlock) ≈ (n × m) / (R × T)                                    │ │
│  │  n = 프로세스 수                                                       │ │
│  │  m = 자원 유형 수                                                      │ │
│  │  R = 총 자원 인스턴스                                                   │ │
│  │  T = 평균 보유 시간                                                    │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【시스템 상태 모델】                                                   │
│  ──────────────────                                                  │
│  class DeadlockModel {                                              │
│      int[] available;       // 가용 자원                              │ │
│      int[][] max;           // 최대 필요량                             │ │
│      int[][] allocation;    // 할당량                                  │ │
│      int[][] need;          // 필요량 = max - allocation              │ │
│                                                                     │
│      int numProcesses;                                              │
│      int numResources;                                              │
│                                                                     │
│      DeadlockModel(int n, int m) {                                  │
│          numProcesses = n;                                          │
│          numResources = m;                                          │
│          available = new int[m];                                    │
│          max = new int[n][m];                                       │
│          allocation = new int[n][m];                                │
│          need = new int[n][m];                                      │
│      }                                                              │
│                                                                     │
│      void calculateNeed() {                                         │
│          for (int i = 0; i < numProcesses; i++) {                   │
│              for (int j = 0; j < numResources; j++) {               │
│                  need[i][j] = max[i][j] - allocation[i][j];         │
│              }                                                      │
│          }                                                          │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【안전성 검사】                                                         │
│  ──────────────────                                                  │
│  boolean isSafe(DeadlockModel model) {                              │
│      int[] work = model.available.clone();                          │
│      boolean[] finish = new boolean[model.numProcesses];            │
│      List<Integer> safeSequence = new ArrayList<>();                │
│                                                                     │
│      while (true) {                                                 │
│          boolean found = false;                                     │
│          for (int i = 0; i < model.numProcesses; i++) {             │
│              if (!finish[i] && canAllocate(model.need[i], work)) {  │
│                  // 프로세스 i가 완료 가능                               │ │
│                  for (int j = 0; j < model.numResources; j++) {     │
│                      work[j] += model.allocation[i][j];             │
│                  }                                                  │
│                  finish[i] = true;                                  │
│                  safeSequence.add(i);                               │
│                  found = true;                                      │
│              }                                                      │
│          }                                                          │
│          if (!found) break;                                         │
│      }                                                              │
│                                                                     │
│      // 모든 프로세스가 완료 가능한지 확인                                 │ │
│      for (boolean f : finish) {                                     │
│          if (!f) return false;  // 불안전 상태                        │ │
│      }                                                              │
│      return true;  // 안전 상태                                       │ │
│  }                                                                  │
│                                                                     │
│  boolean canAllocate(int[] need, int[] work) {                      │
│      for (int i = 0; i < need.length; i++) {                        │
│          if (need[i] > work[i]) return false;                       │
│      }                                                              │
│      return true;                                                   │
│  }                                                                  │
│                                                                     │
│  【그래프 모델 구현】                                                    │
│  ──────────────────                                                  │
│  class ResourceAllocationGraph {                                    │
│      Set<Process> processes = new HashSet<>();                      │
│      Set<Resource> resources = new HashSet<>();                     │
│      List<Edge> edges = new ArrayList<>();                          │
│                                                                     │
│      void addRequestEdge(Process p, Resource r) {                   │
│          edges.add(new Edge(p, r, EdgeType.REQUEST));               │
│      }                                                              │
│                                                                     │
│      void addAssignmentEdge(Resource r, Process p) {                │
│          edges.add(new Edge(r, p, EdgeType.ASSIGNMENT));            │
│      }                                                              │
│                                                                     │
│      boolean hasCycle() {                                           │
│          // 그래프에서 사이클 탐지                                        │ │
│          return new CycleDetector().detect(this);                   │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【교착상태 발생 확률 추정】                                              │
│  ──────────────────                                                  │
│  class DeadlockProbabilityEstimator {                               │
│      double estimateProbability(int processes, int resources,       │
│                                 int totalInstances, double avgHoldTime) {│
│          // 간단한 근사 모델                                            │ │
│          return (double)(processes * resources) /                   │
│                 (totalInstances * avgHoldTime);                     │
│      }                                                              │
│                                                                     │
│      String getRiskLevel(double probability) {                      │
│          if (probability < 0.001) return "LOW";                     │
│          if (probability < 0.01) return "MEDIUM";                   │
│          return "HIGH";                                             │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  【모델 기반 시뮬레이션】                                                 │
│  ──────────────────                                                  │
│  class DeadlockSimulator {                                          │
│      void simulate(List<Process> processes, List<Resource> resources) {│
│          int deadlockCount = 0;                                     │
│          int totalRuns = 10000;                                     │
│                                                                     │
│          for (int run = 0; run < totalRuns; run++) {                │
│              // 무작위 자원 요청 시뮬레이션                                │ │
│              if (simulateRun(processes, resources)) {               │
│                  deadlockCount++;                                   │
│              }                                                      │
│          }                                                          │
│                                                                     │
│          double probability = (double) deadlockCount / totalRuns;   │
│          System.out.println("Deadlock probability: " + probability);│
│      }                                                              │
│  }                                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 교착상태를 수학적/그래프적으로 표현
• 방법: 그래프, 행렬, 상태, 확률 모델
• 조건: Coffman 4조건
• 상태: 안전 vs 불안전
• 도구: 자원 할당 그래프, 은행원 알고리즘
• 활용: 분석, 예측, 시뮬레이션
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [자원 할당 그래프](./301_resource_allocation_graph.md) → 그래프 모델
- [은행원 알고리즘](./302_bankers_algorithm.md) → 행렬 모델
- [교착상태 조건](./297_mutual_exclusion.md) → Coffman 조건
- [안전 상태](./303_safe_state.md) → 상태 모델

### 👶 어린이를 위한 3줄 비유 설명

**개념**: 교착상태 모델링은 "교통 시뮬레이션" 같아요!

**원리**: 미리 계산해봐요!

**효과**: 어디서 막힐지 알 수 있어요!
