---
title: "Feature Store ML Feature Management Reuse"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 676
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 피처 스토어(Feature Store)는 ML 학습(Training)과 추론(Inference) 양쪽에서 동일한 피처 정의를 **Point-in-Time 일관성**과 **온라인/오프라인 이원화 저장(Online-Offline Parity)** 으로 재사용하기 위한 **중앙 집중형 ML 데이터 계층(ML Data Layer)** 으로, Feast, Tecton, Hopsworks, Databricks Feature Store, AWS SageMaker Feature Store, GCP Vertex AI Feature Store 같은 구현체가 특징 레지스트리(Feature Registry)·변환 엔진(Transformation Engine)·서빙 스토어(Serving Store)를 통합 제공한다.
> 2. **가치**: 피처 정의 중복 제거로 데이터 사이언티스트 1인당 피처 준비 시간을 **수일 -> 수 분** 수준으로 단축하고, Training-Serving Skew를 제거하여 **모델 성능 일관성**을 확보하며, 조직 전체에서 **수백~수천 개 피처를 수십~수백 개 모델**이 재사용함으로써 피처-모델 재사용률(Feature Reuse Rate)을 **30~70% 수준**으로 끌어올린다.
> 3. **판단 포인트**: **온라인(Redis/DynamoDB) vs 오프라인(Iceberg/Delta Lake) 듀얼 라이트** 아키텍처 채택 여부, **실시간 스트리밍 변환(Flink/Spark Structured Streaming)** 지원 범위, **온디맨드 변환 vs 사전 머터리얼라이제이션(Pre-materialization)** 트레이드오프, **포인트-인-타임 조인(Point-in-Time Join)** 정확도, **피처 거버넌스(Feature Governance)·계보(Lineage)·품질 모니터링** 수준이 설계의 핵심 결정 변수가 된다.

---

## Ⅰ. 개요 및 필요성

기존 MLOps 환경에서는 데이터 사이언티스트가 Jupyter 노트북 안에서 pandas/SQL로 피처를 가공해 CSV/Pickle로 저장하고, 이를 학습 파이프라인과 추론 서버에서 **각자 다른 코드 경로**로 재구현하는 **"Feature Pipeline 중복"** 문제가 만연했다. 이로 인해 (1) **Training-Serving Skew**(학습은 피처 A, 추론은 피처 A')로 모델 정확도가 운영 환경에서 평균 **5~25% 하락**하는 현상, (2) 동일 피처를 팀별로 재개발해 **연간 수천 시간의 중복 투자**, (3) **피처 정의가 코드/문서/대시보드**에 흩어져 신규 온보딩 시 **평균 2~6주 지식 전이 비용**이 발생했다. Uber의 Michelangelo, Airbnb의 Zipline, LinkedIn의 FeatureStore, Google의 Feast(오픈소스화)가 이를 통합하기 위한 **Feature Store 패턴**으로 정착되었으며, 2017년 Uber Michelangelo 도입 후 **피처 재사용률 80%**, **모델 출시 시간 60% 단축** 효과가 보고된 바 있다.

```text
+------------------------------------------------------------------------------+
|                  기존 ML 파이프라인: 피처 파편화 (AS-IS)                       |
+------------------------------------------------------------------------------+

  Data Scientist A        Data Scientist B        Data Scientist C
  +-------------+         +-------------+         +-------------+
  | Jupyter     |         | Jupyter     |         | Jupyter     |
  |  v          |         |  v          |         |  v          |
  | pandas      |         | Spark SQL   |         | PySpark     |
  |  v          |         |  v          |         |  v          |
  | CSV/Pickle  |         | Parquet     |         | TFRecord    |
  +------+------+         +------+------+         +------+------+
         |                       |                       |
         v                       v                       v
  +-------------+         +-------------+         +-------------+
  | Model A     |         | Model B     |         | Model C     |
  | (Train)     |         | (Train)     |         | (Train)     |
  +------+------+         +------+------+         +------+------+
         |                       |                       |
         v                       v                       v
  +-------------+         +-------------+         +-------------+
  | Serving A   |         | Serving B   |         | Serving C   |
  | (재구현)    |         | (재구현)    |         | (재구현)    |
  +-------------+         +-------------+         +-------------+
   ❌ 피처 정의 중복     ❌ 학습/서빙 불일치    ❌ 거버넌스 부재
```

```text
+------------------------------------------------------------------------------+
|             Feature Store 기반 통합 파이프라인: (TO-BE)                        |
+------------------------------------------------------------------------------+

  Raw Sources (Kafka, S3, RDBMS, SaaS API)
            |
            v
  +-------------------------------------------------+
  |   Feature Pipeline (Spark / Flink / Beam)       |
  |   - Batch Transform   - Stream Transform        |
  |   - On-Demand Transform (Python UDF)            |
  +---------------------+---------------------------+
                        |  Materialize
                        v
  +-------------------------------------------------+
  |           ★ Feature Store (단일 진실 공급원) ★    |
  |  +---------------+  +---------------+           |
  |  | Online Store  |  | Offline Store |           |
  |  | (Redis/       |  | (Iceberg/     |           |
  |  |  DynamoDB)    |  |  Delta/BigQuery)|          |
  |  +-------+-------+  +-------+-------+           |
  |          +--------+---------+                   |
  |                   v                             |
  |       +--------------------+                   |
  |       | Feature Registry   |  <- Schema, Lineage|
  |       | (Catalog/Metadata) |    Version, Owner |
  |       +--------------------+                   |
  +----------+----------------------+---------------+
             |                      |
             v                      v
   +------------------+   +------------------+
   | Training Pipeline|   | Online Inference |
   | (Point-in-Time   |   | (Low-Latency     |
   |  Join, Batch)    |   |  Get Features)   |
   +--------+---------+   +--------+---------+
            v                      v
        Model A/B/C          Real-time Prediction
        (단일 코드 경로)      (서빙 스큐 제거)
```

피처 스토어는 단순한 데이터 저장소를 넘어 **"ML을 위한 데이터 인프라"** 로서, (1) **Feature Registry**(스키마·메타데이터·계보), (2) **Transformation Engine**(배치·스트리밍·온디맨드), (3) **Storage Layer**(온라인·오프라인), (4) **Serving Layer**(학습용·추론용 API)의 **4계층 구조**로 표준화되었다. 이는 2017년 Uber Michelangelo, 2018년 Airbnb Zipline, 2019년 Google Feast 오픈소스 공개 이후 Databricks 2020, Tecton 2021(상용 SaaS) 등으로 확산되었으며, **Lakehouse 아키텍처**(Iceberg + Spark)·**실시간 스트리밍**(Flink·Kafka)·**Feature Platform**(Vector DB 통합) 트렌드와 결합해 진화 중이다.

- **📢 섹션 요약 비유**: 피처 스토어가 없는 세상은 마치 **각 요리사(데이터 사이언티스트)가 같은 '소금'이라는 재료를 각자 다른 이름('Nacl', 'Sodium Chloride', '맛소금')으로 라벨링해 냉장고 여기저기 보관하는 요리 키친**과 같다. 중앙에서 "소금 = NaCl, 원산지 X, 유통기한 Y"로 표준화해 두면, 어떤 요리(모델)에서도 같은 맛을 보장할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

피처 스토어의 4계층 아키텍처는 **데이터 수집 -> 변환 -> 저장 -> 서빙** 흐름을 기반으로, **온라인/오프라인 일관성(Online-Offline Parity)** 과 **시간 정합성(Point-in-Time Correctness)** 이라는 두 가지 핵심 불변량(Invariant)을 보장하도록 설계된다. Feast의 경우 `FeatureView`라는 선언형 DSL로 피처 정의를 기술하고, Tecton은 `FeatureService` 단위로 모델-피처 바인딩을 관리하며, Databricks Feature Store는 Delta Lake의 `FeatureSpec` 테이블과 `FeatureLookup` API로 학습/서빙을 추상화한다.

```text
+----------------------------------------------------------------------------+
|                 Feature Store 4-Tier Reference Architecture                 |
+----------------------------------------------------------------------------+

  Tier 1. Source Layer (데이터 소스)
  +------------+  +------------+  +------------+  +------------+
  | OLTP DB    |  | Event      |  | Object     |  | 3rd-Party  |
  | (MySQL,    |  | Stream     |  | Storage    |  | SaaS API   |
  |  Postgres) |  | (Kafka,    |  | (S3, GCS)  |  | (Stripe,   |
  |            |  |  Kinesis)  |  |            |  |  Salesforce)|
  +-----+------+  +-----+------+  +-----+------+  +-----+------+
        +----------+----+-------+-------+               |
                   v            v                       v
  Tier 2. Transformation Engine (변환 엔진)
  +--------------------------------------------------------------+
  |  +------------+  +------------+  +------------------+         |
  |  | Batch      |  | Streaming  |  | On-Demand        |         |
  |  | (Spark,    |  | (Flink,    |  | (Python UDF,     |         |
  |  |  dbt)      |  |  Spark SS) |  |  gRPC, REST)     |         |
  |  +------------+  +------------+  +------------------+         |
  |  - Window Aggregations (Tumbling, Sliding, Session)         |
  |  - Embedding Generation (LLM, NLP, Vision)                  |
  |  - Joins, Lookups, Type Casting                              |
  +---------------------+----------------------------------------+
                        v
  Tier 3. Storage Layer (이원화된 저장소)
  +----------------------------+  +----------------------------+
  |  Offline Store             |  |  Online Store               |
  |  (대용량·시계열·이력)        |  |  (저지연·실시간 조회)         |
  |  - Apache Iceberg          |  |  - Redis / Bigtable         |
  |  - Delta Lake              |  |  - DynamoDB                 |
  |  - BigQuery / Snowflake    |  |  - Cassandra                |
  |  - Parquet on S3           |  |  - Online Column Store      |
  |  - Time-Travel 지원         |  |  - p99 < 10ms 목표          |
  +------------+---------------+  +-------------+--------------+
               |                                |
               +--------------+-----------------+
                              v
  Tier 4. Serving Layer (서빙 계층)
  +--------------------------------------------------------------+
  |  +-------------------------+  +-------------------------+   |
  |  | Training-time Serving   |  | Online Inference Serving|   |
  |  | (Point-in-Time Join)    |  | (GetOnlineFeatures)     |   |
  |  | - SQL: ASOF JOIN        |  | - REST/gRPC API         |   |
  |  | - Batch Export          |  | - SDK (Python, Java,    |   |
  |  | - Parquet/Arrow IPC     |  |   Go, TS)               |   |
  |  +-------------------------+  +-------------------------+   |
  |  - Feature Registry / Catalog (Schema, Owner, Version)     |
  |  - Monitoring (Drift, Freshness, Null Rate)                |
  |  - Access Control (RBAC, PII Masking)                      |
  +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Feature Registry (피처 레지스트리)** | 피처의 단일 진실 공급원(SSOT)·메타데이터 허브 | 스키마, 타입, 소유자(Owner), 버전, 태그, 데이터 계보(Lineage), SLA 저장. Feast `registry.db`, Tecton `Feature Service` YAML, Databricks `FeatureSpec` 테이블, AWS SageMaker `Feature Group` 메타데이터. **GitOps 통합**으로 PR 기반 피처 변경 승인 워크플로우 지원. |
| **Transformation Engine (변환 엔진)** | 원천 -> 피처 변환 로직 실행 | (1) **Batch**: Spark/DuckDB/dbt로 일·시간 단위 ETL, 백필(Backfill) 가능. (2) **Streaming**: Flink/Spark Structured Streaming으로 Kafka 이벤트 실시간 처리, 윈도우 집계(Tumbling/Sliding/Session). (3) **On-Demand**: 추론 시점에 Python UDF로 즉시 계산 (예: 임베딩, LLM 기반 피처). Tecton은 이 3가지 모드를 동일 DSL로 표현. |
| **Online Store (온라인 스토어)** | 실시간 저지연 피처 조회 (p99 < 10ms) | 키-값 저장소: Redis, DynamoDB, Bigtable, Aerospike, Cassandra. 보통 `entity_id + feature_timestamp`를 PK로, **마지막 값(Last Value)** 만 유지(과거 이력은 오프라인에 보관). TTL(Time-To-Live)로 오래된 데이터 자동 만료. **정규화**하여 1차원 키(예: user_id)당 1~N개 피처. |
| **Offline Store (오프라인 스토어)** | 대용량 학습 데이터 보관·시계열 분석 | 컬럼형 포맷(Parquet/ORC) + 테이블 포맷(Iceberg/Delta/Hudi). 시간 여행(Time Travel) 기능으로 과거 시점의 피처 값 조회 가능. **Point-in-Time Join**(과거 label 시점에 유효했던 피처 값 매칭)이 핵심. BigQuery, Snowflake, Redshift, S3+Iceberg 등이 사용. |
| **Point-in-Time Join (시점 일치 조인)** | 학습 데이터의 **누수(Leakage) 방지** | 라벨(예: 2024-03-15 이탈 여부) 시점 이전의 가장 최근 피처 값을 매칭. SQL의 `ASOF JOIN`(DuckDB, Spark 3.4+) 또는 Feast `get_historical_features()` API가 제공. **데이터 누수(Data Leakage)** 로 인한 모델 AUC 10~30% 허위 향상을 차단. |
| **Feature Serving API** | 학습/추론 양쪽에서 동일 피처 검색 | Feast `get_online_features()`, Tecton `get_features()`, Databricks `score_batch/score_real_time` 엔드포인트. Python/Java/Go SDK, gRPC, REST 지원. **엔티티(예: user_id, session_id)** 기반 일괄 조회(Batch Get) 가능. |
| **Materialization (머터리얼라이제이션)** | 오프라인 -> 온라인 동기화 작업 | 주기(예: 5분) 또는 트리거(예: Kafka offset) 기반. 증분(Incremental) 또는 전체(Full Refresh). 보통 Airflow/Dagster/Tecton Scheduler가 오