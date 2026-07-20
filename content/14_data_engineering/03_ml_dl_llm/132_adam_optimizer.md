---
title: "Adam Optimizer"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 132
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Adam(Adaptive Moment Estimation)은 <strong>Momentum(1차 모멘트, 이동 평균) + RMSProp(2차 모멘트, 기울기 제곱 이동 평균)</strong>을 결합한 적응형 옵티마이저이며, 파라미터별로 <strong>학습률을 자동 조정</strong>한다.
> 2. **가치**: SGD는 모든 파라미터에 같은 학습률을 적용하여 **희소 기울기·비등방 공간에서 수렴이 느리지만**, Adam은 각 파라미터에 적합한 학습률을 자동 계산하여 <strong>빠르고 안정적</strong>으로 수렴한다.
> 3. **판단 포인트**: AdamW(Weight Decay 분리)가 Transformer 학습의 사실상 표준이며, β₁=0.9·β₂=0.999·lr=1e-3이 기본 하이퍼파라미터이다.

---

## Ⅰ. 개요 및 필요성

```text
Adam = Momentum + RMSProp
  m = β₁·m + (1-β₁)·g      (1차 모멘트, 방향)
  v = β₂·v + (1-β₂)·g^     (2차 모멘트, 크기)
  θ = θ - lr · m̂/√(v̂+ε)    (업데이트)
```

- **📢 섹션 요약 비유**: Adam은 <strong>내비게이션</strong>이다. 방향(Momentum)과 속도(RMSProp)를 자동으로 조절하여 목적지(최솟값)에 빠르게 도착한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | SGD | Adam |
|:---|:---|:---|
| <strong>학습률</strong> | 고정 | **적응형** |
| **방향** | 현재 기울기 | **이동 평균 (안정)** |
| **수렴** | 느림 | **빠름** |

---

## Ⅲ~Ⅴ. 결론

Adam/AdamW는 <strong>딥러닝 학습의 사실상 표준 옵티마이저</strong>이며, Transformer·LLM 학습에 필수이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Adam</strong> | Momentum + RMSProp |
| **AdamW** | Weight Decay 분리 |
| <strong>Learning Rate</strong> | 학습 보폭 |
| <strong>Cosine Annealing</strong> | LR 스케줄러 |
| **Lion** | 차세대 옵티마이저 |

### 📈 관련 키워드 및 발전 흐름도

```text
[SGD (1951)] -> [Momentum (1964)] -> [AdaGrad (2011)]
    -> [RMSProp (2012)] -> [Adam (2014)]
    -> [AdamW (2018)] -> [현재: Lion·Sophia — 메모리 효율^]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Adam은 <strong>내비게이션</strong>이에요. 방향과 속도를 **자동으로** 조절해줘요.
2. SGD는 지도 없이 걷기(느림), Adam은 <strong>내비 따라 운전하기(빠름)</strong>예요.
3. 거의 모든 AI 학습에서 <strong>Adam이 기본 설정</strong>으로 쓰인답니다!
