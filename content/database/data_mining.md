+++
title = "데이터 마이닝 (Data Mining)"
date = 2025-03-01

[extra]
categories = "database-relational"
+++

# 데이터 마이닝 (Data Mining)

## 핵심 인사이트 (3줄 요약)
> **대량 데이터에서 유용한 패턴과 지식을 발견**하는 기술. 연관 규칙, 분류, 군집화, 이상 탐지 등의 기법 사용. 비즈니스 의사결정, 추천 시스템, 사기 탐지 등에 활용.

## 1. 개념
데이터 마이닝은 **대규모 데이터 집합에서 패턴, 상관관계, 유용한 정보를 자동으로 발견**하는 프로세스다.

> 비유: "데이터 금광" - 원석(데이터)에서 금(인사이트)을 캐내는 과정

## 2. KDD 프로세스

```
KDD (Knowledge Discovery in Database):

┌──────────────────────────────────────────────────────────┐
│                    1. 데이터 선택                         │
│           (Selection) - 관련 데이터 추출                  │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    2. 데이터 전처리                       │
│      (Preprocessing) - 정제, 결측치 처리, 노이즈 제거    │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    3. 데이터 변환                         │
│      (Transformation) - 정규화, 차원 축소, 특성 추출     │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    4. 데이터 마이닝                       │
│      (Data Mining) - 패턴 발견, 모델 생성                │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    5. 결과 해석 및 평가                   │
│   (Interpretation/Evaluation) - 지식 발견, 시각화        │
└──────────────────────────────────────────────────────────┘
```

## 3. 주요 기법

### 3.1 연관 규칙 (Association Rules)
```
정의: 항목 간의 연관성 발견

예: 장바구니 분석
"맥주를 사는 사람은 땅콩도 산다"

표현: {맥주} → {땅콩}

지표:
1. 지지도 (Support)
   = P(A ∩ B) = A와 B를 동시에 구매한 비율
   Support(맥주→땅콩) = 0.05 (5%)

2. 신뢰도 (Confidence)
   = P(B|A) = A를 샀을 때 B도 살 확률
   Confidence(맥주→땅콩) = 0.6 (60%)

3. 향상도 (Lift)
   = P(B|A) / P(B) = 우연보다 얼마나 더?
   Lift(맥주→땅콩) = 2.0 (2배 더 잘 삼)
```

### 3.2 분류 (Classification)
```
정의: 미리 정의된 클래스로 데이터 분류

지도 학습 (Supervised Learning)

과정:
1. 학습 데이터로 모델 학습
2. 새로운 데이터의 클래스 예측

알고리즘:
- 결정 트리 (Decision Tree)
- 나이브 베이즈 (Naive Bayes)
- 신경망 (Neural Network)
- SVM (Support Vector Machine)
- 랜덤 포레스트 (Random Forest)

예:
┌─────────────────────────────────┐
│        고객 이탈 예측           │
├─────────────────────────────────┤
│ Input: 사용 패턴, 요금, 기간   │
│ Output: 이탈 O/X               │
└─────────────────────────────────┘
```

### 3.3 군집화 (Clustering)
```
정의: 유사한 데이터끼리 그룹화

비지도 학습 (Unsupervised Learning)

특징:
- 미리 정의된 클래스 없음
- 데이터 자체의 패턴 발견

알고리즘:
- K-Means
- 계층적 군집화
- DBSCAN

예: 고객 세분화
    ┌───┐
  ┌─┤ C ├───┐
  │ └───┘   │
┌─┴─┐     ┌─┴─┐
│ A │     │ B │
└───┘     └───┘

A: 가격 민감형
B: 품질 중시형
C: 브랜드 충성형
```

### 3.4 이상 탐지 (Anomaly Detection)
```
정의: 정상 패턴에서 벗어난 데이터 발견

용도:
- 사기 탐지 (신용카드)
- 침입 탐지 (보안)
- 장애 예측 (설비)

방법:
1. 통계적 방법
   - 정규분포에서 벗어난 값

2. 거리 기반
   - 다른 데이터와 거리가 먼 것

3. 밀도 기반
   - 밀도가 낮은 영역의 데이터

예:
     ●●●●●
   ●●●●●●●
   ●●●●●●●  ← 정상
     ●●●●
         ★  ← 이상치
```

### 3.5 회귀 (Regression)
```
정의: 연속형 값 예측

종류:
1. 단순 회귀
   Y = aX + b

2. 다중 회귀
   Y = a₁X₁ + a₂X₂ + ... + b

3. 로지스틱 회귀
   P(Y=1) = 1 / (1 + e^(-z))

예:
- 주가 예측
- 매출 예측
- 온도 예측
```

### 3.6 시계열 분석 (Time Series)
```
정의: 시간 순서 데이터의 패턴 분석

구성 요소:
1. 추세 (Trend)
   ─────────────────→ 장기적 상승/하락

2. 계절성 (Seasonality)
   ↗↘↗↘↗↘ 주기적 반복

3. 순환 (Cycle)
   ↔↔↔↔ 비정기적 변동

4. 불규칙 (Irregular)
   ⚡ 예측 불가한 변동

예:
매출
  ↑    /\/\
  │   /    \  /\
  │  /      \/  \
  │ /
  └──────────────→ 시간
```

## 4. Apriori 알고리즘

```
연관 규칙 발견의 대표 알고리즘

원리: 빈번한 항목 집합만 고려

과정:
1. 후보 생성: k-항목 집합 생성
2. 빈번 항목 집합 찾기: 최소 지지도 이상
3. 연관 규칙 생성: 최소 신뢰도 이상

예:
최소 지지도 = 50%

거래 1: {A, B, C}
거래 2: {A, B}
거래 3: {A, C}
거래 4: {B, C}

1-항목 지지도:
A: 75% ✓  B: 75% ✓  C: 75% ✓

2-항목 지지도:
{A,B}: 50% ✓  {A,C}: 50% ✓  {B,C}: 50% ✓

3-항목 지지도:
{A,B,C}: 25% ✗ (제거)

규칙 생성:
{A} → {B}: 66% 신뢰도
{B} → {A}: 66% 신뢰도
```

## 5. K-Means 군집화

```
알고리즘:
1. K개의 중심점 초기화
2. 각 데이터를 가장 가까운 중심점에 할당
3. 각 클러스터의 중심점 재계산
4. 2-3 반복 (수렴할 때까지)

예: K=2

초기:
    ●1
  ●   ●
  ●   ●2
    ●

할당:
    ●●
  ●●  ●
  ●●  ●●
    ●●

재계산:
    ★1
  ●●  ●
  ●●  ★2
    ●●

최종:
    ●●
  ●●  ●
  ●●  ●●
    ●●
```

## 6. 결정 트리

```
분류를 위한 트리 구조

예: 대출 승인 여부

            ┌──────────────┐
            │  소득 > 5000? │
            └──────┬───────┘
           Yes     │     No
          ┌────────┴────────┐
          ▼                 ▼
    ┌──────────┐      ┌──────────┐
    │신용등급>A?│      │  거절     │
    └────┬─────┘      └──────────┘
   Yes   │   No
  ┌──────┴──────┐
  ▼             ▼
┌────┐       ┌────┐
│승인│       │거절│
└────┘       └────┘

분할 기준:
- 정보 이득 (Information Gain)
- 지니 계수 (Gini Index)
```

## 7. 코드 예시

```python
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from collections import Counter
import math

# ===== 연관 규칙 (Apriori) =====
class Apriori:
    """Apriori 알고리즘 구현"""

    def __init__(self, min_support: float = 0.5, min_confidence: float = 0.7):
        self.min_support = min_support
        self.min_confidence = min_confidence

    def find_frequent_itemsets(self, transactions: List[Set[str]]) -> List[Tuple[Set[str], float]]:
        """빈번 항목 집합 찾기"""
        n_transactions = len(transactions)
        frequent_itemsets = []

        # 1-항목 집합
        items = set()
        for trans in transactions:
            items.update(trans)

        current_itemsets = [frozenset([item]) for item in items]

        k = 1
        while current_itemsets:
            # 지지도 계산
            itemset_supports = []
            for itemset in current_itemsets:
                count = sum(1 for trans in transactions if itemset.issubset(trans))
                support = count / n_transactions
                if support >= self.min_support:
                    itemset_supports.append((set(itemset), support))

            if not itemset_supports:
                break

            frequent_itemsets.extend(itemset_supports)

            # 다음 k-항목 집합 생성
            k += 1
            current_itemsets = self._generate_candidates(
                [frozenset(itemset) for itemset, _ in itemset_supports],
                k
            )

        return frequent_itemsets

    def _generate_candidates(self, itemsets: List[frozenset], k: int) -> List[frozenset]:
        """후보 항목 집합 생성"""
        candidates = set()
        items = set()
        for itemset in itemsets:
            items.update(itemset)

        from itertools import combinations
        for combo in combinations(items, k):
            candidates.add(frozenset(combo))

        return list(candidates)

    def generate_rules(self, transactions: List[Set[str]]) -> List[Tuple[Set[str], Set[str], float, float]]:
        """연관 규칙 생성"""
        frequent = self.find_frequent_itemsets(transactions)
        rules = []

        for itemset, support in frequent:
            if len(itemset) < 2:
                continue

            # 모든 가능한 규칙 생성
            items = list(itemset)
            for i in range(1, len(items)):
                from itertools import combinations
                for antecedent in combinations(items, i):
                    antecedent = set(antecedent)
                    consequent = itemset - antecedent

                    # 신뢰도 계산
                    ant_count = sum(1 for trans in transactions
                                    if antecedent.issubset(trans))
                    both_count = sum(1 for trans in transactions
                                     if itemset.issubset(trans))

                    confidence = both_count / ant_count if ant_count > 0 else 0

                    if confidence >= self.min_confidence:
                        rules.append((antecedent, consequent, support, confidence))

        return rules


# ===== K-Means 군집화 =====
import random

class KMeans:
    """K-Means 군집화 구현"""

    def __init__(self, k: int = 3, max_iters: int = 100):
        self.k = k
        self.max_iters = max_iters
        self.centroids = []

    def fit(self, data: List[List[float]]):
        """군집화 수행"""
        # 중심점 초기화
        self.centroids = random.sample(data, self.k)

        for _ in range(self.max_iters):
            # 클러스터 할당
            clusters = [[] for _ in range(self.k)]
            for point in data:
                distances = [self._distance(point, c) for c in self.centroids]
                cluster_idx = distances.index(min(distances))
                clusters[cluster_idx].append(point)

            # 중심점 재계산
            new_centroids = []
            for cluster in clusters:
                if cluster:
                    new_centroid = [sum(dim) / len(cluster) for dim in zip(*cluster)]
                    new_centroids.append(new_centroid)
                else:
                    new_centroids.append(random.choice(data))

            # 수렴 확인
            if self._centroids_equal(self.centroids, new_centroids):
                break

            self.centroids = new_centroids

        return clusters

    def predict(self, point: List[float]) -> int:
        """새 데이터의 클러스터 예측"""
        distances = [self._distance(point, c) for c in self.centroids]
        return distances.index(min(distances))

    def _distance(self, p1: List[float], p2: List[float]) -> float:
        """유클리드 거리"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def _centroids_equal(self, c1: List, c2: List, tolerance: float = 0.001) -> bool:
        """중심점 동일 여부"""
        for a, b in zip(c1, c2):
            if self._distance(a, b) > tolerance:
                return False
        return True


# ===== 결정 트리 =====
class DecisionTree:
    """간단한 결정 트리 구현"""

    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X: List[List], y: List[str]):
        """트리 학습"""
        self.tree = self._build_tree(X, y, depth=0)

    def predict(self, X: List[List]) -> List[str]:
        """예측"""
        return [self._predict_one(x, self.tree) for x in X]

    def _build_tree(self, X: List, y: List[str], depth: int):
        """트리 구성"""
        # 종료 조건
        if depth >= self.max_depth or len(set(y)) == 1:
            return self._most_common(y)

        # 최적 분할 찾기
        best_feature, best_value = self._find_best_split(X, y)

        if best_feature is None:
            return self._most_common(y)

        # 분할
        left_X, left_y, right_X, right_y = self._split(X, y, best_feature, best_value)

        return {
            'feature': best_feature,
            'value': best_value,
            'left': self._build_tree(left_X, left_y, depth + 1),
            'right': self._build_tree(right_X, right_y, depth + 1)
        }

    def _find_best_split(self, X: List, y: List[str]) -> Tuple[int, any]:
        """최적 분할 찾기"""
        best_gain = 0
        best_feature = None
        best_value = None

        for feature in range(len(X[0])):
            values = set(x[feature] for x in X)
            for value in values:
                left_y = [y[i] for i, x in enumerate(X) if x[feature] == value]
                right_y = [y[i] for i, x in enumerate(X) if x[feature] != value]

                if not left_y or not right_y:
                    continue

                gain = self._information_gain(y, left_y, right_y)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_value = value

        return best_feature, best_value

    def _information_gain(self, parent: List, left: List, right: List) -> float:
        """정보 이득"""
        def entropy(labels):
            counts = Counter(labels)
            total = len(labels)
            return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)

        n = len(parent)
        return entropy(parent) - (len(left) / n * entropy(left) + len(right) / n * entropy(right))

    def _split(self, X: List, y: List, feature: int, value) -> Tuple[List, List, List, List]:
        """데이터 분할"""
        left_X = [x for x in X if x[feature] == value]
        left_y = [y[i] for i, x in enumerate(X) if x[feature] == value]
        right_X = [x for x in X if x[feature] != value]
        right_y = [y[i] for i, x in enumerate(X) if x[feature] != value]
        return left_X, left_y, right_X, right_y

    def _most_common(self, y: List) -> str:
        """최빈값"""
        return Counter(y).most_common(1)[0][0]

    def _predict_one(self, x: List, node) -> str:
        """단일 예측"""
        if isinstance(node, str):
            return node

        if x[node['feature']] == node['value']:
            return self._predict_one(x, node['left'])
        else:
            return self._predict_one(x, node['right'])


# ===== 사용 예시 =====
print("=== 연관 규칙 (Apriori) 테스트 ===")
transactions = [
    {'빵', '우유'},
    {'빵', '기저귀', '맥주', '달걀'},
    {'우유', '기저귀', '맥주', '콜라'},
    {'빵', '우유', '기저귀', '맥주'},
    {'빵', '우유', '기저귀', '콜라'}
]

apriori = Apriori(min_support=0.4, min_confidence=0.6)
rules = apriori.generate_rules(transactions)

print("연관 규칙:")
for ant, cons, sup, conf in rules:
    print(f"  {ant} → {cons}: 지지도={sup:.2f}, 신뢰도={conf:.2f}")

print("\n=== K-Means 군집화 테스트 ===")
data = [
    [1, 1], [1.5, 1.5], [2, 2],  # 클러스터 1
    [8, 8], [8.5, 8.5], [9, 9],  # 클러스터 2
    [15, 15], [15.5, 15.5], [16, 16]  # 클러스터 3
]

kmeans = KMeans(k=3)
clusters = kmeans.fit(data)
print("군집화 완료")
print(f"중심점: {kmeans.centroids}")

print("\n=== 결정 트리 테스트 ===")
X = [
    ['맑음', '고', '보통'],
    ['맑음', '고', '높음'],
    ['흐림', '고', '높음'],
    ['비', '중', '높음'],
    ['비', '낮', '보통'],
    ['흐림', '낮', '보통']
]
y = ['아니오', '아니오', '예', '예', '예', '예']

dt = DecisionTree(max_depth=3)
dt.fit(X, y)

test_data = [['맑음', '낮', '보통'], ['비', '고', '높음']]
predictions = dt.predict(test_data)
print(f"예측 결과: {predictions}")
```

## 8. 마이닝 기법 선택

| 목적 | 적합한 기법 | 예시 |
|------|------------|------|
| 패턴 발견 | 연관 규칙 | 장바구니 분석 |
| 분류/예측 | 분류, 회귀 | 이탈 예측 |
| 그룹화 | 군집화 | 고객 세분화 |
| 이상 발견 | 이상 탐지 | 사기 탐지 |
| 미래 예측 | 시계열 | 수요 예측 |

## 9. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 통찰력 | 숨겨진 패턴 발견 |
| 자동화 | 대규모 데이터 자동 분석 |
| 의사결정 | 데이터 기반 의사결정 |
| 경쟁력 | 비즈니스 인사이트 |

### 단점
| 단점 | 설명 |
|-----|------|
| 복잡성 | 기술적 난이도 |
| 데이터 품질 | 잘못된 데이터 → 잘못된 결과 |
| 과적합 | 학습 데이터에만 맞는 모델 |
| 해석 | 결과 해석의 어려움 |

## 10. 실무에선? (기술사적 판단)
- **추천 시스템**: 연관 규칙 + 협업 필터링
- **CRM**: 군집화로 고객 세분화
- **금융**: 이상 탐지로 사기 탐지
- **마케팅**: 분류로 타겟팅
- **공급망**: 시계열로 수요 예측
- **도구**: Python (scikit-learn, pandas), R, Spark MLlib

## 11. 관련 개념
- 기계 학습 (Machine Learning)
- 데이터 웨어하우스
- 비즈니스 인텔리전스 (BI)
- 빅데이터

---

## 어린이를 위한 종합 설명

**데이터 마이닝은 "데이터 보물찾기"예요!**

### 무엇을 찾을까요? 💎
```
데이터 속에 숨겨진 보물:
- 패턴: "비가 오면 우산이 잘 팔려요"
- 규칙: "사과를 산 사람은 배도 사요"
- 이상: "평소와 다른 행동"
```

### 주요 기법 🔍
```
1. 연관 규칙:
   "A를 사면 B도 산다"
   🛒 맥주 → 땅콩

2. 분류:
   "이건 어떤 종류?"
   📧 스팸인가요? 아닌가요?

3. 군집화:
   "비슷한 것끼리 모으기"
   👥 고객을 그룹으로

4. 이상 탐지:
   "이상한 것 찾기"
   🚨 수상한 카드 사용
```

### 어떻게 쓸까요? 🎯
```
- 쇼핑몰: 추천 상품
- 은행: 사기 탐지
- 병원: 질병 예측
- 게임: 이탈 예측
```

**비밀**: 넷플릭스가 뭘 추천해주는지 알죠? 그게 데이터 마이닝이에요! 🎬✨
