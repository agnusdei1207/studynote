---
title: "Data Lakehouse"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 258
---
> **핵심 인사이트**
> 1. 데이터 레이크하우스(Data Lakehouse)는 데이터 레이크의 유연성·저비용과 데이터 웨어하우스의 ACID·성능·거버넌스를 결합한 하이브리드 아키텍처 — Databricks·Delta Lake가 선도하며, 클라우드 스토리지(S3, ADLS) 위에서 OLAP 수준의 분석 성능을 달성한다.
> 2. 레이크하우스의 핵심 기술은 오픈 테이블 포맷(Delta Lake, Apache Iceberg, Apache Hudi) — 파케이(Parquet) 파일 위에 메타데이터 레이어를 추가해 ACID 트랜잭션·스키마 진화·타임 트래블(Time Travel)을 지원하며, 벤더 잠금 없이 상호운용성을 보장한다.
> 3. 레이크하우스는 데이터 레이크->웨어하우스 이중 구조의 비효율을 해결 — 동일 데이터를 레이크와 웨어하우스 양쪽에 중복 저장·동기화하는 비용과 복잡성을 제거하며, 데이터 사이언스(ML/AI)와 BI 분석을 단일 플랫폼에서 통합 지원한다.

---

## Ⅰ. 레이크하우스 등장 배경

```
데이터 아키텍처 진화:

1세대: 데이터 웨어하우스 (DW)
  정형 데이터 + SQL + ACID
  장점: 고성능 분석, 데이터 품질
  단점: 비싸고, 비정형 데이터 미지원
  예: Teradata, Oracle DW

2세대: 데이터 레이크
  원시 데이터 + Hadoop/S3
  장점: 저비용, 모든 데이터 유형
  단점:
  - ACID 없음 -> 데이터 일관성 문제
  - 성능 낮음
  - 거버넌스 부재 ("데이터 늪")
  - BI 도구 연동 어려움
  예: Hadoop HDFS, S3 기반 레이크

현실: 이중 구조 비효율
  레이크 <- ETL -> 웨어하우스

  문제:
  데이터 중복 (2배 스토리지)
  동기화 지연 (레이크 -> DW ETL 지연)
  ML: 레이크에서 학습
  BI: 웨어하우스에서 쿼리
  -> 두 팀 간 데이터 불일치

3세대: 레이크하우스
  레이크 + 웨어하우스 통합
  오픈 포맷 위에 ACID + 거버넌스

  장점:
  ML/AI + BI 단일 플랫폼
  벤더 독립 (오픈 포맷)
  비용 효율 (S3 기반)
  실시간 + 배치 통합
```

> 📢 **섹션 요약 비유**: 레이크하우스는 복합 쇼핑몰 — 재래시장(레이크: 다양하지만 지저분)과 백화점(웨어하우스: 정갈하지만 비쌈)을 합친 것. 다양하면서도 체계적, 저렴하면서도 품질 있는!

---

## Ⅱ. 오픈 테이블 포맷

```
오픈 테이블 포맷 (Open Table Format):

공통 구조:
  클라우드 스토리지 (S3, GCS, ADLS)
  파케이(Parquet) 파일 + 메타데이터 레이어
  -> ACID, 타임 트래블, 스키마 관리

Delta Lake (Databricks, 2019):
  트랜잭션 로그: JSON 기반
  ACID: O
  타임 트래블: O (버전 기반)
  스키마 진화: O
  통합: Spark, Delta Sharing

  DELETE: 물리 삭제 대신 소프트 삭제 -> Vacuum
  MERGE INTO: Upsert (중요 기능)

  예:
  MERGE INTO target t
  USING source s ON t.id = s.id
  WHEN MATCHED THEN UPDATE SET t.value = s.value
  WHEN NOT MATCHED THEN INSERT *

Apache Iceberg (Netflix, 2018):
  메타데이터: Avro + Parquet
  스냅샷 기반: 각 커밋 = 스냅샷
  Partition Evolution: 스키마 변경 없이 파티셔닝 변경
  Row-Level Delete: 효율적 개별 행 삭제
  통합: Trino, Spark, Flink, Hive

  Trino + Iceberg = 고성능 오픈 레이크하우스

Apache Hudi (Uber, 2016):
  Incremental Processing 특화
  COW (Copy-On-Write): 읽기 최적화
  MOR (Merge-On-Read): 쓰기 최적화
  통합: Spark, Presto
  사용: Uber, Robinhood (실시간 업데이트)

비교:
  Delta Lake: Databricks 생태계 강함
  Iceberg: 가장 넓은 엔진 지원 (중립적)
  Hudi: 실시간 증분 처리 특화
```

> 📢 **섹션 요약 비유**: 오픈 테이블 포맷은 스마트 서류 정리함 — 파케이 파일(서류)에 이력 관리(ACID), 수정 기록(타임 트래블), 목차(메타데이터)를 추가. 어떤 직원(쿼리 엔진)도 읽을 수 있어요!

---

## Ⅲ. 레이크하우스 핵심 기능

```
레이크하우스 주요 기능:

1. ACID 트랜잭션:
  동시 읽기/쓰기 안전

  예: 두 작업 동시 실행
  - 파이프라인 A: 새 데이터 추가
  - BI 도구: 현재 데이터 쿼리
  -> 격리 보장 (쿼리가 중간 상태 보지 않음)

2. 타임 트래블 (Time Travel):
  이전 버전 데이터 조회

  예 (Delta Lake):
  SELECT * FROM sales VERSION AS OF 5
  SELECT * FROM sales TIMESTAMP AS OF '2024-01-01'

  활용:
  - 실수로 삭제된 데이터 복구
  - 데이터 감사 (언제 어떤 값이었나)
  - 재현 가능한 ML 실험 (동일 데이터셋)

3. 스키마 진화 (Schema Evolution):
  기존 데이터 마이그레이션 없이 컬럼 추가/변경

  레거시 레코드: 새 컬럼 = NULL 처리
  하위 호환 유지

4. 스트리밍 + 배치 통합:
  동일 테이블에 실시간 + 배치 쓰기

  예:
  - Kafka -> Flink -> Delta Lake (스트리밍)
  - Spark 배치 -> 동일 Delta 테이블
  -> BI가 하나의 테이블에서 모두 쿼리

5. DML (Data Manipulation Language):
  UPDATE, DELETE, MERGE
  -> 레이크에서 불가능하던 기능 지원
  -> CDC (Change Data Capture) 적용 가능

6. 데이터 거버넌스:
  Unity Catalog (Databricks): 통합 카탈로그
  Apache Atlas: 오픈소스 메타데이터
  Column-Level Security
  Data Lineage (데이터 계보)
```

> 📢 **섹션 요약 비유**: 레이크하우스 기능은 스마트 은행 통장 — ACID(안전한 거래), 타임 트래블(거래 내역 조회), 스키마 진화(통장 항목 추가). 단순 파일 저장에서 완전한 데이터 관리로!

---

## Ⅳ. Databricks Lakehouse 플랫폼

```
Databricks Lakehouse Platform:

아키텍처:

클라우드 스토리지 (S3/ADLS/GCS)
         |
   Delta Lake (오픈 포맷)
         |
   Unity Catalog (거버넌스)
         |
   +------------------+
   | Delta Engine      | (쿼리 엔진)
   | (고성능 Spark)    |
   +------------------+
   |           |
ML/AI       BI/SQL
(MLflow)   (Databricks SQL)

Delta Engine:
  Spark 기반 최적화 쿼리 엔진
  10~100× 성능 향상 (표준 Spark 대비)
  Photon: 네이티브 벡터화 C++ 엔진

MLflow:
  ML 라이프사이클 관리
  실험 추적, 모델 레지스트리
  Feature Store

Databricks SQL:
  BI 도구용 서버리스 SQL 웨어하우스
  Tableau, Power BI 연결

Unity Catalog:
  통합 메타데이터 카탈로그
  3-레벨 이름공간: Catalog.Schema.Table
  Column-Level ACL
  Data Lineage

경쟁 제품:
  Snowflake: 유사 통합 플랫폼 (독점 포맷)
  BigQuery: Google의 서버리스 분석
  Synapse Analytics: Azure 통합 플랫폼

  차이: Databricks = 오픈 포맷 강조
  Snowflake = 성능·관리 편의성 강조
```

> 📢 **섹션 요약 비유**: Databricks는 데이터 올인원 — 스토리지(Delta Lake), 쿼리(SQL), ML(MLflow), 거버넌스(Unity)를 하나로 묶은 데이터 플랫폼 슈퍼마켓. 벤더 잠금 없이!

---

## Ⅴ. 실무 시나리오 — 금융사 레이크하우스 전환

```
핀테크 기업 레이크하우스 전환:

기존 구조 (이중 구조):
  S3 레이크: 원시 거래 데이터, ML 학습
  Redshift 웨어하우스: BI 분석

  문제:
  ETL 파이프라인 유지 비용: 월 500만원
  레이크 -> DW 지연: 3시간
  데이터 불일치: 레이크 vs DW 수치 다름
  Redshift 비용: 월 2,000만원

레이크하우스 전환 (Databricks + Delta Lake):

아키텍처:
  S3 -> Delta Lake 테이블
  Databricks Spark: 처리 + ML
  Databricks SQL: BI 쿼리
  Unity Catalog: 거버넌스

핵심 마이그레이션:
  Redshift 테이블 -> Delta Lake 변환
  Redshift 쿼리 -> Databricks SQL 마이그레이션

타임 트래블 활용:
  규제 감사: "2023년 12월 말 데이터 상태는?"
  SELECT * FROM transactions
  TIMESTAMP AS OF '2023-12-31 23:59:59'

스트리밍 통합:
  실시간 사기 탐지:
  Kafka -> Structured Streaming -> Delta Lake
  -> ML 모델 실시간 스코어링
  -> 결과 Delta 테이블에 저장

결과:
  ETL 파이프라인: 제거 (단일 플랫폼)
  데이터 신선도: 3시간 -> 5분
  데이터 불일치: 0 (단일 소스)
  월 인프라 비용: 2,500만원 -> 1,200만원
  ML 학습 속도: 4배 향상 (Delta Cache)
  규제 감사 대응 시간: 2주 -> 2시간
```

> 📢 **섹션 요약 비유**: 금융사 레이크하우스는 단일 장부 — 레이크(창고 장부)와 웨어하우스(회계 장부) 이중으로 기록하다가, 하나의 스마트 장부(레이크하우스)로 통합. 비용 반, 시간 1/36!

---

## 📌 관련 개념 맵

```
데이터 레이크하우스
+-- 오픈 테이블 포맷
|   +-- Delta Lake (Databricks)
|   +-- Apache Iceberg (Netflix)
|   +-- Apache Hudi (Uber)
+-- 핵심 기능
|   +-- ACID 트랜잭션
|   +-- 타임 트래블
|   +-- 스키마 진화
|   +-- 스트리밍+배치 통합
+-- 플랫폼
|   +-- Databricks Lakehouse
|   +-- Snowflake (유사)
+-- 관련 기술
    +-- Parquet (저장 포맷)
    +-- Spark (처리)
    +-- Unity Catalog (거버넌스)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[데이터 웨어하우스 (1990s)]
정형 데이터, 고비용
SQL + ACID
      |
      v
[Hadoop 데이터 레이크 (2006~)]
빅데이터, 저비용
ACID 없음, 성능 낮음
      |
      v
[이중 구조 문제 (2010s)]
레이크 + DW 동시 운영
중복, 불일치 문제
      |
      v
[Delta Lake 오픈소스 (2019)]
Databricks, ACID+레이크
레이크하우스 개념 구체화
      |
      v
[Iceberg, Hudi 경쟁 (2020~)]
오픈 포맷 경쟁
벤더 중립성 강조
      |
      v
[현재: 레이크하우스 주류화]
Databricks, Snowflake, BigQuery
AI+BI 통합 플랫폼 수렴
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 레이크하우스는 복합 쇼핑몰 — 재래시장(레이크: 뭐든 있지만 복잡)과 백화점(웨어하우스: 정갈하지만 비쌈)을 하나로 합쳤어요!
2. 타임 트래블은 데이터 되감기 — 어제 실수로 지운 데이터? "어제 버전 보여줘!" 한 줄로 복구. 데이터에도 타임머신이 있어요!
3. 오픈 포맷은 표준 USB — Delta Lake/Iceberg/Hudi 모두 같은 파케이 파일. 어떤 도구(Spark, Trino, Flink)로도 읽을 수 있는 표준 규격!
