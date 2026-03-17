+++
title = "풀 가산기 (Full Adder)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 풀 가산기 (Full Adder)

## 핵심 인사이트 (3줄 요약)
1. 풀 가산기는 3개 입력(A, B, Carry_in)에 대해 합(Sum)과 자리올림(Carry_out)을 출력하는 조합 회로로, 다비트 가산의 기본 요소이다
2. 하프 가산기 2개 또는 2개 XOR + 2개 AND + 1개 OR 게이트로 구현하며, Sum = A⊕B⊕Cin, Cout = AB + Cin(A⊕B)로 계산한다
3. 기술사시험에서는 풀 가산기 회로 최적화, 리플 캐리 vs 캐리 룩어헤드, 전파 지연 분석이 핵심이다

## Ⅰ. 개요 (500자 이상)

풀 가산기(Full Adder)는 **3개의 1비트 입력**을 받아 합(Sum)과 자리올림(Carry out)을 출력하는 조합 논리 회로이다. 하프 가산기와 달리 이전 단계의 캐리(Carry in)를 입력으로 받아 처리할 수 있으므로, 다비트 이진수 더하기에 사용할 수 있다.

```
풀 가산기 블록도:
    A ───┐
    B ────┤─── FA ──┬── Sum
Cin ─────┘          │
                    └── Cout
```

**입력:**
- A: 피가산수의 현재 비트
- B: 가산수의 현재 비트
- Cin: 이전 단계의 자리올림

**출력:**
- Sum: A + B + Cin의 합 (1비트)
- Cout: 발생한 자리올림 (0 또는 1)

```
풀 가산기 진리표:
| A | B | Cin | Sum | Cout | 설명 |
|---|---|-----|-----|------|------|
| 0 | 0 |  0  |  0  |  0   | 0+0+0=000 |
| 0 | 0 |  1  |  1  |  0   | 0+0+1=001 |
| 0 | 1 |  0  |  1  |  0   | 0+1+0=001 |
| 0 | 1 |  1  |  0  |  1   | 0+1+1=010 |
| 1 | 0 |  0  |  1  |  0   | 1+0+0=001 |
| 1 | 0 |  1  |  0  |  1   | 1+0+1=010 |
| 1 | 1 |  0  |  0  |  1   | 1+1+0=010 |
| 1 | 1 |  1  |  1  |  1   | 1+1+1=011 |
```

풀 가산기는 **하프 가산기 2개를 직렬 연결**하여 구현할 수 있다. 첫 번째 하프 가산기는 A와 B를 더하고, 두 번째 하프 가산기는 그 결과와 Cin을 더한다. 캐리 출력은 두 하프 가산기의 캐리를 OR로 결합한다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 하프 가산기 2개로 구현

```
풀 가산기 (하프 가산기 2개):
A ──┬──── HA1 ──┬──── HA2 ── Sum
B ──┤           │
    │           │
Cin ┴───────────┴────┴───── Carry1 OR Carry2 = Cout

동작:
1. HA1: A + B → Sum1, Carry1
2. HA2: Sum1 + Cin → Sum, Carry2
3. Cout = Carry1 OR Carry2
```

### 직접 구현 (최적화)

```
풀 가산기 논리 회로 (최적화):
A ──┬─────────┬─── XOR ──── Sum
B ──┤ XOR     │   │
    │         │   │
Cin ┴─────────┴───┘

A ──┬─────────┬─── AND ──┐
B ──┤         │          │
    │ AND     │          OR ─── Cout
    │         │          │
Cin ┴─────────┴─── AND ──┘

불 대수식:
Sum = A ⊕ B ⊕ Cin
    = A·B'·Cin' + A'·B·Cin' + A'·B'·Cin + A·B·Cin

Cout = A·B + Cin·(A ⊕ B)
     = A·B + A·Cin + B·Cin
```

### 전파 지연 분석

```
풀 가산기 타이밍 (하프 가산기 2개 구현):

경로 1: A,B → Sum
HA1 (XOR) → HA2 (XOR)
t_delay = 2 × t_XOR = 2 ~ 3 게이트 지연

경로 2: A,B → Cout
HA1 (AND) → OR
t_delay = t_AND + t_OR = 2 게이트 지연

경로 3: Cin → Sum
HA2 (XOR)
t_delay = t_XOR = 1 ~ 2 게이트 지연

Critical Path: Sum 출력 (2× XOR)
@ t_XOR = 120ps:
t_critical = 240ps
```

### 회로 복잡도

```
트랜지스터 수 (CMOS 구현):

방법 1: 하프 가산기 2개
- HA × 2 = 24 ~ 32 트랜지스터

방법 2: 최적화 직접 구현
- XOR 2개 = 12 ~ 20 트랜지스터
- AND 2개 = 12 트랜지스터
- OR 1개 = 6 트랜지스터
- 총 30 ~ 38 트랜지스터

면적, 전력, 속도 트레이드오프:
- 더 적은 게이트 = 더 적은 지연
- 더 적은 트랜지스터 = 더 적은 면적
- 공유 서브텀 = 최적화
```

## Ⅲ. 융합 비교

### 하프 가산기 vs 풀 가산기

| 비교 항목 | 하프 가산기 | 풀 가산기 |
|----------|-----------|----------|
| 입력 | A, B (2개) | A, B, Cin (3개) |
| 출력 | Sum, Carry (2개) | Sum, Cout (2개) |
| XOR 게이트 | 1개 | 2개 (또는 3개) |
| AND 게이트 | 1개 | 2개 |
| OR 게이트 | 0개 | 1개 |
| 캐리 처리 | 불가 | 가능 |
| 응용 | LSB 가산 | 일반 가산 |

### 다비트 가산기 구성

| 가산기 유형 | HA 수 | FA 수 | 총 지연 (×t_FA) |
|-----------|-------|-------|----------------|
| 4비트 RCA | 1 | 3 | 1 + 2×3 = 7 |
| 8비트 RCA | 1 | 7 | 1 + 2×7 = 15 |
| 16비트 RCA | 1 | 15 | 1 + 2×15 = 31 |
| 32비트 RCA | 1 | 31 | 1 + 2×31 = 63 |

RCA = Ripple Carry Adder

## Ⅳ. 실무 적용 및 기술사적 판단

### 4비트 리플 캐리 가산기

```
4비트 RCA 구조:
A3 B3 ───────┐
A2 B2 ────┐  │
A1 B1 ──┐  │  │
A0 B0 ─┴─┴──┴──┴─ FA ─ FA ─ FA ─ FA
      │  │  │  │   │   │   │   │
      └──┴──┴──┴───┴───┴───┴───┴──→ Carry Chain

LSB: HA (또는 Cin=0인 FA)
Bit 1-3: FA 3개 캐리 체인

지연:
t_total = t_HA + 3 × t_FA
        = t_XOR + 3 × (2 × t_XOR)
        = 7 × t_XOR

@ t_XOR = 120ps: t_total = 840ps
```

### 캐리 룩어헤드 가산기 (Carry Look-Ahead Adder)

```
CLAA 원리:
캐리를 병렬로 계산하여 리플 지연 제거

Generate (G): G[i] = A[i] · B[i]
Propagate (P): P[i] = A[i] ⊕ B[i]

Carry[i] = G[i] + P[i] · Carry[i-1]

C0 = Cin (입력)
C1 = G0 + P0·C0
C2 = G1 + P1·G0 + P1·P0·C0
C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0

4비트 CLAA 지연:
t_total = t_PG + t_CARRY + t_SUM
        = 1 + 2 + 1 = 4 게이트 지연
(RCA의 7게이트 대비 40% 감소)
```

### 풀 가산기 응용

```
1. ALU 산술 연산:
   - 덧셈, 뺄셈 기반

2. 주소 계산:
   - PC + Offset
   - Base + Index

3. 곱셈기:
   - 부분 곱 생성

4. MAC (Multiply-Accumulate):
   - DSP 필터

5. CRC/Checksum:
   - 데이터 무결성 검증
```

## Ⅴ. 기대효과 및 결론

풀 가산기는 다비트 가산의 기본이다. RCA, CLAA, CSA 등 다양한 가산기 아키텍처의 기초이다.

## 📌 관련 개념 맵

```
풀 가산기
├── 정의: 3입력 2출력 더하기
├── 구현
│   ├── 하프 가산기 2개
│   └── XOR 2 + AND 2 + OR 1
├── 파라미터
│   ├── Sum = A⊕B⊕Cin
│   └── Cout = AB + Cin(A⊕B)
└── 응용
    ├── 리플 캐리 가산기
    ├── 캐리 룩어헤드
    └── ALU 산술 회로
```

## 👶 어린이를 위한 3줄 비유 설명

1. 풀 가산기는 세 개의 숫자를 더하는 계산기예요. 두 개의 숫자와 이전 자리에서 올라온 자리올림까지 합쳐서 계산해요
2. 1+1+1=3을 이진수로는 11로 표현하는데, 합은 1이고 자리올림도 1이에요. 풀 가산기는 이 두 가지를 동시에 계산해요
3. 여러 자리 숫자를 더할 때 각 자리마다 풀 가산기를 두고, 자리올림을 다음 자리로 전달하면서 연쇄적으로 계산해요

```python
# 풀 가산기 시뮬레이션 및 고급 분석 도구

class FullAdder:
    """
    풀 가산기 (Full Adder) 시뮬레이션
    3입력 1비트 더하기 수행
    """

    def __init__(self):
        """풀 가산기 초기화"""
        self.name = "Full Adder"

    def add(self, a: int, b: int, carry_in: int) -> tuple[int, int]:
        """
        1비트 더하기 (캐리 포함)

        Args:
            a: 입력 A (0 또는 1)
            b: 입력 B (0 또는 1)
            carry_in: 캐리 입력 (0 또는 1)

        Returns:
            (sum, carry_out): 합과 자리올림 출력
        """
        if a not in [0, 1] or b not in [0, 1] or carry_in not in [0, 1]:
            raise ValueError("모든 입력은 0 또는 1이어야 합니다")

        # Sum = A ⊕ B ⊕ Cin
        sum_bit = a ^ b ^ carry_in

        # Carry = (A·B) + (Cin·(A ⊕ B))
        carry_out = (a & b) | (carry_in & (a ^ b))

        return sum_bit, carry_out

    def truth_table(self) -> list[dict]:
        """진리표 생성"""
        table = []
        for a in [0, 1]:
            for b in [0, 1]:
                for cin in [0, 1]:
                    sum_bit, cout = self.add(a, b, cin)
                    table.append({
                        'A': a,
                        'B': b,
                        'Cin': cin,
                        'Sum': sum_bit,
                        'Cout': cout,
                        'Decimal': a + b + cin,
                        'Result': f"{cout}{sum_bit}₂"
                    })
        return table

    def print_truth_table(self):
        """진리표 출력"""
        print("\n" + "="*60)
        print("풀 가산기 (Full Adder) 진리표")
        print("="*60)
        print(f"{'A':>3} {'B':>3} {'Cin':>4} {'Sum':>4} {'Cout':>5} {'Dec':>4} {'Result':>8}")
        print("-" * 60)

        for row in self.truth_table():
            print(f"{row['A']:>3} {row['B']:>3} {row['Cin']:>4} {row['Sum']:>4} "
                  f"{row['Cout']:>5} {row['Decimal']:>4} {row['Result']:>8}")

        print("="*60)


class NBitAdder:
    """
    n비트 가산기 시뮬레이터
    풀 가산기를 직렬 연결한 리플 캐리 가산기
    """

    def __init__(self, bits: int, carry_lookahead: bool = False):
        """
        n비트 가산기 생성

        Args:
            bits: 비트 수
            carry_lookahead: 캐리 룩어헤드 사용 여부
        """
        self.bits = bits
        self.carry_lookahead = carry_lookahead
        self.fa = FullAdder()

    def add(self, a: int, b: int, carry_in: int = 0) -> tuple[int, int]:
        """
        n비트 더하기 수행

        Args:
            a: 피가산수
            b: 가산수
            carry_in: 입력 캐리

        Returns:
            (result, overflow): 합과 오버플로우 플래그
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다")

        result = 0
        carry = carry_in

        if self.carry_lookahead:
            # 캐리 룩어헤드 방식 (병렬 캐리 계산)
            result, carry = self._add_cla(a, b, carry_in)
        else:
            # 리플 캐리 방식
            for i in range(self.bits):
                a_bit = (a >> i) & 1
                b_bit = (b >> i) & 1
                sum_bit, carry = self.fa.add(a_bit, b_bit, carry)
                result |= (sum_bit << i)

        overflow = carry

        return result, overflow

    def _add_cla(self, a: int, b: int, carry_in: int) -> tuple[int, int]:
        """
        캐리 룩어헤드 더하기 (병렬 캐리 계산)
        """
        # Generate/Propagate 계산
        g = [0] * self.bits  # Generate
        p = [0] * self.bits  # Propagate

        for i in range(self.bits):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1
            g[i] = a_bit & b_bit
            p[i] = a_bit ^ b_bit

        # 캐리 병렬 계산
        c = [0] * (self.bits + 1)
        c[0] = carry_in

        for i in range(self.bits):
            # C[i+1] = G[i] + P[i]·C[i]
            c[i + 1] = g[i] | (p[i] & c[i])

        # 합 계산
        result = 0
        for i in range(self.bits):
            sum_bit = p[i] ^ c[i]
            result |= (sum_bit << i)

        return result, c[self.bits]

    def analyze_delay(self, gate_delay_ps: int = 120) -> dict:
        """
        전파 지연 분석

        Args:
            gate_delay_ps: 게이트 지연 (피코초)
        """
        if self.carry_lookahead:
            # CLAA: PG(1) + Carry(2) + Sum(1) = 4 게이트
            total_gates = 4
        else:
            # RCA: 2×(bits-1) + 1 = 2bits - 1 게이트
            total_gates = 2 * self.bits - 1

        total_delay = total_gates * gate_delay_ps

        return {
            'type': 'Carry Look-Ahead' if self.carry_lookahead else 'Ripple Carry',
            'total_delay_ps': total_delay,
            'total_delay_ns': total_delay / 1000,
            'critical_path_gates': total_gates,
            'max_frequency_mhz': (1 / (total_delay_ps * 1e-12)) / 1e6
        }


class CarryLookAheadUnit:
    """
    캐리 룩어헤드 유닛 분석
    """

    @staticmethod
    def compute_generate_propagate(a: int, b: int, bits: int) -> tuple[list[int], list[int]]:
        """Generate와 Propagate 신호 계산"""
        g = []
        p = []

        for i in range(bits):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1
            g.append(a_bit & b_bit)
            p.append(a_bit ^ b_bit)

        return g, p

    @staticmethod
    def compute_carries(g: list[int], p: list[int], c_in: int) -> list[int]:
        """캐리 병렬 계산"""
        n = len(g)
        c = [0] * (n + 1)
        c[0] = c_in

        for i in range(n):
            c[i + 1] = g[i] | (p[i] & c[i])

        return c


def compare_adder_architectures():
    """가산기 아키텍처 비교"""
    print("\n" + "="*80)
    print("가산기 아키텍처 비교 (Ripple Carry vs Carry Look-Ahead)")
    print("="*80)

    gate_delay = 120  # ps

    for bits in [4, 8, 16, 32, 64]:
        # RCA
        rca = NBitAdder(bits, carry_lookahead=False)
        rca_timing = rca.analyze_delay(gate_delay)

        # CLAA
        cla = NBitAdder(bits, carry_lookahead=True)
        cla_timing = cla.analyze_delay(gate_delay)

        speedup = rca_timing['total_delay_ps'] / cla_timing['total_delay_ps']

        print(f"\n{bits}-비트 가산기:")
        print(f"  RCA:  {rca_timing['total_delay_ps']:>4} ps ({rca_timing['total_delay_ns']:>6.3f} ns) "
              f"@ {rca_timing['max_frequency_mhz']:>7.1f} MHz")
        print(f"  CLAA: {cla_timing['total_delay_ps']:>4} ps ({cla_timing['total_delay_ns']:>6.3f} ns) "
              f"@ {cla_timing['max_frequency_mhz']:>7.1f} MHz")
        print(f"  속도 향상: {speedup:>5.1f}x")


def demonstration():
    """풀 가산기 데모"""
    # 풀 가산기 진리표
    fa = FullAdder()
    fa.print_truth_table()

    print("\n[풀 가산기 동작 예시]")
    print("A + B + Cin = Sum | Carry")
    for a, b, cin in [(0, 0, 1), (0, 1, 1), (1, 1, 0), (1, 1, 1)]:
        s, c = fa.add(a, b, cin)
        print(f"  {a} + {b} + {cin} = {s} | {c} → 결과: {c}{s}₂")

    # 8비트 가산기 비교
    print("\n" + "="*60)
    print("8비트 가산기 동작 비교")
    print("="*60)

    rca8 = NBitAdder(8, carry_lookahead=False)
    cla8 = NBitAdder(8, carry_lookahead=True)

    test_cases = [
        (100, 50, 0),
        (200, 100, 0),
        (255, 1, 0),  # Overflow
        (128, 128, 0),  # Overflow
    ]

    for a, b, cin in test_cases:
        result_rca, ovf_rca = rca8.add(a, b, cin)
        result_cla, ovf_cla = cla8.add(a, b, cin)

        print(f"\n{a:3d} + {b:3d} = {result_rca:3d}", end="")
        if ovf_rca:
            print(f" [오버플로우]")
        else:
            print()

        print(f"  RCA: {result_rca:3d} ({result_rca:08b})")
        print(f"  CLA: {result_cla:3d} ({result_cla:08b})")

    # 아키텍처 비교
    compare_adder_architectures()


if __name__ == "__main__":
    demonstration()
```
