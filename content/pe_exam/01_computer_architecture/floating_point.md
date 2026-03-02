+++
title = "부동 소수점 수 (Floating Point Number)"
date = 2025-02-27

[extra]
categories = "pe_exam-computer_architecture"
+++

# 부동 소수점 수 (Floating Point Number)

## 핵심 인사이트 (3줄 요약)
> **실수를 가수부와 지수부로 분리하여 넓은 범위를 근사적으로 표현**하는 방식. IEEE 754 표준이 국제 표준이며, 정밀도 문제(0.1 + 0.2 ≠ 0.3)가 존재. 단정도(32bit)/배정도(64bit)/반정밀도(16bit)가 실무에서 사용된다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 부동 소수점 수(Floating Point Number)는 **소수점의 위치가 고정되지 않고 움직일 수 있는(Floating) 방식으로 실수를 표현**하는 수 체계로, 과학적 표기법(Scientific Notation)을 2진수로 구현한 것이다. IEEE 754 표준이 전 세계 표준이다.

> 💡 **비유**: 부동 소수점은 **"과학적 표기법"** 같아요. 123,000,000을 1.23 × 10^8로 쓰는 것처럼, 아주 크거나 작은 수를 **가수(1.23)**와 **지수(8)**로 나눠서 표현해요. 숫자의 범위는 엄청 넓지만, 정밀도(유효 숫자)는 한정돼 있죠!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 고정 소수점의 한계**: 32비트 고정 소수점은 범위가 -2^31 ~ 2^31-1로 제한, 큰 수/작은 수 표현 불가
2. **기술적 필요성 - 과학 계산**: 천문학(10^30), 원자 물리(10^-30) 등 극단적 범위의 수 표현 필요
3. **시장/산업 요구 - 통일된 표준**: 초기에는 각 벤더마다 다른 형식 → 1985년 IEEE 754 표준화

**핵심 목적**: **넓은 동적 범위(Dynamic Range)**를 가진 실수 표현

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **부호 비트(Sign)** | 양수/음수 구분 | 0=양수, 1=음수 | + / - |
| **지수부(Exponent)** | 크기 스케일링 | Bias 방식 | 10^n의 n |
| **가수부(Mantissa)** | 유효 숫자 | 정규화된 값 | 1.xxxxx |
| **Bias** | 음수 지수 표현 | 127(32bit), 1023(64bit) | 오프셋 |
| **Hidden Bit** | 암시적 1 | 정규수에서 1.xxx의 1 | 생략된 숫자 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    IEEE 754 부동 소수점 형식                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [단정도 (Single Precision, 32-bit)]                               │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ S │    Exponent    │          Mantissa                      │  │
│   │1bit│    8 bits      │         23 bits                        │  │
│   └─────────────────────────────────────────────────────────────┘  │
│   Bias = 127                                                        │
│   범위: ±3.4 × 10^38, 정밀도: ~7자리                               │
│                                                                     │
│   [배정도 (Double Precision, 64-bit)]                               │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ S │    Exponent    │          Mantissa                      │  │
│   │1bit│   11 bits      │         52 bits                        │  │
│   └─────────────────────────────────────────────────────────────┘  │
│   Bias = 1023                                                       │
│   범위: ±1.8 × 10^308, 정밀도: ~15자리                             │
│                                                                     │
│   [반정밀도 (Half Precision, 16-bit) - AI/딥러닝용]                 │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ S │  Exponent  │    Mantissa                                │  │
│   │1bit│   5 bits   │    10 bits                                 │  │
│   └─────────────────────────────────────────────────────────────┘  │
│   Bias = 15                                                         │
│   범위: ±6.5 × 10^4, 정밀도: ~3자리                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    부동 소수점 표현 원리                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   값 = (-1)^S × (1 + Mantissa) × 2^(Exponent - Bias)               │
│                                                                     │
│   예: -6.625를 단정도로 표현                                        │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ 1단계: 10진수 → 2진수                                       │  │
│   │   6.625 = 110.101₂                                          │  │
│   │   (6 = 110, 0.625 = 0.5 + 0.125 = .1 + .001 = .101)         │  │
│   │                                                              │  │
│   │ 2단계: 정규화 (1.xxxx × 2^n 형태)                           │  │
│   │   110.101₂ = 1.10101 × 2^2                                  │  │
│   │                                                              │  │
│   │ 3단계: 각 필드 값 계산                                       │  │
│   │   Sign = 1 (음수)                                           │  │
│   │   Exponent = 2 + 127 = 129 = 10000001₂                      │  │
│   │   Mantissa = 10101... (23비트로 패딩)                        │  │
│   │                                                              │  │
│   │ 4단계: 최종 비트 패턴                                        │  │
│   │   1 10000001 10101000000000000000000                        │  │
│   │   │    │            │                                        │  │
│   │   S    E            M                                        │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    IEEE 754 특수 값                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌───────────────┬───────────────────┬───────────────────────┐    │
│   │   특수 값     │     Exponent      │       Mantissa        │    │
│   ├───────────────┼───────────────────┼───────────────────────┤    │
│   │  +0           │  000...000 (0)    │  000...000 (0)        │    │
│   │  -0           │  000...000 (0)    │  000...000 (0)        │    │
│   │  비정규수     │  000...000 (0)    │  ≠ 0                 │    │
│   │  정규수       │  001...110        │  임의                 │    │
│   │  +∞           │  111...111 (Max)  │  000...000 (0)        │    │
│   │  -∞           │  111...111 (Max)  │  000...000 (0)        │    │
│   │  NaN          │  111...111 (Max)  │  ≠ 0                 │    │
│   └───────────────┴───────────────────┴───────────────────────┘    │
│                                                                     │
│   NaN 종류:                                                        │
│   - Quiet NaN (qNaN): 연산이 조용히 진행됨                         │
│   - Signaling NaN (sNaN): 예외 발생                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 10진수 → ② 2진수 변환 → ③ 정규화 → ④ Bias 계산 → ⑤ 비트 패턴 생성
```

- **1단계 - 10진수 입력**: 실수를 입력받음
- **2단계 - 2진수 변환**: 정수부/소수부를 각각 2진수로 변환
- **3단계 - 정규화**: 소수점을 이동시켜 1.xxxx × 2^n 형태로 변환
- **4단계 - Bias 계산**: 지수에 Bias를 더해 양수로 만듦
- **5단계 - 비트 패턴 생성**: Sign, Exponent, Mantissa를 조합

**핵심 알고리즘/공식** (해당 시 필수):

```
[IEEE 754 표현 공식]

단정도 (32-bit):
Value = (-1)^S × (1 + M × 2^-23) × 2^(E-127)

배정도 (64-bit):
Value = (-1)^S × (1 + M × 2^-52) × 2^(E-1023)

[정밀도 계산]

단정도 유효 자릿수:
log10(2^24) ≈ 7.22 자리

배정도 유효 자릿수:
log10(2^53) ≈ 15.95 자리

[반정밀도 유효 자릿수]:
log10(2^11) ≈ 3.31 자리

[머신 엡실론 (Machine Epsilon)]
- 연속된 두 부동소수점 수 사이의 최대 상대 간격
- 단정도: ε = 2^-23 ≈ 1.19 × 10^-7
- 배정도: ε = 2^-52 ≈ 2.22 × 10^-16

[정밀도 문제 예시]
0.1(10진) = 0.00011001100110011...(2진, 무한 반복)

0.1 + 0.2 ≠ 0.3 인 이유:
1. 0.1과 0.2 모두 2진수로 정확히 표현 불가
2. 근사값으로 저장됨
3. 근사값 + 근사값 = 더 큰 오차

[반올림 모드 (Rounding Modes)]
1. Round to Nearest Even (기본): 가장 가까운 짝수로
2. Round toward +∞: 양의 무한대 방향으로
3. Round toward -∞: 음의 무한대 방향으로
4. Round toward 0: 0 방향으로 (버림)

[비정규수 (Denormalized Numbers)]
- 지수가 0이고 가수가 0이 아닌 수
- 아주 작은 수를 표현 (Underflow 방지)
- 값 = (-1)^S × (0 + M × 2^-23) × 2^-126 (단정도)
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass
from typing import Tuple, Optional
import struct
import math

@dataclass
class IEEE754Components:
    """IEEE 754 구성 요소"""
    sign: int        # 0 or 1
    exponent: int    # 지수 (bias 적용 전)
    mantissa: int    # 가수 (정수)
    is_normalized: bool = True
    is_nan: bool = False
    is_infinity: bool = False
    is_zero: bool = False

class IEEE754Converter:
    """IEEE 754 부동 소수점 변환기"""

    # 상수
    SINGLE_BIAS = 127
    DOUBLE_BIAS = 1023
    SINGLE_EXP_BITS = 8
    DOUBLE_EXP_BITS = 11
    SINGLE_MANT_BITS = 23
    DOUBLE_MANT_BITS = 52

    @staticmethod
    def float_to_binary(value: float, bits: int = 32) -> str:
        """부동소수점을 2진 문자열로 변환"""
        if bits == 32:
            packed = struct.pack('>f', value)
        else:
            packed = struct.pack('>d', value)

        binary = ''.join(f'{b:08b}' for b in packed)
        return binary

    @staticmethod
    def binary_to_float(binary: str, bits: int = 32) -> float:
        """2진 문자열을 부동소수점으로 변환"""
        if bits == 32:
            # 32비트: 부호 1, 지수 8, 가수 23
            sign = int(binary[0], 2)
            exp = int(binary[1:9], 2)
            mant = int(binary[9:], 2)

            if exp == 0:
                if mant == 0:
                    return 0.0 if sign == 0 else -0.0
                # 비정규수
                return (-1)**sign * (mant / 2**23) * 2**(-126)
            elif exp == 255:
                if mant == 0:
                    return float('inf') if sign == 0 else float('-inf')
                return float('nan')

            # 정규수
            return (-1)**sign * (1 + mant / 2**23) * 2**(exp - 127)
        return 0.0

    @classmethod
    def decompose(cls, value: float, bits: int = 32) -> IEEE754Components:
        """부동소수점 분해"""
        binary = cls.float_to_binary(value, bits)

        if bits == 32:
            sign = int(binary[0])
            exp = int(binary[1:9], 2)
            mant = int(binary[9:], 2)

            # 특수 값 처리
            if exp == 0:
                if mant == 0:
                    return IEEE754Components(sign, 0, 0, is_zero=True)
                # 비정규수
                return IEEE754Components(sign, 0, mant, is_normalized=False)

            if exp == 255:
                if mant == 0:
                    return IEEE754Components(sign, exp, 0, is_infinity=True)
                return IEEE754Components(sign, exp, mant, is_nan=True)

            # 정규수
            actual_exp = exp - cls.SINGLE_BIAS
            return IEEE754Components(sign, actual_exp, mant)

        return IEEE754Components(0, 0, 0)

    @staticmethod
    def decimal_to_ieee754(value: float) -> Tuple[int, int, int]:
        """10진수를 IEEE 754 단정도로 변환 (단계별)"""
        # 부호 결정
        sign = 1 if value < 0 else 0
        value = abs(value)

        # 특수 값 처리
        if value == 0:
            return sign, 0, 0
        if math.isinf(value):
            return sign, 255, 0
        if math.isnan(value):
            return sign, 255, 1

        # 2진수로 변환 (정수부 + 소수부)
        int_part = int(value)
        frac_part = value - int_part

        # 정수부 2진수
        int_binary = bin(int_part)[2:] if int_part > 0 else ''

        # 소수부 2진수 (최대 150비트까지)
        frac_binary = ''
        temp = frac_part
        for _ in range(150):
            temp *= 2
            if temp >= 1:
                frac_binary += '1'
                temp -= 1
            else:
                frac_binary += '0'
            if temp == 0:
                break

        # 정규화
        if int_binary:
            # 정수부가 있는 경우
            exp = len(int_binary) - 1
            mantissa_binary = int_binary[1:] + frac_binary
        else:
            # 소수부만 있는 경우
            first_one = frac_binary.find('1')
            if first_one == -1:
                return sign, 0, 0  # 0
            exp = -(first_one + 1)
            mantissa_binary = frac_binary[first_one + 1:]

        # Bias 적용
        biased_exp = exp + 127

        # 오버플로우/언더플로우 체크
        if biased_exp >= 255:
            return sign, 255, 0  # Infinity
        if biased_exp <= 0:
            # 비정규수 (간단히 0으로 처리)
            return sign, 0, 0

        # 가수를 23비트로 패딩/자르기
        mantissa_binary = mantissa_binary[:23].ljust(23, '0')
        mantissa = int(mantissa_binary, 2)

        return sign, biased_exp, mantissa

class FloatingPointPrecisionDemo:
    """부동 소수점 정밀도 데모"""

    @staticmethod
    def demonstrate_precision_issues():
        """정밀도 문제 시연"""
        print("=== Floating Point Precision Issues ===\n")

        # 0.1 + 0.2 문제
        a = 0.1
        b = 0.2
        result = a + b
        print(f"0.1 + 0.2 = {result}")
        print(f"0.1 + 0.2 == 0.3? {result == 0.3}")
        print(f"0.1 + 0.2 - 0.3 = {result - 0.3}")

        # 비트 패턴 확인
        print(f"\n0.1 비트 패턴: {IEEE754Converter.float_to_binary(0.1)}")
        print(f"0.2 비트 패턴: {IEEE754Converter.float_to_binary(0.2)}")
        print(f"0.3 비트 패턴: {IEEE754Converter.float_to_binary(0.3)}")

        # 머신 엡실론
        print(f"\n=== Machine Epsilon ===")
        eps_single = 2 ** -23
        eps_double = 2 ** -52
        print(f"단정도 ε: {eps_single:.15e}")
        print(f"배정도 ε: {eps_double:.15e}")

        # 큰 수에 작은 수 더하기
        print(f"\n=== Large + Small Number ===")
        big = 1e16
        small = 1.0
        print(f"{big} + {small} = {big + small}")
        print(f"({big} + {small}) - {big} = {(big + small) - big}")

    @staticmethod
    def safe_float_compare(a: float, b: float, tolerance: float = 1e-9) -> bool:
        """안전한 부동 소수점 비교"""
        return abs(a - b) < tolerance

    @staticmethod
    def kahan_sum(numbers: list) -> float:
        """Kahan 합계 알고리즘 (오차 보정)"""
        total = 0.0
        compensation = 0.0

        for num in numbers:
            y = num - compensation
            temp = total + y
            compensation = (temp - total) - y
            total = temp

        return total

# 사용 예시
if __name__ == "__main__":
    # 변환 데모
    print("=== IEEE 754 Conversion Demo ===\n")

    value = -6.625
    sign, exp, mant = IEEE754Converter.decimal_to_ieee754(value)

    print(f"Value: {value}")
    print(f"Sign: {sign}")
    print(f"Exponent (biased): {exp} (binary: {exp:08b})")
    print(f"Mantissa: {mant} (binary: {mant:023b})")

    # 전체 비트 패턴
    full_pattern = f"{sign}{exp:08b}{mant:023b}"
    print(f"Full pattern: {full_pattern}")

    # 정밀도 문제 데모
    print("\n")
    FloatingPointPrecisionDemo.demonstrate_precision_issues()

    # Kahan 합계 데모
    print("\n=== Kahan Summation Demo ===")
    numbers = [0.1] * 10

    naive_sum = sum(numbers)
    kahan_sum_result = FloatingPointPrecisionDemo.kahan_sum(numbers)

    print(f"10 × 0.1 (naive) = {naive_sum}")
    print(f"10 × 0.1 (Kahan) = {kahan_sum_result}")
    print(f"Expected: 1.0")
    print(f"Naive error: {abs(naive_sum - 1.0):.15e}")
    print(f"Kahan error: {abs(kahan_sum_result - 1.0):.15e}")
