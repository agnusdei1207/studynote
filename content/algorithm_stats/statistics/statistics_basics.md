+++
title = "통계학 기초 (Statistics Basics)"
date = 2025-03-01

[extra]
categories = "algorithm_stats-statistics"
+++

# 통계학 기초 (Statistics Basics)

## 핵심 인사이트 (3줄 요약)
> **데이터를 수집, 분석, 해석하는 학문**. 기술통계(요약)와 추론통계(일반화)로 분류. 평균, 분산, 확률분포가 기본 개념.

## 1. 개념
통계학은 **데이터를 수집, 분석, 해석하여 의사결정에 활용**하는 학문이다.

> 비유: "데이터 번역기" - 숫자들을 의미 있는 정보로 변환

## 2. 통계학 분류

```
┌────────────────────────────────────────────────────────┐
│                   통계학 분류                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 기술 통계 (Descriptive Statistics)                 │
│     ┌────────────────────────────────────────────┐    │
│     │ 수집한 데이터를 요약, 정리, 시각화         │    │
│     │                                            │    │
│     │ • 중심 경향: 평균, 중앙값, 최빈값          │    │
│     │ • 산포도: 분산, 표준편차, 범위            │    │
│     │ • 분포: 히스토그램, 박스플롯               │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
│  2. 추론 통계 (Inferential Statistics)                 │
│     ┌────────────────────────────────────────────┐    │
│     │ 표본으로부터 모집단을 추정                 │    │
│     │                                            │    │
│     │ • 추정: 점추정, 구간추정                   │    │
│     │ • 가설 검정: t검정, 카이제곱검정          │    │
│     │ • 상관분석, 회귀분석                       │    │
│     └────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 중심 경향성

```
┌────────────────────────────────────────────────────────┐
│                  중심 경향성 측도                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 평균 (Mean)                                        │
│     x̄ = (x₁ + x₂ + ... + xₙ) / n                      │
│     • 모든 값의 합 / 개수                              │
│     • 이상치에 민감                                    │
│                                                        │
│  2. 중앙값 (Median)                                    │
│     • 정렬 후 가운데 값                                │
│     • 이상치에 강건                                    │
│     • 홀수: 가운데, 짝수: 가운데 두 값의 평균         │
│                                                        │
│  3. 최빈값 (Mode)                                      │
│     • 가장 자주 나타나는 값                            │
│     • 명목형 데이터에 사용                             │
│                                                        │
│  예시: [1, 2, 2, 3, 100]                              │
│  • 평균: 21.6 ← 이상치 영향                           │
│  • 중앙값: 2                                           │
│  • 최빈값: 2                                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 산포도

```
┌────────────────────────────────────────────────────────┐
│                     산포도 측도                         │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 범위 (Range)                                       │
│     Range = 최댓값 - 최솟값                            │
│                                                        │
│  2. 분산 (Variance)                                    │
│     σ² = Σ(xᵢ - μ)² / n                               │
│     s² = Σ(xᵢ - x̄)² / (n-1)  [표본]                  │
│     • 평균으로부터의 거리 제곱 평균                    │
│                                                        │
│  3. 표준편차 (Standard Deviation)                      │
│     σ = √분산                                          │
│     • 원래 단위로 환산                                 │
│     • 데이터의 퍼짐 정도                               │
│                                                        │
│  4. 변동계수 (CV)                                      │
│     CV = (표준편차 / 평균) × 100                       │
│     • 단위가 다른 데이터 비교                          │
│                                                        │
│  5. 사분위수 (Quartiles)                               │
│     Q1: 25%, Q2: 50%, Q3: 75%                         │
│     IQR = Q3 - Q1 (사분위 범위)                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 5. 코드 예시

```python
from typing import List, Dict, Tuple
from collections import Counter
import math

class DescriptiveStatistics:
    """기술 통계"""

    @staticmethod
    def mean(data: List[float]) -> float:
        """평균"""
        return sum(data) / len(data)

    @staticmethod
    def median(data: List[float]) -> float:
        """중앙값"""
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2

        if n % 2 == 0:
            return (sorted_data[mid-1] + sorted_data[mid]) / 2
        return sorted_data[mid]

    @staticmethod
    def mode(data: List[float]) -> List[float]:
        """최빈값"""
        counts = Counter(data)
        max_count = max(counts.values())
        return [val for val, count in counts.items() if count == max_count]

    @staticmethod
    def variance(data: List[float], population: bool = True) -> float:
        """분산"""
        m = DescriptiveStatistics.mean(data)
        n = len(data)
        divisor = n if population else n - 1
        return sum((x - m) ** 2 for x in data) / divisor

    @staticmethod
    def std_dev(data: List[float], population: bool = True) -> float:
        """표준편차"""
        return math.sqrt(DescriptiveStatistics.variance(data, population))

    @staticmethod
    def quartiles(data: List[float]) -> Tuple[float, float, float]:
        """사분위수"""
        sorted_data = sorted(data)
        n = len(sorted_data)

        def get_percentile(p: float) -> float:
            idx = p * (n - 1)
            lower = int(idx)
            upper = lower + 1
            if upper >= n:
                return sorted_data[lower]
            weight = idx - lower
            return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

        return get_percentile(0.25), get_percentile(0.5), get_percentile(0.75)

    @staticmethod
    def describe(data: List[float]) -> Dict:
        """요약 통계"""
        q1, q2, q3 = DescriptiveStatistics.quartiles(data)
        return {
            'count': len(data),
            'mean': DescriptiveStatistics.mean(data),
            'median': q2,
            'mode': DescriptiveStatistics.mode(data),
            'std': DescriptiveStatistics.std_dev(data),
            'variance': DescriptiveStatistics.variance(data),
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data),
            'Q1': q1,
            'Q3': q3,
            'IQR': q3 - q1
        }

class ProbabilityDistribution:
    """확률 분포"""

    @staticmethod
    def normal_pdf(x: float, mean: float, std: float) -> float:
        """정규분포 확률밀도함수"""
        coefficient = 1 / (std * math.sqrt(2 * math.pi))
        exponent = -((x - mean) ** 2) / (2 * std ** 2)
        return coefficient * math.exp(exponent)

    @staticmethod
    def binomial_pmf(k: int, n: int, p: float) -> float:
        """이항분포 확률질량함수"""
        from math import comb
        return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

    @staticmethod
    def poisson_pmf(k: int, lam: float) -> float:
        """포아송분포 확률질량함수"""
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

class CorrelationAnalysis:
    """상관분석"""

    @staticmethod
    def covariance(x: List[float], y: List[float]) -> float:
        """공분산"""
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)

    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """피어슨 상관계수"""
        cov = CorrelationAnalysis.covariance(x, y)
        std_x = DescriptiveStatistics.std_dev(x, population=False)
        std_y = DescriptiveStatistics.std_dev(y, population=False)
        return cov / (std_x * std_y)


# 사용 예시
print("=== 통계학 기초 시연 ===\n")

data = [85, 90, 78, 92, 88, 76, 95, 89, 82, 91]

# 기술 통계
print("--- 기술 통계 ---")
stats = DescriptiveStatistics.describe(data)
print(f"데이터: {data}")
print(f"개수: {stats['count']}")
print(f"평균: {stats['mean']:.2f}")
print(f"중앙값: {stats['median']:.2f}")
print(f"표준편차: {stats['std']:.2f}")
print(f"범위: {stats['range']}")
print(f"IQR: {stats['IQR']:.2f}")

# 확률 분포
print("\n--- 확률 분포 ---")
print(f"정규분포 P(X=50|μ=50,σ=10): {ProbabilityDistribution.normal_pdf(50, 50, 10):.4f}")
print(f"이항분포 P(X=3|n=10,p=0.5): {ProbabilityDistribution.binomial_pmf(3, 10, 0.5):.4f}")
print(f"포아송분포 P(X=2|λ=3): {ProbabilityDistribution.poisson_pmf(2, 3):.4f}")

# 상관분석
print("\n--- 상관분석 ---")
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
corr = CorrelationAnalysis.correlation(x, y)
print(f"X: {x}")
print(f"Y: {y}")
print(f"상관계수: {corr:.4f}")
