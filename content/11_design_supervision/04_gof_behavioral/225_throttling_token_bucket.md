---
title: "Throttling / Token Bucket Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 225
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Token Bucket (토큰 버킷) 알고리즘은 초당 R개 토큰이 버킷에 채워지고 요청마다 토큰을 소비하는 방식으로 API 호출 속도를 제어하는 Rate Limiting (속도 제한) 알고리즘이다 — 버스트(Burst) 트래픽을 버킷 용량(B) 한도 내에서 허용한다.
> 2. **가치**: 토큰이 있으면 즉시 처리(버스트 허용), 토큰이 없으면 요청 거부 또는 대기 — 평균 처리량을 R rps (Requests Per Second)로 제한하면서도 순간 폭발 트래픽에 유연하게 대응한다.
> 3. **판단 포인트**: 토큰 버킷은 버스트 허용 + 평균 속도 제한, 리키 버킷(Leaky Bucket)은 버스트 흡수 + 일정 속도 출력 — 두 알고리즘의 차이가 Rate Limiting 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성
API 서버 없이 무제한 요청을 허용하면:
- DDoS 공격에 취약 (악의적 대량 요청)
- 특정 클라이언트의 과도 사용으로 다른 클라이언트 피해
- 백엔드 DB/서비스 과부하 -> 전체 서비스 다운

<strong>Rate Limiting (속도 제한) 적용 목적</strong>:
- 공정한 자원 배분 (Fair Usage)
- DoS/DDoS 방어
- 서비스 안정성 보장 (SLA)
- 요금 과금 기준 (유료 API 플랜)

| 알고리즘 | 특징 | 버스트 허용 | 구현 복잡도 |
|:---|:---|:---|:---|
| Fixed Window Counter | 시간 창(Window)에서 카운팅 | 제한적 | 단순 |
| Sliding Window Log | 정확한 슬라이딩 윈도우 | 없음 | 복잡, 메모리 많음 |
| Sliding Window Counter | 근사 슬라이딩 윈도우 | 제한적 | 중간 |
| **Token Bucket** | **토큰 소비 방식** | **허용** | **중간** |
| Leaky Bucket | 큐를 통한 일정 속도 출력 | 흡수 후 평활화 | 중간 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: Rate Limiting은 놀이공원 입장 관리 — 아무리 많은 손님이 몰려도 회전문이 초당 R명만 통과시키고, 토큰 버킷은 대기열에 R명씩 들어가는 입장권(토큰)을 주는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+-------------------------------------------------------------+
|                   Token Bucket Algorithm                    |
|                                                             |
|  토큰 생성:                                                   |
|    초당 R개 토큰 추가 ----->  +------------------+            |
|    (Rate Refill)            |    Token Bucket   |            |
|                             |  [T][T][T][T][T]  |            |
|                             |  capacity = B개   |            |
|                             +--------+---------+            |
|                                      |                       |
|  요청 처리:                            |                       |
|    +----------+  토큰 있음?  토큰 소비  |                       |
|    | Request  |-------------> (1개 차감) +--->  처리(200 OK)    |
|    +----------+                                             |
|         |        토큰 없음                                    |
|         +------------------------------>  거부(429 Too Many) |
|                                                             |
|  파라미터:                                                    |
|    R (Rate): 초당 토큰 충전 속도                               |
|    B (Bucket): 버킷 최대 용량 (최대 버스트 크기)               |
+-------------------------------------------------------------+
```

```
Token Bucket (토큰 버킷):
  입력:  [burst][burst][burst]···[quiet]···
  처리:  [burst][burst][burst]···[quiet]···
  -> 버킷에 토큰이 있으면 버스트 즉시 처리
  -> 버킷 비면 거부 (거부 또는 대기)

Leaky Bucket (리키 버킷):
  입력:  [burst][burst][burst]···[quiet]···
  처리:  [▬][▬][▬][▬][▬][▬][▬]···  (일정 속도)
  -> 버스트를 버킷에 흡수하고 일정 속도로 '새어 나옴'
  -> 버킷 넘침 시 패킷 드롭
```

```
AWS API Gateway 쓰로틀링 설정:
  Rate (속도):  초당 요청 수 (rps)
  Burst:        순간 최대 요청 수 (버킷 크기)

예시:
  Rate  = 100 rps (초당 100개 토큰 충전)
  Burst = 500     (버킷 용량, 최대 버스트)

  -> 평시: 초당 100 요청 처리
  -> 갑자기 500 요청: 버킷에 토큰 남아있으면 즉시 처리
  -> 500 초과: 429 Too Many Requests 반환
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 토큰 버킷은 지하철 개찰구 — 평소에는 통행권(토큰)이 쌓이고, 출근 시간 러시(버스트)에는 모아둔 통행권을 한번에 써서 처리하고, 통행권이 다 소진되면 다음 통행권이 쌓일 때까지 대기한다.

---

## Ⅲ. 비교 및 연결
| HTTP 상태 코드 | 의미 | 헤더 |
|:---|:---|:---|
| 200 OK | 요청 처리 성공 | X-RateLimit-Remaining: 99 |
| 429 Too Many Requests | 속도 제한 초과 | Retry-After: 60 |
| 503 Service Unavailable | 서버 과부하 | — |

표준 응답 헤더:
```
X-RateLimit-Limit:     100    (최대 허용 요청 수)
X-RateLimit-Remaining: 73     (남은 요청 수)
X-RateLimit-Reset:     1716000000 (리셋 시각, Unix timestamp)
Retry-After:           30     (재시도 권장 대기 시간, 초)
```

단일 서버에서는 메모리 카운터로 Rate Limiting이 간단하지만, 수평 확장(다중 서버) 환경에서는 중앙 저장소가 필요하다:

```lua
-- Redis Lua 스크립트 (원자적 Token Bucket)
local key       = KEYS[1]           -- "rate:user:123"
local capacity  = tonumber(ARGV[1]) -- 버킷 크기
local refill    = tonumber(ARGV[2]) -- 초당 토큰 충전
local now       = tonumber(ARGV[3]) -- 현재 시각 (ms)
local requested = tonumber(ARGV[4]) -- 요청 토큰 수

local last_tokens = tonumber(redis.call("HGET", key, "tokens") or capacity)
local last_time   = tonumber(redis.call("HGET", key, "ts") or now)

local elapsed = math.max(0, now - last_time) / 1000.0  -- 경과 초
local tokens  = math.min(capacity, last_tokens + elapsed * refill)

if tokens >= requested then
    tokens = tokens - requested
    redis.call("HMSET", key, "tokens", tokens, "ts", now)
    redis.call("EXPIRE", key, math.ceil(capacity / refill) + 1)
    return 1  -- 허용
else
    return 0  -- 거부
end
```

| 수준 | 키 | 설명 |
|:---|:---|:---|
| 전역 (Global) | — | 전체 시스템 트래픽 상한 |
| IP 기반 | `rate:ip:{ip}` | DDoS/스크래핑 방어 |
| 사용자 기반 | `rate:user:{userId}` | 공정 사용 |
| API 키 기반 | `rate:apikey:{key}` | 유료 플랜별 제한 |
| 엔드포인트 기반 | `rate:ep:{endpoint}` | 민감 API 보호 |

- **📢 섹션 요약 비유**: 분산 Rate Limiting은 멀티 지점 은행의 계좌 잔액 관리 — 어느 지점(서버)에서 출금해도 중앙 DB(Redis)에서 잔액(토큰)을 공유하므로 같은 규칙이 적용된다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```java
@Component
public class RateLimitFilter extends OncePerRequestFilter {
    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {
        String userId = extractUserId(request);
        Bucket bucket = buckets.computeIfAbsent(userId, k ->
            Bucket.builder()
                .addLimit(Bandwidth.classic(100, Refill.greedy(100, Duration.ofMinutes(1))))
                .build()
        );

        if (bucket.tryConsume(1)) {
            chain.doFilter(request, response);
        } else {
            response.setStatus(429);
            response.setHeader("Retry-After", "60");
            response.getWriter().write("{\"error\": \"Rate limit exceeded\"}");
        }
    }
}
```

| 서비스 유형 | Rate (rps) | Burst | 설명 |
|:---|:---|:---|:---|
| 무료 API | 10 | 50 | 기본 공정 사용 보장 |
| 유료 기본 플랜 | 100 | 500 | 대부분 서비스 적합 |
| 엔터프라이즈 | 1,000+ | 5,000+ | SLA 계약에 따라 |
| 관리자 API | 10 | 20 | 민감 엔드포인트 보호 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: Rate Limiting 파라미터 설정은 고속도로 속도 제한 설계 — 일반 도로(무료 API)는 60km/h, 고속도로(유료 API)는 110km/h로 다르게 설정하고, 단속 카메라(Redis)가 모든 톨게이트(서버)에서 동일하게 적용한다.

---

## Ⅴ. 기대효과 및 결론
Token Bucket 기반 Rate Limiting은 API 게이트웨이의 필수 구성 요소다:

**기대효과**:
- **공정한 자원 배분**: 특정 클라이언트의 자원 독점 방지
- **DDoS 방어**: 악의적 대량 요청 차단
- <strong>서비스 안정성</strong>: 백엔드 과부하 방지
- **버스트 허용**: 정상적인 트래픽 패턴 수용

**설계 원칙**:
- Rate와 Burst를 서비스 유형별로 별도 설정
- 429 응답에 Retry-After 헤더 포함 (클라이언트 재시도 가이드)
- 분산 환경에서는 Redis + Lua 원자적 구현 필수
- 클라이언트에게 현재 한도를 X-RateLimit-* 헤더로 투명하게 공개

심화 학습에서는 <strong>토큰 버킷 알고리즘의 파라미터(R, B)와 동작 원리</strong>, **리키 버킷과의 차이**, <strong>분산 환경에서의 구현 방법(Redis)</strong>을 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Token Bucket Rate Limiting은 놀이공원 자이로드롭 — 안전을 위해 한번에 R명만 탑승(rate)하고, 여러 명이 미리 대기해도 최대 B명까지만 줄(버킷)을 허용한다. 정원 초과 시 "지금 자리 없어요"(429) 라고 안내한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Rate Limiting (속도 제한) | Token Bucket이 구현하는 상위 개념 |
| 대비 알고리즘 | Leaky Bucket | 일정 출력 속도 보장, 버스트 평활화 |
| 연관 알고리즘 | Fixed/Sliding Window | 다른 Rate Limiting 구현 방식 |
| 구현 도구 | Redis + Lua Script | 분산 환경의 원자적 Rate Limiting |
| 구현 라이브러리 | Bucket4j | Java 토큰 버킷 라이브러리 |
| 연관 인프라 | AWS API Gateway | 서비스 레벨 Rate Limiting 기본 내장 |
| 연관 개념 | Circuit Breaker | Rate Limit 초과 + 장애 복합 대응 |

### 📈 관련 키워드 및 발전 흐름도
rate limiting -> 쓰로틀링과 토큰 버킷 패턴 -> traffic governance

### 👶 어린이를 위한 3줄 비유 설명
1. 토큰 버킷은 동전 게임기 — 동전(토큰)이 있어야 게임을 할 수 있고, 동전이 없으면 기다려야 해. 동전통(버킷)이 꽉 차면 새 동전이 더 들어오지 않아.
2. 초당 R개씩 동전이 자동으로 생기는데, 동전을 모아뒀다가(버스트) 한번에 많이 쓸 수 있어 — 단, 동전통(B) 크기를 넘으면 더 모을 수 없어.
3. 토큰이 부족해서 게임을 못 하면 "토큰 없어요 (429 Too Many Requests), X초 후에 다시 와요 (Retry-After)"라고 친절하게 알려줘야 해.
