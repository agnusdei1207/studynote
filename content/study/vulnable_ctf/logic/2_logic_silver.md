+++
title = "VulnABLE CTF [LUXORA] Write-up: Business Logic 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Business Logic", "Silver", "Rounding Error", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Business Logic 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Business Logic Flaw)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/logic/silver`
- **목표**: 아이템의 가격을 분할하여 구매할 때 발생하는 **부동 소수점(Floating Point) 또는 정수 반올림(Rounding) 결함**을 이용하여, 실제 가격보다 훨씬 적은 돈을 내고 상품을 구매하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/logic/silver` 페이지에는 아주 비싼 상품(예: "Diamond Watch", 가격 `$100.00`)을 분할 결제(Installment Payment)로 살 수 있는 기능이 있습니다.

내 계좌 잔액은 `$5.00` 밖에 없으므로, 일시불로는 절대 살 수 없습니다.
분할 횟수(개월 수)를 입력하는 칸이 있습니다. 

**[정상 분할 결제 테스트]**
- 상품 가격: `$100.00`
- 분할 횟수 파라미터(`installments`): `10`
- 서버 응답: "1회차 결제 금액은 `$10.00` 입니다. (잔액 부족)"

**[해커의 사고 과정]**
1. 1회차 결제 금액 공식은 `Math.round(Total / installments)` 거나, 부동 소수점을 대충 자르는 로직일 것이다.
2. 만약 내가 `installments` 값을 무지막지하게 큰 수, 예를 들어 `100000000000` (천억) 으로 입력한다면 어떻게 될까?
3. `100 / 100000000000 = 0.000000001`
4. 서버가 이 값을 소수점 둘째 자리에서 반올림하거나 버린다면(Truncate), 1회차 결제 금액이 **`$0.00`** 이 될 것이다!

---

## 💥 2. 취약점 식별 및 데이터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Buy -10 Items)--> [ Web Server ]
                                  |-- Total = -500
                                  |-- Balance = Balance - (-500)
                                  |-- Balance Increased!
```


금융/결제 시스템에서 소수점을 다루는 방식(Rounding Error)이나 자료형 한계(Integer Underflow/Overflow)를 찌르는 공격입니다.

### 💡 파라미터 변조 설계
Burp Suite를 통해 분할 횟수 파라미터를 조작합니다.

**[조작된 HTTP 패킷]**
```http
POST /logic/silver/checkout HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session=hacker_session

item_id=99&installments=10000
```
(100 / 10000 = 0.01 이므로, 더 극적으로 0을 만들기 위해 `3333333` 같은 값을 넣을 수도 있습니다.)

---

## 🚀 3. 공격 수행 및 결제 성공 확인

서버로 조작된 패킷을 전송합니다.

### 🔍 서버 내부의 동작
백엔드 로직이 다음과 같이 짜여있다고 가정해 봅시다.

```javascript
let total = 100.00;
let months = parseInt(req.body.installments);

// 1회차 청구 금액 계산 후 정수로 변환 (센트 단위 절사)
let firstPayment = Math.floor(total / months);

// 100 / 10000 = 0.01 -> Math.floor(0.01) = 0 !!
if (user.balance >= firstPayment) {
    user.balance -= firstPayment; // 5 - 0 = 5
    deliverItem();
}
```

### 🔍 서버의 응답
서버는 1회차 결제 금액을 `$0` 으로 계산했고, 내 잔고(`$5`)가 `$0`보다 크거나 같으므로 결제를 승인해 버렸습니다!

```html
HTTP/1.1 200 OK

<div class="success">
  <h2>Payment Successful!</h2>
  <p>First installment of $0.00 has been paid.</p>
  <p>Item "Diamond Watch" delivered to your inventory.</p>
  <p class="flag">FLAG{LOGIC_🥈_ROUNDING_ERROR_F1A2B3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

부동 소수점 연산이나 나눗셈(Division) 로직에서 발생하는 미세한 정밀도 손실(Precision Loss)과 반올림/내림(Rounding) 처리를 악용하여, 비싼 물건을 사실상 공짜(0원)로 구매하는 로직 결함을 뚫어냈습니다.

**🔥 획득한 플래그:**
`FLAG{LOGIC_🥈_ROUNDING_ERROR_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
결제 금액을 계산할 때, 분할 횟수에 대한 상한선(Maximum Limit)을 두지 않았고, 최소 결제 단위(Minimum Amount) 검증도 누락한 것이 원인입니다.

* **안전한 패치 가이드 (정수 연산 및 최소 금액 검증)**
1. **분할 횟수 상한선 설정**: 클라이언트가 보낸 할부 횟수가 비즈니스 정책(예: 최대 12개월)에 맞는지 엄격하게 검사해야 합니다.
   ```javascript
   if (months < 1 || months > 12) return res.status(400).send("Invalid installments.");
   ```
2. **금액은 무조건 정수(Integer)로 처리**: 돈을 다룰 때는 소수점이 있는 실수형(`float`, `double`)을 절대 사용하면 안 됩니다. 달러라면 무조건 **센트(Cent)** 단위의 정수(Integer)로 변환하여 연산해야 부동 소수점 오차가 발생하지 않습니다.
3. **최소 결제 금액 강제**: 어떤 연산 결과를 거치든, 청구되는 금액은 시스템이 허용하는 최소 결제 금액(예: `$1.00`) 이상이어야 한다는 방어 로직을 넣어야 합니다.
   ```javascript
   if (firstPayment <= 0) return res.status(400).send("Payment amount too low.");