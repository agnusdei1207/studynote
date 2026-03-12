+++
weight = 657
title = "657. 데드락(Deadlock) 탐지 및 회피 전략 체크리스트"
date = "2024-05-23"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Deadlock", "Banker's Algorithm", "Prevention", "Detection", "Recovery"]
+++

> **[Insight]**
> 데드락(Deadlock, 교착 상태)은 둘 이상의 프로세스가 서로가 가진 자원을 무한정 기다리며 시스템이 멈추는 치명적인 상태이다.
> 이를 해결하기 위해 발생 조건을 사전에 차단하는 예방(Prevention), 자원 요청 시 안전 상태를 검증하는 회피(Avoidance), 그리고 발생 후 조치하는 탐지 및 복구(Detection & Recovery) 전략을 계층적으로 운용해야 한다.
> 시스템의 효율성과 안전성 사이의 트레이드오프를 고려하여, 현대의 많은 OS는 오버헤드를 줄이기 위해 데드락이 발생하지 않는다고 가정하고 문제를 방치하는 '타조 알고리즘(Ostrich Algorithm)'을 응용 프로그램 수준의 해결에 맡기기도 한다.

---

### Ⅰ. 데드락 발생의 4가지 필수 조건 (Coffman's Condition)

1. Mutual Exclusion (상호 배제)
   - 최소한 하나의 자원은 비공유 모드여야 한다.
2. Hold and Wait (점유하며 대기)
   - 자원을 가진 상태에서 다른 자원을 추가로 요청하며 대기해야 한다.
3. No Preemption (비선점)
   - 다른 프로세스가 가진 자원을 강제로 뺏어올 수 없어야 한다.
4. Circular Wait (환형 대기)
   - 대기 프로세스들이 고리(Circle) 형태로 서로의 자원을 기다려야 한다.

📢 섹션 요약 비유: 데드락은 네 명이 사거리에서 각자 앞차 때문에 꼼짝 못 하는 '교통 마비' 상황과 같습니다.

---

### Ⅱ. 데드락 해결 전략 체크리스트

1. 전략별 비교 다이어그램
   - 예방, 회피, 탐지의 강도와 비용 관계를 보여준다.

```text
[ Deadlock Handling Strategies ]

 High Safety <-----------------------------------------> High Performance
      |                                                      |
 +------------+        +------------+        +------------+  |  +------------+
 | Prevention |        | Avoidance  |        | Detection  |  |  | Ignorance  |
 +------------+        +------------+        +------------+  |  +------------+
 (Condition   )        (Safe State  )        (Resource    )  |  (Ostrich    )
 (Removal     )        (Checking    )        (Graph       )  |  (Algorithm  )
```

2. Prevention (예방) 체크리스트
   - [ ] 자원을 공유 가능하게 만들 수 있는가? (Mutual Exclusion 제거)
   - [ ] 자원을 요청할 때 가진 것을 다 내려놓게 할 수 있는가? (Hold and Wait 제거)
   - [ ] 자원을 강제로 회수할 수 있는가? (No Preemption 제거)
   - [ ] 자원에 고유 번호를 매겨 순서대로만 요청하게 할 수 있는가? (Circular Wait 제거)

📢 섹션 요약 비유: 아예 사거리에 신호등을 설치하거나 일방통행으로 만들어 사고를 '예방'하는 규칙과 같습니다.

---

### Ⅲ. Deadlock Avoidance와 은행원 알고리즘(Banker's Algorithm)

1. Safe State (안전 상태)의 정의
   - 모든 프로세스가 언젠가 자원을 할당받아 정상적으로 종료될 수 있는 순서(Safe Sequence)가 존재하는 상태이다.
2. Banker's Algorithm 동작 원리
   - 프로세스가 자원을 요청할 때, 자원을 빌려준 뒤에도 시스템이 안전 상태로 유지될 수 있는지를 시뮬레이션하여 승인 여부를 결정한다.
3. 한계점
   - 자원의 최대 수요량을 미리 알아야 하며, 프로세스 수가 고정되어야 하는 등 실무 적용이 매우 까다롭다.

📢 섹션 요약 비유: 은행이 대출해줄 때, 이 돈을 빌려줘도 나중에 돈을 돌려받을 수 있는 '안전한 계획'이 있는지 미리 확인하는 것과 같습니다.

---

### Ⅳ. 탐지 및 복구(Detection & Recovery) 전략

1. Resource Allocation Graph (RAG)
   - 자원 할당 그래프를 그려 사이클(Cycle) 존재 여부를 확인한다 (단일 자원 유형인 경우 사이클이 곧 데드락).
2. 복구 방법 (Recovery)
   - **Process Termination**: 데드락에 빠진 프로세스를 하나씩 또는 전부 종료한다.
   - **Resource Preemption**: 데드락이 해제될 때까지 프로세스로부터 자원을 뺏어 다른 프로세스에 준다 (Rollback 발생).
3. 복구 시 고려 사항
   - 희생자(Victim) 선정 기준: 우선순위, 소요 시간, 남은 시간 등을 고려하여 비용이 최소화되는 프로세스를 선택한다.

📢 섹션 요약 비유: 이미 차가 막혔을 때, 경찰이 와서 몇 대의 차를 뒤로 빼게(Rollback) 하거나 돌려보내서 길을 뚫는 것과 같습니다.

---

### Ⅴ. 현대 운영체제의 데드락 대응 (Ostrich Algorithm)

1. 타조 알고리즘(Ostrich Algorithm)
   - "데드락은 거의 발생하지 않으며, 해결 비용이 너무 크다"고 판단하여 무시하는 방식이다.
2. 실무적 해결책
   - 데드락이 발생하면 사용자가 프로세스를 강제 종료(Task Manager)하거나 시스템을 재부팅하게 한다.
3. 시스템 수준의 워치독(Watchdog)
   - 커널 내부에 타이머를 두어 특정 작업이 너무 오래 멈춰 있으면 커널 패닉(Kernel Panic)을 일으키거나 복구 모드로 진입하게 한다.

📢 섹션 요약 비유: 아주 드물게 일어나는 사고를 대비해 엄청나게 비싼 보험을 드느니, 차라리 사고가 나면 그때 해결하는 게 경제적이라는 판단입니다.

---

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 프로세스 동기화(Process Synchronization)
- **자식 노드**: 은행원 알고리즘(Banker's Algorithm), 자원 할당 그래프(RAG), 교착 상태 예방/회피/탐지
- **연관 키워드**: Coffman's Condition, Safe State, Starvation, Victim Selection, Rollback

### 👶 어린아이에게 설명하기
"친구 두 명이 장난감 기차랑 기찻길을 가지고 놀고 싶어 해. 그런데 철수는 기차를 가졌고 기찻길을 기다리고, 영희는 기찻길을 가졌는데 기차를 기다리고 있으면 둘 다 아무것도 못 하겠지? 이걸 '꼼짝 마' 상태라고 해. 대장님은 이런 일이 생기지 않게 친구들에게 미리 물어보거나, 너무 오래 기다리면 잠깐 양보하게 해서 모두가 즐겁게 놀 수 있게 도와준단다!"