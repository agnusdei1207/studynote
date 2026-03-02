+++
title = "RISC (Reduced Instruction Set Computer)"
date = 2025-02-27

[extra]
categories = "pe_exam-computer_architecture"
+++

# RISC (Reduced Instruction Set Computer)

## 핵심 인사이트 (3줄 요약)
> **적은 수의 단순 명령어로 구성된 고성능 프로세서 아키텍처**. 1클럭 1명령어 실행, 고정 길이 명령어, Load/Store 구조가 특징. ARM, RISC-V가 대표하며 모바일·임베디드·서버 시장을 지배한다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: RISC(Reduced Instruction Set Computer)는 **적은 수(~100개)의 단순하고 규칙적인 명령어로 구성된 프로세서 아키텍처**로, 각 명령어가 1 클럭 사이클에 실행되도록 설계되어 파이프라이닝과 슈퍼스칼라 구현에 최적화되어 있다.

> 💡 **비유**: RISC는 **"패스트푸드 주방"** 같아요. 각 요리사가 딱 하나의 단순한 작업만 빠르게 처리하죠. "햄버거 번 올리기", "패티 굽기", "치즈 얹기"... 각 작업은 단순하지만, 컨베이어 벨트(파이프라인)에서 돌아가니 엄청 빨라요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - CISC 명령어 복잡성**: x86 등 CISC 명령어는 1~100+ 클럭 소요, 파이프라이닝 어려움
2. **기술적 필요성 - 80/20 법칙 발견**: 1980년대 연구 결과, 프로그램의 80%가 20%의 단순 명령어만 사용
3. **시장/산업 요구 - 전력 효율**: 모바일 기기 확산으로 저전력 고성능 프로세서 필요

**핵심 목적**: **단순화를 통한 성능 극대화** (파이프라이닝 효율, 전력 효율)

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **명령어 세트** | 적은 수의 단순 명령어 | ~100개, 고정 길이 | 기본 조리 도구 |
| **레지스터 파일** | 다수의 범용 레지스터 | 32개 이상 | 작업대 공간 |
| **파이프라인** | 명령어 병렬 처리 | 5~7단계 | 컨베이어 벨트 |
| **Load/Store 유닛** | 메모리 접근 전담 | 연산과 분리 | 재료 창고 |
| **컴파일러** | 복잡한 연산을 단순 명령어로 | 최적화 담당 | 레시피 설계자 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    RISC 5단계 파이프라인                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   클럭 사이클                                                       │
│   ─────────────────────────────────────────────────────────────→   │
│                                                                     │
│   명령어1: │  IF  │  ID  │  EX  │ MEM │  WB  │                    │
│   명령어2: │      │  IF  │  ID  │ EX  │ MEM  │  WB  │             │
│   명령어3: │      │      │  IF  │ ID  │  EX  │ MEM  │  WB  │      │
│   명령어4: │      │      │      │ IF  │  ID  │  EX  │ MEM  │ ...  │
│   명령어5: │      │      │      │     │  IF  │  ID  │  EX  │ ...  │
│                                                                     │
│   IF  = Instruction Fetch (명령어 인출)                            │
│   ID  = Instruction Decode (명령어 해독)                           │
│   EX  = Execute (실행)                                              │
│   MEM = Memory Access (메모리 접근)                                │
│   WB  = Write Back (결과 기록)                                      │
│                                                                     │
│   CPI 이상적 = 1.0 (한 클럭에 한 명령어 완료)                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    RISC vs CISC 구조 비교                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [RISC - Load/Store 아키텍처]                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  LOAD  R1, A      ; 메모리 → 레지스터                       │  │
│   │  LOAD  R2, B      ; 메모리 → 레지스터                       │  │
│   │  ADD   R3, R1, R2 ; 레지스터끼리 연산                       │  │
│   │  STORE R3, C      ; 레지스터 → 메모리                       │  │
│   └─────────────────────────────────────────────────────────────┘  │
│   특징: 메모리 접근과 연산이 분리됨                                │
│                                                                     │
│   [CISC - Memory-Memory 아키텍처]                                   │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  ADD  C, A, B     ; 메모리끼리 직접 연산                    │  │
│   │                   ; (내부적으로 여러 마이크로 오퍼레이션)    │  │
│   └─────────────────────────────────────────────────────────────┘  │
│   특징: 복잡한 명령어 하나가 여러 작업 수행                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 명령어 인출(IF) → ② 해독(ID) → ③ 실행(EX) → ④ 메모리 접근(MEM) → ⑤ 결과 기록(WB)
```

- **1단계 - IF**: 프로그램 카운터(PC)가 가리키는 명령어를 메모리에서 인출
- **2단계 - ID**: 명령어 해독, 레지스터 값 읽기, 분기 목적지 계산
- **3단계 - EX**: ALU에서 산술/논리 연산 수행 또는 주소 계산
- **4단계 - MEM**: Load/Store 명령어만 메모리 접근
- **5단계 - WB**: 연산 결과를 목적지 레지스터에 기록

**핵심 알고리즘/공식** (해당 시 필수):

```
[RISC 설계 원칙 ( Patterson & Hennessy )]

1. 단순성이 빠르다 (Simplicity favors regularity)
   - 고정 길이 명령어
   - 규칙적인 명령어 포맷

2. 작을수록 빠르다 (Smaller is faster)
   - 적은 수의 명령어
   - 빠른 디코딩

3. 좋은 설계는 좋은 타협을 필요로 한다
   - 명령어 세트의 균형

4. 일반적인 경우를 빠르게 (Make the common case fast)
   - 자주 쓰는 명령어 최적화

[RISC-V 기본 명령어 세트 (RV32I)]

R-type (레지스터-레지스터):
┌──────────────────────────────────────────────────────────────┐
│  funct7   │  rs2   │  rs1   │ funct3 │   rd   │  opcode   │
│  (7bit)   │ (5bit) │ (5bit) │ (3bit) │ (5bit) │  (7bit)   │
└──────────────────────────────────────────────────────────────┘
예: ADD rd, rs1, rs2  →  rd = rs1 + rs2

I-type (즉치값):
┌──────────────────────────────────────────────────────────────┐
│        imm12        │  rs1   │ funct3 │   rd   │  opcode   │
│       (12bit)       │ (5bit) │ (3bit) │ (5bit) │  (7bit)   │
└──────────────────────────────────────────────────────────────┘
예: ADDI rd, rs1, imm  →  rd = rs1 + imm

S-type (저장):
┌──────────────────────────────────────────────────────────────┐
│ imm[11:5] │  rs2   │  rs1   │ funct3 │imm[4:0]│  opcode   │
│  (7bit)   │ (5bit) │ (5bit) │ (3bit) │ (5bit) │  (7bit)   │
└──────────────────────────────────────────────────────────────┘
예: SW rs2, offset(rs1)  →  Memory[rs1+offset] = rs2

[CPI 계산]
CPI (Cycles Per Instruction) = 총 클럭 사이클 / 총 명령어 수

이상적 RISC CPI = 1.0
실제 CPI = 1 + 파이프라인 스톨 사이클

[성능 공식]
Execution Time = IC × CPI × Clock Cycle Time
IC: Instruction Count (명령어 수)
CPI: Cycles Per Instruction
Clock Cycle Time: 클럭 주기

RISC는 CPI 감소 → 성능 향상 (단, IC는 증가 가능)
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum, auto

class Opcode(Enum):
    # R-type
    ADD = 0x33
    SUB = 0x33
    AND = 0x33
    OR  = 0x33
    # I-type
    ADDI = 0x13
    ANDI = 0x13
    LW   = 0x03
    # S-type
    SW   = 0x23
    # B-type
    BEQ  = 0x63
    BLT  = 0x63
    # J-type
    JAL  = 0x6F

@dataclass
class Instruction:
    """RISC-V 명령어"""
    opcode: Opcode
    rd: int = 0       # 목적지 레지스터
    rs1: int = 0      # 소스 레지스터 1
    rs2: int = 0      # 소스 레지스터 2
    imm: int = 0      # 즉치값
    funct3: int = 0   # 기능 코드 3bit
    funct7: int = 0   # 기능 코드 7bit

class RISCVEmulator:
    """RISC-V RV32I 에뮬레이터"""

    def __init__(self):
        # 32개 범용 레지스터 (x0은 항상 0)
        self.registers: List[int] = [0] * 32
        # 메모리 (1MB)
        self.memory: bytearray = bytearray(1024 * 1024)
        # 프로그램 카운터
        self.pc: int = 0
        # 명령어 메모리
        self.instructions: List[Instruction] = []

    def fetch(self) -> Instruction:
        """IF 단계: 명령어 인출"""
        if self.pc // 4 < len(self.instructions):
            return self.instructions[self.pc // 4]
        return None

    def decode(self, instr: Instruction) -> Tuple[str, int, int, int]:
        """ID 단계: 명령어 해독"""
        if instr is None:
            return ("NOP", 0, 0, 0)

        # 레지스터 값 읽기
        rs1_val = self.registers[instr.rs1]
        rs2_val = self.registers[instr.rs2]

        op_name = instr.opcode.name
        return (op_name, rs1_val, rs2_val, instr.imm)

    def execute(self, op_name: str, rs1_val: int, rs2_val: int,
                imm: int) -> Tuple[int, bool, int]:
        """EX 단계: 실행"""
        result = 0
        branch_taken = False
        branch_target = 0

        if op_name == "ADD":
            result = (rs1_val + rs2_val) & 0xFFFFFFFF
        elif op_name == "SUB":
            result = (rs1_val - rs2_val) & 0xFFFFFFFF
        elif op_name == "AND":
            result = rs1_val & rs2_val
        elif op_name == "OR":
            result = rs1_val | rs2_val
        elif op_name == "ADDI":
            result = (rs1_val + imm) & 0xFFFFFFFF
        elif op_name == "ANDI":
            result = rs1_val & imm
        elif op_name == "BEQ":
            if rs1_val == rs2_val:
                branch_taken = True
                branch_target = self.pc + imm
        elif op_name == "BLT":
            # 부호 있는 비교
            if self._to_signed(rs1_val) < self._to_signed(rs2_val):
                branch_taken = True
                branch_target = self.pc + imm
        elif op_name == "LW":
            result = rs1_val + imm  # 주소 계산
        elif op_name == "SW":
            result = rs1_val + imm  # 주소 계산
        elif op_name == "JAL":
            branch_taken = True
            branch_target = self.pc + imm
            result = self.pc + 4  # 반환 주소

        return result, branch_taken, branch_target

    def memory_access(self, op_name: str, address: int, value: int) -> int:
        """MEM 단계: 메모리 접근"""
        if op_name == "LW":
            # 4바이트 로드 (little-endian)
            return (self.memory[address] |
                    (self.memory[address + 1] << 8) |
                    (self.memory[address + 2] << 16) |
                    (self.memory[address + 3] << 24))
        elif op_name == "SW":
            # 4바이트 스토어
            self.memory[address] = value & 0xFF
            self.memory[address + 1] = (value >> 8) & 0xFF
            self.memory[address + 2] = (value >> 16) & 0xFF
            self.memory[address + 3] = (value >> 24) & 0xFF
        return 0

    def write_back(self, instr: Instruction, result: int) -> None:
        """WB 단계: 결과 기록"""
        if instr and instr.rd != 0:  # x0은 항상 0
            self.registers[instr.rd] = result

    def step(self) -> bool:
        """한 명령어 실행 (5단계 파이프라인 시뮬레이션)"""
        # IF
        instr = self.fetch()
        if instr is None:
            return False

        # ID
        op_name, rs1_val, rs2_val, imm = self.decode(instr)

        # EX
        result, branch_taken, branch_target = self.execute(
            op_name, rs1_val, rs2_val, imm
        )

        # MEM
        if op_name in ("LW", "SW"):
            if op_name == "LW":
                result = self.memory_access(op_name, result, 0)
            else:
                self.memory_access(op_name, result, rs2_val)

        # WB
        if op_name not in ("SW", "BEQ", "BLT"):
            self.write_back(instr, result)

        # PC 갱신
        if branch_taken:
            self.pc = branch_target
        else:
            self.pc += 4

        return True

    def _to_signed(self, val: int) -> int:
        """32비트 부호 있는 정수로 변환"""
        if val >= 0x80000000:
            return val - 0x100000000
        return val

    def load_program(self, instructions: List[Instruction]) -> None:
        """프로그램 로드"""
        self.instructions = instructions
        self.pc = 0

    def run(self, max_cycles: int = 1000) -> int:
        """프로그램 실행"""
        cycles = 0
        while cycles < max_cycles and self.step():
            cycles += 1
        return cycles

    def print_registers(self) -> None:
        """레지스터 상태 출력"""
        print("=== Registers ===")
        for i in range(32):
            if self.registers[i] != 0:
                print(f"x{i}: {self.registers[i]}")

# 사용 예시
if __name__ == "__main__":
    cpu = RISCVEmulator()

    # 간단한 프로그램: 1 + 2 + 3 = 6
    program = [
        Instruction(Opcode.ADDI, rd=1, rs1=0, imm=1),    # x1 = 0 + 1 = 1
        Instruction(Opcode.ADDI, rd=2, rs1=0, imm=2),    # x2 = 0 + 2 = 2
        Instruction(Opcode.ADD, rd=3, rs1=1, rs2=2),     # x3 = x1 + x2 = 3
        Instruction(Opcode.ADDI, rd=4, rs1=3, imm=3),    # x4 = x3 + 3 = 6
    ]

    cpu.load_program(program)
    cycles = cpu.run()

    print(f"Executed in {cycles} cycles")
    cpu.print_registers()

    # 성능 분석
    print(f"\n=== Performance Analysis ===")
    print(f"Instructions: {len(program)}")
    print(f"Cycles: {cycles}")
    print(f"CPI: {cycles / len(program):.2f}")
    print(f"Ideal CPI for RISC: 1.0")
