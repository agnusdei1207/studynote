+++
title = "640. 성능 테스트 부하/스트레스/스파이크/인듀어런스"
date = "2026-03-15"
weight = 640
[extra]
categories = ["Software Engineering"]
tags = ["Testing", "Performance Testing", "Load Test", "Stress Test", "Spike Test", "Endurance Test"]
+++

# 640. 성능 테스트 부하/스트레스/스파이크/인듀어런스

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템의 **응답 시간(Response Time)**, **처리량(Throughput)**, **자원 활용도(Resource Utilization)** 등을 측정하여 비즈니스 요구사항인 **SLA (Service Level Agreement)**를 충족하는지, 그리고 시스템의 **한계 용량(Capacity)** 및 **회복성(Resilience)**을 검증하는 검증 활동이다.
> 2. **가치**: 단순한 속도 측정을 넘어, 서비스 장애로 인한 잠재적 매출 손실을 방지하고, 시스템의 병목 구간을 식별하여 인프라 비용을 최적화하며, 아키텍처의 결함을 사전에 교정할 수 있는 기술적 근거를 제공한다.
> 3. **융합**: **카오스 엔지니어링(Chaos Engineering)** 및 **AIOps (Artificial Intelligence for IT Operations)**과 연계하여, 정상 상태뿐만 아니라 비정상 상태에서의 시스템 거동을 예측하고 자율 대응하는 선제적 안정성 확보 체계로 진화하고 있다.

---

### Ⅰ. 개요 (Context & Background)

성능 테스트는 소프트웨어가 기능적 요구사항을 만족하는지 넘어, "얼마나 빨리, 얼마나 많은 사용자를, 얼마나 오래" 처리할 수 있는지를 검증하는 학문이자 실무 기술이다. 과거의 단일 모놀리식 시스템에서는 하드웨어 사양만 확인하면 되었으나, 현대의 **MSA (Microservices Architecture)** 환경에서는 네트워크 지연, DB 커넥션 풀(Connection Pool) 경합, 분산 캐시의 **일관성(Consistency)** 등 복합적인 변수가 성능을 좌우한다.

따라서 성능 테스트는 단순히 '빠른 것'을 확인하는 것이 아니라, 시스템이 견뎌야 할 '예상 부하'를 정확히 시뮬레이션하고, 그 과정에서 발생하는 **TPS (Transactions Per Second)** 저하나 **Latency (지연 시간)** 급증의 원인을 **APM (Application Performance Management)** 도구와 연계하여 분석하는 종합적인 진단 과정이다.

#### 💡 비유: 다리의 안전 진단 (Inspection)
성능 테스트는 신규 개통 교량에 대해 차량을 통과시키지 않고는 다리의 안전성을 보장할 수 없는 것과 같다. 단순히 설계도상의 계산만으로는 실제 교통 체증, 노후화, 돌발 상황(사고 등)에 대처할 수 없기 때문이다. 각종 차량(트래픽)을 직접 다리에 투입하여 교량의 진동, 처짐, 파손 여부를 측정하는 물리적 내구성 테스트와 정확히 일치한다.

#### ASCII 다이어그램: 테스트 유형별 시나리오 시각화
아래 다이어그램은 시간(X축)에 따른 부하량(Y축) 변화를 통해 각 테스트가 시스템에 가하는 스트레스 패턴을 도식화한 것이다.

```text
Load Intensity
  ^
  │        (Spike)
  │         /\          (Stress)
  │        /  \           /
  │       /    \         /
  │      /      \       /  (Break Point)
  │     /        \     /
  │    /          \   /
  │   /            \ /
  │  /______________\______________ (Baseline)
  │ /               \              \
  └───────────────────────────────────────────> Time
   [Load Test]      [Spike]       [Stress]
   : 점진적 증가     : 급격한 폭증   : 파괴 지점까지
   (예: 100->1000)   (예: 0->5000)   (예: 1000->...Error)

   [Endurance Test]
   : 낮은 부하를 매우 긴 시간 동안 지속
   ─────────────────────────────────────────────────────>
   (예: 7 Days @ 500 Users)
```

**[다이어그램 해설]**
위 그래프와 같이 각 테스트는 시스템에 가해지는 에너지의 패턴이 다르다. **Load Test (부하 테스트)**는 계단식으로 부하를 높여가며 변곡점(Turning Point)을 찾는 정상적인 검사다. 반면, **Stress Test (스트레스 테스트)**는 시스템이 붕괴(Down)되는 지점을 의도적으로 찾아내어, 이후 복구 가능 여부를 확인하는 가혹 테스트다. **Spike Test (스파이크 테스트)**는 순간적인 트래픽 폭주(이벤트 페이지 접속 등) 상황을 시뮬레이션하여 큐(Queue) 시스템이나 캐시의 **Miss Ratio**가 급격히 치솟는 순간을 포착하는 데 중점을 둔다. 마지막으로 **Endurance Test (내구성 테스트)**는 낮은 부하가 아니라, '장기간 운영 시 발생하는 메모리 누수(Memory Leak)'나 '파일 디스크립터 고갈' 같은 잠재적 리소스 누수를 찾아내기 위한 시간 축의 테스트다.

**📢 섹션 요약 비유**
> 마치 새로 지은 고속도로가 개통 전, 설계된 통과 차량 대수(부하), 공휴일 귀성차 폭주(스파이크), 24시간 내내 이어지는 화물차 통행(인듀어런스)을 시뮬레이션하여 도로 포장 상태와 톨게이트 처리 속도를 미리 검증하는 도로 안전 진단 과정과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

성능 테스트는 단순히 요청을 보내는 것이 아니라, 실제 사용자의 행동 패턴을 수학적으로 모델링하고 이를 시스템에 가하는 정교한 공학적 작업이다. 이를 위해 **Load Generator (부하 생성기)**, **Test Controller (테스트 컨트롤러)**, **System Under Test (SUT)** 등의 명확한 역할 분담이 필요하다.

#### 1. 성능 테스트 아키텍처 구성 요소
| 구성 요소 (Component) | 역할 (Role) | 상세 동작 (Internal Behavior) | 주요 프로토콜/도구 | 비유 (Analogy) |
|:---:|:---|:---|:---|:---|
| **Workload Model** | 부하 모델링 | 실제 유저의 행동(Think Time, Pacing)을 스크립트로 정의 | JMeter, Gatling, Locust | 연극 대본 |
| **Load Generator** | 부하 생성 | 다수의 가상 스레드(Thread)를 생성하여 HTTP/TCP 요청 전송 | HTTP, HTTPS, WebSocket | 배우들 |
| **Controller** | 제어 및 관리 | 부하의 시작/종료, 스레드 수 조절, 테스트 시나리오 배포 | JMeter Master, k6 Operator | 연출가 |
| **SUT (System Under Test)** | 테스트 대상 | WAS, DB, Redis 등 트래픽을 소비하는 서버 및 인프라 | Java Spring, Nginx, MySQL | 무대 |
| **Monitor/Agent** | 데이터 수집 | CPU, Memory, GC Rate, Disk I/O 등 리소스 메트릭 실시간 수집 | Prometheus, Datadog Agent, JMX | 카메라 맨 |

#### 2. 핵심 성능 지표 (Metrics) 및 수식
성능을 판단하는 척도는 크게 **Response Time (응답 시간)**, **Throughput (처리량)**, **Error Rate (오류율)**, **Resource Utilization (자원 사용률)**으로 나뉜다.

1.  **응답 시간 (Response Time, Latency)**
    -   **RTT (Round Trip Time)**: 요청 전송부터 응답 수신까지의 왕복 시간.
    -   **TTFB (Time To First Byte)**: 요청 후 첫 번째 바이트 데이터를 받을 때까지의 시간(서버 처리 능력의 지표).
    -   $$ \text{Average Response Time} = \frac{\sum \text{Response Times}}{\text{Total Requests}} $$

2.  **처리량 (Throughput)**
    -   단위 시간당 시스템이 처리하는 트랜잭션의 양.
    -   $$ \text{TPS (Transactions Per Second)} = \frac{\text{Total Completed Transactions}}{\text{Time (seconds)}} $$
    -   *목표 설정 예시: 평균 50ms 응답 시간 시, $1000ms / 50ms = 20$ TPS/Thread (이론값). 실제는 컨텍스트 스위칭 등으로 인해 더 낮음.*

3.  **자원 활용도 (Utilization)**
    -   $$ \text{CPU Utilization (\%)} = \frac{\text{CPU Busy Time}}{\text{Total Elapsed Time}} \times 100 $$
    -   **Little's Law**: 시스템 내 평균 고객 수(L)는 도착율($\lambda$)과 평균 체류 시간(W)의 곱과 같다.
    -   $$ L = \lambda \times W $$

#### 3. 부하 생성 시나리오 작성 코드 (Pseudo-Code)
실무에서는 단순 반복 요청보다 '사용자 세션'을 모방해야 한다. 아래는 가상 사용자가 로그인 후 상품을 조회하고 로그아웃하는 과정을 시뮬레이션하는 스크립트의 개념이다.

```text
[Script: Purchase_Simulation.pseudo]

// 1. Init (초기화)
SETUP {
    config.target_host = "api.service.com"
    config.protocol = HTTP/1.1
    config.timeout = 3000ms
}

// 2. Scenario (시나리오)
SCENARIO "User_Buying_Flow" {
    
    // Step 1: Login (POST)
    ACTION POST "/auth/login" {
        BODY: { "id": "${user_id}", "pw": "..." }
        ASSERT Response_Code == 200
        SAVE_HEADER "Auth-Token" -> global_token
    }
    WAIT(2s) // Think Time: 사용자가 로그인 후 머무는 시간

    // Step 2: Browse Item (GET)
    ACTION GET "/products/12345" {
        HEADER: "Authorization: Bearer ${global_token}"
        ASSERT Response_Code == 200
    }
    WAIT(1s)

    // Step 3: Order (POST) - Critical Transaction
    ACTION POST "/orders" {
        HEADER: "Content-Type: application/json"
        BODY: { "productId": 12345, "count": 1 }
        ASSERT Response_Code == 201
    }
}

// 3. Load Strategy (부하 전략)
LOAD_PROFILE {
    RAMP_UP_USERS(100) OVER(60s) // 60초 동안 100명 증가
    HOLD_FOR(300s)               // 5분간 유지 (Stability Check)
    RAMP_TO(500) OVER(30s)       // 30초 만에 500명으로 급증 (Spike)
    GRACEFUL_STOP(10s)           // 점진적 중단
}
```

#### 4. 시스템 리소스 병목 분석도
성능 저하 발생 시, 외부 지표(TPS 저하)와 내부 리소스(CPU, Memory, DB Lock)의 상관관계를 분석해야 한다.

```text
                 [Performance Bottleneck Analysis]
  
  TPS (Throughput)
    ^
    |          ________ (Saturation)
    |         /        \
    |        /          \______ (Degradation)
    |       /
    |      /
    |     /
    |    / (Linear Growth)
    └────────────────────────────────────────────> Users
   
  Response Time (Latency)
    ^
    |                                  (Explosive Increase)
    |                                 /
    |                                /
    |                              _/
    |                             /
    |                            /
    | __________________________/
    └────────────────────────────────────────────> Users
   
  Resource Utilization (CPU/IO)
    ^
    |                                 (100% Usage - Bottleneck)
    |                               _|
    |                             _/
    |                           _/
    |                       ___/
    |            ________--/
    |__________--/
    └────────────────────────────────────────────> Users

    [Point A]: 정상 구간 (Linear Scaling)
    [Point B]: 포화 지점 (Knee of the curve) -> 병목 시작
    [Point C]: 파국 지점 (Collapse) -> TPS 하락, 응답 시간 폭증
```

**[다이어그램 해설]**
위 다이어그램은 시스템 성능의 변곡점을 설명하는 **"Knee of the Curve"** 이론을 보여준다. 사용자(User)가 증가함에 따라 TPS는 선형적으로 증가하다가, 특정 지점(Point B)에서 CPU나 **DB Connection Pool**이 가득 차면서 더 이상 증가하지 못하고 평탄해진다(Saturation). 이 상태에서 사용자를 더 추가하면, 시스템은 처리해야 할 큐(Queue)가 넘치면서 **Context Switching (문맥 교환)** 오버헤드가 발생하고 응답 시간이 기하급수적으로 늘어난다. Point C에 이르면 시스템은 스스로를 보호하기 위해 **Thread Stack Overflow**를 일으키거나 OOM(Out of Memory)으로 죽게 되며, TPS는 오히려 떨어지는 현상을 보인다. 성능 테스트의 핵심은 이 Point B를 정확히 찾아내어, 그 이전에 **Scale-out (수평 확장)** 하거나 **Circuit Breaker (회로 차단기)**를 동작시키는 것이다.

**📢 섹션 요약 비유**
> 고속도로 톨게이트에 차량이 밀리기 시작하면, 처리량(통행 차량 수)은 일정 수준에 머무르고 대기 시장(지연 시간)만 급격히 늘어납니다. 성능 테스트란 이 톨게이트가 '처리할 수 있는 최대 차량 대수'와 '정체가 풀리지 않고 꽉 막히는 시점'을 정확히 찾아내어, 하이패스 차로(캐시)를 추가하거나 부스 증설(스케일 아웃)을 결정하는 정교한 교통 설계 과정입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

성능 테스트는 단순한 **QA (Quality Assurance)** 활동에 그치지 않고, 인프라 비용 절감 및 운영 안정성 확보를 위한 핵심 의사결정 도구로 활용된다.

#### 1. 성능 테스트 vs 스트레스 테스트 vs 부하 테스트 (정량적 비교)

| 구분 | 부하 테스트 (Load Test) | 스트레스 테스트 (Stress Test) | 스파이크 테스트 (Spike Test) | 인듀어런스 테스트 (Endurance Test) |
|:---|:---|:---|:---|:---|
| *