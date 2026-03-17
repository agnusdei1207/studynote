+++
title = "예외 처리 (Exception Handling)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "명령어"]
draft = false
+++

# 예외 처리 (Exception Handling)

## 핵심 인사이트 (3줄 요약)
1. 예외(Exception)는 CPU가 명령어를 실행하면서 발생하는 비정상적인 상황으로, Fault(복귀 가능), Trap(의도적), Abort(복귀 불가)로 분류된다
2. 기술사시험에서는 예외 종류, Exception Handler, Double Fault, Stack Fault, Page Fault 처리가 핵심이다
3. 하드웨어 예외(Trap, Fault)와 소프트웨어 예외(try-catch)는 서로 다른 계층에서 처리된다

## Ⅰ. 개요 (500자 이상)

예외(Exception)는 **CPU가 명령어를 실행하는 도중 발생하는 비정상적인 상황이나 특수한 조건을 처리하기 위해 실행 흐름을 변경하는 메커니즘**이다. 인터럽트와 유사하지만, 내부적이고 동기적으로 발생한다는 점이 다르다.

```
예외 기본 개념:
정의: CPU 내부에서 발생하는 비정상 상황
특징: 동기적 발생, 명령어와 연관
구분: Fault, Trap, Abort, Terminate

발생 원인:
1. 명령어 실행 오류
2. 메모리 접근 위반
3. 권한 위반
4. 정의되지 않은 연산
5. 디버깅 용도

처리 과정:
Exception → Context Save → Handler → 복귀/종료
```

**예외의 핵심 특징:**

1. **동기성**: 명령어 실행 중 발생
2. **예측 가능성**: 동일 조건에서 재현
3. **정확한 위치**: 발생 명령어 식별 가능
4. **복귀 가능성**: 일부는 복귀 가능

```
Exception vs Interrupt:
Exception:
- 내부적 (CPU 내부)
- 동기적 (명령어 실행 중)
- 명령어와 연관
- 예: Divide by Zero

Interrupt:
- 외부적 (I/O 장치)
- 비동기적 (언제든)
- 현재 명령어 무관
- 예: Timer Tick
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 예외 분류

```
Exception Types:

1. Fault (결함):
   - 복귀 가능
   - 명령어 재실행 필요
   - 예: Page Fault

   동작:
   [Fault 발생]
   → Context Save
   → Handler 실행
   → 해결 (Page Load)
   → 명령어 재시작
   → 정상 실행

2. Trap (트랩):
   - 복귀 가능
   - 다음 명령어로 복귀
   - 디버깅 용도
   - 예: Breakpoint

   동작:
   [Trap 발생]
   → Context Save
   → Handler 실행 (디버거)
   → 다음 명령어로 복귀
   → 계속 실행

3. Abort (중단):
   - 복귀 불가
   - 프로그램 종료
   - 심각한 오류
   - 예: Machine Check

   동작:
   [Abort 발생]
   → Handler 실행
   → 프로그램 종료
   → 시스템 재시작

4. Terminate (종료):
   - 일부 아키텍처에서 Abort와 분리
   - 프로세스 강제 종료
```

### x86 예외

```
x86 Exception List:

┌──────────┬─────────────────────┬─────────┬──────────────┐
│ Vector   │ Name                │ Type    │ Description  │
├──────────┼─────────────────────┼─────────┼──────────────┤
│ 0        │ Divide Error        │ Fault   │ DIV/IDIV 오류│
│ 1        │ Debug               │ Fault/Trap│ Breakpoint │
│ 2        │ NMI                 │ Abort   │ Non-Maskable │
│ 3        │ Breakpoint          │ Trap    │ INT 3        │
│ 4        │ Overflow            │ Trap    │ INTO         │
│ 5        │ BOUND Range         │ Fault   │ BOUND        │
│ 6        │ Invalid Opcode      │ Fault   │ undefined op │
│ 7        │ Device Not Avail    │ Fault   │ FPU 없음     │
│ 8        │ Double Fault        │ Abort   │ 예외 중첩    │
│ 9        │ Coprocessor Seg Ovr │ Fault   │ x87 오류     │
│ 10       │ Invalid TSS         │ Fault   │ TSS 오류     │
│ 11       │ Segment Not Present │ Fault   │ Segment 없음 │
│ 12       │ Stack Fault         │ Fault   │ Stack 오류   │
│ 13       │ General Protection  │ Fault   │ GP Fault     │
│ 14       │ Page Fault          │ Fault   │ Page 없음    │
│ 16       │ x87 FP Error        │ Fault   │ FPU 오류     │
│ 17       │ Alignment Check     │ Fault   │ Alignment    │
│ 18       │ Machine Check       │ Abort   │ 하드웨어     │
│ 19       │ SIMD FP             │ Fault   │ SSE/AVX      │
└──────────┴─────────────────────┴─────────┴──────────────┘
```

### Divide Error (Vector 0)

```
나눗셈 오류:

원인:
- DIV/IDIV의 나누는 수가 0
- 몫이 레지스터 크기 초과

예:
MOV AX, 10
MOV CX, 0
DIV CL      ; AX / CX → AX (몫), DX (나머지)
            ; CX=0이므로 Divide Error

복귀:
- Fault로 처리
- 명령어 재시작 불가 (정의되지 않음)
- 일반적으로 프로그램 종료
```

### Debug Exception (Vector 1)

```
디버그 예외:

원인:
- 단일 스텝 실행 (TF=1)
- Breakpoint (INT 3)
- I/O Breakpoint
- Task Switch

DR7 (Debug Control):
- Breakpoint 설정
- 조건 지정
- 길이 지정

DR0-DR3 (Breakpoint Address):
- 최대 4개 Breakpoint

사용:
1. Breakpoint 설정 (DR0 = address)
2. DR7 설정 (enable)
3. TF 설정
4. 프로그램 실행
5. Breakpoint 감지 시 Exception 발생
6. Debugger로 제어 전달
```

### Breakpoint (Vector 3)

```
브레이크포인트 (INT 3):

특징:
- 1바이트 명령어 (0xCC)
- Trap으로 처리
- 다음 명령어로 복귀
- 소프트웨어 디버깅

동작:
1. 코드에 0xCC 삽입
2. 실행 중 INT 3 발생
3. Debugger 제어
4. 원래 바이트 복원
5. 계속 실행

소프�어 Breakpoint:
- INT 3 명령어 삽입
- 1바이트만 필요
- ROM에서 불가

하드웨어 Breakpoint:
- DR 레지스터 사용
- 코드 수정 불필요
- 개수 제한 (4개)
```

### Overflow (Vector 4)

```
오버플로우 예외:

명령어: INTO (Interrupt on Overflow)

동작:
- OF (Overflow Flag) 확인
- OF=1이면 Exception 발생
- OF=0이면 무시

예:
MOV AL, 127
ADD AL, 1      ; AL = 128, OF=1
INTO           ; Overflow Exception 발생

사용:
- 산술 연산 후 오버플로우 확인
- signed 연산 안전성 검사
```

### Invalid Opcode (Vector 6)

```
잘못된 명령어:

원인:
- 정의되지 않은 Opcode
- 잘못된 Operand
- 보호 모드 위반

예:
DB 0xFF       ; 정의되지 않은 명령어
MOV CS, AX    ; 일부 모드에서 허용 안 됨

처리:
- 일반적으로 프로그램 종료
- 에러 메시지 출력
- Emulator에서는 다른 동작 가능
```

### General Protection Fault (Vector 13)

```
일반 보호 오류 (GP Fault):

원인:
1. Segment Limit 초과
2. Privilege 위반
3. 쓰기 불가 영역에 쓰기
4. 읽기 불가 영역에서 읽기
5. 잘못된 Segment Selector

예:
MOV DS, 0x1234     ; 잘못된 Selector
MOV [0xFFFFFFFF], EAX  ; 잘못된 주소

세그먼트 관련:
- Segment Descriptor 오류
- CPL > DPL (Privilege 위반)
- Data Segment에서 Code 실행

처리:
- Windows: 일반적인 애플리케이션 크래시
- Linux: Segmentation Fault (SIGSEGV)
```

### Page Fault (Vector 14)

```
페이지 폴트:

원인:
1. 페이지가 물리 메모리에 없음
2. 접근 권한 위반

CR2 레지스터:
- 발생한 주소 저장

Error Code (Stack):
┌──┬───────────┬──────────────┬─────────┐
│P │W          │R            │U        │
│r │           │            │s        │
│o │(1=Write)  │(1=Read)    │(1=User) │
│t │           │            │         │
└──┴───────────┴──────────────┴─────────┘

P=0: 페이지 부재 (Demand Paging)
P=1: 접근 위반

W=1: 쓰기 시 발생
R=0: 읽기 시 발생

U=1: User 모드
U=0: Kernel 모드

처리:
1. CR2에서 주소 확인
2. 페이지 테이블 확인
3. 페이지 로드 (디스크 → 메모리)
4. 페이지 테이블 업데이트
5. 명령어 재시작

Demand Paging:
- 필요할 때만 로드
- 메모리 효율적
- Page Fault 빈번 가능
```

### Double Fault (Vector 8)

```
이중 폴트:

원인:
- Exception Handler 실행 중 또 다른 Exception 발생

예:
1. Page Fault 발생
2. Page Fault Handler 실행
3. Handler에서 Stack Fault 발생
4. Double Fault

동작:
- TS(Task State) 저장
- 별도의 Handler 실행
- 복귀 불가 (Abort)

Triple Fault:
- Double Fault Handler 실행 중 또 다른 Exception
- 시스템 재시작 (Shutdown)
```

### Stack Fault (Vector 12)

```
스택 폴트:

원인:
1. Stack Limit 초과
2. Stack Pointer 오류
3. Stack Segment가 없음

예:
MOV SP, 0x0000  ; Stack이 0x0000 미만으로
PUSH AX         ; Stack Fault

처리:
- Stack 재설정 필요
- 복구 어려움
```

### Alignment Check (Vector 17)

```
정렬 검사:

원인:
- Misaligned 메모리 접근
- 예: 4바이트 데이터가 4의 배수 아닌 주소

활성화:
- CR0.AM = 1
- EFLAGS.AC = 1
- CPL = 3 (User Mode)

예:
MOV EAX, [0x1001]  ; 4바이트가 홀수 주소
                    ; Alignment Check

영향:
- 성능 저하
- 일부 아키텍처에서만 지원
- x86: 선택적 (느림)
- RISC: 필수 (오류)
```

## Ⅲ. 융합 비교

### 예외 유형 비교

| 유형 | 복귀 | 재시작 | 용도 | 예시 |
|------|------|--------|------|------|
| Fault | 가능 | 명령어 | 복구 | Page Fault |
| Trap | 가능 | 다음 명령 | 디버깅 | Breakpoint |
| Abort | 불가 | - | 치명적 | Machine Check |

### x86 예외

| Vector | 이름 | 타입 | 발생 원인 |
|--------|------|------|-----------|
| 0 | Divide Error | Fault | ÷0 |
| 1 | Debug | Fault/Trap | TF=1, BP |
| 6 | Invalid Opcode | Fault | Unknown op |
| 13 | GP Fault | Fault | Protection |
| 14 | Page Fault | Fault | Page miss |
| 8 | Double Fault | Abort | Nested exception |

### 아키텍처별 예외

| 아키텍처 | Page Fault | Alignment | 단정 |
|----------|------------|-----------|------|
| x86 | Vector 14 | 선택적 | INTO |
| ARM | Data Abort | 필수 | BKPT |
| MIPS | TLB Refill | 필수 | TEQ |
| RISC-V | Load Page Fault | 필수 | EBREAK |

## Ⅳ. 실무 적용 및 기술사적 판단

### Page Fault 처리

```
Demand Paging:

1. 프로그램이 주소 접근
2. MMU: 페이지 테이블 확인
3. Present=0 → Page Fault
4. Exception Handler 실행
5. OS: 페이지 로드 결정
6. Disk → Memory 로드
7. 페이지 테이블 업데이트
8. 명령어 재시작

성능:
- Page Fault: 수백만 cycles
- Disk I/O: 밀리초 단위
- 4KB 페이지 기준

최적화:
- Prefetching
- Working Set 유지
- Large Pages (2MB, 1GB)
```

### Exception Handler

```
ExceptionHandler 구조:

ExceptionHandler:
  ; 1. Exception 정보 저장
  PUSH All_Regs
  PUSH Error_Code
  PUSH Vector_Number

  ; 2. 특정 Handler로 분기
  CALL SpecificHandler

  ; 3. 복귀 또는 종료
  TEST Fatal_Flag
  JNZ Terminate

  ; 4. 복귀 (Fault/Trap)
  POP Error_Code
  POP All_Regs
  IRET

Terminate:
  ; 프로그램 종료
  CALL ExitProcess
```

### 신호 처리 (Linux)

```
Signal vs Exception:

Exception (Hardware):
- CPU가 감지
- 비동기적 전환
- Kernel에서 먼저 처리

Signal (Software):
- Kernel → Process
- POSIX 표준
- 예: SIGSEGV, SIGFPE

매핑:
Page Fault → SIGSEGV (가용 메모리 없음)
           → SIGBUS (액세스 위반)
Divide Error → SIGFPE
Invalid Opcode → SIGILL

Handler:
signal(SIGSEGV, handler);
sigaction(SIGSEGV, &act, NULL);
```

### C++ Exception

```
소프트웨어 예외 (High-Level):

try {
    int* p = nullptr;
    *p = 10;         ; Hardware Exception
} catch (std::exception& e) {
    ; Handler
}

HW → SW 변환:
1. CPU: Page Fault 발생
2. OS: Signal 전송 (SIGSEGV)
3. Runtime: C++ exception 변환
4. catch 블록 실행

Stack Unwinding:
- 소멸자 호출
- Stack Frame 정리
- 예외 전파
```

### 성능 고려사항

```
Exception Overhead:

Page Fault:
- 첫 접근: 10-100ms (Disk I/O)
- 재접근: 100ns (Memory)

Alignment Fixup:
- x86: 하드웨어 자동 수정 (느림)
- RISC: Exception → 소프트웨어 수정

최적화:
1. 항상 정렬된 접근
2. Prefetching
3. mlock() (Page Lock)
4. Large Pages
```

## Ⅴ. 기대효과 및 결론

예외 처리는 CPU의 비정상 상황을 다루는 메커니즘이다. Fault/Trap/Abort 구분과 적절한 Handler가 중요하다.

```python
"""
예외 처리 시뮬레이션
Exception Handling Simulator
"""

class Exception:
    """예외 정의"""

    def __init__(self, vector, name, exc_type, description):
        self.vector = vector
        self.name = name
        self.type = exc_type  # 'fault', 'trap', 'abort'
        self.description = description

    def __repr__(self):
        return f"Exception(0x{self.vector:02X}, {self.name}, {self.type})"


# x86 예외 정의
EXCEPTIONS = {
    0: Exception(0, "Divide Error", "fault", "Division by zero"),
    1: Exception(1, "Debug", "fault", "Debug exception"),
    3: Exception(3, "Breakpoint", "trap", "Breakpoint (INT 3)"),
    4: Exception(4, "Overflow", "trap", "Overflow (INTO)"),
    6: Exception(6, "Invalid Opcode", "fault", "Undefined opcode"),
    8: Exception(8, "Double Fault", "abort", "Nested exception"),
    12: Exception(12, "Stack Fault", "fault", "Stack limit exceeded"),
    13: Exception(13, "General Protection", "fault", "Protection violation"),
    14: Exception(14, "Page Fault", "fault", "Page not present"),
    16: Exception(16, "x87 FP Error", "fault", "FPU error"),
    17: Exception(17, "Alignment Check", "fault", "Misaligned access"),
    18: Exception(18, "Machine Check", "abort", "Hardware error"),
}


class CPU:
    """CPU 시뮬레이션"""

    def __init__(self):
        self.pc = 0
        self.sp = 0x1000
        self.flags = {'CF': 0, 'PF': 0, 'AF': 0, 'ZF': 0, 'SF': 0, 'TF': 0, 'IF': 0, 'DF': 0, 'OF': 0}
        self.regs = {f'R{i}': 0 for i in range(16)}
        self.memory = {}
        self.stack = []
        self.cr2 = 0  # Page Fault Address
        self.in_handler = False
        self.exception_depth = 0

    def execute(self, opcode, operands=None):
        """명령어 실행"""
        self.pc += 1

        # Divide by Zero
        if opcode == 'DIV' and operands and operands[1] == 0:
            self.raise_exception(0)

        # Invalid Opcode
        if opcode == 'INVALID':
            self.raise_exception(6)

        # Overflow
        elif opcode == 'ADDO' and operands:
            result = operands[0] + operands[1]
            if result > 0x7FFFFFFF:
                self.flags['OF'] = 1
            if self.flags['OF'] and opcode == 'ADDO':
                self.raise_exception(4)

        # Breakpoint
        elif opcode == 'INT3':
            self.raise_exception(3)

        # Page Fault
        elif opcode == 'MEM':
            addr = operands[0] if operands else 0
            if not self.page_present(addr):
                self.cr2 = addr
                self.raise_exception(14, error_code=0)

        # General Protection
        elif opcode == 'PRIVILEGE':
            self.raise_exception(13)

        # Stack Overflow
        elif opcode == 'PUSH' and operands:
            if self.sp < 0x100:
                self.raise_exception(12)

    def page_present(self, addr):
        """페이지 존재 확인"""
        # 시뮬레이션: 0x1000-0x1FFF만 존재
        return 0x1000 <= addr < 0x2000

    def raise_exception(self, vector, error_code=0):
        """예외 발생"""
        if vector not in EXCEPTIONS:
            print(f"Unknown exception: 0x{vector:02X}")
            return

        exc = EXCEPTIONS[vector]

        # Double Fault 확인
        if self.in_handler:
            self.exception_depth += 1
            if self.exception_depth >= 2:
                print(f"\n[CRITICAL] Triple Fault - System Shutdown")
                self.exception_depth = 0
                return

            print(f"\n[DOUBLE FAULT] Handler 내에서 또 다른 예외!")
            self.exception_handler(EXCEPTIONS[8])
            return

        print(f"\n[EXCEPTION 0x{vector:02X}] {exc.name} ({exc.type})")
        print(f"  PC = 0x{self.pc:04X}")
        print(f"  Description: {exc.description}")

        if vector == 14:
            print(f"  CR2 (Fault Address) = 0x{self.cr2:04X}")

        self.exception_handler(exc)

    def exception_handler(self, exc):
        """예외 처리기"""
        self.in_handler = True

        print(f"\n[HANDLER] Exception 0x{exc.vector:02X} 처리 시작")

        # Context Save
        context = {
            'pc': self.pc,
            'flags': self.flags.copy(),
            'regs': self.regs.copy()
        }
        self.stack.append(context)

        # 예외 타입별 처리
        if exc.type == 'fault':
            print(f"  Type: Fault - 복귀 가능")
            if exc.vector == 14:  # Page Fault
                print(f"  Action: 페이지 로드 및 명령어 재시작")
                self.memory[self.cr2] = 0  # 페이지 할당
            elif exc.vector == 0:  # Divide Error
                print(f"  Action: 복구 불가 - 프로그램 종료")
                self.terminate()
            else:
                print(f"  Action: 복구 시도")
                self.restore_context(context)

        elif exc.type == 'trap':
            print(f"  Type: Trap - 디버깅/프로파일링")
            if exc.vector == 3:  # Breakpoint
                print(f"  Action: 디버거 제어 전달")
            self.restore_context(context)

        elif exc.type == 'abort':
            print(f"  Type: Abort - 복구 불가")
            self.terminate()

        self.in_handler = False

    def restore_context(self, context):
        """컨텍스트 복원"""
        self.pc = context['pc']
        self.flags = context['flags']
        self.regs = context['regs']
        print(f"  Context restored - PC=0x{self.pc:04X}")

    def terminate(self):
        """프로그램 종료"""
        print(f"\n[TERMINATE] Program terminated due to exception")
        self.in_handler = False
        self.exception_depth = 0


def demo_divide_error():
    """나눗셈 오류"""

    print("=" * 70)
    print("Divide Error (Vector 0)")
    print("=" * 70)

    cpu = CPU()

    print("\n>>> MOV AX, 10")
    print(">>> MOV CX, 0")
    print(">>> DIV CX")

    cpu.regs['R0'] = 10
    cpu.regs['R1'] = 0
    cpu.execute('DIV', [10, 0])


def demo_invalid_opcode():
    """잘못된 명령어"""

    print("\n\n" + "=" * 70)
    print("Invalid Opcode (Vector 6)")
    print("=" * 70)

    cpu = CPU()

    print("\n>>> DB 0xFF  (undefined opcode)")
    cpu.execute('INVALID')


def demo_breakpoint():
    """브레이크포인트"""

    print("\n\n" + "=" * 70)
    print("Breakpoint (Vector 3)")
    print("=" * 70)

    cpu = CPU()

    print("\n>>> INT 3  (breakpoint)")
    cpu.execute('INT3')


def demo_page_fault():
    """페이지 폴트"""

    print("\n\n" + "=" * 70)
    print("Page Fault (Vector 14)")
    print("=" * 70)

    cpu = CPU()

    print("\n>>> MOV EAX, [0x5000]  (not present)")
    cpu.execute('MEM', [0x5000])

    print("\n>>> MOV EAX, [0x1000]  (present)")
    cpu.execute('MEM', [0x1000])


def demo_double_fault():
    """이중 폴트"""

    print("\n\n" + "=" * 70)
    print("Double Fault (Vector 8)")
    print("=" * 70)

    cpu = CPU()

    # Handler에서 예외 발생 시뮬레이션
    print("\n>>> Page Fault → Handler 내에서 Divide Error")

    # Handler 설정 (simulate)
    cpu.in_handler = True

    # Page Fault 발생 (Handler 내)
    cpu.cr2 = 0x5000
    cpu.raise_exception(14)


def demo_comparison():
    """비교"""

    print("\n\n" + "=" * 70)
    print("예외 처리 비교")
    print("=" * 70)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Exception Types                                 │
    ├─────────────────┬──────────┬───────────┬───────────────────────────┤
    │ Type            │ 복귀     │ 재시작    │ 예시                      │
    ├─────────────────┼──────────┼───────────┼───────────────────────────┤
    │ Fault           │ 가능     │ 명령어    │ Page Fault, GP Fault      │
    │                 │          │           │ Divide Error (일부)       │
    ├─────────────────┼──────────┼───────────┼───────────────────────────┤
    │ Trap            │ 가능     │ 다음 명령 │ Breakpoint, Overflow      │
    │                 │          │           │ Debug                     │
    ├─────────────────┼──────────┼───────────┼───────────────────────────┤
    │ Abort           │ 불가     │ -         │ Machine Check,           │
    │                 │          │           │ Double Fault, Triple Fault│
    └─────────────────┴──────────┴───────────┴───────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    x86 Exception Vectors                            │
    ├──────┬───────────────────┬─────────┬───────────────────────────────┤
    │Vector│ Name              │ Type    │ Description                   │
    ├──────┼───────────────────┼─────────┼───────────────────────────────┤
    │ 0    │ Divide Error      │ Fault   │ ÷0, 몫 오버플로우             │
    │ 1    │ Debug             │ F/T     │ TF=1, Breakpoint              │
    │ 3    │ Breakpoint        │ Trap    │ INT 3                         │
    │ 4    │ Overflow          │ Trap    │ INTO (OF=1)                   │
    │ 6    │ Invalid Opcode    │ Fault   │ 정의되지 않은 Opcode          │
    │ 8    │ Double Fault      │ Abort   │ Handler 중 Exception         │
    │ 12   │ Stack Fault       │ Fault   │ Stack Limit 초과              │
    │ 13   │ General Protection│ Fault   │ Protection 위반               │
    │ 14   │ Page Fault        │ Fault   │ Page 부재/위반               │
    │ 16   │ x87 FP Error      │ Fault   │ FPU 오류                      │
    │ 17   │ Alignment Check   │ Fault   │ Misaligned access             │
    │ 18   │ Machine Check     │ Abort   │ 하드웨어 오류                 │
    └──────┴───────────────────┴─────────┴───────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Exception Handling Flow                         │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  [Exception 발생]                                                   │
    │       ↓                                                             │
    │  [현재 명령어 위치 저장]                                            │
    │       ↓                                                             │
    │  [Flags 저장]                                                       │
    │       ↓                                                             │
    │  [IDT에서 Handler 주소 획득]                                        │
    │       ↓                                                             │
    │  [Handler 실행]                                                     │
    │       ↓                                                             │
    │  [Fault: 복구 후 재시작]                                           │
    │  [Trap: 다음 명령어로]                                             │
    │  [Abort: 종료]                                                      │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Page Fault Detail                               │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │  CR2: Fault Address                                                 │
    │  Error Code:                                                        │
    │    bit 0 (P): 0 = Page 부재, 1 = Protection 위반                    │
    │    bit 1 (W): 0 = Read, 1 = Write                                  │
    │    bit 2 (U): 0 = Kernel, 1 = User                                 │
    │                                                                     │
    │  Demand Paging:                                                     │
    │    1. Page Fault 발생                                               │
    │    2. OS가 페이지 로드 (Disk → Memory)                              │
    │    3. Page Table 업데이트 (Present=1)                               │
    │    4. 명령어 재시작                                                 │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_divide_error()
    demo_invalid_opcode()
    demo_breakpoint()
    demo_page_fault()
    demo_double_fault()
    demo_comparison()
