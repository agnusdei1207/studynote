---
title: "Cross Attention"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 128
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Cross-Attention은 <strong>Query는 디코더에서, Key·Value는 인코더에서 오는 Attention</strong>이며, 디코더가 인코더의 출력을 참조하여 <strong>소스->타겟 매핑(번역·요약)을 수행</strong>한다.
> 2. **가치**: 인코더만으로는 소스 문장을 이해하지만 타겟을 생성하지 못하고, 디코더만으로는 소스를 참조하지 못하므로, Cross-Attention이 <strong>인코더의 정보를 디코더로 전달하는 유일한 경로</strong>이다.
> 3. **판단 포인트**: Self-Attention(Q=K=V 같은 시퀀스) vs Cross-Attention(Q≠K,V 다른 시퀀스)을 구분하고, 인코더-디코더 모델(T5·BART)에서만 사용되며, GPT(디코더 전용)에는 없다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Cross-Attention 동작                               |
+-------------------------------------------------------+
|  [인코더] "나는 학생이다" -> 인코더 출력 (K, V)       |
|                                                       |
|  [디코더] "I am a" -> 디코더 상태 (Q)                 |
|                                                       |
|  Cross-Attention:                                     |
|   Q("a"의 상태) × K(인코더 출력)^T -> Attention Score |
|   -> V(인코더 출력) 가중합 -> "student" 예측           |
|                                                       |
|  핵심: Q는 디코더, K·V는 인코더에서 옴               |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Cross-Attention은 <strong>통역사</strong>이다. 화자(인코더)의 말을 듣고(K,V), 청자(디코더)가 이해하는 언어(Q)로 번역한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Cross

| 비교 | Self-Attention | Cross-Attention |
|:---|:---|:---|
| **Q** | 같은 시퀀스 | <strong>디코더</strong> |
| **K, V** | 같은 시퀀스 | <strong>인코더</strong> |
| **용도** | 내부 관계 | **소스->타겟 매핑** |
| **모델** | BERT, GPT | **T5, BART** |

- **📢 섹션 요약 비유**: Self는 자기 자신을 비추는 거울, Cross는 다른 사람을 비추는 쌍안경이다.

---

## Ⅲ. 비교 및 연결

| 모델 | Self | Masked Self | Cross |
|:---|:---|:---|:---|
| <strong>BERT</strong> | ✅ | ❌ | ❌ |
| <strong>GPT</strong> | ❌ | ✅ | ❌ |
| **T5** | ✅ | ✅ | **✅** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### Cross-Attention 적용
- 기계 번역 (T5, mBART).
- 이미지 캡셔닝 (이미지 인코더 -> 텍스트 디코더).
- Stable Diffusion (텍스트 -> 이미지 생성에서 텍스트를 K,V로).

---

## Ⅴ. 기대효과 및 결론

Cross-Attention은 <strong>서로 다른 모달리티·언어 간 정보를 전달하는 핵심 메커니즘</strong>이며, 멀티모달 AI의 기반이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Cross-Attention** | Q(디코더)↔K,V(인코더) |
| <strong>Self-Attention</strong> | 같은 시퀀스 내 참조 |
| <strong>인코더-디코더</strong> | Cross-Attention이 필요한 구조 |
| **Stable Diffusion** | 텍스트 Cross-Attention으로 이미지 생성 |
| **T5** | 인코더-디코더 대표 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Attention (Bahdanau, 2014) — 최초 Cross-Attention]
    |
    v
[Transformer (2017) — Self + Cross + Masked]
    |
    v
[T5 / BART (2019~2020) — 인코더-디코더 사전 학습]
    |
    v
[Stable Diffusion (2022) — Cross-Attention으로 이미지 제어]
    |
    v
[현재: 멀티모달 Cross-Attention — 이미지·텍스트·오디오 융합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Cross-Attention은 <strong>통역사</strong>예요. 한국어(인코더)를 듣고 영어(디코더)로 번역해요.
2. 통역사가 없으면 한국어만 아는 사람과 영어만 아는 사람이 **대화를 못 해요**.
3. Stable Diffusion도 "고양이 그려줘"라는 <strong>글(인코더)을 그림(디코더)으로 통역</strong>한답니다!
