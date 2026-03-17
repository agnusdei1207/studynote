+++
title = "514. 비순환 그래프 디렉터리 (Acyclic-graph Directory) - 별칭(Aliasing) 및 하드 링크"
date = "2026-03-14"
weight = 514
+++

# [비순환 그래프 디렉터리 (Acyclic-graph Directory)]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파일 시스템의 계층 구조를 단순 트리(Tree)에서 방향성 비순환 그래프(DAG, Directed Acyclic Graph)로 확장하여, 물리적 데이터 중복 없이 논리적 공유를 구현하는 구조입니다.
> 2. **가치**: Aliasing(별칭) 및 Hard Link(하드 링크)를 통해 저장 공간 효율성을 극대화하고, Reference Count(참조 횟수) 기반的生命 관리로 데이터 일관성을 보장합니다.
> 3. **융합**: 운영체제(OS)의 VFS(Virtual File System)와 inode 구조를 기반으로, 데이터베이스의 MVCC(Multi-Version Concurrency Control)와 유사한 참조 관리 기법을 활용합니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
비순환 그래프 디렉터리(Acyclic-graph Directory)는 계층적 파일 시스템(Hierarchical File System)의 기본 형태인 트리 구조가 가진 '단일 부모(Single Parent)'라는 엄격한 제약을 극복한 구조입니다. 트리 구조에서는 하나의 파일이나 서브 디렉터리가 반드시 하나의 상위 디렉터리에만 속해야 하므로, 데이터 공유가 불가능합니다. 반면, DAG 구조에서는 **여러 개의 상위 디렉터리가 동일한 자식 노드(파일 또는 서브 디렉터리)를 가리킬 수 있습니다.** 이를 통해 데이터를 물리적으로 복사(Copy)하지 않고도 논리적 경로(Path)를 통해 다중 접근(Multi-access)을 허용하는 것이 핵심 철학입니다. 여기서 '비순환(Acyclic)'이라는 조건은 탐색 알고리즘이 무한 루프에 빠지는 것을 방지하고, 참조 횟수(Reference Count) 기반의 자동 메모리 해제를 가능하게 하는 결정적인 제약 조건입니다.

**2. 기술적 등장 배경 (Evolutionary Context)**
초기 파일 시스템은 단일 사용자 환경에서 단순하고 효율적이었습니다. 그러나 시분할 시스템(Time-sharing System) 및 다중 사용자 운영체제(Multi-user OS)가 도입되면서 다음과 같은 심각한 자원 낭비 및 무결성 문제가 대두되었습니다.

1.  **중복 저장의 낭비 (Redundancy)**: 여러 사용자나 프로젝트가 동일한 라이브러리(예: `libc.so`)나 대용량 문서를 사용할 때, 각자의 디렉터리에 파일을 복사하여 저장하면 디스크 공간(Storage)이 기하급수적으로 낭비됩니다.
2.  **데이터 불일치 (Consistency Issue)**: 원본 파일이 수정(Patching)되었을 때, 복사된 사본들 간의 내용 불일치(Inconsistency)가 발생하여 버전 관리가 악화되고 버그를 유발합니다.
3.  **소프트웨어 공유 필요성**: 시스템 전역에서 공통 유틸리티나 라이브러리를 효율적으로 공유하고 배포할 수 있는 메커니즘이 절실해졌습니다.

이를 해결하기 위해 유닉스(UNIX) 기반의 파일 시스템은 inode(Index Node) 기반의 링크(Link) 개념을 도입하여, **별칭(Aliasing)**을 통해 하나의 물리적 파일을 여러 이름으로 참조할 수 있는 DAG 구조를 채택했습니다.

**3. 아키텍처 도해 (트리 vs DAG 구조 비교)**

아래 다이어그램은 저장 공간 효율성과 구조적 차이를 시각적으로 보여줍니다.

```text
[Case A] Tree Structure (Single Parent)        [Case B] DAG Structure (Multiple Parents/Aliasing)

    [Root]                                         [Root]
     |                                             /    \
  [User]                                        [User1] [User2]
     |                                            |       |
  [Proj]                                      [ProjA] [ProjB]
     |                                               \     /          <-- Aliasing 발생 (공유)
  [Data]                                            \   /
                                                      \ /
                                                [Lib.so] (Physical Data Block #405)
                                                (Reference Count: 2)
```

*도해 심층 해설*:
- **[Case A] Tree 구조**: `Lib.so`가 필요하면 `ProjA`와 `ProjB` 각각의 디스크 공간에 복사해야 합니다. 저장 공간 낭비가 심하고, 원본을 수정하면 복사본과의 동기화가 불가능합니다.
- **[Case B] DAG 구조**: 물리적 데이터 블록(Block #405)은 오직 하나 존재하지만, 서로 다른 경로(`ProjA`와 `ProjB`)에서 이를 동시에 참조합니다. 이를 **Aliasing**이라 합니다. Reference Count가 2로 유지되어 어느 한쪽에서 파일을 삭제해도 다른 쪽의 접근이 유효함을 보장합니다.

**📢 섹션 요약 비유**:
비순환 그래프 디렉터리는 **"대형 쇼핑몰의 복합 출입구 시스템"**과 같습니다. 하나의 거대한 매장(데이터 블록)에 도달하기 위해, 지하철 역과 연결된 지하 통로와 호텔 1층 로비 등 서로 다른 입구(디렉터리 경로)가 존재할 수 있습니다. 어느 입구로 들어오든 결국 같은 매장에 도달하며, 출입구가 여러 개라고 해서 매장 자체가 여러 개 필요한 것은 아닙니다. 단, 내부에서 다시 입구로 나가면 안 되는 비순환 조건을 지킴으로써 길을 잃는 것을 방지합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 상세 분석 (Component Table)**

DAG 구조를 운영체제 차원에서 구현하기 위한 핵심 구성 요소는 다음과 같습니다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Mechanism) | 데이터 구조 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Inode (Index Node)** | 파일의 메타데이터 저장소 | 파일의 소유자, 권한, 크기, **데이터 블록 주소** 보유. **파일 이름은 inode에 없음**. | `struct inode` { uid, mode, size, block_ptr[], ... } | 주민등록등본 (고유 ID 보유) |
| **Dentry (Directory Entry)** | 파일 이름과 Inode의 연결 | 사용자가 인식하는 파일명(문자열)과 실제 데이터를 가리키는 inode 번호를 매핑. | `<Filename, Inode#>` Pair | 전화번호부 (이름 -> ID 검색) |
| **Hard Link (하드 링크)** | Inode에 대한 새로운 참조 경로 생성 | 기존 inode 번호를 가리키는 **새로운 Dentry**를 생성. **Reference Count 증가**. | Filesystem Layer Link | 호적에 올리는 이름 추가 |
| **Ref. Count (Link Count)** | 데이터 생존 여부 판단 | 해당 inode를 가리키는 Dentry(하드 링크)의 개수. `unlink()` 시 이 값이 0이 되어야만 데이터 블록 해제. | `Atomic Integer` | 대출 도서의 예약 인원 수 |
| **Symbolic Link (심볼릭 링크)** | 경로 정보를 저장하는 별도 파일 | 목표 파일의 **경로(Pathname)**를 데이터로 저장하는 특수 파일. inode는 독립적. | `char* pathname` | 목적지를 적은 포스트잇(쪽지) |

**2. 핵심 동작 메커니즘: Hard Link와 Aliasing**

**Aliasing**이란 하나의 물리적 객체(Object)에 대해 두 개 이상의 이름(Name)이 존재하는 상황을 의미합니다. 파일 시스템에서 이는 inode에 대한 다중 Dentry 매핑으로 구현됩니다.

```text
[Step 1] 링크 생성: ln /usr/bin/python3.9 /usr/local/bin/python
          -> 시스템은 /usr/local/bin/ 디렉터리에 새로운 엔트리 생성
          -> "python" 이름을 기존 Inode #12345와 매핑 (Mapping)

[Step 2] Reference Count 증가 (Atomic Operation)
          -> Inode #12345 내부 필드: nlink = 1 -> 2 변경

[Logical View]                      [Physical View (Disk Layout)]
/usr/bin/python3.9  ------>       [Inode #12345: Binary Data]
/usr/local/bin/python -->       [Block #201] [Block #202] ... (Shared)
                                    ^          ^
                                    |          |
                               (Dentry A)  (Dentry B)
```

*도해 심층 해설*:
- 논리적으로 `/usr/bin/python3.9`와 `/usr/local/bin/python`은 별개의 파일처럼 보입니다.
- 그러나 시스템 커널(Kernel) 입장에서 두 경로 모두 동일한 inode 번호(`#12345`)로 resolving(해석)됩니다.
- 디스크 상의 데이터 블록(#201, #202...)은 중복 없이 오직 한 번만 존재하며, 두 경로가 이를 공유합니다. 이로 인해 저장 공간이 절약됩니다.

**3. 핵심 알고리즘 및 소프트웨어적 판단 (파일 삭제 로직)**

파일 시스템에서 파일을 삭제(`unlink`)할 때, DAG 구조에서는 참조 횟수를 확인하여 데이터의 안전한 해제를 보장해야 합니다. 이는 OS의 Resource Management 핵심 로직입니다.

```c
// Pseudo-code for unlink(name) in DAG Structure
int unlink(char *filename) {
    // 1. 경로 이름 분석(Path Resolution)을 통해 inode 획득
    Inode *inode = resolve_path(current_dir, filename);
    if (inode == NULL) return -ERROR_NOT_FOUND;

    // 2. 쓰기 권한 검사 (Permission Check)
    if (!has_write_permission(inode->parent_dir)) return -ERROR_DENIED;

    // 3. [Critical Section] 참조 횟수(Link Count) 감소
    // 여러 프로세스가 동시에 삭제 시도할 수 있으므로 Atomic 연산 필수
    lock_inode(inode);
    inode->link_count--; 
    int is_last_link = (inode->link_count == 0);
    unlock_inode(inode);

    // 4. 데이터 제거 여부 결정 (DAG 핵심 로직)
    if (is_last_link) {
        // 참조하는 곳이 없으면 실제 데이터 블록 해제 (I/O 비용 발생)
        for (int i = 0; i < inode->block_count; i++) {
            free_block(inode->blocks[i]); // Bitmap/MAPFS 업데이트
        }
        free_inode(inode); // Inode 자체 해제
    } else {
        // 아직 다른 경로(Hard Link)에서 사용 중이므로 메타데이터만 업데이트
        // 데이터 블록은 보존됨
    }
    
    // 5. 현재 디렉터리 엔트리에서 이름 제거
    remove_dentry(current_dir, filename);
    return SUCCESS;
}
```

**수식적 모델**:
파일의 생명주기(Lifecycle)는 참조 횟수 $R$에 의해 결정됩니다.
$$ \text{State}(File) = \begin{cases} \text{Active} & \text{if } R > 0 \\ \text{Deleted} & \text{if } R = 0 \end{cases} $$
이 모델은 트리 구조의 단순 삭제와 달리, **"다른 사용자가 사용 중인 데이터를 함부로 삭제하지 않는다"**는 데이터 무결성 원칙을 수학적으로 보장합니다.

**📢 섹션 요약 비유**:
하드 링크와 별칭 시스템은 **"한 사람의 복수 호적(이중 국적)"**과 같습니다. 같은 사람(물리 데이터)이 직장에서는 '김대리'라 불리고, 동아리에서는 '김회장'이라 불릴 수 있습니다. '김대리'라는 직장 이름(링크)을 지운다고 해서 사람이 사라지는 것이 아니며(남은 호적 존재), 모든 호적(모든 링크)이 삭제되어야 비로소 사회적 기록(데이터)에서 완전히 말소됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: 트리 vs DAG vs 일반 그래프**

파일 시스템의 구조적 진화 과정과 각각의 트레이드오프(Trade-off)를 분석합니다.

| 구분 (Criteria) | 트리 구조 (Tree Structure) | 비순환 그래프 (DAG) | 일반 그래프 (General Graph) |
|:---|:---|:---|:---|
| **정의 (Definition)** | 노드가 단 하나의 부모만 가짐 | 노드가 다중 부모를 가질 수 있으나, **순환(Cycle) 허용 안 함** | 노드 간 임의의 연결 가능, 순환 허용 |
| **부모 노드 수** | $N_{parent} = 1$ (Fixed) | $N_{parent} \ge 1$ (Variable) | $N_{parent} \ge 0$ |
| **구현 복잡도** | 낮음 (Low) | 중간 (Medium - Ref Count 관리 필수) | 높음 (High - 순환 탐지 알고리즘 및 GC 필요) |
| **탐색 알고리즘 (Traversal)** | DFS/BFS 가능, 무한 루프 없음 | 방문 확인(Visited Check) 불필요 (순환 없음) | **반드시 Visited Set 필요** (무한 루프 방지) |
| **공유 효율성** | 불가능 (Copy 필수) | 우수 (Hard Link 통해 공유) | 이론적으로 최우수하지만 관리 비용 과다 |
| **삭제 메커니즘** | 단순 제거 (Simple Delete) | **참조 횟수 기반 제거 (Reference Counting)** | Mark-and-Sweep 등 가비지 컬렉션(GC) 필요 |
| **대표 예시** | MS-DOS, 초기 파일 시스템 | **UNIX/Linux (Standard FS)** | 분산 파일 시스템 (특정 네트워크 FS) |

**2. 하드 링크(Hard Link) vs 심볼릭 링크(Symbolic Link) 상세 분석**

DAG 구조에서 가장 중요한 두 가지 링크 방식의 기술적 차이와 운영상의 장단점을 비교합니다.

| 비교 항목 | 하드 링크 (Hard Link) | 심볼릭 링크 / 소프트 링크 (Symbolic/Soft Link) |
|:---|:---|:---|
| **저장 매체 (Storage)** | 원본과 **동일한 Inode** 사용 | **새로운 독립적인 Inode** 생성 |
| **데이터 내용 (Data)** | 원본 파일의 물리적 블록 주소 (Block Pointers) | 원본 파일의 **경로명(Pathname)** 문자열 |
| **파일 시스템 제약** | **동일한 파일 시스템(파티션) 내에서만 생성 가능** | 다른 파일 시스템, 네트워크 드라이브, 파티션 간