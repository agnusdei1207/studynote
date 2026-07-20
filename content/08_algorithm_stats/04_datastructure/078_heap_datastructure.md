---
title: "Heap Datastructure"
date: "2026-04-29"
tags:
  - "studynote-algorithm-stats"
weight: 78
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 힙(Heap)은 완전 이진 트리(Complete Binary Tree) 형태의 자료구조로, 최대 힙(Max-Heap)에서는 부모 노드가 항상 자식보다 크고, 최소 힙(Min-Heap)에서는 부모가 항상 자식보다 작다. 이 힙 속성(Heap Property)으로 인해 루트(Root)는 항상 최댓값(또는 최솟값)이 되어 O(1)에 최우선 원소를 반환한다.
> 2. **가치**: 힙은 우선순위 큐(Priority Queue)의 표준 구현체로, 삽입(Push)과 삭제(Pop) 모두 O(log n)을 보장한다. 다익스트라(Dijkstra) 최단 경로, 프림(Prim) MST, 힙 정렬(Heap Sort), 운영체제의 프로세스 스케줄링이 모두 힙을 핵심 자료구조로 사용한다.
> 3. **판단 포인트**: 힙은 "전체 정렬"이 아닌 "부분 순서(Partial Order)" 구조다. 전체 정렬(O(n log n))이 필요하면 배열 정렬이 적합하지만, "현재 최솟값만 빠르게 필요"한 경우(스트리밍 최솟값, 스케줄러)에는 힙의 O(log n) 삽입/삭제가 훨씬 효율적이다.

---

## Ⅰ. 개요 및 필요성

```text
+------------------------------------------------------------+
|              최대 힙 구조 (배열 인덱스 기반)                  |
+------------------------------------------------------------+
|                                                            |
|         [10]                  인덱스:                       |
|        /    \                 0: 10 (루트)                  |
|      [8]    [9]               1: 8                         |
|     / \    / \                2: 9                         |
|   [5] [7] [3] [6]             3: 5                         |
|                               4: 7  ...                    |
|  배열: [10, 8, 9, 5, 7, 3, 6]                              |
|  부모(i) = (i-1) // 2                                      |
|  왼쪽(i) = 2*i + 1, 오른쪽(i) = 2*i + 2                   |
+------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 힙은 병원 응급실 대기 시스템이다. 가장 위급한 환자(최솟값/최댓값)가 항상 가장 먼저 처치받을 수 있도록, 대기 목록을 반정렬 상태로 유지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 힙 핵심 연산

```python
import heapq  # Python: 기본 최소 힙

# 힙 생성 및 사용
heap = []
heapq.heappush(heap, 5)   # O(log n)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)
min_val = heapq.heappop(heap)  # O(log n): 3 반환

# heapify: 기존 리스트를 힙으로 변환 O(n)
data = [5, 3, 7, 1, 4]
heapq.heapify(data)

# 최대 힙: 값을 음수로 저장
max_heap = []
heapq.heappush(max_heap, -10)
heapq.heappush(max_heap, -5)
max_val = -heapq.heappop(max_heap)  # 10 반환
```

### Sift-Up (삽입) / Sift-Down (삭제) 원리

```text
삽입(Push):  새 원소를 마지막에 추가 -> Sift-Up (부모와 비교·교환)
             O(log n): 트리 높이만큼 비교

삭제(Pop):   루트를 제거 -> 마지막 원소를 루트로 -> Sift-Down
             O(log n): 두 자식 중 더 큰/작은 값과 교환 반복
```

- **📢 섹션 요약 비유**: Sift-Up은 신입사원이 능력에 맞는 직급(부모)을 찾아 올라가는 것이고, Sift-Down은 은퇴한 CEO 자리를 누가 채울지 아래 직급에서 선발(비교·교환)하는 것이다.

---

## Ⅲ. 비교 및 연결

| 연산 | 힙 | 정렬 배열 | 비정렬 배열 |
|:---|:---|:---|:---|
| **삽입** | O(log n) | O(n) | O(1) |
| **최솟값** | O(1) | O(1) | O(n) |
| **삭제 최솟값** | O(log n) | O(1) 삭제+재정렬 불필요 | O(n) |

힙 정렬(Heap Sort):
1. 전체 배열로 힙 구성: O(n)
2. n번 Pop: O(n log n)
-> 총 O(n log n), 추가 공간 O(1) (In-place)

- **📢 섹션 요약 비유**: 힙과 배열 정렬의 차이는 도서관 배열과 우편함 비교다. 도서관(정렬 배열)은 모든 책이 정렬되어 n번째 책도 O(1)에 찾지만, 우편함(힙)은 "가장 중요한 우편"만 즉시 꺼낼 수 있고 나머지 순서는 보장 안 된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 다익스트라 알고리즘에서 힙 활용

```python
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]  # (거리, 노드) 최소 힙

    while pq:
        curr_dist, curr = heapq.heappop(pq)
        if curr_dist > dist[curr]: continue

        for next_node, weight in graph[curr]:
            new_dist = curr_dist + weight
            if new_dist < dist[next_node]:
                dist[next_node] = new_dist
                heapq.heappush(pq, (new_dist, next_node))

    return dist
# 힙 없는 다익스트라: O(V^)
# 힙 기반 다익스트라: O((V+E) log V)
```

- **📢 섹션 요약 비유**: 힙 기반 다익스트라는 GPS 네비게이션이다. 다음에 탐색할 가장 가까운 지점을 힙에서 즉시 꺼내어(O(log n)) 불필요한 탐색 없이 최단 경로를 효율적으로 찾는다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **우선순위 처리** | 최솟값/최댓값 O(1) 접근 |
| **효율적 정렬** | Heap Sort O(n log n) In-place |
| <strong>알고리즘 기반</strong> | 다익스트라, 프림, A* 핵심 구조 |

OS 프로세스 스케줄러(우선순위 스케줄링), 이벤트 루프(Node.js, Java NIO)의 타이머 관리, 스트리밍 데이터의 상위 K개 유지(Top-K 문제)가 모두 힙을 핵심 자료구조로 사용한다.

- **📢 섹션 요약 비유**: 힙은 컴퓨터 세계의 VIP 대기열이다. 중요한 작업(높은 우선순위)이 들어오면 즉시 앞자리를 차지하고, 나머지는 자동으로 재정렬된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>우선순위 큐</strong> | 힙의 가장 일반적인 응용 |
| <strong>다익스트라</strong> | 힙 기반 최단 경로 알고리즘 |
| <strong>힙 정렬</strong> | In-place O(n log n) 정렬 |
| <strong>완전 이진 트리</strong> | 힙의 구조적 기반 |
| <strong>프림 알고리즘</strong> | 힙 기반 MST 알고리즘 |

### 📈 관련 키워드 및 발전 흐름도

```text
[완전 이진 트리 — 힙의 구조적 기반]
    |
    v
[최소/최대 힙 — 힙 속성(Heap Property)]
    |
    v
[우선순위 큐 — 힙의 ADT 응용]
    |
    v
[다익스트라/프림 MST — 그래프 알고리즘 활용]
    |
    v
[스트리밍 Top-K — 실시간 대용량 데이터 처리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 힙은 항상 가장 중요한 것(최솟값/최댓값)이 맨 앞에 있는 특별한 줄이에요!
2. 새 사람이 들어오면 자동으로 자기 위치(우선순위 순서)를 찾아가고, 가장 앞 사람이 나가면 뒤의 사람이 자동으로 재정렬돼요.
3. OS의 작업 스케줄러부터 네비게이션 앱까지, 우선순위가 필요한 거의 모든 곳에서 힙이 사용된답니다!
