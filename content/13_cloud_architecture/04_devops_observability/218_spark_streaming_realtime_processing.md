---
title: "Spark Streaming Realtime Processing"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 218
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Spark Structured Streaming은 실시간 스트림 데이터를 "무한히 쌓이는 테이블(Unbounded Table)"로 추상화하여 배치와 동일한 DataFrame API로 처리하는 실시간 처리 엔진이며, 마이크로 배치와 연속 처리 두 모드를 지원한다.
> 2. **가치**: Kafka 소스와의 완전한 통합, 이벤트 시간(Event-time) 기반 윈도우 연산, 워터마크(Watermark)를 통한 지연 데이터 처리로 정확히 한 번(Exactly-once) 처리 의미론을 보장한다.
> 3. **판단 포인트**: 마이크로 배치는 지연 시간 수백ms~수 초(Latency)지만 처리량(Throughput)이 높고, 연속 처리는 지연 시간 ~1ms이지만 처리량이 낮다. 대부분의 실무는 수 초 지연이 허용되므로 마이크로 배치가 표준이다.

---

## Ⅰ. 개요 및 필요성

기업의 데이터 처리 요구가 "어젯밤 로그 분석(배치)" 수준을 넘어 "지금 이 순간 이상 감지·추천·알림"으로 진화하면서 실시간 스트림 처리가 필수가 됐다. 넷플릭스가 사용자가 영상을 보는 동안 실시간으로 스트리밍 품질을 조정하고, 우버가 실시간으로 근방 드라이버를 매칭하는 것이 대표적 사례다.

초기 Spark Streaming(Spark 1.x)은 DStream(Discretized Stream) API를 사용했다. 스트림 데이터를 고정 시간 간격(예: 1초)으로 RDD로 쪼개어 배치처럼 처리하는 방식이었다. 동작은 했지만 이벤트 시간 처리, 상태 관리, exactly-once 보장이 복잡했다.

Spark 2.0에서 등장한 <strong>Structured Streaming</strong>은 완전히 재설계됐다. 핵심 아이디어: <strong>스트림을 끝없이 행이 추가되는 테이블</strong>로 본다. 개발자는 이 테이블에 배치와 동일한 DataFrame/SQL 쿼리를 작성하고, Spark이 내부적으로 마이크로 배치로 쿼리를 반복 실행하여 결과를 점진적으로 업데이트한다.

📢 **섹션 요약 비유**: Structured Streaming은 뉴스 자막 기계와 같다. 자막 기계는 기자가 전송하는 뉴스(스트림)를 화면 아래에 계속 추가하는 테이블처럼 처리하여, 매초 새로운 자막을 자동으로 표시한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Structured Streaming 실행 모델

```
  +------------------------------------------------------------+
  |               Structured Streaming 처리 모델                |
  +------------------------------------------------------------+
  |                                                             |
  |  소스 (Kafka/File/Socket)                                   |
  |       | 새 데이터 계속 유입                                  |
  |       v                                                     |
  |  Input Table (무한히 쌓이는 테이블 추상화)                   |
  |  +------------------------------------------------------+  |
  |  | T=0 | event_1, event_2                               |  |
  |  | T=1 | event_3, event_4, event_5                      |  |
  |  | T=2 | event_6                                        |  |
  |  | ... | (계속 쌓임)                                     |  |
  |  +------------------------------------------------------+  |
  |       | 동일한 DataFrame 쿼리 적용                           |
  |       v                                                     |
  |  Result Table (쿼리 결과 테이블)                             |
  |       |                                                     |
  |       v 마이크로 배치마다 업데이트                            |
  |  Output (Console/File/Kafka/DB 등)                          |
  +------------------------------------------------------------+
```

### Kafka 소스 연동 코드

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StringType, LongType

spark = SparkSession.builder \
    .appName("RealtimeOrderAnalysis") \
    .getOrCreate()

# Kafka 소스 읽기 (실시간 스트림)
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

# JSON 파싱
schema = StructType() \
    .add("order_id", LongType()) \
    .add("user_id", LongType()) \
    .add("amount", LongType()) \
    .add("timestamp", LongType())

orders = kafka_df \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# 이벤트 시간 기반 윈도우 집계 (5분 윈도우, 1분 슬라이딩)
windowed_counts = orders \
    .withWatermark("timestamp", "10 minutes") \  # 지연 데이터 10분까지 허용
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("user_id")
    ) \
    .agg(count("order_id").alias("order_count"),
         sum("amount").alias("total_amount"))

# 싱크: 콘솔 출력 (처음 N개만, 개발용)
query = windowed_counts.writeStream \
    .outputMode("update") \      # 변경된 행만 출력
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="10 seconds") \  # 10초마다 마이크로 배치
    .start()

query.awaitTermination()
```

### 윈도우 연산 유형

| 윈도우 유형 | 설명 | 예시 |
|:---|:---|:---|
| **Tumbling Window** | 겹치지 않는 고정 크기 윈도우 | 1분마다 초기화 |
| **Sliding Window** | 슬라이딩 간격으로 이동하는 윈도우 | 5분 윈도우, 1분마다 이동 |
| <strong>Session Window</strong> | 비활성 기간으로 세션 구분 | 30초 이상 이벤트 없으면 세션 종료 |

📢 **섹션 요약 비유**: 윈도우 연산은 버스 창문으로 바깥을 보는 것과 같다. Tumbling은 매 정류장마다 새 창문, Sliding은 창문이 조금씩 이동하면서 앞 풍경과 현재 풍경이 겹치는 것이다.

---

## Ⅲ. 비교 및 연결

### 처리 모드 비교

| 모드 | 최소 지연 | 처리량 | 정확도 | 사용 시나리오 |
|:---|:---:|:---:|:---:|:---|
| 마이크로 배치 (기본) | ~100ms | 높음 | Exactly-once | 대부분의 실시간 처리 |
| 연속 처리 (Spark 2.3+) | ~1ms | 낮음 | At-least-once | 초저지연 필요 시 |
| 배치 처리 (비교용) | 분~시간 | 최고 | Exactly-once | 대규모 비실시간 |

### 출력 모드 (OutputMode)

| 모드 | 설명 | 적합 쿼리 |
|:---|:---|:---|
| **Append** | 새로 추가된 행만 출력 | 집계 없는 변환, 워터마크 적용 시 |
| **Complete** | 결과 테이블 전체를 매번 출력 | 소규모 집계 결과 |
| **Update** | 변경된 행만 출력 | 집계 + 실시간 대시보드 |

### Spark Streaming vs Apache Flink

| 항목 | Spark Structured Streaming | Apache Flink |
|:---|:---|:---|
| 처리 방식 | 마이크로 배치 (기본) | 진정한 스트림 처리 |
| 지연 시간 | 수백ms~수 초 | ~수ms |
| 처리량 | 높음 | 중간 |
| 배치 통합 | ✅ (배치와 동일 API) | 별도 DataSet API |
| 상태 관리 | 좋음 | 매우 강함 |
| 적합 시나리오 | 처리량 우선 | 초저지연 필요 |

📢 **섹션 요약 비유**: Spark Streaming과 Flink의 차이는 편의점 계산대(Spark, 10초마다 일괄 처리)와 고속 체크아웃(Flink, 아이템마다 즉시 처리)의 차이다. 빠른 처리량은 편의점이, 즉각 반응은 고속 체크아웃이 강하다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>워터마크(Watermark) 설정</strong>:
```python
# 이벤트 시간 vs 처리 시간
# 이벤트: 15:00:00에 발생 -> 네트워크 지연으로 15:00:30에 도착
# 워터마크 10분 설정: 15:10:00 이후에는 15:00:00 이벤트를 늦은 데이터로 처리

windowed = df \
    .withWatermark("event_time", "10 minutes") \  # 10분 지연 허용
    .groupBy(
        window("event_time", "5 minutes"),
        "user_id"
    ) \
    .count()

# 워터마크 없으면: 지연 데이터 기다리느라 메모리 무한 증가
# 워터마크 있으면: 허용 시간 초과한 지연 데이터는 버리고 상태 메모리 정리
```

<strong>Kafka -> Spark -> S3 파이프라인</strong>:
```python
# Delta Lake로 실시간 데이터 저장 (ACID 트랜잭션 지원)
orders.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://checkpoints/orders/") \
    .option("path", "s3://data/orders/") \
    .trigger(processingTime="30 seconds") \
    .start()
```

**실무자 판단 포인트**:
- Checkpoint Location은 장애 복구의 핵심이다. Spark가 재시작될 때 checkpoint에서 마지막 처리 오프셋을 읽어 중복 처리 없이 이어서 실행한다.
- 상태 있는 집계(Stateful Aggregation)는 상태가 메모리에 축적되므로, 워터마크로 오래된 상태를 주기적으로 정리해야 메모리 문제를 방지한다.
- Structured Streaming과 Delta Lake의 조합이 현대 실시간 데이터 레이크하우스 아키텍처의 표준이 되고 있다.

📢 **섹션 요약 비유**: Checkpoint는 게임 세이브처럼, 서버가 재시작되어도 마지막으로 처리한 위치에서 이어서 처리한다. Checkpoint 없으면 재시작 시 처음부터 또는 중복 처리가 발생한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 배치·스트리밍 통합 | 동일한 DataFrame API로 배치와 스트리밍 처리 |
| Exactly-once 보장 | 체크포인팅과 멱등 싱크로 정확히 한 번 처리 |
| 이벤트 시간 처리 | 네트워크 지연 데이터를 워터마크로 처리 |
| Kafka 완전 통합 | 오프셋 관리·체크포인팅 자동화 |

Spark Structured Streaming은 "빅데이터 배치 처리의 강점을 실시간 처리로 확장"한 결과물이다. 카프카와의 통합, Delta Lake와의 조합으로 현대 Lambda 아키텍처와 Kappa 아키텍처를 모두 Spark 단일 플랫폼으로 구현할 수 있게 됐다. 시스템 설계 학습에서 스트리밍 처리 아키텍처와 Kafka·Spark의 연계는 빈출 주제다.

📢 **섹션 요약 비유**: Structured Streaming은 강의 물흐름(스트림)을 배와 양동이(배치) 없이 수력 발전기로 직접 처리하는 것과 같다. 물이 흐르는 그 자리에서 즉시 에너지(인사이트)를 추출하여 지연 없이 활용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Apache Kafka | Structured Streaming의 가장 일반적인 소스 |
| 워터마크 (Watermark) | 지연 데이터 처리와 상태 메모리 관리의 핵심 |
| 마이크로 배치 | Structured Streaming의 기본 실행 모드 |
| Delta Lake | Structured Streaming 결과 저장의 현대 표준 |
| Apache Flink | 초저지연 스트리밍에서 Spark의 대안 도구 |
| Exactly-once | 체크포인팅으로 보장하는 스트리밍 처리 의미론 |

### 👶 어린이를 위한 3줄 비유 설명

1. Structured Streaming은 쇼핑몰 CCTV처럼, 카메라(Kafka)에서 계속 들어오는 영상(이벤트)을 실시간으로 분석해서 도둑이 있는지(이상 감지) 알려줘.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 처리 (지연 ^, 실시간성 v)
    |
    v
Spark Streaming: 마이크로배치 (준실시간)
    |
    v
Structured Streaming: DataFrame API + Event-Time + Watermark
    |
    v
Flink: True Streaming (이벤트별 처리) · 정확히 한 번 보장
```
2. 마이크로 배치는 10초마다 영상을 묶어서 분석하는 것, 연속 처리는 프레임마다 즉시 분석하는 거야.
3. 워터마크는 "이미 10분 지난 영상은 그냥 넘어가자"라는 규칙이야. 너무 늦게 온 데이터는 기다리지 않고 무시해서 메모리가 꽉 차지 않게 해.
