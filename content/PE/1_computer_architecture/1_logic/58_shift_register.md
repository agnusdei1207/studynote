+++
title = "시프트 레지스터 (Shift Register)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# 시프트 레지스터 (Shift Register)

## 핵심 인사이트 (3줄 요약)
1. 시프트 레지스터는 클럭마다 데이터를 1비트씩 이동시키는 순차 회로로, 직렬-병렬 변환, 지연, 곱셈/나눗셈 등 다양한 용도로 사용된다
2. SISO, SIPO, PISO, PIPO의 4가지 기본 형태가 있으며, 양방향 시프트와 범용 시프트 레지스터로 확장된다
3. 기술사시험에서는 시프트 동작 원리, 직렬/병렬 변환, 응용 회로가 핵심이다

## Ⅰ. 개요 (500자 이상)

시프트 레지스터(Shift Register)는 **클럭 신호에 따라 저장된 데이터를 1비트씩 이동시키는 순차 논리 회로**이다. D 플립플롭을 직렬로 연결하여 구현하며, 데이터의 직렬-병렬 변환, 시간 지연, 비트 이동 연산 등 다양한 기능을 수행한다.

```
시프트 레지스터 기본 개념:
구조: D FF 직렬 연결
입력: Serial In, Parallel In
출력: Serial Out, Parallel Out
제어: Clk, Shift/Load, Direction

동작:
- Clk마다 1비트 이동
- Left Shift: 왼쪽으로 이동 (Q0←Q1←Q2←Q3←SI)
- Right Shift: 오른쪽으로 이동 (SI→Q0→Q1→Q2→Q3→SO)

특징:
- 직렬-병렬 변환
- 데이터 지연
- 비트 조작
```

**시프트 레지스터의 핵심 특징:**

1. **직렬-병렬 변환**: 직렬 데이터를 병렬로 변환하거나 그 반대
2. **지연 기능**: 클럭 사이클만큼 데이터 지연
3. **비트 조작**: 좌/우 시프트를 통한 곱셈/나눗셈
4. **FIFO/버퍼**: 큐 형태의 데이터 저장

```
시프트 레지스터 형태:

SISO (Serial In, Serial Out):
SI → [FF0] → [FF1] → [FF2] → [FF3] → SO

SIPO (Serial In, Parallel Out):
SI → [FF0] → [FF1] → [FF2] → [FF3]
       ↓       ↓       ↓       ↓
      Q0      Q1      Q2      Q3

PISO (Parallel In, Serial Out):
PI0 → [FF0] → [FF1] → [FF2] → [FF3] → SO
PI1 →    ↕
PI2 →    ↕
PI3 →    ↕

PIPO (Parallel In, Parallel Out):
PI0 → [FF0] → [FF1] → [FF2] → [FF3]
       ↓       ↓       ↓       ↓
      Q0      Q1      Q2      Q3
```

시프트 레지스터는 CPU 내부의 레지스터, 직렬 통신, 암호화 회로 등 다양한 곳에 응용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 기본 시프트 레지스터 구조

```
4비트 Right Shift 레지스터:

Serial In (SI) ──┐
                 │
                 ├──[D FF 0]── Q0 ──┬──[D FF 1]── Q1 ──┬──[D FF 2]── Q2 ──┬──[D FF 3]── Q3 ── Serial Out (SO)
                 │                │                │                │
               Clk0             Clk1             Clk2             Clk3
                 │                │                │                │
                 └────────────────┴────────────────┴────────────────┴───── Common Clk

동작:
- Clk마다 모든 FF가 동시에 상태 변경
- Q3 → SO (출력)
- Q2 → Q3
- Q1 → Q2
- Q0 → Q1
- SI → Q0 (입력)
```

### SISO (Serial In, Serial Out)

```
SISO 시프트 레지스터:

SI ──[FF0]──[FF1]──[FF2]──[FF3]── SO

특징:
- 입력: 직렬 1비트
- 출력: 직렬 1비트
- 지연: n 클럭 (n=FF 개수)

타이밍:
Clk: ────┬───┬───┬───┬───┬───
      ↑   ↑   ↑   ↑   ↑   ↑

SI:  ──1─0─1─1─0─1─...

Q0:  ────1─0─1─1─0─1─...
Q1:  ──────1─0─1─1─0─...
Q2:  ────────1─0─1─1─...
Q3:  ───────────1─0─1─...

SO:  ───────────────1─0─1─...

지연: 4 클럭
```

### SIPO (Serial In, Parallel Out)

```
SIPO 시프트 레지스터:

SI ──[FF0]──[FF1]──[FF2]──[FF3]
       ↓       ↓       ↓       ↓
      Q0      Q1      Q2      Q3

특징:
- 입력: 직렬 1비트
- 출력: 병렬 n비트
- 용도: 직렬→병렬 변환

예: 4비트 변환
입력: 1,0,1,1 (직렬)
클럭 1: Q0=1
클럭 2: Q1=0, Q0=?
클럭 3: Q2=1, Q1=0, Q0=?
클럭 4: Q3=1, Q2=1, Q1=0, Q0=?
출력: Q3Q2Q1Q0 = ? (병렬)
```

### PISO (Parallel In, Serial Out)

```
PISO 시프트 레지스터:

PI0 ─┬──[MUX]──[FF0]──[FF1]──[FF2]──[FF3]── SO
PI1 ─┤       ↕       ↓       ↓       ↓
PI2 ─┤   Load      Q0      Q1      Q2
PI3 ─┘   (Shift)   ↓       ↓       ↓
                  Q3      Q2      Q1

동작 모드:
1. Load (Parallel In):
   - MUX가 PI 선택
   - PI0→Q0, PI1→Q1, PI2→Q2, PI3→Q3

2. Shift:
   - MUX가 이전 FF 선택
   - SI→Q0→Q1→Q2→Q3→SO

타이밍:
Load=1: PI0-3 → Q0-3 (병렬 로드)
Load=0, Clk: 시프트 동작
```

### PIPO (Parallel In, Parallel Out)

```
PIPO 시프트 레지스터:

PI0 ──[FF0]──[FF1]──[FF2]──[FF3]
       ↓       ↓       ↓       ↓
      Q0      Q1      Q2      Q3

Load=1: PI → Q (병렬 로드)
Clk: 시프트 동작

특징:
- 입력: 병렬 n비트
- 출력: 병렬 n비트
- 용도: 지연, 버퍼
```

### 양방향 시프트 레지스터

```
Bidirectional Shift Register:

Left Shift:  LS ──→[FF0]←─[FF1]←─[FF2]←─[FF3]
                       ↓       ↓       ↓       ↓
                      Q0      Q1      Q2      Q3

Right Shift: RS ──→[FF0]─→[FF1]─→[FF2]─→[FF3]
                       ↓       ↓       ↓       ↓
                      Q0      Q1      Q2      Q3

MUX 제어:
- S=0: Right Shift (RS→Q0→Q1→Q2→Q3)
- S=1: Left Shift (LS→Q3→Q2→Q1→Q0)

D0 = S·Q1 + S'·RS
D1 = S·Q2 + S'·Q0
D2 = S·Q3 + S'·Q1
D3 = S·LS + S'·Q2
```

### 범용 시프트 레지스터 (Universal)

```
Universal Shift Register (74xx194):

기능:
- Parallel Load
- Right Shift
- Left Shift
- Hold (유지)

제어 신호 (S1, S0):
S1 S0 | 동작
-----|------
0  0  | Hold (유지)
0  1  | Right Shift (RS→Q0→Q1→Q2→Q3)
1  0  | Left Shift (LS→Q3→Q2→Q1→Q0)
1  1  | Parallel Load (PI→Q)

회로 구조:
PI0-3 ──┬──[MUX 0]──[FF0]── Q0
RS   ───┤    ↑       ↓
        │    └── Select
S1,S0 ──┤
        └──[MUX 1]──[FF1]── Q1
             ↑       ↓
             Q0      Q1
            (이하 유사)
```

### 회로 응용

```
1. 직렬-병렬 변환:
   SIPO: 직렬 통신 → 병렬 데이터
   PISO: 병렬 데이터 → 직렬 통신

2. 데이터 지연:
   SISO: n클럭 지연

3. 카운터:
   Ring Counter: Q0→Q1→Q2→Q3→Q0
   Johnson Counter: Q0→Q1→Q2→Q3→Q0'

4. 곱셈/나눗셈:
   Left Shift: ×2
   Right Shift: ÷2
```

## Ⅲ. 융합 비교

### 시프트 레지스터 형태 비교

| 형태 | 입력 | 출력 | 지연 | 응용 |
|------|------|------|------|------|
| SISO | 직렬 | 직렬 | n클럭 | 지연, FIFO |
| SIPO | 직렬 | 병렬 | n클럭 | S→P 변환 |
| PISO | 병렬 | 직렬 | 1클럭 | P→S 변환 |
| PIPO | 병렬 | 병렬 | 1클럭 | 버퍼, 레지스터 |

### 시프트 동작 비교

| 동작 | 방향 | LSB | MSB | 응용 |
|------|------|-----|-----|------|
| Left Shift | ← | ×2 | 0 | 곱셈 |
| Right Shift | → | 0 | ÷2 | 나눗셈 |
| Rotate | ↻ | MSB→LSB | 순환 | 로테이트 |
| Arithmetic | → | MSB유지 | ÷2 | 부호 유지 |

### 응용 회로 비교

| 응용 | 구조 | 지연 | 복잡도 | 특징 |
|------|------|------|--------|------|
| Ring Counter | Qn→Q0 | 1클럭 | 낮음 | 1 hot encoding |
| Johnson Counter | Qn'→Q0 | 1클럭 | 낮음 | 2n 상태 |
| LFSR | 피드백 | 1클럭 | 중간 | PRNG |
| Barrel Shifter | 병렬 MUX | 1클럭 | 높음 | n비트 시프트 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 직렬 통신 인터페이스

```
UART SIPO/PISO:

송신 (PISO):
CPU ──[PIPO]──[PISO]── TxD (직렬)
     Parallel  Shift

수신 (SIPO):
RxD (직렬)──[SIPO]──[PIPO]── CPU
     Shift     Parallel

타이밍:
- Start Bit (0)
- Data Bits (5-8)
- Parity Bit (Optional)
- Stop Bit (1, 1.5, 2)

波特率:
- 9600: 1비트 = 104µs
- 115200: 1비트 = 8.68µs
```

### CPU 레지스터 시프트

```
ALU 시프트 연산:

Operand ──[Barrel Shifter]── Result
           ↑
      Shift Amount

Barrel Shifter:
- n비트 동시 시프트
- O(1) 지연
- O(n²) 게이트

구조:
Input[7:0]
├─→ Shift 0 ─┬─ MUX ─→ Output
│            │
├─→ Shift 1 ─┤
│            │
├─→ Shift 2 ─┤
│            │
└─→ Shift 7 ─┘
```

### LFSR (Linear Feedback Shift Register)

```
LFSR PRNG:

[FF0]→[FF1]→[FF2]→[FF3]
  ↑              │
  └── XOR ←──────┘
      ↑
   Tap (Q3 ⊕ Q2)

특징:
- 의사 난수 생성
- 최대 주기: 2ⁿ-1
- 테스트 패턴 생성

응용:
- 암호화
- 통신 스크램블링
- BIST (Built-In Self-Test)
```

### Ring Counter

```
4비트 Ring Counter:

초기: Q0=1, Q1=0, Q2=0, Q3=0
클럭 1: Q0=0, Q1=1, Q2=0, Q3=0
클럭 2: Q0=0, Q1=0, Q2=1, Q3=0
클럭 3: Q0=0, Q1=0, Q2=0, Q3=1
클럭 4: Q0=1, Q1=0, Q2=0, Q3=0 (순환)

상태: 1000→0100→0010→0001→1000
주기: 4

특징:
- 1 hot encoding
- 디코더 불필요
- 상태 검출 간단
```

## Ⅴ. 기대효과 및 결론

시프트 레지스터는 데이터 이동의 기본이다. 직렬/병렬 변환, 곱셈/나눗셈에 필수적이다.

## 📌 관련 개념 맵

```
시프트 레지스터
├── 형태
│   ├── SISO (Serial In, Serial Out)
│   ├── SIPO (Serial In, Parallel Out)
│   ├── PISO (Parallel In, Serial Out)
│   └── PIPO (Parallel In, Parallel Out)
├── 동작
│   ├── Left Shift (왼쪽으로)
│   ├── Right Shift (오른쪽으로)
│   ├── Rotate (순환)
│   └── Arithmetic (산술)
├── 구현
│   ├── D FF 체인
│   ├── 양방향 MUX
│   └── 범용 (S1,S0 제어)
└── 응용
    ├── 직렬 통신 (UART)
    ├── 곱셈/나눗셈
    ├── Ring/Johnson Counter
    └── LFSR (PRNG)
```

## 👶 어린이를 위한 3줄 비유 설명

1. 시프트 레지스터는 사람들이 일렬로 서서 구슬을 옆으로 넘기는 것과 같아요. 클럭이 오면每个人이 자기 구슬을 옆 사람에게 넘겨요
2. SISO는 한쪽에서 넣고 다른 쪽에서 빼는 것이고, SIPO는 한쪽에서 넣고 모두가 자기 구슬을 보여주는 거예요
3. 시프트는 왼쪽/오른쪽으로 이동할 수 있어요. 왼쪽으로 시프트하면 숫자가 2배가 되고(×2), 오른쪽으로 시프트하면 2로 나뉘어져요(÷2)

```python
# 시프트 레지스터 시뮬레이션

from typing import List


class ShiftRegister:
    """기본 시프트 레지스터 (SISO)"""

    def __init__(self, bits: int):
        """
        n비트 시프트 레지스터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.reg = [0] * bits

    def clock(self, serial_in: int) -> int:
        """
        클럭에 따른 시프트

        Args:
            serial_in: 직렬 입력

        Returns:
            직렬 출력
        """
        serial_out = self.reg[-1]

        # Right Shift
        for i in range(self.bits - 1, 0, -1):
            self.reg[i] = self.reg[i - 1]
        self.reg[0] = serial_in

        return serial_out

    def get_parallel(self) -> List[int]:
        """병렬 출력 (SIPO)"""
        return self.reg.copy()

    def set_parallel(self, data: List[int]):
        """병렬 입력 (PIPO)"""
        if len(data) != self.bits:
            raise ValueError(f"데이터는 {self.bits}비트여야 합니다")
        self.reg = data.copy()


class SIPORegister(ShiftRegister):
    """Serial In, Parallel Out 레지스터"""

    def __init__(self, bits: int):
        super().__init__(bits)

    def load_serial(self, data_bits: List[int]) -> List[int]:
        """
        직렬 데이터 로드

        Args:
            data_bits: 직렬 비트 리스트

        Returns:
            병렬 출력
        """
        for bit in data_bits:
            self.clock(bit)
        return self.get_parallel()


class PISORegister:
    """Parallel In, Serial Out 레지스터"""

    def __init__(self, bits: int):
        self.bits = bits
        self.reg = [0] * bits

    def load_parallel(self, data: List[int]):
        """병렬 로드"""
        if len(data) != self.bits:
            raise ValueError(f"데이터는 {self.bits}비트여야 합니다")
        self.reg = data.copy()

    def shift_out(self) -> List[int]:
        """직렬로 출력"""
        result = []
        for _ in range(self.bits):
            result.append(self.reg[0])
            # Shift
            for i in range(self.bits - 1):
                self.reg[i] = self.reg[i + 1]
            self.reg[-1] = 0
        return result


class UniversalShiftRegister:
    """범용 시프트 레지스터"""

    def __init__(self, bits: int):
        self.bits = bits
        self.reg = [0] * bits

    def clock(self, s1: int, s0: int, serial_in: int = 0, parallel_in: List[int] = None):
        """
        범용 시프트 레지스터 클럭

        Args:
            s1, s0: 제어 신호
            serial_in: 직렬 입력 (LSB for right shift, MSB for left shift)
            parallel_in: 병렬 입력 (parallel load)

        Returns:
            현재 상태
        """
        # Hold
        if s1 == 0 and s0 == 0:
            pass
        # Right Shift
        elif s1 == 0 and s0 == 1:
            for i in range(self.bits - 1, 0, -1):
                self.reg[i] = self.reg[i - 1]
            self.reg[0] = serial_in
        # Left Shift
        elif s1 == 1 and s0 == 0:
            for i in range(self.bits - 1):
                self.reg[i] = self.reg[i + 1]
            self.reg[-1] = serial_in
        # Parallel Load
        elif s1 == 1 and s0 == 1:
            if parallel_in:
                self.reg = parallel_in.copy()

        return self.reg.copy()

    def get_state(self) -> List[int]:
        """현재 상태"""
        return self.reg.copy()


class RingCounter:
    """링 카운터"""

    def __init__(self, bits: int):
        self.bits = bits
        self.reg = [0] * bits
        # 초기: 1000...0
        self.reg[0] = 1

    def clock(self) -> List[int]:
        """클럭에 따른 순환"""
        # Right rotate
        temp = self.reg[-1]
        for i in range(self.bits - 1, 0, -1):
            self.reg[i] = self.reg[i - 1]
        self.reg[0] = temp
        return self.reg.copy()

    def get_state(self) -> int:
        """상태를 정수로 반환"""
        value = 0
        for i in range(self.bits):
            value |= self.reg[i] << i
        return value


class LFSR:
    """Linear Feedback Shift Register"""

    def __init__(self, bits: int, taps: List[int]):
        """
        n비트 LFSR

        Args:
            bits: 비트 수
            taps: 피드백 탭 위치 (0-indexed)
        """
        self.bits = bits
        self.taps = taps
        self.reg = [1] * bits  # 초기: all 1s

    def clock(self) -> int:
        """
        클럭에 따른 상태 변화

        Returns:
            출력 비트
        """
        output = self.reg[-1]

        # 피드백 계산 (XOR)
        feedback = 0
        for tap in self.taps:
            feedback ^= self.reg[tap]

        # Shift
        for i in range(self.bits - 1, 0, -1):
            self.reg[i] = self.reg[i - 1]
        self.reg[0] = feedback

        return output

    def get_state(self) -> int:
        """현재 상태"""
        value = 0
        for i in range(self.bits):
            value |= self.reg[i] << i
        return value


def demonstration():
    """시프트 레지스터 데모"""
    print("=" * 60)
    print("시프트 레지스터 (Shift Register) 데모")
    print("=" * 60)

    # SISO
    print("\n[SISO 시프트 레지스터]")
    siso = ShiftRegister(bits=4)

    # 입력: 1011
    input_bits = [1, 0, 1, 1, 0, 0, 0, 0]
    print(f"입력: {input_bits}")
    print(f"{'Clk':<4} {'SI':<3} {'SO':<3} {'상태':<10}")
    print("-" * 25)

    for i, bit in enumerate(input_bits):
        so = siso.clock(bit)
        state = siso.get_parallel()
        print(f"{i:<4} {bit:<3} {so:<3} {state}")

    # SIPO
    print(f"\n[SIPO 시프트 레지스터]")
    sipo = SIPORegister(bits=4)

    input_data = [1, 0, 1, 1]
    output = sipo.load_serial(input_data)
    print(f"직렬 입력: {input_data}")
    print(f"병렬 출력: {output}")

    # PISO
    print(f"\n[PISO 시프트 레지스터]")
    piso = PISORegister(bits=4)

    parallel_data = [1, 0, 1, 1]
    piso.load_parallel(parallel_data)
    print(f"병렬 입력: {parallel_data}")

    serial_out = piso.shift_out()
    print(f"직렬 출력: {serial_out}")

    # 범용 시프트 레지스터
    print(f"\n[범용 시프트 레지스터]")
    usr = UniversalShiftRegister(bits=4)

    # 초기 상태
    usr.clock(1, 1, parallel_in=[0, 0, 0, 1])
    print(f"초기: {usr.get_state()}")

    # Right Shift
    usr.clock(0, 1, serial_in=1)
    print(f"Right Shift: {usr.get_state()}")

    # Left Shift
    usr.clock(1, 0, serial_in=0)
    print(f"Left Shift: {usr.get_state()}")

    # Hold
    usr.clock(0, 0)
    print(f"Hold: {usr.get_state()}")

    # Ring Counter
    print(f"\n[링 카운터]")
    ring = RingCounter(bits=4)

    print("4 클럭 사이클:")
    for i in range(4):
        state = ring.clock()
        print(f"  {i}: {state} (0b{ring.get_state():04b})")

    # LFSR
    print(f"\n[LFSR (4비트, taps=[3,2])]")
    lfsr = LFSR(bits=4, taps=[3, 2])

    print("16 클럭 사이클:")
    for i in range(16):
        output = lfsr.clock()
        state = lfsr.get_state()
        print(f"  {i:2d}: 출력={output}, 상태=0b{state:04b}")


if __name__ == "__main__":
    demonstration()
```
