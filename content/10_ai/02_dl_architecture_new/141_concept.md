---
title: "Concept"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 141
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LLM(Large Language Model)은 <strong>수십~수천억 파라미터의 Transformer 기반 모델</strong>을 대규모 텍스트로 사전 학습하여, 다음 토큰 예측(CLM)·빈칸 채우기(MLM)를 통해 언어 이해·생성 능력을 획득한 모델이다.
> 2. **가치**: 특정 작업을 위한 별도 모델 학습 없이, <strong>프롬프트만으로(Zero/Few-shot)</strong> 번역·요약·코딩·추론 등 다양한 작업을 수행하며, 스케일링 법칙에 의해 <strong>모델 크기^ -> 능력 창발(Emergence)</strong>이 나타난다.
> 3. **판단 포인트**: 사전 학습(Pre-training)->지시 튜닝(Instruction Tuning)->RLHF(인간 피드백 정렬)의 3단계가 ChatGPT급 모델의 학습 파이프라인이다.

---

## Ⅰ. 개요 및 필요성

```text
LLM 학습 파이프라인:
  1. Pre-training: 대규모 텍스트 -> 다음 토큰 예측 (수개월, 수천 GPU)
  2. Instruction Tuning: 지시-응답 쌍 학습 -> 지시 따르기 능력
  3. RLHF: 인간 선호 피드백 -> 유해 출력 억제 -> 정렬(Alignment)
```

- **📢 섹션 요약 비유**: LLM은 <strong>대학 교육(Pre-training) -> 직무 교육(IT) -> 사회생활 매너(RLHF)</strong>의 3단계로 완성된다.

---

## Ⅱ~Ⅴ. 결론

LLM은 <strong>Pre-training + IT + RLHF</strong>의 3단계로 완성되며, 스케일링 법칙과 Emergence가 핵심 현상이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>LLM</strong> | 대규모 언어 모델 |
| <strong>Pre-training</strong> | 기반 능력 학습 |
| <strong>Instruction Tuning</strong> | 지시 따르기 |
| <strong>RLHF</strong> | 인간 정렬 |
| **Emergence** | 창발적 능력 |

### 📈 관련 키워드 및 발전 흐름도

```text
[GPT-1 (117M, 2018)] -> [GPT-3 (175B, 2020)]
    -> [InstructGPT/ChatGPT (RLHF, 2022)]
    -> [GPT-4 (MoE, 2023)] -> [LLaMA (오픈소스)]
    -> [현재: GPT-5 · Claude · Gemini — 멀티모달+추론]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LLM은 <strong>엄청 많은 책을 읽은 AI</strong>예요. 수십억 문장을 읽었어요.
2. 책을 읽고(Pre-training), <strong>선생님 말씀 듣는 법(IT)</strong>을 배우고, <strong>예의(RLHF)</strong>를 배워요.
3. ChatGPT처럼 **질문하면 답하는** 똑똑한 AI가 되는 거예요!
