+++
title = "371. 거대 페이지 (Huge Pages / Transparent Huge Pages)"
date = "2026-03-14"
weight = 371
+++

# 371. 거대 페이지 (Huge Pages / Transparent Huge Pages)

> **Insight: 메모리 관리의 오버헤드를 줄이는 거대한 도약**
> 1. **본질**: **거대 페이지 (Huge Pages)**는 **TLB (Translation Lookaside Buffer)**의 적중률을 극대화하고 **페이지 테이블 (Page Table)**의 계층 구조를 단순화하여, 메모리 주소 변환에 따른 **CPU (Central Processing Unit)** 사이클 낭비를 근본적으로 제거하는 하드웨어-소프트웨어 결합 최적화 기술입니다.
> 2. **가치**: 대용량 메모리 환경(수백 GB ~ TB)에서 발생하는 **TLB Miss**로 인한 성능 병목을 해소하여, 데이터베이스 쿼리 성능을 최대 30% 이상 향상시키고 가상화 환경(**VM**, **Container**)의 메모리 접근 지연시간을 획기적으로 단축시킵니다.
> 3. **융합**: **OS (Operating System)**의 커널 메모리 관리자와 **CPU**의 **MMU (Memory Management Unit)** 하드웨어 기능이 융합된 기술로, 최근 클라우드 네이티브 환경과 **AI (Artificial Intelligence)** 학습 워크로드의 고대역폭 메모리 요구를 충족시키는 핵심 인프라 기술로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
현대 컴퓨팅 환경에서 **RAM (Random Access Memory)**의 용량은 기가바이트(GB) 단위를 넘어 테라바이트(TB) 단위로 확대되었습니다. 그러나 기존의 가상 메모리 시스템은 4KB라는 작은 페이지 단위를 기준으로 설계되었습니다. 4KB 페이지를 사용하여 1TB의 메모리를 관리하기 위해서는 약 2억 6천만 개 이상의 페이지 테이블 엔트리가 필요하며, 이는 곧 막대한 양의 메모리 오버헤드와 관리 비용으로 이어집니다.

**거대 페이지 (Huge Pages)** 기술은 이러한 한계를 극복하기 위해, **CPU**가 지원하는 더 큰 페이지 크기(예: x86-64에서 2MB 또는 1GB)를 사용하여 메모리를 관리하는 방식입니다. 물리 메모리를 더 큰 덩어리로 할당함으로써, 메모리 매핑 정보를 저장하는 **페이지 테이블(Page Table)**의 크기를 획기적으로 줄이고 주소 변환을 위한 하드웨어 캐시인 **TLB (Translation Lookaside Buffer)**의 효율을 극대화하는 것이 핵심 철학입니다.

### 2. 등장 배경 및 변천
① **기존 한계**: 64비트 시스템으로의 전환과 함께 가상 주소 공간이 폭발적으로 증가함에 따라, 기존 4KB 페이지 기반의 멀티 레벨 페이지 테이블(4-Level Paging) 구조는 메모리 접근 시 **Page Walk** 과정에서 너무 많은 메모리 참조가 발생시켜 성능 저하의 주범이 되었습니다.
② **혁신적 패러다임**: **CPU** 제조사(Intel, AMD)는 **TLB**의 적중률을 높이기 위해 2MB/1GB 페이지를 지원하는 **PSE (Page Size Extension)** 및 **1GB Page** 기능을 추가하였고, **OS** 커널(Linux, Windows)은 이를 활용하여 대용량 메모리를 효율적으로 매핑하는 메커니즘을 구현했습니다.
③ **현재의 비즈니스 요구**: 인메모리 데이터베이스(Oracle, Redis), 빅데이터 분석(Hadoop, Spark), 및 가상화 플랫폼(VMWare, KVM)은 일관된 높은 메모리 대역폭과 낮은 지연시간을 요구하며, 거대 페이지는 이를 만족시키는 필수적인 설정이 되었습니다.

### 3. 구조적 비유 시각화
일반적인 4KB 페이지 관리와 거대 페이지 관리의 차이를 지도(Map)로 비유해보겠습니다.

```text
[Scenario: Managing 1TB Physical Memory]

[Standard 4KB Pages]                 [Huge Pages (2MB)]
---------------------                 ---------------------
Page Table Size: ~2GB                Page Table Size: ~4MB
(Total Entries: ~256M)               (Total Entries: ~512K)
Search Depth: 4 Levels               Search Depth: 3 Levels
Management Overhead: High            Management Overhead: Low

Visual Representation:
[4KB] [4KB] [4KB] [4KB] ... (x256M)  [      2MB Block      ] ... (x512K)
 ^                                      ^
 |                                      |
Tiny Maps (Thousands)                  Giant Map (Hundreds)
```

📢 **섹션 요약 비유**: 도서관에서 수백만 권의 책을 찾을 때, '엽서' 크기의 색인(4KB Page)을 한 장씩 넘기며 찾는 것보다, '신문' 크기의 대형 색인(2MB Huge Page)을 한 장씩 넘겨 한눈에 보는 것이 훨씬 빠르고 효율적입니다. 이것이 거대 페이지가 메모리 검색 속도를 높이는 핵심 원리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석
거대 페이지 시스템은 하드웨어와 운영체제가 밀접하게 상호작용합니다. 주요 구성 요소는 다음과 같습니다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 관련 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|
| **TLB (Translation Lookaside Buffer)** | 고속 주소 변환 캐시 | **CPU** 내부의 캐시로, 가상 주소를 물리 주소로 즉시 변환. Miss 발생 시 성능 급격 하락. | `INVLPG`, `INVLPGB` | 단어 사전책갈피 |
| **Page Directory/Table** | 매핑 테이블 계층 | 4레벨(PML4 -> PDP -> PDE -> PTE) 구조. Huge Page 사용 시 PDE 레벨에서 직접 물리 주소 매핑(PDE가 PTE 역할 겸임). | x86-64 Paging Struct | 거대한 인덱스 |
| **MMU (Memory Management Unit)** | 주소 변환 장치 | **TLB Miss** 발생 시 하드웨어 **Page Table Walker**가 동작하여 메모리 참조. Huge Page는 Walk Depth 감소 → 메모리 접근 횟수 감소. | CR3 Register Control | 주소 검색로봇 |
| **khugepaged** | THP 데몬 (Kernel Thread) | 백그라운드에서 4KB 페이지들을 스캔하고, 물리적으로 연속된 영역을 찾아 2MB 페이지로 **Defrag** 및 병합(Collapse) 수행. | `madvise(MADV_HUGEPAGE)` | 자동 정리 로봇 |
| **Hugetlbfs** | 파일 시스템 (User Space) | 사용자 영역에서 Huge Page를 마치 파일처럼 `mmap`하여 사용할 수 있는 인터페이스 제공. | `shmget`, `mmap` | 전용 예약 창고 |

### 2. 페이지 테이블 구조 및 TLB 커버리지 비교
다음 다이어그램은 4KB 페이지와 2MB 거대 페이지가 **TLB** 엔트리를 점유하는 방식과 페이지 테이블 계층의 차이를 보여줍니다.

```text
[Scenario: Mapping 64MB Memory with x86-64 Architecture]

[A] Standard 4KB Pages (Requires 16,384 Pages)
-------------------------------------------------
Virtual Addr  ----->  TLB (Entry covers 4KB)
  |                             ^
  |                             | (TLB MISS: Frequent)
  v                             | (Coverage: Small)
Page Table Walk (4 Levels)
  PML4 -> PDP -> PDE -> PTE ----> Physical RAM (4KB * 16,384)
  
[B] Huge Pages (2MB) (Requires only 32 Pages)
-------------------------------------------------
Virtual Addr  ----->  TLB (Entry covers 2MB)
  |                             ^
  |                             | (TLB HIT: High Probability)
  v                             | (Coverage: 512x Larger)
Page Table Walk (3 Levels)
  PML4 -> PDP -> PDE (Direct Map) --> Physical RAM (2MB * 32)
  
(Key Insight: In [B], one TLB entry covers 512x more memory 
than [A], drastically reducing the frequency of Misses)
```

### 3. 심층 동작 원리 (THP 동작 사이클)
**THP (Transparent Huge Pages)**는 사용자 개입 없이 커널이 자동으로 성능을 최적화하는 과정을 거칩니다.

1.  **할당 (Allocation)**: 애플리케이션이 `malloc()` 등으로 메모리 요청 시, 커널은 우선 기본 4KB 페이지를 즉시 할당하여 응답성을 확보합니다.
2.  **스캔 (Scanning)**: 백그라운드의 `khugepaged` 스레드가 주기적으로(기본값 등) 메모리 영역을 스캔합니다. 이때 `/sys/kernel/mm/transparent_hugepage/enabled` 설정값을 확인합니다.
3.  **검증 (Checking)**: 해당 영역의 4KB 페이지들이 **물리적으로 연속(Physically Contiguous)**인지, 그리고 페이지들이 수정되지 않은 상태( Clean )인지 확인합니다.
4.  **병합 (Collapse)**: 조건이 충족되면 512개(4KB * 512 = 2MB)의 페이지 테이블 엔트리를 하나의 거대한 엔트리로 축소(Collapse)하고, 상위 레벨 페이지 테이블 포인터를 갱신합니다.
5.  **폴백 (Fallback)**: 물리 메모리가 파편화되어 연속된 2MB 공간을 확보하지 못하면, 기존 4KB 페이지 상태를 유지합니다.

### 4. 핵심 알고리즘 및 코드
리눅스 커널 환경에서 Huge Page를 할당하고 확인하는 실무 코드 및 명령어입니다.

```c
/* System Call: Explicit Huge Page Allocation (User Level) */
/* MAP_HUGETLB flag는 사용자가 직접 Huge Page를 요청함을 의미합니다. */
/* fd=-1, MAP_ANONYMOUS는 익명 매핑(파일 연결 없음)을 의미합니다. */

#define _GNU_SOURCE
#include <sys/mman.h>
#include <stdio.h>
#include <unistd.h>

void* allocate_huge_page(size_t size) {
    // void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
    void *addr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                      MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB | MAP_HUGE_2MB, 
                      -1, 0);
    
    if (addr == MAP_FAILED) {
        perror("mmap (Huge Page) failed");
        return NULL;
    }
    printf("Allocated Huge Page at: %p\n", addr);
    return addr;
}

// Verification: Check /proc/meminfo or 'hugepages' filesystem
```

```bash
# Kernel Parameter Check (Linux)
cat /proc/sys/vm/nr_hugepages        # Static Huge Pages count
cat /sys/kernel/mm/transparent_hugepage/enabled # THP status [always/madvise/never]
```

📢 **섹션 요약 비유**: THP는 마치 택배 회사가 처음에는 작은 박스로 물건을 개별적으로 보내다가, 나중에 로봇 팔이 물건을 확인하고 내용물이 같은 곳으로 가는 것을 확인하면 박스를 뜯어서 대형 컨테이너(2MB)에 다시 담아 운송 효율을 높이는 지능적인 물류 시스템과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 정적 Huge Pages vs 동적 THP 심층 비교
기술적 결정을 내릴 때 두 기술은 명확히 구별되어야 합니다. 특히 **Tail Latency**에 민감한 서비스에서는 중요합니다.

| 비교 항목 | 정적 Huge Pages (Static) | Transparent Huge Pages (THP) |
|:---|:---|:---|
| **메모리 예약 시점** | 시스템 부팅 시 또는 수동 설정 즉시에 **풀(Pool)** 생성 | 실행(Run-time) 중, 메모리 할당 시점에 **On-Demand** 생성 |
| **물리 메모리 연속성** | 100% 보장 (미리 할당됨) | 런타임 상황에 따라 다름 (Compaction 필요) |
| **응용 프로그램 수정** | **필요** (`mmap(MAP_HUGETLB)`, `shmget(SHM_HUGETLB)` 등 명시적 API 사용) | **불필요** (Kernel 2.6.38+ 이상에서는 투명하게 지원) |
| **성능 일관성** | **높음 (High Determinism)** | **중간 (Variable)**: 메모리 파편화 시 `khugepaged` 작동으로 인한 **Stall** 발생 가능 |
| **메모리 오버헤드** | 내부 단편화(Internal Fragmentation) 발생 가능率高 | 필요 시만 할당되어 효율적이나, 병합 실패 시 4KB로 남음 |
| **주요 사용 사례** | Oracle DB, Redis, In-Memory Cache (대규모 메모리 필요) | 범용 애플리케이션, 일반 Web Server, Desktop |

### 2. 타 영역(네트워크, 가상화)과의 시너지 및 오버헤드

**① 가상화(Virtualization)와의 융합: EPT(Extended Page Tables) 효율화**
가상화 환경에서는 **Nested Paging** (AMD) 또는 **EPT (Intel)**라고 불리는 2차원 주소 변환이 발생합니다 (Guest Virtual -> Guest Physical -> Host Physical).

```text
[Virtualization Memory Walk]

Guest OS (4KB)       Host OS (4KB)            Performance Impact
GVA -> GPA -> HPA    GVA -> GPA -> HPA
(Walk x 4)      +    (Walk x 4)          =     Severe Latency
(Walk x 1)      +    (Walk x 1)          =     Optimized Latency
(Using HugePage)     (Using HugePage)
```

- **시너지**: Guest OS가 2MB Huge Page를 사용하고, Host OS 또한 2MB Huge Page를 사용하여 매핑하면, **EPT TLB**의 적중률이 비약적으로 상승합니다. 이는 가상 머신(VM)의 **Context Switching** 및 **VM Exit** 빈도를 줄여줍니다.
- **수치적 지표**: VMware 기준 4KB 페이지 대비 2MB Huge Page 사용 시, TLB Miss 비율이 약 50~70% 감소하여 데이터베이스 트랜잭션 처리량(TPS)이 20% 이상 상승하는 경우가 많습니다.

**② 네트워크(Network)와의 융합: DMA(Direct Memory Access) 및 Zero-Copy**
고성능 네트워킹(DPDK, RDMA)에서는 대량의 데이터를 전송하기 위해 **DMA**를 사용합니다.
- **시너지**: 페이지 폴트(Page Fault) 처리는 DMA 전송 중 치명적인 병목입니다. Huge Page를 사용하면 페이지