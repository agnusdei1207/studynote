+++
title = "612. 하이퍼바이저 (Hypervisor) - Type 1 (Bare-metal) vs Type 2 (Hosted)"
date = "2026-03-14"
weight = 612
+++

# 612. 하이퍼바이저 (Hypervisor) - Type 1 (Bare-metal) vs Type 2 (Hosted)

### 💡 핵심 인사이트 (Insight)
> 1. **본질 (Essence)**: 하이퍼바이저(Hypervisor)는 **VMM (Virtual Machine Monitor)**로서, 물리적 하드웨어 자원(CPU, Memory, I/O)을 추상화하여 여러 개의 독립된 **VM (Virtual Machine)** 에 할당하고, 이들 간의 격리(Isolation)와 상호 작용을 중재하는 핵심 컨트롤 플레인(Control Plane)입니다.
> 2. **가치 (Value)**: Type 1은 Bare-metal 방식으로 Host OS의 오버헤드를 제거하여 데이터 센터 수준의 **고가용성(HA, High Availability)**과 **네이티브 성능(Native Performance)**을 보장하며, Type 2는 Host OS의 장치 드라이버를 재사용하여 높은 호환성과 사용 편의성을 제공합니다.
> 3. **융합 (Convergence)**: 컨테이너(Container) 기술과의 융합(예: **KVM** 기반 OCI 런타임)을 통해 클라우드 네이티브(Cloud Native) 인프라의 기반이 되며, **SR-IOV (Single Root I/O Virtualization)** 등과 결합하여 I/O 성능 병목을 극복하는 방향으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
하이퍼바이저(Hypervisor)는 단일 물리 컴퓨팅 자원 위에서 다수의 운영체제(OS)를 동시에 실행할 수 있게 하는 소프트웨어 계층 또는 펌웨어입니다. 이를 통해 **H/W (Hardware)**의 자원을 **S/W (Software)** 단에서 논리적으로 분할하여 할당합니다. 전통적인 OS 커널(Kernel)이 프로세스를 관리하는 '슈퍼바이저(Supervisor)' 역할을 한다면, 하이퍼바이저는 OS 자체를 하나의 프로세스처럼 관리한다고 하여 'Hyper-' 접두사가 붙었습니다.

#### 2. 작동 배경 및 필요성
과거의 **MTBF (Mean Time Between Failures)**가 짧고 활용률이 낮은 단일 서버 방식에서 벗어나, **TCO (Total Cost of Ownership)** 절감과 유연한 자원 관리를 위해 **서버 가상화(Server Virtualization)**가 필수적으로 요구되었습니다. 물리적으로 1대의 서버를 논리적으로 N대로 분리함으로써, 유휴 자원을 최소화하고 **SLA (Service Level Agreement)**를 준수하는 탄력적 인프라를 구축할 수 있게 되었습니다.

#### 3. 유론의 분기: Type 1 vs Type 2
하이퍼바이저는 운영체제와 하드웨어 사이의 위치에 따라 두 가지 주요 유형으로 나뉩니다.
*   **Type 1 (Bare-metal/Native)**: 하드웨어 위에 하이퍼바이저가 직접 위치.
*   **Type 2 (Hosted)**: 하드웨어 위에 Host OS가 먼저 실행되고, 그 위에 하이퍼바이저가 어플리케이션으로 실행.

#### 4. 상세 구조 비교 (ASCII Diagram)
아래 다이어그램은 두 유형이 스택(Stack) 구조상 어떻게 다른지를 시각화한 것입니다. 특히 **Intercept(감시)** 경로의 차이에 주목해야 합니다.

```text
+----------------------- Type 1: Bare-metal Architecture ----------------------+
|                                                                               |
|  +----------------+ +----------------+ +----------------+                    |
|  |  Guest OS 1    | |  Guest OS 2    | |  Mgmt Console  |  (Dom0 / Service)  |
|  | (App + Kernel) | | (App + Kernel) | |   (Hosted VM)  |                    |
|  +----------------+ +----------------+ +----------------+                    |
|  |      vCPU      | |      vCPU      | |      vCPU      |                    |
|=======================| ====================================================|  <--- HAL / Abstraction
|  |   Hypervisor    | |  (Direct Hardware Access / Ring -1 / VMX Root)     |  <-- Core Control
|=======================| ====================================================|       Layer
|  |   CPU / Mem / I/O Hardware (Intel VT-x / AMD-V)                         |                    |
+------------------------------------------------------------------------------+

+----------------------- Type 2: Hosted Architecture -------------------------+
|                                                                               |
|  +----------------+ +----------------+                                       |
|  |  Guest OS 1    | |  Guest OS 2    |                                       |
|  | (App + Kernel) | | (App + Kernel) |                                       |
|  +----------------+ +----------------+                                       |
|  |      vCPU      | |      vCPU      |                                       |
|=======================| ====================================================|  <--- User Mode
|  |   Hypervisor    | |  (App installed on Host OS)                         |  (Application Layer)
|=======================| ====================================================|       (Ring 3)
|  |   Host OS (Windows / Linux / macOS)                                    |  <-- System Calls
|  |   (Device Drivers / Kernel / Scheduler)                                |       (Ring 0)
|=======================| ====================================================|        |
|  |   CPU / Mem / I/O Hardware                                             |        |
+------------------------------------------------------------------------------+
```
*   **해설 (Explanation)**:
    *   **Type 1**: 하이퍼바이저가 하드웨어를 직접 제어합니다. VM 간의 통신이나 하드웨어 접근은 별도의 OS 계층을 거치지 않고 하이퍼바이저가 직접 스케줄링하므로 오버헤드가 극히 낮습니다.
    *   **Type 2**: 하이퍼바이저가 Host OS 위에서 일반 응용 프로그램(프로세스)으로 실행됩니다. VM의 하드웨어 요청은 하이퍼바이저가 이를 포착하여 다시 Host OS의 시스템 콜(System Call)로 변환하는 이중 구조(Double Overhead)를 갖습니다.

> 📢 **섹션 요약 비유**: Type 1 하이퍼바이저는 '땅을 사서 직접 건물을 짓고 입주자를 모시는 건물주'의 모습이라면, Type 2는 '대형 건물(Host OS)의 한 층을 빌려서 운영하는 입점 상점'과 같습니다. 전자는 주인이 직접 관리하여 효율적이고, 후자는 건물주의 관리 규칙을 따라야 하지만 설치가 매우 쉽습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 주요 구성 요소 (Component Analysis)
가상화 시스템을 이루는 핵심 요소와 그 역할은 다음과 같습니다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Mechanism) | 관련 기술/용어 |
| :--- | :--- | :--- | :--- |
| **Hypervisor** | 자원 스케줄링 및 격리 | CPU 명령어의 민감 명령(Sensitive Instruction)을 포착하여 **Trap** 후 에뮬레이션 | **Ring -1 / VMX Root Mode** |
| **VM (Virtual Machine)** | 독립된 실행 환경 제공 | 하드웨어를 추상화한 가상 장치(vNIC, vDisk)를 제공하여 Guest OS가 인지 | **Guest OS**, **vCPU** |
| **vCPU (Virtual CPU)** | 물리 CPU 스케줄링 단위 | Hypervisor의 스케줄러에 의해 Physical Core에 매핑되어 Time Sharing됨 | **vCPU-to-pCPU Mapping** |
| **VMM (Virtual Machine Monitor)** | 머신 상태 모니터링 | VM의 Exit 이벤트(예: I/O 요청)를 처리하고 다시 Entry(Resume) 시킴 | **VM Exit / VM Entry** |
| **Device Emulator** | 하드웨어 가상화 | 키보드, 마우스, 네트워크 카드 등을 소프트웨어로 에뮬레이션 | **QEMU**, **virtio** |

#### 2. CPU 가상화 및 Ring 구조 (Deep Dive)
전통적인 x86 아키텍처에서는 **Ring 0(커널 모드)**에서만 하드웨어를 직접 제어할 수 있습니다. 가상화 환경에서는 **하이퍼바이저가 가장 권한이 높아야 하므로**, 새로운 권한 모델이 필요합니다.

*   **전통적인 OS**: Ring 0 (Kernel) / Ring 3 (App)
*   **가상화 환경**: Ring -1 (Hypervisor) / Ring 0 (Guest OS) / Ring 3 (App)

```text
+-----------------------------+  Privilege Level
|  Guest Application          |  Ring 3  (User Mode)
|  (User Mode)                |
+-----------------------------+
|  Guest OS Kernel            |  Ring 0  (Supervisor Mode)
|  (Privileged Instructions)  |          ↓ 스케줄링/인터셉트 필요
+=============================+  =========================================
|  Hypervisor (VMM)           |  Ring -1 (VMX Root Mode / Hardware Assist)
|  (Resource Control)         |          ↑ (Intel VT-x / AMD-V)
+=============================+  =========================================
|  Hardware                   |  Physical CPU
+-----------------------------+

[Working Flow: Privileged Instruction Handling]
1. Guest OS가 "I/O 포트 쓰기(OUT指令)" 같은 민감 명령 실행.
2. CPU가 이를 감지하고 Hypervisor로 제어권 이양 (VM Exit).
3. Hypervisor가 해당 명령을 안전하게 처리하거나 가상 장치에 전달.
4. 처리 완료 후 다시 Guest OS로 복귀 (VM Entry).
```

*   **해설**: 이러한 **Binary Translation** (이진 변환) 또는 **H/W Assist** (하드웨어 지원: Intel VT-x) 기술이 없으면 Guest OS가 직접 하드웨어를 건드려 시스템이 충돌합니다. 최신 하이퍼바이저는 CPU의 가상화 보조 기능(Hardware Virtualization)을 적극 활용하여 성능 저하를 최소화합니다.

#### 3. 메모리 가상화 (Memory Virtualization)
단순한 논리 주소(Logical Address) -> 물리 주소(Physical Address) 변환에 더하여, **Guest Physical Address** -> **Host Physical Address**로의 2단계 변환이 필요합니다.

*   **Shadow Page Tables**: Host OS가 Guest의 페이지 테이블을 복사해서 관리하는 방식. 오버헤드 큼.
*   **EPT/NPT (Extended Page Tables)**: 하드웨어(HW)가 2단계 변환을 한 번에 수행하도록 지원. **TLB Miss** 감소로 성능 향상.

#### 4. 핵심 코드: 스케줄링 로직 개념
```c
// [Pseudo-code: Hypervisor Scheduler Logic]
while (system_running) {
    // Run Queue에 대기 중인 vCPU 확인
    vCPU = pick_next_vcpu(run_queue, PRIORITY_BASED);

    if (vCPU != NULL) {
        // 물리 CPU 코어에 할당 및 실행
        load_vcpu_state(vCPU); 
        VM_ENTER(vCPU->context); 
        
        // VM Exit 발생 시 (인터럽트, I/O 요청 등)
        // 하이퍼바이저의 event_handler로 복귀
        handle_vm_exit(vCPU->exit_reason);
        save_vcpu_state(vCPU);
    }
}
```

> 📢 **섹션 요약 비유**: 하이퍼바이저의 아키텍처는 '매우 정교한 교통정리 시스템'과 같습니다. Type 1은 지상 횡단보도(Host OS) 없이 지하철(Hypervisor)이 모든 역을 직행하는 고속 시스템이며, 메모리 가상화는 번호판을 한 번 더 바꾸는 복잡한 주차 관리 시스템과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. Type 1 vs Type 2 심층 기술 비교
단순한 설치 위치 차이를 넘어 내부 메커니즘과 성능 지표(Quantitative Metrics)에서 명확한 차이를 보입니다.

| 비교 항목 (Criteria) | Type 1 (Bare-metal) | Type 2 (Hosted) | 비고 (Notes) |
|:---|:---|:---|:---|
| **성능 (Performance)** | **Native에 근접** (Overhead < 5%) | **낮음** (Overhead 20~40%) | Host OS의 Context Switching 비용 발생 |
| **I/O 처리 방식** | **Passthrough** 또는 **Para-virtualization**<br>(SR-IOV, virtio) | **Emulation**<br>(Host Driver 경유) | 네트워크 대역폭 격차 발생 |
| **Device Driver** | 전용 드라이버 필요 (범용성 낮음) | Host OS 드라이버 재사용 (범용성 높음) | 설치 편의성은 Type 2 우세 |
| **격리성 (Isolation)**| **완전 격리** (HW 레벨) | **의존적** (Host OS 장애 시 모두 종료) | **RTO (Recovery Time Objective)** 차이 |
| **주요 제품** | VMware ESXi, MS Hyper-V, Xen | Oracle VirtualBox, VMware Workstation | |

#### 2. 과목 융합 분석 (Inter-disciplinary Synergy)
*   **운영체제(OS)와의 관계**: 하이퍼바이저는 **Context Switching** 비용을 최소화하는 것이 핵심입니다. 특히 **TLB (Translation Lookaside Buffer)**의 Flush 횟수를 줄이기 위해 **VPID (Virtual Processor Identifier)** 기술을 사용하는 것은 OS의 메모리 관리 전략과 직결됩니다.
*   **네트워크와의 관계**: 가상화 환경에서의 네트워크 패킷 처리는 병목 지점입니다. 이를 해결하기 위해 **SR-IOV (Single Root I/O Virtualization)**를 사용하여 가상 머신이 NIC(Network Interface Card)를 직접 건드리게 함으로써, Hypervisor의 개입을 최소화하고 **DPDK (Data Plane Development Kit)** 같은 고속 패킷 처리 기술과 융합됩니다.

#### 3. 결정 매트릭스 (Decision Matrix)
실무 환경에서 다음 지표를 고려하여 유형을 선택합니다.

*   **TPS (Transactions Per Second)**: 1만 TPS 이상의 고 트랜잭션 처리 → **Type 1** 필수.
*   **Latency**: 1ms 미만의 초저지연 요구 → **Type 1** (Real-time Linux 적용).
*   **UX/Hardware Support**: 다양한 USB/사운드 장치 지원 필요 → **Type 2**.

> 📢 **섹션 요약 비유**: Type 1과 Type 2의 선택은 '고속열차와 관광버스'의 선택과 같습니다. Type 1은 정거장(Hardware)에만 집중하여 목적지로 빠르게 데려다주는 고속열타(KTX)라면, Type 2는 여러 정거장(Host OS의 기능)에 들러서 다양한 짐(장치 호환성)을 나를 수 있는 관광버스와 같습니다. 성능이 중요한지, 편의성이 중요한지에 따라 다릅니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오별 의사결정 (Decision Making)
**시나리오 A: 대규모 공공 클라우