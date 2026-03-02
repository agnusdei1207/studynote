+++
title = "다중 처리기 (Multiprocessor)"
date = 2025-02-27

[extra]
categories = "pe_exam-computer_architecture"
+++

# 다중 처리기 (Multiprocessor)

## 핵심 인사이트 (3줄 요약)
> **두 개 이상의 CPU가 공유 메모리를 통해 병렬로 작업을 처리**하는 시스템. SMP(대칭형), AMP(비대칭형), NUMA 구조로 분류. 캐시 일관성(MESI 프로토콜)과 인터커넥트가 핵심 기술이다.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 다중 처리기(Multiprocessor)는 **두 개 이상의 CPU(프로세서)가 하나의 공유 메모리 시스템에서 병렬로 작업을 처리하는 컴퓨터 아키텍처**로, 처리량(Throughput) 증대, 신뢰성(Reliability) 향상, 비용 효율성을 목적으로 한다.

> 💡 **비유**: 다중 처리기는 **"여러 요리사가 있는 주방"** 같아요. 요리사(CPU)가 여러 명이면 여러 요리를 동시에 만들 수 있죠. 하지만 냉장고(메모리)는 하나라서 서로 "이거 내 거야!" 하고 싸우지 않도록 규칙(캐시 일관성)이 필요해요!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 단일 프로세서의 한계**: 클럭 속도 향상 한계(전력/발열), 물리적 한계
2. **기술적 필요성 - 병렬 처리**: 대용량 데이터 처리, 실시간 응답, 고가용성
3. **시장/산업 요구 - 확장성**: 서버, 데이터센터에서 수평 확장(Scale-out) 필요

**핵심 목적**: **높은 처리량(Throughput)**, **신뢰성(Reliability)**, **비용 효율(Cost-effectiveness)**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **CPU 코어** | 명령어 실행 | 2~128개 이상 | 요리사 |
| **공유 메모리** | 데이터 저장/공유 | 모든 CPU 접근 | 공동 냉장고 |
| **캐시 계층** | L1/L2/L3 캐시 | L3는 공유 | 작업대 |
| **인터커넥트** | CPU 간 통신 | Bus, Crossbar, Mesh | 주방 동선 |
| **캐시 일관성** | 데이터 동기화 | MESI 프로토콜 | 사용 규칙 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    SMP (대칭형 다중 처리기) 구조                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    ┌─────────────────────┐                         │
│                    │   공유 메모리        │                         │
│                    │   (Main Memory)     │                         │
│                    └──────────┬──────────┘                         │
│                               │                                     │
│                    ┌──────────┴──────────┐                         │
│                    │   시스템 버스/       │                         │
│                    │   인터커넥트         │                         │
│                    └──────────┬──────────┘                         │
│            ┌──────────────────┼──────────────────┐                 │
│            │                  │                  │                 │
│     ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐          │
│     │   CPU 0     │   │   CPU 1     │   │   CPU 2     │          │
│     ├─────────────┤   ├─────────────┤   ├─────────────┤          │
│     │ ┌─────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │          │
│     │ │  Core   │ │   │ │  Core   │ │   │ │  Core   │ │          │
│     │ └────┬────┘ │   │ └────┬────┘ │   │ └────┬────┘ │          │
│     │      │      │   │      │      │   │      │      │          │
│     │ ┌────┴────┐ │   │ ┌────┴────┐ │   │ ┌────┴────┐ │          │
│     │ │ L1 Cache│ │   │ │ L1 Cache│ │   │ │ L1 Cache│ │          │
│     │ └────┬────┘ │   │ └────┬────┘ │   │ └────┬────┘ │          │
│     │ ┌────┴────┐ │   │ ┌────┴────┐ │   │ ┌────┴────┐ │          │
│     │ │ L2 Cache│ │   │ │ L2 Cache│ │   │ │ L2 Cache│ │          │
│     │ └────┬────┘ │   │ └────┬────┘ │   │ └────┬────┘ │          │
│     └──────┴──────┘   └──────┴──────┘   └──────┴──────┘          │
│            │                  │                  │                 │
│            └──────────────────┴──────────────────┘                 │
│                               │                                     │
│                    ┌──────────┴──────────┐                         │
│                    │   L3 캐시 (공유)    │                         │
│                    └─────────────────────┘                         │
│                                                                     │
│   특징: 모든 CPU가 동등한 권한, 하나의 OS가 관리                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    NUMA (Non-Uniform Memory Access) 구조            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │                     인터커넥트 (Interconnect)                │ │
│   └───────────────────────────┬──────────────────────────────────┘ │
│            ┌──────────────────┼──────────────────┐                 │
│            │                  │                  │                 │
│     ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐          │
│     │   Node 0    │   │   Node 1    │   │   Node 2    │          │
│     ├─────────────┤   ├─────────────┤   ├─────────────┤          │
│     │ CPU 0, 1   │   │ CPU 2, 3    │   │ CPU 4, 5    │          │
│     │ L3 Cache   │   │ L3 Cache    │   │ L3 Cache    │          │
│     │ 로컬 메모리│   │ 로컬 메모리 │   │ 로컬 메모리 │          │
│     │   (Fast)   │   │   (Fast)    │   │   (Fast)    │          │
│     └─────────────┘   └─────────────┘   └─────────────┘          │
│            │                  │                  │                 │
│            └──────────────────┴──────────────────┘                 │
│                      원격 메모리 접근 (Slow)                       │
│                                                                     │
│   특징: 로컬 메모리는 빠름(Fast), 원격 메모리는 느림(Slow)         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    MESI 캐시 일관성 프로토콜                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   상태 정의:                                                       │
│   ┌────────────────────────────────────────────────────────────┐   │
│   │ M (Modified)  : 수정됨, 이 캐시에만 있는 유일한 복사본    │   │
│   │ E (Exclusive) : 혼자 소유, 수정 안 됨, 메모리와 동일      │   │
│   │ S (Shared)    : 여러 캐시가 공유, 수정 안 됨              │   │
│   │ I (Invalid)   : 무효, 사용 불가                           │   │
│   └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│   상태 전이 다이어그램:                                            │
│                                                                     │
│              ┌─────────────────────────────────┐                   │
│              │           Read Hit              │                   │
│              │    (자신이 S/E/M인 경우)        │                   │
│              │          상태 유지              │                   │
│              └─────────────────────────────────┘                   │
│                         ↑                    │                     │
│                         │                    │                     │
│   ┌──────────┐    Read │                    │ Write    ┌───────┐  │
│   │          │←────────┤                    ├─────────→│       │  │
│   │ Invalid  │         │                    │          │Modified│  │
│   │   (I)    │         │                    │          │  (M)  │  │
│   └────┬─────┘         │                    │          └───┬───┘  │
│        │               │                    │              │       │
│        │ Read          │                    │              │       │
│        │ (다른 캐시    │                    │              │       │
│        │  없음)        │                    │              │       │
│        ↓               │                    │              │       │
│   ┌──────────┐         │                    │         ┌────┴───┐  │
│   │Exclusive │←────────┘                    └────────→│Shared  │  │
│   │   (E)    │   Read (다른 캐시 있음)               │  (S)   │  │
│   └──────────┘                                        └────────┘  │
│        │                                                   ↑       │
│        │ Write (다른 캐시 무효화)                          │       │
│        └───────────────────────────────────────────────────┘       │
│                                                                     │
│   메시지 종류:                                                     │
│   - BusRd: 버스 읽기 요청                                          │
│   - BusRdX: 버스 읽기 + 배타적 소유 요청                           │
│   - Flush: 캐시에서 메모리로 데이터 쓰기                           │
│   - Invalidate: 다른 캐시의 라인 무효화                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① CPU 요청 → ② 캐시 조회 → ③ Hit/Miss 판정 → ④ 일관성 유지 → ⑤ 데이터 반환
```

- **1단계 - CPU 요청**: CPU가 메모리 읽기/쓰기 요청
- **2단계 - 캐시 조회**: L1 → L2 → L3 순서로 캐시 검색
- **3단계 - Hit/Miss 판정**: 캐시에 있으면 Hit, 없으면 Miss
- **4단계 - 일관성 유지**: MESI 프로토콜로 다른 캐시와 동기화
- **5단계 - 데이터 반환**: 요청한 CPU에 데이터 제공

**핵심 알고리즘/공식** (해당 시 필수):

```
[암달의 법칙 (Amdahl's Law)]
병렬 처리에서의 최대 성능 향상 계산

Speedup = 1 / ((1 - P) + P/N)

P: 병렬화 가능한 비율 (0~1)
N: 프로세서 수

예: 80% 병렬화(P=0.8), 10개 프로세서(N=10)
Speedup = 1 / (0.2 + 0.08) = 1/0.28 ≈ 3.57배

결론: 아무리 프로세서를 늘려도 직렬 부분이 병목!

[구스타프손의 법칙 (Gustafson's Law)]
문제 크기를 키우면서 병렬화

Scaled Speedup = N - (1 - P) × (N - 1)

P: 병렬화 비율
N: 프로세서 수

예: 95% 병렬화(P=0.95), 100개 프로세서
Scaled Speedup = 100 - 0.05 × 99 = 95.05배

[캐시 일관성 비용]
Coherence Miss Rate ∝ 프로세서 수 × 공유 데이터 비율

False Sharing 문제:
- 서로 다른 변수가 같은 캐시 라인에 있을 때
- 불필요한 캐시 무효화 발생
- 해결: 패딩으로 변수 분리

[SMP vs NUMA 메모리 접근 시간]
SMP: 모든 메모리 접근 시간 동일 (Uniform)
NUMA:
- 로컬 메모리: ~100ns
- 원격 메모리: ~300ns (3배 느림)
- 최적화: 데이터를 접근하는 CPU 근처에 배치
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum, auto
import threading
import time
from collections import defaultdict

class CacheState(Enum):
    """MESI 캐시 상태"""
    MODIFIED = "M"
    EXCLUSIVE = "E"
    SHARED = "S"
    INVALID = "I"

@dataclass
class CacheLine:
    """캐시 라인"""
    address: int
    data: int
    state: CacheState = CacheState.INVALID

@dataclass
class CacheStats:
    """캐시 통계"""
    hits: int = 0
    misses: int = 0
    reads: int = 0
    writes: int = 0
    invalidations: int = 0
    write_backs: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

class Cache:
    """개별 CPU 캐시"""

    def __init__(self, cpu_id: int, size: int = 16):
        self.cpu_id = cpu_id
        self.size = size
        self.lines: Dict[int, CacheLine] = {}  # address -> CacheLine
        self.stats = CacheStats()
        self.bus = None  # Bus reference

    def read(self, address: int) -> Tuple[int, bool]:
        """캐시 읽기"""
        self.stats.reads += 1

        if address in self.lines and self.lines[address].state != CacheState.INVALID:
            # Cache Hit
            self.stats.hits += 1
            return self.lines[address].data, True

        # Cache Miss
        self.stats.misses += 1
        return 0, False

    def write(self, address: int, data: int) -> None:
        """캐시 쓰기"""
        self.stats.writes += 1

        if address in self.lines:
            line = self.lines[address]
            line.data = data
            line.state = CacheState.MODIFIED
            # 다른 캐시 무효화
            if self.bus:
                self.bus.invalidate(self.cpu_id, address)
        else:
            # 캐시 미스 → 쓰기 할당
            self.lines[address] = CacheLine(address, data, CacheState.MODIFIED)
            if self.bus:
                self.bus.invalidate(self.cpu_id, address)

    def get_state(self, address: int) -> CacheState:
        """캐시 상태 조회"""
        if address in self.lines:
            return self.lines[address].state
        return CacheState.INVALID

    def set_state(self, address: int, state: CacheState) -> None:
        """캐시 상태 설정"""
        if address in self.lines:
            self.lines[address].state = state
            if state == CacheState.INVALID:
                self.stats.invalidations += 1

    def flush(self, address: int) -> int:
        """캐시에서 메모리로 쓰기"""
        if address in self.lines:
            line = self.lines[address]
            if line.state == CacheState.MODIFIED:
                self.stats.write_backs += 1
                return line.data
        return 0

class Bus:
    """시스템 버스 (캐시 일관성 관리)"""

    def __init__(self, memory: 'SharedMemory'):
        self.caches: List[Cache] = []
        self.memory = memory

    def register_cache(self, cache: Cache) -> None:
        """캐시 등록"""
        self.caches.append(cache)
        cache.bus = self

    def read_from_memory(self, address: int) -> int:
        """메모리에서 읽기"""
        return self.memory.read(address)

    def write_to_memory(self, address: int, data: int) -> None:
        """메모리에 쓰기"""
        self.memory.write(address, data)

    def invalidate(self, source_cpu: int, address: int) -> None:
        """다른 캐시 무효화"""
        for cache in self.caches:
            if cache.cpu_id != source_cpu:
                cache.set_state(address, CacheState.INVALID)

    def check_shared(self, address: int) -> bool:
        """다른 캐시에 공유 여부 확인"""
        for cache in self.caches:
            state = cache.get_state(address)
            if state in (CacheState.SHARED, CacheState.EXCLUSIVE,
                         CacheState.MODIFIED):
                return True
        return False

    def get_owner(self, address: int) -> Optional[int]:
        """M 상태인 캐시 찾기"""
        for cache in self.caches:
            if cache.get_state(address) == CacheState.MODIFIED:
                return cache.cpu_id
        return None

class SharedMemory:
    """공유 메모리"""

    def __init__(self, size: int = 1024):
        self.data: Dict[int, int] = defaultdict(int)

    def read(self, address: int) -> int:
        return self.data[address]

    def write(self, address: int, value: int) -> None:
        self.data[address] = value

class MESIController:
    """MESI 프로토콜 컨트롤러"""

    def __init__(self, cache: Cache, bus: Bus):
        self.cache = cache
        self.bus = bus

    def read_request(self, address: int) -> int:
        """읽기 요청 처리"""
        data, hit = self.cache.read(address)

        if hit:
            # Hit: 상태 유지
            return data

        # Miss: 메모리 또는 다른 캐시에서 가져오기
        owner = self.bus.get_owner(address)
        if owner is not None:
            # 다른 캐시에서 가져오기 (Shared 상태)
            data = self._fetch_from_cache(owner, address)
            self.cache.lines[address] = CacheLine(address, data, CacheState.SHARED)
            # 원래 소유자도 Shared로 변경
            self._set_shared(owner, address)
        else:
            # 메모리에서 가져오기
            data = self.bus.read_from_memory(address)
            shared = self.bus.check_shared(address)
            state = CacheState.SHARED if shared else CacheState.EXCLUSIVE
            self.cache.lines[address] = CacheLine(address, data, state)

        return data

    def write_request(self, address: int, data: int) -> None:
        """쓰기 요청 처리"""
        state = self.cache.get_state(address)

        if state == CacheState.MODIFIED:
            # M 상태: 바로 쓰기
            self.cache.write(address, data)
        elif state == CacheState.EXCLUSIVE:
            # E 상태: M로 변경 후 쓰기
            self.cache.lines[address].state = CacheState.MODIFIED
            self.cache.write(address, data)
        else:
            # S, I 상태: 쓰기 전 무효화
            self.cache.write(address, data)

    def _fetch_from_cache(self, cpu_id: int, address: int) -> int:
        """다른 캐시에서 데이터 가져오기"""
        for cache in self.bus.caches:
            if cache.cpu_id == cpu_id:
                return cache.lines[address].data
        return 0

    def _set_shared(self, cpu_id: int, address: int) -> None:
        """다른 캐시를 Shared 상태로 변경"""
        for cache in self.bus.caches:
            if cache.cpu_id == cpu_id:
                cache.set_state(address, CacheState.SHARED)

class Multiprocessor:
    """다중 처리기 시스템"""

    def __init__(self, num_cpus: int = 4):
        self.memory = SharedMemory()
        self.bus = Bus(self.memory)
        self.caches: List[Cache] = []
        self.controllers: List[MESIController] = []

        # CPU 및 캐시 생성
        for i in range(num_cpus):
            cache = Cache(i)
            self.bus.register_cache(cache)
            self.caches.append(cache)
            self.controllers.append(MESIController(cache, self.bus))

    def read(self, cpu_id: int, address: int) -> int:
        """지정 CPU에서 읽기"""
        return self.controllers[cpu_id].read_request(address)

    def write(self, cpu_id: int, address: int, data: int) -> None:
        """지정 CPU에서 쓰기"""
        self.controllers[cpu_id].write_request(address, data)

    def get_stats(self) -> Dict:
        """통계 반환"""
        return {
            f"CPU{i}": {
                "hits": c.stats.hits,
                "misses": c.stats.misses,
                "hit_rate": f"{c.stats.hit_rate:.2%}",
                "invalidations": c.stats.invalidations,
                "write_backs": c.stats.write_backs
            }
            for i, c in enumerate(self.caches)
        }

    def simulate_false_sharing(self) -> None:
        """False Sharing 시뮬레이션"""
        print("\n=== False Sharing Demo ===")
        # 같은 캐시 라인(64바이트)에 있는 변수들
        base_addr = 0  # 캐시 라인 시작

        # CPU 0이 변수 A 쓰기
        self.write(0, base_addr, 100)
        print(f"CPU0 writes A (addr {base_addr}): M state")

        # CPU 1이 같은 라인의 변수 B 쓰기
        self.write(1, base_addr + 4, 200)
        print(f"CPU1 writes B (addr {base_addr+4}): Invalidates CPU0")

        # CPU 0이 다시 A 읽기 → Miss!
        data = self.read(0, base_addr)
        print(f"CPU0 reads A: {'Hit' if self.caches[0].stats.misses < 2 else 'Miss'}")

        print("False Sharing으로 캐시 효율 저하!")

# 사용 예시
if __name__ == "__main__":
    print("=== Multiprocessor Cache Coherence Demo ===\n")

    # 4코어 시스템 생성
    mp = Multiprocessor(num_cpus=4)

    # 시나리오 1: 단순 읽기
    print("=== Scenario 1: Read Sharing ===")
    mp.write(0, 100, 42)  # CPU0이 메모리에 쓰기
    print(f"CPU0 writes addr 100 = 42")

    data = mp.read(1, 100)  # CPU1이 읽기
    print(f"CPU1 reads addr 100 = {data}")
    print(f"CPU0 cache state: {mp.caches[0].get_state(100).value}")
    print(f"CPU1 cache state: {mp.caches[1].get_state(100).value}")

    # 시나리오 2: 쓰기 무효화
    print("\n=== Scenario 2: Write Invalidate ===")
    mp.write(1, 100, 99)  # CPU1이 쓰기
    print(f"CPU1 writes addr 100 = 99")
    print(f"CPU0 cache state: {mp.caches[0].get_state(100).value}")
    print(f"CPU1 cache state: {mp.caches[1].get_state(100).value}")

    # 시나리오 3: False Sharing
    mp.simulate_false_sharing()

    # 통계
    print("\n=== Cache Statistics ===")
    stats = mp.get_stats()
    for cpu, stat in stats.items():
        print(f"{cpu}: Hit Rate = {stat['hit_rate']}, "
              f"Invalidations = {stat['invalidations']}")

    # 암달의 법칙 데모
    print("\n=== Amdahl's Law Demo ===")
    for n in [2, 4, 8, 16, 32, 64]:
        for p in [0.5, 0.75, 0.9, 0.95]:
            speedup = 1 / ((1 - p) + p / n)
            print(f"N={n:2d}, P={p:.0%}: Speedup = {speedup:.2f}x")
        print()
