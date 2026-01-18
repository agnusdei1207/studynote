# JSON-RPC (JavaScript Object Notation - Remote Procedure Call)

## 1. 개요 및 정의

**JSON-RPC (JavaScript Object Notation - Remote Procedure Call)**는 경량 원격 프로시저 호출(Remote Procedure Call) 프로토콜로서, JSON(JavaScript Object Notation) 형식을 사용하여 클라이언트와 서버 간에 요청(request)과 응답(response)을 교환하는 표준화된 통신 방식입니다.

JSON-RPC는 2010년 초 JSON-RPC 1.0으로 처음 공표되었으며, 이후 2013년 JSON-RPC 2.0으로 개정되어 현재까지 널리 사용되고 있습니다. 복잡한 웹 서비스 기술인 SOAP(Simple Object Access Protocol)이나 XML-RPC(XML Remote Procedure Call)에 비해 구현이 간단하고 페이로드(payload) 크기가 작아 경량성을 요구하는 웹 및 모바일 애플리케이션에서 주로 활용됩니다.

---

## 2. 등장 배경

### 2.1 웹 서비스 기술의 발전 과정

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         웹 서비스 기술 발전 히스토리                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  1998: XML-RPC 발표                                                          │
│    → XML 기반의 가장 초기 RPC 프로토콜                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  2000: SOAP 1.1 발표                                                         │
│    → 엔터프라이즈급 트랜잭션 및 보안 기능 포함                               │
│    → 구조 복잡, 페이로드 크기 증가                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  2006: JSON-RPC 1.0 발표                                                     │
│    → XML 대신 JSON 사용으로 경량화                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  2010: JSON-RPC 2.0 발표                                                     │
│    → 배치 요청(batch request), 파라미터 배열/객체 지원                        │
│    → 에러 코드 체계 정비                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  2015~: RESTful API 전성기                                                   │
│    → 자원 중심 URI 설계와 HTTP 메서드 활용                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  현재: JSON-RPC 2.0 + GraphQL + WebSocket                                    │
│    → 실시간 통신 및 다양한 RPC 방식 병행 사용                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 JSON-RPC 등장의 필요성

| 기존 기술 | 단점 | JSON-RPC의 해결책 |
|-----------|------|-------------------|
| XML-RPC | XML 파싱 오버헤드, 구조 복잡 | JSON의 가볍고 직관적인 구조 |
| SOAP | WS-* 스펙의 과도한 복잡성, 대형 페이로드 | 최소한의 스펙, 경량 페이로드 |
| RESTful API | 메서드 호출의 암묵적 표현, Over-fetching | 명시적 메서드 호출, 정확한 응답 크기 |
| gRPC | Protocol Buffers 학습 곡선, HTTP/2 의존성 | 순수 텍스트 기반, 구현 용이성 |

---

## 3. 구성 요소

JSON-RPC 프로토콜은 다음과 핵심 구성 요소로 이루어져 있습니다.

### 3.1 기본 데이터 유형

| 데이터 유형 | 설명 | 예시 |
|-------------|------|------|
| String | UTF-8 인코딩 문자열 | `"methodName"` |
| Number | 정수 또는 부동소수점 | `42`, `3.14` |
| Boolean | true 또는 false | `true` |
| Array | 순서 있는 값의 리스트 | `[1, 2, 3]` |
| Object | 키-값 쌍의 집합 | `{"id": 1}` |
| Null | null 값 | `null` |

### 3.2 요청(Request) 객체 구조

```json
{
  "jsonrpc": "2.0",
  "method": "subtract",
  "params": [42, 23],
  "id": 1
}
```

| 필드 | 필수 여부 | 타입 | 설명 |
|------|-----------|------|------|
| jsonrpc | 필수 | String | 프로토콜 버전 ("2.0") |
| method | 필수 | String | 호출할 메서드 이름 |
| params | 선택 | Array/Object | 메서드에 전달할 매개변수 |
| id | 선택* | String/Number/null | 요청 식별자 (*알림(notification) 제외) |

### 3.3 응답(Response) 객체 구조

```json
{
  "jsonrpc": "2.0",
  "result": 19,
  "id": 1
}
```

| 필드 | 필수 여부 | 타입 | 설명 |
|------|-----------|------|------|
| jsonrpc | 필수 | String | 프로토콜 버전 ("2.0") |
| result | 선택* | - | 호출 결과값 (*에러 시 존재하지 않음) |
| error | 선택* | Object | 에러 정보 (*성공 시 존재하지 않음) |
| id | 필수 | String/Number/null | 요청 시 전달된 id값 |

### 3.4 에러(Error) 객체 구조

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found",
    "data": "Available methods: subtract, add"
  },
  "id": 1
}
```

| 필드 | 필수 여부 | 타입 | 설명 |
|------|-----------|------|------|
| code | 필수 | Number | 에러 코드 (정수형) |
| message | 필수 | String | 에러 메시지 (짧고 간결한 설명) |
| data | 선택 | - | 상세 에러 정보 |

### 3.5 표준 에러 코드

| 코드 | 설명 | 의미 |
|------|------|------|
| -32700 | Parse error | JSON 파싱 실패 |
| -32600 | Invalid Request | 잘못된 JSON-RPC 요청 |
| -32601 | Method not found | 메서드를 찾을 수 없음 |
| -32602 | Invalid params | 잘못된 매개변수 |
| -32603 | Internal error | 내부 서버 오류 |
| -32000 ~ -32099 | Server error | 애플리케이션 정의 에러 |

---

## 4. 핵심 원리

### 4.1 동작 메커니즘

```
┌──────────┐                              ┌──────────┐
│  클라이언트  │                              │  서버    │
└──────────┘                              └──────────┘
     │                                          │
     │  1) JSON-RPC 요청 전송                    │
     │  ───────────────────────────────────>   │
     │  {                                      │
     │    "jsonrpc": "2.0",                     │
     │    "method": "add",                     │
     │    "params": [1, 2],                    │
     │    "id": 1                              │
     │  }                                      │
     │                                          │
     │                                          │  2) 요청 수신 및 파싱
     │                                          │  3) 메서드 매핑
     │                                          │  4) 메서드 실행
     │                                          │  5) 결과 직렬화
     │                                          │
     │  6) JSON-RPC 응답 수신                    │
     │  <───────────────────────────────────   │
     │  {                                      │
     │    "jsonrpc": "2.0",                     │
     │    "result": 3,                         │
     │    "id": 1                              │
     │  }                                      │
     │                                          │
```

### 4.2 통신 모델

#### 4.2.1 단일 요청-응답 (Single Request-Response)

가장 기본적인 모델로, 하나의 요청에 대해 하나의 응답을 반환합니다.

#### 4.2.2 알림 (Notification)

```json
{
  "jsonrpc": "2.0",
  "method": "logMessage",
  "params": ["Server started"]
}
```

- `id` 필드가 생략된 요청
- 응답을 기대하지 않음
- 이벤트 통지, 로깅 등에 사용

#### 4.2.3 배치 요청 (Batch Request)

```json
[
  {"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": "1"},
  {"jsonrpc": "2.0", "method": "subtract", "params": [5, 3], "id": "2"},
  {"jsonrpc": "2.0", "method": "multiply", "params": [4, 6], "id": "3"}
]
```

- 여러 요청을 단일 HTTP 연결로 전송
- 네트워크 레이턴시(latency) 감소
- 서버는 순서에 관계없이 병렬 처리 가능

### 4.3 전송 계층 독립성

JSON-RPC는 전송 계층(Transport Layer)에 독립적입니다.

| 전송 계층 | 특징 | 사용 사례 |
|-----------|------|-----------|
| HTTP/HTTPS | 방화벽 호환성, 널리 사용됨 | 일반 웹 애플리케이션 |
| WebSocket | 양방향 실시간 통신 | 실시간 채팅, 협업 도구 |
| TCP/IP | 직접 소켓 통신 | 고성능 내부 서비스 |
| gRPC Stream | 바이너리 기반 스트리밍 | 마이크로서비스 통신 |

---

## 5. 장단점 분석

### 5.1 장점 (Advantages)

| 장점 | 설명 | 기술사적 관점 |
|------|------|--------------|
| **경량성** | XML 대신 JSON 사용으로 페이로드 크기 감소 (30-50%) | 네트워크 대역폭 절감, 모바일 환경 유리 |
| **구현 용이성** | 간단한 스펙, 최소한의 규칙 | 개발 생산성 향상, 유지보수 용이 |
| **언어 독립성** | JSON은 거의 모든 프로그래밍 언어에서 지원 | 다중 언어 환경의 시스템 통합 |
| **명시적 메서드 호출** | 행위(verb) 중심의 직관적 API 설계 | 비즈니스 로직 명확화 |
| **배치 요청 지원** | 여러 작업을 하나의 요청으로 처리 | 네트워크 오버헤드 최소화 |
| **전송 계층 독립** | HTTP, WebSocket, TCP 등 다양한 전송 계층 사용 | 유연한 아키텍처 설계 |

### 5.2 단점 (Disadvantages)

| 단점 | 설명 | 기술사적 관점 |
|------|------|--------------|
| **표준 에러 처리 부족** | 사용자 정의 에러 코드 체계 필요 | 에러 처리 정책 표준화 필요 |
| **스키마 유효성 검증** | JSON-Schema 지원하지만 필수 아님 | 데이터 무결성 보장 추가 구현 필요 |
| **스트리밍 지원 미흡** | 기본적으로 요청-응답 패러다임 | 대용량 데이터 전송 시 제약 |
| **캐싱 메커니즘 부족** | HTTP 캐싱 활용 제한적 | 성능 최적화 추가 설계 필요 |
| **보안 스펙 미포함** | 전송 계층(TLS)에 의존 | 별도 보안 아키텍처 필요 |

---

## 6. 타 프로토콜과의 비교

### 6.1 상세 비교 표

| 비교 항목 | JSON-RPC 2.0 | RESTful API | gRPC | GraphQL |
|-----------|--------------|-------------|------|---------|
| **데이터 포맷** | JSON | JSON, XML | Protocol Buffers | JSON |
| **전송 프로토콜** | HTTP/HTTPS, WebSocket, TCP | HTTP/HTTPS | HTTP/2 | HTTP/HTTPS |
| **인터페이스 스타일** | 메서드 중심 | 자원 중심 (URI) | 메서드 중심 (IDL) | 쿼리 중심 |
| **동작 방식** | 요청-응답 | GET/POST/PUT/DELETE | 양방향 스트리밍 | 단일 쿼리 |
| **스키마** | 선택적 (JSON-Schema) | OpenAPI/Swagger | Protocol Buffers 강제 | SDL 필수 |
| **코드 생성** | 선택적 | 선택적 | 필수 (protoc) | 선택적 |
| **실시간 통신** | WebSocket 필요 | Server-Sent Events | 지원 | Subscription |
| **성능** | 중간 | 느림 (HTTP/1.1) | 빠름 (HTTP/2 + 바이너리) | 중간 |
| **페이로드 크기** | 작음 | 중간 | 매우 작음 | 중간 |
| **학습 곡선** | 낮음 | 낮음 | 높음 | 중간 |
| **브라우저 호환성** | 우수 | 우수 | 제한적 | 우수 |
| **도구 생태계** | 제한적 | 풍부 | 풍부 | 성장 중 |

### 6.2 사용 시나리오별 권장 프로토콜

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         프로토콜 선택 의사결정 트리                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  시작                                                                        │
│   │                                                                         │
│   ├─ 고성능 내부 마이크로서비스?                                             │
│   │   ├─ YES → gRPC (HTTP/2, Protocol Buffers)                             │
│   │   └─ NO  → 계속                                                         │
│   │                                                                         │
│   ├─ 공개 API 제공?                                                          │
│   │   ├─ YES → RESTful API (OpenAPI 표준, 도구 생태계)                     │
│   │   └─ NO  → 계속                                                         │
│   │                                                                         │
│   ├─ 복잡한 데이터 요구(Over-fetching/Under-fetching)?                      │
│   │   ├─ YES → GraphQL (유연한 쿼리)                                        │
│   │   └─ NO  → 계속                                                         │
│   │                                                                         │
│   ├─ 실시간 양방향 통신 필요?                                                │
│   │   ├─ YES → JSON-RPC over WebSocket 또는 gRPC 스트리밍                   │
│   │   └─ NO  → 계속                                                         │
│   │                                                                         │
│   ├─ 단순한 메서드 호출, 경량성 중시?                                        │
│   │   ├─ YES → JSON-RPC 2.0                                                │
│   │   └─ NO  → RESTful API                                                  │
│   │                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. 기술사적 판단 및 실무 고려사항

### 7.1 아키텍처 설계 시 고려사항

#### 7.1.1 마이크로서비스 아키텍처 내 JSON-RPC 배치

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    마이크로서비스 내 JSON-RPC 활용 아키텍처                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐       HTTP/HTTPS/WebSocket        ┌─────────────┐         │
│  │   게이트웨이   │  ─────────────────────────────→  │  JSON-RPC   │         │
│  │  (Gateway)  │                                    │   서비스 A   │         │
│  └─────────────┘                                    └─────────────┘         │
│        │                                                 │                 │
│        │        ┌─────────────────────────────────┐     │                 │
│        │        │        JSON-RPC 로드 밸런서      │     │                 │
│        │        └─────────────────────────────────┘     │                 │
│        │                                                 │                 │
│  ┌─────────────┐                                        │                 │
│  │   인증서비스  │  ────────────────────────────────────┘                 │
│  └─────────────┘                                                              │
│                                                                             │
│  ┌─────────────┐       HTTP/HTTPS/WebSocket        ┌─────────────┐         │
│  │  클라이언트    │  ←────────────────────────────  │  JSON-RPC   │         │
│  │  (Browser)  │                                    │   서비스 B   │         │
│  └─────────────┘                                    └─────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**설계 원칙:**
1. **서비스 분리**: 각 JSON-RPC 서비스는 단일 책임 원칙(Single Responsibility Principle) 준수
2. **버전 관리**: URL 경로 또는 헤더를 통한 API 버전 관리 (예: `/v1/rpc`)
3. **회복탄력성(Resilience)**: 서킷 브레이커(Circuit Breaker), 재시도(Retry) 메커니즘 구현
4. **관측 가능성(Observability)**: 로깅, 메트릭, 분산 추적(Distributed Tracing) 통합

#### 7.1.2 보안 아키텍처

| 보안 계층 | 보안 메커니즘 | 구현 방안 |
|-----------|---------------|-----------|
| 전송 계층 | TLS 1.3 암호화 | HTTPS, WSS (Secure WebSocket) |
| 인증 | JWT, OAuth 2.0, API Key | Authorization 헤더 또는 쿼리 파라미터 |
| 권한 | Role-Based Access Control (RBAC) | 메서드 레벨 권한 검증 |
| 요청 검증 | Rate Limiting, CSRF 방지 | API Gateway에서 처리 |
| 데이터 검증 | JSON-Schema 유효성 검사 | 서버 사이드 입력 유효성 검증 |

### 7.2 성능 최적화 전략

| 최적화 영역 | 기술 | 기대 효과 |
|-------------|------|-----------|
| **네트워크** | HTTP/2 Multiplexing, GZIP 압축 | 레이턴시 20-40% 감소 |
| **직렬화** | MessagePack (Binary JSON) | 페이로드 크기 30% 감소 |
| **캐싱** | Redis 캐싱, HTTP 캐싱 | 응답 시간 50-70% 향상 |
| **배치 처리** | Batch Request 활용 | 네트워크 왕복 횟수 감소 |
| **커넥션 풀링** | Keep-Alive, 커넥션 재사용 | 커넥션 설정 오버헤드 제거 |
| **비동기 처리** | Event Loop, Worker Pool | 서버 처리량 2-3배 증가 |

### 7.3 모니터링 및 운영

#### 7.3.1 핵심 메트릭 (Key Metrics)

| 메트릭 | 설명 | 임계값(Threshold) |
|--------|------|-------------------|
| 요청 처리량(RPS) | 초당 요청 수 | 서버 사양에 따라 100-10,000+ |
| 응답 시간(Latency) | 요청부터 응답까지의 시간 | p95 < 200ms, p99 < 500ms |
| 에러율(Error Rate) | 전체 요청 중 에러 비율 | < 0.1% |
| 큐 길이(Queue Length) | 대기 중인 요청 수 | < 100 |
| 커넥션 수(Active Connections) | 활성 연결 수 | 커넥션 풀 크기의 80% 이하 |

#### 7.3.2 로깅 전략

```json
{
  "timestamp": "2025-01-18T10:30:45.123Z",
  "level": "info",
  "request_id": "abc-123-def-456",
  "method": "subtract",
  "params": [42, 23],
  "client_ip": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "response_time_ms": 45,
  "status": "success"
}
```

**로깅 원칙:**
1. 구조화된 로그(JSON 형식) 사용
2. 요청 ID(Request ID)를 통한 분산 추적
3. 민감 정보(PII) 마스킹
4. 로그 레벨 적절한 분류

---

## 8. 구현 예시

### 8.1 서버 구현 (Node.js)

```javascript
const http = require('http');

const jsonRPCHandlers = {
  add: (params) => params[0] + params[1],
  subtract: (params) => params[0] - params[1],
  multiply: (params) => params[0] * params[1],
  divide: (params) => {
    if (params[1] === 0) {
      throw { code: -32602, message: "Division by zero" };
    }
    return params[0] / params[1];
  }
};

const server = http.createServer((req, res) => {
  let body = '';

  req.on('data', (chunk) => {
    body += chunk.toString();
  });

  req.on('end', () => {
    try {
      const request = JSON.parse(body);
      const { method, params, id } = request;
      const handler = jsonRPCHandlers[method];

      if (!handler) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          jsonrpc: "2.0",
          error: { code: -32601, message: "Method not found" },
          id: id
        }));
        return;
      }

      const result = handler(params);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        jsonrpc: "2.0",
        result: result,
        id: id
      }));

    } catch (error) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        jsonrpc: "2.0",
        error: { code: -32600, message: error.message || "Invalid request" },
        id: null
      }));
    }
  });
});

server.listen(3000, () => {
  console.log('JSON-RPC Server running on port 3000');
});
```

### 8.2 클라이언트 구현 (Python)

```python
import requests
import json

class JSONRPCClient:
    def __init__(self, url):
        self.url = url
        self.request_id = 0

    def call(self, method, params=None):
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params if params else [],
            "id": self.request_id
        }

        response = requests.post(
            self.url,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )

        result = response.json()

        if 'error' in result:
            raise Exception(f"RPC Error {result['error']['code']}: {result['error']['message']}")

        return result['result']

    def notify(self, method, params=None):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params if params else []
        }

        requests.post(
            self.url,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )

    def batch_call(self, calls):
        self.request_id += 1
        batch = []

        for call in calls:
            self.request_id += 1
            batch.append({
                "jsonrpc": "2.0",
                "method": call['method'],
                "params": call.get('params', []),
                "id": self.request_id
            })

        response = requests.post(
            self.url,
            json=batch,
            headers={'Content-Type': 'application/json'}
        )

        return response.json()

# 사용 예시
client = JSONRPCClient('http://localhost:3000')

# 단일 호출
result = client.call('add', [42, 23])
print(f"Result: {result}")

# 알림
client.notify('logMessage', ['Notification test'])

# 배치 호출
results = client.batch_call([
    {'method': 'add', 'params': [1, 2]},
    {'method': 'subtract', 'params': [10, 5]},
    {'method': 'multiply', 'params': [3, 4]}
])
print(f"Batch results: {results}")
```

---

## 9. 미래 전망

### 9.1 기술 트렌드

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        JSON-RPC 기술 트렌드 로드맵                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  2025                                                                      │
│  ├─ JSON-RPC 2.0 표준 안정화                                                │
│  ├─ WebSocket 기반 실시간 JSON-RPC 보편화                                    │
│  └─ GraphQL + JSON-RPC 하이브리드 패턴 등장                                 │
│                                                                             │
│  2026-2027                                                                 │
│  ├─ JSON-RPC over HTTP/3 (QUIC) 채택                                       │
│  ├─ AI 기반 JSON-RPC API 자동 생성                                          │
│  └─ 표준화된 JSON-RPC 서비스 메시(Service Mesh) 통합                         │
│                                                                             │
│  2028+                                                                     │
│  ├─ WebAssembly 기반 JSON-RPC 핸들러                                        │
│  ├─ JSON-RPC 표준화 에코시스템 완성                                          │
│  └─ 다중 프로토콜 통합 (JSON-RPC + gRPC + REST)                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 새로운 사용 사례

| 영역 | 사용 사례 | JSON-RPC 역할 |
|------|-----------|---------------|
| **서버리스(Serverless)** | AWS Lambda, Cloud Functions | API 게이트웨이와 함수 간 경량 통신 |
| **Edge Computing** | Cloudflare Workers, Vercel Edge | 엣지 노드 간 메서드 호출 |
| **IoT (Internet of Things)** | 센서 네트워크, 스마트 홈 | 리소스 제한 환경의 통신 프로토콜 |
| **Web3 (Decentralized Web)** | Ethereum JSON-RPC, 블록체인 노드 | 블록체인 노드와 지갑 간 통신 |
| **AI/ML 서비스** | 모델 추론, 데이터 전처리 | AI 서비스 API 엔드포인트 |

### 9.3 산업별 적용 전망

| 산업 | 2025 | 2030 (예상) |
|------|------|-------------|
| **핀테크** | 내부 시스템 통합 | 실시간 결제, 블록체인 상호운용성 |
| **헬스케어** | 의료 기기 통신 | 원격 진료 시스템, AI 기반 진단 |
| **모바일** | 하이브리드 앱 통신 | 5G 기반 실시간 협업 앱 |
| **엔터프라이즈** | 레거시 시스템 마이그레이션 | 마이크로서비스 전면 도입 |

---

## 10. 결론

**JSON-RPC (JavaScript Object Notation - Remote Procedure Call)**는 경량성, 구현 용이성, 전송 계층 독립성이라는 장점을 통해 웹 및 모바일 애플리케이션, 마이크로서비스 아키텍처, IoT 환경 등 다양한 분야에서 중요한 역할을 수행하고 있습니다.

기술사 시험의 관점에서 JSON-RPC는 다음과 같은 핵심 평가 요소를 갖습니다:

1. **아키텍처 설계 능력**: RESTful API, gRPC와의 비교를 통한 적합한 프로토콜 선정
2. **성능 최적화**: 배치 요청, 캐싱, 커넥션 풀링을 통한 시스템 성능 향상
3. **보안 설계**: TLS, 인증/권한, 요청 검증을 포함한 보안 아키텍처 구축
4. **운영 관리**: 모니터링, 로깅, 에러 처리를 통한 시스템 안정성 확보
5. **미래 대응력**: HTTP/3, WebAssembly, 서버리스 등 신기술과의 통합 가능성

JSON-RPC는 복잡한 엔터프라이즈 시스템에서는 gRPC나 RESTful API와 함께 사용되며, 특히 경량성과 실시간성이 요구되는 상황에서 효과적인 솔루션으로 자리매김하고 있습니다. 기술사는 프로젝트의 요구사항, 제약 조건, 성능 목표를 종합적으로 분석하여 JSON-RPC를 적절히 활용하는 능력을 갖춰야 합니다.

---

## 부록: 어린이 버전 설명

---

### 어린이를 위한 JSON-RPC 이야기 🚀

#### 📖 쉬운 비유로 이해하기

**JSON-RPC**는 마치 **"전화로 피자 주문하기"**와 비슷해요!

---

#### 🍕 피자 주문 비유

```
┌─────────────────┐                    ┌─────────────────┐
│                 │                    │                 │
│   너 (고객)     │                    │  피자 가게      │
│                 │                    │                 │
└─────────────────┘                    └─────────────────┘
        │                                        │
        │   📞 전화 걸기                          │
        │   "페퍼로니 피자 주문할게요!"            │
        │   ────────────────────────────────→    │
        │                                        │
        │                                        │   👨‍🍳 피자 만들기
        │                                        │
        │   🍕 피자 배달                          │
        │   ←────────────────────────────────    │
```

| 피자 주문 | JSON-RPC |
|-----------|----------|
| 전화 걸기 | **요청(Request)** 보내기 |
| 메뉴 이름 | **메서드(method)** (어떤 일을 할지) |
| 추가 토핑 | **매개변수(params)** (추가 정보) |
| 주문 번호 | **ID** (내 주문인지 확인) |
| 피자 배달 | **응답(Response)** 받기 |

---

#### 🎮 비디오 게임 비유

**JSON-RPC**는 **게임 캐릭터에게 명령 내리기**와 같아요!

```javascript
// 1. 요청: "달려!"
{
  "method": "run",        // 무엇을 할지
  "params": ["fast"],     // 어떻게 할지
  "id": 1                 // 명령 번호
}

// 2. 응답: "달리기 시작했어!"
{
  "result": "running",    // 결과
  "id": 1                 // 같은 명령 번호
}
```

**게임에서의 예시:**
- `run("fast")` → "달리기 시작했어!"
- `jump()` → "점프했어!"
- `attack()` → "공격했어!"

---

#### 📦 택배 배송 비유

**배치 요청(Batch Request)**은 **한 번에 여러 택배 보내기**와 같아요!

```
┌─────────────────┐                    ┌─────────────────┐
│                 │                    │                 │
│   발송인        │                    │   택배 회사      │
│                 │                    │                 │
└─────────────────┘                    └─────────────────┘
        │                                        │
        │   📦📦📦 한 번에 3개의 택배 보내기      │
        │   ────────────────────────────────→    │
        │                                        │
        │                                        │   🚚 택배 배달
        │                                        │
        │   ✅✅✅ 한 번에 3개의 배달 완료        │
        │   ←────────────────────────────────    │
```

**장점:** 택배 하나씩 보내는 것보다 훨씬 빨라요! 🚀

---

#### 🎨 그림으로 보는 JSON-RPC

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   👦 클라이언트 (나)               🖥️ 서버 (컴퓨터)         │
│                                                             │
│   📝 "계산해줘! 5 + 3"          →                           │
│                                   🧮 "5 더하기 3은 8이야!"   │
│                          ←        💬 "8이야!"              │
│                                                             │
│   📝 "빼줘! 10 - 2"          →                           │
│                                   🧮 "10 빼기 2는 8이야!"   │
│                          ←        💬 "8이야!"              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

#### 🌟 왜 JSON-RPC가 좋을까요?

| 좋은 점 | 설명 | 예시 |
|---------|------|------|
| **가벼워요** | 쉽게 이해할 수 있어요 | "더하기"라는 말만 하면 돼요 |
| **빨라요** | 복잡한 설명이 필요 없어요 | 긴 문장 대신 짧은 단어 |
| **친해요** | 모든 컴퓨터가 이해해요 | 한국어, 영어, 중국어 모두 OK |

---

#### 🎭 알림(Notification) 이야기

**알림**은 **응답을 기다리지 않는 말하기**예요!

```
┌─────────────────┐                    ┌─────────────────┐
│                 │                    │                 │
│   📢 스피커      │                    │   👥 청중들      │
│                 │                    │                 │
└─────────────────┘                    └─────────────────┘
        │                                        │
        │   "오늘 점심은 피자 먹을 거예요!"        │
        │   ────────────────────────────────→    │
        │   (답장 기다리지 않아요)                  │
        │                                        │
```

**JSON-RPC에서:**
```json
{
  "method": "sayHello",
  "params": ["안녕하세요!"]
}
// ID가 없어요 = 답장이 필요 없어요!
```

---

#### 🤔 에러(Error) 처리하기

**에러**는 **주문이 실패했을 때** 알려주는 거예요!

```
📞 고객: "하늘색 피자 주문할게요!"
🍕 가게: "죄송해요, 하늘색 피자는 없어요!"
```

**JSON-RPC에서:**
```json
{
  "error": {
    "code": -32601,
    "message": "하늘색 피자는 메뉴에 없어요!"
  },
  "id": 1
}
```

---

#### 🎓 요약: JSON-RPC 한 문장으로

> **JSON-RPC = 컴퓨터끼리 "이것 해줘!"라고 말하고, 그 결과를 받는 간단한 약속**

---

#### 📚 기억하기 쉬운 암기법

**J-S-O-N-R-P-C:**

| 알파벳 | 기억할 말 | 의미 |
|--------|-----------|------|
| **J** | **J**ust | 그냥 쉽게 |
| **S** | **S**end | 요청을 보내고 |
| **O** | **O**ne | 하나씩 또는 여러 개 |
| **N** | **N**ow | 지금 바로 처리 |
| **R** | **R**esult | 결과를 받아요 |
| **P** | **P**rotocol | 이게 통신 규칙이에요 |
| **C** | **C**ool | 정말 멋져요! |

---

#### 🎮 직접 해보기 (가상 체험)

```javascript
// 1. 더하기 요청
{
  "method": "add",
  "params": [5, 3],
  "id": 1
}
// 결과: 8

// 2. 빼기 요청
{
  "method": "subtract",
  "params": [10, 4],
  "id": 2
}
// 결과: 6

// 3. 곱하기 요청
{
  "method": "multiply",
  "params": [2, 5],
  "id": 3
}
// 결과: 10
```

---

이제 **JSON-RPC**가 무엇인지 이해했나요? 🎉

**핵심:** "컴퓨터끼리 쉽고 빠르게 대화하는 방법"이라는 걸 기억하세요!
