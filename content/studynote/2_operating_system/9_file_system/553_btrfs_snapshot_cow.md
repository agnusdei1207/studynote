+++
title = "553. Btrfs (B-tree FS) - 스냅샷 및 CoW 지원"
date = "2026-03-14"
weight = 553
+++

# 553. Btrfs (B-tree FS) - 스냅샷 및 CoW 지원

## # [주제명] Btrfs (B-tree File System)
### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Btrfs (B-tree File System)는 Copy-on-Write (CoW) 메타데이터 아키텍처와 B-tree (Balanced Tree) 구조를 기반으로, 파일 시스템과 논리 볼륨 관리자(LVM, Logical Volume Manager)의 기능을 통합한 차세대 스토리지 솔루션이다.
> 2. **가치**: 데이터 및 메타데이터의 무결성을 256비트 체크섬(Checksum)으로 보장하며, 스냅샷(Snapshot), 압축(Compression), 중복 제거(Deduplication)를 통해 스토리지 효율성을 극대화하고 RTO (Recovery Time Objective)를 획기적으로 단축한다.
> 3. **융합**: OS 커널 레벨에서 RAID (Redundant Array of Independent Disks) 기능을 통합하여 하드웨어 의존성을 제거하고, 가상화(Virtualization) 및 컨테이너(Container) 환경의 계층형 스토리지(Layered Storage)를 최적화한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
Btrfs (B-tree File System, 종종 "Butter FS" 또는 "Better FS"로 불림)는 Oracle을 주축으로 개발된 GPL 라이선스의 리눅스용 파일 시스템이다. 이는 기존 EXT4 (Fourth Extended Filesystem) 시리즈가 가진 볼륨 관리의 한계와 데이터 무결성 검증 기능의 부재를 극복하기 위해 설계되었다. Btrfs의 가장 핵심적인 철학은 **CoW (Copy-on-Write)** 방식을 채용하여, 데이터 갱신 시 In-place Update(원위치 수정)를 수행하지 않고 새로운 블록에 기록함으로써 데이터 손상을 방지하고 스냅샷(Snapshot) 기능을 거의 무료(Almost Free)로 제공하는 데 있다. 기술적으로는 ZFS (Zettabyte File System)의 철학을 리눅스 커널 아키텍처에 맞게 재구현한 것으로 볼 수 있다.

**💡 개념 비유**
기존 파일 시스템(EXT4 등)은 수정 테이프를 사용하여 종이에 내용을 덮어쓰는 방식이다. 한번 덮어쓰면 원본은 영원히 사라진다. 반면, Btrfs는 수정할 때마다 새로운 종이에 내용을 적어 책장에 추가하고, 목차(메타데이터)만 최신 페이지를 가리키도록 수정하는 방식이다. 언제든지 과거의 목차로 되돌리면 그 시점의 책(파일 시스템 상태)을 복구할 수 있다.

**등장 배경 및 발전 과정**
1.  **기존 기술의 한계 (Legacy Limits)**:
    *   EXT 파일 시스템 계열은 고정된 Inode 테이블 구조로 인해 대용량 파일(16TB 이상) 및 파일 시스템(50TB 이상) 지원에 한계가 있었다.
    *   Bit rot(디스크 노화로 인한 조용한 데이터 부패)를 감지할 하드웨어적 또는 파일 시스템 레벨의 자동화된 검증 기능이 부족했다.
    *   LVM (Logical Volume Manager)과 파일 시스템이 분리되어 관리가 복잡하고 스냅샷 생성 시 성능 저하가 크았다.
2.  **혁신적 패러다임 (Paradigm Shift)**:
    *   **스토리지 풀(Pool) 개념 도입**: 여러 물리 디스크를 하나의 논리적 풀로 통합하여 유연한 공간 관리 가능.
    *   **End-to-End Checksum**: 데이터뿐만 아니라 메타데이터까지 모든 블록에 대해 CRC32C (32-bit Cyclic Redundancy Check) 알고리즘을 적용하여 무결성 검증.
3.  **비즈니스 요구 (Business Needs)**:
    *   클라우드 및 가상화 환경에서는 VM 이미지의 생성과 복구가 초 단위로 요구됨. 기존 방식으로는 이에 따른 스토리지 오버헤드가 감당 불가능했음.

```text
[ File System Evolution Context ]

+----------------+       +---------------------+       +---------------------+
|     EXT3/4     | ---> |     LVM + EXT4      | ---> |        Btrfs        |
|  (Journaling)  |       | (Snapshot Support)  |       | (Integrated COW FS) |
+----------------+       +---------------------+       +---------------------+
     |                            |                            |
     v                            v                            v
[ In-place Update ]         [ Layered Management ]      [ Unified COW Engine ]
[ Limited Integrity ]       [ Complex Operations ]      [ Native Data Checksum ]
```

**📢 섹션 요약 비유**: Btrfs는 "연필과 지우개로 수정하던 구식 공책"을 넘어, **"매 페이지마다 날짜가 찍힌 무한 증폭형 지능형 파일링 시스템"**과 같습니다. 중요한 기록을 추가할 때마다 원본을 훼손하지 않고 최신 페이지를 덧붙이기 때문에, 언제든지 과거의 시점으로 되돌리거나 변경 사항을 추적할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Btrfs의 내부는 모든 객체를 B-tree (Balanced Tree) 구조로 관리하며, 이는 검색, 삽입, 삭제 시 O(log N)의 일관된 성능을 보장한다. EXT4가 Inode 테이블을 고정 위치에 두는 반면, Btrfs는 모든 메타데이터를 B-tree 내의 유동적인 노드로 배치하여 구조적 유연성을 확보한다.

**1. 구성 요소 상세 분석 (Component Analysis)**

Btrfs는 여러 개의 내부 B-tree 트리를 사용하여 서로 다른 유형의 정보를 관리한다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Action) | 주요 프로토콜/포맷 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Chunk Tree** | 시스템의 '대장' | 물리 디스크 공간(Chunk)을 할당 및 회수. 물리 주소(Logical Address) <-> 물리 주소(Physical Address) 매핑 테이블 관리 | B-tree / Mixed Block Groups | 건물의 부지 측량 및 토지 대장 |
| **Extent Tree** | 파일 데이터 저장소 | 실제 파일 데이터가 위치한 Extent(연속된 블록 묶음) 정보 저장. 빈 공간(Free Space) 트리 관리 | COW B-tree | 도서관의 책장 위치 및 도서 분류 |
| **FS Tree / Root Tree** | 파일 시스템 구조 | 파일 시스템의 최상위 루트(Root) 정보, 디렉토리 구조, 파일 이름 관리. 스냅샷마다 독립된 루트를 가짐 | B-tree Reference | 회사의 조직도 및 최종 결재자 명단 |
| **Checksum System** | 무결성 검증 | 모든 데이터 및 메타 블록에 대해 256-bit Checksum(CRC32C) 계산 및 검증. 읽기 시 자동 복구(Self-healing) 시도 | CRC32C | 배송 포장의 파손 방지 스티커 및 보험 |

**2. 아키텍처 다이어그램: CoW 및 B-tree 구조**

Btrfs에서 파일 수정이 발생할 때의 내부 데이터 흐름과 메타데이터 갱신 과정을 도식화하면 다음과 같다. 이는 CoW 메커니즘과 트리 재귀 참조(Re-parenting) 과정을 핵심적으로 보여준다.

```text
[ Btrfs Write Operation Flow: File A Modification (CoW Mechanism) ]

   1. Initial State (File A exists)
   -------------------------------
   [ Chunk Tree ]                 [ FS Tree Root ]
   (Maps Logical to Physical)     (Points to Top of File Tree)
        |                                |
        | (Allocates Phys Block 100)     | (Pointer to Inode 123)
        v                                v
   [ Extent A ] -----------------> [ Inode 123 ]
   (Data: "Hello")                (Loc: Phys Block 100)

   2. User Request: Modify File A ("Hello" -> "Hello World")
   --------------------------------------------------------
   < Step A: Allocate New Space (No Overwrite) >
   Chunk Allocator finds Phys Block 200.

   < Step B: Data Write & Checksum >
   [ Extent A' ] (New Data)
   (Data: "Hello World")
   (Checksum: CRC32C calculated)

   < Step C: Metadata CoW (Recursive Update) >
   The path from Root to Leaf is copied and updated.

        [ FS Tree Root' ] (New Root)
        |
        +---> [ Inode 123' ] (Copy)
               |
               +---> [ Extent A' ] (Points to New Data)
   
   [ FS Tree Root ] (Old Root) <--- Isolated (Will be freed by GC later)
        |
        +---> [ Inode 123 ]
               |
               +---> [ Extent A ] (Old Data remains untouched)
```

**[해설]**:
1.  **데이터 기록 (Write Allocation)**: 사용자가 파일을 수정하면, Btrfs는 기존 `Extent A` (물리 블록 100)를 덮어쓰지 않는다. 대신 Chunk Allocator를 통해 새로운 여유 공간(`Phys Block 200`)을 할당받는다. 이때 Zstd (Zstandard) 또는 LZO 압축이 활성화되어 있다면 압축 후 기록한다.
2.  **체크섬 및 포인터 업데이트**: 새 블록에 데이터가 기록되면, 해당 블록의 체크섬(Checksum)을 계산하여 메타데이터 영역에 저장한다. 파일을 가리키는 Inode 역시 수정된다. 기존 Inode를 수정하지 않고 새 `Inode 123'`을 생성하여 새 Extent를 가리킨다.
3.  **루트 교체 (Atomic Switch)**: 이 변경 사항(Leaf Node -> Branch Node)을 따라 올라가며 최종적으로 새로운 `FS Tree Root'`를 생성한다. 트랜잭션(Transaction) 커밋 시점에 Root 포인터가 기존 `Root`에서 `Root'`로 원자적으로 교체된다. 이 순간 파일 시스템 상에서 파일은 수정된 것으로 간주되며, 이전 `Root`는 스냅샷이 참조하고 있지 않다면 백그라운드 GC(Garbage Collection)에 의해 회수된다.

**3. 핵심 알고리즘: NoCOW와 성능 트레이드오프**

Btrfs는 기본적으로 CoW를 사용하지만, `nodatacow` 속성이 설정된 파일이나 VM 이미지, 데이터베이스 파일 등 대용량 Random Write가 발생하는 워크로드에 대해서는 In-place Update를 수행하여 쓰기 증폭(Write Amplification)을 방지한다. 이를 위해 Btrfs 내부적으로는 `ordered_extent` 구조를 사용하여 디스크에 데이터 먼저 기록(Dirty)이 완료된 후 메타데이터(Extents)를 업데이트하는 순서를 보장하여 데이터 일관성을 유지한다.

> **📢 섹션 요약 비유**: Btrfs의 동작 원리는 "도시의 **실시간 위성 지도 업데이트 시스템**"과 같습니다. 건물이 하나 새로 지어지거나 변형되면(CoW), 전체 지도를 다시 그리는 것이 아니라 해당 구역의 타일만 새로 찍어서 교체한 뒤, 지도책의 목차(루트 노드) 페이지 번호만 수정합니다. 덕분에 언제든 이전 버전의 지도(스냅샷)로 되돌릴 수 있으며, 수정 중인 동안에도 다른 사람들은 여전히 안전하게 이전 지도를 볼 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 파일 시스템 심층 비교 분석**

| 비교 항목 | Btrfs (B-tree FS) | EXT4 (Fourth Extended FS) | ZFS (Zettabyte FS) | 비고 (Remind) |
|:---|:---|:---|:---|:---|
| **구조 (Structure)** | Copy-on-Write B-tree | Journaling Block Map (HTree) | Copy-on-Write Merkle Tree | Btrfs/ZFS는 트리 구조 기반으로 스냅샷에 유리 |
| **최대 볼륨 (Max Volume)** | 16 EiB (Exbibyte) | 1 EiB | 256 ZiB (Zebibyte) | Btrfs는 이론적으로 매우 큼 |
| **최대 파일 (Max File)** | 16 EiB | 16 TiB (Tebibyte) | 16 EiB | 대용량 단일 파일 처리 가능 |
| **무결성 (Integrity)** | **전 블록 체크섬 (Checksum)** | 메타데이터에만 한정 (Journal only) | 전 블록 체크섬 (End-to-End) | 데이터 부패(Bit rot) 자동 감지 |
| **스냅샷 (Snapshot)** | 매우 빠름 (CoW 기반) | 지원 불가 (LVM과 결합 시 느림) | 매우 빠름 | 백업 부하 감소 및 RTO 단축 |
| **압축 (Compression)** | ZSTD, LZO, ZLIB 지원 (Online) | EROFS 등으로만 가능 | LZ4, ZLE 지원 (Gzip) | 스토리지 절약 및 I/O 성능 향상 |
| **RAID 지원 (Native)** | RAID 0/1/10/5/6 (Soft RAID) | MDADM, LVM 필요 (External) | RAID-Z, Mirror (Integrated) | 파일 시스템 레벨 RAID로 관리 편의성 증가 |

**2. 과목 융합 관점 (OS, Network, DB)**

*   **운영체제(OS)와의 연계**: Btrfs는 Linux VFS (Virtual File System) 계층과 완벽하게 통합된다. `ioctl` 시스템 콜을 통해 사용자 공간(User Space) 프로그램이 `BTRFS_IOC_SNAP_CREATE` 등의 명령어로 직접 스냅샷 생성을 제어할 수 있다. 이는 Docker와 같은 컨테이너 기술의 핵심인 Layered Storage(OverlayFS, AUFS) 백엔드로 활용되어, 이미지 레이어를 효율관리하는 기반이 된다.

*   **네트워크(Network)와의 시너지**: `btrfs send/receive` 기능은 두 스냅샷 간의 증분 데이터(Incremental Data, Delta)만을 네어트워크 스트림으로 전송한다. SSH (Secure Shell)를 파이프하여 원격 서버로 백업을 받을 때, 전체 파일을 전송하는 rsync 방식에 비해 대역폭 효율이 압도적으로 높다 (N:1 압축 효과). 특히 초기 풀 백업 이후에는 매우 적은 트래픽으로 원격 복구가 가능하다.

*   **데이터베이스(DB)와의 상충관계**: DBMS(MySQL, PostgreSQL 등)는 자체적으로 버퍼 관리자(Buffer Manager)와 WAL(Write-Ahead Logging)을 통해 데이터 일관성을 보장한다. 파일 시스템 차원의 CoW가 발생하면 DB의 페이지 수정과 파일 시스템