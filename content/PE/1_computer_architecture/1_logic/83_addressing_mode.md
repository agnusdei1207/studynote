+++
title = "주소 지정 방식 (Addressing Mode)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# 주소 지정 방식 (Addressing Mode)

## 핵심 인사이트 (3줄 요약)
1. 주소 지정 방식(Addressing Mode)은 명령어가 피연산자의 위치를 지정하는 방법으로, Immediate/Direct/Register/Indirect/Indexed/Relative/Stack 등이 있다
2. 기술사시험에서는 각 방식의 특징, 유효 주소(EA, Effective Address) 계산 방법, 장단점 비교가 핵심이다
3. RISC는 Register/Immediate 위주, CISC는 다양한 Memory Addressing을 지원한다

## Ⅰ. 개요 (500자 이상)

주소 지정 방식(Addressing Mode)은 **CPU가 명령어를 실행할 때 피연산자(Operand)의 위치를 찾는 방법**이다. 명령어의 Opcode는 연산을 지정하지만, 실제 연산에 필요한 데이터가 어디에 있는지는 Addressing Mode가 결정한다.

```
주소 지정 방식 기본 개념:
정의: 피연산자 위치 지정 방법
목적: 코드 효율성, 유연성 제공
구성: Addressing Mode Field + Operand

유효 주소(Effective Address, EA):
실제 데이터가 있는 메모리 주소
계산: Base + Index × Scale + Displacement

분류:
1. Immediate: 데이터 자체
2. Register: 레지스터 번호
3. Direct: 메모리 주소
4. Indirect: 주소를 저장한 메모리
5. Indexed: 인덱스 레지스터 사용
6. Relative: PC 기준 오프셋
7. Stack: Stack Pointer 사용
8. Register Indirect: 레지스터가 주소 저장
```

**주소 지정 방식의 중요성:**

1. **코드 크기**: 적은 비트로 다양한 접근
2. **실행 속도**: 메모리 접근 최소화
3. **프로그래밍 편의성**: 다양한 데이터 구조 지원
4. **코드 밀도**: 짧은 명령어로 많은 기능

```
RISC vs CISC Addressing:
RISC (Load-Store):
- Register, Immediate만 지원
- 메모리 접근은 Load/Store만
- 단순한 EA 계산

CISC (Memory-to-Memory):
- 다양한 메모리 주소 지정
- 복잡한 EA 계산
- 짧은 코드 가능
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 1. Immediate Addressing

```
즉시 주소 지정:

데이터 자체가 명령어에 포함

┌────────┬──────────────┐
│ Opcode │   Immediate  │
│        │    Data      │
└────────┴──────────────┘

예:
MOV AX, 100    ; AX ← 100
ADD BX, 5      ; BX ← BX + 5

특징:
- 메모리 접근 불필요
- 가장 빠름
- 데이터 크기 제한
- 주로 상수에 사용

EA: 없음 (Operand 자체가 데이터)
```

### 2. Direct Addressing

```
직접 주소 지정:

명령어에 메모리 주소 포함

┌────────┬──────────────┐
│ Opcode │   Address    │
│        │   (Direct)   │
└────────┴──────────────┘

예:
MOV AX, [1000H]  ; AX ← Memory[1000H]
ADD BX, [2000H]  ; BX ← BX + Memory[2000H]

특징:
- 주소가 명령어에 직접 기록
- 메모리 접근 1회 필요
- 주소 공간 제한
- 정적 데이터 접근에 사용

EA: Address (명령어의 Operand 필드)
```

### 3. Register Addressing

```
레지스터 주소 지정:

피연산자가 레지스터에 존재

┌────────┬──────┬──────┐
│ Opcode │  R1  │  R2  │
└────────┴──────┴──────┘

예:
MOV AX, BX      ; AX ← BX
ADD CX, DX      ; CX ← CX + DX

특징:
- 메모리 접근 없음
- 가장 빠름 (Immediate 다음)
- 레지스터 개수 제한
- RISC에서 주로 사용

EA: 없음 (레지스터 직접 접근)
```

### 4. Register Indirect Addressing

```
레지스터 간접 주소 지정:

레지스터가 메모리 주소 저장

┌────────┬──────────┐
│ Opcode │ Register │
└────────┴──────────┘
        │
        ▼
    ┌───────┐
    │ Addr  │
    └───────┘
        │
        ▼
    Memory

예:
MOV AX, [BX]    ; AX ← Memory[BX]
ADD CX, [SI]    ; CX ← CX + Memory[SI]

특징:
- 포인터 연산에 사용
- 동적 데이터 접근
- 메모리 접근 1회
- 배열/구조체 접근에 유용

EA: [Register] (레지스터가 저장한 주소)
```

### 5. Indexed Addressing

```
인덱스 주소 지정:

Base + Index로 주소 계산

┌────────┬────────┬──────────┐
│ Opcode │  Base  │  Index   │
└────────┴────────┴──────────┘

EA = Base + Index

예:
MOV AX, [BX + SI]    ; AX ← Memory[BX + SI]
ADD CX, Array[DI]    ; CX ← CX + Memory[Array + DI]

특징:
- 배열 접근에 최적
- 2차원 배열 지원
- Base: 배열 시작
- Index: 요소 번호

변형:
Base + Index × Scale + Displacement
EA = Base + (Index × Scale) + Disp

예 (x86):
MOV EAX, [EBX + ECX*4 + 100]
; 4바이트 정수 배열 접근
```

### 6. Relative Addressing

```
상대 주소 지정:

현재 PC 기준 오프셋

┌────────┬──────────────┐
│ Opcode │   Offset     │
└────────┴──────────────┘
        │
        ▼
    PC + Offset

예:
JMP Label       ; PC ← PC + Offset
JE  Target      ; if Equal, PC ← PC + Offset

특징:
- 분기 명령에 사용
- 위치 독립적 코드(Position Independent)
- 짧은 오프셋으로 표현
- PIC(Position Independent Code)에 사용

EA: PC + Offset (상대적 계산)

장점:
- 코드 재배치 가능
- 메모리 관리 유연
- 공유 라이브러리 지원
```

### 7. Based Addressing

```
베이스 주소 지정:

Base Register + Displacement

┌────────┬──────────┬──────────┐
│ Opcode │   Base   │   Disp   │
└────────┴──────────┴──────────┘

EA = Base + Displacement

예:
MOV AX, [BX + 100]    ; AX ← Memory[BX + 100]
ADD CX, [BP + 50]     ; CX ← CX + Memory[BP + 50]

특징:
- 구조체 멤버 접근
- 스택 프레임 접근
- Base: 구조체 시작
- Disp: 멤버 오프셋

적용:
struct Student {
    int id;       // offset 0
    int age;      // offset 4
    int grade;    // offset 8
};

MOV EAX, [EBX + 8]  ; grade 접근
```

### 8. Auto-Increment/Decrement

```
자동 증가/감소 주소 지정:

접근 후 레지스터 자동 수정

Post-Increment:
MOV AX, [R1+]    ; AX ← Memory[R1], R1 ← R1 + 1

Pre-Decrement:
MOV AX, [-R1]    ; R1 ← R1 - 1, AX ← Memory[R1]

예 (VAX):
MOVL (R5)+, R0   ; Memory[R5] → R0, R5 ← R5 + 4

특징:
- 배열 순회에 최적
- Stack Push/Pop 자동화
- 루프 최적화
- VAX, PDP-11에서 사용

용도:
- 문자열 처리
- 배열 복사
- Stack 연산
- 루프 카운터
```

### 9. Memory-Indirect Addressing

```
메모리 간접 주소 지정:

메모리가 주소를 저장

┌────────┬──────────────┐
│ Opcode │   Address    │
└────────┴──────────────┘
        │
        ▼
    ┌───────┐
    │ Addr2 │
    └───────┘
        │
        ▼
    Data

예:
MOV AX, [[1000H]]  ; AX ← Memory[Memory[1000H]]

특징:
- 이중 포인터
- 동적 테이블 점프
- Jump Table 접근
- 메모리 접근 2회

EA: Memory[Address] (간접 참조)
```

### 10. Scaled Addressing

```
스케일 주소 지정:

Index × Scale + Base

EA = Base + (Index × Scale)

Scale: 1, 2, 4, 8 (데이터 크기)

예 (x86):
MOV EAX, [EBX + ECX*4]
; 정수 배열 접근

MOV AX, [EBX + ECX*2]
; Short 배열 접근

특징:
- 다양한 데이터 타입 지원
- 배열/행렬 연산 최적
- Scale은 2의 거듭제곱만
- x86에서 지원

데이터 크기별 Scale:
Byte:   1
Word:   2
DWord:  4
QWord:  8
```

## Ⅲ. 융합 비교

### 주소 지정 방식 비교

| 방식 | EA 계산 | 메모리 접근 | 속도 | 주요 용도 |
|------|---------|-------------|------|-----------|
| Immediate | 없음 | 0 | 최고 | 상수 |
| Register | 없음 | 0 | 최고 | 임시 변수 |
| Direct | Address | 1 | 빠름 | 전역 변수 |
| Register Indirect | [Reg] | 1 | 보통 | 포인터 |
| Indexed | Base+Index | 1 | 보통 | 배열 |
| Based | Base+Disp | 1 | 보통 | 구조체 |
| Relative | PC+Offset | 0-1 | 빠름 | 분기 |
| Memory Indirect | [Addr] | 2 | 느림 | 이중 포인터 |
| Auto-Inc/Dec | [Reg]± | 1 | 보통 | 문자열 |
| Scaled | Base+Idx*Scale | 1 | 보통 | 다차원 배열 |

### 아키텍처별 지원

| 아키텍처 | 지원 방식 | 특징 |
|----------|-----------|------|
| x86 | 전방위 | 복잡한 메모리 지정 |
| MIPS | Reg/Imm/Base | Load-Store만 |
| ARM | Reg/Imm/Indexed | Shifted Register |
| RISC-V | Reg/Imm | 단순화 |
| VAX | 전방위+Auto | 가장 다양함 |
| 68000 | 전방위 | 복잡한 Addressing |

### 속도 vs 유연성

| 방식 | 속도 | 코드 크기 | 유연성 | 복잡도 |
|------|------|-----------|--------|--------|
| Immediate | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |
| Register | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |
| Direct | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Indirect | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Indexed | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86 Addressing Mode Encoding

```
x86 ModR/M Byte:

7 6 5 4 3 2 1 0
┌──┬──┬───────────┐
│Mo│Re│   R/M     │
│d │g│           │
└──┴──┴───────────┘

Mod (2bit): Addressing Mode
00: Memory [R/M] (Disp=0)
01: Memory [R/M + Disp8]
10: Memory [R/M + Disp32]
11: Register Direct

Reg (3bit): Register
000: EAX
001: ECX
010: EDX
011: EBX
100: SIB Byte
101: EBP (or Disp32)
110: ESI
111: EDI

R/M (3bit): Register/Memory
(Reg와 동일한 코딩)
```

### MIPS Addressing Mode

```
MIPS (Load-Store):

지원 방식:
1. Register: operands in registers
   ADD $t0, $t1, $t2

2. Immediate: 16-bit constant
   ADDI $t0, $t1, 100

3. Base + Displacement: Load/Store only
   LW $t0, 100($t1)
   EA = Register + SignExtend(Imm)

4. PC-Relative: Branch only
   BEQ $t0, $t1, Label
   EA = PC + SignExtend(Imm) × 4

특징:
- Memory-to-Memory 없음
- Load/Store만 메모리 접근
- 단순하고 빠른 디코딩
```

### ARM Addressing Mode

```
ARMv8 Addressing:

1. Register:
   ADD X0, X1, X2

2. Immediate (12-bit):
   ADD X0, X1, #4095

3. Extended Register:
   ADD X0, X1, X2, LSL #2

4. Base + Offset:
   LDR X0, [X1, #8]

5. Pre-indexed:
   LDR X0, [X1, #8]!   ; X1 ← X1 + 8

6. Post-indexed:
   LDR X0, [X1], #8    ; X0 ← Mem[X1], X1 ← X1 + 8

7. PC-Relative:
   LDR X0, .LC0        ; Literal Pool

8. Register Pair:
   LDP X0, X1, [X2]    ; Load Pair
```

### Performance Considerations

```
주소 지정 방식 성능 분석:

1. 레지스터 사용:
   - 가장 빠름
   - 파이프라인 친화적
   - 레지스터 할당 최적화 필요

2. 메모리 접근 최소화:
   - Cache 활용
   - Loop Unrolling
   - Register Tiling

3. 복잡한 Addressing:
   - AGU (Address Generation Unit) 병목
   - μops 증가
   - 디코딩 지연

4. 코드 크기:
   - I-Cache 효율
   - Instruction Fetch
   - Code Density
```

### Compiler Optimization

```
컴파일러 최적화 기법:

1. Strength Reduction:
   × 4 → << 2 (Scale)
   × 8 → << 3
   곱셈을 시프트로 변환

2. Induction Variable:
   for (i=0; i<n; i++)
       a[i] = ...

   변환:
   ptr = &a[0];
   for (i=0; i<n; i++)
       *ptr++ = ...

   Auto-Increment 사용

3. Address Calculation:
   base + i*4 → base + (i << 2)

4. Loop Invariant:
   루프 내 변하지 않는 주소 계산
   외부로 이동
```

## Ⅴ. 기대효과 및 결론

주소 지정 방식은 ISA의 핵심 설계 요소다. RISC는 단순한 Register/Immediate를, CISC는 다양한 Memory Addressing을 지원한다.

```python
"""
주소 지정 방식 시뮬레이션
Addressing Mode Simulator
"""

class AddressingModeSimulator:
    """다양한 주소 지정 방식 시뮬레이션"""

    def __init__(self):
        # 레지스터 파일
        self.registers = {f'R{i}': 0 for i in range(16)}
        self.registers['PC'] = 0

        # 메모리 (256바이트)
        self.memory = [0] * 256

        # Flag 레지스터
        self.flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}

    def immediate_addressing(self, opcode, immediate):
        """
        즉시 주소 지정
        데이터가 명령어에 직접 포함
        """
        print(f"\n[Immediate] {opcode} {immediate}")
        print(f"  Operand = {immediate} (immediate value)")

        if opcode == 'MOV':
            self.registers['R0'] = immediate
        elif opcode == 'ADD':
            self.registers['R0'] += immediate

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def direct_addressing(self, opcode, address):
        """
        직접 주소 지정
        EA = Address (명령어에 직접 지정된 주소)
        """
        print(f"\n[Direct] {opcode} [{address}]")
        ea = address
        print(f"  EA = {address} (direct address)")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]
        elif opcode == 'ADD':
            self.registers['R0'] += self.memory[ea]

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def register_addressing(self, opcode, reg):
        """
        레지스터 주소 지정
        피연산자가 레지스터에 있음
        """
        print(f"\n[Register] {opcode} {reg}")
        print(f"  Data in {reg} = {self.registers[reg]}")
        print(f"  No memory access required")

        if opcode == 'MOV':
            self.registers['R0'] = self.registers[reg]
        elif opcode == 'ADD':
            self.registers['R0'] += self.registers[reg]

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def register_indirect_addressing(self, opcode, reg):
        """
        레지스터 간접 주소 지정
        EA = [Register] (레지스터가 주소를 저장)
        """
        print(f"\n[Register Indirect] {opcode} [{reg}]")
        ea = self.registers[reg]
        print(f"  {reg} = {ea} (holds address)")
        print(f"  EA = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]
        elif opcode == 'ADD':
            self.registers['R0'] += self.memory[ea]

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def indexed_addressing(self, opcode, base_reg, index_reg):
        """
        인덱스 주소 지정
        EA = Base + Index
        """
        print(f"\n[Indexed] {opcode} [{base_reg} + {index_reg}]")
        ea = self.registers[base_reg] + self.registers[index_reg]
        print(f"  Base = {self.registers[base_reg]} ({base_reg})")
        print(f"  Index = {self.registers[index_reg]} ({index_reg})")
        print(f"  EA = {self.registers[base_reg]} + {self.registers[index_reg]} = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]
        elif opcode == 'ADD':
            self.registers['R0'] += self.memory[ea]

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def based_addressing(self, opcode, base_reg, displacement):
        """
        베이스 주소 지정
        EA = Base + Displacement
        """
        print(f"\n[Based] {opcode} [{base_reg} + {displacement}]")
        ea = self.registers[base_reg] + displacement
        print(f"  Base = {self.registers[base_reg]} ({base_reg})")
        print(f"  Displacement = {displacement}")
        print(f"  EA = {self.registers[base_reg]} + {displacement} = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]
        elif opcode == 'ADD':
            self.registers['R0'] += self.memory[ea]

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def relative_addressing(self, offset, current_pc):
        """
        상대 주소 지정
        EA = PC + Offset
        """
        print(f"\n[Relative] JMP offset={offset}")
        print(f"  Current PC = {current_pc}")
        ea = current_pc + offset
        print(f"  EA = {current_pc} + {offset} = {ea}")
        print(f"  Jump to address {ea}")
        return ea

    def scaled_addressing(self, opcode, base_reg, index_reg, scale):
        """
        스케일 주소 지정
        EA = Base + (Index × Scale)
        """
        print(f"\n[Scaled] {opcode} [{base_reg} + {index_reg} × {scale}]")
        ea = self.registers[base_reg] + (self.registers[index_reg] * scale)
        print(f"  Base = {self.registers[base_reg]} ({base_reg})")
        print(f"  Index = {self.registers[index_reg]} ({index_reg})")
        print(f"  Scale = {scale}")
        print(f"  EA = {self.registers[base_reg]} + ({self.registers[index_reg]} × {scale}) = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]
        elif opcode == 'ADD':
            self.registers['R0'] += self.memory[ea]

        self._update_flags(self.registers['R0'])
        print(f"  R0 = {self.registers['R0']}")

    def auto_increment_addressing(self, opcode, reg):
        """
        자동 증가 주소 지정
        접근 후 레지스터 자동 증가
        """
        print(f"\n[Auto Increment] {opcode} [{reg}]+")
        ea = self.registers[reg]
        print(f"  {reg} = {ea} (before access)")
        print(f"  EA = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]

        self.registers[reg] += 1
        print(f"  {reg} ← {ea} + 1 = {self.registers[reg]} (after increment)")
        print(f"  R0 = {self.registers['R0']}")

    def auto_decrement_addressing(self, opcode, reg):
        """
        자동 감소 주소 지정
        접근 전 레지스터 자동 감소
        """
        print(f"\n[Auto Decrement] {opcode} [-{reg}]")
        print(f"  {reg} = {self.registers[reg]} (before access)")

        self.registers[reg] -= 1
        ea = self.registers[reg]

        print(f"  {reg} ← {self.registers[reg] + 1} - 1 = {ea} (after decrement)")
        print(f"  EA = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]

        print(f"  R0 = {self.registers['R0']}")

    def memory_indirect_addressing(self, opcode, address):
        """
        메모리 간접 주소 지정
        EA = Memory[Address]
        """
        print(f"\n[Memory Indirect] {opcode} [[{address}]]")
        indirect_addr = self.memory[address]
        print(f"  Memory[{address}] = {indirect_addr} (holds the target address)")
        ea = indirect_addr
        print(f"  EA = Memory[{address}] = {ea}")
        print(f"  Memory[{ea}] = {self.memory[ea]}")

        if opcode == 'MOV':
            self.registers['R0'] = self.memory[ea]

        print(f"  R0 = {self.registers['R0']}")
        print(f"  (Two memory accesses required)")

    def _update_flags(self, result):
        """플래그 레지스터 업데이트"""
        self.flags['Z'] = 1 if result == 0 else 0
        self.flags['N'] = 1 if result < 0 else 0

    def set_memory(self, address, value):
        """메모리 설정"""
        self.memory[address % 256] = value

    def set_register(self, reg, value):
        """레지스터 설정"""
        self.registers[reg] = value

    def dump_state(self):
        """현재 상태 출력"""
        print("\n=== Processor State ===")
        print("Registers:")
        for i in range(8):
            print(f"  R{i:2d} = {self.registers[f'R{i}']:4d}", end="")
            if i % 4 == 3:
                print()
        print(f"\nFlags: Z={self.flags['Z']} C={self.flags['C']} N={self.flags['N']} V={self.flags['V']}")
        print("\nMemory (selected):")
        for i in [0, 16, 32, 48, 64, 80, 96, 112]:
            values = self.memory[i:i+16]
            print(f"  [{i:3d}]: {' '.join(f'{v:3d}' for v in values)}")


def demo_addressing_modes():
    """주소 지정 방식 데모"""

    print("=" * 70)
    print("주소 지정 방식 (Addressing Mode) 시뮬레이션")
    print("=" * 70)

    sim = AddressingModeSimulator()

    # 메모리 초기화
    for i in range(16):
        sim.set_memory(i, i * 10)
        sim.set_memory(100 + i, i * 100)
        sim.set_memory(200 + i, i * 7)

    # 1. Immediate Addressing
    print("\n### 1. Immediate Addressing (즉시 주소 지정)")
    print("데이터가 명령어에 직접 포함됨")
    sim.set_register('R0', 0)
    sim.immediate_addressing('MOV', 42)
    sim.immediate_addressing('ADD', 10)

    # 2. Register Addressing
    print("\n### 2. Register Addressing (레지스터 주소 지정)")
    print("피연산자가 레지스터에 있음 - 가장 빠름")
    sim.set_register('R0', 0)
    sim.set_register('R5', 100)
    sim.register_addressing('MOV', 'R5')

    sim.set_register('R0', 50)
    sim.set_register('R6', 25)
    sim.register_addressing('ADD', 'R6')

    # 3. Direct Addressing
    print("\n### 3. Direct Addressing (직접 주소 지정)")
    print("명령어에 메모리 주소가 직접 포함됨")
    sim.set_register('R0', 0)
    sim.direct_addressing('MOV', 100)

    # 4. Register Indirect Addressing
    print("\n### 4. Register Indirect Addressing (레지스터 간접 주소 지정)")
    print("레지스터가 메모리 주소를 저장함")
    sim.set_register('R0', 0)
    sim.set_register('R7', 100)
    sim.register_indirect_addressing('MOV', 'R7')

    # 5. Indexed Addressing
    print("\n### 5. Indexed Addressing (인덱스 주소 지정)")
    print("Base + Index로 주소 계산 - 배열 접근에 사용")
    sim.set_register('R0', 0)
    sim.set_register('R8', 100)  # Base
    sim.set_register('R9', 5)    # Index
    sim.indexed_addressing('MOV', 'R8', 'R9')

    # 6. Based Addressing
    print("\n### 6. Based Addressing (베이스 주소 지정)")
    print("Base + Displacement - 구조체 멤버 접근에 사용")
    sim.set_register('R0', 0)
    sim.set_register('R10', 100)  # Base
    sim.based_addressing('MOV', 'R10', 5)  # Offset 5

    # 7. Scaled Addressing
    print("\n### 7. Scaled Addressing (스케일 주소 지정)")
    print("Base + (Index × Scale) - 다양한 데이터 타입 배열")
    sim.set_register('R0', 0)
    sim.set_register('R11', 100)  # Base
    sim.set_register('R12', 3)    # Index
    sim.scaled_addressing('MOV', 'R11', 'R12', 4)  # Scale 4 (int)

    # 8. Auto Increment
    print("\n### 8. Auto Increment Addressing (자동 증가 주소 지정)")
    print("접근 후 레지스터 자동 증가 - 문자열 처리에 사용")
    sim.set_register('R0', 0)
    sim.set_register('R13', 200)
    sim.auto_increment_addressing('MOV', 'R13')
    sim.auto_increment_addressing('MOV', 'R13')

    # 9. Auto Decrement
    print("\n### 9. Auto Decrement Addressing (자동 감소 주소 지정)")
    print("접근 전 레지스터 자동 감소 - Stack Push에 사용")
    sim.set_register('R0', 0)
    sim.set_register('R14', 210)
    sim.auto_decrement_addressing('MOV', 'R14')
    sim.auto_decrement_addressing('MOV', 'R14')

    # 10. Memory Indirect
    print("\n### 10. Memory Indirect Addressing (메모리 간접 주소 지정)")
    print("메모리가 주소를 저장 - Jump Table 접근에 사용")
    sim.set_register('R0', 0)
    sim.set_memory(50, 205)  # 주소 50에 205를 저장
    sim.memory_indirect_addressing('MOV', 50)

    # 11. Relative Addressing
    print("\n### 11. Relative Addressing (상대 주소 지정)")
    print("PC + Offset - 분기 명령에 사용")
    pc = 1000
    new_pc = sim.relative_addressing(50, pc)

    # 최종 상태 출력
    sim.dump_state()


def demo_array_access():
    """배열 접근 시뮬레이션"""

    print("\n\n" + "=" * 70)
    print("배열 접근 방식 비교")
    print("=" * 70)

    sim = AddressingModeSimulator()

    # 배열 초기화: arr[0..9] = {0, 10, 20, ..., 90}
    for i in range(10):
        sim.set_memory(100 + i * 4, i * 10)  # int 배열 (4바이트)

    print("\nint arr[10] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90};")
    print("배열 시작 주소: 100")

    # 1. Direct Addressing (고정 인덱스)
    print("\n### Direct: arr[3] 접근")
    sim.set_register('R0', 0)
    sim.direct_addressing('MOV', 112)  # 100 + 3*4

    # 2. Register Indirect (단일 포인터)
    print("\n### Register Indirect: 포인터로 접근")
    sim.set_register('R0', 0)
    sim.set_register('R1', 112)  # &arr[3]
    sim.register_indirect_addressing('MOV', 'R1')

    # 3. Indexed (배열 순회)
    print("\n### Indexed: 배열 순회")
    sim.set_register('R8', 100)  # Base
    for i in range(5):
        sim.set_register('R0', 0)
        sim.set_register('R9', i)
        sim.indexed_addressing('MOV', 'R8', 'R9')

    # 4. Scaled (타입 크기 고려)
    print("\n### Scaled: 4바이트 int 배열")
    sim.set_register('R0', 0)
    sim.set_register('R11', 100)  # Base
    sim.set_register('R12', 7)    # Index = 7
    sim.scaled_addressing('MOV', 'R11', 'R12', 4)  # Scale = 4

    # 5. Auto Increment (순차 접근)
    print("\n### Auto Increment: 배열 순차 복사")
    sim.set_register('R13', 100)  # 소스
    values = []
    for i in range(5):
        sim.set_register('R0', 0)
        sim.auto_increment_addressing('MOV', 'R13')
        values.append(sim.registers['R0'])
    print(f"  Copied values: {values}")


def demo_performance_comparison():
    """성능 비교"""

    print("\n\n" + "=" * 70)
    print("주소 지정 방식 성능 비교")
    print("=" * 70)

    comparison = """
    ┌────────────────────────┬──────────┬──────────┬──────────┬─────────┐
    │ Addressing Mode        │ Speed    │ Code Size│ Flex     │ Complex │
    ├────────────────────────┼──────────┼──────────┼──────────┼─────────┤
    │ Immediate              │ ★★★★★   │ ★★      │ ★        │ ★       │
    │ Register               │ ★★★★★   │ ★★      │ ★★       │ ★       │
    │ Direct                 │ ★★★★    │ ★★★     │ ★★       │ ★★      │
    │ Register Indirect      │ ★★★     │ ★★★     │ ★★★★     │ ★★★     │
    │ Indexed                │ ★★★     │ ★★★★    │ ★★★★★    │ ★★★     │
    │ Based                  │ ★★★     │ ★★★     │ ★★★★     │ ★★★     │
    │ Relative               │ ★★★★    │ ★★★     │ ★★★      │ ★★      │
    │ Memory Indirect        │ ★★      │ ★★★     │ ★★★★★    │ ★★★★    │
    │ Auto Inc/Dec           │ ★★★     │ ★★★     │ ★★★★     │ ★★★     │
    │ Scaled                 │ ★★★     │ ★★★★    │ ★★★★★    │ ★★★     │
    └────────────────────────┴──────────┴──────────┴──────────┴─────────┘

    사이클 수 (대략적):
    - Immediate:     1 cycle
    - Register:      1 cycle
    - Direct:        2-3 cycles (1 mem access)
    - Reg Indirect:  2-3 cycles (1 mem access)
    - Indexed:       3-4 cycles (1 mem + calc)
    - Memory Indirect: 4-6 cycles (2 mem access)

    RISC vs CISC:
    ┌────────────────────────────────┬──────────────────────┬─────────────────────┐
    │                                │ RISC                 │ CISC                │
    ├────────────────────────────────┼──────────────────────┼─────────────────────┤
    │ 주요 Addressing Mode           │ Register, Immediate  │ 전방위 지원          │
    │ 메모리 접근                    │ Load/Store만         │ 명령어마다 가능      │
    │ EA 계산                         │ 단순 (Base+Disp)     │ 복잡 (Scale*Index)  │
    │ 디코딩 속도                     │ 빠름                 │ 느림                │
    │ 코드 크기                       │ 큼                   │ 작음                │
    │ 파이프라이닝                    │ 유리                 │ 불리                │
    └────────────────────────────────┴──────────────────────┴─────────────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_addressing_modes()
    demo_array_access()
    demo_performance_comparison()
