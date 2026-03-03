+++
title = "B-Tree와 B+ Tree - 데이터베이스 인덱스의 핵심"
date = 2026-03-03

[extra]
categories = "pe_exam-algorithm_stats"
+++

# B-Tree와 B+ Tree - 데이터베이스 인덱스의 핵심

## 핵심 인사이트 (3줄 요약)
> **B-Tree**는 디스크 I/O를 최소화하는 균형 다원 탐색 트리로, 노드당 여러 키를 저장해 높이를 낮춘다. **B+ Tree**는 데이터를 리프 노드에만 저장하고 연결 리스트로 연결해 범위 검색에 최적화되어 있다. 현대 데이터베이스(MySQL, PostgreSQL)의 인덱스 표준은 B+ Tree다.

---

### Ⅰ. 개요

**개념**: B-Tree(Balanced Tree)는 **모든 리프 노드가 동일한 깊이를 갖는 균형 다원 탐색 트리(Balanced Multi-way Search Tree)**로, 노드당 여러 개의 키를 저장하여 디스크 I/O를 최소화한다.

> 💡 **비유**: "도서관의 색인 카드" — 큰 분류(노드) → 중간 분류 → 실제 책(리프)으로 계층적 탐색

**등장 배경**:
1. **기존 문제점**: BST는 최악 O(n), AVL/레드블랙은 메모리 기반에 적합, 디스크에서 높이가 높아 I/O 많음
2. **기술적 필요성**: 대용량 데이터베이스에서 디스크 블록 단위 I/O 최소화, 범위 검색 효율
3. **시장/산업 요구**: RDBMS 인덱스, 파일 시스템, 검색 엔진의 핵심 자료구조

**핵심 목적**: 디스크 기반 대용량 데이터의 O(log n) 탐색, 삽입, 삭제 보장

---

### Ⅱ. 구성 요소 및 핵심 원리

**B-Tree 구성 요소**:
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **M차** | 노드의 최대 자식 수 | 높이 = log_M(N) | 색인 단계 |
| **내부 노드** | 키와 자식 포인터 | M/2 ~ M개 자식 | 중간 분류 |
| **리프 노드** | 실제 데이터/포인터 | 같은 깊이 | 실제 책 |
| **분할(Split)** | 노드 오버플로우 시 | 중간 키 승진 | 새 색인 생성 |
| **병합(Merge)** | 노드 언더플로우 시 | 형제와 결합 | 색인 통합 |

**B-Tree vs B+ Tree 비교**:
| 항목 | B-Tree | ★ B+ Tree |
|------|--------|----------|
| 데이터 저장 | 모든 노드 | ★ 리프 노드만 |
| 리프 연결 | 없음 | ★ 연결 리스트 |
| 범위 검색 | 비효율 | ★ 매우 효율 |
| 노드 활용 | 낮음 | ★ 높음 (더 많은 키) |
| 트리 높이 | 상대적 높음 | ★ 낮음 |
| DB 사용 | 제한적 | ★ MySQL, PostgreSQL |

**구조 다이어그램**:
```
    B-Tree 구조 (M=3, 2-3 트리)
    ┌─────────────────────────────────────────────────────────────┐
    │                         [30 | 60]                           │
    │                       /    |     \                          │
    │                    /       |       \                        │
    │               [10|20]   [40|50]   [70|80|90]                │
    │                                                             │
    │  - 모든 노드에 키와 데이터                                   │
    │  - 리프 간 연결 없음                                         │
    │  - 범위 검색 시 트리 여러 번 왕복                             │
    └─────────────────────────────────────────────────────────────┘

    B+ Tree 구조 (M=3)
    ┌─────────────────────────────────────────────────────────────┐
    │                      [30 | 60] (인덱스만)                    │
    │                    /     |     \                            │
    │                 /        |       \                          │
    │           [10|20] → [40|50] → [70|80|90]                    │
    │            ↑           ↑           ↑                        │
    │          데이터       데이터       데이터                     │
    │                                                             │
    │  - 리프 노드에만 실제 데이터                                  │
    │  - 리프 간 연결 리스트 (← →)                                 │
    │  - 범위 검색: 리프만 순차 탐색                                │
    └─────────────────────────────────────────────────────────────┘

    B+ Tree 리프 노드 연결 (범위 검색 최적화)
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  [10|20] ←→ [30|40] ←→ [50|60] ←→ [70|80]                  │
    │                                                             │
    │  WHERE id BETWEEN 30 AND 70                                 │
    │  → [30|40] → [50|60] → [70|80] 시작점에서만 트리 탐색!       │
    │  → 나머지는 연결 리스트 따라 순차 읽기                       │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    B-Tree 노드 분할 (Split)
    ┌─────────────────────────────────────────────────────────────┐
    │  4차 B-Tree에 35 삽입 시 오버플로우                          │
    │                                                             │
    │  분할 전: [20 | 30 | 40 | 50 | 60]  ← 최대 4개인데 5개!      │
    │                                                             │
    │  분할 과정:                                                 │
    │  1. 중간 키 40을 부모로 승진                                 │
    │  2. 좌측: [20 | 30], 우측: [50 | 60]                        │
    │  3. 35는 좌측에 삽입: [20 | 30 | 35]                        │
    │                                                             │
    │              [40]          ← 승진                           │
    │              /   \                                         │
    │        [20|30|35] [50|60]                                  │
    └─────────────────────────────────────────────────────────────┘
```

**동작 원리**:
```
① 탐색: 루트 시작 → ② 키 범위 탐색 → ③ 자식 이동 → ④ 리프 도달
① 삽입: 리프 찾기 → ② 키 삽입 → ③ 오버플로우 시 분할 → ④ 부모로 전파
① 삭제: 키 찾기 → ② 삭제 → ③ 언더플로우 시 병합/재분배 → ④ 부모로 전파
```

**핵심 알고리즘/공식**:
```
B-Tree 차수(M) 특성:
  - 루트: 2 ~ M개 자식 (리프 제외 최소 2)
  - 내부 노드: ⌈M/2⌉ ~ M개 자식
  - 리프 노드: ⌈M/2⌉ ~ M개 키

B+ Tree 팬아웃(Fan-out):
  - 노드에 데이터 없이 키만 → 더 많은 키 저장
  - 높이 감소 = 디스크 I/O 감소

시간복잡도 (M차 B-Tree, N개 키):
  - 탐색: O(log_M N) = O(h), h = 트리 높이
  - 삽입: O(log_M N) + 분할 비용
  - 삭제: O(log_M N) + 병합/재분배 비용

디스크 I/O:
  - 높이 = ⌈log_M N⌉
  - 1억 개 키, M=100 → 높이 약 3~4
  - 즉, 3~4번의 디스크 읽기로 1억 개 중 하나 찾음!
```

**코드 예시 (Python)**:
```python
"""
B-Tree와 B+ Tree 구현
- 탐색, 삽입, 삭제 연산
- 노드 분할 및 병합
"""
from typing import List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class BTreeNode:
    """B-Tree 노드"""
    keys: List[int] = field(default_factory=list)
    children: List['BTreeNode'] = field(default_factory=list)
    is_leaf: bool = True

    def is_full(self, order: int) -> bool:
        """노드가 가득 찼는지 확인"""
        return len(self.keys) >= order - 1

    def find_key_index(self, key: int) -> int:
        """키가 들어갈 위치 찾기"""
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        return idx


class BTree:
    """
    B-Tree 구현
    - M차 B-Tree (order = M)
    - 탐색, 삽입, 삭제
    """
    def __init__(self, order: int = 4):
        self.order = order  # M차
        self.root: Optional[BTreeNode] = BTreeNode()
        self.min_keys = order // 2  # 최소 키 개수

    def search(self, key: int) -> Tuple[Optional[BTreeNode], int]:
        """키 탐색 - O(log n)"""
        return self._search_node(self.root, key)

    def _search_node(self, node: Optional[BTreeNode], key: int) -> Tuple[Optional[BTreeNode], int]:
        if node is None:
            return None, -1

        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1

        # 키 발견
        if idx < len(node.keys) and key == node.keys[idx]:
            return node, idx

        # 리프 노드면 종료
        if node.is_leaf:
            return None, -1

        # 자식 노드로 이동
        return self._search_node(node.children[idx], key)

    def insert(self, key: int) -> None:
        """키 삽입 - O(log n)"""
        root = self.root

        # 루트가 가득 찼으면 분할
        if root.is_full(self.order):
            new_root = BTreeNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node: BTreeNode, key: int) -> None:
        """가득 차지 않은 노드에 삽입"""
        idx = len(node.keys) - 1

        if node.is_leaf:
            # 리프 노드: 키 삽입
            node.keys.append(0)
            while idx >= 0 and key < node.keys[idx]:
                node.keys[idx + 1] = node.keys[idx]
                idx -= 1
            node.keys[idx + 1] = key
        else:
            # 내부 노드: 자식 찾기
            while idx >= 0 and key < node.keys[idx]:
                idx -= 1
            idx += 1

            # 자식이 가득 찼으면 분할
            if node.children[idx].is_full(self.order):
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    idx += 1

            self._insert_non_full(node.children[idx], key)

    def _split_child(self, parent: BTreeNode, idx: int) -> None:
        """자식 노드 분할"""
        order = self.order
        child = parent.children[idx]
        mid = len(child.keys) // 2

        # 새 노드 생성
        new_node = BTreeNode(is_leaf=child.is_leaf)

        # 중간 키를 부모로 승진
        mid_key = child.keys[mid]
        parent.keys.insert(idx, mid_key)
        parent.children.insert(idx + 1, new_node)

        # 키 분배
        new_node.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]

        # 자식 분배 (내부 노드인 경우)
        if not child.is_leaf:
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

    def delete(self, key: int) -> bool:
        """키 삭제 - O(log n)"""
        if self.root is None:
            return False

        self._delete_from_node(self.root, key)

        # 루트가 비었으면 자식을 루트로
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]

        return True

    def _delete_from_node(self, node: BTreeNode, key: int) -> None:
        """노드에서 키 삭제"""
        idx = node.find_key_index(key)

        # 키가 현재 노드에 있음
        if idx < len(node.keys) and node.keys[idx] == key:
            if node.is_leaf:
                # 리프: 그냥 삭제
                node.keys.pop(idx)
            else:
                # 내부: 전임자 또는 후임자로 교체
                self._delete_internal(node, idx)
        else:
            # 키가 자식에 있음
            if node.is_leaf:
                return  # 키 없음

            # 자식이 최소 키면 채워주기
            if len(node.children[idx].keys) < self.min_keys:
                self._fill_child(node, idx)

            # 재귀 삭제
            self._delete_from_node(node.children[idx], key)

    def _delete_internal(self, node: BTreeNode, idx: int) -> None:
        """내부 노드에서 키 삭제"""
        key = node.keys[idx]

        # 전임자 사용
        if len(node.children[idx].keys) >= self.min_keys:
            pred = self._get_predecessor(node.children[idx])
            node.keys[idx] = pred
            self._delete_from_node(node.children[idx], pred)
        # 후임자 사용
        elif len(node.children[idx + 1].keys) >= self.min_keys:
            succ = self._get_successor(node.children[idx + 1])
            node.keys[idx] = succ
            self._delete_from_node(node.children[idx + 1], succ)
        # 둘 다 최소면 병합
        else:
            self._merge_nodes(node, idx)
            self._delete_from_node(node.children[idx], key)

    def _get_predecessor(self, node: BTreeNode) -> int:
        """전임자 (왼쪽 서브트리 최댓값)"""
        while not node.is_leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_successor(self, node: BTreeNode) -> int:
        """후임자 (오른쪽 서브트리 최솟값)"""
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]

    def _fill_child(self, node: BTreeNode, idx: int) -> None:
        """최소 키 미만인 자식 채우기"""
        if idx > 0 and len(node.children[idx - 1].keys) >= self.min_keys:
            self._borrow_from_prev(node, idx)
        elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) >= self.min_keys:
            self._borrow_from_next(node, idx)
        else:
            if idx < len(node.children) - 1:
                self._merge_nodes(node, idx)
            else:
                self._merge_nodes(node, idx - 1)

    def _borrow_from_prev(self, node: BTreeNode, idx: int) -> None:
        """이전 형제에서 빌려오기"""
        child = node.children[idx]
        sibling = node.children[idx - 1]

        child.keys.insert(0, node.keys[idx - 1])
        node.keys[idx - 1] = sibling.keys.pop()

        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node: BTreeNode, idx: int) -> None:
        """다음 형제에서 빌려오기"""
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys.append(node.keys[idx])
        node.keys[idx] = sibling.keys.pop(0)

        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))

    def _merge_nodes(self, node: BTreeNode, idx: int) -> None:
        """두 자식 노드 병합"""
        child = node.children[idx]
        sibling = node.children[idx + 1]

        # 부모 키 가져오기
        child.keys.append(node.keys[idx])
        child.keys.extend(sibling.keys)

        if not child.is_leaf:
            child.children.extend(sibling.children)

        # 부모에서 키와 자식 제거
        node.keys.pop(idx)
        node.children.pop(idx + 1)

    def traverse(self) -> List[int]:
        """중위 순회"""
        result = []

        def _traverse(node: Optional[BTreeNode]):
            if node is None:
                return
            for i, key in enumerate(node.keys):
                if not node.is_leaf:
                    _traverse(node.children[i])
                result.append(key)
            if not node.is_leaf:
                _traverse(node.children[-1])

        _traverse(self.root)
        return result


# ============== 실행 예시 ==============

if __name__ == "__main__":
    print("=" * 60)
    print(" B-Tree (4차) 연산")
    print("=" * 60)

    btree = BTree(order=4)

    # 삽입
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    print("\n[삽입]")
    for key in keys:
        btree.insert(key)
        print(f"  {key} 삽입 후: {btree.traverse()}")

    # 탐색
    print("\n[탐색]")
    for key in [6, 17, 100]:
        node, idx = btree.search(key)
        if node:
            print(f"  {key}: 찾음 (인덱스 {idx})")
        else:
            print(f"  {key}: 없음")

    # 삭제
    print("\n[삭제]")
    for key in [6, 17, 10]:
        btree.delete(key)
        print(f"  {key} 삭제 후: {btree.traverse()}")

    print("\n" + "=" * 60)
    print(" B-Tree vs B+ Tree 특징")
    print("=" * 60)
    print("""
  B-Tree:
    ✓ 모든 노드에 데이터 저장
    ✓ 단일 검색에 유리 (루트에서 찾을 수도)
    ✗ 범위 검색 비효율

  B+ Tree (DB 표준):
    ✓ 리프 노드에만 데이터 저장
    ✓ 리프 간 연결 리스트 → 범위 검색 O(n)
    ✓ 인덱스 노드에 더 많은 키 → 높이 낮음
    ✓ 모든 검색이 리프까지 → 일정한 응답 시간

  데이터베이스 선택:
    - MySQL InnoDB: B+ Tree
    - PostgreSQL: B+ Tree (BTree 인덱스)
    - MongoDB: B-Tree 변형
    """)
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석 (B+ Tree)**:
| 장점 (B+ Tree) | 단점 (B+ Tree) |
|---------------|----------------|
| ★ 범위 검색 효율 (연결 리스트) | 단일 검색 시 항상 리프까지 |
| ★ 높이 낮음 (더 많은 키) | 리프 노드 중복 키 저장 |
| ★ 일정한 검색 시간 | 구현 복잡도 높음 |
| ★ 디스크 I/O 최소화 | — |

**대안 기술 비교**:
| 비교 항목 | BST/AVL | 해시 | ★ B+ Tree | LSM Tree |
|---------|---------|------|----------|----------|
| 범위 검색 | O | X | ★ O | O |
| 디스크 친화 | X | X | ★ O | ★ O |
| 쓰기 성능 | O(n log n) | O(1) | O(log n) | ★ O(1) |
| 읽기 성능 | O(log n) | ★ O(1) | ★ O(log n) | O(log n) |
| DB 사용 | X | 제한적 | ★ RDBMS | NoSQL |

> **★ 선택 기준**: 범위 검색 + 디스크 저장 → B+ Tree, 쓰기 많음 → LSM Tree, 단일 키 검색 → 해시

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **RDBMS 인덱스** | 기본 키, 보조 인덱스 | 쿼리 응답 99% 단축 |
| **파일 시스템** | 디렉토리 구조 | 파일 검색 O(log n) |
| **검색 엔진** | 역인덱스 저장 | 검색 속도 100배 향상 |
| **캐시** | 범위 캐시 | 메모리 효율 50% 향상 |

**실제 도입 사례**:
- **MySQL InnoDB**: B+ Tree로 PK/인덱스 저장 — 페이지 크기 16KB, 높이 3~4로 수백만 레코드 관리
- **PostgreSQL**: BTree 인덱스 — MVCC와 결합하여 동시성 제어
- **NTFS/HFS+**: 파일 시스템 메타데이터 — B+ Tree 변형

**도입 시 고려사항**:
1. **기술적**: 차수(M) 선택, 페이지 크기, 버퍼 풀 크기
2. **운영적**: 인덱스 재구성, 조각 모음, 통계 갱신
3. **보안적**: 인덱스 정보 유출 방지
4. **경제적**: 인덱스 저장 공간 vs 검색 성능 트레이드오프

**주의사항 / 흔한 실수**:
- ❌ 과도한 인덱스 생성 (쓰기 성능 저하)
- ❌ 선택도 낮은 컬럼 인덱싱 (효과 미미)
- ❌ 인덱스 컬럼 순서 무시 (복합 인덱스)

**관련 개념 / 확장 학습**:
```
📌 B-Tree 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  B-Tree 핵심 연관 개념 맵                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [이진 탐색 트리] ←──→ [B-Tree] ←──→ [데이터베이스]            │
│          ↓              ↓                ↓                      │
│   [균형 트리]       [B+ Tree]        [인덱스]                   │
│          ↓              ↓                ↓                      │
│   [AVL/레드블랙]    [LSM Tree]       [쿼리 최적화]               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 이진 탐색 트리 | 선행 개념 | B-Tree의 기반 | `[tree](./tree.md)` |
| 인덱싱 | 핵심 응용 | DB 인덱스 | `[indexing](../../05_database/indexing.md)` |
| LSM Tree | 대안 기술 | 쓰기 최적화 | — |
| 힙 | 관련 구조 | 우선순위 큐 | `[heap](./heap.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 검색 성능 | O(log_M N) 탐색 | 1억 건에서 3~4회 I/O |
| 범위 검색 | 연결 리스트 활용 | 순차 읽기 최적화 |
| 디스크 효율 | 높이 최소화 | I/O 90% 감소 |

**미래 전망**:
1. **기술 발전 방향**: NVMe SSD 최적화, 학습형 인덱스(Learned Index)
2. **시장 트렌드**: 분산 B-Tree, column-store 인덱스
3. **후속 기술**: Adaptive Radix Tree, Masstree

> **결론**: B+ Tree는 디스크 기반 대용량 데이터베이스 인덱스의 표준으로, 범위 검색 효율성과 낮은 트리 높이로 인해 RDBMS의 핵심 자료구조다. B-Tree와 B+ Tree의 차이점과 분할/병합 과정의 완벽한 이해가 기술사의 필수 역량이다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms' Ch.18, MySQL InnoDB Documentation, PostgreSQL Index Types

---

## 어린이를 위한 종합 설명

**B-Tree는 마치 "거대한 도서관의 색인 카드 시스템"과 같아!**

```
상상해보세요:
  도서관에 책이 1억 권 있어요! 어떻게 빨리 찾을까요?

  📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚
```

**이진 탐색 트리 (책장 하나씩 확인)**:
```
  책 하나를 열어보고 → 왼쪽인가 오른쪽인가?
  → 너무 많이 내려가야 해요! 😫
```

**B-Tree (색인 카드 사용)**:
```
           [30 | 60 | 90]
          /    |    |    \
    [10|20] [40|50] [70|80] [100|110]
     ↓       ↓       ↓        ↓
    책장    책장    책장     책장

  1. "내 책은 50번이야!" → 30~60 사이로!
  2. [40|50] 카드에서 50 찾았어요!
  3. 딱 2번만에 찾았어요! 😊
```

**B+ Tree (더 똑똑한 방법)**:
```
           [30 | 60 | 90] (안내판만!)

    [10|20] ←→ [40|50] ←→ [70|80] ←→ [100|110]
     ↓         ↓         ↓          ↓
    📚📚      📚📚      📚📚       📚📚
   (실제책)   (실제책)   (실제책)    (실제책)

  장점:
  1. 안내판에 책 정보가 없어서 더 많은 번호를 쓸 수 있어요!
  2. "30번부터 80번까지 보여줘!" → 화살표(←→) 따라 쭉 가면 돼요!

  → 도서관 사서 아저씨들이 B+ Tree를 좋아해요! 📖✨
```

**비밀**: 데이터베이스도 똑같아요! 1억 개 데이터를 3~4번만에 찾아요! 🔍
