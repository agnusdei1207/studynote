+++
title = "226. 블로킹 (Blocking) 현상 완화 - 동시성의 병목 해소"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 226
+++

# 226. 블로킹 (Blocking) 현상 완화 - 동시성의 병목 해소
## # 블로킹 (Blocking) 현상 완화 전략
### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 블로킹(Blocking)은 DBMS의 동시성 제어(Concurrency Control) 메커니즘에서, 선행 트랜잭션이 획득한 락(Lock)으로 인해 후행 트랜잭션이 자원에 접근하지 못하고 대기하는 상태를 의미하며, 성능 저하의 직접적인 원인이 된다.
> 2. **가치**: 블로킹을 최소화하면 TPS (Transactions Per Second)가 획기적으로 향상되며, Latency (응답 지연 시간)을 줄여 사용자 경험을 개선하고 시스템 전체의 처리량(Throughput)을 극대화할 수 있다.
> 3. **융합**: MVCC (Multi-Version Concurrency Control)와 같은 비잠계 읽기(Non-locking Read) 기술이 결합되어 현대의 RDBMS 및 NewSQL에서는 읽기 작업과 쓰기 작업 간의 상호 블로킹을 근본적으로 해결하고 있다.
+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
블로킹(Blocking)은 데이터베이스 관리 시스템(DBMS; Database Management System)에서 트랜잭션의 ACID(Atomicity, Consistency, Isolation, Durability) 속성을 보장하기 위해 락(Lock) 기반의 상호 배제(Mutual Exclusion) 메커니즘을 사용할 때 발생하는 필연적인 현상이다. 특정 트랜잭션이 데이터를 수정하거나 참조하기 위해 락을 획득하면, 해당 자원에 대해 호환되지 않는 락을 요청하는 다른 트랜잭션은 선행 트랜잭션이 커밋(Commit)하거나 롤백(Rollback)하여 락을 해제(Lock Release)할 때까지 실행을 멈추고 대기 큐(Wait Queue)에서 대기하게 된다.

**💡 비유: 식당 화장실의 열쇠**
하나의 화장실(자원)을 사용하기 위해 열쇠(락)가 필요한 상황과 같습니다. A라는 사람이 화장실에 들어가 문을 잠갔다면, B라는 사람은 A가 나올 때까지 문 밖에서 기다려야(Blocking) 합니다. 만약 A가 배가 아파 너무 오랫동안 나오지 않는다면(긴 트랜잭션), 밖에서 기다리는 B, C, D는 모두 지각을 하거나 업무에 지장을 받게 됩니다.

**등장 배경 및 진화**
1.  **기존 한계**: 초기의 DBMS는 Lock-based Protocol에 의존하여, 데이터 일관성을 보장하는 과정에서 동시 처리 성능이 급격히 저하되는 병목 현상이 발생했습니다.
2.  **혁신적 패러다임**: 1980년대 MIT에서 연구된 MVCC (Multi-Version Concurrency Control) 개념이 도입되면서, '읽기(Select)' 작업은 과거의 데이터 버전(Snapshot)을 참조하게 하여 락 대기 없이 수행하는 비차단(Non-blocking) 방식이 등장했습니다.
3.  **현재의 비즈니스 요구**: 초당 수만 건 이상의 트랜잭션이 발생하는 금융 거래나 커머스 시스템에서는 마이크로초(µs) 단위의 락 대기 시간조차 치명적이므로, 블로킹을 최소화하는 튜닝과 아키텍처 설계가 필수적입니다.

**📢 섹션 요약 비유**
블로킹은 **'단일 차로의 다리 위에서 건너지 않는 차'**와 같습니다. 앞차가 멈춰 있으면 뒤에 오는 모든 차량이 일제히 멈추는 선형 의존 구조를 가지므로, 이 다리를 건너는 속도(트랜잭션 처리 속도)가 시스템 전체의 흐름을 결정합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

블로킹 현상을 이해하기 위해서는 DBMS의 Lock Manager가 어떻게 락을 할당하고 충돌을 감지하는지, 그리고 MVCC가 이를 어떻게 우회하는지 이해해야 한다.

#### 1. 구성 요소 (상세 분석)

| 구성 요소 | 역할 | 내부 동작 | 프로토콜/주요 특징 | 비유 |
|:---|:---|:---|:---|:---|
| **Lock Manager** | 락 할당 및 충돌 검증 | 자원 요청이 들어오면 Lock Table(Lock Hash)을 조회하여 호환성 매트릭스(Compatibility Matrix) 확인 | 2PL (Two-Phase Locking) | 교통정리 관제소 |
| **TX (Transaction) Table** | 트랜잭션 상태 관리 | 트랜잭션 ID, 시작 시간, 현재 보유 중인 Lock 목록, Rollback 세그먼트 포인터 관리 | MVCC의 Undo Log 연결 | 운전자 신분증 |
| **Wait Queue (대기 큐)** | 블로킹된 세션 저장 | 락 획득에 실패한 요청을 FIFO(First-In, First-Out) 또는 우선순위 순서로 연결 | Request Queue | 톨게이트 대기줄 |
| **Latch (Mutex)** | 메모리 구조 보호 | Lock Table 자체의 동시 접근을 제어하는 OS 수준의 경량 잠금 | Atomic CAS (Compare-And-Swap) | 관제실 출입문 잠금 |
| **MVCC Undo Log** | 이전 버전 데이터 보관 | 수정 전 데이터 이미지를 저장하여, 읽기 트랜잭션이 과거 시점의 데이터를 조회하도록 제공 | Read Committed / Repeatable Read | 타임머신 비디오테이프 |

#### 2. ASCII 구조 다이어그램: 락 관리자와 블로킹 체인

```text
      [Transaction A]          [Transaction B]          [Transaction C]
            |                         |                         |
      UPDATE Row_1              UPDATE Row_1              SELECT Row_1
            |                         |                         |
            +----> (Request X-Lock)   +----> (Request X-Lock)   +----> (Request S-Lock)
            |                         |                         |
            v                         v                         v
   +------------------------+      +------------------------+      +------------------------+
   |    Lock Manager (LM)   |      |    Lock Manager (LM)   |      |    Lock Manager (LM)   |
   +------------------------+      +------------------------+      +------------------------+
   |  Resource: Row_1       |      |  Resource: Row_1       |      |  Resource: Row_1       |
   |  State: LOCKED (X)     |<-----|  State: LOCKED (X)     |<-----|  State: LOCKED (X)     |
   |  Owner: TX A           |      |  Owner: TX A           |      |  Owner: TX A           |
   |  Wait Q: [TX B, TX C]  |      |  Wait Q: [TX B, TX C]  |      |  Wait Q: [TX B, TX C]  |
   +------------------------+      +------------------------+      +------------------------+
            ^                         ^                         ^
            | (Granted)               | (Blocked - Sleeping)    | (Blocked - Sleeping)
            |                         |                         |
            |                         (WAITING...)              (WAITING...)

   ※ TX B와 TX C는 Row_1에 대한 X-Lock(배타적 잠금)을 획득하지 못해
     'Blocked' 상태로 진입하여 CPU 자원을 소모하지 않고 대기(Wait)한다.
```

**다이어그램 해설**
1.  **트랜잭션 A**가 Row 1에 대해 갱신을 수행하기 위해 X-Lock (Exclusive Lock)을 요청합니다. Lock Manager는 이를 승인하고 A를 소유자(Owner)로 등록합니다.
2.  **트랜잭션 B**가 동일한 Row 1을 갱신하려 X-Lock을 요청하지만, A가 이미 보유하고 있으므로 충돌(Collision)이 발생합니다. LM은 B를 대기 큐(Wait Queue)에 넣고 수면(Sleep) 상태로 전환시킵니다. 이것이 **블로킹**입니다.
3.  **트랜잭션 C**가 읽기를 위해 S-Lock (Shared Lock)을 요청합니다. 하지만 일부 고립화 수준(Isolation Level)이나 DBMS 설정에 따라서는 X-Lock 아래에서 S-Lock조차 대기해야 할 수 있습니다. (MySQL InnoDB의 경우 일반적인 Select는 MVCC로 대기하지 않으나, `LOCK IN SHARE MODE` 사용 시 대기함)
4.  A가 Commit/Rollback을 수행하면, LM은 대기 큐의 헤드에 있는 TX B를 깨워(Wakeup) 락을 획득시킵니다.

#### 3. 심층 동작 원리 및 핵심 알고리즘

**블로킹의 타이밍과 로직**
```sql
-- 의사 코드(Pseudo-code)로 보는 락 획득 시도
FUNCTION TryLock(Resource, Tx, Mode):
    CurrentOwner = LockTable.GetOwner(Resource)
    
    IF CurrentOwner == NULL THEN
        -- ① 자원이空闲 상태
        LockTable.SetOwner(Resource, Tx, Mode)
        RETURN SUCCESS
        
    ELSE IF IsCompatible(CurrentOwner.Mode, Mode) THEN
        -- ② 호환 가능 (예: Shared Lock 끼리)
        LockTable.AddSharedOwner(Resource, Tx)
        RETURN SUCCESS
        
    ELSE
        -- ③ 충돌 발생 -> BLOCKING 시작
        IF Tx.Timeout > 0 THEN
            WAIT_ON(Queue, Timeout)  -- OS 상태로 스케줄 아웃됨
            -- Timeout 발생 시 Error Return (LOCK_WAIT_TIMEOUT)
        ELSE
            RETURN ERROR_LOCK_NOWAIT
        END IF
    END IF
END FUNCTION
```
이 로직에서 `WAIT_ON` 구간이 바로 사용자가 느끼는 지연 시간(Latency)입니다. 블로킹 해결의 핵심은 이 `WAIT_ON` 구간에 진입하는 확률을 줄이거나, 대기 시간을 최소화하는 데 있습니다.

**MVCC에 의한 블로킹 회피 (Non-blocking Read)**
MVCC는 데이터를 수정할 때 최신 버전만 저장하는 것이 아니라, 수정 전 이미지를 Undo Segment에 보관합니다. 읽기 트랜잭션은 이 Undo Log를 링크드 리스트로 따라가며 자신이 시작 시점(Snapshot)에 맞는 데이터를 조회합니다. 따라서 쓰기 트랜잭션이 락을 걸고 있어도, 읽기 트랜잭션은 "과거의 데이터"를 읽으므로 락 대기 없이 즉시 수행됩니다.

**📢 섹션 요약 비유**
데이터베이스의 동시성 제어는 **'열쇠가 있는 방과 CCTV가 있는 방'**의 차이와 같습니다. Locking 방식은 열쇠를 얻어야만 들어갈 수 있어 문 앞에서 대기(Blocking)해야 하지만, MVCC는 CCTV(과거 기록)를 통해 현재 누군가 안에 있더라도 밖에서 상황을 확인(읽기)할 수 있게 하여 대기를 없앱니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Locking vs. MVCC

| 비교 항목 | 낙관적 동시성 제어 (OCC) / MVCC | 비관적 동시성 제어 (PCC) / Locking |
|:---|:---|:---|
| **기본 철학** | 트랜잭션 간 충돌이 적다고 가정 (Optimistic) | 트랜잭션 간 충돌이 빈번하다고 가정 (Pessimistic) |
| **읽기(Read) 성능** | **매우 높음 (Non-blocking)** | 낮음 (Shared Lock 경합 발생 가능) |
| **쓰기(Write) 성능** | 충돌 시 Rollback 비용 큼 | 충돌 시 Wait 비용 (Blocking) 발생 |
| **데이터 일관성** | Snapshot Read (일관성 없는 읽기 가능성) | 실시간 Current Read (강한 일관성) |
| **Storage 비용** | Undo Log, Version Chain 추가 저장 필요 | Lock Table 메모리만 필요 |
| **대표 DBMS** | PostgreSQL, MySQL(InnoDB), Oracle | MS SQL(Server 설정 시), Old-style DB |

#### 2. 과목 융합 관점: OS와 네트워크와의 시너지

**A. OS (Operating System)와의 연계: 스핀락(Spinlock) vs. 뮤텍스(Mutex)**
데이터베이스의 락은 주로 OS의 `Mutex`(대기 큐에서 Sleep)와 유사하게 작동하여 CPU 자원을 낭비하지 않지만, 락 대기 시간이 매우 짧은 경우(µs 단위) 문맥 교환(Context Switching) 비용이 더 크다. 따라서 최신 DBMS(예: Oracle latch, PostgreSQL internal lock)는 짧은 대기에는 OS의 `Spinlock`을 사용하여 대기 상태에 진입하지 않고 계속 CPU를 점유하며 확인(Looping)하는 전략을 취합니다. 즉, **블로킹 관리는 OS 스케줄링 전략과 직결**됩니다.

**B. 네트워크(Network)와의 연계: 헤드 오브 라인 블로킹 (HoL Blocking)**
TCP 네트워크에서도 패킷 하나가 손실되면 이후 패킷들이 모두 대기하는 Head-of-Line Blocking이 발생합니다. DB 블로킹 해소 전략인 '락 범위 최소화'는 네트워크의 '파이프라이닝(Pipelining)'이나 '멀티플렉싱(Multiplexing)' 기술과 맥락을 같이 합니다. 자원을 효율적으로 분리(Segmentation)하여 병목이 전체 시스템으로 전파되는 것을 막는다는 공통의 철학을 가집니다.

**📢 섹션 요약 비유**
Locking은 **'전화 선로 하나를 돌려 쓰는 방식'**으로, 한 사람이 통화 중이면 다른 사람은 기다려야 하는 PCC(비관적) 방식입니다. 반면 MVCC는 **'우편함 시스템'**과 같은 OCC(낙관적) 방식으로, 내가 편지를 쓰는 동안 다른 사람이 이미 도착한 편지를 읽는 것을 막지 않습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 블로킹이 발생했을 때, 단순히 "죽어라 기다리는" 상황을 방지하기 위한 구체적인 솔루션을 제시한다.

#### 1. 실무 시나리오 및 의사결정 매트릭스

**시나리오 1: 배치(Batch) 작업 중 온라인 트랜잭션(OLTP) 장애**
- **상황**: 월말 정산 배치가 `UPDATE ACCOUNT`를 실행 중이고,