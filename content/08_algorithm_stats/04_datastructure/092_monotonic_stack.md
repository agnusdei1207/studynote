---
title: "Monotonic Queue"
date: "2026-03-03"
tags:
  - "studynote-algorithm-stats"
weight: 92
---
> **핵심 인사이트 3줄**
> 1. 단조 스택(Monotonic Stack)은 스택 내 원소가 단조 증가 또는 단조 감소 순서를 유지하도록 관리해, 각 원소의 Next Greater/Smaller Element를 O(n)에 찾는 기법이다.
> 2. 히스토그램 최대 직사각형·빗물 트래핑·주식 가격 스팬 등 "현재 원소보다 크거나 작은 가장 가까운 원소"를 찾는 문제 유형에 최적화된 패턴이다.
> 3. 단조 큐(Monotonic Queue)는 슬라이딩 윈도우 최대/최소값을 O(n)에 계산해, O(n·k) 브루트 포스 대비 압도적 성능을 제공한다.

---

## Ⅰ. 단조 스택의 정의와 동작

단조 스택(Monotonic Stack)은 <strong>스택의 원소가 항상 단조 증가 또는 단조 감소 순서를 유지</strong>하는 스택이다.

```
단조 감소 스택 (Next Greater Element 찾기):
  배열: [2, 1, 4, 3, 5]

  push 2 -> [2]
  push 1 -> [2, 1]  (1 < 2이므로 그냥 push)
  push 4 -> 4 > 1: pop 1 -> 1의 NGE=4
           4 > 2: pop 2 -> 2의 NGE=4
           -> [4]
  push 3 -> [4, 3]  (3 < 4이므로 그냥 push)
  push 5 -> 5 > 3: pop 3 -> 3의 NGE=5
           5 > 4: pop 4 -> 4의 NGE=5
           -> [5]

  결과 NGE: [4, 4, 5, 5, -1]
```

📢 **섹션 요약 비유**: 단조 스택은 키 순으로 줄 서기다 — 뒤에서 더 키 큰 사람(NGE)이 오면 본인보다 키 작은 사람들을 전부 내보내고, 그 사람들의 "앞에 키 큰 사람"을 기록한다.

---

## Ⅱ. NGE (Next Greater Element) 구현

```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # 인덱스 저장

    for i in range(n):
        # 현재 값이 스택 top보다 크면 -> pop하고 NGE 기록
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    # 스택에 남은 인덱스 -> NGE 없음 (-1 그대로)
    return result

# 예시
nums = [2, 1, 4, 3, 5]
print(next_greater_element(nums))  # [4, 4, 5, 5, -1]
```

<strong>시간 복잡도</strong>: O(n) — 각 원소는 스택에 1번 push, 1번 pop

📢 **섹션 요약 비유**: NGE 알고리즘은 "나보다 키 큰 사람이 뒤에 오면 알려줘" 시스템이다 — 기다리다가 더 큰 사람이 오면 모든 작은 사람에게 동시에 알림을 보낸다.

---

## Ⅲ. 히스토그램 최대 직사각형 (LeetCode 84)

가장 유명한 단조 스택 응용 문제다.

```python
def largest_rectangle(heights):
    stack = []  # 단조 증가 스택 (인덱스)
    max_area = 0
    heights.append(0)  # 센티넬

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area

# 예시: heights = [2, 1, 5, 6, 2, 3]
# 최대 직사각형 넓이 = 10 (높이 5·6 두 칸)
print(largest_rectangle([2, 1, 5, 6, 2, 3]))  # 10
```

📢 **섹션 요약 비유**: 히스토그램 문제는 도시 건물 사이 가장 큰 빈 공간 찾기다 — 단조 스택으로 각 건물이 너비를 얼마나 차지할 수 있는지 O(n)에 계산한다.

---

## Ⅳ. 단조 큐 (Monotonic Queue) — 슬라이딩 윈도우

단조 큐(Monotonic Queue, Deque)는 <strong>슬라이딩 윈도우의 최대/최소값을 O(1)에 조회</strong>한다.

```python
from collections import deque

def sliding_window_max(nums, k):
    dq = deque()  # 인덱스 저장, 값은 단조 감소
    result = []

    for i in range(len(nums)):
        # 윈도우 범위 밖 원소 제거 (앞에서)
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # 현재 값보다 작은 원소 제거 (뒤에서) -> 단조 감소 유지
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        # 윈도우 완성 후 최대값 = 큐의 맨 앞
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# 예시: nums=[1,3,-1,-3,5,3,6,7], k=3
# 결과: [3, 3, 5, 5, 6, 7]
```

<strong>시간 복잡도</strong>: O(n) — 각 원소 최대 2회 처리 (push+pop)

📢 **섹션 요약 비유**: 슬라이딩 윈도우 최대값은 창문 밖 가장 높은 건물이다 — 창문이 이동할 때마다 전체를 다시 확인(O(nk))하는 대신, 이미 지나친 건물(만료 원소)만 제거하면 된다.

---

## Ⅴ. 단조 스택 응용 패턴

| 문제 유형              | 사용 스택     | 시간 복잡도     |
|---------------------|------------|--------------|
| Next Greater Element | 단조 감소 스택 | O(n)         |
| Next Smaller Element | 단조 증가 스택 | O(n)         |
| 히스토그램 최대 직사각형 | 단조 증가 스택 | O(n)        |
| 빗물 트래핑 (Trapping Rain) | 단조 감소 스택 | O(n)    |
| 주식 가격 스팬        | 단조 감소 스택 | O(n) 평균    |
| 슬라이딩 윈도우 최대   | 단조 큐      | O(n)         |

📢 **섹션 요약 비유**: 단조 스택/큐는 스위스 아미 나이프다 — "가장 가까운 크거나 작은 원소" 유형 문제를 하나의 패턴으로 O(n)에 모두 해결한다.

---

## 📌 관련 개념 맵

```
단조 스택/큐
+-- 단조 스택 (Monotonic Stack)
|   +-- 단조 증가 스택 (Next Smaller Element)
|   +-- 단조 감소 스택 (Next Greater Element)
+-- 주요 응용
|   +-- NGE / NSE 찾기
|   +-- 히스토그램 최대 직사각형 (LC 84)
|   +-- 빗물 트래핑 (LC 42)
+-- 단조 큐 (Monotonic Deque)
|   +-- 슬라이딩 윈도우 최대/최소 (LC 239)
+-- 복잡도
    +-- O(n) — 각 원소 최대 2회 처리
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              단조 스택 발전 흐름                                 |
+--------------+--------------------+-----------------------------+
| 1980년대     | 스택 자료구조 성숙  | LIFO 기본 연산 정립          |
| 1990년대     | 히스토그램 문제    | Largest Rectangle 알고리즘   |
| 2000년대     | 프로그래밍 대회    | 코딩 인터뷰 핵심 패턴화      |
| 2010년대     | LeetCode 보급      | 단조 스택 유형 문제 체계화   |
| 2020년대     | 슬라이딩 윈도우    | 단조 큐 + DP 결합 문제 증가  |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
스택 -> 단조 스택 -> NGE/NSE -> 히스토그램
  v         v           v           v
LIFO   원소 단조성   가장 가까운  최대 면적
  v
단조 큐 -> 슬라이딩 윈도우 최대 -> O(n) 최적화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 단조 스택은 키 순으로 정렬된 줄이다 — 키 큰 사람이 오면 자기보다 작은 사람을 모두 내보내고 들어온다.
2. NGE(Next Greater Element)는 "뒤에서 처음 만나는 나보다 키 큰 사람"이다 — 단조 스택으로 모든 사람의 NGE를 한 번에 O(n)으로 찾는다.
3. 단조 큐는 움직이는 창문이다 — 창문이 이동할 때 가장 큰 값을 매번 다시 찾지 않고, 이전 정보를 재활용해 빠르게 답을 낸다.
