---
title: "Regularization Dropout Batch Norm"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 134
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정규화(Regularization)는 <strong>모델이 학습 데이터에 과적합(Overfitting)하는 것을 방지</strong>하는 기법의 총칭이며, Dropout·BatchNorm·L1/L2·Data Augmentation·Early Stopping이 대표이다.
> 2. **가치**: 과적합 없이는 학습 정확도 99%인데 테스트 60%인 상황이 발생하며, 정규화로 <strong>일반화 성능(Generalization)</strong>을 확보해야 실제 데이터에서도 높은 성능을 발휘한다.
> 3. **판단 포인트**: Dropout(뉴런 랜덤 비활성화)·BatchNorm(층별 정규화)·Weight Decay(L2)가 현대 딥러닝의 3대 정규화이며, Transformer에서는 LayerNorm을 사용한다.

---

## Ⅰ. 개요 및 필요성

```text
Dropout:    학습 시 뉴런 랜덤 50% 비활성화
BatchNorm:  미니배치 단위로 평균 0·분산 1 정규화
L2 (Weight Decay): 가중치 크기 패널티
LayerNorm:  Transformer 표준 (배치 무관)
```

- **📢 섹션 요약 비유**: 정규화는 <strong>시험 전 다양한 문제집으로 연습</strong>하는 것이다. 한 문제집만 외우면(과적합) 새 시험에서 틀린다.

---

## Ⅱ~Ⅴ. 결론

정규화는 <strong>딥러닝 일반화 성능의 핵심</strong>이며, Dropout+BatchNorm/LayerNorm+Weight Decay가 표준 조합이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Dropout</strong> | 뉴런 랜덤 비활성화 |
| **BatchNorm** | 미니배치 정규화 |
| **LayerNorm** | Transformer 정규화 |
| <strong>Weight Decay</strong> | L2 정규화 |
| **과적합** | 정규화가 방지하는 대상 |

### 📈 관련 키워드 및 발전 흐름도

```text
[L1/L2 정규화 (전통)] -> [Dropout (2012, Hinton)]
    -> [BatchNorm (2015)] -> [LayerNorm (2016, Transformer)]
    -> [현재: RMSNorm (Llama) — 더 효율적 정규화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 과적합은 **한 문제집만 외우는** 거예요. 새 시험에서 틀려요.
2. 정규화는 <strong>다양한 문제집으로 연습</strong>하는 거예요. 어떤 시험이든 잘 봐요.
3. Dropout은 <strong>일부러 어려운 환경(뉴런 꺼짐)에서 연습</strong>해서 더 강해져요!
