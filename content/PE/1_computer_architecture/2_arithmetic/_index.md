+++
title = "02. 데이터 표현 및 산술 연산 (Arithmetic)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-computer-architecture"
kids_analogy = "숫자를 전기가 알아들을 수 있는 0과 1의 암호로 바꾸어 계산하는 법을 배우는 곳이에요. 더하기, 빼기, 그리고 아주 큰 숫자나 소수점을 어떻게 실수 없이 다루는지 공부하게 될 거예요!"
+++

# 02. 데이터 표현 및 산술 연산 (Arithmetic)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 보수(Complement) 체계를 이용한 감산의 가산화 및 IEEE 754 표준을 통한 실수의 정밀한 이진 표현 기법.
> 2. **가치**: ALU(Arithmetic Logic Unit)의 연산 효율 극대화 및 수치 해석적 정밀도(Precision) 확보를 통한 시스템 신뢰성 제고.
> 3. **융합**: 고속 연산을 위한 병렬 가산기(CLA) 및 에러 검출을 위한 해밍 코드(Hamming Code) 등 하드웨어 기반의 수치 처리 엔진 설계.

---

### Ⅰ. 개요 (Context & Background)
컴퓨터 산술은 수학적 추상화를 디지털 하드웨어로 구현하는 기술이다. 정수와 실수를 이진 비트로 어떻게 매핑하고, 이를 물리적인 가산기나 승산기로 어떻게 연산하는지가 핵심이다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 구성 요소
- **Fixed-point Representation**: 정수 표현 (부호 절대값, 1의 보수, 2의 보수)
- **Floating-point (IEEE 754)**: 지수부와 가수부를 분리한 실수 표현
- **Adders**: Ripple Carry, Carry Look-ahead (CLA)
- **Error Control**: Parity, Hamming Code, ECC

#### 2. 연산 계층 구조 (ASCII)
```text
    [ Arithmetic Unit Architecture ]
    
    (Data)   +---------------------------+
             | Floating Point Unit (FPU) |  <-- IEEE 754
             +-------------+-------------+
                           |
             +-------------v-------------+
             | Fixed Point Unit (ALU)    |  <-- 2's Complement
             +-------------+-------------+
                           |
             +-------------v-------------+
             | Logic Gate Adders (XOR)   |  <-- Fundamental
             +---------------------------+
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 정수 표현: 1의 보수 vs 2의 보수
| 구분 | 1의 보수 (1's) | 2의 보수 (2's) |
| :--- | :--- | :--- |
| **0의 표현** | +0, -0 두 가지 존재 (모호함) | 한 가지 존재 (명확함) |
| **연산 방식** | End-around Carry 처리 필요 | 단순 가산 후 Carry 무시 |
| **범위** | $-2^{n-1}-1 \sim 2^{n-1}-1$ | $-2^{n-1} \sim 2^{n-1}-1$ (하나 더 표현 가능) |
| **표준** | 구형 시스템 | 현대 대부분의 아키텍처 표준 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무에서는 특히 **Floating-point Overflow/Underflow**와 **Precision Loss**가 치명적이다. 기술사는 고성능 수치 연산 워크로드(AI/HPC)에서 단정밀도(FP32)와 반정밀도(FP16)를 전략적으로 선택하여 연산량과 정확도 사이의 트레이드오프를 결정해야 한다.

---

### Ⅴ. 기대효과 및 결론
정확한 산술 체계는 모든 컴퓨팅의 신뢰성 지표다. 향후 AI 가속기에서의 양자화(Quantization, INT8/FP8) 기술은 산술 연산의 효율성을 극대화하는 방향으로 진화하고 있다.
