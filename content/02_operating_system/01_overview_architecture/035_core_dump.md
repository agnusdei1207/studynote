---
title: "Core Dump"
date: "2026-03-03"
tags:
  - "studynote-operating-system"
weight: 35
---
> **핵심 인사이트**
> 1. Core Dump는 프로세스가 비정상 종료(SIGSEGV, SIGABRT 등) 시 해당 시점의 메모리, 레지스터, 스택 상태를 디스크에 저장한 스냅샷으로 사후 디버깅(Post-mortem Debugging)의 핵심 도구다.
> 2. 덤프 파일에는 프로세스의 가상 주소 공간(코드·데이터·힙·스택), CPU 레지스터 상태, 열린 파일 디스크립터가 포함된다.
> 3. 프로덕션 환경에서는 보안상 코어 덤프를 비활성화하거나 제한하고, 대신 크래시 리포팅 서비스(Sentry, Crashpad)를 활용한다.

---

## I. 코어 덤프 생성 조건

```
프로세스 실행 중
      |
      +-- SIGSEGV (세그멘테이션 폴트)
      +-- SIGABRT (abort() 호출)
      +-- SIGFPE  (부동소수점 오류)
      +-- SIGBUS  (버스 오류)
            |
            v
    커널이 core 파일 생성
    (ulimit -c로 크기 제한)
```

| 시그널    | 원인                    | 코어 덤프 |
|-----------|-------------------------|-----------|
| SIGSEGV   | 잘못된 메모리 접근      | Yes       |
| SIGABRT   | assert 실패, abort()    | Yes       |
| SIGTERM   | 정상 종료 요청          | No        |

> 📢 **섹션 요약 비유**: 비행기 블랙박스처럼 충돌 직전 모든 상태를 기록 — 사고 후 원인 분석에 쓴다.

---

## II. 코어 덤프 파일 구조

```
ELF Core File (ET_CORE)
+-- ELF Header
+-- Program Headers
|   +-- PT_NOTE: 프로세스 정보(PID, 시그널, 레지스터)
|   +-- PT_LOAD: 메모리 세그먼트들
|       +-- .text  (코드 세그먼트)
|       +-- .data  (초기화 데이터)
|       +-- heap   (동적 할당 영역)
|       +-- stack  (스택 프레임들)
+-- Notes Section
    +-- NT_PRSTATUS: 레지스터 값, 시그널 번호
    +-- NT_PRPSINFO: 프로세스 이름, 상태
```

> 📢 **섹션 요약 비유**: 크래시 시점 프로세스의 신분증·지갑·메모장을 통째로 복사해 보관.

---

## III. 코어 덤프 활성화 및 분석

```bash
ulimit -c unlimited
cat /proc/sys/kernel/core_pattern
gdb ./myprogram core.12345
(gdb) bt
(gdb) info regs
(gdb) frame 3
```

| 명령            | 설명                     |
|----------------|--------------------------|
| bt (backtrace) | 함수 호출 스택 출력       |
| info locals    | 현재 프레임 지역 변수     |
| print var      | 변수 값 출력              |

> 📢 **섹션 요약 비유**: GDB로 덤프를 열면 시간이 멈춘 상태의 프로그램을 들여다볼 수 있다.

---

## IV. 프로덕션 환경 처리 전략

```
프로덕션 서버
+-- 코어 덤프 비활성화 (ulimit -c 0)
|   이유: 민감 데이터 노출 위험, 디스크 용량
|
+-- 크래시 리포팅 서비스 연동
|   +-- Sentry (예외 + 스택트레이스)
|   +-- Crashpad / Breakpad
|   +-- systemd-coredump
|
+-- 미니 덤프 (Minidump)
    +-- 전체 메모리 대신 핵심 스택만 저장
```

> 📢 **섹션 요약 비유**: 필요한 정보만 선택적으로 — 전체 녹음은 프라이버시 침해.

---

## V. 실무 시나리오 — 생산 장애 분석

| 단계 | 행동                                     |
|------|------------------------------------------|
| 1    | 로그에서 OOM Killer 시그널 확인          |
| 2    | systemctl status로 종료 코드 확인        |
| 3    | coredumpctl list (systemd 환경)          |
| 4    | coredumpctl gdb로 백트레이스 추출        |
| 5    | 스택·레지스터로 크래시 지점 특정         |
| 6    | ASAN으로 재현 검증                       |

> 📢 **섹션 요약 비유**: 장애 보고서 없이 서버를 고치는 건 블랙박스 없이 비행기 사고를 조사하는 것.

---

## 📌 관련 개념 맵

```
코어 덤프 (Core Dump)
+-- 트리거: SIGSEGV / SIGABRT / SIGFPE
+-- 파일 형식: ELF ET_CORE
|   +-- PT_NOTE (레지스터, 프로세스 정보)
|   +-- PT_LOAD (메모리 세그먼트)
+-- 분석 도구: GDB / lldb / WinDbg
+-- 활성화 제어
|   +-- ulimit -c (크기 한도)
|   +-- /proc/sys/kernel/core_pattern
+-- 대안
    +-- Minidump / Sentry / ASAN
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 유닉스]
코어 = 자기 코어 메모리 전체 덤프
      |
      v
[현대 Linux ELF]
ELF ET_CORE, ulimit, core_pattern 제어
      |
      v
[GDB 사후 디버깅]
bt / info regs 로 크래시 지점 분석
      |
      +-------------------------+
      v                         v
[Minidump / Crashpad]      [ASAN / Valgrind]
경량 크래시 수집             런타임 메모리 탐지
      |
      v
[Sentry / Firebase Crashlytics]
사용자 환경 크래시 자동 수집·분석
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 코어 덤프는 프로그램이 갑자기 멈출 때 그 순간의 상태를 사진 찍어 저장하는 거예요.
2. 나중에 그 사진을 보면서 왜 멈췄을까 조사할 수 있어요.
3. 비행기 블랙박스처럼, 사고가 난 후 원인을 찾는 데 꼭 필요한 도구예요!
