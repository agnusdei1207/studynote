+++
title = "21. DML (Data Manipulation Language)"
date = "2026-03-15"
weight = 21
[extra]
categories = ["Database"]
tags = ["DML", "Data Manipulation Language", "SQL", "SELECT", "INSERT", "UPDATE", "DELETE", "Manipulation"]
+++

# 21. DML (Data Manipulation Language)

## # 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스 내의 데이터를 직접적으로 조회, 생성, 수정, 삭제하는 **비절차적(Non-Procedural) 언어**로, 사용자는 '어떻게(How)' 처리할지가 아닌 '무엇을(What)' 원하는지를 선언하여 결과를 얻습니다.
> 2. **아키텍처**: **DML (Data Manipulation Language)**은 **DBMS (Database Management System)**의 **Query Optimizer (쿼리 최적화기)**를 통해 실행 계획을 수립하고, **Buffer Manager (버퍼 관리자)**를 거쳐 **Storage Engine (스토리지 엔진)**과 상호작용하는 핵심 인터페이스입니다.
> 3. **가치 및 융합**: 모든 비즈니스 로직의 데이터 처리부를 담당하며, **ACID (Atomicity, Consistency, Isolation, Durability)** 트랜잭션 경계 내에서 수행되어 데이터 무결성을 보장하고 응용 프로그램의 개발 생산성을 극대화합니다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 및 철학**
**DML (Data Manipulation Language)**은 데이터베이스 사용자나 응용 프로그램이 데이터베이스에 저장된 데이터를 검색(Retrieve)하거나 갱신(Update)하기 위해 사용하는 언어입니다. **DDL (Data Definition Language)**이 데이터의 구조(스키마)를 정의하는 '정적' 언어라면, DML은 그 안의 내용물을 다루는 '동적' 언어입니다. 관계형 데이터베이스의 핵심인 **SQL (Structured Query Language)**에서 가장 빈번하게 사용되는 하위 집합입니다.

**등장 배경**
파일 시스템 기반의 초기 데이터 처리 방식은 데이터를 접근하기 위해 물리적인 주소나 인덱스 경로를 프로그래머가 일일이 명시해야 하는 **절차적(Procedural)** 방식이었습니다. 이는 데이터 구조가 조금만 변경되어도 프로그램을 전면 수정해야 하는 '데이터 종속(Data Dependence)' 문제를 야기했습니다. 이를 해결하기 위해 E.F. Codd의 관계형 모델과 함께 등장한 DML은 사용자가 데이터의 물리적 위치를 알지 못해도, 수학적 술어(Predicate)를 통해 원하는 결과 집합을 선언(Declare)만 하면 **DBMS**가 알아서 처리해 주는 **비절차적(Non-Procedural)** 선언형 언어로 발전했습니다.

**💡 비유: 스마트 창고의 물류 관리자**
데이터베이스를 거대한 '자동화 창고'라고 가정해 봅시다.
- **DDL**: 창고의 선반 위치와 구조를 설계하고 짓는 시공사 역할.
- **DML**: 창고를 사용하여 물건을 넣고 빼는 '물류 관리자' 역할.
- **사용자**: 관리자에게 "A번 선반에 있는 레고 박스를 가져다 줘"라고 요청하는 고객. 관리자는 컴퓨터 시스템을 통해 어디에 있는지(물리적 위치) 몰라도, "레고 박스(데이터 조건)"라고 말만 하면 시스템이 이를 찾아옵니다.

**📢 섹션 요약 비유**
> **마치 배달 앱을 통해 음식을 주문하는 것과 같습니다.** 우리는 '집에까지 배달해 줘'(What)라고 주문만 할 뿐, 배달 기사가 어떤 길로 운전을 하고 어떻게 주방에서 음식을 포장하는지(How)는 알지 못해도, 시스템(RDBMS)이 알아서 가장 빠르고 정확하게 처리해 줍니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

**1. DML 구성 요소 및 모듈 상세**
DML 문장 하나가 실행되기까지는 다수의 내부 컴포넌트가 유기적으로 작동합니다.

| 요소명 | 역할 | 내부 동작 메커니즘 | 주요 프로토콜/속성 | 비유 |
|:---|:---|:---|:---|:---|
| **SQL Parser** | 구문 분석 | 사용자의 SQL 문장을 토큰(Token) 단위로 분석하고 구문 오류(Syntax Error) 및 권한 여부를 체크함. | Parse Tree 생성 | 비서가 주문 내용 정리 |
| **Query Optimizer** | 실행 계획 수립 | 데이터를 조회하는 가장 효율적인 경로를 결정. **Full Table Scan** vs **Index Scan** 선택 및 조인 순서 결정. | Cost-Based Optimization (CBO) | 내비게이션 경로 탐색 |
| **Relational Engine** | 논리적 연산 수행 | 요청된 데이터를 조건에 맞게 필터링(Filtering), 정렬(Sorting), 조인(Join)하는 알고리즘 실행. | Relational Algebra | 요리사가 재료 손질 |
| **Buffer Manager** | 메모리 관리 | 데이터를 **Buffer Cache (SGA/Shared Pool)**에 적재하여 디스크 I/O를 최소화함. LRU 알고리즘 활용. | Page Replacement | 조리대(작업 공간) |
| **Transaction Manager** | 무결성 보장 | DML 실행 전후로 **Lock**을 걸어 동시성 제어 및 **Undo/Redo Log** 생성을 통해 ACID 보장. | MVCC (Multi-Version Concurrency Control) | 주문 내역 기록/관리 |

**2. DML 처리 흐름 (ASCII Architecture)**

```text
┌─────────────────── USER / APPLICATION ───────────────────┐
│                                                           │
│  SELECT ename FROM emp WHERE sal > 3000;                  │
│           ▲                                               │
│           │                                               │
└───────────┼───────────────────────────────────────────────┘
            │ (1) DML Statement Request
            ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE MANAGEMENT SYSTEM (DBMS)       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Relational Engine]         [Storage Engine]              │
│                                                             │
│  ┌─────────────┐              ┌───────────────────────┐    │
│  │   Parser    │──Syntax OK──>│   Query Optimizer     │    │
│  │ (구문 검증)  │              │  (비용 기반 최적화)    │    │
│  └─────────────┘              └───────────┬───────────┘    │
│                                          │                  │
│                               Generates Execution Plan       │
│                                          ▼                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │     Executor (Relational Engine)                     │   │
│  │  ─> Probes Buffer Cache (Memory)                     │   │
│  │  ─> If Miss? Request I/O to Storage Engine           │   │
│  └───────────────┬─────────────────────────────────────┘   │
│                  │                                         │
│                  ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Buffer Manager (Buffer Cache)                      │   │
│  │  [ LRU: Least Recently Used Algorithm ]             │   │
│  │  ─> Data Page ─> [ HIT ] ─> Return Result           │   │
│  │  ─> Data Page ─> [ MISS ] ─> Disk Access            │   │
│  └───────────────┬─────────────────────────────────────┘   │
│                  │                                         │
└──────────────────┼─────────────────────────────────────────┘
                   │ (3) Result Set
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   DISK STORAGE (Data Files)                 │
│   Table 1  │  Table 2  │  Index 1  │  Redo Log  │ Undo Log │
└─────────────────────────────────────────────────────────────┘
```

**3. 심층 동작 원리 및 코드**

DML 문장은 단순히 실행되지 않고, 커서(Context Area)를 열고 파싱(Parsing) -> 바인딩(Binding) -> 실행(Executing) -> 인출(Fetching)의 과정을 거칩니다.

*   **Parsing (Hard/Soft)**: SQL 문장의 올바름을 확인하고 최적화된 실행 계획을 생성합니다. 이전에 수행된 적이 있는 경우 **Library Cache**에서 찾아 재사용(Soft Parse)합니다.
*   **Fetch Logic**: 데이터를 한 번에 모두 가져오는 것이 아니라, 네트워크 부하를 분산시키기 위해 배열(Array) 단위로 나누어 가져옵니다.

```sql
-- [Deep Dive] DML 실행 내부 관점 (의사코드)
-- 사용자 쿼리: UPDATE employees SET salary = salary * 1.1 WHERE dept_id = 10;

BEGIN
    -- 1. Lock Acquisition (배타적 Lock - X Lock)
    -- dept_id=10 인 행에 대한 잠금 획득 (Concurrency Control)

    -- 2. Redo Log Generation (변경 전 기록 - Rollback 대비)
    WRITE_LOG(BEFORE_IMAGE, current_salary);

    -- 3. Buffer Cache Modify (Update in Memory)
    SET_BUFFER(dept_10_rows, salary, current_salary * 1.1);

    -- 4. Undo Log Generation (변경 내역 기록 - 복구 대비)
    WRITE_UNDO(AFTER_IMAGE, new_salary);

    -- 5. Commit (Transactional End)
    -- 지금까지의 변경사항을 Disk의 Redo Log File에 강제 기록(LGWR)
    -- Lock을 해제하고 다른 사용자에게 변경 내역을 공개.
    COMMIT;
END;
```

**4. DML 주요 명령어별 기술적 특징**

1.  **SELECT (Retrieve)**: 읽기 일관성(Read Consistency)을 위해 **Undo Segment**를 참조하여 특정 시점(Snapshot)의 데이터를 조회합니다. Lock을 생성하지 않거나 다른 사용자의 DML을 방해하지 않는 Non-blocking 방식이 특징입니다.
2.  **INSERT**: 새로운 데이터를 추가하며 **Redo Log**와 **Undo Log**를 모두 생성합니다. Direct-Path Insert(Append) 모드를 사용하면 Buffer Cache를 거치지 않고 데이터 파일에 직접 기록하여 대량 로드 성능을 높일 수 있습니다.
3.  **UPDATE**: 기존 데이터를 변경하며, 변경 전 이미지를 Undo에 저장하고 변경 후 이미지를 Redo에 기록합니다. 행 이동(Row Migration)이 발생할 수 있어 성능 저하의 주원인이 되기도 합니다.
4.  **DELETE**: 데이터를 논리적으로 삭제(Flagging)하며, 빈 공간(HWM, High Water Mark)을 즉시 반환하지 않는 경우가 많아 **Table Reorganization**이 필요할 수 있습니다.

**📢 섹션 요약 비유**
> **마치 정교한 조리 과정과 같습니다.** 재료(Data)를 가져오기 위해 냉장고(Storage)를 열고, 조리대(Buffer Cache)에 올려두고, 칼(Query)로 썰어(Fetch) 그릇(Result)에 담습니다. 이때 주문이 들어오면 주문서(SQL)를 확인(Parser)하고, 요리사(Optimizer)가 "가장 빠른 조리 순서"를 정한 뒤 요리를 시작합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

**1. 절차적 vs 비절차적 DML 비교**

| 구분 | 절차적 DML (Procedural) | 비절차적 DML (Non-Procedural, SQL) |
|:---|:---|:---|
| **정의** | "데이터를 *어떻게* 접근할지" 경로를 명시 | "무엇을* 원하는지* 결과만 정의 |
| **데이터 접근** | 레코드 단위 순차 접근 (Loop 필수) | 집합(Set) 단위 처리 |
| **코드 양** | 복잡하고 길음 | 간결함 |
| **최적화** | 개발자가 수동 수행 | **DBMS Optimizer**가 자동 수행 |
| **호환성** | DBMS 변경 시 코드 수정 필요 | 표준 SQL 준수 시 호환성 높음 |
| **예시** | C 언어 내 임베디드 SQL, 커서 제어 | `SELECT * FROM users WHERE age > 20;` |

**2. 기술적 시너지: OS/File System과의 관계**

DBMS의 DML은 결국 OS 파일 시스템 위에서 구동됩니다.
*   **Buffer Cache vs Page Cache**: Oracle/MySQL의 **Buffer Cache**와 OS의 **Page Cache**는 이중 버퍼링(Double Buffering) 역할을 합니다. DML이 Disk I/O를 발생시킬 때, 직접 Disk로 가는 것이 아니라 이 메모리 계층을 먼저 타격합니다.
*   **Write-Ahead Logging (WAL)**: DML의 변경 사항을 데이터 파일에 반영하기 전에 로그 파일에 먼저 기록하는 기술은 OS의 시스템 로그와 유사하지만, 트랜잭션 무결성을 위해 훨씬 엄격하게 구현됩니다. 이는 시스템 충돌(Crash) 발생 시 ACID의 D(Durability)를 보장하는 핵심입니다.

**3. 데이터 무결성과의 융합 (TCL)**
DML은 단독으로 존재할 수 없으며 반드시 **TCL (Transaction Control Language)**와 결합됩니다.
*   **Auto Commit Mode**: 각 DML 문장 실행 즉시 COMMIT되는 모드 (단순 조회 위주).
*   **Manual Commit Mode**: 트랜잭션 시작(`BEGIN`)부터 `COMMIT`/`ROLLBACK`까지의 원자성(Atomicity)을 보장. 비즈니스 로직의 핵심입니다.

**📢 섹션 요약 비유**
> **절차적 방식은 '택시 운전수에게 "우회전 후 50m 직진"하고 가르쳐주는 것'**이고, **비절차적 방식은 "KTX 역으로 가주세요"라고 목적지만 말하는 것**과 같습니다. 후자는 도로가 막혀도 알아서 우회경로를 찾아주는 똑똑한 내비게이션(Optimizer)가 있기에 가능합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

**1. 실무 시나리오: 대량 데이터 삭제 시의 성능 저하 문제**

*   **문제 상황**: 월말 정산 로직으로 인해 3년 된 로그 데이터(1억 건)를 `DELETE FROM logs WHERE reg_date < ADD_MONTHS(SYSDATE, -36);` 명령어로 삭제하려고 함.
*   **증상**: 삭제 작업 중 로그 테이블에 **Lock**이 걸려 실시간 INSERT(로그 적재)가 전면 중단되어 서비스 장애 발생. Undo Segment가 가득 차서 `Snapshot too old` 오류 발생 가능성 증가.
*   **기술사적 판단 (의사결정)**:
    1.  **DELETE의 한계**: DELETE는 DML이므로 Undo를 생성하고, 공간을 반환하지 않아 **HWM (High Water Mark)**이 내려가지 않음(조회 성능 저하 지속).
    2.  **대안 1 (DDL 활용)**: 데이터가 전체에서 80% 이상 삭제된다면 `TRUNCATE` 혹은