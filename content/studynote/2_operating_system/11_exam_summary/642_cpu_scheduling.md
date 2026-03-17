+++
title = "642. 운영체제 핵심 요약 - CPU 스케줄링"
date = "2024-05-23"
weight = 642
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "CPU 스케줄링", "CPU Scheduling", "Preemptive", "Non-preemptive", "SJF", "Round Robin"]
+++

> **[Insight]**
> CPU 스케줄링은 한정된 CPU 자원을 대기 중인 프로세스들에게 최적으로 배분하여 시스템의 처리량(Throughput)을 극대화하고 응답 시간(Response Time)을 최소화하는 의사결정 과정이다.
> 스케줄링 알고리즘의 선택은 시스템의 성격(Batch vs Interactive vs Real-time)에 따라 달라지며, 공정성(Fairness)과 효율성 사이의 트레이드오프(Trade-off)를 정밀하게 조율하는 것이 핵심이다.
> 현대 OS는 다단계 큐(Multi-level Queue)와 피드백(Feedback) 메커니즘을 결합하여 동적인 워크로드 변화에 유연하게 대응하고 있다.

+++

### Ⅰ. 스케줄링의 목적과 단계

1. 스케줄링의 주요 목표
   - **이용률(Utilization) 극대화**: CPU가 가능한 한 바쁘게 일하도록 유지한다.
   - **처리량(Throughput) 증대**: 단위 시간당 완료되는 프로세스 수를 늘린다.
   - **반환 시간(Turnaround Time) 최소화**: 프로세스 제출부터 완료까지의 시간을 단축한다.
   - **응답 시간(Response Time) 단축**: 대화형 시스템에서 요청에 대한 첫 응답 시간을 줄인다.

2. 스케줄링 단계
   - **장기(Long-term) 스케줄링**: 어떤 프로세스를 준비 큐(Ready Queue)에 넣을지 결정 (Job Scheduler).
   - **중기(Mid-term) 스케줄링**: 메모리 부족 시 프로세스를 일시적으로 제거(Swap-out)하여 차수(Degree of Multiprogramming)를 조절.
   - **단기(Short-term) 스케줄링**: 실행할 프로세스를 준비 큐에서 선택하여 CPU를 할당 (CPU Scheduler).

📢 섹션 요약 비유: 놀이공원 입구에서 입장객을 받는 것(장기), 너무 붐비면 잠시 휴게소로 보내는 것(중기), 그리고 실제 놀이기구에 태우는 순서를 정하는 것(단기)과 같습니다.

+++

### Ⅱ. 선점(Preemptive) vs 비선점(Non-preemptive) 스케줄링

1. 비선점(Non-preemptive) 스케줄링
   - 프로세스가 자발적으로 CPU를 반납할 때까지 다른 프로세스가 CPU를 빼앗을 수 없는 방식이다.
   - 장점: 응답 시간 예측이 용이하고 컨텍스트 스위칭 오버헤드가 적다.
   - 단점: 짧은 작업이 긴 작업 뒤에서 무한정 기다리는 convoy effect(호송 효과)가 발생할 수 있다.

2. 선점(Preemptive) 스케줄링
   - 우선순위가 높거나 타임 슬라이스가 만료된 경우 OS가 강제로 CPU를 회수하는 방식이다.
   - 장점: 대화형 시스템 및 실시간 시스템에 적합하며 응답성이 높다.
   - 단점: 잦은 컨텍스트 스위칭으로 인한 오버헤드와 동기화 문제가 발생한다.

```text
[ Preemptive vs Non-preemptive ]

   Non-preemptive: [ P1 (Complete) ] -> [ P2 (Complete) ]
   
   Preemptive:     [ P1 (Part) ] -> [ P2 (Part) ] -> [ P1 (Part) ]
                    ^ Interrupt      ^ Interrupt
```

📢 섹션 요약 비유: 비선점은 '은행 창구'에서 한 손님 업무가 끝날 때까지 기다리는 것이고, 선점은 '응급실'에서 더 급한 환자가 오면 먼저 처치하는 것과 같습니다.

+++

### Ⅲ. 주요 스케줄링 알고리즘 분석

1. FCFS(First-Come, First-Served)
   - 먼저 도착한 순서대로 처리. 비선점형. convoy effect 발생 위험.
2. SJF(Shortest Job First)
   - 실행 시간이 짧은 프로세스 우선 처리. 평균 대기 시간 최소화(Optimal). 기아(Starvation) 현상 가능성.
3. HRN(Highest Response-ratio Next)
   - SJF의 기아 현상을 보완하기 위해 '에이징(Aging)' 기법 도입. (대기시간+서비스시간)/서비스시간 비율 적용.
4. RR(Round Robin)
   - 동일한 타임 슬라이스(Time Quantum)를 할당하여 순환 처리. 선점형. 시분할 시스템의 표준.
5. 우선순위(Priority) 스케줄링
   - 특정 기준에 따라 우선순위 부여. 낮은 우선순위의 무한 대기 문제는 에이징으로 해결.

📢 섹션 요약 비유: FCFS는 줄 서기, SJF는 빨리 끝날 사람 먼저 하기, RR은 뷔페에서 한 접시씩 돌아가며 담는 것과 같습니다.

+++

### Ⅳ. 다단계 큐(Multi-level Queue)와 피드백 큐(MLFQ)

1. 다단계 큐(Multi-level Queue)
   - 프로세스 성격(시스템, 대화형, 배치 등)에 따라 준비 큐를 여러 개로 분리하여 독자적인 스케줄링 적용.
2. 다단계 피드백 큐(Multi-level Feedback Queue, MLFQ)
   - 프로세스가 큐 사이를 이동할 수 있게 하여 CPU 집중형과 I/O 집중형 프로세스를 동적으로 구분.
   - 하위 큐로 갈수록 타임 슬라이스를 길게 주어 오버헤드를 줄이고 상위 큐에는 높은 우선순위를 부여.

📢 섹션 요약 비유: 공항에서 'VIP/비즈니스/이코노미' 줄을 따로 세우되, 상황에 따라 줄을 옮겨주며 최적의 탑승 순서를 찾는 고도화된 시스템입니다.

+++

### Ⅴ. 다중 프로세서 및 실시간 스케줄링

1. 다중 프로세서 스케줄링(Multi-Processor Scheduling)
   - 부하 균형(Load Balancing): CPU 간 작업 분산.
   - 프로세서 친화성(Processor Affinity): 이전에 실행된 CPU에서 다시 실행되도록 유도 (캐시 효율성).
2. 실시간 스케줄링(Real-time Scheduling)
   - **Soft Real-time**: 마감 시간(Deadline) 준수가 중요하지만 치명적이지 않음.
   - **Hard Real-time**: 마감 시간을 반드시 지켜야 하며, 실패 시 시스템 파손 우려.
   - RMS(Rate Monotonic) 및 EDF(Earliest Deadline First) 알고리즘 사용.

📢 섹션 요약 비유: 여러 개의 주방 화구를 동시에 관리하며, 특히 '주문 후 5분 내 서빙'이라는 엄격한 시간을 반드시 지켜야 하는 특수 요리 상황과 같습니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 프로세스 관리(Process Management)
- **자식 노드**: 임계 영역(Critical Section), 동기화 도구(Synchronization Tools)
- **연관 키워드**: Time Quantum, Starvation, Convoy Effect, Aging, Gantt Chart

### 👶 어린아이에게 설명하기
"우리 친구들, 미끄럼틀을 탈 때 줄을 서는 규칙이 있지? CPU 스케줄링은 그 '순서 정하기 규칙'이란다. 어떤 친구는 먼저 왔으니까 먼저 타고(FCFS), 어떤 친구는 빨리 내려갈 수 있으니까 먼저 타고(SJF), 또 어떤 때는 모든 친구가 10초씩만 돌아가면서 타기도 해(RR). 운영체제 대장님이 이렇게 순서를 잘 정해주면, 아무도 속상해하지 않고 모든 친구가 즐겁게 미끄럼틀을 탈 수 있단다!"