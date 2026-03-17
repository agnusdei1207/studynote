+++
title = "확장 페이지 테이블 (Extended Page Table, EPT)"
date = "2026-03-14"
weight = 661
+++

# 확장 페이지 테이블 (Extended Page Table, EPT)

## # 확장 페이지 테이블 (Extended Page Table, EPT)
### 핵심 인사이트 (3-Line Summary)
> 1. **본질**: 하드웨어 지원 가상화(Hardware-Assisted Virtualization) 환경에서 게스트 운영체제(Guest OS)가 관리하는 **게스트 물리 주소(Guest Physical Address, GPA)**를 호스트(Hypervisor)가 관리하는 실제 **호스트 물리 주소(Host Physical Address, HPA)**로 변환하는 하드웨어 기반의 2차원 주소 변환(2-Dimensional Paging) 메커니즘입니다.
> 2. **가치**: 기존 소프트웨어 기반의 그림자 페이지 테이블(Shadow Page Table, SPT) 방식에서 발생하던 빈번한 **VM Exit(Virtual Machine Exit)** 오버헤드를 근본적으로 제거하여, 가상 머신(Virtual Machine, VM)의 메모리 액세스 성능을 네이티브(Native) 수준으로 끌어올립니다.
> 3. **융합**: TLB(Translation Lookaside Buffer) 가상화 기술인 VPID(Virtual Processor Identifier)와 결합하여 캐시 일관성을 유지하며, 최근에는 TDX(Trust Domain Extensions) 및 SEV-SNP(Secure Encrypted Virtualization-Secure Nested Paging) 등의 **기밀 컴퓨팅(Confidential Computing)** 아키텍처의 핵심 요소로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background) - [600자+]

확장 페이지 테이블(Extended Page Table, EPT)은 x86 아키텍처에서의 가상화 성능 병목을 해결하기 위해 Intel VT-x(Virtualization Technology for x86)와 함께 도입된 하드웨어 기반 메모리 가상화 솔루션입니다. 가상화 환경의 주소 변환은 본질적으로 '이중(Double)' 구조를 가집니다. 게스트 운영체제(Guest OS)는 가상 주소(GVA, Guest Virtual Address)를 게스트 물리 주소(GPA)로 변환하고, 하이퍼바이저(Hypervisor)는 이 GPA를 다시 실제 물리 메모리 주소인 호스트 물리 주소(HPA)로 변환해야 합니다.

EPT가 등장하기 전에는 그림자 페이지 테이블(Shadow Page Table, SPT)이라는 소프트웨어적 기법이 사용되었습니다. SPT는 하이퍼바이저가 Guest OS의 페이지 테이블을 감시하고, 변경될 때마다 실제 물리 주소로 매핑된 '가짜(SHADOW)' 테이블을 동기화하는 방식입니다. 이 방식은 Guest OS가 페이지 테이블을 수정할 때마다 하이퍼바이저로 제어권이 넘어가는 트랩(Trap), 즉 **VM Exit**를 유발하여 막대한 컨텍스트 스위칭 오버헤드를 초래했습니다.

EPT는 이러한 소프트웨어의 개입을 배제하고, CPU의 MMU(Memory Management Unit)가 GPA $\rightarrow$ HPA 변환을 자체적으로 수행하도록 설계되었습니다. 이를 통해 Guest OS는 자신의 페이지 테이블을 자유롭게 수정하면서도 하이퍼바이저의 개입 없이 메모리에 액세스할 수 있게 되었습니다. AMD의 경우 이를 NPT(Nested Page Table) 또는 RVI(Rapid Virtualization Indexing)라고 명명하며 동일한 개념을 적용합니다.

#### 💡 개념 비유
국제 회의에서 통역사가 필요 없는 '실시간 번역 이어폰'을 생각하면 됩니다.
*   **SPT (구조)**: 발표자(Guest OS)가 말을 할 때마다 통역사(Hypervisor)가 개입하여 통역을 번역하고 대본을 수정(Sync)하느라 발표가 자주 끊김. (느림)
*   **EPT (구조)**: 발표자와 참가자가 모두 '실시간 번역 이어폰(Hardware)'을 착용하여, 발표자의 말(High-level language)이 즉시 상대방의 언어(Low-level machine code)로 변환되어 전달됨. (빠름)

```text
       [ Memory Virtualization Evolution ]
┌─────────────────────────────────────────────────────────────┐
│ 1. Software Shadowing (SPT)                                 │
│                                                             │
│    Guest OS:  "Change Page Table Entry"                    │
│          ↓                                                  │
│    CPU TRAP (VM Exit) ⚠️                                    │
│          ↓                                                  │
│    Hypervisor:  "Okay, let me calculate & update shadow..." │
│          ↓ (High Overhead)                                  │
│    Resume Execution                                         │
└─────────────────────────────────────────────────────────────┘
                        ▼ Evolution
┌─────────────────────────────────────────────────────────────┐
│ 2. Hardware Assisted (EPT)                                  │
│                                                             │
│    Guest OS:  "Change Page Table Entry"                    │
│          ↓                                                  │
│    CPU MMU:  "Automatically check GPA -> HPA Mapping"      │
│          ↓ (No Trap, Pure Hardware Speed) ✅                │
│    Resume Execution (Instantaneous)                         │
└─────────────────────────────────────────────────────────────┘
```

> 📢 **섹션 요약 비유**
> 마치 복잡한 세관 통과 절차에서, 매번 직원(소프트웨어)이 여권을 확인하고 도장을 찍는 방식(SPT)에서, 사전 등록된 전용 차선을 통해 센서(하드웨어)가 자동으로 인식하여 통과시키는 '하이패스(EPT)' 시스템으로 업그레이드한 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,200자+]

EPT의 핵심은 기존 x86의 4단계 페이징 구조(CR3 $\rightarrow$ PML4 $\rightarrow$ PDPT $\rightarrow$ PD $\rightarrow$ PT) 위에 또 다른 4단계 페이징 구조를 '중첩(Nested)'시키는 것입니다. 이를 통해 CPU는 메모리 접근 시 두 번의 Walk 과정을 수행합니다.

#### 1. 구성 요소 상세 분석

| 모듈 (Module) | 전체 명칭 (Full Name) | 역할 (Role) | 내부 동작 메커니즘 (Internal Mechanism) | 비고 |
|:---|:---|:---|:---|:---|
| **EPT PML4** | EPT Page Map Level 4 | EPT의 최상위 루트 | **EPTP(EPT Pointer)** 레지스터가 가리키는 테이블로, GPA의 비트 47~39를 인덱스로 사용 | 1개의 EPT는 VM 전체 또는 vCPU에 할당 |
| **EPT PDPT** | EPT Page Directory Pointer Table | 2단계 계층 | 1GB 페이지 매핑 지원 시 PS(Page Size) 비트 사용 | GPA 비트 38~30 사용 |
| **EPT PD** | EPT Page Directory | 3단계 계층 | 2MB Large Page 매핑 지원 | GPA 비트 29~21 사용 |
| **EPT PT** | EPT Page Table | 4단계 계층 (최하위) | 4KB 기본 페이지 단위 매핑, 실제 HPA 프레임 주소 저장 | GPA 비트 20~12 사용 |
| **EPT TLB** | EPT Translation Lookaside Buffer | EPT 전용 캐시 | GPA $\rightarrow$ HPA 변환 결과를 캐싱하여 메모리 접근(Walk) 회수 최소화 | **VPID**와 연동하여 캐시 일관성 유지 |
| **VMCS** | Virtual Machine Control Structure | 제어 상태 저장소 | **EPTP** 값, EPT 활성화 비트('Enable EPT') 등을 저장 | 가상 머신 상태 정의 |

#### 2. 이중 주소 변환 (2-Dimensional Paging) 아키텍처

EPT 환경에서의 메모리 접근은 **논리적 주소 $\rightarrow$ 선형 주소 $\rightarrow$ 물리 주소** 변환 과정이 두 계층에 걸쳐 이루어집니다. 아래 다이어그램은 이 과정을 시각화한 것입니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Logical Address (48-bit) ]                        │
│                             │                                                │
│                             ▼ (Segmentation - rarely used now)              │
│ ┌───────────────────────────────────────────────────────────────────────┐   │
│ │                     [ Linear Address (VA) ]                           │   │
│ │                                                                       │   │
│ │  ┌─── Stage 1 Walk: Guest Paging (Hosted by Guest OS) ────┐          │   │
│ │  │                                                            │          │   │
│ │  │  1. CPU checks Guest CR3 (pointing to Guest PML4)       │          │   │
│ │  │  2. Walks Guest Page Tables (PML4 -> PDPT -> PD -> PT)  │          │   │
│ │  │  3. Result: Guest Physical Address (GPA)                │          │   │
│ │  │                                                            │          │   │
│ │  └────────────────────────────────────────────────────────────┘          │   │
│ │                                  │                                        │   │
│ └──────────────────────────────────┼────────────────────────────────────────┘   │
│                                    ▼                                            │
│ ┌───────────────────────────────────────────────────────────────────────┐   │
│ │                     [ Guest Physical Address (GPA) ]                  │   │
│ │                                                                       │   │
│ │  ┌─── Stage 2 Walk: Extended Paging (Hardware Assisted) ────┐        │   │
│ │  │                                                            │        │   │
│ │  │  1. CPU checks EPTP (pointing to EPT PML4)               │        │   │
│ │  │  2. Walks EPT Tables (EPT PML4 -> EPT PDPT -> EPT PD -> EPT PT) │   │   │
│ │  │  3. Result: Host Physical Address (HPA) / SP (System Physical)  │   │   │
│ │  │                                                            │        │   │
│ │  └────────────────────────────────────────────────────────────┘        │   │
│ │                                  │                                        │   │
│ └──────────────────────────────────┼────────────────────────────────────────┘   │
│                                    ▼                                            │
│ ┌───────────────────────────────────────────────────────────────────────┐   │
│ │                     [ Host Physical Address (HPA) ]                   │   │
│ │                         (Actual DRAM Location)                         │   │
│ └───────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 심층 해설]**
1.  **Guest Walk (1단계)**: Guest OS 입장에서는 자신이 CR3 레지스터를 통해 페이지 테이블을 관리한다고 생각합니다. 이 과정에서 GPA가 도출됩니다. 이때 사용하는 페이지 테이블은 실제 HPA 공간에 존재하지만, Guest OS는 이를 GPA 연속 공간으로 착각합니다.
2.  **EPT Walk (2단계)**: MMU는 도출된 GPA를 기반으로 하이퍼바이저가 설정한 EPT 구조를 순회합니다. 이때 모든 엔트리는 물리 메모리(HPA)에 위치하므로, 메모리 접근이 발생합니다.
3.  **결과**: 최종적으로 HPA가 획득되면 실제 DRAM에 있는 데이터를 읽거나 씁니다. **중요한 점은 이 모든 과정이 하드웨어 파이프라인에 의해 자동으로 수행된다는 점**입니다.

#### 3. EPT 엔트리 구조 및 EPT Violation 처리

EPT 엔트리는 64비트 구조이며, 단순 매핑 정보를 넘어 메모리 보호(Memory Protection)와 성능 최적화 비트를 포함합니다.

```c
/* Intel SDM (Software Developer's Manual) 기반 EPT Entry 구조체 정의 */
struct EPT_Entry {
    uint64_t Read        : 1;    // [Bit 0] 읽기 권한 (0=Block, 1=Allow)
    uint64_t Write       : 1;    // [Bit 1] 쓰기 권한
    uint64_t Execute     : 1;    // [Bit 2] 실행 권한 (NX Bit 기반)
    uint64_t Reserved1   : 5;    // [Bit 3~7] 시스템 예약 영역 (Must be 0)
    uint64_t Accessed    : 1;    // [Bit 8] 접근 비트 (A-bit, HW set)
    uint64_t Dirty       : 1;    // [Bit 9] 수정 비트 (D-bit, HW set)
    uint64_t UserExec    : 1;    // [Bit 10] User Mode 실행 허용 (Ignored in some modes)
    uint64_t PageSize    : 1;    // [Bit 11] 페이지 크기 (0=4KB, 1=2MB/1GB)
    uint64_t Reserved2   : 4;    // [Bit 12~15] Reserved
    uint64_t PFN         : 40;   // [Bit 12~51] HPA Physical Frame Number (Page Base Addr)
    uint64_t Reserved3   : 12;   // [Bit 52~63] 예약 및 소프트웨어 비트
} __attribute__((packed));

/* EPT 위반(EPT Violation) 발생 시 하이퍼바이저 처리 의사코드 */
void handle_ept_violation(uint64_t gpa, uint64_t gva, uint32_t exit_qualification) {
    // 1. EPT 엔트리 조회
    EPT_Entry* entry = walk_ept(gpa);
    
    if (entry == NULL) {
        // Case 1: 페이지가 할당되지 않음 (Demand Paging 시나리오)
        allocate_host_memory_frame(HPA_FRAME);
        map_ept_entry(gpa, HPA_FRAME, READ_WRITE_ACCESS);
        resume_guest_execution();
    } 
    else if (is_write_violation(exit_qualification) && !entry->Write) {
        // Case 2: 쓰기 권한 위반 (Copy-on-Write 또는 보안 훅)
        if (is_cow_page(gpa)) {
            // CoW: 익명 페이지 분리
            private_hpa = copy_page(entry->PFN);
            entry->PFN = private_hpa;
            entry->Write = 1; // 새 페이지에는 쓰기 권한 부여
            flush_ept_tlb();
        } else {
            // 보안 위반 (VM Introspection)
            inject_exception(GUEST_PAGE_FAULT);
        }
    }
}
```

> 📢 **섹션 요약 비유**
> 마치 '이중 잠금장치가 있는 금고'와 같습니다. 첫 번째 잠금(Guest Page Table)은 사용자(Guest OS)가 열 수 있지만, 두 번째 잠금(EPT)은 건물 관리자(Hypervisor)가 보유합니다. EPT는 사용자가 열쇠(Guest PTE)를 돌릴 때마다 관리자가 와서 확인하는 것이 아니라, 열쇠를 돌리면 기계적으로 내부 잠금이 풀리도록 설계된 '전자 금고 시스템'과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [800자+]

EPT는 단순한 가상화 기능을 넘어 운영체제(OS), 컴퓨터 구조(Computer Arch), 보안(Security) 영역과 깊이게 연결됩니다.

#### 1. 심층 기술 비교: SPT vs EPT (정량적 분석)

| 비교 항목 (Criteria) | 그림자 페이지 테이블 (Shadow Page Table, SPT) | 확장 페이지 테이�