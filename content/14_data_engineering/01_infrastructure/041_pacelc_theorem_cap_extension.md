---
title: "PACELC Theorem"
date: "2026-04-05"
tags:
  - "studynote-data-engineering"
weight: 41
---
> **핵심 인사이트**
> 1. PACELC(파셀크) 정리는 Daniel Abadi(2012)가 CAP 정리의 한계를 극복하기 위해 제안한 확장 모델로, 파티션 발생 시(P) 가용성(A)/일관성(C) 트레이드오프 외에 정상 상태에서도 지연(L, Latency)/일관성(C, Consistency) 트레이드오프가 존재함을 명시한다.
> 2. CAP 정리가 "파티션 발생"이라는 극단적 상황만 다루는 반면, PACELC는 파티션이 없는 정상 운영 상황에서도 "낮은 지연(L) vs 강한 일관성(C)"의 선택이 필요함을 보여줌으로써 분산 데이터베이스 선택의 실무적 기준을 제시한다.
> 3. DynamoDB·Cassandra(PA/EL), HBase·VoltDB(PC/EC)처럼 실제 NoSQL/분산 DB는 PACELC 분류로 그 특성을 명확히 설명할 수 있으며, 애플리케이션 요구사항에 따라 PA/EL(가용성·저지연 우선) vs PC/EC(일관성 우선)를 선택해야 한다.

---

## Ⅰ. CAP 정리와 한계

```
CAP 정리 복습:
  C (Consistency): 모든 노드가 동일한 최신 데이터
  A (Availability): 항상 응답 (부분 노드 실패 무관)
  P (Partition Tolerance): 네트워크 분단 내성

CAP: 파티션 상황에서 C vs A 중 하나만 선택

CAP의 한계:
  1. 파티션은 실제로 매우 드문 상황
  2. 파티션이 없을 때의 트레이드오프는?
  3. Latency(지연)를 다루지 않음

실제 분산 시스템의 고민:
  "파티션 없을 때도 복제 일관성 vs 낮은 지연
   사이에서 선택이 필요하다"

PACELC 등장 배경:
  Daniel Abadi (Yale, 2012)
  CAP을 정상 상태(Else 조건)까지 확장
```

> 📢 **섹션 요약 비유**: CAP은 "화재 시 탈출 vs 안전" 딜레마만 다루지만, PACELC는 "평소에도 속도 vs 안전" 딜레마가 있음을 추가로 다룬다.

---

## Ⅱ. PACELC 정리 구조

```
PACELC 정리:

P (Partition 발생 시):
  A (Availability) vs C (Consistency)

E (Else, 정상 상태):
  L (Latency) vs C (Consistency)

전체 표기: PA/EL, PC/EL, PA/EC, PC/EC

PA/EL (가용성 + 저지연 우선):
  파티션: 가용성 선택 (일부 불일치 허용)
  정상:   저지연 선택 (복제 지연 허용)
  예: DynamoDB, Cassandra, Riak

PC/EC (일관성 우선):
  파티션: 일관성 선택 (가용성 포기)
  정상:   일관성 선택 (지연 감수)
  예: HBase, VoltDB, BigTable

PA/EC (혼합):
  파티션: 가용성, 정상: 일관성
  예: MongoDB (기본값: 가용성 우선)

PC/EL (혼합):
  드문 조합, 일부 NewSQL 시도
```

> 📢 **섹션 요약 비유**: PACELC는 마트 계산대 선택 — 손님 많을 때(파티션) 속도 vs 정확도, 평소에도 빠른 계산(L) vs 틀림없는 계산(C).

---

## Ⅲ. 주요 DB PACELC 분류

```
분산 데이터베이스 PACELC 분류:

PA/EL (가용성 + 저지연):
  DynamoDB: 글로벌 테이블, 최종 일관성 기본
  Cassandra: AP 설계, Tunable Consistency
  Riak: 최종 일관성 중심
  Voldemort (LinkedIn): 가용성 극대화

PC/EC (일관성 우선):
  HBase: HDFS 기반, 강한 일관성
  VoltDB: ACID, 분산 트랜잭션
  Zookeeper: 메타데이터 일관성 보장

PA/EC (가용성 우선, 정상 일관성):
  MongoDB: replica set, 기본 primary 읽기

PC/EL:
  드문 조합

RDBMS (분산 상황):
  MySQL Cluster: PC/EC 시도

NewSQL:
  CockroachDB: PC/EC + 분산 트랜잭션
  Google Spanner: PC/EC (TrueTime 활용)
  YugabyteDB: PC/EC (Raft 합의)

Tunable Consistency (Cassandra):
  QUORUM: 과반수 노드 응답 요구
  ALL: 전체 노드 응답 (강한 일관성)
  ONE: 1개 응답 (최저 지연)
```

> 📢 **섹션 요약 비유**: PACELC 분류는 음식점 배달 vs 홀식 선택 — Cassandra(빠른 배달, 오배송 허용), CockroachDB(홀식, 느려도 정확).

---

## Ⅳ. 실무 DB 선택 기준

```
PACELC 기반 DB 선택 기준:

PA/EL 선택 상황:
  - 전 세계 사용자, 낮은 지연 필수
  - 일시적 불일치 허용 (SNS, 추천, 장바구니)
  - 높은 쓰기 처리량 필요
  예: 쇼핑몰 상품 추천, 소셜 피드

PC/EC 선택 상황:
  - 금융 거래, 재고 차감 (이중 청구 불허)
  - 의료 기록 (불일치 위험)
  - 강한 읽기-쓰기 일관성 필요
  예: 결제 시스템, 계좌 이체

혼합 사용 (폴리글랏 퍼시스턴스):
  결제: CockroachDB (PC/EC)
  장바구니: DynamoDB (PA/EL)
  사용자 세션: Redis (PA/EL)
  분석: Cassandra (PA/EL)

Eventual Consistency vs Strong Consistency:
  최종 일관성(PA/EL):
    모든 노드가 결국(eventually) 동기화
    "언제 동기화될지" 보장 없음

  강한 일관성(PC/EC):
    모든 읽기가 최신 쓰기 반영
    Raft, Paxos 합의 알고리즘 필요
    지연 증가 (Round-trip 추가)
```

> 📢 **섹션 요약 비유**: PACELC 선택은 통장 vs 편의점 — 통장(금융)은 PC/EC(정확해야), 편의점 포인트(부가 서비스)는 PA/EL(빨라야).

---

## Ⅴ. 실무 시나리오 — 글로벌 이커머스

```
글로벌 이커머스 C사 DB 설계:

요구사항:
  - 전 세계 50개국, 사용자 1억 명
  - 재고 차감: 이중 판매 절대 불가
  - 상품 카탈로그: 빠른 조회 필요
  - 사용자 장바구니: 짧은 지연 필요
  - 결제: ACID 트랜잭션 필수
  - 추천 시스템: 1초 이내 응답

PACELC 기반 DB 선택:

재고/결제 (PC/EC):
  Google Spanner
  이유: 전 세계 분산 + ACID + 강한 일관성
  비용: 높음, 지연: 중간

상품 카탈로그 (PA/EL):
  DynamoDB Global Tables
  이유: 저지연(~5ms), 최종 일관성 허용

장바구니 (PA/EL):
  Cassandra (DC별 복제)
  이유: 고가용성, 로컬 저지연

사용자 세션 (PA/EL):
  Redis Cluster
  이유: 인메모리, 1ms 미만 지연

추천 시스템 (PA/EL):
  Cassandra + 피처 스토어
  이유: 대규모 쓰기, 저지연 읽기

결과:
  재고 이중 판매 0건 (PC/EC 효과)
  상품 조회 P99: 12ms (PA/EL 효과)
  글로벌 가용성: 99.995%
```

> 📢 **섹션 요약 비유**: 글로벌 이커머스 DB는 백화점 부서별 다른 규정 — 현금(결제, PC/EC)은 정확하게, 진열품(카탈로그, PA/EL)은 빠르게, 고객 쇼핑백(장바구니)도 빠르게.

---

## 📌 관련 개념 맵

```
PACELC 정리
+-- 기반
|   +-- CAP 정리 (Brewer, 2000)
|   +-- Daniel Abadi 확장 (2012)
+-- 분류
|   +-- PA/EL: DynamoDB, Cassandra
|   +-- PC/EC: HBase, Spanner, CockroachDB
+-- 핵심 개념
|   +-- Eventual Consistency
|   +-- Strong Consistency (Raft/Paxos)
|   +-- Tunable Consistency
+-- 선택 기준
    +-- 금융/재고: PC/EC
    +-- 피드/추천: PA/EL
    +-- 폴리글랏: 혼합
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[CAP 정리 (Brewer, 2000)]
분산 시스템 기초 이론
네트워크 파티션 시 트레이드오프
      |
      v
[PACELC 정리 (Abadi, 2012)]
Latency 차원 추가
정상 상태 트레이드오프 명시화
      |
      v
[Tunable Consistency (Cassandra)]
QUORUM/ALL/ONE 선택 가능
애플리케이션이 일관성 수준 결정
      |
      v
[NewSQL 등장 (2015~)]
CockroachDB, Spanner (PC/EC + 분산)
SQL + 분산 + 강한 일관성 시도
      |
      v
[현재: 폴리글랏 퍼시스턴스]
한 서비스에 여러 DB 혼합
도메인별 PACELC 최적 선택
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. CAP은 인터넷이 끊겼을 때 어떻게 할지 규칙이었는데, PACELC는 "평소에도" 빠른 응답(L) vs 정확함(C) 중 하나를 골라야 한다고 알려줘요!
2. DynamoDB·Cassandra는 PA/EL — "좀 틀려도 괜찮으니까 빠르게!", HBase·Spanner는 PC/EC — "느려도 정확하게!"를 선택했어요.
3. 쇼핑몰에서 상품 목록(빠르면 됨, PA/EL)과 결제(틀리면 큰일, PC/EC)에 다른 DB를 쓰는 것처럼 목적에 맞게 선택해야 해요!
