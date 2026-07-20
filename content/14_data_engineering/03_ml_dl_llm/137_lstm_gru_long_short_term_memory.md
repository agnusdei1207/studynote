---
title: "Lstm Gru Long Short Term Memory"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 137
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LSTM(Long Short-Term Memory)은 <strong>Forget·Input·Output 3개의 게이트로 셀 상태(Cell State)를 제어</strong>하여 Vanilla RNN의 장기 의존성(Vanishing Gradient) 문제를 해결한 순환 신경망이며, GRU는 LSTM을 <strong>2개 게이트(Reset·Update)로 단순화</strong>한 경량 변형이다.
> 2. **가치**: RNN은 "어제 비가 왔다"는 기억하지만 "한 달 전 비가 왔다"는 잊지만, LSTM은 <strong>중요한 정보를 셀 상태에 장기 보존</strong>하여 먼 과거의 맥락도 활용한다.
> 3. **판단 포인트**: 성능은 LSTM≈GRU이나 GRU가 파라미터가 적어(학습 빠름) 소규모 데이터에 유리하며, 현재는 <strong>Transformer가 대부분 대체</strong>했으나 시계열·온디바이스에서 여전히 사용된다.

---

## Ⅰ. 개요 및 필요성

```text
LSTM 3 Gate:
  Forget: 어떤 정보를 버릴지 (sigmoid)
  Input:  어떤 정보를 저장할지 (sigmoid × tanh)
  Output: 어떤 정보를 출력할지 (sigmoid)
  Cell State: 정보 고속도로 (장기 기억)

GRU 2 Gate: Reset + Update (LSTM 단순화)
```

- **📢 섹션 요약 비유**: LSTM은 <strong>포스트잇 붙은 일기장</strong>이다. 중요한 페이지에 포스트잇(Gate)을 붙여서 잊지 않는다.

---

## Ⅱ~Ⅴ. 결론

LSTM/GRU는 <strong>시퀀스 모델링의 중요한 이정표</strong>이며, Transformer 이전의 NLP·음성·시계열 핵심 아키텍처였다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>LSTM</strong> | 3 Gate + Cell State |
| <strong>GRU</strong> | 2 Gate (경량) |
| <strong>Cell State</strong> | 장기 기억 고속도로 |
| <strong>Vanishing Gradient</strong> | RNN 문제 -> LSTM 해결 |
| <strong>Transformer</strong> | LSTM 대체 (병렬) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Vanilla RNN (1986)] -> [LSTM (Hochreiter, 1997)]
    -> [GRU (Cho, 2014)] -> [Seq2Seq+Attention (2014)]
    -> [Transformer (2017) — LSTM 대체]
    -> [현재: xLSTM/Mamba — LSTM 르네상스]
```

### 👶 어린이를 위한 3줄 비유 설명
1. LSTM은 <strong>포스트잇 붙은 일기장</strong>이에요. 중요한 페이지를 **잊지 않아요**.
2. RNN은 옛날 일기를 잊지만, LSTM은 <strong>포스트잇(Gate) 덕분에 기억</strong>해요.
3. GRU는 **포스트잇을 2개만 쓰는** 간단한 버전이에요!
