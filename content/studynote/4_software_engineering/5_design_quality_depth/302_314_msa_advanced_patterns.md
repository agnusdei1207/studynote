+++
title = "302-314. 마이크로서비스 설계 패턴 (Circuit Breaker, Saga, BFF)"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 302
+++

# 302-314. 마이크로서비스 설계 패턴 (Circuit Breaker, Saga, BFF)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 시스템의 필연적 장애(Failure)를 탄력적으로 흡수하기 위해 **안정성(Resilience)**과 **일관성(Consistency)**을 설계 레벨에서 보장하는 아키텍처 패턴들의 집합체이다.
> 2. **가치**: MSA (Microservice Architecture) 환경에서 '단일 장애점(SPOF)'을 제거하여 시스템 가용성을 99.99% 이상으로 유지하고, 분산 트랜잭션으로 인한 데이터 불일치를 방지하여 비즈니스 신뢰성을 확보한다.
> 3. **융합**: 클라우드 네이티브(Cloud Native) 환경의 **Kubernetes (K8s)** 기반 서비스 메시(Service Mesh)인 **Istio**와 결합하여 무중단 서비스를 구현하고, Reactive Programming 기반의 비동기 통신과 시너지를 일으킨다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
MSA (Microservice Architecture)는 모놀리식(Monolithic) 시스템을 소수의 서비스로 분리하여 독립적 배포와 확장성을 확보하는 패러다임이지만, 그 대가로 '분산 시스템의 복잡성'을 감내해야 한다. 서비스 간 통신(Network I/O)이 필수적이므로, 네트워크 지연(Latency), 시간 초과(Timeout), 서비스 중단(Downtime)은 예외가 아닌 일상적인 상황이 된다. 따라서 "어떤 서비스가 죽더라도 전체 시스템은 죽지 않아야 한다"는 **탄력성(Resilience)**이 최우선 설계 원칙이 된다. 본 패턴들은 이러한 분산 환경의 난관을 극복하기 위해 제안된 베스트 프랙티스이다.

**등장 배경**
1. **기존 한계**: 모놀리식의 '전체 실패(Fail-Stop)' 방식에서 벗어나려 했으나, RPC(Remote Procedure Call) 도배 시 발생하는 'Snowball Effect(돼지 멱따기 효과)'로 인해 장애 확산이 심각해짐.
2. **혁신적 패러다임**: '취약한 의존성(Fragile Dependency)'을 격리하기 위해 전기 회로의 차단기 개념을 차용한 **Circuit Breaker**와, 분산 DB 트랜잭션의 ACID를 보장하기 위해 로컬 트랜잭션의 순차 실행 및 보상(Compensation)을 전제로 하는 **Saga Pattern**이 등장.
3. **현재의 비즈니스 요구**: 글로벌 대용량 트래픽을 처리하는 **IoT (Internet of Things)** 및 **Fintech** 플랫폼에서 데이터 무결성을 타협하지 않으면서 24/7 서비스 가용성을 유지해야 하는 필수 요구사항으로 자리 잡음.

**💡 비유**
마치 거대한 선박(시스템)이 침몰 사고(장애)를 당했을 때, 칸막이(Bulkhead)를 통해 일부 구획만 침수되도록 하여 배 전체가 가라앉는 것을 막는 설계와 같다.

📢 **섹션 요약 비유**: MSA 패턴 적용은 **"고속도로에서 사고가 났을 때, 비상 차선으로 우회시키고(장애 격리), 사고 난 차량을 빠르게 견인하며(자가 치유), 목적지에 도착한 순서대로 요금 정산을 처리하는(데이터 일관성) 교통 통제 시스템"**을 구축하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

마이크로서비스의 안정성과 데이터 일관성을 담당하는 핵심 컴포넌트와 그 동작 메커니즘을 분석한다.

#### 1. 구성 요소 상세 분석

| 모듈 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 | 주요 파라미터 및 비고 |
|:---|:---|:---|:---|
| **API Gateway** | 클라이언트 요청의 **Single Entry Point**. 라우팅, 인증(AuthN), 인가(AuthZ), SSL Termination, Rate Limiting 처리. | **REST API** / **gRPC** 포워딩. JWT (JSON Web Token) 기반 보안 검증. | Spring Cloud Gateway, Kong, Nginx. `Path`, `Header` 기반 라우팅. |
| **Circuit Breaker** | **HALF-OPEN** 상태를 통해 장애 서비스의 **회복 여부를 탐색**하는 스위치 역할. | Netflix Hystrix(레거시), Resilience4j 주요 사용. 성공 실패 카운터를 기반으로 상태(State Machine) 전이. | `FailureRate`, `SlidingWindowSize`, `WaitDurationInOpenState`. |
| **Saga Coordinator** | 분산 트랜잭션의 흐름 제어. 각 서비스의 로컬 트랜잭션을 순차적으로 호출하고, 실패 시 보상 로직(Compensating Transaction) 실행. | **Choreography** (이벤트 기반 Pub/Sub), **Orchestration** (중앙 집중 제어). 메시징 프로토콜: **AMQP**, **Kafka**. | Saga Log를 통한 실행 내역 기록 (Crash Safety). |
| **BFF** (Backend For Frontend) | 특정 클라이언트(Web/Mobile/IoT)의 UI/UX 요구사항에 맞춰 데이터를 **Aggregate** 하여 응답하는 프레젠테이션 계층. | **GraphQL** 혹은 REST Overfetching 해결. 서로 다른 Microservice에서 가져온 데이터를 조합(Composition). | Latency 최소화를 위한 Edge Computing 위치. |
| **Service Discovery** | 서비스의 동적 IP/Port 변화를 추상화. 서비스 등록(Registration) 및 검색(Discovery) 기능 제공. | **Netflix Eureka**, HashiCorp Consul, Consul, K8s DNS. 클라이언트 사이드 or 서버 사이드 패턴. | Health Check (Heartbeat) 주기, TTL (Time To Live). |

#### 2. 탄력성 메커니즘 (Circuit Breaker & Bulkhead)

**서킷 브레이커(Circuit Breaker, CB)**는 외부 서비스 호출 시 지속적인 실패가 예상되면, 즉시 에러를 반환하여 시스템 자원(Thread, Connection Pool)을 보호한다. 이는 **Client-side Resilience Pattern**이다.

**ASCII 구조 다이어그램: CB 상태 전이 및 흐름**

```ascii
        [State Transition Diagram: Circuit Breaker]

   (Initial)         (Failure Threshold Exceeded)
   --------  Call Failures?  --------------------->  OPEN  (Blocking Calls)
     |           (High Error Rate)                |
   CLOSED                                    (Wait Duration)
     |                                            |
     | <----------------------------------------  |
     |                 (Probe Request Success)    v
     |                                         HALF-OPEN
     | (Successful Call Resets to Closed)      (Allowing 1 Test)
     |----------------------------------------> |
                                                |
                                        (Test Call Failed)
                                                |
                                                v
                                             OPEN (Back to Block)

    [Data Flow Context]

    [Order Service]                           [Payment Service]
         |                                         ^
         | --- 1. Request CreateOrder ---->        | (Failures Mounting)
         |                                         |
         | --- 2. Timeout/500 Error --------------+
         |
         v
    [Circuit Breaker Module] (Inside Order Service)
         |
         | -- (Logic: Error Rate > 50%) --
         |
         v
    [Fallback Logic]
         | -- "Please try again later" -- > [Client App]
```

**해설 (Deep Dive)**
1.  **CLOSED (폐쇄)**: 정상 상태. 모든 요청이 대상 서비스로 전달됨. 내부 카운터(Sliding Window)에서 실패 횟수를 모니터링함.
2.  **OPEN (개방)**: 실패 임계치(Threshold) 도달 시 즉시 전환. 모든 요청을 차단하고 즉시 **Fallback(대안)** 로직 수행.
3.  **HALF-OPEN (반개방)**: 일정 시간(`Sleep Window`) 후, 회복 여부 확인을 위해 1회의 테스트 요청을 허용.
4.  **Fallback**: 데이터베이스의 캐시된 값을 반환하거나, 기본값을 반환하여 사용자 경험을 최악의 경우(I/O Hang)라도 방지함.

#### 3. 데이터 일관성 메커니즘 (Saga Pattern)

분산 트랜잭션에서 **ACID (Atomicity, Consistency, Isolation, Durability)**를 완벽하게 보장하는 **2PC (Two-Phase Commit)**는 Lock에 따른 성능 저하(Synchronous Blocking)로 인해 MSA에 부적합하다. Saga는 각 서비스가 로컬 트랜잭션을 수행하고, 이벤트를 통해 전체를 조정하는 **BASE (Basically Available, Soft state, Eventually consistent)** 모델을 따른다.

**핵심 알고리즘 및 코드 흐름 (Choreography Saga)**

```python
# 가상의 Saga Orchestration 로직 (Pseudo-code)
class OrderSaga:
    def execute_order(self, order_dto):
        saga_log = begin_transaction()
        try:
            # 1. Local Transaction: Order Service
            order_id = OrderRepo.save(order_dto)
            saga_log.append("OrderCreated", order_id)

            # 2. Remote Transaction: Payment Service (Sync/Async)
            payment_resp = PaymentClient.pay(order_id, order_dto.amount)
            if payment_resp.status != "SUCCESS":
                raise PaymentFailedException() # Trigger Compensation

            # 3. Remote Transaction: Stock Service
            stock_resp = StockClient.decrease(order_id, order_dto.items)
            saga_log.append("OrderCompleted", order_id)
            commit_saga(saga_log)

        except Exception as e:
            # 보상 트랜잭션 실행 (역순)
            saga_log.compensating()
            if saga_log.has("OrderCreated"):
                PaymentClient.refund(order_id) # 2. 환불
            OrderRepo.cancel(order_id)         # 1. 주문 취소
            raise SagaRollbackException()
```

**핵심 포인트**: Saga의 가장 큰 위험은 **Isolation(격리성) 부재**로 인한 데이터 오염이다. 이를 방지하기 위해 **Semantic Lock(의미적 잠금, 예: 재고 차감 필드에 Version 관리)**이나 **Pessimistic Locking(비관적 락)**을 로컬 트랜잭션 내에서 수행해야 한다.

📢 **섹션 요약 비유**: 서킷 브레이커는 **"고압 전류가 흐를 때 과부하로 회로가 타지 않도록 자동으로 끊어지는 퓨즈(Fuse)"**이고, Saga 패턴은 **"여행사 패키지 예약에서 비행기는 예약했으나 호텔이 만실일 경우, 자동으로 비행기 표를 취소하고 환불해 주는 에이전트의 일련의 보상 절차"**와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

MSA 패턴들은 단순히 독립적으로 쓰이지 않으며, 타 아키텍처 영역과의 융합 및 상충 관계를 이해해야 한다.

#### 1. 심층 기술 비교: Saga vs 2PC

| 구분 | Saga Pattern | 2PC (Two-Phase Commit) |
|:---|:---|:---|
| **동기/비동기** | **Asynchronous (비동기)** / Non-Blocking | **Synchronous (동기)** / Locking Blocking |
| **성능 (TPS)** | **높음** (Lock이 걸리지 않아 병행 처리 가능) | **낮음** (모든 참여자가 Commit 로그 기록 대기) |
| **일관성 모델** | **Eventually Consistent (결과적 일관성)** | **Strong Consistency (강한 일관성)** |
| **가용성** | 높음 (일부 서비스 장애 시 Saga 로그로 재개 가능) | 낮음 (Coordinator 장애 시 전체 트랜잭션 불가) |
| **복잡도** | **높음** (Compensation 로직 직접 구현 필요) | 낮음 (미들웨어/DB 차원 지원) |
| **적용 분야** | 이커머스 주문, 항공권 발권 (대용량 트랜잭션) | 금융 계좌이체 (잔고 일관성이 중요한 소량 트랜잭션) |

#### 2. 과목 융합 관점 (시너지 및 오버헤드)

**1) 네트워크 (Network) & BFF**
BFF (Backend For Frontend)는 네트워크 트래픽을 최적화하는 핵심 패턴이다. 모바일 앱이 5개의 마이크로서비스에서 데이터를 가져오기 위해 5번의 HTTP 요청을 보내는 것(Slow Network 환경에서 치명적) 대신, BFF 서버에서 1번의 요청을 받아 내부적으로 MSA들을 호출하고 Aggregation하여 응답한다. 이는 **Round Trip Time (RTT)**을 획기적으로 줄인다.
*   **Synergy**: **CDN (Content Delivery Network)** 엣지 위치에 BFF를 배치하여 글로벌 Latency를 최소화하는 **Edge Computing Architecture**와 결합.

**2) 데이터베이스 (Database) & Saga**
Saga는 각 서비스가 **Database per Service** 패턴을 따르므로, 서로 다른 DBMS(e.g., MySQL, MongoDB, Redis) 간의 통합을 의미한다. 이때 **Transactional Outbox** 패턴을 사용하여, 로컬 DB 트랜잭션과 메시지 큐(Kafka 등)의 전송을 원자적으로 묶어야 메시지 유실을 방지할 수 있다.
*   **Tech Convergence**: CDC (Change Data Capture) 기술인 **Debezium**을 통해 DB 로그를 캡쳐하여 Saga 이벤트로 발행하는 방식이 강력된다.

📢 **섹션 요약 비유**: MSA 패턴 융합은 **"영화 제작 팀"**과 같습니다. **감독(BFF)**이 각 스태프(마이크로서비스)에게 지시를 내려 결과물을 취합하고, **현장 감독(Saga)**은 촬영 순서를 관리하며 실수가 나면 다시 찍도록(Compensating) 조율합니다. 만약 스태프가 다치면(Circuit Breaker), 대역을 쓰거나 해당 장면을 생략(Fallback)하여 영화 개봉(서비스 안정성)을 맞추는 것입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오: 대규모 커머스 플랫폼 구축**

*   **상황**: 'A' 쇼핑몰은 블랙프라이데이 이벤트를 앞두고 모놀리스 시스템을 M