+++
title = "624. 컨테이너 런타임 (Container Runtime) - Docker, containerd, CRI-O"
date = "2026-03-14"
weight = 624
+++

### # 컨테이너 런타임 (Container Runtime)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너 런타임은 애플리케이션을 OS 수준에서 가상화하여 격리된 프로세스로 실행하는 '엔진'이며, Linux Kernel의 Namespace(격리)와 Cgroups(자원 제어) 기능을 API화하여 제공하는 핵심 계층입니다.
> 2. **가치**: Monolithic인 Docker에서 분리된 표준화된 아키텍처(containerd, CRI-O)를 통해, 운영체제 독립적인 컨테이너 관리가 가능해졌으며, 이는 Kubernetes (K8s) 클러스터의 안정성과 유지보수성을 획기적으로 향상시켰습니다.
> 3. **융합**: 단순한 실행 도구를 넘어, 클라우드 네이티브(Cloud Native) 생태계의 표준 인터페이스인 CRI (Container Runtime Interface)와 OCI (Open Container Initiative) 규격을 준수하여 DevOps 파이프라인과 보안 시스템과의 긴밀한 통합을 가능하게 합니다.

---

### Ⅰ. 개요 (Context & Background) - 컨테이너 실행 환경의 진화

**1. 개념 및 정의**
컨테이너 런타임(Container Runtime)은 컨테이너 이미지(Image)를 저장소에서 내려받아 압축을 해제(Unpack)하고, 호스트 운영체제의 커널 기능을 호출하여 격리된 프로세스를 생성 및 관리하는 소프트웨어 계층입니다. 이는 단순히 `run` 명령어를 실행하는 것을 넘어, 이미지 라이프사이클 관리, 네트워크 설정, 스토리지 할당, 보안 정책 적용까지 포괄하는 복잡한 시스템입니다.

**2. 등장 배경과 진화 과정**
초기 컨테이너 기술은 LXC (Linux Containers)와 같은 커널 기능을 직접 사용하는 형태였으나, 사용의 복잡성과 이식성 문제가 있었습니다. 이를 해결하기 위해 Docker가 등장하여 모든 기능(이미지 빌드, 배포, 실행)을 하나로 묶은 'All-in-One' 툴로 시장을 장악했습니다. 하지만 Kubernetes (K8s)와 같은 오케스트레이션 도구가 등장하면서, Docker의 무겁고 Monolithic한 아키텍처는 관리의 부담으로 작용했습니다. 이에 따라 **CNR (Container Native Runtime)**이라 불리는 경량화되고 표준화된 런타임(containerd, CRI-O)이 등장하여, 역할 분담(Attention Separation)이 이루어지게 되었습니다.

**💡 비유**
컨테이너 런타임은 **'레고 조립 로봇 팔'**과 같습니다. 사용자(개발자)가 완성된 레고 설계도(이미지)를 제공하면, 로봇 팔(런타임)이 블록을 꺼내고 차근차근 조립하여 실제 작동하는 모형(컨테이너)을 완성해줍니다.

**3. 역할 분담의 필요성**
현대의 컨테이너 런타임은 크게 두 가지 계층으로 나뉩니다.
*   **High-level Runtime (고수준)**: 사용자와 가까운 계층으로 이미지 전송, 볼륨 관리, 네트워크 설정 등의 복잡한 로직을 처리합니다. (예: containerd, CRI-O)
*   **Low-level Runtime (저수준)**: 실제로 커널 시스템 콜(System Call)을 실행하여 프로세스를 격리시키는 실행부입니다. (예: runc, crun)

```text
+-----------------------+       +----------------------+       +-------------------+
|   User / Developer    | ----> | Docker CLI / Kubectl | ----> |   Image Registry  |
+-----------------------+       +----------------------+       +-------------------+
                                         |
                                         v
+--------------------------------------------------------------------------------------------+
|                         HIGH-LEVEL RUNTIME (Management Layer)                             |
|  (Pulls Image, Manages Network, Volumes, Security Context)                                |
|  +-------------------------+              +----------------------+                        |
|  |      Docker Engine      |              | containerd / CRI-O   |                        |
|  | (Legacy: Monolithic)    |              | (Modern: Modular)    |                        |
|  +-------------------------+              +----------------------+                        |
|             |                                     |                                       |
+--------------------------------------------------------------------------------------------+
              |                                     |
              |                                     | exec / create
              v                                     v
+--------------------------------------------------------------------------------------------+
|                         LOW-LEVEL RUNTIME (Execution Layer)                                |
|  (Creates Namespaces, Cgroups, Mounts)                                                     |
|  +------------------------------------------------------------------+                      |
|  |                           runc / crun                            |                      |
|  |   "I just follow the OCI spec and fork() the process."           |                      |
|  +------------------------------------------------------------------+                      |
+--------------------------------------------------------------------------------------------+
              |
              | libcontainer / libnsenter
              v
+--------------------------------------------------------------------------------------------+
|                      LINUX KERNEL (System Call Interface)                                  |
|   Namespace (IPC, NET, PID...) | Cgroups (CPU, Memory...) | Capabilities | Seccomp         |
+--------------------------------------------------------------------------------------------+
```

**📢 섹션 요약 비유**: 런타임의 계층 분리는 **'레스토랑 주방 시스템'**과 같습니다. 고수준 런타임은 주문서를 받아 재료를 손질하고 플레이팅하는 '쉐프(Chef)'이고, 저수준 런타임은 실제 불을 피우고 요리하는 '쿡(Cook)'입니다. 쉐프가 바뀌어도 쿡의 요리법(표준)은 똑같으니 주방이 혼란스럽지 않습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 표준 규격: OCI와 CRI의 상호작용**
컨테이너 생태계의 유연성은 두 가지 핵심 표준에서 나옵니다.
*   **OCI (Open Container Initiative)**: 런타임 사양(Runtime Spec)과 이미지 사양(Image Spec)을 정의합니다. 어떤 런타임이든 OCI 호환 이미지를 실행할 수 있어야 합니다.
*   **CRI (Container Runtime Interface)**: Kubernetes의 kubelet이 컨테이너 런타임과 통신하기 위한 gRPC 기반 인터페이스입니다. 더 이상 Docker에 직접 의존하지 않고 플러그인 방식으로 런타임을 교체 가능하게 합니다.

**2. 아키텍처 상세 구조 및 데이터 흐름**
쿠버네티스 환경에서 컨테이너가 생성되는 과정을 도식화하면 다음과 같습니다. 이 과정에서 `shim`이라는 중요한 컴포넌트가 데몬(Daemon)이 없는 구조를 유지합니다.

```text
[ Kubernetes Control Plane ]
            |
            | kube-apiserver (YAML Manifest)
            v
    +---------------+
    |    Kubelet    | <--- Orchestrator (Pod Lifecycle Manager)
    +-------+-------+
            |
            | gRPC (CRI Protocol: CreatePod/RunPodSandbox)
            v
+---------------------------------------------------------------+
|                   CRI (Interface Layer)                       |
|  +-------------------+          +-------------------+          |
|  |      CRI-O        |          |    containerd     |          |
|  | (RedHat Focus)    |          | (CNCF / Docker)   |          |
|  +-------------------+          +---------+---------+          |
+---------------------------------------------------------------+
                                          |
                                          | Container Start
                                          v
+---------------------------------------------------------------+
|                 containerd (High-Level Runtime)                |
|  +---------------------------------------------------------+  |
|  |  1. Image Pull & Unpack (OverlayFS)                       |  |
|  |  2. Network Namespace Creation (CNI Plugin Interaction)   |  |
|  |  3. Metadata Management                                   |  |
|  +-------------------------+-------------------------------+  |
|                            | exec $container_id               |
+----------------------------+----------------------------------+
                             |
                             | fork & exec
                             v
+---------------------------------------------------------------+
|                 containerd-shim (The Daemonless Layer)         |
|  Role: 1. Keep STDIO open (FIFO Pipes)                         |
|        2. Report exit status back to containerd                |
|        3. Allows containerd to restart (upgrades) w/o killing  |
+----------------------------+----------------------------------+
                             |
                             | libcontainer (Go)
                             v
+---------------------------------------------------------------+
|                   runc (Low-Level Runtime)                     |
|  "Creates a new process, clones namespaces, sets cgroups..."   |
+---------------------------------------------------------------+
```

**3. 심층 동작 원리: runc와 Shim의 역할**
*   **runc**: OCI 표준 구현체로, 단순한 CLI 툴입니다. `runc run` 명령어를 받으면 `fork()` 시스템 콜을 호출하여 자식 프로세스를 생성하고, 여기에 `clone()`, `unshare()`, `setns()` 시스템 콜을 통해 Namespace를 격리합니다. 이 과정이 완료되면 runc 프로세스는 종료되어야 합니다.
*   **containerd-shim**: runc가 종료된 후에도 컨테이너 프로세스(부모 프로세스가 init이 됨)가 살아있어야 하며, 그 컨테이너의 표준 입출력(stdout/stderr)을 로그 수집기(Fluentd 등)로 전달해야 합니다. Shim은 이 '고아(Orphan)' 컨테이너의 부모 역할을 대신 수행하는 매개체입니다.

**4. 핵심 설정 및 코드 스니펙**
containerd 설정(`/etc/containerd/config.toml`) 예시입니다.
```toml
[plugins."io.containerd.grpc.v1.cri"]
  # CRI 플러그인 활성화
  systemd_cgroup = false

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  # 런타임 이름 및 버전
  runtime_type = "io.containerd.runc.v2"
  
  # Base Runtime Spec (OCI) 수정
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

**📢 섹션 요약 비유**: 아키텍처 구조는 **'식당 주문 시스템과 배달원'**과 같습니다. Kubelet은 '손님'이고, CRI는 '주문서(표준 양식)'입니다. containerd는 '주방장'이고, Shim은 '배달 기사'입니다. 주방장이 휴식을 가하거나 교체되더라도(런타임 업데이트), 배달 기사(Shim)가 음식(컨테이너)을 안전하게 배달하는 동안 손님은 서비스 중단을 느끼지 못합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 핵심 런타임 기술 비교 (Docker vs. containerd vs. CRI-O)**

| 비교 항목 | Docker Engine (Legacy) | containerd (Industry Std) | CRI-O (Optimized) |
|:---|:---|:---|:---|
| **구조 (Architecture)** | Monolithic (Daemon 중심) | Modular (Layered) | Microkernel (Lightweight) |
| **대상 사용자 (Target User)** | Developers, Desktop Ops | Cloud Vendors, General K8s | OpenShift/RedHat Ecosystem |
| **CRI 지원 (Native)** | X (Dockershim 필요했음) | O (Built-in Plugin) | O (Built-in) |
| **의존성 (Dependencies)** | 자체적인 라이브러리 중복 | OCI 표준 준수, 경량 | systemd, podman 등 RH 기술과 융합 |
| **주요 장점** | 빌드 및 개발툴 생태계 우수 | 안정성과 범용성 | 보안성(RHCOS)과 경량화 |
| **주요 단점** | 무거운 오버헤드 | 설정 복잡성 상승 | RH 이외 생태계에서의 지연 |

**2. 성능 및 효율성 메트릭스**
*   **Footprint**: Docker Engine은 Python 스크립트와 다중 데몬으로 구성되어 메모리 점유율이 상대적으로 높습니다. containerd와 CRI-O는 단일 바이너리에 가까운 형태로 구성되어 메모리 사용량이 최소화됩니다(약 30~40% 절감 효과).
*   **Startup Latency**: `runc` 실행 속도는 거의 동일하나, High-level 런타임의 오버헤드에 따라 전체 파드 생성 시간 차이가 발생할 수 있습니다.

**3. 타 영역(보안/OS)과의 융합**
*   **보안 (Security)**: Kata Containers나 gVisor와 같은 'Sandboxed Runtime'은 Low-level 런타임 계층에서 VM 기반 격리를 제공합니다. containerd는 이러한 런타임을 플러그인으로 교체하여 Multi-tenant 환경의 보안을 강화할 수 있습니다.
*   **OS 융합**: CRI-O는 Red Hat의 **CoreOS (Red Hat CoreOS - RHCOS)**와 깊게 통합되어 있어, `ignition` 부팅 프로세스와 연계되어 불변(Immutable) 인프라를 구현하는 데 최적화되어 있습니다.

**📢 섹션 요약 비유**: 이들의 차이는 **'자동차와 부품'**의 관계와 유사합니다. Docker는 소비자가 바로 타고 가는 **'완성차'**입니다(편리하지만 무겁습니다). containerd와 CRI-O는 자동차 제조사가 사용하는 **'엔진/섀시 플랫폼'**입니다. 자신이 레이싁 카를 만들건지, 트럭을 만들건지(Kata Containers 등 보안 런타임 연동)에 따라 플랫폼을 골라 쓸 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 트리**
*   **상황 A (Public Cloud 클러스터 운영)**
    *   **환경**: AWS EKS, Azure EKS, Google GKE 사용
    *   **결정**: 클라우드 제공사가 최적화한 Managed Runtime(예: AWS EKS `containerd`)을 그대로 사용한다. Customizing을 시도하면 지원받기 어려울 수 있다.
*   **상황 B (On-Premise / Bare-metal K8s 구축)**
    *   **환경**: 자체 데이터 센터에 물리 서버를 나란히 두어 구축
    *   **결정**: **containerd**를 선택한다. 범용성이 가장 좋고 문서가 풍부하여 트러블슈팅이 유리하다.
*   **상황 C (Red Hat / OpenShift 기반 구축)**
    *   **환경**: RHEL (Red Hat Enterprise Linux) 기반의 OS 사용
    *   **결정**: **CRI-O**를 선택한다. OS의 보안 기능(SElinux, 현재는 Kernel 기능)과 가장 밀접하게 통합되어 있고, Red Hat 지원을 받기에 유리하다.

**2. 도입 체크리스트 (Technical/Operational)**
*   **[ ] CRI 호환성 확인**: 설치하려는 런타임이 사용하는 Kubernetes 버전의 CRI 버전을 지원하는가? (예: K8s 1.24+는 Dockershim 제거)
*   **[ ] cgroup Driver 일치**: 런타임의 `cgroup