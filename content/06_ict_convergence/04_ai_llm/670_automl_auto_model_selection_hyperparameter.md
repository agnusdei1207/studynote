---
title: "AutoML Auto Model Selection Hyperparameter"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 670
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AutoML은 CASH(Combined Algorithm Selection and Hyperparameter optimization) 문제를 해결하기 위해 **탐색 공간 설계(Search Space)**, **탐색 전략(Search Strategy: BO/TPE/Hyperband)**, **조기 종료(Early Stopping/Successive Halving)**의 3축으로 모델·하이퍼파라미터·파이프라인을 자동 탐색하는 Meta-learning 기반 MLOps 자동화 패러다임이다.
> 2. **가치**: 숙련 ML 엔지니어 대비 **모델 개발 시간 60~80% 단축**, Auto-sklearn/AutoGluon 등에서 비전문가의 **Kaggle급 성능 도달**(상위 5% 이내), GPU 자원의 Multi-fidelity 최적화로 **연산 비용 5~50배 절감**이 가능하다.
> 3. **판단 포인트**: **탐색 공간-비용-지연시간** 트레이드오프와 **Warm-start vs Cold-start**, **Black-box 제약조건(SLA/규제)** 하에서 해석가능성 확보 여부, 그리고 **NAS(Neural Architecture Search)** 적용 시 재현성과 Transferability 확보가 핵심 의사결정 기준이다.

---

## Ⅰ. 개요 및 필요성

전통적 ML 개발 프로세스는 **데이터 분석 -> 피처 엔지니어링 -> 모델 후보군 탐색 -> 하이퍼파라미터 튜닝 -> 앙상블/스태킹 -> 검증**이라는 다단계 수작업 사이클을 거친다. Kaggle Grandmaster조차 단일 프로젝트에 수백 회의 실험을 수행하며, KDD 2019 AutoML 트렌드 서베이에 따르면 **데이터 사이언티스트 업무 시간의 80% 이상이 피처 엔지니어링과 HPO(Hyperparameter Optimization)에 소모**된다. 또한 DL에서는 CNN 셀 구조, Transformer attention head 수, activation/skip connection 등 탐색 차원이 기하급수적으로 증가하여 **수동 설계는 더 이상 확장 불가능**하다.

AutoML은 이를 **"AutoModelSelection ⊕ HPO ⊕ Feature Engineering ⊕ Pipeline Optimization ⊕ NAS"**로 통합 자동화하여, *알고리즘 선택(Algorithm Selection)*과 *하이퍼파라미터 최적화(HPO)*를 결합한 **CASH 문제(Thornton et al., KDD 2013)**를 단일 베이지안 최적화 프레임워크로 정형화한다.

```text
[AutoML End-to-End Pipeline Concept]
  +---------------------------------------------------------------------+
  |                         AutoML Orchestrator                        |
  |             (Meta-Learner / Controller / Scheduler)                |
  +-----+-------------+--------------+----------------+-------------+---+
        |             |              |                |             |
        v             v              v                v             v
  +----------+  +----------+  +--------------+  +----------+  +----------+
  | Dataset  |  | Feature  |  | Model        |  |Hyperparam|  | Ensemble |
  | Meta-    |  | Engineer |  | Selection    |  |Optimizati|  | & Stacki |
  | Feature  |  | (Auto FE)|  | (Algorithm   |  | on (BO/  |  | ng       |
  | Extract  |  |          |  |  Library)    |  |  TPE/HB) |  |          |
  +----+-----+  +----+-----+  +------+-------+  +----+-----+  +----+-----+
       |             |               |                |              |
       +-------------+---------------+----------------+--------------+
                                    |
                                    v
                  +-------------------------------+
                  |  Best Pipeline + Leaderboard |
                  |  (모델·전처리·튜닝 결과 리포트)|
                  +-------------------------------+
```

**구 패러다임 vs AutoML 비교**
- **구 방식**: Scikit-learn 코드 직접 작성, GridSearchCV로 수십~수천 조합 전수조사, 각 trial별 수동 로깅 -> 엔지니어 의존성 ^, 재현성 v
- **AutoML 방식**: 탐색 공간 선언 -> 메타러너가 **Surrogate Model(GP/TPE) + Acquisition Function(Expected Improvement/UCB)**로 다음 trial 지시 -> 비동기 분산 실행 + 조기 종료로 자원 효율화

MLOps 측면에서도 AutoML은 **Feature Store + Model Registry + CI/CD**와 결합되어 "데이터 -> 모델 -> 배포"의 Lead Time을 수주에서 수시간으로 단축시킨다.

- **📢 섹션 요약 비유**: AutoML은 마치 **미슐랭 셰프들이 수만 가지 레시피 후보 중에서 요리 재료 조합과 불 세기를 자동으로 시뮬레이션해 최고의 레시피를 골라주는 'AI 미슐랭 오거나이저'**와 같다. 셰프(데이터 사이언티스트)가 레시피 후보군(탐색 공간)을 정해주면, 오거나이저(메타러너)가 시식(evaluation)을 통해 다음 후보를 지능적으로 선택한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

AutoML 시스템은 일반적으로 **① Search Space ② Search Strategy ③ Evaluation/Resource Manager ④ Meta-Learning/Memory ⑤ Pipeline Constructor**의 5계층으로 구성된다. 대표 구현체인 **Auto-sklearn 2.0**의 구조를 기준으로 분해하면 다음과 같다.

```text
[Auto-sklearn / AutoGluon 내부 아키텍처]
   +--------------------------------------------------------------+
   |  Layer 5: Pipeline Constructor (Stacked Ensemble Selector)   |
   |   +--> 15개 base model -> weighted ensemble (caruana 2004)    |
   +--------------------------------------------------------------+
   |  Layer 4: Meta-Learning Memory (Warm-Starting Knowledge)     |
   |   +- Dataset Meta-features (43-dim: #rows, skew, kurt, …)  |
   |   +- k-NN over OpenML-CC18 -> similar task config 추천        |
   |   +- Iterative ensemble (top-k configurations 누적)          |
   +--------------------------------------------------------------+
   |  Layer 3: Search Strategy (Sequential Model-Based Opt.)      |
   |   +- Bayesian Opt. (SMAC / GP / TPE)                         |
   |   +- Acquisition: EI / PI / UCB / LCB                       |
   |   +- Hyperband scheduler (Successive Halving)                |
   +--------------------------------------------------------------+
   |  Layer 2: Resource Manager (Multi-Fidelity Pruner)           |
   |   +- BOHB (Bayesian+Hyperband, Falkner 2018)                 |
   |   +- ASHA (Asynchronous Successive Halving, Ray)             |
   |   +- Population-Based Training (PBT, DeepMind)               |
   +--------------------------------------------------------------+
   |  Layer 1: Search Space Definition (Configuration Space)      |
   |   +- Preprocessors: 14 (imputation, scaling, one-hot…)       |
   |   +- Feature Preprocessors: 14 (PCA, LDA, …)                |
   |   +- Models: 15 (RF, XGBoost, LightGBM, CatBoost, …)        |
   |   +- Hyperparameters: Conditional / Tree-structured (TPE)    |
   +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Search Space Designer** | 알고리즘·전처리·하이퍼파라미터 후보군 정의 | Conditional HP(예: `solver='liblinear'`일 때만 `penalty` 활성), **Log-scale prior**(학습률 `1e-5~1e-1`는 log-uniform), **Hierarchical Space**(Optuna `suggest_int/log/categorical`) |
| **Search Strategy (SMBO)** | 다음 trial의 configuration 추천 | **SMAC**(Random Forest 기반 surrogate), **GP-EI**(Matern 5/2 kernel), **TPE**(Tree-structured Parzen Estimator, 각 HP별 `l(x)`/`g(x)` KDE 분리 추정 후 EI 계산), **BOHB**(BO + Hyperband 결합) |
| **Resource Manager (Multi-Fidelity)** | 저비용 평가로 유망 config 조기 선별 | **Hyperband**: `s_max=4, η=3`로 bracket 구성 -> Successive Halving으로 하위 (1/η) trial 제거, **ASHA**: 비동기 promotion으로 straggler 문제 해결, **PBT**: 주기적 perturbation + exploitation으로 신경망 HPO |
| **Meta-Learning Memory** | 유사 데이터셋의 과거 실험 결과로 warm-start | **Dataset Meta-feature**(statistical/landmark: 1-NN accuracy, decision tree leaf 수) -> **k-NN 거리**로 k개 dataset 선정 -> 그 dataset에서 가장 좋았던 config를 초기 seed로 사용 (Auto-sklearn의 핵심 차별점) |
| **Pipeline Constructor & Ensemble** | top-k trial들의 예측을 결합 | **Caruana Ensemble Selection**(greedy forward selection with replacement, 50개 sub-sample bag), **Stacking**(meta-learner로 Logistic Regression), **Bayesian Model Averaging** |

### 핵심 알고리즘: TPE (Tree-structured Parzen Estimator, Bergstra 2011)

`l(x)` = objective value의 quantile threshold `y*` **이하**인 configuration의 KDE 분포
`g(x)` = threshold **초과**인 configuration의 KDE 분포

Acquisition function:
$$\text{EI}_{\text{TPE}}(x) \propto \frac{l(x)}{g(x)} \quad (\text{最大化})$$

-> `l(x)/g(x)`가 클수록 "objective를 낮게 만드는 HP 영역"에 가까움. **Tree-structured**이기 때문에 categorical/conditional HP를 자연스럽게 다룰 수 있어 Optuna/Hyperopt의 기본 엔진이다.

### HPO의 수학적 정형화

$$\min_{x \in \mathcal{X}} f(x), \quad f(x) = \mathbb{E}_{(x_i, y_i)\sim \mathcal{D}}\left[\mathcal{L}\left(M_{x}(\mathcal{D}_{\text{train}}), \mathcal{D}_{\text{val}}\right)\right]$$

- `X`: search space (categorical × numerical mixed)
- `f(x)`: expensive black-box (한 trial 평가에 수분~수일)
- **Gradient 없음** -> BO가 적합, **Multi-fidelity**로 `f_budget(x; r)` (resource r로 평가) 근사

### NAS (Neural Architecture Search) 확장

| NAS 패러다임 | 대표 알고리즘 | 특징 |
| :--- | :--- | :--- |
| Reinforcement Learning | NAS-RL (Zoph 2017), ENAS | RNN controller가 child network sampling -> reward=val accuracy |
| Evolutionary | AmoebaNet, NSGANet | Population mutation/crossover, elitism selection |
| **Differentiable** | DARTS, PDARTS, PC-DARTS | α(architecture)와 w(weight)를 bilevel gradient로 joint optimize, **GPU 1일**만에 탐색 |
| One-shot / Weight-sharing | DARTS, ProxylessNAS, SPOS | Supernet 1회 학습 -> sub-network 평가, **SLM/TPU 가속** |
| Predictor-based | NAS-Bench-101/201, XGBoost predictor | 미리 계산된 lookup table 또는 학습된 predictor로 score 예측 |

**📢 섹션 요약 비유**: AutoML의 메타러너는 **"미지의 산맥에서 가장 높은 봉우리를 찾는 등반대"**와 같다. 베이지안 옵티마이저(Surrogate)는 **지형도**를 그려주고, Acqusition Function은 **"다음에 어디를 탐사할지 지시"**하며, Hyperband는 **"약한 등반대는 일찍 퇴출시켜 시간을 아끼는 컨트롤 타워"**다. 메타러닝은 **"이전에 등반한 비슷한 산의 노하우"**를 미리 가져다주는 등반 코치 역할이다.

---

## Ⅲ. 비교 및 연결

### 1. AutoML 구성 기술 비교

| 구분 | Grid Search | Random Search | Bayesian Opt. (SMAC/TPE) | Hyperband / BOHB | Population-Based |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **탐색 방식** | 전수 격자 | 균등 무작위 | Surrogate + Acquisition | Random + 자원 적응 | 집단 진화 |
| **성능** | 저차원만 유효 | 차원^에도 robust | 50~200 trial로 SOTA | 동일 budget에 5~50× 효율 | DL에 강점 |
| **연산 비용** | 매우 높음 | 선형 | 중간 (surrogate 비용 추가) | 매우 낮음 (pruning) | 중간 |
| **조건부 HP 지원** | △ | △ | ◎ (TPE tree) | △ | × |
| **조기 종료** | × | × | △ (early stopping surrogate) | ◎ (Successive Halving) | ◎ (kill + exploit) |
| **분산 환경** | △ (trivial parallel) | ◎ | △ (배치 BO 필요) | ◎ (ASHA 비동기) | ◎ |
| **대표 툴** | sklearn | sklearn, Ray Tune | Optuna, SMAC, Hyperopt | Ray Tune, BOHB, Determined | Ray Tune PBT, DeepMind |

### 2. 주요 AutoML 프레임워크 비교

| 프레임워크 | 지원 영역 | 백엔드 | 특징 | 한계 |
| :--- | :--- | :--- | :--- | :--- |
| **Auto-sklearn 2.0** | Tabular | sklearn, XGBoost, RF | Meta-learning + ensemble, OpenML 1000+ dataset | DL 미지원, 단일 머신 |
| **H2O AutoML** | Tabular | H2O, XGBoost | Stacked ensemble, MOJO 배포, Java/Spark 연동 | HP 공간 custom 어려움 |
| **TPOT** | Tabular | sklearn + genetic | Pipeline 전체를 GP 트리로 표현 | 학습 시간 길음 |
| **AutoGluon** | Tabular/Text/Image | MXNet, Torch | OOF stacking, multi-modal, GPU 가속 | 백엔드 lock-in |
| **FLAML** | Tabular/LLMs | sklearn, XGBoost, HF | CFO/CFO+ (cost-frugal optimization), LiteLLM | DL NAS 미지원 |
| **Auto-PyTorch** | Tabular/Image/Text | PyTorch | NAS + HPO 결합, Auto-Net 2.0 | 학습 시간 큼 |
| **Ray Tune + Optuna** | 범용 | Any | 분산 hyperparameter search, ASHA, PBT | 직접 구성 필요 |
| **NNI (Microsoft)** | 범용 | Any | NAS + HPO + compression, GUI/CLI 제공 | 야생 생태계 분산 |
| **Vertex AI / SageMaker Autopilot / Azure ML** | Managed | 클라우드 통합 | AutoML + MLOps 통합, 거버넌스 | 비용·벤더 종속 |
| **Google Vizier** | 범용 | Cloud | Multi-objective