+++
title = "531. 파일 할당 테이블 (FAT, File Allocation Table)"
date = "2026-03-14"
weight = 531
+++

# 531. 파일 할당 테이블 (FAT, File Allocation Table)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **FAT (File Allocation Table)**는 연결 할당(Linked Allocation)의 물리적 한계를 극복하기 위해, 데이터 블록 내부의 포인터 정보를 디스크 특정 영역(테이블)으로 분리하여 관리하는 **지향성 포인터 매핑 구조**이다.
> 2. **가치**: 복잡한 연결 리스트(Linked List) 탐색을 단순 배열(Array) 인덱싱으로 변환하여 $O(N)$의 디스크 탐색 오버헤드를 제거하고, 메모리 캐싱을 통해 임의 접근(Random Access) 성능을 획기적으로 개선한다.
> 3. **융합**: 단순성과 호환성을 바탕으로 **BIOS (Basic Input/Output System)** 및 **UEFI (Unified Extensible Firmware Interface)** 부팅 파티션, 이동식 매체, 임베디드 시스템의 표준 파일 시스템으로 자리 잡았다.

---

## Ⅰ. 개요 (Context & Background)

**파일 할당 테이블(FAT, File Allocation Table)**은 운영체제가 디스크 상의 파일 저장 위치를 추적하기 위해 사용하는 간단하지만 강력한 파일 시스템 구조다. 기존 연결 할당 방식에서는 '다음 블록의 주소'가 데이터 블록 내부에 저장되어 파일을 읽을 때마다 디스크 헤드가 데이터 영역을 순차적으로 읽어야 했다. 이는 **임의 접근(Random Access)** 시 치명적인 병목 구간이었다. FAT는 이 포인터 정보를 데이터 영역과 분리하여 별도의 **인덱스 영역(Index Area)**에 통합 관리함으로써, 파일의 구조를 디스크 헤드의 이동 없이 메모리 상에서만 파악할 수 있게 만들었다.

### 등장 배경: 연결 할당의 딜레마
1.  **기존 한계**: 연결 할당은 순차 접근에는 유리하지만, $i$번째 블록을 찾기 위해 $1$부터 $i-1$번까지 모든 블록을 읽어야 하는 선형 탐색(Linear Search) 비용이 발생한다.
2.  **혁신적 패러다임**: Microsoft(MS)는 디스크의 용량이 작던 시절, 포인터 정보를 전부 **RAM (Random Access Memory)**에 올려서 관리하는 방식을 고안했다. 디스크에는 데이터만 쓰고, 연결 정보는 테이블로 관리하여 디스크 **I/O (Input/Output)**를 최소화한 것이다.
3.  **비즈니스 요구**: 초기 개인용 컴퓨터(PC) 시장에서는 빠른 부팅 속도와 낮은 메모리/디스크 오버헤드가 필수적이었으며, FAT는 이러한 제약 환경에서 최적의 성능을 발휘했다.

### 구조적 비유
FAT 파일 시스템은 거대한 창고에서 물건을 찾는 방법을 개선한 것과 같다. 상자마다 "다음 상자는 3번 진열대"라고 적혀 있어 일일이 상자를 열어봐야 했던 기존 방식(연결 할당) 대신, 입구에 "물품 A는 상자 1 → 3 → 7번에 연속으로 보관"이라고 적힌 **통합 대출 장부(FAT)**를 비치해둔 셈이다.

📢 **섹션 요약 비유**: FAT는 복잡한 미로(디스크)를 탐험할 때, 입구에 있는 **'정보 센터(테이블)'**에서 전체 지도를 확인하고 나서 최적의 경로를 찾아 바로 이동하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

FAT 파일 시스템의 가장 큰 특징은 파일 시스템의 메타데이터와 실제 데이터가 분리되어 있다는 점이다. 디스크는 논리적으로 여러 영역으로 나뉘며, 상호 보완적으로 작동한다.

### 1. 구성 요소 상세 분석
FAT 파일 시스템은 크게 예약 영역(Reserved Area), FAT 영역, 루트 디렉터리 영역, 데이터 영역으로 구성된다.

| 모듈 명칭 | 역할 | 내부 동작 및 상세 | 주요 파라미터/비유 |
|:---|:---|:---|:---|
| **Boot Sector** (부팅 섹터) | 시스템 부팅 및 메타데이터 저장 | **BIOS** 또는 **UEFI** 펌웨어가 가장 먼저 읽는 섹터. 섹터 크기, 클러스터 크기, FAT 개수, 루트 엔트리 수 등 핵심 매개변수(**BPB**, BIOS Parameter Block)를 포함. 부트 스트랩 코드가 위치하여 운영체제 커널 로딩을 수행. | Volume Label, Signature (0x55AA), OEM ID |
| **FAT Region** (FAT 영역) | 파일 연결 정보 보유 | 파일 시스템의 **핵심 맵**. 각 데이터 클러스터(연속된 섹터 묶음)별 다음 위치 포인터를 저장. 데이터 구조상 손상에 대비해 2개(**FAT1**, **FAT2**)를 중복 저장(Mirroring)하며, OS는 보통 FAT1을 쓰고 FAT2를 백업으로 활용. | Cluster Link, Next Entry, EOF Marker |
| **Root Directory** (루트 디렉터리) | 최상위 파일/폴더 정보 저장 | 고정된 크기(예: 512 엔트리)를 가지며, **FAT32**에서는 클러스터 체인으로 관리되어 크기 제한이 사라짐. 파일명, 확장자, 속성(Read-only, Hidden, System), 시작 클러스터 번호, 파일 크기(32bit) 등의 메타데이터 저장. | `.` (Current), `..` (Parent) 처리, LFN (Long File Name) |
| **Data Region** (데이터 영역) | 실제 파일 데이터 저장 | 사용자가 저장하는 실제 내용이 위치하는 곳. 클러스터 단위로 할당되며, 할당 단위가 커질수록 내부 단편화(Internal Fragmentation)가 증가하지만 관리 오버헤드는 줄어듦. 이 영역의 조각화(Fragmentation)가 성능 저하의 주원인이 됨. | Cluster Size (4KB, 8KB...), Slack Space |

### 2. 디스크 레이아웃 및 데이터 흐름 (ASCII Diagram)
FAT 파일 시스템이 디스크 상에 어떻게 배치되는지 시각화하고, 파일이 생성될 때 포인터가 어떻게 업데이트되는지 보여준다.

```text
Disk Physical Layout (Logical View)
+============================================================================+
| Reserved Area                        | FAT 1  | FAT 2  | Root Dir | Data    |
|--------------------------------------|--------|--------|----------|---------|
| Boot Sector + BPB + Other Code       | Table  | (Copy) | Entries  | Region  |
+============================================================================+

Data Flow: Creating a File 'A.txt' (Size: 6KB, Cluster: 2KB)
-----------------------------------------------------------------------
[A] OS reads FAT table into Memory (Cache)
[B] Finds Free Clusters: 2, 5, 8 in FAT Table
[C] Updates FAT Table in Memory: 2->5, 5->8, 8->EOF
[D] Writes Metadata to Root Directory
[E] Writes Data to Clusters 2, 5, 8

      Memory View (FAT Cache)                     Disk Data Area
      +-------+-------+-------+                   +-------------+
Index | ...   | 2     | 3     | ...               | [Cluster 2]  |
      +-------+-------+-------+                   | "A" Data (1) |
Value | ...   | 5     | Free  | ...               +-------------+
      +-------+-------+-------+         -----^          |
                                         |             |
                                         v             |
      +-------+-------+-------+        +-------------+ |
Index | 4     | 5     | 6     |        | [Cluster 5]  | |
      +-------+-------+-------+        | "A" Data (2) | |
Value | Free  | 8     | Free  |        +-------------+ |
      +-------+-------+-------+         -----^         |
                                            |         |
                                            v         v
                                    +-------------+   |
                                    | [Cluster 8]  |<+
                                    | "A" Data (3) |
                                    +-------------+
                                    | 0x0FFFFFF8   | (EOF Mark)
                                    +-------------+
```

**해설**:
위 다이어그램은 파일 `A.txt`가 비연속적으로 클러스터 2, 5, 8번에 할당되는 과정을 보여줍니다. 
1. **운영체제(OS)**는 FAT 영역을 **메모리(RAM)**에 로드합니다. 이로 인해 디스크 액세스 없이 빠르게 빈 공간을 검색합니다.
2. 비연속적인 데이터 블록(2, 5, 8)이 존재하지만, 논리적인 순서는 **FAT 테이블(메모리)**에 의해 2→5→8로 단순화됩니다.
3. 실제 디스크 헤드가 움직여 데이터를 쓸 때는 물리적으로 분산된 위치를 찾아가지만(Seek), 파일의 '연결 상태'를 파악하는 데는 $O(1)$의 시간 복잡도를 가집니다.

### 3. 심층 동작 원리 및 코드 구현
FAT에서 파일을 읽는 과정은 연결 리스트(Linked List)를 순회하는 것과 수학적으로 동일하다. 그러나 포인터가 데이터 영역이 아닌 별도 테이블에 있으므로 캐시 적중률(Cache Hit Ratio)이 높다.

```c
// FAT 파일 읽기 의사 코드 (Pseudo-code)
// 전역 변수: fat_table[] (메모리에 적재된 FAT), disk[]

#define EOF_MARKER     0x0FFFFFF8  // FAT32 End of File Marker
#define CLUSTER_SIZE   4096        // 4KB Cluster

typedef unsigned int DWORD;

void read_fat_file(DWORD start_cluster, int file_size) {
    DWORD current = start_cluster;
    int bytes_read = 0;
    char buffer[CLUSTER_SIZE];

    printf("Starting read from Cluster %d\n", start_cluster);

    while (current != EOF_MARKER) {
        // 1. 디스크 데이터 영역에서 실제 데이터 읽기 (Random Access 가능)
        // FAT 테이블을 보고 알게 된 주소로 바로 이동(Seek)하여 읽음
        read_physical_disk_cluster(current, buffer);
        process_data(buffer); 

        bytes_read += CLUSTER_SIZE;

        // 2. FAT 테이블을 조회하여 다음 클러스터 번호 획득 (O(1) 접근)
        // 디스크를 읽는 것이 아니라 메모리에 있는 배열을 조회함
        current = fat_table[current];
        
        if (bytes_read >= file_size) break;
    }
}
```

### 4. FAT 시리즈 비교 (Bit Depth 및 용량 한계)
FAT는 엔트리를 저장하는 비트 수에 따라 관리 가능한 클러스터 수와 볼륨 크기가 결정된다.

| 종류 | 엔트리 크기 | 최대 클러스터 수 | 최대 볼륨 크기 (이론적) | 클러스터 크기 예시 | 주요 용도 |
|:---|:---:|:---:|:---:|:---|:---|
| **FAT12** | 12비트 | $2^{12}$ (4,096) | ~32 MB (실질적) | 0.5KB ~ 4KB | 플로피 디스크, 작은 미디어 |
| **FAT16** | 16비트 | $2^{16}$ (65,536) | ~2 GB (64KB/Cluster 시) | 2KB ~ 32KB | MSDOS, Windows 95, 작은 파티션 |
| **FAT32** | 28비트 사용 | $2^{28}$ (268,435,456) | ~2 TB (실질적 32GB~2TB) | 4KB ~ 64KB | SD 카드, USB, 대용량 이동식 드라이브 |
| **exFAT** | 32비트 이상 | 매우 큼 | 256 PB (Petabytes) | 4KB ~ 32MB | 4GB 이상 대용량 파일 지원, 최신 장치 |

*주의: FAT32는 32비트 중 상위 4비트를 예약(Reserved)으로 사용하므로 실제로는 28비트를 주소로 활용한다.*

📢 **섹션 요약 비유**: FAT의 구조는 **'비상 연락망'**과 같습니다. 대원들은 각자 몸에 누구에게 연락해야 할지 모르고(데이터 블록), 오직 중앙 사령부(FAT)의 대장정보표만 보고 다음 목적지로 이동합니다. 대장정보표만 메모리에 남기면 전체 작전 경로를 빠르게 파악할 수 있습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: FAT vs. Linked Allocation vs. Indexed Allocation
파일 시스템의 데이터 할당 기법은 FAT 외에도 연결 할당, 인덱스 할당(Unix i-node 방식)이 있으며, 각각은 서로 다른 트레이드오프(Trade-off)를 가진다.

| 비교 항목 | 연결 할당 (Linked Allocation) | **FAT (File Allocation Table)** | 인덱스 할당 (Indexed Allocation, Unix inode) |
|:---|:---|:---|:---|
| **포인터 위치** | **데이터 블록 내부** (헤드) | **별도 테이블 영역** (FAT) | **별도 블록** (i-node 및 간접 블록) |
| **임의 접근** | 매우 느림 ($O(N)$ Seek 필요) | **빠름** (Table 전체를 Memory Cache 시 $O(1)$ 조회) | 매우 빠름 (직접 블록 포인터 $O(1)$, 간접 블록 시 $O(\log N)$) |
| **외부 단편화** | 없음 (Dynamic Allocation) | **있음** (느슨한 연결 가능, 장기 사용 시 Fragmentation 심화) | 없음 (Block 단위 할당) |
| **디스크 오버헤드** | 블록마다 포인터 공간 낭비 | **테이블 크기에 따른 공간 낭비** ($O(N)$) | i-node 영역 낭비 (고정 크기) |
| **신뢰성** | 포인터 손상 시 파일 하나 손상 | **테이블 손상 시 전체 파일 시스템 마비** (Single Point of Failure) | i-node 손상 시 해당 파일만 손상 |
| **구현 복잡도** | 단순 | 단순 (하지만 테이블 관리 로직 필요) | 복잡 (다중 간접 블록 관리) |

### 2. OS 및 네트워크 융합 관점

#### A. OS 커널 및 메모리 관리
- **메모리 맵핑**: FAT는 구조가 단순하여 커널의 **VFS (Virtual File System)** 계층에서 드라이버를 작성하기 쉽다. FAT 테이블을 단순히 배열