---
title: "Real-time Streaming Analytics Kafka Flink"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 674
---
# 674. 실시간 스트리밍 분석 - Kafka & Flink (Real-time Streaming Analytics)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Kafka는 분산 커밋 로그(append-only log) 기반의 이벤트 버퍼/재생(replay) 플랫폼이고, Apache Flink는 Chandy-Lamport 분산 스냅샷과 Watermark 메커니즘을 통해 *event-time* 기준의 *stateful exactly-once* 스트림 연산을 수행하는 분산 프로세서이다. 둘의 결합은 "내구성 있는 입력(Ingress) + 상태를 가진 진정한 스트림 처리(True Streaming Engine)"라는 데이터 파이프라인의 표준 청사진을 완성한다.
> 2. **가치**: 전통적인 T+1 배치 ETL 대비 end-to-end latency를 **수 초 이내**로 단축하고, 이벤트 단위 처리를 통해 비즈니스 의사결정·이상탐지·개인화 추천을 *실시간*으로 수행 가능. 단일 파이프라인이 batch/log 두 경로를 모두 커버하여 운영 복잡도와 인프라 비용을 **30~50% 절감**하며, 장애 시에도 checkpoint 복구로 **데이터 유실 0**을 보장한다.
> 3. **판단 포인트**: ① 카파(Kappa) vs 람다(Lambda) 아키텍처 선택, ② Kafka 파티션 수와 Flink 병렬성(parallelism) 매핑, ③ HashMapStateBackend vs RocksDBStateBackend (State 크기 GB 이상이면 RocksDB), ④ Event time vs Processing time (Watermark 전략), ⑤ Flink 2.0(Adaptive Batch)와 같은 신규 옵션의 트레이드오프. 이 결정이 결국 비용·latency·정확성·장애복구시간(RTO)을 좌우한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 시대적 배경과 요구사항의 변화

기존의 **배치 기반 분석(ETL + Data Warehouse + BI)** 패러다임은 데이터를 야간에 모아서 일 1회 리포트를 생성하는 T+1 방식을 채택했다. 하지만 **4차 산업혁명, 디지털 전환(DX), 초연결(Hyper-connectivity) 사회**로 진입하면서 다음과 같은 비즈니스 요구가 폭발적으로 증가했다.

| 요구 시나리오 | 요구 latency | 전통 배치의 한계 |
| :--- | :--- | :--- |
| 금융 사기 탐지(FDS) | < 1초 | 사기 발생 12시간 후 적발 |
| IoT 센서 이상 탐지 | < 5초 | 설비 고장 후 통보 |
| 전자상거래 실시간 추천 | < 500ms | 클릭 후 다음날 쿠폰 |
| 게임 부정행위 탐지 | < 3초 | 부정 후 24시간 차단 |
| 광고 클릭 과금/어뷰징 | < 1초 | 일간 정산 후 어뷰징 |

배치 시스템은 **① 지연(latency) ② 코드 중복(batch/logic 별도 작성) ③ 디스크 I/O 비효율 ④ 비즈니스 변화 대응력 부족**이라는 구조적 한계를 가진다. 이를 해결하기 위해 **이벤트 스트리밍(Event Streaming)** 패러다임이 등장했고, 그 중심에 **Kafka + Flink**가 있다.

### 1.2 시스템 전체 흐름 (Concept Architecture)

```text
+--------------------------------------------------------------------------+
|                       Event Producers (다중 소스)                          |
|   [Web/App 로그]  [DB CDC]  [IoT 센서]  [API Gateway]  [Message Queue]   |
+------+----------+----------+----------+----------+-----------------------+
       |          |          |          |          |
       v          v          v          v          v
+--------------------------------------------------------------------------+
|                       Apache Kafka Cluster (Durable Buffer)              |
|  +--------------------+  +--------------------+  +--------------------+ |
|  |  Topic: user-click |  |  Topic: order-tx   |  |  Topic: cdc-orders | |
|  |  Partitions: 12    |  |  Partitions: 24    |  |  Partitions: 6     | |
|  |  Retention: 3 days |  |  Retention: 7 days |  |  Retention: 1 day  | |
|  +--------------------+  +--------------------+  +--------------------+ |
|  [Broker 1]   [Broker 2]   [Broker 3]   (KRaft Controller, no ZK)       |
|  Replicated (RF=3), ISR 관리, Log Compaction 옵션                          |
+---------------------------------+----------------------------------------+
                                  |  FlinkKafkaSource (Flink 1.18+ Source API)
                                  v
+--------------------------------------------------------------------------+
|                      Apache Flink Cluster (Stream Processor)             |
|                                                                          |
|  +------------------+    +------------------+    +------------------+    |
|  |   JobManager     |◄--►|   TaskManager-1  |    |   TaskManager-2  |    |
|  |  - Scheduler     |    | Source -> Map     |    |  KeyBy -> Window  |    |
|  |  - Checkpoint    |    | Filter -> Enrich  |    |  Aggregate -> Sink|    |
|  |    Coordinator   |    |  (Slot 1,2,3,4)  |    |  (Slot 5,6,7,8)  |    |
|  +------------------+    +------------------+    +------------------+    |
|           |                                                            |
|           v  (RocksDB / HashMap State Backend)                          |
|  +-----------------------------------------------------------------+    |
|  |  Checkpoint Storage: S3 / HDFS / NFS (Exactly-Once 보장)         |    |
|  +-----------------------------------------------------------------+    |
+---------------------------------+----------------------------------------+
                                  |  FlinkKafkaSink (Two-Phase Commit)
       +--------------------------+--------------------------+
       v                          v                          v
+------------------+    +------------------+    +------------------+
|  Sink Systems    |    |  Serving Layer   |    |  Alerting / BI   |
|  (OLTP / DW)     |    |  (Redis / ES)    |    |  (Grafana / Slack)|
|  PostgreSQL      |    |  검색/추천        |    |  대시보드         |
|  ClickHouse      |    |                  |    |                  |
+------------------+    +------------------+    +------------------+
```

### 1.3 전통 패러다임 대비 새로운 패러다임의 가치

- **기존**: `Source -> (N hours) -> Batch Job (Hadoop/Spark) -> DW -> BI`
- **신규**: `Source -> Kafka (durability) -> Flink (low-latency transform) -> Sink` + 필요 시 동일 토픽을 재생(replay)하여 배치 분석도 가능 -> **Kappa Architecture**

> **📢 섹션 요약 비유**: 기존 배치가 "하루치 우편을 한꺼번에 분류하는 우체국"이었다면, Kafka + Flink는 "택배 컨베이어 벨트(Kafka) 위에 실리는 물건을 실시간으로 분류·포장(Flink)하는 자동 물류센터"와 같다. 택배는 컨베이어에 흘러들자마자 분류되어 곧바로 배송 차량으로 실린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Apache Kafka 핵심 아키텍처

Kafka는 단순한 메시지 큐가 아니라 **분산 커밋 로그(Distributed Commit Log)** 이다. Producer는 broker에 append-only로 쓰고, Consumer는 offset을 기억하면서 독립적으로 읽는다. **디스크에 순차 쓰기(sequential I/O) + OS page cache + zero-copy sendfile** 덕분에 디스크 기반임에도 고성능을 낸다.

```text
+------------------------------------------------------------------+
|            Kafka Broker Internals (Per Topic-Partition)          |
|                                                                  |
|   +--------------------------------------------------------+     |
|   |  Partition 0  (Topic: orders, Replication Factor = 3)  |     |
|   |  +---------+ +---------+ +---------+ +---------+     |     |
|   |  |Segment 0| |Segment 1| |Segment 2| |  Active |     |     |
|   |  |  .log   | |  .log   | |  .log   | |  .log   |     |     |
|   |  |  .index | |  .index | |  .index | |  .index |     |     |
|   |  |.timeidx | |.timeidx | |.timeidx | |.timeidx |     |     |
|   |  +---------+ +---------+ +---------+ +---------+     |     |
|   |