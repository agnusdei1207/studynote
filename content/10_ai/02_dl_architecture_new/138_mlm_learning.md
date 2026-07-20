---
title: "Mlm Learning"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 138
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MLM은 <strong>입력 토큰의 15%를 [MASK]로 가리고 양방향 문맥으로 원래 토큰을 예측</strong>하는 BERT의 사전 학습 방식이며, 빈칸 채우기(Cloze Test)와 같은 원리이다.
> 2. **가치**: GPT의 CLM(Causal LM, 왼->오)은 왼쪽 문맥만 보지만, MLM은 **양쪽 문맥을 동시에** 참조하여 "bank"가 은행인지 강둑인지 더 정확히 판별한다.
> 3. **판단 포인트**: MLM은 <strong>이해(NLU)에 최적</strong>이지만 생성에는 부적합하며, Generative 작업에는 CLM(GPT)·Prefix LM(T5)이 적합하다.

---

## Ⅰ. 개요 및 필요성

```text
입력: "나는 [MASK]에서 [MASK]를 먹었다"
예측: [MASK1] = "식당", [MASK2] = "밥"
  -> 양방향 문맥(나는, 를, 먹었다)을 모두 참조
  -> 양방향 이해 능력 학습
```

- **📢 섹션 요약 비유**: MLM은 <strong>빈칸 채우기 시험</strong>이다. 양쪽 힌트를 보고 빈칸에 들어갈 단어를 맞춘다.

---

## Ⅱ~Ⅴ. 결론

MLM은 <strong>양방향 언어 이해의 핵심 학습 방식</strong>이며, BERT·RoBERTa·DeBERTa의 사전 학습 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **MLM** | 빈칸 채우기 (양방향) |
| **CLM** | 다음 토큰 예측 (GPT) |
| <strong>BERT</strong> | MLM 기반 모델 |
| **RoBERTa** | NSP 제거 + 더 많은 학습 |
| **Denoising** | T5의 변형 MLM |

### 📈 관련 키워드 및 발전 흐름도

```text
[Word2Vec CBOW (2013)] -> [ELMo (2018)]
    -> [BERT MLM (2018)] -> [RoBERTa (NSP 제거, 2019)]
    -> [SpanBERT (Span Masking)]
    -> [현재: Replaced Token Detection (ELECTRA)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. MLM은 <strong>빈칸 채우기 시험</strong>이에요. "나는 ___에서 ___를 먹었다"
2. 앞뒤 단어를 <strong>모두 힌트로</strong> 사용해서 빈칸을 맞춰요.
3. 이렇게 공부하면 **문장의 의미를 깊이** 이해할 수 있어요!
