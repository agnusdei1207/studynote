+++
title = "595. 샌드박스 (Sandboxing) 및 시스템 콜 필터링 (Seccomp (Secure Computing mode))"
date = "2026-03-14"
weight = 595
+++

# 595. 샌드박스 (Sandboxing) 및 시스템 콜 필터링 (Seccomp)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **샌드박스(Sandboxing)**는 신뢰할 수 없는 코드를 실행할 수 있는 격리된 실행 환경을 제공하며, **Seccomp(Secure Computing mode)**는 프로세스가 사용할 수 있는 시스템 콜을 필터링하여 커널 공격 표면을 최소화하는 핵심 보안 메커니즘입니다.
> 2. **가치**: 이러한 기술은 제로데이(Zero-day) 취약점이나 버퍼 오버플로우(Buffer Overflow) 등 공격 코드 실행에 성공하더라도, 시스템 자원 접근을 차단함으로썠 **공격의 영향력을 최소화(Minimize Blast Radius)**하고 데이터 유출을 방지합니다.
> 3. **융합**: 컨테이너(Container) 가상화, 클라우드 보안, 그리고 웹 브라우저의 렌더링 프로세스 격리 등 현대 보안 아키텍처의 근간을 이루며 **Namespace**, **Cgroups**, **Capability**와 결합하여 심층 방어(Defense in Depth)를 실현합니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**샌드박스(Sandboxing)**는 애플리케이션이 시스템의 나머지 부분에 악영향을 미치지 않도록, 외부로부터 격리된 제어된 환경에서 실행하게 하는 보안 메커니즘입니다. 여기서 **Seccomp(Secure Computing mode)**는 리눅스 커널(Linux Kernel) 기능으로, 프로세스가 커널에 요청할 수 있는 **시스템 콜(System Call)**의 종류를 엄격하게 제한하여 공격 표면(Attack Surface)을 축소하는 기술입니다. 즉, 샌드박스가 "감옥"이라면 Seccomp는 "죄수가 사용할 수 있는 도구 목록"을 관리하는 핵심 규칙 집이라 할 수 있습니다.

**기술적 배경 및 필요성**
전통적인 보안 방식인 네트워크 방화벽이나 암호화는 외부 침입을 막는 데 집중하지만, 내부에서 실행되는 악성코드(예: 악성 PDF 문서 내 스크립트)에 대한 방어는 취약할 수 있습니다. 만약 웹 브라우저가 렌더링 과정에서 버퍼 오버플로우 취약점이 발견되어 공격자가 임의의 코드를 실행에 성공한다고 가정해 봅시다. 이때 샌드박싱이 없다면 공격자는 곧바로 사용자의 개인 파일을 탈취하거나 악성 프로그램을 설치할 수 있습니다. 이를 방지하기 위해 **Chroot**, **Namespace**, **Seccomp-BPF** 등의 기술이 등장하여 프로세스의 가시성과 권한을 물리적/논리적으로 제한하게 되었습니다.

**확장성**
현대의 IT 환경인 클라우드 네이티브(Cloud Native)와 마이크로서비스 아키텍처(MSA)에서는 서비스 간의 격리가 필수적입니다. 도커(Docker)와 쿠버네티스(Kubernetes) 같은 컨테이너 기술은 리눅스 커널의 샌드박싱 기능을 적극 활용하여 가볍고 안전한 격리 환경을 제공합니다.

**📢 섹션 요약 비유**
> 이는 "위험한 화학 실험을 진행할 때, 두꺼운 유리벽과 장갑으로 둘러싸인 **특수 실험실(Sandbox)** 안에서 하며, 실험실 내부에서도 **사용할 수 있는 기구(Seccomp)**를 가위나 젓가락으로만 제한하는 것"과 같습니다. 실험 중 사고가 나더라도 실험실 밖의 연구실(Host OS)은 안전합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 샌드박스의 구현 메커니즘과 Seccomp의 필터링 과정을 기술적 관점에서 심층 분석합니다.

#### 1. 샌드박스 구성 요소 및 상세 동작

샌드박스는 단일 기술이 아닌 여러 커널 기능의 조합으로 구현됩니다. 주요 구성 요소는 다음과 같습니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/명령어 (Protocol/Cmd) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Namespaces** | 자원 격리 (Isolation) | PID, UTS, NET, IPC 등 특정 자원을 프로세스 그룹마다 독립된 뷰 제공 | `unshare()`, `clone()` with `CLONE_NEW...` | 투시 거울 (다른 세계처럼 보이게 함) |
| **Cgroups (Control Groups)** | 자원 제한 (Quota) | CPU, Memory, I/O 사용량을 그룹 단위로 제한 및 모니터링 | Virtual Filesys (`/sys/fs/cgroup/`) | 전기 과금 메터 (사용량 제한) |
| **Seccomp-BPF** | 시스템 콜 필터링 (Filter) | BPF 프로그램으로 시스템 콜 번호 및 인자를 검사하여 허용/거부 | `prctl(PR_SET_SECCOMP)` | 출입구 보안 검색대 |
| **Capabilities** | 권한 분할 (Delegation) | Root의 모든 권한을 개별 단위(예: CAP_NET_ADMIN)로 분리하여 필요한 것만 부여 | `capset()`, `capget()` | 제한적인 열쇠 권한 (마스터 키 분리) |
| **FS/Mount Namespace** | 파일 시스템 격리 | 프로세스별로 독립적인 루트 디렉토리(`/`) 및 마운트 포인트 제공 | `chroot()`, `pivot_root()` | 별도의 정원 가꾸기 (가지치기) |

#### 2. Seccomp (Secure Computing mode) 필터링 아키텍처

Seccomp는 프로세스가 실행될 수 있는 시스템 콜을 제한합니다. 특히 **Seccomp-BPF(Berkeley Packet Filter)** 모드는 유연한 필터링을 위해 BPF 가상 머신을 사용하여 시스템 콜의 인자(Arg0~Arg5)까지 검사할 수 있습니다.

**ASCII Diagram: Seccomp System Call Flow**

```text
   [User Space: Untrusted Process]
       |
       | (1) System Call Invoked
       | e.g., write(fd, buf, len) or socket(AF_INET, ...)
       V
   +-------------------------------------------------------+
   | [Linux Kernel Entry]                                  |
   |                                                       |
   |  (2)  Seccomp Hook Triggered                          |
   |       - Context switch from User to Kernel            |
   |                       |                               |
   |                       V                               |
   |  (3)  BPF Program Execution (Filter)                  |
   |       - Input: struct seccomp_data {                  |
   |           nr      (Syscall Number),                   |
   |           arch    (Architecture),                     |
   |           instruction_pointer,                        |
   |           args[6] (Arguments)                         |
   |         }                                             |
   |                                                       |
   |       - Logic:                                        |
   |         IF (nr == ALLOWED_SYSCALL)                    |
   |            RETURN SECCOMP_RET_ALLOW;                  |
   |         ELSE IF (nr == DANGEROUS_SYSCALL)             |
   |            RETURN SECCOMP_RET_KILL_PROCESS;           |
   |         ELSE                                          |
   |            RETURN SECCOMP_RET_LOG;                    |
   |                                                       |
   |                       |                               |
   |            +----------+----------+                    |
   |            |                     |                    |
   |  (4-a) ALLOW               (4-b) DENY/KILL            |
   |            |                     |                    |
   |            V                     V                    |
   |  [Execute Syscall]      [Signal: SIGSYS]             |
   |  - Kernel Logic        - Process Terminated          |
   |  - Hardware I/O        - Audit Log Generated         |
   +-------------------------------------------------------+
```

**도해 설명 (Diagram Analysis)**
1.  **요청 (Request)**: 사용자 영역(User Space)의 프로세스가 시스템 콜(예: 파일 쓰기, 소켓 생성)을 호출합니다. 이때 스케줄러는 컨텍스트 스위칭(Context Switching)을 통해 커널 모드로 진입합니다.
2.  **후킹 (Hooking)**: 리눅스 커널의 시스템 콜 핸들러 진입 부분에 `secure_computing()` 함수가 호출됩니다. 이 함수가 현재 프로세스에 적용된 Seccomp 필터가 있는지 확인합니다.
3.  **필터링 (Filtering)**: 사전에 등록된 BPF(Berkeley Packet Filter) 프로그램이 실행됩니다. 이 필터는 시스템 콜 번호와 그 인자들을 검사하여 미리 정의된 규칙(Allowlist 또는 Denylist)에 따라 판단합니다.
    *   `SECCOMP_RET_ALLOW`: 시스템 콜 실행을 허가합니다.
    *   `SECCOMP_RET_KILL_PROCESS`: 즉시 프로세스를 종료시킵니다. (가장 강력한 보안)
    *   `SECCOMP_RET_ERRNO`: 에러 코드(예: `EPERM`)를 반환하며 시스템 콜을 거부합니다.
    *   `SECCOMP_RET_LOG`: 시스템 콜을 허용하나 로그를 남깁니다. (디버깅용)
4.  **결과 (Result)**: 허용된 경우에만 실제 커널 핵심 로직이 수행되어 하드웨어 자원에 접근합니다. 거부된 경우 프로세스는 에러를 받거나 강제 종료됩니다.

**핵심 알고리즘 및 코드 (BPF Pseudo Code)**
실제 Seccomp 필터는 C 언어와 유사한 BPF 언어로 작성되거나, 라이브러리(libseccomp)를 통해 JSON 등으로 정의할 수 있습니다.

```c
/* Conceptual BPF Filter for Seccomp */
/* Example: Allow only 'read', 'write', and 'exit'. Kill others. */

struct sock_filter filter_code[] = {
    /* Load system call number from architecture-specific offset */
    BPF_STMT(BPF_LD + BPF_W + BPF_ABS, offsetof(struct seccomp_data, nr)),

    /* Check if it is 'read' (SYS_read) */
    BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_read, 1, 0),
    BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),

    /* Check if it is 'write' (SYS_write) */
    BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_write, 1, 0),
    BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),

    /* Check if it is 'exit' (SYS_exit) */
    BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_exit, 1, 0),
    BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),

    /* Default Action: Kill Process (SIGKILL) */
    BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL_PROCESS),
};
```
이 코드 구조는 결정 트리(Decision Tree) 형태로, 매우 빠른 속도로 시스템 콜을 판별하여 오버헤드를 최소화합니다.

**📢 섹션 요약 비유**
> Seccomp 필터링은 "건물 입구에 서 있는 **철저한 문지기**"와 같습니다. 방문자(프로세스)가 "화장실이 어디입니까?(read/write)"라고 물으면 알려주지만, "지하 금고 열쇠 주세요(mount)"라고 하거나 "건물을 불태우겠습니다(reboot)"라고 하면 즉시 제지하고 쫓아내는(KILL) 원칙을 철저히 지킵니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

샌드박스 기술들은 단독으로 쓰이기보다 상호 보완적으로 결합하여 사용됩니다. 이 섹션에서는 주요 격리 기술들을 비교 분석하고, 성능 및 보안 효율성을 분석합니다.

#### 1. 격리 기술 심층 비교 (Isolation Matrix)

| 구분 | **VM (가상 머신)** | **Container (Docker)** | **Process (Native)** |
|:---|:---|:---|:---|
| **격리 레벨** | 하드웨어 레벨 (Hypervisor) | OS 커널 레벨 (Shared Kernel) | 프로세스 레벨 (Shared Address Space) |
| **핵심 기술** | H/W 가상화 (VT-x/AMD-V) | **Namespace, Cgroups, Seccomp** | 표준 리눅스 프로세스 |
| **독립성** | 완전한 OS 커널 독립 | 커널 공유 (위험 상존) | 자원 공유 (위험 높음) |
| **성능 오버헤드** | 큼 (Full Boot 필요) | 매우 작음 (Native 수준) | 없음 |
| **보안 안전성** | 매우 높음 (커널 공격 불가) | 높음 (Seccomp/Capability 보완 필요) | 낮음 |
| **주요 용도** | IaaS, 완전히 다른 OS 실행 | Microservices, CI/CD | 일반 애플리케이션 |

#### 2. 샌드박싱 기술 융합 시너지 (Synergy)
실무 샌드박스 환경에서는 Namespace와 Cgroups가 물리적/논리적 경계를 만들고, Seccomp와 Capability가 행위를 제한하는 다층 방어 체계를 구축합니다.

*   **Namespace + Seccomp**: Namespace는 프로세스가 "다른 세계에 있는 것처럼" 보이게 하지만, 커널 버그를 통해 이 격리를 깨고 나올 수 있습니다. 이때 Seccomp가 `reboot`이나 `mount` 같은 위험한 시스템 콜을 차단하면, 공격자가 격리를 탈출하더라도 호스트 시스템에 피해를 줄 수 있는 도구를 뺏기게 됩니다.
*   **Cgroups + DoS 방어**: 샌드박스 내부의 악성 프로세스가 무한 루프를 돌거나 메모리를 독점하려 할 때, Cgroups가 상한선을 설정하여 호스트 서버의 **자원 고갈(Resource Exhaustion)** 방지(Dos 공격 방어)합니다.

#### 3. 성능 및 오버헤드 분석 (Quantitative Analysis)

Seccomp 적용에 따른 성능 저하는 필터링 규칙의 복잡도에 따라 달라지지만, 일반적으로 매우 낮습니다.
*   **Latency**: Seccomp-BPF 필터 실행은 대략 수십~수백 나노초(ns) 소요. 시스템 콜 자체의 비용(마이크로초 단위)에 비하면 무시할 수 있는 수준(~1% 미만).
*   **Throughput**: 허용된 시스템 콜의 경우 추가적인 스케줄링