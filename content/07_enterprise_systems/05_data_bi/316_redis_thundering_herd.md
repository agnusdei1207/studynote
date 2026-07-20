---
title: "Redis Thundering Herd"
date: "2026-05-09"
tags:
  - "studynote-enterprise-systems"
weight: 316
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 선더링 허드 (Thundering Herd)는 캐시 만료(Cache Expiration) 또는 장애 시 다수의 클라이언트가 동시에 DB에 요청을 쏟아내어 DB가 다운되는 현상으로, Redis (레디스) 캐시 기반 시스템에서 반드시 사전 설계가 필요한 장애 패턴이다.
> 2. **가치**: 캐시 만료 분산 (Cache Expiry Jitter), 캐시 잠금 (Cache Lock / Mutex), 조기 갱신 (Probabilistic Early Expiration), Pub/Sub 기반 캐시 워밍 전략으로 선더링 허드를 방지할 수 있다.
> 3. **판단 포인트**: 캐시 스탬피드 (Cache Stampede)를 방지하기 위한 TTL (Time To Live, 생존 시간) 설계와 만료 분산 전략은 Redis 기반 고트래픽 서비스 설계의 핵심 요소다.

---

## Ⅰ. 개요 및 필요성

Redis는 인메모리 키-값 캐시로 DB 앞단에 위치하여 반복적인 조회 요청을 DB 없이 처리한다. 캐시 히트율 (Cache Hit Ratio)이 99%라면 DB는 1%의 요청만 처리하면 된다. 그런데 이 캐시가 만료되거나 장애가 발생하면, 평소 1%만 받던 DB가 갑자기 100%의 요청을 받아 과부하로 다운된다.

이것이 선더링 허드다. 유명 이벤트 시작(티켓 판매 오픈, 방송 시작)처럼 많은 사용자가 동시에 몰리는 순간 캐시 TTL이 만료되면, 수만 개의 요청이 동시에 DB를 직접 조회하는 폭발적 부하(Cache Stampede)가 발생한다.

- **📢 섹션 요약 비유**: 선더링 허드는 인기 식당 웨이팅 명단이 갑자기 사라졌을 때 모든 손님이 동시에 입구로 달려오는 상황이다. 대기 명단(캐시)이 없어지면 혼란이 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+------------------------------------------------------------------+
|            Redis 선더링 허드 발생 메커니즘과 방지 전략               |
+------------------------------------------------------------------+
|  발생 과정:                                                        |
|  T=0: 수만 클라이언트 -> Redis 캐시 조회 (HIT)                       |
|  T=TTL: Redis 캐시 만료                                            |
|  T=TTL+1ms: 모든 클라이언트 -> Redis MISS -> DB 직접 조회 (폭발!)    |
|                                                                  |
|  방지 전략 1: TTL Jitter (만료 분산)                               |
|  TTL = base_ttl + random(0, jitter)                              |
|  같은 시간에 모든 키가 만료되지 않도록 무작위 분산                    |
|                                                                  |
|  방지 전략 2: Cache Lock (Mutex)                                   |
|  캐시 MISS -> SET NX (원자적 락 획득) -> DB 조회 -> 캐시 저장 -> 락 해제|
|  다른 클라이언트: 락 대기 중 -> 캐시 완성 후 -> Redis 재조회          |
|                                                                  |
|  방지 전략 3: Probabilistic Early Expiration                       |
|  TTL 만료 전, 남은 시간이 임계값 이하이면 일부 요청이 미리 캐시 갱신   |
|  -> 만료 전 백그라운드 갱신으로 만료 순간 폭발 방지                    |
+------------------------------------------------------------------+
```

| 전략                          | 원리                         | 장단점                          |
|:-----------------------------|:----------------------------|:-------------------------------|
| TTL Jitter                   | 만료 시간 무작위 분산          | 간단, 완전한 방지는 아님          |
| Cache Lock (Mutex)           | 첫 요청만 DB 조회, 나머지 대기 | 확실한 방지, 대기 레이턴시 발생    |
| Probabilistic Early Expiration | 만료 전 확률적 선제 갱신      | 낮은 레이턴시, 구현 복잡도 있음   |
| Cache Warming                 | 배포/이벤트 전 캐시 미리 채움  | 이벤트 예측 가능 시 가장 효과적   |

- **📢 섹션 요약 비유**: TTL Jitter는 학생들 하교 시간을 학년별로 다르게 해서 교문 앞 혼잡을 막는 것이다. Cache Lock은 교문에 안내원 1명만 두고 나머지는 줄 세우는 방식이다.

---

## Ⅲ. 비교 및 연결

**캐시 장애 유형 비교**:
- Cache Stampede (선더링 허드): 동시 만료로 DB 폭발
- Cache Avalanche (캐시 사태): 다수 캐시 키가 동시에 만료 -> 대규모 DB 부하
- Cache Penetration (캐시 침투): 존재하지 않는 키를 계속 조회 -> DB 반복 조회

| 장애 유형          | 원인                          | 방지 전략                         |
|:----------------|:-----------------------------|:---------------------------------|
| Cache Stampede  | 단일 인기 키 동시 만료           | Cache Lock, TTL Jitter            |
| Cache Avalanche | 다수 키 동시 만료               | TTL 분산, 영구 캐시                |
| Cache Penetration| 없는 키 반복 조회               | Null Cache, Bloom Filter          |

- **📢 섹션 요약 비유**: Cache Stampede는 인기 제품 재입고 알림이 같은 시간에 나가서 모두가 동시에 클릭하는 현상, Cache Avalanche는 여러 제품이 동시에 품절되는 현상이다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>Redis 선더링 허드 방지 구현 패턴</strong> (의사코드):

```python
# Cache Lock (Mutex) 패턴
def get_data(key):
    value = redis.get(key)
    if value:
        return value
    # 락 획득 시도 (SET NX EX: 원자적 SET if Not eXists, EXpire)
    lock_acquired = redis.set(f"lock:{key}", 1, nx=True, ex=5)
    if lock_acquired:
        value = db.query(key)
        redis.set(key, value, ex=TTL)
        redis.delete(f"lock:{key}")
        return value
    else:
        # 다른 요청이 락 보유 중 -> 짧게 대기 후 재시도
        time.sleep(0.05)
        return redis.get(key)
```

<strong>Redis 클러스터 설계 시 주의</strong>:
- Hot Key Problem: 단일 키에 트래픽 집중 -> 샤딩 키 분산 또는 로컬 캐시 (L1 Cache) 병행
- Redis Sentinel vs Cluster: 단일 마스터 HA (Sentinel), 수평 확장 (Cluster)
- Eviction Policy 선택: `allkeys-lru`, `volatile-lru` 등 메모리 용량 초과 시 정책 명확히 설정

- **📢 섹션 요약 비유**: Redis Cache Lock은 인기 식당에서 한 명씩만 주방에 들어가도록 대기표를 주는 것이다. 무질서하게 모두 달려들면 주방(DB)이 마비된다.

---

## Ⅴ. 기대효과 및 결론

선더링 허드 방지 전략을 적절히 설계하면 트래픽 스파이크 상황에서 DB 과부하를 방지하고, 서비스 가용성을 유지할 수 있다. TTL Jitter와 Cache Lock을 결합하면 대부분의 캐시 스탬피드 시나리오를 방어할 수 있다.

더 나아가 Redis 클러스터, 읽기 복제본(Replica), 로컬 캐시(L1 Cache) 계층을 추가하면 단일 Redis 인스턴스 장애에도 서비스 연속성을 유지할 수 있다. 캐시 전략은 단순히 "캐시를 둔다"가 아니라, 장애 모드를 사전에 설계하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 선더링 허드 방지는 불이 나기 전에 스프링클러를 설치하는 것이다. 불이 나고 나서(장애 발생 후) 설치하면 이미 늦다.

---

### 📌 관련 개념 맵

| 개념                          | 연결 포인트                              |
|:-----------------------------|:----------------------------------------|
| Cache Stampede                | 동시 만료로 발생하는 DB 폭발 패턴          |
| SET NX (Set if Not eXists)   | Redis 원자적 캐시 락 구현 핵심 명령어     |
| TTL Jitter                    | 만료 시간 분산으로 동시 만료 방지         |
| Cache Avalanche / Penetration | 캐시 장애 유형 3가지                     |
| Hot Key Problem               | 단일 키 집중 트래픽 분산 전략            |

### 📈 관련 키워드 및 발전 흐름도

```
DB 직접 조회 병목 -> Redis 캐시 도입
    |
    v
TTL 만료 동시 발생 -> Cache Stampede 장애
    |
    v
TTL Jitter / Cache Lock / Early Expiration 도입
    |
    v
Redis Cluster + Replica + 로컬 L1 캐시 계층화
    |
    v
분산 캐시 관리 자동화 (Cache Warming, Proactive Refresh)
```

### 👶 어린이를 위한 3줄 비유 설명

1. Redis는 자주 찾는 정보를 빠른 메모장(캐시)에 적어두는 것이에요. 없어지면 원래 책(DB)을 다시 찾아야 해요.
2. 선더링 허드는 메모장이 갑자기 지워졌을 때 모든 사람이 동시에 책을 펼치면 책장이 무너지는 현상이에요.
3. 해결책은 메모장 유효기간을 조금씩 다르게 설정하거나, 한 명이 책을 찾는 동안 나머지는 기다리는 규칙을 만드는 거예요!
