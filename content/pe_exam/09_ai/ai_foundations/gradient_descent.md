+++
title = "Gradient Descent (경사하강법)"
date = 2026-03-03

[extra]
categories = "pe_exam-ai"
+++

# Gradient Descent (경사하강법)

## 핵심 인사이트 (3줄 요약)
> 경사하강법은 손실 함수의 기울기를 따라 파라미터를 점진적으로 최적화하는 알고리즘입니다.
> 딥러닝의 역전파(Backpropagation)와 결합하여 모든 신경망 학습의 기반이 됩니다.
> SGD, Adam, AdaGrad 등 다양한 변형이 존재하며, 적절한 선택이 모델 성능을 결정합니다.

---

### Ⅰ. 개요

**개념**: 경사하강법(Gradient Descent)은 손실 함수(Loss Function)를 최소화하기 위해 함수의 기울기(Gradient)의 반대 방향으로 파라미터를 반복적으로 업데이트하는 1차 최적화 알고리즘이다.

> 💡 **비유**: 경사하강법은 **산에서 눈을 가린 채로 가장 낮은 골짜기로 내려가는 것**과 같다. 발밑의 경사를 느끼고, 가장 가파르게 내려가는 쪽으로 한 발짝씩 이동한다. 반복하면 결국 가장 낮은 곳(최솟값)에 도달한다.

**등장 배경** (필수: 3가지 이상 기술):

1. **기존 문제점**: 복잡한 비선형 함수의 최솟값을 해석적으로 구하는 것이 불가능했다. 수학적 폐해(Closed-form) 해가 존재하지 않는 문제가 많았다.

2. **기술적 필요성**: 신경망과 같은 복잡한 모델의 파라미터(수백만~수조 개)를 최적화할 수 있는 효율적인 방법이 필요했다. 미분 가능한 모든 함수에 적용 가능한 범용 방법이 요구되었다.

3. **시장/산업 요구**: 머신러닝/딥러닝 모델의 학습 자동화가 필요했다. 대규모 데이터로부터 최적의 파라미터를 찾는 효율적 방법이 필수적이었다.

**핵심 목적**: 손실 함수 J(θ)를 최소화하는 최적의 파라미터 θ*를 찾는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (필수: 최소 4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **손실 함수 J(θ)** | 최적화할 목적 함수 | 파라미터의 오차를 측정 | 산의 높이 |
| **기울기 (Gradient)** | 손실 함수의 변화율 | ∇J(θ), 가장 가파른 상승 방향 | 산의 경사 |
| **학습률 (Learning Rate, η)** | 한 번에 이동하는 보폭 | 너무 크면 발산, 작으면 느림 | 발걸음 크기 |
| **파라미터 (θ)** | 최적화 대상 가중치 | 반복적으로 업데이트 | 현재 위치 |
| **반복 횟수 (Epoch)** | 업데이트 반복 횟수 | 충분히 수렴할 때까지 | 내려가는 횟수 |

**구조 다이어그램** (필수: ASCII 아트):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Gradient Descent Flow                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. 초기화                                              │
│         ↓                                                               │
│   ┌─────────────────────────────────────────────────────────────┐      │
│   │                     반복 (until 수렴)                        │      │
│   │  ┌─────────────────────────────────────────────────────┐    │      │
│   │  │  2. 순전파 (Forward Pass)                           │    │      │
│   │  │     ŷ = f(X; θ)                                    │    │      │
│   │  └─────────────────────────────────────────────────────┘    │      │
│   │         ↓                                                    │      │
│   │  ┌─────────────────────────────────────────────────────┐    │      │
│   │  │  3. 손실 계산                                       │    │      │
│   │  │     J(θ) = L(y, ŷ)                                  │    │      │
│   │  └─────────────────────────────────────────────────────┘    │      │
│   │         ↓                                                    │      │
│   │  ┌─────────────────────────────────────────────────────┐    │      │
│   │  │  4. 기울기 계산 (Backward Pass)                     │    │      │
│   │  │     ∇J(θ) = ∂J/∂θ                                   │    │      │
│   │  └─────────────────────────────────────────────────────┘    │      │
│   │         ↓                                                    │      │
│   │  ┌─────────────────────────────────────────────────────┐    │      │
│   │  │  5. 파라미터 업데이트                               │    │      │
│   │  │     θ = θ - η · ∇J(θ)                               │    │      │
│   │  └─────────────────────────────────────────────────────┘    │      │
│   └─────────────────────────────────────────────────────────────┘      │
│         ↓                                                               │
│   6. 수렴 확인 → 종료                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):

```
① 파라미터 초기화 → ② 손실 계산 → ③ 기울기 계산 → ④ 파라미터 업데이트 → ⑤ 반복
```

- **1단계 (초기화)**: 파라미터 θ를 무작위로 초기화 (Xavier, He 초기화 등)
- **2단계 (순전파)**: 입력 X에 대해 현재 θ로 예측 ŷ 계산
- **3단계 (손실 계산)**: 예측 ŷ과 실제 y 간의 오차 J(θ) 계산
- **4단계 (역전파)**: 연쇄 법칙으로 각 파라미터에 대한 기울기 ∇J(θ) 계산
- **5단계 (업데이트)**: θ = θ - η · ∇J(θ)로 파라미터 갱신
- **6단계 (수렴 확인)**: 기울기가 0에 가까워지거나, 최대 epoch 도달 시 종료

**핵심 알고리즘/공식** (해당 시 필수):

**기본 경사하강법**:
```
θ(t+1) = θ(t) - η · ∇J(θ(t))
```

**배치 경사하강법 (Batch GD)**: 전체 데이터 사용
```
∇J(θ) = (1/N) Σ ∇L(xᵢ, yᵢ; θ)
```

**확률적 경사하강법 (SGD)**: 단일 샘플 사용
```
θ(t+1) = θ(t) - η · ∇L(xᵢ, yᵢ; θ)
```

**미니배치 SGD**: 배치 크기 B 사용
```
∇J(θ) ≈ (1/B) Σ ∇L(xᵢ, yᵢ; θ), i ∈ batch
```

**코드 예시** (필수: Python 또는 의사코드):

```python
import numpy as np

class GradientDescent:
    """기본 경사하강법 구현"""

    def __init__(self, learning_rate=0.01, max_iters=1000, tol=1e-6):
        self.lr = learning_rate
        self.max_iters = max_iters
        self.tol = tol
        self.history = []

    def optimize(self, loss_fn, grad_fn, theta_init):
        """
        loss_fn: 손실 함수 J(θ)
        grad_fn: 기울기 함수 ∇J(θ)
        theta_init: 초기 파라미터
        """
        theta = theta_init.copy()

        for i in range(self.max_iters):
            # 손실 계산
            loss = loss_fn(theta)
            self.history.append(loss)

            # 기울기 계산
            gradient = grad_fn(theta)

            # 파라미터 업데이트
            theta_new = theta - self.lr * gradient

            # 수렴 확인
            if np.linalg.norm(theta_new - theta) < self.tol:
                print(f"Converged at iteration {i}")
                break

            theta = theta_new

        return theta


class SGD:
    """확률적 경사하강법 with Momentum"""

    def __init__(self, learning_rate=0.01, momentum=0.9):
        self.lr = learning_rate
        self.momentum = momentum
        self.velocity = None

    def step(self, params, grads):
        if self.velocity is None:
            self.velocity = np.zeros_like(params)

        # Momentum 업데이트
        self.velocity = self.momentum * self.velocity - self.lr * grads
        params += self.velocity

        return params


class Adam:
    """Adam Optimizer (Adaptive Moment Estimation)"""

    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = learning_rate
        self.beta1 = beta1  # 1차 모멘텀 감쇠율
        self.beta2 = beta2  # 2차 모멘텀 감쇠율
        self.epsilon = epsilon
        self.m = None  # 1차 모멘텀 (평균)
        self.v = None  # 2차 모멘텀 (분산)
        self.t = 0     # 타임스텝

    def step(self, params, grads):
        if self.m is None:
            self.m = np.zeros_like(params)
            self.v = np.zeros_like(params)

        self.t += 1

        # 1차 모멘텀 업데이트 (지수 이동 평균)
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads

        # 2차 모멘텀 업데이트 (제곱 그래디언트의 지수 이동 평균)
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grads ** 2)

        # 편향 보정 (Bias Correction)
        m_hat = self.m / (1 - self.beta1 ** self.t)
        v_hat = self.v / (1 - self.beta2 ** self.t)

        # 파라미터 업데이트
        params -= self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)

        return params


# 사용 예시: 선형 회귀
def linear_regression_example():
    # 데이터 생성
    np.random.seed(42)
    X = np.random.randn(100, 1)
    y = 3 * X + 2 + np.random.randn(100, 1) * 0.1

    # 손실 함수 (MSE)
    def loss_fn(theta):
        pred = X @ theta
        return np.mean((y - pred) ** 2)

    # 기울기 함수
    def grad_fn(theta):
        pred = X @ theta
        return -2 * X.T @ (y - pred) / len(X)

    # 경사하강법
    gd = GradientDescent(learning_rate=0.1, max_iters=100)
    theta_init = np.zeros((1, 1))
    theta_opt = gd.optimize(loss_fn, grad_fn, theta_init)

    print(f"Optimal theta: {theta_opt.flatten()}")  # [2.99, 1.99] 근처
    print(f"Final loss: {loss_fn(theta_opt):.6f}")

linear_regression_example()
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석** (필수: 최소 3개씩):

| 장점 | 단점 |
|-----|------|
| 모든 미분 가능한 함수에 적용 가능 | 지역 최솟값(Local Minima)에 갇힐 수 있음 |
| 구현이 간단하고 계산 효율적 | 학습률 선택이 어려움 (민감함) |
| 대규모 문제에 확장 가능 | 안장점(Saddle Point)에서 느린 수렴 |
| 병렬/분산 처리 용이 | 비볼록(Non-convex) 함수에서 보장 없음 |

**대안 기술 비교** (필수: 최소 2개 대안):

| 비교 항목 | SGD | Adam | AdaGrad | RMSProp |
|---------|-----|------|---------|---------|
| 핵심 특성 | 기본, 단순 | ★ 적응형, 모멘텀 | 적응형 학습률 | 지수 이동 평균 |
| 수렴 속도 | 느림 | ★ 빠름 | 점점 느려짐 | 빠름 |
| 하이퍼파라미터 | η | η, β₁, β₂ | η | η, γ |
| 희소 데이터 | 약함 | ★ 강함 | ★ 강함 | 강함 |
| 메모리 사용 | 낮음 | 중간 (2x) | 중간 | 중간 |
| 적합 환경 | 일반적 | ★ 딥러닝 표준 | 희소 데이터 | RNN |

> **★ 선택 기준**:
> - **SGD + Momentum**: 컴퓨터 비전, 수렴 품질 중시
> - **Adam**: NLP, 기본 선택, 빠른 학습
> - **AdaGrad**: 희소 특성이 많은 데이터

**학습률 스케줄링 기법**:

| 기법 | 공식 | 특징 |
|-----|------|------|
| Step Decay | η(t) = η₀ × γ^(t/s) | 주기적 감소 |
| Exponential Decay | η(t) = η₀ × e^(-kt) | 지수적 감소 |
| Cosine Annealing | η(t) = η_min + 0.5(η_max - η_min)(1 + cos(πt/T)) | 부드러운 감소 |
| Warmup | η(t) = η₀ × t/T_warmup | 초기 천천히 증가 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (필수: 3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **딥러닝 학습** | Adam + Learning Rate Warmup | 학습 속도 2~3배 향상 |
| **대규모 모델** | LAMB, LARS 등 분산 최적화 | 배치 크기 64K까지 확장 |
| **전이 학습** | 낮은 학습률로 Fine-tuning | 과적합 방지, 성능 10% 향상 |
| **하이퍼파라미터 튜닝** | Learning Rate Finder 사용 | 튜닝 시간 80% 단축 |

**실제 도입 사례** (필수: 구체적 기업/서비스):

- **사례 1: OpenAI GPT-4** - AdamW optimizer + Cosine Decay 사용. 1.8조 파라미터를 25,000 A100 GPU로 학습. Learning Rate Warmup으로 초기 학습 안정화.

- **사례 2: Google BERT** - Adam with Warmup (10,000 steps). Learning Rate 2e-5로 Fine-tuning. GLUE 벤치마크 SOTA 달성.

- **사례 3: Tesla FSD** - SGD + Momentum으로 컴퓨터 비전 모델 학습. 실시간 추론을 위한 경량 모델 최적화.

**도입 시 고려사항** (필수: 4가지 관점):

1. **기술적**: Learning Rate Finder로 적절한 η 탐색, Gradient Clipping으로 폭발 방지, Weight Decay로 정규화

2. **운영적**: 학습 곡선 모니터링 필수, Early Stopping으로 과적합 방지, Checkpoint로 재개 가능

3. **보안적**: 그래디언트 기반 공격(Adversarial) 방어 고려, Differential Privacy와 결합 가능

4. **경제적**: Adam은 SGD 대비 2배 메모리 사용, GPU 선택 시 고려, Learning Rate 스케줄링으로 학습 시간 단축

**주의사항 / 흔한 실수** (필수: 최소 3개):

- ❌ **너무 큰 학습률**: Loss가 발산함. 해결: Learning Rate Finder 사용, 1e-3부터 시작
- ❌ **학습률 Decay 누락**: 수렴이 느려짐. 해결: Cosine Decay 또는 Step Decay 적용
- ❌ **Gradient Clipping 미사용**: RNN에서 그래디언트 폭발. 해결: `torch.nn.utils.clip_grad_norm_` 사용
- ❌ **Adam의 Weight Decay 오해**: AdamW(L2 정규화 분리) 사용 권장

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):

```
┌─────────────────────────────────────────────────────────────────┐
│  Gradient Descent 핵심 연관 개념 맵                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [손실함수] ←──→ [Gradient Descent] ←──→ [역전파]              │
│        ↓                ↓                ↓                       │
│   [MSE/CrossEntropy]  [Adam/SGD]      [Chain Rule]              │
│        ↓                ↓                ↓                       │
│   [정규화] ←──→ [학습률 스케줄링] ←──→ [배치 정규화]             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| Backpropagation | 필수 연결 | 그래디언트 계산 알고리즘 | `[backpropagation](./backpropagation.md)` |
| Loss Function | 선행 개념 | 최적화할 목적 함수 | `[loss_function](./loss_function.md)` |
| Regularization | 병행 기술 | 과적합 방지 | `[regularization](./regularization.md)` |
| Batch Normalization | 학습 안정화 | 내부 공변량 변화 완화 | `[batch_norm](../deep_learning/batch_norm.md)` |
| Learning Rate Schedule | 기법 | 학습률 동적 조정 | `[lr_schedule](./lr_schedule.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과** (필수):

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 학습 속도 | Adam 등 최적화 기법 사용 | SGD 대비 2~5배 향상 |
| 수렴 품질 | 적절한 Learning Rate | Loss < 목표값 도달 |
| 메모리 효율 | SGD + Momentum | Adam 대비 50% 절감 |
| 일반화 성능 | Weight Decay + Scheduler | Test Accuracy 5% 향상 |

**미래 전망** (필수: 3가지 관점):

1. **기술 발전 방향**: 2차 최적화(K-FAC, Shampoo) 연구, 자동 하이퍼파라미터 튜닝(Meta-learning), 분산 최적화 개선

2. **시장 트렌드**: LLM 학습을 위한 대규모 분산 최적화가 핵심, ZeRO, FSDP 등 메모리 최적화 필수

3. **후속 기술**: Learning Rate 없는 최적화(AdaBound), Neural Optimizer, 최적화 자동화(AutoML)

> **결론**: 경사하강법은 딥러닝 학습의 핵심 알고리즘으로, 모든 신경망 최적화의 기반이다. 기술사로서 다양한 Optimizer의 특성을 이해하고, 문제에 맞는 최적화 기법을 선택하는 능력이 필수적이다.

> **※ 참고 표준**: Kingma & Ba (2015) "Adam: A Method for Stochastic Optimization", Robbins & Monro (1951) SGD 이론

---

## 어린이를 위한 종합 설명

경사하강법은 마치 **눈을 가진 채 산에서 가장 낮은 골짜기를 찾아 내려가는 것**과 같아요.

여러분이 산 위에 서 있다고 상상해 보세요. 눈을 가리고 있어서 주위가 안 보여요. 하지만 발밑의 경사는 느낄 수 있죠.

어떻게 가장 낮은 곳으로 갈 수 있을까요?

1. 발밑의 경사를 느껴요. 어느 쪽이 더 가파르게 내려가는지.
2. 가장 가파르게 내려가는 쪽으로 한 발짝 걸어요.
3. 다시 발밑의 경사를 느껴요.
4. 이걸 계속 반복해요!

이렇게 하면 결국 가장 낮은 골짜기에 도달할 수 있어요. 컴퓨터도 똑같이 해요!

- 산의 높이 = **손실 함수** (얼마나 틀렸는지)
- 경사 = **기울기** (어느 방향으로 가면 줄어드는지)
- 발걸음 크기 = **학습률** (한 번에 얼마나 이동할지)

학습률이 너무 크면 골짜기를 지나쳐서 계속 왔다 갔다 할 수 있어요. 너무 작으면 내려가는데 너무 오래 걸리고요. 적당한 발걸음 크기를 찾는 게 중요해요!
