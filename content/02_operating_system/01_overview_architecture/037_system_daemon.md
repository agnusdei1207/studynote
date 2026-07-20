---
title: "System Daemon"
date: "2026-03-03"
tags:
  - "studynote-operating-system"
weight: 37
---
> **핵심 인사이트**
> 1. 데몬(Daemon)은 백그라운드에서 지속적으로 실행되는 서비스 프로세스로, 터미널(제어 터미널)에 연결되지 않고 부팅 시 시작해 시스템이 종료될 때까지 운영된다.
> 2. 데몬 생성의 핵심은 fork-exec 패턴에서 부모를 종료하고, 새 세션(setsid())을 생성해 제어 터미널을 분리하며, 표준 입출력을 /dev/null로 리다이렉트하는 것이다.
> 3. 현대 Linux에서는 systemd가 SysV init을 대체해 데몬 관리를 유닛 파일(Unit File) 기반으로 표준화했으며, 병렬 부팅·소켓 활성화·의존성 추적·cgroup 자원 제어를 제공한다.

---

## I. 데몬의 특성

```
일반 프로세스 vs 데몬 프로세스:

일반 프로세스:
  - 터미널(TTY)에 연결됨
  - 사용자 로그아웃 시 SIGHUP으로 종료
  - 포어그라운드/백그라운드 실행

데몬 프로세스:
  - TTY = ? (없음)
  - 세션 리더 없음 (setsid()로 새 세션 생성)
  - 부팅 시 시작, 시스템 종료 시 종료
  - PID 파일 (/var/run/nginx.pid)로 관리

데몬 이름 규칙: d 접미사
  httpd, sshd, cron, syslogd, ntpd, mysqld
```

> 📢 **섹션 요약 비유**: 데몬은 보이지 않는 집사 — 사용자가 로그인하든 아니든 항상 집안일(서비스)을 처리한다.

---

## II. 전통적 데몬 생성 과정

```
fork-exec 데몬화 과정:

1. fork() -> 자식 프로세스 생성
2. 부모 프로세스 exit() -> 터미널 제어권 반환
3. setsid() -> 새 세션 생성 (PGID, SID = PID)
4. 두 번째 fork() -> 세션 리더 권한 제거
5. umask(0) -> 파일 생성 권한 마스크 초기화
6. chdir("/") -> 작업 디렉토리를 루트로 변경
7. 표준 FD 닫기 -> /dev/null로 리다이렉트
8. 시그널 핸들러 설정 (SIGTERM, SIGHUP 처리)
```

| 단계       | 호출        | 목적                         |
|-----------|------------|------------------------------|
| 분기       | fork()     | 자식 프로세스 생성              |
| 부모 종료  | exit()     | 터미널에서 분리               |
| 세션 독립  | setsid()   | 새 프로세스 그룹·세션 생성      |
| I/O 리다이렉트| dup2() | stdin/stdout -> /dev/null    |

> 📢 **섹션 요약 비유**: 부모(fork)가 가게를 열고 자식에게 맡기고 퇴장(exit) — 자식 데몬은 이후 독립적으로 가게를 운영한다.

---

## III. systemd — 현대 데몬 관리

```
systemd 주요 특징:
  1. 병렬 부팅 (의존성 기반 동시 시작)
  2. 소켓 활성화 (on-demand 시작)
  3. cgroup 기반 자원 제어
  4. 저널 로그 (journald)
  5. 유닛 파일 (.service, .socket, .timer, .mount)

유닛 파일 예시 (nginx.service):
  [Unit]
  Description=NGINX Web Server
  After=network.target

  [Service]
  Type=forking
  PIDFile=/var/run/nginx.pid
  ExecStart=/usr/sbin/nginx
  Restart=on-failure

  [Install]
  WantedBy=multi-user.target

주요 명령:
  systemctl start/stop/restart nginx
  systemctl enable nginx   (부팅 시 자동 시작)
  journalctl -u nginx      (로그 확인)
```

> 📢 **섹션 요약 비유**: systemd는 데몬 관리 앱 — 언제 켜고, 얼마만큼 자원 쓰고, 실패 시 재시작 규칙을 한 파일에 정의.

---

## IV. 핵심 시스템 데몬

```
네트워크/서비스:
  sshd     - SSH 원격 접속 서비스
  httpd    - Apache 웹 서버
  nginx    - NGINX 웹 서버/리버스 프록시
  ntpd     - NTP 시간 동기화

시스템 관리:
  cron     - 주기적 작업 스케줄러
  syslogd  - 시스템 로그 수집 (rsyslog 대체)
  journald - systemd 저널 로그 데몬
  udevd    - 하드웨어 장치 이벤트 처리

데이터베이스:
  mysqld   - MySQL 서버
  mongod   - MongoDB 서버
  redis-server - Redis 인메모리 DB
```

> 📢 **섹션 요약 비유**: 웹 서버 데몬은 24시간 열려있는 은행 창구 — 요청이 올 때마다 응대하고, 아무도 없어도 항상 대기.

---

## V. 실무 시나리오 — 커스텀 데몬 서비스 등록

```
Python 백그라운드 워커를 systemd 데몬으로 등록:

1. 서비스 파일 생성:
   /etc/systemd/system/myworker.service

2. 파일 내용:
   [Unit]
   Description=My Background Worker
   After=network.target redis.service
   Requires=redis.service

   [Service]
   User=appuser
   WorkingDirectory=/opt/myapp
   ExecStart=/usr/bin/python3 /opt/myapp/worker.py
   Restart=always
   RestartSec=5
   StandardOutput=journal
   StandardError=journal

   [Install]
   WantedBy=multi-user.target

3. 등록 및 시작:
   systemctl daemon-reload
   systemctl enable myworker
   systemctl start myworker
```

> 📢 **섹션 요약 비유**: Python 스크립트를 전문 데몬으로 변신 — 부팅 시 자동 시작, 실패 시 자동 재시작, 로그 자동 수집.

---

## 📌 관련 개념 맵

```
시스템 데몬 (Daemon)
+-- 데몬 특성
|   +-- TTY 없음, 세션 독립
|   +-- PID 파일 기반 관리
+-- 데몬화 과정
|   +-- fork-exec-setsid
|   +-- /dev/null 리다이렉트
+-- systemd (현대 관리)
|   +-- 유닛 파일 (.service)
|   +-- 소켓 활성화, cgroup
|   +-- journald 로그
+-- 관련 개념
    +-- init 프로세스 (PID 1)
    +-- SysV init, Upstart
    +-- 프로세스 그룹, 세션
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 Unix 데몬 (1970s~)]
fork-setsid 수동 데몬화
SysV init 스크립트 관리
      |
      v
[SysV init 한계]
순차적 부팅, 의존성 없음
부팅 시간 길어짐 (수 분)
      |
      v
[Upstart (Ubuntu, 2006)]
이벤트 기반 비동기 부팅
      |
      v
[systemd (Lennart Poettering, 2010)]
병렬 부팅, cgroup, 소켓 활성화
사실상 모든 주요 Linux 배포판 채택
      |
      v
[현재: 컨테이너와 데몬의 변화]
Docker: 데몬 대신 컨테이너
Kubernetes: Pod으로 서비스 격리
systemd --user: 사용자 레벨 서비스
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 데몬은 컴퓨터가 켜져 있는 동안 항상 뒤에서 일하는 보이지 않는 일꾼이에요.
2. 웹사이트 서버, 이메일 서버 같은 것들이 모두 데몬으로 계속 실행되고 있어요.
3. systemd는 이 일꾼들을 관리하는 매니저로, 자동으로 켜고 끄고 실패하면 다시 시작시켜줘요!
