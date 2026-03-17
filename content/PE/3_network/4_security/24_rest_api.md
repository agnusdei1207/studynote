+++
title = "24. REST API (Representational State Transfer)"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["REST", "API", "HTTP", "Resource", "Stateless", "HATEOAS"]
draft = false
+++

# REST API (Representational State Transfer)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: REST는 **"분산 **시스템의 **아키텍처 **제약 **조건"**으로, **Resource**(URI), **Representation**(JSON/XML), **HTTP Method**(GET, POST, PUT, DELETE), **Stateless**(무상태), **Uniform Interface**(균일 인터페이스)로 **구성**된다.
> 2. **RESTful**: **HTTP Method**를 **CRUD**(Create, Read, Update, Delete)로 **매핑**하고 **Status Code**(2xx, 3xx, 4xx, 5xx)로 **결과**를 **표현**하며 **HATEOAS**(Hypermedia as the Engine of Application State)로 **링크** 기반 **탐색**을 **지원**한다.
> 3. **융합**: **OpenAPI**(Swagger), **GraphQL**(Data Query), **gRPC**(RPC)와 **비교**되며 **Stateless**로 **수평 **확장**이 **용이**하고 **Cache**(HTTP Cache)로 **성능**을 **최적화**할 **수 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
REST는 **"웹 기반 아키텍처 스타일"**이다.

**REST 6가지 제약**:
1. **Client-Server**: 관심사 분리
2. **Stateless**: 무상태
3. **Cacheable**: 캐시 가능
4. **Uniform Interface**: 균일 인터페이스
5. **Layered System**: 계층 구조
6. **Code on Demand**: 옵션

### 💡 비유
REST는 **"메뉴판****과 같다.
- **메뉴**: Resource
- **주문**: HTTP Method
- **주방**: Server

---

## Ⅱ. 아키텍처 및 핵심 원리

### REST 리소스 설계

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         REST Resource Design                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Resource (URI)                     HTTP Method        CRUD                           │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  /users                    GET                   Read All                           │  │  │
    │  │  /users/{id}               GET                   Read One                           │  │  │
    │  │  /users                    POST                  Create                            │  │  │
    │  │  /users/{id}               PUT                   Update (Replace)                   │  │  │
    │  │  /users/{id}               PATCH                 Update (Partial)                   │  │  │
    │  │  /users/{id}               DELETE                Delete                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### HTTP Status Code

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         HTTP Status Codes                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  2xx (Success)                                                                          │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  200 OK           요청 성공                                                         │  │  │
    │  │  201 Created      리소스 생성 성공                                                    │  │  │
    │  │  204 No Content   성공 but 반환 내용 없음                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  3xx (Redirection)                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  301 Moved Permanently  영구 이동                                                   │  │  │
    │  │  304 Not Modified       캐시 사용                                                     │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  4xx (Client Error)                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  400 Bad Request       잘못된 요청                                                  │  │  │
    │  │  401 Unauthorized      인증 실패                                                     │  │  │
    │  │  403 Forbidden         권한 없음                                                     │  │  │
    │  │  404 Not Found         리소스 없음                                                   │  │  │
    │  │  409 Conflict          충돌                                                         │  │  │
    │  │  422 Unprocessable     잘못된 데이터                                                 │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                                                                         │  │
    │  5xx (Server Error)                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  500 Internal Server   서버 오류                                                     │  │  │
    │  │  503 Unavailable        서비스 불가                                                   │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### API 스타일 비교

| 구분 | REST | GraphQL | gRPC |
|------|------|---------|------|
| **Protocol** | HTTP | HTTP | HTTP/2 |
| **Data** | JSON | JSON | Protobuf |
| **형식** | Resource | Query | Interface |
| **실시간** | Polling | Subscription | Stream |

### Richardson Maturity Model

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         REST Maturity Model                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Level 0: Swamp of POX
    • 단일 URI (POST only)
    • HTTP Method 무시

    Level 1: Resources
    • URI로 Resource 식별
    • GET /users, POST /users

    Level 2: HTTP Verbs
    • HTTP Method로 CRUD 매핑
    • GET, POST, PUT, DELETE

    Level 3: Hypermedia (HATEOAS)
    • 링크로 리소스 연결
    {
        "id": 1,
        "name": "User",
        "_links": {
            "self": "/users/1",
            "orders": "/users/1/orders"
        }
    }
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: OpenAPI 설계
**상황**: API 문서화
**판단**:

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewUser'
      responses:
        '201':
          description: Created
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
```

---

## Ⅴ. 기대효과 및 결론

### REST 기대 효과

| 효과 | RPC | REST |
|------|-----|------|
| **확장성** | 제한적 | 높음 |
| **캐싱** | 어려움 | 쉬움 |
| **학습 곡선** | 낮음 | 중간 |

### 미래 전망

1. **GraphQL**: Flexible Query
2. **gRPC**: High Performance
3. **Event-Driven**: Async

### ※ 참고 표준/가이드
- **Fielding**: REST dissertation
- **OpenAPI**: spec.openapis.org

---

## 📌 관련 개념 맵

- [HTTP](./4_http/1_http_overview.md) - 기초
- [HTTPS](./4_security/23_https.md) - 보안
- [WebSocket](./4_http/2_websocket.md) - 실시간
