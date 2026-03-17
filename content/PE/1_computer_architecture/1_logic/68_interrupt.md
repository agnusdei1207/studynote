+++
title = "인터럽트 (Interrupt)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 인터럽트 (Interrupt)

## 핵심 인사이트 (3줄 요약)
1. 인터럽트(Interrupt)는 CPU가 프로그램 실행 중 외부/내부 이벤트에 의해 실행 흐름을 변경하는 메커니즘으로, 하드웨어 인터럽트와 소프트웨어 인터럽트가 있다
2. 인터럽트 요청 시 CPU는 현재 상태를 저장(PC, PSW 스택 저장)하고 인터럽트 벡터 테이블에서 핸들러 주소를 찾아 ISR을 실행한다
3. 기술사시험에서는 인터럽트 종류, 우선순위, 벡터 테이블, 인터럽트 처리 과정이 핵심이다

## Ⅰ. 개요 (500자 이상)

인터럽트(Interrupt)는 **CPU가 정상적인 프로그램 실행 중에 긴급한 이벤트 발생을 처리하기 위해 실행 흐름을 일시 중단하고 해당 이벤트를 처리하는 메커니즘**이다. 폰 노이만 구조에서 CPU가 폴링(Polling) 방식으로 계속 확인하는 비효율을 해결하기 위해 고안되었다.

```
인터럽트 기본 개념:
목적: CPU의 효율적 이벤트 처리
발생: 하드웨어 신호 또는 소프트웨어 명령
동작: 현재 실행 중단 → ISR 실행 → 복귀

특징:
- 비동기적 발생
- 우선순위 기반 처리
- Context 저장/복원
- 벡터 테이블 기반

장점:
- Polling 불필요 (CPU 효율 ↑)
- 빠른 응답
- 실시간 처리 가능
```

**인터럽트의 핵심 특징:**

1. **비동기성**: 프로그램 실행과 무관하게 발생
2. **우선순위**: 중요도에 따른 처리 순서
3. **투명성**: 프로그램은 인터럽트를 인식하지 못함
4. **자동 복귀**: 처리 후 원래 위치로 복귀

```
Polling vs Interrupt:
Polling:
- CPU가 주기적 확인
- 불필요한 CPU 소모
- 응답 지연

Interrupt:
- 하드웨어 신호로 알림
- CPU 효율적
- 즉각적 응답
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 인터럽트 처리 과정

```
인터럽트 처리 순서:

1. 인터럽트 요청 (IRQ)
   External Device → Interrupt Controller → CPU

2. 명령 완료 대기
   CPU는 현재 명령 완료까지 대기

3. 인터럽트 승인 (INTA)
   CPU → Interrupt Controller

4. 벡터 번호 수신
   Interrupt Controller → CPU

5. Context 저장
   PC → Stack
   PSW → Stack
   Registers → Stack (필요시)

6. ISR 호출
   Vector Table → ISR Address → PC

7. ISR 실행
   인터럽트 서비스 루틴 실행

8. Context 복원
   Stack → PSW
   Stack → PC

9. 원래 프로그램 복귀
```

### 인터럽트 벡터 테이블

```
인터럽트 벡터 테이블 (x86 IVT):

Address  | Contents
---------|------------------
0x00000  | Reset Vector (CS:IP)
0x00004  | Interrupt 0 (Divide Error)
0x00008  | Interrupt 1 (Single Step)
0x0000C  | Interrupt 2 (NMI)
0x00010  | Interrupt 3 (Breakpoint)
...
0x00080  | Interrupt 32 (IRQ0 - Timer)
0x00084  | Interrupt 33 (IRQ1 - Keyboard)
...

구조:
각 엔트리 = 4바이트 (CS:IP 포인터)
IRQ 번호 → 벡터 번호 → 핸들러 주소

예:
IRQ 0 → INT 32 → Vector 0x80
→ Handler Address = [0x80:0x84]
```

### 인터럽트 컨트롤러

```
PIC (Programmable Interrupt Controller):

구조:
IRQ[7:0] ─┬─[PIC]─┬─→ CPU (INTR)
          │      │
Priority ─┤      └─→ Vector Number
Mask     ─┤
          │
INTA ←───┘

기능:
1. IRQ 수신 (8개)
2. 우선순위 결정
3. CPU에 INTR 신호
4. CPU INTA 시 벡터 송신
5. IRQ 마스킹 (IMR)

Cascade (Master/Slave):
Master PIC: IRQ 0-7
Slave PIC: IRQ 8-15 (Master IRQ 2에 연결)
```

### 인터럽트 종류

```
1. 하드웨어 인터럽트 (External):
   - Maskable Interrupt (INTR)
   - Non-Maskable Interrupt (NMI)

2. 소프트웨어 인터럽트 (Internal):
   - Exception (예외)
   - Trap (시스템 콜)
   - Fault (페이지 폴트)

3. 내부 인터럽트:
   - Divide Error
   - Overflow
   - Bounds Check

분류:
가능:           마스크 가능 (INTR)
비가능(NMI):    마스크 불가 (전원, 메모리)
예외(Exception): 실행 중 발생
트랩(Trap):     INT 명령어 (시스템 콜)
```

### 우선순위

```
인터럽트 우선순위 (일반적):

1. Reset (가장 높음)
2. NMI (Non-Maskable)
3. Maskable Interrupt
   - IRQ 0: Timer
   - IRQ 1: Keyboard
   - IRQ 2: Cascade (Slave PIC)
   - IRQ 3: COM2
   - IRQ 4: COM1
   - IRQ 5: LPT2
   - IRQ 6: Floppy
   - IRQ 7: LPT1
   - IRQ 8: RTC (Slave)
   ...
4. Exception (Divide, Overflow)
5. Software Interrupt (INT n)
6. Conditional Branch (가장 낮음)

해결:
- 우선순위 인코더
- Daisy Chain
- Nested Interrupt 가능
```

### 인터럽트 플래그

```
인터럽트 마스크 (IF Flag):

EFLAGS 레지스터 [9] = IF (Interrupt Flag)

IF = 0:
- INTR 무시 (CLI 명령어)
- NMI는 여전히 활성
- ISR 내에서 기본

IF = 1:
- INTR 활성 (STI 명령어)
- 일반 실행 모드

동작:
ISR 진입 시: CPU가 자동으로 IF = 0
ISR 종료 시: IRET 명령어로 IF 복원

CLI (Clear IF): INTR 비활성화
STI (Set IF): INTR 활성화
```

### Nested Interrupt

```
중첩 인터럽트 (Nested Interrupt):

ISR 실행 중 더 높은 우선순위 인터럽트 발생

과정:
1. ISR 실행 중
2. NMI 발생 (높은 우선순위)
3. 현재 ISR Context 저장
4. NMI ISR 실행
5. NMI 완료 후 원래 ISR 복귀
6. 원래 ISR 완료

조건:
- 더 높은 우선순위
- IF = 1 (ISR 내에서 STI)

구현:
ISR 시작: PUSHF; CLI
...
STI  ; 중첩 허용
...
POPF ; 상태 복원
IRET
```

## Ⅲ. 융합 비교

### 인터럽트 vs Polling

| 비교 항목 | 인터럽트 | Polling |
|----------|---------|---------|
| CPU 개입 | 이벤트 시만 | 주기적 |
| 응답 시간 | 빠름 | 느림 |
| CPU 효율 | 높음 | 낮음 |
| 하드웨어 | 복잡 | 단순 |
| 우선순위 | 지원 | 불가 |

### 인터럽트 종류

| 종류 | 원인 | 예시 | 우선순위 |
|------|------|------|----------|
| NMI | 하드웨어 긴급 | 전원, 메모리 | 가장 높음 |
| INTR | 일반 하드웨어 | 키보드, 타이머 | 높음 |
| Exception | 실행 중 오류 | Divide, Page | 중간 |
| Trap | 소프트웨어 요청 | 시스템 콜 | 낮음 |

### 인터럽트 컨트롤러

| 타입 | IRQ 수 | 우선순위 | 응용 |
|------|-------|----------|------|
| 8259A PIC | 8 (Cascade 15) | Fixed | x86 |
| APIC | 256+ | Programmable | Multi-core |
| GIC | 1024+ | Programmable | ARM |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86 인터럽트

```
x86 인터럽트 구조:

1. IDTR (Interrupt Descriptor Table Register):
   - IDT 기준 주소

2. IDT (Interrupt Descriptor Table):
   - 256개 엔트리
   - 각 8바이트 (Gate Descriptor)

3. Gate Descriptor:
   [Offset 31:16][Attr][Selector][Offset 15:0]

타입:
- Task Gate: Task Switch
- Interrupt Gate: IF=0 자동
- Trap Gate: IF 유지

동작:
INT n:
1. IDTR[n] → Gate Descriptor
2. Selector → GDT → Handler Segment
3. Offset → Handler Offset
4. CS:IP → Handler
```

### APIC (Advanced PIC)

```
Local APIC (Core 내부):

구조:
- ICR (Interrupt Command Register)
- ISR (In-Service Register)
- TPR (Task Priority Register)
- EOI (End of Interrupt)

기능:
- IPI (Inter-Processor Interrupt)
- Timer Interrupt
- Thermal Interrupt

I/O APIC (Chipset 내부):

구조:
- 24 IRQ 입력
- Redirection Table
- INTR 신호 생성

동작:
Device → I/O APIC → Local APIC → CPU Core
```

### ARM 인터럽트

```
ARM 인터럽트:

과거:
- IRQ (Interrupt Request)
- FIQ (Fast Interrupt Request)

현재 (ARMv7+):
- IRQ → IRQ Mode
- FIQ → FIQ Mode
- SWI (Software Interrupt)
- Data Abort
- Prefetch Abort
- Undefined Instruction

Vector Table:
0x00000000: Reset
0x00000004: Undefined Instruction
0x00000008: SWI
0x0000000C: Prefetch Abort
0x00000010: Data Abort
0x00000014: Reserved
0x00000018: IRQ
0x0000001C: FIQ

각 벡터 = 명령어 1개 (Jump)
```

### 시스템 콜

```
시스템 콜 (Software Interrupt):

목적: 사용자 모드 → 커널 모드 전환

x86:
INT 0x80 (Linux)
SYSCALL/SYSEXIT (Fast)

ARM:
SWI 0x00 (Linux)
SVC (Supervisor Call)

과정:
1. User Mode: mov eax, 1
2. INT 0x80 (sys_exit)
3. Trap → Kernel Mode
4. IDT[0x80] → System Call Handler
5. Kernel Service 실행
6. IRET → User Mode

보호:
- Ring Level 검사
- 파라미터 검증
- 권한 확인
```

## Ⅴ. 기대효과 및 결론

인터럽트는 이벤트 처리의 핵심이다. CPU 효율을 극대화하고 실시간 응답을 가능하게 한다.

## 📌 관련 개념 맵

```
인터럽트
├── 종류
│   ├── 하드웨어 (INTR, NMI)
│   ├── 소프트웨어 (INT, SYSCALL)
│   └── Exception (Divide, Page)
├── 처리
│   ├── IRQ 요청
│   ├── Context 저장
│   ├── ISR 실행
│   └── IRET 복귀
├── 구조
│   ├── PIC (Interrupt Controller)
│   ├── Vector Table
│   └── Priority Encoder
└── 특징
    ├── 비동기
    ├── 우선순위
    ├── 마스킹
    └── 중첩 가능
```

## 👶 어린이를 위한 3줄 비유 설명

1. 인터럽트는 CPU가 일하다가 전화벨이 울리면 잠깐 멈추고 전화를 받는 것 같아요. 전화를 다 받으면 다시 하던 일을 이어서 해요
2. NMI는 화재 경보 같아서 아무리 바빠도 꼭 처리해야 해요. 일반 인터럽트는 일반 전화라서 나중에 받아도 돼요
3. 벡터 테이블은 전화번호부 같아요. 어떤 전화(인터럽트)가 오면 번호부를 보고 담당자(ISR)에게 연결해줘요

```python
# 인터럽트 시뮬레이션

from typing import List, Dict, Callable, Optional
from enum import Enum


class InterruptType(Enum):
    NMI = "NMI"
    IRQ = "IRQ"
    EXCEPTION = "Exception"
    TRAP = "Trap"


class InterruptRequest:
    """인터럽트 요청"""

    def __init__(self, irq_num: int, int_type: InterruptType, priority: int):
        self.irq_num = irq_num
        self.int_type = int_type
        self.priority = priority

    def __lt__(self, other):
        return self.priority > other.priority  # 높은 우선순위 우선


class CPU:
    """CPU 시뮬레이션"""

    def __init__(self):
        self.pc = 0
        self.psw = 0x200  # IF=1 (인터럽트 활성)
        self.stack = []
        self.interrupt_flag = True
        self.interrupt_controller = None

    def execute_instruction(self):
        """명령어 실행"""
        self.pc += 1

    def push(self, value: int):
        """스택에 푸시"""
        self.stack.append(value)

    def pop(self) -> int:
        """스택에서 팝"""
        return self.stack.pop() if self.stack else 0

    def interrupt_enabled(self) -> bool:
        """인터럽트 활성화 확인"""
        return (self.psw & 0x200) != 0

    def disable_interrupts(self):
        """인터럽트 비활성화 (CLI)"""
        self.psw &= ~0x200
        self.interrupt_flag = False

    def enable_interrupts(self):
        """인터럽트 활성화 (STI)"""
        self.psw |= 0x200
        self.interrupt_flag = True

    def handle_interrupt(self, irq: InterruptRequest):
        """인터럽트 처리"""
        print(f"\n[Interrupt] IRQ {irq.irq_num} ({irq.int_type.value})")
        print(f"  PC before: {self.pc}")

        # Context 저장
        self.push(self.pc)
        self.push(self.psw)

        # 인터럽트 비활성화
        self.disable_interrupts()

        # 핸들러 주소 가져오기
        if self.interrupt_controller:
            handler_addr = self.interrupt_controller.get_handler(irq.irq_num)
            print(f"  Handler: 0x{handler_addr:04X}")
            self.pc = handler_addr

            # ISR 실행
            print(f"  Executing ISR...")

    def iret(self):
        """인터럽트 복귀"""
        print(f"  IRET: restoring context")
        self.psw = self.pop()
        self.pc = self.pop()
        print(f"  PC after: {self.pc}")


class InterruptController:
    """인터럽트 컨트롤러 (PIC)"""

    def __init__(self):
        self.irr = 0  # Interrupt Request Register
        self.isr = 0  # In-Service Register
        self.imr = 0  # Interrupt Mask Register
        self.handlers: Dict[int, int] = {}
        self.pending: List[InterruptRequest] = []

    def register_handler(self, irq: int, handler_addr: int):
        """핸들러 등록"""
        self.handlers[irq] = handler_addr

    def get_handler(self, irq: int) -> int:
        """핸들러 주소 반환"""
        return self.handlers.get(irq, 0)

    def request_interrupt(self, irq: int, int_type: InterruptType, priority: int):
        """인터럽트 요청"""
        if (self.imr >> irq) & 1:
            # 마스크됨
            return False

        self.irr |= (1 << irq)
        self.pending.append(InterruptRequest(irq, int_type, priority))
        print(f"[PIC] IRQ {irq} requested ({int_type.value}, Priority {priority})")
        return True

    def get_highest_priority(self) -> Optional[InterruptRequest]:
        """가장 높은 우선순위 인터럽트 반환"""
        if not self.pending:
            return None

        self.pending.sort()
        return self.pending[0]

    def acknowledge(self, irq: int):
        """인터럽트 승인"""
        self.isr |= (1 << irq)
        self.irr &= ~(1 << irq)
        if self.pending and self.pending[0].irq_num == irq:
            self.pending.pop(0)

    def end_of_interrupt(self, irq: int):
        """인터럽트 처리 완료"""
        self.isr &= ~(1 << irq)
        print(f"[PIC] IRQ {irq} EOI")

    def mask_irq(self, irq: int):
        """IRQ 마스크"""
        self.imr |= (1 << irq)

    def unmask_irq(self, irq: int):
        """IRQ 언마스크"""
        self.imr &= ~(1 << irq)


class Device:
    """디바이스"""

    def __init__(self, name: str, irq: int):
        self.name = name
        self.irq = irq
        self.controller: Optional[InterruptController] = None

    def generate_interrupt(self, priority: int = 5):
        """인터럽트 발생"""
        if self.controller:
            self.controller.request_interrupt(self.irq, InterruptType.IRQ, priority)


class Timer(Device):
    """타이머 디바이스"""

    def __init__(self):
        super().__init__("Timer", irq=0)
        self.counter = 0

    def tick(self):
        """타이머 틱"""
        self.counter += 1
        if self.counter >= 10:
            self.counter = 0
            self.generate_interrupt(priority=10)  # 높은 우선순위


class Keyboard(Device):
    """키보드 디바이스"""

    def __init__(self):
        super().__init__("Keyboard", irq=1)

    def key_press(self, key: str):
        """키 입력"""
        print(f"[Keyboard] Key '{key}' pressed")
        self.generate_interrupt(priority=5)


def demonstration():
    """인터럽트 데모"""
    print("=" * 60)
    print("인터럽트 (Interrupt) 데모")
    print("=" * 60)

    # 초기화
    cpu = CPU()
    pic = InterruptController()
    cpu.interrupt_controller = pic

    # 핸들러 등록
    pic.register_handler(0, 0x1000)  # Timer Handler
    pic.register_handler(1, 0x2000)  # Keyboard Handler

    # 디바이스 연결
    timer = Timer()
    keyboard = Keyboard()
    timer.controller = pic
    keyboard.controller = pic

    # 시뮬레이션
    print("\n[시뮬레이션 시작]")
    print(f"CPU PC: {cpu.pc}, IF={cpu.interrupt_enabled()}")

    # 타이머 인터럽트
    print("\n1. Timer Interrupt:")
    for i in range(10):
        timer.tick()
        cpu.execute_instruction()

    # 인터럽트 처리
    irq = pic.get_highest_priority()
    if irq and cpu.interrupt_enabled():
        pic.acknowledge(irq.irq_num)
        cpu.handle_interrupt(irq)
        cpu.iret()
        pic.end_of_interrupt(irq.irq_num)

    # 키보드 인터럽트
    print("\n2. Keyboard Interrupt:")
    keyboard.key_press('A')
    cpu.execute_instruction()

    irq = pic.get_highest_priority()
    if irq and cpu.interrupt_enabled():
        pic.acknowledge(irq.irq_num)
        cpu.handle_interrupt(irq)
        cpu.iret()
        pic.end_of_interrupt(irq.irq_num)

    # NMI (Non-Maskable Interrupt)
    print("\n3. NMI (마스크 불가):")
    pic.mask_irq(0)  # Timer 마스크
    timer.generate_interrupt(priority=10)  # 마스크되어 무시

    pic.request_interrupt(2, InterruptType.NMI, priority=15)
    cpu.execute_instruction()

    irq = pic.get_highest_priority()
    if irq:  # NMI는 마스크 무시
        pic.acknowledge(irq.irq_num)
        cpu.handle_interrupt(irq)
        cpu.iret()
        pic.end_of_interrupt(irq.irq_num)

    # 우선순위 테스트
    print("\n4. Priority Test:")
    keyboard.generate_interrupt(priority=5)
    timer.generate_interrupt(priority=10)

    cpu.execute_instruction()
    irq = pic.get_highest_priority()
    if irq:
        print(f"  Selected: IRQ {irq.irq_num} (Priority {irq.priority})")
        pic.acknowledge(irq.irq_num)
        cpu.handle_interrupt(irq)
        cpu.iret()
        pic.end_of_interrupt(irq.irq_num)

    # 인터럽트 비활성화 상태
    print("\n5. Interrupt Disabled:")
    cpu.disable_interrupts()
    keyboard.key_press('B')
    cpu.execute_instruction()

    print(f"  CPU IF={cpu.interrupt_enabled()}")
    irq = pic.get_highest_priority()
    if irq and cpu.interrupt_enabled():
        pic.acknowledge(irq.irq_num)
        cpu.handle_interrupt(irq)
    else:
        print("  Interrupt ignored (IF=0)")

    # 소프트웨어 인터럽트 (시스템 콜)
    print("\n6. Software Interrupt (System Call):")
    print("  INT 0x80 (sys_write)")
    pic.request_interrupt(0x80, InterruptType.TRAP, priority=3)

    cpu.execute_instruction()
    irq = pic.get_highest_priority()
    if irq:
        pic.register_handler(0x80, 0x3000)
        pic.acknowledge(irq.irq_num)
        cpu.handle_interrupt(irq)
        cpu.iret()
        pic.end_of_interrupt(irq.irq_num)

    # 인터럽트 상태
    print("\n[PIC Status]")
    print(f"  IRR: 0b{pic.irr:08b}")
    print(f"  ISR: 0b{pic.isr:08b}")
    print(f"  IMR: 0b{pic.imr:08b}")


if __name__ == "__main__":
    demonstration()
```
