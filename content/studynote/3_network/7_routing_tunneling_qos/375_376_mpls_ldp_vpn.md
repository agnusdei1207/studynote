+++
title = "375-376. MPLS 제어 및 MPLS VPN"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 375
+++

# 375-376. MPLS 제어 및 MPLS VPN

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IP 라우팅의 복잡한 Hop-by-Hop 처리를 하드웨어 스위칭 수준으로 최적화하기 위해, **MPLS (Multiprotocol Label Switching)** 기술은 **LDP (Label Distribution Protocol)**를 통해 라벨을 매핑하고, **VRF (Virtual Routing and Forwarding)**를 통해 논리적 분리를 수행합니다.
> 2. **가치**: 기존 레이어 3 장비로 레이어 2의 고속 전송 성능을 구현하며, **L3 MPLS VPN**은 별도의 암호화 장비 없이도 라우팅 테이블 분리(Routing Isolation)를 통해 전용선 수준의 보안성과 QoS(Quality of Service)를 제공합니다.
> 3. **융합**: **RSVP-TE (Resource Reservation Protocol - Traffic Engineering)**와 연계하여 트래픽 엔지니어링이 가능하며, SDN(Software Defined Network) 기반의 Segment Routing(SR-MPLS)으로 진화하는 백본 네트워크의 핵심 기술입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
**MPLS (Multiprotocol Label Switching)**는 초기에는 라우터의 처리 속도 향상을 목적으로 등장했으나, 현재는 **VPN (Virtual Private Network)** 서비스 제공과 **TE (Traffic Engineering)**를 위한 핵심 아키텍처로 자리 잡았습니다. 기존의 IP 라우팅은 패킷을 수신할 때마다 목적지 IP 주소를 확인하고 라우팅 테이블을 검색하는 **Longest Prefix Match** 과정을 거치므로 CPU 부하가 큽니다. 반면, MPLS는 패킷 헤더에 짧은 길이의 '라벨(Label)'을 붙여, 중간 라우터가 복잡한 라우팅 계산 없이 라벨만 바꾸어 전달(Swap)하는 방식을 사용합니다.

이때, "이 목적지 네트워크는 이 라벨을 쓰자"라는 약속을 라우터 간에 자동으로 맺게 해주는 제어 프로토콜이 **LDP (Label Distribution Protocol)**입니다. 즉, LDP는 MPLS 망의 '도로 표지판'을 설치하고 관리하는 시스템입니다.

#### 💡 비유: 우편물의 바코드 시스템
기존 IP 라우팅은 주소를 하나하나 읽어서 경로를 찾는 "우편 집배원" 방식이지만, MPLS는 택배 허브 터미널에서 물건을 분류할 때 주소 대신 "바코드(라벨)"만 스캔하여 컨베이어 벨트에 올리는 방식입니다. LDP는 이 바코드 번호를 미리 결정하여 택배사(라우터) 간에 공유하는 업무 매뉴얼입니다.

#### 등장 배경
1.  **기존 한계**: 인터넷 트래픽의 폭발적 증가로 인해 기존 Layer 3 스위칭(NAT, Routing Look-up)의 성능 병목 발생 및 Frame Relay/ATM과 같은 전용망의 높은 비용.
2.  **혁신적 패러다임**: IP 프로토콜의 유연성과 ATM(Asynchronous Transfer Mode)의 고속 전송 장점을 결합(Coast-to-Coast). 데이터 플레인(Data Plane)에서는 라벨 스위칭으로 고속화, 컨트롤 플레인(Control Plane)에서는 IP 라우팅을 유지.
3.  **비즈니스 요구**: 통신사(ISP)가 단일 물리 망 위에서 여러 고객사에게 안전한 망을 임대해 주는 **VPN 서비스**의 수요 폭증.

#### 📢 섹션 요약 비유
"기존 네트워크가 내비게이션을 켜고 매번 지도를 보며 길을 찾아 여행하는 것이라면, MPLS는 고속도로 진입 전에 미리 '목적지별 티켓(라벨)'을 발권받아, 톨게이트에서는 내비게이션 없이 티켓만 찍고 무조건 빨리 달리는 것과 같습니다."

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 및 상세 기능

| 구성 요소 | Full Name | 역할 | 내부 동작 메커니즘 | 비유 |
|:---:|:---|:---|:---|:---|
| **CE** | **Customer Edge** | 고객사 네트워크의 출입구 라우터 | MPLS 헤더를 인식하지 못하며, 표준 IP 패킷을 송수신함. PE와 **IBGP/EBGP** 등으로 라우팅 정보 교환. | 회사 출근 직원 |
| **PE** | **Provider Edge** | 통신사 망의 에지 라우터 (VPN 식별) | **VRF (Virtual Routing and Forwarding)** 테이블을 유지하여 고객별 라우팅을 분리. 수신 IP 패킷에 **이중 라벨(Outer/Inner)**을 부착. | 매표소 및 안내원 |
| **P** | **Provider** | 통신사 망의 코어 라우터 (고속 전달) | 고객 경로 정보(IP)를 알지 못함. 오직 **Outer Label**만 참조하여 **Label Swap** 수행. LFIB(Label Forwarding Information Base) 사용. | 고속도로 톨게이트 |
| **LSR** | **Label Switch Router** | MPLS가 활성화된 라우터 (PE, P 포함) | MPLS shim 헤더를 처리할 수 있는 하드웨어/소프트웨어 능력 보유. | 티켓 인식기 |
| **LIB** | **Label Information Base** | LDP로 학습한 모든 라벨 정보 저장소 | 제어 평면(Control Plane)에 위치. 실제 포워딩에는 사용되지 않으나 LFIB 생성의 근간. | 원장 대장 |
| **LFIB** | **Label Forwarding Information Base** | 실제 포워딩에 사용하는 테이블 | LIB에서 필요 정보를 추려 데이터 평면(Data Plane)으로 로드. In-Label → Out-Label 매핑. | 실무용 업무手册 |

#### 2. LDP (Label Distribution Protocol) 동작 과정
LDP는 IP 라우팅 프로토콜(OSPF, IS-IS 등)이 최적 경로를 계산한 후, 해당 경로에 라벨을 할당하는 단계를 담당합니다. LDP는 TCP 포트 646을 사용하여 신뢰성을 보장합니다.

```ascii
[LDP 라벨 교환 과정 (Downstream Unsolicited Mode)]

   1. 라우팅 완료                   2. 라벨 매핑 생성                 3. LDP Adjacency
[ R1 ] <---------------------> [ R2 ] <---------------------> [ R3 ]
 10.1.1.0/24                  10.1.1.0/24                    10.1.1.0/24
 (Label: Implicit Null)      (Label: 100)                   (Label: 200)

   ① R3은 10.1.1.0/24가 직접 연결됨. 자신의 LIB에 Label 200 할당 후 R2에게 광고.
   ② R2는 R3으로 가기 위해 Label 100을 생성하고 "10.1.1.0/24는 Label 100을 쓰라"고 R1에게 광고.
   ③ R1은 R2가 Label 100을 쓴다는 정보를 LIB에 저장.
```
**해설**:
위 다이어그램은 LDP가 라우터 간에 어떻게 라벨 정보를 유포하는지 보여줍니다.
1.  **Discovery**: Hello 메시지(UDP Multicast)로 이웃(LDP Peer)를 찾습니다.
2.  **Session Establishment**: TCP 세션을 맺고 Capability를 협상합니다.
3.  **Label Advertisement**: 자신이 가진 네트워크 Prefix에 대해 로컬 라벨을 할당하여 이웃에게 보냅니다. 이 과정에서 **FEC (Forwarding Equivalence Class)**를 생성하여 동일한 처리 방식을 가지는 패킷들을 묶습니다.
4.  **Label Retention/Lib Distribution**: 받은 라벨 정보를 LIB에 저장하고, 이를 바탕으로 LFIB를 구성하여 실제 하드웨어 포워딩 엔진에 로드합니다.

#### 3. MPLS VPN (L3VPN) 핵심 알고리즘: RD와 RT
MPLS VPN은 중복되는 IP 주소(예: A사와 B사 모두 192.168.1.0 사용)를 구별하기 위해 **BGP (Border Gateway Protocol)**의 확장 기능을 사용합니다.

*   **RD (Route Distinguisher)**: 64비트 식별자. VPNv4 Prefix(12Bytes)를 만들어 유일성을 보장합니다.
*   **RT (Route Target)**: BGP **Extended Community** 속성. 라우팅 정보의 Import/Export 정책을 결정합니다.

**코드 구조 개념 (Pythonic Pseudo-code)**:
```python
# PE Router Logic
def process_customer_packet(ip_packet, incoming_interface):
    # 1. Interface mapping to VRF
    vrf = interface_map.get(incoming_interface)
    
    # 2. Routing Lookup inside VRF
    vpn_label = vrf.lookup_vpn_label(ip_packet.dest_ip)
    
    # 3. Finding Outer Label (LDP/IGP)
    next_hop_peer = igp.lookup_next_hop(vpn_label.next_hop_ip)
    transport_label = ldp.get_label_for(next_hop_peer)
    
    # 4. Push Labels
    mpls_packet = ip_packet
    mpls_packet.push_inner_label(vpn_label)  # VPN Identification
    mpls_packet.push_outer_label(transport_label) # Transport to Egress PE
    
    send(mpls_packet)
```

#### 📢 섹션 요약 비유
"LDP는 철도 역마다 '서울행은 1번선, 부산행은 2번선'이라는 라벨표를 붙이는 규칙이고, MPLS VPN의 이중 라벨은 '기업 전용 객차'를 연결하는 과정입니다. 안쪽 라벨(Inner)은 '이 기업 직원만 태워라'는 표지이고, 바깥쪽 라벨(Outer)은 '이 열차는 어느 역으로 가라'는 열차 번호입니다."

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: MPLS vs. IP Routing

| 비교 항목 | Traditional IP Routing | MPLS (Label Switching) |
|:---|:---|:---|
| **전달 기준** | IP Header (Destination Address) | Label (Shim Header) |
| **Lookup 방식** | Software-based Longest Prefix Match | Hardware-based Exact Match (Array Index) |
| **속도 및 성능** | 느림 (Hop-by-Hop 처리) | 매우 빠름 (Switching 속도) |
| **Forwarding Equivalence Class (FEC)** | Destination IP 하나가 하나의 FEC | 목적지, 소스, QoS 등 다양한 기준으로 묶을 수 있음 |
| **주요 프로토콜** | OSPF, BGP | LDP (Labeling), MP-BGP (VPN), RSVP-TE |

#### 2. RSVP-TE (Resource Reservation Protocol - Traffic Engineering)
단순 LDP가 IGP(OSPF/IS-IS)가 계산한 최단 경로를 따르는 반면, **RSVP-TE**는 명시적으로 경로를 설정하고 대역폭을 예약합니다.

*   **동작**: PATH 메시지로 경로를 탐색하고, RESV 메시지로 대역폭을 확보합니다.
*   **CR-LDP (Constraint-Based Routing LDP)**: 과거에 경쟁하던 방식이나 현재는 RSVP-TE가 사실상 표준(De Facto Standard)으로 자리 잡았습니다.
*   **과목 융합**:
    *   **네트워크 (NW)**: 망의 효율성을 극대화하여 특정 링크에 과부하(Choke Point)가 걸리지 않도록 분산.
    *   **보안 (Security)**: 경로를 고정함으로써 해킹에 의한 라우팅 테이블 위조 등으로부터 중요 트래픽 보호.

#### 📢 섹션 요약 비유
"기존 IP 라우팅이 '출퇴근길 막히는 일반 도로'를 자동으로 찾아주는 내비게이션이라면, RSVP-TE는 '경찰이 앞서 개차도(예약된 도로)를 확보해주고 진입을 통제하는' 긴급차량용 도로 관제 시스템입니다."

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정

**상황 A: 전국적인 지사를 둔 금융권 본·지점 연결**
*   **요구사항**: 데이터 보안(Routing Isolation), 지연 시간(Latency) 최소화.
*   **판단**: 공용 인터넷을 통한 **IPsec VPN**은 암호화 오버헤드가 있고 경로가 불안정함. **L3 MPLS VPN**을 도입하여 통신사 전용 망을 활용하되, 금융감독원 규정에 맞는 암호화를 병행(가성의 VPN)하는 것이 바람직함.

**상황 B: 동영상 스트리밍 서비스의 트래픽 폭주**
*   **문제**: 특정 PE-PE 구간에서 대역폭 포화 상태.
*   **판단**: LDP만으로는 최단 경로(IGP Cost)로만 보내기 때문에 병목 구간을 피할 수 없음. **RSVP-TE**를 활용하여 물리적으로는 더 길지만 여유 대역폭이 있는 경로로 터널(Explicit Route Object)을 설정하여 우회시켜야 함.

#### 2. 도입 체크리스트

| 구분 | 체크 항목 | 설명 |
|:---|:---|:---|
| **기술적** | 라우터 지원 여부 | PE 라우터의 **VRF** 라이선스 및 라벨 스택 처리 능력(TCAM Size) 확인 필수. |
| **운영적** | 경로 설계 | Route Reflector(iBGP RR) 설계 및 Full-mesh 부하 방지 계획. |
| **보안적** | 주소 중복 관리 | RD(Route Distinguisher) 할당 정책 수립 (ASN:NN 형태 등). |

#### 3. 안티패턴 (Anti-Pattern)
*   **MPLS Label Range 중복**: 관리자가 라벨을 수동 할당할 때 범위가 겹치면 트래픽이 루핑(Loooping) 발생. LDP 자동 할당 범위와 수동 할당 범위를 철저히 분리해야 함.
*   **Route Leaking**: VRF 간 라우팅 누수 설정 실수로 인해 경쟁사 네트워크로 트래픽 유출. RT Import/Export 필