+++
title = "688. SAST / DAST / IAST 보안 테스팅 도구 비교"
date = "2026-03-15"
weight = 688
[extra]
categories = ["Software Engineering"]
tags = ["Security", "Testing", "SAST", "DAST", "IAST", "DevSecOps", "Vulnerability"]
+++

# 688. SAST / DAST / IAST 보안 테스팅 도구 비교

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 애플리케이션 보안 취약점을 탐지하기 위한 자동화 기법군으로, **SAST (Static Application Security Testing)**, **DAST (Dynamic Application Security Testing)**, **IAST (Interactive Application Security Testing)**로 분류된다.
> 2. **차별점**: **SAST**는 소스코드를 정적 분석하여 '잠재적 결함'을, **DAST**는 실행 중인 애플리케이션에 공격 페이로드를 주입하여 '실제 표출 취약점'을, **IAST**는 런타임 에이전트를 통해 코드와 실행 데이터를 Correlation(상관분석)하여 '낮은 오탐율의 정확한 결함'을 탐지한다.
> 3. **실무 가치**: CI/CD (Continuous Integration/Continuous Deployment) 파이프라인에 **Shift-Left** 전략을 구현하여, 배포 이전 단계에서 보안 수정 비용을 획기적으로 절감하고 **DevSecOps** 문화를 정착시키는 핵심 인프라다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
애플리케이션 보안 테스팅은 소프트웨어 개발 수명 주기(SDLC) 동안 소스코드, 바이너리, 실행 환경 내에 존재하는 보안 허점을 식별 및 완화하는 기술적 활동이다. 전통적인 소프트웨어 개발에서 보안은 개발 완료 후 별도의 전문가(보안 팀)가 수행하는 '모의해킹'이나 '코드 리뷰'에 의존했다. 그러나 애자일(Agile) 및 데브옵스(DevOps) 환경으로 전환됨에 따라, 수동 검사로는 빠른 릴리즈 주기를 따라잡을 수 없게 되었다. 이에 **SAST**, **DAST**, **IAST**와 같은 자동화된 보안 테스팅 도구가 등장하였으며, 이는 개발 단계에서부터 운영 단계까지 지속적인 보안 검증을 가능하게 한다.

#### 2. 등장 배경 및 패러다임 변화
- **① 기존 한계 (Waterfall & Manual Testing)**: 개발末期에 보안을 진행하면 결함 수정을 위한 코드 재작성(Cost of Change)이 기하급수적으로 증가한다. (Boehm's Curve)
- **② 혁신적 패러다임 (Shift-Left)**: 보안 검사 시점을 개발 초기(왼쪽)로 이동시켜, 피드백 루프를 단축하고 개발자가 직접 보안 품질을 관리하게 한다.
- **③ 현재의 비즈니스 요구 (DevSecOps)**: '속도'와 '안전'의 트레이드오프가 아닌, 자동화를 통해 둘을 동시에 달성하는 것이 기업 생존의 핵심 과제가 되었다.

```text
   [ Boehm's Cost of Change Curve 보안 수정 비용 ]
   
   Cost ($)
      ^
      |                                         / (운영 중 발견: 막대한 비용)
      |                                        /
      |                                       /
      |                    /----------------/ (QA 단계 발견: 높은 비용)
      |                   /
      |          /------/------------------- (커밋 시점 발견: 낮은 비용)
      |         /
      |--------/----------------------------▶ Time
       Design  Code   Test   Deploy
       
      => Shift-Left: SAST/SCA를 Code 단계에 배치하여 비용 최소화
```

#### 3. 💡 핵심 비유: 건물의 안전 진단
보안 테스팅 도구들은 건물을 지을 때 안전을 확보하는 방법과 유사하다.
- **SAST**는 건물을 짓기 전 **설계도면**을 보고 "여기 내력벽이 빠졌네?"라고 미리 확인하는 작업이다.
- **DAST**는 건물을 다 지은 뒤 문을 쾅 쾅 부수고 들어가며 **실제 물리적 허점**을 찾는 작업이다.
- **IAST**는 공사 중 자재 안에 **센서(에이전트)**를 심어두고, 건물이 무너질 때 어느 부재가 어느 순간에 부러졌는지 실시간으로 분석하는 작업이다.

#### 📢 섹션 요약 비유
"마치 자동차 생산 라인에서, 설계 단계에서 도면을 검토(SAST)하고, 시주 주행 테스트 중 센서를 부착하여 충격량을 측정(IAST)하며, 최종적으로 충돌 테스트를 실시(DAST)하여 안전성을 3중으로 검증하는 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 상세 기술 비교 (Depth Architecture)

| 구분 | SAST (Static) | DAST (Dynamic) | IAST (Interactive) |
|:---:|:---|:---|:---|
| **Full Name** | **Static Application Security Testing** | **Dynamic Application Security Testing** | **Interactive Application Security Testing** |
| **분석 대상** | 소스코드(Source Code), 바이너리(Bytecode) | 실행 중인 애플리케이션(Running Instance) | 소스코드 + 런타임 메모리/실행 흐름 |
| **접근 방식** | **White-box** (내부 구조 노출) | **Black-box** (외부 공격자 관점) | **Hybrid** (내부/외부 정보 융합) |
| **탐지 메커니즘** | AST(Abstract Syntax Tree) 기반 패턴 매칭, 데이터 플로우 분석(Taint Analysis) | Fuzzing, HTTP Proxy 기반 페이로드 삽입 및 응답 분석 | Instrumentation을 통해 함수 호출 및 데이터 흐름 실시간 추적 |
| **진단 시점** | 코딩(Coding) 및 빌드(Build) 단계 | QA 또는 Staging/Production 단계 | QA 및 Staging 단계 (에이전트 설치 필요) |
| **오탐(False Positive)** | 높음 (실행 문맥을 알 수 없음) | 낮음 (실제 응답 오류를 기반) | 매우 낮음 (실제 실행 확인 + 코드 라인 정확히 매핑) |
| **미탐(False Negative)** | 중간 (논리적 오류나 환경 의존성 취약점 누락 가능) | 높음 (인증 필요 페이지나 복잡한 로직 탐색 한계) | 낮음 (실제 실행되는 경로만 확인하므로 신뢰도 높음) |
| **대표 도구** | SonarQube, Checkmarx, Fortify, Snyk | OWASP ZAP, Burp Suite, AppScan | Contrast Security, Seeker, Veracode IAST |

#### 2. SAST (Static) 심층 동작 원리
SAST는 컴파일러의 기술을 기반으로 한다. 소스코드를 토큰(Token)으로 분해하고 추상 구문 트리(AST)를 생성한 뒤, 미리 정의된 보안 규칙(Ruleset)과 비교한다. 고급 분석의 경우 'Taint Analysis'(오염 분석)를 수행한다. 예를 들어, 사용자 입력(HttpServletRequest.getParameter)이 'Tainted(오염)' 상태로 표시되고, 이것이 sanitizer(정제 과정)를 거치지 않고 SQL 실행문으로 흐르는 경로를 찾아내면 'SQL Injection'을 보고한다.

```text
 [ SAST Data Flow Analysis Example ]
 
 1. Source (오염원)
    String userId = request.getParameter("id");  <-- [Tainted]
    
 2. Through (데이터 흐름)
    ...
    String query = "SELECT * FROM users WHERE id = " + userId;
    
 3. Sink (취약한 싱크)
    statement.execute(query); <--- [Alert: SQL Injection Risk]
    
 => 코드를 실행하지 않고 이 그래프 경로를 분석하여 탐지
```

#### 3. IAST (Interactive) 심층 동작 원리
IAST는 **WASP(White and Black Security Proxy)** 혹은 **Agent** 방식을 사용한다. 애플리케이션이 실행될 때 JVM(Java Virtual Machine)이나 CLR(Common Language Runtime) 수준에서 코드가 해석되는 지점(Instrumentation)에 후킹(Hooking) 코드를 삽입한다.
- **동작 과정**: DAST 도구(또는 QA 테스터)가 요청을 보내면 → IAST 에이전트가 해당 요청을 가로채어(Capture) → 입력값이 처리되는 과정을 메모리에서 모니터링 → 취약한 라이브러리 함수 사용 혹은 미검증 입력 처리가 발생하는 즉시 해당 라인 번호와 스택 트레이스를 보고한다.

```text
   [ IAST Hybrid Architecture ]
   
      [QA Tester / DAST Crawler]
             │  (1) HTTP Request
             ▼
   +--------------------------------------------------+
   │  Application Server (Tomcat/Node.js/etc)        │
   │                                                  │
   │  +------------------+------------------------+  │
   │  │  App Logic       │   IAST Agent (Sensor)  │  │
   │  │                  │                        │  │
   │  │  void login() {  │   [Hook] Validate()    │  │
   │  │     ...          │   [Hook] query.exec()  │  │
   │  │  }               │   (2) Monitor Stack    │  │
   │  +------------------+------------------------+  │
   │          │                     │               │
   │          │ (3) Local Inter-Process/Method Call │
   +----------|-------------------------------------+
              │
              ▼
       (4) Real-time Console Feedback (Exact Line #, False Positive Free)
```

#### 📢 섹션 요약 비유
"SAST는 건물의 설계도면을 눈으로 검토하는 것이라면, IAST는 건물의 기둥 안에 진동 센서를 매달아두고 사람이 다닐 때마다 실시간으로 안전 여부를 판단하는 것과 같습니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 정량적/정성적 융합 비교 분석

| 평가 기준 | SAST (Static) | DAST (Dynamic) | IAST (Interactive) |
|:---:|:---:|:---:|:---:|
| **속도 (Speed)** | ⭐⭐⭐⭐⭐ (초당 수천 라인) | ⭐⭐ (크롤링 및 공격 시간 소요) | ⭐⭐⭐ (런타임 오버헤드 존재) |
| **정확도 (Accuracy)** | ⭐⭐ (오탐 다수) | ⭐⭐⭐ (실제 익스플로잇 가능) | ⭐⭐⭐⭐⭐ (매우 높음) |
| **설치 난이도** | ⭐⭐⭐⭐ (CI 연동 용이) | ⭐⭐⭐ (인증/환경 설정 필요) | ⭐ (에이전트/환경 종속적) |
| **DevSecOps 적합성** | 개발 단계(Shift-Left) 핵심 | 배포 전/Gatekeeper 역할 | QA 단계 품질 보증(QA) |
| **비용 (TCO)** | 도구 라이선스 비용 주도 | 전문가 운영 인건비 포함 | 도구 + 에이전트 관리 비용 |

#### 2. 과목 융합 관점: OS/네트워크/DB와의 시너지

- **A. OS (Operating System)와의 관계**:
  - **DAST**는 OS 레벨의 소켓(Socket) 통신을 조작하여 패킷을 재작성(Replay)하거나 비정상적인 패킷(Fragmented Packet 등)을 전송하여 시스템 안정성을 테스트한다.
  - **IAST** 에이전트는 OS의 시스템 콜(System Call)이나 라이브러리 호출(LoadLibrary)을 가로채기 위해 **ptrace**나 **JVMTI(JVM Tool Interface)**와 같은 OS/Kernel 단계의 디버깅 인터페이스를 활용한다.

- **B. 네트워크(Network)와의 관계**:
  - **DAST**는 **WAF(Web Application Firewall)**의 우회 여부를 테스트한다. 즉, 네트워크 계층에서 필터링하는 패턴을 우회하여 애플리케이션 로직까지 침투 가능한지 검증한다.
  - HTTP 프로토콜의 헤더(Header), 바디(Body), 쿠키(Cookie) 등을 변조하여 입력 검증 로직의 격차를 찾는다.

- **C. DB (Database)와의 관계**:
  - **SAST**의 가장 중요한 타겟은 **SQL Injection**이다. ORM(Object-Relational Mapping)을 사용하더라도 잘못된 동적 쿼리 생성을 탐지하기 위해 데이터베이스 드라이버 호출 패턴을 분석한다.
  - **NoSQL Injection** 같은 신종 공격 탐지를 위해 각 DB 벤더별 API 호출 패턴을 내부적으로 룰화(Rule-based)한다.

#### 📢 섹션 요약 비유
"SAST는 건강검진 설문지(예방), DAST는 실제 수술 전 진단(확인), IAST는 수술 중 모니터링 장치(실시간 관찰)와 같아서, 이 셋을 합쳐야 환자(애플리케이션)의 생명을 온전히 지킬 수 있습니다."

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 대규모 금융 서비스 CI/CD 파이프라인 설계
대규모 금융권 서비스는 보안과 가용성이 모두 중요하다. 단일 도구로는 부족하며, 단계별로 적합한 도구를 배치하는 전략이 필요하다.

**의사결정 프로세스:**
1. **개발자 로컬 환경 (Pre-commit)**:
   - **전략**: **Linter** 형태의 가벼운 SAST 도구 배치.
   - **이유**: 커밋 전에 개발자가 즉시 수정 가능한 단순 실수(Coding Standard) 수정.
2. **빌드 서버 (Build/CI Phase)**:
   - **전략**: 정밀 **SAST** 및 **SCA(Software Composition Analysis)** 수행.
   - **판단**: 오픈소스 라이브러리 취약점(CVE)을 확인하고, 핵심 모듈에 대한 정적 분석을 수행. 이때 발생하는 오탐(False Positive)을 관리하기 위해 '보안 규칙 튜닝'이 필수적이다.
3. **QA 및 Staging 환경 (Test Phase)**:
   - **전략**: **IAST** 에이전트 탑재 및 기능 테스트 병행.
   - **판단**: QA 팀이 별도의 보안 테스트 없이 기능 테스트만 수행해도, 백그라운드에서 보안 취약점이 수집되도록 하