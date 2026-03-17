+++
title = "버스 인터페이스 (Bus Interface)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 버스 인터페이스 (Bus Interface)

## 핵심 인사이트 (3줄 요약)
1. 버스 인터페이스는 CPU와 시스템 버스 사이의 인터페이스로, 주소 래치, 데이터 트랜시버, 버스 제어 논리로 구성되어 버스 동작을 제어한다
2. BIU(Bus Interface Unit)는 버스 마스터링, 타이밍 생성, 데이터 버퍼링을 담당하며 CPU 코어와 버스 사이의 계층을 분리한다
3. 기술사시험에서는 BIU 구조, 버스 사이클, 인터페이스 타이밍, 버스 마스터/슬레이브 모드가 핵심이다

## Ⅰ. 개요 (500자 이상)

버스 인터페이스(Bus Interface)는 **CPU 내부 회로와 외부 시스템 버스 사이를 연결하고, 버스 프로토콜을 처리하는 회로**이다. CPU가 요청하는 메모리나 I/O 액세스를 실제 버스 신호로 변환하고, 외부 버스의 타이밍과 CPU 내부 타이밍을 조율한다.

```
버스 인터페이스 기본 개념:
위치: CPU와 버스 사이
기능: 프로토콜 변환, 타이밍 제어
구성: Address Latch, Data Transceiver, Control Logic

동작:
- CPU 요청 → 버스 사이클 생성
- 버스 신호 → 내부 신호 변환
- 타이밍 매칭
- 버스 마스터링

특징:
- 프로토콜 추상화
- 타이밍 격리
- 버퍼링
- 양방향 변환
```

**버스 인터페이스의 핵심 특징:**

1. **프로토콜 변환**: 내부 버스 프로토콜 → 시스템 버스 프로토콜
2. **타이밍 조율**: CPU 클럭 → 버스 클럭
3. **버퍼링**: 속도 차이 흡수
4. **아비트레이션**: 버스 사용권 협상

```
CPU 내부 vs 외부 버스:
CPU 내부:
- 고속
- 단순 프로토콜
- 코어 전용

시스템 버스:
- 저속
- 복잡 프로토콜
- 다중 장치 공유

BIU가 중간에서 변환/조율
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### BIU 구조

```
Bus Interface Unit 구조:

CPU Core
   │
   │ (Internal Bus)
   ↓
┌─────────────────────────┐
│    BIU (Bus Interface)  │
├─────────────────────────┤
│                         │
│  ┌─────────────────┐    │
│  │ Address Latch   │    │
│  │   & Decoder     │    │
│  └────────┬────────┘    │
│           │             │
│  ┌────────▼────────┐    │
│  │  Data Transceiver│   │
│  │   (Bidirectional)│   │
│  └────────┬────────┘    │
│           │             │
│  ┌────────▼────────┐    │
│  │  Control Logic  │    │
│  │  (Timing, State)│   │
│  └────────┬────────┘    │
│           │             │
└───────────┼─────────────┘
            │
       System Bus
```

### Address Latch

```
Address Latch:

목적: 주소 안정화
타이밍: Address → Latch → Bus

구조:
CPU Address ───┬───┐
               │   │
            ALE └─[Latch]── Bus Address
                   ↑
                Enable

동작:
1. CPU가 Address 출력
2. ALE(Address Latch Enable) 활성
3. Latch가 Address 캡처
4. CPU가 다음 동작 수행 가능
5. Bus에 안정된 Address 유지

회로:
D Q
─┬─[LATCH]─┬── QA
 │         └── QB
ALE
```

### Data Transceiver

```
Data Transceiver:

목적: 양방향 데이터 전송 버퍼

구조:
Internal Data ──┬──[Buffer]── Bus Data
                │    ↑
               OE    DIR

동작:
OE=0: High-Z (버스 분리)
OE=1, DIR=0: Bus → Internal (Read)
OE=1, DIR=1: Internal → Bus (Write)

회로 (245 Transceiver):
A (Internal) ─┬─[Tri-State]─→ B (Bus)
              │    ↑
             DIR   OE
B (Bus) ─────┴─[Tri-State]─→ A (Internal)

타이밍:
Write: DIR=1, OE=0 → 데이터 출력
Read: DIR=0, OE=0 → 데이터 입력
Idle: OE=1 → High-Z
```

### Bus Control Logic

```
Bus Control State Machine:

States:
IDLE → ADDRESS → DATA → WAIT → IDLE

State Machine:
        IDLE
         │ Request
         ▼
      ADDRESS
         │ ALE
         ▼
       DATA
         │ Ready
         │ Wait?
    ┌────┴────┐
    │         │
   WAIT      IDLE
    │         │
    └─────────┘

Control Signals Generation:
State = ADDRESS:
  ALE = 1
  /RD = 1, /WR = 1

State = DATA (Read):
  /RD = 0
  Data를 캡처

State = DATA (Write):
  /WR = 0
  Data를 출력
```

### Timing Generation

```
타이밍 생성:

Clock Domain Crossing:
CPU Core Clock: 200MHz
System Bus Clock: 100MHz

Sync Logic:
CPU Request ──┬──[Flop]──┬──[Flop]── Bus Request
             │   ClkB   │   ClkB
           ClkA

Wait State Insertion:
Bus가 느린 장치 액세스 시
Wait State 추가

타이밍:
T1: Address Phase
T2: Data Phase
T3-Tw: Wait State (Ready=0)
T4: Complete

Control:
/READY 입력이 0이면
T-State 카운터 정지
/READY=1이면 다음 상태로
```

### Bus Mastering

```
버스 마스터 인터페이스:

Bus Master Mode:
- 장치가 버스 제어
- DMA, 다른 CPU 등

Request/Grant:
/BUSREQ ───────────→ Bus Master
←────────────────── /BUSGRANT

과정:
1. Master가 /BUSREQ 활성
2. Current Master가 버스 완료
3. Arbiter가 /BUSGRANT 활성
4. New Master가 버스 제어
5. 사용 후 /BUSREQ 비활성
6. /BUSGRANT 해제

TriState Control:
Master가 아닐 때:
모든 출력 = High-Z

Master일 때:
출력 활성
```

### 인터페이스 타이밍

```
Intel Style Bus Timing (8086):

Memory Read:
T1: ─┬───┬─────┬─────┬
     │   │     │     │
ALE  ┘   └─┐   └─┐
         │     │   │
ADR  ┌───┘     │   │
     │         │   │
RD   ──────────┘   │
     │             │
DAT  ──────────────┘

Wait State:
T4가 /READY=0이면
Tw 추가
Tw: ──┬─────────┬──
     │ /READY=0 │

속도:
Basic: 4T
Wait 1: 5T
Wait 2: 6T
```

## Ⅲ. 융합 비교

### 인터페이스 타입

| 타입 | 프로토콜 | 속도 | 복잡도 | 응용 |
|------|---------|------|--------|------|
| CPU-Bus | Mux | 고속 | 중간 | 8086 |
| PCI-Bridge | PCI | 중간 | 높음 | Chipset |
| USB | Serial | 저속 | 높음 | Peripheral |

### Latch 방식

| 방식 | 회로 | 속도 | 비용 | 응용 |
|------|------|------|------|------|
| Transparent | D Latch | 빠름 | 낮음 | 내부 버스 |
| Edge Triggered | D FF | 중간 | 중간 | 동기 버스 |
| Registered | FF Array | 느림 | 높음 | 고속 버스 |

### Transceiver 타입

| 타입 | 비트 | 방향 | 전류 | 응용 |
|------|------|------|------|------|
| 245 | 8비트 | 양방향 | 64mA | 병렬 버스 |
| 16245 | 16비트 | 양방향 | 64mA | 확장 버스 |
| 1655x | 32비트 | 양방향 | 64mA | PCI |

## Ⅳ. 실무 적용 및 기술사적 판단

### 8086 BIU

```
8086 Bus Interface:

구조:
- 16비트 Data Bus
- 20비트 Address Bus (Mux)
- Control Bus

Address/Data Multiplexing:
AD[15:0]: Address/Data Mux
A[19:16]: Address High

타이밍:
T1: AD에 Address 출력, ALE=1
T2: AD가 Data로 전환
T3: Data 전송
T4: 완료

Latch 사용:
외부 8282/8283 Latch
ALE로 Address 캡처
A[19:0] 유지
```

### PCI Bridge Interface

```
PCI Bridge:

North Bridge 내부:
CPU Interface ←→ PCI Interface

CPU → PCI:
- CPU Cycle → PCI Cycle 변환
- Address Phase
- Data Phase
- Burst 지원

PCI → CPU:
- PCI Request → CPU Bus Request
- Grant 후 전송
- PCI Protocol 변환

Configuration:
BAR (Base Address Register)
- 장치 주소 매핑
- Memory Mapped I/O
```

### AMBA Bus Interface

```
AMBA AHB Interface:

AHB Master Interface:
HADDR: Address Bus
HWDATA: Write Data
HRDATA: Read Data
HTRANS: Transfer Type
HSIZE: Burst Size
HBURST: Burst Type
HPROT: Protection
HWRITE: Read/Write
HREADY: Transfer Complete
HRESP: Response

State Machine:
IDLE → BUSY → NSEQ → SEQ
                    ↻

Decoder:
Address → Slave Select
HSEL[3:0]
```

### Wishbone Interface

```
Wishbone Bus Interface:

Signals:
DAT_I: Input Data
DAT_O: Output Data
ADR: Address
CYC: Cycle
STB: Strobe
WE: Write Enable
SEL: Select
ACK: Acknowledge
STALL: Stall
ERR: Error

Classic Pipeline:
Master ──→ Interconnect ──→ Slave

Cycle:
STB=1, CYC=1 → 요청
ACK=1 → 완료

점대점 연결:
단순하고 빠름
```

## Ⅴ. 기대효과 및 결론

버스 인터페이스는 CPU와 버스의 다리이다. 프로토콜 변환과 타이밍 조율로 안정적인 통신을 제공한다.

## 📌 관련 개념 맵

```
버스 인터페이스
├── 구조
│   ├── Address Latch
│   ├── Data Transceiver
│   └── Control Logic
├── 동작
│   ├── Address Phase
│   ├── Data Phase
│   ├── Wait State
│   └── Bus Mastering
├── 기능
│   ├── Protocol 변환
│   ├── Timing 조율
│   ├── Buffering
│   └── Arbitration
└── 예시
    ├── 8086 BIU
    ├── PCI Bridge
    ├── AMBA AHB
    └── Wishbone
```

## 👶 어린이를 위한 3줄 비유 설명

1. 버스 인터페이스는 통역사 같아요. CPU가 하는 말(내부 신호)을 버스가 이해하는 말(버스 신호)로 번역해줘요
2. Address Latch는 주소를 적어두는 메모장치 같고, Data Transceiver는 양방향으로 물건을 전달하는 배달원 같아요
3. Control Logic은 교통 경찰 같아서 신호등(RD/WR)을 조작하고, 언제 전달할지 타이밍을 정해요

```python
# 버스 인터페이스 시뮬레이션

from typing import List, Optional
from enum import Enum


class BusState(Enum):
    IDLE = "Idle"
    ADDRESS = "Address Phase"
    DATA = "Data Phase"
    WAIT = "Wait State"
    COMPLETE = "Complete"


class AddressLatch:
    """주소 래치"""

    def __init__(self):
        self.latched_address = 0
        self.current_address = 0
        self.ale = False  # Address Latch Enable

    def input(self, address: int):
        """주소 입력"""
        self.current_address = address

    def enable(self):
        """래치 활성화"""
        self.ale = True
        self.latched_address = self.current_address

    def disable(self):
        """래치 비활성화"""
        self.ale = False

    def output(self) -> int:
        """래치된 주소 출력"""
        return self.latched_address


class DataTransceiver:
    """데이터 트랜시버"""

    def __init__(self):
        self.internal_data = 0
        self.bus_data = 0
        self.oe = False  # Output Enable
        self.dir = False  # Direction (0=Read, 1=Write)

    def set_internal(self, data: int):
        """내부 데이터 설정"""
        self.internal_data = data

    def set_bus(self, data: int):
        """버스 데이터 설정"""
        self.bus_data = data

    def set_dir(self, write: bool):
        """방향 설정"""
        self.dir = write

    def enable(self):
        """활성화"""
        self.oe = True

    def disable(self):
        """비활성화 (High-Z)"""
        self.oe = False

    def get_output(self) -> int:
        """출력 데이터"""
        if not self.oe:
            return None  # High-Z
        if self.dir:
            return self.internal_data
        else:
            return None  # Read 모드

    def get_input(self) -> int:
        """입력 데이터"""
        if self.oe and not self.dir:
            return self.bus_data
        return self.internal_data


class BusControlLogic:
    """버스 제어 논리"""

    def __init__(self):
        self.state = BusState.IDLE
        self.ready = True
        self.ale = False
        self.rd = False
        self.wr = False

    def clock(self, request: bool, ready_input: bool) -> dict:
        """클럭에 따른 상태 변화"""
        self.ready = ready_input
        signals = {}

        if self.state == BusState.IDLE:
            if request:
                self.state = BusState.ADDRESS
                self.ale = True
            signals = {"ale": self.ale, "rd": False, "wr": False}

        elif self.state == BusState.ADDRESS:
            self.state = BusState.DATA
            self.ale = False
            self.rd = True  # Read 예시
            signals = {"ale": False, "rd": self.rd, "wr": self.wr}

        elif self.state == BusState.DATA:
            if self.ready:
                self.state = BusState.COMPLETE
            else:
                self.state = BusState.WAIT
            signals = {"ale": False, "rd": self.rd, "wr": self.wr}

        elif self.state == BusState.WAIT:
            if self.ready:
                self.state = BusState.COMPLETE
            signals = {"ale": False, "rd": self.rd, "wr": self.wr}

        elif self.state == BusState.COMPLETE:
            self.state = BusState.IDLE
            self.rd = False
            signals = {"ale": False, "rd": False, "wr": False}

        return {
            "state": self.state,
            "signals": signals
        }


class BusInterfaceUnit:
    """버스 인터페이스 유닛"""

    def __init__(self):
        self.address_latch = AddressLatch()
        self.data_transceiver = DataTransceiver()
        self.control_logic = BusControlLogic()
        self.internal_addr = 0
        self.internal_data = 0
        self.write_mode = False

    def cpu_request(self, address: int, data: int, write: bool):
        """CPU 요청"""
        self.internal_addr = address
        self.internal_data = data
        self.write_mode = write

    def clock_cycle(self, ready: bool) -> dict:
        """한 클럭 사이클"""
        result = {}

        # 제어 논리 업데이트
        control = self.control_logic.clock(
            request=self.control_logic.state != BusState.IDLE or self.internal_addr != 0,
            ready_input=ready
        )

        result["state"] = control["state"].value
        result["signals"] = control["signals"]

        # Address Latch
        if control["signals"]["ale"]:
            self.address_latch.input(self.internal_addr)
            self.address_latch.enable()
            result["address"] = self.address_latch.output()
        else:
            self.address_latch.disable()
            result["address"] = self.address_latch.output()

        # Data Transceiver
        if control["state"] == BusState.DATA:
            if self.write_mode:
                self.data_transceiver.set_dir(True)
                self.data_transceiver.set_internal(self.internal_data)
                self.data_transceiver.enable()
                result["data_out"] = self.data_transceiver.get_output()
            else:
                self.data_transceiver.set_dir(False)
                self.data_transceiver.enable()
                result["data_in"] = self.data_transceiver.get_input()
        elif control["state"] == BusState.COMPLETE:
            if not self.write_mode:
                self.internal_data = self.data_transceiver.get_input()
                result["data_read"] = self.internal_data
            self.data_transceiver.disable()

        return result


def demonstration():
    """버스 인터페이스 데모"""
    print("=" * 60)
    print("버스 인터페이스 (Bus Interface) 데모")
    print("=" * 60)

    biu = BusInterfaceUnit()

    # Read Cycle
    print("\n[Read Cycle]")
    print("CPU: Read request @ 0x1000")

    biu.cpu_request(address=0x1000, data=0, write=False)

    for i in range(6):
        print(f"\nT{i+1}:")
        result = biu.clock_cycle(ready=(i >= 3))
        print(f"  State: {result['state']}")
        print(f"  Signals: ALE={result['signals']['ale']}, RD={result['signals']['rd']}")
        if 'address' in result:
            print(f"  Address Latch: 0x{result['address']:04X}")
        if i == 4 and 'data_read' in result:
            # 버스에 데이터 가정
            biu.data_transceiver.set_bus(0xAA)
            print(f"  Data Read: 0x{result['data_read']:02X}")

    # Write Cycle
    print("\n[Write Cycle]")
    print("CPU: Write 0x55 @ 0x2000")

    biu = BusInterfaceUnit()  # Reset
    biu.cpu_request(address=0x2000, data=0x55, write=True)

    for i in range(6):
        print(f"\nT{i+1}:")
        result = biu.clock_cycle(ready=(i >= 3))
        print(f"  State: {result['state']}")
        print(f"  Signals: ALE={result['signals']['ale']}, WR={result['signals']['wr']}")
        if 'address' in result:
            print(f"  Address Latch: 0x{result['address']:04X}")
        if 'data_out' in result and result['data_out'] is not None:
            print(f"  Data Out: 0x{result['data_out']:02X}")

    # Wait State
    print("\n[Wait State (느린 메모리)]")
    print("CPU: Read @ 0x3000")

    biu = BusInterfaceUnit()
    biu.cpu_request(address=0x3000, data=0, write=False)

    # Ready가 늦게 옴
    ready_sequence = [False, False, False, True, True]
    for i, ready in enumerate(ready_sequence):
        print(f"\nT{i+1}:")
        result = biu.clock_cycle(ready=ready)
        print(f"  State: {result['state']}")
        print(f"  READY: {ready}")
        if result['state'] == BusState.WAIT.value:
            print(f"  → Wait State inserted")

    # Address/Data Multiplexing
    print("\n[Address/Data Multiplexing]")
    print("AD[15:0]에 Address와 Data를 Time-Share")

    print("T1: AD[15:0] = Address (0x1000)")
    print("T2: AD[15:0] = Data (0xAB)")
    print("  → Latch가 Address를 저장")
    print("  → AD 버스가 Data로 전환")

    # Tri-state Buffering
    print("\n[Tri-state Buffering]")
    print("OE=0: High-Z (버스에서 분리)")
    print("OE=1: Active (버스 구동)")

    transceiver = DataTransceiver()
    transceiver.disable()
    print(f"  Disabled: Output = {transceiver.get_output()}")

    transceiver.enable()
    transceiver.set_internal(0x55)
    transceiver.set_dir(True)
    print(f"  Enabled (Write): Output = 0x{transceiver.get_output():02X}")

    transceiver.set_dir(False)
    print(f"  Enabled (Read): Input = {transceiver.get_input():02X}")


if __name__ == "__main__":
    demonstration()
```
