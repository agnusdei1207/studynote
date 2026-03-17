+++
title = "17. 통합 테스트 (Integration Testing)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["Integration-Testing", "System-Testing", "Contract-Testing", "API-Testing", "End-to-End"]
draft = false
+++

# 통합 테스트 (Integration Testing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 통합 테스트는 **"여러 모듈/컴포넌트가 **함께 동작**하는지를 **검증하는 테스트"**로, **Unit Test**가 **격리된 환경**에서 **단일 모듈**을 검증하는 반면, **Integration Test**는 **실제 환경** 또는 **테스트 환경**에서 **모듈 간 인터페이스**와 **데이터 흐름**을 검증한다.
> 2. **가치**: **모듈 간 인터페이스 오류**를 **조기 발견**하고 **시스템 통합**의 **정확성**을 확인하며 **Database**, **External API**, **Message Queue** 같은 **외부 의존성**과의 **상호작용**을 검증하고 **E2E 테스트**와 **중계 역할**을 한다.
> 3. **융합**: **Test Pyramid**에서 **Unit Test(70%)**, **Integration Test(20%)**, **E2E Test(10%)**의 비율로 구성되며 **REST API** 테스트에는 **Postman**, **Newman**, **RestAssured**가 사용되고 **Contract Test**에는 **Pact**가 사용된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
통합 테스트는 **"여러 컴포넌트가 통합되어 제대로 동작하는지 확인하는 테스트"**이다.

**통합 테스트의 범위**:
- **Module 간 통합**: Service + Repository
- **API 통합**: Client + Server
- **Database 통합**: Application + DB
- **External 통합**: Third-party API

### 💡 비유
통합 테스트는 **"부품 조립 테스트"**와 같다.
- **부품**: 단위 테스트 완료 모듈
- **조립**: 통합 테스트
- **완제품**: 시스템 전체

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         통합 테스트의 필요성                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Unit Test만으로는:
    • 모듈 개별로는 잘 작동
    • 통합 시 문제 발생
         ↓
Big Bang Integration:
    • 한 번에 모두 통합
    • 문제 원인 파악 어려움
         ↓
Incremental Integration:
    • 점진적 통합
    • 문제 조기 발견
         ↓
Continuous Integration:
    • 자동화된 통합 테스트
    • 매 빌드 실행
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 통합 전략

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         통합 전략                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Big Bang Integration]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 모든 모듈을 한 번에 통합                                                               │
    │  │  • 장점: 간단함                                                                       │
    │  │  • 단점: 문제 원인 파악 어려움                                                         │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Incremental Integration]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 모듈을 하나씩 순차적으로 통합                                                           │
    │  │  • 장점: 문제 조기 발견, 원인 파악 용이                                                 │
    │  │  • 단점: 많은 테스트 Stub 필요                                                        │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Continuous Integration (CI)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 코드 변경 시마다 자동 통합 테스트                                                         │
    │  │  • 장점: 문제 즉시 발견, 빠른 피드백                                                   │
    │  │  • 단점: 인프라 필요                                                                   │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 테스트 더블 (Test Double) 활용

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         통합 테스트에서의 Test Double                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [In-Memory Database]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 실제 DB 대신 메모리 DB 사용                                                             │
    │  │  • 빠르고 격리됨                                                                       │
    │  │  • 예: H2, SQLite, HSQLDB                                                              │
    │                                                                                         │
    │  @SpringBootTest                                                                        │
    │  @AutoConfigureTestDatabase(connection = H2)                                               │
    │  class OrderServiceIntegrationTest {                                                   │
    │      @Autowired                                                                       │
    │      private OrderService orderService;                                                   │
    │                                                                                         │
    │      @Test                                                                               │
    │      void createOrder() {                                                               │
    │          // 실제 DB 대신 H2 메모리 DB 사용                                                  │
    │          Order order = orderService.create(request);                                     │
    │          assertThat(order.getId()).isNotNull();                                          │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [MockServer]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • External API 대신 Mock Server 사용                                                        │
    │  │  • WireMock, MockServer, Mountebank                                                        │
    │                                                                                         │
    │  @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)                │
    │  class ExternalApiIntegrationTest {                                                     │
    │      @LocalServerPort                                                                   │
    │      private int port;                                                                   │
    │                                                                                         │
    │      @Test                                                                               │
    │      void callExternalApi() {                                                            │
    │          // RestAssured로 Mock API 호출                                                    │
    │          given().mockMvc()                                                               │
    │            .contentType(ContentType.JSON)                                                │
    │            .body("{\"name\":\"Test\"}")                                                     │
    │            .when().post("/api/users")                                                    │
    │            .thenReturn().status(201);                                                     │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [TestContainers]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Docker 컨테이너로 실제 DB/서버 실행                                                       │
    │  │  • 격리되지만 실제 환경과 유사                                                          │
    │  │  • 예: Testcontainers, Docker Compose                                                     │
    │                                                                                         │
    │  @Testcontainers                                                                           │
    │  class PostgreSQLIntegrationTest {                                                       │
    │      @Container                                                                          │
    │      static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")       │
    │                                                                                         │
    │      @Test                                                                               │
    │      void testQuery() {                                                                  │
    │          try (Connection conn = DriverManager.getConnection(                              │
    │                  postgres.getJdbcUrl(), postgres.getUsername(),                         │
    │                  postgres.getPassword())) {                                               │
    │              // 실제 PostgreSQL 테스트                                                       │
    │              Statement stmt = conn.createStatement();                                      │
    │              ResultSet rs = stmt.executeQuery("SELECT 1");                               │
    │              assertTrue(rs.next());                                                      │
    │          }                                                                              │
    │      }                                                                                  │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Unit vs Integration vs E2E Test

| 구분 | Unit | Integration | E2E |
|------|------|-------------|-----|
| **범위** | 단일 모듈 | 여러 모듈 | 전체 시스템 |
| **속도** | 빠름 | 중간 | 느림 |
| **비용** | 낮음 | 중간 | 높음 |
| **유지보수** | 쉬움 | 어려움 | 매우 어려움 |

### 통합 테스트 종류

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         통합 테스트 유형                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Component Integration Test]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 특정 컴포넌트 간 통합 테스트                                                           │
    │  │  • 예: Controller + Service                                                            │
    │  │  • Database 제외 (Mock)                                                               │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [API Integration Test]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • API Endpoint 테스트                                                                    │
    │  │  • HTTP Request/Response 검증                                                           │
    │  │  • 예: POST /api/users                                                               │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Database Integration Test]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • Database 스키마, 제약 조건 테스트                                                     │
    │  │  • ORM 쿼리 검증                                                                       │
    │  │  • Transaction 테스트                                                                  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Contract Test]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 서비스 간 계약(Contract) 검증                                                          │
    │  │  • Consumer + Provider 계약                                                            │
    │  │  • 예: Pact, Spring Cloud Contract                                                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: REST API 통합 테스트
**상황**: 주문 API
**판단**:

```java
// RestAssured 예시
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderApiIntegrationTest {

    @LocalServerPort
    private int port;

    @Test
    void createOrder_Success() {
        String requestBody = """
            {
                "productId": "P001",
                "quantity": 2,
                "customerId": "C001"
            }
            """;

        given()
            .contentType(ContentType.JSON)
            .body(requestBody)
            .when()
            .post("http://localhost:" + port + "/api/orders")
            .then()
            .statusCode(HttpStatus.CREATED)
            .body("id", notNullValue())
            .body("status", equalTo("CREATED"));
    }

    @Test
    void createOrder_InvalidProduct() {
        // 제품 없음
        given()
            .contentType(ContentType.JSON)
            .body("{\"productId\":\"INVALID\",\"quantity\":1}")
            .when()
            .post("http://localhost:" + port + "/api/orders")
            .then()
            .statusCode(HttpStatus.BAD_REQUEST);
    }
}
```

---

## Ⅴ. 기대효과 및 결론

### 통합 테스트 기대 효과

| 효과 | 통합 테스트 없을 시 | 통합 테스트 있을 시 |
|------|-----------------|-------------------|
| **인터페이스 오류** | 운영 중 발견 | 조기 발견 |
| **시스템 신뢰** | 낮음 | 높음 |
| **수정 비용** | 높음 | 낮음 |
| **테스트 시간** | - | 중간 |

### 미래 전망

1. **Service Virtualization**: 완전 환경 모의
2. **Chaos Engineering**: 장애 주입 테스트
3. **AI Test Generation**: 자동 테스트 생성

### ※ 참고 표준/가이드
- **ISTQB**: Integration Testing
- **Martin Fowler**: Test Pyramid
- **Google**: Testing Blog

---

## 📌 관련 개념 맵

- [단위 테스트](./16_unit_testing.md) - 기초
- [E2E 테스트](./18_e2e_testing.md) - 최종 테스트
- [Contract Testing](./19_contract_testing.md) - 계약 테스트
- [CI/CD](../6_devops/21_ci_cd.md) - 자동화
