+++
title = "명령어 세트 (Instruction Set)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# 명령어 세트 (Instruction Set)

## 핵심 인사이트 (3줄 요약)
1. 명령어 세트(Instruction Set)는 CPU가 이해하고 실행할 수 있는 명령어의 집합으로, ISA(Instruction Set Architecture)의 핵심 구성 요소다
2. 기술사시험에서는 명령어 분류(데이터 전송, 산술, 논리, 분기), 오퍼랜드 수, RISC vs CISC 특징이 핵심이다
3. CISC는 복잡한 다양한 명령어를, RISC는 단순한 적은 명령어를 지원하는 상반된 설계 철학을 가진다

## Ⅰ. 개요 (500자 이상)

명령어 세트(Instruction Set)는 **프로그래머가 CPU에 명령을 내리기 위해 사용하는 명령어의 집합이자, 하드웨어가 구현해야 할 명세**다. ISA(Instruction Set Architecture)의 가장 중요한 부분으로, 소프트웨어와 하드웨어의 계약 역할을 한다.

```
명령어 세트 기본 개념:
정의: CPU가 실행 가능한 명령어 집합
역할: SW-HW 인터페이스 명세
특징: 아키텍처마다 고유

구성 요소:
1. Opcode (연산 코드)
2. Operand (피연산자)
3. Addressing Mode (주소 지정)
4. Data Type (데이터 형태)

설계 목표:
- 성능: 빠른 명령어 실행
- 코드 크기: 작은 프로그램
- 구현 복잡도: 단순한 하드웨어
- 확장성: 미래 명령어 추가
```

**명령어 세트의 중요성:**

1. **소프트웨어 호환성**: 같은 ISA에서 실행 가능
2. **컴파일러 타겟**: 코드 생성 대상
3. **성능 결정**: 명령어 특성이 성능에 영향
4. **하드웨어 비용**: 구현 난이도 차이

```
ISA 설계 철학:
CISC (Complex Instruction Set Computer):
- 복잡한 명령어
- 메모리-메모리 연산
- 가변 길이 명령어
- x86, VAX

RISC (Reduced Instruction Set Computer):
- 단순한 명령어
- 레지스터-레지스터 연산
- 고정 길이 명령어
- MIPS, ARM, RISC-V
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 명령어 분류

```
명령어 유형:

1. Data Transfer (데이터 전송):
   - 레지스터 간 이동
   - 메모리 로드/스토어
   - 입출력 전송

   MOV AX, BX      ; 레지스터
   LOAD R1, 100(R2) ; 로드
   STORE R1, 100(R2) ; 스토어

2. Arithmetic (산술 연산):
   - 덧셈, 뺄셈, 곱셈, 나눗셈
   - 증가, 감소

   ADD R1, R2, R3  ; R3 = R1 + R2
   SUB R1, R2      ; R2 = R2 - R1
   MUL A, B        ; A = A × B
   DIV AX, BX      ; AX / BX

3. Logical (논리 연산):
   - AND, OR, XOR, NOT
   - Shift, Rotate

   AND R1, R2      ; R1 = R1 & R2
   OR R1, R2       ; R1 = R1 | R2
   SHL R1, 4       ; Left Shift
   ROR R1, 1       ; Rotate Right

4. Control Transfer (제어 전송):
   - 분기 (Jump/Branch)
   - 조건 분기
   - 호출/반환 (Call/Return)

   JMP Label       ; 무조건 분기
   BEQ R1, R2, L   ; R1==R2면 분기
   CALL Sub        ; 호출
   RET             ; 반환

5. System (시스템):
   - 특권 명령어
   - 시스템 콜
   - 컨텍스트 스위치

   INT 0x80        ; 시스템 콜
   HALT            ; 정지
   NOP             ; No Operation
```

### 오퍼랜드 수

```
오퍼랜드 수에 따른 분류:

0-Operand (Stack 기반):
PUSH operand1
PUSH operand2
ADD          ; stack.pop() + stack.pop()
POP result

장점: 코드 크기 작음
단점: 스택 접근 오버헤드

1-Operand (Accumulator 기반):
LOAD operand1
ADD operand2     ; ACC = ACC + operand2
STORE result

장점: 단순한 명령어
단점: 메모리 접근 빈번

2-Operand (1-Address 또는 2-Address):
MOV R1, operand1
ADD R1, operand2  ; R1 = R1 + operand2

장점: 레지스터 효율
단점: 피연산자 파괴

3-Operand (Load-Store):
ADD R1, R2, R3    ; R3 = R1 + R2

장점: 피연산자 보존
단점: 명령어 길이 길음
```

### 데이터 전송 명령어

```
Data Transfer Instructions:

Load (메모리 → 레지스터):
LW R1, 100(R2)    ; R1 ← Mem[R2+100]
LB R1, 10(R2)     ; Byte Load
LH R1, 20(R2)     ; Halfword Load

Store (레지스터 → 메모리):
SW R1, 100(R2)    ; Mem[R2+100] ← R1
SB R1, 10(R2)     ; Byte Store
SH R1, 20(R2)     ; Halfword Store

Move (레지스터 간):
MOV R1, R2        ; R1 ← R2
MVHI R1, 0x1000   ; High Immediate

Exchange (교환):
XCHG R1, R2       ; R1 ↔ R2

Memory-Memory (일부 CISC):
MOV [1000H], [2000H]  ; Mem[1000] ← Mem[2000]
```

### 산술 연산 명령어

```
Arithmetic Instructions:

Addition:
ADD R1, R2, R3    ; R3 = R1 + R2
ADDI R1, R2, 10   ; R1 = R2 + 10
ADC R1, R2        ; R1 = R1 + R2 + CF

Subtraction:
SUB R1, R2, R3    ; R3 = R1 - R2
SUBI R1, R2, 10   ; R1 = R2 - 10
SBB R1, R2        ; R1 = R1 - R2 - CF

Multiplication:
MUL R1, R2        ; AX = AL × R1 (8-bit)
IMUL R1, R2       ; Signed Multiply

Division:
DIV R1            ; AX = DX:AX / R1
IDIV R1           ; Signed Divide

Increment/Decrement:
INC R1            ; R1 = R1 + 1
DEC R1            ; R1 = R1 - 1

Negation:
NEG R1            ; R1 = -R1
```

### 논리 연산 명령어

```
Logical Instructions:

AND:
AND R1, R2, R3    ; R3 = R1 & R2
ANDI R1, R2, 0xFF ; R1 = R2 & 0xFF

OR:
OR R1, R2, R3     ; R3 = R1 | R2
ORI R1, R2, 0x0F  ; R1 = R2 | 0x0F

XOR:
XOR R1, R2, R3    ; R3 = R1 ^ R2
XORI R1, R2, 0xFF ; R1 = R2 ^ 0xFF

NOT:
NOT R1            ; R1 = ~R1

Test:
TEST R1, R2       ; R1 & R2, Flags만 설정
                 ; ZF, SF, PF 업데이트
```

### 시프트 명령어

```
Shift/Rotate Instructions:

Logical Shift:
SHL R1, R2, count ; R1 = R2 << count
SHR R1, R2, count ; R1 = R2 >> count (logical)

Arithmetic Shift:
SAL R1, R2, count ; R1 = R2 << count (signed)
SAR R1, R2, count ; R1 = R2 >> count (arithmetic)

Rotate:
ROL R1, R2, count ; Rotate Left
ROR R1, R2, count ; Rotate Right
RCL R1, R2, count ; Rotate through CF (Left)
RCR R1, R2, count ; Rotate through CF (Right)

예:
SHL EAX, 4        ; EAX = EAX × 16
SAR EDI, 1        ; EDI = EDI / 2 (signed)
```

### 분기 명령어

```
Branch/Control Flow Instructions:

Unconditional Jump:
JMP Label         ; PC ← Label
JR R1             ; PC ← R1

Conditional Branch:
BEQ R1, R2, Label ; if (R1==R2) PC ← Label
BNE R1, R2, Label ; if (R1≠R2) PC ← Label
BLT R1, R2, Label ; if (R1<R2) PC ← Label
BGT R1, R2, Label ; if (R1>R2) PC ← Label
BLE R1, R2, Label ; if (R1≤R2) PC ← Label
BGE R1, R2, Label ; if (R1≥R2) PC ← Label

Flag-based Branch:
JZ  Label         ; Jump if Zero (ZF=1)
JNZ Label         ; Jump if Not Zero
JC  Label         ; Jump if Carry (CF=1)
JNC Label         ; Jump if No Carry
JO  Label         ; Jump if Overflow
JNO Label         ; Jump if No Overflow
JS  Label         ; Jump if Sign (SF=1)
JNS Label         ; Jump if Not Sign

Call/Return:
CALL Subroutine   ; Push PC, Jump
RET               ; Pop PC
```

### 비교 명령어

```
Comparison Instructions:

Compare:
CMP R1, R2        ; R1 - R2 (Flags만)
CMPI R1, 10       ; R1 - 10 (Flags만)

Test:
TEST R1, R2       ; R1 & R2 (Flags만)

비교 후 분기:
CMP EAX, EBX
JGE greater       ; if EAX≥EBX jump

CISC Comparison:
CMP AX, BX
JG  greater       ; Jump if Greater
JLE less_equal    ; Jump if Less or Equal
```

## Ⅲ. 융합 비교

### CISC vs RISC

| 특성 | CISC | RISC |
|------|------|------|
| 명령어 | 복잡, 다양 | 단순, 적음 |
| 길이 | 가변 | 고정 |
| 오퍼랜드 | 메모리 가능 | 레지스터만 |
| CPI | 1-10+ | 1 |
| 코드 크기 | 작음 | 큼 |
| 하드웨어 | 복잡 | 단순 |
| 컴파일러 | 단순 | 복잡 |

### 아키텍처별 명령어 세트

| 아키텍처 | 유형 | 명령어 수 | 길이 | 특징 |
|----------|------|-----------|------|------|
| x86-64 | CISC | 1500+ | 1-15B | 호환성 중시 |
| ARMv8 | RISC | ~600 | 32-bit | Cond. 코드 |
| MIPS | RISC | ~100 | 32-bit | Load-Store |
| RISC-V | RISC | ~50 | 32-bit | 확장 가능 |

### 명령어 형식

| 형식 | 설명 | 예시 | 아키텍처 |
|------|------|------|----------|
| R | Register | ADD R1, R2, R3 | MIPS |
| I | Immediate | ADDI R1, R2, 10 | MIPS |
| J | Jump | J 0x1000 | MIPS |
| S | Store | SW R1, 10(R2) | MIPS |
| B | Branch | BEQ R1, R2, L | MIPS |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86-64 명령어 세트

```
x86-64 Instruction Groups:

1. General Purpose:
   - MOV, XCHG, PUSH, POP
   - ADD, SUB, MUL, DIV
   - AND, OR, XOR, NOT
   - SHL, SHR, SAR, ROL, ROR

2. Control Transfer:
   - JMP, JE, JNE, JG, JL
   - CALL, RET, IRET
   - LOOP, LOOPE, LOOPNE

3. String:
   - MOVS, CMPS, SCAS, LODS, STOS
   - REP, REPE, REPNE

4. System:
   - INT, IRET, CLI, STI
   - IN, OUT, INS, OUTS

5. SIMD (MMX, SSE, AVX):
   - MOVAPD, ADDPS, MULSD
   - VPADDD, VFMADD
```

### MIPS 명령어 세트

```
MIPS Instruction Formats:

R-Format (Register):
31-26 25-21 20-16 15-11 10-6 5-0
┌───┬────┬────┬────┬───┬─────┐
│Op │ Rs │ Rt │ Rd │Sa │Func │
└───┴────┴────┴────┴───┴─────┘

ADD $t0, $t1, $t2
Op=0, Rs=$t1, Rt=$t2, Rd=$t0, Func=ADD

I-Format (Immediate):
31-26 25-21 20-16 15--------0
┌───┬────┬────┬──────────┐
│Op │ Rs │ Rt │  Imm     │
└───┴────┴────┴──────────┘

ADDI $t0, $t1, 100
Op=ADDI, Rs=$t1, Rt=$t0, Imm=100

J-Format (Jump):
31-26 25----------------------0
┌───┬─────────────────────────┐
│Op │       Address           │
└───┴─────────────────────────┘

J 0x10000
Op=J, Address=0x10000>>2
```

### ARMv8 명령어 세트

```
ARMv8 Instruction Encoding:

31-28 27-24 23-20 19-16 15-12 11-0
┌────┬─────┬─────┬─────┬─────┬─────────┐
│Cond│ Op  │  Op │  Rt │  Rn │Imm12/Rm │
└────┴─────┴─────┴─────┴─────┴─────────┘

Conditional Execution:
ADDEQ R0, R1, R2    ; Execute if Z=1
ADDNE R0, R1, R2    ; Execute if Z=0

Data Processing:
ADD X0, X1, X2
SUB X0, X1, X2
AND X0, X1, X2

Load/Store:
LDR X0, [X1, #8]
STR X0, [X1, #8]
LDP X0, X1, [X2]    ; Load Pair
```

### 명령어 세트 확장

```
ISA Extensions:

x86 Extensions:
- MMX: 57 SIMD 명령어
- SSE: 70+ SIMD 명령어
- SSE2/3/4: 확장
- AVX/AVX2/AVX-512: 256/512-bit
- AES-NI: 암호화
- SGX: Secure Enclave

ARM Extensions:
- NEON: SIMD
- CRC: CRC32
- Crypto: AES, SHA
- SVE: Scalable Vector

RISC-V Extensions:
- M: Multiply/Divide
- A: Atomic
- F/D/Q: Floating Point
- C: Compressed (16-bit)
- V: Vector (1.0)
```

## Ⅴ. 기대효과 및 결론

명령어 세트는 CPU의 기능과 성능을 결정한다. CISC는 코드 밀도, RISC는 단순성과 파이프라이닝을 강조한다.

```python
"""
명령어 세트 시뮬레이션
Instruction Set Simulator
"""

class InstructionSet:
    """명령어 세트 추상화"""

    def __init__(self):
        self.registers = {f'R{i}': 0 for i in range(32)}
        self.memory = {}
        self.pc = 0
        self.flags = {'Z': 0, 'N': 0, 'C': 0, 'V': 0}

    def execute(self, opcode, *operands):
        """명령어 실행"""
        handler = getattr(self, f'op_{opcode.lower()}', None)
        if handler:
            return handler(*operands)
        raise ValueError(f"Unknown opcode: {opcode}")

    # Data Transfer
    def op_mov(self, dst, src):
        """MOV: 레지스터 전송"""
        if isinstance(src, str) and src.startswith('['):
            # Memory load
            addr = int(src[1:-1])
            self.registers[dst] = self.memory.get(addr, 0)
        else:
            # Register move
            self.registers[dst] = self.registers.get(src, src)
        self._update_flags(self.registers[dst])

    def op_load(self, dst, addr):
        """LOAD: 메모리 → 레지스터"""
        self.registers[dst] = self.memory.get(addr, 0)

    def op_store(self, src, addr):
        """STORE: 레지스터 → 메모리"""
        self.memory[addr] = self.registers[src]

    # Arithmetic
    def op_add(self, rd, rs1, rs2):
        """ADD: 덧셈"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        result = val1 + val2
        self.registers[rd] = result
        self._update_flags(result)
        return result

    def op_sub(self, rd, rs1, rs2):
        """SUB: 뺄셈"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        result = val1 - val2
        self.registers[rd] = result
        self._update_flags(result)
        return result

    def op_mul(self, rd, rs1, rs2):
        """MUL: 곱셈"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        result = val1 * val2
        self.registers[rd] = result
        self._update_flags(result)
        return result

    # Logical
    def op_and(self, rd, rs1, rs2):
        """AND: 논리곱"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        result = val1 & val2
        self.registers[rd] = result
        self._update_flags(result)
        return result

    def op_or(self, rd, rs1, rs2):
        """OR: 논리합"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        result = val1 | val2
        self.registers[rd] = result
        self._update_flags(result)
        return result

    def op_xor(self, rd, rs1, rs2):
        """XOR: 배타적 논리합"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        result = val1 ^ val2
        self.registers[rd] = result
        self._update_flags(result)
        return result

    # Shift
    def op_shl(self, rd, rs, amount):
        """SHL: 왼쪽 시프트"""
        val = self.registers.get(rs, rs)
        result = (val << amount) & 0xFFFFFFFF
        self.registers[rd] = result
        self._update_flags(result)
        return result

    def op_shr(self, rd, rs, amount):
        """SHR: 오른쪽 시프트"""
        val = self.registers.get(rs, rs)
        result = val >> amount
        self.registers[rd] = result
        self._update_flags(result)
        return result

    # Branch
    def op_jmp(self, target):
        """JMP: 무조건 분기"""
        old_pc = self.pc
        self.pc = target if isinstance(target, int) else self.registers.get(target, 0)
        return old_pc

    def op_beq(self, rs1, rs2, target):
        """BEQ: 같으면 분기"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        if val1 == val2:
            self.pc = target
            return True
        return False

    def op_blt(self, rs1, rs2, target):
        """BLT: 작으면 분기"""
        val1 = self.registers.get(rs1, rs1)
        val2 = self.registers.get(rs2, rs2)
        if val1 < val2:
            self.pc = target
            return True
        return False

    def _update_flags(self, result):
        """플래그 업데이트"""
        self.flags['Z'] = 1 if result == 0 else 0
        self.flags['N'] = 1 if result < 0 else 0


def demo_risc_vs_cisc():
    """RISC vs CISC 비교"""

    print("=" * 70)
    print("RISC vs CISC 명령어 세트 비교")
    print("=" * 70)

    # CISC 예제 (x86)
    print("\n### CISC (x86)")
    cisc_code = """
    MOV EAX, [1000H]    ; 메모리 → 레지스터
    ADD EAX, [1004H]    ; 메모리 직접 연산
    MOV [1008H], EAX    ; 결과 저장

    ; 3개 명령어, 3번 메모리 접근
    """
    print(cisc_code)

    # RISC 예제 (MIPS)
    print("\n### RISC (MIPS)")
    risc_code = """
    LW  $t0, 0($s0)     ; Load word
    LW  $t1, 4($s0)     ; Load word
    ADD $t2, $t0, $t1   ; 레지스터 연산만
    SW  $t2, 8($s0)     ; Store word

    ; 4개 명령어, Load-Store 구조
    """
    print(risc_code)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                       CISC              │         RISC              │
    ├─────────────────────────────────────────┼─────────────────────────────┤
    │ ADD EAX, [BX]          ; 1 명령어        │ ADD R1, R2, R3            │
    │                         │    ; 1 명령어              │
    │ 메모리-레지스터 연산     │    ; 레지스터만 연산          │
    │                         │                            │
    │ MOVSB                  ; 1 명령어        │ LB R1, 0(R2)              │
    │                         │    ; 1 명령어              │
    │ 문자열 자동 복사        │    ; 수동 루프 필요           │
    │                         │                            │
    │ 코드: 작음              │    ; 코드: 큼               │
    │ 명령어: 복잡            │    ; 명령어: 단순            │
    │ CPI: 1-10+              │    ; CPI: 1                  │
    │ 파이프라인: 어려움       │    ; 파이프라인: 쉬움         │
    └─────────────────────────────────────────┴─────────────────────────────┘
    """
    print(comparison)


def demo_instruction_formats():
    """명령어 형식 데모"""

    print("\n\n" + "=" * 70)
    print("명령어 형식 (Instruction Formats)")
    print("=" * 70)

    formats = """
    MIPS Instruction Formats:

    R-Format (Register Type):
    31 26 25 21 20 16 15 11 10 6 5   0
    ┌───┬────┬────┬────┬───┬─────┐
    │Op │ Rs │ Rt │ Rd │Sa │Func │
    └───┴────┴────┴────┴───┴─────┘
     6    5    5    5   5    6

    예: ADD $t0, $t1, $t2
    Op=0, Rs=$t1, Rt=$t2, Rd=$t0, Func=32

    I-Format (Immediate Type):
    31 26 25 21 20 16 15───────────────0
    ┌───┬────┬────┬──────────────────┐
    │Op │ Rs │ Rt │   Immediate      │
    └───┴────┴────┴──────────────────┘
     6    5    5          16

    예: LW $t0, 100($t1)
    Op=35, Rs=$t1, Rt=$t0, Imm=100

    J-Format (Jump Type):
    31 26 25───────────────────────────0
    ┌───┬─────────────────────────────┐
    │Op │        Address             │
    └───┴─────────────────────────────┘
     6              26

    예: J 0x10000
    Op=2, Address=0x10000>>2

    ─────────────────────────────────────────────────────────────────────

    x86 Instruction Format (Variable):

    [Prefix][Opcode][ModR/M][SIB][Disp][Imm]

    Prefix: 0-4 bytes (LOCK, REP, Segment)
    Opcode: 1-3 bytes
    ModR/M: 1 byte (Addressing mode)
    SIB: 0-1 byte (Scale-Index-Base)
    Disp: 0, 1, 2, 4, or 8 bytes
    Imm: 0, 1, 2, 4, or 8 bytes

    예: MOV EAX, [EBX+ECX*4+100]
    Opcode: 8B
    ModR/M: Encodes EBX+ECX*4+100
    SIB: Scale=2, Index=ECX, Base=EBX
    Disp: 100 (4 bytes)
    """
    print(formats)


def demo_instruction_execution():
    """명령어 실행 시뮬레이션"""

    print("\n\n" + "=" * 70)
    print("명령어 실행 시뮬레이션")
    print("=" * 70)

    isa = InstructionSet()

    # 초기화
    isa.registers['R1'] = 10
    isa.registers['R2'] = 20
    isa.memory[0x100] = 100
    isa.memory[0x104] = 200

    print("\n### 초기 상태")
    print(f"R1 = {isa.registers['R1']}")
    print(f"R2 = {isa.registers['R2']}")
    print(f"Memory[0x100] = {isa.memory[0x100]}")
    print(f"Memory[0x104] = {isa.memory[0x104]}")

    # 산술 연산
    print("\n### 산술 연산")
    print("ADD R3, R1, R2")
    isa.execute('ADD', 'R3', 'R1', 'R2')
    print(f"R3 = R1 + R2 = {isa.registers['R3']}")

    print("\nSUB R4, R2, R1")
    isa.execute('SUB', 'R4', 'R2', 'R1')
    print(f"R4 = R2 - R1 = {isa.registers['R4']}")

    # 논리 연산
    print("\n### 논리 연산")
    print("AND R5, R1, R2")
    isa.execute('AND', 'R5', 'R1', 'R2')
    print(f"R5 = R1 & R2 = {isa.registers['R5']}")

    # 시프트
    print("\n### 시프트 연산")
    print("SHL R6, R1, 2")
    isa.execute('SHL', 'R6', 'R1', 2)
    print(f"R6 = R1 << 2 = {isa.registers['R6']}")

    # 메모리
    print("\n### 메모리 연산")
    print("LOAD R7, 0x100")
    isa.execute('LOAD', 'R7', 0x100)
    print(f"R7 = Memory[0x100] = {isa.registers['R7']}")

    print("\nSTORE R7, 0x200")
    isa.execute('STORE', 'R7', 0x200)
    print(f"Memory[0x200] = {isa.memory.get(0x200, 'undefined')}")

    # 분기
    print("\n### 분기 연산")
    print("BEQ R1, R1, 0x1000")
    taken = isa.execute('BEQ', 'R1', 'R1', 0x1000)
    print(f"Branch taken: {taken}")

    print("\nBNE R1, R2, 0x2000")
    taken = isa.execute('BNE', 'R1', 'R2', 0x2000)
    print(f"Branch taken: {taken}")

    # 최종 상태
    print("\n### 최종 레지스터 상태")
    for i in range(8):
        print(f"R{i} = {isa.registers[f'R{i}']:6d}", end="  ")
        if i % 4 == 3:
            print()


if __name__ == '__main__':
    demo_risc_vs_cisc()
    demo_instruction_formats()
    demo_instruction_execution()
