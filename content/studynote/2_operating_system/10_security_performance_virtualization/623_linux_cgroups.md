+++
title = "623. 리눅스 컨트롤 그룹 (Cgroups) - 자원 제한 기술"
date = "2026-03-14"
weight = 623
+++

# 623. 리눅스 컨트롤 그룹 (Cgroups) - 자원 제한 기술

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리눅스 커널 레벨에서 프로세스 그룹의 **CPU, Memory, I/O** 등 물리 자원을 **정량적(Quantitative)**으로 제한, 모니터링, 제어하는 핵심 가상화 기술.
> 2. **가치**: "Noisy Neighbor" 문제를 해소하여 **Multi-Tenant 환경**에서의 **SLA (Service Level Agreement)** 준수와 시스템 안정성을 보장함. (Latency 최대 90% 절감 효과)
> 3. **융합**: **Docker**, **Kubernetes** 등 **Container Engine**의 자원 관리 엔진이자, **Cloud Native** 인프라의 기반이 되는 기술.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**Cgroups (Control Groups)**는 리눅스 커널에서 제공하는 기능으로, 하나 이상의 프로세스를 그룹화하여 시스템 자원(CPU, 메모리, 디스크 I/O, 네트워크 대역폭 등)의 사용량을 제한하고 우선순위를 할당할 수 있게 합니다. 단순히 프로세스를 격리하는 것(Network Namespace 등)을 넘어, **"물리적 자원을 얼마나 쓰게 할 것인가(Quota)"**를 강제력 있는 정책(Policy)으로 관리하는 기술입니다.

### 2. 등장 배경: 전용 하드웨어에서 공유 클라우드로
과거에는 하나의 물리 서버에 하나의 애플리케이션을 구동하는 전용 환경이 일반적이었습니다. 그러나 가상화 기술의 발전과 클라우드(Cloud) 컴퓨팅의 도래로, 하나의 호스트(OS) 위에서 수백 개의 워크로드가 구동되는 **MSA (Microservices Architecture)** 환경이 되었습니다. 이때 특정 프로세스가 무한 루프를 돌거나 메모리 누수가 발생하여 호스트 전체의 자원을 독점하면, 다른 중요한 서비스들이 멈추는 치명적인 상황이 발생합니다. 이러한 **Resource Contention (자원 경합)** 문제를 해결하기 위해 개발되었습니다.

### 3. Cgroups의 핵심 기능 (4대 기능)
Cgroups는 크게 네 가지 기능을 제공합니다.

1.  **Resource Limiting**: 그룹별로 자원 사용량의 상한(Hard Limit)을 설정 (예: CPU 2코어, RAM 1GB 초과 불가).
2.  **Prioritization**: 자원이 부족할 때 특정 그룹에 더 높은 우선순위(CPU Shares, I/O Weight)를 부여.
3.  **Accounting**: 자원 사용량을 실시간으로 측정하여 과금(Billing)이나 성능 분석의 기썰이터로 활용.
4.  **Control**: 프로세스 그룹 전체를 일시 중지(Freeze)하거나 재개(Resume)하여 체크포인트/복원 기능 구현.

> **💡 비유**: Cgroups는 거대한 공장(서버)의 **'전력 분배반 및 계량기'**와 같습니다. 어떤 부서가 전기를 너무 많이 쓰면 합선을 막기 위해 자동으로 차단기가 내려가고, 생산 라인의 중요도에 따라 전력 공급량을 조절합니다.

📢 **섹션 요약 비유**: Cgroups는 고속도로 톨게이트에서 **'차량(프로세스)마다 통과 가능 횟수를 제한하고, 화물차(무거운 작업)는 전용 차선으로 보내는 교통 통제 시스템'**과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 아키텍처 구성 요소 및 내부 동작
Cgroups는 크게 **Core(코어)**, **Controllers(서브시스템)**, **Hierarchy(계층 구조)**로 구성됩니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 | 관련 약어 |
|:---|:---|:---|:---|
| **cgroup Core** | 그룹 및 계층 구조 관리 | 프로세스(Task)를 특정 그룹에 연결하고 계층별 자원 정책을 적용하는 중앙 허브 | N/A |
| **Subsystem (Controller)** | 특정 자원 제어 담당 | `cpu`, `memory`, `blkio` 등 특정 자원에 대한 통제 로직을 수행 | CSS (Cgroup Subsystem) |
| **cgroupfs (Virtual FS)** | 사용자 인터페이스 제공 | `/sys/fs/cgroup/` 하위의 가상 파일 시스템을 통해 커널과 통신 (Read/Write) | VFS (Virtual File System) |
| **Task (Process)** | 제어 대상 | `fork()` 시 부모의 cgroup을 상속받거나 명시적으로 그룹 이동 | TID (Task ID) |

### 2. Cgroups 계층 구조 및 데이터 흐름 (ASCII)
Cgroups는 **Tree(트리)** 구조를 가집니다. 자식 노드는 부모 노드의 자원 한도 내에서 자원을 할당받습니다. 이를 통해 **Isolation(격리)**과 **Inheritance(상속)**를 동시에 달성합니다.

```text
      [ Root Cgroup (/) ]  <-- 시스템의 모든 자원 (Total Resources)
             |
    +--------+--------+
    |                 |
 [System Slice]    [User Slice]  <-- 상위 그룹 (cpu.shares=1024 vs 512 등)
    |                 |
    +                 +-----------------------+
    |                 |                       |
[ssh-daemon]    [user-1001.slice]       [docker.service]
    |                 |                       |
(PID: 1)         +---+---+               [Container A] [Container B]
                |       |                 |           |
           [app.db] [app.web]        (PID 101)     (PID 205)
           (MySQL)  (Nginx)          (Limit 1G)    (Limit 512M)

   * Key: [Cgroup Directory] -> (Associated Tasks/PIDs)
```

**해설**:
1.  **Root**: 시스템의 모든 자원을 소유합니다.
2.  **Slice**: systemd 단위에서 사용하는 상위 개념으로, 하위 단위들이 자원을 공유하는 영역입니다.
3.  **Scope/Unit**: 실제 서비스나 컨테이너가 배치되는 단위입니다. 위 그림에서 `Container A`는 1GB 메모리 제한이 걸려 있고, 내부의 PID 101 프로세스는 이 제한을 상속받습니다.

### 3. 핵심 알고리즘 및 심층 동작: CPU Scheduler와의 연동
**CFS Scheduler (Completely Fair Scheduler)**는 Cgroups의 정보를 바탕으로 스케줄링을 수행합니다.

```c
/* 리눅스 커널 구조체 예시 (Conceptual C Code) */
struct cgroup_subsys_state {
    /* 부모 cgroup에 대한 참조 (계층 구조 유지) */
    struct cgroup *parent;
    
    /* 자원 사용량 통계 */
    unsigned long usage;
};

/* 메모리 제한 초과 시 동작하는 페이지 폴트 핸들러 로직 */
if (pgfault && (mem_cgroup->usage > mem_cgroup->limit)) {
    if (current->flags & PF_OOM_ORIGIN) {
        /* OOM Killer 발동: 프로세스 강제 종료 */
        oom_killer(); 
    } else {
        /* Swap out or Reclaim */
        try_to_free_pages();
    }
}
```
이 코드는 커널이 페이지 폴트(Page Fault) 발생 시 해당 프로세스가 속한 `mem_cgroup`의 사용량이 제한(`limit`)을 초과했는지 확인하고, 초과 시 **OOM Killer (Out of Memory Killer)**를 호출하여 프로세스를 종료시키는 메커니즘을 개념적으로 보여줍니다.

### 4. 주요 컨트롤러별 제어 방식
-   **cpu**: `cpu.shares`(상대적 가중치, 기본값 1024), `cpu.cfs_quota_us`(절대적 시간 제한, 예: 100ms 중 50ms만 사용) 사용.
-   **memory**: `memory.limit_in_bytes`(물리+Swap 제한), `memory.memsw.limit_in_bytes`(Swap 포함 총량 제한) 사용.
-   **blkio**: `blkio.throttle.read_bps_device`(디스크별 읽기 초당 바이트 제한)를 통해 I/O 스톰 방지.

📢 **섹션 요약 비유**: 아키텍처는 **'기업 조직도와 예산 배정 시스템'**과 같습니다. 본사(Root)가 전체 예산을 가지고, 각 본부(Slice)에 예산을 할당하면, 각 팀(Controller)은 그 안에서 팀원들(Task)에게 업무량과 자원을 분배합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. Cgroups v1 vs v2: 구조적 진화
리눅스 커널 4.5부터 안정화된 **Cgroups v2**는 v1의 복잡성을 해결하고 통합 관리를 강화했습니다.

| 비교 항목 (Criteria) | Cgroups v1 (Legacy) | Cgroups v2 (Unified) |
|:---|:---|:---|
| **계층 구조 (Hierarchy)** | 각 컨트롤러(cpu, memory 등)마다 **독립적인 트리** 구조 가짐 | 모든 컨트롤러가 **단일 통합 트리** 구조 공유 |
| **프로세스 할당** | 프로세스가 서로 다른 컨트롤러 트리의 **다른 그룹**에 속할 수 있음 | 모든 컨트롤러에 대해 프로세스는 **동일한 경로**의 그룹에만 속해야 함 |
| **Thread 관리** | 전체 스레드 그룹만 제어 가능 (Coarse-grained) | **Thread-mode** 지원: 개별 스레드 단위 제어 가능 (Fine-grained) |
| **통합 관리** | 자원 간 상호작용 설정 어려움 (메모리와 I/O 분리) | **Memory-Pressure** 기반 I/O 제어 등 컨트롤러 간 협업 강화 |
| **주요 사용처** | 구형 리눅스 커널, 레거시 시스템 | 최신 배포판(Fedora, Ubuntu 22.04+), **Kubernetes** 표준 |

### 2. 기술 융합 분석: Cgroups + Namespaces = Container
컨테이너 기술은 Cgroups와 **Namespaces**의 융합 결과물입니다.

| 구분 | Namespaces | Cgroups |
|:---:|:---|:---|
| **역할** | **"보이는 것"을 격리** (Isolation) | **"쓰는 것"을 제한** (Limitation) |
| **대상** | PID, Mount, Network, UTS, IPC 등 | CPU, Memory, BlkIO, Devices |
| **철학** | 프로세스가 자신만의 독립된 OS인 것처럼 속임 | 프로세스가 시스템을 독점하지 못하게 막음 |
| **융합 시너지** | 격리된 공간에서 자원을 제한하여 **OS-level Virtualization** 구현 | 자원을 제한하면서 격리된 환경을 보장하여 **Multi-tenancy** 실현 |

> **💡 예시**: 웹 브라우저(Chrome)는 각 탭마다 **Process**를 생성하고, **Cgroups**로 메모리를 제한합니다. 하나의 탭이 멈추거나 과다 메모리를 사용해도 다른 탭이나 브라우저 자체는 죽지 않습니다.

📢 **섹션 요약 비유**: v1이 '각각 다른 스위치로 조명, 온도, 보일러를 제어하는 낡은 배전반'이라면, v2는 '스마트폰 앱 하나로 모든 것을 통합 제어하고 상황에 따라 자동 연동하는 스마트 홈 IoT 시스템'입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정 프로세스
**문제 상황**: 공개 웹 서비스(Apache)와 배치 작업(Spark)이 동일한 8코어 서버에서 구동 중입니다. 배치 작업이 시작되면 웹 서비스의 응답 속도가 급격히 느려집니다.

**의사결정 (Decision Matrix)**:
1.  **자원 진단**: `htop`, `iotop`을 통해 배치 작업이 CPU를 100%, Disk I/O를 100% 사용 중임을 확인.
2.  **정책 수립**:
    -   **Apache (Web)**: `cpu.shares=2048` (높은 우선순위), `blkio.weight=1000`
    -   **Spark (Batch)**: `cpu.cfs_quota_us=50000` (최대 50% 사용), `cpu.cfs_period_us=100000`
3.  **실행**: `systemd` 서드 유니트(Unit) 파일에 `CPUQuota=50%` 설정 후 데몬 재시작.
4.  **결과**: 배치 작업은 처리 시간이 2배 소요되지만, 웹 서비스의 **Latency는 평상시 수준으로 유지**됨. (비즈니스 임팩트 최소화)

### 2. 도입 및 운영 체크리스트
-   **[설정]** 커널 파라미터(`cgroup_enable=memory swapaccount=1`)가 부트 로더(grub)에 활성화되어 있는가?
-   **[모니터링]** `cgexec`, `systemd-cgtop` 명령어를 통해 실시간 자원 사용량을 추적하고 있는가?
-   **[보안]** 불필요한 디바이스 접근을 막기 위해 `devices` 컨트롤러를 통해 Device Whitelist를 적용했는가?
-   **[OOM]** OOM Killer가 터졌을 때, 로그(`/var/log/messages`)를 통해 어떤 Cgroup이 원인인지 식별 가능한가?

### 3. 안티패턴 (Anti-Pattern)
-   **잘못된 Limit 설정**: `memory.limit_in_bytes`를 물리 메모리보다 높게 설정하면 제한이 없는 것과 같음.
-   **Swap 의존**: 메모리 제한만 걸고 Swap을 끄지 않으면, 디스크 I/O 폭증으로 전체 성능이 저하될 수 있음.

📢 **섹션 요약 비유**: 실무 적용은 **'건물의 내진 설계 및 내화 설계'**와 같습니다. 화재(장애)가 발생해도 방화벽(Cgroups)을 통해 건물 전체(호스트)가 무너지는 것을 막고, 피해를 해당 구역(컨테이너)으로 한정시킵니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적 기대효과 (ROI)
| 지표 (Metric) | 도입 전 (Before) | 도입 후 (After) | 개선 효과 (Impact) |
|:---:|:---:|:---:|:---|
| **자원 격리율** | 0% (공유 경쟁) | 100% (완전 격리) | SLO(Service Level Objective) 준수유