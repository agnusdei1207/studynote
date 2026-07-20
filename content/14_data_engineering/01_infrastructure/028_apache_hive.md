---
title: "Apache Hive"
date: "2026-04-29"
tags:
  - "studynote-data-engineering"
weight: 28
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Hive는 HDFS(또는 S3) 위에 SQL 인터페이스(HiveQL)를 제공하는 데이터 웨어하우스 인프라다. SQL 쿼리를 MapReduce/Tez/Spark 잡으로 변환하여 대규모 배치 처리를 SQL로 가능하게 한다.
> 2. **가치**: SQL 기반 분석가가 Java 없이 페타바이트급 데이터를 분석할 수 있게 했다. Hive Metastore(HMS)는 테이블 스키마·파티션 정보를 중앙 집중 관리하여 Spark, Presto, Trino 등 모든 데이터 엔진이 공유하는 메타데이터 표준이 됐다.
> 3. **판단 포인트**: Hive는 배치 분석에 강하지만 인터랙티브 쿼리(초 단위 응답)에는 약하다. 인터랙티브 쿼리는 Presto/Trino(MPP), Spark SQL(인메모리), Impala(C++ 기반)가 대안이다. Hive Metastore는 여전히 레이크하우스(Lakehouse) 메타데이터 허브로 핵심 역할을 유지한다.

---

## Ⅰ. 개요 및 필요성

```text
+----------------------------------------------------------+
|                Apache Hive 아키텍처                       |
+----------------------------------------------------------+
|                                                           |
|  분석가  ->  HiveQL (SQL)                                 |
|                 |                                         |
|          Hive Query Compiler                              |
|                 | SQL -> MapReduce/Tez/Spark Job 변환      |
|          Hive Metastore (HMS)                             |
|          (테이블 스키마·파티션·통계 중앙 저장)            |
|                 |                                         |
|          실행 엔진 (MapReduce / Tez / Spark)              |
|                 |                                         |
|          HDFS / S3 / ADLS (스토리지)                     |
|                                                           |
+----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Apache Hive는 HDFS용 SQL 번역기다. 분석가가 SQL을 말하면 Hive가 이를 Hadoop이 이해하는 MapReduce 언어로 번역해서 실행하고 결과를 가져온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Hive 핵심 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| **HiveQL** | ANSI SQL 호환 쿼리 언어 |
| <strong>Hive Metastore (HMS)</strong> | 테이블 스키마·파티션·통계 중앙 저장소 |
| <strong>쿼리 컴파일러</strong> | SQL -> 실행 계획 최적화 |
| **실행 엔진** | MapReduce / Tez / Spark 중 선택 |
| **SerDe** | 데이터 직렬화/역직렬화 (JSON, Parquet, ORC) |

### Hive 파티셔닝과 버킷팅

```text
파티셔닝 (Partitioning):
  CREATE TABLE sales (id INT, amount DOUBLE)
  PARTITIONED BY (year INT, month INT);
  -> 연·월별 디렉토리로 분리 -> 쿼리 시 불필요 파티션 스킵

버킷팅 (Bucketing):
  CLUSTERED BY (customer_id) INTO 32 BUCKETS;
  -> 해시 기반 데이터 분산 -> JOIN 최적화
```

- **📢 섹션 요약 비유**: Hive 파티셔닝은 도서관 책 분류 체계다. 연도·월별로 책(데이터)을 서가에 정리해서 "2024년 3월" 데이터가 필요할 때 다른 서가는 아예 뒤지지 않는다.

---

## Ⅲ. 비교 및 연결

| 비교 | Hive | Presto/Trino | Spark SQL |
|:---|:---|:---|:---|
| 쿼리 응답 | 분~시간 | 초 | 초~분 |
| 배치 처리 | 최강 | 중간 | 강함 |
| 메타데이터 | HMS 표준 | HMS 호환 | HMS 호환 |
| 사용 사례 | ETL·대규모 배치 | 인터랙티브 | 스트리밍+배치 |

- **📢 섹션 요약 비유**: Hive vs Presto는 느린 화물 기차 vs 빠른 고속열차다. 화물 기차(Hive)는 엄청 많은 화물(대규모 배치)을 운반하고, 고속열차(Presto)는 빠르게 목적지에 도달하지만 용량이 제한적이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Lakehouse에서 Hive Metastore의 역할

```text
데이터 레이크하우스 메타데이터 허브:

  Spark SQL -+
  Trino      +--> Hive Metastore -> S3/HDFS 데이터
  Presto     |   (테이블 스키마·파티션 정보)
  Flink      -+

-> 모든 엔진이 HMS를 통해 동일한 테이블 메타데이터 공유
-> 현대적 대안: AWS Glue Catalog, Nessie, Unity Catalog
```

### ORC vs Parquet 파일 형식

```text
ORC (Optimized Row Columnar):
  - Hive 최적화 포맷, 인덱스·통계 내장
  - Hive ACID(트랜잭션) 지원

Parquet:
  - 범용 컬럼형 포맷, 중립적
  - Spark·Trino·다양한 엔진 최적화
```

- **📢 섹션 요약 비유**: Hive Metastore는 회사 공용 연락처 서버다. 팀마다 다른 커뮤니케이션 앱(Spark, Trino, Flink)을 쓰지만 모두 같은 회사 연락처(메타데이터)를 공유해서 같은 테이블 정보를 본다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong>SQL 접근성</strong> | 비개발자도 페타바이트 분석 |
| <strong>메타데이터 표준</strong> | HMS가 레이크하우스 허브 |
| **비용 효율** | S3 기반 대규모 배치 처리 |

Apache Iceberg·Delta Lake의 등장으로 Hive의 ACID 트랜잭션 한계가 보완됐다. 현대 레이크하우스에서는 Hive 쿼리 엔진보다 Hive Metastore의 역할이 더 중요하며, AWS Glue Catalog, Databricks Unity Catalog 등 관리형 메타스토어로 대체되는 추세다.

- **📢 섹션 요약 비유**: Apache Hive의 진화는 도서관 변천과 같다. 책(데이터) 검색 방법(Hive 쿼리 엔진)은 더 빠른 방법(Spark, Trino)으로 교체됐지만, 도서관 목록 카드(Hive Metastore)는 여전히 모든 사람이 사용하는 핵심 인프라로 남아 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Hive Metastore</strong> | 데이터 레이크하우스 메타데이터 허브 |
| **HiveQL** | SQL을 Hadoop 잡으로 변환 |
| <strong>ORC/Parquet</strong> | Hive 최적 컬럼형 파일 포맷 |
| **Presto/Trino** | Hive 대비 인터랙티브 쿼리 가속 |
| <strong>Apache Iceberg</strong> | Hive ACID 한계 극복 차세대 포맷 |

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS + MapReduce — 원시 Hadoop 배치 처리]
    |
    v
[Apache Hive — SQL 인터페이스, HMS 메타데이터 표준화]
    |
    v
[Tez/Spark 엔진 — Hive 쿼리 실행 가속]
    |
    v
[Presto/Trino — 인터랙티브 MPP SQL 엔진]
    |
    v
[Iceberg/Delta + Unity Catalog — 오픈 테이블 포맷 + 통합 메타스토어]
```

### 👶 어린이를 위한 3줄 비유 설명

1. Apache Hive는 HDFS라는 거대 창고에 SQL이라는 친숙한 언어로 질문할 수 있게 해주는 번역기예요!
2. Hive Metastore는 도서관 목록 카드처럼 모든 데이터의 위치와 구조를 기록해둬요!
3. 요즘은 Hive보다 빠른 Trino, Spark를 더 많이 쓰지만 Metastore는 여전히 모두가 공유하는 핵심 인프라랍니다!
