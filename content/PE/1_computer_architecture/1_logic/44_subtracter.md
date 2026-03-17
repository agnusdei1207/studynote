+++
title = "뺄셈기 (Subtracter)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 뺄셈기 (Subtracter)

## 핵심 인사이트 (3줄 요약)
1. 뺄셈기는 A - B를 수행하는 회로로, 2의 보수를 이용한 방식이 가장 널리 사용되며 A + (~B + 1)로 변환하여 가산기로 구현한다
2. 하프 뺄셈기, 풀 뺄셈기가 있으며, 풀 뺄셈기는 차(Difference)와 Borrow(빌림)를 출력하고 n비트 뺄셈은 풀 뺄셈기를 직렬 연결하여 구현
3. 기술사시험에서는 뺄셈의 2의 보수 변환, 가감산기(Adder-Subtractor), 오버플로/언더플로 검출이 핵심이다

## Ⅰ. 개요 (500자 이상)

뺄셈기(Subtracter)는 **이진수 뺄셈 A - B를 수행**하는 조합 논리 회로이다. 가산기와 유사하게 하프 뺄셈기(Half Subtracter)와 풀 뺄셈기(Full Subtracter)가 있으며, 실제 프로세서에서는 **2의 보수(Two's Complement)를 이용한 뺄셈**이 주로 사용된다.

```
뺄셈의 기본 원리:

방법 1: 직접 뺄셈
  A - B → Difference, Borrow

방법 2: 2의 보수 (실제 사용)
  A - B = A + (~B + 1)
  = A + (2^n - B)
  = A - B + 2^n
```

**하프 뺄셈기(Half Subtracter):**
- 2개 입력(A, B)에 대해 차(Difference)와 빌림(Borrow)을 출력
- 이전 비트의 빌림을 고려하지 않음

```
하프 뺄셈기 진리표:
| A | B | Diff | Borrow | 설명 |
|---|---|------|--------|------|
| 0 | 0 |  0   |   0    | 0-0=0 |
| 0 | 1 |  1   |   1    | 0-1=-1 (빌림) |
| 1 | 0 |  1   |   0    | 1-0=1 |
| 1 | 1 |  0   |   0    | 1-1=0 |

Diff = A ⊕ B
Borrow = A' · B
```

**풀 뺄셈기(Full Subtracter):**
- 3개 입력(A, B, Borrow_in)에 대해 차와 빌림 출력
- n비트 뺄셈의 기본 요소

```
풀 뺄셈기 진리표:
| A | B | Bin | Diff | Bout | 설명 |
|---|---|-----|------|------|------|
| 0 | 0 |  0  |  0   |  0   | 0-0-0=0 |
| 0 | 0 |  1  |  1   |  1   | 0-0-1=-1 |
| 0 | 1 |  0  |  1   |  1   | 0-1-0=-1 |
| 0 | 1 |  1  |  0   |  1   | 0-1-1=-2 |
| 1 | 0 |  0  |  1   |  0   | 1-0-0=1 |
| 1 | 0 |  1  |  0   |  0   | 1-0-1=0 |
| 1 | 1 |  0  |  0   |  0   | 1-1-0=0 |
| 1 | 1 |  1  |  1   |  1   | 1-1-1=-1 |

Diff = A ⊕ B ⊕ Bin
Bout = A'·B + A'·Bin + B·Bin
      = A'·(B + Bin) + B·Bin
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 2의 보수를 이용한 뺄셈

```
2의 보수 뺄셈 회로:

A ──────────────┐
               │
B ────┬───NOT──┴──→ Adder (A + ~B + 1)
      │          │
      └──+1───────┘

구현:
1. B를 비반전 (1의 보수)
2. Cin = 1 (2의 보수)
3. A + ~B + 1 = A - B

예시 (4비트):
A = 0010 (2)
B = 0001 (1)

~B = 1110
A + ~B + 1 = 0010 + 1110 + 1
          = 0010 + 1111
          = 0001 (Cout=1 무시)

결과: 2 - 1 = 1 ✓
```

### 풀 뺄셈기 회로

```
풀 뺄셈기 논리 회로:

A ──┬─────────┬─── XOR ──── Diff
B ──┤ XOR     │   │
    │         │   │
Bin ┴─────────┴───┘

Bout 회로:
A' · (B + Bin) + B · Bin

불 대수식:
Diff = A ⊕ B ⊕ Bin
Bout = A'·B + B·Bin + A'·Bin
```

### 리플 보로우 뺄셈기

```
n비트 리플 보로우 뺄셈기:

A3 B3 ────────┐
A2 B2 ─────┐ │
A1 B1 ───┐ │ │
A0 B0 ───┴─┴─┴── FS ─ FS ─ FS ─ FS
     │  │  │  │   │   │   │   │
     └──┴──┴──┴───┴───┴───┴───┴──→ Borrow Chain

FS = Full Subtracter
지연: (2n - 1) 게이트 (RCA와 동일)
```

### 가감산기 (Adder-Subtractor)

```
n비트 가감산기:

A[n-1:0] ────────┐
                │
B[n-1:0] ──┬────┴──→ Adder
           │     │
    M ─────┴──┬──┘
              │
         MUX(1/M)──→ Cin

동작:
M=0 (Add):  A + B + 0
M=1 (Sub):  A + ~B + 1 = A - B

회로:
M=1이면 B를 반전 (XOR gate)
M=1이면 Cin=1
```

### 전파 지연 분석

```
뺄셈기 지연:

1. 2의 보수 방식 (가산기 재사용):
   - B 반전: t_NOT
   - 가산기: t_adder
   - 총: t_NOT + t_adder

2. 풀 뺄셈기:
   - Diff: 2~3 게이트 (XOR 체인)
   - Bout: 2~3 게이트
   - n비트: (2n - 1) 게이트

3. 리플 보로우:
   - 최악 케이스: 모든 비트에서 빌림 발생
   - t_total = (2n - 1) × t_gate
```

## Ⅲ. 융합 비교

### 하프 뺄셈기 vs 풀 뺄셈기

| 비교 항목 | 하프 뺄셈기 | 풀 뺄셈기 |
|----------|-----------|----------|
| 입력 | A, B (2개) | A, B, Bin (3개) |
| 출력 | Diff, Borrow (2개) | Diff, Bout (2개) |
| 빌림 처리 | 불가 | 가능 |
| 응용 | LSB 뺄셈 | 일반 뺄셈 |

### 뺄셈 구현 방식 비교

| 방식 | 원리 | 지연 | 하드웨어 | 응용 |
|------|------|------|----------|------|
| 직접 뺄셈 | 풀 뺄셈기 | O(n) | 별도 필요 | 드뭄 |
| 2의 보수 | A + ~B + 1 | O(log n) | 가산기 재사용 | 일반적 |
| 가감산기 | MUX + 가산기 | O(log n) | 가산기 + MUX | ALU |

### 가산기 vs 뺄셈기

| 비교 항목 | 가산기 | 뺄셈기 |
|----------|--------|--------|
| 연산 | A + B | A - B |
| 캐리 | Carry | Borrow |
| 2의 보수 | 필요 없음 | ~B + 1 |
| ALU에서 | 기본 | 파생 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 32비트 가감산기

```
32비트 ALU 가감산기:

구조:
- 32비트 CLAA (캐리 룩어헤드)
- 32개 XOR 게이트 (B 반전)
- 1개 MUX (Cin 선택)

동작:
Mode=0: A + B + 0 (덧셈)
Mode=1: A + ~B + 1 (뺄셈)

지연:
- XOR: 1 게이트
- CLAA: 8 게이트
- 총: 9 게이트

@ 120ps: t_total = 1080ps
```

### 오버플로/언더플로 검출

```
부호 있는 뺄셈 오버플로:

조건:
- A > 0, B < 0, 결과 < 0 → 언더플로
- A < 0, B > 0, 결과 > 0 → 오버플로

검출:
Overflow = Cout ⊕ C[n-1]
         = (MSB-1 캐리) ⊕ (MSB 캐리)

또는:
Overflow = (A_MSB ≠ B_MSB) ∧ (Diff_MSB ≠ A_MSB)
```

### DSP 뺄셈

```
FIR 필터 계수:
y[n] = Σ h[k] × x[n-k]

양수/음수 계수:
- 양수: 가산
- 음수: 뺄셈 (2의 보수)

CSA + CLAA 구조:
1. 부분 곱 생성
2. 양수/음수 분리
3. CSA로 합산
4. CLAA로 최종 합
```

## Ⅴ. 기대효과 및 결론

뺄셈은 2의 보수로 가산기로 구현한다. 가감산기는 ALU의 핵심이다.

## 📌 관련 개념 맵

```
뺄셈기
├── 구현 방식
│   ├── 2의 보수 (A + ~B + 1) ★
│   ├── 풀 뺄셈기
│   └── 가감산기
├── 하프 뺄셈기
│   ├── Diff = A ⊕ B
│   └── Borrow = A' · B
├── 풀 뺄셈기
│   ├── Diff = A ⊕ B ⊕ Bin
│   └── Bout = A'·B + B·Bin + A'·Bin
└── 응용
    ├── ALU
    ├── DSP 필터
    └── 부호 있는 연산
```

## 👶 어린이를 위한 3줄 비유 설명

1. 뺄셈기는 덧셈기로 뺄셈을 하는 방법을 사용해요. 5 - 3을 계산할 때, 5 + (-3)으로 바꾸는데, -3은 "3을 뒤집고 1 더하기"로 만들어요
2. 2진수에서 3은 0011인데, 이를 뒤집으면 1100이 되고, 여기에 1을 더하면 1101이 돼요. 이게 -3이에요
3. 그래서 5 - 3 = 5 + (-3) = 0101 + 1101 = 0010(2)가 돼서 정답을 구해요

```python
# 뺄셈기 시뮬레이션

from typing import Tuple


class HalfSubtracter:
    """하프 뺄셈기"""

    def subtract(self, a: int, b: int) -> Tuple[int, int]:
        """
        1비트 뺄셈

        Args:
            a: 피감수
            b: 감수

        Returns:
            (diff, borrow): 차와 빌림
        """
        if a not in [0, 1] or b not in [0, 1]:
            raise ValueError("입력은 0 또는 1이어야 합니다")

        diff = a ^ b
        borrow = (~a & b) & 1

        return diff, borrow


class FullSubtracter:
    """풀 뺄셈기"""

    def subtract(self, a: int, b: int, borrow_in: int) -> Tuple[int, int]:
        """
        1비트 뺄셈 (빌림 포함)

        Args:
            a: 피감수
            b: 감수
            borrow_in: 입력 빌림

        Returns:
            (diff, borrow_out): 차와 출력 빌림
        """
        if a not in [0, 1] or b not in [0, 1] or borrow_in not in [0, 1]:
            raise ValueError("입력은 0 또는 1이어야 합니다")

        # Diff = A ⊕ B ⊕ Bin
        diff = a ^ b ^ borrow_in

        # Bout = A'·B + B·Bin + A'·Bin
        borrow_out = ((~a & b) | (b & borrow_in) | (~a & borrow_in)) & 1

        return diff, borrow_out


class TwosComplementSubtracter:
    """2의 보수 뺄셈기"""

    def __init__(self, bits: int):
        """
        n비트 뺄셈기

        Args:
            bits: 비트 수
        """
        self.bits = bits

    def subtract(self, a: int, b: int) -> Tuple[int, int]:
        """
        A - B = A + (~B + 1)

        Args:
            a: 피감수
            b: 감수

        Returns:
            (result, overflow): 결과와 오버플로우
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다")

        # ~B + 1 (2의 보수)
        b_complement = ((~b) & ((1 << self.bits) - 1)) + 1

        # A + ~B + 1
        result = (a + b_complement) & ((1 << self.bits) - 1)

        # 오버플로우 검출 (부호 있는 경우)
        a_sign = (a >> (self.bits - 1)) & 1
        b_sign = (b >> (self.bits - 1)) & 1
        result_sign = (result >> (self.bits - 1)) & 1

        # 오버플로: 부호가 바뀌는 경우
        overflow = (a_sign != b_sign) and (result_sign != a_sign)

        return result, overflow

    def print_subtraction(self, a: int, b: int):
        """뺄셈 과정 출력"""
        result, overflow = self.subtract(a, b)

        print(f"\n{a} ({a:0{self.bits}b}) - {b} ({b:0{self.bits}b}) = ", end="")

        if overflow:
            print(f"{result} ({result:0{self.bits}b}) [오버플로우]")
        else:
            print(f"{result} ({result:0{self.bits}b})")

        # 2의 보수 계산 과정
        b_inv = (~b) & ((1 << self.bits) - 1)
        b_comp = (b_inv + 1) & ((1 << self.bits) - 1)

        print(f"  ~B = {b_inv:0{self.bits}b}")
        print(f"  ~B + 1 = {b_comp:0{self.bits}b}")
        print(f"  A + (~B + 1) = {a:0{self.bits}b} + {b_comp:0{self.bits}b} = {result:0{self.bits}b}")


class AdderSubtractor:
    """가감산기"""

    def __init__(self, bits: int):
        """
        n비트 가감산기

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.subtractor = TwosComplementSubtracter(bits)

    def calculate(self, a: int, b: int, subtract: bool = False) -> Tuple[int, int]:
        """
        가산 또는 뺄셈

        Args:
            a: 첫 번째 수
            b: 두 번째 수
            subtract: True면 뺄셈, False면 덧셈

        Returns:
            (result, overflow): 결과와 오버플로우
        """
        if subtract:
            return self.subtractor.subtract(a, b)
        else:
            result = (a + b) & ((1 << self.bits) - 1)
            overflow = (a + b) >= (1 << self.bits)
            return result, overflow


def demonstration():
    """뺄셈기 데모"""
    print("=" * 70)
    print("뺄셈기 (Subtracter) 데모")
    print("=" * 70)

    # 하프 뺄셈기
    print("\n[하프 뺄셈기 진리표]")
    print(f"{'A':<2} {'B':<2} {'Diff':<6} {'Borrow':<8}")
    print("-" * 25)

    hs = HalfSubtracter()
    for a in [0, 1]:
        for b in [0, 1]:
            diff, borrow = hs.subtract(a, b)
            print(f"{a:<2} {b:<2} {diff:<6} {borrow:<8}")

    # 풀 뺄셈기
    print("\n[풀 뺄셈기 예시]")
    fs = FullSubtracter()

    test_cases = [(1, 0, 0), (0, 1, 0), (1, 1, 1), (0, 0, 1)]
    for a, b, bin_ in test_cases:
        diff, bout = fs.subtract(a, b, bin_)
        print(f"  {a} - {b} - {bin_} = {diff}, Borrow = {bout}")

    # 8비트 2의 보수 뺄셈
    print("\n" + "=" * 70)
    print("8비트 2의 보수 뺄셈")
    print("=" * 70)

    sub8 = TwosComplementSubtracter(8)

    tests = [
        (100, 50),     # 100 - 50 = 50
        (50, 100),     # 50 - 100 = -50
        (200, 50),     # 200 - 50 = 150
        (50, 200),     # 50 - 200 = -150 (underflow)
    ]

    for a, b in tests:
        sub8.print_subtraction(a, b)

    # 가감산기
    print("\n" + "=" * 70)
    print("가감산기 (Adder-Subtractor)")
    print("=" * 70)

    as_unit = AdderSubtractor(8)

    print("\n덧셈 (Mode=0):")
    result, _ = as_unit.calculate(100, 50, subtract=False)
    print(f"  100 + 50 = {result}")

    print("\n뺄셈 (Mode=1):")
    result, _ = as_unit.calculate(100, 50, subtract=True)
    print(f"  100 - 50 = {result}")

    result, overflow = as_unit.calculate(50, 100, subtract=True)
    print(f"  50 - 100 = {result}", end="")
    if overflow:
        print(" [오버플로우]")
    else:
        print()


if __name__ == "__main__":
    demonstration()
```
