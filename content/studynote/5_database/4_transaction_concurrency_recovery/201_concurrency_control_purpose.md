+++
title = "201. 동시성 제어(Concurrency Control)의 목적"
date = "2026-03-16"
+++

# 201. 동시성 제어(Concurrency Control)의 목적

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 동시성 제어(Concurrency Control)는 다중 트랜잭션 환경에서 데이터의 **ACID (Atomicity, Consistency, Isolation, Durability)** 속성, 특히 **일관성(Consistency)**과 **고립성(Isolation)**을 훼손하지 않도록 실행 순서를 보장하는 핵심 데이터베이스 관리 기술이다.
> 2. **가치**: 논리적 데이터 무결성을 유지함은 물론, 자원 경합(Resource Contention)을 최소화하여 시스템 전체의 **TPS (Transactions Per Second)**를 극대화하고 **응답 시간(Latency)**을 최적화하는 성능의 핵심 축이다.
> 3. **융합**: 운영체제(OS)의 프로세스 동기화(세마포어, 뮤텍스)가 트랜잭션 단위로 확장된 개념이며, 분산 시스템의 **CAP 정리**(Consistency, Availability, Partition Tolerance)에서 일관성을 유지하기 위한 선행 기술이다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**동시성 제어(Concurrency Control)**란 DBMS (Database Management System)에서 다수의 트랜잭션이 동시에 실행될 때, 트랜잭션 간의 상호작용으로 인해 데이터베이스의 일관성이 파괴되는 것을 방지하는 일련의 메커니즘입니다.
단순히 "순서대로 처리(Serializability)"하는 것을 넘어, 병렬 처리의 이점을 살리면서 논리적으로는 순차 실행과 동일한 결과를 보장하는 **직렬 가능성(Serializability)**을 달성하는 것이 기술적 핵심입니다.

#### 2. 등장 배경: ① 한계 → ② 패러다임 → ③ 요구
① **기존 한계**: 초기 파일 시스템이나 단순 Lock 방식은 데이터 공유가 불가능하거나 교착상태(Deadlock) 빈도가 높아 대규모 서비스 처리에 한계가 있었습니다.
② **혁신적 패러다임**: 트랜잭션 스케줄링 알고리즘(2PL, MVCC 등)이 도입되어, "비관적(Pessimistic)" 동시 제어와 "낙관적(Optimistic)" 동시 제어 간의 트레이드오프를 조정하게 되었습니다.
③ **현재 요구**: 클라우드 환경과 초연결 시대로 넘어오며 수천~수만 TPS를 처리해야 하는 상황에서, **Microsecond(µs)** 단위의 Lock Contention을 제어하는 것이 절실해졌습니다.

#### 3. 동시성 제어의 논리적 사고 구조
아래 다이어그램은 동시에 접근하는 사용자의 요청이 시스템 내부에서 어떻게 직렬화(Serialization)되어 처리되는지를 보여줍니다.

```text
[동시성 제어에 의한 스케줄링 개념도]

  ▼ User Space (논리적 병렬)
  ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
  │ Transaction A │      │ Transaction B │      │ Transaction C │
  │ (Read Account)│      │(Update Stock) │      │ (Delete Log)  │
  └───────▲───────┘      └───────▲───────┘      └───────▲───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 ▼
  ▼ Kernel / DBMS Kernel (물리적 직렬화 & 보장)
  ┌───────────────────────────────────────────────────────────────┐
  │             Concurrency Control Manager (CCM)                 │
  │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
  │   │ Lock Mgr│───▶│ Scheduler│───▶│ Deadlock│───▶│Log/Recovery│
  │   │ (Mutex) │    │ (Order) │    │ Detect  │    │  (WAL)  │   │
  │   └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
  └───────────────────────────────────────────────────────────────┘
                                 ▼
  ▼ Data Storage (Physical Disk / SSD)
  ┌───────────────────────────────────────────────────────────────┐
  │   [ Data Page 1 ]  [ Data Page 2 ]  [ Data Page 3 ] ...       │
  │   ▶ Consistent State Isolation Guarantee                      │
  └───────────────────────────────────────────────────────────────┘
```
**(해설)**
다이어그램과 같이 사용자는 자신의 요청이 병렬적으로 처리된다고 인식하지만, 내부의 **CCM (Concurrency Control Manager)**은 이를 적절한 알고리즘에 따라 순서화(Scheduling)합니다. 단순한 차단(Block)이 아니라, **Lock Manager (Lock Manager)**가 세밀한 잠금 획득을 관리하고 교착상태를 감시하며, 결과적으로 **Storage**에는 일관성 있는 상태로만 기록됨을 확인할 수 있습니다.

> **📢 섹션 요약 비유**: 동시성 제어는 복잡한 **고속도로 톨게이트**와 같습니다. 수많은 차량(트랜잭션)이 빠르게 통과하게 하되(처리량 극대화), 차선이 서로 섞이지 않도록 안전선태를 하고(고립성), 최종적으로 모든 차량이 무사 목적지에 도달하도록(일관성) 정리하는 교통정리 시스템입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

동시성 제어를 구현하기 위해서는 트랜잭션의 **격리성 수준(Isolation Level)**과 이를 강제하기 위한 **잠금(Locking) 또는 다중 버전(MVCC)** 메커니즘이 결합되어야 합니다.

#### 1. 핵심 구성 요소 상세

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/기법 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Lock Manager (LM)** | 자원 할당 및 대기 관리 | 잠금 요청(Lock Request) 큐 관리, 데드락 감지 | 2PL (Two-Phase Locking) | 주차장 관리인 |
| **Scheduler (스케줄러)** | 트랜잭션 실행 순서 결정 | 직렬 가능성(Serializability) 검증, 순서 그래프 생성 | precedence Graph | 작업 지시서 |
| **MVCC Engine** | 비차단 읽기(Non-blocking Read) | 데이터의 다중 버전 유지, Undo Log 활용 | Snapshot Isolation (SI) | 문서의 버전 관리(Git) |
| **Time Stamp (TS)** | 논리적 시간 부여 및 순서 보장 | 각 트랜잭션에 진입 시점 부여, 충돌 시 롤백 | TO (Timestamp Ordering) | 접수 번호표 |
| **WAL (Write-Ahead Logging)** | 데이터 복구 및 원자성 보장 | 데이터 변경 전 로그 기록 (Commit 전) | ARIES Algorithm | 카메라 블랙박스 |

#### 2. 상세 아키텍처: 데이터 접근 제어 흐름
트랜잭션이 데이터를 조작할 때, DBMS 내부에서 발생하는 일련의 과정을 도식화합니다.

```text
[트랜잭션 동시성 제어 라이프사이클]

  1. REQUEST
  ┌──────────────────────────────────────────────────────────────┐
  │ T1: UPDATE accounts SET balance = 100 WHERE id = 1          │
  └───────────────────────┬──────────────────────────────────────┘
                            ▼
  2. LOCK ACQUISITION (Lock Manager)
  ┌──────────────────────────────────────────────────────────────┐
  │ [Shared Lock池]  [Exclusive Lock池]                         │
  │  ...read...          [WRITE] ◀── 현재 T1이 X-Lock 획득 시도 │
  └───────────────────────┬──────────────────────────────────────┘
                            │
                 ┌──────────┴───────────┐
                 ▼ Conflict?            ▼ No Conflict
  ┌──────────────────────┐    ┌──────────────────────────────┐
  │  Wait / Block /      │    │  Grant Lock (성공)           │
  │  Deadlock Check      │    │  (Lock Table에 등록)        │
  └──────────────────────┘    └──────────┬───────────────────┘
                                         ▼
  3. EXECUTE & BUFFER (Buffer Pool)
  ┌──────────────────────────────────────────────────────────────┐
  │  [Disk Page] ──▶ [Buffer Frame] ──▶ [Tuple (Old → New)]    │
  │                                │                            │
  │                      (Update in Memory)                     │
  └───────────────────────┬──────────────────────────────────────┘
                            ▼
  4. LOGGING (WAL)
  ┌──────────────────────────────────────────────────────────────┐
  │  <Undo Log> <Redo Log>  (Log Buffer flush to Disk)          │
  └───────────────────────┬──────────────────────────────────────┘
                            ▼
  5. COMMIT / RELEASE
  ┌──────────────────────────────────────────────────────────────┐
  │  Transaction End → Release All Locks → Notify Waiting Txns  │
  └──────────────────────────────────────────────────────────────┘
```
**(해설)**
이 과정은 **PM (Programmable Memory)**에서 **Storage**로 데이터가 내려가기 전의 논리적 흐름입니다. 가장 중요한 점은 **Lock Manager**의 개입입니다. T1이 쓰기 작업을 하려 하면, 다른 트랜잭션이 해당 데이터를 읽거나 쓰지 못하도록 **X-Lock (Exclusive Lock)**을 획득해야 합니다. 충돌이 발생하면 해당 트랜잭션은 대기(Queue)하거나, 시스템 설정에 따라 롤백(Rollback)됩니다. 이러한 메커니즘 덕분에 메모리(RAM)상의 임시 데이터가 실제 디스크에 안전하게 반영됩니다.

#### 3. 핵심 알고리즘: 2PL (Two-Phase Locking)
가장 대표적인 동시성 제어 프로토콜인 **이단계 잠금 프로토콜(2PL)**의 동작 원리입니다. 직렬 가능성을 보장하지만, 교착상태 발생 가능성이 있습니다.

```python
# Pseudo-code for Two-Phase Locking (Strict 2PL)
class Transaction:
    def acquire_lock(self, resource, mode):
        # Growing Phase: 확장 단계 (잠금만 획득, 해제 없음)
        if not LockManager.is_available(resource, mode):
            wait()  # 대기 혹은 Deadlock 발생
        LockManager.grant(resource, self.id, mode)

    def release_locks(self):
        # Shrinking Phase: 축소 단계 (잠금 해제만, 획득 없음)
        # Strict 2PL에서는 Commit 시점에 모든 잠금 해제
        LockManager.release_all(self.id)
        
    def commit(self):
        # WAL flush 후
        write_to_disk()
        self.release_locks()  # Commit 시점에 일괄 해제
```
**(해설)**
위 코드는 **Strict 2PL**를 모방한 것입니다. 핵심은 **Growing Phase**에서는 잠금을 계속 추가하기만 하고, **Commit**이 되는 순간 **Shrinking Phase**가 시작되어 모든 잠금을 해제한다는 점입니다. 이 규칙을 어기면(예: 중간에 Lock을 풀었다가 다시 얻으면) 직렬 가능성이 깨집니다.

> **📢 섹션 요약 비유**: 2PL 프로토콜은 **'예매 시스템'**과 같습니다. 공연장 좌석(데이터)을 예약할 때(Lock 획득), 예약을 완료(Commit)하기 전까지는 다른 사람에게 그 좌석을 팔 수 없고, 내가 취소(Release)하기 전까지는 좌석을 비워둘 수 없는 원칙을 철저히 지키는 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술 비교: 낙관적(Optimistic) vs 비관적(Pessimistic) 제어

| 비교 항목 | 비관적 제어 (Pessimistic CC) | 낙관적 제어 (Optimistic CC) |
|:---|:---|:---|
| **기본 철학** | 충돌이 발생할 것이라고 가정하고 선 잠금 | 충돌이 드물다고 가정하고 일단 진행 |
| **대표 기법** | Locking (Shared/Exclusive), 2PL | Timestamp Ordering, Validation |
| **성능 특징** | 충돌 시 Lock Overhead가 크지만 안정적 | Lock Overhead가 적으나 Rollback 비용 큼 |
| **적합 환경** | 충돌 빈번한 OLTP (금융, 재고) | 충돌 드문 OLAP, 배치 작업 |
| **주요 지표** | Latency 예측 가능 (Wait time 증가) | 평균 Latency 낮으나 최악의 경우 급증 |

#### 2. 분석: Lock 기반 vs MVCC (Multi-Version Concurrency Control)
현대 DB(MySQL, PostgreSQL, Oracle)는 주로 **MVCC**와 **Locking**을 혼합하여 사용합니다.

```text
[MVCC를 활용한 Non-Blocking Read 구조]

  Disk (Storage)
  ┌───────────────────────────────────────────────────┐
  │  Row Data: [ ID:1 | Name:Kim | Balance:10000 ]   │
  └────────────────────┬──────────────────────────────┘
                       ▼ Undo Segment (Rollback Segment)
            ┌──────────────────────────────────────┐
            │ Ver1 (Balance:9000) ◀─── T1이 읽음    │ (Old Version)
            │ Ver2 (Balance:10000) ◀─── T2가 씀    │ (New Version)
            └──────────────────────────────────────┘
                      
  ▼ 동작 상황
  1. T2 (Update): Balance를 9000→10000으로 변경. Excl. Lock 획득.
  2. T1 (Select): 9000원을 읽으려 함.
     → Lock을 기다리지 않고(Undo Log에서) Ver1(9000원)을 즉시 읽음.
```
**(해설)**
이 구조는 동시성 제어의 **융합** 형태입니다. 쓰기(Write) 작업은 여전히 **Lock**을 사용하여 충돌을 막지만, 읽기(Read) 작업은 Lock을 기다리지 않고 **과거 버전의 데이터(Undo Log)**를 읽어서 즉시 반환합니다. 이를 통해 **Latency**를 획기적으로 줄이면서도 일관성을 유지합니다.

#### 3. 타 영역과의 융합 (Synergy)
- **OS (Operating System)**: 프로세스 간 **Mutual Exclusion (상호 배제)**를 위한 세마포어(Semaphore) 구현