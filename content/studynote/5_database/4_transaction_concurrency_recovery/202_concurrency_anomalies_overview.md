+++
title = "202. 병행 수행 시 문제점 (격리성 위배 시)"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 202
+++

# 202. 병행 수행 시 문제점 (격리성 위배 시)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중 트랜잭션 환경에서 **ACID (Atomicity, Consistency, Isolation, Durability)** 특성 중 **격리성(Isolation)**이 보장되지 않을 때 발생하는 논리적 데이터 불일치 현상이다.
> 2. **가치**: 갱신 손실(Lost Update), 더티 읽기(Dirty Read), 반복 불가능 읽기(Non-repeatable Read), 팬텀 리드(Phantom Read) 등 4대 이상 현상을 정량적으로 분석하여 DBMS (Database Management System)의 동시성 제어(Concurrency Control) 성능 지표(TPS, Latency)를 최적화한다.
> 3. **융합**: 운영체제의 레이스 컨디션(Race Condition) 및 임계 영역(Critical Section) 문제와 본질적으로 같으며, 분산 시스템의 CAP 정리(Consistency, Availability, Partition Tolerance) 중 일관성(C) 트레이드오프의 핵심 근거가 된다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
병행 수행(Concurrent Execution) 시 문제점이란, 다수의 트랜잭션(Transaction)이 동일한 데이터 항목(Data Item)에 동시에 접근하여 갱신(Read/Write)할 때, **트랜잭션 스케줄러(Transaction Scheduler)**의 적절한 제어 없이 **연산(Operation)**이 섞여 실행(Interleaving)됨으로써 발생하는 데이터 무결성(Integrity) 침해 현상을 의미합니다. 이는 단일 CPU 환경에서의 시분할(Time Sharing) 방식이나 다중 CPU 환경에서의 진정한 병렬 실행 모두에서 발생할 수 있으며, 결과적으로 데이터베이스의 일관성(Consistency) 상태를 파괴하는 치명적인 오류로 이어집니다.

#### 2. 등장 배경 및 필요성
초기 데이터베이스 환경은 일괄 처리(Batch Processing) 위주로 단일 트랜잭션 실행이 보편적이었습니다. 그러나 온라인 트랜잭션 처리(OLTP, Online Transaction Processing) 환경이 도래하면서 수천 개의 트랜잭션이 초당 몰리는 고부하 상황이 발생했습니다. 이때 모든 트랜잭션을 순차적으로 직렬화(Serializable)하게 처리하면 **처리량(Throughput)**이 급격히 저하되어 실무적으로 사용 불가능해집니다. 따라서 병행 수행은 필수적이나, 이로 인해 발생하는 데이터 오염 문제를 해결하기 위해 **로킹 프로토콜(Locking Protocol)**, **타임스탬프 순서 결정(Timestamp Ordering)**, **다중 버전 동시성 제어(MVCC, Multi-Version Concurrency Control)**와 같은 기술이 등장하게 되었습니다.

```text
[병행 수행 시나리오 개념도]

     시간(Time) ───────────────────────────────────────────────▶
     
 T1: |---Read(X)--|-------Write(X)-------|-------Commit--|
                      ▲                     ▲
                      │                     │
 T2:                 |--Read(Y)--|--Write(X)--|---Commit---|
                      (오염된 데이터 읽기)     (T1의 결과 덮어쓰기)

 [발생 가능 문제]
 ① T1이 Commit 전 Rollback 시 → T2는 더티 데이터(Dirty Data) 보유
 ② T2가 먼저 Commit 시 → T1의 갱신 내역 손실 (Lost Update)
```

#### 3. 상세 해설
위 다이어그램은 두 개의 트랜잭션 T1과 T2가 시간축 상에서 겹치며 실행되는 상황(Interleaving)을 도식화한 것입니다. T1이 데이터 X를 읽고 갱신하는 동안, T2가 개입하여 데이터를 읽거나 쓰는 과정에서 제어 장치(Control Mechanism)가 없다면 T1의 아직 완료되지 않은 중간 상태(Middle State)가 T2에게 노출됩니다. 이를 방지하기 위해 DBMS는 트랜잭션의 고립성을 보장하기 위해 다양한 수단을 제공합니다.

#### 📢 섹션 요약 비유
이는 **'두 명의 비서가 한 대의 타자기로 동시에 문서를 작성하려는 상황'**과 같습니다. 한 명이 타자를 치는 동안 다른 사람이 끼어들어 수정을 가하거나, 아직 저장되지 않은 초안을 가져가 배포해버리면, 최종 문서는 엉망이 되고 말 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 격리성 위배로 인한 4대 주요 문제점 (상세 분석)

병행 제어(Concurrency Control)가 실패했을 때 발생하는 구체적인 현상들은 데이터 정합성에 미치는 영향력과 발생 메커니즘에 따라 다음과 같이 분류됩니다.

| 문제점 (Anomaly) | 기술적 정의 | 발생 조건 (Dependencies) | 피해 영향 | 관련 연산 |
|:---|:---|:---|:---|:---|
| **갱신 손실**<br>(Lost Update) | 두 트랜잭션이 동일 데이터를 Read 후 Write할 때, 후행 트랜잭션의 Commit으로 선행 트랜잭션의 변경이 무시되는 현상 | W1(X) ... W2(X) (Write-Write Conflict) | 데이터 변경 누락 | Write - Write |
| **더티 읽기**<br>(Dirty Read) | 커밋되지 않은(Uncommitted) 중간 데이터를 타 트랜잭션이 Read하고, 이후 원본이 Rollback되어 가짜 데이터를 보유하는 현상 | W1(X) ... R2(X) (Write-Read Conflict) | 데이터 무결성 파괴 | Write - Read |
| **반복 불가능 읽기**<br>(Non-repeatable Read) | 한 트랜잭션 내에서 동일 데이터를 두 번 Read할 때, 사이에 다른 트랜잭션이 수정하여 결과가 상이한 현상 | R1(X) ... W2(X) ... R1(X) | 논리적 모순 발생 | Read - Write |
| **팬텀 리드**<br>(Phantom Read) | 범위 검색(Search) 시, 타 트랜잭션이 새로운 레코드(Tuple)를 삽입/삭제하여 다음 검색에서 '유령' 데이터가 나타나는 현상 | R1(Set) ... W2(Insert) ... R1(Set) | 집계 함수 오류 | Insert/Delete |

#### 2. 문제 발생 시나리오 및 데이터 플로우

아래는 **Lost Update**와 **Dirty Read**가 발생하는 구체적인 연산 순서(Instruction Level)를 도식화한 것입니다.

```text
[상황 A: 갱신 손실 (Lost Update)]
초기값: X = 10

 T1 (A 계좌)                T2 (B 계좌)                DB 상태(X)
 ─────────────────────────────────────────────────────────────────
   Read(X)  ────────▶ 100 가져옴                      (X=10)
                             Read(X)  ────────▶ 100 가져옴   (X=10)
   X = X + 100 (200)                                  (X=10)
                             X = X + 50 (150)             (X=10)
   Write(X) ────────▶ 200 기록                         (X=200)
                             Write(X) ────────▶ 150 기록   (X=150)
                             Commit
   Commit                                               (X=150)
   
 [결과]: T1의 +100 업데이트가 사라짐. (비즈니스상 잔액 부족 현상)


[상황 B: 더티 읽기 (Dirty Read)]

 T1 (출금 작업)              T2 (잔액 조회)                DB 상태(X)
 ─────────────────────────────────────────────────────────────────
   Read(X) ────────▶ 100 가져옴                       (X=100)
   X = X - 100 (0)
   Write(X) ────────▶ 0 기록                          (X=0)
                             Read(X) ────────▶ 0 가져옴    (X=0)
                             (화면: "잔액 0원" 표시)
   [오류 발생으로 Rollback]                            (X=100)
   (원상 복구됨)
   
 [결과]: T2는 사용자에게 0원을 알렸으나, 실제 DB에는 100원 존재.
```

#### 3. 심층 동작 원리 및 알고리즘
이러한 문제를 방어하기 위해 **스케줄러(Scheduler)**는 트랜잭션의 연산(Read/Write)이 요청될 때마다 **직렬 가능성 그래프(Serialization Graph)**를 검사하거나 **잠금(Lock)** 테이블을 참조합니다. 예를 들어, 갱신 손실을 방지하기 위해서는 `Lock(X)` 및 `Unlock(X)` 명령어를 원자적(Atomic) 연산으로 취급해야 하며, **2단계 로킹 프로토콜(2PL, Two-Phase Locking)**을 준수하여 Growing Phase(잠금 획득만 수행)와 Shrinking Phase(잠금 해제만 수행)를 엄격히 분리해야 합니다.

```python
# Pseudo-code: 2PL Protocol Example
def transaction_update(data_id, new_value):
    # Phase 1: Growing Phase (Acquire Locks)
    lock = exclusive_lock_manager.acquire(data_id)  # Blocking if held by others
    
    # Critical Section
    current_val = database.read(data_id)
    updated_val = current_val + new_value
    database.write(data_id, updated_val)
    
    # Phase 2: Shrinking Phase (Release Locks)
    commit()
    exclusive_lock_manager.release(lock)
```

#### 📢 섹션 요약 비유
이러한 문제점들은 **'수험장에서 친구끼리 커닝 페이퍼를 주고받다가 시험지가 뒤섞이는 상황'**과 유사합니다. 친구가 작성하던 답안을 미리 보고 베꼈는데(더티 읽기), 그 친구가 시험을 포기해 답안을 찢어버린다면, 베낸 사람은 엉뚱한 답을 제출하게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술 심층 비교 (Locking vs MVCC)

격리성 위배 문제를 해결하는 대표적인 두 가지 패러다임인 **잠금 기반(Locking-based)** 방식과 **다중 버전 기반(MVCC-based)** 방식은 서로 다른 트레이드오프(Trade-off)를 가집니다.

| 비교 항목 | Locking-based (e.g., 2PL) | MVCC (Multi-Version Concurrency Control) |
|:---|:---|:---|
| **기본 원리** | 트랜잭션 충돌 시 Block(대기) 시켜 순서화 | 데이터의 이전 버전(Snapshot) 유지하여 Non-blocking |
| **갱신 손실 방지** | X-Lock (Exclusive Lock)으로 완벽 방지 | Update 시 비교(CAS) 또는 Locking 사용하여 방지 |
| **더티 읽기 방지** | Lock에 의해 물리적 차단 | Undo Log를 통한 이전 버전 제공으로 자연 방지 |
| **성능 지표** | Lock Contention이 높으면 TPS 급감 | Read는 Never-blocking, Write 충돌 시에만 Lock |
| **교착상태(Deadlock)** | 발생 가능성 높음 (Cycle 형성) | 교착상태 가능성 낮음 (Read 제외) |

#### 2. 타 영역(OS)과의 융합 관점
데이터베이스의 격리성 문제는 운영체제(OS, Operating System)의 **프로세스 동기화(Process Synchronization)** 메커니즘과 본질적으로 동일합니다. OS에서의 **세마포어(Semaphore)**나 **모니터(Monitor)**는 공유 자원에 대한 접근을 제어하며, 이는 DBMS의 **Lock Manager**와 대응됩니다. 다만, OS는 주로 메모리 페이지나 파일에 대한 짧은 시간의 locking을 다루는 반면, DBMS는 디스크에 영구 저장되는 레코드/페이지 단위의 긴 트랜잭션을 다루므로 **교착상태(Deadlock) 감지 및 회복 복잡도**가 훨씬 높습니다.

```text
[격리 수준(Isolation Level)에 따른 허용 기준]

                     ┌───────────────────────┐
                     │  Dirty Read   │  Lost Update │
Level 0 (Read Uncommitted)│      ⭕            │      ⭕          │ (격리 없음)
                     ├───────────────────────┤
Level 1 (Read Committed)  │      ❌            │      ⭕          │ (오염 방지)
                     ├───────────────────────┤
Level 2 (Repeatable Read) │      ❌            │      ❌          │ (모순 방지)
                     ├───────────────────────┤
Level 3 (Serializable)    │      ❌            │      ❌          │ (완벽 격리)
                     └───────────────────────┘

 ⭕ : 문제 발생 가능 (Phenomena 발생)
 ❌ : 문제 방지됨 (Protected by Lock/Version)
```

#### 📢 섹션 요약 비유
잠금 방식(Locking)은 **'단일 차선 교량에서 신호등을 통해 차량을 통제하는 것'**과 같아서, 대기 시간이 길어질 수 있지만(성능 저하) 충돌은 막을 수 있습니다. 반면 MVCC는 **'고속도로의 회전 교차로(Roundabout)'**처럼, 원하는 방향으로 흐름을 분리하여(Rollback Segment) 읽기 차량은 멈추지 않고 통과하게 하는 고성능 구조입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 과정
**상황**: 대규모 이커머스 플랫폼의 **재고 관리(Inventory Management)** 시스템 구축 시, 한정 상품의 동시 주문이 몰리는 이벤트 상황을 가정합니다.

1.  **문제**: MySQL(InnoDB) 기반에서 `REPEATABLE READ` 격리 수준 사용 시, 팬텀 리드(Phantom Read) 현상이 발생하여 재고가 마지막 한 개임에도 여러 고객에게 주문 완료 메시지가 가는 오류 발생.
2.  **원인 분석**: Gap Lock(갭 락)이 제대로 작동하지 않거나, 트랜잭션 외부에서 `SELECT ... FOR UPDATE` 구문을 사용하지 않아 Non-locking read로 인한 갱신 손실 발생.
3.  **해결 전략**:
    -   **전략 A (DBMS 레벨)**: 갱신 쿼리 실행 시 반드시 `SELECT quantity FROM items WHERE id=1 FOR UPDATE;`를 사용하여 명시적 잠금(Explicit Lock)을 획득.
    -   **전략 B (애플리케이