+++
title = "힙 자료구조 (Heap Data Structure)"
date = 2026-03-03

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 힙 자료구조 (Heap Data Structure)

## 핵심 인사이트 (3줄 요약)
> **힙**은 완전 이진 트리 기반의 **우선순위 큐** 구현 자료구조로, 루트에 항상 최댓값(최대 힙) 또는 최솟값(최소 힙)이 위치한다. 삽입/삭제는 O(log n), 최댓값/최솟값 조회는 O(1)이며, **힙 정렬**과 **다익스트라**의 핵심이다. 현대 언어는 `heapq`(Python), `PriorityQueue`(Java)로 제공된다.

---

### Ⅰ. 개요

**개념**: 힙(Heap)은 **완전 이진 트리(Complete Binary Tree)에서 부모 노드가 자식 노드보다 항상 크거나(최대 힙) 작은(최소 힙) 힙 성질(Heap Property)을 만족**하는 자료구조다.

> 💡 **비유**: "응급실 대기 환자 목록" — 항상 가장 위급한 환자(최대 우선순위)가 맨 위에 있어 즉시 호출 가능

**등장 배경**:
1. **기존 문제점**: 일반 큐(FIFO)는 우선순위 반영 불가, 정렬된 배열은 삽입/삭제에 O(n) 소요
2. **기술적 필요성**: 운영체제 스케줄링, 다익스트라 알고리즘, 이벤트 시뮬레이션 등 우선순위 기반 처리
3. **시장/산업 요구**: 실시간 시스템, 작업 스케줄러, 네트워크 패킷 처리의 필수 자료구조

**핵심 목적**: O(1)로 최우선 요소 조회, O(log n)으로 우선순위 기반 삽입/삭제

---

### Ⅱ. 구성 요소 및 핵심 원리

**힙 구성 요소**:
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **루트 노드** | 최대/최소 원소 | O(1) 조회 | 응급실 1순위 환자 |
| **완전 이진 트리** | 힙의 구조 | 마지막 레벨 좌측부터 채움 | 완전히 찬 병원 대기실 |
| **힙 성질** | 부모 ≥ 자식 (최대) | 삽입/삭제 시 유지 | 환자 중증도 순서 |
| **배열 표현** | 인덱스 계산 | 부모=i/2, 자식=2i, 2i+1 | 번호표 기반 위치 |

**구조 다이어그램**:
```
    최대 힙 (Max Heap)                    최소 힙 (Min Heap)
    ┌─────────────────────────┐          ┌─────────────────────────┐
    │          [100]          │          │           [1]           │
    │         /    \          │          │          /    \         │
    │      [40]    [80]       │          │        [5]    [10]      │
    │      /  \    /  \       │          │        / \    /  \      │
    │   [20][30][50][70]      │          │     [15][20][25][40]    │
    │                         │          │                         │
    │   부모 ≥ 자식            │          │   부모 ≤ 자식            │
    │   루트 = 최댓값          │          │   루트 = 최솟값          │
    └─────────────────────────┘          └─────────────────────────┘

    배열 표현 (인덱스 1부터 시작)
    ┌─────────────────────────────────────────────────────────────┐
    │  인덱스:  0    1    2    3    4    5    6    7              │
    │  값:    [-] [100] [40] [80] [20] [30] [50] [70]             │
    │                                                             │
    │  부모 인덱스 = i // 2                                       │
    │  왼쪽 자식 = 2 * i                                          │
    │  오른쪽 자식 = 2 * i + 1                                    │
    │                                                             │
    │  예: 값 40 (인덱스 2)                                       │
    │      부모 = 2//2 = 1 → 값 100                               │
    │      왼쪽 자식 = 2*2 = 4 → 값 20                            │
    │      오른쪽 자식 = 2*2+1 = 5 → 값 30                        │
    └─────────────────────────────────────────────────────────────┘

    삽입 과정 (Heapify-Up / Sift-Up)
    ┌─────────────────────────────────────────────────────────────┐
    │  90 삽입 전:                   90 삽입 후:                   │
    │                                                             │
    │         100                         100                     │
    │        /    \                       /    \                  │
    │      40      80                   90      80                │
    │     /  \    /  \                 /  \    /  \               │
    │   20   30  50  70              40   30  50  70              │
    │                                /                             │
    │                              [90]  ← 마지막 위치에 추가      │
    │                                                             │
    │  Sift-Up 과정:                                              │
    │  ① 90의 부모 40 < 90 → 교환                                 │
    │  ② 90의 부모 100 > 90 → 종료                                │
    │                                                             │
    │         100                         100                     │
    │        /    \                       /    \                  │
    │     [90]    80                    90      80                │
    │     /  \    /  \                 /  \    /  \               │
    │   40   30  50  70              40   30  50  70              │
    └─────────────────────────────────────────────────────────────┘

    삭제 과정 (Heapify-Down / Sift-Down)
    ┌─────────────────────────────────────────────────────────────┐
    │  루트 100 삭제 전:            루트 100 삭제 후:              │
    │                                                             │
    │         100                         80                      │
    │        /    \                       /    \                  │
    │      90      80                   90      70                │
    │     /  \    /  \                 /  \    /                  │
    │   40   30  50  70              40   30  50                  │
    │                                                             │
    │  Sift-Down 과정:                                            │
    │  ① 루트 100 반환, 마지막 70을 루트로                         │
    │  ② 70 vs 자식 90, 80 → 90이 더 큼 → 교환                     │
    │  ③ 70 vs 자식 40, 30 → 40이 더 큼 → 교환                     │
    │  ④ 리프 도달 → 종료                                         │
    │                                                             │
    │         [70]                        90                      │
    │        /    \                       /    \                  │
    │      90      80                  [70]    80                 │
    │     /  \    /                    /  \                       │
    │   40   30  50                  40   30                      │
    └─────────────────────────────────────────────────────────────┘
```

**동작 원리**:
```
① 삽입: 마지막 위치 추가 → ② 부모와 비교(Sift-Up) → ③ 교환 반복 → ④ 제자리 도달
① 삭제: 루트 반환 → ② 마지막 원소 루트로 → ③ 자식과 비교(Sift-Down) → ④ 제자리 도달
① 힙 생성: 배열 → ② 마지막 비리프부터 → ③ Sift-Down → ④ 루트까지 반복
```

**핵심 알고리즘/공식**:
```
힙 인덱스 관계 (0-based):
  부모: (i - 1) // 2
  왼쪽 자식: 2 * i + 1
  오른쪽 자식: 2 * i + 2

힙 성질 (Max Heap):
  A[parent(i)] ≥ A[i]

힙 높이:
  h = ⌊log₂(n)⌋

시간복잡도:
  삽입/삭제: O(log n) = O(h)
  최댓값/최솟값 조회: O(1)
  힙 생성(Heapify): O(n) — 모든 노드 Sift-Down 합
```

**코드 예시 (Python)**:
```python
"""
힙 자료구조 구현
- 최대 힙 / 최소 힙
- 우선순위 큐
- 힙 정렬
"""
from typing import List, Optional, TypeVar, Generic, Callable

T = TypeVar('T')


class Heap(Generic[T]):
    """
    힙 자료구조
    - 최대 힙 / 최소 힙 지원
    - 배열 기반 구현
    """
    def __init__(self, max_heap: bool = True):
        """
        Args:
            max_heap: True면 최대 힙, False면 최소 힙
        """
        self.data: List[T] = []
        self.compare = (lambda a, b: a > b) if max_heap else (lambda a, b: a < b)

    def __len__(self) -> int:
        return len(self.data)

    def _parent(self, i: int) -> int:
        """부모 인덱스"""
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        """왼쪽 자식 인덱스"""
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        """오른쪽 자식 인덱스"""
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        """두 원소 교환"""
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _sift_up(self, i: int) -> None:
        """Sift-Up (Heapify-Up): 삽입 후 위로 올라가며 힙 성질 복원"""
        while i > 0:
            parent = self._parent(i)
            if self.compare(self.data[i], self.data[parent]):
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        """Sift-Down (Heapify-Down): 삭제 후 아래로 내려가며 힙 성질 복원"""
        n = len(self.data)
        while True:
            largest = i
            left = self._left_child(i)
            right = self._right_child(i)

            if left < n and self.compare(self.data[left], self.data[largest]):
                largest = left
            if right < n and self.compare(self.data[right], self.data[largest]):
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def push(self, value: T) -> None:
        """원소 삽입 - O(log n)"""
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def pop(self) -> Optional[T]:
        """최댓값/최솟값 추출 - O(log n)"""
        if not self.data:
            return None

        result = self.data[0]
        last = self.data.pop()

        if self.data:
            self.data[0] = last
            self._sift_down(0)

        return result

    def peek(self) -> Optional[T]:
        """최댓값/최솟값 조회 (삭제 없음) - O(1)"""
        return self.data[0] if self.data else None

    def build_heap(self, arr: List[T]) -> None:
        """
        배열로부터 힙 생성 - O(n)
        마지막 비리프 노드부터 역순으로 Sift-Down
        """
        self.data = arr.copy()
        n = len(self.data)

        # 마지막 비리프 노드부터 루트까지
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)


class PriorityQueue(Generic[T]):
    """
    우선순위 큐 (힙 기반)
    - (우선순위, 값) 쌍 저장
    - 높은 우선순위가 먼저 나옴
    """
    def __init__(self, max_priority: bool = True):
        # (우선순위, 카운터, 값) 저장 — 카운터는 삽입 순서 유지용
        self.heap: Heap = Heap(max_heap=max_priority)
        self.counter = 0

    def push(self, priority: int, value: T) -> None:
        """우선순위와 함께 값 삽입"""
        self.heap.push((priority, self.counter, value))
        self.counter += 1

    def pop(self) -> Optional[tuple]:
        """최우선 원소 추출"""
        item = self.heap.pop()
        if item:
            return (item[0], item[2])  # (우선순위, 값)
        return None

    def peek(self) -> Optional[tuple]:
        """최우선 원소 조회"""
        item = self.heap.peek()
        if item:
            return (item[0], item[2])
        return None


def heap_sort(arr: List[T], ascending: bool = True) -> List[T]:
    """
    힙 정렬 (Heap Sort)
    - 시간복잡도: O(n log n)
    - 공간복잡도: O(1) (in-place 가능)
    - 불안정 정렬
    """
    # 오름차순: 최대 힙 사용 (최댓값을 뒤로)
    heap = Heap(max_heap=ascending)
    heap.build_heap(arr)

    result = []
    while len(heap) > 0:
        result.append(heap.pop())

    return result if not ascending else result[::-1]


def heap_sort_inplace(arr: List[T]) -> List[T]:
    """
    제자리 힙 정렬 (In-place Heap Sort)
    - 추가 메모리 없이 배열 내에서 정렬
    """
    n = len(arr)

    def sift_down(heap: List[T], size: int, i: int):
        """최대 힙 Sift-Down"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < size and heap[left] > heap[largest]:
            largest = left
        if right < size and heap[right] > heap[largest]:
            largest = right

        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            sift_down(heap, size, largest)

    # 1. 최대 힙 생성 - O(n)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)

    # 2. 정렬: 루트(최댓값)를 끝으로 이동 - O(n log n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 최댓값을 뒤로
        sift_down(arr, i, 0)  # 힙 크기 줄이며 복원

    return arr


# ============== 실행 예시 ==============

if __name__ == "__main__":
    print("=" * 60)
    print(" 힙 자료구조")
    print("=" * 60)

    # 최대 힙
    print("\n[최대 힙]")
    max_heap: Heap[int] = Heap(max_heap=True)

    for val in [20, 15, 30, 10, 25, 35, 5]:
        max_heap.push(val)
        print(f"  삽입 {val}: {max_heap.data}")

    print(f"\n최댓값 조회: {max_heap.peek()}")

    while len(max_heap) > 0:
        print(f"  추출: {max_heap.pop()}")

    # 최소 힙
    print("\n[최소 힙]")
    min_heap: Heap[int] = Heap(max_heap=False)

    for val in [20, 15, 30, 10, 25, 35, 5]:
        min_heap.push(val)

    print(f"  최솟값 조회: {min_heap.peek()}")
    print(f"  정렬된 추출: ", end="")
    while len(min_heap) > 0:
        print(min_heap.pop(), end=" ")
    print()

    # 우선순위 큐
    print("\n" + "=" * 60)
    print(" 우선순위 큐")
    print("=" * 60)

    pq: PriorityQueue[str] = PriorityQueue(max_priority=True)
    pq.push(3, "일반 업무")
    pq.push(1, "긴급! 장애")
    pq.push(2, "회의")
    pq.push(5, "낮음")

    print("\n작업 처리 순서:")
    while (item := pq.pop()) is not None:
        print(f"  우선순위 {item[0]}: {item[1]}")

    # 힙 정렬
    print("\n" + "=" * 60)
    print(" 힙 정렬")
    print("=" * 60)

    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"\n원본: {data}")
    print(f"정렬: {heap_sort(data)}")
    print(f"In-place: {heap_sort_inplace(data.copy())}")

    # 힙 생성 O(n) vs O(n log n) 비교
    print("\n" + "=" * 60)
    print(" 힙 생성 효율성")
    print("=" * 60)
    print("  build_heap O(n): 마지막 비리프부터 Sift-Down")
    print("  반복 삽입 O(n log n): 루트부터 순차 삽입")
    print("  → build_heap이 더 효율적!")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:
| 장점 (힙) | 단점 (힙) |
|----------|----------|
| 최댓값/최솟값 O(1) 조회 | 임의 원소 검색 O(n) |
| 삽입/삭제 O(log n) | 정렬된 순회 불가 |
| 힙 정렬 O(n log n) 보장 | 캐시 지역성 낮음 |
| 제자리 정렬 가능 | 불안정 정렬 |

**대안 기술 비교**:
| 비교 항목 | 힙 | ★ 정렬된 배열 | BST | 해시 테이블 |
|---------|-----|-------------|-----|-----------|
| 최댓값/최솟값 | ★ O(1) | ★ O(1) | O(log n) | O(n) |
| 삽입 | O(log n) | O(n) | ★ O(log n) | ★ O(1) |
| 삭제 | O(log n) | O(n) | ★ O(log n) | ★ O(1) |
| 검색 | O(n) | ★ O(log n) | ★ O(log n) | ★ O(1) |
| 정렬 순회 | X | ★ O(n) | ★ O(n) | X |

> **★ 선택 기준**: 우선순위 기반 처리 → 힙, 빠른 검색 → BST/해시, 정렬된 순서 → 정렬된 배열

**정렬 알고리즘 비교**:
| 알고리즘 | 평균 | 최악 | 공간 | 안정성 | 비고 |
|---------|------|------|------|--------|------|
| **힙 정렬** | ★ O(n log n) | ★ O(n log n) | ★ O(1) | X | 최악 보장, 제자리 |
| 퀵 정렬 | O(n log n) | O(n²) | O(log n) | X | 평균 빠름 |
| 병합 정렬 | O(n log n) | O(n log n) | O(n) | ★ O | 안정, 외부정렬 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **다익스트라** | 최소 힙으로 최단 거리 노드 추출 | O(V²) → O(E log V) |
| **OS 스케줄러** | 우선순위 큐로 프로세스 관리 | 응답시간 30% 개선 |
| **이벤트 시뮬레이션** | 시간 기반 이벤트 큐 | 시뮬레이션 속도 5배 |
| **K번째 원소** | 크기 K 힙 유지 | O(n log K) |

**실제 도입 사례**:
- **Python heapq**: 최소 힙 기본 제공 — 다익스트라, 우선순위 큐 구현
- **Java PriorityQueue**: 우선순위 큐 기본 클래스 — 스레드 풀 작업 관리
- **Linux CFS**: Completely Fair Scheduler — 스케줄링 최적화

**도입 시 고려사항**:
1. **기술적**: 최대/최소 힙 선택, 동적 크기, 원소 타입
2. **운영적**: 동시성 제어 (스레드 안전), 메모리 관리
3. **보안적**: 우선순위 조작 방지, 무한 루프 방지
4. **경제적**: 대량 데이터 시 힙 정렬 vs 퀵 정렬 선택

**주의사항 / 흔한 실수**:
- ❌ 인덱스 계산 오류 (0-based vs 1-based)
- ❌ 최대 힙/최소 힙 혼동
- ❌ Sift-Up/Sift-Down 방향 오류

**관련 개념 / 확장 학습**:
```
📌 힙 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  힙 핵심 연관 개념 맵                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [완전 이진 트리] ←──→ [힙] ←──→ [우선순위 큐]                │
│          ↓              ↓              ↓                        │
│   [배열 표현]      [힙 정렬]      [다익스트라]                  │
│          ↓              ↓              ↓                        │
│   [인덱스 계산]    [Heapify]      [K번째 원소]                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 이진 트리 | 기반 구조 | 힙은 완전 이진 트리 | `[tree](./tree.md)` |
| 우선순위 큐 | 핵심 응용 | 힙의 주요 용도 | — |
| 정렬 | 응용 알고리즘 | 힙 정렬 | `[sorting](../algorithm/sorting.md)` |
| 그래프 | 응용 분야 | 다익스트라 | `[shortest_path](../algorithm/shortest_path.md)` |
| 스케줄링 | 실무 응용 | OS 프로세스 스케줄러 | — |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 우선순위 처리 | O(1) 최우선 조회 | 응답시간 1ms 이내 |
| 정렬 효율 | O(n log n) 보장 | 최악의 경우에도 안정 |
| 메모리 효율 | 제자리 정렬 | 추가 공간 O(1) |

**미래 전망**:
1. **기술 발전 방향**: 병렬 힙, Fibonacci 힙 (O(1) 감소 키)
2. **시장 트렌드**: 실시간 시스템, 게임 엔진, 금융 거래 처리
3. **후속 기술**: Pairing Heap, Binomial Heap, Leftist Heap

> **결론**: 힙은 우선순위 기반 데이터 처리의 핵심 자료구조로, O(1) 조회와 O(log n) 삽입/삭제의 효율성으로 다익스트라, 힙 정렬, OS 스케줄러의 기반이다. 최대/최소 힙의 특성과 Sift-Up/Sift-Down 동작의 완벽한 이해가 기술사의 필수 역량이다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms' Ch.6, IEEE Priority Queue Standards, Python heapq Documentation

---

## 어린이를 위한 종합 설명

**힙은 마치 "응급실 환자 대기 명단"과 같아!**

```
상상해보세요:
  병원 응급실에 환자들이 줄지어 있어요!

  👨‍🦽 환자 A (배탈)
  👩‍🦽 환자 B (팔 골절)
  🚑 환자 C (심장마비!)
  👨‍🦽 환자 D (발목 삠)
```

**일반 줄 (FIFO 큐)**:
- "먼저 온 사람부터!"
- 배탈 → 팔 골절 → 심장마비 → 발목 삠
- 😱 심장마비 환자가 너무 늦게 진료받아요!

**힙 (우선순위 큐)**:
- "제일 위급한 사람 먼저!"
- 심장마비! 🚑 → 팔 골절 → 배탈 → 발목 삠
- 😊 위급한 환자가 바로 진료받아요!

**힙의 마법**:
```
최대 힙 (가장 큰 게 위에):          최소 힙 (가장 작은 게 위에):
         100                                1
        /   \                             /   \
      40    80                          5     10
     / \   / \                         / \   / \
    20 30 50 70                      15 20 25 40

  → 100이 제일 위에!                 → 1이 제일 위에!
  → 한 번에 꺼낼 수 있어요!           → 한 번에 꺼낼 수 있어요!
```

**힙 정렬 (제일 큰 걸 계속 꺼내기)**:
1. 100 꺼내기 → [100]
2. 80 꺼내기 → [80, 100]
3. 70 꺼내기 → [70, 80, 100]
4. 계속 반복하면... 정렬 완료! 🎉
