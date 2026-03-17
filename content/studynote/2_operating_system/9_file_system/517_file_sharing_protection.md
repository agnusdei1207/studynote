+++
title = "517. 파일 공유 (File Sharing)와 보호"
date = "2026-03-14"
weight = 517
+++

# 517. 파일 공유 (File Sharing)와 보호

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중 사용자 환경에서 데이터의 협업 가능성을 극대화하되, **DAC (Discretionary Access Control)** 및 **ACL (Access Control List)** 메커니즘을 통해 자원의 무결성과 기밀성을 보장하는 운영체제의 핵심 자원 관리 기법이다.
> 2. **가치**: 시스템 자원의 공유를 통해 업무 효율을 향상시키되, **UID (User ID)** 및 **GID (Group ID)** 기반의 격리성을 확보함으로써 데이터 유출 파급력을 최소화하고 감사 추적성(Auditing)을 확보한다.
> 3. **융합**: 분산 시스템 환경으로 확장될 때 네트워크 파일 시스템(NFS, SMB)과 연동되며, 이때 **일관성 모델(Consistency Model)**의 선택(강력한 일관성 vs 결과적 일관성)이 시스템의 성능과 신뢰도를 결정하는 중요한 변수가 된다.

---

### Ⅰ. 개요 (Context & Background)

파일 공유와 보호는 시분할(Time-Sharing) 시스템 및 다중 사용자(Multi-User) 운영체제 환경에서 필수적인 기능이다. 단순히 파일을 여러 사람이 복사하여 사용하는 것이 아니라, **동일한 데이터副本(Inode)**을 여러 프로세스나 사용자가 동시에 참조하거나 수정할 수 있게 하는 메커니즘이다. 이 과정에서 핵심은 "누가(Who)", "무엇을(What)", "어떻게(How)" 접근하는지를 제어하는 **보호(Protection)** 시스템이다.

기술적 배경을 살펴보면, 초기 배치(Batch) 처리 시스템에서는 자원 독점이 가능했으나, 시스템이 거대해지고 네트워크로 연결되면서 **파일 소유자(Owner)**와 **타 사용자(Others)** 간의 권한 충돌이 발생했다. 이를 해결하기 위해 **UNIX permission 비트 체계(rwx)**가 탄생했으며, 더욱 정교한 제어를 위해 **ACL (Access Control List)**이 도입되었다. 또한, 단일 시스템을 넘어 분산 환경으로 확장됨에 따라 네트워크 상에서의 파일 공유 트래픽과 보안 문제(예: **Kerberos** 인증 등)가 새로운 과제로 대두되었다.

```text
 [ Evolution of File Access ]
 ┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
 │  Isolated System  │ ───▶ │  Time-Sharing     │ ───▶ │  Distributed Sys. │
 │  (Single User)    │      │  (Multi-User)     │      │  (Network FS)     │
 └───────────────────┘      └───────────────────┘      └───────────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
   Physical Access            UID/GID Controls          Encryption / Protocols
   (Lock & Key)               (DAC/ACL)                 (NFS/SMB/AFP)
```

#### 개념 상세 분석
1.  **사용자 식별 (Identification)**: 시스템은 각 사용자를 고유한 **UID (User ID)**로 식별하며, 여러 사용자를 묶어 관리하기 위해 **GID (Group ID)**를 사용한다. 이는 커널(Kernel) 수준에서 프로세스의 자격(Credential)을 검증하는 기준이 된다.
2.  **접근 제어 (Access Control)**: 파일 시스템 객체(Inode)에 저장된 메타데이터를 바탕으로, **시스템 콜(System Call)** 요청 시 **CRUD (Create, Read, Update, Delete)** 연산의 허용 여부을 판단한다.

> 📢 **섹션 요약 비유**: 파일 공유와 보호 체계는 마치 "도서관의 공용 열람실과 개인 사물함"을 함께 운영하는 것과 같습니다. 누구나 들어와 책을 보고 공부할 수 있는 열린 공간(공유)이 있지만, 각자의 소중한 노트나 노트북을 보관하기 위해서는 본인 확인(ID)을 거쳐 잠금 해제(권한 해제)가 필요한 개인 공간(보호)이 반드시 필요한 원리입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

파일 공유와 보호를 구현하기 위해 운영체제는 **VFS (Virtual File System)** 계층과 파일 시스템 드라이버 사이에서 보안 검사를 수행한다.

#### 1. 핵심 구성 요소 및 동작 매커니즘
| 모듈 명칭 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **UID / GID** | 사용자/그룹 식별자 | 프로세스의 **PCB (Process Control Block)**에 저장되며, 시스템 콜 실행 시 커널에 전달됨. | 출입증 (사원증 / 팀 구분) |
| **Inode (Index Node)** | 파일 메타데이터 저장 | 소유자 UID, GID, **Mode Bit(rwx)**, 타임스탬프, 블록 주지를 포함하며, 권한 검사의 근거가 됨. | 도서관 카드 목록 |
| **Mode Bit (Permission)** | 기본 3단위 권한 제어 | **User(u)/Group(g)/Other(o)**에 대해 **Read(4)/Write(2)/Execute(1)**의 8진수 합산으로 설정. | 열람/대출/불가 태그 |
| **ACL (Access Control List)** | 정밀 권한 제어 (확장) | 특정 사용자/그룹별로 허가/거부 목록을 파일 메타데이터 내에 연결 리스트 형태로 저장. | VIP 회원 명부 |
| **System Call Interface** | 권한 검사 트리거 | `open()`, `chmod()`, `chown()` 등 호출 시, 커널 모드 전환 후 **RUID (Real UID)** vs **EUID (Effective UID)** 비교. | 매표소의 티켓 검사기 |

#### 2. 권한 검사 절차 및 아키텍처
파일에 접근을 요청하는 프로세스는 커널을 통해 검사를 받는다. 이때 **DAC (Discretionary Access Control)** 모델을 사용하여, 소유자가 재량대로 권한을 부여한다.

```text
 [ Process Context ]              [ Kernel VFS Layer ]            [ Disk Storage ]
 ┌──────────────────┐             ┌──────────────────────┐         ┌──────────────────┐
 │ Request: Read    │             │ 1. Resolve Path      │         │ ┌──────────────┐ │
 │ "report.txt"     │────────────▶│    (Get Inode #)     │─────────▶│ │ Inode #10523 │ │
 │                  │             │                      │         │ │ Owner: 1001  │ │
 │ Credentials:     │             │ 2. Check Permission  │         │ │ Group: 500   │ │
 │ RUID: 1002       │             │    (i_mode & rwx)    │◀────────│ │ Perm: 640    │ │
 │ GIDs: [500, 501] │             │                      │         │ └──────────────┘ │
 └──────────────────┘             │ 3. Grant/Deny        │         └──────────────────┘
                                 └──────────────────────┘
                                          │
                         ▼ Permission Logic (Pseudo-code) ▼
                         if (uid == inode.i_uid) {
                             mask = inode.mode >> 6; // Owner bits
                         } else if (in_group(gid, inode.i_gid)) {
                             mask = inode.mode >> 3; // Group bits
                         } else {
                             mask = inode.mode;      // Other bits
                         }
                         if ((mask & requested_bit) == 0) {
                             return EACCES; // Error: Access Denied
                         }
```

**해설**:
1.  **Path Resolution**: 파일 시스템 트리를 순회하며 최종 파일의 **Inode**를 메모리로 로드한다.
2.  **Permission Check**: 현재 프로세스의 UID가 파일 소유자인지, 또는 GID가 그룹에 속하는지 확인한다.
3.  **Bitwise Operation**: 요청한 연산(읽기/쓰기/실행)의 비트가 Inode에 설정된 권한 비트와 **AND(&)** 연산 결과가 0이 아니면 접근을 허용한다. 0이면 `EACCES` 에러를 반환한다.

#### 3. 공유 메모리 매핑 (Memory Mapped File)
파일 공유의 또 다른 형태는 `mmap()` 시스템 콜을 이용한 **메모리 맵드 파일(Memory-Mapped File)**이다. 이는 파일 내용을 가상 메모리 주소 공간에 직접 매핑하여, 파일 I/O를 `read()/write()`가 아닌 메모리 포인터 조작으로 수행하게 한다.

```c
/* Code Snippet: Memory Mapped File Sharing */
#include <sys/mman.h>
#include <fcntl.h>

int fd = open("shared_data.bin", O_RDWR); // 1. Open File
void *addr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, 
                  MAP_SHARED, fd, 0);      // 2. Map to Virtual Memory
                  // MAP_SHARED: Changes are visible to other processes instantly.
if (addr == MAP_FAILED) {
    perror("mmap failed");
}
// Access file like memory
sprintf((char*)addr, "Hello Shared World"); 
msync(addr, 4096, MS_SYNC);                 // 3. Sync changes to Disk
munmap(addr, 4096);                         // 4. Unmap
```

**핵심 포인트**: `MAP_SHARED` 플래그를 사용하면, 여러 프로세스가 동일한 파일을 메모리에 매핑했을 때 한 프로세스의 변경 내용이 다른 프로세스의 메모리 영역에도 즉시 반영된다(운영체제에 따라 페이지 폴트 처리 로직이 다름).

> 📢 **섹션 요약 비유**: 아키텍처와 원리는 "고급 보증금 창고"와 같습니다. 손님(프로세스)이 물건(파일)을 찾으려면 먼저 사무실 컴퓨터(Inode)에 예약된 권한(키)이 있는지 확인하고, 열쇠가 맞으면 실제 창고(디스크 블록)에 접근하게 해줍니다. 혹은 쇼윈도처럼 앞쪽 유리창(메모리 맵)에 물건을 보여두어 실제 문을 열지 않고도 내용을 확인하거나 수정하는 방식도 제공합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

파일 공유와 보호는 단순한 운영체제 기능을 넘어 데이터베이스, 네트워크 보안, 분산 시스템과 깊게 연관되어 있다.

#### 1. 일관성 시맨틱 (Consistency Semantics) 심층 비교
파일이 여러 사용자에 의해 공유될 때, "A의 변경 사항이 B에게 언제 보이는가?"에 대한 모델은 분산 시스템 설계의 핵심이다.

| 구분 | **Unix Semantics** (유닉스 시맨틱) | **Session Semantics** (세션 시맨틱) | **Immutable-Shared File** (불변 공유) |
|:---|:---|:---|:---|
| **정의** | 모든 쓰기 연산은 즉시 파일에 반영되며, 모든 사용자에게 즉시 가시된다. | 파일이 열려 있는 동안의 변경은 로컬에만 존재하며, 파일을 닫을(Close) 때 서버에 일괄 반영된다. | 파일은 읽기 전용으로만 공유되며, 수정 시 새로운 버전의 파일을 생성한다. |
| **가시성** | 강력한 일관성 (Strong Consistency). | 최종 쓰기 승리 (Write-on-close). | 버전 관리 형태. |
| **성능** | 디스크 I/O가 빈번하여 동시성 경합(Race Condition) 발생 가능. | 네트워크 트래픽을 Close 시점으로 모아 효율적이나, 충돌(Modify Conflict) 해결 복잡. | 동시성 제어가 매우 단순하여 병렬 읽기 성수 극대화. |
| **주요 사용처** | 로컬 파일 시스템 (NFSv4 등에서도 지원 시도). | SMB/CIFS (Windows), AFS (Andrew File System). | 소프트웨어 배포, CDN (Content Delivery Network). |

#### 2. 타 영역(과목) 융합 분석

**① 데이터베이스 (Database)와의 시너지: ACID vs 파일 시스템**
- **공통점**: 동시성 제어(Concurrency Control)가 필요함. 파일 시스템의 `flock()`은 DB의 **Lock Manager**와 유사하게 동작.
- **차이점**: DB는 **ACID (Atomicity, Consistency, Isolation, Durability)** 특성을 보장하기 위해 **WAL (Write-Ahead Logging)**과 같은 견고한 트랜잭션 로깅을 사용하지만, 일반 파일 시스템은 메타데이터(`ext4`의 **Journaling**)만 보장하고 사용자 데이터까지 완벽히 보장하지 않는 경우가 많음.
- **실무적 함의**: 금융 거래와 같이 데이터 무결성이 중요한 경우, 파일 시스템 위에 DB를 구축하여 파일의 단점을 보완해야 함.

**② 보안 (Security) 및 네트워크와의 융합: 암호화와 인증**
- **링크**: 로컬의 `rwx` 비트는 해커가 시스템 루트(Root) 권한을 탈취하면 무의미해짐. 따라서 **FDE (Full Disk Encryption)** 또는 네트워크 전송 시 **TLS/SSL** 암호화가 필수적임.
- **융합 솔루션**: 현대의 파일 공유는 **NFSv4**나 **SMB3** 프로토콜을 사용하여, **Kerberos** 티켓 기반 인증과 **AES (Advanced Encryption Standard)** 암호화를 조합하여 전송 구간 보안을 확보함.

> 📢 **섹션 요약 비유**: 파일 공유의 일관성 모델은 "협업 문서 편집 방식"과 같습니다. **유닉스 시맨틱**은 '구글 문서(Google Docs)'처럼 글자 하나를 칠 때마다 모든 참여자 화면에 실시간으로 뜨는 방식이고, **세션 시맨틱**은 각자 덮어쓴 뒤 '저장'을 누르는 순간에만 서버로 전송되는 **MS 워드(오프라인 모드)** 같은 방식입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 시스템에서 파일 공유 및 보안 정책을 수립할 때는 보안 강도와 사용 편의성, 그리고 시스템 성능 사이의 트레이드오프를 분석해야 한다.

#### 1. 실무 시나리오별 의사결정

**상황 A: 리눅스 웹 서버 (Web Server) 다중 호스팅**
- **문제**: `apache