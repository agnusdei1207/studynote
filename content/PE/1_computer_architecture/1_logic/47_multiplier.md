+++
title = "곱셈기 (Multiplier)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 곱셈기 (Multiplier)

## 핵심 인사이트 (3줄 요약)
1. 곱셈기는 두 이진수의 곱을 수행하는 회로로, 순차 곱셈기(Sequential Multiplier)와 조합 곱셈기(Combinational Multiplier)가 있으며, 부분 곱(Partial Product)의 합으로 결과를 도출한다
2. n×n비트 곱셈은 n²개의 부분 곱을 생성하고 이를 CSA/CLAA로 합산하며, Wallace Tree와 Dadda Tree는 O(log n) 지연을 달성한다
3. 기술사시험에서는 곱셈 알고리즘, Booth Encoding, Wallace Tree, 부호 있는 곱셈이 핵심이다

## Ⅰ. 개요 (500자 이상)

곱셈기(Multiplier)는 **두 이진수 A와 B의 곱을 계산**하는 디지털 회로이다. 기본적인 곱셈 원리는 10진수와 동일하며, 각 비트별로 부분 곱(Partial Product)을 생성하고 이를 합산하여 최종 결과를 도출한다.

```
이진수 곱셈 예시 (4비트):
     1011  (11)
   × 0110  (6)
   ------
     0000  (1011 × 0)
    1011   (1011 × 1, 1비트 시프트)
   1011    (1011 × 1, 2비트 시프트)
+ 0000     (1011 × 0, 3비트 시프트)
   ------
  010000110  (66)

11 × 6 = 66 ✓
```

**곱셈기의 핵심 구성 요소:**

1. **부분 곱 생성 (Partial Product Generation)**
   - A의 각 비트와 B의 AND 연산
   - n×n비트 곱셈에서 n²개 부분 곱

2. **부분 곱 합산 (Partial Product Addition)**
   - CSA (Carry Save Adder) 또는 RCA로 합산
   - 최종 CLAA로 캐리 전파

3. **결�력 출력 (Result)**
   - 2n비트 결과 (n×n비트 곱셈)

```
n×n비트 곱셈기 구조:
A[n-1:0] ──┐
           ├──→ Partial Product Generator ──┐
B[n-1:0] ──┤                                 │
           │                                 │
           └──→ n²개 Partial Product           │
                                             │
                                  ┌──────────┴──────────┐
                                  │  Addition Network   │
                                  │  (CSA + CLAA)       │
                                  └──────────┬──────────┘
                                             │
                                      Result[2n-1:0]
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 순차 곱셈기 (Sequential Multiplier)

```
순차 곱셈기 알고리즘:

초기화:
Product = 0
Multiplier = B
Multiplicand = A

n번 반복:
if Multiplier[0] == 1:
    Product = Product + Multiplicand
Multiplicand << 1
Multiplier >> 1

회로:
┌─────────────────────────────────────────┐
│  A (Multiplicand) ──→ Shift Left       │
│                      │                  │
│  B (Multiplier)   ───┴──→ Shift Right  │
│         │                             │
│         └──→ Test LSB ──┐             │
│                          │             │
│  Product ←──────────────┴── Adder     │
│    (Accumulator)                      │
└─────────────────────────────────────────┘

지연: n × t_add (n클럭)
면적: 1개 Adder + 2개 Shift Register
```

### 배열 곱셈기 (Array Multiplier)

```
4×4 배열 곱셈기:

    A3 A2 A1 A0
    × B3 B2 B1 B0
    ────────────
        P00      ← Row 0
      P10 P01    ← Row 1
    P20 P11 P02  ← Row 2
  P30 P21 P12 P03 ← Row 3
  ───────────────
  R7 R6 R5 R4 R3 R2 R1 R0

회로:
PP00 ──┐
PP01 ──┤
PP02 ──┼──→ CSA Array → CLAA → Result
...    │
PP33 ──┘

지연: O(n)
면적: O(n²) Full Adder
```

### Wallace Tree 곱셈기

```
Wallace Tree (O(log n) 지연):

Layer 1: n²개 Partial Product
  ↓ (CSA reduction)
Layer 2: ~2/3 n²
  ↓ (CSA reduction)
Layer 3: ~4/9 n²
  ...
  ↓
Final: 2n개 → CLAA → Result

8×8 곱셈 예시:
Layer 0: 64개 PP
Layer 1: 64 → 43 (21 CSA)
Layer 2: 43 → 29 (14 CSA)
Layer 3: 29 → 20 (9 CSA)
Layer 4: 20 → 14 (6 CSA)
Layer 5: 14 → 10 (4 CSA)
Layer 6: 10 → 7 (3 CSA)
Final: 7 → 2 (CLAA)

지연: 6 × t_CSA + t_CLAA
     = 6 × 3 + 8 = 26 게이트

Array: 16 × 3 = 48 게이트
Wallace: 1.85x 빠름
```

### Booth Encoding

```
Radix-2 Booth Encoding:

B[i-1] B[i] | Operation
-----------|------------
    0   0   | No operation
    0   1   | Add A
    1   0   | Subtract A
    1   1   | No operation

장점:
- 부호 있는 곱셈에 적합
- 부분 곱 수 절반 (n² → n²/2)
- 연속된 1을 효율적으로 처리

예시:
7 = 0111
   → 1000 - 1 (2³ - 1)
   → 1회 덧셈, 1회 뺄셈

Radix-4 Booth:
B[i+1] B[i] B[i-1] | Operation
------------------|------------
     0   0   0     | +0
     0   0   1     | +A
     0   1   0     | +A
     0   1   1     | +2A
     1   0   0     | -2A
     1   0   1     | -A
     1   1   0     | -A
     1   1   1     | -0

부분 곱: n² → n²/4
```

### 전파 지연 분석

```
곱셈기 지연 비교:

1. 순차 곱셈기:
   t_total = n × t_add + n × t_clk
   32비트: 32 × 8 + 32 × 1 = 288 클럭

2. 배열 곱셈기:
   t_total = 2n × t_add + n × t_carry
   32비트: 64 × 2 + 32 × 1 = 160 게이트

3. Wallace Tree:
   t_total = log₁.₅(n) × t_CSA + t_CLAA
   32×32: 14 × 3 + 10 = 52 게이트

4. Dadda Tree:
   t_total = log₁.₅(n) × t_CSA + t_CLAA
   Wallace보다 10-20% 느리지만 면적 작음
```

## Ⅲ. 융합 비교

### 곱셈기 방식 비교

| 방식 | 지연 | 면적 | 전력 | 복잡도 | 응용 |
|------|------|------|------|--------|------|
| 순차 | O(n) 클럭 | 작음 | 낮음 | 단순 | 임베디드 |
| 배열 | O(n) | 큼 | 중간 | 중간 | FPGA |
| Wallace | O(log n) | 매우 큼 | 높음 | 복잡 | 고성능 CPU |
| Dadda | O(log n) | 큼 | 중간 | 복잡 | 균형 |
| Booth | O(log n) | 중간 | 중간 | 복잡 | 부호 곱셈 |

### n비트 곱셈기 성능

| n | Array | Wallace | Dadda | Booth |
|---|-------|---------|-------|-------|
| 8 | 20 | 12 | 14 | 10 |
| 16 | 36 | 20 | 24 | 18 |
| 32 | 68 | 36 | 42 | 32 |
| 64 | 132 | 64 | 76 | 58 |

(단위: 게이트 지연)

### 곱셈기 구현 트레이드오프

```
면적 vs 속도:
- Wallace: 가장 빠름, 가장 큼
- Dadda: 10% 느림, 20% 작음
- Array: 느림, 중간 크기

전력 vs 성능:
- 순차: 가장 낮은 전력
- Wallace: 가장 높은 전력
- Dadda: 중간

FPGA 최적화:
- DSP Slice 사용
- 내장 곱셈기 활용
- Carry Chain 활용
```

## Ⅳ. 실무 적용 및 기술사적 판단

### CPU 곱셈기

```
Intel x86-64 곱셈기:

구조:
- 64×64비트 → 128비트 결과
- Radix-4 Booth Encoding
- Wallace Tree + CLAA
- 3-4 파이프라인 스테이지

지연:
- IMUL (정수): 3 클럭
- MUL (부동소수): 5 클럭

파이프라인:
Stage 1: Booth Encoding
Stage 2: Wallace Reduction
Stage 3: CLAA
Stage 4: Rounding (FP)
```

### DSP 곱셈기

```
FIR 필터 곱셈:

y[n] = Σ h[k] × x[n-k]

구현:
1. 병렬 곱셈기 N개
2. CSA 배열로 합산
3. CLAA로 최종 합

지연:
- N개 곱셈: 1 스테이지 (병렬)
- CSA 배열: log₁.₅(N) 스테이지
- CLAA: 1 스테이지
- 총: log₁.₅(N) + 2

N=32:
총 지연 = 4 + 2 = 6 스테이지
```

### FPGA 곱셈기

```
Xilinx DSP48E1:

구조:
- 25×18 비트 곱셈기
- 내장 Adder
- 내장 Accumulator
- 패턴 디텍터

지연:
- 곱셈: 1 클럭 (@ 600MHz)
- 곱-누: 2 클럭
- 파이프라인: 최대 지연 4 클럭

활용:
- FIR/IIR 필터
- FFT 버터플라이
- 행렬 곱셈
```

## Ⅴ. 기대효과 및 결론

곱셈기는 DSP와 그래픽의 핵심이다. Wallace Tree로 O(log n) 지연을 달성한다.

## 📌 관련 개념 맵

```
곱셈기
├── 알고리즘
│   ├── 순차 (Sequential)
│   ├── 배열 (Array)
│   ├── Wallace Tree
│   └── Dadda Tree
├── 최적화
│   ├── Booth Encoding
│   ├── CSA Array
│   └── Pipeline
├── 부호 처리
│   ├── Unsigned
│   ├── 2의 Complement
│   └── Booth
└── 응용
    ├── DSP 필터
    ├── 그래픽
    └── 행렬 연산
```

## 👶 어린이를 위한 3줄 비유 설명

1. 곱셈기는 12 × 34를 계산할 때 12×4, 12×30을 따로 계산해서 더하는 것과 비슷해요. 각 비트마다 부분 곱을 만들고 이를 모두 더해요
2. 1011 × 0110을 계산하면, 1011×0, 1011×1, 1011×1, 1011×0을 각각 계산하고 자리를 맞춰서 더해요
3. Wallace Tree는 이 부분 곱들을 나무 구조로 효율적으로 더해서 64비트 곱셈도 아주 빨리 계산해요

```python
# 곱셈기 시뮬레이션

from typing import List, Tuple
import time


class SequentialMultiplier:
    """순차 곱셈기"""

    def __init__(self, bits: int):
        self.bits = bits

    def multiply(self, a: int, b: int) -> int:
        """
        순차 곱셈 알고리즘

        Args:
            a: 피승수
            b: 승수

        Returns:
            곱
        """
        multiplicand = a
        multiplier = b
        product = 0

        for _ in range(self.bits):
            if multiplier & 1:
                product += multiplicand
            multiplicand <<= 1
            multiplier >>= 1

        return product & ((1 << (2 * self.bits)) - 1)


class ArrayMultiplier:
    """배열 곱셈기"""

    def __init__(self, bits: int):
        self.bits = bits

    def multiply(self, a: int, b: int) -> int:
        """
        배열 곱셈 (부분 곱 합산)

        Args:
            a: 피승수
            b: 승수

        Returns:
            곱
        """
        # 부분 곱 생성
        partial_products = []
        for i in range(self.bits):
            if (b >> i) & 1:
                partial_products.append(a << i)
            else:
                partial_products.append(0)

        # 합산
        result = sum(partial_products)
        return result & ((1 << (2 * self.bits)) - 1)


class WallaceTreeMultiplier:
    """Wallace Tree 곱셈기"""

    def __init__(self, bits: int):
        self.bits = bits

    def multiply(self, a: int, b: int) -> int:
        """
        Wallace Tree 곱셈

        Args:
            a: 피승수
            b: 승수

        Returns:
            곱
        """
        # 부분 곱 생성
        partial_products = []
        for i in range(self.bits):
            for j in range(self.bits):
                if ((a >> i) & 1) and ((b >> j) & 1):
                    partial_products.append(1 << (i + j))

        # Wallace Tree 압축 시뮬레이션
        while len(partial_products) > 2:
            new_pp = []

            # 3개씩 그룹화하여 CSA
            for i in range(0, len(partial_products) - 2, 3):
                if i + 2 < len(partial_products):
                    s = partial_products[i] ^ partial_products[i + 1] ^ partial_products[i + 2]
                    c = ((partial_products[i] & partial_products[i + 1]) |
                         (partial_products[i + 1] & partial_products[i + 2]) |
                         (partial_products[i] & partial_products[i + 2])) << 1
                    new_pp.append(s)
                    new_pp.append(c)
                else:
                    new_pp.extend(partial_products[i:])

            partial_products = new_pp

        result = sum(partial_products)
        return result & ((1 << (2 * self.bits)) - 1)


class BoothMultiplier:
    """Radix-2 Booth 곱셈기"""

    def __init__(self, bits: int):
        self.bits = bits

    def multiply(self, a: int, b: int) -> int:
        """
        Radix-2 Booth 곱셈

        Args:
            a: 피승수
            b: 승수

        Returns:
            곱
        """
        # 2의 보수 처리
        if a >= (1 << (self.bits - 1)):
            a -= (1 << self.bits)
        if b >= (1 << (self.bits - 1)):
            b -= (1 << self.bits)

        product = 0
        acc = 0
        multiplicand = a

        # Booth Encoding
        for i in range(self.bits):
            b_prev = (b >> (i + 1)) & 1
            b_curr = (b >> i) & 1

            if b_curr == 1 and b_prev == 0:
                acc += multiplicand
            elif b_curr == 0 and b_prev == 1:
                acc -= multiplicand

            multiplicand <<= 1

        return acc & ((1 << (2 * self.bits)) - 1)


def demonstration():
    """곱셈기 데모"""
    print("=" * 70)
    print("곱셈기 (Multiplier) 데모")
    print("=" * 70)

    bits = 8

    multipliers = [
        ("Sequential", SequentialMultiplier(bits)),
        ("Array", ArrayMultiplier(bits)),
        ("Wallace Tree", WallaceTreeMultiplier(bits)),
        ("Booth", BoothMultiplier(bits)),
    ]

    test_cases = [
        (12, 15),
        (100, 200),
        (255, 127),
        (128, 128),
    ]

    for a, b in test_cases:
        print(f"\n{a} × {b} = {a * b}")
        print("-" * 40)

        for name, multiplier in multipliers:
            result = multiplier.multiply(a, b)
            expected = a * b
            match = "✓" if result == expected else "✗"
            print(f"  {name:15s}: {result:6} {match}")


def benchmark():
    """성능 벤치마크"""
    print("\n" + "=" * 70)
    print("곱셈기 성능 비교 (32비트)")
    print("=" * 70)

    bits = 32
    iterations = 10000

    multipliers = [
        ("Array", ArrayMultiplier(bits)),
        ("Wallace", WallaceTreeMultiplier(bits)),
        ("Booth", BoothMultiplier(bits)),
    ]

    for name, multiplier in multipliers:
        start = time.time()

        for i in range(iterations):
            multiplier.multiply(i, i + 1)

        elapsed = time.time() - start
        ops_per_sec = iterations / elapsed

        print(f"{name:10s}: {ops_per_sec:,.0f} ops/sec ({elapsed*1000:.2f}ms)")


def partial_product_demo():
    """부분 곱 시뮬레이션"""
    print("\n" + "=" * 70)
    print("부분 곱 (Partial Product) 시뮬레이션")
    print("=" * 70)

    a = 0b1011  # 11
    b = 0b0110  # 6

    print(f"\n     {a:04b} ({a})")
    print(f"   × {b:04b} ({b})")
    print(f"   {'-' * 10}")

    partial_products = []
    for i in range(4):
        pp = ((a & ((b >> i) & 1)) * (1 << i)) if ((b >> i) & 1) else 0
        partial_products.append(pp)
        if pp > 0:
            print(f"     {pp:08b} ({a} × {b & (1<<i):04b}, << {i})")

    print(f"   {'-' * 10}")
    result = sum(partial_products)
    print(f"     {result:08b} ({result})")
    print(f"\n검증: 11 × 6 = {result} ({a * b}) {'✓' if result == a * b else '✗'}")


if __name__ == "__main__":
    demonstration()
    benchmark()
    partial_product_demo()
```
