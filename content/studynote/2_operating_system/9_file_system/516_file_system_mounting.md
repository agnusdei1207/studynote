+++
title = "516. 파일 시스템 마운팅 (Mounting)"
date = "2026-03-14"
weight = 516
+++

# 516. 파일 시스템 마운팅 (Mounting)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마운팅(Mounting)은 OS (Operating System) 커널이 관리하는 단일 디렉터리 트리에, 이기종의 저장 장치나 네트워크 자원의 파일 시스템을 논리적으로 결합시켜 물리적 경계를 허무는 핵심 인프라 메커니즘이다.
> 2. **가치**: `VFS (Virtual File System)` 계층을 통해 Heterogeneity(이질성)를 은폐하고 `Unified Namespace (단일 네임스페이스)`를 제공함으로써, 애플리케이션에게 장치 독립적인 I/O 인터페이스를 보장하여 운영 효율성을 극대화한다.
> 3. **제어**: `Mount Table` 관리와 `Superblock (슈퍼블록)` 검증을 기반으로 시스템 무결성을 유지하며, `Sync (동기화)` 및 `Unmount (언마운트)` 절차를 통해 데이터 손실을 방지하는 철저한 상태 관리가 수반된다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 기술적 정의 및 철학
마운팅이란 커널의 루트 파일 시스템(Root Filesystem) 트리 구조에, 새로운 블록 장치(Block Device)나 네트워크 자원의 파일 시스템을 특정 디렉터리(마운트 포인트) 하위로 논리적으로 연결하는 시스템 콜 및 프로세스를 의미한다. 이는 단순한 경로 연결이 아니라, 해당 경로에 대한 `VFS`의 룩업(Lookup) 연산이 기존 로컬 `Inode (Index Node)`에서 새로운 장치의 `Root Inode`로 교체(Redirect)되도록 커널 내부 데이터 구조를 동적으로 재구성하는 작업이다.

### 2. 등장 배경 및 진화
1.  **초기 제약**: 초기 컴퓨팅 환경은 하나의 물리적 디스크만 사용하거나, 디스크 교체 시 전체 시스템 재부팅이 필요했다.
2.  **유닉스 철학 (UNIX Philosophy)**: "모든 것은 파일이다"라는 철학 아래, 로컬 디스크, 네트워크 소켓, 파이프 등을 하나의 통합된 트리로 관리하여 사용자가 투명하게 접근하게 하려는 패러다임이 등장했다.
3.  **현대적 요구**: 클라우드 환경에서의 `NAS (Network Attached Storage)` 연결, 컨테이너의 볼륨 마운트, 분산 파일 시스템 등 가상화된 자원을 동적으로 통합하는 핵심 인프라로 진화했다.

### 3. 논리적 vs 물리적 뷰

```text
[ Logical View (User/Process) ]          [ Physical View (Kernel/Device) ]
+---------------------------+            +-----------------------------+
| / (Root)                  |            | Disk A (/dev/sda1) - EXT4   |
| ├── bin/                  |            +-----------------------------+
| ├── home/                 | <----------| User Data                   |
| │   └── user/             | (Mount)    +-----------------------------+
| └── mnt/                  |            | Disk B (/dev/sdb1) - XFS    |
|     └── backup/           | <----------| Database Archives           |
+---------------------------+            +-----------------------------+
                                            |
                                            v
                                     +-----------------------------+
                                     | Network (NFS Server)        |
                                     | Remote Files                |
                                     +-----------------------------+
```
> **도해 설명**: 사용자 영역(User Space)에서는 `/mnt/backup`이라는 단일 경로만 인지하지만, 커널 영역(Kernel Space)에서는 해당 경로 요청이 들어올 시점에 물리적으로 완전히 다른 디스크나 네트워크 자원으로 I/O를 라우팅(Routing) 한다. 이러한 투명성(Transparency)이 마운팅의 핵심 가치이다.

📢 **섹션 요약 비유**: 마운팅은 **"복잡한 고속도로 톨게이트에 하이패스 차로(고속 패스)를 병설하여, 진입 방식(장치 종류)에 상관없이 모든 차량을 하나의 톨게이트(마운트 포인트)로 유입시키는 것"**과 같다. 운전자(사용자)는 진입 후 어디로 연결되는지 몰라도 목적지(데이터)에 원활히 도착할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 마운트 아키텍처 상세 구조
마운팅은 커널의 `Mount Table`, `VFS` 인터페이스, 그리고 특정 파일 시스템 드라이버가 상호작용하는 복합적인 메커니즘이다.

#### [주요 컴포넌트 상세표]
| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 관련 프로토콜/구조 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Mount Table** | 마운트 상태 저장 | 마운트 포인트 경로와 장치 ID, 플래그(예: RO, NOEXEC)를 매핑하는 해시 테이블(Hash Table) | Kernel Struct | 전화 번호부 |
| **VFS (Virtual File System)** | 추상화 계층 | 특정 파일 시스템의 세부 구현을 은폐하고 `read()`, `write()`, `open()` 등 표준화된 인터페이스 제공 | POSIX API | 통번역사 |
| **Superblock** | 파일 시스템 메타데이터 | 파일 시스템 전체 크기, Free Block 개수, Inode Table 위치 등 FS의 생명 정보 관리 | FS Specific | 파출부 근무표 |
| **Inode / Dentry Cache** | 경로 탐색 캐싱 | 마운트 포인트 경로 탐색(`d_lookup`) 속도를 높이기 위한 커널 메모리 캐시 | LRU Algorithm | 단축 아이콘 |
| **File System Driver** | 실질적 I/O 실행 | `ext4`, `xfs`, `nfs` 등 특정 포맷의 데이터를 물리적 매체에 기록/판독 | Block/NFS I/O | 장비 조작원 |

### 2. 마운트 수행 절부 (Step-by-Step)
마운트 시스템 콜(`mount(syscall)`)이 호출되었을 때의 커널 내부 동작 과정은 다음과 같다.

```text
            [USER SPACE]                     [KERNEL SPACE]
                  │                                 │
    1. mount("/dev/sdb1", "/mnt")          ▼
 ────────────────────────────────────────────────────────────────
                  │                          │
      ┌───────────▼───────────┐   2. Look up Inode for "/mnt"
      │  System Call Handler  │   (Verify Directory Existence)
      └───────────┬───────────┘              │
                  │        3. Read Superblock of /dev/sdb1
                  │   (Check FS Magic Number, Integrity)
      ┌───────────▼───────────┐              │
      │   File System Driver  │   4. Allocate Mount Descriptor
      │   (e.g., ext4.ko)     │   (Mount Table Entry Creation)
      └───────────┬───────────┘              │
                  │        5. Link VFS Inode of "/mnt"
                  │      to Root Inode of /dev/sdb1
                  │                          │
      └───────────┬───────────┘   ┌──────────▼───────────┐
                  │                │  Mount Table Update │
                  └────────────────│  /mnt -> /dev/sdb1   │
                                   └──────────────────────┘
```
> **도해 해설**:
> 1.  **검증 (Lookup & Verify)**: 사용자가 지정한 마운트 포인트(`target directory`)가 존재하고, 다른 파일 시스템이 이미 마운트되어 있지 않은지(혹은 덮어쓰기 옵션 확인) 검사한다.
> 2.  **판독 (Read SB)**: 소스 장치의 `Superblock`을 읽어 파일 시스템 타입을 식별(Magic Number 확인)하고, 손상 여부를 검사한다.
> 3.  **갱신 (Binding)**: 커널의 마운트 테이블에 새로운 엔트리를 추가하고, `/mnt` 경로에 대한 `Dentry (Directory Entry)` 캐시가 새로운 장치의 루트 `Inode`를 가리키도록 수정(Lookup Redirect)한다.

### 3. 핵심 알고리즘: 경로 해석 (Path Resolution)
`VFS`는 경로 이름을 분석할 때 `Mount Table`을 참조하여 하위 트리를 탈출하고 새로운 트리로 진입하는지를 판단한다. 이를 **'Mount Point Crossing'**이라 한다.

```c
// Pseudo-code for VFS Path Resolution
struct vnode *vfs_lookup(struct vnode *start_dir, char *path) {
    struct vnode *vp = start_dir;
    
    while (*path != '\0') {
        // 1. 현재 vnode가 마운트 포인트인지 확인
        if (IS_MOUNTED(vp)) {
            // Mount Table을 조회하여 실제 파일 시스템의 루트 vnode로 교체
            vp = get_mount_root(vp);
        }

        // 2. 일반 디렉터리 탐색 수행
        vp = lookup_component(vp, extract_token(&path));
        
        if (vp == NULL) return ERR_NOT_FOUND;
    }
    return vp;
}
```
> **코드 분석**: 위 코드는 마운팅의 핵심 로직을 보여준다. 경로 탐색 중 `IS_MOUNTED` 플래그를 만나면, `vnode`(가상 노드)를 부모 트리의 것이 아닌 마운트된 장치의 루트로 교체(Switch)한다. 이 단순한 분기문 덕분에 사용자는 `/mnt/data/file.txt`를 요청할 때 복잡한 장치 식별자나 네트워크 프로토콜을 몰라도 된다.

📢 **섹션 요약 비유**: 마운팅된 시스템의 경로 탐색은 **"호텔 객실의 연결문"**과 같다. 복도(루트 경로)를 걷다가 특정 객실(마운트 포인트)에 들어서면, 그 문을 지나는 순간 갑자기 다른 건물(외부 장치)의 로비에 도착하게 된다. 손님은 그 문이 지나는 순간 공간의 좌표계가 바뀌었음을 인지하지 못하고 자연스럽게 이동한다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. OS별 네임스페이스 구조 비교 (Unix vs Windows)
파일 시스템을 통합하는 방식은 OS 설계 철학에 따라 결정적인 차이를 보인다.

| 비교 항목 | 유닉스/리눅스 (UNIX/Linux) | 윈도우 (Windows) |
|:---|:---|:---|
| **네임스페이스** | **단일 계층 트리 (Single Hierarchical Tree)** | **분리된 드라이브 문자 (Drive Letters)** |
| **루트 (Root)** | `/` (단일 루트) | `C:\`, `D:\`, `E:\` (다중 루트) |
| **마운트 유연성** | 매우 높음 (임의의 깊이의 디렉터리에 마운트 가능) | 상대적으로 낮음 (Volume Mount Point나 경로 기반 마운트는 존재하나 관례상 드라이브 문자 위주) |
| **장치 독립성** | 높음 (물리적 위치와 논리적 경로가 완전히 분리됨) | 낮음 (물리적 파티션과 경로가 강하게 결합됨) |

### 2. 네트워크 저장소와의 융합 (NFS/CIFS)
마운팅은 로컬 디스크를 넘어 네트워크 자원에도 적용된다.
-   **NFS (Network File System)**: 리눅스 환경에서 원격 서버의 디렉토리를 로컬에 마운트하여 로컬 파일 시스템처럼 쓰게 한다. 이때 커널의 `RPC (Remote Procedure Call)` 계층이 I/O 요청을 네트워크 패킷으로 변환한다.
-   **CIFS/SMB**: 윈도우 환경의 네트워크 드라이브 매핑과 유사하나, 리눅스에서는 이를 마운트 포인트에 통합하여 관리한다.

```text
+-------------------------+      Network      +--------------------------+
|   Client System A       | :===============> |   Server System B        |
+-------------------------+                   +--------------------------+
| /data (Local Disk)      |                   | /exports/projects (SSD)  |
| /mnt/backup (NFS Mount) | <--- Mapped ---   |                          |
+-------------------------+                   +--------------------------+
```
> **심층 분석**: 클라이언트 A는 `/mnt/backup`에 접근하지만, 실제 I/O는 서버 B의 디스크(SD)에 발생한다. 이때 **네트워크 대역폭(Latency)**이 파일 시스템 성능의 병목 지점이 된다. 따라서 네트워크 마운트를 사용할 때는 로컬 마운트보다 **Timeout 설정**이나 **Caching 전략(Attribute Caching, Write Back)**이 더욱 중요하다.

📢 **섹션 요약 비유**: 유닉스 방식은 모든 점포가 하나의 거대한 백화점 건물에 입점해 있는 것과 같아서(1층, 5층 등), 엘리베이터(경로)만 타면 어디로든 이동 가능하다. 반면 윈도우 방식은 각 점포가 서로 다른 건물에 떨어져 있어서(C:, D:), 건물 간 이동(경로 변경)이 불편하고 각 건물의 입구(Drive Letter)를 따로 기억해야 하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 서버 확장 및 마운트 전략
기업의 데이터 웨어하우스 서버 스토리지가 부족해졌을 때, 시스템 엔지니어는 새로운 `SAN (Storage Area Network)` 스토리지를 추가하고 마운트해야 한다.

#### [의사결정 매트릭스]
| 시나리오 | 방안 A: 신규 마운트 포인트 생성 | 방안 B: 기존 파티션 확장 (LVM) |
|:---|:---|:---|
| **방식** | 새 디스크를 `/data2` 등 독립 경로에 마운트 | `LVM (Logical Volume Manager)`을 통해 기존 `/home`에 볼륨 합체 |
| **장점** | 장애 격리(Isolation) 용이. 데이터 분리로 관리 포인트 명확 | 사용자 입장에서 파티션 용량 한계 해체. 관리 경로 단순화 |
| **단점** | 경로가 분산되어 스크립트 수정 필요. 용량 분배 비효율 가능성 | 볼륨 그�