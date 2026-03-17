+++
title = "20. DDL (Data Definition Language)"
date = "2026-03-15"
weight = 20
[extra]
categories = ["Database"]
tags = ["DDL", "Data Definition Language", "Schema", "Metadata", "SQL", "CREATE", "ALTER", "DROP"]
+++

# 20. DDL (Data Definition Language)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스의 논리적/물리적 골격을 구축하는 **데이터 정의 언어(Data Definition Language)**로, 데이터 자체가 아닌 데이터의 구조, 제약조건, 관계를 정의하는 **메타데이터(Metadata)** 관리의 핵심 도구이다.
> 2. **무결성 강제**: DDL은 단순히 테이블을 생성하는 것을 넘어, PK/FK 제약조건을 통해 참조 무결성(Referential Integrity)을 DBMS 커널 레벨에서 물리적으로 강제하여 데이터 품질을 보장하는 최후의 방어선이다.
> 3. **시스템 카탈로그 연동**: DDL 명령어 실행은 즉시 **시스템 카탈로그(System Catalog)**, 즉 데이터 사전(Data Dictionary)을 갱신하며, 대부분의 DBMS 환경에서 트랜잭션 관리와 별개로 **자동 커밋(Auto-commit)**되어 되돌릴 수 없는 파괴적 연산을 수행한다.

---

### Ⅰ. 개요 (Context & Background)

**DDL (Data Definition Language)**은 데이터베이스 관리 시스템(RDBMS) 내에서 데이터를 저장하고 관리하기 위한 그릇(Objects)과 구조(Schema)를 정의, 수정, 삭제하는 언어 집합입니다. 이는 데이터의 내용(Content)을 다루는 DML(Data Manipulation Language)과 대비되며, 데이터의 '형식(Form)'과 '범위(Domain)'를 규정하는 데이터베이스 설계의 구현 단계입니다.

**💡 비유: 건축의 청사진과 기둥 세우기**
데이터베이스 구축을 건물 짓기에 비유한다면, DDL은 **설계도면을 바탕으로 기둥을 세우고 벽을 쌓으며 문을 설치하는 '시공 과정'**입니다. 가구(데이터)를 배치하기 전에 방의 크기와 용도를 결정하는 것과 같습니다.

#### 등장 배경 및 필요성
1.  **데이터 구조화의 필요성**: 초기 파일 시스템(File System)에서는 데이터 구조가 애플리케이션 프로그램에 종속되어 있었으나, DDL의 등장으로 **데이터 독립성(Data Independence)**을 확보하여 스키마 변경이 애플리케이션에 미치는 영향을 최소화했습니다.
2.  **데이터 무결성 보장**: 애플리케이션 레벨이 아닌 데이터베이스 엔진 레벨에서 **제약 조건(Constraint)**을 정의함으로써, 잘못된 데이터가 저장되는 것을 원천적으로 차단하고자 하는 패러다임이 도입되었습니다.
3.  **공유 저장소 관리**: 다수의 사용자와 프로그램이 데이터를 공유할 때, **시스템 카탈로그(System Catalog)**라는 중앙화된 메타데이터 저장소를 통해 일관된 구조 정보를 제공하기 위해 개발되었습니다.

```text
[ 데이터베이스 생명주기에서 DDL의 위치 ]
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  요구사항 분석 ─→  설계 (Modeling) ─→  [ 정의 (DDL) ] ─→  조작 (DML)        │
│                                         │                                   │
│                                         └──▶ 물리적 구조 생성               │
│                                             스키마(Schema) 설정             │
│                                             제약사항(Constraint) 적용       │
│                                                                             │
│  * DDL은 설계라는 추상적 개념을 실제 데이터가 저장될 '물리적 공간'으로        │
│    전환(Turning Blueprint to Reality)하는 시점임.                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 📢 섹션 요약 비유
DDL은 건물을 지을 때 '철근을 배치하고 콘크리트를 부어 형태를 잡는 틀(Frame)'을 만드는 과정과 같습니다. 틀이 잘못되면 아무리 좋은 가구(데이터)를 들여놓아도 건물이 무너지거나 사용할 수 없게 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

DDL의 핵심은 **객체(Object)의 생명주기 관리**와 **메타데이터 갱신**입니다. DDL 명령어는 사용자의 질의를 SQL 파서(Parser)가 분석한 후, Optimizer를 거쳐 **Storage Engine**으로 전달되어 물리적 파일을 생성하거나 수정합니다.

#### 1. 주요 명령어 및 구성 요소 상세

| 명령어 | 기능 | 내부 동작 메커니즘 (Internal Mechanism) | Transaction 특성 |
|:---:|:---|:---|:---|
| **CREATE** | 객체 생성 | 시스템 카탈로그에 메타데이터 삽입<br>물리적 디스크 공간(Extent) 할당 | **Implicit Commit**<br>(이전 트랜잭션 종료 후 실행) |
| **ALTER** | 구조 수정 | 카탈로그 정보 갱신<br>기존 데이터 마이그레이션(Migration) 또는 Lock<br>컬럼 추가/삭제/타입 변경 | **Implicit Commit** |
| **DROP** | 객체 삭제 | 카탈로그 정보 삭제<br>물리적 데이터 파일와 공간 해제<br>Rollback 불가능 | **Implicit Commit** |
| **TRUNCATE**| 데이터 삭제 | 테이블 구조 유지, 모든 Row 삭제<br>High-watermark(HWM) 초기화<br>Redo Log 생성 최소화 | **Implicit Commit** |
| **RENAME** | 이름 변경 | 카탈로그 내 객체 식별자(Object ID)의<br>논리적 이름 매핑만 변경 | **Implicit Commit** |

#### 2. DDL 수행 프로세스 및 시스템 카탈로그 (Data Dictionary)

DDL이 실행되면 가장 먼저 변하는 것은 데이터 파일이 아니라 **시스템 카탈로그(System Catalog)**입니다. 이것은 데이터베이스에 대한 '데이터(Define Data)'이므로 **메타데이터(Metadata)**라고 합니다.

```text
    [User SQL]              [DBMS Kernel]                  [Storage]
       │                          │                            │
       │  CREATE TABLE t1...      │                            │
       ├────────────────────────▶│ 1. Syntax Check             │
       │                          │ 2. Security Check          │
       │                          │ 3. Dictionary Update ──────┼──▶ [SYSTEM CATALOG]
       │                          │    (Metadata Insert)       │    - Table Name
       │                          │                            │    - Columns (Type, Len)
       │                          │                            │    - Constraints (PK/FK)
       │                          │ 4. Storage Allocation      │
       │                          ├────────────────────────────┼──▶ [DATA FILE]
       │                          │                            │    (Empty Extent Alloc)
       ▼                          ▼                            ▼
    [Commit] ──────────────────────────────────────────────────▶
    (Auto Commit)             ↳ 성공 시 반환
```

#### 3. 핵심 알고리즘: 제약 조건(Constraint)의 논리적 연결
DDL의 진정한 힘은 데이터 구조 정의를 넘어 **무결성 제약조건(Integrity Constraint)**을 설정하는 데 있습니다. 관계형 데이터베이스의 핵심인 **PK (Primary Key)**와 **FK (Foreign Key)** 정의 시 내부적으로 무결성을 검증합니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Integrity Constraint Validation Flow                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Table A: PARENT]                 [Table B: CHILD]                         │
│  ┌─────────────────────┐           ┌─────────────────────┐                 │
│  │ PK_ID (PRIMARY KEY) │◀──────┐   │ FK_ID (FOREIGN KEY) │                 │
│  │ 1                   │       │   │ 1 (Valid)           │                 │
│  │ 2                   │       │   │ 3 (Valid)           │                 │
│  └─────────────────────┘       │   │ 99 (Orphan)         │                 │
│                                │   └─────────────────────┘                 │
│  [DDL Execution]               │                                            │
│  ALTER TABLE CHILD             │                                            │
│  ADD CONSTRAINT fk_child       │            [Validation Mechanism]          │
│  FOREIGN KEY (fk_id)           │                                            │
│  REFERENCES parent(pk_id)      │                                            │
│                                │                                            │
│   ▼                            │                                            │
│  1. Lock Parent Table (Shared) │                                            │
│  2. Scan Child Table Rows     ─┼──▶ 99가 Parent에 없음!                    │
│  3. Compare Values             │                                            │
│  4. If Mismatch → ROLLBACK DDL │                                            │
│     (Orphan Data Detected)     │                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
*해설*: 위 다이어그램은 FK 제약조건 추가 시 발생하는 **참조 무결성 검증** 과정입니다. 만약 `CHILD` 테이블에 `PARENT` 테이블에 없는 값(예: 99)이 존재한다면, DDL 실행은 즉시 실패하거나 DBMS는 기존 불일치 데이터를 정리하라는 경고를 발생시킵니다.

#### 📢 섹션 요약 비유
DDL 명령어 실행은 건물의 **등기부등본(시스템 카탈로그)**을 먼저 수정하고, 그에 따라 실제 땅(디스크)에 울타리를 치는 과정입니다. 단순히 땅을 파는 것이 아니라, "이곳은 공장만 지을 수 있다"는 법적 제약(Constraint)을 국가 시스템에 등록하는 강력한 행위입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

DDL은 단독으로 존재하지 않으며 DML(Data Manipulation Language), DCL(Data Control Language) 및 운영체제(OS)의 파일 시스템과 긴밀히 상호작용합니다.

#### 1. SQL 명령어군 계층별 비교 분석

| 구분 | DDL (정의) | DML (조작) | DCL (제어) | TCL (트랜잭션) |
|:---:|:---|:---|:---|:---|
| **핵심 기능** | **구조 정의**<br>Schema, Object | **데이터 처리**<br>CRUD Operation | **권한/보안**<br>Grant, Revoke | **논리적 단위**<br>Commit, Rollback |
| **대상** | Metadata<br>(System Catalog) | User Data<br>(Data Files) | Users/Roles | Transaction Block |
| **Commit 특성**| **Auto Commit**<br>(즉시 반영) | **Manual Commit**<br>(필요시) | **Auto Commit** | **Manual** |
| **Rollback** | **불가능** (대부분) | **가능** | **불가능** | **가능** |

#### 2. 기술적 융합: 데이터 독립성 성취
DDL의 가장 중요한 가치는 **Logical Schema(논리적 스키마)**를 통해 **Physical Schema(물리적 스키마)**를 분리하는 데 있습니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Data Independence via DDL (View)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Application Layer]                                                       │
│       │                                                                     │
│       │  SELECT * FROM emp_active;  (Logical View)                          │
│       │                                                                     │
│       ▼                                                                     │
│  [Logical Layer (DDL Definition)]                                          │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │  VIEW: emp_active                                         │             │
│  │  AS SELECT * FROM employees WHERE status = 'ACTIVE';       │             │
│  └───────────────────────────────────────────────────────────┘             │
│       │                                                                     │
│       │  (Transparent Mapping)                                              │
│       │                                                                     │
│       ▼                                                                     │
│  [Physical Layer (Storage)]                                                │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │  Table: employees (Partitioned by Year)                    │             │
│  │  - 2023_Data (Tablespace A)    │  - 2024_Data (Tablespace B)│            │
│  └───────────────────────────────────────────────────────────┘             │
│                                                                             │
│  → 사용자는 'emp_active'라는 가상 테이블(DDL로 정의된)을 조회하지만,         │
│    실제로는 물리적으로 분할된 여러 파티션(Partition)에서 데이터를 가져옵니다. │
│    즉, 물리적 구조 변경이 애플리케이션 논리에 영향을 주지 않습니다.          │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 📢 섹션 요약 비유
DDL은 애플리케이션(운전자)과 데이터(도로) 사이의 **내비게이션 인터페이스**와 같습니다. 도로의 물리적 차선이 변경되더라도(Physical 변경), 내비게이션 지도(View)가 업데이트되면 운전자는 같은 경로를 편리하게 이용할 수 있습니다. 즉, **변화를 캡슐화하는 완충지대** 역할을 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 DDL은 데이터베이스의 **가용성(Availability)**과 **성능(Performance)**에 직접적인 영향을 미치는 고위험 작업입니다. 특히 운영 중인 시스템(Live System)에서의 DDL 실행은 신중한 전략이 요구됩니다.

#### 1. 실무 시나리오: 대용량 테이블 스키마 변경 (Schema Migration)

**문제 상황**: 
전자상거래 주문 테이블(`Orders`)에 5,000만 건의 데이터가 적재되어 있습니다. 마케팅 팀의 요청으로 주문자의 채널 정보(`channel_id VARCHAR(20)`) 컬럼을 신규 추가해야 합니다.

**기술사적 판단 및 의사결정 프로세스**:
1.  **Lock 분석**: 일반적인 `ALTER TABLE ... ADD COLUMN` 구문 실행 시, DBMS는 테이블 전체에 **MDL(Metadata Lock)** 또는 배타적 잠금(Exclusive Lock)을 획득하여 모든 DML(입력/수정/삭제)을 차단할 수 있습니다. 5,000만 건이라면 테이블 재구성(Rewrite)이 발생하여 수분에서 수시간까지 서비스가 중단될 수 있습니다.
2.  **전략 수립 (3가지 방안)**:
    *   **A. 정기 점검 시간 작업**: 서비스를 중단하고 DDL 실행. (가장 안전하지만 가용성 손실)
    *   **B. Online DDL 활용**: MySQL의 `ALGORITHM=INPLACE, LOCK=NONE` 또는 Oracle의 `Online Redefinition` 기능을 사용하여 테이블 재작성 없이 즉시 메타데이터만 변경.
    *   **C. pt-online-schema-change (도구 활용)**: 트리거(Trigger)를 이용해 원본 테이블과 동기화하며 사본