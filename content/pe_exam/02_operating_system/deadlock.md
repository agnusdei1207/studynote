+++
title = "교착상태 (Deadlock)"
date = 2025-03-02

[extra]
categories = "pe_exam-operating_system"
+++

# 교착상태 (Deadlock)

## 핵심 인사이트 (3줄 요약)
> **서로 상대방 자원을 기다리며 무한 대기**. 상호배제, 점유대기, 비선점, 순환대기. 예방/회피/탐지/복구.

## 1. 개념
교착상태(Deadlock)는 **둘 이상의 프로세스가 서로 상대방이 가진 자원을 기다리며 영원히 진행하지 못하는 상태**다. 네 가지 필요조건이 모두 만족될 때 발생한다.

> 비유: "일방통행 좁은 길 맞은편 차" - 서로 비켜줄 수 없어요

## 2. 교착상태 조건

```
┌────────────────────────────────────────────────────────┐
│           교착상태 4가지 필요조건                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1️⃣ 상호 배제 (Mutual Exclusion):                     │
│  ┌────────────────────────────────────────────────┐   │
│  │  • 자원은 한 번에 한 프로세스만 사용            │   │
│  │  • 자원 공유 불가                               │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  2️⃣ 점유 대기 (Hold and Wait):                       │
│  ┌────────────────────────────────────────────────┐   │
│  │  • 자원을 가진 상태에서 다른 자원 대기          │   │
│  │  • 최소 하나의 자원 보유                        │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  3️⃣ 비선점 (No Preemption):                          │
│  ┌────────────────────────────────────────────────┐   │
│  │  • 다른 프로세스의 자원을 강제로 뺏을 수 없음   │   │
│  │  • 자발적 반납만 가능                           │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  4️⃣ 순환 대기 (Circular Wait):                       │
│  ┌────────────────────────────────────────────────┐   │
│  │  • P1→P2→P3→...→Pn→P1                         │   │
│  │  • 원형 대기 형성                               │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  ⚠️ 4가지 모두 만족 시 교착상태 발생!                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 해결 방법

| 방법 | 설명 | 비용 |
|-----|------|------|
| 예방 | 조건 부정 | 자원 활용 저하 |
| 회피 | 안전 상태 유지 | 오버헤드 |
| 탐지 | 주기적 검사 | 복구 비용 |
| 복구 | 무시/종료 | 작업 손실 |

## 4. 은행원 알고리즘

| 용어 | 설명 |
|-----|------|
| Available | 가용 자원 |
| Max | 최대 필요 |
| Allocation | 할당됨 |
| Need | Max - Allocation |

## 5. 교착상태 예방 전략

| 조건 | 예방 방법 |
|-----|----------|
| 상호배제 | 공유 자원 증가 |
| 점유대기 | 전부 할당 또는 대기 |
| 비선점 | 선점 허용 |
| 순환대기 | 자원 순서 부여 |

## 6. 장단점

| 해결책 | 장점 | 단점 |
|-------|------|------|
| 예방 | 확실 | 비효율 |
| 회피 | 유연 | 복잡 |
| 탐지/복구 | 성능 | 손실 |

## 7. 코드 예시

```python
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum

class ProcessState(Enum):
    RUNNING = "실행"
    WAITING = "대기"
    TERMINATED = "종료"
    DEADLOCKED = "교착"

@dataclass
class Resource:
    """자원"""
    rid: int
    name: str
    total: int
    available: int

@dataclass
class Process:
    """프로세스"""
    pid: int
    name: str
    max_need: Dict[int, int] = field(default_factory=dict)
    allocated: Dict[int, int] = field(default_factory=dict)
    state: ProcessState = ProcessState.RUNNING

    @property
    def need(self) -> Dict[int, int]:
        return {r: self.max_need.get(r, 0) - self.allocated.get(r, 0)
                for r in self.max_need}

class DeadlockDetector:
    """교착상태 탐지기"""

    def __init__(self):
        self.processes: Dict[int, Process] = {}
        self.resources: Dict[int, Resource] = {}

    def detect_deadlock(self) -> Tuple[bool, List[int]]:
        """교착상태 탐지"""
        work = {r.rid: r.available for r in self.resources.values()}
        finish = {p.pid: all(p.allocated.get(r, 0) == 0 for r in self.resources)
                 for p in self.processes.values()}

        changed = True
        while changed:
            changed = False
            for pid, process in self.processes.items():
                if finish[pid]:
                    continue

                # Need <= Work 확인
                can_proceed = all(process.need.get(r, 0) <= work.get(r, 0)
                                 for r in self.resources)

                if can_proceed:
                    for r in self.resources:
                        work[r] = work.get(r, 0) + process.allocated.get(r, 0)
                    finish[pid] = True
                    changed = True

        deadlocked = [pid for pid, f in finish.items() if not f]

        if deadlocked:
            print(f"⚠️ 교착상태 탐지: 프로세스 {deadlocked}")
            for pid in deadlocked:
                self.processes[pid].state = ProcessState.DEADLOCKED
        else:
            print("✅ 교착상태 없음")

        return len(deadlocked) > 0, deadlocked

class BankersAlgorithm:
    """은행원 알고리즘"""

    def __init__(self, total_resources: Dict[int, int]):
        self.total = total_resources
        self.available = total_resources.copy()
        self.processes: Dict[int, Process] = {}

    def add_process(self, process: Process):
        """프로세스 추가"""
        self.processes[process.pid] = process

    def request_resources(self, pid: int, request: Dict[int, int]) -> bool:
        """자원 요청"""
        process = self.processes[pid]

        # 요청 <= Need 확인
        for r, amount in request.items():
            if amount > process.need.get(r, 0):
                print(f"❌ 요청이 최대 필요 초과")
                return False

        # 요청 <= Available 확인
        for r, amount in request.items():
            if amount > self.available.get(r, 0):
                print(f"❌ 자원 부족")
                return False

        # 임시 할당
        for r, amount in request.items():
            self.available[r] -= amount
            process.allocated[r] = process.allocated.get(r, 0) + amount

        # 안전성 검사
        if self._is_safe():
            print(f"✅ 안전: 자원 할당 승인")
            return True
        else:
            # 롤백
            for r, amount in request.items():
                self.available[r] += amount
                process.allocated[r] -= amount
            print(f"❌ 불안전: 자원 할당 거부")
            return False

    def _is_safe(self) -> bool:
        """안전 상태 확인"""
        work = self.available.copy()
        finish = {pid: False for pid in self.processes}

        while True:
            found = False
            for pid, process in self.processes.items():
                if finish[pid]:
                    continue

                if all(process.need.get(r, 0) <= work.get(r, 0)
                       for r in self.total):
                    for r in self.total:
                        work[r] = work.get(r, 0) + process.allocated.get(r, 0)
                    finish[pid] = True
                    found = True

            if not found:
                break

        return all(finish.values())

class DeadlockPrevention:
    """교착상태 예방"""

    def __init__(self, resource_order: List[int]):
        self.resource_order = resource_order  # 자원 순서

    def can_request(self, current_resources: Set[int], new_resource: int) -> bool:
        """순환 대기 예방 - 자원 순서 확인"""
        new_idx = self.resource_order.index(new_resource)

        for r in current_resources:
            r_idx = self.resource_order.index(r)
            if new_idx <= r_idx:
                print(f"❌ 자원 순서 위반: {r} 후 {new_resource} 요청 불가")
                return False

        print(f"✅ 자원 순서 준수")
        return True

class DeadlockRecovery:
    """교착상태 복구"""

    def __init__(self):
        self.processes: Dict[int, Process] = {}

    def recover_terminate(self, deadlocked: List[int]) -> int:
        """프로세스 종료로 복구"""
        print(f"🔧 복구: 교착 프로세스 종료")
        for pid in deadlocked:
            self.processes[pid].state = ProcessState.TERMINATED
            print(f"  종료: 프로세스 {pid}")
        return len(deadlocked)

    def recover_preempt(self, victim_pid: int) -> bool:
        """선점으로 복구"""
        print(f"🔧 복구: 프로세스 {victim_pid} 자원 선점")
        victim = self.processes.get(victim_pid)
        if victim:
            victim.allocated.clear()
            victim.state = ProcessState.WAITING
            return True
        return False

# 사용 예시
print("=== 교착상태 시뮬레이션 ===\n")

# 교착상태 탐지
print("--- 교착상태 탐지 ---\n")
detector = DeadlockDetector()

# 자원 생성
detector.resources[0] = Resource(0, "R1", 1, 0)
detector.resources[1] = Resource(1, "R2", 1, 0)

# 프로세스 생성
p1 = Process(1, "P1", max_need={0: 1, 1: 1}, allocated={0: 1})
p2 = Process(2, "P2", max_need={0: 1, 1: 1}, allocated={1: 1})
detector.processes[1] = p1
detector.processes[2] = p2

# 교착상태 탐지
has_deadlock, deadlocked = detector.detect_deadlock()

# 은행원 알고리즘
print("\n--- 은행원 알고리즘 ---\n")
banker = BankersAlgorithm({0: 10, 1: 5})

p1 = Process(1, "P1", max_need={0: 7, 1: 5})
p2 = Process(2, "P2", max_need={0: 3, 1: 2})
banker.add_process(p1)
banker.add_process(p2)

banker.request_resources(1, {0: 3, 1: 2})
banker.request_resources(2, {0: 2})

# 교착상태 예방
print("\n--- 교착상태 예방 ---\n")
prevention = DeadlockPrevention([0, 1, 2])  # R0 < R1 < R2
prevention.can_request(set([1]), 0)  # R1 보유 후 R0 요청 - 실패
prevention.can_request(set([0]), 1)  # R0 보유 후 R1 요청 - 성공

---


## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"교착상태(Deadlock)의 발생 조건 4가지를 설명하고, 예방·회피·탐지·회복 기법을 비교하여 실무 적용 방안을 논하시오."**

---

### Ⅰ. 개요

**교착상태(Deadlock)**란 두 개 이상의 프로세스가 서로 상대방이 점유한 자원을 기다리며 무한 대기 상태에 빠지는 현상이다.

- **등장 배경**: 멀티태스킹 환경에서 다수의 프로세스가 한정된 자원을 경쟁적으로 요구하면서 순환 대기(Circular Wait) 구조가 형성
- **핵심 피해**: CPU, 메모리 등 자원이 무기한 잠금되어 시스템 전체가 마비

---

### Ⅱ. 교착상태 발생 4대 필요 조건 (Coffman 조건)

| 조건 | 설명 | 예시 |
|-----|-----|-----|
| **상호 배제** (Mutual Exclusion) | 자원을 한 번에 한 프로세스만 사용 | 프린터, mutex |
| **점유 대기** (Hold and Wait) | 자원을 가진 채로 다른 자원을 요청 | A가 R1 잡고 R2 요청 |
| **비선점** (No Preemption) | 강제로 자원을 빼앗을 수 없음 | 자원은 자발적 해제만 가능 |
| **순환 대기** (Circular Wait) | A→B→C→A 형태의 순환 자원 요청 | 자원 할당 그래프에 사이클 존재 |

> **4가지 조건이 동시에 성립할 때만 교착상태 발생** → 하나만 제거해도 교착상태 방지 가능

---

### Ⅲ. 교착상태 대응 기법 비교

| 기법 | 방법 | 장점 | 단점 | 적용 |
|-----|-----|-----|-----|-----|
| **예방** (Prevention) | Coffman 조건 4개 중 하나 원천 제거 | 교착상태 원천 차단 | 자원 낭비, 성능 저하 | 안전 임계 시스템 |
| **회피** (Avoidance) | 은행가 알고리즘으로 안전 상태만 허용 | 자원 효율 유지 | 자원 최대 요구량 사전 신고 필요 | 실시간 시스템 |
| **탐지** (Detection) | 자원 할당 그래프의 사이클 주기적 탐지 | 자원 최대 활용 | 탐지 후 회복 비용 발생 | 일반 OS |
| **회복** (Recovery) | 프로세스 강제 종료 or 자원 선점 | 탐지 후 구제 가능 | 데이터 손실, 기아 발생 가능 | OS 커널 |

#### 은행가 알고리즘 핵심 (회피의 대표 기법)

```
안전 상태(Safe State): 모든 프로세스가 교착상태 없이 완료 가능한 실행 순서 존재
불안전 상태: 안전한 실행 순서가 존재하지 않는 상태

판단: Allocation + Need ≤ Available 일 때만 자원 할당 허용
```

---

### Ⅳ. 실무 적용 방안

| 적용 분야 | 방법 | 기대 효과 |
|---------|-----|---------|
| **데이터베이스** | Wait-Die/Wound-Wait 방식으로 Lock 순서 강제화 | 교착상태 없는 트랜잭션 처리 |
| **OS 커널** | 자원 할당 그래프 주기적 탐지 + 우선순위 낮은 프로세스 종료 | 시스템 마비 방지 |
| **분산 시스템** | 타임아웃 기반 Lock 해제, Retry with Backoff | 네트워크 분할 상황에서도 안전 |
| **자바/C++ 개발** | Lock 획득 순서를 전역적으로 일관되게 정의 (Lock Ordering) | Circular Wait 구조 원천 차단 |

---

### Ⅴ. 기대 효과 및 결론

| 효과 영역 | 내용 | 정량 목표 |
|---------|-----|---------|
| **시스템 안정성** | 교착 상태로 인한 서비스 다운 방지 | UpTime 99.99% 이상 |
| **자원 효율** | 회피/탐지 방식으로 자원 낭비 최소화 | 자원 사용률 20% 향상 |
| **개발 생산성** | Lock Ordering 규칙으로 버그 사전 방지 | 동시성 버그 70% 감소 |

#### 결론
> 교착상태 대응 전략 선택은 "안정성 vs 성능" 트레이드오프를 고려해야 한다. 안전성이 최우선인 시스템(원전, 항공)은 예방, 일반 서버는 탐지+회복, 데이터베이스는 회피 전략이 적합하다. 향후 마이크로서비스 아키텍처에서는 분산 락(Distributed Lock)과 Saga 패턴을 결합하여 분산 교착상태를 방지하는 설계가 핵심이 될 것이다.

> **※ 참고**: Dijkstra Banker's Algorithm (1965), POSIX Thread 표준 (IEEE 1003.1)

---

## 어린이를 위한 종합 설명

**교착상태를 쉽게 이해해보자!**

> 서로 상대방 자원을 기다리며 무한 대기. 상호배제, 점유대기, 비선점, 순환대기. 예방/회피/탐지/복구.

```
왜 필요할까?
  핵심 피해: CPU, 메모리 등 자원이 무기한 잠금되어 시스템 전체가 마비

어떻게 동작하나?
  복잡한 문제 → 교착상태 적용 → 더 빠르고 안전한 결과!

핵심 한 줄:
  교착상태 = 똑똑하게 문제를 해결하는 방법
```

> **비유**: 교착상태은 마치 요리사가 레시피를 따르는 것과 같아.
> 혼란스러운 재료들을 정해진 순서대로 조합하면 → 맛있는 요리(최적 결과)가 나오지! 🍳

---
