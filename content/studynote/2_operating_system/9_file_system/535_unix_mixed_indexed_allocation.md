+++
title = "535. UNIX 파일 시스템의 혼합 인덱스 (Direct, Single/Double/Triple Indirect)"
date = "2026-03-14"
weight = 535
+++

# 535. UNIX 파일 시스템의 혼합 인덱스 (Direct, Single/Double/Triple Indirect)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **UNIX File System (UFS, 유닉스 파일 시스템)**은 **inode (Index Node, 아이노드)** 내에 **Direct Block (직접 블록)**과 다단계 **Indirect Block (간접 블록)**을 혼합 배치하여, 파일의 크기에 따라 비대칭적인 I/O 경로를 제공하는 구조이다.
> 2. **가치**: 파일 시스템의 **Localilty of Reference (참조의 지역성)** 전제(대부분의 파일은 작다)에 기반하여, **Direct Pointer**를 통해 대다수의 액세스를 단 1회의 디스크 **Seek (탐색)**으로 완료하여 성능을 극대화한다.
> 3. **융합**: 현대 OS의 **Paging (페이징)** 기법인 **Multi-level Page Table (다단계 페이지 테이블)**과 논리적으로 동일한 트리 구조를 가지며, 데이터베이스의 **B-Tree (Balanced Tree)** 인덱싱과도 설계 철학을 공유한다.

---

### Ⅰ. 개요 (Context & Background)

**UNIX 파일 시스템**의 **혼합 인덱스(Combined Indexing)** 방식은 디스크 공간의 효율성과 데이터 접근 속도라는 두 가지 상충하는 목표를 동시에 달성하기 위해 설계되었다. 파일 시스템의 기본 할당 방식인 연결 할당(Linked Allocation)과 인덱스 할당(Indexed Allocation)은 각각 순차 접근 효율성과 임의 접근 자유도라는 장점을 가졌으나, 대용량 파일 처리나 빈번한 작은 파일 처리에서 한계가 있었다.

**기술적 진화 배경:**
1.  **연결 할당의 한계**: 파일의 각 블록이 다음 블록의 주소를 포함해야 하므로, 임의 접근(Random Access) 시 연결 리스트를 순회해야 하는 **O(N)** 시간 복잡도 문제와 불필요한 디스크 읽기가 발생한다.
2.  **순수 인덱스 할당의 한계**: 하나의 인덱스 블록이 가리킬 수 있는 포인터 개수(예: 4KB 블록 시 1,024개)로 파일 크기가 제한된다. 이를 극복하기 위해 인덱스 블록을 연결하면 다시 연결 할당의 순차 접근 문제가 발생한다.
3.  **UNIX의 패러다임 전환**: "파일 크기의 분포는 **Pareto Distribution (파레토 분포)**를 따른다"는 통계적 관찰에 기초한다. 즉, 전체 파일 수의 80%는 작은 크기(KB 단위)를 가지지만, 디스크 공간의 80%는 일부 거대 파일(GB~TB 단위)이 차지한다는 점을 착안하여, 작은 파일은 1단계 구조로 빠르게, 큰 파일은 다단계 구조로 수용하는 하이브리드 전략을 채택했다.

**💡 개요를 관통하는 비유**
혼합 인덱스는 마치 **"도심의 건물 주소 시스템"**과 같습니다. 대부분의 가게(작은 파일)는 길가 번지(Direct)를 바로 알고 있어 찾기 쉽지만, 대형 쇼핑몰이나 아파트 단지(큰 파일)는 단지 내부 번지(Indirect)를 다시 확인해야 하는 복합적인 구조로 되어 있어, 주소록(inode)의 크기는 작게 유지하면서도 무한한 공간을 관리할 수 있습니다.

📢 **섹션 요약 비유**: 혼합 인덱스 설계는 **"자주 쓰는 전화번호는 단축키에, 그렇지 않은 번호는 주소록에"** 저장하는 스마트폰 주소록과 같습니다. 자주 연락하는 사람(작은 파일)은 단축키(Direct)로 즉시 연결되고, 자주 안 부르는 사람(큰 파일)은 주소록(Indirect)을 열어 이름을 찾는 과정(추가 I/O)을 거치더라도, 전체 주소록 공간을 효율적으로 사용하는 원리입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

혼합 인덱스의 핵심은 **inode (Index Node)** 내부의 주소 배열을 용도별로 계층화하는 데 있다. 전형적인 UNIX **System V** 또는 **BSD** **Fast File System (FFS, 고속 파일 시스템)** 기준으로 **inode**는 보통 15개의 포인터(또는 13개)를 가진다.

#### 1. 구성 요소 상세 분석 (Component Analysis)

| 구분 요소 (Component) | ID | 역할 (Role) | 내부 동작 메커니즘 (Mechanism) | 디스크 I/O 횟수 (Seek Count) | 비유 (Analogy) |
|:---:|:---:|:---|:---|:---:|:---|
| **Direct Pointer**<br>(직접 블록) | 0~11 | 실제 데이터 블록의 물리적 주소를 직접 저장 | inode 내의 주소 값을 디스크 컨트롤러에 전달하여 즉시 접근. 메모리 매핑 시 가장 낮은 **Latency (지연 시간)** 제공. | **1 회** | 바로 주머니에서 꺼내 쓰는 **잔돈** |
| **Single Indirect**<br>(단일 간접) | 12 | 데이터 블록의 주소들을 모아둔 '인덱스 블록' 가리킴 | inode -> 인덱스 블록 로드 -> 내부 포인터 해석 -> 데이터 블록 접근. 1회의 간접 참조 발생. | **2 회** | 내 지갑이 들어있는 **가방** |
| **Double Indirect**<br>(이중 간접) | 13 | '단일 간접 블록'을 가리키는 '이중 간접 블록' 가리킴 | inode -> 이중 인덱스 블록 -> 단일 인덱스 블록 -> 데이터 블록. 2단계 트리 탐색. | **3 회** | 가방이 들어있는 **사물함** |
| **Triple Indirect**<br>(삼중 간접) | 14 | 3단계 깊이의 인덱스 트리의 루트 가리킴 | 파일 시스템의 최대 용량 한계를 확장하기 위한 장치. 접근 경로가 가장 깊음. | **4 회** | 사물함이 있는 **역사물함** |

> **참고 (Reference)**: 블록 크기 $B=4\text{KB}$, 포인터 크기 $P=4\text{B}$ 일 때, 하나의 인덱스 블록은 $1024$개의 포인터를 저장할 수 있다.

#### 2. 구조적 데이터 흐름 (ASCII Architecture)

다음은 사용자가 파일의 끝 부분에 위치한 데이터를 요청했을 때, 파일 시스템이 물리적 블록을 찾아가는 과정을 도식화한 것이다.

```text
  [ User File Offset: Very Large File ]

  +-------------------------------------------------------+
  |  I-Node (Index Node)                                  |
  | +---------------------------------------------------+ |
  | | File Metadata: Permissions, Size, Timestamps...   | |
  | +---------------------------------------------------+ |
  | | [0] Direct Block Ptr  --------------------------+  | |
  | | [1] Direct Block Ptr  ----------------------+   |  | |
  | | ... (Skip for brevity)                     |   |  | |
  | | [11] Direct Block Ptr ------------------+   |   |  | |
  | |                                       |   |   |  | |
  | | [12] Single Indirect Ptr              |   |   |  | |
  | |     (Points to Index Block)           |   |   |  | |
  | |                                       |   |   |  | |
  | | [13] Double Indirect Ptr  ------------+   |   |  | |
  | |     (Points to Double Index Block)        |   |  | |
  | |                                           |   |  | |
  | | [14] Triple Indirect Ptr ------------------+   |  | |
  | |     (Points to Triple Index Block)            |  | |
  | +---------------------------------------------------+ |
  +-------------------------------------------------------+
        |            |                 |               |
        | (Direct)   | (1-Level)       | (2-Level)     | (3-Level)
        v            v                 v               v
  [ Data ]    [ Single ]      [ Double ]       [ Triple ]
  [ Block ]   [ Index  ]      [ Index  ]       [ Index  ] <-- 1st Level Read
              [ 0..N   ]      [ 0..M   ]       [ 0..K   ]
                 |                |                 |
                 v                v                 v
              [ Data ]      [ Single ]       [ Double ] <-- 2nd Level Read
              [ Block ]      [ Index ]       [ Index ]
                             |  ...           |
                             v                v
                          [ Data ]      [ Single ] <-- 3rd Level Read
                          [ Block ]      [ Index ]
                                               |
                                               v
                                            [ Data ]  <-- Final Data
                                            [ Block ]
```

**해설 (Deep Dive Explanation):**
1.  **Direct Path**: inode의 `i_block[0]`~`[11]` 영역은 실제 데이터의 물리적 블록 번호를 직접 저장한다. 운영체제 파일 시스템 드라이버는 이 값을 읽자마자 **Disk Scheduler (디스크 스케줄러)**에게 I/O 요청을 보낸다. 이는 메모리의 **Array (배열)** 접근과 유사한 **O(1)** 성능을 보인다.
2.  **Indirect Path**: 파일 크기가 커질수록(약 48KB 이후), 시스템은 Single Indirect 포인터를 참조한다. 이 포인터가 가리키는 블록은 데이터가 아닌 '주소의 배열'이므로, 시스템은 이를 먼저 **Page Cache (페이지 캐시)**로 로드한 후(Additional I/O), 다시 그 안에서 목적지 주소를 찾는다.
3.  **Tree Traversal**: Triple Indirect 영역에 있는 데이터를 읽는 것은 트리 자료구조에서 **Depth (깊이)**가 3인 노드를 찾는 것과 같다. 블록 주소를 계산하기 위해 `offset / (pointers_per_block^3)` 과 같은 나머지/몫 연산을 수행하여 각 레벨의 인덱스를 추출해야 한다.

#### 3. 핵심 알고리즘: 주소 변환 로직 (Address Translation)

파일 오프셋을 물리적 블록 번호로 변환하는 과정은 수학적 계산과 포인터 추적의 결합이다.

```c
// C-style Pseudocode for UNIX Address Translation
// Assumption: Block Size = 4KB, Pointer Size = 4B
// Addresses per Block = 1024

#define ADDR_PER_BLOCK (BLOCK_SIZE / sizeof(int))
#define DIRECT_BLOCKS 12

struct inode {
    int i_addr[15]; // 12 Direct, 1 Single, 1 Double, 1 Triple
};

// Function: Logical Offset -> Physical Block Number
int bmap(struct inode *ip, long offset) {
    long logical_block_index = offset / BLOCK_SIZE;
    int target_block_addr;

    // 1. Direct Block Zone
    if (logical_block_index < DIRECT_BLOCKS) {
        return ip->i_addr[logical_block_index]; // O(1) Access
    }

    // 2. Single Indirect Zone
    logical_block_index -= DIRECT_BLOCKS;
    if (logical_block_index < ADDR_PER_BLOCK) {
        // Read Index Block First
        int* single_idx_buf = disk_read(ip->i_addr[12]); 
        return single_idx_buf[logical_block_index];
    }

    // 3. Double Indirect Zone
    logical_block_index -= ADDR_PER_BLOCK;
    if (logical_block_index < ADDR_PER_BLOCK * ADDR_PER_BLOCK) {
        int idx1 = logical_block_index / ADDR_PER_BLOCK;
        int idx2 = logical_block_index % ADDR_PER_BLOCK;
        
        // Read First Level Index
        int* double_idx_buf = disk_read(ip->i_addr[13]);
        // Read Second Level Index
        int* single_idx_buf = disk_read(double_idx_buf[idx1]);
        return single_idx_buf[idx2];
    }
    
    // 4. Triple Indirect Zone (Recursive logic extends...)
    // Omitted for brevity, involves 3 levels of disk reads
}
```

📢 **섹션 요약 비유**: 이 인덱싱 구조는 **"지하철 노선도와 환승 시스템"**과 같습니다. 대부분의 승객(데이터)은 본선(Direct)을 통해 바로 목적지에 도착하지만, 외곽 지역(큰 파일)으로 나가는 승객은 환승(Indirect)을 여러 번 해야 합니다. 환승 횟수가 늘어날수록 이동 시간(I/O)이 느어나지만, 모든 역을 직선으로 연결하면 철도 설치 비용(inode 크기)이 감당할 수 없게 되는 것과 같은 이치입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

혼합 인덱스 방식은 다른 파일 시스템 구현 방식과 명확히 구분되며, 컴퓨터 과학 전반의 트리 관리 기법과 맞닿아 있다.

#### 1. 심층 기술 비교 분석표

| 비교 항목 | **혼합 인덱스 (Mixed Indexing)** | **연결 할당 (Linked Allocation)** | **Extent 기반 (Modern FS)** |
|:---|:---|:---|:---|
| **Random Access (임의 접근)** | **지원 (계층적)** <br>직접/간접 포인터 수준에 따라 지연 시간 상이 | **미지원** <br>순차 탐색(Sequential Scan)만 가능 | **지원 (B-Tree)** <br>Extent 트리를 통해 O(Log N) 접근 |
| **외부 단편화** | **존재** <br>블록 단위 할당으로 인해 Free List 관리 중요 | **없음** <br>필요 시 빈 곳 어디든 할당 가능 | **최소화** <br>연속 블록을 그룹(Extent)으로 관리 |
| **Metadata Overhead** | **고정 (Low)** <br>inode 크기가 고정(예: 128B)이어서 관리가 용이함 | **데이터 내 존재** <br>매 블록마다 다음 주소 포인터(4B) 필요 | **가변 (High)** <br>B-Tree 노드가 별도로 필요하므로 소형 파일에 비효율 |
| **대용량 파일 성능** | **중간** <br>Triple Indirect 접근 시 4회 I/O 필요 | **낮음** <br>수십만 개 블록이 있으면 탐색만 해도 시간 과다 | **높음** <br>연속된 공간을 한 번에 매핑하므로 매우 빠름 |

#### 2. 타 과목 융합 분석 (Convergence)

**① 운영체제 (OS) - 메모리 관리와의 유사성:**
혼합 인덱스의 **Direct/Single/Double Indirect** 구조는 가상 메모리의 **Multi-level Page Table (다단계 페이지 테이블)** 구조와 **1:1 매핑**된다.
-   **PDE/PTE**: Dou