+++
title = "03. CPU 스케줄링 (CPU Scheduling)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-operating-system"
kids_analogy = "학교 식당에서 배가 고픈 친구들이 줄을 서 있을 때, 누가 먼저 밥을 먹을지 정해주는 '줄세우기 선생님'과 같아요. 공부를 많이 해야 하는 친구나, 아주 급한 친구를 먼저 보내주기도 한답니다!"
+++

# 03. CPU 스케줄링 (CPU Scheduling)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 한정된 CPU 자원을 대기 중인 여러 프로세스에게 효율적으로 배분하여 시스템 성능을 극대화하는 기법.
> 2. **가치**: CPU 이용률 향상, 처리량 증대, 응답 시간 단축 및 기아 현상(Starvation) 방지를 통한 공정성 확보.
> 3. **융합**: 선점(Preemptive)과 비선점(Non-preemptive) 방식의 조화를 통해 실시간성 및 처리 효율 동시 달성.

---

### Ⅰ. 개요 (Context & Background)
CPU 스케줄러는 시스템의 '교통 정리원'이다. 어떤 프로세스를 Running 상태로 보낼지 결정하며, 이는 시스템 전체의 사용자 경험과 서버의 처리량에 직격탄을 날리는 핵심 로직이다.

---

### Ⅱ. 아키텍처 및 핵심 원리

#### 1. 주요 스케줄링 알고리즘
- **FCFS**: 먼저 온 순서대로 처리 (비선점, Convoy Effect 발생 가능)
- **SJF**: 실행 시간이 짧은 것부터 처리 (Starvation 발생 가능)
- **Round Robin**: 시분할 단위(Time Quantum)로 공평하게 배분 (선점형)
- **Multi-level Feedback Queue (MLFQ)**: 현대 OS의 표준, 우선순위 가변 조정

#### 2. 스케줄링 상태 전이도 (ASCII)
```text
    [ Process State Transitions ]
    
    (Admit)    (Dispatch)         (Interrupt)
    New ----> Ready ----------> Running ----------> Terminated
                ^                |
                |   (I/O Wait)   |
                +---- Waiting <--+
                    (I/O Done)
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 선점 vs 비선점 스케줄링
| 구분 | 선점 (Preemptive) | 비선점 (Non-preemptive) |
| :--- | :--- | :--- |
| **방식** | 강제로 CPU 탈취 가능 | 스스로 CPU를 반납할 때까지 대기 |
| **장점** | 응답성이 좋음 (대화형 시스템) | 문맥 교환 오버헤드 적음 |
| **단점** | 잦은 문맥 교환 비용 발생 | 긴 작업이 CPU 독점 시 응답성 저하 |
| **사례** | Windows, Linux, RR | 구형 OS, Batch 처리 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
실무적으로 **Time Quantum**의 결정은 예술에 가깝다. 너무 크면 FCFS와 같아지고, 너무 작으면 문맥 교환 비용이 성능을 압도한다. 기술사는 시스템의 부하 특성을 분석하여 리눅스의 CFS(Completely Fair Scheduler)와 같은 고도화된 스케줄링 정책을 미세 조정(Tuning)해야 한다.

---

### Ⅴ. 기대효과 및 결론
스케줄링은 멀티코어 및 분산 환경에서 더욱 복잡해지고 있다. 향후 AI 기반의 동적 스케줄링 기술이 도입되어 워크로드의 특성을 미리 예측하고 최적의 자원을 할당하는 지능형 OS로 진화할 것이다.
