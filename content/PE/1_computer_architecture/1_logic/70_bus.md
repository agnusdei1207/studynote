+++
title = "버스 (Bus)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 버스 (Bus)

## 핵심 인사이트 (3줄 요약)
1. 버스(Bus)는 CPU, 메모리, I/O 장치 간 데이터를 전송하는 공유 통로로, Address Bus, Data Bus, Control Bus로 구성된다
2. 버스는 시분할 다중화(Time-Division Multiplexing)로 여러 장치가 공유하며, 버스 마스터가 버스를 제어하고 Arbitration이 충돌을 해결한다
3. 기술사시험에서는 버스 구조, 버스 폭, 동기/비동기 버스, 버스 프로토콜이 핵심이다

## Ⅰ. 개요 (500자 이상)

버스(Bus)는 **컴퓨터 시스템의 각 구성 요소(CPU, 메모리, I/O 장치) 간에 데이터, 주소, 제어 신호를 전송하는 공유 통로**이다. 모든 장치가 연결된 공용선(Wire) 형태로, 가장 경제적인 연결 방식이다.

```
버스 기본 개념:
구조: 공유 전선 (Wire)
구성: Address + Data + Control Bus
동작: 시분할 다중화 (TDM)

특징:
- 공유 자원
- 병렬 전송
- 시분할 사용
- 버스 마스터/슬레이브

장점:
- 단순한 연결
- 낮은 비용
- 유연한 확장

단점:
- 병목 현상
- 충돌 가능
- 전기적 제약
```

**버스의 핵심 특징:**

1. **공유성**: 여러 장치가 하나의 버스 공유
2. **병렬성**: 여러 비트 동시 전송
3. **TDM**: 시간 분할로 장치간 전송
4. **계층적**: 시스템/로컬 버스 계층

```
Point-to-Point vs Bus:
Point-to-Point:
- 1:1 연결
- 빠름
- 비쌈
- 확장 어려움

Bus:
- 1:N 연결
- 느림
- 저렴
- 쉬운 확장
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 버스 구성

```
버스 구조:

        CPU
         │
    ┌────┴────┐
    │ System  │
    │   Bus   │
    └────┬────┘
         │
    ┌────┴────────┬────────┐
    │             │        │
 Memory     Bridge    I/O Device
    │             │        │
    │        Local Bus    │
    │             │        │
    └─────────┬───┴────────┘
             │
          PCI/ISA

구성:
1. Address Bus:
   - CPU → Memory/I/O
   - 단방향 (일반적)
   - 주소 전송

2. Data Bus:
   - 양방향
   - 데이터 전송
   - Bidirectional

3. Control Bus:
   - 제어 신호
   - 양방향/혼합
   - Read/Write, Clock, etc.
```

### Address Bus

```
Address Bus:

구조:
CPU[Address Output] ──→ Memory/I/O

특징:
- 단방향 (CPU → 장치)
- 주소 전용
- 비트 폭 = 주소 공간

예:
- 16비트 → 64KB 주소 공간
- 20비트 → 1MB 주소 공간
- 32비트 → 4GB 주소 공간
- 64비트 → 16EB 주소 공간

Address Decoding:
高位 Address → Chip Select
低位 Address → Internal Address

예: RAM 0x0000-0x3FFF
A[19:14] = 000000 → /CS_RAM
A[13:0] → 내부 주소
```

### Data Bus

```
Data Bus:

구조:
CPU[Data] ←──→ Memory/I/O

특징:
- 양방향 (Bidirectional)
- Tri-state Buffer
- 데이터 비트 폭

비트 폭:
- 8비트: 1바이트 전송
- 16비트: 2바이트 전송 (Word)
- 32비트: 4바이트 전송 (DWord)
- 64비트: 8바이트 전송 (QWord)

Tri-state Buffer:
Data[7:0] ──┬──[Buffer]── Memory
            │    ↑
           OE    DIR
(Output Enable, Direction)

OE=0: High-Z (버스 분리)
OE=1, DIR=0: Memory → CPU
OE=1, DIR=1: CPU → Memory
```

### Control Bus

```
Control Bus 신호:

Read/Write:
- /RD (Read): 읽기 요청
- /WR (Write): 쓰기 요청

Timing:
- CLK (Clock): 동기 버스
- /READY: 데이터 준비
- /WAIT: 대기 요청

Bus Control:
- /BUSREQ: 버스 요청
- /BUSACK: 버스 승인
- ALE: Address Latch Enable

Interrupt:
- IRQ: 인터럽트 요청
- INTA: 인터럽트 승인

DMA:
- HRQ: Hold Request
- HLDA: Hold Acknowledge
- DREQ: DMA Request
- DACK: DMA Acknowledge

Arbitration:
- /BREQ: Bus Request
- /GBK: Bus Grant
```

### 동기 버스

```
Synchronous Bus:

개념:
- 공통 클럭에 동기
- 모든 전송이 클럭 경계

타이밍:
CLK: ─┬─┬─┬─┬─┬─┬─┬─┬─
     ↑ │ ↑ │ ↑ │ ↑ │
     │ │ │ │ │ │ │ │
Address:┌─┘ └─┐   ┌─┘
         │     │   │
Data:   ──────┘   ┌─┘
                 │
Control:────┬───┴──┐
          │Valid │Valid

특징:
- 단순한 프로토콜
- 고속 가능
- 클럭 분주 필요
- 모든 장치 동일 클럭

예:
- CPU 내부 버스
- PCI (동기식)
```

### 비동기 버스

```
Asynchronous Bus:

개념:
- 클럭 독립적
- Handshaking 프로토콜

타이밍 (Full Handshake):
Master: ─┐   ┌───┬─────┐
         │   │   │     │
         │Req │     │
Slave:   ─┴───┴───┬─┴───┐
                   │     │
                Ack     │

과정:
1. Master가 Request 활성
2. Slave가 데이터 준비
3. Slave가 Acknowledge 활성
4. Master가 Request 비활성
5. Slave가 Acknowledge 비활성

특징:
- 장치마다 다른 속도
- 복잡한 프로토콜
- 유연한 타이밍

예:
- ISA Bus
- Memory Interface
```

### 버스 인터페이스

```
Bus Interface Unit:

CPU 내부:
     ┌─────────────┐
     │  BIU (Bus   │
     │ Interface)  │
     └──────┬──────┘
            │
         System Bus

BIU 기능:
1. Address Latch
   - Address 출력
   - ALE로 래치

2. Data Transceiver
   - 송수신 버퍼
   - 양방향 전송

3. Control Logic
   - /RD, /WR 생성
   - Timing 제어

4. Bus Arbitration
   - /BUSREQ 처리
   - 버스 마스터 교체
```

## Ⅲ. 융합 비교

### 버스 타입

| 버스 | 폭 | 속도 | 동기 | 응용 |
|------|-----|------|------|------|
| Front Side | 64비트 | 400-1600MT/s | 동기 | CPU-Memory |
| Back Side | 64비트 | 200-800MT/s | 동기 | CPU-L2 Cache |
| PCI | 32/64비트 | 133-533MB/s | 동기 | Expansion |
| ISA | 16비트 | 8MB/s | 비동기 | Legacy |
| USB | 1비트 | 5-40Gbps | 직렬 | Peripheral |

### 동기 vs 비동기

| 비교 항목 | 동기 | 비동기 |
|----------|------|--------|
| 클럭 | 필요 | 불필요 |
| 프로토콜 | 단순 | 복잡 |
| 속도 | 빠름 | 느림 |
| 유연성 | 낮음 | 높음 |
| 응용 | CPU 내부 | I/O 장치 |

### 병렬 vs 직렬 버스

| 비교 항목 | 병렬 | 직렬 |
|----------|------|------|
| 비트 수 | 여러 | 1 |
| 핀 수 | 많음 | 적음 |
| 속도 | 높음 | 중간 |
| 거리 | 짧음 | 김 |
| 예 | PCI, ISA | USB, SATA |

## Ⅳ. 실무 적용 및 기술사적 판단

### PCI Bus

```
PCI (Peripheral Component Interconnect):

구조:
- 32/64비트 데이터 버스
- 32비트 주소 버스
- 33/66/100/133MHz
- 동기식

특징:
- Plug & Play
- Configuration Space
- Bus Mastering
- Burst Transfer

주소 지정:
Memory Address: 0x00000000-0xFFFFFFFF
I/O Address: 0x0000-0xFFFF
Configuration: 0x000-0xFF (Device)

전송:
- Address Phase: 1 클럭
- Data Phase: N 클럭 (Burst)
```

### ISA Bus

```
ISA (Industry Standard Architecture):

구조:
- 16비트 데이터 버스
- 24비트 주소 버스 (16MB)
- 8.33MHz
- 비동기식

신호:
SA[19:0]: System Address
SD[15:0]: System Data
/MEMR, /MEMW: Memory R/W
/IOR, /IOW: I/O R/W
IRQ[7:0]: 인터럽트
DRQ[3:0]: DMA 요청

타이밍:
- 4 클럭 per read/write
- Wait state 가능
- 최대 8MB/s
```

### Front Side Bus

```
FSB (Front Side Bus):

구조:
- CPU ↔ North Bridge
- 64비트 데이터
- 64비트 주소
- 100-1600MT/s

GTL+ Signaling:
VDD = 1.5V
High = > 1.0V
Low = < 0.4V

DDR:
- 상승/하강 에지 전송
- 2배 데이터 레이트

예: 400MHz FSB
- 400MT/s
- 64비트 × 400MT/s = 3.2GB/s
```

### 시스템 버스 계층

```
계층적 버스 구조:

Level 1: CPU 내부 버스
- 가장 빠름
- 여러 개
- ALU, Reg, Cache 연결

Level 2: System Bus (FSB)
- CPU ↔ Chipset
- 빠름
- Memory 액세스

Level 3: Expansion Bus (PCI/PCIe)
- Chipset ↔ 장치
- 중간 속도
- 확장 카드

Level 4: Peripherals (USB, SATA)
- 외부 장치
- 느림
- 편리성
```

## Ⅴ. 기대효과 및 결론

버스는 시스템의 백본이다. 모든 데이터 전송의 통로이자 병목이다.

## 📌 관련 개념 맵

```
버스 (Bus)
├── 구성
│   ├── Address Bus (단방향)
│   ├── Data Bus (양방향)
│   └── Control Bus (제어)
├── 타입
│   ├── 동기 (CLK 기반)
│   └── 비동기 (Handshake)
├── 동작
│   ├── 시분할 다중화
│   ├── Bus Arbitration
│   └── Bus Mastering
└── 예시
    ├── FSB (CPU-Memory)
    ├── PCI (Expansion)
    ├── ISA (Legacy)
    └── USB (Peripheral)
```

## 👶 어린이를 위한 3줄 비유 설명

1. 버스는 도로 같아요. 여러 차(CPU, 메모리, 장치)가 같은 도로를 이용해서 이동해요
2. Address Bus는 주소 안내판, Data Bus는 화물차, Control Bus는 교통 신호 같아요
3. 동기 버스는 신호등에 맞춰서 모두 같은 속도로 달리고, 비동기 버스는 서로 수신호(Handshake)하면서 달려요

```python
# 버스 시뮬레이션

from typing import List, Dict, Optional
from enum import Enum


class BusState(Enum):
    IDLE = "Idle"
    ADDRESS = "Address Phase"
    DATA = "Data Phase"
    WAIT = "Wait State"


class BusDevice:
    """버스 장치"""

    def __init__(self, name: str, base_addr: int, size: int):
        self.name = name
        self.base_addr = base_addr
        self.size = size
        self.memory = [0] * size
        self.ready = True

    def read(self, address: int) -> int:
        """읽기"""
        offset = address - self.base_addr
        if 0 <= offset < self.size:
            return self.memory[offset]
        return 0

    def write(self, address: int, data: int):
        """쓰기"""
        offset = address - self.base_addr
        if 0 <= offset < self.size:
            self.memory[offset] = data & 0xFF

    def in_range(self, address: int) -> bool:
        """주소 범위 확인"""
        return self.base_addr <= address < self.base_addr + self.size


class SystemBus:
    """시스템 버스"""

    def __init__(self, width: int = 8):
        self.width = width
        self.address_bus = 0
        self.data_bus = 0
        self.control = {"read": False, "write": False}
        self.state = BusState.IDLE
        self.devices: List[BusDevice] = []
        self.current_master = None

    def add_device(self, device: BusDevice):
        """장치 추가"""
        self.devices.append(device)

    def decode_address(self, address: int) -> Optional[BusDevice]:
        """주소 디코딩"""
        for device in self.devices:
            if device.in_range(address):
                return device
        return None

    def read_cycle(self, address: int, master: str) -> int:
        """읽기 사이클"""
        print(f"[{master}] Read Cycle: Address=0x{address:04X}")

        # Address Phase
        self.address_bus = address
        self.state = BusState.ADDRESS
        print(f"  Address Phase: A[0:{self.width-1}]=0x{address:04X}")

        # Device 선택
        target = self.decode_address(address)
        if not target:
            print(f"  Error: No device at address 0x{address:04X}")
            return 0

        # Data Phase
        self.state = BusState.DATA
        data = target.read(address)
        self.data_bus = data

        print(f"  Data Phase: D[0:{self.width-1}]=0x{data:02X}")
        print(f"  → {target.name}.read() = 0x{data:02X}")

        self.state = BusState.IDLE
        return data

    def write_cycle(self, address: int, data: int, master: str):
        """쓰기 사이클"""
        print(f"[{master}] Write Cycle: Address=0x{address:04X}, Data=0x{data:02X}")

        # Address Phase
        self.address_bus = address
        self.state = BusState.ADDRESS
        print(f"  Address Phase: A=0x{address:04X}")

        # Device 선택
        target = self.decode_address(address)
        if not target:
            print(f"  Error: No device at address 0x{address:04X}")
            return

        # Data Phase
        self.state = BusState.DATA
        self.data_bus = data
        target.write(address, data)

        print(f"  Data Phase: D=0x{data:02X}")
        print(f"  → {target.name}.write(0x{data:02X})")

        self.state = BusState.IDLE

    def request_bus(self, master: str) -> bool:
        """버스 요청"""
        if self.current_master is None:
            self.current_master = master
            return True
        return False

    def release_bus(self, master: str):
        """버스 반환"""
        if self.current_master == master:
            self.current_master = None

    def get_status(self) -> Dict:
        """버스 상태"""
        return {
            "state": self.state.value,
            "address": f"0x{self.address_bus:04X}",
            "data": f"0x{self.data_bus:02X}",
            "master": self.current_master
        }


class BusMaster:
    """버스 마스터"""

    def __init__(self, name: str, bus: SystemBus):
        self.name = name
        self.bus = bus

    def read(self, address: int) -> int:
        """읽기"""
        # 버스 요청
        while not self.bus.request_bus(self.name):
            pass

        # 읽기 사이클
        data = self.bus.read_cycle(address, self.name)

        # 버스 반환
        self.bus.release_bus(self.name)

        return data

    def write(self, address: int, data: int):
        """쓰기"""
        # 버스 요청
        while not self.bus.request_bus(self.name):
            pass

        # 쓰기 사이클
        self.bus.write_cycle(address, data, self.name)

        # 버스 반환
        self.bus.release_bus(self.name)

    def block_read(self, start_addr: int, count: int) -> List[int]:
        """블록 읽기 (Burst)"""
        data = []
        for i in range(count):
            data.append(self.read(start_addr + i))
        return data

    def block_write(self, start_addr: int, data: List[int]):
        """블록 쓰기 (Burst)"""
        for i, val in enumerate(data):
            self.write(start_addr + i, val)


def demonstration():
    """버스 데모"""
    print("=" * 60)
    print("버스 (Bus) 데모")
    print("=" * 60)

    # 시스템 버스
    bus = SystemBus(width=8)

    # 장치 추가
    ram = BusDevice("RAM", base_addr=0x0000, size=256)
    io_device1 = BusDevice("IO1", base_addr=0x1000, size=16)
    io_device2 = BusDevice("IO2", base_addr=0x2000, size=16)

    bus.add_device(ram)
    bus.add_device(io_device1)
    bus.add_device(io_device2)

    # CPU (Bus Master)
    cpu = BusMaster("CPU", bus)

    # DMA (Bus Master)
    dma = BusMaster("DMA", bus)

    # 기본 액세스
    print("\n[기본 액세스]")
    cpu.write(0x0000, 0xAA)
    cpu.write(0x0001, 0xBB)
    cpu.write(0x0002, 0xCC)

    data = cpu.read(0x0000)
    print(f"  CPU Read 0x0000: 0x{data:02X}")

    # I/O 액세스
    print("\n[I/O 액세스]")
    cpu.write(0x1000, 0x12)  # IO1
    cpu.write(0x2000, 0x34)  # IO2

    data1 = cpu.read(0x1000)
    data2 = cpu.read(0x2000)
    print(f"  IO1: 0x{data1:02X}")
    print(f"  IO2: 0x{data2:02X}")

    # 버스 경쟁
    print("\n[버스 Arbitration]")
    print("CPU와 DMA가 동시에 버스 요청")

    # CPU가 먼저 요청
    bus.current_master = "CPU"
    print(f"  CPU가 버스 점유")

    # DMA 요청
    if not bus.request_bus("DMA"):
        print(f"  DMA는 CPU가 버스 사용 중이라 대기")

    # CPU가 버스 반환
    bus.release_bus("CPU")
    print(f"  CPU가 버스 반환")

    # DMA가 버스 획득
    if bus.request_bus("DMA"):
        print(f"  DMA가 버스 획득")
        dma.write(0x0005, 0xDD)
        bus.release_bus("DMA")

    # 블록 전송 (Burst)
    print("\n[블록 전송 (Burst Mode)]")
    write_data = [0x10, 0x11, 0x12, 0x13, 0x14]
    cpu.block_write(0x0010, write_data)

    read_data = cpu.block_read(0x0010, 5)
    print(f"  Read back: {[f'0x{d:02X}' for d in read_data]}")

    # 버스 폭 비교
    print("\n[버스 폭 비교]")
    print("8비트 버스:")
    print("  전송: 0xAABB")
    print("  Cycle 1: 0xAA")
    print("  Cycle 2: 0xBB")

    print("\n16비트 버스:")
    print("  전송: 0xAABB")
    print("  Cycle 1: 0xAABB")

    # 버스 상태
    print("\n[버스 상태]")
    status = bus.get_status()
    for key, val in status.items():
        print(f"  {key}: {val}")

    # 동기 vs 비동기
    print("\n[동기 vs 비동기 버스]")
    print("동기 버스:")
    print("  클럭에 동기")
    print("  모든 장치 동일 타이밍")
    print("  예: FSB, PCI")

    print("\n비동기 버스:")
    print("  Handshake 프로토콜")
    print("  장치마다 다른 타이밍")
    print("  예: ISA")


if __name__ == "__main__":
    demonstration()
```
