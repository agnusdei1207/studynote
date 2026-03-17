+++
title = "439. Cgroups 메모리 서브시스템의 자원 제한 동작"
date = "2026-03-14"
weight = 439
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Cgroups(Control Groups) 메모리 서브시스템은 프로세스 그룹별로 사용할 수 있는 물리 메모리 및 스왑 공간의 총량을 제한하고 감시하는 리눅스 커널의 자원 격리 메커니즘이다.
> 2. **가치**: 컨테이너 환경(Docker, K8s)의 핵심 기반 기술로, 특정 앱의 메모리 누수나 폭주가 전체 시스템이나 다른 컨테이너의 안정성을 해치지 않도록 방지(OOM Isolation)한다.
> 3. **융합**: 커널의 메모리 할당자(Page Allocator), 재회수 로직(Reclaim), 그리고 OOM 킬러가 Cgroup 계층 구조와 연동되어 정교하게 동작한다.

---

### Ⅰ. 개요 (Context & Background)

- **概念**: **Cgroups Memory Subsystem (memcg)**은 프로세스들을 그룹으로 묶어 해당 그룹이 소비하는 메모리 통계를 유지하고 제한을 거는 기술이다. 단순히 전체 메모리 크기만 제한하는 것이 아니라, 페이지 캐시, 익명 메모리, 커널 스택 등 다양한 메모리 사용처를 정밀하게 제어한다.

- **💡 비유**: 한 아파트(물리 메모리)에 여러 가구(프로세스 그룹)가 사는데, 각 가구가 쓸 수 있는 전기나 수도의 양(메모리 한도)을 미리 정해두는 것과 같다. 한 가구가 물을 너무 많이 써도 다른 집 수압이 낮아지지 않도록 밸브를 조절하는 역할을 한다.

- **등장 배경**:
  1. **멀티테넌시(Multi-tenancy) 환경**: 서버 한 대를 여러 사용자가 나눠 쓸 때 자원 점유 분쟁을 해결해야 했다.
  2. **컨테이너화의 확산**: 프로세스 단위의 가상화를 위해 독립적인 자원 한도 설정이 필수적이었다.
  3. **예측 가능한 시스템**: 특정 프로세스의 메모리 폭주(Memory Spike) 상황에서도 시스템 핵심 서비스는 살아남아야 했다.

- **📢 섹션 요약 비유**: 뷔페 식당에서 특정 손님이 음식을 싹쓸이하지 못하도록, 1인당 접시 수와 담을 수 있는 양을 제한하는 공정한 배급 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### Cgroups 메모리 제한 및 재회수 흐름

```text
 [ Process Group A ]      [ Memory Controller (memcg) ]      [ Kernel Memory ]
         │                            │                             │
    1. Try Allocate ───▶ 2. Charge to Cgroup ─────────────────────▶ │
         │               (Check limit)                              │
         │                            │                             │
         │               3. Over Limit? ───▶ 4. Reclaim Triggered   │
         │                            │     (Try to free Page Cache)│
         │                            │                             │
         │               5. Still Over? ───▶ 6. OOM Killer (Local)  │
         │                            │     (Kill Process in Group A)
```

**[다이어그램 해설]**
1. **Charging**: 프로세스가 메모리를 할당받으려 하면 커널은 해당 프로세스가 속한 Cgroup의 카운터를 올린다.
2. **Limit Check**: 설정된 `memory.limit_in_bytes`(v1) 또는 `memory.max`(v2)를 초과하는지 확인한다.
3. **Reclaim**: 한도에 도달하면 커널은 즉시 해당 Cgroup 내에서 재회수(Reclaim) 가능한 페이지(예: 안 쓰는 페이지 캐시)를 찾아 비운다.
4. **OOM Killer**: 재회수 후에도 메모리가 부족하면, 전체 시스템이 아닌 **해당 Cgroup 내의 프로세스 중 하나**를 골라 종료시킨다.

- **📢 섹션 요약 비유**: 가계부에 기록된 한도를 넘으려 하면 먼저 안 쓰는 물건을 중고로 팔아(Reclaim) 돈을 마련해보고, 그래도 안 되면 가장 돈을 많이 쓰는 가족의 카드(Process)를 정지시키는 관리 방식입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 주요 파라미터 및 동작 차이

| 파라미터 (v2 기준) | 의미 | 동작 특성 |
|:---|:---|:---|
| **memory.low** | 최저 보장(Reservation) | 시스템 전체 메모리 부족 시에도 이 수치까지는 재회수하지 않음 |
| **memory.high** | 소프트 제한(Throttle) | 이 수치를 넘으면 프로세스 속도를 늦춰(Throttling) 할당 억제 |
| **memory.max** | 하드 제한(Hard Limit) | 절대 넘을 수 없는 선. 초과 시 즉시 재회수 및 OOM 발생 |
| **memory.swap.max** | 스왑 제한 | 그룹이 사용할 수 있는 최대 스왑 공간 제한 |

- **📢 섹션 요약 비유**: '최소 용돈(low)'은 건드리지 않고, '권장 소비액(high)'을 넘으면 잔소리를 하며, '신용카드 한도(max)'를 넘으면 결제를 차단하는 단계별 자원 관리와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 실무 시나리오: 쿠버네티스(K8s)의 Requests vs Limits
쿠버네티스에서 Pod 설정 시 `requests`는 Cgroup의 CPU/Memory 보장(cpu.shares 등)에 관여하고, `limits`는 `memory.max` 설정을 통해 물리적인 상한선을 긋는다. 기술사적으로 중요한 점은 **메모리는 CPU와 달리 비압축성 자원(Non-compressible Resource)**이라는 것이다. CPU는 한도를 넘으면 조금 느려질 뿐이지만, 메모리는 한도를 넘으면 프로세스가 즉사(OOM Kill)한다. 따라서 실무에서는 Java VM의 Heap 크기와 Cgroup Limit 사이의 간격(Headroom)을 적절히 두는 설계가 매우 중요하다.

- **📢 섹션 요약 비유**: 도로는 차가 많아지면 막히기만 하지만(CPU), 엘리베이터는 정원을 초과하면 아예 움직이지 않고 사람을 내리게 하는 것(Memory)과 같은 차이입니다.

---

### Ⅴ. 기대효과 및 결론

#### Cgroups 메모리 제어의 기대효과
1. **시스템 안정성(Stability)**: 이른바 'Noisy Neighbor' 문제를 해결하여 여러 서비스가 평화롭게 공존하게 한다.
2. **자원 효율성(Efficiency)**: 서버의 물리 자원을 낭비 없이 꽉 채워 쓸 수 있는(Bin-packing) 기술적 근거를 제공한다.
3. **과금 모델의 기초**: 클라우드 서비스에서 사용자가 사용한 만큼만 비용을 지불하게 하는 정확한 측정 도구가 된다.

- **📢 섹션 요약 비유**: 울타리를 쳐서 양들이 서로의 풀밭을 침범하지 않게 함으로써, 목장 전체의 풀이 골고루 잘 자라게 만드는 지혜로운 목동의 기술입니다.

---

### 📌 관련 개념 맵
- **Namespace**: Cgroups와 함께 컨테이너 격리를 완성하는 기술 (View 격리).
- **OOM Killer**: 메모리 부족 시 프로세스를 강제 종료하는 커널 핸들러.
- **Pressure Stall Information (PSI)**: 자원 부족으로 인한 시스템 지연 정도를 측정하는 지표.

---

### 👶 어린이를 위한 3줄 비유 설명
1. Cgroups는 여러 명의 친구가 컴퓨터 한 대를 같이 쓸 때, 각자 쓸 수 있는 가방(메모리) 크기를 정해주는 규칙이에요.
2. 한 친구가 욕심내서 가방을 너무 크게 만들면 다른 친구들이 불편하니까, 선생님(커널)이 딱 정해진 크기만 쓰게 감시한답니다.
3. 만약 정해진 크기보다 더 많은 장난감을 넣으려 하면, 선생님이 "안 돼!"라고 말하며 장난감을 하나 빼버리기도 해요.

---

### 🚀 지식 그래프 (Knowledge Graph)
```mermaid
graph TD
    Cgroup[Control Group] --> MemSub[Memory Subsystem]
    MemSub --> Stats[Usage Statistics]
    MemSub --> Limits[Hard/Soft Limits]
    Limits --> Reclaim[Memory Reclaim Process]
    Reclaim -- Fails --> OOM[Cgroup-aware OOM Killer]
    MemSub --> Swap[Swap Control]
    subgraph ContainerRuntime[Docker / K8s]
        Cgroup
    end