---
title: "Ann Mlp"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 128
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ANN(인공 신경망)은 <strong>생물학적 뉴런을 모방</strong>하여 입력->가중치 곱->활성화 함수->출력의 구조를 컴퓨터로 구현한 것이며, MLP(다층 퍼셉트론)는 <strong>은닉층(Hidden Layer)이 1개 이상인 피드포워드 신경망</strong>이다.
> 2. **가치**: 단층 퍼셉트론은 XOR 문제를 풀 수 없는(선형 분리 불가) 근본 한계가 있었으나, <strong>은닉층 추가(MLP) + 역전파(Backpropagation)</strong>로 비선형 문제를 해결하며 딥러닝의 기초가 되었다.
> 3. **판단 포인트**: 활성화 함수(Sigmoid->ReLU), 역전파 알고리즘, Vanishing Gradient 문제와 해결(ReLU·BatchNorm·ResNet)을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    MLP 구조                                           |
+-------------------------------------------------------+
|  [입력층]    x₁, x₂, ..., xₙ                        |
|     v (가중치 W₁)                                     |
|  [은닉층 1]  h₁ = σ(W₁·x + b₁)                      |
|     v (가중치 W₂)                                     |
|  [은닉층 2]  h₂ = σ(W₂·h₁ + b₂)                     |
|     v (가중치 W₃)                                     |
|  [출력층]    y = softmax(W₃·h₂ + b₃)                 |
|                                                       |
|  학습: 역전파 (Backpropagation)로 가중치 업데이트    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: MLP는 여러 층의 <strong>체(필터)</strong>이다. 입력이 여러 체를 통과하면서 점점 세밀하게 분류된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 활성화 함수 진화

| 함수 | 특징 | 문제 |
|:---|:---|:---|
| <strong>Sigmoid</strong> | 0~1 출력 | Vanishing Gradient |
| <strong>Tanh</strong> | -1~1 출력 | Vanishing Gradient |
| <strong>ReLU</strong> | max(0,x) | **현재 표준** |
| **GELU** | Transformer 표준 | GPT/BERT 사용 |

- **📢 섹션 요약 비유**: Sigmoid는 느린 수도꼭지(미세 조절), ReLU는 빠른 스위치(on/off)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 단층 퍼셉트론 | MLP |
|:---|:---|:---|
| **비선형** | 불가 (XOR ✗) | **가능** |
| **깊이** | 0 은닉층 | **1+ 은닉층** |
| **학습** | 퍼셉트론 규칙 | <strong>역전파</strong> |

---

## Ⅳ. 실무 적용 및 실무자 판단

### MLP의 위치
- Transformer의 FFN(Feed-Forward Network) = **2층 MLP**.
- 현대 딥러닝: CNN·RNN·Transformer 모두 MLP를 구성 요소로 포함.

---

## Ⅴ. 기대효과 및 결론

MLP는 <strong>딥러닝의 가장 기본 빌딩 블록</strong>이며, Transformer의 FFN으로 현재까지 핵심 역할을 수행한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>퍼셉트론</strong> | 단층 신경망 (XOR 불가) |
| **MLP** | 다층 퍼셉트론 (비선형 가능) |
| <strong>역전파</strong> | MLP 학습 알고리즘 |
| <strong>ReLU</strong> | 현대 표준 활성화 함수 |
| **FFN** | Transformer 내 MLP |

### 📈 관련 키워드 및 발전 흐름도

```text
[퍼셉트론 (Rosenblatt, 1958)]
    |
    v
[XOR 문제 (Minsky, 1969) — 인공지능 겨울]
    |
    v
[MLP + 역전파 (Rumelhart, 1986)]
    |
    v
[딥러닝 (Hinton, 2006~) — GPU·ReLU·데이터]
    |
    v
[현재: MLP-Mixer / gMLP — MLP만으로 Vision 처리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 퍼셉트론은 <strong>1단 필터</strong>예요. 간단한 것만 걸러낼 수 있어요.
2. MLP는 <strong>여러 단 필터</strong>예요. 복잡한 것도 <strong>세밀하게 분류</strong>할 수 있어요.
3. 틀린 답이 나오면 <strong>역전파(피드백)</strong>로 필터를 조정해서 더 정확해져요!
