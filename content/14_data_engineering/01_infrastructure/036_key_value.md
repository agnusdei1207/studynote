---
title: "Key-Value Store"
date: "2026-03-03"
tags:
  - "studynote-data-engineering"
weight: 36
---
> **핵심 인사이트**
> 1. 키-값 저장소(Key-Value Store)는 고유한 키(Key)에 임의의 값(Value)을 연결해 저장하는 가장 단순한 NoSQL 구조로, 해시 테이블의 분산·영속화 버전이다.
> 2. 단순한 구조 덕분에 O(1) 조회 성능을 달성할 수 있으며, 수평 확장(Sharding)과 레플리케이션이 용이해 세션 저장·캐시·실시간 카운터 등 초저지연이 요구되는 워크로드에 최적이다.
> 3. Redis(메모리 기반 + 영속화)와 DynamoDB(분산 + 서버리스)가 각각 캐시 계층과 글로벌 확장 서비스에서 사실상 표준이며, 선택은 일관성·지연·확장성 요건에 따라 결정한다.

---

## I. 키-값 저장소 원리

```
구조: 해시 맵의 분산 영속화 버전

key: "session:user_1234"
value: {"user_id":1234, "username":"홍길동", "role":"admin", "exp":1735689600}

기본 연산:
  SET key value           <- O(1)
  GET key                 <- O(1)
  DEL key                 <- O(1)
  EXISTS key              <- O(1)
  EXPIRE key seconds      <- TTL 설정

특징:
  - 키: 임의 문자열 (최대 512MB, Redis 기준)
  - 값: 문자열, JSON, 바이너리 등 임의 형식
  - 스키마 없음 (Schema-less)
```

> 📢 **섹션 요약 비유**: 사물함 보관소 — 고유 번호(키)만 알면 내용물(값)을 즉시 꺼낼 수 있다. 내용물 형식은 자유.

---

## II. Redis — 인메모리 키-값 저장소

```
Redis (Remote Dictionary Server) 특성:

메모리 기반 (초고속):
  10만 TPS 이상, 1ms 미만 응답

데이터 구조 (단순 키-값 넘어서):
  String: SET/GET (캐시, 카운터)
  List:   LPUSH/RPUSH (큐, 스택)
  Set:    SADD/SMEMBERS (고유 방문자)
  Sorted Set: ZADD/ZRANGE (리더보드)
  Hash:   HSET/HGET (사용자 프로필)
  Stream: XADD (이벤트 로그)

영속화 (Durability):
  RDB: 주기적 스냅샷 (성능 우선)
  AOF: 모든 쓰기 로그 (데이터 안전 우선)
```

| 사용 패턴       | Redis 자료구조  | 명령           |
|--------------|--------------|---------------|
| 세션 저장      | String + TTL  | SET + EXPIRE  |
| 실시간 카운터  | String        | INCR          |
| 중복 제거      | Set           | SADD          |
| 리더보드       | Sorted Set    | ZADD + ZRANGE |
| 메시지 큐      | List          | LPUSH + BRPOP |

> 📢 **섹션 요약 비유**: Redis는 스위스 군용 칼 — 문자열만 저장하는 단순 사물함에서 순위표·큐·이벤트 로그까지 여러 도구가 담겨있다.

---

## III. DynamoDB — 서버리스 분산 키-값

```
DynamoDB 특성:
  완전 관리형 (서버리스)
  단일 자릿수 밀리초 응답
  자동 수평 확장 (수천 TPS -> 수백만 TPS)

  기본 키 설계:
  - Partition Key (PK): 데이터 분산 키
  - Sort Key (SK): 파티션 내 정렬 (선택)

  예시 설계:
  PK: "USER#1234"
  SK: "ORDER#2024-01-01"
  -> 단일 사용자의 모든 주문을 효율적으로 쿼리
```

| 비교       | Redis           | DynamoDB          |
|-----------|-----------------|-------------------|
| 저장 위치  | 메모리 (주) + 디스크| 디스크 (SSD)    |
| 지연       | < 1 ms          | 1-9 ms            |
| 확장       | 클러스터 수동 설정| 완전 자동          |
| 비용 모델  | 인스턴스         | 요청/스토리지 종량제|
| 일관성     | 최종 일관성      | 강한/최종 일관성 선택|

> 📢 **섹션 요약 비유**: Redis는 빠른 현금 서랍(메모리), DynamoDB는 자동 확장 디지털 금고(클라우드) — 속도와 확장성의 트레이드오프.

---

## IV. 캐시 패턴

```
1. Cache-Aside (Lazy Loading):
   앱 -> Redis에 요청
   Redis 미스 -> DB 쿼리 -> Redis에 저장 -> 반환

2. Write-Through:
   쓰기 시 DB와 캐시에 동시 저장
   항상 캐시와 DB 동기화

3. Write-Behind:
   쓰기 시 캐시에만 저장
   비동기로 DB 반영 (고성능, 데이터 손실 위험)

4. TTL (Time To Live):
   SET session:1234 {...} EX 3600
   1시간 후 자동 만료
```

> 📢 **섹션 요약 비유**: Cache-Aside는 책장에서 찾고 없으면 도서관 가는 것, Write-Through는 빌릴 때 바로 복사해 책장에 꽂는 것.

---

## V. 실무 시나리오 — 이커머스 캐시 아키텍처

```
이커머스 Redis 사용 패턴:

1. 세션: SET session:{token} {json} EX 1800
2. 상품 캐시: SET product:{id} {json} EX 3600
3. 재고 카운터: DECR stock:{product_id}
4. 장바구니: HSET cart:{user_id} {product_id} {qty}
5. 인기 상품: ZINCRBY popular:daily {product_id} 1
6. 속도 제한: INCR rate:{ip}:{minute} + EXPIRE
7. 분산 락: SET lock:{resource} {uuid} NX EX 30
```

> 📢 **섹션 요약 비유**: 이커머스에서 Redis가 없으면 초당 수만 건의 상품 조회를 모두 DB에서 읽어야 한다 — Redis가 DB의 방패막이.

---

## 📌 관련 개념 맵

```
키-값 저장소
+-- Redis (인메모리)
|   +-- 자료구조: String/List/Set/ZSet/Hash
|   +-- 영속화: RDB / AOF
|   +-- 클러스터: 샤딩 + 레플리케이션
+-- DynamoDB (서버리스)
|   +-- PK + SK 설계
|   +-- 자동 확장
|   +-- GSI (글로벌 보조 인덱스)
+-- 캐시 패턴
|   +-- Cache-Aside / Write-Through / Write-Behind
|   +-- TTL (만료 시간)
+-- 관련 NoSQL
    +-- Memcached (단순 캐시)
    +-- Cassandra (열 기반)
    +-- Aerospike (인메모리 + NVMe)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 캐시 기술]
Memcached (2003): 단순 메모리 캐시
      |
      v
[Redis 등장 (2009)]
인메모리 + 다양한 자료구조 + 영속화
Memcached를 대부분 대체
      |
      v
[DynamoDB (Amazon, 2012)]
서버리스 분산 키-값 서비스
      |
      v
[Redis Enterprise / Redis Cloud]
글로벌 분산 Redis, Active-Active
      |
      v
[현재: Redis Stack + AI 기능]
Vector 검색, JSON, TimeSeries 내장
AI 임베딩 벡터 저장소로 활용
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 키-값 저장소는 열쇠(키)만 있으면 해당 사물함(값)을 즉시 열 수 있는 자물쇠 보관함이에요.
2. Redis는 메모리에 저장해서 엄청 빠르고, DynamoDB는 클라우드에서 자동으로 커지는 금고예요.
3. 쇼핑몰에서 상품 정보를 매번 데이터베이스에서 읽지 않고 Redis에 잠깐 저장해두면 훨씬 빠르답니다!
