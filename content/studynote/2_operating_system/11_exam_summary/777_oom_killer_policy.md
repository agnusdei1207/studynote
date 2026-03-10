+++
weight = 777
title = "777. OOM (Out Of Memory) 킬러의 동작 원리와 메모리 보호 정책"
date = "2026-03-10"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "OOM Killer", "Out Of Memory", "oom_score", "메모리 부족", "커널 보호", "자원 회수"]
series = "운영체제 800제"
+++

# OOM (Out Of Memory) 킬러의 동작 원리와 보호 정책

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 운영체제가 가용 물리 메모리와 스왑 공간을 모두 소진했을 때, 전체 시스템이 멈추는 것을 막기 위해 **특정 프로세스를 강제로 종료(Kill)**하여 메모리를 확보하는 최후의 자구책.
> 2. **가치**: 가장 적은 노력으로 최대의 가용성을 확보할 수 있는 프로세스를 합리적인 알고리즘(**oom_score**)으로 선정하여, 핵심 시스템 서비스는 살리고 메모리 점유가 높은 비필수 작업부터 정리한다.
> 3. **융합**: 리눅스 커널의 가상 메모리 관리(MMU), Cgroups 자원 제한, 그리고 `/proc` 인터페이스를 통한 사용자 설정 권한이 결합된 자원 관리의 최종 집행 단계이다.

---

### Ⅰ. OOM 킬러 (Out Of Memory Killer)의 발생 조건

- **Overcommit**: 리눅스는 성능을 위해 실제 물리 메모리보다 더 많은 양을 프로세스에게 약속(Allocate)한다.
- **Panic vs Kill**: 모든 프로세스가 약속된 메모리를 실제로 사용하려 할 때 임계치에 도달하면, 커널은 시스템 전체를 중단(Kernel Panic)시킬지, 아니면 하나만 죽일지 결정한다. (대부분 Kill을 선택)

---

### Ⅱ. 희생자 선정 알고리즘 (oom_score)

커널은 각 프로세스마다 `oom_score`를 계산하며, 점수가 가장 높은 프로세스가 1순위 희생자가 된다.

| 점수 영향 요소 | 설명 | 점수 변화 |
|:---|:---|:---:|
| **메모리 점유량** | 프로세스가 사용 중인 페이지 수 (RSS). | **상승 (+)** |
| **실행 시간** | 오래 실행된 프로세스는 중요할 확률이 높음. | 하락 (-) |
| **사용자 권한** | root 권한의 프로세스는 보호 대상. | 하락 (-) |
| **자식 프로세스** | 자식이 많으면 같이 죽였을 때 회수량이 큼. | 상승 (+) |
| **사용자 설정** | `oom_score_adj` 값을 통해 수동 조절 가능. | 가변 |

---

### Ⅲ. OOM 킬러 동작 아키텍처 (ASCII)

```ascii
    [ System Memory Usage ]
    100% |#########################| <-- OOM Threshold
     95% |####################     | <-- Memory Low Warning
         +-------------------------+
    
    [ Kernel OOM Execution ]
    1. Page Allocation Fails
    2. Try to Reclaim (Flush Cache, Swap)
    3. Still No Memory?
    4. Call out_of_memory()
    5. Calculate oom_score for all processes
    6. Select Victim (Highest Score)
    7. Send SIGKILL to Victim Process
    8. Free Frames and Return to Kernel
```

---

### ④. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 핵심 서비스 보호 전략
- **문제**: DB 서버에서 메모리 부족 시 가장 점유율이 높은 DB 엔진(MySQL 등)이 OOM 킬러에 의해 죽어버리는 현상.
- **기술사적 결단**: 
  - 중요 프로세스의 `/proc/[PID]/oom_score_adj` 값을 **-1000**으로 설정하여 절대 죽지 않도록 보호한다.
  - 대신, 메모리 누수가 의심되거나 덜 중요한 배치 작업의 점수를 높여 우선 희생되도록 유도한다.

#### 2. 기술사적 인사이트: Cgroups 기반 OOM
- 시스템 전체 OOM 외에도, **Docker 컨테이너(Cgroups)**별로 설정된 메모리 한계를 넘을 때 해당 컨테이너 내부에서만 OOM 킬러가 작동할 수 있음을 인지하고, 컨테이너 리소스를 튜닝해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **시스템 생존력 확보**: 특정 앱의 메모리 누수가 전체 서버 다운으로 번지는 것을 차단.
- **무인 운영 가능성**: 관리자 개입 없이도 최악의 상황에서 스스로 자원을 회수하여 정상화.

#### 2. 미래 전망
최근에는 OOM이 발생하기 전, 미리 사용자에게 알림을 주거나(Memory Pressure Stall), 앱 스스로 메모리를 반납하도록 유도하는 **PSI (Pressure Stall Information)** 기술이 발전하고 있다. 또한, 인공지능이 과거의 OOM 이력을 분석하여 선제적으로 프로세스를 재시작하거나 스케일 아웃(Scale-out)을 지시하는 지능형 자원 관리 시스템으로 진화하고 있다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[메모리 누수](./612_memory_leak_detection.md)**: OOM 킬러가 가동되는 가장 흔한 소프트웨어 결함 원인.
- **[Cgroups](../10_security_performance_virtualization/439_topic.md)**: OOM 범위를 컨테이너 단위로 제한하는 기술.
- **[스와핑](../6_memory_management/335_swapping.md)**: OOM 킬러가 작동하기 전 단계의 자원 확보 노력.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **OOM 킬러**는 풍선(메모리)이 터지기 직전에 바늘로 구멍을 하나 톡 내서 바람을 빼주는 **'풍선 구조대'**와 같아요.
2. 풍선이 펑 터지면 다 같이 다치니까(시스템 다운), 가장 크고 덜 중요한 장난감부터 밖으로 던져서 풍선이 안 터지게 지키는 거죠.
3. 소중한 보물(핵심 앱)은 절대로 안 던지도록 선생님(OS)이 미리 약속을 정해둔답니다!
