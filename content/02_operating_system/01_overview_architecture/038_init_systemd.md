---
title: "Init Systemd"
date: "2026-03-03"
tags:
  - "studynote-operating-system"
weight: 38
---
> **핵심 인사이트**
> 1. init(PID 1)은 커널 부팅 후 처음 실행되는 프로세스로 모든 다른 프로세스의 조상이며, 전통적인 SysV init은 순차적 런레벨(Runlevel) 기반 서비스 시작으로 부팅이 느린 한계가 있었다.
> 2. systemd는 의존성 기반 병렬 부팅, 소켓/D-Bus 활성화, cgroup 자원 제어, 저널 로깅을 통합 제공하는 현대적 초기화 시스템으로, 부팅 시간을 수 분에서 수 초로 단축했다.
> 3. systemd vs sysvinit의 핵심 차이: SysV는 "스크립트 실행 순서", systemd는 "의존성 그래프 기반 병렬 시작" — 현재 RHEL/Ubuntu/Debian 등 거의 모든 주요 Linux 배포판이 systemd를 채택했다.

---

## I. init(PID 1)의 역할

```
부팅 순서:
  BIOS/UEFI
    -> 부트로더 (GRUB)
      -> 커널 (vmlinuz)
        -> initramfs (임시 루트)
          -> init (PID 1) 시작
            -> 모든 서비스/프로세스 생성

init의 책임:
  1. 모든 다른 프로세스의 부모
  2. 고아 프로세스(Orphan) 입양 (reparenting)
  3. 좀비 프로세스(Zombie) 정리 (reaping)
  4. 시스템 종료/재시작 관리
  5. 런레벨/타깃 전환 관리
```

> 📢 **섹션 요약 비유**: init은 회사의 첫 직원(PID 1) — 모든 다른 직원을 채용하고, 퇴사한 직원 처리도 담당.

---

## II. SysV init 런레벨

```
SysV init 런레벨 (Runlevel):

  0: 시스템 종료 (Halt)
  1: 단일 사용자 모드 (복구 모드)
  2: 다중 사용자 (NFS 없음)
  3: 다중 사용자 + 네트워크 (텍스트 모드)
  4: 사용자 정의
  5: 다중 사용자 + 그래픽 (GUI 로그인)
  6: 재시작 (Reboot)

/etc/rc.d/ 또는 /etc/init.d/:
  각 런레벨별 시작/종료 스크립트
  이름 규칙: S20network (S=시작, 20=우선순위)
            K80network (K=종료, 80=우선순위)

문제:
  순차 실행 -> 이전 서비스가 완료 후 다음 시작
  부팅 시간: 수 분 소요
  의존성 관리 없음 (스크립트 번호로만 순서 제어)
```

> 📢 **섹션 요약 비유**: SysV는 아침 출근 도어락 비밀번호처럼 순서대로만 가능 — 커피 기계(30번)가 켜져야 에어컨(40번)이 켜지는 고정 순서.

---

## III. systemd 혁신

```
systemd 핵심 개선:

1. 병렬 부팅:
   의존성 그래프 -> 독립 서비스 동시 시작
   부팅 시간: 수 분 -> 수 초

2. 소켓 활성화:
   서비스가 소켓을 미리 열어 요청 대기
   첫 요청이 올 때 실제 서비스 시작 (on-demand)

3. D-Bus 활성화:
   D-Bus 버스 이름으로 서비스 활성화

4. cgroup 통합:
   서비스별 CPU/메모리/IO 자원 제한
   관련 프로세스 그룹 일괄 관리

5. 저널 로깅:
   journald: 구조화된 바이너리 로그
   journalctl -u nginx / -b (부팅 로그)

6. 타깃 (Target):
   런레벨 대신 선언적 타깃
   multi-user.target, graphical.target
```

| SysV 런레벨 | systemd 타깃              |
|---------|--------------------------|
| 0       | poweroff.target          |
| 1       | rescue.target            |
| 3       | multi-user.target        |
| 5       | graphical.target         |
| 6       | reboot.target            |

> 📢 **섹션 요약 비유**: systemd는 프로젝트 매니저 — 의존 관계 있는 것만 순서 지키고, 독립적인 것은 동시에 시작.

---

## IV. systemd 유닛 종류

```
주요 유닛 파일 (.service, .socket, .timer, ...):

.service: 서비스 (데몬 프로세스)
  nginx.service, sshd.service

.socket: 소켓 기반 활성화
  sshd.socket -> 연결 시에만 sshd 시작

.timer: 주기적 실행 (cron 대체)
  backup.timer: 매일 오전 2시 실행

.mount: 파일시스템 마운트
  home.mount: /home 마운트

.target: 서비스 그룹 (런레벨 대체)
  multi-user.target

주요 명령:
  systemctl start/stop/restart/status nginx
  systemctl enable/disable nginx  (부팅 시 자동)
  systemctl list-units
  journalctl -u nginx -f  (실시간 로그)
```

> 📢 **섹션 요약 비유**: .timer는 cron의 systemd 버전 — crontab 대신 유닛 파일로 스케줄 관리, journald로 로그도 통합.

---

## V. 실무 시나리오 — 부팅 성능 분석

```
부팅 분석 명령:
  systemd-analyze              (총 부팅 시간)
  systemd-analyze blame        (서비스별 시간 정렬)
  systemd-analyze critical-chain (임계 경로)

결과 예시:
  Startup finished in 1.2s (kernel) + 3.8s (userspace)
  Total: 5.0s

  systemd-analyze blame:
    2.1s NetworkManager.service
    1.5s snapd.service
    0.8s plymouth-quit-wait.service

최적화:
  disable snapd (사용 안 함)
  -> 부팅 시간 5.0s -> 2.8s (44% 단축)

  실무 서버에서:
  cloud-init 비활성화 (가상머신 아닌 경우)
  불필요한 서비스 disable
```

> 📢 **섹션 요약 비유**: systemd-analyze blame은 부팅 시간 낭비 범인 찾기 — 가장 오래 걸린 서비스를 찾아 비활성화.

---

## 📌 관련 개념 맵

```
init과 systemd
+-- PID 1 역할
|   +-- 모든 프로세스 조상
|   +-- 좀비/고아 관리
+-- SysV init
|   +-- 런레벨 (0-6)
|   +-- 순차 스크립트, 느린 부팅
+-- systemd
|   +-- 병렬 부팅, 의존성 그래프
|   +-- 유닛 파일 (.service, .timer, .socket)
|   +-- cgroup, journald 통합
+-- 관련 개념
    +-- Upstart (이벤트 기반, Ubuntu 이전)
    +-- OpenRC (Alpine Linux)
    +-- runit (더 단순한 대안)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[SysV init (Unix 전통)]
런레벨 기반 순차 부팅
수 분의 부팅 시간
      |
      v
[Upstart (Ubuntu 2006~2014)]
이벤트 기반 비동기 부팅
      |
      v
[systemd (Lennart Poettering, 2010)]
병렬 + 소켓 활성화 + cgroup
Ubuntu 15.04부터 채택
Red Hat/Fedora/Debian 모두 전환
      |
      v
[현재: 컨테이너 시대의 init]
Docker: PID 1 = 앱 프로세스 직접
Kubernetes: kubelet이 프로세스 관리
tini, dumb-init: 컨테이너용 경량 init
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. init은 컴퓨터가 켜질 때 제일 먼저 시작되는 특별한 프로그램으로, 나머지 모든 프로그램의 부모예요.
2. 옛날 방식(SysV)은 서비스를 하나씩 순서대로 켰지만, systemd는 상관없는 서비스들을 동시에 켜서 부팅을 몇 배 빠르게 해요.
3. systemd는 서비스 관리, 로그 수집, 자원 제한을 모두 통합해서 현대 Linux 서버의 핵심 관리자가 됐어요!
