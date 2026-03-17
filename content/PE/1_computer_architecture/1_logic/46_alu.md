+++
title = "ALU (Arithmetic Logic Unit, 산술 논리 연산 장치)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "CPU"]
draft = false
+++

# ALU (Arithmetic Logic Unit, 산술 논리 연산 장치)

## 핵심 인사이트 (3줄 요약)
1. ALU는 CPU의 핵심 구성 요소로 산술 연산(덧셈, 뺄셈), 논리 연산(AND, OR, XOR), 시프트 연산을 수행하며, Operation Code에 따라 MUX로 연산을 선택한다
2. n비트 ALU는 n비트 가산기, n비트 논리 게이트, 시프터, MUX로 구성되며, Flag 레지스터(Zero, Carry, Overflow, Sign)를 출력한다
3. 기술사시험에서는 ALU의 제어 신호, 연산자 선택, Flag 생성, 파이프라인 ALU가 핵심이다

## Ⅰ. 개요 (500자 이상)

ALU(Arithmetic Logic Unit)는 **CPU의 데이터 경로(Data Path)에서 산술 연산과 논리 연산을 수행**하는 하드웨어 모듈이다. 모든 프로그램의 명령어 실행에 필수적인 연산을 담당하며, 레지스터에서 피연산자를 읽어 연산을 수행하고 결과를 다시 레지스터에 저장한다.

```
ALU 기본 구조:

입력:
- Operand A (n비트)
- Operand B (n비트)
- ALU Control (연산 선택)

출력:
- Result (n비트)
- Flags (Z, C, O, S)

연산:
산술: ADD, SUB, INC, DEC
논리: AND, OR, XOR, NOT
시프트: SHL, SHR, ROL, ROR
비교: CMP, TEST
```

**ALU의 핵심 기능:**

1. **산술 연산 (Arithmetic Operations)**
   - ADD: 덧셈 (A + B)
   - SUB: 뺄셈 (A - B)
   - INC: 증가 (A + 1)
   - DEC: 감소 (A - 1)

2. **논리 연산 (Logical Operations)**
   - AND: 논리곱
   - OR: 논리합
   - XOR: 배타적 논리합
   - NOT: 논리 부정

3. **시프트 연산 (Shift Operations)**
   - SHL/SHR: 논리 시프트
   - SAR/SAL: 산술 시프트
   - ROL/ROR: 회전 (Rotate)

4. **비교 연산 (Comparison)**
   - CMP: 비교 (A - B, 결과는 폐기, Flag만 설정)
   - TEST: 테스트 (A AND B, 결과는 폐기, Flag만 설정)

```
ALU Operation Code 예시:
0000: ADD
0001: SUB
0010: AND
0011: OR
0100: XOR
0101: NOT
0110: SHL
0111: SHR
1000: ROL
1001: ROR
1010: CMP
1011: TEST
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### ALU 회로 구조

```
n비트 ALU 구조:

                ┌─────────────────┐
OpA ──┬────────→│    ADDER/SUB    │
      │         │                 │
      │    ┌────┴────┐         ┌──┴──┐ Result
      │    │ LOGIC   │         │ MUX │───→
      │    │ UNIT    │─────────┤     │
OpB ───┴────┤         │         │     │
             │ SHIFT   │─────────┤     │
             └─────────┘         └──┬──┘
                                   │
            ALU Control ───────────┘

LOGIC UNIT:
- AND: A & B
- OR: A | B
- XOR: A ^ B
- NOT: ~A

SHIFTER:
- SHL: A << n
- SHR: A >> n
- ROL: Rotate Left
- ROR: Rotate Right
```

### Flag 생성

```
ALU Flag 레지스터:

Z (Zero): 결과가 0이면 1
  Z = NOR(Result)

C (Carry): 캐리 발생
  산술: C = Cout (가산기 출력)
  시프트: C = 시프트아웃 비트

O (Overflow): 오버플로우
  O = Cin(MSB) ⊕ Cout(MSB)
    또는
  O = (A_MSB = B_MSB) ∧ (Result_MSB ≠ A_MSB)

S (Sign): 결과 부호 (MSB)
  S = Result[n-1]

P (Parity): 패리티 (일부 ALU)
  P = XOR(Result[7:0])  # 하위 8비트
```

### ALU 제어

```
ALU Control Decoder:

OP[3:0] ──┬──→ 1-of-16 Decoder ── Control Signals
           │
           └──→ Function Select

Control Examples:
- ADD: Adder Enable, Sub=0
- SUB: Adder Enable, Sub=1
- AND: Logic Unit Enable, AND Select
- OR:  Logic Unit Enable, OR Select
- SHL: Shifter Enable, Left Shift

MUX Control:
- 4개 연산 단위 중 1개 선택
- 2-bit Control: 00=Adder, 01=Logic, 10=Shift, 11=Mult/Div
```

### 32비트 ALU 예시

```
MIPS ALU (32비트):

연산:
- ADDU, SUBU (산술)
- AND, OR, XOR, NOR (논리)
- SLT, SLTI (비교)

구성:
1. 32비트 가산기
   - CLAA 구현
   - 8 게이트 지연

2. 32비트 논리 유닛
   - 32개 AND/OR/XOR/NOR 게이트
   - 1 게이트 지연

3. 32비트 시프터
   - Barrel Shifter
   - 5 게이트 지연 (32비트)

4. 결과 MUX
   - 4-to-1 MUX
   - 1-2 게이트 지연

총 지연: 8 + 2 = 10 게이트
@ 120ps: 1.2ns → 833 MHz
```

## Ⅲ. 융합 비교

### ALU vs FPU vs GPU

| 비교 항목 | ALU | FPU | GPU |
|----------|-----|-----|-----|
| 데이터 | 정수 | 부동소수점 | 벡터 |
| 연산 | 기본 | sin, cos, exp | 행렬, 텍스처 |
| 정밀도 | 32/64비트 | 32/64/128비트 | 16/32비트 |
| 병렬성 | 1-4 | 1-2 | 1000+ |
| 응용 | 범용 | 과학, 엔지니어링 | 그래픽, AI |

### ALU 구현 방식

| 타입 | 구조 | 속도 | 면적 | 응용 |
|------|------|------|------|------|
| 단순 ALU | 1개 유닛 | 느림 | 작음 | 임베디드 |
| 파이프라인 ALU | 스테이지 분리 | 빠름 | 중간 | 일반 CPU |
| superscalar | 다중 ALU | 매우 빠름 | 큼 | 고성능 CPU |
| Vector ALU | SIMD | 매우 빠름 | 큼 | GPU, DSP |

### ALU 연산 속도

| 연산 | 지연 (게이트) | 시간 (@120ps) |
|------|--------------|---------------|
| ADD | 8 | 960ps |
| SUB | 8 | 960ps |
| AND | 2 | 240ps |
| OR | 2 | 240ps |
| XOR | 2 | 240ps |
| SHL | 5 | 600ps |
| MUL | 10-20 | 1.2-2.4ns |
| DIV | 30-50 | 3.6-6ns |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86-64 ALU

```
Intel/AMD 64비트 ALU:

구조:
- 2개 64비트 ALU (정수)
- 1개 128비트 SIMD (SSE/AVX)
- 1개 256비트 SIMD (AVX2)

연산:
- 산술: ADD, SUB, MUL, IMUL, DIV
- 논리: AND, OR, XOR, NOT, TEST
- 시프트: SHL, SHR, SAR, SAL, ROL, ROR, RCL, RCR
- 비교: CMP, TEST
- 문자열: MOVS, CMPS, SCAS

파이프라인:
- 4단계: IF → ID → EX → WB
- EX 내부: 2-3 서브사이클
- 최대 4개 명령어 동시 발행
```

### ARM ALU

```
ARM Cortex-A76 ALU:

구조:
- 2개 64비트 정수 ALU
- 1개 128비트 NEON (SIMD)

연산:
- 산술: ADD, SUB, ADC, SBC
- 논리: AND, ORR, EOR, BIC, MVN
- 시프트: LSL, LSR, ASR, ROR
- 비교: CMP, CMN, TST, TEQ
- MAC: MADD, MSUB

특징:
- 조건부 실행 (Predicated Execution)
- Barrel Shifter 통합
- MAC 유닛 내장
```

### ALU 설계 고려사항

```

성능 최적화:
1. Critical Path 최소화
   - CLAA 사용
   - Barrel Shifter
   - Carry Chain 최적화

2. 파이프라이닝
   - EX 스테이지 분리
   - Operand Forwarding
   - Scoreboarding

3. Speculation
   - Speculative Add
   - Condition Code Prediction

면적 최적화:
1. 공유 하드웨어
   - Adder 재사용 (가감산기)
   - Logic Unit 공유

2. Function Unit 선택
   - 필수 연산만 구현
   - 나머지는 Microcode
```

## Ⅴ. 기대효과 및 결론

ALU는 CPU의 심장이다. 모든 연산을 수행하며 컴퓨터 성능을 결정한다.

## 📌 관련 개념 맵

```
ALU
├── 산술 연산
│   ├── ADD/SUB
│   ├── MUL/DIV (일부)
│   └── INC/DEC
├── 논리 연산
│   ├── AND/OR
│   ├── XOR/NOT
│   └── TEST
├── 시프트 연산
│   ├── Logical (SHL/SHR)
│   ├── Arithmetic (SAL/SAR)
│   └── Rotate (ROL/ROR)
├── Flag 레지스터
│   ├── Z (Zero)
│   ├── C (Carry)
│   ├── O (Overflow)
│   └── S (Sign)
└── 구현
    ├── Combinational
    ├── Pipelined
    └── Superscalar
```

## 👶 어린이를 위한 3줄 비유 설명

1. ALU는 계산기와 논리 문제를 푸는 도구를 합쳐둔 것 같아요. 숫자 더하기/빼기와 AND/OR 같은 논리 연산을 모두 할 수 있어요
2. 컴퓨터가 "IF문"을 실행할 때 ALU가 조건을 계산하고, "FOR문"에서 카운터를 증가시키는 역할도 해요
3. 현대 CPU는 여러 개의 ALU가 있어서 동시에 여러 계산을 할 수 있어서 훨씬 빠르게 작동해요

```python
# ALU 시뮬레이션

from typing import Tuple, List
from enum import Enum


class ALUOp(Enum):
    """ALU 연산 코드"""
    ADD = 0
    SUB = 1
    AND = 2
    OR = 3
    XOR = 4
    NOT = 5
    SHL = 6
    SHR = 7


class Flags:
    """ALU Flag 레지스터"""

    def __init__(self, z: int = 0, c: int = 0, o: int = 0, s: int = 0):
        self.z = z  # Zero
        self.c = c  # Carry
        self.o = o  # Overflow
        self.s = s  # Sign

    def __str__(self):
        return f"Z={self.z} C={self.c} O={self.o} S={self.s}"

    def to_int(self) -> int:
        """Flag를 정수로 변환 (ZCSR 비트 순서)"""
        return (self.z << 3) | (self.c << 2) | (self.o << 1) | self.s


class ALU:
    """
    산술 논리 연산 장치 (ALU) 시뮬레이션
    """

    def __init__(self, bits: int = 32):
        """
        n비트 ALU 생성

        Args:
            bits: 비트 수
        """
        self.bits = bits
        self.mask = (1 << bits) - 1

    def execute(self, op: ALUOp, a: int, b: int, c_in: int = 0) -> Tuple[int, Flags]:
        """
        ALU 연산 실행

        Args:
            op: 연산 코드
            a: 피연산자 A
            b: 피연산자 B
            c_in: 입력 캐리

        Returns:
            (result, flags): 연산 결과와 Flag
        """
        # 입력 마스크
        a = a & self.mask
        b = b & self.mask

        if op == ALUOp.ADD:
            result, flags = self._add(a, b, c_in)
        elif op == ALUOp.SUB:
            result, flags = self._sub(a, b)
        elif op == ALUOp.AND:
            result = a & b
            flags = self._calc_flags(result)
        elif op == ALUOp.OR:
            result = a | b
            flags = self._calc_flags(result)
        elif op == ALUOp.XOR:
            result = a ^ b
            flags = self._calc_flags(result)
        elif op == ALUOp.NOT:
            result = (~a) & self.mask
            flags = self._calc_flags(result)
        elif op == ALUOp.SHL:
            result = ((a << b) & self.mask)
            flags = self._calc_flags(result)
            flags.c = (a >> (self.bits - b - 1)) & 1 if b < self.bits else 0
        elif op == ALUOp.SHR:
            result = (a >> b)
            flags = self._calc_flags(result)
            flags.c = (a >> (b - 1)) & 1 if b > 0 else 0
        else:
            raise ValueError(f"알 수 없는 연산: {op}")

        return result & self.mask, flags

    def _add(self, a: int, b: int, c_in: int) -> Tuple[int, Flags]:
        """덧셈"""
        result = a + b + c_in

        # 캐리
        c_out = 1 if result >= (1 << self.bits) else 0

        # 오버플로우 (부호 있는 경우)
        a_sign = (a >> (self.bits - 1)) & 1
        b_sign = (b >> (self.bits - 1)) & 1
        r_sign = ((result & self.mask) >> (self.bits - 1)) & 1
        overflow = (a_sign == b_sign) and (r_sign != a_sign)

        result = result & self.mask
        flags = self._calc_flags(result)
        flags.c = c_out
        flags.o = overflow

        return result, flags

    def _sub(self, a: int, b: int) -> Tuple[int, Flags]:
        """뺄셈 (A - B)"""
        # A + ~B + 1
        b_comp = ((~b) & self.mask) + 1
        return self._add(a, b_comp, 0)

    def _calc_flags(self, result: int) -> Flags:
        """Flag 계산"""
        z = 1 if result == 0 else 0
        s = (result >> (self.bits - 1)) & 1
        return Flags(z=z, s=s)


class CPU:
    """간단한 CPU 시뮬레이션 (ALU 포함)"""

    def __init__(self):
        self.registers = [0] * 8  # R0-R7
        self.alu = ALU(bits=32)
        self.pc = 0  # Program Counter
        self.flags = Flags()

    def execute_instruction(self, op: ALUOp, rd: int, rs1: int, rs2: int = None):
        """
        명령어 실행

        Args:
            op: 연산
            rd: Destination 레지스터
            rs1: Source 레지스터 1
            rs2: Source 레지스터 2 (없으면 rs1 사용)
        """
        a = self.registers[rs1]
        b = self.registers[rs2] if rs2 is not None else 0

        result, flags = self.alu.execute(op, a, b)
        self.registers[rd] = result
        self.flags = flags

        print(f"R{rd} = R{rs1} ", end="")
        if rs2 is not None:
            print(f"{op.name} R{rs2} ", end="")
        else:
            print(f"{op.name} ", end="")
        print(f"= {result:08X} [{flags}]")


def demonstration():
    """ALU 데모"""
    print("=" * 70)
    print("ALU (Arithmetic Logic Unit) 데모")
    print("=" * 70)

    alu = ALU(bits=32)

    # 산술 연산
    print("\n[산술 연산]")
    operations = [
        (ALUOp.ADD, 100, 50),
        (ALUOp.SUB, 100, 50),
        (ALUOp.ADD, 0xFFFFFFFF, 1),  # Overflow
    ]

    for op, a, b in operations:
        result, flags = alu.execute(op, a, b)
        print(f"{a:08X} {op.name:3s} {b:08X} = {result:08X} [{flags}]")

    # 논리 연산
    print("\n[논리 연산]")
    logic_ops = [
        (ALUOp.AND, 0xFF00FF00, 0x00FF00FF),
        (ALUOp.OR, 0xFF000000, 0x00FF0000),
        (ALUOp.XOR, 0xFFFFFFFF, 0x12345678),
        (ALUOp.NOT, 0x12345678, 0),
    ]

    for op, a, b in logic_ops:
        result, flags = alu.execute(op, a, b)
        print(f"{a:08X} {op.name:3s} {b:08X} = {result:08X} [{flags}]")

    # 시프트 연산
    print("\n[시프트 연산]")
    shift_ops = [
        (ALUOp.SHL, 0x00000001, 4),
        (ALUOp.SHR, 0x80000000, 4),
        (ALUOp.SHL, 0x12345678, 8),
    ]

    for op, a, b in shift_ops:
        result, flags = alu.execute(op, a, b)
        print(f"{a:08X} {op.name:3s} {b:d} = {result:08X} [C={flags.c}]")

    # CPU 시뮬레이션
    print("\n" + "=" * 70)
    print("CPU 명령어 실행")
    print("=" * 70)

    cpu = CPU()

    # 초기화
    cpu.registers[1] = 100
    cpu.registers[2] = 50
    cpu.registers[3] = 0xFF00FF00
    cpu.registers[4] = 0x00FF00FF

    print("\n초근 레지스터 상태:")
    for i, val in enumerate(cpu.registers[:5]):
        print(f"  R{i} = 0x{val:08X}")

    print("\n명령어 실행:")
    cpu.execute_instruction(ALUOp.ADD, 0, 1, 2)   # R0 = R1 + R2
    cpu.execute_instruction(ALUOp.SUB, 5, 1, 2)   # R5 = R1 - R2
    cpu.execute_instruction(ALUOp.AND, 6, 3, 4)   # R6 = R3 & R4
    cpu.execute_instruction(ALUOp.XOR, 7, 1, 2)   # R7 = R1 ^ R2

    print("\n결과 레지스터 상태:")
    for i, val in enumerate(cpu.registers[:8]):
        print(f"  R{i} = 0x{val:08X}")


def alu_benchmark():
    """ALU 성능 벤치마크"""
    import time

    print("\n" + "=" * 70)
    print("ALU 성능 벤치마크")
    print("=" * 70)

    alu = ALU(bits=64)

    iterations = 1000000

    operations = [
        ALUOp.ADD,
        ALUOp.SUB,
        ALUOp.AND,
        ALUOp.OR,
        ALUOp.XOR,
    ]

    for op in operations:
        start = time.time()

        for i in range(iterations):
            alu.execute(op, i, i + 1)

        elapsed = time.time() - start
        ops_per_sec = iterations / elapsed

        print(f"{op.name:3s}: {ops_per_sec:,.0f} ops/sec ({elapsed*1000:.2f}ms for {iterations:,})")


if __name__ == "__main__":
    demonstration()
    alu_benchmark()
```
