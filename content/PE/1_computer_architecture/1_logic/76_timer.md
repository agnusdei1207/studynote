+++
title = "타이머 (Timer)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 타이머 (Timer)

## 핵심 인사이트 (3줄 요약)
1. 타이머(Timer)는 클럭 신호를 카운트하여 시간을 측정하고 일정한 간격으로 인터럽트를 발생시키는 하드웨어로, Counter, Prescaler, Output Compare, Input Capture 기능을 제공한다
2. 카운터는 클럭마다 증가/감소하며 오버플로우/언더플로우 시 인터럽트를 발생시키고, Output Compare는 특정 카운트 값에서 출력을 제어한다
3. 기술사시험에서는 타이머 구조, Prescaler, 카운터 모드, PWM 생성, 실시간 클럭이 핵심이다

## Ⅰ. 개요 (500자 이상)

타이머(Timer)는 **일정한 주기로 동작하거나 특정 시간 간격을 측정하는 하드웨어 카운터**이다. CPU가 시간을 관리하는 소프트웨어 방식과 달리, 하드웨어 타이머는 정확하고 CPU 개입 없이 동작한다.

```
타이머 기본 개념:
구조: Counter + Control Logic
입력: 클럭, 제어 신호
출력: 카운트 값, 인터럽트, PWM

동작:
- 클럭마다 카운트
- 오버플로우 시 인터럽트
- 주기적 이벤트 생성

특징:
- CPU 독립적 동작
- 정확한 시간 측정
- 주기적 인터럽트
- PWM 출력 가능
```

**타이머의 핵심 특징:**

1. **독립성**: CPU와 독립적으로 카운트
2. **정확성**: 클럭 기반 정확한 시간
3. **자동**: 인터럽트 자동 발생
4. **다목적**: 시간 측정, PWM, 이벤트

```
소프트웨어 vs 하드웨어 타이머:
소프트웨어:
- CPU가 카운트
- 비효율적
- 부정확

하드웨어:
- 전용 카운터
- 효율적
- 정확
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 타이머 기본 구조

```
타이머 구조:

Clk ──┬──[Prescaler]──┬──[Counter]──┬──→ Count Value
     │               │             │
     │            Control         ↓
     └───────────────┴─────────→ Interrupt

구성 요소:
1. Clock Source:
   - System Clock
   - External Clock

2. Prescaler:
   - 클럭 분주
   - 1:1, 1:8, 1:64 등

3. Counter:
   - 8/16/32비트
   - Up/Down Count

4. Control Logic:
   - Start/Stop
   - Mode Selection

5. Compare/Capture:
   - Output Compare
   - Input Capture
```

### 카운터 동작

```
카운터 타이밍:

Up Counting Mode:
Clk ─┬──┬──┬──┬──┬──┬──┬──
     ↑  ↑  ↑  ↑  ↑  ↑  ↑
     │  │  │  │  │  │  │
Cnt ─┴──┴──┴──┴──┴──┴──┴──
    0  1  2  3 ... 255 → 0 (Overflow)

Down Counting Mode:
Clk ─┬──┬──┬──┬──┬──┬──┬──
     ↑  ↑  ↑  ↑  ↑  ↑  ↑
     │  │  │  │  │  │  │
Cnt ─┴──┴──┴──┴──┴──┴──┴──
  255 254 253 ... 0 → 255 (Underflow)

주기:
Period = (Max+1) × Prescaler × Clock Period
       = 256 × Prescaler / Freq
```

### Prescaler

```
프리스케일러:

목적: 클럭 속도 감소

구조:
Input Clock ──┬──[Counter]──┬── Scaled Clock
              │           │
           Prescale     MUX
           Value        Select

예 (8-bit Prescaler):
Prescaler = 8
Input: 1MHz
Output: 125kHz (1MHz / 8)

타이밍:
Timer Clock = System Clock / Prescaler
Resolution = Prescaler / System Clock

설정:
Prescaler = 1:  최고 해상도
Prescaler = 256: 긴 주기
```

### Output Compare

```
Output Compare:

개념:
특정 카운트 값에서 출력 변화

구조:
Compare Register ─┬──[Comparator]──┬── Output
                    │             │
               Counter Value   Match

동작:
1. Compare Value 설정
2. Counter가 증가
3. Counter == Compare → Match
4. Output 변화 (Toggle/Set/Clear)

예:
Compare = 100
Count: 0 → 100 (Match!) → Output High
Count: 100 → 200 (Match!) → Output Low

결과: PWM 생성 가능
```

### Input Capture

```
Input Capture:

개념:
외부 이벤트 시점을 카운트 값으로 저장

구조:
External Pin ───┬──[Edge Detector]──┬── Capture Register
                  │               │
               Counter           Store

동작:
1. Pin에 Edge 발생 (Rising/Falling)
2. 현재 Counter 값을 Capture Register에 저장
3. 인터럽트 발생
4. CPU가 Capture 값 읽기

응용:
- 펄스 폭 측정
- 주파수 측정
- 속도계
- 엔코더
```

### PWM (Pulse Width Modulation)

```
PWM 생성:

개념:
일정한 Duty Cycle의 파형 생성

구조:
2개 Output Compare:
- OCR1: Rising Edge
- OCR2: Falling Edge

타이밍:
Period = OCR2 - OCR1
Duty = (OCR2 - OCR1) / Max

예 (10kHz PWM, 50% Duty):
Clock = 1MHz
Prescaler = 1
Max = 100
Period = 100 clocks = 100µs (10kHz)
OCR1 = 0, OCR2 = 50

Duty = 50/100 = 50%

파형:
      ┌───────┐
      │       │
─────┘       └─────
 0    50    100
```

### RTC (Real-Time Clock)

```
실시간 클럭:

구조:
32.768 kHz Crystal ─→ Divider → 1 Hz → Seconds Counter
                                              ↓
                                         Minutes Counter
                                              ↓
                                         Hours Counter

특징:
- 배터리 백업
- 낮은 전력
- 정확한 시간

레지스터:
Seconds: 0-59
Minutes: 0-59
Hours: 0-23
Days: 1-31
Months: 1-12
Years: 2000-2099

액세스:
CPU가 레지스터 읽기/쓰기
```

## Ⅲ. 융합 비교

### 타이머 타입

| 타입 | 비트 | 모드 | 특징 | 응용 |
|------|------|------|------|------|
| 8-bit Timer | 8 | Up/Down | 단순 | 작은 주기 |
| 16-bit Timer | 16 | Up/Down/PWM | 범용 | 일반 |
| 32-bit Timer | 32 | Complex | 정밀 | 정밀 제어 |
| RTC | 32 | Real-time | 시간 | 시스템 시간 |

### 카운터 모드

| 모드 | 동작 | 오버플로우 | 응용 |
|------|------|-----------|------|
| Up Count | 증가 | Max→0 | 일반 |
| Down Count | 감소 | 0→Max | Count Down |
| Toggle |翻转 | 교차 | PWM |
| PWM | 가변 Duty | - | 모터 제어 |

### Prescaler 설정

| 설정 | 분주비 | 해상도 | 최대 주기 |
|------|--------|--------|----------|
| 1:1 | 1 | 높음 | 짧음 |
| 1:8 | 8 | 중간 | 중간 |
| 1:64 | 64 | 낮음 | 김 |

## Ⅳ. 실무 적용 및 기술사적 판단

### Intel 8254 PIT

```
8254 Programmable Interval Timer:

구조:
- 3개 Independent Counter
- 16비트 each
- 6가지 동작 모드

Mode 0: Interrupt on Terminal Count
Mode 1: Hardware Retriggerable One-Shot
Mode 2: Rate Generator
Mode 3: Square Wave Generator
Mode 4: Software Triggered Strobe
Mode 5: Hardware Triggered Strobe

PC 사용:
Counter 0: System Timer (IRQ 0)
  - 18.2 Hz (1.19MHz / 65536)
  - System Tick

Counter 1: RAM Refresh
  - 15.6 µs (DRAM Refresh)

Counter 2: Speaker
  - Beeper Sound
```

### ARM Cortex-M SysTick

```
SysTick Timer:

구조:
- 24비트 Down Counter
- System Clock 기반
- Auto-Reload

레지스터:
CTRL: Enable, TickInt, ClkSource
LOAD: Reload Value
VAL: Current Value

주기:
Period = (LOAD + 1) / Clock

RTOS Tick 설정:
Clock = 72MHz
Desired Tick = 1ms (1kHz)
LOAD = 72000 - 1

응용:
- RTOS Kernel Tick
- Delay 함수
- Scheduler
```

### Watchdog Timer

```

워치독 타이머:

목적:
시스템 Hang 감지 및 Reset

구조:
Counter ─→ 0 → Reset
    ↑
   Kick (Software)

동작:
1. 초기화 후 Count Down
2. Software가 주기적으로 Kick (재설정)
3. Software가 Hang → Count 0
4. System Reset

Kick (Feed):
주기적으로 WDT Register 쓰기
ARM: IWDG_KR = 0xAAAA

주기:
Timeout = (Count + 1) / WDT_Clock

설정:
- 1초 ~ 10초
- Application에 따라
```

### PWM Motor Control

```
PWM 모터 제어:

Speed Control:
Duty Cycle → 속도

예 (DC Motor):
Duty 0% → 정지
Duty 25% → 저속
Duty 50% → 중속
Duty 75% → 고속
Duty 100% → 최고속

Frequency:
- 1kHz ~ 20kHz
- 너무 낮음: 진동
- 너무 높음: Switching Loss

Servo Motor:
50Hz 고정
Duty 5% → -90°
Duty 7.5% → 0°
Duty 10% → +90°
```

## Ⅴ. 기대효과 및 결론

타이머는 시간의 기준이다. 정확한 시간 측정과 주기적 이벤트를 제공한다.

## 📌 관련 개념 맵

```
타이머 (Timer)
├── 구조
│   ├── Counter (카운터)
│   ├── Prescaler (분주기)
│   ├── Control (제어)
│   └── Interrupt (인터럽트)
├── 모드
│   ├── Up Count
│   ├── Down Count
│   ├── PWM
│   └── Capture
├── 기능
│   ├── 시간 측정
│   ├── PWM 출력
│   ├── Input Capture
│   └── Periodic Interrupt
└── 응용
    ├── System Tick
    ├── PWM Motor
    ├── RTC
    └── Watchdog
```

## 👶 어린이를 위한 3줄 비유 설명

1. 타이머는 초시계 같아요. 일정한 간격으로 카운트하면서 시간을 재고, 정해진 시간이 되면 알람(인터럽트)을 울려요
2. PWM은 스위치를 빠르게 켜고 끄는 것 같아요. 켜는 시간을 조절하면 전구의 밝기나 모터의 속도를 조절할 수 있어요
3. Prescaler는 속도 조절 같아요. 클럭을 나누면 카운터가 천천히 올라가서 더 긴 시간을 측정할 수 있어요

```python
# 타이머 시뮬레이션

from typing import Callable, Optional
from enum import Enum


class TimerMode(Enum):
    UP = "Up Count"
    DOWN = "Down Count"
    PWM = "PWM"


class Timer:
    """타이머 시뮬레이션"""

    def __init__(self, bits: int = 16, prescaler: int = 1):
        self.bits = bits
        self.max_value = (1 << bits) - 1
        self.prescaler = prescaler
        self.counter = 0
        self.running = False
        self.mode = TimerMode.UP
        self.reload_value = 0
        self.overflow_count = 0
        self.on_overflow: Optional[Callable] = None
        self.prescaler_counter = 0

    def start(self):
        """타이머 시작"""
        self.running = True

    def stop(self):
        """타이머 정지"""
        self.running = False

    def reset(self):
        """타이머 리셋"""
        self.counter = 0
        self.prescaler_counter = 0
        self.overflow_count = 0

    def set_reload(self, value: int):
        """리로드 값 설정"""
        self.reload_value = value & self.max_value

    def set_mode(self, mode: TimerMode):
        """모드 설정"""
        self.mode = mode

    def clock(self):
        """클럭 입력"""
        if not self.running:
            return

        # Prescaler 처리
        self.prescaler_counter += 1
        if self.prescaler_counter < self.prescaler:
            return
        self.prescaler_counter = 0

        # 카운터
        if self.mode == TimerMode.UP:
            self.counter += 1
            if self.counter > self.max_value:
                self.counter = 0
                self.overflow_count += 1
                if self.on_overflow:
                    self.on_overflow()

        elif self.mode == TimerMode.DOWN:
            if self.counter == 0:
                self.counter = self.reload_value
                self.overflow_count += 1
                if self.on_overflow:
                    self.on_overflow()
            else:
                self.counter -= 1

    def get_count(self) -> int:
        """카운트 값 반환"""
        return self.counter

    def get_overflow(self) -> int:
        """오버플로우 횟수 반환"""
        return self.overflow_count


class PWMOutput:
    """PWM 출력"""

    def __init__(self, timer: Timer):
        self.timer = timer
        self.duty_cycle = 0.5  # 50%
        self.frequency = 1000  # 1kHz
        self.output = False

    def set_duty_cycle(self, duty: float):
        """Duty Cycle 설정 (0.0 ~ 1.0)"""
        self.duty_cycle = max(0.0, min(1.0, duty))

    def set_frequency(self, freq: int):
        """주파수 설정"""
        self.frequency = freq

    def update(self):
        """PWM 출력 업데이트"""
        # 간단한 PWM 구현
        count = self.timer.get_count()
        max_val = self.timer.max_value
        threshold = int(max_val * self.duty_cycle)

        self.output = count < threshold

    def get_output(self) -> bool:
        """출력 상태 반환"""
        return self.output


class InputCapture:
    """Input Capture"""

    def __init__(self, timer: Timer):
        self.timer = timer
        self.captured_value = 0
        self.edge_count = 0
        self.last_period = 0
        self.last_capture = 0

    def capture(self, edge: str):
        """입력 캡처"""
        self.captured_value = self.timer.get_count()
        self.edge_count += 1

        # 주기 계산
        if self.last_capture > 0:
            self.last_period = self.captured_value - self.last_capture

        self.last_capture = self.captured_value

    def get_captured(self) -> int:
        """캡처된 값 반환"""
        return self.captured_value

    def get_period(self) -> int:
        """주기 반환"""
        return self.last_period


class RealTimeClock:
    """실시간 클럭"""

    def __init__(self):
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.days = 1
        self.months = 1
        self.years = 2000

    def tick(self):
        """1초 진행"""
        self.seconds += 1

        if self.seconds >= 60:
            self.seconds = 0
            self.minutes += 1

            if self.minutes >= 60:
                self.minutes = 0
                self.hours += 1

                if self.hours >= 24:
                    self.hours = 0
                    self.days += 1

                    # 간단한 날짜 계산
                    days_in_month = 30
                    if self.days > days_in_month:
                        self.days = 1
                        self.months += 1

                        if self.months > 12:
                            self.months = 1
                            self.years += 1

    def set_time(self, hours: int, minutes: int, seconds: int):
        """시간 설정"""
        self.hours = hours % 24
        self.minutes = minutes % 60
        self.seconds = seconds % 60

    def get_time(self) -> tuple:
        """시간 반환"""
        return (self.hours, self.minutes, self.seconds)

    def __str__(self):
        return f"{self.years:04d}-{self.months:02d}-{self.days:02d} " \
               f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"


def demonstration():
    """타이머 데모"""
    print("=" * 60)
    print("타이머 (Timer) 데모")
    print("=" * 60)

    # 기본 타이머
    print("\n[기본 타이머]")
    timer = Timer(bits=8, prescaler=1)

    def overflow_handler():
        print(f"  Overflow! Count = {timer.get_count()}")

    timer.on_overflow = overflow_handler
    timer.set_reload(100)

    timer.start()

    print("Up Counting Mode:")
    for i in range(20):
        timer.clock()
        if i % 5 == 0:
            print(f"  Clock {i}: Count = {timer.get_count()}")

    # PWM
    print("\n[PWM Output]")
    pwm_timer = Timer(bits=8, prescaler=1)
    pwm = PWMOutput(pwm_timer)

    pwm_timer.start()

    # PWM Duty Cycle 변경
    duties = [0.0, 0.25, 0.5, 0.75, 1.0]

    for duty in duties:
        print(f"\nDuty Cycle: {duty*100:.0f}%")

        pwm.set_duty_cycle(duty)

        # 1주기 시뮬레이션
        outputs = []
        for _ in range(16):
            pwm_timer.clock()
            pwm.update()
            outputs.append("█" if pwm.get_output() else " ")

        print("  " + "".join(outputs))

    # Input Capture
    print("\n[Input Capture]")
    capture_timer = Timer(bits=16, prescaler=1)
    capture = InputCapture(capture_timer)

    capture_timer.start()

    # Edge 입력 시뮬레이션
    edges = [10, 30, 50, 90]  # Edge 발생 시점

    print("Edge Capture:")
    for edge_time in edges:
        # 카운터를 Edge 시점으로 설정
        while capture_timer.get_count() < edge_time:
            capture_timer.clock()

        capture.capture("Rising")
        print(f"  Edge at {edge_time}: Captured = {capture.get_captured()}")
        print(f"  Period = {capture.get_period()}")

    # RTC
    print("\n[실시간 클럭 (RTC)]")
    rtc = RealTimeClock()

    rtc.set_time(12, 30, 0)
    print(f"Initial: {rtc}")

    print("\nForward 10 seconds:")
    for _ in range(10):
        rtc.tick()
    print(f"After 10s: {rtc}")

    # System Tick
    print("\n[System Tick Timer]")
    sys_tick = Timer(bits=24, prescaler=72000)  # 72MHz / 72000 = 1kHz

    tick_count = 0

    def tick_handler():
        nonlocal tick_count
        tick_count += 1
        if tick_count % 100 == 0:
            print(f"  100ms elapsed (Ticks: {tick_count})")

    sys_tick.on_overflow = tick_handler
    sys_tick.set_reload(0)  # Max value
    sys_tick.start()

    print("RTOS Tick Simulation:")
    for _ in range(20000):
        sys_tick.clock()
        if tick_count >= 100:
            break

    # Watchdog Timer
    print("\n[Watchdog Timer]")
    wdt = Timer(bits=8, prescaler=1)

    wdt.set_reload(100)  # 100 clocks timeout
    wdt.start()

    # Normal operation (Kick in time)
    print("Normal Operation:")
    for i in range(3):
        wdt.clock()
        # Kick (재설정)
        wdt.counter = 50
        print(f"  Cycle {i}: Kick, Count = {wdt.get_count()}")

    # Hung operation (no Kick)
    print("\nHung Operation:")
    for i in range(110):
        wdt.clock()
        if wdt.get_count() == 0:
            print(f"  Cycle {i}: Watchdog Timeout! System Reset")
            break

    # Prescaler 효과
    print("\n[Prescaler 효과]")
    print("Clock = 1MHz")

    for presc in [1, 8, 64]:
        timer_p = Timer(bits=16, prescaler=presc)
        timer_p.set_reload(65535)

        # 최대 주기 계산
        max_period = (timer_p.max_value + 1) * presc / 1e6
        freq = 1.0 / max_period if max_period > 0 else 0

        print(f"  Prescaler {presc}:")
        print(f"    Max Period: {max_period*1000:.2f} ms")
        print(f"    Frequency: {freq:.2f} Hz")


if __name__ == "__main__":
    demonstration()
