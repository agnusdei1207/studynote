+++
title = "동적계획법 (Dynamic Programming)"
date = 2025-03-01

[extra]
categories = "algorithm_stats-algorithm"
+++

# 동적계획법 (Dynamic Programming)

## 핵심 인사이트 (3줄 요약)
> **중복되는 부분 문제의 결과를 저장(메모이제이션)하여 효율적으로 해결**. 최적 부분 구조와 중복 부분 문제가 핵심 조건. Top-down vs Bottom-up 두 가지 방식.

## 1. 개념
동적계획법(Dynamic Programming, DP)은 **복잡한 문제를 작은 부분 문제로 나누어 해결하고, 그 결과를 저장하여 중복 계산을 피하는** 알고리즘 설계 기법이다.

> 비유: "수학 공식 암기" - 이전에 계산한 결과를 적어두고 다시 사용

## 2. DP 적용 조건

```
┌────────────────────────────────────────────────────────┐
│                  DP 적용 조건                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 최적 부분 구조 (Optimal Substructure)              │
│     ┌────────────────────────────────────────────┐    │
│     │ 문제의 최적 해가 부분 문제의 최적 해로     │    │
│     │ 구성될 때                                  │    │
│     │                                            │    │
│     │ 예: 최단 경로                              │    │
│     │ A→C 최단 경로 = A→B 최단 + B→C 최단       │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 중복 부분 문제 (Overlapping Subproblems)           │
│     ┌────────────────────────────────────────────┐    │
│     │ 같은 부분 문제가 여러 번 반복될 때         │    │
│     │                                            │    │
│     │ 예: 피보나치                               │    │
│     │ F(5) = F(4) + F(3)                         │    │
│     │ F(4) = F(3) + F(2)  ← F(3) 중복           │    │
│     │ F(3) = F(2) + F(1)  ← F(2) 중복           │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. DP 구현 방식

```
┌────────────────────────────────────────────────────────┐
│                  DP 구현 방식                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. Top-down (메모이제이션)                            │
│     ┌────────────────────────────────────────────┐    │
│     │ • 재귀 호출                                │    │
│     │ • 필요한 문제만 해결                       │    │
│     │ • 캐시(메모) 사용                          │    │
│     │                                            │    │
│     │ def fib(n, memo={}):                       │    │
│     │     if n in memo: return memo[n]          │    │
│     │     if n <= 1: return n                   │    │
│     │     memo[n] = fib(n-1) + fib(n-2)         │    │
│     │     return memo[n]                         │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. Bottom-up (타뷸레이션)                             │
│     ┌────────────────────────────────────────────┐    │
│     │ • 반복문 사용                              │    │
│     │ • 작은 문제부터 순차적 해결                │    │
│     │ • 보통 더 효율적                           │    │
│     │                                            │    │
│     │ def fib(n):                                │    │
│     │     dp = [0] * (n+1)                      │    │
│     │     dp[1] = 1                              │    │
│     │     for i in range(2, n+1):               │    │
│     │         dp[i] = dp[i-1] + dp[i-2]         │    │
│     │     return dp[n]                           │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 대표적인 DP 문제

```
┌────────────────────────────────────────────────────────┐
│                  대표 DP 문제                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 피보나치 수열                                      │
│     F(n) = F(n-1) + F(n-2)                            │
│     시간: O(n) vs O(2^n) (재귀)                        │
│                                                        │
│  2. 최장 공통 부분 수열 (LCS)                          │
│     두 수열의 공통 부분 중 가장 긴 것                  │
│     시간: O(mn)                                        │
│                                                        │
│  3. 배낭 문제 (Knapsack)                               │
│     무게 제한 내 최대 가치                             │
│     시간: O(nW)                                        │
│                                                        │
│  4. 동전 교환                                          │
│     금액을 만드는 최소 동전 수                         │
│     시간: O(nm)                                        │
│                                                        │
│  5. 최단 경로 (Floyd-Warshall)                         │
│     모든 쌍 최단 경로                                  │
│     시간: O(V³)                                        │
│                                                        │
│  6. 편집 거리 (Edit Distance)                          │
│     문자열 변환 최소 연산                              │
│     시간: O(mn)                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from typing import List, Dict
from functools import lru_cache

class DynamicProgramming:
    """동적계획법 예시"""

    # 1. 피보나치
    @staticmethod
    def fib_naive(n: int) -> int:
        """일반 재귀 - O(2^n)"""
        if n <= 1:
            return n
        return DynamicProgramming.fib_naive(n-1) + DynamicProgramming.fib_naive(n-2)

    @staticmethod
    def fib_memo(n: int, memo: Dict[int, int] = None) -> int:
        """메모이제이션 - O(n)"""
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = DynamicProgramming.fib_memo(n-1, memo) + DynamicProgramming.fib_memo(n-2, memo)
        return memo[n]

    @staticmethod
    def fib_dp(n: int) -> int:
        """바텀업 DP - O(n)"""
        if n <= 1:
            return n
        dp = [0] * (n + 1)
        dp[1] = 1
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]

    # 2. 최장 공통 부분 수열 (LCS)
    @staticmethod
    def lcs(s1: str, s2: str) -> int:
        """LCS 길이 - O(mn)"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[m][n]

    # 3. 배낭 문제
    @staticmethod
    def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
        """0-1 배낭 문제 - O(nW)"""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        dp[i-1][w],  # 포함 안 함
                        dp[i-1][w - weights[i-1]] + values[i-1]  # 포함
                    )
                else:
                    dp[i][w] = dp[i-1][w]

        return dp[n][capacity]

    # 4. 동전 교환
    @staticmethod
    def coin_change(coins: List[int], amount: int) -> int:
        """최소 동전 수 - O(nm)"""
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

    # 5. 계단 오르기
    @staticmethod
    def climb_stairs(n: int) -> int:
        """n계단 오르는 방법 수 (1 or 2칸)"""
        if n <= 2:
            return n
        dp = [0] * (n + 1)
        dp[1], dp[2] = 1, 2

        for i in range(3, n + 1):
            dp[i] = dp[i-1] + dp[i-2]

        return dp[n]

    # 6. 최대 부분 배열 합 (Kadane)
    @staticmethod
    def max_subarray(nums: List[int]) -> int:
        """연속된 부분 배열의 최대 합 - O(n)"""
        if not nums:
            return 0

        max_sum = nums[0]
        current_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum


# 사용 예시
print("=== 동적계획법 시연 ===\n")

# 피보나치
print("--- 피보나치 ---")
n = 10
print(f"F({n}) 메모이제이션: {DynamicProgramming.fib_memo(n)}")
print(f"F({n}) 바텀업: {DynamicProgramming.fib_dp(n)}")

# LCS
print("\n--- 최장 공통 부분 수열 ---")
s1, s2 = "ABCBDAB", "BDCAB"
print(f"'{s1}' vs '{s2}'")
print(f"LCS 길이: {DynamicProgramming.lcs(s1, s2)}")

# 배낭 문제
print("\n--- 배낭 문제 ---")
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5
print(f"무게: {weights}, 가치: {values}")
print(f"용량 {capacity}일 때 최대 가치: {DynamicProgramming.knapsack(weights, values, capacity)}")

# 동전 교환
print("\n--- 동전 교환 ---")
coins = [1, 2, 5]
amount = 11
print(f"동전: {coins}, 금액: {amount}")
print(f"최소 동전 수: {DynamicProgramming.coin_change(coins, amount)}")

# 계단 오르기
print("\n--- 계단 오르기 ---")
n = 5
print(f"{n}계단 오르는 방법: {DynamicProgramming.climb_stairs(n)}")

# 최대 부분 배열
print("\n--- 최대 부분 배열 합 ---")
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"배열: {nums}")
print(f"최대 부분 배열 합: {DynamicProgramming.max_subarray(nums)}")
