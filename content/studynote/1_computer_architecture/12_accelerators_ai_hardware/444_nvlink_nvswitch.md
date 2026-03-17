+++
title = "NVLink / NVSwitch"
date = "2026-03-14"
weight = 444
+++

# NVLink / NVSwitch

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NVLink (NVIDIA High-Speed Interconnect)는 GPU 간 병목을 제거하기 위한 초고대역폭·저지연 상호 연결 기술이며, NVSwitch는 이를 망(Fabric) 형태로 확장하여 다수의 GPU를 완전 연결(Full-mesh) 토폴로지로 묶는 고성능 스위칭 아키텍처입니다.
> 2. **가치**: 기존 PCIe (Peripheral Component Interconnect Express) Gen5 대비 최대 14배 이상의 대역폭을 제공하여, 대규모 AI 모델 학습 시 필수적인 집합 통신(Collective Communication) 성능을 극대화하고 시스템 전체의 MFU (Model FLOPS Utilization)를 획기적으로 개선합니다.
> 3. **융합**: CPU 중심의 폰 노이만 구조를 넘어, GPU가 직접 메모리를 관리하고 통신하는 가속기 중심 아키텍처(Accelerator-Centric Architecture)의 핵심 기반이며, AI 데이터센터와 HPC (High-Performance Computing) 인프라의 표준으로 자리 잡았습니다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 정의**
NVLink는 NVIDIA가 개발한 직렬 점대점(Serial Point-to-Point) 상호 연결 기술로, GPU(Graphics Processing Unit) 간, 또는 GPU와 CPU 간의 데이터 병목 현상을 해결하기 위해 설계되었습니다. 기존 범용 인터페이스인 PCIe가 호스트 시스템의 복잡한 계층 구조를 거쳐야 했던 것과 달리, NVLink는 GPU 간 직접적인 데이터 경로를 제공합니다. NVSwitch는 이러한 NVLink 링크들을 집약하여, 최대 18개(Blackwell 아키텍처 기준)의 GPU를 서로 완전 연결된 단일 논리 시스템으로 통합하는 고속 스위칭 패브릭입니다.

**💡 기술적 비유**
마치 도심의 좁은 골목길(PCIe)로 수백 대의 화물차가 오가며 병목을 일으키던 것을, 16차선 초고속 도로(NVLink)와 거대한 입체 교차로(NVSwitch)를 건설하여, 모든 화물차가 신호 대기 없이 직행으로 이동할 수 있게 만든 것과 같습니다.

**등장 배경 및 기술적 필요성**
1.  **PCIe 대역폭의 한계**: 딥러닝 연산량은 피코(FLOPs) 단위로 폭발하지만, 데이터를 이동시키는 인터커넥션 대역폭은 기하급수적으로 증가하지 못했습니다. AI 모델 학습의 90% 이상이 통신 대기 시간(Idle time)으로 소모되는 'Memory Wall' 문제가 심각했습니다.
2.  **강결합(Fine-grained) 병렬화의 등장**: 거대 언어 모델(LLM)을 학습시키기 위해 텐서 병렬화(Tensor Parallelism)가 필수적이 되었습니다. 이는 연산 중 GPU 간 실시간 데이터 합산(All-Reduce)이 빈번하게 일어나며, PCIe의 수십 마이크로초(µs) 수준 지연 시간은 용납할 수 없는 수준이었습니다.
3.  **Coherency 일관성**: 이기종 간 통신(CPU-GPU)뿐만 아니라 GPU 간 캐시 일관성(Cache Coherency)을 유지하기 위한 하드웨어적 지원이 필요했습니다.

📢 **섹션 요약 비유**: 각자의 방에 고립되어 인터폰으로 대화하던(CPU 주변장치 방식) 팀원들을, 칸막이를 모두 헐어버린 통합 오픈플랜 사무실(NVLink Unified Memory)로 이주시켜, 말하지 않아도 서로의 화면을 실시간으로 확인하고 협업할 수 있게 한 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

NVLink와 NVSwitch의 아키텍처는 물리적 계층(Physical Layer)에서 프로토콜, 그상위의 토폴로지까지 고도로 최적화되어 있습니다.

**[구성 요소 상세 분석]**
| 요소명 | 역할 및 정의 | 내부 동작 메커니즘 | 핵심 프로토콜/지표 | 비유 |
|:---|:---|:---|:---|:---|
| **NVLink Controller** | GPU 내부의 호스트 인터페이스 | 데이터 패킷을 송수신하며 Flow Control, CRC(Cyclic Redundancy Check) 오류 수정 수행 | 4th Gen: 50GB/s/lane (H100) | 송수신관제탑 |
| **NVSwitch Chip** | 비차단(Non-blocking) 교환기 | 12.8Tbps/s 이상의 처리 용량을 가진 Crossbar 스위치로, 모든 포트가 동시에 전대역폭 사용 가능 | Cut-through Routing | 거대 환승 터미널 |
| **SerDes (Serializer/Deserializer)** | 아날로그 신호 처리 | 병렬 데이터를 고속 직렬 신호로 변환하여 전송선로를 통해 전송 | PAM4 (Pulse Amplitude Modulation) | 고속 광케이블 변환기 |
| **SMI (Stream Management Interface)** | NVIDIA 네트워크 제어 프로토콜 | In-band 통신을 통해 GPU의 전력, 온도, 성능 메트릭을 원격으로 모니터링 및 제어 | TCP/IP 기반 제어 | 원격 제어 시스템 |
| **P2P (Peer-to-Peer) DMA** | GPU 간 직접 메모리 접근 | CPU 개입 없이 GPU A가 GPU B의 VRAM에 직접 데이터 쓰기 가능 | Atomic Operations 지원 | 택배사의 물류 허브 직송 |

**[NVLink/NVSwitch 아키텍처 데이터 흐름도]**
아래 다이어그램은 NVSwitch를 통해 GPU들이 Full-mesh로 연결된 구조를 보여줍니다. 모든 GPU는 스위치를 통해 다른 모든 GPU에 대해 동등한 대역폭을 가집니다.

```
     +--------------------- Block 1 ---------------------+
     |          (NVLink Fabric over NVSwitch)            |
     |                                                    |
     |   [GPU 0] <---> [GPU 1] <---> [GPU 2] <---> [GPU 3] |
     |      |  ^   ^       |  ^   ^       |  ^   ^       |  |
     |      v  |   |       v  |   |       v  |   |       |  |
     |   +------------------------------------------------+ |
     |   |           NVSwitch Complex (NVLink Switch)      | |
     |   +------------------------------------------------+ |
     |      ^  |   |       ^  |   |       ^  |   |       |  |
     |      |  v   |       |  v   |       |  v   |       |  |
     |   [GPU 4] <---> [GPU 5] <---> [GPU 6] <---> [GPU 7] |
     |                                                    |
     +------------------------------------------------------+
     
     < Legend >
     <---> : NVLink Link (100GB/s+ per link, bidirectional)
       ^|v : Connection points to Switch Fabric
```

**심층 동작 원리 및 기술**
1.  **Lane Aggregation (레인 집적화)**:
    NVLink는 기본적으로 높은 대역폭을 위해 여러 개의 랜(Lane)을 묶어서 사용합니다. 예를 들어, 4세대 NVLink(H100 기준)는 하나의 링크(Link)가 4개의 랜(Lane)으로 구성되며, 각 랜은 25GB/s(GT/s)의 속도를 내어 총 100GB/s의 전이중(Full-duplex) 대역폭을 제공합니다. 하나의 GPU는 보통 18~24개의 NVLink 포트를 가지며, 이를 통해 단일 GPU는 총 900GB/s~1.8TB/s의 탈중앙화된 I/O 성능을 확보합니다.

2.  **Non-blocking Switching (비차단 스위칭)**:
    NVSwitch 내부는 크로스바(Crossbar) 구조로 설계되어, 입력 포트가 다른 출력 포트를 사용할 때 경합이 발생하지 않습니다. 즉, GPU 0이 GPU 7에게 데이터를 보내는 동안, GPU 1과 GPU 4도 최대 대역폭으로 통신할 수 있습니다. 이는 `N x (대역폭)`의 총 시스템 대역폭을 보장합니다.

3.  **SHARP (Scalable Hierarchical Aggregation and Reduction Protocol)**:
    기존 네트워크에서는 데이터가 목적지에 도착해야 연산이 가능했습니다. 하지만 NVSwitch와 InfiniBand 네트워크 등에 탑재된 SHARP 기술은 스위치 내부에서 전송 중인 데이터를 가지고 연산(주로 Reduce, Sum 등)을 수행한 뒤 결과만 전달합니다. 이를 통해 통신 트래픽을 절반으로 줄이고 지연 시간을 획기적으로 단축합니다.

```c
/* Pseudo Code: NVLink Accelerated All-Reduce
 * [기존 PCIe 방식] vs [NVLink/NVSwitch 방식 비교]
 */

// CASE 1: PCIe 방식 (CPU 메모리 거쳐감)
// Latency: ~50µs (Host Memory Copy Overhead)
cudaMemcpyAsync(&h_buf[0], &d_buf[0], size, D2H, stream0); // GPU -> CPU
reduce_on_host(&h_result);                                // CPU Calc
cudaMemcpyAsync(&d_final, &h_result, size, H2D, stream0); // CPU -> GPU

// CASE 2: NVLink P2P (GPU Direct Access)
// Latency: ~5µs (Kernel launch + Direct transfer)
// PCIe 버스를 우회하고 NVLink를 통해 다른 GPU의 VRAM에 직접 접근
cudaMemcpyPeerAsync(&d_dest[1], 1, &d_src[0], 0, size);   // GPU 0 -> GPU 1 Direct

// CASE 3: SHARP/Collective Offload (스위치 내부 연산)
// Latency: Minimal
// 데이터 전송 과정에서 스위치가 알아서 덧셈을 완료하고 리턴
// ncclAllReduce(...) // NCCL이 NVLink 토폴로지를 인식하여 SHARP 최적화 경로 선택
```

📢 **섹션 요약 비유**: 모든 시민이 서로 직통 전화선을 깐 것이 아니라, 거대한 전화 교환국(NVSwitch)을 설치하고, 가로수를 건드리지 않고 지하에 케이블을 묻어(NVLink) 트래픽 무료·무제한 통화망을 구축한 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

NVLink 기술은 단순한 하드웨어 속도 향상을 넘어, 시스템 아키텍처와 알고리즘, 네트워크 프로토콜 전반에 영향을 미칩니다.

**[상호 연결 기술 심층 비교]**

| 구분 | PCIe Gen5 x16 | NVLink 4.0 (Hopper) | InfiniBand NDR400 |
|:---|:---|:---|:---|
| **Raw Bandwidth** | 64 GB/s (Uni-direction) | 450 GB/s (Bi-direction, per GPU) | 50 GB/s (per port, per direction) |
| **Latency** | ~200 ns (PHY) + SW Overhead | ~25 ns (Extremely Low) | Network Stack dependent (~500ns+) |
| **Topology** | Root Complex - Endpoint Tree | Full-Mesh / 2D Torus | Fat-Tree / Dragonfly |
| **Memory Access** | DMA (Limited) | P2P Access + Atomic | RDMA (Remote DMA) |
| **Primary Use** | Host (CPU) <-> Device (GPU) | Device <-> Device (Scale-up) | Node <-> Node (Scale-out) |
| **Protocol Overhead**| Heavy (TCP/IP overhead if used) | Lightweight (Native) | Medium (IPoIB/RoCE) |

**[과목 융합 관점 분석]**
1.  **운영체제(OS) & 가상화**:
    NVLink는 IOMMU (Input-Output Memory Management Unit) 수준에서 `P2P (Peer-to-Peer)` 접근을 지원합니다. 이를 통해 OS 커널은 서로 다른 GPU의 물리 메모리 주소 공간을 하나의 논리적 주소 공간으로 매핑(`CXL` 유사 개념)할 수 있습니다. 즉, `cudaMalloc()`을 할 때, GPU 0의 메모리가 부족하면 OS는 투명하게 GPU 1의 메모리를 할당하여 애플리케이션 장애 없는 메모리 확장(Overcommit)을 지원합니다.

2.  **알고리즘(Algorithm) & 소프트웨어 스택**:
    NVLink의 존재는 `NCCL (NVIDIA Collective Communications Library)`의 알고리즘을 변화시켰습니다.
    - **Ring All-Reduce (PCIe 시대)**: GPU가 원형으로 연결되어 데이터를 순차적으로 전달. 병목이 존재.
    - **Tree/Sharp Reduce (NVLink 시대)**: Full-mesh 구조를 활용하여 트리 형태의 계층적 집합을 수행하거나, NVSwitch 내부에서 바로 연산을 완료하여 통신 비용을 $O(N)$이 아닌 $O(\log N)$ 수준으로 최적화합니다.

**[도입 의사결정 매트릭스: 비용 대비 성능]**
워크로드가 **CPU 연산이 많거나**, 데이터 전송이 **배치 단위로 드문드문 발생(Bulk Transfer)**한다면 PCIe만으로 충분합니다. 하지만 **거대 트랜스포머 모델(GPT, BERT 등)**의 학습처럼, 매 레이어마다 미니배치(Mini-batch)의 Gradient를 합산해야 하는 경우, NVLink는 선택이 아닌 필수 생존 전략이 됩니다.

📢 **섹션 요약 비유**: 일반 국도(PCIe)는 화물 트럭이 느리더라도 많은 양을 운반하는 데 적합하지만, 긴급 팀즈원(KT-ATM)이나 대형 병원 간 장기 이송처럼 시간이 곧 돈인 경우에는 전용 헬기패드(NVLink)가 있어야만 생사가 결정됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

NVLink/NVSwitch 기술을 도입할 때는 단순한 성능 향상을 넘어 총소유비용(TCO)과 워크로드 특성을 분석한 전략적 의사결정이 필요합니다.

**[실무 시나리오 및 의사결정 프로세스]**

**1. 시나리오: 대규모 LLM 서비스 구축 (LLM Serving)**
- **문제**: 수백억 개 파라미터 모델을 단일 GPU(80GB VRAM)에 담을 수 없음.
- **의사결정**: NVLink를 통해 8개의 GPU를 하나의 논리적 유닛(MIG 없이)으로 묶는 `Tensor Parallelism` 전략 채택.
- **결과**: 모델 무게 제약 해소, 추론 Latency 획기적 감소.

**2. 시나리오: 과학 기술 시뮬레이션 (CFD)**
- **문제**: 3차원 유체 역학 격자(Grid) 데이터의 경계(Boundary) 정보 교환이 매우 잦