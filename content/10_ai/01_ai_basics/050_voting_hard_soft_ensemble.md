---
title: "Hard vs Soft Voting Ensemble"
date: "2025-01-01"
tags:
  - "VotingClassifier"
  - "ensemble learning"
  - "hard voting"
  - "scikit-learn"
  - "soft voting"
  - "voting ensemble"
  - "weighted voting"
  - "studynote-ai"
weight: 50
---
> **핵심 인사이트 3줄**
> 1. 하드 보팅(Hard Voting)은 각 분류기의 클래스 예측(다수결)을 집계하고, 소프트 보팅(Soft Voting)은 각 분류기의 확률값을 평균해 더 정확한 결과를 낸다.
> 2. 소프트 보팅은 분류기가 보정된 확률(calibrated probability)을 출력할 때 효과적이며, 하드 보팅보다 일반적으로 성능이 높다.
> 3. 가중 보팅(Weighted Voting)은 성능이 높은 분류기에 더 높은 가중치를 부여해 단순 다수결의 한계를 극복한다.

---

## Ⅰ. 앙상블과 보팅 개요

### 1.1 보팅 앙상블 구조

```
입력 X
  +--> 분류기 1 (예: 로지스틱 회귀)  --> 예측1
  +--> 분류기 2 (예: Decision Tree)  --> 예측2
  +--> 분류기 3 (예: SVM)            --> 예측3
                                          v
                                    보팅 집계 -> 최종 예측
```

### 1.2 보팅의 전제 조건

- 분류기들이 <strong>상호 독립적</strong>이고 오류 패턴이 다를 때 효과적
- 개별 정확도 ≥ 50% 이어야 다수결이 의미 있음

📢 **섹션 요약 비유**: 세 명의 의사에게 진단 받아 2명 이상이 같은 병명을 말하면 그걸 따르는 것 — 독립적인 의견이 핵심.

---

## Ⅱ. 하드 보팅 (Hard Voting)

### 2.1 원리

각 분류기가 클래스 레이블을 예측 -> 가장 많이 나온 클래스 선택 (다수결).

```
예시 (3 클래스: A, B, C):
분류기1: A
분류기2: A
분류기3: B
---------
결과: A (2표 다수결)
```

### 2.2 한계

- 확률 정보 무시: 0.51 A vs 0.99 A를 동등하게 1표 처리
- 신뢰도 낮은 분류기와 높은 분류기를 동일하게 취급

📢 **섹션 요약 비유**: 하드 보팅은 "찍기" 투표 — 자신 없어도 확신에 차 있어도 한 표씩 동등하다.

---

## Ⅲ. 소프트 보팅 (Soft Voting)

### 3.1 원리

각 분류기의 클래스별 확률을 평균 -> 가장 높은 평균 확률 클래스 선택.

```
예시:
분류기1: P(A)=0.7, P(B)=0.3
분류기2: P(A)=0.6, P(B)=0.4
분류기3: P(A)=0.3, P(B)=0.7
-----------------------------
평균:    P(A)=0.533, P(B)=0.467
결과: A
```

### 3.2 소프트 보팅이 유리한 경우

- 분류기들이 보정된 확률을 출력할 때 (calibration 필요)
- 클래스 불균형 상황

```python
from sklearn.ensemble import VotingClassifier
from sklearn.calibration import CalibratedClassifierCV

clf = VotingClassifier(estimators=[...], voting='soft')
```

📢 **섹션 요약 비유**: 소프트 보팅은 "확신도 투표" — "아마 A인 것 같다(60%)"와 "확실히 A다(99%)"를 다르게 반영.

---

## Ⅳ. 가중 보팅 (Weighted Voting)

### 4.1 가중 하드 보팅

```
가중치: clf1=2, clf2=1, clf3=1
clf1->A: 2표, clf2->A: 1표, clf3->B: 1표
결과: A (3표 vs 1표)
```

### 4.2 가중 소프트 보팅

```
P_final(k) = Σ(w_i × P_i(k)) / Σw_i
```

### 4.3 scikit-learn 구현

```python
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

lr = LogisticRegression()
dt = DecisionTreeClassifier()
svc = SVC(probability=True)

vc = VotingClassifier(
    estimators=[('lr', lr), ('dt', dt), ('svc', svc)],
    voting='soft',
    weights=[2, 1, 1]  # LR에 더 높은 가중치
)
vc.fit(X_train, y_train)
```

📢 **섹션 요약 비유**: 가중 보팅은 전문가 위원회 — 경험 많은 전문가(높은 가중치) 의견이 더 반영된다.

---

## Ⅴ. 성능 비교와 활용 전략

### 5.1 보팅 방식 비교

| 방식          | 장점               | 단점                      | 적합한 상황            |
|-------------|------------------|--------------------------|-----------------------|
| 하드 보팅     | 단순, 빠름          | 확률 무시                 | 분류기 확률 불신뢰 시  |
| 소프트 보팅   | 확률 활용, 정확     | calibration 필요          | 확률 출력 분류기 혼합  |
| 가중 보팅     | 성능 차이 반영      | 가중치 튜닝 필요           | 성능 불균형 분류기 조합 |

### 5.2 실무 팁

- SVM은 기본적으로 확률 미지원 -> `probability=True` 설정 또는 `CalibratedClassifierCV` 래핑
- 트리 기반 모델(Decision Tree, RandomForest)은 소프트 보팅에 유리
- 이질적(heterogeneous) 분류기 조합이 동질 분류기보다 효과적

📢 **섹션 요약 비유**: 다양한 배경의 전문가(이질 분류기)가 같은 분야 전문가보다 종종 더 나은 집단 결정을 내린다.

---

## 📌 관련 개념 맵

```
보팅 앙상블
+-- 하드 보팅 (다수결)
+-- 소프트 보팅 (확률 평균)
+-- 가중 보팅 (가중치 부여)
+-- 관련 앙상블
    +-- 배깅 (Bagging) — Bootstrap 샘플링
    +-- 부스팅 (Boosting) — 순차 학습
    +-- 스태킹 (Stacking) — 메타 학습기
```

---

## 📈 관련 키워드 및 발전 흐름도

```
단일 분류기 (1980s)
     |  분산 감소 필요
     v
배깅/부스팅 (1990s) — 동질 앙상블
     |  이질 분류기 결합
     v
보팅 앙상블 (하드/소프트, 2000s)
     |  확률 보정 필요
     v
보정된 소프트 보팅 + 가중치 최적화
     |  딥러닝 분류기 통합
     v
신경망 + 전통 ML 혼합 앙상블 (현재)
```

**핵심 키워드**: 하드 보팅, 소프트 보팅, 가중 보팅, VotingClassifier, 확률 보정, 이질 앙상블

---

## 👶 어린이를 위한 3줄 비유 설명

1. 하드 보팅은 손들기 투표 — 많이 손든 쪽이 이기고, 자신감은 안 따져.
2. 소프트 보팅은 점수 투표 — 각자 "A가 70점, B가 30점" 이라고 점수를 내면 평균이 가장 높은 쪽이 이겨.
3. 가중 보팅은 선생님 의견에 더 많은 점수를 주는 것 — 똑똑한 친구 말을 조금 더 듣는 거야.
