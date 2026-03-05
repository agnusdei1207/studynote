+++
title = "캐시 메모리 (Cache Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# 캐시 메모리 (Cache Memory)

## 핵심 인사이트 (3줄 요약)
1. 캐시 메모리는 CPU와 메인 메모리 사이의 고속 버퍼로, 지역성(Locality) 원리를 이용해 자주 참조하는 데이터를 SRAM에 저장하여 메모리 병목을 해결한다
2. Direct Map, Set Associative, Fully Associative의 매핑 방식이 있으며, Hit/Miss 판정을 위해 Tag, Valid, Dirty 비트를 사용한다
3. 기술사시험에서는 캐시 라인 구조, 매핑 방식, 교체/Write 정책, Miss 종류가 핵심이다

## Ⅰ. 개요 (500자 이상)

캐시 메모리(Cache Memory)는 **CPU의 속도와 메인 메모리의 속도 차이를 줄이기 위해 중간에 배치된 고속 버퍼 메모리**이다. SRAM으로 구현되며, 지역성(Locality) 원리에 따라 자주 사용하는 데이터를 미리 가져와서 CPU가 빠르게 액세스할 수 있게 한다.

```
캐시 기본 개념:
구조: SRAM 기반 고속 메모리
위치: CPU와 메인 메모리 사이
목적: 메모리 액세스 시간 감소

원리: 지역성 (Locality)
1. 시간적 지역성 (Temporal):
   최근 참조한 데이터를 다시 참조

2. 공간적 지역성 (Spatial):
   인접한 데이터 참조 가능성 높음

동작:
- Hit: 캐시에 데이터 있음 → 빠름
- Miss: 캐시에 없음 → 메모리 액세스

특징:
- SRAM (빠름)
- 투명 (CPU 인식 불필요)
- 자동 관리 (HW)
- 계층 구조 (L1/L2/L3)
```

**캐시의 핵심 특징:**

1. **속도 향상**: 메모리 지연 시간 90%+ 감소
2. **투명성**: CPU는 캐시 존재를 인식하지 않아도 됨
3. **자동 관리**: 하드웨어가 자동으로 데이터 관리
4. **계층 구조**: L1 → L2 → L3 → Memory

```
메모리 계층:
L1 Cache: < 1ns, 32-64KB
L2 Cache: 3-10ns, 256KB-8MB
L3 Cache: 10-20ns, 8-64MB
Main Memory: 50-100ns, 4-64GB
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### 캐시 라인 구조

```
캐시 라인 (Cache Line) 구조:

메인 메모리:
[Block 0] [Block 1] [Block 2] ...

캐시:
┌────────┬────────┬────────┐
│ Valid  │ Tag    │ Data   │
├────────┼────────┼────────┤
│ 1비트  │ 20비트  │ 32비트 │
└────────┴────────┴────────┘

구성 요소:
1. Valid Bit: 데이터 유효성
   - 1: 유효한 데이터
   - 0: 빈 캐시 라인

2. Tag Block: 블록 식별
   - 상위 주소 비트

3. Data Block: 실제 데이터
   - 일반적으로 32-256바이트

주소 분해:
CPU Address[31:0]
├── Tag [31:12]
├── Index [11:5]  (Set 선택)
└── Offset [4:0]  (바이트 선택)
```

### 매핑 방식

```
1. Direct Mapped (직접 매핑):

메인 메모리 Block 0 ──→ Cache Set 0, Way 0
메인 메모리 Block 1 ──→ Cache Set 1, Way 0
메인 메모리 Block N ──→ Cache Set N mod S, Way 0

장점:
- 단순한 구조
- 빠른 검색
- 적은 하드웨어

단점:
- Conflict Miss 많음
- 낮은 Hit Rate

구조:
Set당 1개 Way
Tag 비교: 1회
```

```
2. Fully Associative (완전 연관 매핑):

메인 메모리 Block 0 ──→ Cache Set 0, Way 0~N (아무 곳이나)
메인 메모리 Block 1 ──→ Cache Set 0, Way 0~N (아무 곳이나)

장점:
- 가장 높은 Hit Rate
- Conflict Miss 없음

단점:
- 복잡한 구조
- 느린 검색 (병렬 Tag 비교 필요)
- 큰 하드웨어

구조:
1개 Set, N개 Way
Tag 비교: N회 (병렬)
```

```
3. Set Associative (세트 연관 매핑):

메인 메모리 Block 0 ──→ Cache Set 0, Way 0~K
메인 메모리 Block 1 ──→ Cache Set 1, Way 0~K

장점:
- Direct와 Fully의 절충
- 높은 Hit Rate
- 합리적인 하드웨어

단점:
- 중간 복잡도
- 중간 지연

구조:
S개 Set, K개 Way/Set
Tag 비교: K회 (병렬)
```

### 캐시 동작

```
Read 동작:

1. CPU Address 입력
2. Index로 Set 선택
3. Set 내 모든 Way의 Tag 병렬 비교
4. Tag Match + Valid=1 → Hit
   - Data[Offset] → CPU
5. Match 없음 → Miss
   - 메모리에서 Block 가져오기
   - 캐시에 저장
   - CPU에 전달

타이밍:
Hit: ~1 클럭
Miss: ~10-100 클럭
```

### 쓰기 정책

```
Write 정책:

1. Write Through:
   - 캐시와 메모리 동시에 쓰기
   - 항상 일관성 유지
   - 느린 쓰기

2. Write Back:
   - 캐시만 쓰기
   - Dirty Bit 설정
   - Eviction 시 메모리에 쓰기
   - 빠른 쓰기

Write Allocate:
- Miss 시 캐시에 가져오기

No-Write Allocate:
- Miss 시 메모리에만 쓰기

조합:
- Write Through + No-Write Allocate
- Write Back + Write Allocate (일반적)
```

### 교체 정책

```
Replacement Policy:

1. LRU (Least Recently Used):
   - 가장 오랫동안 사용 안 한 라인 교체
   - 구현: Counter나 Bit

2. FIFO (First In First Out):
   - 가장 먼저 들어온 라인 교체
   - 단순하지만 비효율적

3. Random:
   - 무작위 교체
   - 하드웨어 단순

4. Pseudo-LRU:
   - 근사 LRU
   - 하드웨어 효율적
```

### 캐시 코어언스

```
Cache Coherence (다중 코어):

문제:
- Core 0이 Cache[0] 쓰기
- Core 1이 Cache[0] 읽기
- 데이터 불일치

해결:

1. Write Invalidate:
   - Core 0 쓰기 시 다른 Core의 캐시 무효화
   - 다른 Core가 다시 읽을 때 메모리 참조

2. Write Update (Broadcast):
   - Core 0 쓰기 시 모든 Core에 전파
   - 즉시 일관성

프로토콜:
- MESI: Modified, Exclusive, Shared, Invalid
- MOESI: + Owner
```

## Ⅲ. 융합 비교

### 매핑 방식 비교

| 방식 | Hit Rate | 검색 속도 | 하드웨어 | 응용 |
|------|----------|----------|----------|------|
| Direct | 낮음 | 빠름 | 작음 | L1 |
| 2-Way | 중간 | 중간 | 중간 | L1/L2 |
| 4-Way | 높음 | 중간 | 중간 | L2/L3 |
| 8-Way | 매우 높음 | 느림 | 큼 | L3 |
| Full | 가장 높음 | 매우 느림 | 매우 큼 | TLB |

### 캐시 레벨

| 레벨 | 크기 | 속도 | 구조 | 위치 |
|------|------|------|------|------|
| L1 I | 16-64KB | < 1ns | Direct/4-Way | Core 내부 |
| L1 D | 16-64KB | < 1ns | Direct/4-Way | Core 내부 |
| L2 | 256KB-8MB | 3-10ns | 8-Way | Core 근처 |
| L3 | 8-64MB | 10-20ns | 16-Way | Chip 공유 |

### Miss 종류

| 종류 | 원인 | 해결 |
|------|------|------|
| Compulsory | 첫 액세스 | Prefetch |
| Capacity | 캐시 작음 | 크기 증가 |
| Conflict | Direct Map | Associativity 증가 |

## Ⅳ. 실무 적용 및 기술사적 판단

### L1 캐시 설계

```
L1 Instruction Cache:

구조:
- 32KB
- 64B Line
- 4-Way Set Associative
- 512 Sets
- Virtually Indexed Physically Tagged

주소 변환:
VA[31:0]
├── Tag [31:15]
├── Index [14:6]
└── Offset [5:0]

Index로 Set 선택
Tag로 물리 주소 비교
장점: TLB 없이도 빠름

성능:
- Hit Rate: ~95%
- Hit Time: 1-2 클럭
- Miss Penalty: ~10 클럭
```

### Victim Cache

```
Victim Cache:

개념:
- L1에서 Eviction된 라인 저장
- 작은 Fully Associative Cache
- L1과 L2 사이

구조:
- 4-8 엔트리
- Fully Associative
- LRU

장점:
- Conflict Miss 감소
- L1 Hit Rate 향상
- 작은 비용

예:
L1 (Direct) → Victim (4-way) → L2
```

### Prefetching

```
Prefetching:

개념:
- 미리 데이터를 캐시로 가져오기
- Miss 감소

종류:

1. Sequential Prefetch:
   - 다음 Block 예측
   - 단순하지만 효과적

2. Strided Prefetch:
   - 일정 간격 액세스 예측
   - Array 탐색

3. Stream Buffer:
   - 여러 Block 예측
   - Sequential + Lookahead

효과:
- Miss Rate 50~80% 감소
- Overhead: 메모리 대역폭
```

### NI Cache (Non-Inclusive)

```
NI Cache (Non-Inclusive):

개념:
- L3가 L1/L2의 일부를 포함하지 않음
- 중복 데이터 제거
- 효율적 공간 활용

종류:
1. Inclusive: L3 ⊇ L2 ⊇ L1
2. Exclusive: L3 ∩ (L2 ∪ L1) = Ø
3. Non-Inclusive: 제약 없음

장점:
- 용량 증가
- Hit Rate 향상

단점:
- Coherence 복잡
- snooping 비용
```

## Ⅴ. 기대효과 및 결론

캐시는 메모리 병목을 해결한다. 지역성을 활용해 90%+ Hit Rate를 달성한다.

## 📌 관련 개념 맵

```
캐시 메모리
├── 구조
│   ├── Cache Line (Tag + Valid + Data)
│   ├── Set (Index로 선택)
│   └── Way (Set 내 라인)
├── 매핑
│   ├── Direct Mapped (1-Way)
│   ├── Set Associative (K-Way)
│   └── Fully Associative (N-Way)
├── 정책
│   ├── Write (Through vs Back)
│   ├── Replace (LRU/FIFO/Random)
│   └── Allocate (Write vs No-Write)
├── Miss
│   ├── Compulsory (Cold)
│   ├── Capacity
│   └── Conflict
└── 레벨
    ├── L1 (빠름, 작음)
    ├── L2 (중간)
    └── L3 (느림, 큼)
```

## 👶 어린이를 위한 3줄 비유 설명

1. 캐시는 가방 같아요. 자주 쓰는 물건을 가방에 넣어두면 서랍(메모리)에서 찾을 필요가 없어서 바로 쓸 수 있어요
2. L1 캐시는 주머니, L2는 가방, L3은 서류 가방 같아요. 주머니가 제일 빠르지만 적게 넣을 수 있고, 서류 가방은 느리지만 많이 넣을 수 있어요
3. 지역성은 "방금 쓴 물건을 또 쓰고", "옆에 있는 물건도 같이 쓴다"는 원칙이에요. 이 원칙으로 미리 무엇을 캐시에 넣을지 예측해요

```python
# 캐시 메모리 시뮬레이션

from typing import List, Dict, Tuple
from enum import Enum


class CacheLine:
    """캐시 라인"""

    def __init__(self, block_size: int):
        self.valid = False
        self.dirty = False
        self.tag = 0
        self.data = [0] * block_size
        self.last_access = 0


class Cache:
    """캐시 메모리"""

    def __init__(self, size: int, block_size: int, associativity: int):
        """
        캐시 초기화

        Args:
            size: 캐시 크기 (바이트)
            block_size: 블록 크기 (바이트)
            associativity: 연관도 (1=Direct, K=K-Way)
        """
        self.size = size
        self.block_size = block_size
        self.associativity = associativity
        self.num_sets = size // (block_size * associativity)
        self.offset_bits = (block_size - 1).bit_length()
        self.index_bits = (self.num_sets - 1).bit_length()

        # 캐시: [sets][ways]
        self.cache: List[List[CacheLine]] = [
            [CacheLine(block_size) for _ in range(associativity)]
            for _ in range(self.num_sets)
        ]

        self.access_count = 0
        self.hit_count = 0
        self.miss_count = 0

    def _get_index(self, address: int) -> int:
        """인덱스 추출"""
        return (address >> self.offset_bits) & (self.num_sets - 1)

    def _get_tag(self, address: int) -> int:
        """태그 추출"""
        return address >> (self.offset_bits + self.index_bits)

    def _find_line(self, index: int, tag: int) -> Tuple[bool, int]:
        """라인 찾기 (Hit/Miss)"""
        for way in range(self.associativity):
            line = self.cache[index][way]
            if line.valid and line.tag == tag:
                return True, way
        return False, -1

    def _find_victim(self, index: int) -> int:
        """교체 대상 찾기 (LRU)"""
        victim_way = 0
        oldest_access = self.cache[index][0].last_access

        for way in range(1, self.associativity):
            line = self.cache[index][way]
            if not line.valid:
                return way
            if line.last_access < oldest_access:
                oldest_access = line.last_access
                victim_way = way

        return victim_way

    def read(self, address: int, memory: List[int]) -> int:
        """읽기"""
        self.access_count += 1

        index = self._get_index(address)
        tag = self._get_tag(address)

        hit, way = self._find_line(index, tag)

        if hit:
            # Cache Hit
            self.hit_count += 1
            line = self.cache[index][way]
            line.last_access = self.access_count
            offset = address & (self.block_size - 1)
            return line.data[offset]
        else:
            # Cache Miss
            self.miss_count += 1

            # 메모리에서 블록 가져오기
            block_addr = address & ~(self.block_size - 1)
            new_data = []
            for i in range(self.block_size):
                if block_addr + i < len(memory):
                    new_data.append(memory[block_addr + i])
                else:
                    new_data.append(0)

            # 교체 대상 찾기
            victim_way = self._find_victim(index)

            # 캐시에 저장
            line = self.cache[index][victim_way]
            line.valid = True
            line.dirty = False
            line.tag = tag
            line.data = new_data
            line.last_access = self.access_count

            offset = address & (self.block_size - 1)
            return line.data[offset]

    def write(self, address: int, data: int, memory: List[int]):
        """쓰기 (Write-Back)"""
        self.access_count += 1

        index = self._get_index(address)
        tag = self._get_tag(address)

        hit, way = self._find_line(index, tag)

        if hit:
            # Cache Hit
            self.hit_count += 1
            line = self.cache[index][way]
            line.last_access = self.access_count
            line.dirty = True
            offset = address & (self.block_size - 1)
            line.data[offset] = data
        else:
            # Cache Miss
            self.miss_count += 1

            # 메모리에서 블록 가져오기
            block_addr = address & ~(self.block_size - 1)
            new_data = []
            for i in range(self.block_size):
                if block_addr + i < len(memory):
                    new_data.append(memory[block_addr + i])
                else:
                    new_data.append(0)

            # 교체 대상 찾기
            victim_way = self._find_victim(index)

            # 캐시에 저장
            line = self.cache[index][victim_way]
            line.valid = True
            line.dirty = True
            line.tag = tag
            line.data = new_data
            line.last_access = self.access_count

            offset = address & (self.block_size - 1)
            line.data[offset] = data

    def hit_rate(self) -> float:
        """Hit Rate"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0

    def stats(self) -> Dict:
        """통계"""
        return {
            "accesses": self.access_count,
            "hits": self.hit_count,
            "misses": self.miss_count,
            "hit_rate": self.hit_rate()
        }


def demonstration():
    """캐시 데모"""
    print("=" * 60)
    print("캐시 메모리 (Cache Memory) 데모")
    print("=" * 60)

    # Direct Mapped Cache
    print("\n[Direct Mapped Cache]")
    direct_cache = Cache(size=256, block_size=16, associativity=1)
    memory = list(range(256))

    print("액세스:")
    for addr in [0, 16, 32, 48, 0, 16]:
        data = direct_cache.read(addr, memory)
        print(f"  Address {addr:3d}: Data = {data:3d}")

    print(f"\n통계: {direct_cache.stats()}")

    # 4-Way Set Associative
    print("\n[4-Way Set Associative Cache]")
    assoc_cache = Cache(size=256, block_size=16, associativity=4)

    print("액세스:")
    for addr in [0, 16, 32, 48, 0, 16]:
        data = assoc_cache.read(addr, memory)
        print(f"  Address {addr:3d}: Data = {data:3d}")

    print(f"\n통계: {assoc_cache.stats()}")

    # Sequential 액세스 (좋은 지역성)
    print("\n[Sequential 액세스 (좋은 지역성)]")
    cache1 = Cache(size=256, block_size=16, associativity=4)
    memory1 = list(range(1024))

    for addr in range(256):
        cache1.read(addr, memory1)

    print(f"Hit Rate: {cache1.hit_rate():.1%}")

    # Random 액세스 (나쁜 지역성)
    print("\n[Random 액세스 (나쁜 지역성)]")
    cache2 = Cache(size=256, block_size=16, associativity=4)
    import random
    random.seed(42)

    for _ in range(256):
        addr = random.randint(0, 1000)
        cache2.read(addr, memory1)

    print(f"Hit Rate: {cache2.hit_rate():.1%}")

    # 매핑 방식 비교
    print("\n[매핑 방식 비교]")
    import random
    random.seed(42)

    configs = [
        ("Direct", 1),
        ("2-Way", 2),
        ("4-Way", 4),
        ("8-Way", 8)
    ]

    test_addrs = [random.randint(0, 500) for _ in range(1000)]

    for name, assoc in configs:
        cache = Cache(size=512, block_size=16, associativity=assoc)
        for addr in test_addrs:
            cache.read(addr, memory1)
        print(f"{name}: Hit Rate = {cache.hit_rate():.1%}")

    # Write-Back 시뮬레이션
    print("\n[Write-Back 정책]")
    cache3 = Cache(size=256, block_size=16, associativity=4)
    memory3 = [0] * 256

    # 쓰기
    cache3.write(0, 100, memory3)
    cache3.write(1, 101, memory3)
    cache3.write(16, 200, memory3)

    # 읽기 (캐시에서)
    data0 = cache3.read(0, memory3)
    data1 = cache3.read(1, memory3)
    data16 = cache3.read(16, memory3)

    print(f"Address 0: {data0} (Cached)")
    print(f"Address 1: {data1} (Cached)")
    print(f"Address 16: {data16} (Cached)")
    print(f"Memory[0]: {memory3[0]} (Still 0, not written back)")

    # Multi-level Cache
    print("\n[Multi-level Cache]")
    l1_cache = Cache(size=64, block_size=8, associativity=2)
    l2_cache = Cache(size=256, block_size=16, associativity=4)
    memory4 = list(range(1024))

    l1_hits = 0
    l2_hits = 0
    misses = 0

    for addr in range(100):
        # L1 확인
        index = (addr >> 3) & (l1_cache.num_sets - 1)
        tag = addr >> (3 + l1_cache.index_bits)

        hit, _ = l1_cache._find_line(index, tag)
        if hit:
            l1_hits += 1
            l1_cache.read(addr, memory4)
        else:
            # L2 확인
            l1_cache.read(addr, memory4)  # L1 miss로 처리

            index2 = (addr >> 4) & (l2_cache.num_sets - 1)
            tag2 = addr >> (4 + l2_cache.index_bits)

            hit2, _ = l2_cache._find_line(index2, tag2)
            if hit2:
                l2_hits += 1
            else:
                misses += 1
                l2_cache.read(addr, memory4)

    total = l1_hits + l2_hits + misses
    print(f"L1 Hits: {l1_hits} ({l1_hits/total:.1%})")
    print(f"L2 Hits: {l2_hits} ({l2_hits/total:.1%})")
    print(f"Misses: {misses} ({misses/total:.1%})")


if __name__ == "__main__":
    demonstration()
```
