---
title: "Nsp Next Sentence Prediction"
date: "2026-04-19"
tags:
  - "studynote-ai"
weight: 139
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NSP는 <strong>두 문장이 원래 연속된 문장인지(IsNext) 아닌지(NotNext)를 이진 분류</strong>하는 BERT의 두 번째 사전 학습 목표이며, 문장 간 관계(함의·모순·중립)를 학습한다.
> 2. **가치**: QA(질문-지문 관계)·NLI(자연어 추론)·문장 유사도 등 <strong>문장 쌍(Sentence Pair) 작업의 성능을 향상</strong>시키기 위해 설계되었다.
> 3. **판단 포인트**: RoBERTa(2019)는 <strong>NSP를 제거해도 성능이 같거나 높다</strong>는 것을 입증하여, 이후 모델(ALBERT·DeBERTa)에서는 NSP 대신 SOP(Sentence Order Prediction)를 사용하거나 제거했다.

---

## Ⅰ. 개요 및 필요성

```text
NSP 학습:
  [CLS] 문장A [SEP] 문장B [SEP]
  -> IsNext (50%): 원래 연속 문장
  -> NotNext (50%): 랜덤 다른 문서의 문장
  -> [CLS] 토큰으로 이진 분류
```

- **📢 섹션 요약 비유**: NSP는 <strong>연결된 퍼즐 조각인지 확인</strong>하는 것이다. 두 조각이 맞는지(IsNext) 아닌지(NotNext) 판별한다.

---

## Ⅱ~Ⅴ. 결론

NSP는 <strong>문장 관계 학습의 초기 기법</strong>이지만, RoBERTa 이후 효과가 의문시되어 SOP·제거가 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **NSP** | 문장 연속성 판별 |
| <strong>MLM</strong> | BERT의 1번째 목표 |
| **SOP** | ALBERT의 대안 |
| **RoBERTa** | NSP 제거 |
| **[CLS]** | 분류 토큰 |

### 📈 관련 키워드 및 발전 흐름도

```text
[BERT NSP (2018)] -> [RoBERTa: NSP 제거 (2019)]
    -> [ALBERT: SOP 대체 (2019)]
    -> [현재: 대부분 모델에서 NSP 미사용]
```

### 👶 어린이를 위한 3줄 비유 설명
1. NSP는 <strong>퍼즐 조각 맞추기</strong>예요. 두 조각이 **원래 붙어있었는지** 확인해요.
2. "비가 온다" 다음에 "우산을 쓴다"는 **맞지만(IsNext)**, "피자를 먹다"는 **안 맞아요(NotNext)**.
3. 나중에 연구해보니 **이 훈련이 없어도** 잘 해서, 요즘은 안 쓰기도 해요!
