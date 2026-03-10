+++
title = "527. 색인 블록 크기 한계 해결 - 연결 색인, 다중 수준 색인 (Multilevel Index)"
weight = 527
+++

# 527. 프로액터 패턴 (Proactor Pattern)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비동기 작업 완료를 기다리는 패턴
> 2. **가치**: 진정한 비동기 처리와 높은 성능
> 3. **융합**: 리액터, 비동기 I/O, 완료 포트와 연관

---

## Ⅰ. 개요

### 개념 정의
**프로액터 패턴(Proactor Pattern)**은 **비동기 작업이 완료되면 그에 따른 핸들러를 호출하는 디자인 패턴**입니다.

### 💡 비유: 음식 호출기
프로액터 패턴은 **음식점의 호출기(삐삐)와 같습니다.** 음식이 완성되면 호출기가 울리고, 손님이 음식을 받으러 갑니다.

### 프로액터 패턴 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                프로액터 패턴 구조                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【구성 요소】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │   Proactor (프로액터)                                        │   │   │
│  │   ───▶ 비동기 작업 관리                                       │   │   │
│  │      │                                                        │ │   │
│  │      ▼                                                        │ │   │
│  │   Asynchronous Operation Processor (비동기 작업 처리기)          │   │   │
│  │   ───▶ 실제 비동기 작업 수행                                     │   │   │
│  │      │                                                        │ │   │
│  │      ▼                                                        │ │   │
│  │   Completion Handler (완료 핸들러)                               │   │   │
│  │   ───▶ 작업 완료 시 호출                                        │   │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【작동 흐름】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. Initiator가 비동기 작업 요청                                │ │   │
│  │  2. Proactor가 작업을 Asynchronous Processor에 전달             │ │   │
│  │  3. Asynchronous Processor가 작업 수행                           │ │   │
│  │  4. 작업 완료 시 Completion Event 큐에 이벤트 추가               │ │   │
│  │  5. Proactor가 이벤트를 꺼내 Completion Handler 호출             │ │   │
│  │  6. Completion Handler가 결과 처리                              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【프로액터 vs 리액터】                                               │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특징            리액터                    프로액터                  │ │   │
│  │  ────            ────                    ────────                  │ │   │
│  │  이벤트 시점      읽기/쓰기 가능         작업 완료 시                │ │   │
│  │  작업 수행        애플리케이션이           운영체제/커널              │ │   │
│  │  스레드 모델      단일/다중 스레드        다중 스레드                │ │   │
│  │  복잡도           낮음                     높음                      │ │   │
│  │  성능             중간                     높음                      │ │   │
│  │  예시             Java NIO, epoll         Windows IOCP, Boost.Asio   │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                프로액터 패턴 상세                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Windows IOCP (I/O Completion Port)】                                │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  // 완료 포트 생성                                          │   │   │
│  │  HANDLE iocp = CreateIoCompletionPort(                       │   │   │
│  │      INVALID_HANDLE_VALUE, NULL, 0, 0);                       │   │   │
│  │                                                             │ │   │
│  │  // 비동기 읽기 요청                                          │   │   │
│  │  OVERLAPPED overlapped = {0};                               │   │   │
│  │  ReadFile(handle, buffer, size, NULL, &overlapped);         │   │   │
│  │                                                             │ │   │
│  │  // 완료 대기                                                │   │   │
│  │  DWORD bytesTransferred;                                    │   │   │
│  │  ULONG_PTR completionKey;                                   │   │   │
│  │  LPOVERLAPPED pOverlapped;                                  │   │   │
│  │  GetQueuedCompletionStatus(iocp, &bytesTransferred,         │   │   │
│  │      &completionKey, &pOverlapped, INFINITE);               │   │   │
│  │                                                             │ │   │
│  │  // 완료 처리                                                │   │   │
│  │  handleCompletion(completionKey, bytesTransferred);          │   │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【Boost.Asio (C++)】                                                │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  #include <boost/asio.hpp>                                  │ │   │
│  │                                                             │ │   │
│  │  void handle_read(const boost::system::error_code& ec,        │   │   │
│  │              std::size_t bytes_transferred) {                  │   │   │
│  │      if (!ec) {                                              │   │   │
│  │          // 데이터 처리                                       │   │   │
│  │          process_data(buffer, bytes_transferred);             │   │   │
│  │      }                                                         │   │   │
│  │  }                                                             │ │   │
│  │                                                             │ │   │
│  │  void async_read() {                                          │   │   │
│  │      socket.async_read_some(boost::asio::buffer(buffer),      │   │   │
│  │          handle_read);                                         │   │   │
│  │  }                                                             │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【장단점】                                                           │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  장점:                                                       │ │   │
│  │  • 진정한 비동기: 작업 완료까지 대기 없음                   │ │   │
│  │  • 높은 성능: 커널이 직접 처리                                  │ │   │
│  │  • 확장성: 스레드 풀 활용 가능                               │ │   │
│  │  • 자원 효율: CPU 사용 최적화                               │ │   │
│  │                                                             │ │   │
│  │  단점:                                                       │ │   │
│  │  • 복잡성: 구현이 어려움                                │ │   │
│  │  • 플랫폼 의존: Windows IOCP, Boost.Asio 등 필요               │ │   │
│  │  • 디버깅: 비동기 흐름 추적이 어려움                  │ │   │
│  │  • 학습 곡선: 개념 이해가 어려움                 │ │   │
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
│  【Windows IOCP 서버 예시】                                         │
│  ──────────────────                                                │
│  #include <windows.h>                              │
│  #include <winsock2.h>                             │
│                                                             │
│  #define MAX_THREADS 4                              │
│                                                             │
│  HANDLE g_iocp;                               │
│  SOCKET g_listenSocket;                          │
│                                                             │
│  // 완료 핸들러                               │
│  void CALLBACK CompletionHandler(DWORD error, DWORD bytes,     │
│          LPWSAOVERLAPPED overlapped) {                      │
│      if (error == 0) {                               │
│          // 데이터 처리                                  │
│          ProcessData(overlapped, bytes);                  │
│      } else {                                              │
│          // 에러 처리                  │
│          HandleError(error);                         │
│      }                                                     │   │   │
│  }                                                     │   │   │
│                                                             │
│  // 비동기 읽기 시작                              │
│  void StartAsyncRead(SOCKET client) {                       │
│      LPWSAOVERLAPPED* overlapped = HeapAlloc(sizeof(WSAOVERLAPPED));  │
│      ZeroMemory(overlapped, 0, sizeof(WSAOVERLAPPED));               │
│      overlapped->hEvent = WSACreateEvent(NULL, NULL, 0, FALSE);  │
│      // 비동기 읽기 요청                                  │
│      WSABUF buf; {0};                              │
│      buf.len = BUFFER_SIZE;                              │
│      buf.buf = buffer;                              │
│      DWORD flags = 0;                              │
│      if (WSARecv(client, &buf, buf.len, &flags, NULL, overlapped) == 0) {   │
│          // 에러 처리                                  │
│          HandleError(WSAGetLastError());                  │
│      }                                                 │   │   │
│      // 완료 포트에 알림 등록                      │
│      CreateIoCompletionPort((HANDLE)client, 0, NULL, g_iocp);               │
│  }                                                     │   │   │
│                                                             │
│  // 워커 스레드 함수                             │
│  DWORD WINAPI WorkerThread(LPVOID param) {                 │
│      DWORD bytesTransferred;                              │
│      ULONG_PTR completionKey;                             │
│      LPWSAOVERLAPPED pOverlapped;                          │
│                                                             │
│      while (TRUE) {                                │
│          // 완료 이벤트 대기                            │
│          if (GetQueuedCompletionStatus(g_iocp, &bytesTransferred,                 │
│                          &completionKey, &pOverlapped, INFINITE)) {               │
│              // 완료 핸들러 호출                            │
│              CompletionHandler(NOErr, bytesTransferred, pOverlapped);                │
│          }                                                 │   │   │
│      }                                                 │   │   │
│      return 0;                                          │
│  }                                                     │   │   │
│                                                             │
│  int main() {                                            │
│      // 완료 포트 생성                              │
│      g_iocp = CreateIoCompletionPort(INVALID_handle_value, NULL, 0, 0);              │
│      if (g_iocp == NULL) return 1;                      │
│                                                             │
│      // 리슨 소켓 생성                      │
│      g_listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO);                │
│      bind(g_listenSocket, (struct sockaddr_in*)&addr, sizeof(addr));  │
│      listen(g_listenSocket, SOMAXCONN);                       │
│                                                             │
│      // 완료 포트에 소켓 연결                        │
│      createIoCompletionPort((HANDLE)g_listenSocket, 0, NULL, g_iocp);                │
│                                                             │
│      // 워커 스레드 생성                              │
│      HANDLE hThreads[MAX_THREADS];                       │
│      for (int i = 0; i < MAX_THREADS; i++) {                      │
│          hThreads[i] = CreateThread(NULL, 0, WorkerThread, NULL, 0, &_iocp);  │
│      }                                                 │   │   │
│                                                             │
│      // 연결 대기                              │
│      WaitForSingleObject(g_listenSocket, IN 1000);                      │
│      printf("Server listening on port 8080\n");               │
│      }                                                 │   │   │
│  }                                                     │   │   │
│                                                             │
│  【Boost.Asio 예시】                                         │
│  ──────────────────                                            │
│  #include <boost/asio.hpp>                               │
│  #include <iostream>                               │
│                                                             │
│  using namespace io = boost::asio::ip::tcp;                 │
│  using namespace io:: boost::asio::ip::tcp;socket;                │
│                                                             │
│  class Session :                               │
│      tcp::socket socket;                              │
│      boost::asio::streambuf buffer;                  │
│                                                             │
│      void start() {                                │
│          // 비동기 연결 요청                              │
│          boost::asio::async_connect(socket,                 │
│              boost::asio::ip::tcp::resolver::query("127.0.0.1"), 8080),                │
│              handle_connect);                            │
│          });                                                 │   │   │
│      }                                                 │   │   │
│                                                             │
│      void handle_connect(const boost::system::error_code& ec,            │
│          tcp::endpoint endpoint) {                   │
│          if (!ec) {                              │
│              std::cout << "Connect error: " << ec.message() << std::endl;                 │
│          } else {                              │
│              // 비동기 읽기 요청                            │
│              boost::asio::async_read(socket, boost::asio::buffer(buffer),                 │
│              handle_read);                            │
│          }                                                 │   │   │
│      }                                                 │   │   │
│                                                             │
│      void handle_read(const boost::system::error_code& ec, size_t len) {             │
│          if (!ec) {                              │
│              std::cout << "Read error: " << ec.message() << std::endl;                 │
│          } else {                              │
│              // 데이터 처리                              │
│              std::cout << "Read " << len << " bytes" << std::endl;                 │
│              // 다음 데이터 읽기                              │
│              start_read();                            │
│          }                                                 │   │   │
│      }                                                 │   │   │
│                                                             │
│      void start_read() {                                │
│          boost::asio::async_read(socket, boost::asio::buffer(buffer),                 │
│              handle_read);                            │
│          socket.async_read_some(boost::asio::buffer(buffer), handle_read);  │
│      }                                                 │   │   │
│                                                             │
│      void run() {                                │
│          boost::asio::io_context io_context;                   │
│          tcp::acceptor acceptor(io_context);                       │
│          start();                                │
│          io_context.run();                                │
│      }                                                 │   │   │
│  }                                                     │   │   │
│                                                             │
│  【libuv + Windows IOCP 예시】                               │
│  ──────────────────                                            │
│  // libuv는 IOCP를 사용하여 Windows에서 고성능 구현                │
│  #include <uv.h>                                │
│  #include <stdio.h>                             │
│                                                             │
│  void on_read(uv_stream_t*stream, ssize_t nread, const uv_buf_t *buf) {      │
│      // 데이터 처리                              │
│      printf("Read %ld bytes\n", nread);                       │
│      uv_stop_reading(stream);                            │
│  }                                                     │   │   │
│                                                             │
│  int main() {                                            │
│      uv_loop_t *loop = uv_default_loop();                  │
│      uv_tcp_t server;                                │
│      struct sockaddr_in addr;                            │
│                                                             │
│      uv_tcp_init(loop, &server);                         │
│      uv_ip4_addr("0.0.0.0", 8080, &addr);                      │
│      uv_tcp_bind(&server, (const struct sockaddr*)&addr, 0);                 │
│      uv_listen((uv_stream_t*)&server, 128, on_new_connection);               │
│                                                             │
│      uv_run(loop, UV_RUN_DEFAULT);                        │
│      return 0;                                          │
│  }                                                     │   │   │
│                                                             │
│  void on_new_connection(uv_stream_t *server, int status) {                │
│      if (status < 0) {                              │
│          fprintf(stderr, "New connection error %s\n", uv_strerror(status));               │
│          return;                                             │
│      }                                                 │   │   │
│                                                             │
│      uv_tcp_t *client = malloc(sizeof(uv_tcp_t));                  │
│      uv_tcp_init(loop, client);                         │
│      uv_accept(server, (uv_stream_t*)client, 0, NULL);                       │
│      uv_read_start((uv_stream_t*)client, alloc_read_buffer(), 0, on_read);                    │
│  }                                                     │   │   │
│                                                             │
│  void alloc_read_buffer() {                                │
│      buf.base = (char*) malloc(65536);                         │
│  }                                                     │   │   │
│                                                             │
│  void on_read(uv_stream_t *stream, ssize_t nread, const uv_buf_t *buf) {                  │
│      if (nread > 0) {                              │
│          // 더 이상 데이터 읽기                          │
│          buf.len += nread;                              │
│          uv_read_start(stream, alloc_read_buffer(), 0, on_read);                  │
│      } else if (nread == 0) {                        │
│          // 읽기 완료 - 클라이언트 종료                   │
│          uv_close((uv_handle_t*)stream);                        │
│      }                                                     │   │   │
│  }                                                     │   │   │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 비동기 작업 완료 시 핸들러 호출
• 구성: Proactor, Asynchronous Processor, Completion Handler
• 작동: 비동기 요청 → 작업 수행 → 완료 알림 → 핸들러 호출
• 리액터: 읽기/쓰기 가능 시점에 이벤트
• 프로액터: 작업 완료 시점에 이벤트
• 장점: 진정한 비동기, 높은 성능, 확장성
• 단점: 복잡성, 플랫폼 의존
 디버깅 어려움
• 구현: Windows IOCP, Boost.Asio, libuv
 Node.js
• 용도: 고성능 서버, 실시간 처리
```

- **병렬 정리**:** 프로액터 패턴은 진정한 비동기를 위해 비동기 작업 완료 시점을 이벤트를 발생시킩니다. 즉, 커널이 직접 작업을 수행하므 리액터보다 성능이 우수하지만 구현이 더 복잡합니다.

 특히 리액터 패턴은 읽기/쓰기 가능 여부를 먼저 확인하고 반면, 프로액터는 실제 완료 여부를 알려줩니다. 따라서 프로액터는 I/O 완료 후 핸들러를 호출하는 반면, 리액터는 데이터가 준비되면 핸들러를 호출합니다.
```
- **비유 설명**:
- 리액터: "웨이터가 테이블을 확인해서 주문을 받습니다"
- 프로액터: "주방에서 음식이 완성되면 호출기가 울립니다"

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 프로액터 패턴은 "음식 호출기" 같아요!

**원리**: 음식이 완성되면 알려줘요!

**효과**: 바로 음식을 받으러 가요!
