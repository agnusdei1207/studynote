+++
title = "693. 제로 트러스트 아키텍처 최소 권한 원칙"
date = "2026-03-15"
weight = 693
[extra]
categories = ["Software Engineering"]
tags = ["Security", "Zero Trust", "NIST 800-207", "Micro-segmentation", "IAM", "Cybersecurity"]
+++

# 693. 제로 트러스트 아키텍처 최소 권한 원칙

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: "신뢰는 검증되어야 하며, 신원은 맥락에 따라 결정된다"는 철학에 기초하여, 네트워크 경계 내외부를 불문하고 모든 액세스 요청에 대해 ID, 디바이스, 데이터 상태를 기반으로 지속적인 인증 및 최소 권한 부여를 수행하는 **동적 보안 패러다임**입니다.
> 2. **가치**: 방화벽과 VPN (Virtual Private Network)으로 대변되는 기존 경계 기반 보안(Perimeter Security)의 붕괴 이후, 클라우드 및 하이브리드 환경에서 랜섬웨어와 같은 내부 침해 확산(Lateral Movement)을 차단하여 데이터 유출 방지 효과를 극대화합니다.
> 3. **융합**: IAM (Identity and Access Management), SASE (Secure Access Service Edge), 마이크로 세분화(Micro-segmentation) 기술이 융합되어, 단순한 네트워크 접근 제어를 넘어 데이터 보안 거버넌스의 핵심 표준(NIST SP 800-207)으로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 철학의 재정립
제로 트러스트(Zero Trust)는 2010년 포레스터(Forrester)의 존 킨더벅(John Kindervag)이 주창한 개념으로, "물리적 또는 논리적 네트워크 경계 내부에 있는 사용자, 디바이스, 애플리케이션을 기본적으로 신뢰하지 않는다"는 보안 모델입니다. 전통적인 보안이 "내부는 안전, 외부는 위험"이라는 이분법적 사고에 기초했다면, 제로 트러스트는 **"신뢰할 수 있는 영역은 없으며, 모든 요청은 악의적인 것으로 간주된다"**는 전제하에 출발합니다. 이는 단순한 기술적 구현을 넘어, 보안의 근본적인 신뢰 모델을 재설계하는 아키텍처적 패러다임 시프트(Paradigm Shift)입니다.

### 등장 배경: 경계 보안의 한계 (De-perimeterization)
기존의 기업 보안은 방화벽(Firewall)이라는 견고한 성벽을 쌓고, 내부 사용자는 무조건 신뢰하는 **성(Castle)과 해자(Moat) 모델**을 따랐습니다. 그러나 클라우드 컴퓨팅(Cloud Computing)의 도입, 모바일 기기의 확산, 그리고 원격 근무(Remote Work)의 일상화로 인해 '경계'라는 개념 자체가 모호해졌습니다. 공격자가 방화벽을 뚫거나, 악의적인 내부자가 한 번 진입하면 평평한 네트워크(Flat Network) 위에서 중요 자산까지 자유롭게 이동하는 **Lateral Movement(횡적 이동)**가 가능해지면서 기존 모델은 붕괴되었습니다. 이에 따라 네트워크의 위치와 무관하게 데이터 중심으로 보안을 재구축해야 한다는 요구가 강력히 제기되었습니다.

### 💡 비유: 공항 보안 검색대
제로 트러스트는 공항의 보안 시스템과 유사합니다. 비행기(리소스)에 탑승하기 위해 사용자는 일등석이든 비즈니스석이든 관계없이, 매번 보안 검색대(인증/인가)를 통과해야 합니다. 비행기 티켓(권한)이 있더라도 흉기 소지 여부(기기 상태)나 여권(신원)을 검사받아야 하며, 탑승 후에도 기내 승무원이 승객의 행동을 지속적으로 모니터링하는 것과 같습니다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                       [ 보안 모델 진화 과정 ]                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 1. 전통적 보안 (Castle & Moat)                                       │
│    ┌─────────────────────────────────────────┐                       │
│    │          안전한 내부 망 (Trusted)       │                       │
│    │    ┌───────────┐       ┌───────────┐   │  ▲ 한 번 뚫리면       │
│    │    │  금고    │◄─────┤│  금고    │   │  │ 내부 전체 털림     │
│    │  (DB)        │       │(DB)       │   │  │ (Lateral Movement)│
│    │    └─────▲─────┘       └─────▲─────┘   │  ▼                   │
│    │          │                 │           │                       │
│    └──────────┼─────────────────┼───────────┘                       │
│               │                 │                                   │
│        ▼     ▼▼               ▼▼     ▼                             │
│     [ 🏰 방화벽 ] ────────▶ 외부 (Untrusted)                          │
│                                                                      │
│ -------------------------------------------------------------------- │
│                                                                      │
│ 2. 제로 트러스트 (Zero Trust)                                        │
│    ┌───┐   ┌─▼──┐   ┌─▼──┐   ┌─▼──┐   ┌─▼──┐   ┌─▼──┐   ┌───┐    │
│    │ A │──▶│ PEP│──▶│ PDP│──▶│ PEP│──▶│ B  │   │ C  │   │ D  │    │
│    └───┘   └────┘   └────┘   └────┘   └────┘   └────┘   └───┘    │
│      │      ↑                  ↑                 ▲                 │
│      └──────┴──────────────────┴─────────────────┘                 │
│                   (모든 경로에서 검증)                               │
│                                                                      │
│   "네트워크 위치와 상관없이, A가 B에 접근할 때마다 신원을 검증함"     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 📢 섹션 요약 비유
> 마치 거대한 성벽을 허무는 대신, 성 안의 모든 방과 금고마다 **생체 인식 잠금장치를 설치하여** 누가, 언제, 어디서 들어오려 하는지 실시간으로 확인하고 방마다 다른 열쇠를 요구하는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. NIST SP 800-207 기반 핵심 논리 아키텍처
NIST (National Institute of Standards and Technology)의 SP 800-207 문서에서 정의하는 제로 트러스트 논리 아키텍처는 **PDP (Policy Decision Point)**와 **PEP (Policy Enforcement Point)**라는 두 가지 핵심 컴포넌트의 상호작용으로 정의됩니다. 이는 모든 액세스 요청이 필터링되는 제어 평면(Control Plane)과 데이터가 실제로 흐르는 데이터 평면(Data Plane)으로 엄격히 분리됨을 의미합니다.

### 2. 구성 요소 상세 분석표

| 구성 요소 | 전체 명칭 (Abbreviation) | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---:|:---|:---|:---|:---|
| **주체 (Subject)** | Principal | 액세스를 요청하는 사용자, 디바이스, 서비스 또는 프로세스. 속성(Attribute) 정보를 제공. | SAML, OIDC | 손님 |
| **자산 (Resource)** | Target Asset | 보호 대상이 되는 데이터, 애플리케이션, 서비스, API. | HTTPS, SSH | 방 안의 물건 |
| **PDP** | Policy Decision Point | "뇌" 역할. 신뢰 정책(Policy)을 해석하고 PEP로부터 수집한 컨텍스트(Context)를 기반으로 허용/거부 여부를 판단. | XACML, REST API | 판사 |
| **PEP** | Policy Enforcement Point | "문지기" 역할. 주체의 요청을 가로채서 PDP에 전달하고, PDP의 결정을 시행(접속 차단/허용/설정 적용). | IPsec, mTLS, Proxy | 경비원 |
| **정책 저장소** | Policy Administration Point | 신뢰할 수 있는 소스에서 수집한 정책(Rule)을 저장하는 데이터베이스. | LDAP, SQL | 법전 |
| **CI/CD** | Continuous Improvement | 시스템 로그를 분석하여 정책을 지속적으로 최적화하고 탐지 규칙을 업데이트. | SIEM, SOAR | 감사원 |

### 3. 제로 트러스트 상세 데이터 흐름도
아래 다이어그램은 사용자가 리소스에 접근하기 위해 거쳐야 하는 검증 프로세스의 5단계를 도식화한 것입니다.

```text
    [ ① Subject: User / Device ]
                 │
                 │ Request Access (HTTPS)
                 ▼
    ┌────────────────────────────────────────────────────┐
    │ ② PEP (Policy Enforcement Point) - Gatekeeper      │
    │    - Request Interception                          │
    │    - Context Collection (Device Health, Location)  │
    └─────────────────────┬──────────────────────────────┘
                          │ Context Inquiry
                          ▼
    ┌────────────────────────────────────────────────────┐
    │ ③ PDP (Policy Decision Point) - Brain             │
    │    ┌──────────────────────────────────────────┐   │
    │    │  Dynamic Policy Engine (Rule Based)      │   │
    │    │  IF (User == 'Admin' AND                 │   │
    │    │      Device == 'Managed' AND             │   │
    │    │      RiskScore < 'Threshold')            │   │
    │    │  THEN Allow ELSE Deny                    │   │
    │    └──────────────────────────────────────────┘   │
    │             ▲                                      │
    │             │  Lookup                              │
    │    ┌────────┴────────┐                            │
    │    │ Trust Store      │                            │
    │    │ (ID, Cert, Attr) │                            │
    │    └─────────────────┘                            │
    └─────────────────────┬──────────────────────────────┘
                          │ Decision (Allow/Deny)
                          ▼
    ┌────────────────────────────────────────────────────┐
    │ ④ PEP (Enforcement)                               │
    │    - Permit Access to ⑤ Resource                  │
    │    - Establish Tunnel (mTLS/IPsec)                │
    │    - Apply Limitations (JIT/JEA)                  │
    └────────────────────────────────────────────────────┘
                          │
                          ▼
                   [ ⑤ Resource ]
```

### 4. 심층 동작 원리 및 알고리즘
제로 트러스트의 결정 과정은 단순히 ID/PW 검증을 넘어 다변수(Multi-factor) 분석을 수행합니다.

**A. 신뢰 알고리즘 (Trust Algorithm)**
$Trust Score = f(User\_Identity, Device\_Health, Context, Behavior\_Pattern)$
- **User\_Identity**: MFA (Multi-Factor Authentication), SSO (Single Sign-On) 상태.
- **Device\_Health**: OS 패치 수준, 루팅/탈옥 여부, EDR (Endpoint Detection and Response) 설치 여부.
- **Context**: 접속 시간, 위치(Geo-fencing), IP 신뢰도.

**B. JIT (Just-In-Time) & JEA (Just-Enough-Access)**
- **JIT**: 필요할 때만 임시 접속 권한을 발급. (상시 계정 부재)
- **JEA**: 필요한 최소한의 작업만 수행 가능하도록 권한 제한. (예: 관리자 계정이라도 파일 다운로드 금지)

```python
# Zero Trust Decision Logic Pseudo-code
def evaluate_access_request(user, device, resource):
    # 1. Verify Identity (Authentication)
    if not authenticate(user.mfa_token):
        return Response(DENY, reason="Invalid Credentials")

    # 2. Check Device Posture
    if device.os_version < MIN_OS_VERSION or not device.edr_active:
        return Response(DENY, reason="Unhealthy Device")

    # 3. Evaluate Risk Score (Behavioral Analysis)
    risk_score = calculate_risk(user, device, resource)
    
    # 4. Apply Policy (Authorization)
    policy = get_policy(user.role, resource.type)
    
    if risk_score > policy.risk_threshold:
        # Trigger Step-up Authentication
        return Response(CHALLENGE, method="Biometric")
    
    # 5. Grant Least Privilege Access
    return Response(ALLOW, 
                    scope=policy.minimal_scope, 
                    ttl=policy.max_duration)
```

### 📢 섹션 요약 비유
> 마치 고급 주차장 시스템과 같습니다. 단순히 주차권을 가지고 있다고(인증) 입장이 허용되는 것이 아니라, 차량 번호 인식(기기 검증), 예약 여부 확인(권한), 그리고 입구에서 번호표 발부(세션 생성)까지 모든 과정이 자동화되어 있으며, 주차장 내부에서도 CCTV를 통해 지속적으로 감시됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: VPN vs. ZTNA
기존의 네트워크 접속 방식인 VPN과 제로 트러스트의 구현체인 ZTNA (Zero Trust Network Access)는 근본적인 신뢰 모델에서 차이가 있습니다.

| 비교 항목 | 가상 사설망 (VPN) | 제로 트러스트 네트워크 접근 (ZTNA) |
|:---:|:---|:---|
| **신뢰 모델** | **연결 기반 신뢰**: 터널이 연결되면 내부 네트워크 전체에 대해 암묵적 신뢰 부여 | **애플리케이션 기반 불신**: 접속 전후 매 요청마다 신원과 권한 검증 |
| **네트워크 접근성** | **브로드캐스트 접근**: 연결된 사용자는 해당 서브넷의 모든 자원(포함된/미포함) 스캔 가능 | **다이렉트 접근**: 애플리케이션에 대한 URL/IP만 노출되며, 네트워크 레벨 숨김 (Dark Cloud) |
| **사용자 경험 (UX)** | 터널링으로 인한 대역폭 병목 및 지연(Latency) 발생 가능 | 클라우드 게이트웨이 경유를 통한 가속화 및 로컬 브레이크아웃(Local Breakout) 지원 |
| **보안 가시성** | 터널 내부 트래픽 암호화되어 중간 검증 어려움 (Blind Spot) | 세션 및 애플리케이션 레벨 로그 상세 수집 가능 (Granular Visibility) |
| **확장성** | Concentr