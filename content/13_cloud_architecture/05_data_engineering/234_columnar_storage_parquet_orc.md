---
title: "Columnar Storage Parquet Orc"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 234
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컬럼 지향 스토리지(Columnar Storage)는 데이터를 <strong>행(Row) 단위가 아닌 열(Column) 단위로 압축 저장</strong>하여 OLAP 분석 쿼리 시 필요한 열만 읽어 I/O를 극적으로 절감한다.
> 2. **가치**: 동일 열의 데이터는 타입이 동일하므로 <strong>압축률이 5~10배 높고</strong>, 특정 열만 선택적으로 읽는 OLAP 쿼리에서 로우 기반 대비 수십 배 빠른 스캔 성능을 발휘한다.
> 3. **판단 포인트**: Apache Parquet은 범용 컬럼 포맷, Apache ORC는 Hive/Spark 최적화 포맷으로, 데이터 레이크·레이크하우스의 <strong>표준 저장 포맷</strong>으로 반드시 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

전통 RDBMS는 한 행의 모든 컬럼을 디스크에 연속 저장한다(Row-oriented). INSERT/UPDATE 트랜잭션에는 효율적이지만, "전체 주문 중 매출 금액 합계"처럼 특정 컬럼만 읽는 OLAP 쿼리에서는 불필요한 컬럼까지 전부 읽어야 하는 I/O 낭비가 발생한다.

```
[Row-oriented 저장]
Row 1: [order_id=1][customer_id=C001][product="책"][amount=30000][date=2024-01-01]
Row 2: [order_id=2][customer_id=C002][product="노트북"][amount=1500000][date=2024-01-02]
...

SELECT SUM(amount) FROM orders;  -> 모든 행의 모든 컬럼을 읽어야 함

[Column-oriented 저장]
order_id: [1][2][3][4]...
customer_id: [C001][C002][C003]...
product: [책][노트북][마우스]...
amount: [30000][1500000][25000]...  <- 이것만 읽음!
date: [2024-01-01][2024-01-02]...

SELECT SUM(amount) FROM orders;  -> amount 컬럼 파일만 읽음 (I/O 95% 절감)
```

📢 **섹션 요약 비유**: Row-oriented는 엑셀 시트를 행 단위로 저장하는 것이고, Column-oriented는 같은 항목(열)끼리 묶어서 저장하는 것이다. "전체 직원 연봉 합계"를 구할 때, 연봉 열 하나만 꺼내면 되니 훨씬 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Apache Parquet 파일 구조

```
+--------------------------------------------------------+
|                 Parquet 파일 구조                        |
|                                                        |
|  Magic Number (4 bytes)                                |
|  +-------------------------------------------------+  |
|  | Row Group 1 (행 그룹, 예: 128MB)                 |  |
|  |  +-----------------------------------------+    |  |
|  |  | Column Chunk 1 (order_id)               |    |  |
|  |  |  - Data Pages (RLE+Dictionary 인코딩)   |    |  |
|  |  |  - Column Statistics (min/max/null cnt) |    |  |
|  |  +-----------------------------------------+    |  |
|  |  | Column Chunk 2 (amount)                 |    |  |
|  |  |  - Data Pages                           |    |  |
|  |  |  - Column Statistics                    |    |  |
|  |  +-----------------------------------------+    |  |
|  +-------------------------------------------------+  |
|  | Row Group 2 ...                                  |  |
|  +-------------------------------------------------+  |
|  File Footer (스키마, Row Group 위치, 통계)              |
|  Magic Number (4 bytes)                                |
+--------------------------------------------------------+
```

### Parquet 압축 및 인코딩 최적화

| 최적화 기법 | 설명 | 효과 |
|:---|:---|:---|
| **Dictionary Encoding** | 반복 값을 정수 ID로 치환 | 문자열 컬럼 압축 우수 |
| <strong>RLE (Run-Length Encoding)</strong> | 연속 동일 값 압축 | 정렬된 컬럼 효율적 |
| <strong>Delta Encoding</strong> | 이전 값과의 차이만 저장 | 타임스탬프, 순차 ID |
| <strong>Bit Packing</strong> | 필요 최소 비트 수로 저장 | 정수 범위 최적화 |
| <strong>압축 코덱</strong> | Snappy, Zstd, Gzip | Snappy: 속도^, Zstd: 압축률^ |

### Predicate Pushdown (조건 푸시다운)

```
SELECT * FROM orders WHERE amount > 1000000

Parquet 엔진 동작:
1. File Footer에서 Row Group 통계 확인
2. Row Group 2: amount max=500000 -> amount > 1000000 없음 -> 스킵!
3. Row Group 5: amount max=3000000 -> 조건 가능성 -> 읽기

효과: 전체 파일의 70~90% 읽지 않고 건너뜀
```

📢 **섹션 요약 비유**: Predicate Pushdown은 책 목차(Footer 통계)를 먼저 보고, 관련 없는 챕터는 넘기는 것이다. "200페이지 이후 내용만 필요하다"면 목차에서 바로 200페이지로 이동하듯, 통계로 불필요한 Row Group을 건너뛴다.

---

## Ⅲ. 비교 및 연결

### Parquet vs ORC vs Avro vs CSV

| 비교 항목 | Parquet | ORC | Avro | CSV |
|:---|:---|:---|:---|:---|
| **저장 방식** | 컬럼 지향 | 컬럼 지향 | 행 지향 | 행 지향 |
| <strong>압축률</strong> | 높음 | 높음 | 중간 | 낮음 |
| <strong>OLAP 쿼리</strong> | 우수 | 우수 | 보통 | 나쁨 |
| <strong>쓰기 성능</strong> | 보통 | 보통 | 우수 | 우수 |
| **스트리밍** | 제한 | 제한 | 우수 | 우수 |
| <strong>스키마 진화</strong> | 제한 | 제한 | 우수 | 없음 |
| **생태계** | 범용 (Spark, Hive, Presto) | Hive/ORC 최적 | Kafka 스키마 | 범용 |
| **적합 사례** | 데이터 레이크 OLAP | Hive DW | 스트리밍 직렬화 | 소규모 교환 |

### 파일 포맷 선택 기준

```
[워크로드별 포맷 선택]
OLAP 분석 (읽기 중심):  Parquet > ORC >> Avro > CSV
스트리밍 이벤트 직렬화: Avro (Protobuf) >> Parquet
레이크하우스 테이블:    Parquet (Delta Lake / Iceberg)
Hive DW:               ORC (Hive 네이티브 최적화)
데이터 교환:            Parquet > CSV
ML 피처 스토어:         Parquet (Feast 등)
```

📢 **섹션 요약 비유**: 포맷 선택은 짐을 싸는 방식이다. 여행 캐리어(Parquet/ORC)는 체계적으로 정리해 공간 절약, 긴급 배낭(Avro)은 빠르게 넣고 빼기, 비닐백(CSV)은 단순하지만 비효율이다. 분석 여행(OLAP)엔 캐리어, 마라톤(스트리밍)엔 배낭이 맞다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Parquet 최적화 실무 가이드

```python
# Spark에서 Parquet 최적화 저장
df.write \
  .partitionBy("date", "region")  # 파티션 분할 (쿼리 범위 축소)
  .option("compression", "zstd")  # Zstandard 압축 (압축률+속도 균형)
  .option("maxRecordsPerFile", 1000000)  # Row Group 크기 조절
  .mode("overwrite") \
  .parquet("s3://bucket/silver/orders/")

# 읽기 최적화
spark.conf.set("spark.sql.parquet.filterPushdown", "true")
spark.conf.set("spark.sql.parquet.mergeSchema", "false")
df = spark.read.parquet("s3://bucket/silver/orders/") \
     .filter(col("date") >= "2024-01-01") \  # Predicate Pushdown
     .select("order_id", "amount", "status")  # Column Pruning
```

### 파티셔닝 전략

```
[파티셔닝 설계 예시]
s3://bucket/orders/
+-- year=2024/month=01/day=01/part-00000.parquet
+-- year=2024/month=01/day=02/part-00000.parquet
...

쿼리: WHERE date = '2024-01-15'
-> year=2024/month=01/day=15/ 폴더만 읽음 (나머지 99% 스킵)

주의: 파티션 과세분화 (너무 많은 소형 파일) 방지
     적정 파일 크기: 128MB ~ 512MB
```

📢 **섹션 요약 비유**: 파티셔닝은 서류함에 날짜별로 구분자(탭)를 꽂아두는 것이다. 1월 15일 서류만 필요하면 전체를 뒤지지 않고 "1월 탭" 안에서 "15일 탭"을 바로 꺼낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 정량 기준 |
|:---|:---|
| <strong>압축률</strong> | CSV 대비 5~10배 저장 공간 절감 |
| <strong>쿼리 속도</strong> | Row 기반 대비 OLAP 쿼리 5~50배 빠름 |
| **I/O 절감** | Column Pruning + Predicate Pushdown으로 90%+ I/O 절감 |
| **스토리지 비용** | S3 비용 50~80% 절감 (CSV -> Parquet 전환) |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong>쓰기 성능</strong> | Row 기반 대비 쓰기 속도 느림 (컬럼 재조합 비용) |
| <strong>소형 파일 문제</strong> | 소규모 배치 쓰기 시 파일 수 폭발 (OPTIMIZE 필요) |
| **스트리밍 직렬화 불리** | 이벤트 단위 쓰기에는 Avro/Protobuf 선호 |
| **실시간 행 업데이트 어려움** | 컬럼 지향 특성 상 단건 UPDATE 비효율 |

📢 **섹션 요약 비유**: Parquet은 연필 케이스다. 연필(데이터)을 종류별(컬럼별)로 정렬해 넣으면 꺼낼 때 빠르고 공간도 절약된다. 단, 처음 정리하는 시간(쓰기 비용)이 필요하고, 연필 한 자루씩 추가하는 것(단건 업데이트)은 번거롭다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| OLAP | 컬럼 지향 스토리지가 가장 큰 성능 이점을 발휘하는 쿼리 패턴 |
| 데이터 레이크 | Parquet/ORC가 표준 파일 포맷으로 사용되는 저장소 |
| Delta Lake / Iceberg | Parquet 위에 트랜잭션 레이어를 추가한 테이블 포맷 |
| Predicate Pushdown | 컬럼 통계 기반 읽기 스킵으로 쿼리 최적화 |
| Apache Spark | Parquet 읽기·쓰기 최적화의 핵심 엔진 |
| 파티셔닝 | 컬럼 지향 포맷과 결합하여 쿼리 범위 최소화 |
| Avro | 스트리밍 직렬화용 행 지향 포맷, Kafka 스키마 레지스트리 |

### 👶 어린이를 위한 3줄 비유 설명
1. 컬럼 지향 저장은 학용품을 종류별로 보관하는 것이다. 연필통에는 연필만, 자 통에는 자만 넣으면, "연필 몇 개야?"라고 물을 때 연필통만 열면 된다.

### 📈 관련 키워드 및 발전 흐름도

```text
행 지향 (Row): OLTP 최적화 (INSERT/UPDATE 빠름)
    |
    v
컬럼 지향 (Columnar): OLAP 최적화 (집계 쿼리 빠름)
    +-► Parquet · ORC: 파일 포맷
    +-► 압축률 ^: 같은 타입 데이터 연속 저장
    |
    v
벡터화 실행: SIMD · Arrow 인메모리 포맷
```
2. Parquet은 잘 정리된 서랍장이다. 각 서랍에 같은 종류의 물건이 빽빽이 정리되어(압축), 필요한 서랍만 열어도(컬럼 선택) 원하는 걸 빠르게 찾을 수 있다.
3. CSV는 모든 물건을 큰 상자에 섞어 넣은 것이다. 단순하지만, 연필을 찾으려면 상자 전체를 뒤져야 해서 시간이 오래 걸린다.
