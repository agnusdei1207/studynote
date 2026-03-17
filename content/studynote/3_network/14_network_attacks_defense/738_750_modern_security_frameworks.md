+++
title = "738-750. 현대 보안 프레임워크 (Zero Trust, SASE, SOAR)"
date = "2026-03-14"
[extra]
category = "Network Security"
id = 738
+++

# 738-750. 현대 보안 프레임워크 (Zero Trust, SASE, SOAR)

## # [현대 보안 프레임워크]
### 핵심 인사이트 (3줄 요약)
> 1. **본질**: "신뢰할 수 있는 네트워크 경계"라는 전제를 폐기하고, `ZTNA (Zero Trust Network Access)`를 기반으로 사용자, 디바이스, 데이터의 상태를 실시간으로 검증하는 'Identity-Based Security'로 패러다임이 전환됨.
> 2. **가치**: `SASE (Secure Access Service Edge)`를 통해 네트워크(전송)와 보안(검사)을 클라우드 엣지(Edge)로 통합하여, 글로벌 라텐시를 50% 이상 절감하고 온프레미스 장비 구축 비용(CAPEX)을 획기적으로 절감.
> 3. **융합**: `SOAR (Security Orchestration, Automation and Response)`가 `SIEM (Security Information and Event Management)` 및 `AI (Artificial Intelligence)`와 결합하여 대응 시간(MTTD/MTTR)을 분 단위로 단축하고, 인간 보안 전문가의 피로도를 해소하는 자율 방어 체계를 구현.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 정의 및 철학
현대 보안 프레임워크는 기존의 **城堡(Castle-and-Moat)** 방식, 즉 내부는 안전하고 외부는 위험하다는 이분법적 사고를 완전히 배제한다. 클라우드 컴퓨팅, 재택근무, `IoT (Internet of Things)` 기기의 폭발적 증가로 네트워크 경계가 물리적으로 소멸(`Perimeter-less`)됨에 따라, **"신뢰하되 검증하라(Trust but Verify)"가 아닌 "신뢰하지 말고 항상 검증하라(Never Trust, Always Verify)"**로 철학이 전환되었다.

#### 2. 기술적 등장 배경
① **기존 한계**: 내부망 침투 후 탈취된 계정으로의 `Lateral Movement (횡적 이동)`를 막을 수 없는 IP 기반 방화벽의 한계.  
② **혁신적 패러다임**: 신원(Identity)을 새로운 경계(`New Perimeter`)로 설정하고, `IAM (Identity and Access Management)`과 `MFA (Multi-Factor Authentication)`를 중심으로 재편.  
③ **비즈니스 요구**: 언제 어디서나 접속하는 `Hybrid Work` 환경을 지원하면서도, 보안 수준을 유지해야 하는 기업의 생존 요구.

> **💡 비유**: 과거의 보안은 '성벽과 해자'로 성을 지키는 것이었다면, 현대 보안은 사람 한 명 한 명이 군인 신분증을 들고 지나갈 때마다 모든 문에서 총구를 겨누고 검사하는 '철저한 통제 구역'을 운영하는 것이다.

#### 📢 섹션 요약 비유
마치 과거에는 지갑을 잃어버리면 집 문만 걸어 잠그면 되었지만, 이제는 지갑을 잃어버리면 모든 카드를 즉시 정지시키고(Zero Trust), 거래 내역을 실시간으로 감시하며(SIEM), 이상 거래가 감지되면 자동으로 카드를 면시시키는(SOAR) 스마트한 보안 시스템이 필요한 시대가 된 것입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

현대 보안은 크게 **접근 제어(Zero Trust)**, **인프라 통합(SASE)**, **운영 자동화(SOAR)**의 3축으로 구성된다. 이들은 데이터의 생성부터 소멸까지의 생애 주기를 보호한다.

#### 1. 핵심 구성 요소 비교

| 요소 | ZTNA (Zero Trust Network Access) | SASE (Secure Access Service Edge) | SOAR (Security Orchestration, Automation and Response) |
|:---|:---|:---|:---|
| **핵심 역할** | 신원 기반 접근 통제 (경계 제거) | 네트워크 + 보안 기능의 클라우드 통합 | 보안 대응 워크플로우 자동화 |
| **주요 기술** | `SDP (Software Defined Perimeter)`, `PDP (Policy Decision Point)` | `SD-WAN`, `FWaaS (Firewall as a Service)`, `CASB` | Playbook, API Hooking, `ML (Machine Learning)` |
| **대상** | 사용자/디바이스 인증 | 트래픽 라우팅 및 검사 | 로그 분석 및 위협 헌팅 |
| **작동 방식** | 접속 전 사전 인증 및 최소 권한 부여 | 사용자 근처의 `PoP (Point of Presence)`로 연결 | 시나리오 기반 자동 조치 실행 |

#### 2. 제로 트러스트 아키텍처 (ZTA) 구조도

제로 트러스트는 단순한 기술이 아니라 `NIST (National Institute of Standards and Technology)` SP 800-207에서 정의하는 아키텍처 프레임워크다. `CP (Control Plane)`과 `DP (Data Plane)`의 논리적 분리가 핵심이다.

```ascii
      [ subject = Principle Architectual Flow ]

      [ User / Device ]
            |
            | 1. Access Request (with Token/Certificate)
            v
   +-------------------------------+
   |  Control Plane (Policy Engine) |  <-- 결정권자 (PDP)
   |  - Analyze: Identity, Device,   |
   |    Location, Time, Behavior     |
   |  - Evaluate: Policy Rules       |
   +-------------------------------+
            |
            | 2. Issue Dyn. Access Token / Policy
            v
   +-------------------------------+
   |  Policy Enforcement Point (PEP) | <-- 실행자 (Gateway/Firewall)
   |  - Enforces: Allow/Deny         |
   +-------------------------------+
            |
            | 3. Establish Mutual TLS (mTLS) Tunnel
            v
      [ Resource / App ]
```

**[해설]**:
1. **인증 요청**: 사용자는 접속 권한을 요청하며, 이 과정에서 디바이스의 상태(OS 패치 여부, 안티바이러스 설치 여부)와 사용자 컨텍스트가 함께 전달됨.
2. **정책 결정**: PDP는 정책 데이터베이스(`PDP`)를 조회하여 접근 허용 여부를 결정. 이때 신뢰 점수(`Trust Score`)가 사용됨.
3. **집행 및 검증**: PEP는 토큰을 검증하고, 암호화된 터널(`mTLS`)을 생성하여 사용자와 리소스 간의 직접 통신을 잠시 허용함. 통신 중에도 지속적인 검증이 이루어짐.

#### 3. SASE (Secure Access Service Edge) 심층 분석

`SASE`는 네트워크(`SD-WAN`)와 보안(`SEC`) 서비스가 클라우드 엣지에서 만나는 하이브리드 모델이다. `CASB (Cloud Access Security Broker)`는 그중에서도 SaaS 사용을 제어하는 핵심 컴포넌트다.

```ascii
      [ SASE Service Model: Network + Security as a Service ]

   (Remote User)          (Branch Office)         (HQ)
        |                        |                    |
        +--------+---------------+--------------------+
                 | Internet / Private Line
                 v
      +--------------------------------------------------+
      |           Cloud Provider Edge (POP)              |
      |  +--------------------------------------------+  |
      |  |   Security Stack (Identification & Inspection) |
      |  |   1. CASB (Shadow IT Control)                |
      |  |   2. SWG (Web Filtering)                     |
      |  |   3. FWaaS (Firewall)                        |
      |  |   4. ZTNA (Private Access)                   |
      |  +------------------+-------------------------+  |
      |                     |                            |
      |   Network Stack     |                            |
      |   5. SD-WAN (Optimization/QoS)                   |
      |                     |                            |
      +---------------------+----------------------------+
                          |
                          | Clean Traffic
                          v
                 [ Cloud App / Data Center ]
```

**[해설]**:  
SASE의 핵심은 보안 검사가 사용자의 사무실(온프레미스)이 아니라, **클라우드 엣지(POP)**에서 일어난다는 점이다. 서울에 있는 사용자가 미국에 있는 SaaS에 접속할 때, 데이터는 사용자와 가까운 POP로 가서 먼저 보안 검사(디지털 면역)을 거친 뒤, 안전하게 목적지로 향한다. 이는 `Backhauling`(모든 트래픽을 본사로 우회시키는 구식 방식)의 병목을 제거한다.

> **💡 기술적 팁**: `DLP (Data Loss Prevention)`는 SASE 스택 내에서 데이터가 나가는 모든 경로를 감시하며, `CASB`는 API 모드와 프록시 모드로 작동하여 클라우드 내부의 설정 오류(Misconfiguration)를 잡아낸다.

#### 📢 섹션 요약 비유
SASE는 공항의 보안 심사대와 비행기 네트워크를 하나로 합친 것과 같습니다. 여러분이 집(분사)에서 출발하든 본사에서 출발하든, 상관없이 공항(클라우드 엣지)에 도착하는 순간 보안 검사(보안 기능)를 받고, 가장 빠른 항로(SD-WAN)로 목적지로 이동하게 됩니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 기술 비교 분석표: Perimeter vs. Zero Trust

| 구분 | 전통적 경계 보안 (Perimeter Security) | 제로 트러스트 (Zero Trust) |
|:---|:---|:---|
| **신뢰 모델** | 내부망 = 신뢰됨 | 내부망 = 신뢰 안 함 (Hostile) |
| **접근 제어** | IP 기반 (`5-tuple`) | 신원(Identity) 기반 |
| **데이터 위치** | 데이터 센터(온프레미스) 중심 | 클라우드/Edge 분산 |
| **암호화** | 네트워크 구간 암호화(VPN) | **E2E (End-to-End)** 암호화 |
| **확장성** | 물리적 장비 추가에 따른 비용 급증 | 클라우드 기반 탄력적 확장 |

#### 2. SOAR와 기존 SIEM의 융합 관계

`SIEM`이 "병원의 CT/MRI 촬영 및 판독(진단)"이라면, `SOAR`는 "응급 처치 및 수술(치료)"에 해당한다. 두 기술은 결합하여 **Security Operations Center (SOC)**의 효율을 극대화한다.

```ascii
      [ The Security Operations Workflow ]

   [ Endpoints / Network ]
           |
           | (Logs & Events)
           v
   +-----------------+
   |      SIEM       | <--- collects data, Correlation
   | (Detection)     | ---> Generates Alert (Phishing? Malware?)
   +-----------------+
           |
           | (Trigger)
           v
   +-----------------+       +------------------+
   |      SOAR       | <---> |  Threat Intel    |
   | (Response)      |       |  (Blocklists)    |
   +-----------------+       +------------------+
      |          ^
      | (Action)  | (Feedback)
      v          |
   [ Firewall ]-[ Endpoint ]-[ Email Server ]
   (Block IP)   (Isolate)     (Delete Spam)
```

**[해설]**:
1. **SIEM**은 다양한 로그를 수집하여 상관관계 분석(Correlation)을 통해 공격을 탐지.
2. **SOAR**는 SIEM의 알림을 트리거(Trigger)로 받아 Playbook(플레이북)에 정의된 대로 대응.
   * 예: 피싱 메일 감지 → `EDR (Endpoint Detection and Response)`에 연락 → 격리(Isolate) 조치 → 메일 서버에서 삭제 → 유사 해시값(TTP)을 블랙리스트에 추가.
3. 이 과정에서 사람의 개입을 최소화하여 `MTTR (Mean Time To Respond)`을 수시간에서 수분으로 줄임.

#### 3. 과목 융합 분석
*   **네트워크 (NW)**: SASE는 `MPLS` 망을 `SD-WAN`으로 대체하여 회선 비용을 절감하고 라텐시를 개선하는 네트워크 구조 혁신을 가져옴.
*   **데이터베이스 (DB)**: 클라우드 데이터베이스(`RDS`, `Redshift` 등)로의 접근 시 `CASB`가 작동하여 쿼리 수준에서의 데이터 유출을 방지.
*   **인공지능 (AI)**: SIEM과 SOAR에 적용된 `AI/ML`은 정상적인 패턴(Baseline)을 학습하여, 기존 룰 기반으로는 탐지하지 못했던 제로데이 공격(0-day Attack)이나 내자자 위협(`Insider Threat`)을 감지함.

#### 📢 섹션 요약 비유
네트워크와 보안의 융합(SASE)은 마치 도로(네트워크)와 교통 단속(보안)을 하나의 '스마트 무인 교통 시스템'으로 통합하는 것과 같습니다. SOAR와 SIEM의 결합은 순찰 도중 사건을 발견하면(SIEM), 경찰서에 보고하지 않고 현장에서 즉시 처벌하고 통로를 차단하는(SOAR) 자율 기동 순찰차와 같습니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 랜섬웨어 대응 (Ransomware Response)

**상황**: 재무팀 직원의 PC에서 악성 매크로가 실행되어 랜섬웨어가 네트워크 전반으로 퍼지려고 함.
**[의사결정 프로세스]**:

1.  **탐지 (SIEM/EDR)**: `EDR`이 파일의 행위 이상을 감지하여 SIEM으로 알림 전송. (Source IP, Hash value 확인).
2.  **오케스트레이션 (SOAR)**: SOAR 플랫폼이 랜섬웨어 플레이북 실행.
    *   **Step 1**: 영향 받는 호스트의 스위치 포트를 `Shut` 하거나 `VLAN` 변경하여 격리(Containment).
    *   **Step 2**: 공유 네트워크 드라이브의 쓰기 권한 차단.
    *   **Step 3**: 관리자에게 즉각적인 메시지(Slack/SMS) 발송.
3.  **결과**: 30초 이내에 확산 차단. 관리자는 로그만 확인하면 됨.

#### 2. 도입 체크리스트 및 고려사항

| 구분 | 점검 항목 | 상세 내용 |
|:---|:---|:---|
| **기술적** | 네트워크 트래픽 | 기존 인터넷 회선 대역폭이 SASE 트래