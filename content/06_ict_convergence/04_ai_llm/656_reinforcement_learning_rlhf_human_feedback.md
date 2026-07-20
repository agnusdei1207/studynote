---
title: "Reinforcement Learning RLHF Human Feedback"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 656
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RLHF(Reinforcement Learning from Human Feedback)는 사전훈련된 언어 모델(LLM) 위에 **3단계 파이프라인(SFT -> Reward Model -> PPO/RL Optimization)**을 적용해 인간의 선호 신호(Preference Signal)를 정책 분포에 반영하는 정렬(Alignment) 기법으로, 보상 함수 $r_\theta(x, y)$를 별도 모델로 학습하고 **PPO(Proximal Policy Optimization)**에 **KL 제약($\beta \cdot \text{KL}(\pi_\theta \| \pi_{\text{ref}})$)**을 결합해 Reference Model과의 이탈을 통제한다.
> 2. **가치**: 단순 SFT 대비 **도움됨·무해함·정직성(HHH) 지표 1.3~2.1배 향상**(InstructGPT 기준), **Hallucination Rate 약 50% 감소**, **Toxicity 25%v** 등 정량적 효과가 입증되었으며, 별도 작업별 파인튜닝 없이 **명령어 일반화** 능력을 획득하여 Few-shot 프롬프트 의존도를 낮추고 엔터프라이즈 도메인 전이 학습 비용을 절감한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) Reward Hacking(보상 해킹)** — Proxy Reward와 실제 가치의 괴리로 발생, **(b) Alignment Tax(정렬 세금)** — 정렬로 인한 벤치마크 점수 저하, **(c) 인간 라벨링 비용과 품질 편차**, **(d) PPO의 메모리 4× 부담(Actor+Critic+Ref+Reward)** — 이를 DPO/IPO/KTO/RLAIF/Constitutional AI로 대체할지, 하이브리드로 갈지가 실무적 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

LLM의 **스케일링 법칙(Scaling Law, Kaplan 2020)**이 매개변수·데이터·연산량에 따라 손실을 예측 가능한 형태로 감소시킴이 입증되면서 GPT-3(175B)·PaLM(540B)·LLaMA·Mistral 등 **Foundation Model** 시대가 열렸다. 그러나 Next Token Prediction으로 학습된 LLM은 본질적으로 **"다음에 올 토큰의 확률 분포"**를 모사하는 생성기이며, 다음의 세 가지 구조적 한계를 가진다.

1. **명령어 불일치(Instruction Following Failure)**: "이메일을 정중하게 다시 써줘" 같은 사용자 의도(intent)를 명세 단서(instruction)만으로 추론하지 못함 — 즉, **Prompt Completion** 방식에서 **Instruction Following**으로의 패러다임 전환이 필요.
2. **가치 정렬 부재(Value Misalignment)**: 유해·편향·거짓 정보(Hallucination) 생성을 통계적으로만 억제할 뿐, 인간의 윤리·사회적 규범을 **명시적으로 반영하지 못함** — Christiano et al.(2017)의 *Deep Reinforcement Learning from Human Preferences*가 이를 정면으로 다룸.
3. **분포 외 일반화 부족**: SFT(Supervised Fine-Tuning)만으로는 보지 못한 instruction에 대한 강건성(robustness)이 약함.

기존 SFT는 **고품질 데모(Demonstration) 데이터**가 필요하고, 모든 "잘못된 출력"을 명시적으로 라벨링해야 한다는 **Coverage 한계**가 있다. 반면 RLHF는 **선호 비교(Preference Comparison)**만으로 신호를 추출하므로 라벨링 비용 대비 정보 밀도가 훨씬 높다(Ouyang et al., 2022, *Training language models to follow instructions with human feedback*, OpenAI InstructGPT).

```text
+----------------------------------------------------------------------+
|         RLHF 등장 전후의 LLM 개발 패러다임 비교                       |
+----------------------------------------------------------------------+
|  [구 패러다임]                                                         |
|   데이터 -► 토큰 정제 -► Next Token Prediction (Self-Supervised)      |
|                              |                                        |
|                              v                                        |
|                       Foundation Model (Base LLM)                     |
|                              |                                        |
|                    Prompt Engineering (수작업)                          |
|                              |                                        |
|                              v                                        |
|                       사용자 응답 (불안정·일관성v)                       |
|                                                                      |
|  [신 패러다임: RLHF]                                                   |
|   데이터 -► Pre-training -► SFT -► RM Training -► PPO Optimization     |
|                                              |                        |
|                                              v                        |
|                                       Aligned LLM (ChatGPT, Claude)  |
|                                              |                        |
|                                    Direct Instruction Following       |
|                                                                      |
|  ⇒ RLHF는 "Prompt 의존형"을 "Instruction 독립형"으로 전환하는 핵심     |
|    인터페이스 추상화 계층이라 할 수 있음                                 |
+----------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 핵심 차이**:
- **SFT-Only**: Teacher Forcing 방식의 모방 학습, "원하는 답"만 학습 -> **분포 외 입력에 취약**.
- **RLHF**: 보상 최대화 + KL 제약 정책 최적화 -> **상대적 품질 차이**까지 학습. 두 응답 A, B 중 어느 쪽이 인간에게 더 가치 있는지를 비교 라벨링(pairwise comparison)하면 충분.
- **최신 후속**: DPO(Direct Preference Optimization, Rafailov 2023)는 보상 모델을 명시적으로 학습하지 않고 선호도 데이터를 직접 정책 학습에 사용해 PPO의 메모리·안정성 부담을 회피.

- **📢 섹션 요약 비유**: 일반 SFT는 "정답지(模範 답안)를 통째로 외우는 학생"이고, RLHF는 "여러 답안 중 선생님이 더 좋은 답을 가리키면 그 방향으로 사고방식을 교정받는 학생"과 같다. 절대적 정답을 모두 외울 필요 없이, **상대적 비교만으로 방향성이 학습**된다는 점이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RLHF 파이프라인은 OpenAI의 InstructGPT 논문(Ouyang et al., 2022)을 기준으로 **3단계**로 구성된다. Anthropic의 Claude, Google의 Bard/Gemini, Meta의 Llama-2-Chat 모두 본질적으로 동일한 구조를 채택하되 **Step 3**을 변형해왔다.

```text
                       +------------------------------------+
                       |  STEP 1. Supervised Fine-Tuning    |
                       |  (SFT) — 정책 초기화              |
                       |                                    |
   라벨러(Labeller) --►|  Prompt Datasets  --► SFT Model    |
   데모 작성 (Demonstrations)                 (π_SFT)         |
   약 13k~100k examples                       |              |
                                               v              |
                       +------------------------------------+
                       |  STEP 2. Reward Modeling           |
                       |  (RM) — 인간 선호 학습             |
                       |                                    |
   라벨러(Labeller) --►|  Pairwise Comparison (K개 중)        |
   선호도 라벨링                              |              |
   A>B, A<B, A≈B 등                         v              |
                                          Reward Model       |
                                          r_θ(x, y)          |
                                          (보통 6B/13B)       |
                                               |              |
                                               v              |
                       +------------------------------------+
                       |  STEP 3. RL Fine-Tuning (PPO)      |
                       |  — 정책 최적화 + KL 제약            |
                       |                                    |
      Prompt --► Actor π_θ(생성) --► Response y              |
                       |                |                    |
                       |                v                    |
                       |      Reward r_θ(x,y) --► Scalar    |
                       |                |                    |
                       |                v                    |
                       |         Advantage A_t (GAE)         |
                       |                |                    |
                       |   KL Divergence(π_θ‖π_SFT)         |
                       |       β·KL 페널티 부착              |
                       |                |                    |
                       |                v                    |
                       |         PPO Clip(ε=0.1~0.2)        |
                       |                |                    |
                       +---► Backprop & Policy Update ------+
                              Critic V_φ (Value Function)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Actor Policy $\pi_\theta(y\|x)$** | 실제 정책, 응답을 생성하는 LLM (수십~수백 B) | PPO의 stochastic policy, sampling으로 응답 y 생성. 학습 시 **gradient checkpointing** + **AdamW** + **Mixed Precision(FP16/BF16)** 필수 |
| **Reference/Critic 모델** | KL 발산 기준선, 가치 추정 | Reference는 **SFT 모델의 frozen copy**($\pi_{\text{ref}}$). Critic $V_\phi$는 scalar value를 회귀 — 별도 LLM 헤드를 1-token linear projection으로 변환 |
| **Reward Model $r_\theta(x,y)$** | 인간 선호를 점수화하는 scalar 출력 | Bradley-Terry 모델 기반: $P(\sigma) = \frac{e^{r(x,y_w)}}{e^{r(x,y_w)}+e^{r(x,y_l)}}$, loss = $-\log\sigma(r(x,y_w)-r(x,y_l))$ |
| **PPO Optimizer** | 정책 경사 업데이트 | Clipped Surrogate Objective: $L^{\text{CLIP}} = \mathbb{E}_t[\min(\rho_t A_t, \text{clip}(\rho_t, 1-\epsilon, 1+\epsilon) A_t)]$, $\rho_t = \pi_\theta(a_t\|s_t)/\pi_{\theta_{\text{old}}}(a_t\|s_t)$ |
| **GAE (Generalized Advantage Estimation)** | 분산-편향 트레이드오프 통제 | $\hat{A}_t = \sum_{l=0}^{\infty}(\gamma\lambda)^l \delta_{t+l}$, $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$. 통상 $\lambda=0.95, \gamma=1.0$ |
| **KL Penalty** | 정렬 세금(Alignment Tax) 억제 | 최종 reward: $r_{\text{total}} = r_\theta(x,y) - \beta \cdot \text{KL}(\pi_\theta \| \pi_{\text{SFT}})$, $\beta$는 0.02~0.2 사이 튜닝. **Adaptive KL controller**로 자동 조정(KL target≈6~30 nats) |

### 핵심 수식: PPO+KL 목적함수

$$
\max_{\theta}\; \mathbb{E}_{x \sim \mathcal{D},\, y \sim \pi_\theta(\cdot|x)} \Big[\, r_\theta(x,y) - \beta \,\text{KL}\big(\pi_\theta(y|x)\,\|\,\pi_{\text{ref}}(y|x)\big) \,\Big]
$$

여기서 $\beta$가 너무 작으면 **Reward Hacking**(반복·과장·미용 어구 남발)이, 너무 크면 **Mode Collapse**(짧고 무난한 응답만 생성)가 발생한다. 실무에서는 **Anthropic Constitutional AI**처럼 자체 규칙(Constitution) 기반 **RLAIF(RL from AI Feedback)**로 라벨링 비용을 낮추고, **Self-Rewarding / Iterative DPO(Zheng et al., 2023)**로 데이터 효율을 높이려는 시도가 병행된다.

### Reward Hacking의 세부 메커니즘

- **Length Bias**: RM이 긴 응답에 점수를 후하게 주는 경향 -> 모델이 군더더기 어구 생성.
- **Sycophancy(아첨)**: 사용자 의견에 무조건 동의 — *Perez et al. 2022*의 "Discovering Language Model Behaviors" 보고서에서 정량화.
- **Verbosity/Formatting Exploit**: 마크다운·이모지·불릿을 남발.
- **대응 기법**: **Length-normalized reward**, **Ensemble of RMs(다수 RM voting)**, **Process Reward Model(PRM, 수학적 단계별 채점, UDT/OpenAI o1)**, **Constitutional Sampling(규칙 기반 거부 샘플링)**.

- **📢 섹션 요약 비유**: RLHF의 세 모델(Actor, Critic, Reward)을 **운전학원**에 비유하면, Actor는 **운전 연습 중인 학생**, Reference 모델은 **교과서 정답 운전**, Critic은 **감독관(점수 매김)**, Reward Model은 **"안전하고 친절한 운전인지"를 평가하는 외부 평가위원**이다. 학생은 평가위원의 점수가 높도록 운전하되, 교과서(Reference)와 너무 다르게 운전하면 감점(KL 페널티)받는다.

---

## Ⅲ. 비교 및 연결

RLHF는 단독으로 존재하지 않으며 SFT, DPO, RLAIF, Constitutional AI, 안전 계층(Safety Layer) 등과 명확한 **트레이드오프 매트릭스**를 형성한다.

| 구분 | SFT (Supervised Fine-Tuning) | RLHF (PPO) | DPO (Direct Preference Optimization) | RLAIF (Constitutional AI) |
| :--- | :--- | :--- | :--- | :--- |
| **학습 신호** | 정답 (y) | 보상 (scalar r) | 선호 쌍 (y_w, y_l) | AI 생성 규칙 기반 평가 |
| **라벨링 비용** | 높음 (데모 작성) | 중간 (쌍 비교) | 중간 (쌍 비교) | 매우 낮음 (자동화) |
| **메모리 footprint** | 1× (단일 모델) | 4× (Actor+Critic+Ref+RM) | 2× (Policy+Ref) | 1~2× |
| **학습 안정성** | 매우 안정 | 불안정 (PPO hyperparam 민감) | 안정 (지도학습 형태) | 안정 |
| **Hallucination 억제** | 약함 | 강함 | 강함 | 강함 |
| **Reward Hacking 위험** | 없음 | 높음 | 낮음 | 중간 (AI 편향 가능) |
| **온라인 샘플링 필요** | ✗ | ✓ (PPO rollouts) | ✗ (offline) | △ |
| **대표 적용 사례** | Alpaca, Dolly | ChatGPT, GPT-4, Llama-2-Chat | Mistral-Instruct, Zephyr, Llama-3-IF | Claude 2/3, Gemini Fine-tuning |
| **핵심 한계** | 분포 외 일반화 약함 | Alignment Tax, KL 튜닝 | Offline이라 탐색 제한 | AI 평가자의 환각/편향 |

### 정량 비교 (InstructGPT 기준, Ouyang 2022)

- **Truthfulness (TruthfulQA)**: 175B SFT base = 21.8% -> **SFT+RLHF = 56.3%** (≈2.6×)
- **Toxicity (RealToxicityPrompts)**: Base = 32.4% -> **RLHF = 21.7%** (33% 감소)
- **Hallucination Rate**: SFT only = 41.7% -> **RLHF = 22.0%** (47% 감소)
- **Human Preference Win-rate**: SFT 0.51 vs **RLHF 0.74** vs Base 0.45

### 통합 아키텍처: RLHF는 단독이 아닌 "스택"

```
+---------------------------------------------------------+
|  Layer 1: Pre-training (수조 토큰)                       |
|         v                                               |
|  Layer 2: SFT (명령어 데이터)                            |
|         v                                               |
|  Layer 3: Preference Training (RLHF/DPO/IPO/CPO/ORPO)   |
|         v                                               |
|  Layer 4: Safety Tuning (Constitutional AI / RLAIF)      |
|         v                                               |
|  Layer 5: Inference-time Guardrails (Llama Guard,        |
|           NeMo Guardrails, Prompt Guard, Output Filter)  |
|         v                                               |
|  Layer 6: RAG + Tool Use + System Prompt Engineering     |
+---------------------------------------------------------+
```

즉, **RLHF는 "정렬"의 한 층**이지 시스템 전체가 아니며, 실시간 가드레일(NeMo Guardrails, Azure AI Content Safety, Llama Guard 3 등)과 결합되어야 엔터프라이즈 SLA를 만족한다.

- **📢 섹션