+++
title = "247. 교착 상태 탐지 대기 그래프 (Wait-for Graph)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 247
+++

# 247. 교착 상태 탐지 대기 그래프 (Wait-for Graph)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 대기 그래프(Wait-for Graph)는 트랜잭션 간의 자원 대기 관계를 방향 그래프(Directed Graph)로 모델링하여, 교착 상태(Deadlock) 발생 가능성을 시각적으로 판별하는 데이터베이스의 핵심 제어 구조이다.
> 2. **가치**: 단순한 대기 상태 모니터링을 넘어, 그래프 내 **사이클(Cycle) 존재 여부**를 수학적 알고리즘(DFS, 위상 정렬 등)으로 검증함으로써 시스템 레벨의 교착 상태를 확정 짓고, 트랜잭션 Rollback의 기준을 제공한다.
> 3. **융합**: 운영체제(OS)의 자원 할당 그래프(Resource Allocation Graph) 이론을 기반으로 데이터베이스의 동시성 제어(Concurrency Control) 메커니즘과 결합되어, 고가용성(HA) 시스템의 무결성을 보장하는 최후의 방어선 역할을 수행한다.

+++

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
대기 그래프(Wait-for Graph)는 데이터베이스 관리 시스템(DBMS; Database Management System)에서 동시에 실행되는 여러 트랜잭션(Transaction) 간의 자원 대기 관계를 표현한 이중 방향 그래프(Bipartite Directed Graph)의 변형입니다.
여기서 **노드(Node)**는 활성화된 트랜잭션을, **방향성 간선(Directed Edge)**은 "트랜잭션 A가 트랜잭션 B가 점유한 데이터(Data Item)를 기다리고 있다"는 의미를 가집니다. 기존의 시스템 자원 할당 그래프가 '프로세스-자원' 간의 관계를 표현하는 것과 달리, 대기 그래프는 트랜잭션 간의 의존성을 직접 연결하여 복잡도를 낮추고 분석을 용이하게 만듭니다.

**2. 💡 비유**
이는 마치 여러 자동차가 교차로에 진입해 상대방의 통행이 끝나기를 기다리는 상황과 같습니다. 만약 A차가 B차를, B차는 C차를, 그리고 C차는 다시 A차를 기다리는 원형 대기가 형성된다면, 이 교차로는 영원히 막히게 됩니다. 대기 그래프는 이 원형 대기 구조를 지도(Map)로 그려주는 역할을 합니다.

**3. 등장 배경 및 필요성**
① **기존 한계**: 락(Lock) 기반의 동시성 제어에서 '타임아웃(Timeout)' 기법은 교착 상태가 발생했는지 확실하지 않은 상태에서 무조건 대기를 멈추거나, 반대로 너무 오래 기다려야 하므로 리소스 낭비가 심했습니다.
② **혁신적 패러다임**: 그래프 이론(Graph Theory)을 도입하여, 트랜잭션의 대기 관계를 수학적 구조로 변환하고 **'사이클(Cycle)' 존재 여부**만으로 교착 상태를 O(1) 혹은 O(N)의 복잡도로 빠르게 판별하고자 하는 패러다임이 등장했습니다.
③ **현재의 비즈니스 요구**: 금융권(FinTech)이나 대규모 커머스 시스템에서는 트랜잭션 처리량(TPS; Transactions Per Second)이 매우 높고, 교착 상태 발생 시 시스템 장애로 직결되므로, 이를 즉각 감지하고 해결해야 하는 실무적 요구가 매우 강력합니다.

**📢 섹션 요약 비유**: 대기 그래프의 도입은 마치 복잡한 도시의 교통 상황을 CCTV로 단순 모니터링하는 것에서 벗어나, 실시간 교통 흐름 알고리즘을 통해 '교차로 진입 불가 구역'을 수학적으로 예측하여 신호등을 제어하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 정의**

대기 그래프는 트랜잭션의 상태 변화에 따라 동적으로 변경되는 자료 구조입니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/특징 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **노드 (Node)** | 실행 중인 트랜잭션 객체 | $T_i$: 작업 요청 단위 (Process ID) | 고유 식별자(ID) 할당 | 운전자 |
| **간선 (Edge)** | 대기 관계 (Dependency) | $T_i \rightarrow T_j$: $T_i$가 $T_j$의 Lock을 대기 | Lock Request Queue의 연결 | 추월 불가 대기열 |
| **사이클 (Cycle)** | 교착 상태의 증거 | $T_1 \rightarrow T_2 \rightarrow \dots \rightarrow T_1$ | 그래프 탐색 알고리즘 탐지 대상 | 원형 서로 막힘 |
| **Lock Manager** | 그래프 관리 주체 | 간선 추가/제거 및 사이클 검사 트리거 | Deadlock Detection Interval | 교통 통제소 |
| **Victim** | 제거될 트랜잭션 | 사이클을 끊기 위해 Rollback될 대상 | Cost Based Selection(비용 기반) | 사고 차량 견인 |

**2. 아키텍처 다이어그램 및 데이터 흐름**

아래 다이어그램은 Lock Manager(LM)가 트랜잭션의 요청을 받아 대기 그래프를 갱신하고, 주기적으로 사이클을 검사하는 과정을 도식화한 것입니다.

```text
[Wait-for Graph Architecture & Cycle Detection Flow]

1. Request Phase (트랜잭션 요청)
   ┌─────────┐
   │ T1      │───────────(Request Lock on Row A)────────▶ ┌──────────────┐
   └─────────┘                                             │  Lock Table   │
                                                           │ (Resource A) │
   ┌─────────┐                                             │ Held by: T2  │
   │ T2      │───────────(Request Lock on Row B)────────▶ └──────┬───────┘
   └─────────┘                                                     │
                                                                   ▼
2. Graph Construction (대기 그래프 구성)                  ┌──────────────────┐
   If (Lock is Held by Other)                              │  Lock Manager    │
      Add Edge: Ti -> Tj                                   │ (Wait-for Graph) │
   End If                                                  └─────────┬────────┘
        ▲                                                        │
        │  Graph Update                                           │
        └────────────────────────────────────────────────────────┘

3. Visualization & Detection (탐지)
      ┌────┐                 ┌────┐
   T1 │    │────────────────▶│ T2 │ (Wait for A held by T2)
      └────┘                 └────┘
        ▲                      │
        │ ┌────────────────────┘
        │ │  (Wait for B held by T3)
      ┌────┐
      │ T3 │────────────────────┘
      └────┘
        * Graph Status: Cycle Detected (T1 -> T2 -> T3 -> T1)

4. Resolution (해결)
   Trigger ▶ [Deadlock Resolver] ▶ Select Victim (e.g., T3) ▶ ROLLBACK T3
```

**3. 심층 동작 원리 및 알고리즘**
대기 그래프의 핵심은 **'간선(Edge)의 동적 관리'**와 **'사이클(Cycle)의 탐지'**입니다.

1.  **간선 생성 (Edge Creation)**: 트랜잭션 $T_i$가 자원 $R$을 요청했을 때, $R$을 이미 점유한 $T_j$가 있다면 시스템은 `Wait-for Graph`에 $T_i$에서 $T_j$로 향하는 간선을 생성합니다. 이때 $T_i$는 블록(Block) 상태가 됩니다.
2.  **간선 제거 (Edge Removal)**: $T_j$가 작업을 완료하고 커밋(Commit)하여 Lock을 해제하면, $T_i$가 $R$을 획득하므로 $T_i \rightarrow T_j$ 간선을 삭제합니다. $T_i$는 실행(Runnable) 상태로 전환됩니다.
3.  **사이클 탐지 알고리즘 (Cycle Detection Algorithm)**:
    - 주로 **DFS (Depth-First Search, 깊이 우선 탐색)** 알고리즘을 사용합니다.
    - 그래프의 모든 노드를 순회하며, 현재 방문 중인 노드가 이미 방문 경로(스택)에 존재하는지 확인합니다. (**Back Edge** 확인)
    - 수학적으로 $G=(V, E)$인 그래프에서 $V$는 트랜잭션 집합, $E$는 대기 간선 집합이며, 사이클 $C$가 존재하면 $\exists C \subset E$ such that $\sum_{v \in C} deg(v) \ge 2$를 만족합니다.

**4. 핵심 코드 및 로직 (Pseudo-code)**

```python
# Python-style Pseudo-code for Deadlock Detection
class LockManager:
    def __init__(self):
        self.wait_for_graph = defaultdict(set) # Adjacency List
        self.transactions = set()

    def request_lock(self, txn, resource):
        owner = self.get_lock_owner(resource)
        if owner is None:
            self.grant_lock(txn, resource) # Lock 획득 성공
            self.remove_edge(txn, owner)   # 대기 그래프 간선 제거 (이전 대기가 있었다면)
        elif owner != txn:
            self.wait_for_graph[txn].add(owner) # 간선 추가: T_wait -> T_hold
            self.block(txn)
            self.detect_deadlock() # 사이클 탐지 트리거

    def detect_deadlock(self):
        visited = set()
        rec_stack = set() # 재귀 호출 스택 (현재 경로)

        for node in list(self.wait_for_graph.keys()):
            if node not in visited:
                if self.dfs(node, visited, rec_stack):
                    self.resolve_deadlock()
                    break

    def dfs(self, node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in self.wait_for_graph[node]:
            if neighbor not in visited:
                if self.dfs(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True # 사이클 발견!

        rec_stack.remove(node)
        return False
```

**📢 섹션 요약 비유**: 대기 그래프의 동작 원리는 마치 **'GPS 내비게이션의 실시간 경로 재탐색'**과 같습니다. 내비게이션(트랜잭션)이 목적지(자원)로 가려는데 앞차(Lock)가 막고 있으면, 시스템은 이를 '대기 경로(Edge)'로 인식합니다. 만약 A가 B를, B가 C를, C가 다시 A를 막고 있는 순환 구조가 포착되면, 내비게이션은 "이 경로는 막혔다"고 판단하고, 가장 낮은 우선순위의 차량(Victim)을 다른 길로 우회시키거나(Rollback) 경로를 초기화하는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 심층 비교: Wait-for Graph vs. Timeout**

대기 그래프 기법과 전통적인 타임아웃(Timeout) 기법은 실무에서 자주 비교됩니다.

| 비교 항목 (Criteria) | Wait-for Graph (대기 그래프) | Timeout (타임아웃) |
|:---|:---|:---|
| **탐지 메커니즘** | 능동적 (Active): 그래프 탐색으로 사이클 명시적 판별 | 수동적 (Passive): 대기 시간 초과 시 잠정적 판별 |
| **부하 (Overhead)** | CPU 및 메모리 사용량이 높음 (주기적 탐지 필요) | 트랜잭션 대기 큐(Wait Queue) 관리 외 추가 오버헤드 적음 |
| **정확도 (Accuracy)** | 매우 높음 (False Positive 거의 없음) | 낮음 (교착 상태가 아닌데 느린 처리로 오판 가능) |
| **응답 속도 (Latency)** | 즉각적 (Cycle 형성 즉시 감지 가능) | 지연 발생 (Timeout 설정 시간까지 대기 필요) |
| **구현 복잡도** | 높음 (그래프 자료구조 및 탐지 알고리즘 필요) | 낮음 (Timer 설정만으로 구현 가능) |
| **주요 사용처** | OLTP, 금융 거래 등 정합성이 중요한 대규모 시스템 | 간단한 애플리케이션, 분산 환경에서의 최후의 수단 |

**2. 타 과목 융합 관점 (시너지 및 오버헤드)**

**① 운영체제(OS)와의 융합:**
대기 그래프는 OS의 **자원 할당 그래프(RAG; Resource Allocation Graph)** 이론을 직접적으로 차용했습니다. OS에서는 프로세스가 I/O 장치나 메모리를 요청할 때 교착 상태가 발생하며, 이를 Avoidance(은행원 알고리즘)나 Detection(사이클 탐지)으로 해결합니다. 차이점이라면 OS는 '자원'을 노드로 포함하지만, DBMS의 대기 그래프는 트랜잭션 간 관계에 집중하여 자원을 추상화한다는 점입니다.

**② 분산 데이터베이스(DDMS)와의 융합:**
단일 서버가 아닌 분산 환경에서는 **'분산 대기 그래프(Distributed Wait-for Graph)'** 문제가 발생합니다. 트랜잭션이 서로 다른 노드에 있을 때, 각 노드의 로컬 그래프만으로는 전체 사이클을 파악하기 어렵습니다.
- **오버헤드**: 전체 그래프를 구성하기 위해 노드 간에 메시지를 교환해야 하므로 네트워크 트래픽이 증가합니다.
- **해결 기법**: 계층적 탐지(Hierarchical Detection)나 우편 조사법(Probe Algorithm) 등을 사용하여 네트워크 부하를 줄이면서 전역 사이클을 찾습니다.

**③ 네트워크와의 연관성:**
분산 트랜잭션 처리(2PC; Two-Phase Commit) 과정에서 교착 상태가 발생하면, 네트워크 지연(Latency)과 결합하여 사이클 탐지가 늦어질 경우 시스템 전체가 멈추는 **Thundering Herd** 현상을 유발할 수도 있어, 탐지 주기 조정이 매우 중요합니다.

**📢 섹션 요약 비유**: 대기 그래프와 타임아웃의 선택은 **'지구상의 위치를 찾는 방식'**의 차이와 같