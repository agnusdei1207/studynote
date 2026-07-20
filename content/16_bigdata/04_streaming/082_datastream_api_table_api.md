---
title: "Datastream Api Table Api"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 82
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Apache Flink는 두 가지 프로그래밍 계층을 제공한다. DataStream API (데이터스트림 API)는 이벤트 단위의 세밀한 스트림 처리를 위한 저수준 API이고, Table API & SQL (테이블 API)은 관계형 테이블 개념을 스트림에 적용한 고수준 선언적 API로, 두 계층은 내부적으로 동일한 DataStream 실행 엔진으로 컴파일된다.
- **가치**: SQL을 아는 데이터 엔지니어는 Table API/SQL로 스트리밍 집계·조인·윈도우를 신속하게 개발하고, 복잡한 상태 관리나 커스텀 타임스탬프 추출이 필요한 경우 DataStream API로 세밀하게 제어하는 <strong>계층화된 유연성</strong>이 Flink의 큰 장점이다.
- **판단 포인트**: Table API/SQL은 선언적이라 Flink가 최적화(술어 푸시다운, 공통 부분식 제거 등)를 자동으로 수행하지만, DataStream API는 개발자가 직접 최적화해야 하므로 운영 경험과 스트리밍 지식이 더 많이 요구된다.

---

## Ⅰ. 개요 및 필요성

### 1. Flink API 계층 구조

```
사용자 편의성 ^          ^ 표현력
+----------------------------------------+
|  SQL (문자열 SQL 쿼리)                  |  <- 가장 선언적
+----------------------------------------+
|  Table API (Java/Scala/Python DSL)     |
+----------------------------------------+
|  DataStream / DataSet API              |  <- 세밀한 제어
+----------------------------------------+
|  Stateful Functions (저수준)           |  <- 가장 강력한 제어
+----------------------------------------+
```

### 2. 각 API의 사용 상황

- **SQL**: "Kafka 토픽에서 5분 집계를 구하라" — BI 엔지니어, 빠른 프로토타이핑
- <strong>Table API</strong>: SQL이지만 프로그래밍 방식으로 동적 쿼리 생성 필요 시
- <strong>DataStream API</strong>: 커스텀 타임스탬프 추출, 복잡한 상태 로직, ML 모델 인라인 실행

**📢 섹션 요약 비유**
> Flink의 두 계층은 "자동 변속기(Table/SQL)와 수동 변속기(DataStream API)"와 같다. 일반 운전에는 자동이 편리하지만, 험한 오프로드(복잡한 비즈니스 로직)는 수동이 더 정밀하게 제어된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. DataStream API 핵심 구조

```java
// Java DataStream API 예시
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// 1. Source: Kafka에서 데이터 읽기
DataStream<String> stream = env.fromSource(
    KafkaSource.<String>builder()
        .setBootstrapServers("kafka:9092")
        .setTopics("events")
        .build(),
    WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(5)),
    "KafkaSource"
);

// 2. Transformation
DataStream<Tuple2<String, Integer>> result = stream
    .map(json -> parseEvent(json))          // map: 1:1 변환
    .filter(e -> e.getAmount() > 100)        // filter: 필터링
    .keyBy(e -> e.getUserId())               // keyBy: 키 분할
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))  // 윈도우
    .sum(1);                                 // 집계

// 3. Sink: 결과 저장
result.addSink(new ElasticsearchSink<>(...));

env.execute("UserActivityAggregation");
```

### 2. Table API & SQL 핵심 구조

```java
// Java Table API + SQL 예시
StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

// DataStream -> Table 변환
Table eventTable = tableEnv.fromDataStream(
    stream,
    Schema.newBuilder()
        .columnByExpression("rowtime", "CAST(ts AS TIMESTAMP_LTZ(3))")
        .watermark("rowtime", "rowtime - INTERVAL '5' SECOND")
        .build()
);

// SQL로 5분 텀블링 윈도우 집계
Table result = tableEnv.sqlQuery(
    "SELECT user_id, TUMBLE_END(rowtime, INTERVAL '5' MINUTE) as window_end, " +
    "       SUM(amount) as total_amount " +
    "FROM events " +
    "GROUP BY user_id, TUMBLE(rowtime, INTERVAL '5' MINUTE)"
);

// Table -> DataStream 변환 (다시 저수준으로)
DataStream<Row> outputStream = tableEnv.toDataStream(result);
```

### 3. 연산자 비교

| 연산 | DataStream API | Table API / SQL |
|:---|:---|:---|
| 필터 | `.filter(pred)` | `WHERE condition` |
| 변환 | `.map(func)` | `SELECT expr` |
| 집계 | `.reduce()` / `.aggregate()` | `GROUP BY ... SUM()` |
| 조인 | `.connect().flatMap()` | `JOIN ... ON` |
| 윈도우 | `.window(TumblingEventTime...)` | `TUMBLE()`, `HOP()`, `SESSION()` |
| 상태 | `ValueState`, `MapState` 직접 사용 | 내부 자동 처리 |

**📢 섹션 요약 비유**
> DataStream API는 "재료를 직접 손질하고 요리하는 셰프"이고, Table API/SQL은 "레시피 카드(SQL)대로 로봇이 자동으로 조리하는 방식"이다. 셰프는 더 창의적이지만 기술이 필요하고, 로봇은 빠르고 표준화되어 있다.

---

## Ⅲ. 비교 및 연결

### 1. Table API SQL의 Flink 고유 SQL 확장

표준 SQL에 없는 스트리밍 전용 구문들:

```sql
-- 텀블링 윈도우 집계
SELECT TUMBLE_START(event_time, INTERVAL '10' MINUTE) AS window_start,
       user_id, COUNT(*) AS cnt
FROM events
GROUP BY TUMBLE(event_time, INTERVAL '10' MINUTE), user_id;

-- 슬라이딩 윈도우 (HOP)
SELECT HOP_START(event_time, INTERVAL '5' MINUTE, INTERVAL '1' HOUR) AS win_start,
       AVG(score) AS avg_score
FROM events
GROUP BY HOP(event_time, INTERVAL '5' MINUTE, INTERVAL '1' HOUR);

-- 스트림-스트림 인터벌 조인
SELECT a.user_id, b.product_id
FROM clicks a JOIN purchases b
ON a.user_id = b.user_id
AND b.event_time BETWEEN a.event_time AND a.event_time + INTERVAL '30' MINUTE;
```

### 2. API 간 상호 변환

```java
// Table -> DataStream (복잡한 로직 처리 후 Table로 복귀)
DataStream<Row> ds = tableEnv.toDataStream(table);
DataStream<Row> processed = ds.process(new ComplexProcessFunction());
Table backToTable = tableEnv.fromDataStream(processed);
```

**📢 섹션 요약 비유**
> Flink의 두 API 전환은 "번역가(Table API/SQL)와 원어민 대화(DataStream API)를 필요에 따라 섞어 쓰는 것"이다. 표준 대화는 번역기로 충분하지만, 세밀한 감정 표현은 원어민과 직접 소통해야 한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. API 선택 가이드

| 요구사항 | 권장 API |
|:---|:---|
| Kafka 이벤트 SQL 집계/필터 | Table API / SQL |
| 5분 윈도우 집계 대시보드 | SQL (TUMBLE 윈도우) |
| 커스텀 타임스탬프 파싱 | DataStream API |
| ML 모델 인라인 호출 | DataStream API |
| CDC(Change Data Capture) 처리 | Table API (Upsert 커넥터) |
| 복잡한 패턴 매칭 (CEP) | DataStream API + Flink CEP 라이브러리 |

### 2. 주요 커넥터 (Source/Sink)

| 커넥터 | 방향 | 비고 |
|:---|:---|:---|
| Apache Kafka Connector | Source + Sink | Exactly-Once 지원 |
| JDBC Connector | Source + Sink | MySQL, PostgreSQL |
| Elasticsearch Connector | Sink | 검색 인덱스 업데이트 |
| Hadoop FileSystem | Source + Sink | HDFS, S3 |
| Apache HBase Connector | Source + Sink | 랜덤 읽기/쓰기 |

**📢 섹션 요약 비유**
> DataStream API는 "맞춤 양복", Table API/SQL은 "기성복"이다. 기성복(SQL)이 대부분 상황에 잘 맞고 빠르지만, 특별한 체형(복잡한 비즈니스 로직)에는 맞춤 양복(DataStream)이 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 개발 생산성 | SQL 알면 스트리밍 앱 빠르게 개발 가능 |
| 최적화 자동화 | Table API/SQL은 Flink 옵티마이저가 자동 최적화 |
| 유연성 | 두 API 혼용으로 선언적+절차적 처리 결합 |
| 생태계 통합 | JDBC, Kafka, ES 등 다양한 커넥터 |

### 2. 결론

Flink의 DataStream API와 Table API/SQL은 <strong>상호 보완적인 두 층의 프로그래밍 모델</strong>이다. 학습 정리에서는 두 API의 추상화 수준 차이, 내부적으로 동일한 실행 엔진으로 컴파일된다는 통합성, 그리고 스트리밍 SQL의 고유 구문(TUMBLE, HOP, SESSION 윈도우)을 서술하는 것이 핵심이다.

**📢 섹션 요약 비유**
> Flink의 두 API는 "같은 공장의 두 입구"다. 자동화 생산 라인(Table API/SQL)으로 들어가면 로봇이 알아서 처리하고, 수작업 라인(DataStream API)으로 들어가면 세밀하게 직접 제어한다. 두 라인의 결과물은 같은 공장 창고에 모인다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Flink 아키텍처 | 실행 환경 | DataStream/Table API의 실행 기반 |
| 윈도우 연산 | 핵심 활용 | TUMBLE/HOP/SESSION 윈도우 |
| Watermark | 연동 개념 | Table API의 WATERMARK 정의와 연동 |
| Kafka 커넥터 | Source/Sink | 가장 많이 사용되는 스트리밍 소스 |
| CEP (Complex Event Processing) | 확장 기능 | DataStream API 위의 패턴 감지 라이브러리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Flink RDD]
    |
    v
[DataStream API]
    |
    v
[Table API/SQL]
    |
    v
[통합 스트리밍]
    |
    v
[Kappa 아키텍처]
```

Flink의 스트리밍 API가 저수준 RDD에서 고수준 SQL까지 통합되며 카파 아키텍처로 수렴하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

Flink에는 두 가지 요리 방법이 있어요. Table API/SQL은 "레시피대로 요리하는 방법"(편리하고 빠름)이고, DataStream API는 "셰프가 직접 창의적으로 요리하는 방법"(어렵지만 자유로움)이에요. 같은 Flink 주방(실행 엔진)에서 요리하지만, 어떤 방법으로 요청하느냐가 다를 뿐이고 최종 음식(결과 데이터)은 같은 품질이랍니다!
