+++
title = "SRAM (Static Random Access Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# SRAM (Static Random Access Memory)

## 핵심 인사이트 (3줄 요약)
1. SRAM(Static RAM)은 6개 트랜지스터(6T)로 구성된 플립플롭 기반 메모리 셀로, 리프레시 없이 안정적으로 데이터를 유지하는 가장 빠른 RAM이다
2. 2개의 인버터가 래치를 형성하고 2개의 액세스 트랜지스터가 비트라인 연결을 제어하며, 캐시 메모리(L1/L2/L3)에 주로 사용된다
3. 기술사시험에서는 6T 셀 구조, 읽기/쓰기 동작, Sense Amp, Precharge가 핵심이다

## Ⅰ. 개요 (500자 이상)

SRAM(Static Random Access Memory)은 **플립플롭 기반의 정적 랜덤 액세스 메모리로, 리프레시 없이 전원이 공급되는 한 데이터를 안정적으로 유지하는 고속 메모리**이다. 6개의 MOSFET(6T)으로 구성된 셀이 기본 단위이며, DRAM에 비해 빠르지만 비트 당 면적이 크고 비싸다.

```
SRAM 기본 개념:
구조: 6T (6 Transistor) 셀
- 2개 PMOS + 2개 NMOS = 2개 인버터 (래치)
- 2개 NMOS = 액세스 트랜지스터

동작:
- Idle: 양 비트라인 Precharge (VDD/2)
- Read: WL 활성화, 비트라인 전압 차 감지
- Write: WL 활성화, 비트라인으로 데이터 강제

특징:
- 비휘발성 아님 (전원 필요)
- 리프레시 불필요 (Static)
- 매우 빠름 (< 10ns)
- 비쌈 (6TR/cell)
- 캐시 메모리
```

**SRAM의 핵심 특징:**

1. **정적 유지**: 리프레시 불필요, 플립플롭으로 유지
2. **고속 액세스**: 캐시 메모리 수준의 빠른 속도
3. **낮은 지연**: Sense Amp로 빠른 감지
4. **큰 면적**: 6T로 인해 DRAM보다 6배 큼

```
SRAM vs DRAM:
SRAM (6T):
- 빠름 (< 10ns)
- 리프레시 불필요
- 비쌈, 큼
- 캐시

DRAM (1T-1C):
- 느림 (50-100ns)
- 리프레시 필요 (64ms)
- 쌈, 작음
- 메인 메모리
```

SRAM은 CPU 내부 캐시, 레지스터 파일, 고성능 버퍼 등에 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 6T SRAM 셀 구조

```
6T SRAM 셀:

         VDD
          │
       ┌──┴──┐
    ┌──┤ PM2 ├──┐
    │  └─┬─┘  │
    │    │    │
    │  ┌─┴─┐  │
┌───┬─┤ NM2├──┼───── Q'
│   │  └─┬─┘  │
│   │    │    │
│   │  ┌─┴─┐  │
│   └──┤ PM1├──┼───── Q
│      └─┬─┘  │
│        │    │
│      ┌─┴─┐  │
└──────┤ NM1├──┘
       └─┬─┘
         │
        GND

액세스 TR:
WL ─┬──[NM3]─── Q ──┬─ BL
    │               │
    └──[NM4]─── Q' ─┴─ BL'

구성:
- PM1, NM1: 인버터 1 (Q 출력)
- PM2, NM2: 인버터 2 (Q' 출력)
- NM3: Q 액세스 TR
- NM4: Q' 액세스 TR
```

### SRAM 읽기 동작

```
SRAM Read 동작:

1. Precharge 단계:
BL, BL' ──┐
          │ VDD/2로 Precharge
          └──[PMOS]── VDD

2. Word Line 활성화:
WL ──┐   ┌──
     └───┘
      ↑
    활성화

3. 비트라인 감지:
Q=0, Q'=1 (가정):
BL ──→ VDD/2 ↓ (방전)
BL'─→ VDD/2 ↑ (유지)

4. Sense Amp:
BL/BL' 차 증폭 → Data Out

타이밍:
t_precharge: ~1ns
t_access: ~3-5ns
Total: ~5ns
```

### SRAM 쓰기 동작

```
SRAM Write 동작:

1. Write Driver 준비:
Din = 0 (가정)
BL ──→ 0
BL'─→ VDD (강제)

2. Word Line 활성화:
WL ──┐   ┌──
     └───┘

3. 데이터 강제:
BL=0, BL'=VDD
↓
Cell 내부 래치 강제翻转
Q ← 0, Q' ← 1

4. Word Line 비활성화:
WL=0 → Cell 안정화

타이밍:
t_setup: ~1ns
t_write: ~3ns
Total: ~5ns
```

### Sense Amplifier

```
Sense Amplifier 구조:

BL ───┐
      │
      ├──[PMOS]──┬── Output
      │    ↑     │
BL'───┤    │     │
      │  [Bias]  │
      └──[PMOS]──┘

동형 Sense Amp:
VDD
 │
PM ─┬── BL
PM ─┬── BL'
 │   │
 NM  NM
  │   │
  └─┬─┘
    │
  [Bias]

특징:
- 차동 증폭
- 빠른 감지 (< 1ns)
- 낮은 전력
- 작은 면적
```

### Precharge 회로

```
Precharge 회로:

BL ──┬──[PM]── VDD
     │     ↑
     │  EQ (Equalize)
BL'──┴──[PM]── VDD

EQ=1: BL, BL' 모두 VDD로
EQ=0: High-Z

동작:
Read/Write 전 Precharge
BL=BL'=VDD
→ 빠른 안정화
→ 신뢰성 향상
```

### SRAM 어레이 구조

```
SRAM 어레이:

WL[0] ──┬─[Cell]─[Cell]─[Cell]─...
WL[1] ──┼─[Cell]─[Cell]─[Cell]─...
WL[2] ──┼─[Cell]─[Cell]─[Cell]─...
  ...   │
        │
       BL[0]  BL[1]  BL[2] ...
       [SA]   [SA]   [SA]
         ↓     ↓     ↓
       D[0]   D[1]   D[2]

구조:
- 2D 어레이 (행 × 열)
- Row Decoder로 WL 선택
- Column MUX로 BL 선택
- Sense Amp로 데이터 감지
```

### 액세스 타이밍

```
SRAM Read Timing:

Address ─┐          ┌─────┐
         │Valid    │     │Valid
CS ──────┴─────┬───┴─────┴─────
WE ─────────────┴────────────── (Read Mode)
             ↑
         t_rc (Read Cycle)

Dout ─────────────────┐       ┌──
                      │Valid  │
                      └───────┘
                      ↑
                   t_aa (Address Access)

SRAM Write Timing:

Address ─┐          ┌─────┐
         │Valid    │     │Valid
Din ─────┴──────────┴──────┴──
         │         │Valid
CS ──────┴─────────┴──────┬──
WE ────────┬──────────────┴──
           ↑      ↑
         t_su    t_h
(Setup/Hold)
```

## Ⅲ. 융합 비교

### SRAM 셀 구조

| 타입 | TR 수 | 구조 | 속도 | 전력 | 응용 |
|------|-------|------|------|------|------|
| 6T | 6 | 2 인버터 + 2 액세스 | 빠름 | 중간 | 캐시 |
| 4T | 4 | 2 인버터 + VDD/GND | 빠름 | 높음 | 레지스터 |
| 8T | 8 | 6T + 2 Read Port | 매우 빠름 | 높음 | multi-port |
| 10T | 10 | 8T + 2 Write Port | 매우 빠름 | 높음 | RF |

### SRAM vs DRAM

| 비교 항목 | SRAM | DRAM |
|----------|------|------|
| 셀 | 6T | 1T-1C |
| 비트 당 TR | 6 | 1 |
| 면적 (f²) | ~120 | ~20 |
| 속도 | 1-10ns | 50-100ns |
| 리프레시 | 불필요 | 필요 (64ms) |
| 전력 | 낮음 (Idle) | 높음 (Refresh) |
| 비용 | 높음 | 낮음 |
| 응용 | 캐시 | 메인 메모리 |

### SRAM 응용

| 응용 | 용량 | 속도 | 구조 |
|------|------|------|------|
| L1 캐시 | 32-64KB | < 1ns | 6T, Direct Map |
| L2 캐시 | 256KB-8MB | 3-10ns | 6T, Set Assoc |
| L3 캐시 | 8-64MB | 10-20ns | 6T/DRAM, Shared |
| Register File | 128-1KB | < 1ns | 6T, Multi-port |
| TLB | 4-8KB | < 1ns | 6T, CAM |

## Ⅳ. 실무 적용 및 기술사적 판단

### L1 캐시 SRAM

```
L1 Instruction Cache:

구조:
- 32KB per Core
- 64B Line Size
- 4-way Set Associative
- 512 Sets

Tag Array:
[Valid][Tag][Data]

구현:
- 6T SRAM 셀
- Physical Tag + Virtual Index
- Virtually Physically Tagged

타이밍:
- Hit: < 1 클럭
- Miss: ~10 클럭 (L2)

성능:
- Hit Rate: ~95%
- Bandwidth: ~64B/cycle
```

### 레지스터 파일 SRAM

```
MIPS 레지스터 파일:

구조:
- 32×32비트
- 2 Read Port, 1 Write Port
- 6T Multi-port SRAM

구현:
Read Port 1:
Addr[4:0] → Decoder → Reg[Addr] → RD1

Read Port 2:
Addr[4:0] → Decoder → Reg[Addr] → RD2

Write Port:
Addr[4:0] → Decoder → WE[Addr]
WD[31:0] → Reg[Addr] @ Clk↑

특징:
- 1 클럭 읽기 (조합)
- 1 클럭 쓰기 (동기)
- $0는 하드웨어로 0
```

### CAM (Content Addressable Memory)

```
CAM SRAM:

구조:
Cell[0]: [Search][Mask][Store]
Cell[1]: [Search][Mask][Store]
...

동작:
1. Search Data 입력
2. 모든 Cell에 병렬 비교
3. Match Line 활성화
4. Match Address 출력

응용:
- TLB (Translation Lookaside Buffer)
- TCAM (Ternary CAM for Routing)
- Cache Tag Compare

구현:
- 10T SRAM + Compare Logic
- XOR 기반 매칭
- Priority Encoder
```

### Low Power SRAM

```
전력 절감 기술:

1. Supply Scaling:
VDD ↓ → Power ↓²
단점: Speed ↓

2. Clock Gating:
Idle Bank에 Clk 차단

3. Word Line Pulsing:
WL 활성화 시간 최소화

4. Bit Line Segmentation:
긴 BL 분리 → Capacitance ↓

5. Sleep Mode:
유휴 시 VDD ↓

DVS (Dynamic Voltage Scaling):
활성: VDD = 1.0V
Idle: VDD = 0.6V
Sleep: VDD = 0.3V
```

## Ⅴ. 기대효과 및 결론

SRAM은 고속 캐시의 핵심이다. 6T 플립플롭 구조로 안정적이고 빠른 액세스를 제공한다.

## 📌 관련 개념 맵

```
SRAM
├── 구조
│   ├── 6T Cell (기본)
│   │   ├── 2 인버터 (래치)
│   │   └── 2 액세스 TR
│   ├── Sense Amplifier
│   ├── Precharge 회로
│   └── Word/Bit Line
├── 동작
│   ├── Read (WL 활성화 → 감지)
│   ├── Write (WL 활성화 → 강제)
│   └── Standby (유지)
├── 특징
│   ├── 빠름 (< 10ns)
│   ├── 리프레시 불필요
│   ├── 비쌈
│   └── 큰 면적
└── 응용
    ├── L1/L2/L3 캐시
    ├── 레지스터 파일
    ├── TLB
    └── 버퍼
```

## 👶 어린이를 위한 3줄 비유 설명

1. SRAM은 전구 스위치 같아요. 스위치를 켜야 불이 켜지고, 꺼도 전원이 있으면 계속 켜져 있어요 (상태 유지)
2. 6개의 트랜지스터가 서로 물려서 상태를 유지해요. 두 개가 서로를 지지해서 안정적이에요 (래치)
3. CPU 안에 아주 작게 만들어서 자주 쓰는 데이터를 빠르게 꺼내 쓰는 보관함이에요 (L1 캐시)

```python
# SRAM 시뮬레이션

from typing import List, Tuple


class SRAMCell:
    """6T SRAM 셀 시뮬레이션"""

    def __init__(self):
        self.q = 0
        self.q_prime = 1
        self.word_line = 0
        self.bit_line = 0
        self.bit_line_prime = 0

    def activate_wl(self):
        """워드라인 활성화"""
        self.word_line = 1

    def deactivate_wl(self):
        """워드라인 비활성화"""
        self.word_line = 0

    def precharge(self):
        """프리차지 (BL=BL'=VDD/2)"""
        self.bit_line = 0.5
        self.bit_line_prime = 0.5

    def read(self) -> int:
        """읽기"""
        self.precharge()
        self.activate_wl()

        # 비트라인 감지 (간소화)
        if self.q == 0:
            self.bit_line = 0.0  # 방전
        else:
            self.bit_line = 1.0

        if self.q_prime == 0:
            self.bit_line_prime = 0.0
        else:
            self.bit_line_prime = 1.0

        # Sense Amp
        data = 1 if self.bit_line > self.bit_line_prime else 0

        self.deactivate_wl()
        return data

    def write(self, data: int):
        """쓰기"""
        # 비트라인 구동
        self.bit_line = data
        self.bit_line_prime = 1 - data

        # WL 활성화
        self.activate_wl()

        # 셀 상태 강제
        self.q = data
        self.q_prime = 1 - data

        self.deactivate_wl()

    def get_state(self) -> Tuple[int, int]:
        return self.q, self.q_prime


class SRAM:
    """SRAM 어레이"""

    def __init__(self, rows: int, cols: int):
        """
        SRAM 어레이

        Args:
            rows: 워드라인 수 (행)
            cols: 비트라인 수 (열)
        """
        self.rows = rows
        self.cols = cols
        self.cells = [[SRAMCell() for _ in range(cols)] for _ in range(rows)]
        self.access_count = 0

    def read(self, row: int, col: int) -> int:
        """읽기"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(f"주소 범위 초과: ({row}, {col})")
        self.access_count += 1
        return self.cells[row][col].read()

    def write(self, row: int, col: int, data: int):
        """쓰기"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise ValueError(f"주소 범위 초과: ({row}, {col})")
        self.access_count += 1
        self.cells[row][col].write(data)

    def read_word(self, row: int) -> List[int]:
        """워드 읽기 (전체 행)"""
        return [self.read(row, col) for col in range(self.cols)]

    def write_word(self, row: int, data: List[int]):
        """워드 쓰기 (전체 행)"""
        for col, val in enumerate(data):
            self.write(row, col, val)


class CacheMemorySRAM:
    """SRAM 기반 캐시"""

    def __init__(self, size: int, line_size: int, ways: int):
        self.size = size
        self.line_size = line_size
        self.ways = ways
        self.sets = size // (line_size * ways)

        # SRAM 어레이
        self.tag_sram = SRAM(self.sets, ways)
        self.valid_sram = SRAM(self.sets, ways)
        self.data_sram = SRAM(size, 8)

        self.hits = 0
        self.misses = 0

    def _get_set(self, address: int) -> int:
        return (address // self.line_size) % self.sets

    def _get_tag(self, address: int) -> int:
        return address // (self.line_size * self.sets)

    def read(self, address: int, main_mem: 'Memory') -> int:
        set_idx = self._get_set(address)
        tag = self._get_tag(address)

        # 태그 비교
        for way in range(self.ways):
            if self.valid_sram.read(set_idx, way) and \
               self.tag_sram.read(set_idx, way) == tag:
                self.hits += 1
                return self.data_sram.read(address, 0)

        self.misses += 1
        data = main_mem.read(address)
        self.data_sram.write(address, 0, data)

        return data

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class Memory:
    """메인 메모리 시뮬레이션"""

    def __init__(self, size: int):
        self.data = list(range(size))

    def read(self, address: int) -> int:
        if 0 <= address < len(self.data):
            return self.data[address]
        return 0


def demonstration():
    """SRAM 데모"""
    print("=" * 60)
    print("SRAM (Static RAM) 데모")
    print("=" * 60)

    # SRAM 셀
    print("\n[SRAM 셀]")
    cell = SRAMCell()

    print("쓰기:")
    cell.write(1)
    print(f"  Q = {cell.q}, Q' = {cell.q_prime}")

    print("\n읽기:")
    data = cell.read()
    print(f"  Data = {data}")

    # SRAM 어레이
    print("\n[SRAM 어레이]")
    sram = SRAM(rows=4, cols=8)

    # 쓰기
    print("쓰기:")
    for row in range(4):
        for col in range(8):
            sram.write(row, col, row * 8 + col)

    print("\n읽기:")
    for row in range(4):
        word = sram.read_word(row)
        print(f"  Row {row}: {word}")

    # 캐시 시뮬레이션
    print("\n[SRAM 캐시]")
    main_mem = Memory(size=1024)
    cache = CacheMemorySRAM(size=256, line_size=4, ways=4)

    # 시퀀셜 액세스
    print("시퀀셜 액세스:")
    for i in range(64):
        cache.read(i, main_mem)

    print(f"  Hit Rate: {cache.hit_rate():.1%}")
    print(f"  Hits: {cache.hits}, Misses: {cache.misses}")

    # 랜덤 액세스
    cache2 = CacheMemorySRAM(size=256, line_size=4, ways=4)
    print("\n랜덤 액세스:")
    import random
    random.seed(42)
    for _ in range(64):
        addr = random.randint(0, 200)
        cache2.read(addr, main_mem)

    print(f"  Hit Rate: {cache2.hit_rate():.1%}")
    print(f"  Hits: {cache2.hits}, Misses: {cache2.misses}")


if __name__ == "__main__":
    demonstration()
```
