---
title: "Feature Engineering Auto Feature Generation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 749
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 자동 피처 생성(Automated Feature Generation, AFG)은 원천 변수(Raw Variables)에 대해 **다항식 확장(Polynomial Expansion), 교차항(Cross Features), 시계열 집계(Windowed Aggregations), 비선형 변환(Non-linear Transformations), 임베딩 기반 합성(Embedding-based Synthesis)**을 탐색-생성-평가 루프(Search-Generate-Evaluate Loop)로 자동화하여 Featuretools·tsfresh·OneBM·Cognito·AutoFeat·LFE·OpenFE 같은 엔진이 후보 피처 공간(H_candidate)을 체계적으로 조합·선별하는 메커니리즘이다.
> 2. **가치**: 캐글(Kaggle)·KDD Cup 등 실무 데이터에서 수동 피처 엔지니어링 대비 모델 성능(AUC, RMSE, LogLoss)을 **5~25% 개선**하고, 데이터 사이언티스트의 반복 작업 시간을 **70~90% 단축**한다. 탐색 공간이 1,000만 차원 이상이 될 때 L1·mRMR·SHAP-importance 기반 피처 선택(Feature Selection) 파이프라인과 결합하여 차원의 저주(Curse of Dimensionality)를 제어한다.
> 3. **판단 포인트**: **탐색 폭(Beam Width) vs. 계산 복잡도(O(|F|^d · n))**, **해석 가능성(Interpretability) vs. 표현력(Expressiveness)**, **데이터 누수(Data Leakage) 방지 (시계열 Out-of-Time Split, Group K-Fold)**의 트레이드오프, 그리고 **자동 생성 피처의 도메인 검수(Domain Validation) 및 거버넌스(Auditability)**가 핵심 결정 요인이다.

---

## Ⅰ. 개요 및 필요성

자동 피처 생성(AFG)은 머신러닝 파이프라인에서 가장 노동 집약적인 단계인 수동 피처 엔지니어링(Manual Feature Engineering)을 자동화하는 기술이다. 전통적 ML 워크플로우에서 데이터 정제·라벨링 다음으로 큰 병목이 피처 설계이며, Andrew Ng 교수의 "Data-centric AI" 관점에서도 모델 자체보다 양질의 피처가 일반화 성능을 좌우한다. 그러나 10~1,000개의 원시 컬럼이 존재할 때 이항·삼항 교차(Binary/Ternary Cross)만으로 후보 피처가 C(|F|,2) ≈ 수십만~수억 차원에 달해 사람이 전수 탐색하는 것은 불가능하다.

기존 패러다임(Knowledge-Driven Feature Engineering)은 도메인 전문가의 휴리스틱, 통계 검정, 트리 기반 중요도(Tree-based Importance) 활용에 의존했다. 이는 **①주관성**, **②재현성 결여**, **③확장성 한계**, **④시계열·멀티모달 데이터 대응 곤란** 문제를 안고 있다. 반면 AFG는 **연산자 그래프(Operator Graph) 탐색**, **유전 프로그래밍(Genetic Programming, GP)**, **강화학습(RL) 기반 피처 합성**, **메타러닝(Meta-Learning) 기반 warm-start**, **LLM 기반 의미론적 피처 제안**으로 데이터 자체에서 통계를 추출·결합·평가하는 **데이터 중심(Data-Centric) 접근**을 취한다.

특히 2020년 이후 AutoML 프레임워크(Auto-sklearn, H2O, FLAML, AutoGluon, PyCaret)가 AFG를 핵심 모듈로 내장하면서, KDD Cup 2018(KKBox Churn), IEEE-CIS Fraud Detection, M5 Forecasting(Walmart) 등 대형 경연에서 AFG 파이프라인이 우승 솔루션의 공통 인프라로 자리 잡았다.

```text
[ 전통 수동 피처 엔지니어링 vs. 자동 피처 생성 AFG ]

[전통 방식]                                                       [AFG 방식]
  Raw Data --► 도메인 지식 --► 휴리스틱 변환 --► 수동 후보군    Raw Data --► 연산자 라이브러리
              (도메인 전문가)     (log, ratio)       (10~50개)                     |
                  |                                              v
                  v                                       +--------------+
           모델 학습 (XGB/LGB)                             | 탐색 엔진     |
                  |                                        | - DFS(깊이탐색)|
                  v                                        | - GP(유전)     |
            성능 평가 (5-fold CV)                          | - RL/Agent    |
                  |                                        | - LLM-제안    |
                  v                                        +------+-------+
            수동 반복 (Trial-and-Error)                            v
                                                            후보 피처 풀(H_candidate)
                                                            = Σ 합성 피처 (Cross, Agg…)
                                                                    |
                                                                    v
                                                            +------------------+
                                                            | 피처 선택기        |
                                                            | - L1 (Lasso)      |
                                                            | - mRMR            |
                                                            | - SHAP-importance |
                                                            | - Mutual Info.    |
                                                            +--------+---------+
                                                                     v
                                                            정제된 피처 셋 (Top-K)
                                                                     |
                                                                     v
                                                            모델 학습 + CV 평가
                                                                     |
                                                                     v
                                                          메타러너(메타러닝)/Agent
                                                          -> 다음 라운드 제안
                                                                     |
                                                                     v
                                                          조기 종료/수렴/최적해 반환
```

**AFG의 동학(Dynamics)**
- **탐색 공간(Search Space)**: 1차 단항(Unary) {log, sqrt, +, ×, ÷, x², tanh} + 2차 교차(Binary) {+, −, ×, ÷} + 집계(Aggregation) {mean, std, skew, kurt, max-min, trend, autocorr}
- **탐색 전략(Search Strategy)**: 폭우선(BFS, Featuretools DFS), 유전 알고리즘(Crossover/Mutation), 베이지안 옵티마이저, 강화학습 정책(RL Agent)
- **평가(Evaluation)**: 단변량 F-test -> LightGBM Proxy Model -> 전체 모델 CV(AUC/RMSE) 의 3단계 점진적 검증
- **선택(Selection)**: 안정성(Stability Selection, 100 subsamples) + 중요도 + 다중공선성(VIF<10) 제거

- **📢 섹션 요약 비유**: 기존 방식은 셰프가 직접 재료를 손질해 요리하는 '수제 요리'라면, AFG는 재료의 모든 조합을 자동으로 시험하여 최적의 레시피를 찾아내는 'AI 미슐랭 로봇'과 같다. 단, 재료(데이터) 자체가 신선해야 맛있는 요리(모델)가 나온다(Garbage In, Garbage Out).

---

## Ⅱ. 아키텍처 및 핵심 원리

AFG 시스템은 **①연산자(Operator) 레지스트리**, **②탐색 컨트롤러(Search Controller)**, **③평가·선택 모듈(Evaluator/Selector)**, **④메타러닝/조기 종료 관리자(Meta-Controller)**의 4계층 아키텍처로 구성된다. Featuretools의 Deep Feature Synthesis(DFS)를 기준으로 분해하면 다음과 같다.

```text
                       [ AFG 4-Layer 아키텍처 ]

  +---------------------------------------------------------------------+
  |  ① 연산자 레지스트리 (Operator Registry)                             |
  |  +------------+------------+--------------+----------------------+  |
  |  | 단항(Unary)| 이항(Binary)| 집계(Agg.)    | 시계열(Windowed)      |  |
  |  | log,sqrt   | +,−,×,÷    | mean,std,median| rolling_mean, lag    |  |
  |  | x²,tanh    | concat     | mode,cumsum   | exp_decay, autocorr  |  |
  |  | bin        | diff       | skew,kurt     | trend, seasonal_diff |  |
  |  +------------+------------+--------------+----------------------+  |
  +-------------------------------+-------------------------------------+
                                  v
  +---------------------------------------------------------------------+
  |  ② 탐색 컨트롤러 (Search Controller)                                |
  |  +--------------+  +--------------+  +------------------------+    |
  |  | DFS / Beam   |  | Genetic Prog.|  | RL/Agent (LFE, AAAR)   |    |
  |  | (Featuretools|  | (AutoFeat)   |  | (OpenFE, ExploreKit)   |    |
  |  |  Tsfresh)    |  |              |  |                        |    |
  |  +--------------+  +--------------+  +------------------------+    |
  |   깊이 d ∈ [1,3]      crossover/mut.    policy π(·|state)         |
  |   폭 w (top-k)        fitness=F1/AUC    reward=ΔAUC − λ·|F|      |
  +-------------------------------+-------------------------------------+
                                  v
  +---------------------------------------------------------------------+
  |  ③ 평가·선택 모듈 (Evaluator + Selector)                            |
  |  (a) 단변량 점수 : F-stats / Mutual Info / Pearson / χ²             |
  |  (b) Proxy Model : LightGBM(50 rounds) -> gain/cover                 |
  |  (c) 최종 점수  : K-Fold CV AUC / LogLoss / RMSE                    |
  |  ----------------------------------------------------------------   |
  |  • 안정성 선택 (Bootstrap 100회 등장 피처만 채택)                    |
  |  • VIF < 10, 상관 |ρ| < 0.95 로 가지치기                            |
  |  • SHAP/Tree importance Top-K                                       |
  +-------------------------------+-------------------------------------+
                                  v
  +---------------------------------------------------------------------+
  |  ④ 메타 컨트롤러 (Meta-Controller)                                  |
  |  • 시간 예산(Time Budget)·메모리 예산(Memory Budget)                 |
  |  • 메타러닝 Warm-Start (OpenML Meta-features -> 추천 연산자 셋)       |
  |  • 조기 종료 (성능 plateau 감지: ΔAUC < ε, 5 연속 round)            |
  |  • LLM 기반 의미론적 제안 (변수명 + Docstring -> 후보 합성)           |
  +---------------------------------------------------------------------+
                                  |
                                  v
                    [ 최종 피처 셋 (K=20~200) ] -> Downstream ML
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **연산자 레지스트리 (Operator Library)** | 원천 변수 변환·결합의 원자 단위(Atomic Unit) 정의 | 단항(15종: log, sqrt, bin, normalize), 이항(6종: +,−,×,÷,concat,ratio), 집계(20종: mean, std, median, max, min, skew, kurt, count, n_unique, trend), 윈도우(rolling_mean, rolling_std, exp_decay_mean, lag_k, diff_k, autocorr_lag) |
| **탐색 컨트롤러 (Search Controller)** | 후보 피처 그래프(G=(V,E)) 탐색 | DFS(깊이우선, Featuretools): max_depth∈{2,3}, n_features 제한. GP(유전, AutoFeat): population=200, crossover·mutation·elitism. RL(AAAR/LFE/GRFG): Q-learning, ε-greedy 0.1, reward = ΔAUC − λ·\|F\| (regularizer). 베이지안(MCFS): GP-UCB 획득함수 |
| **평가자 (Evaluator)** | 후보 피처의 예측력·안정성 측정 | 1차: 단변량 Mutual Information / F-regression (P<1e-3). 2차: LightGBM Proxy (50 rounds, early_stopping) -> gain importance. 3차: 5-Fold StratifiedKFold CV (AUC/LogLoss/RMSE). 시계열은 TimeSeriesSplit(Time-based) |
| **선택기 (Selector)** | 차원 축소·다중공선성 제거 | L1-Lasso (α 튜닝), mRMR(Min-Redundancy Max-Relevance, mRMR-MID/MIQ), 안정성 선택(Stability Selection, threshold 0.6), VIF<10, Pearson \|ρ\|<0.95, SHAP-importance 상위 K개 |
| **메타 컨트롤러 (Meta-Controller)** | 자원 관리·warm-start·LLM 제안 | OpenML 1,000+ 데이터셋 메타피처(meta-feature: n, dim, skew, class_entropy) -> 유사도(K-NN) 기반 추천. LLM(Llama-3, GPT-4o): 변수명·dtypes·description 입력 -> 자연어 후보 합성 제안 (e.g., "value_per_unit = price / quantity") |
| **검수 거버넌스 (Governance Layer)** | 자동화 피처의 해석·감사 | 피처 명세서(Feature Card) 자동 생성: 정의, 분포, NULL%, 단변량 AUC, SHAP 평균. 도메인 룰(예: 음수가 될 수 없는 도메인 지식 -> ratio 연산 차단) |

**핵심 수식 및 알고리즘 심화**

1. **Deep Feature Synthesis (DFS) - Featuretools**
   - 원천 테이블 R = {T₁, T₂, ..., T_m}, 관계(foreign key) 그래프 G, 깊이 d
   - 1차 피처: F₁ = {f = op(x) | x ∈ Tᵢ, op ∈ O₁}
   - k차 피처: F_k = {f = op(x, y) | x ∈ F_{k−1} ∪ Tᵢ, y ∈ T_j, op ∈ O₂} ∪ {f = agg(g, window) | g ∈ F_{k−1}, agg ∈ O_agg}
   - |F_k| ≤ n_features 제한, max_depth ≤ 3
   - 시간 절약: entityset + cutoff_time 매개변수로 **시계열 누수 차단**

2. **유전 프로그래밍(Genetic Programming) - AutoFeat**
   - 개체(individual) = 표현식 트리(Expression Tree, sklearn-style)
   - 적합도(Fitness) F(θ) = 0.5·AUC_cv + 0.3·(1−corr_redundancy) + 0.2·(1−sparsity)
   - 선택: Tournament(size=3) / NSGA-II 다목적(AUC^, |F|v)
   - 연산자: Subtree Crossover, Point Mutation, Shrink Mutation, hoist, copy

3. **강화학습 기반 - LFE (Learning Feature Engineering)**
   - State s_t = (현재 피처 셋, 모델 메트릭), Action a_t = (피처 추가/제거/변환), Reward r_t = AUC(s_{t+1}) − AUC(s_t) − λ·|F|
   - Policy π_θ : Deep Q-Network (Dueling DDQN), ε-greedy 0.1->0.01 (decay)
   - Episode = 1,000 step, Replay Buffer 10⁵

4. **선형 탐색 기반 - OpenFE (2023 NeurIPS)**
   - 단일 후보 피처 평가에 **GBDT 모델 가속화** (1회 학습으로 모든 1차·2차 교차 점수 추정)
   - 피처별 1차 평가 + 다변량 MB( Monte Carlo) 후방 선택
   - L-BFGS로 평가 모델 가중치 보정

5. **시계열 특화 - tsfresh / tsfel / Catch22**
   - 794개 통계 피처(유한집합) + Hugging Face `setfit` 기반 의미론적 라벨링
   - EfficientFCParameters / MinimalFCParameters로 차원 축소
   - FDR(Fisher-Discriminant-Ratio) Benjamini-Yekutieli 보정으로 다중비교 통제

6. **임베딩 기반 합성 - AutoEmbed / DeepFM / TabNet**
   - 범주형 임베딩 E ∈ ℝ^{k}의 외적(e₁ ⊗ e₂) = e₁ e₂ᵀ로 2차 교차 자동 생성
   - attention 가중치로 유효 교차만 강조

**핵심 하이퍼파라미터 및 튜닝 포인트**
- `max_depth` ∈ {2, 3, 4} (깊이^ -> 후보 폭발, 과적합 위험)
- `n_features` ∈ {50, 100, 200} (탐색 한도)
- `correlation_threshold` ∈ {0.9, 0.95}
- `cv_folds` ∈ {5, 10} (K-Fold, Group, Stratified, Time-series