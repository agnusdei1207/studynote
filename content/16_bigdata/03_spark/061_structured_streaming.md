---
title: "Spark Structured Streaming"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 61
---
## 핵심 인사이트 (3줄 요약)
1. <strong>구조적 스트리밍 (Structured Streaming)</strong>은 Spark SQL 엔진 위에서 동작하는 확장 가능하고 결함 허용(Fault-tolerant)이 가능한 스트림 처리 엔진이다.
2. 실시간 데이터를 지속적으로 추가되는 <strong>'무한 테이블(Unbounded Table)'</strong>로 간주하여, 배치 처리와 동일한 DataFrame/Dataset API로 스트리밍 로직을 작성할 수 있다.
3. <strong>체크포인트와 Write-ahead Log</strong>를 통해 '정확히 한 번(Exactly-once)' 처리 보증을 제공하며, 이벤트 시간(Event-time) 처리 및 워터마크 기능을 완벽히 지원한다.

---

### Ⅰ. 개요 (Context & Background)
- **정의**: 정적 데이터에 대한 배치 쿼리를 실행하듯이 스트리밍 데이터를 처리할 수 있게 해주는 고수준 API 기반의 실시간 처리 프레임워크이다.
- **배경**: 기존 DStream(마이크로 배치)의 복잡한 RDD 조작과 이벤트 시간 처리의 한계를 극복하고, 배치와 스트리밍 코드의 통합(Unified)을 실현하기 위해 등장했다.
- **주요 활용**: 실시간 ETL 파이프라인, 실시간 대시보드 업데이트, IoT 센서 데이터의 이상 탐지, 실시간 개인화 추천 시스템 등에서 표준으로 사용된다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 무한 테이블 (Unbounded Table) 모델
```text
[ Data Stream ] (Incoming events)
      |
      V
[ Input Table ] (Unbounded / Append-only)
+-------+-------+-------+
| Col 1 | Col 2 | Col 3 |  <-- New data appended every trigger
+-------+-------+-------+
      |
      V [ Incremental Query ] (Spark SQL Engine)
      |
[ Result Table ] (Updated state)
      |
      V [ Output Sink ] (External Storage)
```

#### 2. 핵심 처리 메커니즘
- **Trigger**: 데이터를 처리할 주기를 결정한다 (예: 1초마다, 혹은 데이터가 들어오는 즉시 처리하는 연속 모드).
- **Watermarking**: 늦게 도착한 데이터(Late Data)를 얼마나 기다릴지 정의하여 상태 정보의 메모리 무한 증식을 방지한다.
- <strong>State Store</strong>: 윈도우 합계나 조인 처리를 위해 필요한 중간 상태값을 인메모리 혹은 HDFS/S3에 안전하게 보관한다.
- <strong>Fault Tolerance</strong>: Checkpointing을 통해 장애 발생 시 마지막 처리 지점부터 중단 없이 재시작할 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Spark Streaming (DStream) | Structured Streaming |
| :--- | :--- | :--- |
| <strong>기반 추상화</strong> | RDD (Low-level) | DataFrame / Dataset (High-level) |
| **처리 모델** | 마이크로 배치 전용 | 마이크로 배치 + 연속 처리(Continuous) |
| **이벤트 시간 처리** | 지원 미흡 (Processing Time 위주) | 워터마크 기반 완벽 지원 |
| **코드 통합** | 배치 코드와 별도 작성 필요 | 배치 쿼리와 90% 이상 동일 코드 사용 |
| **보증 수준** | At-least-once (일부 상황) | Exactly-once (엔드 투 엔드 보장) |

---

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- **배치-스트림 통합 아키텍처**: 동일한 로직을 배치 데이터와 실시간 데이터에 모두 적용할 수 있어 유지보수 비용을 획기적으로 낮춘다 (Lambda/Kappa 아키텍처 구현 용이).
- <strong>Sink 선택 전략</strong>: Kafka, HDFS, Console 외에도 Delta Lake와 결합하여 실시간 데이터 레이크하우스를 구축하는 것이 최신 기술 트렌드이다.
- <strong>성능 최적화</strong>: 셔플링을 유도하는 윈도우 연산 시 파티션 개수(`spark.sql.shuffle.partitions`)를 데이터 규모에 맞게 조정하고, 로컬 상태 저장소의 성능(RocksDB 등)을 튜닝해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 데이터 엔지니어가 실시간 처리를 위해 특별한 기술을 새로 배울 필요 없이 기존 SQL/DataFrame 지식만으로 고성능 실시간 시스템을 구축할 수 있게 한다.
- **결론**: 구조적 스트리밍은 '배치와 스트리밍의 경계'를 허문 혁신적인 도구이다. 향후 Apache Flink와의 경쟁 속에서도 Spark 생태계의 강력한 통합 이점을 바탕으로 실시간 데이터 처리의 중추 역할을 지속할 것으로 전망된다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
1. <strong>Micro-batching</strong>: 데이터를 아주 작은 단위로 묶어 처리하는 방식
2. <strong>Exactly-once Semantics</strong>: 데이터 손실이나 중복 없이 정확히 한 번 처리됨을 보장
3. **Event Time**: 데이터가 시스템에 입력된 시간이 아닌, 실제 발생한 시간

---

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 처리 (Batch Processing) — 정해진 주기 대규모 데이터 처리]
    |
    v
[스트리밍 처리 (Streaming) — 실시간 연속 데이터 처리]
    |
    v
[Spark Streaming (DStream) — RDD 기반 마이크로 배치]
    |
    v
[Structured Streaming — DataFrame API 기반 연속 처리]
    |
    v
[워터마크 (Watermark) — 지연 데이터 처리 기준 시간 설정]
    |
    v
[Delta Live Tables — 선언형 스트리밍 파이프라인 자동화]
```
Structured Streaming은 DStream의 복잡성을 DataFrame API로 추상화하여, 배치와 스트리밍을 통합하는 현대 실시간 파이프라인의 표준이 되었다.

### 👶 어린이를 위한 3줄 비유 설명
1. "수도꼭지에서 물이 계속 나오는 것처럼, 멈추지 않고 들어오는 데이터를 바로바로 정리하는 기계예요."
2. "예전에는 바가지로 물을 퍼 날랐다면(배치), 이제는 호스를 연결해서 물이 흐르는 대로 분류하는 것과 같아요."
3. "깜빡하고 늦게 들어온 데이터도 제자리에 쏙쏙 끼워 넣어주는 아주 똑똑한 정리 대장이랍니다!"
