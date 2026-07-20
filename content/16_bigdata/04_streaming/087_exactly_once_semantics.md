---
title: "Exactly Once Semantics"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 87
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Exactly-Once Semantics (정확히 한 번 의미론)은 시스템 장애가 발생해도 각 이벤트가 <strong>정확히 한 번만 처리되어 결과에 반영</strong>되는 것을 보장하며, 내부적으로는 분산 스냅샷(Chandy-Lamport) + 2단계 커밋(2PC, 2-Phase Commit) + 멱등적(Idempotent) Sink의 조합으로 달성한다.
- **가치**: 금융 거래, 재고 차감, 과금(Billing) 시스템에서 중복 처리(At-Least-Once)는 이중 청구·이중 배송을 유발하고, 누락 처리(At-Most-Once)는 데이터 손실을 유발하므로 정확히 한 번 보장이 비즈니스 정합성의 기반이다.
- **판단 포인트**: Exactly-Once는 세 보장 수준 중 가장 비용이 높다(체크포인트 + 2PC 오버헤드). 모든 파이프라인에 적용하면 처리량이 줄어들므로 <strong>비즈니스 영향도</strong>가 높은 파이프라인(결제, 재고)에만 선택적으로 적용하는 것이 최적이다.

---

## Ⅰ. 개요 및 필요성

### 1. 세 가지 처리 보장 수준

| 보장 수준 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| At-Most-Once (최대 한 번) | 처리 확인 없이 전송 -> 유실 가능 | 가장 빠름, 최저 오버헤드 | 데이터 손실 가능 |
| At-Least-Once (최소 한 번) | 장애 시 재전송 -> 중복 가능 | 빠름, 유실 없음 | 중복 처리 가능 |
| Exactly-Once (정확히 한 번) | 중복도 없고 유실도 없음 | 완전한 정합성 | 가장 느림, 복잡함 |

### 2. 왜 Exactly-Once가 어려운가

분산 시스템에서 Exactly-Once는 근본적으로 어렵다. 메시지가 전송되었는지, 수신되었는지, 처리되었는지, 결과가 저장되었는지를 분산된 노드들이 일관성 있게 합의해야 하기 때문이다.

```
[장애 발생 시나리오]

Source -> Process -> Sink

Sink에 쓰는 도중 프로세스가 죽으면:
  - 결과가 Sink에 절반 쓰였나? 안 쓰였나?
  - Source의 오프셋을 커밋했나? 안 했나?

-> 재시작 시 어디서부터 다시 처리해야 할지 불명확!
```

**📢 섹션 요약 비유**
> Exactly-Once는 "ATM에서 돈을 뽑는 것"과 같다. 잔액 차감 후 현금 미출금(누락), 현금 출금 후 잔액 미차감(중복) — 둘 다 안 되며, 오류가 나도 정확히 한 번만 처리되어야 한다. 이를 분산 환경에서 구현하는 것이 핵심 과제다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Flink의 Exactly-Once: 체크포인트 + 2PC

```
[Flink Exactly-Once 동작 흐름]

1. 체크포인트 시작 (JobManager -> Barrier 삽입)
   Kafka Source ---- [Barrier N] ----> Process ---- [Barrier N] ----> Sink
                                                                    (Pre-commit)

2. 모든 연산자 Barrier 수신 -> 상태 스냅샷 저장
   Process: 현재 집계 상태 -> HDFS/S3 저장

3. Sink: Pre-commit (2PC Phase 1)
   Kafka Sink: Transaction 열기, 메시지 쓰기 (미완료 상태)
   Database Sink: Prepared Statement 실행

4. JobManager: 모든 확인 수신 -> Commit 신호 (2PC Phase 2)
   Kafka Sink: Transaction Commit <- Exactly-Once 완료
   Database Sink: COMMIT 실행

5. Source Offset Commit
   Kafka Source: 처리된 오프셋 커밋 (중복 방지)
```

### 2. 2단계 커밋(2PC) in Kafka

```java
// Kafka Sink Exactly-Once 설정
KafkaSink<String> sink = KafkaSink.<String>builder()
    .setBootstrapServers("kafka:9092")
    .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setTopic("output-topic")
        .setValueSerializationSchema(new SimpleStringSchema())
        .build())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)  // 핵심!
    .setTransactionalIdPrefix("flink-txn")
    .build();

// 체크포인트 활성화 (Exactly-Once의 전제)
env.enableCheckpointing(30_000);
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
```

### 3. 멱등적 Sink (Idempotent Sink)

2PC 없이도 <strong>멱등적(Idempotent) 쓰기</strong> — 같은 데이터를 여러 번 써도 결과가 같음 — 로 At-Least-Once + Idempotent = 사실상 Exactly-Once 효과를 낼 수 있다.

```
Idempotent Sink 예시:
  Elasticsearch: 고유 ID로 UPSERT -> 중복 써도 같은 결과
  HBase: Row Key 기반 PUT -> 같은 Row Key 중복 써도 덮어씀
  Parquet: 파티션 덮어쓰기 -> 동일 파티션 재처리 시 정확히 한 번과 동일

Non-Idempotent Sink:
  Kafka Topic 쓰기 -> 중복 메시지 발생 (2PC 필요)
  카운터 업데이트 -> INCREMENT 중복 시 값 증가
```

### 4. 보장 수준 비교

| 구현 방법 | 보장 수준 | 오버헤드 |
|:---|:---|:---|
| 체크포인트 없음 | At-Most-Once | 없음 |
| 체크포인트 + At-Least-Once 모드 | At-Least-Once | 낮음 |
| 체크포인트 + 2PC Sink | Exactly-Once | 중간 |
| 체크포인트 + Idempotent Sink | 사실상 Exactly-Once | 낮음 |

**📢 섹션 요약 비유**
> 2PC는 "계약서 작성 절차"와 같다. 1단계: 양쪽이 "서명할 준비 완료" 확인(Pre-commit), 2단계: 동시에 서명(Commit). 한 쪽이 중간에 쓰러지면 계약을 취소하고 다시 진행한다.

---

## Ⅲ. 비교 및 연결

### 1. Kafka Transactions와 Exactly-Once

Kafka 0.11+부터 트랜잭션 API를 지원하여 프로듀서 -> 토픽 쓰기의 Exactly-Once가 가능하다.

```
Kafka Transactions:
  ProducerID + Epoch: 장애 후 재시작 시 이전 트랜잭션 식별
  TransactionalId: 같은 논리적 프로듀서 식별
  Isolation Level: Consumer의 read_committed -> 커밋된 메시지만 읽음
```

### 2. Flink Kafka Exactly-Once End-to-End

```
Kafka Source (읽기 오프셋 관리)
  -> Flink 처리 (체크포인트 기반 상태 저장)
  -> Kafka Sink (Transaction 기반 쓰기)
  -> Consumer (read_committed isolation)

-> 전 구간 Exactly-Once 달성
```

**📢 섹션 요약 비유**
> Kafka Transaction은 "공증된 계약서"다. 내가 서명(메시지 전송)하고 공증(커밋)이 완료될 때까지 상대방(Consumer)은 계약 내용을 볼 수 없다. 공증 전에 내가 사고를 당해도(장애) 계약은 없던 일이 된다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Exactly-Once 적용 우선순위

| 파이프라인 유형 | Exactly-Once 필요 여부 | 이유 |
|:---|:---|:---|
| 결제/청구 시스템 | ✅ 필수 | 이중 청구 불가 |
| 재고 차감 | ✅ 필수 | 이중 차감 = 마이너스 재고 |
| 실시간 지표 대시보드 | △ 선택 | 약간의 오차 허용 가능 |
| 로그 집계 | ❌ At-Least-Once 충분 | 중복 로그 영향 미미 |
| 클릭스트림 분석 | △ 선택 | 비즈니스 중요도에 따라 |

### 2. 체크리스트

- [ ] `DeliveryGuarantee.EXACTLY_ONCE` 설정 + 체크포인트 활성화
- [ ] Kafka Consumer `isolation.level=read_committed` 설정
- [ ] TransactionalId 접두사 중복 없도록 설정 (다중 잡 운영 시)
- [ ] 2PC 트랜잭션 타임아웃 > 체크포인트 간격으로 설정
- [ ] Idempotent Sink 가능 여부 우선 검토 (2PC보다 오버헤드 낮음)

**📢 섹션 요약 비유**
> Exactly-Once 보장은 "수술실 체크리스트"와 같다. 모든 단계(체크포인트 + 2PC + 오프셋 커밋)가 정확히 완료되었는지 확인하고, 하나라도 실패하면 처음부터 다시 시작한다. 느리지만 안전하다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 데이터 무결성 보장 | 중복/누락 없는 스트리밍 결과 |
| 비즈니스 정합성 | 금융/재고 시스템 신뢰성 확보 |
| 감사 추적 | 정확한 이벤트 처리 이력 보장 |

### 2. 결론

Exactly-Once Semantics는 <strong>스트리밍 신뢰성의 최고 수준</strong>이다. 학습 정리에서는 세 보장 수준의 정의와 차이, Flink의 체크포인트 + 2PC 구현 메커니즘, Kafka 트랜잭션과의 연계, 그리고 비용-신뢰성 트레이드오프를 서술하는 것이 핵심이다. "모든 파이프라인에 Exactly-Once가 필요한 것은 아니다"라는 판단 기준도 함께 제시하면 완성도가 높아진다.

**📢 섹션 요약 비유**
> Exactly-Once는 "정밀 외과 수술"과 같다. 모든 상처를 완벽하게 봉합하지만 시간이 오래 걸린다. 모든 상처(파이프라인)에 정밀 수술이 필요한 것은 아니다. 작은 상처(로그 집계)는 반창고(At-Least-Once)로 충분하고, 심장 수술(결제 시스템)만 정밀 수술(Exactly-Once)이 필요하다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Checkpoint (Flink) | 구현 기반 | 상태 스냅샷으로 재시작 지점 보장 |
| 2PC (2-Phase Commit) | 구현 기법 | Sink 쓰기의 원자성 보장 |
| Kafka Transactions | 연동 기술 | End-to-End Exactly-Once의 Sink 구현 |
| Idempotent Sink | 대안 방식 | 2PC 없이 Exactly-Once 효과 |
| At-Least-Once | 하위 수준 | Exactly-Once의 비교 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[최대 1회 (At-Most-Once) — 손실 허용]
    |
    v
[최소 1회 (At-Least-Once) — 중복 허용]
    |
    v
[정확히 1회 (Exactly-Once Semantics) — 완전 보장]
    |
    v
[분산 트랜잭션 (Distributed Transaction) — 2PC 커밋]
    |
    v
[멱등 프로듀서 (Idempotent Producer) — 트랜잭션 API Kafka]
```

이 흐름은 손실을 허용하는 최대 1회와 중복을 허용하는 최소 1회 사이에서 출발해, 분산 트랜잭션과 멱등성으로 정확히 1회를 구현하는 발전을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

은행 ATM에서 돈을 뽑을 때 "계좌에서 돈이 나가는 것"과 "현금이 나오는 것"이 동시에 정확히 한 번만 일어나야 해요. 정전이 나서 현금이 안 나왔는데 잔액만 줄었다면(At-Least-Once 실패), 아니면 현금은 나왔는데 잔액이 안 줄었다면(중복 처리) 모두 큰일이죠! Exactly-Once는 "ATM이 어떤 상황에서도 딱 한 번만 거래가 일어나도록 보장"하는 것이에요.
