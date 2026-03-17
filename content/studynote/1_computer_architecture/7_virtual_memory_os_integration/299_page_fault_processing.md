+++
title = "페이징(Paging) 시스템의 핵심 메커니즘= 페이지 폴트 처리 과정 심화 분석"
date = "2026-03-14"
+++

# 페이징(Paging) 시스템의 핵심 메커니즘= 페이지 폴트 처리 과정 심화 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**= 페이지 폴트(Page Fault)는 가상 메모리(Virtual Memory) 관리의 핵심 인터럽트로, 논리적 주소 공간의 페이지가 물리적 프레임에 없을 때 발생하여 OS(Operating System)가 이를 동적으로 해결하는 과정이다.
> 2. **가치**= 메모리 낭비를 최소화하는 요구 페이징(Demand Paging)을 실현하며, 프로세스에게 물리 메모리 크기의 제약을 넘어선 연속적인 주소 공간을 제공하여 다중 프로그래밍 정도(Multiprogramming Level)를 극대화한다.
> 3. **융합**= TLB(Translation Lookaside Buffer) 미스, 디스크 I/O 스케줄링, 프로세스 스케줄링(Context Switching)과 연결되는 시스템 성능의 병목 지점이며, 최신 하드웨어에서는 MMU(Memory Management Unit)와 OS 커널의 협력으로 마이크로초(µs) 단위의 지연을 최적화한다.




## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
페이지 폴트(Page Fault)는 **CPU (Central Processing Unit)** 가 특정 가상 주소(Virtual Address)를 참조할 때, 해당 주소에 해당하는 페이지가 현재 **주 메모리 (Main Memory, RAM)** 에 적재되어 있지 않아 **MMU (Memory Management Unit)** 가 발생시키는 예외(Exception) 또는 인터럽트(Trap)를 의미한다.
이는 가상 메모리 시스템의 근간을 이루는 '요구 페이징(Demand Paging)' 전략의 필연적인 산출물이다. 시스템은 프로세스의 모든 코드/데이터를 메모리에 올리는 대신, 실행 흐름上 실제로 필요해지는 시점에 페이지를 로드(Load)함으로써 한정된 물리 자원을 효율적으로 분배한다.

### 2. 등장 배경 및 기술적 필요성
① **물리 메모리의 한계**: 과거와 달리 현대의 애플리케이션(게임, AI, 빅데이터 등)은 TB 단위의 데이터를 다루려 하지만, 물리적으로 장착 가능한 RAM은 한정되어 있다.
② **추상화의 필요성**: 개발자는 물리 메모리의 부재를 신경 쓰지 않고, 마치 무한한 메모리가 존재하는 것처럼 프로그래밍해야 한다.
③ **효율적인 자원 관리**: 실행되지 않는 코드를 메모리에 유지하는 것은 낭비이다. OS는 페이지 폴트를 통해 각 페이지의 '참조 시점(Reference Time)'을 정확히 포착하고, 가장 적절한 타이밍에 메모리를 할당하여 시스템 처리량(Throughput)을 극대화한다.

### 3. 내부 동작의 철학
페이지 폴트는 시스템의 '실패(Fail)'가 아니라 '기회(Opportunity)'이다. 이는 커널(Kernel)에게 "이 페이지가 실제로 사용되는 순간이다"라는 강력한 신호를 보내며, 이를 통해 동적 메모리 할당, **COW (Copy-On-Write)** 구현, 메모리 맵 파일(Memory-Mapped File) 로딩 등의 복잡한 작업을 수행한다.

> 📢 **섹션 요약 비유**
> 마치 거대한 도서관에서 독자가 책을 요청하면, 사서가 보관 창고(디스크)에서 해당 책을 꺼내어 서가(RAM)에 비치하고 독자에게 건네주는 **'예약 대출 서비스'**와 같습니다. 독자는 책이 어디에 있든 항상 가질 수 있다고 생각하지만, 실제로는 요청하는 순간에 비로소 준비가 완료됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

페이지 폴트 처리는 하드웨어(MMU)와 소프트웨어(OS Kernel)의 긴밀한 협업이 요구되는 고도로 설계된 프로세스이다. 이 과정은 나노초(ns) 단위의 메모리 접근과 밀리초(ms) 단위의 디스크 I/O가 혼재하는 병목 구간이다.

### 1. 구성 요소 상세 분석
| 구성 요소 | 전체 명칭 | 역할 및 내부 동작 | 프로토콜/특징 |
|:---:|:---|:---|:---|
| **MMU** | Memory Management Unit | CPU가 생성한 가상 주소를 물리 주소로 변환. Page Table의 Valid/Invalid 비트를 검사하여 폴트 유무를 결정함. | 하드웨어 회로, TLB 캐시 활용 |
| **Page Table** | Page Table | 가상 주소(VPN) → 물리 주소(PFN) 매핑 정보 저장. **PTE (Page Table Entry)** 내의 Valid Bit, Dirty Bit, Reference Bit 관리. | 커널 메모리 영역 관리 |
| **Swap Space** | Backing Store | 물리 메모리에서 쫓겨난 페이지들이 임시 저장되는 디스크 영역. 페이지 폴트 발생 시 데이터 원본으로 활용됨. | 파일 시스템과 독립적 (Swap Partition) |
| **Page Fault Handler** | Kernel Routine | 인터럽트가 발생하면 호출되는 OS 루틴. 물리 메모리 여부 확인, 희생자(Victim) 선정, 디스크 I/O 요청을 수행함. | 소프트웨어 인터럽트 처리 루틴 |
| **Frame Allocator** | Physical Memory Manager | 물리 메모리의 빈 프레임(Free Frame) 목록을 관리하며, 부족 시 Page Replacement Algorithm을 가동하여 공간 확보. | Buddy System, Slab Allocator 등 |

### 2. 페이지 폴트 처리 절차 (Data Flow & State Transition)

아래 다이어그램은 페이지 폴트 발생 시 하드웨어와 OS가 상호작용하여 메모리 매핑을 완료하는 전체 수명 주기를 도식화한 것이다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PAGE FAULT HANDLING SEQUENCE                             │
└─────────────────────────────────────────────────────────────────────────────┘

[ CPU Context ]                [ Hardware MMU ]                [ OS Kernel ]
   (User Mode)                      (Trap)                        (Kernel Mode)

  ┌─────────┐    VA             ┌─────────────┐                 ┌──────────────┐
  │ Process │ ────────────────> │  TLB Lookup │ ───(Miss)─────> │  Interrupt   │
  │         │                   │   (Cache)   │                 │  Controller  │
  └─────────┘                   └─────────────┘                 └──────┬───────┘
        ▲                             │                             │
        │                             v                             │
        │                    ┌─────────────┐                      │
        │                    │   Page      │                      │
        │          (Valid=0) │   Table     │ ───(Trap)─────────────┤
        │                    │   Access    │                      │
        │                    └─────────────┘                      │
        │                                                          │
        │                                                          ▼
        │                                                 ┌─────────────────┐
        │                                                 │ Fault Handler    │
        │                                                 │ (Software)       │
        │                                                 │ 1. Address Check │
        │                                                 │ 2. Find Frame    │
        │                                                 └───────┬─────────┘
        │                                                         │
        │                                                         v
        │                                                 ┌─────────────────┐
        │                                                 │ Physical Mem    │
        │                                                 │ ┌───┬───┬───┐   │
        │                                                 │ │   │   │   │   │
        │                                                 │ └───┴───┴───┘   │
        │                                                 │ [Free? No]      │
        │                                                 │ └──────┬────────┘
        │                                                         │
        │                                                         v
        │                                                 ┌─────────────────┐
        │                                                 │ Replacement     │
        │                                                 │ Algorithm       │
        │                                                 │ (LRU/NRU)       │
        │                                                 └───────┬─────────┘
        │                                                         │
        │                  Swap-In                               v
        │                   <────┐                   ┌─────────────────┐
        │                        │                   │ Disk I/O        │
        │                        │                   │ (Blocking Op)   │
        │                        │                   └─────────────────┘
        │                        │
        │  Update Table          │
        │  (Valid=1)             │
        │  <────┐                │
        │       │                │
        └───────┴────────────────┘
            Restart Instruction
```

### 3. 심층 동작 원리 (Step-by-Step)

1. **Address Translation & Trap**: CPU가 가상 주소를 생성하면 MMU는 먼저 TLB를 확인하고, 실패 시 Page Table을 접근한다. 이때 해당 PTE의 **Valid Bit (유효 비트)** 가 '0'인 것을 확인하면, 하드웨어는 즉시 OS 커널에 **페이지 폴트 예외(Page Fault Exception)**를 발생(Trap)시킨다.
2. **OS Context Save & Handler Invoke**: 현재 실행 중이던 프로세스의 상태(PCB, Registers)를 스택에 저장하고, 유저 모드(User Mode)에서 커널 모드(Kernel Mode)로 전환하여 페이지 폴트 핸들러 루틴으로 진입한다.
3. **Validity Check**: OS는 해당 가상 주소가 프로세스의 논리적 주소 공간 내에 있는 유효한 주소인지 검사한다. (잘못된 주소 접근 시 Segmentation Fault 발생)
4. **Frame Allocation (Swap-in Strategy)**:
   - 여유 프레임(Free Frame) 리스트가 있다면 즉시 할당.
   - 없다면, **페이지 교체 알고리즘 (Page Replacement Algorithm)** 을 실행하여 희생 페이지(Victim Page)를 선정한다.
   - 희생 페이지가 수정된 상태(**Dirty Bit = 1**)라면, 디스크에 **Write-back(Swap-out)** 후 프레임을 확보한다.
5. **Disk I/O (Scheduling)**: 디스크 컨트롤러에 I/O 요청을 전송하여 Backing Store에서 필요한 페이지를 읽어온다. 이때 프로세스는 **I/O Wait** 상태로 전환되어 CPU를 양보한다(Preemption).
6. **Table Update & Mapping**: I/O 완료 인터럽트를 받으면, 해당 페이지가 적재된 물리 프레임 번호(PFN)를 Page Table Entry에 기록하고 Valid Bit를 '1'로 설정한다. 동시에 TLB도 업데이트된다.
7. **Instruction Restart**: 프로세스 상태를 **Ready** 상태로 이동시키고, 이전 인터럭션이 발생했던 명령어(IP)를 처음부터 다시 실행(Restart)한다.

### 4. 핵심 알고리즘 및 코드 (C Pseudo Code)
아래는 OS 커널 내부의 페이지 폴트 처리 로직을 단순화한 의사코드이다.

```c
// OS Kernel: Page Fault Handler Routine
void handle_page_fault(CPU_Context* context, VirtualAddress vaddr) {
    // 1. 주소 유효성 검사 (Legal Access Check)
    if (!is_valid_address(vaddr, current_process->pcb)) {
        send_signal(SIGSEGV, current_process); // Segmentation Fault
        return;
    }

    // 2. 물리 프레임 확보 (Frame Allocation Strategy)
    PhysicalFrame* pframe = get_free_frame();
    if (pframe == NULL) {
        // 3. 페이지 교체 (Page Replacement)
        pframe = select_victim_frame(); // Algorithm: LRU, FIFO, Clock, etc.
        
        // 4. Dirty Check & Swap-out
        if (pframe->pte->dirty_bit == 1) {
            disk_write(pframe->pte->backing_store_addr, pframe->data);
        }
        update_page_table(pframe->pte, INVALID); // Invalidate victim
    }

    // 5. 디스크에서 페이지 로드 (I/O Operation)
    // 이 함수는 블로킹(Blocking) 형태로 동작하며 디스크 I/O를 수행
    disk_read(vaddr->backing_store_addr, pframe->data);

    // 6. 페이지 테이블 업데이트 (Mapping Update)
    PageTableEntry* pte = get_pte(vaddr);
    pte->frame_number = pframe->id;
    pte->valid_bit = 1;
    pte->dirty_bit = 0;
    pte->reference_bit = 1;

    // TLB Flush (Entry Refresh)
    tlb_flush(vaddr);

    // 7. 프로세스 재개 (Resume)
    restore_context_and_restart(context);
}
```

> 📢 **섹션 요약 비유**
> 책이 서가에 없다는 신호(트랩)를 받은 도서관 사서(OS)는, 빈 서가(프레임)가 없다면 이용이 적은 책을 한 권 골라 창고로 반납시키고(Swap-out), 그 자리에 손님이 원하는 책을 꺼내와 꽂아둔 뒤(디스크 I/O), 대장 장부(페이지 테이블)를 수정하고 손님에게 다시 책을 읽으라 권하는(명령어 재시작) 고도의 업무 프로세스입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

페이지 폴트는 운영체제의 독립된 기능이 아니라, 하드웨어 구조, 시스템 성능, 다른 리소스 관리 기법과 밀접하게 상호작용한다.

### 1. 심층 기술 비교: Major Fault vs. Minor Fault
페이지 폴트는 항상 디스크 접근을 수반하는 것은 아니다. 성능 영향력에 따라 다음과 같이 분류된다.

| 비교 항목 | 마이너 폴트 (Minor Fault / Soft Fault) | 메이저 폴트 (Major Fault / Hard Fault) |
|:---|:---|:---|
| **발생 조건** | 페이지가 물리 메모리에 **이미 존재**하지만, 현재 프로세스의 페이지 테이블에 매핑되지 않음 | 페이지가 물리 메모리에 **없음**. 반드시 **Backing Store(디스크)**에서 로드해야 함 |
| **I/O 발생** | 없음 (No Disk I/O) | 있음 (Disk Read Required) |
| **지연 시간 (Latency)** | 수마이크로초 (µs) 수준 (메모리 복사 및 테이블 업데이트만) | 수밀리초 (ms) 수준 (디스크 탐색/회전 지연 포함) |
| **주요 원인** | 포크(Fork) 후 공유 라이브러리 연결, **COW (Copy-on-Write)** 초기 매핑 | 실제 실행 흐름에 따른 첫 로드, 메모리 부족에 따른 스왑 아웃 후 재참조 |
| **성능 영향** | 무시할 수 있을 정도로 적음 | 시스템 성능 저하(Slowdown) 및 **Thrashing** 유발 가능성 높음 |

### 2. 과목 융합 관점 분석
페이지 폴트 처리는 컴퓨터 시스템의 다른 영역과 어떤 시너지와 트레이드오프를 가지는가?

- **[컴퓨터 구조 & OS] TLB (Translation Lookaside Buffer)와의 관계**:
    TLB는 가상 주소 → 물리 주소 변환 결과를 캐싱하는 하드웨어이다.