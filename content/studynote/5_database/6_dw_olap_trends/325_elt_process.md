+++
title = "325. ELT (Extraction, Loading, Transformation) - 클라우드 기반의 혁신"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 325
+++

# 325. ELT (Extraction, Loading, Transformation) - 클라우드 기반의 혁신

### # ELT (Extraction, Loading, Transformation)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: ELT (Extraction, Loading, Transformation)는 데이터 추출 후 즉시 변환하지 않고 목적지 시스템(Data Warehouse/Data Lake)에 원시(Raw) 상태로 적재한 뒤, 목적지 시스템의 강력한 컴퓨팅 파워를 이용해 후속 변환을 수행하는 **'적재 후 변환' 아키텍처**이다.
> 2. **가치**: 중간 변환 계층(Staging Server)을 제거하여 **ETL (Extract, Transform, Load)** 대비 로딩 속도를 획기적으로 단축(Latency 최소화)하며, 원본 데이터를 보존하여 분석 유연성(Schema-on-Read)을 극대화한다.
> 3. **융합**: MPP (Massively Parallel Processing) 기반의 클라우드 DW (예: Snowflake, Google BigQuery, Amazon Redshift)와 결합하여 분석 환경을 혁신하며, **dbt (data build tool)**와 같은 엔지니어링 프레임워크와 함께 **Modern Data Stack (MDS)**의 핵심 패러다임으로 자리 잡았다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
ELT는 데이터 통합에서 데이터를 소스로부터 추출(Extract)하여 즉시 타겟 데이터 저장소에 적재(Load)한 후, 타겟 저장소 내부에서 데이터를 변환(Transform)하는 프로세스를 의미한다. 전통적인 ETL이 데이터가 타겟에 들어가기 전에 "정제(Clean)"되는 것을 강조했다면, ELT는 데이터가 타겟에 들어간 후 "가공(Process)"되는 것을 핵심으로 한다. 이는 **SaaS (Software as a Service)** 기반의 데이터 웨어하우스가 기존 온프레미스 DBMS의 성능 한계를 넘어서는 컴퓨팅 파워와 저장소 분리(Storage-Compute Decoupling) 아키텍처를 제공함에 따라 가능해진 패러다임이다.

**2. 등장 배경 및 필요성**
① **기존 한계 (ETL의 병목)**: 전통적인 ETL은 데이터가 증가함에 따라 변환을 처리하기 위한 중간 서버의 확장이 어려웠다. 또한, 소스 시스템의 부하를 줄이기 위해 변환 로직이 매우 복잡해지는 문제가 있었다.
② **혁신적 패러다임 (Cloud Native)**: AWS S3, Azure Blob Storage와 같은 **오브젝트 스토리지 (Object Storage)**의 등장과 함께, 데이터를 미리 변환하지 않고 저장하는 비용이 저렴해졌다. 이에 따라 **Data Lake** 패턴이 등장하였고, 이를 기반으로 분석 쿼리 수행 시에만 변환을 수행하는 ELT 방식이 효율적인 것으로 입증되었다.
③ **비즈니스 요구 (Agility)**: 비즈니스 환경이 빠르게 변화함에 따라, 미리 스키마를 정의(Structured)하기보다 데이터를 먼저 확보하고 필요에 따라 유연하게 스키마를 적용하는 **Schema-on-Read** 방식이 선호되게 되었다.

> **📢 섹션 요약 비유**: ELT는 마치 **'이사 당일 박스 채로 넣고, 나중에 정리하는 방식'**과 같습니다. 이사 짐을 처리하기 전에 미리 다 펴서 정리해서 옷장에 넣는 것(ETL)은 시간이 오래 걸리고 옷장 공간이 부족하기 마련입니다. 반면 ELT는 일단 박스 채로 집안(Data Warehouse)에 쳐박아넣어두고(Load), 나중에 필요할 때 박스를 열어 정리(Transform)하는 방식입니다. 덕분에 이사 속도는 매우 빠르고, 물건이 필요할 때마다 다른 용도로도 꺼내 쓸 수 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 동작**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 기술적 특징 (Internal Mechanism) | 주요 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **소스 시스템**<br>(Source System) | 데이터 생성 및 제공 | OLTP, ERP, SaaS 로그 등 다양한 형태의 데이터 생성. API 또는 CDC 기반으로 변경 감지. | SQL, API (REST/GraphQL), CDC | 원료 공급지 |
| **추출 계층**<br>(Extraction Layer) | 데이터 수집 | 데이터 형식 변환 없이 그대로 추출. 증분 로드(Incremental Load) 및 전체 로드 지원. | JDBC/ODBC, Replication Slot | 운송 트럭 |
| **적재처 (Raw)**<br>(Landing Zone) | 원천 데이터 보관 | 데이터 구조를 가공하지 않은 원본(Raw) 저장. JSON, Parquet 등의 포맷으로 저장. | **S3 (Simple Storage Service)**,<br>**ADLS (Azure Data Lake Storage)** | 창고 (Raw) |
| **변환 엔진**<br>(In-DB Transform) | 데이터 가공 | 타겟 DW의 리소스를 사용하여 SQL 기반으로 대규모 병렬 처리. | SQL (Standard/Procedural) | 정리 작업반 |
| **데이터 웨어하우스**<br>(Target DW) | 최종 저장 및 제공 | BI 도구가 조회하는 정제된 데이터 저장. 컬럼러 스토리지 기반 초고속 검색. | **MPP (Massively Parallel Processing)** | 진열장 |

**2. 아키텍처 데이터 흐름도**

ELT 아키텍처의 가장 큰 특징은 변환(Transformation) 로직의 소유권이 중간 서버에서 타겟 데이터베이스로 이동했다는 점이다. 아래 다이어그램은 데이터가 소스에서 추출되어 스토리지에 쌓이고, 이후 컴퓨팅 자원에 의해 가공되는 과정을 도시화한 것이다.

```text
[ ELT Architecture & Data Flow Diagram ]

1. Extraction & Loading Phase (High Throughput)
┌─────────────────────┐          ┌─────────────────────────────────────────┐
│   Source Systems    │          │   Cloud Storage / Data Lake (Raw Zone)  │
│                     │          │                                         │
│  [ RDBMS (SaaS) ]   │ ────(E)──▶│  ┌─────────────────────────────────┐   │
│  [ Flat Files ]     │          │  │  File_20231025.json (Original)   │   │
│  [ API Logs ]       │ ────(E)──▶│  ├─────────────────────────────────┤   │
└─────────────────────┘          │  │  Table_B_CDC.log (Raw Schema)   │   │
                                 │  └─────────────────────────────────┘   │
                                 └─────────────────────────────────────────┘
                                                 │
                                                 │ (T: In-Database Processing)
                                                 ▼
2. Transformation Phase (Compute Isolated)
                                 ┌─────────────────────────────────────────┐
                                 │   Compute Engine (MPP Cluster)          │
                                 │                                         │
                                 │   [ SELECT ..., CASE, ... GROUP BY ]    │
◀────────────────────────────────│   ────────────────────────────────▶   │
      (SQL Execution)             │   Transform Logic (Stored Procedures)  │
                                 └─────────────────────────────────────────┘
                                                 │
                                                 ▼
                                 ┌─────────────────────────────────────────┐
                                 │   Structured Data (Refined Zone)        │
                                 │   [ Analytics Ready Views ]              │
                                 └─────────────────────────────────────────┘
```

*도해 설명:*
1.  **Extract & Load**: 데이터 소스에서 네트워크를 통해 데이터를 끌어옵니다. 이때 데이터의 무결성 검사는 기본적으로 수행하지만, 비즈니스 로직에 따른 가공(Transform) 없이 **Object Storage**에 '원본 그대로' 던져 넣습니다. 이 단계에서 I/O 병목이 최소화됩니다.
2.  **Transform**: 데이터 분석가나 엔지니어가 쿼리를 요청하면, 혹은 스케줄러에 의해 트리거되면 **Compute Instance**들이 스토리지에서 원본 데이터를 읽어와 메모리에 올립니다. 이때 **MPP (Massively Parallel Processing)** 방식을 사용하여 수천 개의 노드가 동시에 데이터를 가공합니다.
3.  **Serve**: 가공된 데이터는 다시 스토리지의 별도 영역(Silver/Gold Layer)에 저장되거나, 사용자에게 즉시 쿼리 결과로 반환됩니다.

**3. 심층 동작 원리 (In-Database Transformation)**

ELT의 핵심은 "데이터를 가공하는 코드가 데이터가 있는 곳으로 이동한다"는 것이다.
① **스토리지와 컴퓨팅의 분리 (Decoupling)**: 클라우드 DW(예: Snowflake, BigQuery)는 데이터를 저장하는 스토리지와 데이터를 연산하는 CPU/Memory 자원이 분리되어 있다. 따라서 데이터를 옮길 필요 없이, 필요한 순간에만 컴퓨팅 파워를 확장(Scale-up)하여 변환 작업을 수행하고, 작업이 끝나면 다시 축소(Scale-down)할 수 있다.
② **병렬 처리 (Parallelism)**: ELT의 변환 단계는 주로 SQL 문으로 작성된다. 예를 들어, `CREATE TABLE target AS SELECT * FROM source`와 같은 문장은 데이터베이스 옵티마이저에 의해 자동으로 수백 개의 작업 조각으로 쪼개지며, 각 노드에서 동시에 실행된다.
③ **반복 가능성 (Idempotency)**: 소스 데이터가 타겟 시스템 내부에 원본 상태로 보존되어 있기 때문에, 변환 로직에 버그가 있거나 분석 요건이 변경되어도 소스 시스템에 다시 요청할 필요 없이 타겟 내의 데이터를 다시 로드(Reload)하여 변환 로직만 수정하면 된다.

**4. 핵심 알고리즘 및 코드 (SQL 중심 변환)**

ELT에서의 변환은 복잡한 ETL 스크립트(Python/Java)가 아닌, 데이터베이스 최적화된 SQL(SQL: Structured Query Language)이 주를 이룬다.

```sql
-- ELT Transform Example: dbt (data build tool) style SQL Model
-- 목적: 원천 로그 테이블(raw_events)에서 일일 활성 사용자(DAU) 집계 테이블 생성

{{
    config(
        materialized='table', -- 결과를 물리적 테이블로 생성
        schema='analytics'    -- 분석용 스키마에 저장
    )
}}

WITH source_data AS (
    -- 1. 원본 데이터 추출 (Raw Zone)
    SELECT
        user_id,
        event_timestamp,
        event_type
    FROM {{ source('raw_data', 'events') }}
    WHERE event_timestamp >= DATEADD(day, -1, CURRENT_DATE())
),

cleaned_data AS (
    -- 2. 데이터 정제 및 변환 (Business Logic)
    SELECT
        user_id,
        DATE_TRUNC('day', event_timestamp) as activity_date
    FROM source_data
    WHERE event_type = 'login' -- 로그인 이벤트만 필터링
      AND user_id IS NOT NULL  -- 결측치 제거
)

-- 3. 최종 집계 (Aggregation)
SELECT
    activity_date,
    COUNT(DISTINCT user_id) as daily_active_users
FROM cleaned_data
GROUP BY 1
ORDER BY 1 DESC;
```

> **📢 섹션 요약 비유**: ELT는 **'고속도로 요금소의 하이패스 시스템'**과 같습니다. 과거에는 톨게이트에서 일일히 현금을 걷고(중간 변환) 차량을 통과시키느라 병목이 있었다면, ELT는 차량이 그냥 무조건 달리게 두고(Load), 나중에 중앙 센터에서 한꺼번에 정산 처리(Transform)하는 방식입니다. 덕분에 도로(데이터 파이프라인)의 흐름은 막히지 않고 처리 속도는 비약적으로 빨라집니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 심층 비교: ETL vs ELT**

| 비교 항목 | **ETL (Extract, Transform, Load)** | **ELT (Extract, Load, Transform)** |
|:---|:---|:---|
| **데이터 처리 순서** | Extract → **Transform (Staging)** → Load | Extract → **Load** → **Transform (Target)** |
| **변환 로직 위치** | 중간 서버 (ETL Server / ETL Tool) | **타겟 데이터베이스 내부** |
| **데이터 적재 형태** | 비즈니스 요구에 맞게 가공된 상태로 적재 | **원시 데이터(Raw Data)** 상태로 적재 |
| **스키마 전략** | **Schema-on-Write** (쓰기 시 스키마 적용) | **Schema-on-Read** (읽기 시 스키마 적용) |
| **컴퓨팅 자원** | 변환을 위한 별도 하드웨어 필요 (Up-front Cost) | 클라우드 DW의 탄력적 컴퓨팅 활용 (Pay-per-use) |
| **데이터 유연성** | 낮음 (변환 후 재가공 어려움) | 높음 (원본 보존으로 언제든 재변환 가능) |
| **주요 사용 사례** | 온프레미스 중심, 데이터 이동이 적은 정형 처리 | 클라우드 기반, 빅데이터, 비정형/반정형 데이터 포함 |

**2. 타 과목 및 기술 융합 관점**

① **운영체제 (OS) 및 컴퓨터 구조와의 시너지**
ELT가 가능해진 근본적인 이유는 컴퓨터 구조의 진화에 있다. 기존 **OLTP (Online Transaction Processing)** 환경에서는 데이터 처리가 I/O Bound였으나, 클라우드 환경에서는 **NUMA (Non-Uniform Memory Access)** 구조의 대규모 메모리와 **NVMe SSD**를 통해 네트워크 대역폭만 확보된다면 I/O 병목 없이 즉시 적재가 가능하다. 또한, OS 레벨의 컨테이너화 기술(Docker/Kubernetes)은 변환 작업을 위한 컴퓨팅 노드를 순간적으로 띄우고 내리는 것을 가능하게 하여 ELT의 효율성을 높인다.

② **네트워크 및 보안 (Security)과의 상관관계**
*   **네트워크 비용**: 데이터를 클라우드로 한 번만 옮기면 되므로(AWS Direct Access 등), 중간 서버를 거치는 트래픽을 줄일 수 있다.
*   **보안**: 원천 데이터가 그대로 타겟에 저장되므로 **Encryption at Rest** 및 **Column-Level Security**가 필수적이다. 민감 정보(PII)를 마스킹하는 로직이 적재 *전*이 아닌 *후*에 일