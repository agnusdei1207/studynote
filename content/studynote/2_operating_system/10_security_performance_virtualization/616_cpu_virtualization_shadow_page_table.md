+++
title = "616. CPU 가상화 및 섀도 페이지 테이블 (Shadow Page Table)"
date = "2026-03-14"
weight = 616
+++

# 616. CPU 가상화 및 섀도 페이지 테이블 (Shadow Page Table)

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**CPU 가상화 (CPU Virtualization)** 환경에서 가장 큰 난관 중 하나는 메모리 주소 공간의 **이중 추상화 (Double Abstraction)** 문제입니다. 전통적인 시스템에서 운영체제(OS)는 **MMU (Memory Management Unit)**를 통해 가상 주소(VA, Virtual Address)를 물리 주소(PA, Physical Address)로 변환합니다. 그러나 가상화 환경에서 게스트 OS(Guest OS)가 인식하는 '물리 주소'는 실제 하드웨어의 물리 주소가 아닌, 하이퍼바이저가 할당한 **가상의 물리 주소(GPA, Guest Physical Address)**입니다.

여기서 **섀도 페이지 테이블 (Shadow Page Table, SPT)**은 하이퍼바이저가 이러한 주소 변환의 간극을 메우기 위해 구축하는 소프트웨어적 기술입니다. 하이퍼바이저는 게스트 OS가 관리하는 페이지 테이블을 감시하고, 이를 바탕으로 **GVA (Guest Virtual Address)**를 실제 메모리 주소인 **HPA (Host Physical Address)**로 직접 매핑하는 또 다른 페이지 테이블(그림자 테이블)을 생성하여 CPU에 로드합니다.

### 2. 등장 배경 및 필요성
- **① 기존 한계**: x86 아키텍처의 초기 MMU는 하드웨어적으로 주소 변환을 한 단계(VA → PA)만 지원했습니다. 따라서 **GVA → GPA → HPA**와 같은 2단계 변환을 하드웨어가 처리할 수 없었습니다.
- **② 혁신적 패러다임**: 하드웨어의 지원 없이 순수 소프트웨어적으로 이 문제를 해결하기 위해, 하이퍼바이저가 게스트 OS가 변경하는 페이지 테이블을 실시간으로 가로채어(Copy-on-Write), CPU가 곧바로 이해할 수 있는 '합성된 페이지 테이블'을 동적으로 만들어내는 방식이 고안되었습니다.
- **③ 비즈니스 요구**: VMware와 같은 초기 가상화 솔루션은 기존 하드웨어를 수정 없이 가상화를 구현해야 하는 과제를 안고 있었으며, SPT는 이를 가능하게 한 핵심 기술이었습니다.

### 3. ASCII 다이어그램: 주소 공간의 중첩 구조
아래 다이어그램은 가상화 환경에서 메모리 주소가 어떻게 분리되고 중첩되는지를 시각화한 것입니다.

```text
[ Application View ]       [ Guest OS View ]          [ Hypervisor View ]      [ Hardware ]
-------------------        -----------------          ------------------      -------------
Process A (GVA)    --->    Guest Phy. Mem.     --->    Host Phy. Mem.     --->   RAM
0x00400000                0x80000000 (GPA)            0x7F000000 (HPA)
(Virtual)                 (Physical to Guest)         (Real Physical)
```

> **[다이어그램 해설]**
> 1. **Application View**: 애플리케이션은 **GVA**를 사용하며, 자신이 연속된 메모리를 갖는다고 생각합니다.
> 2. **Guest OS View**: 게스트 OS는 자신이 물리 메모리(**GPA**)를 직접 관리한다고 믿지만, 이는 실제 물리 주소가 아닙니다.
> 3. **Hypervisor View**: 하이퍼바이저는 실제 하드웨어 주소(**HPA**)를 관리하며, GPA와 HPA 간의 매핑을 책임집니다.
> 4. **Hardware**: 최종적으로 CPU는 HPA를 통해 실제 RAM에 액세스합니다.

📢 **섹션 요약 비유**: 이 구조는 마치 "호텔 객실 번호표(GVA)"를 가진 손님이, "호텔 건물 내부 번호(GPA)"를 찾아갔는데 그곳이 실제로는 "지적도상의 번호(HPA)"와 다른 복잡한 연결 구조를 가진 건물과 같습니다. 섀도 페이지 테이블은 이 복잡한 연결을 손님께는 보이지 않게 처리하는 호텔 VIP 관리자와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 역할 (Component Table)
섀도 페이지 테이블 시스템을 구성하는 핵심 요소들은 다음과 같습니다.

| 요소명 | 전체 명칭 (Abbreviation) | 역할 | 내부 동작 메커니즘 | 비고 |
|:---|:---|:---|:---|:---|
| **GPT** | Guest Page Table | 게스트 OS가 관리하는 페이지 테이블 | 게스트 커널에 의해 GPA로 매핑 정보 관리 | 읽기 전용(RO) 설정 대상 |
| **SPT** | Shadow Page Table | 하이퍼바이저가 생성하는 '그림자' 테이블 | GVA → HPA의 1:1 직접 매핑 정보 저장 | CPU의 CR3 레지스터에 로드 |
| **CR3** | Control Register 3 | 페이지 테이블 베이스 주소 레지스터 | 현재 실행 중인 프로세스의 페이지 테이블 포인터 저장 | **VM Entry** 시 SPT 주소로 교체 |
| **VMCS** | Virtual Machine Control Structure | 가상 머신의 상태 및 제어 정보 저장 | 게스트 상태(CR3 등)와 호스트 상태를 분리 저장 | Intel VT-x 기반 |
| **TLB** | Translation Lookaside Buffer | 주소 변환 결과 캐시 | 최근 변환된 GVA→HPA 매핑을 캐싱 | SPT 교체 시 Flush 필요 |

### 2. 섀도 페이지 테이블 동작 메커니즘 (Synchronization)
섀도 페이지 테이블의 핵심은 게스트 OS가 자신의 페이지 테이블(GPT)을 수정할 때, 이를 감지하여 하이퍼바이저의 SPT에도 반영하는 **동기화(Synchronization)** 과정입니다.

```text
[Timing Diagram: Page Fault Handling & Sync]

Guest OS                       Hypervisor (VMM)                Hardware (CPU)
    |                               |                               |
    | 1. Try Write to GPT           |                               |
    |------------------------------>|                               |
    |                               |                               |
    |                          2. [VM-EXIT] Trigger!              |
    |                          (Page Fault on Read-Only GPT)       |
    |                               |                               |
    |                          3. Emulate Write                   |
    |                          - Update Guest's GPT (in GPA)      |
    |                          - Calculate HPA mapping             |
    |                          - Update SPT (GVA -> HPA)          |
    |                               |                               |
    |                               | 4. Flush TLB (Invalidate)     |
    |                               |------------------------------->|
    |                               |                               |
    | 5. Resume Execution (VM-Entry)|                               |
    |<------------------------------|                               |
    | 6. Retry Access (using SPT)   |                               |
    |------------------------------>| 7. Hit in SPT (HPA mapped)     |
    |                               |                               |
```

> **[다이어그램 해설]**
> 1. **트리거(Trigger)**: 게스트 OS가 커널 모드에서 자신의 페이지 디렉터리(GPT)를 수정하려 하면, 하이퍼바이저가 미리 GPT를 **쓰기 금지(Write-Protect)** 상태로 두었기 때문에 **VM-Exit**가 발생합니다.
> 2. **에뮬레이션(Emulate)**: 하이퍼바이저는 게스트가 GPT에 쓰려고 했던 내용을 분석하여, 게스트 메모리(GPA) 상의 GPT 내용을 갱신하고, 동시에 실제 하드웨어가 사용할 SPT(GVA->HPA) 항목도 갱신합니다.
> 3. **TLB 플러시**: 변경된 매핑 정보가 반영되도록 TLB를 무효화합니다.
> 4. **재개(Resume)**: 게스트 OS에게 명령어가 실행된 것처럼 속여 컨텍스트를 돌려주면, 이후 메모리 접근은 갱신된 SPT를 통해 HPA로 직행합니다.

### 3. 핵심 알고리즘 및 코드 (C 스타일 의사코드)
SPT 동기화의 핵심 로직을 간소화하여 표현합니다.

```c
// Hypervisor SPT Sync Logic (Pseudo-code)
void handle_page_table_sync(Guest_Context* ctx, GVA fault_addr) {
    // 1. 게스트가 쓰려고 했던 GPT 엔트리 위치 확인
    GPA target_gpa = get_guest_page_table_base(ctx) + get_page_offset(fault_addr);
    
    // 2. 게스트 의도대로 GPT(메모리 상) 업데이트 (GPA -> GPA mapping)
    // *Note: 실제로는 게스트 메모리 공간에 쓰기 수행
    write_guest_memory(ctx, target_gpa, ctx->new_pte_value);

    // 3. HPA(Real Machine) 매핑 정보를 조회하여 SPT 엔트리 생성/갱신
    HPA real_hpa = translate_gpa_to_hpa(target_gpa);
    
    // 4. SPT(GVA -> HPA) 엔트리 갱신
    // CR3는 현재 SPT를 가리키고 있음
    update_spt_entry(ctx->cr3_shadow, fault_addr, real_hpa, FLAGS);
    
    // 5. TLB 일관성 유지를 위한 Flush
    asm volatile ("invlpg %0" : : "m" (fault_addr));
}
```

📢 **섹션 요약 비유**: 섀도 페이지 테이블 관리는 마치 "고속도로 톨게이트의 하이패스 차선"과 같습니다. 운전자(게스트 OS)는 그냥 통과하면 된다고 생각하지만, 실제로는 뒤쪽 관제실(하이퍼바이저)에서 차량 번호(GVA)를 실제 출발지/도착지(HPA) 정보로 실시간 매핑하여 요금을 정산하고 차단기를 올립니다. 차량이 차선을 바꿀 때마다 관제실이 이를 즉시 반영해야 사고(충돌)가 나지 않습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술적 비교: Shadow PT vs. Hardware-Assisted (EPT/NPT)
순수 소프트웨어 방식(SPT)과 하드웨어 가속 방식(EPT)의 비교는 가상화 성능 논의의 핵심입니다.

| 비교 항목 | 섀도 페이지 테이블 (Shadow PT) | 하드웨어 중첩 페이지 테이블 (EPT/NPT) |
|:---|:---|:---|
| **매핑 구조** | **Single Mapping**: GVA -> HPA (합쳐진 테이블) | **Nested Mapping**: GVA -> GPA (Guest PT), GPA -> HPA (EPT) |
| **주요 병목** | 높은 **VM-Exit 빈도**: 페이지 테이블 변경 시마다 트랩 발생 | 낮은 **VM-Exit 빈도**: EPT Miss 시에만 발생 |
| **메모리 오버헤드** | 높음: 프로세스마다 별도 SPT 유지 필요 | 낮음: 호스트는 하나의 EPT만 유의 (공유 가능) |
| **구현 복잡도** | 매우 높음: 복잡한 트랩/에뮬레이션 로직 필요 | 낮음: 하드웨어가 2차 변환 처리 |
| **전환 비용(Context Switch)** | 높음: CR3 교체 시 TLB Flush 필수적 | 낮음: VPID와 같은 태그로 TLB 공유 가능 |
| **대표 플랫폼** | 초기 VMware, Binary Translation | Intel VT-x + EPT, AMD-V + RVI |

### 2. ASCII 다이어그램: 주소 변환 비교 (Walk-through)
두 방식의 변환 경로(Walk) 차이를 시각화합니다.

```text
[ Shadow PT (Software) ]
 GVA ──────────────> SPT (Shadow Page Table)
 └─[Hardware Walk]─┘        │
                           └─> HPA (Direct Mapping)
                           
(특징: CPU는 하나의 테이블만 걸음. 하지만 테이블을 유지하는 비용이 큼)


[ Hardware EPT (Assisted) ]
 GVA ──> Guest PT ──> GPA ──> EPT ──> HPA
 └─Walk1─┘        │      └─Walk2─┘
                 │
(특징: 2단계 Walk. CPU가 자동으로 처리. 하이퍼바이저 개입 최소화)
```

> **[다이어그램 해설]**
> - **Shadow PT**: 하이퍼바이저가 미리 "지름길(SPT)"을 만들어둡니다. CPU는 SPT만 보면 되므로 실행 속도는 빠르지만, 지름길을 최신으로 유지하는 관리 비용(오버헤드)이 극도로 높습니다.
> - **Hardware EPT**: "중간 경로(Guest PT)"와 "실제 경로(EPT)"를 분리했습니다. CPU가 2단계를 자동으로 탐색하므로 관리가 쉽고 효율적입니다.

### 3. 타 과목 융합 분석
- **OS (Operating System)**: 페이지 폴트(Page Fault) 처리 핸들러의 원리를 이해해야 하지만, 가상화 환경에서는 이 폴트가 실제 메모리 부족 때문인지, 혹은 SPT 동기화를 위한 트랩(Trap)인지를 **이중으로 판별**해야 하는 로직이 추가됩니다.
- **컴퓨터 구조 (Computer Architecture)**: **TLB (Translation Lookaside Buffer)**의 성능이 가상화 성능을 좌우합니다. SPT 방식에서는 CR3가 교체될 때마다 TLB를 모두 지워야(Flush) 하는 문제가 있어 **VPID (Virtual Processor Identifier)** 기술과 같은 하드웨어적 보완이 필요해집니다.

📢 **섹션 요약 비유**: 섀도 페이지 테이블은 "통역가가 통역문을 미리 만들어두는 방식"이고, EPT는 "실시간 동시 통역 기계"를 도입한 것과 같습니다. 미리 만들어두는 방식은 나중에 수정이 생기면(페이지 테이블 변경) 문서를 다시 출력해야 하지만(오버헤드), 동시 통역 기계는 화자가 말하는 대로 즉시 처리하므로 훨씬 효율적입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정
**상황**: 레거시 하드웨어(Intel VT-x 지원 이전 CPU 또는 EPT 미지원 환경)에서 서버 가상화를 구축해야 하는 상황.
- **문제**: 하드웨어적인 2차 주소 변환(Nested Paging)이 불가능하여 순수 소프트웨어 가상화(BT + SPT)를 사용해야 함.
- **결과**: 가상 머신(VM) 생성 및 메모리 할당 시 높은 지연(Latency) 발생.