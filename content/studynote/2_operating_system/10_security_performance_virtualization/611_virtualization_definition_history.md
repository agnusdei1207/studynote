+++
title = "611. 가상화 (Virtualization) 정의 및 역사"
date = "2026-03-14"
weight = 611
+++

# 611. 가상화 (Virtualization) 정의 및 역사

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 가상화(Virtualization)는 Hypervisor(하이퍼바이저)라는 중간 추상화 계층을 통해 물리적 컴퓨팅 자원(CPU, Memory, Disk)을 소프트웨어적으로 분할 및 격리하여, 하나의 하드웨어 위에서 다수의 독립된 실행 환경(VM)을 제공하는 기술입니다.
> 2. **가치**: 서버 통합(Consolidation)을 통해 하드웨어 가동률을 10~15%에서 60~80% 이상으로 끌어올려 비용을 절감하고, Live Migration(라이브 마이그레이션)을 통해 무중단 서비스와 재해 복구(DR) 능력을 극대화합니다.
> 3. **융합**: 현대 클라우드 컴퓨팅(Cloud Computing)의 근간으로, OS 가상화(컨테이너)와 결합하여 MSA(Microservices Architecture) 및 DevOps 환경을 지원하는 인프라의 핵심 엔진입니다.

---

### Ⅰ. 개요 (Context & Background) - 가상화의 기본 철학

#### 1. 개념 및 정의
가상화(Virtualization)는 "하나의 물리적 리소스를 여러 개의 논리적 리소스로 보이게 하거나(분할), 여러 개의 물리적 리소스를 하나의 논리적 리소스로 보이게 하는(통합) 기술"로 정의할 수 있습니다.
전통적인 컴퓨팅 환경에서는 운영체제(OS)가 하드웨어를 직접 독점하여 사용했습니다. 그러나 가상화 환경에서는 **Hypervisor (VMM, Virtual Machine Monitor)** 라는 소프트웨어 계층이 하드웨어와 OS 사이에 개입하여, 물리적 자원을 가상의 머신(VM, Virtual Machine)에 필요한 만큼만 동적으로 할당하고 관리합니다. 이때 각 VM은 자신이 독립적인 물리 서버를 사용한다고 착각하게 됩니다(Illusion of Isolation).

#### 2. 기술적 등장 배경
1.  **기존 한계**: 1990년대~2000년대 초반의 x86 서버 환경에서는 하나의 OS가 하나의 애플리케이션을 구동하는 'One App - One OS' 방식이 주류였습니다. 이는 서버의 자원(CPU/Memory)이 낭비되고, 데이터센터의 공간, 전력, 냉각 비용이 폭발적으로 증가하는 원인이 되었습니다.
2.  **혁신적 패러다임**: VMware가 출시한 x86 가상화 기술은 "여러 개의 OS를 하나의 하드웨어에서 구동"하는 패러다임을 가져왔습니다. 이를 통해 기업은 물리적 서버 수를 획기적으로 줄일 수 있게 되었습니다.
3.  **현재의 비즈니스 요구**: 현재의 민첩한 비즈니스 환경(Agile)에서는 가상화를 넘어, 코드 실행 환경을 즉시 provisioning(프로비저닝)하고 자동으로 확장하는 클라우드 네이티브(Cloud Native) 아키텍처로 진화하고 있습니다.

#### 3. 가상화 작동 구조 도식
가상화는 기본적으로 하드웨어와 게스트 OS 사이에 명령어를 번역하고 자원을 스케줄링하는 계층이 존재합니다.

```text
+------------------+       +------------------+
| Application #1   |       | Application #2   |
+------------------+       +------------------+
| Guest OS (Linux) |       | Guest OS (Win)   |
+------------------+       +------------------+
|       Virtual Hardware Layer (CPU, RAM, Disk abstraction)        |
+-----------------------------------------------------+------------+
|                Hypervisor (VMM) / Host OS          |   Host OS  |
+-----------------------------------------------------+------------+
|                  Physical Hardware (x86 Server)                   |
+-----------------------------------------------------+------------+
       [      Virtual Machine 1 (Isolated)      ]   [ VM 2... ]
```
*(도입 설명: 위 다이어그램은 Hypervisor가 물리 하드웨어 위에서 각각의 가상 머신(VM)들이 독립된 가상 하드웨어를 갖도록 중재하는 계층 구조를 보여줍니다.)*

**해설**:
위 구조에서 가장 핵심은 **Hypervisor** 계층입니다. Hypervisor는 CPU의 특권 명령(Privileged Instruction)이나 메모리 주소 변환(Address Translation) 과정을 가로챕니다(Interception). 이를 통해 VM A가 메모리 주소 0x1000에 접근하려 할 때, 실제 물리 메모리의 0x5000 주소로 매핑(Mapping)하여 다른 VM과의 메모리 충돌을 방지합니다. 즉, 소프트웨어적으로 하드웨어를 여러 개로 쪼개어 각 OS에게 분배하는 '시스템 소프트웨어'의 핵심 역할을 수행합니다.

📢 **섹션 요약 비유**: 가상화는 **'하나의 대형 건물을 여러 세대로 나누어 각 호수에 따로 분양하는 아파트 구조'**와 같습니다. 건물(하드웨어)은 하나지만, 중간 관리 사무소(Hypervisor)가 전기, 수도, 엘리베이터(자원)를 관리하면서 각 세대(VM)는 서로의 존재를 모른 채 독립적인 생활(OS 및 App)을 영위합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - Popek & Goldberg와 하드웨어 지원

#### 1. 구성 요소 상세 분석
가상화 시스템을 구성하는 핵심 요소는 다음과 같습니다.

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/기술 (Protocol/Tech) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Hypervisor (VMM)** | 자원 관리자 및 스케줄러 | 하드웨어 명령어 가로채기(Trap) 및 에뮬레이션, 메모리 매핑 테이블 관리 | Intel VT-x, AMD-V | 건물 관리자/통제실 |
| **Guest OS** | 가상 머신의 운영체제 | 일반 OS처럼 동작하지만, I/O 요청 시 Hypervisor를 통해야 함 | Linux, Windows | 각 세대의 가족 구성원 |
| **VM Monitor Loop** | 감시 및 Context Switching | VM Exit 발생 시 호스트로 제어권 이동 및 완료 후 VM Resume | VMXROOT/Non-Root Mode | 상황에 따른 보호 모드 |
| **Virtual Device** | 가상 하드웨어 장치 | 물리 NIC/Disk를 논리적 장치(vNIC/vDisk)로 매핑, 요청 큐잉 | VirtIO, SR-IOV | 가상의 인터폰/공용 배관 |
| **Resource Pool** | 물리 자원 풀 | CPU 코어, 메모리 페이지, Storage 용량을 동적으로 할당 가능한 상태로 관리 | NUMA Awareness | 공용 수탉/공급 저장고 |

#### 2. 필수 조건: Popek and Goldberg Requirements (1974)
1974년 Gerald Popek과 Robert Goldberg는 가상 가능한 컴퓨터 시스템이 갖춰야 할 3가지 수학적 조건을 제시했습니다. 이는 현대 가상화의 철학적 기반입니다.

```text
+-----------------------------------------------------------------------+
|               P & G Virtualization Requirements                       |
+-----------------------------------------------------------------------+
|                                                                       |
|  1. Equivalence (동등성)                                              |
|     -> 프로그램 실행 결과가 가상 환경 vs 물리 환경에서 동일해야 함.    |
|                                                                       |
|  2. Resource Control (자원 제어)                                       |
|     -> VMM가 시스템 자원을 완전히 통제하고, Guest가 이를 우회할 수 없음.|
|                                                                       |
|  3. Efficiency (효율성)                                               |
|     -> 대부분의 명령어가 하드웨어에서 직접 실행(직접 실행 모드)되어야함.|
|                                                                       |
+-----------------------------------------------------------------------+
```
*(도입 설명: x86 아키텍처는 초기에 'Ring 0' 명령어 처리 문제로 효율성을 만족시키지 못했으나, 하드웨어 보조 기술(Extended Page Tables 등)을 통해 이를 극복했습니다.)*

**해설**:
- **Efficiency(효율성)**: 모든 명령어를 소프트웨어로 에뮬레이션(Emulation)하면 속도가 느려집니다. 가상화는 안전한(User Mode) 명령어는 CPU가 직접 처리하게 하고, 위험한(Sensitive) 명령어만 Hypervisor가 처리하는 Binary Translation(이진 번역) 또는 하드웨어 지원(HVM)을 사용하여 네이티브 성능에 근접하게 만듭니다.
- **Resource Control(자원 제어)**: Guest OS가 하드웨어를 직접 건드리지 못하게 막아야 합니다. 이를 위해 CPU는 **Ring 0(가장 높은 권한)**을 Hypervisor가 점유하고, Guest OS는 **Ring 1** 또는 **Ring -1(VMX Root Operation)** 에서 실행되며, 하드웨어 접근이 필요할 때 Trap(함정)을 발생시켜 Hypervisor의 허락을 받게 합니다.

#### 3. 핵심 알고리즘 및 코드: Shadow Page Tables
x86 가상화에서 가장 복잡한 문제는 메모리 가상화입니다. Guest OS는 자신이 가상 메모리 주소(GVA)를 물리 주소(GPA)로 변환한다고 생각하지만, 실제로는 Hypervisor가 다시 GPA를 실제 물리 주소(HPA)로 변환해야 합니다(2차 주소 변환).

```assembly
/* Conceptual Pseudo-code for Memory Virtualization Walkthrough */

/* 1. Guest OS Translation (Guest Logical -> Guest Physical) */
GPA = Guest_Page_Table.walk(GLA); 

/* 2. Hypervisor Intervention (Guest Physical -> Host Physical) */
/* Intel EPT (Extended Page Tables) or AMD NPT (Nested Page Tables) */
/* Hardware performs this lookup in background */
HPA = EPT.walk(GPA); 

/* If entry missing -> VM Exit (#VMEXIT) -> Hypervisor handles Page Fault */
if (EPT.miss(GPA)) {
    invoke_hypervisor_fault_handler();
    update_ept_structure();
    resume_vm();
}
```

📢 **섹션 요약 비유**: 가상화의 원리는 **'고속도로 통행료 징수 시스템'**과 같습니다. 일반 차량(일반 명령어)은 하이패스 차로를 통해 그냥 통과하지만, 위험 물질을 싣거나 요금을 내야 하는 트럭(민감 명령어)은 검문소(Hypervisor/Trap)에서 반드시 멈춰서 확인(Control)을 받아야 합니다. 이 과정이 매우 빠르게(직접 실행) 일어나야 병목이 생기지 않습니다(효율성).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 가상화 유형 심층 기술 비교
가상화는 구현 방식에 따라 전가상화, 반가상화, 하드웨어 지원 가상화로 나뉩니다.

| 비교 항목 | 전가상화 (Full Virtualization) | 반가상화 (Para-Virtualization) | 하드웨어 지원 가상화 (HVM) |
|:---|:---|:---|:---|
| **정의 (Definition)** | Guest OS를 수정 없이 그대로 실행 가능 | Guest OS 커널을 수정하여 Hypervisor와 협력 | CPU의 가상화 명령어세트(Intel VT-x) 사용 |
| **성능 (Performance)** | 중간 (~80% Native) | 우수 (~95% Native) | 매우 우수 (Near Native, ~98%+) |
| **기술적 특징** | Sensitive 명령어를 Binary Translation으로 처리 | Hypercall(하이퍼콜)을 통해 직접 요청, 오버헤드 감소 | Ring -1에서 직접 제어, Trap/Emulation 최소화 |
| **호환성 (Compatibility)** | 높음 (기존 OS 설치 가능) | 낮음 (커널 수정 필요) | 높음 (수정 불필요, 최신 표준) |
| **대표 예시 (Example)** | VMware Workstation,早期 VirtualBox | Xen (PV Mode),早期 KVM | VMware ESXi, KVM, Hyper-V |

#### 2. 하이퍼바이저 유형 비교 (Type 1 vs Type 2)

```text
+-----------------------------+        +-----------------------------+
|      Type 1 (Bare Metal)    |        |      Type 2 (Hosted)        |
|        +-----------+        |        |        +-----------+        |
|        |Guest OS #1|        |        |   Host |Guest OS #1|        |
|        +-----------+        |        |   OS   +-----------+        |
|        |Guest OS #2|        |        |  (Win/ |Guest OS #2|        |
|        +-----------+        |        |  Linux)+-----------+        |
|    +------------------------+--+     |   +--------------------------+
|    |     Hypervisor (ESXi)   |      |   |   Hypervisor (VMware)    |
|    +---------------------------+     |   +--------------------------+
|    |      Hardware (x86)      |     |   |      Hardware (x86)      |
|    +---------------------------+     |   +--------------------------+
|     [Data Center, Production]      |     [Development, Testing]
```

**해설**:
- **Type 1 (Native)**: 하드웨어 바로 위에 Hypervisor가 위치합니다. 운영체제 없이 직접 하드웨어를 제어하므로 오버헤드가 가장 적고 안정성이 높아 기업용 서버(Production)에 필수적입니다. (예: VMware ESXi, Xen, Microsoft Hyper-V)
- **Type 2 (Hosted)**: 호스트 OS(Windows, Linux 등) 위에 애플리케이션 형태로 설치됩니다. 호스트 OS의 자원을 공유받아 사용하므로 I/O 성능이 Type 1보다 낮고 호스트 OS가 다운되면 가상머신도 같이 죽는 위험이 있습니다. 개발이나 테스트 환경에 적합합니다. (예: VMware Workstation, VirtualBox)

#### 3. 타 과목 융합 관점
- **OS (Operating System)**: 가상화는 프로세스(Process) 수준의 격리를 넘어 OS 자체를 격리합니다. 즉, "OS의 운영 자체를 프로세스화"한 기술로 볼 수 있으며, Context Switching 비용을 OS 스케줄링에 통합합니다.
- **네트워크 (Network)**: 가상 스위치(vSwitch) 기술을 통해 서버 내부에서 VM 간의 트래픽을 라우팅합니다. 이는 물리적 네트워크 장비(스위치, 라우터)를 소프트웨어로 정의하는 SDN(Software Defined Networking)의 시초가 되었습니다.

📢 **섹션 요약 비유**: 가상화 유형은 **'여행 방식'**에 비유할 수 있습니다. 전가상화는 **'현지 가이드 없이 혼자 여행(무조건적 가능)'**이고, 반가상화는 **'현지 언어를 조금 배워서 가이드와