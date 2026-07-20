---
title: "Columnar Storage Format Parquet Orc"
date: "2026-04-05"
tags:
  - "studynote-data-engineering"
weight: 45
---
> **핵심 인사이트**
> 1. 컬럼형 저장 형식(Columnar Storage Format)은 행(Row) 대신 열(Column) 단위로 데이터를 저장해 분석 쿼리의 I/O를 극적으로 줄이는 빅데이터 핵심 기술 — 수백만 행에서 특정 열 5개만 조회할 때 행 기반은 전체 행을 읽지만, 컬럼형은 해당 열만 읽는다.
> 2. Apache Parquet와 ORC(Optimized Row Columnar)는 현재 빅데이터 생태계의 양대 표준 — Parquet는 Spark·다중 언어 생태계에서 강점, ORC는 Hive 최적화와 ACID 트랜잭션 지원에서 강점이며, 두 형식 모두 압축·술어 푸시다운(Predicate Pushdown)을 지원한다.
> 3. Parquet/ORC의 핵심 최적화 기법은 Row Group + Column Chunk + 압축 + 통계(Min/Max/Bloom Filter) — 쿼리 엔진이 Row Group 통계를 이용해 불필요한 Row Group 자체를 건너뛰는 "스킵핑"이 성능의 핵심이다.

---

## Ⅰ. 행 기반 vs 컬럼 기반

```
저장 형식 비교:

샘플 데이터 (3행 × 4열):
  id | name  | age | salary
  1  | Alice |  30 | 5000
  2  | Bob   |  25 | 4000
  3  | Carol |  35 | 6000

행 기반 (Row-Oriented):
  저장: [1,Alice,30,5000][2,Bob,25,4000][3,Carol,35,6000]

  장점: 행 단위 CRUD 빠름 (OLTP)
  단점: 전체 열 다 읽어야 함 (분석)

컬럼 기반 (Column-Oriented):
  저장: [1,2,3][Alice,Bob,Carol][30,25,35][5000,4000,6000]

  장점: 필요한 열만 읽음 (OLAP)
  압축률 높음 (같은 타입 데이터)

쿼리 차이:
  SELECT AVG(salary) FROM employees

  행 기반: id, name, age, salary 모두 읽음 (100%)
  컬럼형: salary 열만 읽음 (25%)

  1억 행, 100열 테이블:
  행 기반: 5개 열 쿼리 -> 100열 전부 읽음
  컬럼형: 5개 열 쿼리 -> 5열만 읽음 (95% I/O 절감)

압축 효율:
  컬럼 내 데이터 = 동일 타입 + 유사 값

  salary열: 4000, 5000, 4500, 5200...
  -> 델타 인코딩: +0, +1000, -500, +700
  -> RLE: 같은 값 반복 (부서 코드 등)
  -> 압축률 5~10× 일반적
```

> 📢 **섹션 요약 비유**: 컬럼형은 책장 정리법 — 행 기반은 책 한 권씩(행) 정리, 컬럼형은 같은 색 책(열)끼리 정리. "빨간 책 몇 권?" 물으면 빨간 칸만 보면 OK!

---

## Ⅱ. Apache Parquet

```
Apache Parquet:
  Apache Foundation 오픈소스 (2013)
  Twitter + Cloudera 공동 개발

파일 구조:
  +-----------------------------+
  | Magic Number (PAR1)         |
  +-----------------------------+
  | Row Group 1                 |
  |   Column Chunk A            |
  |     Page 1, Page 2, ...     |
  |   Column Chunk B            |
  |     Page 1, Page 2, ...     |
  +-----------------------------+
  | Row Group 2                 |
  |   ...                       |
  +-----------------------------+
  | Footer (메타데이터)          |
  |   스키마, 통계(Min/Max)      |
  |   Row Group 오프셋          |
  | Magic Number (PAR1)         |
  +-----------------------------+

핵심 구성:
  Row Group: 기본 128MB~1GB
    -> 병렬 처리 단위
  Column Chunk: 열 데이터 블록
  Page: 인코딩·압축 단위 (1MB)

인코딩:
  Dictionary Encoding: 반복 값 사전화
  RLE (Run-Length Encoding): 연속 값 압축
  Bit Packing: 정수 소형 비트 패킹
  Delta Encoding: 연속 증가 값

압축 코덱:
  Snappy (기본): 빠름, 적당한 압축률
  GZIP: 높은 압축률, 느림
  LZ4: 초고속, 중간 압축률
  ZSTD: 빠름 + 높은 압축률 (권장)

술어 푸시다운:
  Row Group Footer 통계:
  min_value=1000, max_value=5000

  WHERE salary > 6000:
  -> 이 Row Group 건너뜀! (I/O 절감)
```

> 📢 **섹션 요약 비유**: Parquet는 목차 있는 백과사전 — Row Group = 챕터, 목차(Footer 통계)로 "이 챕터에 찾는 내용 있나?" 확인. 없으면 챕터 통째로 건너뜀!

---

## Ⅲ. Apache ORC

```
Apache ORC (Optimized Row Columnar):
  Hive 프로젝트에서 탄생 (2013)
  Hortonworks 개발

파일 구조:
  +---------------------------+
  | ORC Header (Magic: ORC)   |
  +---------------------------+
  | Stripe 1                  |
  |   Index Data              |
  |   Row Data (컬럼별)        |
  |   Stripe Footer           |
  +---------------------------+
  | Stripe 2                  |
  |   ...                     |
  +---------------------------+
  | File Footer               |
  |   Stripe 목록              |
  |   스키마                   |
  |   통계                    |
  | Postscript                |
  +---------------------------+

Stripe = Parquet Row Group (기본 256MB)

ORC 특화 기능:

1. ACID 트랜잭션:
   Hive 3.0+ 지원
   INSERT, UPDATE, DELETE 지원
   (Parquet는 기본 append-only)

2. Bloom Filter:
   특정 값 존재 여부 빠른 확인
   WHERE id = 12345 -> Bloom Filter로 Stripe 스킵

3. 경량 인덱스:
   Row Index (10,000행마다 통계)
   Bloom Filter Index

4. LLAP (Live Long and Process):
   Hive LLAP과 통합 최적화
   인메모리 캐시

ORC 적합 환경:
  Hive 기반 데이터 웨어하우스
  UPDATE/DELETE 필요한 SCD(천천히 변하는 차원)
  Hive ACID 트랜잭션
```

> 📢 **섹션 요약 비유**: ORC는 Hive 최적화 선반 — Hive 창고(Hive 웨어하우스)에 최적화된 정리 방식. 특히 물건 교체(UPDATE/ACID)가 필요할 때 강점!

---

## Ⅳ. Parquet vs ORC vs CSV

```
비교표:

항목           | CSV      | Parquet   | ORC
---------------|----------|-----------|----------
저장 방식      | 행 기반  | 컬럼 기반 | 컬럼 기반
압축 지원      | 없음     | 있음      | 있음
스키마 내장    | 없음     | 있음      | 있음
읽기 성능 (분석) | 낮음  | 높음      | 높음
ACID 트랜잭션  | 없음     | 없음(기본)| 있음 (Hive)
파싱 오버헤드  | 없음     | 있음      | 있음
생태계 지원    | 범용     | Spark 최적| Hive 최적
Bloom Filter   | 없음     | 있음(선택)| 있음
복잡 타입 지원 | 없음     | 중첩 스키마| 중첩 스키마

선택 가이드:
  CSV: 소규모 데이터, 호환성 최우선
  Parquet: Spark, Presto/Trino, Athena, Iceberg
  ORC: Hive, Hive ACID 트랜잭션 필요 시

현재 트렌드:
  Parquet -> Apache Iceberg, Delta Lake 표준
  ORC -> Hive 기반 환경

  Delta Lake: Parquet 기반 + ACID 보완
  Apache Iceberg: Parquet/ORC/Avro 지원

성능 벤치마크 (1억 행, 10열 중 3열 쿼리):
  CSV:     100s
  Parquet: 8s   (ZSTD 압축, 술어 푸시다운)
  ORC:     10s  (ZLIB 압축, Bloom Filter)
```

> 📢 **섹션 요약 비유**: Parquet vs ORC는 삼성 vs LG 가전 — 둘 다 훌륭하지만, Spark 집(생태계)에는 Parquet가, Hive 집에는 ORC가 잘 맞아요!

---

## Ⅴ. 실무 시나리오 — 데이터 레이크 최적화

```
전자상거래 데이터 레이크 최적화:

초기 상황:
  S3에 CSV 파일 적재
  Athena 쿼리: 일 주문 분석 -> 10~30분
  비용: 쿼리당 $50~200 (스캔 비용)

문제 진단:
  Athena = Presto 기반 (S3 스캔)
  CSV: 스키마 없음, 압축 없음, 전체 스캔

  일 주문 테이블: 5억 행, 50열
  주요 쿼리: 5열만 사용, 날짜 필터링

최적화 전략:

1. CSV -> Parquet 변환 (ZSTD 압축):
   Glue ETL로 일배치 변환

   결과:
   CSV: 500GB/일 -> Parquet: 80GB/일 (84% 압축)

2. Hive 파티셔닝:
   S3 키: s3://bucket/orders/year=2024/month=01/day=15/

   WHERE order_date = '2024-01-15'
   -> 해당 파티션만 스캔

3. Row Group 크기 최적화:
   Row Group = 256MB (대용량 배치 쿼리 최적)

4. 술어 푸시다운 최적화:
   컬럼 순서 = 카디널리티 높은 것 먼저
   -> Bloom Filter 효과 극대화

결과:
  쿼리 시간: 10~30분 -> 30~90초
  스캔 비용: $50~200 -> $2~8 (96% 절감)
  월 Athena 비용: 500만원 -> 20만원

  추가: Delta Lake 전환으로 ACID 지원
  (일 데이터 수정 필요 케이스 처리)
```

> 📢 **섹션 요약 비유**: 데이터 레이크 최적화는 창고 정리 — CSV(무분류 박스) -> Parquet(카테고리별 투명 박스). "1월 주문"만 찾을 때 해당 칸만 보면 OK. 비용 96% 절감!

---

## 📌 관련 개념 맵

```
컬럼형 저장 형식
+-- Apache Parquet
|   +-- Row Group / Column Chunk / Page
|   +-- 압축 (Snappy, ZSTD)
|   +-- 술어 푸시다운
+-- Apache ORC
|   +-- Stripe / Index / Bloom Filter
|   +-- Hive ACID
+-- 비교
|   +-- CSV (행 기반)
|   +-- Avro (직렬화)
+-- 상위 기술
    +-- Delta Lake (Parquet + ACID)
    +-- Apache Iceberg (Parquet/ORC)
    +-- Apache Hudi
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[RC File / SequenceFile (2000s)]
Hadoop 초기 컬럼형 시도
제한적 기능
      |
      v
[Parquet + ORC 등장 (2013)]
Hadoop 생태계 표준 컬럼형
Twitter/Hortonworks 주도
      |
      v
[Delta Lake / Iceberg / Hudi (2016~)]
컬럼형 + ACID + 스냅샷
레이크하우스 패러다임
      |
      v
[현재: 오픈 테이블 포맷]
Apache Iceberg 표준 부상
Parquet 기반 멀티엔진
AWS, Snowflake, Databricks 지원
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 컬럼형은 같은 종류끼리 묶기 — CSV가 "1번 사람 모든 정보"를 묶으면, Parquet는 "모든 사람의 나이"를 묶어요. 나이만 필요할 때 엄청 빠르죠!
2. 술어 푸시다운은 목차 이용하기 — "1월 데이터"를 찾을 때 목차(Row Group 통계) 보고 12월 데이터는 통째로 건너뛰어요!
3. Parquet는 Spark 친구, ORC는 Hive 친구 — 같은 기능이지만 각자 잘 맞는 생태계가 달라요. 쓰는 도구에 맞게 선택!
