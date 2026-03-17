+++
title = "440. 트랜잭션 ACID 특성 - 데이터베이스의 헌법"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 440
+++

# 440. 트랜잭션 ACID 특성 - 데이터베이스의 헌법

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ACID는 **Transaction (트랜잭션)** 이 데이터베이스에서 수행되는 동안 데이터의 무결성과 신뢰성을 보장하기 위해 반드시 준수해야 하는 4가지 핵심 속성인 **Atomicity (원자성), Consistency (일관성), Isolation (독립성/격리성), Durability (지속성)**의 약어입니다.
> 2. **가치**: 시스템 장애(서버 다운, 네트워크 단절 등)나 다중 사용자의 동시 접근 환경에서도 데이터가 **Partial Update (부분 갱신)** 되지 않음을 보장하며, 이는 금융 거래와 같은 Critical System (치명적 시스템)에서 **RTO (Recovery Time Objective)** 및 **RPO (Recovery Point Objective)**를 0에 수렴하게 만드는 기술적 근간입니다.
> 3. **융합**: 단순한 논리적 개념을 넘어, **Recovery Management (회복 관리)** 기술인 WAL(Write-Ahead Logging)과 **Concurrency Control (병행 제어)** 기술인 Locking Protocol, **MVCC (Multi-Version Concurrency Control)** 등과 밀접하게 결합하여 DBMS 내부 커널의 핵심 메커니즘을 구성합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**ACID**란 데이터베이스 내에서 하나의 논리적 작업 단위인 **Transaction (트랜잭션)**이 수행될 때, 데이터의 무결성을 보장하기 위해 반드시 충족해야 하는 4가지 핵심 속성의 집합입니다.
트랜잭션은 데이터베이스 상태를 변화시키는 일련의 연산 집합(예: `SELECT`, `UPDATE`, `INSERT`, `DELETE`)으로 정의되며, 이 과정에서 시스템 장애, 동시성 충돌, 네트워크 오류 등 다양한 예외 상황이 발생하더라도 데이터가 항상 정확한 상태를 유지하도록 강제하는 규칙입니다. 이는 데이터베이스 시스템을 단순한 데이터 저장소가 아닌 '신뢰할 수 있는 상태 기계(State Machine)'로 승격시키는 철학적이자 공학적인 기반이 됩니다.

#### 2. 💡 비유: 무조건 한 팀이 되어야 하는 이동식 (All or Nothing)
계좌 이체를 예로 들어봅시다. A가 B에게 100만 원을 송금한다면, "A의 계좌에서 100만 원을 차감"하고 "B의 계좌에 100만 원을 추가"하는 두 가지 작업은 반드시 하나의 세트로 묶여야 합니다. A의 돈은 빠졌는데 전산망 오류로 B의 계좌에 입금되지 않았다면, 혹은 입금은 됐는데 출금이 안 됐다면 이는 재앙입니다. ACID는 이 두 작업이 마치 원자(Atom)처럼 쪼개질 수 없는 하나의 단위로 처리되어, 둘 다 성공하거나(Control) 둘 다 실패하여(Rollback) 원래대로 돌아가는 것을 보장합니다.

#### 3. 등장 배경: ① 초기의 한계 → ② 일관성 추구 → ③ 현대의 분산 환경 도전
① **초기 파일 시스템의 한계**: 초기 데이터 저장소는 데이터를 파일 단위로 관리하였으나, 시스템 오류 발생 시 데이터의 중간 상태가 저장되어 **Inconsistent State (불일치 상태)**에 빠지는 문제가 있었습니다. ② **트랜잭션 개념의 도입**: 1970년대 **System R** 프로젝트 등을 통해 트랜잭션 개념이 정립되고 ACID 속성이 수학적으로 정의되면서, 데이터베이스는 상업적 신뢰성을 획득할 수 있었습니다. ③ **현대의 확장**: 현재에는 수천만 명의 동시 접속을 처리하는 **High Concurrency (고동시성)** 환경과 데이터 분산 저장 환경에서 이 ACID 속성을 어떻게 효율적으로 구현할 것인가가 핵심 과제로 떠올랐습니다.

> **📢 섹션 요약 비유**: ACID는 마치 **'양날 철극 위의 줄타기'**와 같습니다. 한쪽 발은 **속도(성능)**에, 다른 한쪽 발은 **안전(무결성)**에 두고 있습니다. 아무리 빨리 달려도(성능 개선) 중간에 떨어져서 데이터가 망가지면 안 되므로, 안전띠(ACID)를 매고 균형을 유지하며 최적의 속도를 내는 것이 DBMS의 목표입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 상세 분석
ACID는 4가지 속성이 독립적으로 존재하는 것이 아니라, 서로 밀접하게 얽혀 데이터베이스 **Buffer Manager (버퍼 관리자)**, **Transaction Manager (트랜잭션 관리자)**, **Recovery Manager (회복 관리자)**에 의해 구현됩니다.

| 속성 | 기술 명칭 (Full Name) | 핵심 역할 | 내부 동작 메커니즘 (Implementation) | 주요 Protocol/기술 | 비유 |
|:---:|:---|:---|:---|:---|:---|
| **A** | **Atomicity** <br>(원자성) | **"All or Nothing"** <br>트랜잭션의 연산이 모두 반영되거나, 전혀 반영되지 않음을 보장 | **Undo (Undo Logs)**: 실패 시 트랜잭션 시작 전 상태로 복귀 | Write-Ahead Logging (WAL) <br>Shadow Paging | 레고 조립: 완성되지 않으면 다시 분해함 |
| **C** | **Consistency** <br>(일관성) | **"Data Correctness"** <br>트랜잭션 수행前后 DB가 유효한 상태(무결성 제약) 유지 | **Constraint Check**: 데이터베이스 규칙(Key, Domain) 위반 시 Rollback | Integrity Constraints <br>Triggers | 회계 원칙: 대변과 차변은 항상 일치함 |
| **I** | **Isolation** <br>(격리성) | **"Concurrency"** <br>동시 실행되는 트랜잭션 간 서로 간섭하지 않음 | **Locking / MVCC**: 데이터 접근을 직렬화하거나 버전 분리 | Locking (2PL), <br>MVCC (Snapshot) | 칸막이 있는 시험장: 다른 사람 답안 안 보임 |
| **D** | **Durability** <br>(지속성) | **"Survivability"** <br>커밋된 데이터는 영구적으로 저장되어 장애에도 살아남음 | **Redo (Redo Logs)**: 비휘발성 저장소(Disk)로 로그 기록 | WAL, <br>Checkpointing | 돌판에 새기면: 종이가 찢겨도 글씨는 남음 |

#### 2. 아키텍처 및 데이터 흐름 (ASCII Diagram)

트랜잭션이 ACID 속성을 유지하며 처리되는 과정은 크게 **Log Buffer**, **Data Buffer**, **Disk Storage** 간의 데이터 교환으로 이해할 수 있습니다.

```text
   [ User Application ]
             │
             ▼
┌──────────────────────────────────────────────────────┐
│  Database Management System (DBMS) Kernel            │
│  ┌────────────────────────────────────────────────┐  │
│  │  Transaction Manager (TM)                      │  │
│  │  - Begin, Commit, Rollback 제어                │  │
│  └──────────────┬─────────────────────────────────┘  │
│                 │                                     │
│  ┌──────────────▼─────────────────────────────────┐  │
│  │  Recovery & Concurrency Controller             │  │
│  │  (Lock Manager / MVCC Engine)                  │  │
│  │  - Isolation 보장 (Locking)                    │  │
│  └──────────────┬─────────────────────────────────┘  │
│                 │                                     │
│  ┌──────────────▼─────────────────────────────────┐  │
│  │  Buffer Manager (Shared Pool / Buffer Cache)   │  │
│  │  ┌──────────────┐      ┌──────────────┐        │  │
│  │  │ Log Buffer   │      │ Data Buffer  │        │  │
│  │  │ (Redo/Undo)  │      │ (Page Cache) │        │  │
│  │  └──────┬───────┘      └──────┬───────┘        │  │
│  └─────────┼────────────────────┼─────────────────┘  │
└────────────┼────────────────────┼────────────────────┘
             │                    │
             │ WAL Protocol       │ Dirty Page Write
             │ (Log First!)       │ (Checkpoint)
             ▼                    ▼
     ┌───────────────┐    ┌──────────────────┐
     │  Log Files    │    │  Data Files      │
     │  (Redo/Undo)  │    │  (Tables/Indexes)│
     └───────────────┘    └──────────────────┘
             ▲                    ▲
             │   Non-Volatile     │
             └────── Storage ─────┘
```

**[다이어그램 해설]**
1.  **요청 및 제어 (TM)**: 사용자가 트랜잭션을 시작(`BEGIN`)하면 **Transaction Manager**가 할당된 **LSN (Log Sequence Number)**을 부여합니다.
2.  **버퍼 처리**: 변경 사항은 즉시 디스크에 쓰이지 않고 메모리 영역인 **Data Buffer**와 **Log Buffer**에 기록됩니다. 이는 디스크 I/O의 병목을 줄이기 위함입니다.
3.  **고립성 확보 (Lock/MVCC)**: 데이터 접근 시 **Lock Manager**가 테이블/행 레벨의 Lock을 걸어 다른 트랜잭션의 접근을 제어하거나, **MVCC** 방식을 사용하여 이전 버전의 데이터(Snapshot)를 제공함으로써 읽기 작업이 쓰기 작업을 방해하지 않도록 합니다.
4.  **영속성 확보 (WAL)**: 커밋(`COMMIT`) 시점이 되면 **Write-Ahead Logging (WAL)** 규칙에 따라, 데이터 파일보다 먼저 **Log Buffer**의 내용을 **Redo Log** 파일에 플러시(Flush)합니다. 이때까지 트랜잭션은 성공한 것으로 간주됩니다.
5.  **데이터 기록 (Checkpoint)**: 체크포인트(Checkpoint) 이벤트가 발생하면 메모리의 더티 페이지(Dirty Page)가 실제 데이터 파일로 기록됩니다.

#### 3. 핵심 알고리즘 및 코드 (WAL Protocol)
**WAL (Write-Ahead Logging)**은 Atomicity와 Durability를 동시에 구현하는 핵심 알고리즘입니다. 데이터를 데이터 파일에 쓰기 전에 반드시 로그 파일에 먼저 기록해야 한다는 원칙입니다.

```sql
/* [의사코드] WAL Protocol 기반 트랜잭션 커밋 로직 */
FUNCTION Transaction_Commit(transaction_id):
    
    1. BEGIN TRANSACTION
       /* 메모리 상의 Data Buffer에 변경 사항 반영 (Cached) */
       
    2. GENERATE_LOG_RECORD(transaction_id, operation_type, data_before, data_after)
       /* 로그 레코드 생성: Undo 정보(Before image) + Redo 정보(After image) */

    3. WRITE_TO_LOG_BUFFER(log_record)
       /* 로그를 버퍼에 작성 */

    4. FLUSH_LOG_TO_DISK()
       /* 핵심: 데이터 파일을 수정하기 전에 로그를 안정적인 디스크에 기록함.
          - 이 시점에서 전원이 나가도 Log를 통해 복구 가능 (Durability 보장) */

    5. UNLOCK_RESOURCES(transaction_id)
       /* Lock 해제 (다른 트랜잭션이 접근 가능) */

    6. RETURN "COMMIT SUCCESS"
       
    /* 실제 데이터 파일(Data File)에 대한 쓰기는 
       Checkpoint 발생 시나 Background 스레드에 의해 비동기적으로 처리됨 */
END FUNCTION
```

> **📢 섹션 요약 비유**: ACID와 WAL 구조는 마치 **'음식점 주문 및 주방 시스템'**과 같습니다.
> 1. **주문 (Transaction)**: 손님이 주문서를 떼어냅니다.
> 2. **기록 (Log)**: 주방장이 요리를 시작하기 전에 **주문서(로그)를 KDS(주방 디스플레이)에 고정(플러시)**시킵니다. (이 주문서가 확보되어야 요리를 시작합니다.)
> 3. **요리 (Buffer)**: 요리는 냄퍼(메모리)에서 이루어지지만, 완성되기 전까지 손님에게는 서빙되지 않습니다.
> 4. **서빙 (Commit)**: 요리가 완성되면(Commit), 주방장은 주문서를 '완료' 처리하고 손님에게 제공합니다. 나중에 손님이 "이거 다시 만들어줘"라고 해도(UNDO), 주문서가 남아있으니 처리할 수 있고, 설령 화재가 나도(Disaster) 주문서는 금고에 보관되어 있으니 다시 만들 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 격리 수준(Isolation Level)에 따른 기술적 트레이드오프 (비교표)
ACID의 속성 중 **Isolation**은 성능(Concurrency)과 가장 첨예하게 대립하는 속성입니다. **ANSI/ISO SQL 표준**에서는 격리 수준을 4단계로 나누어, 사용자가 성능과 정합성 사이에서 선택할 수 있게 합니다. 이는 **MVCC**와 **Locking** 기술의 융합 결과입니다.

| 격리 수준 (Isolation Level) | Dirty Read (더티 읽기) | Non-Repeatable Read (반복 불가능 읽기) | Phantom Read (팬텀 읽기) | Locking Overhead | Real-world Usage |
|:---|:---:|:---:|:---:|:---:|:---|
| **Read Uncommitted** | 발생함 | 발생함 | 발생함 | **낮음** (Lock 없음) | 거의 사용 안 함 (Long-running 분석 쿼리 등 극히 예외적) |
| **Read Committed** <br>(Oracle, PostgreSQL Default) | **방지** | 발생함 | 발생함 | **중간** (SELECT 시 Lock X, Update 시 Lock O) | **범용적** (대부분의 웹 서비스) |
| **Repeatable Read** <br>(MySQL Default) | **방지** | **방지** | 발생함 가능성* | **높음** (Shared Lock 유지) | 금융 거래, 재고 관리 등 정합성 중요 �