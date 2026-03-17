+++
title = "VulnABLE CTF [LUXORA] Write-up: Request Smuggling 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Request Smuggling", "Bronze", "CL.TE", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Request Smuggling 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Request Smuggling)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/smuggle/bronze`
- **목표**: 프론트엔드 서버(로드밸런서/프록시)와 백엔드 서버 간의 HTTP 요청 해석 차이(CL.TE)를 악용하여, 프론트엔드에서는 허용된 경로로 요청을 보내지만 백엔드에서는 몰래 숨겨둔(Smuggled) 관리자 전용 경로로 해석되도록 만들어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 아키텍처 분석 (Reconnaissance)

현대의 웹 아키텍처는 보통 사용자가 프론트엔드 리버스 프록시(Nginx, HAProxy)를 먼저 거치고, 그 프록시가 내부 백엔드(Node.js, Tomcat)로 요청을 전달하는 구조입니다.

`/admin/smuggle` 경로에 직접 접속해 봅니다.
➔ **[프론트엔드 응답]**: `403 Forbidden: External access to /admin is blocked by Proxy.`

**[해커의 사고 과정]**
1. 프론트엔드 프록시가 `/admin` 으로 시작하는 요청을 얄짤없이 차단하고 있다.
2. 하지만 프록시를 속이고(Bypass) 백엔드에 직접 `/admin` 요청을 보낼 수 있다면?
3. 프론트엔드와 백엔드가 HTTP 요청 패킷의 끝(경계)을 판단하는 기준이 다르다면 **HTTP Request Smuggling** 공격이 가능하다!
4. `Content-Length (CL)` 헤더와 `Transfer-Encoding (TE)` 헤더를 동시에 보내서 반응을 보자.

---

## 💥 2. 취약점 식별 및 CL.TE 페이로드 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(CL.TE Malformed Request)--> [ Front-end Proxy (Reads CL) ]
                                            |-- Forwards as One Request
                                            [ Back-end Server (Reads TE) ]
                                            |-- Splits into Two Requests!
```


이 챌린지는 **CL.TE (Content-Length / Transfer-Encoding)** 취약점 환경입니다.
- **프론트엔드(Proxy)**: `Content-Length` (CL) 를 기준으로 패킷을 자름.
- **백엔드(Server)**: `Transfer-Encoding: chunked` (TE) 를 우선하여 패킷을 자름.

### 💡 밀수(Smuggling) 페이로드 작성
Burp Suite의 Repeater에서 'Update Content-Length' 기능을 끄고, 프로토콜 지원을 HTTP/1.1 로 맞춘 뒤, 줄바꿈(`\r\n`)을 아주 정교하게 맞춰서 전송합니다.

**[조작된 HTTP 패킷]**
```http
POST /smuggle/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Content-Length: 44
Transfer-Encoding: chunked

0

GET /admin/smuggle HTTP/1.1
Host: localhost:3000
X-Ignore: X
```
*(주의: 0 뒤에 빈 줄(`\r\n\r\n`)이 반드시 두 번 들어가야 Chunked 형식의 끝으로 인식됩니다.)*

---

## 🚀 3. 공격 수행 및 통신 흐름 분석

### 🔍 프론트엔드(Proxy)의 해석
프록시는 `Content-Length: 44`를 보고, 바디 전체(0부터 끝까지)를 **하나의 정상적인 POST 요청**으로 간주합니다. `/smuggle/bronze` 경로이므로 방화벽을 통과시켜 백엔드로 넘깁니다.

### 🔍 백엔드(Server)의 해석
백엔드는 `Transfer-Encoding: chunked`를 우선적으로 읽습니다.
1. `0\r\n\r\n` 을 만나는 순간, "아, 첫 번째 POST 요청이 여기서 끝났구나!" 라고 생각합니다.
2. 그리고 아직 소켓 버퍼에 남아있는 뒷부분(`GET /admin/smuggle HTTP/1.1...`)을 **새롭게 들어온 두 번째 요청(Smuggled Request)**으로 해석해 버립니다!

### 🔍 서버의 응답
잠시 후, 큐(Queue)에 밀려있던 나의 다음 요청(혹은 다른 사용자의 요청)에 대한 응답으로, 백엔드가 몰래 처리했던 `/admin/smuggle` 의 결과가 돌아옵니다.

```html
HTTP/1.1 200 OK

<div class="admin-panel">
  <h1>Secret Admin Interface</h1>
  <p>FLAG{SMUGGLE_🥉_CL_TE_BYPASS_A1B2C3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

HTTP 규격의 모호함(두 개의 길이 헤더가 동시에 올 때의 처리 방식)을 악용하여, WAF나 리버스 프록시의 라우팅/차단 정책을 완벽하게 무력화(Bypass)하는 공격을 성사시켰습니다.

**🔥 획득한 플래그:**
`FLAG{SMUGGLE_🥉_CL_TE_BYPASS_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프론트엔드와 백엔드의 HTTP 파싱 규격(RFC 7230) 구현체가 서로 달라 발생하는 구조적 취약점입니다. (RFC에서는 `Content-Length`와 `Transfer-Encoding`이 동시에 오면 `Content-Length`를 무시하라고 명시되어 있으나, 프록시가 이를 어긴 것입니다.)

* **안전한 패치 가이드 (HTTP 파서 정규화 및 HTTP/2)**
1. **프론트엔드 정규화 (Normalization)**: 프록시(Nginx, HAProxy, AWS ALB 등) 설정을 점검하여, 모호한 헤더가 포함된 요청은 무조건 400 Bad Request로 드랍(Drop)하도록 설정해야 합니다.
2. **HTTP/2 도입**: HTTP/1.1의 텍스트 기반 파싱의 한계 때문에 Smuggling이 발생합니다. 프론트엔드와 백엔드 구간(End-to-End)의 통신을 바이너리 프레이밍 계층을 사용하는 **HTTP/2**로 업그레이드하면 이 취약점 클래스 전체가 근본적으로 소멸합니다.