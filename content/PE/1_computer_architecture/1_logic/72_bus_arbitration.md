+++
title = "버스 Arbitration (Bus Arbitration)"
date = 2026-03-05
categories = ["컴퓨터구조", "논리회로", "입출력"]
draft = false
+++

# 버스 중재 (Bus Arbitration)

## 핵심 인사이트 (3줄 요약)
1. 버스 중재(Arbitration)는 다중 버스 마스터가 동시에 버스를 요청할 때 우선순위를 결정하고 버스 사용권을 할당하는 메커니즘이다
2. Centralized(중앙)과 Distributed(분산) 방식이 있으며, Daisy Chain, Fixed Priority, Round Robin, Fairness 알고리즘이 사용된다
3. 기술사시험에서는 중재 방식, 우선순위 결정, Request/Grant 프로토콜, Deadlock 해결이 핵심이다

## Ⅰ. 개요 (500자 이상)

버스 중재(Bus Arbitration)는 **여러 버스 마스터(Bus Master)가 동시에 버스 사용을 요청할 때, 충돌을 방지하고 적절한 순서로 버스 사용권을 부여하는 제어 메커니즘**이다. DMA, 다중 CPU, 고속 I/O 장치 등이 동시에 버스를 사용하려 할 때 필요하다.

```
버스 중재 기본 개념:
목적: 버스 충돌 방지, 순차적 사용권 부여
요소: Arbiter (중재자), Master (요청자), Bus (공유 자원)
동작: Request → Arbitration → Grant → Bus Use → Release

특징:
- 공유 자원 관리
- 우선순위 결정
- 공평성 보장
- Deadlock 방지

알고리즘:
- Fixed Priority: 고정 우선순위
- Round Robin: 순차 회전
- Fair Queuing: 공평 큐
- Dynamic: 동적 우선순위
```

**버스 중재의 핵심 특징:**

1. **충돌 해결**: 동시 요청 시 하나만 승인
2. **우선순위**: 중요도에 따른 순서 결정
3. **공평성**: 모든 Master가 기회를 얻도록
4. **효율성**: 버스 활용도 최대화

```
중재 필요성:
- DMA Controller: 버스 요청
- CPU: 버스 요청
- 다른 Master: 버스 요청
→ 동시 요청 시 충돌
→ Arbiter가 중재
```

## Ⅱ. 아키텍처 및 핵심 원리 (1000자 이상)

### Centralized Arbitration

```
중앙 집중식 중재:

구조:
Master 0 ─┬─[BREQ]───┐
Master 1 ─┤          │
Master 2 ─┤   [Arbiter]── Bus
Master 3 ─┤          │
         └──[BGTN]───┘

요청:
각 Master가 BREQ 활성

중재:
Arbiter가 모든 BREQ 수신
우선순위 계산
하나의 Master 선택

승인:
해당 Master에 BGTN 활성
다른 Master는 대기

장점:
- 단순한 구조
- 명확한 우선순위
- 쉬운 구현

단점:
- Arbiter 병목
- 단일 장애점
- 확장 제한
```

### Distributed Arbitration

```

분산식 중재:

구조:
Master 0 ─[BREQ]──┬── Bus
Master 1 ─[BREQ]──┤
Master 2 ─[BREQ]──┤
Master 3 ─[BREQ]──┘
        │
    [Daisy Chain]
        │
   [Bus Grant]

동작:
1. Master가 BREQ 활성
2. Daisy Chain으로 전파
3. 먼저 받은 Master가 승인
4. 나머지는 대기

장점:
- 병목 없음
- 장애 허용
- 확장 용이

단점:
- 우선순위 고정
- Daisy Chain 지연
- 복잡한 제어
```

### Daisy Chain

```
Daisy Chain Arbitration:

구조:
BREQ[0] ──┬──[Priority 0]── BG[0] ──┐
BREQ[1] ──┼──[Priority 1]── BG[1] ──┤
BREQ[2] ──┼──[Priority 2]── BG[2] ──┤
BREQ[3] ──┘              BG[3] ──┘

BGIN ───→ [M0] → [M1] → [M2] → [M3] → BGOUT

동작:
1. BGIN 신호 입력
2. M0가 버스 필요?
   - Yes: BGIN 소비, Bus 사용
   - No: BGIN을 M1로 전달
3. 순차적으로 확인

특징:
- 가장 가까운 Master가 우선
- 하드웨어 간단
- 지연 누적
- Master 0가 항상 우선
```

### Fixed Priority

```
고정 우선순위:

구현:
Priority Encoder
Input: BREQ[3:0]
Output: Grant[3:0]

논리:
if BREQ[0]: Grant = 0001
elif BREQ[1]: Grant = 0010
elif BREQ[2]: Grant = 0100
elif BREQ[3]: Grant = 1000

특징:
- Master 0 > Master 1 > Master 2 > Master 3
- 단순하고 빠름
- 기아(Starvation) 가능

Starvation 예:
Master 3이 계속 요청
Master 0도 계속 요청
→ Master 3는 영원히 대기

해결:
Priority Aging
- 대기 시간 증가 시 우선순위 상향
```

### Round Robin

```
Round Robin Arbitration:

구조:
Queue: [M0, M1, M2, M3]
   ↓
Front 서비스 후 Rear로 이동

동작:
1. 현재 서비스 중인 Master
2. 완료 후 Queue 회전
3. 다음 Master 서비스

예:
Cycle 1: M0 → M1 → M2 → M3
Cycle 2: M1 → M2 → M3 → M0
Cycle 3: M2 → M3 → M0 → M1

특징:
- 공평한 기회
- Starvation 없음
- 대기 시간 예측 가능
- 하드웨어 복잡

구현:
Circular Pointer
Next = (Current + 1) % N
```

### Fair Arbitration

```
공평 중재:

Fairness Algorithm:
1. Fair Queuing:
   - 모든 Master 동등
   - FCFS (First Come First Serve)

2. Weighted Fair Queuing:
   - Master별 가중치
   - W0:W1 = 2:1
   - M0는 2회, M1은 1회

3. Least Laxity First:
   - 남은 시간이 적은 Master 우선

4. Aging:
   - 대기 시간에 따른 우선순위 증가

구현:
Counter per Master
Waiting[i]++
Priority[i] = Base[i] + Aging[Waiting[i]]
```

## Ⅲ. 융합 비교

### 중재 방식

| 방식 | 구조 | 복잡도 | 지연 | 확장성 | 응용 |
|------|------|--------|------|--------|------|
| Centralized | 중앙 Arbiter | 낮음 | 짧음 | 제한 | PCI |
| Distributed | Daisy Chain | 중간 | 김 | 좋음 | VME |
| Split Transaction | 복잡 | 높음 | 김 | 좋음 | PCI-X |

### 우선순위 알고리즘

| 알고리즘 | 공평성 | Starvation | 응답 시간 | 구현 |
|----------|--------|-----------|----------|------|
| Fixed | 낮음 | 있음 | 일정 | 단순 |
| Round Robin | 높음 | 없음 | 균등 | 중간 |
| Fair Queue | 매우 높음 | 없음 | 가변 | 복잡 |
| Aging | 중간 | 없음 | 가변 | 중간 |

### Request/Grant 프로토콜

| 프로토콜 | 신호 수 | 타이밍 | 복잡도 | 응용 |
|----------|--------|--------|--------|------|
| 2-Wire (R/G) | 2 | 단순 | 낮음 | Simple |
| 3-Wire (R/G/B) | 3 | 중간 | 중간 | 표준 |
| Split | 복잡 | 복잡 | 높음 | 고성능 |

## Ⅳ. 실무 적용 및 기술사적 판단

### PCI Arbitration

```
PCI Bus Arbitration:

구조:
PCI Arbiter (Chipset 내부)
REQ#[7:0]: Master 요청
GNT#[7:0]: Master 승인

동작:
1. Master가 REQ# 활성
2. Arbiter가 우선순위 결정
3. GNT# 활성으로 승인
4. Master가 FRAME# 활성으로 시작
5. 완료 후 REQ# 비활성
6. GNT# 해제

특징:
- Fairness 보장
- Hidden Arbitration
- 완료 중에 다음 중재
```

### VME Bus Arbitration

```
VME Bus Arbitration:

구조:
Daisy Chain + Centralized

신호:
BR*: Bus Request
BG*: Bus Grant
BCLR*: Bus Clear
BBSY*: Bus Busy

동작:
1. Master가 BR* 활성
2. Daisy Chain으로 BG* 전파
3. 활성 Master가 BBSY* 활성
4. 버스 사용
5. 완료 후 BBSY* 비활성

4가지 Level:
- Priority 1-3
- Daisy Chain per Level
```

### Multicore Arbitration

```

멀티코어 시스템 중재:

구조:
Core 0 ─┬
Core 1 ─┼─[L2 Cache]─┬─[L3 Cache]─┬─[MC]
Core 2 ─┤             │            │
Core 3 ─┘             │            │

중재 레벨:
1. L1 → L2: 내부 Arbitration
2. L2 → L3: Coherent Arbitration
3. L3 → MC: Memory Arbitration

Coherency:
- MESI Protocol
- Snooping
- Directory Based

우선순위:
- Real-time > Normal > Background
```

### Deadlock Prevention

```
Deadlock 해결:

상황:
Master A가 버스 대기
Master B가 버스 대기
둘 다 서로의 자원을 기다림

해결:

1. Timeout:
   - 일정 시간 후 재시도
   - 강제 해제

2. Priority Aging:
   - 대기 시간 증가
   - 우선순위 상향

3. Preemption:
   - 낮은 우선순위 강제 해제
   - 높은 우선순위에 양보

구현:
Timer + Counter
if Wait > Threshold:
  Priority++
```

## Ⅴ. 기대효과 및 결론

버스 중재는 공유 자원 관리의 핵심이다. 충돌을 방지하고 효율적인 버스 사용을 보장한다.

## 📌 관련 개념 맵

```
버스 중재
├── 방식
│   ├── Centralized (중앙)
│   │   ├── Daisy Chain
│   │   ├── Fixed Priority
│   │   └── Round Robin
│   └── Distributed (분산)
│       └── Self Arbitration
├── 알고리즘
│   ├── Fixed Priority
│   ├── Round Robin
│   ├── Fair Queuing
│   └── Aging
├── 프로토콜
│   ├── Request/Grant
│   ├── Bus Busy
│   └── Split Transaction
└── 문제 해결
    ├── Starvation 방지
    ├── Deadlock 해결
    └── Fairness 보장
```

## 👶 어린이를 위한 3줄 비유 설명

1. 버스 중재는 도로의 교통 경찰 같아요. 여러 차가 동시에 가려고 하면 누구를 먼저 보낼지 정해요
2. Daisy Chain은 줄 서기 같아요. 앞에 있는 사람이 먼저 들어가고, 뒤에 있는 사람은 기다려야 해요
3. Round Robin은 순번제 같아요. 한 사람씩 돌아가면서 기회를 줘서 모두가 공평하게 쓸 수 있어요

```python
# 버스 중재 시뮬레이션

from typing import List, Optional
from enum import Enum


class ArbitrationType(Enum):
    CENTRALIZED = "Centralized"
    DISTRIBUTED = "Distributed"


class BusMaster:
    """버스 마스터"""

    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
        self.request = False
        self.grant = False
        self.bus_uses = 0
        self.wait_time = 0

    def request_bus(self):
        """버스 요청"""
        self.request = True
        print(f"[{self.name}] Bus Request")

    def release_bus(self):
        """버스 반환"""
        self.request = False
        self.grant = False
        print(f"[{self.name}] Bus Release")


class CentralizedArbiter:
    """중앙 집중식 중재자"""

    def __init__(self, algorithm: str = "fixed"):
        self.algorithm = algorithm
        self.masters: List[BusMaster] = []
        self.current_master = None
        self.round_robin_index = 0

    def add_master(self, master: BusMaster):
        """마스터 추가"""
        self.masters.append(master)

    def arbitrate(self) -> Optional[BusMaster]:
        """중재 수행"""
        requesters = [m for m in self.masters if m.request]

        if not requesters:
            return None

        if self.algorithm == "fixed":
            # 고정 우선순위
            winner = min(requesters, key=lambda m: m.priority)

        elif self.algorithm == "round_robin":
            # Round Robin
            candidates = requesters
            # 현재 인덱스부터 검색
            for i in range(len(self.masters)):
                idx = (self.round_robin_index + i) % len(self.masters)
                master = self.masters[idx]
                if master in candidates:
                    winner = master
                    self.round_robin_index = (idx + 1) % len(self.masters)
                    break

        elif self.algorithm == "fair":
            # 가장 오래 기다린 Master
            winner = max(requesters, key=lambda m: m.wait_time)

        else:
            winner = requesters[0]

        # 승인
        for master in self.masters:
            master.grant = (master == winner)

        # 대기 시간 증가
        for master in self.masters:
            if master.request and master != winner:
                master.wait_time += 1

        self.current_master = winner
        return winner


class DistributedArbiter:
    """분산식 중재 (Daisy Chain)"""

    def __init__(self, masters: List[BusMaster]):
        self.masters = sorted(masters, key=lambda m: m.priority)
        self.bus_grant = False

    def arbitrate(self) -> Optional[BusMaster]:
        """Daisy Chain 중재"""
        if not self.bus_grant:
            for master in self.masters:
                if master.request:
                    # Grant to first requesting master
                    for m in self.masters:
                        m.grant = False
                    master.grant = True
                    self.bus_grant = True
                    return master
        return None

    def release(self, master: BusMaster):
        """버스 반환"""
        if master.grant:
            master.grant = False
            self.bus_grant = False


def demonstration():
    """버스 중재 데모"""
    print("=" * 60)
    print("버스 중재 (Bus Arbitration) 데모")
    print("=" * 60)

    # 마스터 생성
    masters = [
        BusMaster("CPU", priority=0),
        BusMaster("DMA0", priority=1),
        BusMaster("DMA1", priority=2),
        BusMaster("Network", priority=3),
    ]

    # Fixed Priority 중재
    print("\n[Fixed Priority Arbitration]")
    arbiter_fixed = CentralizedArbiter(algorithm="fixed")
    for master in masters:
        arbiter_fixed.add_master(master)

    # 동시 요청
    print("\n동시 요청 (모든 Master):")
    for master in masters:
        master.request_bus()

    winner = arbiter_fixed.arbitrate()
    if winner:
        print(f"→ Winner: {winner.name} (Priority {winner.priority})")
        winner.bus_uses += 1
        winner.wait_time = 0
        winner.release_bus()

    # Round Robin 중재
    print("\n[Round Robin Arbitration]")
    arbiter_rr = CentralizedArbiter(algorithm="round_robin")
    for master in masters:
        arbiter_rr.add_master(master)

    print("\n3 Cycle Round Robin:")
    for cycle in range(3):
        print(f"\nCycle {cycle + 1}:")

        # 일부 Master만 요청
        if cycle == 0:
            masters[1].request_bus()
            masters[3].request_bus()
        elif cycle == 1:
            masters[0].request_bus()
            masters[1].request_bus()
        else:
            masters[2].request_bus()
            masters[3].request_bus()

        winner = arbiter_rr.arbitrate()
        if winner:
            print(f"  → {winner.name} wins")
            winner.release_bus()

        for m in masters:
            m.request = False
            m.grant = False

    # Fair Arbitration
    print("\n[Fair Arbitration (Longest Wait First)]")
    arbiter_fair = CentralizedArbiter(algorithm="fair")
    for master in masters:
        arbiter_fair.add_master(master)

    # 대기 시간 설정
    masters[1].wait_time = 5
    masters[2].wait_time = 10
    masters[3].wait_time = 1

    print("\nWait Times:")
    for m in masters:
        print(f"  {m.name}: {m.wait_time} cycles")

    for m in masters[1:]:  # CPU 제외
        m.request_bus()

    winner = arbiter_fair.arbitrate()
    if winner:
        print(f"→ Winner: {winner.name} (Waited {winner.wait_time} cycles)")

    # Daisy Chain
    print("\n[Daisy Chain Arbitration]")
    arbiter_daisy = DistributedArbiter(masters)

    masters[0].request_bus()
    masters[2].request_bus()

    winner = arbiter_daisy.arbitrate()
    if winner:
        print(f"→ {winner.name} wins (first in chain)")
        print(f"  {masters[2].name} must wait")

    # Starvation 예시
    print("\n[Starvation Problem]")
    arbiter_starve = CentralizedArbiter(algorithm="fixed")
    for master in masters:
        arbiter_starve.add_master(master)

    print("\nContinuous requests:")
    for i in range(10):
        masters[0].request_bus()  # CPU (highest priority)
        masters[3].request_bus()  # Network (lowest priority)

        winner = arbiter_starve.arbitrate()
        print(f"  Cycle {i+1}: {winner.name}")

        winner.release_bus()
        if winner == masters[0]:
            masters[3].wait_time += 1

    print(f"\nNetwork waited {masters[3].wait_time} cycles")

    # Aging으로 Starvation 해결
    print("\n[Aging Solution]")
    print("Wait time increases priority")
    print("After 5 cycles, Network priority would increase")
    print("→ Prevents starvation")

    # 통계
    print("\n[Statistics]")
    print("Algorithm Comparison:")
    algorithms = ["fixed", "round_robin", "fair"]

    for algo in algorithms:
        arbiter = CentralizedArbiter(algorithm=algo)
        for master in masters:
            arbiter.add_master(master)

        # 10 cycle simulation
        uses = {m.name: 0 for m in masters}
        for i in range(10):
            for m in masters:
                m.request = (i % 2 == 0)  # Alternating
            winner = arbiter.arbitrate()
            if winner:
                uses[winner.name] += 1
                winner.release_bus()

        print(f"\n{algo.capitalize()}:")
        for name, count in uses.items():
            print(f"  {name}: {count} uses")


if __name__ == "__main__":
    demonstration()
```
