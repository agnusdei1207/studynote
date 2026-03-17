+++
title = "416. DML(Data Manipulation Language) - 데이터의 생동하는 변화"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 416
+++

# 416. DML(Data Manipulation Language) - 데이터의 생동하는 변화

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DML (Data Manipulation Language, 데이터 조작 언어)은 정의된 스키마 구조 내에서 데이터베이스의 상태를 변화시키거나 조회하는 모든 상호작용을 총괄하는 SQL (Structured Query Language)의 핵심 하위 집합입니다.
> 2. **가치**: 비즈니스 로직을 데이터 영속성(Persistence) 계층으로 투영하는 실질적인 인터페이스로, 트랜잭션(Transaction) 처리 메커니즘을 통해 데이터의 정합성(Consistency)과 원자성(Atomicity)을 보장합니다.
> 3. **융합**: OS(Operating System)의 파일 시스템 쓰기와 버퍼 관리 원리를 결합하여 ACID 특성을 구현하며, 이를 통해 애플리케이션 계층과 스토리지 계층 간의 신뢰할 수 있는 데이터 동기화를 달성합니다.

---

### Ⅰ. 개요 (Context & Background) - [600자+]

DML은 사용자나 애플리케이션이 데이터베이스 관리시스템(DBMS, Database Management System)에 저장된 데이터에 접근하여 조작할 수 있게 하는 명령어 집합입니다. 단순히 데이터를 읽고 쓰는 행위를 넘어, 관계형 모델(Relational Model)에 기반하여 집합(Set) 단위로 데이터를 처리하는 수학적 엔진의 사용자 인터페이스(UI) 역할을 합니다. 이는 DDL (Data Definition Language)이 데이터의 구조(Structure)를 정의하는 '설계도'라면, DML은 그 설계도 위에서 실제 작업을 수행하는 '시공사'에 비유할 수 있습니다.

DML의 등장 배경은 파일 시스템(File System) 기반의 데이터 처리가 가진 **데이터 중복(Data Redundancy)**, **불일치(Inconsistency)**, **접근 비효율성**을 해결하기 위한 것입니다. 사용자는 물리적 저장소의 복잡성을 알 필요 없이 논리적인 집합 연산을 통해 데이터를 다룰 수 있게 되었으며, 특히 **트랜잭션(Transaction)** 개념이 결합되면서 은행 송금과 같이 데이터의 무결성이 생명인 현대 비즈니스 시스템의 근간이 되었습니다.

#### 💡 핵심 용어 및 약어
- **DML (Data Manipulation Language)**: 데이터 조작 언어로, 데이터를 조회, 삽입, 수정, 삭제하는 언어.
- **SQL (Structured Query Language)**: 구조화된 질의 언어로, RDBMS에서 표준으로 사용하는 언어.
- **DBMS (Database Management System)**: 데이터베이스를 관리하는 소프트웨어 시스템.
- **ACID (Atomicity, Consistency, Isolation, Durability)**: 트랜잭션이 안전하게 수행되기 위해 보장해야 할 4가지 속성.

#### 📢 섹션 요약 비유
DML은 건물이 지어진 후(DDL 완료) 입주자가 살아가는 모든 생활 양식입니다. 짐을 들여놓고(INSERT), 가구를 배치하고(UPDATE), 쓰레기를 버리며(DELETE), 필요한 물건을 찾는(SELECT) 과정 자체이며, 이 모든 과정은 펜션 주인의 관리 규칙(트랜잭션) 아래 안전하게 보호받습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,200자+]

DML의 기능은 크게 조회와 갱신으로 나뉩니다. 조회는 DBMS의 버퍼 관리자(Buffer Manager)로부터 데이터 페이지를 불러와 결과를 반환하는 과정이며, 갱신(Insert/Update/Delete)은 훨씬 복잡한 **로깅(Logging)**과 **락킹(Locking)** 메커니즘이 수반됩니다.

#### 1. DML 주요 명령어 및 동작 매커니즘

| 명령어 (Command) | 기능 (Function) | 내부 동작 원리 (Internal Mechanism) | 트랜잭션 로깅 |
|:---:|:---|:---|:---:|
| **SELECT** | 데이터 조회 | 인덱스 스캔(Index Scan) 또는 풀 테이블 스캔(Full Table Scan)을 통해 Buffer Pool의 데이터 페이지를 읽어 메모리에 로드. Lock(S) Shared Lock 발생. | 불필요 (No Logging) |
| **INSERT** | 데이터 생성 | 새로운 튜플(Tuple) 생성 → Free List 또는 PFS(Page Free Space)를 참조하여 빈 페이지 확보 → Redo Log 기록 → Undo Log(삭제 로그) 기록 | Redo + Undo |
| **UPDATE** | 데이터 수정 | 기존 데이터에 Lock(X) 획득 → Redo Log(변경 전/후 이미지) 기록 → Undo Log(변경 전 이미지) 기록 → 버퍼 페이지 수정 | Redo + Undo |
| **DELETE** | 데이터 삭제 | 삭제 대상 튜플에 Lock(X) 획득 → Redo Log 기록 → Undo Log(삽입 로그) 기록 → 페이지에서 행을 삭제(마킹) 처리 | Redo + Undo |

#### 2. DML 실행 구조 및 로그 기반 아키텍처

DML문이 실행되면 데이터는 즉시 디스크(Data File)에 기록되지 않고, 먼저 메모리 상의 **Buffer Pool**에 존재하는 데이터 페이지(Page)를 수정합니다. 이데이터 변경 사항은 순차적 쓰기가 가능한 디스크의 **Log File**에 먼저 기록되어(WAL, Write-Ahead Logging), 시스템 장애 발생 시 복구가 가능하도록 합니다.

```text
[ DML Processing Architecture & Log Flow ]

   Client (App)
      │
      ▼ SQL Command
  ┌─────────────────────────────────────────────────────┐
  │              SQL Parser & Optimizer                 │
  │  - Parse Syntax  - Create Execution Plan            │
  └──────────────────────────┬──────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     [ SELECT Path ]                [ UPDATE Path (DML) ]
              │                             │
              ▼                             ▼
    ┌─────────────────┐       ┌─────────────────────────────┐
    │   Buffer Pool   │       │    Transaction Manager (TX) │
    │  (Shared Mem)   │       │    - Acquire Lock (X/S)     │
    │                 │       │    - Generate LSN           │
    │ [Data Page]     │       └─────────────┬───────────────┘
    │   Read ────────▶│                     │
    └─────────────────┘                     ▼
                                    ┌───────────────────────┐
                                    │   Log Manager (WAL)    │
                                    │                       │
                                    │  ┌─────────────────┐   │
                                    │  │  Log Buffer     │   │
                                    │  │  (Seq Write)    │   │
                                    │  └────────┬────────┘   │
                                    └───────────┼────────────┘
                                                │
                      ┌─────────────────────────┴─────────────────────┐
                      ▼ (File System / OS I/O)                        ▼
               ┌──────────────┐                              ┌──────────────┐
               │  Redo Log    │                              │    Data     │
               │  (Sequential)│                              │    File     │
               │  (Fast I/O)  │                              │ (Random I/O)│
               └──────────────┘                              └──────────────┘
```

**다이어그램 해설**:
1.  **요청 및 분석**: 사용자의 DML 요청은 파서(Parser)와 옵티마이저(Optimizer)를 거쳐 실행 계획을 수립합니다.
2.  **트랜잭션 관리**: 갱신 연산(Insert/Update/Delete)은 트랜잭션 관리자의 제어를 받아 적절한 Lock을 획득합니다.
3.  **로그 기반 수정 (WAL)**: 데이터 파일(Random Access)에 바로 쓰는 것은 느리기 때문에, 먼저 메모리의 로그 버퍼에 변경 사항을 기록하고, 이를 순차적으로 디스크의 Redo Log에 기록합니다. 이를 **WAL (Write-Ahead Logging)** 원칙이라 합니다.
4.  **버퍼 관리**: 실제 데이터 페이지는 메모리 Buffer Pool에서 수정(Dirty Page로 마킹)되며, 필요한 시점(Checkpoint)에 디스크의 데이터 파일으로 반영됩니다.

#### 3. 트랜잭션 제어 언어 (TCL)와의 결합
DML은 단독으로 쓰이기보다 TCL (Transaction Control Language)과 결합하여 원자성을 보장합니다.
*   **COMMIT**: Redo Log를 디스크에 영구화하고, Lock을 해제하며, 수정된 페이지를 사용 가능한 상태로 변경.
*   **ROLLBACK**: Undo Log를 읽어 메모리 상의 데이터 페이지를 변경 전 상태로 복원(Restore)하고, Lock을 해제.

#### 📢 섹션 요약 비유
DML의 UPDATE 과정은 **'도서관에서 책을 수정하는 과정'**과 같습니다. 먼저 사서로부터 책(데이터 페이지)을 빌려와(Lock) 메모리(Buffer)에 두고, 수정사항을 별도의 수정일지(Log)에 먼저 기록합니다(WAL). 그 후 책 내용을 수정하고, 대출 시간이 다 되거나 작업을 마치면(COMMIT) 비로소 책장에 반납합니다. 이때 수정일지가 없었다면, 실수로 페이지를 찢었을 때 복구할 수 없겠죠.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [800자+]

DML의 성능과 특성은 OS의 파일 시스템 및 하드웨어와 깊은 연관이 있습니다.

#### 1. 심층 기술 비교: DML vs File System I/O

| 비교 항목 | DML (RDBMS 환경) | File System I/O (OS 레벨) |
|:---|:---|:---|
| **접근 단위** | **논리적 단위** (Record/Tuple, Set) | **물리적 단위** (File, Block) |
| **구조 의존성** | 스키마(Schema)에 종속적 | 구조 독립적 (Byte Stream) |
| **데이터 무결성** | ACID 트랜잭션 보장 (자동) | 애플리케이션 구현 필요 (수동) |
| **동시성 제어** | Locking, MVCC 제공 | 파일 락(Lock) 기능 제한적 |
| **성능 병목** | 로그 기록(Logging) 및 Lock 경합 | 디스크 헤드 이동(Seek) 지연 |

#### 2. OS 및 하드웨어 융합 관점
DML의 `INSERT`나 `UPDATE` 연산이 많은 시스템에서는 DBMS가 OS의 파일 시스템 캐시(OS Page Cache)를 우회하여 **Direct I/O**를 사용하는 경우가 많습니다. 이는 이중 버퍼링(Double Buffering)으로 인한 메모리 낭비를 막고, DBMS 자체의 버퍼 풀(Buffer Pool) 전략을 따르기 위함입니다.

*   **SI (Storage Interface)**: SAN (Storage Area Network)이나 NVMe SSD와 같은 고속 스토리지는 DML의 트랜잭션 처리량(TPS, Transactions Per Second)을 결정하는 물리적 한계를 확장합니다.
*   **Write Penalty**: SSD는 쓰기 연산 시 소거(Erase) 후 쓰기(Write)가 필요하므로, DML의 `UPDATE` 빈도가 높은 환경에서는 SSD의 수명과 성능 저하(Slowdown)가 발생할 수 있어, 이를 모니터링하는 것이 중요합니다.

#### 3. SELECT vs WRITE (INSERT/UPDATE/DELETE) 특성 분석

```text
[ Resource Usage Comparison ]

     Metric (CPU/Memory/Disk)
          ▲
    High  │        ┌─────────┐
          │        │  SORT   │  (SELECT with Order By)
          │        │  HASH   │  (SELECT with Join)
          │        └─────────┘
          │       ┌───────────────┐
          │       │  SELECT (Scan)│
          │       └───────┬───────┘
          │       ┌───────┴───────┐
          │       │  DML (Write)  │  (Heavy Locking & Logging)
          │       └───────────────┘
    Low   └──────────────────────────────────▶  Latency
           OLAP (Read Heavy)      OLTP (Write Heavy)
```

**해설**:
*   **OLTP (Online Transaction Processing)**: `INSERT`, `UPDATE`, `DELETE`가 빈번한 시스템입니다. DML 연산 단건의 속도(Latency)가 중요하며, Lock 경합을 최소화하는 것이 핵심입니다.
*   **OLAP (Online Analytical Processing)**: 대량의 `SELECT` 위주의 배치 작업입니다. 복잡한 쿼리를 최적화하고 전체 테이블 스캔 시간을 줄이는 것이 핵심입니다.

#### 📢 섹션 요약 비유
DML의 갱신(UPDATE) 연산은 **'복잡한 공사 중인 도로'**와 같습니다. 도로(File System)를 직접 파는 것(OS I/O)보다는, 교통정리(Locking)를 하고 공사 일지(Log)를 작성하며, 우회도로(Redo Log)를 통해 차량을 먼저 통과시키는 고속도로 통행료 징수 시스템(DML)이 훨씬 안전하고 체계적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

실무에서 DML을 설계할 때는 단순히 문법을 맞추는 것을 넘어, 데이터 일관성과 성능의 트레이드오프를 고려해야 합니다.

#### 1. 대량 데이터 처리 실무 시나리오 (Batch Processing)

**상황**: 1000만 건의 고객 등급 데이터를 일괄 업데이트해야 할 때.
*   **나쁜 예 (Anti-Pattern)**: `UPDATE Customers SET Grade = 'VIP' WHERE Score > 10000;` (단일 트랜잭션 실행)
    *   **문제점**: 단일 트랜잭션이 너무 길어지면 **Rollback Segment**가 부족해질 수 있고, 테이블 전체에 Lock이 걸려 다른 서비스가 마비됩니다. (Lock Escalation)
*   **좋은 예 (Best Practice)**: 분할 처리 (Chunked Commit)
    *   **전략**: 5,000건씩 끊어서 처리하고 COMMIT을 수행합니다.
    *   **장점**: 트랜잭션 부하를 분산하고, Lock을 짧게 유지하며, 장애 발생 시 재시작 범위를 최소화합니다.

```sql
-- Pseudo-code for Batch Update
DECLARE @BatchSize INT = 5000;
WHILE EXISTS (SELECT 1 FROM Customers WHERE Grade = 'NORMAL' AND Score > 10000)
BEGIN
    UPDATE TOP (@BatchSize) Customers
    SET Grade = 'VIP'
    WHERE Grade = 'NORMAL' AND Score > 10000;
    
    WAIT