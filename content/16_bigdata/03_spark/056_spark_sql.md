---
title: "Spark Sql"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 56
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Spark SQL은 분산 데이터셋(RDD, Parquet, JSON, Hive 테이블 등)에 대해 표준 SQL과 DataFrame/Dataset API를 동일한 실행 엔진으로 처리하는 스파크의 구조적 처리 계층으로, 스키마 정보를 알기 때문에 Catalyst 옵티마이저가 최적 실행 계획을 자동으로 수립한다.
- **가치**: 데이터 엔지니어는 Hive 메타스토어와 연동하여 기존 SQL 워크로드를 코드 변경 없이 스파크로 이관하고, 데이터 과학자는 `spark.sql("SELECT ...")` 한 줄로 페타바이트 규모 데이터를 쿼리할 수 있어 분석 생산성이 획기적으로 향상된다.
- **판단 포인트**: 구조화된 데이터(스키마 존재)를 처리할 때는 RDD보다 반드시 DataFrame/Spark SQL을 사용해야 하며, 이는 Tungsten 엔진의 메모리 최적화와 Catalyst의 술어 푸시다운(Predicate Pushdown)이 적용되어 성능이 수 배 이상 차이가 난다.

---

## Ⅰ. 개요 및 필요성

### 1. RDD 시대의 한계

초기 Spark의 RDD는 강력했지만 근본적인 약점이 있었다.
- <strong>스키마 부재</strong>: `RDD[Row]`는 데이터 내부 컬럼 타입을 알 수 없어 스파크가 블랙박스처럼 취급
- **최적화 불가**: 사용자가 `map -> filter -> join` 순서로 작성해도 스파크는 더 나은 순서를 알아도 재배열 불가
- <strong>다양한 데이터 소스 통합 어려움</strong>: 각 포맷마다 별도 파싱 코드가 필요

### 2. Spark SQL의 해결책

Spark SQL (Apache Spark 1.3, 2014)은 <strong>데이터에 스키마를 부여</strong>함으로써 이 문제를 근본적으로 해결한다.

```python
# RDD 방식 (최적화 불가)
rdd.filter(lambda x: x[2] > 1000).map(lambda x: (x[0], x[2]))

# Spark SQL 방식 (Catalyst가 최적화)
spark.sql("SELECT user_id, amount FROM transactions WHERE amount > 1000")
df.filter(df.amount > 1000).select("user_id", "amount")
```

**📢 섹션 요약 비유**
> RDD는 "부품 목록 없이 공장을 돌리는 것"이고, Spark SQL은 "정확한 설계도(스키마)를 가지고 가장 효율적인 생산 순서를 AI가 짜주는 스마트 공장"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Spark SQL 실행 파이프라인

```
+---------------------------------------------------------------+
|  SQL 문자열 / DataFrame API / Dataset API                      |
+----------------------+----------------------------------------+
                       |
                       v
+--------------------------------------------------------------+
|  파서 (Parser) — SQL -> 비해석 논리 계획 (Unresolved LP)        |
+----------------------+---------------------------------------+
                       |
                       v
+--------------------------------------------------------------+
|  Analyzer — 카탈로그 참조 -> 해석된 논리 계획 (Resolved LP)    |
|  (테이블명, 컬럼명, 타입 검증)                                 |
+----------------------+---------------------------------------+
                       |
                       v
+--------------------------------------------------------------+
|  Catalyst Optimizer — 규칙 기반 + 비용 기반 최적화             |
|  · 술어 푸시다운 (Predicate Pushdown)                         |
|  · 컬럼 프루닝 (Column Pruning)                               |
|  · 상수 폴딩, 조인 순서 최적화                                 |
+----------------------+---------------------------------------+
                       |
                       v
+--------------------------------------------------------------+
|  물리 계획 선택 (Physical Planning) — 최적 물리 계획 선택      |
|  (SortMergeJoin vs BroadcastHashJoin 결정 등)                 |
+----------------------+---------------------------------------+
                       |
                       v
+--------------------------------------------------------------+
|  코드 생성 (Codegen) — Tungsten, JVM 바이트코드 직접 생성      |
+----------------------+---------------------------------------+
                       |
                       v
             분산 RDD 실행 (Spark Core)
```

### 2. Hive 메타스토어 연동

Spark SQL은 Hive 메타스토어(Hive Metastore)와 완벽하게 호환된다.

```python
# SparkSession 생성 시 Hive 지원 활성화
spark = SparkSession.builder \
    .config("spark.sql.warehouse.dir", "/warehouse") \
    .enableHiveSupport() \
    .getOrCreate()

# Hive 테이블 직접 쿼리
result = spark.sql("SELECT * FROM hive_db.sales WHERE year = 2024")
```

### 3. 주요 API 비교

| API 종류 | 타입 안전성 | 유연성 | 최적화 | 주요 사용자 |
|:---|:---|:---|:---|:---|
| SQL 문자열 | 런타임 검증 | 높음 | Catalyst 전적용 | SQL 사용자, BI 툴 |
| DataFrame API | 런타임 검증 | 높음 | Catalyst 전적용 | Python/R 엔지니어 |
| Dataset API | 컴파일 타임 | 보통 | Catalyst 전적용 | Scala/Java 개발자 |
| RDD API | 없음 | 최고 | 불가 | 저수준 제어 필요 시 |

**📢 섹션 요약 비유**
> Spark SQL은 "자동 항법장치가 달린 선박"이다. 목적지(쿼리 의도)만 입력하면 Catalyst(항법장치)가 최적 항로(실행 계획)를 계산하고, Tungsten(엔진)이 최고 속도로 주행한다.

---

## Ⅲ. 비교 및 연결

### 1. Spark SQL vs Apache Hive

| 비교 항목 | Apache Hive | Spark SQL |
|:---|:---|:---|
| 실행 엔진 | MapReduce / Tez | Spark RDD (인메모리) |
| 지연 시간 | 수 분~수십 분 | 수 초~수 분 |
| 처리 방식 | 배치 전용 | 배치 + 인터랙티브 + 스트리밍 |
| SQL 표준 | HQL (확장 SQL) | ANSI SQL (3.x+에서 강화) |
| 메타스토어 | Hive Metastore | Hive Metastore 공유 가능 |
| ML 연동 | 불가 | MLlib, Python UDF 연동 용이 |

### 2. 연결 개념

- <strong>Catalyst Optimizer</strong>: Spark SQL의 최적화 핵심 엔진 (별도 파일 참조)
- <strong>Tungsten 엔진</strong>: 물리적 실행 최적화, Off-heap 메모리, Codegen
- **AQE (Adaptive Query Execution)**: 런타임 통계 기반 실행 계획 동적 재최적화
- <strong>Delta Lake</strong>: Spark SQL 위에서 ACID 트랜잭션과 TIME TRAVEL 제공

**📢 섹션 요약 비유**
> Spark SQL은 Hive와 비교하면 "디젤 기관차에서 고속 전철로 업그레이드"이다. 선로(메타스토어)는 그대로 사용하면서 엔진과 동력계통만 바꿔 속도를 10배 높였다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Spark SQL 성능 튜닝 체크리스트

- [ ] <strong>파티션 프루닝</strong>: 파티션 컬럼으로 필터링하여 스캔 데이터 최소화
- [ ] **컬럼형 포맷 사용**: Parquet/ORC 포맷으로 컬럼 프루닝 효과 극대화
- [ ] <strong>BroadcastJoin 힌트</strong>: 소규모 테이블(< 10MB, 기본값) 조인 시 명시적 힌트 사용
- [ ] **AQE 활성화**: `spark.sql.adaptive.enabled=true` (Spark 3.0+ 기본 활성화)
- [ ] <strong>셔플 파티션 조정</strong>: `spark.sql.shuffle.partitions` 기본 200 -> 데이터 규모에 맞게 조정
- [ ] <strong>캐싱 전략</strong>: 반복 참조 DataFrame은 `df.cache()` 또는 `CACHE TABLE`

### 2. Spark SQL 3.x ANSI SQL 강화

Spark 3.0+부터 `spark.sql.ansi.enabled=true` 설정 시 표준 SQL 동작을 따른다.
- 정수 오버플로 오류 발생 (기존: 묵시적 래핑)
- 잘못된 캐스팅 예외 발생 (기존: null 반환)
- 서브쿼리, 윈도우 함수 표준 강화

**📢 섹션 요약 비유**
> Spark SQL 튜닝은 "고속도로 진입 전략"과 같다. 파티션 프루닝은 출발지에서 꼭 필요한 짐만 싣는 것(스캔 최소화), BroadcastJoin은 작은 짐을 트럭마다 미리 실어두는 것(셔플 제거), AQE는 실시간 교통정보로 경로를 재탐색하는 것이다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 생산성 향상 | SQL 한 줄로 PB 규모 데이터 쿼리 |
| 성능 개선 | MapReduce 대비 최대 100배 빠른 분산 SQL |
| 통합 인터페이스 | SQL, Python, Scala, Java, R 모두 동일 엔진 |
| 기존 자산 활용 | Hive 테이블, 메타스토어 그대로 재사용 |
| 레이크하우스 기반 | Delta Lake/Iceberg와 결합해 ACID SQL 처리 |

### 2. 한계 및 미래 전망

- 복잡한 비구조적 변환은 여전히 RDD/Python UDF가 유연하나 성능 저하 주의
- Pandas UDF(벡터화 UDF)로 Python 생태계와 고성능 연동 가능
- Spark Connect (3.4+): 클라이언트-서버 분리 아키텍처로 원격 SQL 실행 지원

**📢 섹션 요약 비유**
> Spark SQL은 빅데이터 세계의 "만능 칼"이다. SQL이라는 친숙한 언어로 Hadoop의 방대한 창고를 제트기 속도로 뒤질 수 있게 해주며, 앞으로는 클라우드 어디서나 원격으로 이 칼을 사용할 수 있는 시대(Spark Connect)로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Catalyst Optimizer | 내부 구성 | SQL/DataFrame -> 최적 실행 계획 변환 |
| Tungsten 엔진 | 내부 구성 | 물리 실행 최적화, 메모리/CPU 효율화 |
| AQE | 확장 기능 | 런타임 재최적화, Skew Join 자동 처리 |
| Hive Metastore | 통합 대상 | 테이블 메타데이터 공유 |
| Delta Lake | 응용 | Spark SQL 위의 ACID 트랜잭션 계층 |
| DataFrame API | 동등 인터페이스 | SQL과 동일 실행 계획 생성 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Catalyst Optimizer]
    |
    v
[Tungsten Engine]
    |
    v
[AQE (Adaptive Query Execution)]
    |
    v
[Hive Metastore]
    |
    v
[Delta Lake]
```

이 흐름도는 Catalyst Optimizer에서 출발해 Delta Lake까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

Spark SQL은 도서관(데이터)에서 원하는 책을 찾아주는 <strong>스마트 사서</strong>예요. 사서한테 "2020년 이후 출판된 과학책 제목 알려줘" 라고 말(SQL)만 하면, 사서가 가장 빠른 방법으로 책장을 뒤져서 목록을 만들어줘요. 직접 책장을 하나하나 뒤질(RDD) 필요가 없답니다!
