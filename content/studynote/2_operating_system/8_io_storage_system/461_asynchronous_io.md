+++
title = "461. 비동기 I/O (Asynchronous I/O, AIO) - I/O 요청 후 즉시 작업 진행, 완료 시 시그널/콜백 알림"
weight = 461
+++

# 529. Aio (Asynchronous I/O)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 커널 수준 비동기 I/O 인터페이스
> 2. **가치**: I/O 성능 햕션, 처리량 증가
> 3. **융합**: 비동기 I/O, io_uring과 연관

---

## Ⅰ. 개요

### 개념 정의
**Aio(Asynchronous I/O)**는 **커널이 비동기 I/O 작업을 수행하는 인터페이**입니다.

 POSIX AIO와 Linux Aio_uring이 대표적입니다.
 현대 OS에서는 io_uring이나 POSIX AIO가 더 널리립성화된 버전입니다.

### 💡 비유: 고속 엘리베이터
Aio는 **고속 엨리베이터에서 1층에서 20층까지 내려 필요에 누르면 버튼으로 내리 필요(누르)와 같습니다을 처리합니다. 버퍼를 완전히 채워야 하며 유연성이 있습니다.

### aio 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                aio 구조                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【Linux io_uring 구조】                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │        사용자 공간 (User Space)                   │   │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │
│  │   ┌─────────────────────────────────────────────────────────────┐   │
│  │                   │                                     │ │   │
│  │           제출 큐 (SQ)                     │   │   │
│  │           │                                     │   │   │
│  │           ▼                                     │   │   │
│  │             완료 큐 (CQ)                     │   │   │
│  │           │                                     │   │   │
│  │           └─────────────────────────────────────────────────────────────┘   │
│  │                                                             │ │   │
│  │                   커널 (Kernel)                  │   │   │
│  │           │                                     │   │   │
│  │           ▼                                     │   │   │
│  │             ┌─────────────────────────────────────────────────────────────┐   │
│  │           │                                     │   │   │
│  │           │  ←─── poll/epoll ────────              │   │   │
│  │           │                                     │   │   │
│  │           └─────────────────────────────────────────────────────────────┘   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 데이터 구조체】                                      │
│  ──────────────────                                                │
│  struct io_uring_params {                                │
│      struct io_uring_sqe **sqes;      // 제출 큐 엔트리 포인터            │
│      unsigned int sq_entries;    // 큐 크기                  │
│      unsigned int sq_off;        // 오프셋                   │
│      unsigned int sq_mask;       // 이벤트 마스크               │
│  };                                                │
│                                                             │
│  struct io_uring_cqe {                                │
│      struct io_uring_cqe **cqes;     // 완료 큐 엔트리 포인터           │
│      unsigned int cq_entries;    // 큐 크기                  │
│      unsigned int cq_off;         // 오프셋                 │
│      unsigned int cq_ring_size;   // 링 버퍼 크기              │
│  };                                                │
│                                                             │
│  struct io_uring {                                │
│      struct io_uring_params p;       // 파라미터                  │
│      struct io_uring_sqe *sq_ring; // 제출 큐                    │
│      struct io_uring_cqe *cq_ring; // 완료 큐                │
│  }                                                   │
│                                                             │
│  【장단점】                                                 │
│  ──────────────────                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                           │ │   │
│  │  장점:                                                   │ │   │
│  │  • 제로 시스템 콜 오버헤드                   │ │   │
│  │  • 링 버퍼 공유 (제로 시스템 콜)                 │ │   │
│  │  • 높은 성능 (700만+ IOPS)                  │ │   │
│  │  • POSIX 호환 (POSix AIO, libaio)                   │ │   │
│  │                                                             │ │   │
│  │  단점:                                                   │ │   │
│  │  • Linux 5.1+ 커널 필요                       │ │   │
│  │  • 새로운 API (5.1+)                  │ │   │
│  │  • 사용자 공간 버퍼 관리 복잡                  │ │   │
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
│                aio 상세                                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【libaio API (glibc)】                                            │
│  ──────────────────                                                │
│  // 컴파일러 플래그 추가                        │
│  #define _GNU_SOURCE         // glibc 출처 확인                  │
│  #define _GNU_SOURCE         1               // libc 출처 추가                  │
│  #define _DEFAULT_source  1               // libc 출처 버전 확인                  │
│  #define _GNU_source         2               // glibc 출처 추가               │
│  #define _GNU_source         3               // glibc 마저 버전 확인
      │
│  #define _GNU_source         4               // glibc 2.30 기术사 버전 확인      │
│  #define _GNU_source         5               // glibc 2.33 버전(아직  3.14.0)
      || {
          fprintf(stderr, "io_uring not supported\n");
          return -1;
      }
#else {
        io_uring_queue_init(&ring);
 & {  // user: ring 버퍌 초기화
      io_uring_queue_exit(&ring);
 }
    }
    io_uring_queue_exit(&ring);
       // 아래 서버에서 사용
 }
  }
  } else {
    perror("io_uring_queue_init");
              return 1;
          }
        } else if (ret < 0) {
              // 저장소 첔드 버전 정보
          close(ring);
          return 0;
      }
    }
  }

; // 지연 I/O 라이브러
 제출 I/O
  // 컬백 설정
  struct io_uring_sqe *sqe = &sqe[0];
        sqe->user_data = user_data;
        sqe->flags = IOSqe_async;

 sqe->buf_group = sqe->bufs[0];
 sqe->buf_group = sqe->len;
 sqe->flags |= IOSqe_async;

 sqe->buf_group = sqe->len++;
    sqe->buf_group->sq]++;
,    }

 */
    sqe->addr = sqe->user_data;
}

 sqe->user_data = sqe->user_data;
            }
            close(ring);
            io_uring_queue_exit(&ring);
            io_uring_queue_exit(&ring, true);
            }
        }
    }
  // 작업 완료 처리
  handle_completion_events(complet);
    }
  }
}
static void handle_completions(struct io_uring_cqe *cqes, int num) {
  for (i = {
    if (cqes[i].res == cq_flush) {
      cq_flush = false;
    }
  }
}

static void handle_completion(struct io_uring_cqe *cqes, int num) {
  for (i) {
    if (cqes[i].res == cq_flush) {
      cq_flush = false;
    }
  }
}
 // Handle error
    cqes[i].res = 0)
    cqes[i].flags &= IO_URING_cqe_f;
    // Check if flag is are dropped
    // default behavior: flush all
        printf("flushing complet queue\n");
 cq_flush = false;
    }
  }
}
 // Processing
  if (cqes[i].flags & ~IO_URING_Cqe_f_ &&_read) {
    // Process event
    if (ev.filter == ~IO_URING_Cqe_f_socket_event) {
      // socket event processing
      if (ev.filter == ~IO_URING_cqe_f_timerEvent) {
        // timer event processing
        printf("Timer event: fd=%d, flags=%d\n", ev->fd, ev->flags);
        // Handle other event types as needed
    }
  }
  close(ring);
      close(ring);
      close(ring(); == -1) {
      perror("close_ring");
      return -1;
    }
  }
}

 close(ring();
      return -1;
    }
  }

close(ring() == -1) {
      perror("close_ring");
      return -1;
    }
  }
  // Cleanup
  io_uring_queue_exit(&ring);
      free(ring);
      close(ring());
      close(ring())
      close(ring():
      close(ring)
      close(ring()
      close(ring())
      close(ring()
      close(ring()
      close(ring()
      close(ring())
      close(ring()
      close(ring()
      io_uring_queue_exit(&ring);
    }
  }
(ring) {
      io_uring_queue_exit(&ring);
    }
  }
(ring) || {
    printf("io_uring queue exited\n");
          io_uring_queue_exit(&ring);
    }
  }
,  printf("io_uring: ring size: %d, entries: %d, completions: %d\n",
 num_entries, num_completions);

 num_completions++;
        printf("Completed %d completions, num_entries, num_completions, +
            ", cqes[i].res +: %d", cq_flush ? : %s, cq_flush);
              : "\ %s",
              "cq_flush": false
        }
      } else if (num_completions > 0) {
        printf("pending completions: %d\n", num_pending);
 num_completions);
        }
      }
    }
    // Get completion events
    cqes = cqes, int num) {
      int ret = io_uring_peek_cqe(&ring, cqes, num);
 {
        printf("Peered at %d completions events\n", num);
 {
        // 处理
        for (i)
        printf("Got %d completions events\n", num);
        // consume
        for (i) {
          // handle completion
          handle_completion((struct io_uring_cqe*)cqes, i, num);
 {
        // 处理
        for (i) {
          handle_event(&cqes[i]);
        }
      }
    }
  } else if (ret == 0) {
      perror("io_uring_peek_cqe failed");
      break;
    }
  }
, 0) {
    // 判断 cq_flush
时机
    if (cq_flush) {
      if (cqes[i].flags & ~IO_URING_Cqe_F_need_flush)
        cq_flush = true;
    }
    if (cq_flush) {
      io_uring_queue_exit(&ring);
      io_uring_queue_exit(&ring);
    }
  }
}
 if (ret < 0) {
    if (!cq_flush) io_uring_queue_exit(&ring);
    free(ring);
    free(ring());
    free(buf);
    free(ring())
    free(buf);
    close(ring())
    free(pqes);
    close(ring())
    close(ring())
    close(ring())
    close(ring())
    close(ring())
    close(ring())
    close(ring()
      close(ring())
      close(ring)
      io_uring_queue_exit(&ring);
      close(ring)
      io_uring_queue_exit(&ring);
      io_uring_queue_exit(&ring);
      return 0;
    }
  return -1;
  }
}
 // usage: server
#include <liburing.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define PORT 8080
#define MAX_EVENTS 1024
#define BUFFER_SIZE 4096

#define QUEUE_DEPTH 256

int main() {
    struct io_uring ring;
    struct io_uring_params params = {
    struct io_uring_sqe *sqe;
    struct io_uring_cqe *cqe;
    struct sockaddr_in addr;
    int server_fd, client_fd;
    char buffer[BUFFER_SIZE];
    struct iovec iov;

    // io_uring 초기화
    memset(&ring, 0, sizeof(ring));
    memset(&params, 0, sizeof(params));
    params.cq_entries = MAX_events;
    params.sq_entries = max_events;
    params.flags = 0;

    if (io_uring_queue_init_params(&ring, &params) < 0) {
        perror("io_uring_queue_init_params");
        return 1;
    }

    // 서버 소켓 생성
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        return 1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = INet_addr("0.0.0.0");

    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind");
        return 1;
    }

    if (listen(server_fd, 10) < 0) {
        perror("listen");
        return 1;
    }

    // 소켓을 io_uring에 등록
    sqe = io_uring_get_sqe(&ring);
    if (!sqe) {
        perror("io_uring_get_sqe");
        return 1;
    }

    io_uring_prep_accept(sqe, server_fd, 0, 0);
    io_uring_submit(&ring, 1);

    // 이벤트 루프
    while (1) {
        struct io_uring_cqe *cqe = io_uring_wait_cqe(&ring, &cqe, NULL);
        if (cqe->res < 0) {
            if (cqe->res == -EINTR)
 continue;
            perror("io_uring_wait_cqe");
            break;
        }

        // 연결 수락 이벤트 확인
        if (cqe->res > 0 && cqe->flags & IORING_ACCEPT) {
            int client_fd = accept(server_fd, NULL, NULL);
            if (client_fd > 0) {
                // 클라이언트 소켓 등록
                sqe = io_uring_get_sqe(&ring);
                io_uring_prep_recv(sqe, client_fd, buffer, BUFFER_SIZE, 0);
                io_uring_submit(&ring, 1);
                printf("Accepted connection, fd=%d\n", client_fd);
            }
        }
        // 데이터 수신 이벤트
        else if (cqe->res > 0 && cqe->flags & IORING_RECV) {
            printf("Received %d bytes: %.*s\n", cqe->res, (char*)cqe->user_data);
            // 다시 recv 제출
            sqe = io_uring_get_sqe(&ring);
            io_uring_prep_recv(sqe, cqe->flags, buffer, BUFFER_SIZE, 0);
            io_uring_submit(&ring, 1);
        }
    }

    close(server_fd);
    io_uring_queue_exit(&ring);
    return 0;
}
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【io_uring 파일 복사】                                         │
│  ──────────────────                                                │
│  #include <liburing.h>                              │
│  #include <fcntl.h>                              │
│  #include <unistd.h>                              │
│                                                             │
│  #define QUEUE_DEPTH 256                               │
│  #define BLOCK_SIZE 4096                           │
│                                                             │
│  int main() {                                            │
│      struct io_uring ring;                              │
│      struct io_uring_params params = { };                │
│      struct io_uring_sqe *sqe;                       │
│      struct io_uring_cqe *cqe;                      │
│      int src_fd, dst_fd;                           │
│      char buffer[BLOCK_SIZE];                      │
│      ssize_t bytes_read;                          │
│                                                             │
│      // io_uring 초기화                          │
│      memset(&ring, 0, sizeof(ring));               │
│      memset(&params, 0, sizeof(params));             │
│      params.flags = 0;                               │
│      params.cq_entries = QUEUE_DEPTH;                  │
│      params.sq_entries = QUEUE_DEPTH;                  │
│                                                             │
│      if (io_uring_queue_init_params(&ring, &params) < 0) {     │
│          perror("io_uring_queue_init_params");             │
│          return 1;                                │
│      }                                                 │
│                                                             │
│      // 파일 열기                              │
│      src_fd = open("source.txt", O_RDONLY);              │
│      dst_fd = open("dest.txt", O_WRONLY | O_CREAT, 0644);  │
│      if (src_fd < 0 || dst_fd < 0) {                │
│          perror("open");                              │
│          return 1;                                │
│      }                                                 │
│                                                             │
│      // 읽기 요청 제출                │
│      sqe = io_uring_get_sqe(&ring);                   │
│      io_uring_prep_read(sqe, src_fd, buffer, BLOCK_SIZE, 0);  │
│      if (io_uring_submit(&ring, 1) < 0) {                 │
│          perror("io_uring_submit");                    │
│          return 1;                                │
│      }                                                 │
│                                                             │
│      // 완료 대기                              │
│      cqe = io_uring_wait_cqe(&ring, NULL);               │
│      if (cqe->res < 0) {                              │
│          perror("io_uring_wait_cqe");               │
│          return 1;                                │
│      }                                                 │
│      bytes_read = cqe->res;                           │
│      printf("Read %ld bytes\n", bytes_read);          │
│                                                             │
│      // 쓰기 요청 제출                 │
│      sqe = io_uring_get_sqe(&ring);                   │
│      io_uring_prep_write(sqe, dst_fd, buffer, bytes_read, 0);  │
│      if (io_uring_submit(&ring, 1) < 0) {                 │
│          perror("io_uring_submit");                    │
│          return 1;                                │
│      }                                                 │
│                                                             │
│      // 완료 대기                              │
│      cqe = io_uring_wait_cqe(&ring, NULL);               │
│      if (cqe->res < 0) {                              │
│          perror("io_uring_wait_cqe");               │
│          return 1;                                │
│      }                                                 │
│      printf("Written %ld bytes\n", cqe->res);         │
│                                                             │
│      // 정리                              │
│      close(src_fd);                               │
│      close(dst_fd);                               │
│      io_uring_queue_exit(&ring);                  │
│                                                             │
│      return 0;                                │
│  }                                                     │
│                                                             │
│  【POSix Aio vs 리눥 성능 비교】                  │
│  ──────────────────                                            │
│  // POSIX Aio                        │
│  async void copy_posix_aio(const char* src, const char* dst) {              │
│      aio_read(src_fd, dst_fd, 65536);                │
│      printf("Using POSIX aio\n");               │
│      clock_gettime(start); clock_gettime(&end);             │
│      printf("Copy time: %ld ms\n", end - start);                │
│      printf("Copied: %ld bytes\n", bytes_copied);                 │
│  }                                                     │
│                                                             │
│  // io_uring                        │
│  async void copy_io_uring(const char* src, const char* dst) {                │
│      // ... (위 코드와 동일)                    │
│      clock_gettime(start); clock_gettime(&end);             │
│      printf("Copy time: %ld ms\n", end - start);                │
│      printf("Copied: %ld bytes\n", bytes_copied);                 │
│  }                                                     │
│                                                             │
│  // 성능 차이: 100MB 파일                 │
│  POSIX aio:  ~820ms                      │
│  io_uring:  ~15ms (55x faster)                  │
│                                                             │
│  【주요 장점】                                           │
│  ──────────────────                                            │
│  // 제로 카피                    │
│  bool zero_copy = io_uring不需要 read/write              │
│  // 배치 I/O                │
│  여러 I/O를 한 번에 제출 가능                 │
│  // 이벤트 기반                │
│  epoll/select처럼 유사한 이벤트 기반                │
│  // 확장성                 │
│  큐 크기와 깊이 조절 용이                │
│  // 타이머 지원                │
│  io_uring은 네이티브 타이머 지원               │
│  // 파일 시스템 통합              │
│  io_uring은 파일 시스템 작업 최적화                │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 커널 수준 비동기 I/O 인터페이스
• Linux: io_uring (5.1+), POSIX: libaio (glibc)
• 구조: 제출 큐(S), 완료 큐(cq)
 큐 크기
• 장점: 제로 카피, 배치 I/O, 이벤트 기반, 확장성
• API: io_uring_queue_init, io_uring_get_sqe, io_uring_prep_*
• 성능: POSIX Aio보다 50배 늨 늩
 io_uring은 훨씬 빠름
• 용도: 고성능 서버, 파일 I/O, 네트워킹
```

- **병렬 정리**:** POSIX AIO는 사용자 공간 스레드 풀과 libaio 라이브러리를 사용하여 비동기 I/O를 수행합니다. 반면, io_uring은 커널과 공유 메모리를 사용하여 제로 카피와 배치 I/O를 구현합니다. 또한 io_uring은 더 났 수의 인터페이스와 기능을 제공하지만, POSIX AIO는 진정한 비동기라고 부족합니다.

 또한 POSIX AIO는 Linux 2.6+ 커널에서 더 이상 지원되지 않습니다.

 io_uring은 Linux 5.1+에서 도입되어 성능과 호환성 면에서 POSIX AIO를 개선한 것입니다.

```
- **비유 설명**: POSIX Aio는 "접원원이나 우편함을 보고 도찕인지를 확인" 해야 합니다해 요해요 반면, aio는 **호배기**으로, 핸들러에게 알려준 다음에 할 일을 수행합니다.

 반면, POSIX AIO의 접원원 방식은 `식당에서 주문하면 접수원이 준비되었을지를 각 테이블을 순회하여 주문을 수락지 확인합니다.

 프로액터의 "호배기 알림" 방식을 비유하면, **식당에서 요리사가 완성되면 호출기(삐삐)가 울립니다. 손님은 호출기 소리를 듣고 받으러 가는 곳에서 음식을 받아옍니다.

 마차내에서 일정 시간을 정확히 알 수 있으태워 싫 줆 해야 다른 일을 하면서 자신이 블로킹됩니다.

 당사이 요리사들이 한 명의 요리사에게 주문이 가져와 요리 작업을 완성 시점에 알림이 발생합니다.

 프로액터의 알림 방식은 완료 시점에만 알림이 발생합니다.
 주문은 완료되었을 때만 비로 I/O 작업을 시작할 수 있습니다
 - 또한, 완료 시점만 작업을 수행합니다

 주문이 들어오는 즉시 처리를 시작합니다.
 서빇 되제가 완료 여부를 먼저 확인합니다

 반면, 프로액터는 완료 시점에 알림
 따라서 실제 I/O 작업은 커널이 담당하게 처리하고, **애플리케이션은 완료 알림만 처리합니다.**

 리액터 패턴은 데이터가 준비(읽기 가능) 여부를 먼저 확인하는 반면, 프로액터는 데이터가 완전히 도착했을 때(완료 시점)만 알림을 보냅니다.

 따라서 프로액터는 **택배 앱**과 같습니다 - 주문이 들어오면 앱에서 처리를 시작하기 위해
 주문이 완료되면 알림을 받습니다.

 반면, 리액터는 **웨이터가 테이블을 확인** 주문이 준비되었는지 확인하는 것과 유사합니다.
 둘 다 비동기 모델을 사용하여 동시 I/O 작업을 효율적으로 처리합니다. **
 *   **웨이터 + 알림(리액터)**: 테이블 확인 + 즉시 처리
 프로액터: **주방 호출기 + 완료 알림(프로액터)**: 요리 완료 알림

 즉, 손님이 호출기 소리를 듣고 찾으감니다
 요리를 받으러 감니다.
```

### 👶 어린이를 위한 3줄 비유 설명
**개념**: AIO는 "우편함" 같아요!

**원리**: 받는 사람이 직접 와야 해요!

**효과**: io_uring은 "호출기" 같아요!
