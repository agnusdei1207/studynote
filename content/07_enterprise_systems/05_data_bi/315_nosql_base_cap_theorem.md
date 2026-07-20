---
title: "NoSQL BASE CAP Theorem"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
weight: 315
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAP 정리는 분산 시스템이 Consistency(일관성), Availability(가용성), Partition Tolerance(분단 내성) 셋 중 둘만 동시에 완전히 보장할 수 있다는 이론이다.
> 2. **가치**: BASE (Basically Available, Soft state, Eventually consistent)는 CAP의 AP 선택 결과로, 높은 가용성과 수평 확장을 택하는 대신 일시적 불일관성을 허용한다.
> 3. **판단 포인트**: 금융 거래·재고 관리는 ACID/CP가 필수이고, 소셜 피드·장바구니는 BASE/AP로 가용성 우선이 적합하다.

## Ⅰ. 개요 및 필요성

단일 서버 관계형 DB는 ACID (Atomicity, Consistency, Isolation, Durability) 트랜잭션으로 강한 일관성을 보장한다.
그러나 수평 확장이 필요한 분산 시스템에서는 네트워크 분단(Partition)이 반드시 발생하므로, Eric Brewer가 2000년에 발표한 CAP 정리에 따라 C 또는 A 중 하나를 타협해야 한다.

CAP 정리 3 속성:
- <strong>Consistency (C)</strong>: 모든 노드가 동일 시점에 동일 데이터를 봄
- <strong>Availability (A)</strong>: 모든 요청이 응답을 받음 (오류 없이)
- <strong>Partition Tolerance (P)</strong>: 네트워크 분단 상황에서도 동작 지속

실제 분산 시스템에서 P는 포기할 수 없으므로 CP 또는 AP를 선택한다.

📢 **섹션 요약 비유**: CAP는 "맛있고, 빠르고, 저렴한" 식당의 삼각형이다. 세 가지를 동시에 모두 갖추기는 불가능하다.

## Ⅱ. 아키텍처 및 핵심 원리

### CP vs AP 시스템 분류

| 분류 | 특징 | 대표 DB |
|:---|:---|:---|
| CP (일관성+분단 내성) | 분단 시 응답 거부, 일관성 보장 | HBase, Zookeeper, MongoDB(w:majority) |
| AP (가용성+분단 내성) | 분단 시에도 응답, 일시적 불일관성 | Cassandra, DynamoDB, CouchDB |
| CA (이론적 구분) | 분산 아닌 단일 서버 | 전통 RDBMS (MySQL, PostgreSQL) |

### BASE vs ACID 비교

| 항목 | ACID | BASE |
|:---|:---|:---|
| Atomicity | 전체 성공 or 전체 롤백 | 최선의 결과 시도 |
| Consistency | 트랜잭션 후 항상 일관 | 결과적 일관성 (Eventually) |
| Isolation | 트랜잭션 간 완전 격리 | 약한 격리 (동시성 증가) |
| Durability vs Soft state | 영속 보장 | 일시적 상태 허용 |
| 확장성 | 수직 확장 한계 | 수평 확장 용이 |

### ASCII 다이어그램: CAP 삼각형과 DB 배치

```
  +-------------------------------------------------------------+
  |                  CAP 삼각형                                  |
  |                                                             |
  |                Consistency (C)                              |
  |                      △                                      |
  |                     / \                                     |
  |                    /   \                                    |
  |                   /     \                                   |
  |         CP 영역  /       \  (불가능 영역)                    |
  |                 /         \                                 |
  |        HBase   /           \  MongoDB                      |
  |     Zookeeper ●             ● (default)                    |
  |               /    ×전부     \                              |
  |              / (이론상 불가)  \                              |
  |             /-----------------\                            |
  |            /                   \                           |
  | Partition ●                     ● Availability             |
  | Tolerance  \       AP 영역      /  (A)                     |
  |    (P)      \                  /                           |
  |              \ Cassandra      /                            |
  |               ● DynamoDB ●   /                             |
  |                \  CouchDB   /                              |
  |                 ●----------●                               |
  |                                                             |
  |  RDBMS (MySQL, PostgreSQL): 단일 서버 -> CA 영역 (P 포기)    |
  +-------------------------------------------------------------+
```

### 일관성 레벨 스펙트럼

| 레벨 | 설명 | 지연 | 사용 예 |
|:---|:---|:---|:---|
| Strong (강한 일관성) | 모든 노드 즉시 동일 | 높음 | 금융 잔액 |
| Bounded Staleness | N초 이내 일관성 보장 | 중간 | 재고 조회 |
| Session | 같은 세션 내 일관성 | 낮음 | 사용자 프로필 |
| Eventual (결과적 일관성) | 언젠가 일관 (수ms~수초) | 매우 낮음 | 소셜 피드, 장바구니 |

📢 **섹션 요약 비유**: 결과적 일관성은 소문이다. 처음엔 사람마다 다르게 알지만, 시간이 지나면 모두 같은 내용을 알게 된다.

## Ⅲ. 비교 및 연결

### PACELC 확장 정리

CAP의 한계를 보완한 PACELC (Partition -> AP or CP, Else -> Latency or Consistency):
- **분단 시 (P)**: A(가용성) vs C(일관성) 선택
- **정상 시 (E)**: L(지연) vs C(일관성) 트레이드오프

| DB | 분단 시 | 정상 시 |
|:---|:---|:---|
| Cassandra | AP | EL (지연 최소화) |
| DynamoDB | AP | EL |
| HBase | CP | EC (일관성 강조) |
| MongoDB | CP (default) | EC |

📢 **섹션 요약 비유**: PACELC는 CAP보다 현실적인 지도다. 평상시 운전 규칙(Else)과 사고 시 대응(Partition)을 모두 다룬다.

## Ⅳ. 실무 적용 및 실무자 판단

### 일관성 모델 선택 체크리스트

- [ ] 데이터의 금전적 가치가 있는가? (은행 잔액 -> CP/ACID 필수)
- [ ] 일시적 불일관성이 비즈니스에 허용 가능한가? (좋아요 수 -> AP/BASE OK)
- [ ] 지리적 분산 배포 필요 여부 (멀티 리전 -> AP 선호)
- [ ] 99.99% 이상 가용성 요건 -> AP 우선 고려

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 재고 차감에 Cassandra AP | 동시 구매 시 재고 초과 판매 | CP DB (HBase, Redis SETNX) 사용 |
| 모든 NoSQL에 ACID 기대 | Cassandra는 Eventual Consistency | LWT (Light-weight Transaction) 사용 |

📢 **섹션 요약 비유**: 재고 차감에 AP DB를 쓰는 건 여러 계산대에서 동시에 마지막 상품을 판매하는 것이다. 손님 2명이 같은 물건을 사고 집에 가면 한 명은 빈손이다.

## Ⅴ. 기대효과 및 결론

### BASE 설계 적합 영역

| 도메인 | 일관성 모델 | 이유 |
|:---|:---|:---|
| 소셜 피드, 댓글 | BASE/AP | 좋아요 수 수초 차이 무방 |
| 장바구니 | BASE/AP | 임시 불일관성 허용 |
| 재고 관리 | ACID/CP | 초과 판매 불가 |
| 금융 이체 | ACID/CP | 원자성 필수 |

📢 **섹션 요약 비유**: 은행 계좌는 ACID(금고), 소셜 피드는 BASE(게시판)다. 금고는 느려도 확실해야 하고, 게시판은 빠르되 잠깐 틀려도 괜찮다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CAP 정리 | 이론 기반 | C/A/P 셋 중 둘만 보장 |
| ACID | 트랜잭션 모델 | CP 계열 일관성 보장 |
| BASE | 일관성 모델 | AP 계열 결과적 일관성 |
| PACELC | 확장 이론 | 정상 시 Latency vs Consistency |
| Eventual Consistency | 상태 | 시간 경과 후 일관성 수렴 |

### 📈 관련 키워드 및 발전 흐름도

```
RDB ACID 트랜잭션 - 분산 환경 확장 한계
    |
    v
CAP 정리 - 일관성·가용성·분할내성 동시 불가
    |
    v
NoSQL BASE - 결과적 일관성으로 가용성 극대화
    |
    v
CP 계열 (HBase, ZooKeeper) vs AP 계열 (Cassandra)
    |
    v
NewSQL (CockroachDB, Spanner) - ACID + 수평 확장
```

> **키워드**: CAP Theorem, BASE, ACID, NoSQL, Eventual Consistency, Partition Tolerance, NewSQL, CockroachDB

### 👶 어린이를 위한 3줄 비유 설명

1. CAP는 "맛있고 빠르고 저렴한 식당"처럼 세 가지를 동시에 다 가질 수 없다는 법칙이에요.
2. ACID는 은행 금고처럼 느리지만 확실한 것, BASE는 소문처럼 빠르지만 잠깐 틀릴 수 있는 것이에요.
3. Eventual Consistency는 "나중엔 다 같아져요"라는 약속이에요. 지금 당장은 달라도 괜찮아요.
