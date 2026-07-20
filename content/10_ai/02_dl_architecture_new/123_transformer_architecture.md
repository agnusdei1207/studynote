---
title: "Transformer Architecture"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 123
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 <strong>순환(RNN) 없이 Self-Attention만으로 시퀀스를 병렬 처리</strong>하는 아키텍처이며, "Attention Is All You Need"(Vaswani, 2017)에서 제안되어 현대 AI의 <strong>사실상 유일한 기반 아키텍처</strong>가 되었다.
> 2. **가치**: RNN은 시퀀스를 순차 처리하여 <strong>병렬화 불가·장거리 의존성 약화</strong>라는 근본 한계가 있었으나, Transformer는 <strong>모든 위치를 동시에 참조(Self-Attention)</strong>하고 <strong>GPU 병렬화가 가능</strong>하여 학습 속도와 성능을 혁신적으로 개선했다.
> 3. **판단 포인트**: <strong>인코더-디코더 구조</strong>(기계 번역), <strong>인코더만</strong>(BERT, 분류), <strong>디코더만</strong>(GPT, 생성)의 3가지 변형을 구분하고, Multi-Head Attention·Positional Encoding·Layer Normalization이 핵심 구성 요소이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Transformer 구조                                   |
+-------------------------------------------------------+
|  [인코더 ×N]              [디코더 ×N]                 |
|  +--------------+        +--------------+            |
|  | Multi-Head   |        | Masked Multi-|            |
|  | Self-Attn    |        | Head Self-Attn|           |
|  | + Add & Norm |        | + Add & Norm |            |
|  |              |        |              |            |
|  | Feed-Forward |   --->  | Cross-Attn   |            |
|  | + Add & Norm |        | (Enc->Dec)    |            |
|  +--------------+        | Feed-Forward |            |
|                          | + Add & Norm |            |
|  + Positional Encoding   +--------------+            |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: RNN은 줄서기(순차 처리)이고, Transformer는 회의(모든 사람이 동시에 서로 참조, 병렬 처리)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 구성 요소

| 요소 | 역할 |
|:---|:---|
| <strong>Self-Attention</strong> | 시퀀스 내 모든 위치 상호 참조 |
| **Multi-Head** | 여러 관점에서 동시 Attention |
| <strong>Positional Encoding</strong> | 순서 정보 주입 (sin/cos) |
| **Residual + LayerNorm** | 깊은 학습 안정화 |
| <strong>Feed-Forward</strong> | 비선형 변환 (MLP) |

### Transformer 변형

| 변형 | 구성 | 대표 | 용도 |
|:---|:---|:---|:---|
| <strong>인코더-디코더</strong> | 둘 다 | T5 | 번역 |
| <strong>인코더만</strong> | 인코더 | <strong>BERT</strong> | 분류·NER |
| <strong>디코더만</strong> | 디코더 | <strong>GPT</strong> | 텍스트 생성 |

- **📢 섹션 요약 비유**: BERT는 독해 시험(양방향 이해), GPT는 작문 시험(왼->오 생성)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | RNN | LSTM | Transformer |
|:---|:---|:---|:---|
| <strong>병렬화</strong> | 불가 | 불가 | **가능** |
| **장거리** | 약함 | 개선 | **Self-Attn** |
| **학습 속도** | 느림 | 느림 | **빠름** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Transformer 적용 분야
- NLP: BERT·GPT·T5.
- Vision: ViT·DINO.
- Audio: Whisper.
- Multimodal: GPT-4V·Gemini.

---

## Ⅴ. 기대효과 및 결론

Transformer는 <strong>현대 AI의 단일 기반 아키텍처</strong>이며, NLP를 넘어 Vision·Audio·Multimodal까지 적용되어 AI 패러다임을 완전히 바꾸었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Self-Attention</strong> | Transformer의 핵심 연산 |
| **Multi-Head** | 다관점 병렬 Attention |
| <strong>Positional Encoding</strong> | 순서 정보 주입 |
| <strong>BERT</strong> | 인코더만 사용 (양방향) |
| <strong>GPT</strong> | 디코더만 사용 (자기 회귀) |

### 📈 관련 키워드 및 발전 흐름도

```text
[RNN / LSTM (순환, ~2016)]
    |
    v
[Attention (Bahdanau, 2014) — 병목 해소]
    |
    v
[Transformer (Vaswani, 2017) — "Attention Is All You Need"]
    |
    v
[BERT (2018) / GPT-2 (2019) — 사전 학습 혁명]
    |
    v
[현재: GPT-4 / Gemini / Claude — 거대 Transformer]
```

### 👶 어린이를 위한 3줄 비유 설명
1. RNN은 <strong>줄서기</strong>예요. 앞 사람이 끝나야 다음 사람이 시작하니까 느려요.
2. Transformer는 <strong>회의</strong>예요. 모든 사람이 <strong>동시에 서로 이야기(Self-Attention)</strong>해서 빨라요.
3. ChatGPT, BERT, Gemini 모두 <strong>Transformer</strong>로 만들어졌답니다!
