---
title: "Prompt Tuning"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 136
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Prompt Tuning은 <strong>모델 가중치를 동결하고, 입력 앞에 붙이는 연속(Soft) 프롬프트 벡터만 학습</strong>하여 특정 작업에 적응하는 PEFT 기법이며, 학습 파라미터가 전체의 <strong>0.01% 미만</strong>이다.
> 2. **가치**: 모델 자체를 건드리지 않으므로 <strong>하나의 모델로 수천 개의 다른 프롬프트(=어댑터)</strong>를 동시에 서빙할 수 있으며, 배포·관리가 극도로 효율적이다.
> 3. **판단 포인트**: 모델 규모가 클수록(10B+) Prompt Tuning이 Full FT에 근접한 성능을 내며, 소규모 모델에서는 LoRA가 더 효과적이다.

---

## Ⅰ. 개요 및 필요성

```text
Hard Prompt: 사람이 작성한 텍스트 프롬프트
Soft Prompt: 학습 가능한 연속 벡터 (임베딩 공간)
  모델 동결 -> 프롬프트 벡터만 학습 -> 파라미터 <0.01%
```

- **📢 섹션 요약 비유**: Prompt Tuning은 **자물쇠(모델)는 그대로 두고 열쇠(프롬프트)만 만드는** 것이다.

---

## Ⅱ~Ⅴ. 결론

Prompt Tuning은 <strong>다작업 서빙에 최적</strong>이며, 대규모 모델에서 LoRA의 경량 대안으로 활용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Prompt Tuning** | 소프트 프롬프트 학습 |
| **Prefix Tuning** | Prompt Tuning 변형 |
| <strong>LoRA</strong> | 더 높은 성능 대안 |
| **Hard Prompt** | 사람이 작성 (고정) |
| **Soft Prompt** | 학습 가능 (연속) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Hard Prompt Engineering (2020)]
    -> [Prefix Tuning (2021)] -> [Prompt Tuning (2021, Google)]
    -> [P-Tuning v2 (2022)] -> [현재: LoRA+Prompt 하이브리드]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Prompt Tuning은 <strong>자물쇠(AI)는 그대로 두고 열쇠(프롬프트)만 만드는</strong> 거예요.
2. 열쇠 하나로 <strong>하나의 문제</strong>를 풀 수 있어요. 열쇠가 100개면 100개 문제!
3. 자물쇠를 바꾸는 것(Full FT)보다 **열쇠만 만드는 게** 훨씬 빨라요!
