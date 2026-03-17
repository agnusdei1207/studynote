+++
title = "215. 배타 락 (Exclusive Lock / Write Lock, X-Lock)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 215
+++

# 215. 배타 락 (Exclusive Lock / Write Lock, X-Lock)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 배타 락(Exclusive Lock, X-Lock)은 트랜잭션(Transaction)이 데이터를 갱신할 때, **다른 모든 트랜잭션의 읽기(Shared Lock) 및 쓰기 접근을 물리적으로 차단**하여 데이터의 독점적 사용권을 보장하는 가장 강력한 잠금 메커니즘이다.
> 2. **가치**: 동시성 제어(Concurrency Control)의 핵심 수단으로, **갱신 손실(Lost Update)**, 모순된 비판독(Inconsistent Retrieval), 더티 읽기(Dirty Read) 등의 이상 현상을 원천 봉쇄하여 DBMS의 **ACID(Isolation, Atomicity)** 속성을 엄격하게 준수하게 한다.
> 3. **융합**: 2단계 락킹(2PL, Two-Phase Locking) 프로토콜의 성장 단계(Growing Phase)에서 핵심적인 역할을 수행하며, 격리 수준(Isolation Level) 설정에 따라 전체 시스템의 **처리량(Throughput)**과 **지연 시간(Latency)**의 트레이드오프를 결정하는 결정적 요소이다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**배타 락(Exclusive Lock, X-Lock)** 또는 **쓰기 락(Write Lock)**은 DBMS의 잠금 관리자(Lock Manager)가 제공하는 잠금 모드 중 하나로, 특정 트랜잭션이 데이터 레코드(Record)나 페이지(Page)를 **수정(Write)** 하려고 할 때, 해당 데이터에 대해 다른 트랜잭션의 어떠한 접근도 허용하지 않는 **독점적 상태**를 만드는 메커니즘이다.
이는 **공유 락(Shared Lock, S-Lock)**과 대조되는 개념으로, S-Lock이 '읽기 전용'으로 여러 트랜잭션이 동시에 접근 가능함에 비해, X-Lock은 **무조건 단일 트랜잭션에 의해서만 획득**되어야 한다는 상호 배제(Mutual Exclusion) 원칙을 철저히 따른다.

#### 2. 💡 비유: 화장실 변기의 잠금
공중화장실의 변기를 생각하면 이해가 쉽다. 변기 문을 잠그지 않으면(S-Lock 상태), 밖에서 문을 열어볼 수도 있고 사용하려는 사람도 들어올 수 있다. 하지만 문을 안에서 잠그면(X-Lock 상태), 밖에서는 아무리 급해도 문을 열 수 없을 뿐만 아니라, 안에 무슨 일이 일어나는지 볼 수도 없다. 사용자가 나가고 잠금을 해제(Unlock)하기 전까지는 다른 사람의 접근이 차단되는 원리이다.

#### 3. 등장 배경 및 필요성
① **데이터 무결성 침해**: 데이터베이스 초기 환경에서는 동시성 제어가 없어, 두 개의 트랜잭션이 동시에 같은 데이터를 수정하면 '나중에 수정한 값'만 남거나(갱신 손실), 데이터가 섞이는 문제가 발생했다.
② **잠금(Locking)의 도입**: 이를 해결하기 위해 데이터에 '자물쇠'를 채우는 개념이 도입되었다. 특히 쓰기 연산은 데이터 자체를 변경하므로, 읽기보다 훨씬 강력한 통제가 필요했다.
③ **비즈니스 요구**: 금융권(잔액 수정), 재고 관리(재고 차감) 등 0.001%의 오류도 허용되지 않는 현대의 트랜잭션 처리 환경에서 **X-Lock은 데이터 정합성을 보장하는 최후의 보루**로 자리 잡았다.

#### 4. 📢 섹션 요약 비유
배타 락은 **'계약서 작성 중인 서랍'**과 같습니다. 어떤 직원이 계약서를 수정하기 위해 서랍을 열고 문을 잠그면, 다른 직원들은 그 내용을 확인하려 해도 서랍이 열리지 않고(읽기 불가), 자신이 수정하려 해도 문이 열리지 않습니다(쓰기 불가). 작성을 마치고 열쇠를 반납해야 비로소 다른 사람이 서랍을 이용할 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 배타 락의 상세 모듈 및 동작
배타 락은 단순히 "잠금"이라는 상태 비트(Bit) 하나로 동작하지 않는다. **잠금 관리자(Lock Manager)**는 메모리 상의 **잠금 테이블(Lock Table)**을 통해 다음과 같은 정보를 관리한다.

| 요소명 | 역할 | 내부 동작 | 프로토콜/상태 | 비유 |
|:---|:---|:---|:---|:---|
| **Lock Table (해시 테이블)** | 잠금 정보 저장소 | 현재 어떤 트랜잭션이 어떤 객체(Object ID)에 락을 걸었는지 저장 | Key: Data ID, Value: Lock List | 경비실의 출입자 대장 |
| **Lock Request Queue** | 대기열 관리 | X-Lock을 획득하지 못한 요청을 FIFO(선입선출) 방식으로 대기시킴 | `Blocked` 상태로 전이 | 줄 서 있는 대기 인원 |
| **Transaction ID (TX_ID)** | 트랜잭션 식별자 | 락을 요청한 주체를 식별 (프로세스 ID와 매핑) | Global Unique ID | 직원 사번 |
| **Lock Mode** | 잠금 모드 | S-Lock(읽기)과 X-Lock(쓰기)을 구분하여 호환성(Compatibility) 판단 | `IS`, `IX`, `S`, `X` | 읽기용/쓰기용 구분 |
| **Wait-For Graph** | 교착 상태 감지 | 트랜잭션 간의 대기 그래프를 형성하여 사이클(Cycle) 발생 시 교착 상태(Deadlock)로 판단 | 주기적 감지 (Deadlock Detector) | 누가 누구를 기리는지 지도 |

#### 2. ASCII 구조 다이어그램: 잠금 관리자(Lock Manager)의 내부 구조
아래는 트랜잭션이 `UPDATE` 문을 실행했을 때, 잠금 관리자가 X-Lock을 처리하는 과정이다.

```text
[Lock Manager Architecture & X-Lock Flow]

Transaction(T1)           Lock Manager                 Data Store
    |                           |                            |
    | --- (1) UPDATE Request    |                            |
    |       (Target: Row_A)     |                            |
    |                           |                            |
    |           (2) Lookup Lock Table                     (3) Check Page Lock
    |           ────────────────────────────────────────────────> 
    |                           |                            |
    |           (4) Is Locked? (Check Lock Table)              |
    |           [Key: Row_A]                                 |
    |           - List: Empty?                                |
    |                           |                            |
    | <─── (5) GRANTED (X-Lock) ─┘                            |
    |                           |                            |
    | --- (6) Write Data ------>                            |
    |                           |                            |
    |                           |                            |
    v                           v                            v
[State: Row_A is owned by T1]


Wait-For Graph (내부 메모리 구조)
[T1] --holds--> [Row_A: X-Lock]

[Competitor Flow]
If T2 requests S-Lock on Row_A:
[T2] --waits for--> [T1] (Blocked in Queue)
```

**(다이어그램 해설)**
1.  **트랜잭션 요청**: `T1`이 데이터 갱신을 위해 `Row_A`에 대한 X-Lock을 요청한다.
2.  **잠금 테이블 조회**: LM은 `Row_A`의 키를 해싱(Hashing)하여 현재 다른 트랜잭션이 락을 걸었는지 확인한다.
3.  **호환성 확인**: 현재 `Row_A`에 락이 없거나, 있어도 `T1` 자신이 이미 S-Lock을 가지고 있어 **Upgrade(상향)**가 가능한 경우에만 X-Lock을 부여한다.
4.  **독점 점유**: X-Lock이 부여되면, 향후 들어오는 `T2`의 S-Lock(읽기) 요청은 호환성 불가(Compatibility Matrix상 `X`는 `S`와 배타적)로 인해 대기열(Queue)에 묶인다.
5.  **데이터 수정**: 트랜잭션은 이후 실제 데이터 버퍼에 변경사항을 기록한다.

#### 3. 락 호환성 매트릭스 (Lock Compatibility Matrix)
X-Lock의 핵심은 비호환성(Non-compatibility)에 있다. 아래는 표준적인 락 호환성 규칙이다.

| Request \ Current | **S (Shared)** | **X (Exclusive)** |
|:---:|:---:|:---:|
| **S (Shared)** | ✅ **Compatible** (동시 읽기 가능) | ❌ **Conflict** (대기 필요) |
| **X (Exclusive)** | ❌ **Conflict** (대기 필요) | ❌ **Conflict** (대기 필요) |

*   **핵심 코드 로직 (Pseudo-code)**
    ```sql
    -- 락 매니저의 핵심 로직 예시
    FUNCTION request_lock(transaction, resource, mode):
        current_lock = get_lock(resource)
        
        IF current_lock IS NULL:
            GRANT(transaction, resource, mode)
        ELSE IF is_compatible(current_lock.mode, mode):
             -- 같은 트랜잭션이면 유지, 다른 트랜잭션이면 S끼리만 허용
            GRANT(transaction, resource, mode)
        ELSE:
             -- X-Lock은 여기서 다 막힘 (Block)
            WAIT(transaction, resource, mode)
            CHECK_DEADLOCK()
    ```

#### 4. 📢 섹션 요약 비유
배타 락의 동작은 **'미술관의 유일한 복사 테이블'**과 같습니다. 많은 사람이 그림을 감상할 수는 있지만(S-Lock), 누군가 그림을 수정하거나 훼손하려면(X-Lock) 반드시 전시장을 폐쇄하고 자신 혼자만 입장해야 합니다. 폐쇄 기간 동안 감상객들은 문 앞에서 대기해야 하며, 수정 작업이 끝나고 전시장이 재개되어야만 다시 감상이 가능해집니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. S-Lock과 X-Lock의 심층 기술 비교

| 비교 항목 | 공유 락 (Shared Lock, S-Lock) | 배타 락 (Exclusive Lock, X-Lock) |
|:---|:---|:---|
| **목적** | 데이터 안정적 읽기 (Repeatable Read) | 데이터 수정 및 독점적 갱신 |
| **동시성 정도** | 높음 (High Concurrency) <br> 여러 트랜잭션이 동시에 보유 가능 | 낮음 (Low Concurrency) <br> 단 하나의 트랜잭션만 보유 |
| **호환성** | S와 S는 호환, X와는 비호환 | 모든 락(S, X)과 비호완 |
| **성능 영향** | 읽기 성능 유지 (단, 갱신 시 대기 발생 가능) | **쓰기 병목(Bottleneck)의 주범** |
| **리소스 낭비** | 낮음 (CPU, Memory 버퍼 공유) | 높음 (다른 트랜잭션을 Block 시킴) |

#### 2. 타 과목 융합 분석
*   **운영체제(OS)와의 시너지**: DB의 X-Lock은 OS 커널의 **뮤텍스(Mutex)** 또는 **쓰기 시매틱(Writer Semaphore)**와 개념적으로 동일하다. 단, OS 레벨은 프로세스/스레드간 자원 경쟁을 다루고, DB는 논리적 튜플(Tuple)간 경쟁을 다룬다는 차이가 있으나, **Critical Section(임계 영역)** 보호 원칙은 동일하다.
*   **네트워크와의 연관**: 분산 DB 환경(Distributed DB)에서 X-Lock은 **2단계 커밋(2PC, Two-Phase Commit)** 프로토콜과 연동된다. 노드 A의 X-Lock 해제 시점이 노드 B의 준비(Prepare) 단계와 맞물리지 않으면 **분산 불일치(Distributed Inconsistency)**가 발생할 수 있어, 네트워크 지연 시 락 유지 시간이 길어지면 전체 트랜잭션 타임아웃(Transaction Timeout)으로 이어질 위험이 크다.

#### 3. 격리 수준(Isolation Level)별 X-Lock 동작
*   **Read Uncommitted**: X-Lock 중이더라도 다른 트랜잭션이 **Dirty Read**(커밋되지 않은 데이터 읽기)가 가능하다. (성능 최우선, 정합성 최악)
*   **Read Committed**: X-Lock이 걸려 있으면, 커밋 전까지 다른 트랜잭션이 데이터를 읽을 수 없다. (가장 널리 사용됨)
*   **Repeatable Read / Serializable**: 범위 잠금(Gap Lock, Next-Key)과 결합하여 X-Lock의 범위를 넓혀 팬텀 리드(Phantom Read)까지 방지한다. (정합성 최우선, 병목 발생 가능성 높음)

#### 4. 📢 섹션 요약 비유
공유 락(S-Lock)과 배타 락(X-Lock)의 관계는 **'도서관의 열람실'**과 같습니다. 열람실(S-Lock)은 수십 명이 함께 들어가서 조용히 책을 읽을 수 있습니다. 하지만 도서관 직원이 책 수리나 장비 교체를 위해 공간을 폐쇄하는 것(X-Lock)이 발생하면, 모든 독자는 밖으로 나와야 하고 직원의 작업이 끝날 때까지 아무도 입장할 수 없습니다. **"읽기(Shared)는 함께, 쓰기(Exclusive)는 혼자"**가 규칙입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스

**시나리오 A: 대규모 재고 차감 이벤트 (SaaS 커머스)**
*   **상황**: 한정판 상품 100개를 10,000명이 동시에 구매하려 함.
*   **문제**: `SELECT FOR UPDATE`(X-Lock 획득 쿼리)를 행 단위로 걸면, 데이터베이스의 **Latch 경합**과 **Lock Wait**으로 인해 TPS가 급격히 하락한다.
*   **해결 전략**: 
    1.  **DB 락 분할**: 파티셔닝(Partitioning)을 통해 락의 물