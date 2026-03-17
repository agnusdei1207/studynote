+++
title = "338. NAS (Network Attached Storage)"
date = "2026-03-14"
weight = 338
+++

# # 338. NAS (Network Attached Storage)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **NAS (Network Attached Storage)**는 독립적인 **Network (TCP/IP)** 상에 존재하며, 자체적인 **OS (Operating System)**와 **File System**을 탑재하여 클라이언트에게 **File-Level** 데이터 접근을 제공하는 고도로 특화된 Storage Appliance이다.
> 2. **가치**: DAS (Direct Attached Storage)의 단절된 Silo 문제를 해결하고, SAN (Storage Area Network)의 고비용 구조를 대체하여, 다양한 **Heterogeneous OS (Windows, Linux, macOS)** 환경 간의 데이터 공유와 협업 효율성을 극대화한다.
> 3. **융합**: 10GbE/40GbE 등 **High-Speed Ethernet** 기반의 네트워크 기술 발전과 **NVMe (Non-Volatile Memory express)** Cache 기술, 그리고 **Object Storage (S3-compatible)**와의 융합을 통해 단순 파일 서버를 넘어 Hybrid Cloud Edge의 핵심 인프라로 진화 중이다.

---

### Ⅰ. 개요 (Context & Background)

NAS는 "Storage가 Network에 직접 부착되는 형태"를 의미합니다. 전통적인 Host 부착형 저장장치인 DAS가 서버의 종속적인 부품인 반면, NAS는 스마트한 Storage 장치입니다. 즉, 네트워크 스위치(Switch)를 통해 **LAN (Local Area Network)** 환경에 연결되며, **IP (Internet Protocol)** 주소를 할당받아 독립적인 하나의 노드(Node)로 동작합니다.

내부적으로는 x86 또는 ARM 기반의 **CPU (Central Processing Unit)**와 **RAM (Random Access Memory)**를 탑재하여 경량화된 **OS (Operating System)**(예: Linux Kernel 기반의 Custom OS)을 구동합니다. 이에 따라 호스트(클라이언트)는 단순히 데이터를 쓰는 행위만 할 뿐, 파일 관리의 복잡한 연산(메타데이터 처리, 파일 Locking 등)을 NAS가 전담하게 됩니다. 이러한 구조는 File Sharing이라는 특정 업무 집중적 환경에서 Host의 부하를 줄이고 Storage 관리 효율을 높이는 결과를 가져왔습니다.

#### 💡 개념 비유
특정 요리사(서버)만이 쓸 수 있는 사설 창고(DAS)가 아니라, 누구나 와서 물건을 넣고 뺄 수 있는 공용 보관 창고에 키카드 시스템을 설치한 **"스마트 공용 보관함"**과 같습니다.

#### 📊 기술 진화 배경
| 단계 | 기술 | 한계 | 혁신 | 요구사항 |
|:---:|:---:|:---|:---|:---|
| 1세대 | DAS (SCSI Direct) | 서버 장애 시 데이터 공유 불가, 공간 효율 저하 | 독립된 케이블링 필요 없음 | 개별 서버 저장 |
| 2세대 | **NAS (IP Network)** | **Network Traffic**으로 인한 병목 발생 가능 | **파일 공유** 및 **이기종 연결** 지원 | 협업 및 중앙화 |
| 3세대 | SAN (Fiber Channel) | 고비용, 관리 복잡성 (LVM 관리 등) | 블록 레벨 고속 전송 | DB/금융 거래 |
| 4세대 | Unified NAS | NAS와 SAN의 통합 | 프로토콜 혼용 지원 (File + Block) | 데이터 통합 관리 |

#### ASCII: 스토리지 연결 방식의 비교
```text
      [ DAS 구조 ]                    [ NAS 구조 ]                     [ SAN 구조 ]
+------------------+             +------------------+             +------------------+
|   Host Server    |             |   LAN Switch     |             |   FC Switch      |
| [App] + [FileSys]|             |  (IP Network)    |             | (Block Network)  |
+--------|---------+             +--------|---------+             +--------|---------+
         |   ^                            |   ^                            |   ^
         v   |                            v   |                            v   |
      [Direct Cable]                  [TCP/IP]                        [Fiber Channel]
         |   ^                            |   ^                            |   |
+--------|-|---------+             +--------|---------+             +--------|---------+
|    Storage Box   |             |   NAS Device    |             |    SAN Array    |
| (No Intelligence)|             | [File System]   |             |  (Block Only)   |
+------------------+             | [OS + CPU]      |             +------------------+
                                 +------------------+
```
*(해설: DAS는 서버가 직접 디스크를 제어하지만, NAS와 SAN은 네트워크를 경유함. NAS는 파일 시스템을 가짐으로써 스마트한 장치로 동작함)*

📢 **섹션 요약 비유**: NAS의 등장은 마치 집집마다 우물을 파서 사용하던(DAS) 시대에서, 수도관(LAN)을 통해 깨끗한 물을 공급하는 상수도 시스템으로 전환하여 누구나 수도꼭지를 틀면 물을 쓸 수 있게 한 인프라 혁명과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

NAS의 핵심은 **"Processing Offloading"**입니다. 일반 서버가 파일을 처리하려면 파일 시스템 생성, 권한 검사, 블록 매핑 등의 작업을 수행해야 하지만, NAS를 사용하면 클라이언트는 단순히 **"파일 전송 요청"**만 네트워크에 보내면, NAS 내부의 CPU와 OS가 나머지 복잡한 작업을 처리합니다.

#### 1. 핵심 구성 요소 상세 분석
| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Network Interface** | 데이터 송수수 입구 | **TCP/IP Stack** Offloading을 통해 패킷 처리 속도 향상 | **10GbE**, **LACP** | 빠른 출입구 |
| **CPU (Processor)** | 명령어 처리 | RAID 연산, **File System** 메타데이터 관리, 암호화(Encryption) 연산 | Intel/AMD SoC, ASIC | 창고 관리자 두뇌 |
| **Memory (DRAM)** | 캐시 및 버퍼링 | 자주 접근하는 **Metadata**와 파일 데이터를 적재하여 Disk I/O 감소 | DDR4/DDR5 | 작업대 |
| **File System Layer** | 논리적 데이터 관리 | 파일 생성, 삭제, 권한 제어, **Journaling** 로그 관리 | **ZFS**, **Btrfs**, EXT4 | 정리 시스템 |
| **Physical Storage** | 데이터 영구 저장 | **HDD**나 **SSD**를 **RAID** Redundancy Array로 묶어 데이터 보호 | RAID 6, RAID 10 | 실제 물품 보관 선반 |

#### 2. 데이터 I/O 흐름 (Deep Dive Mechanism)
클라이언트가 NAS의 데이터를 요청할 때, 데이터는 비트(Bit) 단위가 아닌 **파일(File)** 단위로 이동합니다.
1.  **요청 (Request)**: 클라이언트 OS는 VFS (Virtual File System) 계층을 통해 **SMB (Server Message Block)** 또는 **NFS (Network File System)** 명령을 생성하여 LAN으로 전송.
2.  **수신 및 해석 (Receiving)**: NAS의 **NIC (Network Interface Card)**가 패킷을 수신하고 내부 **CPU**가 요청을 해석.
3.  **메타데이터 조회 (Metadata Lookup)**: 내부 **File System**이 해당 파일의 위치(블록 주소), 권한, Lock 상태 확인.
4.  **디스크 액세스 (Disk Access)**: **RAID Controller**를 통해 실제 디스크(HDD/SSD)에서 데이터를 읽어 **RAM**으로 적재.
5.  **전송 (Response)**: 네트워크 계층을 통해 다시 클라이언트에게 파일 전송.

#### ASCII: NAS 내부 프로세싱 플로우
```text
  [Client PC]                     [ NAS Appliance ]                     [ Disks ]
+-------------+                  +------------------+                  +--------+
| User App    |                  |   Network Stack  |                  |  HDD   |
+------|------+  (1) SMB Read    +--------|---------+  (4) Read Blocks +---|----+
       |      ------------------> |  CPU  |   RAM   | -----------------> | SSD   |
       |                          +---|---|----|----+                  +--------+
       |                              |    |    |
       |           (3) Return File    |    |    | (2) Metadata Lookup
       | <-------------------------- |    |    v
       |                              |  File System (ZFS/Btrfs)
       v                              v
  [User View]                     [Storage Processing]
```
*(해설: 클라이언트는 단순히 요청만 보내지만, NAS 내부에서는 파일 시스템 관리, 캐싱, RAID 디스크 접근이라는 무거운 작업이 모두 수행됨)*

#### 3. 핵심 알고리즘: 파일 시스템의 차별성 (ZFS 예시)
NAS 성능의 핵심은 파일 시스템에 있습니다. 기존의 EXT4는 디스크 장애 복구 능력이 제한적이나, 채용되는 전용 파일 시스템들은 **Self-Healing** 기능을 가집니다.
*   **Copy-on-Write (CoW)**: 데이터를 덮어쓰지 않고 새 위치에 기록하므로 데이터 손상이 최소화됨.
*   **Snapshot**: 특정 시점의 데이터 상태를 즉시 복사하여 Ransomware 공격 대응.

```c
/* ZFS Copy-on-Write Conceptual Logic */
// 1. 기존 블록 수정 요청
// Old Block [0x1234] = Data_A
// Old Block [0x5678] = Pointer_to_0x1234

// 2. ZFS 파일 시스템 동작
New_Block [0xABCD] = Data_Modified; // 새 블록에 기록
New_Pointer [0x9999] = 0xABCD;      // 포인터 변경 (Atomic)
Old_Pointer [0x5678] = 0x1234;      // 이전 포인터는 스냅샷 보존 시 계속 존존 (Garbage Collection될 때까지)
```
*(해설: 수정 시 원본을 보존하여 데이터 안정성을 확보하는 구조)*

📢 **섹션 요약 비유**: NAS는 식당에서 주문을 받는 시스템입니다. 손님(클라이언트)은 그저 "김치찌개(SMB) 주세요"라고 메뉴 이름만 외치면, 웨이터(CPU)가 주방(Storage)에 가서 재료를 찾고(Check Metadata), 요리하고(Cooking), 가져다주는(Plating) 모든 복잡한 과정을 대신 처리해 주는 서비스형 창고입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

NAS는 SAN과 빈번하게 비교됩니다. 이 두 기술은 상호 배타적이기보다는 상호 보완적이며, 각기 다른 데이터 접근 패턴에 최적화되어 있습니다.

#### 1. 심층 기술 비교: NAS vs SAN
| 비교 항목 | **NAS (File-Level)** | **SAN (Block-Level)** | **비고** |
|:---|:---|:---|:---|
| **데이터 단위** | File (전체 파일) | **Block** (4KB Chunk) | Block이 더 Low-Level |
| **Network Protocol** | **TCP/IP** (Ethernet) | **Fibre Channel (FC)** or **iSCSI** (IP) | Layer 3 vs Layer 2~4 |
| **File System 위치** | **NAS 내부 장착** | **Host(서버) 내부 장착** | 관리 주체의 차이 |
| **주요 용도** | 파일 공유, 유저 데이터, 홈 디렉토리 | **DB**, Email, Transaction 시스템 | Random I/O vs Sequential I/O |
| **성능 병목** | Network Bandwidth, Protocol Overhead | **HBA** Throughput, Disk Queue | SAN이 일반적으로 Latency 낮음 |
| **투자 비용** | 상대적으로 저렴 (이더넷 활용) | 고가 (FC Switch, HBA) | |

#### 2. 과목 융합 관점: OS/네트워크와의 시너지
*   **OS (운영체제)**: NAS의 성능은 **VFS (Virtual File System)**의 캐싱 정책과 **TCP Window Size**에 의존합니다. OS의 **Page Cache** 튜닝이 없으면 NAS의 빠른 디스크도 느려질 수 있습니다.
*   **Network (네트워크)**: 표준 **LAN (Local Area Network)**을 사용하기 때문에, 네트워크의 혼잡 제어(**Congestion Control**)나 **Jumbo Frame (MTU 9000)** 설정 등 네트워크 엔지니어링 기술이 곧 스토리지 성능으로 직결됩니다.
*   **Security (보안)**: **AD (Active Directory)** 연동을 통해 **ACL (Access Control List)**을 통합 관리함으로써 ID 기반의 보안 정책을 스토리지 레벨까지 확장 적용합니다.

#### ASCII: 프로토콜 스택 비교
```text
   [ NAS Protocol Stack ]          [ SAN Protocol Stack (iSCSI) ]
+-----------------------+          +-----------------------+
| Application (File I/O)|          | Application (DB/App)  |
+-----------------------+          +-----------------------+
|   SMB  /  NFS         |          |   SCSI CDB (Command)  |  <-- Interface
+-----------------------+          +-----------------------+
|   TCP (Transport)     |          |   TCP (Transport)     |
+-----------------------+          +-----------------------+
|   IP (Network)        |          |   IP (Network)        |
+-----------------------+          +-----------------------+
|   Ethernet (MAC)      |          |   Ethernet (MAC)      |
+-----------------------+          +-----------------------+
                                    (iSCSI는 SCSI 명령을 IP 패킷에 담아 SAN 처럼 씀)
```

📢 **섹션 요약 비유**: NAS는 사람들이 돌아다니며 문서를 나눠 가지는 **"협업 오피스(협업형)"**이고, SAN은 우체국 직원만 들어가서 빠르게 우편물을 분류하는 **"물류 센터(거래형)"**과 같습니다. 직원들이 돌아다니는 구조이므로 복도(LAN)가 넓어야 하지만, 관리자는 각 방에서 개별 책상을 관리할 필요가 없습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

NAS 도입 시 가장 중요한 것은 **"IOPS와 Throughput 중 무엇이 중요한가?"**를 판단하는 것입니다.

#### 1. 실무 시나리오 및 의사결정
1.  **상황 A (영상 편집팀)**: 4K 영상 원본은 파일 크기가 크므로 **Throughput(대역폭)**이 중요함.
    *   **Decision**: **Link Aggregation (LACP)** 혹은 **40GbE** 포트를 사용하여 병목을 해소하고, **SSD Cache** 기능이 있는 NAS 선택.
2.  **상황 B (소규모 사무실)**: 문서, 엑셀 파일은 IOPS(초당 트랜잭션)보다 편리성과 백업이 중요함.
    *   **Decision**: 2-Bay 또는 4-Bay