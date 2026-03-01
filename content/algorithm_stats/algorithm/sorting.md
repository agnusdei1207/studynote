+++
title = "정렬 알고리즘 (Sorting Algorithm)"
date = 2025-03-01

[extra]
categories = "algorithm_stats-algorithm"
+++

# 정렬 알고리즘 (Sorting Algorithm)

## 핵심 인사이트 (3줄 요약)
> **데이터를 특정 순서로 재배열하는 알고리즘**. O(n²)의 단순 정렬과 O(n log n)의 효율 정렬로 분류. 안정성, 제자리성, 시간복잡도가 선택 기준.

## 1. 개념
정렬 알고리즘은 **데이터를 오름차순 또는 내림차순으로 재배열**하는 알고리즘이다.

> 비유: "책장 정리" - 책들을 제목순으로 나열

## 2. 정렬 알고리즘 분류

```
┌─────────────────────────────────────────────────────────┐
│                   정렬 알고리즘 분류                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  시간복잡도 기준:                                       │
│                                                         │
│  O(n²) - 단순 정렬                                      │
│  ┌───────────────────────────────────────────────┐     │
│  │ • 버블 정렬 (Bubble Sort)                     │     │
│  │ • 선택 정렬 (Selection Sort)                  │     │
│  │ • 삽입 정렬 (Insertion Sort)                  │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  O(n log n) - 효율 정렬                                 │
│  ┌───────────────────────────────────────────────┐     │
│  │ • 퀵 정렬 (Quick Sort)                        │     │
│  │ • 병합 정렬 (Merge Sort)                      │     │
│  │ • 힙 정렬 (Heap Sort)                         │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  O(n) - 특수 정렬 (제한적 조건)                         │
│  ┌───────────────────────────────────────────────┐     │
│  │ • 계수 정렬 (Counting Sort)                   │     │
│  │ • 기수 정렬 (Radix Sort)                      │     │
│  │ • 버킷 정렬 (Bucket Sort)                     │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 3. 정렬 알고리즘 비교

| 알고리즘 | 최선 | 평균 | 최악 | 공간 | 안정 |
|---------|------|------|------|------|------|
| 버블 | O(n) | O(n²) | O(n²) | O(1) | O |
| 선택 | O(n²) | O(n²) | O(n²) | O(1) | X |
| 삽입 | O(n) | O(n²) | O(n²) | O(1) | O |
| 퀵 | O(n log n) | O(n log n) | O(n²) | O(log n) | X |
| 병합 | O(n log n) | O(n log n) | O(n log n) | O(n) | O |
| 힙 | O(n log n) | O(n log n) | O(n log n) | O(1) | X |

## 4. 주요 정렬 알고리즘

### 4.1 버블 정렬 (Bubble Sort)
```
인접한 두 원소를 비교하여 교환

과정:
[5, 3, 8, 1, 2]
Pass 1:
[3, 5, 8, 1, 2]  5↔3
[3, 5, 8, 1, 2]  8>5 유지
[3, 5, 1, 8, 2]  8↔1
[3, 5, 1, 2, 8]  8↔2  ← 8 확정

Pass 2:
[3, 5, 1, 2, 8]
[3, 1, 5, 2, 8]  5↔1
[3, 1, 2, 5, 8]  5↔2  ← 5 확정

... 반복

시간복잡도: O(n²)
특징: 구현 쉬움, 비효율적
```

### 4.2 선택 정렬 (Selection Sort)
```
최솟값을 찾아 맨 앞으로 이동

과정:
[5, 3, 8, 1, 2]  최솟값 1 → 맨 앞
[1, 3, 8, 5, 2]  최솟값 2 → 두 번째
[1, 2, 8, 5, 3]  최솟값 3 → 세 번째
[1, 2, 3, 5, 8]  완료

시간복잡도: O(n²)
특징: 교환 횟수 적음
```

### 4.3 삽입 정렬 (Insertion Sort)
```
각 원소를 적절한 위치에 삽입

과정:
[5]           → 정렬됨
[3, 5]        → 3 삽입
[3, 5, 8]     → 8 삽입
[1, 3, 5, 8]  → 1 삽입
[1, 2, 3, 5, 8] → 2 삽입

시간복잡도: O(n²) (거의 정렬된 경우 O(n))
특징: 작은 데이터에 효율적
```

### 4.4 퀵 정렬 (Quick Sort)
```
피벗을 기준으로 분할 정복

과정:
[5, 3, 8, 1, 2]  피벗=5
[3, 1, 2] 5 [8]  분할

[3, 1, 2] 피벗=3
[1, 2] 3 []      분할

[1, 2] 피벗=1
[] 1 [2]         분할

결합: [1, 2, 3, 5, 8]

시간복잡도: 평균 O(n log n), 최악 O(n²)
특징: 실제로 가장 빠름
```

### 4.5 병합 정렬 (Merge Sort)
```
분할 정복, 항상 O(n log n) 보장

과정:
[5, 3, 8, 1, 2]
      ↓ 분할
[5, 3] [8, 1, 2]
  ↓       ↓
[5][3] [8][1,2]
         ↓
       [1][2]
      ↓ 병합
[3, 5] [1, 2, 8]
      ↓ 병합
[1, 2, 3, 5, 8]

시간복잡도: O(n log n)
특징: 안정 정렬, 추가 공간 필요
```

## 5. 코드 예시

```python
from typing import List

def bubble_sort(arr: List[int]) -> List[int]:
    """버블 정렬"""
    n = len(arr)
    result = arr.copy()

    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if result[j] > result[j+1]:
                result[j], result[j+1] = result[j+1], result[j]
                swapped = True
        if not swapped:
            break
    return result

def selection_sort(arr: List[int]) -> List[int]:
    """선택 정렬"""
    n = len(arr)
    result = arr.copy()

    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result

def insertion_sort(arr: List[int]) -> List[int]:
    """삽입 정렬"""
    result = arr.copy()

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j+1] = result[j]
            j -= 1
        result[j+1] = key
    return result

def quick_sort(arr: List[int]) -> List[int]:
    """퀵 정렬"""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr: List[int]) -> List[int]:
    """병합 정렬"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """병합 함수"""
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

def heap_sort(arr: List[int]) -> List[int]:
    """힙 정렬"""
    import heapq
    result = arr.copy()
    heapq.heapify(result)
    return [heapq.heappop(result) for _ in range(len(result))]


# 사용 예시
print("=== 정렬 알고리즘 비교 ===\n")

data = [64, 34, 25, 12, 22, 11, 90]
print(f"원본: {data}")
print(f"\n버블 정렬: {bubble_sort(data)}")
print(f"선택 정렬: {selection_sort(data)}")
print(f"삽입 정렬: {insertion_sort(data)}")
print(f"퀵 정렬:   {quick_sort(data)}")
print(f"병합 정렬: {merge_sort(data)}")
print(f"힙 정렬:   {heap_sort(data)}")

# 성능 비교
import time
import random

large_data = [random.randint(1, 10000) for _ in range(1000)]

print("\n=== 1000개 데이터 성능 비교 ===")
algorithms = [
    ("버블 정렬", bubble_sort),
    ("선택 정렬", selection_sort),
    ("삽입 정렬", insertion_sort),
    ("퀵 정렬", quick_sort),
    ("병합 정렬", merge_sort),
    ("힙 정렬", heap_sort),
]

for name, func in algorithms:
    start = time.time()
    func(large_data)
    elapsed = time.time() - start
    print(f"{name}: {elapsed*1000:.2f}ms")
```

## 6. 안정 정렬 vs 불안정 정렬

```
안정 정렬 (Stable Sort):
- 같은 값의 상대적 순서 유지
- 예: [(3,A), (2,B), (3,C)] → [(2,B), (3,A), (3,C)]
- 버블, 삽입, 병합

불안정 정렬 (Unstable Sort):
- 같은 값의 순서 바뀔 수 있음
- 선택, 퀵, 힙

예시:
원본: [(3, 'A'), (2, 'B'), (3, 'C')]

안정 정렬 후: [(2, 'B'), (3, 'A'), (3, 'C')]
              → (3,A)가 (3,C)보다 앞에 있음 유지

불안정 정렬 후: [(2, 'B'), (3, 'C'), (3, 'A')]
              → 순서 바뀔 수 있음
```

## 7. 내부 정렬 vs 외부 정렬

```
내부 정렬 (Internal Sort):
- 메모리에 모든 데이터 적재 가능
- 버블, 퀵, 병합, 힙 등

외부 정렬 (External Sort):
- 데이터가 메모리보다 커서 디스크 사용
- 외부 병합 정렬
- 대용량 파일 정렬
```

## 8. 장단점

### 단순 정렬 (O(n²))
| 장점 | 단점 |
|-----|------|
| 구현 쉬움 | 느림 |
| 적은 공간 | 대용량 부적합 |
| 거의 정렬된 경우 빠름 |  |

### 효율 정렬 (O(n log n))
| 장점 | 단점 |
|-----|------|
| 빠름 | 구현 복잡 |
| 대용량 처리 | 추가 공간 (병합) |
|  | 최악 O(n²) (퀵) |

## 9. 실무에선? (기술사적 판단)
- **일반적**: 퀵 정렬 (평균 가장 빠름)
- **안정성 필요**: 병합 정렬
- **거의 정렬됨**: 삽입 정렬
- **메모리 제한**: 힙 정렬
- **라이브러리**: TimSort (Python, Java)

## 10. 관련 개념
- 시간복잡도
- 분할 정복
- 힙
- 이진 탐색

---

## 어린이를 위한 종합 설명

**정렬은 "줄 세우기"예요!**

### 왜 필요할까요? 📚
```
엉망인 책장:
"원하는 책 찾기 힘들어요!" 😫

정리된 책장:
"바로 찾을 수 있어요!" 😊
```

### 정렬 방법들 🔢
```
버블 정렬: 옆에랑 계속 바꾸기
  "너랑 나랑 바꿔!"

선택 정렬: 제일 작은 걸 앞으로
  "제일 작은 거 찾았다!"

삽입 정렬: 알맞은 자리에 끼워넣기
  "여기가 내 자리!"

퀵 정렬: 기준보다 작은 건 왼쪽, 큰 건 오른쪽
  "5보다 작아? 왼쪽!"
```

### 빠르기 비교 🏃
```
느림: 버블, 선택, 삽입
  O(n²) - 친구 100명이면 10,000번!

빠름: 퀵, 병합, 힙
  O(n log n) - 친구 100명이면 660번!
```

**비밀**: 컴퓨터도 정렬을 배워요! 💻✨
