+++
title = "211. 직렬 가능 스케줄 (Serializable Schedule) - 데이터 일관성의 보루"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 211
+++

# 211. 직렬 가능 스케줄 (Serializable Schedule) - 데이터 일관성의 보루

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 직렬 가능 스케줄은 다중 트랜잭션(Transaction)이 병행 수행(Concurrent Execution)되더라도, 그 **실행 결과가 어느 하나의 순차적 실행(Sequential Execution) 결과와 수학적으로 동일함을 보장**하는 스케줄링 이론의 최상위 기준입니다.
> 2. **가치**: 데이터베이스의 일관성(Consistency)을 유지하기 위한 '이상적인 상태'를 정의하며, 현대 DBMS의 **Serializable 격리 수준(Isolation Level)**이 목표로 하는 성질입니다. 이를 통해 Dirty Read, Non-repeatable Read, Phantom Read 등의 이상 현상을 근원적으로 차단합니다.
> 3. **융합**: OS의 교착상태(Deadlock) 탐지(자원 할당 그래프)와 이론적 배경을 공유하며, 분산 시스템(Distributed System)의 선형성(Linearizability) 개념으로 확장됩니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**직렬 가능 스케줄(Serializable Schedule)**이란, 여러 트랜잭션이 시간적으로 겹쳐 실행되는 **비직렬 스케줄(Non-serial Schedule)**임에도 불구하고, 그 **최종 결과 데이터베이스 상태(Resulting DB State)**와 읽기 값 집합이 트랜잭션들을 어떤 순서로든 순차적으로 실행한 직렬 스케줄(Serial Schedule)과 완전히 동일한 성질을 갖는 것을 의미합니다. 데이터베이스 관리 시스템(DBMS)은 동시성 제어(Concurrency Control)를 통해 성능(Performance)을 높이되, 데이터 정합성을 잃지 않기 위해 이 '직렬 가능성'을 필수적인 정당성 조건으로 삼습니다.

**등장 배경 및 필요성**
단일 프로세스 환경에서는 트랜잭션이 순차적으로 실행되어 문제가 없었으나, 대용량 처리를 위한 다중 사용자 환경으로 전환되며 병행 수행이 필수적이 되었습니다. 단순히 실행 속도를 높이기 위해 작업을 섞어버리면, **데이터 갱신 분실(Lost Update)**, **모순성 분석(Inconsistent Analysis)** 등의 문제가 발생합니다. 따라서 "우리가 섞어서 실행했지만, 결과적으로는 섞지 않은 것과 같다"라고 증명할 수 있는 수학적 기준이 필요해졌습니다.

**💡 비유**
이는 **여러 요리사가 하나의 부엌에서 동시에 요리를 하되, 나중에 나온 요리들이 마치 한 명이 다 차례대로 요리해서 완성한 것과 똑같은 맛과 상태를 유지해야 하는** 고도의 셰프 시스템과 같습니다.

**📢 섹션 요약 비유**
직렬 가능 스케줄은 **'복잡한 교차로에서 신호등 없이 진입하더라도, 사고 없이 통과한 차량들의 순서가 마치 신호등이 있어서 한 대씩 순서대로 통과한 것과 완벽하게 동일한 흐름을 보장하는 교통 체계'**와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 및 동작 원리**
직렬 가능성을 판단하기 위해서는 연산 간의 충돌(Conflict)을 이해해야 합니다. 트랜잭션의 기본 연산인 `READ(X)`와 `WRITE(X)`는 다음 조건에서 충돌합니다.
1. **동일한 데이터 항목**에 접근
2. 적어도 하나가 `WRITE` 연산
3. 서로 다른 트랜잭션 소속

**Precedence Graph (선행 그래프) 알고리즘**
직렬 가능성을 판별하는 가장 강력한 도구는 **Precedence Graph (우선순위 그래프)** 또는 **Serialization Graph (직렬화 그래프)**입니다. 이 그래프에서 **사이클(Cycle)이 존재하지 않아야(Directed Acyclic Graph, DAG)** 직렬 가능합니다.

**ASCII 구조 다이어그램: Precedence Graph 생성 규칙**

```text
[직렬 가능성 판별 로직: Precedence Graph]

 분석 대상 스케줄 S: T1 -> T2 -> T3 혼합 실행

 1. 의존성(Edge) 생성 규칙 (Conflict Operation 기반)
    ┌─────────────────────────────────────────────────────────────┐
    │  조건: T_i의 연산 A와 T_j의 연산 B가 충돌(Conflict)하고,    │
    │        스케줄 S 상에서 A가 B보다 먼저 실행됨               │
    │                                                             │
    │   [T_i: Operation A] ───────▶ [T_j: Operation B]          │
    │   (화살표: T_i가 T_j보다 먼저 수행되어야 함을 의미)        │
    └─────────────────────────────────────────────────────────────┘

 2. 판별 프로세스 (Cycle Detection)
    
    [Step 1] 연산 분석
    T1: Read(A) ────────────────────┐
    T2:             ──▶ Read(A) ───▶ Write(A) ────┐
    T3:                    ──▶ Write(A) ──────────┘
    
    [Step 2] Edge 추출
    - T1:Read(A) vs T2:Write(A) ──▶ Edge: T1 → T2
    - T1:Read(A) vs T3:Write(A) ──▶ Edge: T1 → T3
    - T2:Write(A) vs T3:Write(A) ──▶ Edge: T2 → T3

    [Step 3] 그래프 시각화 및 판정
    
      ┌───┐
      │ T1 │────────┐
      └───┘        ▼
             ┌─────────────────┐
             ▼                 │
          ┌───┐   ┌───┐   ┌───┐
          │ T2 │──▶│ T3 │   │ ? │
          └───┘   └───┘   └───┘
          
      결과: 사이클(Cycle) 없음.
      의미: T1 → T2 → T3 순서로 직렬화 가능함. (Serializable ✅)
```

**해설 (Deep Dive)**
위 다이어그램은 **Precedence Graph**를 통해 직렬 가능성을 판별하는 과정을 보여줍니다.
1. **Edge 생성**: 트랜잭션 간의 데이터 충돌(Read-Write, Write-Write)이 발생할 때, 선행 작업이 후행 작업에게 화살표를 연결합니다. 이는 "내가 먼저 데이터를 건드렸으니 너는 내 결과를 반드시 반영해야 한다"는 **의존 관계(Dependency)**를 나타냅니다.
2. **사이클 탐지**: 만약 `T1 → T2`, `T2 → T3`, `T3 → T1`과 같이 순환 참조가 생긴다면, "계란이 먼저인지 닭이 먼저인지" 알 수 없는 상태가 되어 **Deadlock** 또는 **Non-serializable** 상태가 됩니다. 그래프가 **DAG(Directed Acyclic Graph, 방향성 비순환 그래프)** 형태라면, 위상 정렬(Topological Sort)을 통해 하나의 직렬 순서를 재구성할 수 있으므로 직렬 가능하다고 판정합니다.

**핵심 알고리즘 코드 (Pseudo-code)**
```python
# Precedence Graph Cycle Detection (DFS 기반)
def is_serializable(schedule):
    # 1. 그래프 초기화
    graph = build_graph_from_conflicts(schedule) 
    visited = set()
    rec_stack = set()

    # 2. DFS를 통한 사이클 탐지
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor): return True
            elif neighbor in rec_stack:
                # Back-edge 발견 -> 사이클 존재
                return True
        
        rec_stack.remove(node)
        return False

    # 3. 모든 노드에 대해 DFS 수행
    for transaction in graph:
        if transaction not in visited:
            if dfs(transaction):
                return False # 사이클 있음 -> 비직렬 가능
    return True # 사이클 없음 -> 직렬 가능
```

**📢 섹션 요약 비유**
직렬 가능성 판별은 **'여러 사람이 동시에 쓴 이력서를 편집할 때, 누가 먼저 썼는지 추적하여 마지막 버전이 오류 없이 합쳐졌는지 화살표로 연결 검증하는 버전 관리 시스템'**과 같습니다. 화살표가 꼬이지(사이클) 않아야 최종본이 성립됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

직렬 가능성은 그 엄격함의 수준에 따라 **충돌 직렬 가능성(Conflict Serializability)**과 **뷰 직렬 가능성(View Serializability)**으로 구분됩니다.

**비교 분석표**

| 비교 항목 | Conflict Serializability (CS) | View Serializability (VS) |
|:---|:---|:---|
| **정의** | 충돌하는 연산 쌍의 순서가 직렬 스케줄과 보존되는지 확인 | 트랜잭션이 읽고 쓴 데이터의 최종 결과(View)가 직렬 스케줄과 동일한지 확인 |
| **판별 복잡도** | 다항 시간(Polynomial Time) 가능 - 쉬움 | NP-Complete 문제 - 매우 어려움 |
| **판별 방법** | Precedence Graph의 사이클 확인 | 충돌 의존성 + Blind Write 확인 |
| **범위 관계** | VS ⊂ CS (CS는 VS의 부분 집합) | CS ⊆ VS (VS는 CS를 포함하는 상위 개념) |
| **실무 적용** | 대부분의 DBMS가 보장하는 기준 | 이론적 연구 목식, 실무 구현 비효율 |

**ASCII 다이어그램: Blind Write와 직렬 가능성**

```text
[Blind Write에 따른 직렬 가능성 변화]

 상황: T1: W(A), T2: W(A) (둘 다 A를 읽지 않고 씀 - Blind Write)

 1. Conflict Serializability 분석
     W(A)와 W(A)는 충돌로 간주 -> Edge 생성
     T1 → T2 (또는 T2 → T1)
     
     스케줄 S: W1(A) -> W2(A)
     그래프: T1 -> T2 (사이클 없음) ✅ Conflict Serializable

 2. 뷰 직렬 가능성의 미묘함 (Complex View Case)
     만약 T3가 끼어들고 초기값(Initial Value)을 고려해야 한다면?
     
     Example:
     T1: R(A) -> W(A)
     T2: W(A)      (Bl Write)
     T3: W(A)      (Bl Write)

     이 경우, T1이 읽은 값이 최종적으로 어떻게 되는지에 따라
     직렬 순서가 달라질 수 있으며, CS보다 판별이 복잡해짐.
```

**과목 융합 및 시너지**
- **OS (운영체제)**: **교착상태(Deadlock) 탐지** 알고리즘인 '자원 할당 그래프(Resource Allocation Graph)'와 직렬 가능성의 '선행 그래프(Precedence Graph)'는 이론적으로 동일한 위상(Topology)을 공유합니다. 자원을 데이터 항목으로, 프로세스를 트랜잭션으로 치환하면 동일한 사이클 탐지 로직을 적용할 수 있습니다.
- **분산 DB (Distributed DB)**: 단일 노드의 직렬 가능성을 넘어, **글로벌 직렬 가능성(Global Serializability)**을 보장하기 위해 **2단계 로킹(2PL, Two-Phase Locking)** 프로토콜이나 타임스탬프 순서화(Timestamp Ordering)가 사용됩니다.

**📢 섹션 요약 비유**
충돌 직렬 가능성은 **'사람이 사람과 충돌하는 순서를 기록하여 순서를 매기는 것'**이라면, 뷰 직렬 가능성은 **'실제 결과물에 남은 손길(지문)만 가지고 작성 순서를 역추적하는 포렌식 기술'**과 같습니다. 전자는 명확하지만, 후자는 경우에 따라 미궁에 빠질 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1. **은행권 핵심 금융 거래 시스템 (Core Banking)**
   - **문제**: 이체와 동시에 조회가 일어나며 잔액이 바뀌는 상황.
   - **의사결정**: `Serializable` 격리 수준을 적용하여 충돌 직렬 가능성을 보장한다.
   - **기술적 선택**: 강력한 Locking 기반 DBMS 설정 사용. 성능 저하가 있더라도 데이터 무결성(Integrity)이 우선시됨.

2. **대규모 SNS 피드 타임라인**
   - **문제**: 수천만 TPS(Transactions Per Second) 발생.
   - **의사결정**: 완벽한 직렬 가능성 보장보다 **Eventual Consistency(결국 일관성)**를 택하거나 `Read Committed` 수준으로 낮춰 처리량(Throughput)을 확보한다.
   - **이유**: 사소한 순서 차이(Non-serializable Anomaly)가 비즈니스에 치명적이 않기 때문.

3. **재고 관리 시스템 (Inventory Management)**
   - **문제**: 선착순 이벤트 동시 주문 폭주.
   - **의사결정**: 낙관적 동시 제어(Optimistic Concurrency Control)를 사용하되, 커밋 시점에 충돌이 감지되면 롤백(Rollback)하여 직렬 가능성을 강제한다.

**도입 체크리스트**
- [ ] **트랜잭션 간 격리**: 트랜잭션들이 서로의 중간 결과를 보지 않도록 격리(Isolation)되었는가?
- [ ] **사이클 감지**: 동시성 제어 매니저가 작업 의존성 사이클을 탐지하고 적절히 롤백/대기 처리하는가?
- [ ] **Lock 순서**: 다중 Lock 획득 시 교착상태 방지를 위해 순서를 규칙적으로 정하는가? (Global Ordering)

**안티패턴 (Anti-Patterns)**
- **Write Skew(쓰기 꼬임)**: `Serializable`이 아닌 `Repeatable Read` 수준에서 발생할 수 있는 현상으로, 두 트랜�