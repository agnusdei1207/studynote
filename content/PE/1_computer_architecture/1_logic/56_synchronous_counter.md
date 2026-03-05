+++
title = "동기식 카운터 (Synchronous Counter)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# 동기식 카운터 (Synchronous Counter)

## 핵심 인사이트 (3줄 요약)
1. 동기식 카운터는 모든 플립플롭이 공통 클럭에 동기화되어 병렬로 상태를 전이시키는 카운터로, 리플(비동기) 카운터의 전파 지연 문제를 해결하여 고속 동작이 가능하다
2. 각 플립플롭의 J, K 입력이 이전 단계의 출력을 조합 논리로 계산되어 모든 FF가 동시에 상태를 변화시키며, Parallel Carry 방식으로 최대 1 클럭 지연을 달성한다
3. 기술사시험에서는 동기식 카운터의 구조, Carry Look-Ahead, 리플 카운터와의 비교, 최대 클럭 주파수 계산이 핵심이다

## Ⅰ. 개요 (500자 이사)

동기식 카운터(Synchronous Counter)는 **모든 플립플롭이 공통 클럭에 동기화되어 병렬로 상태를 전이**하는 순차 회로이다. 비동기식(리플) 카운터가 플립플롭의 출력을 다음 플립플립플롭의 클럭으로 사용하여 직렬로 전파되는 반면, 동기식 카운터는 모든 FF가 동일한 클럭에 동기화되어 병렬로 동작한다.

```
동기식 vs 비동기식 카운터:

비동기식 (리플):
FF0: Clk = Fin
FF1: Clk = Q0
FF2: Clk = Q1
FF3: Clk = Q2
지연: Q0 → Q1 → Q2 → Q3 (직렬 전파)

동기식:
FF0, FF1, FF2, FF3: Clk = Fin (공통)
J, K = 이전 단계 조합 논리
지연: 1 클럭 (병렬)
```

**동기식 카운터의 핵심 특징:**

1. **병렬 동작**: 모든 FF가 동일 클럭에 동기화
2. **빠른 속도**: 1 클럭에 모든 비트 동시 전이
3. **예측 가능한 타이밍**: 지연 시간 일정
4. **합성 용이**: FPGA/ASIC으로 자동 합성 가능

```
리플 카운터 문제점:
- 전파 지연: n × t_pd
- 최악 케이스: 모든 비트가 전이 (111→000)
- 최대 클럭: 1 / (n × t_pd)

동기식 카운터 해결:
- 병렬 Carry
- 1 클럭에 모든 비트 전이
- 최대 클럭: 1 / (t_setup + t_pd)
```

동기식 카운터는 고성능 CPU, DSP, 통신 시스템 등 널리 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 4비트 동기식 카운터

```
4비트 동기식 카운터 구조:

Clk ───┬── T/JK FF 0 ── Q0
        ├── T/JK FF 1 ── Q1
        ├── T/JK FF 2 ── Q2
        └── T/JK FF 3 ── Q3

입력 논리 (JK FF, J=K=Toggle):
FF0: J0=K0=1 (항상 토글)
FF1: J1=K1=Q0
FF2: J2=K2=Q0·Q1
FF3: J3=K3=Q0·Q1·Q2

모든 FF: 공통 Clk
```

### 진리표

```
4비트 동기식 카운터 진리표:

| Clk | Q3 Q2 Q1 Q0 | Q3' Q2' Q1' Q0' | J3 K3 | J2 K2 | J1 K1 | J0 K0 | 다음 상태 |
|-----|------------|---------------|-------|-------|-------|-------|----------|
| ↑   | 0  0   0  0 | 1    1    1    1 | 0 0 | 0 0 | 0 0 | 1 1 | 0  0  0  1 |
| ↑   | 0  0  0  1 | 1    1    1    0 | 0 0 | 0 1 | 1 0 | 0 0  0  1 0 |
| ↑   | 0  0  0  1 | 1    1    1    0 | 0 0 | 1 1 | 1 0 | 0 0  0 1 1 |
| ↑   | 0  0   1  1 | 1    1    0    0 | 0 1 | 1 1 | 1 1 | 0  0  1  0 0 |
| ↑   | 0  0  1  0 | 1    1    0    1 | 0 1 | 1 1 | 0 1 | 0 0  1  0 1 |
... 16 카운트까지 반복
```

### Carry Chain

```
동기식 Carry 체인:

Q0 Q1 Q2 Q3
 │  │  │  │
 └──┴──┴──┴──→ Carry Logic

Carry Logic:
C1 = Q0 (FF1의 캐리/입력)
C2 = Q0·Q1 (FF2의 캐리)
C3 = Q0·Q1·Q2 (FF3의 캐리)

지연:
- Carry 생성: 2-3 게이트 (AND 게이트 체인)
- FF 동작: 1 클럭
- 총: 1 클럭 + Carry Logic 지연
```

### 전파 지연 분석

```
동기식 카운터 지연:

한 클럭 사이클:
1. Carry Logic 계산: 2-3 게이트
2. Setup: J, K 안정화
3. 클럭 상승 에지
4. FF 상태 전이: 1 클럭

총 지연:
t_total = t_carry_logic + t_setup + t_ff
        = 2-3 게이트 + 1 게이트
        = 3-4 게이트

@ 100ps/게이트:
t_total = 300-400ps
f_max = 2.5-3.3 GHz

리플 비교:
- 리플: 4 × 500ps = 2ns (최악)
- 동기식: 400ps (일정)
```

### Up/Down 카운터

```
동기식 Up/Down 카운터:

Up/Down ──┬── T/JK FF 0 ── Q0
          ├── T/JK FF 1 ── Q1
          └── T/JK FF 2 ── Q2

Up=1, Down=0:
- 카운트 증가 (0 → 1 → 2 → ...)

Up=0, Down=1:
- 카운트 감소 (n → n-1 → n-2 → ...)

입력 논리:
Up=1, Down=0:
  J0=K0=1
  J1=K1=Q0 (증가)
  J2=K2=Q0·Q1

Up=0, Down=1:
  J0=K0=1
  J1=K1=~Q0 (감소)
  J2=K2=Q0·Q1 또는 다른 논리
```

## Ⅲ. 융합 비교

### 동기식 vs 비동기식 카운터

| 비교 항목 | 비동기식 (리플) | 동기식 |
|----------|------------------|--------|
| 클럭 | 직렬 연결 | 공통 |
| 지연 | O(n) × t_pd | O(1) |
| 최악 지연 | n × t_pd | t_carry + t_ff |
| 속도 | 느림 | 빠름 |
| 합성 | 간단 | 복잡 |
| 면적 | 작음 | 큼 |
| 응용 | 저속 | 고속 |

### Carry 방식 비교

| 방식 | 구조 | 지연 | 복잡도 | 응용 |
|------|------|------|--------|------|
| Ripple Carry | 직렬 | O(n) | 단순 | 소형 |
| Carry Look-Ahead | 병렬 | O(log n) | 복잡 | 고성능 |
| Carry Select | 선택 | O(√n) | 중간 | 중간 |
| Carry Save | 분리 | O(1) | 복잡 | 고성능 |

### 카운터 구현 비교

| 타입 | FF | 클럭 | 속도 | 용도 |
|------|----|----|------|------|
| 리플 카운터 | T/JK FF | 독립 | 느림 | 간단 |
| 동기식 카운터 | T/JK FF + Logic | 공통 | 빠름 | 일반 |
| BCD 카운터 | JK FF + BCD Logic | 공통 | 중간 | 디스플레이 |
| 링 카운터 | FF + 반환 | 공통 | 빠름 | 특수 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 8비트 동기식 카운터

```
8비트 Parallel Carry 카운터:

Clk ──┬── FF 0 ── Q0
       ├── FF 1 ── Q1
       ├── ...
       └── FF 7 ── Q7

Carry Logic:
C1 = Q0
C2 = Q0·Q1
C3 = Q0·Q1·Q2
...
C7 = Q0·Q1·...·Q6

구현:
- 2입력 AND 게이트 21개
- OR 게이트 7개
- 각 FF: JK FF (J=K=toggle 또는 입력)

지연:
- Carry Logic: 3-4 게이트 (최악 캐리)
- FF Setup: 1 게이트
- 총: 4-5 게이트
@ 100ps: 400-500ps
f_max: 2-2.5 GHz
```

### 모듈형 카운터

```
4비트 모듈 카운터 (Load, Clear, Enable):

Control Inputs:
- Load: 병렬 로드
- Clear: 동기 리셋
- Enable: 카운트 활성화

Load=1: P[3:0] → Q[3:0]
Clear=1: Q[3:0] ← 0

구조:
P3 P2 P1 P0
│  │  │  │
├──┴──┴──┴──┴──→ MUX ── J, K
     │          │
   Clk ─────────┴── FF
     │
   Enable, Clear

특징:
- 병렬 데이터 로드 가능
- 리셋 기능
- Enable로 카운트 제어
```

### BCD 카운터

```
BCD (Binary Coded Decimal) 카운터:

10진수 0-9 카운트:
0000 → 0001 → ... → 1001 → 0000

각 자릿수마다 카운터:
개별 자림수: 4비트 (0-9)
10진 자릿수: 4개 × 4비트 = 16비트

동기식 BCD 카운터:
- 각 자릿수 독립 카운터
- Carry Logic: 9 → 다음 자릿수로 Carry
- 6개 FF + Decoder

BCD → 7세그먼트 디코딩:
- BCD 값을 7세그먼트로 변환
- 디스플레이 구동
```

## Ⅴ. 기대효과 및 결론

동기식 카운터는 고속 카운팅의 표준이다. 1 클럭에 모든 비트가 전이한다.

## 📌 관련 개념 맵

```
동기식 카운터
├── 구조
│   ├── 공통 클럭
│   ├── 조합 논리 (Carry)
│   └── 플립플롭 배열
├── Carry 방식
│   ├── Ripple Carry
│   ├── Carry Look-Ahead
│   ├── Carry Select
│   └── Carry Save
├── 기능
│   ├── Up Counter
│   ├── Down Counter
│   └── Up/Down Counter
└── 응용
    ├── CPU PC (Program Counter)
    ├── 타이머/카운터
    └── 주파수 분배기
```

## 👶 어린이를 위한 3줄 비유 설명

1. 동기식 카운터는 모든 사람이 동시에 "하나!" 하고 카운트를 올리는 것과 같아요. 각 자리를 담당하는 사람이 동시에 숫자를 올려서 1 클럭에 모든 자리가 동시에 변해요
2. 비동기식은 앞사람이 세면 뒷사람이 세는 방식이라 지연이 생기는데, 동기식은 모두 동시에 카운트해서 빠르고 정확해요
3. 컴퓨터의 프로그램 카운터(PC)는 동기식 카운터로 만들어져 있어서, 클럭마다 명령어 주소를 동시에 계산해요

```python
# 동기식 카운터 시뮬레이션

from typing import List


class SynchronousCounter:
    """동기식 카운터 시뮬레이션"""

    def __init__(self, bits: int):
        """
        n비트 동기식 카운터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.count = 0

    def clock(self, enable: int = 1, clear: int = 0) -> int:
        """
        클럭에 따른 카운트

        Args:
            enable: 카운트 활성화 (1=증가, 0=유지)
            clear: 리셋 (1=리셋)

        Returns:
            현재 카운트 값
        """
        if clear:
            self.count = 0
        elif enable:
            max_count = (1 << self.bits) - 1
            self.count = (self.count + 1) & max_count

        return self.count

    def get_count(self) -> int:
        """현재 카운트 값 반환"""
        return self.count

    def load(self, data: int):
        """
        병렬 로드

        Args:
            data: 로드할 값
        """
        max_value = (1 << self.bits) - 1
        self.count = data & max_value


class UpDownCounter:
    """Up/Down 동기식 카운터"""

    def __init__(self, bits: int):
        """
        n비트 Up/Down 카운터

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.count = 0

    def clock(self, up: int, down: int, enable: int = 1) -> int:
        """
        클럭에 따른 카운트

        Args:
            up: 증가 (1=증가)
            down: 감소 (1=감소)
            enable: 활성화

        Returns:
            현재 카운트 값
        """
        if not enable:
            return self.count

        max_count = (1 << self.bits) - 1

        if up and not down:
            self.count = (self.count + 1) & max_count
        elif down and not up:
            self.count = (self.count - 1) & max_count
        # 둘 다 0이면 유지
        # 둘 다 1이면 Wrap-around

        return self.count

    def get_count(self) -> int:
        """현재 카운트 값 반환"""
        return self.count


class BCDCounter:
    """BCD 카운터"""

    def __init__(self, digits: int = 2):
        """
        n자릿수 BCD 카운터

        Args:
            digits: 자릿수
        """
        self.digits = digits
        self.counters = [SynchronousCounter(4) for _ in range(digits)]

    def clock(self, enable: int = 1, clear: int = 0) -> int:
        """
        클럭에 따른 카운트

        Args:
            enable: 활성화
            clear: 리셋

        Returns:
            BCD 값 (정수)
        """
        if clear:
            for counter in self.counters:
                counter.clear()
            return 0

        if not enable:
            return self.get_bcd_value()

        # 첫 번째 자릿수 카운트
        carry = 1
        for i, counter in enumerate(self.counters):
            if carry:
                counter.clock(1, 0)
                digit = counter.get_count()
                carry = (digit == 0 and i < self.digits - 1)
            else:
                break

        return self.get_bcd_value()

    def get_bcd_value(self) -> int:
        """BCD 값을 정수로 반환"""
        value = 0
        for i, counter in enumerate(self.counters):
            digit = counter.get_count()
            value += digit * (10 ** i)
        return value

    def load(self, bcd_value: int):
        """BCD 값 로드"""
        for i in range(self.digits):
            digit = (bcd_value // (10 ** i)) % 10
            self.counters[i].load(digit)


class FrequencyDivider:
    """주파수 분배기 (동기식)"""

    def __init__(self, division_ratio: int):
        """
        주파수 분배기

        Args:
            division_ratio: 분주비 (예: 10 = ÷10)
        """
        self.division_ratio = division_ratio
        self.counter = 0
        self.output = 0

    def clock(self, clk: int) -> int:
        """
        클럭에 따른 분주

        Args:
            clk: 입력 클럭

        Returns:
            현재 출력 값
        """
        if clk:
            self.counter = (self.counter + 1) % self.division_ratio
            self.output = 1 if self.counter == 0 else 0

        return self.output


def demonstration():
    """동기식 카운터 데모"""
    print("="*60)
    print("동기식 카운터 (Synchronous Counter) 데모")
    print("="*60)

    # 4비트 동기식 카운터
    print("\n[4비트 동기식 카운터]")
    sync_counter = SynchronousCounter(bits=4)

    print("0부터 20까지 카운트:")
    for i in range(21):
        count = sync_counter.clock(1)
        print(f"{i:2d}: 0b{count:04b} ({count:3d})")

    # Up/Down 카운터
    print(f"\n[4비트 Up/Down 카운터]")
    updown_counter = UpDownCounter(bits=4)

    # 0→10→5→15→0
    sequence = [
        (1, 0, 1, "Up"),
        (1, 0, 1, "Up"),
        (1, 0, 1, "Up"),
        (0, 1, 1, "Down"),
        (0, 1, 1, "Down"),
        (1, 0, 1, "Up"),
    ]

    for up, down, enable, desc in sequence:
        count = updown_counter.clock(up, down, enable)
        print(f"{desc}: {count:2d} (0b{count:04b})")

    # BCD 카운터
    print(f"\n[2자릿수 BCD 카운터]")
    bcd_counter = BCDCounter(digits=2)

    print("0부터 50까지 카운트:")
    for i in range(51):
        bcd = bcd_counter.clock(1)
        print(f"{i:2d}: {bcd:02d} (BCD)")

    # 주파수 분배기
    print(f"\n[주파수 분배기 (÷10)]")
    freq_div = FrequencyDivider(division_ratio=10)

    print("입력 클럭 20개:")
    outputs = []
    for i in range(20):
        output = freq_div.clock(1)
        outputs.append(output)
        print(f"  {i}: Clk=1 → Out={output}")

    pulse_count = sum(outputs)
    print(f"\n출력 펄스 수: {pulse_count} (이론: 2)")

    # 성능 비교
    print(f"\n[성능 비교: 리플 vs 동기식]")
    print(f"4비트 카운터:")
    print(f"  리플: 최악 지연 = 4 × 500ps = 2ns (500MHz)")
    print(f"  동기식: 지연 = 500ps (2GHz)")
    print(f"  속도 향상: 4x")


if __name__ == "__main__":
    demonstration()
```
