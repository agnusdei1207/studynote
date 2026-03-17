+++
title = "CISC 명령어 세트 (CISC Instruction Set)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# CISC 명령어 세트 (CISC Instruction Set)

## 핵심 인사이트 (3줄 요약)
1. CISC(Complex Instruction Set Computer)는 복잡하고 강력한 명령어를 지원하여 코드 크기를 줄이고 메모리 접근을 최소화하는 설계 철학이다
2. 기술사시험에서는 x86 명령어 형식, Microcode 구조, Memory-to-Memory 연산, String 명령어가 핵심이다
3. 현대 x86-64는 내부적으로 RISC 마이크로연산으로 변환하여 실행하는 하이브리드 구조다

## Ⅰ. 개요 (500자 이상)

CISC(Complex Instruction Set Computer)는 **복잡하고 다양한 명령어를 제공하여 하나의 명령어로 여러 작업을 수행하고, 메모리와 레지스터 간의 직접 연산을 지원하는 명령어 세트 아키텍처**다. 1970년대 IBM System/360, VAX, x86 등에서 개발되었다.

```
CISC 설계 목표:
1. 코드 크기 최소화 (메모리 비쌌음)
2. 프로그래머 편의성 (고수준 언어 대체)
3. 컴파일러 단순화 (복잡한 명령어)
4. 메모리 접근 감소 (Memory-Memory 연산)

핵심 특징:
- 가변 길이 명령어 (1-15바이트)
- 복잡한 Addressing Mode
- Memory-to-Memory 연산
- Microcode 구현
- 강력한 String 명령어

장점:
- 작은 코드 크기
- 적은 명령어 수
- 복잡한 작업 한 명령어로

단점:
- 명령어 실행 시간 불균일
- 파이프라이닝 어려움
- 하드웨어 복잡도 높음
- 전력 소모 큼
```

**CISC의 역사적 배경:**

```
1950-60년대:
- 메모리 비쌈 → 코드 크기 중요
- 어셈블리 주도 → 복잡한 명령어 필요

1970년대:
- IBM System/360 (CISC 선구)
- VAX-11 (DEC, 완벽한 CISC)
- Intel 8086 (x86 탄생)

1980-90년대:
- x86 확장 (80286, 80386, 80486)
- RISC 도전에 맞서 Microcode 도입

2000년대 이후:
- x86-64 (AMD64)
- 내부적으로 마이크로연산으로 변환
- CISC 명령어 → RISC 내부 실행
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### x86 명령어 형식

```
x86 Instruction Format:

┌──────┬──────┬───────┬─────┬──────┬─────┐
│Prefix│Opcode│ ModRM │ SIB │Disp  │ Imm │
└──────┴──────┴───────┴─────┴──────┴─────┘
 0-4B   1-3B   0-1B   0-1B  0-8B   0-8B

Prefix (선택):
- LOCK: 0xF0 (Atomic 연산)
- REP: 0xF3 (Repeat)
- REPE/REPNE: 0xF3 (String)
- Segment override: 0x2E, 0x36, 0x3E, 0x26, 0x64, 0x65
- Operand size: 0x66 (16/32-bit toggle)
- Address size: 0x67 (16/32-bit toggle)

Opcode (필수):
- 1-3바이트
- 기본 연산 정의

ModR/M (Addressing Mode):
7 6 5 4 3 2 1 0
┌──┬──┬───────────┐
│Mo│Re│   R/M     │
│d │g│           │
└──┴──┴───────────┘
Mod(2): Addressing mode
Reg(3): Register/Opcode extension
R/M(3): Register/Memory

SIB (Scale-Index-Base):
7 6 5 4 3 2 1 0
┌───┬──────┬───────────┐
│Sc │Index│  Base     │
│ale│      │           │
└───┴──────┴───────────┘
Scale(2): 1, 2, 4, 8
Index(3): Index register
Base(3): Base register

Displacement (선택):
- 0, 1, 2, 4, 8바이트
- 주소 계산용 오프셋

Immediate (선택):
- 0, 1, 2, 4, 8바이트
- 즉시값
```

### Memory-to-Memory 연산

```
직접 메모리 연산:

RISC와 달리 메모리 간 직접 연산 가능

MOV EAX, [EBX]     ; 메모리 → 레지스터
ADD EAX, [ECX]     ; 메모리 + 레지스터
MOV [EDX], EAX     ; 레지스터 → 메모리

CISC 특유:
ADD [EBX], EAX     ; 메모리 직접 수정
                   ; Mem[EBX] += EAX

CMP [EDI], 0       ; 메모리 직접 비교

장점:
- Load/Store 명령어 불필요
- 코드 간결

단점:
- 메모리 접근 시간 예측 어려움
- 파이프라인 방해
```

### String 명령어

```
x86 String Instructions:

MOVSB/MOVSW/MOVSD:
- DS:[ESI] → ES:[EDI]
- ESI, EDI 자동 증가/감소
- DF(Direction Flag) 따름

예:
MOVSB           ; Byte 복사
MOVSW           ; Word 복사
MOVSD           ; Dword 복사

REP MOVSB       ; ECX 만큼 반복
; while (ECX-- > 0)
;     ES:[EDI++] = DS:[ESI++]

CMPSB/CMPSW/CMPSD:
- DS:[ESI] - ES:[EDI]
- 비교 결과를 Flags에
- ZF, SF, PF 업데이트

REPZ CMPSB      ; 같으면 계속
REPNZ CMPSB     ; 다르면 계속

SCASB/SCASW/SCASD:
- AL/AX/EAX - ES:[EDI]
- 스캔 결과 Flags에

REPNE SCASB     ; 다를 때까지 스캔

LODSB/LODSW/LODSD:
- DS:[ESI] → AL/AX/EAX
- ESI 자동 증가/감소

STOSB/STOSW/STOSD:
- AL/AX/EAX → ES:[EDI]
- EDI 자동 증가/감소

REP STOSB       ; 메모리 채우기
; 예: memset() 구현
```

### Complex Addressing

```
x86 Addressing Modes:

1. Register:
   MOV EAX, EBX

2. Immediate:
   MOV EAX, 100

3. Direct:
   MOV EAX, [0x1000]

4. Register Indirect:
   MOV EAX, [EBX]

5. Register Displacement:
   MOV EAX, [EBX+100]

6. Base + Index:
   MOV EAX, [EBX+ESI]

7. Scale * Index + Displacement:
   MOV EAX, [ESI*4+100]

8. Base + Scale*Index + Displacement:
   MOV EAX, [EBX+ESI*4+100]

복잡한 예:
MOV EAX, [EBX+ECX*8+0x1000]

계산:
EA = EBX + (ECX × 8) + 0x1000

용도:
- 구조체 멤버 접근
- 배열 인덱싱
- 다차원 배열
```

### Microcode 구조

```
Microcode Architecture:

CISC 명령어 → Microcode → Micro-ops

복잡한 CISC 명령어는 내부적으로
단순한 RISC-style 마이크로연산으로 분해

예: string 명령어
REP MOVSB → Micro-ops:
  1. Check ECX
  2. If ECX==0, done
  3. Load byte from [DS:ESI]
  4. Store byte to [ES:EDI]
  5. ESI += DF
  6. EDI += DF
  7. ECX--
  8. Loop to 1

이점:
- 복잡한 명령어 지원
- 내부 RISC 단순화
- 파이프라인 효율

Intel Micro-op Fusion:
- 여러 마이크로연산을 하나로 결합
- Decoding 오버헤드 감소
- Trace Cache 활용
```

### CISC 명령어 예제

```
1. LOOP (복합 명령어):
LOOP Label
; ECX--
; if (ECX != 0) JMP Label

RISC로 변환:
DEC ECX
JNZ Label

2. ENTER (Stack Frame):
ENTER 16, 0    ; Stack Frame 생성
; PUSH BP
; MOV BP, SP
; SP -= 16

3. LEAVE (Stack Frame 정리):
LEAVE
; SP = BP
; POP BP

4. XLAT (Lookup Table):
XLAT            ; AL = DS:[BX+AL]
; 테이블 변환에 사용

5. RDTSC (Time Stamp Counter):
RDTSC
; EDX:EAX = TSC
; 고해상도 타이머

6. CPUID (CPU Identification):
CPUID
; 프로세서 정보 반환

7. CMPXCHG (Compare and Exchange):
CMPXCHG dest, source
; if (EAX == dest)
;     dest = source, ZF=1
; else
;     EAX = dest, ZF=0
; Atomic 연산 기반

8. LOCK (Atomic Prefix):
LOCK ADD [mem], EAX
; 원자적 추가
; Multiprocessor 안전
```

## Ⅲ. 융합 비교

### CISC vs RISC

| 특성 | CISC | RISC |
|------|------|------|
| 명령어 | 복잡, 다양 | 단순, 적음 |
| 길이 | 가변 (1-15B) | 고정 (4B) |
| CPI | 1-10+ | 1 |
| 코드 크기 | 작음 | 큼 |
| 파이프라인 | 어려움 | 쉬움 |
| Addressing | 복잡 | 단순 |
| 하드웨어 | Microcode | Hardwired |

### x86 vs ARM 명령어

| 작업 | x86 (CISC) | ARM (RISC) |
|------|------------|------------|
| 복사 | MOV | MOV |
| 더하기 | ADD | ADD |
| 문자열 복사 | REP MOVSB | Loop + LDR/STR |
| Stack | PUSH/POP | PUSH/POP |
| 조건부 | Jcc | 조건 코드 포함 |

### 아키텍처별 CISC

| 아키텍처 | 시대 | 명령어 수 | 특징 |
|----------|------|-----------|------|
| IBM/360 | 1960s | ~100 | 초기 CISC |
| VAX-11 | 1970s | ~300 | 완벽한 CISC |
| x86 | 1978- | 1500+ | 가장 널리 사용 |
| M68k | 1980s | ~1000 | 직관적 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 현대 x86-64 내부 구조

```
x86-64 Microarchitecture:

Front End:
1. Instruction Fetch
2. Pre-decode
3. Instruction Queue
4. Decoder (x86 → μops)

Back End:
5. μop Queue
6. Register Renaming
7. Reorder Buffer
8. Reservation Stations
9. Execution Units
10. Retirement

Decoder:
- Simple Decoder: 1 μop (4개 병렬)
- Vector Decoder: 1-4 μops (1개)
- Microcode Sequencer: 복잡한 명령어

μop Examples:
MOV EAX, [EBX]     → 1 μop
ADD EAX, EBX       → 1 μop
REP MOVSB          → 여러 μops
MUL EAX            → 3 μops
```

### 성능 최적화

```
CISC 코드 최적화:

1. 단순 명령어 선호:
   ; 나쁨:
   LOOP Label
   ; 좋음:
   DEC ECX
   JNZ Label

2. String 명령어 활용:
   REP MOVSD      ; 빠른 메모리 복사
   REP STOSB      ; 빠른 메모리 초기화

3. 복잡한 명령어 피하기:
   ; 나쁨:
   ENTER 100, 0   ; 느림
   ; 좋음:
   PUSH EBP
   MOV EBP, ESP
   SUB ESP, 100

4. LEA 활용:
   LEA EAX, [EBX+ECX*4+100]  ; 주소 계산만
```

### 호환성 문제

```
x86 하위 호환성:

1978: 8086 (16-bit)
1985: 80386 (32-bit)
2003: AMD64 (64-bit)

모든 x86-64 프로세서는:
- 실제 모드 (8086 호환)
- 보호 모드 (80386)
- 롱 모드 (64-bit)

레거시 명령어:
- AAA, AAS, AAM, AAD (BCD)
- AAM, AAD (adjust)
- LOOP, LOOPE, LOOPNE
- ENTER, LEAVE

최적 프로세서에서도 지원:
- 호환성 유지
- 성능은 느림
```

## Ⅴ. 기대효과 및 결론

CISC는 코드 크기와 프로그래밍 편의성을 강조한다. 현대 x86은 내부적으로 RISC 마이크로연산으로 변환하여 성능을 확보한다.

```python
"""
CISC 명령어 세트 시뮬레이션
CISC Instruction Set Simulator
"""

class CISC_Simulator:
    """CISC 명령어 세트 시뮬레이션"""

    def __init__(self):
        # 레지스터
        self.regs = {f'R{i}': 0 for i in range(16)}
        self.regs.update({
            'EAX': 0, 'EBX': 0, 'ECX': 0, 'EDX': 0,
            'ESI': 0, 'EDI': 0, 'EBP': 0, 'ESP': 0x1000,
            'EIP': 0
        })

        # 세그먼트 레지스터
        self.segs = {'CS': 0, 'DS': 0, 'ES': 0, 'SS': 0}

        # 플래그
        self.flags = {'CF': 0, 'PF': 0, 'AF': 0, 'ZF': 0, 'SF': 0, 'TF': 0, 'IF': 0, 'DF': 0, 'OF': 0}

        # 메모리
        self.memory = {}

    def execute(self, instruction):
        """명령어 실행"""
        parts = instruction.split()
        opcode = parts[0].upper()
        operands = [p.rstrip(',') for p in parts[1:]] if len(parts) > 1 else []

        handler = getattr(self, f'op_{opcode.lower()}', None)
        if handler:
            return handler(*operands)
        else:
            print(f"  [Unknown opcode: {opcode}]")

    # Data Transfer
    def op_mov(self, dst, src):
        """MOV: 데이터 전송"""
        if src.startswith('['):
            addr = self._parse_addr(src[1:-1])
            value = self.memory.get(addr, 0)
            self.regs[dst] = value
            print(f"  {dst} ← Mem[{hex(addr)}] = {value}")
        elif dst.startswith('['):
            addr = self._parse_addr(dst[1:-1])
            value = self._parse_operand(src)
            self.memory[addr] = value
            print(f"  Mem[{hex(addr)}] ← {value}")
        else:
            value = self._parse_operand(src)
            self.regs[dst] = value
            print(f"  {dst} ← {value}")

    # Arithmetic
    def op_add(self, dst, src):
        """ADD: 덧셈"""
        dst_val = self.regs.get(dst, 0)
        src_val = self._parse_operand(src)
        result = dst_val + src_val
        self.regs[dst] = result
        self._update_flags(result)
        print(f"  {dst} ← {dst_val} + {src_val} = {result}")

    def op_sub(self, dst, src):
        """SUB: 뺄셈"""
        dst_val = self.regs.get(dst, 0)
        src_val = self._parse_operand(src)
        result = dst_val - src_val
        self.regs[dst] = result
        self._update_flags(result)
        print(f"  {dst} ← {dst_val} - {src_val} = {result}")

    # Stack
    def op_push(self, src):
        """PUSH: 스택에 저장"""
        value = self._parse_operand(src)
        self.regs['ESP'] -= 4
        self.memory[self.regs['ESP']] = value
        print(f"  PUSH {value} → [ESP={hex(self.regs['ESP'])}]")

    def op_pop(self, dst):
        """POP: 스택에서 꺼내기"""
        value = self.memory.get(self.regs['ESP'], 0)
        self.regs[dst] = value
        self.memory.pop(self.regs['ESP'], None)
        self.regs['ESP'] += 4
        print(f"  POP → {dst} = {value}, ESP = {hex(self.regs['ESP'])}")

    # String
    def op_movsb(self):
        """MOVSB: 문자열 바이트 복사"""
        src_addr = self.regs['ESI']
        dst_addr = self.regs['EDI']
        value = self.memory.get(src_addr, 0)
        self.memory[dst_addr] = value

        direction = -1 if self.flags['DF'] else 1
        self.regs['ESI'] += direction
        self.regs['EDI'] += direction

        print(f"  MOVSB: [{hex(dst_addr)}] ← [{hex(src_addr)}] = {value}")

    def op_rep_movsb(self):
        """REP MOVSB: 반복 문자열 복사"""
        ecx = self.regs['ECX']
        print(f"  REP MOVSB: ECX={ecx}")

        for _ in range(ecx):
            self.op_movsb()
            self.regs['ECX'] -= 1
            if self.regs['ECX'] == 0:
                break

    def op_stosb(self):
        """STOSB: 문자열 저장"""
        dst_addr = self.regs['EDI']
        self.memory[dst_addr] = self.regs['EAX'] & 0xFF

        direction = -1 if self.flags['DF'] else 1
        self.regs['EDI'] += direction

        print(f"  STOSB: [{hex(dst_addr)}] ← AL = {self.regs['EAX'] & 0xFF}")

    # Complex
    def op_xlat(self):
        """XLAT: 테이블 변환"""
        table_base = self.regs['EBX']
        index = self.regs['EAX'] & 0xFF
        addr = table_base + index
        value = self.memory.get(addr, 0)
        self.regs['EAX'] = (self.regs['EAX'] & ~0xFF) | (value & 0xFF)
        print(f"  XLAT: AL = Mem[EBX+AL] = Mem[{hex(addr)}] = {value}")

    def op_enter(self, size, level=0):
        """ENTER: 스택 프레임 생성"""
        size = int(size)
        level = int(level)

        old_bp = self.regs['EBP']
        self.op_push('EBP')
        self.regs['EBP'] = self.regs['ESP']

        if level > 0:
            for _ in range(level - 1):
                self.regs['ESP'] -= 4
                temp_bp = self.regs['EBP']
                # 복잡한 nesting 처리

        self.regs['ESP'] -= size
        print(f"  ENTER {size}, {level}: BP={hex(self.regs['EBP'])}, SP={hex(self.regs['ESP'])}")

    def op_leave(self):
        """LEAVE: 스택 프레임 제거"""
        self.regs['ESP'] = self.regs['EBP']
        self.op_pop('EBP')
        print(f"  LEAVE: BP={hex(self.regs['EBP'])}, SP={hex(self.regs['ESP'])}")

    def _parse_operand(self, op):
        """피연산자 파싱"""
        # 레지스터
        if op in self.regs:
            return self.regs[op]
        # 숫자
        try:
            return int(op)
        except ValueError:
            return 0

    def _parse_addr(self, addr_str):
        """주소 파싱"""
        # 단순화: 레지스터나 숫자
        if addr_str in self.regs:
            return self.regs[addr_str]
        try:
            return int(addr_str, 0)  # hex, decimal 모두
        except:
            return 0

    def _update_flags(self, result):
        """플래그 업데이트"""
        self.flags['ZF'] = 1 if result == 0 else 0
        self.flags['SF'] = 1 if result < 0 else 0


def demo_cisc_features():
    """CISC 특징 데모"""

    print("=" * 70)
    print("CISC 명령어 세트 특징")
    print("=" * 70)

    sim = CISC_Simulator()

    # 초기화
    sim.regs['EAX'] = 100
    sim.regs['EBX'] = 50
    sim.regs['ECX'] = 10
    sim.memory[0x1000] = 200
    sim.memory[0x1004] = 300

    print("\n### 초기 상태")
    print(f"EAX={sim.regs['EAX']}, EBX={sim.regs['EBX']}, ECX={sim.regs['ECX']}")

    # 메모리-메모리 연산 시뮬레이션
    print("\n### 메모리 직접 연산 (CISC 특유)")
    print("\nMOV EAX, [0x1000]")
    sim.execute("MOV EAX, [0x1000]")

    print("\nADD EAX, [0x1004]")
    sim.execute("ADD EAX, [0x1004]")

    # 스택 명령어
    print("\n### 스택 명령어")
    print("\nPUSH EAX")
    sim.execute("PUSH EAX")

    print("\nPUSH EBX")
    sim.execute("PUSH EBX")

    print("\nPOP ECX")
    sim.execute("POP ECX")

    # 문자열 명령어
    print("\n### 문자열 명령어 (String Instructions)")
    sim.regs['ESI'] = 0x2000
    sim.regs['EDI'] = 0x3000
    sim.regs['ECX'] = 5

    # 데이터 설정
    for i in range(5):
        sim.memory[0x2000 + i] = 0x40 + i  # '@', 'A', 'B', ...

    print("\nMOVSB (단일 복사)")
    sim.execute("MOVSB")

    print("\nREP MOVSB (반복 복사)")
    sim.execute("REP MOVSB")

    # ENTER/LEAVE
    print("\n### ENTER/LEAVE (Stack Frame)")
    print("\nENTER 16, 0")
    sim.execute("ENTER 16, 0")

    print("\nLEAVE")
    sim.execute("LEAVE")


def demo_cisc_vs_risc():
    """CISC vs RISC 비교"""

    print("\n\n" + "=" * 70)
    print("CISC vs RISC 코드 비교")
    print("=" * 70)

    comparison = """
    작업: 배열 합계 계산
    int sum = 0;
    for (int i = 0; i < 100; i++)
        sum += array[i];

    ┌─────────────────────────────────────────────────────────────────────┐
    │ CISC (x86)                                    │ RISC (MIPS)          │
    ├────────────────────────────────────────────────┼─────────────────────┤
    │ MOV EAX, [array]        ; 1명령어             │ ADDI $t0, $zero, 0  │
    │ ADD EAX, [array+4]      ; 메모리 직접         │ LW   $t1, array($t0)│
    │ ADD EAX, [array+8]                           │ ADD  $t2, $zero, 0  │
    │ ...                                           │ loop:               │
    │                                               │   ADD  $t2, $t2, $t1│
    │                                               │   ADDI $t0, $t0, 4  │
    │                                               │   LW   $t1,array($t0)│
    │                                               │   BNE  $t1, $zero,loop│
    └────────────────────────────────────────────────┴─────────────────────┘

    작업: 문자열 복사 (strcpy)

    ┌─────────────────────────────────────────────────────────────────────┐
    │ CISC (x86)                                    │ RISC (MIPS)          │
    ├────────────────────────────────────────────────┼─────────────────────┤
    │ REP MOVSB              ; 1명령어로 전체 복사   │ loop:               │
    │                                               │   LB   $t0, 0($t1)  │
    │                                               │   SB   $t0, 0($t2)  │
    │                                               │   ADDI $t1, $t1, 1  │
    │                                               │   ADDI $t2, $t2, 1  │
    │                                               │   BNE  $t0, $zero,loop│
    └────────────────────────────────────────────────┴─────────────────────┘

    작업: Stack Frame 생성

    ┌─────────────────────────────────────────────────────────────────────┐
    │ CISC (x86)                                    │ RISC (MIPS)          │
    ├────────────────────────────────────────────────┼─────────────────────┤
    │ ENTER 100, 0           ; 1명령어              │ ADDI $sp, $sp, -100 │
    │                                               │ SW   $ra, 96($sp)   │
    │                                               │ SW   $fp, 92($sp)   │
    │                                               │ ADDI $fp, $sp, 0    │
    └────────────────────────────────────────────────┴─────────────────────┘
    """

    print(comparison)

    summary = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                        요약                                         │
    ├─────────────────────────────────────────────────────────────────────┤
    │ CISC 장점:                                                          │
    │   - 적은 명령어 수                                                   │
    │   - 작은 코드 크기 (메모리 절약)                                     │
    │   - 복잡한 작업을 단일 명령어로                                       │
    │   - 프로그래머 친화적                                               │
    │                                                                     │
    │ CISC 단점:                                                          │
    │   - 명령어 실행 시간 불균일                                         │
    │   - 파이프라인 구현 어려움                                           │
    │   - 하드웨어 복잡 (Microcode 필요)                                  │
    │   - 전력 소모 큼                                                    │
    │                                                                     │
    │ 현대 x86 해결책:                                                    │
    │   - 내부적으로 마이크로연산(μop)으로 변환                             │
    │   - CISC 인터페이스, RISC 내부                                       │
    │   - 마이크로연산 융합, 트레이스 캐시                                  │
    └─────────────────────────────────────────────────────────────────────┘
    """

    print(summary)


if __name__ == '__main__':
    demo_cisc_features()
    demo_cisc_vs_risc()
