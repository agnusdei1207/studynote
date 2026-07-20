---
title: "Concept"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 145
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RLHF는 <strong>인간 평가자의 선호도 피드백으로 보상 모델(Reward Model)을 학습</strong>하고, 이를 기반으로 <strong>PPO(Proximal Policy Optimization) 강화학습</strong>으로 LLM을 인간 의도에 정렬(Align)하는 기법이다.
> 2. **가치**: 사전 학습된 LLM은 <strong>유해·편향·비관련 출력</strong>을 생성할 수 있지만, RLHF는 "인간이 선호하는 답변"을 학습하여 <strong>ChatGPT 수준의 안전하고 유용한 대화</strong>를 가능하게 했다.
> 3. **판단 포인트**: SFT(Supervised Fine-tuning)->RM(Reward Model) 학습->PPO 정렬의 3단계이며, DPO(Direct Preference Optimization)가 RM 없이 직접 정렬하는 간소화 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
RLHF 3단계:
  1. SFT: 지시-응답 쌍으로 기본 능력 학습
  2. Reward Model: 인간 선호(A>B) 비교 데이터 -> RM 학습
  3. PPO: RM 점수를 보상으로 LLM 강화학습 -> 정렬
DPO: RM 없이 선호 데이터로 직접 정렬 (간소화)
```

- **📢 섹션 요약 비유**: RLHF는 <strong>반려견 교육</strong>이다. 좋은 행동(선호 답변)에 간식(보상)을 주고, 나쁜 행동(유해 답변)을 억제한다.

---

## Ⅱ~Ⅴ. 결론

RLHF는 <strong>ChatGPT의 핵심 기술</strong>이며, DPO가 간소화 대안으로 부상 중이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>RLHF</strong> | 인간 피드백 강화학습 |
| <strong>Reward Model</strong> | 선호도 점수화 |
| <strong>PPO</strong> | 정책 최적화 |
| <strong>DPO</strong> | 직접 정렬 (간소화) |
| **Alignment** | 인간 의도 정렬 |

### 📈 관련 키워드 및 발전 흐름도

```text
[InstructGPT (RLHF, 2022)] -> [ChatGPT (2022)]
    -> [DPO (2023, RM 불필요)]
    -> [KTO (2024, 비교 불필요)]
    -> [현재: Constitutional AI (Anthropic)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RLHF는 <strong>반려견 교육</strong>이에요. 좋은 행동에 <strong>간식(보상)</strong>을 줘요.
2. "이 답변이 더 좋아" 하고 **사람이 골라주면** AI가 배워요.
3. 이렇게 배워서 ChatGPT가 **예의 바르고 유용한** 답을 해요!
