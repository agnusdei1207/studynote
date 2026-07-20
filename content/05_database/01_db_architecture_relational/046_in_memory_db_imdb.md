---
title: "In-Memory Database"
date: "2026-04-05"
tags:
  - "studynote-database"
weight: 46
---
> **핵심 인사이트**
> 1. 인메모리 DB(IMDB)는 모든 데이터를 RAM에 상주시켜 디스크 I/O를 완전 제거 — 전통 디스크 기반 DB 대비 10~1,000배 빠른 응답(마이크로초 단위)을 달성하며, 트랜잭션 처리(OLTP), 캐싱, 실시간 분석에서 핵심 역할을 한다.
> 2. IMDB의 핵심 과제는 내구성(Durability) 확보 — 전원 장애 시 RAM 데이터 소실을 방지하기 위해 WAL(Write-Ahead Logging), 스냅샷, 배터리 백업 RAM(NVRAM) 등을 활용하며, Redis의 RDB/AOF가 대표적 해결책이다.
> 3. RAM 가격 하락과 DRAM 용량 증가로 IMDB 적용 범위 확대 — 수TB RAM 서버 등장으로 전통 DW 워크로드까지 IMDB로 처리 가능해졌으며, SAP HANA, VoltDB, Redis Enterprise가 이 영역을 선도한다.

---

## Ⅰ. IMDB 개요

```
IMDB vs 전통 디스크 DB:

전통 DB (디스크 기반):
  데이터: 디스크 (HDD: ms, SSD: us)
  처리: 디스크 읽기 -> 버퍼 풀 -> CPU

  병목: 디스크 I/O (랜덤 읽기 HDD: ~10ms)

  예: MySQL SELECT -> 100ms (캐시 미스)

IMDB (메모리 기반):
  데이터: 완전히 RAM에 상주
  처리: RAM 직접 접근 -> CPU

  RAM 접근: ~100ns (HDD 대비 100,000×)

  예: Redis GET -> ~10-100μs

성능 비교:
  HDD: 100 IOPS
  SSD: 100,000 IOPS
  DRAM: 100,000,000+ "IOPS"

IMDB 유형:
  1. 전용 인메모리 (Pure IMDB):
     Redis, Memcached, VoltDB

  2. 인메모리 옵션 (Hybrid):
     MySQL Memory Engine
     SAP HANA (주로 IMDB)

  3. 클라우드 인메모리:
     Amazon ElastiCache (Redis/Memcached)
     Azure Cache for Redis
     Google Cloud Memorystore

RAM 비용:
  DRAM 32GB: ~$50~100 (2024)
  -> 수십~수백 GB IMDB = 수백~수천만원
  -> 성능 이점 대비 비용 효과적
```

> 📢 **섹션 요약 비유**: IMDB는 책상 위 노트 vs 책장 창고 — 책장(디스크)에서 책 꺼내기(ms) vs 이미 책상(RAM)에 펼쳐진 노트 보기(μs). 1,000배 빠른 차이!

---

## Ⅱ. 내구성 메커니즘

```
IMDB 내구성 (Durability) 문제:
  RAM = 휘발성 -> 전원 장애 -> 데이터 소실

Redis 내구성 옵션:

1. RDB (Redis Database Snapshot):
   주기적으로 디스크에 스냅샷 저장

   예: 5분마다 또는 100개 변경마다
   파일: dump.rdb

   장점: 파일 작음, 복구 빠름
   단점: 마지막 스냅샷 이후 데이터 손실 가능

   RPO: 최대 5분 데이터 손실

2. AOF (Append-Only File):
   모든 쓰기 명령을 로그 파일에 추가

   파일: appendonly.aof

   fsync 옵션:
   - always: 매 명령 -> 가장 안전 (성능 v)
   - everysec: 1초마다 -> 균형 (기본)
   - no: OS에 위임 -> 가장 빠름

   RPO: everysec = 최대 1초 데이터 손실

   단점: 파일 크기 증가 (주기적 rewrite)

3. RDB + AOF 혼합:
   AOF에 RDB 스냅샷 포함 (Redis 4+)
   재시작 빠름 + AOF 보호

4. Redis Cluster + Replica:
   Master-Replica 복제
   Master 장애 -> Replica 자동 승격
   -> RPO ≈ 0 (비동기 복제 시 소량 손실)

VoltDB:
  ACID 트랜잭션 완전 지원 IMDB
  2PC (2-Phase Commit)
  K-Safety: 노드 장애 대비 복제
  WAL -> 영구 스토리지
```

> 📢 **섹션 요약 비유**: IMDB 내구성은 노트 백업 — 책상 노트(RAM)는 지진(전원장애)에 사라지므로, 주기적으로 사진(스냅샷=RDB) 찍거나 모든 수정 기록(AOF) 유지!

---

## Ⅲ. 데이터 구조와 활용

```
Redis 데이터 구조:

String: 문자열
  SET user:1 "Alice"
  GET user:1 -> "Alice"
  INCR counter -> 원자적 증가
  사용: 캐싱, 카운터, 세션

List: 연결 리스트
  LPUSH queue "task1"
  RPOP queue
  사용: 큐, 스택, 최근 항목

Hash: 필드-값 맵
  HSET user:1 name "Alice" age 30
  HGETALL user:1
  사용: 객체 저장

Set: 중복 없는 집합
  SADD online_users "u1" "u2"
  SISMEMBER online_users "u1"
  사용: 태그, 좋아요, 팔로워

Sorted Set (ZSet): 점수 기반 정렬 집합
  ZADD leaderboard 1500 "Alice"
  ZRANGE leaderboard 0 9 WITHSCORES
  사용: 리더보드, 우선순위 큐

Geospatial:
  GEOADD locations 127.0 37.5 "Seoul"
  GEODIST locations "Seoul" "Busan"
  사용: 위치 기반 서비스

HyperLogLog:
  PFADD visitors "user1" "user2"
  PFCOUNT visitors -> 근사 고유 카운트
  사용: 대규모 카디널리티 추정 (12KB로!)

Streams:
  XADD events * type "click" page "/home"
  XREAD streams events 0
  사용: 이벤트 스트리밍, 로그
```

> 📢 **섹션 요약 비유**: Redis 데이터 구조는 다용도 도구 세트 — String(메모장), List(할일 목록), Hash(명함), Set(친구 목록), ZSet(순위표). 상황에 맞는 도구 선택!

---

## Ⅳ. 캐싱 전략

```
IMDB 캐싱 패턴:

Cache-Aside (Look-Aside, Lazy Loading):
  가장 일반적

  읽기:
  앱 -> 캐시(Redis) 확인
  히트: 캐시에서 반환
  미스: DB 조회 -> 캐시 저장 -> 반환

  쓰기:
  앱 -> DB 갱신 -> 캐시 삭제 (또는 무효화)

  장점: 필요한 것만 캐싱 (필요 시 로드)
  단점: 첫 요청 느림 (Cache Miss)

Write-Through:
  쓰기: DB + 캐시 동시 갱신
  읽기: 캐시에서만

  장점: 캐시 항상 최신
  단점: 쓰기 지연 (2번 쓰기)

Write-Behind (Write-Back):
  쓰기: 캐시만 갱신 (비동기 DB 반영)

  장점: 쓰기 속도 빠름
  단점: DB 동기화 지연, 캐시 장애 시 손실

TTL (Time-To-Live):
  캐시 만료 시간 설정
  SET session:xyz "data" EX 3600  # 1시간

  너무 짧은 TTL: 캐시 효율 낮음
  너무 긴 TTL: 오래된 데이터 제공

Thundering Herd (Cache Stampede):
  대량 캐시 동시 만료 -> DB 과부하

  해결:
  - TTL 지터(랜덤 분산)
  - 캐시 갱신 잠금 (단일 프로세스만)
  - 소프트 TTL + 하드 TTL 이중 구조
```

> 📢 **섹션 요약 비유**: 캐싱 전략은 음식 보관 방법 — Cache-Aside는 먹을 때만 냉장고 확인, Write-Through는 만들자마자 냉동+냉장 동시, Write-Back은 일단 냉장고만!

---

## Ⅴ. 실무 시나리오 — 전자상거래 캐싱 아키텍처

```
전자상거래 Redis 캐싱 아키텍처:

대상 데이터:
  상품 정보: 변경 드물음 (TTL 1시간)
  재고 현황: 자주 변경 (TTL 10초)
  사용자 세션: 30분 TTL
  리더보드: 판매 순위 (실시간)

아키텍처:

[사용자]
   v 요청
[API 서버] -> Redis Cluster
   v 캐시 미스
[MySQL/DynamoDB]

상품 캐시:
  HSET product:12345 name "운동화" price "89000" stock "50"
  EXPIRE product:12345 3600

  히트율 목표: 95% (캐시 미스 5%만 DB)

세션 관리:
  SET session:abc123 (JSON 직렬화) EX 1800
  EXPIRE session:abc123 1800 (요청마다 갱신)

재고 실시간:
  DECR product:12345:stock  (원자적 감소)
  -> 재고 0 -> 품절 처리
  (DB에 비동기 반영)

리더보드:
  ZADD sales:rank:daily <판매량> <상품ID>
  ZREVRANGE sales:rank:daily 0 9 WITHSCORES
  -> 실시간 TOP 10

Redis Cluster 구성:
  3 Master × 2 Replica = 6 노드
  자동 샤딩 (16,384 슬롯)
  장애 자동 페일오버

결과:
  DB 쿼리: 초당 10만 -> 5천 (95% 절감)
  응답 시간: 150ms -> 8ms
  DB CPU: 90% -> 35%
  Flash Sale 트래픽 (초당 100만 요청) 처리
```

> 📢 **섹션 요약 비유**: 전자상거래 Redis는 빠른 계산원 — DB(창고)에서 물건 꺼내는 대신, 자주 팔리는 상품(캐시)을 계산대(Redis) 앞에 미리 배치. 줄 서는 시간(응답) 1/20!

---

## 📌 관련 개념 맵

```
인메모리 DB (IMDB)
+-- 대표 제품
|   +-- Redis (다구조, 캐시+메시징)
|   +-- Memcached (단순 캐시)
|   +-- SAP HANA (엔터프라이즈 IMDB)
|   +-- VoltDB (ACID IMDB)
+-- 내구성
|   +-- RDB 스냅샷
|   +-- AOF 로그
|   +-- Replica 복제
+-- 캐싱 패턴
|   +-- Cache-Aside (Lazy)
|   +-- Write-Through
|   +-- Write-Behind
+-- 데이터 구조
    +-- String, List, Hash, Set
    +-- Sorted Set, HyperLogLog, Streams
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[IMDB 초기 연구 (1980s)]
메모리 가격 높음
제한적 특수 목적 사용
      |
      v
[Memcached (2003)]
웹 캐싱 표준
Facebook 대규모 도입
      |
      v
[Redis (2009)]
다양한 데이터 구조
내구성 옵션 추가
      |
      v
[RAM 가격 하락 (2010s~)]
SAP HANA: 대용량 IMDB
OLAP도 IMDB 가능
      |
      v
[현재: 클라우드 IMDB]
ElastiCache, Azure Cache
Redis Enterprise: 멀티티어
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. IMDB는 책상 위 필기 — 창고(디스크)에서 책 꺼내기 대신 이미 책상(RAM)에 펼쳐진 노트. 1,000배 빨리 읽을 수 있어요!
2. Redis 내구성은 노트 사진 찍기 — 책상 노트(RAM)가 지워지면 안 되니 주기적으로 사진(스냅샷) 찍고 수정 기록(AOF) 저장!
3. 캐시 히트는 신나는 빠름 — 95% 요청이 캐시에서 해결되면 DB는 5%만 일해요. 요청 20배 많아도 DB가 안 힘들어요!
