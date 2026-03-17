+++
title = "NVMe-oF (NVMe over Fabrics)"
date = "2026-03-14"
[extra]
+++

# NVMe-oF (NVMe over Fabrics)

+++
title = "NVMe-oF (NVMe over Fabrics)"
weight = 343
+++

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: NVMe-oF는 로컬 PCIe 버스의 고성능 프로토콜을 네트워크 패브릭(Fabric)으로 확장하여, 스토리지 네트워크의 병목을 제거하는 표준화된 캡슐화 기술입니다.
> 2. **가치**: 기존 SAN(Storage Area Network) 대비 **지연 시간(Latency)을 최대 90% 이ward 절감**하고, CPU 오버헤드를 획기적으로 낮추어 데이터센터의 에너지 효율과 처리량을 극대화합니다.
> 3. **융합**: 컴포저블 인프라(Composable Infrastructure)와 AI/ML 워크로드의 필수 인프라로, TCP/IP, RDMA(Remote Direct Memory Access), FC(Fibre Channel) 등 기존 네트워크 계층과 융합하여 스토리지의 유연성을 보장합니다.

---

### Ⅰ. 개요 (Context & Background)

NVMe-oF(NVMe over Fabrics)는 NVMe(Non-Volatile Memory Express) 프로토콜의 범용성을 서버 내부의 PCIe 버스 한계로부터 네트워크 전체로 확장하기 위해 NVM Express Inc.가 표준화한 기술 specification입니다. 기존의 스토리지 네트워크 프로토콜들이 SAS(Serial Attached SCSI)나 SCSI(Small Computer System Interface) 명령어 계층을 기반으로 하여, 호스트(Host)와 타겟(Target) 간에 불필요한 명령어 변환(Translation)과 복잡한 에뮬레이션 과정을 거쳐야 했던 반면, NVMe-oF는 NVMe 명령어 셋 자체를 네트워크 패킷 안에 캡슐화(Encapsulation)하여 전송합니다.

이 기술의 등장 배경에는 **'CPU 속도와 스토리지 I/O 속도의 격차(Gap)'**라는 근본적인 문제가 자리하고 있습니다. Flash Memory 기반의 SSD(Solid State Drive)가 급격히 보급됨에 따라, 병목 구간은 디스크(Device)에서 네트워크(Network)와 프로토콜(Protocol) 처리 소프트웨어로 이동했습니다. 데이터센터는 수천 개의 코어를 가진 최신 서버(CPU)와 마이크로초(µs) 단위로 반응하는 NVMe SSD 간의 데이터 교환에서, 기존 iSCSI(Internet Small Computer System Interface)나 FC(Fibre Channel) 같은 SCSI 기반 프로토콜이 발생시키는 수만 사이클의 컨텍스트 스위칭(Context Switching)과 인터럽트(Interrupt)를 감당할 수 없게 된 것입니다. 따라서 **'로컬 메모리 접근과 유사한 수준의 원격 접근'**을 실현하기 위해 개발된 것이 NVMe-oF입니다.

> **📢 섹션 요약 비유:**
> 서울(서버 CPU)에서 부산(스토리지)까지 화물을 보낼 때, 중간에 여러 번 하역하고 포장을 바꾸는 물류 센터(SCSI 레이어 변환)를 거치느라 며칠이 걸리던 것을, 화물을 그대로 싣고 고속도로 위에서 역주행(직행)하듯이 내보내는 **KTX 직통 열차(NVMe-oF)**로 바꾸어, 1시간 만에 배송을 완료하는 것과 같습니다.

#### ASCII 다이어그램: 진화하는 스토리지 패러다임

```ascii
+--------------------------+       +---------------------------+       +--------------------------+
|       [Legacy Era]        |       |      [Transition Era]     |       |      [NVMe-oF Era]       |
+--------------------------+       +---------------------------+       +--------------------------+
|                          |       |                           |       |                          |
|  [App]      [App]         |       |  [App]      [App]         |       |  [App]      [App]        |
|    |          |           |       |    |          |           |       |    |          |           |
|  [OS]       [OS]          |       |  [OS]       [OS]          |       |  [OS]       [OS]         |
|    |          |           |       |    |          |           |       |    |          |           |
| [SCSI Driver]             |       | [AHCI/SATA]  [NVMe Driver]|       | [NVMe Driver]            |
|    | (High Latency)       |       |    |          | (Low Lat) |       |    | (Ultra Low Lat)       |
| [HBA] ------ Network ---- |       | [SATA/PCIe]  [PCIe]      |       | [NVMe-oF] --- Fabric ---- |
| (FC/iSCSI)  (Bottleneck) |       |                          |       | (RDMA/TCP)  (Efficient) |
|                          |       |                           |       |                          |
+--------------------------+       +---------------------------+       +--------------------------+

💡 해설:
기존 Legacy 환경에서는 Host와 Storage 사이에 복잡한 SCSI 계층이 존재하여 병목이 발생했습니다.
NVMe-oF 시대에는 이 계층을 평탄화(Flattening)하여, 마치 로컬 버스에 연결된 것처럼 네트워크를 통해 직접 제어합니다.
```

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

NVMe-oF의 핵심 설계 철학은 **'Host Software Transparency(호스트 소프트웨어 투명성)'**입니다. 호스트 입장에서는 자신의 로컬 NVMe 컨트롤러에 접속하는 것과 동일한 드라이버 인터페이스를 유지하면서, 물리적인 전송 매체만 네트워크 패브릭으로 교체하는 구조를 가집니다. 이를 위해 NVMe-oF는 **FABRICS 명령어 세트**를 정의하여, 컨트롤러 연결(Connect), 연결 해제(Disconnect), 인증(Authenticate) 등 네트워크 특유의 작업을 표준 NVMe 명령어와 별도로 처리합니다.

#### 1. 핵심 구성 요소 (Component Table)

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|:---|
| **Host** | N/A | 스토리지를 사용하는 클라이언트 서버 | NVMe Driver를 통해 I/O 요청 생성 및 SQ/CQ 관리 | NVMe Queue I/O | 송장을 작성하는 발송인 |
| **Controller** | NVMe Controller | I/O 요청을 처리하는 엔진 | Submission Queue(SQ)의 명령을 해석하여 Execution | NVMe Admin & I/O Cmd | 택배 물류 센터의 분류기 |
| **Subsystem** | NVM Subsystem | 하나 이상의 컨트롤러와 네임스페이스의 집합 | 논리적인 스토리지 도메인을 형성 | NVMe Spec | 전체 택배 영업소 |
| **Transport** | Fabric Transport | 네트워크상의 데이터 전달 층 | NVMe Q Pair를 패킷에 캡슐화하여 전송/수신 | RDMA, FC, TCP | 도로 및 차량 |
| **Queue Pair** | Submission & Completion Queue | 명령과 완료 상태를 저장하는 큐 | 호스트는 SQ에 쓰고, 컨트롤러는 CQ에 씀 (Doorbell registers) | PCIe Memory Mapped I/O | 주문서와 영수증 상자 |
| **CAP** | Controller Attributes | 컨트롤러의 성능 특성 레지스터 | 최대 큐 개수, 입출력 큐 사이즈 등 정의 | HW Register | 공장의 하루 생산량 명시 |

#### 2. NVMe-oF 동작 시퀀스 및 아키텍처

NVMe-oF의 데이터 전송은 크게 **Capsule Management(캡슐 관리)** 단계와 **Data Transfer(데이터 전송)** 단계로 나뉩니다. 호스트는 네트워크를 통해 원격 컨트롤러의 메모리에 직접 접근하거나, 데이터를 In-Band 방식으로 전송합니다. 특히 RDMA(Remote Direct Memory Access) 환경에서는 호스트 CPU가 데이터를 복사(Copy)하지 않고, 타겟의 메모리 영역에 직접 쓰기(Direct Write)를 수행하여 오버헤드를 제거합니다.

```ascii
<< Host System >>                                          << Target Storage >>
+-----------------------+                                  +-----------------------+
|  Application Layer    |                                  |  NVMe Device          |
+-----------------------+                                  +-----------------------+
|  NVMe Driver          |                                  |  NVMe Controller      |
|  (Creates I/O Command)|                                  |  (Processes I/O)      |
+----------+------------+                                  +-----------+-----------+
|  NVMe Transport       |                                  |  NVMe Transport       |
|  [Encapsulation]      |                                  |  [Decapsulation]      |
|  - SQ(Submit Queue)   |                                  |  - CQ(Comp Queue)     |
+----------+------------+                                  +-----------+-----------+
           |                                                     ^
           | 1. Capsule Cmd (NVMe Cmd in Transport Pkt)         | 4. Capsule Comp
           v                                                     |
+-----------------------+      Network Fabric      +-----------------------+
|  NIC / HBA            | <=======================> |  Port / NIC           |
|  (RNIC / CNA)         |   (RoCEv2 / FC / TCP)   |  (Target Port)        |
+-----------------------+                          +-----------------------+
           |                                                     ^
           | 2. RDMA Write / Read (Data Direct Placement)        | 3. Data Ack
           |    (Zero-copy, Bypassing CPU)                       |
           +-----------------------------------------------------+

💡 해설:
1. 호스트의 NVMe 드라이버가 SQ에 I/O 명령어를 쓰면, Transport 계층이 이를 캡슐화하여 네트워크로 전송(1).
2. RDMA 환경에서는 데이터가 호스트 CPU를 거치지 않고 RNIC을 통해 타겟 메모리로 직접 쓰임(2). 이를 'Zero-Copy'라 함.
3. 타겟은 데이터 전송 완료 후 RDMA 작업 완료 신호를 보냄(3).
4. 마지막으로 타겟은 CQ(Completion Queue)에 완료 엔트리를 쓰고 호스트에게 인터럽트를 알림(4).
```

#### 3. 핵심 알고리즘 및 코드 구조

NVMe-oF의 핵심은 **IO Queue Pair(QP)**의 매핑과 **Submission Queue Entry(SQE)**의 구조입니다.

```c
/* [가상코드] NVMe-oF Submission Queue Entry 구조 및 전송 */
// NVM Express Specification, Figure 88 (Command Dword 0/1)

struct nvme_command {
    /* DW0 : Command Dword 0 */
    uint32_t CDW0 : 16;  // Opcode(CREATE IO SQ, READ, WRITE 등)
    uint32_t FUSE : 2;   // Fused Operation support
    uint32_t RSVD : 4;
    uint32_t PSDT : 2;   // PRP or SGL for Data Transfer
    uint32_t CID  : 16;  // Command Identifier (Unique per I/O)

    /* DW1~DW5 : Metadata / PRP / Data Pointers */
    uint64_t PRP1;       // Phys Region Page 1 (시점 주소)
    uint64_t PRP2;       // Phys Region Page 2 (연속 주소 or SGL)
    
    /* DW10~DW11 : Logical Block Address & Length */
    uint64_t SLBA;       // Starting LBA (읽기/쓰기 시작 위치)
    uint32_t NLB : 16;   // Number of Logical Blocks (0's based value)
    /* ... 상세 필드 생략 ... */
};

// [동작 원리]
// 1. Host Driver는 위 구조체를 메모리에 채움.
// 2. RDMA Send 작업을 통해 Remote Target의 Submission Queue 메모리 영역으로 전송.
// 3. Target Controller가 이를 파싱하여 NAND 플래시에 명령을 전달.
```

> **📢 섹션 요약 비유:**
> 마치 고속 도로 톨게이트에서 하이패스 차로를 별도로 운영하여, 요금 정산(프로토콜 처리)을 위해 차량(CPU)이 멈추지 않고 시속 100km로 통과할 수 있게 하는 것과 같습니다. NVMe-oF는 복잡한 네트워크 '톨게이트'를 넘어 스토리지 데이터를 위한 전용 고속 철도(RDMA)를 깔아 놓은 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

NVMe-oF의 가치는 기존 스토리지 프로토콜과의 정량적 비교를 통해 명확해집니다. 특히 OS/컴퓨터 구조 측면에서의 **CPU 사이클 절약**과 네트워크 측면의 **대역폭 활용 효율성**이 핵심입니다.

#### 1. 심층 기술 비교 (NVMe-oF vs Legacy)

| 비교 항목 | Legacy SCSI (iSCSI/FCP) | NVMe-oF (RDMA/TCP) | 분석 (Analysis) |
|:---|:---|:---|:---|
| **명령어 세트** | SCSI (Serial Attached SCSI) | NVMe (Non-Volatile Memory Express) | SCSI는 회전식 디스크(HDD) 중심 설계. NVMe는 병렬성 극대화 설계. |
| **큐 구조** | Single Queue (Per Target) | Multi-Queue (65,535 Queues) | 멀티코어 CPU에서 Lock Contention을 거의 제거하여 성능 선형적 확보 가능. |
| **지연 시간 (Latency)** | ~50µs ~ 100µs (이론상) | **< 10µs** (RDMA 기반) | 네트워크 왕복 지연(RTT)과 프로토콜 변환 비용이 획기적 절감됨. |
| **CPU 오버헤드** | High (Interrupt + Copy) | Low (Kernel Bypass/Offload) | 데이터 처리를 위해 CPU가 수행해야 하는 Context Switch가 획기적 감소. |
| **최대 전송 크기** | 제한적 (Block Limit) | 매우 큼 (Up to 64KB PRP entry) | 대용량 데이터 전송 시 효율이 높음. |
| **전송 매체** | TCP/IP 또는 FC | RDMA, FC, TCP | 기존 이더넷(LOSSLESS) 및 FC 인프라 호환 가능. |

#### 2. 융합 관점 시너지 및 오버헤드 분석

1.  **융합 1: OS 및 컴퓨터 구조 (System Architecture)**
    *   **Synergy**: 멀티코어 환경에서 NVMe-oF는 각 코어가 독립적인 I/O 큐(CPU Pinning)를 가질 수 있게 하여, 메모리 버스와 캐시 라인(Cache Line) 경합을 줄입니다. NUMA(Non-Uniform Memory Access) 아키텍처와 결합하여 로컬 소켓에 연결된 RNIC(RDMA NIC)를 통해 원격 메모리에 접근하면, 이를 **'리모트 메모리(Remote Memory)'**처럼 사용할 수 있는 가능성이 열립니다.
    *   **Overhead**: RDMA 설정(Memory Registration, Page Table Locking)을 위한 초기 설정 비용이 발생하나, 장시간 유지되는 연결에서는 무시할