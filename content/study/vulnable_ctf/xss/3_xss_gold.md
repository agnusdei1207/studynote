+++
title = "VulnABLE CTF [LUXORA] Write-up: XSS 🥇 Gold"
description = "LUXORA 플랫폼의 Gold 난이도 DOM-based XSS 취약점 분석 및 클라이언트 사이드 자바스크립트 흐름 추적 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XSS", "Gold", "DOM XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XSS 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (XSS)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/xss/gold`
- **목표**: 서버 사이드에서 HTML 인코딩이 완벽하게 적용되어 Reflected/Stored XSS가 불가능한 환경에서, 브라우저에서 동작하는 클라이언트 사이드 자바스크립트의 결함(Source to Sink)을 찾아 **DOM-based XSS**를 성공시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/xss/gold#welcome` 경로에 접속하면 화면에 "Hello, welcome!" 이라는 글씨가 뜹니다.
URL의 해시(Hash, `#`) 뒤에 오는 문자열을 바꾸어 봅니다.

* `http://localhost:3000/xss/gold#hacker` ➔ 화면 출력: `Hello, hacker!`

**[서버 응답 확인]**
Burp Suite나 네트워크 탭을 열어 서버에서 받아온 원본 HTML 소스를 확인해 봅니다.

```html
<!-- 서버가 보내준 원본 HTML 소스 -->
<div id="greeting">Hello, </div>
<script>
  // 클라이언트 브라우저에서 실행되는 자바스크립트
  var hashValue = window.location.hash.substring(1);
  if (hashValue) {
      document.getElementById('greeting').innerHTML += decodeURIComponent(hashValue);
  }
</script>
```

**[해커의 사고 과정]**
1. 이 페이지는 서버가 나의 입력값(`hacker`)을 HTML에 박아서 내려주지 않는다.
2. 서버가 내려준 순수 HTML(뼈대)을 브라우저가 먼저 그리고 난 뒤, 브라우저 안에서 돌아가는 자바스크립트가 URL의 `#` 뒷부분을 읽어와서 화면(`innerHTML`)에 동적으로 끼워 넣고 있다.
3. 그렇다면 서버의 필터링이나 WAF는 아무 소용이 없다. 이 공격은 오직 내 브라우저 안에서만 일어나는 **DOM-based XSS**다!

---

## 💥 2. 취약점 식별 및 데이터 흐름(Data Flow) 분석

DOM XSS를 찾기 위해서는 두 가지 요소를 파악해야 합니다.
* **Source (입력원)**: 악성 데이터가 들어오는 곳. 여기서는 `window.location.hash` 입니다.
* **Sink (실행점)**: 그 데이터가 실행되거나 렌더링되는 위험한 함수. 여기서는 `innerHTML` 입니다.

`innerHTML`은 전달받은 문자열을 HTML 태그로 해석해서 브라우저 DOM 트리에 꽂아버리는 아주 강력하고 위험한 Sink입니다.

---

## 🚀 3. 공격 수행 및 DOM XSS 익스플로잇 (Exploitation)

`innerHTML`은 `<script>` 태그를 직접 넣으면 보안상 실행하지 않도록 최신 브라우저들이 막아두었습니다. 따라서 Silver 난이도에서 썼던 이벤트 핸들러(Event Handler) 우회 기법을 다시 사용합니다.

### 💡 페이로드 작성
```html
<img src="x" onerror="alert('DOM_XSS_SUCCESS')">
```

이 문자열을 URL의 해시(`#`) 뒤에 붙입니다. (서버로 전송되지 않으므로 URL 인코딩은 브라우저에 따라 선택 사항이지만, 스크립트의 `decodeURIComponent`가 있으므로 인코딩해도 풀립니다.)

### 페이로드 적용 (브라우저 주소창 입력)
```text
http://localhost:3000/xss/gold#<img src="x" onerror="alert('DOM_XSS_SUCCESS')">
```

### 🔍 클라이언트 내부의 반응
1. 브라우저가 `window.location.hash` 에서 `#<img src="x"...>` 를 읽어옵니다.
2. `#`을 떼어내고 `innerHTML` 에 문자열을 할당합니다.
3. DOM 트리가 즉시 업데이트되면서 `<img>` 태그가 생성되고, 이미지 로드에 실패하여 `onerror` 속성의 자바스크립트가 실행됩니다!

### 🚩 플래그 획득
브라우저 한가운데 경고창이 뜨면서 챌린지 성공 로그가 뜹니다.

```text
[!] System: DOM-based XSS executed.
FLAG: FLAG{XSS_🥇_DOM_BASED_INNERHTML_D7E8F9}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

서버가 아무리 입력값을 깐깐하게 검증하고 HTML 인코딩을 하더라도, 프론트엔드 자바스크립트(SPA, React, Vue 등) 단에서 데이터를 다루는 함수를 잘못 사용하면 치명적인 XSS가 발생함을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{XSS_🥇_DOM_BASED_INNERHTML_D7E8F9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
사용자로부터 가져온 데이터(URL, 쿠키, LocalStorage 등)를 DOM 트리에 꽂아 넣을 때, 텍스트가 아닌 'HTML 구조'로 해석되게끔 허용한 것이 원인입니다.

* **안전한 패치 가이드 (안전한 Sink 사용)**
자바스크립트에서 DOM을 조작할 때, 특별한 이유가 없다면 `innerHTML`을 절대로 사용하지 마세요. 대신 입력값을 오직 순수한 텍스트로만 취급하는 `innerText` 나 `textContent` 속성을 사용해야 합니다.

```javascript
// 취약한 방식 (HTML로 해석됨)
document.getElementById('greeting').innerHTML = userInput;

// 안전한 방식 (HTML 태그가 와도 그냥 문자열로 화면에 출력됨)
document.getElementById('greeting').textContent = userInput;
```

만약 부득이하게 HTML을 렌더링해야 한다면(예: 마크다운 에디터), 반드시 클라이언트 사이드 XSS 필터 라이브러리(예: `DOMPurify`)를 통과시킨 후 안전한 HTML만 삽입해야 합니다.
```javascript
// DOMPurify를 이용한 안전한 삽입
document.getElementById('greeting').innerHTML = DOMPurify.sanitize(userInput);
```