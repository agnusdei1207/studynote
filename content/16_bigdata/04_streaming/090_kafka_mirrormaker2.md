---
title: "Kafka Mirrormaker2"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 90
---
## 핵심 인사이트 (3줄 요약)

- **본질**: Kafka MirrorMaker 2 (MM2, 카프카 미러메이커 2)는 Apache Kafka 2.4+부터 도입된 Kafka Connect 기반의 클러스터 간 복제 도구로, 양방향(Bidirectional) 복제, 오프셋 변환(Offset Translation), 토픽 자동 생성을 지원하여 재해 복구(DR, Disaster Recovery)와 지리적 분산 배포의 표준 솔루션이다.
- **가치**: 레거시 MirrorMaker 1은 오프셋 동기화가 없어 장애 시 Consumer 위치를 잃었지만, MM2는 오프셋을 자동으로 변환·저장하여 DR 전환 후에도 Consumer가 처리 위치를 유지하고 메시지 재처리를 최소화한다.
- **판단 포인트**: MM2는 단순 복제가 아니라 "Active-Passive(단방향)"와 "Active-Active(양방향)"를 모두 지원하므로 DR 요구사항(RTO, RPO)과 지역별 독립 쓰기 필요 여부에 따라 토폴로지를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. 클러스터 간 복제가 필요한 이유

단일 Kafka 클러스터는 다음 시나리오에 취약하다.

| 시나리오 | 문제 | 해결책 |
|:---|:---|:---|
| 데이터센터 장애 | 단일 클러스터 = 단일 장애점 | DR 클러스터에 복제 |
| 지역별 서비스 확장 | 글로벌 Consumer의 높은 지연 | 지역 근접 클러스터 복제 |
| 클러스터 분리 운영 | 개발/스테이징/프로덕션 격리 | 환경 간 선택적 복제 |
| Kafka 버전 업그레이드 | 무중단 마이그레이션 필요 | 신구 버전 클러스터 병행 복제 |

### 2. MirrorMaker 1의 한계와 MM2의 등장

| 항목 | MirrorMaker 1 | MirrorMaker 2 |
|:---|:---|:---|
| 기반 | 단순 Consumer/Producer | Kafka Connect Framework |
| 오프셋 동기화 | ❌ 없음 | ✅ 자동 변환 및 동기화 |
| 양방향 복제 | ❌ 불가 | ✅ Active-Active 지원 |
| 토픽 자동 생성 | ❌ 수동 | ✅ 자동 |
| 모니터링 | 제한적 | Kafka Connect 메트릭 활용 |

**📢 섹션 요약 비유**
> MM1은 "편지를 사람이 직접 복사해서 보내는 것"이고, MM2는 "자동 팩스 시스템"이다. MM2는 복사본에 원본 번호 매핑(오프셋 변환)까지 자동으로 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. MM2 아키텍처 구성

```
[Active-Passive DR 구성]

Primary Cluster (US-East)              Secondary Cluster (US-West, DR)
+--------------------------+           +--------------------------+
|  Topic: orders           |           |  Topic: us-east.orders   |
|  Partition 0: msg1..1000 |  MM2 복제 |  Partition 0: msg1..1000 |
|  Partition 1: msg2..800  | ---------->|  Partition 1: msg2..800  |
|  Consumer offset: 950    |           |  Consumer offset: 950    |
|                          |           |  (오프셋 변환 자동 저장)  |
+--------------------------+           +--------------------------+

[Active-Active 양방향 구성]
US-East <--------------------> US-East.us-west.events (접두사 자동 추가)
US-West <--------------------> US-West.us-east.events (무한 루프 방지)
```

### 2. MM2 설정 예시

```properties
# MirrorMaker 2 설정 (mm2.properties)
clusters = primary, secondary

# 클러스터 접속 정보
primary.bootstrap.servers = primary-kafka:9092
secondary.bootstrap.servers = secondary-kafka:9092

# 복제 방향: primary -> secondary
primary->secondary.enabled = true
primary->secondary.topics = orders, transactions, events.*  # 복제할 토픽 패턴

# 토픽 자동 생성 활성화
sync.topic.configs.enabled = true
sync.topic.acls.enabled = true

# 복제 인자
replication.factor = 3

# 오프셋 동기화 주기
offset-syncs.topic.replication.factor = 3
```

### 3. 오프셋 변환(Offset Translation)

```
원본 클러스터 (Primary):
  orders 파티션 0: 오프셋 0~10,000

복제 클러스터 (Secondary):
  us-east.orders 파티션 0: 오프셋 0~10,000 (같음, 또는 다를 수 있음)

MM2가 저장하는 오프셋 변환 맵:
  Primary:orders:0:9500 -> Secondary:us-east.orders:0:9500

DR 전환 후 Consumer 재시작:
  원래 오프셋(9500) -> Secondary에서 9500 위치 -> 중단 없이 재시작!
```

### 4. 주요 내부 토픽

| 내부 토픽 | 용도 |
|:---|:---|
| `heartbeats` | 클러스터 간 연결 상태 확인 |
| `mm2-configs.secondary.internal` | 복제 설정 상태 저장 |
| `mm2-offsets.secondary.internal` | 오프셋 변환 맵 저장 |
| `mm2-status.secondary.internal` | 태스크 상태 저장 |

**📢 섹션 요약 비유**
> MM2의 오프셋 변환은 "해외 이사 시 책 번호 매핑"이다. 원래 집(Primary)에서 책(메시지)에 번호(오프셋)를 매겼는데, 새 집(Secondary)에서 번호가 달라질 수 있다. MM2는 두 집의 번호 대조표(오프셋 변환 맵)를 자동으로 관리한다.

---

## Ⅲ. 비교 및 연결

### 1. DR 토폴로지 선택

| 토폴로지 | 구성 | 장점 | 단점 |
|:---|:---|:---|:---|
| Active-Passive | Primary -> Secondary | 단순, 명확한 DR 전환 | Secondary는 읽기 전용 |
| Active-Active | 양방향 복제 | 지역별 독립 쓰기 가능 | 루프 방지 로직 필요 |
| Hub-and-Spoke | 중앙 -> 다수 지역 | 중앙 집중식 관리 | 중앙 장애 시 전체 영향 |
| Fan-Out | 1 소스 -> N 대상 | 동일 데이터 다목적 활용 | 대역폭 소모 |

### 2. Kafka MirrorMaker 2 vs Confluent Replicator

| 항목 | MirrorMaker 2 (오픈소스) | Confluent Replicator (상용) |
|:---|:---|:---|
| 라이선스 | 오픈소스 | 유료 (Confluent Enterprise) |
| 오프셋 변환 | ✅ | ✅ (더 세밀한 제어) |
| 모니터링 | Kafka Connect 기본 | Confluent Control Center |
| 스키마 레지스트리 | 별도 설정 필요 | 자동 통합 |

**📢 섹션 요약 비유**
> Active-Passive는 "본사-지점 구조", Active-Active는 "두 본사 병렬 운영"이다. 지점(Secondary)은 본사가 닫힐 때만 역할을 하지만, 두 본사는 항상 동시에 영업한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### 1. DR 전환 절차

```
정상 운영:
  Primary - MM2 복제 ---> Secondary (읽기 전용)
  Consumer <- Primary 읽기

Primary 장애 발생:
1. Secondary의 오프셋 변환 맵 확인
2. Consumer 연결을 Secondary로 전환
3. 토픽 이름 변경: us-east.orders -> orders (Alias 설정)
4. Consumer 재시작 (오프셋 변환으로 처리 위치 복원)

Primary 복구 후:
5. 역방향 복제(Secondary -> Primary) 실행
6. 오프셋 재동기화 후 Primary 복귀
```

### 2. 체크리스트

- [ ] MM2 Connect Worker 수: 최소 3대 (HA 구성)
- [ ] 복제 토픽 패턴 명확화 (전체 복제 vs 선택 복제)
- [ ] 오프셋 변환 맵 저장 토픽의 복제 인자 = 3
- [ ] DR 전환 훈련 주기적 수행 (실제 전환 없이는 검증 불가)
- [ ] Consumer 코드에 DR 클러스터 주소 자동 전환 로직 포함

**📢 섹션 요약 비유**
> DR 전환 훈련은 "화재 대피 훈련"과 같다. 실제 화재가 나기 전에 훈련해야 실전에서 당황하지 않는다. MM2 설정이 완벽해도 DR 전환을 한 번도 안 해봤다면 실제 상황에서 실수가 발생한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| RPO 최소화 | 거의 실시간 복제로 데이터 손실 최소화 |
| RTO 단축 | 오프셋 변환으로 빠른 Consumer 재시작 |
| 무중단 마이그레이션 | Kafka 버전 업그레이드 시 병렬 운영 |
| 글로벌 확장 | 지역별 클러스터에 동일 데이터 제공 |

### 2. 결론

Kafka MirrorMaker 2는 엔터프라이즈 Kafka 운영에서 <strong>DR과 글로벌 분산의 핵심 인프라</strong>다. 학습 정리에서는 MM1의 한계(오프셋 비동기화), MM2의 개선(Kafka Connect 기반, 오프셋 변환), Active-Passive vs Active-Active 토폴로지 선택 기준, 그리고 DR 전환 절차를 함께 서술하는 것이 핵심이다.

**📢 섹션 요약 비유**
> MirrorMaker 2는 "데이터 센터의 자동 백업 시스템"이다. 매 순간 원본 데이터를 복사하고, 복사본 위치(오프셋)도 자동으로 매핑하여, 원본이 사라져도 복사본에서 정확히 어디서부터 계속할 수 있는지 알고 있다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Kafka Connect | 기반 프레임워크 | MM2는 Connect Connector로 구현 |
| Consumer Lag | 복제 상태 측정 | 복제 Lag = 원본과 복사본의 오프셋 차이 |
| DR (Disaster Recovery) | 주요 목적 | Active-Passive DR의 핵심 도구 |
| 오프셋 변환 | 핵심 기능 | DR 전환 후 Consumer 위치 복원 |
| Kafka 파티셔닝 | 복제 단위 | 파티션 단위로 복제 |


### 📈 관련 키워드 및 발전 흐름도

```text
[단일 클러스터 Kafka — 하나의 데이터센터 내 메시지 브로커, 장애 시 단일 장애점]
    |
    v
[Kafka MirrorMaker 1 — 간단한 컨슈머+프로듀서 복제, 오프셋 변환 미지원]
    |
    v
[Kafka MirrorMaker 2 (MM2) — Kafka Connect 기반, 오프셋 변환·자동 토픽 동기화 지원]
    |
    v
[Active-Passive DR — MM2로 보조 클러스터를 원본과 동기화, 장애 시 Failover 전환]
    |
    v
[Active-Active 다중 리전 — 양방향 복제로 지역 간 고가용성 메시지 처리 아키텍처]
```

이 흐름은 단일 클러스터의 단일 장애점 위험을 해소하기 위해 MirrorMaker 1에서 오프셋 변환과 자동 동기화를 지원하는 MM2로 진화하고, Active-Passive DR을 거쳐 완전한 Active-Active 다중 리전 아키텍처로 발전하는 Kafka 클러스터 복제의 핵심 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

Kafka MirrorMaker 2는 "중요 숙제의 사본을 만드는 자동 복사기"예요. 원본 공책(Primary 클러스터)의 내용을 실시간으로 사본 공책(Secondary 클러스터)에 복사하고, 어디까지 읽었는지(오프셋)도 기록해 둬요. 원본 공책이 불에 타도(Primary 장애) 사본 공책에서 읽던 곳부터 바로 이어서 공부할 수 있어요!
