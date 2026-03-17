+++
title = "230. Repeatable Read (레벨 2) - 일관된 시간의 박제"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 230
+++

# 230. Repeatable Read (레벨 2) - 일관된 시간의 박제
## # [트랜잭션 격리 수준: Repeatable Read]
### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션 내에서 **한 번 조회한 데이터는 트랜잭션이 종료될 때까지 동일한 값이 유지됨을 보장**하는 격리 수준입니다. 즉, 논리적으로 트랜잭션 시작 시점의 데이터베이스 상태(Snapshot)를 '박제'하여 시간의 흐름을 차단합니다.
> 2. **가치**: **Non-Repeatable Read (비반복 읽기)** 현상을 원천적으로 차단하여, 재고 산정, 금융 잔액 확인 등 데이터 일관성이 중요한 비즈니스 로직의 무결성을 보장합니다. 특히 MySQL (InnoDB)의 기본 전략으로, 높은 동시성 처리와 안정성의 균형을 제공합니다.
> 3. **융합**: **MVCC (Multi-Version Concurrency Control)** 기술과 결합하여 Lock(잠금) 기반의 동시성 제어가 주는 성능 저하를 최소화하면서도, 사용자에게는 마치 단독으로 DB를 사용하는 것 같은 **일관된 뷰(View)**를 제공합니다.
+++

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
**Repeatable Read (RR, 반복 가능한 읽기)**는 트랜잭션 격리 수준(Transaction Isolation Level) 중 세 번째 단계로, ISO/ANSI SQL 표준에서 정의된 격리 수준입니다. 이 수준은 하나의 트랜잭션 내에서 동일한 **SELECT (Read)** 쿼리를 여러 번 수행할 경우, 항상 처음 읽었던 데이터와 동일한 결과 집합(Result Set)을 반환함을 보장합니다. 이는 다른 트랜잭션이 데이터를 **Commit (커밋)** 하더라도 영향을 받지 않는다는 것을 의미하며, 트랜잭션의 **Read Consistency (읽기 일관성)**를 트랜잭션 생명 주기 전체로 확장하는 개념입니다.

**2. 💡 비유**
한 학생이 도서관에서 책을 빌려 정해진 시간 동안만 보는 것과 같습니다. 다른 학생(다른 트랜잭션)이 그 책의 내용을 수정하고 반납(Commit)하더라도, 나는 빌렸을 때의 원본 내용을 끝까지 볼 수 있습니다.

**3. 등장 배경 및 기술적 철학**
데이터베이스 초기에는 **Lock-based Concurrency Control (잠금 기반 동시성 제어)**가 주를 이루었습니다. 이는 데이터를 읽을 때마다 **Shared Lock (공유 잠금)**을 걸어 다른 트랜잭션의 수정을 물리적으로 막는 방식입니다. 하지만 이는 동시성이 급격히 떨어지는 병목 현상을 야기했습니다.
이를 해결하기 위해 **MVCC (Multi-Version Concurrency Control)**라는 패러다임이 등장했습니다. Repeatable Read는 이 패러다임 위에서 구현됩니다. 데이터를 수정할 때 즉시 덮어쓰는 것이 아니라, 새로운 버전을 생성하고, 읽는 트랜잭션은 자신이 시작된 시점에 맞는 적절한 과거 버전(Undo Log를 통해)을 바라보도록 함으로써, '잠금' 없이도 '일관성'을 확보하는 혁신적인 접근 방식입니다.

**📢 섹션 요약 비유**: Repeatable Read는 **'단체 사진 촬영 시간'**과 같습니다. 사진 촬영(트랜잭션 시작)이 끝난 후, 찍힌 사람들(데이터)이 자리에서 일어나고 다른 사람들이 들어오더라도(변경 및 커밋), 사진 속의 장면(스냅샷)은 변하지 않습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 동원 기술**

| 요소명 | 역할 | 내부 동작 | 프로토콜/메커니즘 | 비유 |
|:---|:---|:---|:---|:---|
| **MVCC (Multi-Version Concurrency Control)** | 다중 버전 관리 | 데이터 변경 시 새 버전 생성, 이전 버전을 Undo Segment에 보존 | Row-level Versioning | 수정하기 전 원본 복사본 보관 |
| **Undo Log** | 과거 데이터 복원 | 트랜잭션 롤백을 위한 Before Image 저장 및 Read Consistency 제공 | Rollback Segment | 시간을 돌리는 타임머신 |
| **Read View** | 스냅샷 정의 | 트랜잭션 시작 시점의 활성 트랜잭션 리스트(ID)를 스냅샷으로 보유 | Visibility Check (m_ids, min_trx_id) | 유효 기간이 적힌 입장권 |
| **Transaction ID (TRX_ID)** | 순서 번호 | 데이터 행마다 수정을 가한 트랜잭션의 ID를 기록 | Monotonic Increment | 도장 찍는 번호표 |
| **Next-Key Lock** | 갭 및 레코드 락 | Phantom Read를 방지하기 위해 레코드와 그 앞의 갭(Gap)을 함께 잠금 | Record Lock + Gap Lock | 빈 의자까지 예약해두기 |

**2. ASCII 구조 다이어그램: MVCC 기반 Read View 생성 및 확인 흐름**

아래 다이어그램은 MySQL(InnoDB)에서 트랜잭션이 데이터를 읽을 때, 자신의 **Read View(읽기 뷰)**와 데이터 행의 **TRX_ID**를 비교하여 가시성을 판단하는 메커니즘을 도식화한 것입니다.

```text
[MVCC Visibility Check Algorithm]

┌─────────────────────────────────────────────────────────────┐
│  🔍 Transaction T1 (SELECT Query)                          │
│  ┌─────────────────────┐                                    │
│  │ Read View (RV 100)  │ ──▶ Min: 100 / Max: 105          │
│  │ Active IDs: {101}   │                                   │
│  └─────────────────────┘                                    │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
          ┌───────────────────────────────────────┐
          │       Data Page on Disk               │
          └───────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │   Row A  │        │   Row B  │        │   Row C  │
   │ TRX_ID:  │        │ TRX_ID:  │        │ TRX_ID:  │
   │   99     │        │   102    │        │   50     │
   └────┬─────┘        └────┬─────┘        └────┬─────┘
        │                  │                  │
        │ 1. Is ID < Min?  │ 2. Is ID in     │ 3. Is ID < Min?
        │    (99 < 100)    │    Active Set?   │    (50 < 100)
        │                  │    (102 in {101})│
        ▼                  ▼                  ▼
   ✅ VISIBLE          ❌ INVISIBLE         ✅ VISIBLE
   (Old Version)      (From Future)       (Old Version)
        │                  │                  │
        │                  ▼                  │
        │          ┌──────────────┐           │
        │          │ Access Undo │           │
        │          │ Log (Prev)  │           │
        │          └──────────────┘           │
        └───────────┬──────────────────────────┘
                    ▼
          Return to User (Consistent Snapshot)
```

**다이어그램 해설**:
1.  **Read View 생성**: 트랜잭션 T1이 시작되면 현재 활성화된 트랜잭션 ID 리스트를 기반으로 Read View를 생성합니다. (Min: 가장 빠른 활성 ID, Max: 시스템이 할당할 다음 ID)
2.  **TRX_ID 비교**: 데이터 행(Row)을 조회할 때, 행 헤더에 있는 `TRX_ID`를 Read View와 비교합니다.
    *   **Case A (TRX_ID=99)**: T1 시작 이전에 커밋된 데이터이므로 그대로 반환합니다.
    *   **Case B (TRX_ID=102)**: T1이 시작된 이후에 커밋된 데이터(미래의 데이터)이므로 사용자에게 보여주면 안 됩니다. `Undo Log`를 타고 거슬러 올라가 T1 입장에서 유효한 과거 버전을 찾습니다.
    *   **Case C (TRX_ID=50)**: 오래된 데이터이므로 그대로 반환합니다.

**3. 심층 동작 원리: Non-Repeatable Read 방지 메커니즘**

Repeatable Read가 **Non-Repeatable Read (반복 불가능한 읽기)**를 방지하는 과정은 다음과 같습니다.

1.  **최초 조회 (First Read)**:
    *   `SELECT * FROM User WHERE id = 1;` 실행.
    *   이때 현재 시점의 `Read View`를 생성하고, 이를 트랜잭션 내부에 캐싱(Caching)합니다.
    *   데이터 반환.
2.  **외부 수정 (External Update)**:
    *   다른 트랜잭션(T2)이 해당 `id=1`인 데이터를 수정하고 **Commit**을 수행합니다.
    *   T2는 데이터베이스 파일에는 새 버전(최신 데이터)을 기록하지만, T1의 세션에는 영향을 주지 않습니다.
3.  **재 조회 (Second Read)**:
    *   T1이 다시 `SELECT * FROM User WHERE id = 1;` 실행.
    *   **핵심**: T1은 새로운 Read View를 생성하지 않고, **시작 시점에 생성했던 캐싱된 Read View**를 재사용합니다.
    *   따라서 T2가 커밋한 최신 데이터는 T1의 Read View 입장에서 '미래의 데이터'로 판단되어 무시되고, Undo Log를 통해 과거의 원본 데이터가 다시 조회됩니다.

**4. 핵심 알고리즘 코드 (Pseudo-SQL)**

```sql
-- MySQL InnoDB Engine (Pseudo Logic)
FUNCTION GetRowVersion(row, current_read_view):
    WHILE row.TRX_ID is not visible to current_read_view:
        -- 현재 행의 TRX_ID가 Read View의 활성 리스트에 있거나(Max보다 크면)
        -- 혹은 Read View의 Min보다 작지 않으면(시작 전이 아니면)
        
        IF row.TRX_ID == current_read_view.creator_id:
            -- 내가 수정한 행이면 보임
            RETURN row;
        ELSE:
            -- Undo Log를 따라가서 이전 버전을 가져옴
            row = roll_pointer.undo_log_segment;
    END WHILE
    RETURN row;
```

**📢 섹션 요약 비유**: Repeatable Read의 데이터 관리는 **'박물관 유물 전시'**와 같습니다. 관람객(트랜잭션)이 입장하는 순간 찍힌 사진(Read View)을 가지고 있어, 전시 도중에 관리자가 유물을 다른 것으로 교체해도(Update Commit), 관람객은 여전히 가이드북(스냅샷)에 있는 원래 모습을 계속 보게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: Read Committed vs. Repeatable Read**

| 비교 항목 | Read Committed (RC, 레벨 1) | Repeatable Read (RR, 레벨 2) |
|:---|:---|:---|
| **정의** | 커밋된 데이터만 읽기 | 트랜잭션 내에서 반복 읽기 보장 |
| **Read View** | **매 쿼리마다 새로 생성** | **트랜잭션 시작 시 1회만 생성** |
| **Non-Repeatable Read** | 발생 가능 ❌ | 방지됨 ✅ |
| **Phantom Read** | 발생 가능 ❌ | 이론적 가능성 ⚠️ (InnoDB는 방어) |
| **Locking 방식** | 수정된 행에만 Lock | 범위(Next-Key) Lock 사용 |
| **Undo Log 부하** | 적음 (과거 버전 빠른 정리) | 많음 (긴 트랜잭션 시 Undo 급증) |
| **주요 사용처** | 웹 서비스, 최신 데이터 반映 중시 | 금융 결제, 재고, 통계(일관성 중시) |

**2. 과목 융합 관점**
*   **운영체제(OS)와의 시너지**: 데이터베이스의 Undo Log는 운영체제의 **Virtual Memory (가상 메모리)** 관리 기법인 **Copy-on-Write (COW)**와 유사합니다. 쓰기 시점에 실제 데이터를 복사하여 원본을 보존하는 방식은 메모리 관리와 트랜잭션 관리 모두에서 '일관성'과 '회복'을 위한 핵심 전략입니다.
*   **네트워크와의 시너지**: 네트워크의 **TCP (Transmission Control Protocol)** 흐름 제어와 유사하게, 트랜잭션은 자신의 '버퍼(RC)'를 넘어선 데이터를 수용하지 않음으로써 논리적 흐름을 깨지 않게 보호합니다.

**3. Phantom Read (팬텀 리드)와 Next-Key Lock**
ISO 표준에서는 Repeatable Read가 Phantom Read를 방지하지 못한다고 하지만, 실무 표준인 **MySQL InnoDB**는 **Next-Key Lock**을 사용하여 이를 방지합니다.

*   **Phantom Read**: 첫 번째 쿼리에서 없던 행이 두 번째 쿼리에서 생겨나는 현상입니다.
*   **Next-Key Lock**: 단순히 레코드만 잠그는 것이 아니라, **Index Record Lock + Gap Lock**을 결합하여 인덱스 레코드와 그 바로 앞의 갭(Gap, 빈 공간)을 함께 잠급니다. 이로써 다른 트랜잭션이 새로운 행을 삽입하는 것을 물리적으로 차단합니다.

**📢 섹션 요약 비유**: Read Committed는 **'실시간 뉴스'**와 같아서 화면이 바뀌면 내용도 즉시 바뀌지만, Repeatable Read는 **'녹화된 방송'**과 같습니다. 중간에 광고가 편집되거나 수정되더라도(외부 커밋), 방송을 처음부터 끝까지 본 시청자에게는 원래 내용 그대로만 보입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 과정**

*   **시나리오 A: 금융 송금 시스템**
    *   **상황**: A 계좌에서 B 계좌로 100만 원 이체. 잔액 조회 1차, 이체 실행, 잔액 조회 2차.
    *   **문제**: Read Committed 레벨에서는 조회 1과 2 사이에 다른 트랜잭션이 끼어들어 잔액을 변조할 수