---
title: "Loss Function Optimizer Gradient Descent"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 131
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 딥러닝 학습은 <strong>①손실 함수(Loss Function)로 예측과 정답의 차이를 측정</strong>하고, <strong>②경사 하강법(Gradient Descent)으로 손실을 줄이는 방향을 계산</strong>하며, <strong>③옵티마이저(Optimizer)가 가중치를 업데이트</strong>하는 3단계 순환이다.
> 2. **가치**: 이 3가지가 잘못되면 학습이 수렴하지 않거나(발산), 지역 최솟값에 갇히거나(과소적합), 과적합되므로 <strong>각 요소의 선택이 모델 성능을 직접 결정</strong>한다.
> 3. **판단 포인트**: 분류(Cross-Entropy), 회귀(MSE), 옵티마이저(Adam이 사실상 표준), 학습률 스케줄러(Cosine Annealing)가 현대 딥러닝의 표준 조합이다.

---

## Ⅰ. 개요 및 필요성

```text
학습 루프: 예측 -> 손실 계산 -> 역전파 -> 가중치 업데이트 -> 반복
  Loss: Cross-Entropy (분류), MSE (회귀)
  Optimizer: SGD -> Momentum -> Adam (표준)
```

- **📢 섹션 요약 비유**: 손실 함수는 **시험 채점**, 경사 하강법은 **"어떻게 공부하면 점수가 오를까" 방향 계산**, 옵티마이저는 <strong>실제 공부 전략</strong>이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 옵티마이저 | 특징 |
|:---|:---|
| **SGD** | 기본, 느림 |
| <strong>Momentum</strong> | 관성 추가, 진동v |
| <strong>Adam</strong> | <strong>Momentum+RMSProp, 표준</strong> |
| **AdamW** | Adam+Weight Decay |

---

## Ⅲ~Ⅴ. 결론

손실 함수·옵티마이저·경사 하강법은 <strong>딥러닝 학습의 핵심 엔진</strong>이며, Adam/AdamW가 현재 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Loss Function</strong> | 예측↔정답 차이 측정 |
| <strong>Gradient Descent</strong> | 손실 최소화 방향 |
| <strong>Adam</strong> | 적응형 옵티마이저 (표준) |
| <strong>Learning Rate</strong> | 학습 보폭 |
| <strong>Backpropagation</strong> | 역전파 (기울기 계산) |

### 📈 관련 키워드 및 발전 흐름도

```text
[SGD (1951)] -> [Momentum (1964)] -> [AdaGrad (2011)]
    -> [RMSProp (2012)] -> [Adam (2014) — 표준]
    -> [AdamW (2018)] -> [현재: Lion·Sophia — 차세대 옵티마이저]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 손실 함수는 <strong>시험 채점</strong>이에요. 틀린 게 많으면 점수(손실)가 높아요.
2. 경사 하강법은 **"어떻게 공부하면 점수가 오를까"** 방향을 알려줘요.
3. 옵티마이저(Adam)는 <strong>가장 효율적인 공부법</strong>이라 시험 점수가 빨리 올라요!
