+++
title = "DRAM (Dynamic Random Access Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# DRAM (Dynamic Random Access Memory)

## 핵심 인사이트 (3줄 요약)
1. DRAM(Dynamic RAM)은 1개 트랜지스터와 1개 캐패시터(1T-1C)로 구성된 저비용 메모리로, 캐패시터의 전하로 데이터를 저장하고 주기적 리프레시가 필요하다
2. SRAM보다 6배 작고 저렴하지만 리프레시로 인해 느리고, RAS/CAS 신호로 행/열을 순차적으로 액세스한다
3. 기술사시험에서는 1T-1C 구조, 리프레시 방식, RAS/CAS 타이밍, DDR이 핵심이다

## Ⅰ. 개요 (500자 이상)

DRAM(Dynamic Random Access Memory)은 **1개의 트랜지스터와 1개의 캐패시터(1T-1C)로 데이터를 저장하는 동적 랜덤 액세스 메모리**이다. 캐패시터에 충전된 전하의 유무로 0과 1을 구분하며, 누설 전류로 인해 주기적인 리프레시(재충전)가 필요하다.

```
DRAM 기본 개념:
구조: 1T-1C (1 Transistor + 1 Capacitor)
- TR: 액세스 제어
- Cap: 전하 저장 (데이터)

동작:
- Write: WL 활성화, Cap 충전/방전
- Read: WL 활성화, Cap 전하 감지
- Refresh: 주기적 재충전 (64ms)

특징:
- 휘발성
- 리프레시 필요
- 저렴하고 작음
- 대용량
- 메인 메모리
```

**DRAM의 핵심 특징:**

1. **고밀도**: 1T-1C로 SRAM보다 6배 작음
2. **저비용**: 비트 당 가격 낮음
3. **리프레시**: 주기적 재충전 필요
4. **순차 액세스**: RAS→CAS 순서

```
DRAM vs SRAM:
DRAM (1T-1C):
- 작고 저렴
- 느림 (50-100ns)
- 리프레시 필요
- 메인 메모리

SRAM (6T):
- 크고 비쌈
- 빠름 (< 10ns)
- 리프레시 불필요
- 캐시
```

DRAM은 PC 메인 메모리, 그래픽 카드 VRAM, 모바일 LPDRAM 등 광범위하게 사용된다.

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 1T-1C DRAM 셀 구조

```
DRAM 셀 (1T-1C):

      VDD
       │
    [Cap] ← C (전하 저장)
       │
      WL
       │
    [TR]
    │   │
    └───┴── BL (Bit Line)
        ↑
       GND

구성:
- 1개 MOSFET (액세스 TR)
- 1개 Capacitor (저장소)

동작:
Idle: WL=0, TR off, Cap 유지
Read: WL=1, TR on, Cap→BL
Write: WL=1, TR on, BL→Cap

데이터:
C충전 = 1, C방전 = 0
```

### DRAM 읽기 동작

```
DRAM Read (Destructive):

1. Precharge:
BL, BL' → VDD/2

2. Row Activate (RAS):
RA[9:0] 입력 → Row Decoder → WL 활성화
WL=1 → 모든 Cell의 Cap → BL

3. Sensing:
BL 전압 변화 감지
Sense Amp로 증폭

4. Column Select (CAS):
CA[9:0] 입력 → Column MUX → Bit Line 선택
Data → Dout

5. Write Back:
감지한 데이터를 다시 Cell에 쓰기
(읽기가 파괴적이므로)

타이밍:
tRCD: RAS→CAS 지연 (~15ns)
tRAS: Row Active 시간 (~35ns)
tRP: Precharge 시간 (~15ns)
```

### DRAM 쓰기 동작

```
DRAM Write:

1. Precharge:
BL, BL' → VDD/2

2. Row Activate (RAS):
RA[9:0] → WL 활성화

3. Data Load:
Din → Write Driver → BL
BL=Data, BL'=Data'

4. Column Select (CAS):
CA[9:0] → Bit Line 선택

5. Write:
WL=1, TR=on → BL→Cap

타이밍:
tRCD: RAS→CAS
tWR: Write Recovery (~15ns)
```

### 리프레시 동작

```
DRAM Refresh:

문제:
캐패시터 누설 전류
→ 전하 방출
→ 데이터 소실

해결:
주기적 재충전

리프레시 주기:
tREF = 64ms (JEDEC 표준)
행 수 = 8192 (8K)
리프레시 간격 = 64ms / 8192 = 7.8µs

방식:

1. RAS-Only Refresh:
RAS만 활성화
자동으로 Sense Amp→Write Back

RAS ──┐   ┌───┐   ┌───┐
      └───┘   └───┘
CAS ──────────────────────
RA[12:0] ─┬──┬──┬──
          │  │  │
         Row0 Row1 ...

2. CBR (CAS Before RAS):
CAS를 먼저 Low, 그 후 RAS
내부 카운터로 Row 자동 증가

CAS ───┐       ┌───┐
        └───────┘
RAS ─────┐   ┌───┐   ┌───┐
         └───┘   └───┘
        Row0   Row1

3. Self Refresh:
절전 모드
내부 리프레시 자동 수행
```

### RAS/CAS 타이밍

```
DRAM 액세스 타이밍:

Read:
RAS ──┐        ┌─────┐
      │        │     │
CAS ──┴────┬───┴─────┴─────
        │   ↑
        │ tRCD (RAS→CAS)
        │
       Dout ───────────────┐       ┌──
                           │Valid  │
                           └───────┘
                           ↑ tCL (CAS Latency)

Write:
RAS ──┐        ┌─────┐
      │        │     │
CAS ──┴────┬───┴─────┴─────
Din ────┴──┬──┴──┬──┴──
          │    │
         tWR  tDS

타이밍 파라미터:
tRCD: RAS to CAS Delay
tRP: Row Precharge Time
tRAS: Row Active Time
CL: CAS Latency
tWR: Write Recovery
```

### DRAM 어드레스 분할

```
어드레스 분할 (Multiplexing):

CPU Address[23:0]
│
├─ Row Address[11:0] → RAS
└─ Col Address[11:0] → CAS

2분할 액세스:

1. RAS Phase:
RA[11:0] 입력
RAS = 0 (Active)
→ Row 선택

2. CAS Phase:
CA[11:0] 입력
CAS = 0 (Active)
→ Column 선택

장점:
- 핀 수 감소
- 패키지 작음

단점:
- 2단계 액세스
- 지연 증가
```

## Ⅲ. 융합 비교

### DRAM 세대

| 세대 | 전압 | 속도 | 클럭 | 특징 |
|------|------|------|------|------|
| SDR | 3.3V | 66-133MHz | 1x | SDR SDRAM |
| DDR | 2.5V | 100-200MHz | 2x | Double Data Rate |
| DDR2 | 1.8V | 200-533MHz | 4x | 4n Prefetch |
| DDR3 | 1.5V | 400-1066MHz | 8x | 8n Prefetch |
| DDR4 | 1.2V | 800-1600MHz | 8x | 고밀도 |
| DDR5 | 1.1V | 1600-3200MHz | 16x | 2チャンネル 내장 |

### DRAM 타입

| 타입 | 구조 | 전력 | 속도 | 응용 |
|------|------|------|------|------|
| SDRAM | Sync | 중간 | 중간 | PC |
| DDR | Double | 중간 | 빠름 | PC |
| LPDDR | Low Power | 낮음 | 중간 | 모바일 |
| GDDR | Graphics | 높음 | 매우 빠름 | GPU |
| HBM | Stacked | 중간 | 매우 빠름 | HPC/AI |

### SDRAM vs DRAM

| 비교 항목 | Async DRAM | SDRAM |
|----------|------------|-------|
| 클럭 | 없음 | 있음 |
| 동기 | 비동기 | 동기 |
| 속도 | 느림 | 빠름 |
| 인터페이스 | RAS/CAS | CLK+CMD |
| 파이프라이닝 | 불가 | 가능 |
| 응용 | 구형 PC | 현대 PC |

## Ⅳ. 실무 적용 및 기술사적 판단

### DDR SDRAM

```
DDR (Double Data Rate):

개념:
- 클럭 상승/하강 에지 모두 전송
- 2배 데이터 전송률

타이밍:
Clk ──┬───┬───┬───┬───
      ↑   ↑   ↑   ↑
      └─┬─┘   └─┬─┘
    Rising  Falling

DQ ──┬─┬─┬─┬─┬─┬─┬─┬─
     │ │ │ │ │ │ │ │
     D0 D1 D2 D3 D4 D5 D6 D7

전송률:
- Clk = 100MHz
- DDR = 200MT/s
- 64비트 × 200MT/s = 1.6GB/s

DDR4-3200:
- Base Clk = 200MHz
- Data Rate = 3200MT/s
- BW = 200MHz × 2 × 64bit × 2 / 8 = 25.6GB/s
```

### LPDDR

```
LPDDR (Low Power DDR):

특징:
1. 낮은 전압:
   LPDDR4: 1.1V
   LPDDR5: 0.9V

2. 전력 절감:
   Idle 시 Deep Power Down
   Partial Array Self Refresh

3. 작은 폼팩터:
   PoP (Package on Package)
   SoC 위 적층

응용:
- 스마트폰
- 태블릿
- 웨어러블

타이밍:
LPDDR4X-4266:
- 4266MT/s
- 17GB/s (64-bit)
- 1.1V
```

### 메모리 컨트롤러

```
메모리 컨트롤러:

기능:
1. 주소 변환
2. 타이밍 제어
3. 리프레시 관리
4. 뱅크 인터리빙
5. ECC (Error Correction)

구조:
CPU ──→ MC ──→ DRAM Channel
       │
       ├── Scheduler (명령 큐)
       ├── Timer (리프레시)
       └── Arbiter (뱅크 스케줄링)

뱅크 인터리빙:
Bank 0: Row 0
Bank 1: Row 0
Bank 2: Row 0
Bank 3: Row 0
→ 병렬 액세스

Command Ordering:
Read → Read (Open Row)
Read → Precharge → Activate → Read
```

### ECC DRAM

```
ECC (Error Correcting Code):

개념:
- 추가 비트로 오류 검출/정정
- SECDED (Single Error Correct, Double Error Detect)

구현:
Data[63:0] + ECC[7:0]
- 64비트 데이터
- 8비트 ECC (총 72비트)

오류 정정:
- 1비트 오류: 자동 정정
- 2비트 오류: 검출만
- 3비트+ 오류: 검출 불가

Hamming Code:
 parity(1,2,4,8,16,32,64)

응용:
- 서버
- 워크스테이션
- 미션 크리티컬 시스템
```

## Ⅴ. 기대효과 및 결론

DRAM은 대용량 메모리의 표준이다. 1T-1C 구조로 저렴하고 고밀도 저장을 실현한다.

## 📌 관련 개념 맵

```
DRAM
├── 구조
│   ├── 1T-1C Cell
│   ├── RAS (Row Address Strobe)
│   ├── CAS (Column Address Strobe)
│   └── Sense Amplifier
├── 동작
│   ├── Read (RAS→CAS)
│   ├── Write (RAS→CAS)
│   ├── Refresh (64ms 주기)
│   └── Precharge
├── 타입
│   ├── SDRAM (동기)
│   ├── DDR (Double Rate)
│   ├── LPDDR (Low Power)
│   └── GDDR (Graphics)
└── 특징
    ├── 고밀도
    ├── 저비용
    ├── 리프레시 필요
    └── 메인 메모리
```

## 👶 어린이를 위한 3줄 비유 설명

1. DRAM은 물통 같아요. 전기(물)를 채워두면 1이고 비워두면 0이에요. 하지만 물통에 구멍이 있어서 계속 새 나가요
2. 물이 새는 걸 막으려면 주기적으로 다시 채워야 해요(리프레시). 컴퓨터는 64ms마다 모든 물통을 확인해서 다시 채워요
3. DRAM은 이 물통을 수백만 개 만들어서 큰 저장소를 만들어요. SRAM보다 6배나 작아서 많이 만들 수 있지만, 리프레시 때문에 조금 느려요

```python
# DRAM 시뮬레이션

from typing import List
import time


class DRAMCell:
    """1T-1C DRAM 셀 시뮬레이션"""

    def __init__(self, leak_rate: float = 0.01):
        self.capacitance = 0.0  # 0.0~1.0
        self.leak_rate = leak_rate  # 누설률

    def write(self, data: int):
        """쓰기 (충전/방전)"""
        self.capacitance = float(data)

    def read(self) -> int:
        """읽기 (파괴적)"""
        # 전하 감지
        data = 1 if self.capacitance > 0.5 else 0

        # 읽기는 파괴적 (전하 방출)
        self.capacitance *= 0.5

        return data

    def leak(self):
        """전하 누설"""
        self.capacitance = max(0.0, self.capacitance - self.leak_rate)

    def refresh(self):
        """리프레시 (재충전)"""
        # 현재 상태 강화
        if self.capacitance > 0.5:
            self.capacitance = 1.0


class DRAMRow:
    """DRAM 행 (Word Line)"""

    def __init__(self, cols: int):
        self.cols = cols
        self.cells = [DRAMCell() for _ in range(cols)]
        self.active = False

    def activate(self):
        """행 활성화 (RAS)"""
        self.active = True

    def precharge(self):
        """프리차지"""
        self.active = False

    def read(self, col: int) -> int:
        """읽기"""
        if not self.active:
            raise RuntimeError("Row not activated")
        return self.cells[col].read()

    def write(self, col: int, data: int):
        """쓰기"""
        if not self.active:
            raise RuntimeError("Row not activated")
        self.cells[col].write(data)

    def leak(self):
        """모든 셀 누설"""
        for cell in self.cells:
            cell.leak()

    def refresh_row(self):
        """행 리프레시"""
        for cell in self.cells:
            cell.refresh()


class DRAMBank:
    """DRAM 뱅크"""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.memory = [DRAMRow(cols) for _ in range(rows)]
        self.active_row = -1

    def activate(self, row_addr: int):
        """행 활성화 (RAS)"""
        if self.active_row >= 0:
            self.memory[self.active_row].precharge()
        self.memory[row_addr].activate()
        self.active_row = row_addr

    def read(self, row_addr: int, col_addr: int) -> int:
        """읽기"""
        if self.active_row != row_addr:
            self.activate(row_addr)
        return self.memory[row_addr].read(col_addr)

    def write(self, row_addr: int, col_addr: int, data: int):
        """쓰기"""
        if self.active_row != row_addr:
            self.activate(row_addr)
        self.memory[row_addr].write(col_addr, data)

    def refresh(self, row_addr: int):
        """행 리프레시"""
        self.memory[row_addr].refresh_row()

    def leak_all(self):
        """모든 셀 누설 시뮬레이션"""
        for row in self.memory:
            row.leak()


class DRAM:
    """DRAM 시뮬레이터"""

    def __init__(self, rows: int = 4, cols: int = 4, banks: int = 2):
        self.rows = rows
        self.cols = cols
        self.banks = [DRAMBank(rows, cols) for _ in range(banks)]
        self.refresh_count = 0
        self.access_count = 0

    def read(self, bank: int, row: int, col: int) -> int:
        """읽기"""
        self.access_count += 1
        return self.banks[bank].read(row, col)

    def write(self, bank: int, row: int, col: int, data: int):
        """쓰기"""
        self.access_count += 1
        self.banks[bank].write(row, col, data)

    def refresh_all(self):
        """전체 리프레시"""
        for bank in self.banks:
            for row in range(self.rows):
                bank.refresh(row)
        self.refresh_count += 1

    def leak_all(self):
        """누설 시뮬레이션"""
        for bank in self.banks:
            bank.leak_all()

    def dump(self):
        """덤프"""
        result = "DRAM State:\n"
        for bi, bank in enumerate(self.banks):
            result += f"Bank {bi}:\n"
            for ri in range(self.rows):
                row_data = []
                for ci in range(self.cols):
                    val = bank.read(ri, ci)
                    row_data.append(f"{val}")
                result += f"  Row {ri}: {' '.join(row_data)}\n"
        return result


def demonstration():
    """DRAM 데모"""
    print("=" * 60)
    print("DRAM (Dynamic RAM) 데모")
    print("=" * 60)

    # DRAM 셀
    print("\n[DRAM 셀 (1T-1C)]")
    cell = DRAMCell(leak_rate=0.1)

    print("쓰기:")
    cell.write(1)
    print(f"  Capacitance = {cell.capacitance:.2f}")

    print("\n누설:")
    for i in range(5):
        cell.leak()
        print(f"  Time {i}: C = {cell.capacitance:.2f}")

    print("\n리프레시:")
    cell.refresh()
    print(f"  C = {cell.capacitance:.2f}")

    # DRAM
    print("\n[DRAM 어레이]")
    dram = DRAM(rows=4, cols=4, banks=2)

    # 초기화
    print("쓰기:")
    for bank in [0, 1]:
        for row in range(4):
            for col in range(4):
                data = bank * 16 + row * 4 + col
                dram.write(bank, row, col, data % 2)

    print("\n읽기:")
    for bank in [0, 1]:
        for row in range(2):
            for col in range(4):
                data = dram.read(bank, row, col)
                print(f"  Bank{bank} Row{row} Col{col} = {data}")

    # 누설 시뮬레이션
    print("\n[누설과 리프레시]")
    dram2 = DRAM(rows=2, cols=4, banks=1)

    # 데이터 쓰기
    for col in range(4):
        dram2.write(0, 0, col, 1)

    print("초기 상태:")
    for col in range(4):
        print(f"  Col{col} = {dram2.read(0, 0, col)}")

    print("\n누설 (5 타임 스텝):")
    for i in range(5):
        dram2.leak_all()
        if i < 3:
            print(f"  Time {i+1}: {' '.join(str(dram2.read(0, 0, c)) for c in range(4))}")

    print("\n리프레시 후:")
    dram2.refresh_all()
    for col in range(4):
        print(f"  Col{col} = {dram2.read(0, 0, col)}")

    # RAS/CAS 타이밍
    print("\n[RAS/CAS 타이밍]")
    dram3 = DRAM(rows=4, cols=4, banks=1)

    # RAS (Row Activate)
    print("RAS: Activate Row 1")
    dram3.banks[0].activate(1)

    # CAS (Column Access)
    print("CAS: Read Col 0, 1, 2, 3")
    for col in range(4):
        data = dram3.read(0, 1, col)
        print(f"  Row 1, Col {col} = {data}")

    # 다른 행 액세스 (Precharge 필요)
    print("\nPrecharge + Activate Row 2")
    dram3.banks[0].activate(2)

    print("CAS: Read Col 0-3")
    for col in range(4):
        data = dram3.read(0, 2, col)
        print(f"  Row 2, Col {col} = {data}")

    # 리프레시 오버헤드
    print("\n[리프레시 오버헤드]")
    dram4 = DRAM(rows=8, cols=8, banks=1)

    print("액세스와 리프레시:")
    for i in range(10):
        # 일부 액세스
        dram4.write(0, i % 8, 0, 1)
        dram4.read(0, i % 8, 0)

        # 주기적 리프레시
        if i % 3 == 0:
            dram4.refresh_all()
            print(f"  Cycle {i}: Refresh performed (count={dram4.refresh_count})")

    print(f"\nTotal refreshes: {dram4.refresh_count}")
    print(f"Total accesses: {dram4.access_count}")


if __name__ == "__main__":
    demonstration()
```
