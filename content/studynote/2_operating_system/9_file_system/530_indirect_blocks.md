+++
title = "530. i-node 단일/이중/삼중 간접 블록 (Indirect Blocks) - 대용량 파일 확장 지원 체계"
weight = 530
+++

# 530. 파일 AIO (File AIO)
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 리눅스 파일 비동기 I/O 인터페이스
> 2. **가치**: 높은 성능의 파일 I/O 작업
> 3. **융합**: AIO, 비동기 I/O, io_uring과 연관

---

## Ⅰ. 개요

### 개념 정의
**파일 AIO(File AIO)**는 **리눅스 커널에서 파일 I/O 작업을 비동기로 수행하기 위한 인터페이스**입니다.

### 💡 비유: 도서관 대출
파일 AIO는 **도서관에서 책을 대출하는 것**과 같습니다. 책을 빌려 달라고 알림을 받으면 찾으러 갈 수 있습니다.

### 파일 AIO 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                파일 AIO 구조                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【AIO vs POSIX AIO】                                           │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  특징                POSIX AIO                Linux File AIO                │ │   │
│  │  ────                ──────────                ──────────────                │ │   │
│  │  구현 방식            사용자 공간             커널 수준                          │ │   │
│  │  스레드                사용자 스레드              커널 스레드                        │ │   │
│  │  이벤트 알림            시그널/폴링               콜백/이벤트 큐                   │ │   │
│  │  성능                중간                     높음                              │ │   │
│  │  복잡도              낮음                      높음                              │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 구조체】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  struct iocb {                                              │ │   │
│  │      __u64 aio_data;         // 사용자 데이터                  │ │   │
│  │      __u32 aio_key;         // 요청 키                            │ │   │
│  │      __u16 aio_lio_opcode;  // 리스트 I/O opcode             │ │   │
│  │      __u16 aio_reqprio;    // 요청 우선순위                    │ │   │
│  │      __u32 aio_fildes;      // 파일 디스크립터                    │ │   │
│  │      __u64 aio_buf;         // 버퍼 주소                        │ │   │
│  │      __u64 aio_nbytes;      // 전송 바이트 수                   │ │   │
│  │      __s64 aio_offset;      // 파일 오프셋                    │ │   │
│  │      ...                                                     │ │   │
│  │  };                                                          │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【작동 방식】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. iocb 구조체 초기화                                       │ │   │
│  │  2. io_submit()으로 요청 제출                                 │ │   │
│  │  3. 커널이 비동기로 작업 수행                                  │ │   │
│  │  4. io_getevents()로 완료 이벤트 수신                          │ │   │
│  │  5. 결과 처리                                                │ │   │
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
│                파일 AIO 상세                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【주요 API】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  함수                  설명                                       │ │   │
│  │  ────                  ────                                       │ │   │
│  │  io_setup()          AIO 컨텍스트 초기화                         │ │   │
│  │  io_destroy()        AIO 컨텍스트 소멸                           │ │   │
│  │  io_submit()         비동기 I/O 요청 제출                       │ │   │
│  │  io_cancel()         비동기 I/O 요청 취소                       │ │   │
│  │  io_getevents()      완료 이벤트 대기                           │ │   │
│  │  io_pgetevents()     시그널과 함께 완료 대기                   │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【io_setup 예시】                                                  │
│  ──────────────────                                                │
│  #include <libaio.h>                                              │
│  #include <fcntl.h>                                                │
│  #include <unistd.h>                                               │
│                                                                     │
│  #define MAX_EVENTS 128                                             │
│                                                                     │
│  int main() {                                                        │
│      io_context_t ctx = 0;                                          │
│      struct iocb cb;                                                │
│      struct iocb *cbs[1] = {&cb};                                  │
│      struct io_event events[MAX_EVENTS];                           │
│                                                                     │
│      // AIO 컨텍스트 초기화                                           │
│      if (io_setup(MAX_EVENTS, &ctx) < 0) {                           │
│          perror("io_setup");                                         │
│          return 1;                                                    │
│      }                                                               │
│                                                                     │
│      // 파일 열기                                                     │
│      int fd = open("test.txt", O_RDONLY);                           │
│      if (fd < 0) {                                                    │
│          perror("open");                                              │
│          io_destroy(ctx);                                            │
│          return 1;                                                    │
│      }                                                               │
│                                                                     │
│      // 버퍼 할당                                                   │
│      char *buffer = malloc(4096);                                   │
│                                                                     │
│      // I/O 요청 준비                                               │
│      io_prep_pread(&cb, fd, buffer, 4096, 0);                       │
│      cb.data = buffer;  // 사용자 데이터                           │
│                                                                     │
│      // 요청 제출                                                     │
│      if (io_submit(ctx, 1, cbs) < 0) {                              │
│          perror("io_submit");                                        │
│          close(fd);                                                  │
│          io_destroy(ctx);                                            │
│          return 1;                                                    │
│      }                                                               │
│                                                                     │
│      // 완료 대기                                                     │
│      int n = io_getevents(ctx, 1, MAX_EVENTS, events, NULL);        │
│      if (n > 0) {                                                    │
│          printf("Read %ld bytes\n", events[0].res);                  │
│      }                                                               │
│                                                                     │
│      // 정리                                                          │
│      free(buffer);                                                   │
│      close(fd);                                                      │
│      io_destroy(ctx);                                                │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  【장단점】                                                           │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  장점:                                                       │ │   │
│  │  • 커널 수준 비동기 I/O                                       │ │   │
│  │  • 높은 성능                                                 │ │   │
│  │  • 다중 I/O 요청 동시 처리                                    │ │   │
│  │  • 이벤트 기반 완료 알림                                      │ │   │
│  │                                                             │ │   │
│  │  단점:                                                       │ │   │
│  │  • libaio 라이브러리 필요                                     │ │   │
│  │  • 복잡한 API                                                 │ │   │
│  │  • O_DIRECT 사용 시 제약                                      │ │   │
│  │  • io_uring으로 대체되는 추세                                  │ │   │
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
│  【libaio 설치】                                                    │
│  ──────────────────                                                │
│  // Ubuntu/Debian                                                 │
│  $ sudo apt-get install libaio-dev                                │
│                                                                     │
│  // CentOS/RHEL                                                    │
│  $ sudo yum install libaio-devel                                  │
│                                                                     │
│  【컴파일】                                                          │
│  ──────────────────                                                │
│  $ gcc -o aio_test aio_test.c -laio                               │
│                                                                     │
│  【다중 요청 예시】                                                  │
│  ──────────────────                                                │
│  #include <libaio.h>                                              │
│  #include <fcntl.h>                                                │
│  #include <stdlib.h>                                               │
│                                                                     │
│  #define NUM_IOS 4                                                 │
│  #define MAX_EVENTS 128                                             │
│                                                                     │
│  int main() {                                                        │
│      io_context_t ctx = 0;                                          │
│      struct iocb cbs[NUM_IOS];                                      │
│      struct iocb *cb_ptrs[NUM_IOS];                                 │
│      struct io_event events[MAX_EVENTS];                           │
│                                                                     │
│      io_setup(MAX_EVENTS, &ctx);                                    │
│                                                                     │
│      // 여러 파일 열기                                              │
│      int fds[NUM_IOS];                                              │
│      char *buffers[NUM_IOS];                                        │
│                                                                     │
│      for (int i = 0; i < NUM_IOS; i++) {                            │
│          char filename[32];                                          │
│          sprintf(filename, "file%d.txt", i);                        │
│          fds[i] = open(filename, O_RDONLY | O_DIRECT);             │
│          posix_memalign(&buffers[i], 512, 4096);                   │
│          cb_ptrs[i] = &cbs[i];                                      │
│          io_prep_pread(&cbs[i], fds[i], buffers[i], 4096, 0);       │
│      }                                                               │
│                                                                     │
│      // 모든 요청 동시 제출                                          │
│      io_submit(ctx, NUM_IOS, cb_ptrs);                              │
│                                                                     │
│      // 완료 대기                                                     │
│      int completed = 0;                                              │
│      while (completed < NUM_IOS) {                                   │
│          int n = io_getevents(ctx, 1, MAX_EVENTS, events, NULL);    │
│          for (int i = 0; i < n; i++) {                              │
│              printf("IO %ld: read %ld bytes\n",                       │
│                     events[i].obj - (long)cbs,                        │
│                     events[i].res);                                  │
│              completed++;                                            │
│          }                                                             │
│      }                                                               │
│                                                                     │
│      // 정리                                                          │
│      for (int i = 0; i < NUM_IOS; i++) {                            │
│          close(fds[i]);                                              │
│          free(buffers[i]);                                           │
│      }                                                               │
│      io_destroy(ctx);                                                │
│      return 0;                                                        │
│  }                                                                   │
│                                                                     │
│  【O_DIRECT 요구사항】                                               │
│  ──────────────────                                                │
│  // 버퍼 정렬 필요                                                   │
│  void *buffer;                                                      │
│  posix_memalign(&buffer, 512, 4096);  // 512바이트 정렬              │
│                                                                     │
│  // 또는                                                           │
│  void *buffer = aligned_alloc(512, 4096);                           │
│                                                                     │
│  【성능 비교】                                                        │
│  ──────────────────                                                │
│  // 동기 읽기                                                        │
│  for (int i = 0; i < 1000; i++) {                                    │
│      read(fd, buf, size);  // 매번 대기                            │
│  }                                                               │
│  // File AIO                                                        │
│  io_submit(ctx, 1000, cbs);  // 모두 비동기로 제출                │
│  io_getevents(ctx, 1000, ...);  // 완료 대기                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 리눅스 커널 파일 비동기 I/O
• API: io_setup, io_submit, io_getevents, io_destroy
• 구조: iocb, io_event, io_context_t
• 비교: POSIX AIO (사용자 공간) vs File AIO (커널)
• 장점: 커널 수준, 높은 성능, 다중 요청
• 단점: libaio 필요, O_DIRECT 제약, 복잡한 API
• 대체: io_uring으로 대체 추세
• 요구: 버퍼 정렬 (512바이트)
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [비동기 I/O](./517_asynchronous_io.md) → 비동기 처리
- [io_uring](./529_aio.md) → 차세대 비동기 I/O
- [POSIX AIO](./517_asynchronous_io.md) → 표준 비동기 I/O

### 👶 어린이를 위한 3줄 비유 설명
**개념**: 파일 AIO는 "도서관 대출" 같아요!

**원리**: 빌리고 나중에 알림을 받아요!

**효과**: 다른 일을 하면서 기다릴 수 있어요!
