+++
title = "572. 보호 도메인 (Protection Domain) - 프로세스가 접근할 수 있는 자원(객체)과 권한(Access Right)의 집합"
date = "2026-03-14"
weight = 572
+++

# # [보호 도메인 (Protection Domain)]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 보호 도메인은 운영체제가 시스템 자원에 대한 접근을 제어하기 위해 설정하는 논리적 경계이자, 프로세스의 **"실행 권한 컨텍스트(Execution Context)"**입니다. 단순한 접근 권한 리스트를 넘어, **접근 행렬(Access Matrix)**의 행(Row)을 하드웨어적/소프트웨어적으로 구현한 보안 아키텍처의 핵심 추상화(Abstraction)입니다.
> 2. **가치**: 시스템의 신뢰성(Reliability)과 보안성(Security)을 계층적으로 보장합니다. **격리(Isolation)**를 통해 프로세스 간 간섭을 차단하고, **검증(Verification)**을 통해 불법적인 메모리 접근이나 **I/O (Input/Output)** 명령 실행을 런타임에 차단하여 시스템 붕괴를 방지합니다.
> 3. **융합**: 하드웨어의 **CPL (Current Privilege Level)**, 가상화 기술의 **EPT (Extended Page Table)**, 클라우드의 **Namespace** 격리 등, 현대 보안 기술의 근간이 됩니다. 특히 컨테이너(Container) 보안과 **MAC (Mandatory Access Control)** 시스템인 SELinux의 정책 결정 논리와 직결됩니다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 보호 도메인(Protection Domain)이란 컴퓨터 시스템에서 프로세스가 접근할 수 있는 자원(Objects)의 집합과 그 자원에 대해 수행 가능한 연산(Operations)의 권한을 정의한 **보호 공간**입니다. 수학적으로는 도메인 $D$는 순서쌍 $(Object, Rights)$의 집합으로 표현됩니다. 이 개념의 핵심은 **"도메인 간의 전환(Domain Switching)은 자유로울 수 없으며, 반드시 신뢰할 수 있는 게이트(Trusted Gate)를 통해 검증되어야 한다"**는 것입니다. 이는 소프트웨어적 체크를 넘어 **CPU (Central Processing Unit)**의 명령어 실행 권한(Ring Level)과 직결된 하드웨어적 보호 계층을 형성합니다.

- **💡 비유**: 보호 도메인은 **"건물의 출입권한이 부여된 스마트 카드(Key Card)"**와 같습니다.
    - **마스터 키(커널 모드):** 모든 출입문(서버실, 전원실, 네트워크 장비)을 열고 보안 시스템을 해제할 수 있는 권한.
    - **사원 카드(사용자 모드):** 자신의 책상(할당된 메모리)과 공용 휴게실(공유 라이브러리)에만 출입 가능.
    - **핵심:** 사원 카드를 가진 사람이 마스터 키 구역에 들어가려면 반드시 보안 담당자(시스템 콜/인터럽트)에게 신분을 확인받고 **임시 보안증(Temporary Token)**을 발급받아야 합니다.

- **등장 배경**:
    1.  **초기 컴퓨팅의 위험**: 초기 시스템에서는 한 프로그램이 모든 메모리와 장치를 독점하여, 잘못된 루프 하나가 전체 시스템을 멈추거나 다른 프로그램의 데이터를 파괴했습니다.
    2.  **MULTICS와 Ring 구조의 탄생**: 1960년대 후반 **MULTICS (Multiplexed Information and Computing Service)** 프로젝트에서 계층적 보호를 위해 **Ring (원형 구조)** 개념을 도입했습니다. 이는 이후 x86 CPU의 **Protection Ring** 메커니즘으로 정착되었습니다.
    3.  **최소 권한의 원칙(Principle of Least Privilege)**: 현대 OS로 오면서 프로세스가 필요한 최소한의 자원에만 접근하도록 설계하는 추세로 변화했습니다. 이는 **DAC (Discretionary Access Control)**에서 **MAC (Mandatory Access Control)** 및 **Capability-based Security**로 진화하는 계기가 되었습니다.

보호 도메인의 시각적 개념과 자원 접근의 흐름을 도식화하면 다음과 같습니다.

```text
       [보호 도메인의 논리적 경계와 접근 제어 흐름]

    ┌───────────────────────────────────────────────────────────────┐
    │                    Domain D0 (Kernel)                         │
    │  ┌─────────────────────────────────────────────────────────┐  │
    │  │  • Hardware Control (I/O, Interrupts)                  │  │
    │  │  • Memory Management (Page Tables, TLB)                │  │
    │  │  • File System (Ext4, XFS Journaling)                  │  │
    │  │  • Security Enforcement (SELinux, LSM Hooks)           │  │
    │  └─────────────────────────────────────────────────────────┘  │
    ▲                         │                                     │
    │                         │ ▲                                   │
    ──┼─────────────────────────┼─────────────────────────────────────
    │   │ System Call Gate     │ │ iret (Return)
    │   │ (Trusted Entry Pt)   │ │ (Context Restore)
    │   ▼                     │ │
    │  ┌─────────────────────────────────────────────────────────┐  │
    │  │              Domain D1 (User Process A)                  │  │
    │  │  ┌────────────────┐  ┌────────────────┐                 │  │
    │  │  │  Code Segment  │  │   Data Segment │                 │  │
    │  │  │  (App Logic)   │  │  (Heap/Stack)  │                 │  │
    │  │  └────────────────┘  └────────────────┘                 │  │
    │  │  ┌─────────────────────────────────────────────────┐   │  │
    │  │  │   File Descriptor Table (Only A's resources)    │   │  │
    │  │  └─────────────────────────────────────────────────┘   │  │
    │  └─────────────────────────────────────────────────────────┘  │
    │                                                               │
    │  ▶ 도메인 D1은 자신의 경계 내 자원에만 직접 접근 가능          │
    │  ▶ 화면 출력(I/O) 필요 시?                                     │
    │    └─▶ System Call (Gate) ──▶ 커널(D0)이 권한 확인 후 수행    │
    └───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 상기 도표는 시스템을 **커널 도메인(D0)**과 **사용자 도메인(D1)**으로 구획(Zoning)한 것입니다. 도메인 D1 내부의 프로세스는 독립된 우주에 갇혀 있는 것과 같습니다. 이 경계를 넘어 하드웨어나 다른 프로세스의 자원에 접근하려면, 반드시 **'게이트(Gate)'**인 시스템 콜을 통과해야 합니다. 이 과정에서 **CPU (Central Processing Unit)**는 하드웨어적으로 권한을 검증하고, 스택 포인터(Stack Pointer)를 교체하는 등의 **Context Switching**을 수행하며, 이는 불법적인 메모리 침해를 원천적으로 차단하는 **보호막(Shield)** 역할을 합니다.

> **📢 섹션 요약 비유**: 보호 도메인은 **"국가 간의 국경과 통관 절차"**와 같습니다. 관광객(사용자 프로세스)은 자유 구역(사용자 공간)에서는 자유롭지만, 국경(커널 경계)을 넘어 비행기(하드웨어 자원)를 타거나 입국 심사(시스템 자원 접근)를 하려면 반드시 세관 직원(시스템 콜)에게 여권(권한)을 제시하고 검사를 받아야 합니다. 허가 없이 국경을 넘으면 불법 침입(보안 위반)이 되어 바로 체포됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 상세 분석

보호 도메인을 구현하고 유지하기 위한 시스템의 핵심 구성 요소와 내부 동작 메커니즘은 다음과 같습니다.

| 요소명 | 역할 및 내부 동작 | 관련 기술/Protocol | 비유 |
|:---|:---|:---|:---|
| **Access Matrix** | 시스템의 모든 보호 상태를 정의하는 추상적 모델. 행(Row)은 도메인, 열(Column)은 객체(Object)이며 값은 권한(R/W/X)임. | POSIX Capabilities, SELinux Policy, **ACL (Access Control List)** | 건물의 **총 출입 인가 대장** |
| **Domain Switcher** | 도메인 간 전환을 담당하며, **CPL (Current Privilege Level)** 변경, 스택 교체, 레지스터 보존을 수행. 보안 검증이 핵심. | `syscall`/`sysret`, `int 0x2e`, `iret`指令, **TSS (Task State Segment)** | 국경 검색대의 **여권 스캐너** |
| **Capability List** | **"무엇을 할 수 있는가"**를 나열하는 토큰. 소유하고 있다는 것 자체가 권한 증명(Ticket 모델). 객체를 직접 참조하여 접근 속도가 빠름. | **PID (Process ID)**, File Descriptor, KeyRing | 본인 인증 없이 착용하면 바로 통과되는 **VIP 패스** |
| **Reference Monitor** | 모든 자원 접근 요청을 중개(Mediate)하여 보안 정책을 강제하는 커널 내의 논리적 모듈. 반드시 완전성을 유지해야 함. **LSM (Linux Security Modules)** Hook | 출입구의 **무장 경비원** |
| **Memory Protection Unit** | **MMU (Memory Management Unit)**의 일부로, 가상 주소를 물리 주소로 변환하면서 페이지 테이블의 **U/S (User/Supervisor)** 비트를 검사하여 접근을 차단함. | Page Tables, TLB, **XNU (X is Not Unix)** VM Map | 사무실 복도의 **사원증 리더기** |

### 2. 하드웨어적 보호: x86 Ring Architecture

현대 운영체제는 **IA-32** 아키텍처가 제공하는 **Privilege Level**을 사용하여 도메인을 구현합니다. 이는 0~3단계의 Ring 구조로, 숫자가 낮을수록 강력한 권한을 가집니다. 보통 Ring 0은 커널용, Ring 3은 애플리케이션용으로 사용됩니다.

```text
    [x86 Ring Architecture & Domain Transition Mechanism]

        ┌───────────────────────────────────────────────────────────┐
        │ Ring 0 (Kernel Mode)         [Most Trusted Domain]       │
        │ ───────────────────────────────────────────────────────── │
        │   • Privilege Level: 0 (CPL=0)                            │
        │   • Access: All Memory, All I/O Ports, CR Registers       │
        │   • Execution: MOV to CR3 (Load Page Directory), IN/OUT   │
        │   • Role: OS Kernel, Hypervisor, Device Drivers           │
        ├───────────────────────────────────────────────────────────┤
        │ Ring 1 & 2 (Device Drivers) [Intermediate Levels]         │
        │ ───────────────────────────────────────────────────────── │
        │   • Rarely used in modern OS (mostly consolidated to 0)   │
        ├───────────────────────────────────────────────────────────┤
        │ Ring 3 (User Mode)           [Least Trusted Domain]       │
        │ ───────────────────────────────────────────────────────── │
        │   • Privilege Level: 3 (CPL=3)                            │
        │   • Access: User's Virtual Memory (via Paging)            │
        │   • Restriction: Execution of I/O instructions (GP Fault) │
        │   • Role: Applications, Web Browsers, DB Servers          │
        └───────────────────────────────────────────────────────────┘

    [Domain Switching: System Call Flow]
    1. User Mode (Ring 3)                    2. Kernel Mode (Ring 0)
       App executes: syscall instruction     ──▶   IDT (Interrupt Descriptor Table)
       ┌───────────────────┐                      ┌───────────────────┐
       │   User Stack      │                      │   Kernel Stack    │
       │   Param 1: EBX    │                      │   Save SS, ESP    │
       │   Param 2: ECX    │                      │   Save EFLAGS     │
       │   Syscall No: EAX │                      │   Save Return IP  │
       └───────────────────┘                      │   Jump to Handler │
                                                  └───────────────────┘
       ▲                                           │
       │ iret (Restore CPL 3)                     │
       └───────────────────────────────────────────┘
```

**[다이어그램 해설]** 시스템 콜이 발생하면 **CPU (Central Processing Unit)**는 특정 명령어(`syscall` 또는 `int 0x80`)를 통해 하드웨어적으로 **CPL (Current Privilege Level)**을 3에서 0으로 즉시 변경합니다(Privilege Escalation). 동시에 사용자 스택 포인터(`SS:ESP`)를 커널 스택 포인터로 교체하여, 커널 코드가 사용자 메모리의 오염되지 않은 공간에서 작업할 수 있도록 보장합니다. 작업 완료 후 `iret` 명령어는 이전 상태를 복구하며 CPL을 다시 3으로 되돌립니다. 이 하드웨어적 지원은 애플리케이션이 자의적으로 권한을 상승시키는 것을 물리적으로 불가능하게 만듭니다.

### 3. 심층 동작: Access Matrix의 구현 (Linux Kernel 예시)

논리적 모델인 **Access Matrix**는 실제 구현에서 메모리 낭비를 방지하기 위해 **ACL (Access Control List)** 또는 **Capability (C-List)** 형태로 최적화되어 저장됩니다. 리눅스 커널의 `inode`와 `task_struct`를 통한 권한 검증 과정을 살펴봅니다.

```c
/* [가상 코드] 리눅스 커널의 도메인 전환 및 권한 검사 로직 */
// 1. Domain Transition (System Call Entry)
ENTRY(system_call)
    SWAPGS                       // GS 레지스터 교환 (Kernel Per-CPU 데이터 접근)
    movq %rsp, %gs:pda_oldrsp    // 사용자 스택 저장
    movq %gs:pda_kernelstack, %rsp // 커널 스택으로 교환 (중요!)
    // ...

// 2. Access Verification (File Open Example)
// Domain D1(User Process) tries to access Object O(File)
int sys_open(const char *filename, int flags, int mode) {
    struct inode *inode;
    struct task_struct *current_task; // Current Domain Context

    // A. Resolving Object (Get Inode)
    inode = resolve_path(filename);

    // B. Reference Monitor Check (Permission Matrix Lookup)
    if (!inode_permission(inode, current_task->creds)) {
        // Check ACL: DAC (User/Group/Other)
        // Check Capability: CAP_DAC_OVERRIDE (Root equivalent power)
        return -EPERM; // Access Denied
    }

    // C