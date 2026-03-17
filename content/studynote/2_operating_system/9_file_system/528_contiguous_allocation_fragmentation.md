+++
title = "528. 연속 할당의 문제점 - 외부 단편화 (External Fragmentation)"
date = "2026-03-14"
weight = 528
+++

# 528. 연속 할당의 문제점 - 외부 단편화 (External Fragmentation)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 외부 단편화(External Fragmentation)는 가변 크기 다중 파티션(Multi-partition) 환경에서, 전체 여유 공간은 충분하나 불연속적인 작은 블록(Hole)으로 분산되어 연속 할당을 요구하는 프로세스를 수용할 수 없는 상태를 의미한다.
> 2. **가치**: 시스템 자원의 **이용률(Utilization)**을 50% 이하로 떨어뜨려 **Compaction (압축)** 비용을 발생시키거나, 심각한 경우 OOM(Out of Memory) 상황을 유발하여 **가용성(Availability)**을 저해하는 주요 성능 병목 현상이다.
> 3. **융합**: 물리 메모리 관리의 근본적 한계를 보여주며, **Paging (페이징)**, **Segmentation (세그먼테이션)**, 파일 시스템의 **Linked Allocation (연결 할당)** 등 불연속 할당 기법 도입의 이론적 근거가 된다.

---

### Ⅰ. 개요 (Context & Background) - [Memory Dynamics]

#### 1. 개념 및 정의
**외부 단편화(External Fragmentation)**란 **연속 할당(Contiguous Allocation)** 방식을 사용하는 메모리 관리 시스템(Memory Management System)이나 파일 시스템(File System)에서 발생하는 현상이다. 
물리 메모리(Physical Memory)나 디스크 공간 전체의 합계(Free Space Total)는 새로운 프로세스나 파일을 수용하기에 충분하지만, 가용 공간들이 물리적으로 떨어진 작은 조각(Hole)들의 형태로 존재하기 때문에, 연속된 특정 크기의 공간을 요구하는 할당 요청을 충족시킬 수 없는 상태를 말한다. 

이는 **내부 단편화(Internal Fragmentation)**와 대비되는 개념이다. 내부 단편화는 고정 분할(Fixed Partition) 환경에서 프로세스 크기가 파티션보다 작아 파티션 내부에 남는 공간이 발생하는 것이고, 외부 단편화는 가변 분할(Variable Partition) 환경에서 할당과 해제(Allocation/Deallocation)가 반복되며 생기는 '틈'을 의미한다.

#### 2. 등장 배경 및 문제의 심각성
초기의 단순한 운영체제(Operating System)는 구현의 단순성(Simplicity)과 접근 속도(Access Speed)를 이유로 연속 할당 방식을 채택했다. 하지만 다중 프로그래밍(Multiprogramming) 환경이 고도화되며 다음과 같은 악순환이 발생했다.

1.  **Loading**: 프로세스 A, B, C가 연속적으로 메모리에 적재됨.
2.  **Termination**: 중간에 위치한 프로세스 B가 종료되며 중간에 빈 공간(Hole) 발생.
3.  **Arrival**: 새로운 프로세스 D가 할당을 요청함.
4.  **Issue**: 프로세스 D가 기존의 빈 공간(Hole)보다 크거나, 작은 조각들을 합친 합계는 충분하지만 단일 조각으로는 부족할 경우 할당 불가 상태가 됨.

#### 3. ASCII 다이어그램: 시간에 따른 단편화 진행 과정
아래는 연속 할당 방식에서 시간 경과에 따라 공간이 조각나는 과정을 시각화한 것이다.

```text
[ Timeline: T0 (Initial State - Ordered) ]
┌─────────────────────────────────────────────────────────────────┐
│ Process A      │ Process B      │ Free (Hole)   │ Process C    │
│ Size: 30MB     │ Size: 40MB     │ Size: 50MB    │ Size: 20MB   │
└─────────────────────────────────────────────────────────────────┘
     [ Used ]        [ Used ]          [ Free ]         [ Used ]

[ Timeline: T1 (After Process B & C terminated) ]
┌───────────────────────┬───────────────────────────────────────────┐
│ Process A             │ Free             │ Free                  │
│ Size: 30MB            │ Size: 40MB       │ Size: 20MB            │
└───────────────────────┴───────────────────────────────────────────┘
     [ Used ]                  [ Hole_1 ]              [ Hole_2 ]

[ Timeline: T2 (New Process D & E allocated in Hole_1) ]
┌───────────────┬──────────┬───────────┬─────────────────────────────┐
│ Process A     │ Proc D   │ Proc E    │ Free                        │
│ Size: 30MB    │ Size:20  │ Size:15   │ Size: 5 (Remains) + 20MB    │
└───────────────┴──────────┴───────────┴─────────────────────────────┘
  [ Used ]        [ Used ]    [ Used ]      [ Hole_3 ]  [ Hole_2 ]
  
 👉 Total Free Space = 5MB + 20MB = 25MB
 👉 New Request: Process F (Requires 25MB)
 👉 Result: ALLOCATION FAILED
     (이유: 연속된 25MB 공간이 존재하지 않음. 가장 큰 덩어리는 20MB)
```

**(해설)**
위 다이어그램은 T2 시점에서 전체 여유 공간은 25MB이지만, 이것이 두 개의 떨어진 덩어리(5MB, 20MB)로 나뉘어 있어 25MB짜리 프로세스 F를 할당할 수 없음을 보여준다. 이러한 현상이 반복되면 메모리는 "스위스 치즈(Swiss Cheese)"처럼 구멍이 숭숭 뚫린 형태가 되며, 실제로는 쓸 수 없는 많은 양의 메모리가 방치되는 **External Fragmentation** 상태에 빠지게 된다.

> 📢 **섹션 요약 비유**: 외부 단편화는 "소파 위에 앉고 싶은 세 사람"과 같습니다. 소파 전체 길이에는 세 사람이 다 앉을 수 있는 공간이 충분하지만, 중간에 짐 가방(이미 사용 중인 블록)이 놓여 있어 세 사람이 나란히 앉을 수(연속 할당) 없는 상황과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [Mechanism & Strategies]

#### 1. 구성 요소 및 할당 전략 분석
연속 할당 시스템에서 가용 공간(Hole)을 관리하는 **Dynamic Storage Allocation Problem**의 해결 전략은 외부 단편화의 정도에 직접적인 영향을 미친다. 주요 전략 비교는 다음과 같다.

| 약어 | 전체 명칭 (Full Name) | 동작 원리 (Operation) | 외부 단편화 영향 | 시간 복잡도 |
|:---:|:---|:---|:---:|:---:|
| **FF** | **First-Fit** | 요청 크기를 수용할 수 있는 **첫 번째** 빈 공간을 탐색하여 할당. | 높음 (High) | $O(N) |
| **BF** | **Best-Fit** | 요청 크기를 수용할 수 있는 공간 중 **가장 작은** 공간(잉여 최소화)을 선택. | **매우 높음 (Very High)** | $O(N) |
| **WF** | **Worst-Fit** | 가장 큰 빈 공간에서 할당하여 남는 공간을 충분히 크게 만듦. | 보통 (Moderate) | $O(N) |

#### 2. 심층 분석: Best-Fit의 딜레마 (Knuth's Analysis)
많은 사용자가 "Best-Fit가 내부 낭비를 줄여주므로 효율적일 것이다"라고 착각하지만, **Donald Knuth**는 그의 저서 *The Art of Computer Programming*에서 Best-Fit이 외부 단편화를 악화시킬 수 있음을 증명했다. 
- **메커니즘**: Best-Fit은 요청 크기에 가장 근접한 구멍을 선택한다. 이는 할당 후 남는 잔여 공간(Residue)이 매우 작다는 것을 의미한다.
- **결과**: 이 작은 잔여 공간(Residue)은 향후 대부분의 프로세스 크기보다 작아져 재사용이 불가능한 **Useless Sliver(쓸모없는 조각)**으로 전락한다. 시스템이 오래 운영될수록 이러한 조각들이 메모리 곳곳에 쌓여 가용 공간을 잠식하게 된다.

#### 3. ASCII 다이어그램: 할당 알고리즘 시뮬레이션
동일한 메모리 상태에서 서로 다른 알고리즘이 어떻게 다른 결과를 만들어내는지 시각화한다.

```text
[ Initial Memory State ]
Addresses: 0x0000      0x1000     0x2000     0x3000     0x5000     0x6000
           ┌───────────┬──────────┬──────────┬──────────┬──────────┬───────┐
           │  Used     │  Hole 1  │  Used    │  Hole 2  │  Used    │Hole 3 │
           │  (1KB)    │  (2KB)   │  (1KB)   │  (4KB)   │  (1KB)   │ (3KB) │
           └───────────┴──────────┴──────────┴──────────┴──────────┴───────┘

[ Request: Allocate Process X (Size: 3KB) ]

[ Scenario A: First-Fit ]
  ─────────────────────────────────────────────────────────────────────
  1. Scan Start.
  2. Hole 1 (2KB): Too small. Skip.
  3. Hole 2 (4KB): Fits! Allocate here.
  4. Result State:
     Hole 2 -> [ Proc X (3KB) ] [ Remainder: 1KB ]
     * Generated a new 1KB sliver (likely unusable for large reqs)

[ Scenario B: Best-Fit ]
  ─────────────────────────────────────────────────────────────────────
  1. Scan All Holes: 2KB, 4KB, 3KB.
  2. Candidates: Hole 2 (4KB), Hole 3 (3KB).
  3. Select Hole 3 (3KB) because it is the "tightest" fit.
  4. Result State:
     Hole 3 -> [ Proc X (3KB) ] [ Remainder: 0KB ]
     * No space wasted, but Hole 3 is completely gone.
     * Future requests for >2KB must fight for Hole 2, leading to fragmentation earlier.

[ Scenario C: Worst-Fit ]
  ─────────────────────────────────────────────────────────────────────
  1. Scan All Holes.
  2. Select Hole 2 (4KB) because it is the largest.
  3. Result State:
     Hole 2 -> [ Proc X (3KB) ] [ Remainder: 1KB ]
     * Leaves Hole 3 (3KB) intact for future 3KB requests.
     * Large holes are broken, but large remainder is preserved if possible.
```

**(해설)**
Best-Fit는 3KB 요청에 대해 3KB 구멍(Hole 3)을 완벽히 사용하여 잔여 공간을 0으로 만드는 것처럼 보이나, 이는 시스템의 유연성(Flexibility)을 저해한다. 반면 Worst-Fit는 가장 큰 4KB를 쪼개어 1KB를 남기지만, 3KB 구멍은 그대로 보존하여 향후 3KB 요청이 들어왔을 때를 대비한다. 이처럼 외부 단편화 관리는 "잔여 공간의 크기 분포(Distribution of Hole Sizes)"를 어떻게 유지하느냐의 싸움이다.

#### 4. 핵심 코드: 메모리 블록 관리 자료구조 (C언어)
연속 할당 시스템의 핵심은 메모리 블록을 추적하는 연결 리스트(Linked List)와 분할(Splitting) 로직에 있다.

```c
#include <stdio.h>
#include <stdlib.h>

// 메모리 블록을 표현하는 노드 구조체
typedef struct memory_block {
    size_t size;                      // 블록의 크기 (헤더 포함 여부는 설계에 따름)
    int is_free;                      // 1: Free, 0: Allocated
    struct memory_block *next;        // 다음 블록에 대한 포인터
    void *start_addr;                 // 실제 메모리 시작 주소 (시뮬레이션용)
} block_t;

// First-Fit 할당 함수 구현
void *allocate_first_fit(block_t **head, size_t size) {
    block_t *current = *head;
    block_t *prev = NULL;

    while (current != NULL) {
        if (current->is_free && current->size >= size) {
            // 1. 적합한 공간 발견
            
            // 2. 분할(Splitting) 로직: 
            // 남는 공간이 최소 블록 크기보다 크다면 나눔
            if (current->size > size + sizeof(block_t)) {
                block_t *new_block = (block_t *)((void *)current + sizeof(block_t) + size);
                new_block->size = current->size - size - sizeof(block_t);
                new_block->is_free = 1;
                new_block->next = current->next;
                
                current->size = size;
                current->next = new_block; 
                // 이 로직이 반복될수록 작은 free block들이 리스트 사이사이에 끼어듦 (External Fragmentation 유발)
            }

            current->is_free = 0;
            return current->start_addr;
        }
        prev = current;
        current = current->next;
    }
    return NULL; // Allocation Failed (External Fragmentation)
}
```

> 📢 **섹션 요약 비유**: 이 과정은 "주차장 관리"와 같습니다. First-Fit은 들어오는 차량에게 보이는 첫 번째 빈 주차 공간을 배정합니다. Best-Fit은 차량에 딱 맞는 좁은 공간만 골라서 배정하다가, 나중에 버스가 왔을 때 타격이 큽니다. Worst-Fit은 널찍한 주차 공간에 승용차를 세워서 공간을 낭비하는 것처럼 보이지만, 독수리 차 같은 대형 차량이 올 때를 대비해 넓은 공간을 최대한 보존하려는 전략입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: 외부 단편화 vs 내부 단편화
운영체제 설계 시 가장 중요한 트레이드오프(Trade-off) 중 하나이다.

| 비교 항목 | 내부 단편화 (Internal Fragmentation) | 외부 단편화 (External Fragmentation) |
|:---|:---|:---|
| **발생 환경** | **고정 분할(Fixed Partition)** | **가변 분할(Variable Partition)** |
| **발생 원인** | 프로세스 크기가 블록(페이지) 크기의 배수가 아니어서 발생하는 **내부적 낭비**. | 전체 공간은 충분하나, 공간들이 분산되어 발생하는 **외부적 불연속**. |
| **물리적 위치** | 할당된 메모리 영역 **내부**. | 할당된 메모리 영역 **사이(틈)**. |
| **주요 해결책** | 페이지 크기(Page Size) 감소 (오버헤드 증가). | **Compaction (압축)**, **Paging (