---
title: "Transformer Architecture Self Attention"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 139
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 <strong>RNN의 순차 처리를 Self-Attention으로 대체</strong>하여 시퀀스 전체를 병렬 처리하는 아키텍처이며, "Attention Is All You Need"(2017, Google)에서 제안되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 <strong>병렬화 불가·장기 의존성 약점</strong>이 있지만, Transformer는 <strong>O(1) 거리로 모든 위치에 접근</strong>하고 GPU 병렬화가 완벽하여 대규모 학습이 가능하다.
> 3. **판단 포인트**: Encoder-only(BERT, 이해)·Decoder-only(GPT, 생성)·Encoder-Decoder(T5, 번역)로 변형되며, Multi-Head Attention·Positional Encoding·Feed-Forward Network가 핵심 구성이다.

---

## Ⅰ. 개요 및 필요성

```text
Transformer = Encoder + Decoder
  Encoder: [Multi-Head Self-Attention -> FFN] × N
  Decoder: [Masked Self-Attention -> Cross-Attention -> FFN] × N
  + Positional Encoding (순서 정보)
```

- **📢 섹션 요약 비유**: RNN은 **줄 서서 한 명씩 통과(순차)**, Transformer는 <strong>모든 사람이 동시에 대화(병렬)</strong>하는 것이다.

---

## Ⅱ~Ⅴ. 결론

Transformer는 <strong>현대 AI의 기반 아키텍처</strong>이며, BERT·GPT·T5·LLM·ViT 모두 Transformer 변형이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Transformer</strong> | Self-Attention 기반 |
| <strong>Self-Attention</strong> | 모든 위치 간 관련도 |
| **Multi-Head** | 다관점 Attention |
| <strong>Positional Encoding</strong> | 순서 정보 주입 |
| <strong>GPT/BERT</strong> | Decoder/Encoder 변형 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Seq2Seq+Attention (2014)] -> [Transformer (2017, Google)]
    -> [BERT (Encoder, 2018)] -> [GPT-2/3 (Decoder, 2019~)]
    -> [T5 (Enc-Dec, 2019)] -> [GPT-4/LLM (2023~)]
    -> [현재: Mamba/RWKV — Transformer 대안 탐색]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 **한 줄로 서서 순서대로** 이야기를 전달해요(느림).
2. Transformer는 <strong>모든 사람이 동시에 대화</strong>해서 훨씬 빨라요(병렬).
3. ChatGPT, BERT, 번역기 등 <strong>거의 모든 AI</strong>가 Transformer를 사용해요!
