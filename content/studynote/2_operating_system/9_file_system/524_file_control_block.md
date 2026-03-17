+++
title = "524. 파일 제어 블록 (FCB, File Control Block) / 아이노드 (inode)"
date = "2026-03-14"
weight = 524
+++

# 524. 파일 제어 블록 (FCB, File Control Block) / 아이노드 (inode)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: FCB (File Control Block)는 파일 시스템(File System) 내에서 파일의 **메타데이터(Metadata)**를 관리하는 핵심 제어 구조체로, 데이터 블록과 논리적 파일을 분리하여 추상화한다.
> 2. **가치**: inode (Index Node) 기반의 구조는 하드 링크(Hard Link)를 통한 다중 이름 관리를 지원하며, **Direct/Indirect Block** 매핑을 통해 소규모 파일의 빠른 접근부터 대용량 파일의 효율적 저장까지 지원하여 I/O 성능을 최적화한다.
> 3. **융합**: VFS (Virtual File System)의 `inode` 캐싱(Caching)과 Page Cache 연동을 통해 메모리 관리(Memory Management)와 결합하며, DAC (Discretionary Access Control)의 기반이 되어 시스템 보안의 핵심 축을 담당한다.

---

### Ⅰ. 개요 (Context & Background)

**FCB (File Control Block)**는 운영체제(Operating System, OS)가 각 파일마다 유지하는 정보의 집합체로, 파일 시스템의 **'뇌'**에 해당한다. 이는 사용자가 파일의 실제 데이터(내용)를 직접 다루지 않고도 파일을 생성, 삭제, 읽기, 쓰기할 수 있게 해주는 논리적 인터페이스의 근간이다.

파일 시스템의 발달 과정에서 초기에는 파일명과 데이터가 섞여 있었으나, 관리의 복잡도가 높아지고 다중 사용자 환경(Multi-user Environment)이 도입되면서 **"파일의 이름(Naming)"과 "파일의 실체(Entity)"의 분리**가 필수적인 과제로 대두되었다. 특히 UNIX 계열의 시스템에서는 이를 **inode (Index Node)**라는 구조로 체계화하여, 하나의 물리적 데이터가 여러 개의 논리적 이름(하드 링크)을 가질 수 있는 유연성을 제공한다.

> **💡 개념 비유**: FCB는 도서관의 **'책 목록 카드(카탈로그)'**와 같다. 책(실제 데이터)은 서가에 꽂혀 있지만, 그 책의 위치, 분류 번호, 저자, 대출 가능 여부와 같은 정보는 목록 카드(FCB)에 따로 기록되어 있다. 사서(OS)는 책의 내용을 다 읽지 않아도 카드만 보고 책을 관리할 수 있다.

**등장 배경 및 철학**
1.  **추상화 (Abstraction)**: 저장 장치(Storage Device)의 복잡한 물리적 섹터(Pysical Sector) 주소를 사용자에게 숨기고, 논리적인 바이트 스트림(Byte Stream) 단위로 접근하게 한다.
2.  **성능 최적화 (Performance Optimization)**: 파일 목록을 조회(list)하거나 권한을 검증(check permission)할 때, 수 GB의 파일 데이터를 읽을 필요 없이 수백 바이트의 FCB만 읽으면 되므로 엄청난 I/O 비용을 절약한다.
3.  **공유 및 동시성 (Sharing & Concurrency)**: 다른 경로에서 동일한 파일에 접근해야 할 때, FCB를 통해 참조 횟수(Reference Count)를 관리하여 안전하게 공유할 수 있는 메커니즘을 제공한다.

📢 **섹션 요약 비유**: 파일 제어 블록의 개념은 마치 **"호텔의 객실 키 카드와 컴퓨터 등록부"**가 합쳐진 것과 같다. 손님(사용자)은 방 번호(파일명)만 알고 있지만, 호텔 직원(OS)은 중앙 컴퓨터(FCB)를 통해 해당 객실의 청소 상태, 현재 투숙객, 잔여 비용 등의 상세 정보를 실시간으로 파악하고 관리하는 원리다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

FCB의 구현은 파일 시스템마다 상이하지만, **POSIX (Portable Operating System Interface)** 표준을 따르는 리눅스(Linux) 시스템에서는 **inode (Index Node)**라는 구조체를 사용한다.

#### 1. 구성 요소 (Components)
inode는 파일 시스템 생성 시 할당된 고정 번호(inode number)를 식별자로 가지며, 크게 파일의 속성을 나타내는 메타데이터 영역과 데이터의 위치를 가리키는 포인터 영역으로 나뉜다.

| 구분 (Category) | 항목 (Field) | 설명 (Description) | 내부 동작 (Internal Behavior) |
|:---:|:---|:---|:---|
| **식별자** | **inode 번호** | 파일 시스템 내 유일한 ID | 파일 시스템 파티션 내 고유 값, 디렉터리 엔트리에 저장됨 |
| **유형** | **File Mode** | 파일, 디렉터리, 블록 디바이스, 심볼릭 링크 등 구분 | `st_mode` 변수의 상위 비트(Bit Mask)를 통해 판별 |
| **권한** | **Access Rights** | 읽기/쓰기/실행 (rwx) 권한 | User, Group, Others별 3비트씩 총 12비트 할당 (setuid/setgid 포함) |
| **소유자** | **UID / GID** | 사용자(User) 및 그룹(Group) ID | `chown` 시스템 호출 시 커널(Kernel)이 이 필드를 수정 |
| **시간 정보** | **Timestamps** | atime(Access), mtime(Modify), ctime(Change) | 데이터 쓰기 → mtime 갱신, 메타데이터 변경 → ctime 갱신 |
| **크기** | **File Size** | 바이트(Byte) 단위 파일 크기 | `off_t` 타입(주로 64비트)으로 저장, 대용량 파일 지원 |
| **링크 수** | **Link Count** | 이 파일을 가리키는 하드 링크의 개수 | 0이 되면 데이터 블록과 inode 자체를 디스크에서 해제(Deallocate) |
| **데이터 포인터** | **Block Pointers** | 데이터가 저장된 디스크 블록 주소 배열 | **Direct/Indirect** 주소 지정 방식을 사용하여 유연한 매핑 수행 |

#### 2. 데이터 블록 매핑 메커니즘 (Direct & Indirect Blocks)
파일의 크기는 가변적이므로, 고정된 크기의 inode 내부에 모든 데이터 블록의 주소를 저장하기 어렵다. 이를 해결하기 위해 유닉스 파일 시스템(UNIX File System, UFS)은 계층적인 주소 지정 방식을 사용한다.

**ASCII 다이어그램: inode 구조와 Direct/Indirect 블록 매핑**

```text
      [ inode 구조체 (Fixed Size: 256 Bytes) ]
   ┌───────────────────────────────────────────┐
   │ File Permissions │ Owner (UID/GID) │ Size │  <- 메타데이터 영역
   │ File Times (atime/mtime/ctime) │ Links...│
   ├───────────────────────────────────────────┤
   │  Data Block Pointers Array (15 Pointers)  │
   │  ┌─────────────────────────────────────┐  │
   │  │ 0  ──┐                               │  │
   │  │ 1  ──┤                               │  │
   │  │ .. ──┼──▶ [Data Block 0]            │  │ (Direct Blocks: 12개)
   │  │ 11 ──┘   (Small File Data)          │  │ 빠른 접근, 1단계 I/O
   │  ├─────────────────────────────────────┤  │
   │  │ 12 ───────────────────┐              │  │
   │  │      (Single Indirect)│              │  │
   │  │                       └──▶ [Indirect] │  │
   │  │                            ├─▶ [DB12] │  │ (Single Indirect: 1개)
   │  │                            ├─▶ [DB13] │  │ 중간 파일, 2단계 I/O
   │  │                            └─▶ ...    │  │
   │  ├─────────────────────────────────────┤  │
   │  │ 13 ───────────────────────┐          │  │
   │  │      (Double Indirect)    │          │  │
   │  │                          ┌┴─▶ [Double]│  │
   │  │                          │    └─▶ [Single] │ (Double Indirect: 1개)
   │  │                          │       └─▶ [DB]  │ 대용량 파일, 3단계 I/O
   │  ├─────────────────────────────────────┤  │
   │  │ 14 ───────────────────────┐          │  │
   │  │      (Triple Indirect)    │          │  │
   │  │                          └┴─▶ [Triple]│  │
   │  │                               ...     │  │ (Triple Indirect: 1개)
   │  │                                     ... │  │ 매우 큰 파일, 4단계 I/O
   │  └─────────────────────────────────────┘  │
   └───────────────────────────────────────────┘
```

**해설:**
1.  **직접 블록 (Direct Blocks, 0~11)**: 실제 데이터가 담긴 디스크 블록의 주소를 직접 가리킨다. 대부분의 일반 파일(예: 텍스트 파일, 소스 코드)은 이 영역에 들어가며, 단 한 번의 디스크 접근만으로 데이터를 읽을 수 있어 가장 빠르다.
2.  **단일 간접 블록 (Single Indirect Block, 12)**: 데이터를 담은 블록을 가리키는 것이 아니라, **'주소들의 목록'**을 담은 블록을 가리킨다. 블록 크기가 4KB이고 주소가 4Byte(32bit)라면, 하나의 간접 블록은 1,024개의 데이터 블록을 가리킬 수 있다(약 4MB 추가 지원).
3.  **이중/삼중 간접 블록 (Double/Triple Indirect Block, 13/14)**: 포인터가 가리키는 대상이 다시 간접 블록인 구조다. 이론적으로 지오바이트(GB)~테라바이트(TB) 단위의 파일을 지원할 수 있지만, 데이터를 읽기 위해 디스크를 여러 번 읽어야 하므로 접근 속도(Latency)는 증가한다. (최신 파일 시스템은 이를 **Extent** 기법으로 개선하기도 함)

**핵심 알고리즘: 파일 오프셋 → 블록 주소 변환**
파일 시스템이 `read(fd, buffer, 1000, offset=5000000)`과 같은 시스템 호출을 받았을 때, 커널은 오프셋을 블록 주소로 변환해야 한다.

```c
// Pseudo-code: Logical Block Number (LBN) to Physical Block Address
// Assumptions: Block Size = 4KB, Pointers per Block = 1024
// Direct: 12 blocks, Single Indirect: 1024 blocks, ...

struct inode {
    unsigned int addrs[15]; // 12 Direct, 1 Indirect, ...
};

uint bmap(struct inode *ip, uint offset) {
    uint lbn = offset / BSIZE; // Logical Block Number (예: lbn = 1225)
    uint addr_index;

    if (lbn < 12) {
        // 1. Direct Block 영역
        return ip->addrs[lbn];
    } 
    else if (lbn < 12 + 1024) {
        // 2. Single Indirect 영역 (lbn이 1225라면, index는 1213)
        addr_index = lbn - 12;
        
        // 간접 블록의 내용을 메모리로 읽어옴 ( 디스크 I/O 발생 )
        uint* indirect_block = (uint*)read_disk_block(ip->addrs[12]);
        return indirect_block[addr_index];
    }
    else {
        // 3. Double Indirect 영역
        // ... (이중 포인터 역참조 로직 수행) ...
    }
}
```

📢 **섹션 요약 비유**: inode의 데이터 포인터 구조는 **"도심의 주소 체계"**와 같다. 가까운 거리(Direct Block)는 번지수만 바로 알려주지만, 지방(Indirect Block)으로 갈수록 "시 > 구 > 동 > 번지"와 같이 계층적인 안내(간접 참조)를 거쳐야 정확한 위치(데이터)를 찾을 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

FCB(inode)는 단순한 저장소 정보를 넘어, OS의 메모리 관리, 보안, 데이터베이스 시스템과 깊이 상호작용한다.

#### 1. 디스크 inode vs 메모리 VFS inode
리눅스 커널은 하드웨어(HDD/SSD)에 존재하는 정적인 정보와 메모리(RAM)에 존재하는 동적인 정보를 분리하여 관리한다. 이를 **VFS (Virtual File System)** 계층이 추상화한다.

**ASCII 다이어그램: 디스크 inode와 VFS inode의 관계**

```text
         [ Disk (HDD/SSD) ]                     [ Memory (RAM) ]
┌───────────────────────────┐             ┌──────────────────────────┐
│ Inode Table (Static)      │             │ VFS Inode Cache (Dynamic)│
│ ┌───────────────────────┐ │    Load     │ ┌──────────────────────┐ │
│ │ On-Disk Inode #1024   │ │ ───────────▶│ │ struct inode *cached │ │
│ │ - Permissions: 644    │ │   (I/O)     │ │ - State: "Dirty"     │ │
│ │ - Size: 4096          │ │             │ │ - Lock: Semaphore    │ │
│ │ - Ptrs: [12, ...]     │ │             │ │ - Ref Count: 3       │ │
│ └───────────────────────┘ │             │ └──────────────────────┘ │
└───────────────────────────┘             └──────────────────────────┘
         ▲                                          │
         │ Writeback                                │ Process Access
         │ (Dirty Flushing)                         ▼
    ┌────┴───────┐                           ┌──────────┐
    │ Filesystem │                           │ fd Table │
    └────────────┘                           └──────────┘
```

**해설:**
-   **On-Disk Inode**: 영구 저장소(Persistent Storage)에 존재하며, 파일 시스템이 마운트(Mount)될 때의 '원본(Source of Truth)'이다.
-   **VFS Inode**: 파일에 접근할 때마다 디스크에서 읽어오면 너무 느리므로, 커널 메모리(Slab Allocator)에 캐싱(Caching)해둔다.
-   **차이점**: 메모리상 VFS inode에는 파일 시스템이 실제로 필요하지 않은, OS 운영을 위한 **락(Lock)**, **참조 카운트(Reference Count)**, **더티 플래그(Dirty Flag)** 등의 동적 정보가 추가된다.

#### 2. 과목 융합 분석

| 융합 영역 | 상세 설명 및 시