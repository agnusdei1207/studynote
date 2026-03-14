+++
title = "VulnABLE CTF [LUXORA] Write-up: XSS 🥈 Silver"
description = "LUXORA 플랫폼의 Silver 난이도 XSS 우회 기법 - 스크립트 태그 필터링 우회를 통한 Stored XSS 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "XSS", "Silver", "Stored XSS", "Filter Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: XSS 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (XSS)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/xss/silver`
- **목표**: 서버가 `<script>` 태그를 필터링하는 상황에서, HTML 이벤트 핸들러(Event Handler)를 이용한 **Stored XSS** 페이로드를 작성하여 필터를 우회하고 관리자의 브라우저에서 코드를 실행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 필터 반응 분석 (Reconnaissance)

`/xss/silver` 경로에는 사용자가 상품에 대한 "리뷰(Review)"를 남기고, 다른 사람들이 그 리뷰를 볼 수 있는 게시판 기능이 있습니다. 

리뷰 내용에 Bronze 단계에서 성공했던 `<script>alert('XSS')</script>` 를 입력하고 저장해봅니다.

**[서버의 응답 화면]**
```html
<div class="review">
  <p>User Review:</p>
  <p>[Blocked] Script tags are not allowed!</p>
</div>
```

**[해커의 사고 과정]**
1. 개발자가 Bronze의 해킹을 겪고 `<script>` 태그를 차단하는 정규식을 넣었다.
2. 하지만 자바스크립트를 실행하는 방법은 `<script>` 태그 하나만 있는 것이 아니다.
3. HTML 태그 속성으로 들어가는 **이벤트 핸들러(Event Handlers, 예: `onload`, `onerror`, `onmouseover`)**를 사용하면 `<script>` 단어 없이도 자바스크립트를 트리거(Trigger)할 수 있다!

---

## 💥 2. 필터링 우회 전략 (Bypass Strategy)

XSS 공격의 핵심은 브라우저가 사용자 입력을 '데이터'가 아닌 '실행 가능한 코드'로 착각하게 만드는 것입니다. 

### 💡 대표적인 이벤트 핸들러 우회 페이로드
1. **이미지 태그(`<img>`) 에러 유도**: 
   - 없는 이미지를 부르라고 시킨 뒤, 에러가 났을 때(`onerror`) 자바스크립트를 실행시킵니다.
   - ` <img src="x" onerror="alert('XSS')"> `
2. **SVG 태그 로드**:
   - ` <svg onload="alert('XSS')"> `
3. **링크 태그(`<a>`) 자바스크립트 스키마**:
   - 클릭을 유도하여 실행시킵니다.
   - ` <a href="javascript:alert('XSS')">Click Me!</a> `

여기서는 사용자의 상호작용(클릭 등) 없이도 페이지가 로드되자마자 즉시 실행되는 **`<img>` 태그 페이로드**를 선택하겠습니다.

---

## 🚀 3. 공격 수행 및 Stored XSS 익스플로잇 (Exploitation)

리뷰 입력 폼에 우회 페이로드를 입력하고 제출(Submit)합니다.

**[주입할 페이로드]**
```html
Great product! <img src="x" onerror="alert('XSS_SILVER_SUCCESS')">
```

### 🔍 서버의 응답 및 브라우저 렌더링
서버는 이 문자열에서 `<script>`를 찾지 못했으므로 "안전하다"고 판단하고 데이터베이스에 그대로 저장(Stored)합니다. 

잠시 후, 희생자(또는 챌린지 봇 관리자)가 이 리뷰 페이지를 열어봅니다.

```html
<!-- 희생자 브라우저에 렌더링된 HTML -->
<div class="review">
  <p>User Review:</p>
  <p>Great product! <img src="x" onerror="alert('XSS_SILVER_SUCCESS')"></p>
</div>
```

1. 브라우저는 `src="x"` 라는 이미지를 불러오려고 시도합니다.
2. 당연히 `x`라는 이미지는 없으므로 로드에 실패(Error)합니다.
3. 브라우저는 즉시 `onerror` 이벤트 핸들러에 적힌 `alert('XSS_SILVER_SUCCESS')` 자바스크립트를 실행합니다!

### 🚩 플래그 획득
관리자 봇의 브라우저에서 스크립트가 실행됨과 동시에, 시스템은 XSS 우회 성공을 인정하고 챌린지 플래그를 노출합니다.

```text
[!] System: Filter bypass detected. Stored XSS executed.
FLAG: FLAG{XSS_🥈_EVENT_HANDLER_B4C5D6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

블랙리스트 방식(`<script>` 차단)의 필터링은 수백 가지가 넘는 HTML 이벤트 핸들러 앞에서는 무용지물이 됨을 입증했습니다. 또한, 공격이 데이터베이스에 저장되는 **Stored XSS**의 특성상, 한 번만 주입해두면 해당 페이지를 방문하는 모든 사용자가 공격 대상이 되는 무서운 파급력을 가집니다.

**🔥 획득한 플래그:**
`FLAG{XSS_🥈_EVENT_HANDLER_B4C5D6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 원인은, 사용자 입력을 출력할 때 HTML 엔티티 인코딩(Entity Encoding)을 적용하지 않고 그대로 렌더링한 것입니다. 

* **안전한 패치 가이드 (HTML Entity Encoding 의무화)**
어떤 태그나 키워드를 막을지 고민할 필요가 없습니다. 서버에서 화면으로 값을 뿌려줄 때, HTML의 구조를 짤 수 있는 모든 꺾쇠(`<`, `>`)와 따옴표(`"`, `'`)를 무력화(Encoding)시켜야 합니다.

**[안전하게 렌더링된 결과 (목표)]**
```html
<!-- 브라우저가 이를 태그로 인식하지 않고, 문자 모양 그대로 텍스트로만 그려줌 -->
<p>Great product! &lt;img src=&quot;x&quot; onerror=&quot;alert(&#39;XSS&#39;)&quot;&gt;</p>
```

최신 프레임워크(React, Vue 등)는 이를 기본적으로 수행해 주므로, 개발자가 임의로 위험한 함수(예: React의 `dangerouslySetInnerHTML`, Vue의 `v-html`)를 사용하지 않는 것이 가장 중요합니다.