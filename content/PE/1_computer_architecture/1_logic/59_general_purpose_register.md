+++
title = "범용 레지스터 (General Purpose Register)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "순차회로"]
draft = false
+++

# 범용 레지스터 (General Purpose Register)

## 핵심 인사이트 (3줄 요약)
1. 범용 레지스터(GPR)는 CPU 내에서 데이터를 임시 저장하는 D 플립플롭 기반의 순차 회로로, 읽기/쓰기 제어와 병렬 데이터 입출력이 특징이다
2. n비트 레지스터는 n개의 D FF를 병렬로 연결하여 구현하며, Enable, Clock, Reset 등의 제어 신호로 동작을 제어한다
3. 기술사시험에서는 레지스터 구조, 읽기/쓰기 타이밍, 레지스터 파일 구성이 핵심이다

## Ⅰ. 개요 (500자 이상)

범용 레지스터(General Purpose Register, GPR)는 **CPU 내에서 데이터를 임시로 저장하고 가공하는 순차 논리 회로**이다. D 플립플롭을 병렬로 연결하여 n비트 데이터를 저장할 수 있으며, 클럭의 상승/하강 에지에서 데이터를 캡처한다.

```
범용 레지스터 기본 개념:
구조: n개 D FF 병렬 연결
입력: Data[n-1:0], Write Enable, Clk, Reset
출력: Q[n-1:0]

동작:
- Write=1, Clk↑: D → Q (데이터 저장)
- Write=0: 상태 유지
- Reset=1: Q ← 0 (또는 초기값)

특징:
- 병렬 입출력
- 빠른 액세스 (1 클럭)
- 에지 트리거
- 삼상 출력 (버스 연결)
```

**범용 레지스터의 핵심 특징:**

1. **병렬 저장**: n비트를 동시에 저장
2. **에지 트리거**: 클럭 에지에서만 상태 변경
3. **빠른 액세스**: 1 클럭 사이클 내 읽기/쓰기
4. **버스 연결**: 삼상 출력으로 공유 버스 연결

```
레지스터 vs 메모리:
레지스터:
- 1 클럭 액세스
- CPU 내부
- 용량 작음 (개수~수십 개)
- 빠름

메모리:
- 수십~수백 클럭
- CPU 외부
- 용량 큼 (GB)
- 느림
```

범용 레지스터는 ALU 연산 결과 저장, 주소 계산, 임시 변수 저장 등 다양한 용도로 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 기본 레지스터 구조

```
n비트 범용 레지스터:

Data[0] ──┐
Data[1] ──┼──[Write]──┬──[D FF 0]── Q[0]
Data[2] ──┤           │
   ...    ┤          ... ↕  (클럭 공유)
Data[n-1]─┘           │
                     └──[D FF n-1]── Q[n-1]
                           ↑
                        Reset

Clk ────────────────────────┴─── (모든 FF에 공통)

제어:
Write=1, Clk↑: Data → Q
Write=0: 유지
Reset=1: Q ← 0
```

### D FF 기반 레지스터

```
1비트 레지스터 셀:

D ──┐
     │
     ├──[MUX]──[D FF]── Q ──┬──[Tristate]── Output
     │   ↑       ↑          │    ↑
   WE  ─┘    Clk       Reset   OE
  (Write Enable)     (Output Enable)

동작:
- WE=1, Clk↑: D → FF
- WE=0: 유지
- OE=1: Q → Output
- OE=0: High-Z (버스 분리)
```

### 타이밍 다이어그램

```
레지스터 쓰기:

Data:  ────┐       ┌─────┐       ┌───
            0xAA   │ 0x55│
           ┌───┐   └──┐  └───┐
WE:    ────┤   ├──────┤      ├────
           └───┘      └──┘
Clk:   ────┬───┬───┬───┬───┬───
            ↑   ↑   ↑   ↑   ↑
            │   │   │   │   │
          쓰기  │  쓰기 │   │
              유지   유지  |

Q:     ────┐   ┌─────┐   ┌───
            0xAA│ 0x55│

시점:
t1: WE=1, Clk↑ → Q ← Data (0xAA)
t2: WE=0 → 유지
t3: WE=1, Clk↑ → Q ← Data (0x55)
```

### 삼상 출력 (Tristate Buffer)

```
삼상 버퍼:

Q ──[Tristate]── Bus
     ↑
    OE

동작:
OE=0: High-Z (버스에서 분리)
OE=1: Q → Bus (구동)

버스 공유:
Reg1 Q1 ─┬
Reg2 Q2 ─┼──[Tristate]── Data Bus
Reg3 Q3 ─┘

OE1=1, OE2=0, OE3=0: Reg1 구동
OE1=0, OE2=1, OE3=0: Reg2 구동
```

### 레지스터 읽기/쓰기

```
동기식 쓰기 (Synchronous Write):

1. CPU → Data Bus: 데이터
2. CPU → RegSel: 레지스터 선택
3. CPU → Write: 쓰기 신호
4. Clk↑: Data Bus → 선택된 Reg

비동기식 읽기 (Asynchronous Read):

1. CPU → RegSel: 레지스터 선택
2. CPU → Read: 읽기 신호
3. Reg Q → Data Bus (즉시, Clk 무관)
```

### Reset 동작

```
Reset (초기화):

1. Asynchronous Reset:
Reset=1 → 즉시 Q ← 0 (Clk 무관)

2. Synchronous Reset:
Reset=1, Clk↑ → Q ← 0

동기 Reset vs 비동기 Reset:
비동기: 빠름, 메타스터빌리티 위험
동기: 안정, 클럭 필요
```

### 다중 포트 레지스터

```
2포트 레지스터 (Read/Write 동시):

Write Port:
DataIn ──────────────────→ FF
            ↑
         WriteEnable

Read Ports:
FF ──→ Q_A (Read Port A)
FF ──→ Q_B (Read Port B)

동시 읽기/쓰기 가능
```

## Ⅲ. 융합 비교

### 레지스터 vs 래치

| 비교 항목 | 레지스터 | 래치 |
|----------|---------|------|
| 트리거 | 에지 | 레벨 |
| 클럭 | Clock | Enable |
| 투명성 | 없음 | 있음 |
| 응용 | CPU | 파이프라인 |

### 레지스터 구현

| 방식 | 구조 | 지연 | 전력 | 응용 |
|------|------|------|------|------|
| D FF | Master-Slave | 중간 | 중간 | 범용 |
| Pulsed Latch | Latch + Pulse | 작음 | 낮음 | 고성능 |
| Static RAM | 6T | 큼 | 낮음 | 저전력 |

### Reset 방식

| 방식 | 타이밍 | 장점 | 단점 | 응용 |
|------|--------|------|------|------|
| Async Reset | 즉시 | 빠름 | Glitch 위험 | 시스템 |
| Sync Reset | Clk 동기 | 안정 | 느림 | 내부 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 레지스터 파일

```
레지스터 파일 (Register File):

Read Port 1 (A1) ──┬──[Decoder]──[Reg 0]──┬── RD1
Read Port 2 (A2) ──┤              ...    ├── RD2
Write Port (A3) ───┤           [Reg n-1]──┘
Write Data (WD3) ──┘
Write Enable (WE3)─┘

구조:
- n개 레지스터 배열
- 2개 읽기 포트
- 1개 쓰기 포트
- Decoder로 레지스터 선택

특징:
- 동시 2개 읽기
- 1개 쓰기
- 1 클럭 액세스
```

### MIPS 레지스터 파일

```
MIPS 32비트 레지스터 파일:

32 × 32비트 레지스터
- $0 ~ $31
- $0: 항상 0
- $31: 반환 주소 (Return Address)

Read Ports:
rs ─→ 5비트 입력 ─→[Decoder]→[Reg File]→32비트 출력
rt ─→ 5비트 입력 ─→[Decoder]→[Reg File]→32비트 출력

Write Port:
rd ─→ 5비트 입력 ─→[Decoder]
Write Data ───────────────────→[Reg File]
RegWrite ─────────────────────→ Enable

타이밍:
- Read: 조합 회로 (즉시)
- Write: Clk↑에 저장
```

### 파이프라인 레지스터

```
파이프라인 레지스터:

Stage 1 ──[Pipeline Reg]── Stage 2

동작:
- 클럭마다 데이터 전송
- 각 Stage의 결과 저장
- 다음 Stage로 전달

IF/ID ── PC, Instruction
ID/EX ── Register values, Control
EX/MEM ── ALU result, Register
MEM/WB ── Memory data, Register

특징:
- 동기식 전송
- 격리 (Stage 간)
- 스텝별 디버깅
```

### 플래그 레지스터

```
플래그 레지스터 (Status Register):

비트 구성:
[31:5] Reserved
[4]    C (Carry)
[3]    V (Overflow)
[2]    Z (Zero)
[1]    N (Negative)
[0]    Reserved

동작:
ALU Result → Flag Generator → Flags

Flag Generation:
Z = (Result == 0)
N = Result[MSB]
C = Cout from addition
V = (A[MSB]==B[MSB]) & (Result[MSB]!=A[MSB])

용도:
- 조건 분기
- 산술 플래그
- 인터럽트 플래그
```

## Ⅴ. 기대효과 및 결론

범용 레지스터는 CPU의 작업 공간이다. 빠른 액세스로 연산 속도를 결정한다.

## 📌 관련 개념 맵

```
범용 레지스터
├── 구조
│   ├── D FF 병렬 연결
│   ├── Write Enable (WE)
│   ├── Output Enable (OE)
│   └── Tristate Buffer
├── 동작
│   ├── Synchronous Write (Clk↑)
│   ├── Asynchronous Read
│   ├── Reset (Sync/Async)
│   └── Hold (유지)
├── 특징
│   ├── 병렬 입출력
│   ├── 1 클럭 액세스
│   ├── 비투명성
│   └── 버스 공유
└── 응용
    ├── 레지스터 파일
    ├── 파이프라인 레지스터
    ├── 플래그 레지스터
    └── 프로그램 카운터
```

## 👶 어린이를 위한 3줄 비유 설명

1. 범용 레지스터는 책상 위의 서류 정리함 같아요. 여러 개의 칸이 있어서 종이를 넣고 꺼낼 수 있어요
2. Write 신호를 보내면 데이터를 레지스터에 저장하고, Read 신호를 보내면 저장된 데이터를 꺼내볼 수 있어요
3. CPU는 레지스터에 있는 데이터를 바로 사용할 수 있어서 메모리보다 훨씬 빨라요. 계산 결과를 잠시 넣어두는 보관함이에요

```python
# 범용 레지스터 시뮬레이션

from typing import List, Optional


class Register:
    """범용 레지스터"""

    def __init__(self, bits: int = 32, name: str = "Reg"):
        """
        n비트 레지스터

        Args:
            bits: 비트 수
            name: 레지스터 이름
        """
        self.bits = bits
        self.name = name
        self.value = 0
        self.prev_clk = 0

    def clock(self, data: int, we: int, clk: int, reset: int = 0) -> int:
        """
        클럭에 따른 상태 변화

        Args:
            data: 입력 데이터
            we: Write Enable (0/1)
            clk: 클럭 신호 (0/1)
            reset: Reset 신호 (0/1)

        Returns:
            현재 값
        """
        # Asynchronous Reset
        if reset == 1:
            self.value = 0
            return self.value

        # 상승 에지 검출
        if self.prev_clk == 0 and clk == 1:
            if we == 1:
                # 데이터 쓰기
                self.value = data & ((1 << self.bits) - 1)

        self.prev_clk = clk
        return self.value

    def read(self) -> int:
        """비동기 읽기"""
        return self.value

    def write(self, data: int, clk: int):
        """동기식 쓰기 (상승 에지)"""
        self.clock(data, we=1, clk=clk)

    def reset(self):
        """리셋"""
        self.value = 0
        self.prev_clk = 0

    def __str__(self):
        return f"{self.name}: 0x{self.value:0{self.bits//4}X} ({self.value})"

    def __repr__(self):
        return self.__str__()


class TristateRegister(Register):
    """삼상 출력 레지스터"""

    def __init__(self, bits: int = 32, name: str = "Reg"):
        super().__init__(bits, name)
        self.output_enable = 0
        self.bus_value = None

    def read(self, oe: int = 1) -> Optional[int]:
        """
        삼상 읽기

        Args:
            oe: Output Enable (0/1)

        Returns:
            oe=1: 값, oe=0: None (High-Z)
        """
        self.output_enable = oe
        if oe == 1:
            return self.value
        return None  # High-Z


class RegisterFile:
    """레지스터 파일"""

    def __init__(self, num_regs: int = 32, bits: int = 32):
        """
        레지스터 파일

        Args:
            num_regs: 레지스터 개수
            bits: 비트 수
        """
        self.num_regs = num_regs
        self.bits = bits
        self.regs = [Register(bits, f"R{i}") for i in range(num_regs)]
        self.regs[0].value = 0  # $0은 항상 0

    def read(self, reg_num: int) -> int:
        """
        레지스터 읽기

        Args:
            reg_num: 레지스터 번호

        Returns:
            레지스터 값
        """
        if not (0 <= reg_num < self.num_regs):
            raise ValueError(f"레지스터 번호 범위 초과: {reg_num}")
        return self.regs[reg_num].read()

    def write(self, reg_num: int, data: int, we: int, clk: int):
        """
        레지스터 쓰기

        Args:
            reg_num: 레지스터 번호
            data: 쓰기 데이터
            we: Write Enable
            clk: 클럭
        """
        if not (0 <= reg_num < self.num_regs):
            raise ValueError(f"레지스터 번호 범위 초과: {reg_num}")

        # $0에는 쓸 수 없음
        if reg_num == 0:
            return

        self.regs[reg_num].clock(data, we, clk)

    def read_two(self, rs: int, rt: int) -> tuple:
        """
        두 레지스터 동시 읽기

        Args:
            rs: 첫 번째 레지스터 번호
            rt: 두 번째 레지스터 번호

        Returns:
            (rs 값, rt 값)
        """
        return self.read(rs), self.read(rt)

    def __str__(self):
        result = "Register File:\n"
        for i in range(0, self.num_regs, 4):
            row = []
            for j in range(4):
                if i + j < self.num_regs:
                    row.append(f"{self.regs[i+j]}")
            result += "  " + ", ".join(row) + "\n"
        return result


class PipelineRegister:
    """파이프라인 레지스터"""

    def __init__(self, bits: int, name: str = "PipeReg"):
        self.bits = bits
        self.name = name
        self.value = 0
        self.prev_clk = 0

    def clock(self, input_data: int, clk: int) -> int:
        """
        클럭에 따른 데이터 전송

        Args:
            input_data: 입력 데이터
            clk: 클럭

        Returns:
            현재 출력
        """
        # 상승 에지에서 입력 캡처
        if self.prev_clk == 0 and clk == 1:
            self.value = input_data & ((1 << self.bits) - 1)

        self.prev_clk = clk
        return self.value

    def get_output(self) -> int:
        """출력 반환"""
        return self.value


class StatusRegister:
    """상태 레지스터 (플래그)"""

    def __init__(self):
        self.c = 0  # Carry
        self.v = 0  # Overflow
        self.z = 0  # Zero
        self.n = 0  # Negative

    def update_flags(self, result: int, carry_out: int = 0):
        """
        ALU 결과로 플래그 업데이트

        Args:
            result: ALU 결과 (32비트)
            carry_out: 캐리 출력
        """
        self.z = 1 if result == 0 else 0
        self.n = (result >> 31) & 1
        self.c = carry_out

    def get_flags(self) -> int:
        """플래그 값을 4비트로 반환"""
        return (self.c << 3) | (self.v << 2) | (self.z << 1) | self.n

    def __str__(self):
        return f"Flags: C={self.c} V={self.v} Z={self.z} N={self.n}"


def demonstration():
    """범용 레지스터 데모"""
    print("=" * 60)
    print("범용 레지스터 (General Purpose Register) 데모")
    print("=" * 60)

    # 기본 레지스터
    print("\n[기본 레지스터 동작]")
    reg = Register(bits=8, name="R1")

    # 시뮬레이션
    test_sequence = [
        (0xAA, 1, 1, "Data=0xAA, WE=1, Clk=1 → 쓰기"),
        (0x55, 0, 0, "Data=0x55, WE=0 → 무시"),
        (0x55, 1, 1, "Data=0x55, WE=1, Clk=1 → 쓰기"),
        (0xFF, 0, 1, "Data=0xFF, WE=0 → 무시"),
    ]

    print(f"{'Data':<6} {'WE':<3} {'Clk':<4} {'R1':<8} {'설명':<30}")
    print("-" * 55)

    for data, we, clk, desc in test_sequence:
        value = reg.clock(data, we, clk)
        print(f"0x{data:02X}   {we:<3} {clk:<4} 0x{value:02X}     {desc}")

    # 레지스터 파일
    print(f"\n[레지스터 파일 (MIPS 스타일)]")
    reg_file = RegisterFile(num_regs=8, bits=8)

    # 초기화
    print(reg_file)

    # 쓰기
    print("\n쓰기 연산:")
    clk = 0
    for i in range(1, 5):
        clk = 1 - clk  # 클럭 토글
        reg_file.write(i, i * 0x11, we=1, clk=clk)
        print(f"  R{i} ← 0x{i * 0x11:02X}")

    print(reg_file)

    # 읽기
    print("\n읽기 연산:")
    rs, rt = reg_file.read_two(1, 3)
    print(f"  read(R1, R3) = (0x{rs:02X}, 0x{rt:02X})")

    # 파이프라인 레지스터
    print(f"\n[파이프라인 레지스터]")
    pipe_regs = [
        PipelineRegister(bits=8, name="IF/ID"),
        PipelineRegister(bits=8, name="ID/EX"),
        PipelineRegister(bits=8, name="EX/MEM"),
    ]

    # 데이터 전파
    data = 0x11
    print("클럭마다 1스테이지 전파:")
    for cycle in range(5):
        # 첫 번째 파이프라인 레지스터 입력
        if cycle < 3:
            input_data = data + cycle * 0x11
        else:
            input_data = 0

        clk = 1
        # 파이프라인 전파
        for i in range(len(pipe_regs)):
            if i == 0:
                pipe_regs[i].clock(input_data, clk)
            else:
                pipe_regs[i].clock(pipe_regs[i-1].get_output(), clk)

        clk = 0
        for reg in pipe_regs:
            reg.clock(0, clk)

        # 출력
        outputs = [f"{pr.get_output():02X}" for pr in pipe_regs]
        print(f"  Cycle {cycle}: [{', '.join(outputs)}]")

    # 상태 레지스터
    print(f"\n[상태 레지스터]")
    status = StatusRegister()

    # ALU 결과 시뮬레이션
    alu_results = [0, 10, -5, 0, 127]
    for result in alu_results:
        status.update_flags(result)
        print(f"  Result={result:4d} → {status}")


if __name__ == "__main__":
    demonstration()
```
