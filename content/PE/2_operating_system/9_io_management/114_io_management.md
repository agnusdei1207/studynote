+++
title = "47. I/O 관리 (I/O Management)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["I/O-Management", "Polling", "Interrupt", "DMA", "Device-Driver"]
draft = false
+++

# I/O 관리 (I/O Management)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: I/O 관리는 **"CPU와 **장치** 간 **데이터 **전송**을 **제어**하는 **기법\"**으로, **Polling**(CPU **주도), **Interrupt**(장치 **주도), **DMA**(Direct Memory Access, **장치** ↔ **메모리 **직접 **전송)**으로 **구현**된다.
> 2. **구조**: **Device Controller**가 **장치**를 **제어**하고 **Device Driver**(Kernel **모듈)**가 **Controller**와 **통신**하며 **VFS**(Virtual File System)가 **파일 **시스템 **추상화**를 **제공**한다.
> 3. **기법**: **Buffering**(데이터 **버퍼링)**, **Caching**(자주 **접근 **데이터 **캐싱)**, **Spooling**(인쇄 **대기열)**으로 **성능**을 **향상**하고 **Asynchronous I/O**(비동기 **입출력)**로 **CPU **활용**을 **최적화**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
I/O 관리는 **"입출력 장치 제어"**이다.

**I/O 장치 유형**:
| 유형 | 속도 | 예시 | 특징 |
|------|------|------|------|
| **Block** | 중간 | SSD, HDD | 블록 단위 |
| **Character** | 느림 | 키보드, 시리얼 | 스트림 |
| **Network** | 빠름 | NIC | 패킷 |
| **Graphics** | 빠름 | GPU | 프레임 |

### 💡 비유
I/O 관리는 ****사무 **실무 ****와 같다.
- **직원**: CPU
- **고객**: I/O 장치
- **대기**: Interrupt

---

## Ⅱ. 아키텍처 및 핵심 원리

### I/O 시스템 구조

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         I/O System Architecture                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Application                                                                            │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  write(fd, buffer, size)                                                            │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │            │                                                                             │  │
    │            ▼ System Call                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  Kernel (I/O Subsystem)                                                              │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  • Scheduling: Queue I/O requests                                                 │  │  │  │
    │  │  │  • Buffering: Manage I/O buffers                                                  │  │  │  │
    │  │  │  • Caching: Cache frequently accessed data                                        │  │  │  │
    │  │  │  • Spooling: Device allocation (e.g., printer spooler)                             │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │            │                                                                             │  │  │
    │  │            ▼                                                                             │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Device-Independent I/O Software                                                   │  │  │  │
    │  │  │  • Uniform interface for all devices                                               │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │            │                                                                             │  │  │
    │  │            ▼                                                                             │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Device Drivers (Device-Specific)                                                  │  │  │  │
    │  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │  │  │
    │  │  │  │ Disk Driver  │  │ NIC Driver   │  │ TTY Driver   │  │ GPU Driver   │           │  │  │
    │  │  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘           │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  │            │                                                                             │  │  │
    │  │            ▼ Device Controller Interface (PCIe, USB, SATA)                              │  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────────┐  │  │  │
    │  │  │  Device Controllers                                                                  │  │  │  │
    │  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │  │  │  │
    │  │  │  │ Disk Ctrl    │  │ NIC Ctrl     │  │ USB Ctrl     │  │ GPU Ctrl     │           │  │  │  │
    │  │  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘           │  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### I/O 제어 방식

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         I/O Control Methods                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    1. Programmed I/O (Polling):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // CPU continuously checks device status                                               │  │
    │  while (device.status != READY) {   // Busy waiting                                      │  │
    │      // CPU wasted                                                                      │  │
    │  }                                                                                       │  │
    │  data = device.data;                                                                    │  │
    │                                                                                         │  │
    │  • Simple but CPU-intensive                                                              │  │
    │  • CPU利用率低 ( wastes cycles in polling loop)                                          │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    2. Interrupt-Driven I/O:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // CPU issues command and continues other work                                         │  │
    │  device.command = READ;                                                                 │  │
    │  scheduler_switch();         // CPU switches to other process                             │  │
    │                                                                                         │  │
    │  // Device triggers interrupt when ready                                                │  │
    │  ISR (Interrupt Service Routine):                                                       │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  1. Save context                                                                     │  │  │
    │  │  2. Acknowledge interrupt                                                            │  │  │
    │  │  3. Read data from device                                                            │  │  │
    │  │  4. Wake up waiting process                                                          │  │  │
    │  │  5. Restore context                                                                  │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  • CPU efficient but interrupt overhead per byte (for large transfers)                   │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    3. Direct Memory Access (DMA):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // CPU sets up DMA transfer and continues                                              │  │
    │  DMA_reg.src = device_buffer;   // Device address                                       │  │
    │  DMA_reg.dst = memory_buffer;   // Memory address                                       │  │
    │  DMA_reg.count = 4096;          // Bytes to transfer                                    │  │
    │  DMA_reg.cmd = START;                                                                  │  │
    │                                                                                         │  │
    │  // DMA controller transfers data directly                                              │  │
    │  // Only interrupt when transfer complete                                               │  │
    │                                                                                         │  │
    │  ISR on completion:                                                                     │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  • Check DMA status                                                                  │  │  │
    │  │  • Wake up waiting process                                                           │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  • Best for large transfers (disk, network)                                             │  │
    │  • CPU free during transfer                                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### DMA 작동 원리

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         DMA Transfer Process                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  CPU                        DMA Controller              Disk Controller                   │  │
    │  ┌───────────────────────────┐ ┌──────────────────────────────────────────────────────────┐  │  │
    │  │  1. Program DMA           │ │                                                          │  │  │
    │  │     DMA_reg.src = device  │ │                                                          │  │  │
    │  │     DMA_reg.dst = memory  │ │                                                          │  │  │
    │  │     DMA_reg.count = N     │ │                                                          │  │  │
    │  │     DMA_reg.cmd = START   │ │                                                          │  │  │
    │  └───────────────────────────┘ │                                                          │  │  │
    │            │                  │  2. Arbitrate bus (request from DMA)                       │  │  │
    │            │                  │  3. Transfer data from disk to memory                     │  │  │
    │            │                  │     ┌──────────────────────────────────────────────────────┐ │  │  │
    │            │                  │     │  Each cycle:                                       │ │  │  │
    │            │                  │     │  • Read from disk (Disk → DMA)                     │ │  │  │
    │            │                  │     │  • Write to memory (DMA → Memory)                   │ │  │  │
    │            │                  │     │  • Decrement count, increment addresses             │ │  │  │
    │            │                  │     └──────────────────────────────────────────────────────┘ │  │  │
    │            │                  │  4. Repeat until count = 0                                │  │  │
    │            │                  │  5. Trigger interrupt to CPU                              │  │  │
    │  ┌───────────────────────────┐ │                                                          │  │  │
    │  │  6. ISR: Wake up process  │ │                                                          │  │  │
    │  └───────────────────────────┘ │                                                          │  │  │
    │                            └──────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### I/O 기법 비교

| 기법 | CPU 활용 | 전송 단위 | 복잡도 | 사용처 |
|------|----------|----------|--------|--------|
| **Polling** | 낮음 | 1 바이트 | 낮음 | 단순 장치 |
| **Interrupt** | 중간 | 가변 | 중간 | 키보드, 마우스 |
| **DMA** | 높음 | 대량 | 높음 | 디스크, 네트워크 |

### Buffering vs Caching

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Buffering vs Caching                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Buffering (Stream-oriented):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Purpose: Smooth rate mismatch between producer and consumer                            │  │
    │                                                                                         │  │
    │  Example: Keyboard input                                                                │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  User types: "hello" (1 char/10ms)                                                   │  │  │
    │  │  Buffer: [h][e][l][l][o] (accumulates in kernel buffer)                               │  │  │
    │  │  App reads: fgets(buffer) - entire line at once                                      │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Types:                                                                                 │  │
    │  • Single buffer: one buffer, double buffering possible                                 │  │
    │  • Circular buffer: FIFO queue for streaming                                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Caching (Block-oriented):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Purpose: Reduce disk access by storing frequently used blocks                           │  │
    │                                                                                         │  │
    │  Example: Disk cache                                                                    │  │
    │  ┌──────────────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  App requests: Block 1000                                                            │  │  │
    │  │  Cache miss: Read from disk → Store in cache                                        │  │  │
    │  │  App requests: Block 1000 again                                                      │  │  │
    │  │  Cache hit: Return from cache (no disk access)                                       │  │  │
    │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
    │                                                                                         │  │
    │  Algorithms:                                                                            │  │
    │  • LRU: Least Recently Used                                                             │  │
    │  • LFU: Least Frequently Used                                                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Asynchronous I/O

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Synchronous vs Asynchronous I/O                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Synchronous (Blocking):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Application blocks until I/O completes                                              │  │
    │  n = read(fd, buffer, size);   // Blocks here                                          │  │
    │  process(buffer, n);                                                                     │  │
    │                                                                                         │  │
    │  • Simple programming model                                                             │  │
    │  • Poor concurrency (one I/O at a time)                                                 │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Asynchronous (Non-blocking):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Application continues while I/O in progress                                         │  │
    │  aio_read(&request);           // Submit I/O request                                    │  │
    │                                                                                         │  │
    │  // Do other work while I/O completes                                                   │  │
    │  do_other_work();                                                                        │  │
    │                                                                                         │  │
    │  // Check or wait for completion                                                        │  │
    │  aio_suspend(&request);        // Blocks until I/O complete                              │  │
    │  process(request.buffer, request.return_size);                                          │  │
    │                                                                                         │  │
    │  • Better concurrency                                                                   │  │
    │  • Complex programming (callbacks, promises)                                             │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Event-Driven (epoll/kqueue):
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  // Monitor multiple file descriptors                                                    │  │
    │  epfd = epoll_create1(0);                                                                │  │
    │  epoll_ctl(epfd, EPOLL_CTL_ADD, fd1, &event);                                           │  │
    │  epoll_ctl(epfd, EPOLL_CTL_ADD, fd2, &event);                                           │  │
    │                                                                                         │  │
    │  while (1) {                                                                             │  │
    │      nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);  // Block until event              │  │
    │      for (i = 0; i < nfds; i++) {                                                       │  │
    │          if (events[i].events & EPOLLIN) {                                              │  │
    │              n = read(events[i].data.fd, buffer, size);                                  │  │
    │              process(buffer, n);                                                         │  │
    │          }                                                                                │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  • Single thread handles many connections                                                │  │
    │  • Used in high-performance servers (Nginx, Node.js)                                      │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: 고성능 웹 서버 I/O
**상황**: 10만 동시 연결
**판단**: epoll + Non-blocking I/O + Edge-triggered

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         High-Performance Web Server I/O                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Requirements:
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 100,000 concurrent connections                                                        │  │
    │  • Low latency (< 10ms)                                                                  │  │
    │  • High throughput (> 10 Gbps)                                                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    Solution: Event-Driven Architecture (epoll)
    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  int epfd = epoll_create1(0);                                                            │  │
    │  struct epoll_event ev;                                                                  │  │
    │                                                                                         │  │
    │  // Set socket to non-blocking mode                                                      │  │
    │  fcntl(listen_fd, F_SETFL, O_NONBLOCK);                                                  │  │
    │                                                                                         │  │
    │  // Add listening socket to epoll (edge-triggered)                                       │  │
    │  ev.events = EPOLLIN | EPOLLET;    // Edge-triggered                                     │  │
    │  ev.data.fd = listen_fd;                                                                 │  │
    │  epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);                                         │  │
    │                                                                                         │  │
    │  while (1) {                                                                             │  │
    │      int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);                                │  │
    │                                                                                         │  │
    │      for (int i = 0; i < nfds; i++) {                                                   │  │
    │          if (events[i].data.fd == listen_fd) {                                           │  │
    │              // Accept new connections                                                   │  │
    │              while ((conn_fd = accept(listen_fd, ...)) > 0) {                            │  │
    │                  fcntl(conn_fd, F_SETFL, O_NONBLOCK);                                    │  │
    │                  ev.events = EPOLLIN | EPOLLOUT | EPOLLET;                               │  │
    │                  ev.data.fd = conn_fd;                                                   │  │
    │                  epoll_ctl(epfd, EPOLL_CTL_ADD, conn_fd, &ev);                            │  │
    │              }                                                                            │  │
    │          } else {                                                                        │  │
    │              // Handle existing connection                                               │  │
    │              conn_fd = events[i].data.fd;                                                │  │
    │                                                                                         │  │
    │              if (events[i].events & EPOLLIN) {                                           │  │
    │                  // Read until EAGAIN (edge-triggered)                                    │  │
    │                  while ((n = read(conn_fd, buffer, size)) > 0) {                          │  │
    │                      process_request(buffer, n);                                         │  │
    │                  }                                                                        │  │
    │              }                                                                            │  │
    │                                                                                         │  │
    │              if (events[i].events & EPOLLOUT) {                                          │  │
    │                  // Write response                                                       │  │
    │                  write(conn_fd, response, response_len);                                  │  │
    │              }                                                                            │  │
    │          }                                                                                │  │
    │      }                                                                                    │  │
    │  }                                                                                       │  │
    │                                                                                         │  │
    │  → Single thread handles 100K connections                                               │  │
    │  → No context switch overhead                                                            │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅴ. 기대효과 및 결론

### I/O 관리 기대 효과

| 기법 | CPU 효율 | 처리량 | 복잡도 |
|------|----------|--------|--------|
| **Polling** | 낮음 | 낮음 | 낮음 |
| **Interrupt** | 중간 | 중간 | 중간 |
| **DMA** | 높음 | 높음 | 높음 |
| **Async** | 최고 | 최고 | 최고 |

### 모범 사례

1. **대용량**: DMA 사용
2. **대기열**: Spooling
3. **캐싱**: Page cache
4. **이벤트**: epoll/kqueue

### 미래 전망

1. **NVMe**: PCIe 직접 접근
2. **SPDK**: Userspace I/O
3. **RDMA**: 원격 DMA
4. **CXL**: 메모리 일관성 I/O

### ※ 참고 표준/가이드
- **POSIX**: I/O System Calls
- **Linux**: IO_uring
- **Windows**: IOCP

---

## 📌 관련 개념 맵

- [파일 시스템](./8_file_system/113_file_system.md) - VFS
- [인터럽트](./1_os_overview/16_interrupt.md) - ISR
- [DMA](../../1_computer_architecture/6_bus/88_bus.md) - 버스 마스터링

