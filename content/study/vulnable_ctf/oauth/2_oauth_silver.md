+++
title = "VulnABLE CTF [LUXORA] Write-up: OAuth Misconfiguration 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "OAuth", "Silver", "CSRF", "State Parameter", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: OAuth Misconfiguration 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (OAuth Misconfig)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/oauth/silver`
- **목표**: OAuth 2.0 흐름에서 `state` 파라미터의 검증 부재를 악용하여, 공격자의 SNS 계정을 피해자의 LUXORA 계정에 강제로 연동(Account Link)시키는 CSRF(Cross-Site Request Forgery) 공격을 수행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/oauth/silver` 페이지에는 "Connect your Social Account" 기능이 있습니다.
사용자가 자신의 소셜 계정을 LUXORA 계정에 연동하여, 다음부터는 소셜 로그인만으로 들어올 수 있게 해주는 기능입니다.

**[정상적인 소셜 연동 흐름]**
1. 사용자가 연동 버튼을 누르면 다음 URL로 이동합니다.
   ```http
   https://social.luxora.test/auth?client_id=luxapp&response_type=code&redirect_uri=http://localhost:3000/oauth/silver/callback
   ```
2. 사용자가 `social.luxora.test` 에서 로그인을 완료합니다.
3. 소셜 서버는 사용자를 콜백 주소로 리다이렉트 시킵니다.
   ```http
   http://localhost:3000/oauth/silver/callback?code=AUTH_CODE_12345
   ```
4. LUXORA 서버는 저 코드를 이용해 소셜 계정 식별자를 받아오고, 현재 로그인된 계정과 연동시킵니다.

**[해커의 사고 과정]**
1. OAuth 흐름을 잘 보면, 뭔가 하나 빠져 있다. 원래는 CSRF 방어를 위해 요청 시 `state=랜덤값` 을 보내고 콜백에서 그 값을 검증해야 한다.
2. 하지만 이 시스템은 `state` 파라미터를 전혀 쓰지 않거나 검증하지 않고 있다.
3. 만약 내가 내 소셜 계정으로 로그인해서 `?code=해커의_코드` 를 받아낸 다음, 이 URL을 피해자에게 보내서 클릭하게 만든다면?
4. 피해자의 LUXORA 계정에 해커의 소셜 계정이 연동될 것이다! 그러면 나는 내 소셜 계정으로 로그인해서 피해자의 계정을 탈취할 수 있다!

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(redirect_uri=attacker.com)--> [ OAuth Server ]
                                              |-- Redirects Victim with Auth Code
[ Victim ]   --(Sends Auth Code)------------> [ Attacker Server ]
```


이른바 **OAuth CSRF (또는 Account Linking CSRF)** 공격입니다.

### 💡 공격 시나리오 설계
1. **해커의 인증 코드 획득**: 해커는 자신의 계정으로 소셜 로그인을 진행하되, 콜백 URL로 리다이렉트 되기 직전에 Burp Suite 등으로 패킷을 잡아두고 서버로 코드가 넘어가는 것을 막습니다. (또는 수동으로 콜백 URL만 복사해 둡니다.)
   * 해커가 얻은 콜백 URL: `http://localhost:3000/oauth/silver/callback?code=HACKER_SECRET_CODE`

2. **악성 링크 유포**: 해커는 자신이 얻은 저 URL을 그대로 피해자(Admin)에게 보냅니다.
   * `Hey Admin, check out this funny cat picture: <a href="http://localhost:3000/oauth/silver/callback?code=HACKER_SECRET_CODE">Click Here</a>`

3. **강제 연동(Forced Linking)**: 피해자가 현재 LUXORA 사이트에 로그인된 상태에서 저 링크를 클릭하면, LUXORA 서버는 피해자의 계정에 해커의 소셜 계정을 연동해 버립니다.

---

## 🚀 3. 공격 수행 및 계정 탈취

### Step 1. 함정 링크 전송
위에서 설계한 악성 콜백 링크를 챌린지 환경의 봇(Admin)에게 전송합니다. 봇이 링크를 클릭하는 시뮬레이션이 동작합니다.

### Step 2. 백도어 로그인 (Backdoor Login)
이제 해커는 `http://localhost:3000/oauth/silver` 로 가서, **자신의 소셜 계정**으로 "Social Login" 버튼을 클릭합니다.

### 🔍 서버의 응답
해커의 소셜 계정은 방금 전 피해자(Admin)의 계정과 강제로 연동(Linked)되었습니다. 따라서 시스템은 해커를 관리자로 인식하고 대시보드를 열어줍니다!

```html
<div class="dashboard">
  <h2>Welcome back, Administrator!</h2>
  <p>Your social account has been successfully verified.</p>
  <p class="flag">FLAG{OAUTH_🥈_CSRF_ACCOUNT_LINK_E5F6G7}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

OAuth 프로토콜에서 상태 관리(State)를 생략했을 때, 해커의 인가 코드(Authorization Code)가 피해자의 세션에 주입되어 계정이 통째로 탈취되는 과정을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{OAUTH_🥈_CSRF_ACCOUNT_LINK_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 문제는 CSRF(Cross-Site Request Forgery)의 변종으로, OAuth 명세(RFC 6749)에서 `state` 파라미터 사용을 **강력히 권고(RECOMMENDED)**하고 있음에도 불구하고 이를 구현하지 않은 개발자의 과실입니다.

* **안전한 패치 가이드 (State 파라미터 강제 검증)**
1. **State 발급**: 사용자가 "소셜 연동" 버튼을 누르는 순간, 백엔드에서 암호학적으로 안전한 난수(State)를 생성하여 사용자의 현재 세션(Session)에 저장하고, 이를 OAuth 요청 URL에 포함시킵니다.
   ```javascript
   const state = crypto.randomBytes(16).toString('hex');
   req.session.oauth_state = state;
   const authUrl = `https://social.luxora.test/auth?...&state=${state}`;
   ```

2. **State 검증**: 인증 서버로부터 리다이렉트 되어 돌아올 때, URL 파라미터에 있는 `state` 값과 현재 세션에 저장된 `oauth_state` 값이 정확히 일치하는지 비교합니다.
   ```javascript
   if (!req.query.state || req.query.state !== req.session.oauth_state) {
       return res.status(403).send("CSRF Attack Detected! State mismatch.");
   }
   // 검증 통과 후 연동 진행
   ```
이렇게 조치하면 해커가 자신의 코드가 담긴 링크를 피해자에게 보내더라도, 해커의 State 값과 피해자 세션의 State 값이 일치하지 않으므로 공격이 100% 차단됩니다.