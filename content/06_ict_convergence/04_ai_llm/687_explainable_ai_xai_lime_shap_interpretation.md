---
title: "Explainable AI XAI LIME SHAP Interpretation"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 687
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: XAI(Explainable AI)는 블랙박스 모델 $f(x)$의 예측 결과 $y$에 대해 인간이 인지 가능한 $\text{Explanation}(x)$를 사후적으로(post-hoc) 산출하는 메커니즘으로, **LIME**은 국소 선형대수 근사(Local Surrogate) 기반, **SHAP**은 협력게임이론의 Shapley Value를 특성 기여도에 매핑하는 **가법적 설명 모형(Additive Feature Attribution Model)** 이다.
> 2. **가치**: GDPR 제22조(자동화된 의사결정에 대한 권리), EU AI Act(2024), 금융권의 SR 11-7, 의료 AI의 FDA GMLP(Guidance for Machine Learning-Enabled Medical Devices) 등 규제 컴플라이언스 충족, 모델 디버깅·편향·공정성 검증·인과추론 보조를 통해 MLOps 전주기 거버넌스 강화 및 모델 신뢰도 20~40% 향상에 기여한다.
> 3. **판단 포인트**: **LIME**은 모델 무관(model-agnostic)·저비용이지만 표본 추출·$\pi_x$ 가중치 설정에 따라 설명의 **불안정성(Instability)** 문제가 발생하고, **SHAP**은 이론적 일관성(Locally Accurate·Missingness·Consistency 3대 공리)을 보장하나 $O(2^M)$ 계산 복잡도로 고차원 데이터에서 TreeSHAP·SamplingSHAP 등 알고리즘 선택이 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

딥러닝·앙상블·LLM 등 고성능 모델이 산업 현장에서 결정적 의사결정을 내리면서, **"왜(Why)"** 라는 질문이 더 이상 학술적 호기심이 아닌 법적·윤리적 필수 요건이 되었다. 전통적인 **Transparent Box Model**(Decision Tree, Linear/Logistic Regression, GAM 등)은 본질적으로 해석 가능하지만 예측 성능이 낮고, **Black-Box Model**(DNN, XGBoost, Transformer)은 성능은 우수하나 의사결정 근거를 인간이 직관적으로 이해하기 어렵다. 이 간극을 메우기 위해 **DARPA XAI Program(2017)**, **Gartner Hype Cycle for AI**의 5대 메가트렌드 채택, 그리고 **OECD AI Principles(2019)** 및 국내 **AI 신뢰성 평가 가이드라인(NIA, 2023)** 등 다양한 표준이 등장했다.

```text
[ XAI 전체 아키텍처 - Black-Box 모델 해석 파이프라인 ]

   +--------------------+                        +----------------------+
   |  Input Domain (X)  |                        |  Explanation Layer   |
   |  +--------------+  |    f: X -> Y             |  +----------------+  |
   |  | Raw Feature  |--+------+                 |  |  Local Expl.   |  |
   |  | (고차원·비선형)|  |      |                 |  |  LIME / Kernel |  |
   |  +--------------+  |      v                 |  |  SHAP / LRP    |  |
   +--------------------+  +--------------+      |  +----------------+  |
                          |  Black-Box   |      |  +----------------+  |
   +--------------------+  |   Model f    |      |  |  Global Expl.   |  |
   |  Background Data   |-->|  (DNN/XGB/  |------>|  |  SHAP Summary / |  |
   |   (Perturbation)   |  |  Transfomer) |      |  |  Feature Import |  |
   |                    |  +------+-------+      |  +----------------+  |
   +--------------------+         | y             |  +----------------+  |
                                  v                |  |  Visual Expl.  |  |
                          +--------------+         |  |  Force/Depend  |  |
                          |  Prediction  |--------->|  |  /Decision Plot|  |
                          |  y = f(x)    |         |  +----------------+  |
                          +--------------+         +----------------------+
                                                          |
                                                          v
                                                [End User: 도메인 전문가,
                                                 감사자, 의사결정권자, 규제기관]
```

전통적 ML 시대는 **단일 모델의 단일 해석**(예: 회귀계수 $\beta_i$)으로 충분했으나, **하이퍼파라미터 수천~수만 개**의 딥러닝과 **앙상블 트리**가 등장하면서 ① **Local 해석**(개별 예측), ② **Global 해석**(전체 모델 거동), ③ **Counterfactual 해석**(입력 변경 시 결과 변화), ④ **Model Comparison**(서로 다른 모델 간 거동 비교)의 4단계 해석 체계가 요구된다. LIME·SHAP은 ①번에 최적화되어 있고, 이를 확장해 ②③④까지 아우르는 통합 XAI 플랫폼이 **H2O.ai Explainable AI, Microsoft InterpretML, AWS SageMaker Clarify, Google Vertex AI Explainable AI** 등으로 산업화되었다.

- **📢 섹션 요약 비유**: 의사가 환자에게 "당신은 감기입니다"라고만 하면 환자는 불안하지만, "체온 38.5℃, 백혈구 12,000, 인후 발적 -> 종합하면 인플루엔자 의심 -> 따라서 타미플루 처방"처럼 **근거와 결론의 사슬**을 보여주면 환자가 치료에 협조하는 것과 같다. XAI는 바로 그 **근거 사슬(Reasoning Chain)**을 AI 모델에 부여하는 기술이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. LIME (Local Interpretable Model-agnostic Explanations, KDD 2016)

LIME의 핵심 가정은 *"복잡한 비선형 모델 $f$도 국소 영역에서는 단순한 선형 모델 $g$로 충분히 근사 가능하다"* 는 **Locally Linear Approximation**이다. 알고리즘은 4단계로 구성된다.

```text
[ LIME 알고리즘 상세 흐름도 ]

   Step 1) 원본 x (연속형 d차원) -> 이진 표현 x' (interpretable representation)
           예) Tabular: x' ∈ {0,1}^d  (존재/비존재)
               Text:     x' ∈ {0,1}^T  (단어의 출현 여부)
               Image:    x' ∈ {0,1}^S  (super-pixel의 on/off)

   Step 2) Perturbation Sampling
           +------------------------------------------+
           |  z' ∈ {0,1}^d  : x' 주변 N개 샘플 생성   |
           |  z = h_x(z')    : 원본 공간으로 역변환     |
           |  y_i = f(z_i)   : 블랙박스 예측값 획득     |
           +------------------------------------------+
                          |
                          v
   Step 3) Distance-weighted Surrogate Fitting
           π_x(z) = exp(-D(x,z)^2 / σ^2)   <- 지수 커널 가중치
           g(z') = w_g · z'                  <- interpretable model
           L(f, g, π_x) = Σ π_x(z)·(f(z)-g(z'))^2
                          |
                          v
   Step 4) Explanation
           ξ(x) = argmin_{g ∈ G}  L(f, g, π_x)  +  Ω(g)
                                          ^ 모델 복잡도 penalty (예: non-zero 계수 수)
           -> 상위 K개 feature의 가중치 w_g 를 "기여도"로 반환
```

핵심 수식 분해:
- **LIME의 목적함수** $\xi(x) = \arg\min_{g} L(f, g, \pi_x) + \Omega(g)$에서 $\Omega(g)$는 모델의 복잡도(예: 의사결정 규칙 수, 비영 계수 수)를 제한하여 인간이 읽을 수 있는 수준으로 강제한다.
- **SP-LIME(Submodular Pick)**는 전체 데이터셋에 대한 **대표적인 설명 K개**를 추출하기 위해 **Submodular Optimization**(Greedy + Marginal Gain)을 적용, 전역적(global) 이해를 가능케 한다.
- **LIME 한계**: ① perturbation 시 의미 없는 데이터(out-of-distribution) 생성 가능 -> **LORE**(2022)가 counterfactual-aware 샘플링으로 보완, ② Kernel width $\sigma$ 민감성 -> **ALIME**(2020)가 Auto-Encoder 기반 가중치 자동학습 제안, ③ 불안정성(instability) -> 동일 입력에 대해 매번 다른 설명 발생.

### 2. SHAP (SHapley Additive exPlanations, NIPS 2017)

SHAP은 **1953년 Lloyd Shapley의 게임이론**에서 유래한 **Shapley Value**를 ML에 적용한 것으로, 3대 공리(①Local Accuracy / ②Missingness / ③Consistency)를 모두 만족하는 **유일한(uniqueness) 설명 방법**이다.

```text
[ SHAP 가치 산출 메커니즘 - Shapley Value 계산 그래프 ]

   F = {1,2,...,M}  : 전체 feature 집합
   S ⊆ F\{i}       : feature i를 제외한 부분집합
   f_x(S)          : S에 속한 feature만 사용한 예측 (marginal contribution)

   +--------------------------------------------------------+
   |                  Shapley Value (φ_i)                    |
   |                                                        |
   |              |S|! · (M - |S| - 1)!                      |
   |  φ_i  =   Σ -------------------------- · [f(S∪{i}) - f(S)]|
   |           S⊆F\{i}              M!                       |
   |                                                        |
   |   ^              ^              ^                      |
   |   |              |              |                      |
   | 가중치       한계기여도       가법적 설명식              |
   | (조합가중)   (marginal)      g(z') = φ_0 + Σ φ_i z_i'   |
   +--------------------------------------------------------+
                          |
                          v
   SHAP 변형 알고리즘 (데이터/모델별 최적화)
   +----------+----------+-------------+-------------+------------+
   |  Kernel  |  TreeSHAP|  DeepSHAP   | SamplingSHAP|  LinearSHAP|
   |  SHAP    |  (Lundb.)|  (DeepLift  | (Stochastic | (Linear    |
   | (Model-  |  O(TLD²) |   기반)     |  Approx.)   |  Regression|
   | agnostic)|  Tree전용 |  DNN전용    |  O(MS) 표본 |  계수와동일)|
   +----------+----------+-------------+-------------+------------+
                          |
                          v
   Visualization Layer
   +--------------+--------------+---------------+--------------+
   |  Force Plot  | Summary Plot | Dependence    |  Decision    |
   | (1 instance) | (전체)       | Plot (2D)     |  Plot (acc.) |
   +--------------+--------------+---------------+--------------+
```

**SHAP의 3대 이론적 공리**:
1. **Local Accuracy** (효율성): $f(x) = g(x') = \phi_0 + \sum_{i=1}^M \phi_i x_i'$ — 단일 예측값이 모든 특성 기여도의 합과 일치
2. **Missingness**: $x_i' = 0$이면 $\phi_i = 0$ — 누락된 특성은 기여도 0
3. **Consistency**: 모델이 바뀌어 한 특성의 marginal contribution이 증가하면 $\phi_i$는 절대 감소하지 않음 -> **LIME의 불안정성 문제 해결**

**KernelSHAP의 실전 손실함수**:
$$L(\pi, f) = \sum_{z' \in Z} \left[ f(h_x(z')) - \underbrace{\mathbb{E}_{X}[f(X)]}_{\phi_0} - \sum_{i=1}^M \phi_i z_i' \right]^2 \pi_x'(z')$$
샘플링 $z' \sim \{0,1\}^M$에 대해 가중 최소제곱으로 $\phi$를 복원하며, $M$이 클 때 $2M+1$개의 strategic 샘플만으로 정확한 해를 구한다.

**TreeSHAP 시간 복잡도**:
$$T_{\text{TreeSHAP}} = O(T \cdot L \cdot D^2)$$
$T$=트리 수, $L$=리프 수, $D$=깊이. XGBoost/LightGBM/CatBoost 등 트리 기반 모델에 대해 다항시간 내 정확한 Shapley value 계산이 가능하다.

### 3. 핵심 구성 요소 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Interpretable Representation $x'$** | 원본->해석가능 공간 변환 | Tabular: 0/1 존재벡터 / Text: TF-IDF 단어 존재 / Image: super-pixel mask (Quickshift, Felzenszwalb) |
| **Perturbation / Sampling Engine** | 국소 영역 샘플 생성 | LIME: 0/1 마스킹 노이즈