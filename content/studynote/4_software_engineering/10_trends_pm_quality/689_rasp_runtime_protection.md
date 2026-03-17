+++
title = "689. RASP 런타임 자체 보호"
date = "2026-03-15"
weight = 689
[extra]
categories = ["Software Engineering"]
tags = ["Security", "RASP", "Runtime Protection", "Self-Protection", "DevSecOps", "Zero Trust"]
+++

# 689. RASP 런타임 자체 보호

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: WAF(Web Application Firewall)의 한계를 극복하기 위해 애플리케이션 **런타임(Runtime) 환경 내부에 보안 로직을 삽입하여**, 실행 코드의 맥락(Context)을 실시간으로 분석하고 차단하는 **자가 보호(Self-Protection) 기술**.
> 2. **가치**: 네트워크 트래픽 패턴이 아닌 **실제 실행 흐름(Execution Flow)과 데이터 의미**를 분석하므로, 오탐(False Positive)을 획기적으로 줄이고 암호화된 트래픽 내의 공격(Injection, Logic Flaw)을 정밀하게 탐지.
> 3. **융합**: 패치가 불가능한 레거시 시스템에 대한 **가상 패칭(Virtual Patching)** 솔루션으로 활용되며, **제로 트러스트(Zero Trust)** 아키텍처의 애플리케이션 계층 최종 방어선 구현.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**RASP (Runtime Application Self-Protection, 런타임 애플리케이션 자가 보호)**는 애플리케이션이 실행되는 동안 해당 환경(예: JVM, CLR)에 직접 개입하여 보안 기능을 수행하는 기술입니다. 기존의 보안 장비가 애플리케이션 외부에서 트래픽을 관찰하는 것과 달리, RASP는 애플리케이션 프로세스 내부에서 함수 호출, 라이브러리 사용, 네트워크 소켓 및 데이터베이스 쿼리 등을 모니터링합니다.

#### 2. 등장 배경: 경계 보안의 붕괴와 런타임 보안의 필요성
전통적인 보안은 **네트워크 경계(Network Perimeter)**를 지키는 데 집중했습니다. 하지만 클라우드 컴퓨팅의 도입과 엔터프라이즈 경계의 모호해짐에 따라, 공격자는 방화벽 우회, 암호화 트래픽(SSL/TLS) 악용, 복잡한 HTTP 파라미터 조작 등을 통해 내부로 침투할 수 있게 되었습니다. 특히 **SQL Injection (SQLi)**이나 **XSS (Cross-Site Scripting)**와 같은 공격은 정상적인 HTTP 요청으로 위장하므로, 페이로드의 '형식'만 보는 WAF로는 완벽한 탐지가 불가능했습니다. 이에 따라 애플리케이션이 스스로 자신의 상태를 진단하고 보호하는 **RASP** 기술이 Gartner에 의해 제안되고 도입되기 시작했습니다.

#### 3. 작동 배경: 신뢰할 수 있는 실행 환경 (Trusted Execution)
RASP는 보안 에이전트가 애플리케이션과 **동일한 메모리 공간**을 공유하거나, 런타임에 **Hooking(후킹)** 기술을 통해 API 호출을 가로챕니다. 이를 통해 "이 데이터가 실제로 데이터베이스 쿼리문으로 조합되어 실행되려 하는가?"와 같은 실행 맥락(Context)을 파악할 수 있어, 외부 공격과 내부의 정상적인 로직을 명확히 구분할 수 있습니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        보안 관점의 패러다임 변화                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1세대] 네트워크 방화벽 (Firewall)                                          │
│   → "IP와 포트를 막는다" (접근 제어)                                         │
│                                                                             │
│  [2세대] 웹 방화벽 (WAF)                                                     │
│   → "패킷의 내용(Payload)을 검사한다" (시그니처 기반, 외부 관찰)              │
│   → 한계: 암호화 통신 복호화 비용, 오탐(False Positive), 우회 공격           │
│                                                                             │
│  [3세대] 런타임 자가 보호 (RASP)  ★                                          │
│   → "코드가 실행되는 순간을 감시한다" (내부 관찰, 맥락 기반)                  │
│   → 장점: 암호화 트래픽 무관, 비즈니스 로직 이해, 정밀 차단                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **📢 섹션 요약 비유**: RASP의 도입은 마치 성벽(방화벽)과 입구 검문대(WAF)만 믿던 고성 요새에, 성 안의 왕을 직접 호위하는 **"근위대(Secret Service)"**를 배치하는 것과 같습니다. 적이 성문을 몰래 통과하더라도 왕의 옆에 있는 근위대가 칼을 빼들려는 순간 그 팔을 비틀어 제지하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 (Modules)

| 요소명 | 역할 | 내부 동작 메커니즘 | 주요 프로토콜/기술 | 비유 |
|:---:|:---|:---|:---|:---|
| **Instrumentation Agent** | 런타임 개입 및 코드 삽입 | JVM(Java Virtual Machine) 로드 시 `javaagent` 또는 OS의 `ptrace` 시스템 콜을 사용하여 타겟 애플리케이션의 메모리 공간에 탑재됨. | JVM TI, JNI, .NET Profiling API | 몸에 붙는 센서 |
| **Hooking Engine** | 시스템 호출 및 라이브러리 함수 가로채기 | `strcpy`, `sprintf`, `JDBC.executeQuery` 등의 취약한 함수 주소를 RASP의 검사 루틴 주소로 변경(Runtime Redirecting). | Dynamic Binary Instrumentation (DBI) | 도청 장치 |
| **Context Analyzer** | 실행 맥락 및 데이터 의미 분석 | 콜 스택(Call Stack)을 추적하여 현재 요청이 인증된 세션인지, 관리자 권한인지, 비즈니스 로직상 정상적인 흐름인지 판단. | Stack Walking, Taint Analysis (오염 분석) | 데이터 분석관 |
| **Security Policy Engine** | 차단/허용/로깅 결정 | 사전에 정의된 룰셋(Rule-based) 또는 ML 모델을 통해 현재 행위가 공격 패턴(SQLi, XSS, Path Traversal 등)에 부합하는지 계산. | Regex, Bayesian Filter, Decision Tree | 심판관 |
| **Blocking/Action Module** | 즉각적인 대응 수행 | 공격으로 판단되면 예외(Exception)를 발생시켜 트랜잭션을 강제 종료하거나, 가짜 에러 페이지를 반환하여 공격자를 교란함. | Exception Throwing, HTTP 403/500 | 제압반 |

#### 2. 아키텍처 및 데이터 흐름도

```text
      ┌─────────────────────────────────────────────────────────────────┐
      │                    Attack Vector (Attacker)                     │
      └───────────────────────────────┬─────────────────────────────────┘
                                      │ 1. Malicious Payload (e.g., "' OR 1=1 --")
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           [ Traditional Boundary ]                          │
│  ┌─────────────────┐    ┌─────────────────┐                               │
│  │  WAF / IPS      │    │  Load Balancer  │                               │
│  │  (External)     │    │  (SSL Offload)  │                               │
│  └───────┬─────────┘    └─────────────────┘                               │
│          │ (May Miss Encrypted/Polyglot attacks)                          │
└──────────┼─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Application Server (Runtime)                            │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  User Application Thread (e.g., Apache Tomcat)                       │ │
│  │                                                                       │ │
│  │   [Controller] ──▶ [Service] ──▶ [DAO]                                │ │
│  │        │              │             │                                │ │
│  │        │              │             ▼                                │ │
│  │        │              │        ┌──────────────────┐                  │ │
│  │        │              │        │  DB Connection   │                  │ │
│  │        │              │        └────────┬─────────┘                  │ │
│  │        │              │                 │                            │ │
│  │        │     ┌────────▼─────────────────▼───────────┐                │ │
│  │        │     │         RASP Agent (Hooking)          │                │ │
│  │        │     │  ┌─────────────────────────────────┐  │                │ │
│  │        │     │  │  1. Intercept SQL Execution     │  │                │ │
│  │        │     │  │  2. Analyze Input + Context     │  │                │ │
│  │        │     │  │  3. Compare Policy (SQLi Rule)  │  │                │ │
│  │        │     │  └───────────────┬─────────────────┘  │                │ │
│  │        │     │                  │                    │                │ │
│  │        │     │          ┌───────▼───────┐           │                │ │
│  │        │     │          │   Decision?   │           │                │ │
│  │        │     │          └───────┬───────┘           │                │ │
│  │        │     │                  │                    │                │ │
│  │        │     │     ┌────────────┼────────────┐       │                │ │
│  │        │     │     ▼            ▼            ▼       │                │ │
│  │        │     │  [Allow]    [Block]      [Log]       │                │ │
│  │        │     │     │            │            │       │                │ │
│  │        │     ▼     ▼            ▼            │       │                │ │
│  │        │  [Execute] [Throw Exception]         │       │                │ │
│  └────────┼──────────────────────────────────────┼───────┘                │ │
│           │                                      │                        │
└───────────┼──────────────────────────────────────┼─────────────────────────┘
            │                                      │
            ▼                                      ▼
     [Normal Response]                     [Security Alert / 403]
```

#### 3. 심층 기술 원리: 훅(Hook)과 섀도우 스택(Shadow Stack)

RASP의 핵심은 **API Hooking**과 **Taint Analysis(데이터 오염 분석)**입니다.
1.  **Hooking Mechanism**: RASP 에이전트는 애플리케이션 시작 시 `premain` (Java) 또는 `DllMain` (C#) 진입점을 통해 로드됩니다. 이후 **JVM Tool Interface (JVM TI)** 또는 **Detours** 라이브러리를 사용하여, 보안상 취감한 함수(예: `java.lang.Runtime.exec`, `System.IO.File.Open`, `java.sql.Statement.execute`)의 시작 주소를 `NOP` 명령으로 비활성화하고, 자신의 검사 루틴(JMP) 주소로 덮어씁니다.
2.  **Taint Analysis**: 사용자 입력(Request Parameter)을 메모리에 'Taint(오염)' 플래그와 함께 저장합니다. 이 데이터가 복사되거나 변형될 때 플래그를 추적(Propagation)하다가, 만약 'Taint'가 된 데이터가 SQL 쿼리 생성이나 시스템 명령어 실행에 사용되려 하면 즉시 위협으로 간주합니다.

```c
// [Pseudo Code: RASP Hooking Logic inside Runtime]
original_function_execute(query) {
    // 1. Check Taint Flag
    if (query.is_tainted) {
        
        // 2. Check Context (Is this a safe stored procedure?)
        if (!query.is_whitelisted_stored_procedure) {
            
            // 3. Syntax Check (SQL Injection heuristic)
            if (contains_sql_meta_chars(query)) {
                RASP_Block("SQL Injection Detected", query.get_stack_trace());
                return;
            }
        }
    }
    
    // 4. If safe, proceed to original execution
    return execute_original(query);
}
```

> **📢 섹션 요약 비유**: RASP의 동작 원리는 마치 **"현금 수송 차량의 도어 잠금 장치"**와 같습니다. 운전자(애플리케이션)가 문을 열려고 하면, 잠금 장치(RASP)가 "이곳이 정상적인 은행입니까?", "운전자가 인가된 사람입니까?"를 0.01초 만에 판단하여, 조금이라도 의심스러우면 도어를 물리적으로 잠가버리는 방식입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. WAF vs RASP vs IAST 기술적 비교 분석

| 비교 항목 | WAF (Web App Firewall) | RASP (Runtime App Self-Protection) | IAST (Interactive App Security Testing) |
|:---:|:---|:---|:---|
| **위치 (Position)** | **Network Edge** (Reverse Proxy) | **Runtime Process** (In-Process) | **Build/Test Phase** (Agent in QA Env) |
| **관점 (View)** | 외부 트래픽 (Black-box) | 내부 실행 흐름 (White-box) | 내부 실행 흐름 (White-box) |
| **차단 여부** | 차단 가능 (Inline) | **차단 가능 (Inline)** | 차단 불가 (탐지만 가능, Test용) |
| **성능 영향** | 미미 (네트워크 지연) | **중간~높음 (CPU/메모리 사용)** | 높음 (테스트 시에만) |
| **False Positive** | 높음 (정상 트래픽 오인) | **낮음 (맥락 인지)** | N/A (테스트 결과물) |
| **운영 부하** | 룰셋(Ruleset) 관리 | 에이전트 버전 관리, 정책 튜닝 | 개발자 리소스 소모 |
| **주요 용도** | DoS 방어, 간단한 필터링 | **논리적 결함 방어, 제로데이 방어** | 개발 단계 취약점 찾기 |

#### 2. 다각도 분석: WAF와의 시너지
RASP는 WAF를 완전히 대체하기보다 **Defensive Depth (심층 방어)** 차원에서 상호 보완적으로 사용됩니다.
- **WAF**: "쓸데없는 트래픽을 미리 거르고 RASP의 부하를 줄여주는 **1차 방패**" 역할. Bulk DDoS 공격 등을 여기서 처리.
- **RASP**: "WAF를 뚫고 들어온 정교한 공격을 막아내는 **핵심 수비수**" 역할. 애플리케이션 로직에 직접적인 위협만 선별