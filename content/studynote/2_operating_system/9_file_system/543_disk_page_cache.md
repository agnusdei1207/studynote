+++
title = "[디스크 캐시 (Disk Cache) 및 페이지 캐시 (Page Cache)]"
date = "2026-03-14"
[extra]
weight = 543
title = "543. 디스크 캐시 (Disk Cache) 및 페이지 캐시"
+++

# [디스크 캐시 (Disk Cache) 및 페이지 캐시 (Page Cache)]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디스크 캐시와 페이지 캐시는 CPU (Central Processing Unit)와 디스크(HDD/SSD) 사이의 현격한 속도 차이(Gap)를 해소하기 위해 주기억장치(RAM)를 데이터 중간 저장소로 활용하는 완충(Buffer) 메커니즘이다.
> 2. **가치**: 시스템 호출(System Call) 오버헤드와 물리적 디스크 탐색(Seek) 지연을 제거하여 I/O 처리량(Throughput)을 1,000배 이상 향상시키며, 애플리케이션의 응답 시간(Latency)을 획기적으로 단축한다.
> 3. **융합**: 가상 메모리(Virtual Memory) 시스템과 통합되어 페이지(Page) 단위로 관리되며, Read-Ahead 기술과 Write-Back 전략을 통해 OS 커널의 성능을 극대화한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**
디스크 캐시는 광의로는 디스크 성능을 높이기 위한 모든 캐싱 기술을 의미하지만, 현대 OS (Operating System) 관점에서는 주로 **페이지 캐시 (Page Cache)**를 지칭합니다. 페이지 캐시는 파일 시스템(File System)의 데이터뿐만 아니라 메타데이터(Metadata)까지 포함하여, 보조기억장치의 내용을 페이지(Page, 보통 4KB) 단위로 메인 메모리(RAM)에 복사해두는 소프트웨어 계층입니다. 이는 단순한 임시 저장소를 넘어, 커널이 파일 I/O를 처리하는 핵심 창구 역할을 수행합니다.

**💡 비유: 사무실과 원격 창고**
CPU를 사무실의 직원, RAM을 책상, 디스크를 먼 곳에 있는 창고라고 생각해봅시다. 책상(RAM)에 자주 쓰는 서류(데이터)를 꺼내두면, 매번 창고(디스크)까지 왔다 갈 필요가 없어 업무 속도가 비약적으로 빨라집니다. 만약 책상이 꽉 차면, 덜 중요한 서류는 다시 창고로 보내거나(Reclaim) 폐기합니다.

**등장 배경: 메모리 월(Memory Wall)과 I/O 병목**
1.  **기존 한계**: CPU의 연산 속도는 무어의 법칙에 따라 기하급수적으로 발전했지만, 기계적 회전이나 플래시 읽기가 필요한 디스크의 속도는 그에 미치지 못해 심각한 병목이 발생했습니다.
2.  **혁신적 패러다임**: **지역성 (Locality)** 원리(최근 접근한 데이터는 다시 접근할 가능성이 높음)를 발견하고, 남는 RAM을 **캐시(Cache)**로 적극 활용하는 자원 관리 정책이 도입되었습니다.
3.  **현재의 비즈니스 요구**: 빅데이터 분석 및 고트래픽 웹 서비스는 디스크 지연 시간(Latency)을 허용하지 않으며, OS 차원의 투명한 캐싱은 필수적인 성능 보장 장치가 되었습니다. 데이터베이스와 같은 애플리케이션 계층에서도 이를 우회하거나 재활용하는 방식으로 최적화를 시도합니다.

```text
[ Performance Gap Evolution ]

CPU Speed  ++++++++++++++++++++++++++++++++++++++ (Exponential Growth)
           |                                    |
           |          [Memory Wall]             |
           |          Gap Widens                |
Disk Speed ++++++++++++++++++++++++++++++++++++++ (Linear Growth)
           ^          ^           ^             ^
           1980s      1990s       2000s         2020s
           
[ Solution: Page Cache ]
Uses free RAM (DRAM) to hide the Disk Latency gap.
```

**📢 섹션 요약 비유**
> 마치 도서관에서 **'자주 대출하는 책을 복사본을 만들어 열람실 비치대(RAM)에 두는 것'**과 같습니다. 독자가 책을 요청하면 서고(디스크)까지 가는 대신 비치대에서 즉시 가져다주므로 대기 시간이 사라집니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Architecture & Mechanism)

페이지 캐시는 단순한 저장소가 아니라, 가상 메모리 주소 공간과 물리적 프레임을 매핑하는 복잡한 커널 서브시스템입니다. 리눅스 커널은 이를 관리하기 위해 `address_space` 객체, `radix tree`, 그리고 `page` 구조체를 사용합니다.

**구성 요소 (Component)**

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/구조 (Protocol/Struct) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **address_space** | 가상 주소와 페이지 매핑 관리 | inode와 페이지 테이블을 연결하는 컨테이너 | struct address_space | 도서관 목록 |
| **Page Cache** | 실제 데이터 저장소 (Physical Frame) | 디스크 블록 내용을 저장한 물리적 메모리 페이지 | struct page (Radix Tree Node) | 책장의 책 |
| **Dirty Page** | 수정된 페이지 추적 | 쓰기 작업이 발생하여 디스크와 내용이 달라짐 | PG_dirty Flag | 수정 필요한 서류 |
| **VFS (Virtual File System)** | 추상화 계층 | Ext4, XFS 등 서로 다른 파일 시스템의 통합 인터페이스 제공 | file_operations, dentry | 사서 시스템 |
| **Page Fault Handler** | 캐시 미스(Miss) 처리 | 데이터가 부재할 때 디스크 I/O 트리거 및 복구 | do_page_fault() | 주문 발생 직원 |

**아키텍처 다이어그램 (ASCII Diagram)**

애플리케이션이 데이터를 요청했을 때, OS 커널 내부에서 일어나는 흐름은 다음과 같습니다. `read()` 시스템 호출이 발생하면 커널은 먼저 페이지 캐시를 확인합니다.

```text
+----------------+        System Call (read/write)        +-------------------+
|  Application   | -------------------------------------> | System Call Interface|
|   (User Mode)  | <------------------------------------- | (Kernel Entry)     |
+----------------+          Return Data / Status          +---------+---------+
                                                                     |
                                                                     v
                 +-------------------------------------------------------------+
                 |                   OS Kernel (VFS Layer)                     |
                 |  +-------------------------------------------------------+  |
                 |  |   1️⃣ Lookup (address_space -> radix_tree)            |  |
                 |  |    "Is this page in memory?"                          |  |
                 |  +-------------------------------------------------------+  |
                 |                         |                                    |
                 |          +------------- YES ------------+   +---- NO ----+     |
                 |          v                             v   v            |     |
                 |   [ Cache HIT ]                  [ Cache MISS ]           |     |
                 |          |                             |                 |     |
+----------------+          v                             v                 v     v
|  Hardware   |   +---------------------------+   +-----------------+   +--------------+
|   (RAM)     |   | 2️⃣ Page Cache (RAM)       |   | 3️⃣ I/O Scheduler |   |  4️⃣ Disk     |
+-------------+   |    - Copy Data to User    |   |   (Elevator/CFQ) |   |  (HDD/SSD)   |
| Page Frames |   |    - Update Access Time  |   +--------+--------+   +--------------+
+-------------+   +---------------------------+            |     (Load Block)
                                                        |           |
                                                        +<----------+
```

**심층 동작 원리 (Deep Dive)**
페이지 캐시의 작동은 크게 '읽기(Read)'와 '쓰기(Write)' 경로로 나뉩니다.

1.  **Lookup (탐색)**: VFS는 요청한 파일의 오프셋(Offset)을 페이지 번호로 변환하고, **Radix Tree** 구조를 통해 해당 페이지가 물리 메모리에 있는지 $O(1)$에 가까운 시간에 검색합니다.
2.  **Hit (적중) & Copy-on-Write**: 페이지가 메모리에 있다면, 데이터를 복사하여 사용자 공간(User Space) 버퍼로 반환합니다. 이 과정에서 `mmap()`을 사용했다면 별도의 복사 없이 메모리 매핑만 수행하여 성능을 높입니다.
3.  **Miss (실패) & Read-Ahead**: 페이지가 없다면 **Page Fault(페이지 부재)**가 발생합니다. 이때 커널은 단순히 요청한 페이지만 가져오는 것이 아니라, **Read-Ahead (Sequential Read)** 기법을 통해 인접한 여러 페이지를 예측하여 미리 읽어옵니다. 이는 디스크의 탐색 시간(Seek Time)을 최소화하여 순차 읽기 성능을 비약적으로 향상시킵니다.
4.  **Write (쓰기) & Dirtying**: 데이터 기록 시 즉시 디스크에 쓰지 않고 페이지 캐시의 내용을 수정한 뒤, 해당 페이지를 **Dirty(더티)** 상태로 표시합니다. 실제 디스크 기록은 백그라운드의 `pdflush` 또는 `kworker` 스레드에 의해 나중에 일괄 처리(Write-Back)됩니다.

**핵심 알고리즘 및 코드 스니펫**
페이지 캐시의 검색 속도는 Radix Tree에 의존합니다. Linux Kernel의 `find_get_page` 매크로는 다음과 같은 논리로 동작합니다.

```c
// Conceptual Linux Kernel Logic for Cache Lookup
struct page *find_get_page(struct address_space *mapping, unsigned long offset) {
    // 1. Search the Radix Tree for the page corresponding to the offset
    struct page *page = radix_tree_lookup(&mapping->page_tree, offset);

    // 2. If found (HIT), increment reference count to prevent eviction
    if (page) {
        get_page(page);
    }
    
    // 3. Return page pointer (NULL if Miss)
    return page;
}
```

**📢 섹션 요약 비유**
> 마치 **'대형 도매 마트의 계산대 벨트 컨베이어'**와 같습니다. 바코드를 찍어 상품(페이지)을 찾으면(Hit) 즉시 출구로 보내고, 없으면(Miss) 창고에서 가져와 컨베이어에 올립니다. 또한, 계산이 완료된 상품(쓰기 완료)은 즉시 트럭에 싣지 않고 잠시 옆에 쌓아두었다가 트럭이 꽉 차면 한꺼번에 실어 보냅니다(Write-Back).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

페이지 캐시는 시스템의 다른 계층과 유기적으로 상호작용하며, 지연(Latency)과 처리량(Throughput) 사이의 트레이드오프를 관리합니다. 특히 가상 메모리(Virtual Memory) 시스템과의 경쟁 관계는 시스템 성능 튜닝의 핵심입니다.

**1. 쓰기 전략 심층 비교 (Write Strategies)**

| 비교 항목 (Metric) | Write-Through (통과 쓰기) | Write-Back (지연 쓰기) |
|:---|:---|:---|
| **정의 (Definition)** | 데이터를 캐시와 디스크에 동시에 기록 | 데이터를 캐시에만 기록 후 일괄 디스크 반영 |
| **데이터 무결성 (Consistency)** | ★★★★★ (캐시와 디스크 항상 일치) | ★★☆☆☆ (Flush 전까지 불일치 상태 존재) |
| **쓰기 성능 (Write Speed)** | ★★☆☆☆ (디스크 I/O 속도에 종속적) | ★★★★★ (메모리 속도로 즉시 완료 응답) |
| **손실 위험 (Risk)** | 없음 (No Risk) | 정전 시 Dirty Page 손실 가능 |
| **활용처 (Use Case)** | 금융 DB 등 강한 일관성이 요구될 때 | 일반 파일 시스템 (Linux Default), 로그 |

**2. 메모리 관리와의 융합 (Convergence with VM)**
페이지 캐시는 **가상 메모리(Virtual Memory)**의 스왑(Swap) 영역과 경쟁 관계에 놓입니다. RAM이 부족할 경우, OS는 캐시된 페이지를 해제(Reclaim)해야 합니다.
-   **Anonymous Memory**: 프로세스의 힙(Heap), 스택(Stack) 등 파일에 백업되지 않은 메모리입니다. 부족 시 Swap 영역으로 내보내집니다.
-   **Page Cache**: 파일에서 읽은 데이터입니다. 단순히 폐기(Evict)해도 디스크에 원본이 있으므로 Swap 비용이 들지 않습니다.

```text
[ Memory Reclaim Strategy (kswapd daemon) ]

   +---------------------+
   |     Available RAM   |
   +---------------------+
           ^ Low Watermark
           |
   +-------+-------+  <--- kswapd WAKE UP
   |               |
   v               v
+-------+     +-------+
|  LRU  |     |  LRU  |
| Active|     |Inactive|
+-------+     +-------+
   ^             ^
   |             +---- ▶ [Evict First] (Page Cache mostly)
   |                   Why? No swap I/O needed, just drop.
   |
   +---------------- ▶ [Swap Out] (Anonymous Memory)
                      Expensive (Disk I/O required)
```

위 그림과 같이 OS는 메모리 부족 시(Page Fault 발생 시), Swap I/O 비용이 드는 익명 메모리보다 페이지 캐시를 먼저 해제하려 시도합니다.

**정량적 지표 분석 (Metrics)**
-   **Cache Hit Ratio**: 캐시 적중률이 95% 이상일 때, I/O 성능은 순수 메모리 접근 수준에 근접합니다.
-   **Page Fault Rate**:
    -   **Soft Fault (Minor Fault)**: 페이지가 이미 캐시에 있으나, Page Table Entry만 업데이트하면 되는 경우 (매우 빠름).
    -   **Hard Fault (Major Fault)**: 디스크 로드가 필요한 경우 (느림, ms 단위).
    -   *목표*: Hard Fault Rate을 0에 가깝게 만드는 것이 OS 튜닝의 핵심입니다.

**📢 섹션 요약 비유**
> 쓰기 전략은 **'메신저 앱의 송신/수신 여부'**와 같습니다. Write-Through는 "전송 완료" 표시가 떠야 용건을 끝내는 신중함이 있고(안전하지만 느림), Write-Back은 일단 "보내기"만 누르고 나중에 배달되는 빠른 처리 방식입니다(빠르지만 중간에 연결 끊기면 사라질 수 있음).

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 환경에서 페이지 캐시의 동작을 이해하지 못하면 "남는 메모리가 �