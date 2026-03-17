+++
title = "371-374. 가상 라우팅(VRF)과 MPLS 기술"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 371
+++

# 371-374. 가상 라우팅(VRF)과 MPLS 기술

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **VRF (Virtual Routing and Forwarding)**는 단일 라우터 내의 라우팅 테이블을 논리적으로 분리하여 Address Overlap(주소 중복) 문제를 해결하는 가상화 핵심 기술이며, **MPLS (Multiprotocol Label Switching)**는 이러한 경로 정보를 짧은 Label로 치환하여 L2 스위칭 속도로 L3 라우팅을 수행하는 하이브리드 전송 기술입니다.
> 2. **가치**: 통신 사업자(Carrier) 및 대형 기업은 물리적 망을 재구축하지 않고도 논리적으로 분리된 안전한 VPN 서비스를 제공할 수 있으며, 라우팅Lookup 성능을 획기적으로 높여 QoS(Quality of Service) 보장이 가능한 구조를 확보합니다.
> 3. **융합**: VRF는 L3 VPN 구현의 기반이 되며, MPLS는 SD-WAN, Traffic Engineering(TE)과 결합하여 차세대 네트워크 아키텍처의 핵심 전송 계층으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
가상 라우팅 및 포워딩(VRF)과 다중 프로토콜 라벨 스위칭(MPLS)은 인터넷의 폭발적인 트래픽 증가와 기업 간 보안 통신(VPN)의 요구로 탄생했습니다.
- **VRF (Virtual Routing and Forwarding)**: 하나의 물리적 라우터 내에서 여러 개의 독립된 라우팅 테이블(RIB)을 생성하여, 서로 다른 고객이나 그룹이 동일한 IP 주소 공간을 사용하더라도 트래픽이 섞이지 않도록 완벽히 격리하는 기술입니다.
- **MPLS (Multiprotocol Label Switching)**: 기존의 L3(IP) 계층에서 복잡한 라우팅 Lookup 과정을 거치는 방식에서 벗어나, 패킷 헤더 앞에 고정 길이의 '라벨(Label)'을 붙여 L2(Data Link Layer) 스위칭 속도로 전달하는 '2.5계층' 기술입니다.

**2. 기술적 배경 및 철학**
과거 전용선(Leased Line) 기반의 통신은 비용이 매우 비쌌습니다. 통신사는 저렴한 패킷망(Internet) 기반으로 전용선 수준의 보안과 품질을 제공해야 하는 과제에 직면했습니다.
- **한계**: 기존 IP 라우팅은 Hop-by-Hop 방식으로 매 라우터마다 DIP(Destination IP)를 기반으로 FIB(Forwarding Information Base)를 검색하는 '최장 일치(Longest Prefix Match)' 알고리즘을 수행하므로, 고속 처리에 한계가 있었습니다.
- **혁신**: VRF로 테넌트(Tenant)별 논리적 분리를 확보하고, MPLS를 통해 경로를 미리 정해진 라벨로 매핑(Label Switching)하여 하드웨어 스위칭 속도를 구현함으로써 'IP over ATM'의 복잡성을 제거하고 효율성을 극대화했습니다.

**3. 동작 환경**
이 기술들은 주로 통신 사업자의 백본(Backbone) 망이나 대형 캠퍼스/데이터 센터의 코어(Core) 라우터에서 운영됩니다. Cisco IOS-XR, Juniper Junos 등의 고성능 라우터 OS에서 RD(Route Distinguisher)와 RT(Route Target) 같은 BGP 확장 속성과 결합하여 구현됩니다.

> **📢 섹션 요약 비유**: VRF와 MPLS는 마치 '하나의 거대한 우체국'에서 고객별로 '창구(VRF)'를 완전히 분리하여 다른 사람의 편지가 섞이지 않게 하고, 편지 분류 직원이 주소를 일일이 읽지 않고 '미리 붙여진 번호표(MPLS Label)'만 보고 초고속으로 분류기를 통과시키는 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. VRF의 구조 및 메커니즘**
VRF는 단순한 테이블 분리를 넘어, 라우터 내의 모든 포워딩 결정 요소를 독립시킵니다. 각 VRF는 고유한 인터페이스, 라우팅 테이블, CEF(Forwarding Information Base) 테이블을 가집니다.

| 구성 요소 | 역할 및 내부 동작 | 프로토콜/기술 | 비유 |
|:---:|:---|:---:|:---|
| **VRF Table** | IP 라우팅 테이블(RIB)의 논리적 인스턴스. 각 VRF는 서로 다른 RIB를 유지하여 경로 정보가 격리됨. | RIB (Routing Information Base) | 다른 회사용 전화번호부 |
| **RD (Route Distinguisher)** | **64비트 식별자** (e.g., ASN:NN). 중복되는 IPv4 주소(Prefix) 앞에 붙어 **VPN-IPv4** 주소(96비트)로 변환하여 유일성을 부여함. | **BGP/MPLS VPN** 표준 (RFC 4364) | 사람 이름 앞에 붙는 주민번호 |
| **RT (Route Target)** | **라우팅 정보의 Import/Export 정책**. BGP Extended Community 속성으로, "이 경로는 어디로 흘러들어가고/나가야 할지"를 결정하는 태그. | BGP Extended Community | 택배 배송지 분류용 바코드 |
| **Sub-interface** | 물리적 포트(예: Gi0/0)를 논리적으로 쪼개(Gi0/0.100, Gi0/0.200) 각각 다른 VRF에 바인딩. | 802.1Q (VLAN Tagging) | 한 건물의 여러 입구 |
| **RD <-> VRF Mapping** | 라우터 내부에서 RT를 분석하여 수신한 라우팅 정보를 어느 VRF 테이블에 넣을지 결정하는 매핑 로직. | VRF Selection | 소포 분류 직원의 판단 |

**2. MPLS 아키텍처: Label Switching**

MPLS 망은 크게 경로를 설정하는 **제어 평면(Control Plane)**과 데이터를 전달하는 **데이터 평면(Data Plane)**으로 나뉩니다.

```ascii
[MPLS Domain Packet Flow Architecture]

          [CE Router]         [Provider Edge: LER]         [Provider: LSR]         [Provider Edge: LER]         [CE Router]
   (Customer A)   IP          IP + Label(Swap)    Label(Swap)   Label(Swap)   Label(Pop)   IP          IP
   Host A -------->[Push]--------------------------->[Swap]--------------------->[Pop]---------------> Host B
   (192.168.1.1)   |  (Ingress)                   (Core Transit)            (Egress)           |  (192.168.1.2)
                   |                                                               |
                 [VRF Table A]                                                  [VRF Table A]
```

**[도해 설명]**
1. **Ingress LER (Label Edge Router)**: CE(Customer Edge)로부터 IP 패킷을 수신하면, 목적지 IP를 확인하여 FIB 테이블을 조회한 뒤 해당 경로에 매핑된 **Label(Push)**을 부착하여 MPLS 망으로 내보냅니다.
2. **LSR (Label Switch Router)**: 들어오는 패킷의 **Label만 읽습니다**. LIB(Label Information Base)를 참조하여 들어오는 Label을 나가는 Label로 **교체(Swap)**합니다. IP 헤더를 검사하지 않으므로 매우 빠릅니다.
3. **Egress LER**: 최종 목적지에 도착하면 Label을 **제거(Pop)**하고, 원래의 IP 패킷 상태로 복원하여 CE 라우터로 전달합니다.

**3. 핵심 메커니즘: LFIB와 Label Stack**
- **LFIB (Label Forwarding Information Base)**: LSR의 데이터 평면에 존재하며, `[Incoming Label] → [Outgoing Label] → [Outgoing Interface]` 형태의 매핑 테이블을 하드웨어(Line Card)에 저장하여 O(1)의 시간 복잡도로 포워딩합니다.
- **Penultimate Hop Popping (PHP)**: Egress LER의 부하를 줄이기 위해, 마지막 바로 이전 라우터에서 Label을 제거하는 최적화 기법이 사용됩니다.

> **📢 섹션 요약 비유**: MPLS는 고속도로의 **'하이패스(Hi-Pass) 시스템'**과 유사합니다. 입구 톨게이트(LER)에서 목적지를 확인하고 하이패스 단말기(Label)를 부착하면, 중간 톨게이트들(LSR)은 차량을 세우지 않고 단말기 인식만으로 통행료(Lookup)를 처리하고 통과시킵니다. 출구에서는 하이패스 기기를 제거하고 일반 도로로 진입합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술 비교: IP Routing vs. MPLS**

| 비교 항목 | Traditional IP Routing | MPLS (Label Switching) |
|:---|:---|:---|
| **Lookup 방식** | **Longest Prefix Match** (복잡한 트리 탐색) | **Exact Match** (해시 테이블 검색, 단순 색인) |
| **포워딩 속도** | 소프트웨어 처리 혹은 복잡한 TCAM 필요 | 하드웨어 스위칭 수준의 초고속 처리 |
| **오버헤드** | 홉(Hop)마다 반복적인 헤더 분석 | Label Swap만 수행하므로 CPU 부하 적음 |
| **트래픽 공학 (TE)** | 비효율적 (IGP Cost에 의존) | **Explicit Routing** 가능 (특정 경로로 강제 가능) |
| **계층** | L3 (Network Layer) | L2.5 (介于 L2와 L3 사이) |

**2. VRF와 MPLS의 시너지 (MPLS VPN)**
VRF는 단일 장비 내에서의 격리일 뿐입니다. 이를 지리적으로 분산된 망으로 확장하기 위해 MPLS가 사용됩니다.
- **상관관계**: VRF는 '내부 방', MPLS는 '방과 방을 연결하는 전용 고속 통로'입니다.
- **BGP Extension**: MPLS VPN 구현시 MP-BGP(Multiprotocol BGP)를 사용하여 VPN-IPv4 주소를 교환합니다. 이때 RD가 주소 중복을 막고, RT가 경로를 VRF에 바인딩하는 결합제 역할을 합니다.

**3. 타 영역과의 융합 (Convergence)**
- **보안(Security)**: VRF를 이용한 **VRF-Aware Firewall** 구성 시, 인터넷 트래픽과 내부 트래픽을 논리적으로 완전 분리하여 보안 정책을 간소화할 수 있습니다.
- **성능(QoS)**: MPLS EXP(Experimental) bits(3비트)를 사용하여 L3 라우팅보다 더 세밀한 CoS(Class of Service) 분류가 가능하며, VoIP 트래픽에 대한 우선순위 처리가 용이합니다.

> **📢 섹션 요약 비유**: 기존 IP 라우팅이 '지도를 보고 매번 길을 찾는 운전'이라면, MPLS는 '내비게이션에 저장된 초고속 코스를 무의식적으로 따라가는 레이싱'입니다. 여기에 VRF는 각 팀이 전용 차량을 타고 경쟁하거나 방해받지 않도록 격리된 '전용 주행 선'을 제공합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

1.  **스토리지 리플리케이션 (Storage Replication)**: 데이터 센터 간 대용량 스토리지 동기화
    -   **문제**: 공용 인터넷을 사용할 경우 지터(Jitter)와 보안 이슈로 동기화가 불안정함.
    -   **MPLS VPN 적용**: 통신사 MPLS 망을 통해 대역폭을 보장(QoS)받고, VRF로 격리된 안전한 터널을 구축하여 RPO/RTO(복구 시간 목표)를 준수.

2.  **금융권 본지점 연결 (Hub-and-Spoke)**:
    -   **문제**: 수백 개의 지점이 본점으로 연결되어야 하며, 지점 간 통신은 차단해야 함.
    -   **VRF-Lite 활용**: 본점 라우터에서 VRF를 여러 개 생성하여, 지점별로 독립된 라우팅 테이블을 제공함으로써, 지정된 경로 외의 트래픽 유출을 방지(라우팅 누수 방지).

**2. 도입 체크리스트 (Checklist)**

| 구분 | 점검 항목 | 설명 |
|:---:|:---|:---|
| **기술적** | **Route Leaking 확인** | VRF 간 통신이 필요한 경우, Import/Export Route Policy가 정확히 설정되었는가? |
| **기술적** | **MTU 사이즈** | MPLS Label 추가(4바이트 x 스택 수)로 인해 패킷 크기가 증가하므로, 인터페이스 MTU를 조정(IP MTU 1500 -> 1524 등)했는가? |
| **운영적** | **Label Range** | 전체 망에서 사용할 Label 범위(Static vs Dynamic)를 사전에 계획했는가? |
| **보안적** | **RD/RT 중복** | 잘못된 RT 설정으로 인해 타 고객의 라우팅 정보가 유입되는 사고를 방지했는가? |

**3. 안티패턴 (Anti-Pattern)**
- **L3 장비의 VRF 오남용**: VRF는 보안 솔루션이 아닙니다. VRF만으로는 트래픽 내용을 암호화하지 못하므로, 민감 데이터는 반드시 IPSec VPN과 조합하여 사용해야 합니다.
- **Full Mesh 라우터 문제**: MPLS 망 내의 모든 라우터가 모든 경로를 알면(LDP Full Mesh), 메모리 과부하가 발생합니다. 이를 위해 **LDP (Label Distribution Protocol)**의 IGP Sync 및 **Route Reflector** 구조가 필요합니다.

> **📢 섹션 요약 비유**: 건물을 지을 때 VRF는 '각 입주사의 독립적인 전력/수도 계량기' 설치와 같아서 사용량과 장애를 분리하고, MPLS는 건물