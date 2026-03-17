+++
title = "339. DAS (Direct Attached Storage)"
date = "2026-03-14"
weight = 339
+++

# [DAS] Direct Attached Storage (직결 저장소)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스토리지 장치를 네트워크(Network) 프로토콜 없이 호스트(Host)의 I/O 인터페이스에 전용 케이블로 1:1로 직접 연결하여, 운영체제(OS)가 로컬 디스크(Local Disk)처럼 관리하는 가장 원초적이고 고성능을 보장하는 스토리지 아키텍처이다.
> 2. **가치**: 프로토콜 오버헤드(Protocol Overhead)가 배제된(Block-Level) 원시 I/O 성능(Raw Performance)을 제공하여, 단일 서버가 처리해야 하는 초대용량 데이터베이스나 멀티미디어 처리 환경에서 **초저지연(Ultra-low Latency)**을 실현한다.
> 3. **융합**: SAS/SATA/PCIe(NVMe) 등의 인터페이스 발전과 더불어 최근에는 HCI(Hyper-Converged Infrastructure)의 로컬 스토리지 자원으로 활용되며, 소프트웨어 정의 스토리지(SDS, Software Defined Storage)와 결합하여 분산 시스템의 기반 물리 계층을 구성한다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 기술적 정의 및 철학
**DAS (Direct Attached Storage)**는 데이터를 저장하는 외부 스토리지 장치를 서버의 인터페이스 포트(HBA)에 네트워크 스위치나 라우터를 거치지 않고 직접 케이블링(Direct Cabling)하여 연결하는 방식이다. 호스트 입장에서는 내장 하드디스크와 차이가 없는 **블록 레벨(Block-Level)** 장치로 인식되며, 파일 시스템(File System)의 생성, 관리, 권한 부여 등 모든 권한이 연결된 호스트 서버에게 독점적으로 귀속된다.

#### 2. 기술적 배경 및 진화
데이터 스토리지의 초창기에는 PC나 서버의 내부 버스(Internal Bus)인 **IDE (Integrated Drive Electronics)**나 **SCSI (Small Computer System Interface)**에 디스크를 직접 장착하는 것이 유일한 방법이었다. 이후 데이터 양이 폭발하면서 서버 섀시(Chassis) 내부의 물리적 공간 한계를 극복하기 위해 외장형 인클로저(Enclosure)를 꽂아 쓰는 형태로 발전하였다. **NAS (Network Attached Storage)**나 **SAN (Storage Area Network)**과 같은 네트워크 기반 스토리지가 등장했음에도 불구하고, DAS는 네트워크 패킷 처리에 따른 지연(Latency)이 허용되지 않는 **고성능 컴퓨팅(HPC, High-Performance Computing)** 영역에서 여전히 그 유효성을 유지하고 있다.

```text
[ Storage Evolution Context ]

+-----------+      +-----------+      +----------------------+
|   Internal|      | External  |      |   Network (SAN/NAS)  |
|   (DAS)   | --> |   (DAS)   | --> |   (Shared Storage)   |
+-----------+      +-----------+      +----------------------+
   (1대1)             (1대1)              (N대 : N 공유)
   Local Bus         Cable(SAS/USB)      Fabric(Switch)
```

📢 **섹션 요약 비유**: 거대한 도서관(네트워크 스토리지)을 이용하려면 카드를 찍고 분실물 센터를 거쳐야 하지만, 내 집 서재(DAS)는 굳이 신발을 신지 않아도 가장 가까운 거리에서 책을 꺼내 읽을 수 있는 가장 원초적이고 빠른 저장 방식입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 (Component Architecture)
DAS는 크게 호스트의 **HBA (Host Bus Adapter)**, 전송을 위한 **케이블링**, 그리고 **디스크 배열(Disk Array)**로 구성된다. 운영체제(OS)는 파일 시스템 계층에서 직접 볼륨을 관리하며, 스토리지 장치 자체는 단순한 블록 저장소 역할만 수행한다.

| 구성 요소 (Component) | 기술적 역할 (Role) | 주요 프로토콜/규격 (Protocol) | 세부 동작 메커니즘 (Deep Dive) |
|:---:|:---|:---|:---|
| **HBA (Host Bus Adapter)** | 호스트와 스토리지 간의 물리적/논리적 연결을 담당하는 bridge 역할 | PCIe, SATA, SCSI, Fibre Channel(FC) | 호스트의 메모리와 스토리지 간의 **DMA (Direct Memory Access)** 제어 및 명령어 큐(Command Queue) 관리 수행 |
| **Interface Cable** | 고속 직렬 데이터 전송을 위한 물리적 매체 | SAS, SATA, Thunderbolt, USB 3.x/4, NVMe-over-Fabrics(가상) | 전송 거리가 짧아 신호 감쇠가 적고, 프로토콜 오버헤드(Header/Packet)가 최소화된 'Raw' 신호 전달 |
| **DAS Enclosure** | 다수의 디스크를 수납하고 전원/냉각을 제공하는 케이싱 | JBOD (Just a Bunch Of Disks), RAID Controller | 디스크의 핫스왑(Hot-swap)을 지원하며, 내부적으로 **Hardware RAID (Redundant Array of Independent Disks)** 기능을 통해 성능 및 안정성 제공 |
| **Host OS File System** | 블록 디바이스를 논리적 파일 단위로 관리 | NTFS, EXT4, ZFS, APFS | 스토리지를 직접 소유하므로, 권한 관리(Access Control)와 캐싱(Caching)을 OS가 독점적으로 수행 |

#### 2. 상세 아키텍처 및 데이터 흐름 (Data Flow)
DAS 환경에서의 I/O 경로는 네트워크 계층(Layer 3~4)을 완전히 생략하고 물리적 계층(Layer 1)과 데이터 링크 계층(Layer 2)만을 거친다.

```text
+------------------+             +-----------------------------------+
|   Host Server    |             |           DAS Subsystem           |
|                  |  Direct I/O |                                   |
|  +------------+  |             |  +-----------------------------+  |
|  | Application|  |             |  |    RAID Controller / HBA    |  |
|  +------|------+  |             |  +-------------|---------------+  |
|         |         |             |                | (SATA/SAS/FC)    |
|  +------v------+  |             |  +-------------v---------------+  |
|  | File System |  |             |  |    Physical Disk Drives     |  |
|  | (NTFS/EXT)  |  |             |  |  [HDD] [HDD] [SSD] [SSD]    |  |
|  +------|------+  |             |  +-----------------------------+  |
|         |         |             |                                   |
|  +------v------+  |             |  (No separate OS/Processor for     |
|  |  Volume Mgr |  |             |   File System logic exists here)  |
|  |   / LVM     |  |             +-----------------------------------+
|  +------|------+  |
|         |         |
|  +------v------+  |
|  |  Block I/O  |  |
|  |  Filter     |  |
|  +------|------+  |
+---------|--------+
          |
+---------v--------+
| HBA (SAS/FC/USB)|
+---------|--------+
          |
<------------------------------------------------->
        Point-to-Point Cable (No Switching)
```

**[데이터 흐름 해설]**
1.  **I/O Request**: 애플리케이션이 파일 시스템에 `Write` 요청을 생성.
2.  **Block Translation**: 파일 시스템이 이를 논리 블록 주소(LBA, Logical Block Address)로 변환.
3.  **HBA Transfer**: **HBA (Host Bus Adapter)**가 CPU의 개입 없이 DMA를 사용하여 메모리 데이터를 읽어 전용 케이블로 전송.
4.  **Direct Write**: 외장형 DAS 컨트롤러가 데이터를 받아 물리적 디스크 플래터(Platter)나 셀(Cell)에 기록.
5.  **ACK**: 확인 신호가 없는 네트워크 통신이 아닌, 하드웨어 인터럽트(Interrupt) 방식으로 완료 신호를 호스트에게 전달.

#### 3. 핵심 알고리즘 및 인터페이스 기술
-   **SAS (Serial Attached SCSI)**: DAS의 가장 대표적인 엔터프라이즈 인터페이스로, 기존 병렬 방식의 SCSI를 직렬화하여 대역폭을 획기적으로 높였으며, 포트 멀티플렉싱을 통해 하나의 포트로 여러 디스크를 연결(Expander)할 수 있다.
-   **NCQ (Native Command Queuing)**: 호스트가 한 번에 여러 명령어를 전달하고, 디스크가 이를 재정렬하여 헤드 이동을 최소화하는 알고리즘. SATA 및 SAS에서 DAS의 성능을 극대화하는 핵심 기술이다.

```c
/* Pseudo-code: DAS I/O Logic vs Network I/O */
// [DAS / SAN Block Mode]
// Direct Hardware Command, No Network Stack Overhead
void das_write_block(int lba, void* data) {
    HBA->COMMAND_REG = WRITE_CMD;
    HBA->LBA_REG     = lba;
    HBA->DATA_PTR    = data; // DMA Address
    HBA->START       = 1;
    while(HBA->STATUS != DONE); // Polling or Interrupt
}
```

📢 **섹션 요약 비유**: 회사 내에서 결재를 위로 올렸다가 내려오는 지루한 행정 절차(네트워크 프로토콜) 없이, 사장님(Host OS)이 옆자리 비서(DAS)에게 말을 걸면 즉시 서류를 전달받는 방식처럼 중간 단계가 없는 '원샷(One-shot)' 업무 처리가 가능합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 스토리지 아키텍처 심층 비교 (DAS vs NAS vs SAN)

| 비교 항목 (Criteria) | DAS (Direct Attached Storage) | NAS (Network Attached Storage) | SAN (Storage Area Network) |
|:---:|:---|:---|:---|
| **접속 방식 (Access)** | 직접 연결 (1:1) | 이더넷(LAN)을 통한 공유 (N:N) | 전용 Fiber Channel/iSCSI 망 (N:N) |
| **데이터 단위 (Unit)** | **Block Level (Raw)** | File Level (NFS, SMB/CIFS) | **Block Level (Raw)** |
| **주인 소유권 (Owner)** | 호스트 OS 독점 | 스토리지 OS(Embedded)가 관리 | 공유 플랫폼, LUN 매핑으로 할당 |
| **성능 (Performance)** | **최고 (Native Speed)** | 네트워크 대역폭 제한 | 고성능이나 네트워크 지연 존재 |
| **확장성 (Scalability)** | 낮음 (포트/케이블 물리적 한계) | 중간 (LAN 스위치 포트 증설) | 매우 높음 (스위칭 구조) |
| **비용 (Cost)** | 낮음 (단순 케이블 연결) | 낮음~중간 | 매우 높음 (스위치, HBA, 라이선스) |

#### 2. 타 영역(시스템 아키텍처)과의 융합 분석
-   **OS 및 DB (Operating System & Database)**:
    데이터베이스 관리 시스템(DBMS)은 주기적으로 **Checkpoint**나 **Recovery**를 수행하며, 이때 발생하는 대규모 순차 I/O(Sequential I/O)는 네트워크 대역폭 병목을 유발하기 쉽다. DAS는 이러한 **Latency-sensitive**한 워크로드에 최적화되어 있어, **Oracle RAC**와 같은 클러스터링 환경이 아닌 단일 독립형 DB 서버에는 여전히 DAS가 선호되기도 한다. 단, OS가 죽으면 데이터에 접근할 수 없는 **SPOF (Single Point of Failure)** 리스크가 공존한다.

-   **가상화 (Virtualization)**:
    전통적인 **VMware ESXi**나 **Hyper-V** 환경에서 여대 호스트가 공유된 스토리지를 통해 라이브 마이그레이션(vMotion)을 수행하려면 SAN/NAS가 필수적이다. 그러나 **HCI (Hyper-Converged Infrastructure)**는 각 노드에 붙은 DAS를 가상화 소프트웨어 계층(vSAN 등)으로 논리적으로 묶어 분산 스토리지 풀을 생성함으로써, DAS의 **저렴한 비용**과 **고성능**을 유지하면서 SAN의 **공유성**을 확보하는 융합 형태로 진화했다.

```text
       [ Convergence Flow: DAS to Distributed Storage ]

      Node 1                 Node 2                 Node 3
   +-------+              +-------+              +-------+
   | DAS   |              | DAS   |              | DAS   |
   | (1TB) |              | (1TB) |              | (1TB) |
   +---+---+              +---+---+              +---+---+
       |                      |                      |
       | (Software Layer)     |                      |
       +----------------------+----------------------+
                   |
             [ Distributed Storage Pool (3TB) ]
                   (vSAN / Ceph / GlusterFS)
```

📢 **섹션 요약 비유**: 각자 전용 화장실(DAS)을 가지고 있으면 사용할 때는 편하지만, 다른 방 친구가 내 화장실을 쓰지 못하는 단점이 있습니다. 이를 해결하기 위해 각 방의 화장실 문을 헐어버리고 복도로 연결(HCI/Sw-defined)하여, 실제로는 각 방의 화장실(DAS)을 쓰면서 겉으로는 하나의 거대한 공용 화장실(SAN)처럼 쓰게 만든 기술입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 도입 시나리오 및 의사결정 트리
기술사는 다음의 상황에서 DAS 도입을 고려하여야 한다.
-   **고립된 고성능 워크로드 (Isolated HPC)**: 렌더링 팜(Rendering Farm)의 각 노드, 초고속(HFT) 트레이딩 서버. 타 서버와 데이터를 공유할 필요가 없고, 오로지 디스크의 IOPS와 대역폭만 필요한 경우.
-   **비용 제약이 심한 소규모 구축**: 중소기업의 백업 서버, CCTV 녹화용 서버. 수만 달러의 SAN 스위치를 도입할 예산이 없으며, 단일 서버 장애 시 가용성 중단이 허용되는 환경.

```text
[ Decision Matrix ]
             +-----------------+
   Start     | Need Storage?   |
             +--------+--------+
                      | Yes
                      v
             +--------+--------+
             | Data Sharing    |---- Yes ---> Use NAS/SAN
             | required?       |
             +--------+--------+
                      | No (Dedicated)
                      v