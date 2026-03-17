+++
title = "VulnABLE CTF [LUXORA] Write-up: Secret Leakage 🥈 Silver"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Secret Leakage", "Silver", "Source Map", "Webpack", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Secret Leakage 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Secret Leakage)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/secret/silver`
- **목표**: 프론트엔드 자바스크립트 파일이 난독화(Minified)되어 읽기 힘든 상황에서, 배포 시 실수로 남겨둔 **소스 맵(Source Map)** 파일을 찾아내어 원본 소스코드를 복원(Unpack)하고 그 안의 숨겨진 정보를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/secret/silver` 페이지에 접속한 뒤, 브라우저 개발자 도구(F12)의 Sources 탭을 확인합니다.
페이지는 `app.min.js` 라는 자바스크립트 파일을 로드하고 있습니다.

**[app.min.js 내용]**
```javascript
!function(e,t){"object"==typeof exports&&"object"==typeof module...console.log("App loaded!");...
```
코드가 완전히 압축되고 난독화(Obfuscation)되어 변수명은 모두 `a`, `b`, `c` 로 바뀌었고 구조를 파악하기가 거의 불가능합니다.

**[해커의 사고 과정]**
1. 현대의 웹(React, Vue 등)은 빌드 도구(Webpack, Vite)를 거치면서 코드를 압축(Minify)한다.
2. 하지만 디버깅을 위해 압축된 코드와 원본 코드를 연결해 주는 지도(Map) 역할을 하는 파일인 **`.map` 파일(Source Map)** 을 생성한다.
3. 개발자가 빌드 결과물을 서버에 올릴 때, 실수로 이 `.map` 파일까지 같이 올려버렸다면?
4. 자바스크립트 파일 맨 끝에 `//# sourceMappingURL=...` 주석이 있는지 확인하거나, 브라우저 주소창에 직접 `.map` 확장자를 쳐보자!

---

## 💥 2. 취약점 식별 및 소스코드 복원 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(View Source)--> [ JS File / .map File ]
                                |-- API_KEY = "XYZ123"
                                |-- Extracted!
```


`app.min.js` 파일의 URL을 확인한 후, 그 뒤에 `.map` 을 붙여서 요청해 봅니다.

**[소스 맵 요청]**
```http
GET /assets/js/app.min.js.map HTTP/1.1
Host: localhost:3000
```

### 💡 소스 맵 발견
서버가 404 에러를 뱉지 않고 거대한 JSON 덩어리를 반환합니다! 이 파일이 바로 Source Map 입니다.

### 💡 원본 소스코드 복원 (Unpacking)
이 JSON 파일을 직접 읽어도 되지만, `sourcemapper` (파이썬 도구)나 브라우저 개발자 도구의 자체 기능을 이용하면 원래의 폴더 구조와 소스코드를 완벽하게 복원할 수 있습니다.

```bash
# 터미널에서 Source Map 복원 도구 실행
$ npx source-map-unpacker https://localhost:3000/assets/js/app.min.js.map ./unpacked_source
```

---

## 🚀 3. 원본 코드 분석 및 플래그 획득

복원된 `./unpacked_source` 폴더를 열어보면, 압축되기 전의 깨끗한 구조가 나타납니다.
`src/components/`, `src/utils/` 등 개발자가 짠 원래 폴더 트리가 그대로 보입니다.

그 중 인증과 관련된 유틸리티 파일 `src/utils/auth.js` 를 열어봅니다.

**[복원된 src/utils/auth.js 내용]**
```javascript
import { encrypt } from 'crypto-utils';

export function loginAdmin(password) {
    // TODO: 백엔드 검증으로 옮길 것
    const ADMIN_FALLBACK_PASSWORD = "SuperSecretAdminFallback2023!";
    const INTERNAL_DEBUG_FLAG = "FLAG{SECRET_🥈_SOURCE_MAP_LEAK_D4E5F6}";

    if (password === ADMIN_FALLBACK_PASSWORD) {
        return true;
    }
    return false;
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

난독화(Minification)는 보안 메커니즘이 아니며, 소스 맵(`.map`) 파일이 대중에 노출되면 애플리케이션의 모든 지적 재산과 하드코딩된 내부 로직이 1초 만에 평문으로 역설계(Reverse Engineering)됨을 입증했습니다.

**🔥 획득한 플래그:**
`FLAG{SECRET_🥈_SOURCE_MAP_LEAK_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
빌드 스크립트(Webpack 등)의 기본 설정이 소스 맵 생성을 켜두고 있고, 배포 시 이를 제외하지 않았기 때문입니다.

* **안전한 패치 가이드 (빌드 및 배포 설정 수정)**
1. **프로덕션 빌드 시 Source Map 비활성화**:
   Webpack, Vite, Create React App 등의 설정에서 프로덕션(Production) 빌드 시에는 소스 맵이 생성되지 않도록 명시적으로 설정해야 합니다.
   ```javascript
   // vue.config.js 예시
   module.exports = {
       productionSourceMap: false
   }
   ```
2. **배포 필터링**:
   부득이하게 에러 트래킹(Sentry 등)을 위해 소스 맵을 만들어야 한다면, CI/CD 배포 스크립트(`rsync` 등)에서 `*.map` 파일이 Public 웹 디렉터리로 넘어가지 않도록 강력하게 제외(Exclude) 처리해야 합니다. 소스 맵은 오직 모니터링 도구 내부로만 안전하게 업로드되어야 합니다.