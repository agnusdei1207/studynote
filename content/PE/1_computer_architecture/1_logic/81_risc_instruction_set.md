+++
title = "RISC 명령어 세트 (RISC Instruction Set)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# RISC 명령어 세트 (RISC Instruction Set)

## 핵심 인사이트 (3줄 요약)
1. RISC(Reduced Instruction Set Computer)는 단순한 명령어와 Load/Store 구조로 빠른 파이프라이닝과 단순한 하드웨어를 목표로 하는 명령어 세트 설계 철학이다
2. 모든 명령어가 고정 길이(32비트)이며, 메모리 액세스는 Load/Store 명령어로만 수행하고 레지스-레지스터 연산만 지원한다
3. 기술사시험에서는 RISC 설계 원칙, Load/Store 구조, 파이프라이닝, MIPS/ARM/RISC-V가 핵심이다

## Ⅰ. 개요 (500자 이상)

RISC(Reduced Instruction Set Computer)는 **단순한 명령어 세트과 Load/Store 구조로 높은 성능과 단순한 하드웨어를 달성하는 설계 철학**이다. 1980년대 스탠포드 대학 연구에서 시작되어 MIPS, ARM, RISC-V 등 대중적인 ISA가 RISC 설계를 따른다.

```
RISC 설계 철학:
목적: CISC의 복잡성 해결

원칙:
1. Simplicity: 단순한 명령어
2. Load/Store: 메모리 액세 제한
3. Pipeline: 단순한 파이프라인
4. Register: 많은 범용 레지스

특징:
- 고정 길이 명령어
- 단순한 디코딩
- 레지스 중심
- 컴파일러 최적화

결과:
- 높은 클럭 속도
- 낮은 CPI (CPI=1)
- 낮은 전력
```

**RISC의 핵심 특징:**

1. **단순성**: 모든 명령어 1 클럭 실행
2. **Load/Store**: 메모리는 Load/Store로만 접근
3. **레지스터**: 많은 범용 레지스
4. **파이프라인**: 명령어어 단순하여 파이프라인 효율적

```
RISC vs CISC:
RISC:
- 단순 명령어
- Load/Store
- 파이프라인 친화

CISC:
- 복잡한 명령어
- Memory Operand
- Microcode
```

## Ⅱ. 아키텍처 및 핵싱 원리 (1000자 이상)

### Load/Store 구조

```
Load/Store Architecture:

RISC:
산술/논리 연산:
ADD R1, R2, R3  ← Register-Register

메모리 액세:
LW R1, 0(R2)    ← Load Word
SW R1, 0(R2)    ← Store Word

CISC:
산술/논리 연산:
ADD EAX, [EBX]   ← Memory-Register

RISC 장점:
- 명령어 단순
- 디코딩 간단
- 파이프라인 깊게
```

### 명령어 포맷

```

MIPS R-format (Register):

31  26 25  21 20 16 15 11   7   6  5   0
┌───┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬─┐
│Op │Rs │Rt │Rd │Sa │St│Fn │   │   │   │
└───┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴─┘

예: ADD $t0, $t1, $t2
Op=0 (ADD)
Rs=$t1 (Source 1)
Rt=$t2 (Source 2)
Rd=$t0 (Destination)
```

### I-format (Immediate)

```

MIPS I-format (Immediate):

31 26 25 21 20                16 15        7  6         0
┌───┬──┬──┴───────────────────────┬───────┴─────────────┴─────────┐
│Op │Rs │rt │    Immediate[15:0]       │          │               │
└───┴──┴──┴───────────────────────┴──────────┴─────────────┴─────────┘

예: ADDI $t0, 100
Op=0x08 (ADDI)
Rs=$0 (Source)
Rt=$t0 (Destination)
Imm=100

타이밍:
IF/ID Phase:
  I-format 명령어
ID/EX Phase:
  ALU Operation
EX/MEM Phase:
  (None, Register)
MEM/WB:
  Register Write
```

### J-format (Jump)

```
MIPS J-format (Jump):

31 26 25                        0
┌───┴┬───────────────────────────┬───────┴──────────────────┐
│Op │    Address[25:0]            │          │               │
└───┴┴───────────────────────────┴──────────┴──────────────────┘

예: J 0x1000
Op=0x02 (J)
Addr=0x1000

Branch Target:
PC ← PC + SignExt(Imm << 2)

타이밍:
IF: Jump Target 계산
ID: PC ← Target
EX: ALU (NOP)
MEM: (None)
WB: PC ← Target
```

### 파이프라이닝

```

5-Stage Pipeline:

IF  ID   EX   MEM  WB
↓   ↓    ↓    ↓    ↓
Fetch Decode Execute Memory Writeback

각 Stage 동작:
IF: Instruction Fetch
  - PC → Memory
  - IR ← Instruction

ID: Instruction Decode
  - Register Read
  - Control Signal

EX: Execute
  - ALU Operation
  - Branch Target

MEM: Memory Access
  - Load/Store

WB: Write Back
  - Register Write

RISC의 파이프라인 장점:
- 모든 명령어 5 Stage
- CPI = 1 (이상적인 경우)
- Deep Pipeline 가능
- High Frequency
```

### 범용 레지스

```

RISC 레지스 설계:

MIPS (32개 레지스):
- $0-$7: $t0-$t7 (Temporary)
- $8-$15: $s0-$s7 (Saved)
- $16-$23: $t0-$t7 (Temp)
- $24-$31: $k0-$k1 (Kernel)
- $28: $gp (Global Pointer)
- $29: $sp (Stack Pointer)

ARM (16개 레지스):
- R0-R12: General Purpose
- R13: SP (Stack Pointer)
- R14: LR (Link Register)
- R15: PC (Program Counter)

RISC-V (32개 레지스트):
- x0-x7: Arguments (a0-a7)
- x8-x15: Saved (s0-s7)
- x16-x27: Temporary (t0-t11)
- x28-x31: Arguments (a0-a3)

설계 원칙:
- 레지스: 적게
- 범용: 많이
- 특수 목적: 일부
```

## Ⅲ. 융합 비교

### RISC ISA 비교

| ISA | 비트 | 명령어 | 레지스 | 특징 |
|-----|------|--------|--------|------|
| MIPS32 | 32 | 100+ | 32 | 고전형 |
| ARMv8 | 32/64 | 100+ | 30 | 모바일 |
| RISC-V | 32 | 50+ | 32 | 확장형 |

### RISC vs CISC 성능

| 항목 | RISC | CISC |
|------|------|------|
| CPI | 1-2 | 1-100+ |
| 클럭 | 높음 | 낮음 |
| 전력 | 낮음 | 높음 |
| 코드 크기 | 큼음 | 작음 |

### 파이프라인 깊이

| 아키텍처 | 파이프라인 | 클럭 | CPI |
|----------|----------|------|-----|
| RISC-V 5-stage | 5 | 3GHz | 1 |
| ARM Cortex-A72 | 15+ | 2.5GHz | 1 |
| MIPS32 5-stage | 5 | 1GHz | 1 |
| Intel Core (CISC) | 14-20 | 5GHz | 0.5-4 |

## Ⅳ. 실무 적용 및 기술사적 판단

### MIPS I

```
MIPS I:

명령어 예:
ADD $t0, $t1, $t2
LW $t0, 0($s1)
SW $t0, 0($s1)
BEQ $t0, $t1, Label

파이프라인):
IF: 4-stage (IF, ID, EX, WB)
- 배타: 1 클럭
- Throughput: 1 IPC

레지스터:
32개 32비트 레지스
- $0-$7: Temp
- $8-$15: Saved
- $16-$23: Temp
- $24-$31: Special

특징:
- 단순하고 규칙적
- 교과용으로 채택
```

### ARM

```
ARM (Advanced RISC Machine):

ARMv8-A 64-bit:
- Load/Store
- 31개 64비트 레지스
- 3-address format

명령어:
LDR X0, [X1]      ; Load
ADD X0, X1, X2    ; Add
STR X0, [X1]      ; Store
B   Label          ; Branch

Thumb-16비트:
- 코드 크기 50% 감소
- 성능 70-80%
- 저전력

Cortex-A76:
- Decoding 3-stage
- Issue 8-stage
- 3GHz+ 가능
```

### RISC-V

```
RISC-V:

특징:
- 오픈 소스 ISA
- 확장 가능한 모듈러 ISA
- 4가지 명령어 형식

R32I Base:
- 47개 기본 명령어
- 31개 레지스
- Load/Store
- 32비트 고정 길이

확장:
M: Multiply (32×32 → 64)
A: Atomic
F: Floating Point
C: Compressed (16비트)
V: Vector (SIMD)

장점:
- 단순하고 깔끔
- 무료 및 개방
- 다양한 확장
```

### SPARC

```

SPARC (Scalable Processor ARchitecture):

Oracle SPARC M8:
- 8-issue
- 32KB L1 I-Cache
- 256KB L2 Cache
- 3.6GHz

명령어 형식:
- 3-address format
- Register Window
- Branch Delay Slot

특징:
- Register Window
- Register Spill
- CALL/RET 효율적
```

## Ⅴ. 기대효과 및 결론

RISC는 현대 CPU의 기본이다. 단순함과 효율로 고성능을 달성한다.

## 📌 관련 개념 맵

```
RISC 명령어 세트
├── 설계 원칙
│   ├── Simplicity
│   ├── Load/Store
│   ├── Pipeline
│   └── Large Register File
├── 명령어 형식
│   ├── R-format (Register)
│   ├── I-format (Immediate)
│   ├── J-format (Jump)
│   └── S-type (Store)
├── 특징
│   ├── Fixed Length
│   ├── Simple Decoding
│   ├── CPI=1
│   └── Compiler Optimization
└── 예시
    ├── MIPS32
    ├── ARM
    ├── RISC-V
    └── SPARC
```

## 👶 어린이를 위한 3줄 비유 설명

1. RISC는 단순한 도구 상자 같아요. 각각 도구는 한 가지 일만 전문적으로 하고, 조합해서 복잡한 일도 할 수 있어요
2. Load/Store는 창고에서 물건을 가져오는 전용 도구 같아요. 메모리에서 읽기/쓰기는 Load/Store만 사용하고, 연산은 레지스에서만 해요
3. 파이프라인은 조립 라인 같아요. 명령어 처리를 여러 단계로 나누어서 각 단계가 동시에 여러 명령어를 처리할 수 있어서 빠르게 동작해요

```python
# RISC 명령어 시뮬레이션

from typing import List, Dict, Optional
from enum import Enum


class Opcode(Enum):
    ADD = 0x00
    ADDI = 0x08
    SUB = 0x02
    AND = 0x24
    OR = 0x25
    LW = 0x23
    SW = 0x2B
    BEQ = 0x04
    J = 0x02


class RISCProcessor:
    """RISC 프로세서 시뮬레이션"""

    def __init__(self):
        # 32개 레지스
        self.registers = [0] * 32
        self.pc = 0
        self.memory = [0] * 65536
        self.running = True

    def fetch(self) -> int:
        """명령어 인출"""
        if 0 <= self.pc < len(self.memory):
            instruction = self.memory[self.pc]
            self.pc += 4
            return instruction
        return 0

    def decode_execute(self, instruction: int) -> bool:
        """명령어 디코딩 및 실행"""
        # MIPS 32비트 포맷
        opcode = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = (instruction >> 0) & 0x3F

        # R-type
        if opcode == 0x00:  # ADD
            self.registers[rd] = self.registers[rs] + self.registers[rt]
            print(f"  ADD ${rd}, ${rs}, ${rt}")
            print(f"    ${rd} = {self.registers[rd]}")
            return True

        # I-type
        elif opcode == 0x08:  # ADDI
            immediate = instruction & 0xFFFF
            self.registers[rt] = self.registers[rs] + immediate
            print(f"  ADDI ${rt}, {rs}, {immediate}")
            print(f"    ${rt} = {self.registers[rt]}")
            return True

        # LW (Load Word)
        elif opcode == 0x23:
            offset = instruction & 0xFFFF
            addr = (self.registers[rs] + offset) & 0xFFFF
            self.registers[rt] = self.memory[addr]
            print(f"  LW ${rt}, {offset}(${rs})")
            print(f"    ${rt} = 0x{self.registers[rt]:04X} @ 0x{addr:04X}")
            return True

        # SW (Store Word)
        elif opcode == 0x2B:
            offset = 0
            for i in range(4):
                offset |= (instruction >> (i * 8)) & 0xFF
            addr = (self.registers[rs] + offset) & 0xFFFF
            data = self.registers[rt]
            self.memory[addr] = data
            print(f"  SW ${rt}, {offset}(${rs})")
            print(f"    0x{addr:04X} ← 0x{data:04X}")
            return True

        # BEQ (Branch if Equal)
        elif opcode == 0x04:
            offset = 0
            for i in range(16):
                offset |= (instruction >> (i * 8)) & 0xFF
            sign_bit = (offset >> 15) & 0x1
            if sign_bit:
                offset |= 0xFFFF0000

            if self.registers[rs] == self.registers[rt]:
                self.pc += offset
                print(f"  BEQ ${rs}, ${rt}, 0x{offset:04X}")
                print(f"    Branch taken → PC=0x{self.pc:04X}")
            else:
                self.pc += 4
                print(f"  BEQ ${rs}, ${rt}, 0x{offset:04X}")
                print(f"    Branch not taken → PC=0x{self.pc:04X}")
            return True

        # J (Jump)
        elif opcode == 0x02:
            addr = 0
            for i in range(26):
                addr |= (instruction >> (i * 8)) & 0xFF
            self.pc = addr
            print(f"  J 0x{addr:04X}")
            print(f"    Jump → PC=0x{self.pc:04X}")
            return True

        return False

    def run(self, num_cycles: int = 10):
        """프로그램 실행"""
        print(f"RISC Processor Run ({num_cycles} cycles)")
        print("=" * 50)

        cycle = 0
        while cycle < num_cycles and self.running:
            inst = self.fetch()
            if inst == 0:
                break

            print(f"\nCycle {cycle}:")
            print(f"  PC=0x{self.pc-4:04X}")

            executed = self.decode_execute(inst)
            cycle += 1

        print("\n최종 상태:")
        print(f"PC: 0x{self.pc:04X}")
        print(f"Registers:")
        for i in range(8):
            print(f"  ${i}: 0x{self.registers[i]:08X}")

    def load_program(self, program: List[tuple]):
        """프로그램 로드"""
        self.memory = [0] * 65536

        addr = 0
        for mnemonic, *operands in program:
            if mnemonic == "ADD":
                rd, rs, rt = operands
                # R-format: ADD Rd, Rs, Rt
                inst = (0x00 << 26) | (rs << 21) | (rt << 16) | (rd << 11)
            elif mnemonic == "ADDI":
                rt, rs, imm = operands
                # I-format: ADDI Rt, Rs, Imm
                inst = (0x08 << 26) | (rs << 21) | (rt << 16) | (imm & 0xFFFF)
            elif mnemonic == "LW":
                rt, rs, offset = operands
                # I-format: LW Rt, offset(rs)
                inst = (0x23 << 26) | (rs << 21) (rt << 16) | offset
            elif mnemonic == "SW":
                rt, rs, offset = operands
                # S-format: SW Rt, offset(rs)
                inst = (0x2B << 26) | (rs << 21) (rt << 16) | offset
            elif mnemonic == "BEQ":
                rs, rt, offset = operands
                # I-format: BEQ Rs, Rt, offset
                inst = (0x04 << 26) | (rs << 21) (rt << 16) | offset
            elif mnemonic == "J":
                addr = operands[0]
                # J-format: J Address
                inst = (0x02 << 26) | addr
            else:
                continue

            self.memory[addr] = inst
            addr += 4

        print("프로그램 로드 완료")


def demonstration():
    """RISC 데모"""
    print("=" * 60)
    print("RISC 명령어 세트 (RISC Instruction Set) 데모")
    print("=" * 60)

    # RISC 프로세서
    cpu = RISCProcessor()

    # 프로그램 작성
    print("\n[프로그램 작성]")
    program = [
        # INIT: $1 = 1
        ("ADDI", 1, 0, 1),
        # LOOP: 5번 반복
        ("ADDI", 2, 2, 1),
        ("BEQ", 2, 1, -8),
        # END: $2 = 6
        ("ADDI", 1, 0, 1),
    ]

    cpu.load_program(program)

    # 실행
    cpu.run(20)

    # RISC 특징
    print("\n[RISC 특징]")
    features = [
        "단순한 명령어 (ADD, SUB, AND, OR)",
        "Load/Store만 메모리 액세",
        "고정 길이 32비트",
        "3주소 연산 (R1, R2, R3)",
        "높은 CPI ≈ 1",
        "깊은 파이프라인",
        "컴파일러 최적화",
    ]

    for feature in features:
        print(f"  • {feature}")

    # RISC vs CISC 코드 비교
    print("\n[코드 비교: A = B + C]")

    print("\nCISC (x86):")
    x86_code = [
        "MOV EAX, 1",
        "MOV EBX, 2",
        "ADD EAX, EBX",  # EAX = EAX + EBX
        "MOV ECX, EAX",
    ]
    print("\n  ".intel_syntax nop\n"
    for line in x86_code:
        print(f"  {line}")

    print("\nRISC (MIPS):")
    mips_code = [
        "ADDI $1, $0, 1",  # $1 = 1
        "ADDI $2, $0, 2",  # $2 = 2
        "ADD $1, $1, $2",  # $1 = $1 + $2 = 3
        "ADDI $2, $2, 3",  # $2 = 2 + 3 = 5
    ]
    print("\n  .text\n  .globl main")
    for line in mips_code:
        print(f"  {line}")

    print("\n분석:")
    print("  CISC: 4명령어, 4+4+5+5 = 18 바이트")
    print("  RISC: 4명령어, 4×4 = 16 바이트")
    print("  (RISC가 더 효율적인 경우도 있음)")

    # CPI 비교
    print("\n[CPI (Clock Per Instruction) 비교]")
    print("RISC:")
    print("  대부분의 명령어: 1 클럭")
    print("  일부 명령어: 2-3 클럭")
    print("  평균: 1.1-1.2")

    print("\nCISC:")
    print("  간단 명령어: 1 클럭")
    print("  복잡한 명령어: 10-100 클럭")
    print("  평균: 4-5 클럭")

    # 레지스 수 비교
    print("\n[레지스터 수]")
    print("RISC:")
    print("  MIPS32: 32개")
    print("  ARMv8: 31개 (R0-R30)")
    print("  RISC-V: 32개")

    print("\nCISC:")
    print("  x86-64: 16개")
    print("    EAX, ECX, EDX, EBX")
    print("    R8-R15")

    print("\nRISC가 레지스가 많은 이유:")
    print("  • Load/Store 구조")
     print("  • Register Renaming")
     print("  • 함수 호출 효율적")
    print("  • 컴파일러 최적화")


if __name__ == "__main__":
    demonstration()
