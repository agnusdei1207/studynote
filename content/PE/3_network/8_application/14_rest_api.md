+++
title = "14. RESTful API (Representational State Transfer)"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["REST", "RESTful-API", "Resource-Based", "Stateless", "HATEOAS"]
draft = false
+++

# RESTful API (Representational State Transfer)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: REST는 **"자원(Resource) 중심의 **아키텍처 스타일"**로, **URI**로 **자원**을 식별하고 **HTTP Method**(GET, POST, PUT, DELETE)로 **행위**를 표현하며 **Stateless**(무상태) **통신**으로 **확장성**을 높인다.
> 2. **가치**: **단순함**(HTTP 기반), **확장성**(Stateless), **캐시 가능**(Cacheable), **계층 구조**(Layered System)로 **웹 서비스**의 **표준 아키텍처**가 되었고 **GraphQL**, **gRPC**와 경쟁한다.
> 3. **융합**: **JSON**(JavaScript Object Notation), **XML**로 **데이터 교환**하고 **OpenAPI**(Swagger), **API Gateway**로 **관리**하며 **HATEOAS**(Hypermedia as the Engine of Application State)로 **자기 서술적** API를 구현한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
REST는 **"분산 하이퍼미디어 시스템을 위한 아키텍처 스타일"**이다.

**REST의 핵심 원칙**:
- **Resource**: URI로 식별
- **Representation**: JSON/XML 등으로 표현
- **Stateless**: 클라이언트 상태 저장 안 함
- **Uniform Interface**: 일관된 인터페이스

### 💡 비유
REST는 **"메뉴판 주문 시스템"**과 같다.
- **메뉴**: Resource (URI)
- **주문**: Method (GET/POST/PUT/DELETE)
- **주문서**: Representation (JSON)

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         REST의 발전                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

RPC (SOAP):
    • 프로시저 호출 중심
    • XML, 복잡함
         ↓
REST (Roy Fielding, 2000):
    • Resource 중심
    • 단순함, HTTP 활용
         ↓
RESTful API:
    • JSON 표준
    • OpenAPI/Swagger
         ↓
현대:
    • GraphQL, gRPC 경쟁
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### REST 6가지 제약 조건

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         REST 6가지 제약 조건                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Client-Server

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 관심사 분리                                                                          │
    │  │  • Client: UI                                                                        │
    │  │  │  • Server: Data/Business Logic                                                    │
    │  │  │  → 독립적 개발/확장 가능                                                           │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Stateless

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 서버가 클라이언트 상태 저장 안 함                                                       │
    │  │  • 모든 요청에 필요한 정보 포함                                                         │
    │  │  → 확장성 높음 (로드 밸런싱 용이)                                                      │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  # Bad (Stateful)                                                                  │  │
    │  │  POST /login ──> "session_id=abc123"                                                │  │
    │  │  GET /profile (session_id: abc123) ──> User Profile                                │  │
    │  │                                                                                     │  │
    │  │  # Good (Stateless)                                                                │  │
    │  │  GET /profile ──> Authorization: Bearer abc123                                       │  │
    │  │  ──> User Profile                                                                  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Cacheable

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 응답을 캐시 가능으로 표시                                                             │
    │  │  • ETag, Last-Modified, Cache-Control                                                │
    │  │  → 네트워크 사용 감소                                                                 │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    4. Uniform Interface

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 일관된 인터페이스                                                                     │
    │  │  • Resource identification (URI)                                                     │
    │  │  │  • Representation manipulation (JSON/XML)                                         │
    │  │  │  • Self-descriptive messages (HTTP verbs/status)                                   │
    │  │  │  • HATEOAS (Hypermedia as the Engine of Application State)                         │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    5. Layered System

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 계층 구조                                                                              │
    │  │  • Client → API Gateway → Service → Database                                        │
    │  │  │  → 각 계층 독립적 수정 가능                                                         │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    6. Code on Demand (Optional)

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 서버가 코드 전송 (JavaScript)                                                          │
    │  │  → 선택적 제약 조건                                                                   │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### RESTful API 설계

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RESTful API 설계 예시                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Resource 설계]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • URI는 명사(자원) 중심                                                                   │
    │  │  • 동사(Method)로 행위 표현                                                            │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Resource            URI                    Method                                │  │
    │  │  ─────────────────────────────────────────────────────────────────────────────      │  │
    │  │  Users 목록          /api/users             GET                                   │  │
    │  │  User 생성           /api/users             POST                                  │  │
    │  │  User 조회           /api/users/{id}        GET                                   │  │
    │  │  User 전체 수정      /api/users/{id}        PUT                                   │  │
    │  │  User 부분 수정      /api/users/{id}        PATCH                                 │  │
    │  │  User 삭제           /api/users/{id}        DELETE                                │  │
    │  │                                                                                     │  │
    │  │  User의 주문 목록     /api/users/{id}/orders GET                                   │  │
    │  │  Order 생성           /api/users/{id}/orders POST                                  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [올바른 URI 설계]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Bad URI                      Good URI                                                │
    │  ────────────────────────────────────────────────────────────────────────────────────  │
    │  /getUsers              ──>    GET    /api/users                                      │
    │  /createUser            ──>    POST   /api/users                                      │
    │  /updateUser            ──>    PUT    /api/users/{id}                                 │
    │  /deleteUser            ──>    DELETE /api/users/{id}                                 │
    │  /user                  ──>    /api/users/{id}      (singular → plural)                │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Request/Response 예시]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # Request: User 생성                                                                  │
    │  POST /api/users HTTP/1.1                                                              │
    │  Host: api.example.com                                                                 │
    │  Content-Type: application/json                                                        │
    │                                                                                         │
    │  {                                                                                       │
    │    "name": "Hong Gil-dong",                                                             │
    │    "email": "hong@example.com",                                                         │
    │    "age": 30                                                                            │
    │  }                                                                                       │
    │                                                                                         │
    │  # Response: 201 Created                                                                │
    │  HTTP/1.1 201 Created                                                                   │
    │  Location: /api/users/123                                                               │
    │  Content-Type: application/json                                                        │
    │                                                                                         │
    │  {                                                                                       │
    │    "id": 123,                                                                           │
    │    "name": "Hong Gil-dong",                                                             │
    │    "email": "hong@example.com",                                                         │
    │    "age": 30,                                                                           │
    │    "created_at": "2026-03-06T10:00:00Z"                                                 │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### HATEOAS

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         HATEOAS (Hypermedia as the Engine of Application State)         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 응답에 다음 가능한 동작 포함                                                            │
    │  │  • API를 자기 서술적(Self-descriptive)으로 만듦                                         │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  # 일반적인 REST API                                                                  │  │
    │  │  GET /api/users/123                                                                  │  │
    │  │  {                                                                                   │  │
    │  │    "id": 123,                                                                         │  │
    │  │    "name": "Hong",                                                                    │  │
    │  │    "email": "hong@example.com"                                                       │  │
    │  │  }                                                                                    │  │
    │  │                                                                                       │  │
    │  │  # HATEOAS 적용 API                                                                   │  │
    │  │  GET /api/users/123                                                                  │  │
    │  │  {                                                                                   │  │
    │  │    "id": 123,                                                                         │  │
    │  │    "name": "Hong",                                                                    │  │
    │  │    "email": "hong@example.com",                                                       │  │
    │  │    "_links": {                                                                        │  │
    │  │      "self": { "href": "/api/users/123" },                                           │  │
    │  │      "update": { "href": "/api/users/123" },                                         │  │
    │  │      "delete": { "href": "/api/users/123" },                                         │  │
    │  │      "orders": { "href": "/api/users/123/orders" }                                   │  │
    │  │    }                                                                                  │  │
    │  │  }                                                                                    │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### REST vs RPC vs GraphQL

| 구분 | REST | RPC (gRPC) | GraphQL |
|------|------|-----------|---------|
| **중심** | Resource | Procedure | Query |
| **Protocol** | HTTP | HTTP/2 | HTTP |
| **Payload** | JSON | Protobuf | JSON |
| **Overfetching** | O | X | X |

### REST maturity model (Richardson)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Richardson Maturity Model                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Level 0: Swamp of POX
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 단일 URI (POST)                                                                      │
    │  • 모든 요청을 하나로                                                                    │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Level 1: Resources
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 각 Resource별 URI                                                                     │
    │  • HTTP Method 구분 없음                                                                 │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Level 2: HTTP Verbs
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • HTTP Method (GET, POST, PUT, DELETE) 사용                                            │
    │  • Status Code 활용                                                                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Level 3: Hypermedia (HATEOAS)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 응답에 다음 동작 포함                                                                 │
    │  • 완전한 REST                                                                           │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: RESTful API 설계
**상황**: 블로그 API
**판단**:

```yaml
# OpenAPI 3.0 예시
openapi: 3.0.0
info:
  title: Blog API
  version: 1.0.0

paths:
  /api/posts:
    get:
      summary: Get all posts
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: List of posts
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Post'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: Create post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostCreate'
      responses:
        '201':
          description: Post created
          headers:
            Location:
              schema:
                type: string
                example: /api/posts/123

  /api/posts/{id}:
    get:
      summary: Get post by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Post details
        '404':
          description: Post not found

    put:
      summary: Update entire post
    patch:
      summary: Partial update
    delete:
      summary: Delete post
      responses:
        '204':
          description: No content

components:
  schemas:
    Post:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        content:
          type: string
        created_at:
          type: string
          format: date-time
```

---

## Ⅴ. 기대효과 및 결론

### RESTful API 기대 효과

| 효과 | REST | SOAP/RPC |
|------|------|----------|
| **단순함** | O (HTTP) | X (WS-*) |
| **확장성** | O (Stateless) | △ |
| **캐시** | O | △ |
| **표준화** | O | O |

### 미래 전망

1. **HTTP/3**: QUIC 기반
2. **GraphQL**: Query 유연성
3. **gRPC**: 고성능 RPC

### ※ 참고 표준/가이드
- **RFC 7231**: HTTP/1.1
- **OpenAPI**: 3.0 Specification
- **Fielding**: REST Dissertation

---

## 📌 관련 개념 맵

- [HTTP](./12_http.md) - 기반 프로토콜
- [HTTPS](./13_https.md) - 보안
- [API Gateway](../9_security/17_api_gateway.md) - 관리
- [GraphQL](./16_graphql.md) - 대안
