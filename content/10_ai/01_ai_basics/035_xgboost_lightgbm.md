---
title: "XGBoost & LightGBM"
date: "2026-03-03"
tags:
  - "studynote-ai"
weight: 35
---
> **핵심 인사이트**
> 1. XGBoost (Extreme Gradient Boosting)와 LightGBM은 모두 Gradient Boosting 계열의 앙상블 알고리즘으로, 테이블 형식 데이터(정형 데이터)에서 최고 수준의 성능을 보이는 ML 표준 도구다.
> 2. XGBoost는 레벨 단위(Level-wise) 트리 성장으로 안정적이고, LightGBM은 리프 단위(Leaf-wise) 트리 성장으로 더 빠르고 낮은 메모리로 동일 성능을 달성한다.
> 3. Kaggle·산업 데이터 대회에서 XGBoost/LightGBM은 딥러닝보다 정형 데이터에서 우위를 점하며, CatBoost와 함께 "테이블 데이터 3대 부스터"를 형성한다.

---

## I. XGBoost vs LightGBM 핵심 비교

```
GBM (Gradient Boosting Machine) 계열

XGBoost (2016, Chen & Guestrin)
   Level-wise 트리 성장
   정규화 (L1, L2) 내장
   GPU 지원, 분산 학습

LightGBM (2017, Microsoft)
   Leaf-wise 트리 성장
   GOSS (Gradient-based One-Side Sampling)
   EFB (Exclusive Feature Bundling)
   더 빠름, 더 낮은 메모리
```

| 비교 항목      | XGBoost         | LightGBM        |
|--------------|-----------------|-----------------|
| 트리 성장 방식 | Level-wise      | Leaf-wise       |
| 학습 속도     | 빠름             | 매우 빠름        |
| 메모리 사용   | 높음             | 낮음             |
| 과적합 위험   | 낮음             | 높음 (소규모 데이터)|
| 범주형 처리   | 직접 안됨        | 내장 지원        |
| 적합한 데이터 | 중간 크기        | 대용량 (100만+) |

> 📢 **섹션 요약 비유**: XGBoost는 꼼꼼하게 층층이 쌓는 벽돌공, LightGBM은 가장 약한 곳을 집중 공략하는 수리공 — 같은 결과, 다른 전략.

---

## II. XGBoost 핵심 원리

```
목적 함수:
  Obj = Sum(Loss(yi, y_pred_i)) + Sum(Omega(fk))

  Loss: 예측 오류 (회귀: MSE, 분류: LogLoss)
  Omega: 정규화 항 (트리 복잡도 패널티)

트리 분기 기준 (Gain):
  Gain = 0.5 * [GL^2/(HL+lambda) + GR^2/(HR+lambda)
              - (GL+GR)^2/(HL+HR+lambda)] - gamma

  G = 1차 미분(그래디언트), H = 2차 미분(헤시안)
  lambda, gamma: 정규화 하이퍼파라미터
```

### XGBoost 주요 하이퍼파라미터

| 파라미터       | 의미                   | 기본값  |
|--------------|------------------------|--------|
| n_estimators | 트리 개수               | 100    |
| max_depth    | 트리 최대 깊이          | 6      |
| learning_rate| 학습률 (eta)            | 0.3    |
| subsample    | 행 샘플링 비율          | 1.0    |
| colsample    | 열(특성) 샘플링 비율    | 1.0    |
| lambda       | L2 정규화              | 1.0    |

> 📢 **섹션 요약 비유**: 각 선생님(트리)이 이전 선생님의 실수를 집중 가르치는 보충수업 — 수업(learning_rate)이 너무 크면 오히려 혼란스럽다.

---

## III. LightGBM 핵심 기법

```
Leaf-wise 성장 vs Level-wise:

Level-wise (XGBoost):
  레벨 1: [A] [B]
  레벨 2: [A1][A2] [B1][B2]
  모든 리프를 균등 확장

Leaf-wise (LightGBM):
  [Root]
  가장 Loss 감소가 큰 리프만 확장
  -> 비대칭 트리 생성 -> 더 빠른 수렴
```

### LightGBM 최적화 기법

| 기법  | 설명                                      |
|------|-------------------------------------------|
| GOSS | 큰 그래디언트 샘플은 전부 사용, 작은 것은 무작위 샘플링 |
| EFB  | 상호 배타적인 피처를 묶어 피처 수 감소     |
| 히스토그램 | 연속 값을 이산 구간으로 묶어 분기 탐색 가속 |

> 📢 **섹션 요약 비유**: 수업에서 잘 틀리는 학생에게만 집중 — 다 아는 학생을 반복 지도하는 시간을 줄인다.

---

## IV. 실용 코드 예시

```python
import xgboost as xgb
from lightgbm import LGBMClassifier

# XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=500, max_depth=6, learning_rate=0.05,
    subsample=0.8, colsample_bytree=0.8,
    use_label_encoder=False, eval_metric='logloss'
)
xgb_model.fit(X_train, y_train,
    eval_set=[(X_val, y_val)], early_stopping_rounds=50)

# LightGBM
lgbm = LGBMClassifier(
    n_estimators=1000, num_leaves=63, learning_rate=0.05,
    min_child_samples=20, subsample=0.8, colsample_bytree=0.8
)
lgbm.fit(X_train, y_train,
    eval_set=[(X_val, y_val)], callbacks=[lgb.early_stopping(50)])
```

> 📢 **섹션 요약 비유**: Early Stopping은 시험을 더 볼 필요가 없을 때 멈추는 것 — 과한 공부(과적합)를 방지한다.

---

## V. 실무 시나리오 — Kaggle 정형 데이터 경진대회

| 단계          | 전략                                        |
|-------------|---------------------------------------------|
| 피처 엔지니어링 | 결측값 처리, 인코딩, 교차 특성 생성         |
| 모델 선택     | LightGBM (대용량), XGBoost (소-중 규모)     |
| 하이퍼파라미터 | Optuna / Bayesian 최적화                    |
| 앙상블        | XGBoost + LightGBM + CatBoost 스태킹        |
| 검증         | K-Fold CV, OOF (Out-of-Fold) 예측           |

> 📢 **섹션 요약 비유**: Kaggle 금메달의 레시피 — LightGBM으로 속도, XGBoost로 안정성, CatBoost로 범주형 처리, 셋을 합치면 최강.

---

## 📌 관련 개념 맵

```
Gradient Boosting 계열
+-- GBM (Friedman, 2001)
+-- XGBoost (2016)
|   +-- Level-wise 트리
|   +-- 2차 미분 목적함수
|   +-- L1/L2 정규화
+-- LightGBM (2017, Microsoft)
|   +-- Leaf-wise 트리
|   +-- GOSS / EFB
|   +-- 히스토그램 알고리즘
+-- CatBoost (2017, Yandex)
|   +-- 범주형 피처 내장 처리
|   +-- Ordered Boosting
+-- 공통 기법
    +-- Early Stopping
    +-- Feature Importance
    +-- SHAP 해석
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[Bagging 계열 (1990s)]
Random Forest: 병렬 독립 트리
      |
      v
[Boosting 계열]
AdaBoost (1996) -> GBM (2001)
오차를 줄이는 순차 학습
      |
      v
[XGBoost (2016)]
2차 미분 + 정규화로 GBM 고도화
Kaggle 제패 시작
      |
      v
[LightGBM (2017)]
Leaf-wise + GOSS + EFB: 10배 이상 속도 향상
      |
      v
[CatBoost (2017)]
범주형 특성 처리 혁신
      |
      v
[현재: AutoML + SHAP]
Optuna 최적화 + SHAP 피처 중요도
정형 데이터에서 딥러닝보다 강력
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. XGBoost와 LightGBM은 여러 약한 예측기(나무)를 합쳐 강한 예측기를 만드는 팀워크 알고리즘이에요.
2. 각 나무는 이전 나무가 틀린 부분을 집중적으로 고치면서 점점 똑똑해져요.
3. 표 형태의 데이터 분석에서는 딥러닝보다 더 빠르고 정확할 때가 많답니다!
