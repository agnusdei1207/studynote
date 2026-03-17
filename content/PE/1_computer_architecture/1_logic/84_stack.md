+++
title = "스택 (Stack)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# 스택 (Stack)

## 핵심 인사이트 (3줄 요약)
1. 스택(Stack)은 LIFO(Last In First Out) 구조로, PUSH/POP 연산으로 데이터를 저장하고 꺼내는 후입선출 메모리 영역이다
2. 기술사시험에서는 Stack Pointer(SP), Stack Frame, 함수 호출 규약, Stack Overflow/Underflow가 핵심이다
3. 함수 호출, 지역 변수, 인자 전달, Return Address 저장에 사용되며, 하드웨어와 소프트웨어적으로 구현된다

## Ⅰ. 개요 (500자 이상)

스택(Stack)은 **후입선출(LIFO, Last In First Out) 구조의 메모리 영역**으로, 함수 호출, 지역 변수, 복귀 주소 저장 등에 사용된다. Stack Pointer(SP)라는 전용 레지스터로 현재 위치를 추적한다.

```
스택 기본 개념:
구조: LIFO (Last In First Out)
연산: PUSH (저장), POP (꺼내기)
관리: Stack Pointer (SP)
용도: 함수 호출, 지역 변수, 인자

동작:
PUSH: SP 감소 → 데이터 저장
POP: 데이터 로드 → SP 증가

종류:
1. 하드웨어 스택: CPU 명령어 지원
2. 소프트웨어 스택: 메모리 영역 활용
3. 시스템 스택: OS/Kernel용
4. 사용자 스택: Application용
```

**스택의 핵심 특징:**

1. **LIFO**: 가장 마지막에 넣은 데이터가 먼저 나옴
2. **SP 관리**: 자동 증감으로 위치 추적
3. **Stack Frame**: 함수마다 독립 영역
4. **Overflow/Underflow**: 경계 위반 시 오류

```
Stack vs Heap:
Stack:
- 자동 할당/해제
- LIFO 순서
- 빠른 접근
- 크기 제한
- 함수 호출/지역변수

Heap:
- 동적 할당/해제
- 임의 순서
- 상대적으로 느림
- 크기 유연
- 동적 메모리
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 스택 구조

```
스택 메모리 배치:

하향식 스택 (Descending, 일반적):
┌──────────────────────────────────┐
│         High Address             │
│                                  │
│                                  │
│              ↓                   │
│           Growing                │
│                                  │
│                                  │
├──────────────────────────────────┤ ← SP 초기값
│                                  │
│              ↑                   │
│                                  │
│         Low Address              │
└──────────────────────────────────┘

상향식 스택 (Ascending):
┌──────────────────────────────────┐
│         High Address             │
│                                  │
│              ↑                   │
│          Growing                 │
│                                  │
├──────────────────────────────────┤ ← SP 초기값
│              ↓                   │
│                                  │
│         Low Address              │
└──────────────────────────────────┘
```

### PUSH 연산

```
PUSH 연산 (하향식 스택):

단계:
1. SP ← SP - Element_Size
2. [SP] ← Source

예 (PUSH R1):
Before:
    SP → 0x1000
    R1  = 0xABCD

After:
    0x0FFC → 0xABCD
    SP → 0x0FFC

비트:
DEC SP         ; SP 감소
MOV [SP], R1   ; 데이터 저장

x86:
PUSH EAX       ; SP ← SP - 4
               ; [SS:SP] ← EAX

MIPS:
ADDI $sp, $sp, -4   ; $sp -= 4
SW $ra, 0($sp)      ; 저장
```

### POP 연산

```
POP 연산 (하향식 스택):

단계:
1. Destination ← [SP]
2. SP ← SP + Element_Size

예 (POP R1):
Before:
    0x0FFC → 0xABCD
    SP → 0x0FFC

After:
    SP → 0x1000
    R1  = 0xABCD

비트:
MOV R1, [SP]   ; 데이터 로드
INC SP         ; SP 증가

x86:
POP EAX        ; EAX ← [SS:SP]
               ; SP ← SP + 4

MIPS:
LW $ra, 0($sp)      ; 로드
ADDI $sp, $sp, 4    ; $sp += 4
```

### Stack Frame

```
스택 프레임 구조:

┌────────────────────────────────┐
│     이전 함수의 Stack Frame     │
├────────────────────────────────┤
│         Return Address         │ ← Caller의 FP
├────────────────────────────────┤
│     Saved Frame Pointer (FP)   │ ← 현재 FP
├────────────────────────────────┤
│         지역 변수 #1            │
│         지역 변수 #2            │
│         ...                    │
├────────────────────────────────┤
│         Saved Registers        │
├────────────────────────────────┤
│         인자 #N (선택)          │
├────────────────────────────────┤ ← SP
│     다음 함수를 위한 공간       │
└────────────────────────────────┘

FP (Frame Pointer): 기준점
SP (Stack Pointer): 현재 위치
```

### 함수 호출과 스택

```
함수 호출 스택 동작:

int add(int a, int b) {
    int c = a + b;
    return c;
}

int main() {
    int result = add(10, 20);
    return 0;
}

스택 변화:

1. main() 시작:
   SP 초기화

2. add() 호출 전:
   PUSH b (20)
   PUSH a (10)
   PUSH Return Address

3. add() 진입:
   PUSH FP
   FP ← SP
   SP ← SP - local_size
   ; c 저장 공간 확보

4. add() 실행:
   c ← a + b

5. add() 반환:
   return value → 레지스터
   SP ← FP
   POP FP
   POP Return Address
   SP ← SP + arg_size

6. main() 복귀:
   result ← return value
```

### Stack Pointer 레지스터

```
SP 레지스터:

역할:
- 현재 Stack Top 지정
- PUSH/POP 시 자동 갱신
- 함수 진입/퇴장 시 관리

아키텍처별 SP:
x86:
  SS:SP (16-bit)
  SS:ESP (32-bit)
  SS:RSP (64-bit)

MIPS:
  $sp ($29)
  $fp ($30) - Frame Pointer

ARM:
  SP (R13)
  FP (R11) - Frame Pointer

RISC-V:
  sp (x2)
  fp (s0, x8)
```

### Stack Overflow

```
스택 오버플로우:

원인:
1. 무한 재귀 호출
2. 너무 큰 지역 변수
3. 깊은 함수 호출

증상:
- Segmentation Fault
- 예기치 않은 동작
- 보안 취약점

예 (무한 재귀):
void infinite() {
    char buffer[1000];
    infinite();  // SP 계속 감소
}
```

### Stack Underflow

```
스택 언더플로우:

원인:
1. 너무 많은 POP
2. SP 관리 실수
3. 스택 불일치

증상:
- 잘못된 데이터 로드
- 프로그램崩溃

예:
for (int i = 0; i < 100; i++) {
    POP R1  // 너무 많은 POP
}
```

### 하드웨어 스택 명령어

```
x86 Stack 명령어:

PUSH reg:
  SP ← SP - 2/4/8
  [SP] ← reg

POP reg:
  reg ← [SP]
  SP ← SP + 2/4/8

PUSHA:
  AX, CX, DX, BX, SP, BP, SI, DI 순으로 PUSH

POPA:
  DI, SI, BP, SP, BX, DX, CX, AX 순으로 POP

PUSHF:
  FLAGS → Stack

POPF:
  Stack → FLAGS

PUSHAD/PUSHADQ:
  모든 범용 레지스터 PUSH

CALL near:
  PUSH EIP
  JMP target

RET:
  POP EIP
```

### Calling Convention

```
함수 호출 규약 (x86-64 System V):

레지스터 인자 전달:
RDI: 1번째 인자
RSI: 2번째 인자
RDX: 3번째 인자
RCX: 4번째 인자
R8:  5번째 인자
R9:  6번째 인자
스택: 7번째 이상 인자

반환값:
RAX: 정수 반환
XMM0: 부동소수점 반환

보존 레지스터 (Callee-saved):
RBX, RBP, R12-R15

임시 레지스터 (Caller-saved):
RAX, RCX, RDX, RSI, RDI, R8-R11
```

## Ⅲ. 융합 비교

### Stack 유형 비교

| 유형 | 성장 방향 | 장점 | 단점 | 사용 |
|------|-----------|------|------|------|
| Descending | 감소 | Heap과 분리 | - | 대부분 |
| Ascending | 증가 | 단순 | Heap 충돌 가능 | 일부 |

### Stack vs Heap

| 특성 | Stack | Heap |
|------|-------|------|
| 할당 | 자동 | 수동 |
| 순서 | LIFO | 임의 |
| 속도 | 빠름 | 느림 |
| 크기 | 제한 | 큼 |
| 용도 | 지역변수 | 동적 메모리 |
| 해제 | 자동 | 명시적 |

### Calling Convention 비교

| 규약 | 인자 전달 | 반환 | 스택 정리 | 사용 |
|------|-----------|------|-----------|------|
| cdecl | Stack (→) | EAX | Caller | C (x86) |
| stdcall | Stack (→) | EAX | Callee | Windows API |
| fastcall | Reg+Stack | EAX | Callee | 최적화 |
| thiscall | Reg+Stack | EAX | Callee | C++ 메서드 |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86 Stack Frame

```
x86-64 Stack Frame Layout:

High Address
┌────────────────────────────────┐
│     이전 함수의 Frame          │
├────────────────────────────────┤
│     Return Address (8B)        │ ← RBP
├────────────────────────────────┤
│     Saved RBP (8B)             │
├────────────────────────────────┤
│     지역 변수                  │
│     (16B aligned)              │
├────────────────────────────────┤
│     Saved Registers           │
├────────────────────────────────┤
│     Home Space (32B)           │
├────────────────────────────────┤ ← RSP
│     Red Zone (128B)            │
└────────────────────────────────┘
Low Address

Prologue:
PUSH RBP
MOV RBP, RSP
AND RSP, -16       ; 16-byte alignment
SUB RSP, N         ; 지역 변수 공간

Epilogue:
MOV RSP, RBP
POP RBP
RET
```

### ARM Stack Frame

```
ARMv8 Stack Frame:

High Address
┌────────────────────────────────┐
│     이전 함수의 Frame          │
├────────────────────────────────┤
│     Return Address (LR)        │ ← FP (X29)
├────────────────────────────────┤
│     Saved FP (X29)             │
├────────────────────────────────┤
│     Saved Registers           │
│     X19-X28                    │
├────────────────────────────────┤
│     지역 변수                  │
│     (16B aligned)              │
├────────────────────────────────┤ ← SP (X31)
│     Padding                   │
└────────────────────────────────┘
Low Address

PUSH {FP, LR}
MOV FP, SP
SUB SP, SP, #N     ; local_size

...
MOV SP, FP
POP {FP, LR}
RET
```

### MIPS Stack Frame

```
MIPS Stack Frame:

High Address
┌────────────────────────────────┐
│     Argument Word #N           │
├────────────────────────────────┤
│     Saved RA ($31)             │
├────────────────────────────────┤
│     Saved FP ($30)             │
├────────────────────────────────┤
│     Saved Registers           │
│     ($16-$23, $f20-$f31)      │
├────────────────────────────────┤
│     Local Variables           │
├────────────────────────────────┤ ← $sp
│     Stack Argument Area       │
└────────────────────────────────┘
Low Address

Prologue:
ADDI $sp, $sp, -frame_size
SW $ra, frame_size-4($sp)
SW $fp, frame_size-8($sp)

Epilogue:
LW $ra, frame_size-4($sp)
LW $fp, frame_size-8($sp)
ADDI $sp, $sp, frame_size
JR $ra
```

### Buffer Overflow 보호

```
스택 보호 기법:

1. Stack Canary:
   FP와 지역 변수 사이에 canary 값
   함수 반환 전 확인

   ┌────────────────────┐
   │   Return Address   │
   ├────────────────────┤
   │   Saved FP         │
   ├────────────────────┤
   │   Canary           │ ← 보호 값
   ├────────────────────┤
   │   Local Variables  │
   └────────────────────┘

2. ASLR (Address Space Layout Randomization):
   스택 시작 주소 랜덤화
   공격자 주소 예측 어려움

3. NX Bit (No-Execute):
   스택 영역 실행 비허용
   Shellcode 방지

4. Shadow Stack:
   별도의 Return Address 스택
   ROP 공격 방지
```

### Stack Alignment

```
스택 정렬 (Alignment):

x86-64 ABI:
- 16-byte 정렬 필요
- Call 전 SP가 16의 배수
- SSE/AVX 명령어 효율

예:
Before call: SP = 0x1000 (16-byte aligned)
After call:  SP = 0x0FF8 (Return Address 저장)

함수 진입 시:
PUSH RBP        ; SP = 0x0FF0
MOV RBP, RSP
AND RSP, -16    ; SP = 0x0FF0 (정렬 유지)

정렬이 필요한 이유:
1. SIMD 명령어 요구
2. 캐시 라인 정렬
3. 성능 최적화
```

## Ⅴ. 기대효과 및 결론

스택은 함수 호출, 지역 변수 저장에 필수적인 LIFO 구조다. SP, FP 관리와 Calling Convention 준수가 중요하다.

```python
"""
스택 시뮬레이션
Stack Simulator
"""

class Stack:
    """하드웨어 스택 시뮬레이션"""

    def __init__(self, size=1024, descending=True):
        self.size = size
        self.descending = descending
        self.memory = [0] * size
        self.sp = size if descending else 0
        self.initial_sp = self.sp
        self.frames = []
        self.elements = []  # 디버깅용

    def push(self, value, size=4):
        """
        PUSH 연산
        """
        if self.descending:
            self.sp -= size
            if self.sp < 0:
                raise StackOverflow(f"Stack overflow: SP={self.sp}")
            self.memory[self.sp:self.sp+size] = self._to_bytes(value, size)
        else:
            if self.sp + size > self.size:
                raise StackOverflow(f"Stack overflow: SP={self.sp}")
            self.memory[self.sp:self.sp+size] = self._to_bytes(value, size)
            self.sp += size

        self.elements.append(value)
        return self.sp

    def pop(self, size=4):
        """
        POP 연산
        """
        if self.descending:
            if self.sp < 0:
                raise StackUnderflow(f"Stack underflow: SP={self.sp}")
            value = self._from_bytes(self.memory[self.sp:self.sp+size])
            self.memory[self.sp:self.sp+size] = [0] * size
            self.sp += size
            if self.sp > self.initial_sp:
                self.sp = self.initial_sp
        else:
            if self.sp == 0:
                raise StackUnderflow(f"Stack underflow: SP={self.sp}")
            self.sp -= size
            value = self._from_bytes(self.memory[self.sp:self.sp+size])
            self.memory[self.sp:self.sp+size] = [0] * size

        if self.elements:
            self.elements.pop()
        return value

    def peek(self, offset=0, size=4):
        """
        PEEK: 스택의 데이터 확인 (제거 안 함)
        """
        if self.descending:
            addr = self.sp + offset
        else:
            addr = self.sp - offset - size
        return self._from_bytes(self.memory[addr:addr+size])

    def push_frame(self, return_addr, frame_pointer=None):
        """
        스택 프레임 생성
        """
        frame = {
            'sp': self.sp,
            'return_addr': return_addr,
            'fp': frame_pointer,
            'locals': [],
            'args': []
        }
        self.frames.append(frame)

        # Return Address PUSH
        self.push(return_addr)

        # Old FP PUSH
        old_fp = self.frames[-2]['sp'] if len(self.frames) > 1 else self.initial_sp
        self.push(old_fp)

        return frame

    def pop_frame(self):
        """
        스택 프레임 제거
        """
        if not self.frames:
            raise StackError("No frame to pop")

        frame = self.frames.pop()

        # Old FP 복원
        old_fp = self.pop()

        # Return Address 복원
        ret_addr = self.pop()

        return ret_addr

    def allocate_local(self, size):
        """
        지역 변수 공간 할당
        """
        if not self.frames:
            raise StackError("No active frame")

        frame = self.frames[-1]

        if self.descending:
            self.sp -= size
        else:
            self.sp += size

        frame['locals'].append((self.sp, size))
        return self.sp

    def store_local(self, offset, value, size=4):
        """
        지역 변수 저장
        """
        addr = self.sp + offset if self.descending else self.sp - offset - size
        self.memory[addr:addr+size] = self._to_bytes(value, size)

    def load_local(self, offset, size=4):
        """
        지역 변수 로드
        """
        addr = self.sp + offset if self.descending else self.sp - offset - size
        return self._from_bytes(self.memory[addr:addr+size])

    def _to_bytes(self, value, size):
        """정수를 바이트로 변환"""
        return [(value >> (i * 8)) & 0xFF for i in range(size)]

    def _from_bytes(self, bytes_data):
        """바이트를 정수로 변환"""
        value = 0
        for i, b in enumerate(bytes_data):
            value |= b << (i * 8)
        return value

    def dump(self, num_words=16):
        """스택 내용 출력"""
        print(f"\n=== Stack Dump (SP={self.sp}, Base={self.initial_sp}) ===")

        if self.descending:
            # SP부터 initial_sp까지
            for i in range(self.sp, min(self.sp + num_words * 4, self.initial_sp), 4):
                if i < 0:
                    continue
                marker = " ← SP" if i == self.sp else ""
                marker += " ← FP" if any(f['fp'] == i for f in self.frames) else ""
                value = self._from_bytes(self.memory[i:i+4])
                print(f"  0x{i:04X}: 0x{value:08X}{marker}")
        else:
            # 0부터 SP까지
            for i in range(max(0, self.sp - num_words * 4), self.sp, 4):
                marker = " ← SP" if i == self.sp - 4 else ""
                value = self._from_bytes(self.memory[i:i+4])
                print(f"  0x{i:04X}: 0x{value:08X}{marker}")

        print(f"\n  Elements: {self.elements[-8:] if len(self.elements) > 8 else self.elements}")


class StackOverflow(Exception):
    """스택 오버플로우"""
    pass


class StackUnderflow(Exception):
    """스택 언더플로우"""
    pass


class StackError(Exception):
    """스택 오류"""
    pass


class FunctionCall:
    """함수 호출 시뮬레이션"""

    def __init__(self, stack):
        self.stack = stack
        self.call_depth = 0
        self.return_values = {}

    def call(self, func_name, args):
        """
        함수 호출 시뮬레이션
        """
        print(f"\n[CALL] {func_name}({', '.join(map(str, args))})")

        # 인자 PUSH (역순)
        for arg in reversed(args):
            self.stack.push(arg)

        # Return Address (시뮬레이션용)
        return_addr = self.call_depth * 1000 + 0x1000

        # Stack Frame 생성
        frame = self.stack.push_frame(return_addr)

        self.call_depth += 1

        return return_addr

    def ret(self, return_value=None):
        """
        함수 반환 시뮬레이션
        """
        ret_addr = self.stack.pop_frame()
        self.call_depth -= 1

        if return_value is not None:
            print(f"[RET] Returning {return_value}")

        return ret_addr

    def local_var(self, size=4):
        """지역 변수 할당"""
        return self.stack.allocate_local(size)


def demo_stack_operations():
    """기본 스택 연산 데모"""

    print("=" * 70)
    print("스택 기본 연산 (Basic Stack Operations)")
    print("=" * 70)

    stack = Stack(size=256, descending=True)

    print("\n### PUSH 연산")
    for i in range(5):
        addr = stack.push(0x1000 + i * 0x10)
        print(f"  PUSH 0x{0x1000 + i * 0x10:04X} → SP = 0x{addr:04X}")

    stack.dump()

    print("\n### POP 연산")
    for i in range(3):
        value = stack.pop()
        print(f"  POP → 0x{value:04X}, SP = 0x{stack.sp:04X}")

    stack.dump()

    print("\n### PEEK 연산")
    print(f"  PEEK (top): 0x{stack.peek():04X}")
    print(f"  PEEK (offset=4): 0x{stack.peek(4):04X}")

    print("\n### 스택 크기")
    print(f"  Used: {stack.initial_sp - stack.sp} bytes")
    print(f"  Available: {stack.sp} bytes")


def demo_function_calls():
    """함수 호출 스택 시뮬레이션"""

    print("\n\n" + "=" * 70)
    print("함수 호출 스택 (Function Call Stack)")
    print("=" * 70)

    stack = Stack(size=1024)
    fc = FunctionCall(stack)

    # main() 함수
    print("\n### main() 시작")
    fc.call('main', [])
    main_local = fc.local_var(4)
    stack.store_local(0, 100)  # result = 100
    print(f"  Local variable at offset 0: {stack.load_local(0)}")
    stack.dump()

    # add() 함수 호출
    print("\n### add(a=10, b=20) 호출")
    fc.call('add', [10, 20])

    # 지역 변수
    add_local = fc.local_var(4)
    stack.store_local(0, 30)  # c = 10 + 20
    print(f"  Local c = {stack.load_local(0)}")
    stack.dump()

    # add() 반환
    print("\n### add() 반환")
    fc.ret(30)
    stack.dump()

    # subtract() 호출
    print("\n### subtract(x=100, y=30) 호출")
    fc.call('subtract', [100, 30])
    sub_local = fc.local_var(4)
    stack.store_local(0, 70)
    print(f"  Local result = {stack.load_local(0)}")
    stack.dump()

    # subtract() 반환
    print("\n### subtract() 반환")
    fc.ret(70)
    stack.dump()

    # main() 반환
    print("\n### main() 반환")
    fc.ret()
    stack.dump()


def demo_recursion():
    """재귀 호출 시뮬레이션"""

    print("\n\n" + "=" * 70)
    print("재귀 호출 (Recursive Call)")
    print("=" * 70)

    stack = Stack(size=1024)
    fc = FunctionCall(stack)

    def factorial(n, depth=0):
        """factorial 재귀 함수"""
        indent = "  " * depth
        print(f"{indent}factorial({n}) 호출")

        fc.call('factorial', [n])
        local_var = fc.local_var(4)

        if n <= 1:
            result = 1
            print(f"{indent}  Base case: return 1")
        else:
            result = n * factorial(n - 1, depth + 1)
            print(f"{indent}  Return {n} * {result // n} = {result}")

        stack.store_local(0, result)
        fc.ret(result)

        return result

    try:
        result = factorial(5)
        print(f"\n\n결과: 5! = {result}")
        stack.dump()

    except StackOverflow:
        print("\n스택 오버플로우 발생!")


def demo_stack_overflow():
    """스택 오버플로우 시뮬레이션"""

    print("\n\n" + "=" * 70)
    print("스택 오버플로우 (Stack Overflow)")
    print("=" * 70)

    # 작은 스택으로 오버플로우 유도
    stack = Stack(size=64)

    print("\n### 무한 PUSH 시도")
    try:
        for i in range(100):
            stack.push(0xABCD)
            if i % 10 == 9:
                print(f"  {i+1} pushes, SP = {stack.sp}")
    except StackOverflow as e:
        print(f"\n  [ERROR] {e}")

    stack.dump()


def demo_stack_alignment():
    """스택 정렬 시뮬레이션"""

    print("\n\n" + "=" * 70)
    print("스택 정렬 (Stack Alignment)")
    print("=" * 70)

    stack = Stack(size=1024)

    print("\n### 16-byte 정렬 확인")
    print(f"Initial SP: 0x{stack.sp:04X} (16-byte aligned: {stack.sp % 16 == 0})")

    # 4바이트 PUSH
    stack.push(0x11111111)
    print(f"After PUSH: 0x{stack.sp:04X} (aligned: {stack.sp % 16 == 0})")

    # 8바이트 PUSH
    stack.push(0x22222222, size=8)
    print(f"After 8B PUSH: 0x{stack.sp:04X} (aligned: {stack.sp % 16 == 0})")

    # 정렬 조정
    misalignment = stack.sp % 16
    if misalignment != 0:
        padding = 16 - misalignment
        stack.sp -= padding
        print(f"Padding: {padding} bytes")
        print(f"Aligned SP: 0x{stack.sp:04X} (16-byte aligned: {stack.sp % 16 == 0})")


def demo_comparison():
    """스택 vs 힙 비교"""

    print("\n\n" + "=" * 70)
    print("스택 vs 힙 비교")
    print("=" * 70)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                        STACK          │           HEAP              │
    ├───────────────────────────────────────┼─────────────────────────────┤
    │ 할당      │ 자동 (함수 진입/퇴장)     │ 수동 (malloc/new)           │
    │ 해제      │ 자동                      │ 명시적 (free/delete)        │
    │ 순서      │ LIFO                       │ 임의                        │
    │ 속도      │ 매우 빠름 (SP만 변경)      │ 느림 (할당자 필요)          │
    │ 크기      │ 제한됨 (1-8MB)            │ 큼 (시스템 메모리)           │
    │ 용도      │ 지역 변수, Return Address │ 동적 배열, 객체             │
    │ 단편화    │ 없음                       │ 가능 (내부/외부)            │
    │ 캐칭      │ 유리 (지역성)             │ 불리 (분산)                 │
    │ 스레딩    │ 독립적                     │ 공유 가능                   │
    └───────────────────────────────────────┴─────────────────────────────┘

    Calling Convention (x86-64 System V):
    ┌─────────────────────────────────────────────────────────────────────┐
    │ 인자 전달:                                                      │
    │   RDI, RSI, RDX, RCX, R8, R9 (첫 6개)                            │
    │   Stack (7번째 이상)                                              │
    │                                                                  │
    │ 반환값:                                                          │
    │   RAX (정수), XMM0 (부동소수점)                                   │
    │                                                                  │
    │ 보존 레지스터 (Callee-saved):                                    │
    │   RBX, RBP, R12-R15                                              │
    │                                                                  │
    │ 임시 레지스터 (Caller-saved):                                    │
    │   RAX, RCX, RDX, RSI, RDI, R8-R11                                │
    │                                                                  │
    │ 정렬:                                                            │
    │   16-byte 경계 필요 (call 전)                                    │
    └─────────────────────────────────────────────────────────────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_stack_operations()
    demo_function_calls()
    demo_recursion()
    demo_stack_overflow()
    demo_stack_alignment()
    demo_comparison()
