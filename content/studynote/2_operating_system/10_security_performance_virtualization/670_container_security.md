+++
title = "670. 컨테이너 보안 (Container Security)"
date = "2026-03-16"
weight = 670
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "컨테이너 보안", "Container Security", "Docker 보안", "Kubernetes 보안", "Rootless"]
+++

# 670. 컨테이너 보안 (Container Security)

## # [컨테이너 보안]

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너는 **Host OS (Host Operating System)**의 커널을 공유하는 **Process Isolation(프로세스 격리)** 기술이므로, 하이퍼바이저 기반의 **VM (Virtual Machine)** 보다 격리 레벨이 낮습니다. 이를 보완하기 위해 Linux Kernel의 **Namespace (네임스페이스)**, **Cgroup (Control Groups)**, **LSM (Linux Security Modules)** 등을 심도 있게 활용하여 **Shared Kernel (공유 커널)**의 취약점을 방어해야 합니다.
> 2. **가치**: **DevSecOps (Development, Security, and Operations)** 프로세스를 통해 이미지 빌드 단계의 취약점(Scan)을 사전에 제거하고, 런타임 시 **Rootless (Non-root User)** 모드와 **Immutable Infrastructure (불변 인프라)**를 구현함으로써, **Container Escape (컨테이너 탈출)** 공격으로 인한 호스트 침해 위험을 최소화합니다.
> 3. **융합**: OS의 강제 접근 통제인 **SELinux (Security-Enhanced Linux)**/AppArmor를 컨테이너에 적용하거나, **Kubernetes (K8s)**의 **Pod Security Standards (PSS)**, **CIS Benchmark (Center for Internet Security Benchmark)**를 연동하여 선언적 보안 정책을 자동화하는 것이 핵심입니다.

+++

### Ⅰ. 개요 (Context & Background)

컨테이너 보안이란 **Docker**, **containerd**, **CRI-O**와 같은 **CRI (Container Runtime Interface)** 기반 환경에서 발생할 수 있는 보안 위협을 식별, 완화, 대응하는 기술 체계입니다. 전통적인 가상화(VM)가 **Hypervisor (Type 1 or Type 2)**를 통해 하드웨어 수준에서 격리되는 것과 달리, 컨테이너는 호스트 커널을 공유하므로 **"보안 경계(Security Boundary)"**가 훨씬 얇고 공격 표면이 넓다는 근본적인 한계를 가집니다.

이에 따라 컨테이너 보안은 단순한 네트워크 침입 방지를 넘어, **"커널 취약점 공유(RunC Escape 등)", "이미지 공급망(Supply Chain) 위협(Malicious Dependency)", "런타임 권한 남용(Privileged Container)"**이라는 3가지 축을 중심으로 **Defense in Depth (심층 방어)** 전략이 수립되어야 합니다.

#### 💡 비유: '고급 레지던스 호텔'
컨테이너 환경은 **"거대한 하나의 건물(호스트 커널)에 벽만 얇게 세워놓은 호텔 스위트 룸"**과 같습니다. 각 룸(컨테이너)은 독립적인 배관(파일 시스템)과 가구(애플리케이션)를 가지지만, 모두 같은 수도관과 전력망(커널 자원)을 공유합니다. 만약 한 투숙객(해커)이 벽을 뚫거나 수도관을 조작하면, 옆 룸은 물론 건물 전체(호스트 시스템)가 위험해지므로, 각 룸마다 별도의 보안 요원(Security Context)을 배치하고 룸 출입권한(Privilege)을 철저히 통제해야 합니다.

#### 등장 배경 및 시장 요구
기존의 모놀리식(Monolithic) 애플리케이션에서 **MSA (Microservices Architecture)**로의 전환과 **CI/CD (Continuous Integration/Continuous Deployment)** 파이프라인의 고도화로 인해 컨테이너 기술이 표준이 되었습니다. 그러나 **"Log4j"** 사태나 **"SolarWinds"** 공급망 공격에서 보듯, 악성 코드가 포함된 이미지가 배포되거나 런타임에 권한 상승이 발생할 경우 클러스터 전체가 랜섬웨어(Ransomware)의 피해자가 될 수 있습니다. 이를 방어하기 위한 **선제적 검증(Static Analysis)**과 **실시간 행동 감시(Runtime Security)** 기술이 절실한 상황입니다.

#### ASCII 아키텍처: 가상화 기술 비교 (VM vs Container)
아래는 가상머신과 컨테이너의 보안 격리 계층(Layer)과 공격 표면을 비교한 다이어그램입니다.

```text
=============================================================================
[ Virtual Machine Architecture ]            [ Container Architecture ]
=============================================================================

 +---------------------------+              +---------------------------+
 | App A | App B | App C     |              | App A | App B | App C     |
 +-----------+---------------+              +-----------+---------------+
 | Guest OS (Linux/Win)      |              | Bins/Libs (User Space)    |
 |       ↓                   |              |       ↓                   |
 |  Hypervisor (ESXi/Xen)    |              | Container Engine (Docker) |
 |===========================| <--- HW LV   |===========================| <--- OS LV
 | Host Hardware (CPU/Mem)   |              | Host OS (Shared Kernel)   |
 +---------------------------+              +---------------------------+
                                           | Kernel Vulnerabilities    |
                                           | (Shared Attack Surface)   |
                                           +---------------------------+

 [Key Differences]
 - VM:   Complete Isolation via Hardware Abstraction.
 - Container: Process Isolation via Kernel Features (Namespace/Cgroup).
```

> **📝 해설**:
> *   **VM (Virtual Machine)**: 하이퍼바이저가 하드웨어 명령어를 직접 인터셉트하여 **하드웨어 레벨(HW LV)**의 강력한 격리를 제공합니다. 게스트 OS가 손상되어도 호스트 하드웨어로의 직접적인 접근은 차단됩니다.
> *   **Container**: 호스트 커널의 **Namespace (자원 격리)**와 **Cgroup (자원 제한)** 기능만을 사용하므로 **OS 레벨(OS LV)**에서 격리됩니다. 이는 커널 버그(예: `Dirty Cow`, `CVE-2019-5736 runc escape`)를 이용하면 커널 권한을 탈취하여 호스트 시스템을 장악할 수 있는 **Shared Attack Surface (공유 공격 표면)**을 가집니다.

#### 📢 섹션 요약 비유
컨테이너 보안의 개요는 **"화재 경보기와 스프링클러가 없는 고층 빌딩에 수천 명을 입주시키는 것"**과 같습니다. 입주와 퇴주(배포/회수)가 자유롭고 효율적이지만(컨테이너의 장점), 한 층에서 불이 나면 순식간에 전체로 번질 수 있는 구조적 위험(커널 공유)을 인지하고, 이를 방지하기 위해 각 호수에 내화재질로 방을 만들고(Immutable), 출입을 통제하는(Non-root) 것이 필수적입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

컨테이너 보안의 핵심은 **"공격 표면(Attack Surface)을 최소화"**하고 **"실행 권한(Execution Context)을 제어"**하는 데 있습니다. 이를 위해 리눅스 커널의 기본 primitives인 **Namespace**, **Cgroup**, 그리고 보안 강화를 위한 **LSM (Linux Security Modules)**이 어떻게 상호작용하는지 심층적으로 이해해야 합니다.

#### 1. 핵심 구성 요소 (Kernel Primitives)

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 Flags/예시 | 비유 |
|:---|:---|:---|:---|:---|
| **Namespace** | 리소스 격리 | PID, NET, IPC, MNT, UTS 등을 프로세스별로 분리하여 서로 다른 시스템처럼 보이게 함 | `CLONE_NEWPID`, `CLONE_NEWNET` | 투명한 방막이 |
| **Cgroup (Control Groups)** | 자원 제한 | CPU, Memory, Disk I/O 등의 사용량을 제한하고 우선순위 부여 (DoS 방어) | `v1`, `v2` | 전기 과부하 방지 차단기 |
| **Capabilities** | 루트 권한 분리 | root 사용자의 모든 권한(CAP_SYS_ADMIN 등)을 잘게 쪼개어 필요한 것만 부여 | `CAP_NET_BIND_SERVICE` | 제한된 마스터 키 |
| **Seccomp (Secure Computing Mode)** | 시스템 콜 필터링 | 프로세스가 호출할 수 있는 시스템 콜을 화이트리스트/블랙리스트로 제한 | `prctl(PR_SET_SECCOMP)` | 관광지 허용된 경로 외 출입 금지 |
| **LSM (AppArmor/SELinux)** | 강제 접근 통제(MAC) | 파일 접근, 네트워크 포트 등에 대한 커널 수준의 접근 제어 정책 강제 | `enforce`, `complain` | 파일별 보안 인력 배치 |

#### 2. 컨테이너 런타임 보안 흐름도
다음은 사용자가 `docker run` 명령어를 입력했을 때, **OCI (Open Container Initiative)** 스펙에 따라 런타임이 커널의 보안 기능을 설정하는 흐름입니다.

```text
[ USER COMMAND: docker run --security-opt ... ]

      ↓
+------------------------------------------------------------+
| 1. Docker Engine (High-level)                             |
|    - parsing CLI arguments, image management              |
+------------------------------------------------------------+
      ↓
+------------------------------------------------------------+
| 2. Container Runtime Interface (CRI) / Low-level Runtime  |
|    (containerd / CRI-O / runc)                             |
|                                                            |
|  [Step 1] Create OCI Spec (config.json)                   |
|    ├── Define Namespace (Clone Flags)                     |
|    ├── Define Cgroup limits (Memory/CPU quota)            |
|    └── Define User (UID/GID mapping)                      |
|                                                            |
|  [Step 2] Syscalls for Security Context                   |
|    ├── unshare(CLONE_NEWNS ...)  ← Namespace Isolation    |
|    ├── setrlimit(...)            ← Resource Limits        |
|    ├── prctl(PR_CAPBSET_DROP)    ← Drop Capabilities      |
|    ├── prctl(PR_SET_NO_NEW_PRIVS)                        |
|    └── seccomp(SECCOMP_MODE_FILTER) ← Syscall Filtering   |
|                                                            |
|  [Step 3] Execute with LSM Hooks                          |
|    └── SELinux/AppArmor label enforcement (check enforce) |
+------------------------------------------------------------+
      ↓
[ Container Process Start (PID 1 inside Namespace) ]
   (Isolated View, Restricted Resources, Filtered Actions)
```

> **📝 해설**:
> 1.  **Namespace Isolation**: `unshare` 시스템 콜을 통해 프로세스를 독립된 **PID (Process ID)**, **NET (Network Stack)** 공간에 배치합니다. 이때 `/proc` 파일 시스템도 마운트 옵션을 통해 격리된 정보만 보이도록 조작합니다.
> 2.  **Capabilities Dropping**: 컨테이너는 기본적으로 `root` 사용자로 실행되지만, **`CAP_SYS_ADMIN`** (시스템 관리자 권한)이나 **`CAP_SYS_MODULE`** (커널 모듈 로딩) 등 위험한 Capability를 제거(Drop)하여, 컨테이너 탈출 시에도 호스트에 영향을 줄 수 없도록 합니다.
> 3.  **Seccomp-BPF**: **BPF (Berkeley Packet Filter)**를 사용하여 커널 내에서 시스템 콜을 가로챕니다. 예를 들어 웹 서버 컨테이너에서 `execve` (새로운 프로세스 실행)나 `mount` (파일 시스템 마운트) 등의 호출을 차단하여 **RCE (Remote Code Execution)** 공격을 원천 봉쇄합니다.

#### 3. Rootless Container (루트리스 컨테이너)
기존 Docker Daemon은 **`root`** 권한으로 실행되어 **Daemon 취약점 → 호스트 장악**의 위험이 있었습니다. 이를 해결하기 위해 일반 사용자 권한으로 컨테이너를 실행하는 기술입니다.

```text
[ Rootful (Traditional) ]        [ Rootless (Modern Secure) ]
---------------------------       ---------------------------
 Docker Daemon (root)    ←→      User Namespace (Subuid/Subgid)
      |                              |
      v                              v
 Child Process (root)        Child Process (mapped to root)
      |                              |
  Host Root Risk?          <strong>YES (Critical)</strong>              <strong>NO (Protected by Kernel)</strong>
```
*   **기술 원리**: `/etc/subuid`와 `/etc/subgid`를 통해 호스트의 일반 사용자(UID 1000)가 컨테이너 내부에서는 root(UID 0)로 매핑(Mapping)됩니다. 커널은 이를 실제 권한이 아닌 '가상 권한'으로 인식하여 호스트 시스템을 보호합니다.

#### 4. 실무 설정 예시 (Kubernetes SecurityContext)
**Kubernetes (K8s)** 환경에서 보안 정책을 코드로 강제하는 예시입니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secured-pod
spec:
  securityContext:
    # ① Pod 전체 레벨의 FSGroup 설정 (Volume 보안)
    fsGroup: 2000
  containers:
  - name: app
    image: gcr.io/secure-app:latest
    securityContext:
      # ② Root 사용자 실행 금지 (핵심)
      runAsNonRoot: true
      runAsUser: 1000
      
      # ③ Root 파일 시스템 읽기 전용 (Ransomware/Worm 방지)
      readOnlyRootFilesystem: true
      
      # ④ 권한 상승 금지 (setuid 비활성화)
      allowPrivilegeEscalation: false
      
      # ⑤ Capability 제어 (기본 제거 후 필요한 것만 추가)
      capabilities:
        drop:
        - ALL        # 모든 권한 제거
        add:
        - NET_BIND_SERVICE  # 80/443 포트 바인드 권한만 허용
        
      # ⑥ Seccomp 프로파일 적용 (RuntimeDefault 권장)
      seccompProfile:
        type: RuntimeDefault
```

#### 📢 섹션 요약 비유
컨테이너의 보안 아키텍처는 **"죄수를 수감하는 고도의 보안 교도소"**와 유사합니다. **Namespace**는 죄수가 다른 감옥을 볼 수 없게 하는 '차단 벽'이고, **Cgroup**은 죄수가 쓸 수 있는 '식량과 물의 양'을 제한하며, **Seccomp**는 죄수가 간수에게 요청할 수 있는 '행동 요청 목록'을 엄격히 검열하는 것과 같습니다. 마지막으로 **Rootless**는 교도소장조차도 절대적인 권한을 갖지 못하게 하는 '시민 통제 시스템'과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

컨테이너