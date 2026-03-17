+++
title = "디코더 (Decoder)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "조합회로"]
draft = false
+++

# 디코더 (Decoder)

## 핵심 인사이트 (3줄 요약)
1. 디코더는 n비트 입력을 2^n개 출력 중 하나를 활성화하는 조합 회로로, 주소 디코딩, 메모리 선택, 7-세그먼트 디스플레이 구동에 사용된다
2. 2^n-to-n 디코더는 각 출력에 해당하는 입력 조합에 대해서만 1이 되고, 나머지는 0이 되는 One-Hot 코드를 생성한다
3. 기술사시험에서는 디코더의 메모리 어드레스 디코딩, 칩 선택 신호, 7-세그먼트 디코더, 인코더와의 비교가 핵심이다

## Ⅰ. 개요 (500자 이상)

디코더(Decoder)는 **n비트 이진 코드를 입력받아 2^n개 출력 중 해당하는 하나를 활성화**하는 조합 논리 회로이다. 인코더의 역변환으로, 인코더가 2^n개 입력을 n비트 코드로 압축하는 반면, 디코더는 n비트 코드를 2^n개 개별 신호로 확장(Decoding)한다.

```
2-to-4 디코더:
입력: S1 S0 (2비트 선택)
출력: Y0 Y1 Y2 Y3 (4개 출력)

진리표:
| S1 S0 | Y3 Y2 Y1 Y0 |
|-------|------------|
| 0  0  | 0  0  0  1 |
| 0  1  | 0  0  1  0 |
| 1  0  | 0  1  0  0 |
| 1  1  | 1  0  0  0 |
```

**주요 응용:**
1. **메모리 주소 디코딩**: CPU가 보낸 주소를 특정 메모리 칩의 Chip Select(CS) 신호로 변환
2. **I/O 장치 선택**: 주소 디코딩을 통해 특정 I/O 장치 활성화
3. **7-세그먼트 디코더**: BCD 코드를 7-세그먼트 LED 구동 신호로 변환
4. **명령어 디코딩**: 명령어 코드를 제어 신호로 변환

디코더는 일반적으로 **Active-Low 출력(출력이 0일 때 활성)**을 사용한다. 이는 여러 디코더를 캐스케이딩(Cascading)할 때 유리하다.

```
3-to-8 디코더 (74LS138):
입력: A2 A1 A0 (3비트 주소)
출력: Y0' Y1' ... Y7' (Active Low)
Enable: G1 G2A' G2B' (Chip Select)

G1=1, G2A'=0, G2B'=1일 때만 동작
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 디코더 회로 구조

```
2-to-4 디코더 회로:
S1 ──┬───────┬────── AND(Y3) ─── Y3
     │       │      │
     │    NOT     ─┴── AND(Y2) ─── Y2
     │       │      │
S0 ──┼───────┼── AND(Y1) ─── Y1
     │       │   │
     │    NOT └── AND(Y0) ─── Y0

불 대수식:
Y0 = S1' · S0'
Y1 = S1' · S0
Y2 = S1 · S0'
Y3 = S1 · S0

각 minterm에 해당하는 AND 게이트
```

### BCD 7-세그먼트 디코더

```
BCD 7-세그먼트 디코더:
입력: D C B A (BCD 코드)
출력: a b c d e f g (7개 LED)

BCD → 7-세그먼트 변환:
0 (0000) → a b c d e f (g OFF)
1 (0001) → b c
2 (0010) → a b d e g
3 (0011) → a b c d g
4 (0100) → b c f g
5 (0101) → a c d f g
6 (0110) → a c d e f g
7 (0111) → a b c
8 (1000) → a b c d e f g
9 (1001) → a b c d f g

회로 복잡도:
- 각 세그먼트는 4입력 OR-AND 구조
- 약 50-100 게이트
- ROM/PLD로도 구현 가능
```

### 메모리 주소 디코딩

```
16KB 메모리 시스템 주소 디코딩:
CPU 주소: A15 A14 A13 ... A1 A0 (16비트)
메모리 크기: 16KB = 2^14 (A13-A0)
칩 선택: A15 A14로 디코딩

A15 A14
  0   0  → RAM0 (0000-3FFF)
  0   1  → RAM1 (4000-7FFF)
  1   0  → ROM  (8000-BFFF)
  1   1  → I/O  (C000-FFFF)

2-to-4 디코더로 Chip Select 생성:
CS0' = A15' · A14' (RAM0 활성)
CS1' = A15' · A14  (RAM1 활성)
CS2' = A15  · A14' (ROM 활성)
CS3' = A15  · A14  (I/O 활성)
```

### 디코더 캐스케이딩

```
4-to-16 디코더 (2-to-4 × 2개):
A3 ───┐
      │
A2 ───┴──→ 2-to-4 Decoder (High) → CS0' CS1' CS2' CS3'
           │
A1 ────┬───┴──→ 2-to-4 Decoder (Low) → CS0' CS1' CS2' CS3'
       │
A0 ────┘

High Decoder 출력 → Low Decoder Enable
총 16개 출력 (Y0' ~ Y15')
```

## Ⅲ. 융합 비교

### 디코더 vs 인코더

| 비교 항목 | 디코더 (Decoder) | 인코더 (Encoder) |
|----------|-----------------|------------------|
| 입력 | n비트 코드 | 2^n개 입력 |
| 출력 | 2^n개 (One-Hot) | n비트 코드 |
| 기능 | 코드 → 신호 분해 | 신호 → 코드 압축 |
| 응용 | 주소 디코딩 | 우선순위 인코딩 |
| 복잡도 | O(2^n) 크기 | O(n) 작음 |

### 디코더 vs MUX

| 비교 항목 | 디코더 | MUX |
|----------|--------|-----|
| 입력 | n비트 주소 | 2^n개 데이터 + n비트 선택 |
| 출력 | 2^n개 | 1개 |
| 기능 | 주소 해석 | 데이터 선택 |
| 응용 | 메모리 디코딩 | ALU 입력 선택 |

### 디코더 유형

| 타입 | 입력 | 출력 | Enable | 응용 |
|------|------|------|--------|------|
| 2-to-4 | 2비트 | 4개 | 1-3개 | 작은 시스템 |
| 3-to-8 | 3비트 | 8개 | 3개 | 주소 디코딩 |
| 4-to-16 | 4비트 | 16개 | 2개 | 대형 시스템 |
| BCD-7seg | 4비트 | 7개 | 없음 | 디스플레이 |

## Ⅳ. 실무 적용 및 기술사적 판단

### 64KB 메모리 시스템 디코딩

```
64KB 메모리 맵:
0000-3FFF: RAM  (16KB)
4000-7FFF: RAM  (16KB)
8000-BFFF: ROM  (16KB)
C000-FFFF: I/O  (16KB)

주소 디코딩 회로:
A15 A14 A13 A12 ──→ Decoder

간단 디코딩 (A15, A14만 사용):
- CS_RAM0' = A15' · A14'
- CS_RAM1' = A15' · A14
- CS_ROM'  = A15  · A14'
- CS_IO'   = A15  · A14

세분 디코딩 (A15-A12 사용):
- 4KB 그래뉼러리티
- 4-to-16 디코더 사용
```

### 7-세그먼트 디코더 설계

```
Truth Table (일부):
D C B A | a b c d e f g
--------|----------------
0 0 0 0 | 1 1 1 1 1 1 0
0 0 0 1 | 0 1 1 0 0 0 0
0 0 1 0 | 1 1 0 1 1 0 1
...

K-Map 최적화:
a = D' + B·C' + B'·C + A
b = D' + B' + (C ⊕ A)
c = D' + C + A'
...

CMOS 구현:
- 각 세그먼트 = AOI/OAI 게이트
- 10-15 트랜지스터/세그먼트
- 총 ~100 트랜지스터
```

### 디코더 응용 회로

```
1. 명령어 디코더:
   Opcode → Control Signals
   - 6비트 Opcode → 64개 마이크로연산

2. 인터럽트 컨트롤러:
   Interrupt Vector → Priority Encoding

3. FPGA Look-Up Table:
   N입력 → 2^N개 LUT

4. 주소 라인 디코딩:
   A[31:0] → Bank Select
```

## Ⅴ. 기대효과 및 결론

디코더는 주소 디코딩의 핵심이다. 메모리, I/O 장치 선택에 필수적이다.

## 📌 관련 개념 맵

```
디코더
├── 정의: n비트 → 2^n개 One-Hot
├── 종류
│   ├── 2-to-4 디코더
│   ├── 3-to-8 디코더
│   ├── 4-to-16 디코더
│   └── BCD 7-세그먼트
└── 응용
    ├── 메모리 주소 디코딩
    ├── I/O 장치 선택
    ├── 명령어 디코딩
    └── 7-세그먼트 디스플레이
```

## 👶 어린이를 위한 3줄 비유 설명

1. 디코더는 "비밀번호"를 받아서 해당하는 문을 열어주는 열쇠 관리자와 비슷해요. 2비트 코드(00, 01, 10, 11)를 입력하면 4개의 문 중 하나를 열어줘요
2. 컴퓨터가 메모리 주소를 보내면 디코더가 그 주소를 해석해서 "어떤 메모리 칩을 사용할지" 선택해요
3. 숫자 표시판에 7-세그먼트 디코더가 있어서, 0~9까지의 숫자 코드를 받아서 7개의 LED를 적절히 켜서 숫자를 표시해요

```python
# 디코더 시뮬레이션 및 분석 도구

from typing import List, Dict, Tuple


class Decoder:
    """
    n-to-2^n 디코더 시뮬레이션
    """

    def __init__(self, input_bits: int):
        """
        n-to-2^n 디코더 생성

        Args:
            input_bits: 입력 비트 수
        """
        if input_bits < 1 or input_bits > 16:
            raise ValueError("입력 비트는 1~16 범위여야 합니다")

        self.input_bits = input_bits
        self.output_bits = 2 ** input_bits
        self.name = f"{input_bits}-to-{self.output_bits} Decoder"

    def decode(self, input_code: int) -> List[int]:
        """
        입력 코드를 디코딩

        Args:
            input_code: 입력 코드 (0 ~ 2^n-1)

        Returns:
            One-Hot 출력 리스트 (길이 2^n)
        """
        if not (0 <= input_code < self.output_bits):
            raise ValueError(f"입력 코드는 0 ~ {self.output_bits - 1} 범위여야 합니다")

        output = [0] * self.output_bits
        output[input_code] = 1
        return output

    def decode_active_low(self, input_code: int) -> List[int]:
        """
        Active-Low 출력 디코딩

        Args:
            input_code: 입력 코드

        Returns:
            Active-Low One-Hot 출력 (0=활성, 1=비활성)
        """
        output = self.decode(input_code)
        return [1 - x for x in output]

    def truth_table(self) -> List[Dict]:
        """진리표 생성"""
        table = []
        for code in range(self.output_bits):
            output = self.decode(code)
            row = {
                'input': f"{code:0{self.input_bits}b}",
                'output': output,
                'active_output': output.index(1)
            }
            table.append(row)
        return table

    def print_truth_table(self):
        """진리표 출력"""
        print(f"\n{'='*70}")
        print(f"{self.name} 진리표")
        print(f"{'='*70}")

        for row in self.truth_table():
            print(f"입력: {row['input']} → 출력[{row['active_output']}] = 1")

        print("="*70)


class BCD7SegmentDecoder:
    """
    BCD 7-세그먼트 디코더
    """

    # 7-세그먼트 패턴 (a b c d e f g)
    # 0 = OFF, 1 = ON
    SEGMENT_PATTERNS = {
        0: [1, 1, 1, 1, 1, 1, 0],  # 0
        1: [0, 1, 1, 0, 0, 0, 0],  # 1
        2: [1, 1, 0, 1, 1, 0, 1],  # 2
        3: [1, 1, 1, 1, 0, 0, 1],  # 3
        4: [0, 1, 1, 0, 0, 1, 1],  # 4
        5: [1, 0, 1, 1, 0, 1, 1],  # 5
        6: [1, 0, 1, 1, 1, 1, 1],  # 6
        7: [1, 1, 1, 0, 0, 0, 0],  # 7
        8: [1, 1, 1, 1, 1, 1, 1],  # 8
        9: [1, 1, 1, 1, 0, 1, 1],  # 9
    }

    def __init__(self):
        self.name = "BCD 7-Segment Decoder"

    def decode(self, bcd: int) -> List[int]:
        """
        BCD를 7-세그먼트로 변환

        Args:
            bcd: BCD 코드 (0-9)

        Returns:
            7개 세그먼트 상태 [a, b, c, d, e, f, g]
        """
        if not (0 <= bcd <= 9):
            raise ValueError("BCD 입력은 0-9 범위여야 합니다")

        return self.SEGMENT_PATTERNS[bcd].copy()

    def display(self, bcd: int) -> str:
        """
        7-세그먼트 디스플레이 ASCII 아트

        Args:
            bcd: BCD 코드

        Returns:
            ASCII 디스플레이 문자열
        """
        segments = self.decode(bcd)
        a, b, c, d, e, f, g = segments

        # 7-세그먼트 레이아웃
        #   a
        # f   b
        #   g
        # e   c
        #   d

        display = []
        display.append(" " + ("_" if a else " ") + " ")  # a
        display.append(("|" if f else " ") + " " + ("|" if b else " "))  # f, b
        display.append(" " + ("_" if g else " ") + " ")  # g
        display.append(("|" if e else " ") + " " + ("|" if c else " "))  # e, c
        display.append(" " + ("_" if d else " ") + " ")  # d

        return "\n".join(display)

    def print_table(self):
        """BCD 7-세그먼트 변환표 출력"""
        print(f"\n{'='*60}")
        print("BCD 7-세그먼트 디코더 변환표")
        print(f"{'='*60}")

        for bcd in range(10):
            segments = self.decode(bcd)
            seg_str = "".join(['1' if s else '0' for s in segments])
            print(f"\nBCD {bcd} → 세그먼트: {seg_str} (a b c d e f g)")
            print(self.display(bcd))

        print("="*60)


class MemoryAddressDecoder:
    """
    메모리 주소 디코더
    """

    def __init__(self, total_bits: int, decode_bits: int):
        """
        주소 디코더 생성

        Args:
            total_bits: 총 주소 비트 수
            decode_bits: 디코딩에 사용할 상위 비트 수
        """
        self.total_bits = total_bits
        self.decode_bits = decode_bits
        self.decoder = Decoder(decode_bits)

    def decode_address(self, address: int) -> Tuple[int, List[int]]:
        """
        주소를 디코딩하여 Chip Select 생성

        Args:
            address: 메모리 주소

        Returns:
            (selected_bank, chip_selects): 선택된 뱅크, CS 신호들
        """
        if not (0 <= address < 2**self.total_bits):
            raise ValueError(f"주소는 0 ~ {2**self.total_bits - 1} 범위여야 합니다")

        # 상위 비트 추출
        high_bits = address >> (self.total_bits - self.decode_bits)

        # 디코딩
        chip_selects = self.decoder.decode_active_low(high_bits)

        return high_bits, chip_selects

    def analyze_memory_map(self, block_size: int) -> List[Dict]:
        """
        메모리 맵 분석

        Args:
            block_size: 각 블록의 크기 (바이트)

        Returns:
            메모리 맵 정보 리스트
        """
        memory_map = []
        num_blocks = 2 ** self.decode_bits

        for i in range(num_blocks):
            start_addr = i * block_size
            end_addr = start_addr + block_size - 1

            memory_map.append({
                'block': i,
                'start': start_addr,
                'end': end_addr,
                'start_hex': f"{start_addr:04X}",
                'end_hex': f"{end_addr:04X}",
                'size_kb': block_size // 1024
            })

        return memory_map

    def print_memory_map(self, block_size: int):
        """메모리 맵 출력"""
        print(f"\n{'='*80}")
        print(f"메모리 주소 디코딩 (상위 {self.decode_bits}비트)")
        print(f"{'='*80}")

        for block in self.analyze_memory_map(block_size):
            print(f"Block {block['block']}: {block['start_hex']}h - {block['end_hex']}h "
                  f"({block['size_kb']}KB)")

        print("="*80)


def demonstration():
    """디코더 데모"""
    # 2-to-4 디코더
    dec2 = Decoder(2)
    dec2.print_truth_table()

    print("\n[2-to-4 디코더 동작 예시]")
    for code in [0, 1, 2, 3]:
        output = dec2.decode(code)
        active = output.index(1)
        print(f"  입력 {code:02b} → 출력[{active}] 활성")

    # 3-to-8 디코더
    dec3 = Decoder(3)
    print(f"\n[3-to-8 디코더]")
    print(f"입력 5 (101b) → 출력: {dec3.decode(5)}")

    # BCD 7-세그먼트
    bcd_decoder = BCD7SegmentDecoder()
    bcd_decoder.print_table()

    # 메모리 주소 디코딩 (64KB, 상위 2비트)
    addr_decoder = MemoryAddressDecoder(total_bits=16, decode_bits=2)

    print(f"\n[주소 디코딩 예시]")
    test_addresses = [0x0000, 0x3FFF, 0x4000, 0x8000, 0xC000]
    for addr in test_addresses:
        bank, cs = addr_decoder.decode_address(addr)
        print(f"주소 {addr:04X}h → Bank {bank}, CS: {cs}")

    addr_decoder.print_memory_map(block_size=16*1024)  # 16KB 블록


if __name__ == "__main__":
    demonstration()
```
