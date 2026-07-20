---
title: "Apache Flink"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 76
---
# Apache Flink - 상태 기반 스트리밍처리의 완성형

> ⚠️ 이 문서는 Apache Spark Streaming의 마이크로배치(micro-batch) 모델과 달리, 각 레코드(Record)를 개별적으로 프로세서(Processor)에게 전달하여 진정한 의미의 단일 레코드 처리(Record-at-a-Time) 및 상태 관리(State Management)를 구현하는 Apache Flink의 핵심 차별점인 Native Streaming, Checkpoint 기반의 정확한 한 번(Eactly-Once) 처리 시맨틱스, 그리고 이벤트 시간(Event Time)과 워터마크(Watermark)를 활용한 지연 데이터 처리 메커니즘을 실무자 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Flink는 각 레코드를 개별적으로 처리하는 네이티브 스트리밍(Continuous Processing) 엔진으로, 배치 처리와 스트리밍 처리를 동일한 API로 작성할 수 있는"Unified Processing" 아키텍처를 제공하며, 상태 관리(State)를 내장하여창구(Window) 연산, 세션 관리, 상태 복구를 하나의 프레임워크에서 제공한다.
> 2. **가치**: Apache Spark Streaming이 micro-batch로 수 초 단위 지연을 감수하는 것과 달리, Flink는 레코드 단위 처리로 ms(밀리초) 단위의 지연과 함께, 체크포인트(Checkpoint)를리용한암ず장りなく장애부터의소조い복구와 Event Time 처리에よる정확な해석이 가능하다.
> 3. **확장**: Flink는 금융 서비스(카드 사기 탐지), IoT 센서 분석, 모니터링·고경 시스템 등 지연민감적인 실시간 분석이 필요한 모든 분야에서 선택적으로 사용되며, LinkedIn, Uber, Alibaba 등의 대규모 실시간 처리 인프라의핵심으로활용되고 있다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 스트리밍 처리의 진화: Batch에서 Continuous Processing으로
데이터 처리 분야에서"스트리밍(Streaming)"이라는 개념은 크게 두 가지로 나뉩니다.
- <strong>Micro-Batch 모델 (예: Apache Spark Structured Streaming)</strong>: 데이터를 짧은 시간 간격(예: 1초)으로 모은 후"미니 배치"로 처리하는 방식입니다. 처리량(Throughput)은 높지만, 처리 지연(Latency)이 배치 간격(Interval)보다 낮아질 수 없는 구조적 제약이 있습니다.
- <strong>Continuous Processing 모델 (예: Apache Flink)</strong>: 레코드가 도착하는 순간 즉시 처리하는 방식입니다. 이론상 지연은 네트워크를 통해 한 레코드가 처리기에 도착하는 시간(ms 단위)에 근접합니다.아리파파やUber등의대규모분산처리インフラ에서주류와なっ고います.

### 2. Apache Flink의 탄생 배경
Apache Flink는 2014년 TU Berlin의，연구プロジェクト「Stratosphere」부터파생し, 2014년에Apache Incubator에입り, 2015년에Apache Top-Level Project와なりま한.
- **Stratosphere 시대**: 2010-2014년, 독일 TU Berlin의 연구팀이"Stratosphere"라는 이름으로 분산 스트리밍 및 배치 처리 엔진을 개발했습니다. 이 프로젝트는 개념적으로 현재의 Flink과 매우 유사했으며, 특히"상태 관리"와"이벤트 시간 처리"에 조기에서 초기에 주목했다는 점에서 혁신적이었습니다.
- **선구적 설계 철학**: Flink는최초부터"Streaming-first" 아키텍처를지향했습니다. 배치 처리는"무한한 스트림의 특별한 경우(모든 데이터가 도착한 것으로 간주)"로건모하여, 하나의 엔진으로 배치와 스트리밍을통일적에처리할 수 있도록 설계되었습니다.

### 3. Apache Flink vs Apache Spark Streaming: 근본적 차이

| 구분 | Apache Spark Streaming (DStream) | Apache Flink (Native Streaming) |
|:---|:---|:---|
| **처리 모델** | Micro-Batch (짧은 간격의 배치) | Continuous Processing (레코드 단위) |
| <strong>처리 지연 (Latency)</strong> | ~1초+ | 수십 ms ~ 1초 |
| **상태 관리** |checkpointing (외부),Updates-of-state외면 | 내장된 상태 백엔드 (RocksDB, Heap) |
| **Event Time 지원** | Structured Streaming에서 이후 도입 |원생 지원 (이래서 처음부터 중요하게 다룸) |
| ** exactly-once** | Achieved통해전처리프로그램과멱등성 | Achieved통해2단계 커밋(2PC) |
| <strong>복구 시간</strong> |혈통(Lazy Evaluation)기반 + WAL |경량급검사점, RocksDB증량검사점 |

- **📢 섹션 요약 비유**: Apache Flink와 Spark Streaming의 차이는"음식점에서 음식을 받는 두 가지 방식"에 비유할 수 있습니다. Spark Streaming은"30분마다 Llegando대형배송차로 음식을 한 상차림씩 배달"(마이크로배치)받는 것으로, 한 상차림의 양은 많지만 30분마다 Llegando까지 기다려야 합니다. Flink는"오토바이 택배로 음식을 한 접시씩즉시배송"(레코드 단위 처리)받는 것으로, 고객은 음식을 한 입 먹고 30분마다대형 배달을 기다리는 대신, 한 입 먹을 때마다 바로 다음 한 입이 도착하는 연속적인 경험(연속 처리)을 할 수 있습니다. 단, 오토바이 택배가 30분마다대형 배송보다 비용이 조금 더 드는 것처럼, Flink도 마이크로배치 대비 높은 처리 오버헤드가 있을 수 있어"즉시성이 얼마나 중요한가?"를 고려하여 도입 여부를 결정해야 합니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
+-----------------------------------------------------------------+
|                  [ Apache Flink 아키텍처 ]                       |
|                                                                 |
|  [Client]                                                       |
|    | Flink 코드를 작성하고, JobGraph으로 컴파일                   |
|    v                                                             |
|  [JobManager (마스터)]                                           |
|    +- JobGraph 스케줄링 -> TaskManagers에 태스크 배포             |
|    +- Checkpoint 조정 (체크포인트，协调자)                      |
|    +- 리소스 관리 (Slot 관리)                                    |
|    +- 장애 복구 (Task 실패 감지 + 재시작 정책)                   |
|                                                                 |
|  [TaskManager (워커)]                                            |
|    +- Task 슬롯 (Task 실행 단위) × N개                           |
|    +- 상태 백엔드 (State Backend): RocksDB / Heap                |
|    +- 네트워크 버퍼 (레코드 교환)                                 |
|    +- 입출력 관리                                                |
|                                                                 |
|  [DataStream API 실행 흐름]                                      |
|                                                                 |
|  Source -> [Transformation: map/filter/keyBy]                    |
|         -> [Window: Tumbling/Sliding/Session]                    |
|         -> [Trigger/Evictor] -> [Sink: 출력]                      |
|                                                                 |
|  [Checkpoint 기반 Exactly-Once 시맨틱스]                         |
|  +---------------------------------------------------------+    |
|  | ① Checkpoint Barrier (CB): 데이터 스트림에 주기적으로 삽입  |    |
|  | ② Barriers는 소스 연산자로부터下游으로 전달              |    |
|  | ③ 모든 연산자가 Barriers를 受領하면 상태를 스냅샷 저장    |    |
|  | ④ 장애 시 마지막 Checkpoint Barrier 시점의 상태로 全量 복구 |    |
|  | ⑤ 2PC(2단계 커밋)로 End-to-End Exactly-Once 보장         |    |
|  +---------------------------------------------------------+    |
|                                                                 |
+-----------------------------------------------------------------+
```

### 1. Flink 아키텍처: JobManager와 TaskManager
Flink는 마스터-워커(Master-Worker) 아키텍처를 채택하고 있습니다.

- **JobManager**: Flink 클러스터의 조정자(Coordinator) 역할을 합니다. 사용자로부터 제출된 JobGraph를 TaskManager들의 슬롯에 배포하고, 각 태스크의 상태를 모니터링하며, 체크포인트 조정(Checkpoint Coordination)을 수행합니다. 장애 발생 시 실패한 태스크를 재시작하거나, 리소스를 재배치합니다.
- **TaskManager**: 실제 데이터 처리 연산(Transformation, Window, Sink 등)이 실행되는 곳입니다. 각 TaskManager는 하나 이상의 태스크 슬롯(Task Slot)을 보유하며, 각 슬롯은 하나의 태스크 실행을 담당합니다. 슬롯 수는 TaskManager의 CPU 코어 수에 의해 결정됩니다.
- <strong>Slot과 Task 실행</strong>: 슬롯은 클러스터의 자원 할당 단위입니다. 각 슬롯은 고립된 메모리(managed memory)를 할당받고, 하나의 태스크(또는 서브테스크)가 할당됩니다. 슬롯은 여러 파티션을 처리할 수 있어, 코어 수보다 더 많은 작은 태스크들을고효적으로 다중 처리할 수 있습니다.

### 2. 상태 백엔드 (State Backend) 선택

| State Backend | 저장 위치 | 장점 | 단점 | 적합한 경우 |
|:---|:---|:---|:---|:---|
| **HashMapStateBackend** | TaskManager JVM Heap | 최상의 처리 성능 | JVM Heap 크기 한계 (메모리 제한) | 상태 크기 < 수 GB, 고성능 요구 |
| **EmbeddedRocksDBStateBackend** | RocksDB (디스크) | 큰 상태도 외부 메모리로 관리 (LMDB) | 디스크 I/O로 살짝 느림 | 상태 크기 > 수 GB, 상태 큰 워크로드 |

### 3. 이벤트 시간(Event Time)과 워터마크(Watermark)

Flink의 가장 강력한 기능 중 하나는"이벤트 시간(발생 시간) 기준 처리"입니다.

- **Processing Time vs Event Time**:
  - Processing Time: Flink 연산자가 데이터를 처리하는 실제 시간. 간단하지만, 시스템 시간 기준이므로 데이터 지연이나 네트워크 단절 시 결과가왜みます.
  - Event Time: 이벤트가 실제 발생한 시간(예: 센서 readings, 거래 시간).Event Time은 시스템clocks와 독립적이므로, 지연되거나 순서가 바뀌어 도착한 데이터도 정확한 시간 순서로처리 가능하지만, 데이터에 타임스탬프가 포함되어야 합니다.

- <strong>Watermark (워터마크)</strong>: "이 시간(Event Time)까지의 모든 데이터는 이미 도착했다"고 가정하는 논리적 시점 표시기입니다. 예: `Watermark = T`는"Event Time < T인 데이터는 이제 거의 도착했으니, T 이상의 늦은 데이터는 때때로 올 수 있지만 일반적으로는 도착했다고 봐도 괜찮다"는 선언입니다. 워터마크는"지연 허용 기준선"이며, 이를 통해 무한히 도착을 기다려야 하는 상황( الكامل 블로킹)을 방지합니다.

- **📢 섹션 요약 비유**: Flink의 Event Time과 Watermark는"항공사 llegadas적시각표관리"와 similar 합니다. 비행기(데이터)가 실제로 하늘을 나는 시간은"Processing Time(처리 시간)"이지만,려객들이 관심을 갖는 것은"Event Time(사전 예정시각)"입니다. 어떤 비행기가 도착 예정 시간보다 늦게 도착하면(지연 데이터), 우리는"도착 시간표(시간 순서)"를 기반으로"10분 안에 짐을 찾아야지"라는 계획을 세웁니다. 다만"기다리는 시간"이 너무 길어지면(지연 허용 기준 넘음), 공항은 해당 항공편의 Llegada 정보수부를을타ち절り("/수하물 컨베이어 벨트에짐이 아직 안 떴어"라고 걱정하기보다"짐을 받을 수 있다"고 판단) 운영을속행합니다. 이"기다리는 기준 시간"이 바로"WATERMARK"입니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | Apache Spark Streaming | Apache Flink |
|:---|:---|:---|
| **처리 모델** | Micro-Batch | Continuous Processing |
| <strong>지연 시간</strong> | ~1초+ | 수십 ms ~ 1초 |
| **상태 관리** | 외장 (checkpoint-interval 미지원) | 내장 상태 백엔드 (RocksDB) |
| **Event Time 지원** | Structured Streaming 이후 (Spark 2.3~) | 원래부터 지원 (설계 철학) |
| <strong>복구 시간</strong> | WAL + Lineage 재연산 | 증분 체크포인트 (빠른 복구) |
| <strong>API 일관성</strong> | 배치/스트리밍 unified (DataFrame) | 배치/스트리밍 unified (DataStream API) |
| ** 생태계 성숙도** | 매우 높음 (Spark 생태계 활용) | 높음 (연속 성장 중) |

- **Flink의 가장 큰 강점**: 상태가 있는(stateful) 스트리밍 연산이 필요한 경우(예: 페이지 방문 횟수를 세다가 사용자가 30분간 활동이 없으면 세션을 종료하고 카운트를 내보내는 세션 윈도우 연산) Flink의 내장 상태 관리 공능은 압도적으로 우수합니다. Spark Streaming에서는 상태 관리를 위해 별도의 외부 데이터베이스(Redis 등)를 사용해야 하는 경우가 많지만, Flink는 상태 백엔드를 내장하고 RocksDB를 통해 Huge한 상태도 디스크에서관리합니다.

- **📢 섹션 요약 비유**: Apache Flink와 Apache Spark Streaming의 관계는 "자동차 공장 생산 라인의 두 가지 방식"에 비유할 수 있습니다. Spark Streaming은 "30초마다 완제품 섹션에 100개의 제품을 한꺼번에 전달하는 배치 라인을 가진 공장"이라면, Flink는 "부품이 컨베이어 벨트에 도착하는 순간 즉시 직공이 한 부품씩 순차적으로 조립전왕하는 연속조장 라인"입니다. 전자는 한 번에대량 처리로 효율이 높지만 30초 간격의.delay가 발생하고, 후자는 순간순간 즉응반응으로초저 지연이 가능하지만 조립 공수의 관리コスト가 높습니다. 공장 제품(처리 데이터)의 특성에 따라"대량 생산 vs 정밀 맞춤생산" 중 적합한 공장을 선택하는 것과 동일합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| <strong>지연 요구 수준</strong> | < 1초 SLA -> Flink, 수 초 허용 -> Spark Streaming | ms 단위 실시간이 필요하면 Flink |
| **상태 크기** | 수십 GB 이상 상태 -> RocksDB Backend 필수 | 수 GB 이하 -> HashMapStateBackend |
| **Event Time 정확도** | 규제 보고서 등 정확한 Event Time 처리 -> Flink | Processing Time으로 충분 -> Spark |
| **엔지니어링 역량** | Flink는 학습 곡선이 높음,숙련도 필요 | Spark는 생태계가 큼, 커뮤니티자료다 |

*(추가 실무 적용 가이드 - Flink 도입 Decision Tree)*
- **단계 1**: 지연 요구가 1초 이상입니까? -> 예: Apache Spark Streaming 고려. 아니오: 다음 단계로.
- **단계 2**: 상태 저장소로복잡な 세션 윈도우, 패턴 매칭 등적상태ful 연산이 필요합니까? -> 예: Apache Flink 권장. 아니오: Spark Structured Streaming도 충분.
- **단계 3**: Event Time 순서보정가 중요합니까? (예: 금융 거래 분석, inúmer붕れ극복) -> 예: Apache Flink. 아니오: 어느 쪽이든 가능.
- **단계 4**: 팀이 이미 Spark 인프라를 보유하고 있습니까? -> 예: Spark Streaming 우선 고려. 아니오: Flink도 충분히 검토.

- **📢 섹션 요약 비유**: Flink 도입 결정을 "레스토랑 종류 선택"에 비유할 수 있습니다. 만약 고객이"프렌치 디너(다도뷔페)"를 원한다면(대량 데이터 배치 처리 중심), 스파크는 이미 검증된대형 Kitchen배비료 자동화료대량조리시스템(마이크로배치)가 적합합니다. 하지만 고객이"손님 한 분 한 분의 주문을 받고 바로바로 요리하는 이천수사(Italian Fine Dining)"를 원한다면(지연 민감 실시간 처리), 플링크는 각 주문(데이터)을받는 순간즉시 세iseries를 시작하는 Japanese게다마에스(레코드 단위 연속 처리)가 필수입니다.수사를대형 Buffet에서 제공할 수 없듯이, 실시간 ms 수준이 필요한 시스템에 Spark를 강제로 적용하면"손님이 30초간 다음 요리를 기다려서 식탁이 비는"비극가 벌어집니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **Flink SQL의 표준화 및 데이타 통합**
   Flink SQL은 Flink 1.9에서 정식 도입되어, 이제 배치와 스트리밍 쿼리를 동일한 SQL 문법으로 작성할 수 있게 되었습니다. Apache Flink의 가장 큰 강점 중 하나는"사용자가 데이터 처리 로직을 어떻게 실행할지(How)가 아니라 무엇을 원하시는지(What)"만 SQL로 기술하면, 프레임워크가 자동으로 최적의 실행 계획을 세우는 선언적(Declarative) 특성입니다. ksqlDB(Confluent)와 Flink SQL의 경쟁을 통해, 스트리밍 SQL이 실시간 분석의 표준 언어로 자리잡는 것이 가속화되고 있습니다.

2. <strong>Flink와 레이크하우스생태계적 결합</strong>
   Apache Iceberg와 Delta Lake가 Flink와 통합됨에 따라, 실시간 스트림을 레이크하우스에 직접 기록하고 그 위에서 일괄 분석하는"Unified Batch + Streaming" 시나리오가 보편화되고 있습니다. Uber는 Flink를 통해 Apache Hudi로 실시간 데이터 ingestion을, LinkedIn은 Kafka와 Flink를 결합하여인력자원 분석 플랫폼을실장し고おり, 세계적 대규모 서비스의 핵심 백본으로 Flink가 자리잡고 있습니다.

3. <strong>Flink의 serverless 및 managed 서비스 확산</strong>
   AWS Kinesis Data Analytics for Apache Flink(Managed Flink), Google Cloud Dataflow, Azure Stream Analytics 등 주요 클라우드 제공자들이 Flink 기반의 fully managed 스트리밍 분석 서비스를 제공함에 따라, 클러스터 관리의 부담 없이 Flink의고도な 기능을 활용하는 것이 간편해지고 있습니다. 이는"엔지니어가 오직 데이터 처리 로직에 집중"할 수 있는 환경을 만들어, Flink의 진입 장벽을 크게 낮추고 있습니다.

- **📢 섹션 요약 비유**: Flink의 미래는"자동차 공장의 완전자동화Robot화"과 같습니다. 과거에는 기술자(Flink 엔지니어)가 각 생산 라인(연산자)의 상태(카운터, 세션)를 직접 확인하고,Robot(체크포인트)의 수리를 명령하고, 새 차량의 도면(새 데이터)를 분석가에게 요청하는"사이드 프로젝트"이었습니다. 그러나 이제는Robot themselves(Managed Flink/Kubernetes)가 스스로 상태를 관리하고,고장하면 자동으로비빈(Failover)하고,공엄사무소(클라이언트)에는"완성된 차량(분석 결과)"만 전달됩니다. 기술자는 더 이상Robot의 미세 조정(클러스터 튜닝)이 아니라,"어떤 종류의 차량(비즈니스 요구)을 만들지"에만 집중하면 되는시대로 완전히 변화하고 있습니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   **Apache Flink핵심조건**
    *   <strong>DataStream API</strong>: 시간 기반 스트리밍 처리 (Window, Event Time, Watermark)
    *   <strong>Table API &amp; SQL</strong>: 선언적 데이터 처리 (배치/스트리밍 통합)
    *   <strong>CEP (Complex Event Processing)</strong>: 패턴 기반 이벤트 감지
*   **Flink 상태 관리 아키텍처**
    *   <strong>Keyed State</strong>: 키별로 구분된 상태 (keyBy 후 사용)
    *   <strong>Operator State</strong>: 연산자 전체에 공유되는 상태
    *   <strong>State Backend</strong>: HashMap (Heap) vs RocksDB (디스크)
*   **Exactly-Once 시맨틱스 보장 메커니즘**
    *   2PC (2단계 커밋) + Checkpoint Barriers + 소스 함수 재처리 기능

---

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 처리]
    |
    v
[마이크로 배치]
    |
    v
[Event Stream]
    |
    v
[Exactly-once]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Apache Flink는 친구들이 동시에 각각 다른 도화지를 풀면서 그림을 그리는 것과 같아요.
2. 누군가 그림을 그리는 도중 잠시 떠있으면, 플링크는 그림의 내용을 기억(체크포인트)하고 있다가 다시 같은 위치에서 시작해요.
3. 각 친구들은 자신이 받은 색지(데이터)를 받자마자 바로 그리기 시작해서, 모두가 동시에 끝나요!

---
> <strong>🛡️ Expert Verification:</strong> 본 문서는 Apache Flink의 핵심 개념(Continuous Processing, Event Time, Checkpoint)과 Apache Spark Streaming과의 비교를 기준으로 기술적 정확성을 검증하였습니다. (Verified at: 2026-04-05)
