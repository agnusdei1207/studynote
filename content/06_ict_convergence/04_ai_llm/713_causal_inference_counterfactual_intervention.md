---
title: "Causal Inference Counterfactual Intervention"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 713
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 인과 추론 반사실 분석 개입 효과는 Judea Pearl의 Structural Causal Model(SCM)과 Donald Rubin의 Potential Outcomes Framework를 통합하여 관측 데이터에서 `P(Y|do(X))`를 식별하고, 실제로 발생하지 않은 반사실적 상황(`Y_x(u)`)을 정량화하여 처치(Treatment)의 인과 효과를 추정하는 통계적·인과적 추론 체계이다.
> 2. **가치**: 전통적 머신러닝의 예측 정확도(Accuracy) 대비, 의사결정의 정책적 함의(Policy Implication)를 30~70% 수준으로 제고하고, A/B 테스트의 표본 효율성을 propensity score weighting(IPW)·doubly robust estimator(AIPW) 등을 통해 분산 15~40% 절감 가능하다. 또한 Selection Bias·Confounding로 인한 잘못된 의사결정 비용을 사전에 차단한다.
> 3. **판단 포인트**: 핵심 trade-off는 (1) **식별 가정(Identification Assumption)**의 실현 가능성(SUTVA, ignorability, positivity, consistency) vs 인과 효과 추정의 정밀도, (2) **관측 연구(Observational Study)**의 데이터 풍부성 vs 무작위 통제 시험(RCT)의 인과 타당도, (3) **개입 모델(Interventional)**과 **반사실 모델(Counterfactual)**의 그래프 분리·통합 설계이다.

---

## Ⅰ. 개요 및 필요성

전통적인 머신러닝과 통계학은 **"연관성(Correlation)"** `P(Y|X)`을 모델링하는 데 최적화되어 있다. 그러나 비즈니스·정책·의료 현장에서 요구하는 의사결정은 **"원인(Causation)"** `P(Y|do(X))`이다. "광고 노출이 매출을 증가시켰는가?", "특정 약이 환자를 회복시켰는가?", "신규 기능이 사용자 이탈률을 낮췄는가?"와 같은 질문은 모두 인과적이며, 단순한 상관관계 분석으로는 **Confounding Variable(교락변수)**로 인해 잘못된 결론을 도출할 위험이 크다. Judea Pearl은 이를 **"Ladder of Causation"**으로 3단계(Association -> Intervention -> Counterfactual)로 계층화하였고, 그 정점에서 반사실적 추론이 위치한다.

특히 개입 효과(Intervention Effect)는 "X를 X'로 변경했을 때 Y의 변화량"을 정량화하는 것으로, A/B 테스트·이중차분법(DID)·회귀불연속설계(RDD)·도구변수(IV)·매칭(Matching)·Causal Forest 등의 방법론이 실제 환경에 적용된다. 그러나 관측 데이터만으로는 RCT를 수행할 수 없는 의료·경제·소셜 네트워크 환경에서 **"do-operator"**를 통해 인과적 효과를 근사 추정하는 기술이 필수적이다.

```text
[인과 추론 3단계 사다리: Ladder of Causation]

      +-------------------------------------+
      |  ③ Counterfactual (반사실)         |  <- Y_x(u): 만약 ~이었다면?
      |     "관측되지 않은 세계"             |     P(Y_x | X, Y)
      +----------------^--------------------+
                       | (SCM + do-calculus 필요)
      +----------------+--------------------+
      |  ② Intervention (개입)              |  <- P(Y | do(X=x))
      |     "만약 X를 강제로 x로 설정한다면"  |     do-calculus + DAG
      +----------------^--------------------+
                       | (그래프 절단 필요)
      +----------------+--------------------+
      |  ① Association (연관)              |  <- P(Y | X)
      |     "X를 가진 사람이 Y일 확률"       |     통계/ML의 전통 영역
      +-------------------------------------+

[기존 통계 vs 인과 추론 패러다임 비교]

    기존 통계/ML                인과 추론 (Causal Inference)
   +--------------+           +--------------------------+
   | Data: 관측치 |           | Data: 관측치 + 개입 이력  |
   | Model: y=f(x)|   ---►   | Model: SCM, DAG, PO      |
   | Goal: 예측   |           | Goal: 인과 효과 추정      |
   | Question: ?  |           | Question: What if / Why? |
   +--------------+           +--------------------------+
        v                                v
   "X면 Y일 확률"               "X가 Y를 발생시켰는가?"
   (Correlation)                 (Causation)
```

- **📢 섹션 요약 비유**: 연관성은 "아이스크림이 많이 팔리면 익사 사고가 늘어난다"는 통찰을 주는 것이고, 인과 추론은 "실제 원인은 더운 날씨(Confounder)이며, 아이스크림이 익사를 유발하지 않는다"는 진짜 원인을 밝혀내는 **탐정 수사**와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

인과 추론의 핵심 아키텍처는 **(1) Structural Causal Model(SCM)로 인과 그래프(Causal DAG)를 명시화 -> (2) do-calculus로 개입(Intervention)의 확률 분포 변환 -> (3) Potential Outcomes로 반사실(Counterfactual) 정량화**의 3단 파이프라인으로 구성된다.

```text
[인과 추론 시스템 아키텍처]

  +--------------------------------------------------------------+
  |  ① Causal DAG (Directed Acyclic Graph) 명시화               |
  |  +-----+   Z   +-----+                                     |
  |  |  Z  |------►|  X  |--► Y                                |
  |  |Confounder |Trmt |  Outcome                              |
  |  +-----+   ^   +-----+                                     |
  |              +-- selection bias                            |
  |  [변수 간 인과 방향 명시, Backdoor/Frontdoor Path 식별]      |
  +--------------------------+-----------------------------------+
                             v
  +--------------------------------------------------------------+
  |  ② do-calculus: Intervention Operator 적용                  |
  |   P(Y=y | do(X=x)) = Σz P(Y=y|X=x, Z=z) P(Z=z)            |
  |   [X로 들어오는 모든 incoming edge를 절단(graph mutilation)] |
  |   [Rule 1: Insertion/Deletion of Observations]              |
  |   [Rule 2: Action/Observation Exchange]                     |
  |   [Rule 3: Insertion/Deletion of Actions]                   |
  +--------------------------+-----------------------------------+
                             v
  +--------------------------------------------------------------+
  |  ③ Counterfactual Reasoning Layer                           |
  |  Y_x(u) = Y_{M_x(u)}(u)  [3-step abduction-action-prediction]
  |  [개별 단위(u) 수준 반사실 효과: τ_i = Y_1(u) - Y_0(u)]     |
  |  [반사실 검증: Twin Network, Normalized Weighted Causal...] |
  +--------------------------+-----------------------------------+
                             v
  +--------------------------------------------------------------+
  |  ④ Causal Effect Estimator (ATE, ATT, CATE, ITE)           |
  |  - Matching / IPW / AIPW / Doubly Robust                    |
  |  - Instrumental Variable (2SLS)                             |
  |  - Difference-in-Differences (DID) / Synthetic Control      |
  |  - Causal Forest / Causal Tree (Heterogeneous Effects)      |
  |  - G-computation / TMLE (Targeted Maximum Likelihood)       |
  +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Causal DAG / SCM** | 인과 구조 명세화 | 변수 노드(원인·결과·교락) + 방향성 엣지로 표현. `M`-구조(Mediator), `Colliders`, `Confounders`를 식별. `d-separation` 기준으로 조건부 독립성 검증. |
| **do-calculus Operator** | 개입의 확률 분포 변환 | Pearl의 3가지 규칙으로 `P(Y\|do(X))`를 관측 분포 `P(Y\|X)`로 환원. **graph mutilation**: X의 모든 incoming edge 제거. Backdoor adjustment: `Σ_z P(Y\|X,Z)P(Z)`. Frontdoor adjustment: 매개변수 M을 통한 식별. |
| **Potential Outcomes (Neyman-Rubin)** | 반사실 변수 정량화 | `Y_i(1)`, `Y_i(0)` 동시 정의. **Fundamental Problem of Causal Inference**: 한 개인의 두 잠재적 결과는 동시 관측 불가. ITE `τ_i = Y_i(1) - Y_i(0)` 정의. |
| **Causal Effect Estimator** | ATE/ATT/CATE/ITE 추정 | ATE = `E[Y(1)-Y(0)]`. ATT = `E[Y(1)-Y(0)\|T=1]`. CATE = `E[Y(1)-Y(0)\|X=x]`. 추정 방법: (a) **IPW**(Inverse Propensity Weighting): `E[ Y·T/e(X) - Y·(1-T)/(1-e(X)) ]` (b) **AIPW**: IPW + 회귀 모델의 **doubly robust** 결합 (c) **TMLE**: 효율성 극대화 (d) **Causal Forest**: 이질적 처치 효과(HTE) 추정 (e) **Synthetic Control**: 단일 처리 단위 가중합 구성 |
| **Identification Assumption Layer** | 가정 검증·민감도 분석 | SUTVA(Stable Unit Treatment Value), Ignorability/Unconfoundedness(`(Y(0),Y(1))⊥T\|X`), Positivity(`0<P(T=1\|X)<1`), Consistency(`Y=Y(T)`). E-value, Rosenbaum bounds로 미관측 교락 변수 강도 측정. |

### 핵심 수식 및 알고리즘

**(1) Backdoor Adjustment Formula (Pearl, 1995)**

$$P(Y=y \mid do(X=x)) = \sum_{z} P(Y=y \mid X=x, Z=z) \cdot P(Z=z)$$

여기서 Z는 X의 모든 backdoor path를 차단하는 조정 변수 집합.

**(2) Inverse Propensity Weighting (IPW) Estimator**

$$\widehat{ATE}_{IPW} = \frac{1}{n} \sum_{i=1}^{n} \left[ \frac{T_i Y_i}{\hat{e}(X_i)} - \frac{(1-T_i) Y_i}{1-\hat{e}(X_i)} \right]$$

여기서 `e(X) = P(T=1|X)`는 propensity score, propensity clipping(`0.01 < e < 0.99`)으로 분산 폭발 방지.

**(3) Doubly Robust (AIPW) Estimator**

$$\widehat{ATE}_{AIPW} = \frac{1}{n} \sum_{i=1}^{n} \left[ \hat{\mu}_1(X_i) - \hat{\mu}_0(X_i) + \frac{T_i(Y_i - \hat{\mu}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-T_i)(Y_i - \hat{\mu}_0(X_i))}{1-\hat{e}(X_i)} \right]$$

둘 중 하나만 일관 추정량이어도 일관성 확보 -> **이중 강건성(Doubly Robust)** 보장.

**(4) Counterfactual Computation (3-step process)**

1. **Abduction**: Evidence `E=e`를 통해 외생 변수 U의 사후 분포 `P(U|E=e)` 추론
2. **Action**: `do(X=x)` 적용, modified SCM `M_x` 획득
3. **Prediction**: `M_x`에서 U의 사후 분포를 입력으로 Y의 분포 예측

-> 결과: `Y_x(u) = Y_{M_x(u)}(u)` (개별 단위 반사실 결과)

- **📢 섹션 요약 비유**: SCM은 "요리 레시피"이고, do-calculus는 "불을 강제로 켜는 스위치"이며, 반사실 추론은 "레시피대로 만들었지만 만약 소금을 더 넣었더라면 어땠을까?"를 되돌아보는 **시계 역행** 시뮬레이션과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | **전통 통계/A/B 테스트 (RCT)** | **관측 인과 추론 (Observational Causal)** | **반사실 인과 추론 (Counterfactual)** |
| :--- | :--- | :--- | :--- |
| **데이터 형태** | 무작위 배정된 실험군·대조군 | 자연 발생하는 관측 데이터(과거 로그 등) | 관측 + 개입 이력 + 도메인 지식 결합 |
| **핵심 가정** | 무작위 배정(임의성) | Ignorability(비관측 교락 부재) | SUTVA + Consistency + Positivity |
| **식별 가능성** | 모든 변수 동일 분포 하에서 항상 가능 | 그래프 구조 + 가정 검증 필요 | SCM 매개변수 베이지안 추론 필요 |
| **추정 가능 효과** | ATE (Average Treatment Effect) | ATE, ATT, ATU, CATE | ITE (Individual Treatment Effect) |
| **표본 효율성** | 표본 크기 큼(통계적 검정력 위해) | 상대적으로 작은 표본으로 가능 | 데이터 부족 시 Causal Forest로 보완 |
| **외부 타당도(External Validity)** | 낮음(특정 모집단 한정) | 높음(현실 데이터 기반) | 높음 + 시나리오 분석 가능 |
| **주요 한계** | 비용·윤리적 제약(의료·정책 적용 어려움) | 미관측 교락 변수(Unobserved Confounder) 민감 | 계산 복잡도, 가정이 강함 |
| **대표 기법** | T-test, ANOVA, Randomization Unit | IPW, Matching, PS, Doubly Robust, IV, DID | SCM + Twin Network, CEVAE, GANITE, CausalBERT |
| **활용 사례** | 신규 약 임상 시험, UX A/B 테스트 | 마케팅 캠페인 효과, 의료 코호트 분석 | 개인화 처방, 추천 시스템, 헬스케어 시뮬레이션 |

**다른 시스템·도구와의 연결:**

- **Lift Analysis / Uplift Modeling**: 마케팅 인과 효과 측정에 CATE 직접 활용 (Library: `CausalML`, `DoWhy`, `EconML`, `Dowhy`/`EconML` MS Research OSS)
- **A/B Test Platform (Optimizely, GrowthBook)**: `do(T=1)`의 시뮬레이션을 RCT로 실증
- **Recommender System**: 추천 개입이 만족도를 증가시켰는지 Causal Recommendation (Counterfactual Reasoning)로 분석
- **Time-Series Causal (PCMCI, VAR-LiNGAM)**: Granger 인과성 + 비선형 인과 발견 알고리즘
- **LLM Causal Reasoning**: GPT/Claude 모델에 DAG 명시 + Counterfactual Prompt로 인과 추론 능력 평가

- **📢 섹션 요약 비유**: RCT는 "정해진 온도에서 요리"이고, 관측 인과 추론은 "이미 만들어진 음식을 역추적해 레시피를 추론"하는 것이며, 반사실 추론은 "다른 재료로 다시 만들었을 때 맛을 미리 시식"하는 **예지몽**과 같다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 실무자형 판단 체크리스트

1. **DAG 명시화 및 d-separation 검증**: 도메인 전문가(SME)와 함께 모든 관측 변수의 인과 관계를 명시