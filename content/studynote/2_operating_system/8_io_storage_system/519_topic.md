+++
title = "519. 디스크 상의 구조 - 부트 제어 블록, 볼륨 제어 블록(슈퍼블록), 디렉터리 구조, FCB(아이노드)"
weight = 519
+++

# 519. I/O 멀티플렉싱 (I/O Multiplexing)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 스레드로 여러 I/O 동시 감시
> 2. **가치**: 높은 동시성과 자원 효율
> 3. **융합**: 논블로킹, 이벤트 루프, 리액터와 연관

---

## Ⅰ. 개요

### 개념 정의

I/O 멀티플렉싱(I/O Multiplexing)은 **단일 스레드에서 여러 파일 디스크립터의 I/O 이벤트를 동시에 감시하는 기술**이다.

### 💡 비유: 여러 전화선 감시
I/O 멀티플렉싱은 **한 사람이 여러 전화선을 동시에 감시하는 것**과 같다. 어떤 전화가 울리는지 확인한다.

### I/O 멀티플렉싱 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                I/O 멀티플렉싱 구조                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 개념】                                                          │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │       파일 디스크립터들                                                   │ │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                       │ │
│  │  │ fd0 │  │ fd1 │  │ fd2 │  │ fd3 │  │ fd4 │                       │ │
│  │  │소켓 │  │파일 │  │파이프│  │소켓 │  │ stdin│                       │ │
│  │  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘                       │ │
│  │     │        │        │        │        │                            │ │
│  │     └────────┴────────┼────────┴────────┘                            │ │
│  │                       │                                             │ │
│  │                       ▼                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────┐    │ │
│  │  │                   I/O 멀티플렉서                              │    │ │
│  │  │                 (select/poll/epoll)                          │    │ │
│  │  │                                                              │    │ │
│  │  │  어떤 fd가 준비되었는지 감시                                    │    │ │
│  │  └─────────────────────────────────────────────────────────────┘    │ │
│  │                       │                                             │ │
│  │                       ▼                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────┐    │ │
│  │  │                   단일 스레드                                 │    │ │
│  │  │  준비된 fd만 처리 → 효율적                                    │    │ │
│  │  └─────────────────────────────────────────────────────────────┘    │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【주요 API 비교】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  API       시스템           최대 FD     성능        특징                   │ │
│  │  ────      ──────           ───────     ────        ────                   │ │
│  │  select    POSIX            1024       O(n)        이식성 좋음              │ │
│  │  poll      POSIX            무제한      O(n)        select 개선             │ │
│  │  epoll     Linux            무제한      O(1)        고성능                  │ │
│  │  kqueue    BSD/macOS        무제한      O(1)        고성능                  │ │
│  │  IOCP      Windows          무제한      O(1)        완료 포트                │ │
│  │  /dev/poll Solaris          무제한      O(1)        고성능                  │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석

### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                I/O 멀티플렉싱 상세                                     │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【select() API】                                                        │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  #include <sys/select.h>                                                │ │
│  │                                                             │ │
│  │  int select(int nfds,                                                   │ │
│  │              fd_set *readfds,                                           │ │
│  │              fd_set *writefds,                                          │ │
│  │              fd_set *exceptfds,                                         │ │
│  │              struct timeval *timeout);                                  │ │
│  │                                                             │ │
│  │  매크로:                                                                 │ │
│  │  FD_ZERO(set)    // 세트 초기화                                          │ │
│  │  FD_SET(fd, set) // fd 추가                                             │ │
│  │  FD_CLR(fd, set) // fd 제거                                             │ │
│  │  FD_ISSET(fd, set) // fd 확인                                           │ │
│  │                                                             │ │
│  │  제한: FD_SETSIZE (보통 1024)                                            │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【epoll API (Linux)】                                                   │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  #include <sys/epoll.h>                                                 │ │
│  │                                                             │ │
│  │  int epoll_create1(int flags);     // 인스턴스 생성                      │ │
│  │  int epoll_ctl(int epfd, int op,   // fd 등록/수정/삭제                  │ │
│  │                  int fd, struct epoll_event *event);                    │ │
│  │  int epoll_wait(int epfd, struct epoll_event *events,                   │ │
│  │                  int maxevents, int timeout);     // 이벤트 대기         │ │
│  │                                                             │ │
│  │  트리거 모드:                                                             │ │
│  │  • Level-triggered (LT): 이벤트가 있으면 계속 알림                        │ │
│  │  • Edge-triggered (ET): 상태 변화 시에만 알림                             │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  【이벤트 루프 패턴】                                                      │
│  ──────────────────                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │  while (running) {                                                       │ │
│  │      // 1. 이벤트 대기                                                    │ │
│  │      n = epoll_wait(epfd, events, MAX_EVENTS, timeout);                  │ │
│  │                                                             │ │
│  │      // 2. 이벤트 처리                                                    │ │
│  │      for (i = 0; i < n; i++) {                                           │ │
│  │          if (events[i].events & EPOLLIN) {                                │ │
│  │              // 읽기 이벤트 처리                                           │ │
│  │              handle_read(events[i].data.fd);                             │ │
│  │          }                                                                │ │
│  │          if (events[i].events & EPOLLOUT) {                              │ │
│  │              // 쓰기 이벤트 처리                                           │ │
│  │              handle_write(events[i].data.fd);                            │ │
│  │          }                                                                │ │
│  │      }                                                                    │ │
│  │                                                             │ │
│  │      // 3. 타이머/기타 작업                                               │ │
│  │      process_timers();                                                   │ │
│  │  }                                                                        │ │
│  │                                                             │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용

### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【select() 예시】                                                        │
│  ──────────────────                                                  │
│  #include <sys/select.h>                                             │
│  #include <stdio.h>                                                  │
│                                                                     │
│  int main() {                                                        │
│      fd_set readfds;                                                 │
│      struct timeval timeout;                                         │
│                                                                     │
│      while (1) {                                                      │
│          FD_ZERO(&readfds);                                          │
│          FD_SET(STDIN_FILENO, &readfds);                             │
│          FD_SET(socket_fd, &readfds);                                │
│                                                                     │
│          timeout.tv_sec = 5;                                         │
│          timeout.tv_usec = 0;                                        │
│                                                                     │
│          int ret = select(maxfd + 1, &readfds, NULL, NULL, &timeout);│
│          if (ret == -1) {                                            │
│              perror("select");                                        │
│              break;                                                   │
│          } else if (ret == 0) {                                      │
│              printf("Timeout\n");                                     │
│              continue;                                                │
│          }                                                             │
│                                                                     │
│          if (FD_ISSET(STDIN_FILENO, &readfds)) {                    │
│              // 표준 입력 처리                                         │
│              char buf[1024];                                          │
│              read(STDIN_FILENO, buf, sizeof(buf));                    │
│          }                                                             │
│          if (FD_ISSET(socket_fd, &readfds)) {                       │
│              // 소켓 처리                                              │
│              recv(socket_fd, buf, sizeof(buf), 0);                   │
│          }                                                             │
│      }                                                               │
│  }                                                                   │
│                                                                     │
│  【epoll 예시 (Linux 고성능)】                                           │
│  ──────────────────                                                  │
│  #include <sys/epoll.h>                                              │
│  #include <fcntl.h>                                                  │
│                                                                     │
│  #define MAX_EVENTS 1024                                              │
│                                                                     │
│  int main() {                                                        │
│      int listen_fd = socket(AF_INET, SOCK_STREAM, 0);                │
│      fcntl(listen_fd, F_SETFL, O_NONBLOCK);                          │
│      bind(listen_fd, ...);                                           │
│      listen(listen_fd, SOMAXCONN);                                   │
│                                                                     │
│      int epfd = epoll_create1(0);                                    │
│                                                                     │
│      struct epoll_event ev;                                          │
│      ev.events = EPOLLIN;                                            │
│      ev.data.fd = listen_fd;                                         │
│      epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);                 │
│                                                                     │
│      struct epoll_event events[MAX_EVENTS];                          │
│                                                                     │
│      while (1) {                                                      │
│          int n = epoll_wait(epfd, events, MAX_EVENTS, -1);           │
│                                                                     │
│          for (int i = 0; i < n; i++) {                               │
│              if (events[i].data.fd == listen_fd) {                   │
│                  // 새 연결 수락                                        │
│                  int client_fd = accept(listen_fd, NULL, NULL);       │
│                  fcntl(client_fd, F_SETFL, O_NONBLOCK);              │
│                                                                     │
│                  ev.events = EPOLLIN | EPOLLET;  // Edge-triggered  │
│                  ev.data.fd = client_fd;                              │
│                  epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &ev);     │
│              } else {                                                 │
│                  // 클라이언트 데이터                                    │
│                  handle_client(events[i].data.fd);                   │
│              }                                                         │
│          }                                                             │
│      }                                                               │
│  }                                                                   │
│                                                                     │
│  【kqueue 예시 (BSD/macOS)】                                             │
│  ──────────────────                                                  │
│  #include <sys/event.h>                                              │
│                                                                     │
│  int kq = kqueue();                                                  │
│  struct kevent change;                                               │
│  struct kevent event;                                                │
│                                                                     │
│  EV_SET(&change, fd, EVFILT_READ, EV_ADD | EV_ENABLE, 0, 0, NULL); │
│                                                                     │
│  while (1) {                                                          │
│      int n = kevent(kq, &change, 1, &event, 1, NULL);               │
│      if (n > 0) {                                                     │
│          if (event.filter == EVFILT_READ) {                          │
│              // 읽기 가능                                              │
│              read(event.ident, buf, sizeof(buf));                    │
│          }                                                             │
│      }                                                               │
│  }                                                                   │
│                                                                     │
│  【성능 비교】                                                            │
│  ──────────────────                                                  │
│  // 연결 10,000개일 때                                                   │
│  select/poll: O(n) → 10,000번 순회                                   │
│  epoll/kqueue: O(1) → 준비된 연결만                                   │
│                                                                     │
│  // 벤치마크 (C10K 문제)                                                │
│  select:  ~1,000 연결까지 양호                                         │
│  poll:    ~10,000 연결까지 양호                                        │
│  epoll:   100,000+ 연결 가능                                          │
│                                                                     │
│  【사용 예시】                                                            │
│  ──────────────────                                                  │
│  // Nginx, Redis, Node.js libuv 모두 epoll/kqueue 사용               │
│                                                                     │
│  // Python selectors                                                  │
│  import selectors                                                    │
│  sel = selectors.DefaultSelector()  # 자동으로 최적 선택               │
│  sel.register(sock, selectors.EVENT_READ, data=None)                 │
│  events = sel.select(timeout=None)                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론

### 핵심 요약

```
• 개념: 단일 스레드로 여러 I/O 동시 감시
• API: select, poll, epoll, kqueue, IOCP
• select: POSIX, 1024 제한, O(n)
• poll: 무제한 FD, O(n)
• epoll/kqueue: O(1), 고성능
• 트리거: Level-triggered vs Edge-triggered
• 패턴: 이벤트 루프
• 용도: 웹서버, 프록시, 채팅 서버
• 사례: Nginx, Redis, Node.js
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [논블로킹 I/O](./518_blocking_nonblocking_io.md) → I/O 모드
- [비동기 I/O](./517_asynchronous_io.md) → 비동기 처리
- [이벤트 루프](./520_event_loop.md) → 처리 패턴

### 👶 어린이를 위한 3줄 비유 설명

**개념**: I/O 멀티플렉싱은 "여러 전화선 감시" 같아요!

**원리**: 어떤 전화가 울리는지 한 번에 봐요!

**효과**: 많은 걸 동시에 처리해요!
