---
title: "Activation Function"
date: "2026-04-19"
tags:
  - "studynote-data-engineering"
weight: 129
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 활성화 함수는 <strong>신경망의 각 뉴런 출력에 적용되는 비선형 변환</strong>이며, 이것이 없으면 아무리 깊은 신경망도 **단일 선형 변환과 동일**(표현력 없음)하다.
> 2. **가치**: Sigmoid->Tanh->ReLU->GELU->SwiGLU의 발전이 딥러닝 성능을 직접적으로 향상시켰으며, <strong>ReLU가 Vanishing Gradient 문제를 해결</strong>하여 딥러닝 르네상스를 열었다.
> 3. **판단 포인트**: CNN/MLP는 ReLU, Transformer는 GELU, 최신 LLM(Llama)은 SwiGLU가 표준이며, 출력층은 분류(Softmax)·회귀(Linear)·확률(Sigmoid)로 구분한다.

---

## Ⅰ. 개요 및 필요성

```text
활성화 함수 비교:
Sigmoid: σ(x) = 1/(1+e⁻ˣ)     -> 0~1, Vanishing
ReLU:    f(x) = max(0, x)       -> 현재 표준, Dead Neuron
GELU:    f(x) = x·Φ(x)         -> Transformer 표준
SwiGLU:  f(x) = Swish(xW₁)⊙xW₂ -> LLM 최신
```

- **📢 섹션 요약 비유**: 활성화 함수는 신경망의 <strong>스위치</strong>이다. 스위치가 없으면 전기(정보)가 그냥 흐를 뿐 아무 기능을 못 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 함수 | 범위 | 장점 | 문제 |
|:---|:---|:---|:---|
| <strong>Sigmoid</strong> | 0~1 | 확률 출력 | Vanishing |
| <strong>ReLU</strong> | 0~∞ | **Vanishing 해결** | Dead Neuron |
| **GELU** | 연속 | Transformer 최적 | - |
| **SwiGLU** | 연속 | <strong>LLM 최고 성능</strong> | 파라미터^ |

---

## Ⅲ. 비교 및 연결

| 용도 | 함수 |
|:---|:---|
| **은닉층** | ReLU / GELU / SwiGLU |
| <strong>이진 분류</strong> | Sigmoid |
| <strong>다중 분류</strong> | Softmax |
| **회귀** | Linear (없음) |

---

## Ⅳ~Ⅴ. 결론

활성화 함수는 <strong>딥러닝의 비선형 표현력의 원천</strong>이며, ReLU->GELU->SwiGLU의 진화가 모델 성능을 직접 견인한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>ReLU</strong> | CNN/MLP 표준 |
| **GELU** | Transformer 표준 |
| **SwiGLU** | LLM 최신 (Llama/PaLM) |
| <strong>Vanishing Gradient</strong> | Sigmoid/Tanh 문제 |
| <strong>Softmax</strong> | 출력층 분류 활성화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Sigmoid (1980s)] -> [Tanh (1990s)] -> [ReLU (2010, Nair)]
    -> [GELU (2016)] -> [SwiGLU (2022, PaLM/Llama)]
    -> [현재: 학습 가능 활성화 (KAN, 2024)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 활성화 함수는 신경망의 <strong>스위치</strong>예요. 켜야(비선형) 뇌가 <strong>생각</strong>할 수 있어요.
2. 옛날 스위치(Sigmoid)는 **느렸지만**, 새 스위치(ReLU)는 빠르고 강해요.
3. 최신 스위치(SwiGLU)는 AI가 <strong>더 똑똑하게 생각</strong>할 수 있게 해줘요!
