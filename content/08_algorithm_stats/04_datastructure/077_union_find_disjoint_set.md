---
title: "Union Find Disjoint Set"
date: "2026-04-29"
tags:
  - "studynote-algorithm-stats"
weight: 77
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Union-Find (또는 Disjoint Set Union, DSU)는 여러 원소들을 서로소 집합(Disjoint Set)으로 관리하며, Union(두 집합 합치기)과 Find(원소의 소속 집합 루트 찾기) 연산을 효율적으로 지원하는 자료구조다.
> 2. **가치**: Union-Find는 그래프의 연결 요소(Connected Components) 판별, 크루스칼(Kruskal) MST (Minimum Spanning Tree, 최소 신장 트리) 알고리즘의 사이클 검출에 핵심 역할을 한다. 경로 압축(Path Compression)과 랭크 기반 합집합(Union by Rank)을 적용하면 거의 상수 시간(아커만 함수의 역함수, α(n)≈4)에 각 연산을 처리한다.
> 3. **판단 포인트**: 두 노드가 같은 집합에 속하는지 판별하는 Find 연산이 O(α(n))≈O(1)에 수행되어, 동적으로 변하는 네트워크에서의 연결성 검사에 매우 효율적이다. BFS/DFS가 정적 그래프 연결성 검사라면, Union-Find는 동적 간선 추가 시 연결성 유지에 최적화되어 있다.

---

## Ⅰ. 개요 및 필요성

```text
+----------------------------------------------------------+
|           Union-Find 핵심 연산                             |
+----------------------------------------------------------+
|                                                          |
|  Find(x)  : x가 속한 집합의 루트(대표 원소) 반환           |
|  Union(x,y): x의 집합과 y의 집합을 하나로 합치기            |
|  isConnected(x,y): Find(x)==Find(y) -> 같은 집합 여부      |
|                                                          |
|  최적화                                                    |
|  +- 경로 압축 (Path Compression): Find 시 루트 직결        |
|  +- 랭크 합집합 (Union by Rank): 트리 높이 균형 유지        |
+----------------------------------------------------------+
```

경로 압축 없이 Union-Find를 구현하면 편향 트리(Skewed Tree)가 되어 Find가 O(n)으로 저하된다.

- **📢 섹션 요약 비유**: Union-Find는 학교의 반 배정 시스템이다. 학생(노드)을 반(집합)에 배정(Union)하고, 특정 학생이 몇 반인지 확인(Find)할 수 있다. 반을 합칠 때는 학생 수가 많은 반의 반장(루트)을 대표로 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 경로 압축 (Path Compression)

```python
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])  # 경로 압축: 루트를 직접 가리킴
    return parent[x]

def union(parent, rank, x, y):
    rx, ry = find(parent, x), find(parent, y)
    if rx == ry: return  # 이미 같은 집합
    # 랭크 기반 합집합
    if rank[rx] < rank[ry]: rx, ry = ry, rx
    parent[ry] = rx
    if rank[rx] == rank[ry]: rank[rx] += 1
```

### 크루스칼 MST에서의 Union-Find 활용

```text
간선을 가중치 오름차순 정렬
    |
    v
각 간선 (u, v) 순회
    |
    v
[Find(u) == Find(v)?]
  YES -> 사이클 형성 -> 간선 제외 (Skip)
  NO  -> 사이클 없음  -> 간선 MST에 포함, Union(u,v)
```

- **📢 섹션 요약 비유**: 경로 압축은 지하철 탑승 이력을 단순화하는 것이다. 원래 A->B->C->D(루트) 경로로 다녀왔다면, 다음에는 A->D 직접 경로를 기억하게 하여 매번 전체 경로를 따라가지 않아도 된다.

---

## Ⅲ. 비교 및 연결

| 연산 | Union-Find | BFS/DFS |
|:---|:---|:---|
| **사용 목적** | 동적 그래프 연결성, MST 사이클 검출 | 정적 그래프 탐색, 경로 찾기 |
| <strong>시간 복잡도</strong> | O(α(n)) per op ≈ O(1) | O(V+E) per traversal |
| <strong>공간 복잡도</strong> | O(n) | O(V+E) |
| **간선 추가** | 효율적 (Union 1회) | 재탐색 필요 |

- **📢 섹션 요약 비유**: BFS/DFS는 미로 전체를 탐색하는 것이고, Union-Find는 미로 지도를 가지고 "이 두 방이 연결되어 있나?"만 빠르게 답하는 것이다. 동적으로 연결이 추가되는 상황에서는 Union-Find가 훨씬 효율적이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무 시나리오: 네트워크 구성 요소 실시간 모니터링
```python
n = 1000000  # 1M 서버 노드
parent = list(range(n))
rank = [0] * n

# 새 링크 추가 시
def add_link(u, v):
    union(parent, rank, u, v)

# 두 서버 연결 여부 실시간 확인
def is_connected(u, v):
    return find(parent, u) == find(parent, v)

# 각 쿼리 O(α(n)) ≈ O(1) -> 1M 노드도 즉시 응답
```

#### 코딩 테스트 활용 패턴
- **사이클 검출**: 그래프에 간선 추가 시 Union-Find로 O(α(n))에 사이클 판별
- <strong>MST (크루스칼)</strong>: 간선 정렬 + Union-Find -> O(E log E)
- **최소 간선 연결**: N개 노드를 N-1개 간선으로 연결 + 사이클 없음 = Spanning Tree

- **📢 섹션 요약 비유**: Union-Find는 SNS의 팔로우 네트워크에서 두 사람이 같은 커뮤니티에 속하는지 즉시 확인하는 것이다. 친구 관계(간선)가 새로 생겨도 Union 한 번으로 업데이트하고, isConnected 한 번으로 같은 그룹인지 확인할 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **효율성** | 경로 압축+랭크 -> 거의 O(1) 연산 |
| <strong>MST</strong> | 크루스칼 알고리즘의 핵심 컴포넌트 |
| **동적 연결성** | 실시간 간선 추가 시 연결성 유지 |

Union-Find는 CPU 코어 할당(같은 소켓의 코어 그룹화), 파일 시스템의 아이노드 관리, 네트워크 라우팅 도메인 분리 등 대규모 시스템에서 폭넓게 활용된다.

- **📢 섹션 요약 비유**: Union-Find는 거대한 조직도를 관리하는 시스템이다. 팀 합병(Union)이 일어나도 누가 최고 책임자(루트)인지 즉시 확인(Find)할 수 있으며, 경로 압축으로 중간 단계를 건너뛰어 빠르게 정보를 얻는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>크루스칼 MST</strong> | Union-Find를 사이클 검출에 활용 |
| <strong>그래프 연결 요소</strong> | Union-Find로 O(V+E) -> O(V·α(n)) |
| <strong>경로 압축</strong> | Find 연산 최적화의 핵심 기법 |
| **아커만 역함수(α)** | 경로압축+랭크 시 실질적 상수 복잡도 |
| <strong>프림 알고리즘</strong> | MST 대안 (우선순위 큐 기반) |

### 📈 관련 키워드 및 발전 흐름도

```text
[기본 Union-Find — 루트 탐색 O(n)]
    |
    v
[경로 압축 (Path Compression) — O(log n)]
    |
    v
[랭크 기반 합집합 (Union by Rank) — O(log n)]
    |
    v
[경로 압축 + 랭크 — O(α(n)) ≈ O(1)]
    |
    v
[응용: 크루스칼 MST, 동적 연결성, 클러스터링]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Union-Find는 반 배정 시스템이에요! 학생들을 같은 반으로 묶고(Union), 특정 학생이 몇 반인지 빠르게 찾는(Find) 도구예요.
2. 처음에는 모두 각자 따로 있다가, 팀을 이룰 때마다 Union으로 합치고, 팀 대표(루트)를 경로 압축으로 기억해 빠르게 찾아요.
3. 이 도구 덕분에 수백만 개의 요소 사이에서 "이 둘이 같은 팀인가?"를 거의 즉시 답할 수 있답니다!
