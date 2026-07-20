---
title: "Proactor Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 213
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Proactor (프로액터) 패턴은 I/O 완료(Completion) 이벤트를 기반으로 OS가 I/O를 대신 수행하고, 완료 후 Completion Handler (완료 핸들러)를 호출하는 비동기 I/O 아키텍처 패턴이다.
> 2. **가치**: CPU 스레드가 I/O 대기 없이 다른 작업을 계속 처리할 수 있어 고성능 네트워크 서버에서 극단적인 처리량(Throughput)을 달성한다.
> 3. **판단 포인트**: Reactor (리액터)는 "I/O 준비됨(Readiness)" 신호를 받아 앱이 직접 I/O를 수행하지만, Proactor는 "I/O 완료(Completion)" 신호를 받아 결과 데이터를 바로 처리한다 — OS가 I/O를 대리 수행하느냐의 차이가 핵심이다.

---

## Ⅰ. 개요 및 필요성
전통적인 동기 서버에서는 클라이언트 요청 1개당 스레드 1개를 할당한다. 연결이 1만 개라면 1만 개의 스레드가 필요하고, 대부분은 I/O를 기다리며 블록(Block)된 채 CPU를 낭비한다. 이를 C10K 문제(C10K Problem, 동시 10,000 클라이언트 처리 문제)라고 부른다.

해결책의 진화 경로:

```
동기 블로킹(Sync Blocking)
  +-> 멀티스레드(Multi-Thread) 동기 — 스레드 폭발 문제
       +-> 이벤트 루프 + Reactor — 준비 이벤트, 앱이 I/O 수행
            +-> Proactor — 완료 이벤트, OS가 I/O 수행
```

Proactor 패턴의 핵심 동기:
- <strong>스레드 절감</strong>: 소수의 스레드(Thread Pool)로 수천~수만 연결 처리
- **CPU 효율**: 스레드가 I/O 대기 없이 Completion Handler 실행에만 집중
- **OS 위임**: Windows IOCP (I/O Completion Port, 입출력 완료 포트), Linux `io_uring` 등 OS 레벨 비동기 I/O 활용

| 관점 | Reactor (리액터) | Proactor (프로액터) |
|:---|:---|:---|
| 이벤트 시점 | I/O 준비(Readiness) | I/O 완료(Completion) |
| I/O 수행 주체 | 애플리케이션(App) | OS 커널(Kernel) |
| 버퍼 제공 시점 | 이벤트 수신 후 직접 호출 | 비동기 요청 시 미리 제공 |
| 대표 구현 | `epoll`, `select`, `kqueue` | Windows IOCP, `io_uring` |
| 복잡도 | 상대적으로 단순 | 비교적 복잡(버퍼 수명 관리) |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: Reactor는 "손님이 도착하면 알려줘, 내가 문을 열게(readiness)" 이고 Proactor는 "손님을 안으로 모시고 자리까지 안내한 다음 나한테 알려줘(completion)" 다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 참여자 | 역할 |
|:---|:---|
| Initiator (이니시에이터) | 비동기 I/O 요청을 시작하고 Completion Handler를 등록 |
| Asynchronous Operation (비동기 오퍼레이션) | OS가 수행할 실제 I/O 작업 (read/write) |
| Async Op Processor (비동기 오퍼레이션 프로세서) | OS 커널 — I/O를 실제로 수행 |
| Completion Event Queue (완료 이벤트 큐) | OS가 완료된 I/O 결과를 쌓아두는 큐 (IOCP 큐) |
| Proactor (프로액터) | 완료 큐에서 이벤트를 꺼내 Completion Handler에 디스패치 |
| Completion Handler (완료 핸들러) | 비즈니스 로직 수행 (읽은 데이터 처리 등) |

```
+--------------------------------------------------------------+
|                        Proactor Pattern                      |
|                                                              |
|  +--------------+   1. 비동기 I/O 요청 + Handler 등록        |
|  |  Initiator   |-------------------------------------+     |
|  +--------------+                                     |     |
|                                                       v     |
|  +--------------------------------------------------------+  |
|  |              OS Kernel (비동기 오퍼레이션 프로세서)       |  |
|  |   2. 실제 I/O 수행 (디스크 읽기, 네트워크 수신 등)        |  |
|  +-----------------------+--------------------------------+  |
|                          | 3. I/O 완료 -> 결과를 큐에 삽입     |
|                          v                                   |
|  +---------------------------------------------------------+ |
|  |          Completion Event Queue (완료 이벤트 큐)          | |
|  |   [결과 데이터 A] [결과 데이터 B] [결과 데이터 C] ...      | |
|  +-----------------------+---------------------------------+ |
|                          | 4. 이벤트 디큐(Dequeue)            |
|                          v                                   |
|  +--------------+   5. Handler 호출   +------------------+   |
|  |   Proactor   |--------------------->| Completion       |   |
|  | (이벤트 루프) |                     | Handler          |   |
|  +--------------+                     | (비즈니스 로직)   |   |
|                                       +------------------+   |
+--------------------------------------------------------------+
```

```
CreateIoCompletionPort()   <- IOCP 생성 및 소켓 연결
       |
WSARecv(overlapped)        <- 비동기 수신 시작 (버퍼를 OS에 미리 제공)
       |
       +-> [OS가 비동기로 TCP 수신 수행]
              |
       GetQueuedCompletionStatus()  <- 스레드 풀 워커가 완료 대기
              |
       완료 이벤트 수신 -> 수신된 데이터로 비즈니스 로직 처리
```

```cpp
// 비동기 읽기 시작 (Initiator 역할)
socket.async_read_some(
    asio::buffer(buf),
     {   // Completion Handler
        if (!ec) process(buf, bytes);
    }
);
// io_context.run() -> Proactor 역할 (완료 이벤트 디스패치)
```

- **📢 섹션 요약 비유**: 음식 배달 앱에서 주문 후 내가 직접 음식을 가지러 가면 Reactor, 배달원이 문 앞까지 갖다주고 "배달 완료" 알림을 보내면 Proactor다.

---

## Ⅲ. 비교 및 연결
| I/O 모델 | 블로킹 여부 | I/O 수행 주체 | 알림 시점 | 대표 OS API |
|:---|:---|:---|:---|:---|
| Blocking I/O | 블로킹 | 앱 | I/O 완료 후 | `read()`, `recv()` |
| Non-Blocking I/O | 논블로킹 | 앱 | 즉시 반환 (EAGAIN) | `fcntl(O_NONBLOCK)` |
| I/O Multiplexing (Reactor) | 준(準)블로킹 | 앱 | I/O 준비 시 | `epoll`, `select` |
| Signal-Driven I/O | 논블로킹 | 앱 | I/O 준비 시 (시그널) | `SIGIO` |
| **Async I/O (Proactor)** | **논블로킹** | **OS** | **I/O 완료 시** | <strong>IOCP, <code>io_uring</code></strong> |

| 패턴 | 관계 | 설명 |
|:---|:---|:---|
| Reactor | 대비 | 준비 이벤트 기반, 앱이 I/O 수행 |
| Half-Sync/Half-Async | 조합 | 비동기 수신 계층 + 동기 처리 계층 |
| Thread Pool | 조합 | Completion Handler 실행을 스레드 풀에 위임 |
| Command | 활용 | Completion Handler를 Command 객체로 캡슐화 |

- **📢 섹션 요약 비유**: 도서관 사서처럼 Reactor는 "책이 반납됐어요(준비)"라고 알리고, Proactor는 "책을 찾아서 책상 위에 올려놓았어요(완료)"라고 알린다.

---

## Ⅳ. 실무 적용 및 실무자 판단
**1. Windows IOCP 기반 서버**
- AcceptEx -> WSARecv/WSASend -> GetQueuedCompletionStatus 루프
- 스레드 풀 크기는 보통 CPU 코어 수의 2배 (I/O 완료 후 CPU 처리 고려)

<strong>2. Linux io_uring (커널 5.1+)</strong>
- Submission Queue (제출 큐)에 I/O 요청을 일괄 등록
- Completion Queue (완료 큐)에서 완료 이벤트 수확(Harvest)
- 시스템 콜 오버헤드 최소화 — 고빈도 소규모 I/O에 최적

**3. Boost.Asio / ASIO**
- 내부적으로 OS별 최적 비동기 I/O 백엔드 선택 (Windows: IOCP, Linux: epoll/io_uring)
- `io_context.run()`이 Proactor 역할

| 이슈 | 설명 | 대응 |
|:---|:---|:---|
| 버퍼 수명 관리 | OS가 I/O를 수행하는 동안 버퍼가 살아있어야 함 | 스마트 포인터, 공유 버퍼 |
| 에러 전파 | 완료 이벤트에 오류 코드 포함 | error_code 반드시 확인 |
| 역압(Backpressure) | 완료 큐 폭증 시 메모리 고갈 | 최대 동시 요청 수 제한 |
| 디버깅 난이도 | 비동기 흐름 추적 어려움 | 상관 ID(Correlation ID) 부여 |

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 주방장(CPU)이 설거지(I/O)를 식기세척기(OS)에 맡기고 요리(비즈니스 로직)에만 집중하는 것 — 단, 세척기에 그릇을 넣은 뒤 뚜껑을 열기 전까지(I/O 완료 전까지) 그릇(버퍼)을 건드리면 안 된다.

---

## Ⅴ. 기대효과 및 결론
Proactor 패턴은 비동기 I/O의 정점에 해당하는 아키텍처 패턴이다. OS가 I/O를 전담하고 애플리케이션은 순수하게 완료된 결과를 처리하는 역할 분리는 다음 효과를 제공한다:

- <strong>스레드 효율성 극대화</strong>: 소수 스레드로 수만 연결 처리 (C10K 해결)
- **CPU 가동률 향상**: I/O 블로킹 없이 Completion Handler 연속 실행
- <strong>응답 지연 감소</strong>: OS 레벨 비동기 I/O는 커널 내부에서 최적화됨

그러나 버퍼 수명 관리, 에러 전파, 복잡한 제어 흐름은 설계 복잡도를 높인다. 따라서 <strong>고성능 네트워크 서버(게임 서버, 실시간 스트리밍, 금융 거래 시스템)에서는 Proactor가 최선</strong>이지만, 간단한 서비스에서는 Reactor 기반 Node.js나 Netty가 충분하다.

심화 학습에서는 Reactor와 Proactor의 **"I/O 수행 주체"** 와 **"이벤트 발생 시점"** 의 차이를 명확히 서술하는 것이 핵심이다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Proactor는 "내가 할 일이 완전히 준비된 트레이로 날아오는 식당" — 요리사는 서빙도, 재료 준비도 신경 쓰지 않고 오직 최종 플레이팅(완료 처리)만 담당한다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 비동기 I/O 아키텍처 | 이벤트 기반 서버 설계의 상위 범주 |
| 하위 개념 | Completion Handler | 완료 이벤트를 처리하는 콜백 함수 |
| 대비 개념 | Reactor Pattern | I/O 준비 이벤트 기반, 앱이 I/O 수행 |
| 연관 개념 | Thread Pool Pattern | Completion Handler 실행 스레드 관리 |
| 구현체 | Windows IOCP | OS 레벨 완료 포트 메커니즘 |
| 구현체 | Boost.Asio | C++ Proactor 추상화 라이브러리 |
| 연관 개념 | Half-Sync/Half-Async | 비동기 수신 + 동기 처리 계층 분리 |

### 📈 관련 키워드 및 발전 흐름도
비동기 I/O 완료 -> 프로액터 패턴 -> Completion 기반 서버

### 👶 어린이를 위한 3줄 비유 설명
1. 레스토랑에서 음식을 주문하면, 셰프(OS)가 다 만들어서 테이블에 직접 가져다 줄 때 "다 됐어요!" 라고 알려주는 것이 Proactor야.
2. 내가 주방 앞에서 기다리다가 "음식 준비됐어요" 신호를 받고 직접 음식을 가져오면 Reactor고, 완성된 음식이 배달되면 Proactor야.
3. OS라는 로봇이 모든 무거운 일을 다 해주고 "다 끝났어!" 라고 알려줘서, 나는 결과만 받아 처리하면 되는 것이 Proactor 패턴이야.
