---
title: "Client Server"
date: "2026-04-05"
tags:
  - "studynote-operating-system"
weight: 49
---
> **핵심 인사이트**
> 1. 클라이언트-서버 모델(Client-Server Model)은 요청자(Client)와 제공자(Server)의 역할을 분리하는 분산 컴퓨팅의 가장 기본 패러다임 — OS 관점에서 프로세스 간 통신(IPC), 소켓, 스레드 관리까지 OS의 핵심 기능이 이 모델을 지탱한다.
> 2. 서버의 연결 처리 방식(단일 프로세스·멀티프로세스·멀티스레드·이벤트 루프)이 성능과 자원 효율의 핵심 트레이드오프 — Apache의 프로세스 기반 vs Nginx의 이벤트 루프 차이가 C10K 문제 해결의 분기점이 되었다.
> 3. 현대 마이크로서비스는 클라이언트-서버를 N-Tier로 확장한 것 — 서비스가 동시에 클라이언트이자 서버로 동작하며, 서비스 디스커버리·로드밸런서·서킷 브레이커가 전통적 서버의 역할을 분산화했다.

---

## Ⅰ. 클라이언트-서버 기본 구조

```
클라이언트-서버 모델:

클라이언트 (Client):
  서비스 요청자
  능동적: 연결 시작
  예: 브라우저, 모바일 앱, CLI

서버 (Server):
  서비스 제공자
  수동적: 연결 대기
  예: 웹 서버, DB 서버, 파일 서버

기본 통신 흐름:

클라이언트 -> [요청: Request] -> 서버
클라이언트 <- [응답: Response] <- 서버

소켓 기반 통신:
  서버:
  1. socket() -> 소켓 생성
  2. bind(IP, Port) -> 주소 바인딩
  3. listen() -> 연결 대기
  4. accept() -> 연결 수락 (블로킹)
  5. recv()/send() -> 데이터 교환
  6. close() -> 연결 종료

  클라이언트:
  1. socket() -> 소켓 생성
  2. connect(서버IP, 서버Port) -> 연결 시도
  3. send()/recv() -> 데이터 교환
  4. close() -> 종료

아키텍처 유형:
  2-Tier: 클라이언트 ↔ DB 서버 (직접)
  3-Tier: 클라이언트 ↔ 앱 서버 ↔ DB 서버
  N-Tier: 마이크로서비스 (각 서비스가 클라+서버)
```

> 📢 **섹션 요약 비유**: 클라이언트-서버 = 손님과 식당 — 손님(클라이언트)이 주문(요청), 식당(서버)이 요리해서 전달(응답). 식당은 항상 열려 있고(listen), 손님이 와야 시작!

---

## Ⅱ. 서버의 연결 처리 방식

```
서버 연결 처리 모델:

1. 단일 프로세스 (Single Process):
  연결 하나씩 순차 처리

  while True:
      conn = accept()
      handle(conn)  # 완료될 때까지 대기

  문제: 동시 접속 불가 (처음부터 비실용)

2. 멀티프로세스 (Multi-Process):
  요청마다 fork()로 자식 프로세스 생성

  while True:
      conn = accept()
      pid = fork()
      if pid == 0:   # 자식 프로세스
          handle(conn)
          exit()

  Apache 전통 방식 (prefork MPM)

  단점:
  fork() 비용: ~수ms, 메모리 복사(CoW)
  프로세스당 메모리: ~50MB
  동시 1000연결: 50GB 메모리!

3. 멀티스레드 (Multi-Thread):
  요청마다 스레드 생성 (또는 스레드 풀)

  while True:
      conn = accept()
      thread = Thread(target=handle, args=(conn,))
      thread.start()

  Apache worker MPM

  스레드 특성:
  프로세스보다 생성 빠름 (~수십us)
  메모리 공유 (stack만 분리, 약 8MB)

  단점:
  C10K(10,000 동시 연결) 시 스레드 10,000개
  컨텍스트 스위칭 오버헤드 급증

4. 이벤트 루프 (Event Loop / Non-Blocking I/O):
  단일 스레드가 모든 연결 이벤트 처리

  epoll (Linux):
  while True:
      events = epoll.wait()  # 준비된 이벤트 대기
      for event in events:
          if event.type == READ:
              handle_read(event.fd)
          elif event.type == WRITE:
              handle_write(event.fd)

  Nginx, Node.js 방식

  장점:
  C10K 이상 처리 (C100K+)
  메모리 효율 (스레드 수 제한)

  단점:
  CPU 집약 작업에 부적합
  콜백 지옥 (비동기 복잡성)
```

> 📢 **섹션 요약 비유**: 서버 처리 방식 = 식당 서빙 방식 — 멀티프로세스(손님마다 요리사 1명), 멀티스레드(웨이터 여러 명), 이벤트 루프(웨이터 1명이 알림(이벤트) 받으며 효율적으로 처리). Nginx = 1명 슈퍼 웨이터!

---

## Ⅲ. C10K 문제와 해결

```
C10K 문제 (1999, Dan Kegel):
  단일 서버에서 동시 10,000 연결 처리 도전

  당시 Apache (멀티프로세스) 한계:
  프로세스 10,000개 × 50MB = 500GB 메모리 필요
  컨텍스트 스위칭: 10,000번/초 -> CPU 병목

해결책:

epoll (Linux 2.6):
  select(): O(N) - 전체 FD 스캔
  poll(): O(N) - 유사
  epoll(): O(1) - 이벤트 기반 준비 통보

  epoll 메커니즘:
  - epoll_create(): 이벤트 큐 생성
  - epoll_ctl(): FD 등록/수정/삭제
  - epoll_wait(): 준비된 이벤트 블로킹 대기

  10,000 연결 중 100개 활성 -> 100개만 처리

Nginx 아키텍처:
  마스터 프로세스 1개
  워커 프로세스 = CPU 코어 수 (예: 16개)
  각 워커: 이벤트 루프로 수천 연결 처리

  구성:
  worker_processes auto;  # CPU 코어 수
  events {
      worker_connections 1024;
      use epoll;
  }

  이론적 최대: 16 × 1024 = 16,384 동시 연결

Node.js libuv:
  V8 엔진 + libuv(이벤트 루프 라이브러리)
  epoll(Linux), kqueue(macOS), IOCP(Windows) 통합

  비동기 I/O:
  fs.readFile('data.json', (err, data) => {
      // I/O 완료 후 콜백 (블로킹 없음)
  });
```

> 📢 **섹션 요약 비유**: C10K = 동시 손님 1만 명 — 멀티프로세스 식당은 요리사 1만 명 고용(불가). Nginx/epoll은 "요청 완료" 알림 시스템으로 효율화. 알림 받은 것만 처리!

---

## Ⅳ. 로드밸런싱과 고가용성

```
로드밸런서 (Load Balancer):
  다수의 서버에 요청 분산
  단일 장애 지점(SPOF) 제거

로드밸런싱 알고리즘:

라운드 로빈 (Round Robin):
  순서대로 서버에 배분
  1->2->3->1->2->3
  단순, 서버 성능 동일할 때 적합

가중 라운드 로빈 (Weighted RR):
  서버 성능에 따라 비율 조정
  A(4코어): 4배, B(2코어): 2배, C(2코어): 2배
  -> A에 50%, B에 25%, C에 25%

최소 연결 (Least Connections):
  현재 연결 수가 가장 적은 서버에 배분
  처리 시간이 다른 요청에 효과적

IP 해시 (IP Hash):
  클라이언트 IP로 서버 고정
  세션 친화성(Session Affinity) 필요 시

헬스 체크 (Health Check):
  주기적으로 서버 상태 확인

  HTTP: GET /health -> 200 OK (정상)
  TCP: 연결 시도 성공 여부

  이상 감지 시: 라우팅에서 제외 (자동)

L4 vs L7 로드밸런서:
  L4 (Transport): IP/Port 기반 (빠름, 내용 모름)
  L7 (Application): URL/헤더 기반 (느리지만 스마트)

  L7 예:
  /api/ -> API 서버 클러스터
  /static/ -> 파일 서버
  /admin/ -> 관리 서버
```

> 📢 **섹션 요약 비유**: 로드밸런서 = 식당 안내 데스크 — 손님 오면 대기줄 짧은 테이블(최소 연결) 배정. 한 테이블 고장(헬스 체크 실패) 시 자동으로 다른 테이블 배정!

---

## Ⅴ. 실무 시나리오 — 대규모 API 서버 설계

```
월 10억 요청 처리 API 서버 아키텍처:

요구사항:
  RPS 피크: 50,000 req/s
  P99 응답시간: 50ms 이하
  가용성: 99.99% (연 52분 이하 다운)

아키텍처:

클라이언트 -> CDN(CloudFront)
  -> L7 로드밸런서(ALB) × 2
  -> API 서버 클러스터 (20대)
  -> 내부 L4 LB -> DB 서버

API 서버 (Nginx + Node.js):
  Nginx:
  worker_processes 8;
  worker_connections 4096;
  upstream api_pool {
      server 127.0.0.1:3000 weight=1;
      server 127.0.0.1:3001 weight=1;
      ...
      keepalive 100;
  }

  Node.js PM2 클러스터:
  instances = CPU 코어 수
  -> 각 인스턴스: 이벤트 루프로 I/O 처리

연결 풀:
  DB 연결 풀: 서버당 20연결 × 20대 = 400연결

  연결 생성 비용: ~20ms
  풀로 재사용 -> ~1ms 이하

성능 결과:
  Nginx + epoll: 50,000 RPS 안정 처리
  P99: 23ms (목표 50ms 대비 여유)
  서버 1대 CPU: 45% (헤드룸 55%)

  쿠버네티스 HPA:
  CPU 70% 초과 시 자동 스케일아웃
  RPS 급증 -> 20 -> 40대 자동 확장
```

> 📢 **섹션 요약 비유**: 대규모 API 서버 = 패스트푸드 체인 본사 관리 — CDN(포장 완료품 배달), ALB(매장 안내), Nginx(주문 접수), Node.js(요리), DB 풀(식재료 창고). 자동 확장으로 피크도 안정!

---

## 📌 관련 개념 맵

```
클라이언트-서버 아키텍처
+-- 통신 기반
|   +-- 소켓 (Socket)
|   +-- TCP/UDP
+-- 서버 처리 방식
|   +-- 멀티프로세스 (fork)
|   +-- 멀티스레드
|   +-- 이벤트 루프 (epoll)
+-- 스케일링
|   +-- 로드밸런서 (L4/L7)
|   +-- 헬스 체크
|   +-- 수평 확장 (Scale-Out)
+-- 현대 발전
    +-- 마이크로서비스
    +-- 서비스 메시
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[클라이언트-서버 모델 (1960s)]
메인프레임 + 터미널
중앙 집중 처리
      |
      v
[인터넷 웹 서버 (1990s)]
Apache, IIS
멀티프로세스
      |
      v
[C10K 문제 제기 (1999)]
동시 연결 한계
      |
      v
[Nginx, epoll (2000s)]
이벤트 루프 대중화
C10K 해결
      |
      v
[마이크로서비스 (2010s~)]
N-Tier 분산
서비스 메시, K8s
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 클라이언트-서버 = 손님과 식당 — 손님(클라이언트)이 주문(요청), 식당(서버)이 항상 열려 대기. 손님이 와야 시작!
2. epoll 이벤트 루프 = 1명 슈퍼 웨이터 — 1,000 손님 알림 기다리다 완성된 것만 처리. 수천 동시 연결을 혼자 효율적으로!
3. 로드밸런서 = 식당 안내 데스크 — 손님 오면 가장 한가한 테이블 배정. 테이블 고장 시 자동으로 다른 곳으로!
