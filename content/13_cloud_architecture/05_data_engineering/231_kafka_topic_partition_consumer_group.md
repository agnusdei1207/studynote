---
title: "Kafka Topic Partition Consumer Group"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 231
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 카프카의 Topic(논리 채널)·Partition(물리 분할)·Consumer Group(병렬 소비)은 <strong>처리량 확장과 메시지 순서 보장을 동시에 달성</strong>하기 위한 3-Layer 설계다.
> 2. **가치**: 파티션 수만큼 병렬 처리 수준이 결정되고, 컨슈머 그룹 내 각 컨슈머가 전담 파티션을 가져가므로 <strong>소비자 수를 늘리기만 해도 처리량이 선형 확장</strong>된다.
> 3. **판단 포인트**: 파티션 내 메시지 순서만 보장되므로, 동일 고객 ID의 이벤트를 순서대로 처리하려면 <strong>고객 ID를 파티션 키로 설정</strong>해야 같은 파티션으로 라우팅된다.

---

## Ⅰ. 개요 및 필요성

카프카의 확장성과 순서 보장은 Topic-Partition-Consumer Group 3계층 구조로 실현된다. 이 구조를 이해하지 못하면 핫스팟(특정 파티션에만 메시지 집중), 순서 보장 실패, 소비자 리밸런싱 폭풍 등 실무 장애를 만나게 된다.

```
[3계층 구조]
Topic (논리 채널: "user-orders")
+-- Partition 0  [msg0][msg1][msg2][msg3]... (파티션 내 순서 보장)
+-- Partition 1  [msg0][msg1][msg2]...
+-- Partition 2  [msg0][msg1][msg2][msg3][msg4]...

Consumer Group "order-processor"
+-- Consumer A  ---> Partition 0 (전담)
+-- Consumer B  ---> Partition 1 (전담)
+-- Consumer C  ---> Partition 2 (전담)

Consumer Group "analytics"
+-- Consumer X  ---> Partition 0 + Partition 1 (2개 담당)
+-- Consumer Y  ---> Partition 2 (1개 담당)
```

**핵심 설계 원칙**: 컨슈머 그룹은 독립적이므로, 동일 토픽을 "order-processor" 그룹과 "analytics" 그룹이 완전히 별도로 소비할 수 있다. 한 그룹의 소비가 다른 그룹에 영향을 주지 않는다.

📢 **섹션 요약 비유**: Topic은 신문, Partition은 신문의 섹션(정치·경제·스포츠), Consumer Group은 독자 그룹이다. 각 독자 그룹은 서로 다른 목적으로 같은 신문을 읽고, 각 섹션은 담당 독자가 읽는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 파티션 키와 라우팅 전략

```
[파티션 키 기반 라우팅]
Producer가 메시지 발행 시:
  파티션 번호 = hash(partition_key) % 파티션 수

예시:
  customer_id = "C001" -> hash("C001") % 3 = 0 -> Partition 0
  customer_id = "C002" -> hash("C002") % 3 = 1 -> Partition 1
  customer_id = "C001" -> hash("C001") % 3 = 0 -> Partition 0 (항상 같은 파티션)

효과: 동일 customer_id의 이벤트는 항상 같은 파티션 -> 순서 보장
```

### 오프셋 관리

```
[오프셋(Offset) 구조]
Partition 0:
메시지: [주문생성][결제시작][결제완료][배송시작][배송완료]
오프셋:    0        1        2         3        4

Consumer A 현재 오프셋: 3 (배송시작까지 처리 완료)

처리 방식:
  auto.commit: 주기적 자동 커밋 (중복 처리 가능성)
  manual commit: 처리 성공 후 명시적 커밋 (At-Least-Once 보장)
  Exactly-Once: 트랜잭션 + 멱등성 프로듀서 조합
```

### 컨슈머 그룹 리밸런싱

```
[리밸런싱 시나리오]
상황 1: Consumer C 추가
  이전: A->P0, B->P1, P2 미소비
  이후: A->P0, B->P1, C->P2  <- 리밸런싱 발생

상황 2: Consumer B 장애
  이전: A->P0, B->P1(장애!), C->P2
  이후: A->P0+P1, C->P2  <- 리밸런싱 발생
  (B의 마지막 오프셋 이후부터 A가 이어받음)

리밸런싱 중: 파티션 재할당 동안 소비 일시 중단
```

| 리밸런싱 프로토콜 | 설명 | 특성 |
|:---|:---|:---|
| **Eager Rebalance** | 모든 파티션 해제 후 재할당 | 단순하지만 처리 중단 시간 김 |
| **Cooperative (Incremental) Rebalance** | 필요한 파티션만 재할당 | 중단 시간 최소화, Kafka 2.4+ |

📢 **섹션 요약 비유**: 리밸런싱은 계산대(파티션) 재배정이다. 계산원(컨슈머) 한 명이 퇴근하면 남은 계산원들이 담당 계산대를 나눠 맡는 과정이다. 이 과정에서 잠시 계산이 멈추는(처리 중단) 불편이 있다.

---

## Ⅲ. 비교 및 연결

### 파티션 수 설계 기준

| 고려사항 | 권장 값 | 이유 |
|:---|:---|:---|
| <strong>목표 처리량</strong> | 파티션 수 ≥ 목표 TPS / 파티션당 최대 TPS | 처리량 확보 |
| **컨슈머 최대 수** | 파티션 수 = 최대 컨슈머 수 | 모든 컨슈머 활용 |
| **리텐션 크기** | 파티션 수 × 예상 크기 ≤ 브로커 디스크 | 스토리지 관리 |
| <strong>리더 분산</strong> | 파티션 수 = 브로커 수의 배수 | 리더 균등 분배 |
| **실무 권장** | 시작: 6~12개, 나중에 증가 | 나중에 줄이기 불가 |

### 컨슈머 그룹 vs 단일 소비자 패턴

| 패턴 | 설명 | 사용 사례 |
|:---|:---|:---|
| **단일 소비자** | 모든 파티션 읽기, 순서 보장 | 로그 집계, 감사 |
| <strong>컨슈머 그룹</strong> | 파티션 분산 소비, 병렬 처리 | 이벤트 처리, ETL |
| **다중 그룹** | 동일 토픽 여러 팀 독립 소비 | 분석+처리 동시 |
| <strong>KStream (Kafka Streams)</strong> | DStream 내부 처리 | 단순 스트림 변환 |

📢 **섹션 요약 비유**: 파티션 수와 컨슈머 수의 관계는 고속도로 차선과 차량의 관계다. 차선(파티션)이 6개인데 차(컨슈머)가 3대면 3개 차선이 비어 낭비되고, 차가 10대면 4대는 차선이 없어 대기해야 한다. 차선수 = 최대 차량 수가 이상적이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 파티션 키 설계 전략

```
[좋은 파티션 키 설계]
✅ 높은 카디널리티 (customer_id, session_id)
   -> 파티션 균등 분포, 핫스팟 방지

✅ 비즈니스 순서 요건에 맞는 키
   -> 동일 고객 이벤트 순서 보장 필요 -> customer_id
   -> 동일 주문 이벤트 순서 보장 필요 -> order_id

❌ 낮은 카디널리티 키
   -> 날짜(YYYY-MM-DD) -> 하루치 이벤트 모두 같은 파티션 -> 핫스팟
   -> 성별(M/F) -> 파티션 2개에 모든 트래픽 집중

[핫스팟 해결 방법]
핵심 키 + 랜덤 접미사: customer_id + "-" + random(0,5)
-> 순서 보장 희생, 분산 극대화
```

### 실무 Consumer 구현 예시

```python
from confluent_kafka import Consumer, TopicPartition, KafkaError

consumer = Consumer({
    'bootstrap.servers': 'broker1:9092,broker2:9092',
    'group.id': 'order-processor',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # 수동 커밋으로 At-Least-Once 보장
})
consumer.subscribe(['user-orders'])

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        raise KafkaException(msg.error())

    # 처리 로직
    process_order(msg.value())

    # 처리 성공 후 커밋
    consumer.commit(asynchronous=False)
```

📢 **섹션 요약 비유**: 수동 커밋(enable.auto.commit=False)은 영수증에 서명하는 것과 같다. 물건을 받고 나서 서명해야 거래가 완료된다. 자동 커밋은 물건을 받기도 전에 서명하는 것이라 물건이 분실되면(처리 실패) 증거가 없다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **선형 확장** | 파티션 수 증가 -> 컨슈머 수 증가 -> 처리량 선형 확장 |
| **순서 보장** | 파티션 키 기반 라우팅으로 동일 개체 이벤트 순서 보장 |
| <strong>장애 복구</strong> | 오프셋 기반 재처리로 장애 후 데이터 손실 없이 재개 |
| **멀티 소비** | 동일 토픽을 여러 컨슈머 그룹이 독립 소비 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| <strong>파티션 수 증가만 가능</strong> | 파티션 줄이기 불가 (처음부터 충분히 설계) |
| **리밸런싱 중단** | 컨슈머 변경 시 일시적 처리 중단 |
| **핫스팟 위험** | 파티션 키 카디널리티 낮으면 특정 파티션에 편중 |
| <strong>파티션 간 순서 미보장</strong> | 전체 토픽 순서 보장은 파티션 1개로만 가능 (처리량 희생) |

📢 **섹션 요약 비유**: 파티션 수를 늘리는 것은 도로 확장 공사와 같다. 차선을 늘리면(파티션 증가) 더 많은 차(메시지)가 동시에 달릴 수 있지만, 차선을 줄이는 공사(파티션 감소)는 불가능하고 공사 중(리밸런싱)에는 잠깐 교통이 막힌다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| Apache Kafka | 토픽·파티션·컨슈머 그룹이 구현되는 시스템 |
| 오프셋 (Offset) | 파티션 내 소비 위치 추적, 재처리의 핵심 |
| 스키마 레지스트리 | 토픽 메시지의 스키마 버전 관리 (Confluent) |
| CDC / Debezium | 파티션 키로 테이블 PK 사용, 순서 보장 |
| 컨슈머 그룹 코디네이터 | 리밸런싱 조정 역할 (Kafka Broker 내) |
| KRaft | ZooKeeper 없이 Kafka 자체 메타데이터 관리 (Kafka 3.x+) |
| 스트림 처리 (Flink) | Kafka 파티션을 소스로 병렬 처리 |

### 👶 어린이를 위한 3줄 비유 설명
1. 토픽은 택배 분류 벨트, 파티션은 벨트를 여러 줄로 나눈 것이다. 여러 줄(파티션)에서 여러 분류원(컨슈머)이 동시에 택배를 분류하면 훨씬 빠르다.

### 📈 관련 키워드 및 발전 흐름도

```text
Topic: 메시지 카테고리 (주문 · 결제 · 로그)
    |
    v
Partition: 수평 분할 -> 병렬 소비
    +-► Key 기반 라우팅: 같은 키 -> 같은 파티션
    +-► Consumer Group: 파티션 : 컨슈머 = 1:1 매핑
    |
    v
Rebalancing · Sticky Assignor -> 안정적 파티션 할당
```
2. 컨슈머 그룹은 택배 회사와 같다. CJ택배(그룹 A)와 한진택배(그룹 B)가 동시에 같은 벨트에서 각자 자기 택배만 가져간다. 두 회사가 서로 방해하지 않는다.
3. 오프셋은 택배 추적 번호다. "나는 100번 택배까지 받았어요"라고 표시해두면, 다음에 다시 시작할 때 101번부터 받을 수 있고, 틀렸다면 95번으로 돌아가 다시 받을 수 있다.
