+++
title = "트리 (Tree)"
date = 2025-03-01

[extra]
categories = "algorithm_stats-data_structure"
+++

# 트리 (Tree)

## 핵심 인사이트 (3줄 요약)
> **계층적 구조를 표현하는 비선형 자료구조**. 루트, 노드, 간선으로 구성. 이진 트리, BST, AVL, 힙 등 다양한 변형 존재.

## 1. 개념
트리는 **노드(Node)들이 계층적으로 연결된 비선형 자료구조**로, 사이클이 없는 연결 그래프다.

> 비유: "조직도" - CEO(루트) 아래로 부서들이 계층적으로 배치

## 2. 트리 용어

```
┌────────────────────────────────────────────────────────┐
│                    트리 용어                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│               A (루트, 깊이 0, 레벨 1)                 │
│              ╱ ╲                                       │
│             ╱   ╲                                      │
│            B     C (깊이 1, 레벨 2)                    │
│           ╱ ╲     ╲                                    │
│          ╱   ╲     ╲                                   │
│         D     E     F (깊이 2, 레벨 3)                 │
│        ╱                                              │
│       G (깊이 3, 레벨 4)                               │
│                                                        │
│  루트(Root): 최상위 노드 (A)                           │
│  부모(Parent): 상위 노드 (B는 D, E의 부모)             │
│  자식(Child): 하위 노드 (D, E는 B의 자식)              │
│  형제(Sibling): 같은 부모 (D, E는 형제)                │
│  리프(Leaf): 자식이 없는 노드 (G, E, F)                │
│  깊이(Depth): 루트에서의 거리                          │
│  높이(Height): 리프에서의 거리 (A의 높이 = 3)          │
│  차수(Degree): 자식의 수 (A의 차수 = 2)                │
│  레벨(Level): 깊이 + 1                                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 트리 종류

```
┌────────────────────────────────────────────────────────┐
│                    트리 종류                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 이진 트리 (Binary Tree)                           │
│     - 각 노드가 최대 2개의 자식                        │
│     - 포화 이진 트리: 모든 레벨이 꽉 참               │
│     - 완전 이진 트리: 마지막 레벨 제외하고 꽉 참      │
│                                                        │
│  2. 이진 탐색 트리 (BST: Binary Search Tree)          │
│     - 왼쪽 자식 < 부모 < 오른쪽 자식                  │
│     - 탐색, 삽입, 삭제: O(log n) ~ O(n)               │
│                                                        │
│  3. 균형 트리                                          │
│     - AVL 트리: 회전으로 균형 유지                    │
│     - 레드-블랙 트리: 색상으로 균형 유지              │
│     - 항상 O(log n) 보장                              │
│                                                        │
│  4. 힙 (Heap)                                          │
│     - 최대 힙: 부모 ≥ 자식                            │
│     - 최소 힙: 부모 ≤ 자식                            │
│     - 우선순위 큐 구현                                 │
│                                                        │
│  5. B-트리                                             │
│     - 데이터베이스 인덱스                              │
│     - 디스크 기반 트리                                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 트리 순회

```
┌────────────────────────────────────────────────────────┐
│                    트리 순회                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│           트리 예시:                                   │
│               A                                        │
│              ╱ ╲                                       │
│             B   C                                      │
│            ╱ ╲                                         │
│           D   E                                        │
│                                                        │
│  1. 전위 순회 (Preorder): 루트 → 왼쪽 → 오른쪽        │
│     결과: A → B → D → E → C                           │
│                                                        │
│  2. 중위 순회 (Inorder): 왼쪽 → 루트 → 오른쪽         │
│     결과: D → B → E → A → C                           │
│                                                        │
│  3. 후위 순회 (Postorder): 왼쪽 → 오른쪽 → 루트       │
│     결과: D → E → B → C → A                           │
│                                                        │
│  4. 레벨 순회 (Level-order): 위에서 아래로, 왼→오     │
│     결과: A → B → C → D → E                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from dataclasses import dataclass
from typing import Optional, List, Callable
from collections import deque

@dataclass
class TreeNode:
    """트리 노드"""
    value: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None

class BinaryTree:
    """이진 트리"""

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def preorder(self, node: Optional[TreeNode] = None, result: List[int] = None) -> List[int]:
        """전위 순회"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result

        result.append(node.value)
        if node.left:
            self.preorder(node.left, result)
        if node.right:
            self.preorder(node.right, result)

        return result

    def inorder(self, node: Optional[TreeNode] = None, result: List[int] = None) -> List[int]:
        """중위 순회"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result

        if node.left:
            self.inorder(node.left, result)
        result.append(node.value)
        if node.right:
            self.inorder(node.right, result)

        return result

    def postorder(self, node: Optional[TreeNode] = None, result: List[int] = None) -> List[int]:
        """후위 순회"""
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result

        if node.left:
            self.postorder(node.left, result)
        if node.right:
            self.postorder(node.right, result)
        result.append(node.value)

        return result

    def level_order(self) -> List[int]:
        """레벨 순회"""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.value)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def height(self, node: Optional[TreeNode] = None) -> int:
        """높이 계산"""
        if node is None:
            node = self.root
        if node is None:
            return 0

        left_height = self.height(node.left) if node.left else 0
        right_height = self.height(node.right) if node.right else 0

        return max(left_height, right_height) + 1

class BinarySearchTree:
    """이진 탐색 트리"""

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def insert(self, value: int):
        """삽입"""
        if not self.root:
            self.root = TreeNode(value)
            return

        def _insert(node: TreeNode, value: int):
            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value)
                else:
                    _insert(node.left, value)
            else:
                if node.right is None:
                    node.right = TreeNode(value)
                else:
                    _insert(node.right, value)

        _insert(self.root, value)

    def search(self, value: int) -> bool:
        """탐색"""
        def _search(node: Optional[TreeNode], value: int) -> bool:
            if node is None:
                return False
            if node.value == value:
                return True
            if value < node.value:
                return _search(node.left, value)
            return _search(node.right, value)

        return _search(self.root, value)

    def delete(self, value: int):
        """삭제"""
        def _min_value_node(node: TreeNode) -> TreeNode:
            current = node
            while current.left:
                current = current.left
            return current

        def _delete(node: Optional[TreeNode], value: int) -> Optional[TreeNode]:
            if node is None:
                return None

            if value < node.value:
                node.left = _delete(node.left, value)
            elif value > node.value:
                node.right = _delete(node.right, value)
            else:
                # 삭제할 노드 찾음
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                # 두 자식이 있는 경우
                min_node = _min_value_node(node.right)
                node.value = min_node.value
                node.right = _delete(node.right, min_node.value)

            return node

        self.root = _delete(self.root, value)

    def inorder(self) -> List[int]:
        """중위 순회 (정렬된 순서)"""
        result = []

        def _inorder(node: Optional[TreeNode]):
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)

        _inorder(self.root)
        return result


# 사용 예시
print("=== 트리 알고리즘 시연 ===\n")

# 이진 트리
print("--- 이진 트리 순회 ---")
bt = BinaryTree()
bt.root = TreeNode('A')
bt.root.left = TreeNode('B')
bt.root.right = TreeNode('C')
bt.root.left.left = TreeNode('D')
bt.root.left.right = TreeNode('E')

print(f"전위 순회: {bt.preorder()}")
print(f"중위 순회: {bt.inorder()}")
print(f"후위 순회: {bt.postorder()}")
print(f"레벨 순회: {bt.level_order()}")
print(f"높이: {bt.height()}")

# 이진 탐색 트리
print("\n--- 이진 탐색 트리 ---")
bst = BinarySearchTree()
for val in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(val)

print(f"중위 순회 (정렬): {bst.inorder()}")
print(f"30 검색: {bst.search(30)}")
print(f"100 검색: {bst.search(100)}")

bst.delete(30)
print(f"30 삭제 후: {bst.inorder()}")
