---
title: "RLHF (Reinforcement Learning from Human Feedback)"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 337
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RLHF (Reinforcement Learning from Human Feedback) 는 사전 학습된 LLM (Large Language Model) 이 "사람이 선호하는 응답"을 생성하도록 유도하는 3단계 파이프라인으로, SFT (Supervised Fine-Tuning) -> 보상 모델 (Reward Model) 학습 -> PPO (Proximal Policy Optimization) 강화학습 순으로 진행된다.
> 2. **가치**: 언어 모델의 유해성 감소, 사실성 향상, 지시 따르기 (Instruction Following) 능력 향상을 동시에 달성해 ChatGPT, Claude, Gemini 의 공통 핵심 기술이 됐다.
> 3. **판단 포인트**: PPO 는 정책 업데이트 폭을 클리핑 (Clipping) 으로 제한해 안정성을 확보하고, KL 패널티로 SFT 모델과 지나치게 멀어지는 것을 방지한다는 이중 안전장치를 반드시 서술해야 한다.

---

## Ⅰ. 개요 및 필요성

### 정렬 (Alignment) 문제란?

GPT 류 모델은 다음 토큰 예측 (Next Token Prediction) 으로 사전 학습되어 "그럴듯한 문장 완성"에는 탁월하지만, "도움이 되고, 해롭지 않고, 정직한 (HHH, Helpful·Harmless·Honest)" 응답을 보장하지 않는다. 이 불일치를 **정렬 문제 (Alignment Problem)** 라 한다.

| 문제 유형 | 예시 | RLHF 해결 방식 |
|:---|:---|:---|
| 유해 콘텐츠 | 위험 물질 제조법 제공 | 보상 모델이 낮은 점수 부여 |
| 환각 (Hallucination) | 없는 논문 인용 | 정확한 응답 선호 학습 |
| 지시 무시 | "3줄 요약" 을 20줄 출력 | 형식 준수 응답 선호 |
| 지나친 동의 | 틀린 전제에 동조 | 사실 기반 반박 학습 |

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: RLHF 없는 LLM 은 "박학다식하지만 눈치 없는 천재"다. 질문에 뭐든 대답하지만, 상황과 예의를 모른다. RLHF 는 이 천재에게 "사회 교육"을 시키는 과정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### RLHF 3단계 파이프라인

```
  +--------------------------------------------------------------+
  |                   RLHF 전체 파이프라인                       |
  +--------------+------------------+----------------------------+
  |  [Step 1]    |    [Step 2]      |       [Step 3]             |
  |  SFT 지도    |  Reward Model    |     PPO 강화학습            |
  |  미세조정    |  학습            |                            |
  +--------------+------------------+----------------------------+
  | 사전학습 LLM | 동일 프롬프트에  |  SFT 모델 = 초기 정책      |
  |    +         | 2개 응답 생성    |  보상 모델로 점수 계산      |
  | 인간 작성    | 사람이 선호 선택 |  PPO 로 정책 업데이트       |
  | 예시 대화    | 순위 학습        |  KL 패널티 적용             |
  |    v         |      v           |      v                     |
  |  SFT 모델    |  Reward Model    |   정렬된 LLM (RL Model)    |
  +--------------+------------------+----------------------------+
```

### 보상 모델 (Reward Model) 학습

- **입력**: (프롬프트, 응답) 쌍
- **레이블**: 사람이 선택한 선호 응답 (A > B 형식 비교)
- **목표**: 선호 응답에 높은 스칼라 점수 r 부여
- **손실 (Bradley-Terry 모델)**: `L = -E[log σ(r(x,y_w) - r(x,y_l))]`
  - y_w: 선호 응답 (winner), y_l: 비선호 응답 (loser)

### PPO (Proximal Policy Optimization) 핵심 수식

```
  PPO Clipped Objective (클리핑 목적 함수):
  L_CLIP = E[min(rₜ(θ)Aₜ, clip(rₜ(θ), 1-ε, 1+ε) · Aₜ)]

  여기서:
  - rₜ(θ)  : 새 정책 / 이전 정책 확률비 (probability ratio)
  - Aₜ     : 어드밴티지 (Advantage) — 기대 대비 초과 보상
  - ε      : 클리핑 계수 (보통 0.1~0.2)

  최종 RLHF 보상:
  r_total = r_RM(x,y) - β · KL[π_θ(y|x) || π_SFT(y|x)]
  - β : KL 패널티 계수 (SFT 로부터 이탈 억제)
```

### KL 패널티의 역할

KL 발산 (KL Divergence) 을 패널티로 추가하지 않으면 모델이 보상 모델을 해킹 (Reward Hacking) — 보상 점수만 높지만 품질은 떨어지는 응답을 생성하는 현상이 발생한다. KL 패널티는 "SFT 모델에서 너무 멀어지면 불이익" 을 주어 안전망 역할을 한다.

- **📢 섹션 요약 비유**: PPO 는 "급격한 성격 변화를 막는 심리 치료"다. 한 번의 상담으로 너무 극단적으로 변하지 않도록 (클리핑), 원래 성격에서 너무 멀어지지 않도록 (KL 패널티) 두 가지 제동 장치를 건다.

---

## Ⅲ. 비교 및 연결

### RLHF 대안 방법론 비교

| 방법 | 핵심 아이디어 | 장점 | 단점 |
|:---|:---|:---|:---|
| RLHF + PPO | 보상 모델 + 강화학습 | 고품질 정렬 | 구현 복잡, Reward Hacking 취약 |
| DPO (Direct Preference Optimization) | 직접 선호 최적화 | 단순 구현, 보상 모델 불필요 | PPO 대비 표현력 제한 |
| RLAIF (RL from AI Feedback) | AI 가 피드백 제공 | 확장성 높음 | AI 편향 전파 가능성 |
| Constitutional AI (CAI) | 헌법 규칙 자기 비판 | 투명성 높음 | 규칙 설계 비용 |

### ChatGPT 구현 방식 (OpenAI InstructGPT)

1. **SFT**: GPT-3 + 인간 작성 데모 데이터 (13K 개) 미세조정
2. <strong>Reward Model</strong>: 6B 파라미터 모델로 33K 비교 데이터 학습
3. <strong>PPO</strong>: SFT 모델을 초기 정책으로 PPO 적용, β=0.02 KL 패널티

- **📢 섹션 요약 비유**: RLHF vs DPO 는 "경기에서 심판(보상 모델)을 두고 반칙 시 벌점 주는 방식" vs "선수가 직접 좋아하는 플레이 스타일을 학습하는 방식"의 차이다. 심판이 있으면 정교하지만 복잡하고, 없으면 단순하지만 미묘한 조정이 어렵다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### RLHF 구현 오픈소스 생태계

| 도구 | 설명 |
|:---|:---|
| TRL (Transformer Reinforcement Learning) | HuggingFace RLHF 라이브러리 |
| DeepSpeed-Chat | Microsoft 엔드투엔드 RLHF |
| OpenRLHF | 분산 RLHF 학습 프레임워크 |
| LLaMA-Factory | SFT+RLHF 통합 파인튜닝 도구 |

### 학습 주제 포인트

- RLHF 3단계 (SFT -> Reward Model -> PPO) 순서와 각 단계의 목적 명시
- PPO 클리핑 목적 함수와 KL 패널티의 역할 구별
- Reward Hacking 개념과 KL 패널티가 방지책이 되는 원리
- DPO (Direct Preference Optimization) 와 비교: 보상 모델 유무
- 인간 피드백 데이터 수집 비용과 확장성 한계 언급

- **📢 섹션 요약 비유**: RLHF 는 "AI 를 인턴으로 고용해 처음엔 교육(SFT), 다음엔 팀장 평가(Reward Model), 마지막엔 실적 기반 성과급(PPO)" 을 주는 방식으로 점점 더 회사 문화에 맞게 만드는 과정이다.

---

## Ⅴ. 기대효과 및 결론

- **정렬 달성**: 지시 따르기, 유해성 감소, 사실성 향상 동시 실현
- **확장성**: SFT 데이터 수천 건으로도 큰 효과 (데이터 효율 높음)
- **산업 적용**: ChatGPT, Claude, Gemini, Llama 2 Chat 에 공통 적용
- **한계**: 인간 피드백 데이터 수집 비용, 평가자 편향, Reward Hacking

RLHF 는 언어 모델을 "텍스트 생성기"에서 "유용한 어시스턴트"로 전환하는 핵심 기술이다. 심화 학습에서는 3단계 파이프라인, PPO 수식의 클리핑과 KL 패널티, DPO 와의 비교를 명확히 서술하면 고득점이 가능하다.

- **📢 섹션 요약 비유**: RLHF 는 "백과사전 달달 외운 똑똑이"를 "사람들이 좋아하는 답을 주는 현명한 친구"로 바꾸는 사회화 프로세스다. 지식은 이미 있으니, 어떻게 말하는지를 훈련하는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| SFT (Supervised Fine-Tuning) | 지도 미세조정, 데모 데이터 / RLHF 1단계 기반 모델 |
| Reward Model (보상 모델) | Bradley-Terry, 선호 학습 / RLHF 2단계 평가 함수 |
| PPO (Proximal Policy Optimization) | 클리핑, KL 패널티 / RLHF 3단계 정책 최적화 |
| DPO (Direct Preference Optimization) | 보상 모델 제거 / RLHF 경량 대안 |
| KL Divergence (KL 발산) | 정보 이론, 분포 차이 / Reward Hacking 방지 |
| Alignment (정렬) | HHH, 안전 AI / RLHF 의 궁극 목표 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] -> [RLHF (Reinforcement Learning from Human Feedback)] -> [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 📚 AI 가 처음엔 책에서 배우고(SFT), 선생님이 좋은 답/나쁜 답을 골라주면(Reward Model), 좋은 점수 받으려고 스스로 더 잘 말하는 방법을 연습해요(PPO).
2. ⚖️ 너무 이상하게 변하지 않도록 "원래 너답게 말해!" 라는 규칙(KL 패널티)도 있어요.
3. 🤝 이렇게 훈련하면 ChatGPT 처럼 사람이 원하는 걸 잘 도와주는 AI 가 돼요!
