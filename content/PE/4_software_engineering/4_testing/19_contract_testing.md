+++
title = "19. 계약 테스트 (Contract Testing)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Contract-Testing", "Pact", "Pact-Flow", "Consumer-Driven", "API-Contract"]
draft = false
+++

# 계약 테스트 (Contract Testing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 계약 테스트는 **"서비스 간 **인터페이스**(API)의 **계약(Contract)**을 **정의하고 **검증하는 테스트"**로, **Consumer**(호출자)가 **계약을 정의**하고 **Provider**(제공자)가 **계약을 준수**하는지 확인하여 **통합 문제**를 **조기 발견**한다.
> 2. **가치**: **Microservice Architecture**에서 **서비스 간 통신**의 **안정성**을 보장하고 **변경 파급효과**(Breaking Change)를 **조기 감지**하며 **E2E 테스트**보다 **빠르고 **안정적**이며 **Mock Server** 의존성을 **제거**한다.
> 3. **융합**: **Pact**(Ruby/Java/JS/Go), **Pact Flow**, **Spring Cloud Contract**가 **대표 도구**이며 **Consumer-Driven Contract Testing(CDC)** 패턴으로 **Consumer**가 **우선** 계약을 **정의**하고 **CI/CD Pipeline**에서 **자동 검증**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
계약 테스트는 **"서비스 간 인터페이스 규약을 검증하는 테스트"**이다.

**계약의 구성 요소**:
- **Request**: HTTP Method, Path, Headers, Body
- **Response**: Status Code, Headers, Body Schema

### 💡 비유
계약 테스트는 **"물품 계약서"**와 같다.
- **계약서**: API 명세
- **검수**: 실제 제공물 확인
- **불일치**: 계약 위반

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         계약 테스트의 필요성                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Microservices:
    • 수십~수백 개 서비스
    • 복잡한 통신 관계
         ↓
Integration Issues:
    • Provider 변경 → Consumer 장애
    • E2E 테스트 느리고 불안정
         ↓
Contract Testing:
    • 인터페이스 계약 검증
    • 조기 발견, 빠른 피드백
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### Consumer-Driven Contract Testing (CDC)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CDC 테스트 흐름                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [1. Consumer가 계약 정의]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Consumer Service                                                                     │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  // Consumer Test (Java + Pact)                                                    │  │
    │  │  @Pact(provider = "UserService", consumer = "OrderService")                        │  │
    │  │  public PactFragment userPact(PactDslWithProvider builder) {                       │  │
    │  │      return builder                                                                 │  │
    │  │          .given("user exists")                                                      │  │
    │  │          .uponReceiving("a request for user profile")                               │  │
    │  │          .path("/api/users/123")                                                    │  │
    │  │          .method("GET")                                                             │  │
    │  │          .willRespondWith()                                                         │  │
    │  │          .status(200)                                                               │  │
    │  │          .body("{\\"id\\":123,\\"name\\":\\"Hong\\",\\"email\\":\\"hong@example.com\\"}") │  │
    │  │          .toFragment();                                                              │  │
    │  │  }                                                                                  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [2. 계약 파일 생성 (Pact JSON)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  {                                                                                       │
    │    "consumer": {                                                                         │
    │      "name": "OrderService"                                                             │
    │    },                                                                                    │
    │    "provider": {                                                                         │
    │      "name": "UserService"                                                              │
    │    },                                                                                    │
    │    "interactions": [                                                                     │
    │      {                                                                                   │
    │        "description": "a request for user profile",                                      │
    │        "providerState": "user exists",                                                   │
    │        "request": {                                                                      │
    │          "method": "GET",                                                                │
    │          "path": "/api/users/123"                                                        │
    │        },                                                                                 │
    │        "response": {                                                                     │
    │          "status": 200,                                                                  │
    │          "headers": {                                                                    │
    │            "Content-Type": "application/json"                                             │
    │          },                                                                              │
    │          "body": {                                                                       │
    │            "id": 123,                                                                    │
    │            "name": "Hong",                                                               │
    │            "email": "hong@example.com"                                                   │
    │          }                                                                               │
    │        }                                                                                 │
    │      }                                                                                   │
    │    ]                                                                                     │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [3. Provider가 계약 검증]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Provider Service                                                                       │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  // Provider Test (Pact Verification)                                               │  │
    │  │  @Test                                                                               │  │
    │  │  @PactVerification(provider = "UserService", fragment = "userPact")                 │  │
    │  │  public void testUserPact(MockServer mockServer) {                                  │  │
    │  │      // Pact이 제공한 Mock Server로 실제 구현 검증                                    │  │
    │  │      mockMvc.perform(get("/api/users/123"))                                          │  │
    │  │          .andExpect(status().isOk())                                                 │  │
    │  │          .andExpect(jsonPath("$.id").value(123))                                      │  │
    │  │          .andExpect(jsonPath("$.name").value("Hong"))                                 │  │
    │  │          .andExpect(jsonPath("$.email").value("hong@example.com"));                   │  │
    │  │  }                                                                                  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Pact Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Pact CI/CD Workflow                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Consumer CI Pipeline                   Provider CI Pipeline                     │  │
    │  │  ┌────────────────────────────────────┐  ┌────────────────────────────────────┐  │  │
    │  │  │ 1. Consumer Test                   │  │ 3. Pact Broker에서 계약 가져옴      │  │  │
    │  │  │    (Contract 생성)                 │  │                                    │  │  │
    │  │  │                                    │  │ 4. Provider Test                  │  │  │
    │  │  │                                    │  │    (계약 준수 검증)                │  │  │
    │  │  │ 2. Pact Publish                    │  │                                    │  │  │
    │  │  │    ──> Pact Broker ───>            │  │ 5. Contract 실패 시               │  │  │
    │  │  │                                    │  │    Consumer/Provider 알림          │  │  │
    │  │  └────────────────────────────────────┘  └────────────────────────────────────┘  │  │
    │  │                                                                                  │  │
    │  │  [Pact Broker]                                                                   │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  • 계약 저장소                                                                    │  │  │
    │  │  │  • 버전 관리                                                                    │  │  │
    │  │  │  • Web UI로 계약 확인                                                            │  │  │
    │  │  │  • Pact Flow (Pact Broker + Webhook)                                          │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Pact Flow - 자동 검증]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Consumer가 계약 변경 → Pact Broker에 푸시                                          │
    │  2. Pact Broker가 Provider CI 트리거                                                    │
    │  3. Provider가 계약 검증                                                                  │
    │  4. 결과를 Pact Broker에 통보                                                           │
    │  5. 계약 위반 시 Consumer에게 알림                                                        │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 테스트 레벨 비교

| 구분 | Unit | Contract | Integration | E2E |
|------|------|----------|-------------|-----|
| **범위** | 단일 함수 | 인터페이스 | 서비스 간 | 전체 시스템 |
| **속도** | ms | 초 | 초~분 | 분 |
| **비용** | 낮음 | 낮음 | 중간 | 높음 |
| **Microservice** | 단일 서비스 | 서비스 간 | 실제 연동 | 전체 |

### 계약 위반 시나리오

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         계약 위반 예시                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [시나리오: 필드 누락]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Consumer가 기대하는 계약:                                                              │
    │  {                                                                                       │
    │    "id": 123,                                                                             │
    │    "name": "Hong",                                                                       │
    │    "email": "hong@example.com"                                                           │
    │  }                                                                                       │
    │                                                                                         │
    │  Provider가 실제 반환:                                                                   │
    │  {                                                                                       │
    │    "id": 123,                                                                             │
    │    "name": "Hong"                                                                        │
    │    # "email" 필드 누락!                                                                  │
    │  }                                                                                       │
    │                                                                                         │
    │  → 계약 위반 (Contract Violation)                                                        │
    │  → Provider 수정 필요                                                                    │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [시나리오: 타입 불일치]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Consumer 기대: {"age": 30} (integer)                                                   │
    │  Provider 반환: {"age": "30"} (string)                                                  │
    │  → 계약 위반                                                                             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Spring Cloud Contract
**상황**: Java Microservice
**판단**:

```groovy
// Consumer (Order Service) - 계약 정의
build.gradle:
dependencies {
    testImplementation 'org.springframework.cloud:spring-cloud-starter-contract-verifier'
}

// Contract (Groovy DSL)
org.springframework.cloud.contract.spec.Contract.make {
    description "Should return user profile"
    request {
        method GET()
        url("/api/users/123")
        headers {
            header("Content-Type", "application/json")
        }
    }
    response {
        status OK()
        body([
            id: 123,
            name: "Hong",
            email: "hong@example.com"
        ])
        headers {
            header("Content-Type", "application/json")
        }
    }
}

// Provider (User Service) - 계약 검증
@Test
void testUserContract() {
    // Contract에서 생성된 테스트 실행
    RestAssuredMockMvc.standaloneSetup(userController)
    RestAssuredMockMvc
        .given()
            .param("id", 123)
        .when()
            .get("/api/users/123")
        .then()
            .statusCode(200)
            .body("id", equalTo(123))
            .body("name", equalTo("Hong"))
            .body("email", equalTo("hong@example.com"))
}
```

---

## Ⅴ. 기대효과 및 결론

### 계약 테스트 기대 효과

| 효과 | 계약 테스트 없을 시 | 계약 테스트 있을 시 |
|------|----------------|-----------------|
| **통합 장애** | 운영 중 발견 | 조기 발견 |
| **변경 영향** | 알 수 없음 | 명확 |
| **E2E 의존** | 높음 | 낮음 |

### 계약 테스트 모범 사례

1. **Consumer 우선**: Consumer가 계약 주도
2. **버전 관리**: 계약 변경 시 버전 명시
3. **Pact Broker**: 중앙 저장소 활용
4. **자동화**: CI/CD 통합
5. **협업**: Consumer/Provider 간 소통

### 미래 전망

1. **Async Contract**: Kafka/Event 기반
2. **GraphQL Contract**: Schema 검증
3. **AI Contract**: 자동 계약 생성

### ※ 참고 표준/가이드
- **Pact**: pact.io
- **Spring Cloud Contract**: docs.spring.io
- **Pact Flow**: pactflow.io

---

## 📌 관련 개념 맵

- [통합 테스트](./17_integration_testing.md) - 서비스 간 테스트
- [E2E 테스트](./18_e2e_testing.md) - 전체 시스템
- [CI/CD](../6_devops/21_ci_cd.md) - 자동화
- [Microservice](../3_architecture/20_microservice.md) - 아키텍처
