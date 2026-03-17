+++
title = "525. 디렉터리 구현 - 선형 리스트 (Linear List)"
date = "2026-03-14"
weight = 525
+++

# [디렉터리 구현 - 선형 리스트 (Linear List)]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선형 리스트(Linear List)는 파일 시스템의 가장 기초가 되는 메타데이터 관리 구조로, 파일명과 **Inode (Index Node)** 포인터 쌍을 물리적 순서대로 나열하는 단순 연결(Sequential Chain) 방식이다.
> 2. **가치**: 복잡한 알고리즘 연산 없이 O(1)의 삽입 연산이 가능하고 메모리/디스크 오버헤드가 거의 없어, **ROM (Read-Only Memory)** 기반의 임베디드 시스템이나 부팅 파티션(Boot Partition)과 같은 자원 제약 환경에서 핵심적인 역할을 수행한다.
> 3. **융합**: 현대 OS의 **VFS (Virtual File System)**는 성능 저하를 방지하기 위해 dentry 캐싱을 적용하지만, 저레벨 디스크 블록 구조 자체는 여전히 선형성을 띠는 경우가 많으며, 이는 데이터베이스의 풀 테이블 스캔(Full Table Scan) 최적화 기법과 직결된다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
선형 리스트(Linear List) 디렉터리 구현은 파일 시스템 내에서 파일의 논리적 식별자(파일명)와 해당 파일의 메타데이터 위치(Inode 번호 또는 **FCB (File Control Block)** 주소)를 매핑하는 테이블을, 물리적 순서대로 나열하는 자료 구조를 의미한다. 배열(Array) 기반의 연속 할당 방식과 연결 리스트(Linked List) 기반의 불연속 할당 방식이 있으나, 데이터를 찾기 위해 순차적으로 접근해야 하는 **Sequential Access (순차 접근)** 특성은 동일하다.

**등장 배경 및 철학**
초기 컴퓨팅 환경(CP/M, MS-DOS)과 단순한 파일 시스템(**FAT (File Allocation Table)**)은 하드웨어 자원이 희소했고 파일 개수가 적었다. 따라서 복잡한 해싱(Hashing)이나 균형 트리(Balanced Tree) 구조의 연산 오버헤드를 감당할 수 없었다. 선형 리스트는 "구현의 단순성(Simplicity)"과 "공간 효율성(Spatial Efficiency)"을 극대화하기 위해 탄생했으며, 디스크의 섹터 단위 읽기 특성과 잘 맞물려 작동한다.

**구조적 한계와 현대적 맥락**
파일 개수 $N$이 증가함에 따라 검색 시간 복잡도가 $O(N)$으로 선형적으로 증가하므로, 현대의 고성능 파일 시스템(EXT4, NTFS, ZFS)은 검색을 위해 **HTree (Hash Tree)**나 **B+ Tree** 구조를 사용한다. 그러나 선형 리스트는 여전히 부팅 로더나 소규모 로그 영역, 혹은 복잡한 인덱싱이 필요 없는 임시 파일 시스템(**RAM Disk**, **tmpfs**)의 기반이다.

```text
[ Evolution of Directory Structures ]

Stage 1: Linear List (Simple)
[File A] -> [File B] -> [File C] -> (...)
+ Slow Search (O(N)), Fast Append, Low Memory

Stage 2: Tree/Hash (Complex)
    [Root]
    /  |  \
 [A]  [B]  [C] ... (Indexed)
+ Fast Search (O(log N) or O(1)), High Overhead, Complex Logic
```

📢 **섹션 요약 비유**: 선형 리스트는 마치 **"번호표 없이 줄 서서 입장하는 주말 카페의 대기 명단"**과 같습니다. 가장 뒤에 이름을 적는 것(삽입)은 매우 쉽고 빠르지만, 내 차례가 되었는지 확인하려면(검색) 처음부터 끝까지 이름을 하나하나 읽어봐야 하는 구조입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**
선형 리스트 디렉터리는 복잡한 계층 구조 없이 플랫(Flat)한 데이터 레코드의 연속체이다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 데이터 타입/크기 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **File Name** | 사용자 식별자 (User Key) | 문자열 비교(`strcmp`)를 통해 Key 역할 수행, Null로 종료 | `char[]` (가변) | 사람 이름 |
| **Inode Number** | 메타데이터 포인터 (Pointer) | 파일 시스템의 **Inode 테이블** 인덱스를 가리킴 | `unsigned int` (4B) | 주민등록번호 |
| **Record Status** | 유효성 비트 (Valid Bit) | 파일 삭제 시 해당 슬록(Slot) 재사용을 위해 'Free' 표시 | `char` (1B) | 퇴거 표시 |
| **Next Pointer** | 연결 고리 (Chain) | (Linked List 시) 다음 레코드의 물리적 블록 주소를 저장 | `block_addr` (4B) | 다음 집 주소 |
| **Length** | 레코드 길이 | 가변 길이 파일명 처리를 위해 현재 엔트리의 크기 저장 | `short` (2B) | 편지지 크기 |

**아키텍처 다이어그램 및 데이터 흐름**
다음은 연결 리스트(Linked List) 형태를 기반으로 한 선형 디렉터리의 메모리 및 디스크 레이아웃과 파일 시스템 스택 간의 상호작용을 도식화한 것이다.

```text
+-----------------------------------------------------------------------+
|                   [ File System Layer (VFS) ]                         |
|  System Call: open("/config/sys.cfg", O_RDONLY)                       |
+-----------------------------------------------------------------------+
                                    | 1. Lookup Request
                                    v
+-----------------------------------------------------------------------+
|               [ Directory Implementation Layer (Linear List) ]        |
+-----------------------------------------------------------------------+
|  [ Directory Block on Disk ]                                          |
|  +------------------+      +------------------+      +------------------+
|  | Entry 1          |      | Entry 2          |      | Entry 3          |
|  | Name: "boot.ini" | ---> | Name: "logo.png"| ---> | Name: "sys.cfg"  |
|  | Inode: #1204     |      | Inode: #3509     |      | Inode: #8821     |
|  | Next: Ptr Entry2 |      | Next: Ptr Entry3 |      | Next: NULL       |
|  +------------------+      +------------------+      +------------------+
|                                                                  ^
|                                                                  | 2. Pointer Chasing
|                                                       (Sequential Scan)
+-----------------------------------------------------------------------+
                                    | 3. Found Inode #8821
                                    v
+-----------------------------------------------------------------------+
|                         [ Inode Table (Metadata) ]                    |
+-----------------------------------------------------------------------+
| #8821 | [ Type: REG | Mode: 644 | Size: 4096 | Ptrs: [Blk#500] ]      |
+-----------------------------------------------------------------------+
```

**심층 동작 원리 (Algorithm & Mechanism)**
운영체제의 파일 시스템 드라이버가 `open("sys.cfg")` 시스템 콜을 처리하여 선형 리스트를 탐색하는 과정은 다음과 같다.

1.  **Initialization**: **VFS (Virtual File System)**는 해당 경로의 마지막 컴포넌트인 디렉터리에 대한 **dentry** 캐시를 확인한다. Miss 발생 시 디스크 I/O 요청.
2.  **Linear Scan (The Core Mechanism)**:
    *   디스크 블록을 버퍼 캐시(Buffer Cache)로 로드.
    *   블록 내의 첫 번째 엔트리부터 순회(Iteration) 시작.
    *   `strcmp(entry->name, "sys.cfg") == 0` 연산 수행.
    *   **Performance Critical Point**: 문자열 비교 연산이 $N$번 반복됨. 디스크 헤드가 블록을 건너뛰며 발생하는 **Seek Time**이 누적됨.
3.  **Validation**:
    *   파일명이 일치하더라도 `Record Status`가 "Deleted" 또는 "Free" 상태이면 계속 진행.
    *   유효한 엔트리 발견 시 `Inode Number` 추출.
4.  **Return**: 발견된 Inode 번호를 통해 실제 데이터 블록의 주소를 얻고, 파일 디스크립터(File Descriptor)를 반환.

```c
// Pseudo-code: Linear Search in Directory (Deep Dive Version)
struct DirEntry* linear_search_directory(struct SuperBlock* sb, char* target_name) {
    struct Block* current_block = read_directory_block(sb->dir_start_block);
    struct DirEntry* entry = (struct DirEntry*)current_block->data;

    while (current_block != NULL) {
        // 1. Check if entry is active
        if (entry->status != ENTRY_DELETED) {
            // 2. String Comparison (Expensive CPU operation)
            if (strncmp(entry->file_name, target_name, MAX_NAME_LEN) == 0) {
                return entry; // Success: Return Inode Pointer
            }
        }

        // 3. Move to next entry
        entry = (struct DirEntry*)((char*)entry + entry->length);
        
        // End of block? Load next linked block
        if (offset >= BLOCK_SIZE) {
            current_block = read_block(current_block->next_ptr);
            entry = (struct DirEntry*)current_block->data;
        }
    }
    return NULL; // Failure: Not Found (O(N))
}
```

📢 **섹션 요약 비유**: 이 구조는 **"기차에 짐을 싣고 내리는 과정"**과 같습니다. 짐을 찾을 때 창고지기가 기적을 울리며 1번 칸부터 마지막 칸까지 문을 열고 하나하나 확인해야 합니다. 기차가 길어지면(파일이 많아지면) 찾는 시간이 기차의 길이에 정확히 비례해서 늘어납니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

선형 리스트는 단순함이 무기이나, 대용량 환경에서는 치명적이다. 이를 극복하기 위한 타 자료 구조와의 비교 분석과 타 시스템(OS, DB)과의 융합 관점을 서술한다.

**심층 기술 비교: Linear List vs. Advanced Structures**

| 비교 항목 | 선형 리스트 (Linear List) | 해시 테이블 (Hash Table) | B-Tree (Balanced Tree) |
|:---|:---|:---|:---|
| **검색 복잡도 (Search)** | **O(N)** - Worst Case: 전체 스캔 | **O(1)** - Average: Constant access | **O(log N)** - Stable: Logarithmic |
| **삽입/삭제 (Insert/Delete)**| **O(1)** (Append) / **O(N)** (Search) | **O(1)** (Collision 처리 비용 제외) | **O(log N)** (Rotation/Rebalancing) |
| **공간 오버헤드 (Space)** | **낮음 (Low)** - 데이터 저장만 수행 | **높음 (High)** - Bucket 관리 공간 필요 | **높음 (High)** - 자식 노드 포인터 저장 |
| **순차 접근 (Sequential Access)**| **우수** - 인접 블록 읽기 유리 | **불량** - 무작위 접근으로 캐시 미스 유발 | **우수** - In-order Traversal 가능 |
| **구현 복잡도 (Complexity)**| **매우 낮음** - 포인터 연산만 가능 | **중간** - Collision Resolution 로직 필요 | **매우 높음** - 재귀적 로직 및 균형 유지 |

**융합 관점 1: OS 메모리 관리와의 상관관계 (Synergy)**
*   **Page Cache (페이지 캐시)와의 시너지**: 선형 리스트의 디스크 성능 저하를 극복하는 가장 강력한 무기는 OS의 **Page Cache**이다. 한 번 읽힌 디렉터리 블록이 RAM에 캐싱되면, 이후의 $O(N)$ 검색 연산은 메모리 대역폭만으로 수행되어 디스크 탐색 없이 빠르게 처리된다.
*   **TLB (Translation Lookaside Buffer)**: 선형 리스트는 메모리 접근 패턴이 순차적(Sequential)이므로, **Spatial Locality (공간 지역성)**이 뛰어나다. 이는 CPU의 TLB 히트율과 하드웨어 **Prefetcher (프리페처)**의 효율을 높이는 데 기여한다.

**융합 관점 2: 데이터베이스 인덱싱과의 비유 (Trade-off)**
*   데이터베이스 관점에서 선형 리스트는 "Heap Table"에 가깝다. 데이터가 소량일 때는 인덱스를 타는 비용(O(log N)의 트리 탐색 + 디스크 Random I/O)보다, 테이블을 처음부터 읽는 **Full Table Scan** (O(N)의 Sequential I/O)이 더 빠를 수 있다.
*   **Decision Point**: 파일 개수가 **Threshold (임계값, 예: 1,000개)** 이하일 때는 선형 리스트가 복잡한 트리 구조보다 총 실행 시간(Total Latency)이 더 짧을 수 있는 이유이다.

📢 **섹션 요약 비유**: 선형 리스트는 **"편의점 냉장고"**와 같습니다. 음료수가 몇 개 없을 땐 눈으로 슉 스캔하면 바로 찾습니다. 하지만 데이터가 많아지면 **"자판기(해시 테이블)"**처럼 버튼(해시 키)을 눌러 바로 꺼내는 방식이나, **"대형 도서관 분류식(B-Tree)"**처럼 정리된 위치를 찾아가는 방식이 훨씬 효율적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

시스템 아키텍트로서 선형 리스트 방식을 채택할지, 고급 구조로 전환할지에 대한 의사결정 트리와 체크리스트를 제시한다.

**실무 시나리오 및 의사결정 프로세스**

1.  **Scenario A: 임베디드 시스템 / 부트로더 (Bootloader)**
    *   *Context*: 리눅스 부팅 초기 `initramfs`나 펌웨어 영역. **SRAM (Static RAM)** 용량이 극도로 제한적임.
    *   *Decision*: **선형 리스트 채택 (Adopt)**.
    *   *Rationale*: 코드 크기(Code Size)를 최소화해야 하며, 파일 개수가 수십 개 내외임. 복잡한 B-Tree 로직을 위한 스택 메모리(Stack Memory) 할당이 부담스러움. 단순한 포인터 연산으로 충분함.

2.  **Scenario B: 대용량 스토리지 서버 (NAS / Cloud Storage)**
    *   *Context*: 수십만 개의 사진 파일이 저장된 사진첩 앱 백엔드.
    *   *Decision*: **선형 리스트 기피 (Avoid) 및 Hashing/B-Tree 이주**.
    *   *Rationale*: 사용자 경험(UX) 측면에서 폴더 로딩 시간이 1초 이상