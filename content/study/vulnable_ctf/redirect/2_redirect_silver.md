+++
title = "VulnABLE CTF [LUXORA] Write-up: Open Redirect 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Open Redirect", "Silver", "Filter Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Open Redirect 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (Open Redirect)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/redirect/silver`
- **목표**: 서버가 `http://` 와 `https://` 와 같은 절대 경로 스키마를 정규식으로 필터링하는 상황에서, 브라우저의 URL 해석 방식(Protocol-Relative URL, 백슬래시 등)을 악용하여 필터를 우회하고 외부 도메인으로 리다이렉트를 성사시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/redirect/silver` 페이지 역시 로그인 후 이동할 경로를 파라미터로 받습니다.

**[Bronze 방식(절대 경로) 테스트]**
```http
GET /redirect/silver/login?next=http://evil.com
```

**[서버의 에러 응답]**
```html
Error: External redirects are not allowed. "http://" is blocked.
```

**[해커의 사고 과정]**
1. 개발자가 `http://` 와 `https://` 문자열이 들어가면 무조건 에러를 띄우도록(블랙리스트) 만들었다.
2. 하지만 브라우저는 아주 다양한 형태의 URL을 이해한다.
3. 스키마(http)를 생략하고 슬래시 두 개(`//`)로 시작하는 **Protocol-Relative URL (프로토콜 상대 URL)** 을 쓰면 어떨까?
4. 또는 슬래시(`/`) 대신 역슬래시(`\`)를 섞어 쓰면 서버의 정규식은 피하면서 브라우저는 알아서 정상 URL로 고쳐서 이동하지 않을까?

---

## 💥 2. 취약점 식별 및 필터 우회 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Victim ] --(GET /login?next=//attacker.com)--> [ Web Server ]
                                                 |-- Redirects to Attacker Site
```


블랙리스트 기반 필터링의 가장 큰 맹점은 해커가 무수히 많은 우회 형태(Bypass Payload)를 만들어낼 수 있다는 것입니다.

### 💡 다양한 Bypass 페이로드 테스트

1. **Protocol-Relative URL (가장 흔한 우회)**
   `?next=//evil-attacker.com`
   ➔ 서버는 `http://` 가 없으므로 통과시킵니다. 브라우저는 현재 페이지가 `http`라면 자동으로 `http://evil-attacker.com` 으로 이동합니다.

2. **백슬래시 혼합 (브라우저 관용성 악용)**
   `?next=/\evil-attacker.com`
   `?next=\\evil-attacker.com`
   ➔ 서버(정규식)는 이것이 슬래시 2개로 시작하지 않거나 외부 도메인이 아니라고 착각합니다. 하지만 크롬/엣지 등의 브라우저는 역슬래시를 슬래시로 자동 교정하여 이동합니다.

3. **URL 인코딩 결합**
   `?next=%09//evil-attacker.com` (앞에 탭 문자 삽입)
   `?next=/%0d/evil-attacker.com` (중간에 캐리지 리턴 삽입)

이 챌린지에서는 서버가 `//` 로 시작하는 것도 막고 있다고 가정하고, **역슬래시 혼합 방식**을 사용해 보겠습니다.

---

## 🚀 3. 공격 수행 및 결과 확인

역슬래시 페이로드를 사용하여 타겟 봇(Admin)을 유도합니다.

**[조작된 URL 생성]**
```text
http://localhost:3000/redirect/silver/login?next=/\evil-attacker.com/phishing
```

### 🔍 서버의 동작 (필터 통과)
서버의 엉성한 정규식(예: `if(url.startsWith('http') || url.startsWith('//'))`)은 `/\` 패턴을 잡지 못합니다.
서버는 이 값을 정상적인 내부 경로(Relative Path)로 착각하여 헤더를 세팅합니다.

```http
HTTP/1.1 302 Found
Location: /\evil-attacker.com/phishing
```

### 🔍 브라우저의 해석 및 플래그 획득
피해자의 브라우저는 `Location: /\evil-attacker.com/phishing` 을 받고, 자동으로 역슬래시를 정규화하여 `//evil-attacker.com/phishing` 으로 해석한 뒤 해커의 사이트로 이동합니다.

```text
[!] System: Filter bypass detected. Open Redirect successful.
FLAG: FLAG{REDIRECT_🥈_FILTER_BYPASS_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

블랙리스트 방식의 입력값 검증이 브라우저의 유연한 URL 해석 규격(RFC 3986 및 브라우저 자체 교정)과 충돌할 때 얼마나 쉽게 우회되는지를 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{REDIRECT_🥈_FILTER_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
'나쁜 것을 골라내는(Blacklisting)' 방식을 사용한 것이 근본 원인입니다.

* **안전한 패치 가이드 (완벽한 URL 파싱 및 도메인 검증)**
사용자가 입력한 URL을 단순 문자열(String)로 다루지 말고, 백엔드 언어에 내장된 강력한 **URL 파싱 라이브러리(URL Parser)**를 사용하여 호스트네임을 명확히 추출하고 비교해야 합니다.

```javascript
// Node.js의 URL 모듈을 사용한 안전한 방식
const { URL } = require('url');

app.get('/login', (req, res) => {
    try {
        // 브라우저가 보는 것과 똑같이 URL을 파싱함
        // 상대 경로(/dashboard)가 들어오면 기본 도메인을 붙여서 평가함
        const parsedUrl = new URL(req.query.next, 'http://localhost:3000');
        
        // Hostname이 정확히 내 서버 도메인과 일치하는지(화이트리스트) 깐깐하게 비교
        if (parsedUrl.hostname === 'localhost' || parsedUrl.hostname === 'www.luxora.test') {
            return res.redirect(parsedUrl.href);
        } else {
            return res.redirect('/default-dashboard');
        }
    } catch (e) {
        // 이상한 문자가 섞여 파싱에 실패하면 기본 경로로 보냄
        return res.redirect('/default-dashboard');
    }
});
```
이 방식을 사용하면 해커가 `/\evil.com` 을 보내든 `%00` 을 섞든, URL 파서가 브라우저와 동일하게 `evil.com` 이라는 호스트를 뽑아내므로 완벽한 화이트리스트 차단이 가능합니다.