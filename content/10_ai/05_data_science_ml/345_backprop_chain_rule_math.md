---
title: "Backpropagation"
date: "2026-05-09"
tags:
  - "studynote-ai"
weight: 345
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 역전파 (Backpropagation) 는 연쇄 법칙 (Chain Rule) 을 계산 그래프 (Computational Graph) 에 적용해, 손실 함수의 각 파라미터에 대한 편미분 ∂L/∂w 를 출력층에서 입력층 방향으로 효율적으로 계산하는 알고리즘이다.
> 2. **가치**: 역전파 없이는 파라미터 수가 수십억 개인 LLM (Large Language Model) 의 학습이 불가능하며, 자동 미분 (Autograd) 엔진 (PyTorch, TensorFlow) 은 모두 역전파를 자동화한 것이다.
> 3. **판단 포인트**: 수치 미분 (Numerical Gradient) 은 O(d) 번 순전파가 필요해 O(d) 비용이지만, 역전파는 단 한 번의 역방향 패스로 모든 편미분을 O(1) 비율로 계산한다는 계산 복잡도 차이를 명시해야 한다.

---

## Ⅰ. 개요 및 필요성

### 역전파의 등장 배경

경사 하강법 (Gradient Descent) 으로 신경망을 학습하려면 모든 파라미터에 대한 손실 함수의 편미분이 필요하다. 파라미터 수 d 에 대해:

| 방법 | 계산 방식 | 비용 | 한계 |
|:---|:---|:---:|:---|
| 수치 미분 (Numerical Gradient) | (f(w+ε)-f(w-ε))/2ε | O(d) | 파라미터 1개당 2번 순전파 |
| 기호 미분 (Symbolic Differentiation) | 수식 표현 | O(d) | 중간 수식 폭발적 증가 |
| 역전파 (Backpropagation) | 계산 그래프 역방향 | O(1)* | 한 번으로 모든 편미분 |

*전체 비용은 O(순전파 비용) 의 상수 배

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 역전파는 "모든 사원의 성과급을 계산할 때, 각 사원을 하나씩 회의실에 불러 따로 평가하는(수치 미분) 대신, 전체 회의에서 한 번에 책임 분담을 계산하는(역전파)" 방법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 연쇄 법칙 (Chain Rule) 기본

```
  합성 함수 y = f(g(x)) 의 미분:
  dy/dx = (dy/dg) · (dg/dx)

  다변수 체인 룰:
  ∂L/∂w = ∂L/∂z · ∂z/∂w   (z = wx + b)

  실제 수식:
  z = wx + b -> ∂z/∂w = x
  a = σ(z)   -> ∂a/∂z = σ'(z)
  L = loss(a)-> ∂L/∂a = loss'(a)

  따라서: ∂L/∂w = ∂L/∂a · ∂a/∂z · ∂z/∂w
                = loss'(a) · σ'(z) · x
```

### 계산 그래프 (Computational Graph) 와 역전파

```
  순전파 (Forward Pass): 좌 -> 우
  역전파 (Backward Pass): 우 -> 좌

  x --->[× w]---> z --->[σ]---> a --->[L]---> Loss
  ^             ^            ^           |
  w             w            a           |
                ^            ^           v
                |    역전파   | ∂L/∂a <---+
                |            |
  ∂L/∂w <-------|------------+
       = ∂L/∂z · ∂z/∂w
       = (∂L/∂a · σ'(z)) · x

  계산 그래프 노드별 역전파 규칙:
  +---------------------------------------------------+
  |  덧셈 노드: 기울기를 그대로 양 쪽으로 분배          |
  |  곱셈 노드: 기울기 × 상대방 입력값 (교차 곱)       |
  |  활성화 노드: 기울기 × 활성화 함수 도함수           |
  +---------------------------------------------------+
```

### 2층 신경망 전체 역전파 수식 전개

```
  구조: x -> [Linear 1] -> h -> [ReLU] -> a -> [Linear 2] -> y -> [MSE] -> L

  Forward:
  h₁ = W₁x + b₁
  a₁ = ReLU(h₁)
  y = W₂a₁ + b₂
  L = (1/2)(y - t)^   (t: 정답)

  Backward (연쇄 법칙):
  δL/δy = y - t                         (MSE 도함수)
  δL/δW₂ = δL/δy · a₁ᵀ               (Linear 2)
  δL/δa₁ = W₂ᵀ · δL/δy               (a₁ 기울기)
  δL/δh₁ = δL/δa₁ ⊙ ReLU'(h₁)        (ReLU 역전파)
  δL/δW₁ = δL/δh₁ · xᵀ              (Linear 1)
  δL/δb₁ = δL/δh₁                    (bias 기울기)
```

### 수치 미분 vs 자동 미분 비교

```
  수치 미분 (Numerical Gradient) 검증:
  ∂L/∂wᵢ ≈ [L(w + εeᵢ) - L(w - εeᵢ)] / (2ε)
  비용: 파라미터 d 개 × 2번 순전파 = O(d)
  활용: 역전파 구현 검증 (Gradient Check)

  자동 미분 (Autograd):
  PyTorch: tensor.backward() -> .grad 자동 계산
  JAX: jax.grad(loss_fn)(params)
  비용: 역전파 1회 = O(순전파 비용의 ~3배)
```

- **📢 섹션 요약 비유**: 역전파의 연쇄 법칙은 "공장 라인에서 불량 원인을 역추적할 때, 최종 불량품에서 시작해 각 공정의 기여도를 뒤로 거슬러 계산하는" 불량 원인 분석이다.

---

## Ⅲ. 비교 및 연결

### Forward Mode vs Reverse Mode 자동 미분

| 항목 | Forward Mode | Reverse Mode (역전파) |
|:---|:---|:---|
| 계산 방향 | 입력 -> 출력 | 출력 -> 입력 |
| 비용 | O(d) — 입력 차원 | O(1) — 출력 차원 |
| 유리한 경우 | 출력 차원 >> 입력 차원 | 입력 차원 >> 출력 차원 |
| 딥러닝 적용 | 비적합 (파라미터 수 방대) | 적합 (손실 = 스칼라 1개) |

- **📢 섹션 요약 비유**: Forward vs Reverse Mode 는 "여러 도시에서 한 목적지까지의 최단 경로 계산" 에서 "각 도시에서 출발하는 경우(Forward, 비효율)" vs "목적지에서 거꾸로 계산(Reverse, 역전파, 효율)" 의 차이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### PyTorch Autograd 활용 예시

```python
import torch

# 파라미터 정의 (requires_grad=True)
w = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
x = torch.tensor([1.0, 2.0])

# 순전파
z = w @ x      # 행렬-벡터 곱
loss = z.sum()

# 역전파 (연쇄 법칙 자동 적용)
loss.backward()

print(w.grad)  # ∂loss/∂w 자동 계산

# 수치 미분으로 검증 (Gradient Check)
eps = 1e-5
for i in range(w.shape[0]):
    for j in range(w.shape[1]):
        w_plus = w.detach().clone(); w_plus[i,j] += eps
        w_minus = w.detach().clone(); w_minus[i,j] -= eps
        numerical = ((w_plus @ x).sum() - (w_minus @ x).sum()) / (2*eps)
        print(f"w[{i},{j}]: analytic={w.grad[i,j]:.4f}, numerical={numerical:.4f}")
```

### 학습 주제 포인트

- 연쇄 법칙 수식: ∂L/∂w = ∂L/∂z · ∂z/∂w 와 구체적 전개
- 계산 그래프 노드별 역전파 규칙 (덧셈: 분배, 곱셈: 교차 곱)
- 역전파 비용 O(순전파 비용의 상수 배) 대 수치 미분 O(d) 비교
- Autograd 와 역전파의 관계: 동적 계산 그래프 (PyTorch) vs 정적 (TensorFlow 1.x)
- Gradient Check 원리: 수치 미분으로 역전파 구현 검증

- **📢 섹션 요약 비유**: 역전파는 "수천 명 직원 중 누가 프로젝트 성공에 얼마나 기여했는지, CEO 피드백 한 번으로 전 직원에게 즉시 배분하는" 인사 평가 시스템이다. 각자 따로 평가하면 수천 배 오래 걸린다.

---

## Ⅴ. 기대효과 및 결론

- **효율성**: 파라미터 수와 무관하게 단 한 번의 역방향 패스로 모든 기울기 계산
- **자동화**: PyTorch Autograd, TensorFlow GradientTape 로 구현 자동화
- **범용성**: 어떤 미분 가능한 연산 조합에도 적용 가능
- **한계**: 미분 불가 연산 (argmax 등) 에는 Straight-Through Estimator 등 근사 필요

역전파는 현대 딥러닝 학습의 수학적 엔진이다. 심화 학습에서는 연쇄 법칙 수식 전개, 계산 그래프 역전파 규칙, 수치 미분과의 복잡도 비교, Autograd 와의 관계를 체계적으로 서술하면 고득점 가능하다.

- **📢 섹션 요약 비유**: 역전파는 "지구 온난화에서 각 나라·산업의 책임을 추적하는 것처럼, 최종 오차(지구 온도 상승)에서 출발해 각 파라미터(각 배출원)의 기여도를 정확히 역추적"하는 책임 분석 엔진이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연쇄 법칙 (Chain Rule) | 합성 함수, 편미분 / 역전파의 수학적 기반 |
| 계산 그래프 | 노드, 엣지, 순전파 / 역전파 구조 표현 도구 |
| 수치 미분 (Numerical Gradient) | ε, Gradient Check / 역전파 검증 방법 |
| Autograd | PyTorch, TensorFlow / 역전파 자동화 엔진 |
| 기울기 소실 | Sigmoid 도함수 0.25 / 역전파 적용 시 주의 사항 |
| Forward Mode AD | Jacobian-Vector Product / 역전파의 대안 (연구용) |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] -> [역전파 편미분 (Backpropagation)] -> [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 🎯 역전파는 "축구 시합에서 진 이유를 찾을 때, 최종 결과(패배)에서 거꾸로 각 선수(파라미터)의 잘못을 계산하는" 방법이에요.
2. ⛓️ 연쇄 법칙은 "A 가 B 를 움직이고, B 가 C 를 움직이면, A 가 C 에 미치는 영향 = A->B 영향 × B->C 영향" 이에요.
3. 🤖 PyTorch 는 이걸 자동으로 해줘서, 우리가 직접 계산하지 않아도 돼요!
