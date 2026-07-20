---
title: "Vanishing/Exploding Gradient"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 380
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기울기 소실 (Vanishing Gradient)은 역전파 시 깊은 레이어로 갈수록 기울기가 0에 수렴하고, 기울기 폭발 (Exploding Gradient)은 기울기가 지수적으로 커지는 현상으로 깊은 신경망 학습을 방해한다.
> 2. **가치**: Kaiming He 초기화 (Kaiming He Initialization)는 ReLU (Rectified Linear Unit) 계열 활성화 함수의 특성을 반영해 각 레이어 출력의 분산을 일정하게 유지하여 이 문제를 구조적으로 해결한다.
> 3. **판단 포인트**: ReLU는 Kaiming/He 초기화, Sigmoid·Tanh는 Xavier/Glorot 초기화가 표준이며, 잔차 연결 (Residual Connection)과 배치 정규화 (Batch Normalization)를 병행하면 수백 레이어 학습이 가능하다.

---

## Ⅰ. 개요 및 필요성

역전파 (Backpropagation)에서 기울기는 연쇄 법칙 (Chain Rule)으로 계산된다:

```
∂L/∂W₁ = ∂L/∂aₙ · ∂aₙ/∂aₙ₋₁ · ... · ∂a₂/∂a₁ · ∂a₁/∂W₁
```

L번의 행렬-벡터 곱이 연속되면, 각 활성화 도함수의 절댓값이 1보다 작으면 0으로(소실), 1보다 크면 ∞로(폭발) 수렴한다. Sigmoid의 최대 도함수 = 0.25이므로 깊은 네트워크에서 필연적으로 소실된다.

- **📢 섹션 요약 비유**: 전화기 여러 대를 거쳐 속삭이기(기울기)를 전달하면, 10명만 거쳐도 아무 말도 안 들린다(소실). 반대로 스피커를 여러 번 증폭하면 귀가 찢어진다(폭발).

---

## Ⅱ. 아키텍처 및 핵심 원리

### 소실/폭발 발생 조건

```
기울기 = Π_{l=1}^{L} W_l · σ'(z_l)

σ'(Sigmoid) ≤ 0.25  -> L층 후 기울기 ≤ (0.25)^L ≈ 0
σ'(ReLU)    = 1(x>0), 0(x≤0) -> 소실 최소화 (Dead Neuron 문제 있음)
```

### Kaiming He 초기화

He et al. (2015) - "Delving Deep into Rectifiers" 논문:

ReLU의 경우 음수 입력이 모두 0이므로 <strong>활성화 분산이 입력 분산의 절반</strong>이 된다.

```
Xavier 초기화 (Sigmoid/Tanh):
W ~ N(0, 2/(nᵢₙ + nₒᵤₜ))

Kaiming He 초기화 (ReLU):
W ~ N(0, 2/nᵢₙ)    <- 분모가 2배 작음

nᵢₙ = 현재 레이어의 입력 차원 수 (fan-in)
```

```
+--------------------------------------------------+
|  분산 유지 체인 (Variance Propagation)            |
|                                                  |
|  입력 Var=1  ->  W ~ N(0, 2/n)  ->  ReLU          |
|  -> 출력 Var ≈ 1  ->  다음 레이어로 전달           |
|                                                  |
|  Kaiming 없이:  Var -> 0 또는 -> ∞                 |
|  Kaiming 적용:  Var ≈ 1 안정적 유지              |
+--------------------------------------------------+
```

| 초기화 | 활성화 함수 | 분산 공식 | 비고 |
|:---|:---|:---|:---|
| Kaiming He | ReLU, Leaky ReLU | 2/nᵢₙ | 현대 표준 |
| Xavier/Glorot | Sigmoid, Tanh | 2/(nᵢₙ+nₒᵤₜ) | 고전 표준 |
| LeCun | SELU | 1/nᵢₙ | 자기 정규화 |
| 상수(0) | - | 0 | 모든 뉴런 동일 학습, 사용 금지 |

### 추가 해결책

- <strong>잔차 연결 (Residual Connection, ResNet)</strong>: F(x) + x -> 기울기 고속도로
- <strong>배치 정규화 (Batch Normalization)</strong>: 중간 활성화 정규화로 안정화
- <strong>기울기 클리핑 (Gradient Clipping)</strong>: 폭발 방지, RNN에서 주로 사용
- <strong>LSTM/GRU</strong>: 게이트 구조로 장기 의존성 보존

- **📢 섹션 요약 비유**: Kaiming 초기화는 "스피커 볼륨을 처음부터 정확히 맞춰서 신호가 너무 작아지거나 너무 커지지 않도록" 세팅하는 것이다.

---

## Ⅲ. 비교 및 연결

| 문제 | 증상 | 주요 해결책 |
|:---|:---|:---|
| 기울기 소실 | 초기 레이어 학습 없음 | Kaiming 초기화, ResNet, BN |
| 기울기 폭발 | 손실 NaN, 불안정 | 클리핑, 학습률 감소 |
| Dead Neuron | ReLU 출력 항상 0 | Leaky ReLU, ELU |

- **📢 섹션 요약 비유**: Kaiming 초기화는 건물의 기초 공사다. 처음부터 기초를 제대로 놓아야 100층 건물(깊은 네트워크)도 안전하게 세울 수 있다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**PyTorch 기본값**: Kaiming Uniform 초기화 (`nn.Linear`, `nn.Conv2d`)
**TensorFlow/Keras 기본값**: Glorot Uniform (Xavier)

깊은 CNN 설계 시 BatchNorm + ReLU + Kaiming 삼박자가 표준이다. 트랜스포머는 LayerNorm을 사용하며 잔차 연결로 기울기 소실을 방지한다.

실무자 판단: 학습 초반 손실이 전혀 감소하지 않으면 -> 기울기 소실 의심 -> 초기화 방법, 활성화 함수, 네트워크 깊이 점검.

- **📢 섹션 요약 비유**: 기울기 클리핑은 "자동차 최고 속도 제한기"다. 폭발적으로 빠른 기울기를 제한해 안전한 학습을 보장한다.

---

## Ⅴ. 기대효과 및 결론

Kaiming He 초기화는 ReLU 기반 딥러닝의 필수 설정으로, ResNet이 152층 학습을 가능하게 한 핵심 요소 중 하나다. 기울기 소실/폭발 문제의 이론적 이해는 새로운 아키텍처 설계와 학습 실패 디버깅의 핵심 역량이다.

- **📢 섹션 요약 비유**: Kaiming 초기화는 딥러닝의 "출발선 세팅"이다. 올바른 출발선에서 시작해야 아무리 긴 레이스(깊은 네트워크)도 완주할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 기울기 소실 | Sigmoid, 깊은 네트워크 / 학습 불가 원인 |
| 기울기 폭발 | 큰 가중치, RNN / 손실 발산 원인 |
| Kaiming He 초기화 | ReLU, 2/nᵢₙ / 분산 보존 초기화 |
| Xavier 초기화 | Sigmoid, Tanh / 고전 분산 보존 |
| 잔차 연결 | ResNet, Skip Connection / 기울기 고속도로 |
| 기울기 클리핑 | 임계값, RNN / 폭발 방지 |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [기울기 소실/폭발 (Vanishing/Exploding Gradient)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 기울기 소실은 "전화 메시지가 10명을 거치면 아무도 원래 말을 못 알아듣는" 상황이야.
2. Kaiming 초기화는 "마이크 볼륨을 처음부터 딱 맞게 설정해서 모든 방에 선명하게 들리게 하는 것"이야.
3. 잔차 연결은 "중간 전화 연결을 생략하고 직통 전화선을 연결"하는 것처럼 기울기가 빠르게 전달되게 해줘.
