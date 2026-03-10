+++
title = "464. io_uring - 최신 리눅스 커널 비동기 I/O 프레임워크 (링 버퍼 기반, 제로 시스템콜 목표)"
weight = 464
+++

# 536. io_uring

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Linux 고성능 비동기 I/O 프레임워크
> 2. **가치**: 시스템 콜 오버헤드 최소화
> 3. **융합**: 비동기 I/O, 링 버퍼, 제로카피와 연관

---

## Ⅰ. 개요

### 개념 정의
**io_uring**은 **Linux 5.1+에서 도입된 고성능 비동기 I/O 프레임워크**입니다. 커널과 사용자 공간 간 링 버퍼를 공유하여 시스템 콜 오버헤드를 최소화합니다.

### 💡 비유: 회전 초밥 벨트
io_uring은 **회전 초밥 벨트**와 같습니다. 접시원이 제출 큐에 주문을 올리고, 완료 큐에서 완료된 주문을 가져갑니다.

### io_uring 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                io_uring 구조                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【핵심 구조】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │   사용자 공간                    커널 공간                         │ │   │
│  │  ┌─────────────────┐         ┌─────────────────┐                 │ │   │
│  │  │  제출 큐 (SQ)      │  ──────▶  │  완료 큐 (CQ)      │                 │ │   │
│  │  │  ┌───┬───┬───┐ │         │  ┌───┬───┬───┐ │                 │ │   │
│  │  │  │SQE│SQE│SQE│ │  ▀─────▶  │  │CQE│CQE│CQE│ │                 │ │   │
│  │  │  └───┴───┴───┘ │  ◀──────  │  └───┴───┴───┘ │                 │ │   │
│  │  │              │  처리    │              │                 │ │   │
│  │  │   tail ▲       │         │   head ▲       │                 │ │   │
│  │  │              │         │              │                 │ │   │
│  │  └─────────────────┘         └─────────────────┘                 │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 구조체】                                                      │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  struct io_uring_params {                                     │ │   │
│  │      __u32 sq_entries;      // SQ 항목 수                        │ │   │
│  │      __u32 cq_entries;      // CQ 항목 수                        │ │   │
│  │      __u32 flags;           // 설정 플래그                        │ │   │
│  │      __u32 sq_thread_cpu;   // 폴링 스레드 CPU                   │ │   │
│  │      __u32 sq_thread_idle;  // 폴링 스레드 idle 시간              │ │   │
│  │      __u32 features;        // 기능 플래그                        │ │   │
│  │      __u32 wq_fd;           // 워커 큐 FD                        │ │   │
│  │      __u32 resv[3];        // 예약                               │ │   │
│  │  };                                                          │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 장점】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • 제로카피: 커널-사용자 공간 데이터 복사 없음                    │ │   │
│  │  • 버퍼링: 다중 I/O 요청 일괄 처리 가능                         │ │   │
│  │  • 유연성: 파일, 소켓, 타이머 등 통합 지원                       │ │   │
│  │  • 확장성: 대규모 동시 연결 처리 가능                            │ │   │
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
│                io_uring 상세                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【주요 시스템 콜】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  io_uring_setup(entries, params)     // io_uring 인스턴스 생성          │ │   │
│  │  io_uring_register(ring, opcode, fd, arg) // 파일/버퍼 등록                │ │   │
│  │  io_uring_enter(ring, flags)          // 제출 및 완료 대기                   │ │   │
│  │  io_uring_wait_cqe(ring, cqe_ptr)     // 완료 이벤트 대기                     │ │   │
│  │  io_uring_peek_cqe(ring, cqe_ptr)     // 완료 이벤트 확인 (비차단)             │ │   │
│  │  io_uring_sqe_set_data(sqe, data)   // SQE 사용자 데이터 설정                │ │   │
│  │  io_uring_cqe_seen(ring, cqe)       // CQE 처리 완료 표시                  │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【liburing 라이브러리 예시】                                           │
│  ──────────────────                                                │
│  #include <liburing.h>                                              │
│  #include <fcntl.h>                                               │
│  #include <unistd.h>                                               │
│                                                                     │
│  int main() {                                                        │
│      struct io_uring ring;                                          │
│      struct io_uring_params params = { };                          │
│                                                                     │
│      // io_uring 초기화                                                │
│      io_uring_queue_init_params(&ring, &params);                           │
│      // 제출 엔트리 획득                                                │
│      struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);                    │
│      io_uring_prep_read(sqe, fd, buffer, size, offset);               │
│      sqe->user_data = buffer;                                           │
│                                                                     │
│      // 제출                                                            │
│      io_uring_submit(&ring);                                         │
│                                                                     │
│      // 완료 대기                                                          │
│      struct io_uring_cqe *cqe;                                         │
│      io_uring_wait_cqe(&ring, &cqe);                               │
│                                                                     │
│      // 결과 확인                                                          │
│      int bytes_read = cqe->res;                               │
│      printf("Read %d bytes\n", bytes_read);                       │
│      io_uring_cqe_seen(&ring, cqe);                                │
│                                                                     │
│      io_uring_queue_exit(&ring);                                     │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  【고급 기능】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  • SQ 폴링: 커널 스레드가 SQ를 폴링                    │ │   │
│  │  • 고정 버퍼: 등록된 버퍼 재사용                       │ │   │
│  │  • 체인: 여러 작업 연결                               │ │   │
│  │  • 타임아웃: 작업 시간 제한 설정                        │ │   │
│  │  • 비동기 버퍼 선택: 버퍼 선택 최적화                  │ │   │
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
│  【고성능 에코 서버 예시】                                            │
│  ──────────────────                                                │
│  #include <liburing.h>                                              │
│  #include <sys/socket.h>                                             │
│  #include <netinet/in.h>                                              │
│                                                                     │
│  #define MAX_CONNECTIONS 1024                                        │
│  #define BUFFER_SIZE 4096                                          │
│                                                                     │
│  int main() {                                                        │
│      struct io_uring ring;                                          │
│      struct io_uring_params params = { .flags = IORING_SETUP_SQPOLL};  │
│                                                                     │
│      io_uring_queue_init_params(&ring, &params);                           │
│                                                                     │
│      int server_fd = socket(AF_INET, SOCK_STREAM, 0);                │
│      // ... bind, listen ...                                  │
│                                                                     │
│      while (1) {                                                      │
│          struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);           │
│          io_uring_prep_accept(sqe, server_fd, client_addr, client_addrlen);  │
│          io_uring_submit(&ring);                                     │
│                                                                     │
│          struct io_uring_cqe *cqe;                                     │
│          io_uring_wait_cqe(&ring, &cqe);                               │
│          // 이벤트 처리...                                         │
│          io_uring_cqe_seen(&ring, cqe);                               │
│      }                                                               │
│  }                                                                   │
│                                                                     │
│  【버퍼 등록 예시】                                                 │
│  ──────────────────                                                │
│  struct iovec iov = {                                              │
│      .iov_base = buffer,                                             │
│      .iov_len = BUFFER_SIZE                                          │
│  };                                                                 │
│  io_uring_register(ring.ring_fd, IORING_REGISTER_BUFFERS, &iov, 1);   │
│                                                                     │
│  【체인 예시: read → write】                                             │
│  ──────────────────                                                │
│  struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);                │
│  io_uring_prep_read(sqe, fd, buf, size, offset);                     │
│  sqe->flags |= IOSQE_IO_LINK;  // 다음 작업과 연결                │
│                                                                     │
│  struct io_uring_sqe *sqe2 = io_uring_get_sqe(&ring);               │
│  io_uring_prep_write(sqe2, fd, buf, size, offset + size);            │
│  io_uring_submit(&ring);  // 한 번에 두 작업 제출                   │
│                                                                     │
│  【타임아웃 설정】                                                  │
│  ──────────────────                                                │
│  struct __kernel_timespec ts = {                                    │
│      .tv_sec = 5,                                                   │
│      .tv_nsec = 0                                                    │
│  };                                                                 │
│  io_uring_prep_timeout(sqe, &ts, 0, IORING_TIMEOUT_ABS);            │
│                                                                     │
│  【지원 확인】                                                        │
│  ──────────────────                                                │
│  // 커널 버전 확인                                              │
│  $ uname -r                                                         │
│  5.15.0                                                             │
│                                                                     │
│  // io_uring 지원 확인                                               │
│  $ cat /proc/sys/kernel/io_uring_disabled                          │
│  0  // 0 = 활성화                                               │
│                                                                     │
│  // liburing 설치                                                │
│  $ sudo apt install liburing-dev                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: Linux 고성능 비동기 I/O 프레임워크
• 구조: 제출 큐(SQ) + 완료 큐(CQ)
• 장점: 제로카피, 버퍼링, 유연성, 확장성
• API: io_uring_setup, io_uring_submit, io_uring_wait_cqe
• 라이브러리: liburing
• 지원: Linux 5.1+
• 기능: SQ 폴링, 고정 버퍼, 체인, 타임아웃
• 용도: 고성능 서버, 스토리지, 네트워킹
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [비동기 I/O](./517_asynchronous_io.md) → 비동기 처리
- [AIO](./529_aio.md) → 비동기 I/O 비교
- [이벤트 루프](./520_event_loop.md) → 이벤트 처리

### 👶 어린이를 위한 3줄 비유 설명
**개념**: io_uring은 "회전 초밥 벨트" 같아요!

**원리**: 주문을 올리고 완성된 것을 가져가요!

**효과**: 매우 빠르고 효율적이에요!
