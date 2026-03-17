+++
title = "790. 이벤트 버스 카프카(Kafka) 비동기 내결함성 설계"
date = "2026-03-15"
weight = 790
[extra]
categories = ["Software Engineering"]
tags = ["Architecture", "Event Bus", "Kafka", "Asynchronous", "Fault Tolerance", "EDA", "Scalability"]
+++

# 790. 이벤트 버스 카프카(Kafka) 비동기 내결함성 설계

## # [주제명] 이벤트 버스 카프카 비동기 내결함성 설계

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **MSA (Microservice Architecture)** 환경에서 서비스 간 강결합(Coupling)을 제거하고, **EDA (Event-Driven Architecture)**의 척추 역할을 하며 대용량 이벤트를 실시간으로 처리하는 **분산 스트리밍 플랫폼(Distributed Streaming Platform)**입니다.
> 2. **기술적 우위**: **디스크 기반 순차 로그(Sequential Log)** 저장 방식과 **Zero Copy** 기술을 통해 휘발성 MQ 대비 수백 배의 처리량(TPS)을 보장하며, **Replication(복제)** 메커니즘을 통해 데이터 무손실 내결함성을 제공합니다.
> 3. **가치**: '느슨한 결합(Loose Coupling)'과 '높은 응집도'를 통해 시스템의 유지보수성을 극대화하고, **트랜잭션 아웃박스(Transactional Outbox)** 패턴 등과 결합하여 데이터 정합성을 준수하는 분산 트랜잭션 환경을 구축합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**이벤트 버스(Event Bus)**는 마이크로서비스 간의 통신을 중계하는 중간 계층으로, 발행자(Publisher)가 특정 구독자(Subscriber)를 알지 못해도 메시지(이벤트)를 전송할 수 있는 **비동기 메시징 패턴(Asynchronous Messaging Pattern)**의 물리적 구현체입니다. 아파치 카프카(Apache Kafka)는 이 이벤트 버스의 사실상 표준(De Facto Standard)으로, 단순한 메시지 큐를 넘어 **이벤트 저장소(Event Store)**의 역할을 수행합니다.

#### 2. 배경 및 필요성
① **동기 통신(Synchronous Communication)의 한계**: 기존 **REST API**나 **RPC (Remote Procedure Call)** 방식은 호출 대상 서비스가 정상 작동해야만 요청이 완료되므로, 장애가 연쇄 전파되는 **누출(Latency)** 문제와 단일 장애점(SPOF) 이슈가 발생합니다.
② **이벤트 기반 아키텍처(EDA)의 부상**: 비즈니스 프로세스를 실시간 상태 변화(State Change)의 흐름으로 보는 패러다임이 전환되면서, 이를 효율적으로 처리할 고처리량(High Throughput) 파이프라인이 필수적으로 요구되었습니다.
③ **고가용성 및 내결함성 요구**: 서비스의 규모가 거대해짐에 따라, 특정 서비스의 일시적 장애가 전체 시스템의 데이터 유실로 이어지지 않도록 메시지를 안전하게 **버퍼링(Buffering)**하고 **재시도(Retry)**할 수 있는 매커니즘이 필요해졌습니다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                   [통신 패러다임의 진화]                                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [Phase 1: Monolith]               [Phase 2: Sync RPC]          [Phase 3: EDA]│
│  ┌──────────────┐                  ┌─────────┐                 ┌───────────┐ │
│  │   Function   │   Direct Call    │  Svc A  │    Event Pub    │  Producer │ │
│  │      A       ├─────────────────▶│         ├────────────────▶│           │ │
│  └──────────────┘                  └────┬────┘                 └─────┬─────┘ │
│                                        │                             │       │
│                                        │    Direct HTTP Call         │       │
│                                     ┌──▼──────┐                      │       │
│                                     │  Svc B  │◀─────────────────────┼───┐   │
│                                     └─────────┘   Async Pull/Push    │   │   │
│                                                            │       │   │   │
│                                                            ▼       ▼   ▼   │
│                                                       [   Kafka / Event Bus  ]│
│                                                       │         │           ││
│                                                    ┌──▼──┐   ┌──▼──┐      ││
│                                                    │Svc C│   │Svc D│      ││
│                                                    └─────┘   └─────┘      ││
└────────────────────────────────────────────────────────────────────────────┘
```
*도해 1: 통신 패턴의 진화. 블록(Block)이 발생하는 동기 방식에서 이벤트를 통해 완전히 분리되는 비동기 방식으로 변천.*

#### 3. 💡 비유
이벤트 버스는 거대한 물류 센터의 **'자동 분류 시스템이 장착된 컨테이너 터미널'**과 같습니다. 화물(이벤트)을 싣는 선박(생산자)은 하역 장소(소비자)가 구체적으로 어디인지 몰라도, 터미널(Kafka)에 화물만 내려놓으면 됩니다. 터미널은 화물을 안전하게 보관(Persistence)하다가, 트럭(소비자)이 준비되면 순서대로 적재해 줍니다.

#### 📢 섹션 요약 비유
**마치 우체국에 편지를 부치는 것과 같습니다.** 편지를 띄우는 사람(Producer)은 배달원(Consumer)이 당장 출근했는지, 아파서 병가인지 전혀 신경 쓰지 않고 우체통에 편지를 넣으면 됩니다. 우체국(Kafka)이 배달이 가능한 시점에 알아서 배달을 처리하니까요.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (상세 분석)

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 메커니즘 (Internal Mechanism) | 주요 프로토콜/특징 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Broker (브로커)** | 카프카 클러스터를 구성하는 개별 서버 | 메시지를 수신하고 디스크에 저장. Zookeeper/Controller와 메타데이터 동기화 | **TCP/IP**, KRaft Mode | 물류 센터의 창고 |
| **Topic (토픽)** | 메시지의 논리적 채널 (Stream) | 0개 이상의 파티션으로 나뉘며, 이름으로 식별됨 | Multi-subscriber | 택배 분류별 '파란 박스' |
| **Partition (파티션)** | **병렬 처리의 핵심 물리 단위** | **Offset(순번)** 기반 순차 저장. 하나의 파티션은 하나의 브로커(Leader)가 관리 | **Append-Only Log** | 컨테이너 터미널의 '적재 선반' |
| **Producer (생산자)** | 이벤트를 생성하여 토픽으로 전송 | **Serializer**를 통해 직렬화하며, Key의 해시 값으로 파티션 지정 | **Batching**, Compression | 화물을 싣고 오는 선박 |
| **Consumer (소비자)** | 토픽의 파티션에서 메시지를 읽음 | **Consumer Group** 내에서 파티션을 분배(Rebalancing). **Offset Commit**으로 진행도 관리 | **Pull-based** | 화물을 나르는 트럭 |
| **Replication (복제)** | 데이터 내결함성 제공 | ISR(In-Sync Replica) 목록을 관리하여 Leader 장애 시 Follower가 승계 | **ACKs(0,1,all)** | 보험용 사본 원본 |

#### 2. 카프카 내부 데이터 구조 및 흐름
카프카의 핵심은 메모리가 아닌 **디스크(Log Segment)**에 데이터를 쓰되, 순차 쓰기(Sequential Write)만 수행하여 **OS Page Cache**의 효율을 극대화하고 **Zero Copy**(sendfile 시스템 콜)를 통해 네트워크로 전송하는 것입니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [Kafka Topic Architecture]                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [ Producer Service ]                                                      │
│        │                                                                   │
│        │ 1. Serialize (Key: "OrderID", Value: Json)                         │
│        │ 2. Partitioner (Hash(Key) % Partition_Count)                       │
│        ▼                                                                   │
│   ┌─────────────────────────────────────────────────┐                      │
│   │              Topic: user-events                 │                      │
│   ├─────────────────┬─────────────────┬──────────────┤                      │
│   │   Partition 0   │   Partition 1   │ Partition 2  │  (Logical Stream)   │
│   │   [Leader: B1]  │   [Leader: B2]  │ [Leader: B3] │                      │
│   │   [Replica: B3] │   [Replica: B1] │ [Replica: B2]│  (High Availability)│
│   └────────┬────────┴────────┬────────┴──────┬───────┘                      │
│            │                 │               │                             │
│            │                 │               │                             │
│   ┌────────▼─────────┐ ┌────▼──────────┐ ┌──▼───────────┐                   │
│   │   Log Segment    │ │  Log Segment  │ │ Log Segment  │                   │
│   │ ┌─┬─┬─┬─┬─┬─┬─┬─┐ │ │ ┌─┬─┬─┬─┬─┬─┐ │ ┌─┬─┬─┬─┬─┬─┐ │                   │
│   │ │0│1│2│3│4│5│6│7│ │ │ │0│1│2│3│4│5│ │ │0│1│2│3│4│5│ │ (Physical Disk)   │
│   │ └─┴─┴─┴─┴─┴─┴─┴─┘ │ │ └─┴─┴─┴─┴─┴─┘ │ └─┴─┴─┴─┴─┴─┘ │                   │
│   │   ▲               │ │   ▲           │ │   ▲         │                   │
│   │   │ Offset        │ │   │ Offset    │ │   │ Offset   │                   │
│   └───┼───────────────┘ └───┼───────────┘ └───┼─────────┘                   │
│       │ Read                     │                  │                         │
│       ▼                          ▼                  ▼                         │
│   ┌─────────────┐           ┌──────────┐       ┌──────────┐                    │
│   │ Consumer G1 │           │Consumer G1│       │Consumer G2│                   │
│   │ (Member A)  │           │(Member B) │       │(Member C) │                   │
│   └─────────────┘           └──────────┘       └──────────┘                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
*도해 2: 토픽과 파티션의 물리적/논리적 구조. 메시지는 Key에 따라 특정 파티션에 순차적으로 적재되며, 복제본(Replica)은 다른 브로커에 저장됨.*

#### 3. 심층 동작 원리: 내결함성 (Fault Tolerance)
① **Producer Acknowledgment (ACK)**: 프로듀서는 `acks=all` (또는 `-1`) 설정을 통해 ISR(In-Sync Replicas)에 속한 모든 복제본이 메시지를 받았음을 확인받기 전까지 커밋을 완료하지 않습니다.
② **Consumer Offset Management**: 컨슈머는 메시지 처리를 완료한 후, Kafka의 내부 토픽(`__consumer_offsets`)에 자신의 Offset을 저장합니다. 장애 발생 시, 저장된 Offset 이후의 데이터부터 다시 읽어옴으로써 **Exactly-Once** 또는 **At-Least-Once** 처리를 보장합니다.
③ **Rebalancing (재균형)**: 컨슈머 그룹 내에 장애가 발생하거나 새로운 컨슈머가 추가되면, 파티션 소유권을 재분배하는 리더 컨슈머가 판타지아(Fantasy)라 불리는 리더 선출 과정을 통해 균형을 맞춥니다.

```java
// [Core Logic] Kafka Producer Configuration for High Reliability
Properties props = new Properties();
props.put("bootstrap.servers", "kafka-broker1:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

// CRITICAL: Fault Tolerance Settings
// acks=all : Ensure data is written to all ISR replicas
props.put("acks", "all"); 
// enable.idempotence=true : Ensure exactly-once delivery from producer side (prevent duplicates)
props.put("enable.idempotence", "true");
// retries=Integer.MAX_VALUE : Retry forever on transient network errors
props.put("retries", Integer.MAX_VALUE); 
// max.in.flight.requests.per.connection=5 : Allow pipelining while maintaining idempotence
props.put("max.in.flight.requests.per.connection", 5);

Producer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("orders", "order-123", "{\"amount\": 100}"));
```
*코드 스니펫: 내결함성을 극대화하는 프로듀서 설정 예시.*

#### 📢 섹션 요약 비유
**마치 '녹음기(Tape Recorder)'로 방송을 녹화하는 것과 같습니다.** 라디오 DJ(생산자)가 실시간으로 이야기를 하면, 녹음기(카프카)는 테이프(로그 세그먼트)에 순서대로 기록합니다. 청취자(소비자)는 도중에 라디오를 껐다가(장애) 다시 켜고, 이어폨 선을 뽑았던 구간(Offset)부터 다시 이어서 들을 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Apache Kafka vs RabbitMQ
이벤트 버스를 구현하기 위한 기술적 선택지에서 **Kafka(로그 중심)**와 **RabbitMQ(메시지 큐 중심)**는 가장 대표적인 비교 대상입니다.

| 비교 항목 (Criteria) | RabbitMQ (AMQP Protocol) | Apache Kafka (Log-Based) |
|:---|:---|:---|
| **데이터 모델** | **Smart Broker, Dumb Consumer** (브로커가 전송 관리) | **Dumb Broker, Smart Consumer** (브로커는 저장만, 컨슈머가 가져감) |
| **메시지 보관** | 전달 완료 시 즉시 삭제 (메모리/디스크) | **Retention Policy**에 따라 기간/용량 한도까지 영구 보관 |
| *