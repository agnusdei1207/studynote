+++
title = "534. 인덱스 할당의 확장 - 연결 방식, 다단계 인덱스, 혼합 인덱스"
date = "2026-03-14"
weight = 534
+++

# [534. 인덱스 할당의 확장 - 연결 방식, 다단계 인덱스, 혼합 인덱스]

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 인덱스 블록의 물리적 주소 공간 한계를 극복하기 위해, 인덱스 블록을 연결(Linked)하거나 계층(Multi-level)을 형성하거나, 직접/간접 포인터를 혼합(Combined)하여 대용량 파일 지원을 가능하게 하는 구조적 확장 기법이다.
> 2. **가치**: 4KB 블록 기준 단일 인덱스로는 4MB만 커버되지만, 다단계/혼합 확장을 통해 수 TB(Terabyte)급 파일까지 **O(1)** 또는 **O(log N)**의 접근 시간 복잡도로 관리하여 시스템 확장성(Scalability)을 비약적으로 향상시킨다.
> 3. **융합**: 이 기법은 OS의 파일 시스템(Ext4, NTFS, APFS)과 데이터베이스의 B-Tree 인덱싱의 근간이 되며, 가상 메모리의 페이징 테이블 구조와도 설계 철학을 같이한다.

---

### Ⅰ. 개요 (Context & Background) - 인덱스 할당의 확장성 한계와 극복

#### 1. 개념 및 배경
파일 시스템(File System)에서 데이터는 고정 크기의 블록(Block) 단위로 저장되며, 이러한 블록들의 위치를 가리키는 주소(Address)를 인덱스 블록(Index Block)에 저장하여 관리한다. 기본적인 **인덱스 할당(Indexed Allocation)** 방식은 하나의 인덱스 블록이 가질 수 있는 포인터 수에 물리적 제한이 있다.

예를 들어, 디스크 블록 크기가 **4KB**이고 블록 주소(포인터)의 크기가 **4B**(Bytes)일 때, 하나의 인덱스 블록은 단 1,024개(4096 / 4)의 주소를 저장할 수 있다. 이는 **4,096 Byte × 1,024 = 4MB**의 파일 크기만 지원 가능함을 의미한다. 현대의 멀티미디어 데이터나 빅데이터 환경에서 이러한 제한은 치명적이다. 따라서 단일 인덱스 블록의 용량을 넘어서는 대용량 파일(Large Files)을 효율적으로 접근하고 관리하기 위해 인덱스 구조를 확장할 필요성이 생긴다.

#### 2. 기술적 한계 및 패러다임 시프트
① **기존 한계**: 단일 인덱스 블록의 포인터 개수 제약으로 인한 파일 크기 상한선 존재. 연결 할당(Linked Allocation)의 순차 접근 성능 문제와 연속 할당(Contiguous Allocation)의 단편화 문제를 동시에 해결해야 함.
② **혁신적 패러다임**: 인덱스 블록 자체를 데이터처럼 취급하거나, 인덱스를 가리키는 인덱스(Indirection)를 도입하여 계층 구조(Hierarchy)를 형성. 이를 통해 논리적 주소 공간(Logical Address Space)을 물리적 제약 없이 확장.
③ **비즈니스 요구**: 수십 기가바이트(GB)에서 테라바이트(TB) 단위의 대용량 로그 파일, 고해상도 영상, DB 백업 파일을 저장하고 빠르게 검색(Retrieval)해야 하는 현실적 요구사항 대응.

#### 3. 확장 전략별 구조적 비유 (ASCII)

```text
+=============================================================================+
|                 [ Index Block Expansion Strategies ]                       |
+=============================================================================+
| Strategy 1. Linked Scheme      | Strategy 2. Multi-level Index             |
| (Chain of Index Blocks)        | (Tree Structure)                          |
|                                |                                           |
|  [Index 1] ──next──▶ [Index 2] │        [Root Index Block]                 |
|    |  |  |           |  |  |   │          /    |    \                      |
| [D][D][D]         [D][D][D]    │    [L1-1] [L1-2] [L1-3]                   |
| (Access Time: O(N))            │     /|\      /|\      /|\                 |
|                                │   [D] [D] [D] [D] [D] [D]                |
|                                | (Access Time: O(1) ~ O(log N))           |
+-----------------------------------------------------------------------------+
| Strategy 3. Combined Scheme (UNIX inode)                                    |
|                                                                             |
| [ inode ]                                                                   |
| [Direct][Direct]... + [Single Indirect] + [Double Indirect] + [Triple ...]  |
|   ▲                     ▲                      ▲                          |
| (Small Files)         (Medium)               (Huge Files)                  |
+=============================================================================+
```
*도해 설명: Linked는 끝을 찾을 때까지 걸어가는 것이고, Multi-level은 지하철 노선도를 보고 환승하는 것이며, Combined은 자주 쓰는 물건은 주머니에(Direct), 덜 쓰는 것은 가방에(Single Indirect) 넣는 전략이다.*

📢 **섹션 요약 비유**: 확장된 인덱스 할당은 "단층 건물에서 고층 빌딩으로의 진화"와 같습니다. 단층 건물(단일 인덱스)은 거주자(데이터)가 조금만 늘어나도 붐비지만, 고층 빌딩(다단계/혼합)은 엘리베이터(포인터)를 통해 수만 명의 거주자를 효율적으로 수용할 수 있게 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 분석
확장된 인덱스 할당을 구성하는 핵심 요소들은 파일의 크기와 접근 패턴에 따라 메모리 공간을 어떻게 활용할지 결정한다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/구조 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Direct Pointer** (직접 포인터) | 파일의 시작 데이터 블록을 직접 가리킴 | FCB (File Control Block) 내에 존재, 추가 I/O 없이 바로 데이터 접근 | 메타데이터 내부 주소 | **지갑 속 현금**: 바로 꺼내 쓸 수 있는 가장 빠른 자산 |
| **Indirect Pointer** (간접 포인터) | 데이터 블록 대신 '인덱스 블록'을 가리킴 | 포인터를 해석하기 위해 디스크 접근이 추가로 필요함 | 단일/이중/삼중 구분 | **두꺼비 집**: 열쇠를 찾으려면 집안을 뒤져야 함 |
| **Index Block** (인덱스 블록) | 데이터 블록의 주소들을 저장하는 전용 데이터 블록 | 사용자 데이터가 아닌 '주소 정보'만 저장, 포인터 크기에 따라 용량 결정 | 배열(Array) 형태 | **목차 (Table of Contents)**: 내용의 위치를 안내 |
| **Link Pointer** (연결 포인터) | 다음 인덱스 블록을 연결하는 포인터 | 연결 리스트(Linked List) 형성, 순차 접근 유발 | Null일 때까지 순회 | **다음 쪽 번호**: 책장 끝에 적힌 페이지 넘기기 |
| **inode** | 파일의 소유자, 권한, 크기, 위치 등 메타데이터 저장 | UNIX/Linux 시스템의 핵심 구조체, Direct/Indirect 포인터 배열 포함 | 고정 크기 구조체 | **사람명부**: 개인의 모든 기본 정보가 담긴 문서 |

#### 2. 핵심 확장 기법 및 ASCII 다이어그램

**A. 연결 방식 (Linked Scheme)**
기존 인덱스 블록의 마지막 필드를 예약하여 다음 인덱스 블록의 주소를 저장하는 방식이다. 파일이 커질 때마다 인덱스 블록을 동적으로 추가 할당한다. 구현이 간단하지만, 임의 접근(Random Access) 성능이 저하된다.

**B. 다단계 인덱스 (Multi-level Index)**
이진 트리(Binary Tree)나 B-Tree와 유사하게, 상위 인덱스 블록이 하위 인덱스 블록을 가리키는 구조이다. 예를 들어 2단계 인덱스는 Root Index가 가리키는 리프 노드가 실제 데이터 블록을 가리킨다. $O(1)$에 가까운 접근 성능을 제공한다.

**C. UNIX 혼합 방식 (Combined Scheme - inode)**
가장 현실적이고 널리 쓰이는 방식으로, `inode` 내에 직접 주소 12개, 단일 간접 1개, 이중 간접 1개, 삼중 간접 1개 등을 배치하여 파일 크기에 따라 최적의 경로를 선택한다.

```text
================================================================================
                    [ UNIX Style Combined Scheme (inode) ]
================================================================================

[  FCB / inode  ]
┌────────────────────────────────────────────────────────────────────────────┐
│ File Metadata: Permission, Size, Owner, Dates...                          │
├────────────────────────────────────────────────────────────────────────────┤
│ Direct Pointers (0 ~ 11)                                                  │
│ [P0] ──▶ [Data]  [P1] ──▶ [Data] ... [P11] ──▶ [Data]                     │
│ (Small files: Immediate access, No extra I/O)                             │
├────────────────────────────────────────────────────────────────────────────┤
│ Single Indirect Pointer (12)                                              │
│ [P_Single] ──▶ [Index Block S1] ──▶ [Data] [Data] [Data] ... [Data]      │
│ (Medium files: +4KB * 1024 = +4MB)                                        │
├────────────────────────────────────────────────────────────────────────────┤
│ Double Indirect Pointer (13)                                              │
│ [P_Double] ──▶ [Index Block D1]                                           │
│                └─▶ [Index Block D2-1] ──▶ [Data]...                       │
│                └─▶ [Index Block D2-2] ──▶ [Data]...                       │
│ (Large files: +4GB)                                                       │
├────────────────────────────────────────────────────────────────────────────┤
│ Triple Indirect Pointer (14)                                              │
│ [P_Triple] ──▶ [1st] ──▶ [2nd] ──▶ [3rd] ... ──▶ [Data]                  │
│ (Huge files: +4TB)                                                        │
└────────────────────────────────────────────────────────────────────────────┘

[ Calculation Logic (Assume Block=4KB, Ptr=4B) ]
- Direct: 12 * 4KB = 48KB
- Single: 1 * 1024 * 4KB = 4MB
- Double: 1 * 1024 * 1024 * 4KB = 4GB
- Triple: 1 * 1024^3 * 4KB = 4TB
================================================================================
```
**해설**:
1.  **Direct Block**: 파일의 초기 48KB는 최고 속도로 접근한다. 웹 서버의 작은 HTML 파일이나 아이콘 등은 이 영역에 들어있어 성능이 극대화된다.
2.  **Indirection (간접화)**: 파일이 커질수록 깊이(Depth)가 깊어진다. `Triple Indirect` 포인터를 통해 이론적으로 수 테라바이트(TB)의 파일도 하나의 inode로 관리된다.
3.  **공간 효율성**: 파일 크기가 작더라도 `inode` 크기는 고정(일반적으로 128~256Bytes)이므로 메모리 낭비가 최소화된다.

#### 3. 핵심 알고리즘 및 수식
파일 시스템의 최대 파일 크기 $S_{max}$는 다음과 같이 계산된다.

$$ S_{max} = (N_{direct} \times B) + (B/P \times B) + (B/P)^2 \times B + (B/P)^3 \times B $$

*   $B$: 디스크 블록 크기 (Byte)
*   $P$: 포인터 크기 (Byte)
*   $B/P$: 하나의 인덱스 블록이 가질 수 있는 포인터 수

```c
// C 의사코드: 다단계 인덱스 블록 접근 로직
// Block Size: 4096, Pointer Size: 4 => Pointers per Block: 1024

#define BLOCK_SIZE 4096
#define PTR_PER_BLOCK (BLOCK_SIZE / sizeof(int))

typedef struct {
    int direct[12];
    int single_indirect;
    int double_indirect;
    int triple_indirect;
} Inode;

// 이중 간접 블록을 통한 데이터 접근 시뮬레이션
void read_double_indirect(int disk_block_num, int logical_block_index) {
    // 1단계: 1차 인덱스 블록 로드 (디스크 I/O 발생)
    int *first_index_block = (int *)read_disk_block(disk_block_num);
    
    // 2단계: 오프셋 계산 (Tree 구조 탐색)
    int index1 = logical_block_index / PTR_PER_BLOCK;
    int index2 = logical_block_index % PTR_PER_BLOCK;
    
    // 3단계: 2차 인덱스 블록 주소 획득 및 로드 (디스크 I/O 발생)
    int second_block_num = first_index_block[index1];
    int *second_index_block = (int *)read_disk_block(second_block_num);
    
    // 4단계: 최종 데이터 블록 주소 획득
    int data_block_num = second_index_block[index2];
    
    // 최종 데이터 로드
    byte *data = read_disk_block(data_block_num);
}
```

📢 **섹션 요약 비유**: 이 아키텍처는 "도서관의 분류 시스템"과 흡사합니다. 대출 빈도가 높은 신간(Direct)은 입구 바로 앞에 비치하고, 조금 덜 빈간한 책(Single Indirect)은 1열 서가에, 그리고 오래된 논문이나 전집(Double/Triple Indirect)은 지하 서고의 목차를 2번, 3번 거쳐서 찾아가는 방식입니다. 이렇게 하면 방의 크기(인덱스 공간)를 아주 작게 유지하면서도 도서관의 총 장서 수(파일 크기)를 무한대로 늘릴 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 (Quantitative & Structural)

| 비교 항목 | 연결 방식 (Linked) | 다단계 인덱스 (Multi-level) | 혼합 방식 (Combined) |
|:---|:---|:---|:---|
| **접근 방식** | 순차적 (Sequential) | 임의적 (Random) | 파일 크기 기반 적응적 (Adaptive) |
| **성능 (Latency)** | $O(N)$: 끝부분일수록 느림 | $O(1)$ ~ $O(\text{depth})$: 매우 빠름 | 작은 파일 $O(1)$, 큰 파일 $O(\text{depth})$ |
| **공