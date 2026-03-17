+++
title = "519. 가상 파일 시스템 (VFS, Virtual File System) 계층"
date = "2026-03-14"
weight = 519
+++

# 519. 가상 파일 시스템 (VFS, Virtual File System) 계층

## # 핵심 인사이트 (3줄 요약)
> 1. **본질**: VFS (Virtual File System)는 이기종 파일 시스템(EXT4, NTFS, NFS 등)의 구현적 차이를 **은폐(Capsulation)**하고, 상위 계층에 `POSIX (Portable Operating System Interface)` 표준 인터페이스를 제공하는 커널 내부의 **추상화 미들웨어(Abstraction Middleware)**이다.
> 2. **가치**: 애플리케이션은 저장 매체의 물리적 특성(로컬 디스크, 네트워크, 메모리)을 고려하지 않고 표준화된 **시스템 콜(System Call)**만으로 데이터 입출력을 수행하므로, 코드 수정 없는 스토리지 교체가 가능하여 **이식성(Portability)**과 **확장성(Extensibility)**이 극대화된다.
> 3. **구조**: C 언어 기반 커널에서 **함수 포인터(Function Pointer)**와 구조체를 활용하여 객체 지향의 **다형성(Polymorphism)**을 에뮬레이션하며, `dentry` 캐시와 `Page Cache`를 통해 '커널 모드 전환 비용'과 '디스크 I/O'를 최소화하는 고성능 아키텍처를 구현한다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
가상 파일 시스템 (VFS, Virtual File System)은 유닉스(UNIX) 및 리눅스(Linux) 커널의 핵심 서브시스템으로, 물리적·논리적으로 상이한 다양한 파일 시스템이 존재하더라도 응용 프로그램(Application)이 이를 **통일된 방식(Uniform Interface)**으로 접근할 수 있도록 지원하는 소프트웨어 계층이다. 이는 하드웨어의 복잡성을 숨기는 운영체제의 기본 철학을 파일 시스템 영역으로 확장한 것으로, 소프트웨어 공학의 **브리지 패턴(Bridge Pattern)**을 운영체제 커널에 구현한 대표적인 사례이다.

**2. 등장 배경 및 필연성**
초기 운영체제는 단일 파일 시스템(예: System V FS)만을 지원하여 성능을 최우선으로 했다. 그러나 네트워크 기술 발달, 마이크로소프트(Microsoft) 윈도우(Windows)와의 상호 운용성 필요성, 그리고 클라우드(Cloud) 환경의 등장으로 운영체제 내부에서 수십 가지의 서로 다른 파일 시스템(로컬 디스크, 네트워크 스토리지, 가상 파일 시스템 등)을 동시에 마운트(Mount)하여 사용해야 하는 **이기종 통합(Heterogeneous Integration)** 환경이 도래했다. 매번 새로운 스토리지마다 애플리케이션을 재작성하는 것은 비효율적이므로, 커널 차원에서 이를 중재하고 API를 표준화할 수 있는 **인터페이스 계층의 도입**이 필연적으로 요구되었다.

**3. 작동 철학: "모든 것은 파일이다"**
VFS는 유닉스 철학인 **"모든 것은 파일이다(Everything is a File)"**를 실현하는 엔진이다. 일반 파일, 디렉터리, 블록 디바이스, 소켓(Socket), 파이프(Pipe), 심지어 프로세스 정보까지도 동일한 `open()`, `read()`, `write()`, `close()` 인터페이스로 다루게 한다. VFS는 사용자 공간(User Space)의 요청이 들어오면, 요청의 대상이 어떤 파일 시스템에 속하는지 식별하여, 해당 실제 파일 시스템(Actual Filesystem)의 구체적인 드라이버 함수로 요청을 **라우팅(Routing)**하는 **스위칭 로직(Switching Logic)**을 수행한다.

> **📢 섹션 요약 비유**: VFS는 "만능 통번역기가 장착된 국제 회의 센터"와 같습니다. 참가자들이 한국어(EXT4), 영어(NFS), 불어(FAT32)를 사용하든 상관없이, 발언자(애플리케이션)는 마이크에 대고 말만 하면(표준 API 호출), 통역사(VFS)가 상대방의 언어(물리 스토리지 프로토콜)로 번역하여 전달합니다. 참가자들은 서로의 언어를 배울 필요가 없습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. VFS 4대 핵심 객체 구조**
VFS는 객체 지향 언어가 아닌 C 언어로 작성되었지만, 구조체와 함수 포인터 배열을 활용하여 완벽한 **객체 지향 패턴(Object-Oriented Pattern)**을 구현한다. 각 객체는 파일 시스템의 특정 요소를 추상화하며, 커널 메모리 상에서 유기적으로 연결된다.

| 객체 (Object) | 전체 명칭 (Abbreviation) | 역할 및 내부 동작 | 주요 필드 및 함수 포인터 |
|:---|:---|:---|:---|
| **Superblock** | Superblock (파일 시스템 헤더) | 마운트된 파일 시스템 전체의 메타데이터 관리.<br>전체 블록 수, Inode 테이블 위치, 파일 시스템 타입 정보 포함.<br>파일 시스템의 '생명 주기' 관리. | `s_type`, `s_op` (super_operations)<br>함수: `read_inode()`, `write_inode()`, `statfs()` |
| **Inode** | Index Node (파일 노드) | 파일의 고유 번호와 권한, 크기, 데이터 블록 위치 등 속성 관리.<br>파일의 **이름(Name)**은 포함하지 않음. | `i_mode`, `i_sb`, `i_op`, `i_fop`<br>함수: `truncate()`, `setattr()`, `permission()` |
| **Dentry** | Directory Entry (경로 캐시) | 파일의 전체 경로(Path)와 실제 Inode를 매핑하는 캐싱 엔트리.<br>파일 시스템 트리 구조의 탐색 속도를 결정함.<br>계층 구조(Hierarchy) 표현. | `d_parent`, `d_inode`, `d_hash`<br>상태: `DCACHE_XXX` 플래그 |
| **File** | File Object (열린 파일 컨텍스트) | 프로세스가 파일을 열었을 때 생성되는 인스턴스.<br>현재 읽기/쓰기 포인터(Offset)와 접근 모드(R/W) 저장.<br>프로세스별 독립적인 접근 관점 제공. | `f_pos`, `f_op`, `f_dentry`<br>함수: `llseek()`, `read()`, `write()`, `mmap()` |

**2. VFS 아키텍처 다이어그램**
다음은 사용자 프로세스의 `read()` 시스템 콜이 VFS를 거쳐 물리 디스크에 도달하는 계층별 흐름을 도식화한 것이다. VFS는 상위의 표준 인터페이스와 하위의 구체적 구현 사이에서 다리(Bridge) 역할을 수행한다.

```text
┌─────────────────────────────────────────────────────────────────┐
│ [ User Space : Application Layer ]                             │
│  Process (fd: 3)                                                │
└───────────────────────────────┬─────────────────────────────────┘
                                │ 1. read(3, buf, 1024)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ [ System Call Interface (Kernel Entry Point) ]                 │
│  sys_read()  →  vfs_read()                                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ [ VFS Layer (Virtual File System) ]                            │
│  ① File Descriptor → file struct 조회 (fdarray[])              │
│  ② 권한 검증 (security_file_permission)                        │
│  ③ 다형성 호출: file->f_op->read()                             │
│     (만약 EXT4 파일이라면, ext4_file_read이 등록되어 있음)      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ [ VFS Cache Management Layer ]                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │ Dentry Cache   │  │ Inode Cache    │  │ Page Cache     │   │
│  │ (Path Lookup)  │  │ (Metadata)     │  │ (File Data)    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│     ▲ Hit?             ▲ Hit?               ▲ Hit?             │
└────┼───────────────────┼───────────────────┼───────────────────┘
     │ Miss             │ Miss               │ Miss
     │                  │                    │
     ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ [ Physical Filesystem Implementation ]                         │
│  (e.g., EXT4, XFS, NFS, FAT32)                                 │
│                                                                 │
│  [EXT4 Example]                                                │
│   • ext4_file_read()                                           │
│   • ext4_map_blocks()  (논리 블록 → 물리 블록 매핑)           │
│   • Journaling Transaction (로그 트랜잭션 시작)                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ [ Block I/O Layer & Device Driver ]                            │
│  Generic Block Layer → IO Scheduler → Device Driver (AHCI/SAS) │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ [ Hardware Storage ]                                           │
│  HDD / SSD / NVMe / Network Storage                            │
└─────────────────────────────────────────────────────────────────┘
```

**3. 다형성(Polymorphism)의 구현 원리: 함수 포인터**
VFS의 핵심은 `file_operations`와 `inode_operations` 구조체에 있다. 각 파일 시스템은 자신만의 동작 방식을 정의한 함수 포인터 테이블을 VFS에 등록(register_filesystem)한다. VFS는 이 테이블을 통해 실제 코드를 실행 시점에 바인딩하는 **동적 디스패치(Dynamic Dispatch)**를 수행한다.

```c
// 리눅스 커널 소스 기반 예시 (개념적 구조)

// 1. VFS 공용 인터페이스 정의 (include/linux/fs.h)
struct file_operations {
    loff_t (*llseek) (struct file *, loff_t, int);
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
    // ...
};

// 2. EXT4 파일 시스템의 구체적 구현 등록
const struct file_operations ext4_file_operations = {
    .llseek  = generic_file_llseek,
    .read    = new_sync_read,       // EXT4 전용 읽기 로직 (저널링 체크 등 포함)
    .write   = ext4_file_write_iter,// EXT4 전용 쓰기 로직 (디렉터리 엔트리 갱신 등)
    .mmap    = ext4_file_mmap,
};

// 3. 네트워크 파일 시스템(NFS)의 구체적 구현 등록
const struct file_operations nfs_file_operations = {
    .llseek  = nfs_file_llseek,
    .read    = nfs_file_read,        // NFS 전용 읽기 로직 (RPC 요청 생성)
    .write   = nfs_file_write,       // NFS 전용 쓰기 로직 (서버 동기화)
};

// 4. VFS의 런타임 동작
ssize_t vfs_read(struct file *file, char __user *buf, size_t count, loff_t *pos)
{
    // file 객체 내부에 등록된 함수 포인터(f_op->read)를 호출
    // 실제 실행되는 함수는 file이 가리키는 파일 시스템 종류에 따라 다름
    if (file->f_op->read)
        return file->f_op->read(file, buf, count, pos);
    // ...
}
```

> **📢 섹션 요약 비유**: VFS는 "자동 변속기(Transmission)가 장착된 자동차"와 같습니다. 운전자(사용자 프로세스)는 악셀과 브레이크(표준 API)만 조작하면 됩니다. 자동차의 내부 기계가 가솔린 엔진(EXT4)인지, 전기 모터(NFS)인지, 혹은 수동 변속기(FAT)인지는 상관없이, 변속기(VFS)가 운전 의도를 각 엔진에 맞는 기계적 신호(함수 포인터)로 변환하여 바퀴를 돌려줍니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 파일 시스템 간 기술적 차이 분석**
VFS 아래에 존재하는 다양한 파일 시스템들은 VFS를 통해 비로소 하나의 시스템 내에서 융합될 수 있다. VFS는 이들의 **저장 매체 성격**, **데이터 무결성 전략**, **지연 시간(Latency)**의 근본적인 차이를 어떻게 추상화하는가?

| 구분 | EXT4 (Extended File System 4) | NFS (Network File System) | VFS의 추상화 및 융합 역할 |
|:---|:---|:---|:---|
| **저장소 매체** | 로컬 HDD/SSD (Block Device) | 원격 서버 (Network Socket) | `struct file` 내 `f_mapping`을 통해 로컬 `address_space`와 네트워크 `rpc_ops`를 분기 처리 |
| **데이터 접근 단위** | 블록 (Block, 4KB) | 파일/메타데이터 (Protocol) | VFS `read()` 시스템 콜 내부에서 로컬은 `__bread()` 호출, 네트워크는 `nfs_read_rpc()` 호출로 자동 분기 |
| **지연 시간 (Latency)** | 저지연 (µs~ms 단위) | 고지연 (ms~수십 ms, RTT dependent) | `O_NONBLOCK` 플래그 처리 로직을 파일 시스템별로 위임하여 블로킹/논블로킹 투명성 제공 |
| **동시성 제어** | 락 (Lock), Journaling | 파일 잠금 (File Locking), RPC Sequence | `file_lock` 구조체를 통해 POSIX 레코드 락을 통합 관리하되, 실제 잠금 구현은 각 FS에게 위임 |

**2. 융합 시너지: IPC(프로세스 간 통신)와의 완벽한 통합**
VFS의 가장 강력한 융합 사례는 로컬 파일뿐만 아니라 **소켓(Socket)**이나 **파이프(Pipe)**와 같은 IPC 통신 수단까지도 동일한 인터페이스로 관리한다는 점이다. `socket