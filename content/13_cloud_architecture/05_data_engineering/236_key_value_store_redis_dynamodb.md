---
title: "Key Value Store Redis Dynamodb"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 236
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 키-값 저장소(Key-Value Store)는 고유한 키(Key)로 값(Value)을 O(1) 시간에 조회하는 가장 단순한 NoSQL 구조로, <strong>밀리초 이하 응답 속도</strong>가 핵심 가치다.
> 2. **가치**: Redis는 인메모리 기반으로 문자열·해시·리스트·셋·정렬셋 등 <strong>풍부한 자료구조</strong>를 제공해 세션·캐시·리더보드에, DynamoDB는 완전관리형 서버리스로 <strong>무한 확장</strong>에 적합하다.
> 3. **판단 포인트**: Redis는 단일 서버 메모리 용량이 한계이므로 대용량 영구 저장은 DynamoDB가 적합하고, 두 시스템을 <strong>DynamoDB DAX(캐시) + DynamoDB(영구)</strong>처럼 조합하는 패턴이 일반적이다.

---

## Ⅰ. 개요 및 필요성

웹 서비스에서 DB 쿼리 병목은 만성적 문제다. 매 페이지 요청마다 복잡한 SQL을 실행하면 응답이 수백ms~수초로 늘어난다. 키-값 저장소는 이 병목을 해결하는 첫 번째 방어선이다.

```
[캐시 패턴 - Cache Aside]
1. 앱 -> Redis 조회 (Cache Hit: 1ms 응답)
        v Cache Miss
2. 앱 -> DB 조회 (100ms 응답)
3. 앱 -> Redis 저장 (TTL 설정)
4. 다음 요청 -> Redis 캐시 Hit (1ms 응답)

효과: DB 부하 90%+ 감소, 응답 속도 100배 향상
```

<strong>키-값 저장소 주요 사용 사례:</strong>
- <strong>세션 관리</strong>: 로그인 사용자 세션 토큰 저장 (TTL 자동 만료)
- **캐시**: DB/API 응답 캐싱 (Cache Aside, Write-Through)
- **실시간 리더보드**: 게임 점수 랭킹 (Redis ZSet)
- <strong>분산 락</strong>: 동시성 제어 (Redlock 알고리즘)
- <strong>Rate Limiting</strong>: API 요청 속도 제한 (Sliding Window)
- **Pub/Sub**: 경량 실시간 메시지 발행/구독

📢 **섹션 요약 비유**: 키-값 저장소는 열쇠고리다. 각 열쇠(키)에 방(값)이 매핑되어 있어, 열쇠만 있으면 즉시 방을 열 수 있다. 열쇠가 없으면 방 목록 전체를 뒤져야(DB 풀스캔) 하지만, 열쇠고리는 O(1)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Redis 자료구조 및 활용 패턴

```
[Redis 5가지 핵심 자료구조]
+------------+-----------------------------------------------+
| String     | SET/GET, INCR/DECR, EXPIRE (TTL)              |
|            | 사례: 세션 토큰, 카운터, 분산 락               |
+------------+-----------------------------------------------+
| Hash       | HSET/HGET, HMGET, HGETALL                     |
|            | 사례: 사용자 프로필, 상품 정보                  |
+------------+-----------------------------------------------+
| List       | LPUSH/RPUSH, LPOP/RPOP, LRANGE                |
|            | 사례: 메시지 큐, 최근 방문 기록                 |
+------------+-----------------------------------------------+
| Set        | SADD/SMEMBERS, SUNION, SINTER                 |
|            | 사례: 유니크 방문자, 태그 교집합                |
+------------+-----------------------------------------------+
| Sorted Set | ZADD/ZRANGE, ZREVRANGEBYSCORE                 |
|  (ZSet)    | 사례: 실시간 점수 랭킹, 시간 순 이벤트          |
+------------+-----------------------------------------------+
```

### Redis 영속성 옵션

| 옵션 | 설명 | 특성 |
|:---|:---|:---|
| <strong>RDB (Snapshot)</strong> | 주기적 스냅샷 파일 저장 | 빠른 복구, 마지막 스냅샷 이후 데이터 손실 |
| <strong>AOF (Append Only File)</strong> | 모든 쓰기 명령 로그 기록 | 높은 내구성, 디스크 비용 ^ |
| **RDB + AOF 혼합** | 스냅샷 + 이후 AOF | 균형 잡힌 복구 |
| **No Persistence** | 메모리만 (순수 캐시) | 최고 성능, 재시작 시 데이터 삭제 |

### DynamoDB 아키텍처

```
[DynamoDB 핵심 개념]
테이블: users
+--------------------------------------------------------+
| Partition Key (PK): user_id  (해시 키)                  |
| Sort Key (SK): created_at    (선택적 범위 키)            |
+--------------------------------------------------------+
| {PK:"U001", SK:"2024-01-01", name:"김철수", tier:"VIP"} |
| {PK:"U001", SK:"2024-01-15", name:"김철수", tier:"VIP"} |
| {PK:"U002", SK:"2024-01-10", name:"이영희", tier:"일반"} |
+--------------------------------------------------------+

PK 기반 조회: O(1) 해시 조회
SK 기반 범위: PK 고정 + SK 범위 쿼리
GSI (Global Secondary Index): 다른 속성으로 추가 인덱스
```

### DynamoDB DAX (가속 캐시)

```
앱 -> DAX (인메모리, 마이크로초 응답)
       v Cache Miss
     DynamoDB (밀리초 응답)

DAX: DynamoDB용 인메모리 캐시 클러스터
     Redis와 유사하지만 DynamoDB API와 완전 호환
     코드 변경 없이 URL만 DAX로 변경
```

📢 **섹션 요약 비유**: DynamoDB의 PK와 SK는 주민등록 시스템이다. 주민번호(PK)로 사람을 찾고, 사건 날짜(SK)로 특정 기간 기록만 조회한다. 인덱스 없이 다른 속성으로 찾으면 전수조사(Full Scan) 해야 한다.

---

## Ⅲ. 비교 및 연결

### Redis vs DynamoDB 비교

| 비교 항목 | Redis | Amazon DynamoDB |
|:---|:---|:---|
| **스토리지 유형** | 인메모리 (+ 디스크 영속) | 분산 SSD |
| **응답 속도** | 마이크로초~밀리초 | 밀리초 |
| <strong>데이터 크기</strong> | 수십GB ~ 수TB | 무제한 |
| **비용** | 메모리 비용 | 처리량/스토리지 과금 |
| **자료구조** | 풍부 (Hash, ZSet, List…) | 단순 (Item 기반) |
| <strong>트랜잭션</strong> | 제한적 (MULTI/EXEC) | ACID (같은 파티션) |
| **관리** | 직접 관리 or Redis Cloud | 완전 관리형 (서버리스) |
| **적합 사례** | 캐시, 세션, 리더보드 | 대규모 SaaS 앱, 완전 서버리스 |

### 캐시 패턴 비교

| 패턴 | 설명 | 특성 |
|:---|:---|:---|
| <strong>Cache Aside (Lazy)</strong> | 캐시 미스 시 앱이 DB 조회 후 캐시 저장 | 가장 일반적 |
| <strong>Write-Through</strong> | 쓰기 시 캐시+DB 동시 저장 | 일관성 ^, 쓰기 지연 ^ |
| **Write-Behind** | 캐시 먼저 쓰고 비동기로 DB 저장 | 쓰기 성능 ^, 손실 위험 |
| **Read-Through** | 캐시가 DB 조회를 대행 | 캐시 계층 추상화 |

📢 **섹션 요약 비유**: Cache Aside는 편의점이 없으면 대형마트에서 가져오는 것, Write-Through는 편의점 납품할 때 창고에도 동시에 넣는 것, Write-Behind는 편의점에만 먼저 넣고 나중에 창고 정리하는 것이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### Redis 실무 명령어

```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# String: 세션 저장 (TTL 1시간)
r.setex('session:tok123', 3600, '{"user_id": "U001", "role": "admin"}')

# Hash: 사용자 프로필 (부분 업데이트)
r.hset('user:U001', mapping={'name': '김철수', 'tier': 'VIP', 'points': 5000})
r.hincrby('user:U001', 'points', 500)  # 포인트 증가

# Sorted Set: 실시간 리더보드
r.zadd('leaderboard:2024-01', {'player1': 1500, 'player2': 2300})
top10 = r.zrevrange('leaderboard:2024-01', 0, 9, withscores=True)

# 분산 락 (Redlock)
lock = r.set('lock:order_123', 'worker_1', nx=True, ex=30)
if lock:
    # 독점 작업 수행
    r.delete('lock:order_123')
```

### DynamoDB 설계 주의사항

```
[핫 파티션 방지]
문제: user_type='VIP' 파티션에 80% 트래픽 집중
해결: PK에 랜덤 접미사 추가 (Write Sharding)
     user_id#1, user_id#2, ... user_id#N

[Single Table Design 패턴]
RDB 여러 테이블을 DynamoDB 단일 테이블로 모델링
PK="USER#U001", SK="PROFILE" -> 사용자 정보
PK="USER#U001", SK="ORDER#20240115" -> 사용자의 주문
PK="ORDER#O001", SK="ITEM#P001" -> 주문의 상품
```

📢 **섹션 요약 비유**: DynamoDB Single Table Design은 다용도 가구와 같다. 여러 서랍(PK+SK 조합)이 있어 사람 정보, 주문 정보, 상품 정보를 하나의 가구(테이블)에 넣지만, 서랍 라벨(PK/SK 네이밍 규칙)을 잘 설계해야 원하는 걸 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **응답 속도 향상** | DB 대비 100~10,000배 빠른 조회 |
| **DB 부하 감소** | 반복 쿼리를 캐시에서 처리해 DB 트래픽 90%+ 감소 |
| **무한 확장** | DynamoDB: 요청량에 따른 자동 확장 |
| <strong>TTL 자동 만료</strong> | 세션 만료, 임시 데이터 자동 삭제 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **Cache Invalidation** | 캐시 무효화 시점 관리가 데이터 일관성의 핵심 과제 |
| <strong>Redis 메모리 한계</strong> | 데이터가 메모리를 초과하면 Eviction 발생 |
| <strong>DynamoDB 비용</strong> | 읽기/쓰기 단위(RCU/WCU)로 과금, 예측 어려움 |
| <strong>핫 파티션</strong> | DynamoDB PK 설계 오류 시 특정 파티션 과부하 |

📢 **섹션 요약 비유**: Redis 캐시는 책상 위 자주 보는 책이다. 책장(DB)에 가지 않아도 즉시 꺼낼 수 있지만, 책상이 꽉 차면 덜 보는 책을 치워야 한다(Eviction). 캐시 무효화는 책 내용이 바뀌면 책상의 책도 교체하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| CAP 정리 | Redis/DynamoDB의 AP 특성 (가용성 우선) |
| 캐시 패턴 | Cache Aside, Write-Through 등 캐싱 전략 |
| 세션 관리 | Redis의 핵심 사용 사례 |
| DynamoDB DAX | DynamoDB 전용 인메모리 캐시 계층 |
| 컨시스턴트 해싱 | DynamoDB 파티션 분산 메커니즘 |
| Redis Sentinel | Redis 고가용성 구성 |
| Redis Cluster | Redis 수평 확장 분산 구성 |

### 👶 어린이를 위한 3줄 비유 설명
1. 키-값 저장소는 자동 판매기와 같다. 버튼(키)을 누르면 음료(값)가 즉시 나온다. 슈퍼마켓(DB)보다 훨씬 빠르지만, 넣을 수 있는 음료 종류(데이터 구조)가 정해져 있다.

### 📈 관련 키워드 및 발전 흐름도

```text
Key-Value: O(1) 조회 · 초저지연
    +-► In-Memory: Redis · Memcached (캐시)
    +-► Persistent: DynamoDB · etcd (영속)
    |
    v
활용: 세션 · 캐시 · 설정 · 분산 락
```
2. Redis는 교실 앞 칠판이다. 자주 필요한 내용을 칠판(메모리)에 적어두면 교과서(DB)를 매번 찾을 필요가 없다. 단, 칠판 크기(메모리)는 정해져 있다.
3. DynamoDB는 무제한 자동 창고다. 물건이 아무리 많아도 자동으로 공간이 늘어나고(서버리스 확장), 바코드(키)로 즉시 찾을 수 있지만, 바코드 분류 체계(PK/SK 설계)를 잘 만들어야 한다.
