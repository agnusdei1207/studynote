---
title: "Cloud Data Lake Architecture Design"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 634
---
```markdown
# 634. 클라우드 데이터 레이크 아키텍처 설계 (Cloud Data Lake Architecture Design)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Object Storage(S3/ADLS/GCS) 기반의 **Schema-on-Read** 원리와, **컴퓨트-스토리지 분리(Decoupled Storage-Compute)**, 그리고 **ACID 트랜잭션을 지원하는 Open Table Format(Delta Lake, Apache Iceberg, Apache Hudi)**의 결합을 통해 페타바이트급 정형·반정형·비정형 데이터를 통합 저장·처리하는 계층형(Medallion) 분석 플랫폼이다.
> 2. **가치**: 동일한 데이터 카피본 없이 다중 분석 엔진(Spark, Trino, Snowflake, Athena, EMR, Databricks SQL, dbt)이 동시 접근하는 **"One Copy, Many Workloads"** 구조로, 데이터 사일로 제거, 분석 시간 70% 단축, 스토리지 비용 80% 절감(컬럼형 변환·압축·Lifecycle 정책 적용 시)의 정량적 효과를 제공한다.
> 3. **판단 포인트**: "데이터 늪(Data Swamp) 회피"가 핵심이며, **레이크 vs 레이크하우스 vs 데이터 메시(Data Mesh)**, **배치·마이크로배치·스트리밍 통합**, **메타데이터 카탈로그 거버넌스**, **멀티 클라우드/하이브리드 인터옵**, **Privacy & Sovereignty 컴플라이언스**(GDPR, 개인정보보호법) 설계가 실무자의 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전 세계 데이터 생성량은 2025년 약 180ZB에 달하며, IDC는 "데이터의 80% 이상이 비정형·반정형이며, 그중 90%는 분석·활용되지 않는다"고 보고했다. 전통적인 엔터프라이즈 데이터 웨어하우스(EDW)는 **Schema-on-Write, 수직 확장(SMP), ETL 기반 정형 데이터 전용**이라는 한계로 인해 ①IoT·로그·이미지·텍스트·스트림 데이터의 폭증, ②분석 요구사항의 빠른 변화(agile analytics), ③데이터 사이언티스트의 자유로운 탐색(Exploratory Data Analysis) 요구를 수용하지 못했다.

이에 등장한 **클라우드 데이터 레이크**는 "원시 데이터를 가장 거친 형태(Raw)로 무제한 저장하고, 분석 시점에 스키마를 적용(Schema-on-Read)"하는 James Dixon의 2010년 컨셉을, 오브젝트 스토리지의 저가·무한 확장성과 오픈 테이블 포맷의 트랜잭션·시간여행(Time Travel) 기능으로 산업화한 것이다. 최근에는 단순 레이크를 넘어, **레이크하우스(Lakehouse)** 와 **데이터 메시(Data Mesh)** 패러다임이 융합되며 거버넌스·도메인 자율성·AI 네이티브 분석을 동시에 만족시키는 진화형 아키텍처로 자리 잡고 있다.

```text
[기존 DW vs Modern Data Lake - 패러다임 비교]

   +-----------------------+                    +------------------------------------+
   |  Traditional EDW      |                    |  Modern Cloud Data Lake            |
   +-----------------------+    ------►         +------------------------------------+
   | Sources: ERP/CRM only |                    | Sources: ALL (Batch/Micro/Stream)  |
   | ETL -> Cleansed -> DW   |                    | Ingest Raw -> Bronze/Silver/Gold    |
   | Schema-on-Write       |                    | Schema-on-Read + ACID (Iceberg)    |
   | Proprietary Engine    |                    | Open Formats + Open Engines        |
   | Vertical Scale-up     |                    | Decoupled Storage-Compute (S3+)    |
   | Cost: $20K/TB/yr      |                    | Cost: $200/TB/yr (Hot) ~$12/TB(Glacier)
   | Time-to-Insight: Wks  |                    | Time-to-Insight: Mins~Hrs          |
   +-----------------------+                    +------------------------------------+

   [ 데이터 폭증 트래픽 (일일 평균) ]
   +----------+
   | IoT 센서 | -- 1.2 TB/일 --+
   | 앱 로그  | -- 850 GB/일 --+--► [Kafka/Kinesis] --► [Bronze Raw Zone]
   | API 호출 | -- 320 GB/일 --+                            |
   | CRM/ERP  | -- 180 GB/일 --+                            v
   | 이미지   | -- 4.5 TB/일 --► [S3 Raw]         [Schema-on-Read Engine]
   +----------+                                            |
                                                           v
                                                  [BI/ML/AI Workloads]
```

**왜 필요한가? — 비즈니스 트리거**
- **Cost Pressure**: 1TB당 온프레미스 DW 유지비용 18,000~25,000 USD/yr -> 오브젝트 스토리지 + 콜드 스토리지(S3 Glacier/ADLS Archive) 기반 시 1,000 USD/yr 이하로 하락.
- **Time-to-Market**: 신규 분석 모델 요구 발생 시 ETL 파이프라인 재설계 불필요(스키마 진화 지원), **셀프서비스 분석** 가능.
- **AI/ML 워크로드 통합**: 학습용 피처 스토어(Feature Store: Feast, Tecton, Databricks Feature Store)와 데이터 레이크가 동일 스토리지를 공유 -> **Data -> Feature -> Model -> Inference** 루프 단축.
- **규제 대응**: GDPR/개인정보보호법상 삭제권(Right to Erasure) 충족을 위해 단일 카피본에서 컬럼 단위 파티션 + Iceberg Hidden Partition + Time Travel 기반 Soft Delete + Compaction로 일관 처리.

- **📢 섹션 요약 비유**: 데이터 레이크는 "**보물창고**"와 같다. 정리가 안 된 물건도 모두 던져 넣을 수 있고(원시 데이터 무제한 수집), 필요할 때 어떤 돋보기(쿼리 엔진)로든 들여다볼 수 있으며, 보물 분류대(메타데이터 카탈로그)가 비로소 "쓰레기 창고(Data Swamp)"가 되지 않게 지켜준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 계층형(Medallion) 아키텍처 — Bronze / Silver / Gold

Databricks가 2019년 제안한 **Medallion Architecture**는 데이터 품질·정제 수준에 따라 레이크를 3개 논리적 존(Zone)으로 분리한다. 동일 S3 버킷 내 prefix(`s3://lake/bronze/`, `/silver/`, `/gold/`)로 구현되며, **불변성(Immutability)** 과 **단계적 정제(Progressive Refinement)** 원칙을 따른다.

```text
[ Cloud Data Lake - 계층형 아키텍처 전체 흐름도 ]

  +---------------------------------------------------------------------------------------------+
  |                                    INGESTION LAYER                                          |
  |  +----------+  +----------+  +----------+  +----------+  +----------+  +----------+         |
  |  | RDBMS    |  | SaaS API |  | IoT MQTT |  | App Logs |  | Image/   |  | CDC      |         |
  |  | (CDC)    |  | (REST)   |  | (Sensor) |  | (Filebeat)| | Video    |  | (Debezium)|        |
  |  +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+-----+  +----+-----+         |
  |       |             |             |             |             |             |                |
  |       v             v             v             v             v             v                |
  |  +--------------------------------------------------------------------------------------+    |
  |  |    Apache Kafka / Amazon Kinesis / Azure Event Hubs / Pub/Sub   (Streaming)         |    |
  |  |    +   AWS DMS / DMS SCT / Fivetran / Airbyte / Spark Structured Streaming (Batch) |    |
  |  +--------------------------------------------------------------------------------------+    |
  +--------------------------------------+--------------------------------------------------+
                                         |
                       +-----------------+-----------------+
                       v                                   v
  +--------------------------------+         +--------------------------------+
  |  BRONZE ZONE (Raw / Append)    |         |  STREAMING / REAL-TIME EDGE    |
  |  +--------------------------+  |         |  +--------------------------+  |
  |  | s3://lake/bronze/         |  |         |  | KSQL / Flink / Spark    |  |
  |  |  + sales/YYYY/MM/DD/     |  |         |  | Structured Streaming    |  |
  |  |  + iot/sensor_id/dt=... |  |         |  | -> Materialized View     |  |
  |  |  + clickstream/event=...  |  |         |  |   (Low Latency)         |  |
  |  |                          |  |         |  +--------------------------+  |
  |  | Format: Parquet/JSON/Avro|  |         +--------------------------------+
  |  | Partition: dt, source    |  |
  |  | Append-only, Immutable   |  |
  |  | + Schema Registry (Confluent)| |
  |  | + Metadata: _source, _ts |  |
  |  +--------------------------+  |
  +--------------+-----------------+
                 |  Auto Loader / Delta Live Tables / dbt
                 v
  +--------------------------------------------------------------------+
  |  SILVER ZONE (Cleansed / Conformed / Deduplicated)                |
  |  +------------------------------------------------------------+    |
  |  |  s3://lake/silver/                                         |    |
  |  |   + sales_enriched/    (joined with customer/product)      |    |
  |  |   + iot_cleaned/       (null handling, unit conversion)    |    |
  |  |   + clickstream_sessionized/  (session window 30m)         |    |
  |  |                                                            |    |
  |  |  • Schema enforcement (Delta Schema Check)                 |    |
  |  |  • Data Quality: Great Expectations / Soda / DQX          |    |
  |  |  • Deduplication: MERGE INTO (SCD Type 2)                 |    |
  |  |  • PII Tagging (Column-level: catalog-governed)            |    |
  |  |  • Table Format: Delta Lake / Apache Iceberg / Hudi        |    |
  |  +------------------------------------------------------------+    |
  +--------------+-----------------------------------------------------+
                 |  Business Logic / Aggregation / KPI Derivation
                 v
  +--------------------------------------------------------------------+
  |  GOLD ZONE (Curated / Business-Ready / Aggregated)                 |
  |  +------------------------------------------------------------+    |
  |  |  s3://lake/gold/                                           |    |
  |  |   + dim_customer/      (SCD2, 100M rows)                  |    |
  |  |   + fact_sales_daily/  (Star Schema)                       |    |
  |  |   + ml_feature_store/  (online/offline features)          |    |
  |  |   + kpi_dashboard/     (materialized for BI tools)        |    |
  |  |                                                            |    |
  |  |  • Row-level + Column-level Security (RLS/CLS)            |    |
  |  |  • Optimized: Z-Order / Liquid Clustering / Bloom Filter   |    |
  |  |  • Vacuum / Expire Snapshots (retention 7~30 days)         |    |
  |  |  • Publish to: Snowflake, Redshift, BigQuery, Tableau     |    |
  |  +------------------------------------------------------------+    |
  +--------------+-----------------------------------------------------+
                 |
                 v
  +--------------------------------------------------------------------+
  |  CONSUMPTION LAYER                                                  |
  |  +------------+  +------------+  +------------+  +------------+    |
  |  | BI Tools   |  | ML/AI      |  | Reverse ETL|  | API/Apps   |    |
  |  | (Tableau,  |  | (MLflow,   |  | (Hightouch,|  | (GraphQL,  |    |
  |  |  Looker,   |  |  SageMaker,|  |  Census)   |  |  REST)     |    |
  |  |  Power BI) |  |  Vertex AI)|  |            |  |            |    |
  |  +------------+  +------------+  +------------+  +------------+    |
  +--------------------------------------------------------------------+

  +---------------------------------------------------------------------+
  |  CROSS-CUTTING: GOVERNANCE & METADATA LAYER                          |
  |  +------------+  +------------+  +------------+  +------------+     |
  |  | Unity      |  | AWS Glue   |  | Hive Metas |  | DataHub /  |     |
  |  | Catalog    |  | Data Cat.  |  | tore (HMS) |  | Amundsen / |     |
  |  | (Databricks|  | + Lake     |  | + Polaris  |  | Atlas /    |     |
  |  | 3-in-1)    |  | Formation  |  | (REST)     |  | Marquez    |     |
  |  +------------+  +------------+  +------------+  +------------+     |
  |   + Data Lineage (OpenLineage / Marquez)                             |
  |   + Data Quality (Great Expectations / Soda)                         |
  |   + Data Contract (Protobuf / Avro Schema Registry)                  |
  |   + Access Control (ABAC / RBAC via OIDC + SCIM)                    |
  +---------------------------------------------------------------------+
```

### 2. 핵심 구성 요소 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Object Storage** | 무제한 확장, 11 9s 내구성의 원시 데이터 저장소 | **Amazon S3**(Standard/IA/Glacier IR/Deep Archive), **Azure Data Lake Storage Gen2**(HNS namespace, ACL), **Google Cloud Storage**(Autoclass 자동 티어링), **MinIO/OSS**(온프레). 핵심: **Hadoop Compatibility**(