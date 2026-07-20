---
title: "Self Attention"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 124
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self-Attention은 <strong>같은 시퀀스 내에서 각 위치가 다른 모든 위치를 참조</strong>하여 문맥을 파악하는 메커니즘이며, Transformer의 핵심 연산이다. Q·K·V가 모두 <strong>같은 시퀀스에서 생성</strong>된다.
> 2. **가치**: "The animal didn't cross the street because **it** was too tired"에서 "it"이 "animal"을 가리킨다는 것을 파악하려면 문장 전체를 참조해야 하며, Self-Attention이 이를 <strong>가중치로 정량화</strong>한다.
> 3. **판단 포인트**: Cross-Attention(Q≠K,V, 인코더->디코더)과 구분하고, **Masked Self-Attention**(디코더에서 미래 토큰 참조 방지)의 필요성을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Self-Attention 동작                                |
+-------------------------------------------------------+
|  입력: "The cat sat on the mat"                       |
|                                                       |
|  "sat"의 Self-Attention:                              |
|   "The"->0.05, "cat"->0.30, "sat"->0.10               |
|   "on"->0.15, "the"->0.05, "mat"->0.35                |
|   -> "sat"은 "cat"과 "mat"에 높은 가중치!            |
|   -> "누가(cat) 어디에(mat) 앉았는지" 파악            |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Self-Attention은 교실에서 **모든 학생이 서로의 얼굴을 보면서** 누가 누구와 관련 있는지 파악하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Self vs Cross vs Masked

| 유형 | Q·K·V | 용도 |
|:---|:---|:---|
| **Self** | 같은 시퀀스 | <strong>인코더 (양방향)</strong> |
| **Cross** | Q(디코더), K,V(인코더) | 인코더->디코더 참조 |
| **Masked Self** | 같은 시퀀스 + 미래 마스킹 | <strong>디코더 (자기 회귀)</strong> |

- **📢 섹션 요약 비유**: Self는 책 전체를 보고 이해하는 것, Masked는 앞 페이지만 보고 다음 페이지를 예측하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | RNN | Self-Attention |
|:---|:---|:---|
| <strong>참조 범위</strong> | 직전 상태 | **전체 시퀀스** |
| <strong>병렬화</strong> | 불가 | **가능** |
| **장거리 의존성** | 약함 | **강함** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 계산 복잡도
- Self-Attention: **O(n^)** — 시퀀스 길이 n에 대해 모든 쌍 비교.
- 해결: Linear Attention·Flash Attention·Sliding Window.

---

## Ⅴ. 기대효과 및 결론

Self-Attention은 <strong>Transformer·BERT·GPT의 단일 핵심 메커니즘</strong>이며, Vision(ViT)·Audio(Whisper)까지 확장되어 현대 AI의 근간이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Self-Attention** | 같은 시퀀스 내 상호 참조 |
| **Masked Self-Attention** | 미래 토큰 마스킹 (GPT 디코더) |
| **Multi-Head** | 다관점 Self-Attention |
| **O(n^) 복잡도** | Self-Attention의 한계 |
| **Flash Attention** | O(n^) 메모리 최적화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cross-Attention (Bahdanau, 2014)]
    |
    v
[Self-Attention (Transformer, 2017)]
    |
    v
[Multi-Head + Masked Self-Attention (GPT)]
    |
    v
[Efficient Attention (Linformer, 2020 — O(n))]
    |
    v
[현재: Flash Attention 2/3 — 메모리 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Self-Attention은 교실에서 **모든 친구의 얼굴을 보면서** 관계를 파악하는 거예요.
2. "고양이가 매트 위에 앉았다"에서 "앉았다"는 **"고양이"와 "매트"를 더 많이** 봐요.
3. 이 방법 덕분에 AI가 <strong>문장의 뜻을 정확하게 이해</strong>할 수 있답니다!
