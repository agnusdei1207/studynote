+++
title = "378. 로컬 노드 할당 vs 인터리브 할당"
date = "2026-03-14"
weight = 378
+++

# 378. 로컬 노드 할당 vs 인터리브 할당

> **본질**: NUMA (Non-Uniform Memory Access) 아키텍처 환경에서 운영체제 커널이 물리 메모리 페이지를 배치하는 핵심 전략으로, **메모리 액세스 지연 시간(Latency)** 최소화와 **데이터 전송률(Bandwidth)** 극대화 사이의 트레이드-오프(Trade-off)를 결정하는 메모리 관리 기술입니다.
>
> **가치**: 로컬 노드 할당은 QPI (QuickPath Interconnect) 또는 Infinity Fabric과 같은 인터커넥트를 통한 원격 접근 비용을 제거하여 단일 스레드 성능과 저지연성을 보장하며, 인터리브 할당은 다중 노드의 메모리 컨트롤러를 병렬 활용하여 대규모 데이터 처리 시 시스템 전체의 처리량(Throughput)을 획기적으로 향상시킵니다.
>
> **융합**: OS 스케줄러의 CPU Affinity/CPU Pinning 정책과 밀접하게 연동되며, 고성능 컴퓨팅(HPC), 대용량 인메모리 데이터베이스(IMDB), 가상화 플랫폼(Hypervisor)의 메모리 파티셔닝 최적화에 직접적으로 적용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
현대의 멀티 프로세서(Multi-Processor) 서버 아키텍처는 모든 CPU가 메모리를 동일한 속도로 접근하는 UMA (Uniform Memory Access) 방식에서, 메모리가 각 CPU 소켓(Socket)별로 분리된 **NUMA (Non-Uniform Memory Access)** 구조로 진화했습니다. 이 구조에서 CPU는 자신이 속한 로컬 노드(Local Node)의 메모리에는 빠르게 접근하지만, 다른 노드(원격 노드)의 메모리에 접근할 때는 인터커넥트(Interconnect)를 거쳐야 하므로 상대적으로 높은 지연 시간(Latency)이 발생합니다.

이러한 하드웨어적 특성을 운영체제가 효율적으로 활용하기 위해 메모리 할당 시 크게 두 가지 전략을 선택합니다.
**① 로컬 노드 할당 (Local Node Allocation)**: 요청한 CPU가 속한 노드 내의 메모리만을 사용하여 액세스 시간을 최소화하는 전략입니다.
**② 인터리브 할당 (Interleaved Allocation)**: 가상 주소(Virtual Address)에 따라 페이지를 여러 노드에 균등하게 분산(Striping) 배치하여, 전체 메모리 대역폭의 총량(Bandwidth Aggregation)을 극대화하는 전략입니다.

### 2. 등장 배경 및 비즈니스 요구
① **스케일업(Scale-up)의 한계와 극복**: 단일 버스 방식의 UMA는 메모리 대역폭 병목을 야기했습니다. NUMA는 이를 해결했지만, '어디에 메모리를 할당할 것인가'라는 새로운 문제를 남겼습니다.
② **워크로드의 이분화**: 금융 거래와 같은 **저지연(Low Latency)** 워크로드와 빅데이터 분석과 같은 **고처리량(High Throughput)** 워크로드가 공존하게 되면서 단일 정책으로는 모든 요구를 충족할 수 없게 되었습니다.
③ **비즈니스 효율성**: 클라우드 환경에서는 하드웨어 자원을 효율적으로 분배하여 TCO (Total Cost of Ownership)를 낮추고 SLA (Service Level Agreement)를 준수해야 합니다. 이에 따라 특정 애플리케이션에 최적화된 메모리 정책 설정이 필수적인 기술적 과제로 대두되었습니다.

### 3. 아키텍처 개요 도해
두 전략의 핵심 차이는 메모리 접근의 '거리(Distance)'와 '경로(Path)'에 있습니다.

```text
   [1] Local Allocation Concept          [2] Interleaved Allocation Concept
       
   CPU 0 (Request)                       CPU 0 (Request)
      |                                      |
      | (Short Path)                         | (Calculation Logic)
      v                                      v
   +-----------------+                   +------------------+       +------------------+
   |   Node 0        |                   |   Node 0         |       |   Node 1        |
   | +-------------+ |                   | (Page A, C, E...) |       | (Page B, D, F...) |
   | | MEMORY      | |                   | (Striping Set 1) |       | (Striping Set 2) |
   | +-------------+ |                   +--------+---------+       +--------+---------+
   +-----------------+                            |                         |
        ^                                         +-----------+-------------+
        |                                                     |
        | v                                         (Aggregate Bandwidth Usage)
   [Low Latency Access]                                [High Bandwidth]
```
*도해 1: 두 할당 정책의 개념적 접근 방식 비교*

#### 도해 1 해설
위 다이어그램은 메모리 요청이 처리되는 논리적 경로를 보여줍니다.
- **로컬 할당 [1]**: CPU 0이 요청하면 운영체제는 무조건 Node 0 내의 여유 공간을 할당합니다. 데이터가 인터커넥트를 건너지 않으므로 지연 시간이 가장 짧습니다.
- **인터리브 할당 [2]**: 운영체제는 페이지 번호를 노드 개수로 나눈(Modulo) 결과에 따라 페이지를 A는 Node 0에, B는 Node 1에 식별하여 배치합니다. 하나의 스레드라도 메모리를 읽을 때 여러 노드의 컨트롤러가 동시에 작동하여 대역폭을 합산(aggregate)할 수 있습니다.

📢 **섹션 요약 비유**: 병원 약제부를 운영할 때, **로컬 할당**은 응급실에 바로 붙어 있는 '비상약품 cabinets'을 두어 의사가 약을 찾는 시간을 최소화하는 것이고, **인터리브 할당**은 대규모 종합병원의 중앙 약국을 여러 층에 나누어 배치하여, 수많은 환자가 동시에 약을 받더라도 전체 수령 속도(처리량)가 최대가 되도록 하는 전략과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 상세 동작 비교
이 기술을 이해하기 위해서는 물리 메모리를 관리하는 커널의 하위 시스템과 그 매커니즘을 파악해야 합니다.

| 구성 요소 (Component) | 로컬 노드 할당 (Local Node) | 인터리브 할당 (Interleaved) | 기술적 상세 (Technical Detail) |
|:---|:---|:---|:---|
| **정책 설정 (Policy)** | `MPOL_BIND` 또는 `MPOL_PREFERRED` | `MPOL_INTERLEAVE` | Linux `set_mempolicy()` 시스템 콜 사용 |
| **페이지 프레임 선택** | 현재 CPU의 `numa_node_id()` 반환 값과 일치하는 Free List 사용 | `(Page_Index % Total_Nodes)` 연산으로 노드 결정 | 해시(Hash) 기반 Round-Robin 분산 |
| **타겟 메모리 컨트롤러** | **로컬 IMC (Integrated Memory Controller)** 1개만 독점 | **모든 노드의 IMC**를 병렬로 활용 | Memory Channel Utilization 극대화 |
| **Latency (지연시간)** | **최소화** (Local Access: ~60~80ns) | **증가** (Remote Access 포함: ~100~140ns 평균) | Interconnect Hop 유무에 따른 차이 |
| **Bandwidth (대역폭)** | Node 1개의 대역폭으로 제한 (예: ~40 GB/s) | **Node N개의 대역폭 합산** (예: ~160 GB/s) | MLP (Memory Level Parallelism) 효과 |
| **주요 용도** | Latency-sensitive 작업 (DB Transaction, Web Server) | Bandwidth-sensitive 작업 (HPC, Video Rendering) | Workload Characterization에 따른 선택 |

### 2. 시스템 레벨 동작 메커니즘
리눅스 커널은 **Buddy System**과 **Slab Allocator** 위에서 물리적 프레임(PFN)을 할당하기 직전, NUMA 정책을 참조하여 최종 노드를 결정합니다.

```text
[Kernel Memory Allocation Flow]
--------------------------------------------------------------------
 Application
      |
      | malloc() / mmap()
      v
+---------------------+
|   User Space VA     |  <--- Virtual Address (0x7f...)
+---------------------+
      |
      | Page Fault (First Access)
      v
+------------------------------------------------------------------+
|                        KERNEL SPACE                               |
| +----------------+      +------------------+      +-------------+ |
| |  Page Table    | ---> |  NUMA Policy     | ---> |   Buddy     | |
| |  Walk (MMU)    |      |  Check           |      |  Allocator  | |
| +----------------+      +------------------+      +-------------+ |
 |                                                                   |
 | [Case A: Local Policy]                            [Case B: Interleave] |
 | | Current CPU = Node 0                            | VA Offset = 0x4000   |
 | v                                                  v                    |
 | Target Node = 0                                   | 0x4000 % 4 Nodes = 0 |
 | | (Direct Allocation)                             | Target Node = 0      |
 | v                                                  | VA Offset = 0x8000   |
 | Node 0 Free List ------------------------------> | | 0x8000 % 4 Nodes = 1 |
 |                                                    | Target Node = 1      |
 |                                                    | (Striped Alloc)      |
 +--------------------------------------------------+----------------------+
```

#### 메커니즘 해설
1.  **페이지 폴트(Page Fault) 발생**: 애플리케이션이 가상 메모리에 처음 접근하면 하드웨어 인터럽트가 발생하고 커널의 페이지 폴트 핸들러가 호출됩니다.
2.  **정책 확인 (Policy Check)**: 커널은 해당 프로세스(`task_struct`)에 부여된 `mempolicy`를 확인합니다.
3.  **노드 선정 (Node Selection)**:
    - **Local**: 현재 실행 중인 CPU가 속한 노드 ID를 가져와(` numa_node_id()`), 해당 노드의 `zonelist`를 스캔합니다.
    - **Interleave**: 가상 주소(Virtual Address)의 오프셋과 노드 마스크(Node Mask)를 XOR 연산하거나 Modulo 연산하여 대상 노드를 계산합니다.
4.  **물리적 할당**: 결정된 노드의 버디 시스템에서 가용한 4KB 페이지 프레임을 할당하고 페이지 테이블 엔트리(PTE)를 매핑합니다.

### 3. 핵심 알고리즘 및 코드 구현
다음은 리눅스 커너(v5.x 이상)에서 메모리 할당 시 노드를 선택하는 핵심 루틴을 단순화한 C 코드입니다.

```c
// file: mm/mempolicy.c (Simplified)
// 
// 핵심 함수: alloc_pages_current(gfp_t gfp, unsigned order)
// 구조체 mempolicy 정의: include/linux/mempolicy.h

/*
 * MPOL_INTERLEAVE 정책 시 노드 선택 로직
 * 가상 주소 페이지의 순서에 따라 노드를 순환(Round-Robin) 선택.
 */
static unsigned int interleave_nodes(struct mempolicy *policy)
{
    // nid를 순환적으로 증가시켜 부하 분산
    // 이 함수는 호출될 때마다 다음 노드 ID를 반환함
    unsigned int nid;
    nid = current->il_next; // 현재 프로세스의 interleave 다음 노드
    policy->v.nodes = next_node(nid, policy->v.nodes);
    return nid;
}

/*
 * 페이지 할당 경로에서의 의사결정
 */
struct page *alloc_pages_current(gfp_t gfp, unsigned int order)
{
    struct mempolicy *pol = current->mempolicy;
    unsigned int nid;

    // [로컬 할당 또는 기본 정책]
    if (pol->mode == MPOL_PREFERRED || pol->mode == MPOL_BIND) {
        // 현재 CPU가 속한 노드를 우선 선택 (Local Allocation)
        nid = numa_node_id(); 
    } 
    // [인터리브 할당]
    else if (pol->mode == MPOL_INTERLEAVE) {
        // 정책에 정의된 로직에 따라 노드 계산
        nid = interleave_nodes(pol);
    }
    
    // 결정된 nid에서 페이지 할당 시도
    return __alloc_pages_nodemask(gfp, order, nid, &pol->v.nodes);
}
```
이 코드는 앞서 설명한 'Ⅱ. 2' 다이어그램의 논리를 구현한 것으로, `numa_node_id()`를 통해 로컬성을 확보하느냐, `interleave_nodes()`를 통해 대역폭을 분산하느냐가 갈리는 지점입니다.

📢 **섹션 요약 비유**: **로컬 할당**은 '내 책상 서랍'을 사용하는 것과 같습니다. 서랍이 작아서 많은 것을 넣을 수는 없지만(대역폭 제한), 물건을 집어넣고 꺼내는 시간이 즉시 이루어집니다(Latency 최소). 반면 **인터리브 할당**은 사무실 전체의 공용 사물함을 여러 명이 번갈아가며 효율적으로 사용하는 것과 같습니다. 특정 사람의 접근 속도는 느려질 수 있지만, 사무실 전체의 물량 처리 속도는 비약적으로 증가합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교 분석표

| 비교 항목 (Metric) | 로컬 노드 할당 (Local Node Alloc) | 인터리브 할당 (Interleaved Alloc) | 비고 (Remarks) |
|:---:|:---:|:---:|:---|
| **접근 지연 시간 (Access Latency)** | **매우 낮음 (Low)** <br> (Interconnect Hop X) | **높음 (High)** <br> (원격 액세스 평균 지연 발생) | 단일 쓰레드 성능은 Local이 유리함 |
| **총 메모리 대역폭 (Total Bandwidth)** | 낮음 (Low) <br> (단일 노드 IMC 속도에 한정) | **매우 높음 (High)** <br> (모든 노드 IMC 속도의 합) | HPC/Sientific 작업은 Interleave가 유리함 |
| **메모리 병목 지점 (Bottleneck)** | 특정 노드의 메모리 용량/대역폭 | 인터커넥트(QPI/UPI)의 대역폭 | 병목이 발생하는 지층(Layer)이 다름 |
| **캐시 지역성 (Cache Locality)** | **높음 (High)** <br> (LLC Hit 확률 증가) | 낮음 (Low) <br> (데이터가 분산되어 Cache Miss 가능성) | 데이터 재사용성이 중요하면 Local 선택 |

### 2. 타 영역(Subject) 융합 분석

#### (1) 운영체제 및 CPU 구조 (OS & Architecture)
**CPU 캐시 코히어런스(Cache Coherence) 프로토콜**과의 상호작용입니다.
- **MESI Protocol (Modified, Exclusive, Shared, Invalid)**: 로컬 할당을 사용하면 특정 노드 내의 **Last Level Cache (LLC, L3 Cache)**에 데이터가 집중됩니다