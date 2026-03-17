+++
title = "216. 2단계 락킹 프로토콜 (2PL, Two-Phase Locking)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 216
+++

# 216. 2단계 락킹 프로토콜 (2PL, Two-Phase Locking)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션의 락(Lock) 획득과 해제 시점을 시간축 상에서 철저히 분리하여, **비직렬화(Non-serial)된 실행 순서에서도 데이터의 정합성과 직렬 가능성(Serializability)을 수학적으로 보장**하는 동시성 제어의 핵심 프로토콜이다.
> 2. **가치**: 데이터베이스 시스템에서 충돌 직렬 가능성(Conflict Serializability)을 보장하는 가장 강력하고 대중적인 알고리즘이며, 원자성(Atomicity)을 보장하는 기반이 되지만, **교착 상태(Deadlock) 발생 가능성**이라는 내재된 트레이드오프를 관리해야 한다.
> 3. **융합**: OS의 세마포어(Semaphore)와 분산 시스템의 분산 락(Distributed Lock) 기반을 형성하며, 격리 수준(Isolation Level) 조정을 통해 현대의 DBMS(MySQL, Oracle 등)에서 ANSI 표준을 준수하는 핵심 엔진 로직으로 작동한다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
**2단계 락킹 (2PL, Two-Phase Locking)**은 트랜잭션 처리(Transaction Processing)에서 데이터 일관성을 보장하기 위해, 트랜잭션의 수명 주기 동안 '락 획득(Lock Acquisition)'과 '락 해제(Lock Release)'라는 두 가지 상호 배타적인 단계를 강제하는 프로토콜이다.
이 프로토콜의 철학은 "트랜잭션이 데이터를 읽거나 쓰기 위해서는 먼저 독점적인 권한을 설정해야 하며, 한번 권한 해제를 시작하면 새로운 권한 요청을 할 수 없다"는 엄격한 규율에 있다. 이는 비즈니스 로직의 복잡한 연산 순서와 무관하게, 데이터베이스 엔진 레벨에서 실행 순서의 충돌을 방지한다.

**2. 등장 배경 및 필요성**
다중 사용자 환경(Multi-user Environment)에서 트랜잭션이 동시에 실행될 때, **Lost Update(갱신 분실)**나 **Inconsistent Retrieval(모순된 읽기)**와 같이 현실 세계의 논리와 맞지 않는 결과가 발생할 수 있다.
이를 해결하기 위해 단순히 순차적으로 실행(Serial Execution)하면 안전하지만 성능이 급격히 저하된다(Throughput 감소). 2PL은 동시성(Concurrency)을 유지하면서도, 결과적으로 직렬 실행(Serial Execution)한 것과 동일한 효과(Serializability)를 내기 위해 고안되었다.

> 📢 **섹션 요약 비유**: 2PL은 **'계산대 라인 정책'**과 같습니다. 한 번 계산을 시작하여 물건을 비우기 시작하면(축소 단계), 다시 매장으로 들어가 다른 물건을 담을 수 없도록(확장 단계 재진입 금지) 통제하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상태 정의**

2PL의 동작은 시간의 흐름에 따라 두 가지 명확한 페이즈(Phase)로 나뉜다. 아래 표는 각 단계의 핵심 특성을 기술한 것이다.

| 구성 요소 | 단계 명칭 | 허용 연산 | 금지 연산 | 내부 동작 메커니즘 |
|:---:|:---:|:---:|:---:|:---|
| **Phase 1** | **확장 단계** <br> (Growing Phase) | `Lock-S` (Shared Lock) <br> `Lock-X` (Exclusive Lock) | `Unlock` | 트랜잭션가 필요한 자원에 대해 **Lock Manager**에게 락을 요청. 이미 타 트랜잭션이 점유 시 대기(Queue). **보유 락 수(Lock Count)는 일방적으로 증가함.** |
| **Lock Point** | **락 포인트** | - | - | 확장 단계에서 축소 단계로 넘어가는 **전환 지점**. 이 시점에 트랜잭션이 보유한 최대 락 수를 기록하며, 이후 스케줄의 직렬 가능성 순서가 결정됨. |
| **Phase 2** | **축소 단계** <br> (Shrinking Phase) | `Unlock` | `Lock-S`, `Lock-X` | 트랜잭션이 커밋(Commit) 혹은 롤백(Rollback)에 앞서 보유한 락을 해제. **새로운 데이터 아이템 접근 불가.** |

**2. ASCII 구조 다이어그램 및 수행 흐름**

아래 다이어그램은 트랜잭션 T1이 2PL 규약을 준수하며 시간 흐름에 따라 락을 관리하는 상태 전이도(State Transition Diagram)이다.

```text
   [2PL Protocol State Transition]

   Number of Locks Held (Lock Count)
          ▲
          │
      5   │                  .---------------------------.
          │                 /  (3) Shrinking Phase       \
      4   │                /   (Unlock Operations Only)   \
          │               /                               \
      3   │              /                                 \
          │             /           . . . . . . . . . . . .
      2   │            /           /                        \
          │           /           /                          \
      1   │          /           /                            \
          │         /           /                              \
      0   │--------/-----------/------------------------\--------▶ Time
             Point(A)      Point(B)                   Point(C)
             Start        [Lock Point]                End (Commit)

   ① Point A -> Point B: [Growing Phase]
      - 락을 계속 획득함.
      - Unlock 절대 불가.
      - Lock Point (B) 도달 시 최대 락 보유 상태.

   ② Point B -> Point C: [Shrinking Phase]
      - 락을 해제하기 시작함.
      - Lock 절대 불가.
      - 트랜잭션 종료 시 모든 락 반환.
```

**3. 심층 동작 원리 및 알고리즘**

2PL이 직렬 가능성을 보장하는 이유는 **'락 포인트(Lock Point)'**의 존재 때문이다. 트랜잭션들이 서로 충돌하는 연산(Conflicting Operation, 예: Read-Write, Write-Write)을 수행할 때, 2PL을 준수하는 모든 트랜잭션은 **자신의 락 포인트에 도달한 순서대로 직렬화 가능**하다. 만약 T1이 A를 읽고 있고 T2가 A를 쓰려 한다면, T2는 T1의 락이 해제될 때까지 대기해야 하므로, 결과적으로 T1의 실행이 T2보다 먼저 처리된 것과 같다.

[Code Snippet: Conceptual Logic]
```python
# Pseudo-code for Lock Manager in 2PL
class Transaction:
    def __init__(self, tid):
        self.tid = tid
        self.state = "GROWING"  # Initial State
        self.locks_held = set()

    def acquire_lock(self, item, mode):
        # 2PL Rule 1: Cannot acquire lock if state is SHRINKING
        if self.state == "SHRINKING":
            raise ProtocolViolationError("Lock request in Shrinking Phase")
        
        # Request Lock from Lock Manager
        # wait if conflict...
        self.locks_held.add(item)

    def release_lock(self, item):
        self.locks_held.remove(item)
        
        # 2PL Rule 2: First unlock triggers Shrinking Phase
        if self.state == "GROWING":
            self.state = "SHRINKING" # Lock Point passed
```

> 📢 **섹션 요약 비유**: 2PL의 동작은 **'등산 급수 물통 채우기'**와 같습니다. 산행(트랜잭션) 초반에는 물이 부족하면 계속 물통을 채우기만 하다가(Growing), 물통이 꽉 차는 순간(Lock Point) 이후에는 목적지에 도달할 때만 물을 마시거나 쏟을 수(Shrinking) 있으며, 도중에 다시 물을 채우러 돌아갈 수 없는 원칙을 따릅니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기본 2PL vs 엄격 2PL (Strict 2PL) vs 강한 엄격 2PL (Rigorous 2PL)**

기본적인 2PL은 직렬 가능성은 보장하지만, 데이터 무결성 측면에서 **'갱신 연쇄 복귀(Rollback Cascading)'** 문제를 야기할 수 있다. 이를 해결하기 위해 실무에서는 변형된 형태를 사용한다.

| 비교 항목 | 기본 2PL (Basic 2PL) | 엄격 2PL (Strict 2PL) | 강한 엄격 2PL (Rigorous 2PL) |
|:---|:---|:---|:---|
| **락 해제 시점** | 축소 단계 진입 후 즉시 해제 가능 | **커밋(Commit) 시 일괄 해제** | **커밋(Commit) 시 일괄 해제** |
| **읽기 락(S-Lock)** | 조기 해제 가능 | 커밋 시 유지 | 커밋 시 유지 |
| **쓰기 락(X-Lock)** | 조기 해제 가능 | **커밋 시까지 유지** | **커밋 시까지 유지** |
| **주요 장점** | 동시성(Concurrency)이 상대적으로 높음 | **Rollback Cascading 방지** (안정성) | 복구 매커니즘 단순화 (Recovery Simplified) |
| **주요 단점** | 오염된 데이터 읽기(Dirty Read) 가능성 발생 | 락 유지 시간 증가로 병행 성능 저하 | 동시성 저하 |
| **실무 적용도** | 낮음 (이론적 모델) | **매우 높음 (DBMS 표준)** | 높음 (일부 고성능 DB) |

**2. 타 과목 융합 관점**

*   **운영체제(OS)와의 시너지**: 2PL의 기본 철학은 OS 커널의 **세마포어(Semaphore)** 또는 **뮤텍스(Mutex)**의 기능과 동일하다. 다만 DB는 데이터의 '논리적 일관성(Logic Consistency)'을 보장해야 하므로, 단순한 이진 락(Binary Lock)이 아닌 공유/베타적(S/X) 모드와 **그래프 기반의 교착 상태 탐지(Deadlock Detection)**가 결합된 고도화된 형태로 발전했다.
*   **네트워크(분산 DB)와의 상관관계**: 분산 데이터베이스 환경(Distributed DB)에서는 2PL이 **'분산 2PL(Distributed 2PL)'**으로 확장된다. 이때는 단일 노드의 락 매니저가 아닌, **코디네이터(Coordinator)**가 전체 트랜잭션의 2단계 커밋(2PC, Two-Phase Commit)과 2PL을 협력 제어하므로, 네트워크 지연(Latency)과 프로토콜 오버헤드가 비즈니스 성능에 치명적 영향을 미칠 수 있다.

**3. 정량적 성능 분석 (TPS vs Consistency)**

*   **Concurrency Level**: 기본 2PL > Strict 2PL
*   **Recovery Cost**: Strict 2PL < 기본 2PL (Cascade 방지로 UNDO 로그 감소)

> 📢 **섹션 요약 비유**: 기본 2PL은 **'즉석 카페 테이블 예약'**과 같아서, 자리를 일찍 비워주면 다른 손님(트랜잭션)이 이용할 수 있어 효율적이지만, 앉은 사람이 다시 오거나 난동을 부리면(롤백) 옆 사람에게 영향을 줍니다. **엄격 2PL(Strict 2PL)**은 **'호텔 체크아웃 시스템'**처럼, 손님이 룸을 완전히 비우고 카드키를 반납할 때까지(Commit) 다른 사람에게 방을 주지 않아 안전하지만, 방이 비어 있어도 대기해야 하는 비효율이 발생합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

*   **Scenario A: 금융권 계좌 이체 시스템**
    *   **상황**: A 계좌에서 B 계좌로 100만원 이체. 이체 도중 장애 발생 시 복구가 필수적임.
    *   **결정**: **Strict 2PL (엄격 2PL)** 적용.
    *   **이유**: 갱신 연쇄 복귀를 방지해야 한다. 만약 중간 단계에서 락을 풀면 다른 트랜잭션이 변경 중인 데이터를 읽을 수 있어, 롤백 시 데이터 정합성이 무너질 위험이 있음.

*   **Scenario B: 대규모 로그 분석 시스템 (OLAP)**
    *   **상황**: 하루 단위로 배치(Batch) 돌면서 대량 데이터를 수정.
    *   **결정**: 2PL 완화 또는 MVCC(Multi-Version Concurrency Control) 혼용 고려.
    *   **이유**: 2PL은 락 경합(Lock Contention)이 심해 대용량 처리에서 병목이 됨. 현대 DBMS는 2PL의 엄격한 제약을 완화하기 위해 **MVCC**를 기본으로 사용하여 읽기 차단을 방지함.

**2. 도입 및 운영 체크리스트**

*   **기술적 검토**
    *   [ ] 현재 DBMS의 기본 Locking Mechanism 확인 (MySQL InnoDB는 Record Lock + Gap Lock 사용)
    *   [ ] `Lock Wait Timeout` 설정 적정성 점검 (교착 상태 발생 시 대기 시간)
    *   [ ] 트랜잭션 범위(Transaction Scope) 최소화 (2PL 구간을 짧게 가져갈수록 병목 감소)

*   **운영/보안적 검토**
    *   [ ] Deadlock Monitor (교착 상태 감시기) 활성화 및 로그 수집
    *   [ ] 긴 트랜잭션(Long-running Transaction) 탐지 알림 설정 (비즈니스 로직 최적화 필요)

**3. 안티패턴 (Anti-Pattern)**

*   **락 변환(Lock Conversion) 미고려**: S-Lock을 가진 상태에서 X-Lock으로 업그레이드할 때, 교착 상태가 발생하기 쉽다.
*   **사용자 인터페이스에서의 트랜잭션 장애**: 사용자가 "