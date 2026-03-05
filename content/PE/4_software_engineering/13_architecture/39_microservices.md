+++
title = "39. 마이크로서비스 아키텍처 (Microservices Architecture)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Microservices", "API-Gateway", "Service-Discovery", "Saga", "Circuit-Breaker"]
draft = false
+++

# 마이크로서비스 아키텍처 (Microservices Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이크로서비스는 **\"대형 **애플리케이션**을 **작은 **독립 **서비스**로 **분해**하여 **각각 **별도 **프로세스**로 **배포**하고 **API**로 **통신**하는 **아키텍처\"**로, **단일 **책임**(Single Responsibility), **독립 **배포**, **기술 ** heterogeneity**를 **지향**한다.
> 2. **구조**: **API Gateway**(Kong, **Ambassador)**가 **외부 **요청**을 **받고 **Service Discovery**(Consul, **Eureka**, **etcd)**로 **서비스**를 **찾으며 **Service Mesh**(Istio, **Linkerd**)가 **서비스 **간 **통신**을 **관리**한다.
> 3. **패턴**: **Saga Pattern**(분산 **트랜잭션), **Circuit Breaker**(Hystrix, **Resilience4j)**, **API Versioning**, **Event-Driven **Architecture**(Kafka, **RabbitMQ)**로 **안정성**과 **확장성**을 **보장**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
마이크로서비스는 **"서비스 분산화"**이다.

**모놀리식 vs 마이크로서비스**:
| 구분 | 모놀리식 | 마이크로서비스 |
|------|----------|----------------|
| **배포** | 전체 | 서비스별 |
| **스케일링** | 전체 | 서비스별 |
| **기술스택** | 단일 | 다양 |
| **복잡도** | 낮음 | 높음 |

### 💡 비유
마이크로서비스는 ****전문 **의료 **진 ****과 같다.
- **모놀리식**: 일반의 (모든 것 처리)
- **마이크로서비스**: 전문의 (각각의 역할)

---

## Ⅱ. 아키텍처 및 핵심 원리

### 마이크로서비스 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Microservices Architecture                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Client (Web/Mobile)                                                                   │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  https://api.example.com/users/123                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  API Gateway (Kong, Ambassador, AWS API Gateway)                                     │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  • Authentication: JWT validation, OAuth2                                        │  │  │  │
    │  │  │  • Rate Limiting: 100 req/min per API key                                        │  │  │  │
    │  │  │  • Routing: /users/* → user-service, /orders/* → order-service                   │  │  │  │
    │  │  │  • Load Balancing: Round robin across service instances                          │  │  │  │
    │  │  │  • Response Aggregation: Combine multiple service responses                       │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Service Discovery (Consul, Eureka, etcd)                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Service Registry: user-service → [10.0.1.5:8001, 10.0.1.6:8001, 10.0.1.7:8001]      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Microservices (Independent Processes)                                               │  │  │
    │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │  │
    │  │  │ User Service │  │ Order Service│  │ Product Svc  │  │ Payment Svc  │               │  │  │
    │  │  │ (Go)         │  │ (Java)       │  │ (Node.js)    │  │ (Python)     │               │  │  │
    │  │  │              │  │              │  │              │  │              │               │  │  │
    │  │  │ 10.0.1.5:8001│  │ 10.0.2.5:9001│  │ 10.0.3.5:7001│  │ 10.0.4.5:6001│               │  │  │
    │  │  │ 10.0.1.6:8001│  │ 10.0.2.6:9001│  │ 10.0.3.6:7001│  │ 10.0.4.6:6001│               │  │  │
    │  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Service Mesh (Istio)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Service Mesh Architecture                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Without Service Mesh:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Service A → Service B → Service C                                                      │  │
    │  ┌──────────┐   ┌──────────┐   ┌──────────┐                                            │  │
    │  │ app code │──→│ app code │──→│ app code │                                            │  │
    │  └──────────┘   └──────────┘   └──────────┘                                            │  │
    │  • Each service implements retry, timeout, circuit breaker                               │  │
    │  • Cross-cutting concerns scattered across services                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    With Istio Service Mesh:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Service A           Service B           Service C                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Application Container                                                          │  │  │  │
    │  │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │  │  │
    │  │  │  │  app code (business logic only, no network logic)                            │  │  │  │  │
    │  │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Envoy Proxy (Sidecar) - Intercepts all traffic                                  │  │  │  │
    │  │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │  │  │
    │  │  │  │  • mTLS: Mutual TLS for service-to-service encryption                        │  │  │  │  │
    │  │  │  │  • Traffic Management: Canary, Blue-Green deployment                         │  │  │  │  │
    │  │  │  │  • Observability: Metrics, Logs, Traces auto-collected                       │  │  │  │  │
    │  │  │  │  • Resilience: Retry, Timeout, Circuit Breaker, Rate Limiting                 │  │  │  │  │
    │  │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                                │  │
    │  → App code专注于业务逻辑，网络功能全部交给Sidecar Proxy                                         │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 통신 패턴 비교

| 패턴 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **Synchronous** | REST/HTTP | 간단 | 지연 |
| **Asynchronous** | Message Queue | decoupling | 복잡 |
| **Event-Driven** | Pub/Sub | 확장 | 일관성 |

### Saga Pattern (분산 트랜잭션)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Saga Pattern - Order Processing                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Problem: Create Order (requires multiple services)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Order Service: Create order                                                         │  │
    │  2. Payment Service: Process payment                                                     │  │
    │  3. Inventory Service: Reserve stock                                                     │  │
    │  4. Shipping Service: Schedule shipment                                                  │  │
    │                                                                                         │  │
    │  Challenge: What if payment succeeds but inventory reservation fails?                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution: Choreography Saga (Event-Driven)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Order Service                                                                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Create order (PENDING state)                                                      │  │  │
    │  │  2. Emit OrderCreated event                                                          │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Kafka                                                                      │  │
    │  Payment Service                                                                        │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Consume OrderCreated                                                             │  │  │
    │  │  2. Process payment                                                                   │  │  │
    │  │  3. If success: Emit PaymentSucceeded                                                │  │  │
    │  │     If failure: Emit PaymentFailed → Order cancels                                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Kafka                                                                      │  │
    │  Inventory Service                                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Consume PaymentSucceeded                                                          │  │  │
    │  │  2. Reserve stock                                                                     │  │  │
    │  │  3. If success: Emit InventoryReserved                                                │  │  │
    │  │     If failure: Emit InventoryFailed → Emit RefundPayment → Refund                    │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ Kafka                                                                      │  │
    │  Order Service (Complete)                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Consume InventoryReserved → Update order to CONFIRMED                               │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Circuit Breaker Pattern

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Circuit Breaker States                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CLOSED (Normal Operation)                                                              │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Requests pass through to downstream service                                       │  │  │
    │  │  • Track failures                                                                     │  │  │
    │  │  • If failure rate > threshold (e.g., 50% failure in last 10 requests):               │  │  │
    │  │    → Transition to OPEN                                                              │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  OPEN (Circuit Open)                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • All requests fail immediately (no actual call to downstream)                       │  │  │
    │  │  • Return cached fallback response or error                                          │  │  │
    │  │  • After timeout (e.g., 60 seconds): Attempt transition to HALF_OPEN                 │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼                                                                             │  │
    │  HALF_OPEN (Testing)                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Allow limited requests (e.g., 3 requests) to test if downstream recovered         │  │  │
    │  │  • If success: Transition to CLOSED                                                   │  │  │
    │  │  • If failure: Transition back to OPEN                                                │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Implementation (Resilience4j - Java):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CircuitBreakerConfig config = CircuitBreakerConfig.custom()                             │  │
    │      .failureRateThreshold(50)           // 50% failure rate triggers open               │  │
    │      .waitDurationInOpenState(Duration.ofSeconds(60))  // Wait 60s before half-open      │  │
    │      .permittedNumberOfCallsInHalfOpenState(3)   // 3 test calls in half-open           │  │
    │      .slidingWindowType(SlidingWindowType.COUNT_BASED)                                  │  │
    │      .slidingWindowSize(10)               // Last 10 calls                              │  │
    │      .build();                                                                              │  │
    │                                                                                         │  │
    │  CircuitBreakerRegistry registry = CircuitBreakerRegistry.of(config);                     │  │
    │  CircuitBreaker cb = registry.circuitBreaker("paymentService");                           │  │
    │                                                                                         │  │
    │  // Use in service call                                                                   │  │
    │  Supplier<PaymentResult> supplier = CircuitBreaker                                       │  │
    │      .decorateSupplier(() -> paymentService.process(payment), cb);                        │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 전자상거래 마이크로서비스
**상황**: 대규모 트래픽, 블랙프라이데이
**판단**: Kubernetes + Istio + Kafka

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         E-Commerce Microservices Design                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Services:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Frontend: React SPA (CDN)                                                           │  │
    │  2. API Gateway: Kong (rate limit, auth, routing)                                       │  │
    │  3. Product Service: Product catalog, search (Elasticsearch)                            │  │
    │  4. Order Service: Order management                                                      │  │
    │  5. Payment Service: Payment processing                                                  │  │
    │  6. Inventory Service: Stock management                                                  │  │
    │  7. Notification Service: Email/SMS                                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Deployment (Kubernetes):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # product-service deployment (scale: 10 pods)                                           │  │
    │  apiVersion: apps/v1                                                                     │  │
    │  kind: Deployment                                                                       │  │
    │  metadata:                                                                               │  │
    │    name: product-service                                                                │  │
    │  spec:                                                                                   │  │
    │    replicas: 10                                                                          │  │
    │    selector:                                                                             │  │
    │      matchLabels:                                                                        │  │
    │        app: product-service                                                             │  │
    │    template:                                                                             │  │
    │      metadata:                                                                           │  │
    │        labels:                                                                           │  │
    │          app: product-service                                                           │  │
    │          version: v2                                                                    │  │
    │      spec:                                                                               │  │
    │        containers:                                                                       │  │
    │        - name: product-service                                                          │  │
    │          image: product-service:v2                                                       │  │
    │          resources:                                                                      │  │
    │            requests:                                                                     │  │
    │              memory: "256Mi"                                                             │  │
    │              cpu: "250m"                                                                 │  │
    │            limits:                                                                       │  │
    │              memory: "512Mi"                                                             │  │
    │              cpu: "500m"                                                                 │  │
    │          livenessProbe:                                                                  │  │
    │            httpGet:                                                                      │  │
    │              path: /health                                                               │  │
    │              port: 8001                                                                  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### 마이크로서비스 기대 효과

| 효과 | 모놀리식 | 마이크로서비스 |
|------|----------|----------------|
| **배포** | 전체 | 서비스별 |
| **확장** | 전체 | 서비스별 |
| **복잡도** | 코드 | 네트워크 |
| **팀** | 대형 | 소형 |

### 모범 사례

1. **DDD**: Domain-driven design
2. **API**: Version from v1
3. **Observability**: Distributed tracing
4. **Automation**: CI/CD 필수

### 미래 전망

1. **Serverless**: FaaS + Microservices
2. **Service Mesh**: 표준화
3. **Event-Driven**: Kafka 기반
4. **Multi-cloud**: Portable services

### ※ 참고 표준/가이드
- **CNCF**: Cloud Native Landscape
- **Kubernetes**: k8s.io/docs
- **Istio**: istio.io/docs

---

## 📌 관련 개념 맵

- [컨테이너](./9_virtualization/35_container.md) - 배포 단위
- [CI/CD](./10_cicd/36_ci_cd_tools.md) - 자동화
- [API 설계](./6_api/34_api_design.md) - RESTful

