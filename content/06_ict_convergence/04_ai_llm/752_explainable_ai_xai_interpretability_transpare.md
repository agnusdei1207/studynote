---
title: "Explainable AI XAI Interpretability Transparency"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 752
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 설명 가능 AI(XAI)는 블랙박스 모델(심층 신경망, 앙상블, LLM 등)의 의사결정 과정을 인간이 이해 가능한 형태(규칙, 피처 기여도, 개념, 반사실)로 투명하게 변환하는 MLOps 핵심 영역으로, **모델 자체의 해석 가능성(Intrinsic Interpretability)**과 **사후 설명(Post-hoc Explanation)**으로 이원화되며 SHAP(게임 이론 기반 Shapley Value), LIME(국소 선형 근사), Grad-CAM(그래디언트 기반 시각화), Integrated Gradients(축적 경로 적분), LRP(층별 역전파), TCAV(개념 활성화 벡터) 등의 알고리즘이 표준 스택을 구성한다.
> 2. **가치**: EU AI Act(2024.08 발효)·GDPR 제22조(Right to Explanation)·NIST AI RMF 1.0·ISO/IEC 42001(AIMS) 등 글로벌 규제에서 고위험 AI 시스템(신용평가·의료·채용·법집행)의 설명 의무가 강제됨에 따라, XAI 도입 시 **모델 거버넌스 컴플라이언스 확보 + 모델 디버깅/편향 탐지 + 사용자 신뢰도(Trust Calibration) 향상**이라는 정량·정성적 가치를 동시에 달성하며, 의료 AI에서는 진단 정당화 근거 제공으로 임상 의사결정 보조 정확도를 12~18% 향상시킨 사례(Mayo Clinic, 2023)가 보고되었다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **①예측 성능 vs 해석 가능성(Inherent-accuracy trade-off)**, **②국소 충실도 vs 전역 일관성(Local vs Global fidelity)**, **③설명의 충실도(Faithfulness) vs 인간 이해도(Comprehensibility)**, **④계산 비용 vs 응답 지연(SHAP Exact는 O(2^M), KernelSHAP O(M²))**이며, 아키텍처 선택 시 **도메인 위험도(High-stakes 여부), 데이터 모달리티(테이블/이미지/NLP), 설명 대상 이해도(개발자/도메인 전문가/일반 사용자/규제자)**에 따라 Intrinsic-by-design, Post-hoc, Surrogate model, Concept-based 중 최적 전략을 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 통계학습(SVM, Random Forest, XGBoost)은 변수 중요도(Variable Importance)·결정경계 시각화 등 제한적이나 의미 있는 설명을 제공했으나, 2012년 AlexNet 이후 급부상한 딥러닝과 2017년 이후의 대규모 언어 모델(LLM), 그리고 2020년대 이후 멀티모달·생성형 AI로 패러다임이 전환되면서 **모델 내부의 비선형·고차원·분산 표현(Distributed Representation)**이 인간의 직관적 이해 범주를 완전히 벗어나게 되었다. 이러한 "블랙박스화"는 정확도(Accuracy)·AUC·F1 등 성능 지표로는 환원되지 않는 새로운 위험 차원을 야기한다.

DARPA(미국 국방고등연구계획국)는 2016년 XAI(Explainable AI) 프로그램을 통해 학계·산업계의 설명 가능성 연구를 체계화하였으며, DARPA의 정의에 따르면 XAI는 "사용자가 AI 시스템의 의사결정을 이해·신뢰·효과적으로 관리할 수 있도록 하는 AI 시스템 개발"을 의미한다. 이 정의를 분해하면 다음 4가지 핵심 요구가 도출된다:

- **Explanation**: 모델이 왜 그런 예측/결정을 내렸는지에 대한 근거 제시
- **Meaningfulness**: 설명 대상(개발자, 도메인 전문가, 일반 사용자, 규제자)에게 의미 있는 형식
- **Accuracy of Explanation**: 설명 자체가 모델 동작을 정확히 반영(Faithfulness)
- **Knowledge Limits**: 모델이 "모르는 것을 모른다"는 불확실성 정량화

```text
[ XAI 개념적 흐름도: 블랙박스에서 인간 이해로 ]

  +-------------+       +-----------------+       +----------------+
  | Input Data  |------->|  Black-Box Model|------->|  Prediction    |
  | (X ∈ ℝ^n)  |       | (DNN/Ensemble/  |       |  (ŷ ∈ ℝ^k)    |
  |             |       |   LLM/SVM/...)  |       |                |
  +-------------+       +-----------------+       +--------+-------+
                                                           |
                                                           v
                              +------------------------------------------+
                              |      Explanation Layer (XAI)             |
                              |  +--------------+  +------------------+  |
                              |  | Feature      |  | Concept-based    |  |
                              |  | Attribution  |  | (TCAV, CBM)      |  |
                              |  | (SHAP/LIME)  |  |                  |  |
                              |  +--------------+  +------------------+  |
                              |  +--------------+  +------------------+  |
                              |  | Visual       |  | Counterfactual   |  |
                              |  | Saliency     |  | (DiCE, Wachter)  |  |
                              |  | (Grad-CAM)   |  |                  |  |
                              |  +--------------+  +------------------+  |
                              |  +--------------+  +------------------+  |
                              |  | Rule-based   |  | Attention        |  |
                              |  | (Anchors,    |  | Map/Token Score  |  |
                              |  |  Skope-Rules)|  | (BERT, ViT)      |  |
                              |  +--------------+  +------------------+  |
                              +--------------------+---------------------+
                                                   |
                    +------------------------------+------------------------------+
                    v                              v                              v
         +------------------+         +------------------+         +------------------+
         |   Developer      |         | Domain Expert    |         |  End User/       |
         | (Debug, Audit)   |         | (Doctor, Loan    |         |  Regulator       |
         |                  |         |  Officer, Judge) |         |  (GDPR/AI Act)   |
         +------------------+         +------------------+         +------------------+
```

**왜 지금 XAI가 필수인가 (Old vs New Paradigm 비교)**

| 차원 | 전통 통계학습 (1990-2012) | 현대 AI (2012-현재) |
| :--- | :--- | :--- |
| **모델 복잡도** | 수십~수백 파라미터 (로지스틱 회귀, 얕은 트리) | 수십억~수조 파라미터 (GPT-4, PaLM, GPT-5) |
| **표현 방식** | 사람이 읽을 수 있는 계수/규칙 | 고차원 임베딩, 분산 표현, Attention 가중치 |
| **설명 가능성** | 본질적(Intrinsic) — 결정 규칙 자체가 설명 | 사후(Post-hoc) — 별도 알고리즘으로 역추론 |
| **규제 환경** | FCRA, ECOA, GDPR 사전 단계 | EU AI Act, NIST AI RMF, ISO/IEC 42001, 한국 AI 기본법(2024.12) |
| **위험 인식** | "왜 틀렸는가" 디버깅 수준 | 의료 오진, 채용 차별, 자율주행 사고, 금융 차별 — **생명·권리·재산** 직결 |
| **데이터** | 정형(Structured), 소규모 | 비정형(이미지·텍스트·음성·비디오), 대규모 |

특히 **EU AI Act(2024.08 발효, 2026.08 전면시행)**는 신용평가·채용·법집행·생체인식·의료기기 등 4단계 위험 등급 중 **고위험(High-Risk) AI 시스템**에 대해 (a) 인간 감독(Human Oversight) (b) 투명성·설명 의무 (c) 기술 문서화 (d) 데이터 거버넌스를 의무화하고, 위반 시 매출의 7%(최대 €35M) 과징금을 부과한다. 한국의 **AI 기본법(2024.12.26 시행)**도 고영향 AI(신용·채용·의료·법률)에 대해 (1) 설명 제공 권리 (2) 거버넌스 체계 구축 (3) 영향평가 실시를 핵심 골자로 한다.

- **📢 섹션 요약 비유**: 기존 자동차는 엔진룸을 열어보면 어디 부품이 어떻게 돌아가는지 보였지만, 현대 자율주행 전기차는 외관만 보고는 "왜 갑자기 브레이크를 밟았는지" 알 수 없습니다. XAI는 이 자율주행차에 **"블랙박스 + 실시간 사고 다이어그램"**을 함께 장착하는 기술이며, 단순 기록을 넘어 "브레이크 밟음: 앞 차량 충돌 예측 97%, 보행자 인식 점수 0.94" 같은 **판단 근거 로그**를 운전자와 보험사·규제자에게 제공하는 일입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

XAI 시스템은 **①대상 모델(Black/White-box)**, **②설명 생성 모듈(Explanation Generator)**, **③평가 모듈(Evaluation Harness)**, **④인간 인터페이스(Human-Computer Explanation Interface)**의 4계층으로 구성된다. 각 계층은 독립적으로 진화 가능하며, MLOps 파이프라인 상에서 **학습(Training) -> 검증(Validation) -> 배포(Deployment) -> 모니터링(Monitoring)** 전체 단계에 통합된다.

```text
[ XAI 시스템 아키텍처 및 데이터 흐름 ]

  +-------------------------------------------------------------------------+
  |                       Layer 1: Target Model                            |
  |  +--------------+  +--------------+  +--------------+  +-------------+ |
  |  | Black-Box    |  | Black-Box    |  | White-Box    |  | Hybrid      | |
  |  | Deep         |  | Ensemble     |  | Linear/Tree  |  | Concept     | |
  |  | (ResNet,     |  | (XGBoost,    |  | (Logistic,   |  | Bottleneck  | |
  |  |  BERT, GPT)  |  |  LightGBM)   |  |  CART, GAM)  |  | Network     | |
  |  +------+-------+  +------+-------+  +------+-------+  +------+------+ |
  |         +------------------+------------------+------------------+     |
  |                                    |                                     |
  |                                    v (Inference API)                     |
  |                          +----------------------+                       |
  |                          | f(x) -> ŷ, logit, p   |                       |
  |                          | (Prediction + Score)  |                       |
  |                          +----------+-----------+                       |
  +-------------------------------------+-----------------------------------+
                                        |
  +-------------------------------------+-----------------------------------+
  |                       Layer 2: Explanation Generator                    |
  |                                     v                                     |
  |  +------------------------------------------------------------------+    |
  |  |  A. Feature Attribution Methods (Local + Quantitative)          |    |
  |  |     +- SHAP (Tree/Deep/Gradient/Kernel)  — Shapley Value      |    |
  |  |     +- LIME (Tabular/Text/Image)         — Local Surrogate    |    |
  |  |     +- Integrated Gradients             — Axiomatic Baseline  |    |
  |  |     +- LRP (Layer-wise Relevance Prop.) — DNN-specific        |    |
  |  |     +- Input × Gradient, Occlusion, Permutation Importance    |    |
  |  +------------------------------------------------------------------+    |
  |  +------------------------------------------------------------------+    |
  |  |  B. Saliency / Visualization Methods (Image/CV Domain)          |    |
  |  |     +- Grad-CAM, Grad-CAM++           — Class Activation Map  |    |
  |  |     +- Score-CAM, Eigen-CAM           — Perturbation-free     |    |
  |  |     +- Saliency Maps, SmoothGrad      — Noise-augmented       |    |
  |  +------------------------------------------------------------------+    |
  |  +------------------------------------------------------------------+    |
  |  |  C. Concept & Prototype Methods (Semantic-Level)                |    |
  |  |     +- TCAV (Testing w/ Concept Activation Vectors)            |    |
  |  |     +- Concept Bottleneck Models (CBM, Label-free CBM)         |    |
  |  |     +- ProtoPNet, Deformable ProtoPNet                         |    |
  |  +------------------------------------------------------------------+    |
  |  +------------------------------------------------------------------+    |
  |  |  D. Example & Counterfactual Methods (Instance-Based)           |    |
  |  |     +- Counterfactuals: DiCE, Wachter-MCF, Alibi               |    |
  |  |     +- Anchors (High-Precision Rules)                          |    |
  |  |     +- Influential Instances: Influence Functions, TracIn     |    |
  |  |     +- k-NN Retrieval from Latent Space (RAG-style)            |    |
  |  +------------------------------------------------------------------+    |
  |  +------------------------------------------------------------------+    |
  |  |  E. Attention & Token-Level (NLP/LLM)                           |    |
  |  |     +- Attention Rollout, Attention Flow                       |    |
  |  |     +- BERTViz, exBERT, Transformer Explanation                |    |
  |  |     +- LLM Self-Explanation (Chain-of-Thought, ReAct)          |    |
  |  +------------------------------------------------------------------+    |
  +-------------------------------------+-----------------------------------+
                                        |
                                        v
  +-------------------------------------------------------------------------+
  |              Layer 3: Evaluation Harness (Faithfulness Checks)         |
  |  +--------------------+  +--------------------+  +-----------------+   |
  |  | Faithfulness       |  | Robustness         |  | Comprehensibility|  |
  |  | - Sufficiency      |  | - Max-Sensitivity  |  | - User Studies  |   |
  |  | - Necessity        |  | - Stability Index  |  | - Cognitive Load|   |
  |  | - Monotonicity     |  | - Adversarial      |  | - Time-to-Task  |   |
  |  | - Infidelity       |  |   Perturbation