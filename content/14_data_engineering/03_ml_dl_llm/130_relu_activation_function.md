---
title: "Relu Activation Function"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 130
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ReLU(Rectified Linear Unit)는 <strong>f(x) = max(0, x)</strong>로 정의되는 활성화 함수이며, 양수는 그대로 통과, 음수는 0으로 차단하는 단순한 구조로 <strong>Vanishing Gradient 문제를 해결</strong>하여 딥러닝을 실용화했다.
> 2. **가치**: Sigmoid의 기울기 소실로 깊은 신경망 학습이 불가능했던 한계를 ReLU가 극복하여 <strong>2012년 AlexNet의 ImageNet 우승</strong>을 이끌었다.
> 3. **판단 포인트**: Dead Neuron(음수 영역 영구 0) 문제가 있어 Leaky ReLU·PReLU·ELU 등 변형이 존재하며, Transformer에서는 GELU·SwiGLU가 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
ReLU: f(x) = max(0, x)
  x > 0 -> x (그대로), x ≤ 0 -> 0 (차단)
  기울기: x > 0 -> 1, x ≤ 0 -> 0
  -> Vanishing Gradient 없음 (기울기=1 유지)
```

- **📢 섹션 요약 비유**: ReLU는 문(양수=열림, 음수=닫힘)이다. Sigmoid는 반쯤 열린 문(기울기 소실 위험).

---

## Ⅱ. 아키텍처 및 핵심 원리

| 변형 | 수식 | 특징 |
|:---|:---|:---|
| <strong>Leaky ReLU</strong> | max(0.01x, x) | Dead Neuron 방지 |
| **PReLU** | max(αx, x) | α 학습 |
| **ELU** | α(eˣ-1), x | 부드러운 음수 |

---

## Ⅲ~Ⅴ. 결론

ReLU는 <strong>딥러닝의 가장 기본적이고 중요한 활성화 함수</strong>이며, CNN/MLP에서 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>ReLU</strong> | max(0,x) — CNN 표준 |
| <strong>Vanishing Gradient</strong> | Sigmoid의 문제 -> ReLU 해결 |
| **Dead Neuron** | ReLU의 문제 -> Leaky ReLU 해결 |
| **GELU** | Transformer 표준 |
| **AlexNet** | ReLU를 최초 대규모 적용 (2012) |

### 📈 관련 키워드 및 발전 흐름도

```text
[Sigmoid (1980s)] -> [ReLU (2010, Nair)] -> [AlexNet ReLU 성공 (2012)]
    -> [Leaky/PReLU (2015)] -> [GELU (2016, Transformer)]
    -> [SwiGLU (2022, LLM)] -> [현재: KAN (2024)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ReLU는 <strong>문</strong>이에요. 좋은 신호(양수)는 **열어서 통과**, 나쁜 신호(음수)는 <strong>닫아서 차단</strong>해요.
2. 옛날 문(Sigmoid)은 **반만 열려서** 신호가 점점 약해졌어요(Vanishing).
3. ReLU 덕분에 <strong>깊은 신경망</strong>도 잘 학습할 수 있게 됐답니다!
