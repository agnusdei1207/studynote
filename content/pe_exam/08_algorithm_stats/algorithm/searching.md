+++
title = "탐색 알고리즘 (Searching Algorithms)"
date = 2026-03-03

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 탐색 알고리즘 (Searching Algorithms)

## 핵심 인사이트 (3줄 요약)
> **탐색**은 데이터 집합에서 특정 값이나 조건을 만족하는 요소를 찾는 알고리즘이다. **이진 탐색**은 정렬된 데이터에서 O(log n)의 효율성을 보이며, **해시 테이블**은 평균 O(1)로 가장 빠르다. 데이터 구조와 검색 패턴에 따라 최적의 알고리즘을 선택해야 한다.

---

### Ⅰ. 개요

**개념**: 탐색 알고리즘(Searching Algorithm)은 **데이터 집합에서 특정 값, 조건, 또는 패턴을 만족하는 요소(들)를 찾는 알고리즘**이다.

> 💡 **비유**: "도서관에서 책 찾기" — 정리된 도서관(정렬)에서는 번호표를 따라 빠르게 찾지만, 엉망인 방(비정렬)에서는 하나하나 뒤져야 한다.

**등장 배경**:
1. **기존 문제점**: 대용량 데이터에서 선형 탐색 O(n)의 비효율성
2. **기술적 필요성**: 실시간 검색, DB 인덱싱, 자동완성 등 빠른 데이터 접근 요구
3. **시장/산업 요구**: 검색 엔진, 추천 시스템, 로그 분석의 핵심 기술

**핵심 목적**: 최소 비용으로 원하는 데이터의 존재 여부 확인 및 위치 파악

---

### Ⅱ. 구성 요소 및 핵심 원리

**탐색 알고리즘 분류**:
| 구분 | 알고리즘 | 시간복잡도 | 조건 | 특징 |
|------|----------|-----------|------|------|
| **배열 기반** | 선형 탐색 | O(n) | 없음 | 단순, 범용 |
| **배열 기반** | 이진 탐색 | O(log n) | 정렬됨 | 빠름, 전제조건 |
| **트리 기반** | BST 탐색 | O(log n)~O(n) | 트리 | 동적 삽입/삭제 |
| **트리 기반** | B-트리 | O(log n) | 트리 | DB 인덱스 |
| **해시 기반** | 해시 테이블 | O(1) 평균 | 해시함수 | 최고 성능 |
| **문자열** | KMP | O(n+m) | 패턴 | 부분 일치 |

**구조 다이어그램**:
```
                탐색 알고리즘 분류
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │   ┌─────────────────────────────────────────────────┐ │
    │   │              선형 탐색 (Linear Search)          │ │
    │   │  [3][7][1][9][4][2][8][5][6] → 순차적 비교      │ │
    │   │   ↑                              O(n)           │ │
    │   │   찾는 값: 8                                    │ │
    │   └─────────────────────────────────────────────────┘ │
    │                                                        │
    │   ┌─────────────────────────────────────────────────┐ │
    │   │              이진 탐색 (Binary Search)          │ │
    │   │  [1][2][3][4][5][6][7][8][9] → 정렬 필수        │ │
    │   │           ↑        ↑        ↑   O(log n)        │ │
    │   │          low      mid      high                 │ │
    │   │   mid=5, 8>5 → 오른쪽 탐색                      │ │
    │   └─────────────────────────────────────────────────┘ │
    │                                                        │
    │   ┌─────────────────────────────────────────────────┐ │
    │   │              해시 탐색 (Hash Search)            │ │
    │   │  key: "apple" → hash("apple") = 3 → bucket[3]   │ │
    │   │                                                  │ │
    │   │  bucket[0]:                                      │ │
    │   │  bucket[1]: ("cat", value1)                     │ │
    │   │  bucket[2]:                                      │ │
    │   │  bucket[3]: ("apple", value2) ← O(1) 평균       │ │
    │   │  bucket[4]: ("dog", value3)                     │ │
    │   └─────────────────────────────────────────────────┘ │
    │                                                        │
    └────────────────────────────────────────────────────────┘

    이진 탐색 트리 (BST) 탐색 과정
    ┌─────────────────────────────────────────────────────────┐
    │                      [8]                                │
    │                    /     \                              │
    │                 [3]       [10]                          │
    │                /   \        \                           │
    │             [1]   [6]      [14]                         │
    │                  /   \                                 │
    │               [4]   [7]                                │
    │                                                         │
    │  찾는 값: 6                                             │
    │  ① 8과 비교: 6 < 8 → 왼쪽                              │
    │  ② 3과 비교: 6 > 3 → 오른쪽                            │
    │  ③ 6과 비교: 6 = 6 → 찾음! (3단계)                      │
    └─────────────────────────────────────────────────────────┘
```

**동작 원리**:
```
① 선형 탐색: 처음부터 → ② 순차 비교 → ③ 찾거나 끝까지 → ④ 결과 반환
① 이진 탐색: 중간값 비교 → ② 범위 축소 → ③ 반복 → ④ 찾거나 범위 소진
① 해시 탐색: 키 해싱 → ② 버킷 접근 → ③ 충돌 처리 → ④ 값 반환
① BST 탐색: 루트 비교 → ② 좌/우 선택 → ③ 재귀 → ④ 찾거나 리프 도달
```

**핵심 알고리즘/공식**:
```
이진 탐색 불변식 (Loop Invariant):
  - arr[low..mid-1] < target < arr[mid+1..high]
  - 탐색 범위가 반씩 줄어듦: n → n/2 → n/4 → ... → 1
  - 최대 비교 횟수: ⌈log₂(n+1)⌉

해시 함수 요구사항:
  - 결정성: 같은 키 → 같은 해시값
  - 균등 분포: 해시값이 버킷에 고르게 분산
  - 효율성: O(1) 계산

해시 충돌 해결:
  - 체이닝 (Chaining): 연결 리스트로 충돌 원소 연결
  - 오픈 어드레싱 (Open Addressing): 다른 버킷 탐색 (선형/이차/이중해싱)
```

**코드 예시 (Python)**:
```python
"""
탐색 알고리즘 구현
- 선형 탐색: O(n)
- 이진 탐색: O(log n)
- 해시 테이블: O(1) 평균
- 이진 탐색 트리: O(log n) 평균
- 문자열 탐색: KMP, 보이어-무어
"""
from typing import List, Optional, Any, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')


# ============== 선형 탐색 ==============

def linear_search(arr: List[T], target: T) -> int:
    """
    선형 탐색 (Linear Search)
    - 처음부터 끝까지 순차적 비교
    - 시간복잡도: O(n)
    - 정렬 불필요, 범용적
    """
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1  # 찾지 못함


# ============== 이진 탐색 ==============

def binary_search(arr: List[T], target: T) -> int:
    """
    이진 탐색 (Binary Search)
    - 정렬된 배열에서 범위를 반씩 줄여가며 탐색
    - 시간복잡도: O(log n)
    - 전제조건: 배열이 정렬되어 있어야 함
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1  # 찾지 못함


def binary_search_recursive(arr: List[T], target: T,
                            low: int = 0, high: int = None) -> int:
    """이진 탐색 (재귀 버전)"""
    if high is None:
        high = len(arr) - 1

    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


def lower_bound(arr: List[T], target: T) -> int:
    """
    Lower Bound: target 이상인 첫 번째 원소의 인덱스
    - 삽입 위치 찾기에 활용
    """
    low, high = 0, len(arr)

    while low < high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid

    return low


def upper_bound(arr: List[T], target: T) -> int:
    """
    Upper Bound: target 초과인 첫 번째 원소의 인덱스
    - 범위 개수 계산에 활용
    """
    low, high = 0, len(arr)

    while low < high:
        mid = (low + high) // 2
        if arr[mid] <= target:
            low = mid + 1
        else:
            high = mid

    return low


# ============== 해시 테이블 ==============

@dataclass
class HashNode(Generic[T]):
    """해시 노드 (체이닝용)"""
    key: str
    value: T
    next: Optional['HashNode[T]'] = None


class HashTable(Generic[T]):
    """
    해시 테이블 (Hash Table)
    - 체이닝(Chaining)으로 충돌 해결
    - 평균 O(1), 최악 O(n)
    """
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.buckets: List[Optional[HashNode[T]]] = [None] * capacity

    def _hash(self, key: str) -> int:
        """해시 함수 (간단한 다항 해싱)"""
        hash_value = 0
        for i, char in enumerate(key):
            hash_value += ord(char) * (31 ** i)
        return hash_value % self.capacity

    def put(self, key: str, value: T) -> None:
        """키-값 쌍 삽입/갱신"""
        index = self._hash(key)
        node = self.buckets[index]

        # 기존 키 찾기
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        # 새 노드 삽입 (헤드에)
        new_node = HashNode(key, value, self.buckets[index])
        self.buckets[index] = new_node
        self.size += 1

        # 리해싱 필요시 확장
        if self.size > self.capacity * 0.75:
            self._resize()

    def get(self, key: str) -> Optional[T]:
        """키로 값 조회"""
        index = self._hash(key)
        node = self.buckets[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        return None

    def remove(self, key: str) -> bool:
        """키 삭제"""
        index = self._hash(key)
        node = self.buckets[index]
        prev = None

        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next

        return False

    def _resize(self) -> None:
        """버킷 확장 (리해싱)"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for node in old_buckets:
            while node:
                self.put(node.key, node.value)
                node = node.next


# ============== 이진 탐색 트리 ==============

@dataclass
class BSTNode(Generic[T]):
    """BST 노드"""
    key: T
    left: Optional['BSTNode[T]'] = None
    right: Optional['BSTNode[T]'] = None


class BinarySearchTree(Generic[T]):
    """
    이진 탐색 트리 (Binary Search Tree)
    - 평균 O(log n), 최악 O(n) (편향 트리)
    - 동적 삽입/삭제에 유리
    """
    def __init__(self):
        self.root: Optional[BSTNode[T]] = None

    def insert(self, key: T) -> None:
        """키 삽입"""
        if self.root is None:
            self.root = BSTNode(key)
            return

        def _insert(node: BSTNode[T], key: T) -> BSTNode[T]:
            if key < node.key:
                if node.left is None:
                    node.left = BSTNode(key)
                else:
                    _insert(node.left, key)
            elif key > node.key:
                if node.right is None:
                    node.right = BSTNode(key)
                else:
                    _insert(node.right, key)
            # 중복 키는 무시
            return node

        _insert(self.root, key)

    def search(self, key: T) -> bool:
        """키 검색"""
        def _search(node: Optional[BSTNode[T]], key: T) -> bool:
            if node is None:
                return False
            if key == node.key:
                return True
            elif key < node.key:
                return _search(node.left, key)
            else:
                return _search(node.right, key)

        return _search(self.root, key)

    def inorder(self) -> List[T]:
        """중위 순회 (정렬된 순서)"""
        result: List[T] = []

        def _inorder(node: Optional[BSTNode[T]]):
            if node:
                _inorder(node.left)
                result.append(node.key)
                _inorder(node.right)

        _inorder(self.root)
        return result


# ============== 문자열 탐색 ==============

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    KMP 알고리즘 (Knuth-Morris-Pratt)
    - 실패 함수(LPS)로 불필요한 비교 건너뜀
    - 시간복잡도: O(n + m)
    """
    if not pattern:
        return []

    # LPS (Longest Proper Prefix which is also Suffix) 계산
    def compute_lps(pattern: str) -> List[int]:
        m = len(pattern)
        lps = [0] * m
        length = 0  # 이전 LPS 길이

        for i in range(1, m):
            while length > 0 and pattern[i] != pattern[length]:
                length = lps[length - 1]

            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length

        return lps

    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    result = []

    i = j = 0  # i: text 인덱스, j: pattern 인덱스

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:  # 패턴 발견
                result.append(i - m)
                j = lps[j - 1]  # LPS로 점프
        else:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1

    return result


def boyer_moore_search(text: str, pattern: str) -> List[int]:
    """
    보이어-무어 알고리즘 (Boyer-Moore)
    - 불일치 시 최대 점프로 건너뜀
    - 평균 O(n/m), 최악 O(nm)
    """
    if not pattern:
        return []

    # Bad Character 테이블
    def bad_char_table(pattern: str) -> dict:
        table = {}
        m = len(pattern)
        for i in range(m - 1):
            table[pattern[i]] = m - 1 - i
        return table

    n, m = len(text), len(pattern)
    bad_char = bad_char_table(pattern)
    result = []

    i = 0
    while i <= n - m:
        j = m - 1  # 패턴의 뒤에서부터 비교

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:  # 패턴 발견
            result.append(i)
            # 다음 위치 계산
            shift = bad_char.get(text[i + m], m) if i + m < n else 1
            i += shift
        else:
            # 불일치 시 이동
            shift = bad_char.get(text[i + j], m)
            i += max(1, shift - (m - 1 - j))

    return result


# ============== 실행 예시 ==============

if __name__ == "__main__":
    print("=" * 60)
    print(" 탐색 알고리즘 비교")
    print("=" * 60)

    # 선형 탐색 vs 이진 탐색
    data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 13

    print(f"\n데이터: {data}")
    print(f"찾는 값: {target}")

    idx = linear_search(data, target)
    print(f"선형 탐색: 인덱스 {idx}")

    idx = binary_search(data, target)
    print(f"이진 탐색: 인덱스 {idx}")

    # Lower/Upper Bound
    data2 = [1, 2, 2, 2, 3, 4, 5]
    print(f"\n데이터: {data2}")
    print(f"Lower Bound(2): 인덱스 {lower_bound(data2, 2)}")
    print(f"Upper Bound(2): 인덱스 {upper_bound(data2, 2)}")
    print(f"값 2의 개수: {upper_bound(data2, 2) - lower_bound(data2, 2)}")

    # 해시 테이블
    print("\n" + "=" * 60)
    print(" 해시 테이블")
    print("=" * 60)

    ht: HashTable[int] = HashTable()
    ht.put("apple", 100)
    ht.put("banana", 200)
    ht.put("cherry", 300)

    print(f"apple: {ht.get('apple')}")
    print(f"banana: {ht.get('banana')}")
    print(f"grape: {ht.get('grape')}")

    # BST
    print("\n" + "=" * 60)
    print(" 이진 탐색 트리")
    print("=" * 60)

    bst: BinarySearchTree[int] = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)

    print(f"중위 순회 (정렬): {bst.inorder()}")
    print(f"40 검색: {bst.search(40)}")
    print(f"100 검색: {bst.search(100)}")

    # 문자열 탐색
    print("\n" + "=" * 60)
    print(" 문자열 탐색")
    print("=" * 60)

    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"

    kmp_result = kmp_search(text, pattern)
    print(f"텍스트: {text}")
    print(f"패턴: {pattern}")
    print(f"KMP 발견 위치: {kmp_result}")

    bm_result = boyer_moore_search(text, pattern)
    print(f"보이어-무어 발견 위치: {bm_result}")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:
| 장점 (이진 탐색) | 단점 (이진 탐색) |
|-----------------|------------------|
| O(log n)으로 매우 빠름 | 정렬된 데이터 필수 |
| 추가 공간 불필요 | 삽입/삭제 시 재정렬 필요 |
| 구현이 간단 | 동적 데이터에 부적합 |

| 장점 (해시 테이블) | 단점 (해시 테이블) |
|-------------------|-------------------|
| 평균 O(1)로 가장 빠름 | 충돌 처리 필요 |
| 삽입/삭제도 O(1) | 순서 유지 불가 |
| 범용성 높음 | 공간 오버헤드 |

**대안 기술 비교**:
| 비교 항목 | 선형 탐색 | 이진 탐색 | BST | ★ 해시 |
|---------|----------|----------|-----|--------|
| 시간복잡도 | O(n) | ★ O(log n) | O(log n)~O(n) | ★★ O(1) 평균 |
| 정렬 필요 | X | O | X | X |
| 삽입/삭제 | O(1) | O(n) | ★ O(log n) | ★ O(1) |
| 순서 유지 | O | O | ★ O | X |
| 범위 쿼리 | O | ★ O | ★ O | X |

> **★ 선택 기준**: 정적 정렬 데이터 → 이진 탐색, 동적 데이터 → BST/해시, O(1) 필수 → 해시, 범위 쿼리 → BST/B-트리

**기술 진화 계보**:
```
선형 탐색 → 이진 탐색(1946) → BST(1960) → 해시(1953→현대화) → B-트리(1970) → LSM-트리(1996)
```

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **데이터베이스 인덱스** | B-트리 기반 인덱스 구축 | 쿼리 응답시간 99% 단축 |
| **캐시 시스템** | 해시 테이블로 캐시 구현 | 조회 지연 1ms 이내 |
| **자동완성** | Trie + 이진 탐색 조합 | 응답속도 50ms 이내 |
| **로그 검색** | 역인덱스 + 이진 탐색 | 검색 시간 90% 단축 |

**실제 도입 사례**:
- **Google**: Bigtable의 SSTable 내부에 이진 탐색 활용
- **Redis**: 전체 해시 테이블로 O(1) 키-값 저장
- **MySQL**: InnoDB B+트리 인덱스로 O(log n) 검색

**도입 시 고려사항**:
1. **기술적**: 데이터 크기, 정렬 여부, 삽입/삭제 빈도, 메모리 제약
2. **운영적**: 캐시 적중률, 분산 환경, 일관성 요구사항
3. **보안적**: 타이밍 공격 방지 (상수 시간 비교)
4. **경제적**: 인덱스 저장 공간 vs 검색 성능 트레이드오프

**주의사항 / 흔한 실수**:
- ❌ 정렬되지 않은 배열에 이진 탐색 적용
- ❌ 해시 테이블에서 순서 의존적 로직 작성
- ❌ BST 편향 방지 (AVL/레드블랙 트리 필요)

**관련 개념 / 확장 학습**:
```
📌 탐색 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  탐색 핵심 연관 개념 맵                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [정렬] ←──────→ [탐색] ←──────→ [인덱싱]                      │
│        ↓              ↓               ↓                         │
│   [이진 탐색]     [해시테이블]    [B-트리]                       │
│        ↓              ↓               ↓                         │
│   [Divide&Conquer] [충돌해결]   [데이터베이스]                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 정렬 | 선행 개념 | 이진 탐색의 전제조건 | `[sorting](./sorting.md)` |
| 해시 | 핵심 자료구조 | O(1) 탐색 | `[hash](../data_structure/hash.md)` |
| B-트리 | 응용 개념 | DB 인덱스 | `[b_tree](../data_structure/b_tree.md)` |
| 트라이 | 문자열 탐색 | 접두사 검색 | `[trie](../data_structure/trie.md)` |
| 그래프 탐색 | 확장 개념 | DFS/BFS | `[graph](./graph.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 검색 속도 | 이진 탐색 적용 | O(n) → O(log n) |
| 캐시 적중 | 해시 테이블 활용 | 95% 이상 적중률 |
| DB 성능 | B-트리 인덱싱 | 쿼리 시간 99% 단축 |

**미래 전망**:
1. **기술 발전 방향**: 머신러닝 기반 학습형 인덱스, SIMD 병렬 탐색
2. **시장 트렌드**: 분산 탐색, 실시간 스트림 검색
3. **후속 기술**: Learned Index Structures, Bloom Filter 최적화

> **결론**: 탐색 알고리즘은 데이터 접근의 핵심으로, 정렬 여부, 동적 변경, 공간 제약 등을 고려하여 이진 탐색, 해시, BST 중 최적을 선택하는 기술사적 판단력이 필수다. 특히 DB 인덱스 설계에서 B-트리의 이해가 중요하다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms' Ch.11-12, Knuth TAOCP Vol.3, ACM Computing Surveys

---

## 어린이를 위한 종합 설명

**탐색은 마치 "숨바꼭질에서 친구 찾기"와 같아!**

```
상상해보세요:
  도서관에 책이 1000권 있어요. 그중 "해리포터"를 찾아야 해요!

  📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚
```

**선형 탐색 (한 권씩 다 보기)**:
- 1번 책부터 시작해서...
- "해리포터야?" → 아니요
- "해리포터야?" → 아니요
- 계속 1000권까지 확인...
- 😫 힘들어요! 오래 걸려요!

**이진 탐색 (정리된 도서관에서 똑똑하게)**:
- 책들이 가나다순으로 정리되어 있어요!
- 500번째 책을 펴요 → "ㅎ"로 시작! "해리포터"는 더 뒤에 있네요!
- 750번째 책을 펴요 → "후"로 시작! 너무 뒤로 왔네요!
- 625번째 책을 펴요 → "해"! 여기 근처네요!
- 😊 10번 정도만에 찾았어요!

**해시 테이블 (책 위치를 미리 아는 마법)**:
- 도서관에 "해리포터는 7번 선반!"이라고 적힌 마법의 안내서가 있어요
- "해리포터 찾아줘!" → 안내서 확인 → "7번 선반!" → 바로 찾아요!
- 🎉 단 1번에 찾았어요!

**어떤 방법이 좋을까요?**
- 책이 엉망으로 섞여 있으면: 선형 탐색밖에 못 해요 (느려요 ㅠㅠ)
- 책이 정리되어 있으면: 이진 탐색 (빨라요!)
- 안내서가 있으면: 해시 테이블 (제일 빨라요! ⚡)
