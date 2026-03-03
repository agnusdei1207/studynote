+++
title = "앙상블 학습 (Ensemble Learning)"
date = 2026-03-02
[extra]
categories = "pe_exam-ai"
+++

# 앙상블 학습 (Ensemble Learning)

## 핵심 인사이트 (3줄 요약)
> **앙상블 학습(Ensemble Learning)**은 "집단 지성"의 원리를 활용하여 여러 개의 약한 학습기(Weak Learner)를 결합해 하나의 강력한 예측 모델(Strong Learner)을 만드는 기술이다. **배깅(Bagging)**은 분산을 줄이고(랜덤 포레스트), **부스팅(Boosting)**은 편향을 줄이며(XGBoost, LightGBM), **스태킹(Stacking)**은 메타 모델을 학습한다. 정형 데이터 경진대회(Kaggle 등)와 실무에서 부동의 성능 1위 기법이다.

---

### Ⅰ. 개요 (개념 + 등장 배경)

**개념**: 앙상블 학습은 단일 알고리즘에 의존하지 않고 여러 개의 다양한 모델의 예측을 결합하여 성능(정확도)을 향상시키고 과적합을 방지하는 머신러닝 메타 알고리즘이다.

> 비유: "어려운 문제를 풀 때, 혼자 푸는 것보다 전문가 100명이 각자 풀고 다수결 투표를 하는 것이 더 정답에 가깝다 (집단 지성)"

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: 단일 모델의 한계 - 높은 복잡도로 인한 과적합(Variance 문제) 또는 단순한 구조로 인한 과소적합(Bias 문제) 딜레마 (편향-분산 트레이드오프)
2. **기술적 필요성**: 배깅 제안 (Breiman, 1996) - 복원 추출과 평균화로 모델의 분산 감소 증명; 에이다부스트 (Freund & Schapire, 1997) - 약한 학습기를 순차 결합해 강한 학습기로 변환
3. **시장/산업 요구**: GBM 기반의 XGBoost(2014) / LightGBM 등장으로 정형(Tabular) 데이터 분야를 석권, Kaggle 대회 상위 랭커 솔루션의 90% 이상이 앙상블 기법 활용

**핵심 목적**: 단일 모델의 약점을 보완하여 예측 성능 향상, 과적합 방지, 일반화 능력 강화.

---

### Ⅱ. 구성 요소 및 핵심 원리

**앙상블 학습 3대 기법** (필수: 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **배깅 (Bagging)** | 분산 감소, 과적합 방지 | 병렬 학습, 독립적 모델 | 민주주의 다수결 |
| **부스팅 (Boosting)** | 편향 감소, 정확도 향상 | 순차 학습, 오차 보정 | 오답 노트 집중 훈련 |
| **스태킹 (Stacking)** | 메타 모델로 최적 결합 | 다양한 알고리즘 결합 | 전문가 위원회 |
| **보팅 (Voting)** | 하드/소프트 보팅 | 단순 결합 방식 | 투표 |
| **베깅 (Pasting)** | 비복원 추출 배깅 | 데이터 다양성 증가 | 다른 문제 풀기 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Ensemble Learning Techniques                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Bagging (Bootstrap Aggregating)                                     │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │   Original    Bootstrap 1    Bootstrap 2    Bootstrap 3       │     │
│  │    Data     ──→ [A,B,C]  ──→ [A,C,D]  ──→ [B,C,D]            │     │
│  │                    ↓              ↓              ↓              │     │
│  │               Model 1        Model 2        Model 3            │     │
│  │                    ↓              ↓              ↓              │     │
│  │               Pred 1         Pred 2         Pred 3             │     │
│  │                    └──────────────┬──────────────┘              │     │
│  │                                   ↓                              │     │
│  │                      Average / Majority Vote                     │     │
│  │                              ↓                                   │     │
│  │                         Final Prediction                         │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  2. Boosting                                                            │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │   Data ──→ [Model 1] ──→ Errors ──→ [Model 2] ──→ Errors      │     │
│  │               ↑                    ↑                           │     │
│  │               │    Weight Update   │                           │     │
│  │               └────────────────────┘                           │     │
│  │                          ↓                                      │     │
│  │                   [Model 3] ──→ ... ──→ Final Model            │     │
│  │                                                          │      │     │
│  │   Key: 이전 모델이 틀린 샘플에 가중치 ↑ (순차적 오차 보정)     │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  3. Stacking                                                            │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │   Data ──→ ┌──────────┬──────────┬──────────┐                 │     │
│  │            │ Model 1  │ Model 2  │ Model 3  │                 │     │
│  │            │ (SVM)    │ (RF)     │ (XGB)    │                 │     │
│  │            └────┬─────┴────┬─────┴────┬─────┘                 │     │
│  │                 ↓          ↓          ↓                        │     │
│  │              Pred 1     Pred 2     Pred 3                      │     │
│  │                 └──────────┬──────────┘                        │     │
│  │                            ↓                                   │     │
│  │                    Meta-Learner (Logistic)                     │     │
│  │                            ↓                                   │     │
│  │                    Final Prediction                            │     │
│  └───────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 데이터 분할 → ② 개별 모델 학습 → ③ 예측 생성 → ④ 예측 결합 → ⑤ 최종 출력
```

- **배깅 (Bagging)**:
  - 1단계: 원본 데이터에서 복원 추출로 K개의 부트스트랩 샘플 생성
  - 2단계: 각 샘플로 독립적인 모델 학습 (병렬 가능)
  - 3단계: 모든 모델의 예측을 평균(회귀) 또는 다수결(분류)로 결합
  - 핵심: 분산(Variance) 감소로 과적합 방지

- **부스팅 (Boosting)**:
  - 1단계: 첫 모델 학습, 모든 샘플 동일 가중치
  - 2단계: 오답 샘플의 가중치 증가
  - 3단계: 가중치 기반으로 다음 모델 학습 (순차적)
  - 4단계: 반복하며 모든 모델의 가중 합으로 최종 예측
  - 핵심: 편향(Bias) 감소로 정확도 향상

- **스태킹 (Stacking)**:
  - 1단계: 서로 다른 알고리즘으로 K개의 기본 모델 학습
  - 2단계: 각 모델의 예측값을 새로운 특성으로 변환
  - 3단계: 메타 모델(Meta-Learner)이 기본 모델 예측을 입력으로 학습
  - 4단계: 메타 모델의 예측이 최종 출력

**핵심 알고리즘/공식** (해당 시 필수):

**Random Forest (배깅 기반)**:
```
각 트리가 m개의 특성을 무작위 선택 (√p 또는 log2(p))
최종 예측: ŷ = (1/K) × Σ ŷ_k  (회귀)
           ŷ = mode(ŷ_1, ŷ_2, ..., ŷ_K)  (분류)

Out-of-Bag (OOB) Error:
부트스트랩에 포함되지 않은 샘플로 검증
→ 별도 검증셋 없이 성능 추정 가능
```

**Gradient Boosting (부스팅 기반)**:
```
F_0(x) = argmin_γ Σ L(y_i, γ)  # 초기 예측

For m = 1 to M:
  r_im = -∂L(y_i, F_{m-1}(x_i)) / ∂F_{m-1}(x_i)  # 잔차(Residual)

  h_m(x) = argmin_h Σ (r_im - h(x_i))²  # 잔차 예측 트리

  γ_m = argmin_γ Σ L(y_i, F_{m-1}(x_i) + γ×h_m(x_i))  # 학습률

  F_m(x) = F_{m-1}(x) + η × γ_m × h_m(x)  # 업데이트

η: 학습률 (Learning Rate, 0.01~0.3)
M: 트리 개수 (n_estimators)
```

**XGBoost 목적 함수**:
```
Obj = Σ L(y_i, ŷ_i) + Σ Ω(f_k)

Ω(f) = γT + (1/2)λ||w||²

T: 터미널 노드 수
w: 리프 가중치
γ: 복잡도 페널티
λ: L2 정규화

→ 정규화 항으로 과적합 방지
```

**코드 예시** (필수: Python):

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    VotingClassifier,
    StackingClassifier,
    BaggingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import lightgbm as lgb

# 1. Bagging: Random Forest
def train_random_forest(X_train, y_train, X_test, y_test):
    """랜덤 포레스트 학습"""
    rf = RandomForestClassifier(
        n_estimators=100,      # 트리 개수
        max_depth=10,         # 최대 깊이
        min_samples_split=5,  # 분할 최소 샘플 수
        min_samples_leaf=2,   # 리프 최소 샘플 수
        max_features='sqrt',  # 특성 선택 방식
        bootstrap=True,       # 부트스트랩 사용
        oob_score=True,       # OOB 점수 계산
        n_jobs=-1,            # 병렬 처리
        random_state=42
    )

    rf.fit(X_train, y_train)

    # OOB 점수 (별도 검증셋 없이 성능 추정)
    print(f"OOB Score: {rf.oob_score_:.4f}")

    # 특성 중요도
    feature_importance = pd.DataFrame({
        'feature': range(X_train.shape[1]),
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nTop 5 Features:")
    print(feature_importance.head())

    # 평가
    y_pred = rf.predict(X_test)
    print(f"\nTest Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    return rf


# 2. Boosting: XGBoost
def train_xgboost(X_train, y_train, X_test, y_test):
    """XGBoost 학습"""
    # DMatrix 변환 (최적화된 데이터 구조)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 6,
        'eta': 0.1,              # 학습률
        'subsample': 0.8,        # 행 샘플링
        'colsample_bytree': 0.8, # 열 샘플링
        'lambda': 1,             # L2 정규화
        'alpha': 0,              # L1 정규화
        'seed': 42
    }

    # 학습
    bst = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=[(dtest, 'test')],
        early_stopping_rounds=10,
        verbose_eval=10
    )

    # 예측
    y_pred_prob = bst.predict(dtest)
    y_pred = (y_pred_prob > 0.5).astype(int)
    print(f"XGBoost Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    return bst


# 3. Boosting: LightGBM
def train_lightgbm(X_train, y_train, X_test, y_test):
    """LightGBM 학습 (대용량 데이터에 빠름)"""
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1,
        'seed': 42
    }

    gbm = lgb.train(
        params,
        train_data,
        num_boost_round=100,
        valid_sets=[test_data],
        callbacks=[lgb.early_stopping(10), lgb.log_evaluation(10)]
    )

    y_pred = (gbm.predict(X_test) > 0.5).astype(int)
    print(f"LightGBM Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    return gbm


# 4. Voting Ensemble
def train_voting_ensemble(X_train, y_train, X_test, y_test):
    """보팅 앙상블"""
    # 개별 모델 정의
    estimators = [
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('xgb', xgb.XGBClassifier(n_estimators=100, random_state=42)),
        ('svm', SVC(probability=True, random_state=42))
    ]

    # 소프트 보팅 (확률 평균)
    soft_voting = VotingClassifier(estimators=estimators, voting='soft')
    soft_voting.fit(X_train, y_train)

    # 하드 보팅 (다수결)
    hard_voting = VotingClassifier(estimators=estimators, voting='hard')
    hard_voting.fit(X_train, y_train)

    y_pred_soft = soft_voting.predict(X_test)
    y_pred_hard = hard_voting.predict(X_test)

    print(f"Soft Voting Accuracy: {accuracy_score(y_test, y_pred_soft):.4f}")
    print(f"Hard Voting Accuracy: {accuracy_score(y_test, y_pred_hard):.4f}")

    return soft_voting, hard_voting


# 5. Stacking Ensemble
def train_stacking_ensemble(X_train, y_train, X_test, y_test):
    """스태킹 앙상블"""
    # 기본 모델들 (Level 0)
    base_estimators = [
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('xgb', xgb.XGBClassifier(n_estimators=100, random_state=42)),
        ('dt', DecisionTreeClassifier(max_depth=5, random_state=42))
    ]

    # 메타 모델 (Level 1)
    meta_learner = LogisticRegression()

    # 스태킹 분류기
    stacking = StackingClassifier(
        estimators=base_estimators,
        final_estimator=meta_learner,
        cv=5,  # 교차 검증으로 메타 특성 생성
        stack_method='predict_proba'  # 확률 사용
    )

    stacking.fit(X_train, y_train)
    y_pred = stacking.predict(X_test)

    print(f"Stacking Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    return stacking


# 메인 실행
if __name__ == "__main__":
    from sklearn.datasets import make_classification

    # 데이터 생성
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=15,
        n_redundant=5, n_classes=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("=== Random Forest (Bagging) ===")
    rf_model = train_random_forest(X_train, y_train, X_test, y_test)

    print("\n=== XGBoost (Boosting) ===")
    xgb_model = train_xgboost(X_train, y_train, X_test, y_test)

    print("\n=== LightGBM (Boosting) ===")
    lgb_model = train_lightgbm(X_train, y_train, X_test, y_test)

    print("\n=== Voting Ensemble ===")
    soft_model, hard_model = train_voting_ensemble(X_train, y_train, X_test, y_test)

    print("\n=== Stacking Ensemble ===")
    stacking_model = train_stacking_ensemble(X_train, y_train, X_test, y_test)
```

---

### Ⅲ. 기술 비교 분석 (장단점 + 배깅 vs 부스팅)

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| 단일 모델 대비 성능 우수 (20~30%) | 하이퍼파라미터 튜닝 복잡 |
| 과적합 방지 (특히 배깅) | 학습/추론 시간 증가 |
| 안정적이고 견고한 예측 | 모델 해석력 저하 (블랙박스) |
| 다양한 알고리즘 조합 가능 | 배포 및 유지보수 복잡 |

**배깅 vs 부스팅 비교** (필수: 최소 2개 대안):

| 비교 항목 | 배깅 (Random Forest) | 부스팅 (XGBoost, LightGBM) |
|---------|---------------------|---------------------------|
| 핵심 특성 | 분산(Variance) 감소 | ★ 편향(Bias) 감소 |
| 학습 방식 | 병렬 (독립적 학습) | 순차 (이전 모델 실수 교정) |
| 이상치 민감도 | 덜 민감함 (강건함) | ★ 매우 민감함 |
| 모델 구조 | 깊고 복잡한 트리 | 얕고 간단한 트리 |
| 학습 속도 | 빠름 (병렬 연산) | 상대적 느림 (순차 연산) |
| 튜닝 난이도 | 낮음 (기본값 좋음) | ★ 높음 (하이퍼파라미터 많음) |
| 최고 성능 | 높음 | ★ 매우 높음 (대회 표준) |
| 적합 상황 | 빠르고 강건한 베이스라인 | 최고 성능 필요 시 |

> **★ 선택 기준**:
> - **빠르고 강건한 베이스라인**: Random Forest
> - **최고 성능이 필수 (금융/의료)**: XGBoost / LightGBM
> - **대용량 데이터 (> 1M 행)**: LightGBM (히스토그램 기반으로 빠름)
> - **해석 가능성 중요**: Random Forest + Feature Importance
> - **복잡한 비선형 패턴**: XGBoost + 깊은 트리

**부스팅 알고리즘 세부 비교**:

| 알고리즘 | 특징 | 장점 | 단점 |
|---------|------|------|------|
| AdaBoost | 오답 가중치 증가 | 단순, 이상치 강건 | 노이즈 민감 |
| GBM | 잔차 예측 | 유연한 손실함수 | 느림, 튜닝 어려움 |
| ★ XGBoost | 정규화 + 병렬화 | 빠름, 성능 우수 | 하이퍼파라미터 많음 |
| ★ LightGBM | 히스토그램 기반 | 대용량에서 빠름 | 작은 데이터에서 과적합 |
| CatBoost | 범주형 특화 | 범주형 변수 처리 | 메모리 사용 많음 |

---

### Ⅳ. 실무 적용 방안 (기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 산업 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융 (신용평가)** | XGBoost + 불균형 처리 (SMOTE) | 부도 예측 정확도 85%+ |
| **이커머스 (이탈 예측)** | Random Forest + Feature Importance | 이탈 예측 AUC 0.90+ |
| **제조 (설비 고장)** | LightGBM + 시계열 특성 | 고장 예측 정확도 95%+ |
| **의료 (질병 진단)** | Stacking (RF+XGB+DNN) | 민감도 90%+ 특이도 85%+ |
| **캐글 대회** | 다양한 앙상블 조합 | 상위 1% 랭킹 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: Netflix 추천 시스템** - 다양한 앙상블 모델 결합으로 추천 품질 향상. CTR(클릭률) 10% 이상 개선.
- **사례 2: Kaggle 대회 상위 랭커** - XGBoost + LightGBM + Neural Network 스태킹이 상위 1% 솔루션의 표준. 2015~2020년 정형 데이터 대회 90% 이상이 앙상블 기법 사용.
- **사례 3: 금융권 신용평가** - XGBoost로 신용불량자 예측. 기존 로지스틱 회귀 대비 AUC 0.05~0.10 향상.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: 트리 깊이(Max Depth) 제한으로 과적합 방지, 학습률(Learning Rate)과 트리 개수 균형, 조기 종료(Early Stopping) 필수
2. **운영적**: 스태킹은 배포 복잡도 급증, 모델 버전 관리, A/B 테스트로 성능 검증
3. **보안적**: Feature Importance로 데이터 유출 위험 평가, 모델 설명 가능성(XAI) 요구
4. **경제적**: 앙상블은 추론 비용 증가, 실시간 서비스에서는 단일 모델 고려, GPU 가속 활용

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **과도한 트리 깊이**: 심각한 과적합 발생. 해결: max_depth=3~7 제한
- ❌ **학습률 너무 높음**: 수렴 실패. 해결: eta=0.01~0.1, 트리 개수 늘리기
- ❌ **검증 데이터 누수**: 교차 검증으로 튜닝. 해결: Time Series Split (시계열)
- ❌ **스태킹 과신**: 복잡도만 늘리고 성능 개선 없음. 해결: 단순 모델 먼저 시도

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  Ensemble Learning 핵심 연관 개념 맵                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [Bagging] ←──→ [Ensemble Learning] ←──→ [Boosting]           │
│       ↓                   ↓                    ↓                │
│   [Random Forest]    [Voting/Stacking]    [XGBoost/LightGBM]   │
│       ↓                   ↓                    ↓                │
│   [Variance↓] ←──→ [Bias-Variance Tradeoff] ←──→ [Bias↓]       │
│                           ↓                                     │
│                      [과적합 방지]                               │
│                           ↓                                     │
│                    [Cross-Validation]                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 결정 트리 | 기본 구성 요소 | 앙상블의 베이스 모델 | `[decision_tree](./decision_tree.md)` |
| 정규화 | 과적합 방지 | L1/L2 정규화와 연관 | `[regularization](./regularization.md)` |
| 기계학습 기초 | 상위 개념 | ML의 핵심 기법 | `[machine_learning](./machine_learning.md)` |
| 과적합 | 해결 대상 | 앙상블이 방지하는 현상 | `[overfitting](./overfitting.md)` |
| 교차 검증 | 평가 방법 | 앙상블 성능 검증 | `[cross_validation](./cross_validation.md)` |
| XGBoost | 구체 알고리즘 | 부스팅의 대표 | `[xgboost](./xgboost.md)` |

---

### Ⅴ. 기대 효과 및 결론 (미래 전망 포함)

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 정확도 상승 | 단일 알고리즘 한계 돌파 | 단일 의사결정트리 대비 20~30% 우위 |
| 안정성 확보 | 여러 모델 결합 분산 처리 | 특정 편향 데이터셋 시 예측 변동 최소화 |
| 산업계 표준화 | 정형 데이터 최고 엔진 | 신경망을 꺾고 정형 데이터 분석 프레임워크 1위 |
| Kaggle 성적 | 대회 우승 솔루션 | 상위 1% 랭커의 90%가 앙상블 활용 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: AutoML로 자동 앙상블, Neural Architecture Search와 결합, Knowledge Distillation으로 경량화
2. **시장 트렌드**: 정형 데이터는 XGBoost/LightGBM이 딥러닝보다 우위, TabNet 등 딥러닝 기반 앙상블 연구
3. **후속 기술**: AutoGluon, MLBox 등 AutoML 도구에서 자동 앙상블 지원, LLM + 앙상블 하이브리드

> **결론**: 비정형 데이터(이미지/자연어)에 딥러닝이 있다면, 정형 데이터(엑셀, RDB 구조)에는 앙상블 학습(XGBoost, LightGBM)이 있다. 기술사는 편향/분산의 트레이드오프를 이해하고 실무 문제의 특징(데이터 양, 설명 요구 수준, 배포 복잡도)에 맞춰 랜덤 포레스트와 부스팅 알고리즘을 최적으로 선택 설계해야 한다.

> **※ 참고 표준**: Breiman (1996) "Bagging Predictors", Freund & Schapire (1997) "AdaBoost", Chen & Guestrin (2016) "XGBoost", Ke et al. (2017) "LightGBM"

---

## 어린이를 위한 종합 설명

**앙상블 학습은 "반 친구들 모두가 힘을 합쳐 수수께끼 푸는 방법"이야!**

```
혼자 풀면?
- 똑똑한 철수라도 한쪽으로 치우진 생각(편향)을 할 수 있어 정답을 틀릴 수 있어.

1. 배깅 (Bagging - 민주주의 다수결!)
반 친구 30명이 각자 풀고 투표를 해!
서로의 실수가 다 달라서 다같이 합치면 정답일 확률이 확 올라가
(랜덤 포레스트 선생님).

2. 부스팅 (Boosting - 오답 노트 집중 훈련!)
1번 친구가 먼저 풀고, 틀린 문제만 모아.
2번 친구는 그 틀린 문제만 집중적으로 공부해서 다시 풀어봐.
계속 반복하면 약점이 완벽히 보완돼!
(XGBoost 척척박사).

3. 스탱킹 (Stacking - 전문가 위원회!)
수학 잘하는 친구, 과학 잘하는 친구, 국어 잘하는 친구가 각자 풀어.
그 답들을 모아서 반장이 최종 결정!
→ 더 똑똑한 답이 나와!
```

> 앙상블 학습 = 약한 지식도 모이면 천재 AI가 되는 마법! 혼자보다 함께가 더 강해지는 비결!

---
