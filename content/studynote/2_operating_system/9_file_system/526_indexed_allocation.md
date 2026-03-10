+++
title = "526. 색인 할당 (Indexed Allocation) - 모든 블록 포인터를 색인 블록(Index Block) 하나에 모아 저장"
weight = 526
+++

# 526. 리액터 패턴 (Reactor Pattern)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이벤트 기반 비동기 I/O 처리
> 2. **가치**: 확장성과 유연성이 좋음
 3. **융합**: 비동기 I/O, 이벤트 루프, 콜백과 연관

---

## Ⅰ. 개요

### 개념 정의
**리액터 패턴(Reactor Pattern)**은 **비동기 I/O 이벤트를 처리하는 디자인 패턴**입니다.

### 💡 비유: 음식점 주문
리액터 패턴은 **음식점에서 주문을 받아 요리사가 준비되면 요리사에게 알리는 방식**과 같다. 주문이 들어오자 요리사는 처리합니다

### 리액터 패턴 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                리액터 패턴 구조                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【구성 요소】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │   Handles (핸들러) ───▶ Demultiplexer (디멀티플렉서) ◀──▶ Acceptor (수락기)      │   │   │
│  │      │                   │             │              │             │ │   │
│  │      │                   │             │              │             │ │   │
│  │      ▼                   │             ▼              │             │ │   │
│  │   Concrete Handlers                                            │   │   │
│  │   (구체적 핸들러 구현)                                    │   │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【작동 흐름】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  1. Acceptor 이벤트 감시                              │ │   │
│  │  2. 이벤트 발생 시 Demultiplexer에 전달                │ │   │
│  │  3. Demultiplexer가 적절한 Handler 호출                 │ │   │
│  │  4. Handler가 비즈니스 로직 수행                   │ │   │
│  │  5. 결과를 Completion Handler로 전달                │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【구현 예시: Java NIO]                                    │
│  ──────────────────                                                │
│  // Selector (Acceptor 역할)                                │
│  Selector selector = Selector.open();                     │
│  ServerSocketChannel server = ServerSocketChannel.open();       │
│  server.register(selector, SelectionKey.OP_ACCEPT);           │
│                                                             │
│  // 이벤트 루프                                         │
│  while (true) {                                          │
│      selector.select();                                   │
│      for (SelectionKey key : selector.selectedKeys()) {          │
│          if (key.isAcceptable()) {                            │
│              SocketChannel client = server.accept();            │
│              client.register(selector, SelectionKey.OP_READ);   │
│          }                                                     │
│          if (key.isReadable()) {                             │
│              // Demultiplexer가 Handler 호출                    │
│              handleRead(key);                              │
│          }                                                     │
│      }                                                       │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                리액터 패턴 상세                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Demultiplexer 구현】                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  class Demultiplexer {                                    │ │   │
│  │      private Map<EventType, EventHandler> handlers = new HashMap<>();       │ │   │
│  │                                                             │ │   │
│  │      public void registerHandler(EventType type, EventHandler handler) {       │   │
│  │          handlers.put(type, handler);                        │ │   │
│  │      }                                                 │   │   │
│  │      public void dispatch(Event event) {                      │ │   │
│  │          EventHandler handler = handlers.get(event.getType());           │   │
│  │          if (handler != null) {                             │ │   │
│  │              handler.handle(event);                          │ │   │
│  │          }                                                 │   │   │
│  │      }                                                 │   │   │
│  │  }                                                   │   │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Java NIO 예시】                                              │
│  ──────────────────                                                │
│  class EchoHandler implements CompletionHandler {                 │
│      public void completed(Session session, {                       │
│          System.out("Echo: " + session.data());               │
│      }                                                     │   │   │
│  }                                                             │
│  class ReadHandler implements EventHandler {                     │
│      public void handle(Event event) {                         │
│          if (event.type == EventType.READ) {                    │
│              ByteBuffer buf = ByteBuffer.allocate(1024);               │
│              SocketChannel channel = (SocketChannel) event.source;   │
│              channel.read(buf);                                 │
│              // 비즈니스 로직 수행...                         │
│          }                                                 │   │   │
│      }                                                     │   │   │
│  }                                                             │
│  【장단점】                                                 │
│  ──────────────────                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  장점:                                                                 │ │   │
│  │  • 높은 동시성: 단일 스레드로 많은 연결 처리               │ │   │
│  │  • 확장성: 새로운 핸들러 쉽게 추가                 │ │   │
│  │  • 유연성: 핸들러 교체가 용이                    │ │   │
│  │  • 테스트 용이: Mock 핸들러 주입 가능                  │ │   │
│  │                                                             │ │   │
│  │  단점:                                                                 │ │   │
│  │  • 콜백 복잡성: 핸들러 체인이 길어질 수 있음              │ │   │
│  │  • 제어 흐름: 반환 흐름이 복잡할 수 있음                  │ │   │
│  │  • 디버깅: 비동기 흐름 추적이 어려움                  │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Java NIO 리액터 구현】                                         │
│  ──────────────────                                                │
│  import java.nio.channels.*;                             │
│  import java.nio.ByteBuffer;                              │
│                                                             │
│  // Acceptor 역할                                         │
│  class ReactorAcceptor {                               │
│      private Selector selector;                               │
│      private ServerSocketChannel server;                   │
│                                                             │
│      public ReactorAcceptor(int port) throws IOException {            │
│          selector = Selector.open();                         │
│          server = ServerSocketChannel.open();                   │
│          server.bind(new InetSocketAddress(port)););              │
│          server.register(selector, SelectionKey.OP_ACCEPT);           │
│      }                                                     │   │   │
│                                                             │
│      public void accept() throws IOException {                 │
│          if (key.isAcceptable()) {                              │
│              SocketChannel client = server.accept();            │
│              client.configureBlocking(false);                  │
│              client.register(selector, SelectionKey.OP_READ);           │
│          }                                                     │   │   │
│      }                                                 │   │   │
│  }                                                             │
│  // Demultiplexer 역할                                │
│  class ReactorDemultiplexer {                         │
│      private Map<Integer, EventHandler> handlers = new HashMap<>();       │
│                                                             │
│      public void registerHandler(int type, EventHandler handler) {       │   │
│          handlers.put(type, handler);                        │
│      }                                                     │   │   │
│                                                             │
│      public void dispatch(int type, SelectionKey key) {                │
│          EventHandler handler = handlers.get(type);            │
│          if (handler != null) {                             │
│              handler.handle(key);                       │
│          }                                                 │   │   │
│      }                                                 │   │   │
│  }                                                             │
│  // 이벤트 루프                                            │
│  class ReactorEventLoop {                              │
│      private Selector selector;                               │
│      private boolean running = true;                     │
│                                                             │
│      public void run() throws IOException {                 │
│          while (running) {                              │
│              selector.select();                             │
│              Iterator<SelectionKey> it = selector.selectedKeys().iterator();   │
│              while (it.hasNext()) {                            │
│                  SelectionKey key = it.next();               │
│                  // 이벤트 디스패치                       │
│                  dispatch(key);                       │
│              }                                                 │   │   │
│          }                                                 │   │   │
│      }                                                 │   │   │
│  }                                                             │
│  【C libuv 예시 (libuv reactor)]】                                   │
│  ──────────────────                                            │
│  #include <uv.h>                                     │
│  #include <stdlib.h>                               │
│                                                             │
│  void on_read(uv_stream_t *stream, ssize_t nread, const uv_buf_t *buf, void *priv) {  │
│      // 데이터 처리                                         │
│      printf("Read %ld bytes\n", nread);                       │
│  }                                                     │   │   │
│                                                             │
│  int main() {                                            │
│      uv_loop_t *loop = uv_default_loop();                  │
│      uv_tcp_t server;                                │
│      struct sockaddr_in addr;                            │
│                                                             │
│      // 서버 설정                               │
│      uv_tcp_init(loop, &server);                        │
│      uv_ip4_addr("0.0.0.0", 8080, &addr);                  │
│      uv_tcp_bind(&server, (const struct sockaddr*)&addr, 0);          │
│      uv_listen((uv_stream_t*)&server, 128, on_new_connection);    │
│                                                             │
│      // 이벤트 루프 실행                               │
│      uv_run(loop, UV_RUN_DEFAULT);                     │
│      return 0;                                          │
│  }                                                     │
│                                                             │
│  void on_new_connection(uv_stream_t *server, int status) {         │
│      if (status < 0) {                              │
│          fprintf(stderr, "New connection error %s\n", uv_strerror(status));  │
│          return;                                       │
│      }                                                 │
│                                                             │
│      uv_tcp_t *client = (uv_tcp_t*)malloc(sizeof(uv_tcp_t));         │
│      uv_tcp_init(loop, client);                        │
│      uv_accept(server, (uv_stream_t*)client, on_read);            │
│  }                                                     │
│                                                             │
│  【Node.js 리액터 예시】                                      │
│  ──────────────────                                            │
│  const net = require('net');                          │
│                                                             │
│  // 서버 생성 (Node.js는 기본적으로 리액터 패턴 사용)          │
│  const server = net.createServer((socket) => {        │
│      socket.on('data', (data) => {                     │
│          // 핸들러 호출                               │
│          handleData(data);                            │
│      });                                             │
│  });                                                 │
│  server.listen(8080);                                 │
│                                                             │
│  【Twisted (Python) 예시】                                    │
│  ──────────────────                                            │
│  from twisted.internet import reactor               │
│  from twisted.internet.protocol import Protocol, Factory  │
│                                                             │
│  class EchoProtocol(Protocol):                       │
│      def dataReceived(self, data):                   │
│          self.transport.write(data)                  │
│                                                             │
│  class EchoFactory(Factory):                        │
│      def buildProtocol(self, addr):                  │
│          return EchoProtocol()                       │
│                                                             │
│  reactor.listenTCP(8080, EchoFactory())             │
│  reactor.run()                                       │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 이벤트 기반 비동기 I/O 처리 패턴
• 구성: Acceptor, Demultiplexer, Handlers
• Acceptor: 이벤트 감시
• Demultiplexer: 이벤트 분배
• Handler: 이벤트 처리
• 장점: 높은 동시성, 확장성, 유연성
• 단점: 콜백 복잡성, 디버깅 어려움
• 구현: Java NIO, libuv, Node.js, Twisted
• 용도: 웹서버, 채팅 서버, 게임 서버
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [비동기 I/O](./517_asynchronous_io.md) → 비동기 처리
- [I/O 멀티플렉싱](./519_io_multiplexing.md) → 이벤트 감시
- [이벤트 루프](./520_event_loop.md) → 이벤트 처리



### 👶 어린이를 위한 3줄 비유 설명

**개념**: 리액터 패턴은 "음식점 주문 시스템" 같아요!

**원리**: 주문이 들어오면 담당자가 처리해요!

**효과**: 많은 주문을 빠르게 처리해요!
