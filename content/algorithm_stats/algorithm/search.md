+++
title = "탐색 알고리즘 (Search Algorithm)"
date = 2025-03-01

[extra]
categories = "algorithm_stats-algorithm"
+++

# 탐색 알고리즘 (Search Algorithm)

## 핵심 인사이트 (3줄 요약)
> **데이터에서 원하는 값을 찾는 알고리즘**. 선형 탐색 O(n), 이진 탐색 O(log n), 해시 탐색 O(1). 정렬 여부와 데이터 크기에 따라 선택.

## 1. 개념
탐색 알고리즘은 **데이터 집합에서 특정 값을 찾거나 위치를 확인**하는 알고리즘이다.

> 비유: "책에서 단어 찾기" - 처음부터 읽기 vs 색인 활용

## 2. 탐색 알고리즘 분류

```
┌────────────────────────────────────────────────────────┐
│                   탐색 알고리즘 분류                    │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 선형 탐색 (Linear Search)                         │
│     ┌────────────────────────────────────────────┐    │
│     │ 순차적으로 하나씩 비교                      │    │
│     │ 시간복잡도: O(n)                            │    │
│     │ 정렬 안 된 데이터에서 사용                  │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 이진 탐색 (Binary Search)                         │
│     ┌────────────────────────────────────────────┐    │
│     │ 정렬된 데이터에서 중간값 비교               │    │
│     │ 시간복잡도: O(log n)                        │    │
│     │ 반드시 정렬된 데이터 필요                  │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  3. 해시 탐색 (Hash Search)                           │
│     ┌────────────────────────────────────────────┐    │
│     │ 해시 함수로 직접 위치 계산                  │    │
│     │ 평균 시간복잡도: O(1)                       │    │
│     │ 충돌 처리 필요                             │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  4. 트리 탐색 (Tree Search)                           │
│     ┌────────────────────────────────────────────┐    │
│     │ 이진 탐색 트리: O(log n) ~ O(n)            │    │
│     │ DFS (깊이 우선), BFS (너비 우선)           │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 탐색 알고리즘 비교

```
┌────────────────────────────────────────────────────────┐
│                  탐색 알고리즘 비교                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  알고리즘    최선    평균    최악    전제조건         │
│  ─────────────────────────────────────────────────    │
│  선형 탐색   O(1)    O(n)    O(n)    없음             │
│  이진 탐색   O(1)   O(log n) O(log n) 정렬됨         │
│  해시 탐색   O(1)    O(1)    O(n)    해시함수        │
│  BST 탐색    O(log n) O(log n) O(n)   BST 구조       │
│  AVL 탐색    O(log n) O(log n) O(log n) AVL 트리     │
│                                                        │
│  n=1,000,000일 때:                                    │
│  - 선형 탐색: 최대 1,000,000회 비교                   │
│  - 이진 탐색: 최대 20회 비교                          │
│  - 해시 탐색: 평균 1회                                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 코드 예시

```python
from typing import List, Optional, Dict
import time
import random

class SearchAlgorithms:
    """탐색 알고리즘 구현"""

    @staticmethod
    def linear_search(arr: List[int], target: int) -> int:
        """선형 탐색"""
        for i, val in enumerate(arr):
            if val == target:
                return i
        return -1

    @staticmethod
    def binary_search(arr: List[int], target: int) -> int:
        """이진 탐색 (반복문)"""
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    @staticmethod
    def binary_search_recursive(arr: List[int], target: int,
                                left: int = 0, right: int = None) -> int:
        """이진 탐색 (재귀)"""
        if right is None:
            right = len(arr) - 1

        if left > right:
            return -1

        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return SearchAlgorithms.binary_search_recursive(arr, target, mid + 1, right)
        else:
            return SearchAlgorithms.binary_search_recursive(arr, target, left, mid - 1)

    @staticmethod
    def lower_bound(arr: List[int], target: int) -> int:
        """하한 (target 이상인 첫 번째 위치)"""
        left, right = 0, len(arr)

        while left < right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            else:
                right = mid

        return left

    @staticmethod
    def upper_bound(arr: List[int], target: int) -> int:
        """상한 (target 초과인 첫 번째 위치)"""
        left, right = 0, len(arr)

        while left < right:
            mid = (left + right) // 2
            if arr[mid] <= target:
                left = mid + 1
            else:
                right = mid

        return left

class HashTable:
    """해시 테이블"""

    def __init__(self, size: int = 100):
        self.size = size
        self.table: List[List[tuple]] = [[] for _ in range(size)]

    def _hash(self, key: int) -> int:
        """해시 함수"""
        return key % self.size

    def insert(self, key: int, value: any):
        """삽입"""
        index = self._hash(key)
        # 이미 있는지 확인
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def search(self, key: int) -> Optional[any]:
        """탐색"""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key: int) -> bool:
        """삭제"""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False

def performance_test():
    """성능 테스트"""
    print("=== 탐색 알고리즘 성능 비교 ===\n")

    # 테스트 데이터
    sizes = [1000, 10000, 100000]

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[-1]  # 최악의 경우

        print(f"데이터 크기: {size}")

        # 선형 탐색
        start = time.time()
        SearchAlgorithms.linear_search(arr, target)
        linear_time = time.time() - start

        # 이진 탐색
        start = time.time()
        SearchAlgorithms.binary_search(arr, target)
        binary_time = time.time() - start

        # 해시 탐색
        ht = HashTable(size * 2)
        for val in arr:
            ht.insert(val, val)

        start = time.time()
        ht.search(target)
        hash_time = time.time() - start

        print(f"  선형 탐색: {linear_time*1000:.4f}ms")
        print(f"  이진 탐색: {binary_time*1000:.4f}ms")
        print(f"  해시 탐색: {hash_time*1000:.4f}ms")
        print()


# 사용 예시
print("=== 탐색 알고리즘 시연 ===\n")

arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 7

print(f"배열: {arr}")
print(f"찾을 값: {target}\n")

# 선형 탐색
idx = SearchAlgorithms.linear_search(arr, target)
print(f"선형 탐색: 인덱스 {idx}")

# 이진 탐색
idx = SearchAlgorithms.binary_search(arr, target)
print(f"이진 탐색: 인덱스 {idx}")

# 이진 탐색 (재귀)
idx = SearchAlgorithms.binary_search_recursive(arr, target)
print(f"이진 탐색 (재귀): 인덱스 {idx}")

# 하한/상한
arr2 = [1, 2, 2, 2, 3, 4, 5]
print(f"\n배열: {arr2}")
print(f"2의 하한: {SearchAlgorithms.lower_bound(arr2, 2)}")  # 1
print(f"2의 상한: {SearchAlgorithms.upper_bound(arr2, 2)}")  # 4

# 해시 테이블
print("\n--- 해시 테이블 ---")
ht = HashTable(10)
ht.insert(1, "사과")
ht.insert(11, "바나나")  # 충돌
ht.insert(2, "오렌지")

print(f"키 1 검색: {ht.search(1)}")
print(f"키 11 검색: {ht.search(11)}")
print(f"키 99 검색: {ht.search(99)}")

# 성능 테스트
performance_test()
