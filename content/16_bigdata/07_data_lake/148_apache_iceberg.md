---
title: "Apache Iceberg"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 148
---
## 핵심 인사이트 (3줄 요약)
1. Apache Iceberg는 Netflix가 고안한 오픈 테이블 포맷으로, <strong>히든 파티셔닝(Hidden Partitioning)</strong>을 통해 쿼리 작성자가 파티션 컬럼을 알지 못해도 파티션 프루닝(Partition Pruning)이 자동 적용된다.
2. <strong>파티션 진화(Partition Evolution)</strong>와 <strong>스키마 진화</strong>, <strong>스냅샷 격리</strong>, <strong>행 수준 삭제(Row-Level Delete)</strong>를 지원하여 멀티 페타바이트 분석 테이블을 안전하게 운영할 수 있다.
3. Spark, Flink, Trino, Hive, Dremio 등 다수 엔진이 네이티브 지원하여 벤더 종속 없는 <strong>멀티엔진 오픈 레이크하우스</strong>의 사실상 표준으로 자리 잡고 있다.

---

## Ⅰ. 개요 및 필요성

초기 Hive 기반 데이터 레이크는 파티션 디렉터리 구조를 그대로 노출했다(`/year=2026/month=04/day=21`). 이 방식은 사용자가 쿼리에 파티션 조건을 명시해야만 파티션 프루닝이 작동하여 실수 시 풀 스캔(Full Table Scan)이 발생했다. 또한 파티션 전략 변경 시 기존 데이터를 전부 재작성해야 하는 운영 부담이 있었다.

Netflix는 수백 PB 규모의 테이블 운영 경험에서 이 한계를 극복하기 위해 Iceberg를 설계했다. Iceberg는 테이블 메타데이터를 트리 구조(Catalog -> Snapshot -> Manifest List -> Manifest File -> Data File)로 관리하여 물리적 파티션 구조를 숨기고, 엔진이 메타데이터만 읽어 최적 접근 경로를 선택하게 한다.

| 항목 | Hive 파티셔닝 | Iceberg 히든 파티셔닝 |
|:---|:---|:---|
| 파티션 조건 명시 | 쿼리에 직접 기재 필수 | 엔진이 자동 추론 |
| 파티션 변경 | 전체 데이터 재작성 | 메타데이터만 변경 |
| 스캔 최적화 | 컬럼 기반 필터 없음 | Min/Max 기반 파일 스킵 |
| 동시성 제어 | 없음 | 낙관적 동시성 (OCC) |

> 📢 **섹션 요약 비유**: Hive는 서랍마다 이름표를 붙이고 사람이 직접 열어야 하는 서랍장이고, Iceberg는 AI 비서가 내용물을 다 파악해서 어느 서랍인지 알아서 꺼내주는 스마트 서랍장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|                 Apache Iceberg 메타데이터 트리                    |
+------------------------------------------------------------------+
|                                                                  |
|  [Catalog]  (Hive / REST / AWS Glue / Nessie)                   |
|       |                                                          |
|       +-->  [Table Metadata]  (metadata.json)                    |
|                  |   스키마 / 파티션 스펙 / 스냅샷 목록          |
|                  |                                               |
|                  +-->  [Snapshot]  (커밋 시점 스냅샷)             |
|                            |                                     |
|                            +-->  [Manifest List]  (*.avro)       |
|                                       |  파티션 범위 요약        |
|                                       |                          |
|                            +----------+----------+              |
|                            v                     v              |
|                    [Manifest File]        [Manifest File]        |
|                    (데이터 파일 목록,      (추가/삭제 델타)        |
|                     컬럼 통계 포함)                              |
|                            |                                     |
|                    +-------+--------+                            |
|                    v               v                             |
|              part-001.parquet  part-002.parquet                  |
+------------------------------------------------------------------+
```

**핵심 기능 요약**

| 기능 | 설명 | 이점 |
|:---|:---|:---|
| 히든 파티셔닝 | 파티션 변환 함수(years/months/bucket 등) 메타데이터 저장 | 쿼리 단순화, 실수 방지 |
| 파티션 진화 | 기존 데이터 재작성 없이 파티션 전략 변경 | 운영 유연성 |
| 스냅샷 격리 | 각 트랜잭션이 독립적 스냅샷 생성 | 타임 트래블 가능 |
| 행 수준 삭제 | Equality Delete / Position Delete 파일 | GDPR 삭제 지원 |
| 증분 읽기 | `incrementalScan` API로 스냅샷 간 변경분만 읽기 | 스트리밍 처리 효율화 |

> 📢 **섹션 요약 비유**: Iceberg 메타데이터 트리는 도서관 색인 시스템과 같다. 책 제목(Catalog)으로 서가 위치(Manifest)를 찾고, 서가에서 원하는 페이지(Data File)만 꺼낸다. 모든 색인이 최신으로 유지되어 새 책이 추가돼도 인덱스만 갱신하면 된다.

---

## Ⅲ. 비교 및 연결

<strong>Iceberg vs Delta Lake vs Hudi (세부 비교)</strong>

| 항목 | Iceberg | Delta Lake | Hudi |
|:---|:---|:---|:---|
| 파티셔닝 | 히든 (자동 추론) | 명시적 | 명시적 |
| 파티션 진화 | 데이터 재작성 없음 | 파티션 재작성 필요 | 제한적 지원 |
| 엔진 지원 | Spark/Flink/Trino/Hive/Dremio | Spark 중심, Trino 지원 | Spark 중심 |
| 삭제 파일 방식 | Equality/Position Delete 파일 | 새 Parquet 파일로 대체 | MOR 로그 파일 |
| 카탈로그 표준 | REST Catalog (IETF 표준화 중) | Unity Catalog | Hive Metastore |
| 클라우드 채택 | AWS Athena/Glue 기본 지원 | Databricks 기본 | Cloudera 기본 |

**주목할 트렌드**: AWS, Google Cloud, Snowflake가 Iceberg를 기본 테이블 포맷으로 채택하면서 <strong>멀티엔진 오픈 레이크하우스의 사실상 표준</strong>으로 부상하고 있다.

> 📢 **섹션 요약 비유**: Delta Lake가 애플 생태계처럼 Spark에 최적화되어 편하다면, Iceberg는 안드로이드처럼 다양한 기기(엔진)에서 동작하는 개방형 표준이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**주요 활용 시나리오**

- **대규모 히스토리 테이블**: 수십억 행 이벤트 테이블의 날짜별 파티션 자동 프루닝
- **멀티엔진 환경**: Spark로 쓰고 Trino로 쿼리하는 혼합 환경
- <strong>GDPR 삭제</strong>: Equality Delete 파일로 특정 사용자 데이터 논리 삭제 후 compaction
- <strong>CDC 파이프라인</strong>: Flink가 Kafka 변경 데이터를 Iceberg 테이블에 실시간 upsert

**학습 정리 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| 히든 파티셔닝 원리 | 파티션 변환 함수를 메타데이터에 저장, 엔진이 쿼리 필터에서 자동 추론 |
| 스냅샷 격리 메커니즘 | 각 커밋이 새 스냅샷을 생성, 구 스냅샷은 expire snapshots로 GC |
| Manifest 역할 | 데이터 파일 목록 + 컬럼별 min/max 통계 -> 파일 스킵 최적화 |
| 파티션 진화 장점 | ALTER TABLE 후 새 파일만 새 파티션 전략 적용, 기존 파일 불변 |

> 📢 **섹션 요약 비유**: Iceberg 운영은 스마트 빌딩 관리와 같다. 새 층을 추가해도 기존 층 구조를 바꾸지 않고, 모든 층의 현황은 통제 센터(메타데이터)에서 실시간으로 파악된다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 쿼리 성능 | Min/Max 통계 기반 파일 스킵으로 풀 스캔 최소화 |
| 운영 비용 절감 | 파티션 변경 시 데이터 재작성 불필요 -> 컴퓨팅 비용 절감 |
| 벤더 독립성 | 오픈 포맷으로 클라우드·엔진 변경 자유로움 |
| 규정 준수 | 행 수준 삭제로 GDPR 우측 삭제 요건 충족 |

Apache Iceberg는 2024년 이후 AWS Athena, Snowflake, Spark 3.x, Flink, Trino의 기본 테이블 포맷으로 채택되며 오픈 레이크하우스 생태계의 중심축이 됐다. 심화 학습에서는 <strong>히든 파티셔닝 원리</strong>, <strong>메타데이터 트리 구조(Manifest List -> Manifest -> Data File)</strong>, <strong>파티션 진화</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: Iceberg는 도시 지도 앱과 같다. 길이 바뀌어도(파티션 진화) 앱 지도만 업데이트하면 되고, 어느 네비게이션 앱(엔진)을 써도 같은 지도 데이터를 활용할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Manifest List | 핵심 메타데이터 | 스냅샷 내 Manifest 파일 목록 |
| Hidden Partitioning | 핵심 기능 | 파티션 변환 함수 자동 추론 |
| Snapshot | 트랜잭션 단위 | 각 커밋의 테이블 상태 |
| REST Catalog | 카탈로그 표준 | 멀티엔진 테이블 등록·조회 |
| Equality Delete | 행 삭제 방식 | 특정 컬럼 값 기준 논리 삭제 |
| Apache Nessie | 버전 관리 카탈로그 | Git과 유사한 브랜치 기반 카탈로그 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 레이크 (Data Lake)]
    |
    v
[테이블 포맷 (Table Format)]
    |
    v
[Apache Iceberg (Apache Iceberg)]
    |
    v
[타임 트래블 (Time Travel)]
```

이 흐름도는 데이터 레이크를 테이블 포맷으로 다듬고 Apache Iceberg의 타임 트래블로 확장되는 흐름을 보여준다.
### 👶 어린이를 위한 3줄 비유 설명
1. Iceberg는 스마트 도서관이에요. 책(데이터)이 어느 방(파티션)에 있는지 알아서 찾아줘서 직접 돌아다닐 필요가 없어요.
2. 도서관 구조(파티션)를 바꿔도 이미 있는 책들을 다시 옮길 필요가 없고, 새 책만 새 구조에 따라 놓으면 돼요.
3. 어떤 도서관 로봇(엔진)을 써도 같은 방식으로 책을 찾을 수 있어서 누구나 편리하게 이용할 수 있답니다.
