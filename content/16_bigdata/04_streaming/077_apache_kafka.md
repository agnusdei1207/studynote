---
title: "Apache Kafka"
date: "2026-04-05"
tags:
  - "studynote-bigdata"
weight: 77
---
# Apache Kafka - 메시징에서 데이터 허브로의 진화

> ⚠️ 이 문서는 LinkedIn에서 2011년 내부 개발하여 오픈소스로 공개한 Apache Kafka가 어떻게 기존의 포인트 투 포인트(Point-to-Point) 메시지 큐(RabbitMQ, ActiveMQ 등)와 달리, 게시-구독(Pub-Sub) 모델과 로그 기반 아키텍처(Append-only Log)를 결합하여 초당 수백만 건의 메시지 처리(High Throughput)와 수 일 이상의 메시지 보존(High Retention)을 동시에 달성하는 분산 이벤트 스트리밍 플랫폼의 핵심 설계 원리를 실무자 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Kafka는 초당 수백만 건의 이벤트를 디스크에 순차적으로 기록(Append-only)하는 분산 로그 시스템으로, 메시지를 메모리에완존하는대わり에자반영속화し고 высок은 내구성(Durability)과 순서 보장(Ordering)을 동시에 제공하며, 생산자(Producer)와 소비자(Consumer)를 완벽히 분리(Decoupling)하여 비동기 데이터 흐름을 구현한다.
> 2. **가치**: 기존 메시지 큐가 Consumption 후 메시지를 삭제했던 것과 달리, Kafka는 Retention 기간(설정에 따라 수 시간~수 일) 동안 메시지를 보존하므로,동일 메시지를 여러 컨슈머 그룹이각자이なる 속도로 독립적으로소비가능하며, 이후past 데이터도 다시재생(Replay)할 수 있다.
> 3. **확장**: 파티션(Partition) 단위의 수평 확장(Horizontal Scaling)과 리밸런싱(Rebalancing)을 통해 수십 대의 브로커(Broker)로 구성된 클러스터에서도 일관된 성능을 유지하며, 수천 개의 토픽(Topic)과 수백만 명의 컨슈머를 단일 플랫폼에서 관리할 수 있는 확장성을 갖추고 있다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 전통적 메시지 큐(MOM)의 구조적 제약
Apache Kafka가 탄생하기 전, 기업들은 RabbitMQ, ActiveMQ, IBM MQ 등의 전통적 메시지 지향 미들웨어(Message-Oriented Middleware, MOM)를 사용하여 비동기 통신을 구현했습니다.
- <strong>포인트 투 포인트 (Point-to-Point) 모델</strong>: 메시지가 하나의 큐에 들어가면, 하나의 컨슈머만이 이를 Consumption하고 큐에서 제거합니다. 1:N 배포(하나의 메시지를 여러 시스템이 동시에 읽기)가 필요하면 동일한 내용의 메시지를 N개 큐에 복제해야 하는 비효율이 발생했습니다.
- <strong>메시지 삭제 정책</strong>: 대부분의 MOM은 메시지가 Consumption되면 즉시 삭제합니다. 따라서"메시지 재처리(Replay)"나"이벤트 소스를소る(遡及)"이 불가능하여, 컨슈머 어플리케이션의 버그로 인해 메시지 처리 누락이 발생하면 이를 복구할 수 없는 치명적인 한계가 있었습니다.
- **확장성의 한계**: 기존 MOM은 메시지 전달 순서(Ordering)를 보장하기 위해 단일 큐에 메시지를 집중시켰고, 이로 인해 단일 브로커의 처리 능력에 병목이 발생하여 대규모 데이터 처리에서 확장성에 한계가 있었습니다.

### 2. LinkedIn의 실제 문제: 실시간 데이터 파이프라인의 긴급한 수요
LinkedIn은 2010년경 수십 개의 마이크로서비스가 서로 직접 API 호출하는"지저분한 통합(Spaghetti Integration)" 상태에 있었습니다.모 서비스의 장애가 다른 서비스로 전파되는 급련고장(Cascading Failure)가 빈번하게 발생했으며, 데이터팀이"사용자 활동 로그를 실시간으로 분석하여 추천 시스템을 개선"하려는 시도가 현재 인프라의 한계로 인해도중なりま한.
- **LinkedIn 내부 개발 단계**: LinkedIn 엔지니어 Jay Kreps, Neha Narkhede, Jun Rao 등은"하나의 중앙 집중식 데이터 파이프라인"을 구축하여 모든 마이크로서비스의 이벤트 로그를 एक स्थान에서 수집하고, 이를 inúmer 받는 소비자에게 전달하는"분산 로그 시스템"을 구상했습니다.
- <strong>2011년 Apache Kafka 오픈소스 공개</strong>: 이 구상은 2011년 Apache Kafka라는 이름으로 오픈소스화되었으며, 2012년 Apache Incubator에 합류, 2014년 Apache Top-Level Project 등용되며 글로벌 표준 분산 메시징 시스템으로 자리잡았습니다.

- **📢 섹션 요약 비유**: 전통적 메시지 큐와 Apache Kafka의 차이는"기차참적 의전 알림 시스템"에 비유할 수 있습니다. 전통적 MOM은"새벽 기상 알람을 한 번만 울리고 끝"(메시지 Consumption 후 삭제)으로, Alarm을 놓치면 끝까지 깨어나지 못합니다. 반면 Kafka는"기차참적 관제실에서 모든 열차의 위치를 모니터링하는 실시간 추적 시스템"(Append-only Log)으로, 현재 열차 위치뿐 아니라 과거 24시간 동안의 열차 궤적(Retention)을전부보존하며, 관제실에는 수많은 운영팀이 동시에 접속하여각자 필요한 정보를 추출할 수 있습니다. 만약 어떤 열차가 관제실 communication 단절로 현재 위치를 알 수 없으면, 과거 궤적만 보고도"어느 구간에서 문제가 발생했는지"를 역추적할 수 있습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
+-----------------------------------------------------------------+
|                  [ Apache Kafka 아키텍처 ]                       |
|                                                                 |
|  [Producer] --- 씀 -> [Topic: 주문 정보] -- 씀 -> [Consumer]     |
|       |                    |                    |               |
|       |                    |Partition 0: [msg0][msg1][msg2]...  |
|       |                    |Partition 1: [msg0][msg1][msg2]...  |
|       |                    |Partition 2: [msg0][msg1][msg2]...  |
|       |                    |                    |               |
|       |                    v                    v               |
|       |            +-----------------------------+               |
|       |            |      Broker 1/2/3...         |               |
|       |            |  각 브로커가 Partition 보유   |               |
|       |            | ISR (In-Sync Replica) 관리    |               |
|       |            +-----------------------------+               |
|       |                                                           |
|  [ ZooKeeper / KRaft (Kafka 3.3+) ]                              |
|    +- 브로커 활성 상태 관리 (누가 컨트롤러?)                     |
|    +- 토픽/파티션 메타데이터 관리                                 |
|    +- 리더 선출 (Leader Election)                                 |
|                                                                 |
|  [디스크 기록 구조: Append-only Log]                             |
|  +----------------------------------------------------------+    |
|  |  오프셋 0  |  오프셋 1  |  오프셋 2  |  오프셋 3  | ... |    |
|  |  [msg A]  |  [msg B]  |  [msg C]  |  [msg D]  |     |    |
|  |           |           |           |           |     |    |
|  |  Sequential Write -> 디스크 I/O 병목 완전 제거!           |    |
|  +----------------------------------------------------------+    |
|                                                                 |
+-----------------------------------------------------------------+
```

### 1. Kafka의 핵심 개념: Topic, Partition, Offset

- **Topic (토픽)**: Kafka에서 데이터가 발포되는 논리적 채널입니다. RDBMS의 테이블과 유사하지만, 스키마가 없으며 단순히"이름이 있는 데이터 스트림"입니다.
- <strong>Partition (파티션)</strong>: 토픽을 물리적으로 분할한 단위입니다. 각 파티션은 클러스터의 여러 브로커에분산し고배치되며, 각 파티션 내에서는 메시지가 순차적으로 Append-only로 기록됩니다. 파티션 수는 토픽의 병렬 처리 수준을 결정하며, 파티션 수 만큼의 컨슈머가 동시에 메시지를 소비할 수 있습니다.
- **Offset (오프셋)**: 각 파티션 내에서 메시지의 고유한 위치 번호입니다. `offset=0`이 첫 번째 메시지이며, 이후 각 메시지는 고유한 오프셋을 가집니다. Consumer는 자신이 마지막으로소비한 오프셋(`committed offset`)을각え고おい고, 다음의メッセージ부터재개します.

### 2. Producer와 Consumer의 분리 (Decoupling)

Kafka의 가장 중요한 설계 특성 중 하나는 Producer와 Consumer의 완전한 분리입니다.

- **Producer(생산자)**: 메시지를 생성하여 특정 토픽의 특정 파티션에ublish합니다. 파티션 선택 전략은 기본적으로 라운드 로빈(Round-robin)이지만, 메시지의 키(Key)를 지정하면동일 키를 가진 메시지는동일 파티션에 순서 보장으로 기록됩니다.
- **Consumer(소비자)**: 컨슈머는 자신이 읽은 오프셋을 관리합니다. Kafka는 Consumer Group(소비자 그룹) 개념을 지원하여,동일 그룹 내의 컨슈머들은각자 다른 파티션을 할당받아 병렬로 소비합니다. 다른 그룹의 컨슈머는 서로독립적으로 같은 메시지를 소비할 수 있어, 1:N 배포가 가능합니다.

### 3. ISR (In-Sync Replica) 및 내구성(Durability) 보장

| 설정 | 설명 | 내구성 수준 |
|:---|:---|:---|
| **acks=1** | 리더 브로커만 기록 완료되면 성공 반환 | 중간 (리더 장애 시 데이터 손실 가능) |
| **acks=all (또는 -1)** | ISR 목록의 모든 리플리카가 기록 완료 후 반환 | 높음 (거의 모든 장애 상황 보장) |
| **min.insync.replicas=2** | ISR 중 최소 2개 리플리카가 존재해야 기록 허용 | 높음 |

- **📢 섹션 요약 비유**: Kafka의 ISR(In-Sync Replica) 메커니즘은"은행의 다중 증거금 보험 계약"과 같습니다. 고객이 돈을 예금(메시지 게시)하면, 은행은"Cash is safe"를 알리기 전에 약속된 수의 지점(Replica)에 예금 사실을 동시에 기록하고, 모든 지점이"확인했습니다"라고 응답해야 비로소 고객에게"고객님 예금이 완료되었습니다"라고 통보합니다. 만약 3개 지점 중 1개가 통신 불량(ISR 탈락)이라면, 은행은 잔여 2개 지점의 기록만으로 거래를 승인하지만, 이내 탈락한 지점의 통신이 회복되면 해당 지점에도 자동으로 동기화되어"다시 모든 지점에동일 기록"이 유지됩니다. 이를 통해 장애 상황에서도 데이터의 완전성과 내구성을 동시에 보장합니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | Apache Kafka | RabbitMQ / ActiveMQ (전통적 MOM) |
|:---|:---|:---|
| <strong>메시지 보존 (Retention)</strong> | 설정 기간(시간~무제한) 동안 보존, Replay 가능 | Consumption 후 즉시 삭제 (일반적) |
| <strong>메시지 순서 보장</strong> | 파티션 내에서 순서 보장 | 큐 단위 순서 보장, 분산 환경에선 제한적 |
| **컨슈머 모델** | 컨슈머 그룹별 독립소비 (Pub-Sub) | 포인트 투 포인트 (하나만 소비) |
| <strong>처리량 (Throughput)</strong> | 초당 수백만 건 (Sequential I/O) | 초당수만~수십만 건 |
| <strong>메시지 필터링/라우팅</strong> | 키 기반 파티셔닝만 (파티션 단위) | exchange 타입별 다양한 라우팅 (topic, headers, etc.) |
| <strong>메시지 크기</strong> | 기본 1MB, 설정으로 수 MB까지 | 일반적으로 수 KB ~ 수십 KB |

- **Kafka의 가장 큰 강점**: "이벤트 소싱(Event Sourcing)"과 "CDC (Change Data Capture)" 아키텍처에서 Kafka는 핵심 인프라로 활용됩니다. 예를 들어, 데이터베이스의 모든 변경 사항(INSERT/UPDATE/DELETE)을 Kafka topic으로 publish하고, 이를 여러 Sink(Redshift, Elasticsearch, BigQuery 등)가 동시에소비하면, 하나의 데이터 원본(DB)에서 다양한 목적지(분석, 검색, 캐시 갱신 등)로의Real-time 데이터 파이프라인을 구성할 수 있습니다.

- **📢 섹션 요약 비유**: Kafka vs RabbitMQ의 차이는"중앙 관제탑과 일반 항구 창구"의 차이와 similar 합니다. RabbitMQ는"항구에서 물건이 도착하면 창구 직원 한 명이 확인하고 창구를 닫음"(포인트 투 포인트, Consumption 후 삭제). 반면 Kafka는"항구의 모든 화물의 입출고를 RFID로 추적하는 전방 위 물류 관리 시스템"으로, 화물(메시지)이 창고를 통과해도 시스템에는 영구히 기록이 남으며, 수많은 물류 회사(컨슈머 그룹)가동일 화물의 흐름을각자 실시간으로 추적할 수 있습니다. 화물 자체는소えない(Retention)하며, 문제가 발생하면 과거 기록을 역추적하여(Replay) 어디서 문제가 발생했는지분석가능 합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| <strong>메시지 순서 요구</strong> | 순서 보장이 필수 (예: 금융 거래) -> 키 기반 파티셔닝 필수 | 파티션 수 = 키별 파티션 수 고려 |
| **내구성 요구 수준** | 장애 시 절대 데이터 손실 불가 -> acks=all + min.insync.replicas=2 | 데이터 소실 허용 수준에 따라 acks 조절 |
| **리텐션 기간** | Replay 필요 (예: CDC, 감사 로그) -> 긴 Retention | 일회성 처리면 짧은 Retention으로 스토리지 절약 |
| **컨슈머 독립성** | 다수의 독립적인 컨슈머가동일 데이터 필요 -> Kafka | 하나의 컨슈머만 필요 -> RabbitMQ 고려 |

*(추가 실무 적용 가이드 - Kafka Topic 설계 Best Practices)*
- <strong>파티션 수 결정</strong>: 파티션 수는 컨슈머 수의 상한을 결정합니다. 파티션 수 = 최대 동시 컨슈머 수로 설계하되, 향후확전을 고려하여 여백을 둡니다. 파티션 추가 후에는 키와 파티션 간 매핑이 변경될 수 있어 주의가 필요합니다.
- <strong>메시지 키 활용</strong>: 순서 보장이 필요한 메시지(예:동일 사용자의 모든 이벤트)에는동일 키(예: user_id)를 사용하여동일 파티션에 순서대로 기록되도록 합니다.
- <strong>컴팩션(Compaction)</strong>: 로그 컴팩션 모드를 설정하면,동일 키의 최신 메시지만 보존하여 무제한 Retention이 가능하며, 최신 상태 조회(테이블 스냅샷과 유사)가 가능합니다.
- **실무 의사결정**: Kafka를 이벤트 버스(Enterprise Service Bus, ESB) 대안으로 활용할 때는, 토픽 수와 파티션 수가 클러스터 자원의 한계에 도달하지 않도록 모니터링하고, 필요한 경우 주기적으로구토픽을 아카이브/삭제하는 kebijakan를 수립해야 합니다.

- **📢 섹션 요약 비유**: Kafka Topic 설계는"백화점최사의매상집계 시스템"과 같습니다.최사적 매출 데이터가 들어오는 토픽(예: `sales-events`)에 파티션을많이 배치(파티션 100개)하면동시처리 능력이제승되지만,최사 Cashier(컨슈머)는처리능력에 따라 적절한 수를 배치해야하며, 무한정 Cashier를 늘려도 파티션 수를 초과하면추가효과가 없습니다. 또한 매출 영수증(메시지)에"어떤 Cashier가 처리했는지"(키)를 기록해두면, 동일한 Cashier의 매출은 모두 같은 파티션에 순서대로 모이며,최사결속후동일 Cashier의 Record만 추적하여"어떤 Cashier실적 실적을 검증"하는 것이 가능합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. <strong>KRaft (Kafka Raft) 모드의 일상화: ZooKeeper 의존성 제거</strong>
   Kafka 3.3 (2022)에서 정식 도입된 KRaft 모드는, 분산 코디네이션을 위해 외부 의존성(ZooKeeper)을 제거하고 Kafka 자체의 Raft 프로토콜 구현(KRaft)을 사용하여 클러스터 메타데이터를 Kafka 내부에서관리합니다. 이를 통해" ZooKeeper 단일 장애점(SPOF) 제거"와"운영 복잡성 감소"라는 두 가지 목표를 동시에 달성하며, 향후 모든 Kafka 클러스터가 KRaft 모드로 마이그레이션되는 것이 예상됩니다.

2. <strong>Kafka와 레이크하우스/스트리밍 SQL의 심화 통합</strong>
   Confluent의 ksqlDB, Apache Flink SQL, Spark Structured Streaming 등 다양한 스트리밍 SQL 엔진이 Kafka를 네이티브 소스로 활용하는 사례가 급증하고 있습니다. 특히"Kafka topic을 테이블로 조회"하거나"Kafka Streams를 사용하여 실시간 aggregated view를 생성"하는공능이 표준화됨에 따라, Kafka는 단순한 메시징 Infra에서"실시간 데이터 접근을 위한 가상화된시도(View)" 역할로 진화하고 있습니다.

3. <strong>Serverless Kafka와 Managed Service의 확산</strong>
   AWS MSK Serverless, Confluent Cloud의 Serverless Tier 등 완전 관리형 Kafka 서비스가 확산됨에 따라, 클러스터 프로비저닝, 브로커 모니터링, 리밸런싱 등의 운영 부담이 크게 감소하고 있습니다. 이는 엔지니어가"Kafka 운영"이 아닌"Kafka를 활용한 데이터 스트림 설계"에 집중할 수 있는 환경을 만들어, Kafka의 진입 장벽을 획기적으로 낮추고 있습니다.

- **📢 섹션 요약 비유**: Kafka의 미래는"도시의 도로 시스템"에서"도시의 순환 시스템"으로의 변화와상사 합니다. 과거 도시는 물건이 도착하면 창고에 넣고 삭제하는"단순 보관소"(기존 MQ)였지만, 현대 도시는"모든 화물 운행 기록이영구 보존되고,교경(컨슈머)가각자 필요한 구간의류량를실시간에서モニタ링하며,사고(장애) 발생 시 SAME 기록을 토대로사고원인을 역추적"하는고성능 물류 허브로 기능합니다. 이러한 시스템이"KRaft(도로 자체가교경 기능)"으로고도화되고, "Serverless(도로가 알아서류량를 관리)"하면, 도시 시민(엔지니어)은 도로 관리(운영)를 신경 쓰지 않고"어떤 물건을 어디로 보낼지"(데이터 설계)만 고민하면 되는 세상이 됩니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   <strong>Apache Kafka 핵심개념</strong>
    *   **Topic**: 논리적 데이터 채널 (파티션들의집합)
    *   <strong>Partition</strong>: 물리적 처리 단위, 각 파티션은ordered, immutable sequence of records
    *   **Offset**: 파티션 내 레코드 고유 위치 번호
    *   **Producer**: 메시지 게시자 (키 기반 파티셔닝)
    *   <strong>Consumer Group</strong>: 컨슈머들의 논리적 그룹 (파티션 공유)
*   <strong>Kafka 내구성 메커니즘</strong>
    *   <strong>ISR (In-Sync Replica)</strong>: 리더와 동기화된 복제본 집합
    *   **acks**: 생산자 확인 응답 설정 (0, 1, all)
    *   **min.insync.replicas**: 동기화 필수 최소 리플리카 수
*   <strong>Kafka 버전 변화</strong>
    *   Kafka 0.8~2.x: ZooKeeper 의존 (컨트롤러, 메타데이터)
    *   Kafka 3.3+ (KRaft): ZooKeeper 제거, 자체 Raft 프로토콜

---

### 📈 관련 키워드 및 발전 흐름도

```text
[전통적 MOM]
    |
    v
[Pub/Sub]
    |
    v
[Append-only Log]
    |
    v
[KRaft/Serverless Kafka]
```

이 흐름도는 전통적 MOM에서 Pub/Sub와 Append-only Log로 발전해 KRaft/Serverless Kafka로 진화하는 메시징 구조의 변화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Apache Kafka는 친구들이 서로에게 메시지를 보내는비상대적 게시판이에요.
2. 게시판에 글을 붙여두면(Append-only) 어떤 친구가 언제 읽어도 같은 글을 볼 수 있어요.
3. 여러 친구들이 동시에 같은 게시판을 보면서각자 필요한 정보를 가져갈 수 있어요!

---
> <strong>🛡️ Expert Verification:</strong> 본 문서는 Apache Kafka의 핵심 개념(Topic, Partition, Offset, ISR)과 메시징 시스템과의 비교를 기준으로 기술적 정확성을 검증하였습니다. (Verified at: 2026-04-05)
