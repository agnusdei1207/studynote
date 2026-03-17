+++
title = "527. 할당 방법 (Allocation Methods) - 연속 할당 (Contiguous Allocation)"
date = "2026-03-14"
weight = 527
+++

# 527. 할당 방법 (Allocation Methods) - 연속 할당 (Contiguous Allocation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 연속 할당(Contiguous Allocation)은 파일 시스템(File System)에서 파일의 데이터 블록들이 디스크 상의 물리적으로 인접한 연속된 섹터(Sector)나 블록(Block)에 배치되는 가장 직관적인 할당 기법입니다. 이는 메모리 관리의 연속 할당 기법과 논리적으로 동일합니다.
> 2. **가치**: **랜덤 액세스(Random Access)**가 가능하며, 순차 읽기(Sequential Read) 시 디스크 헤드(Head)의 이동인 **탐색 시간(Seek Time)**이 최소화되어 **전송률(Transfer Rate)**이 극대화됩니다. 매핑을 위한 메타데이터 오버헤드가 거의 없다는 것이 가장 큰 장점입니다.
> 3. **융합**: 그러나 **외부 단편화(External Fragmentation)** 문제와 파일 크기의 동적 변경(Pre-allocation 필요) 이슈로 인해, 일반 범용 OS(Windows, Linux 등)의 주된 파일 시스템에서는 배제되었으나, ISO 9660(CD-ROM), SSD FTL(Flash Translation Layer)의 로그 구조, 혹은 고성능 데이터베이스의 고정 크기 테이블스페이스管理等 특수 목적으로 여전히 활용됩니다.




### Ⅰ. 개요 (Context & Background)

연속 할당은 각 파일에 대해 디스크 상의 **연속적인 주소 공간(Contiguous Address Space)**을 할당하는 방식입니다.
이 방식의 핵심 철학은 "물리적 배치와 논리적 배치의 일치"에 있습니다. 사용자가 파일의 n번째 바이트를 요청하면, 시스템은 단순한 산술 연산을 통해 즉시 물리적 위치를 계산할 수 있습니다.

#### 1. 기술적 배경 및 역사
초기 컴퓨팅 환경에서는 디스크 공간 관리의 단순성이 무엇보다 중요했습니다. 연속 할당은 파일 시스템의 관리 자료구조(File Allocation Table, inode 등)를 최소화할 수 있어 자원이 제한적인 환경에서 효율적이었습니다. 하지만 파일의 생성과 삭제가 반복됨에 따라 디스크 곳곳에 빈 공간(Hole)이 발생하는 **외부 단편화**가 심각한 성능 저하의 원인이 되었으며, 이를 해결하기 위해 **압축(Compaction)** 기술이 연구되었습니다.

#### 2. 작동 원리 (Operating Mechanism)
파일 시스템은 파일 생성 시, 해당 파일의 크기를 정확히 알거나 예측해야 합니다. 디렉터리 엔트리에는 파일의 이름과 함께 **시작 주소(Starting Block Number)**와 **길이(Length, Blocks)**만 저장됩니다. 이를 통해 O(1)의 시간 복잡도로 접근이 가능합니다.

#### 3. 연속 할당의 디스크 레이아웃 시각화

```text
[ Logical File System View vs. Physical Disk Layout ]

[Logical File]           [Physical Disk Blocks (Linear Address Space)]
File A (Size 4)          [Block 0] [Block 1] [Block 2] [Block 3] ...
| Data 1 |   =======>    |  A-D1   |  A-D2   |  A-D3   |  A-D4   |
| Data 2 |
| Data 3 |
| Data 4 |

[Directory Structure Mapping]
+------------------+----------------+----------+
| File Name        | Start Address  | Length   |
+------------------+----------------+----------+
| File A           |       0        |    4     |
| File B           |      10        |    3     |
+------------------+----------------+----------+
```
> **도해 해설**: 위 다이어그램은 논리적인 파일의 순서가 물리적인 디스크 블록 번호와 1:1로 매핑되는 모습을 보여줍니다. 인덱싱을 위한 별도의 복잡한 테이블이 필요 없이, 시작점과 길이만 있으면 전체 영역을 즉시 파악할 수 있습니다.

📢 **섹션 요약 비유**: 연속 할당은 **"기차 객차 연결"**과 같습니다. 서울(시작 주소)에서 부산(끝 주소)까지 가는 기차는 객차들이 떨어지지 않고 순서대로 연결되어 있어야 합니다. 기차의 번호표(길이 정보)만 보면 몇 호 객차에 누가 타 있는지 바로 알 수 있죠. 하지만 객차를 중간에 끼워 넣으려면 전체 기차를 밀어내고 자리를 만들어야 하는 단점이 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

연속 할당 시스템의 성능과 안정성은 디스크 스케줄링과 밀접하게 관련되어 있으며, 주소 변환 알고리즘이 매우 단순합니다.

#### 1. 구성 요소 및 상세 기술

| 요소 명칭 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 관련 파라미터/프로토콜 |
|:---|:---|:---|:---|
| **디렉터리 엔트리**<br>(Directory Entry) | 파일 메타데이터 저장 | 파일명, **시작 주소(Start Address)**, **길이(Length)**를 저장. 별도의 FAT(File Allocation Table) 불필요. | Block No, File Size (bytes) |
| **디스크 공간 관리자**<br>(Disk Space Manager) | 가용 공간 탐색 및 할당 | First-Fit, Best-Fit 등의 알고리즘을 사용해 연속된 빈 영역(Hole)을 검색. | Free List, Bit Vector |
| **접근 방식 모듈**<br>(Access Method) | 논리 주소 → 물리 주소 변환 | `Physical_Addr = Start + Logical_Offset` 산술 연산 수행. | LBA (Logical Block Addressing) |
| **I/O 컨트롤러**<br>(I/O Controller) | 물리적 데이터 전송 | Sequential Access 시 Seek Time 없이 Track/Cylinder를 따라 연속 읽기. | SATA, NVMe, SCSI Command Set |

#### 2. 주소 변환 알고리즘 및 코드

연속 할당의 가장 강력한 무기는 O(1)의 주소 계산입니다. 링크드 리스트(Linked Allocation)나 인덱스(Indexed Allocation)와 달리 포인터 추적(Indirection)이 없습니다.

```c
/* 
 * Pseudo-code: Contiguous Allocation Address Translation
 * No indirection overhead exists.
 */

// Define File Metadata
typedef struct {
    char filename[256];
    int  start_block;    // Physical Starting Block Number
    int  length_blocks;  // Total File Length in Blocks
} FileEntry;

// Function to translate Logical Byte Offset to Physical Block Number
// Args: file_meta, logical_offset (byte)
// Returns: Physical Block Number, Offset within Block
void get_physical_address(FileEntry *file, long logical_offset, int *phy_blk, int *blk_off) {
    int BLOCK_SIZE = 4096; // 4KB
    
    // 1. Check boundaries
    if (logical_offset >= file->length_blocks * BLOCK_SIZE) {
        handle_error("Access Violation: Offset exceeds file size");
    }

    // 2. Direct Arithmetic Calculation (The Core Strength)
    // No disk I/O needed to find the location (unlike Linked Lists)
    *phy_blk = file->start_block + (logical_offset / BLOCK_SIZE);
    *blk_off = logical_offset % BLOCK_SIZE;
    
    // Result is immediately ready for Disk Driver
}
```

#### 3. 디스크 헤드 동작 및 I/O 패턴 분석

연속 할당은 회전 지연(Rotational Latency)과 탐색 시간(Seek Time)을 최소화합니다.

```text
[ Disk Head Movement Analysis: Sequential Read ]

[Track 0]  [Track 1]  [Track 2]  [Track 3]
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Block 0 │→│Block 1 │→│Block 2 │→│Block 3 │  (Continuous Logical Flow)
└────────┘ └────────┘ └────────┘ └────────┘
     ↑                                         
  [Head]  --- Minimal Seek (Cylinder Switch) --> 

vs.

[ Fragmented Layout (Linked/Indexed) ]
[Track 0]        [Track 5]        [Track 2]
┌────────┐       ┌────────┐       ┌────────┐
│Block 0 │ ────→ │Block 1 │ ────→ │Block 2 │  (Random Seek Jumps)
└────────┘       └────────┘       └────────┘
     ▲                ▲                 ▲
   [Head] --------Long Seek---------> [Head]
```
> **도해 해설**: 위 다이어그램은 연속 할당(상단)과 불연속 할당(하단)의 디스크 헤드 이동 궤적을 비교합니다. 연속 할당은 헤드가 물리적으로 인접한 트랙을 순서대로 읽으며 데이터 전송 대역폭을 100% 활용하지만, 불연속 할당은 데이터를 읽기 위해 헤드가 왔다 갔다(Thrashing)하며 엄청난 기계적 지연을 유발합니다.

📢 **섹션 요약 비유**: 연속 할당의 주소 변환은 **"좌석 배치표"**와 같습니다. "A열 1번부터 10번까지 예약"이라는 정보만 있으면, 5번째 손님이 어디에 앉아 있는지 더할 것도 없이 바로 알 수 있습니다. 굳이 1번 자리에 가서 "다음 사람은 2번에 있어"라고 물어볼 필요가 없는 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

연속 할당은 성능 면에서는 최강이지만, 공간 효율성 면에서는 가장 취약한 방식입니다. 이를 타 할당 방식과 정량적으로 비교 분석합니다.

#### 1. 파일 할당 방식 심층 비교 (Quantitative Analysis)

| 비교 항목 (Metric) | 연속 할당 (Contiguous) | 연결 할당 (Linked) | 색인 할당 (Indexed) | 비고 및 분석 |
|:---|:---|:---|:---|:---|
| **접근 속도 (Access Speed)** | **매우 빠름 (O(1))**<br>Direct Access 지원 | 느림 (O(N))<br>순차 접근만 유리 | 보통 (O(1)~O(Indirection))<br>Small Index 접근 빠름 | DBMS, 실시간 시스템에서 Contiguous 선호 |
| **디스크 공간 효율 (Space Eff.)** | **낮음 (External Frag.)** | 높음 (No Int. Frag.)<br>포인터 오버헤드 존재 | 높음 (No Ext. Frag.)<br>Index Block 소모 | 외부 단편화(External Fragmentation)가 치명적 약점 |
| **파일 확장 (File Expansion)**| **어려움**<br>Pre-allocation 필요 | 유연함 | 매우 유연함 | 동적으로 커지는 로그 파일에는 부적합 |
| **신뢰성 (Reliability)** | 취약 (하나의 손상=전체 손상) | 취약 (포인터 끊어짐) | **높음** (다중 링크 가능) | RAID와 결합 시 신뢰성 확보 가능 |
| **구현 복잡도 (Complexity)**| **단순** | 단순 | 복잡 | 임베디드 시스템에서는 단순함이 장점 |

#### 2. OS/Architecture 융합 관점

1.  **OS와의 관계 (OS Integration)**:
    *   **메모리 관리(Memory Management)와의 유사성**: 연속 할당은 메모리의 **MFT(Multiprogramming with Fixed Number of Tasks, 고정 분할)** 방식과 논리적으로 동일합니다. 프로세스가 연속적인 메모리를 필요로 하듯, 파일도 연속적인 디스크 블록을 요구합니다. 따라서 **Compaction(메모리 압축)** 기술이 디스크에도 동일하게 적용될 수 있으나, 디스크의 대용량(GB~TB)으로 인해 압축에 드는 비용(Cost)이 매우 크다는 문제가 있습니다.
    *   **캐시 효과**: 연속 할당은 **Read-ahead(선반입)** 기법과 시너지가 극대화됩니다. CPU 캐시 라인(Cache Line)이 데이터를 가져올 때 연속된 바이트를 가져오는 것처럼, 디스크 컨트롤러도 연속된 블록을 예측하여 버퍼로 미리 가져오기 때문입니다.

2.  **데이터베이스(DBMS)와의 시너지**:
    *   현대의 DBMS(Oracle, MySQL 등)는 **Tablespace**나 **Datafile** 단위로 공간을 할당받을 때, OS 파일 시스템의 할당 방식과 무관하게 내부적으로 **Extent(연속된 블록 묶음)** 단위로 데이터를 관리합니다. 이는 연속 할당의 성능 이점을 소프트웨어적으로 시뮬레이션하는 것입니다.

#### 3. 할당 알고리즘 성능 분석 (Placement Strategy)

빈 공간을 관리하는 전략에 따라 외부 단편화 발생 정도가 달라집니다.

```text
[ Free Space Management Strategies ]

[Memory Layout Example]
| Used (10) | [Free (50)] | Used (20) | [Free (15)] | Used (30) |
            ▲                         ▲
         Start A                   Start B

Request: Allocate 40 Blocks

1. First-Fit (최초 적합)
   - Action: Allocate at Start A.
   - Result: [Free (50)] -> [Used (40)] + [Free (10)]
   - Pros: Fast decision.
   - Cons: Leaves small fragments at the beginning.

2. Best-Fit (최적 적합)
   - Action: Search entire list. Allocate at Start A (Size 50 is closer to 40 than Start B 15? No, Start B is too small).
   - Wait, Start B is too small (15 < 40). So A is the only choice.
   - Scenario Change: If Start A was 45 and Start B was 100.
     First-Fit -> A (Leaves 5)
     Best-Fit -> A (Leaves 5)
   - Comparison with Worst-Fit: Worst-Fit would pick the Largest hole (B).
```
> **도해 해설**: 최초 적합(First-Fit)은 가장 먼저 발견되는 곳에 할당하여 속도가 빠르지만, 앞쪽 공간에 작은 자투리 공간을 남기는 경향이 있습니다. 최악 적합(Worst-Fit)은 가장 큰 공간을 깨부수어 할당하므로, 남는 공간이 커서 나중에 할당 가능성이 높아지지만, 큰 덩어리를 유지하기 어렵게 만듭니다.

📢 **섹션 요약 비유**: 연속 할당의 공간 관리는 **"피자 판 자르기"**와 같습니다. 피자(디스크)가 통으로 있을 때는 누구나 크게 떼어 먹을 수 있지만(First-Fit), 먹다 남은 조각들(External Fragmentation)이 여기저기 널려 있으면, 배가 고픈 사람(새 파일)은 자신보다 작은 조각