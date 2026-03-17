+++
title = "플래시 메모리 (Flash Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# 플래시 메모리 (Flash Memory)

## 핵심 인사이트 (3줄 요약)
1. 플래시 메모리는 전기적으로 소거 and 재기록 가능한 비휘발성 메모리로, Floating Gate에 전하를 저장하여 데이터를 유지한다
2. NOR 플래시는 임의 액세스가 가능해 코드 실행에 적합하고, NAND 플래시는 순차 액세스에 특화되어 대용량 저장에 적합하다
3. 기술사시험에서는 Floating Gate 구조, 블록 소거, 웨어 레벨링, SLC/MLC/TLC가 핵심이다

## Ⅰ. 개요 (500자 이상)

플래시 메모리(Flash Memory)는 **전기적으로 소거하고 재프로그래밍 가능한 비휘발성 메모리**로, EEPROM 기술을 기반으로 하지만 블록 단위로 소거하여 속도를 높인다. Floating Gate(부유 게이트)에 전하를 주입하여 데이터를 저장하며, 전원이 차단되어도 데이터가 유지된다.

```
플래시 메모리 기본 개념:
구조: Floating Gate MOSFET
- Floating Gate: 전하 저장
- Control Gate: 액세스 제어

동작:
- Program: 전하 주입 (FN Tunneling / Hot Carrier)
- Erase: 전하 방출 (FN Tunneling)
- Read: 문턱 전압 감지

특징:
- 비휘발성
- 전기적 소거/재기록
- 블록 단위 소거
- 높은 밀도
- 낮은 비용
```

**플래시 메모리의 핵심 특징:**

1. **비휘발성**: 전원 차단 후에도 데이터 유지
2. **블록 소거**: 블록/페이지 단위로 소거
3. **전기적 재기록**: 10만~100만 회 쓰기 가능
4. **두 가지 형태**: NOR(코드) vs NAND(데이터)

```
플래시 vs EEPROM:
EEPROM:
- 바이트 단위 소거
- 느린 쓰기
- 낮은 밀도

Flash:
- 블록 단위 소거
- 빠른 쓰기
- 높은 밀도
```

플래시 메모리는 USB 메모리, SD 카드, SSD, 스마트폰 저장소 등 널리 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Floating Gate 구조

```
Floating Gate MOSFET:

Control Gate
     │
     │
  ┌──┴──┐
  │ FG  │ ← Floating Gate (전하 저장)
  └──┬──┘
     │
  ┌──┴──┐
  │ Oxide│ ← Tunnel Oxide (절연층)
  └──┬──┘
     │
  Substrate

동작 원리:
1. Program (쓰기):
   - FG에 전하 주입
   - Vth 증가
   - Cell = 0

2. Erase (소거):
   - FG에서 전하 방출
   - Vth 감소
   - Cell = 1

3. Read (읽기):
   - Vth 측정
   - 전하 있음 → 0
   - 전하 없음 → 1
```

### 프로그래밍 방식

```
1. Hot Carrier Injection (HCI):

NOR Flash Program:

Drain ──┐
        │ High Voltage
Source ─┴───┐
          │
          │    CG
          └───[FG]─┘
              │
            Substrate

동작:
- V_Drain = 높음 (~5V)
- V_CG = 중간 (~10V)
- 전자가 FG로 주입
- 빠르지만 전력 소모 큼

2. Fowler-Nordheim Tunneling:

NAND Flash Program/Erase:

Tunnel Oxide
     │
     │    e⁻ ──── Tunneling
     │   ↗
  ┌──┴──┐
  │ FG  │
  └──┬──┘
     │
  Substrate

동작:
- V_CG = 매우 높음 (~20V)
- 전자가 Oxide를 터널링
- 느리지만 전력 효율적
```

### NOR 플래시

```
NOR 플래시 구조:

Bit Line
  │
  ├─[Cell]─┬─[Cell]─┬─[Cell]─┬─ ...
  │        │        │
WL0 ────┐   │   ┌─────┐
WL1 ─────┼──┼───┼─────┼
WL2 ─────┼──┼───┼─────┼
...      │  │   │     │
        │  │   │     │
      Source Line

구조:
- 셀이 병렬 연결 (NOR 구조)
- 각 셀 독립 액세스
- 임의 액세스 가능

특징:
- 빠른 읽기 (< 100ns)
- XIP (eXecute In Place)
- 낮은 밀도
- 큰 셀 크기
- 코드 저장

응용:
- BIOS/UEFI
- 임베디드 코드
- 마이크로컨트롤러
```

### NAND 플래시

```
NAND 플래시 구조:

Bit Line
  │
  │
[Cell]─[Cell]─[Cell]─[Cell]
  │      │      │      │
[Cell]─[Cell]─[Cell]─[Cell]
  │      │      │      │
  └──┬───┴───┬──┴───┬──┘
     WL0    WL1   WL2

구조:
- 셀이 직렬 연결 (NAND 구조)
- 페이지 단위 액세스
- 순차적 읽기

특징:
- 높은 밀도
- 작은 셀 크기
- 빠른 쓰기
- 순차 액세스
- 데이터 저장

페이지/블록:
- Page: 2KB-16KB (쓰기 단위)
- Block: 256KB-16MB (소거 단위)
- Plane: 여러 Block
- Die: 여러 Plane
```

### SLC/MLC/TLC/QLC

```
셀 당 비트 수:

SLC (Single Level Cell):
- 1비트/cell
- 2개 상태 (0, 1)
- Vth 분포 2개
- 가장 빠르고 내구성 좋음
- 비쌈

MLC (Multi Level Cell):
- 2비트/cell
- 4개 상태 (00, 01, 10, 11)
- Vth 분포 4개
- 중간 속도/내구성
- 중간 가격

TLC (Triple Level Cell):
- 3비트/cell
- 8개 상태
- Vth 분포 8개
- 느리고 내구성 낮음
- 저렴

QLC (Quad Level Cell):
- 4비트/cell
- 16개 상태
- Vth 분포 16개
- 가장 느림
- 가장 저렴

Vth 분포:
SLC: |      █      |
MLC: |  █  █  █  █  |
TLC: |█ █ █ █ █ █ █ █|
```

### 읽기/쓰기/소거 동작

```
NAND 플래시 동작:

1. Read (페이지 단위):
- Row Address → Block/Page 선택
- Page → Sense Amp
- Data → 출력

2. Write (Program):
- Page가 Erase 상태인지 확인
- Row Address 입력
- Data 입력
- Program pulse 인가
- Verify
- Retry if needed

3. Erase (블록 단위):
- Block Address 입력
- High Voltage 인가
- 모든 Cell의 전하 방출
- Block = 모두 1

타이밍:
t_READ: ~50µs
t_PROG: ~200µs~1ms
t_ERASE: ~1~5ms
```

### 웨어 레벨링

```
Wear Leveling:

문제:
- Block마다 쓰기 횟수 제한 (10만~100만)
- 편중된 쓰기 → 조기 사망

해결:
- 쓰기 균등 분배

Algorithm:
1. Dynamic Wear Leveling:
   - 자주 변경되는 Data 이동
   - Hot Data ↔ Cold Data 교환

2. Static Wear Leveling:
   - 정적 Data도 이동
   - 모든 Block 균등화

구현:
Logical Block → Physical Block Mapping
- LBA 0 → PBA 100
- LBA 1 → PBA 50
- ... (동적 재배치)

효과:
- 수명 2~10배 연장
```

## Ⅲ. 융합 비교

### NOR vs NAND

| 비교 항목 | NOR | NAND |
|----------|-----|------|
| 구조 | 병렬 | 직렬 |
| 액세스 | 임의 | 순차 |
| 읽기 | 매우 빠름 | 빠름 |
| 쓰기 | 느림 | 빠름 |
| 소거 | 느림 | 빠름 |
| 밀도 | 낮음 | 높음 |
| 비용 | 높음 | 낮음 |
| 응용 | 코드 | 데이터 |
| XIP | 가능 | 불가 |

### SLC/MLC/TLC/QLC

| 타입 | 비트/셀 | 쓰기 회수 | 속도 | 내구성 | 비용 |
|------|---------|-----------|------|--------|------|
| SLC | 1 | 100K+ | 빠름 | 높음 | 높음 |
| MLC | 2 | 3K-10K | 중간 | 중간 | 중간 |
| TLC | 3 | 1K-3K | 느림 | 낮음 | 낮음 |
| QLC | 4 | < 1K | 매우 느림 | 매우 낮음 | 매우 낮음 |

### 플래시 응용

| 응용 | 타입 | 용량 | 특징 |
|------|------|------|------|
| USB | NAND | 32GB-1TB | 휴대용 |
| SD Card | NAND | 32GB-1TB | 카메라 |
| eMMC | NAND | 32GB-256GB | 모바일 |
| SSD | NAND | 256GB-4TB | PC 저장 |
| UFS | NAND | 128GB-1TB | 고성능 모바일 |
| Serial Flash | NOR | 1MB-32MB | BIOS |

## Ⅳ. 실무 적용 및 기술사적 판단

### SSD (Solid State Drive)

```
SSD 구조:

Host (PC)
  │
  └→ SSD Controller
        │
        ├── FTL (Flash Translation Layer)
        ├── Wear Leveling
        ├── Error Correction
        └── DRAM Cache
              │
        ┌─────┴─────┐
        │           │
    NAND Die    NAND Die
    (Multi-chip)

FTL 기능:
1. Logical → Physical 매핑
2. Garbage Collection
3. Wear Leveling
4. Bad Block Management

성능:
- 읽기: ~500MB/s ~ 7GB/s (NVMe)
- 쓰기: ~300MB/s ~ 5GB/s
- IOPS: ~10K ~ 1M+
```

### eMMC vs UFS

```
eMMC (embedded MultiMediaCard):
- 인터페이스: Parallel (8-bit)
- 속도: ~400MB/s (eMMC 5.1)
- 구조: CommandQueue X
- 응용: 저가형 스마트폰

UFS (Universal Flash Storage):
- 인터페이스: Serial (MIPI M-PHY)
- 속도: ~2GB/s (UFS 3.1)
- 구조: CommandQueue O
- Full Duplex
- 응용: 고성능 스마트폰

비교:
eMMC: Half Duplex, 느림
UFS: Full Duplex, 빠름
```

### 3D NAND

```
3D V-NAND (Vertical NAND):

구조:
- 2D: 평면 배치
- 3D: 적층 (32~128층)

장점:
- 밀도 급격 증가
- 비용 감소
- 성능 향상

제조 공정:
1. 하층 CMOS 형성
2. 절연층 적층
3. 채널 홀 형성 (Etching)
4. Word Line 형성
5. 상부 연결

특징:
- TLC/QLC + 3D
- 1Tb+ 칩 가능
- SSD 가격 하락
```

### NVMe

```
NVMe (Non-Volatile Memory Express):

개념:
- 플래시 전용 프로토콜
- PCIe 기반
- Low Latency

특징:
1. 여러 Command Queue
   - AHCI: 1 Queue, 32 Command
   - NVMe: 64K Queue, 64K Command

2. 낮은 Latency
   - AHCI: ~50µs
   - NVMe: ~10µs

3. 높은 IOPS
   - AHCI: ~100K
   - NVMe: ~1M+

4. 고대역폭
   - PCIe Gen4: ~8GB/s
   - PCIe Gen5: ~16GB/s
```

## Ⅴ. 기대효과 및 결론

플래시 메모리는 현대 저장의 핵심이다. 비휘발성과 전기적 재기록으로 SSD와 모바일 혁명을 이끌었다.

## 📌 관련 개념 맵

```
플래시 메모리
├── 구조
│   ├── Floating Gate MOSFET
│   ├── Tunnel Oxide
│   └── Control Gate
├── 타입
│   ├── NOR (병렬, 코드)
│   └── NAND (직렬, 데이터)
├── 동작
│   ├── Program (전하 주입)
│   ├── Erase (전하 방출)
│   ├── Read (Vth 감지)
│   └── Block/Page 단위
├── 셀 타입
│   ├── SLC (1비트)
│   ├── MLC (2비트)
│   ├── TLC (3비트)
│   └── QLC (4비트)
└── 응용
    ├── SSD
    ├── USB/SD Card
    ├── eMMC/UFS
    └── BIOS/UEFI
```

## 👶 어린이를 위한 3줄 비유 설명

1. 플래시 메모리는 전기로 지우고 다시 쓸 수 있는 매직 붙어 있은 메모장 같아요. 전기를 끊어도 내용이 안 사라져요
2. USB나 SSD는 이 플래시 메모리로 만들어져요. NOR는 책처럼 페이지를 바로 펼 수 있고(코드), NAND는 필름처럼 순서대로 봐야 해요(데이터)
3. 쓰기 횟수가 제한되어 있어서 컴퓨터가 자주 쓰는 곳과 드물게 쓰는 곳을 바꿔가면서 사용해요(웨어 레벨링)

```python
# 플래시 메모리 시뮬레이션

from typing import List, Dict
import random


class FlashCell:
    """플래시 셀"""

    def __init__(self, cell_type: str = "SLC"):
        self.cell_type = cell_type
        self.threshold = 0.0  # Vth
        self.erase()

    def erase(self):
        """소거 (모두 1)"""
        self.threshold = -1.0  # Erased 상태

    def program(self, data: int) -> bool:
        """프로그래밍"""
        if self.cell_type == "SLC":
            target = 1.0 if data == 0 else -1.0
        elif self.cell_type == "MLC":
            # 00: 2.0, 01: 0.5, 10: -0.5, 11: -2.0
            targets = {0b00: 2.0, 0b01: 0.5, 0b10: -0.5, 0b11: -2.0}
            target = targets.get(data, -2.0)
        else:
            target = 1.0 if data == 0 else -1.0

        self.threshold = target
        return True

    def read(self) -> int:
        """읽기"""
        if self.cell_type == "SLC":
            return 0 if self.threshold > 0 else 1
        elif self.cell_type == "MLC":
            if self.threshold > 1.0:
                return 0b00
            elif self.threshold > 0:
                return 0b01
            elif self.threshold > -1.0:
                return 0b10
            else:
                return 0b11
        return 1


class FlashPage:
    """플래시 페이지"""

    def __init__(self, page_size: int, cell_type: str = "SLC"):
        self.page_size = page_size
        self.cell_type = cell_type
        self.cells = [FlashCell(cell_type) for _ in range(page_size)]
        self.is_erased = True

    def erase(self):
        """페이지 소거"""
        for cell in self.cells:
            cell.erase()
        self.is_erased = True

    def write(self, offset: int, data: List[int]) -> bool:
        """쓰기"""
        if not self.is_erased:
            return False  # 소거 필요

        for i, val in enumerate(data):
            if offset + i < self.page_size:
                self.cells[offset + i].program(val)

        self.is_erased = False
        return True

    def read(self, offset: int, length: int) -> List[int]:
        """읽기"""
        result = []
        for i in range(length):
            if offset + i < self.page_size:
                result.append(self.cells[offset + i].read())
        return result


class FlashBlock:
    """플래시 블록"""

    def __init__(self, num_pages: int, page_size: int, cell_type: str = "SLC"):
        self.num_pages = num_pages
        self.page_size = page_size
        self.cell_type = cell_type
        self.pages = [FlashPage(page_size, cell_type) for _ in range(num_pages)]
        self.erase_count = 0
        self.max_erases = 100000 if cell_type == "SLC" else 3000

    def erase(self):
        """블록 소거"""
        for page in self.pages:
            page.erase()
        self.erase_count += 1

    def is_bad(self) -> bool:
        """불량 블록 확인"""
        return self.erase_count >= self.max_erases

    def write_page(self, page_num: int, data: List[int]) -> bool:
        """페이지 쓰기"""
        if page_num >= self.num_pages:
            return False
        return self.pages[page_num].write(0, data)

    def read_page(self, page_num: int) -> List[int]:
        """페이지 읽기"""
        if page_num >= self.num_pages:
            return []
        return self.pages[page_num].read(0, self.page_size)


class FlashMemory:
    """플래시 메모리"""

    def __init__(self, num_blocks: int, pages_per_block: int, page_size: int,
                 cell_type: str = "SLC"):
        self.num_blocks = num_blocks
        self.pages_per_block = pages_per_block
        self.page_size = page_size
        self.cell_type = cell_type
        self.blocks = [FlashBlock(pages_per_block, page_size, cell_type)
                       for _ in range(num_blocks)]

        # Logical → Physical 매핑
        self.lba_to_pba: Dict[int, int] = {}
        self.pba_to_lba: Dict[int, int] = {}
        self.free_blocks = set(range(num_blocks))

    def write(self, lba: int, data: List[int]) -> bool:
        """쓰기"""
        # 블록 할당
        if lba not in self.lba_to_pba:
            if not self.free_blocks:
                # Garbage Collection 필요
                return False
            pba = self.free_blocks.pop()
            self.lba_to_pba[lba] = pba
            self.pba_to_lba[pba] = lba

        pba = self.lba_to_pba[lba]

        # 블록 소거
        self.blocks[pba].erase()

        # 페이지 쓰기
        page_num = lba % self.pages_per_block
        return self.blocks[pba].write_page(page_num, data)

    def read(self, lba: int) -> List[int]:
        """읽기"""
        if lba not in self.lba_to_pba:
            return []

        pba = self.lba_to_pba[lba]
        page_num = lba % self.pages_per_block
        return self.blocks[pba].read_page(page_num)

    def erase_block(self, pba: int):
        """블록 소거"""
        if pba < len(self.blocks):
            self.blocks[pba].erase()

    def get_stats(self) -> Dict:
        """통계"""
        total_erases = sum(b.erase_count for b in self.blocks)
        bad_blocks = sum(1 for b in self.blocks if b.is_bad())
        return {
            "total_erases": total_erases,
            "bad_blocks": bad_blocks,
            "free_blocks": len(self.free_blocks)
        }


def demonstration():
    """플래시 메모리 데모"""
    print("=" * 60)
    print("플래시 메모리 (Flash Memory) 데모")
    print("=" * 60)

    # SLC vs MLC
    print("\n[SLC vs MLC]")
    slc_cell = FlashCell("SLC")
    mlc_cell = FlashCell("MLC")

    print("SLC:")
    slc_cell.program(0)
    print(f"  Program 0 → Read = {slc_cell.read()}")
    slc_cell.program(1)
    print(f"  Program 1 → Read = {slc_cell.read()}")

    print("\nMLC:")
    mlc_cell.program(0b00)
    print(f"  Program 00 → Read = {mlc_cell.read():02b}")
    mlc_cell.erase()
    mlc_cell.program(0b10)
    print(f"  Program 10 → Read = {mlc_cell.read():02b}")

    # NOR vs NAND 시뮬레이션
    print("\n[NOR vs NAND 액세스]")
    print("NOR: 임의 액세스 가능")
    nor_addrs = [0, 100, 5, 50]
    print(f"  액세스: {nor_addrs} (순서 상관없음)")

    print("\nNAND: 페이지 단위 액세스")
    page_addrs = [0, 1, 2, 3]
    print(f"  액세스: Page {page_addrs} (순차적)")

    # 플래시 메모리
    print("\n[플래시 메모리 시뮬레이션]")
    flash = FlashMemory(num_blocks=16, pages_per_block=4, page_size=8,
                        cell_type="SLC")

    # 쓰기
    print("쓰기:")
    for lba in range(5):
        data = [(lba * 8 + i) % 2 for i in range(8)]
        flash.write(lba, data)
        pba = flash.lba_to_pba.get(lba, -1)
        print(f"  LBA {lba} → PBA {pba}")

    # 읽기
    print("\n읽기:")
    for lba in range(3):
        data = flash.read(lba)
        print(f"  LBA {lba}: {data}")

    # 웨어 레벨링 시뮬레이션
    print("\n[웨어 레벨링 효과]")
    flash2 = FlashMemory(num_blocks=4, pages_per_block=2, page_size=4)

    # 편중된 쓰기 (웨어 레벨링 없음)
    print("편중된 쓰기 (LBA 0만 반복):")
    for _ in range(10):
        flash2.write(0, [1] * 4)

    stats = flash2.get_stats()
    print(f"  Block 0 Erase Count: {flash2.blocks[0].erase_count}")
    print(f"  Block 1 Erase Count: {flash2.blocks[1].erase_count}")

    # 웨어 레벨링
    print("\n웨어 레벨링 (LBA 회전):")
    flash3 = FlashMemory(num_blocks=4, pages_per_block=2, page_size=4)

    for i in range(10):
        lba = i % 4  # LBA 회전
        flash3.write(lba, [1] * 4)

    print("Erase Counts:")
    for i, block in enumerate(flash3.blocks):
        print(f"  Block {i}: {block.erase_count}")

    # SSD 시뮬레이션
    print("\n[SSD 성능]")
    print("Read: ~500MB/s")
    print("Write: ~300MB/s")
    print("IOPS: ~100K")
    print("Latency: ~50µs")

    # 3D NAND
    print("\n[3D NAND]")
    print("2D NAND: 단층, 1Tb/chip")
    print("3D NAND (32층): 32Tb/chip")
    print("3D NAND (128층): 128Tb/chip")
    print("밀도: 32~128배 증가")


if __name__ == "__main__":
    demonstration()
```
