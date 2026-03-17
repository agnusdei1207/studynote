+++
title = "서브루틴 (Subroutine)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# 서브루틴 (Subroutine)

## 핵심 인사이트 (3줄 요약)
1. 서브루틴(Subroutine)은 재사용 가능한 코드 단위로, CALL/RET 명령어로 호출하고 복귀하며, 인자 전달과 반환값 처리가 필요하다
2. 기술사시험에서는 CALL/RET 메커니즘, Stack Frame 구조, Context Save/Restore, 인자 전달 방식이 핵심이다
3. Nested Call, Reentrant Subroutine, Tail Call Optimization 등 최적화 기법이 중요하다

## Ⅰ. 개요 (500자 이상)

서브루틴(Subroutine) 또는 프로시저(Procedure), 함수(Function)는 **반복적으로 사용되는 코드를 독립적으로 정의하고 필요할 때 호출하여 실행하는 프로그래밍 구조**다. 코드 재사용성, 모듈화, 유지보수성을 높인다.

```
서브루틴 기본 개념:
정의: 재사용 가능한 코드 단위
별칭: Subroutine, Procedure, Function, Method
특징: 한 번 정의, 여러 번 호출

구성 요소:
1. 인자 (Parameters/Arguments): 입력 데이터
2. 반환값 (Return Value): 출력 데이터
3. 지역 변수 (Local Variables): 내부 상태
4. 복귀 주소 (Return Address): 호출 위치

호출 과정:
1. 인자 전달 (Parameter Passing)
2. 복귀 주소 저장 (Return Address)
3. Jump to Subroutine
4. 실행
5. 복귀 주소로 Return
```

**서브루틴의 핵심 기능:**

1. **코드 재사용**: 중복 제거
2. **모듈화**: 문제 분해
3. **추상화**: 복잡성 숨김
4. **유지보수**: 중앙 집중 수정

```
Subroutine vs Macro:
Subroutine:
- 실행 시 Jump
- 코드 중복 없음
- 호출 오버헤드 있음
- 메모리 효율적

Macro:
- 컴파일 시 확장
- 코드 중복 발생
- 호출 오버헤드 없음
- 메모리 비효율적
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### CALL 명령어

```
CALL 명령어 동작:

단계:
1. Return Address를 Stack에 PUSH
2. Target Address로 JMP

예 (x86):
CALL 0x1000
; SP ← SP - 4
; [SS:SP] ← EIP (다음 명령어 주소)
; EIP ← 0x1000

예 (MIPS):
JAL 0x10000     ; Jump and Link
; $31 ← PC + 4  (Return Address)
; PC ← 0x10000

예 (ARM):
BL  0x1000      ; Branch with Link
; LR ← PC + 4   (Return Address)
; PC ← 0x1000

동작 비교:
x86:   Stack에 Return Address 저장
MIPS:  $31 레지스터에 저장
ARM:   LR 레지스터에 저장
```

### RET 명령어

```
RET 명령어 동작:

단계:
1. Stack에서 Return Address POP
2. 해당 주소로 JMP

예 (x86):
RET
; EIP ← [SS:SP]
; SP ← SP + 4

RET N           ; N만큼 SP 추가 증가
; EIP ← [SS:SP]
; SP ← SP + 4 + N

예 (MIPS):
JR $ra          ; Jump Register
; PC ← $ra

예 (ARM):
MOV PC, LR
; PC ← LR

RET             (ARMv8)
; PC ← X30
```

### Stack Frame 구조

```
서브루틴 Stack Frame:

┌────────────────────────────────┐
│     Caller's Stack Frame       │
├────────────────────────────────┤
│     Return Address (RA)        │ ← 호출 전 SP
├────────────────────────────────┤
│     Saved Frame Pointer (FP)   │ ← 현재 FP
├────────────────────────────────┤
│     Saved Registers           │
│     (Callee-saved)            │
├────────────────────────────────┤
│     Local Variables           │
│     (n bytes)                 │
├────────────────────────────────┤
│     Saved Temporaries         │
│     (Spill)                   │
├────────────────────────────────┤ ← 현재 SP
│     Padding (Alignment)       │
└────────────────────────────────┘

Prologue (함수 진입):
PUSH FP
MOV  FP, SP
SUB  SP, SP, #local_size
PUSH callee_saved_regs

Epilogue (함수 퇴장):
POP  callee_saved_regs
MOV  SP, FP
POP  FP
RET
```

### 인자 전달 방식

```
Parameter Passing Methods:

1. 레지스터 전달 (Register):
   - 빠름
   - 레지스터 개수 제한
   - 예: RDI, RSI, RDX (x86-64)

2. 스택 전달 (Stack):
   - 많은 인자 지원
   - 메모리 접근 필요
   - 예: 7번째 이상 인자

3. 레지스터+스택 혼합:
   - 처음 몇 개는 레지스터
   - 나머지는 스택
   - 현대적 방식

예 (x86-64 System V):
func(a, b, c, d, e, f, g, h)

전달:
RDI = a
RSI = b
RDX = c
RCX = d
R8  = e
R9  = f
[SP+8]  = g
[SP+16] = h
```

### 값 호출 vs 참조 호출

```
Call by Value vs Call by Reference:

Call by Value:
- 값 자체를 복사 전달
- 원본 변경 없음
- 메모리 사용량 증가

예:
void func(int x) {
    x = 10;    // 지역 변수만 변경
}
int a = 5;
func(a);       // a는 여전히 5

Call by Reference:
- 주소를 전달
- 원본 직접 변경
- 포인터 사용

예:
void func(int *x) {
    *x = 10;   // 원본 메모리 변경
}
int a = 5;
func(&a);      // a는 10

Call by Name (Macro):
- 텍스트 치환
- 평가 시점 차이
- ALGOL 60
```

### Nested Call

```
중첩 호출 (Nested Subroutine Call):

funcA() {
    funcB();      // A → B
}

funcB() {
    funcC();      // A → B → C
}

funcC() {
    return;       // C → B → A
}

스택 변화:

초기:
SP → 0x1000

funcA() 호출:
SP → 0x0FFC  (Return Address A)

funcB() 호출:
SP → 0x0FF8  (Return Address B)

funcC() 호출:
SP → 0x0FF4  (Return Address C)

funcC() 반환:
SP → 0x0FF8  (POP Return Address C)

funcB() 반환:
SP → 0x0FFC  (POP Return Address B)

funcA() 반환:
SP → 0x1000  (POP Return Address A)
```

### Reentrant Subroutine

```
재진입 가능 서브루틴 (Reentrant):

정의:
- 여러 번 동시 호출 가능
- 정적 데이터 사용 안 함
- Thread-safe

특징:
1. 지역 변수만 사용
2. 인자로 모든 데이터 전달
3. 호출자가 데이터 저장

예 (Reentrant):
int add(int a, int b) {
    return a + b;    // 지역 변수만
}

예 (Non-Reentrant):
int counter = 0;
int increment() {
    return counter++;    // 전역 변수 사용
}

Reentrant 변환:
int increment(int *counter) {
    return (*counter)++; // 인자로 전달
}
```

### Recursive Subroutine

```
재귀 서브루틴 (Recursive Subroutine):

정의:
- 자기 자신을 호출
- Base Case 필요
- Stack Frame 누적

예 (Factorial):
int factorial(int n) {
    if (n <= 1)          // Base Case
        return 1;
    return n * factorial(n - 1);  // Recursive Case
}

Stack 변화 (factorial(3)):

factorial(3) 호출:
  Frame 3: n=3
  factorial(2) 호출:
    Frame 2: n=2
    factorial(1) 호출:
      Frame 1: n=1
      return 1
    return 2 * 1 = 2
  return 3 * 2 = 6

스택 사용: 3개 Frame
```

### Tail Call Optimization

```
꼬리 호출 최적화 (Tail Call Optimization):

꼬리 호출 (Tail Call):
- 함수의 마지막 연산이 호출
- 반환값이 바로 전달됨

예:
int funcA(int x) {
    return funcB(x + 1);  // Tail Call
}

최적화:
- 새로운 Frame 생성 안 함
- Stack 재사용
- Stack Overflow 방지

비교:

최적화 전:
funcA(x):
  PUSH Frame A
  CALL funcB(x+1)
  ...
  POP Frame A
  RET

최적화 후:
funcA(x):
  JMP funcB(x+1)  ; CALL 대신 JMP
  ; Frame 재사용
```

### Context Switching

```
컨텍스트 전환 (Context Saving):

호출 시 저장할 내용:
1. Return Address
2. Caller-saved Registers (Temporaries)
3. Frame Pointer
4. Flags (필요시)

Callee-saved Registers:
- Callee가 저장 후 복원
- 호출자가 신경 안 써도 됨

Caller-saved Registers:
- Callee가 자유롭게 사용
- 호출자가 필요 시 저장

x86-64:
Callee-saved: RBX, RBP, R12-R15
Caller-saved: RAX, RCX, RDX, RSI, RDI, R8-R11

MIPS:
Callee-saved: $16-$23, $fp, $ra
Caller-saved: $2-$15, $24-$25

ARMv8:
Callee-saved: X19-X29, SP
Caller-saved: X0-X18, X30(LR)
```

## Ⅲ. 융합 비교

### 인자 전달 방식 비교

| 방식 | 장점 | 단점 | 속도 | 사용 |
|------|------|------|------|------|
| Register | 가장 빠름 | 개수 제한 | 최고 | 소수 인자 |
| Stack | 무제한 | 메모리 접근 | 느림 | 다수 인자 |
| Hybrid | 균형 | 복잡 | 보통 | 현대적 |

### 호출 방식 비교

| 방식 | 복귀 주소 저장 | 장점 | 단점 | 사용 |
|------|----------------|------|------|------|
| Memory Stack | 메모리 | 무제한 Nested | 느림 | x86 |
| Register | Link Register | 빠름 | 1개만 | ARM, MIPS |
| Interrupt Table | Table | 빠름 | 복잡 | MS-DOS |

### Reentrancy 비교

| 유형 | 특징 | Thread-safe | 재진입 | 예시 |
|------|------|-------------|--------|------|
| Reentrant | 지역 변수만 | O | O | 순수 함수 |
| Non-Reentrant | 정적 데이터 | X | X | 상태 유지 함수 |
| Thread-safe | 동기화 | O | X | Lock 사용 |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86-64 호출 규약

```
System V AMD64 ABI:

레지스터 할당:
RDI: 1번째 인자
RSI: 2번째 인자
RDX: 3번째 인자
RCX: 4번째 인자
R8:  5번째 인자
R9:  6번째 인자

Stack:
[SP+0]:  Return Address (자동)
[SP+8]:  7번째 인자
[SP+16]: 8번째 인자

반환값:
RAX: 정수 반환
XMM0: 부동소수점 반환

스택 정렬:
16-byte 경계 유지

예:
int add(int a, int b, int c, int d,
        int e, int f, int g, int h);

RDI=a, RSI=b, RDX=c, RCX=d
R8=e, R9=f
[SP+8]=g, [SP+16]=h
```

### ARMv64 호출 규약

```
AArch64 AAPCS:

레지스터 할당:
X0: 1번째 인자/반환값
X1: 2번째 인자
X2: 3번째 인자
X3: 4번째 인자
X4: 5번째 인자
X5: 6번째 인자
X6: 6번째 인자
X7: 6번째 인자

Stack:
[SP]: 9번째 이상 인자

반환값:
X0: 정수 반환
D0: 부동소수점 반환

보존 레지스터:
X19-X28: Callee-saved
X29: Frame Pointer
X30: Link Register

SP: 16-byte 정렬
```

### MIPS 호출 규약

```
MIPS Calling Convention:

레지스터 할당:
A0 ($4): 1번째 인자
A1 ($5): 2번째 인자
A2 ($6): 3번째 인자
A3 ($7): 4번째 인자

Stack (12($sp)부터):
5번째 이상 인자

반환값:
V0 ($2): 반환값
V1 ($3): 2번째 반환값

보존 레지스터:
S0-S7 ($16-$23): Callee-saved
GP, FP, SP, RA

임시 레지스터:
T0-T9 ($8-$15, $24-$25): Caller-saved
A0-A3 ($4-$7): Caller-saved
V0-V1 ($2-$3): Caller-saved
```

### Leaf Function 최적화

```
Leaf Function (잎 함수):

정의:
- 다른 함수 호출 안 함
- Stack Frame 불필요

최적화:
1. Stack Frame 생성 안 함
2. SP 변경 없음
3. FP 사용 안 함
4. 레지스터만 사용

예:
int add(int a, int b) {
    return a + b;
}

최적화된 어셈블리:
ADD A0, A0, A1    ; A0 = a + b
JR RA             ; return

; Stack Frame 불필요!
```

### Inline Function

```
인라인 함수 (Inline Function):

정의:
- 호출 오버헤드 제거
- 코드에 직접 삽입

장점:
- CALL/RET 오버헤드 없음
- 최적화 기회 증가
- 레지스터 할당 유연

단점:
- 코드 크기 증가
- Instruction Cache 효율 저하

예:
inline int add(int a, int b) {
    return a + b;
}

int main() {
    int x = add(1, 2);    ; CALL 없이 직접 계산
    int y = add(3, 4);    ; CALL 없이 직접 계산
}

컴파일 결과:
MOV EAX, 1
ADD EAX, 2
MOV [x], EAX

MOV EAX, 3
ADD EAX, 4
MOV [y], EAX
```

## Ⅴ. 기대효과 및 결론

서브루틴은 프로그래밍의 기본 구조로, CALL/RET 명령어와 Stack Frame으로 구현된다. 효율적인 Parameter Passing과 Context Saving이 핵심이다.

```python
"""
서브루틴 시뮬레이션
Subroutine Call Simulator
"""

class SubroutineSimulator:
    """서브루틴 호출 시뮬레이션"""

    def __init__(self):
        # 레지스터
        self.pc = 0          # Program Counter
        self.sp = 0x1000     # Stack Pointer
        self.fp = 0x1000     # Frame Pointer
        self.lr = 0          # Link Register (Return Address)
        self.regs = {f'R{i}': 0 for i in range(32)}  # 범용 레지스터

        # 메모리
        self.memory = {}
        self.stack = {}

        # 호출 스택 (디버깅용)
        self.call_stack = []

        # 함수 정의
        self.functions = {}

    def define_function(self, name, params, code, return_reg='R0'):
        """함수 정의"""
        self.functions[name] = {
            'params': params,
            'code': code,
            'return_reg': return_reg
        }

    def call(self, func_name, *args):
        """
        함수 호출 (CALL 명령어)
        """
        if func_name not in self.functions:
            raise ValueError(f"Unknown function: {func_name}")

        func = self.functions[func_name]

        # Return Address 저장 (Link Register)
        old_lr = self.lr
        old_pc = self.pc
        self.lr = self.pc + 1

        # Old Frame Pointer 저장
        old_fp = self.fp

        # 인자 전달 (레지스터)
        for i, arg in enumerate(args):
            if i < len(func['params']):
                param_name = func['params'][i]
                self.regs[f'R{i}'] = arg

        # Stack Frame 생성
        self.sp -= 4
        self.stack[self.sp] = old_fp
        self.fp = self.sp

        # 호출 스택 기록
        self.call_stack.append({
            'name': func_name,
            'pc': old_pc,
            'fp': old_fp,
            'lr': old_lr,
            'args': args
        })

        # 함수 실행
        print(f"\n[CALL] {func_name}({', '.join(map(str, args))})")
        print(f"  Return Address (LR) = 0x{self.lr:04X}")
        print(f"  Old FP = 0x{old_fp:04X}")
        print(f"  New FP = 0x{self.fp:04X}")
        print(f"  SP = 0x{self.sp:04X}")

        # 함수 코드 실행
        result = func['code'](self, *args)

        # 반환값 저장
        self.regs[func['return_reg']] = result

        return result

    def ret(self, return_value=0):
        """
        함수 반환 (RET 명령어)
        """
        if not self.call_stack:
            raise RuntimeError("No function to return from")

        frame = self.call_stack.pop()

        # 반환값
        print(f"\n[RET] {frame['name']} → {return_value}")

        # Frame Pointer 복원
        self.fp = self.stack.get(self.sp, frame['fp'])
        self.sp += 4

        # Return Address 복원
        return_addr = self.lr
        self.pc = frame['pc']
        self.lr = frame['lr']

        print(f"  Restored FP = 0x{self.fp:04X}")
        print(f"  Restored PC = 0x{return_addr:04X}")
        print(f"  SP = 0x{self.sp:04X}")

        return return_value

    def push(self, value):
        """Stack PUSH"""
        self.sp -= 4
        self.stack[self.sp] = value

    def pop(self):
        """Stack POP"""
        value = self.stack.get(self.sp, 0)
        del self.stack[self.sp]
        self.sp += 4
        return value

    def dump_state(self):
        """현재 상태 출력"""
        print(f"\n=== Processor State ===")
        print(f"PC = 0x{self.pc:04X}")
        print(f"SP = 0x{self.sp:04X}")
        print(f"FP = 0x{self.fp:04X}")
        print(f"LR = 0x{self.lr:04X}")

        print(f"\nRegisters (selected):")
        for i in [0, 1, 2, 3, 28, 29, 30, 31]:
            print(f"  R{i:2d} = {self.regs[f'R{i}']:6d}", end="")
            if i % 4 == 3:
                print()

        if self.call_stack:
            print(f"\nCall Stack ({len(self.call_stack)} frames):")
            for i, frame in enumerate(reversed(self.call_stack[-5:])):
                print(f"  [{i}] {frame['name']}({', '.join(map(str, frame['args']))})")

    def dump_stack(self, num_words=8):
        """Stack 메모리 덤프"""
        print(f"\n=== Stack Dump (SP=0x{self.sp:04X}) ===")
        for i in range(self.sp, self.sp + num_words * 4, 4):
            if i in self.stack:
                marker = " ← SP" if i == self.sp else ""
                marker += " ← FP" if i == self.fp else ""
                print(f"  0x{i:04X}: 0x{self.stack[i]:08X}{marker}")


def demo_basic_call():
    """기본 함수 호출"""

    print("=" * 70)
    print("기본 서브루틴 호출 (Basic Subroutine Call)")
    print("=" * 70)

    sim = SubroutineSimulator()

    # add 함수 정의
    def add_code(sim, a, b):
        """두 수 더하기"""
        result = a + b
        print(f"  Computing: {a} + {b} = {result}")
        return result

    sim.define_function('add', ['a', 'b'], add_code)

    # multiply 함수 정의
    def mul_code(sim, a, b):
        """두 수 곱하기"""
        result = a * b
        print(f"  Computing: {a} × {b} = {result}")
        return result

    sim.define_function('mul', ['a', 'b'], mul_code)

    # 호출
    sim.call('add', 10, 20)
    sim.ret(30)

    sim.call('mul', 5, 6)
    sim.ret(30)

    sim.dump_state()


def demo_nested_call():
    """중첩 호출"""

    print("\n\n" + "=" * 70)
    print("중첩 서브루틴 호출 (Nested Call)")
    print("=" * 70)

    sim = SubroutineSimulator()

    # inner 함수
    def inner_code(sim, x):
        print(f"    inner({x}) 실행")
        result = x * 2
        return result

    sim.define_function('inner', ['x'], inner_code)

    # outer 함수
    def outer_code(sim, a, b):
        print(f"  outer({a}, {b}) 실행")
        temp1 = sim.call('inner', a)
        sim.ret(temp1)

        temp2 = sim.call('inner', b)
        sim.ret(temp2)

        result = temp1 + temp2
        print(f"  outer 반환: {result}")
        return result

    sim.define_function('outer', ['a', 'b'], outer_code)

    # 호출
    print(">> outer(10, 20) 호출")
    result = sim.call('outer', 10, 20)
    sim.ret(result)

    sim.dump_state()
    sim.dump_stack()


def demo_recursive_call():
    """재귀 호출"""

    print("\n\n" + "=" * 70)
    print("재귀 서브루틴 (Recursive Subroutine)")
    print("=" * 70)

    sim = SubroutineSimulator()

    # factorial 함수
    def factorial_code(sim, n):
        indent = "  " * len(sim.call_stack)
        print(f"{indent}factorial({n})")

        if n <= 1:
            print(f"{indent}  Base case: return 1")
            return 1
        else:
            print(f"{indent}  Recursive: factorial({n-1})")
            temp = sim.call('factorial', n - 1)
            result = n * temp
            sim.ret(temp)
            print(f"{indent}  Return {n} × {temp} = {result}")
            return result

    sim.define_function('factorial', ['n'], factorial_code)

    # 호출
    print(">> factorial(5) 호출")
    result = sim.call('factorial', 5)
    sim.ret(result)

    print(f"\n최종 결과: 5! = {result}")
    sim.dump_stack()


def demo_parameter_passing():
    """인자 전달 방식"""

    print("\n\n" + "=" * 70)
    print("인자 전달 방식 (Parameter Passing)")
    print("=" * 70)

    sim = SubroutineSimulator()

    # by_value: 값 복사
    def by_value_code(sim, x):
        print(f"  받은 값: {x}")
        x = x + 100  # 지역 변경
        print(f"  변경된 값: {x}")
        return x

    sim.define_function('by_value', ['x'], by_value_code)

    # by_reference (시뮬레이션: 주소 전달)
    def by_ref_code(sim, addr):
        print(f"  받은 주소: 0x{addr:04X}")
        value = sim.memory.get(addr, 0)
        print(f"  주소의 값: {value}")
        sim.memory[addr] = value + 100
        print(f"  변경된 값: {sim.memory[addr]}")
        return sim.memory[addr]

    sim.define_function('by_ref', ['addr'], by_ref_code)

    # Call by Value
    print("\n### Call by Value")
    x_val = 50
    print(f"호출 전: x = {x_val}")
    sim.call('by_value', x_val)
    sim.ret(0)
    print(f"호출 후: x = {x_val} (변경 없음)")

    # Call by Reference
    print("\n### Call by Reference")
    sim.memory[0x2000] = 50
    print(f"호출 전: mem[0x2000] = {sim.memory[0x2000]}")
    sim.call('by_ref', 0x2000)
    sim.ret(0)
    print(f"호출 후: mem[0x2000] = {sim.memory[0x2000]} (변경됨)")


def demo_tail_call():
    """꼬리 호출 최적화"""

    print("\n\n" + "=" * 70)
    print("꼬리 호출 최적화 (Tail Call Optimization)")
    print("=" * 70)

    explanation = """
    꼬리 호출 (Tail Call):
    - 함수의 마지막 연산이 다른 함수 호출
    - 반환값을 추가 처리 없이 바로 반환

    장점:
    - 새로운 Stack Frame 불필요
    - Stack 재사용
    - Stack Overflow 방지

    일반 호출:
    funcA() {
      temp = funcB()  ; Stack Frame 유지
      return temp + 1
    }

    꼬리 호출:
    funcA() {
      return funcB()  ; Frame 재사용 가능
    }
    """

    print(explanation)

    # 일반 재귀
    print("\n### 일반 재귀 (Non-Tail)")
    print("def factorial(n):")
    print("    if n <= 1: return 1")
    print("    return n * factorial(n - 1)  ; 곱셈 후 반환")

    # 꼬리 호출 재귀
    print("\n### 꼬리 호출 재귀 (Tail Call)")
    print("def factorial(n, acc=1):")
    print("    if n <= 1: return acc")
    print("    return factorial(n - 1, acc * n)  ; 바로 반환")


def demo_comparison():
    """호출 방식 비교"""

    print("\n\n" + "=" * 70)
    print("서브루틴 호출 방식 비교")
    print("=" * 70)

    comparison = """
    ┌────────────────────────────────────────────────────────────────────┐
    │                     Link Register vs Stack                        │
    ├────────────────────────────────────┬───────────────────────────────┤
    │ Link Register (ARM, MIPS)          │ Memory Stack (x86)           │
    ├────────────────────────────────────┼───────────────────────────────┤
    │ Return Address를 LR에 저장         │ Return Address를 Stack에 저장 │
    │ 1 Cycle                             │ 2-3 Cycles                   │
    │ 추가 메모리 접근 없음               │ 메모리 접근 필요             │
    │ 중첩 깊이 제한 (Leaf만)             │ 무제한 중첩                  │
    │ Leaf 함수에서 Frame 불필요          │ 모든 함수에 Frame 필요       │
    └────────────────────────────────────┴───────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────┐
    │                     Parameter Passing                             │
    ├────────────────────────────────────────────────────────────────────┤
    │ Register (빠름)   │ Stack (느림)        │ Hybrid (균형)             │
    ├───────────────────┼─────────────────────┼──────────────────────────┤
    │ x86-64: RDI,RSI,  │ x86: [SP+8],       │ x86-64 System V:         │
    │        RDX,RCX,   │      [SP+16] 등     │ RDI-R9 (6개)             │
    │        R8,R9      │ PUSH로 전달         │ Stack (7개 이상)         │
    │                   │                     │                          │
    │ ARM64: X0-X7      │ x86 32-bit:         │ ARM64 AAPCS:             │
    │                   │ Stack만 사용        │ X0-X7 (8개)              │
    │                   │                     │ Stack (9개 이상)         │
    └───────────────────┴─────────────────────┴──────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────┐
    │                     Call Convention                               │
    ├───────────────────┬───────────────────┬────────────────────────────┤
    │                   │ Caller-saved      │ Callee-saved               │
    ├───────────────────┼───────────────────┼────────────────────────────┤
    │ x86-64            │ RAX,RCX,RDX,RSI,  │ RBX,RBP,R12-R15            │
    │                   │ RDI,R8-R11        │                             │
    ├───────────────────┼───────────────────┼────────────────────────────┤
    │ ARM64             │ X0-X18,X30(LR)    │ X19-X28,FP,SP              │
    ├───────────────────┼───────────────────┼────────────────────────────┤
    │ MIPS              │ T0-T9,A0-A3,V0-V1 │ S0-S7,GP,FP,RA             │
    └───────────────────┴───────────────────┴────────────────────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_basic_call()
    demo_nested_call()
    demo_recursive_call()
    demo_parameter_passing()
    demo_tail_call()
    demo_comparison()
