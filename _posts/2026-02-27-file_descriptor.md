---
layout: note
categories: cs_fundamentals-operating_system
original_path: cs_fundamentals/operating_system
title: 파일 디스크립터 (File Descriptor)
date: 2026-02-27
---

# 파일 디스크립터 (File Descriptor)

## 1. 개념

**파일 디스크립터(File Descriptor, FD)**는 유닉스(Unix) 및 유닉스 계열 운영체제에서 **커널이 관리하는 열린 파일(또는 입출력 리소스)을 식별하기 위한 음이 아닌 정수값**이다. 유닉스 철학인 **"모든 것은 파일이다(Everything is a file)"**의 핵심 구현체로, 일반 파일뿐만 아니라 소켓, 파이프, 디바이스 등 모든 입출력 자원을 동일한 방식으로 추상화하여 접근할 수 있게 한다.

```c
// 파일 디스크립터는 단순한 정수값
int fd = open("example.txt", O_RDONLY);  // fd는 3, 4, 5... 등의 정수
```

## 2. 등장 배경

### 2.1 역사적 배경

| 시기 | 사건 | 의미 |
|------|------|------|
| 1969년 | Unix 개발 시작 | PDP-7 하드웨어 추상화 필요 |
| 1970년대 | "Everything is a file" 철학 확립 | 파일 시스템의 통일된 인터페이스 |
| 1983년 | POSIX 표준화 | 이식 가능한 운영체제 인터페이스 |

### 2.2 해결하고자 한 문제

1. **하드웨어 독립성**: 다양한 장치(디스크, 터미널, 프린터 등)를 동일한 방식으로 접근
2. **프로그래밍 단순화**: 파일, 네트워크, 파이프 등에 대해 동일한 `read()`, `write()` API 사용
3. **자원 관리 추상화**: 커널이 모든 입출력 자원을 중앙에서 관리

## 3. 구성 요소

### 3.1 파일 디스크립터 테이블 (File Descriptor Table)

```
┌─────────────────────────────────────────────────────────────┐
│                    프로세스별 자원 구조                       │
├─────────────────────────────────────────────────────────────┤
│  Process A                    Kernel                        │
│  ┌─────────────────┐         ┌─────────────────────────────┐│
│  │ FD Table        │         │ System-wide Open File Table ││
│  │ ┌─────┬───────┐ │         │ ┌─────┬──────────┬────────┐ ││
│  │ │  0  │ stdin │─┼────────┼─┼─│     │ offset   │ mode   │ ││
│  │ ├─────┼───────┤ │         │ │     │ refs     │ vnode  │ ││
│  │ │  1  │ stdout│─┼────────┼─┼─│     │          │        │ ││
│  │ ├─────┼───────┤ │         │ └─────┴──────────┴────────┘ ││
│  │ │  2  │ stderr│─┼────────┼─┼─────────────────────────────┘│
│  │ ├─────┼───────┤ │         │ ┌─────────────────────────────┐│
│  │ │  3  │ file  │─┼────────┼─┼─│ Inode Table (VFS)          ││
│  │ └─────┴───────┘ │         │ │  실제 파일 메타데이터       ││
│  └─────────────────┘         │ └─────────────────────────────┘│
│                              └─────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

### 3.2 표준 파일 디스크립터

| FD | 이름 | C 매크로 | 용도 | 일반적 대상 |
|----|------|----------|------|-------------|
| 0 | 표준 입력 | `STDIN_FILENO` | 프로그램 입력 | 키보드 |
| 1 | 표준 출력 | `STDOUT_FILENO` | 프로그램 출력 | 터미널 |
| 2 | 표준 오류 | `STDERR_FILENO` | 오류 메시지 | 터미널 |

### 3.3 커널 자료구조

```
┌────────────────────────────────────────────────────────────┐
│ 1. File Descriptor Table (per process)                     │
│    - 프로세스마다 독립적                                    │
│    - FD → Open File Descriptor 포인터 매핑                 │
├────────────────────────────────────────────────────────────┤
│ 2. Open File Descriptor Table (system-wide)                │
│    - 열린 파일의 상태 정보                                  │
│    - 파일 오프셋(offset), 접근 모드, 참조 카운트            │
├────────────────────────────────────────────────────────────┤
│ 3. Inode Table / VNode (file system)                       │
│    - 실제 파일의 메타데이터                                 │
│    - 파일 크기, 권한, 디스크 블록 위치                      │
└────────────────────────────────────────────────────────────┘
```

## 4. 핵심 원리

### 4.1 파일 디스크립터 할당 규칙

커널은 **사용 가능한 가장 작은 음이 아닌 정수**를 새 FD로 할당한다.

```
프로세스 시작:  [0:stdin][1:stdout][2:stderr]
open() 호출:    [0:stdin][1:stdout][2:stderr][3:new_file]  ← 3 할당
close(1):       [0:stdin][---free---][2:stderr][3:new_file]
open() 호출:    [0:stdin][1:new_file2][2:stderr][3:new_file] ← 1 재사용
```

### 4.2 파일 오프셋 공유 vs 독립

```
┌─────────────────────────────────────────────────────────────┐
│ Case 1: fork() 후 부모-자식 간 FD 공유                       │
│                                                              │
│ Parent          Open File Table         Child               │
│ ┌───┐          ┌─────────────┐          ┌───┐               │
│ │fd │─┐        │ offset: 100 │        ┌─│fd │               │
│ └───┘ │        │ refs: 2     │        │ └───┘               │
│       └────────►│             │◄───────┘                    │
│                └─────────────┘                              │
│ 같은 파일 오프셋 공유 → 한 쪽이 읽으면 다른 쪽도 offset 변경  │
├─────────────────────────────────────────────────────────────┤
│ Case 2: 독립적인 open() 호출                                 │
│                                                              │
│ Process A                    Process B                      │
│ ┌───┐   ┌─────────────┐     ┌───┐   ┌─────────────┐        │
│ │fd │──►│ offset: 0   │     │fd │──►│ offset: 0   │        │
│ └───┘   │ refs: 1     │     └───┘   │ refs: 1     │        │
│         └─────────────┘             └─────────────┘        │
│ 독립적인 오프셋 → 서로 영향 없음                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 주요 시스템 호출

```c
// 파일 열기/닫기
int open(const char *pathname, int flags, mode_t mode);
int close(int fd);

// 읽기/쓰기
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);

// 위치 이동
off_t lseek(int fd, off_t offset, int whence);

// 복제
int dup(int oldfd);           // 가장 낮은 사용 가능한 FD에 복제
int dup2(int oldfd, int newfd); // 지정된 FD에 복제

// 제어
int fcntl(int fd, int cmd, ... /* arg */ );
int ioctl(int fd, unsigned long request, ...);
```

## 5. 다양한 활용 분야

### 5.1 일반 파일 입출력

```c
int fd = open("/data/log.txt", O_WRONLY | O_CREAT | O_APPEND, 0644);
write(fd, "Log message\n", 12);
close(fd);
```

### 5.2 네트워크 소켓 통신

유닉스에서 **소켓도 파일 디스크립터로 표현**된다.

```c
// TCP 소켓 생성
int server_fd = socket(AF_INET, SOCK_STREAM, 0);

// 바인딩, 리스닝, 수락
bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
listen(server_fd, 5);
int client_fd = accept(server_fd, NULL, NULL);

// 소켓도 read/write 사용 가능
char buffer[1024];
int n = read(client_fd, buffer, sizeof(buffer));
write(client_fd, "HTTP/1.1 200 OK\r\n", 17);
```

```
┌─────────────────────────────────────────────────────────────┐
│              네트워크 통신에서의 FD                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client Process              Server Process                 │
│  ┌──────────┐               ┌──────────┐                    │
│  │ socket() │──fd 3         │ socket() │──fd 3 (listen)    │
│  │ connect()│               │ bind()   │                    │
│  │ write()  │──────────────►│ listen() │                    │
│  │ read()   │◄─────────────│ accept() │──fd 4 (client)    │
│  └──────────┘               │ read()   │                    │
│                             │ write()  │                    │
│                             └──────────┘                    │
│                                                              │
│  소켓 FD도 일반 파일처럼 read/write로 통신                   │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 프로세스 간 통신 (IPC)

#### 5.3.1 파이프 (Pipe)

```c
int pipefd[2];  // pipefd[0]: 읽기용, pipefd[1]: 쓰기용
pipe(pipefd);

// 부모-자식 통신
if (fork() == 0) {
    // 자식: 쓰기만
    close(pipefd[0]);
    write(pipefd[1], "Hello", 5);
} else {
    // 부모: 읽기만
    close(pipefd[1]);
    read(pipefd[0], buf, 5);
}
```

```
┌─────────────────────────────────────────────────────────────┐
│                    파이프 구조                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Process A                     Process B                    │
│  ┌──────────┐                 ┌──────────┐                  │
│  │ pipefd[1]│────write────────►│ pipefd[0]│───read──►       │
│  │ (쓰기용) │    Kernel Buffer │ (읽기용) │                  │
│  └──────────┘   ┌───────────┐ └──────────┘                  │
│                 │ 4KB Buffer│                               │
│                 └───────────┘                               │
│                                                              │
│  단방향 통신: A → B                                          │
└─────────────────────────────────────────────────────────────┘
```

#### 5.3.2 유닉스 도메인 소켓

```c
// 같은 시스템 내 프로세스 간 고속 통신
int fd = socket(AF_UNIX, SOCK_STREAM, 0);
struct sockaddr_un addr;
addr.sun_family = AF_UNIX;
strcpy(addr.sun_path, "/tmp/mysocket");
connect(fd, (struct sockaddr*)&addr, sizeof(addr));
```

### 5.4 장치 파일 (Device File)

```bash
# 하드웨어도 FD로 접근
/dev/null    # 블랙홀 (버림)
/dev/zero    # 무한 0 바이트
/dev/random  # 난수 발생기
/dev/tty     # 제어 터미널
```

```c
// /dev/null 예제: 출력 무시
int devnull = open("/dev/null", O_WRONLY);
dup2(devnull, STDOUT_FILENO);  // stdout을 /dev/null로 리다이렉트
printf("이 메시지는 사라짐\n");
```

### 5.5 이벤트 기반 I/O 멀티플렉싱

대량의 FD를 효율적으로 관리하는 기법들:

```c
// select: 전통적 방식 (FD_SETSIZE 제한)
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(socket_fd, &readfds);
select(max_fd + 1, &readfds, NULL, NULL, NULL);

// poll: select의 개선판
struct pollfd fds[100];
fds[0].fd = socket_fd;
fds[0].events = POLLIN;
poll(fds, 100, -1);

// epoll: 리눅스 고성능 (수만 개 연결 처리 가능)
int epfd = epoll_create1(0);
struct epoll_event ev = {.events = EPOLLIN, .data.fd = socket_fd};
epoll_ctl(epfd, EPOLL_CTL_ADD, socket_fd, &ev);
epoll_wait(epfd, events, MAX_EVENTS, -1);

// kqueue: BSD/macOS 고성능
int kq = kqueue();
struct kevent ev;
EV_SET(&ev, socket_fd, EVFILT_READ, EV_ADD, 0, 0, NULL);
kevent(kq, &ev, 1, NULL, 0, NULL);
```

```
┌─────────────────────────────────────────────────────────────┐
│            I/O 멀티플렉싱 성능 비교                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  연결 수  │   select   │    poll    │   epoll/kqueue        │
│  ─────────┼────────────┼────────────┼────────────────        │
│    100    │    O(100)  │   O(100)   │    O(1)               │
│   1,000   │    O(1000) │   O(1000)  │    O(1)               │
│  10,000   │    O(10000)│   O(10000) │    O(1)               │
│ 100,000   │   제한초과 │   제한초과 │    O(1)               │
│                                                              │
│  C10K Problem → epoll/kqueue로 해결                          │
└─────────────────────────────────────────────────────────────┘
```

### 5.6 리다이렉션과 파이프라인

```bash
# 쉘 리다이렉션 내부 동작
ls > output.txt       # dup2(open("output.txt"), STDOUT_FILENO)
cat < input.txt       # dup2(open("input.txt"), STDIN_FILENO)
ls 2> error.txt       # dup2(open("error.txt"), STDERR_FILENO)

# 파이프라인
ls | grep ".txt"      # pipe() + fork() + dup2()
```

## 6. 장단점

### 6.1 장점

| 장점 | 설명 |
|------|------|
| **통일된 인터페이스** | 파일, 소켓, 파이프, 장치 모두 동일한 API |
| **단순성** | 정수 인덱스로 자원 접근 |
| **이식성** | POSIX 표준, 유닉스 계열 전체 사용 가능 |
| **효율성** | O(1) 접근 (테이블 인덱싱) |
| **상속 용이** | fork() 시 자동 상속 |
| **표준 스트림** | 입출력 리다이렉션, 파이프 구현 용이 |

### 6.2 단점

| 단점 | 설명 | 해결책 |
|------|------|--------|
| **갯수 제한** | 프로세스당 최대 FD 수 제한 | `ulimit -n` 조정 |
| **정수 오용** | 다른 정수와 혼동 가능 | 타입 안전 언어 사용 |
| **보안 이슈** | FD 누출 시 권한 문제 | close-on-exec 플래그 |
| **이식성 제한** | Windows는 핸들(Handle) 사용 | 추상화 레이어 |

### 6.3 제한값 확인 및 조정

```bash
# 현재 제한 확인
ulimit -n              # 소프트 리밋
cat /proc/sys/fs/file-max  # 시스템 전체 최대

# 임시 조정
ulimit -n 65535

# 영구 조정 (/etc/security/limits.conf)
*    soft    nofile    65535
*    hard    nofile    65535
```

## 7. 비교

### 7.1 운영체제별 비교

| 특성 | Unix/Linux (FD) | Windows (Handle) |
|------|-----------------|------------------|
| 식별자 | 음이 아닌 정수 | `HANDLE` (포인터 크기) |
| 철학 | "모든 것은 파일" | "객체 기반" |
| 소켓 | FD 사용 | 별도 `SOCKET` 타입 |
| API | `read()`, `write()` | `ReadFile()`, `WriteFile()` |
| 상속 | 자동 | `SetHandleInformation()` 필요 |

### 7.2 파일 열기 방식 비교

| 방식 | 설명 | 예시 |
|------|------|------|
| **FD (저수준)** | 커널 직접 호출 | `open()`, `read()` |
| **FILE* (고수준)** | 버퍼링 포함 | `fopen()`, `fread()` |
| **C++ 스트림** | 객체 지향 | `ifstream`, `ofstream` |

```c
// 저수준 (FD)
int fd = open("file.txt", O_RDONLY);

// 고수준 (FILE*)
FILE* fp = fopen("file.txt", "r");

// 변환
int fd = fileno(fp);           // FILE* → FD
FILE* fp = fdopen(fd, "r");    // FD → FILE*
```

## 8. 기술사적 판단

### 8.1 설계 관점

1. **추상화의 훌륭한 예**: 하드웨어 차이를 숨기고 통일된 인터페이스 제공
2. **단순함의 힘**: 정수 하나로 모든 자원 관리
3. **조합 가능성(Composability)**: 파이프, 리다이렉션으로 작은 프로그램 조합

### 8.2 현업 적용 사례

| 분야 | 활용 | 주요 기술 |
|------|------|-----------|
| **웹 서버** | 10만+ 동시 연결 | Nginx, epoll |
| **데이터베이스** | 파일 I/O 최적화 | Direct I/O, AIO |
| **컨테이너** | 네트워크 네임스페이스 | Docker, veth |
| **메시지 큐** | 유닉스 소켓 통신 | Unix Domain Socket |

### 8.3 주의사항

```c
// FD 누출 (Leak) 방지
void bad_example() {
    int fd = open("file.txt", O_RDONLY);
    if (error) {
        return;  // FD 누출! close() 누락
    }
    close(fd);
}

void good_example() {
    int fd = open("file.txt", O_RDONLY);
    if (fd < 0) return;

    if (error) {
        close(fd);  // 모든 경로에서 close
        return;
    }
    close(fd);
}
```

## 9. 미래 전망

### 9.1 발전 방향

| 분야 | 현재 | 미래 |
|------|------|------|
| **비동기 I/O** | epoll, kqueue | `io_uring` (리눅스) |
| **성능** | 컨텍스트 스위칭 | 제로카피, 사용자폴트 I/O |
| **보안** | 권한 기반 | FD 격리, Capability |

### 9.2 io_uring: 차세대 비동기 I/O

```c
// 기존: 여러 시스템 콜 필요
read(fd1, buf1, size1);  // 컨텍스트 스위칭
read(fd2, buf2, size2);  // 컨텍스트 스위칭

// io_uring: 한 번의 제출로 여러 I/O 처리
struct io_uring ring;
io_uring_queue_init(256, &ring, 0);

struct io_uring_sqe *sqe;
sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd1, buf1, size1, 0);
sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd2, buf2, size2, 0);
io_uring_submit(&ring);  // 단 한 번의 시스템 콜
```

### 9.3 클라우드 네이티브 환경

- **eBPF**: FD 기반 이벤트와 연동한 네트워크 처리
- **SPDK**: 파일 시스템 우회, 사용자 공간 직접 장치 접근
- **WebAssembly**: WASI (WebAssembly System Interface)에서 FD 모델 채택

---

## 🧒 어린이를 위한 설명

### 비유: 도서관 사물함 번호표

파일 디스크립터는 **도서관 사물함의 번호표**와 같아요!

```
┌─────────────────────────────────────────────────────────────┐
│                    🏫 도서관 비유                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  파일 디스크립터(FD) = 사물함 번호표                         │
│                                                              │
│  ┌─────────────────────────────────────────────┐            │
│  │  사물함 #0  │  📖 stdin   │  입력 책        │            │
│  │  사물함 #1  │  📝 stdout  │  출력 노트      │            │
│  │  사물함 #2  │  ⚠️ stderr  │  오류 공책      │            │
│  │  사물함 #3  │  📄 file    │  내가 연 파일   │            │
│  └─────────────────────────────────────────────┘            │
│                                                              │
│  1. 사물함 번호만 알면 무엇이든 꺼낼 수 있어요               │
│  2. 책, 공책, 편지, 그림... 모두 같은 방법으로!             │
│  3. 다 쓰면 꼭 반납(close)해야 해요                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 재미있는 예시

1. **표준 입력(0) = 친구가 말해주기**
   - 프로그램: "무슨 말인지 들려줘!"
   - 키보드: (입력한 내용)

2. **표준 출력(1) = 칠판에 쓰기**
   - 프로그램: "결과를 칠판에 쓸게!"
   - 화면: (출력된 내용)

3. **파이프(|) = 전화기 연결하기**
   ```
   친구 A ──[말하기]──► 파이프 ──[듣기]──► 친구 B
           "hello.txt 찾아줘"     "찾았어!"
   ```

4. **리다이렉션(>) = 우편함에 넣기**
   ```
   프로그램이 말하는 걸 화면 대신 파일에 저장!
   ```

### 기억하기 쉬운 공식

> **FD는 "만능 리모컨 번호"**
> - 번호만 알면 TV, 에어컨, 오디오 모두 조작 가능
> - FD만 알면 파일, 소켓, 파이프 모두 조작 가능!
