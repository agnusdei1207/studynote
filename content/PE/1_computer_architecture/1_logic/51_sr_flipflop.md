+++
title = "SR 플립플롭 (SR Flip-Flop)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# SR 플립플롭 (SR Flip-Flop)

## 핵심 인사이트 (3줄 요약)
1. SR 플립플롭은 클럭 신호(Clk)의 에지(상승 또는 하강)에서만 S, R 입력을 샘플링하여 상태를 변경하는 순차 회로로, SR 래치에 클럭 제어를 추가하여 타이밍을 동기화한다
2. 에지 트리거 방식은 레벨 트리거 래치와 달리 입력이 투명하게 전달되지 않으며, 정확한 타이밍 제어를 위해 클럭의 상승/하강 에지에서만 상태가 변한다
3. 기술사시험에서는 SR 플립플롭의 클럭 동기 방식, 에지 트리거 회로, 래치와의 차이, 메타스터빌리티가 핵심이다

## Ⅰ. 개요 (500자 이상)

SR 플립플롭(Set-Reset Flip-Flop)는 **클럭 신호(Clock, Clk)의 에지(Edge)에서만 동작하도록 설계된 순차 논리 회로**이다. SR 래치가 입력이 활성화되어 있는 동안 계속 변화할 수 있는 반면, SR 플립플롭은 클럭의 상승 에지(Rising Edge) 또는 하강 에지(Falling Edge)에서만 S, R 입력을 샘플링하여 상태를 변경한다.

```
SR 플립플롭 기본 개념:
입력: S (Set), R (Reset), Clk (Clock)
출력: Q, Q'

동작:
- 상승 에지(0→1): S, R을 샘플링하여 상태 변경
- 그 외: 상태 유지 (무시)

클럭 에지 트리거:
- Positive Edge: 0→1 전이에서만 동작
- Negative Edge: 1→0 전이에서만 동작
```

**클럭 동기화의 필요성:**

1. **타이밍 제어**: 모든 회로가 동일한 타이밍으로 동작
2. **데이터 안정성**: 클럭 에지에서만 데이터 전송
3. **경쟁 조건 방지**: 비동기 입력 간섭 최소화
4. **시스템 안정화**: 동기식 시스템 설계

```
비동기 vs 동기:
비동기 (래치):
- 입력 즉시 반영
- 타이밍 예측 어려움
- 경쟁 조건 위험

동기 (플립플롭):
- 클럭에 따라 동작
- 타이밍 예측 가능
- 안정적 동작
```

SR 플립플롭은 레지스터, 카운터, 상태 기계 등에서 사용되며, 현대 디지털 시스템의 핵심 저장 요소이다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 에지 트리거 SR 플립플롭 구조

```
Positive Edge SR 플립플롭:

S ───┐
     │
Clk ─┼── Edge Detector ─┐
     │                  │
R ───┴──────────────────┴── SR Latch
                            │
                         Q, Q'

Edge Detector:
Clk ──┬── AND ── Clk_Edge
      │    │
Clk' ─┘    │
           ↑
    상승 에지 검출 (0→1)

또는:
S ──┐
    │
R ──┼── 2개 D 플립플롭 (Master-Slave)
    │
Clk ─┘ (에지 트리거)
```

### 에지 검출 회로

```
상승 에지 검출기:

Clk ───┬── AND ── Clk_Rise
       │    │
Clk' ──┴────┘

동작:
Clk  : 0──1──1──0──0──1─
Clk' : 1──0──0──1──1──0─
AND  : 0──1──0──0──0──1─
       ↑      ↑
    상승 에지 (펄스 출력)

지연:
- NOT 게이트 지연만큼 Clk' 지연
- AND로 짧은 펄스 생성
- 펄스 폭 = 게이트 지연
```

### 진리표

```
Positive Edge SR 플립플롭:

| Clk | S | R | Q(t+1) | 동작 |
|-----|---|---|--------|------|
| 0→0 | X | X | Q(t) | 유지 |
| 0→1 | X | X | Q(t) | 유지 |
| 1→1 | X | X | Q(t) | 유지 |
| 1→0 | X | X | Q(t) | 유지 |
| ↑   | 0 | 0 | Q(t) | 유지 |
| ↑   | 0 | 1 |  0   | Reset |
| ↑   | 1 | 0 |  1   | Set |
| ↑   | 1 | 1 |  X   | 금지 |

↑: 상승 에지 (0→1)
X: 무관 (Don't Care)
```

### 타이밍 다이어그램

```
SR 플립플롭 타이밍:

   Clk: ────┐   ┌───┐   ┌───┐
            0→1 1→0 0→1 1→0
            ↑    ↑   ↑

   S: ────────┐   ┌───┐─────
              │   │
   R: ────────────┘   └───┐

   Q: ────────────┐   ┌───┐
   0 ──────────1───┘   └───┘ 0
                  Set   Reset

시점 분석:
t1: 상승 에지, S=0, R=0 → 유지
t2: 상승 에지, S=1, R=0 → Q=1 (Set)
t3: 상승 에지, S=0, R=1 → Q=0 (Reset)
```

### 전파 지연

```
에지 트리거 지연:

1. Edge Detector:
   - Clk → NOT: t_NOT
   - AND 게이트: t_AND
   - 총: t_NOT + t_AND

2. SR Latch:
   - S/R → Q: 2-3 게이트

3. 총 지연:
   t_total = t_NOT + t_AND + 2~3 게이트
           = 4-5 게이트

@ 100ps/게이트:
t_pd = 400-500ps
최대 클럭 = 1 / 500ps = 2 GHz

실제:
- 셋업/홀드 시간 고려
- 일반적으로 1 GHz 이하
```

### 메타스터빌리티

```
에지 근처 타이밍 위반:

        S/R 변화
            │
            ↓
   ┌────────┴────────┐
   │ t_setup │ t_hold │
   └─────────────────┘
             ↑
        Clk 상승 에지

셋업 위반:
- 에지 직전 S/R 변화
- 불안정한 상태
- 복구 시간 소요

홀드 위반:
- 에지 직후 S/R 변화
- 상태 오류 가능
- 회로 불안정

해결:
- 셋업/홀드 시간 준수
- STA 검증
- 셋업/홀드 마진 확인
```

## Ⅲ. 융합 비교

### SR 래치 vs SR 플립플롭

| 비교 항목 | SR 래치 | SR 플립플롭 |
|----------|---------|-------------|
| 트리거 | 레벨 | 에지 |
| 클럭 | 없음 | 필수 |
| 투명성 | 있음 | 없음 |
| 입력 반영 | 즉시 | 에지에서만 |
| 타이밍 제어 | 어려움 | 쉬움 |
| 응용 | 임시 저장 | 레지스터 |

### Positive vs Negative Edge

| 비교 항목 | Positive Edge | Negative Edge |
|----------|---------------|---------------|
| 트리거 | 0→1 | 1→0 |
| 표기 | ↑ 또는 ⟆ | ↓ 또는 ⟇ |
| 회로 | Clk + Clk' AND | Clk' + Clk AND |
| 응용 | 일반적 | 특수 목적 |

### 플립플롭 구현 방식

| 방식 | 구조 | 지연 | 면적 | 응용 |
|------|------|------|------|------|
| Edge Detector | + 래치 | 빠름 | 작음 | 간단 |
| Master-Slave | 2개 래치 | 중간 | 중간 | 일반적 |
| 6T SRAM | 6 트랜지스터 | 빠름 | 큼 | 메모리 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 동기식 레지스터

```
SR 플립플롭 레지스터:

D ───┐
     │
     ├── S ─┐
Clk ─┤    │
     │    └── SR FF ── Q
     └── R ──┘
         │
      D → SR 변환

D=0: S=0, R=1 → Reset (Q=0)
D=1: S=1, R=0 → Set (Q=1)

n비트 레지스터:
- n개 SR 플립플롭 병렬
- 공통 Clk
- 개별 D 입력
```

### 상태 기계

```
FSM (Finite State Machine):

State ── SR FF ── Next State
  ↓                    ↓
Current State       Logic

Clk에 따라 상태 전이:
1. 현재 상태 → 조합 논리
2. 조합 논리 → SR 입력
3. Clk 에지 → 다음 상태

예: 3-state 카운터
State 0 → State 1 → State 2 → State 0
```

### 클럭 도메인 교차

```
CDC (Clock Domain Crossing):

ClkA ── SR FF ── Q ───┐
                     │
                     └─→ ClkB ── SR FF ── Q'

문제:
- ClkA와 ClkB 위상차
- 셋업/홀드 위험

해결:
- 2 플립플롭 동기화
- FIFO 버퍼
- 핸드셰이크 프로토콜
```

## Ⅴ. 기대효과 및 결론

SR 플립플롭은 동기식 설계의 기초이다. 클럭 동기로 타이밍을 제어한다.

## 📌 관련 개념 맵

```
SR 플립플롭
├── 구조
│   ├── S 입력 (Set)
│   ├── R 입력 (Reset)
│   ├── Clk 입력 (Clock)
│   └── Q, Q' 출력
├── 트리거 방식
│   ├── Positive Edge (상승)
│   └── Negative Edge (하강)
├── 동작
│   ├── 에지에서만 상태 변경
│   ├── S=1: Set (Q=1)
│   ├── R=1: Reset (Q=0)
│   └── S=R=0: 유지
├── 타이밍
│   ├── 셋업 시간
│   ├── 홀드 시간
│   └── 전파 지연
└── 응용
    ├── 레지스터
    ├── 카운터
    └── 상태 기계
```

## 👶 어린이를 위한 3줄 비유 설명

1. SR 플립플롭은 사진기 같아요. 셔터(Clk)을 누르는 순간(S/R)에만 장면을 찍어서 저장(Q)해요
2. 셔터를 누르지 않으면 Set이나 Reset을 바꿔도 사진(Q)은 변하지 않아요. 셔터를 누를 때만 입력이 반영돼요
3. 컴퓨터의 레지스터는 수많은 플립플롭으로 만들어져서, 클럭 신호에 맞춰 데이터를 저장하고 처리해요

```python
# SR 플립플롭 시뮬레이션

from typing import Tuple, List


class EdgeDetector:
    """상승 에지 검출기"""

    def __init__(self):
        self.prev_clk = 0

    def detect_rising(self, clk: int) -> int:
        """
        상승 에지 검출

        Args:
            clk: 현재 클럭 값

        Returns:
            1 if 상승 에지, else 0
        """
        edge = 1 if (self.prev_clk == 0 and clk == 1) else 0
        self.prev_clk = clk
        return edge


class SRFlipFlop:
    """SR 플립플롭 시뮬레이션"""

    def __init__(self, edge_type: str = "rising"):
        """
        SR 플립플롭 초기화

        Args:
            edge_type: "rising" 또는 "falling"
        """
        self.q = 0
        self.q_prime = 1
        self.edge_type = edge_type
        self.edge_detector = EdgeDetector()
        self.prev_clk = 0

    def clock(self, s: int, r: int, clk: int) -> Tuple[int, int]:
        """
        클럭에 따른 상태 변화

        Args:
            s: Set 입력
            r: Reset 입력
            clk: 클럭 신호

        Returns:
            (q, q_prime): 현재 상태
        """
        if s not in [0, 1] or r not in [0, 1] or clk not in [0, 1]:
            raise ValueError("S, R, Clk는 0 또는 1이어야 합니다")

        # 에지 검출
        edge = 0
        if self.edge_type == "rising":
            edge = 1 if (self.prev_clk == 0 and clk == 1) else 0
        else:  # falling
            edge = 1 if (self.prev_clk == 1 and clk == 0) else 0

        self.prev_clk = clk

        # 에지에서만 상태 변경
        if edge == 1:
            if s == 1 and r == 1:
                raise ValueError("S=R=1은 금지된 상태입니다")
            elif s == 1:
                self.q = 1
                self.q_prime = 0
            elif r == 1:
                self.q = 0
                self.q_prime = 1
            # else: s=0, r=0 → 유지

        return self.q, self.q_prime

    def get_state(self) -> Tuple[int, int]:
        """현재 상태 반환"""
        return self.q, self.q_prime

    def reset(self):
        """플립플롭 리셋"""
        self.q = 0
        self.q_prime = 1


class MultiBitSRFF:
    """다중 비트 SR 플립플롭"""

    def __init__(self, bits: int):
        """
        n비트 SR 플립플롭

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.ffs = [SRFlipFlop() for _ in range(bits)]

    def clock(self, data: int, clk: int) -> List[int]:
        """
        클럭에 따른 상태 변화

        Args:
            data: 입력 데이터 (정수)
            clk: 클럭 신호

        Returns:
            상태 리스트
        """
        if not (0 <= data < 2**self.bits):
            raise ValueError(f"데이터는 {self.bits}비트 범위 내여야 합니다")

        outputs = []
        for i in range(self.bits):
            # 데이터 비트를 S, 반전을 R로
            bit = (data >> i) & 1
            s = bit
            r = 1 - bit

            self.ffs[i].clock(s, r, clk)
            outputs.append(self.ffs[i].get_state()[0])

        return outputs

    def get_state(self) -> int:
        """전체 상태를 정수로 반환"""
        value = 0
        for i in range(self.bits):
            value |= self.ffs[i].get_state()[0] << i
        return value


class StateMachine:
    """상태 기계 시뮬레이션 (3-state 카운터)"""

    def __init__(self):
        self.ff = SRFlipFlop()
        self.state = 0

    def step(self, s: int, r: int, clk: int) -> int:
        """
        한 스텝 진행

        Args:
            s: Set 입력 (상태 전환)
            r: Reset 입력 (초기화)
            clk: 클럭

        Returns:
            다음 상태
        """
        q, _ = self.ff.clock(s, r, clk)
        self.state = q
        return self.state


def demonstration():
    """SR 플립플롭 데모"""
    print("="*60)
    print("SR 플립플롭 (SR Flip-Flop) 데모")
    print("="*60)

    # SR 플립플롭
    print("\n[Positive Edge SR 플립플롭]")
    sr_ff = SRFlipFlop(edge_type="rising")

    test_sequence = [
        # (S, R, Clk, 설명)
        (0, 0, 0, "초기 (Clk=0)"),
        (0, 0, 1, "유지 (Clk=1, 에지 아님)"),
        (1, 0, 1, "Set (Clk 상승 에지)"),
        (0, 1, 0, "무시 (Clk=1→0)"),
        (0, 1, 1, "Reset (Clk 상승 에지)"),
        (0, 0, 1, "유지 (Clk 상승 에지)"),
    ]

    print(f"{'S':<3} {'R':<3} {'Clk':<4} {'Q':<3} {'설명':<15}")
    print("-" * 35)

    for s, r, clk, desc in test_sequence:
        q, q_prime = sr_ff.clock(s, r, clk)
        print(f"{s:<3} {r:<3} {clk:<4} {q:<3} {desc:<15}")

    # 다중 비트
    print(f"\n[8비트 SR 플립플롭 레지스터]")
    sr_ff8 = MultiBitSRFF(8)

    clock_cycles = [
        (0b10101010, 0),
        (0b10101010, 1),  # 상승 에지, 래치
        (0b11001100, 0),
        (0b11001100, 1),  # 상승 에지, 래치
    ]

    for data, clk in clock_cycles:
        result = sr_ff8.clock(data, clk)
        edge = "↑" if clk == 1 else ""
        print(f"Clk={clk} {edge}, Data=0b{data:08b} → Q=0b{sr_ff8.get_state():08b}")

    # 상태 기계
    print(f"\n[3-State 카운터]")
    fsm = StateMachine()

    # State 0 → 1 → 2 → 0
    print("State 0 → 1 → 2 → 0 전이:")

    # State 0 → 1
    state = fsm.step(s=1, r=0, clk=1)
    print(f"  S=1, R=0, Clk↑ → State = {state}")

    # State 1 → 2
    state = fsm.step(s=1, r=0, clk=0)
    state = fsm.step(s=1, r=0, clk=1)
    print(f"  S=1, R=0, Clk↑ → State = {state}")

    # State 2 → 0
    state = fsm.step(s=1, r=0, clk=0)
    state = fsm.step(s=1, r=0, clk=1)
    print(f"  S=1, R=0, Clk↑ → State = {state}")

    # Reset
    state = fsm.step(s=0, r=1, clk=1)
    print(f"  S=0, R=1, Clk↑ → State = {state} (Reset)")


if __name__ == "__main__":
    demonstration()
```
