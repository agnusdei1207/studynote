+++
title = "[OS] 151. 네임스페이스 격리 프로세스 (Namespace Isolation)"
date = "2026-03-04"
[extra]
categories = "studynote-operating-system"
tags = ["Namespace", "Isolation", "Container", "Linux Kernel", "Security"]
+++

# [OS] 네임스페이스 격리 프로세스 (Namespace Isolation)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리눅스 커널(Linux Kernel) 차원에서 프로세스별 자원(IDC, NET, MNT 등)의 가시성을 분리하여, 단일 커널 위에서 **OS-Level Virtualization (운영체제 수준 가상화)**을 구현하는 핵심 메커니즘이다.
> 2. **가치**: 하이퍼바이저(Hypervisor) 기반의 VM(Virtual Machine) 대비 오버헤드를 획기적으로 줄여(**ms→ms 이하**), MSA(Microservices Architecture) 환경에서의 **API 응답 속도 향상** 및 **리소스 효율성**을 극대화한다.
> 3. **융합**: cgroup(Control Group)의 자원 제어와 결합하여 컨테이너를 완성하며, 최근에는 eBPF(Extended Berkeley Packet Filter)와 연계하여 보안 가시성을 강화하는 방향으로 진화 중이다.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념**
Namespace Isolation(네임스페이스 격리)은 리눅스 커널의 핵심 기능으로, 하나의 호스트 시스템에서 실행되는 프로세스들을 서로 다른 실행 환경에 배치하는 기술이다. 이는 단순히 프로세스 ID(Process ID, PID)를 다르게 부여하는 것을 넘어, 파일 시스템(File System), 네트워크 스택(Network Stack), IPC(Inter-Process Communication) 등 시스템의 핵심 리소스에 대한 '관점(View)' 자체를 분리한다. 즉, 격리된 프로세스 입장에서 자신은 운영체제의 유일한 사용자인 것처럼 인지하게 된다.

**💡 비유**
이는 하나의 대형 건물(Host OS) 내에 있지만, 각기 다른 회사(Tenant)가 입주하여 자신만의 사무실(Namespace)을 사용하는 것과 같다. 복도를 통해 이동할 수는 있지만(Context Switch), 각 사무실 내부의 구조와 직원들은 서로 완전히 분리되어 있다.

**등장 배경**
① **기존 한계**: 전통적인 하이퍼바이저 기반 가상화는 게스트 OS(Guest OS) 전체를 부팅해야 하므로 막대한 메모리와 시작 시간(Booting Time)이 소요되었다. ② **혁신적 패러다임**: 구글(Google)의 Borg 시스템 등에서 시작된 '프로세스 단위 격리' 개념이 리눅스 커널 2.6.x 이후 Namespaces 기능으로 정식 편입되었다. ③ **현재의 비즈니스 요구**: 클라우드 네이티브(Cloud-Native) 시대가 도래하며, 수초~수분 내에 수천 개의 서비스를 생성하고 종료해야 하는 무거운 VM의 한계를 극복할 대안으로 Docker, Kubernetes 같은 컨테이너 기술의 근간이 되었다.

```text
+-------------------------------------------------------------------+
|                       Host OS (Single Kernel)                     |
|  +---------------------------+  +-------------------------------+  |
|  |  View A (Namespace A)     |  |  View B (Namespace B)        |  |
|  |  ----------------------   |  |  ---------------------------- |  |
|  |  PID 1 (My App)           |  |  PID 1 (Other App)            |  |
|  |  IP: 192.168.1.10         |  |  IP: 10.0.0.5                 |  |
|  |  Root: /app/data          |  |  Root: /web/html             |  |
|  +---------------------------+  +-------------------------------+  |
|             ^                                ^                    |
|             | (Isolation)                    | (Isolation)        |
+-------------------------------------------------------------------+
```
*(해설: 위 다이어그램은 단일 커널 위에서 두 개의 서로 다른 뷰(View)가 공존하는 모습을 도식화한 것이다. A와 B는 각각 자신만이 유일한 시스템이라고 착각하지만, 실제로는 하나의 커널 자원을 공유하고 있다.)*

**📢 섹션 요약 비유**
마치 거대한 창고(Host) 안에 칸막이를 쳐서, 각 입주자가 자신의 공간만을 바라보도록 만드는 '가상의 독립 사무실' 구획 기술입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**구성 요소 (표)**
| 요소명 (Namespace Type) | 역할 | 내부 동작 (Kernel Object) | 관련 시스템 콜 | 비유 |
|:---|:---|:---|:---|:---|
| **UTS (Unix Timesharing System)** | 호스트명/도메인명 격리 | `struct utsname` 분리 | `clone(CLONE_NEWUTS)` | 건물 입구의 간판 분리 |
| **IPC (Inter-Process Communication)** | 메시지 큐/세마포어 격리 | IPC 식별자(ID) 매핑 테이블 분리 | `clone(CLONE_NEWIPC)` | 사내 메신저 그룹 채팅방 |
| **PID (Process ID)** | 프로세스 ID 공간 격리 | PID 할당 번호표(PID Namespace) 분리 | `clone(CLONE_NEWPID)` | 각 부서별 독립적인 사번 부여 |
| **Network (NET)** | 네트워크 스택(인터페이스, 라우팅) 격리 | Network Namespace 인스턴스 생성 | `clone(CLONE_NEWNET)` | 각 사무실별 전용 dedicated 회선 |
| **Mount (MNT)** | 파일시스템 마운트 포인트 격리 | Mount Tree(Dentry) 분리 | `clone(CLONE_NEWNS)` | 각자의 폴더 구조 및 보관함 |
| **User (UID)** | 사용자/그룹 ID 매핑 | UID/GID 매핑 테이블 관리 | `clone(CLONE_NEWUSER)` | 외부인에게 내부 직원 증명서 발급 |

**ASCII 구조 다이어그램 + 해설**

```text
   [User Space Process]
          |
          | execve(container_runtime)
          v
   +------------------+         clone() System Call
   |   fork() / clone| ----------------------------------------+
   +------------------+                                         |
          |                                                      |
          v                                                      v
   +------------------+                                +-------------------+
   |  Parent Process  |                                | Child Process     |
   |  (Host Shell)    |                                | (Container Init)  |
   |  [NS: Host]      |                                | [NS: New Set]     |
   +------------------+                                +-------------------+
          ^                                                     |
          |                                                     | setns()
          |                                                     v
   +---------------------------------------------------------------+
   |                    Linux Kernel Space                         |
   |                                                               |
   |   +----------------+  +----------------+  +----------------+  |
   |   |  nsproxy       |->| uts_namespace  |  | net_namespace  |  |
   |   | (task_struct)  |  | (nodename)     |  | (dev, routes)  |  |
   |   +----------------+  +----------------+  +----------------+  |
   |                                                               |
   +---------------------------------------------------------------+
```
*(해설: 프로세스 생성 시 `clone()` 시스템 콜에 `CLONE_NEWxxx` 플래그를 전달하면, 커널은 해당 `task_struct`에 연결된 `nsproxy` 구조체가 가리키는 네임스페이스 객체를 새로 할당하거나 기존 것을 참조하게 한다. 이로써 부모와 자식 프로세스는 완전히 다른 자원 세계를 바라보게 된다.)*

**심층 동작 원리 (5단계)**
① **호출 (Invocation)**: 사용자가 `docker run` 명령을 입력하면, Container Runtime(Containerd 등)은 커널에게 `clone()` 시스템 콜을 요청하며, 여기에 격리 플래그(`CLONE_NEWPID`, `CLONE_NEWNET` 등)를 인자로 전달한다.
② **객체 할당 (Allocation)**: 커널은 해당 플래그를 확인하여 기존의 글로벌 네임스페이스 대신, 새로운 네임스페이스 객체(C Kernel Object)를 힙(Heap) 영역에 할당한다.
③ **매핑 (Mapping)**: 새로 생성된 자식 프로세스의 `task_struct` 내부 포인터가 이 새로운 객체를 가리키도록 설정한다.
④ **뷰 제공 (View Provisioning)**: 프로세스가 자원 요청(예: `getpid()`, `ifconfig`)을 하면, 커널은 프로세스가 가리키는 네임스페이스 객체 내의 정보만을 반환한다.
⑤ **폴백 및 소멸 (Fallback & Teardown)**: 네임스페이스 내의 모든 프로세스가 종료되면, 해당 자원은 참조 카운트(Reference Count)가 0이 되어 메모리에서 해제된다.

**핵심 알고리즘 및 코드**
```c
// 리눅스 커널(대략적 C 언어 스타일)에서의 네임스페이스 생성 로직
// 실제 커널 코드는 ns_proxy.c 및 kernel/nsproxy.c 등에 분포함.

struct task_struct *task; // 프로세스 제어 블록(PCB)

// 시스템 콜 핸들러 내부 로직 시뮬레이션
long sys_clone(unsigned long flags, ...) {
    // 1. flags에 CLONE_NEW* 플래그가 있는지 확인
    if (flags & (CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWIPC | 
                 CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWUSER)) {
        
        // 2. 새로운 네임스페이스 생성 및 검증
        err = create_new_namespaces(flags, current);
        if (err) 
            return -ENOMEM; // 메모리 부족 혹은 권한 실패
    }

    // 3. 자식 프로세스 생성 및 nsproxy 연결
    struct task_struct *child = copy_process(flags, ...);
    
    // 4. 자식의 task_struct->nsproxy를 새로 생성된 객체로 연결
    child->nsproxy = new_nsproxy;

    return child->pid;
}
```

**📢 섹션 요약 비유**
마치 건물 입구에서 경비원(Syscall)이 출입증(ID)을 확인하고, 해당 사무실(Namespace)만의 열쇠를 건네주어, 복도를 통해서는 다른 사무실에 들어갈 수 없도록 잠그는 보안 프로세스와 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

**심층 기술 비교: VM vs Container**

| 비교 항목 (Metrics) | 가상머신 (Hypervisor) | 컨테이너 (Namespace) | 수치적 차이 (Example) |
|:---|:---|:---|:---|
| **격리 레벨 (Isolation)** | 하드웨어 레벨 (Strong Isolation) | 프로세스 레벨 (Kernel-Level Sharing) | VM의 격리성이 더 높음 (CVE 발생 시 영향도 차이) |
| **부팅 시간 (Boot Time)** | OS 로딩 필요 (수 분) | 프로세스 생성 (수 ms ~ 초) | **VM: ~2min vs Container: ~50ms** |
| **오버헤드 (Overhead)** | 게스트 OS 커널 메모리 중복 | 커널 공유, 프로세스 스레드만 | **VM: ~500MB vs Container: ~10MB** (이미지 크기) |
| **성능 (Performance)** | 하이퍼바이저 통해 I/O (약간의 손실) | 네이티브 I/O (거의 손실 없음) | **네트워크 처리량: Container가 약 2~5% 우수** |
| **이식성 (Portability)** | 전체 이미지 무거움 | 레이어드(Layered) 이미지로 가벼움 | 배포 속도에서 컨테이너 압승 |

**과목 융합 관점**

1.  **OS & 보안 (Security)**:
    -   Namespace는 단순히 "보이지 않게" 하는 것이지, "권한을 제어"하지는 못한다. 예를 들어, User Namespace를 사용하지 않으면, 컨테이너 내의 root가 곧 호스트의 root와 동일한 권한을 가질 수 있다.
    -   따라서 **보안(Security)** 영역의 **Capability-based Security(능력 기반 보안)** 및 **Rootless Container** 기술과 반드시 결합되어야 한다.

2.  **컴퓨터 구조 & 네트워크 (Network)**:
    -   Network Namespace 격리 시, 기본적으로 외부와 통신이 불가능하다.
    -   이때 **veth(Virtual Ethernet)** pair 장치와 **Linux Bridge**를 생성하여, 호스트의 물리적 NIC(Network Interface Card)와 연결해야 한다.
    -   이는 **가상 스위치(Virtual Switch)** 개념으로 확장되며, 오버레이 네트워크(VXLAN, Geneve) 기술과 융합되어 SDN(Software Defined Networking)을 구현한다.

```text
      [ Container A ]          [ Container B ]
      (eth0: 10.0.0.2)         (eth0: 10.0.0.3)
           |                        |
      veth-a                   veth-b
(Cable)   |                        |   (Cable)
      +--+------------------------+--+
      |        Linux Bridge (cbr0)   |
      +--+-------------+-------------+
         |             |
      eth0 (Host Physical NIC)
         |
      [ External Network ]
```
*(해설: 네트워크 네임스페이스는 서로 통신이 불가능하므로, 케이블처럼 연결해주는 가상 이더넷 디바이스(veth pair)를 사용하여 브리지로 연결한 모습이다. 이는 OS의 자원 격리와 네트워크의 연결성을 해결하는 융합 아키텍처이다.)*

**📢 섹션 요약 비유**
단지 주소(네임스페이스)를 다르게 하는 것만으로는 충분치 않으며, 마치 아파트 단지(네트워크) 내에 전용 회선(veth)을 깔고 각 호수(컨테이너)로 연결해 주는 공사(OS 네트워킹 스택)가 병행되어야 실제 서비스가 가능합니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**실무 시나리오: MSA(Microservices Architecture) 전환**
-   **문제 상황**: 모놀리식(Monolithic) 구조의 레거시 애플리케이션을 도커(Docker) 기반으로 분리하려 한다. 하지만 일부 모듈은 보안상 이유로 강력한 격리가 필요하고, 다른 모듈은 극한의 성능이 필요하다.
-   **의사결정 과정**:
    1.  **성능 중요 모듈 (API Gateway)**: 경량 네임스페이스 기반 컨테이너를 사용하여 **Latency(지연 시간)**를 최소화한다.
    2.  **보안 중요 모듈 (Payment)**: 일반 네임스페이스는 부족하다 판단, **Kata Containers** (VM