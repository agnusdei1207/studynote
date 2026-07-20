---
title: "Masked Self Attention"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 127
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Masked Self-Attention은 <strong>디코더에서 현재 위치 이후의 미래 토큰을 참조하지 못하도록 마스킹(-∞)하는 Self-Attention</strong>이며, GPT 등 자기 회귀(Autoregressive) 모델의 핵심 메커니즘이다.
> 2. **가치**: "I love"까지 생성 후 다음 토큰을 예측할 때, 정답인 "you"를 이미 본 상태에서 예측하면 <strong>학습이 무의미(data leakage)</strong>하므로, Masked Self-Attention이 미래를 가려서 <strong>진정한 예측</strong>을 가능하게 한다.
> 3. **판단 포인트**: Causal Mask(하삼각 행렬)를 Attention Score에 적용하여 미래 위치에 -∞를 더하고 softmax 후 0이 되게 하며, BERT(양방향)는 마스킹 없이 전체 참조한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Masked Self-Attention                              |
+-------------------------------------------------------+
|  입력: "I love you <EOS>"                             |
|                                                       |
|  Attention Matrix (마스킹 전):                        |
|       I    love  you  <EOS>                           |
|  I  [ 0.5  0.3   0.1  0.1 ]                          |
|  love[ 0.2  0.4   0.3  0.1 ]                         |
|  you [ 0.1  0.2   0.5  0.2 ]                         |
|                                                       |
|  Causal Mask (하삼각):                                |
|       I    love  you  <EOS>                           |
|  I  [ ✓    ✗     ✗    ✗   ]                          |
|  love[ ✓    ✓     ✗    ✗   ]                         |
|  you [ ✓    ✓     ✓    ✗   ]                         |
|                                                       |
|  "love" 예측 시 "I"만 참조 (미래 차단!)              |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Masked Self-Attention은 시험에서 <strong>다음 문제의 답을 못 보게 가리는 것</strong>이다. 답을 보면 실력 측정이 안 되니까.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Masked Self vs Cross

| 유형 | 마스킹 | 용도 |
|:---|:---|:---|
| **Self** | 없음 | 인코더 (BERT) |
| **Masked Self** | **하삼각** | <strong>디코더 (GPT)</strong> |
| **Cross** | 없음 | 인코더->디코더 참조 |

- **📢 섹션 요약 비유**: Self는 책 전체를 보고 이해, Masked는 앞 페이지만 보고 다음 페이지 예측.

---

## Ⅲ. 비교 및 연결

| 비교 | BERT (Self) | GPT (Masked Self) |
|:---|:---|:---|
| <strong>참조</strong> | 양방향 | **왼->오만** |
| **학습** | MLM (빈칸) | **다음 토큰 예측** |
| **용도** | 이해·분류 | <strong>생성</strong> |

---

## Ⅳ. 실무 적용 및 실무자 판단

### KV Cache
- 자기 회귀 생성 시 이전 Key·Value를 캐싱하여 중복 계산 방지.
- Masked Self-Attention의 성질(과거만 참조)을 활용한 추론 최적화.

---

## Ⅴ. 기대효과 및 결론

Masked Self-Attention은 <strong>GPT·Llama 등 자기 회귀 LLM의 필수 구성 요소</strong>이며, KV Cache와 결합하여 효율적 텍스트 생성을 실현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Causal Mask** | 하삼각 행렬 (미래 차단) |
| <strong>Autoregressive</strong> | 이전 토큰으로 다음 예측 |
| <strong>KV Cache</strong> | 추론 시 Key·Value 재사용 |
| <strong>BERT</strong> | 마스킹 없음 (양방향) |
| <strong>GPT</strong> | Masked Self-Attention 사용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Self-Attention (Transformer, 2017)]
    |
    v
[Masked Self-Attention (GPT-1, 2018)]
    |
    v
[KV Cache 최적화 (2020~)]
    |
    v
[Sliding Window Attention (Mistral, 2023)]
    |
    v
[현재: Sparse + Masked — 효율적 긴 시퀀스 생성]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Masked Self-Attention은 시험에서 **다음 문제의 답을 가리는** 거예요.
2. 답을 미리 보면 <strong>진짜 실력</strong>을 측정할 수 없으니까요.
3. GPT가 <strong>앞 단어만 보고 다음 단어를 예측</strong>할 수 있는 건 이 마스킹 덕분이에요!
