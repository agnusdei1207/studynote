+++
title = "809-814. 스토리지 및 HPC 네트워킹 (RDMA, InfiniBand)"
date = "2026-03-14"
[extra]
category = "Data Center & Cloud"
id = 809
+++

# 809-814. 스토리지 및 HPC 네트워킹 (RDMA, InfiniBand)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존 TCP/IP 스택의 CPU 및 메모리 복사 오버헤드를 제거하여, 네트워크 경로를 통해 원격 메모리에 직접 접근하는 **Zero-copy(무복사)** 아키텍처가 핵심입니다.
> 2. **가치**: AI 훈련 및 HPC (High-Performance Computing) 환경에서 마이크로초(µs) 단위의 초저지연(Low Latency)과 100Gbps~400Gbps 이상의 대역폭을 확보하여 연산 성능을 극대화합니다.
> 3. **융합**: 스토리지 프로토콜(iSCSI, FCP)의 성능 한계를 극복하기 위해 이더넷(RoCE)과 전용 인터커넥트(InfiniBand)의 진화가 융합되고 있습니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**스토리지 네트워킹(Storage Networking)**은 서버의 호스트 버스 어댑터(HBA)와 스토리지 장치 간의 데이터 경로를 최적화하는 기술 분야입니다. 초기에는 DAS (Direct Attached Storage)에서 시작하여, 네트워크의 등장과 함께 SAN (Storage Area Network)과 NAS (Network Attached Storage)로 분화되었습니다. 그러나 빅데이터와 AI 시대가 도래하면서, 기존의 소프트웨어 기반 스택이 가진 처리 속도의 한계가 명확해졌습니다. 이를 해결하기 위해 등장한 패러다임이 바로 하드웨어 가속화된 데이터 전송 기술입니다.

#### 2. 등장 배경: OS 커널 스택의 병목
기존 **TCP/IP (Transmission Control Protocol/Internet Protocol)** 통신은 애플리케이션 데이터가 네트워크로 나가기 위해 여러 번의 **Context Switching(문맥 교환)**과 **Memory Copy(메모리 복사)** 과정을 거쳐야 합니다.

```ascii
+----------------------+     Context Switch     +----------------------+
| Application Space    | <---------------------> |    Kernel Space      |
| (User Buffer)        |                        | (Socket Buffer)      |
+----------------------+                        +----------------------+
       | (1) Copy                                       | (2) Copy
       v                                               v
+-----------------------------------------------------------------------+
|                     NIC (Network Interface Card) Driver               |
+-----------------------------------------------------------------------+
       | (3) Copy (DMA)
       v
+-----------------------------------------------------------------------+
|                           Hardware NIC                                |
+-----------------------------------------------------------------------+
```
이러한 과정은 CPU 자원을 소모적으로 낭비하며, AI 학습이나 금융 거래와 같이 초고속 처리가 필요한 현대 환경에서는 치명적인 병목 구간(Bottleneck)으로 작용합니다.

#### 3. 핵심 기술의 분화
이를 극복하기 위해 **NIC (Network Interface Card)**가 CPU의 개입 없이 직접 메모리를 액세스하는 **DMA (Direct Memory Access)** 기능을 원격지로 확장한 **RDMA (Remote Direct Memory Access)** 기술이 등장했습니다. 또한, 이를 지원하는 전용 매체로서 기존 이더넷의 비효율을 제거한 **InfiniBand (IB)**와 기존 이더넷 인프라를 활용하는 **RoCE (RDMA over Converged Ethernet)**가 경쟁하고 있습니다.

> 📢 **섹션 요약 비유**: 기존 네트워크는 우편물을 보낼 때 직원이 매번 본사에 와서 서류를 검사하고 도장을 찍은 뒤에 우체국에 가는 느린 과정이었던 반면, RDMA는 직원이 본사에 보고 없이 집에서 바로 옆 건물 편의함으로 물건을 순간이동 시키는 '다차원 배송 시스템'과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 (RDMA Architecture)
RDMA를 구현하기 위해서는 하드웨어와 소프트웨어의 긴밀한 협조가 필요합니다.

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **HCA / RNIC** | Host Channel Adapter / RDMA NIC | 기존 NIC의 기능에 RDMA 엔진을 탑재. CPU 개입 없이 원격 메모리 기록/읽기 수행 | Verbs API | 배달원이 직접 열쇠를 가진 관리자 |
| **Verbs** | RDMA Verbs (API) | 애플리케이션이 RDMA 장치를 제어하기 위한 표준화된 인터페이스 (Libibverbs 등) | IB verbs, OFED | 배달 요청서 양식 |
| **QP** | Queue Pair (Send/Receive) | 전송 작업을 큐잉하는 메커니즘. SQ(Send Queue)와 RQ(Receive Queue)로 구성 | Work Queue (WQ) | 보낼 편지함과 받을 편지함 |
| **MR** | Memory Region | 애플리케이션이 RDMA 장치에게 접근을 허용할 메모리 영역을 등록 및 PIN 고정 | Key-based Access | 배달 허용된 나의 창고 구역 |
| **CQ** | Completion Queue | 완료된 작업의 결과를 애플리케이션에게 비동기적으로 알려주는 큐 | Polling/CQE | 배달 완료 알림 표시판 |

#### 2. Zero-copy 데이터 전송 흐름
아래는 TCP/IP와 RDMA의 데이터 경로를 비교한 아키텍처 다이어그램입니다.

```ascii
[TCP/IP Legacy Stack vs. RDMA Stack]

LEGACY TCP/IP PATH (High CPU Usage):
+-----------+    Copy    +-----------+    Copy    +-----------+
|  User App | --------> |  Kernel   | --------> |  NIC HW   |
|  Buffer   |           |  Socket   |           |  Buffer   |
+-----------+           +-----------+           +-----------+
      ^                        |  Copy              |
      |________________________|___________________|
   (Interrupt & Context Switch Overhead)

RDMA PATH (Zero Copy, Kernel Bypass):
+-----------+                               +-----------+
|  User App | ===========================> |  NIC HW   |
|  Buffer   |    Direct Data Placement     |  Wire     |
+-----------+          (DMA Engine)        +-----------+
      |                                    |
      | <--- Completion Event (CQE) -------|
```

**[다이어그램 해설]**
RDMA의 가장 큰 특징은 **Kernel Bypass(커널 우회)**와 **Zero-copy(무복사)**입니다.
1. **Legacy 방식**: 데이터는 Application Buffer → Kernel Socket Buffer → NIC Driver Buffer → NIC Hardware로 이동하며 3~4번의 메모리 복사가 발생합니다. 또한 패킷 도착 시 CPU에게 인터럽트를 걸어 커널이 처리해야 하므로 오버헤드가 큽니다.
2. **RDMA 방식**: 애플리케이션은 OS Kernel을 거치지 않고, HCA(RDMA NIC)에게 명령을 내립니다. HCA는 직접 Application Buffer의 데이터를 읽어 Wire로 내보냅니다. 수신 측에서도 NIC가 직접 Application Buffer에 데이터를 기록합니다. 이 과정에서 CPU는 단지 명령을 내리는 작업(Queue Posting)만 수행하며 실제 데이터 이동(DMA)은 하드웨어가 담당합니다.

#### 3. 핵심 기술: 동작 메커니즘
RDMA 동작의 핵심은 **메모리 등록(Memory Registration)**과 **키토큰(Key Token)** 교환입니다.
*   **Step 1 (Exchange)**: 연결 초기, 양쪽 노드는 자신의 메모리 주소(VA)와 접근 키(Key)를 정보를 교환합니다(Side Channel, TCP 등 활용).
*   **Step 2 (Post Send)**: 발신지 애플리케이션은 Send Queue에 작업을 등록합니다. 이때 데이터가 아닌 "어디(Address)에서 얼마나(Length) 읽을지"에 대한 포인터 정보를 전송합니다.
*   **Step 3 (RDMA Read/Write)**: 수신 측 NIC는 자신의 메모리에 직접 데이터를 쓰거나(Write), 발신 측이 요청하면 원격 메모리를 읽어(Read) 보냅니다. 이 모든 과정은 OS Kernel overhead 없이 진행됩니다.

> 📢 **섹션 요약 비유**: RDMA는 마치 국가 기관의 복잡한 행정 절차(커널 스택)를 거치지 않고, 대사관 직원(HCA)이 상대국 대사의 금고(메모리)에 직접 접근할 수 있는 특별한 '외교 면책권'을 가진 것과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RDMA 전송 프로토콜 심층 분석
RDMA를 구현하는 대표적인 3가지 전송 프로토콜을 비교 분석합니다.

| 구분 | InfiniBand (IB) | RoCE v2 (RDMA over Converged Ethernet) | iWARP (Internet Wide Area RDMA Protocol) |
|:---|:---|:---|:---|
| **전송 계층** | 전용 링크 계층 (IB Layer) | UDP/IP (L3) | TCP/IP (L4) |
| **네트워크** | 전용 스위치 및 케이블 | 일반 기가/10기가/이더넷 스위치 | 일반 IP 네트워크 |
| **성능 (Latency)** | **최우수** (1µs 미만 가능) | 우수 (Sub-10µs, ECN/PFC 의존) | 양호 (TCP 오버헤드로 인해 IB/RoCE 저하) |
| **Lossless 지원** | 하드웨어 Credit 기반 Flow Control | PFC (Priority Flow Control) + ECN 필요 | TCP의 혼잡 제어(Congestion Control) 의존 |
| **활용도** | AI 슈퍼컴퓨터, HPC | AI 데이터센터(NVIDIA, Meta), 일반 DC | 구형 스토리지, 원격 RDMA |
| **비용** | 매우 높음 (전용 장비) | 중간 (이더넷 인프라 활용 가능) | 낮음 (기존 장비 활용) |

#### 2. 스토리지 프로토콜과의 융합 (NVMe over Fabrics)
스토리지 영역에서도 RDMA의 장점을 취하기 위해 **NVMe over Fabrics (NVMe-oF)** 기술이 등장했습니다. 기존 SATA/SAS의 버스 병목과 이더넷 스토리지(iSCSI)의 소프트웨어 병목을 동시에 해결합니다.

```ascii
[NVMe-oF RDMA Transport Flow]

Host (Server)              Network (InfiniBand/RoCE)              Target (Storage)
+-------------+                                             +-------------+
| NVMe Driver |                                             | NVMe Subsys  |
+------+------+                                             +------+------+
       |                                                      |
       | 1. Capsule/CMD (RDMA Write)                          |
       |---> RDMA NIC (HCA) ====================> RDMA NIC (HCA) --->|
       |                                                      | 2. Parse Cmd
       |                                                      |      |
       |                                                      |      v
       |                                                      |  [Namespace]
       |                                                      |      |
       |                                                      | 3. Data Fetch
       | <================================== RDMA Read/Write <------|
       | 4. Completion (CQE)                                    |
       v                                                      v
```

**[분석 포인트]**
*   **iSCSI vs NVMe-oF**: iSCSI는 SCSI 명령을 TCP/IP로 캡슐화하지만, CPU 부하가 높고 Latency가 큽니다. NVMe-oF는 RDMA를 통해 **CPU利用率(CPU Utilization)**을 1% 미만으로 유지하며 수백만 IOPS를 달성합니다.
*   **Convergence(융합)**: HPC 네트워크 기술이 스토리지 영역으로 파고들어, 컴퓨팅과 스토리지의 경계를 허무는 **Composable Infrastructure(구성 가능한 인프라)**의 기반이 되고 있습니다.

#### 3. InfiniBand vs Ethernet (Traffic Management)
AI 학습 클러스터에서 InfiniBand가 갖는 특별한 이점은 **Tail Latency(꼬리 지연시간)** 방지입니다. 이더넷은 **ECN (Explicit Congestion Notification)**과 **PFC (Priority Flow Control)**를 통해 Lossless 네트워크를 구현하려 하지만, "Incast"(여러 발신자가 하나의 수신자에게 몰림) 상황에서 Queueing Delay가 발생할 수 있습니다. 반면, InfiniBand는 하드웨어 수준에서 **Adaptive Routing (적응형 라우팅)**을 지원하여 혼잡한 경로를 피해 데이터를 전송합니다.

> 📢 **섹션 요약 비유**: **InfiniBand**는 신호등이 없고 다리가 알아서 넓어지는 과학적으로 설계된 '차세대 스마트 고속도로'이고, **RoCE**는 기존 도로 위에 특수 차량 전용 차로를 그어놓은 'BRT(간선급행버스체계)'와 같으며, **iWARP**는 일반 차량과 섞여 다니며 성능은 보장되지 않지만 어디든 갈 수 있는 '일반 버스'와 같습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 도입 의사결정 매트릭스 (실무 시나리오)

| 시나리오 (Scenario) | 최적 기술 (Optimal Tech) | 의사결정 근거 (Rationale) |
|:---|:---|:---|
| **초대형 AI 훈련 (GPU Cluster)** | **InfiniBand (NDR 400G)** | GPU가 연산을 멈추고 데이터를 기다리는 시간(GPU Bubble)을 최소화해야 함. IB의 **SHARP (Scalable Hierarchical Aggregation and Reduction Protocol)** 기능을 통해 집합 연산(All-Reduce) 네트워크 내에서 수행하여 훈련 속도를 2배 이상 높임. |
| **범용 데이터센터 개편** | **RoCE v2 (Lossless Ethernet)** | 장비 교체 비용(CAPEX)을 줄이면서도 기존 이더넷 관리 체제를 유지해야 함. 최신 스위치(L2/L3)의 PFC/ECN 기능이 충분히 성숙하여 AI/HPC 워크로드를 95% 수준으로 커버 가능. |
| **원격 데이터 복제 (DR)** | **FC (Fibre Channel) or iWARP** | 안정성과 호환성이 중요. 물리적 거리가 멀 경우 TCP 기반의 흐름 제어가 유리할 수 있음. |

#### 2. 기술적/운영적 도입 체크리스트

**[기술적 사항]**
*   [ ] **MTU (Maximum Transmission Unit)** 설정: RDMA 효율을 위해 반드시 **Jumbo Frame (MT