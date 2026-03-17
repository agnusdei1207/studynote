+++
title = "221. 강건한 2단계 락킹 (Rigorous 2PL)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 221
+++

# 221. 강건한 2단계 락킹 (Rigorous 2PL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 강건한 2단계 락킹(Rigorous 2PL)은 트랜잭션(Transaction)이 획득한 **모든 유형의 락(Lock)**을 커밋(Commit) 혹은 어보트(Abort) 시점까지 단 한 건도 해제하지 않고 보유하는 가장 엄격한 동시성 제어 프로토콜입니다.
> 2. **가치**: 데이터베이스의 일관성(Consistency)과 회복가능성(Recoverability)을 물리적으로 보장하며, 연쇄적 롤백(Cascading Rollback)을 완전히 방지하여 금융 결제나 재무 정산 등 무결성이 절대적인 시스템의 핵심 안전장치가 됩니다.
> 3. **융합**: 운영체제(OS)의 교착상태(Deadlock) 관리 기법과 밀접하게 연관되며, 트랜잭션 격리 수준(Isolation Level) 중 가장 높은 단계인 'Serializable'을 구현하는 구현 기반입니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**강건한 2단계 락킹 (Rigorous Two-Phase Locking)**은 트랜잭션의 생명주기 동안 락 획득(Expanding Phase)과 락 해제(Shrinking Phase)의 경계를 명확히 하되, **해제 단계(Shrinking Phase)를 트랜잭션 종료 직후의 단 일순간으로만 허용**하는 가장 보수적인 2PL(2-Phase Locking) 변형입니다.
일반적인 2PL이 락의 해제 시점을 자유롭게 허용하는 반면, Rigorous 2PL은 트랜잭션이 Commit 혹은 Abort 로그를 완료하기 전까지는 읽기 락(S-Lock)과 쓰기 락(X-Lock)을 포함한 **모든 잠금을 반납하지 않습니다**. 이로 인해 어떤 트랜잭션도 현재 활성 트랜잭션이 수정한 데이터를 읽거나 참조할 수 없으므로, 데이터베이스는 항상 "커밋된 데이터만 보이는" 안전한 상태를 유지합니다.

**💡 비유: 도서관의 완벽한 독점**
일반적인 독서실이 책을 다 보면 바로 꽂아두고 다른 책을 보는 것과 달리, Rigorous 2PL은 도서관에서 책을 빌릴 때 '나가는 문 앞'에서야 모든 책을 한꺼번에 반납하는 규칙과 같습니다. 내가 도서관에 있는 동안(트랜잭션 활성화) 다른 사람은 내가 빌린 책을 절대 볼 수 없으므로, 책의 내용이 바뀔지라도 혼란은 일어나지 않습니다.

**등장 배경 및 필요성**
1.  **기존 한계**: 완화된 락킹(Relaxed Locking) 전략들은 트랜잭션이 쓰기 락(X-Lock)을 일찍 해제할 경우, 다른 트랜잭션이 커밋되지 않은(Uncommitted) 데이터를 읽게 되어 **Dirty Read** 문제에 노출됩니다. 또한, 이후 롤백 발생 시 연쇄적으로 다른 트랜잭션도 롤백해야 하는 **Cascading Rollback** 오버헤드가 발생합니다.
2.  **혁신적 패러다임**: "해제를 미루자(Late Release)". 모든 락을 종료 시까지 유지함으로써, **회복가능 스케줄(Recoverable Schedule)**을 자동으로 보장하고, **연쇄 롤백을 구조적으로 불가능**하게 만듭니다.
3.  **현재 비즈니스 요구**: 실시간 금융 거래, 재무 재무제표 생성, 재고 관리 등 데이터의 정합성이 깨지면 시스템 자체의 신뢰가 무너지는 영역에서는 성능 저하를 감수하고서라도 이 방식이 채택됩니다.

> **📢 섹션 요약 비유**: Rigorous 2PL은 **'국가 기밀 문서를 다루는 보관실'**과 같습니다. 작업자는 보관실 안에 있는 동안 문서를 읽거나 수정할 수 있지만, 보안 규정상 절대 문서를 책상에 두고 나갈 수 없고, 퇴실할 때 모든 문서를 보관함에 완벽히 납부해야만 다음 사람이 입장할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 (동적 상태 테이블)**
Rigorous 2PL의 핵심은 락 매니저(Lock Manager)가 트랜잭션의 상태와 락 요청을 제어하는 방식에 있습니다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|
| **Tx (Transaction)** | 작업 단위 | DBMS의 논리적 실행 단위로, 시작(Start)부터 종료(End)까지의 원자성을 가짐 | `BEGIN_TX` ~ `END_TX` | 작업자 |
| **Lock Manager (LM)** | 트래픽 감시관 | 락 요청 큐(Lock Queue)를 관리하며, 충돌 발생 시 대기(Wait) 또는 교착(Deadlock) 처리 | `Lock(S)`, `Lock(X)` | 출입통제관 |
| **S-Lock (Shared Lock)** | 읽기 잠금 | 데이터 읽기 전 획득. **Rigorous 2PL에서는 Commit 전까지 해제 금지** | `SELECT ... FOR SHARE` | 읽기 전용 승인 |
| **X-Lock (Exclusive Lock)** | 쓰기 잠금 | 데이터 수정 시 획득. 다른 모든 트랜잭션의 접근을 차단 | `UPDATE`, `DELETE` | 독점 점유 승인 |
| **LTM (Lock Table)** | 상태 저장소 | 어떤 트랜잭션이 어떤 데이터에 락을 걸었는지 저장하는 메모리 상의 해시 테이블 | Memory Structure | 대장부 기록부 |

**ASCII 구조 다이어그램: 락의 수명 주기 비교**
아래는 일반적인 2PL과 강건한 2PL의 시간선(Time-line) 비교입니다. Rigorous 2PL은 **Unlock 시점**이 유일하게 **Commit/Abort**와 일치함을 확인할 수 있습니다.

```text
[ Timeline ] -------------------------------------------------------->
             [Acquire]                  [Processing]              [End]
Basic 2PL   : [L][L]----[U][U]------------[L]------[U][U]------[Commit]
             (S/X)      (Unlock Mixed)    (New Lock) (Unlock)   (End)

Strict 2PL  : [L][L]-------------------------[U][U]------------[Commit]
             (S/X)      (Hold X only)      (Unlock)            (End)

Rigorous 2PL: [L][L]--------------------------------------[U][Commit]
             (S/X)      (Hold ALL!)              (Unlock All)   (End)
             └─ Phase 1 (Growing) ─┘           └─ Phase 2 (Shrinking) ─┘
             (모든 락 유지)                       (종료 직전 일제 해제)
```
*(L: Lock, U: Unlock, S: Shared Lock, X: Exclusive Lock)*

**다이어그램 해설**
Rigorous 2PL의 다이어그램을 보면 `Phase 1(Growing)` 구간이 트랜잭션의 전체 작업 시간과 거의 일치하며, `Phase 2(Shrinking)` 구간은 종료 직후의 점(point)으로 수렴합니다. 이는 트랜잭션이 활성화된 기간 동안 자신이 가진 모든 권한(Lock)을 놓지 않음을 의미합니다. 다른 트랜잭션은 이 기간 동안 해당 데이터에 대해 접근 불가능한 상태로 Blocking됩니다. 이로 인해 **Cascading Rollback**이 발생할 가능성이 구조적으로 0%가 됩니다.

**심층 동작 원리 및 의사결정 코드**
다음은 Lock Manager가 Rigorous 2PL 규칙을 적용하는 핵심 알고리즘 의사코드입니다.

```python
class LockManager:
    def acquire_lock(self, tx, data, lock_mode):
        # 1. 충돌 확인 (현재 락과 요청 락이 호환되는지?)
        current_lock = self.get_lock(data)
        
        if self.is_compatible(current_lock, lock_mode):
            self.grant_lock(tx, data, lock_mode) # 락 부여
        else:
            # 2. Rigorous 2PL의 핵심: 기다림(Wait) 또는 중단
            # 이미 커밋되지 않은 트랜잭션이 락을 잡고 있다면 무조건 대기
            self.wait(tx, data) 
            # (참고: 실무에서는 타임아웃이나 데드락 감지 스레드가 작동)

    def release_all_locks(self, tx):
        # 3. 핵심 제약: COMMIT/ABORT 시점 외에는 이 함수가 호출되지 않음
        for data in tx.locks_held:
            self.unlock(data)
        
        # 4. Unlock 이후 대기하던 다른 트랜잭션 깨우기
        self.wakeup_waiting_txs()
```

> **📢 섹션 요약 비유**: Rigorous 2PL의 동작 원리는 **'소부하는 맹주'**와 같습니다. 일반적인 방식(Conservative)은 계약을 조금씩 확정 짓는 반면, Rigorous 2PL은 계약이 완전히 끝날 때까지 집행 유예를 하지 않고 모든 권한을 행사하다가, 끝나는 순간에 모든 권한을 내려놓습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교 분석표**
Rigorous 2PL을 타 프로토콜과 다각도로 비교 분석합니다. (S-Lock: 읽기 락, X-Lock: 쓰기 락)

| 구분 | Rigorous 2PL (강건 2PL) | Strict 2PL (엄격 2PL) | Conservative 2PL (보수 2PL) | 최적화(Optimistic) |
|:---|:---|:---|:---|:---|
| **락 해제 시점** | **Commit/Abort 시점** (일제 해제) | X-Lock만 종료 시 유지 | 시작 전 모두 획득 | Validation 시 |
| **S-Lock 유지** | **종료 시까지 유지** | 중간 해제 허용 (가능) | 종료 시까지 유지 | 없음 |
| **회복가능성** | **보장** (Cascading Rollback 방지) | 보장 (X-Lock 유지로) | 보장 | 확인 필요 |
| **직렬화 가능성** | **보장** | 보장 | 보장 | 충돌 시 롤백 |
| **병행성 (Concurrency)** | **매우 낮음** (낭비 심함) | 중간 | 매우 낮음 (초기 락 비용) | 높음 |
| **주요 용도** | **금융, 핵심 정산** | 일반적인 DB 기본값 | 분산 DB 등 | 분석, 배치 작업 |

**과목 융합 관점 분석**

1.  **운영체제 (OS) - 교착상태(Deadlock)**
    Rigorous 2PL은 락을 오래 동안 잡고 있으므로, **교착상태(Deadlock)** 발생 확률이 다른 2PL 대비 높습니다. 이를 해결하기 위해 OS의 **Wait-Die(기다림-죽음)** 또는 **Wound-Wait(상처-기다림)** 같은 타임스탬프 기반 프로토콜이나, **Wait-for Graph(대기 그래프)** 순환 감지 알고리즘이 필수적으로 결합됩니다. 즉, "안전성은 Rigorous 2PL이 맡고, 교착 해제는 OS가 맡는" 구조입니다.

2.  **소프트웨어 공학 - 트랜잭션 격리 수준 (Isolation Levels)**
    **ANSI/ISO SQL 표준**에서 정의하는 `SERIALIZABLE` 수준을 구현하는 가장 손쉬운 물리적 수단이 바로 Rigorous 2PL입니다. `REPEATABLE READ` 수준에서 발생할 수 있는 **Phantom Read(팬텀 리드)** 현상을Predicate Lock(술어 락)을 통해 Rigorous 2PL이 적용된다면 완벽히 차단합니다. 따라서 "읽는 데이터가 변하지 않는다"는 논리적 요구사항을 물리적 Lock이 충족시키는 융합 지점입니다.

> **📢 섹션 요약 비유**: Rigorous 2PL은 **'고속도로의 폐쇄형 교통 통제'**와 같습니다. 모든 차량(트랜잭션)이 목적지에 도착할 때까지 진입로를 막아버리기 때문에, 안전사고(데이터 불일치)는 0%에 가깝지만, 도로 전체의 흐름(처리량 TPS)은 극도로 정체됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **시나리오: 은행 야간 일일 마감 배치 (Batch)**
    -   **상황**: 전체 고객의 잔액을 계산하여 이자를 입금하고 이체 내역을 집계하는 배치 작업.
    -   **판단**: 수천만 건의 데이터를 수정하는 중간에 다른 세션(인터넷 뱅킹 등)이 데이터를 조회하면 `Dirty Read`나 `Inconsistent Read`가 발생해 장부가 일치하지 않습니다.
    -   **전략**: 배치 시작 시 `BEGIN TRANSACTION` 후, **Rigorous 2PL** 모드로 전환하여 배치가 완료되고 `COMMIT` 될 때까지 모든 테이블에 X-Lock을 걸거나 전체 DB를 Read Only 모드로 전환합니다. 성능 저하는 발생하나, 재무 무결성을 위해 불가피합니다.

2.  **시나리오: 실시간 재고 관리 시스템**
    -   **상황**: 한정된 상품(예: 콘서트 티켓) N개를 동시에 수만 명이 예매하려 함.
    -   **문제**: 일반적인 락킹은 '선착순'이 아닌 '먼저 락을 딴 놈이 잡는' 구조가 되어, 특정 세션이 독점할 수 있습니다.
    -   **의사결정**: 너무 많은 병목을 유발하므로, **Rigorous 2PL은 권장되지 않습니다.** 대신 row-level locking과 Optimis