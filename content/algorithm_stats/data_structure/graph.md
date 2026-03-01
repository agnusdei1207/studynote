+++
title = "그래프 (Graph)"
date = 2025-03-01

[extra]
categories = "algorithm_stats-data_structure"
+++

# 그래프 (Graph)

## 핵심 인사이트 (3줄 요약)
> **정점(Vertex)과 간선(Edge)으로 구성된 비선형 자료구조**. 방향/무방향, 가중/무가중으로 분류. DFS, BFS, 최단경로, MST 알고리즘이 핵심.

## 1. 개념
그래프는 **정점(Vertex, Node)들과 이들을 연결하는 간선(Edge, Link)들로 구성**된 자료구조다.

> 비유: "지하철 노선도" - 역(정점)과 선로(간선)로 연결

## 2. 그래프 용어

```
┌────────────────────────────────────────────────────────┐
│                   그래프 용어                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  정점 (Vertex/Node): 데이터의 요소                     │
│  간선 (Edge/Link): 정점 간의 연결                      │
│  차수 (Degree): 정점에 연결된 간선 수                  │
│  경로 (Path): 한 정점에서 다른 정점까지의 간선序列     │
│  사이클 (Cycle): 시작과 끝이 같은 경로                 │
│  가중치 (Weight): 간선에 할당된 값                     │
│                                                        │
│  ┌───────────────────────────────────────┐            │
│  │         A ─── B                       │            │
│  │        ╱ ╲     │                      │            │
│  │       ╱   ╲    │                      │            │
│  │      C─────D───E                      │            │
│  └───────────────────────────────────────┘            │
│                                                        │
│  정점: A, B, C, D, E (5개)                            │
│  간선: A-B, A-C, A-D, B-E, C-D, D-E (6개)             │
│  A의 차수: 3 (B, C, D와 연결)                         │
│  경로: A → D → E (A에서 E까지)                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 그래프 종류

```
┌────────────────────────────────────────────────────────┐
│                   그래프 종류                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 방향 그래프 vs 무방향 그래프                       │
│                                                        │
│     무방향: A ── B    (양방향)                         │
│     방향:  A ─→ B    (단방향)                         │
│                                                        │
│  2. 가중치 그래프 vs 무가중치 그래프                   │
│                                                        │
│     무가중: A ── B                                     │
│     가중:   A ──5── B  (비용/거리)                     │
│                                                        │
│  3. 연결 그래프 vs 비연결 그래프                       │
│                                                        │
│     연결: 모든 정점이 경로로 연결                      │
│     비연결: 일부 정점이 분리됨                         │
│                                                        │
│  4. 사이클 그래프 vs 비순환 그래프 (DAG)               │
│                                                        │
│     사이클: A → B → C → A (순환)                       │
│     DAG:   A → B → C (순환 없음)                       │
│                                                        │
│  5. 완전 그래프                                        │
│     모든 정점 쌍이 간선으로 연결                       │
│     간선 수: n(n-1)/2                                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 그래프 표현 방식

```
┌────────────────────────────────────────────────────────┐
│                  그래프 표현 방식                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 인접 행렬 (Adjacency Matrix)                       │
│     ┌─────────────────────────────────────────┐       │
│     │     A   B   C   D                       │       │
│     │ A [ 0   1   1   0 ]                     │       │
│     │ B [ 1   0   0   1 ]                     │       │
│     │ C [ 1   0   0   1 ]                     │       │
│     │ D [ 0   1   1   0 ]                     │       │
│     └─────────────────────────────────────────┘       │
│     장점: 간선 존재 여부 O(1)                          │
│     단점: 공간 O(V²), 희소 그래프 비효율              │
│                                                        │
│  2. 인접 리스트 (Adjacency List)                       │
│     ┌─────────────────────────────────────────┐       │
│     │ A → [B, C]                              │       │
│     │ B → [A, D]                              │       │
│     │ C → [A, D]                              │       │
│     │ D → [B, C]                              │       │
│     └─────────────────────────────────────────┘       │
│     장점: 공간 O(V+E), 희소 그래프 효율               │
│     단점: 간선 존재 여부 O(V)                         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from collections import defaultdict, deque
from typing import Dict, List, Set, Optional, Tuple
import heapq

class Graph:
    """그래프 구현"""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj_list: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        self.vertices: Set[str] = set()

    def add_vertex(self, vertex: str):
        """정점 추가"""
        self.vertices.add(vertex)

    def add_edge(self, u: str, v: str, weight: int = 1):
        """간선 추가"""
        self.vertices.add(u)
        self.vertices.add(v)
        self.adj_list[u].append((v, weight))

        if not self.directed:
            self.adj_list[v].append((u, weight))

    def dfs(self, start: str) -> List[str]:
        """깊이 우선 탐색 (DFS)"""
        visited = set()
        result = []

        def _dfs(vertex: str):
            visited.add(vertex)
            result.append(vertex)

            for neighbor, _ in self.adj_list[vertex]:
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return result

    def dfs_iterative(self, start: str) -> List[str]:
        """DFS (반복문)"""
        visited = set()
        result = []
        stack = [start]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                for neighbor, _ in reversed(self.adj_list[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def bfs(self, start: str) -> List[str]:
        """너비 우선 탐색 (BFS)"""
        visited = set([start])
        result = []
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor, _ in self.adj_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dijkstra(self, start: str) -> Dict[str, int]:
        """다익스트라 최단 경로"""
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0

        pq = [(0, start)]

        while pq:
            dist, vertex = heapq.heappop(pq)

            if dist > distances[vertex]:
                continue

            for neighbor, weight in self.adj_list[vertex]:
                new_dist = dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances

    def has_cycle(self) -> bool:
        """사이클 존재 여부 (무방향 그래프)"""
        visited = set()

        def _dfs_cycle(vertex: str, parent: str) -> bool:
            visited.add(vertex)

            for neighbor, _ in self.adj_list[vertex]:
                if neighbor not in visited:
                    if _dfs_cycle(neighbor, vertex):
                        return True
                elif neighbor != parent:
                    return True

            return False

        for vertex in self.vertices:
            if vertex not in visited:
                if _dfs_cycle(vertex, None):
                    return True

        return False

    def topological_sort(self) -> Optional[List[str]]:
        """위상 정렬 (방향 그래프)"""
        in_degree = {v: 0 for v in self.vertices}

        for vertex in self.vertices:
            for neighbor, _ in self.adj_list[vertex]:
                in_degree[neighbor] += 1

        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor, _ in self.adj_list[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.vertices):
            return None  # 사이클 존재

        return result


# 사용 예시
print("=== 그래프 알고리즘 시연 ===\n")

# 그래프 생성
g = Graph(directed=False)
g.add_edge('A', 'B', 1)
g.add_edge('A', 'C', 2)
g.add_edge('B', 'D', 3)
g.add_edge('C', 'D', 1)
g.add_edge('D', 'E', 2)

print("인접 리스트:")
for vertex in sorted(g.vertices):
    neighbors = [(n, w) for n, w in g.adj_list[vertex]]
    print(f"  {vertex}: {neighbors}")

# DFS
print(f"\nDFS (A에서 시작): {g.dfs('A')}")

# BFS
print(f"BFS (A에서 시작): {g.bfs('A')}")

# 다익스트라
print("\n다익스트라 (A에서 각 정점까지의 최단 거리):")
distances = g.dijkstra('A')
for vertex, dist in sorted(distances.items()):
    print(f"  A → {vertex}: {dist}")

# 사이클 탐지
print(f"\n사이클 존재: {g.has_cycle()}")

# 방향 그래프 위상 정렬
print("\n--- 방향 그래프 위상 정렬 ---")
dag = Graph(directed=True)
dag.add_edge('A', 'C')
dag.add_edge('B', 'C')
dag.add_edge('C', 'D')
dag.add_edge('D', 'E')

topo_order = dag.topological_sort()
print(f"위상 정렬: {topo_order}")
