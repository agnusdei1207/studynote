+++
title = "인터럽트 처리 (Interrupt Handling)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 인터럽트 처리 (Interrupt Handling)

## 핵심 인사이트 (3줄 요약)
1. 인터럽트(Interrupt)는 CPU가 현재 실행 중인 프로그램을 일시 중단하고 긴급한 이벤트를 처리하는 메커니즘으로, Hardware Interrupt와 Software Interrupt가 있다
2. 기술사시험에서는 인터럽트 종류, Vector Table, Priority, Nested Interrupt, Context Saving/Restoring이 핵심이다
3. 인터럽트 처리 과정은 Request → Acknowledge → Context Save → ISR 실행 → Context Restore → Return 순으로 진행된다

## Ⅰ. 개요 (500자 이상)

인터럽트(Interrupt)는 **CPU가 정상적인 명령어 실행 흐름을 중단하고, 긴급한 이벤트를 처리하기 위해 제어를 ISR(Interrupt Service Routine)로 전달하는 하드웨어/소프트웨어 메커니즘**이다. 폰 노이만 구조에서 I/O 처리의 핵심이다.

```
인터럽트 기본 개념:
정의: CPU의 현재 실행 흐름 변경 요구
목적: 긴급 이벤트 처리, I/O 효율화
특징: 비동기적, 우선순위 기반

구성:
1. Interrupt Source: 인터럽트 발생원
2. Interrupt Controller: 우선순위 판정
3. Vector Table: ISR 주소 테이블
4. ISR: 인터럽트 처리 루틴

장점:
- CPU 효율 향상 (Polling 불필요)
- 빠른 응답 시간
- 다중 이벤트 처리 가능
- 실시간 처리 지원
```

**인터럽트의 핵심 요소:**

1. **비동기성**: 예측 불가능한 시점에 발생
2. **우선순위**: 중요도에 따른 처리 순서
3. **자동 Context Save**: 레지스터 자동 저장
4. **벡터화된 처리**: 빠른 ISR 분기

```
Interrupt vs Polling:
Interrupt:
- 하드웨어 주도
- CPU 대기 없음
- 빠른 응답
- 복잡한 구현

Polling:
- 소프트웨어 주도
- CPU 순환 확인
- 응답 지연
- 단순한 구현
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 인터럽트 종류

```
인터럽트 분류:

1. Hardware Interrupt (하드웨어 인터럽트):
   - 외부 장치에서 발생
   - 비동기적 발생
   - 예: 키보드 입력, 타이머, 디스크 완료

   ┌─────────────────────────────────┐
   │         CPU                     │
   │  ┌──────────────────────────┐  │
   │  │   Current Program        │  │
   │  └──────────────────────────┘  │
   │            ↑ Interrupt          │
   │  ┌───────┴──────────────────┐  │
   │  │   ISR                    │  │
   │  └──────────────────────────┘  │
   └─────────────────────────────────┘
         ↑              ↑
    Timer        Keyboard, Disk

2. Software Interrupt (소프트웨어 인터럽트):
   - 프로그램에 의한 명시적 호출
   - 동기적 발생
   - 예: 시스템 콜, 예외 처리

   INT 0x80   ; Linux 시스템 콜
   INT 0x21   ; DOS 인터럽트
   INT 3      ; Breakpoint

3. Internal Interrupt (내부 인터럽트/Exception):
   - CPU 내부에서 발생
   - 프로그램 실행 중 오류
   - 예: Divide by Zero, Page Fault

   Division by Zero
   Invalid Opcode
   Protection Fault
   Page Fault
```

### 인터럽트 처리 과정

```
인터럽트 처리 순서:

1. Interrupt Request (INTR):
   외부 장치가 INTR 신호를 CPU로 전송

2. Interrupt Acknowledge (INTA):
   CPU가 현재 명령어 완료 후 INTA 신호 전송

3. Vector Number 수신:
   Interrupt Controller가 Vector Number 전달

4. Context Save:
   - PC, PSW(Priority/Status Word) Stack에 PUSH
   - 자동으로 수행됨

5. ISR 호출:
   Vector Table에서 ISR 주소 획득
   PC ← ISR Address

6. ISR 실행:
   인터럽트 처리 루틴 실행
   - 레지스터 저장 (PUSH)
   - 이벤트 처리
   - 레지스터 복원 (POP)

7. Context Restore:
   Stack에서 PC, PSW 복원

8. IRET (Interrupt Return):
   원래 프로그램 재개

시간 순서:
T0: CPU 실행 중
T1: INTR 신호
T2: INTA (명령어 완료 후)
T3: Vector 수신
T4: Context Save (2-3 cycles)
T5: ISR Jump
T6: ISR 실행 (가변)
T7: IRET
T8: 원래 프로그램 재개
```

### Interrupt Vector Table

```
인터럽트 벡터 테이블 (IVT):

구조:
- 메모리의 고정 위치 (시작 주소)
- 각 Vector는 ISR 주소 저장
- 256개 Vector (0-255)

x86 (Real Mode):
주소: 0x0000 - 0x03FF
크기: 1024 bytes (256 × 4)
각 Vector: 4 bytes (Segment:Offset)

┌─────────────────────────────────┐
│  Vector 0: Divide by Zero       │ → ISR0
├─────────────────────────────────┤
│  Vector 1: Debug                │ → ISR1
├─────────────────────────────────┤
│  Vector 2: NMI                  │ → ISR2
├─────────────────────────────────┤
│  ...                            │
├─────────────────────────────────┤
│  Vector 8: Double Fault         │ → ISR8
├─────────────────────────────────┤
│  ...                            │
├─────────────────────────────────┤
│  Vector 0x21: DOS               │ → ISR21h
├─────────────────────────────────┤
│  Vector 0x80: Linux System Call │ → ISR80h
└─────────────────────────────────┘

IDT (Interrupt Descriptor Table, Protected Mode):
- 8 bytes per entry
- Segment Selector + Offset
- Privilege Level 정보
- Type 정보 (Trap/Interrupt/Task Gate)
```

### Interrupt Controller

```
PIC (Programmable Interrupt Controller):

역할:
1. 여러 IRQ를 하나의 INTR로 묶음
2. 우선순위 판정
3. Vector Number 할당
4. Masking 지원

8259 PIC Structure:

┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│IRQ0 │IRQ1 │IRQ2 │IRQ3 │IRQ4 │IRQ5 │IRQ6 │IRQ7 │
└──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┘
   │     │     │     │     │     │     │     │
  Timer  KBD   PIC2 COM2 COM1  LPT2  LPT1  FDC
   │     │     │     │     │     │     │     │
   └─────┴─────┴─────┴─────┴─────┴─────┴─────┘
                   ↓
              Priority Resolver
                   ↓
              Interrupt to CPU
                   ↓
              Vector Number

IRQ 할당 (x86):
IRQ0: System Timer (PIT)
IRQ1: Keyboard
IRQ2: Cascade (PIC2)
IRQ3: COM2
IRQ4: COM1
IRQ5: LPT2
IRQ6: Floppy
IRQ7: LPT1

APIC (Advanced PIC):
- 각 CPU에 Local APIC
- I/O APIC에서 외부 장치 연결
- Multiprocessor 지원
```

### Interrupt Priority

```
인터럽트 우선순위:

x86 Priority (높은 순):
1. Exception (내부 인터럽트)
   - Divide by Zero
   - Page Fault
   - Protection Fault

2. NMI (Non-Maskable Interrupt)
   - 하드웨어 오류
   - 메모리 패리티 오류
   - 마스크 불가

3. Maskable Interrupt (INTR)
   - I/O 완료
   - 타이머
   - 마스크 가능

우선순위 결정:
1. 고정 우선순위 (Fixed Priority)
   - 낮은 IRQ가 높은 우선순위

2. 회전 우선순위 (Rotating Priority)
   - 서비스 후 우선순위 변경
   - Starvation 방지

3. 동적 우선순위 (Dynamic Priority)
   - 상황에 따라 변경
```

### Nested Interrupt

```
중첩 인터럽트 (Nested Interrupt):

정의:
- ISR 실행 중 더 높은 우선순위 인터럽트 허용

동작:
1. ISR 실행 중
2. 높은 우선순위 인터럽트 발생
3. 현재 ISR 중단
4. Context Save (현재 상태)
5. 새로운 ISR 실행
6. 완료 후 복귀
7. 원래 ISR 재개

스택 변화:

┌────────────────────────┐
│     User Program       │
├────────────────────────┤
│     Return Addr        │
├────────────────────────┤
│     Flags              │
├────────────────────────┤ ← ISR1 진입
│     ISR1 Context       │
├────────────────────────┤ ← ISR2 중첩
│     Return Addr        │
├────────────────────────┤
│     Flags              │
├────────────────────────┤
│     ISR2 Context       │
└────────────────────────┘

주의:
- 무한 중첩 방지
- Stack Overflow 확인
- 재진입 가능한 ISR 필요
```

### Context Saving

```
컨텍스트 저장 (Context Saving):

자동 저장 (Hardware):
- PC (Program Counter)
- PSW (Processor Status Word)
  - Flag 레지스터
  - Interrupt Enable bit

수동 저장 (Software ISR):
PUSH AX       ; 범용 레지스터
PUSH BX
PUSH CX
PUSH DX
PUSH SI
PUSH DI
PUSH BP
PUSH DS
PUSH ES

... ISR Code ...

POP ES        ; 역순 복원
POP DS
POP BP
POP DI
POP SI
POP DX
POP CX
POP BX
POP AX
IRET          ; PC, Flags 자동 복원
```

### Interrupt Masking

```
인터럽트 마스킹 (Interrupt Masking):

목적:
- 중요한 작업 중 인터럽트 차단
- Race Condition 방지

x86:
CLI           ; Clear Interrupt Flag (Disable)
... Critical Section ...
STI           ; Set Interrupt Flag (Enable)

IMR (Interrupt Mask Register):
- 각 IRQ별 Masking
- 1: Masked (Disable)
- 0: Unmasked (Enable)

예:
IMR = 0xFF   ; 모두 Masked
IMR = 0xFE   ; IRQ0만 Enable
IMR = 0x00   ; 모두 Enable

주의:
- NMI는 마스킹 불가
- Exception은 항상 발생
```

### Software Interrupt

```
소프트웨어 인터럽트 (Software Interrupt):

용도:
1. 시스템 콜 (System Call)
2. 디버깅 (Breakpoint)
3. 가상화 (VM Exit)

x86:
INT n        ; n번 Vector 호출
  - n: 0-255

예:
; Linux System Call (32-bit)
MOV EAX, 4   ; sys_write
MOV EBX, 1   ; stdout
MOV ECX, msg ; buffer
MOV EDX, len ; length
INT 0x80

; DOS System Call
MOV AH, 9    ; print string
MOV DX, msg
INT 0x21

; Breakpoint
INT 3

ARMv7:
SWI 0x80     ; Software Interrupt

ARMv8:
SVC #0       ; Supervisor Call
```

## Ⅲ. 융합 비교

### 인터럽트 vs 폴링

| 특성 | Interrupt | Polling |
|------|-----------|---------|
| CPU 효율 | 높음 | 낮음 |
| 응답 시간 | 빠름 | 느림 |
| 구현 복잡도 | 높음 | 낮음 |
| 하드웨어 | 필요 | 안 함 |
| 우선순위 | 지원 | 수동 |

### 인터럽트 종류

| 종류 | 발생원 | 예시 | 마스킹 |
|------|--------|------|--------|
| Hardware | 외부 장치 | Timer, KBD | 가능 |
| Software | INT 명령 | System Call | 불가 |
| Exception | CPU 내부 | Divide Error | 불가 |
| NMI | 긴급 이벤트 | Power Fail | 불가 |

### 인터럽트 제어기

| 제어기 | CPU 수 | IRQ 수 | 특징 |
|--------|--------|--------|------|
| 8259 PIC | 1 | 8 (Cascade 15) | Legacy |
| APIC | 다중 | 256+ | Multiprocessor |
| GIC | 다중 | 1020+ | ARM |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86 인터럽트 처리

```
x86 Interrupt Handling:

1. 인터럽트 발생:
   INTR 신호 → CPU

2. 현재 명령어 완료 후:
   - IF=1 확인 (Interrupt Flag)
   - INTA 신호 전송

3. Vector 수신:
   - 8259가 Vector Number 전송
   - 예: IRQ 0 → Vector 8

4. Context Save (자동):
   PUSHF         ; Flags
   PUSH CS       ; Code Segment
   PUSH IP       ; Instruction Pointer
   IF ← 0        ; Disable interrupt

5. ISR 호출:
   - IDT[Vector] → Offset:Segment
   - JMP ISR

6. ISR 실행:
   PUSH AX
   PUSH ...
   ... 처리 ...
   POP ...
   POP AX

7. 복귀:
   IRET          ; POP IP, CS, Flags

타이밍:
명령어 완료: T
Context Save: 2-3T
ISR Jump: 1T
ISR 실행: 가변
IRET: 2T
```

### ARM 인터럽트 처리

```
ARM Interrupt Handling:

인터럽트 모드:
1. IRQ (Interrupt Request)
   - 일반 인터럽트
   - CPSR.I=0일 때만

2. FIQ (Fast Interrupt Request)
   - 고속 인터럽트
   - 더 높은 우선순위
   - 전용 레지스터 (R8_fiq-R14_fiq)

동작 (IRQ):
1. 인터럽트 감지
2. 현재 상태 저장:
   - CPSR → SPSR_irq
   - PC → LR_irq
   - CPSR 모드 변경 → IRQ
3. IRQ Handler 실행
4. 복귀:
   - SPSR_irq → CPSR
   - LR_irq - 4 → PC

ARMv8 (Exception Level):
EL0: User
EL1: OS Kernel
EL2: Hypervisor
EL3: Secure Monitor
```

### 인터럽트 지연 시간

```
Interrupt Latency:

정의:
인터럽트 발생부터 ISR 시작까지 시간

구성:
1. Recognition Latency:
   - CPU가 인터럽트 인지 시간
   - 최대 1 명령어

2. Synchronization Latency:
   - 현재 명령어 완료까지
   - 최대 명령어 실행 시간

3. Context Save:
   - Push/Pop 시간
   - 2-10 cycles

4. ISR Dispatch:
   - Vector Lookup
   - Jump

총 지연:
Latency = Sync + Context + Dispatch
         = 1-1000+ cycles

최적화:
- 짧은 명령어 사용
- 인터럽트 허용 구간 확대
- 자동 Context Save 하드웨어
```

### 실시간 시스템

```
Real-Time Interrupt:

요구사항:
1. 결정론적 응답 시간
2. 최대 지연 시간 보장
3. 우선순위 기반 스케줄링

RTLinux (Real-Time Linux):
- 하드 실시간 지원
- 인터럽트 핸들러 우선순위
- Preemptible Kernel

RTOS (Real-Time OS):
- uC/OS, FreeRTOS, VxWorks
- 빠른 인터럽트 응답
- Deterministic scheduling
```

## Ⅴ. 기대효과 및 결론

인터럽트는 CPU와 I/O 장치 간의 비동기 통신 메커니즘이다. 효율적인 처리를 위해 Vector Table, Priority, Nested Interrupt가 필요하다.

```python
"""
인터럽트 처리 시뮬레이션
Interrupt Handling Simulator
"""

class InterruptController:
    """인터럽트 제어기"""

    def __init__(self, num_irq=8):
        self.num_irq = num_irq
        self.irq_pending = [False] * num_irq
        self.irq_mask = [False] * num_irq  # True = Masked
        self.vector_base = 32
        self.priority = list(range(num_irq))  # 낮은 번호가 높은 우선순위

    def request(self, irq):
        """IRQ 요청"""
        if 0 <= irq < self.num_irq:
            self.irq_pending[irq] = True
            return self.check_interrupt()
        return None

    def mask(self, irq, enable=True):
        """IRQ 마스킹"""
        if 0 <= irq < self.num_irq:
            self.irq_mask[irq] = enable

    def check_interrupt(self):
        """처리할 인터럽트 확인"""
        for irq in self.priority:
            if self.irq_pending[irq] and not self.irq_mask[irq]:
                return self.vector_base + irq
        return None

    def ack(self, irq):
        """인터럽트 완료 확인"""
        if 0 <= irq < self.num_irq:
            self.irq_pending[irq] = False

    def get_state(self):
        """현재 상태"""
        return {
            'pending': [i for i, p in enumerate(self.irq_pending) if p],
            'masked': [i for i, m in enumerate(self.irq_mask) if m],
            'pending_masked': [i for i in range(self.num_irq)
                              if self.irq_pending[i] and self.irq_mask[i]]
        }


class InterruptHandler:
    """인터럽트 처리기"""

    def __init__(self):
        self.ic = InterruptController(8)
        self.pc = 0
        self.stack = []
        self.flag_interrupt = True  # IF (Interrupt Flag)
        self.nesting_level = 0
        self.max_nesting = 5

        # ISR 루틴
        self.isr_table = {}
        for i in range(8):
            self.isr_table[32 + i] = self._default_isr(i)

    def _default_isr(self, irq):
        """기본 ISR"""
        def isr():
            print(f"    [ISR] Handling IRQ{irq}")
        return isr

    def register_isr(self, vector, isr):
        """ISR 등록"""
        self.isr_table[vector] = isr

    def interrupt_request(self, irq):
        """인터럽트 요청 (외부 장치)"""
        print(f"\n[IRQ{irq}] Request from device")
        vector = self.ic.request(irq)
        if vector is not None:
            print(f"  → Vector 0x{vector:02X} generated")
            return vector
        else:
            print(f"  → Masked or no pending")
            return None

    def check_and_handle(self):
        """인터럽트 확인 및 처리"""
        if not self.flag_interrupt:
            return False

        # PIC에서 확인
        vector = self.ic.check_interrupt()
        if vector is not None:
            irq = vector - self.ic.vector_base
            self._handle_interrupt(irq, vector)
            return True
        return False

    def _handle_interrupt(self, irq, vector):
        """인터럽트 처리"""
        print(f"\n[CPU] Interrupt at PC=0x{self.pc:04X}")
        print(f"  Vector: 0x{vector:02X}, IRQ: {irq}")

        # 1. Context Save
        self._context_save()

        # 2. Disable Interrupt
        old_if = self.flag_interrupt
        self.flag_interrupt = False

        # 3. ISR 실행
        print(f"  [ENTER] ISR (Nesting: {self.nesting_level})")
        isr = self.isr_table.get(vector)
        if isr:
            isr()

        # 4. Enable Interrupt
        self.flag_interrupt = old_if

        # 5. Context Restore
        self._context_restore()

        # 6. ACK
        self.ic.ack(irq)

        print(f"  [EXIT] ISR, Return to PC=0x{self.pc:04X}")

    def _context_save(self):
        """컨텍스트 저장"""
        context = {'pc': self.pc, 'flags': self.flag_interrupt}
        self.stack.append(context)
        self.nesting_level += 1
        print(f"  Context saved: PC=0x{self.pc:04X}")

    def _context_restore(self):
        """컨텍스트 복원"""
        if self.stack:
            context = self.stack.pop()
            self.pc = context['pc']
            self.nesting_level -= 1
            print(f"  Context restored: PC=0x{self.pc:04X}")

    def cli(self):
        """인터럽트 비활성화"""
        self.flag_interrupt = False
        print(f"\n[CLI] Interrupt Disabled (IF=0)")

    def sti(self):
        """인터럽트 활성화"""
        self.flag_interrupt = True
        print(f"\n[STI] Interrupt Enabled (IF=1)")

    def execute_instruction(self, cycles=1):
        """명령어 실행"""
        for _ in range(cycles):
            # 인터럽트 확인
            if self.check_and_handle():
                continue

            # 명령어 실행
            print(f"  [PC=0x{self.pc:04X}] Executing instruction")
            self.pc += 1

    def dump_state(self):
        """상태 출력"""
        state = self.ic.get_state()
        print(f"\n=== Interrupt Controller State ===")
        print(f"Pending IRQs: {state['pending'] if state['pending'] else 'None'}")
        print(f"Masked IRQs: {state['masked'] if state['masked'] else 'None'}")
        print(f"Pending but Masked: {state['pending_masked'] if state['pending_masked'] else 'None'}")
        print(f"CPU IF={int(self.flag_interrupt)}")


def demo_basic_interrupt():
    """기본 인터럽트 처리"""

    print("=" * 70)
    print("기본 인터럽트 처리 (Basic Interrupt Handling)")
    print("=" * 70)

    handler = InterruptHandler()

    # ISR 등록
    def timer_isr():
        print("    [ISR Timer] System tick")

    def keyboard_isr():
        print("    [ISR Keyboard] Key press detected")

    handler.register_isr(32, timer_isr)      # IRQ0 = Vector 32
    handler.register_isr(33, keyboard_isr)   # IRQ1 = Vector 33

    # 명령어 실행
    print("\n### CPU 실행 중...")
    for i in range(3):
        handler.execute_instruction(2)

        # 인터럽트 발생
        if i == 0:
            handler.interrupt_request(0)  # Timer
        elif i == 1:
            handler.interrupt_request(1)  # Keyboard

    handler.dump_state()


def demo_priority():
    """우선순위 처리"""

    print("\n\n" + "=" * 70)
    print("인터럽트 우선순위 (Interrupt Priority)")
    print("=" * 70)

    handler = InterruptHandler()

    # ISR 등록
    handler.register_isr(32, lambda: print("    [ISR0] High priority"))
    handler.register_isr(33, lambda: print("    [ISR1] Lower priority"))

    # 동시 인터럽트 요청
    print("\n### 동시 인터럽트 요청 (IRQ0, IRQ1)")
    handler.interrupt_request(0)
    handler.interrupt_request(1)

    # 처리
    print("\n### 인터럽트 처리")
    handler.execute_instruction(1)

    # 두 번째 인터럽트
    print("\n### 다음 인터럽트")
    handler.execute_instruction(1)


def demo_nested_interrupt():
    """중첩 인터럽트"""

    print("\n\n" + "=" * 70)
    print("중첩 인터럽트 (Nested Interrupt)")
    print("=" * 70)

    handler = InterruptHandler()

    # 중첩 가능한 ISR
    def nested_isr():
        if handler.nesting_level == 1:
            print("    [ISR1] Enabling interrupt for nesting")
            handler.sti()
            handler.execute_instruction(1)  # 다른 인터럽트 허용
            print("    [ISR1] Disabling interrupt")
        else:
            print("    [ISR0] Inner interrupt")

    handler.register_isr(32, nested_isr)
    handler.register_isr(33, lambda: print("    [ISR1] Lower priority"))

    # 첫 번째 인터럽트
    print("\n### IRQ0 발생")
    handler.interrupt_request(0)
    handler.execute_instruction(1)


def demo_masking():
    """인터럽트 마스킹"""

    print("\n\n" + "=" * 70)
    print("인터럽트 마스킹 (Interrupt Masking)")
    print("=" * 70)

    handler = InterruptHandler()

    # 마스킹
    print("\n### IRQ0 마스킹")
    handler.ic.mask(0, enable=True)
    handler.dump_state()

    # 요청하지만 마스킹됨
    print("\n### IRQ0 요청 (마스킹됨)")
    handler.interrupt_request(0)
    handler.execute_instruction(1)

    # 언마스크
    print("\n### IRQ0 언마스크")
    handler.ic.mask(0, enable=False)
    handler.dump_state()

    # 새로운 요청
    print("\n### IRQ0 요청 (허용됨)")
    handler.interrupt_request(0)
    handler.execute_instruction(1)


def demo_cli_sti():
    """CLI/STI 명령어"""

    print("\n\n" + "=" * 70)
    print("CLI/STI (Interrupt Enable/Disable)")
    print("=" * 70)

    handler = InterruptHandler()

    # 인터럽트 활성화 상태
    print("\n### 초기 상태 (IF=1)")
    handler.dump_state()

    # 인터럽트 발생
    print("\n### IRQ0 요청")
    handler.interrupt_request(0)
    handler.execute_instruction(1)

    # CLI로 비활성화
    print("\n### CLI 실행")
    handler.cli()

    # 인터럽트 무시
    print("\n### IRQ1 요청 (무시됨)")
    handler.interrupt_request(1)
    handler.execute_instruction(1)

    # STI로 활성화
    print("\n### STI 실행")
    handler.sti()

    # 인터럽트 처리
    print("\n### 인터럽트 처리")
    handler.execute_instruction(1)


def demo_latency():
    """인터럽트 지연 시간"""

    print("\n\n" + "=" * 70)
    print("인터럽트 지연 시간 (Interrupt Latency)")
    print("=" * 70)

    explanation = """
    인터럽트 지연 시간 구성:

    1. Recognition Latency:
       - CPU가 인터럽트 인지 시간
       - 최대 1 명령어 (1-20 cycles)

    2. Synchronization Latency:
       - 현재 명령어 완료까지
       - 복잡한 명령어일수록 길음
       - 예: MUL, DIV, String ops

    3. Context Save:
       - Push/Pop 시간
       - 자동: 2-3 cycles
       - 수동: 10-100 cycles

    4. ISR Dispatch:
       - Vector Table Lookup
       - Jump: 1-2 cycles

    최악의 경우:
    Long Instruction (50 cycles)
    + Context Save (10 cycles)
    + Dispatch (2 cycles)
    = 62 cycles

    @ 3GHz: ~20ns

    최적화:
    - 짧은 명령어 사용
    - 인터럽트 가능 구간 확대
    - 자동 Context Save
    """

    print(explanation)


def demo_comparison():
    """비교"""

    print("\n\n" + "=" * 70)
    print("인터럽트 vs 폴링 비교")
    print("=" * 70)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Interrupt vs Polling                             │
    ├─────────────────────────────────┬───────────────────────────────────┤
    │ Interrupt                       │ Polling                           │
    ├─────────────────────────────────┼───────────────────────────────────┤
    │ 하드웨어 주도                   │ 소프트웨어 주도                  │
    │ 비동기적 발생                   │ 주기적 확인                       │
    │ 빠른 응답 (0-1000 cycles)       │ 느린 응답 (폴링 간격)            │
    │ CPU 효율 높음                   │ CPU 낭비                          │
    │ 복잡한 하드웨어 필요            │ 단순한 구현                       │
    │ 우선순위 기반 처리              │ 순차적 처리                       │
    │ 다중 장치 동시 지원             │ 루프 필요                         │
    │                                 │                                   │
    │ 적용:                           │ 적용:                             │
    │ - 키보드, 마우스                │ - 단순 상태 확인                  │
    │ - 네트워크 패킷                 │ - 폴링 가능한 장치                │
    │ - 실시간 시스템                 │ - 임베디드 시스템                 │
    └─────────────────────────────────┴───────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Interrupt Types                                  │
    ├─────────────────────┬───────────────┬───────────────┬───────────────┤
    │ Hardware            │ Software      │ Exception     │ NMI           │
    ├─────────────────────┼───────────────┼───────────────┼───────────────┤
    │ 외부 장치 발생      │ INT 명령      │ CPU 내부      │ 비마스크able   │
    │ 비동기적            │ 동기적        │ 동기적        │ 최우선순위     │
    │ 마스크 가능         │ 항상 발생     │ 항상 발생     │ 전원 오류 등   │
    │ Timer, KBD, Disk   │ System Call   │ Divide Error  │ 하드웨어 Fail  │
    └─────────────────────┴───────────────┴───────────────┴───────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_basic_interrupt()
    demo_priority()
    demo_nested_interrupt()
    demo_masking()
    demo_cli_sti()
    demo_latency()
    demo_comparison()
