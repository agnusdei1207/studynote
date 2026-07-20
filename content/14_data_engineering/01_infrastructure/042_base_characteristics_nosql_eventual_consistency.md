---
title: "Base Characteristics Nosql Eventual Consistency"
date: "2026-04-05"
tags:
  - "studynote-data-engineering"
weight: 42
---
> **핵심 인사이트**
> 1. BASE(Basically Available, Soft-state, Eventual Consistency)는 ACID의 엄격한 일관성을 포기하고 가용성과 분산성을 극대화한 NoSQL의 설계 철학으로, CAP 정리에서 Partition Tolerance를 선택한 시스템이 필연적으로 채택하는 일관성 모델이다.
> 2. BASE의 핵심인 Eventual Consistency(결과적 일관성)는 "언젠가는 모든 노드가 같은 값을 갖게 된다"는 보장으로, Amazon Dynamo의 사례처럼 짧은 불일치 윈도우 동안 읽기 요청이 구버전 데이터를 반환할 수 있다 — 이것이 허용되는 서비스(소셜 피드, 장바구니)와 불허되는 서비스(금융 결제, 재고)를 구분하는 기준이 된다.
> 3. BASE는 ACID와 상반된 개념이 아니라 트레이드오프 — 현대 시스템은 중요도에 따라 코어 트랜잭션(ACID)과 주변 데이터(BASE)를 혼합하는 폴리글롯 퍼시스턴스(Polyglot Persistence) 아키텍처를 채택한다.

---

## Ⅰ. BASE 3요소 상세

```
BASE (Basically Available, Soft-state, Eventual Consistency):

B - Basically Available (기본적 가용성):
  일부 노드 장애 시에도 시스템 전체는 응답 가능
  단, 응답이 최신 데이터가 아닐 수 있음
  예: Cassandra의 일부 노드 다운 -> 나머지 노드 계속 읽기/쓰기

S - Soft-state (연한 상태):
  외부 입력 없이도 시간이 지남에 따라 시스템 상태가 변화 가능
  복제 과정에서 노드 간 일시적 불일치 허용
  예: DNS 캐시 TTL 만료 전 구버전 IP 반환

E - Eventual Consistency (결과적 일관성):
  "충분한 시간이 지나면 모든 복제본이 일치한다"
  언제: 새로운 쓰기가 없고 복제가 완료된 후
  보장: 일관성을 보장하지만 즉시는 아님

비교:
  ACID Consistency: 트랜잭션 후 즉시 모든 읽기가 최신값 반환
  BASE E. Consistency: 모든 노드가 결국에는 같아짐

ε-가용성 (Epsilon Availability):
  수학적 표현: staleness(t) ≤ ε
  ε: 허용 가능한 최대 불일치 윈도우 (예: 100ms)
  실제 Dynamo: 수 밀리초 ~ 수 초
```

> 📢 **섹션 요약 비유**: BASE는 여러 지점 카페의 메뉴판 — 본사에서 가격이 바뀌면 모든 지점이 즉시 동시에 바뀌지 않지만 며칠 내에 전부 바뀜(결과적 일관성).

---

## Ⅱ. ACID vs BASE 비교

```
ACID (전통 RDBMS):
  A - Atomicity: 전부 성공 또는 전부 롤백
  C - Consistency: 항상 유효한 상태 유지
  I - Isolation: 트랜잭션 간 격리
  D - Durability: 커밋 후 영구 저장

  장점: 강력한 일관성, 에러 처리 간단
  단점: 분산 환경에서 성능/가용성 저하
  적합: 금융 결제, 회계, 재고 관리

BASE (NoSQL):
  B - Basically Available
  A - Soft-state
  S - Eventual Consistency

  장점: 고가용성, 수평 확장성, 파티션 내성
  단점: 복잡한 애플리케이션 로직 (충돌 해결)
  적합: SNS 피드, 쇼핑 카트, 로그 수집, DNS

CAP 정리와의 연결:
  ACID: CP (일관성 + 분산, 가용성 약화)
  BASE: AP (가용성 + 분산, 일관성 약화)

현실의 일관성 수준 스펙트럼:
  Strong -> Linearizable -> Sequential -> Causal -> Eventual
  강한 일관성 ------------------------------> 약한 일관성
  낮은 가용성                                   높은 가용성
```

> 📢 **섹션 요약 비유**: ACID vs BASE는 현금 vs 외상 장부 — 현금(ACID)은 즉시 정확하지만 느리고, 외상(BASE)은 빠르지만 정산(동기화)이 나중.

---

## Ⅲ. Eventual Consistency 구현 방법

```
결과적 일관성 구현 기법:

1. Vector Clock (벡터 클락):
   각 노드가 [N1:v1, N2:v2, N3:v3] 타임스탬프 유지
   쓰기 충돌 탐지에 사용
   Amazon Dynamo DB 적용 사례

2. Last-Write-Wins (LWW):
   타임스탬프 기반 최신 쓰기 승리
   간단하지만 클럭 동기화 필요
   Cassandra 기본 충돌 해결 방식

3. Multi-Version Concurrency Control (MVCC):
   충돌 발생 시 여러 버전 보존
   읽기 시 애플리케이션이 병합(merge) 결정
   CouchDB, Riak 적용

4. CRDTs (Conflict-free Replicated Data Types):
   수학적으로 충돌 없이 자동 병합 가능한 자료구조
   카운터 CRDT: 분산 Like 카운트 합산
   Set CRDT: 쇼핑 카트 아이템 집합 병합
   Riak, Redis Enterprise 활용

읽기 복구 (Read Repair):
  읽기 요청 시 오래된 복제본을 최신으로 갱신
  Cassandra, Dynamo 기반 시스템

안티-엔트로피 (Anti-Entropy):
  백그라운드 프로세스로 지속적 노드 간 동기화
  Merkle Tree로 불일치 탐지 후 복제
```

> 📢 **섹션 요약 비유**: Eventual Consistency는 소문 퍼지기 — 여러 친구에게 전달되다 보면 결국 모두 알게 되지만, 처음엔 아직 모르는 친구가 있을 수 있어요.

---

## Ⅳ. NoSQL 시스템별 BASE 구현

```
주요 NoSQL DB BASE 구현 방식:

Amazon DynamoDB:
  Read Consistency: Eventually Consistent (기본) vs Strongly Consistent (옵션)
  Eventual: 읽기 용량 절반 소비, 저렴
  Strong: 최신 쓰기 반영 보장, 비용 2배

Cassandra:
  Replication Factor (RF): 데이터 복사본 수
  Consistency Level:
    ONE: 1개 노드 응답으로 읽기 완료
    QUORUM: 과반수 노드 응답 (RF=3이면 2개)
    ALL: 전체 노드 응답 (강한 일관성)
  R + W > RF -> Strong Consistency 달성 가능

MongoDB:
  기본: PRIMARY 노드에서만 읽기 (강한 일관성)
  Read Concern secondaryPreferred -> Eventual
  Write Concern w:1 vs w:majority

Redis Cluster:
  비동기 복제 (PRIMARY -> REPLICA)
  PRIMARY 장애 시 REPLICA 승격 전 데이터 손실 가능
  -> BASE 모델

주의 사항:
  BASE로 설계된 시스템에서 ACID 트랜잭션을 억지로 구현하면
  결국 성능/확장성 이점을 잃음
  -> 올바른 데이터 모델링 선택이 핵심
```

> 📢 **섹션 요약 비유**: NoSQL BASE 설정은 스피커 음량 조절 — 가용성(볼륨 높음) vs 일관성(음질 좋음) 사이에서 Consistency Level이라는 다이얼로 균형 조정.

---

## Ⅴ. 실무 시나리오 — 폴리글롯 퍼시스턴스

```
이커머스 폴리글롯 퍼시스턴스 아키텍처:

결제 서비스 (ACID 필수):
  PostgreSQL (RDBMS)
  트랜잭션: 결제 + 재고 감소 원자적 처리
  Isolation Level: Serializable
  이유: 오버셀링, 중복 결제 절대 불가

상품 카탈로그 (BASE 허용):
  MongoDB
  일관성: Eventual (약간 지연된 가격 표시 OK)
  이유: 수백만 SKU, 빠른 읽기 > 즉시 일관성

장바구니 (BASE 최적):
  Redis (CRDT 기반)
  일관성: Eventual
  이유: 일시적 불일치(동일 기기 2개 탭)는 허용
        가용성이 더 중요 (장바구니 오류 = 매출 손실)

사용자 세션 (BASE):
  Redis Cluster
  일관성: Eventual
  이유: 세션 데이터 약간 오래돼도 UX 영향 미미

리뷰/평점 (BASE):
  Cassandra
  일관성: ONE (빠른 읽기)
  이유: 리뷰 평균 0.01점 차이는 무관

검색 인덱스 (BASE):
  Elasticsearch
  일관성: Eventual (인덱싱 지연 수초 허용)
  이유: 검색 결과에 신상품 즉시 반영 불필요

결론:
  "모든 데이터에 ACID" -> 과도 엔지니어링
  "모든 데이터에 BASE" -> 금융 데이터 위험
  -> 데이터 중요도별 적합한 일관성 모델 선택
```

> 📢 **섹션 요약 비유**: 폴리글롯 퍼시스턴스는 주방 도구 전문화 — 칼은 썰기(ACID 결제), 냄비는 끓이기(BASE 피드), 믹서는 갈기(검색 엔진), 각자 전문 도구 사용.

---

## 📌 관련 개념 맵

```
BASE 특성
+-- 3요소
|   +-- Basically Available
|   +-- Soft-state
|   +-- Eventual Consistency
+-- 관련 이론
|   +-- CAP 정리 (AP 선택)
|   +-- PACELC 정리
+-- 구현 기법
|   +-- Vector Clock
|   +-- LWW, MVCC, CRDTs
|   +-- Read Repair, Anti-Entropy
+-- 적용 시스템
|   +-- DynamoDB, Cassandra, Redis
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[RDBMS ACID 시대 (1970s~)]
C.J. Date, Edgar Codd 관계형 모델
트랜잭션 ACID 원칙 확립
      |
      v
[인터넷 규모 확장 문제 (2000s)]
Google Bigtable (2006), Amazon Dynamo (2007)
BASE 개념 Eric Brewer 공식화
      |
      v
[CAP 정리 실용화 (2010~)]
NoSQL 운동 (CouchDB, MongoDB, Cassandra)
BASE를 명시적으로 채택
      |
      v
[CRDT 발전 (2011~)]
충돌 없는 분산 자료구조
Riak, Redis Enterprise 채택
      |
      v
[현재: 뉴SQL + BASE 혼합]
CockroachDB, Spanner (분산 ACID)
Google Spanner: 외부 일관성 (TrueTime API)
NewSQL: ACID + 분산 확장성 동시 달성
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. BASE는 여러 지점 카페의 메뉴판 — 본사에서 가격이 바뀌어도 모든 지점이 동시에 바뀌지 않지만 며칠 내에 전부 같아져요!
2. 결과적 일관성은 소문이 퍼지는 것 — 처음엔 모르는 친구가 있지만 결국 모두 알게 돼요.
3. 중요한 결제 데이터는 ACID(은행 금고), 덜 중요한 피드 데이터는 BASE(보통 서랍) — 각각 다른 규칙으로 저장해요!
