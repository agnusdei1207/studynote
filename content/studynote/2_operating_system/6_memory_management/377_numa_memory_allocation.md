+++
title = "Title"
date = "2026-03-14"
[extra]
+++

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**1. 정량적 기대효과 및 ROI 분석**
NUMA 아키텍처의 최적화된 적용은 시스템의 처리량과 응답 속도에 결정적인 영향을 미칩니다. 특히 **SMP (Symmetric Multi-Processing)**의 확장성 한계를 극복하여, 대규모 서버 환경에서 선형적인 성능 향상을 기대할 수 있습니다.

| 지표 (Metric) | 최적화 전 (UMA/비최적화) | 최적화 후 (NUMA Aware) | 비고 (Remark) |
|:---:|:---:|:---:|:---|
| **메모리 대역폭** | 공유 버스 대역폭에 의해 제한 (예: ~100 GB/s) | 노드별 대역폭 합산 (예: 200+ GB/s) | 소켓 수에 비례하여 증가 |
| **접근 지연시간 (Latency)** | 원격 접근 빈도 높음 (평균 100ns+ 이상 지연) | 로컬 접근 유도 (지연 최소화, ~60ns 유지) | **TLB (Translation Lookaside Buffer)** Miss 감소 효과 |
| **TPS (Transactions Per Sec)** | Memory Bus Contention으로 병목 발생 | CPU Core 수에 따른 선형적 스케일링 달성 | **RTO (Recovery Time Objective)** 단축에 기여 |
| **시스템 확장성** | 8~16코어 이상에서 성능 포화 | 수백 코어 환경까지 효율적인 자원 활용 | TCO (Total Cost of Ownership) 절감 |

**2. 미래 전망 및 진화 방향**
-   **CXL (Compute Express Link)**: 기존의 NUMA 인터커넥트보다 훨씬 빠르고 유연한 **CXL (Compute Express Link)** 표준의 등장으로, CPU와 가속기(**GPGPU**, **FPGA**) 간의 메모리 코히어런시(Coherency)가 유지되는 "새로운 형태의 NUMA"가 등장하고 있습니다. 이는 메모리 풀링(Memory Pooling)을 가능하게 하여 클라우드 자원의 효율을 혁신적으로 개선할 것입니다.
-   **Chiplet Architecture**: Intel 및 AMD가 밀려주는 **Chiplet** 기반의 프로세서 설계는 패키지 내부에 여러 개의 다이(Die)를 연결하는 구조로, 내부적으로도 NUMA 도메인이 세분화되고 있습니다. 이에 따라 OS 스케줄러와 미들웨어의 세밀한 NUMA 인식이 더욱 중요해질 것입니다.

**3. 관련 표준 및 법규**
-   **ACPI (Advanced Configuration and Power Interface)**: 시스템의 하드웨어 구성(NODE, 거리 행렬 등)을 OS에 설명하는 표준 인터페이스로, **SRAT (System Resource Affinity Table)**와 **SLIT (System Locality Information Table)**을 통해 NUMA 토폴로지를 정의합니다.
-   **ISO/IEC 23001**: 멀티미디어 코덱의 병렬 처리를 위한 아키텍처 가이드 등에서 메모리 액세스 패턴의 최적화를 권고하고 있습니다.

### 📢 섹션 요약 비유
도시가 커지는 과정에서 단일 도심(UMA) 위주의 개발은 교통 체증을 유발합니다. 하지만 여러 개의 자족적인 도시권(NODE)을 건설하고 그 사이를 고속철도(CXL/QPI)로 연결하면(NEW URBAN PLANNING), 전체 국토의 용량과 처리 속도(TPS)를 비약적으로 높일 수 있습니다. NUMA는 이러한 거대 도시 설계의 청사진입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
-   **CPU Affinity**: 프로세스를 특정 코어에 묶는 기술로, NUMA 노드 고정의 선결 조건임.
-   **Huge Page (HugeTLB)**: 대용량 메모리 페이지를 사용하여 **TLB (Translation Lookaside Buffer)** Miss를 줄이며, NUMA 노드 간의 페이지 이동 오버헤드를 감소시킴.
-   **RDMA (Remote Direct Memory Access)**: 네트워크를 통해 원격 메모리에 직접 접근하는 기술로, NUMA의 개념을 네트워크 단위로 확장한 기술임.
-   **Non-Uniform Memory Access (NUMA)**: (현재 문서)
-   **Cache Coherence**: 다중 프로세서가 캐시 일관성을 유지하는 메커니즘(MESI 프로토콜 등)으로, NUMA 인터커넥트의 기반이 됨.

### 👶 어린이를 위한 3줄 비유 설명
1.  **내 방 책상(Local Memory)**: 학교에서 내 책상에 있는 물건은 바로 꺼내 쓸 수 있는 것처럼, 컴퓨터도 자신이 가장 가까이에 있는 메모리를 제일 빨리 사용합니다.
2.  **친구 방 책상(Remote Memory)**: 하지만 다른 반 친구의 책상에 있는 물건을 가져오려면 복도를 걸어가서 허락을 구해야 하니까 시간이 훨씬 오래 걸리겠죠? 이것이 NUMA의 핵심입니다.
3.  **정리 정돈(Allocation Policy)**: 그래서 우리가 물건을 사용할 때, 내 책상에 없는 물건을 자꾸 친구 책상에서 찾지 않도록, 처음부터 내 책실에 둘 곳을 잘 정해놓는 것이 중요합니다.