+++
title = "45. NUMA (Non-Uniform Memory Access)"
date = 2026-03-06
categories = ["studynotes-computer-architecture"]
tags = ["NUMA", "UMA", "Memory-Access", "Multi-Socket", "Node-Interconnect"]
draft = false
+++

# NUMA (Non-Uniform Memory Access)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NUMA는 **"각 **소켓**(Socket)**이 **로컬 **메모리**(Local **Memory)**를 **가지고 **원격 **메모리**(Remote **Memory)**에 **접근**하는 **아키텍처\\\"**로, **로컬 **액세스**는 **빠르고**(50-100ns)**, **원격 **액세스**는 **느리다**(100-200ns)**.
> 2. **구조**: **Node**(소켓 + **메모리)**와 **Interconnect**(QPI, **UPI, **Infinity **Fabric)**로 **연결**되고 **NUMA **Node**(0, 1, **2...)**마다 **독립적인 **메모리 **컨트롤러**와 **캐시**가 **있다.
> 3. **최적화**: **First **Touch **Policy**, **NUMA **Affinity**, **Interleaving**으로 **메모리 **할당**을 **최적화**하고 **numactl**, **taskset**으로 **프로세스**를 **바인딩**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
NUMA는 **"비균일 메모리 접근"** 아키텍처이다.

**메모리 액세스 유형**:
| 유형 | 설명 | 지연시간 | 대역폭 |
|------|------|----------|--------|
| **UMA** | 모든 CPU가 동일한 지연시간 | 동일 | 공유 |
| **NUMA** | 로컬/원격 메모리 | 상이 | 다름 |

### 💡 비유
NUMA는 ****아파트 **단지 ****와 같다.
- **방**: 로컬 메모리
- **이웃**: 원격 메모리
- **복도**: 인터커넥트

---

## Ⅱ. 아키텍처 및 핵심 원리

### NUMA 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         NUMA Architecture (2-Socket)                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Physical Layout:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Socket 0 (Node 0)                              Socket 1 (Node 1)                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  CPU 0-7              Memory          │  CPU 8-15              Memory                 │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │  │
    │  │  │  Core 0-15                128GB DDR4          Core 16-31          128GB DDR4     │  │  │  │  │  │
    │  │  │  L3 Cache (Shared)         Memory Ctrl        L3 Cache (Shared)   Memory Ctrl  │  │  │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │ QPI/UPI/Infinity Fabric (20-25 GB/s)                                         │  │
    │            ◄───────────────────────────────────────────────────────────────────────────────>│  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
    │  → Node 0: CPU 0-7 + 128GB memory (Local to CPU 0-7)                                      │  │
    │  → Node 1: CPU 8-15 + 128GB memory (Local to CPU 8-15)                                    │  │
    │  → Total: 16 CPUs, 256GB memory                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Memory Access Latency:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CPU 0 (Node 0) accesses:                                                                 │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Access Type   │  Latency  │  Bandwidth  │  Path                                   │  │  │
    │  │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │  │
    │  │  │  Local (Node 0)│  ~70ns    │  ~50 GB/s   │  Integrated Memory Controller          │  │  │
    │  │  │  Remote (Node 1)│ ~120ns  │  ~25 GB/s   │  QPI/UPI Interconnect                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  → Remote access: ~2x latency, ~0.5x bandwidth                                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### NUMA Topology

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         NUMA Topology (4-Socket Example)                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Mesh Interconnect:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │     Node 0          Node 1                                                                │  │
    │  ┌──────────┐   ┌──────────┐                                                             │  │
    │  │ CPU 0-15 │   │ CPU 16-31│                                                             │  │
    │  │  128GB   │   │  128GB   │                                                             │  │
    │  └────┬─────┘   └─────┬────┘                                                             │  │
    │       │               │                                                                    │  │
    │       │    Interconnect (Mesh)                                                            │  │
    │       │               │                                                                    │  │
    │  ┌────┴─────┐   ┌─────┴────┐                                                             │  │
    │  │ CPU 32-47│   │ CPU 48-63│                                                             │  │
    │  │  128GB   │   │  128GB   │                                                             │  │
    │  └──────────┘   └──────────┘                                                             │  │
    │     Node 2          Node 3                                                                │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Distance Matrix (NUMA Distance):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  │  From/To  │  Node 0  │  Node 1  │  Node 2  │  Node 3  │                               │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────────────│  │
    │  │  Node 0   │  10      │  20      │  20      │  30      │  (local = 10, remote = 20+)   │  │
    │  │  Node 1   │  20      │  10      │  30      │  20      │                               │  │
    │  │  Node 2   │  20      │  30      │  10      │  20      │                               │  │
    │  │  Node 3   │  30      │  20      │  20      │  10      │                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### First Touch Policy

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         First Touch Memory Allocation                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Default Behavior (First Touch):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Thread 0 (CPU 0, Node 0) allocates and initializes array[0..N-1]                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  int *array = malloc(N * sizeof(int));  // Virtual memory only                        │  │  │
    │  │  for (int i = 0; i < N; i++) {                                                        │  │  │
    │  │      array[i] = i;  // Page fault → allocate page on Node 0                          │  │  │
    │  │  }                                                                                     │  │  │
    │  │  → All pages allocated on Node 0 (local to Thread 0)                                  │  │  │
    │  │  → Thread 1 (CPU 8, Node 1) accessing array[0..N-1] → Remote access!                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    NUMA-Aware Allocation:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Thread 0 (CPU 0, Node 0) allocates array[0..N/2] on Node 0                               │  │
    │  Thread 1 (CPU 8, Node 1) allocates array[N/2..N] on Node 1                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  // Thread 0                                                                          │  │  │
    │  │  numa_alloc_onnode(N/2 * sizeof(int), 0);  // Allocate on Node 0                     │  │  │
    │  │  for (int i = 0; i < N/2; i++) {                                                      │  │  │
    │  │      array[i] = i;                                                                    │  │  │
    │  │  }                                                                                     │  │  │
    │  │                                                                                       │  │  │
    │  │  // Thread 1                                                                          │  │  │
    │  │  numa_alloc_onnode(N/2 * sizeof(int), 1);  // Allocate on Node 1                     │  │  │
    │  │  for (int i = N/2; i < N; i++) {                                                      │  │  │
    │  │      array[i] = i;                                                                    │  │  │
    │  │  }                                                                                     │  │  │
    │  │  → Each thread accesses local memory only                                             │  │  │
    │  │  → No cross-node traffic                                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### UMA vs NUMA 비교

| 특성 | UMA (SMP) | NUMA |
|------|-----------|------|
| **메모리** | 공통 | 분산 |
| **지연시간** | 동일 | 상이 |
| **확장성** | ~8 CPU | ~1024 CPU |
| **프로그래밍** | 단순 | 복잡 |

### NUMA 최적화 기법

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         NUMA Optimization Techniques                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. CPU Pinning (Affinity):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Pin process to CPU 0 (Node 0)                                                        │  │
    │  taskset -c 0 ./myapp                                                                   │  │
    │                                                                                         │  │
    │  # Pin process to Node 0 (CPUs 0-7)                                                      │  │
    │  numactl --cpunodebind=0 --membind=0 ./myapp                                            │  │
    │  → CPU and memory both on Node 0                                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Interleaved Allocation:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Allocate memory striped across all nodes                                              │  │
    │  numactl --interleave=all ./myapp                                                        │  │
    │  → Pages round-robin: 0→Node0, 1→Node1, 2→Node0, 3→Node1...                              │  │
    │  → Good: Workloads with random memory access                                             │  │
    │  → Bad: Sequential access patterns                                                       │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Page Migration:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Move pages to Node 0                                                                  │  │
    │  numactl --membind=0 --cpunodebind=0 migrate-pages <pid> 0 all                            │  │
    │  → Pages moved to Node 0 (expensive, but useful for long-running processes)               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### NUMA Anti-Patterns

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         NUMA Anti-Patterns                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. False Sharing + NUMA:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  struct Counter {                                                                        │  │
    │      int value;                                                                          │  │
    │  } counters[64];                                                                         │  │
    │                                                                                         │  │
    │  Thread 0 (Node 0): increments counters[0-31]                                            │  │
    │  Thread 1 (Node 1): increments counters[32-63]                                          │  │
    │  → Both counters may be on same page (allocated by Thread 0)                             │  │
    │  → Cache coherence traffic across QPI/UPI                                                │  │
    │  → Solution: Allocate on separate nodes or pad to cache line                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. All Memory on Node 0:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Thread 0 allocates all data                                                          │  │
    │  void *data = malloc(1024 * 1024 * 1024);  // On Node 0                                  │  │
    │  memset(data, 0, 1024 * 1024 * 1024);                                                   │  │
    │                                                                                         │  │
    │  // Thread 1 (Node 1) processes data                                                     │  │
    │  #pragma omp parallel for                                                               │  │
    │  for (int i = 0; i < N; i++) {                                                           │  │
    │      ((int*)data)[i] = process(i);  // Remote access for Thread 1                       │  │
    │  }                                                                                       │  │
    │  → Thread 1 experiences ~2x latency                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 데이터베이스 서버 NUMA 튜닝
**상황**: 2-socket x86, PostgreSQL 256GB
**판단**: Node isolation + Huge Pages

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Database NUMA Tuning                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  PostgreSQL runs on Node 0, but some connections pinned to Node 1                        │  │
    │  → Remote memory access: ~120ns vs ~70ns (~70% slower)                                   │  │
    │  → Interconnect saturation                                                               │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution 1: Node Isolation (1 instance per node):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Run PostgreSQL on Node 0 only                                                         │  │
    │  numactl --cpunodebind=0 --membind=0 postgres -D /data/node0                             │  │
    │                                                                                         │  │
    │  # Run another PostgreSQL on Node 1 only                                                 │  │
    │  numactl --cpunodebind=1 --membind=1 postgres -D /data/node1                             │  │
    │  → 2x throughput, no cross-node traffic                                                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution 2: NUMA-Aware Memory Allocator (jemalloc):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Configure PostgreSQL to use jemalloc                                                   │  │
    │  export LD_PRELOAD=/usr/lib64/libjemalloc.so.2                                           │  │
    │  export MALLOC_CONF="dirty_decay_ms:1000,muzzy_decay_ms:1000,narenas:8"                  │  │
    │  → jemalloc allocates thread-local arenas (reduces cross-node traffic)                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Monitoring:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Check NUMA hit/miss ratios                                                             │  │
    │  $ numastat -m                                                                           │  │
    │  │  Node           Hit          Miss                                                       │  │
    │  │  0          12345678        12345                                                       │  │
    │  │  1           987654        987654 (high miss rate!)                                     │  │
    │  │                                                                                         │  │
    │  │  → Node 1 experiencing high remote access                                              │  │
    │  │  → Investigate: Move processes to Node 1 or allocate memory on Node 1                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### NUMA 기대 효과

| 시나리오 | 미최적화 | 최적화 | 개선 |
|----------|----------|--------|------|
| **OLTP** | 100K TPS | 150K TPS | 50% |
| **Analytics** | 10 GB/s | 25 GB/s | 150% |
| **HPC** | 500 GFLOPS | 800 GFLOPS | 60% |

### 모범 사례

1. **Local first**: 로컬 메모리 우선
2. **Pinning**: CPU+메모리 같은 노드
3. **Monitoring**: numastat
4. **Testing**: 노드 격리

### 미래 전망

1. **CXL**: coherent interconnect
2. **Gen-Z**: memory semantic fabric
3. **CCIX**: cache coherent
4. **3D IC**: HBM closer

### ※ 참고 표준/가이드
- **Intel**: NUMA Optimization
- **AMD**: NUMA Guide
- **Linux**: numactl manpage

---

## 📌 관련 개념 맵

- [멀티코어](./7_multicore/97_multicore.md) - 코어
- [캐시](./7_cache/87_cache.md) - 일관성
- [가상화](./12_virtualization/133_hardware_virtualization.md) - VM
