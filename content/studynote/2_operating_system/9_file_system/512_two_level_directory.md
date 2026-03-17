+++
title = "512. 2단계 디렉터리 (Two-level Directory) - MFD, UFD"
date = "2026-03-14"
weight = 512
+++

# 512. 2단계 디렉터리 (Two-level Directory) - MFD, UFD

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 2단계 디렉터리 (Two-level Directory)는 단일 계층의 한계를 돌파하기 위해 시스템 전체의 인덱스 역할을 하는 **MFD (Master File Directory)**와 개별 사용자의 파일을 관리하는 **UFD (User File Directory)**로 계층을 분리하여, 다중 사용자 **OS (Operating System)** 환경에서 **파일 이름 충돌 (Naming Collision)**을 논리적으로 격리하는 구조다.
> 2. **가치**: 사용자 간의 **격리성 (Isolation)**과 프라이버시를 기본적으로 보장하여 데이터 무결성을 확보하며, 검색 시 스캔해야 하는 엔트리 수를 $O(N)$에서 $O(M)+O(U)$로 획기적으로 줄여 접근 성능을 개선한다.
> 3. **융합**: 현대 운영체제의 **홈 디렉터리 (Home Directory)** 개념의 시초가 되며, **파일 시스템 (File System)**과 **보안 (Security)** 정책의 결합을 보여주는 핵심 아키텍처로서, 향후 **ACL (Access Control List)** 및 **파이썬(Python)** 등의 모듈 시스템 namespace 개념의 기반이 되었다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
2단계 디렉터리는 **SFD (Single-level Directory, 단일 계층 디렉터리)** 구조가 가진 사용자 간 파일 이름 중복 및 보안 문제를 해결하기 위해 제안된 파일 시스템 관리 기법이다. 이 구조에서는 물리적 저장 매체 전체를 관리하는 루트 디렉터리인 **MFD (Master File Directory)**와 각 사용자별로 할당된 **UFD (User File Directory)**의 2계층으로 파일 시스템을 논리적으로 분리한다.
파일 시스템의 **FCB (File Control Block, 파일 제어 블록)**나 **Inode (Index Node)**와 같은 메타데이터는 UFD 내부에 존재하며, 파일 접근 시에는 반드시 사용자 식별자를 통해 MFD를 거쳐 해당 UFD로 도달해야 하므로, 물리적인 디스크는 공유하되 논리적인 파일 공간은 완전히 분리된 효과를 낸다.

#### 2. 등장 배경 및 필요성 (Why Evolution Matters)
초기 컴퓨팅 환경인 일괄 처리(Batch Processing) 시스템에서는 한 명의 사용자가 시스템 전체를 독점하는 Mainframe 방식이었기에 단일 디렉터리로 충분했다. 그러나 1960년대 중반 이후, **MIT (Massachusetts Institute of Technology)**의 **CTSS (Compatible Time-Sharing System)**와 IBM의 **OS/360** 등장과 함께 **TSS (Time Sharing System, 시분할 시스템)**가 보편화되었다.
여러 사용자가 동시에 하나의 **CPU (Central Processing Unit)**와 디스크를 공유하는 환경에서는 'mail.txt'나 'test.c'와 같은 공통적인 파일 이름이 서로 덮어쓰는 치명적인 문제가 발생했다. 이를 해결하기 위해 사용자별로 독립된 파일 공간을 보장하는 2단계 구조가 도입되었으며, 이는 오늘날 리눅스/유닉스의 `/home` 구조로 정착되었다.

#### 3. 핵심 기술 용어 (Terminology)

| 약어 (Abbreviation) | 전체 명칭 (Full Name) | 정의 및 역할 |
|:---:|:---|:---|
| **MFD** | Master File Directory | 시스템의 최상위 루트에 존재하며, 등록된 모든 사용자의 계정명과 그에 해당하는 UFD의 물리적 주소(포인터)를 저장하는 인덱스 파일 |
| **UFD** | User File Directory | 개별 사용자가 소유한 파일의 메타데이터(파일명, 크기, 생성일, 접근 권한, 위치 등)를 관리하는 2차원적 하위 디렉터리 |
| **CWD** | Current Working Directory | 현재 프로세스가 작업 중인 활성화된 디렉터리 위치. 2단계 구조에서는 특정 사용자의 UFD가 이 역할을 수행 |
| **Pathname** | Path Name | 파일을 유일하게 식별하기 위한 문자열열로, 2단계 구조에서는 `[System]/[User]/[File]` 또는 `/User/File` 형식 사용 |

📢 **섹션 요약 비유**: 2단계 디렉터리는 거대한 "아파트 단지의 관리실과 각 세대"와 같습니다. 관리실(MFD)에는 101호, 102호 같은 세대명과 주민 명부만 있고, 실제 생활 물건들은 각자의 집(UFD) 안에 보관됩니다. 따라서 101호와 102호에 똑같은 'LG 냉장고'가 있어도 서로 다른 냉장고인 것처럼, 파일 이름 충돌을 자연스럽게 해결합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 (Internal Behavior) | 관련 프로토콜/구조 |
|:---|:---|:---|:---|
| **MFD (Root)** | 시스템 사용자 인덱싱 및 인증 | 시스템 부팅 시 메모리 혹은 고정 섹터에 로딩되며 `login` 시도 시 사용자명 탐색 수행 | Linear Search or Hash Table |
| **UFD (Leaf)** | 사용자 파일 메타데이터 관리 | 해당 사용자 로그인 시 **CWD (Current Working Directory)**로 설정되어 이후 파일 작업의 기준점이 됨 | Linked List or Array of FCBs |
| **FCB (File Control Block)** | 파일 속성 및 위치 정보 저장 | 디스크 할당 정보(블록 번호), 파일 크기, 생성 시간, 접근 권한(R/W/X) 비트 포함 | UNIX Inode 구조와 유사 |
| **Login Procedure** | 컨텍스트 스위칭 및 세션 설정 | ① MFD 탐색 → ② UFD 포인터 획득 → ③ 메모리에 UFD 로딩 → ④ 사용자 쉘 초기화 | System Call (`open`, `chdir`) |
| **File Descriptor** | 커널 내 파일 핸들 관리 | 프로세스별 파일 테이블에 엔트리를 추가하여 시스템 자원을 추적 | Kernel Object Management |

#### 2. 구조 및 데이터 흐름도 (ASCII Architecture)

다음은 **MFD**와 **UFD**를 통해 파일을 탐색하는 논리적 구조와 메모리/디스크 간의 데이터 흐름을 도식화한 것이다.

```text
+=======================================================================+
|                       LOGICAL FILE SYSTEM VIEW                        |
+=======================================================================+
|                                                                       |
|  [ Level 1: MFD (Master File Directory) ]                             |
|  +---------------------+---------------------+---------------------+  |
|  | User: "Alice"       | User: "Bob"         | User: "Charlie"     |  |
|  | UFD_Ptr: ----+      | UFD_Ptr: ------+    | UFD_Ptr: ------+    |  |
|  +--------------|------+-----------|---------+--------------|-----+  |
|                 |                  |                        |        |
|                 | (Pointer)        | (Pointer)              |        |
|                 ▼                  ▼                        ▼        |
|  [ Level 2: UFD (User File Directory) ]                            |
|  +---------------------+    +---------------------+    +---------------------+ |
|  | File: "Mail"        |    | File: "Mail"        |    | File: "data.bin"   | |
|  | Attr: -rw-r--r--    |    | Attr: -rw-------    |    | Attr: -rwxr-xr-x   | |
|  | Addr: 0x1024...     |    | Addr: 0x5021...     |    | Addr: 0x9011...     | |
|  +---------------------+    +---------------------+    +---------------------+ |
|  | File: "Test.c"      |    | File: "Test.c"      |    |                     | |
|  | Attr: -rwxr-xr-x    |    | Attr: -rw-------    |    |                     | |
|  | Addr: 0x2048...     |    | Addr: 0x3321...     |    |                     | |
|  +---------------------+    +---------------------+    +---------------------+ |
|                                                                       |
+=======================================================================+
         ▲                                    ▲
         |                                    |
    1. Search MFD for "Alice"           1. Search MFD for "Bob"
    2. Retrieve UFD Pointer             2. Retrieve UFD Pointer
    3. Set UFD as CWD (Current Dir)     3. Set UFD as CWD
    4. Search "Test.c" in CWD           4. Search "Test.c" in CWD
```

**[다이어그램 해설]**
이 다이어그램은 파일 경로 `/Alice/Test.c`를 처리하는 **File System**의 내부 메커니즘을 시각화한 것입니다.
1.  **사용자 인증 (MFD Lookup)**: 파일 시스템은 가장 먼저 최상위 루트에 있는 MFD를 스캔하여 "Alice"라는 문자열(사용자명)을 찾습니다. 이 과정은 사용자가 로그인하거나 파일 경로를 지정할 때 수행됩니다.
2.  **포인터 역참조 (Dereferencing)**: "Alice" 엔트리에는 그녀의 파일들이 모여 있는 UFD의 물리적 섹터 주소(Pointer)가 저장되어 있습니다. 시스템은 이 포인터를 통해 Level 2로 내려갑니다.
3.  **작업 디렉터리 설정 (CWD)**: Alice의 UFD가 메모리에 로드되며, 이제부터 시스템은 이 위치를 기준점(CWD)으로 삼습니다.
4.  **파일 검색 (File Lookup)**: Alice의 UFD 내부에서 "Test.c"를 검색합니다. Bob의 UFD에 있는 "Test.c"는 물리적 주소(0x3321)가 다르므로, 서로 전혀 다른 파일 객체로 취급됩니다.

#### 3. 핵심 동작 알고리즘 및 코드 (Pseudo-code)

2단계 디렉터리 구조에서의 파일 열기(Open) 연산은 다음과 같은 의사 코드(Pseudo-code)로 표현할 수 있으며, 이는 **OS Kernel**의 파일 시스템 드라이버 구현의 기초가 된다.

```c
// Function: Open File in Two-Level Directory Structure
// Input: username (string), filename (string)
// Output: File Pointer (Success) or Error Code (Failure)

FILE* two_level_open(char* username, char* filename) {
    // Phase 1: MFD 탐색 (사용자 검증)
    // 전역 MFD 리스트를 순회하거나 해싱하여 사용자 엔트리 검색
    // Time Complexity: O(M) where M is total users
    
    UFD* target_ufd = MFD.search(username); 
    
    if (target_ufd == NULL) {
        return ERROR_USER_NOT_FOUND; // 존재하지 않는 사용자
    }

    // Phase 2: UFD 탐색 (파일 검색)
    // 해당 사용자의 UFD 내부에서 파일명 검색
    // Time Complexity: O(U) where U is user's file count
    
    FCB* file_entry = target_ufd->search(filename); 
    
    if (file_entry == NULL) {
        return ERROR_FILE_NOT_FOUND; // 해당 파일 없음
    }

    // Phase 3: 접근 제어 확인 (Access Control)
    // 파일 소유자 또는 권한 비트(Read/Write/Execute) 체크
    // 현대 OS의 chmod/chown 시스템 콜의 기초 원리
    if (!check_permission(file_entry, current_user_process)) {
        return ERROR_PERMISSION_DENIED;
    }

    // Phase 4: 시스템 파일 테이블 등록 및 핸들 반환
    return load_file_to_memory(file_entry);
}
```

#### 4. 실무 수준의 고찰 (Performance & Storage)
실제 **DBMS (Database Management System)**나 대용량 **파일 서버** 설계 시, 2단계 구조는 간단한 인덱싱 전략을 제공하지만 한계가 명확하다. 사용자 수($M$)가 수만 명 이상으로 늘어날 경우, MFD를 선형 탐색(Linear Search)하는 것은 비효율적이다. 따라서 현대적인 시스템은 MFD 검색을 최적화하기 위해 **Hash Table**이나 **B-Tree (Balanced Tree)** 인덱스를 사용하여 로그인 및 파일 검색 지연 시간(Latency)을 최소화한다.

📢 **섹션 요약 비유**: 파일을 찾는 과정은 "부동산 등기소에서 등기부등본을 찾는 순서"와 같습니다. 먼저 '동(Users)' 번호로 건물 목록(MFD)을 찾고, 그 건물 내의 '호(File)' 번호로 실제 집 주소를 찾는 것입니다. 이 체계 덕분에 전국(전체 시스템)에 똑같은 이름의 집(파일)이 있어도 주소(Path)가 겹치지 않게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 분석표 (1-Level vs 2-Level vs Tree)

| 비교 항목 | 단일 계층 디렉터리 (1-Level) | 2단계 디렉터리 (2-Level) | 계층적 디렉터리 (Tree/Hierarchical) |
|:---|:---|:---|:---|
| **구조 (Structure)** | 모든 파일이 하나의 리스트에 존재 | MFD - UFD (고정된 깊이 2) | MFD - SubDirs - Files (가변 깊이) |
| **네이밍 (Naming)** | 전역적 유일성 요구 (Global Unique) | 사용자 내 유일성 (Local Unique) | 경로에 의한 유일성 (Path Unique) |
| **검색 복잡도 (Search)** | $O(T)$ (전체 파일 수 $T$ 스캔) | $O(M) + O(U)$ (사용자 + 파일) | $O(D \times B)$ (깊이 $D$ $\times$ 분기) |
| **프라이버시 (Privacy)** | None (모든 사용자가 전체 접근) | High (다른 사용자의 UFD 접근 차단) | Configurable (권한 설정에 따름) |
| **공유 (Sharing)** | 매우 쉬움 (모두가 같은 공간) | 매우 어려움 (논리적 격리됨) | 쉬움 (심볼릭 링크/공유 폴더) |
| **대표 예시** | MS-DOS (초기), 임베디드 OS | 초기 UNIX, IBM Mainframe | Modern Windows/macOS/Linux |

#### 2. 타 과목 융합 분석 (OS & Network & Security & DB)

**A. 보안 (Security) & 접근 제어**
2단계 구조는 **Access Control List (ACL, 접근 제어 목록)**의 가장 기초적인 형태를 제공한다. MFD에 사용자 ID가 있으므로, 시스템은 파일 소유권(Ownership)을 명확히 할 수 있다. 이