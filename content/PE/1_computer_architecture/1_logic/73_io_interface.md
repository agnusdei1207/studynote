+++
title = "I/O 인터페이스 (I/O Interface)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# I/O 인터페이스 (I/O Interface)

## 핵심 인사이트 (3줄 요약)
1. I/O 인터페이스는 CPU와 I/O 장치 사이의 하드웨어 계층으로, 신호 레벨 변환, 데이터 버퍼링, 프로토콜 변환, 인터럽트 생성을 수행한다
2. Port-mapped I/O와 Memory-mapped I/O 두 가지 주소 지정 방식이 있으며, Control, Status, Data 레지스터로 장치를 제어한다
3. 기술사시험에서는 I/O 인터페이스 구조, 포트 주소, CSR 레지스터, 인터럽트 기반 I/O가 핵심이다

## Ⅰ. 개요 (500자 이상)

I/O 인터페이스(Input/Output Interface)는 **CPU와 다양한 I/O 장치(키보드, 디스플레이, 디스크 등) 사이를 연결하고, 서로 다른 신호 규격과 데이터 전송 속도를 조율하는 하드웨어**이다. CPU가 직접 각 장치를 제어하는 복잡성을 줄이고 표준화된 인터페이스를 제공한다.

```
I/O 인터페이스 기본 개념:
위치: CPU와 I/O 장치 사이
기능: 신호 변환, 프로토콜 변환, 버퍼링
구성: 데이터 버퍼, 제어 레지스터, 상태 레지스터

동작:
- CPU → Interface → Device
- Device → Interface → CPU

특징:
- 표준화된 연결
- 속도 차이 흡수
- 인터럽트 기반 제어
- DMA 지원
```

**I/O 인터페이스의 핵심 특징:**

1. **신호 변환**: CPU 신호 ↔ 장치 신호
2. **버퍼링**: 속도 차이 흡수
3. **프로토콜**: 장치별 통신 규약
4. **제어**: 장치 동작 제어

```
직접 연결 문제:
CPU와 장치 직접 연결 시:
- 신호 레벨 차이
- 속도 차이
- 프로토콜 복잡성
- 인터럽트 처리
→ I/O 인터페이스로 해결
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### I/O 인터페이스 구조

```
I/O 인터페이스 구조:

CPU Side:
    System Bus
         │
    ┌────┴────┐
    │  I/O    │
    │Interface│
    └────┬────┘
         │
    Device Bus
         │
      Device

내부 구성:
1. Data Buffer:
   - 입력/출력 데이터 버퍼
   - FIFO 또는 레지스터

2. Control Register:
   - 장치 제어 명령
   - 동작 모드 설정

3. Status Register:
   - 장치 상태 정보
   - Busy, Ready, Error

4. Address Decoder:
   - 포트 주소 디코딩
   - Chip Select

5. Interrupt Logic:
   - 인터럽트 생성
   - 우선순위
```

### Port-Mapped I/O

```
Port-Mapped I/O (Isolated I/O):

개념:
- 별도의 I/O 주소 공간
- 전용 IN/OUT 명령어

주소:
- I/O 주소: 0x0000-0xFFFF (64K 포트)
- 메모리 주소: 별도

명령어:
IN AL, PORT  ; PORT에서 AL로 읽기
OUT PORT, AL ; AL에서 PORT로 쓰기

신호:
M/IO# = 0: I/O 액세스
M/IO# = 1: 메모리 액세스

장점:
- 명확한 I/O 구분
- 메모리 공간 보존
- 전용 명령어

단점:
- 제한된 주소 공간
- 추가 명령어 필요

예: x86, x64
```

### Memory-Mapped I/O

```
Memory-Mapped I/O:

개념:
- I/O를 메모리 주소 공간에 매핑
- 일반 메모리 명령어로 액세스

주소:
- I/O 주소: 메모리 주소의 일부
- 예: 0xFFFF0000-0xFFFFFFFF

명령어:
MOV AL, [ADDRESS]  ; 읽기
MOV [ADDRESS], AL  ; 쓰기

신호:
M/IO# = 1 (항상 메모리 사이클)
주소 Decoder로 I/O 구분

장점:
- 간단한 명령어 세트
- 다양한 메모리 명령어 활용
- 큰 주소 공간

단점:
- 메모리 공간 차지
- 캐시 문제

예: ARM, MIPS, RISC-V
```

### Control/Status/Data Registers

```
CSR (Control/Status Registers):

1. Data Register:
   - 데이터 송수신
   - Read/Write

2. Control Register:
   - 장치 제어
   - Bit별 기능

   예:
   Bit 7: Enable (1=활성)
   Bit 6: Speed (0=저속, 1=고속)
   Bit 5: Direction (0=In, 1=Out)
   ...

3. Status Register:
   - 장치 상태 보고

   예:
   Bit 7: Busy (1=Busy)
   Bit 6: Ready (1=Ready)
   Bit 5: Error (1=Error)
   Bit 4: Interrupt (1=Pending)

액세스:
CPU가 Read/Write로 제어
```

### Parallel I/O Interface

```
Parallel I/O (8255 예):

구조:
Port A: 8비트 입출력
Port B: 8비트 입출력
Port C: 8비트 입출력
Control Word: 제어 레지스터

모드:
Mode 0: Simple I/O
Mode 1: Strobed I/O
Mode 2: Bidirectional Bus

Control Word:
D7: Mode Set
D6-5: Mode Selection
D4: Port A Direction
D3: Port C Upper Direction
D2: Mode Selection
D1: Port B Direction
D0: Port C Lower Direction

응용:
- 키보드 인터페이스
- 프린터 인터페이스
- 디지털 I/O
```

### Serial I/O Interface

```
Serial I/O (UART 예):

구조:
Transmit Buffer
Transmit Shift Register
Receive Shift Register
Receive Buffer
Baud Rate Generator

동작:
송신:
CPU → TX Buffer → Shift Register → Serial Out

수신:
Serial In → Shift Register → RX Buffer → CPU

신호:
TX: Transmit Data
RX: Receive Data
RTS: Request to Send
CTS: Clear to Send

Control:
LCR (Line Control):
- Word Length
- Stop Bits
- Parity

LSR (Line Status):
- Data Ready
- Overrun Error
- Parity Error
```

### Interrupt-Based I/O

```
인터럽트 기반 I/O:

과정:
1. Device가 데이터 준비
2. Interface가 인터럽트 요청
3. CPU가 ISR 실행
4. ISR에서 I/O 처리

예: 키보드 입력

1. Key Press
2. Keyboard Controller:
   - Data를 Buffer에 저장
   - IRQ 1 활성
3. CPU:
   - Interrupt 받음
   - ISR 실행 (Keyboard Handler)
   - IN AL, 0x60 (Scancode 읽기)
4. 완료:
   - EOI
   - 다음 Key 대기

장점:
- CPU 효율적
- 빠른 응답
- 실시간 처리
```

## Ⅲ. 융합 비교

### I/O 방식

| 방식 | 주소 공간 | 명령어 | 응용 |
|------|----------|--------|------|
| Port-Mapped | 분리 | IN/OUT | x86 |
| Memory-Mapped | 통합 | MOV | ARM, MIPS |

### 인터페이스 타입

| 타입 | 데이터 폭 | 속도 | 응용 |
|------|----------|------|------|
| Parallel | 8/16/32비트 | 빠름 | 프린터, 디스크 |
| Serial | 1비트 | 느림 | 키보드, 마우스 |
| DMA | 병렬 | 매우 빠름 | 고속 장치 |

### 인터페이스 칩

| 칩 | 포트 | 특징 | 응용 |
|------|------|------|------|
| 8255 | 3×8비트 | Programmable | 병렬 I/O |
| 8250 | 1×직렬 | UART | 시리얼 |
| 8237 | 4채널 | DMA Controller | DMA |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86 I/O Ports

```
x86 I/O Port Map:

0x00-0x1F: DMA Controller 1
0x20-0x3F: PIC (8259)
0x40-0x5F: PIT (Timer)
0x60-0x6F: Keyboard Controller
0x70-0x7F: RTC/CMOS
0x80-0x9F: DMA Page Register
0xA0-0xBF: PIC 2
0xC0-0xDF: DMA Controller 2
0xF0-0xFF: Coprocessor

액세스:
MOV DX, 0x60
IN AL, DX  ; 키보드 읽기

MOV DX, 0x378
MOV AL, 'A'
OUT DX, AL  ; 프린터 쓰기
```

### UART (16550)

```
16550 UART:

레지스터:
THR (0x00): Transmit Hold Register
RBR (0x00): Receive Buffer Register
IER (0x01): Interrupt Enable
IIR (0x02): Interrupt Identification
FCR (0x02): FIFO Control
LCR (0x03): Line Control
MCR (0x04): Modem Control
LSR (0x05): Line Status
MSR (0x06): Modem Status
SCR (0x07): Scratch Register

DLL, DLM: Divisor Latch (Baud Rate)

설정:
Baud Rate: 9600
Word Length: 8비트
Stop Bits: 1
Parity: None

액세스:
OUT LCR, 0x80  ; DLAB=1
OUT DLL, 0x0C  ; 9600 baud
OUT DLM, 0x00
OUT LCR, 0x03  ; 8N1
```

### USB Interface

```
USB Host Controller:

구조:
Host Controller
 Root Hub
  Port 1
  Port 2
  ...

전송 모드:
Control: 설정/제어
Bulk: 대량 데이터 (디스크)
Interrupt: 주기적 (마우스)
Isochronous: 실시간 (오디오)

Endpoint:
각 장치의 논리적 연결
Endpoint 0: Control Endpoint
Endpoint 1-IN: Interrupt IN
...

데이터 패킷:
TOKEN: Setup, IN, OUT
DATA: Data Packet
HANDSHAKE: ACK, NAK
```

### GPIO Interface

```
GPIO (General Purpose I/O):

구조:
8/16/32비트 Port
각 비트 독립 제어

레지스터:
GPIO_DATA: 데이터 Read/Write
GPIO_DIR: 방향 (0=In, 1=Out)
GPIO_SET: Set 비트
GPIO_CLEAR: Clear 비트
GPIO_TOGGLE: Toggle 비트

액세스:
DIR = 0xFF  ; All Output
DATA = 0x55  ; Output 0b01010101

응용:
- LED 제어
- 스위치 입력
- Relay 제어
- Chip Select
```

## Ⅴ. 기대효과 및 결론

I/O 인터페이스는 CPU와 장치의 다리이다. 표준화된 연결로 복잡성을 줄이고 호환성을 높인다.

## 📌 관련 개념 맵

```
I/O 인터페이스
├── 주소 지정
│   ├── Port-Mapped (IN/OUT)
│   └── Memory-Mapped (MOV)
├── 구조
│   ├── Data Buffer
│   ├── Control Register
│   ├── Status Register
│   └── Interrupt Logic
├── 타입
│   ├── Parallel (8255)
│   ├── Serial (UART)
│   └── DMA (8237)
└── 동작
    ├── Programmed I/O
    ├── Interrupt I/O
    └── DMA
```

## 👶 어린이를 위한 3줄 비유 설명

1. I/O 인터페이스는 통역사 같아요. CPU가 하는 말을 프린터가 이해하는 말로 번역해주고, 프린터의 상태를 CPU에게 알려줘요
2. Port-Mapped I/O는 전화 따로, 인터넷 따로인 것처럼 I/O용 번호가 따로 있어요. Memory-Mapped는 모든 것을 하나의 번호로 관리해요
3. Control Register는 스위치 같아서 장치를 켜고 끌 수 있고, Status Register는 표시판 같아서 장치 상태를 보여줘요

```python
# I/O 인터페이스 시뮬레이션

from typing import Dict, List
from enum import Enum


class IOAddressing(Enum):
    PORT_MAPPED = "Port-Mapped"
    MEMORY_MAPPED = "Memory-Mapped"


class StatusBits(Enum):
    BUSY = 0x80
    READY = 0x40
    ERROR = 0x20
    INTERRUPT = 0x10


class IOInterface:
    """I/O 인터페이스"""

    def __init__(self, name: str, base_addr: int):
        self.name = name
        self.base_addr = base_addr
        self.data_reg = 0
        self.control_reg = 0
        self.status_reg = StatusBits.READY.value

    def read_data(self) -> int:
        """데이터 레지스터 읽기"""
        return self.data_reg

    def write_data(self, data: int):
        """데이터 레지스터 쓰기"""
        self.data_reg = data & 0xFF

    def read_control(self) -> int:
        """제어 레지스터 읽기"""
        return self.control_reg

    def write_control(self, control: int):
        """제어 레지스터 쓰기"""
        self.control_reg = control & 0xFF

    def read_status(self) -> int:
        """상태 레지스터 읽기"""
        return self.status_reg

    def set_status(self, bit: StatusBits):
        """상태 비트 설정"""
        self.status_reg |= bit.value

    def clear_status(self, bit: StatusBits):
        """상태 비트 클리어"""
        self.status_reg &= ~bit.value

    def is_busy(self) -> bool:
        """Busy 상태 확인"""
        return (self.status_reg & StatusBits.BUSY.value) != 0

    def is_ready(self) -> bool:
        """Ready 상태 확인"""
        return (self.status_reg & StatusBits.READY.value) != 0

    def has_error(self) -> bool:
        """Error 상태 확인"""
        return (self.status_reg & StatusBits.ERROR.value) != 0


class PortMappedIO:
    """Port-Mapped I/O 시스템"""

    def __init__(self):
        self.ports: Dict[int, IOInterface] = {}

    def add_interface(self, interface: IOInterface):
        """인터페이스 추가"""
        offset = 0
        self.ports[interface.base_addr + offset] = interface
        self.ports[interface.base_addr + offset + 1] = interface  # Control
        self.ports[interface.base_addr + offset + 2] = interface  # Status

    def in_port(self, port: int) -> int:
        """포트 읽기 (IN 명령어)"""
        if port in self.ports:
            interface = self.ports[port]
            offset = port - interface.base_addr

            if offset == 0:
                return interface.read_data()
            elif offset == 1:
                return interface.read_control()
            elif offset == 2:
                return interface.read_status()
        return 0

    def out_port(self, port: int, data: int):
        """포트 쓰기 (OUT 명령어)"""
        if port in self.ports:
            interface = self.ports[port]
            offset = port - interface.base_addr

            if offset == 0:
                interface.write_data(data)
            elif offset == 1:
                interface.write_control(data)


class MemoryMappedIO:
    """Memory-Mapped I/O 시스템"""

    def __init__(self, memory_size: int = 65536):
        self.memory = [0] * memory_size
        self.interfaces: Dict[int, IOInterface] = {}

    def add_interface(self, interface: IOInterface):
        """인터페이스 추가 (메모리에 매핑)"""
        self.interfaces[interface.base_addr] = interface
        for i in range(4):  # 4레지스터
            self.memory[interface.base_addr + i] = 0

    def read_mem(self, address: int) -> int:
        """메모리 읽기 (MOV 명령어)"""
        # I/O 영역 확인
        for base, interface in self.interfaces.items():
            if base <= address < base + 4:
                offset = address - base
                if offset == 0:
                    return interface.read_data()
                elif offset == 1:
                    return interface.read_control()
                elif offset == 2:
                    return interface.read_status()

        # 일반 메모리
        if 0 <= address < len(self.memory):
            return self.memory[address]
        return 0

    def write_mem(self, address: int, data: int):
        """메모리 쓰기 (MOV 명령어)"""
        # I/O 영역 확인
        for base, interface in self.interfaces.items():
            if base <= address < base + 4:
                offset = address - base
                if offset == 0:
                    interface.write_data(data)
                elif offset == 1:
                    interface.write_control(data)
                return

        # 일반 메모리
        if 0 <= address < len(self.memory):
            self.memory[address] = data & 0xFF


class Device:
    """I/O 장치"""

    def __init__(self, name: str):
        self.name = name
        self.data = 0

    def send_data(self, interface: IOInterface):
        """데이터 전송"""
        if interface.is_ready():
            interface.write_data(self.data)
            interface.set_status(StatusBits.BUSY)
            interface.clear_status(StatusBits.READY)
            print(f"[{self.name}] Data sent: 0x{self.data:02X}")

    def receive_data(self, interface: IOInterface):
        """데이터 수신"""
        if interface.is_ready():
            data = interface.read_data()
            self.data = data
            print(f"[{self.name}] Data received: 0x{data:02X}")


def demonstration():
    """I/O 인터페이스 데모"""
    print("=" * 60)
    print("I/O 인터페이스 (I/O Interface) 데모")
    print("=" * 60)

    # Port-Mapped I/O
    print("\n[Port-Mapped I/O]")
    port_io = PortMappedIO()

    keyboard = IOInterface("Keyboard", base_addr=0x60)
    port_io.add_interface(keyboard)

    # IN 명령어
    data = port_io.in_port(0x60)  # Data Register
    status = port_io.in_port(0x62)  # Status Register

    print(f"IN AL, 0x60 → AL = 0x{data:02X}")
    print(f"IN AL, 0x62 → AL = 0b{status:08b}")

    # OUT 명령어
    port_io.out_port(0x60, 0xAA)  # Command Write
    print(f"OUT 0x60, AL (AL=0xAA)")

    # Memory-Mapped I/O
    print("\n[Memory-Mapped I/O]")
    mem_io = MemoryMappedIO()

    uart = IOInterface("UART", base_addr=0xFFFF0000)
    mem_io.add_interface(uart)

    # MOV 명령어
    lcr = mem_io.read_mem(0xFFFF0003)  # LCR Register
    print(f"MOV EAX, [0xFFFF0003] → EAX = 0x{lcr:02X}")

    mem_io.write_mem(0xFFFF0000, 0x55)  # THR Write
    print(f"MOV [0xFFFF0000], AL (AL=0x55)")

    # 제어/상태 레지스터
    print("\n[Control/Status Registers]")
    interface = IOInterface("Test", base_addr=0x100)

    # 제어 레지스터 쓰기
    print("Control Register (예시):")
    print("  Bit 7: Enable (1=On)")
    print("  Bit 6: Speed (0=Low, 1=High)")
    print("  Bit 5: Direction (0=In, 1=Out)")

    interface.write_control(0b10100000)  # Enable, High Speed, Out
    control = interface.read_control()
    print(f"  Write 0b10100000 → Read back: 0b{control:08b}")

    # 상태 레지스터
    print("\nStatus Register:")
    interface.set_status(StatusBits.READY)
    status = interface.read_status()
    print(f"  Status: 0b{status:08b}")
    print(f"  Busy: {interface.is_busy()}")
    print(f"  Ready: {interface.is_ready()}")
    print(f"  Error: {interface.has_error()}")

    # 인터럽트 기반 I/O
    print("\n[Interrupt-Based I/O]")
    print("Device → Interface → IRQ → CPU ISR")

    device = Device("Keyboard")
    interface2 = IOInterface("Keyboard", base_addr=0x60)

    # 장치가 데이터 준비
    device.data = 0x1B  # ESC Key

    # 인터럽트 생성
    print("1. Key Press")
    print("2. Keyboard Interface stores data")
    interface2.write_data(0x1B)
    interface2.set_status(StatusBits.READY)

    print("3. IRQ 1 generated")
    print("4. CPU ISR executes")

    # ISR에서 I/O 처리
    print("5. ISR: IN AL, 0x60")
    scancode = interface2.read_data()
    print(f"   → Scancode = 0x{scancode:02X}")

    # 비교
    print("\n[Port-Mapped vs Memory-Mapped]")
    print("Port-Mapped:")
    print("  - IN AL, PORT")
    print("  - OUT PORT, AL")
    print("  - 별도 I/O 공간")
    print("  - x86, x64")

    print("\nMemory-Mapped:")
    print("  - MOV AL, [ADDR]")
    print("  - MOV [ADDR], AL")
    print("  - 통합 주소 공간")
    print("  - ARM, MIPS")


if __name__ == "__main__":
    demonstration()
```
