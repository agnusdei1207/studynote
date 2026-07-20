---
title: "Gateway MSA Entry Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 239
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: API 게이트웨이 (API Gateway) 는 MSA (Microservices Architecture) 의 모든 외부 요청이 통과하는 단일 진입점으로, 인증·라우팅·로드밸런싱·속도제한을 중앙화한다.
> 2. **가치**: 클라이언트가 개별 마이크로서비스의 내부 구조를 알 필요가 없어 결합도가 낮아지고, 횡단 관심사 (Cross-Cutting Concerns) 를 서비스 코드 밖에서 처리한다.
> 3. **판단 포인트**: 게이트웨이가 SPoF (Single Point of Failure: 단일 장애점) 이 될 수 있으므로, 고가용성 (HA: High Availability) 구성과 회로 차단기 (Circuit Breaker) 가 필수다.

---

## Ⅰ. 개요 및 필요성
모놀리식 (Monolithic) 아키텍처에서는 단일 서버가 모든 요청을 처리했다. MSA (Microservices Architecture) 로 전환하면 주문 서비스, 결제 서비스, 사용자 서비스 등 수십 개의 마이크로서비스가 각자의 포트와 프로토콜을 가진다.

클라이언트(모바일 앱, 웹 브라우저)가 이 모든 서비스의 주소를 알아야 한다면:

- <strong>서비스 변경 시 클라이언트도 수정</strong> 필요
- <strong>인증·로깅이 서비스마다 중복</strong> 구현
- <strong>CORS (Cross-Origin Resource Sharing) 정책 서비스마다 개별</strong> 설정

API 게이트웨이는 이 모든 문제를 해결하는 <strong>MSA의 정문</strong>이다.

API 게이트웨이가 동기 HTTP (HyperText Transfer Protocol) 요청의 진입점이라면, <strong>메시지 게이트웨이 (Message Gateway)</strong> 는 비동기 메시지 채널(Kafka, RabbitMQ)에서 동일한 역할을 수행한다—메시지 포맷 변환, 라우팅, 필터링.

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 쇼핑몰 백화점의 정문 안내 데스크처럼, API 게이트웨이는 모든 방문객(요청)을 맞이하고 적절한 매장(서비스)으로 안내한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+------------------------------------------------------------------+
|                    API Gateway 아키텍처                           |
|                                                                  |
|  [클라이언트]                                                     |
|  Mobile App -----+                                               |
|  Web Browser ----+                                               |
|  Partner API ----+                                               |
|                  v                                               |
|         +----------------------------------------+               |
|         |          API Gateway                   |               |
|         |  +---------------------------------+   |               |
|         |  |  1. SSL 종료 (TLS Termination)   |   |               |
|         |  |  2. 인증/인가 (Auth/AuthZ)        |   |               |
|         |  |  3. 요청 라우팅 (Routing)         |   |               |
|         |  |  4. 속도 제한 (Rate Limiting)     |   |               |
|         |  |  5. 요청 집계 (Aggregation)       |   |               |
|         |  |  6. 로드 밸런싱 (Load Balancing)  |   |               |
|         |  |  7. 캐싱 (Caching)               |   |               |
|         |  +---------------------------------+   |               |
|         +------------------+-------------------+               |
|                            |                                     |
|          +-----------------+----------------------+             |
|          v                 v                       v             |
|  +--------------+  +--------------+  +--------------------+     |
|  | User Service |  | Order Service|  |  Payment Service   |     |
|  | :8081        |  | :8082        |  |  :8083             |     |
|  +--------------+  +--------------+  +--------------------+     |
+------------------------------------------------------------------+
```

단일 게이트웨이 대신 클라이언트 유형별로 최적화된 게이트웨이를 두는 패턴:

```
Mobile App  --->  Mobile BFF  --->  마이크로서비스들
Web App     --->  Web BFF     --->  마이크로서비스들
Partner     --->  Partner GW  --->  마이크로서비스들
```

| 기능 | 설명 | 대표 구현 |
|:---|:---|:---|
| 라우팅 (Routing) | URL -> 서비스 매핑 | Spring Cloud Gateway, Kong |
| 인증 (Authentication) | JWT (JSON Web Token) 검증 | OAuth2 통합 |
| 속도 제한 (Rate Limiting) | 초당 요청 수 제한 | Redis 기반 카운터 |
| 서킷 브레이커 (Circuit Breaker) | 장애 서비스 격리 | Resilience4j |
| 집계 (Aggregation) | 여러 서비스 결과 합산 | GraphQL Gateway |

- **📢 섹션 요약 비유**: 게이트웨이는 공항 관제탑이다. 모든 비행기(요청)의 이착륙(라우팅)을 관리하고, 악천후(서비스 장애) 시 회항(Circuit Breaker)을 결정한다.

---

## Ⅲ. 비교 및 연결
| 제품 | 유형 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| Kong | 오픈소스 + 상용 | Lua 플러그인, 고성능 | 대규모 기업 |
| AWS API Gateway | 클라우드 관리형 | Lambda 통합, 서버리스 | AWS 환경 |
| Spring Cloud Gateway | Java 기반 | Reactor 비동기, Spring 통합 | Spring Boot MSA |
| Nginx (엔진엑스) | 범용 리버스 프록시 | 경량, 빠름 | 간단한 라우팅 |
| Istio Service Mesh | 서비스 메시 | 사이드카 방식, mTLS | Kubernetes 환경 |

| 항목 | API Gateway | Service Mesh (Istio) |
|:---|:---|:---|
| 위치 | 외부 경계 (Edge) | 내부 서비스 간 (East-West) |
| 제어 대상 | 외부 -> 내부 트래픽 | 서비스 간 트래픽 |
| 사이드카 | 불필요 | Envoy 사이드카 필요 |
| 복잡도 | 중간 | 높음 |
| 주요 기능 | 외부 인증, 라우팅 | 내부 mTLS, 트레이싱 |

- **📢 섹션 요약 비유**: API 게이트웨이는 나라의 국경 검문소(외부->내부), 서비스 메시는 나라 안에서 도시 간 이동을 관리하는 고속도로 시스템이다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://USER-SERVICE
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
        - id: order-service
          uri: lb://ORDER-SERVICE
          predicates:
            - Path=/api/orders/**
```

게이트웨이 자체가 단일 장애점이 되지 않도록:

1. **수평 확장 (Horizontal Scaling)**: 게이트웨이 인스턴스 다중화
2. <strong>Health Check (상태 확인)</strong>: 주기적 서비스 상태 모니터링
3. <strong>Circuit Breaker (서킷 브레이커)</strong>: 장애 서비스 자동 격리
4. <strong>Fallback</strong>: 서비스 불가 시 기본 응답 반환

"MSA 도입 시 API 게이트웨이가 왜 필요한가?" — 답은 <strong>캡슐화 + 횡단 관심사 중앙화</strong>다. 클라이언트-서비스 결합도를 낮추고, 인증·로깅을 서비스 코드와 완전히 분리한다.

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 게이트웨이는 건물 로비의 방문객 등록 시스템이다. 누가 들어오는지 기록하고(로깅), 허가받은 사람만 통과(인증)하며, 특정 층(서비스)으로 안내(라우팅)한다.

---

## Ⅴ. 기대효과 및 결론
API 게이트웨이 도입 효과:

- <strong>결합도 감소</strong>: 클라이언트가 내부 서비스 구조 변경에 영향받지 않음
- **보안 강화**: 외부에 노출되는 진입점을 하나로 제한
- **운영 가시성**: 게이트웨이에서 전체 트래픽 모니터링 가능
- **개발 생산성**: 각 서비스에서 인증·로깅 코드 제거

MSA 전환에서 API 게이트웨이는 선택이 아닌 필수 인프라가 됐다. BFF (Backend For Frontend) 패턴과 결합하면 모바일·웹·파트너 API를 각각 최적화할 수 있어 클라이언트 경험도 향상된다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: API 게이트웨이가 없는 MSA는 입구 없는 대형 쇼핑몰이다. 각 매장에 직접 들어가야 하니 안전도 없고, 안내도 없고, 혼란만 가득하다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | MSA (Microservices Architecture) | 게이트웨이가 필요한 분산 아키텍처 |
| 하위 개념 | BFF (Backend For Frontend) | 클라이언트별 최적화 게이트웨이 변형 |
| 하위 개념 | Rate Limiting (속도 제한) | 게이트웨이 핵심 기능 |
| 연관 개념 | Service Mesh (Istio) | 내부 서비스 간 트래픽 관리 |
| 연관 개념 | Circuit Breaker (서킷 브레이커) | 장애 격리 패턴 |
| 연관 개념 | Load Balancer (로드 밸런서) | 요청 분산 처리 인프라 |

### 📈 관련 키워드 및 발전 흐름도
edge routing -> 게이트웨이 MSA 진입점 패턴 -> service mesh·BFF

### 👶 어린이를 위한 3줄 비유 설명
1. 놀이공원 입구(API 게이트웨이)에서 표를 확인하고(인증), 어떤 놀이기구(서비스)로 갈지 안내해 줘.
2. 입구가 하나라서, 어떤 놀이기구가 어디 있는지 손님은 몰라도 돼—입구가 다 알아서 안내해!
3. 놀이기구 하나가 고장 나도(서비스 장애) 입구에서 미리 알고 다른 데로 안내(Circuit Breaker)해 줄 수 있어.
