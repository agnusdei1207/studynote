+++
title = "21. 신호 (Signal)"
date = 2026-03-06
categories = ["studynotes-operating-system"]
tags = ["Signal", "IPC", "SIGTERM", "SIGKILL", "Signal-Handler", "UNIX-Signal"]
draft = false
+++

# 신호 (Signal)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 신호는 **"프로세스에게 **이벤트나 **예외 상황**을 **비동기적으로 알리는 **소프트웨어 인터럽트"**로, **Kernel**이 **프로세스**에게 **전송**하고 **프로세스**는 **Signal Handler**를 통해 **사용자 정의 동작**을 수행하거나 **Default Action**(**종료, 무시, 코어 덤프**)을 실행한다.
> 2. **가치**: **프로세스 제어**(Process Control)를 위한 **IPC(Inter-Process Communication)** 수단으로 **SIGTERM**(정상 종료), **SIGKILL**(강제 종료), **SIGSTOP**(일시 정지), **SIGCONT**(재개) 같은 **제어 신호**와 **SIGSEGV**(Segmentation Fault), **SIGFPE**(Floating Point Exception) 같은 **예외 신호**로 **오류 처리**에 사용된다.
> 3. **융합**: **UNIX/Linux**의 **Signal**(31~64번), **Windows**의 **Asynchronous Procedure Call(APC)**로 구현되며, **Shell**(Ctrl+C = SIGINT), **Terminal**(SIGHUP = 터미널 종료), **Daemon**(SIGHUP 재시작)과 연계되고 **Python signal**, **Node.js child_process** 등으로 **프로그래밍** 가능하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
신호는 **"커널이 프로세스에게 비동기적으로 전달하는 메시지"**이다.

**신호의 특징**:
- **비동기**: 언제든지 발생 가능
- **간단**: 작은 데이터 전달 (번호만)
- **User/Kernel**: 사용자/커널 정의

### 💡 비유
신호는 **"알림/문자"**와 같다.
- **SIGINT**: 인터럽트 (Ctrl+C)
- **SIGKILL**: 강제 종료
- **SIGSTOP**: 일시 정지

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         신호의 발전                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

초기 UNIX:
    • kill() 시스템 콜
    • 15개 신호만 존재
         ↓
POSIX (1990년대):
    • 표준화
    • Real-time Signal 추가
         ↓
Modern Linux:
    • 64개 신호 (1~64)
    • Queueing, RT Signal
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 표준 신호

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         주요 신호                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Signal    │  Value │  Default Action        │  Description                            │
    │  ─────────────────────────────────────────────────────────────────────────────────────  │
    │  SIGHUP    │  1     │  Terminate            │  터미널 종료 (Daemon 재시작)           │
    │  SIGINT    │  2     │  Terminate            │  인터럽트 (Ctrl+C)                     │
    │  SIGQUIT   │  3     │  Core Dump           │  Quit + Core Dump (Ctrl+\)             │
    │  SIGILL    │  4     │  Core Dump           │  Illegal Instruction                     │
    │  SIGABRT   │  6     │  Core Dump           │  Abort(3) 호출                         │
    │  SIGFPE    │  8     │  Core Dump           │  Floating Point Exception               │
    │  SIGKILL   │  9     │  Terminate (무시)    │  강제 종료 (무시 불가)                │
    │  SIGSEGV   │  11    │  Core Dump           │  Segment Fault (잘못된 메모리 접근)     │
    │  SIGPIPE   │  13    │  Terminate            │  Broken Pipe (읽기 없는 파이프)         │
    │  SIGALRM   │  14    │  Terminate            │  Alarm Clock (setitimer)               │
    │  SIGTERM   │  15    │  Terminate            │  종료 요청 (Graceful Shutdown)          │
    │  SIGUSR1   │  10    │  User-defined         │  사용자 정의 1                         │
    │  SIGUSR2   │  12    │  User-defined         │  사용자 정의 2                         │
    │  SIGCHLD   │  17    │  Ignore              │  자식 상태 변화                         │
    │  SIGCONT   │  18    │  Continue (무시)     │  일시 정지 후 재개                       │
    │  SIGSTOP   │  19    │  Stop (무시)         │  일시 정지                              │
    │  SIGTSTP   │  20    │  Stop                │  터미널 정지 (Ctrl+Z)                    │
    │  SIGTTIN   │  21    │  Ignore              │  Background 읽기 가능                      │
    │  SIGTTOU   │  22    │  Stop                │  Background 쓰기 요청                     │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Signal Handler

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Signal Handler 등록                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  #include <signal.h>                                                                    │
    │  #include <stdio.h>                                                                     │
    │  #include <unistd.h>                                                                    │
    │  #include <stdlib.h>                                                                    │
    │                                                                                         │
    │  // Signal Handler 함수                                                                  │
    │  void sigint_handler(int sig) {                                                           │
    │      printf("Received SIGINT (Ctrl+C)\n");                                             │
    │      printf("Cleaning up...\n");                                                        │
    │      exit(0);                                                                            │
    │  }                                                                                      │
    │                                                                                         │
    │  int main() {                                                                           │
    │      // SIGINT 핸들러 등록                                                               │
    │      signal(SIGINT, sigint_handler);                                                     │
    │                                                                                         │
    │      // 무한 루프                                                                          │
    │      while (1) {                                                                          │
    │          printf("Running...\n");                                                         │
    │          sleep(1);                                                                       │
    │      }                                                                                  │
    │      return 0;                                                                          │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [sigaction (POSIX)]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  #include <signal.h>                                                                    │
    │  #include <stdio.h>                                                                     │
    │  #include <unistd.h>                                                                    │
    │  #include <stdlib.h>                                                                    │
    │                                                                                         │
    │  void handler(int sig) {                                                                │
    │      printf("Received signal %d\n", sig);                                                │
    │  }                                                                                      │
    │                                                                                         │
    │  int main() {                                                                           │
    │      struct sigaction sa;                                                                │
    │                                                                                         │
    │      sa.sa_handler = handler;                                                            │
    │      sigemptyset(&sa.sa_mask);                                                           │
    │      sa.sa_flags = 0;                                                                    │
    │                                                                                         │
    │      // SIGINT, SIGTERM 핸들러 등록                                                        │
    │      sigaction(SIGINT, &sa, NULL);                                                       │
    │      sigaction(SIGTERM, &sa, NULL);                                                      │
    │                                                                                         │
    │      while (1) pause();  // 신호 대기                                                      │
    │      return 0;                                                                          │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Signal 전송

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Signal 전송 방법                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [kill() 시스템 콜]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  #include <signal.h>                                                                    │
    │  #include <unistd.h>                                                                    │
    │  #include <sys/types.h>                                                                │
    │  #include <stdio.h>                                                                     │
    │  #include <stdlib.h>                                                                    │
    │                                                                                         │
    │  int main(int argc, char *argv[]) {                                                      │
    │      if (argc < 2) {                                                                    │
    │          printf("Usage: %s <pid>\n", argv[0]);                                           │
    │          return 1;                                                                      │
    │      }                                                                                  │
    │                                                                                         │
    │      pid_t pid = atoi(argv[1]);                                                          │
    │                                                                                         │
    │      // SIGTERM 전송                                                                     │
    │      if (kill(pid, SIGTERM) == -1) {                                                      │
    │          perror("kill");                                                                │
    │          return 1;                                                                      │
    │      }                                                                                  │
    │                                                                                         │
    │      printf("Sent SIGTERM to process %d\n", pid);                                        │
    │      return 0;                                                                          │
    │  }                                                                                      │
    │                                                                                         │
    │  $ ./send_signal 1234                                                                   │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Shell 명령어]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # 신호 전송                                                                              │
    │  $ kill -SIGTERM 1234       # 또는 kill 15 1234, kill -TERM 1234                              │
    │  $ kill -9 1234              # 강제 종료 (SIGKILL)                                         │
    │  $ kill -l                   # 신호 목록                                                  │
    │  $ kill -STOP 1234           # 일시 정지 (SIGSTOP)                                        │
    │  $ kill -CONT 1234           # 재개 (SIGCONT)                                            │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Signal Mask

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Signal Mask (차단)                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 특정 신호를 일시적으로 블로킹                                                           │
    │  │  • Critical Section 중 Signal 방지                                                          │
    │                                                                                         │
    │  #include <signal.h>                                                                    │
    │  #include <stdio.h>                                                                     │
    │  #include <unistd.h>                                                                    │
    │  #include <stdlib.h>                                                                    │
    │                                                                                         │
    │  int main() {                                                                           │
    │      sigset_t mask;                                                                     │
    │                                                                                         │
    │      // SIGINT, SIGTSTP 블록                                                               │
    │      sigemptyset(&mask);                                                                 │
    │      sigaddset(&mask, SIGINT);                                                           │
    │      sigaddset(&mask, SIGTSTP);                                                          │
    │                                                                                         │
    │      // Signal Mask 설정 (Block)                                                          │
    │      sigprocmask(SIG_BLOCK, &mask, NULL);                                                │
    │                                                                                         │
    │      printf("Critical section: signals blocked\n");                                     │
    │      sleep(5);                                                                           │
    │                                                                                         │
    │      // Signal Mask 해제 (Unblock)                                                        │
    │      sigprocmask(SIG_UNBLOCK, &mask, NULL);                                              │
    │                                                                                         │
    │      printf("Signals unblocked\n");                                                      │
    │      return 0;                                                                          │
    │  }                                                                                      │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### Signal vs Interrupt

| 구분 | Signal | Interrupt |
|------|--------|-----------|
| **발생원** | Software (Kernel/User) | Hardware |
| **비동기** | O | O |
| **우선순위** | 낮음 | 높음 |
| **핸들러** | User-defined | ISR |

### 과목 융합 관점 분석

#### 1. IPC ↔ Signal
- **Notification**: 비동기 알림
- **Synchronization**: SIGCHLD
- **Job Control**: SIGTSTP, SIGCONT

#### 2. Daemon ↔ Signal
- **SIGHUP**: Config Reload
- **SIGTERM**: Graceful Shutdown
- **SIGUSR1/2**: Custom Action

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: Graceful Shutdown
**상황**: 서버 안전 종료
**판단**:

```c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

volatile bool running = true;

void sigterm_handler(int sig) {
    printf("Received SIGTERM, shutting down gracefully...\n");
    running = false;
}

int main() {
    // Signal Handler 등록
    signal(SIGTERM, sigterm_handler);
    signal(SIGINT, sigterm_handler);

    // 서버 루프
    while (running) {
        // Accept new connections
        // Process requests
        pause();  // Signal 대기
    }

    // 자원 정리
    printf("Cleaning up resources...\n");
    // Close connections, Save state

    return 0;
}
```

---

## Ⅴ. 기대효과 및 결론

### Signal 기대 효과

| 효과 | Signal 없을 시 | Signal 있을 시 |
|------|-------------|---------------|
| **프로세스 제어** | Kill만 가능 | Stop/Restart |
| **오류 처리** | Crash 복구 | Core Dump |
| **IPC** | 복잡 | 간단 |

### 미래 전망

1. **signalfd**: Signal을 파일 디스크립터로
2. **eventfd**: Event notification
3. **Timerfd**: 타이머 기반

### ※ 참고 표준/가이드
- **POSIX**: signal, sigaction
- **Linux**: man 7 signal
- **IEEE**: 1003.1

---

## 📌 관련 개념 맵

- [IPC 개요](../5_ipc/93_ipc_overview.md) - 개요
- [파이프](../5_ipc/95_pipe.md) - 다른 IPC
- [공유 메모리](../5_ipc/96_shared_memory.md) - 공유 IPC
- [인터럽트](../4_interrupt/104_interrupt.md) - 하드웨어 인터럽트
