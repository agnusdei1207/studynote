---
title: "Data Lakehouse Unified Analytics Platform"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 673
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 레이크하우스(Data Lakehouse)는 오픈 테이블 포맷(Delta Lake, Apache Iceberg, Apache Hudi)을 통해 객체 스토리지(S3, ADLS, GCS) 위에 ACID 트랜잭션, 스키마 강제/진화, 타임 트래블, 통계 기반 데이터 스키핑을 제공하여, 기존 데이터 레이크의 유연성과 데이터 웨어하우스의 성능·거버넌스를 단일 계층에서 통합한 패러다임이다.
> 2. **가치**: 동일 데이터 사본으로 배치/스트리밍/ML/BI 워크로드가 동시 처리되어 ETL 중복 제거, 스토리지 비용 약 50~70% 절감, 데이터 중복성(Data Gravity) 문제 해소, 데이터 사일로 제거 및 단일 거버넌스(Unity Catalog, Polaris, Hive Metastore) 적용을 통해 TTM(Time-To-Market)을 평균 3~6개월 단축한다.
> 3. **판단 포인트**: 핵심 의사결정 포인트는 ① 오픈 테이블 포맷 선택(Delta vs Iceberg vs Hudi), ② 컴퓨트-스토리지 분리(Decoupled) 아키텍처의 메타데이터 카탈로그 분리 전략, ③ 메달리온 아키텍처(브론즈/실버/골드) 적용 깊이, ④ 옵티마이즈·좁은 컴팩션(OPTIMIZE/Z-Order/VACUUM) 오퍼레이션 정책, ⑤ 멀티 클라우드/하이브리드 환경에서의 데이터 셰어링(Delta Sharing) 및 페더레이션 설계이다.

---

## Ⅰ. 개요 및 필요성

기존 데이터 분석 플랫폼은 두 가지 극단 사이에서 진화해 왔다. **1세대 데이터 웨어하우스**(Teradata, Oracle Exadata, Netezza)는 고가의 전용 MPP(Massively Parallel Processing) 어플라이언스 위에 열 지향 스토리지를 두고 강력한 SQL 분석과 ACID 트랜잭션을 제공했지만, 비정형 데이터 처리와 스키마 유연성이 부족하여 스토리지 비용이 데이터 TB당 수백 달러에 달했다. **2세대 데이터 레이크**(Hadoop HDFS + Spark + Parquet)는 저비용 객체 스토리지에 모든 데이터를 스키마-온-리드(Schema-on-Read)로 적재하여 머신러닝·비정형 로그·이미지 분석까지 흡수했으나, 트랜잭션 부재로 인한 "스왐프 지옥(Data Swamp)" 문제, 작은 파일(Small File) 누적, 부분 업데이트/머지 불가능, 카탈로그-스토리지 정합성 깨짐 등의 운영 이슈가 발생했다.

이에 2019년 Databricks가 제안한 **레이크하우스**는 객체 스토리지를 그대로 유지하면서 **트랜잭션 로그(Delta Log / Iceberg Manifest / Hudi Timeline)** 라는 메타데이터 계층을 추가하여 두 패러다임의 장점만 결합한 형태이다. 이후 Apache Iceberg가 2020년 Netflix에서, Apache Hudi가 Uber에서 각각 오픈소스화 되며 **오픈 테이블 포맷(OTF, Open Table Format)** 생태계가 폭발적으로 성장했고, Snowflake·BigQuery·Redshift 같은 기존 DW도 Iceberg 테이블을 네이티브로 읽고 쓰는 방향으로 빠르게 수렴하고 있다.

```text
[ 데이터 분석 플랫폼 진화 아키텍처 ]

  +-----------------+   +-----------------+   +------------------------+
  | Data Warehouse  |   |  Data Lake      |   |  Data Lakehouse        |
  | (1990s~2010s)   |   | (2010s)         |   | (2019~현재)            |
  +-----------------+   +-----------------+   +------------------------+
   |                        |                       |
   v                        v                       v
 Proprietary HW           Commodity HDFS         Object Storage
 (Exadata, Netezza)       + YARN/MapReduce        (S3/ADLS/GCS/OSS)
   |                        |                       |
 Proprietary FS           Raw Parquet/ORC/Avro   + Transaction Log
 (Block storage)          Schema-on-Read          (Delta/Iceberg/Hudi)
   |                        |                       |
 SQL Only                 No ACID                 ACID + Schema Enforce
   |                        |                       |
 Expensive $300+/TB        $20/TB but Swamp       $20/TB + Governed
   |                        |                       |
 BI/Reporting             ML/Big Data             BI + ML + Streaming
                                              + Data Sharing + AI

       [ 진화 동인 (Drivers) ]
   • 클라우드 객체 스토리지의 보편화 (S3 99.999999999% durability)
   • 데이터 규모 폭증 (페타 -> 엑사바이트)
   • AI/ML 워크로드의 정형+비정형 통합 요구
   • 데이터 카피제로(Data Copy Zero) 컴플라이언스 (GDPR/개인정보보호법)
   • 트랜잭션 일관성 없는 레이크의 운영 비용 한계
```

실무적 관점에서 데이터 레이크하우스는 단순한 기술 트렌드가 아니라, **데이터를 "한 번 저장하고 여러 의미(Semantic Layer)로 해석"하는 의미론적 통합(Semantic Unification)** 으로, 데이터 거버넌스·컴플라이언스·AI 시대의 필수 인프라로 자리 잡았다. 특히 2024년 이후 **Apache Iceberg**가 사실상 표준으로 부상하면서(Snowflake, BigQuery, Redshift, Trino, Dremio, Spark 모두 Iceberg 네이티브), 벤더 종속성 탈피(Lock-in 제거)와 멀티엔진 상호운용성(Interoperability)이 핵심 평가 기준으로 격상되었다.

- **📢 섹션 요약 비유**: 데이터 웨어하우스는 "값비싼 유리 진열장"에 정제된 보석만 보이는 박물관, 데이터 레이크는 "정리 안 된 창고"에 모든 박스를 던져두는 것이고, 레이크하우스는 "RFID 칩이 붙은 박스를 스마트 선반에 진열"해 창고의 유연성과 박물관의 관리 능력을 동시에 갖춘 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

레이크하우스는 4개의 논리 계층으로 구성된다. ① **스토리지 계층**(Object Storage) ② **메타데이터·트랜잭션 계층**(오픈 테이블 포맷) ③ **컴퓨트 엔진 계층**(SQL/ML/Streaming) ④ **거버넌스·카탈로그 계층**. 각 계층은 REST API 기반의 표준 인터페이스로 느슨하게 결합(Decoupled)되어 있어, 스토리지를 바꾸지 않고 컴퓨트 엔진을 교체하거나 그 반대가 가능하다.

```text
[ 데이터 레이크하우스 4계층 아키텍처 ]

   +--------------------------------------------------------------------+
   |  4. 거버넌스 & 카탈로그 계층 (Governance & Catalog)                  |
   |  +-----------------+ +------------------+ +-------------------+    |
   |  | Unity Catalog   | | Polaris Catalog  | | AWS Lake Formation |   |
   |  | (Databricks)    | | (Snowflake OSS)  | | (AWS Glue)         |   |
   |  | • RBAC/ABAC     | | • Iceberg REST   | | • LF-Tags, Grants  |   |
   |  | • Lineage       | | • OIDC Auth      | | • Column-level ACL |   |
   |  | • PII Tagging   | | • Vended Creds   | | • Cross-account    |   |
   |  +--------+--------+ +---------+--------+ +---------+---------+   |
   |           +----------+----------+----------+---------+             |
   |              +------v----------------------v------+               |
   |              |  표준 카탈로그 인터페이스 (Iceberg REST,            |
   |              |  Delta UniForm, HMS Thrift, Nessie) |               |
   |              +------+-----------------------------+               |
   +---------------------+----------------------------------------------+
                         |
   +---------------------+----------------------------------------------+
   |  3. 컴퓨트 엔진 계층 (Compute)                                      |
   |   +----------+ +----------+ +----------+ +----------+ +---------+ |
   |   | Spark    | | Trino/   | | Flink    | | Photon   | | Dremio  | |
   |   | (Scala)  | | Presto   | | (Stream) | | (C++/SIMD)| | Sonar   | |
   |   +-----+----+ +----+-----+ +----+-----+ +----+-----+ +----+----+ |
   |         |            |            |             |            |      |
   |         +------------+-----+------+-------------+------------+      |
   |                            |  DataFrame API / SQL / ML / Streaming  |
   +----------------------------+----------------------------------------+
                                |
   +----------------------------+----------------------------------------+
   |  2. 메타데이터 & 트랜잭션 계층 (Open Table Format)                    |
   |  +------------------+ +------------------+ +--------------------+   |
   |  | Delta Lake       | | Apache Iceberg   | | Apache Hudi        |   |
   |  | • _delta_log/    | | • manifest list  | | • .hoodie/timeline |   |
   |  | • JSON+Checkpoint| | • snapshot id    | | • Copy-on-Write    |   |
   |  | • VACUUM/OPTIMIZE| | • hidden partit. | | • Merge-on-Read    |   |
   |  | • Z-Order/Bloom  | | • sort/partition  | | • record-level idx |   |
   |  +--------+---------+ +--------+---------+ +----------+---------+   |
   |           +---------------------+---------------------+             |
   +---------------------------------+----------------------------------+
                                     |
   +---------------------------------+----------------------------------+
   |  1. 스토리지 계층 (Object Storage)                                  |
   |  +---------+  +----------+  +---------+  +----------+  +--------+  |
   |  | AWS S3  |  | ADLS Gen2|  | GCS     |  | NCloud   |  | MinIO  |  |
   |  |         |  | (Azure)  |  | (GCP)   |  | Object   |  | On-Prem|  |
   |  +---------+  +----------+  +---------+  +----------+  +--------+  |
   |     Parquet / ORC / Avro 컬럼형 파일 (Columnar)                      |
   +--------------------------------------------------------------------+

[ 트랜잭션 로그 동작 순서 (Delta Lake 기준) ]
   ① Writer -> 트랜잭션 시작 (txId=100, version=10)
   ② Parquet 파일 생성: part-00000-...snappy.parquet (add)
   ③ _delta_log/00000000000000000010.json 에 액션 기록 (add/remove/setTxn)
   ④ 체크포인트 생성: 00000000000000000010.checkpoint.parquet (10버전마다)
   ⑤ Reader -> 최신 스냅샷 조회 (Snapshot Isolation: Read Committed)
   ⑥ Optimistic Concurrency: 충돌 시 TransactionConflictException -> 재시도
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **스토리지 계층 (Object Storage)** | 모든 원천·정제·집계 데이터를 컬럼형 파일로 보존 | Parquet(기본), ORC, Avro. S3 Standard-IA/Glacier, ADLS Hot/Cool/Archive 계층화. 데이터 사일로 없이 단일 사본(Single Source of Truth) 유지 |
| **트랜잭션 로그 (Transaction Log)** | 원자성(Atomic)·일관성(Consistent)·격리(Isolated)·지속성(Durable) 보장 | Delta Lake는 `_delta_log/*.json`에 add/remove/commitInfo를 append-only로 기록. Iceberg는 `metadata.json` v1/v2 + `manifest-list` 계층. Hudi는 `*.commit` 타임라인. 낙관적 동시성 제어(OCC) 기반 충돌 감지 |
| **메타데이터 카탈로그 (Catalog)** | 테이블/스키마/파티션/통계 정보를 단일 위치에서 관리 | Hive Metastore(Thrift), AWS Glue Data Catalog, Unity Catalog(Delta), Nessie/Gravitino(브랜치·태그 지원), Polaris(Iceberg REST). 카탈로그 API 표준화(Iceberg REST Catalog)로 엔진 간 상호운용성 확보 |
| **컴퓨트 엔진 (Compute Engine)** | SQL·DataFrame·ML·Streaming을 통한 데이터 처리 | Apache Spark(범용 배치/ML), Trino/Presto(상호적 SQL), Flink(저지연 스트리밍), Photon(Databricks C++ SIMD 가속), Dremio Sonar(컬럼형 MPP). 동일한 OTF를 여러 엔진이 동시 읽기 가능(Reader-Writer 분리) |
| **거버넌스 (Governance)** | 접근제어·계보·품질·PII 보호 통합 | RBAC/ABAC(역할/속성 기반), 컬럼 단위 마스킹, 자동 리니지(OpenLineage), 데이터 계약(Data Contract), DQ 규칙(Great Expectations), PII 자동 탐지(클라우드 DLP) |
| **오케스트레이션 (Orchestration)** | 데이터 파이프라인 스케줄링 및 의존성 관리 | Apache Airflow, Dagster, Prefect, Databricks Workflows, AWS Step Functions, GCP Cloud Composer. 메달리션 계층(Bronze->Silver->Gold) 간 SCD2·CDC 흐름 제어 |

**핵심 동작 원리 ①: 타임 트래블 (Time Travel)**
트랜잭션 로그의 모든 버전이 보존되어 있어, `SELECT * FROM table TIMESTAMP AS OF '2024-12-01 00:00:00'` 또는 `VERSION AS OF 123`으로 과거 스냅샷 조회 가능. GDPR "잊힐 권리" 대응 시 특정 사용자 행을 DELETE한 후 휴지통(VACUUM 보존 기간 7~30일) 없이 영구 삭제하고, 감사 추적(Audit Trail)에 활용한다. Iceberg는 `snapshot-id` 기반, Delta는 `version` 기반, Hudi는 `commit-time` 기반으로 구현된다.

**핵심 동작 원리 ②: 스키마 진화 & 강제 (Schema Evolution & Enforcement)**
Delta Lake는 쓰기 시점에 스키마를 강제 검증(Schema Validation)하여 컬럼 누락/타입 불일치 시 `AnalysisException` 발생. 이후 `ALTER TABLE ... ADD