+++
title = "캐리 세이브 가산기 (Carry Save Adder, CSA)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 캐리 세이브 가산기 (Carry Save Adder, CSA)

## 핵심 인사이트 (3줄 요약)
1. CSA는 3개의 n비트 수를 더하여 n비트 Sum과 n비트 Carry를 별도로 출력하며, 캐리 전파를 지연시켜 O(1) 지연을 달성하는 가산기이다
2. CSA는 주로 여러 수를 더할 때(예: 곱셈의 부분 곱 합산) 사용되며, 최종 단계에서 Carry Propagate Adder(CPA)로 Sum과 Carry를 합친다
3. 기술사시험에서는 CSA의 Sum/Carry 분리, Wallace Tree, Dadda Tree 곱셈기 구조가 핵심이다

## Ⅰ. 개요 (500자 이상)

캐리 세이브 가산기(Carry Save Adder, CSA)는 **3개의 n비트 수를 더할 때 캐리 전파를 수행하지 않고** Sum 벡터와 Carry 벡터를 별도로 출력하는 조합 회로이다. 일반적인 가산기가 캐리를 바로 전파하는 반면, CSA는 "캐리를 저장(Save)"하여 나중에 처리한다.

```
CSA 기본 개념:
일반 가산기: A + B + C → S + C_out (캐리 즉시 전파)
CSA:        A + B + C → Sum 벡터 + Carry 벡터 (캐리 지연)

Sum[i] = A[i] ⊕ B[i] ⊕ C[i]
Carry[i] = Majority(A[i], B[i], C[i])
        = (A[i]·B[i]) + (B[i]·C[i]) + (C[i]·A[i])
```

**CSA의 핵심 특징:**
1. **캐리 전파 없음**: 각 비트가 독립적으로 계산
2. **O(1) 지연**: n비트라도 일정한 지연
3. **3입력 2출력**: 3개 숫자를 2개 숫자로 압축

```
CSA 동작 예시 (4비트):
A = 0011 (3)
B = 0101 (5)
C = 0110 (6)

비트별 계산:
Bit 0: 1+1+0 = 10₂ → Sum[0]=0, Carry[0]=1
Bit 1: 1+0+1 = 10₂ → Sum[1]=0, Carry[1]=1
Bit 2: 0+1+1 = 10₂ → Sum[2]=0, Carry[2]=1
Bit 3: 0+0+0 = 00₂ → Sum[3]=0, Carry[3]=0

Sum = 0000
Carry = 0111 (왼쪽으로 1비트 시프트 필요)

최종 합 = Sum + (Carry << 1) = 0000 + 1110 = 1110 (14)
3+5+6 = 14 ✓
```

CSA는 **여러 수를 더해야 할 때** 매우 유용하다. 예를 들어 곱셈에서 부분 곱(Partial Product)을 합산할 때, CSA를 사용하여 캐리 전파를 최종 단계까지 지연시킬 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### CSA 회로 구조

```
n비트 CSA 구조:

A[n-1:0] ──┐
           ├──→ Full Adder × n ──┬──→ Sum[n-1:0]
B[n-1:0] ──┤                      │
           │                      └──→ Carry[n-2:0]
C[n-1:0] ──┘

각 비트 i (0 ~ n-1):
Sum[i] = A[i] ⊕ B[i] ⊕ C[i]
Carry[i] = Majority(A[i], B[i], C[i])

참고: Carry[i]는 (i+1)비트에 영향
```

### 전파 지연 분석

```
CSA 타이밍:

각 Full Adder:
- Sum 경로: XOR 3개 = 2~3 게이트 지연
- Carry 경로: Majority = 2 게이트 지연

n비트 CSA:
- 모든 비트가 병렬로 동작
- t_CSA = 2~3 게이트 (n에 무관)

RCA 비교:
- n비트 RCA: (2n-1) 게이트
- 32비트: RCA = 63 게이트, CSA = 3 게이트
- 속도 향상: 21x
```

### CSA 배열 (CSA Array)

```
m개의 수를 더하는 CSA 배열:

입력: X1, X2, X3, ..., Xm (각 n비트)

CSA 1: X1 + X2 + X3 → S1, C1
CSA 2: S1 + X4 + C1<<1 → S2, C2
CSA 3: S2 + X5 + C2<<1 → S3, C3
...

CSA (m-2)개 사용

최종: CPA(S_{m-2} + C_{m-2}<<1) → 최종 합

총 지연:
= (m-2) × t_CSA + t_CPA
= (m-2) × 3 + t_CPA (게이트)

RCA 비교:
= (m-1) × t_n-bit_RCA
= (m-1) × (2n-1)

m=10, n=32:
CSA: 8×3 + 8 = 32 게이트
RCA: 9×63 = 567 게이트
속도 향상: 17.7x
```

### Wallace Tree

```
Wallace Tree 곱셈기:

CSA를 트리 형태로 배치하여 레이어 최소화

n×n 비트 곱셈:
- n²개 부분 곱 생성
- Wallace Tree로 압축
- log₁.₅(n) 레이어

예시 (8×8 곱셈):
- 64개 부분 곱
- Layer 1: 64 → 43 (21 CSA)
- Layer 2: 43 → 29 (14 CSA)
- Layer 3: 29 → 20 (9 CSA)
- Layer 4: 20 → 14 (6 CSA)
- Layer 5: 14 → 10 (4 CSA)
- Layer 6: 10 → 7 (3 CSA)
- 최종 CPA: 7 → 2

총 6 CSA 레이어 + 1 CPA
```

## Ⅲ. 융합 비교

### CSA vs RCA

| 비교 항목 | CSA | RCA |
|----------|-----|-----|
| 입력 | 3개 n비트 | 2개 n비트 + Cin |
| 출력 | Sum + Carry (n비트) | Sum + Cout (n+1비트) |
| 지연 | O(1) | O(n) |
| 캐리 전파 | 없음 | 있음 |
| 응용 | 다중 덧셈, 곱셈 | 일반 덧셈 |

### 다중 덧셈 방식 비교

| 방식 | 지연 | 하드웨어 | 응용 |
|------|------|----------|------|
| RCA 체인 | O(mn) | 작음 | 소형 시스템 |
| CSA 배열 | O(m + log n) | 중간 | DSP, 곱셈 |
| Wallace Tree | O(log n) | 큼 | 고성능 |
| Dadda Tree | O(log n) | 중간 | 균형 |

### 트리 곱셈기 비교

| 타입 | 레이어 수 | CSA 수 | CPA 크기 | 면적 |
|------|----------|--------|----------|------|
| 순차 CSA | m-2 | m-2 | 2n | 작음 |
| Wallace | log₁.₅(n) | 많음 | 2n | 큼 |
| Dadda | 최적화 | 적음 | n+1 | 중간 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 곱셈기 설계

```
32×32 비트 곱셈기 (Wallace Tree):

1. 부분 곱 생성:
   - 1024개 (32×32) 부분 곱

2. Wallace Tree 압축:
   - 약 15 레이어
   - ~500 CSA

3. 최종 CPA:
   - 64비트 CLAA
   - 약 8 게이트 지연

총 지연:
- 부분 곱: 1 게이트 (AND)
- Wallace: 15 × 3 = 45 게이트
- CPA: 8 게이트
- 총: 54 게이트

순차 RCA: 31 × 63 = 1953 게이트
속도 향상: 36x
```

### FIR 필터 구현

```
FIR 필터 (N탭):

y[n] = Σ h[k] × x[n-k]

CSA 배열 사용:
1. 곱셈: N개 병렬
2. CSA 배열로 합산
3. 최종 CPA

지연:
- N개 곱셈: t_mul
- CSA 배열: (N-2) × t_CSA
- CPA: t_CPA

N=32, 32비트:
- 곱셈: 10 게이트
- CSA: 30 × 3 = 90 게이트
- CPA: 8 게이트
- 총: 108 게이트

순차: 31 × 63 = 1953 게이트
```

### FPGA CSA 구현

```
FPGA 최적화:

Xilinx:
- 각 SLICE에 여러 FA
- LUT로 CSA 구현
- 빠른 Carry Chain

DSP Slice 활용:
- 내장 27×18 곱셈기
- 내장 가산기
- CSA 필요 없음

Intel:
- ALM으로 CSA
- LAB 내 Carry Chain
- 자동 합성
```

## Ⅴ. 기대효과 및 결론

CSA는 다중 덧셈과 곱셈에 필수적이다. 캐리 전파를 지연시켜 O(1) 지연을 달성한다.

## 📌 관련 개념 맵

```
캐리 세이브 가산기
├── 원리: 3입력 → Sum + Carry (캐리 지연)
├── 구조
│   ├── Full Adder × n
│   ├── Sum 벡터
│   └── Carry 벡터
├── 응용
│   ├── CSA 배열
│   ├── Wallace Tree
│   ├── Dadda Tree
│   └── 곱셈기
└── 장점
    ├── O(1) 지연
    ├── 다중 덧셈 최적화
    └── 곱셈 가속
```

## 👶 어린이를 위한 3줄 비유 설명

1. CSA는 세 명의 학생이 시험을 볼 때 각자 점수를 계산하고, 나중에 선생님이 합계를 내는 것과 비슷해요. 각 비트는 자기 자리만 계산하고 자리올림은 나중에 해요
2. 예를 들어 3+5+6을 계산할 때, CSA는 일의 자리(1+1+0), 십의 자리(1+0+1)를 각각 따로 계산해요. 3+5+6=14에서 Sum=0000, Carry=0111을 출력하고 나중에 합쳐요
3. 이렇게 하면 많은 숫자를 더할 때 각 단계가 기다릴 필요 없어서 곱셈처럼 여러 번 더해야 할 때 아주 빨라요

```python
# 캐리 세이브 가산기 시뮬레이션

from typing import List, Tuple


class CarrySaveAdder:
    """
    캐리 세이브 가산기 (Carry Save Adder) 시뮬레이션
    """

    def __init__(self, bits: int):
        """
        n비트 CSA 생성

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.name = f"{bits}-bit Carry Save Adder"

    def add(self, a: int, b: int, c: int) -> Tuple[int, int]:
        """
        3개의 n비트 수 더하기 (캐리 세이브)

        Args:
            a: 첫 번째 수
            b: 두 번째 수
            c: 세 번째 수

        Returns:
            (sum, carry): Sum 벡터와 Carry 벡터
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits) or not (0 <= c < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다")

        sum_vec = 0
        carry_vec = 0

        for i in range(self.bits):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1
            c_bit = (c >> i) & 1

            # Sum[i] = A[i] ⊕ B[i] ⊕ C[i]
            sum_bit = a_bit ^ b_bit ^ c_bit
            sum_vec |= (sum_bit << i)

            # Carry[i] = Majority(A[i], B[i], C[i])
            carry_bit = (a_bit & b_bit) | (b_bit & c_bit) | (c_bit & a_bit)
            carry_vec |= (carry_bit << i)

        return sum_vec, carry_vec

    def add_csa_array(self, numbers: List[int]) -> Tuple[int, int]:
        """
        CSA 배열로 여러 수 더하기

        Args:
            numbers: 더할 수들의 리스트

        Returns:
            (sum, carry): 최종 Sum과 Carry 벡터
        """
        if len(numbers) < 3:
            raise ValueError("최소 3개의 수가 필요합니다")

        # 첫 번째 CSA
        sum_vec, carry_vec = self.add(numbers[0], numbers[1], numbers[2])

        # 나머지 수들에 대해 CSA 반복
        for num in numbers[3:]:
            # Carry는 왼쪽으로 1비트 시프트
            shifted_carry = carry_vec << 1
            sum_vec, carry_vec = self.add(sum_vec, shifted_carry, num)

        return sum_vec, carry_vec

    def finalize(self, sum_vec: int, carry_vec: int) -> int:
        """
        Sum과 Carry를 최종 합으로 변환

        Args:
            sum_vec: Sum 벡터
            carry_vec: Carry 벡터

        Returns:
            최종 합
        """
        # Carry는 왼쪽으로 1비트 시프트하여 Sum에 더함
        return sum_vec + (carry_vec << 1)


class WallaceTreeMultiplier:
    """
    월리스 트리 곱셈기 시뮬레이션
    """

    def __init__(self, bits: int):
        """
        n×n 비트 월리스 트리 곱셈기

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.csa = CarrySaveAdder(bits * 2)  # 곱셈 결과는 2n비트

    def multiply(self, a: int, b: int) -> int:
        """
        월리스 트리로 곱셈 수행

        Args:
            a: 피승수
            b: 승수

        Returns:
            곱
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다")

        # 부분 곱 생성
        partial_products = []
        for i in range(self.bits):
            if (b >> i) & 1:
                partial_products.append(a << i)

        # 부분 곱이 2개 이하면 합산 후 반환
        if len(partial_products) <= 1:
            return sum(partial_products) if partial_products else 0

        if len(partial_products) == 2:
            return partial_products[0] + partial_products[1]

        # CSA 배열로 압축
        sum_vec, carry_vec = self.csa.add_csa_array(partial_products)

        # 최종 합산
        result = sum_vec + (carry_vec << 1)

        return result


def demonstration():
    """CSLA 데모"""
    print(f"\n{'='*70}")
    print("캐리 세이브 가산기 (Carry Save Adder) 데모")
    print(f"{'='*70}")

    # 8비트 CSA
    csa8 = CarrySaveAdder(8)

    print("\n[3개 수 더하기]")
    test_cases = [
        (3, 5, 6),      # 3 + 5 + 6 = 14
        (10, 20, 30),   # 10 + 20 + 30 = 60
        (100, 50, 75),  # 100 + 50 + 75 = 225
        (255, 128, 64), # 255 + 128 + 64 = 447 (8비트 오버플로우)
    ]

    for a, b, c in test_cases:
        sum_vec, carry_vec = csa8.add(a, b, c)
        result = csa8.finalize(sum_vec, carry_vec)

        print(f"\n{a} + {b} + {c} = {result}")
        print(f"  Sum 벡터: {sum_vec:08b} ({sum_vec})")
        print(f"  Carry 벡터: {carry_vec:08b} ({carry_vec})")
        print(f"  최종: {sum_vec} + ({carry_vec} << 1) = {sum_vec} + {carry_vec << 1} = {result}")

    # CSA 배열 (여러 수 더하기)
    print(f"\n{'='*70}")
    print("CSA 배열: 여러 수 더하기")
    print(f"{'='*70}")

    numbers = [10, 20, 30, 40, 50, 60, 70, 80]
    sum_vec, carry_vec = csa8.add_csa_array(numbers)
    result = csa8.finalize(sum_vec, carry_vec)

    print(f"\n입력: {numbers}")
    print(f"합계: {sum(numbers)} = {sum(numbers)}")
    print(f"CSA 결과: {result}")
    print(f"  Sum: {sum_vec:08b}")
    print(f"  Carry: {carry_vec:08b}")
    print(f"  Final: {result:010b} ({result})")

    # Wallace Tree 곱셈
    print(f"\n{'='*70}")
    print("Wallace Tree 곱셈기")
    print(f"{'='*70}")

    wallace8 = WallaceTreeMultiplier(8)

    mul_tests = [
        (12, 15),   # 12 × 15 = 180
        (100, 200), # 100 × 200 = 20000
        (255, 127), # 255 × 127 = 32385
    ]

    for a, b in mul_tests:
        result = wallace8.multiply(a, b)
        expected = a * b
        print(f"\n{a} × {b} = {result} (기대: {expected}) {'✓' if result == expected else '✗'}")


def compare_with_rca():
    """CSA와 RCA 비교"""
    print(f"\n{'='*70}")
    print("CSA vs RCA: 다중 덧셈 비교")
    print(f"{'='*70}")

    n = 32
    m = 10  # 더할 수의 개수

    # CSA 배열
    csa = CarrySaveAdder(n)
    numbers = [100 + i for i in range(m)]

    # CSA 지연 (게이트 단위 추정)
    csa_delay = (m - 2) * 3 + 8  # (m-2) CSA + 32비트 CLAA

    # RCA 지연
    rca_delay = (m - 1) * (2 * n - 1)

    print(f"\n{n}비트 {m}개 수 더하기:")
    print(f"  CSA 배열: {csa_delay} 게이트 지연")
    print(f"  RCA 체인: {rca_delay} 게이트 지연")
    print(f"  속도 향상: {rca_delay / csa_delay:.1f}x")


if __name__ == "__main__":
    demonstration()
    compare_with_rca()
```
