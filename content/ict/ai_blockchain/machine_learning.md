+++
title = "머신러닝 (Machine Learning)"
date = 2025-03-01

[extra]
categories = "ict-ai_blockchain"
+++

# 머신러닝 (Machine Learning)

## 핵심 인사이트 (3줄 요약)
> **데이터로부터 패턴을 학습하여 예측/결정**을 내리는 AI 기술. 지도/비지도/강화학습 3가지 유형. 데이터 전처리, 모델 학습, 평가의 파이프라인으로 구성.

## 1. 개념
머신러닝은 **명시적인 프로그래밍 없이 데이터로부터 학습하여 성능을 향상**시키는 알고리즘과 기술을 연구하는 분야다.

> 비유: "경험으로 배우는 컴퓨터" - 아이가 사과를 보고 배우듯 데이터로 학습

## 2. 머신러닝 유형

```
┌────────────────────────────────────────────────────────┐
│                  머신러닝 학습 유형                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 지도 학습 (Supervised Learning)                    │
│     - 정답(라벨)이 있는 데이터로 학습                  │
│     ┌────────────────────────────────────────┐        │
│     │ 분류 (Classification)                  │        │
│     │ - 스팸 vs 정상 메일                    │        │
│     │ - 고양이 vs 강아지                     │        │
│     │                                        │        │
│     │ 회귀 (Regression)                      │        │
│     │ - 집값 예측                            │        │
│     │ - 주가 예측                            │        │
│     └────────────────────────────────────────┘        │
│                                                        │
│  2. 비지도 학습 (Unsupervised Learning)                │
│     - 정답 없이 데이터의 구조 학습                     │
│     ┌────────────────────────────────────────┐        │
│     │ 클러스터링 (Clustering)                │        │
│     │ - 고객 세분화                          │        │
│     │                                        │        │
│     │ 차원 축소 (Dimensionality Reduction)   │        │
│     │ - PCA, t-SNE                          │        │
│     └────────────────────────────────────────┘        │
│                                                        │
│  3. 강화 학습 (Reinforcement Learning)                 │
│     - 행동과 보상을 통해 학습                          │
│     ┌────────────────────────────────────────┐        │
│     │ 에이전트가 환경과 상호작용              │        │
│     │ 행동 → 보상/벌점 → 정책 개선            │        │
│     │ 예: 게임, 로봇 제어                     │        │
│     └────────────────────────────────────────┘        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 주요 알고리즘

```
┌────────────────────────────────────────────────────────┐
│                  머신러닝 알고리즘                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  지도 학습:                                            │
│  - 선형 회귀 (Linear Regression)                      │
│  - 로지스틱 회귀 (Logistic Regression)                │
│  - 결정 트리 (Decision Tree)                          │
│  - 랜덤 포레스트 (Random Forest)                      │
│  - SVM (Support Vector Machine)                       │
│  - KNN (K-Nearest Neighbors)                          │
│  - 신경망 (Neural Networks)                           │
│                                                        │
│  비지도 학습:                                          │
│  - K-Means 클러스터링                                 │
│  - 계층적 클러스터링                                  │
│  - DBSCAN                                             │
│  - PCA (주성분 분석)                                  │
│  - 오토인코더                                         │
│                                                        │
│  앙상블:                                               │
│  - 배깅 (Bagging)                                     │
│  - 부스팅 (Boosting): XGBoost, LightGBM              │
│  - 스태킹 (Stacking)                                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 코드 예시

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import random
import math

class ProblemType(Enum):
    CLASSIFICATION = "분류"
    REGRESSION = "회귀"
    CLUSTERING = "클러스터링"

@dataclass
class DataPoint:
    """데이터 포인트"""
    features: List[float]
    label: Optional[float] = None

class KNearestNeighbors:
    """K-최근접 이웃 알고리즘"""

    def __init__(self, k: int = 3):
        self.k = k
        self.train_data: List[DataPoint] = []

    def fit(self, data: List[DataPoint]):
        """학습 데이터 저장"""
        self.train_data = data

    def predict(self, point: DataPoint) -> float:
        """예측"""
        # 거리 계산
        distances = []
        for train_point in self.train_data:
            dist = self._euclidean_distance(point.features, train_point.features)
            distances.append((dist, train_point.label))

        # K개 선택
        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:self.k]

        # 다수결 투표 (분류)
        labels = [label for _, label in k_nearest]
        return max(set(labels), key=labels.count)

    def _euclidean_distance(self, a: List[float], b: List[float]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

class LinearRegression:
    """선형 회귀"""

    def __init__(self, learning_rate: float = 0.01, epochs: int = 1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights: List[float] = []
        self.bias: float = 0.0

    def fit(self, X: List[List[float]], y: List[float]):
        """학습 (경사 하강법)"""
        n_samples = len(X)
        n_features = len(X[0]) if X else 0

        # 가중치 초기화
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for epoch in range(self.epochs):
            # 예측
            y_pred = [self._predict_single(x) for x in X]

            # 그라디언트 계산
            dw = [0.0] * n_features
            db = 0.0

            for i in range(n_samples):
                error = y_pred[i] - y[i]
                for j in range(n_features):
                    dw[j] += error * X[i][j]
                db += error

            # 가중치 업데이트
            for j in range(n_features):
                self.weights[j] -= self.lr * dw[j] / n_samples
            self.bias -= self.lr * db / n_samples

    def predict(self, X: List[List[float]]) -> List[float]:
        """예측"""
        return [self._predict_single(x) for x in X]

    def _predict_single(self, x: List[float]) -> float:
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

class KMeans:
    """K-Means 클러스터링"""

    def __init__(self, k: int = 3, max_iters: int = 100):
        self.k = k
        self.max_iters = max_iters
        self.centroids: List[List[float]] = []

    def fit(self, X: List[List[float]]) -> List[int]:
        """클러스터링"""
        n_samples = len(X)

        # 초기 중심점 선택
        self.centroids = random.sample(X, self.k)

        labels = [0] * n_samples

        for _ in range(self.max_iters):
            # 할당 단계
            new_labels = []
            for x in X:
                distances = [self._euclidean_distance(x, c) for c in self.centroids]
                new_labels.append(distances.index(min(distances)))

            # 수렴 확인
            if new_labels == labels:
                break
            labels = new_labels

            # 업데이트 단계
            for i in range(self.k):
                cluster_points = [X[j] for j in range(n_samples) if labels[j] == i]
                if cluster_points:
                    self.centroids[i] = [
                        sum(p[d] for p in cluster_points) / len(cluster_points)
                        for d in range(len(X[0]))
                    ]

        return labels

    def _euclidean_distance(self, a: List[float], b: List[float]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# 사용 예시
print("=== 머신러닝 알고리즘 시뮬레이션 ===\n")

# KNN 분류
print("--- KNN 분류 ---")
train_data = [
    DataPoint([1, 1], 0),
    DataPoint([1, 2], 0),
    DataPoint([2, 2], 0),
    DataPoint([5, 5], 1),
    DataPoint([6, 5], 1),
    DataPoint([6, 6], 1),
]

knn = KNearestNeighbors(k=3)
knn.fit(train_data)

test_point = DataPoint([3, 3])
prediction = knn.predict(test_point)
print(f"테스트 포인트 {test_point.features} → 클래스 {prediction}")

# 선형 회귀
print("\n--- 선형 회귀 ---")
X = [[1], [2], [3], [4], [5]]
y = [2, 4, 5, 4, 5]

lr = LinearRegression(learning_rate=0.01, epochs=1000)
lr.fit(X, y)

predictions = lr.predict([[6], [7]])
print(f"y = {lr.weights[0]:.2f}x + {lr.bias:.2f}")
print(f"6 → {predictions[0]:.2f}, 7 → {predictions[1]:.2f}")

# K-Means 클러스터링
print("\n--- K-Means 클러스터링 ---")
X_cluster = [[1, 1], [1, 2], [2, 1], [5, 5], [6, 5], [5, 6]]

kmeans = KMeans(k=2)
labels = kmeans.fit(X_cluster)

for i, (point, label) in enumerate(zip(X_cluster, labels)):
    print(f"포인트 {point} → 클러스터 {label}")
print(f"중심점: {kmeans.centroids}")
```

## 5. 머신러닝 파이프라인

```
┌──────────────────────────────────────────────────────┐
│              머신러닝 파이프라인                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. 데이터 수집                                      │
│     - API, DB, 파일, 크롤링                          │
│                                                      │
│  2. 데이터 전처리                                    │
│     - 결측치 처리                                    │
│     - 이상치 제거                                    │
│     - 정규화/표준화                                  │
│     - 인코딩                                         │
│                                                      │
│  3. 특성 공학 (Feature Engineering)                  │
│     - 특성 선택                                      │
│     - 특성 추출                                      │
│     - 차원 축소                                      │
│                                                      │
│  4. 모델 학습                                        │
│     - 알고리즘 선택                                  │
│     - 하이퍼파라미터 튜닝                            │
│     - 교차 검증                                      │
│                                                      │
│  5. 모델 평가                                        │
│     - 정확도, 정밀도, 재현율, F1                     │
│     - RMSE, MAE (회귀)                               │
│                                                      │
│  6. 모델 배포                                        │
│     - API 서빙                                       │
│     - 모델 모니터링                                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 6. 평가 지표

```
분류:
┌────────────────────────────────────────┐
│          실제값                        │
│        ┌───────┬───────┐              │
│        │  양성 │  음성 │              │
├────┬───┼───────┼───────┤              │
│예측│양성│  TP   │  FP   │              │
│값  │음성│  FN   │  TN   │              │
└────┴───┴───────┴───────┘              │

정확도(Accuracy) = (TP + TN) / 전체
정밀도(Precision) = TP / (TP + FP)
재현율(Recall) = TP / (TP + FN)
F1-Score = 2 * (정밀도 * 재현율) / (정밀도 + 재현율)

회귀:
MSE (Mean Squared Error)
RMSE (Root MSE)
MAE (Mean Absolute Error)
R² Score
```

## 7. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 자동화 | 패턴 자동 학습 |
| 확장성 | 대규모 데이터 |
| 적응성 | 지속적 개선 |
| 복잡성 | 복잡한 패턴 인식 |

### 단점
| 단점 | 설명 |
|-----|------|
| 데이터 | 많은 데이터 필요 |
| 해석 | 블랙박스 |
| 편향 | 데이터 편향 |
| 비용 | 컴퓨팅 비용 |

## 8. 실무에선? (기술사적 판단)
- **추천**: 협업 필터링, 딥러닝
- **이상 탐지**: 오토인코더, Isolation Forest
- **자연어**: BERT, GPT
- **이미지**: CNN, ViT
- **MLOps**: MLflow, Kubeflow

## 9. 관련 개념
- 딥러닝
- 데이터 사이언스
- MLOps
- 특성 공학

---

## 어린이를 위한 종합 설명

**머신러닝은 "컴퓨터가 공부해요!"**

### 어떻게 배우나요? 📚
```
선생님이 정답 알려줘요 (지도학습)
  "이건 사과야!"

스스로 찾아요 (비지도학습)
  "이것들이 비슷하네!"

보상받으며 배워요 (강화학습)
  "잘했어! 또 이렇게!"
```

### 무엇을 할 수 있나요? 🤖
```
사진 보고 고양이인지 알아요
이메일이 스팸인지 알아요
날씨를 예측해요
넷플릭스가 영화를 추천해요
```

### 학습 과정 🎓
```
1. 예제를 많이 봐요
2. 패턴을 찾아요
3. 규칙을 만들어요
4. 테스트해요
5. 틀리면 다시 배워요
```

**비밀**: 유튜브가 뭘 좋아하는지 아는 것도 머신러닝이에요! 🎬✨
