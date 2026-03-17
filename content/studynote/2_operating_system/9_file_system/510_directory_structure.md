+++
title = "510. 디렉터리 (Directory) 논리적 구조"
date = "2026-03-14"
weight = 510
+++

# 510. 디렉터리 (Directory) 논리적 구조

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디렉터리(Directory)는 파일 시스템(File System)의 **'논리적 네비게이션 계층(Layer of Navigation)'**으로서, 사용자가 인식하는 추상적인 파일명(Symbolic File Name)을 물리적인 저장소 내의 블록 번호나 inode(Index Node)로 매핑하는 핵심 메타데이터 저장소이다.
> 2. **가치**: 단일 평면 구조의 한계를 넘어 계층적 트리(Hierarchical Tree) 및 비순환 그래프(Acyclic Graph) 구조를 통해 파일의 논리적 분류, 접근 권한 격리, 이름 중복 해결을 가능하게 하며, 이를 통해 스토리지 관리 효율성을 극대화하고 탐색 복잡도를 $O(N)$에서 $O(\log N)$ 수준으로 최적화한다.
> 3. **융합**: VFS (Virtual File System) 계층에서 추상화되어 EXT4, NTFS, FAT 등 이기종 파일 시스템의 네임스페이스(Namespace)를 통합 관리하며, 프로세스의 파일 접근 시스템 콜(System Call) 경로에서 핵심적인 인덱싱 역할을 수행한다.

---

### Ⅰ. 개요 (Context & Background)

**디렉터리(Directory)**는 파일 시스템의 핵심 구조로, 수많은 파일 정보(File Metadata)와 위치 정보를 체계적으로 관리하기 위한 **'특수한 목적의 파일'**이다. 단순히 파일 이름을 저장하는 컨테이너를 넘어, 파일 시스템의 전체적인 위상(Topology)을 정의하고 사용자에게 투명한 네임스페이스를 제공하는 데이터베이스 역할을 수행한다.

초기의 일반용 운영체제(예: CP/M, 초기 MS-DOS)에서는 시스템 전체의 파일이 하나의 리스트에 존재하는 **단일 레벨 디렉터리(Single-level Directory)**를 사용했다. 그러나 다중 사용자(Multi-user) 환경과 대용량 저장 장치(HDD, SSD)의 등장으로 파일 수가 폭발적으로 증가하면서, 파일 분류와 관리가 필수적인 과제로 대두되었다. 이에 따라 MS-DOS의 파일 할당 테이블(FAT, File Allocation Table) 구조를 거쳐 유닉스(UNIX) 계열의 계층적 트리 구조로 발전했다. 현대의 디렉터리는 단순한 텍스트 라인 리스트가 아니라, B-Tree나 Extent 기반의 고성능 인덱싱 구조를 가진 복잡한 데이터베이스 형태로 구현되어 수백만 개의 파일을 밀리초 단위로 탐색한다.

#### 💡 비유 (Analogy)
디렉터리는 거대한 도시의 **'지하철 노선도 및 역명표'**와 같다. 승객(사용자/프로세스)은 복잡한 선로의 배선(물리적 섹터/블록)이나 신호 시스템을 알 필요 없이, 역 이름(파일명)과 노선(경로)만 확인하면 원하는 위치로 즉시 이동할 수 있다. 또한, 역이 노선별로 분류되어 있는 것처럼 디렉터리는 파일을 체계적으로 정리한다.

#### 📢 섹션 요약 비유
마치 도서관이 수만 권의 책을 아무렇게나 쌓아두는 것이 아니라, **'분류 번호 시스템(예: 듀이십진법)'**을 도입하여 주제별로 분류하고, 원하는 책의 위치를 즉시 찾아낼 수 있게 하는 인덱스 사서와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

디렉터리의 아키텍처는 파일 시스템의 성능과 직결된다. 탐색 속도, 명명 규칙(Naming Convention), 그리고 공유 유연성에 따라 구조가 진화해왔으며, 내부적으로는 메타데이터와 포인터의 집합체로 구성된다.

#### 1. 핵심 구성 요소 (Components)

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **FCB (File Control Block)** | 파일 제어 블록 | 파일명, 위치(블록 번호), 크기, 생성 시간, 권한 비트 등을 포함하는 디렉터리 엔트리의 실질적 데이터 본체 | 사람의 주민등록등본 |
| **inode (Index Node)** | 인덱스 노드 | 유닉스 계열에서 파일 이름을 제외한 속성 정보와 데이터 블록 포인터 배열을 저장. 디렉터리 엔트리는 `파일명 + inode 번호`의 쌍(Pair)으로 구성됨 | 집의 주소지 번호(우편번호) |
| **Pathname Resolver** | 경로 분석기 | `/`, `.`, `..` 등의 구분자(Delimiter)를 파싱하여 루트부터 현재 디렉터리까지 트리를 순회(Traverse)하는 커널 모듈 | 내비게이션 경로 안내 |
| **dentry Cache** | 디렉터리 엔트리 캐시 | 최근 접근한 디렉터리의 경로 분석 결과를 메인 메모리(RAM)에 상주시켜 디스크 I/O를 제거하여 성능 향상 | 자주 쓰는 번호 즉시dialing |

#### 2. 논리적 구조의 진화 단계 (Evolution Stages)

파일 시스템의 요구사항 변화에 따라 디렉터리 구조는 다음과 같이 진화했다.

1.  **단일 레벨 디렉터리 (Single-level Directory)**:
    -   시스템 전체에 하나의 디렉터리만 존재.
    -   **장점**: 구현简单, 속도 빠름.
    -   **단점**: 파일명 중복 불가(Conflict), 다중 사용자 환경 부적합.

2.  **2단계 디렉터리 (Two-level Directory)**:
    -   각 사용자(User)별로 고유한 사용자 파일 디렉터리(UFD)를 가지고, 이를 관리하는 마스터 파일 디렉터리(MFD)를 둠.
    -   **구조**: `MFD -> [UserA(UFD), UserB(UFD)]`
    -   **단점**: 사용자 간 파일 공유 어려움, 사용자 자신의 파일 그룹핑 불가.

3.  **트리 구조 디렉터리 (Tree-structured Directory)**:
    -   현대 OS(Windows, Linux, macOS)의 표준 구조.
    -   하나의 루트(Root)를 시작으로 가지(Branch)와 잎(Leaf: 파일)으로 확장됨.
    -   **특징**: 로그 파일 시스템(Journaling File System)과 결합하여 무결성 제공.

#### 3. 아키텍처 다이어그램 (Tree Structure & Internal Flow)

아래 다이어그램은 논리적인 트리 구조와 이를 지탱하는 물리적인 inode 매커니즘을 함께 도식화한 것이다.

```text
[ Logical Directory Tree View ]         [ Physical Metadata Layer ]
                                         
[ Root Directory (/) ]                   
  |                                    
  +-- [ home ]  (inode: 12)              
       |                                 [ Inode Table (Disk) ]
       +-- [ userA ] (inode: 45)          | 12 | -> Block 200 (home's data)
            |                             | 45 | -> Block 500 (userA's data)
            +-- [ project ] (inode: 89)   | 89 | -> Block 800 (project's data)
                 |                         
                 +-- src.c (inode: 102)   [ Directory Entry (Block 800) ]
                                          | File Name | inode # |
                                          | "src.c"   |   102   | <-- Mapping
                                          | "data.txt"|   105   |
```

**[다이어그램 해설]**
사용자가 `/home/userA/project/src.c`를 요청하면, 파일 시스템 드라이버는 루트 디렉터리의 inode(보통 2번)를 읽는다. 루트의 데이터 블록에는 `home`이라는 이름과 inode 번호(12)가 저장되어 있다. 이어서 inode 12를 읽어 `userA`의 위치(inode 45)를 확인하고, 이 과정을 재귀적으로(Recursively) 반복하여 최종적으로 `src.c`의 데이터가 담긴 inode 102를 획득한다. 이때 각 단계에서 디스크 블록을 읽는 오버헤드를 줄이기 위해 리눅스 커널은 `dentry` 캐시를 활용한다.

#### 4. 심층 동작 원리 (Path Resolution Algorithm)

경로 이름(Pathname)을 실제 파일로 변환하는 과정은 토큰 파싱과 트리 탐색의 반복이다.

1.  **Parsing (파싱)**: 경로 문자열을 `/` 구분자를 기준으로 토큰으로 분리한다. (예: `["home", "userA", "project", "src.c"]`)
2.  **Traversing (순회)**: 현재 디렉터리의 데이터 블록을 로드하고, 하위 파일명 목록에서 다음 토큰(예: `home`)을 검색(Search)한다.
3.  **Indirection (간접 참조)**: 검색된 엔트리의 inode 번호를 통해 다음 inode 정보를 로드하고, 현재 작업 디렉터리(Current Working Directory)를 갱신한다.
4.  **Access (접근)**: 최종 토큰(파일명)에 도달하면 해당 inode의 권한 비트(Permission Bit)를 확인하고 파일을 연다.

#### 5. 핵심 알고리즘 (Path Resolution Pseudo-code)

```python
# Pseudo-code for Path Resolution in Kernel
def resolve_path(pathname_str):
    # 1. Initialize state
    current_inode = get_inode(ROOT_INODE_NUM) 
    components = split(pathname_str, '/') 
    
    for name in components:
        if not name: continue  # Handle root '/'

        # 2. Check permissions (Read access on directory)
        if not check_permission(current_inode, 'r'):
            raise PermissionError("Access Denied")

        # 3. Load directory data (Disk I/O)
        dir_data = read_directory_data(current_inode)

        # 4. Linear search or Hash lookup for entry
        target_entry = search_entry(dir_data, name)
        
        if target_entry is NULL:
            raise FileNotFoundError(f"'{name}' not found")
        
        # 5. Update context
        current_inode = target_entry.inode_ptr
        
    return current_inode # Returns final inode
```

#### 📢 섹션 요약 비유
마치 거대한 **'기업 조직도'**와 같습니다. CEO(루트) 밑에 팀장(서브 디렉터리)이 있고, 그 밑에 사원(파일)이 있는 구조로, 보고 계선을 따라가면 원하는 담당자를 정확히 찾을 수 있는 체계적인 계층 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

디렉터리 구조는 단순한 계층을 넘어 데이터 공유와 효율성을 위한 고급 형태로 발전했다. 특히 **비순환 그래프(Acyclic Graph)** 구조는 현대 OS의 핵심 기능인 파일 공유를 가능하게 한다.

#### 1. 심층 기술 비교표 (Directory Structure Comparison)

| 비교 항목 | Tree-Structured (Hierarchical) | Acyclic Graph (Shared) |
|:---|:---|:---|
| **구조 형태** | 부모 노드가 자식 노드를 가짐 (1:N) | 자식 노드가 여러 부모를 가질 수 있음 (N:N) |
| **탐색 복잡도** | 경로 길이 $H$에 대해 $O(H)$ | 순환 탐지 로직이 필요하여 상대적으로 높음 |
| **네이밍 (Naming)** | 경로에 따른 고유한 이름 | 다중 경로 허용 (Aliasing 현상 발생) |
| **파일 공유** | 복사(Copy)만 가능 (중복 저장) | Link(하드/소프트)를 통한 참조 공유 |
| **구현 메커니즘** | 단순 트리 | inode 참조 카운트(Reference Count) 또는 심볼릭 경로 |

#### 2. 고급 연결: 비순환 그래프 디렉터리 (Acyclic Graph Directory)

하나의 파일이나 하위 디렉터리가 여러 상위 디렉터리에 속할 수 있게 하는 구조이다.

-   **Aliasing**: 동일한 파일이 서로 다른 경로(이름)를 가질 수 있는 현상. 예: `/userA/report.txt`와 `/public/report.txt`가 같은 파일을 가리킴.
-   **Link의 구현 기법**:
    1.  **Hard Link (하드 링크)**:
        -   원본 파일의 **inode 번호를 직접 공유**.
        -   디렉터리 엔트리가 여러 개 존재하지만, 실제 데이터 블록은 하나.
        -   **Reference Counting**: 원본 inode의 링크 카운트를 증가시킴. 카운트가 0이 될 때만 데이터 삭제.
    2.  **Symbolic Link (심볼릭 링크 / Soft Link)**:
        -   원본 파일의 **경로명(Pathname)을 데이터로 가지는 특수 파일**.
        -   inode가 별도로 존재하며, 파일 타입이 'Link'로 표시됨.
        -   원본이 삭제되면 'Dangling Link'(끊어진 링크)가 됨.

#### 3. 과목 융합 관점 (OS, Network, DB)

-   **데이터베이스 (DB)**: 디렉터리의 트리 구조는 B-Tree 인덱싱 알고리즘과 밀접하다. 빠른 검색을 위해 디렉터리 엔트리를 정렬된 상태로 유지하거나 Hash Table을 사용하는 것은 DBMS의 인덱싱 전략과 동일하다.
-   **네트워크 (DNS)**: 도메인 네임 시스템(DNS)의 도메인 구조(`www.google.com`)는 파일 시스템의 트리 구조와 논리적으로 일치한다. 루트(.) 서버부터 최종 서브도메인까지 내려가는 분산 계층 구조는 디렉터리 탐색 메커니즘과 같다.

#### 4. 구조 비교 다이어그램 (Hard Link vs Symbolic Link)

```text
[ Scenario: Sharing 'shared_data.bin' ]

1. Hard Link Structure (Inode Sharing)
   -------------------------------------------------------
   | Dir A Entry      |                  | Dir B Entry    |
   | "my_link" --------+----->[ inode 50 ] <-------- "pub"|
   -------------------------------------------------------                    |
                        | (Data Blocks on Disk)                             |
                        +---> [ Block 100: "Actual Data" ]
                        |
                        +---> Ref Count: 2
                        
   => Both entries point to the SAME metadata(inode). 
   Faster, but cannot cross file systems.

2. Symbolic Link Structure (Path Pointer)
   -------------------------------------------------------
   | Dir A Entry      |                  | Dir B Entry    |
   | "my_link" --------+----->[ inode 88 ] <-------- "pub"|
   | (Link File