+++
title = "하프 가산기 (Half Adder)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 하프 가산기 (Half Adder)

## 핵심 인사이트 (3줄 요약)
1. 하프 가산기는 1비트 이진수 더하기를 수행하는 조합 회로로, XOR 게이트로 합(Sum)을 AND 게이트로 자리올림(Carry)을 생성한다
2. 2개 입력(A, B)에 대해 Sum = A⊕B, Carry = A·B를 출력하며, 캐리 입력이 없어 단독으로는 다비트 가산에 사용할 수 없다
3. 기술사시험에서는 하프 가산기와 풀 가산기의 차이, 리플 캐리 가산기 구성, 전파 지연 분석이 핵심이다

## Ⅰ. 개요 (500자 이상)

하프 가산기(Half Adder)는 **1비트 이진 더하기**를 수행하는 가장 기본적인 조합 논리 회로이다. 두 개의 1비트 입력 A와 B를 받아 합(Sum)과 자리올림(Carry out)을 출력한다. 하프 가산기는 이전 단계의 캐리를 고려하지 않으므로, 다비트 이진수 더하기를 위해서는 캐리 입력을 처리할 수 있는 풀 가산기(Full Adder)가 필요하다.

```
하프 가산기 블록도:
    A ──┐
         │
    B ───┤─── HA ──┬── Sum (A⊕B)
                │
                └── Carry (A·B)
```

**합(Sum)**은 XOR 연산으로 구현된다. A와 B가 다르면 1, 같으면 0이 된다. 이는 1비트 이진수 더하기의 합 비트를 정확히 표현한다.
- 0+0=0, 0+1=1, 1+0=1, 1+1=0(캐리 발생)

**자리올림(Carry out)**은 AND 연산으로 구현된다. A와 B가 모두 1일 때만 상위 비트로 1을 캐리한다.
- 1+1=10₂ 이므로 Sum=0, Carry=1

```
하프 가산기 진리표:
| A | B | Sum | Carry | 설명 |
|---|---|-----|-------|------|
| 0 | 0 |  0  |   0   | 0+0=00 |
| 0 | 1 |  1  |   0   | 0+1=01 |
| 1 | 0 |  1  |   0   | 1+0=01 |
| 1 | 1 |  0  |   1   | 1+1=10 |
```

하프 가산기는 LSB(Least Significant Bit) 더하기에 사용된다. 최상위 비트가 아닌 다른 비트 위치에서는 이전 단계의 캐리를 처리해야 하므로 풀 가산기가 필요하다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 하프 가산기 회로 구조

```
하프 가산기 논리 회로:
    A ──────┬─────── AND ──── Carry
            │       │
    B ──────┼───────┤
            │       │
            └── XOR ──── Sum

회로 구성:
1. XOR 게이트: Sum = A ⊕ B
2. AND 게이트: Carry = A · B

게이트 레벨 구현 (CMOS):
XOR 게이트: 6-10개 트랜지스터
AND 게이트: 6개 트랜지스터 (NAND + Inverter)
총 트랜지스터: 12-16개
```

### 불 대수식

```
Sum = A ⊕ B = A·B' + A'·B

Carry = A · B

논리 최적화:
- XOR는 2-level SOP로 표현 가능
- AND는 단일 게이트로 구현
- 공통 서브텀 없음 (최적화 필요 없음)
```

### 전파 지연 분석

```
하프 가산기 타이밍:

입력 → 출력 경로:
1. A,B → Sum (XOR)
   t_P,SUM = t_XOR = 2~3게이트 지연

2. A,B → Carry (AND)
   t_P,CARRY = t_AND = 1게이트 지연

게이트 지연 (CMOS 65nm):
- t_AND = 50ps
- t_XOR = 120ps
- t_inverter = 30ps

t_P,SUM ≈ 120ps
t_P,CARRY ≈ 50ps

Critical Path: Sum 출력 (XOR 경로)
```

### 전력 소비 분석

```
동적 전력:
P_dynamic = α · C_L · V_DD² · f

하프 가산기 기생 커패시턴스:
- C_XOR ≈ 2fF
- C_AND ≈ 0.8fF
- 총 C_L ≈ 2.8fF

@ 1GHz, V_DD=1.0V, α=0.25:
P_dynamic ≈ 0.25 × 2.8fF × 1.0² × 1GHz
          ≈ 0.7μW per gate
```

## Ⅲ. 융합 비교

### 하프 가산기 vs 풀 가산기

| 비교 항목 | 하프 가산기 | 풀 가산기 |
|----------|-----------|----------|
| 입력 수 | 2 (A, B) | 3 (A, B, Carry_in) |
| Carry 입력 | 없음 | 있음 |
| 게이트 수 | 2 (XOR, AND) | 5 (2 XOR, 2 AND, 1 OR) |
| 용도 | LSB 더하기 | 일반 비트 더하기 |
| 단독 사용 | 다비트 불가 | 다비트 가능 |

### 다비트 가산기 구성

| 가산기 유형 | 하프 가산기 수 | 풀 가산기 수 | 총 지연 |
|-----------|--------------|-------------|---------|
| 4비트 RCA | 1 | 3 | 3 × t_FA + t_HA |
| 8비트 RCA | 1 | 7 | 7 × t_FA + t_HA |
| 16비트 RCA | 1 | 15 | 15 × t_FA + t_HA |
| 32비트 RCA | 1 | 31 | 31 × t_FA + t_HA |

RCA = Ripple Carry Adder
t_FA = 풀 가산기 지연
t_HA = 하프 가산기 지연

## Ⅳ. 실무 적용 및 기술사적 판단

### 4비트 리플 캐리 가산기 (Ripple Carry Adder)

```
4비트 RCA 구성:
A3 B3 ──────────┐
A2 B2 ─────┐    │
A1 B1 ──┐  │    │
A0 B0 HA ─┴──┴──┴── FA3 ── S3 C3
        │  │  │    │
        └──┴──┴────┴─── C_out

구조:
Bit 0: HA (하프 가산기)
Bit 1-3: FA (풀 가산기 3개)

총 지연:
t_total = t_HA + 3 × t_FA
        = t_XOR + 3 × (2 × t_XOR)
        = 7 × t_XOR

@ t_XOR = 120ps:
t_total = 840ps
```

### 하프 가산자 응용 사례

```
1. LSB 더하기:
   - 모든 다비트 가산기의 첫 번째 스테이지

2. 주소 계산:
   - PC + 1 (단순 증가)

3. 인덱스 계산:
   - 배열 인덱스 증가

4. 간단한 카운터:
   - 1비트 카운터 구현

5. 패리티 계산:
   - XOR를 이용한 패리티 비트 생성
```

## Ⅴ. 기대효과 및 결론

하프 가산기는 1비트 더하기의 기초이다. LSB 더하기에 사용되며, 풀 가산기와 결합하여 다비트 가산기를 구성한다.

## 📌 관련 개념 맵

```
하프 가산기
├── 정의: 1비트 더하기 (캐리 입력 없음)
├── 구성
│   ├── XOR 게이트 (Sum)
│   └── AND 게이트 (Carry)
├── 제약
│   ├── 캐리 입력 없음
│   └── 다비트 가산에 부적합
└── 응용
    ├── LSB 더하기
    ├── 풀 가산기 구성 요소
    └── 리플 캐리 가산기
```

## 👶 어린이를 위한 3줄 비유 설명

1. 하프 가산기는 한 자리 숫자 두 개를 더하는 계산기예요. 예를 들어 0+0=0, 0+1=1, 1+0=1, 1+1=10(합은 0, 캐리는 1)로 계산해요
2. 1+1 같은 경우는 답이 10이 돼서 자리올림이 발생하는데, 하프 가산기는 합과 자리올림을 따로 출력해요
3. 여러 자리 숫자를 더하려면 이전 자리에서 올라온 자리올림까지 고려해야 하는데, 하프 가산기는 이걸 못해서 풀 가산기가 필요해요

```python
# 하프 가산기 시뮬레이션 및 분석 도구

class HalfAdder:
    """
    하프 가산기 (Half Adder) 시뮬레이션
    1비트 이진수 더하기 수행
    """

    def __init__(self):
        """하프 가산기 초기화"""
        self.name = "Half Adder"

    def add(self, a: int, b: int) -> tuple[int, int]:
        """
        1비트 더하기 수행

        Args:
            a: 입력 A (0 또는 1)
            b: 입력 B (0 또는 1)

        Returns:
            (sum, carry): 합과 자리올림
        """
        if a not in [0, 1] or b not in [0, 1]:
            raise ValueError("입력은 0 또는 1이어야 합니다")

        # XOR: 합 계산
        sum_bit = a ^ b

        # AND: 캐리 계산
        carry = a & b

        return sum_bit, carry

    def truth_table(self) -> list[dict]:
        """진리표 생성"""
        table = []
        for a in [0, 1]:
            for b in [0, 1]:
                sum_bit, carry = self.add(a, b)
                table.append({
                    'A': a,
                    'B': b,
                    'Sum': sum_bit,
                    'Carry': carry,
                    'Result': f"{carry}{sum_bit}₂"
                })
        return table

    def print_truth_table(self):
        """진리표 출력"""
        print("\n" + "="*50)
        print("하프 가산기 (Half Adder) 진리표")
        print("="*50)
        print(f"{'A':>4} {'B':>4} {'Sum':>6} {'Carry':>8} {'Result':>8}")
        print("-" * 50)

        for row in self.truth_table():
            print(f"{row['A']:>4} {row['B']:>4} {row['Sum']:>6} {row['Carry']:>8} {row['Result']:>8}")

        print("="*50)


class RippleCarryAdder:
    """
    리플 캐리 가산기 (Ripple Carry Adder)
    하프 가산기 + 풀 가산기 조합
    """

    def __init__(self, bits: int):
        """
        n비트 리플 캐리 가산기 생성

        Args:
            bits: 비트 수 (4, 8, 16, 32 등)
        """
        self.bits = bits
        self.name = f"{bits}-bit Ripple Carry Adder"
        self.ha = HalfAdder()

    def full_add(self, a: int, b: int, carry_in: int) -> tuple[int, int]:
        """
        풀 가산기 동작 (하프 가산기 2개로 구현)

        Args:
            a: 입력 A (0 또는 1)
            b: 입력 B (0 또는 1)
            carry_in: 캐리 입력

        Returns:
            (sum, carry_out): 합과 자리올림 출력
        """
        # 첫 번째 하프 가산기: A + B
        sum1, carry1 = self.ha.add(a, b)

        # 두 번째 하프 가산기: sum1 + carry_in
        sum_final, carry2 = self.ha.add(sum1, carry_in)

        # 캐리 출력: carry1 OR carry2
        carry_out = carry1 | carry2

        return sum_final, carry_out

    def add(self, a: int, b: int) -> tuple[int, int]:
        """
        n비트 더하기 수행

        Args:
            a: 피가산수 (0 ~ 2^n-1)
            b: 가산수 (0 ~ 2^n-1)

        Returns:
            (sum, overflow): 합과 오버플로우 플래그
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다 (0 ~ {2**self.bits - 1})")

        result = 0
        carry = 0

        # LSB: 하프 가산기 사용
        sum_bit, carry = self.ha.add(a & 1, b & 1)
        result |= sum_bit

        # 나머지 비트: 풀 가산기 사용
        for i in range(1, self.bits):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1
            sum_bit, carry = self.full_add(a_bit, b_bit, carry)
            result |= (sum_bit << i)

        overflow = carry

        return result, overflow

    def analyze_delay(self, gate_delay_ps: int = 120) -> dict:
        """
        전파 지연 분석

        Args:
            gate_delay_ps: 게이트 지연 (피코초)

        Returns:
            지연 분석 결과
        """
        # 하프 가산기: XOR (1게이트)
        t_ha = gate_delay_ps

        # 풀 가산기: 2 XOR (2게이트)
        t_fa = 2 * gate_delay_ps

        # 총 지연: t_ha + (bits-1) * t_fa
        total_delay = t_ha + (self.bits - 1) * t_fa

        return {
            'half_adder_delay_ps': t_ha,
            'full_adder_delay_ps': t_fa,
            'total_delay_ps': total_delay,
            'total_delay_ns': total_delay / 1000,
            'critical_path_gates': 1 + 2 * (self.bits - 1)
        }


def analyze_adder_performance():
    """다양한 비트 수의 가산기 성능 비교"""
    print("\n" + "="*70)
    print("리플 캐리 가산기 성능 분석")
    print("="*70)

    gate_delay = 120  # ps

    for bits in [4, 8, 16, 32, 64]:
        rca = RippleCarryAdder(bits)
        timing = rca.analyze_delay(gate_delay)

        print(f"\n{rca.name}:")
        print(f"  하프 가산기 지연: {timing['half_adder_delay_ps']} ps")
        print(f"  풀 가산기 지연: {timing['full_adder_delay_ps']} ps")
        print(f"  총 지연: {timing['total_delay_ps']} ps ({timing['total_delay_ns']:.3f} ns)")
        print(f"  Critical Path: {timing['critical_path_gates']} 게이트")


def demonstration():
    """하프 가산기 데모"""
    # 하프 가산기 데모
    ha = HalfAdder()
    ha.print_truth_table()

    print("\n[하프 가산기 동작 예시]")
    for a, b in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        s, c = ha.add(a, b)
        print(f"  {a} + {b} = Sum={s}, Carry={c} → 결과: {c}{s}₂")

    # 4비트 리플 캐리 가산기 데모
    print("\n" + "="*50)
    print("4비트 리플 캐리 가산기 (Ripple Carry Adder)")
    print("="*50)

    rca4 = RippleCarryAdder(4)

    test_cases = [
        (5, 3),    # 0101 + 0011 = 1000 (8)
        (7, 9),    # 0111 + 1001 = 0000 (16, overflow)
        (10, 6),   # 1010 + 0110 = 0000 (16, overflow)
        (15, 1),   # 1111 + 0001 = 0000 (16, overflow)
    ]

    for a, b in test_cases:
        result, overflow = rca4.add(a, b)
        print(f"\n  {a:2d} ({a:04b}) + {b:2d} ({b:04b}) = ", end="")
        print(f"{result:2d} ({result:04b})", end="")
        if overflow:
            print(f" [오버플로우: {overflow}]")
        else:
            print()

    # 성능 분석
    analyze_adder_performance()


if __name__ == "__main__":
    demonstration()
```
