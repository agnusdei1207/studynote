+++
title = "비교기 (Comparator)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 비교기 (Comparator)

## 핵심 인사이트 (3줄 요약)
1. 비교기는 두 이진수 A와 B를 비교하여 A>B, A=B, A<B를 판단하는 조합 회로로, 등가 비교기(Equality Comparator)와 크기 비교기(Magnitude Comparator)가 있다
2. 1비트 비교는 XNOR로 등가를, AND+OR로 크기 비교를 수행하며, n비트는 MSB부터 순차적으로 비교하여 결과를 도출한다
3. 기술사시험에서는 비교기의 회로 구현, 캐스케이딩, 우선순위 인코더와의 결합이 핵심이다

## Ⅰ. 개요 (500자 이상)

비교기(Comparator)는 **두 이진수 A와 B를 비교**하여 A가 B보다 큰지(>), 같은지(=), 작은지(<)를 판단하는 조합 논리 회로이다. 프로세서의 분기 명령어(Conditional Branch)에서 조건 판단, 메모리 주소 비교, 데이터 정렬(Sorting) 하드웨어 등 다양한 곳에 사용된다.

```
비교기 출력:
GT (Greater Than): A > B일 때 1
EQ (Equal): A = B일 때 1
LT (Less Than): A < B일 때 1

출력은 상호 배타적:
- GT, EQ, LT 중 정확히 하나가 1
```

**1비트 등가 비교기:**
```
A ──┐
    │
B ──┴── XNOR ── EQ

EQ = A ⊙ B = A·B + A'·B'
```

**1비트 크기 비교기:**
```
A > B: A=1, B=0일 때만
GT = A · B'

A < B: A=0, B=1일 때만
LT = A' · B

EQ = A ⊙ B
```

**n비트 등가 비교기:**
```
A[n-1:0] = B[n-1:0]?

EQ = (A[0]⊙B[0]) · (A[1]⊙B[1]) · ... · (A[n-1]⊙B[n-1])
   = Π (A[i] ⊙ B[i])

모든 비트가 같아야 EQ=1
```

**n비트 크기 비교기:**
```
MSB부터 비교:

A > B if:
  MSB 비트에서 A=1, B=0
  또는 MSB가 같고 다음 비트에서 A=1, B=0
  또는 ...

A = B if:
  모든 비트가 같음

A < B if:
  MSB 비트에서 A=0, B=1
  또는 MSB가 같고 다음 비트에서 A=0, B=1
  또는 ...
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 4비트 크기 비교기

```
4비트 비교기 (74LS85):

입력: A3A2A1A0, B3B2B1B0
출력: GT, EQ, LT
캐스케이딩: I_GT, I_EQ, I_LT

동작:
1. MSB(A3, B3)부터 비교
2. A3>B3이면 GT=1 (결정)
3. A3=B3이면 다음 비트로 이동
4. 모든 비트가 같으면 EQ=1
5. 그 외 경우 LT=1

불 대수식:
GT = A3·B3' +
     (A3⊙B3)·A2·B2' +
     (A3⊙B3)·(A2⊙B2)·A1·B1' +
     (A3⊙B3)·(A2⊙B2)·(A1⊙B1)·A0·B0'

EQ = (A3⊙B3)·(A2⊙B2)·(A1⊙B1)·(A0⊙B0)

LT = A3'·B3 +
     (A3⊙B3)·A2'·B2 +
     (A3⊙B3)·(A2⊙B2)·A1'·B1 +
     (A3⊙B3)·(A2⊙B2)·(A1⊙B1)·A0'·B0
```

### 캐스케이딩

```
8비트 비교기 (4비트 × 2):

상위 4비트: Comp1
하위 4비트: Comp0

Comp0 (A3A2A1A0 vs B3B2B1B0):
  A[3:0] > B[3:0] → I_GT = 1
  A[3:0] = B[3:0] → I_EQ = 1
  A[3:0] < B[3:0] → I_LT = 1

Comp1 (A7A6A5A4 vs B7B6B5B4):
  입력: A[7:4], B[7:4]
  캐스케이딩: I_GT, I_EQ, I_LT = Comp0 출력

출력: 최종 GT, EQ, LT
```

### 전파 지연 분석

```
비교기 지연:

1. 1비트 등가:
   - XNOR: 1~2 게이트

2. n비트 등가:
   - n개 XNOR 병렬
   - 1개 n입력 AND
   - t_total = 2 + log₂(n) 게이트

3. n비트 크기 비교:
   - MSB에서 결정: 2~3 게이트
   - LSB까지 전파: O(n) 게이트

예시 (4비트):
t_eq = 2 + 2 = 4 게이트
t_gt = 3 게이트 (최악: MSB 결정 안 됨)
```

### 부호 있는 비교

```
부호 있는 비교 (2의 보수):

양수 vs 음수:
  양수 > 음수 (항상)

음수 vs 음수:
  절댓값이 작은 쪽이 큼
  (예: -1 > -2)

구현:
1. 부호 비트 확인
2. 부호가 다르면 양수가 큼
3. 부호가 같으면 절댓값 비교

Sign_A = A[n-1]
Sign_B = B[n-1]

GT = Sign_A'·Sign_B · (|A| > |B|)  # 양수 > 음수
    + Sign_A·Sign_B · (|A| < |B|)  # 음수: 작은 절댓값이 큼
```

## Ⅲ. 융합 비교

### 등가 비교기 vs 크기 비교기

| 비교 항목 | 등가 비교기 | 크기 비교기 |
|----------|-----------|------------|
| 출력 | EQ (1비트) | GT, EQ, LT (3비트) |
| 복잡도 | 낮음 | 높음 |
| 지연 | O(log n) | O(n) 최악 |
| 응용 | Cache hit, 주소 일치 | 분기, 정렬 |

### 비교기 구현 방식

| 방식 | 원리 | 지연 | 면적 | 응용 |
|------|------|------|------|------|
| XNOR + AND | 등가만 | O(log n) | 작음 | Cache tag |
| 순차 비교 | MSB→LSB | O(n) | 중간 | 일반 |
| 병렬 트리 | Tree 구조 | O(log n) | 큼 | 고성능 |
| 가산기 이용 | A-B 후 검사 | O(log n) | 중간 | ALU |

### n비트 비교기 복잡도

| 비트 수 | 등가 게이트 | 크기 비교 게이트 | 등가 지연 | 크기 지연 |
|--------|-----------|-----------------|----------|----------|
| 4 | 4 XNOR + 1 AND(4) | ~30 | 4 | 3-8 |
| 8 | 8 XNOR + 1 AND(8) | ~60 | 5 | 3-12 |
| 16 | 16 XNOR + 1 AND(16) | ~120 | 6 | 3-20 |
| 32 | 32 XNOR + 1 AND(32) | ~240 | 7 | 3-36 |

## Ⅳ. 실무 적용 및 기술사적 판단

### CPU 분기 명령어

```
조건부 분기 (Conditional Branch):

BEQ: Branch if EQual
  if (Rs == Rt) PC = PC + offset

BNE: Branch if Not Equal
  if (Rs != Rt) PC = PC + offset

BLT: Branch if Less Than
  if (Rs < Rt) PC = PC + offset

BGT: Branch if Greater Than
  if (Rs > Rt) PC = PC + offset

구현:
1. ALU로 Rs - Rt 연산
2. 결과와 플래그 검사
3. 비교기로 조건 확인
4. MUX로 PC 선택
```

### Cache Tag 비교

```
Cache Hit/Miss 검출:

주소: Tag + Index + Offset

Tag 비교:
Cache_Tag == Addr_Tag?

Tag 비교기 (등가):
- n비트 XNOR + AND
- 빠른 비교 (O(log n))
- Way가 여러 개면 병렬 비교

예시 (4-way Set Associative):
4개 Tag 병렬 비교
Hit = Tag1 Match + Tag2 Match + Tag3 Match + Tag4 Match
```

### 우선순위 인코더와 결합

```
우선순위 결정:

여러 요청 중 최우선순위 선택:

[Req0] ──┐
[Req1] ──┤
[Req2] ──┼──→ Priority Encoder → Grant
[Req3] ──┤
...     ──┘

비교기 체인:
Req0 > Req1?
Req1 > Req2?
...

또는:
Binary Tree 비교기
- O(log n) 지연
- 고속 우선순위 결정
```

## Ⅴ. 기대효과 및 결론

비교기는 조건 판단의 핵심이다. 분기 명령, Cache, 정렬 하드웨어에 필수적이다.

## 📌 관련 개념 맵

```
비교기
├── 종류
│   ├── 등가 비교기 (Equality)
│   └── 크기 비교기 (Magnitude)
├── 1비트
│   ├── EQ = A ⊙ B
│   ├── GT = A·B'
│   └── LT = A'·B
├── n비트
│   ├── MSB 우선 비교
│   └── 캐스케이딩
└── 응용
    ├── 분기 명령어
    ├── Cache Tag
    └── 우선순위 인코더
```

## 👶 어린이를 위한 3줄 비유 설명

1. 비교기는 두 숫자를 비교해서 누가 더 큰지, 같은지, 작은지를 판단하는 판사 같아요. A와 B를 입력하면 "A가 크다", "같다", "A가 작다" 중 하나를 알려줘요
2. 자리수가 많은 숫자는 가장 큰 자리(앞자리)부터 비교해요. 예를 들어 1000과 0111을 비교하면, 첫 번째 자리에서 1>0이니까 1000이 더 커요
3. 컴퓨터가 "if문"을 실행할 때 비교기가 조건을 확인해서 참이면 한 코드를, 거짓이면 다른 코드를 실행하게 해요

```python
# 비교기 시뮬레이션

from typing import Tuple


class BitComparator:
    """1비트 비교기"""

    def compare(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        1비트 비교

        Args:
            a: 입력 A
            b: 입력 B

        Returns:
            (gt, eq, lt): A>B, A=B, A<B
        """
        if a not in [0, 1] or b not in [0, 1]:
            raise ValueError("입력은 0 또는 1이어야 합니다")

        gt = a & ~b
        eq = ~(a ^ b) & 1
        lt = ~a & b

        return gt, eq, lt


class NBitComparator:
    """n비트 크기 비교기"""

    def __init__(self, bits: int):
        """
        n비트 비교기 생성

        Args:
            bits: 비트 수
        """
        self.bits = bits

    def compare(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        n비트 비교

        Args:
            a: 피비교수 A
            b: 피비교수 B

        Returns:
            (gt, eq, lt): A>B, A=B, A<B
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다")

        # MSB부터 비교
        for i in range(self.bits - 1, -1, -1):
            a_bit = (a >> i) & 1
            b_bit = (b >> i) & 1

            if a_bit > b_bit:
                return (1, 0, 0)  # A > B
            elif a_bit < b_bit:
                return (0, 0, 1)  # A < B

        return (0, 1, 0)  # A == B

    def compare_signed(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        부호 있는 n비트 비교 (2의 보수)

        Args:
            a: 피비교수 A
            b: 피비교수 B

        Returns:
            (gt, eq, lt): A>B, A=B, A<B
        """
        # 부호 확장 후 비교
        sign_bit = self.bits - 1

        # 음수 보정
        if a & (1 << sign_bit):
            a -= (1 << self.bits)
        if b & (1 << sign_bit):
            b -= (1 << self.bits)

        if a > b:
            return (1, 0, 0)
        elif a < b:
            return (0, 0, 1)
        else:
            return (0, 1, 0)


class EqualityComparator:
    """n비트 등가 비교기"""

    def __init__(self, bits: int):
        self.bits = bits

    def equals(self, a: int, b: int) -> int:
        """
        등가 비교

        Args:
            a: 입력 A
            b: 입력 B

        Returns:
            1 if A == B, else 0
        """
        if not (0 <= a < 2**self.bits) or not (0 <= b < 2**self.bits):
            raise ValueError(f"입력은 {self.bits}비트 범위 내여야 합니다")

        # XNOR → AND
        return 1 if a == b else 0


def demonstration():
    """비교기 데모"""
    print("=" * 70)
    print("비교기 (Comparator) 데모")
    print("=" * 70)

    # 1비트 비교기
    print("\n[1비트 비교기 진리표]")
    print(f"{'A':<2} {'B':<2} {'GT':<4} {'EQ':<4} {'LT':<4}")
    print("-" * 20)

    comp1 = BitComparator()
    for a in [0, 1]:
        for b in [0, 1]:
            gt, eq, lt = comp1.compare(a, b)
            result = "GT" if gt else ("EQ" if eq else "LT")
            print(f"{a:<2} {b:<2} {gt:<4} {eq:<4} {lt:<4} ({result})")

    # 8비트 비교기
    print("\n[8비트 비교기]")
    comp8 = NBitComparator(8)

    test_cases = [
        (100, 50),
        (50, 100),
        (127, 127),
        (255, 0),
        (0, 255),
    ]

    for a, b in test_cases:
        gt, eq, lt = comp8.compare(a, b)
        result = "A > B" if gt else ("A == B" if eq else "A < B")
        print(f"  {a:3} ({a:08b}) vs {b:3} ({b:08b}): {result}")

    # 부호 있는 비교
    print("\n[부호 있는 8비트 비교]")
    comp8_signed = NBitComparator(8)

    signed_tests = [
        (10, -10),
        (-10, 10),
        (-50, -100),
        (100, -50),
    ]

    for a, b in signed_tests:
        # 2의 보수 표현
        a_twos = a & 0xFF
        b_twos = b & 0xFF

        gt, eq, lt = comp8_signed.compare_signed(a_twos, b_twos)
        result = "A > B" if gt else ("A == B" if eq else "A < B")
        print(f"  {a:4} ({a_twos:08b}) vs {b:4} ({b_twos:08b}): {result}")

    # 등가 비교기
    print("\n[등가 비교기]")
    eq_comp = EqualityComparator(8)

    eq_tests = [(100, 100), (100, 50), (255, 255), (0, 1)]
    for a, b in eq_tests:
        eq = eq_comp.equals(a, b)
        print(f"  {a} == {b}: {eq}")

    # Cache Tag 비교 시뮬레이션
    print("\n[Cache Tag 비교]")
    cache_tags = [0x1A, 0x2B, 0x3C, 0x4D]  # 4-way
    addr_tag = 0x2B

    print(f"Address Tag: 0x{addr_tag:02X}")
    print(f"Cache Tags: {[f'0x{t:02X}' for t in cache_tags]}")

    eq_comp4 = EqualityComparator(8)
    hit = 0
    hit_way = -1

    for way, tag in enumerate(cache_tags):
        if eq_comp.equals(addr_tag, tag):
            hit = 1
            hit_way = way
            break

    if hit:
        print(f"Cache HIT! (Way {hit_way})")
    else:
        print("Cache MISS!")


if __name__ == "__main__":
    demonstration()
```
