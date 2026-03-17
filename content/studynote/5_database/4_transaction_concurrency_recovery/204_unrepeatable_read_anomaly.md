+++
title = "204. 모순성 (Inconsistency / Unrepeatable Read)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 204
+++

# 204. 모순성 (Inconsistency / Unrepeatable Read)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모순성(Inconsistency) 또는 비반복 읽기(Unrepeatable Read)는 트랜잭션의 격리 수준(Isolation Level)이 낮을 때 발생하며, **단일 트랜잭션 내에서 동일한 데이터를 두 번 이상 읽을 때, 중간에 다른 트랜잭션에 의해 데이터가 수정(Update)되어 읽기 결과가 달라지는 현상**을 의미합니다.
> 2. **가치**: 재고 관리나 금융 결산처럼 "읽기 일관성(Read Consistency)"이 필수적인 시스템에서 심각한 데이터 무결성 훼손을 야기하므로, 이를 방지하기 위해 DBMS는 **Shared Lock(공유 잠금)** 유지 또는 **MVCC(Multi-Version Concurrency Control)** 기반의 Snapshot Read 기능을 제공합니다.
> 3. **융합**: 대용량 처리에서 Locking 기반의 해결책은 병목(Bottleneck)을 유발하므로, 현대적인 DB(MySQL, PostgreSQL 등)는 **Non-Blocking Read**를 구현하기 위해 Undo Log를 활용한 MVCC 방식을 채택하여 동시성(Concurrency)과 일관성(Consistency)을 동시에 확보합니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의 및 철학**
모순성(Inconsistency)은 데이터베이스 트랜잭션의 ACID 특성 중 **Isolation(격리성)**이 보장되지 않을 때 발생하는 대표적인 현상입니다. 구체적으로는 **Unrepeatable Read(비반복 읽기)**라고 하며, 하나의 트랜잭션 내에서 `SELECT` 쿼리를 통해 특정 데이터를 조회했을 때, 그 사이 다른 트랜잭션이 해당 데이터를 `UPDATE` 또는 `DELETE`하고 커밋(commit)할 경우, 첫 번째 트랜잭션이 다시 같은 데이터를 읽었을 때 값이 변경되거나 사라져버리는 현상입니다.

**2. 등장 배경 (배경 vs 한계)**
- **① 기존 한계**: 초기 관계형 데이터베이스(RDBMS)나 높은 동시성을 요구하는 시스템에서는 트랜잭션 처리량(Transaction Per Second, TPS)을 높이기 위해 데이터 읽기 시 잠금(Lock)을 사용하지 않거나 매우 짧게 유지했습니다. 이는 `READ UNCOMMITTED`나 `READ COMMITTED` 수준에서 빈번한 모순성을 초래했습니다.
- **② 혁신적 패러다임**: 데이터의 정합성이 생명인 금융이나 회계 시스템에서는 "내가 조회하는 순간의 데이터는 끝까지 변하면 안 된다"는 요구가 발생했습니다. 이를 해결하기 위해 **2PL(Two-Phase Locking)** 프로토콜이 도입되었으나, 이는 읽기 연산마저 쓰기와 충돌하여 병목을 유발했습니다.
- **③ 현재의 비즈니스 요구**: 현대의 웹 서비스는 초당 수만 건의 요청을 처리하면서도 결제 및 정산 데이터의 일관성을 보장해야 합니다. 따라서 Locking을 최소화하면서 일관성을 확보하는 **MVCC(Multi-Version Concurrency Control)** 기술이 표준으로 자리 잡았습니다.

**3. 동작 시나리오 시각화**
아래는 모순성이 발생하는 표준적인 시나리오입니다.

```text
         [모순성 (Unrepeatable Read) 발생 시나리오]

  Time │         Transaction A (TX_A)              │         Transaction B (TX_B)
  ─────┼───────────────────────────────────────────┼───────────────────────────────────────────
   t1  │  BEGIN;                                   │
   t2  │  SELECT balance FROM users WHERE id=1;    │
       │  (Result: 10,000원)                       │
   t3  │                                           │  BEGIN;
   t4  │                                           │  UPDATE users SET balance=20,000 WHERE id=1;
   t5  │                                           │  COMMIT;  (데이터 변경 확정)
   t6  │  SELECT balance FROM users WHERE id=1;    │
       │  (Result: 20,000원) ◀──💥 INCONSISTENCY!  │
   t7  │  COMMIT;                                  │
  ─────┴───────────────────────────────────────────┴───────────────────────────────────────────
  
  문제점: TX_A는 자신이 시작한 트랜잭션 내에서 "id=1의 잔고"가 
          동일하리라 기대했으나(Logic Consistency), 
          중간에 TX_B에 의해 값이 변경되어 로직에 오류를 발생시킴.
```

**📢 섹션 요약 비유**
모순성은 **"계산기로 숫자를 더하고 있는데, 제3자가 숫자판 위의 숫자를 몰래 지우고 다른 숫자로 바꿔놓아, 결과적으로 앞뒤가 맞지 않는 계산서가 작성되는 상황"**과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 메커니즘**
모순성을 해결하기 위한 주요 아키텍처 구성 요소는 다음과 같습니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/특징 |
|:---|:---|:---|:---|
| **Lock Manager (잠금 관리자)** | 데이터 접근 직렬화 | 트랜잭션이 데이터를 읽을 때 **Shared Lock (S-Lock)**을 획득하고, 트랜잭션 종료 시까지 유지하여 다른 트랜잭션의 쓰기를 방지 | 2PL (Two-Phase Locking) |
| **MVCC Engine** | 비동시성 버전 관리 | 데이터 변경 시 **Undo Log**에 이전 버전을 저장하고, 읽기 요청이 들어오면 트랜잭션 ID(Sequence Number)를 비교하여 적절한 과거 버전을 제공 | Non-Blocking Read |
| **Undo Log (언두 로그)** | 과거 데이터 보관 | Update 실행 전 원본 데이터를 백업하는 저장소. Rollback 시 복구용으로 쓰이며, MVCC에서는 과거 데이터 조회용으로 활용 | Cyclic Buffer |
| **Transaction ID (TX_ID)** | 순서 및 버전 판별 | 트랜잭션 생성 순서 부여하는 고유 번호. 데이터 행(Row)마다 `DB_TRX_ID`를 저장하여, 현재 트랜잭션보다 나중에 변경된 사항을 무시하게 함 | Monotonic Increment |
| **Isolation Level (격리 수준)** | 정책 결정 계층 | `REPEATABLE READ` 이상 설정 시, 트랜잭션 내 첫 번째 Read 시점의 Snapshot을 고정하여 모순성 차단 | ANSI/ISO SQL Standard |

**2. 핵심 아키텍처: MVCC vs Locking**
모순성 해결의 핵심은 "어떻게 동시성을 희생하지 않고 일관성을 잠글 것인가"에 있습니다.

```text
    [모순성 해결 아키텍처 비교]

    방법 A: Locking Based (Shared Lock)
    ──────────────────────────────────────────────
       TX_A (Read) ──[ S-LOCK 획득 ]──> 데이터 (10)
                                      ▲
                                      │ (쓰기 차단)
                                      │
       TX_B (Update) ────────────[ 대기/블로킹 ]...
       
       *장점: 매우 엄격한 일관성
       *단점: 읽기 작업 때문에 쓰기가 막힘 (Concurrency 저하)

    방법 B: MVCC Based (Multi-Version)
    ──────────────────────────────────────────────
       Memory Buffer Pool (Disk)
       ┌───────────────────────────────────┐
       │ Row ID: 101                        │
       │ Current Val: 200 (TX_ID: 20)       │ ◀── TX_B가 최신 데이터로 Update
       │───────────────────────────────────│
       │ Undo Log: 100 (TX_ID: 10) <───────┘─── TX_A를 위한 과거 버전 보관
       └───────────────────────────────────┘
                ▲             │
           (Read)        (Update)
           TX_A            TX_B
       
       *TX_A는 자신의 TX_ID(10)보다 나중에 변경된 데이터를 무시하고,
        Undo Log의 100을 읽음.
       *TX_B는 최신 데이터 200을 읽음.
       *결과: 두 트랜잭션이 Lock으로 경쟁하지 않고 병렬 실행됨.
```

**3. 심층 동작 원리 (MVCC의 Read View)**
대표적인 오픈소스 DB인 **MySQL InnoDB** 엔진의 동작 원리를 코드 및 로직으로 분석합니다.

*   **Read View 구조체**: 트랜잭션이 시작될 때 현재 활성화된 트랜잭션 리스트를 스냅샷으로 저장합니다.
*   **가시성 판별 로직**:
    1.  `DB_TRX_ID` < `Read View.min_trx_id`: 내 트랜잭션보다 이전에 커밋된 데이터 → **Visible (읽기 가능)**
    2.  `DB_TRX_ID` >= `Read View.max_trx_id`: 내 트랜잭션이 시작한 후에 커밋된 데이터 → **Invisible (Undo Log 접근)**

```sql
-- [의사 코드] MVCC Visibility Check
FUNCTION CheckVisibility(row_trx_id, read_view):
    IF row_trx_id < read_view.up_limit_id:
        RETURN VISIBLE; -- 오래된 데이터, 안전함
    ELSE IF row_trx_id >= read_view.low_limit_id:
        RETURN INVISIBLE; -- 미래의 데이터, Undo Log로 이동
    ELSE:
        IF row_trx_id IN read_view.active_ids:
            RETURN INVISIBLE; -- 아직 활성화된 트랜잭션이 수정 중, Undo Log로 이동
        ELSE:
            RETURN VISIBLE; -- 커밋된 이후의 데이터, 안전함
    END IF
END FUNCTION
```

**4. 수식적 모델링**
트랜잭션 일관성을 만족하는 상태 $S$는 다음과 같이 정의됩니다.
$$S_{t1} = S_{t2} \quad (where \quad t1, t2 \in T_{range})$$
여기서 $S_{t1}$은 트랜잭션 $T$ 내의 시점 $t1$에서의 데이터 상태입니다. 모순성은 $S_{t1} \neq S_{t2}$인 상황을 방지하는 것입니다.

**📢 섹션 요약 비유**
MVCC 아키텍처는 **"도서관에서 사본 복사기를 둬서, 누군가 원본에 필기해도 내가 빌린 복사본에는 변함이 없게 하는 것"**과 같습니다. 원본에 쓰는 사람(쓰기 트랜잭션)과 복사본을 읽는 사람(읽기 트랜잭션)이 서로 방해하지 않습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 격리 수준별 모순성 허용 비교**

| 격리 수준 (Isolation Level) | 모순성 (Inconsistency) 발생 여부 | 해결 방식 | 성능 영향 |
|:---|:---|:---|:---|
| **Read Uncommitted** | **발생함** (갱신 분실, 더티 리드) | 해결 안 함 | 가장 높은 성능 |
| **Read Committed (RC)** | **발생함** (Non-Repeatable Read) | `SELECT` 시점만 Lock 걸거나 Snapshot 생성 | 일반적 (Oracle 기본값) |
| **Repeatable Read (RR)** | **방지함** | 트랜잭션 시작 시점 Snapshot 고정 (MySQL 기본값) | 락 경합 발생 가능 |
| **Serializable** | **완전 방지** | 읽기 범위에 범위 Lock(Range Lock) 부여 | 가장 낮은 성능 (병목 심화) |

**2. 기술 스택별 융합 관점**

*   **(1) 데이터베이스 & 애플리케이션 계층 (Persistence & Logic)**:
    *   **관계**: 단순히 DB 격리 수준을 높인다고 해결되지 않습니다. 예를 들어, `SELECT ... FOR UPDATE` 구문을 사용하여 명시적으로 **X-Lock(Exclusive Lock)**을 걸면 모순성을 막을 수 있지만, 이는 교착상태(Deadlock) 위험을 내포합니다. 따라서 서비스 레벨에서 **낙관적 락(Optimistic Locking - Version Column)**을 사용하여 애플리케이션 레벨에서 충돌을 감지하는 하이브리드 전략이 유효합니다.
*   **(2) 운영체제 (OS) & 분산 시스템 (Distributed System)**:
    *   **관계**: 분산 DB(예: Google Spanner, CockroachDB)에서는 **True Time**이나 **HLC(Hybrid Logical Clock)**를 사용하여 전역적으로 일관된 스냅샷을 생성합니다. 이는 단일 노드의 모순성 해결을 넘어, 네트워크 지연(Latency)이 발생하는 분산 환경에서도 모순성이 발생하지 않도록 **Clock Synchronization** 기술과 융합됩니다.

**3. 정량적 의사결정 매트릭스**
모순성 방지 기술을 선택할 때의 고려 사항입니다.

```text
   [Pain Point vs Solution Matrix]

   High Concurrency (TPS)  ────────────────────────────
   │
   │                         [MVCC]
   │                         (MySQL/PostgreSQL)
   │                         • Low Contention
   │                         • More Storage (Undo Log)
   │
   │─────────────────────────────────────── Accuracy ──>
   │
   │                         [Pessimistic Lock]
   │                         (2PL / Select For Update)
   │                         • High Contention
   │                         • High Accuracy
```

**📢 섹션 요약 비유**
격리 수준을 높이는 것은 **"보안 검색대를 설치하여 검문을 강화하는 것"**과 같습니다. 검사가 엄격해질수록(격리 수준 상승) 통과 시간(성능)은 늦어지지만, 무단 침입자(모순성)를 막을 수 있습니다. MVCC는 **'사전 등록된 신원증(스냅샷)'을 미리 나눠주어 검색대를 통과하지 않고도 입장하게 하는 시스템**입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 프로세스**

*   **Case 1: 금융 결제 시스템 (Accounting System)**
    *   **상황**: 당일 10시 기준으로 모든 계좌의 잔액 합계를 산출하는 배치 작업이 수행 중입니다. 이 과정에서 다른 사용자가 입금을 시도합니다.
    *   **문제**: 배치가 1계좌를 읽고 합산하는 사이 입금이 발생하면, 배치의 합계금액과 실제 장부의 합계금액이 맞지 않는 '대차 불일치'가 발생합니다.