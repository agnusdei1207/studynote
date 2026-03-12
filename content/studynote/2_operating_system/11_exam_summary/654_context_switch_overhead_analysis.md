+++
weight = 654
title = "654. 문맥 교환(Context Switch) 오버헤드 발생 지점 분석"
date = "2024-05-23"
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Context Switching", "Overhead", "PCB", "Cache Cold", "TLB Flush"]
+++

> **[Insight]**
> 문맥 교환(Context Switch)은 다중 프로그래밍(Multiprogramming) 환경을 가능케 하는 필수적인 메커니즘이지만, 시스템 입장에서는 순수한 관리 비용(Overhead)으로 작용한다.
> 오버헤드는 단순히 CPU 레지스터를 저장하고 복원하는 하드웨어적 시간을 넘어, 캐시(Cache)와 TLB(Translation Lookaside Buffer)의 무효화로 인한 성능 저하까지 포함한다.
> 따라서 효율적인 운영체제 설계는 문맥 교환의 빈도를 최적화하고, 하드웨어 특성을 고려하여 전환 비용을 최소화하는 전략에 집중한다.

---

### Ⅰ. 문맥 교환(Context Switch)의 정의와 필요성

1. 핵심 정의
   - CPU가 현재 실행 중인 프로세스(또는 스레드)의 상태를 저장하고, 다음에 실행할 프로세스의 상태를 불러와 실행권을 넘기는 과정이다.
2. 발생 시점
   - **Preemption**: 할당된 타임 슬라이스(Time Slice)가 만료되었을 때.
   - **I/O Block**: 프로세스가 입출력을 요청하여 대기 상태로 전환될 때.
   - **Interrupt**: 하드웨어 인터럽트 처리가 필요할 때.

📢 섹션 요약 비유: 문맥 교환은 공부하던 책(Process A)을 덮고 다른 책(Process B)을 펴서 다시 읽기 시작하는 '준비 과정'과 같습니다.

---

### Ⅱ. 오버헤드 발생 지점 상세 분석

1. 상태 저장 및 복원 (Direct Overhead)
   - PCB(Process Control Block)에 레지스터, PC, 스택 포인터 등을 저장하고 읽어오는 순수 작업 시간이다.

```text
[ Context Switch Overhead Components ]

   High Overhead <-------------------------------------> Low Overhead
        |                                                   |
   +----------+       +-----------+       +----------+      +-----------+
   | TLB/Cache|       | Scheduler |       | State    |      | Mode      |
   | Flush    |       | Algorithm |       | Save/Load|      | Switch    |
   +----------+       +-----------+       +----------+      +-----------+
    (Indirect)         (Computing)          (Direct)          (Minimal)
```

2. 스케줄링 알고리즘 수행
   - Ready Queue에서 다음 실행할 프로세스를 선택하기 위한 연산 오버헤드이다.
3. 캐시 및 TLB 오버헤드 (Indirect Overhead)
   - **Cache Pollution**: 새로운 프로세스가 실행되면서 이전 프로세스의 캐시 데이터가 밀려나고 캐시 미스(Cache Miss)가 급증한다.
   - **TLB Flush**: 프로세스 전환 시 주소 공간이 달라지므로 가상 주소 변환 정보를 담은 TLB를 비워야 하며, 이는 메모리 접근 속도 저하로 이어진다.

📢 섹션 요약 비유: 책을 바꿀 때 책상을 치우고(Cache Flush) 필요한 필기도구를 다시 꺼내는(State Load) 시간이 실제 공부 시간보다 길어질 수 있는 것과 같습니다.

---

### Ⅲ. 프로세스 vs 스레드 문맥 교환의 차이

1. 프로세스 문맥 교환 (Heavyweight)
   - 서로 다른 가상 주소 공간을 가지므로 페이지 테이블(Page Table) 교체가 필요하며, TLB를 반드시 플러시해야 하므로 오버헤드가 크다.
2. 스레드 문맥 교환 (Lightweight)
   - 같은 프로세스 내의 스레드들은 주소 공간을 공유하므로 페이지 테이블 교체가 불필요하고 TLB를 유지할 수 있어 상대적으로 빠르다.
3. 공유 자원 관리
   - 스레드 간 전환은 캐시 데이터의 일부를 재사용할 가능성이 높아 캐시 효율성이 프로세스 전환보다 우수하다.

📢 섹션 요약 비유: 다른 과목으로 공부를 바꾸는 것(Process Switch)보다 같은 과목의 다른 단원을 공부하는 것(Thread Switch)이 훨씬 덜 번거로운 것과 같습니다.

---

### Ⅳ. 하드웨어적 최적화 기술

1. ASID (Address Space Identifier)
   - TLB 엔트리에 프로세스 ID를 태깅하여, 문맥 교환 시 TLB를 전체 플러시하지 않고도 주소 공간을 구분하게 함으로써 성능을 비약적으로 향상한다.
2. 하드웨어 스레딩 (Simultaneous Multi-Threading, SMT)
   - CPU 내부에 여러 세트의 레지스터를 두어 하드웨어적으로 빠르게 문맥을 전환한다. (예: Intel Hyper-Threading)
3. 레지스터 윈도우(Register Window)
   - SPARC 아키텍처 등에서 사용하며, 레지스터 집합을 겹치게 배치하여 저장/복원 오버헤드를 줄인다.

📢 섹션 요약 비유: 책상 서랍 여러 개에 각 과목의 필기도구를 미리 넣어두고 서랍만 바꿔 열면(Register Set) 되는 아주 편리한 책상과 같습니다.

---

### Ⅴ. 시스템 설계 시 고려사항

1. 타임 슬라이스(Time Slice / Quantum) 결정
   - 너무 길면 응답성(Responsiveness)이 떨어지고, 너무 짧으면 문맥 교환 오버헤드가 전체 성능을 갉아먹는다. (Trade-off)
2. Affinity 스케줄링
   - 캐시 데이터를 최대한 활용하기 위해 이전에 실행되었던 동일한 CPU 코어에 프로세스를 다시 할당하는 전략이다.
3. 커널 스레드 최적화
   - 불필요한 사용자/커널 모드 전환과 문맥 교환을 줄이기 위해 LWP(Lightweight Process) 모델 등을 활용한다.

📢 섹션 요약 비유: 책을 1분마다 바꾸면(Short Quantum) 책 바꾸느라 시간을 다 쓰고, 10시간 동안 한 권만 읽으면(Long Quantum) 다른 일을 전혀 못 하는 것과 같아서 '적당한 시간'이 중요합니다.

---

### 💡 지식 그래프(Knowledge Graph)
- **부모 노드**: CPU 스케줄링(CPU Scheduling)
- **자식 노드**: PCB(Process Control Block), TLB(Translation Lookaside Buffer), Cache Locality
- **연관 키워드**: Overhead, Time Slice, Preemption, ASID, SMT

### 👶 어린아이에게 설명하기
"친구가 여러 명 있을 때, 한 친구하고만 놀면 다른 친구들이 서운하겠지? 그래서 '10분씩 번갈아 가면서 놀기'로 규칙을 정했단다. 그런데 장난감을 다 치우고 다른 친구가 놀 장난감을 꺼내는 시간이 너무 오래 걸리면 실제 노는 시간이 줄어들 거야. 그래서 대장님은 장난감을 빨리 치우고 꺼내는 방법을 고민해서 친구들이 모두 즐겁게 놀 수 있게 도와준단다!"