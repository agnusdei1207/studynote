+++
title = "665. 제로 트러스트 (Zero Trust)"
date = "2026-03-14"
+++

# 665. 제로 트러스트 (Zero Trust)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**= "신뢰는 증명되어야 한다(Verify, Then Trust)"는 철학을 바탕으로, 네트워크 경계(Perimeter) 내부라도 **기본 신뢰(Default Trust)**를 배제하고 **모든 접근 요청을 실시간 검증**하는 보안 아키텍처입니다.
> 2. **가치**= 랜섬웨어와 같은 **내부자 위협(Insider Threat)** 및 **횡적 이동(Lateral Movement)**을 차단하여, 침해 발생 시 피해 범위를 최소화하고 **MTTD(Mean Time To Detect, 평균 탐지 시간)** 및 **MTTR(Mean Time To Resolve, 평균 대응 시간)**을 획기적으로 단축시킵니다.
> 3. **융합**= **IAM (Identity and Access Management)**, **NAC (Network Access Control)**, **SDP (Software Defined Perimeter)** 기술이 융합되며, 단순한 네트워크 보안을 넘어 **클라우드(ZTNA)** 및 **엔드포인트(XDR)** 보안으로 확장되는 **SASE (Secure Access Service Edge)**의 핵심 축을 이룹니다.




### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
제로 트러스트(Zero Trust, ZT)는 "네트워크 내부는 안전하다"는 전통적인 보안 가정을 완전히 부정합니다. 2010년 Forrester의 John Kindervag가 최초로 정립했으며, 이후 **NIST (National Institute of Standards and Technology)**의 SP 800-207 표준을 통해 체계화되었습니다. 핵심은 사용자, 디바이스, 애플리케이션의 위치와 관계없이 **접근 요청마다 신원을 검증**하고 **최소 권한 원칙(Least Privilege)**을 적용하는 것입니다. 이는 물리적 경계가 무의미해진 클라우드 및 원격 근무 환경에 필수적인 패러다임입니다.

#### 2. 등장 배경: 경계 기반 보안의 한계
과거의 **Castle-and-Moat(성과 해자)** 모델은 방화벽과 **VPN (Virtual Private Network)**이 외부의 위협을 막는 한계선(Perimeter) 역할을 했습니다. 그러나 클라우드 도입, 모바일 워크, IoT 확산으로 인해 경계는 모호해졌습니다. 해커가 방화벽을 뚫거나 내부자의 계정이 탈취되면, 내부망은 아무런 방어 없이 무너집니다. 이러한 내부 망에서의 **후킹(Hooking)** 및 **피벗팅(Pivoting)** 공격을 방어하기 위해 등장했습니다.

**비교: 전통적 보안 vs 제로 트러스트**

| 구분 | 전통적 보안 (Perimeter-based) | 제로 트러스트 (Zero Trust) |
|:---|:---|:---|
| **신뢰 모델** | 내부망 = 신뢰 (Trust Internal) | 내부망 = 불신 (Never Trust, Always Verify) |
| **검증 시점** | 초기 로그인 시 1회 (Static) | 모든 요청마다 상시 검증 (Dynamic) |
| **접근 권한** | 넓은 권한(Standing Access) | 최소 권한(JIT/JEA) |
| **주요 위협 방어** | 외부 침입 방어 | 내부 확산(Lateral Movement) 방어 |

```text
┌─────────────────────────────────────────────────────────────────────┐
│                      보안 패러다임의 변화                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [과거: Castle & Moat]           [현재: Zero Trust]                 │
│                                                                     │
│   (외부)      │        (내부)        (외부/내부)     │   (데이터)    │
│   ❌❌❌❌     │    ✅✅✅✅✅         ❌❌❌❌      │   ❌❌✅    │
│   ───────────┼─────────────>       ❌❌❌❌      │   ❌✅❌    │
│   Firewall   │   Open Network      ❌❌❌❌      │   ❌✅✅    │
│              │                      ─────────────┼──────────> │
│              │                      검증 요구     │   신뢰 불   │
│                                                                     │
│   "한번 뚫리면                       "데이터 주변에는              │
│    끝장이다"                        항상 검증이 있다"              │
└─────────────────────────────────────────────────────────────────────┘
```
*도입: 위 도표는 보안의 신뢰 경계가 네트워크 경계에서 개별 자원 주변으로 이동함을 시각화합니다. 경계 기반 모델은 성벽 내부를 평원으로 보는 반면, 제로 트러스트는 성벽이 사라지고 모든 집마다 성벽이 존재하는 상태를 의미합니다.*
*해설: 전통 모델은 일단 성벽(방화벽)을 넘으면 모든 곳을 자유롭게 돌아다닐 수 있는 '트러스트 온 디맨드(Trust on Demand)' 상태였습니다. 반면, 제로 트러스트는 보물(데이터)이 있는 방마다 별도의 경비원과 생체 인식 잠금장치가 설치된 것과 같습니다. 즉, 보안의 단위가 네트워크 세그먼트에서 **Identity(신원)**와 **Asset(자산)** 수준으로 세분화(Micro-segmentation)되었습니다.*

#### 3. 💡 비유: '공항 보안 검색대'
제로 트러스트는 **비행기 탑승 전 모든 승객이 보안 검색대를 통과하는 것**과 같습니다. 비행기(내부망)에 이미 탑승한 승객(내부 사용자)이라 할지라도, 화장실에 다녀오거나 기내식을 먹을 때마다 매번 탑승권과 신분증을 확인하고 보안 검사를 다시 받는 구조입니다. 단순히 공항 입장만 검사하는 것이 아니라 **모든 행동과 이동마다 검증(Verification)**하는 것이 핵심입니다.

#### 📢 섹션 요약 비유
"마치 거대한 성(네트워크)에 단 한 번만 문을 열어주는 것이 아니라, 성 안의 모든 방마다 경비원을 세워 **출입할 때마다 열쇠와 신분증을 다시 확인**하게 만드는 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 논리 구성 요소 (NIST SP 800-207)
제로 트러스트는 단일 장비가 아니라 논리적인 컴포넌트의 조합입니다. **NIST (National Institute of Standards and Technology)** 표준에 정의된 핵심 요소는 다음과 같습니다.

| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **PDP** | Policy Decision Point | **결정 내리는 뇌**<br>요청을 분석하고 신뢰 알고리즘에 따라 허용/거부 결정을 내림 | REST API, TLS, X.509 | 경비 대장 |
| **PEP** | Policy Enforcement Point | **결정 집행하는 팔**<br>PDP의 결정에 따라 트래픽을 차단하거나 통신 세션을 설정 | IPTables, NGFW, Proxy, mTLS | 출입문 |
| **PA** | Policy Administrator | **관리자**<br>PDP와 PEP의 설정을 구성하고 신뢰 정책을 배포 및 관리 | SSH, SNMP, RESTCONF | 인사팀 |
| **CP** | Control Plane | **제어 영역**<br>정책 결정, 관리 트래픽, 신원 확인이 처리되는 논리적 영역 | gRPC, Message Queue | 본부 |
| **DP** | Data Plane | **데이터 영역**<br>실제 사용자 트래픽이 흐르는 경로로, PEP에 의해 제어됨 | IP, TCP, HTTP, QUIC | 도로 |

#### 2. 논리적 아키텍처 및 데이터 흐름
제로 트러스트의 동작은 요청(Request) 발생부터 검증(Verification), 집행(Enforcement)까지의 단계적 프로세스를 따릅니다. 아래 다이어그램은 사용자가 자원(Resource)에 접근할 때의 흐름을 도식화한 것입니다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  Zero Trust Logical Architecture                    │
│                 (Based on NIST SP 800-207)                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Subject: Principal]                                               │
│    User / Device ────(1. Access Request)────>                        │
│        ▲                                                        │
│        │                                                    │
│  [Policy Decision Point (PDP)] <───(2. Context Query)───┐   │
│   (Control Plane)          │                           │   │
│        │                   │                           │   │
│        │                   ▼                           │   │
│        │     ┌───────────────────────────────┐        │   │
│        │     │  Policy Administrator (PA)    │        │   │
│        │     └───────────────────────────────┘        │   │
│        │                                           │   │
│        │  (3. Decision Token: Allow/Deny)         │   │
│        └───────────────────┐                       │   │
│                            ▼                       │   │
│  [Policy Enforcement Point (PEP)] <───────┐   │   │
│       │ (Resource Gateway)                │   │   │
│       │                                   │   │   │
│       │                             (Dynamic Auth)  │
│       ▼                                   │   │   │
│  [Resource: Asset] ────────────────────────┘   │   │
│   (App / Data / Service)                   │   │
│                                             │   │
│                                              └───┘
│                        Trust Algorithm (Id + Device + Network)
└──────────────────────────────────────────────────────────────────────┘
```
*도입: 아키텍처는 제어부(Control Plane)와 데이터부(Data Plane)가 분리된 논리적 구조를 가집니다. 사용자의 모든 요청은 PEP에 의해 가로채지고, PDP는 다양한 신뢰 데이터 소스를 조회하여 결정을 내립니다.*
*해설: 이 과정에서 가장 중요한 것은 **PDP는 Control Plane**에 존재하여 네트워크 트래픽을 직접 처리하지 않는다는 점입니다(Decoupling). 사용자 요청은 PEP(예: VPN 게이트웨이, 프록시, 에이전트)에 도달하고, PEP는 PDP에게 "이 사용자를 통과시켜도 되는가?"를 질의(Query)합니다. PDP는 사용자의 신원(ID), 장치 건전성(Device Posture), 시간/위치(Context)를 실시간으로 종합 판단하여 암호화된 토큰(Token) 또는 명령을 PEP에게 내립니다. 이를 통해 정책 결정 로직과 데이터 전송 로직을 분리하여 보안성과 성능을 동시에 확보합니다.*

#### 3. 심층 동작 원리 및 핵심 알고리즘
제로 트러스트의 검증은 단순히 암호를 확인하는 것이 아니라 **위험 점수(Risk Score)** 기반의 동적 알고리즘을 사용합니다.

1.  **요청 수집 (Request Ingestion)**: PEP가 트래픽을 차단하고 요청자의 세션 ID, 목적지 IP, HTTP 헤더를 추출.
2.  **신뢰 평가 (Trust Evaluation)**:
    *   $Trust Score = f(Identity, Device, Network, Behavior)$
    *   **Identity**: **MFA (Multi-Factor Authentication)** 인증 여부, 계정 속상.
    *   **Device**: OS 패치 레벨, **EDR (Endpoint Detection and Response)** 설치 여부, 루팅/탈옥(Jailbreak) 여부.
    *   **Network**: IP 대역(공공 와이파이 vs 사무실), 지리적 위치(Geo-fencing).
3.  **정책 조회 (Policy Lookup)**: **RBAC (Role-Based Access Control)** 및 **ABAC (Attribute-Based Access Control)** 규칙 엔진에 질의.
4.  **결과 전송 (Decision Enforcement)**:
    *   Allow: PEP가 세션을 생성하고 통신 허용.
    *   Deny: 연결 종료 및 로그 기록.
    *   Limit: 예를 들어 읽기 전용(Read-Only) 권한으로 다운그레이드.

```python
# Pseudo-code: PDP의 의사결정 로직 예시
def evaluate_access_request(user, device, resource):
    # 1. 신원 검증 (Authentication)
    if not user.is_authenticated():
        return "Deny: No Auth"
    
    # 2. MFA 강제 (High Risk Resource)
    if resource.sensitivity == 'HIGH' and not user.mfa_verified:
        return "Deny: MFA Required"
    
    # 3. 장치 상태 검증 (Posture Check)
    if not device.is_compliant(os_version=">=10.15", has_av="True", has_edr="True"):
        return "Deny: Unhealthy Device"
    
    # 4. 맥락 검증 (Time/Location/Behavior)
    if user.location != "Office" and resource.is_internal_only:
        # 예외: VPN 또는 ZTNA 터널을 통한 접속인지 확인
        if not session.is_secure_tunnel():
            return "Deny: Location Violation"

    # 5. 최소 권한 부여 (JIT: Just-In-Time)
    # 데이터 수정 권한이 필요한 경우에만 쓰기 권한 부여
    if request.method == "READ":
        return "Allow: Read-Only"
    else:
        return "Allow: Read-Write (Session Timeout: 10m)"
```

#### 📢 섹션 요약 비유
"마치 고도로 감시되는 **은행 금고**와 같습니다. 금고 문(PEP)은 경비 대장(PDP)에게 무전으로 '이 사람의 지문, 출입카드, 현재 위치를 확인해 달라'고 요청하고, 모든 항목이 OK 사인을 받아야만 전자 잠금이 해제됩니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 제로 트러스트 네트워크 액세스 (ZTNA) vs VPN
전통적인 **VPN (Virtual Private Network)**과 제로 트러스트의 구현체인 **ZTNA (Zero Trust Network Access)**의 기술적 차이는 실무 구현 시 가장 중요한 포인트입니다.

| 비교 항목 | VPN (Virtual Private Network) | ZTNA (Zero Trust Network Access) |
|:---|:---|:---|
| **접근 방식** | 네트워크 레벨 연결 (L3 Tunnel) | 애플리케이션 레벨 연결 (L7 Gateway) |
| **신뢰 범위** | 연결 시 전체 서브넷 접근 가능 | 특정 앱/서비스만 접근 허용 |
| **네트워크 가시성** | 사용자가 내부 IP 스캔 가능 | 사용자에게 리소스가 숨겨짐 (Dark Site) |
| **성능** | VPN 허