+++
title = "명령어 포맷 (Instruction Format)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# 명령어 포맷 (Instruction Format)

## 핵심 인사이트 (3줄 요약)
1. 명령어 포맷(Instruction Format)은 기계어 명령어가 메모리에 저장되는 비트 구조로, Operation Code(Opcode)와 Operand(피연산자) 필드로 구성된다
2. Variable Length(가변 길이)와 Fixed Length(고정 길이) 포맷이 있으며, RISC는 고정 길이를, CISC는 가변 길이를 주로 사용한다
3. 기술사시험에서는 명령어 필드 구조, Opcode 배치, Operand 수, 주소 지정 필드가 핵심이다

## Ⅰ. 개요 (500자 이상)

명령어 포맷(Instruction Format)은 **기계어 명령어가 이진수로 메모리에 저장되는 형식**이다. CPU가 명령어를 해석하고 실행하기 위해 정해진 비트 배열 구조를 따른다.

```
명령어 포맷 기본 개념:
구조: Opcode + Operand(s)
길이: 16/32/64비트 등
유형: Fixed vs Variable

구성:
1. Opcode: 연산 코드
2. Operand: 피연산자 정보
   - Register Number
   - Address
   - Immediate Data
   - Addressing Mode

특징:
- CPU 아키텍처마다 상이
- 명령어 세트에 따라 다름
- 하드웨어 복잡도 결정
```

**명령어 포맷의 핵심 특징:**

1. **Opcode**: 연산 식별
2. **Operands**: 피연산자 정보
3. **Addressing Mode**: 데이터 위치 지정
4. **Length**: 명령어 비트 폭

```
RISC vs CISC 포맷:
RISC:
- 고정 길이 (32비트)
- 단순한 구조
- Register Operand

CISC:
- 가변 길이 (1-15바이트)
- 복잡한 구조
- Memory Operand
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 기본 포맷 구조

```
기본 명령어 포맷:

┌────────┬────────┬────────┬────────┐
│ Opcode │ Operand1 │ Operand2 │ Operand3│
└────────┴────────┴────────┴────────┘

구성:
1. Opcode (연산 코드):
   - 수행할 연산
   - 일반적으로 상위 비트

2. Operands (피연산자):
   - Source 1
   - Source 2
   - Destination

예 (3-Operand):
ADD R1, R2, R3
R3 ← R1 + R2
```

### 1-Operand 명령어

```
1-Operand 포맷:

┌────────┬────────┐
│ Opcode │ Operand │
└────────┴────────┘

예:
INC R1
R1 ← R1 + 1

JMP Label
PC ← Label

NOT R1
R1 ← ~R1

구조:
Opcode: 8비트
Operand: 24비트 (Register 또는 Address)
```

### 2-Operand 명령어

```
2-Operand 포맷:

┌────────┬────────┬────────┐
│ Opcode │   Src   │   Dest  │
└────────┴────────┴────────┘

또는:

┌────────┬────────┬────────┐
│ Opcode │   Dest  │   Src   │
└────────┴────────┴────────┘

예:
MOV R1, R2
R1 ← R2

SUB R1, R2
R1 ← R1 - R2

구조:
Opcode: 8비트
Src/Dest: 각 16비트 (레지스터)
```

### 3-Operand 명령어

```
3-Operand 포맷:

┌────────┬────────┬────────┬────────┐
│ Opcode │   R1    │   R2    │   R3    │
└────────┴────────┴────────┴────────┘

예:
ADD R1, R2, R3
R3 ← R1 + R2

MUL R1, R2, R3
R3 ← R1 × R2

구조:
Opcode: 8비트
R1, R2, R3: 각 8비트 (레지스터 번호)

장점:
- Load-Store 아키텍처
- RISC에서 주로 사용
- 단순한 디코딩
```

### Variable Length Format

```

가변 길이 포맷 (CISC):

명령어마다 길이가 다름

예 (x86):
1바이트: NOP
2바이트: INC AX
3바이트: JMP 0x1234
4바이트: MOV EAX, [EBX]
5바이트+: MOV EAX, [0x12345678]

형태:
[Prefix][Opcode][ModRM][SIB][Disp][Imm]

장점:
- 코드 밀도 높음
- 메모리 효율
- 디코딩 복잡

단점:
- 파이프라인 복잡
- 디코딩 시간
```

### Register-Based Format

```
레지스터 기반 포맷 (RISC):

┌────────┬──────┬──────┬──────┐
│ Opcode │  R1  │  R2  │  R3  │
└────────┴──────┴──────┴──────┘
      8      5      5      5

예 (MIPS):
R-format: OP R1, R2, R3

Opcode=0 (ADD)
R1=5 ($t0)
R2=6 ($t1)
R3=7 ($t2)

비트:
31-26: Opcode
25-21: R1
20-16: R2
15-11: R3
10-6:  Shift
5-0:  Function

이진: 000000 00101 00110 00111 00000 100000
```

### Memory-Based Format

```

메모리 기반 포맷:

┌────────┬────────┬────────┬────────┐
│ Opcode│   Base │ Index │  Disp  │
└────────┴────────┴────────┴────────┘

또는:

┌────────┬────────┬────────┬────────┐
│ Opcode│   Mode │   Reg  │  Addr  │
└────────┴────────┴────────┴────────┘

예 (Load/Store):
LB R1, 100(R2)
R1 ← Memory[R2 + 100]

구조:
Opcode: Load/Store
Mode: Addressing Mode
Reg: Destination Register
Addr: Base + Displacement
```

## Ⅲ. 융합 비교

### 포맷 길이

| 유형 | 길이 | 장점 | 단점 | 응용 |
|------|------|------|------|------|
| Fixed | 일정 | 디코딩 빠름 | 공간 낭비 | RISC |
| Variable | 가변 | 효율적 | 디코딩 복잡 | CISC |

### Operand 수

| 수 | 포맷 | 예시 | 장점 | 단점 |
|----|------|------|------|------|
| 0 | Opcode only | NOP | 단순 | 기능 제한 |
| 1 | Opcode + Op | INC | 일반적 | 오퍼랜드 |
| 2 | Opcode + 2 Op | MOV | 표준 | - |
| 3 | Opcode + 3 Op | ADD | Load-Store | 큰 포맷 |

### 아키텍처별 포맷

| 아키텍처 | 포맷 | 길이 | 특징 |
|----------|------|------|------|
| MIPS | Fixed | 32비트 | 3-Operand |
| ARM | Fixed | 32비트 | Cond. Code |
| x86 | Variable | 1-15B | ModR/M |
| RISC-V | Fixed | 32비트 | Compact |

## Ⅳ. 실무 적용 및 기술사적 판단

### MIPS R-Format

```
MIPS R-Format:

31 26 25 21 20 16 15 11 10 6 5   0
┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│Op│Rs│Rt│Rd│Sa│St│Fn│Cd│ 0  │
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

필드:
Op (6): Opcode (0=R-type)
Rs (5): Source Register
Rt (5): Source/Register
Rd (5): Destination Register
Sa (5): Shift Amount
St (5): Shift Type
Fn (6): Function
Cd (2): Condition Code

예:
ADD $t0, $t1, $t2
```

### x86 ModR/M

```
x86 ModR/M Byte:

7 6 5 4 3 2 1 0
┌─┬─┬───────────┬─┬─┬─┐
│Mo│Re│   Reg    │  │RM│ │
│d │g│           │  │  │Scla
│  │ │           │  │  │le

Mod (2): Addressing Mode
Reg (3): Register (or Opcode Ext)
R/M (3): Register/Memory
Scla: Scale (Index)

해석:
Mod=00, Reg=000: [EAX]
Mod=00, R/M=000: EAX
Mod=00, R/M=100: SIB
```

### ARM Cond

```
ARM Conditional Field:

31 28 27 24 23 20
┌────┬────┬────┬────┐
│Cond│Op │   │    │
└────┴────┴────┴────┘

Cond (4): Condition Code
0000: EQ (Equal)
0001: NE (Not Equal)
1010: GE (Greater or Equal)
1100: GT (Greater Than)
1110: AL (Always)

예:
ADDEQ R0, R1, R2
Only execute if Z=1
```

### VLIW Format

```

VLIW (Very Long Instruction Word):

┌───────┬───────┬───────┬───────┐
│ OP1   │ OP2   │ OP3   │ OP4   │
├───────┼───────┼───────┼───────┤
│ Src1  │ Src2  │ Src3  │ Src4  │
└───────┴───────┴───────┴───────┘

특징:
- 여러 명령어 병렬 실행
- Fixed Length
- Compiler dependency
- EPIC, IA-64
```

## Ⅴ. 기대효과 및 결론

명령어 포맷은 ISA를 결정한다. RISC는 단순한 고정 길이, CISC는 효율적인 가변 길이를 사용한다.

## 📌 관련 개념 맵

```
명령어 포맷
├── 구조
│   ├── Opcode
│   ├── Operands
│   └── Addressing Mode
├── 유형
│   ├── Fixed Length
│   │   └── RISC
│   └── Variable Length
│       └── CISC
├── 필드
│   ├── Condition Code
│   ├── Register Number
│   └── Immediate Data
└── 설계
    ├── 코드 밀도
    ├── 디코딩 속도
    └── 파이프라이닝
```

## 👶 어린이를 위한 3줄 비유 설명

1. 명령어 포맷은 명령어가 컴퓨터에 저장되는 형식이에요. Opcode는 무슨 일을 할지, Operand는 대상이 무엇인지 적어있어요
2. RISC는 모든 명령어가 같은 길이(32비트)를 가져서 간단하지만, CISC는 명령어마다 길이가 달라서 효율적이에요
3. 가변 길이 포맷은 짧은 명령어는 짧게, 긴 명령어는 길게 저장해서 메모리를 아껴지만, 해석하는 하드웨어가 더 복잡해져요
