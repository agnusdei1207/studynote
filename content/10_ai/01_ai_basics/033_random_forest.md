---
title: "Random Forest"
date: "2026-03-03"
tags:
  - "studynote-ai"
weight: 33
---
> **핵심 인사이트 3줄**
> 1. 랜덤 포레스트(Random Forest)는 배깅(Bagging) + 특성 무작위화(Feature Randomness)를 결합해 다수의 독립적인 의사결정 트리를 앙상블하는 강력한 지도학습 모델이다.
> 2. 각 트리가 부트스트랩 샘플과 무작위 선택된 특성 부분집합으로 학습해 상관관계가 낮은 다양한 트리를 생성하며, 다수결/평균으로 최종 예측한다.
> 3. 특성 중요도(Feature Importance) 계산이 내장되어 해석 가능성이 뛰어나고, 과적합에 강하며, 결측값·이상치에도 견고해 실무에서 가장 널리 사용되는 기반 모델이다.

---

## Ⅰ. 랜덤 포레스트의 구조와 원리

랜덤 포레스트(Random Forest)는 <strong>Leo Breiman(2001)</strong>이 제안한 배깅 기반 앙상블 알고리즘이다.

```
원본 데이터 (N개 샘플)
    v 부트스트랩 샘플링 (복원 추출)
+---------------------------------------------------+
|  Tree 1        Tree 2        Tree 3   ...  Tree k |
|  (m개 특성)    (m개 특성)    (m개 특성)            |
|  예측: A       예측: B       예측: A               |
+---------------------------------------------------+
           v 다수결 (분류) / 평균 (회귀)
        최종 예측: A (가장 많은 표)
```

### 두 가지 무작위성

1. **부트스트랩 샘플링**: 각 트리마다 복원 추출로 N개 샘플 선택 (약 63.2% 고유 샘플)
2. **특성 무작위화**: 각 분기점에서 m개 특성만 고려 (m ≈ √p, p=전체 특성 수)

📢 **섹션 요약 비유**: 랜덤 포레스트는 다수결 전문가 패널이다 — 서로 다른 배경(부트스트랩)과 전공(무작위 특성)을 가진 전문가들이 투표해 편향 없는 결론을 낸다.

---

## Ⅱ. 핵심 하이퍼파라미터

| 파라미터             | 설명                          | 기본값·권장 범위      |
|------------------|------------------------------|---------------------|
| n_estimators     | 트리 개수                     | 100~500 (많을수록 좋음) |
| max_features     | 각 분기점 고려 특성 수         | 분류: √p, 회귀: p/3  |
| max_depth        | 각 트리 최대 깊이              | None (완전 성장)     |
| min_samples_leaf | 리프 최소 샘플 수             | 1~5                  |
| bootstrap        | 부트스트랩 사용 여부           | True                 |
| oob_score        | OOB 오류율로 검증             | True (권장)          |

### OOB (Out-of-Bag) 오류

```
부트스트랩 샘플 ≈ 63.2% -> 나머지 36.8%는 OOB 샘플
각 트리에서 OOB 샘플로 검증 -> 교차 검증 대체 가능
```

📢 **섹션 요약 비유**: OOB는 시험에 안 나온 문제로 실력을 테스트하는 것이다 — 공부(훈련)에 안 쓴 예제로 채점해 진짜 실력을 측정한다.

---

## Ⅲ. 특성 중요도 (Feature Importance)

### 불순도 기반 중요도 (MDI)

```python
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 특성 중요도 시각화
importance = rf.feature_importances_
feature_names = X_train.columns
```

### 순열 중요도 (Permutation Importance)

```
1. 기본 모델 성능 측정
2. 특성 j를 무작위 섞음 (순열)
3. 성능 저하 측정 -> 큰 저하 = 중요한 특성
장점: 편향 없음, MDI보다 신뢰도 높음
```

📢 **섹션 요약 비유**: 특성 중요도는 팀에서 선수 한 명을 빼봤을 때 얼마나 성적이 떨어지는지로 그 선수의 가치를 측정하는 것이다.

---

## Ⅳ. 코드 구현 (Python)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(
    n_estimators=200,
    max_features='sqrt',  # 분류용 √p
    max_depth=None,
    oob_score=True,
    random_state=42,
    n_jobs=-1  # 멀티코어 병렬
)
rf.fit(X_train, y_train)

print(f"OOB Score: {rf.oob_score_:.3f}")
print(classification_report(y_test, rf.predict(X_test)))
print("Top 5 features:")
idx = rf.feature_importances_.argsort()[::-1][:5]
for i in idx:
    print(f"  {load_breast_cancer().feature_names[i]}: "
          f"{rf.feature_importances_[i]:.4f}")
```

📢 **섹션 요약 비유**: n_jobs=-1은 모든 CPU 코어를 동원하는 것이다 — 100그루의 나무를 혼자 심는 대신(n_jobs=1) 모든 인부를 동시에 투입(n_jobs=-1)한다.

---

## Ⅴ. 랜덤 포레스트 vs 그래디언트 부스팅

| 특성          | 랜덤 포레스트        | XGBoost / LightGBM     |
|-------------|---------------------|------------------------|
| 학습 방식    | 병렬 (독립 트리)    | 순차 (이전 오류 보완)    |
| 과적합 저항  | 강함                 | 중간 (하이퍼파라미터 민감) |
| 속도         | 빠름                 | 느림 (많은 트리 반복)    |
| 성능 (일반)  | 좋음                 | 더 좋음 (튜닝 시)        |
| 해석 가능성  | 높음 (OOB, MDI)    | 중간                     |
| 결측값 처리  | 내장 없음            | 내장 처리 (XGBoost)     |
| 적합 상황    | 빠른 베이스라인      | Kaggle 경진대회, 세밀 튜닝|

📢 **섹션 요약 비유**: RF vs XGBoost는 민주주의 vs 멘토링 학습이다 — RF는 각자 독립 투표, XGBoost는 이전 실수를 선생님이 집중 보완한다.

---

## 📌 관련 개념 맵

```
랜덤 포레스트 (Random Forest)
+-- 기반 알고리즘
|   +-- 배깅 (Bagging)
|   +-- 부트스트랩 샘플링
|   +-- 의사결정 트리 (Base Learner)
+-- 핵심 기능
|   +-- OOB 오류율 (교차 검증 대체)
|   +-- 특성 중요도 (MDI / 순열)
+-- 앙상블 비교
|   +-- 배깅 계열: RF, Extra Trees
|   +-- 부스팅 계열: XGBoost, LightGBM, CatBoost
+-- 실용 장점
    +-- 과적합 저항
    +-- 결측값·이상치 견고성
    +-- 특성 스케일링 불필요
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              랜덤 포레스트 발전 흐름                             |
+--------------+--------------------+-----------------------------+
| 1994년       | 배깅(Bagging) 제안  | Breiman, 앙상블 기초         |
| 1995년       | 랜덤 특성 아이디어  | Ho, 무작위 특성 부분집합     |
| 2001년       | RF 논문 발표        | Breiman, 완성된 RF 알고리즘   |
| 2010년대     | scikit-learn 보급   | Python ML 표준 라이브러리     |
| 2014년       | XGBoost 등장        | RF 성능 능가, Kaggle 지배     |
| 2020년대     | AutoML·설명 AI     | SHAP + RF, 자동화 ML 파이프라인|
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
결정 트리 -> 배깅 -> 랜덤 포레스트 -> XGBoost/LightGBM
    v         v           v                v
단일 트리  부트스트랩  OOB 검증          부스팅 앙상블
    v
특성 중요도 -> SHAP 설명 -> XAI (설명 가능한 AI)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 랜덤 포레스트는 100명 전문가 다수결이다 — 각자 다른 공부를 하고(무작위 특성) 다른 문제를 풀어(부트스트랩) 가장 많이 나온 답이 정답이 된다.
2. OOB 점수는 예습 안 한 문제로 시험 보기다 — 공부 안 한 문제도 잘 맞히면 진짜 잘 이해한 것이다.
3. 특성 중요도는 선수별 기여도다 — 한 선수를 빼봤을 때 팀 성적이 많이 떨어지면 그 선수가 핵심 선수이다.
