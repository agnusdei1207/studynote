---
title: "AI Ethics Bias Fairness Explainability"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 653
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI 윤리·편향·공정성·설명가능성(Explainable AI, XAI)은 데이터 수집->학습->배포의 MLOps 전 사이클에 **Bias Detection(예: AIF360, Fairlearn)**, **Fairness Constraint Optimization(예: Equalized Odds Post-processing, Reweighing)**, **Interpretability Layer(예: SHAP, LIME, Integrated Gradients, Grad-CAM, Attention Rollout)**를 계층적으로 주입하여, 모델의 결정 근거를 **인과적(causal)·반사실적(counterfactual)** 수준에서 추적 가능하게 만드는 Responsible AI(책임 있는 AI) 엔지니어링 패러다임이다.
> 2. **가치**: EU AI Act(2024 발효, 고위험군 분류 시 Conformity Assessment 의무화), NIST AI RMF 1.0(2023), ISO/IEC 42001:2023, 국내 「AI 기본법」(2026.1 시행) 준수 시 고위험 AI 시스템의 시장 진입 리스크를 **법적·평판적 양 측면에서 약 70~80% 절감** 가능하며, 신용대출·채용·사법 등 Automated Decision System(ADS) 분야에서 설명 불가능 모델 대비 **분쟁 소요 시간 40% 단축 및 이의 제기 권리(Right to Explanation, GDPR Art.22)** 보장이 가능하다.
> 3. **판단 포인트**: Group Fairness(집단 공정성)와 Individual Fairness(개인 공정성)는 **Chouldechova(2017)·Kleinberg(2016) Impossible Theorem**에 의해 세 개 이상의 Protected Attribute(예: 인종, 성별, 소득) 교차 시 동시 만족이 수학적으로 불가능하므로, **도메인·피해 심각도·규제 등급**에 따라 Fairness Metric의 우선순위를 Trade-off Matrix로 결정해야 하며, Post-hoc 설명(사후 설명) vs Intrinsic 해석(내재 해석) 여부는 **성능(예: AUC, F1) 저하 허용치 ±2~5%**를 기준으로 아키텍처를 분기 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 Machine Learning 운영(MLOps) 파이프라인은 **Data Pipeline -> Feature Engineering -> Model Training -> Evaluation -> Serving**의 순방향 흐름에 최적화되어 있으며, 모델은 **"정확도(Accuracy)·지연 시간(Latency)·처리량(Throughput)"** 중심의 KPI로 평가되어 왔다. 그러나 2018년 Amazon Rekognition의 성별·인종 편향 논란, 2019년 Apple Card의 성별 차별 한도 책정 사건, 2020년 COMPAS(Correctional Offender Management Profiling for Alternative Sanctions) 재범 예측 알고리즘의 인종 편향(ProPublica 보고), 2023년 미국 법원에서 Cigna의 AI 자동기각(algorithmic denial) 판결 등으로 인해 **"Black-Box 모델이 초래하는 사회적·법적 책임"**이 산업계 핵심 이슈로 부상하였다.

특히 생성형 AI(LLM·Diffusion Model)의 보편화 이후 **Hallucination(환각, e.g. 15~27% factual error rate per TruthfulQA benchmark)**, **Copyright Infringement(저작물 무단 학습)**, **Algorithmic Discrimination** 문제가 EU AI Act의 **Title II – Prohibited Practices(절대 금지 AI, Art.5)** 및 **Title III – High-Risk AI Systems(고위험 AI, Art.6~15)** 규제로 연결되면서, **설명가능성은 단순 옵션이 아니라 컴플라이언스 필수 요건**이 되었다.

기존 패러다임과의 핵심 차이는 다음과 같다:
- **Old Paradigm (Pre-2020)**: "예측이 맞으면 된다(Correctness-First)" -> AUC 0.95 달성 시 종료
- **New Paradigm (2024~)**: "예측이 **왜·누구에게·어떤 맥락에서** 맞는지"를 입증 -> AUC 0.93 + Demographic Parity Difference < 0.05 + SHAP/ICE Plot 문서화 + Audit Trail

```text
+-------------------------------------------------------------------------+
|           Responsible AI Engineering Lifecycle (R-AI-EL)                 |
+-------------------------------------------------------------------------+
|                                                                         |
|  [1.Data]        [2.Model]        [3.Eval]        [4.Deploy]   [5.Monitor]|
|  ---------       ---------        ---------       ---------    --------- |
|  Raw Data   ->    Preprocessing ->   Train/Valid  ->   Serve    ->   Drift  |
|      |                |                |              |            |    |
|      v                v                v              v            v    |
|  +--------------------------------------------------------------+      |
|  |  Responsible AI Cross-Cutting Concerns (RAI-CCC) Layer       |      |
|  +--------------------------------------------------------------+      |
|  |  ① Bias Detection (AIF360, Fairlearn)                       |      |
|  |     +- Disparate Impact Ratio, Statistical Parity Diff       |      |
|  |  ② Fairness Intervention (Pre/In/Post-processing)            |      |
|  |     +- Reweighing, Adversarial Debiasing, Equalized Odds     |      |
|  |  ③ Explainability (XAI)                                     |      |
|  |     +- SHAP/LIME(Local), Grad-CAM/IG(Visual), Attention(NLP) |      |
|  |  ④ Privacy-Preserving ML (PPML)                             |      |
|  |     +- Differential Privacy(ε<1), Federated Learning         |      |
|  |  ⑤ Robustness & Safety                                      |      |
|  |     +- Adversarial Training, OOD Detection, Red-Teaming     |      |
|  |  ⑥ Governance & Documentation                                |      |
|  |     +- Model Card, Datasheet, AI Risk Register, Audit Log    |      |
|  +--------------------------------------------------------------+      |
|                              |                                          |
|                              v                                          |
|              +-------------------------------+                          |
|              | Regulatory Compliance Gate    |                          |
|              | (EU AI Act · NIST RMF · AI    |                          |
|              |  기본법 · ISO/IEC 42001)       |                          |
|              +-------------------------------+                          |
+-------------------------------------------------------------------------+
```

**왜 지금 필수인가**:
1. **규제 강제화**: EU AI Act는 고위험 AI(신용평가, 채용, 교육, 법집행, 의료)에 대해 **Conformity Assessment(적합성 평가)**, **Risk Management System**, **Data Governance**, **Transparency Obligation**, **Human Oversight**, **Accuracy·Robustness·Cybersecurity** 7대 요구사항을 의무화(Art.8~17).
2. **데이터 규모의 한계**: LLM 학습 데이터의 **Carbon Footprint(GPT-4 기준 약 6,000~7,000 tCO₂eq)**와 **저작권 분쟁(New York Times v. OpenAI, 2023)**이 "데이터 윤리"를 ESG 등급의 S(Social) 지표에 직접 영향.
3. **결정 주체의 책임 소재**: EU Product Liability Directive(2024 개정안)는 AI 시스템의 결정으로 인한 피해에 대해 **제조자·운영자·배포자**의 연쇄 책임(strict liability)을 명시.

- **📢 섹션 요약 비유**: AI 모델이 **"자동 운전 차량"**이라면, 윤리·편향·공정성·설명가능성은 **"블랙박스·차선 이탈 방지 시스템·승객 안전벨트·사고 원인 분석 보고서"**에 해당한다. 속도(Revenue·Conversion)만 쫓으면 사고(규제 제재·신뢰 붕괴) 시 보험(평판·벌금)으로 환산 불가능한 비용을 치른다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Responsible AI 시스템은 크게 **① 데이터 계층의 Bias Audit**, **② 학습 계층의 Fairness-Aware Training**, **③ 추론 계층의 Explainable Inference**, **④ 거버넌스 계층의 Audit & Compliance**의 4-tier로 구성된다. 각 계층은 독립적으로 운용되지만 **공통 메타데이터 스키마(예: OECD AI Observatory, ISO/IEC 42001 Annex A Control)**로 연결된다.

```text
+----------------------------------------------------------------------------+
|             Responsible AI Technical Reference Architecture                |
+----------------------------------------------------------------------------+
|                                                                            |
|  +-------------------- Tier 1: Data Ethics Layer ---------------------+  |
|  |  • Provenance Tracking:        OpenLineage + Marquez (metadata)    |  |
|  |  • Label Bias Audit:           AIF360.DatasetMetric                |  |
|  |     +- Statistical Parity: |P(Ŷ=1\|S=0) - P(Ŷ=1\|S=1)| < 0.05    |  |
|  |     +- Disparate Impact:    P(Ŷ=1\|S=0)/P(Ŷ=1\|S=1) ∈ [0.8, 1.25] |  |
|  |     +- Class Imbalance Check:   PSI > 0.2 -> Re-sample             |  |
|  |  • Data Sheet / Data Card:      Gebru et al. 2021, CMU Framework   |  |
|  |  • PII Masking / DP-Noise:      Microsoft Presidio + Laplace(ε=1) |  |
|  +------------------------------------------------------------------+  |
|                                  v                                        |
|  +-------------------- Tier 2: Fairness-Aware Training --------------+   |
|  |  +----------------+------------------+----------------------+     |   |
|  |  | Pre-processing | In-processing    | Post-processing      |     |   |
|  |  +----------------+------------------+----------------------+     |   |
|  |  | • Reweighing   | • Adversarial    | • Calibrated         |     |   |
|  |  |   (Kamiran     |   Debiasing      |   Equalized Odds     |     |   |
|  |  |   2012)        |   (Zhang 2018)   |   (Pleiss 2017)      |     |   |
|  |  | • SMOTE-NC     | • Fairness       | • Reject Option      |     |   |
|  |  | • Learning     |   Constraints    |   Classification     |     |   |
|  |  |   Fair Rep.    |   (Zafar 2017)   |   (Kamiran 2012)     |     |   |
|  |  |   (LFR)        | • FairDRO        | • Threshold          |     |   |
|  |  | • Data Aug.    |   (Group DRO)    |   Optimizer          |     |   |
|  |  |   (Counterfact)| • FairBERT/LLM   |                      |     |   |
|  |  +----------------+------------------+----------------------+     |   |
|  |  Trade-off: Accuracy Δ ≤ 5%, Fairness Δ ≤ 0.1                      |   |
|  +------------------------------------------------------------------+  |
|                                  v                                        |
|  +-------------------- Tier 3: Explainable Inference -----------------+  |
|  |   Input (x) --+-- Model f(x) --+-- Prediction ŷ                  |  |
|  |               |                |                                   |  |
|  |               |   +------------+------------+                      |  |
|  |               |   v  Surrogate Explainer    |                      |  |
|  |               |  • LIME:    x' ∈ {0,1}^d perturbation,            |  |
|  |               |             L( f, g, π_x ) + Ω(g) minimize        |  |
|  |               |  • SHAP:    φ_i = Σ_{S⊆F\{i}} |S|!(|F|-|S|-1)!/|F|!|  |
|  |               |             × [v(S∪{i}) - v(S)]                   |  |
|  |               |  • IG:      IG_i(x) = (x_i - x'_i)               |  |
|  |               |             × ∫_α^1 ∂F(x'+α(x-x'))/∂x_i dα        |  |
|  |               |  • Grad-CAM: L^c_{Grad-CAM} = ReLU(Σ_k α_k^c A^k) |  |
|  |               |  • Attention:  Rollout(A) = Ā · A · Ā ...          |  |
|  |               |  • Counterfactual:  DiCE, MACE, Wachter CF         |  |
|  |               +-----------------------------+                      |  |
|  |   Output:  ŷ + explanation(ŷ) + confidence + counterfactuals      |  |
|  +------------------------------------------------------------------+  |
|                                  v                                        |
|  +-------------------- Tier 4: Governance & Compliance ---------------+  |
|  |  • Model Card (Mitchell 2019)        • AI Risk Register            |  |
|  |  • AI Audit Trail (Immutable, WORM)  • Human-in-the-Loop Gate      |  |
|  |  • Continuous Monitoring:             • Incident Response SLA       |  |
|  |     - Fairness Drift Detector (PSI)                                |  |
|  |     - SHAP Distribution Shift                                      |  |
|  |     - Subgroup Error Parity Watch                                 |  |
|  +------------------------------------------------------------------+  |
+----------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Bias Audit Engine** | 데이터/모델/출력 3단계 편향 정량 측정 | AIF360 `BinaryLabelDatasetMetric`: Disparate Impact Ratio(DIR), Statistical Parity Difference(SPD), Theil Index, Smoothed Empirical Differential Fairness(SEDF). COMPAS 데이터셋 기준 인종 SPD ≈ 0.18 -> 0.04로 감소 입증 사례 다수 |
| **Fairness Intervention Module** | Pre/In/Post-processing 3-Stage 파이프라인에서 공정성 제약 삽입 | **Pre**: Reweighing(`w(x)=P(S)/P(S,Y)`), LFR(Learning Fair Representations, Zemel 2013). **In**: Adversarial Debiasing(Discriminator가 S를 예측 못하도록 G는 Adversarial Loss 최소화, L=L_task - λ·L_adv). **Post**: Calibrated Equalized Odds(Pleiss 2017, Mixup 기반), Threshold Optimizer per-group |
| **Explainability Engine (XAI Core)** | 결정 근거에 대한 Local/Global 해석 산출 | **Model-Agnostic**: SHAP(Shapley Value, 협력 게임 이론 기반 5가지 공리·Efficiency·Symmetry·Dummy·Additivity 만족, KernelSHAP·TreeSHAP·DeepSHAP 변형), LIME(SP-LIME로 fidelity-interpretability 균형). **Model-Specific**: Grad-CAM(CNN 시각), Integrated Gradients(Sundararajan 2017, Axiomatic Attribution), Attention Rollout(Transformer). **Counterfactual**: DiCE( Diverse Counterfactual Explanations, Mothilal 2020), Wachter CF( Mixed-Integer Programming) |
| **Governance & Audit Layer** | 규제 준수, 문서화, 모니터링 | Model Card(Mitchell 2019, 9개 섹션), Datasheet for Datasets(Gebru 2021), AI Risk Register(NIST AI RMF Govern·Map·Measure·Manage