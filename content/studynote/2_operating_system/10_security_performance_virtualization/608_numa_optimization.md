+++
title = "608. NUMA 자원 배분 최적화 (numactl)"
date = "2026-03-14"
weight = 608
+++

# # [NUMA 자원 배분 최적화 (numactl)]

## 핵심 인사이트 (3줄 요약)
> 1. **본질 (Essence)**: SMP (Symmetric Multi-Processing)의 확장성 한계를 극복하기 위해 등장한 NUMA (Non-Uniform Memory Access) 아키텍처는 메모리 액세스 속도의 비대칭성을 인정하고, 이를 OS 커널 및 하드웨어가 협력하여 관리하는 구조입니다.
> 2. **가치 (Value)**: `numactl`과 같은 CLI (Command Line Interface) 도구를 활용해 **CPU Affinity**와 **Memory Policy**를 제어함으로써, 원격 메모리(Remote Memory) 접근으로 인한 지연 시간(Latency)을 최소화하고 대역폭(Bandwidth)을 보장하여 시스템 처리량(TPS)을 20~30% 이상 개선할 수 있습니다.
> 3. **융합 (Convergence)**: 가상화(vNUMA), 대규모 인메모리 DB, 고성능 컴퓨팅(HPC) 환경에서 필수적이며, OS 스케줄러의 `CFS` (Completely Fair Scheduler)와 연동하여 프로세스와 메모리의 물리적 거리를 최적화하는 핵심 엔지니어링 영역입니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
NUMA (Non-Uniform Memory Access)는 다중 프로세서 시스템에서 각 CPU가 로컬 메모리(Local Memory)를 가지고 있으며, 다른 CPU에 연결된 메모리(Remote Memory)에 접근할 때 상대적으로 더 높은 비용이 드는 아키텍처를 의미합니다. 기존의 UMA (Uniform Memory Access) 방식이 모든 CPU가 단일 메모리 컨트롤러를 통해 메모리에 접근하여 병목을 일으키는 것과 대비됩니다. 리눅스 커널은 이러한 하드웨어拓扑(Topology)를 인지하고 `Zone`, `Node` 단위로 메모리를 관리합니다.

**2. 기술적 배경과 필요성**
- **SMP의 한계**: 프로세서 코어 수가 증가함에 따라 메모리 버스(Memory Bus)와 FSB (Front Side Bus)에서의 경합(Contention)이 심화되어 스케일링이 어려웠습니다.
- **CC-NUMA 등장**: 캐시 일관성 프로토콜(Cache Coherency Protocol)을 유지하면서 메모리를 분산시켜 확장성을 확보했습니다.
- **비대칭성 비용**: Interconnect(AMD의 Infinity Fabric, Intel의 QPI/UPI)를 거쳐 타 노드 메모리에 접근할 경우, 액세스 지연이 로컬 대비 1.5~2배 이상 증가할 수 있으며, 이는 실무 레이턴시에 민감한 금융 거래 시스템이나 실시간 분석 시스템에서 치명적입니다.

**3. First-Touch 정책의 이해**
리눅스 커널은 기본적으로 **Demand Paging**과 **First-Touch** 전략을 사용합니다. 즉, 프로세스가 `malloc()` 등으로 메모리를 요청한다고 즉시 물리 메모리와 매핑하지 않고, 실제 데이터가 기록되는(Write) 시점에 현재 실행 중인 CPU가 속한 노드에 메모리 페이지를 할당합니다. 따라서 초기화 코드가 실행되는 CPU 위치가 곧 메모리 위치를 결정합니다.

> **💡 개요 비유**: NUMA는 '여러 멤버가 사는 대형 하우스'와 같습니다. 거실(공유 메모리)에 있는 냉장고를 모두가 쓰러 가면 복잡하지만, 각 방에 냉장고(로컬 메모리)를 두고 쓰면 편리하지만, 다른 방 냉장고를 쓰러 갈 때는 복도를 지나야 해서 시간이 더 걸립니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. NUMA 시스템의 구성 요소**
NUMA 시스템을 이해하기 위해서는 물리적 구성 요소와 이를 추상화하는 소프트웨어 요소를 명확히히 해야 합니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 관련 프로토콜/명령어 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Node** | CPU + 메모리의 그룹 | 독립적인 메모리 컨트롤러를 가진 최단 단위 | - | 독립된 방 |
| **Interconnect** | 노드 간 연결망 | QPI, UPI, HyperTransport 등을 통해 데이터 전송 | MESI Protocol | 복도 통로 |
| **Local Memory** | 해당 노드에 직결된 메모리 | 낮은 Latency, 높은 Bandwidth로 접근 | - | 내 방 금고 |
| **Remote Memory** | 타 노드에 위치한 메모리 | Interconnect를 경유하여 접근, Latency 증가 | - | 친구 방 금고 |
| **OS Kernel Scheduler** | 스레드/메모리 배치 | 로드 밸런싱과 NUMA Balancing 수행 | `sched_setaffinity` | 집안 총무 |

**2. NUMA 노드 구조 및 데이터 플로우 ASCII**
아래는 2개의 소켓(Node 0, Node 1)으로 구성된 전형적인 NUMA 서버의 아키텍처입니다. Interconnect(예: Intel UPI)를 통해 노드 간 통신이 발생함을 확인할 수 있습니다.

```text
       [Node 0 (Socket 0)]                     [Node 1 (Socket 1)]
+-----------------------------+        +-----------------------------+
|  CPU Package (Package 0)    |        |  CPU Package (Package 1)    |
| +-------------------------+ |        | +-------------------------+ |
| | Core 0  (Thread t0)     | |        | | Core 8  (Thread t8)     | |
| | Core 1  (Thread t1)     | |        | | Core 9  (Thread t9)     | |
| |      L3 Cache (Shared)  | |        | |      L3 Cache (Shared)  | |
| +-------------------------+ |        | +-------------------------+ |
|       IMC (Memory Ctrl 0)   |        |       IMC (Memory Ctrl 1)   |
+-------------|---------------+        +---------------|-------------+
              |                                     |
      Local Access (Fast)                  Local Access (Fast)
              |                                     |
      +-------|-----------------------+-------------|-------+
      |       |                       |             |       |
      |  [DDR Channel A]         [DDR Channel B]   |  [DDR] |
      |  (Physical RAM 0)                          | (RAM 1)|
      +---------------------------------------------+--------+
                        ^
                        |  Interconnect (QPI/UPI)
                        |  (High Latency Path)
                        +-------------------------> [ Remote Access ]
```

*   **해설**:
    1.  **CPU Package**: 각 소켓은 여러 개의 코어와 공유 L3 캐시, 그리고 독립적인 IMC (Integrated Memory Controller)를 포함합니다.
    2.  **Local Access**: Core 0이 Node 0의 메모리에 접근할 때는 내부 버스를 거치므로 지연 시간이 최소화됩니다 (약 80~100ns).
    3.  **Remote Access**: Core 0이 Node 1의 메모리를 필요로 할 경우, QPI/UPI (Ultra Path Interconnect) 라인을 통해 요청을 보냅니다. 이 과정에서 추가적인 프로토콜 오버헤드가 발생하며 지연 시간이 크게 증가합니다 (약 150~200ns 이상).

**3. 핵심 동작 원리 및 알고리즘**
리눅스 커널의 메모리 할당자는 페이지 할당 시 `struct page` 구조체의 `NUMA node` ID를 참조합니다. `numactl`은 이 과정에 개입하여 **페이지 할당 정책(Page Allocation Policy)**을 변경합니다.

-   **MPOL_BIND (Membind)**: 특정 노드의 메모리만 사용하도록 강제. 해당 노드 메모리가 부족하면 할당 실패(ENOMEM) 발생. 결정론적 성능이 필요할 때 사용.
-   **MPOL_INTERLEAVE**: 할당 요청을 Round-Robin 방식으로 여러 노드에 분산. 스트라이드 접근 패턴이 있는 대용량 데이터 처리 시 대역폭을 극대화함.
-   **MPOL_PREFERRED**: 지정한 노드를 우선 선호하지만, 부족할 경우 타 노드 사용.

**4. 실무 레벨 코드 (numactl 활용)**
```bash
# 1. 시스템의 NUMA 하드웨어 구조 확인
$ numactl -H
available: 2 nodes (0-1)
node 0 cpus: 0 1 2 3 4 5 6 7
node 0 size: 64036 MB
node 1 cpus: 8 9 10 11 12 13 14 15
node 1 size: 64512 MB

# 2. 특정 노드(Node 0)에 CPU와 메모리를 모두 바인딩하여 서버 실행
# --cpunodebind: CPU 실행 노드 고정
# --membind: 메모리 할당 노드 고정
$ numactl --cpunodebind=0 --membind=0 ./my_database_server

# 3. 메모리는 Node 0에 할당하되, CPU는 Node 1에서 실행 (비추천 테스트 케이스)
$ numactl --cpunodebind=1 --membind=0 ./high_latency_app
```

> **📢 섹션 요약 비유**: 마치 복잡한 **대형 도시의 고속도로 체계**와 같습니다. 출근길(프로세스 실행)에 본인 집(로컬 메모리) 바로 앞 고속도로를 이용하면 빠르지만, 다른 도시에 사는 친구 집(원격 메모리)을 가려면 복잡한 시내를 지나는 고속터미널(Interconnect)을 거쳐야 하므로 시간이 배로 걸립니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 정량적 기술 비교: UMA vs NUMA**
기술적 의사결정을 위해 지표를 명확히 합니다.

| 구분 (Criteria) | UMA (SMP) | NUMA | 비고 (Notes) |
|:---|:---|:---|:---|
| **메모리 접근 시간** | 모든 CPU에 대해 동일 (Uniform) | **비균등 (Non-Uniform)** | 로컬:원 remote 약 1.5~2배 차이 |
| **확장성 (Scalability)** | 낮음 (버스 병목) | **높음 (CC-NUMA)** | 수백 코어까지 가능 |
| **프로그래밍 난이도** | 낮음 (OS가 투명하게 처리) | **높음 (Aware 필요)** | `numactl`, `mbind` 시스템 콜 이해 필요 |
| **주요 사용 사례** | 일반 PC, 소형 서버 | **엔터프라이즈 서버, HPC** | 대용량 인메모리 DB 등 |

**2. 타 영역과의 융합 (OS & Network & AI)**
-   **OS 커널 (CFS & NUMA Balancing)**:
    최신 리눅스 커널은 `Automatic NUMA Balancing` 기능을 포함합니다. 커널은 주기적으로 프로세스의 메모리 접근 패턴을 스캔하여(Scanning), 원격 메모리 접근이 빈번한 페이지를 로컬 노드로 **Migration(이주)** 시킵니다. 이는 OS의 `Page Fault` 핸들링과 밀접하게 연결됩니다.
-   **네트워크 (IRQ Affinity)**:
    고속 패킷 처리가 필요한 시스템에서, 특정 NIC (Network Interface Card)의 인터럽트(IRQ)가 발생했을 때 이를 처리하는 CPU가 동일한 노드에 있지 않으면, 패킷 처리 과정에서 캐시 미스(Cache Miss)가 빈번해집니다. 따라서 `irqbalance` 데몬이나 `set_irq_affinity` 스크립트를 통해 **NIC와 같은 NUMA 노드에 할당된 코어**에서 인터럽트를 처리하도록 설정해야 대기열(Queue) 병목을 막을 수 있습니다.
-   **AI/딥러닝 (GPU Direct)**:
    GPU가 NUMA 특정 노드에 연결된 PCIe 장치인 경우, GPU 학습 데이터를 메모리에 올릴 때 반드시 해당 **NUMA 노드의 로컬 메모리**에 할당해야 합니다. 그렇지 않으면 GPU로 데이터를 복사하는 시간(DMA)이 느려져 학습 속도가 저하됩니다.

> **📢 섹션 요약 비유**: 소방서의 **출동 배차 시스템**과 같습니다. 사고가 난 지역(데이터 요청)과 가장 가까운 소방서(로컬 노드)의 차량을 출동시키는 것이 가장 빠르지만, 만약 그 소방서에 차량이 없다면 다음 가까운 소방서(원격 노드)의 지원을 받아야 하므로 도착 시간이 지연됩니다. 이 상황을 미리 예측하고 차량을 배치하는 것이 융합 관점의 핵심입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 매트릭스**

| 시나리오 | 최적 전략 (Action) | 예상 성능 향상 (ROI) |
|:---|:---|:---|
| **OLTP 데이터베이스**<br>(높은 동시성, 낮은 지연) | `--membind`와 `--cpunodebind`를 사용해 특정 노드에 격리(Isolation). | Latency 20% 감소, TPS 15% 증가 |
| **분석 쿼리 (OLAP)**<br>(순차 처리, 대용량 스캔) | `--interleave=all` 사용. 전체 메모리 대역폭을 극대화. | 스캔 속도 1.5~2배 향상 |
| **가상화 호스트 (KVM)** | vCPU 피닝(Pinning) 및 VM 메모리를 특정 노드에 설정 (vNUMA). | VM 간 간섭 감소, 예측 가능한 성능 |

**2. 도입 체크리스트**

-   **[ ] 하드웨어 점검**: `lscpu` 또는 `numactl -H`를 통해 실제 물리적 소켓 구성을 확인했는가?
-   **[ ] 워크로드 분석**: 메모리 집약적(Memory-bound) 작업인가, 연산 집약적(Compute-bound) 작업인가?
-   **[ ] 현재 상태 모니터링**: `numastat`를 통해 `numa_hit` 대비 `numa_miss`, `numa_foreign` 비율을 측정했는가?
-   **[ ] 설정 적용**: 프로세스 실행 시 `numactl`을 적용하거나, `systemd` 서비스 유닛에 `NUMAPolicy` 설정을 반영했는가?

**3. 안티패턴 (Anti-Pattern) 주의사항**

-   **Cross-Node Memory Allocation**: 프로세스는 Node 0에서 실행되는데, 메모리를 `numactl --membind=1`을 통해 N