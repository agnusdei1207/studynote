+++
title = "666. SASE (Secure Access Service Edge)"
date = "2026-03-16"
weight = 666
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "SASE", "Secure Access Service Edge", "네트워크 보안", "SD-WAN", "SSE"]
+++

# SASE (Secure Access Service Edge)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SASE (Secure Access Service Edge)는 네트워킹(SD-WAN)과 보안(SSE) 기능을 **엣지(Edge) 클라우드로 통합**한 아키텍처로, 사용자와 리소스의 물리적 위치에 구애받지 않는 **ID 중심의 보안 모델**을 구현한다.
> 2. **가치**: 기존 하이브리드 웹(Hub-and-Spoke) 구조의 **MPLS (Multiprotocol Label Switching) 비용을 제거**하고, 애플리케이션 접속 지연(Latency)을 최소화하여 **사용자 경험(UX)과 보안 효율성을 동시에 확보**한다.
> 3. **융합**: SD-WAN의 궤로 최적화 기능에 **SSE (Security Service Edge)**를 탑재하여, ZTNA(제로 트러스트), CASB, SWG 등의 보안 서비스를 **클로즈(Close) 프로시시(Closest Point of Presence)**에서 제공하는 네트워크·보안 융합 기술이다.

+++

### Ⅰ. 개요 (Context & Background)

SASE는 2019년 Gartner가 정의한 개념으로, 물리적인 보안 장비와 전용 회선(MPLS)에 의존하던 전통적 네트워크 보안 패러다임을 클라우드 중심으로 전환하는 기술이다.

**1. 개념 및 철학**
SASE는 WAN(Wide Area Network) 기능과 네트워크 보안 서비스를 단일한 클라우드 플랫폼으로 전달하는 서비스 모델이다. 핵심은 "Identity가 새로의 경계(New Perimeter)"라는 철학으로, 사용자의 IP 주소가 아닌 **신원(Identity)과 장치의 상태(Context)**를 기반으로 접근을 제어한다. 이는 더 이상 데이터 센터(Data Center)가 트래픽의 중심축이 아니며, 클라우드 애플리케이션과 모바일 사용자가 분산된 아키텍처에 적합하다.

**2. 등장 배경: 3가지 패러다임 시프트**
① **하드웨어 정점에서 소프트웨어 정점으로**: 전통적 방화벽과 로드 밸런서가 가상화되어 클라우드 서비스 형태로 제공됨.
② **사무실 중심에서 사용자 중심으로**: 코로나19 이후 원격 근무와 재택근무가 일상화되며, 본사를 거쳐 인터넷으로 나가는 "헤브앤스포크(Hub-and-Spoke)" 트래픽 패턴이 비효율적으로 변화.
③ **SaaS(Software as a Service)의 폭발적 증가**: 트래픽의 80% 이상이 인터넷으로 직접 나가며, 본사 보안 장비를 우회하는 "Shadow IT" 문제 대두.

**3. 💡 비유: 고속도로와 통합 요금소**
SASE는 **"고속도로 진입로마다 설치된 '스마트 하이패스 + 위반 차량 단속 시스템' 일체형 게이트"**와 같다. 과거에는 모든 차량이 수도권(본사)에 있는 거대한 톨게이트를 거쳐야 했으나, SASE는 전국 각지(PoP)에 진입 시 보안 검사와 통로 최적화를 동시에 수행한다.

**4. 📢 섹션 요약 비유**
> 과거 모든 차량이 서울(본사)로 집결해 요금을 내고 다시 지방으로 가던 비효율적인 시스템을, 전국의 고속도로 진입로마다 요금 정산과 안전 검사를 동시에 처리하는 **"스마트 통합 톨게이트"**로 개선한 것과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

SASE는 크게 네트워킹을 담당하는 **SD-WAN**과 보안을 담당하는 **SSE (Security Service Edge)**가 결합된 구조를 가진다.

**1. 핵심 구성 요소 상세**

| 구성 요소 | 전체 명칭 | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **SD-WAN** | Software-Defined WAN | 궤로 최적화, 패킷 분류(Critical/General)하여 비즈니스 크리티컬 애플리케이션의 성능 보장 | BGP, OSPF, Segment Routing | 스마트 내비게이션(길 찾기) |
| **ZTNA** | Zero Trust Network Access | ID 기반 접근 제어. 접속 전 사용자/단체 검증 후 애플리케이션 접속 허용(Deny by Default) | mTLS, JWT | 전용 카드키 인증 |
| **CASB** | Cloud Access Security Broker | 클라우드 사용 가시성 확보 및 제어. Shadow IT 탐지 및 데이터 암호화 | API Mode, Forward Proxy | 클라우드 상품 출입구의 검표원 |
| **SWG** | Secure Web Gateway | 웹 트래픽 필터링, 악성 URL 차단, SSL 검사(Decryption) | HTTPS Inspection | 인터넷 해야 방호벽 |
| **FWaaS** | Firewall as a Service | L3~L7 방화벽 기능을 클라우드에서 제공. Stateful Inspection 수행 | Stateful Inspection | 가상 방화벽 |
| **RBI** | Remote Browser Isolation | 위험 웹사이트를 격리된 클라우드 브라우저에서 렌더링하여 안전한 스트림만 전송 | HTML/CSS Streaming | 위험물질 로봇 팔로 다루기 |

**2. SASE 트래픽 처리 흐름 (Data Plane)**
사용자가 클라우드 애플리케이션에 접속할 때, 물리적인 거리에 상관없이 가장 가까운 SASE PoP(Point of Presence)로 연결되어 보안 검사를 거치는 과정은 다음과 같다.

```text
   [흐름: 사용자 → SASE PoP → 목적지]
   1. User (Remote Branch)
      │
      ▼
   2. SD-WAN CPE (Software Edge)  <-- 경로 최적화 및 암호화(IPsec)
      │
      │ (Internet / Private Circuit)
      │
      ▼
   3. ┌─────────────────────────────────────────────┐
      │           SASE Cloud PoP (Nearest)         │
      │                                             │
      │  ┌───────────────────────────────────────┐ │
      │  │  ① Traffic Identification             │ │  <-- "이 트래픽은 Office365인가?"
      │  └───────────┬───────────────────────────┘ │
      │              ▼                             │
      │  ┌───────────────────────────────────────┐ │
      │  │  ② Security Stack Execution (SSE)     │ │
      │  │    - Authentication (IdP Check)       │ │
      │  │    - CASB (Shadow IT Check)           │ │
      │  │    - Anti-Malware / Threat Intel.     │ │
      │  └───────────┬───────────────────────────┘ │
      │              ▼                             │
      │  ┌───────────────────────────────────────┐ │
      │  │  ③ Forwarding / Optimization          │ │
      │  │    - Direct Internet Breakout         │ │
      │  └───────────┬───────────────────────────┘ │
      └──────────────┼─────────────────────────────┘
                     │
                     ▼
   4. Destination (SaaS App / Public Cloud)
```

**3. 다이어그램 해설**
① **Traffic Identification**: 사용자로부터 오는 패킷을 분석하여 트래픽의 성질(비디오, 웹, 메일 등)을 식별한다.
② **Security Stack Execution**: 사용자의 신원을 확인(IdP 연동)하고, CASB를 통해 승인되지 않은 클라우드 서비스 접속을 차단하며, 악성 코드를 검사한다. 이 모든 과정은 투명하게(Transparent) 수행된다.
③ **Forwarding**: 검사가 완료된 트래픽을 목적지까지 가장 빠른 경로로 전송한다. 본사 데이터 센터를 거치지 않고 인터넷으로 바로 나가는 구조를 가지므로 **Latency가 획기적으로 감소**한다.

**4. 📢 섹션 요약 비유**
> 집(본사)에 설치된 공기청정기(보안 장비)를 통해서만 숨을 쉴 수 있는 것이 아니라, **내가 서 있는 도시 전체에 공기청정기가 설치된 것과 같습니다.** 어디에 있든 숨을 들이마시는 순간 공기는 깨끗해집니다(Secure Access).

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술적 진화: 전통 방식 vs SASE**

| 비교 항목 | Legacy Hub-and-Spoke (MPLS) | SASE Architecture | 변화 효과 |
|:---|:---|:---|:---|
| **트래픽 경로** | 지사 → 본사 → 인터넷 (Triangle Routing) | 지사 → PoP → 목적지 (Direct Routing) | **지연 시간 40~60% 감소** |
| **보안 경계** | 데이터센터(본사) 기반 방화벽 | 사용자/디바이스 기반(ID) | **데이터 유출 방지 강화** |
| **확장성** | 장비 추가 설치 필요 (CapEx) | 클라우드 라이선스 (OpEx) | **신규 지사 개소 시간 1주→1시간** |
| **주요 회선** | MPLS 전용회선 (고비용) | 인터넷 망 (범용) + SD-WAN | **회선 비용 30~50% 절감** |

**2. 타 기술과의 시너지/관계**
- **네트워킹(OS) 관점**: SD-WAN 기술은 **전송 계층(Layer 4)**과 **응용 계층(Layer 7)** 인지를 결합하여 트래픽을 우선순위별로 처리(QoS)한다. 이는 운영체제의 스케줄링 알고리즘이 프로세스를 관리하는 것과 유사한 네트워크 레벨의 스케줄링이다.
- **보안 관점**: **ZTNA (Zero Trust Network Access)**는 "신뢰할 수 있는 내부 네트워크"라는 개념을 없앤다. 즉, 내부망에 접속했다 하더라도 매 요청마다 신원을 확인하므로, 내부에서의 횡적 이동(Lateral Movement)을 차단하는 미래형 보안 모델이다.

**3. 📢 섹션 요약 비유**
> 과거에는 공항 수하물 보안 처리를 위해 모든 승객이 제3국(본사)을 경유해야 했다면, 이제는 **출발지 공항(PoP)에서 보안 검색과 탑승수속을 동시에 처리하고 목적지로 직항**하는 것과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 도입 시나리오 및 의사결정**

- **시나리오 A: 글로벌 법인 연결 (MPLS 대체)**
  - **상황**: 해외 법인 5곳의 본사 VPN 연결 비용이 월 5천만 원이나 듦.
  - **SASE 솔루션**: 로컬 인터넷 회선 + SD-WAN CPE 장치 설치.
  - **결과**: 회선 비용 절감 및 PoP에 의한 지연 시간 최소화 (APAC 지역 접속성 개선).

- **시나리오 B: 재택근무자 보안 강화**
  - **상황**: 직원들이 집에서 개인 PC로 회사 ERP 접속 시 데이터 유출 위험 존재.
  - **SASE 솔루션**: Agent 기반 ZTNA 도입. PC 안티바이러스 점검 후 접속 허용 + 복사/붙여넣기 방지(DLP).
  - **결과**: VPN 트래픽 서버 과부하 해소 및 사용자 불편 개선.

**2. 도입 체크리스트 (Technical & Operational)**

| 구분 | 체크항목 | 설명 |
|:---|:---|:---|
| **기술적** | **PoP(점) 커버리지** | 사용자가 거주하는 지역 근처에 제공업체의 PoP가 존재하는가? (Latency 영향) |
| **기술적** | **상호 운용성(Interop)** | 기존 ID 프로바이더(Active Directory, Okta)와의 연동 여부 |
| **운영적** | **관제 툴 통합** | 로그 및 이벤트를 SIEM(Security Information and Event Management)으로 전송 가능 여부 |
| **보안적** | **규정 준수(Compliance)** | 데이터 보존 기간, 지역별 데이터 주권법 준수 여부 |

**3. 안티패턴 (Anti-Pattern)**
- ❌ **"부분적 도입 실패"**: 네트워크(SD-WAN)만 먼저 도입하고 보안(SSE)은 기존 하드웨어 방화벽에 의존할 경우, **"보안 구멍(Hole)"**이 발생한다. 트래픽은 빨라졌으나 검사는 받지 못하는 상태가 되므로 반드시 통합 도입이 필요하다.

**4. 📢 섹션 요약 비유**
> 자동차를 빠르게 만들려고(SD-WAN)만 하면 될 것이 아니라, **제동 장치와 에어백(보안)을 함께 업그레이드해야 안전한 고속 주행이 가능**합니다. 성능만 높이고 보안을 빼면 날으는 차가 되는 셈입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**1. 정량/정성 기대효과 (ROI)**

| 항목 | 도입 전 (Legacy) | 도입 후 (SASE) | 효과 |
|:---|:---|:---|:---|
| **TCO (총소유비용)** | 회선비 + 장비 구입비 | 구독비(라이선스) | 약 30% 비용 절감 |
| **애플리케이션 성능** | 평균 80ms (Hub 경유) | 평균 20ms (Direct) | **UX 체감 점수 40% 상승** |
| **보안 관리 복잡도** | 지사별 장비 관리 | 중앙 콘솔(Cloud) | **관리 업무 시간 70% 단축** |

**2. 미래 전망 (SASE의 진화)**
향후 3~5년 내 SASE는 단순한 네트워크/보안 융합을 넘어 **AI/ML 기반의 자가 보안(Self-Securing)**으로 진화할 것이다. 예를 들어, 사용자의 행동 패턴(UEBA)을 학