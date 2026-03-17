+++
title = "VulnABLE CTF [LUXORA] Write-up: Weak Crypto 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Crypto", "Silver", "ECB Mode", "Block Cipher", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Weak Crypto 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Weak Cryptography)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/crypto/silver`
- **목표**: 서버가 데이터를 "진짜 암호화(Encryption)" 하긴 했으나, 보안에 매우 취약한 블록 암호 모드인 **AES-ECB 모드**를 사용한 것을 간파하고, 암호문 블록을 잘라 붙여(Cut and Paste) 관리자 권한의 암호문을 위조해내라.

---

## 🕵️‍♂️ 1. 정보 수집 및 암호문 패턴 분석 (Reconnaissance)

`/crypto/silver` 경로에서 계정 생성 시 쿠키(`token`)가 어떻게 발급되는지 테스트해 봅니다.

**[테스트 1: username = `user1`]**
```http
Set-Cookie: token=U2FsdGVkX1+...A1B2
```

**[테스트 2: username = `user2`]**
```http
Set-Cookie: token=U2FsdGVkX1+...C3D4
```

이번에는 길이가 긴 사용자 이름으로 테스트해 봅니다.
**[테스트 3: username = `AAAAAAAA` (8바이트)]**
```http
Set-Cookie: token=7e8e5d0a6c...
```
**[테스트 4: username = `AAAAAAAAAAAAAAAA` (16바이트)]**
```http
Set-Cookie: token=7e8e5d0a6c...7e8e5d0a6c...
```

**[해커의 사고 과정]**
1. 쿠키 값이 길고 무작위로 보인다. 이건 Base64가 아니라 진짜 암호화된 값(Ciphertext)이다.
2. 하지만 `A`를 16글자 넣었더니, 암호문이 정확히 같은 패턴(`7e8e5d0a6c...`)으로 두 번 반복해서 나왔다!
3. 이것은 16바이트 단위로 평문을 잘라서 각각 따로 암호화하는 **AES-ECB 모드**의 전형적인 증상이다. (IV, Initialization Vector가 없음)
4. ECB 모드는 같은 평문 블록은 항상 같은 암호문 블록을 만들어낸다. 이를 이용해 블록을 내 마음대로 잘라서 이어 붙이면(Cut & Paste) 새로운 의미의 암호문을 만들 수 있다!

---

## 💥 2. 취약점 식별 및 ECB Cut & Paste 공격 설계

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ]
|-- Intercepts Ciphertext/Token
|-- Analyzes Pattern (ECB Block, Base64, etc.)
|-- Cuts/Pastes/Decodes/Spoofs
|-- Sends Forged Token --> [ Web Server ]
                           |-- Accepts Forged Token
```


서버가 암호화하는 평문(Plaintext)의 구조가 대략 이렇다고 유추할 수 있습니다.
`username=[내가입력한값]&role=user`

블록은 16바이트 단위로 잘립니다. 우리는 `role=admin` 이라는 문자열이 깔끔하게 하나의 블록에 들어가도록 입력값을 조절해야 합니다.

### 💡 평문 블록 정렬 (Block Alignment)
목표 평문 구조를 16바이트 블록으로 그려봅니다.

* **블록 1**: `username=aaaaaaa` (16바이트, a는 7개)
* **블록 2**: `admin&role=user` (16바이트, admin 뒤에 패딩을 채워 넣음)
* **블록 3**: (이후는 버릴 부분)

우리는 `username` 칸에 `aaaaaaaadmin` 을 입력하여, `admin`이라는 글자가 정확히 두 번째 블록의 첫 글자로 오도록 밉니다(Shift).

**[공격 수행 시나리오]**
1. 해커는 여러 번의 가입 시도를 통해 블록 길이를 맞춥니다.
2. `admin` 이라는 문자열이 담긴 암호문 블록을 획득하여 복사(Copy)해 둡니다.
3. 원래 사용하던 정상적인 `user` 암호문 블록의 맨 마지막(role=user 부분)을 잘라내고, 아까 복사해 둔 `admin` 블록을 붙여넣기(Paste) 합니다.

---

## 🚀 3. 공격 수행 및 권한 탈취

이 과정은 수동으로 하기엔 패딩 계산이 복잡하므로, Burp Suite의 Crypto 확장 기능이나 파이썬의 `pwntools` 등을 활용합니다.

개념적으로, 서버에 두 번의 요청을 보냅니다.

1. **블록 추출용 요청**: `username=aaaaaaaadmin           `
   ➔ 서버가 암호화한 값 반환: `[블록A][블록B_admin][블록C]`
   ➔ 해커는 여기서 **[블록B_admin]** 부분(16바이트)만 뚝 떼어서 저장해 둡니다.

2. **베이스 토큰용 요청**: `username=hacker`
   ➔ 서버가 암호화한 값 반환: `[블록X_hacker][블록Y_role_user]`

3. **토큰 조립 (Cut & Paste)**
   해커는 `[블록X_hacker]` 뒤에 아까 훔친 `[블록B_admin]`을 이어 붙입니다.
   ➔ 조립된 가짜 토큰: `[블록X_hacker][블록B_admin]`

### 🔍 서버의 응답
조립된 토큰을 쿠키에 넣고 관리자 페이지로 접근합니다.
서버는 이 토큰을 자신의 키로 복호화합니다.
복호화된 평문: `username=hacker&role=admin           `

서버는 이 평문을 보고 권한을 상승시켜 줍니다!

```html
HTTP/1.1 200 OK

<div class="success">
  <h2>Welcome to the Admin Area</h2>
  <p>ECB Cut and Paste Attack Successful.</p>
  <p class="flag">FLAG{CRYPTO_🥈_ECB_CUT_AND_PASTE_E5F6G7}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

가장 강력한 암호화 알고리즘인 AES를 사용하더라도, 운영 모드(Cipher Mode)를 잘못 선택하면(ECB 모드) 해커가 평문을 알지 못해도 암호문을 레고 블록처럼 재조립하여 인증을 파괴할 수 있음을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{CRYPTO_🥈_ECB_CUT_AND_PASTE_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
블록 암호에서 **ECB (Electronic Codebook)** 모드는 똑같은 블록이 똑같은 암호문으로 변환되기 때문에 패턴이 고스란히 노출되는 치명적인 결함이 있습니다. (유명한 펭귄 이미지 암호화 밈 참조)

* **안전한 패치 가이드 (안전한 암호화 모드 및 무결성 검증)**
1. **ECB 모드 절대 사용 금지**: `AES-128-ECB` 대신, 반드시 매번 다른 IV(초기화 벡터)를 사용하여 패턴을 숨기는 **CBC 모드 (AES-256-CBC)** 또는 **GCM 모드 (AES-256-GCM)** 를 사용해야 합니다.
2. **Authenticated Encryption (AEAD)**: CBC 모드조차도 Bit-Flipping(비트 반전) 공격이나 Padding Oracle 공격에 취약할 수 있습니다. 가장 현대적이고 안전한 방식은 암호화와 무결성 검증(서명)을 동시에 수행하는 **AES-GCM (Galois/Counter Mode)**을 사용하는 것입니다.

```javascript
// Node.js의 crypto 모듈을 사용한 안전한 AES-GCM 암호화 예시
const crypto = require('crypto');
const algorithm = 'aes-256-gcm';
const iv = crypto.randomBytes(12); // 매번 랜덤한 IV 생성

const cipher = crypto.createCipheriv(algorithm, SECRET_KEY, iv);
let encrypted = cipher.update(plaintext, 'utf8', 'hex');
encrypted += cipher.final('hex');
const authTag = cipher.getAuthTag().toString('hex'); // 무결성 서명표

// 복호화할 때는 IV와 authTag를 함께 보내어 데이터가 1비트라도 조작되었는지 검증함