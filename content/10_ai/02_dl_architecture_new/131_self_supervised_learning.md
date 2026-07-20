---
title: "Self Supervised Learning"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 131
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Self-Supervised Learning(SSL)은 <strong>라벨 없는 데이터에서 데이터 자체로 학습 신호를 생성</strong>하는 방법이며, "다음 단어 예측(GPT)"·"빈칸 채우기(BERT)"가 대표적 pretext task이다.
> 2. **가치**: 라벨링은 비용이 높지만 비라벨 데이터는 무한하므로, SSL로 대규모 사전 학습 후 소량 라벨 데이터로 Fine-tuning하면 <strong>라벨 효율이 극대화</strong>된다.
> 3. **판단 포인트**: NLP(MLM·CLM)·Vision(Contrastive·MAE)·멀티모달(CLIP) 각 분야의 SSL 방식을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
지도 학습: 데이터+라벨 필요 (비쌈)
SSL: 데이터만 (무료), 라벨은 데이터 자체에서 생성
  NLP: "나는 [MASK] 이다" -> 학생 예측 (BERT)
  Vision: 이미지 일부 가림 -> 복원 (MAE)
```

- **📢 섹션 요약 비유**: SSL은 <strong>빈칸 채우기 시험</strong>이다. 선생님(라벨)이 정답을 알려주지 않아도 문장(데이터) 자체에서 정답을 유추한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 분야 | SSL 방식 | 대표 |
|:---|:---|:---|
| **NLP** | MLM, CLM | BERT, GPT |
| **Vision** | Contrastive, MAE | SimCLR, MAE |
| <strong>멀티모달</strong> | 이미지-텍스트 매칭 | <strong>CLIP</strong> |

---

## Ⅲ~Ⅴ. 결론

SSL은 <strong>Foundation Model의 핵심 학습 패러다임</strong>이며, 라벨 없는 대규모 데이터로 범용 표현을 학습하는 것이 현대 AI의 기본이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SSL** | 라벨 없이 학습 |
| <strong>MLM</strong> | 빈칸 채우기 (BERT) |
| **CLM** | 다음 단어 예측 (GPT) |
| **Contrastive** | 유사/비유사 쌍 학습 |
| <strong>CLIP</strong> | 이미지-텍스트 SSL |

### 📈 관련 키워드 및 발전 흐름도

```text
[지도 학습 (라벨 필수)] -> [Word2Vec SSL (2013)]
    -> [BERT MLM / GPT CLM (2018)] -> [SimCLR (2020, Vision SSL)]
    -> [CLIP (2021, 멀티모달)]
    -> [현재: DINO v2 / MAE — Vision SSL 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SSL은 <strong>빈칸 채우기 시험</strong>이에요. 선생님이 정답을 안 알려줘도 <strong>문장에서 유추</strong>해요.
2. "나는 ___ 이다"에서 "학생"을 **스스로 맞추는** 거예요.
3. 정답(라벨)이 없어도 **엄청 많은 문제를 풀면** AI가 똑똑해진답니다!
