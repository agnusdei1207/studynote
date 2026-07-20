---
title: "Global Minimum"
date: "2026-04-10"
tags:
  - "studynote-ai"
weight: 83
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Loss Function (손실 함수)을 최소화하는 최적화는 단순히 낮은 점 하나를 찾는 일이 아니라, 복잡한 지형에서 좋은 골짜기를 찾는 일이다.
- **가치**: SGD (Stochastic Gradient Descent), Adam (Adaptive Moment Estimation), BN (Batch Normalization) 같은 기법은 노이즈, 관성, 평탄화로 saddle point와 sharp minima의 함정을 줄인다.
- **판단 포인트**: 딥러닝에서는 global minimum을 무조건 추구하기보다, 일반화가 좋은 flat minima를 찾는 것이 더 중요하며, local minima보다 saddle point가 더 큰 문제인 경우가 많다.

---

## Ⅰ. 개요 및 필요성

경사하강법 (Gradient Descent)은 손실 함수의 기울기를 따라 파라미터를 갱신해 더 낮은 지점으로 이동하는 방법이다. 하지만 신경망의 손실 공간은 단순한 1차원 골짜기가 아니라, 수많은 봉우리와 골짜기, 평평한 구간이 섞인 고차원 지형이다. 그래서 지역 최솟값 (Local Minima)과 전역 최솟값 (Global Minimum)을 구분해야 한다.

지역 최솟값은 주변보다 낮지만 전체에서는 가장 낮지 않을 수 있는 지점이고, 전역 최솟값은 전체 손실 공간에서 가장 낮은 지점이다. 문제는 딥러닝에서는 진짜 나쁜 local minima보다 saddle point가 더 자주 발목을 잡는다는 점이다. 어떤 방향으로는 내려가고 다른 방향으로는 올라가는 지점에서는 기울기가 작아 보여도 오래 머물 수 있다.

```text
loss
 ^              /
 |     /
 |    /  \__        saddle point
 | __/       \___    local minimum
 |/              \__  global minimum
 +-----------------------------> parameter
```

따라서 최적화의 핵심은 "가장 낮은 점" 하나를 집착적으로 찾는 것이 아니라, 충분히 좋은 지점으로 안정적으로 수렴하는 것이다. 이 관점이 있어야 학습률, 배치 크기, 정규화 전략을 제대로 판단할 수 있다.

- **📢 섹션 요약 비유**: 산길을 걷는다고 생각하면 된다. 가장 낮은 웅덩이만 찾는 것이 아니라, 넘어지지 않고 끝까지 갈 수 있는 길을 찾는 것이 더 중요하다.

## Ⅱ. 아키텍처 및 핵심 원리

Loss Function은 모델이 얼마나 틀렸는지를 숫자로 나타내고, Gradient Descent는 그 값을 줄이기 위해 파라미터를 조금씩 조정한다. 고차원 공간에서는 기울기 정보가 완벽하지 않기 때문에, 노이즈와 보조 기법이 학습에 도움이 된다.

| 기법 | 핵심 작동 원리 | 기대 효과 |
| :--- | :--- | :--- |
| SGD (Stochastic Gradient Descent) | 미니배치 노이즈를 이용해 이동 | saddle point 탈출, 탐색성 증가 |
| Momentum | 이전 방향의 관성을 유지 | 진동 감소, 완만한 이동 |
| Adam (Adaptive Moment Estimation) | 1차/2차 모멘트를 이용해 보폭 조정 | 빠른 수렴, 파라미터별 적응 |
| Learning Rate Scheduling | 학습률을 단계적으로 조정 | 초반 탐색, 후반 미세 조정 |
| BN (Batch Normalization) | 입력 분포를 정규화해 지형을 평탄화 | 안정적 학습, 기울기 전달 개선 |

```text
기울기 v
+--------------+
| noisy step   |  SGD의 흔들림
+------+-------+
       v
+--------------+
| momentum     |  방향 관성
+------+-------+
       v
+--------------+
| adaptive step|  Adam의 적응 보폭
+--------------+
```

SGD는 노이즈 덕분에 좁은 골짜기에 갇히지 않는 장점이 있고, Momentum은 지그재그를 줄이며, Adam은 파라미터마다 다른 보폭을 준다. BN은 입력 분포를 안정화해 손실 지형을 덜 거칠게 만들어 준다.

결국 이 기법들은 모두 "더 낮은 곳"을 찾기 위한 것이면서도, 동시에 "덜 위험한 곳"으로 이동하기 위한 장치다.

- **📢 섹션 요약 비유**: 눈을 가리고 미끄러운 산을 내려갈 때, 친구가 살짝 등을 밀어 주거나 걸음을 조절해 주면 같은 길도 훨씬 안전해진다.

## Ⅲ. 비교 및 연결

Local minima, global minimum, saddle point는 서로 다르게 다뤄야 한다. local minima는 주변보다 낮은 고점처럼 보이지만, 실제로는 충분히 좋은 해가 될 수 있다. saddle point는 어떤 방향은 내려가고 어떤 방향은 올라가므로, 기울기 정보만 보면 멈춘 것처럼 보이기 쉽다. deep learning에서는 이 saddle point가 더 큰 문제다.

| 지형 | 특징 | 실무 의미 |
| :--- | :--- | :--- |
| Local Minima | 주변보다 낮지만 전체 최저는 아님 | 대부분은 괜찮은 해일 수 있음 |
| Global Minimum | 전체에서 가장 낮음 | 꼭 찾아야만 좋은 것은 아님 |
| Saddle Point | 한쪽은 올라가고 한쪽은 내려감 | 학습 정체의 주요 원인 |
| Sharp Minima | 골이 좁고 예민함 | 훈련 손실은 낮아도 일반화가 나쁠 수 있음 |
| Flat Minima | 골이 완만함 | 잡음에 강하고 일반화가 좋을 가능성 큼 |

좋은 모델은 training loss가 가장 낮은 모델이 아니라 validation 성능이 안정적인 모델이다. 그래서 sharp minima를 무조건 선호하면 안 되고, flat minima 쪽이 일반화에 유리한 경우가 많다.

경사하강법의 종류도 비교해 볼 수 있다. full-batch 방식은 안정적이지만 탐색성이 약하고, SGD는 노이즈가 있어 탈출에 유리하다. 그래서 실제 딥러닝은 계산 효율과 탐색성의 균형을 맞추기 위해 미니배치 기반의 SGD 계열을 사용한다.

- **📢 섹션 요약 비유**: 같은 방을 찾더라도 좁고 날카로운 쪽보다 넓고 완만한 쪽이 오래 머물기 좋다. 딥러닝도 너무 뾰족한 골짜기보다 넉넉한 골짜기를 좋아한다.

## Ⅳ. 실무 적용 및 실무자 판단

학습이 잘 안 될 때는 먼저 loss landscape의 문제인지, 하이퍼파라미터의 문제인지, 데이터의 문제인지 나눠 봐야 한다. 예를 들어 학습률이 너무 크면 발산하고, 너무 작으면 saddle point에서 오래 머물 수 있다. 따라서 학습률 조정과 모멘텀 설정이 가장 먼저 점검할 항목이다.

### 적용 기준

1. 초반 수렴이 느리면 SGD 계열에서 학습률과 Momentum을 함께 본다.
2. 진동이 심하면 Learning Rate Scheduling으로 후반 보폭을 줄인다.
3. 배치가 너무 작아 흔들리면 BN이나 배치 크기 조정을 고려한다.
4. 훈련 손실만 낮고 검증 성능이 나쁘면 sharp minima 또는 과적합을 의심한다.
5. global minimum 집착보다 generalization 중심으로 판단한다.

### 안티패턴

- training loss만 보고 모델이 최고라고 판단하기
- 너무 큰 batch로 노이즈를 없애서 saddle point 탈출성을 약화시키기
- 학습률을 끝까지 고정하기
- validation 성능이 떨어지는데도 훈련 손실만 줄이기

학습 정리에서는 "딥러닝 최적화의 핵심은 global minimum 추적이 아니라, saddle point를 피하고 flat minima에 수렴해 일반화를 확보하는 것"이라고 정리하면 좋다. 이 문장이 문제의 본질을 잘 압축한다.

- **📢 섹션 요약 비유**: 시험장에서 만점을 한 문제만 오래 붙잡는다고 전체 성적이 오르지 않는다. 먼저 막힌 문제를 넘기고, 전체 점수가 잘 나오게 해야 한다.

## Ⅴ. 기대효과 및 결론

좋은 최적화는 단순히 낮은 손실이 아니라 안정적인 일반화를 만든다. 따라서 딥러닝에서는 local minima보다 saddle point와 sharp minima의 위험을 더 의식해야 한다. SGD, Momentum, Adam, Learning Rate Scheduling, BN은 모두 그 위험을 줄이는 도구다.

결론적으로 최적화는 "가장 낮은 점을 찾는 산수"가 아니라 "학습이 잘 끝나고 새 데이터에도 잘 맞는 지점을 찾는 탐색"이다. 이 시각을 가지면 알고리즘 선택과 하이퍼파라미터 조정의 이유가 분명해진다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Loss Function | 최소화 대상 |
| Gradient Descent | 기울기 기반 갱신 |
| SGD (Stochastic Gradient Descent) | 노이즈를 이용한 탐색 |
| Momentum | 관성 기반 보조 |
| Adam (Adaptive Moment Estimation) | 적응형 학습률 |
| BN (Batch Normalization) | 손실 지형 평탄화 |
| Sharp / Flat Minima | 일반화 품질 차이 |

### 📈 관련 키워드 및 발전 흐름도

```text
Loss Function
    |
    v
Gradient Descent
    |
    +---------------> SGD (Stochastic Gradient Descent)
    |
    +---------------> Momentum
    |
    +---------------> Adam (Adaptive Moment Estimation)
    |
    +---------------> BN (Batch Normalization)
```

이 흐름은 "문제 정의 -> 탐색 -> 탈출 보조 -> 수렴 안정화"로 최적화 전략이 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 언덕에서 공을 굴릴 때는 낮은 곳으로 가려고 해요.
2. 그런데 중간에 멈추거나, 좁고 날카로운 곳에 빠질 수 있어요.
3. 그래서 컴퓨터는 살짝 흔들어 주고, 걸음도 조절하면서 더 좋은 자리를 찾는답니다.
