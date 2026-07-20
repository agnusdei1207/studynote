---
title: "Apache ZooKeeper"
date: "2026-04-29"
tags:
  - "studynote-data-engineering"
weight: 29
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache ZooKeeper는 분산 시스템의 조율(Coordination) 서비스다. 분산 잠금(Distributed Lock), 리더 선출(Leader Election), 설정 관리(Config), 서비스 디스커버리(Service Discovery)를 일관성 있게 제공하는 분산 CP 시스템이다.
> 2. **가치**: 분산 환경에서 "두 노드가 동시에 같은 결정을 내리는 것"(스플릿 브레인, Split Brain)을 방지한다. ZAB(ZooKeeper Atomic Broadcast) 프로토콜로 과반수(쿼럼) 합의를 보장하여 일관성을 제공한다.
> 3. **판단 포인트**: ZooKeeper는 Kafka, HBase, Hadoop YARN, Solr의 핵심 의존성이었으나 운영 복잡성으로 인해 대안이 등장했다. Kafka는 KRaft(내장 Raft)로 ZooKeeper 의존성 제거(Kafka 3.3+), etcd(쿠버네티스), Consul이 현대적 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
+----------------------------------------------------------+
|          ZooKeeper 분산 조율 서비스                        |
+----------------------------------------------------------+
|                                                           |
|  분산 잠금:    노드 A      ZooKeeper     노드 B           |
|               "잠금 요청" ->  [Lock Znode] <- "대기"       |
|               잠금 획득 -> 작업 수행 -> 잠금 해제           |
|                                                           |
|  리더 선출:   노드1, 노드2, 노드3가 경쟁                   |
|               -> ZooKeeper가 공정한 리더 선출              |
|               -> 리더 장애 시 자동 재선출                  |
|                                                           |
|  ZooKeeper 앙상블 (최소 3개, 홀수 권장):                   |
|  [ZK1] [ZK2] [ZK3]  -> 과반수(2개) 살아있으면 정상 운영   |
+----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: ZooKeeper는 분산 시스템의 신뢰할 수 있는 공증인이다. 여러 서버가 "내가 리더야!"라고 주장할 때, ZooKeeper라는 공증인이 공정하게 하나만 인정하고 나머지에게 통보한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ZooKeeper znode (데이터 모델)

```text
ZooKeeper 데이터 트리 (/):
  /kafka/
    /brokers/
      /0001  -> broker 1 연결 정보
      /0002  -> broker 2 연결 정보
    /controller -> 현재 컨트롤러(리더) 브로커 ID

znode 타입:
  persistent: 클라이언트 연결 끊겨도 유지
  ephemeral:  클라이언트 세션 종료 시 자동 삭제 (리더 선출에 활용)
  sequential: 순서 번호 자동 부여 (공정한 잠금 구현)
```

### ZAB 프로토콜

```text
ZAB (ZooKeeper Atomic Broadcast):
  1. Leader가 변경 사항 제안 (Proposal)
  2. 과반수(n/2+1) Follower가 ACK
  3. Leader가 COMMIT 전파
  -> 모든 노드 동일 순서로 상태 업데이트 보장
```

- **📢 섹션 요약 비유**: ZAB 프로토콜은 민주주의 투표 시스템이다. 대통령(Leader)이 법안(변경사항)을 제출하면 국회의원(Follower) 과반수가 동의해야 통과된다. 과반수 미달이면 부결된다.

---

## Ⅲ. 비교 및 연결

| 비교 | ZooKeeper | etcd | Consul |
|:---|:---|:---|:---|
| 합의 | ZAB | Raft | Raft |
| 사용처 | Kafka, Hadoop | Kubernetes | 서비스 메시 |
| 복잡성 | 높음 | 낮음 | 중간 |
| 현황 | 레거시 의존 | 쿠버네티스 표준 | HashiCorp |

- **📢 섹션 요약 비유**: ZooKeeper vs etcd vs Consul은 공증인 세 명이다. ZooKeeper는 오래된 신뢰성 있는 공증인(복잡하지만 검증됨), etcd는 쿠버네티스 마을의 공식 공증인(간단·현대적), Consul은 클라우드 네이티브 환경 전문 공증인이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Kafka ZooKeeper 의존성 제거

```text
전통 Kafka 아키텍처:
  Kafka Broker + ZooKeeper 앙상블 분리 운영
  -> ZooKeeper 관리 부담, ZK-Kafka 버전 호환 이슈

Kafka KRaft (Kafka 3.3+, 2022):
  Kafka 내장 Raft 합의 프로토콜
  -> ZooKeeper 완전 제거 가능
  -> 단일 클러스터 운영, 관리 단순화
  -> 메타데이터 처리 성능 10배 향상
```

### ZooKeeper 적용 사례

```text
HBase: 마스터 서버 선출, RegionServer 등록
Hadoop YARN: ResourceManager HA
SolrCloud: 클러스터 상태·컬렉션 메타데이터 관리
Kafka (2.x 이하): 컨트롤러 선출, 토픽 메타데이터
```

- **�� 섹션 요약 비유**: Kafka KRaft는 공증인(ZooKeeper)을 회사 내부로 인수한 것이다. 외부 공증인에게 매번 의뢰하는 대신, 회사 내부 법무팀(KRaft)을 만들어서 더 빠르고 간편하게 처리한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong>분산 일관성</strong> | 과반수 합의로 Split Brain 방지 |
| **고가용성** | 앙상블로 장애 내성 |
| **범용 조율** | 잠금·리더·설정·디스커버리 통합 |

ZooKeeper는 대규모 분산 시스템의 조율 서비스 표준을 정립했다. 현재는 Kafka KRaft, 쿠버네티스 etcd로 대체되는 추세지만, ZooKeeper가 해결한 분산 조율 문제(리더 선출, 분산 잠금, 일관성)는 모든 현대 분산 시스템에서 여전히 핵심 과제다.

- **📢 섹션 요약 비유**: ZooKeeper의 레거시는 고등학교 수학의 기초와 같다. 지금은 계산기(Kafka KRaft, etcd)를 쓰지만, ZooKeeper가 해결한 분산 조율 원리를 이해하면 모든 현대 분산 시스템을 더 깊이 이해할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Raft/ZAB</strong> | 분산 합의 프로토콜 |
| <strong>etcd</strong> | 쿠버네티스 핵심 조율 서비스 |
| **KRaft** | Kafka 내장 ZooKeeper 대체 |
| **리더 선출** | 분산 시스템 핵심 조율 패턴 |
| <strong>CAP 정리</strong> | ZooKeeper는 CP 시스템 |

### 📈 관련 키워드 및 발전 흐름도

```text
[분산 시스템 조율 문제 — Split Brain, 리더 선출]
    |
    v
[Apache ZooKeeper — ZAB 프로토콜, 범용 조율 서비스]
    |
    v
[etcd — Raft 기반, Kubernetes 표준 조율]
    |
    v
[Kafka KRaft — ZooKeeper 의존성 제거]
    |
    v
[서비스 메시 — Consul 기반 서비스 디스커버리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. ZooKeeper는 여러 컴퓨터가 동시에 같은 결정을 내리지 않도록 조율하는 공증인이에요!
2. 리더 선출, 잠금 관리, 설정 공유 등 분산 시스템의 핵심 문제를 해결해줘요!
3. 요즘 Kafka는 ZooKeeper를 없애고 내부 직접 조율(KRaft)로 더 간단하게 운영한답니다!
