+++
title = "618. 서킷 브레이커 (Circuit Breaker) 장애 연쇄 차단 메커니즘"
date = "2026-03-15"
[extra]
categories = "studynote-se"
+++

# 서킷 브레이커 (Circuit Breaker) 장애 연쇄 차단 메커니즘

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 원격 서비스 호출 시 장애가 반복되면 **일시적으로 호출을 차단**하여 시스템 전체의 연쇄적 장애(Cascading Failure) 방지
> 2. **가치**: 빠른 실패(Fail Fast), 자원 보존, 자동 복구 → 가용성 99.9% 유지, 리소스 고갈 방지
> 3. **융합**: Resilience4j, Hystrix, Istio, Retry, Timeout, Fallback Pattern과 연계

---

## Ⅰ. 개요 (Context & Background) - [500자+]

### 개념

**서킷 브레이커 (Circuit Breaker)**는 분산 시스템에서 **외부 서비스 장애가 전체 시스템으로 확산되는 것을 방지**하는 패턴입니다. 마치 전기의 과부하를 방지하기 위한 **회로 차단기(Circuit Breaker)**와 같은 원리로, 일정 횟수 이상 실패가 반복되면 **회로를 개방(Open)**하여 추가 호출을 차단합니다.

상태 전이(State Transition)는 세 가지로 구성됩니다:
1. **Closed (닫힘)**: 정상 상태, 요청 전달
2. **Open (열림)**: 장애 감지, 요청 차단 (즉시 실패 반환)
3. **Half-Open (반열림)**: 복구 확인을 위한 시험적 요청 허용

```
┌─────────────────────────────────────────────────────────────┐
│                   서킷 브레이커 개념                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [정상 상태: Closed]                                        │
│  ┌──────────┐    요청    ┌──────────┐                      │
│  │  Client  │───────────►│ Service  │  ◄─── 정상 응답      │
│  └──────────┘             └──────────┘                      │
│                                                             │
│  [장애 발생: 실패 임계값 도달]                              │
│  ┌──────────┐    요청    ┌──────────┐                      │
│  │  Client  │───────────►│ Service  │  ◄─── 타임아웃/에러  │
│  └──────────┘             └──────────┘                      │
│     │                                                    │
│     │ 5회 연속 실패                                       │
│     ▼                                                    │
│  [상태 전이: Open]                                        │
│  ┌──────────┐    요청    ┌──────────┐                      │
│  │  Client  │───X────────│ Circuit  │  ◄─── 즉시 실패!     │
│  └──────────┘  차단됨    │  Breaker │                      │
│                                  │                         │
│  [일정 시간 경과 후: Half-Open]                          │
│  ┌──────────┐   시험 요청  ┌──────────┐                    │
│  │  Client  │─────────────►│ Service  │  ◄─── 1회만 허용    │
│  └──────────┘   (1회만)    └──────────┘                    │
│     │                                                    │
│     │ 성공 → Closed, 실패 → Open                         │
└─────────────────────────────────────────────────────────────┘
```

### 💡 비유

**집의 전기 차단기**와 같습니다. 전기 과부하가 걸리면 차단기가 내려가서 정전을 일으키지만, 이는 화재를 방지하기 위함입니다. 일정 시간이 지나면 다시 전기를 켜서(반열림) 정상인지 확인합니다. 마찬가지로, 서비스 장애 시 일부 요청을 실패시키더라도 전체 시스템의 붕괴를 방지하는 것이 목표입니다.

### 등장 배경

| 단계 | 한계점 | 혁신적 패러다임 |
|:---:|:---|:---|
| **① 동기 호출** | 외부 서비스 장애 시 스레드 대기 | **스레드 풀 고갈(Thread Starvation)** |
| **② Retry만** | 재시도로 부하 증폭 | **재시도 폭발(Retry Storm)** |
| **③ Timeout만** | 대기 시간만 줄어듦 | **자원 여전히 점유** |
| **④ Circuit Breaker** | 빠른 실패 + 자원 보호 | **탄력성(Resilience) 확보** |

현재의 비즈니스 요구로서는 **클라우드 환경의 예측 불가능한 장애, 마이크로서비스 간 연쇄 실패 방지, 자가 치유(Self-healing)**이 필수적입니다.

### 📢 섹션 요약 비유

마치 **교통 통제**와 같습니다. 사고가 발생한 도로(서비스)를 미리 막아서(Open), 다른 차량들이 줄을 서서 기다리지 않게 합니다. 대체 경로(Fallback)를 안내하거나, 일정 시간 후에 도로가 복구되었는지 확인(Half-Open)합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 파라미터 | 비유 |
|:---|:---|:---|:---|:---|
| **Circuit Breaker** | 장애 감지 및 차단 | 성공/실패 카운트, 상태 관리 | failureThreshold, timeout | 차단기 |
| **State Machine** | 상태 전이 관리 | Closed → Open → Half-Open | waitDurationInOpenState | 상태 머신 |
| **Metrics Collector** | 성능 지표 수집 | sliding window 크기 | slidingWindowSize, minimumCalls | 계량기 |
| **Fallback** | 대체 로직 수행 | 캐시, 기본값 반환 | fallbackMethod | 비상 계단 |
| **Event Publisher** | 상태 변경 알림 | CircuitOpenEvent, CircuitResetEvent | - | 알림 시스템 |

### ASCII 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    서킷 브레이커 상태 전이 다이어그램                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                                                                             │
│    ┌─────────────────────────────────────────────────────────┐             │
│    │                                                         │             │
│    │   CLOSED (정상)                                         │             │
│    │   ┌─────────────────────────────────────────────────┐   │             │
│    │   │ • 요청을 서비스로 전달                           │   │             │
│    │   │ • 실패 횟수 카운트                               │   │             │
│    │   │ • 임계값 도달 시 OPEN으로 전이                   │   │             │
│    │   │                                                  │   │             │
│    │   │ [파라미터]                                       │   │             │
│    │   │ - failureThreshold: 5 (연속 실패 기준)          │   │             │
│    │   │ - slidingWindowSize: 100 (슬라이딩 윈도우)      │   │             │
│    │   │ - slowCallDurationThreshold: 2s (지연 임계값)   │   │             │
│    │   └─────────────────────────────────────────────────┘   │             │
│    │                                                         │             │
│    └───────────────────────┬─────────────────────────────────┘             │
│                           │                                                 │
│                           │ 실패율 > 50% OR                                │
│                           │ 연속 실패 > failureThreshold                    │
│                           │                                                 │
│                           ▼                                                 │
│    ┌─────────────────────────────────────────────────────────┐             │
│    │                                                         │             │
│    │   OPEN (장애 감지)                                     │             │
│    │   ┌─────────────────────────────────────────────────┐   │             │
│    │   │ • 모든 요청 즉시 실패 (CallNotPermittedException)│   │             │
│    │   │ • waitDurationInOpenState 동안 유지              │   │             │
│    │   │                                                  │   │             │
│    │   │ [파라미터]                                       │   │             │
│    │   │ - waitDurationInOpenState: 60s (기본값)         │   │             │
│    │   │ - permittedNumberOfCallsInHalfOpenState: 10     │   │             │
│    │   └─────────────────────────────────────────────────┘   │             │
│    │                                                         │             │
│    └───────────────────────┬─────────────────────────────────┘             │
│                           │                                                 │
│                           │ waitDurationInOpenState 경과                    │
│                           │                                                 │
│                           ▼                                                 │
│    ┌─────────────────────────────────────────────────────────┐             │
│    │                                                         │             │
│    │   HALF-OPEN (복구 확인)                                │             │
│    │   ┌─────────────────────────────────────────────────┐   │             │
│    │   │ • 제한된 수의 요청만 허용                        │   │             │
│    │   │ • 성공 시 CLOSED, 실패 시 OPEN으로 복귀         │   │             │
│    │   │                                                  │   │             │
│    │   │ [파라미터]                                       │   │             │
│    │   │ - permittedNumberOfCallsInHalfOpenState: 10     │   │             │
│    │   │   (반열림 상태에서 허용할 최대 호출 수)          │   │             │
│    │   └─────────────────────────────────────────────────┘   │             │
│    │                                                         │             │
│    └───────────────────────┬─────────────────────────────────┘             │
│                           │                                                 │
│         ┌─────────────────┴─────────────────┐                              │
│         │                                  │                              │
│    ▼    │                                  ▼    │                        │
│ 성공   │                               실패    │                        │
│         │                                  │                             │
│         ▼                                  ▼                             │
│  [CLOSED]                              [OPEN]                           │
│  복귀                                  재진입                             │
│                                                                             │
│                                                                             │
│  [이벤트 흐름]                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  1. StateTransitionEvent (CLOSED → OPEN)                         │     │
│  │     - 장애 알림, 모니터링 시스템 연동                             │     │
│  │  2. CircuitOpenEvent                                            │     │
│  │     - Fallback 로직 트리거                                       │     │
│  │  3. CircuitHalfOpenEvent                                         │     │
│  │     - 복구 시도 알림                                             │     │
│  │  4. CircuitClosedEvent                                          │     │
│  │     - 정상 복귀 알림                                             │     │
│  └──────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**해설**:

1. **Closed → Open 전이 조건**:
   - **Count-based**: slidingWindowSize 내에서 failureThreshold 이상 연속 실패
   - **Time-based**: slowCallDurationThreshold(예: 2초) 초과 호출이 비율(예: 50%) 이상
   - **예시**: 최근 100회 호출 중 51회 이상이 2초 이상 지연 → Open

2. **Open 상태 동작**:
   - 모든 요청이 **즉시 CallNotPermittedException**으로 실패
   - 외부 서비스로의 네트워크 호출 자체가 발생하지 않아 자원 절약
   - Fallback 메서드가 있다면 자동 실행

3. **Half-Open → Closed/Open 전이**:
   - permittedNumberOfCallsInHalfOpenState(예: 10회)만큼 시험 호출 허용
   - 모두 성공하면 Closed, 하나라도 실패하면 Open으로 복귀
   - **점진적 복구**를 통한 급작스러운 부하 방지

### 심층 동작 원리

```
① Sliding Window 기반 실패율 계산
   └─> 최근 N회(or T초) 호출의 성공/실패 추적
   └─> 실패율 = 실패 횟수 / 전체 호출 횟수
   └─> Count-based vs Time-based 선택 가능

② 임계값 도달 감지
   └─> 실패율 > failureThreshold(예: 50%)
   └─> OR 연속 실패 > failureThreshold(예: 5회)
   └─> 상태 전이 트리거 발생

③ Open 상태 진입
   └─> waitDurationInOpenState(예: 60초) 동안 유지
   └─> 모든 요청 CircuitOpenException 반환

④ Half-Open 상태 진입
   └─> waitDurationInOpenState 경과 후
   └─> permittedNumberOfCallsInHalfOpenState(예: 10회) 만큼 허용
   └─> 성공 시 Closed, 실패 시 Open

⑤ 상태 이벤트 발행
   └─> StateTransitionEvent
   └─> 모니터링 시스템에 전송
```

### 핵심 알고리즘 & 코드

```java
// ============ Resilience4j 서킷 브레이커 설정 (Spring Boot) ============

import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

/*
--- application.yml ---
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        registerHealthIndicator: true
        slidingWindowSize: 100           # 슬라이딩 윈도우 크기
        minimumNumberOfCalls: 10         # 최소 호출 수
        permittedNumberOfCallsInHalfOpenState: 10
        automaticTransitionFromOpenToHalfOpenEnabled: true
        waitDurationInOpenState: 60s     # Open 상태 유지 시간
        failureRateThreshold: 50         # 실패율 임계값 (%)
        slowCallRateThreshold: 100       # 지연 호출률 임계값 (%)
        slowCallDurationThreshold: 2s    # 지연 임계값
        recordExceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
        ignoreExceptions:
          - java.lang.IllegalArgumentException
*/

@Configuration
public class CircuitBreakerConfig {

    @Bean
    public CircuitBreakerRegistry circuitBreakerRegistry() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .slidingWindowSize(100)
            .slidingWindowType(SlidingWindowType.COUNT_BASED)  // COUNT_BASED or TIME_BASED
            .minimumNumberOfCalls(10)
            .failureRateThreshold(50)
            .waitDurationInOpenState(Duration.ofSeconds(60))
            .permittedNumberOfCallsInHalfOpenState(10)
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            .slowCallRateThreshold(100)
            .build();

        CircuitBreakerRegistry registry = CircuitBreakerRegistry.of(
            CircuitBreakerConfig.of("paymentService", config)
        );

        // 상태 변경 이벤트 리스너
        CircuitBreaker paymentCB = registry.circuitBreaker("paymentService");
        paymentCB.getEventPublisher()
            .onStateTransition(event ->
                log.info("State transition: {}", event)
            )
            .onFailure(event ->
                log.error("Failure: {}", event.getThrowable())
            )
            .onSuccess(event ->
                log.info("Success")
            );

        return registry;
    }
}

// ============ 서킷 브레이커 적용 서비스 ============

@Service
public class PaymentService {

    private final RestTemplate restTemplate;
    private final CircuitBreaker circuitBreaker;

    public PaymentService(RestTemplate restTemplate, CircuitBreakerRegistry registry) {
        this.restTemplate = restTemplate;
        this.circuitBreaker = registry.circuitBreaker("paymentService");
    }

    /**
     * 서킷 브레이커로 보호된 결제 호출
     */
    public PaymentResponse processPayment(PaymentRequest request) {
        // CircuitBreaker 데코레이터 적용
        Supplier<PaymentResponse> supplier = CircuitBreaker
            .decorateSupplier(circuitBreaker, () -> callPaymentAPI(request));

        // Fallback 제공
        Supplier<PaymentResponse> supplierWithFallback = Decorators
            .ofSupplier(supplier)
            .withFallback(CallNotPermittedException.class, throwable -> {
                log.warn("Circuit breaker is OPEN, using fallback");
                return getFallbackResponse(request);
            })
            .get();

        try {
            return supplierWithFallback.get();
        } catch (Exception e) {
            throw new PaymentProcessingException("Payment failed", e);
        }
    }

    /**
     * 실제 외부 API 호출
     */
    private PaymentResponse callPaymentAPI(PaymentRequest request) {
        return restTemplate.postForObject(
            "http://payment-service/api/payments",
            request,
            PaymentResponse.class
        );
    }

    /**
     * Fallback: 캐시된 결제 결과 반환
     */
    private PaymentResponse getFallbackResponse(PaymentRequest request) {
        // 캐시 확인 또는 기본값 반환
        return PaymentResponse.builder()
            .status("PENDING")
            .message("Payment is being processed")
            .build();
    }
}

// ============ 애너테이션 기반 사용 (Spring AOP) ============

@Service
public class OrderService {

    @CircuitBreaker(
        name = "paymentService",
        fallbackMethod = "paymentFallback"
    )
    public PaymentResponse processPayment(PaymentRequest request) {
        return restTemplate.postForObject(
            "http://payment-service/api/payments",
            request,
            PaymentResponse.class
        );
    }

    /**
     * Fallback 메서드
     * - 예외 타입을 매개변수로 받아야 함
     * - 같은 반환 타입이어야 함
     */
    private PaymentResponse paymentFallback(PaymentRequest request, Exception e) {
        log.warn("Payment service unavailable: {}", e.getMessage());

        // 1) 캐시된 결과 반환
        PaymentResponse cached = cacheService.getCachedPayment(request.getId());
        if (cached != null) {
            return cached;
        }

        // 2) 기본값 반환
        return PaymentResponse.builder()
            .status("PENDING")
            .message("Payment queued")
            .build();
    }
}

// ============ TypeScript/JavaScript 버전 (resilience4j-typescript) ============

/*
import {
    CircuitBreaker,
    CircuitBreakerConfig
} from 'resilience4j-typescript';

const circuitBreakerConfig = CircuitBreakerConfig.custom()
    .slidingWindowSize(100)
    .failureRateThreshold(50)
    .waitDurationInOpenState(60000)
    .permittedNumberOfCallsInHalfOpenState(10)
    .build();

const paymentCircuitBreaker = new CircuitBreaker(
    'paymentService',
    circuitBreakerConfig
);

// 상태 변경 이벤트 리스너
paymentCircuitBreaker.onStateTransition(event => {
    console.log(`State transition: ${event}`);
});

async function processPayment(request: PaymentRequest): Promise<PaymentResponse> {
    return paymentCircuitBreaker.execute(async () => {
        // 실제 API 호출
        return await axios.post('http://payment-service/api/payments', request);
    }, async (error) => {
        // Fallback
        console.error('Circuit breaker OPEN, using fallback');
        return {
            status: 'PENDING',
            message: 'Payment queued'
        };
    });
}
*/
```

### 📢 섹션 요약 비유

마치 **물탱크의 플로트 밸브(Float Valve)**와 같습니다. 물이 계속 흘러들면(장애 누적), 플로트가 떠올라 자동으로 물을 차단합니다(Open). 수위가 내려가면 다시 물을 받아들이기 시작합니다(Half-Open → Closed). 이로 인해 물탱크가 넘쳐흐르는 것(시스템 붕괴)을 방지합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

### 심층 기술 비교: 탄력성 패턴

| 패턴 | 목적 | 적용 시점 | 트레이드오프 |
|:---|:---|:---|:---|
| **Circuit Breaker** | 연쇄 장애 방지 | 장애 반복 | 일부 요청 실패 허용 |
| **Retry** | 일시적 장애 극복 | 네트워크 오류 | 재시도 폭발(Retry Storm) |
| **Timeout** | 무한 대기 방지 | 장기 응답 지연 | 빠른 실패 vs 미완료 |
| **Bulkhead** | 자원 격리 | 스레드 풀 고갈 | 리소스 사용량 증가 |
| **Fallback** | 대체 로직 제공 | 서비스 장애 | 데이터 일관성 문제 |

### 과목 융합 관점

**1) 네트워크 관점 (TCP/HTTP)**

서킷 브레이커는 **애플리케이션 계층의 탄력성 패턴**이지만, TCP 재전송과 유사한 철학을 공유합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    TCP 재전송 vs 서킷 브레이커              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [TCP 재전송]                                               │
│  ┌──────────┐    SYN       ┌──────────┐                    │
│  │  Client  │─────────────►│  Server  │                    │
│  └──────────┘              └────┬─────┘                    │
│     │                         │                           │
│     │  ACK 없음 (타임아웃)     │                           │
│     │                         ▼                           │
│  ┌──────────┐    재전송     ┌──────────┐                    │
│  │  Client  │─────────────►│  Server  │  ◄─── 네트워크 회복│
│  └──────────┘  (지수적 백오프)└──────────┘                    │
│                                                             │
│  [서킷 브레이커]                                            │
│  ┌──────────┐    요청       ┌──────────┐                    │
│  │  Client  │─────────────►│  Server  │                    │
│  └──────────┘  (CB Closed) └──────────┘                    │
│     │                         │                           │
│     │  연속 실패 (5회)          │                           │
│     │                         ▼                           │
│  ┌──────────┐    차단       ┌──────────┐                    │
│  │  Client  │─────X─────────│ Circuit  │  ◄─── 빠른 실패    │
│  └──────────┘  (CB Open)     │ Breaker  │                    │
└─────────────────────────────────────────────────────────────┘
```

TCP는 네트워크 패킷 손실을 복구하고, 서킷 브레이커는 애플리케이션 장애를 복구합니다.

**2) 운영체제 관점 (장애 감지)**

운영체제의 **워치독 타이머(Watchdog Timer)**와 유사합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                  Watchdog Timer vs Circuit Breaker          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Watchdog Timer]                                           │
│  ┌─────────────────────────────────────────────┐           │
│  │  Main Loop                                  │           │
│  │  ┌────────┐                               │           │
│  │  │ Task   │───► watchdog_reset()  ◄─────┐  │           │
│  │  └────────┘                            │  │           │
│  │        │                               │  │           │
│  │        │ Task Hang (응답 없음)           │  │           │
│  │        │                               │  │           │
│  │  ┌────▼─────────┐                     │  │           │
│  │  │ Timeout!     │                     │  │           │
│  │  │ System Reset │─────────────────────┘  │           │
│  │  └──────────────┘                        │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  [Circuit Breaker]                                          │
│  ┌─────────────────────────────────────────────┐           │
│  │  Remote Call                                │           │
│  │  ┌────────┐                               │           │
│  │  │Request │───► Service Call              │           │
│  │  └────────┘     ↓                         │           │
│  │        │      Response (Success)           │           │
│  │        │      reset_failure_count()        │           │
│  │        │                                 │           │
│  │        │ Timeout/Error (5회 연속)         │           │
│  │        │                                 │           │
│  │  ┌────▼─────────┐                        │           │
│  │  │ Circuit Open │                        │           │
│  │  │ Fast Fail    │                        │           │
│  │  └──────────────┘                        │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유

마치 **교통 정체 관제 시스템**과 같습니다. 고속도로에 사고가 발생하면, 진입 전 단계에서 진입을 막아서(Open) 정체를 확산 방지합니다. 사고가 정리되면, 소량의 차량을 통과시켜(Half-Open) 도로가 정상인지 확인한 후, 전면 개방(Closed)합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [800자+]

### 실무 시나리오

**Scenario 1: 핀테크 결제 서비스**

```
┌─────────────────────────────────────────────────────────────┐
│                 서킷 브레이컈 적용 예시                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [PG사 연동 장애 시나리오]                                   │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │Order Service │─────►│  PG Service  │                   │
│  └──────────────┘      └──────┬───────┘                   │
│                              │                            │
│                              │ 장애 발생!                  │
│                              ▼                            │
│  [Without Circuit Breaker]                            │
│  - 스레드 풀 고갈                                      │
│  - 전체 주문 시스템 마비                                │
│  - 고객 불만 폭주                                      │
│                                                             │
│  [With Circuit Breaker]                               │
│  1. 5회 연속 타임아웃 → OPEN                            │
│  2. 즉시 Fallback 실행                                   │
│     - 캐시된 환율 사용                                    │
│     - "결제 대기 중" 메시지                              │
│  3. 백그라운드로 재시도 (메시지 큐)                       │
│  4. PG사 복구 확인 → HALF-OPEN → CLOSED                   │
└─────────────────────────────────────────────────────────────┘
```

**의사결정 과정**:
1. **임계값 설정**: 실패율 50%, 연속 실패 5회
2. **대기 시간**: 60초 (PG사 복구 시간 고려)
3. **Fallback 전략**: 캐시 → 기본값 → 메시지 큐

**Scenario 2: 스트리밍 서비스 추천 엔진**

```java
@Service
public class RecommendationService {

    @CircuitBreaker(
        name = "recommendationEngine",
        fallbackMethod = "getFallbackRecommendations"
    )
    public List<Product> getRecommendations(String userId) {
        // ML 기반 추천 엔진 호출
        return mlClient.getPersonalizedProducts(userId);
    }

    /**
     * Fallback: 인기 상품 목록 반환
     */
    private List<Product> getFallbackRecommendations(String userId, Exception e) {
        log.warn("ML engine unavailable, using popularity-based fallback");

        // 1) 캐시된 인기 상품 반환
        List<Product> popular = cacheService.getPopularProducts();
        if (!popular.isEmpty()) {
            return popular;
        }

        // 2) 데이터베이스에서 인기 상품 조회
        return productRepository.findTop20ByOrderBySalesDesc();
    }
}
```

### 도입 체크리스트

**기술적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **임계값 설정** | 실패율, 연속 실패, 지연 임계값 | |
| **슬라이딩 윈도우** | Count-based vs Time-based 선택 | |
| **Fallback 정책** | 캐시, 기본값, 메시지 큐 | |
| **상태 이벤트** | 모니터링 시스템 연동 | |
| **Health Check** | 서킷 상태 노출 (/actuator/health) | |
| **테스트** | 장애 주입(Chaos Monkey) 테스트 | |

**운영·보안적 체크리스트**

| 항목 | 확인 사항 | 점수 (1-5) |
|:---|:---|:---:|
| **모니터링** | Prometheus + Grafana 대시보드 | |
| **알림** | CircuitOpenEvent 시 PagerDuty | |
| **로그** | 상태 전이 로그 추적 | |
| **복구 절차**** | 수동 복구 스크립트 준비 | |

### 안티패턴

**❌ 잘못된 Fallback 구현**

```java
// 안티패턴: Fallback에서 예외를 다시 던짐
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() {
    return remoteService.call();
}

private Response fallback(Exception e) {
    // ❌ Fallback에서 예외 발생 → 효과 없음
    throw new RuntimeException("Service unavailable", e);
}
```

**개선 방안**:

```java
// 올바른 패턴: Fallback에서 항상 유효한 값 반환
@CircuitBreaker(name = "service", fallbackMethod = "fallback")
public Response callService() {
    return remoteService.call();
}

private Response fallback(Exception e) {
    // ✅ 항상 유효한 응답 반환
    return Response.builder()
        .status("DEGRADED")
        .data(getCachedData())
        .build();
}
```

### 📢 섹션 요약 비유

마치 **비상 발사대**와 같습니다. 정상 상황(Closed)에서는 정상 근무하지만, 비상 상황(Open)이 되면 즉시 대기 태세로 전환합니다. 상황이 안정되면(Half-Open), 소규모 정찰대를 보내 확인 후 정상 근무를 재개합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard) - [400자+]

### 정량/정성 기대효과

| 지표 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **연쇄 장애율** | 월 2회 (전체 마비) | 월 0회 (부분 장애로 격리) | **100% 방지** |
| **평균 응답 시간** | 5초 (타임아웃 대기) | 50ms (즉시 실패) | **99% 개선** |
| **자원 사용량** | 스레드 풀 100% 소진 | 30% 사용 | **70% 절감** |
| **복구 시간** | 수동 재시작 30분+ | 자동 복구 1분 이내 | **97% 단축** |
| **고객 경험** | "서비스 불안정" 불만 | "일시적 지연" 인지 | **CSAT 40% 향상** |

### 미래 전망

1. **AI 기반 예측적 서킷 브레이커**: ML로 장애 예측하여 선제적으로 차단
2. **서비스 메시 통합**: Istio/VirtualMachine의 Circuit Breaking
3. **글로벌 서킷 브레이커**: 리전 간 장애 격리
4. **자동 튜닝**: A/B 테스트 기반 최적 임계값 자동 결정

### 참고 표준

- **Release It!** (Michael Nygard) - 서킷 브레이커 패턴 원본
- **Resilience4j Documentation**
- **Hystrix Documentation** (Netflix, deprecated but reference)
- **Spring Cloud Circuit Breaker**
- **Istio Circuit Breaking**

### 📢 섹션 요약 비유

미래의 서킷 브레이커는 **자율 주행 자동차의 충돌 방지 시스템**과 같이 발전할 것입니다. 단순히 장애를 감지하는 것을 넘어, **예측 모델을 통해 장애를 미리 예방**하고, **자가 치유(Self-healing)**를 통해 인간 개입 없이 시스템을 복구할 것입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[마이크로서비스 아키텍처](./556_msa.md)**: MSA 전체 패턴
- **[서비스 디스커버리](./617_service_discovery.md)**: Eureka와 연계
- **[재시도 패턴](./retry_pattern.md)**: 재시도 전략
- **[벌크헤드 패턴](./bulkhead_pattern.md)**: 자원 격리
- **[Fallback 패턴](./fallback_pattern.md)**: 대체 로직 설계

### 👶 어린이를 위한 3줄 비유 설명

**1) 개념**: 집의 **전기 차단기**와 같습니다. 전기가 너무 많이 사용되거나 합선이 발생하면, 차단기가 떨어져서 정전이 되지만 화재를 막아줍니다.

**2) 원리**: 컴퓨터 프로그램도 마찬가지입니다. 어떤 서비스가 계속 실패하면, 그 서비스를 잠깐 끊어버려서(Open) 다른 부분에까지 문제가 퍼지지 않게 합니다. 나중에 다시 시도해서(Half-Open) 괜찮아지면 다시 연결합니다(Closed).

**3) 효과**: 하나의 서비스가 고장 나더라도, 전체 시스템이 멈추는 일을 막아줍니다. 마치 전기 차단기가 불이 나는 것을 막아주듯이, 서킷 브레이커는 시스템 붕괴를 막아줍니다.
