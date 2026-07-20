---
title: "CAP Theorem"
date: "2026-03-19"
tags:
  - "studynote-data-engineering"
weight: 40
---
> **핵심 인사이트**
> 1. CAP 정리(CAP Theorem, Brewer 2000)는 분산 데이터베이스 시스템이 일관성(Consistency)·가용성(Availability)·파티션 내성(Partition Tolerance) 세 가지를 동시에 완벽히 보장할 수 없으며, 파티션(네트워크 분리)은 실제 환경에서 불가피하므로 CP 또는 AP 중 하나를 선택해야 한다는 근본 제약이다.
> 2. CP 시스템(MongoDB, HBase, ZooKeeper)은 파티션 발생 시 가용성을 희생해 일관성을 유지하고, AP 시스템(Cassandra, DynamoDB, CouchDB)은 가용성을 유지하되 결과적 일관성(Eventual Consistency)을 허용한다.
> 3. 현실 설계에서 CAP는 이진 선택이 아닌 스펙트럼이며, PACELC 모델(2012)이 파티션 없는 상황에서도 지연(Latency)과 일관성 트레이드오프를 추가로 고려하는 더 실용적 프레임워크다.

---

## Ⅰ. CAP 세 축

```
CAP 정리의 세 속성:

C (Consistency, 일관성):
  모든 노드가 동시에 같은 데이터를 봄
  읽기 요청 -> 항상 최신 데이터 반환
  "강한 일관성 (Strong Consistency)"

A (Availability, 가용성):
  모든 요청에 응답 (성공/실패 상관없이)
  응답이 없거나 타임아웃 없음
  "항상 응답"

P (Partition Tolerance, 파티션 내성):
  네트워크 분리 시에도 시스템 계속 동작
  메시지 손실/지연이 발생해도 작동

핵심 결론:
  P는 분산 시스템에서 포기 불가 (현실적으로 발생)
  따라서 CP or AP 선택

  CA 시스템 = 실질적으로 단일 노드 (분산 아님)
```

> 📢 **섹션 요약 비유**: CAP는 쌍둥이 중 항상 한 명은 자야 하는 것 — 일관성(C)과 가용성(A) 중 네트워크 장애(P) 때는 하나를 포기해야 한다.

---

## Ⅱ. CP 시스템

```
CP (Consistency + Partition Tolerance):

특성:
  파티션 발생 시 -> 가용성 희생
  일부 요청에 "오류/타임아웃" 반환
  -> 잘못된 데이터 반환보다 오류 선호

대표 시스템:
  HBase:
    HDFS 기반 컬럼 스토어
    강한 일관성 (단일 리전)
    Zookeeper로 분산 코디네이션

  MongoDB (기본 설정):
    Primary-Secondary 복제
    Primary 장애 시 쓰기 차단 (일시적)

  ZooKeeper:
    분산 코디네이션 서비스
    리더 선출, 설정 관리
    Paxos 합의 알고리즘 기반

사용 케이스:
  금융 거래 (이중 인출 방지 필수)
  재고 관리 (마이너스 재고 방지)
  예약 시스템 (중복 예약 방지)
```

> 📢 **섹션 요약 비유**: CP 시스템은 보수적인 은행 창구 — 시스템 점검 중에는 "잠시 후 다시 오세요"라고 하지만 실수로 이중 인출은 절대 안 한다.

---

## Ⅲ. AP 시스템

```
AP (Availability + Partition Tolerance):

특성:
  파티션 발생 시 -> 일관성 희생
  모든 요청에 응답 (최신이 아닐 수 있음)
  결과적 일관성 (Eventual Consistency)
  "나중에는 동기화됨"

대표 시스템:
  Cassandra (AP 기본):
    멀티 마스터, 모든 노드 동등
    일관성 수준 조정 가능 (ONE, QUORUM, ALL)
    파티션 시에도 계속 쓰기 허용

  DynamoDB:
    AWS 관리형 NoSQL
    기본 Eventually Consistent
    옵션으로 Strong Consistent 선택 가능

  CouchDB:
    멀티 마스터 복제
    충돌 감지 + 자동 해결 정책

사용 케이스:
  SNS 좋아요 수 (약간 틀려도 괜찮음)
  쇼핑몰 장바구니
  콘텐츠 캐싱 레이어
```

> 📢 **섹션 요약 비유**: AP 시스템은 소셜 미디어 좋아요 — 잠깐 동안 내가 본 좋아요 수와 다른 사람 것이 달라도 나중엔 같아지면 OK.

---

## Ⅳ. PACELC 모델

```
PACELC (Daniel Abadi, 2012):
CAP의 한계를 보완한 확장 모델

CAP 한계:
  파티션 없을 때의 트레이드오프 설명 불가

PACELC:
  Partition 발생 시:
    A (Availability) vs C (Consistency)
    (= CAP와 동일)

  Else (파티션 없을 때):
    L (Latency) vs C (Consistency)

핵심: 파티션 없어도 일관성을 높이면 지연 증가

분류:
  PA/EL: Cassandra (가용성 + 저지연)
  PC/EC: HBase (일관성 우선)
  PA/EC: MongoDB (기본)
  PC/EL: ZooKeeper (강한 일관성, 높은 지연 허용)

실무 함의:
  "우리 시스템은 CAP에서 C vs A"뿐 아니라
  "정상 상태에서도 Latency vs Consistency" 고려 필요
```

> 📢 **섹션 요약 비유**: PACELC는 CAP보다 현실적인 고민 — 네트워크 멀쩡할 때도 "빠른 응답 vs 정확한 응답" 중 뭘 더 원하냐의 선택이 있다.

---

## Ⅴ. 실무 시나리오 — E-commerce 시스템 설계

```
이커머스 데이터베이스 설계 CAP 선택:

요구사항 분석:
  주문/결제: 절대 이중 처리 불가 -> CP 선택
  상품 재고: 마이너스 재고 방지 -> CP 선택
  장바구니: 약간의 불일치 허용 -> AP 선택
  상품 조회: 최신 가격 아니어도 OK -> AP 선택
  리뷰/댓글: 결과적 일관성 충분 -> AP 선택

데이터 저장소 선택:
  주문 DB: PostgreSQL (RDBMS, 강한 일관성)
  재고 DB: Redis + 분산 락 (Redlock)
  장바구니: DynamoDB (AP, 고가용성)
  상품 카탈로그: Elasticsearch (검색, AP)
  세션: Redis Cluster

Black Friday 트래픽 시나리오:
  상품 조회 트래픽 100배 급증
  -> AP 카탈로그 DB: 문제 없이 확장

  재고 차감 동시 요청 급증
  -> CP 재고 DB: 락 경합 증가 -> 일부 지연
  -> 해결: 재고 사전 예약 + 배치 차감

결론: 데이터 성격별 CP/AP 혼합 아키텍처
```

> 📢 **섹션 요약 비유**: E-commerce CAP 선택은 식당 음식 준비 — 계산서(결제)는 정확해야 하고(CP), 오늘의 메뉴판(카탈로그)은 잠깐 틀려도 OK(AP).

---

## 📌 관련 개념 맵

```
CAP 정리 (CAP Theorem)
+-- 세 속성
|   +-- C (Consistency)
|   +-- A (Availability)
|   +-- P (Partition Tolerance)
+-- 시스템 유형
|   +-- CP: HBase, MongoDB, ZooKeeper
|   +-- AP: Cassandra, DynamoDB, CouchDB
+-- 확장 모델
|   +-- PACELC (Latency vs Consistency)
+-- 일관성 모델
    +-- Strong Consistency
    +-- Eventual Consistency
    +-- Read-your-writes, Monotonic Read
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[분산 시스템 연구 (1980s)]
Lamport Clock, Byzantine Fault
      |
      v
[CAP 추측 (Brewer, 2000)]
PODC 키노트 발표
      |
      v
[CAP 수학적 증명 (2002)]
Gilbert & Lynch 논문
      |
      v
[NoSQL 움직임 (2009~)]
Cassandra, MongoDB, DynamoDB
CAP 기반 설계 패턴 실용화
      |
      v
[PACELC 모델 (Abadi, 2012)]
CAP 한계 보완
      |
      v
[현재: 뉴SQL / 분산 SQL]
CockroachDB, Spanner: CP + 글로벌 분산
"CAP를 우회"하는 Paxos/Raft 기반 설계
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. CAP 정리는 세 가지 좋은 점(정확함, 빠름, 고장에도 OK) 중 동시에 두 개만 선택할 수 있는 규칙이에요.
2. 인터넷 장애가 나면 "일단 응답하되 데이터가 조금 오래됐을 수 있어요(AP)" 또는 "정확한 데이터가 준비될 때까지 잠깐 기다려요(CP)" 중 하나를 선택해야 해요.
3. 은행 앱(CP)과 SNS 좋아요(AP)가 다르게 작동하는 이유가 바로 이 CAP 정리 때문이에요!
