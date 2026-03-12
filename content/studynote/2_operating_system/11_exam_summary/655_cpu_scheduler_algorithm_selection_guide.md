+++
weight = 655
title = "655. CPU 스케줄러 알고리즘 선택 가이드"
date = "2024-05-23"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "CPU Scheduling", "Algorithm", "Selection Guide", "Throughput", "Response Time"]
+++

> **[Insight]**
> CPU 스케줄링(CPU Scheduling) 알고리즘은 시스템의 목적과 부하 특성에 따라 최적의 선택이 달라지며, 완벽한 만능 알고리즘은 존재하지 않는다.
> 알고리즘 선택은 처리량(Throughput), 대기 시간(Waiting Time), 응답 시간(Response Time), 자원 이용률(Utilization) 사이의 정교한 트레이드오프(Trade-off)를 수반한다.
> 현대의 범용 운영체제는 대화형 사용자와 배경 처리 작업을 동시에 만족시키기 위해 다단계 피드백 큐(MLFQ, Multi-Level Feedback Queue)와 같은 복합형 알고리즘을 주로 채택한다.

---

### Ⅰ. 스케줄링 알고리즘 선택 기준 (Criteria)

1. 사용자 관점 (User-Oriented)
   - **Response Time**: 대화형 시스템에서 사용자의 입력에 반응하는 시간의 최소화.
   - **Turnaround Time**: 프로세스 제출부터 완료까지의 총 소요 시간 단축.
2. 시스템 관점 (System-Oriented)
   - **Throughput**: 단위 시간당 처리 가능한 프로세스 수 극대화.
   - **CPU Utilization**: CPU가 항상 바쁘게 동작하도록 유지.
3. 공정성 (Fairness)
   - 특정 프로세스가 기아(Starvation) 현상을 겪지 않도록 자원을 골고루 분배.

📢 섹션 요약 비유: 스케줄러 알고리즘 선택은 '빠른 서비스(Fast Food)'를 제공할지, '정성스런 코스 요리(Fine Dining)'를 제공할지 결정하는 경영 전략과 같습니다.

---

### Ⅱ. 주요 알고리즘 비교 분석표

1. 비선점형(Non-preemptive) vs 선점형(Preemptive)
   - 강제로 실행을 중단시킬 수 있는지 여부에 따른 분류이다.

```text
[ CPU Scheduling Algorithm Guide ]

 Algorithm | Category | Best for... | Key Advantage | Key Disadvantage
-----------|----------|-------------|---------------|-----------------
 FCFS      | Non-Pre  | Batch Jobs  | Simple, Fair  | Convoy Effect
 SJF       | Non-Pre  | Batch Jobs  | Min Wait Time | Starvation
 RR        | Pre-emp  | Interactive | Low Response  | High Overhead
 Priority  | Both     | Real-time   | High Urgent   | Starvation
 MLFQ      | Pre-emp  | General OS  | Adaptive      | Complex Design
```

2. Convoy Effect (호위 효과)
   - FCFS에서 긴 작업 뒤에 짧은 작업들이 기다리며 대기 시간이 급증하는 현상.
3. Aging (에이징) 기법
   - Priority 스케줄링에서 오래 기다린 프로세스의 우선순위를 높여 Starvation을 방지하는 해법.

📢 섹션 요약 비유: 줄을 선 순서대로 처리할지(FCFS), 금방 끝날 사람부터 먼저 해줄지(SJF), 아니면 조금씩 돌아가며 처리할지(RR)를 정하는 규칙들입니다.

---

### Ⅲ. 상황별 알고리즘 선택 가이드

1. 일괄 처리 시스템 (Batch Systems)
   - 처리량(Throughput)이 중요하므로 FCFS나 SJF를 주로 사용하며, 문맥 교환 오버헤드를 줄인다.
2. 대화형 시스템 (Interactive Systems)
   - 응답성(Response Time)이 핵심이므로 RR(Round Robin)을 기반으로 하며, 사용자 경험을 우선시한다.
3. 실시간 시스템 (Real-time Systems)
   - 마감 시간(Deadline) 보장이 생명이므로 정적/동적 우선순위 기반 스케줄링(RMS, EDF)을 사용한다.
4. 범용 운영체제 (General Purpose OS)
   - 다양한 부하가 섞여 있으므로 MLFQ를 사용하여 대화형 작업에는 높은 우선순위를, CPU 위주 작업에는 긴 시간을 할당한다.

📢 섹션 요약 비유: 공장 생산 라인(Batch)에는 효율이 최고지만, 손님이 있는 매장(Interactive)에는 친절한 응대(Response)가 우선인 것과 같습니다.

---

### Ⅳ. Round Robin(RR) 타임 슬라이스(Quantum) 설정 가이드

1. Quantum이 너무 클 때 ($q \to \infty$)
   - FCFS와 동일해지며, 대화형 사용자의 응답 성능이 급격히 저하된다.
2. Quantum이 너무 작을 때 ($q \to 0$)
   - 문맥 교환 오버헤드가 CPU 시간을 모두 소모하여 실질적인 처리가 불가능해진다. (Processor Sharing)
3. 황금률 (Rule of Thumb)
   - 전체 작업의 약 80%가 단일 Quantum 내에 완료될 수 있는 수준으로 설정하는 것이 일반적이다.

📢 섹션 요약 비유: 손님에게 한 마디씩만 말할 기회를 주면(Too Small) 인사만 하다가 시간이 가고, 한 시간씩 주면(Too Large) 뒷사람이 도망가는 것과 같습니다.

---

### Ⅴ. 현대 멀티코어 환경의 스케줄링 트렌드

1. Processor Affinity (프로세서 친화성)
   - 특정 프로세스를 이전에 실행됐던 코어에 계속 할당하여 캐시 히트율을 높인다. (Soft/Hard Affinity)
2. Load Balancing (부하 균형)
   - 여러 CPU 코어 간의 작업 불균형을 해소하기 위해 Push Migration 또는 Pull Migration 기법을 사용한다.
3. Energy-Aware Scheduling (에너지 인지 스케줄링)
   - 성능과 전력 소모 사이의 균형을 위해 빅리틀(big.LITTLE) 아키텍처에 맞춰 스케줄링을 최적화한다.

📢 섹션 요약 비유: 능숙한 요리사에게 계속 같은 메뉴를 시키는 것(Affinity)이 효율적이며, 한 명만 바쁘면 다른 요리사에게 일을 나눠주는(Load Balancing) 전략입니다.

---

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 프로세스 관리(Process Management)
- **자식 노드**: FCFS, SJF, RR, MLFQ, 마감 시간 스케줄링(Deadline Scheduling)
- **연관 키워드**: Starvation, Convoy Effect, Time Quantum, Aging, Turnaround Time

### 👶 어린아이에게 설명하기
"놀이터에서 미끄럼틀을 탈 때 어떻게 타는 게 제일 좋을까? 줄을 선 순서대로 타는 방법도 있고, 빨리 내려오는 친구부터 먼저 타게 하는 방법도 있어. 그런데 운영체제라는 대장님은 어떤 친구는 조금만 타고 비켜주게 하고, 어떤 친구는 한 번에 많이 타게 하면서 모든 친구가 기분 좋게 놀 수 있도록 아주 복잡한 계산을 해서 순서를 정해준단다!"