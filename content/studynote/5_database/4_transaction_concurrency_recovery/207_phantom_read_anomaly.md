+++
title = "207. 유령 읽기 (Phantom Read) - 사라졌다 나타나는 데이터"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 207
+++

# 207. 유령 읽기 (Phantom Read) - 사라졌다 나타나는 데이터

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 유령 읽기(Phantom Read)는 한 트랜잭션 내에서 **동일 범위 쿼리(Range Query)를 수행할 때, 타 트랜잭션의 삽입(INSERT) 또는 삭제(DELETE)로 인해 결과 집합(Result Set)의 행(Row) 개수가 변하거나 새로운 행이 나타나는 현상**이다.
> 2. **가치**: 데이터 정합성을 위반하여 재고 수급, 재무 결산 등 **집합 기반(Base Aggregate) 연산에서 심각한 오차를 유발**할 수 있으며, 이를 방지하기 위해 DBMS는 높은 비용의 Locking이나 MVCC(Multi-Version Concurrency Control) 전략을 사용한다.
> 3. **융합**: MySQL InnoDB의 `Next-Key Lock` 알고리즘(Record Lock + Gap Lock)과 OSI 7계열의 트랜잭션 격리 수준(Transaction Isolation Level) 표준이 밀접하게 연관되며, 동시성 제어(Concurrency Control) 설계의 핵심 체크 포인트다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**유령 읽기(Phantom Read)**란, 트랜잭션의 일관성이 깨지는 현상 중 하나로, **특정 범위(Query Range)를 조회했을 때, 처음에는 없던 데이터가 다른 트랜잭션의 커밋으로 인해 '유령'처럼 갑자기 나타나거나(INSERT), 존재하던 데이터가 사라지는(DELETE) 현상**을 의미합니다.

이는 단순히 값의 변경이 아니라 **'결과 집합의 구성要素(Element) 자체가 변하는 것'**을 다룹니다. 예를 들어, `WHERE age > 20` 조건으로 10명을 조회했는데, 도중에 다른 트랜잭션이 25세 회원을 추가하여 다시 조회했을 때 11명이 되는 경우가 이에 해당합니다.

#### 2. 등장 배경 및 기술적 한계
관계형 데이터베이스(RDBMS) 발전 초기에는 Locking 비용을 줄이기 위해 낮은 격리 수준(Read Committed 등)을 기본으로 사용했습니다. 그러나 금융, 재무, 재고 관리 등에서 **"집합의 크기 변화"**를 허용할 수 없는 요구사항이 생기면서, 이를 어떻게 방지할 것인가가 중요한 과제로 떠올랐습니다.

단순히 `SELECT`만 수행하는 경우, 일반적인 행(Row) 단위의 공유 락(Shared Lock)은 조회 직후 해제되므로, 그 사이 틈새(Timing Gap)로 새로운 데이터가 들어오는 것을 막을 수 없습니다. 이를 해결하기 위해 범위 자체를 잠그는 **갭 락(Gap Lock)**이나 **순차 직렬화(Serializable)** 기술이 도입되었습니다.

#### 3. 아키텍처적 맥락
ACID(Atomicity, Consistency, Isolation, Durability) 속성 중 **Isolation(고립성)**을 보장하기 위한 핵심 기술 중 하나입니다. 단순 읽기 일관성과 달리 범위 기반의 일관성을 요구하기에, DBMS 내부적으로는 인덱스 구조와 밀접하게 동작하며 설계되어야 합니다.

```text
+---------------------+-----------------------------------------------+
| 격리 수준 (Level)    | 발생 가능성 (Possibility of Phantom)          |
+---------------------+-----------------------------------------------+
| Read Uncommitted    | Yes (Always)                                  |
| Read Committed      | Yes (Possible)                                |
| Repeatable Read     | Depends (Prevented by Locking/MVCC Strategy)  |
| Serializable        | No (Fully Prevented)                          |
+---------------------+-----------------------------------------------+
```

> **💡 비유**: **'입국 심사대'**와 같습니다. 직원(T1)이 현재 대기자 명단을 확인했는데, 그 사이 뒷문으로 새로운 대기자(T2)가 끼어들어 명단이 바뀌어버리는 혼란 상황입니다.

> **📢 섹션 요약 비유**: 유령 읽기는 **"공을 카운트 하는 사이에 다른 사람이 코트로 새로운 공을 던져 넣어, 전체 공의 개수가 달라진 상황"**과 같습니다. 이를 막으려면 카운트하는 동안 코트 전체에 빗장을 걸어야 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 (Components)

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 비유 (Analogy) |
|:---|:---|:---|:---|
| **범위 쿼리 (Range Query)** | 유령 읽기가 발생하는 대상 | 특정 조건(WHERE 절)을 만족하는 행의 집합을 찾는 검색 연산 | 탐색 범위 설정 |
| **갭 락 (Gap Lock)** | 빈 공간의 잠금 | 인덱스 레코드 사이의 빈 공간(Gap)에 락을 걸어, 해당 범위 내의 INSERT를 방지 | 빈 의자에 '예약' 표시 |
| **넥스트 키 락 (Next-Key Lock)** | InnoDB의 강력한 방어책 | **Record Lock(레코드 잠금) + Gap Lock(갭 잠금)**의 조합으로, 바로 앞의 레코드부터 갭까지를 하나의 단위로 잠금 | 내 옆자리와 빈자리를 동시 점유 |
| **MVCC (Multi-Version Concurrency Control)** | 비잠금형 일관성 | 데이터 변경 시 이전 버전(Undo Log)을 유지하여, 특정 시점(Snapshot)의 데이터를 읽게 함 | 과거의 사진을 보여줌 |
| **인덱스 (Index)** | 잠금의 범위 결정 | B-Tree 등의 구조를 통해 락을 거는 정확한 범위(Physical Range)를 식별 | 지도상의 구역 선정 |

#### 2. 발생 메커니즘 및 데이터 흐름 (ASCII Architecture)

유령 읽기는 주로 트랜잭션이 '범위'를 다룰 때 발생합니다. 아래는 **레코드 락(Record Lock)만으로는 유령 읽기를 막을 수 없음**을 보여주는 아키텍처 다이어그램입니다.

```text
[Phantom Read Architecture: Lock Failure Scenario]

      [ Index Structure (B-Tree Leaf Node View) ]
      
      Key:  10      20      30      40      50
           [  ]    [  ]    [  ]    [  ]    [  ]
            |       |       |       |       |
            +-------+-------+-------+-------+--- Indexed Column (ID)
            
  [Step 1] T1: SELECT * FROM table WHERE id > 20 AND id < 40;
           > Acquired 'Shared Lock' on Record 30 only.
           > (Lock is released immediately if Read Committed)
           
           ------------------------------------------------
           
           [T2 enters the GAP]  <<<<< GAP LOCK REQUIRED HERE!
           
  [Step 2] T2: INSERT INTO table VALUES (35, 'Ghost');
           > Inserts 35 into the space between 30 and 40.
           > T2 Commits. (Successfully written to Disk)
           
  [Step 3] T1: SELECT * FROM table WHERE id > 20 AND id < 40;
           > Result: [ 30, **35** ]  <-- Phantom appears!
           > Inconsistent Set detected.
```

**해설 (Explanation)**:
위 다이어그램은 T1이 `id=30`인 레코드만 조회하고 잠그는 상황을 가정합니다. T1이 트랜잭션을 유지하는 동안, T2는 20과 40 사이의 빈 공간(Gap)인 `id=35`에 데이터를 삽입합니다. T1이 다시 조회하면 `id=35`가 새롭게 보이게 되며, 이는 물리적인 레코드 락만으로는 방어되지 않음을 시사합니다.

#### 3. 핵심 알고리즘: Next-Key Lock 동작 원리

MySQL InnoDB 스토리지 엔진은 `REPEATABLE READ` 격리 수준에서 기본적으로 **Next-Key Lock**을 사용하여 유령 읽기를 방지합니다.

**수식 및 로직:**
`Next-Key Lock = (Index Record Lock) + (Gap Lock before Record)`

이는 실제 존재하는 인덱스 레코드를 잠그는 것과 더불어, 그 레코드 **바로 앞의 갭(Gap)까지 함께 잠금**으로써, 새로운 레코드의 생성을 원천 차단합니다.

**실무 코드 시뮬레이션 (Pseudo-SQL)**:

```sql
-- MySQL InnoDB Default Scenario
-- 트랜잭션 A (T1)
START TRANSACTION;
-- id가 10보다 큰 레코드를 조회. (데이터: 15, 20, 25가 존재한다고 가정)
-- InnoDB는 내부적으로 다음과 같은 Lock을 설정함:
-- 1. (Negative Infinity, 15] - Next-Key Lock
-- 2. (15, 20] - Next-Key Lock
-- 3. (20, 25] - Next-Key Lock
-- 4. (25, Positive Infinity) - Gap Lock
SELECT * FROM users WHERE id > 10 FOR UPDATE; 

-- 트랜잭션 B (T2)
START TRANSACTION;
-- T2는 10과 15 사이의 갭에 데이터를 넣으려 시도
INSERT INTO users VALUES (12, 'Hacker'); 
-- Result: WAITING (Locked by T1's Gap Lock)
-- T1이 COMMIT/ROLLBACK 할 때까지 대기해야 함.
```

#### 4. MVCC와의 관계
MVCC는 **읽기(SELECT) 작업에 대해서**는 트랜잭션 시작 시점의 스냅샷(Snapshot)을 제공하여, Non-repeatable Read나 Phantom Read를 **"논리적으로(Consistent Read)"** 방지합니다. 하지만 **`SELECT ... FOR UPDATE`**나 **`INSERT`** 작업이 얽혀 있을 때는 물리적인 락(Locking)이 우선 적용되어야 하며, 이때 갭 락(Gap Lock)이 필수적인 역할을 수행합니다.

> **📢 섹션 요약 비유**: Next-Key Lock은 **"해변의 울타리"**와 같습니다. 울타리(Record Lock)를 세우는 것뿐만 아니라, 울타리가 설치될 예정인 앞쪽 모래사장(Gap)에까지 '출입 금지' 테이프를 쳐서, 울타리 사이에 새로운 집이 생기는 것을 미리 막는 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교표 (Phantom Read vs. Non-repeatable Read)

| 구분 (Criteria) | 비반복 읽기 (Non-repeatable Read) | 유령 읽기 (Phantom Read) |
|:---|:---|:---|
| **발생 원인** | **수정 (UPDATE)** 또는 **삭제 (DELETE)** | **삽입 (INSERT)** 또는 **삭제 (DELETE)** |
| **관심 대상** | **단일 행 (Row)**의 값 변화 | **범위 (Range)**의 결과 집합 변화 |
| **핵심 이슈** | 데이터의 값이 달라짐 | 데이터의 개수나 존재 여부가 달라짐 |
| **방어 기술** | 행 단위 공유 락 (Row Shared Lock) | 갭 락 (Gap Lock) / Next-Key Lock |
| **MVCC 방어** | 스냅샷 읽기로 완벽 방어 가능 | 스냅샷 읽기로 방어 가능하나, Locking 모드에서는 Gap Lock 필수 |

#### 2. 격리 수준별 방어 전략 비교

| 격리 수준 (Isolation Level) | 동작 원리 (Mechanism) | 유령 읽기 발생 여부 | 성능 영향 (Performance Impact) |
|:---|:---|:---:|:---:|
| **Read Uncommitted** | Lock을 거의 사용하지 않음 | ⚠️ 발생 | 매우 낮음 (빠름) |
| **Read Committed** | 각 쿼리마다 새로운 스냅샷 생성 | ⚠️ 발생 | 낮음 |
| **Repeatable Read** | **MVCC + Next-Key Lock** (InnoDB) | 🟡 방어 (기본값) | 중간 (Lock 경합 발생 가능) |
| **Serializable** | 범위 읽기 시 공유 잠금(Shared Lock) 유지 | ✅ 완벽 방어 | 매우 높음 (병목 심각) |

#### 3. 타 과목 융합 분석
- **[OS (Operating System)]**: OS의 세마포어(Semaphore)나 뮤텍스(Mutex)는 주로 '단일 자원'에 대한 접근 제어를 다룹니다. 유령 읽기 방어를 위한 갭 락은 OS 관점에서 **'자원이 아직 생성되지 않은 가상의 공간(Candidate Space)'에 대한 접근 제어**로 확장할 수 있는 고급 개념입니다.
- **[네트워크 (Network)]**: TCP 흐름 제어(Flow Control)와 유사합니다. 데이터 손실을 방지하기 위해 윈도우 크기(Window Size)를 조절하듯이, DB는 갭 락을 통해 데이터 집합의 범위(Window)를 고정하여 일관성을 유지합니다.

> **📢 섹션 요약 비유**: 격리 수준의 선택은 **'보안 체크와 통행 속도의 트레이드오프'**와 같습니다. Serializable은 모든 사람에게 일일이 신분증을 검사하고 통로 자체를 막아버리는 엄격한 국경 검사이고, Read Uncommitted는 그냥 지나가게 하는 무방비 상태입니다. 우리는 중간단계인 Repeatable Read에서 스마트한 갭 락으로 균형을 찾습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정

**시나리오 1: 재고 관리 시스템 (Inventory Management)**
- **문제**: 창고의 현재 재고를 확인하여 부족한 분량을 주문하려는데, 주문 처리 중간에 다른 입고가 발생하여 수량이 맞지 않음.
- **해결**: 재고 확인 쿼리를 수행할 때 `FOR SHARE` 또는 **Next-Key Lock**이 활성화된 격리 수준을 사용하여, 입고(INSERT)가 일시적으로 차단되도록 설정해야 한다.

**시나리오 2: 통계 리포트 생성 (Batch Reporting)**
- **문제**: 일일 매출 집계 중에 새로운 주문이 계속 들어와서 숫자가 계속 바뀜.
- **해결**: 분석 쿼리는 `READ COMMITTED` 수준으로 실행하여, 집계 도중 락으로 인한 트랜잭션 처리 지연(Latency)을 최소화하는 전략이 유효할 수 있음. **"집계 시점의 스냅샷"**만 중요하므로, 유령 읽기가 발생하더라도 성능을 위해 이를 허용하는 엔지니어