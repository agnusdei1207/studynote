+++
title = "375. 메모리 보호 키 (Memory Protection Keys)"
date = "2026-03-14"
weight = 375
+++

# 375. 메모리 보호 키 (Memory Protection Keys)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존 커널 개입 기반 메모리 보호 방식(`mprotect`)의 성능 병목을, 사용자 공간(User Space)에서 직접 접근 권한을 제어하는 **MPK (Memory Protection Keys)** 하드웨어 기능으로 혁신적으로 개선한 기술입니다.
> 2. **가치**: 시스템 콜(System Call) 오버헤드와 **TLB (Translation Lookaside Buffer)** 플러시 비용을 제거하여, 메모리 보호 경계(Sandboxing)를 유지하면서도 데이터 처리 처리량을 최대 10배 이상 향상시킬 수 있습니다.
> 3. **융합**: 고성능 In-Memory DB, 보안 가상화(Confidential Computing), 웹 브라우저의 렌더링 엔진 보안 등, 보안과 성능의 Trade-off를 극복해야 하는 미래 시스템의 핵심 기반 기술입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**MPK (Memory Protection Keys)**는 x86-64 아키텍처(Intel SKYLAKE 이상, AMD ZEN 이상)부터 도입된 하드웨어 기반 메모리 보호 메커니즘입니다. 전통적인 페이지 테이블의 권한 비트(R/W)를 수정하기 위해서는 커널 모드로 진입하여 `PTE (Page Table Entry)`를 갱신하고, 결과적으로 **TLB Shootdown**이 발생하여 막대한 성능 손실이 발생했습니다.

MPK는 이러한 문제를 해결하기 위해 **PKE (Protection Keys Extensions)**를 활용합니다. 각 메모리 페이지에 4비트의 '키'를 태깅하고, 프로세스(또는 스레드)는 자신만의 **PKRU (Protection Key Register for User)** 레지스터를 조작하여 특정 키를 가진 메모리 영역에 대한 접근을 즉시 차단하거나 허용합니다. 이 모든 과정이 시스템 콜 없이 사용자 모드(User Mode)에서 명령어 한 줄(`WRPKRU`)로 완료됩니다.

#### 2. 등장 배경 및 필요성
① **기존 한계**: 기존 `mprotect()` 시스템 콜은 페이지 테이블을 수정하므로, 멀티코어 환경에서 모든 코어의 **TLB (Translation Lookaside Buffer)**를 무효화(Flush)하는 매우 비싼 연산이 수반되었습니다. 보안을 위한 격리(Sandboxing)가 빈번할수록 성능이 급격히 저하되는 문제가 있었습니다.
② **혁신적 패러다임**: 메모리 맵(페이지 테이블)은 '정적(Static)'으로 유지하되, 접근 권한(Policy)만 '동적(Dynamic)'으로 변경하여 성능 저하 없이 보안 체계를 유지하자는 패러다임의 전환이었습니다.
③ **비즈니스 요구**: 금융권 HTS(High-Performance Trading System), 인메모리 데이터베이스, 웹 브라우저의 보안 샌드박스 등에서 '보안'과 '극한의 성능'을 동시에 달성해야 하는 요구가 급증했습니다.

#### 3. 기술적 구조 및 배경 (ASCII 다이어그램)

```text
[Conventional mprotect() vs MPK Operation Flow]

+-----------------------------+          +----------------------------+
|      CONVENTIONAL METHOD    |          |          MPK METHOD        |
+-----------------------------+          +----------------------------+
| 1. App calls mprotect()     |          | 1. App executes WRPKRU      |
|    (System Call)            |          |    (User Instruction)       |
|           |                  |          |           |                 |
|           v                  |          |           v                 |
| 2. Kernel modifies PTE       |          | 2. CPU updates PKRU Reg     |
|    (Page Table Entry)        |          |    (User Register)          |
|           |                  |          |           |                 |
|           v                  |          |           v                 |
| 3. IPI (Inter-Processor      |          | 3. Permission Check         |
|    Interrupt) to all Cores   |          |    (Hardware Check)         |
|           |                  |          |           |                 |
|           v                  |          |           v                 |
| 4. Global TLB Flush!         |          | 4. Block Access (No Flush)  |
|    <-- [BOTTLENECK]          |          |    <-- [SUPER FAST]         |
+-----------------------------+          +----------------------------+
```

> **해설**: 전통적인 방식은 페이지 테이블(자물쇠 구조)을 바꾸기 위해 모든 코어에 통신(IPI)하고 캐시(TLB)를 비우는 막대한 비용을 지불합니다. 반면, MPK는 자물쇠는 그대로 둔 채 내 손의 열쇠 뭉치(PKRU)만 바꾸는 것이므로 즉시 적용됩니다. 이는 가상 메모리 관리의 기본 전제인 "페이지 속성 변경은 비싸다"는 공식을 깨는 결정적인 차이입니다.

📢 **섹션 요약 비유**:
수천 명의 직원이 출입하는 빌딩의 보안 시스템을 바꾸는 데, 모든 직원에게 방송을 보내고 출입카드를 새로 발급(TLB Flush)하는 기존 방식 대신, 경비실의 **마스터 컴퓨터(PKRU) 설정만 수정하여 특정 구역의 잠금을 즉시 제어하는 것**과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
MPK 시스템은 크게 페이지 테이블의 태깅 정보와 이를 해석하는 CPU 레지스터로 구성됩니다. 아래 표는 각 구성 요소의 역할과 내부 동작을 상세히 명세합니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 상세 (Internal Operation) | 프로토콜/명령어 | 비유 (Analogy) |
| :--- | :--- | :--- | :--- | :--- |
| **PTE (Page Table Entry)** | 메모리 페이지 태깅 | 64비트 엔트리 중 비트 62:59(4비트)를 사용하여 해당 페이지에 0~15번 키(PKey) 할당. 기존 R/W 비트와 무관하게 추가적인 검증 레이어 제공 | 하드웨어 구조 | 문에 부착된 '색상표' |
| **PKRU Register** | 접근 권한 제어 (정책) | 32비트 레지스터(CR4 내의 PKU bit 활성화 필요). 각 키마다 2비트씩 할당(AD: Access Disable, WD: Write Disable) 총 16개 키 관리. 스레드별 독립적인 컨텍스트 유지 | `WRPKRU`, `RDPKRU` | 현관에 있는 '키패드' |
| **MMU (Memory Management Unit)** | 실시간 검증 수행 | 메모리 접근 시, CPU는 TLB Lookup 시 해당 PTE의 Key와 현재 스레드의 PKRU 레지스터 값을 AND 연산하여 권한 확인. 위반 시 즉시 `#PF` (Page Fault) 트랩 발생 | 하드웨어 회로 | 자동문 개폐 시스템 |

#### 2. 하드웨어 레벨 데이터 흐름 (ASCII 다이어그램)
MPK가 동작하는 메커니즘은 **MMU**의 페이지 트래버설 과정에 필터링 로직이 추가되는 것입니다.

```text
[MPK Hardware Checking Flow]

+----------------------+                  +-----------------------+
|   Thread Execution   |                  |   Memory Access Request|
+----------------------+                  +-----------+-----------+
           |                                         |
           v                                         v
+----------------------+                  +-----------------------+
| User Code Executes   |                  | Virtual Address (VA)  |
| "WRPKRU reg, val"    | ---> (Update) -->| PKRU (Per-Thread Reg) |
+----------------------+                  +-----------+-----------+
            |                                          |
            |                                          |
            +<----------------+ (Read Access) <--------+
                               |
                               v
               +-----------------------------------------------+
               |        MMU (Memory Management Unit)            |
               +-----------------------------------------------+
               | 1. TLB Lookup (Get Physical Address & PKey)    |
               |    --> PKey = 5 (from PTE)                     |
               |                                                |
               | 2. Check Permission against PKRU               |
               |    IF (PKRU[Key_5].AD == 1)                    |
               |       --> TRAP (#PF - Page Fault)              |
               |    ELSE IF (PKRU[Key_5].WD == 1 && IS_WRITE)   |
               |       --> TRAP (#PF)                           |
               |    ELSE                                       |
               |       --> ALLOW ACCESS (Permit)                |
               +-----------------------------------------------+
```

> **해설**: 사용자가 `WRPKRU` 명령어를 통해 레지스터를 변경하면, 이는 즉시 현재 스레드의 컨텍스트에 반영됩니다. 이후 메모리 접근 발생 시 MMU는 주소 변환(TLB Lookup)과정에서 읽어온 페이지의 Protection Key 값과, 현재 레지스터의 해당 키 비트를 대조합니다. 레지스터 비트가 '1'로 설정되어 있으면(Disable), 예외(Exception)를 발생시켜 접근을 차단합니다. 즉, 소프트웨어 개입 없이 하드웨어적으로 나노초(ns) 단위의 보안 검사가 수행됩니다.

#### 3. 핵심 알고리즘 및 실무 코드 (Linux API)
리눅스 커널은 `sys/mman.h`를 통해 MPK 기능을 API로 제공합니다.

```c
/*
 * MPK 활용 의사 코드 (Pseudo Code for Fast Protection)
 * 목적: 민감한 데이터 버퍼를 평소에는 읽기 전용(RO)으로 유지하다가,
 *      갱신 필요 시만 순간적으로 쓰기(W)를 허용하여 공격 노출 면적 최소화
 */
#include <sys/mman.h>

// 1. 키 할당: 시스템 전체에서 사용 가능한 PKey 풀에서 하나 확보
//    반환된 pkey_val은 0~15 사이의 정수
int pkey_val = pkey_alloc(0, 0); 

// 2. 메모리 영역 보호: 특정 버퍼(buf)에 pkey_val 적용
//    기존 mprotect와 유사하지만, PTE의 Protection Key 필드를 설정
pkey_mprotect(buf, size, PROT_READ, pkey_val);

// ... [일반적인 로직 처리: 버퍼 읽기 허용] ...

// 3. 쓰기가 필요한 순간: 시스템 콜 없이 레지스터만 변경
//    PKEY_DISABLE_WRITE (0x2)를 해당 키에 설정하여 쓰기 방지
//    레지스터 명령어는 단일 사이클 명령어이므로 오버헤드 무시 가능
unsigned long old_pkru = pkey_set(pkey_val, PKEY_DISABLE_WRITE); 

// --- 민감한 데이터 수정 로직 수행 ---
// 이 시점에 다른 스레드나 잘못된 로직이 buf에 쓰려고 시도하면 SIGSEGV 발생

// 4. 수정 완료 후 즉시 락 재적용 (또는 롤백)
pkey_set(pkey_val, 0); // 다시 쓰기 가능하게 하거나, 락으로 복구
```
> **기술적 포인트**: `pkey_set` 함수 내부는 사용자 공간에서 **WRPKRU** 명령어를 실행하는 `asm volatile` 인라인 어셈블리로 구성됩니다. 커널로 문맥 교환(Context Switch)이 발생하지 않으므로 나노초(ns) 단위의 제어가 가능합니다.

📢 **섹션 요약 비유**:
건물의 열쇠구조(PTE)를 변경하려면 건물 전체의 도면을 수정하고 공지해야 하지만, MPK는 **각 사람이 가지고 있는 스마트 키(PKRU)의 권한 등급만 변경하는 것**과 같습니다. 문(페이지)은 그대로인데, 내 키가 잠겨서 아무리 돌려도 문이 안 열리는 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: MPK vs mprotect vs MPS
MPK는 기존의 메모리 격리 기술과 특징이 완전히 상이합니다. 아래 표는 각 기술의 정량적, 구조적 차이를 분석한 것입니다.

| 비교 항목 | MPK (Memory Protection Keys) | mprotect (System Call) | MPS (Memory Protection Keys Supervisor) |
| :--- | :--- | :--- | :--- |
| **동작 공간** | **User Space (Ring 3)** | Kernel Space (Ring 0) | Kernel/S Supervisor Space |
| **권한 변경 비용** | **极低 (~10 ns)** | 매우 높음 (~1,000 ns+) | 저렴 (~10 ns) |
| **부가 효과** | **TLB 유지 (Cache Friendly)** | TLB Flush (Performance Kill) | TLB 유지 |
| **격리 단위** | Key Domain (1~16) | Page 단위 | Key Domain |
| **변경 대상** | PKRU Register (권한) | Page Table Entry (속성) | PKRS Register |
| **주요 용도** | 유저 메모리 동적 보호 | 정적 메모리 맵 설정 | 커널 내부 데이터 보호 |

#### 2. 분야별 융합 시너지 및 오버헤드 분석 (ASCII 다이어그램)
MPK는 단순히 '빠른 mprotect'가 아니라, 소프트웨어 아키텍처의 보안 패러다임을 변경합니다.

```text
[MPK Application Layers]

+---------------------------------------------------------------+
|                    Operating System (Kernel)                  |
+---------------------------------------------------------------+
| [Kernel Space]                                               |
| - MPS (Supervisor Keys): Protect Kernel Data Structures     |
|   (e.g., preventing ROP attacks on kernel heap)              |
+---------------------------------------------------------------+
            ^  ^  ^
            |  |  | Context Switch (Save/Restore PKRU)
            |  |  |
+---------------------------------------------------------------+
|                    Application (User Space)                   |
+---------------------------------------------------------------+
| [Database Engine]   [Web Browser]      [High-Frequency Trading|
|                      (Renderer)          (HFT System)         |
| - JIT Heap Guard    - Isodi Heap         - Order Book Lock    |
| - Transaction Buf   - Wasm Guard         |                    |
|                     |                     |                    |
|   +-----------------+---------------------+--------------------+
|   |         MPK LIBRARY (pkey_mprotect)                     |
|   +-----------------------------------------------------------+
+---------------------------------------------------------------+
```
> **해설**: MPK는 커널 영역에서의 데이터 구조 보호(MPS)부터 사용자 영역의 JIT 컴파일러, 데이터베이스 트랜잭션 버퍼 보호까지 폭넓게 활용됩니다. 특히 웹 브라우저의 경우, 웹어셈블리(Wasm)나 JS 엔진의 가비지 컬렉션 힙에 대한 공격을 막는 데 필수적입니다.

*   **OS & 가상화 (Virtualization)**
    *   **시너지**: KVM(Kernel-based Virtual Machine) 등에서 게스트 OS의 페이지 테이블 수정으로 인한 **VM Exit** 비용을 절감할 수 있습니다.
    *   **오버헤드**: PKey 리소스(16개)는 커널과 사용자 공간이 공유하거나 분리