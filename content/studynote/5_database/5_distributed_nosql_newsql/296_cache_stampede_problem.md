+++
title = "296. 캐시 스탬피드 (Cache Stampede) - 분산 시스템의 압사 사고"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 296
+++

# 296. 캐시 스탬피드 (Cache Stampede) - 분산 시스템의 압사 사고

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 캐시 스탬피드(Cache Stampede)는 **Hot Key**의 캐시 만료(TTL Expiration) 시점에 다중 요청이 동시에 **Cache Miss**를 감지, 원본 DB(Source of Truth)로 폭주하는 **Thundering Herd** 현상을 의미한다.
> 2. **가치**: 대규모 트래픽 처리 시스템에서 가장 치명적인 **SPOF (Single Point of Failure)** 요인이며, 이를 방어하지 못하면 데이터베이스 과부하로 전체 서비스가 마비된다.
> 3. **융합**: **Mutex Lock**, **Distributed Lock (Redlock)**, **PER (Probabilistic Early Recomputation)** 등의 알고리즘을 결합하여 데이터 일관성과 고가용성(High Availability)을 동시에 확보해야 한다.

---

### Ⅰ. 개요 (Context & Background)

캐시 스탬피드(Cache Stampede), 일명 'Dog-pile Effect'는 분산 시스템, 특히 대용량 트래픽을 처리하는 **Read-Intensive**한 아키텍처에서 발생하는 대표적인 병목 현상이다. 기본적으로 **Cache-Aside** 패턴(Lazy Loading)을 사용하는 시스템은 캐시에 데이터가 없을 때만 DB에 접근한다. 그러나 인기 있는 핫 아이템(예: 메가세일 이벤트 페이지, 실시간 1위 검색어)의 캐시가 만료되는 순간, 수만~수십만의 요청이 동시에 'Cache Miss' 판정을 받게 되고, 이들이 모두 원본 데이터베이스로 몰려들어 **DB Connection Pool**을 고갈시키고 **CPU 사이클**을 폭주시킨다.

이 현상은 단순히 트래픽이 많은 것과는 다르다. 트래픽이 캐시 계층에서 걸러지면 DB는 안전하지만, 스탬피드는 '걸러주어야 할 방패(캐시)'가 사라진 순간에 창끝(요청)이 모두 뚫리는 **하이브리드 장애**라는 점이 특징이다.

- **💡 비유**: **심장박동에 맞춰 열리는 전자문**이 있다고 상상해보자. 평소엔 문이 열려있어 사람들이 자유롭게 지나가지만(Cache Hit), 정오 알람(만료)과 동시에 문이 쇄도로 닫혀버린다. 그때 수천 명의 사람이 문에 부딪히며(Gap), 갑자기 문이 다시 열리면 그 압력에 의해 사람들이 한꺼번에 아주 좁은 문으로 빨려 들어가 담가지는 것과 같다.

- **등장 배경**:
    1.  **기존 한계**: 단순 캐싱만으로는 TTL(Time To Live) 갱신 시점의 간극을 메울 수 없음.
    2.  **혁신적 패러다임**: '단순 만료'가 아닌 '확률적 갱신' 및 '동기화 제어' 개념의 도입.
    3.  **비즈니스 요구**: 쿠폰 발급, 주식 장마감 등 **Spike Traffic**이 발생하는 이벤트 기반 서비스의 안정성 확보 필요.

> **📢 섹션 요약 비유**: 캐시 스탬피드는 **'고속도로 톨게이트의 바리케이드가 동시에 열렸다가 닫히는 찰나의 혼란'**과 같습니다. 바리케이드가 열리면(캐시 만료) 멈춰 있던 수천 대의 차가 동시에 좁은 통로(DB)로 진입하려 해 교통체증이 일어나는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

캐시 스탬피드의 기술적 메커니즘은 **Race Condition**과 **Lock Contention**으로 요약된다. 아래는 주요 구성 요소와 발생 프로세스를 분석한 표이다.

#### 1. 구성 요소 상세 분석

| 요소명 | 역할 | 내부 동작 및 파라미터 | 프로토콜/포멧 | 비유 |
|:---|:---|:---|:---|:---|
| **Client** | 요청자 | 고유키(Key)를 기반으로 데이터 조회 요청 전송. `Latency`에 민감함. | HTTP/gRPC | 손님 |
| **Cache Server** | 1차 방어선 | `GET` 요청 수신. `TTL > 0`이면 반환, `TTL = 0`이면 **NULL** 반환 및 삭제. | Redis/Memcached | 빠른 계산대 |
| **Database (RDBMS)** | Source of Truth | 디스크 I/O가 수반되는 무거운 쿼리 수행. Connection Pool(`max_conn`) 제한 존재. | SQL | 창고 |
| **Lock Manager** | 동기화 제어 | **Mutex** 또는 **Distributed Lock**을 통해 특정 키의 갱신 주체를 1개로 제한. | Redlock(Redis) | 번호표 기계 |

#### 2. 발생 메커니즘 및 데이터 흐름

아래 다이어그램은 TTL 만료 시점에서의 비동기적 경합 상황을 도시화한 것이다.

```text
   [Time Flow] ────────────────────────────────▶
      
   T1 (Normal)              T2 (Expired)              T3 (Recovery)
   ┌──────────┐            ┌──────────┐             ┌──────────┐
   │ Cache    │            │ Cache    │             │ Cache    │
   │ [Data A] │            │ [NULL]   │◀─ Stampede! │ [Data A] │
   └────┬─────┘            └────┬─────┘             └────┬─────┘
        │                       │                         ▲
        │ Hit                   │ Miss                    │
        ▼                       │ Miss                    │ Set
   [Request R1]                 ▼                         │
   [Request R2]          [Request R3] ──┐                [Request R_N]
   ...                    [Request R4] ──┤ Logic: Check DB
                         [Request R5] ──┤
                                  │     ▼
                          ┌───────▼───────────────────────┐
                          │      Database Server          │
                          │  (SELECT * FROM ITEM ...)     │
                          │  ● CPU 100% Spike             │
                          │  ● I/O Wait High              │
                          │  ● Connection Pool Exhausted  │
                          └───────────────────────────────┘
```

**[다이어그램 해설]**
1.  **T1 단계**: 캐시 서버가 유효한 데이터(`Data A`)를 유지하며 모든 요청을 빠르게 처리함.
2.  **T2 단계 (Critical Moment)**: TTL이 도달하여 캐시 데이터가 증발함. 이 순간 `T+0.001s` 사이에 들어온 수천 개의 요청(R3~R1000)이 캐시에서 빈손(`NULL`)을 돌려받음.
3.  **T3 단계 (Storm)**: 모든 요청이 "데이터가 없으니 DB에 가자"라는 판단을 하여 동시에 DB 쿼리를 실행함. 이때 DB는 순식간에 임계치(CPU/Memory)를 초과하여 다운되거나 응답 불능 상태가 됨.

#### 3. 심층 알고리즘: Mutex Lock (Single Flight Pattern)

이를 방어하기 위해 가장 널리 쓰이는 방식은 **'값 설정 전담자를 1명으로 뽑는 것'**이다. 의사코드(Pseudocode)는 다음과 같다.

```python
# Pseudocode: Cache Stampede Protection using Mutex
def get_data(key):
    # 1. 캐시 시도
    data = cache.get(key)
    if data is not None:
        return data  # Cache Hit

    # 2. 캐시 미스 시, 락 획득 시도
    # lock_key는 보통 "lock:{original_key}" 형태 사용
    lock_acquired = cache.set(lock_key, "1", nx=True, ex=10) # nx: Only set if not exists
    
    if lock_acquired:
        try:
            # 3. [Winner] DB 조회 및 캐시 갱신
            new_data = db.query("SELECT * FROM table WHERE id = %s", key)
            cache.set(key, new_data, ttl=3600)
            return new_data
        finally:
            cache.delete(lock_key) # 락 해제
    else:
        # 4. [Loser] 락을 못 얻었다면, 잠시 대기 후 재시도 혹은 기존 데이터 반환
        # 옵션 A: 약간의 지연(Sleep) 후 다시 캐시 조회
        time.sleep(0.05) 
        return get_data(key) 
        # 옵션 B: 완전히 오래된 데이터(Stale Data)라도 반환하여 가용성 확보
```

> **📢 섹션 요약 비유**: 데이터베이스 앞에 **'번호표 뽑기 기계(Lock)'**를 설치한 것과 같습니다. 캐시가 사라진 순간 수천 명이 몰려와도, 번호표를 뽑은 단 한 명만 창고(DB)로 들어가 물건을 가져오고 나머지는 입구에서 기다리게 하여 창고가 무너지는 것을 막습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

캐시 스탬피드 해결을 위한 기술들은 선택이 아닌 상황에 맞는 조합이 필요하다.

#### 1. 기술적 대책 비교 분석표

| 구분 | Mutex Lock (락킹) | Probabilistic Early Recomputation (PER) |
|:---|:---|:---|
| **핵심 전략** | **경쟁 제어**: 갱신 주체를 1개로 제한 | **선제적 갱신**: 만료되기 전에 확률적으로 재계산 |
| **대상 데이터** | 갱신 비용이 매우 비싼 데이터(Join 복잡) | 조회수가 매우 높고 비교적 계산이 가벼운 데이터 |
| **응답 속도** | 빠름 (Hit 시) / 지연 가능 (Miss 대기 시) | 매우 빠름 (만료 자체가 거의 발생하지 않음) |
| **부하 분산** | DB 부하를 획기적으로 줄임 (1회 쿼리) | 평소 CPU 사용량은 약간 증가하지만 피크 시 부하 없음 |
| **복잡도** | 구현이 쉬우나 Deadlock 유의 필요 | 수식(확률) 계산 및 캐시 로직 복잡도 높음 |

#### 2. 타 과목 융합 시너지 및 오버헤드

-   **운영체제(OS)와의 융합 (I/O Multiplexing)**:
    캐시 스탬피드 방어 로직(락 획득 대기)은 비동기 I/O(Non-blocking I/O) 모델 위에서 구현되어야 한다. 락을 얻기 위해 Thread를 Block(대기)시키면, 그 순간 서버의 **Concurrency(동시성)**가 급격히 떨어져 오히려 병목이 발생할 수 있기 때문이다.
-   **네트워크(Network)와의 융합 (Latency vs. Consistency)**:
    분산 락(Redlock)을 사용할 경우, 네트워크 왕복(RTT)에 따른 **Latency**가 증가한다. 이때 기본적인 **CAP Theorem**의 상충 관계가 발생한다. Lock을 강하게 걸면 Consistency는 지켜지지만 Availability(응답 속도)가 저하될 수 있다.

```text
[Trade-off Visualization]

   High Consistency
      ▲
      │      [Mutex Lock] (Distributed Lock)
      │         ●
      │       (Low Latency? No, High Safety)
      │
      │
      └────────────────────────────────────────▶ High Availability
         ●
      [PER]
   (High Availability? Yes, Low Impact)
```

> **📢 섹션 요약 비유**: **'병원 접수 시스템'**으로 비유할 수 있습니다. Mutex는 **'호흡기 환자 1명을 먼저 입장시키고 문을 잠그는 방식'**(정확한 진단 우선)이고, PER은 **'대기 시간이 다 되기 1분 전에 미리 간호사가 환자를 부르는 방식'**(혼란 방지 우선)입니다. 상황에 따라 응급실 Mutex와 예방 접종 PER을 선택해야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서는 단순히 '기술을 적용하는 것'을 넘어 장애 상황 시의 **Fallback 전략**과 **유지보수성**을 고려해야 한다.

#### 1. 실무 시나리오 기반 의사결정

1.  **Flash Sale (번개 세일) 상품 페이지**:
    -   **상황**: 수백만 명이 동시에 접속. DB 조회 쿼리가 복잡한 상품 정보+재고 조회.
    -   **판단**: **Mutex Lock + Stale Data**.
    -   **이유**: 정확한 재고 연동이 중요하므로 Lock을 걸되, 락 획득 실패 시에도 에러를 내지 않고 '5초 전 데이터(Stale)'라도 보여주어 사용자 경험(UX)을 해치지 않는 전략을 취한다. (Soft Degradation)

2.  **실시간 랭킹/차트 (Top 100)**:
    -   **상황**: 1초마다 갱신되는 데이터, TTL이 매우 짧음.
    -   **판단**: **Jitter (Random TTL)** 또는 **Hot Key Offloading**.
    -   **이유**: 매초 정각에 모든 키가 갱신되는 것을 방지하기 위해 TTL에 `±(0~10%)`의 Jitter(흔들림)를 주어 갱신 시점을 분산시킨다.

3.  **뉴스 피드 (Social Timeline)**:
    -   **상황**: 개인화된 추천 알고리즘으로 DB 부하가 상당함.
    -   **판단**: **PER (Probabilistic Early Recomputation)**.
    -   **이유**: 사용자가 느끼지 못할 사이에 미리 갱신하여 만료 시점 자체를 삭제한다.

#### 2. 도입 체크리스트 (Anti-pattern 방지)

| 구분 | 체크항목 | 설명 |
|:---|:---|:---|
| **기술적** | **Lock Timeout** 설정 | 락을 획득한 프로세스가 죽을 경우를 대비해, 반드시 **Expire Time**을 설정하여 교착상태(Deadlock)를 방지할 것? |
| **기술적** | **Cache Warming** | 서비스 기동 시나 배포 직후, 캐시가 비어있는 상태(Cold Start)