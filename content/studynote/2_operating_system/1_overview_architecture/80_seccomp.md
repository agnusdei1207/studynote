+++
title = "80. 시스템 호출 차단 (Seccomp)"
date = "2026-03-12"
weight = 80
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Seccomp", "시스템 콜 차단", "커널 보안", "샌드박스", "공격 표면 축소"]
+++

# 시스템 호출 차단 (Seccomp)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Seccomp (Secure Computing Mode)는 리눅스 커널(Linux Kernel) 레벨에서 프로세스의 시스템 호출(System Call) 집합을 제한하여, 애플리케이션의 **공격 표면(Attack Surface)을 획기적으로 축소**하는 샌드박싱 메커니즘이다.
> 2. **가치**: 웹 브라우저나 컨테이너와 같이 불신할 수 있는 코드를 실행해야 하는 환경에서, **제로데이(Zero-day) 커널 취약점**이 악용되더라도 시스템 호출 차단을 통해 호스트 시스템의 파급 방지(RCE, Remote Code Execution 방지) 및 권한 상승을 원천 봉쇄한다.
> 3. **융합**: BPF (Berkeley Packet Filter) 기반의 유연한 필터링(Seccomp-BPF)을 통해 cgroups(Control Groups), 네임스페이스(Namespaces)와 결합하여 **컨테이너 보안의 핵심 방화벽** 역할을 수행하며, LSM (Linux Security Modules)과 연동하여 심층 방어(Defense in Depth)를 구현한다.

+++

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**Seccomp (Secure Computing Mode)**는 리눅스 커널(버전 2.6.12 이상)에 도입된 보안 기능으로, 프로세스가 자신이 호출할 수 있는 시스템 호출을 스스로 제한할 수 있는 기능을 제공한다. 이는 프로세스가 **"나는 단순한 연산만 수행하며, 파일 입출력이나 네트워킹 같은 복잡하고 위험한 작업은 수행하지 않겠다"**고 커널에게 선언하는 '자발적 격리(Voluntary Confinement)' 형태를 띤다. 일반적인 접근 제어인 DAC (Discretionary Access Control)나 MAC (Mandatory Access Control)이 '자원(Who)'에 초점을 맞춘다면, Seccomp는 **'행위(What)'**를 제어하는 데 중점을 둔다는 점에서 근본적인 차이가 있다.

### 2. 💡 핵심 비유: 은행의 '서류 제한 창구'
일반적인 프로세스의 실행은 은행 창구에서 모든 업무(대출, 송금, 금고 개방 등)를 처리할 수 있는 **'만능 창구'**를 이용하는 것과 같다. 해커는 이 창구의 직원을 협박(취약점 공격)하여 금고를 열려 시도할 수 있다. 반면, Seccomp를 적용한 프로세스는 **'단순 입출금 전용 창구'**만 이용하겠다고 약속하는 것과 같다. 아무리 해커가 직원을 협박하더라도, 해당 창구의 컴퓨터에는 금고 여는 버튼(위험한 시스템 콜) 자체가 물리적으로 존재하지 않으므로 금고를 열 수 없다.

### 3. 등장 배경: 커널 공격 표면의 확장과 한계
- **① 기존 한계**: 전통적인 보안 모델은 '사용자'나 '파일' 단위의 권한을 제어할 뿐, 프로세스가 어떤 **커널 함수**를 호출하는지는 제어하지 못했다. 공격자는 웹 서버 프로세스의 권한으로 `execve` (실행)나 `ptrace` (디버깅) 같은 시스템 콜을 악용하여 쉘을 획득하거나 권한을 상승시켰다.
- **② 혁신적 패러다임**: 구글 크롬(Google Chrome) 팀이 웹 브라우저 렌더링 엔진을 보호하기 위해 제안한 Seccomp는 "프로세스가 필요로 하는 최소한의 권한만 남기고 나머지 커널 기능은 포기한다"는 **최소 권한의 원칙(Principle of Least Privilege)**을 시스템 콜 레벨로 구현했다.
- **③ 현재의 요구**: 클라우드 환경과 컨테이너 가상화(Docker, Kubernetes)가 보편화되면서, 호스트 커널을 공유하는 수많은 워크로드를 격리하기 위해 Seccomp는 선택이 아닌 필수 보안 기준으로 자리 잡았다.

### 4. 작동 시나리오 다이어그램
```text
   [Normal Process]                    [Seccomp Process]
+-------------------+           +-------------------+
| User Logic        |           | User Logic        |
| +-- execve()      |           | +-- execve()      |
| +-- socket()      |           | +-- socket()      |
| +-- open()        |           | +-- read()        |
+--------+----------+           +--------+----------+
         |                               |
         |                               | (PR_SET_SECCOMP)
         v                               v
+--------------------------------------------------+
|              Linux Kernel (System Call Layer)    |
|                                                  |
|  [All Syscalls]                  [Filtered List] |
|  +-- execve (ALLOWED)           +-- execve (BLOCKED) > SIGKILL
|  +-- socket (ALLOWED)           +-- socket (BLOCKED) > SIGKILL
|  +-- open   (ALLOWED)           +-- read   (ALLOWED)
+--------------------------------------------------+
```
*해설: 일반 프로세스는 커널이 제공하는 모든 시스템 콜을 호출할 수 있지만, Seccomp가 적용된 프로세스는 필터링 규칙에 따라 허용된 목록(Allow-list) 외의 호출이 즉시 차단된다.*

### 5. 📢 섹션 요약 비유
> **"복잡한 관공서의 모든 민원실을 열어두는 대신, 오직 '민원서류 접수' 창구 하나만 개방하고 나머지는 모두 철문으로 용접해 버리는 것과 같습니다. 직원(해커)이 아무리 다른 업무를 시도해도 문 자체가 없어 실행할 수 없습니다."**

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 (상세 분석)
Seccomp 시스템은 크게 유저 공간의 인터페이스와 커널 공간의 필터 엔진으로 나뉜다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 관련 프로토콜/구조 | 비유 |
|:---|:---|:---|:---|:---|
| **BPF (Berkeley Packet Filter)** | 필터링 규칙 해석기 | 네트워크 패킷 필터링용으로 설계된 가상 머신을 시스템 콜 인자 검사에 재활용 | `BPF_STMT`, `BPF_JUMP` | 스마트 CCTV 분석 소프트웨어 |
| **seccomp_data 구조체** | 시스템 콜 컨텍스트 | 호출된 시스템 콜 번호, 아키텍처, 인자(args) 값을 담는 메모리 블록 | `struct seccomp_data` | 현장 검증 서류 봉투 |
| **LSM (Linux Security Modules) Hook** | 커널 내 연결 고리 | 시스템 콜 처리 경로 중 `security_task_prctl` 등의 훅을 통해 필터 로직 호출 | LSM Hooks | 경비반 출동 명령서 |
| **Task Struct** | 프로세스 상태 저장 | 커널 내 프로세스 정보 구조체에 필터 모드(Strict/Filter)와 BPF 프로그램 포인터 저장 | `task_struct->seccomp` | 보안 등급 카드 |
| **Audit Subsystem** | 로깅 및 모니터링 | 차단된 시스템 콜의 상세 정보를 syslog(Auditd)에 기록하여 보안 관제 | `audit_log_*` | 침입 시도 기록부 |

### 2. Seccomp-BPF 아키텍처 다이어그램
아래는 유저 영역에서 필터를 로드하고, 커널 진입 시 시스템 콜을 검사하는 흐름을 도식화한 것이다.

```text
   +-------------------+
   |  User Application |
   | (e.g., Web Server)|
   +---------+---------+
             |
             | 1. prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)
             |    (BPF Bytecode 로드 요청)
             v
   +-------------------------------------------------------+
   |                    Linux Kernel                       |
   |                                                       |
   |   +------------------+      +-----------------------+ |
   |   |   Seccomp Layer  |      |   BPF Interpreter     | |
   |   +--------+---------+      +----------+------------+ |
   |            |                           ^              |
   |            | (save filter)             | (execute)    |
   |            v                           |              |
   |   +--------+---------+                                |
   |   | Task Struct      |  Filter Rules   |              |
   |   | (task->seccomp)  | <---------------+              |
   |   +--------+---------+                                |
   |            |                                          |
   |            | 2. System Call Trap (e.g., socket())     |
   |            v                                          |
   |   +--------+---------+                                |
   |   |  Secure Computing| <--- Hook Point (entry_SYSCALL)|
   |   |      Check       |                                |
   |   +--------+---------+                                |
   |            |                                          |
   |    +-------+-------+                                  |
   |    | Evaluation?  |                                  |
   |    +-------+-------+                                  |
   |            |                                          |
   |    [YES]   |   [NO] (Allow)          [NO] (Deny)       |
   |     +------+--------+       +-------------+           |
   |     | KILL_PROCESS   |       | Run Syscall |           |
   |     | (SIGSYS)       |       | (return to  |           |
   |     +----------------+       |  userspace) |           |
   |                               +-------------+           |
   +-------------------------------------------------------+
```

### 3. 다이어그램 상세 해석 (200자+)
위 다이어그램은 Seccomp가 커널 내부에서 시스템 콜 처리 경로 중간에 **훅(Hook)**을 형성하여 필터링을 수행하는 과정을 보여준다.
1. **필터 로드(①)**: 사용자 공간의 프로세스는 `prctl()` 시스템 콜을 통해 BPF 바이트코드를 커널에 전달한다. 커널은 이 코드의 무해성을 검증한 후 현재 프로세스의 `task_struct` 내부에 저장한다. 이 과정은 일회성으로 수행된다.
2. **시스템 콜 인터셉트(②)**: 애플리케이션이 시스템 콜을 호출하면, 소프트웨어 인터럽트(Trap)가 발생하여 커널 모드로 진입한다. 이때 기존 시스템 콜 핸들러가 실행되기 직전에 Seccomp 레이어가 개입한다.
3. **필터링 수행(③)**: 커널 내장된 BPF 가상 머신이 로드된 규칙을 실행하여 현재 시스템 콜 번호와 아규먼트가 허용 목록(Allow-list)에 있는지 확인한다. 이 과정은 매우 빠르며(JIT 컴파일 지원), 캐시를 적극 활용한다.
4. **결과 처리(④)**: 검증 결과에 따라 허용될 경우 원래의 시스템 콜 핸들러가 실행되어 정상적인 기능을 수행하지만, 거부될 경우 커널은 즉시 프로세스를 강제 종료(`SIGKILL`)하거나 에러 코드(`EPERM`)를 반환하여 악의적인 행위를 차단한다. 이때 감사(Audit) 로그가 남는다.

### 4. 핵심 동작 알고리즘 및 코드
Seccomp 필터는 `sock_fprog` 구조체를 사용하여 정의되며, 보통은 **libseccomp** 라이브러리를 활용하지만 내부 원리를 이해하기 위해 원시 코드를 살펴본다.

**BPF 필터 로드 예시 (C언어 & libseccomp)**
```c
#include <linux/seccomp.h>
#include <sys/prctl.h>
#include <seccomp.h> /* libseccomp 래퍼 */

/* 실무에서는 복잡한 BPF 명령어를 직접 코딩하기보다 라이브러리를 사용함 */

void apply_seccomp_filter(void) {
    /* scmp_filter_ctx: 필터 컨텍스트 생성 (기본 정책: KILL) */
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);

    /* 1. 기본적인 시스템 콜 허용 (파라미터 검증 없음) */
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);

    /* 2. 복잡한 규칙 예: write는 fd 1(stdout/stderr)에만 허용 */
    /* 인자 0(arg 0)이 1보다 크면(K) 에러 발생(Errno EPERM) */
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(write), 1,
                     SCMP_A0(SCMP_CMP_GT, 1)); // arg0 > 1 check

    /* 3. 커널에 필터 로드 및 컨텍스트 해제 */
    if (seccomp_load(ctx) >= 0) {
        // 성공: 이 프로세스는 위 syscall만 사용 가능
    } else {
        // 실패: 보안 정책 적용 실패 (프로세스 종료 권장)
    }
    seccomp_release(ctx);
}
```
*코드 분석: 이 코드는 `write` 시스템 콜에 대해 BPF 비교문(`SCMP_CMP`)을 사용하여 파일 디스크립터(`fd`)를 검사한다. 이처럼 단순 호출 여부뿐만 아니라 호출 인자까지 검증하는 것이 Seccomp-BPF의 강점이다.*

### 5. 📢 섹션 요약 비유
> **"고속도로 톨게이트에 스마트 요금소(Seccomp Filter)를 설치하여, 차량 번호(System Call)와 적재货物(Arguments)를 스캔합니다. 허용 목록에 없거나 위험 물질을 싣고 있는 차량은 진입 즉시 차량을 압수(Kill)하고 목록에 있는 차량만 통과(Allow)시키는 강력한 출입 통제 시스템입니다."**

+++

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: Seccomp vs AppArmor vs Firejail

| 구분 (Criteria) | **Seccomp** | **AppArmor (MAC)** | **Firejail (User-Space Wrapper)** |
|:---|:---|:---|:---|
| **작동 계층 (Layer)** | **커널 레벨** (System Call Interface) | **커널 �