+++
title = "540. 그룹화 (Grouping) 및 계수 (Counting) 방식"
date = "2026-03-14"
weight = 540
+++

# 540. 그룹화 (Grouping) 및 계수 (Counting) 방식

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **그룹화 (Grouping)**는 연결 리스트(Linked List)의 포인터 오버헤드를 최소화하기 위해 여러 빈 블록의 주소를 하나의 블록에 묶어서 관리하는 방식이며, **계수 (Counting)**는 연속된 빈 공간의 **시작 주소 (Start Address)**와 **개수 (Count)**를 쌍(Pair)으로 관리하여 저장 공간의 효율성을 극대화하는 기법이다.
> 2. **가치**: **FAT (File Allocation Table)**나 비트맵(Bitmap) 방식의 단점(느린 검색, 공간 낭비)을 보완하여, 대용량 디스크 환경에서 **메타데이터의 크기**를 줄이고 연속 할당(Contiguous Allocation) 필요 시 **탐색 속도 (Seek Time)**를 획기적으로 단축한다.
> 3. **융합**: 현대 파일 시스템(**Ext4**, **NTFS**, **APFS**)의 **Extents (익스텐트)** 기법의 이론적 기반이 되며, 데이터베이스의 **Segment Allocation**이나 메모리 관리의 **Buddy System**과도 설계 철학을 공유한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**
운영체제(OS)가 파일 시스템의 **빈 공간 목록 (Free Space List)**을 관리할 때, 모든 블록을 개별적으로 관리하면 관리를 위한 메타데이터 자체가 너무 커진다. 예를 들어, 1TB 디스크를 4KB 블록으로 쓴다면 약 2억 6천만 개의 엔트리가 필요하다. 이를 해결하기 위해 등장한 것이 **그룹화**와 **계수** 방식이다. 이 두 방식은 '공간의 지역성(Spatial Locality)'을 적극 활용하여 관리 오버헤드를 줄이는 것을 목표로 한다.

**등장 배경 및 진화**
1.  **한계**: 기존 **연결 리스트 (Linked List)** 방식은 n개의 빈 블록을 찾기 위해 디스크를 n번 읽어야 하는 치명적인 성능 저하(**I/O Burst**)가 있었다.
2.  **혁신**: 디스크 헤드의 이동을 줄이기 위해 연속된 공간을 선호하게 되면서, 단순히 "어디가 비었는가"를 넘어 "얼마나 연속으로 비었는가"를 관리하는 **계수(Counting)** 방식이 등장했다.
3.  **현재**: 대용량화되면서 실제 파일 시스템 구현에서는 이를 더욱 정교화한 **Extents**나 **B+ Tree** 기반의 관리 방식으로 발전하였으나, 임베디드나 간단한 파일 시스템에서는 여전히 유효한 알고리즘이다.

**💡 비유**
주소록에 전화번호를 하나씩 적는 대신, 회사 주소록처럼 부서별로 묶어서(그룹화) 관리하거나, 호텔 예약 시 "101호부터 105호까지 연속 예약"이라고 묶어서 말하는 것과 같다.

📢 **섹션 요약 비유**: 그룹화와 계수는 "도서관 사서의 책 정리법"과 같습니다. 사서가 책 한 권마다 도서대출부에 한 줄씩 쓰는 대신, 빈 책장 한 칸을 한 단위로 묶어서 기록(그룹화)하거나 "3번 책장은 10칸 연속 비어 있음"이라고 요약하여 적는(계수) 방식입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 두 방식의 내부 구조와 동작 메커니즘을 기술사 수준으로 분석한다.

#### 1. 구성 요소 비교

| 구분 | 그룹화 (Grouping) | 계수 (Counting) |
|:---|:---|:---|
| **데이터 단위** | `n`개의 블록 주소 목록 | `(Start Address, Count)` 쌍 |
| **저장 공간** | `n * (Pointer Size)` | `1 * (Pointer Size) + 1 * (Integer Size)` |
| **연속성 활용** | 낮음 (주소 흩어짐 허용) | 높음 (연속된 공간 전제) |
| **주요 용도** | 연결 리스트의 성능 보완 | 대규모 연속 공간 할당 |
| **복잡도 (할당)** | 리스트 탐색 후 제거 | 연속 공간 검색 및 분할 (Split) |

#### 2. 그룹화 (Grouping) 동작 메커니즘

연결 리스트의 노드 하나에 주소를 1개만 저장하는 대신, **비어있는 블록 하나를 '노드'로 활용**하여 그 안에 다른 비어있는 블록들의 주소를 대량으로 저장하는 방식이다.

**[ASCII 다이어그램: 그룹화 방식의 메모리 레이아웃]**

```text
[논리적 관점: Free List]
┌──────────────┐   next   ┌──────────────┐
│ Group Block  │─────────▶│ Group Block  │ ──────▶ ...
│   #100       │          │   #505       │
└──────┬───────┘          └──────────────┘
       │
       │ (Contains addresses)
       ▼
┌─────────────────────────────────────────────────────┐
│  Physical Block #100 (Used as Index Node)           │
├─────────────────────────────────────────────────────┤
│ [1] Free Block Addr: 102                            │
│ [2] Free Block Addr: 205                            │
│ [3] Free Block Addr: 409                            │
│ ...                                                 │
│ [n] Pointer to Next Free Block Group: #505 ────────┐│
└─────────────────────────────────────────────────────┘│
                                                          │
                                ┌─────────────────────────┘
                                ▼
                       Physical Block #505 (Data)
```

**[해설]**
1.  **포인터 효율성**: 일반적인 연결 리스트는 1개의 주소를 얻으려 1개의 블록을 읽어야 하지만, 그룹화는 1개의 블록(#100)을 읽으면 내부에 있는 수백 개의 주소를 즉시 얻을 수 있다.
2.  **재귀적 구조**: 첫 번째 블록은 데이터용 블록이 아니라 **인덱스(Index)** 역할을 수행한다. 이는 CPU의 **페이지 테이블 (Page Table)**의 다단계 구조와 유사한 메커니즘이다.
3.  **단점**: 모든 주소가 연속적이지 않을 때 유리하나, 리스트 중간의 주소를 사용하면 인덱스 블록을 업데이트해야 하는 쓰기 비용(Copy-on-Write 등)이 발생할 수 있다.

#### 3. 계수 (Counting) 동작 메커니즘

디스크상의 블록들은 파일 생성/삭제 과정에서 흩어지기보다 연속적인 구간(Cluster)을 이루는 경향이 있다. 이를 **런(Run)**이라고 부르며, 계수 방식은 이 런을 `[Start, Length]` 쌍으로 압축한다.

**[ASCII 다이어그램: 계수 방식의 논리/물리 매핑]**

```text
[관리 테이블 (In-Memory or On-Disk)]
┌──────────────────────────────────────┐
│ Entry 1: [ Start: 100, Count: 3 ]    │ ──┐
├──────────────────────────────────────┤   │
│ Entry 2: [ Start: 500, Count: 10 ]   │   │ mapping
├──────────────────────────────────────┤   │
│ Entry 3: [ Start: 800, Count: 5 ]    │   │
└──────────────────────────────────────┘   │
                                            ▼
         [Physical Disk Block Layout]
100(B), 101(B), 102(B), 103(Used), ... , 500(B), 501(B), ... , 509(B), 510(Used)...

(Allocation Request: Need 2 blocks)
→ System checks Entry 1 (Count 3 >= 2)
→ Allocates Block 100, 101
→ Update Entry 1: [ Start: 102, Count: 1 ] (Remaining)
```

**[해설]**
1.  **압축 효과**: 1000개의 연속된 빈 블록을 관리하기 위해 단 2개의 변수(Start, Count)만 필요하므로 메모리 효율이 극대화된다. 이는 **RLE (Run-Length Encoding)** 압축 알고리즘의 원리와 동일하다.
2.  **할당 알고리즘 (Best-Fit/First-Fit)**:
    *   파일 시스템은 `FreeList`를 순회하며 `Count >= Request_Size`인 첫 번째 엔트리를 찾는다(First-Fit).
    *   할당 후 남은 공간이 있다면 엔트리를 분할(Split)하여 갱신한다.
3.  **단편화 관리**: 파일이 중간에 삭제되어 구간이 나뉘면 `[Start, Count]` 엔트리가 2개로 늘어난다(External Fragmentation 발생). 이를 해결하기 위해 주기적으로 **디스크 조각 모음 (Defragmentation)**을 수행하여 엔트리를 병합(Merge)해야 한다.

**[핵심 알고리즘: 계수 방식의 분할(Split) 및 병합(Merge)]**

```c
struct FreeEntry {
    unsigned int start_addr;
    unsigned int count;
};

// 할당 시 분할 (Split) 로직 예시
void allocate_block(struct FreeEntry* entry, int req_size) {
    if (entry->count > req_size) {
        // 요청한 만큼만 할당하고, 시작 주소를 뒤로 미루며 개수를 줄임
        entry->start_addr += req_size;
        entry->count -= req_size;
    } else {
        // 딱 맞거나 부족하면 엔트리 자체를 제거 (linked list에서 노드 삭제)
        remove_entry(entry);
    }
}

// 해제 시 병합 (Coalescing) 로직 예시
void free_block(unsigned int start, unsigned int count) {
    struct FreeEntry* prev = find_previous_entry(start);
    struct FreeEntry* next = find_next_entry(start);
    
    // 앞뒤 빈 공간과 연속되면 하나로 합침
    if (prev && (prev->start_addr + prev->count == start)) {
        prev->count += count;
        start = prev->start_addr; // 뒤쪽 병합을 위해 start 갱신
        count = prev->count;
        // 필요 시 prev 노드 제거 로직 추가
    }
    
    if (next && (start + count == next->start_addr)) {
        next->start_addr = start;
        next->count += count;
    } else {
        add_new_entry(start, count);
    }
}
```
*(코드는 개념적 구현을 보여주며, 실제 커널 코드는 Doubly Linked List와 Tree 구조를 복합적으로 사용한다.)*

📢 **섹션 요약 비유**: 그룹화는 "휴대폰 단체 문자장"처럼 연락처를 통째로 보관하는 것이고, 계수는 "기차의 대절"처럼 1번 칸부터 50번 칸까지 한 줄로 묶어서 관리하는 것과 같습니다. 기차 대절표(계수)는 승객 명단(그룹화)보다 훨씬 가볍고 관리가 간단합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 분석

| 분석 지표 | 연결 리스트 (Linked List) | 그룹화 (Grouping) | 계수 (Counting) |
|:---|:---|:---|:---|
| **검색 속도 (Search)** | $O(N)$ (매우 느림) | $O(N/GroupSize)$ (개선됨) | $O(Entries)$ (매우 빠름) |
| **공간 오버헤드** | 블록당 1 포인터 | 블록당 N 포인터 | 엔트리당 {Start, Count} |
| **연속 할당 유리성** | 낮음 | 중간 | **매우 높음** |
| **구현 복잡도** | 단순 | 중간 | 복잡 (Split/Merge 로직 필요) |
| **외부 단편화** | 심함 | 보통 | 적음 (연속 공간 보존 유도) |

#### 2. 타 과목 융합 분석 (OS & Database & Network)

**[ASCII 다이어그램: 시스템 간 공간 관리 철학 비교]**

```text
+------------------+------------------------+--------------------------+
|    File System   |      Database (DBMS)   |     Network (TCP)        |
+------------------+------------------------+--------------------------+
| Counting Method  |       Extents          |     Sliding Window       |
| [Start, Count]   |  [PageID, Length]      |   [SeqNo, WindowSize]    |
|                  |                        |                          |
| Disk Blocks      |  Data Pages            |  Receive Buffer          |
+------------------+------------------------+--------------------------+
| Goal: Minimize   |  Goal: Sequential I/O  |  Goal: Flow Control      |
| Fragmentation    |  for Table Scan        |  (Avoid Overflow)        |
+------------------+------------------------+--------------------------+
```

**[융합 서술]**
1.  **데이터베이스 (DBMS)와의 시너지**:
    *   오라클(Oracle)이나 MySQL의 InnoDB 스토리지 엔진은 **Extents**를 사용한다. 이는 계수 방식의 확장된 버전으로, 연속된 데이터 페이지(Blocks)를 묶어서 관리한다. 이를 통해 **Table Scan** 시 디스크 헤드가 이동하는 횟수를 최소화하여 Sequential I/O 성능을 높인다.
2.  **네트워크 프로토콜 (TCP/IP)과의 연관성**:
    *   TCP의 **흐름 제어 (Flow Control)**나 **슬라이딩 윈도우 (Sliding Window)** 기법은 송수신 버퍼의 공간을 `[Start Seq, Window Size]`로 관리한다. 이는 계수 방식과 동일한 철학으로, "연속된 공간의 크기"를 미리 약속함으로써 통신 오버헤드를 줄이는 전략이다.
3.  **메모리 관리 (OS Memory)**:
    *   **Buddy System (버디 시스템)**은 2의 제곱 크기로 블록을 분할/병합하지만, 기본적으로 연속된 공간을 관리한다는 점에서 계수 방식의 목표와 일맥상통한다.

📢 **섹션 요약 비유**: 계수 방식은 네트워크의 "고속도로 통행료"와 같습니다. 고속도로는 차 1대마다 톨게이트를 설치하지 않고, '진입 지점'과 '이동 거리'를 기반으로 통행료를 정산하여 병목을 없앱니다. 이처럼 연산 횟수를 줄이는 것이 핵심입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 트리

**시나