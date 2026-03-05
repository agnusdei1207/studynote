+++
title = "주소 인코딩 (Address Encoding)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# 주소 인코딩 (Address Encoding)

## 핵심 인사이트 (3줄 요약)
1. 주소 인코딩은 메모리 주소 공간을 효율적으로 관리하고 액세스하기 위한 방식으로, Byte/Word Addressing, Big/Little Endian, Segment/Page, Virtual Memory 등 다양한 기법이 있다
2. Byte Addressing은 바이트 단위 주소 지정을, Word Addressing은 워드 단위 지정을 의미하며, Endian은 멀티바이트 데이터의 저장 순서를 결정한다
3. 기술사시험에서는 주소 계산, Endian 변환, Segment/Page 테이블 구조, Virtual Address 변환이 핵심이다

## Ⅰ. 개요 (500자 이상)

주소 인코딩(Address Encoding)은 **메모리의 각 위치를 식별하고 액세스하기 위한 주소를 부여하고 관리하는 방식**이다. 컴퓨터는 바이트 단위로 주소를 지정하지만, 워드 단위로 액세스할 수도 있으며, 멀티바이트 데이터의 저장 순서(Endianness)와 주소 공간 확장(가상 메모리)을 고려해야 한다.

```
주소 인코딩 기본 개념:
목적: 메모리 위치 식별
단위: Byte (일반적)
범위: 0 ~ 2ⁿ-1 (n비트 주소)

구성:
Physical Address: 실제 메모리 주소
Virtual Address: 프로세스 논리 주소
Linear Address: 세그먼트 후 주소

특징:
- Byte 단위 (대부분)
- Word aligned (성능)
- 가상/물리 분리
- 페이지/세그먼트 관리
```

**주소 인코딩의 핵심 요소:**

1. **Addressing Mode**: Byte vs Word
2. **Endianness**: Big vs Little
3. **Alignment**: 성능 최적화
4. **Virtual Memory**: 주소 공간 확장

```
주소 체계:
Virtual Address (프로세스)
    ↓ MMU
Linear Address (세그먼트 후)
    ↓ Page Table
Physical Address (실제 메모리)
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Byte Addressing

```
Byte Addressing:

메모리:
Address: 0   1   2   3   4   5   6   7
Data:   [B0][B1][B2][B3][B4][B5][B6][B7]

각 바이트마다 고유 주소
- Address 0: Byte 0
- Address 1: Byte 1
- ...

특징:
- 가장 일반적
- 바이트 단위 액세스
- 문자 처리에 적합

Word 액세스:
- 32비트 Word = 4 바이트
- Address 0 → [B0][B1][B2][B3]
- Address 4 → [B4][B5][B6][B7]
```

### Word Addressing

```
Word Addressing:

메모리:
Word Address: 0   1   2   3
Data:        [W0][W1][W2][W3]
             (각 4바이트)

특징:
- 워드 단위 주소
- 단순한 하드웨어
- 과거 슈퍼컴퓨터

Address 변환:
Byte Address = Word Address × Word Size
Word Address = Byte Address / Word Size

예: 4바이트 Word
Word 0 → Byte 0-3
Word 1 → Byte 4-7
```

### Endianness

```
Endianness (멀티바이트 저장 순서):

Big Endian (MSB First):
Address 0 1 2 3
Data    [MSB][...][...][LSB]
Value 0x12345678 저장:
0: 0x12, 1: 0x34, 2: 0x56, 3: 0x78

Little Endian (LSB First):
Address 0 1 2 3
Data    [LSB][...][...][MSB]
Value 0x12345678 저장:
0: 0x78, 1: 0x56, 2: 0x34, 3: 0x12

비교:
Big Endian: 네트워크, IBM, SPARC
Little Endian: x86, ARM
```

### Address Alignment

```
Alignment (정렬):

Aligned Access (주소가 n의 배수):
- Word (4바이트): Address % 4 == 0
- 예: 0, 4, 8, 12...

Unaligned Access:
- Word를 1, 5, 9...에 저장
- 2개 액세스 필요
- 느림 또는 에러

예: 4바이트 Word @ Address 2
Address: 0 1 2 3 4 5 6 7
Data:    [  ][XX][XX][  ][  ]
         액세스 1  액세스 2

성능:
Aligned: 1 메모리 액세스
Unaligned: 2 메모리 액세스
```

### Segment Addressing

```
세그먼트 주소 (x86 Real Mode):

Logical Address:
Segment:Offset
(16비트: 16비트)

Physical Address 계산:
PA = Segment × 16 + Offset

예:
Segment = 0x1000
Offset = 0x0100
PA = 0x1000 × 16 + 0x0100
   = 0x10000 + 0x0100
   = 0x10100

세그먼트 레지스터:
- CS: Code Segment
- DS: Data Segment
- SS: Stack Segment
- ES: Extra Segment

장점:
- 20비트 주소 공간 (1MB)
- 작은 오프셋으로 큰 공간 액세스
```

### Paging

```
페이징 주소 (Virtual Memory):

Virtual Address [31:0]
├── Page Number [31:12]
└── Page Offset [11:0]

Page Table Entry (PTE):
[Valid][Prot][Frame Number][...]

주소 변환:
1. VA[31:12]로 PTE 검색
2. PTE에서 Frame Number 추출
3. PA = Frame Number || VA[11:0]

예:
VA = 0x0040_1234
Page Number = 0x00401
Page Offset = 0x234

PTE[0x00401] = {Valid=1, Frame=0x00123}
PA = 0x00123 || 0x234 = 0x00123_0234

TLB (Translation Lookaside Buffer):
- 페이지 테이블 캐시
- 빠른 주소 변환
```

### Multi-level Paging

```
다단계 페이징 (x86-64):

4-Level Paging:
PML4 → PDP → PD → PT → Page

Virtual Address [63:0]
├── PML4 Index [63:48] (9비트)
├── PDP Index [47:39] (9비트)
├── PD Index [38:30] (9비트)
├── PT Index [29:21] (9비트)
└── Page Offset [20:0] (12비트)

주소 변환:
1. PML4[VA[63:48]] → PDP 주소
2. PDP[VA[47:39]] → PD 주소
3. PD[VA[38:30]] → PT 주소
4. PT[VA[29:21]] → Frame 주소
5. PA = Frame || VA[20:0]

장점:
- 48비트 VA 공간 (256TB)
- 희소한 공간 효율적
```

## Ⅲ. 융합 비교

### Addressing 모드

| 모드 | 단위 | 주소 범위 | 응용 |
|------|------|----------|------|
| Byte | 1바이트 | 0~2ⁿ-1 | 범용 |
| Word | 2/4/8바이트 | 0~2ⁿ/W -1 | 과거 슈퍼컴퓨터 |
| Bit | 1비트 | 0~8×2ⁿ-1 | 일부 임베디드 |

### Endianness

| 타입 | MSB 위치 | 예시 | 아키텍처 |
|------|----------|------|----------|
| Big | 최저 주소 | Network, SPARC | IBM, PowerPC |
| Little | 최고 주소 | x86, ARM | Intel, AMD |
| Bi-Endian | 선택 가능 | ARM, MIPS | configurable |

### 주소 정렬

| 정렬 | 주소 조건 | 액세스 | 성능 |
|------|----------|--------|------|
| 1바이트 | 항상 | 1회 | 항상 |
| 2바이트 | 짝수 | 1-2회 | Aligned 빠름 |
| 4바이트 | 4의 배수 | 1-2회 | Aligned 빠름 |
| 8바이트 | 8의 배수 | 1-2회 | Aligned 빠름 |

## Ⅳ. 실무 적용 및 기술사적 판단

### x86 Addressing

```
x86-64 주소 지정:

Register Addressing:
MOV RAX, [RBX]

Displacement:
MOV RAX, [RBX + 8]

Base + Index:
MOV RAX, [RBX + RCX]

Base + Index * Scale + Displacement:
MOV RAX, [RBX + RCX*4 + 100]

Addressing Components:
- Base Register: RBX
- Index Register: RCX
- Scale: 1, 2, 4, 8
- Displacement: 0/8/32비트

Effective Address:
EA = Base + Index * Scale + Displacement
```

### MIPS Addressing

```
MIPS 주소 지정:

Base Register:
LW R1, 0(R2)
→ Address = R2 + 0

PC-Relative:
BEQ R1, R2, label
→ Address = PC + offset

Jump Target:
J label
→ Address = PC[31:28] || (offset × 4)

Immediate:
ADDI R1, R2, imm
→ Sign-extended immediate

특징:
- Load/Store 아키텍처
- 모든 주소 레지스터 기반
- Word aligned (4의 배수)
```

### ARM Addressing

```
ARM 주소 지정:

Register Offset:
LDR R0, [R1, R2]

Immediate Offset:
LDR R0, [R1, #4]

Scaled Register:
LDR R0, [R1, R2, LSL #2]
→ Address = R1 + (R2 × 4)

Pre-indexed:
LDR R0, [R1, #4]!
→ R1 = R1 + 4
→ Load from [R1]

Post-indexed:
LDR R0, [R1], #4
→ Load from [R1]
→ R1 = R1 + 4

PC-Relative:
LDR PC, [PC, #offset]
→ Address = PC + offset
```

### Virtual Memory

```

가상 메모리 시스템:

구성:
1. Page Table:
   - VA → PA 매핑
   - OS 관리

2. TLB:
   - 페이지 테이블 캐시
   - HW 관리

3. MMU:
   - 주소 변환 하드웨어
   - TLB + Page Walker

동작:
1. CPU가 VA 요청
2. TLB 확인
3. TLB Hit → PA 반환
4. TLB Miss → Page Table Walk
5. PA 반환

Page Fault:
- VA에 매핑 없음
- OS로 트랩
- 페이지 로드/할당
- 재시도

장점:
- 프로세스 격리
- 큰 주소 공간
- 물리 메모리 초과 액세스
```

## Ⅴ. 기대효과 및 결론

주소 인코딩은 메모리 관리의 기초다. Endian, Alignment, Virtual Memory로 효율적인 액세스를 제공한다.

## 📌 관련 개념 맵

```
주소 인코딩
├── 단위
│   ├── Byte Addressing (일반적)
│   └── Word Addressing (과거)
├── Endianness
│   ├── Big Endian (MSB First)
│   └── Little Endian (LSB First)
├── 정렬
│   ├── Aligned (빠름)
│   └── Unaligned (느림)
├── 방식
│   ├── Segment (x86 Real Mode)
│   ├── Paging (Virtual Memory)
│   └── Flat (Linear)
└── 변환
    ├── Logical → Linear (Segment)
    └── Linear → Physical (Paging)
```

## 👶 어린이를 위한 3줄 비유 설명

1. 주소 인코딩은 집 주소 같아요. 101호, 102호처럼 각 바이트에 번호를 붙여서 찾기 쉽게 해요
2. Endian은 멀티바이트 숫자를 쓸 때 순서를 정하는 거예요. Big은 큰 자리를 먼저 쓰고, Little은 작은 자리를 먼저 써요
3. 정렬은 책장에 책을 꽂을 때 자리에 딱 맞춰 꽂는 것 같아요. 자리에 맞추면 한 번에 뽑을 수 있지만, 삐뚤게 꽂으면 두 번 뽑아야 해요

```python
# 주소 인코딩 시뮬레이션

from typing import List, Dict, Tuple


class ByteAddressableMemory:
    """Byte Addressable Memory"""

    def __init__(self, size: int):
        self.memory = [0] * size

    def read_byte(self, address: int) -> int:
        """바이트 읽기"""
        if 0 <= address < len(self.memory):
            return self.memory[address]
        raise ValueError("주소 범위 초과")

    def write_byte(self, address: int, data: int):
        """바이트 쓰기"""
        if 0 <= address < len(self.memory):
            self.memory[address] = data & 0xFF
        else:
            raise ValueError("주소 범위 초과")

    def read_word(self, address: int, word_size: int = 4) -> int:
        """워드 읽기 (Little Endian)"""
        result = 0
        for i in range(word_size):
            byte = self.read_byte(address + i)
            result |= byte << (i * 8)
        return result

    def read_word_be(self, address: int, word_size: int = 4) -> int:
        """워드 읽기 (Big Endian)"""
        result = 0
        for i in range(word_size):
            byte = self.read_byte(address + i)
            result |= byte << ((word_size - 1 - i) * 8)
        return result

    def write_word(self, address: int, data: int, word_size: int = 4):
        """워드 쓰기 (Little Endian)"""
        for i in range(word_size):
            byte = (data >> (i * 8)) & 0xFF
            self.write_byte(address + i, byte)

    def write_word_be(self, address: int, data: int, word_size: int = 4):
        """워드 쓰기 (Big Endian)"""
        for i in range(word_size):
            byte = (data >> ((word_size - 1 - i) * 8)) & 0xFF
            self.write_byte(address + i, byte)


class WordAddressableMemory:
    """Word Addressable Memory"""

    def __init__(self, size: int, word_size: int = 4):
        self.word_size = word_size
        self.memory = [0] * size

    def read_word(self, address: int) -> int:
        """워드 읽기"""
        if 0 <= address < len(self.memory):
            return self.memory[address]
        raise ValueError("주소 범위 초과")

    def write_word(self, address: int, data: int):
        """워드 쓰기"""
        if 0 <= address < len(self.memory):
            self.memory[address] = data & ((1 << (self.word_size * 8)) - 1)
        else:
            raise ValueError("주소 범위 초관")

    def to_byte_address(self, word_addr: int) -> int:
        """워드 주소 → 바이트 주소"""
        return word_addr * self.word_size

    def from_byte_address(self, byte_addr: int) -> int:
        """바이트 주소 → 워드 주소"""
        return byte_addr // self.word_size


class SegmentAddressing:
    """세그먼트 주소 지정 (x86 Real Mode)"""

    @staticmethod
    def to_physical(segment: int, offset: int) -> int:
        """논리 주소 → 물리 주소"""
        return (segment << 4) + offset

    @staticmethod
    def from_physical(physical: int, segment: int) -> int:
        """물리 주소 → 오프셋"""
        return physical - (segment << 4)


class PageTable:
    """페이지 테이블"""

    def __init__(self, page_size: int = 4096):
        self.page_size = page_size
        self.offset_bits = (page_size - 1).bit_length()
        self.entries: Dict[int, int] = {}  # VPN → PFN

    def map_page(self, vpn: int, pfn: int):
        """페이지 매핑"""
        self.entries[vpn] = pfn

    def translate(self, virtual_address: int) -> int:
        """가상 주소 → 물리 주소"""
        vpn = virtual_address >> self.offset_bits
        offset = virtual_address & (self.page_size - 1)

        if vpn not in self.entries:
            raise ValueError(f"Page Fault: VPN {vpn} not mapped")

        pfn = self.entries[vpn]
        physical_address = (pfn << self.offset_bits) | offset
        return physical_address


class TLB:
    """Translation Lookaside Buffer"""

    def __init__(self, size: int = 16):
        self.size = size
        self.entries: List[Tuple[int, int]] = []  # (VPN, PFN)
        self.access_order: List[int] = []

    def lookup(self, vpn: int) -> Tuple[bool, int]:
        """TLB 조회"""
        for i, (v, p) in enumerate(self.entries):
            if v == vpn:
                # Hit
                if i in self.access_order:
                    self.access_order.remove(i)
                self.access_order.append(i)
                return True, p
        return False, -1

    def insert(self, vpn: int, pfn: int):
        """TLB 삽입"""
        if len(self.entries) >= self.size:
            # LRU 교체
            lru_index = self.access_order.pop(0)
            self.entries[lru_index] = (vpn, pfn)
            self.access_order.append(lru_index)
        else:
            self.entries.append((vpn, pfn))
            self.access_order.append(len(self.entries) - 1)


def demonstration():
    """주소 인코딩 데모"""
    print("=" * 60)
    print("주소 인코딩 (Address Encoding) 데모")
    print("=" * 60)

    # Byte Addressable Memory
    print("\n[Byte Addressable Memory]")
    mem = ByteAddressableMemory(256)

    # 워드 쓰기
    mem.write_word(0, 0x12345678)
    print(f"Write 0x12345678 @ Address 0")

    # 바이트 읽기
    print("\nByte Reads:")
    for i in range(4):
        byte = mem.read_byte(i)
        print(f"  Address {i}: 0x{byte:02X}")

    # Endian 비교
    print("\n[Endianness]")
    mem2 = ByteAddressableMemory(16)

    value = 0xAABBCCDD
    mem2.write_word(0, value)  # Little Endian
    mem2.write_word_be(4, value)  # Big Endian

    print(f"Value: 0x{value:08X}")
    print(f"\nLittle Endian @ 0:")
    for i in range(4):
        print(f"  Address {i}: 0x{mem2.read_byte(i):02X}")

    print(f"\nBig Endian @ 4:")
    for i in range(4):
        print(f"  Address {4+i}: 0x{mem2.read_byte(4+i):02X}")

    # Word Addressable
    print("\n[Word Addressable Memory]")
    wmem = WordAddressableMemory(size=64, word_size=4)

    wmem.write_word(0, 0x1000)
    wmem.write_word(1, 0x2000)
    print(f"Word 0: 0x{wmem.read_word(0):04X}")
    print(f"Word 1: 0x{wmem.read_word(1):04X}")

    print(f"\nByte Address of Word 0: {wmem.to_byte_address(0)}")
    print(f"Word Address of Byte 8: {wmem.from_byte_address(8)}")

    # Segment Addressing
    print("\n[Segment Addressing (x86 Real Mode)]")

    logical_addrs = [
        (0x1000, 0x0100),
        (0x2000, 0x0200),
        (0xA000, 0x1234)
    ]

    print("Logical → Physical:")
    for seg, off in logical_addrs:
        pa = SegmentAddressing.to_physical(seg, off)
        print(f"  {seg:04X}:{off:04X} → 0x{pa:05X}")

    # Paging
    print("\n[Paging]")
    page_table = PageTable(page_size=4096)

    # 페이지 매핑
    page_table.map_page(vpn=0x00100, pfn=0x00100)
    page_table.map_page(vpn=0x00101, pfn=0x00500)

    # 주소 변환
    virtual_addrs = [0x00100000, 0x00100100, 0x00101000]
    print("Virtual → Physical:")
    for va in virtual_addrs:
        try:
            pa = page_table.translate(va)
            print(f"  0x{va:08X} → 0x{pa:08X}")
        except ValueError as e:
            print(f"  0x{va:08X} → Page Fault")

    # TLB
    print("\n[TLB]")
    tlb = TLB(size=4)

    # TLB 삽입
    tlb.insert(0x100, 0x500)
    tlb.insert(0x101, 0x501)

    # TLB 조회
    print("TLB Lookup:")
    vpns = [0x100, 0x101, 0x102]
    for vpn in vpns:
        hit, pfn = tlb.lookup(vpn)
        if hit:
            print(f"  VPN 0x{vpn:03X} → Hit, PFN = 0x{pfn:03X}")
        else:
            print(f"  VPN 0x{vpn:03X} → Miss")

    # Alignment
    print("\n[Address Alignment]")
    addresses = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    print("4-byte Alignment:")
    for addr in addresses:
        aligned = (addr % 4 == 0)
        accesses = 1 if aligned else 2
        print(f"  Address {addr}: {'Aligned' if aligned else 'Unaligned'} ({accesses} accesses)")

    # Mixed Endian 시스템
    print("\n[Bi-Endian System]")
    mem3 = ByteAddressableMemory(16)

    # Little Endian 모드
    mem3.write_word(0, 0x12345678)
    le_value = mem3.read_word(0)
    print(f"Little Endian: 0x{le_value:08X}")

    # Big Endian 모드
    mem3.write_word_be(0, 0x12345678)
    be_value = mem3.read_word_be(0)
    print(f"Big Endian: 0x{be_value:08X}")

    # Address Space 계산
    print("\n[Address Space]")
    print("32-bit: 2³² = 4GB")
    print("64-bit: 2⁶⁴ = 16EB")
    print("48-bit Virtual: 2⁴⁸ = 256TB")


if __name__ == "__main__":
    demonstration()
```
