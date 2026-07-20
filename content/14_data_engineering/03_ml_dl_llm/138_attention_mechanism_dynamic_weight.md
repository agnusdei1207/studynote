---
title: "Attention Mechanism Dynamic Weight"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 138
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Attention은 <strong>입력 시퀀스의 모든 위치에 대해 현재 출력과의 관련도(유사도)를 계산하여 동적 가중치를 부여</strong>하는 메커니즘이며, Transformer의 핵심 구성 요소(Self-Attention)이다.
> 2. **가치**: RNN은 긴 문장에서 초반 정보를 잊지만(Vanishing), Attention은 <strong>거리에 무관하게 관련 위치에 직접 접근</strong>하여 장기 의존성 문제를 근본적으로 해결한다.
> 3. **판단 포인트**: Scaled Dot-Product Attention(Q·K·V)이 표준이며, Multi-Head Attention으로 다양한 관점의 관련도를 동시에 학습한다.

---

## Ⅰ. 개요 및 필요성

```text
Attention(Q, K, V) = softmax(QK^T / √d_k) · V
  Q: Query (현재 위치) -> "무엇에 집중할까?"
  K: Key (모든 위치) -> "관련도 계산"
  V: Value (모든 위치) -> "가중 합산"
```

- **📢 섹션 요약 비유**: Attention은 <strong>시험 문제(Query)에 맞는 교과서 페이지(Key)를 찾아 해당 내용(Value)에 집중</strong>하는 것이다.

---

## Ⅱ~Ⅴ. 결론

Attention은 <strong>현대 AI의 가장 중요한 메커니즘</strong>이며, Transformer·LLM·Vision의 핵심 구성 요소이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Attention** | 동적 가중치 |
| <strong>Self-Attention</strong> | 자기 자신에 대한 Attention |
| **Multi-Head** | 다관점 Attention |
| **Q·K·V** | Query·Key·Value |
| <strong>Transformer</strong> | Attention 기반 아키텍처 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Seq2Seq (2014)] -> [Bahdanau Attention (2014)]
    -> [Luong Attention (2015)]
    -> [Self-Attention -> Transformer (2017)]
    -> [현재: Flash Attention — 메모리 효율^]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Attention은 <strong>시험 문제(Query)</strong>에 맞는 <strong>교과서 페이지(Key)</strong>를 찾아요.
2. 관련 있는 페이지의 <strong>내용(Value)</strong>에 집중하고 나머지는 무시해요.
3. 긴 문장에서도 **중요한 단어만 골라** 이해할 수 있어요!
