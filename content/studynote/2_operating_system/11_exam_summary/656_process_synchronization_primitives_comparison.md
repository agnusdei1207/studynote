+++
title = "656. 프로세스 동기화 프리미티브(Mutex, Semaphore, Spinlock) 비교표"
date = "2024-05-23"
weight = 656
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Synchronization", "Mutex", "Semaphore", "Spinlock", "Race Condition"]
+++

> **[Insight]**
> 공유 자원에 대한 동시 접근(Concurrent Access)은 경쟁 상태(Race Condition)를 유발하여 데이터의 일관성을 파괴할 수 있으므로, 적절한 동기화 프리미티브(Synchronization Primitive) 선택이 중요하다.
> 뮤텍스(Mutex), 세마포어(Semaphore), 스핀락(Spinlock)은 각기 다른 대기 방식과 자원 관리 메커니즘을 가지고 있으며, 이는 성능과 시스템 복잡도 사이의 균형을 결정한다.
> 하드웨어의 원자적 명령어(Atomic Instruction) 지원을 기반으로 소프트웨어적 추상화가 이루어지며, 데드락(Deadlock) 방지를 위한 정교한 설계가 수반되어야 한다.

+++

### Ⅰ. 임계 구역(Critical Section)과 동기화의 필요성

1. 임계 구역(Critical Section)의 정의
   - 여러 프로세스가 공유 데이터를 접근하며 실행되는 코드 영역으로, 오직 하나의 프로세스만 진입 가능해야 한다.
2. 동기화 해결의 3대 조건
   - **Mutual Exclusion (상호 배제)**: 한 번에 한 프로세스만 진입.
   - **Progress (진행)**: 진입 결정이 무한정 연기되지 않음.
   - **Bounded Waiting (한정 대기)**: 대기 시간이 무한정 길어지지 않음.

📢 섹션 요약 비유: 임계 구역은 '화장실 한 칸'과 같아서, 동시에 여러 명이 들어가면 곤란해지므로 '잠금 장치'가 필요합니다.

+++

### Ⅱ. 주요 동기화 프리미티브 비교표

1. 프리미티브별 특징 요약
   - 동작 방식과 소유권 여부에 따른 분류이다.

```text
[ Synchronization Primitives Comparison ]

 Primitive | Ownership | Wait Type    | Counter | Use Case
-----------|-----------|--------------|---------|-------------------
 Mutex     | Yes       | Sleep / Wait | Binary  | 1 process at a time
 Semaphore | No        | Sleep / Wait | Integer | Multiple resources
 Spinlock  | Yes       | Busy Wait    | Binary  | Short-term lock
 Monitor   | Yes       | Wait Queue   | -       | High-level abstraction
```

2. Mutex (Mutual Exclusion)
   - 소유권이 있으며, 락을 건 프로세스만 해제 가능(Unlocking).
3. Semaphore
   - S값(카운터)을 사용하여 허용 개수만큼 프로세스 진입 가능. (P: wait, V: signal)
4. Spinlock
   - 락을 얻을 때까지 CPU를 점유하며 반복적으로 확인(Busy Waiting). 문맥 교환 오버헤드보다 대기 시간이 짧을 때 유리하다.

📢 섹션 요약 비유: 뮤텍스는 '하나뿐인 열쇠'이고, 세마포어는 '자리가 여러 개인 주차장 입구 전광판'이며, 스핀락은 '문이 열릴 때까지 문고리를 계속 돌려보는 것'과 같습니다.

+++

### Ⅲ. 세마포어(Semaphore)의 상세 동작 (P, V 연산)

1. P(S) 연산 (Proberen, Test)
   - S가 0 이하이면 대기, 0보다 크면 S를 1 감소시키고 진입한다.
2. V(S) 연산 (Verhogen, Increment)
   - S를 1 증가시키고 대기 중인 프로세스를 깨운다(Wake-up).
3. 이진 세마포어(Binary) vs 계수 세마포어(Counting)
   - 이진은 Mutex와 유사하게 동작하며, 계수는 유한한 자원(Resource Pool) 관리에 적합하다.

📢 섹션 요약 비유: 주차장에 빈자리가 있으면 들어가고(P), 나갈 때 빈자리가 하나 늘었다고 알려주는(V) 관리원과 같습니다.

+++

### Ⅳ. 하드웨어 기반 동기화 및 소프트웨어 기법

1. Atomic Instructions
   - **Test-And-Set (TAS)**: 하드웨어적으로 중단 없이 값을 읽고 쓰는 명령어.
   - **Compare-And-Swap (CAS)**: 예상값과 같으면 새로운 값으로 교체하는 명령어.
2. 피터슨 알고리즘(Peterson's Algorithm)
   - 두 프로세스 간의 동기화를 보장하는 고전적인 소프트웨어적 해결책(현대적 아키텍처에서는 메모리 배리어 문제로 직접 사용이 어렵다).
3. 모니터(Monitor)
   - 공유 자원과 접근 함수를 하나의 객체로 캡슐화하여 사용자가 명시적으로 락을 관리할 필요가 없게 만든 고급 추상화 도구 (예: Java의 `synchronized`).

📢 섹션 요약 비유: 번호표 기계(Atomic Instruction)가 있어서 한 번에 한 명만 번호표를 뽑는 것을 보장해주는 원리와 같습니다.

+++

### Ⅴ. 동기화 관련 고전적 문제 및 해결

1. 유한 버퍼 문제 (Bounded-Buffer Problem)
   - 생산자-소비자 간의 데이터 일관성 유지.
2. 읽기-쓰기 문제 (Readers-Writers Problem)
   - 읽기 중에는 여러 명 허용, 쓰기 중에는 독점적 접근 보장.
3. 식사하는 철학자 문제 (Dining Philosophers Problem)
   - 한정된 자원(포크)으로 인한 데드락 방지 연구의 기본 모델.

📢 섹션 요약 비유: 식당에서 젓가락이 한 짝씩밖에 없을 때, 모두가 왼쪽 것만 들고 오른쪽 것을 기다리다가 굶어 죽지 않게 하는 규칙을 세우는 것과 같습니다.

+++

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: 프로세스 동기화(Process Synchronization)
- **자식 노드**: Mutex, Semaphore, Spinlock, Event, Condition Variable
- **연관 키워드**: Critical Section, Race Condition, Busy Wait, Deadlock, Atomic Operation

### 👶 어린아이에게 설명하기
"장난감 하나를 가지고 여러 친구가 놀고 싶어 하면 싸움이 나겠지? 그래서 규칙이 필요해. '선생님이 주시는 보물 열쇠(Mutex)를 가진 친구만 장난감을 만질 수 있어!'라고 정하는 거야. 친구가 놀고 나면 열쇠를 돌려주고, 다음 친구가 그 열쇠를 받아서 노는 거야. 그러면 싸우지 않고 사이좋게 놀 수 있단다!"