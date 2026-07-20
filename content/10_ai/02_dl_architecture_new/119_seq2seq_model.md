---
title: "Seq2Seq Model"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 119
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Seq2Seq은 <strong>인코더 RNN이 입력 시퀀스를 고정 길이 컨텍스트 벡터로 압축</strong>하고, <strong>디코더 RNN이 이 벡터를 기반으로 출력 시퀀스를 생성</strong>하는 인코더-디코더 아키텍처이다.
> 2. **가치**: 입력과 출력의 **길이가 다른** 태스크(기계 번역: "I love you" -> "나는 너를 사랑해", 요약, 챗봇)에 최적이며, 이전 RNN은 입력=출력 길이가 같아야 했다.
> 3. **판단 포인트**: 컨텍스트 벡터가 <strong>고정 길이(병목)</strong>이므로 긴 입력에서 정보 손실이 발생하며, 이를 해결한 것이 **Attention 메커니즘**(Bahdanau, 2014)이고, 최종 진화가 <strong>Transformer</strong>(2017)이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Seq2Seq 아키텍처                                   |
+-------------------------------------------------------+
|  [인코더]                  [디코더]                    |
|   I -> h1 -> love -> h2 -> you -> h3                     |
|                              |                        |
|                         Context Vector (c)            |
|                              |                        |
|                    <SOS> -> 나는 -> 너를 -> 사랑해 -> <EOS>|
|                                                       |
|  문제: c가 고정 길이 -> 긴 문장에서 정보 손실!        |
|  해결: Attention -> c 대신 모든 h_i를 가중 참조       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 인코더는 통역사가 영어 문장을 듣고 메모(컨텍스트 벡터)하는 것이고, 디코더는 그 메모를 보고 한국어로 말하는 것이다. 메모가 한 줄(고정 길이)이면 긴 문장은 다 못 적는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Seq2Seq 구성 요소

| 요소 | 역할 |
|:---|:---|
| <strong>인코더</strong> | 입력 시퀀스 -> 컨텍스트 벡터 압축 |
| <strong>디코더</strong> | 컨텍스트 벡터 -> 출력 시퀀스 생성 |
| <strong>Context Vector</strong> | 인코더 최종 Hidden State |
| **Teacher Forcing** | 학습 시 정답 토큰을 디코더 입력으로 사용 |

### Teacher Forcing vs Autoregressive

| 방식 | 학습 | 추론 |
|:---|:---|:---|
| **Teacher Forcing** | 정답 토큰 입력 (빠름) | 사용 불가 |
| <strong>Autoregressive</strong> | 이전 출력을 다음 입력 | **추론 시 사용** |

- **📢 섹션 요약 비유**: Teacher Forcing은 선생님이 정답을 불러주면서 받아쓰기 연습하는 것이고, Autoregressive는 혼자 써보는 실전이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Seq2Seq | Seq2Seq+Attention | Transformer |
|:---|:---|:---|:---|
| **병목** | 고정 벡터 | <strong>가중 참조로 해소</strong> | Self-Attention |
| <strong>병렬화</strong> | 불가 | 불가 | **가능** |
| <strong>성능</strong> | 기본 | 향상 | **최고** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Seq2Seq 적용 분야
1. **기계 번역**: 원문 -> 번역문 (Google NMT 초기).
2. **챗봇**: 질문 -> 응답 생성.
3. <strong>텍스트 요약</strong>: 긴 문서 -> 요약문.
4. **음성 인식**: 오디오 -> 텍스트.

---

## Ⅴ. 기대효과 및 결론

Seq2Seq은 "가변 길이 입력 -> 가변 길이 출력"이라는 근본 문제를 해결한 혁신 아키텍처이며, Attention과 결합하여 Transformer의 직접적 전신이 되었다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>인코더-디코더</strong> | Seq2Seq의 핵심 구조 |
| <strong>Context Vector</strong> | 인코더가 생성하는 고정 길이 벡터 (병목) |
| **Attention** | 병목을 해결하는 가중 참조 메커니즘 |
| **Teacher Forcing** | 학습 시 정답 토큰 제공 전략 |
| <strong>Transformer</strong> | Seq2Seq + Self-Attention의 진화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[RNN (입력=출력 길이 동일)]
    |
    v
[Seq2Seq (2014, Sutskever) — 가변 길이 변환]
    |
    v
[Attention (2014, Bahdanau) — 병목 해소]
    |
    v
[Transformer (2017) — Self-Attention, 순환 제거]
    |
    v
[현재: GPT/BERT — Transformer 기반 거대 모델]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Seq2Seq은 <strong>통역사</strong>예요. 영어(입력)를 듣고 <strong>메모(컨텍스트 벡터)</strong>한 뒤, 한국어(출력)로 말해요.
2. 문제는 메모가 <strong>한 줄뿐</strong>이라 긴 문장은 다 못 적어요 (정보 손실).
3. 그래서 Attention이 등장해서 <strong>전체 문장을 보면서 번역</strong>할 수 있게 되었답니다!
