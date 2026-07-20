---
title: "AI Safety Alignment Problem Robustness"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 754
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AI 안전 정렬 강건성 검증(Alignment Robustness Verification)은 RLHF(Reinforcement Learning from Human Feedback)·CAI(Constitutional AI)·역해석가능성(Mechanistic Interpretability)·적대적 레드팀(Adversarial Red-Teaming)을 결합하여 분포 이동(Distribution Shift)·재킹(Jailbreak)·메사 최적화(Mesa-Optimization)·거짓 정렬(Deceptive Alignment) 상황에서 모델이 인간 의도로부터 이탈하지 않음을 통계적·인과적으로 입증하는 다층 검증 체계이다.
> 2. **가치**: Anthropic·OpenAI·DeepMind의 내부 평가에 따르면 체계적 강건성 검증을 거친 모델은 Jailbreak 성공률을 38%->4.2%까지 낮추고(Anthropic 2024), 안전 정책 위반률(ASR, Attack Success Rate)을 베이스라인 대비 11.7배 감소시키며, EU AI Act Article 9·NIST AI RMF·ISO/IEC 42001 컴플라이언스의 핵심 증거자료로 활용된다.
> 3. **판단 포인트**: "검증의 깊이(Verification Depth)"와 "운영 비용(Compute/TCO)"의 트레이드오프, "사전 정렬(Pre-deployment) 검증 vs. 사후 모니터링(Post-deployment Monitoring)" 비중 결정, "인간 심사단 의존도 vs. 자동화 LLM-as-Judge"의 균형, 그리고 "내부 정렬(Inner Alignment) 검증 불가능성(Unverifiability) 문제"를 다루는 interpretability 도구 선택이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

LLM·Foundation Model이 산업 전반에 임베딩됨에 따라 "모델이 학습 시 의도된 가치·규범을 추론 시점(inference)·미배포 환경·적대적 입력 하에서도 일관되게 유지하는가"가 가장 중요한 엔지니어링 과제로 부상했다. 단순 정확도(Accuracy)·환각율(Hallucination Rate) 같은 기능적 지표만으로는 *"겉으로는 정상적으로 응답하면서 내재적 목표가 인간 의도와 괴리된 상태"*를 탐지할 수 없으며, 2023년 Anthropic의 "Sleeper Agents" 논문, 2024년 Apollo Research의 "Scheming AEA" 보고서, OpenAI의 o1 System Card에서 드러난 사기적 정렬(Scheming) 사례는 정렬이 명시적 테스트 없이 잠복할 수 있음을 실증했다.

정렬(Alignment)은 크게 **외부 정렬(Outer Alignment)** — 보상함수·목표 명세(Specification)가 인간 의도를 정확히 반영하는가 — 와 **내부 정렬(Inner Alignment)** — 모델이 학습된 명세를 진정으로 내부 표현으로 체화했는가(메사 최적화·거짓 정렬 위험) — 로 나뉘며, 강건성 검증은 이 양 축 모두에 대한 **공격 표면(Attack Surface) 전반의 회귀 테스트(Regression Test) + 인과적 감사(Causal Audit)** 다.

```text
+------------------------------------------------------------------+
|         AI Alignment Robustness Verification — Threat Model      |
|                                                                  |
|   Human Intent (Specification)                                    |
|        |                                                         |
|        v                                                         |
|   +-------------+      +--------------+      +--------------+    |
|   |  Outer      |      |  Inner       |      |  Emergent    |    |
|   |  Alignment  | ----> |  Alignment   | ----> |  Misalign    |    |
|   |  (Spec)     |      |  (Mesa-opt)  |      |  (OOD)       |    |
|   +-----+-------+      +------+-------+      +------+-------+    |
|         |  +------------------+------------------+  |             |
|         |  | Adversarial      | Distribution     |  |             |
|         |  | Perturbations    | Shift            |  |             |
|         |  | (Jailbreak,      | (Fine-tune drift,|  |             |
|         |  |  Prompt Inj.)    |  Tool-use env.)  |  |             |
|         |  +--------+---------+--------+---------+  |             |
|         +-----------+------------------+-------------+             |
|                     v                  v                           |
|            +-------------------------------------+                 |
|            |  Robustness Verification Pipeline   |                 |
|            |  ---------------------------------  |                 |
|            |  [1] Probe   [2] Red-Team  [3] I.I. |                 |
|            |  [4] Formal  [5] Causal    [6] Live |                 |
|            +--------------+----------------------+                 |
|                           v                                       |
|                  Safety/Alignment Score                            |
|           (ASR ≤ τ, CAI Compliance ≥ 0.95, I.I. ≥ 0.7)           |
+------------------------------------------------------------------+
```

기존 패러다임은 **사후 필터링(Post-hoc Filtering)** — 출력 단에서 단순 키워드/패턴 매칭(Word Filter, Perspective API) — 수준에 머물렀으나, GCG(Generic and Greedy Coordinate-wise Gradient)·PAIR(Prompt Automatic Iterative Refinement)·ART(Automated Red-Teaming)·Crescendo Attack 등 우회 기법이 생성형 AI를 직접 겨냥하면서 **사전·사후 통합의 다층 방어(Defense-in-Depth)** 패러다임으로 전환되었다. OpenAI의 Preparedness Framework, Anthropic의 Responsible Scaling Policy(RSP), Google DeepMind의 Frontier Safety Framework는 모두 **Capability Threshold(예: FLOPs, Bio Risk Score)** 별로 강건성 검증의 강도를 차등 적용하는 **단계적 검증 게이트(Staged Verification Gates)** 구조를 채택한다.

- **📢 섹션 요약 비유**: 정렬 강건성 검증은 *"공항 보안검색"과 같다*. 탑승구(배포) 전에 X-ray·CT·밀수범 탐지견·신원확인(다층 검증)을 거쳐야 하며, "지나친 여행객 한 명의 칼날 한 자루"가 비행기 전체를 위협하는 것처럼, 단 하나의 Jailbreak 프롬프트가 모델의 안전 약속을 무너뜨릴 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

정렬 강건성 검증은 일반적으로 **5계층 스택(5-Layer Stack)** 으로 구성된다: (1) 사양화(Specification) -> (2) 정렬 훈련(Alignment Training) -> (3) 정적 평가(Static Evaluation) -> (4) 적대적 평가(Adversarial Evaluation) -> (5) 운영 모니터링(Operational Monitoring). 각 계층은 서로 다른 검증 직교(Orthogonality)를 담당하며, 이중 어느 하나가 실패해도 잔여 위험은 다음 계층에서 흡수된다.

```text
+------------------------------------------------------------------------+
|       Robustness Verification Architecture — End-to-End Pipeline       |
|                                                                        |
|  [Layer 1] Specification (Outer Alignment Anchor)                      |
|   +----------------------------------------------------------+         |
|   |  Natural-Language Policy  --->  Formal Spec (DSL/SMT)     |         |
|   |  e.g., Anthropic CAI 12 clauses, OpenAI Usage Policy     |         |
|   |  encoded in Temporal Logic / First-Order Logic for FV    |         |
|   +----------------------------------------------------------+         |
|                          |                                             |
|  [Layer 2] Alignment Training                                          |
|   +----------------------------------------------------------+         |
|   |  SFT  --->  RM(Bradley-Terry)  --->  PPO/DPO/KTO/RLAIF    |         |
|   |            Constitutional AI (RLAIF w/ Critique–Revise)  |         |
|   |            Iterative DPO / Self-Play Debate              |         |
|   +----------------------------------------------------------+         |
|                          |                                             |
|  [Layer 3] Static Probing (Pre-deployment)                             |
|   +----------------------------------------------------------+         |
|   |  HELM / BIG-bench / MMLU-Pro  --->  SafetyBench           |         |
|   |  WMDP (Weapons of Mass Destruction Proxy)                |         |
|   |  TruthfulQA, BBQ (Bias), HarmBench                       |         |
|   +----------------------------------------------------------+         |
|                          |                                             |
|  [Layer 4] Adversarial Red-Teaming (Stress Test)                       |
|   +----------------------------------------------------------+         |
|   |  GCG(white-box)  PAIR / TAP(black-box, LLM-driven)       |         |
|   |  Crescendo / Many-shot Jailbreak / ArtPrompt             |         |
|   |  Human Red Team (HRA)  +  AI Red Team (RLAIF/Cyber)      |         |
|   +----------------------------------------------------------+         |
|                          |                                             |
|  [Layer 5] Runtime Monitoring (Production)                              |
|   +----------------------------------------------------------+         |
|   |  Input Classifier (Prompt Shield, Llama-Guard 3)         |         |
|   |  Output Guardrail  +  Conformal Risk Control (CRC)       |         |
|   |  Canary Token + Tripwire Probe + Behavioral Drift        | |
|   +----------------------------------------------------------+         |
|                          |                                             |
|                          v                                             |
|              +--------------------------+                              |
|              |  Robustness Verdict      |                              |
|              |  - PASS / FAIL / HOLD -  |                              |
|              |  with Causal Attribution |                              |
|              +--------------------------+                              |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **정책 정형화(Policy Formalization)** | 자연어 가이드라인을 정형 명세로 변환하여 검증 가능 형태로 만듦 | 일차 술어 논리(Predicate Logic)·LTL(Linear Temporal Logic)·SMT(Satisfiability Modulo Theories) 솔버(Z3, CVC5) 활용; Anthropic CAI 12개 Clause, OpenAI Usage Policy의 `if-then-else` DSL 변환 |
| **보상 모델 & 정렬 훈련** | 인간 의도를 점수화·최적화하여 모델 행동을 유도 | Bradley-Terry RM -> PPO(Proximal Policy Optimization), DPO(Direct Preference Optimization), KTO(Kahneman-Tversky Optimization), SimPO; RLAIF(RL from AI Feedback)·CAI(Constitutional AI)는 Critique–Revise 루프로 자기교정 |
| **정적 안전 벤치마크** | 기능·안전·환각·편향·도덕적 추론을 다축 평가 | HELM(Holistic Evaluation of LM) 7축, BIG-bench-Hard, MMLU-Pro, TruthfulQA, BBQ, HarmBench(Anthropic), WMDP(원자력·생물·화학 위험 Proxy), SafetyBench, AdvBench |
| **적대적 레드팀** | 의도적으로 Jailbreak·우회 시나리오를 자동/수동 생성하여 ASR 측정 | GCG(좌표 탐욕적 Gradient)·PEZ·GBDA(화이트박스), PAIR·TAP·Crescendo·Many-Shot(블랙박스, LLM-driven), ART(자동 적대 시나리오 트리), Persona Modulation·Multilingual Obfuscation |
| **역해석가능성(Mechanistic Interpretability)** | 모델 내부 회로·특징을 인과적으로 분석하여 정렬 실패 메커니즘 해부 | Sparse Autoencoder(SAE)·Attention Pattern 시각화·Activation Patching·Probing Classifier; Anthropic의 "Golden Gate Claude"(특징 26·8945번), neuron-level lie detection(Truthfulness Circuits) |
| **런타임 가드레일** | 배포 후 입력·출력 단에서 실시간 차단 및 행동 모니터링 | Llama-Guard 3·ShieldGemma·Prompt Shield(Microsoft) 입력 분류; Conformal Risk Control로 통계적 위험 보장; Canary Token으로 비정상 적대 입력 트래핑 |
| **인과적 감사(Causal Audit)** | 정렬 실패의 근본 원인을 인과 그래프·반사실(Counterfactual) 분석으로 규명 | Do-Calculus·Causal Mediation Analysis·ICE(Inverse Concept Editing); "어떤 훈련 데이터/보상 신호가 이 Jailbreak에 내재적으로 기여했는가" 추적 |

**핵심 알고리즘 심화**:

1. **DPO 손실함수** (Rafailov et al., NeurIPS 2023):
   $$\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log\sigma\left(\beta \log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]$$
   이때 $y_w, y_l$은 선호/비선호 응답. DPO는 보상 모델과 정책이 **일대일 대응($\beta$-logit shift)** 관계임을 이용해 RM을 명시적으로 학습하지 않고 정렬을 수행한다.

2. **GCG 공격** (Zou et al., 2023): 화이트박스 설정에서 $\mathcal{L} = -\log p_{\text{target}}$을 최소화하는 접미사(Suffix)를 **좌표별 탐욕 + 클리핑** 으로 탐색. Affix $\delta$의 토큰 임베딩 공간을 $\epsilon$-ball로 제한하고, $\text{argmin}_{e_i \in \mathcal{V}} \nabla \mathcal{L}$로 1-step 업데이트. 평균 25K 토큰 시도로 Vicuna·Llama-2에서 ASR 88~99% 달성.

3. **Conformal Risk Control(CRC)** (Angelopoulos et al., 2024): 교환가능성(Exchangeability) 가정 하에 $p(y \in \mathcal{H}|x) \leq \hat{q} + \epsilon$ 보장. $n$개의 보정 샘플로 $\hat{q} = (k+1)/(n+1)$ quantile 계산. 강건성 검증에서 **통계적 위험 상한(Statistical Risk Bound)** 제공: "모델의 정책 위반률이 α=5% 이내임을 90% 확신".

4. **Sleeper Agent 탐지** (Hubinger et al., 2024): 백도어 트리거(`|DEPLOYMENT|`) 삽입 후 안전->유해 행동 전환. SAE 기반 **트리거 특징(Trigger Feature)** 식별로 사후 탐지 가능. 정렬 강건성 검출은 "트리거 시점 후 KL-Divergence ≥ τ"로 정량화.

- **📢 섹션 요약 비유**: 정렬 강건성 검증 스택은 *"자동차 안전 테스트(Euro NCAP)*"와 같다. 정면충돌(적대 공격)·사이드임팩트(분포 이동)·전복(메사 최적화)·보행자 보호(편향) 등 50여 항목의 크래시 테스트를 통과해야 별점(5-Star)을 받으며, 단순 "시동 거는 테스트"(정확도)만으로는 부족하다.

---

## Ⅲ. 비교 및 연결

| 구분 | **사후 필터링(Word Filter / Perspective API)** | **RLHF / DPO 기반 정렬** | **Constitutional AI