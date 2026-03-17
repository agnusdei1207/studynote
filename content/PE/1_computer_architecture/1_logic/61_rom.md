+++
title = "ROM (Read-Only Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# ROM (Read-Only Memory)

## 핵심 인사이트 (3줄 요약)
1. ROM(Read-Only Memory)은 읽기 전용 메모리로 제조 시 데이터가 프로그램되며, 전원이 꺼져도 내용이 유지되는 비휘발성 메모리이다
2. Mask ROM, PROM, EPROM, EEPROM 등 다양한 형태가 있으며, 어드레스 디코더와 데이터 저장 셀 어레이로 구성된다
3. 기술사시험에서는 ROM 구조, 어드레싱 방식, 각 타입별 특징과 응용이 핵심이다

## Ⅰ. 개요 (500자 이상)

ROM(Read-Only Memory)은 **읽기 전용 메모리로, 제조 시 또는 사용자가 한 번 프로그램하면 변경할 수 없거나 특수한 방법으로만 재프로그래밍 가능한 비휘발성 메모리**이다. 전원이 공급되지 않아도 저장된 데이터를 유지하며, 주로 펌웨어, 부팅 코드, 마이크로코드 등을 저장하는 데 사용된다.

```
ROM 기본 개념:
구조: 2D 어레이 (Word × Bit)
입력: Address[n-1:0], CS (Chip Select)
출력: Data[m-1:0]

동작:
- Address로 Word 선택
- Decoder 활성화
- Data 출력
- 쓰기 불가 (일반적)

특징:
- 비휘발성
- 읽기 전용
- 빠른 액세스
- 낮은 지연
```

**ROM의 핵심 특징:**

1. **비휘발성**: 전원 차단 후에도 데이터 유지
2. **읽기 전용**: 일반적으로 쓰기 불가
3. **빠른 액세스**: RAM보다 빠를 수 있음
4. **낮은 비용**: 대량 생산 시 저렴

```
ROM vs RAM:
ROM:
- 비휘발성
- 읽기 전용
- 느린 쓰기 (불가능)
- 펌웨어 저장

RAM:
- 휘발성
- 읽기/쓰기
- 빠른 쓰기
- 데이터 저장
```

ROM은 컴퓨터 부팅, 임베디드 시스템, 마이크로컨트롤러 등 다양한 곳에 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### ROM 기본 구조

```
n×m 비트 ROM 구조:

Address[n-1:0]
│
├──[Address Decoder]── Word Lines[2ⁿ-1:0]
│                  │
│    Cell[0,0] ────┤
│    Cell[0,1] ────┤
│     ...      ────┼──[Sense Amp]── Data[m-1:0]
│    Cell[m-1,0]───┘
│
    [CS] ────────────── Output Enable

구성 요소:
1. Address Decoder: n→2ⁿ 디코더
2. Cell Array: 2ⁿ×m 비트 셀
3. Sense Amp: 데이터 증폭
4. Output Buffer: 출력 버퍼

동작:
1. Address 입력
2. Decoder가 Word Line 활성화
3. 해당 셀의 데이터 판독
4. Sense Amp로 증폭
5. 출력
```

### 어드레스 디코딩

```
어드레스 디코딩 방식:

1D 디코딩 (선형):
A[3:0] ──[Decoder]── WL[15:0]

장점: 단순
단점: Decoder 크기 커짐

2D 디코딩 (매트릭스):
A[7:4] ──[Decoder]── Row[15:0]
A[3:0] ──[Decoder]── Col[15:0]

장점: Decoder 크기 작음
단점: 복잡

2D 예 (256×8):
A[7:4] → 16 Row Decoder
A[3:0] → 16 Column Decoder
Word → Row∩Col
```

### 셀 구조

```
ROM 셀 구조 (Mask ROM):

VDD
 │
 │    WL
 │    │
 └─┬──┤
   │  │
  ┌┴┐ │
  │ │ │ ── Bit Line
  └─┘ │
      │
    GND

Presence/Absence of Transistor:
- TR 존재: Bit Line Pull-down → 0
- TR 없음: Bit Line Pull-up → 1

구현:
- Mask ROM: 마스크로 TR 배치 결정
- PROM: 퓨즈로 TR 연결/절단
- EPROM: FAMOS TR
- EEPROM: Floating Gate
```

### Mask ROM

```
Mask ROM (MROM):

제조 공정:
1. 마스크 설계 (데이터 패턴)
2. 웨이퍼 제조 시 TR 배치 결정
3. Metalization으로 연결/절단

특징:
- 제조 시 데이터 결정
- 변경 불가
- 대량 생산 시 저렴
- 낮은 단가

응용:
- BIOS (과거)
- 캐릭터 ROM
- 마이크로코드
- 고정 데이터

용량: 1KB ~ 1MB+
지연: 50-200ns
```

### PROM (Programmable ROM)

```
PROM (一次性):

구조:
- 퓨즈(Fuse) 기반
- 모든 셀에 TR 존재
- 프로그래밍 시 퓨즈 절단

프로그래밍:
- 고전압 적용 (12-21V)
- 퓨즈 과전류로 절단
- 한 번만 프로그래밍 가능

타이밍:
VPP ──┐
      │ 12-21V
      └──┐
         │ Program
Address ───┐
           │
Data ──────┘

특징:
- 사용자 프로그래밍
- 일회성
- 소량 생산 적합
```

### EPROM (Erasable PROM)

```
EPROM (UV Erasable):

구조:
- FAMOS (Floating Gate Avalanche MOS)
- Floating Gate에 전하 저장
- UV로 전하 방출

프로그래밍:
- 고전압 (12-25V)
- 항복(Breakdown)으로 전하 주입
- 전하 = 논리 0

소거(Erase):
- UV 광 노출 (QUARTZ 윈도우)
- 10-20분 노출
- 전체 소거 (선택 불가)

특징:
- 재프로그래밍 가능 (100~1000회)
- UV 소거
- QUARTZ 패키지

응용:
- 개발 보드
- 마이크로컨트롤러
- prototyping
```

### EEPROM (Electrically EPROM)

```
EEPROM (전기적 소거):

구조:
- Floating Gate MOS
- 전기적 소거 가능
- 바이트 단위 소거

프로그래밍/소거:
- Fowler-Nordheim Tunneling
- 고전압 터널링 (±12-20V)
- 바이트 단위 쓰기/소거

특징:
- 전기적 재프로그래밍
- 바이트 단위 액세스
- 수십만 회 쓰기 가능
- 느린 쓰기 (ms)

지연:
- 읽기: 50-200ns
- 쓰기: 1-10ms

응용:
- BIOS
- 설정 저장
- 시스템 데이터
```

### Flash Memory

```
Flash Memory:

구조:
- EEPROM 기술 기반
- 블록 단위 소거
- NOR vs NAND

NOR Flash:
- 임의 액세스
- XIP (eXecute In Place)
- 소용량
- 코드 저장

NAND Flash:
- 순차 액세스
- 밀도 높음
- 대용량
- 데이터 저장

소거 단위:
- NOR: 64KB-1MB 블록
- NAND: 16KB-256KB 페이지

특징:
- 전기적 소거/쓰기
- 블록 단위 소거
- 10만-100만 회 쓰기
- 빠른 읽기
```

## Ⅲ. 융합 비교

### ROM 타입 비교

| 타입 | 프로그래밍 | 소거 | 재작성 | 속도 | 응용 |
|------|-----------|------|--------|------|------|
| Mask ROM | 제조사 | 불가 | 불가 | 빠름 | 대량 생산 |
| PROM | 사용자 | 불가 | 불가 | 빠름 | 프로토타입 |
| EPROM | 사용자 | UV | 가능 | 중간 | 개발 |
| EEPROM | 사용자 | 전기 | 가능 | 느림 | 설정 |
| Flash | 사용자 | 전기 | 가능 | 중간 | 저장소 |

### ROM vs RAM

| 비교 항목 | ROM | RAM |
|----------|-----|-----|
| 휘발성 | 없음 | 있음 |
| 읽기 | 가능 | 가능 |
| 쓰기 | 불가/제한 | 자유 |
| 비트 당 비용 | 낮음 | 높음 |
| 밀도 | 높음 | 중간 |
| 속도 | 빠름 | 매우 빠름 |
| 응용 | 코드 | 데이터 |

### Flash 타입

| 타입 | 구조 | 액세스 | 밀도 | 응용 |
|------|------|--------|------|------|
| NOR | 병렬 | 임의 | 낮음 | 코드 |
| NAND | 직렬 | 순차 | 높음 | 데이터 |
| 3D NAND | 적층 | 순차 | 매우 높음 | SSD |

## Ⅳ. 실무 적용 및 기술사적 판단

### BIOS ROM

```
BIOS (Basic Input/Output System):

위치: 메인보드 ROM
용량: 1MB-8MB
기능:
- POST (Power-On Self-Test)
- 부팅 로더
- 하드웨어 초기화
- 인터럽트 핸들러

구현:
- 과거: Mask ROM, EPROM
- 현재: Flash BIOS
- 업데이트 가능

액세스:
CPU → Address → BIOS ROM → Instruction

특징:
- XIP (eXecute In Place)
- 첫 16KB @ 0xFFFF0000 (x86)
- Shadowing 가능
```

### 마이크로코드 ROM

```
마이크로코드:

용도:
- CISC 명령어 내부 마이크로연산
- 복잡한 명령어 구현

구조:
Microcode ROM:
- Address: Opcode + Flags
- Output: Micro-operations

예: Intel x86
MUL 명령어:
- Microcode: Load, Shift, Add, Store...
- ROM Lookup으로 마이크로연산 시퀀스

특징:
- CISC 복잡성 숨김
- 버그 수정 용이 (패치)
- 면적/전력 비용
```

### 임베디드 시스템

```
임베디드 시스템 메모리 맵:

0x0000: Reset Vector (ROM)
0x0004: Interrupt Vector (ROM)
...
0x8000: Application Code (ROM)
0xF000: Bootloader (Flash ROM)

0x10000: RAM 시작
0x10000: Data Section
0x20000: Heap
0x30000: Stack

특징:
- 코드: ROM/Flash
- 데이터: RAM
- 부팅: ROM
```

### FPGA Configuration ROM

```
FPGA Configuration:

구성:
- Configuration ROM (Flash)
- Bitstream 저장
- 전원 켜기 시 로딩

동작:
1. 전원 ON
2. FPGA 내부 Controller 활성화
3. Config ROM → Bitstream 로드
4. Configuration SRAM에 로드
5. FPGA 동작 시작

특징:
- 비휘발성 설정 저장
- 빠른 로딩 (ms)
- 재프로그래밍 가능
```

## Ⅴ. 기대효과 및 결론

ROM은 비휘발성 저장의 기초이다. 시스템 부팅과 펌웨어 저장에 필수적이다.

## 📌 관련 개념 맵

```
ROM
├── 타입
│   ├── Mask ROM (제조사 프로그래밍)
│   ├── PROM (일회성)
│   ├── EPROM (UV 소거)
│   ├── EEPROM (전기적 소거)
│   └── Flash (블록 소거)
├── 구조
│   ├── Address Decoder
│   ├── Cell Array
│   ├── Sense Amplifier
│   └── Output Buffer
├── 특징
│   ├── 비휘발성
│   ├── 읽기 전용
│   └── 빠른 액세스
└── 응용
    ├── BIOS/UEFI
    ├── 마이크로코드
    ├── 임베디드 시스템
    └── FPGA Configuration
```

## 👶 어린이를 위한 3줄 비유 설명

1. ROM은 한 번 적으면 지울 수 없는 노트 같아요. 공장에서 미리 적어놓거나, 한 번만 적을 수 있어요
2. 전원을 꺼도 내용이 안 사라져서 컴퓨터가 켜질 때 가장 먼저 실행해야 할 프로그램(BIOS)을 저장해요
3. EPROM은 자외선을 쬐면 지워져서 다시 쓸 수 있고, Flash는 USB 메모리처럼 컴퓨터에서 지우고 다시 쓸 수 있어요

```python
# ROM 시뮬레이션

from typing import List


class ROM:
    """기본 ROM 시뮬레이션"""

    def __init__(self, size: int, word_size: int = 8, data: List[int] = None):
        """
        ROM 초기화

        Args:
            size: 워드 수 (2ⁿ)
            word_size: 워드 비트 수
            data: 초기 데이터
        """
        self.size = size
        self.word_size = word_size
        self.data = [0] * size

        if data:
            for i, val in enumerate(data):
                if i < size:
                    self.data[i] = val & ((1 << word_size) - 1)

    def read(self, address: int) -> int:
        """
        읽기

        Args:
            address: 읽기 주소

        Returns:
            데이터
        """
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")
        return self.data[address]

    def __str__(self):
        result = f"ROM ({self.size}x{self.word_size}):\n"
        for i in range(0, self.size, 8):
            row = []
            for j in range(8):
                if i + j < self.size:
                    row.append(f"[{i+j:3d}]=0x{self.data[i+j]:02X}")
            result += "  " + " ".join(row) + "\n"
        return result


class MaskROM(ROM):
    """Mask ROM (제조 시 데이터 결정)"""

    def __init__(self, mask_data: List[int]):
        super().__init__(len(mask_data), 8, mask_data)
        self.mask_data = mask_data.copy()

    def is_programmable(self) -> bool:
        """프로그래밍 가능 여부"""
        return False


class PROM(ROM):
    """PROM (일회성 프로그래밍)"""

    def __init__(self, size: int, word_size: int = 8):
        super().__init__(size, word_size)
        self.programmed = [False] * size

    def program(self, address: int, data: int) -> bool:
        """
        프로그래밍 (퓨즈 절단)

        Args:
            address: 프로그램 주소
            data: 프로그램 데이터

        Returns:
            성공 여부
        """
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")

        if self.programmed[address]:
            print(f"  Error: 주소 {address}는 이미 프로그램됨")
            return False

        self.data[address] = data & ((1 << self.word_size) - 1)
        self.programmed[address] = True
        return True

    def is_programmable(self) -> bool:
        return True


class EPROM(ROM):
    """EPROM (UV 소거)"""

    def __init__(self, size: int, word_size: int = 8):
        super().__init__(size, word_size)
        self.program_count = 0
        self.max_programs = 1000

    def program(self, address: int, data: int):
        """프로그래밍"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")

        self.data[address] = data & ((1 << self.word_size) - 1)
        self.program_count += 1

    def erase_uv(self):
        """UV 소거 (전체 소거)"""
        self.data = [0] * self.size
        print("  EPROM UV 소거 완료 (모두 0으로 초기화)")

    def can_program(self) -> bool:
        """프로그래밍 가능 여부"""
        return self.program_count < self.max_programs


class EEPROM(ROM):
    """EEPROM (전기적 소거)"""

    def __init__(self, size: int, word_size: int = 8):
        super().__init__(size, word_size)
        self.write_count = 0
        self.max_writes = 100000

    def write(self, address: int, data: int):
        """바이트 단위 쓰기"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")

        if self.write_count >= self.max_writes:
            raise RuntimeError("쓰기 횟수 초과")

        self.data[address] = data & ((1 << self.word_size) - 1)
        self.write_count += 1

    def erase(self, address: int):
        """바이트 단위 소거"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")

        self.data[address] = 0


class FlashROM:
    """Flash ROM (블록 단위 소거)"""

    def __init__(self, size: int, block_size: int = 64, word_size: int = 8):
        self.size = size
        self.block_size = block_size
        self.word_size = word_size
        self.data = [0] * size
        self.write_count = 0
        self.max_writes = 100000

    def read(self, address: int) -> int:
        """읽기"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")
        return self.data[address]

    def write(self, address: int, data: int):
        """페이지 단위 쓰기 (소거 후 가능)"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")

        if self.data[address] != 0:
            # 소거되지 않으면 에러
            block = address // self.block_size
            raise ValueError(f"블록 {block}가 소거되지 않음 (먼저 소거 필요)")

        self.data[address] = data & ((1 << self.word_size) - 1)
        self.write_count += 1

    def erase_block(self, block: int):
        """블록 단위 소거"""
        if not (0 <= block < self.size // self.block_size):
            raise ValueError(f"블록 번호 초과: {block}")

        start = block * self.block_size
        for i in range(start, min(start + self.block_size, self.size)):
            self.data[i] = 0


def demonstration():
    """ROM 데모"""
    print("=" * 60)
    print("ROM (Read-Only Memory) 데모")
    print("=" * 60)

    # Mask ROM
    print("\n[Mask ROM]")
    bios_data = [0xEA, 0x00, 0xE0, 0x00, 0x10, 0x20, 0x30, 0x40]
    mask_rom = MaskROM(bios_data)
    print(mask_rom)
    print(f"주소 0 읽기: 0x{mask_rom.read(0):02X}")

    # PROM
    print("\n[PROM (일회성 프로그래밍)]")
    prom = PROM(size=16, word_size=8)

    # 프로그래밍
    print("프로그래밍:")
    prom.program(0, 0xAA)
    print("  주소 0 ← 0xAA")
    prom.program(1, 0x55)
    print("  주소 1 ← 0x55")

    # 재프로그래밍 시도
    print("\n재프로그래밍 시도:")
    prom.program(0, 0xFF)  # 실패해야 함

    print(f"\n주소 0 읽기: 0x{prom.read(0):02X}")
    print(f"주소 1 읽기: 0x{prom.read(1):02X}")

    # EPROM
    print("\n[EPROM (UV 소거)]")
    eprom = EPROM(size=8)

    # 프로그래밍
    print("프로그래밍:")
    for i in range(8):
        eprom.program(i, i * 0x11)
        print(f"  주소 {i} ← 0x{i * 0x11:02X}")

    print(f"\n주소 3 읽기: 0x{eprom.read(3):02X}")

    # UV 소거
    print("\nUV 소거:")
    eprom.erase_uv()
    print(f"주소 3 읽기: 0x{eprom.read(3):02X}")

    # EEPROM
    print("\n[EEPROM (전기적 소거)]")
    eeprom = EEPROM(size=8)

    # 쓰기
    print("쓰기:")
    for i in range(4):
        eeprom.write(i, 0x10 * (i + 1))
        print(f"  주소 {i} ← 0x{0x10 * (i + 1):02X}")

    print(f"\n주소 2 읽기: 0x{eeprom.read(2):02X}")

    # 소거 후 재작성
    print("\n소거 후 재작성:")
    eeprom.erase(2)
    eeprom.write(2, 0xFF)
    print(f"  주소 2 ← 0xFF")
    print(f"  주소 2 읽기: 0x{eeprom.read(2):02X}")

    # Flash ROM
    print("\n[Flash ROM (블록 단위 소거)]")
    flash = FlashROM(size=256, block_size=64, word_size=8)

    # 읽기 (초기 0)
    print("초기 상태:")
    print(f"  주소 0 읽기: 0x{flash.read(0):02X}")

    # 쓰기 시도 (소거 안 함)
    print("\n쓰기 시도 (소거 안 함):")
    try:
        flash.write(0, 0xAA)
    except ValueError as e:
        print(f"  Error: {e}")

    # 블록 소거 후 쓰기
    print("\n블록 0 소거 후 쓰기:")
    flash.erase_block(0)
    flash.write(0, 0xAA)
    print(f"  주소 0 ← 0xAA")
    print(f"  주소 0 읽기: 0x{flash.read(0):02X}")

    # BIOS 시뮬레이션
    print("\n[BIOS ROM 시뮬레이션]")
    bios = ROM(size=16, word_size=8, data=[
        0xEA, 0x00,  # JMP 0x0000 (Reset Vector)
        0xE0, 0x00,  # MOV A, 0x00
        0x10, 0x20,  # ADD 0x1020
        0x30, 0x40,  # SUB 0x3040
        0x50, 0x60,  # MUL 0x5060
        0x70, 0x80,  # DIV 0x7080
        0x90, 0xA0,  # AND 0x90A0
        0xB0, 0xC0,  # OR  0xB0C0
    ])

    print("Reset Vector (주소 0-1):")
    print(f"  0x{bios.read(0):02X} 0x{bios.read(1):02X}")

    print("\n명령어 페치:")
    for i in range(0, 16, 2):
        opcode = bios.read(i)
        operand_low = bios.read(i + 1)
        print(f"  주소 {i:2d}: Opcode=0x{opcode:02X}, Operand=0x{operand_low:02X}")


if __name__ == "__main__":
    demonstration()
```
