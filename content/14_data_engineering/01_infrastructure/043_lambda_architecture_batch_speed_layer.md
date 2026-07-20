---
title: "Lambda Architecture Batch Speed Layer"
date: "2026-04-05"
tags:
  - "studynote-data-engineering"
weight: 43
---
> **핵심 인사이트**
> 1. 람다 아키텍처(Lambda Architecture)는 Nathan Marz가 제안한 데이터 처리 아키텍처로 — 배치 레이어(정확성), 스피드 레이어(실시간성), 서빙 레이어(통합 조회)의 3계층으로 "정확하고 빠른" 데이터 처리를 달성하지만, 동일 로직을 두 번 구현해야 하는 "코드 중복" 문제가 근본 한계이다.
> 2. 람다의 이진적 접근(배치 OR 스피드)과 달리, 카파 아키텍처(Kappa Architecture)는 스트리밍 레이어만으로 모든 처리를 통합하여 코드 중복을 해소하지만 — 대규모 재처리(Reprocessing) 시 배치보다 자원이 많이 소요되는 트레이드오프가 있다.
> 3. 현대 데이터 플랫폼(Databricks, Apache Flink)은 배치와 스트리밍을 동일 API로 처리하는 "통합 컴퓨팅(Unified Compute)" 패러다임으로 람다의 한계를 극복하며 — Kappa에 가까운 형태로 수렴하고 있다.

---

## Ⅰ. 람다 아키텍처 3계층

```
람다 아키텍처 (Lambda Architecture):
  Nathan Marz (Twitter) 제안, 2012

  데이터 소스
      |
      +-- 배치 레이어 (Batch Layer) ----------+
      |   - 전체 히스토리 데이터 처리         |
      |   - 높은 정확성, 느린 처리(시간~일)   |
      |   - Hadoop MapReduce, Spark Batch     |
      |   - Batch View (하루치 집계 등)       |
      |                                      |
      +-- 스피드 레이어 (Speed Layer) ---------+
      |   - 최근 데이터만 처리 (배치 지연 보완)|
      |   - 낮은 지연(수초 이내), 근사치 허용 |
      |   - Storm, Flink, Spark Streaming    |
      |   - Realtime View (최신 수분 데이터)  |
      |                                      |
      +--------------------------------------+
                                             v
                               서빙 레이어 (Serving Layer)
                               - Batch View + Realtime View 병합
                               - 쿼리 응답 (HBase, Cassandra)
                               - 쿼리: Batch + Speed 조합 결과

핵심 원칙:
  1. 불변성 (Immutability): 원본 데이터 수정 없음
  2. 재계산 (Recomputation): 배치 레이어는 전체 재계산 가능
  3. 정확성 (Accuracy): 배치 레이어가 최종 정확한 답 제공
```

> 📢 **섹션 요약 비유**: 람다 아키텍처는 어제 신문(배치) + 속보 알림(스피드) 조합 — 어제까지의 정확한 기사(배치 뷰)와 방금 업데이트된 속보(리얼타임 뷰)를 함께 보여줘요.

---

## Ⅱ. 배치 레이어 상세

```
배치 레이어 (Batch Layer):

특징:
  전체 데이터셋(역사적 데이터 포함)을 처리
  정확성 최우선
  지연 허용 (시간 ~ 일 단위)

데이터 스토어:
  HDFS, Amazon S3, Azure ADLS
  포맷: Parquet, ORC (컬럼 지향, 압축 효율)

처리 엔진:
  Apache Hadoop MapReduce (초기)
  Apache Spark (현재 표준)
    - 인메모리 처리 -> 10~100배 빠름
    - Spark SQL, DataFrame API

배치 뷰 (Batch View):
  집계/변환 결과를 미리 계산해서 저장
  예: 일별 판매 합계, 월별 사용자 활동 통계

배치 처리 주기:
  일간 배치: 매일 새벽 2시 (D-1 데이터)
  주간 배치: 월요일 새벽 (주간 통계)
  임시 전체 재처리: 스키마 변경 시

배치 레이어 한계:
  지연: 방금 발생한 이벤트는 내일 집계에 포함
  -> 사용자가 "오늘 내 구매 합계"를 보려면?
  -> 스피드 레이어 필요

Apache Spark 배치 예시:
  spark.read.parquet("s3://data/events/2026-04-05/")
    .groupBy("user_id", "date")
    .agg(sum("amount").alias("daily_total"))
    .write.parquet("s3://batch-views/daily_user_total/")
```

> 📢 **섹션 요약 비유**: 배치 레이어는 월말 정산 — 한 달 거래 전부를 정확히 계산하지만 결과가 다음날 나와요. 정확하지만 느려요.

---

## Ⅲ. 스피드 레이어 상세

```
스피드 레이어 (Speed Layer):

특징:
  최근 데이터만 처리 (배치 지연 구간 보완)
  낮은 지연 최우선 (수초~수분)
  근사치 허용 (정확성 < 속도)
  처리 완료 시 데이터 삭제 (배치가 최종 권위)

처리 엔진:
  Apache Storm: 지연 최소화 (수ms)
  Apache Spark Streaming: 마이크로 배치 (수초)
  Apache Flink: 진정한 스트리밍 + 이벤트 타임
  Kafka Streams: 경량, 라이브러리 형태

리얼타임 뷰 (Realtime View):
  배치 뷰의 최신화 역할
  예: "오늘 현재까지" 집계 (배치 뷰 없는 부분)

스피드 레이어 한계:
  지연 보상 로직: 배치와 동일 비즈니스 로직 재구현 필요
  -> 코드 중복 = 람다의 핵심 문제

쿼리 시 조합:
  총 판매액 쿼리:
    결과 = Batch View (어제까지) + Realtime View (오늘 현재)

  코드:
    batch_result = query_hbase("batch_view", user_id, date_range)
    speed_result = query_cassandra("speed_view", user_id, today)
    total = batch_result + speed_result

Flink 스트리밍 예시:
  DataStream<Event> stream = env.addSource(kafkaConsumer);
  stream
    .keyBy(event -> event.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .sum("amount")
    .addSink(cassandraSink);
```

> 📢 **섹션 요약 비유**: 스피드 레이어는 편의점 장부 — 하루 매출이 마감되기 전, 오늘 오전까지 판 것을 메모장에 빠르게 기록. 정확하지 않아도 되니까 빠르게만.

---

## Ⅳ. 람다 vs 카파 아키텍처

```
람다의 문제:
  동일 비즈니스 로직을 두 번 구현
    배치: Spark SQL로 집계 로직
    스피드: Flink로 동일 집계 로직
  -> 코드 불일치 위험
  -> 유지보수 비용 2배

카파 아키텍처 (Kappa Architecture):
  Jay Kreps (LinkedIn) 제안, 2014

  핵심: 스트리밍 레이어 하나로 통합

  데이터 소스 -> Kafka (로그 저장) -> 스트리밍 처리 -> 서빙

  배치 재처리가 필요하면:
    Kafka에 전체 로그 보관 (Kafka Log Compaction)
    스트리밍 처리를 처음부터 재실행 (재처리 = 스트리밍)

람다 vs 카파 비교:

항목            | 람다                  | 카파
----------------+-----------------------+---------------------------
코드 복잡도     | 높음 (로직 2회 구현)  | 낮음 (스트리밍만)
재처리          | 배치 재실행 (빠름)    | 스트리밍 재처리 (느리고 비용)
정확성          | 높음 (배치 최종 권위) | 높음 (이벤트 타임 Flink)
인프라 복잡도   | 높음 (2레이어)        | 낮음 (1레이어)
대규모 재처리   | 유리                  | 불리 (자원 많이 소요)

현대 트렌드:
  Databricks Delta Live Tables:
    배치 + 스트리밍을 동일 코드로 처리
    람다의 이점 + 카파의 단순성

  Apache Flink + Apache Iceberg:
    스트리밍 처리 + 배치 쿼리 통합
    = Kappa + 대규모 재처리 개선
```

> 📢 **섹션 요약 비유**: 람다 vs 카파는 두 가지 장부 vs 하나의 디지털 장부 — 람다는 종이 장부(배치) + 메모장(스피드) 두 개, 카파는 클라우드 실시간 장부 하나. 현대는 카파 방향.

---

## Ⅴ. 실무 시나리오 — 이커머스 실시간 대시보드

```
이커머스 판매 대시보드 람다 아키텍처:

요구사항:
  "현재 판매 현황" 대시보드 (수초 지연 허용)
  "월간 매출 통계" 보고서 (일 1회 배치)

람다 아키텍처 구현:

  데이터 소스:
    주문 서비스 -> Kafka 토픽 (orders)

  배치 레이어:
    Spark on EMR, 매일 새벽 3시 실행
    S3 Parquet (원본) -> 일별/월별 집계 -> HBase (batch view)

  스피드 레이어:
    Kafka -> Flink -> Cassandra (speed view)
    Tumbling Window: 1분 단위 집계

  서빙 레이어:
    대시보드 API:
      GET /dashboard/sales?date=today

      Response:
        historical (배치 뷰, HBase): 어제까지 합계
        realtime (스피드 뷰, Cassandra): 오늘 지금까지
        total = historical + realtime

성능:
  배치 정확성: D-1 기준 정확
  스피드 지연: ~30초
  쿼리 응답: 100ms 이내

카파로 전환 검토:
  문제: 동일 집계 로직 Spark + Flink 중복
  해결: Flink로 통합 + Kafka 24시간 로그 보관

  전환 후:
    코드 50% 감소
    인프라 40% 단순화
    재처리: Kafka lag으로 처음부터 재실행 (수시간 소요)
```

> 📢 **섹션 요약 비유**: 이커머스 람다 아키텍처는 은행 잔액 조회 — 어제까지 정산된 잔액(배치) + 오늘 ATM 출금 합산(스피드)을 더해서 현재 잔액 표시.

---

## 📌 관련 개념 맵

```
람다 아키텍처
+-- 3계층
|   +-- 배치 레이어 (Spark, Hadoop)
|   +-- 스피드 레이어 (Flink, Storm)
|   +-- 서빙 레이어 (HBase, Cassandra)
+-- 장단점
|   +-- 장점: 정확성 + 실시간성 동시
|   +-- 단점: 코드 중복
+-- 대안
|   +-- 카파 아키텍처 (스트리밍 통합)
|   +-- Delta Live Tables (Databricks)
+-- 관련 기술
|   +-- Apache Kafka, Flink, Spark
|   +-- Apache Iceberg
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[분산 배치 처리 (2004)]
Google MapReduce, Hadoop
      |
      v
[람다 아키텍처 제안 (2012)]
Nathan Marz: 배치 + 스피드 통합
"Big Data" 책 출판
      |
      v
[카파 아키텍처 제안 (2014)]
Jay Kreps (LinkedIn): 스트리밍으로 통합
Kafka 기반 단일 파이프라인
      |
      v
[실시간 처리 고도화 (2015~)]
Apache Flink: 이벤트 타임, 정확한 스트리밍
Spark Structured Streaming
      |
      v
[현재: 통합 데이터 플랫폼]
Delta Live Tables (Databricks)
배치+스트리밍 동일 코드
Apache Iceberg + Flink
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 람다 아키텍처는 어제 신문 + 속보 조합 — 정확한 어제 기사(배치)와 방금 올라온 속보(스피드)를 합쳐서 보여줘요!
2. 배치는 느리지만 정확, 스피드는 빠르지만 근사치 — 두 개를 합치면 빠르고 정확한 결과를 얻을 수 있어요.
3. 현대는 카파 아키텍처로 진화 — "두 개의 시스템을 만드는 게 너무 복잡하니, 스트리밍 하나만 잘 만들자"는 방향이에요!
