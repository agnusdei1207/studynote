+++
title = "RAM (Random Access Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# RAM (Random Access Memory)

## 핵심 인사이트 (3줄 요약)
1. RAM(Random Access Memory)은 임의 액세스가 가능한 읽기/쓰기 메모리로, SRAM과 DRAM 두 가지 형태가 있으며 전원이 차단되면 데이터가 소실되는 휘발성 메모리이다
2. SRAM은 플립플롭 기반으로 빠르지만 비싸고, DRAM은 캐패시터 기반으로 느리지만 저렴하고 고밀도이다
3. 기술사시험에서는 SRAM/DRAM 구조, 리프레시, 액세스 타이밍, 인터리빙이 핵심이다

## Ⅰ. 개요 (500자 이상)

RAM(Random Access Memory)은 **임의의 주소에 동일한 시간으로 액세스할 수 있는 읽기/쓰기 가능한 메모리**이다. 메인 메모리, 캐시, 레지스터 등 컴퓨터의 거의 모든 데이터 저장 장치가 RAM의 일종이다. 전원이 공급되는 동안만 데이터를 유지하는 휘발성(Volatile) 특성을 가진다.

```
RAM 기본 개념:
구조: 2D 어레이 (Word × Bit)
입력: Address[n-1:0], Din[m-1:0], WE (Write Enable), CS (Chip Select)
출력: Dout[m-1:0]

동작:
- Address로 Word 선택
- WE=0: Read (Dout ← Data)
- WE=1: Write (Data ← Din)
- 임의 액세스 (모든 주소 동일 시간)

특징:
- 휘발성
- 읽기/쓰기 가능
- 빠른 액세스
- 낮은 지연
```

**RAM의 핵심 특징:**

1. **임의 액세스**: 어떤 주소든 동일한 시간으로 액세스
2. **휘발성**: 전원 차단 시 데이터 소실
3. **읽기/쓰기**: 데이터 수정 가능
4. **빠른 속도**: 보조 기기보다 훨씬 빠름

```
RAM vs ROM:
RAM:
- 휘발성
- 읽기/쓰기
- 빠름
- 메인 메모리

ROM:
- 비휘발성
- 읽기 전용
- 중간
- 펌웨어
```

RAM은 SRAM(Static RAM)과 DRAM(Dynamic RAM) 두 가지 주요 형태로 나뉜다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### RAM 기본 구조

```
n×m 비트 RAM 구조:

Address[n-1:0]
│
├──[Address Decoder]── Word Lines[2ⁿ-1:0]
│                  │
│    Cell[0,0] ────┤
│    Cell[0,1] ────┤
│     ...      ────┼──[Sense Amp]── Dout[m-1:0]
│    Cell[m-1,0]───┘      ↑
│                         │
Din[m-1:0] ─────────[Write Driver]
│                  ↑
│                 WE
│                 ↑
│                CS

구성 요소:
1. Address Decoder: 주소 디코딩
2. Cell Array: 데이터 저장
3. Sense Amp: 읽기 데이터 증폭
4. Write Driver: 쓰기 데이터 구동
5. Control: CS, WE 제어

동작:
Read: CS=1, WE=0 → Dout = Memory[Address]
Write: CS=1, WE=1 → Memory[Address] = Din
```

### SRAM (Static RAM)

```
SRAM 셀 구조 (6T):

   VDD VDD
    │   │
   PM PM
   │   │
┌──┴┐ ┌┴──┐
│ Q │ │Q' │
└┬─┘ └┬─┘
  │   │
  NM NM
  │   │
  └─┬─┘
    │
   GND

WL (Word Line)
│
BL (Bit Line)
│
BL' (Bit Line')

구조:
- 2개 인버터 (4개 TR)
- 2개 액세스 TR
- 총 6개 TR

동작:
- Idle: WL=0, 양쪽 비트라인 Precharge
- Read: WL=1, BL/BL'로 상태 감지
- Write: WL=1, BL/BL'로 데이터 강제

특징:
- 안정적 (리프레시 불필요)
- 빠름 (< 10ns)
- 비싸고 큼
- 캐시 메모리
```

### DRAM (Dynamic RAM)

```
DRAM 셀 구조 (1T-1C):

   VDD
    │
    └───[Capacitor]──┐
                     │
   WL               TR
    │               │
    └───┬──[TR]─┬───┘
        │       │
       BL     GND

구조:
- 1개 트랜지스터
- 1개 캐패시터

동작:
- Idle: TR off, Capacitor 유지
- Read: WL=1, TR on, Charge 감지
- Write: WL=1, TR on, Charge 충전/방전

문제:
- 누설 전류 (Leakage)
- 전하 방출
- 주기적 리프레시 필요

리프레시:
- 주기: 64ms (JEDEC)
- 행 단위 리프레시
- 8192 행 → 8192/64ms = 7.8µs 간격
```

### 액세스 타이밍

```
SRAM 액세스 타이밍:

Read:
Address ───┐           ┌─────┐
           │Valid      │     │Valid
CS ────────┴─────┬─────┘     └─────
WE ─────────────┴─────────────── (Read Mode)
                  ↑
              t_acc (액세스 시간)

Dout ─────────────────┐       ┌──
                      │Valid  │
                      └───────┘
                      ↑
                   t_acc

Write:
Address ───┐           ┌─────┐
           │Valid      │     │Valid
Din ───────┴─────────┬─┴─────┴──
                    │Valid
CS ──────────────────┴──────┬──
WE ────────────────┬────────┴──
                   ↑   ↑
                 t_su t_h
(Setup/Hold time)
```

### DRAM 리프레시

```
DRAM 리프레시 방식:

1. RAS-Only Refresh:
RAS ──┐   ┌───┐   ┌───┐
      └───┘   └───┘
CAS ────────────────────── (High)
Row Address ──┬───┬───┬───
              │   │   │
            Refresh Row

2. CAS-Before-RAS (CBR):
CAS ───┐       ┌───┐
        └───────┘
RAS ─────┐   ┌───┐   ┌───┐
         └───┘   └───┘
         ↑
    Auto Refresh

3. Hidden Refresh:
Normal 액세스 사이에 리프resh

리프레시 주기:
t_refresh = 64ms (JEDEC)
행 수 = 8192 (8K)
리프레시 간격 = 64ms / 8192 = 7.8µs
```

### 메모리 인터리빙

```
인터리빙 (Interleaving):

목적:
- 액세스 시간 감축
- 대역폭 향상

2-way 인터리빙:
Address[0] = 0 → Bank 0
Address[0] = 1 → Bank 1

Sequence:
0 → Bank 0
1 → Bank 1
2 → Bank 0
3 → Bank 1

장점:
- Bank 0 액세스 중 Bank 1 Precharge
- 병렬 동작 가능

4-way 인터리빙:
Address[1:0]
00 → Bank 0
01 → Bank 1
10 → Bank 2
11 → Bank 3
```

### 버스트 모드

```
Burst Mode:

개념:
- 한 번 액세스로 연속 데이터 전송
- Precharge/RAS 생략

예: Burst Length = 4
Address: 0, 1, 2, 3

Normal:
0: RAS + CAS + Data
1: Precharge + RAS + CAS + Data
2: ...
3: ...
Total: 4 × (RAS + CAS + Data)

Burst:
0: RAS + CAS + Data[0]
   Data[1] (RAS/CAS 생략)
   Data[2]
   Data[3]
Total: RAS + CAS + 4 × Data

이득: ~50% 시간 절약
```

## Ⅲ. 융합 비교

### SRAM vs DRAM

| 비교 항목 | SRAM | DRAM |
|----------|------|------|
| 셀 구조 | 6T | 1T-1C |
| 비트 당 TR | 6 | 1 |
| 속도 | < 10ns | 50-100ns |
| 리프레시 | 불필요 | 필수 (64ms) |
| 밀도 | 낮음 | 높음 |
| 비용 | 높음 | 낮음 |
| 전력 | 낮음 (Idle) | 높음 (리프레시) |
| 응용 | 캐시 | 메인 메모리 |

### RAM 타입

| 타입 | 기술 | 속도 | 전력 | 응용 |
|------|------|------|------|------|
| SRAM | 6T | 가장 빠름 | 낮음 | L1/L2 캐시 |
| DRAM | 1T-1C | 빠름 | 중간 | 메인 메모리 |
| SDRAM | Sync DRAM | 중간 | 중간 | PC 메모리 |
| DDR | Double Data Rate | 빠름 | 중간 | 고성능 PC |
| LPDDR | Low Power DRAM | 중간 | 낮음 | 모바일 |

### 메모리 계층

| 계층 | 기술 | 용량 | 속도 | 비용 |
|------|------|------|------|------|
| L1 캐시 | SRAM | 32-64KB | < 1ns | 매우 높음 |
| L2 캐시 | SRAM | 256KB-8MB | 3-10ns | 높음 |
| L3 캐시 | SRAM/DRAM | 8-64MB | 10-20ns | 중간 |
| 메인 메모리 | DRAM | 4-64GB | 50-100ns | 낮음 |
| SSD | NAND Flash | 256GB-4TB | 100µs | 매우 낮음 |

## Ⅳ. 실무 적용 및 기술사적 판단

### DDR SDRAM

```
DDR (Double Data Rate) SDRAM:

개념:
- 클럭의 상승/하강 에지 모두 전송
- 2배 데이터 전송률

타이밍:
Clk ──┬───┬───┬───┬───
      ↑   ↑   ↑   ↑
      └─┬─┘   └─┬─┘
    Rising  Falling

Data ─┬─┬─┬─┬─┬─┬─┬─┬─
      │ │ │ │ │ │ │ │
      D0 D1 D2 D3 D4 D5 D6 D7

전송률:
- Clk = 100MHz
- DDR = 200MT/s (Mega Transfers/sec)
- 64비트 버스 → 1.6GB/s

DDR 세대:
DDR: 2.5V, 200-400MT/s
DDR2: 1.8V, 400-1066MT/s
DDR3: 1.5V, 800-2133MT/s
DDR4: 1.2V, 2133-3200MT/s
DDR5: 1.1V, 4800-6400MT/s
```

### 메모리 컨트롤러

```
메모리 컨트롤러:

기능:
1. 주소 변환 (CPU → Physical → DRAM)
2. 타이밍 제어 (RAS, CAS, WE)
3. 리프레시 관리
4. 에러 정정 (ECC)
5. 뱅크 관리

구조:
CPU ──→ Memory Controller ──→ DRAM
       │
       ├── Scheduler (명령 큐)
       ├── Timer (리프레시)
       └── ECC (에러 정정)

타이밍 파라미터:
tRCD: RAS→CAS 지연
tRP: Row Precharge 시간
tRAS: Row Active 시간
CL: CAS Latency
```

### 캐시 메모리

```
SRAM 캐시 구조:

L1 Cache:
- 32-64KB per Core
- SRAM 기반
- 4-8 way associative
- < 1ns 액세스

L2 Cache:
- 256KB-8MB
- SRAM 기반
- 8-16 way
- 3-10ns 액세스

L3 Cache:
- 8-64MB (Shared)
- SRAM/DRAM
- 16-64 way
- 10-20ns 액세스

태그 구조:
┌────────┬────────┬───────┐
│ Valid  │ Tag    │ Data  │
├────────┼────────┼───────┤
│ 1비트  │ 20비트  │ 32비트│
└────────┴────────┴───────┘
```

### 메모리 대역폭

```
대역폭 계산:

BW = Frequency × Bus Width × Data Rate

예: DDR4-3200
Frequency = 1600MHz (Clk)
Bus Width = 64비트 = 8바이트
Data Rate = 2 (DDR)

BW = 1600MHz × 8B × 2 = 25.6GB/s

Dual Channel:
BW = 25.6GB/s × 2 = 51.2GB/s

특징:
- 듀얼 채널: 2× 대역폭
- 쿼드 채널: 4× 대역폭
- 인터리빙: 순차 액세스 최적화
```

## Ⅴ. 기대효과 및 결론

RAM은 컴퓨터의 작업 공간이다. SRAM은 캐시로, DRAM은 메인 메모리로 사용된다.

## 📌 관련 개념 맵

```
RAM
├── 타입
│   ├── SRAM (Static)
│   │   ├── 6T 셀
│   │   ├── 빠름
│   │   ├── 비쌈
│   │   └── 캐시
│   └── DRAM (Dynamic)
│       ├── 1T-1C 셀
│       ├── 느림
│       ├── 쌈
│       ├── 리프레시 필요
│       └── 메인 메모리
├── 특징
│   ├── 휘발성
│   ├── 임의 액세스
│   └── 읽기/쓰기
└── 응용
    ├── 캐시 메모리
    ├── 메인 메모리
    ├── 비디오 메모리
    └── 버퍼
```

## 👶 어린이를 위한 3줄 비유 설명

1. RAM은 메모장 같아요. 적어두면 전원이 켜져 있는 동안에는 내용이 남아있지만, 전원을 끄면 다 사라져요
2. SRAM은 비싸지만 빠른 고급 메모장이고, DRAM은 싸지만 조금 느린 일반 메모장이에요
3. SRAM은 CPU 바로 옆에 작게 두어서 자주 쓰는 것을 빠르게 꺼내 쓰고(캐시), DRAM은 크게 많이 두어서 모든 데이터를 저장해요(메인 메모리)

```python
# RAM 시뮬레이션

from typing import List


class RAM:
    """기본 RAM 시뮬레이션"""

    def __init__(self, size: int, word_size: int = 8):
        """
        RAM 초기화

        Args:
            size: 워드 수
            word_size: 워드 비트 수
        """
        self.size = size
        self.word_size = word_size
        self.data = [0] * size

    def read(self, address: int) -> int:
        """읽기"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")
        return self.data[address]

    def write(self, address: int, data: int):
        """쓰기"""
        if not (0 <= address < self.size):
            raise ValueError(f"주소 범위 초과: {address}")
        self.data[address] = data & ((1 << self.word_size) - 1)

    def __str__(self):
        result = f"RAM ({self.size}x{self.word_size}):\n"
        for i in range(0, self.size, 16):
            if i < self.size:
                row = []
                for j in range(16):
                    if i + j < self.size:
                        row.append(f"{self.data[i+j]:02X}")
                    else:
                        row.append("  ")
                result += f"  {i:04X}: " + " ".join(row) + "\n"
        return result


class SRAM(RAM):
    """SRAM (Static RAM)"""

    def __init__(self, size: int, word_size: int = 8, access_time: float = 1.0):
        super().__init__(size, word_size)
        self.access_time = access_time
        self.read_count = 0
        self.write_count = 0

    def read(self, address: int) -> int:
        self.read_count += 1
        return super().read(address)

    def write(self, address: int, data: int):
        self.write_count += 1
        super().write(address, data)

    def stats(self):
        """통계"""
        return {"reads": self.read_count, "writes": self.write_count}


class DRAM(RAM):
    """DRAM (Dynamic RAM)"""

    def __init__(self, size: int, word_size: int = 8, access_time: float = 5.0,
                 refresh_interval: int = 100):
        super().__init__(size, word_size)
        self.access_time = access_time
        self.refresh_interval = refresh_interval
        self.access_count = 0
        self.refresh_count = 0

    def read(self, address: int) -> int:
        self.access_count += 1

        # 리프레시 체크
        if self.access_count % self.refresh_interval == 0:
            self._refresh()

        return super().read(address)

    def write(self, address: int, data: int):
        self.access_count += 1

        if self.access_count % self.refresh_interval == 0:
            self._refresh()

        super().write(address, data)

    def _refresh(self):
        """리프레시"""
        self.refresh_count += 1
        # 실제 DRAM은 전하 보충

    def stats(self):
        return {"accesses": self.access_count, "refreshes": self.refresh_count}


class CacheMemory:
    """캐시 메모리 (SRAM 기반)"""

    def __init__(self, size: int, line_size: int = 4, ways: int = 4):
        self.size = size
        self.line_size = line_size
        self.ways = ways
        self.sets = size // (line_size * ways)

        # 캐시: [sets][ways]
        self.tags = [[None for _ in range(ways)] for _ in range(self.sets)]
        self.valid = [[False for _ in range(ways)] for _ in range(self.sets)]
        self.data = [[None for _ in range(ways)] for _ in range(self.sets)]
        self.lru = [[0 for _ in range(ways)] for _ in range(self.sets)]

        self.hits = 0
        self.misses = 0

    def _get_set(self, address: int) -> int:
        return (address // self.line_size) % self.sets

    def _get_tag(self, address: int) -> int:
        return address // (self.line_size * self.sets)

    def _update_lru(self, set_idx: int, way_idx: int):
        for i in range(self.ways):
            if self.lru[set_idx][i] < self.lru[set_idx][way_idx]:
                self.lru[set_idx][i] += 1
        self.lru[set_idx][way_idx] = 0

    def read(self, address: int, main_memory: RAM) -> int:
        set_idx = self._get_set(address)
        tag = self._get_tag(address)

        # 태그 검색
        for way in range(self.ways):
            if self.valid[set_idx][way] and self.tags[set_idx][way] == tag:
                # Cache Hit
                self.hits += 1
                self._update_lru(set_idx, way)
                return self.data[set_idx][way]

        # Cache Miss
        self.misses += 1

        # LRU way 선택
        lru_way = 0
        for way in range(1, self.ways):
            if self.lru[set_idx][way] > self.lru[set_idx][lru_way]:
                lru_way = way

        # 메모리에서 로드
        data = main_memory.read(address)
        self.tags[set_idx][lru_way] = tag
        self.valid[set_idx][lru_way] = True
        self.data[set_idx][lru_way] = data
        self._update_lru(set_idx, lru_way)

        return data

    def hit_rate(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total


class InterleavedMemory:
    """인터리빙 메모리"""

    def __init__(self, num_banks: int, bank_size: int):
        self.num_banks = num_banks
        self.banks = [RAM(bank_size) for _ in range(num_banks)]

    def _get_bank(self, address: int) -> int:
        return address % self.num_banks

    def _get_bank_addr(self, address: int) -> int:
        return address // self.num_banks

    def read(self, address: int) -> int:
        bank = self._get_bank(address)
        bank_addr = self._get_bank_addr(address)
        return self.banks[bank].read(bank_addr)

    def write(self, address: int, data: int):
        bank = self._get_bank(address)
        bank_addr = self._get_bank_addr(address)
        self.banks[bank].write(bank_addr, data)


def demonstration():
    """RAM 데모"""
    print("=" * 60)
    print("RAM (Random Access Memory) 데모")
    print("=" * 60)

    # 기본 RAM
    print("\n[기본 RAM]")
    ram = RAM(size=256, word_size=8)

    # 쓰기
    print("쓰기:")
    for i in range(0, 16):
        ram.write(i, i * 0x11)
    print(f"  주소 0-15에 데이터 쓰기 완료")

    # 읽기
    print("\n읽기:")
    for i in [0, 5, 10, 15]:
        print(f"  주소 {i:2d}: 0x{ram.read(i):02X}")

    # SRAM
    print("\n[SRAM]")
    sram = SRAM(size=16, word_size=8, access_time=1.0)

    # 연산 시뮬레이션
    print("연산 시뮬레이션:")
    sram.write(0, 10)  # A = 10
    sram.write(1, 20)  # B = 20

    a = sram.read(0)
    b = sram.read(1)
    sram.write(2, a + b)  # C = A + B

    print(f"  A = {a}, B = {b}")
    print(f"  C = A + B = {sram.read(2)}")
    print(f"\n  통계: {sram.stats()}")

    # DRAM
    print("\n[DRAM]")
    dram = DRAM(size=16, word_size=8, access_time=5.0, refresh_interval=5)

    print("연산 시뮬레이션 (리프레시 포함):")
    dram.write(0, 30)
    dram.write(1, 40)

    c = dram.read(0)
    d = dram.read(1)
    dram.write(2, c + d)

    print(f"  C = {c}, D = {d}")
    print(f"  E = C + D = {dram.read(2)}")
    print(f"\n  통계: {dram.stats()}")

    # 캐시
    print("\n[캐시 메모리]")
    main_mem = RAM(size=1024, word_size=8)
    cache = CacheMemory(size=64, line_size=4, ways=4)

    # 메인 메모리 초기화
    for i in range(256):
        main_mem.write(i, i)

    # 시퀀셜 액세스 (좋은 지역성)
    print("시퀀셜 액세스 (지역성 좋음):")
    for i in range(32):
        cache.read(i, main_mem)

    hit_rate = cache.hit_rate()
    print(f"  Hit Rate: {hit_rate:.1%}")
    print(f"  Hits: {cache.hits}, Misses: {cache.misses}")

    # 랜덤 액세스 (나쁜 지역성)
    cache2 = CacheMemory(size=64, line_size=4, ways=4)
    print("\n랜덤 액세스 (지역성 나쁨):")
    import random
    random.seed(42)
    for _ in range(32):
        addr = random.randint(0, 100)
        cache2.read(addr, main_mem)

    hit_rate2 = cache2.hit_rate()
    print(f"  Hit Rate: {hit_rate2:.1%}")
    print(f"  Hits: {cache2.hits}, Misses: {cache2.misses}")

    # 인터리빙
    print("\n[인터리빙 메모리]")
    inter_mem = InterleavedMemory(num_banks=4, bank_size=16)

    # 연속 주소 쓰기
    print("연속 주소 쓰기 (4-way 인터리빙):")
    for i in range(16):
        inter_mem.write(i, i * 0x10)
        bank = inter_mem._get_bank(i)
        print(f"  주소 {i:2d} → Bank {bank}, Data = 0x{i * 0x10:02X}")

    print("\n연속 주소 읽기:")
    for i in range(8):
        data = inter_mem.read(i)
        bank = inter_mem._get_bank(i)
        print(f"  주소 {i:2d} ← Bank {bank}, Data = 0x{data:02X}")


if __name__ == "__main__":
    demonstration()
```
