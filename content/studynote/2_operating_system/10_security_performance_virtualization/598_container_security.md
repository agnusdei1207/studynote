+++
title = "598. 컨테이너 보안 (Container Security) - 격리 및 리소스 제한"
date = "2026-03-14"
weight = 598
+++

# [컨테이너 보안 (Container Security) - 격리 및 리소스 제한]

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너는 Host OS (Host Operating System)의 커널을 공유하므로, 격리(Isolation)는 `Namespace`와 `Cgroups` 같은 커널 기술에 의존하며, 이는 Hypervisor 방식의 VM (Virtual Machine)보다 가볍지만 공격 표면(Attack Surface)이 넓은 구조적 특성을 가집니다.
> 2. **가치**: 불�요한 권한 제거(Deprivileging)와 리소스 쿼터(Quota)를 통해 **Noisy Neighbor 문제를 해결**하고, **Zero Trust (영제로 신뢰)** 모델 기반의 런타임 보안을 구현하여 클라우드 네이티브 환경의 안정성을 확보합니다.
> 3. **융합**: 가상화 기술(Hypervisor)과 리눅스 커널 보안 모듸(LSM: Linux Security Modules)이 융합된 `Kata Containers`나 `gVisor` 같은 **MicroVM** 기술로 진화하여 '성능'과 '격리'라는 두 마리 토끼를 잡고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
컨테이너 보안이란 Application (응용 프로그램)을 실행하기 위해 필요한 코드, 런타임, 시스템 도구, 라이브러리, 설정 등을 패키징한 **Container Image (컨테이너 이미지)**의 빌드(Build) 단계부터 운송(Transport), 실행(Runtime) 단계에 이르기까지의 생애 주기 전반을 보호하는 기술과 프로세스를 의미합니다.
기존의 VM 보안이 하드웨어 레벨의 완전한 추상화를 기반으로 한 '강한 격리(Strong Isolation)'를 제공하는 반면, 컨테이너는 **Shared Kernel (공유 커널)** 아키텍처를 채택하여 프로세스 수준의 격리를 제공합니다. 따라서 컨테이너 보안의 핵심은 **"공유된 커널 위에서 얼마나 효과적으로 프로세스를 속이고(Isolation) 제한(Restriction)하느냐"**에 달려 있습니다.

**💡 비유: 주거 형태의 비유**
*   **아파트 (VM)**: 방음벽(하드웨어)으로 완전히 분리된 독립된 공간. 관리 비용 비쌈.
*   **원룸 오피스텔 (Container)**: 얇은 벽(커널 기술)으로 나뉜 독립된 공간. 화장실, 주방(커널)은 이웃과 공유하거나 건물 관리소에 의존. 저렴하고 빠르지만 옆집 소리가 들리거나 벽을 뚫고 들어올 위험이 있음.

**등장 배경**
① **기존 한계**: Monolithic Architecture (모놀리식 아키텍처)에서 MSA (Microservices Architecture)로 전환되면서, VM의 무거운 시작 시간(Boot time)과 자원 낭비가 병목으로 작용함.
② **혁신적 패러다임**: **DevOps (Dev + Ops)** 및 **DevSecOps** 문화 확산과 함께 인프라를 코드(IaC)로 관리하는 추세에 맞춰, 가볍고 이동성이 뛰어난 컨테이너 기술이 도입됨.
③ **현재 요구**: 클라우드 환경에서의 탄력적 운영을 위해 컨테이너 오케스트레이션(예: Kubernetes)이 표준이 되었으나, 공유 커널의 보안 취약점(예: Container Escape)이 대두되면서 이에 대한 강력한 대응 기술이 필수적이 됨.

📢 **섹션 요약 비유**: 컨테이너 보안의 개요는 '수많은 가게(애플리케이션)가 들어선 대형 쇼핑몰(호스트 서버)에서, 각 가게가 독립적으로 운영되도록 하면서도 쇼핑몰의 화재시스템(공유 커널)을 공유하기 때문에, 화재가 다른 가게로 번지지 않도록 방화문과 전력 사용량을 철저히 통제(리소스 제한 및 격리)하는 관리 체계'와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

컨테이너 보안은 단일 기술이 아니라 리눅스 커널의 여러 기능을 조합한 **Defense in Depth (심층 방어)** 계층 구조입니다. 이 섹션에서는 컨테이너의 격리와 리소스 제어를 담당하는 핵심 요소를 분석합니다.

**1. 구성 요소 상세 분석**

| 요소명 (Component) | 전체 명칭 (Full Name) | 역할 (Role) | 내부 동작 (Mechanism) | 프로토콜/명령어 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|:---|
| **Namespace** | Namespace (Linux Kernel Feature) | **격리 (Isolation)** | 프로세스가 시스템 자원(PID, NET, MNT 등)을 독립적으로 보도록 View를 분리함. | `CLONE_NEWPID`, `CLONE_NEWNET` | 투명한 유리 벽 (시야 차단) |
| **Cgroups** | Control Groups (Control Groups) | **리소스 제한 (Limitation)** | CPU, Memory, I/O 등 자원 사용량을 쿼터(Quota)로 설정하여 DoS 공격 방지. | `cgroups`, `--memory="512m"` | 전력 차단기 (전력 과부하 방지) |
| **Capabilities** | Linux Capabilities | **권한 분리 (Privilege Drop)** | Root 권한을 세분화하여 불필요한 권한(예: SYS_MODULE) 제거. | `CAP_NET_BIND_SERVICE`, `--cap-drop` | 제한된 열쇠 권한 (마스터 키 해제) |
| **Seccomp** | Secure Computing Mode | **시스템 콜 필터링 (Filtering)** | 프로세스가 호출할 수 있는 시스템 콜(System Call)을 화이트리스트 방식으로 제한. | `seccomp-bpf`, `SCMP_ACT_KILL` | 출입구 보안 검색대 (허용 물품만 통과) |
| **LSM** | Linux Security Modules | **강제 접근 통제 (MAC)** | 커널 객체에 대한 보안 정책(AppArmor, SELinux)을 강제하여 악성 행위 차단. | `apparmor_parser`, `setenforce` | 건물 보안 규칙 (행동 강령) |

**2. 컨테이너 격리 아키텍처 다이어그램**

아래 다이어그램은 사용자 공간(User Space)의 애플리케이션이 커널 공간(Kernel Space)으로 요청을 보낼 때, 격리와 보안 계층을 통과하는 과정을 도식화한 것입니다.

```text
+------------------------------------------------------------------+
|                 Host OS (Shared Kernel)                           |
| +--------------------------------------------------------------+  |
| |  [User Space]  Container A (App Process)                     |  |
| |  PID 1 (False Root)  |  Isolated View                        |  |
| |       v              |                                       |  |
| |  [Syscall] ----------+---------->                            |  |
| |                                    |                          |  |
| |  +-----------------[Security Boundary Layer]----------------+ |  |
| |  | 1. Seccomp: "Is 'write()' allowed? Yes.                  | |  |
| |  | 2. Capabilities: "Do you have CAP_DAC_OVERRIDE? No."     | |  |
| |  | 3. LSM/AppArmor: "Profile says '/var/log' is Read-Only." | |  |
| |  +----------------------------------------------------------+ |  |
| |                                    |                          |  |
| |  [Kernel Space]   <---------------+                          |  |
| |  4. Namespace: "Map Container PID 1 to Host PID 14052"      |  |
| |  5. Cgroups:  "Throttle CPU usage if exceeds Limit."        |  |
| +--------------------------------------------------------------+  |
|                                                                  |
|   [Hardware] CPU, RAM, Disk (Directly Accessed via Kernel)       |
+------------------------------------------------------------------+

      Legend:
      ① Namespace: Creates illusion of isolated OS.
      ② Cgroups: Enforces resource constraints (CPU/Mem).
      ③ Security Layers: Filter dangerous operations before kernel executes.
```

**3. 심층 동작 원리: 시스템 콜 필터링 (Seccomp-BPF)**
프로세스가 커널에 명령을 내리기 위해서는 반드시 **System Call (시스템 콜)**을 거쳐야 합니다. `Seccomp (Secure Computing Mode)`는 이 지점에서 **BPF (Berkeley Packet Filter)**를 사용하여 필터링을 수행합니다.
*   **동작 순서**:
    1.  애플리케이션이 시스템 콜(예: `clone()`, `execve()`) 발생.
    2.  Seccomp BPF 필터가 시스템 콜 번호를 확인.
    3.  화이트리스트(White-list)에 있는지 비교.
    4.  허용되지 않은 시스템 콜일 경우 `SIGKILL` 시그널을 보내 즉시 프로세스 종료.
    5.  허용된 경우 커널의 실제 함수로 디스패치(Dispatch).

**4. 핵심 알고리즘 및 코드: Namespace Forking**
아래는 C 언어로 `clone()` 시스템 콜을 사용하여 새로운 PID 네임스페이스를 생성하는 컨테이너의 기초 로직입니다.

```c
#define _GNU_SOURCE
#include <sched.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

// Child process function
static int child_func(void* arg) {
    // Inside this new namespace, this process sees itself as PID 1
    printf("Child PID inside namespace: %d\n", getpid());
    execv("/bin/bash", NULL); // Execute shell
    return 0;
}

#define STACK_SIZE (1024 * 1024)
int main() {
    char* stack = malloc(STACK_SIZE) + STACK_SIZE; // Stack grows downward

    // ① CLONE_NEWPID: Isolate Process ID namespace
    // ② CLONE_NEWNET: Isolate Network namespace
    int flags = CLONE_NEWPID | CLONE_NEWNET | SIGCHLD;

    // Create child process with new namespaces
    pid_t pid = clone(child_func, stack, flags, NULL);

    if (pid == -1) {
        perror("clone failed");
        exit(1);
    }

    waitpid(pid, NULL, 0); // Wait for child
    return 0;
}
```

📢 **섹션 요약 비유**: 컨테이너의 아키텍처는 '하나의 거대한 공장(호스트 커널) 내에 설치된 수많은 유리 부스(네임스페이스)'와 같습니다. 각 부스의 근로자(프로세스)는 자신만의 공간에 갇혀 있는 것처럼 느끼지만, 전기와 용수(CPU/RAM)는 중앙 제어실(Cgroups)이 배선을 통해 공급량을 제한합니다. 또한, 위험한 도구를 반입하지 못하도록 출입구마다 보안 검색대(Seccomp/Capabilities)가 설치된 구조입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

컨테이너 보안은 단순히 도커(Docker) 설정만의 문제가 아닙니다. 운영체제(OS), 가상화(VM), 네트워크 보안 정책이 복합적으로 작용합니다.

**1. 심층 기술 비교표: Container vs. VM vs. Unikernel**

| 구분 | VM (Virtual Machine) | Container (Docker/LXC) | Unikernel (Library OS) |
|:---|:---|:---|:---|
| **격리 계층** | **Hypervisor** (Hardware Level) | **OS Kernel** (Shared) | **Application** (Compiled into Kernel) |
| **Guest OS** | 필수 (Full OS Kernel) | 불필요 (Host Kernel 공유) | 불필요 (App + Kernel만 존재) |
| **공격 표면** | 넓음 (OS 자체의 취약점 포함하나 격리됨) | **넓음** (Host Kernel 취약점 공유됨) | **매우 좁음** (불필요한 코드가 없음) |
| **성능 오버헤드** | 높음 (H/W Emulation) | **낮음** (Native Speed) | **매우 낮음** (No Context Switching) |
| **보안 강도** | ⭐⭐⭐⭐⭐ (강력한 격리) | ⭐⭐⭐ (프로세스 격리 수준) | ⭐⭐⭐⭐ (표면적 공격 면역) |
| **주요 보안 이슈** | VM Escape | **Container Escape**, Kernel Panic | N/A (단일 실패점) |

**2. 과목 융합 관점 분석**

*   **[OS/컴퓨터구조]와의 융합: Ring 모델 및 컨텍스트 스위칭**
    *   프로세스는 **Ring 3 (User Mode)**에서 실행되며, 시스템 자원 접근을 위해 **Ring 0 (Kernel Mode)**로 진입해야 합니다. 컨테이너는 이 전이 과정(Context Switching)에서 오버헤드가 적지만, 커널(Ring 0) 버그(예: 'Dirty COW')가 발생하면 모든 컨테이너가 영향을 받습니다.
    *   **시너지/오버헤드**: 컨테이너는 VM처럼 가상화된 하드웨어 드라이버를 처리하는 오버헤드가 없어 빠르지만, 반대로 특정 컨테이너의 Kernel Panic(커널 패닉)이 발생하면 전체 호스트가 다운될 수 있는 **단일 실패점(Single Point of Failure)** 위험이 상존합니다.

*   **[네트워크]와의 융합: SDN (Software Defined Networking)**
    *   컨테이너는 기본적으로 `veth` (Virtual Ethernet) 쌍과 `bridge`를 통해 통신합니다. 이때 **Service Mesh (Istio, Linkerd)**나 **CNI (Container Network Interface)** 플러그인을 통해 네트워크 흐름을 제어합니다.
    *   **시너지**: 마이크로서비스 간 통신을 암호화(mTLS)하고 세밀한 트래픽 제어가 가능합니다.

📢 **섹션 요약 비유**: 컨테이너 보안은 '하이브리드 자동차'와 같습니다. 엔진(커널)과 모터(사용자 공간)가 직접 연결되어 효율적(성능)이지만, 엔진 과열(커널 취약점)이 발생하면 차 전체가 멈춥니다. 반면, VM은 '기관차가 객차를 끄는 형태'로 객차가 고장 나도 기관차는 안전하지만 연결(하이퍼바이저) 유지에 비용이 듭니다. 두 장점을 융합한 '하이