---
title: "Apache Pulsar"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 94
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Apache Pulsar (아파치 펄사)는 메시지 라우팅을 담당하는 브로커(Broker)와 데이터 저장을 담당하는 북키퍼(BookKeeper)를 물리적으로 분리하는 계층화 아키텍처를 채택하여, 브로커와 스토리지를 독립적으로 확장하고 토픽을 중단 없이 다른 브로커로 이동할 수 있다.
- **가치**: Kafka는 파티션이 특정 브로커에 고정되어 있어 브로커 장애 시 해당 파티션의 리밸런싱 지연이 발생하지만, Pulsar는 스토리지가 브로커와 분리되어 있어 브로커 장애 시 즉각적인 토픽 이전(Topic Ownership Transfer)이 가능하고 스케일 인/아웃이 유연하다.
- **판단 포인트**: Pulsar는 멀티 테넌시(Multi-Tenancy), 지역 복제(Geo-Replication), 계층형 스토리지(Tiered Storage)가 기본 내장되어 대형 클라우드 서비스 제공자에게 유리하지만, 운영 복잡도(브로커 + BookKeeper + ZooKeeper 3계층 관리)가 Kafka보다 높다.

---

## Ⅰ. 개요 및 필요성

### 1. Kafka의 구조적 한계

Kafka는 파티션이 특정 브로커에 고정(Coupled)되어 있다.

```
Kafka 문제:
  Broker 1: Partition 0, 1 (Leader)
  Broker 2: Partition 2 (Leader) <- 이 브로커 장애 발생!

  -> Partition 2의 팔로워가 리더가 될 때까지 일시 불가용
  -> 새 브로커 추가 시 파티션 재배치 필요 (시간 소요)
  -> 클러스터 규모 커질수록 리밸런싱 비용 증가
```

### 2. Pulsar의 분리 아키텍처

```
Pulsar 해결책:
  Broker: 라우팅·서빙 담당 (상태 없음, Stateless)
  BookKeeper: 실제 데이터 저장 (상태 있음, Stateful)

  Broker 2 장애 시:
  -> 해당 토픽의 소유권(Ownership)만 다른 Broker로 즉시 이전
  -> 데이터는 BookKeeper에 그대로 있어 손실 없음
  -> 리밸런싱 수 초 내 완료
```

**📢 섹션 요약 비유**
> Kafka는 "창고(스토리지)를 가진 배달부(브로커)"이고, Pulsar는 "창고(BookKeeper)는 창고업체에 맡기고 배달만 하는 배달부(브로커)"이다. 배달부가 교체되도 창고는 그대로라 물건을 다시 찾을 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Pulsar 아키텍처 다이어그램

```
+--------------------------------------------------------------+
|  Apache Pulsar 클러스터                                       |
|                                                              |
|  +-----------------------------------------------------+    |
|  |  서빙 계층 (Brokers) — Stateless                     |    |
|  |  Broker 1   Broker 2   Broker 3                      |    |
|  |  (토픽 소유권 관리, 프로토콜 처리)                     |    |
|  +----------------------+------------------------------+    |
|                         | 읽기/쓰기 (Ledger)                 |
|  +----------------------v------------------------------+    |
|  |  스토리지 계층 (Apache BookKeeper) — Stateful         |    |
|  |  Bookie 1   Bookie 2   Bookie 3                      |    |
|  |  (데이터 영구 저장, Ledger 기반)                       |    |
|  +----------------------+------------------------------+    |
|                         |                                    |
|  +----------------------v------------------------------+    |
|  |  계층형 스토리지 (Tiered Storage) — 선택적            |    |
|  |  S3 / GCS / ADLS (콜드 데이터 자동 이전)              |    |
|  +-----------------------------------------------------+    |
|                                                              |
|  메타데이터: ZooKeeper (또는 Oxia, BookKeeper Metadata)       |
+--------------------------------------------------------------+
```

### 2. Pulsar의 핵심 기능

| 기능 | 설명 | Kafka 비교 |
|:---|:---|:---|
| Multi-Tenancy | 테넌트/네임스페이스 계층 구조로 완전 격리 | 토픽 명명 규칙으로만 구분 |
| Geo-Replication | 클러스터 간 비동기 복제 내장 | MirrorMaker 2 별도 필요 |
| Tiered Storage | 오래된 데이터를 S3/GCS로 자동 이전 | Confluent Tiered Storage (유료) |
| Pulsar Functions | 경량 스트림 처리 함수 내장 | Kafka Streams 별도 라이브러리 |
| 구독 유형 | Exclusive/Shared/Failover/Key-Shared | 컨슈머 그룹으로만 구분 |

### 3. 구독 유형(Subscription Types)

```
Exclusive:   하나의 Consumer만 구독 (순서 보장 강력)
Shared:      여러 Consumer에 메시지 분배 (병렬 처리, 순서 불보장)
Failover:    하나가 Active, 나머지 Standby (HA)
Key-Shared:  같은 키는 같은 Consumer로 (순서 보장 + 병렬)
```

**📢 섹션 요약 비유**
> Pulsar의 멀티 테넌시는 "오피스 빌딩 임대 구조"와 같다. 한 빌딩(클러스터)에 여러 회사(테넌트)가 입주하되, 각 회사의 사무실(네임스페이스)은 완전히 격리된다. 복도(브로커)는 공유하지만 내부는 독립적이다.

---

## Ⅲ. 비교 및 연결

### 1. Pulsar vs Kafka 심층 비교

| 비교 항목 | Apache Kafka | Apache Pulsar |
|:---|:---|:---|
| 아키텍처 | 모놀리식 (브로커 = 스토리지) | 분리 아키텍처 (Broker + BookKeeper) |
| 스케일링 | 브로커 단위 (파티션 재배치 필요) | 브로커/스토리지 독립 스케일링 |
| 멀티 테넌시 | 제한적 (토픽 명명 규칙) | 네이티브 (Tenant/NS/Topic) |
| Geo-Replication | MirrorMaker 2 필요 | 내장 |
| 운영 복잡도 | 중간 (단일 계층) | 높음 (3계층: Broker/BK/ZK) |
| 생태계 | 성숙 (Confluent 등) | 성장 중 (StreamNative 등) |
| 메시지 보존 | 토픽 단위 설정 | Ledger 단위, Tiered Storage |

### 2. 연결 개념

- **BookKeeper**: Pulsar의 스토리지 엔진, Ledger 기반 순서화된 로그
- **Pulsar Functions**: Java/Python/Go로 작성하는 경량 스트림 처리 로직
- **Pulsar IO**: Source/Sink 커넥터 프레임워크 (Kafka Connect 유사)

**📢 섹션 요약 비유**
> Kafka vs Pulsar는 "아파트(Kafka: 집과 창고 일체형) vs 주상복합(Pulsar: 주거와 창고 분리)"와 같다. 아파트가 더 단순하지만, 주상복합은 창고를 독립적으로 확장하거나 교체할 수 있다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. Pulsar 선택 적합 시나리오

| 시나리오 | Pulsar 선택 이유 |
|:---|:---|
| 대규모 SaaS 플랫폼 (멀티 테넌트) | 기본 내장 테넌트 격리 |
| 글로벌 서비스 (지역 복제 필수) | Geo-Replication 내장 |
| 무제한 보존 필요 (비용 최적화) | Tiered Storage로 콜드 데이터 -> S3 이전 |
| 브로커 확장 빈번 | 스토리지와 독립 스케일링 가능 |

### 2. Pulsar vs Kafka 선택 기준

| 선택 기준 | Kafka | Pulsar |
|:---|:---|:---|
| 운영 팀 경험 | 풍부한 Kafka 경험 있을 때 | 새로운 아키텍처 도입 가능 시 |
| 요구 기능 | 단순 메시지 큐 + 스트리밍 | 멀티 테넌시 + Geo-DR + Tiered Storage |
| 생태계 | 성숙한 Confluent/MSK | 성장 중, StreamNative 지원 |
| 벤더 지원 | Confluent, Cloudera | StreamNative |

### 3. 체크리스트

- [ ] BookKeeper 앙상블 크기: 최소 3 Bookie (쿼럼 2)
- [ ] ZooKeeper 또는 Oxia 메타데이터 스토어 HA 구성
- [ ] Broker 메모리: Managed Ledger Cache 최적화
- [ ] Tiered Storage: 데이터 보존 정책과 비용 계획 수립

**📢 섹션 요약 비유**
> Pulsar 운영은 "세 팀이 협업하는 복합 물류센터 관리"와 같다. 배달팀(Broker), 창고팀(BookKeeper), 관리팀(ZooKeeper)이 각자 역할을 하는데, 한 팀이 없으면 전체 운영이 어렵다. 각 팀의 HA를 별도로 보장해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 즉각적 장애 복구 | 브로커 장애 시 수 초 내 토픽 이전 |
| 독립적 확장 | 처리량 증가 시 브로커만, 스토리지 증가 시 BookKeeper만 추가 |
| 비용 최적화 | Tiered Storage로 콜드 데이터 저렴한 오브젝트 스토리지 이전 |
| 멀티 테넌트 | 단일 클러스터에서 다수 팀/서비스 격리 운영 |

### 2. 결론

Apache Pulsar는 <strong>대규모 멀티 테넌트 및 글로벌 분산 스트리밍에 최적화된 차세대 메시징 플랫폼</strong>이다. 학습 정리에서는 Kafka와의 구조적 차이(컴퓨팅/스토리지 분리), 멀티 테넌시·Geo-Replication·Tiered Storage의 기본 내장 가치, 그리고 높은 운영 복잡도를 균형 있게 서술해야 한다.

**📢 섹션 요약 비유**
> Pulsar는 "Kafka의 진화형 후계자"를 자처하지만, "더 강력한 무기를 다루려면 더 많은 훈련이 필요하다"는 트레이드오프가 있다. 운영 역량이 충분하고 멀티 테넌시/Geo-DR이 진짜 필요한 환경이라면 Pulsar가 Kafka보다 우위에 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Apache Kafka | 비교/경쟁 | 기존 표준, Pulsar가 해결하려는 한계 |
| Apache BookKeeper | 스토리지 엔진 | Pulsar의 데이터 저장 계층 |
| Pulsar Functions | 내장 기능 | 경량 스트리밍 로직 실행 |
| Tiered Storage | 비용 최적화 | 오래된 데이터 -> 저렴한 오브젝트 스토리지 |
| Geo-Replication | DR 기능 | 클러스터 간 자동 복제 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 메시지 큐 (ActiveMQ·RabbitMQ) — 단일 브로커, 스케일 한계]
    |
    v
[Apache Kafka — 분산 로그, 높은 처리량의 스트리밍 표준]
    |
    v
[Apache Pulsar — 브로커·저장소 분리(BookKeeper), 지역 복제 내장]
    |
    v
[Pulsar Functions — 경량 스트림 처리 컴퓨팅을 브로커 내 통합]
    |
    v
[클라우드 네이티브 스트리밍 — 서버리스 이벤트 허브로 진화]
```
Apache Pulsar는 Kafka의 처리량과 전통 MQ의 유연성을 결합하고, 저장소 계층 분리와 지역 복제를 기본 내장해 멀티테넌트 클라우드 메시징 플랫폼으로 자리잡았다.

### 👶 어린이를 위한 3줄 비유 설명

Kafka는 "배달부(브로커)가 직접 창고도 가진 구조"이고, Pulsar는 "배달부(브로커)와 창고업체(BookKeeper)가 분리된 구조"예요. 배달부가 아파도(브로커 장애) 창고는 멀쩡하니까 다른 배달부가 즉시 가서 물건을 가져올 수 있어요. 창고를 더 늘리고 싶으면 창고만(BookKeeper) 추가하고, 배달부를 더 늘리고 싶으면 배달부만 추가하면 되니까 각각 독립적으로 키울 수 있어요!
