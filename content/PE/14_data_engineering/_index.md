+++
title = "도메인 14: 데이터 엔지니어링 (Data Engineering)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-data-engineering"
kids_analogy = "세상 여기저기서 쏟아지는 '더러운 흙탕물(원시 데이터)'을 모아서, 깨끗하게 정수하고 파이프를 통해 요리사(데이터 분석가)나 로봇(AI)이 마실 수 있는 '1급수'로 만들어주는 상수도 공사예요!"
+++

# 도메인 14: 데이터 엔지니어링 (Data Engineering)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파편화된 원시 데이터(Raw Data)를 수집, 정제, 적재(ETL/ELT)하여 데이터 분석가, 과학자, 그리고 AI 모델이 즉각적이고 신뢰할 수 있게 사용할 수 있도록 거대한 배관망(Data Pipeline)을 설계하고 유지보수하는 아키텍처 공학.
> 2. **가치**: 데이터 사일로(Silo)를 파단하고 전사적 데이터 레이크하우스(Lakehouse)를 구축함으로써, 기업의 통찰력(Insight) 도출 시간을 단축하고 데이터 기반 의사결정(Data-driven Decision)의 무결성을 강제함.
> 3. **융합**: 고전적인 정형 데이터용 Data Warehouse를 넘어, Kafka 기반의 실시간 스트리밍 처리와 Spark의 인메모리 분산 컴퓨팅이 융합되어 AI 파이프라인의 젖줄(Bloodline)로 전면 진화.

---

### Ⅰ. 개요 (Context & Background)
아무리 정교한 딥러닝 모델(AI)이 존재하더라도, 입력되는 데이터가 오염되었거나 편향되어 있다면 그 결과는 끔찍한 재앙이 된다(Garbage In, Garbage Out). 과거에는 데이터베이스 관리자(DBA)가 정형 데이터 위주로 SQL을 다루었다면, 모바일과 IoT 시대가 열리면서 초당 수백만 건의 비정형 로그(JSON, 이미지, 텍스트)가 쏟아지는 '빅데이터 폭발'이 발생했다.
**데이터 엔지니어링(Data Engineering)**은 이 거친 폭포수를 통제하기 위해 탄생했다. 이는 단순한 데이터 복사 작업이 아니다. 멱등성(Idempotency)을 보장하는 분산 파이프라인을 구축하고, 데이터의 계보(Data Lineage)를 추적하며, 수백 테라바이트의 데이터를 조인(Join)할 때 발생하는 메모리 셔플(Shuffle) 병목을 압살하는 고도의 분산 시스템 아키텍처 튜닝 과정이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

데이터 엔지니어링은 데이터의 추출(Extract)부터 서빙(Serve)까지의 모든 흐름을 관장하는 다층적 레이어 아키텍처다.

#### 1. 핵심 공학 도메인
| 도메인 | 상세 역할 | 내부 동작/활용 기법 | 관련 도구 및 엔진 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Ingestion (수집)** | 다양한 소스에서 데이터 추출 | CDC(변경 데이터 캡처), 실시간 스트리밍, 배치 | Kafka, Debezium, Fluentd | 강에서 물 펌프질 |
| **Storage (저장)** | 대용량 원시/정제 데이터 보관 | 분산 파일 시스템, 객체 스토리지, 컬럼형 포맷 | HDFS, S3, Parquet, Iceberg | 거대한 댐과 정수장 |
| **Processing (처리)** | 데이터의 정제 및 변환(Transform) | 인메모리 맵리듀스, 마이크로 배치, 윈도우 연산 | Apache Spark, Flink | 수질 정화 필터링 |
| **Orchestration** | 파이프라인 워크플로우 제어 | 방향성 비순환 그래프(DAG) 기반 스케줄링, 재시도 | Apache Airflow, Dagster | 공장의 자동화 컨베이어 |
| **Governance** | 데이터 품질 및 보안 통제 | 메타데이터 관리, 권한 제어, 데이터 카탈로그 | Amundsen, Apache Atlas | 수질 검사관 및 규정 |

#### 2. 모던 데이터 스택 (Modern Data Stack) 아키텍처 다이어그램 (ASCII)
전통적인 ETL에서 벗어나, 무한한 클라우드 스토리지에 데이터를 먼저 적재하고(Load) 나중에 클라우드 DW의 막강한 컴퓨팅 파워로 변환(Transform)하는 ELT 아키텍처.
```text
    [ ELT-based Cloud Data Lakehouse Architecture ]
    
    (Sources)          (Extract & Load)           [ Data Lakehouse (S3 / GCS) ]          (Transform via dbt)
    +---------+       +----------------+        +-----------------------------------+       +-------------+
    | RDBMS   |       | Fivetran /     |        | 1. Bronze Layer (Raw JSON/CSV)    |       |             |
    | (MySQL) | ----> | Airbyte        | -----> |    - 원본 데이터 그대로 적재        | ----> | SQL을 통한  |
    +---------+       | (Batch EL)     |        +-----------------------------------+       | 데이터 정제 |
                                                | 2. Silver Layer (Cleaned Parquet) | <---- | 및 비즈니스 |
    +---------+       +----------------+        |    - Null 제거, 스키마 강제, 필터 | ----> | 로직 반영   |
    | App Logs| ----> | Apache Kafka   | -----> +-----------------------------------+       | (DAG 형태)  |
    | (Click) |       | (Real-time Stream)      | 3. Gold Layer (Aggregated)        | <---- |             |
    +---------+       +----------------+        |    - BI 툴 및 AI 훈련용 데이터 마트 |       +-------------+
                                                +-----------------------------------+
                                                                 | (Data Serving)
                                                +----------------v------------------+
                                                | Tableau / Superset / AI ML Model  |
                                                +-----------------------------------+
```

#### 3. 핵심 알고리즘 메커니즘 (Columnar Storage Format - Parquet)
전통적인 RDBMS(Row-based)는 한 레코드(Row)를 통째로 읽어 집계 쿼리에 극도로 비효율적이다. Data Engineering은 이를 타파하기 위해 **컬럼형 스토리지(Columnar Format, 예: Apache Parquet)**를 사용한다.
① 동일한 컬럼(예: '나이')의 데이터만 연속된 디스크 블록에 모아서 저장한다.
② "평균 나이"를 구하는 쿼리 시, 불필요한 '이름', '주소' 컬럼 블록을 디스크에서 읽지 않아 I/O를 99% 삭감(Projection Pushdown)한다.
③ 동일한 데이터 타입이 연속되므로 RLE(Run-Length Encoding)나 Dictionary 인코딩을 통해 압축률(Compression)을 극한으로 끌어올린다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 데이터 처리 패러다임: ETL vs ELT 심층 비교
| 비교 항목 | ETL (Extract $\rightarrow$ Transform $\rightarrow$ Load) | ELT (Extract $\rightarrow$ Load $\rightarrow$ Transform) | 기술사적 파급력 |
| :--- | :--- | :--- | :--- |
| **처리 위치(엔진)** | 적재 전 독립적인 무거운 ETL 서버에서 변환 | 타겟 스토리지(DW) 내부의 분산 컴퓨팅 엔진 사용 | 클라우드 DW의 파워(Snowflake 등)를 100% 활용하는 ELT가 현대 표준 |
| **데이터 유실 리스크**| 변환 과정 중 에러 발생 시 원시 데이터 유실 위험 | 원본 데이터가 호수에 일단 보존되므로 재처리 용이 | Data Lake의 사상을 완벽히 지원 |
| **유연성** | 요구사항 변경 시 파이프라인 코드를 전면 수정 | 분석가가 원할 때 타겟 내부에서 SQL로 유연하게 변환 | dbt(Data Build Tool)와 결합하여 분석가(Analyst)에게 엔지니어링 권한 위임 |
| **컴플라이언스 보안** | 이동 중 개인정보(PII) 마스킹 등 보안 처리에 유리 | 암호화되지 않은 Raw 데이터 적재 시 보안 통제 철저 필요 | PII 데이터는 ELT 전 Ingestion 단계에서 마스킹 강제 |

#### 2. 전사 데이터 아키텍처: DW vs Data Lake vs Data Lakehouse
| 항목 | Data Warehouse (DW) | Data Lake | Data Lakehouse |
| :--- | :--- | :--- | :--- |
| **데이터 구조** | 엄격한 정형 데이터 (Schema-on-Write) | 정형, 반정형, 비정형 (Schema-on-Read) | 두 가지의 장점 융합 |
| **저장 비용** | 매우 비쌈 (고성능 스토리지) | 매우 저렴 (S3, GCS 객체 스토리지) | 저렴 (객체 스토리지 기반) |
| **ACID 트랜잭션** | 완벽히 지원 | 미지원 (단순 파일 저장소) | 지원 (Apache Iceberg, Delta Lake 포맷) |
| **타겟 유저** | 비즈니스 분석가 (BI 대시보드) | 데이터 과학자 (ML/DL 모델 훈련) | 전사 통합 데이터 플랫폼 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1: 이종 DB 동기화를 위한 람다(Lambda) 아키텍처의 파단 및 카파(Kappa) 전환**
- **문제 상황**: 일일 배치(Batch) 파이프라인과 실시간(Real-time) 스트리밍 파이프라인이 분리된 람다 아키텍처를 운영 중. 두 파이프라인의 코드가 파편화되어 유지보수가 불가능하고, 뷰(View) 병합 시 데이터 불일치 발생.
- **기술사적 결단**: 배치와 스트리밍의 경계를 허무는 **카파(Kappa) 아키텍처**로 전면 전환. 모든 데이터 소스를 Kafka를 통해 스트림 이벤트로 취급하고, Apache Flink를 단일 처리 엔진으로 사용하여 코드 중복을 제거한다. 과거 데이터(배치) 재처리가 필요할 때는 Kafka의 오프셋(Offset)을 과거로 되감아 스트리밍 엔진 하나로 완벽히 재현(Replay)한다.

**시나리오 2: 거대 조직의 데이터 병목 타파 (Data Mesh 도입)**
- **문제 상황**: 중앙 집중형 데이터 엔지니어링 팀 하나가 전사 50개 부서의 파이프라인 생성 요청을 감당하지 못해, 비즈니스 부서의 데이터 분석 대기 시간이 수개월로 지연됨.
- **기술사적 결단**: 물리적 아키텍처가 아닌 조직적/논리적 분산 아키텍처인 **데이터 메시(Data Mesh)** 패러다임을 도입. 데이터를 중앙 호수에 가두는 대신, 각 비즈니스 도메인 팀(마케팅, 재무 등)이 데이터를 마이크로서비스처럼 하나의 '제품(Data as a Product)'으로 직접 소유하고 생산하도록 자율성을 부여한다. 중앙은 오직 상호 운용성(Interoperability)을 위한 데이터 거버넌스와 인프라 플랫폼만 제공한다.

**도입 시 고려사항 (안티패턴)**
- **데이터 늪 (Data Swamp) 안티패턴**: 빅데이터 시대라며 아무런 스키마나 메타데이터(카탈로그) 정의 없이 무작정 S3에 Raw 데이터를 쏟아붓는 행위. 결국 아무도 데이터의 의미와 출처를 모르게 되어 분석이 불가능한 쓰레기장(Swamp)이 된다. 기술사는 반드시 데이터 적재 전 **데이터 카탈로그(Data Catalog)**를 자동 갱신하고 데이터 계보(Lineage)를 추적하는 거버넌스 체계를 아키텍처의 심장부에 박아 넣어야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량적 기대효과 (ROI)**
| 파이프라인 최적화 요소 | 비즈니스/인프라 타겟 | 정량적 개선 효과 (ROI) |
| :--- | :--- | :--- |
| **Parquet + 파티셔닝 도입** | 대규모 쿼리 스캔 비용 최소화 | 클라우드 DW(Athena, BigQuery) 쿼리 과금 **90% 절감**, 속도 10배 폭증 |
| **CDC (Change Data Capture)** | 소스 DB 부하 없는 실시간 데이터 동기화 | 배치 쿼리로 인한 새벽 DB Lock 해소, 데이터 최신화(Latency) **1초 이내** |
| **Airflow 멱등성 설계** | 파이프라인 실패 복구 시간 | 에러 발생 시 수동 복구 시간 5시간 $\rightarrow$ **자동 재시도를 통한 0분** |

**미래 전망 및 진화 방향**:
데이터 엔지니어링은 AI의 힘을 빌려 **'DataOps'**의 궁극적 형태로 진화하고 있다. 데이터 파이프라인의 코드를 짜는 것을 넘어, 데이터 자체의 품질을 CI/CD 파이프라인에서 자동 검증하고, 스키마가 변경되면 머신러닝이 이를 감지해 파이프라인을 스스로 복구하는 **자가 치유 데이터 시스템(Self-healing Data System)**이 다가오고 있다. 결국 데이터 플랫폼은 모든 기업의 최상위 추상화 계층(Platform as a Service)으로 군림할 것이다.

**※ 참고 표준/가이드**:
- DAMA-DMBOK (Data Management Body of Knowledge): 전사적 데이터 관리(거버넌스, 아키텍처, 품질 등)를 위한 글로벌 사실상 표준.
- ISO 8000: 데이터 품질 및 관리에 관한 국제 표준 규격.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [`[빅데이터 분산 컴퓨팅(Hadoop/Spark)]`](@/PE/16_bigdata/_index.md): 데이터 엔지니어가 다루는 수백 테라바이트급 물리적 분산 처리 엔진의 코어.
- [`[클라우드 데이터 웨어하우스(DW)]`](@/PE/5_database/_index.md): 구조화된 데이터를 비즈니스 분석가에게 서빙하는 최종 목적지(Target).
- [`[인공지능과 머신러닝(MLOps)]`](@/PE/10_ai/_index.md): 파이프라인을 통해 정제된 피처(Feature) 데이터를 먹고 자라는 가장 중요한 컨슈머(Consumer).
- [`[데브옵스(DevOps) 및 CI/CD]`](@/PE/15_devops_sre/_index.md): 데이터 파이프라인 코드(Airflow DAG, dbt)를 안전하게 배포하고 모니터링하는 인프라 철학.
- [`[소프트웨어 아키텍처(MSA)]`](@/PE/4_software_engineering/_index.md): 데이터 메시(Data Mesh)와 본질적인 사상을 공유하는 도메인 주도 분산 설계 철학.