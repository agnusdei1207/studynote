+++
title = "541-545. 네트워크 보안 인증 (AAA, RADIUS, TACACS+, Kerberos)"
date = "2026-03-14"
[extra]
+++

# 541-545. 네트워크 보안 인증 (AAA, RADIUS, TACACS+, Kerberos)

> **1. 본질**: AAA (Authentication, Authorization, Accounting)는 네트워크 자원 접근에 대한 **보안 3요소(Identity, Permission, Audit)**를 체계화한 프레임워크입니다.
> **2. 가치**: 중앙 집중식 사용자 관리를 통해 **운영 효율을 70% 이상 향상**시키며, 강력한 감사 기능(Auditing)으로 보안 규정 준수(Compliance)를 만족시킵니다.
> **3. 융합**: 네트워크 장비(NAS)의 접근 제어는 물론, Zero Trust(영구 신뢰 없는 보안) 아키텍처의 핵심 **PDP (Policy Decision Point)** 역할을 수행합니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
네트워크 보안 인증은 단순한 "비밀번호 확인"을 넘어, **AAA (Authentication, Authorization, Accounting)**라는 통합된 보안 프레임워크를 기반으로 작동합니다.
- **Authentication (인증)**: 사용자의 신원을 검증(Identity Verification)합니다.
- **Authorization (인가)**: 인증된 사용자에게 수행 가능한 작업의 범위를 제한합니다.
- **Accounting (계정 관리)**: 사용자의 자원 사용량, 시간, 수행 명령어 등을 기록하여 보안 감사(Audit) 자료로 활용합니다.

**2. 💡 비유**
마치 고급 회원제 클럽에 들어가는 과정과 같습니다. 현관에서 **회원증을 확인(Authentication)**하고, VIP 라운지는 **골드 회원만 출입 가능하도록 통제(Authorization)**하며, 나중에 **"누가, 언제, 몇 시간 동안 있었는지" CCTV와 출입 기록으로 확인(Accounting)**하는 시스템입니다.

**3. 등장 배경**
① **기존 한계**: 초기 네트워크는 라우터나 스위치마다 로컬(Local) 데이터베이스에 ID/PW를 저장했으나, 사용자가 수백 명으로 늘어나면서 **비밀번호 변경 및 관리의 비효율성**이 심각한 문제가 되었습니다. 또한, 해커의 침입 사실을 알 수 없는 **"Blind Spot"**이 존재했습니다.
② **혁신적 패러다임**: **AAA 서버(중앙 인증 서버)**를 도입하여 모든 사용자 정보를 한 곳에서 관리하고, 네트워크 장비(NAS: Network Access Server)는 인증 서버에만 질의하도록 아키텍처를 분리했습니다.
③ **현재의 비즈니스 요구**: 기업 내부망 보안 강화 및 각종 규제(개인정보보호법 등)에 대응하기 위해 **"누가, 언제, 어떤 명령어를 쳤는지"**에 대한 추적ability가 필수가 되었습니다.

**4. 📢 섹션 요약 비유**
네트워크 보안 인증의 개요는 **"건물의 출입관리 시스템을 통합 경비실로 이전한 것"**과 같습니다. 각 가게(네트워크 장비)마다 경비원을 두는 대신, 중앙 경비실(AAA Server)에서 모든 출입증을 확인하고 기록을 남기는 효율적인 시스템입니다.

```ascii
+---------------------------------------------------------------+
|                   [ AAA Architecture Context ]                |
+---------------------------------------------------------------+
|                                                               |
|   ① Past (Local)              ② Present (Centralized AAA)    |
|  +-------+    +-------+      +-------+      +-------------+  |
|  |Router | PW |Router |      |Router |----->|   AAA       |  |
|  | DB    |    | DB    |      |       | Auth |  Server     |  |
|  +-------+    +-------+      +-------+      | (RADIUS/    |  |
|     ↓          ↓                              |  TACACS+)   |  |
|  Inefficiency & Isolation                     +-------------+  |
|                                              User Info, Policy|
+---------------------------------------------------------------+
```
*(도해 1: 로컬 인증에서 중앙 AAA 인증으로의 패러다임 이동)*

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. AAA 프로토콜: RADIUS vs TACACS+**
AAA를 구현하기 위한 대표적인 프로토콜로 **RADIUS (Remote Authentication Dial-In User Service)**와 **TACACS+ (Terminal Access Controller Access-Control System Plus)**가 있습니다.

| 구분 | RADIUS (RFC 2865) | TACACS+ (Cisco Proprietary) |
|:---:|:---|:---|
| **개발 배경** | Network Access Server(통신 서버) 인증용 | 라우터/스위치 관리자 접속 제어용 |
| **사용 포트** | UDP 1812(Auth), 1813(Acct) | TCP 49 |
| **신뢰성** | **UDP** 기반으로 패킷 손실 가능성 (약 3회 재전송) | **TCP** 기반으로 신뢰성 보장 |
| **보안성** | Password만 암호화, Header는 평문 | **전체 패킷 암호화** (공격자 분석 어려움) |
| **기능 결합도** | **AAA**(Auth+Author) 통합, A(Accounting) 분리 | **AAA 완전 분리** (각 요청 별도 처리) |
| **주요 용도** | 일반 사용자 네트워크 접속 (Wi-Fi, VPN) | 장비 관리자(Admin) 권한 제어 (Command 제어) |

**2. RADIUS 인증 절차 (상세 동작)**
RADIUS는 UDP의 빠름을 장점으로 하지만, 인증과 권한 부여가 묶여 있어 세밀한 제어가 어렵습니다.

```ascii
[RADIUS Authentication Flow]

[Client(NAS)]              [RADIUS Server]                [User DB]
     |  1. Access-Request    |                              |
     | (User ID / PW Encrypt) |                             |
     |----------------------->|  2. Lookup User ID          |
     |                        |---------------------------->|
     |                        |<----------------------------|
     |  3. Access-Accept      |  4. Verify Password         |
     | (Auth + Attributes)    | (Radius Attribute Profile)   |
     |<-----------------------|                             |
     |                        |                             |
```
*(도해 2: RADIUS의 요청-응답 기반 인증 흐름)*
> **해설**:
> 1. 클라이언트(스위치 등)가 사용자로부터 ID/PW를 받아 **RADIUS Access-Request** 패킷을 생성합니다. 이때 비밀번호는 MD5 등으로 해싱되어 전송됩니다.
> 2. 서버는 사용자 DB를 조회하여 존재하는지 확인합니다.
> 3. 존재한다면 비밀번호를 검증하고, 사용자 프로필(VLAN ID, 할당 IP 등)을 포함한 **Access-Accept** 패킷을 반환합니다.
> 4. UDP 프로토콜이므로 응답이 없으면 타임아웃 후 재전송합니다.

**3. TACACS+ 인증 절차 (상세 동작)**
TACACS+는 TCP의 신뢰성을 바탕으로 AAA를 완전히 분리하여 관리자의 명령어 한 줄까지 감사할 수 있습니다.

```ascii
[TACACS+ AAA Separation Flow]

  [Admin] --(1) Auth Start--> [Router] --(Authen)--------> [TACACS+]
                                 <-----(Success)-----------
  [Admin] --(2) Enter Cmd --> [Router] --(Author)---------> [TACACS+]
      "show run"                   <-----(Permit)-----------
                                  --(Accounting)-----------> [TACACS+]
                                           (Log: Executed "show run")
```
*(도해 3: TACACS+의 세분화된 AAA 흐름)*
> **해설**:
> **Authentication**(로그인), **Authorization**(명령어 허용), **Accounting**(명령어 기록) 과정이 각각 독립적인 세션을 통해 이루어집니다. 관리자가 `enable` 모드로 진입하거나 설정 변경 명령어(`conf t`)를 입력할 때마다 라우터는 매번 서버에게 "이 사용자에게 이 권한이 있는지?"를 확인(Authorization Check)합니다. 이로써 "모든 사람은 로그인할 수 있으나, 설정 변경은 특정 그룹만 가능"하게 하는 세밀한 **RBAC (Role-Based Access Control)**이 구현됩니다.

**4. 핵심 알고리즘 및 보안 매커니즘**
RADIUS는 비밀번호만 숨기고 TACACS+는 전체를 숨기는 차이는 패킷 구조에서 기인합니다.
- **RADIUS**: `Shared Secret`과 `Request Authenticator`를 XOR 연산하여 Password만 숨깁니다. Header 정보(속성 값)가 평문이라 해커가 어떤 권한이 부여되었는지 유추 가능합니다.
- **TACACS+**: MD5 Hash Chaining을 사용해 패킷 전체를 암호화하므로 내부 내용을 알 수 없습니다.

**5. 📢 섹션 요약 비유**
RADIUS는 **'자동 입차 게이트'**와 같습니다. 차량이 들어오면 계산기를 찍고(인증+결제) 바로 들여보냅니다. 반면 TACACS+는 **'공항 보안 검색대'**와 같습니다. 출입권을 확인하고(인증), 수하물을 검사하고(인가), 모든 과정을 카메라로 기록(계정 관리)하는 등 단계별로 깐깐하게 따집니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. AAA 및 프로토콜 심층 비교**

| 비교 항목 | RADIUS | TACACS+ | Kerberos (Ticket-Based) |
|:---|:---|:---|:---|
| **주 목적** | 네트워크 접속 제어 (NAS) | 장비 관리자 권한 제어 | SSO (Single Sign-On) 구현 |
| **프로토콜 구조** | Client/Server (UDP) | Client/Server (TCP) | 3-Tier (KDC: AS + TGS) |
| **단점** | 암호화 범위 제한, 세밀한 권한 제어 어려움 | 벤더 종속성(Cisco), 복잡한 설정 | 시간 동기화 중요 (Time Skew 문제) |
| **융합 영역** | Wi-Fi, VPN, 802.1X 포트 보안 | CLI 환경 (SSH/Console) 감사 | Active Directory, Web 인증 |

**2. Kerberos (Symmetric Key Based Authentication)**
Kerberos는 MIT에서 개발된 티켓 기반 인증 시스템으로, **KDC (Key Distribution Center)**가 핵심입니다.

```ascii
[Kerberos Ticket Exchange Flow]

   [User]                 [KDC (AS/TGS)]                [Service]
      |                         |                           |
      | 1. ID Request (Pre-Auth) |                           |
      |------------------------->|                           |
      | 2. TGT (Ticket Granting Ticket) {Session Key}        |
      |<-------------------------|                           |
      |                          |                           |
      | 3. Service Request (TGT + Service ID)                |
      |------------------------->|                           |
      |                          | 4. Create Service Ticket  |
      | 5. Service Ticket {User Info} ---------------------->|
      |<-------------------------|                           |
      | 6. Access with Ticket                                |
      |------------------------------------------------------>|
```
*(도해 4: Kerberos의 티켓 교환 과정)*
> **해설**:
> 1. **AS (Authentication Service)**: 사용자가 ID를 보내면, 비밀키 암호화된 **TGT**를 발급합니다. 이는 마치 "입장권을 사기 위한 자격이 있음"을 증명하는 티켓입니다.
> 2. **TGS (Ticket Granting Service)**: 사용자가 TGT를 제시하고 특정 서비스(예: 파일 서버) 이용을 요청하면, 서비스 전용 티켓(**Session Key** 포함)을 발급합니다.
> 3. **Service Access**: 사용자는 서비스 티켓을 가지고 실제 서버에 접속합니다. 서버는 티켓을 검증하고 즉시 세션을 형성합니다.
> * **장점**: 패스워드가 네트워크를 직접 타지 않아 스니핑(Sniffing)에 안전합니다. **Replay Attack(재전송 공격) 방지**를 위해 Timestamp를 강제합니다.

**3. 과목 융합 관점 (OS/Network)**
- **OS/Active Directory**: 윈도우 도메인 환경에서 Kerberos는 기본 인증 메커니즘입니다. 로그인 시 티켓이 발급되고, 파일 접근 시마다 티켓이 자동으로 사용되므로 사용자는 매번 비밀번호를 넣지 않아도 됩니다 (**SSO**).
- **네트워크/보안**: 무선 AP(Wi-Fi)에서 802.1X 인증을 수행할 때, EAPOL 패킷을 캡슐화하여 RADIUS 서버로 전달합니다. 즉, **"Wi-Fi AP는 포트를 열어주지 않고, RADIUS 서버가 'OK'라고 할 때만 열어주는 Gatekeeper 역할"**을 합니다.

**4. 📢 섹션 요약 비유**
Kerberos는 **'테마파크 자유이용권'** 시스템입니다. 매표소(KDC)에서 돈을 내고 티켓(TGT)을 사면, 놀이기구(서비스)마다 티켓을 다시 살 필요 없이 자유롭게 이용합니다. 기프트샵(RADIUS)은 물건을 살 때마다 카드를 찍듯이 매번 인증을 하고, 전용 관리실(TACACS+)은 직원이 관리자 키를 사용할 때마다 그 용도를 철저히 검사하는 곳입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**
1. **상황**: 대기업 본사의 네트워크 운영팀에서 유선/무선 네트워크 접속 및 장비 관리 체계 구축 필요.
2. **요구사항**: 일반 직원은 사내 인터넷만 사용 가능하게 하고, 네트워크 운영자는 모든 장비에 접속하여 설정을 변경할 수 있어야 함. 단, 모든 관리자의 명령어 로그는 사이버 감사(Audit)를 위해 5년 보관해야 함.
3. **의사결정 매트릭스**:
   - **일반 직원/게스트 Wi-Fi**: **RADIUS + 802.1X** 사용. (속도와 범용성 중시). AD와 연동하여 사용자 계정으로 인증.
   - **장비 관리자(NetAdmin)**: **TACACS+** 사용. TCP 기반 안정성과 전체 패킷 암호화, 그리고 무엇보다 **'Authorization' 기능(명령어별 권한 제어)**이 필수적임.
   - **결과**: 이중 인증 체계(Dual Authentication Protocol)를 구축하여 보안성과 효율성을 동시에 확보.

**2. 도입 체크리스트**
| 구분 | 체크 항목 |
|:---|:---|
|**기술적**|[ ] NAS(장비)가 지원하는 프로토콜 확인 (RADIUS/TACACS+)<br>[ ] NTP (Network Time Protocol) 동기화 (TACACS+는 시간 기반 로그가 중요)<br>[ ]