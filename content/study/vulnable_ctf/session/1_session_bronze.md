+++
title = "VulnABLE CTF [LUXORA] Write-up: Session Attacks 🥉 Bronze"
description = "LUXORA 플랫폼의 Session Fixation 취약점을 이용한 세션 고정 공격 및 관리자 권한 탈취 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Session Attack", "Bronze", "Session Fixation", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Session Attacks 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Session Attacks)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/session/bronze`
- **목표**: 로그인 전과 후의 세션 ID(Session ID)가 변하지 않는 **세션 고정(Session Fixation)** 취약점을 악용하여, 공격자가 미리 설정해둔 세션으로 타겟 사용자(피해자)가 로그인하도록 유도한 뒤 계정 권한을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/session/bronze` 경로에 처음 접근하면, 로그인 창이 뜨면서 브라우저에 임의의 `session_id` 쿠키가 부여됩니다.

**[최초 접속 시 (로그인 전)]**
```http
HTTP/1.1 200 OK
Set-Cookie: session_id=abc123xyz; Path=/
```
이 시점에서 내 세션은 아직 아무 권한이 없는 '익명(Anonymous)' 상태입니다.

이제 정상적인 테스트 계정(`user` / `password`)으로 로그인을 수행해 봅니다.

**[로그인 성공 시]**
```http
HTTP/1.1 200 OK
// 응답 헤더에 새로운 Set-Cookie 가 없음!!
```

**[해커의 사고 과정]**
1. 정상적인 웹 프레임워크는 사용자가 로그인을 성공하면, 이전에 쓰던 세션을 파기하고 완전히 새로운(안전한) 난수 세션 ID를 새로 발급(`Session Regeneration`)해야 한다.
2. 하지만 이 서버는 내가 처음 접속했을 때 받은 `abc123xyz` 라는 세션 ID를 로그인 이후에도 **그대로 유지**하고 있다.
3. 그렇다면, 내가 임의로 만든 세션 ID를 피해자의 브라우저에 강제로 세팅해두고(Fixation), 피해자가 그 상태에서 관리자 로그인을 하게 만들면 어떻게 될까?

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation Strategy)

공격의 핵심은 "내가 만든 세션 ID를 다른 사람이 쓰게 만드는 것"입니다.

### 💡 Session Fixation 공격 시나리오
1. **세션 획득**: 해커가 타겟 사이트에 접속하여 유효한 세션 쿠키(`session_id=hacker_trap_999`)를 하나 받습니다. (또는 직접 만듭니다.)
2. **함정 파기 (Fixation)**: 해커가 피해자(Admin)에게 악성 링크를 보냅니다. 이 링크를 클릭하면 피해자의 브라우저 쿠키에 해커의 세션 ID가 세팅됩니다. (보통 XSS나 파라미터 조작을 통해 수행)
3. **피해자 로그인**: 피해자는 아무 의심 없이 자신의 ID/PW를 치고 로그인합니다. 이때 시스템은 해커의 세션 ID(`hacker_trap_999`)에 "관리자 권한"을 부여해 버립니다.
4. **해커의 접속**: 해커는 이미 알고 있는 세션 ID(`hacker_trap_999`)를 가지고 타겟 사이트에 접속하면, 비밀번호를 몰라도 관리자로 로그인되어 있습니다!

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

이번 CTF 환경에서는 피해자(봇)에게 악성 링크를 보내는 헬퍼 기능이 제공된다고 가정합니다.

### Step 1. 함정 세션 생성
해커의 브라우저에서 쿠키 편집기를 열고, 값을 내가 기억하기 쉬운 값으로 강제 변경합니다.
- 변경된 쿠키: `session_id=HACKER_SESSION_123`

### Step 2. 피해자 브라우저에 세션 고정 (Fixation)
취약한 애플리케이션의 URL 파라미터(`?session=...`)를 통해 세션을 고정시킬 수 있는 기능이 있다고 가정하고 피해자에게 링크를 보냅니다.
```text
http://localhost:3000/session/bronze/login?session_id=HACKER_SESSION_123
```

*(피해자가 링크를 클릭하고 관리자로 로그인하는 시뮬레이션이 백그라운드에서 동작합니다.)*

### Step 3. 권한 탈취 확인
이제 해커의 브라우저(또는 Burp Suite)에서 `session_id=HACKER_SESSION_123` 을 달고 보호된 대시보드(`/session/bronze/dashboard`)에 접속합니다.

```http
GET /session/bronze/dashboard HTTP/1.1
Host: localhost:3000
Cookie: session_id=HACKER_SESSION_123
```

### 🔍 서버의 응답
서버는 이 세션이 아까 관리자가 정상적으로 로그인하여 인증을 마친 세션이라고 판단하고 문을 열어줍니다!

```html
<h2>Admin Dashboard</h2>
<p>Welcome, Administrator.</p>
<p class="flag">FLAG{SESSION_🥉_FIXATION_C7D8E9}</p>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

로그인 전후로 세션 식별자가 갱신되지 않는 사소한 로직 결함이, 세션 탈취(Hijacking)와 동일한 파괴력을 가지는 권한 탈취 취약점으로 이어짐을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{SESSION_🥉_FIXATION_C7D8E9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 원인은 **"로그인(권한 변경) 시 세션 재발급 누락"** 입니다.

* **취약한 코드 예시**
```javascript
// 사용자가 로그인에 성공하면, 기존 세션 객체에 로그인 정보만 덧붙임
req.session.userId = user.id;
req.session.role = user.role;
```

* **안전한 패치 가이드 (Session Regeneration)**
모든 웹 프레임워크는 로그인/로그아웃 등 권한이 바뀌는 중대한 이벤트 발생 시, 무조건 기존 세션을 날려버리고 완전히 새로운 세션 ID를 발급하는 함수를 제공합니다.
```javascript
// Node.js (express-session) 환경에서의 안전한 처리
req.session.regenerate(function(err) {
    if(err) throw err;
    
    // 재생성된 새 세션에 권한 부여
    req.session.userId = user.id;
    req.session.role = user.role;
    res.redirect('/dashboard');
});
```
이렇게 하면 해커가 심어둔 `HACKER_SESSION_123` 은 피해자가 로그인 버튼을 누르는 순간 즉시 파기되고, 피해자에게만 새로운 안전한 세션이 발급되어 공격이 무력화됩니다.