+++
title = "JK 플립플롭 (JK Flip-Flop)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# JK 플립플롭 (JK Flip-Flop)

## 핵심 인사이트 (3줄 요약)
1. JK 플립플롭은 SR 플립플롭의 금지 상태(S=R=1)를 해결하고 J=K=1일 때 토글(Toggle) 동작을 추가하여 카운터, 상태 기계 등 다양한 순차 회로를 구현할 수 있다
2. J=1이면 Set, K=1이면 Reset, J=K=1이면 Q을 반전(토글)하며, 클럭 에지에서만 상태가 변하는 에지 트리거 회로이다
3. 기술사시험에서는 JK 플립플롭의 진리표, T 플립플롭과의 관계, 카운터 구현, 응용 회로 설계가 핵심이다

## Ⅰ. 개요 (500자 이상)

JK 플립플롭(Jack Kilby Flip-Flop)는 **SR 플립플롭의 금지 상태(S=R=1) 문제를 해결하고 토글(Toggle) 기능을 추가**하여 다양한 순차 회로를 구현할 수 있는 저장 장치이다. J와 K 두 입력을 가지며, SR 플립플롭과 달리 J=K=1일 때 출력을 반전시키는 토글 동작을 수행한다.

```
JK 플립플롭 기본 개념:
입력: J (Jump/Set), K (Kill/Reset), Clk (Clock)
출력: Q, Q'

동작:
- J=1, K=0: Set (Q=1)
- J=0, K=1: Reset (Q=0)
- J=0, K=0: 상태 유지
- J=1, K=1: 토글 (Q ← Q')

토글 기능:
J=K=1일 때 클럭 에지마다 Q가 반전
0 → 1 → 0 → 1 → ...
```

**JK 플립플롭의 핵심 특징:**

1. **금지 상태 없음**: J=K=1이 토글로 정의됨
2. **다기능**: Set, Reset, Hold, Toggle 가능
3. **카운터 구현**: J=K=1로 2분 주파 카운터
4. **상태 기계**: 다양한 상태 전이 가능

```
SR vs JK 플립플롭:
SR: S=R=1 → 금지 상태 (정의되지 않음)
JK: J=K=1 → 토글 (정의됨)

JK 플립플롭 = SR 플립플롭 + 토글 회로
```

JK 플립플롭은 카운터, 시프트 레지스, 주파수 분배기 등 다양한 순차 회로에 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### JK 플립플롭 회로 구조

```
JK 플립플롭 구조:

J ───┐
     │
K ───┼── JK Logic ── SR FF ── Q, Q'
     │              (에지 트리거)
Clk ──┘

JK Logic:
S = J · Q'
R = K · Q

J=1, K=1일 때:
S = 1 · Q' = Q'
R = 1 · Q = Q

Q=0이면: S=1, R=0 → Q←1 (토글)
Q=1이면: S=0, R=1 → Q←0 (토글)
```

### 진리표

```
Positive Edge JK 플립플롭:
| Clk | J | K | Q(t) | Q(t+1) | 동작 |
|-----|---|---|------|--------|------|
| ↑   | 0 | 0 |   X  |   X    | 유지 (Hold) |
| ↑   | 0 | 1 |   X  |   0    | Reset |
| ↑   | 1 | 0 |   X  |   1    | Set |
| ↑   | 1 | 1 |   0  |   1    | Toggle (0→1) |
| ↑   | 1 | 1 |   1  |   0    | Toggle (1→0) |
| X   | X | X |   X  |   X    | 유지 |

↑: 상승 에지
X: 무관
```

### 토글 동작

```
JK 플립플롭 토글 (J=K=1):

Clk: ────┬───┬───┬───┬───┬───
      ↑   ↑   ↑   ↑   ↑
      1   2   3   4   5

Q: ────┐   ┌───┐   ┌───┐
   0   1   0   1   0

설명:
1: Q=0 → Q=1 (토글)
2: Q=1 → Q=0 (토글)
3: Q=0 → Q=1 (토글)
4: Q=1 → Q=0 (토글)
5: Q=0 → Q=1 (토글)

특징:
- 주파수 1/2
- 50% 듀티 사각파
```

### 상태도

```
JK 플립플롭 상태도:

     JK=01 ─────→ JK=XX (유지)
      │             ↑
      ↓             │
   JK=11 (토글) ←────┘
      │
      ↓
   JK=10
      │
      ↓
      └────→ (Loop)

상태 전이:
Q=0: J=1 → Q=1 (Set)
Q=1: K=1 → Q=0 (Reset)
Q=0: J=K=1 → Q=1 (Toggle)
Q=1: J=K=1 → Q=0 (Toggle)
```

### 전파 지연

```
JK 플립플롭 지연:

1. JK Logic:
   - AND 게이트: t_AND
   - S = J·Q', R = K·Q

2. SR 플립플롭:
   - 에지 검출 + 래치: 3-4 게이트

3. 총 지연:
   t_total = t_AND + 4 게이트
           = 5 게이트

@ 100ps/게이트:
t_pd = 500ps
f_max = 2 GHz (이론)
실제: 1-1.5 GHz (마진 포함)
```

### 마스터-슬레이브 JK 플립플롭

```
Master-Slave JK FF 구조:

Clk ──┬── Master JK Latch (Clk=1)
      │    │
J, K ──┴──── Qm, Qm'
           │
Clk' ───┬── Slave JK Latch (Clk'=1)
        │    │
Qm, Qm' ─┴── Q, Q'

동작:
Clk=1: Master 활성, Slave 래치
Clk=0: Master 래치, Slave 활성

이점:
- 투명성 제거
- 에지 트리거 안정화
- Race Condition 방지
```

## Ⅲ. 융합 비교

### 플립플롭 종류 비교

| 비교 항목 | SR FF | JK FF | D FF | T FF |
|----------|-------|-------|------|------|
| 입력 | S, R, Clk | J, K, Clk | D, Clk | T, Clk |
| Set | S=1 | J=1 | D=1 | - |
| Reset | R=1 | K=1 | D=0 | - |
| Hold | S=R=0 | J=K=0 | - | T=0 |
| Toggle | 금지 | J=K=1 | - | T=1 |
| 금지 상태 | S=R=1 | 없음 | 없음 | 없음 |
| 응용 | 기본 | 카운터 | 레지스터 | 카운터 |

### JK vs T 플립플롭

| 비교 항목 | JK FF | T FF |
|----------|-------|------|
| 입력 | J, K | T |
| Toggle | J=K=1 | T=1 |
| Reset | K=1 | J=K=0으로 대체 |
| 유연성 | 높음 | 낮음 |
| 복잡도 | 높음 | 낮음 |
| 응용 | 범용 | 카운터 전용 |

### 카운터 구현

| 방식 | 회로 | 클럭 수 | 복잡도 |
|------|------|---------|--------|
| JK FF (J=K=1) | JK FF × n | 2ⁿ | 낮음 |
| T FF | T FF × n | 2ⁿ | 낮음 |
| D FF + XOR | D FF + LOGIC | 2ⁿ | 중간 |
| 동기식 카운터 | LOGIC + FF | n | 높음 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 3비트 카운터

```
JK 플립플롭 3비트 카운터 (J=K=1):

Q0: JK FF 0 ──┐
Q1: JK FF 1 ←─┤ (Clk 분주)
Q2: JK FF 2 ←─┤

Clk ─────────┴── Clk0
               │
               ├── Clk1 (Q0 상승/하강)
               └── Clk2 (Q1 상승/하강)

동작:
- FF0: 매 클럭 토글 (÷2)
- FF1: Q0 상승/하강 시 토글 (÷4)
- FF2: Q1 상승/하강 시 토글 (÷8)

출력: Q2 Q1 Q0
000 → 001 → 010 → 011 → 100 → 101 → 110 → 111 → 000

지연:
- 최악: 리플 캐리
- 3 스테이지: 3 × t_pd
```

### 동기식 카운터

```
동기식 JK 카운터 (Parallel Carry):

Clk ───┬── JK FF 0 ── Q0
       │    │
       ├── JK FF 1 ── Q1
       │    │
       └── JK FF 2 ── Q2

Carry Logic:
J1 = K1 = Q0
J2 = K2 = Q0·Q1

특징:
- 모든 FF 동시 클럭
- 병렬 캐리
- 빠른 동작

지연:
- t_setup + t_pd (한 클럭)
- n비트: 1 클럭 (리플 아님)
```

### 주파수 분배기

```
JK FF 주파수 분배기:

Fin ── JK FF (J=K=1) ── Q0 ──÷2
                         │
                         └─ JK FF (J=K=1) ── Q1 ──÷4
                                                │
                                                └─ JK FF (J=K=1) ── Q2 ──÷8

주파수:
Fin:     f
Q0:      f/2 (50% 듀티)
Q1:      f/4 (25% 듀티)
Q2:      f/8 (12.5% 듀티)

응용:
- 클럭 생성
- 타이밍 생성
- 비동기 카운터
```

## Ⅴ. 기대효과 및 결론

JK 플립플롭은 다목적 순차 회로이다. 카운터, 상태 기계에 필수적이다.

## 📌 관련 개념 맵

```
JK 플립플롭
├── 구조
│   ├── J 입력 (Set)
│   ├── K 입력 (Reset)
│   ├── Clk 입력 (Clock)
│   └── Q, Q' 출력
├── 동작
│   ├── J=1, K=0: Set (Q=1)
│   ├── J=0, K=1: Reset (Q=0)
│   ├── J=0, K=0: 유지
│   └── J=1, K=1: 토글 (Q←Q')
├── 특징
│   ├── 금지 상태 없음
│   ├── 토글 기능
│   └── 다기능
└── 응용
    ├── 카운터
    ├── 상태 기계
    └── 주파수 분배기
```

## 👶 어린이를 위한 3줄 비유 설명

1. JK 플립플롭은 전구 스위치와 비슷해요. J=K=1이면 클럭 때마다 전구가 켜졌다 꺼졌다 해요(토글)
2. J=1이면 전구 켜고(Set), K=1이면 전구 끄고(Reset), J=K=0이면 상태 유지해요. J=K=1일 때만 스위치를 반복해서 누르는 것과 같아요
3. 컴퓨터 카운터는 JK 플립플롭 여러 개를 연결해서 만들 수 있어요. 클럭마다 숫자가 1씩 증가하는 카운터를 구현할 수 있어요

```python
# JK 플립플롭 시뮬레이션

from typing import List, Tuple


class JKFlipFlop:
    """JK 플립플롭 시뮬레이션"""

    def __init__(self, edge_type: str = "rising"):
        """
        JK 플립플롭 초기화

        Args:
            edge_type: "rising" 또는 "falling"
        """
        self.q = 0
        self.q_prime = 1
        self.edge_type = edge_type
        self.prev_clk = 0

    def clock(self, j: int, k: int, clk: int) -> Tuple[int, int]:
        """
        클럭에 따른 상태 변화

        Args:
            j: J 입력 (0 또는 1)
            k: K 입력 (0 또는 1)
            clk: 클럭 신호

        Returns:
            (q, q_prime): 현재 상태
        """
        if j not in [0, 1] or k not in [0, 1] or clk not in [0, 1]:
            raise ValueError("J, K, Clk는 0 또는 1이어야 합니다")

        # 에지 검출
        edge = False
        if self.edge_type == "rising":
            edge = (self.prev_clk == 0 and clk == 1)
        else:  # falling
            edge = (self.prev_clk == 1 and clk == 0)

        self.prev_clk = clk

        # 에지에서만 상태 변경
        if edge:
            if j == 0 and k == 0:
                pass  # 유지
            elif j == 0 and k == 1:
                self.q = 0  # Reset
                self.q_prime = 1
            elif j == 1 and k == 0:
                self.q = 1  # Set
                self.q_prime = 0
            elif j == 1 and k == 1:
                # 토글
                self.q = 1 - self.q
                self.q_prime = 1 - self.q_prime

        return self.q, self.q_prime

    def get_state(self) -> Tuple[int, int]:
        """현재 상태 반환"""
        return self.q, self.q_prime


class JKCounter:
    """JK 플립플롭 카운터"""

    def __init__(self, bits: int):
        """
        n비트 카운터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.ffs = [JKFlipFlop() for _ in range(bits)]

    def clock(self, j: List[int], k: List[int], clk: int) -> int:
        """
        클럭에 따른 카운트

        Args:
            j: J 입력 리스트 (길이 = bits)
            k: K 입력 리스트 (길이 = bits)
            clk: 클럭 신호

        Returns:
            현재 카운트 값
        """
        if len(j) != self.bits or len(k) != self.bits:
            raise ValueError(f"J, K는 {self.bits}개여야 합니다")

        # 리플 카운터: 각 FF의 J=K=1
        for i in range(self.bits):
            self.ffs[i].clock(1, 1, clk)
            # 다음 FF의 클럭은 이전 FF의 출력
            if i < self.bits - 1:
                clk = self.ffs[i].get_state()[0]

        return self.get_count()

    def get_count(self) -> int:
        """현재 카운트 값"""
        value = 0
        for i in range(self.bits):
            value |= self.ffs[i].get_state()[0] << i
        return value


class TFlipFlop:
    """T 플립플롭 (JK의 변형)"""

    def __init__(self, edge_type: str = "rising"):
        """
        T 플립플롭 초기화

        Args:
            edge_type: "rising" 또는 "falling"
        """
        self.jk_ff = JKFlipFlop(edge_type)

    def clock(self, t: int, clk: int) -> Tuple[int, int]:
        """
        클럭에 따른 상태 변화

        Args:
            t: T 입력 (0=유지, 1=토글)
            clk: 클럭 신호

        Returns:
            (q, q_prime): 현재 상태
        """
        # T FF는 JK FF의 특수 경우
        # T=0: J=0, K=0 (유지)
        # T=1: J=1, K=1 (토글)
        j = t
        k = t
        return self.jk_ff.clock(j, k, clk)


class FrequencyDivider:
    """주파수 분배기"""

    def __init__(self, stages: int):
        """
        n단계 주파수 분배기

        Args:
            stages: 분배 단계 수
        """
        self.ffs = [TFlipFlop() for _ in range(stages)]

    def clock(self, clk: int) -> List[int]:
        """
        클럭에 따른 분배

        Args:
            clk: 입력 클럭

        Returns:
            각 단계의 출력
        """
        outputs = []

        for i in range(len(self.ffs)):
            # T=1로 설정 (항상 토글)
            self.ffs[i].clock(1, clk)
            outputs.append(self.ffs[i].get_state()[0])
            # 다음 FF의 클럭은 이전 FF의 출력
            clk = outputs[-1]

        return outputs


def demonstration():
    """JK 플립플롭 데모"""
    print("="*60)
    print("JK 플립플롭 (JK Flip-Flop) 데모")
    print("="*60)

    # JK 플립플롭
    print("\n[JK 플립플롭 진리표]")
    jk_ff = JKFlipFlop()

    test_cases = [
        (0, 0, 1, "J=0, K=0: 유지"),
        (0, 1, 1, "J=0, K=1: Reset"),
        (1, 0, 1, "J=1, K=0: Set"),
        (1, 1, 1, "J=1, K=1: 토글 (0→1)"),
        (0, 0, 0, "Clk=0: 무시"),
        (1, 1, 1, "J=1, K=1: 토글 (1→0)"),
    ]

    print(f"{'J':<3} {'K':<3} {'Clk':<4} {'Q(t+1)':<8} {'설명':<20}")
    print("-" * 45)

    for j, k, clk, desc in test_cases:
        q, _ = jk_ff.clock(j, k, clk)
        print(f"{j:<3} {k:<3} {clk:<4} {q:<8} {desc:<20}")

    # 카운터
    print(f"\n[3비트 JK 카운터]")
    counter = JKCounter(bits=3)

    print(f"0부터 7까지 카운트:")
    for i in range(10):
        count = counter.clock([], [], 1)  # J=K=1 (리플)
        print(f"  {i}: 0b{count:03b} ({count})")

    # 주파수 분배기
    print(f"\n[4단계 주파수 분배기]")
    freq_div = FrequencyDivider(stages=4)

    print("입력 클럭 10 사이클:")
    for i in range(10):
        outputs = freq_div.clock(1)  # 상승 에지
        if i < 10:
            q0, q1, q2, q3 = outputs
            print(f"  {i}: Q3={q3} Q2={q2} Q1={q1} Q0={q0}")

    # T 플립플롭
    print(f"\n[T 플립플롭 (JK 변형)]")
    t_ff = TFlipFlop()

    print("T=1로 8 클럭:")
    for i in range(8):
        q, _ = t_ff.clock(1, 1)
        print(f"  {i}: Q={q}")


if __name__ == "__main__":
    demonstration()
```
