+++
title = "T 플립플롭 (T Flip-Flop)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# T 플립플롭 (T Flip-Flop)

## 핵심 인사이트 (3줄 요약)
1. T 플립플롭은 T(Toggle) 입력이 1일 때마다 출력을 반전(0→1, 1→0)시키는 순차 회로로, JK 플립플롭의 J=K=1 상태를 단순화하여 카운터와 주파수 분배기에 특화되어 있다
2. T=0이면 상태 유지, T=1이면 토글 동작을 하며, 클럭 상승/하강 에지에서만 반응하는 에지 트리거 회로이다
3. 기술사시험에서는 T 플립플롭의 진리표, JK와의 관계, 2분 주파 카운터 구현, 응용 회로가 핵심이다

## Ⅰ. 개요 (500자 이상)

T 플립플롭(Toggle Flip-Flop)는 **단일 토글 입력 T에 의해 출력을 반전시키는 특화된 순차 회로**이다. JK 플립플롭의 J=K=1 상태만을 구현한 단순화된 형태로, 카운터와 주파수 분배기 등 주파수를 나누는 회로에 널리 사용된다.

```
T 플립플롭 기본 개념:
입력: T (Toggle), Clk (Clock)
출력: Q, Q'

동작:
- T=0: 상태 유지 (Hold)
- T=1: 토글 (Toggle, Q ← Q')

특징:
- 단일 입력: T만으로 제어
- 자동 반전: T=1 시 자동으로 Q 반전
- 2분 주파: 출력 주파수 = 입력 클럭 / 2
```

**T 플립플롭의 핵심 특징:**

1. **단순성**: JK 플립플롭보다 단순한 구조
2. **주파수 분배**: 입력 클럭의 1/2 주파수 출력
3. **카운터 구현**: 여러 개를 연결하여 n비트 카운터
4. **비동기 설계**: 간단한 리플 카운터 구현 가능

```
T 플립플롭 vs JK 플립플롭:
JK FF: J=K=1 → 토글
      J=0, K=0 → 유지
      J=1, K=0 → Set
      J=0, K=1 → Reset

T FF:  T=1 → 토글
      T=0 → 유지

T FF는 JK FF의 기능을 제한한 형태
```

T 플립플롭은 비동기 카운터, 주파수 분배기, 타이밍 생성기 등 다양한 응용이 있다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### T 플립플롭 회로 구조

```
T 플립플롭 구조 (JK 기반):

T ───┬── J ←─┐
     │        │
T ───┴── K ←─┴── JK FF (J=K=T)
     │
Clk ──┘

또는 D FF 기반:

T ───┐
     │
Clk ─┼── XOR ←────┐
     │    │        │
Q ───┴────┴── D FF ← Q'

Q ← (Q ⊕ T)
```

### 진리표

```
Positive Edge T 플립플롭:
| Clk | T | Q(t) | Q(t+1) | 동작 |
|-----|---|------|--------|------|
| ↑   | 0 |  X   |   X    | 유지 |
| ↑   | 1 |  0   |   1    | Toggle (0→1) |
| ↑   | 1 |  1   |   0    | Toggle (1→0) |
| X   | X |  X   |   X    | 유지 |

↑: 상승 에지
X: 무관
```

### 토글 동작

```
T 플립플롭 타이밍 (T=1):

Clk: ────┬───┬───┬───┬───┬───
      ↑   ↑   ↑   ↑   ↑
      1   2   3   4   5

Q: ────┐   ┌───┐   ┌───┐
   0   1   0   1   0

출력 파형:
- 50% 듀티 사각파
- 주파수 = Clk / 2
- 기간 = 2 × Clk 기간
```

### 상태도

```
T 플립플롭 상태도:

    T=1
     ↓
   Q=0 ←→→ Q=1
     ↑      ↓
     └──────┘

상태 전이:
Q=0, T=1 → Q=1 (Toggle)
Q=1, T=1 → Q=0 (Toggle)
Q=0, T=0 → Q=0 (유지)
Q=1, T=0 → Q=1 (유지)
```

### 전파 지연

```
T 플립플롭 지연:

JK 기반 구현:
1. J=K=T: 무지연
2. JK FF: 4-5 게이트

총 지연: 4-5 게이트

@ 100ps/게이트:
t_pd = 400-500ps
f_max = 2-2.5 GHz

D FF + XOR 구현:
1. XOR: 1 게이트 (D ← Q⊕T)
2. D FF: 3-4 게이트

총 지연: 4-5 게이트
```

### 다단계 T 플립플롭 카운터

```
n비트 리플 카운터:

T FF 0 ── Q0 ── T FF 1 ── Q1 ── T FF 2 ── Q2
     ↑        ↑           ↑
   Clk0     Clk1        Clk2

동작:
- FF0: 매 클럭 토글 (÷2)
- FF1: Q0 변화마다 토글 (÷4)
- FF2: Q1 변화마다 토글 (÷8)

리플 지연:
- 최악 케이스: Q0 → Q1 → Q2
- 3 × t_pd
- 비동기 전파
```

## Ⅲ. 융합 비교

### 플립플롭 토글 비교

| 비교 항목 | SR FF | JK FF | D FF | T FF |
|----------|-------|-------|------|------|
| Toggle | 금지 | J=K=1 | D=Q' | T=1 |
| 유지 | S=R=0 | J=K=0 | - | T=0 |
| 구현 복잡도 | 중간 | 높음 | 중간 | 낮음 |
| 응용 | 일반 | 범용 | 레지스터 | 카운터 |

### T 플립플롭 구현 방식

| 방식 | 구조 | 지연 | 면적 | 응용 |
|------|------|------|------|------|
| JK 기반 | JK FF (J=K) | 중간 | 큼 | 범용 |
| D FF 기반 | D FF + XOR | 중간 | 중간 | 간단 |
| 동기식 | 로직 + FF | 빠름 | 큼 | 고성능 |
| 비동기 | FF 체인 | 느림 | 작음 | 저전력 |

### 카운터 구현 비교

| 방식 | 구조 | 클럭 | 지연 | 복잡도 |
|------|------|------|------|--------|
| T FF 리플 | FF 체인 | 2ⁿ | O(n) | 단순 |
| T FF 동기 | Parallel | n | O(1) | 복잡 |
| D FF + LOGIC | D FF + XOR | n | O(1) | 중간 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 비동기 카운터

```
4비트 비동기 T FF 카운터:

FF0: T FF, Clk=Fin
FF1: T FF, Clk=Q0
FF2: T FF, Clk=Q1
FF3: T FF, Clk=Q2

출력: Q3 Q2 Q1 Q0
0000 → 0001 → 0010 → 0011 → ... → 1111 → 0000

동작:
- FF0: Fin 주파수의 1/2
- FF1: Q0 주파수의 1/2 = Fin의 1/4
- FF2: Q1 주파수의 1/2 = Fin의 1/8
- FF3: Q2 주파수의 1/2 = Fin의 1/16

지연:
- 최악 케이스: Q0 → Q1 → Q2 → Q3
- 4 × t_pd
- 2ns @ 500ps/게이트
```

### 주파수 분배기

```
4단계 주파수 분배기:

Fin ── T FF 0 ── Q0 (Fin/2)
              │
              └─ T FF 1 ── Q1 (Fin/4)
                         │
                         └─ T FF 2 ── Q2 (Fin/8)
                                    │
                                    └─ T FF 3 ── Q3 (Fin/16)

주파수 관계:
Fin:     f
Q0:      f/2
Q1:      f/4
Q2:      f/8
Q3:      f/16

듀티:
- 각 출력: 50%
- 위상차: 리플 지연으로 인한 스큐
```

### 2분 주파 카운터

```
T FF를 이용한 2분 주파:

T FF (T=1 상시)
  │
  └── Q

입력 클럭:
  ┌─┐ ┌─┐ ┌─┐ ┌─┐
  │ │ │ │ │ │ │ │ │
  └─┘ └─┘ └─┘ └─┘

출력 Q:
  ┌───┐   ┌───┐
  │   │   │   │
  └───┘   └───┘

주파수:
- 입력: f
- 출력: f/2
- 듀티: 50%
```

## Ⅴ. 기대효效果 및 결론

T 플립플롭은 카운터의 핵심이다. 주파수 분배, 비동기 카운터에 필수적이다.

## 📌 관련 개념 맵

```
T 플립플롭
├── 구조
│   ├── T 입력 (Toggle)
│   ├── Clk 입력 (Clock)
│   └── Q, Q' 출력
├── 동작
│   ├── T=0: 유지
│   └── T=1: 토글 (Q←Q')
├── 특징
│   ├── 2분 주파
│   ├── 50% 듀티
│   └── 단순 구조
├── 구현
│   ├── JK 기반 (J=K=T)
│   └── D FF + XOR
└── 응용
    ├── 카운터
    ├── 주파수 분배기
    └── 비동기 카운터
```

## 👶 어린이를 위한 3줄 비유 설명

1. T 플립플롭은 스위치 한 번으로 제어되는 전구 같아요. T=1일 때마다 클럭이 오면 전구가 켜졌다 꺼져요 (토글)
2. T=0이면 스위치를 만지지 않아서 상태가 유지되고, T=1이면 클럭마다 상태가 바뀌. 클럭 2번마다 전구가 한 번씩 켜져요(2분 주파)
3. 컴퓨터 카운터는 T 플립플롭 여러 개를 연결해서 만들 수 있어요. 첫 번째는 1의 자리를, 두 번째는 2의 자리를, 세 번째는 4의 자리를 카운트해요

```python
# T 플립플롭 시뮬레이션

from typing import List


class TFlipFlop:
    """T 플립플롭 시뮬레이션"""

    def __init__(self, edge_type: str = "rising"):
        """
        T 플립플롭 초기화

        Args:
            edge_type: "rising" 또는 "falling"
        """
        self.q = 0
        self.q_prime = 1
        self.edge_type = edge_type
        self.prev_clk = 0

    def clock(self, t: int, clk: int) -> tuple:
        """
        클럭에 따른 상태 변화

        Args:
            t: T 입력 (Toggle)
            clk: 클럭 신호

        Returns:
            (q, q_prime): 현재 상태
        """
        if t not in [0, 1] or clk not in [0, 1]:
            raise ValueError("T, Clk는 0 또는 1이어야 합니다")

        # 에지 검출
        edge = False
        if self.edge_type == "rising":
            edge = (self.prev_clk == 0 and clk == 1)
        else:  # falling
            edge = (self.prev_clk == 1 and clk == 0)

        self.prev_clk = clk

        # 에지에서만 상태 변경
        if edge and t == 1:
            # 토글
            self.q = 1 - self.q
            self.q_prime = 1 - self.q_prime

        return self.q, self.q_prime

    def get_state(self) -> tuple:
        """현재 상태 반환"""
        return self.q, self.q_prime


class RippleCounter:
    """리플 카운터 (T FF 기반)"""

    def __init__(self, bits: int):
        """
        n비트 리플 카운터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.ffs = [TFlipFlop() for _ in range(bits)]

    def clock(self, clk: int) -> int:
        """
        클럭에 따른 카운트

        Args:
            clk: 입력 클럭

        Returns:
            현재 카운트 값
        """
        # 첫 번째 FF: 입력 클럭 사용
        self.ffs[0].clock(1, clk)

        # 나머지 FF: 이전 FF의 Q를 클럭으로 사용
        for i in range(1, self.bits):
            prev_q = self.ffs[i-1].get_state()[0]
            # 상승 에지 검출
            if self.ffs[i].prev_clk == 0 and prev_q == 1:
                self.ffs[i].clock(1, prev_q)
            self.ffs[i].prev_clk = prev_q

        return self.get_count()

    def get_count(self) -> int:
        """현재 카운트 값"""
        value = 0
        for i in range(self.bits):
            value |= self.ffs[i].get_state()[0] << i
        return value


class FrequencyDivider:
    """주파수 분배기"""

    def __init__(self, stages: int):
        """
        n단계 주파수 분배기

        Args:
            stages: 분배 단계 수
        """
        self.stages = stages
        self.ffs = [TFlipFlop() for _ in range(stages)]

    def clock(self, clk_in: int) -> List[int]:
        """
        클럭 분배

        Args:
            clk_in: 입력 클럭

        Returns:
            각 단계의 출력
        """
        outputs = []
        clk = clk_in

        for i in range(self.stages):
            self.ffs[i].clock(1, clk)
            q = self.ffs[i].get_state()[0]
            outputs.append(q)
            clk = q  # 다음 FF의 클럭

        return outputs


def demonstration():
    """T 플립플롭 데모"""
    print("="*60)
    print("T 플립플롭 (T Flip-Flop) 데모")
    print("="*60)

    # T 플립플롭
    print("\n[T 플립플롭 진리표]")
    t_ff = TFlipFlop()

    test_cases = [
        (0, 1, "T=0, Clk=1: 유지"),
        (1, 0, "T=1, Clk=0: 무시"),
        (1, 1, "T=1, Clk=1: 0→1 (Toggle)"),
        (0, 1, "T=0, Clk=1: 유지"),
        (1, 1, "T=1, Clk=1: 1→0 (Toggle)"),
    ]

    print(f"{'T':<3} {'Clk':<4} {'Q(t+1)':<8} {'설명':<20}")
    print("-" * 40)

    for t, clk, desc in test_cases:
        q, _ = t_ff.clock(t, clk)
        print(f"{t:<3} {clk:<4} {q:<8} {desc:<20}")

    # 리플 카운터
    print(f"\n[4비트 리플 카운터]")
    counter = RippleCounter(bits=4)

    print("0부터 15까지 카운트:")
    for i in range(16):
        count = counter.clock(1)
        print(f"  {i:2d}: 0b{count:04b} ({count})")

    # 주파수 분배기
    print(f"\n[4단계 주파수 분배기]")
    freq_div = FrequencyDivider(stages=4)

    print("입력 클럭 16 사이클:")
    all_outputs = []
    for i in range(16):
        outputs = freq_div.clock(1)
        all_outputs.append(outputs)
        if i < 8:
            print(f"  {i}: Q3={outputs[3]} Q2={outputs[2]} Q1={outputs[1]} Q0={outputs[0]}")

    # 주파수 확인
    print(f"\n[주파수 확인]")
    for i in range(4):
        transitions = 0
        prev = all_outputs[-1][i]
        for j in range(len(all_outputs)-1, 0, -1):
            curr = all_outputs[j][i]
            if curr != prev:
                transitions += 1
            prev = curr
        print(f"  Q{i}: {transitions} 전이 (이론: {16 // (2**(i+1))})")


if __name__ == "__main__":
    demonstration()
```
