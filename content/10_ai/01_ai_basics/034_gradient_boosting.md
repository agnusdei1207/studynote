---
title: "Gradient Boosting"
date: "2026-03-04"
tags:
  - "studynote-ai"
weight: 34
---
> **핵심 인사이트 3줄**
> 1. 그래디언트 부스팅(Gradient Boosting)은 약한 학습기(결정 트리)를 순차적으로 앙상블해 이전 모델의 잔차(Residual Error)를 반복적으로 줄이는 부스팅 알고리즘으로, 표 형식 데이터에서 최강의 성능을 보인다.
> 2. XGBoost·LightGBM·CatBoost는 그래디언트 부스팅을 병렬화·최적화한 구현체로, 특히 LightGBM의 Leaf-wise 트리 성장과 히스토그램 근사가 처리 속도를 수십 배 향상시켰다.
> 3. 그래디언트 부스팅의 핵심 하이퍼파라미터는 학습률(learning rate)·트리 깊이·서브샘플링으로, 작은 학습률 + 많은 트리(+ 조기 종료)가 정규화와 성능의 최적 균형을 제공한다.

---

## Ⅰ. 그래디언트 부스팅의 핵심 알고리즘

```
그래디언트 부스팅 순서:

1. 초기 예측: F₀(x) = argmin_γ Σ L(yᵢ, γ)  (평균값 초기화)
2. for t = 1 to T:
   a. 잔차 계산: rᵢ = -[∂L(yᵢ, F(xᵢ)) / ∂F(xᵢ)]
      (손실 함수의 그래디언트)
   b. 잔차에 트리 학습: hₜ(x)
   c. 모델 업데이트: Fₜ(x) = Fₜ₋₁(x) + ν·hₜ(x)
      (ν = 학습률, 0 < ν ≤ 1)
3. 최종: F(x) = F₀ + ν·h₁ + ν·h₂ + ... + ν·hₜ
```

📢 **섹션 요약 비유**: 그래디언트 부스팅은 오답 모음집이다 — 첫 번째 학생이 틀린 문제를 두 번째 학생이 집중 공부하고, 두 번째가 틀린 문제를 세 번째가 집중 공부하는 방식으로 팀 전체가 점점 개선된다.

---

## Ⅱ. XGBoost vs LightGBM vs CatBoost

| 특성           | XGBoost          | LightGBM            | CatBoost             |
|-------------|-----------------|---------------------|----------------------|
| 트리 성장     | Level-wise       | Leaf-wise (더 빠름)  | Oblivious Tree       |
| 속도          | 중간              | 매우 빠름            | 중간                  |
| 범주형 변수   | 인코딩 필요       | 제한적 내장          | 완벽한 내장 처리       |
| 메모리        | 높음              | 낮음 (히스토그램)    | 중간                  |
| GPU 지원     | ✅               | ✅                  | ✅                   |

### LightGBM 핵심 최적화

```
Level-wise (XGBoost):
  레벨 단위로 모든 리프를 균등 분할
  -> 균형 트리, 메모리 예측 가능

Leaf-wise (LightGBM):
  가장 큰 손실 감소 리프 우선 분할
  -> 불균형하지만 더 낮은 오차
  -> 과적합 방지: max_depth 제한 필요
```

📢 **섹션 요약 비유**: Leaf-wise vs Level-wise는 공부 방법 차이다 — 모든 과목을 균등하게(Level-wise) vs 가장 못하는 과목에 집중(Leaf-wise). 집중 공부가 빠르지만 지나치면 편식(과적합)이 된다.

---

## Ⅲ. 하이퍼파라미터 튜닝

| 파라미터             | 역할                | 권장값           |
|--------------------|---------------------|----------------|
| n_estimators        | 트리 개수            | 100~1000       |
| learning_rate (ν)  | 각 트리 기여도       | 0.01~0.3       |
| max_depth           | 트리 최대 깊이       | 3~8            |
| subsample           | 행 샘플링 비율       | 0.7~0.9        |
| colsample_bytree    | 열 샘플링 비율       | 0.7~0.9        |
| min_child_weight    | 리프 최소 샘플 수    | 1~10           |

### 조기 종료 (Early Stopping)

```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    early_stopping_rounds=50  # 50 라운드 개선 없으면 중단
)
model.fit(X_train, y_train,
          eval_set=[(X_val, y_val)],
          verbose=100)
```

📢 **섹션 요약 비유**: 조기 종료는 시험 준비 중 멈추는 것이다 — 50번 더 공부해도 점수가 안 오르면, 이미 충분히 준비됐다고 판단하고 공부를 멈춘다.

---

## Ⅳ. 특성 중요도 (Feature Importance)

```
그래디언트 부스팅 특성 중요도 계산 방식:
  1. Gain (정보 이득): 해당 특성이 분할에서 기여한 정보 이득 합산
  2. Split count: 해당 특성이 사용된 분할 횟수
  3. Permutation: 해당 특성을 섞었을 때 성능 감소량

SHAP (SHapley Additive exPlanations):
  -> 각 샘플의 예측에 특성이 얼마나 기여했는지
  -> 전체 중요도 + 개별 샘플 설명
```

📢 **섹션 요약 비유**: SHAP 값은 팀 기여도 분석이다 — 팀 승리(예측 결과)에 각 선수(특성)가 얼마나 기여했는지 수치로 보여준다.

---

## Ⅴ. 그래디언트 부스팅 실전 응용

| 분야           | 응용                              |
|-------------|----------------------------------|
| Kaggle 경진  | 표 형식 데이터 1위 알고리즘       |
| 신용 평가     | 대출 부도 예측 (LightGBM)        |
| 클릭률 예측   | 광고 CTR 예측 (XGBoost)          |
| 이상 거래 탐지| 카드 사기 탐지                   |
| 의료 진단     | 질병 위험도 예측                  |

```python
# LightGBM 기본 파이프라인
import lightgbm as lgb
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

model = lgb.LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    num_leaves=31
)
model.fit(X_train, y_train,
          eval_set=[(X_val, y_val)],
          callbacks=[lgb.early_stopping(50)])
```

📢 **섹션 요약 비유**: 그래디언트 부스팅은 Kaggle 대회의 비밀 무기다 — 표 형식 데이터(엑셀 같은 데이터)에서는 딥러닝보다도 XGBoost·LightGBM이 자주 우승한다.

---

## 📌 관련 개념 맵

```
그래디언트 부스팅 (Gradient Boosting)
+-- 알고리즘
|   +-- 잔차(Residual) 반복 학습
|   +-- 손실 함수 그래디언트 활용
+-- 구현체
|   +-- XGBoost (Level-wise)
|   +-- LightGBM (Leaf-wise, 히스토그램)
|   +-- CatBoost (범주형 특화)
+-- 주요 기법
|   +-- 조기 종료 (Early Stopping)
|   +-- 서브샘플링 (행/열)
|   +-- SHAP 특성 중요도
+-- 앙상블 비교
    +-- 배깅 (Bagging): 랜덤 포레스트
    +-- 부스팅 (Boosting): AdaBoost, GBM
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              그래디언트 부스팅 발전 흐름                         |
+--------------+--------------------+-----------------------------+
| 1996년       | AdaBoost 발표      | 최초 부스팅 알고리즘          |
| 1999년       | GBM 논문 (Friedman) | 그래디언트 부스팅 이론 정립  |
| 2014년       | XGBoost 오픈소스   | Tianqi Chen, Kaggle 지배 시작|
| 2017년       | LightGBM (MS)      | Leaf-wise, 히스토그램 최적화 |
| 2017년       | CatBoost (Yandex)  | 범주형 변수 자동 처리         |
| 2020년       | SHAP 기반 설명 AI  | XAI + 그래디언트 부스팅 결합  |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
약한 학습기(결정 트리) -> 잔차 계산 -> 그래디언트 부스팅
    v                        v                  v
순차 앙상블             L2 잔차/로그오즈     T개 트리 합산
    v
XGBoost -> LightGBM -> CatBoost -> AutoML 기본 알고리즘
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 그래디언트 부스팅은 오답 교사다 — 첫 번째 선생님이 틀린 문제를 두 번째 선생님이 가르치고, 그것도 틀린 문제를 세 번째 선생님이 가르치는 방식이다.
2. 학습률은 각 선생님의 영향력이다 — 학습률이 작으면(0.01) 각 선생님의 기여가 작아서 더 많은 선생님(트리)이 필요하지만, 최종 결과가 더 안정적이다.
3. LightGBM이 XGBoost보다 빠른 이유는 히스토그램이다 — 모든 값을 정확히 기록(XGBoost) 대신, 범위로 묶어(히스토그램) 계산하면 계산량이 훨씬 줄어든다.
