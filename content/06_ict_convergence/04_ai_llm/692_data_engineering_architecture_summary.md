---
title: "Data Engineering Architecture Summary"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 692
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 엔지니어링 아키텍처는 **다층 파이프라인(수집->저장->처리->서빙->거버넌스)** 으로, 원천 트랜잭션 데이터를 **Bronze/Silver/Gold 메달리온 패턴**과 **Iceberg/Delta Lake/Hudi 오픈 테이블 포맷**을 통해 트러스트된 데이터 프로덕트로 변환하는 End-to-End 시스템이다.
> 2. **가치**: 스토리지/컴퓨트 분리(Storage-Compute Disaggregation)로 비용 탄력성을 확보하고, **CDC + Streaming + Lakehouse** 조합으로 데이터 신선도(Freshness)를 배치 T+1에서 실시간 분 단위로 단축하며, 데이터 리니지·품질·접근제어 통합으로 컴플라이언스 대응력을 제고한다.
> 3. **판단 포인트**: **Lambda vs Kappa**, **Lake vs Warehouse vs Lakehouse**, **중앙집중형(Monolith) vs 연합형(Data Mesh)** 구조 선택 시, 일관성(Consistency)·지연시간(Latency)·비용·팀 자율성·거버넌스 복잡도 간 트레이드오프를 도메인 특성에 맞춰 정량적으로权衡해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 BI 환경은 **RDBMS -> ODS -> DW -> DM** 의 단방향 ETL 파이프라인으로 구성되어, 데이터 볼륨이 TB 단위를 넘어가고 비정형/반정형 데이터(로그, IoT 센서, 클릭스트림, 이미지, 텍스트)가 폭증하면서 한계에 부딪혔다. 또한 ML/AI 워크로드, 실시간 의사결정, 그리고 GDPR/개인정보보호법 등 규제 준수 요구가 동시에 증가하면서, **단일 RDB로는 처리 불가능한 5V(Volume, Velocity, Variety, Veracity, Value)** 문제를 해결할 새로운 아키텍처 패러다임이 요구되었다.

```text
+-------------------------------------------------------------------------+
|        데이터 엔지니어링 아키텍처 진화: 전통 BI -> Modern Data Stack      |
+-------------------------------------------------------------------------+
|                                                                         |
|  [1990s-2000s]              [2010s]                  [2020s+]           |
|  +----------+               +----------+             +--------------+  |
|  | RDBMS    |               | Hadoop   |             | Lakehouse    |  |
|  | ETL      |    -----►     | HDFS     |   -----►    | Stream-First |  |
|  | DW       |               | MapReduce|             | Data Mesh    |  |
|  | Batch    |               | ETL->ELT  |             | AI-Native    |  |
|  +----------+               +----------+             +--------------+  |
|        |                          |                          |         |
|   T+1 Batch Only            Schema-on-Read           Schema Evolution  |
|   구조화 데이터              정형/비정형 혼합          Real-time + Batch |
|   단일 시스템                 Data Silo 문제          Federated 거버넌스|
+-------------------------------------------------------------------------+

  트리거: 데이터 폭증, ML 수요, 규제 강화, 클라우드 전환, 실시간 요구
```

데이터 엔지니어링 아키텍처는 단순한 기술 조합이 아니라 **데이터를 "프로덕트"로 다루는 엔지니어링 Discipline**이다. 이는 SW 엔지니어링의 **버전관리, 테스트, CI/CD, 모니터링** 원칙을 데이터 파이프라인에 적용하여, **신뢰 가능한(Trusted) 데이터 자산**을 지속적으로 제공할 수 있게 한다. 기존에는 데이터팀이 "엑셀 받아서 처리"하는 식의 수작업에 의존했다면, 현대 데이터 아키텍처는 **Airflow/Dagster 기반 오케스트레이션 + dbt 기반 변환 테스트 + Great Expectations 기반 데이터 품질 검증 + DataHub/Atlas 기반 리니지 추적**을 통해 **데이터 신뢰도(Data Trustworthiness)** 를 엔지니어링 수준으로 끌어올린다.

- **📢 섹션 요약 비유**: 데이터 엔지니어링 아키텍처는 마치 **수도관 시스템**과 같다. 정수장(수집·정제) -> 배수관(저장) -> 정화시설(처리) -> 가정(서빙) -> 수질검사(거버넌스)가 분리되어야 깨끗한 물(신뢰할 수 있는 데이터)을 안정적으로 공급할 수 있다. 1990년대에는 정수장·배수관·가정이 전부 한 덩어리(전통 DW)였지만, 지금은 각 기능이 분리·모듈화되어 효율과 안전성이 극대화되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리

현대 데이터 엔지니어링 아키텍처는 크게 **6개 계층(Layer)** 으로 구성되며, 각 계층은 독립적으로 확장·교체 가능하도록 **느슨한 결합(Loose Coupling)** 으로 설계된다.

```text
+------------------------------------------------------------------------------+
|                    Modern Data Engineering Architecture                      |
|                                                                              |
|  +--------------+                                                            |
|  |  ① Source    |  MySQL, PostgreSQL, MongoDB, Kafka, IoT, S3, API, Logs    |
|  |   Systems    |                                                            |
|  +------+-------+                                                            |
|         |  CDC(Debezium) / Streaming / Batch                                |
|         v                                                                    |
|  +--------------+                                                            |
|  |  ② Ingestion |  Kafka Connect, Flink CDC, Fivetran, Airbyte, Kinesis   |
|  |     Layer    |  +- Schema Registry(Avro/Protobuf)                        |
|  +------+-------+                                                            |
|         |  Raw/Append-Only                                                  |
|         v                                                                    |
|  +--------------+                                                            |
|  |  ③ Storage   |  Bronze(Raw) --► Silver(Cleansed) --► Gold(Aggregated)  |
|  |   (Lakehouse)|  Storage: S3 / ADLS / GCS / MinIO                       |
|  |              |  Format: Delta Lake / Apache Iceberg / Apache Hudi       |
|  +------+-------+                                                            |
|         |  Spark / dbt / Flink SQL                                          |
|         v                                                                    |
|  +--------------+                                                            |
|  |  ④ Process   |  배치: Spark, dbt                                         |
|  |   & Modeling |  스트림: Flink, Kafka Streams, Spark Structured Streaming |
|  |              |  변환: dbt(sql + tests + docs)                             |
|  +------+-------+                                                            |
|         |  SQL/REST/gRPC                                                    |
|         v                                                                    |
|  +--------------+                                                            |
|  |  ⑤ Serving   |  OLAP: Snowflake, BigQuery, StarRocks, ClickHouse, Druid|
|  |     Layer    |  Search: Elasticsearch, OpenSearch                       |
|  |              |  ML Feature Store: Feast, Tecton                          |
|  |              |  API: GraphQL, REST                                       |
|  +------+-------+                                                            |
|         |                                                                    |
|         v                                                                    |
|  +--------------+                                                            |
|  |  ⑥ Consumer  |  BI(Looker/Tableau/Superset) / ML(TensorFlow/PyTorch)   |
|  |              |  Apps / Reverse ETL(Hightouch/Census) -> 운영시스템       |
|  +--------------+                                                            |
|                                                                              |
|  +----------------------------------------------------------------------+    |
|  | Cross-Cutting:  ⑦ Orchestration(Airflow/Dagster/Prefect)             |    |
|  |                 ⑧ Governance(DataHub/Unity/Collibra/Atlan/Purview)   |    |
|  |                 ⑨ Data Quality(Great Expectations/Soda/Deequ)        |    |
|  |                 ⑩ Observability(Monte Carlo/Datafold/Anomalo)        |    |
|  |                 ⑪ Security & Privacy(Immuta, Vault, Column-level Mask)|    |
|  +----------------------------------------------------------------------+    |
+------------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① Source Systems** | 트랜잭션·로그·외부 데이터 원천 | OLTP DB(PostgreSQL, MySQL, Oracle), NoSQL(MongoDB, Cassandra), Message Broker(Kafka, RabbitMQ), SaaS API(Salesforce, Stripe), IoT 게이트웨이, Web/App 로그 |
| **② Ingestion Layer** | 소스->스토리지 데이터 유입 | **CDC(Change Data Capture)**: Debezium 기반 binlog/log 기반 변경 캡처, **Streaming**: Kafka + Kafka Connect / Flink CDC, **Batch**: Sqoop / Fivetran / Airbyte, **API Integration**: GraphQL/REST Polling, **Schema Registry**: Avro/Protobuf로 진화 추적 |
| **③ Storage Layer (Lakehouse)** | 원본->정제->집계 데이터를 계층적으로 저장 | **Bronze**: 원본 그대로(Append-Only), **Silver**: 중복 제거·스키마 정제·CDC 머지, **Gold**: 비즈니스 도메인별 집계·Dimensional Modeling. 파일 포맷은 **Parquet/ORC**(컬럼형), 트랜잭션·ACID·Time-Travel은 **Delta Lake / Iceberg / Hudi** 오버레이로 구현 |
| **④ Processing & Modeling** | 데이터 변환·집계·ML 피처 생성 | **배치**: Apache Spark(Structured API), **스트림**: Flink(Exactly-Once + State Backend), **변환**: dbt(SQL 모델 + 자동 생성 문서 + 데이터 테스트), **ML 피처**: Feast(Online/Offline Store 동기화) |
| **⑤ Serving Layer** | 분석/ML/운영이 즉시 소비 가능하도록 데이터 노출 | **OLAP 엔진**: 컬럼형 스토리지 + 벡터화 실행(SIMD), **Search**: 역색인 + 분산 검색, **Feature Store**: Online Low-Latency KV Store(DynamoDB/Redis), **Reverse ETL**: 분석 결과를 운영 DB로 역동기화하여 액션 가능화 |
| **⑥ Orchestration** | 파이프라인 스케줄링·의존성·재시도·모니터링 | **Airflow**: DAG 기반, **Dagster**: Asset-Centric(데이터 중심), **Prefect**: Dynamic Workflow, **Argo/Temporal**: 컨테이너 기반 워크플로우 |
| **⑦ Governance & Quality** | 리니지·카탈로그·품질·접근제어 | **메타데이터**: Hive Metastore / Glue Catalog / Unity Catalog, **리니지**: OpenLineage + Marquez/DataHub, **품질 테스트**: dbt tests + Great Expectations, **PII 마스킹**: 동적 마스킹(Immuta), **접근제어**: RBAC + ABAC + Column-Level Policy |

### 핵심 메커니즘 심화

**1) 메달리온 아키텍처(Medallion Architecture) 상세 동작**
- **Bronze 계층**: 원본 데이터를 그대로 적재(Immutable). 예: Kafka 토픽별 원시 이벤트 + Debezium CDC 레코드. 스키마 검증은 약하게(스키마 진화 허용), 파티션은 `dt=YYYY-MM-DD` 형태로 일자별.
- **Silver 계층**: Bronze에서 읽어 **중복 제거(Deduplication via primary key)**, **Late-Arriving Event 처리(Watermark + Allowed Lateness)**, **Schema Enforcement**, **CDC 머지(upsert/merge into)** 수행. 비즈니스 엔티티 기준 통합 뷰(예: `customer_360`) 생성.
- **Gold 계층**: Silver에서 **Dimensional Modeling(Kimball: Fact/Dim)** 또는 **One Big Table(OBT)** 또는 **Data Vault** 방식으로 집계. BI 대시보드/ML 학습 데이터로 직접 사용. 컬럼 수가 적고, 행 단위 업데이트는 거의 없음.

**2) Lakehouse 트랜잭션 보장 메커니즘**
오픈 테이블 포맷은 파일 기반 데이터레이크에 **로그 계층**을 추가하여 RDBMS의 ACID 트랜잭션을 구현한다.
- **Delta Lake**: `_delta_log/` JSON 체크포인트 + Parquet 데이터 파일. **Optimistic Concurrency Control(OCC)** + **Z-Order Clustering**으로 멀티클라이언트 동시성 보장.
- **Apache Iceberg**: **메타데이터 계층(manifest list -> manifest -> data file) 3단계**로 히든 파티셔닝·스키마 진화·시간 여행(Time Travel) 지원. **Hidden Partitioning**으로 사용자 실수 방지.
- **Apache Hudi**: **Copy-on-Write(CoW) vs Merge-on-Read(MoR)** 모드, **Record-Level Index**(Hoodie Key)로 빠른 upsert/delete, 변경 스트림(CDC 스트림 자체) 제공.

**3) CDC 기반 실시간 수집의 원리**
MySQL binlog -> Debezium Kafka Connect -> Kafka Topic -> Flink/Flink CDC -> Iceberg/StarRocks로 흘러가며, **Log-Based CDC**는 트랜잭션의 일관성을 보존한 채로 모든 INSERT/UPDATE/DELETE 이벤트를 발행한다. 이 방식은 **Timestamp-based Polling CDC** 대비 네트워크 부하 1/10, 지연 ms 단위, 누락 없음의 장점이 있다.

- **📢 섹션 요약 비유**: 메달리온 아키텍처는 **곡물 도정 공정**과 같다. Bronze는 **수확한 그대로의 쌀(거칠고 이물질 포함)**, Silver는 **도정되어 정선된 쌀(등급 분류, 불순물 제거)**, Gold는 **포장된 상품 쌀(고객 요구 규격·중량 패키징)**. 각 단계에서 품질 검사를 거치므로, 최종 소비자는 신뢰할 수 있는 상품만 받는다.

---

## Ⅲ. 비교 및 연결

데이터 엔지니어링은 유사하지만 상이한 패러다임 간 선택의 연속선(Trade-off Spectrum) 위에