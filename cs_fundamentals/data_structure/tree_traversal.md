# 자료구조: 트리와 트리 탐색 (Tree Data Structure & Tree Traversal)

## 📌 개요

**트리(Tree)**는 **노드(Node)**와 **간선(Edge)**으로 이루어진 계층적 자료구조로, 하나의 루트 노드(Root Node)에서 시작하여 자식 노드(Child Node)들이 가지처럼 뻗어나가는 비선형(Non-linear) 구조이다. 트리 탐색(Tree Traversal)은 트리의 모든 노드를 체계적으로 방문하는 방법을 의미한다.

---

## 1. 트리의 기본 용어

| 용어 | 영문 | 설명 |
|------|------|------|
| **노드 (Node)** | Node | 트리를 구성하는 기본 요소. 데이터와 다른 노드로의 연결 정보를 포함 |
| **루트 노드** | Root Node | 트리의 최상위 노드. 부모가 없는 유일한 노드 |
| **부모 노드** | Parent Node | 특정 노드의 바로 위에 연결된 노드 |
| **자식 노드** | Child Node | 특정 노드의 바로 아래에 연결된 노드 |
| **리프 노드** | Leaf Node (Terminal Node) | 자식이 없는 노드. 트리의 끝단 |
| **내부 노드** | Internal Node | 적어도 하나의 자식을 가진 노드 |
| **형제 노드** | Sibling Node | 같은 부모를 가진 노드들 |
| **간선** | Edge | 노드와 노드를 연결하는 선 |
| **깊이** | Depth | 루트 노드에서 특정 노드까지의 간선 수 |
| **높이** | Height | 특정 노드에서 리프 노드까지의 가장 긴 경로의 간선 수 |
| **레벨** | Level | 같은 깊이에 있는 노드들의 집합 (루트 = 레벨 0 또는 1) |
| **서브트리** | Subtree | 특정 노드를 루트로 하는 트리의 부분집합 |
| **차수** | Degree | 특정 노드의 자식 노드 개수 |

---

## 2. 트리의 종류

### 2.1 이진 트리 (Binary Tree)
각 노드가 **최대 2개의 자식 노드**를 가지는 트리

```
        1
       / \
      2   3
     / \
    4   5
```

### 2.2 완전 이진 트리 (CBT, Complete Binary Tree)
마지막 레벨을 제외한 모든 레벨이 완전히 채워져 있고, 마지막 레벨은 왼쪽부터 순서대로 채워진 트리

### 2.3 포화 이진 트리 (PBT, Perfect Binary Tree)
모든 내부 노드가 2개의 자식을 가지며, 모든 리프 노드가 같은 레벨에 있는 트리

### 2.4 이진 탐색 트리 (BST, Binary Search Tree)
**왼쪽 서브트리 < 부모 노드 < 오른쪽 서브트리** 규칙을 따르는 이진 트리

### 2.5 균형 트리 (Balanced Tree)
모든 리프 노드의 깊이 차이가 최소화된 트리
- **AVL 트리**: Adelson-Velsky and Landis가 제안한 자가 균형 이진 탐색 트리
- **레드-블랙 트리 (Red-Black Tree)**: 색상 규칙을 통해 균형을 유지하는 트리

### 2.6 B-트리 (B-Tree)
하나의 노드가 여러 개의 키를 가질 수 있는 균형 탐색 트리. 데이터베이스와 파일 시스템에서 주로 사용

---

## 3. 트리 탐색 방법 (Tree Traversal Methods)

트리 탐색은 크게 **깊이 우선 탐색 (DFS, Depth-First Search)**과 **너비 우선 탐색 (BFS, Breadth-First Search)**으로 나뉜다.

---

## 4. 깊이 우선 탐색 (DFS, Depth-First Search)

DFS는 한 경로를 끝까지 탐색한 후 다른 경로로 이동하는 방식이다. **스택(Stack)** 또는 **재귀(Recursion)**를 사용하여 구현한다.

### 4.1 전위 순회 (Preorder Traversal)
**방문 순서: 루트 → 왼쪽 서브트리 → 오른쪽 서브트리**

> 🎯 **용도**: 트리 복사, 트리 직렬화(Serialization)

```
        1
       / \
      2   3
     / \
    4   5

전위 순회 결과: 1 → 2 → 4 → 5 → 3
```

```python
def preorder(node):
    if node is None:
        return
    print(node.value)        # 루트 방문
    preorder(node.left)      # 왼쪽 서브트리
    preorder(node.right)     # 오른쪽 서브트리
```

### 4.2 중위 순회 (Inorder Traversal)
**방문 순서: 왼쪽 서브트리 → 루트 → 오른쪽 서브트리**

> 🎯 **용도**: 이진 탐색 트리(BST)에서 **오름차순 정렬** 결과 출력

```
        4
       / \
      2   6
     / \ / \
    1  3 5  7

중위 순회 결과: 1 → 2 → 3 → 4 → 5 → 6 → 7 (정렬된 순서!)
```

```python
def inorder(node):
    if node is None:
        return
    inorder(node.left)       # 왼쪽 서브트리
    print(node.value)        # 루트 방문
    inorder(node.right)      # 오른쪽 서브트리
```

### 4.3 후위 순회 (Postorder Traversal)
**방문 순서: 왼쪽 서브트리 → 오른쪽 서브트리 → 루트**

> 🎯 **용도**: 트리 삭제, 수식 트리 계산, 디렉토리 크기 계산

```
        1
       / \
      2   3
     / \
    4   5

후위 순회 결과: 4 → 5 → 2 → 3 → 1
```

```python
def postorder(node):
    if node is None:
        return
    postorder(node.left)     # 왼쪽 서브트리
    postorder(node.right)    # 오른쪽 서브트리
    print(node.value)        # 루트 방문
```

---

## 5. 너비 우선 탐색 (BFS, Breadth-First Search)

### 5.1 레벨 순회 (Level Order Traversal)
**방문 순서: 레벨 단위로 왼쪽에서 오른쪽으로 순차 방문**

**큐(Queue)**를 사용하여 구현하며, FIFO(First-In First-Out) 원칙을 따른다.

> 🎯 **용도**: 최단 경로 탐색, 레벨별 노드 처리

```
        1
       / \
      2   3
     / \   \
    4   5   6

레벨 순회 결과: 1 → 2 → 3 → 4 → 5 → 6
```

```python
from collections import deque

def level_order(root):
    if root is None:
        return
    
    queue = deque([root])
    
    while queue:
        node = queue.popleft()      # 큐에서 노드 꺼내기
        print(node.value)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

---

## 6. DFS vs BFS 비교

| 특성 | DFS (Depth-First Search) | BFS (Breadth-First Search) |
|------|--------------------------|---------------------------|
| **탐색 방식** | 깊이 우선 (한 경로 끝까지) | 너비 우선 (레벨 단위) |
| **자료구조** | 스택 (Stack) 또는 재귀 | 큐 (Queue) |
| **메모리 사용** | 트리 높이에 비례 O(h) | 트리 너비에 비례 O(w) |
| **최단 경로 보장** | ❌ 보장하지 않음 | ✅ 보장함 (가중치 없는 경우) |
| **적합한 상황** | 깊은 트리, 모든 경로 탐색 필요 | 얕은 트리, 최단 경로 탐색 |

---

## 7. 비유로 이해하기

> 🌳 **회사 조직도 비유**
>
> 트리는 회사 조직도와 같다.
> - **루트 노드**: CEO(Chief Executive Officer, 최고경영자)
> - **내부 노드**: 각 부서의 팀장
> - **리프 노드**: 일반 사원
> - **깊이**: 조직에서의 직급 단계

> 🏠 **집 청소 비유**
>
> - **DFS (전위/중위/후위 순회)**: 한 방을 완전히 청소한 후 다음 방으로 이동
> - **BFS (레벨 순회)**: 모든 방의 바닥을 먼저 쓸고, 그 다음 모든 방의 먼지를 닦기

---

## 8. 시간 및 공간 복잡도

모든 트리 탐색 방법은 **모든 노드를 한 번씩 방문**하므로:

| 복잡도 | DFS | BFS |
|--------|-----|-----|
| **시간 복잡도** | O(N) | O(N) |
| **공간 복잡도** | O(H) - 트리 높이 | O(W) - 트리 최대 너비 |

- **N**: 노드의 총 개수
- **H**: 트리의 높이 (Height)
- **W**: 트리의 최대 너비 (Width)

---

## 9. 순회 방법 선택 가이드

| 상황 | 권장 순회 방법 |
|------|---------------|
| 이진 탐색 트리에서 정렬된 데이터 출력 | **중위 순회 (Inorder)** |
| 트리 복사 또는 직렬화 | **전위 순회 (Preorder)** |
| 트리 삭제 또는 디렉토리 크기 계산 | **후위 순회 (Postorder)** |
| 최단 경로 탐색 (가중치 없음) | **레벨 순회 (BFS)** |
| 경로 존재 여부 확인 | **DFS (전위/중위/후위)** |

---

## 10. 정리

| 개념 | 핵심 내용 |
|------|----------|
| **트리** | 계층적 비선형 자료구조 |
| **전위 순회 (Preorder)** | 루트 → 왼쪽 → 오른쪽 |
| **중위 순회 (Inorder)** | 왼쪽 → 루트 → 오른쪽 (BST 정렬) |
| **후위 순회 (Postorder)** | 왼쪽 → 오른쪽 → 루트 (삭제 적합) |
| **레벨 순회 (Level Order)** | 레벨 단위 탐색 (BFS) |
| **DFS** | 스택/재귀 사용, 깊이 우선 |
| **BFS** | 큐 사용, 너비 우선, 최단 경로 보장 |

---

## 📚 참고 용어 (Full Forms)

- **DFS**: Depth-First Search (깊이 우선 탐색)
- **BFS**: Breadth-First Search (너비 우선 탐색)
- **BST**: Binary Search Tree (이진 탐색 트리)
- **CBT**: Complete Binary Tree (완전 이진 트리)
- **PBT**: Perfect Binary Tree (포화 이진 트리)
- **AVL**: Adelson-Velsky and Landis (자가 균형 이진 탐색 트리)
- **FIFO**: First-In First-Out (선입 선출)
- **CEO**: Chief Executive Officer (최고경영자)
