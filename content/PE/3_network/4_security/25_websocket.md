+++
title = "25. WebSocket"
date = 2026-03-06
categories = ["studynotes-network"]
tags = ["WebSocket", "Real-time", "Full-Duplex", "Push", "TCP"]
draft = false
+++

# WebSocket

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: WebSocket은 **"단일 **TCP **연결**에서 **양방향**(Full-Duplex) **실시간 **통신**을 **제공**하는 **프로토콜"**으로, **HTTP Upgrade**로 **초기 **연결**을 **설정**하고 **프레임**(Frame) 기반 **메시지**를 **교환**하며 **Server Push**가 **가능**하다.
> 2. **가치**: **HTTP Polling**(주기적 요청)의 **오버헤드**를 **제거**하고 **Real-time**으로 **데이터**를 **전송**하며 **Chat**, **Gaming**, **Collaboration** 같은 **Interactive** 애플리케이션에 **적합**하다.
> 3. **융합**: **WS**(WebSocket Secure)는 **TLS**로 **암호화**하며 **Socket.io**, **SignalR**, **ws**(Node.js)가 **라이브러리**를 **제공**하고 **HTTP/3**는 **QUIC** 위에서 **WebSocket**을 **지원**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
WebSocket은 **"양방향 실시간 통신 프로토콜"**이다.

**WebSocket 특징**:
- **Full-Duplex**: 동시 송수신
- **Persistent**: 연결 유지
- **Low Latency**: 헤더 적음
- **Server Push**: 서버 전송

### 💡 비유
WebSocket은 **"전화 회선****과 같다.
- **연결**: TCP Handshake
- **대화**: 양방향
- **끊김**: Close

---

## Ⅱ. 아키텍처 및 핵심 원리

### WebSocket Handshake

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         WebSocket Handshake                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Client                                                Server
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  HTTP Upgrade Request                                                                 │  │
    │  ──────────────────────────────────────────────────────────────────────────────────────────▶│
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  GET /chat HTTP/1.1                                                                 │  │  │
    │  │  Host: server.example.com                                                             │  │  │
    │  │  Upgrade: websocket                                                                   │  │  │
    │  │  Connection: Upgrade                                                                 │  │  │
    │  │  Sec-WebSocket-Key: dGhlIHNhbXBwIG5vce==                                               │  │  │
    │  │  Sec-WebSocket-Version: 13                                                            │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  ◀──────────────────────────────────────────────────────────────────────────────────────────│
    │  HTTP Switching Protocols                                                               │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  HTTP/1.1 101 Switching Protocols                                                    │  │  │
    │  │  Upgrade: websocket                                                                   │  │  │
    │  │  Connection: Upgrade                                                                 │  │  │
    │  │  Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=                                     │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  → WebSocket Connection Established!                                                     │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### WebSocket Frame

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         WebSocket Frame Structure                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  0     1     2     3             4                   5               6                 7      │  │
    │  0─────┬─────┬─────┬─────────────┬───────────────────┬───────────────────────┬──────│  │
    │  │ FIN │ RSV1│ RSV2│ RSV3│                OPCODE                  │ MASK                  │ Payload    │  │
    │  │     │     │     │     │  │  │  │x                 │  │  │  │                     │          │  │
    │  └─────┴─────┴─────┴─────┴─────────────┴───────────────────┴───────────────────────┴──────┘  │
    │                                                                                         │  │
    │  FIN: 0=continues, 1=last frame                                                        │  │
    │  Opcode: 0x1=TEXT, 0x2=BINARY, 0x8=CLOSE                                             │  │
    │  MASK: 1=client sends masked, 0=server sends unmasked                                    │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 통신 방식 비교

| 구분 | HTTP Polling | Long Polling | WebSocket |
|------|--------------|---------------|-----------|
| **지연** | 높음 | 중간 | 낮음 |
| **오버헤드** | 높음 | 중간 | 낮음 |
| **Server Push** | X | O | O |

### WebSocket vs SSE

| 구분 | WebSocket | SSE |
|------|-----------|-----|
| **통신** | 양방향 | 단방향 |
| **바이너리** | O | X |
| **프로토콜** | WS | HTTP |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Chat 앱
**상황**: 실시간 메시지
**판단**:

```javascript
// Client
const ws = new WebSocket('wss://example.com/chat');

ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'join', room: 'general' }));
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    displayMessage(msg);
};

// Server (Node.js)
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
    ws.on('message', (data) => {
        wss.clients.forEach((client) => {
            if (client !== ws) client.send(data);
        });
    });
});
```

---

## Ⅴ. 기대효과 및 결론

### WebSocket 기대 효과

| 효과 | Polling | WebSocket |
|------|---------|-----------|
| **지연** | 1~N초 | <100ms |
| **부하** | 높음 | 낮음 |
| **복잡도** | 낮음 | 중간 |

### 미래 전망

1. **HTTP/3**: QUIC 기반
2. **WebRTC**: P2P
3. **Graphql**: Subscription

### ※ 참고 표준/가이드
- **RFC 6455**: WebSocket
- **MDN**: WebSocket API

---

## 📌 관련 개념 맵

- [HTTP](./4_http/1_http_overview.md) - 기초
- [HTTPS](./4_security/23_https.md) - 보안
- [REST](./4_security/24_rest_api.md) - API
