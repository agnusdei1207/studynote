---
title: "Columnar Store Olap"
date: "2026-04-05"
tags:
  - "studynote-database"
weight: 47
---
> **핵심 인사이트**
> 1. 컬럼 기반 스토리지(Columnar Store)는 동일 컬럼의 값을 연속으로 저장하여 OLAP 분석 쿼리에서 극적인 I/O 절감을 달성 — "SELECT AVG(price) FROM orders"처럼 특정 컬럼만 읽는 분석 쿼리는 행 기반 저장보다 100배 이상 빠를 수 있다.
> 2. 컬럼 압축이 컬럼 스토리지의 또 다른 핵심 장점 — 동일 컬럼의 값은 타입이 동일하고 중복이 많아 RLE(Run-Length Encoding), 사전 인코딩(Dictionary Encoding), 비트맵 인덱스(Bitmap Index) 등으로 5~20배 압축이 가능하다.
> 3. OLTP vs OLAP의 저장 방식 선택 원칙 — 행 단위 CRUD 많은 OLTP는 행 기반(InnoDB, PostgreSQL Heap), 컬럼 집계 분석 위주 OLAP는 컬럼 기반(Redshift, BigQuery, Snowflake, ClickHouse)이 적합하며, 하이브리드 HTAP 데이터베이스가 이를 통합하는 추세다.

---

## Ⅰ. 행 기반 vs 컬럼 기반

```
저장 방식 비교:

테이블 예:
  ID | Name   | Age | Salary
  1  | Alice  | 30  | 5000
  2  | Bob    | 25  | 6000
  3  | Carol  | 35  | 4500

행 기반 저장 (Row Store):
  [1, Alice, 30, 5000] [2, Bob, 25, 6000] [3, Carol, 35, 4500]
  -> 한 행의 모든 컬럼이 연속 저장
  -> 행 삽입/조회 빠름 (OLTP 유리)

컬럼 기반 저장 (Column Store):
  ID: [1, 2, 3]
  Name: [Alice, Bob, Carol]
  Age: [30, 25, 35]
  Salary: [5000, 6000, 4500]
  -> 컬럼별로 연속 저장
  -> 컬럼 집계 빠름 (OLAP 유리)

쿼리 비교:
  SELECT AVG(Salary) FROM employees;

  행 기반: 모든 행의 모든 컬럼 읽기
  -> ID, Name, Age 불필요하지만 읽음
  -> I/O: 전체 테이블

  컬럼 기반: Salary 컬럼만 읽기
  -> ID, Name, Age 완전 건너뜀
  -> I/O: Salary 컬럼만 (예: 1/4 I/O)

  1억 행, 100개 컬럼, 3개 컬럼 집계:
  행 기반: 100개 컬럼 I/O
  컬럼 기반: 3개 컬럼 I/O (33배 절감)
```

> 📢 **섹션 요약 비유**: 컬럼 저장은 세로 서랍 — 행 기반은 가로 서랍(한 사람 정보 한 서랍). 컬럼 기반은 세로 서랍(직원들의 급여만 한 서랍). "급여 통계"엔 세로 서랍이 훨씬 빠름!

---

## Ⅱ. 컬럼 압축 기법

```
컬럼 스토리지 압축:

1. RLE (Run-Length Encoding):
  연속 동일 값을 (값, 횟수)로 압축

  원본: [부산, 부산, 부산, 서울, 서울]
  압축: [(부산, 3), (서울, 2)]

  적합: 정렬된 컬럼, 낮은 카디널리티
  예: 날짜 정렬 후 지역 코드

2. 사전 인코딩 (Dictionary Encoding):
  고유 값 -> 정수 매핑

  원본: [iPhone, Samsung, iPhone, LG, Samsung]
  사전: {iPhone:0, Samsung:1, LG:2}
  압축: [0, 1, 0, 2, 1]

  적합: 문자열, 낮은~중간 카디널리티
  예: 상품명, 지역, 카테고리

3. 비트 패킹 (Bit Packing):
  작은 정수를 최소 비트로 저장

  최댓값 < 16 -> 4비트로 충분
  (기본 int = 32비트) -> 8× 압축

4. 델타 인코딩 (Delta Encoding):
  연속 값의 차이를 저장

  원본: [100, 102, 105, 108, 110]
  델타: [100, +2, +3, +3, +2]

  적합: 단조 증가 시계열 (타임스탬프, ID)

5. ZSTD/LZ4 (범용 압축):
  위의 방법 이후 추가 범용 압축

압축 효율 예 (Parquet):
  원본: 10GB CSV
  Parquet + Snappy: 2GB (5× 압축)
  Parquet + ZSTD: 1.5GB (6.7×)
```

> 📢 **섹션 요약 비유**: 컬럼 압축은 종류별 정리 — "부산×3"으로 써서 공간 절약(RLE), 지역명 대신 코드 번호(사전 인코딩). 같은 종류끼리 모아서 훨씬 작게!

---

## Ⅲ. 대표 컬럼 스토리지 DB

```
주요 컬럼 기반 OLAP DB:

Amazon Redshift:
  AWS 관리형 데이터 웨어하우스
  컬럼 저장 + MPP(대규모 병렬 처리)
  인코딩: AZ64, LZO, Zstandard
  AQUA: 하드웨어 가속 쿼리
  TB~PB 규모

Google BigQuery:
  서버리스 (완전 관리형)
  컬럼 저장 + 드레멜(Dremel) 엔진
  스토리지/컴퓨팅 분리
  온디맨드 가격: TB당 $5
  네스티드 데이터(JSON) 지원

Snowflake:
  클라우드 멀티 플랫폼 (AWS/Azure/GCP)
  마이크로 파티션 (50~500MB)
  타임 트래블, 데이터 공유
  컴퓨팅 크레딧 기반 과금

ClickHouse:
  오픈소스, 실시간 OLAP
  초고속 집계 (초당 수십억 행)
  MergeTree 엔진
  Yandex, CloudFlare 사용

Apache Parquet:
  오픈소스 컬럼 저장 파일 포맷
  Hadoop, Spark 생태계 표준
  Snowflake, BigQuery 지원

Apache Arrow:
  인메모리 컬럼 데이터 포맷
  분석 라이브러리 간 제로카피 공유
  Pandas, R 통합

비교 선택:
  서버리스 단발성 쿼리: BigQuery
  예측 가능한 대규모 DW: Redshift/Snowflake
  실시간 분석 (초저지연): ClickHouse
  자체 관리 오픈소스: Apache Druid/Pinot
```

> 📢 **섹션 요약 비유**: 컬럼 DB 선택은 음식점 선택 — BigQuery(음식 배달: 서버리스), Redshift(패밀리 레스토랑: 예약 필요), ClickHouse(패스트푸드: 가장 빠름), Snowflake(뷔페: 유연함)!

---

## Ⅳ. HTAP — 행+컬럼 통합

```
HTAP (Hybrid Transactional/Analytical Processing):

배경:
  OLTP: 행 기반 (MySQL, PostgreSQL)
  OLAP: 컬럼 기반 (Redshift, BigQuery)

  이중 구조:
  OLTP -> ETL(수 시간) -> OLAP

  문제: 분석 데이터 신선도 낮음 (수 시간 지연)

HTAP 솔루션:

TiDB (PingCAP):
  TiKV (행 기반): OLTP
  TiFlash (컬럼 기반): 실시간 OLAP
  동일 쿼리 -> 최적 스토리지 자동 선택

  Raft 복제: TiKV -> TiFlash 실시간 동기
  ETL 없이 HTAP 가능

SingleStore (구 MemSQL):
  인메모리 행 기반 + 컬럼 기반 혼합
  한 테이블에 두 가지 저장 방식

Oracle Dual Format:
  동일 데이터를 행+컬럼 동시 저장
  In-Memory Column Store (IMCS)

MySQL HeatWave (Oracle):
  MySQL에 분산 인메모리 컬럼 엔진 추가
  OLAP 쿼리 100× 가속

한계:
  행+컬럼 동시 저장 -> 스토리지 2배 비용
  쓰기 증폭 (두 저장 방식 모두 업데이트)

  -> 순수 OLAP 워크로드엔 컬럼 전용 DB 유리
```

> 📢 **섹션 요약 비유**: HTAP는 하이브리드 자동차 — 도심(OLTP)엔 전기모터(행 기반), 고속도로(OLAP)엔 가솔린(컬럼 기반). 하나의 차에 두 동력. 편리하지만 무겁고 비싸요!

---

## Ⅴ. 실무 시나리오 — 이커머스 분석 플랫폼

```
이커머스 DW 컬럼 스토리지 최적화:

데이터:
  주문 테이블: 10억 건 (5년 누적)
  컬럼: 50개 (주문ID, 고객ID, 상품ID, 금액, ...)
  원본 크기: 2TB (CSV 기준)

Redshift 적용:

파티셔닝 (Sort Key):
  ORDER_DATE 기준 정렬
  -> 날짜 범위 쿼리 시 불필요한 블록 건너뜀

분산 키 (Dist Key):
  CUSTOMER_ID 기반 분산
  -> 고객별 집계 시 네트워크 셔플 최소화

인코딩:
  ORDER_DATE: AZ64 (날짜 최적)
  STATUS (배송상태): BYTEDICT (낮은 카디널리티)
  AMOUNT: AZ64 (숫자)
  PRODUCT_NAME: ZSTD (텍스트)

압축 결과:
  원본: 2TB
  압축 후: 280GB (7.1× 압축)
  스토리지 비용: 1/7 절감

쿼리 성능 (월별 매출 집계):
  SELECT YEAR(order_date), MONTH(order_date),
         SUM(amount), COUNT(*)
  FROM orders
  WHERE order_date >= '2024-01-01'
  GROUP BY 1, 2;

  Before (MySQL): 45분 (전체 테이블 스캔)
  After (Redshift): 8초
  -> 337× 가속 (Sort Key + 컬럼 저장)

추가 최적화:
  Materialized View: 자주 쓰는 집계 사전 계산
  Spectrum: S3 외부 데이터 직접 쿼리 (저비용)
  Concurrency Scaling: 동시 쿼리 급증 시 자동 확장
```

> 📢 **섹션 요약 비유**: 이커머스 Redshift 최적화 — 10억 주문 데이터를 날짜별 정렬(Sort Key) + 압축(7× 절감) + 컬럼 저장. "월별 매출"이 MySQL 45분 -> Redshift 8초. 337배 빠름!

---

## 📌 관련 개념 맵

```
컬럼 기반 스토리지
+-- 압축 기법
|   +-- RLE, 사전 인코딩
|   +-- 비트 패킹, 델타 인코딩
+-- 대표 DB
|   +-- Redshift, BigQuery, Snowflake
|   +-- ClickHouse, Apache Druid
+-- 파일 포맷
|   +-- Apache Parquet
|   +-- Apache Arrow (인메모리)
+-- HTAP
    +-- TiDB (TiKV+TiFlash)
    +-- MySQL HeatWave
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[C-Store 연구 (2005)]
MIT Stonebraker 등
컬럼 스토리지 학술 근거
      |
      v
[Vertica 상용화 (2007)]
C-Store 기반
엔터프라이즈 컬럼 DW
      |
      v
[클라우드 DW (2012~)]
AWS Redshift (2012)
Google BigQuery (2011)
      |
      v
[오픈 포맷 표준 (2013~)]
Apache Parquet, ORC
Hadoop 생태계 컬럼화
      |
      v
[현재: 실시간 OLAP+HTAP]
ClickHouse 고속 집계
TiDB HTAP 통합
레이크하우스+컬럼 포맷
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 컬럼 저장은 세로 서랍 — "급여만 보고 싶어"라면 급여 서랍(컬럼) 하나만 열면 돼요. 가로 서랍(행 기반)은 모든 서랍 다 열어야 해요!
2. 컬럼 압축은 반복 줄이기 — "부산부산부산" 대신 "부산×3"으로 저장(RLE). 같은 것이 많을수록 더 많이 압축!
3. HTAP는 하이브리드 자동차 — OLTP(도심 전기)와 OLAP(고속도로 가솔린)을 하나의 DB에. 편리하지만 비용은 2배!
