+++
weight = 786
title = "786. 리눅스 Cgroups(Control Groups)의 자원 제한 및 컨테이너 격리"
date = "2026-03-10"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Cgroups", "Control Groups", "자원 제한", "Resource Limit", "컨테이너", "Docker", "Quotas"]
series = "운영체제 800제"
+++

# 리눅스 Cgroups(Control Groups)의 자원 제한 및 격리

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로세스들을 계층적인 그룹으로 묶어, 해당 그룹이 사용할 수 있는 **시스템 자원(CPU, Memory, Disk I/O, Network)의 양을 제어하고 제한**하는 리눅스 커널 기술.
> 2. **가치**: 특정 프로세스가 시스템 전체의 자원을 독점하여 다른 서비스에 영향을 주는 'Noisy Neighbor' 문제를 방지하며, 클라우드 환경의 **멀티테넌시(Multi-tenancy)** 구현을 가능케 한다.
> 3. **융합**: 보여지는 세상을 나누는 **Namespace** 기술과 결합하여 현대 '컨테이너(Docker)'의 물리적 실행 경계를 형성하는 핵심 축이다.

---

### Ⅰ. Cgroups (Control Groups)의 주요 서브시스템

각 자원별로 독립적인 제어기(Controller)가 존재한다.

| 서브시스템 | 제어 대상 | 주요 기능 |
|:---|:---|:---|
| **cpu** | CPU 시간 | 프로세스 그룹별 CPU 점유율(Shares) 및 할당 시간(Quota) 제어. |
| **memory** | 물리 메모리 | 프로세스 그룹의 최대 메모리 사용량 제한 및 OOM 발생 제어. |
| **blkio** | 블록 I/O | 디스크 읽기/쓰기 속도(BPS) 및 횟수(IOPS) 제한. |
| **cpuset** | CPU 코어 | 특정 프로세스 그룹이 사용할 수 있는 CPU 코어와 메모리 노드(NUMA) 지정. |
| **net_cls** | 네트워크 | 네트워크 패킷에 태그를 붙여 트래픽 제어(QoS)와 연동. |

---

### Ⅱ. Cgroups 작동 아키텍처 (ASCII)

가상 파일 시스템(cgroupfs) 인터페이스를 통해 자원을 관리한다.

```ascii
    [ User / Container Engine ]
    |  mkdir /sys/fs/cgroup/memory/my_container
    |  echo 512M > /sys/fs/cgroup/memory/my_container/memory.limit_in_bytes
    v
    +-----------------------------------------------------------+
    | [ Linux Kernel: Cgroups Engine ]                          |
    |                                                           |
    |  Hierarchy Management:                                     |
    |  Root ---+--- Group A (CPU: 20%)                          |
    |          +--- Group B (CPU: 80%)                          |
    |                                                           |
    |  Resource Accounting & Enforcement:                       |
    |  IF (Group A Usage > Limit) -> THROTTLE or KILL           |
    +-----------------------------|-----------------------------+
                                  v
    +-----------------------------------------------------------+
    | [ Physical Hardware: CPU / RAM / Disk ]                   |
    +-----------------------------------------------------------+
```

---

### Ⅲ. Cgroups v1 vs v2 차이점

| 구분 | Cgroups v1 | Cgroups v2 |
|:---|:---|:---|
| **구조** | 자원별 독립적 계층 (복잡) | **단일 통합 계층 (Unified)** |
| **일관성** | 서브시스템 간 연동 어려움 | 모든 자원이 동일한 프로세스 그룹 관리 |
| **기능** | 풍부함 (성숙도 높음) | 개선된 자원 제어 로직, 관리 단순화 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 컨테이너 자원 튜닝 (Kubernetes)
- **현상**: 특정 Pod가 메모리를 과도하게 사용하여 노드 전체가 느려지거나 재부팅됨.
- **기술사적 결단**: 
  - Kubernetes의 **`resources.limits`**를 설정하면 내부적으로 Cgroups의 `memory.limit_in_bytes`가 동작한다. 
  - 메모리 초과 시 해당 컨테이너만 죽이는 **OOM Killer**가 작동하도록 설계하고, CPU는 초과 시 죽이지 않고 성능만 제한하는 **Throttling** 방식을 적용한다.

#### 2. 기술사적 인사이트
- **Namespace vs Cgroups**: 네임스페이스는 "무엇을 볼 수 있는가(Isolation)"를 결정하고, Cgroups는 "얼마나 쓸 수 있는가(Quota)"를 결정한다. 이 두 조화가 깨지면 컨테이너는 껍데기만 남거나(보안 취약), 폭주하는 기관차(자원 고갈)가 된다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **SLA 보장**: 중요 서비스에 대한 자원 우선순위 보장.
- **인프라 밀도 향상**: 자원 낭비 없이 하나의 서버에 수백 개의 마이크로서비스 수용.

#### 2. 미래 전망
최근에는 하드웨어가 직접 Cgroups의 역할을 수행하는 **I/O 가속기**나 **SmartNIC**과의 연동이 강화되고 있다. 또한, AI 스케줄러가 실시간 부하를 예측하여 Cgroups 설정을 동적으로 바꾸는 **자율형 자원 관리** 기술이 클라우드 인프라의 핵심으로 자리 잡을 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[네임스페이스](./744_container_namespace_isolation.md)**: Cgroups와 짝을 이루는 격리 기술.
- **[OOM 킬러](./777_oom_killer_policy.md)**: Cgroups 메모리 한계 도달 시 호출되는 최종 집행자.
- **[도커 (Docker)](../../13_cloud_architecture/2_container_k8s/_index.md)**: Cgroups 기술을 활용하는 최상위 플랫폼.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **Cgroups**는 간식을 나눠주는 **'공평한 선생님'**과 같아요. 
2. 욕심쟁이 친구가 혼자서 모든 과자(자원)를 다 먹지 못하게, 한 명당 "딱 3개씩만 먹어!"라고 미리 양을 정해주는 규칙이죠.
3. 이 규칙 덕분에 모든 친구가 배고프지 않고 사이좋게 나눠 먹을 수 있답니다!
