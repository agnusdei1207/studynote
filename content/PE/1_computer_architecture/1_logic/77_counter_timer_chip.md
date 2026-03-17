+++
title = "카운터/타이머 칩 (Counter/Timer Chip)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 카운터/타이머 칩 (Counter/Timer Chip)

## 핵심 인사이트 (3줄 요약)
1. 카운터/타이머 칩은 복수 개의 독립적인 카운터/타이머를 하나의 칩에 통합한 것으로, Intel 8254 PIT와 같이 3개의 16비트 카운터와 다양한 동작 모드를 제공한다
2. 각 카운터는 독립적으로 클럭 입력, 게이트 입력, 출력을 가지며 6가지 동작 모드(Interrupt on TC, Rate Generator, Square Wave 등)를 지원한다
3. 기술사시험에서는 8254 내부 구조, 동작 모드, 프로그래밍 방법, PC 시스템 활용이 핵심이다

## Ⅰ. 개요 (500자 이상)

카운터/타이머 칩(Counter/Timer Chip)은 **여러 개의 독립적인 카운터와 타이머 기능을 하나의 칩에 통합한 집적 회로**이다. 가장 대표적인 예는 Intel 8254 Programmable Interval Timer(PIT)로, 3개의 16비트 카운터를 제공한다.

```
카운터/타이머 칩 기본 개념:
구조: 복수 개의 독립 Counter
입력: Clock, Gate, Data
출력: OUT, Interrupt

기능:
- 주기적 인터럽트 생성
- PWM 출력
- 이벤트 카운트
- 주파수 분배

특징:
- 복수 채널
- 독립 동작
- 다양한 모드
- 프로그래밍 가능

응용:
- System Timer
- PWM Generator
- Event Counter
- Frequency Divider
```

**8254 PIT 핵심 특징:**

1. **3개 카운터**: 독립적인 16비트 카운터
2. **6가지 모드**: 다양한 동작 모드
3. **Binary/BCD**: 카운트 방식 선택
4. **Counter Latch**: 읽기 동안 카운트 유지

```
8254 vs 단일 타이머:
단일 타이머:
- 1개 카운터
- 단일 모드
- 제한된 기능

8254:
- 3개 카운터
- 6가지 모드
- 다양한 응용
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 8254 내부 구조

```
8254 PIT 구조:

Data Bus[7:0] ──┬──┬──┬────────→ [Control Word] ─┬─ Control Logic
               │  │                          │
               │  └──────────────→ [Counter 0] ─┼─ OUT0
               │                  [Counter 1] ─┼─ OUT1
               └─────────────────[Counter 2] ─┼─ OUT2
                                            │
CS, A0, A1, RD, WR ────────────────────────┘

Counter 구조 (16비트):
Clock ──→ [Clock Enable] ──→ [16-bit Counter] ──→ OUT
           ↑                  ↓
        Gate           Control Logic
                            ↓
                         Data Bus

Control Word:
SC1, SC0: Counter Select (0-2)
RW1, RW0: Read/Write Select
M2, M1, M0: Mode Select
BCD: Binary/BCD
```

### 카운터 선택

```
Counter Selection (CS):

A1 A0 | Counter
-----|--------
 0  0 | Counter 0
 0  1 | Counter 1
 1  0 | Counter 2
 1  1 | Control Word (Read Back)

Control Word Format:
SC1 SC0 RW1 RW0 M2 M1 M0 BCD
 0   0   0   0   0   0   0   0
└─┬─┘ └──┬──┘ └─────┬──┘
   │       │         │
 Counter R/W   Mode  BCD

예:
SC=00: Counter 0
RW=11: Latch then Read/Write
M=011: Mode 3 (Square Wave)
BCD=0: Binary 16-bit
```

### Read/Write Logic

```

Read/Write Mode:

RW1 RW0 | 동작
--------|------
 0   0  | Latch Count (Counter Freeze)
 0   1  | Read/Write LSB only
 1   0  | Read/Write MSB only
 1   1  | Latch then Read/Write LSB, then MSB

LSB/MSB Access:
초기 쓰기:
WR (LSB) → Counter Low Byte
WR (MSB) → Counter High Byte

읽기:
WR (Latch) → Counter Freeze
RD (LSB) → Low Byte
RD (MSB) → High Byte

Latch Command:
SC=11 (Read Back Command)
RW=00 (Latch Count)
```

### 동작 모드

```
Mode 0: Interrupt on Terminal Count

동작:
- Counter가 0이 되면 OUT이 High
- 0에서 유지
- 인터럽트 발생

용도:
- One-shot
- Event counter

타이밍:
      ┌─┐
Clock ┤ ├─┬─┬─┬─┬─
      └─┘ │ │ │ │
Gate  ────┴─┴─┴─┴───
Count  3 2 1 0 0 0
OUT    ────────────┐
                   └─── High

Mode 1: Hardware Retriggerable One-Shot

동작:
- Gate Rising Edge에서 시작
- Counter Down
- 0에서 유지

용도:
- Single Pulse
- Gated Counter

Mode 2: Rate Generator

동작:
- 0에서 Counter Reload
- 주기적 펄스
- N분주

용도:
- Frequency Divider
- Baud Rate Generator

Mode 3: Square Wave Generator

동작:
- 짝수 카운트 시 High
- 홀수 카운트 시 Low
- 50% Duty Cycle

용도:
- System Timer
- Audio Tone
```

### Mode 4 & 5

```
Mode 4: Software Triggered Strobe

동작:
- Software Write로 시작
- Count Down
- 0에서 1 클럭 펄스

용도:
- Strobe Pulse
- Delay

Mode 5: Hardware Triggered Strobe

동작:
- Gate Rising Edge로 시작
- Count Down
- 0에서 1 클럭 펄스

용도:
- Gated Strobe
- External Trigger
```

### Gate 입력

```
Gate (G) 입력:

기능:
- 카운트 Enable/Disable
- Trigger Source

Mode별 동작:
Mode 0: Gate=1 → Count
         Gate=0 → Hold

Mode 1: Gate ↑ → Start (Retrigger)
Mode 2: Gate=1 → Count
         Gate=0 → Reset

Mode 3: Gate=1 → Count
         Gate=0 → Reset

Mode 4: Gate 무시
Mode 5: Gate ↑ → Start

타이밍:
Gate ──┬─────┬─────┬─────┬
      │     │     │     │
Count ─┘     └─┬───┘     └─
              │
           Enabled
```

### Counter Latching

```
Counter Latch:

문제:
- 읽는 동안 값 변화
- 8비트 Bus로 16비트 읽기

해결:
Latch Command로 현재 값 고정

과정:
1. Control Word Write
   SC=11, RW=00
   (Latch specific counter)

2. Counter Freeze
   현재 값이 Latch Register에 저장

3. Read
   LSB → Data Bus
   MSB → Data Bus

4. Unlatch
   다시 Counting 시작

Read Back Command:
SC1 SC0 = Counter Select
D5 D4 D3 D2 D1 D0 = 0 (Latch Count)
```

## Ⅲ. 융합 비교

### 타이머 칩 비교

| 칩 | 카운터 | 비트 | 모드 | 특징 | 응용 |
|------|-------|------|------|------|------|
| 8254 | 3 | 16 | 6 | 표준 | x86 PC |
| 8253 | 3 | 16 | 6 | 구형 | 구형 PC |
| 82C54 | 3 | 16 | 6 | CMOS | 저전력 |
| RTC | 1 | 32 | - | Real-time | 시간 |

### 모드 비교

| 모드 | 이름 | 출력 | Trigger | 응용 |
|------|------|------|---------|------|
| 0 | Interrupt on TC | Level | SW | Event |
| 1 | One-shot | Pulse | HW | Pulse |
| 2 | Rate Gen | Pulse | - | Clock |
| 3 | Square Wave | Square | - | Timer |
| 4 | Strobe | Pulse | SW | Delay |
| 5 | Triggered Strobe | Pulse | HW | Strobe |

### 카운터 크기

| 비트 | 범위 | 주기 @ 1MHz | Resolution |
|------|------|-------------|------------|
| 8 | 0-255 | 256µs | 1µs |
| 16 | 0-65535 | 65.5ms | 1µs |
| 24 | 0-16M | 16.7s | 1µs |
| 32 | 0-4G | ~1hr | 1ns |

## Ⅳ. 실무 적용 및 기술사적 판단

### PC System Timer

```
PC의 8254 활용:

Counter 0: System Timer
- Clock: 1.19318 MHz
- Mode 3 (Square Wave)
- Reload: 65536 (0x0000)
- Frequency: 1.19318MHz / 65536 = 18.2 Hz
- Output: IRQ 0
- 용도: System Tick, Time slicing

Counter 1: RAM Refresh
- Clock: 1.19318 MHz
- Mode 2 (Rate Generator)
- Reload: 18
- Output: DRAM Refresh Request
- Period: 18 / 1.19MHz = 15µs
- 용도: DRAM Refresh (64KB / 2ms)

Counter 2: Speaker
- Clock: 1.19318 MHz
- Mode 3 (Square Wave)
- Reload: Variable
- Output: Speaker
- 용도: Sound Generation
```

### DOS Timer Programming

```
DOS Timer Interrupt:

IRQ 0 Handler:
INT 08h:
- Push All Registers
- Call Timer Tick Handler
- Increment BIOS Data Area Variables
- Call Application Hook (INT 1Ch)
- EOI
- IRET

Timer Variables:
Timer Tick: 0040:006Ch (DWORD)
          18.2 ticks/second
          549ms increment

애플리케이션:
C Language:
- gettime()
- clock()
- time_t 구조체

Assembly:
INT 1Ah: Get System Time
```

### Sound Generation

```

8254로 소리 생성:

Counter 2 Programming:
1. Port 0x43: Control Word
   CW = 0xB6 (Mode 3, LSB/MSB, Binary)

2. Port 0x42: LSB
   Divisor Low = Frequency / Desired

3. Port 0x42: MSB
   Divisor High

주파수 계산:
Divisor = 1193180 / Frequency

예:
440 Hz (A4 Note):
Divisor = 1193180 / 440 = 2711

타이밍:
Divisor = 2711
  0x0A = 10 (Low)
  0xA9 = 169 (High)

Gate 제어:
Port 0x61: Bit 0-1
- Bit 0: Gate 2 (Speaker Enable)
- Bit 1: Timer Data (Speaker Data)
```

### High-Resolution Timer

```

고해상도 타이머:

PC의 제한:
- 18.2 Hz 최대
- 55ms Resolution

해결:
1. TSC (Time Stamp Counter)
   - RDTSC Instruction
   - CPU 클럭 기반
   - 나노초 해상도

2. HPET (High Precision Event Timer)
   - 64비트 Counter
   - 10+ MHz Clock
   - 나노초 해상도

3. ACPI Power Management
   - Fixed TSC
   - invariant TSC
   - C-State awareness
```

## Ⅴ. 기대효과 및 결론

카운터/타이머 칩은 시간 관리의 핵심이다. 8254는 PC 표준으로 30년 이상 사용되었다.

## 📌 관련 개념 맵

```
카운터/타이머 칩
├── 8254 구조
│   ├── 3개 16비트 Counter
│   ├── Control Word
│   ├── Clock/Gate/Out
│   └── Data Bus Interface
├── 동작 모드
│   ├── Mode 0: Interrupt on TC
│   ├── Mode 1: Hardware One-Shot
│   ├── Mode 2: Rate Generator
│   ├── Mode 3: Square Wave
│   ├── Mode 4: Software Strobe
│   └── Mode 5: Hardware Strobe
├── Programming
│   ├── Control Word Write
│   ├── Counter Value Write
│   ├── Counter Latch
│   └── Read Back
└── PC 응용
    ├── Counter 0: System Timer
    ├── Counter 1: RAM Refresh
    └── Counter 2: Speaker
```

## 👶 어린이를 위한 3줄 비유 설명

1. 카운터/타이머 칩은 3개의 알람시계가 하나의 칩에 들어있는 것과 같아요. 각각 다른 목적으로 사용할 수 있어요
2. Counter 0은 시스템 시계, Counter 1은 램 새로고침, Counter 2는 스피커 소리 내는 데 쓰여요
3. 모드는 알람 종류 같아요. Mode 0은 한 번 울리고, Mode 3은 주기적으로 울려서 시계처럼 사용해요

```python
# 8254 PIT 시뮬레이션

from typing import List, Optional
from enum import Enum


class CounterMode(Enum):
    MODE_0 = 0  # Interrupt on Terminal Count
    MODE_1 = 1  # Hardware Retriggerable One-Shot
    MODE_2 = 2  # Rate Generator
    MODE_3 = 3  # Square Wave Generator
    MODE_4 = 4  # Software Triggered Strobe
    MODE_5 = 5  # Hardware Triggered Strobe


class CounterChannel:
    """8254 Counter Channel"""

    def __init__(self, number: int):
        self.number = number
        self.count = 0
        self.reload_value = 0
        self.latched_value = 0
        self.latched = False
        self.output = 0
        self.mode = CounterMode.MODE_0
        self.gate = 1  # Gate Input
        self.bcd = False
        self.read_latched = False
        self.msb_written = False
        self.lsb_written = False
        self.initialized = False

    def write_count(self, data: int, is_msb: bool = False):
        """카운트 값 쓰기"""
        if self.read_latched:
            return  # Latched 상태에서는 쓰기 불가

        if not is_msb:
            # LSB 쓰기
            self.reload_value = (self.reload_value & 0xFF00) | data
            self.lsb_written = True
        else:
            # MSB 쓰기
            if self.lsb_written:
                # LSB/MSB 순서대로 쓰기
                self.reload_value = (self.reload_value & 0x00FF) | (data << 8)
                self.count = self.reload_value
                self.initialized = True
                self.lsb_written = False
            else:
                # MSB만 쓰기
                self.reload_value = (self.reload_value & 0x00FF) | (data << 8)
                self.count = self.reload_value
                self.initialized = True

    def read_count(self, is_msb: bool = False) -> int:
        """카운트 값 읽기"""
        if self.latched:
            value = self.latched_value
            if is_msb:
                self.latched = False
            return (value >> 8) & 0xFF if is_msb else value & 0xFF
        else:
            return (self.count >> 8) & 0xFF if is_msb else self.count & 0xFF

    def latch(self):
        """카운터 래치"""
        self.latched_value = self.count
        self.latched = True

    def clock(self):
        """클럭 입력"""
        if not self.initialized or self.gate == 0:
            return

        if self.mode == CounterMode.MODE_0:
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.output = 1

        elif self.mode == CounterMode.MODE_2:
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.count = self.reload_value
                    self.output ^= 1

        elif self.mode == CounterMode.MODE_3:
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.count = self.reload_value
                    self.output ^= 1

    def trigger(self):
        """Hardware Trigger (Gate Rising Edge)"""
        if self.mode in [CounterMode.MODE_1, CounterMode.MODE_5]:
            self.count = self.reload_value


class PIT8254:
    """8254 PIT 시뮬레이터"""

    def __init__(self):
        self.channels = [CounterChannel(i) for i in range(3)]
        self.control_word = 0
        self.clock_frequency = 1_193_182  # 1.193182 MHz

    def write_control(self, data: int):
        """Control Word 쓰기"""
        self.control_word = data

        sc = (data >> 6) & 0x03
        rw = (data >> 4) & 0x03
        mode = CounterMode((data >> 1) & 0x07)
        bcd = (data & 0x01) != 0

        if sc == 0b11:
            # Read Back Command
            pass  # 간소화
        else:
            channel = self.channels[sc]
            channel.mode = mode
            channel.bcd = bcd

            if rw == 0:
                # Latch Count
                channel.latch()
            elif rw == 1:
                # LSB Only
                channel.lsb_written = True
                channel.msb_written = True
            elif rw == 2:
                # MSB Only
                channel.msb_written = True
            elif rw == 3:
                # LSB then MSB
                pass

    def write_channel(self, channel: int, data: int):
        """채널에 데이터 쓰기"""
        if 0 <= channel < 3:
            ch = self.channels[channel]
            if ch.msb_written and not ch.lsb_written:
                ch.write_count(data, is_msb=True)
            else:
                ch.write_count(data, is_msb=False)

    def read_channel(self, channel: int) -> int:
        """채널 읽기"""
        if 0 <= channel < 3:
            ch = self.channels[channel]
            return ch.read_count()
        return 0

    def tick(self):
        """시스템 클럭 틱"""
        for ch in self.channels:
            ch.clock()

    def gate(self, channel: int, value: int):
        """Gate 입력"""
        if 0 <= channel < 3:
            self.channels[channel].gate = value
            if value == 1:  # Rising Edge
                self.channels[channel].trigger()

    def get_output(self, channel: int) -> int:
        """출력 반환"""
        if 0 <= channel < 3:
            return self.channels[channel].output
        return 0


def demonstration():
    """8254 PIT 데모"""
    print("=" * 60)
    print("8254 PIT (Programmable Interval Timer) 데모")
    print("=" * 60)

    pit = PIT8254()

    # Counter 0: System Timer 설정
    print("\n[Counter 0: System Timer]")
    print("Mode 3 (Square Wave), Reload=65536")

    # Control Word: Counter 0, Mode 3, LSB/MSB, Binary
    pit.write_control(0b00110110)  # 00 11 011 0
    # 0x36: SC=00, RW=11, M=011, BCD=0

    # Reload Value: 65536 (0x0000)
    pit.write_channel(0, 0x00)  # LSB
    pit.write_channel(0, 0x00)  # MSB

    print(f"  Frequency: {pit.clock_frequency} Hz")
    print(f"  Reload: 65536")
    print(f"  Output: {pit.clock_frequency / 65536:.2f} Hz (18.2 Hz)")

    # Counter 1: RAM Refresh 설정
    print("\n[Counter 1: RAM Refresh]")
    print("Mode 2 (Rate Generator), Reload=18")

    # Control Word
    pit.write_control(0b01010100)  # 01 01 010 0
    pit.write_channel(1, 18)  # LSB only

    print(f"  Period: {18 / pit.clock_frequency * 1e9:.1f} µs")

    # Counter 2: Speaker 설정
    print("\n[Counter 2: Speaker]")
    print("Mode 3 (Square Wave), Variable Frequency")

    # Control Word
    pit.write_control(0b10110110)  # 10 11 011 0
    pit.write_channel(2, 0x00)  # LSB
    pit.write_channel(2, 0x10)  # MSB

    freq = pit.clock_frequency / 0x1000
    print(f"  Frequency: {freq:.1f} Hz")

    # 시뮬레이션
    print("\n[시뮬레이션 - Counter 0]")
    pit.channels[0].count = 65535

    for i in range(10):
        pit.tick()
        count = pit.channels[0].count
        output = pit.channels[0].output
        print(f"  Tick {i+1}: Count={count:5d}, Out={output}")

    # Mode 비교
    print("\n[모드 비교]")
    modes = [
        CounterMode.MODE_0,
        CounterMode.MODE_2,
        CounterMode.MODE_3,
    ]

    for mode in modes:
        print(f"\nMode {mode.value}: {mode.name}")
        pit2 = PIT8254()
        ch = pit2.channels[0]
        ch.mode = mode
        ch.reload_value = 5
        ch.count = 5

        print("  Clock  |  Count |  Out")
        print("  -------|--------|-----")
        for i in range(12):
            pit2.tick()
            count = ch.count
            out = ch.output
            print(f"  {i+1:6}  |  {count:6} |  {out:3}")

    # 프로그래밍 예제
    print("\n[8254 프로그래밍]")
    print("Counter 0을 100Hz로 설정:")

    target_freq = 100
    divisor = pit.clock_frequency / target_freq
    print(f"  Divisor = {divisor:.0f} = 0x{int(divisor):04X}")

    lsb = int(divisor) & 0xFF
    msb = (int(divisor) >> 8) & 0xFF
    print(f"  LSB = 0x{lsb:02X}")
    print(f"  MSB = 0x{msb:02X}")

    # Gate 기능
    print("\n[Gate 입력]")
    pit3 = PIT8254()

    pit3.write_control(0b00110010)  # Mode 0
    pit3.write_channel(0, 10)
    pit3.gate(0, 0)  # Disable

    print("Gate=0인 상태에서 clock:")
    for i in range(5):
        pit3.tick()
        print(f"  Clock {i}: Count={pit3.channels[0].count}")

    print("\nGate=1로 Enable:")
    pit3.gate(0, 1)
    for i in range(5):
        pit3.tick()
        print(f"  Clock {i}: Count={pit3.channels[0].count}")


if __name__ == "__main__":
    demonstration()
