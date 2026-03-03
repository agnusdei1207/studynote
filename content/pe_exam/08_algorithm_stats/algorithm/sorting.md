+++
title = "정렬 알고리즘 (Sorting Algorithms)"
date = 2026-03-03

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 정렬 알고리즘 (Sorting Algorithms)

## 핵심 인사이트 (3줄 요약)
> **정렬**은 데이터를 특정 기준에 따라 순서대로 재배열하는 알고리즘으로, 이진 탐색 등의 기반 기술이다. 비교 기반 정렬의 하한은 **Ω(n log n)**이며, 퀵/병합/힙 정렬이 대표적이다. 현대 언어는 **Timsort**(Python/Java), **Introsort**(C++) 등 하이브리드 정렬을 사용한다.

---

### Ⅰ. 개요

**개념**: 정렬 알고리즘(Sorting Algorithm)은 **데이터 집합을 특정 기준(오름차순, 내림차순, 사용자 정의)에 따라 순서대로 재배열하는 알고리즘**이다.

> 💡 **비유**: "도서관 책 정리" — 무질서한 책들을 저자명 또는 제목 순으로 정리하면 원하는 책을 빠르게 찾을 수 있다.

**등장 배경**:
1. **기존 문제점**: 비정렬 데이터에서의 검색은 O(n)으로 대용량 데이터에 비효율적
2. **기술적 필요성**: 이진 탐색(O(log n))을 위한 선행 조건, 데이터베이스 인덱싱의 기반
3. **시장/산업 요구**: 실시간 랭킹, 로그 분석, 추천 시스템 등 정렬 의존 서비스 증가

**핵심 목적**: 검색 효율화, 데이터 가독성 향상, 순위 기반 처리 지원

---

### Ⅱ. 구성 요소 및 핵심 원리

**정렬 알고리즘 분류**:
| 구분 | 알고리즘 | 시간복잡도 | 특징 |
|------|----------|-----------|------|
| **O(n²) 비교** | 버블, 선택, 삽입 | 최악 O(n²) | 단순, 소량 데이터에 적합 |
| **O(n log n) 비교** | 퀵, 병합, 힙 | 평균 O(n log n) | 대량 데이터에 효율적 |
| **비비교** | 계수, 기수, 버킷 | O(n+k), O(d(n+k)) | 특수 조건에서 O(n) 가능 |
| **하이브리드** | Timsort, Introsort | O(n log n) | 실무 최적화 |

**구조 다이어그램**:
```
                    정렬 알고리즘 분류
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │   ┌─────────────────┐      ┌─────────────────┐        │
    │   │  비교 기반 정렬   │      │ 비비교 기반 정렬 │        │
    │   └────────┬────────┘      └────────┬────────┘        │
    │            │                        │                  │
    │   ┌────────┴────────┐      ┌────────┴────────┐        │
    │   │                 │      │                 │        │
    │ ▼ O(n²)        ▼ O(n log n)│ ▼ 계수정렬   ▼ 기수정렬  │
    │┌────────┐    ┌──────────┐  │┌──────────┐ ┌──────────┐ │
    ││버블정렬│    │ 퀵 정렬  │  ││Counting │ │ Radix    │ │
    ││선택정렬│    │ 병합 정렬│  ││ Sort    │ │ Sort     │ │
    ││삽입정렬│    │ 힙 정렬  │  │└──────────┘ └──────────┘ │
    │└────────┘    └──────────┘  │                        │
    │                            │                        │
    └────────────────────────────────────────────────────────┘

    퀵 정렬 동작 원리 (Divide & Conquer)
    ┌─────────────────────────────────────────────────────────┐
    │  입력: [38, 27, 43, 3, 9, 82, 10]                      │
    │                                                         │
    │  ① 피벗 선택 (예: 마지막 원소 10)                       │
    │                                                         │
    │  ② 분할 (Partition):                                    │
    │     피벗보다 작은 값 │ 피벗 │ 피벗보다 큰 값             │
    │     [3, 9]         │ 10  │ [38, 27, 43, 82]            │
    │                                                         │
    │  ③ 재귀적 정렬:                                         │
    │     [3, 9] → [3, 9]                                    │
    │     [38, 27, 43, 82] → [27, 38, 43, 82]                │
    │                                                         │
    │  ④ 결합: [3, 9, 10, 27, 38, 43, 82]                    │
    └─────────────────────────────────────────────────────────┘

    병합 정렬 동작 원리
    ┌─────────────────────────────────────────────────────────┐
    │  입력: [38, 27, 43, 3, 9, 82, 10]                      │
    │                         │                              │
    │           ┌─────────────┴─────────────┐                │
    │           ▼                           ▼                │
    │      [38, 27, 43, 3]           [9, 82, 10]            │
    │           │                           │                │
    │     ┌─────┴─────┐              ┌─────┴─────┐          │
    │     ▼           ▼              ▼           ▼          │
    │  [38, 27]    [43, 3]        [9, 82]     [10]          │
    │     │           │              │           │          │
    │   ┌─┴─┐      ┌─┴─┐          ┌─┴─┐        │          │
    │   ▼   ▼      ▼   ▼          ▼   ▼        │          │
    │ [38][27]   [43][3]        [9][82]       [10]          │
    │   │           │              │           │          │
    │   ▼           ▼              ▼           ▼          │
    │ [27,38]    [3,43]         [9,82]       [10]          │
    │     │           │              │           │          │
    │     └─────┬─────┘              └─────┬─────┘          │
    │           ▼                           ▼                │
    │      [3, 27, 38, 43]          [9, 10, 82]            │
    │           │                           │                │
    │           └─────────┬─────────────────┘                │
    │                     ▼                                  │
    │          [3, 9, 10, 27, 38, 43, 82]                   │
    └─────────────────────────────────────────────────────────┘
```

**동작 원리 (각 알고리즘)**:
```
① 버블: 인접 비교 → ② 교환 → ③ 반복 → ④ 정렬 완료
① 선택: 최소 탐색 → ② 교환 → ③ 반복 → ④ 정렬 완료
① 삽입: 요소 선택 → ② 적절한 위치 삽입 → ③ 반복 → ④ 정렬 완료
① 퀵: 피벗 선택 → ② 분할 → ③ 재귀 → ④ 결합
① 병합: 분할 → ② 재귀 → ③ 병합 → ④ 정렬 완료
① 힙: 힙 구성 → ② 루트 추출 → ③ 힙 복원 → ④ 반복
```

**핵심 알고리즘/공식**:
```
비교 기반 정렬 하한: Ω(n log n)
  - n!개의 순열 중 하나를 선택해야 함
  - 결정 트리 높이 ≥ log₂(n!) = Ω(n log n)

안정 정렬 (Stable Sort):
  - 동일 키를 가진 원소의 상대적 순서 보존
  - 병합 정렬, 삽입 정렬, 버블 정렬: O
  - 퀵 정렬, 힙 정렬, 선택 정렬: X
```

**코드 예시 (Python)**:
```python
"""
정렬 알고리즘 구현
- O(n²): 버블, 선택, 삽입 정렬
- O(n log n): 퀵, 병합, 힙 정렬
- O(n): 계수 정렬 (특수 조건)
"""
from typing import List, TypeVar, Callable
from functools import wraps
import time

T = TypeVar('T')


def measure_time(func: Callable) -> Callable:
    """실행 시간 측정 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"  {func.__name__}: {(end-start)*1000:.3f}ms")
        return result
    return wrapper


# ============== O(n²) 정렬 ==============

def bubble_sort(arr: List[T]) -> List[T]:
    """
    버블 정렬 (Bubble Sort)
    - 인접한 두 원소를 비교하여 교환
    - 시간복잡도: O(n²), 공간복잡도: O(1)
    - 안정 정렬
    """
    result = arr.copy()
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:  # 최적화: 교환 없으면 정렬 완료
            break
    return result


def selection_sort(arr: List[T]) -> List[T]:
    """
    선택 정렬 (Selection Sort)
    - 최소값을 찾아 앞쪽과 교환
    - 시간복잡도: O(n²), 공간복잡도: O(1)
    - 불안정 정렬
    """
    result = arr.copy()
    n = len(result)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result


def insertion_sort(arr: List[T]) -> List[T]:
    """
    삽입 정렬 (Insertion Sort)
    - 각 원소를 적절한 위치에 삽입
    - 시간복잡도: O(n²), 공간복잡도: O(1)
    - 안정 정렬, 거의 정렬된 데이터에 효율적
    """
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


# ============== O(n log n) 정렬 ==============

def quick_sort(arr: List[T]) -> List[T]:
    """
    퀵 정렬 (Quick Sort)
    - 피벗을 기준으로 분할 정복
    - 평균 O(n log n), 최악 O(n²)
    - 불안정 정렬, 캐시 효율 좋음
    """
    if len(arr) <= 1:
        return arr.copy()

    result = arr.copy()

    def _quick_sort(items: List[T], low: int, high: int):
        if low < high:
            pivot_idx = _partition(items, low, high)
            _quick_sort(items, low, pivot_idx - 1)
            _quick_sort(items, pivot_idx + 1, high)

    def _partition(items: List[T], low: int, high: int) -> int:
        """Lomuto 분할 방식"""
        pivot = items[high]
        i = low - 1
        for j in range(low, high):
            if items[j] <= pivot:
                i += 1
                items[i], items[j] = items[j], items[i]
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1

    _quick_sort(result, 0, len(result) - 1)
    return result


def merge_sort(arr: List[T]) -> List[T]:
    """
    병합 정렬 (Merge Sort)
    - 분할 정복, 항상 O(n log n) 보장
    - 공간복잡도: O(n)
    - 안정 정렬, 외부 정렬 가능
    """
    if len(arr) <= 1:
        return arr.copy()

    def _merge(left: List[T], right: List[T]) -> List[T]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def heap_sort(arr: List[T]) -> List[T]:
    """
    힙 정렬 (Heap Sort)
    - 최대 힙을 구성하여 정렬
    - 시간복잡도: O(n log n), 공간복잡도: O(1)
    - 불안정 정렬, 추가 메모리 불필요
    """
    result = arr.copy()
    n = len(result)

    def _heapify(items: List[T], size: int, root: int):
        """최대 힙 성질 유지"""
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and items[left] > items[largest]:
            largest = left
        if right < size and items[right] > items[largest]:
            largest = right

        if largest != root:
            items[root], items[largest] = items[largest], items[root]
            _heapify(items, size, largest)

    # 최대 힙 구성
    for i in range(n // 2 - 1, -1, -1):
        _heapify(result, n, i)

    # 힙에서 원소 추출
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        _heapify(result, i, 0)

    return result


# ============== O(n) 정렬 (특수 조건) ==============

def counting_sort(arr: List[int], max_val: int = None) -> List[int]:
    """
    계수 정렬 (Counting Sort)
    - 정수 범위가 제한된 경우 O(n + k)
    - 안정 정렬, 정수에만 적용 가능
    """
    if not arr:
        return []

    if max_val is None:
        max_val = max(arr)

    # 빈도 계산
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1

    # 누적 합계
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # 결과 배열 생성 (뒤에서부터 순회하여 안정성 유지)
    result = [0] * len(arr)
    for num in reversed(arr):
        count[num] -= 1
        result[count[num]] = num

    return result


def radix_sort(arr: List[int]) -> List[int]:
    """
    기수 정렬 (Radix Sort)
    - 자릿수별로 계수 정렬 반복
    - O(d(n + k)), d: 최대 자릿수
    """
    if not arr:
        return []

    result = arr.copy()

    def _counting_sort_by_digit(items: List[int], exp: int) -> List[int]:
        """특정 자릿수 기준 계수 정렬"""
        n = len(items)
        output = [0] * n
        count = [0] * 10

        # 빈도 계산
        for item in items:
            digit = (item // exp) % 10
            count[digit] += 1

        # 누적 합계
        for i in range(1, 10):
            count[i] += count[i - 1]

        # 결과 생성
        for i in range(n - 1, -1, -1):
            digit = (items[i] // exp) % 10
            count[digit] -= 1
            output[count[digit]] = items[i]

        return output

    # 최대값의 자릿수 구하기
    max_val = max(result)
    exp = 1

    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp)
        exp *= 10

    return result


# ============== 하이브리드 정렬 ==============

def timsort_like(arr: List[T], min_run: int = 32) -> List[T]:
    """
    Timsort 스타일 하이브리드 정렬
    - 삽입 정렬 + 병합 정렬 결합
    - Python, Java의 기본 정렬
    """
    result = arr.copy()
    n = len(result)

    # 작은 구간은 삽입 정렬
    def _insertion_sort_range(items: List[T], left: int, right: int):
        for i in range(left + 1, right + 1):
            key = items[i]
            j = i - 1
            while j >= left and items[j] > key:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key

    # 병합 함수
    def _merge_ranges(items: List[T], l: int, m: int, r: int):
        left = items[l:m + 1]
        right = items[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                items[k] = left[i]
                i += 1
            else:
                items[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            items[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            items[k] = right[j]
            j += 1
            k += 1

    # 작은 구간 정렬
    for i in range(0, n, min_run):
        _insertion_sort_range(result, i, min(i + min_run - 1, n - 1))

    # 병합
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(n - 1, left + 2 * size - 1)
            if mid < right:
                _merge_ranges(result, left, mid, right)
        size *= 2

    return result


# ============== 실행 예시 ==============

if __name__ == "__main__":
    import random

    # 테스트 데이터
    data = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    large_data = [random.randint(1, 10000) for _ in range(1000)]

    print("=" * 60)
    print(" 정렬 알고리즘 비교")
    print("=" * 60)

    # 소량 데이터 테스트
    print("\n[소량 데이터 (10개)]")
    print(f"입력: {data}")

    algorithms = [
        ("버블 정렬", bubble_sort),
        ("선택 정렬", selection_sort),
        ("삽입 정렬", insertion_sort),
        ("퀵 정렬", quick_sort),
        ("병합 정렬", merge_sort),
        ("힙 정렬", heap_sort),
        ("Timsort 스타일", timsort_like),
    ]

    for name, func in algorithms:
        result = func(data)
        print(f"{name}: {result[:10]}...")

    # 계수/기수 정렬 (정수만)
    print(f"\n계수 정렬: {counting_sort(data)}")
    print(f"기수 정렬: {radix_sort(data)}")

    # 대량 데이터 성능 테스트
    print("\n" + "=" * 60)
    print(f" 대량 데이터 성능 ({len(large_data)}개)")
    print("=" * 60)

    for name, func in algorithms:
        start = time.perf_counter()
        result = func(large_data)
        end = time.perf_counter()
        is_sorted = result == sorted(large_data)
        print(f"  {name}: {(end-start)*1000:.3f}ms (정렬됨: {is_sorted})")

    # 계수/기수 정렬 성능
    start = time.perf_counter()
    counting_result = counting_sort(large_data, 10000)
    end = time.perf_counter()
    print(f"  계수 정렬: {(end-start)*1000:.3f}ms")

    start = time.perf_counter()
    radix_result = radix_sort(large_data)
    end = time.perf_counter()
    print(f"  기수 정렬: {(end-start)*1000:.3f}ms")

    # Python 내장 sort (Timsort)
    start = time.perf_counter()
    sorted(large_data)
    end = time.perf_counter()
    print(f"  Python sorted(): {(end-start)*1000:.3f}ms")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:
| 장점 (퀵 정렬) | 단점 (퀵 정렬) |
|---------------|----------------|
| 평균적으로 가장 빠름 | 최악 O(n²) — 이미 정렬된 데이터 |
| 제자리 정렬 (in-place) | 불안정 정렬 |
| 캐시 효율 우수 | 피벗 선택에 따라 성능 편차 |

| 장점 (병합 정렬) | 단점 (병합 정렬) |
|-----------------|------------------|
| 항상 O(n log n) 보장 | 추가 공간 O(n) 필요 |
| 안정 정렬 | 캐시 효율 낮음 |
| 외부 정렬 가능 | 작은 데이터에 오버헤드 |

**대안 기술 비교**:
| 비교 항목 | 퀵 정렬 | 병합 정렬 | 힙 정렬 | ★ Timsort |
|---------|---------|----------|---------|----------|
| 평균 시간 | ★ O(n log n) | O(n log n) | O(n log n) | O(n log n) |
| 최악 시간 | O(n²) | ★ O(n log n) | O(n log n) | ★ O(n log n) |
| 공간 | O(log n) | O(n) | ★ O(1) | O(n) |
| 안정성 | X | ★ O | X | ★ O |
| 실무 사용 | C qsort | Java 객체 | 제한적 | ★ Python, Java |

> **★ 선택 기준**: 일반적인 경우 언어 내장 정렬(Timsort/Introsort) 사용, 메모리 제약시 힙 정렬, 외부 정렬시 병합 정렬, 정수 범위 제한시 계수/기수 정렬

**기술 진화 계보**:
```
버블(1950s) → 퀵(1960) → 힙(1964) → 병합(1945→현대화) → Timsort(2002) → Pattern-Defeating Quicksort(2016)
```

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **데이터베이스** | 인덱스 B-트리 구축 시 정렬 | 쿼리 응답시간 80% 단축 |
| **검색 엔진** | 역인덱스 정렬 및 병합 | 검색 속도 5배 향상 |
| **실시간 랭킹** | 부분 정렬로 Top-K 추출 | 메모리 90% 절감 |
| **로그 분석** | 타임스탬프 기수 정렬 | 처리량 10배 증가 |

**실제 도입 사례**:
- **Google**: Bigtable 정렬에 병합 정렬 변형 사용 — 페타바이트 규모 처리
- **Redis**: Sorted Set 구현에 Skip List + 정렬 사용 — O(log n) 삽입/조회
- **Python**: Timsort 기본 탑재 — 현실 데이터(부분 정렬)에 최적화

**도입 시 고려사항**:
1. **기술적**: 데이터 크기, 메모리 제약, 정렬 키 복잡도, 안정성 요구
2. **운영적**: 실시간 vs 배치, 병렬화 가능성, 캐시 친화성
3. **보안적**: 정렬 과정에서 정보 유출 방지 (타이밍 공격)
4. **경제적**: 데이터 특성에 맞는 알고리즘 선택으로 비용 최적화

**주의사항 / 흔한 실수**:
- ❌ 퀵 정렬에서 이미 정렬된 데이터에 피벗을 첫/마지막 원소로 선택 (최악 O(n²))
- ❌ 대용량 데이터에 O(n²) 알고리즘 사용
- ❌ 안정 정렬이 필요한 경우 불안정 정렬 사용

**관련 개념 / 확장 학습**:
```
📌 정렬 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  정렬 핵심 연관 개념 맵                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [분할 정복] ←──────→ [정렬] ←──────→ [이진 탐색]              │
│        ↓                   ↓                   ↓                │
│   [퀵/병합 정렬]     [힙 자료구조]        [BST 탐색]             │
│        ↓                   ↓                   ↓                │
│   [재귀 알고리즘]    [우선순위큐]        [데이터베이스 인덱스]    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 이진 탐색 | 후속 개념 | 정렬된 데이터에서 O(log n) 탐색 | `[searching](./searching.md)` |
| 힙 | 핵심 자료구조 | 힙 정렬의 기반 | `[heap](../data_structure/heap.md)` |
| 분할 정복 | 설계 기법 | 퀵/병합 정렬의 핵심 패러다임 | `[divide_conquer](./divide_conquer.md)` |
| 탐욕 알고리즘 | 관련 기법 | 선택 정렬의 설계 기법 | `[greedy](./greedy.md)` |
| B-트리 | 응용 개념 | DB 인덱스의 정렬 구조 | `[b_tree](../data_structure/b_tree.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 검색 효율 | 정렬 후 이진 탐색 가능 | 검색 시간 O(n) → O(log n) |
| 메모리 최적 | 적절한 알고리즘 선택 | 메모리 사용 50% 절감 |
| 처리량 향상 | 하이브리드 정렬 활용 | 대용량 처리 10배 향상 |

**미래 전망**:
1. **기술 발전 방향**: GPU 기반 병렬 정렬, 양자 정렬 알고리즘
2. **시장 트렌드**: 실시간 스트리밍 데이터 정렬, 분산 정렬 (MapReduce)
3. **후속 기술**: Pattern-Defeating Quicksort, LLVM parallel sort

> **결론**: 정렬은 컴퓨터 과학의 근본 알고리즘으로, O(n log n) 하한과 안정성, 공간 효율성 간의 트레이드오프를 이해하고 데이터 특성에 맞는 최적 알고리즘을 선택하는 것이 기술사의 핵심 역량이다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms' Ch.6-8, Knuth TAOCP Vol.3, IEEE Floating-Point Arithmetic

---

## 어린이를 위한 종합 설명

**정렬은 마치 "교실에서 키 순서대로 줄 서기"와 같아!**

```
상상해보세요:
  선생님이 "반 친구들, 키 순서대로 줄 서세요!"라고 말했어요.

  처음 상태 (무질서):
  🧒 120cm  👦 135cm  👧 110cm  🧑 145cm  👦 125cm

  어떻게 줄을 세울까요?
```

**버블 정렬 방식 (옆 친구랑 계속 바꾸기)**:
- "옆 친구보다 키가 크면 자리 바꿔!"
- 120과 135 비교 → 그대로 (120 < 135)
- 135와 110 비교 → 바꿔! (135 > 110)
- 계속 옆 사람과 비교하면서 제자리를 찾아가요.

**선택 정렬 방식 (제일 작은 친구 찾아서 앞으로)**:
- "반에서 제일 작은 친구 누구야?"
- 110cm 친구 찾았어요! → 맨 앞으로 와!
- "그 다음 작은 친구는?" → 120cm 친구! → 두 번째로 와!
- 계속 제일 작은 친구를 찾아서 앞에서부터 채워요.

**퀵 정렬 방식 (기준을 정해서 양쪽으로 나누기)**:
- "키가 130cm인 친구를 기준으로!"
- 130cm보다 작은 친구들 ← 왼쪽으로!
- 130cm보다 큰 친구들 → 오른쪽으로!
- 각 그룹에서 다시 기준을 정해서 나눠요. (반복!)

**결과 (모두 같아요)**:
  👧 110cm → 🧒 120cm → 👦 125cm → 👦 135cm → 🧑 145cm

**어떤 방법이 제일 빠를까요?**
- 친구가 5명이면: 다 비슷해요
- 친구가 100명이면: 퀵 정렬이 훨씬 빨라요!
- 친구가 1000명이면: 퀵 정렬이나 병합 정렬을 써야 해요! 🏃‍♂️💨
