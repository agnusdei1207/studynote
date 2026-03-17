+++
title = "227. 트랜잭션 고립화 수준 (Isolation Level) - 정합성과 성능의 저울질"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 227
+++

# 227. 트랜잭션 고립화 수준 (Isolation Level) - 정합성과 성능의 저울질
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션 고립화 수준(Isolation Level)은 동시성 제어(Concurrency Control)의 핵심 메커니즘으로, **ACID(Isolation) 특성**을 구현하기 위해 다중 트랜잭션 간의 데이터 가시성(Visibility)과 잠금(Locking) 범위를 조절하는 데이터베이스의 설계 기준이다.
> 2. **가치**: 비즈니스 요구사항에 따라 **Dirty Read(더티 읽기), Non-Repeatable Read(반복 불가능 읽기), Phantom Read(팬텀 읽기)** 등의 이상 현상(Anomaly) 발생 가능성과 처리 처리량(Throughput) 사이의 정량적 트레이드오프(Trade-off)를 제어하여 시스템의 무결성과 성능을 동시에 확보한다.
> 3. **융합**: 단순한 DB 설정을 넘어 **Lock-Based Protocol(잠금 기반 프로토콜)**과 **MVCC(Multi-Version Concurrency Control, 다중 버전 동시성 제어)** 방식의 동작 방식을 결정짓는 핵심 아키텍처 요소이며, 분산 처리 및 OS의 세마포어(Semaphore) 개념과도 깊이 연결된다.
+++

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 철학**
**트랜잭션 고립화 수준 (Isolation Level)**은 **DBMS (Database Management System, 데이터베이스 관리 시스템)** 에서 동시에 실행되는 트랜잭션들이 서로 간섭하지 않도록 격리하는 정도를 정의한 것이다. **ACID** 특성 중 'I(Isolation, 격리성)'를 구현하는 구체적인 수단으로, 하나의 트랜잭션이 다른 트랜잭션의 중간 단계 데이터를 볼 수 있게 할 것인가, 아니면 완벽하게 숨길 것인가를 결정한다.

**💡 비유: 은행 창구의 업무 처리**
은행 창구에서 고객이 입금을 완료하기 전까진 다른 직원에게 그 내역이 보이지 않아야 한다. 하지만 조회만 하는 창구에서는 인생입금 중인 금액이라도 대략적으로나마 보여줘야 대기 시간을 줄일 수 있다. 이 '얼마나 엄격하게 숨길 것인가'가 바로 격리 수준이다.

**등장 배경**
① **기존 한계**: 단순한 **Locking (잠금)** 만으로는 동시성 이상 현상을 모두 차단할 경우, 시스템의 처리량(Throughput)이 급격히 저하되는 병목 현상 발생.
② **혁신적 패러다임**: 모든 트랜잭션을 직렬(Serial)로 처리하지 않고, 허용 가능한 수준의 데이터 정합성 손실을 감수하면서 병렬 처리를 극대화하는 계층화된 접근 방식(ANSI/ISO SQL 표준) 도입.
③ **현재의 비즈니스 요구**: 초대형 트래픽 처리를 위해 실제로는 데이터가 조금 늦게 보이더라도(Propogation Delay), 읽기 성능을 최우선으로 하는 **Eventual Consistency (결과적 일관성)** 모델과의 타협점이 필요해짐.

```text
[동시성 vs 정합성의 스펙트럼]

       ▲ 정합성 (Data Correctness)
       │
       │ [Serializable]      ────  완벽한 무결성 (Lock Overhead 극대화)
       │   Level 3
       │
       │ [Repeatable Read]   ────  행 단위 잠금/스냅샷 (MySQL Default)
       │   Level 2
       │
       │ [Read Committed]    ────  문장 단위 스냅샷 (Oracle Default)
       │   Level 1
       │
       │ [Read Uncommitted]  ────  최소한의 잠금 (성능 극대화)
       │   Level 0
       │
       └──────────────────────────────▶ 성능 (Performance/Throughput)
```

**📢 섹션 요약 비유**
> 격리 수준 조정은 마치 **'고속도로의 안전거리'**를 설정하는 것과 같습니다. 안전거리를 넓히면(Level 3) 추돌 사고(데이터 오류)는 없어지지만 도로 혼잡(성능 저하)이 심해지고, 안전거리를 좁히면(Level 0) 차들이 꽉꽉 채워 달릴 수 있지만 미세한 속도 차이로도 사고가 나기 쉽습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**구성 요소 (표)**
격리 수준은 단순한 설정값이 아니라 내부적인 다음과 같은 요소들의 복합적인 작용 결과다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 관련 프로토콜/명령어 | 비유 |
|:---|:---|:---|:---|:---|
| **S-Lock** | 데이터 읽기 잠금 | 공유 잠금. 다른 트랜잭션도 읽기는 가능하지만 쓰기는 불가능 (`LOCK IN SHARE MODE`) | `SELECT ... FOR SHARE` | 책을 서로 함께 읽는 행위 |
| **X-Lock** | 데이터 쓰기 잠금 | 베타적 잠금. 다른 트랜잭션의 읽기/쓰기 모두 차단 (`FOR UPDATE`) | `SELECT ... FOR UPDATE` | 책에 필기하는 중엔 다른 사람 못 보게 함 |
| **MVCC** | 비관적 잠금 해결 | 데이터 변경 시 새 버전(Undo Log) 생성. 읽기는 과거 버전 참조. | Row-level Hidden Column | 약속 번호표 배부 시스템 |
| **Gap Lock** | Phantom Read 방지 | 인덱스의 간격(Gap) 자체를 잠금. 새로운 레코드 삽입 방지. | Next-Key Lock | 빈 의자에 앉지 못하게 미리 막음 |
| **Predicate Lock** | 범위 쿼리 잠금 | `WHERE` 조건을 만족하는 범위 자체에 잠금을 검. (Serializable 주요) | Range Lock | 구역 전체를 통째로 봉쇄 |

**ASCII 구조 다이어그램: Locking vs MVCC**

```text
[격리 수준 구현 기술의 발전]

1. 낮은 수준 (Read Uncommitted)
   ────────────────────────────────────────
   Tx A: [          UPDATE (X-Lock)        ]
   Tx B:         [ SELECT (No Lock) ✅ Dirty Read ]


2. 높은 수준 (Serializable, Traditional)
   ────────────────────────────────────────
   Tx A: [ S-Lock ] [ Wait ] [ S-Lock ]
   Tx B:    [ S-Lock ]
   (Wait: B가 A를 기다림 = 병목 발생)

   
3. 현대적 수준 (Repeatable Read + MVCC)
   ────────────────────────────────────────
   Storage Engine: [ Current Ver: 100 ] [ Undo Log: 99, 98... ]
   
   Tx A (Old Snapshot): [ SELECT -> Read Ver 99 ] ──┐
                                                   │ (Non-blocking)
   Tx B (New Write):  [ UPDATE -> Write Ver 100 ] ─┘
```

**심층 동작 원리**
1. **데이터 접근 요청**: 트랜잭션이 `SELECT` 혹은 `UPDATE`를 요청한다.
2. **잠금 매니저(Lock Manager) 확인**: 해당 레코드 혹은 범위에 **S-Lock / X-Lock**이 걸려 있는지 확인한다.
   - 만약 **MVCC** 방식(InnoDB 등)이라면, 읽기 작업은 잠금을 대기하지 않고 **Undo Segment**에 저장된 과거 스냅샷을 즉시 반환한다.
3. **버전 체인(Version Chain) 순회**: 요청한 시점(Transaction ID)보다 이전의 커밋된 데이터를 찾을 때까지 메모리 내의 체인을 따라간다.
4. **폴백(Fallback) 처리**: 만약 충돌하는 쓰기 잠금이 존재하고, 격리 수준이 높다면(Lock-based), 트랜잭션은 대기(Block)하거나 롤백(Rollback)된다.

**핵심 알고리즘 및 예시 (Python-style Pseudo-code)**
높은 격리 수준에서의 체크 로직을 단순화하면 다음과 같다.

```python
# [의사코드] Repeatable Read Validation
def validate_transaction(tx, current_db_state):
    for read_item in tx.read_set:
        # 1. 읽었던 데이터가 변경되었는가?
        if read_item.version != tx.snapshot_version:
            raise RollbackError("Non-Repeatable Read detected")
            
    for write_item in tx.write_set:
        # 2. 쓰려는 데이터가 다른 트랜잭션에 의해 변경되었는가? (Check Write Skew)
        if write_item.is_locked_by_other(tx):
            raise SerializationFailureError("Conflict detected")
            
    # 3. 팬텀 체크 (Index Scan)
    if tx.index_range.has_new_insertion():
        raise PhantomReadError()
        
    commit(tx)
```

**📢 섹션 요약 비유**
> 고립화 수준의 아키텍처는 **'사진 촬영 모드'**와 같습니다. 
> - **Read Uncommitted**는 누르자마자 찍히는 live 화면이다 보니 배경이 엉망이지만 빠릅니다. 
> - **MVCC**는 촬영 당시의 이미지를 스마트폰 버퍼(Snapshot)에 저장해두기 때문에, 촬영 후 배경이 변해도 내 사진(트랜잭션)은 변하지 않습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

**격리 수준별 이상 현상 (Anomaly) 허용 범위 분석표**

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read | 주요 구현 기술 | 성능 영향도 |
|:---|:---:|:---:|:---:|:---|:---:|
| **Read Uncommitted** | ⚠️ 발생 | ⚠️ 발생 | ⚠️ 발생 | 무조건 읽기 | **최고** (Lock X) |
| **Read Committed (RC)** | ✅ 방지 | ⚠️ 발생 | ⚠️ 발생 | MVCC Snapshot (Stmt) | **높음** |
| **Repeatable Read (RR)** | ✅ 방지 | ✅ 방지 | ⚠️ 발생 (Lock 한정)<br>✅ 방지 (MVCC 한정) | MVCC Snapshot (Tx), Gap Lock | **중간** |
| **Serializable** | ✅ 방지 | ✅ 방지 | ✅ 방지 | Range Lock, Strict 2PL | **낮음** (Lock O) |

*참고: MySQL(InnoDB)의 RR 수준에서는 Gap Lock을 통해 Phantom Read를 방지하지만, 이론적인 정의와는 차이가 있을 수 있음.*

**OS/소프트웨어 공학적 융합 분석**

1. **OS와의 관계 (Synchronization Primitives)**
   - 트랜잭션의 격리 수준은 OS 커널의 **Mutex (Mutual Exclusion)**, **Semaphore**, **Monitor** 개념과 직결된다.
   - **Read Committed**는 OS의 `Readers-Writers Lock`에서 읽기 선호(Read-Preferring) 정책과 유사하여, 다중 스레드가 자원을 동시에 읽을 수 있게 허용하여 처리량을 높인다.
   - **Serializable**은 모든 작업을 Critical Section(임계 영역)으로 간주하여, OS 레벨의 `context switching` 오버헤드가 DB 서버 전체에 발생하는 것과 같은 효과를 낸다.

2. **분산 시스템과의 관계 (CAP Theorem)**
   - 격리 수준은 **CAP 이론**(Consistency, Availability, Partition Tolerance)의 **Consistency(일관성)** 강도와 비례한다.
   - 높은 격리 수준(Serializable)은 분산 환경에서 Parition 발생 시 Availability(가용성)를 포기하고 데이터 일치를 택하는(Prefer C over A) 설계로 이어진다.

```text
[비교 시각화: 잠금의 범위 (Scope)]

Level 0 (RU):    [ row ]
                 ↑ (Lock 없음, 그냥 읽음)

Level 1 (RC):    [ row ] [ row ]
                 ↑ (읽는 순간의 Commit된 데이터만 반환)

Level 2 (RR):    [ row ] [ row ] [ row ]
                 ↑ (트랜잭션 시작 시점 전체를 고정 Snapshot)

Level 3 (Ser):   [ Gap ] [ row ] [ row ] [ Gap ]
                 ↑ (범위 자체를 잠금, Insert 방지)
```

**📢 섹션 요약 비유**
> 격리 수준 비교는 **'도서관의 열람실 규칙'**과 같습니다. 
> - **RU**는 누구나 들어와서 책을 마음대로 넘겨볼 수 있습니다. 
> - **RC**는 책이 비치(Commit)되었을 때만 볼 수 있습니다. 
> - **Serializable**은 책 한 꺼번에 한 명만 보거나, 책장 전체를 다 쓸 때까지 다른 사람이 접근 못 하게 막는 강력한 독점 규칙입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**실무 시나리오별 의사결정 매트릭스**

1. **금융 핀테크 이체 시스템 (Financial Core)**
   - **상황**: A 계좌에서 B 계죄로 10억 원 이체 시, A의 잔액이 줄어드는 도중에 B 계좌 조회가 일어남.
   - **결정**: **Serializable** 또는 **Repeatable Read** 필수.
   - **이유**: 이중 지급(Double Spending) 방지와 자산 유출 방지가 최우선이므로, 성능 저하를 감수하고서라도 잠금(Lock)을 강화한다. 또한 `FOR UPDATE` 구문을 활용한 명시적 잠금이 필수적이다.

2. **대용량 SNS 뉴스피드 (Social Feed)**
   - **상황**: 사용자가 포스트를 작성 중이고, 다른 사용자가 그 사용자의 프로필을 조회하는 경우.
   - **결정**: **Read Committed** 채택.
   - **이유**: 작성 중인(Commit 전) 포스트는 조회해서는 안 되지만, 이미 반영된 글은 즉시 보여주어야 한다. SR(Repeatable Read)의 경우 조회 성능이 저하되고 Undo Log 부하가 크므로 RC가 가장 효율적이다.

3. **배치 리포트 생성 (Analytics/Batch)**
   - **상황**: 전날의 매출 통계를 새벽에 계산.
   - **결정**: **Read Uncommitted** 고려 (혹은 No-Lock Hint).
   - **이유**: 정확한