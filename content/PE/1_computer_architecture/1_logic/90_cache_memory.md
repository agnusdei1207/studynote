+++
title = "캐시 메모리 (Cache Memory)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "메모리"]
draft = false
+++

# 캐시 메모리 (Cache Memory)

## 핵심 인사이트 (3줄 요약)
1. 캐시(Cache)는 CPU와 메모리 사이의 고속 버퍼로, 지역성(Locality) 원리를 활용해 메모리 접근 지연을 줄인다
2. 기술사시험에서는 Mapping(Direct, Associative, Set), Replacement(LRU, FIFO), Write Policy(Write-Through, Write-Back)가 핵심이다
3. Hit Ratio를 높이는 것이 목표이며, Cache Size, Block Size, Associativity가 성능을 결정한다

## Ⅰ. 개요 (500자 이상)

캐시 메모리(Cache Memory)는 **CPU의 빠른 처리 속도와 상대적으로 느린 메모리 접근 속도의 차이를 해소하기 위한 고속 버퍼 메모리**다. 자주 사용하는 데이터를 미리 저장해 두어 CPU가 메모리에 직접 접근하는 횟수를 줄인다.

```
캐시 기본 개념:
위치: CPU와 Main Memory 사이
속도: CPU > Cache >> Memory
크기: 작음 (KB ~ MB)
목적: 메모리 Access Time 감소

메모리 계층:
CPU Registers (< 1ns)
L1 Cache (~1ns, 32-64KB)
L2 Cache (~3ns, 256KB-2MB)
L3 Cache (~10ns, 8-64MB)
Main Memory (~50-100ns, GB)

지역성 (Locality):
1. 시간적 지역성 (Temporal):
   - 최근 접근한 데이터를 다시 접근

2. 공간적 지역성 (Spatial):
   - 인접한 데이터 접근 가능

3. 순차적 지역성 (Sequential):
   - 순차적인 접근 패턴
```

**캐시의 핵심 원리:**

```
Hit: 찾는 데이터가 캐시에 있음
Miss: 찾는 데이터가 캐시에 없음

Hit Ratio = Hit / (Hit + Miss)
Average Access Time = Hit Time + Miss Rate × Miss Penalty

예:
Hit Time = 1 cycle
Miss Penalty = 100 cycles
Hit Ratio = 95%

AAT = 1 + 0.05 × 100 = 1 + 5 = 6 cycles
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Mapping Techniques

```
캐시 매핑 방식:

1. Direct Mapping (직접 매핑):
   각 메모리 블록이 정확히 하나의 캐시 라인에 매핑

   구조:
   ┌────────────────────────────┐
   │ Tag │ Line │ Valid │ Dirty │
   └────────────────────────────┘

   매핑:
   Cache Line = (Block Address) mod (Number of Lines)
   Tag = Block Address / Number of Lines

   장점: 단순, 빠름
   단점: Conflict Miss 빈번

2. Fully Associative (완전 연관 매핑):
   메모리 블록이 어느 캐시 라인에나 매핑 가능

   매핑:
   어디든 가능 (Tag 전체 비교)

   장점: 유연함, Conflict Miss 없음
   단점: 복잡, 느림 (병렬 비교 필요)

3. Set Associative (세트 연관 매핑):
   Direct와 Associative의 절충

   구조:
   N-way Set Associative
   각 Set이 N개의 Line 보유

   매핑:
   Set = (Block Address) mod (Number of Sets)
   Line = Set 내 아무 곳이나

   예: 4-way Set Associative
   ┌───────┬───────┬───────┬───────┐
   │ Set 0 │ Line1 │ Line2 │ Line3 │ Line4 │
   ├───────┼───────┼───────┼───────┤
   │ Set 1 │ Line1 │ Line2 │ Line3 │ Line4 │
   └───────┴───────┴───────┴───────┘
```

### Cache Address Structure

```
주소 구조:

Direct Mapping:
┌─────────┬──────────────┬──────────┐
│  Tag    │   Line       │  Word    │
└─────────┴──────────────┴──────────┘

Tag: 고유 식별자
Line: 캐시 라인 번호
Word: 블록 내 단어

Set Associative:
┌─────────┬──────────────┬──────────┬──────────┐
│  Tag    │    Set       │  Word    │  Byte    │
└─────────┴──────────────┴──────────┴──────────┘

Fully Associative:
┌─────────┬──────────────────────┬──────────┐
│  Tag    │       Word           │  Byte    │
└─────────┴──────────────────────┴──────────┘

예 (32-bit 주소, 4KB Direct Cache):
Cache Size: 4KB = 4096B
Block Size: 16B
Number of Lines: 4096 / 16 = 256

Word: 4 bits (16 words per block)
Line: 8 bits (256 lines)
Tag: 20 bits (32 - 8 - 4)
```

### Replacement Policy

```
교체 정책 (Miss 시 교체 대상 선정):

1. LRU (Least Recently Used):
   가장 오랫동안 사용하지 않은 것

   구현:
   - 사용 순서 추적
   - Counter 또는 Reference Bit 사용

   2-way 예:
   ┌───────┬─────────┐
   │ Line  │ Used    │
   ├───────┼─────────┤
   │   A   │ Recently│ ← 선정 안 됨
   │   B   │ Old     │ ← 교체 대상
   └───────┴─────────┘

2. FIFO (First In First Out):
   가장 먼저 들어온 것

   구현:
   - Queue 구조
   - 단순한 구현

   문제:
   - 자주 사용하는 것도 교체 가능

3. Random:
   무작위 선택

   장점: 하드웨어 단순
   단점: 성능 불균형

4. LFU (Least Frequently Used):
   가장 적게 사용된 것

   구현:
   - 접근 횟수 추적

5. Optimal (Belady's Algorithm):
   미래를 알고 있다는 가정
   이론적 하한선
   실제 구현 불가
```

### Write Policy

```
쓰기 정책:

1. Write-Through (즉시 쓰기):
   캐시와 메모리에 동시에 기록

   장점:
   - 메모리 항상 최신
   - 일관성 유지 쉬움

   단점:
   - 느린 메모리 쓰기
   - Bus Traffic 많음

2. Write-Back (지연 쓰기):
   캐시에만 기록, 메모리는 추후 기록

   장점:
   - 빠른 쓰기
   - Bus Traffic 적음

   단점:
   - 메모리 불일치
   - Dirty Bit 필요

   Dirty Bit:
   - 1: 캐시가 수정됨
   - 0: 캐시가 메모리와 동일

3. Write-Allocate:
   Miss 시 블록을 캐시로 가져온 후 기록

4. No-Write-Allocate:
   Miss 시 메모리에 직접 기록

일반적 조합:
- Write-Through + No-Write-Allocate
- Write-Back + Write-Allocate
```

### Cache Performance

```
성능 지표:

1. Hit Ratio (h):
   h = Hits / (Hits + Misses)

2. Miss Ratio (m):
   m = 1 - h

3. Average Access Time (AAT):
   AAT = Hit Time + m × Miss Penalty

   예:
   L1: Hit Time = 1ns, Miss Rate = 5%
   L2: Hit Time = 10ns, Miss Rate = 20%
   Memory: 100ns

   AAT = 1 + 0.05 × (10 + 0.2 × 100)
       = 1 + 0.05 × 30
       = 1 + 1.5 = 2.5ns

4. AMAT (Average Memory Access Time):
   AAT과 동일

Multilevel Cache (L1, L2, L3):
L1 Miss → L2 확인 → L3 확인 → Memory

Global vs Local Miss Rate:
- Local: 해당 캐시의 Miss Rate
- Global: 전체 CPU 요청의 Miss Rate
```

### Types of Cache Misses

```
캐시 Miss 유형 (4C):

1. Compulsory Miss (Cold Start):
   - 첫 접근으로 인한 Miss
   - 필연적 발생
   - 해결: Prefetching

2. Capacity Miss:
   - 캐시 크기 부족
   - 해결: 캐시 크기 증가

3. Conflict Miss:
   - 매핑 충돌 (Direct Mapping)
   - 해결: Associativity 증가

4. Coherence Miss:
   - Multiprocessor에서 다른 CPU가 수정
   - 해결: Cache Coherence Protocol

Miss 분석:
Total Miss = Compulsory + Capacity + Conflict + Coherence
```

## Ⅲ. 융합 비교

### Mapping 비교

| 방식 | Hit Time | Miss Rate | 복잡도 | 용도 |
|------|----------|-----------|--------|------|
| Direct | 빠름 | 높음 | 낮음 | L1 |
| Set-Way | 중간 | 중간 | 중간 | L1/L2 |
| Fully | 느림 | 낮음 | 높음 | L2/L3 |

### Replacement 비교

| 정책 | Hit Rate | 구현 | 용도 |
|------|----------|------|------|
| LRU | 높음 | 복잡 | 일반 |
| FIFO | 중간 | 단순 | 소형 |
| Random | 낮음 | 매우 단순 | 특수 |

### Write Policy 비교

| 정책 | 쓰기 속도 | 일관성 | 용도 |
|------|-----------|--------|------|
| Write-Through | 느림 | 높음 | SMP |
| Write-Back | 빠름 | 낮음 | 단일 |

## Ⅳ. 실무 적용 및 기술사적 판단

### Intel Cache Hierarchy

```
Intel Core Cache:

L1 Instruction Cache:
- 32 KB
- 8-way Set Associative
- 64 Byte Line

L1 Data Cache:
- 32 KB
- 8-way Set Associative
- 64 Byte Line

L2 Unified Cache:
- 256 KB per core
- 4-way Set Associative
- 256 Byte Line

L3 Shared Cache:
- 8-64 MB
- 16-way Set Associative
- Inclusive (L3가 L1/L2 포함)

Non-Inclusive (AMD):
- L3가 L1/L2 포함 안 함
- 더 효율적
```

### ARM Cache

```
ARM Cortex Cache:

L1:
- 16-64 KB
- 4-way Set Associative
- VIPT (Virtually Indexed Physical Tag)

L2:
- 128KB - 1MB
- 8-way or 16-way

L3:
- 일부 모델에서만

특징:
- PIPT 또는 VIPT
- Parity/ECC 지원
- Cache Locking
```

### Cache Optimization

```
최적화 기법:

1. Block Size 조정:
   - 너무 크면: Capacity Miss 증가
   - 너무 작으면: Spatial Locality 손실
   - 최적: 32-128 bytes

2. Associativity 조정:
   - Direct: Conflict Miss
   - 4-way: 균형
   - 8-way+: 한계점

3. Victim Cache:
   - 교체된 블록 저장
   - 작은 Fully-Associative Cache

4. Prefetching:
   - 순차적 접근 예측
   - Hardware/Software Prefetch
   - Strided Prefetch

5. Loop Tiling:
   - Working Set 감소
   - Cache Conscious Programming
```

## Ⅴ. 기대효과 및 결론

캐시는 메모리 병목을 해결하는 핵심 기술이다. Hit Ratio를 높이고 AAT를 줄이는 설계가 중요하다.

```python
"""
캐시 시뮬레이션
Cache Memory Simulator
"""

class Cache:
    """캐시 시뮬레이션"""

    def __init__(self, size, block_size, associativity=1):
        self.size = size
        self.block_size = block_size
        self.associativity = associativity

        # 캐시 구조
        self.num_sets = (size // block_size) // associativity
        self.sets = [[{'tag': None, 'valid': False, 'dirty': False, 'data': None, 'lru': 0}
                      for _ in range(associativity)] for _ in range(self.num_sets)]

        # 통계
        self.hits = 0
        self.misses = 0

    def access(self, address):
        """메모리 접근"""
        block_addr = address // self.block_size
        set_index = block_addr % self.num_sets
        tag = block_addr // self.num_sets

        cache_set = self.sets[set_index]

        # Hit 확인
        for line in cache_set:
            if line['valid'] and line['tag'] == tag:
                self.hits += 1
                line['lru'] = self._get_lru_counter()
                return True  # Hit

        # Miss
        self.misses += 1
        self._replace(set_index, tag)
        return False  # Miss

    def _replace(self, set_index, new_tag):
        """교체 정책 (LRU)"""
        cache_set = self.sets[set_index]

        # 빈 라인 찾기
        for line in cache_set:
            if not line['valid']:
                line['tag'] = new_tag
                line['valid'] = True
                line['lru'] = self._get_lru_counter()
                return

        # LRU 교체
        lru_line = min(cache_set, key=lambda x: x['lru'])
        lru_line['tag'] = new_tag
        lru_line['valid'] = True
        lru_line['lru'] = self._get_lru_counter()

    def _get_lru_counter(self):
        """LRU 카운터"""
        return self.hits + self.misses

    def get_hit_ratio(self):
        """Hit Ratio"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0

    def get_stats(self):
        """통계"""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_ratio': self.get_hit_ratio(),
            'total_access': self.hits + self.misses
        }


def demo_cache_simulation():
    """캐시 시뮬레이션 데모"""

    print("=" * 70)
    print("Cache Memory Simulation")
    print("=" * 70)

    # Direct Mapping Cache
    print("\n### Direct Mapping Cache (4KB, 16B block)")
    cache = Cache(size=4096, block_size=16, associativity=1)

    # Sequential access
    print("Sequential Access: 0, 16, 32, ..., 1000")
    for addr in range(0, 1000, 16):
        cache.access(addr)

    print(f"Hit Ratio: {cache.get_hit_ratio():.2%}")

    # Random access
    cache2 = Cache(size=4096, block_size=16, associativity=1)
    import random
    random.seed(42)

    print("\nRandom Access: 1000 random addresses")
    for _ in range(1000):
        addr = random.randint(0, 10000) * 16
        cache2.access(addr)

    print(f"Hit Ratio: {cache2.get_hit_ratio():.2%}")


def demo_comparison():
    """비교"""

    print("\n\n" + "=" * 70)
    print("Cache Comparison")
    print("=" * 70)

    comparison = """
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Mapping Techniques                               │
    ├───────────────────┬───────────────┬───────────────┬──────────────────┤
    │                   │ Direct        │ 4-way        │ Fully            │
    ├───────────────────┼───────────────┼───────────────┼──────────────────┤
    │ Hit Time          │ 1 cycle       │ 2 cycles      │ 3+ cycles        │
    │ Miss Rate         │ High          │ Medium        │ Low             │
    │ Hardware Cost     │ Low           │ Medium        │ High            │
    │ Conflict Miss     │ Frequent      │ Less          │ None            │
    │ Usage             │ L1 I-Cache    │ L1 D-Cache    │ L2/L3           │
    └───────────────────┴───────────────┴───────────────┴──────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Multilevel Cache (Intel i7)                     │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │   L1I (32KB)           L1D (32KB)           L2 (256KB)          L3  │
    │   ┌─────────┐          ┌─────────┐          ┌─────────┐      ┌──────┐│
    │   │ 8-way   │          │ 8-way   │          │ 4-way   │      │16-way││
    │   │ 64B line│          │ 64B line│          │256B line│      │Shared││
    │   │ ~4 cycles│         │ ~4 cycles│         │ ~12 cycles│     │~40   ││
    │   │ ~95% hit│          │ ~90% hit│          │ ~80% hit │      │~50%  ││
    │   └────┬────┘          └────┬────┘          └────┬────┘      └───┬──┘│
    │        │                     │                     │               │   │
    │        └─────────────────────┴─────────────────────┴───────────────┘   │
    │                                    ↓                                 │
    │                              Main Memory                             │
    │                              (~100ns)                                │
    │                                                                     │
    │   AMAT = 4 + 0.1×(12 + 0.2×(40 + 0.5×100))                        │
    │        = 4 + 0.1×(12 + 0.2×90)                                     │
    │        = 4 + 0.1×30 = 7 cycles                                      │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
    """

    print(comparison)


if __name__ == '__main__':
    demo_cache_simulation()
    demo_comparison()
