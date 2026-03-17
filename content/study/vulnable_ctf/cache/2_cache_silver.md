+++
title = "VulnABLE CTF [LUXORA] Write-up: Cache Poisoning 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Cache Poisoning", "Silver", "Parameter Cloaking", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Cache Poisoning 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Cache Poisoning)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/cache/silver`
- **목표**: 프론트엔드 캐시 서버가 파라미터(`?q=...`)를 캐시 키에 포함(Keyed)시키지만, 백엔드 서버와의 파라미터 파싱 규칙 차이를 악용하는 **Parameter Cloaking (파라미터 은닉)** 기법을 사용하여 악성 스크립트가 담긴 페이지를 캐싱하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 파싱 로직 분석 (Reconnaissance)

`/cache/silver` 페이지는 URL의 파라미터를 읽어서 화면에 띄워주는 검색 기능입니다.

**[정상 요청 테스트 1]**
```http
GET /cache/silver?search=apple HTTP/1.1
```
➔ 서버 응답 화면: `Search results for: apple`
➔ 캐시 동작: 이 응답은 `/cache/silver?search=apple` 이라는 전체 URL을 키로 하여 캐시됩니다.

만약 여기에 악성 코드를 넣으면 어떻게 될까요?
`GET /cache/silver?search=<script>alert(1)</script>`
➔ 캐시 서버는 이 요청을 `search=<script>...` 라는 키로 저장합니다.
➔ 결과적으로 **나에게만 악성 코드가 캐시될 뿐**, `?search=apple`을 검색하는 정상적인 희생자에게는 아무 영향이 없습니다. (Poisoning 실패)

**[해커의 사고 과정]**
1. 캐시 서버가 파라미터 전체를 Key로 잡고 있기 때문에, 파라미터 안에 악성코드를 대놓고 넣으면 캐시 키가 달라져 버린다.
2. 하지만 캐시 서버(예: Varnish, Nginx)와 백엔드(예: Node.js, Ruby)가 여러 개의 파라미터를 읽어들이는 **구분자(Separator)** 인식 방식이 다르다면?
3. 흔히 쓰이는 구분자인 `&` 외에, 프레임워크에 따라 세미콜론(`;`)을 파라미터 구분자로 인정하는 경우가 있다.

---

## 💥 2. 취약점 식별 및 Parameter Cloaking 전략

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Malicious Header/Payload)--> [ Cache Server (Varnish) ] --> [ Web Server ]
                                             |-- Caches Malicious Response
[ Victim ]   --(Normal Request)------------> [ Cache Server ]
                                             |-- Returns Poisoned Cache!
```


이 취약점은 캐시 서버와 백엔드 서버 간의 **URL 파싱 불일치 (Parsing Discrepancy)** 에서 발생합니다.

### 💡 파라미터 은닉 (Cloaking) 테스트
세미콜론(`;`)을 사용하여 파라미터를 이어 붙여 봅니다.

**[테스트 요청]**
```http
GET /cache/silver?search=apple;search=hacked HTTP/1.1
```

**[해석의 차이]**
1. **프론트엔드 캐시 서버 (예: Varnish)**:
   - 캐시 서버는 오직 `&` 만을 파라미터 구분자로 인정합니다.
   - 따라서 이 요청의 파라미터는 `search` 한 개 뿐이며, 그 값은 `apple;search=hacked` 전체라고 생각합니다.
   - **캐시 키**: `/cache/silver?search=apple;search=hacked` (일반 유저의 검색어와 다르므로 공격 실패)

2. **우회 기법: URL 인코딩 불일치 활용**
   세미콜론 대신, 물음표(`?`) 자체의 인코딩 문제나, 프레임워크가 특정 파라미터(`utm_content`, `cb` 등)를 캐시 키에서 제외(Exclude)하도록 설정된 룰을 찾습니다.

이 챌린지에서는 캐시 서버가 마케팅 분석 파라미터인 **`utm_source` 를 캐시 키에서 강제로 제외(Unkeyed)**하도록 설정되어 있습니다.

---

## 🚀 3. 공격 수행 및 Cache Poisoning 연계

캐시 키에서 제외되는 `utm_source` 파라미터를 악용하여, 백엔드에는 두 번째 `search` 파라미터를 밀어 넣는(Cloaking) 방식을 설계합니다. 백엔드(Node.js 등)는 같은 이름의 파라미터가 2개 들어오면 **마지막 값**을 우선시합니다.

### 💡 페이로드 설계
**[조작된 페이로드]**
```http
GET /cache/silver?search=apple&utm_source=123&search=<script>alert('POISONED')</script> HTTP/1.1
Host: localhost:3000
```

### 🔍 서버 구조의 동작 흐름
1. **캐시 서버 (Varnish)**:
   - "어? URL에 `utm_source`가 있네. 이건 캐시 키에서 빼야 해."
   - 캐시 서버는 `&utm_source=...` 부터 그 뒤에 딸려오는 모든 문자열을 캐시 키 생성 규칙에서 누락하는 버그가 있습니다.
   - **생성된 캐시 키**: `/cache/silver?search=apple`
   - 이후 이 요청을 백엔드로 넘깁니다 (전체 문자열을 다 보냄).

2. **백엔드 (Node.js)**:
   - 넘어온 URL: `?search=apple&utm_source=123&search=<script>alert('POISONED')</script>`
   - "search 파라미터가 두 개네? 마지막 걸(악성 스크립트) 써야지."
   - 백엔드는 XSS 스크립트가 박힌 HTML을 생성하여 캐시 서버로 돌려줍니다.

3. **캐시 서버 저장**:
   - 캐시 서버는 방금 만든 **`/cache/silver?search=apple`** 이라는 지극히 정상적인 캐시 키에, 악성 응답을 60초 동안 저장합니다.

### 🔍 희생자의 접속 및 결과 확인
잠시 후 희생자(Admin)가 정상적인 사과 검색을 시도합니다.

```http
GET /cache/silver?search=apple HTTP/1.1
```

캐시 서버는 자신이 들고 있던 캐시(악성 응답)를 즉시 반환하며, 피해자의 브라우저에서 `alert('POISONED')` 가 실행됩니다!

```text
[!] System: Parameter Cloaking Cache Poisoning successful.
FLAG: FLAG{CACHE_🥈_PARAM_CLOAKING_F1A2B3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

보안을 위해 혹은 성능을 위해 특정 파라미터(`utm_*`)를 캐시 키에서 제외하는 설정이, 백엔드의 파라미터 덮어쓰기 특성과 결합되었을 때 완벽한 캐시 오염 공격으로 승화됨을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{CACHE_🥈_PARAM_CLOAKING_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
캐시 서버가 파라미터를 정규화(Normalization)하거나 제외할 때 사용하는 정규표현식이 엉성하여, 그 뒤에 따라오는 악의적인 파라미터까지 통째로 무시(Unkeyed)해버린 것이 원인입니다.

* **안전한 패치 가이드 (캐시 정규화 및 파라미터 검증)**
1. **정교한 캐시 제외 규칙 작성**: 캐시 서버(Varnish/CDN) 설정에서 특정 파라미터를 제외할 때, 그 파라미터 값만 정확히 도려내고 나머지 파라미터들은 캐시 키에 정상적으로 포함되도록 정규표현식을 엄격하게 수정해야 합니다.
2. **백엔드 파라미터 엄격화 (Parameter Pollution 방어)**: 백엔드 프레임워크가 동일한 이름의 파라미터가 2개 이상 들어올 때 마지막 것을 덮어쓰지 말고, 400 Bad Request 에러를 내거나 배열(Array)로 처리하도록 설정해야 합니다. (Node.js의 `hpp` 미들웨어 사용 등)
   ```javascript
   // Node.js Express 환경에서의 파라미터 오염 방지
   const hpp = require('hpp');
   app.use(hpp()); // 동일한 파라미터가 오면 마지막 값 하나만 남기지 않고 배열로 처리하거나 차단