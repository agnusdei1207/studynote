+++
title = "535. 그룹화 (Grouping) / 계수 (Counting) 기법"
weight = 535
+++

# 535. Zero-Copy (Zero-copy)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자 공간과 커널 공간 간 데이터 복사 없음
> 2. **가치**: 큰 파일에서 높은 성능, 빠른 복사
> 3. **융합**: mmap, sendfile, DMA와 연관

---

## Ⅰ. 개요

### 개념 정의
**Zero-copy(Zero-copy)**는 **파일을 메모리에 매핑한 때 커널이 사용자 공간에서 직접 복사하는 기술**입니다. I/O 작업 없이 read()/를 직접 수행합니다.

### 💡 비유: 카드 복사
Zero-copy는 **카드 한 장을 복사해서 책상에 다시 놓는 것**과 같습니다. 원본은 그대로 있고 다른 내용이 추가되면 확장됩니다,### Zero-copy 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                Zero-copy 구조                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【기본 작동 방식】                                              │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  1. open()로 파일 열기                                  │ │   │
│  │  2. mmap()으로 매핑 (O_DIRECT)                         │ │   │
│  │  3. memcpy()로 복사                         │ │   │
│  │  4. close()로 매핑 해제                           │ │   │
│  │                                                             │ │   │
│  │  O_DIRECT:                                                  │ │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  프로세스                                               │ │   │
│  │    │                                                     │ │   │
│  │    │  read()                                              │ │   │
│  │    │  write()  ───▶ kernel buffer cache     │   │   │
│  │    └─────────────────────────────────────────────────────────────┘   │
│  │                                                             │ │   │
│  │    │                                                     │ │   │
│  │    ▼                                                     │ │   │
│  │   mmap()                                                  │ │   │
│  │    └─────────────────────────────────────────────────────────────┘   │
│  │                                                             │ │   │
│  │    │                                                     │ │   │
│  │    ▼                                                     │ │   │
│  │   사용자 공간 (직접 접근)                                │ │   │
│  │                                                             │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【성능 비교】                                                 │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  작업              read()/write()         sendfile()               │ │   │
│  │  ────              ──────────                ──────────                │ │   │
│  │  시스템 콜          2회                   1회                     │ │   │
│  │  데이터 복사        커널 → 사용자 공간       사용자 공간 → 커널       │ │   │
│  │  컨텍스트 전환       2회                   0회                     │ │   │
│  │  CPU 사용           높음 (전환 비용)          낮음                    │ │   │
│  │  버퍼 크기           페이지 크기           페이지 크기             │ │   │
│  │  성능              중간                    높음                    │ │   │
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
│                Zero-copy 상세                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【splice() 시스템 콜】                                              │
│  ──────────────────                                                │
│  // 파일의 일부를 다른 위치로 이동 (데이터 복사 없음)                  │
│  ssize_t splice(int fd_in, loff_t off_in,                      │
│                    int fd_out, loff_t off_out, size_t len);           │
│                                                                     │
│  【sendfile() 시스템 콜】                                            │
│  ──────────────────                                                │
│  // 파일 내용을 다른 파일로 복사 (커널 공간에서만 수행)             │
│  ssize_t sendfile(int out_fd, int in_fd, off_t *offset, size_t count);      │
│                                                                     │
│  // Linux에서 sendfile은 버전에 따라 다름                          │
│  ssize_t sendfile(int out_fd, int in_fd, off_t offset, size_t count);      │
│  // 또는                                                │
│  ssize_t copy_file_range(int fd_in, int fd_out,                        │
│                    loff_t off_in, loff_t off_out, size_t len);          │
│                                                                     │
│  【mmap + memcpy vs sendfile】                                       │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  특징                mmap + memcpy          sendfile                    │ │   │
│  │  ────                ──────────                ──────────                  │ │   │
│  │  사용자 공간        사용 (매핑)                미사용                       │ │   │
│  │  시스템 콜          mmap, memcpy         sendfile                    │ │   │
│  │  데이터 복사        2회                      0회                         │ │   │
│  │  CPU 사용           높음                      낮음                        │ │   │
│  │  메모리 사용         높음                      낮음                        │ │   │
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
│  【sendfile 예시】                                                   │
│  ──────────────────                                                │
│  #include <sys/sendfile.h>                                          │
│  #include <fcntl.h>                                                 │
│  #include <unistd.h>                                                │
│                                                                     │
│  int copy_file(const char *src, const char *dst) {                  │
│      int in_fd = open(src, O_RDONLY);                               │
│      if (in_fd < 0) return -1;                                       │
│                                                                     │
│      int out_fd = open(dst, O_WRONLY | O_CREAT | O_TRUNC, 0644);     │
│      if (out_fd < 0) {                                               │
│          close(in_fd);                                               │
│          return -1;                                                  │
│      }                                                               │
│                                                                     │
│      // 파일 크기 획득                                               │
│      off_t offset = 0;                                               │
│      struct stat st;                                                 │
│      fstat(in_fd, &st);                                              │
│                                                                     │
│      // sendfile로 복사                                              │
│      ssize_t sent = sendfile(out_fd, in_fd, &offset, st.st_size);    │
│                                                                     │
│      close(in_fd);                                                   │
│      close(out_fd);                                                  │
│      return (sent == st.st_size) ? 0 : -1;                           │
│  }                                                                   │
│                                                                     │
│  【splice 예시】                                                     │
│  ──────────────────                                                │
│  #include <fcntl.h>                                                 │
│                                                                     │
│  // 파이프를 통한 데이터 전송                                         │
│  void pipe_transfer(int pipe_in, int pipe_out, size_t len) {         │
│      loff_t off_in = 0, off_out = 0;                                 │
│      while (len > 0) {                                               │
│          ssize_t n = splice(pipe_in, &off_in,                        │
│                             pipe_out, &off_out,                      │
│                             len, SPLICE_F_MOVE);                     │
│          if (n <= 0) break;                                          │
│          len -= n;                                                   │
│      }                                                               │
│  }                                                                   │
│                                                                     │
│  【tee 예시 (파이프 복제)】                                          │
│  ──────────────────                                                │
│  // 데이터를 하나의 파이프에서 여러 파이프로 복사                   │
│  ssize_t tee(int fd_in, int fd_out, size_t len, unsigned int flags);│
│                                                                     │
│  // 예: 로깅 시스템에서 원본 데이터를 보존하면서 복사              │
│                                                                     │
│  【vmsplice 예시】                                                   │
│  ──────────────────                                                │
│  // 사용자 공간 데이터를 파이프로 전송                              │
│  ssize_t vmsplice(int fd, const struct iovec *iov,                  │
│                   unsigned long nr_segs, unsigned int flags);         │
│                                                                     │
│  struct iovec iov = {                                               │
│      .iov_base = buffer,                                            │
│      .iov_len = buffer_size                                         │
│  };                                                                 │
│  vmsplice(pipe_fd, &iov, 1, SPLICE_F_GIFT);                          │
│                                                                     │
│  【웹서버에서의 sendfile】                                           │
│  ──────────────────                                                │
│  // 정적 파일 전송                                                   │
│  void send_static_file(int client_fd, int file_fd,                  │
│                         off_t offset, size_t size) {                 │
│      // TCP 소켓으로 파일 직접 전송                                 │
│      sendfile(client_fd, file_fd, &offset, size);                    │
│  }                                                                   │
│                                                                     │
│  // 장점:                                                            │
│  // - 사용자 공간 버퍼 할당 없음                                     │
│  // - CPU 사용 최소화                                                 │
│  // - 높은 처리량                                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 커널 공간에서 직접 데이터 복사
• API: sendfile, splice, tee, vmsplice
• 장점: 사용자 공간 복사 없음, CPU 사용 최소화
• 비교: mmap+memcpy vs sendfile
• sendfile: 파일 → 소켓 직접 전송
• splice: 파이프 간 데이터 이동
• tee: 파이프 데이터 복제
• vmsplice: 사용자 공간 → 파이프
• 용도: 웹서버, 파일 복사, 스트리밍
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [Scatter/Gather I/O](./534_scatter_gather.md) → 벡터화 I/O
- [직접 I/O](./532_direct_io.md) → I/O 방식
- [DMA](./512_dma.md) → 직접 메모리 액세

### 👶 어린이를 위한 3줄 비유 설명
**개념**: Zero-copy는 "택배 직접 배달" 같아요!

**원리**: 중간 창고를 거치지 않아요!

**효과**: 빠르고 효율적이에요!
