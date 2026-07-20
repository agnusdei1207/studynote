---
title: "Attention Mechanism"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 121
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Attention은 디코더가 출력을 생성할 때, 인코더의 <strong>모든 Hidden State에 가중치(Attention Weight)를 부여하여 동적으로 참조</strong>하는 메커니즘으로, 고정 컨텍스트 벡터의 정보 병목을 해소한다.
> 2. **가치**: "I love you" -> "나는 너를 사랑해" 번역 시, "사랑해"를 생성할 때 <strong>"love"에 높은 가중치</strong>를 부여하여 해당 입력에 "주목(Attend)"한다. 이로써 긴 문장에서도 정보 손실 없이 정확한 번역이 가능해진다.
> 3. **판단 포인트**: Bahdanau(Additive) Attention과 Luong(Multiplicative/Dot-product) Attention을 구분하고, Self-Attention(Transformer)으로의 진화를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Attention 동작 과정                                |
+-------------------------------------------------------+
|  인코더: h₁(I), h₂(love), h₃(you)                   |
|                                                       |
|  디코더 t=3 ("사랑해" 생성):                          |
|   1. s₃(디코더 상태)와 h₁,h₂,h₃ 유사도 계산         |
|   2. e₃₁=score(s₃,h₁), e₃₂=score(s₃,h₂)...        |
|   3. α = softmax([e₃₁, e₃₂, e₃₃])                  |
|      = [0.1, 0.8, 0.1]  <- "love"에 집중!            |
|   4. c₃ = 0.1·h₁ + 0.8·h₂ + 0.1·h₃ (가중 합)       |
|   5. 출력 = f(s₃, c₃) -> "사랑해"                    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Attention은 시험 중 **전체 교과서를 보면서** 문제에 관련된 페이지에 **형광펜을 칠하는** 것이다. 관련 높은 페이지일수록 밝게 칠한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Attention 유형

| 유형 | Score 함수 | 특징 |
|:---|:---|:---|
| **Bahdanau (Additive)** | v^T · tanh(W[s;h]) | 학습 파라미터 많음 |
| <strong>Luong (Dot-product)</strong> | s^T · h | **효율적, 빠름** |
| <strong>Scaled Dot-product</strong> | (Q·K^T)/√d_k | <strong>Transformer 표준</strong> |

### Cross-Attention vs Self-Attention

| 비교 | Cross-Attention | Self-Attention |
|:---|:---|:---|
| **Q** | 디코더 | **같은 시퀀스** |
| **K, V** | 인코더 | **같은 시퀀스** |
| **대표** | Seq2Seq Attention | <strong>Transformer</strong> |

- **📢 섹션 요약 비유**: Cross-Attention은 번역가가 원문을 참조하는 것이고, Self-Attention은 글 쓸 때 자기 문장 앞뒤를 돌아보는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 고정 컨텍스트 | Attention | Self-Attention |
|:---|:---|:---|:---|
| <strong>참조</strong> | 마지막 h만 | **모든 h** | **자기 시퀀스** |
| <strong>병렬화</strong> | 불가 | 불가 | **가능** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Attention의 해석 가능성
- Attention 가중치를 시각화하면 "모델이 어디를 보고 판단했는지" 확인 가능 -> 설명 가능 AI(XAI)의 초기 형태.

---

## Ⅴ. 기대효과 및 결론

Attention은 <strong>현대 AI의 가장 중요한 단일 아이디어</strong>이며, Transformer·BERT·GPT·ViT·Diffusion 등 거의 모든 최신 모델의 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Bahdanau Attention** | Additive Score, 2014 |
| **Luong Attention** | Dot-product Score, 2015 |
| <strong>Self-Attention</strong> | Transformer의 핵심 |
| <strong>Multi-Head Attention</strong> | 여러 관점에서 Attention |
| **Cross-Attention** | 인코더-디코더 Attention |

### 📈 관련 키워드 및 발전 흐름도

```text
[Seq2Seq 고정 컨텍스트 벡터 (2014)]
    |
    v
[Bahdanau Attention (2014) — Additive]
    |
    v
[Luong Attention (2015) — Dot-product]
    |
    v
[Self-Attention + Transformer (2017) — "Attention Is All You Need"]
    |
    v
[현재: Flash Attention / Linear Attention — 효율적 Attention]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Attention은 시험 중 **교과서 전체를 보면서** 문제와 관련된 페이지에 <strong>형광펜</strong>을 치는 거예요.
2. 관련 높은 페이지는 **밝게**, 관련 낮은 페이지는 **약하게** 칠해요.
3. 이 아이디어가 너무 좋아서 <strong>ChatGPT(Transformer)의 핵심 기술</strong>이 되었답니다!
