+++
title = "DMA (Direct Memory Access)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# DMA (Direct Memory Access)

## 핵심 인사이트 (3줄 요약)
1. DMA(Direct Memory Access)는 CPU 개입 없이 장치와 메모리 간에 직접 데이터를 전송하는 하드웨어로, CPU 부하를 줄이고 전송 효율을 높인다
2. DMA 컨트롤러는 주소 레지스터, 카운터, 제어 레지스터로 구성되며 Cycle Stealing, Burst Mode, Transparent 모드로 동작한다
3. 기술사시험에서는 DMA 동작 원리, 전송 모드, CPU-DMA 경쟁, 버스 마스터링이 핵심이다

## Ⅰ. 개요 (500자 이상)

DMA(Direct Memory Access)는 **CPU의 개입 없이 I/O 장치와 메모리 사이에서 직접 데이터를 전송하는 하드웨어 메커니즘**이다. CPU가 모든 데이터 전송을 처리하는 방식(Programmed I/O)의 비효율을 해결하기 위해 고안되었다.

```
DMA 기본 개념:
목적: CPU 부하 없는 데이터 전송
구현: DMA Controller (DMAC)
동작: 장치 ↔ DMA ↔ 메모리

특징:
- CPU 독립적 동작
- 높은 전송 속도
- 버스 마스터링
- 블록 전송

장점:
- CPU 효율 ↑ (다른 작업 가능)
- 전송 속도 ↑ (버스 직접 제어)
- 인터럽트 감소 (블록 단위)
```

**DMA의 핵심 특징:**

1. **버스 마스터링**: DMA가 버스를 제어
2. **CPU 독립**: 전송 중 CPU 다른 작업 가능
3. **블록 전송**: 대량 데이터 한 번에 전송
4. **자동 완료**: 카운트만큼 전송 후 인터럽트

```
Programmed I/O vs DMA:
Programmed I/O:
- CPU가 모든 바이트 전송
- 느림
- CPU 점유

DMA:
- DMA가 전체 블록 전송
- 빠름
- CPU 해방
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### DMA 컨트롤러 구조

```
DMA Controller 구조:

CPU ←─→ DMAC
           │
        Control Registers:
        - CAR (Current Address Register)
        - CCR (Current Count Register)
        - MAR (Memory Address Register)
        - DAR (Device Address Register)
        - MR (Mode Register)
        - SR (Status Register)

    Channels (typically 4-8):
    CH0: [Addr][Count][Control] → Device 0
    CH1: [Addr][Count][Control] → Device 1
    CH2: [Addr][Count][Control] → Device 2
    CH3: [Addr][Count][Control] → Device 3

    Priority Encoder:
    - 다중 채널 중 하나 선택
    - Fixed / Rotating Priority

    Bus Interface:
    - Address Bus
    - Data Bus
    - Control Bus (HRQ, HLDA, DREQ, DACK)
```

### DMA 동작 과정

```
DMA 전송 과정:

1. 초기화 (CPU):
   - 소스 주소 설정
   - 목적지 주소 설정
   - 전송 바이트 수 설정
   - 전송 모드 설정
   - DMA 활성화

2. DMA 요청 (DREQ):
   Device → DMAC → DREQ 신호

3. 버스 요청 (HRQ):
   DMAC → CPU → HRQ (Hold Request)

4. 버스 승인 (HLDA):
   CPU → DMAC → HLDA (Hold Acknowledge)
   CPU는 버스를 양보

5. DMA 전송:
   DMAC가 버스 제어
   Memory ↔ Device 데이터 전송

6. 카운트 감소:
   전송마다 카운트 감소

7. 완료 (Terminal Count):
   Count = 0
   DMAC → CPU → 인터럽트

8. 버스 반환:
   DMAC → CPU → 버스 반환
```

### DMA 전송 모드

```
1. Single Transfer Mode:
   - 바이트/워드 단위 전송
   - 매번 DREQ 필요
   - CPU가 버스를 자주 회수

2. Block Transfer Mode (Burst):
   - 블록 전체 연속 전송
   - 한 번 DREQ로 전체 전송
   - CPU는 완료까지 버스 양보

3. Demand Transfer Mode:
   - DREQ 활성 중 계속 전송
   - DREQ 해제 시 중단
   - 나중에 재개 가능

4. Cascade Mode:
   - DMAC 여러 개 연결
   - Master-Slave 구조
```

### Cycle Stealing

```
Cycle Stealing:

개념:
- DMA가 CPU 사이클 "훔치기"
- CPU와 DMA가 버스 번갈아 사용

타이밍:
CPU: ─┬─┬─┬─┬─┬─┬─┬─┬─┬─
     │ │ │ │ │ │ │ │ │
DMA: ──┴─┴─┴─┴─────┴─┴─┴─┴─
     ←───Steal──→  ←─Steal─→

특징:
- 전송 중 CPU도 작동
- 전체 성능 저하 적음
- 전송 시간 길어짐

응용:
- 저속 장치
- 실시간 시스템
```

### Burst Mode

```
Burst Mode:

개념:
- 연속적인 버스 사이클 점유
- 전체 블록 연속 전송

타이밍:
CPU: ─┬────────────────────┬─
     │                    │
DMA: ─┴←──Burst───→────────┴─

특징:
- 최대 전송 속도
- CPU는 완료까지 대기
- 높은 버스 점유

응용:
- 고속 장치
- 대용량 전송
- Disk I/O
```

### Fly-By Transfer

```
Fly-By Transfer (Transparent):

개념:
- 메모리에 저장하지 않고
- 장치로 직접 전송

과정:
Device → DMAC → Device (Read)
Memory → DMAC → Device (Write)

특징:
- 추가 버스 사이클 불필요
- 메모리 액세스 감소
- 빠른 전송

제한:
- 일부 DMA만 지원
- 메모리-메모리 전송 불가
```

### Bus Arbitration

```
DMA 버스 중재 (Arbitration):

다중 DMA 채널:
DREQ0 ──┐
DREQ1 ──┤
DREQ2 ──┼──→ Priority Encoder → Channel Select
DREQ3 ──┘

우선순위 방식:
1. Fixed Priority:
   CH0 > CH1 > CH2 > CH3
   - 단순
   - 기아(Starvation) 가능

2. Rotating Priority:
   - Round Robin
   - 공평한 기회

3. Flat Priority:
   - 같은 우선순위
   - FCFS

HRQ/HLDA 프로토콜:
DMAC: CPU, HRQ (버스 요청)
CPU: DMAC, HLDA (버스 승인)
DMAC: 전송 수행
DMAC: CPU, 완료 알림
```

## Ⅲ. 융합 비교

### I/O 방식 비교

| 방식 | CPU 개입 | 속도 | 복잡도 | 응용 |
|------|---------|------|--------|------|
| Programmed I/O | 매 바이트 | 느림 | 낮음 | 단순 장치 |
| Interrupt I/O | 인터럽트 시 | 중간 | 중간 | 문자 장치 |
| DMA | 초기화/완료만 | 빠름 | 높음 | 블록 장치 |

### DMA 전송 모드

| 모드 | 버스 점유 | CPU 간섭 | 속도 | 응용 |
|------|----------|----------|------|------|
| Single | 짧음 | 있음 | 느림 | 저속 |
| Block | 김 | 없음 | 빠름 | 고속 |
| Demand | 가변 | 있음 | 중간 | 유연 |
| Cascade | - | - | - | 다단계 |

### DMA 컨트롤러

| 타입 | 채널 | 데이터 폭 | 특징 | 응용 |
|------|-------|-----------|------|------|
| 8237A | 4 | 8/16비트 | Cascade 지원 | x86 PC |
| PDMA | 8+ | 32/64비트 | 고성능 | 현대 CPU |
| Intel I/OAT | 여러 | 64비트 | Offload | Server |

## Ⅳ. 실무 적용 및 기술사적 판단

### 8237A DMA

```
Intel 8237A DMAC:

구조:
- 4개 채널 (8비트)
- Cascade로 8개 확장
- 64KB 전송 가능

레지스터:
- CAR: Current Address (16비트)
- CCR: Current Count (16비트)
- MAR: Memory Address
- PR: Page Register (상위 4비트)

채널 할당:
CH0: DRAM Refresh (사용 안 함)
CH1: (예약)
CH2: Floppy Disk
CH3: (예약)

Slave 8237:
CH0-3: Master CH4-7에 연결
```

### IDE/ATA DMA

```
IDE DMA (Bus Master):

구조:
Drive ←→ Bus Master DMA ←→ Memory

PIO vs DMA:
PIO: CPU가 모든 데이터 전송
DMA: Drive가 메모리에 직접 전송

UDMA (Ultra DMA):
- 33, 66, 100, 133 MB/s
- Double Edge Clocking
- CRC Error Detection

전송 모드:
- Multiword DMA
- Ultra DMA
```

### PCI DMA

```
PCI Bus Mastering:

DMA 절차:
1. Device가 Bus Master 요청
2. PCI Arbiter가 승인
3. Device가 메모리 주소 버스에
4. 데이터 전송
5. 완료 후 버스 반환

특징:
- 장치가 Bus Master 가능
- Memory Mapped I/O
- Scatter-Gather 지원

Scatter-Gather:
- 불연속 메모리 전송
- 여러 작은 버퍼를 하나로
- SG List 사용
```

### Scatter-Gather DMA

```
Scatter-Gather:

개념:
불연속 메모리 영역을
하나의 연속된 데이터로 전송

Memory Layout:
[Buffer 0: 0x1000-0x10FF]
[Buffer 1: 0x2000-0x20FF]
[Buffer 2: 0x3000-0x30FF]

SG List:
Entry 0: {Addr=0x1000, Len=0x100}
Entry 1: {Addr=0x2000, Len=0x100}
Entry 2: {Addr=0x3000, Len=0x100}

DMA 전송:
Device → SG List 순서대로 전송
CPU: 한 번의 DMA 요청으로 완료

장점:
- 메모리 복사 불필요
- Fragmented 버퍼 지원
- 효율적 네트워크 I/O
```

## Ⅴ. 기대효과 및 결론

DMA는 고속 I/O의 핵심이다. CPU를 해방시키고 전송 효율을 극대화한다.

## 📌 관련 개념 맵

```
DMA
├── 구조
│   ├── DMA Controller (DMAC)
│   ├── Address Register
│   ├── Count Register
│   └── Control Register
├── 동작
│   ├── 초기화 (CPU)
│   ├── DREQ (장치 요청)
│   ├── HRQ/HLDA (버스 요청/승인)
│   └── 전송 및 완료
├── 모드
│   ├── Single (Cycle Stealing)
│   ├── Block (Burst)
│   ├── Demand
│   └── Cascade
└── 특징
    ├── Bus Mastering
    ├── CPU 독립
    ├── 블록 전송
    └── Scatter-Gather
```

## 👶 어린이를 위한 3줄 비유 설명

1. DMA는 택배 기사 같아요. CPU가 일하는 동안 택배 기사가 물건을(데이터를) 집(메모리)으로 배달해요
2. Programmed I/O는 CPU가 택배를 직접 나르는 거고, DMA는 택배 회사에 맡기는 거예요. 훨씬 효율적이죠
3. Cycle Stealing은 택배 기사가 길을 잠깐 쓰는 거고, Burst는 도로 전체를 독점해서 쓰는 거예요. Burst는 더 빠르지만 다른 차(CPU)는 기다려야 해요

```python
# DMA 시뮬레이션

from typing import List, Dict, Optional
from enum import Enum


class DMAMode(Enum):
    SINGLE = "Single Transfer"
    BLOCK = "Block Transfer"
    DEMAND = "Demand Transfer"
    CASCADE = "Cascade"


class DMAChannel:
    """DMA 채널"""

    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.current_address = 0
        self.current_count = 0
        self.base_address = 0
        self.base_count = 0
        self.mode = DMAMode.SINGLE
        self.device = None
        self.active = False

    def initialize(self, address: int, count: int, mode: DMAMode):
        """채널 초기화"""
        self.base_address = address
        self.base_count = count
        self.current_address = address
        self.current_count = count
        self.mode = mode
        self.active = False

    def reset(self):
        """채널 리셋"""
        self.current_address = self.base_address
        self.current_count = self.base_count
        self.active = False


class DMAController:
    """DMA 컨트롤러"""

    def __init__(self, num_channels: int = 4):
        self.num_channels = num_channels
        self.channels = [DMAChannel(i) for i in range(num_channels)]
        self.memory = [0] * 65536  # 64KB 메모리
        self.hrq = False  # Hold Request
        self.hlda = False  # Hold Acknowledge
        self.current_channel = None

    def write_memory(self, address: int, data: int):
        """메모리 쓰기"""
        if 0 <= address < len(self.memory):
            self.memory[address] = data & 0xFF

    def read_memory(self, address: int) -> int:
        """메모리 읽기"""
        if 0 <= address < len(self.memory):
            return self.memory[address]
        return 0

    def request_dma(self, channel_id: int):
        """DMA 요청 (DREQ)"""
        if 0 <= channel_id < self.num_channels:
            channel = self.channels[channel_id]
            if channel.current_count > 0:
                self.hrq = True
                return True
        return False

    def grant_bus(self):
        """버스 승인 (HLDA)"""
        self.hlda = True

    def release_bus(self):
        """버스 반환"""
        self.hlda = False
        self.current_channel = None

    def select_channel(self) -> Optional[int]:
        """우선순위 기반 채널 선택"""
        for i in range(self.num_channels):
            ch = self.channels[i]
            if ch.current_count > 0:
                return i
        return None

    def transfer_single(self, channel_id: int) -> bool:
        """단일 전송 (Cycle Stealing)"""
        channel = self.channels[channel_id]

        if channel.current_count <= 0:
            return False

        # 전송 (Read 예)
        data = channel.device.read() if channel.device else 0
        self.write_memory(channel.current_address, data)

        # 업데이트
        channel.current_address += 1
        channel.current_count -= 1

        return True

    def transfer_block(self, channel_id: int) -> int:
        """블록 전송 (Burst)"""
        channel = self.channels[channel_id]
        transferred = 0

        while channel.current_count > 0:
            data = channel.device.read() if channel.device else 0
            self.write_memory(channel.current_address, data)

            channel.current_address += 1
            channel.current_count -= 1
            transferred += 1

        return transferred

    def execute(self) -> Dict:
        """DMA 실행"""
        if not self.hlda:
            return {"status": "waiting for bus"}

        channel_id = self.select_channel()
        if channel_id is None:
            return {"status": "no active channel"}

        channel = self.channels[channel_id]
        self.current_channel = channel_id

        if channel.mode == DMAMode.SINGLE:
            success = self.transfer_single(channel_id)
            return {
                "channel": channel_id,
                "mode": "single",
                "remaining": channel.current_count,
                "address": channel.current_address
            }

        elif channel.mode == DMAMode.BLOCK:
            transferred = self.transfer_block(channel_id)
            return {
                "channel": channel_id,
                "mode": "block",
                "transferred": transferred,
                "complete": channel.current_count == 0
            }

        return {"status": "unknown mode"}


class Device:
    """I/O 장치"""

    def __init__(self, name: str):
        self.name = name
        self.data = 0

    def read(self) -> int:
        """데이터 읽기"""
        return self.data

    def write(self, data: int):
        """데이터 쓰기"""
        self.data = data


class CPU:
    """CPU 시뮬레이션"""

    def __init__(self):
        self.working = True
        self.instructions_executed = 0

    def execute_instruction(self):
        """명령어 실행"""
        self.instructions_executed += 1

    def handle_hrq(self, dma: DMAController) -> bool:
        """HRQ 처리"""
        if dma.hrq and not dma.hlda:
            print(f"[CPU] HRQ received, granting HLDA")
            dma.grant_bus()
            return True
        return False

    def check_dma_complete(self, dma: DMAController):
        """DMA 완료 확인"""
        if dma.hlda and dma.current_channel is not None:
            ch = dma.channels[dma.current_channel]
            if ch.current_count == 0:
                print(f"[CPU] DMA on CH{dma.current_channel} complete")
                dma.release_bus()
                ch.active = False


def demonstration():
    """DMA 데모"""
    print("=" * 60)
    print("DMA (Direct Memory Access) 데모")
    print("=" * 60)

    # 초기화
    dma = DMAController(num_channels=4)
    cpu = CPU()

    # 장치
    disk = Device("Disk")
    network = Device("Network")

    # 채널 설정
    print("\n[DMA 채널 초기화]")
    dma.channels[0].device = disk
    dma.channels[0].initialize(0x1000, 10, DMAMode.SINGLE)
    print(f"  CH0: Address=0x{0x1000:04X}, Count=10, Mode=Single")

    dma.channels[1].device = network
    dma.channels[1].initialize(0x2000, 5, DMAMode.BLOCK)
    print(f"  CH1: Address=0x{0x2000:04X}, Count=5, Mode=Block")

    # Single Transfer Mode
    print("\n[Single Transfer Mode (Cycle Stealing)]")
    disk.data = 0xAA

    for i in range(3):
        print(f"\n  Cycle {i+1}:")

        # DMA 요청
        if dma.request_dma(0):
            cpu.handle_hrq(dma)

            # DMA 전송
            result = dma.execute()
            print(f"    DMA: {result}")

            # CPU가 버스를 회수하여 작업
            dma.release_bus()
            cpu.execute_instruction()

        # 장치 데이터 변경
        disk.data = 0xBB + i

    # Block Transfer Mode
    print("\n[Block Transfer Mode (Burst)]")
    network.data = 0xCC
    dma.request_dma(1)
    cpu.handle_hrq(dma)

    result = dma.execute()
    print(f"  DMA: {result}")

    # CPU는 전체 블록 전송 동안 대기
    print(f"  CPU: Waiting for DMA complete...")

    # 완료 확인
    cpu.check_dma_complete(dma)
    dma.release_bus()

    # 메모리 확인
    print("\n[메모리 내용 확인]")
    print(f"  0x1000-0x1009: ", end="")
    for i in range(10):
        print(f"{dma.read_memory(0x1000 + i):02X} ", end="")
    print()

    print(f"  0x2000-0x2004: ", end="")
    for i in range(5):
        print(f"{dma.read_memory(0x2000 + i):02X} ", end="")
    print()

    # DMA 우선순위
    print("\n[DMA 채널 우선순위]")
    dma.channels[0].reset()
    dma.channels[0].initialize(0x3000, 3, DMAMode.SINGLE)
    dma.channels[1].reset()
    dma.channels[1].initialize(0x4000, 5, DMAMode.SINGLE)

    # 둘 다 요청
    dma.request_dma(0)
    dma.request_dma(1)

    selected = dma.select_channel()
    print(f"  Selected Channel: {selected} (CH0 has higher priority)")

    # Scatter-Gather
    print("\n[Scatter-Gather DMA]")
    print("  Buffer 0: 0x5000-0x500F")
    print("  Buffer 1: 0x6000-0x600F")
    print("  Buffer 2: 0x7000-0x700F")
    print("  → Device로 연속 전송")

    # 성능 비교
    print("\n[성능 비교]")
    print("  Programmed I/O:")
    print("    - 1000 바이트 전송")
    print("    - CPU: 1000명령어 (LOAD/STORE)")
    print("    - 시간: 1000 클럭")

    print("\n  DMA:")
    print("    - 1000 바이트 전송")
    print("    - CPU: 10명령어 (초기화/완료)")
    print("    - 시간: 100 클럭 (DMA)")
    print("    - 절감: 90%")


if __name__ == "__main__":
    demonstration()
```
