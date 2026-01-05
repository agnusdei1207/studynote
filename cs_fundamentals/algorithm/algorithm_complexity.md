# 알고리즘 복잡도 (Algorithm Complexity)

## 📌 개요

**알고리즘 복잡도(Algorithm Complexity)**란 알고리즘이 문제를 해결하는 데 필요한 **자원(Resource)**의 양을 정량적으로 분석하는 척도이다. 주로 **시간 복잡도(Time Complexity)**와 **공간 복잡도(Space Complexity)**로 구분된다.

---

## 1. 시간 복잡도 (Time Complexity)

### 1.1 정의

**시간 복잡도(Time Complexity)**는 알고리즘이 실행되는 데 걸리는 시간을 입력 크기(Input Size, n)의 함수로 표현한 것이다. 실제 실행 시간이 아니라 **연산 횟수(Operation Count)**를 기준으로 측정한다.

### 1.2 왜 연산 횟수인가?

실제 실행 시간은 다음과 같은 외부 요인에 영향을 받는다:
- CPU(Central Processing Unit, 중앙 처리 장치) 성능
- 프로그래밍 언어
- 컴파일러 최적화 수준
- 운영체제(Operating System, OS) 상태

따라서 **하드웨어에 독립적인 분석**을 위해 연산 횟수를 기준으로 삼는다.

### 1.3 비유로 이해하기

> 🏠 **집을 짓는 비유**
>
> 시간 복잡도는 "집을 짓는 데 벽돌 몇 개가 필요한가?"와 같다. 
> - 집 크기(n)가 커지면 필요한 벽돌 수도 증가한다.
> - 실제로 벽돌을 얼마나 빨리 쌓느냐(하드웨어)는 별개의 문제다.

---

## 2. 공간 복잡도 (Space Complexity)

### 2.1 정의

**공간 복잡도(Space Complexity)**는 알고리즘이 실행되는 동안 사용하는 **메모리(Memory) 공간**의 양을 입력 크기의 함수로 표현한 것이다.

### 2.2 구성 요소

공간 복잡도는 크게 두 부분으로 나뉜다:

| 구분 | 설명 | 예시 |
|------|------|------|
| **고정 공간 (Fixed Space)** | 입력 크기와 무관하게 필요한 공간 | 변수, 상수, 프로그램 코드 |
| **가변 공간 (Variable Space)** | 입력 크기에 비례하여 증가하는 공간 | 동적 배열, 재귀 호출 스택 |

### 2.3 비유로 이해하기

> 📦 **창고 정리 비유**
>
> 공간 복잡도는 "물건을 정리하는 데 필요한 창고 면적"과 같다.
> - 물건(n)이 많아지면 필요한 창고 면적도 커진다.
> - 정리하는 방법(알고리즘)에 따라 필요한 면적이 달라진다.

---

## 3. 점근적 표기법 (Asymptotic Notation)

입력 크기가 무한히 커질 때 알고리즘의 성능을 표현하는 방법이다.

### 3.1 빅-오 표기법 (Big-O Notation) - O(f(n))

**최악의 경우(Worst Case)**의 상한선을 나타낸다.

```
T(n) = O(f(n))

의미: T(n) ≤ c × f(n), (n ≥ n₀인 모든 n에 대해)
```

**주요 특징:**
- 가장 널리 사용되는 표기법
- 알고리즘의 **성능 보장(Upper Bound)**을 의미

### 3.2 빅-오메가 표기법 (Big-Omega Notation) - Ω(f(n))

**최선의 경우(Best Case)**의 하한선을 나타낸다.

```
T(n) = Ω(f(n))

의미: T(n) ≥ c × f(n), (n ≥ n₀인 모든 n에 대해)
```

### 3.3 빅-세타 표기법 (Big-Theta Notation) - Θ(f(n))

**평균적인 경우(Average Case)**로, 상한과 하한이 동일할 때 사용한다.

```
T(n) = Θ(f(n))

의미: c₁ × f(n) ≤ T(n) ≤ c₂ × f(n)
```

### 3.4 비유로 이해하기

> 🚗 **자동차 여행 비유**
>
> 서울에서 부산까지 가는 시간을 예측한다고 가정하자.
> - **Big-O (O)**: "아무리 늦어도 6시간 안에는 도착한다" (상한선)
> - **Big-Omega (Ω)**: "아무리 빨라도 3시간은 걸린다" (하한선)
> - **Big-Theta (Θ)**: "보통 4~5시간 걸린다" (평균적인 범위)

---

## 4. 주요 시간 복잡도 클래스

| 복잡도 | 명칭 | 예시 알고리즘 | 설명 |
|--------|------|---------------|------|
| **O(1)** | 상수 시간 (Constant Time) | 배열 인덱스 접근, 해시 테이블 조회 | 입력 크기와 무관하게 일정 |
| **O(log n)** | 로그 시간 (Logarithmic Time) | 이진 탐색 (Binary Search) | 입력이 반씩 줄어듦 |
| **O(n)** | 선형 시간 (Linear Time) | 순차 탐색, 배열 순회 | 입력 크기에 비례 |
| **O(n log n)** | 선형 로그 시간 (Linearithmic Time) | 병합 정렬 (Merge Sort), 퀵 정렬 (Quick Sort) | 효율적인 정렬 알고리즘 |
| **O(n²)** | 이차 시간 (Quadratic Time) | 버블 정렬 (Bubble Sort), 선택 정렬 (Selection Sort) | 이중 반복문 |
| **O(n³)** | 삼차 시간 (Cubic Time) | 행렬 곱셈 (나이브) | 삼중 반복문 |
| **O(2ⁿ)** | 지수 시간 (Exponential Time) | 피보나치 재귀, 부분집합 문제 | 입력마다 연산 2배 증가 |
| **O(n!)** | 팩토리얼 시간 (Factorial Time) | 외판원 문제 (TSP, Traveling Salesman Problem) 완전 탐색 | 모든 순열 탐색 |

### 4.1 성능 비교 그래프 (개념적)

```
연산 횟수
    ↑
    │                                          O(n!)
    │                                     O(2ⁿ)
    │                                O(n³)
    │                          O(n²)
    │                   O(n log n)
    │            O(n)
    │     O(log n)
    │ O(1)
    └─────────────────────────────────────────→ n (입력 크기)
```

---

## 5. 시간 복잡도 분석 방법

### 5.1 기본 연산 규칙

```
1. 순차 실행: T(n) = T₁(n) + T₂(n) → O(max(T₁, T₂))
2. 조건문: T(n) = max(T_if, T_else)
3. 반복문: T(n) = 반복 횟수 × 내부 연산 복잡도
4. 중첩 반복문: T(n) = 외부 반복 × 내부 반복 × 내부 연산
```

### 5.2 예시 분석

#### 예시 1: 단순 반복문 - O(n)
```python
def sum_array(arr):
    total = 0           # O(1)
    for num in arr:     # O(n)
        total += num    # O(1)
    return total        # O(1)
# 전체: O(1) + O(n) × O(1) + O(1) = O(n)
```

#### 예시 2: 이중 반복문 - O(n²)
```python
def print_pairs(arr):
    n = len(arr)            # O(1)
    for i in range(n):      # O(n)
        for j in range(n):  # O(n)
            print(arr[i], arr[j])  # O(1)
# 전체: O(n) × O(n) × O(1) = O(n²)
```

#### 예시 3: 이진 탐색 - O(log n)
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:              # O(log n) - 매번 절반씩 줄어듦
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## 6. 공간 복잡도 분석

### 6.1 반복문 vs 재귀

| 방식 | 공간 복잡도 | 설명 |
|------|-------------|------|
| 반복문 | O(1) | 추가 변수만 사용 |
| 재귀 | O(n) | 호출 스택(Call Stack)에 n개 프레임 저장 |

#### 예시: 팩토리얼 계산

**반복문 (O(1) 공간)**
```python
def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

**재귀 (O(n) 공간)**
```python
def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)  # n개의 스택 프레임 필요
```

### 6.2 꼬리 재귀 최적화 (TCO, Tail Call Optimization)

일부 언어/컴파일러에서는 **꼬리 재귀(Tail Recursion)**를 반복문처럼 최적화하여 O(1) 공간으로 처리할 수 있다.

```python
# 꼬리 재귀 형태
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)
```

---

## 7. 복잡도 분석 시 주의사항

### 7.1 상수 계수 무시

Big-O 표기법에서는 상수 계수를 무시한다:
- O(2n) → O(n)
- O(n/2) → O(n)
- O(100) → O(1)

### 7.2 낮은 차수 항 무시

최고 차수 항만 남긴다:
- O(n² + n) → O(n²)
- O(n³ + n² + n) → O(n³)

### 7.3 실제 성능과의 차이

**주의:** Big-O는 점근적 상한이므로 작은 입력에서는 다른 결과가 나올 수 있다.

| 상황 | 설명 |
|------|------|
| 작은 n | 상수 계수가 중요할 수 있음 |
| 캐시 친화성 | 메모리 접근 패턴이 실제 성능에 영향 |
| 분기 예측 | CPU(Central Processing Unit) 파이프라인 효율성 |

---

## 8. 복잡도 클래스 (Complexity Classes) - 계산 이론

### 8.1 P 클래스 (P Class)

**다항 시간(Polynomial Time)**에 해결 가능한 문제들의 집합

- 정의: O(n^k) 시간에 결정론적 튜링 머신(Deterministic Turing Machine)으로 해결 가능
- 예시: 정렬, 최단 경로 탐색, 이진 탐색

### 8.2 NP 클래스 (NP Class)

**NP(Nondeterministic Polynomial time)**는 비결정론적 튜링 머신으로 다항 시간에 해결되거나, 
결정론적 튜링 머신으로 다항 시간에 **검증(Verification)** 가능한 문제들의 집합

- 예시: 해밀턴 경로(Hamiltonian Path), SAT(Boolean Satisfiability Problem)

### 8.3 NP-완전 (NP-Complete)

- NP에 속하면서, 모든 NP 문제가 다항 시간에 환원(Reduction) 가능한 문제
- 한 NP-완전 문제가 P에 속하면 P = NP가 증명됨

### 8.4 NP-난해 (NP-Hard)

- 모든 NP 문제가 다항 시간에 환원 가능하지만, 자신은 NP에 속하지 않을 수도 있는 문제

```
┌──────────────────────────────────────────┐
│                  NP-Hard                 │
│  ┌────────────────────────────────┐      │
│  │           NP                   │      │
│  │   ┌────────────────────┐       │      │
│  │   │   NP-Complete      │       │      │
│  │   │ ┌───────────────┐  │       │      │
│  │   │ │      P        │  │       │      │
│  │   │ └───────────────┘  │       │      │
│  │   └────────────────────┘       │      │
│  └────────────────────────────────┘      │
└──────────────────────────────────────────┘
```

---

## 9. 실무 적용 가이드

### 9.1 복잡도 선택 기준

| 데이터 크기 (n) | 허용 가능한 복잡도 |
|-----------------|-------------------|
| n ≤ 10 | O(n!), O(2ⁿ) |
| n ≤ 20 | O(2ⁿ) |
| n ≤ 100 | O(n³) |
| n ≤ 1,000 | O(n²) |
| n ≤ 100,000 | O(n log n) |
| n ≤ 10,000,000 | O(n) |
| n > 10,000,000 | O(log n), O(1) |

### 9.2 최적화 전략

1. **알고리즘 개선**: O(n²) → O(n log n) (예: 버블 정렬 → 병합 정렬)
2. **자료구조 변경**: 리스트 → 해시 테이블 (탐색 O(n) → O(1))
3. **메모이제이션(Memoization)**: 중복 계산 방지
4. **다이나믹 프로그래밍(DP, Dynamic Programming)**: 부분 문제 결과 재활용

---

## 10. 정리

| 개념 | 핵심 내용 |
|------|----------|
| **시간 복잡도** | 연산 횟수를 입력 크기의 함수로 표현 |
| **공간 복잡도** | 메모리 사용량을 입력 크기의 함수로 표현 |
| **Big-O** | 최악의 경우 상한선 |
| **Big-Omega** | 최선의 경우 하한선 |
| **Big-Theta** | 평균적인 범위 (상한 = 하한) |
| **P vs NP** | 계산 이론에서 가장 중요한 미해결 문제 중 하나 |

---

## 📚 참고 자료

1. Cormen, T. H., et al. (2022). *Introduction to Algorithms (4th Edition)*. MIT Press.
2. Knuth, D. E. (1997). *The Art of Computer Programming, Volume 1: Fundamental Algorithms*. Addison-Wesley.
3. Sedgewick, R., & Wayne, K. (2011). *Algorithms (4th Edition)*. Addison-Wesley.
