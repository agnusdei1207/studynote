---
title: "Reactor Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 212
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Reactor (리액터) 패턴은 단일 스레드의 이벤트 루프(Event Loop)가 I/O Multiplexing(다중화)을 통해 다수의 I/O 이벤트를 동시에 감시하고, 이벤트 발생 시 등록된 핸들러를 즉시 호출하는 비동기 I/O 아키텍처다.
> 2. **가치**: 스레드 생성 없이 수만 개의 동시 연결을 처리할 수 있어, C10K (Concurrent 10,000 connections) 문제를 해결하는 핵심 기술이다.
> 3. **판단 포인트**: CPU 집중 작업이 아닌 I/O 대기가 많은 상황(네트워크 서버, API 게이트웨이 등)에서 최적이다. CPU 집중 작업은 Worker Thread Pool과 결합한다.

---

## Ⅰ. 개요 및 필요성
```
  Thread-Per-Connection 모델:
  연결 10,000개 -> 스레드 10,000개
  -> 스레드 스택 메모리: 10,000 × 1MB = 10GB!
  -> Context Switching (문맥 교환) 오버헤드 폭발
  -> OS 스레드 한계 도달
```

```
  Reactor 모델:
  연결 10,000개 -> 단일 이벤트 루프 + 소수의 스레드
  -> I/O 준비 완료된 연결만 처리 (select/epoll)
  -> Context Switching 최소화
  -> Node.js, Nginx가 이 모델로 수만 동시 연결 처리
```

| 기술 | OS | 특징 | 성능 |
|:---|:---|:---|:---|
| `select` | Unix/Windows | 최대 1024 FD | O(n) |
| `poll` | Unix | FD 제한 없음 | O(n) |
| `epoll` | Linux | 이벤트 기반 알림 | O(1) |
| `kqueue` | macOS/BSD | epoll과 유사 | O(1) |
| `IOCP` | Windows | 완료 기반(Proactor) | O(1) |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 수박 밭 관리 — 1만 개 수박(연결)을 1만 명 농부(스레드)가 각각 지키는 게 아니라, 드론(이벤트 루프)이 날아다니며 익은 수박(준비된 I/O)만 수확 팀에게 알려준다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  +---------------------------------------------------------+
  |  Reactor (= Dispatcher = Event Loop)                    |
  |  -> Synchronous Event Demultiplexer를 감시               |
  |  -> 이벤트 발생 시 Handle에 연결된 Event Handler 호출   |
  +----------------------------------------------------------+
           | 이벤트 등록            | 이벤트 발생 알림
           v                        v
  +----------------+    +-----------------------------------+
  |  Handle (FD)   |    |  Synchronous Event Demultiplexer  |
  |  - 소켓        |    |  (select / epoll / kqueue)        |
  |  - 파일 디스크 |    |  -> I/O 준비 완료된 Handle 반환   |
  |  - 파이프      |    +-----------------------------------+
  +----------------+
           |
           v
  +--------------------------------------------------------+
  |  Event Handler (이벤트 핸들러)                         |
  |  - AcceptEventHandler: 새 연결 수락                    |
  |  - ReadEventHandler: 데이터 읽기                       |
  |  - WriteEventHandler: 데이터 쓰기                      |
  +--------------------------------------------------------+
```

```
  [ Reactor Event Loop ]

  while (running) {
      1. events = demultiplexer.select()     // epoll_wait: I/O 준비 대기
                                             // (CPU는 이 단계에서 다른 스레드에 양보)
      2. for (event in events) {
           handler = registry.get(event.handle)
           handler.handleEvent(event)        // 이벤트 핸들러 즉시 호출
         }
  }

  --------------------------------------------------
  시간 흐름:

  t=0  select() 대기 (CPU 반환)
  t=5ms 소켓A 읽기 준비 -> ReadHandler.handle(A)
  t=5ms 소켓B 쓰기 준비 -> WriteHandler.handle(B)
  t=6ms 처리 완료 -> select() 대기 재진입
  t=10ms 소켓C 연결 요청 -> AcceptHandler.handle(C)
  ...
```

```
  Node.js I/O 처리 구조:

  JavaScript Code (단일 스레드)
         |
         | fs.readFile(), http.get() 등 비동기 API 호출
         v
  +----------------------------------------------+
  |  libuv Event Loop (Reactor 구현)             |
  |                                              |
  |  ① Timers       -> setTimeout, setInterval   |
  |  ② I/O Pending  -> 완료된 I/O 콜백           |
  |  ③ Idle/Prepare -> 내부 처리                  |
  |  ④ Poll         -> epoll로 새 I/O 이벤트 대기 |
  |  ⑤ Check        -> setImmediate              |
  |  ⑥ Close        -> 소켓 닫기 등              |
  +----------------------------------------------+
         |
         v CPU 집중 작업 -> Worker Thread Pool (libuv)
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| 검증 포인트 | 테스트·로그·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 119 종합상황실 — 상황실(Event Loop)이 모든 신고 채널(Handle)을 모니터링하고, 신고가 들어오면(이벤트) 해당 전담팀(Event Handler)에게 즉시 연결한다. 신고가 없는 동안은 CPU를 낭비하지 않는다.

---

## Ⅲ. 비교 및 연결
| 항목 | Thread-Per-Connection | Reactor | Proactor |
|:---|:---|:---|:---|
| **동기/비동기** | 동기 | 동기 이벤트 감시 | 완료 기반 비동기 |
| **알림 시점** | 블로킹 | I/O 준비 완료 시 | I/O 완료 후 |
| <strong>스레드 수</strong> | 연결 수만큼 | 소수 | 소수 |
| **구현 복잡도** | 낮음 | 중간 | 높음 |
| **OS 지원** | 모든 OS | Unix (epoll/kqueue) | Windows (IOCP) |
| **대표 구현** | Tomcat BIO | Node.js, Nginx, Netty | Windows IOCP |

| 시스템 | Reactor 구현 방식 |
|:---|:---|
| Node.js | libuv, epoll/kqueue |
| Nginx | epoll 기반 단일 마스터 + 워커 |
| Netty (Java) | Boss Group + Worker Group |
| Redis | 단일 스레드 이벤트 루프 |
| Kafka | NIO Selector |

- **📢 섹션 요약 비유**: Reactor vs Proactor = "음식점 종업원이 주방에서 음식이 나오면 가져오는 것(Reactor)" vs "주방에서 종업원 자리까지 직접 가져다주는 것(Proactor)". 시작 시점이 다르다.

---

## Ⅳ. 실무 적용 및 실무자 판단
```
  Netty = 고성능 비동기 네트워크 프레임워크 (Reactor 구현)

  +---------------------------------------------------------+
  |  Boss EventLoopGroup (연결 수락 전담)                   |
  |  -> 새 연결을 accept -> Worker Group에 할당              |
  +--------------------------+------------------------------+
                              | 연결 등록
  +---------------------------v-----------------------------+
  |  Worker EventLoopGroup (I/O 처리 전담)                  |
  |  -> 각 Worker = 이벤트 루프 스레드                       |
  |  -> ChannelPipeline을 통해 Handler 체인 실행             |
  +---------------------------------------------------------+

  // 코드 예시
  EventLoopGroup bossGroup = new NioEventLoopGroup(1);
  EventLoopGroup workerGroup = new NioEventLoopGroup(4);

  ServerBootstrap b = new ServerBootstrap()
      .group(bossGroup, workerGroup)
      .childHandler(new ChannelInitializer<>() {
          protected void initChannel(Channel ch) {
              ch.pipeline().addLast(new HttpDecoder(), new MyHandler());
          }
      });
```

```
  적합한 상황:
  ✅ 수천~수만 개의 동시 연결
  ✅ I/O 대기 시간이 처리 시간의 대부분
  ✅ 각 요청 처리 시간이 짧음
  ✅ 실시간 웹소켓, 채팅 서버, API 게이트웨이

  부적합한 상황:
  ❌ CPU 집중 연산 (암호화, 이미지 처리)
     -> 이벤트 루프 블로킹 위험
     -> Worker Thread Pool 분리 필요
  ❌ 복잡한 트랜잭션 처리
     -> Spring MVC의 Thread-Per-Request가 더 적합
```

- <strong>I/O Multiplexing</strong> (select/epoll) 메커니즘과 Reactor의 연관성 명시
- **C10K 문제** 해결 방법으로 Reactor 패턴 제시
- Node.js, Nginx, Netty 등 실제 구현 사례로 신뢰성 강화
- **Reactor vs Proactor** 차이 (I/O 준비 시 알림 vs 완료 후 알림)

### 판단 체크리스트
1. 해결하려는 변화 축이 분명한가?
2. 추상화 비용보다 변경 절감 효과가 큰가?
3. 테스트·로그·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 공항 내 자동 안내판(이벤트 루프) — 모든 항공편 게이트(Handle)를 실시간 감시하다가 탑승 안내가 시작되면(I/O 이벤트) 해당 게이트 서비스 직원(Event Handler)에게 즉시 알린다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| 높은 동시성 | 스레드 수와 무관하게 수만 연결 처리 |
| 낮은 메모리 | 스레드 스택 최소화 |
| 낮은 지연 | epoll의 O(1) 이벤트 통지 |
| 에너지 효율 | I/O 대기 중 CPU 반환 |

- **블로킹 코드 금지**: 이벤트 루프 내 블로킹 작업 -> 모든 연결 지연
- **CPU 집중 작업**: Worker Thread Pool로 반드시 오프로드
- **콜백 지옥(Callback Hell)**: Promise/async-await/Reactive Streams로 해결

Reactor (리액터) 패턴은 현대 고성능 서버의 핵심 아키텍처다. Node.js, Nginx, Netty, Redis 모두 이 패턴을 기반으로 수만 개의 동시 연결을 소수의 스레드로 처리한다. I/O 집중 워크로드에서 Thread-Per-Connection의 수십 배 처리량을 달성한다.

확장 방향은 ① 선언형 API와의 결합, ② 관측 가능성(Observability) 내장, ③ 분산 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Reactor는 "스마트 교통 관제 시스템" — 모든 도로(I/O 채널)를 실시간 감시하다가 사고(이벤트)가 나면 해당 구역 대응팀(Handler)을 즉시 출동시킨다. 평상시에는 단 한 명의 관제원(Event Loop)으로 충분하다.

---

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 동시성 패턴 (Concurrency Pattern) | 병렬 처리 설계 패턴 그룹 |
| 하위 개념 | Event Handler / Handle / Dispatcher | Reactor 4요소 |
| 연관 개념 | epoll / kqueue | I/O Multiplexing 기술 |
| 연관 개념 | Node.js libuv | Reactor 패턴의 JS 구현 |
| 연관 개념 | Netty | Java 고성능 Reactor 프레임워크 |
| 연관 개념 | Proactor Pattern | 완료 기반 비동기의 대안 패턴 |

### 📈 관련 키워드 및 발전 흐름도
이벤트 분리 -> 리액터 패턴 -> 논블로킹 서버

### 👶 어린이를 위한 3줄 비유 설명
1. 놀이공원에서 놀이기구(연결)가 만 개 있어도, 안내원(이벤트 루프)은 딱 한 명이에요.
2. 안내원은 라디오(epoll)로 "이 기구 탈 수 있어요!"라는 신호가 오면 해당 기구 직원에게 알려줘요.
3. 이렇게 적은 사람으로 만 개의 기구를 동시에 관리하는 게 Reactor 패턴이에요!
