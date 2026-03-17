+++
title = "cgroups (Control Groups) 자원 할당"
date = "2026-03-14"
weight = 668
+++

# cgroups (Control Groups) 자원 할당

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 제어 그룹 (Control Groups, cgroups)은 리눅스 커널의 핵심 서브시스템으로, 프로세스 그룹을 대상으로 **CPU (Central Processing Unit)**, 메모리, 디스크 입출력 (Block I/O) 등 물리 자원의 할당량을 제한하고 측정하는 격리 메커니즘입니다.
> 2. **가치**: 컨테이너 가상화 환경에서 'Noisy Neighbor (시끄러운 이웃)' 문제를 해결하여 특정 워크로드의 과도한 자원 독점을 방지하고, 서비스 수준 계약 (SLA: Service Level Agreement)을 보장하는 안정성을 제공합니다.
> 3. **융합**: 단일 커널 트리를 통합 관리하는 cgroups v2와 쿠버네티스 (Kubernetes)의 **QoS (Quality of Service)** 클래스가 결합하여, 클라우드 네이티브 환경에서 세분화된 자원 관리와 보안 격리의 표준으로 자리 잡고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

**cgroups (Control Groups)**은 리눅스 커널 버전 2.6.24에서 처음 도입되어, 다중 프로세스가 공유하는 시스템 자원을 그룹 단위로 통제하고 모니터링하는 기술입니다. 기존의 프로세스 격리가 논리적 공간 분리에 그쳤다면, cgroups은 물리적 자원 사용량 자체를 제어합니다.

가상화 기술이 발전함에 따라, 하나의 호스트 위에서 수십, 수백 개의 컨테이너가 실행되는 환경이 일상화되었습니다. 이때 특정 컨테이너가 악의적으로 또는 실수로 무한 루프를 돌거나 메모리를 누출시킨다면, 호스트 전체의 성능이 저하되는 **'Starvation (기아)'** 현상이 발생합니다. cgroups는 운영체제 차원에서 이러한 상황을 방지하기 위해 프로세스 계층 구조 (Process Hierarchy)와 무관하게 자원 관리 계층을 구축합니다.

### 💡 핵심 비유
이는 마치 **'고속도로 통행료 징수 시스템 (Tollgate System)'**과 같습니다. 수많은 차량(프로세스)이 도로(자원)를 이용하려 할 때, 톨게이트(cgroups)가 차량의 종류나 소속에 따라 진입 차로 수와 주행 가능 속도를 강제로 제한함으로써, 특정 차량이 도로를 점유하여 정체를 유발하는 것을 방지하는 원리입니다.

### 등장 배경 및 기술적 파급 효과
1.  **기존 한계**: 단순 프로세스 우선순위 (Nice 값) 조정만으로는 특정 프로세스가 CPU 코어를 100% 점유하는 것을 막을 수 없었음.
2.  **혁신적 패러다임**: 프로세스 그룹에 대한 'Hard Limit(물리적 상한)'을 설정하여, 시스템 관리자가 자원을 예산 관리처럼 정확하게 분배 가능.
3.  **현재 비즈니스 요구**: 클라우드 멀티테넌시 (Multi-tenancy) 환경에서 각 고객에게 보장된 성능을 제공하고, 과금 청구의 기초 데이터로 활용.

> 📢 **섹션 요약 비유**
> 호텔의 **'뷔페 이용 제도'**와 같습니다. 아무리 대식가 손님(특정 프로세스)이 방문하더라도, 호텔 측(cgroups)이 1인당 요리 접시를 5개로 제한하는 규칙을 적용하면, 남은 손님들이 굶는 일(서비스 거부) 없이 모두가 만족하며 식사를 할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

cgroups는 **VFS (Virtual File System)** 인터페이스를 통해 사용자 공간(User Space)과 상호작용합니다. `/sys/fs/cgroup/` 경로에 마운트된 가상 파일 시스템을 통해 설정을 변경하며, 이는 리눅스의 **"모든 것은 파일이다"**라는 철학을 따릅니다.

### 1. 핵심 구성 요소 (Components)

cgroups 시스템은 크게 4가지 핵심 개념으로 구성됩니다.

| 구성 요소 | 역할 | 내부 동작 프로세스 | 프로토콜/인터페이스 | 비유 |
|:---|:---|:---|:---|:---|
| **Task (태스크)** | 제어의 대상 | 시스템의 프로세스 또는 스레드 | PID (Process ID) | 도로를 달리는 자동차 |
| **Cgroup (제어 그룹)** | 자원 할당 단위 | Task들의 집합을 묶는 그룹 | 디렉토리 구조 | 차량 그룹 (예: 화물차 그룹) |
| **Subsystem (컨트롤러)** | 제어 로직 | 특정 자원(CPU/Mem)을 제어하는 커널 모듈 | Kernel Module | 교통정보 통제 센터 |
| **Hierarchy (계층 구조)** | 그룹 간 관계 | Cgroup들이 트리 형태로 연결된 구조 | Directory Tree | 도로망의 계층 (고속도로 -> 국도) |

### 2. 주요 서브시스템 (Controllers) 상세

cgroups는 각기 다른 자원을 관리하는 다양한 컨트롤러를 제공합니다. (※ 대표적인 5개 기술 집중 분석)

1.  **cpu**: **CFS (Completely Fair Scheduler)**를 통해 CPU 시간을 할당. `cpu.shares`(상대적 가중치) 또는 `cpu.cfs_quota_us`(절대적 시간 제한)를 사용.
2.  **memory**: 물리 메모리 및 **Swap** 메모리 사용량을 제한. `memory.limit_in_bytes` 설정 초과 시 **OOM Killer (Out Of Memory Killer)**가 프로세스를 종료시킴.
3.  **blkio (Block Input/Output)**: 블록 디바이스(HDD/SSD)에 대한 읽기/쓰기 대역폭과 **IOPS (Input/Output Operations Per Second)**를 제어.
4.  **cpuset**: 멀티코어 시스템에서 특정 CPU 코어와 메모리 노드(NUMA Node)에 프로세스를 바인딩하여 캐시 친화성을 높임.
5.  **pids**: 그룹 내 생성 가능한 프로세스 ID 개수를 제한하여 **Fork Bomb** 등의 공격을 방어.

### 3. ASCII 구조 다이어그램 및 데이터 흐름

아래는 사용자가 `memory.limit_in_bytes` 값을 설정했을 때, 커널 내부에서 이 값이 실제 프로세스 제어로 이어지는 아키텍처 흐름입니다.

```text
[ User Space: Admin ]
      |
      | 1. 설정 명령어 입력 (echo 1G > .../memory.limit_in_bytes)
      v
[ Virtual File System (VFS) ]
      |
      | 2. syscall write() 호출
      v
[ cgroups Core (Kernel) ]
      |
      +---> [ cgroup_subsys_state ]
      |      |
      |      | 3. 설정값 갱신 (Configuration Update)
      v
      |
[ Memory Controller (Driver) ]
      |
      | 4. Page Fault 발생 시마다 검사 (Hooking)
      v
[ Linux Kernel Memory Manager ]
      |
      | 5. 한도 초과 확인 (Limit Check)
      |    -> True : OOM Kill 신호 전송  /  False : 할당 승인
      v
[ Target Process ]
```

#### 다이어그램 해설
1.  **도입 (Introduction)**: 관리자가 `/sys/fs/cgroup/...` 경로에 제한 값을 기록하면, 이는 일반 파일 쓰기 작업처럼 보이지만 내부적으로는 **VFS**를 거쳐 커널의 cgroups 코어로 전달됩니다.
2.  **전달 (Delivery)**: cgroups 코어는 해당 요청을 담당하는 서브시스템(예: Memory Controller)으로 전달하고, 커널 메모리 관리자는 자신의 **자료 구조 (Page Table, LRU List)**에 이 제약 조건을 등록합니다.
3.  **실행 (Action)**: 대상 프로세스가 메모리 할당을 요청할 때마다(페이지 폴트 발생 시), 커널은 이 제약 조건을 확인합니다. 임계값을 초과하면 즉시 프로세스에 **SIGKILL** 시그널을 보내 강제 종료시킴으로써 시스템 붕괴를 막습니다.

### 4. 핵심 알고리즘 및 코드
리눅스 커널에서 cgroups 메모리 제한을 적용하는 핵심 로직은 페이지 폴트 핸들러 내부에 위치합니다. (개념적 의사코드)

```c
// Simplified Kernel Logic for Memory Cgroup
bool try_charge(struct page *page, struct mm_struct *mm) {
    struct mem_cgroup *memcg = get_mem_cgroup_from_mm(mm);
    
    // 현재 그룹의 사용량이 한계(limit)를 넘었는지 확인
    if (res_counter_charge(&memcg->res, PAGE_SIZE)) {
        // 1. 회수 시도 (Reclaim): 오래된 메모리를 해제하여 공간 확보
        if (try_to_free_mem_cgroup_pages(memcg) > 0) {
            return SUCCESS; // 회수 성공 시 할당 승인
        }
        
        // 2. OOM (Out of Memory) 트리거: 회수 불가능하면 프로세스 강제 종료
        mem_cgroup_out_of_memory(memcg);
        return FAIL; 
    }
    
    page->cgroup = memcg; // 페이지를 해당 cgroup에 귀속시킴
    return SUCCESS;
}
```

> 📢 **섹션 요약 비유**
> 건물의 **'전력 분전반과 차단기'**와 같습니다. 각 세입자(프로세스)는 배선반(cgroups)을 통해 전기를 공급받으며, 사용량이 계약된 **Ampere(암페어)**를 초과하면 회로가 자동으로 끊겨(Throttling/Killing), 건물 전체의 화재(시스템 다운)를 막습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

cgroups는 단순한 자원 제한을 넘어 가상화, 보안, 네트워킹 등 타 영역과 깊게 연결됩니다.

### 1. cgroups v1 vs cgroups v2 기술 비교
리눅스 커널 4.5부터 안정화된 cgroups v2는 v1의 구조적 복잡성을 해결했습니다.

| 비교 항목 | cgroups v1 (Legacy) | cgroups v2 (Unified) |
|:---|:---|:---|
| **계층 구조** | 각 컨트롤러마다 독립적인 트리 가능 (Mount per controller) | **단일 계층 구조 (Unified Hierarchy)**: 모든 컨트롤러가 하나의 트리 공유 |
| **프로세스 소속** | 여러 트리에 동시에 소속 가능 (다중 소속 허용) | 오직 하나의 트리에만 소속 가능 (관계 명확화) |
| **설정 방식** | 디렉토리별로 느슨하게 연결된 파일들 | **'eBPF (Extended Berkeley Packet Filter)'**와 연동된 제어 가능 |
| **디버깅 난이도** | 하이브리드 설정으로 인한 디버깅 어려움 | 단일 경로(`/sys/fs/cgroup/`)로 직관적 관리 |

### 2. 기술 융합 분석: Namespace와의 결합

```text
[ Container Architecture ]
      |
      +-- [ Namespaces ] (Visibility Isolation)
      |      |
      |      +-- UTS: Hostname 격리
      |      +-- NET: Network Stack 격리
      |      +-- PID: Process ID 격리
      |
      +-- [ cgroups ] (Resource Constraint)
             |
             +-- CPU, Memory: Resource 제한
```

-   **상관관계**: **Namespace (네임스페이스)**는 프로세스가 "보는" 시각을 가려주는 역할(예: 자기가 혼자 쓰는 OS라고 착각하게 함)을 한다면, cgroups는 실제 "쓰는" 행위를 제한하는 역할을 합니다.
-   **Synergy (시너지)**: Namespace만 있고 cgroups가 없다면, 컨테이너는 독립된 환경처럼 보이지만 여전히 호스트의 모든 자원을 쓸 수 있어 위험합니다. 반대로 cgroups만 있고 Namespace가 없다면, 자원은 제한되지만 프로세스가 다른 프로세스를 보고 조작할 수 있어 보안에 취약합니다. 둘의 결합으로 완벽한 **OS-level Virtualization**이 실현됩니다.

> 📢 **섹션 요약 비유**
> **'집과 열쇠'**의 관계입니다. Namespace는 집안의 벽으로 시선을 가리는 것(프라이버시)이고, cgroups은 현관문 열쇠로 실제 출입을 통제하는 것(권한)입니다. 벽이 있어도 열쇠가 없으면 남의 집을 들어갈 수 없듯, 두 기술은 상호 보완적으로 작동합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 cgroups는 주로 Docker, Kubernetes 등의 **CRI (Container Runtime Interface)** 하단에서 자동으로 적용되지만, 성능 튜닝을 위해 직접 제어해야 할 경우도 있습니다.

### 1. 실무 시나리오 의사결정

**문제 상황**: 웹 서비스 컨테이너가 간헐적으로 응답하지 않음.
**원인 파악**: 로그 분석 결과, 배치 작업 컨테이너가 CPU를 100% 점유하여 웹 서버의 CPU Time을 확보하지 못함(CPU Starvation).
**의사결정 과정**:
1.  **cpu.shares (1024 default)**: 웹 서버 그룹은 `2048`(2배 우선순위), 배치 그룹은 `512`(0.5배)로 설정하여 가중치 부여.
2.  **cpuset**: 배치 작업은 CPU Core 0~1번에만 고정(Binding), 웹 서버는 2~3번 사용하여 코어 간 간섭(Context Switching Overhead) 최소화.
3.  **결과**: 배치 작업은 느려지더라도 웹 서비스의 지연 시간(Latency)이 **SLA(50ms 이하)**를 준수함.

### 2. cgroups v2 도입 체크리스트

| 구분 | 체크항목 | 상세 내용 |
|:---|:---|:---|
| **기술적** | **Kernel Version** | 리눅스 커널 4.5 이상 또는 RHEL 8 이상 사용 여부 확인 |
| | **eBPF 지원** | cgroup v2의 장점인 eBPF 기반 모니터링 도구(BCC 등) 활용 가능 여부 |
| | **Controller 호환성** | 사용 중인 CRI(runc, containerd)가 cgroup v2 드라이