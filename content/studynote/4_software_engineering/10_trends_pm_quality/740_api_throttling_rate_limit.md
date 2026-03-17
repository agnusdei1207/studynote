+++
title = "740. API 스로틀링 Rate Limit DDoS 방어"
date = "2026-03-15"
weight = 740
[extra]
categories = ["Software Engineering"]
tags = ["API Security", "Rate Limiting", "Throttling", "DDoS Defense", "Availability", "Architecture Pattern"]
+++

# 740. API 스로틀링 Rate Limit DDoS 방어

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **API (Application Programming Interface)**의 가용성을 위협하는 과부하를 방지하기 위해, 트래픽 유입량을 시스템의 처리 용량(CPU, Memory, DB Connection 등) 내로 억제하고 조절하는 **트래픽 쉐이핑(Traffic Shaping) 및 보호 기술**입니다.
> 2. **제어 기법**: 특정 시간 윈도우 내 요청 횟수를 강제 제한하는 **Rate Limiting**과 시스템 부하(Load)에 따라 동적으로 처리 속도를 늦추는 **Throttling**을 상호 보완적으로 활용하여 정상 서비스를 보장합니다.
> 3. **가치**: 악의적인 **DoS (Denial of Service)** 공격을 1라인에서 차단하여 서버 리소스 고갈을 막고, 공유 클라우드 환경(Multi-tenant)에서 **'Noisy Neighbor' 문제**를 해결하여 공정한 자원 배분 및 비용 최적화를 달성합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학: "완벽한 방어는 불가능하다, 통제해야 한다"
API 스로틀링과 Rate Limiting은 단순한 '차단'이 아니라 시스템의 '생존'을 위한 통제 메커니즘입니다. 분산 시스템 환경에서 트래픽은 예측 불가능한 스파이크(Spike) 형태로 유입됩니다. 서버의 **Thread Per Request** 모델이나 **비동기 I/O (Non-blocking I/O)** 모델 모두 처리 가능한 자원풀(Resource Pool)의 한계가 존재합니다. 이 임계치(Critical Threshold)를 초과하는 순간, 시스템은 **Ladder of Failures(실패의 사다리)**를 밟아 **OOM (Out of Memory)**이나 **DB Connection Pool 고갈**로 이어져 전체 장애(Cascading Failure)가 발생합니다. 따라서 서버 앞단에서 트래픽을 평활화(Smoothing)하고, 초과분은 폐기(Drop)하거나 지연(Delay)시켜 시스템을 **Safe State(안전 상태)**로 유지하는 것이 본질입니다.

### 2. 등장 배경: ① 기존 한계 → ② 패러다임 변화
1.  **기존 한계 (Hard Limitation)**: 초기 웹 서비스는 단순히 서버 하드웨어(Scale-up)를 늘려 트래픽을 감당하려 했으나, 클라우드 네이티브 시대(Microservices Architecture)로 오며 무한 확장이 불가능해짐 (DB Lock, 외부 API 호출 제한 등).
2.  **혁신적 패러다임 (Shift to Resilience)**: **SLA (Service Level Agreement)** 준수를 위해 '모든 요청을 받아주는 것'보다 '약속된 성능을 보장하는 것'이 중요해짐.
3.  **현재 비즈니스 요구**: SaaS 플랫폼화에 따라, 공용 자원을 사용하는 특정 테넌트의 독점을 막고 '공정성(Fairness)'을 보장하는 정책(Policy) 기반의 트래픽 관리가 필수적이 됨.

### 3. ASCII 다이어그램: 개념적 비유
```text
      [ 일상 속의 트래픽 제어: 고속도로 요금소 ]
      
  자동차들(Request) ──▶ [ 진입 램프 ] ────▶ [ 고속도로 본선 (서버) ]
                           │
            ┌──────────────┴───────────────┐
            ▼                             ▼
     [ 하이패스 차선 ]               [ 일반 차선 ]
    (Token Bucket/유료)             (Queue/무료)
            │                             │
    "빠르게 통과 가능"              "줄을 서서 기다림"
            │                             │
            ▼                             ▼
┌─────────────────────────────────────────────────┐
│  ▲  톨게이트(게이트웨이)의 역할                 │
│  │                                            │
│  │  만약 진입 램프가 막히면(Throttling),     │
│  │  고속도로 본선이 꽉 차서 움직일 수 없게  │
│  │  되는 것(=서버 다운)을 막는다!            │
└─────────────────────────────────────────────────┘
```
> **해설**: Rate Limit은 "하이패스 차선 이용 횟수 제한"과 같아서, 할당량을 소진하면 아예 진입을 막습니다. Throttling은 "톨게이트 바로 앞의 신호등"과 같아서, 아무리 차가 많아도 고속도로 본선(서버)에 진입하는 속도를 조절하여 정체를 막습니다.

### 📢 섹션 요약 비유
> "마치 거대한 댐이 수문을 조절하여 홍수 시에도 흐름을 통제하고, 가뭄 시에도 물을 꼭꼭 눌러담아 하류의 안전을 지키는 것과 같습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (5개+ 모듈 상세)
| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 프로토콜/기술 | 비유 |
|:---:|:---|:---|:---|:---|
| **API Gateway** | 트래픽 진입점 및 검사관 | 모든 요청을 가로채 **Pre-request Hook**을 통해 제어 로직 수행 | HTTP/HTTPS, gRPC | 톨게이트 부스 |
| **Policy Engine** | 제한 규칙 저장소 | 유저 등급(Tier), 리소스별 **Quota** 설정 및 판정 로직 수행 | YAML/JSON Config | 요금표 |
| **State Store** | 상태 저장소 | 분산 환경에서 **Counter** 값을 유지하기 위한 외부 저장소 (일관성 필수) | Redis (In-memory) | 계수기 바구니 |
| **Algorithm Core** | 판정 알고리즘 | 토큰 생성, 누출, 시간 윈도우 계산 등 수행 (TBA, LBA 등) | Lua Scripting | 계산 로직 |
| **Monitor & Alert** | 관찰자 | 실시간 **TPS (Transactions Per Second)** 모니터링 및 임계치 도달 시 알림 | Prometheus, Grafana | CCTV 및 경보기 |

### 2. 대표 알고리즘 및 메커니즘
1.  **Token Bucket Algorithm (TBA)**:
    -   **원리**: 바구니(Bucket)에 정해진 속도로 토큰(Token)을 채움. 요청이 오면 토큰 1개를 소모하여 통과시킴. 토큰이 없으면 요청을 거부(429).
    -   **특징**: 버스트(Burst) 트래픽 허용 (바구니 크기만큼 저장). **Latency**가 낮아 실시간성이 요구될 때 유리함.
2.  **Leaky Bucket Algorithm (LBA)**:
    -   **원리**: 요청을 큐(Queue)에 담고, 정해진 속도로 처리(Leak)함. 큐가 가득 차면 요청을 거부.
    -   **특징**: 트래픽을 **완전히 균등하게(Smoothing)** 만듦. 버스트 불가. 네트워크 패킷 셰이핑에 주로 사용.
3.  **Fixed Window Counter**:
    -   **원리**: 1분 단위 등 고정된 시간 창(Window) 내 카운트.
    -   **한계**: 창의 경계선(Timestamp Boundary)에서 트래픽이 몰리는 문제(2배 허용) 발생 가능.
4.  **Sliding Window Log**:
    -   **원리**: 요청의 **타임스탬프**를 로그로 남겨, 현재 시간에서 역슬라이드하여 카운트.
    -   **장점**: 가장 정확함. **단점**: 메모리 사용량이 많음.

### 3. 아키텍처 구조 및 데이터 흐름 (ASCII)
```text
   [Request Flow]
     Client
       │
       │ ① API Request (API Key / IP / User ID)
       ▼
 ┌───────────────────────────────────────────────────────┐
 │                 API Gateway / Load Balancer           │
 │  ┌─────────────────────────────────────────────────┐  │
 │  │   Middleware: Rate Limiter                      │  │
 │  │   ┌─────────────────────────────────────────┐   │  │
 │  │   │ 1. Identify Key (Hash Map Lookup)       │   │  │
 │  │   │    -> Resolve 'tenant_id' or 'user_id'  │   │  │
 │  │   │                                         │   │  │
 │  │   │ 2. Check State (Redis GET)              │   │  │
 │  │   │    key: "limit:user:123:window"         │   │  │
 │  │   │    val: "current_count"                 │   │  │
 │  │   │    -> Algorithm (Token Bucket Logic)    │   │  │
 │  │   │                                         │   │  │
 │  │   │ 3. Decision                             │   │  │
 │  │   │    IF count < limit                     │   │  │
 │  │   │       -> PASS (Forward to Service)      │   │  │
 │  │   │       -> INCR counter (Redis SET)       │   │  │
 │  │   │    ELSE                                 │   │  │
 │  │   │       -> REJECT (HTTP 429 Too Many Req) │   │  │
 │  │   └─────────────────────────────────────────┘   │  │
 └───────────────────────────────────────────────────────┘
       │                                    ▲
       │ ④ Response (JSON Data)             │ ② Sync Counter
       │  or Error 429                       │
       ▼                                    │
    [App Server]                      [Distributed Cache]
    (Business Logic)                    (Redis Cluster)
```
> **해설**: 위 그림은 **API Gateway** 패턴에서의 동작을 나타냅니다. 핵심은 **Statelessness**를 유지하기 위해 별도의 **Redis** 같은 저장소를 둔다는 점입니다. 서버가 여러 대라도(Redis Cluster), 공유 카운터를 통해 전체 트래픽을 정확히 제어할 수 있습니다. 또한 `INCR` 명령어는 원자성(Atomic)을 보장해야 하므로 **Lua Script**나 **Transaction**을 사용하여 **Race Condition**을 방지해야 합니다.

### 4. 핵심 코드 및 수식 (Redis + Lua)
```lua
-- Redis Lua Script for Token Bucket (Atomic Execution)
-- KEYS[1]: Rate Limit Key (e.g., "user:123:api")
-- ARGV[1]: Capacity (버킷 크기, 예: 100)
-- ARGV[2]: Tokens per second (충전 속도, 예: 10)
-- ARGV[3]: Current timestamp (seconds)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local tokens_per_sec = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- 1. 현재 상태 조회
local info = redis.call('hmget', key, 'tokens', 'last_refill_time')
local current_tokens = tonumber(info[1]) or capacity
local last_refill_time = tonumber(info[2]) or now

-- 2. 토큰 충전 계산 (Time delta)
local delta = math.max(0, now - last_refill_time)
local added_tokens = delta * tokens_per_sec
current_tokens = math.min(capacity, current_tokens + added_tokens)

-- 3. 토큰 소비 가능 여부 판단
if current_tokens >= 1 then
    -- 요청 허용: 토큰 1개 소비
    redis.call('hmset', key, 'tokens', current_tokens - 1, 'last_refill_time', now)
    redis.call('expire', key, 600) -- Cleanup
    return 1   -- Allowed
else
    -- 요청 거부: 상태만 갱신 (Refresh info)
    redis.call('hmset', key, 'tokens', current_tokens, 'last_refill_time', now)
    redis.call('expire', key, 600)
    return 0   -- Denied
end
```
> **수식 설명**: `New_Tokens = min(Capacity, Current_Tokens + (Now - Last_Time) × Rate)`

### 📢 섹션 요약 비유
> "수도꼭지(Rate Limiter)에서 일정한 속도로 물(토큰)이 채워지는 양동이(Bucket)를 생각해보세요. 컵(요청)에 물을 담을 수 있으면 통과이고, 양동이가 비어 있으면 물이 채워질 때까지 기다려야 하거나(Throttling) 아예 물을 받을 수 없게(Rate Limit) 되는 것입니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: Rate Limiting vs Throttling
| 비교 항목 | Rate Limiting (정적 제한) | Throttling (동적 조절) |
|:---|:---|:---|
| **목표 (Goal)** | **Fairness (공정성)** 보장 | **Stability (안정성)** 유지 |
| **제한 대상** | 사용자별, API 키별, IP별 | 전체 시스템 Load, DB CPU Usage |
| **결과 처리** | **Hard Reject** (HTTP 429) | **Delay** (Queuing) 또는 Reject |
| **주요 지표** | Request Count (e.g., 100/min) | System Load Avg, Latency (ms) |
| **구현 난이도** | 구현 쉬움 (Stateful Counter) | 구현 어려움 (Metrics-based Feedback) |
| **적용 예시** | 무료 사용자 API 호출 제한 | 배치 작업 시 DB I/O 억제 |

### 2. OSI 7계층 및 아키텍처 융합 관점
- **L3/L4 (Network Layer) vs L7 (Application Layer)**:
    - **L3/L4 (Firewall, Load Balancer)**: **SYN Flood** 같은 **DoS (Denial of Service)** 공격 방어에 효과적임. 패킷 단위로 차단하여 대역폭 절약.
    - **L7 (API Gateway, WAF)**: **HTTP GET/POST** 패턴 분석을 통한 정교한 제어 가능. 특정 URL(`/login`)에 대한 Brute Force 공격 차단 등에 탁월.
- **MSA (Microservices Architecture)와의 시너지**:
    - 각 **MSA** 서비스마다 개별적으로 제한을 두면 **Configuration Hell**이 발생함. **Service Mesh (Istio, Envoy)**를 활용하여 글로벌하게 Rate Limit 정책을 배포하는 것이 표준으로 자리 잡고 있음.

### 3. 성능 메트릭 분석 (정량적 의사결정)
Rate Limiting 도입 시 **Throughput(처리량)**은 소폭 감소할 수 있으나(Overhead), **P99 Latency(99번째 백분위수 지연시간)**은 급격히 개선됩니다.
-   **도입 전**: P99 = 800ms (Spike 시 5000ms 이상 폭증)
-