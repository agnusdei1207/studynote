+++
title = "D 플립플롭 (D Flip-Flop)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# D 플립플롭 (D Flip-Flop)

## 핵심 인사이트 (3줄 요약)
1. D 플립플롭은 클럭 상승/하강 에지에서 D 입력을 샘플링하여 Q에 저장하는 에지 트리거 저장 장치로, 레지스터, 카운터, 시프트 레지스터 등 디지털 시스템의 핵심 저장 요소이다
2. D 래치와 달리 클럭 에지에서만 동작하며, 투명성이 없고 셋업/홀드 시간을 준수해야 안정적으로 동작한다
3. 기술사시험에서는 D 플립플롭의 타이밍 다이어그램, 셋업/홀드 시간, 메타스터빌리티, 병렬 D 플립플롭 구조가 핵심이다

## Ⅰ. 개요 (500자 이상)

D 플립플롭(Data Flip-Flop, D-FF)는 **클럭 신호의 에지(Edge)에서만 D 입력을 샘플링하여 Q 출력에 저장**하는 가장 널리 사용되는 순차 논리 회로이다. SR 플립플롭의 금지 상태 문제를 해결하고 단일 데이터 입력으로 1비트 정보를 저장한다.

```
D 플립플롭 기본 개념:
입력: D (Data), Clk (Clock)
출력: Q (저장된 값), Q' (반전)

동작:
- 클럭 상승 에지(↑): Q ← D (샘플링)
- 그 외 시간: Q 유지

타이밍:
          ┌─── t_setup ───┐
D ─────────┤               ├─── t_hold ───
            └───────┬───────┘
                    ↑
              Clk 상승 에지
```

**D 플립플롭의 핵심 특징:**

1. **에지 트리거**: 클럭의 상승 또는 하강 에지에서만 동작
2. **비투명성**: 입력이 출력에 즉시 반영되지 않음
3. **단일 데이터 입력**: S, R 없이 D 하나만으로 동작
4. **금지 상태 없음**: D의 값에 따라 자동으로 Set/Reset 결정

```
D 플립플롭 vs D 래치:
D 래치: E=1일 때 D가 Q에 즉시 반영 (투명)
D 플립플롭: Clk 에지에서만 D가 Q로 전송 (비투명)

장점:
- 타이밍 예측 가능
- 동기식 설계 용이
- 경쟁 조건 최소화
```

D 플립플롭은 CPU 레지스터, 카운터, 시프트 레지스터, 상태 기계 등 모든 동기식 디지털 시스템의 기본 요소이다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### D 플립플롭 회로 구조

```
D 플립플롭 구조 (Positive Edge):

D ───┐
     │
Clk ─┼── Edge Detector + D Latch
     │
     └── Q, Q'

또는 Master-Slave 구조:

Clk ──┬── Master Latch (Clk=1 활성)
      │    │
D ────┴──── Qm
           │
Clk' ───┬── Slave Latch (Clk'=1 활성)
        │    │
Qm ─────┴── Q

Master-Slave 동작:
Clk=1: Master 투명, Slave 래치
Clk=0: Master 래치, Slave 투명
Clk 상승/하강: 데이터 전송
```

### 진리표

```
Positive Edge D 플립플롭:
| Clk | D | Q(t+1) | 동작 |
|-----|---|--------|------|
| 0 | X | Q(t) | 유지 |
| 1 | X | Q(t) | 유지 |
| ↓ | X | Q(t) | 유지 |
| ↑ | 0 |   0   | Q←0 |
| ↑ | 1 |   1   | Q←1 |

↑: 상승 에지
X: 무관 (Don't Care)
```

### 타이밍 다이어그램

```
D 플립플롭 타이밍:

   D: ──┐   ┌──┐   ┌──┐
      │   │  ││   ││
 Clk: ───┴─┬┴┬┴───┴┬┴┬──
            ↑  ↑   ↑  ↑
         ↑  ↑   ↑  ↑
   Q: ───┴──┴───┴──┴──

샘플링 시점:
1: D=1 → Q=1
2: D=0 → Q=0
3: D=1 → Q=1
4: D=1 → Q=1 (D 변화 없음)

특징:
- Clk=1 또는 Clk=0 기간의 D 변화 무시
- 상승 에지에서만 D를 샘플링
```

### 셋업/홀드 시간

```
타이밍 제약 조건:

   D: ─────────┐        ┌───
              │        │
 Clk: ─────────┴────────┴───
                ↑        ↑
             t_setup  t_hold

1. 셋업 시간 (t_setup):
   - Clk 에지 이전 D가 안정되어야 할 시간
   - 일반적으로 0.5~2 ns

2. 홀드 시간 (t_hold):
   - Clk 에지 이후 D를 유지해야 할 시간
   - 일반적으로 0~0.5 ns

3. 클럭-to-Q 지연 (t_cq):
   - Clk 에지에서 Q 변화까지의 시간
   - 일반적으로 0.5~1 ns

위반 시:
- 메타스터빌리티 발생
- Q가 불안정
- 회로 오동작
```

### 메타스터빌리티

```
D 플립플롭 메타스터빌리티:

정상 동작:
D 변화 → 안정화 → Clk 에지 → Q 안정

위반 동작:
D 변화 → Clk 에지 → Q 불안정
              ↑
         셋업/홀드 위반

회로적 원인:
- 피드백 루프 미완성
- Master-Slave 경쟁
- 신호 레벨 중간

복구 시간:
- 일반적으로 2-5 ns
- 불확실한 값
- 설계에서 절대 피해야 함
```

### 다중 비트 D 플립플롭

```
n비트 D 플립플롭:

D[n-1:0] ──┬── D FF 0 ── Q[0]
           ├── D FF 1 ── Q[1]
           ├── ...      ── ...
           └── D FF n-1 ── Q[n-1]
                │
           Clk (공통)

용도:
- n비트 레지스터
- 병렬 데이터 저장
- 카운터
- 시프트 레지스터

지연:
- 모든 비트 거의 동시
- 스큐(Skew): 50-200 ps
```

## Ⅲ. 융합 비교

### D 플립플롭 vs D 래치

| 비교 항목 | D 래치 | D 플립플롭 |
|----------|--------|-----------|
| 트리거 | 레벨 | 에지 |
| Enable | E=1 시 투명 | Clk 에지에서만 |
| 투명성 | 있음 | 없음 |
| 셋업/홀드 | 필요 | 필요 |
| 타이밍 제어 | 어려움 | 쉬움 |
| 응용 | 파이프라인 | 일반 레지스터 |
| 합성 | 간단 | 복잡 |

### 플립플롭 종류

| 타입 | 입력 | 출력 | 특징 | 응용 |
|------|------|------|------|------|
| D FF | D, Clk | Q | 데이터 저장 | 일반적 |
| JK FF | J, K, Clk | Q | 토글 | 카운터 |
| T FF | T, Clk | Q | 토글 전용 | 카운터 |
| SR FF | S, R, Clk | Q | Set/Reset | 상태 기계 |

### Positive vs Negative Edge

| 비교 항목 | Positive Edge | Negative Edge |
|----------|---------------|---------------|
| 트리거 | 0→1 | 1→0 |
| 지연 | 빠름 | 중간 |
| 응용 | 일반적 | Low-Power |
| 표기 | ⟆ 또는 ↑ | ⟇ 또는 ↓ |

## Ⅳ. 실무 적용 및 기술사적 판단

### CPU 레지스터

```
32비트 범용 레지스터:

D[31:0] ──┬── D FF 0  ── Q[0]
          ├── D FF 1  ── Q[1]
          ├── ...      ── ...
          └── D FF 31 ── Q[31]
               │
          Clk (공통)

Write Back WB 스테이지:
- WB 클럭 상승 에지
- ALU Result → 레지스터
- 한 클럭에 쓰기 완료

지연:
- Clk-to-Q: ~500ps
- 셋업: 200ps
- 홀드: 100ps

@ 3GHz 클럭 (333ps):
- 타이밍 마진: 333 - 500 = -167ps (위반!)
- 해결: 파이프라이닝 필요
```

### 카운터

```
4비트 카운터 (D FF 기반):

Q3 Q2 Q1 Q0
│  │  │  │
└──┴──┴──┴──→ D FF 3
│  │  │  │
└──┴──┴──┴──→ D FF 2
│  │  │  │
└──┴──┴──┴──→ D FF 1
│  │  │  │
└──┴──┴──┴──→ D FF 0
          │
   Clk ────┴── Increment

동작:
- 각 Q[i]이 D[i+1]로 입력
- D[0] = ~Q[0] (토글)
- Clk마다 +1 카운트

지연:
- 4 스테이지: 4 × t_cq
- 총 지연: ~2ns
- 최대 클럭: 500 MHz
```

### 시프트 레지스터

```
4비트 시프트 레지스터:

Din ── D FF 0 ── Q0 ── D FF 1 ── Q1 ── D FF 2 ── Q2 ── D FF 3 ── Q3
        ↑          ↑          ↑          ↑
       Clk        Clk        Clk        Clk

좌측 시프트 (Left Shift):
- 각 클럭마다 한 비트 이동
- Q0 → Q1 → Q2 → Q3

용도:
- 곱셈/나눗셈
- 직렬-병렬 변환
- 데이터 시프트

지연:
- n비트 시프트: n × t_cq
- 파이프라인으로 개선 가능
```

## Ⅴ. 기대효과 및 결론

D 플립플롭은 디지털 시스템의 핵심이다. 동기식 설계의 기본 저장 요소이다.

## 📌 관련 개념 맵

```
D 플립플롭
├── 구조
│   ├── D 입력 (Data)
│   ├── Clk 입력 (Clock)
│   └── Q, Q' 출력
├── 트리거
│   ├── Positive Edge (0→1)
│   └── Negative Edge (1→0)
├── 타이밍
│   ├── 셋업 시간
│   ├── 홀드 시간
│   └── Clk-to-Q 지연
├── 메타스터빌리티
│   ├── 셋업/홀드 위반
│   ├── 복구 시간
│   └── 안정화
└── 응용
    ├── 레지스터
    ├── 카운터
    └── 시프트 레지스터
```

## 👶 어린이를 위한 3줄 비유 설명

1. D 플립플롭은 사진기 같아요. 셔터 버튼(Clk)을 누르는 순간에만 D의 값을 사진(Q)으로 찍어서 저장해요
2. 셔터를 누르지 않으면 D가 변해도 사진(Q)은 변하지 않아요. 셔터를 누를 때만 D값이 Q로 저장돼요
3. 컴퓨터의 레지스터는 수많은 D 플립플롭으로 만들어져서, 클럭 신호에 맞춰 데이터를 저장하고 처리해요

```python
# D 플립플롭 시뮬레이션

from typing import List


class DFlipFlop:
    """D 플립플롭 시뮬레이션"""

    def __init__(self, edge_type: str = "rising"):
        """
        D 플립플롭 초기화

        Args:
            edge_type: "rising" 또는 "falling"
        """
        self.q = 0
        self.q_prime = 1
        self.edge_type = edge_type
        self.prev_clk = 0

    def clock(self, d: int, clk: int) -> tuple:
        """
        클럭에 따른 상태 변화

        Args:
            d: Data 입력
            clk: 클럭 신호

        Returns:
            (q, q_prime): 현재 상태
        """
        if d not in [0, 1] or clk not in [0, 1]:
            raise ValueError("D, Clk는 0 또는 1이어야 합니다")

        # 에지 검출
        edge = False
        if self.edge_type == "rising":
            edge = (self.prev_clk == 0 and clk == 1)
        else:  # falling
            edge = (self.prev_clk == 1 and clk == 0)

        self.prev_clk = clk

        # 에지에서만 상태 변경
        if edge:
            self.q = d
            self.q_prime = 1 - d

        return self.q, self.q_prime

    def get_state(self) -> tuple:
        """현재 상태 반환"""
        return self.q, self.q_prime

    def reset(self):
        """플립플롭 리셋"""
        self.q = 0
        self.q_prime = 1


class MultiBitDFF:
    """다중 비트 D 플립플롭"""

    def __init__(self, bits: int):
        """
        n비트 D 플립플롭

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.ffs = [DFlipFlop() for _ in range(bits)]

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
            bit = (data >> i) & 1
            self.ffs[i].clock(bit, clk)
            outputs.append(self.ffs[i].get_state()[0])

        return outputs

    def get_state(self) -> int:
        """전체 상태를 정수로 반환"""
        value = 0
        for i in range(self.bits):
            value |= self.ffs[i].get_state()[0] << i
        return value


class Counter:
    """카운터 시뮬레이션"""

    def __init__(self, bits: int = 4):
        """
        n비트 카운터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.dff = MultiBitDFF(bits)

    def increment(self, clk: int) -> int:
        """
        카운트 증가

        Args:
            clk: 클럭 신호

        Returns:
            현재 카운트 값
        """
        if clk == 1:
            current = self.dff.get_state()
            next_val = (current + 1) & ((1 << self.bits) - 1)
            self.dff.clock(next_val, clk)
        return self.dff.get_state()


class ShiftRegister:
    """시프트 레지스터 시뮬레이션"""

    def __init__(self, bits: int = 8):
        """
        n비트 시프트 레지스터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.dff = MultiBitDFF(bits)

    def shift_left(self, data_in: int, clk: int) -> int:
        """
        좌측 시프트

        Args:
            data_in: 입력 데이터 (LSB)
            clk: 클럭 신호

        Returns:
            현재 레지스터 값
        """
        if clk == 1:
            current = self.dff.get_state()
            # 좌측 시프트: 새로운 비트를 LSB로
            next_val = ((current << 1) | data_in) & ((1 << self.bits) - 1)
            self.dff.clock(next_val, clk)
        return self.dff.get_state()


def demonstration():
    """D 플립플롭 데모"""
    print("="*60)
    print("D 플립플롭 (D Flip-Flop) 데모")
    print("="*60)

    # D 플립플롭
    print("\n[Positive Edge D 플립플롭]")
    d_ff = DFlipFlop(edge_type="rising")

    test_sequence = [
        (0, 0, "초기"),
        (1, 0, "무시 (Clk=0)"),
        (1, 1, "무시 (Clk=1, 에지 아님)"),
        (0, 1, "D=1 → Q=1 (상승 에지)"),
        (1, 0, "무시 (Clk=1→0)"),
        (1, 1, "D=1 → Q=1 (상승 에지)"),
        (0, 1, "D=0 → Q=0 (상승 에지)"),
    ]

    print(f"{'D':<3} {'Clk':<4} {'Q':<3} {'설명':<25}")
    print("-" * 40)

    for d, clk, desc in test_sequence:
        q, _ = d_ff.clock(d, clk)
        print(f"{d:<3} {clk:<4} {q:<3} {desc:<25}")

    # 다중 비트
    print(f"\n[8비트 레지스터]")
    reg_8bit = MultiBitDFF(8)

    data_in = 0b10101010
    print(f"입력 데이터: 0b{data_in:08b}")

    # 클럭 3 사이클
    for i in range(3):
        clk = 1
        reg_8bit.clock(data_in, clk)
        print(f"클럭 {i+1} (상승 에지): Q = 0b{reg_8bit.get_state():08b}")

    # 카운터
    print(f"\n[4비트 카운터]")
    counter = Counter(bits=4)

    print(f"0부터 15까지 카운트:")
    for i in range(16):
        count = counter.increment(1 if i == 0 else 0)  # 첫 번만 상승 에지
        if i < 16:
            print(f"  {i}: 0b{count:04b} ({count})")

    # 시프트 레지스터
    print(f"\n[8비트 시프트 레지스터]")
    shift_reg = ShiftRegister(bits=8)

    # 1을 왼쪽으로 시프트
    print("좌측 시프트 (1 입력):")
    for i in range(8):
        result = shift_reg.shift_left(1, 1)  # data_in=1
        print(f"  {i}: 0b{result:08b}")


if __name__ == "__main__":
    demonstration()
```
