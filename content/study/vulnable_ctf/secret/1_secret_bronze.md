+++
title = "VulnABLE CTF [LUXORA] Write-up: Secret Leakage 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Secret Leakage", "Bronze", "Hardcoded Credentials", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Secret Leakage 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Secret Leakage)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/secret/bronze`
- **목표**: 프론트엔드 자바스크립트 소스코드 내부에 개발자가 실수로 하드코딩(Hardcoding)해 둔 외부 API 연동 키(Secret Key)를 찾아내라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 동작 분석 (Reconnaissance)

`/secret/bronze` 페이지는 사용자가 배송지 주소를 입력하면, 외부 지도 API(Google Maps 등)를 호출하여 주소의 좌표를 화면에 표시해 주는 기능입니다.

**[해커의 사고 과정]**
1. 웹 브라우저에서 지도를 그리는 기능은 주로 프론트엔드(Client-Side) 자바스크립트에서 외부 API를 호출하여 처리한다.
2. 외부 API를 호출하려면 반드시 "API Key"가 필요하다.
3. 이 키를 백엔드에서 안전하게 숨겨서 요청을 대리 수행(Proxy)하지 않고, 만약 프론트엔드 자바스크립트 파일 안에 그대로 적어두었다면 누구나 읽을 수 있다!

---

## 💥 2. 취약점 식별 및 소스코드 분석 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(View Source)--> [ JS File / .map File ]
                                |-- API_KEY = "XYZ123"
                                |-- Extracted!
```


이 취약점은 가장 흔하고 단순한 형태의 **Hardcoded Credentials (하드코딩된 자격 증명)** 입니다.

### 💡 소스코드 열람
브라우저에서 `F12(개발자 도구)`를 열고 `Sources` 탭으로 이동하거나, 단순히 `Ctrl + U (페이지 소스 보기)`를 누릅니다. 페이지에서 로드하고 있는 자바스크립트 파일(`main.js` 또는 `map.js`)을 찾아 열어봅니다.

**[map.js 내용]**
```javascript
function loadMap(address) {
    // DO NOT COMMIT THIS KEY - Use Environment Variables instead!
    const GOOGLE_MAPS_API_KEY = "AIzaSyB-EXAMPLE-SECRET-KEY-A1B2C3D4";
    const SECRET_DEV_FLAG = "FLAG{SECRET_🥉_HARDCODED_JS_F1A2B3}";

    fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${GOOGLE_MAPS_API_KEY}`)
        .then(response => response.json())
        .then(data => {
            console.log("Map loaded!");
            // 렌더링 로직...
        });
}
```

---

## 🚀 3. 플래그 획득 및 권한 도용

개발자가 "커밋하지 마세요"라고 주석까지 달아놓았지만, 이미 브라우저로 전송된 자바스크립트 파일 안에 API 키와 플래그가 평문으로 떡하니 박혀있습니다.

해커는 이 `GOOGLE_MAPS_API_KEY`를 복사하여 자신의 웹사이트에서 마음대로 지도를 렌더링하는 데 사용하게 되며, 이로 인해 발생한 모든 트래픽 요금(Billing)은 LUXORA 플랫폼이 부담하게 됩니다. (이른바 API Key 탈취 및 과금 폭탄 공격)

---

## 🚩 4. 롸잇업 결론 및 플래그

가장 기초적이지만 가장 빈번하게 일어나는 실수인, 프론트엔드 코드 내 민감 정보 하드코딩 취약점을 확인했습니다.

**🔥 획득한 플래그:**
`FLAG{SECRET_🥉_HARDCODED_JS_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
브라우저로 전송되는 모든 HTML, CSS, JS 코드는 사용자(해커)가 100% 읽을 수 있습니다. 여기에 비밀번호나 비밀 키를 넣는 것은 대문에 집 열쇠를 붙여놓는 것과 같습니다.

* **안전한 패치 가이드 (Backend Proxy 및 제한된 키 사용)**
1. **백엔드를 통한 API 호출 (Backend Proxy)**:
   프론트엔드 자바스크립트는 타사 API(Google Maps)를 직접 호출하지 말고, 자사 백엔드 서버(`/api/get-map`)를 호출해야 합니다. 그러면 백엔드 서버가 환경변수(`.env`)에서 안전하게 숨겨진 API 키를 꺼내어 구글 서버와 통신한 뒤 결과만 프론트엔드로 내려줍니다.
2. **API 키 사용 제한 (HTTP Referer Restriction)**:
   부득이하게 프론트엔드에서 키를 써야 한다면(예: 지도 렌더링 등), 해당 API 발급 콘솔(구글 클라우드 플랫폼 등)에 들어가서 **"이 키는 `https://www.luxora.test` 도메인에서 온 요청만 승인한다"** 라고 IP 또는 Referer 제한을 강력하게 걸어두어야 합니다. 이렇게 하면 키가 유출되더라도 해커의 서버에서는 사용할 수 없습니다.