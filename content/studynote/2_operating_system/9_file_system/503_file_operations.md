+++
title = "503. 파일 연산 (File Operations) - create, write, read, reposition, delete, truncate"
date = "2026-03-14"
weight = 503
+++

# # 503. 파일 연산 (File Operations)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파일 연산(File Operations)은 **사용자 공간(User Space)**의 프로세스가 커널(Kernel)의 **파일 시스템(File System)** 기능을 안전하게 활용하기 위해 호출하는 **시스템 콜(System Call)** 인터페이스의 집합이다.
> 2. **가치**: 이 추상화 계층은 하드웨어의 복잡성(섹터 관리, 헤드 이동, 회전 지연 등)을 은폐하고, **권한 검사(Permission Check)**와 **동시성 제어(Concurrency Control)**를 자동화하여 데이터 무결성과 보안을 보장한다.
> 3. **융합**: `Open()` 시스템 콜을 통해 메타데이터를 메모리에 **캐싱(Caching)**하는 전략은 **DBMS (Database Management System)**의 **버퍼 관리(Buffer Management)**와 **소켓 프로그래밍(Socket Programming)**의 기초가 되는 자원 관리 패러다임이다.

---

### Ⅰ. 개요 (Context & Background)

파일 연산은 운영체제(OS)가 제공하는 가장 핵심적인 추상화 서비스 중 하나로, 저장 장치의 물리적 데이터 블록을 사용자가 이해하기 쉬운 '논리적 파일' 개념으로 매핑하는 과정이다. 현대 운영체제는 단순히 데이터를 쓰고 읽는 것을 넘어, 파일의 생성부터 소멸까지의 생애 주기(Life Cycle)를 관리하며, 이 과정에서 발생할 수 있는 충돌을 방지하기 위해 정교한 상태 기계(State Machine)를 유지한다.

#### 1. 기술적 배경과 필요성
초기 컴퓨팅 환경에서는 프로그래머가 디스크의 실제 섹터(Sector) 번호를 지정하여 데이터를 써야 했으나, 이는 하드웨어 의존적이며 오류 가능성이 높은 방식이었다. 이를 해결하기 위해 **파일 시스템(File System)**이 등장했다. 파일 시스템은 데이터를 '파일'이라는 단위로 관리하며, 다음과 같은 이유로 연산 체계가 필수적이다.
-   **추상화 (Abstraction)**: 복잡한 **블록 디바이스 드라이버(Block Device Driver)** 동작을 숨기고 일관된 인터페이스 제공.
-   **접근 제어 (Access Control)**: 소유자(Owner), 그룹(Group), 기타 사용자(Others)에 대한 읽기/쓰기 권한을 커널 차원에서 검증.
-   **자원 공유 (Resource Sharing)**: 여러 프로세스가 안전하게 동일한 파일에 접근할 수 있도록 메커니즘 제공.

#### 2. 연산의 계층 구조
파일 연산은 사용자 모드(User Mode)의 **API (Application Programming Interface)**에서 시작되어, 커널 모드(Kernel Mode)의 **시스템 콜 인터페이스(System Call Interface)**를 거쳐, **VFS (Virtual File System)** 및 **파일 시스템 드라이버(File System Driver)**로 전달되는 다계층 구조를 가진다.

```text
 [ Application Layer ]  : fopen("data.txt", "w")
        │
        ▼ (Library Call)
 [ Standard Library (libc) ]
        │
        ▼ (Trap / Mode Switch)
 [ System Call Interface (SCI) ] : sys_open()
        │
        ▼
 [ VFS (Virtual File Switch) ]    : 공통 파일 인터페이스 유지
        │
        ├─▶ [ EXT4 Driver ] ──▶ [ Disk I/O ]
        ├─▶ [ NTFS Driver ] ──▶ [ Disk I/O ]
        └─▶ [ NFS Driver ]  ──▶ [ Network I/O ]
```

**해설**: 위 다이어그램은 사용자 프로세스가 파일을 열 때 호출이 전달되는 경로를 보여준다. `fopen`과 같은 표준 라이브러리 함수는 결국 `sys_open`과 같은 시스템 콜을 유발하여 CPU 모드를 유저 모드에서 커널 모드로 전환(Trap)시킨다. **VFS**는 서로 다른 파일 시스템(EXT4, NTFS 등)에 대해 통일된 인터페이스를 제공하여 상위 계층이 하위 파일 시스템의 종류를 신경 쓰지 않도록 추상화한다. 이는 '폴리모피즘(Polymorphism)' 디자인 패턴의 OS 구현 예시이다.

📢 **섹션 요약 비유**: 파일 연산 체계는 마치 **'복잡한 주방 시스템'**을 이용하는 **'식당 주문 시스템'**과 같습니다. 손님(사용자 프로세스)은 메뉴(API)만 보고 주문하면, 웨이터(시스템 콜 인터페이스)가 주방(커널/VFS)으로 전달합니다. 주방장은 어떤 재료가 어디에 있는지(물리적 디스크 위치), 누가 주문했는지(권한)를 신경 써서 요리를 완성합니다. 손님은 주방의 복잡한 프로세스를 알 필요 없이 맛있는 음식(데이터)만 받으면 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

파일 연산을 수행하기 위한 아키텍처는 크게 **심층 커널 자료 구조(Kernel Data Structures)**와 **6대 핵심 연산 로직**으로 나눌 수 있다.

#### 1. 핵심 커널 자료 구조 분석
파일 연산이 수행될 때 커널 메모리(RAM) 상에 유지되는 주요 테이블과 구조체는 다음과 같다.

| 구조 요소 | 역할 | 주요 필드/내용 | 비유 |
|:---:|:---|:---|:---|
| **PCB (Process Control Block)** | 프로세스별 열린 파일 목록 관리 | `fd[]` (File Descriptor Array) | **"내 지갑"** (내가 소유한 자산 목록) |
| **File Descriptor (fd)** | 사용자 공간에 반환되는 인덱스 | 0, 1, 2 (Stdin, Stdout, Stderr)... | **"주문 번호표"** |
| **System Open File Table** | 전역 파일 오프셋(File Pointer) 및 상태 관리 | File Offset, Open Flags, Status Flags | **"주방 주문 대장"** |
| **Inode (Index Node)** | 파일의 메타데이터 및 데이터 블록 주소 | File Size, Permissions, Block Pointers | **"도서관 목차판"** |
| **Per-Process File Table** | FD를 System Open File Table과 연결 | Pointer to System Entry | **"개인 링크"** |

#### 2. 상세 연산 동작 메커니즘 (Operations Logic)

**① 생성 (Creating a File)**
새로운 파일을 생성하는 `create()` 연산은 파일 시스템에 새로운 노드를 할당하는 과정이다.
1.  **경로 해석 (Path Resolution)**: 디렉터리 트리를 순회하며 파일명이 존재하는지 검사.
2.  **Inode 할당 (Inode Allocation)**: 가용 Inode 비트맵(Free Inode Bitmap)을 스캔하여 비어있는 Inode 확보.
3.  **메타데이터 초기화**: 소유자 **UID (User ID)**, **GID (Group ID)**, 모드(Permission Bits), 생성 시간 등 기록.
4.  **디렉터리 엔트리 추가 (Directory Entry Addition)**: 부모 디렉터리의 데이터 블록에 `<파일명, Inode 번호>` 쌍 삽입.

**② 쓰기 (Writing to a File)**
데이터를 기록하는 `write()`는 가장 복잡한 과정을 거친다.
1.  **버퍼 캐시 확인 (Buffer Cache Lookup)**: 요청한 데이터 블록이 이미 **페이지 캐시(Page Cache)**에 있는지 확인.
2.  **공간 할당 (Block Allocation)**: 파일 크기가 증가해야 한다면, 가용 블록 비트맵에서 블록을 할당하고 Inode의 간접 블록(Indirect Block) 포인터를 업데이트.
3.  **데이터 복사 (Copy-to-User/Kernel)**: 사용자 버퍼의 데이터를 커널 버퍼로 복사.
4.  **포인터 갱신 (Pointer Update)**: 시스템 전역 열린 파일 테이블의 `current file offset`을 쓴 바이트 수만큼 증가.

**③ 위치 재설정 (Repositioning / Seek)**
`lseek()` 연산은 실제 디스크 I/O를 유발하지 않고, 메모리상의 오프셋 값만 변경한다.
-   **수식**: `New_Offset = Base + Offset`
-   **Base**: `SEEK_SET(0)`, `SEEK_CUR(1)`, `SEEK_END(2)` (각각 시작, 현재, 끝 기준)

**④ 파일 자르기 (Truncating)**
`truncate()`는 데이터 블록을 해제하지만 메타데이터는 남긴다. 로그 파일 초기화 등에 사용된다.

```text
   [ User Process ]           [ Kernel Memory ]               [ Disk Storage ]
          |                          |                              |
  fd = open("log")                 |                              |
          |-----(System Call)------>|                              |
          |                          | 1. Lookup Inode ──────────▶| Search /
          |                          | 2. Load Inode to Memory ◀─| Read
          |                          | 3. Create FD Table Entry   |
          |<----(Return fd)---------|                              |
          |                          |                              |
  write(fd, "DATA")                 |                              |
          |-----(System Call)------>|                              |
          |                          | 1. Check Permission         |
          |                          | 2. Alloc Data Blocks ─────▶| Update Bitmap
          |                          | 3. Copy Data to Buffer     |
          |                          | 4. Update Offset (n += 4)   |
          |<----(Return Bytes)------|                              |
          |                          |                              |
  truncate(fd, 0)                   |                              |
          |-----(System Call)------>|                              |
          |                          | 1. Mark Blocks Free ──────▶| Update Bitmap
          |                          | 2. Update Inode Size = 0    |
          |                          | 3. Inode Dirty Marked       |
```

**해설**: 위 다이어그램은 `open`, `write`, `truncate` 연산이 커널의 자료 구조와 어떻게 상호작용하는지 보여준다. `open`은 디스크에서 메타데이터를 메모리로 가져오는 비용이 드는 작업이므로, 이후 `write`는 단순히 메모리 버퍼에 데이터를 쓰고 오프셋만 조정하는 고속 작업으로 처리된다. `truncate`는 데이터 블록을 해제(링크 카운트 감소 및 비트맵 수정)하는 작업을 수행하며, 파일의 크기 정보를 0으로 만든다.

**⑤ C 코드 스니펫 (실무 레벨)**
```c
#include <fcntl.h>
#include <unistd.h>

int main() {
    // open(): O_CREAT(생성) | O_RDWR(읽기/쓰기) | O_TRUNC(기존 데이터 삭제)
    // 0644: 권한 (rw-r--r--)
    int fd = open("test.dat", O_CREAT | O_RDWR | O_TRUNC, 0644);
    if (fd < 0) return -1; // 에러 처리

    // write(): 커널 버퍼로 데이터 복사
    const char *msg = "BrainScience PE";
    write(fd, msg, 16);

    // lseek(): 파일 포인터를 시작점(0)으로 이동
    lseek(fd, 0, SEEK_SET);

    // read(): 현재 포인터 위치에서 데이터 읽기
    char buf[32];
    read(fd, buf, 16);

    close(fd); // 자원 반납
    return 0;
}
```

📢 **섹션 요약 비유**: 파일 연산의 아키텍처는 **"비디오 편집기"**와 흡사합니다. 파일을 생성하는 것은 **"새 타임라인 만들기"**이며, 데이터 쓰기는 **"클립 추가"**입니다. 위치 재설정(Seek)은 **"재생 헤드 이동"**으로, 실제 데이터를 옮기는 것이 아니라 보는 위치만 바꾸는 것입니다. Truncate는 **"잘라내기"** 기능으로, 프로젝트 설정은 남기지만 내용은 싹 비우는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

파일 연산 방식은 운영체제마다 차이가 있으며, 다른 컴퓨터 과학 분야와 밀접하게 연관되어 있다.

#### 1. 심층 기술 비교: 저수준 vs 고수준 I/O

| 비교 항목 | 저수준 파일 I/O (System Call) | 고수준 파일 I/O (Library Function) |
|:---|:---|:---|
| **대표 함수** | `open()`, `read()`, `write()`, `lseek()` | `fopen()`, `fread()`, `fwrite()`, `fseek()` |
| **인터페이스** | 파일 디스크립터(`int fd`) 사용 | 파일 포인터(`FILE* stream`) 사용 |
| **버퍼링** | **사용자 수준 버퍼 없음** (커널 버퍼만 존재) | **사용자 수준 버퍼 존재** (I/O 성능 향상) |
| **이식성 (Portability)** | UNIX/Linux 계열에 종속적 | 표준 C 라이브러리(ANSI C)로 이식성 높음 |
| **세밀한 제어** | 권한 비트, O_NONBLOCK 등 세밀한 제어 가능 | 포맷팅(sprintf 등)과 버퍼링 자동 관리 |

#### 2. 데이터베이스 및 네트워크와의 융합 (OS & DB & Network)
-   **DBMS와의 시너지 (Buffer Management)**: DBMS는 OS의 파일 시스템을 신뢁하지 않고(이중 캐싱 방지), 직접 **O_DIRECT** 플래그를 사용하여 디스크 I/O를 수행하거나 자신만의 **버퍼 풀(Buffer Pool)**을 관리한다. 이는 파일 연산의 '캐싱 메커니즘'을 DB가 직접 최적화하는 사례다.
-   **네트워크와의 융합 (Socket as File)**: UNIX 철학(**"모든 것은 파일이다"**)에 따라, **소켓(Socket)**과 **파이프(Pipe)** 역시 파일 디스크립터로 관리된다. 따라서 `read()`, `write()` 연산이 로컬 파일과 네트워크 패킷 송수신에 동일하게 사용된다.

#### 3. 성능 메트릭 (Performance Metrics)
-   **Latency (지연 시간)**: `open()` 시스템 콜은 파일을 열 때마다 디렉터리 검색과 Inode 로드가 필요하므로 무겁다. 따라서 한 번 열고 여러 번 읽기/쓰기를 수행해야 한다.
-   **Throughput (처리량)**: `write()` 시 시스템 콜 오버헤드(Context Switching)가 크므로, 작은 데이터