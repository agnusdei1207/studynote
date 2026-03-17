+++
title = "12. HTTP (Hypertext Transfer Protocol)"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["HTTP", "HTTPS", "REST", "HTTP-Methods", "Status-Codes", "Headers"]
draft = false
+++

# HTTP (Hypertext Transfer Protocol)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: HTTP는 **"웹에서 데이터를 **교환하기 위한 **Request-Response 프로토콜"**로, **Client**가 **Request**를 보내면 **Server**가 **Response**를 반환하는 **Stateless(무상태)** 프로토콜이며 **TCP 80포트**, **HTTPS는 **TCP 443포트**를 사용한다.
> 2. **가치**: **단순함(Simplicity)**과 **확장성(Extensibility)**로 **웹의 기반**이 되며 **RESTful API**의 **표준 프로토콜**로 사용되고 **Cache**, **Proxy**, **CDN** 같은 **중계 장비**와 **협력**할 수 있다.
> 3. **융합**: **HTTP/1.1**의 **Keep-Alive**, **HTTP/2**의 **Multiplexing**, **HTTP/3(QUIC)**의 **UDP 기반**으로 진화하며 **WebSocket**, **Server-Sent Events(SSE)** 같은 **실시간 통신**도 지원한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
HTTP는 **"월드 와이드 웹(WWW)에서 하이퍼미디어 문서를 전송하는 프로토콜"**이다.

**HTTP의 특징**:
- **Stateless**: 이전 요청无关
- **Request-Response**: 클라이언트 요청, 서버 응답
- **Text-based**: 사람이 읽기 쉬움

### 💡 비유
HTTP는 **"주문-배달 시스템"**과 같다.
- **Request**: 주문서
- **Response**: 배달물
- **Stateless**: 매번 새 주문

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         HTTP의 발전                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

HTTP/0.9 (1991):
    • GET만 존재
    • HTML만 전송
         ↓
HTTP/1.0 (1996):
    • HEAD, POST 추가
    • Header 도입
    • Status Code
         ↓
HTTP/1.1 (1997):
    • Keep-Alive (연결 유지)
    • Host Header 필수
    • Pipelining
         ↓
HTTP/2 (2015):
    • Binary Protocol
    • Multiplexing (Stream)
    • Header Compression (HPACK)
         ↓
HTTP/3 (2022):
    • QUIC over UDP
    • Connection Migration
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### HTTP Request 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         HTTP Request 메시지                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  GET /index.html HTTP/1.1                                                               │
    │  Host: www.example.com                                                                 │
    │  User-Agent: Mozilla/5.0                                                                │
    │  Accept: text/html,application/xhtml+xml                                                │
    │  Accept-Language: ko-KR,ko;q=0.9,en;q=0.8                                                │
    │  Connection: keep-alive                                                                 │
    │                                                                                         │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Request Line                                                                       │  │
    │  │  ┌──────────┬────────────────┬─────────────┬─────────────┐                        │  │
    │  │  │ Method   │  URI            │  Version     │  CRLF        │                        │  │
    │  │  └──────────┴────────────────┴─────────────┴─────────────┘                        │  │
    │  │                                                                                      │  │
    │  │  Request Headers                                                                     │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Header-Name: Value                                                              │  │
    │  │  │  Header-Name: Value                                                              │  │
    │  │  │  ...                                                                             │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │
    │  │                                                                                      │  │
    │  │  Message Body (Optional)                                                            │  │
    │  │  POST/PUT/PATCH 시 데이터                                                            │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### HTTP Methods

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         HTTP Method (CRUD)                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Method  │  CRUD  │  Idempotent  │  Safe  │  Description                             │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  GET     │  Read   │  O           │  O     │  리소스 조회                              │
    │  POST    │  Create │  X           │  X     │  리소스 생성, 데이터 전송               │
    │  PUT     │  Update │  O           │  X     │  리소스 전체 교체                        │
    │  PATCH   │  Update │  X*          │  X     │  리소스 부분 수정                        │
    │  DELETE  │  Delete │  O           │  X     │  리소스 삭제                              │
    │  HEAD    │  -      │  O           │  O     │  Header만 조회 (본문 없음)              │
    │  OPTIONS │  -      │  O           │  O     │  지원하는 Method 확인                     │
    │  TRACE   │  -      │  O           │  O     │  경로 추적 (디버깅)                       │
    │  CONNECT │  -      │  X           │  X     │  프록시 연결 (HTTPS Tunnel)              │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    * PATCH는 Idempotent 아닐 수 있음 (구현에 따라)

    [Method 사용 예시]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # 조회                                                                                   │
    │  GET /api/users/1 HTTP/1.1                                                              │
    │                                                                                         │
    │  # 생성                                                                                   │
    │  POST /api/users HTTP/1.1                                                                │
    │  Content-Type: application/json                                                        │
    │  {"name": "Hong", "email": "hong@example.com"}                                            │
    │                                                                                         │
    │  # 전체 수정                                                                              │
    │  PUT /api/users/1 HTTP/1.1                                                               │
    │  Content-Type: application/json                                                        │
    │  {"id": 1, "name": "Kim", "email": "kim@example.com"}                                    │
    │                                                                                         │
    │  # 부분 수정                                                                              │
    │  PATCH /api/users/1 HTTP/1.1                                                             │
    │  Content-Type: application/json                                                        │
    │  {"email": "newemail@example.com"}                                                       │
    │                                                                                         │
    │  # 삭제                                                                                   │
    │  DELETE /api/users/1 HTTP/1.1                                                            │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### HTTP Status Codes

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         HTTP Status Code                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Code  │  Meaning              │  Description                                         │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  1xx   │  Informational       │  요청 수신, 처리 중 (100 Continue)                     │
    │  2xx   │  Success              │  요청 성공                                          │
    │  3xx   │  Redirection          │  추가 조치 필요 (301, 302, 304)                     │
    │  4xx   │  Client Error         │  클라이언트 오류 (400, 401, 403, 404)               │
    │  5xx   │  Server Error         │  서버 오류 (500, 502, 503)                          │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [주요 Status Code]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  200 OK: 요청 성공                                                                        │
    │  201 Created: 리소스 생성 성공                                                            │
    │  204 No Content: 성공 but 반환 내용 없음 (DELETE)                                         │
    │                                                                                         │
    │  301 Moved Permanently: 영구 이동                                                       │
    │  302 Found: 일시 이동                                                                  │
    │  304 Not Modified: ETag/Last-Modified 기반 캐시                                         │
    │                                                                                         │
    │  400 Bad Request: 잘못된 요청                                                           │
    │  401 Unauthorized: 인증 필요                                                             │
    │  403 Forbidden: 권한 부족                                                               │
    │  404 Not Found: 리소스 없음                                                              │
    │  409 Conflict: 충돌 (중복 생성 등)                                                        │
    │                                                                                         │
    │  500 Internal Server Error: 서버 내부 오류                                               │
    │  502 Bad Gateway: 상류 서버 오류                                                         │
    │  503 Service Unavailable: 서비스 과부하                                                   │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### HTTP Headers

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         주요 HTTP Headers                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Header                │  Type       │  Description                                     │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  Host                  │  Request    │  도메인 이름 (HTTP/1.1 필수)                      │
    │  User-Agent            │  Request    │  클라이언트 정보                                 │
    │  Accept               │  Request    │  콘텐츠 타입 (text/html, application/json)          │
    │  Content-Type          │  Both       │  바디 타입 (application/json)                    │
    │  Content-Length        │  Both       │  바디 길이                                       │
    │  Authorization        │  Request    │  인증 토큰 (Bearer xxx)                          │
    │  Location             │  Response   │  이동 URL (3xx)                                  │
    │  Set-Cookie           │  Response   │  쿠키 설정                                       │
    │  Cache-Control        │  Both       │  캐시 정책 (no-cache, max-age)                   │
    │  ETag                 │  Response   │  리소스 버전 (캐시용)                           │
    │  Last-Modified        │  Response   │  최종 수정 일시                                  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### HTTP/1.1 vs HTTP/2 vs HTTP/3

| 구분 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|---------|--------|--------|
| **전송** | Text | Binary | Binary |
| **Multiplexing** | X | O | O |
| **Header Comp** | X | HPACK | QPACK |
| **전송 계층** | TCP | TCP | QUIC(UDP) |
| **HOL Blocking** | O | 완화 | 해결 |

### RESTful API

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         RESTful API 설계 원칙                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Resource-Based URI                                                                  │
    │  • /api/users (사용자 목록)                                                             │
    │  • /api/users/1 (ID=1 사용자)                                                           │
    │                                                                                         │
    │  2. HTTP Method 매핑                                                                    │
    │  • GET: 조회                                                                            │
    │  • POST: 생성                                                                           │
    │  • PUT: 전체 수정                                                                       │
    │  • PATCH: 부분 수정                                                                     │
    │  • DELETE: 삭제                                                                         │
    │                                                                                         │
    │  3. Status Code                                                                         │
    │  • 2xx: 성공                                                                            │
    │  │  4xx: 클라이언트 오류                                                                  │
    │  │  5xx: 서버 오류                                                                      │
    │                                                                                         │
    │  4. Stateless                                                                          │
    │  • 각 요청에 필요한 모든 정보 포함                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: REST API 설계
**상황**: 블로그 게시글 API
**판단**:

```yaml
# URI 설계
GET    /api/posts          # 목록 조회
GET    /api/posts/123      # 게시글 조회
POST   /api/posts          # 게시글 생성
PUT    /api/posts/123      # 게시글 전체 수정
PATCH  /api/posts/123      # 게시글 부분 수정
DELETE /api/posts/123      # 게시글 삭제

# Status Code
200 OK               # 조회/수정 성공
201 Created         # 생성 성공 (Location: /api/posts/123)
204 No Content      # 삭제 성공
400 Bad Request     # 잘못된 요청
401 Unauthorized    # 인증 필요
403 Forbidden       # 권한 없음
404 Not Found       # 리소스 없음
409 Conflict        # 충돌 (이미 존재)
500 Internal Error  # 서버 오류

# Request/Response 예시
POST /api/posts HTTP/1.1
Content-Type: application/json

{
  "title": "HTTP 개요",
  "content": "...",
  "author_id": 1
}

HTTP/1.1 201 Created
Location: /api/posts/456
```

---

## Ⅴ. 기대효과 및 결론

### HTTP 기대 효과

| 효과 | HTTP 없을 시 | HTTP 있을 시 |
|------|------------|-------------|
| **상호 운용** | 불가능 | 범용 |
| **확장성** | 낮음 | 높음 |
| **단순함** | 복잡 | Text-based |
| **보안** | 없음 | HTTPS |

### 미래 전망

1. **HTTP/3**: QUIC, UDP
2. **HTTP/2 Push**: Server Push
3. **Edge Computing**: CDN 통합

### ※ 참고 표준/가이드
- **RFC 7231**: HTTP/1.1
- **RFC 7540**: HTTP/2
- **RFC 9114**: HTTP/3

---

## 📌 관련 개념 맵

- [TCP/IP](../7_protocols/11_tcp_ip.md) - 전송 계층
- [HTTPS](../8_security/13_https.md) - 보안
- [RESTful API](./14_rest_api.md) - API 설계
- [WebSocket](./15_websocket.md) - 실시간 통신
