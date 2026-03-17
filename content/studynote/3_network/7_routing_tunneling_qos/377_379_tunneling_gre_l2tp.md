+++
title = "377-379. 터널링 기술: GRE와 L2TP"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 377
+++

# 377-379. 터널링 기술: GRE와 L2TP

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: **터널링 (Tunneling)**은 이질적인 네트워크망 사이에서 프로토콜 간의 호환성을 유지하거나, 공용망(Internet)을 통해 사설망의 데이터를 안전하게(혹은 논리적으로 분리하여) 전송하기 위한 **캡슐화 (Encapsulation)** 기술입니다.
> 2. **가치**: 물리적인 회선 설치 비용을 절감하고, **IPv6**와 같은 새로운 프로토콜 도입 시 기존 인프라를 활용한 **부드러운 전환 (Smooth Transition)** 전략을 제공하며, 원격지 사무간 연결 시 구간별 보안 정책 적용이 가능합니다.
> 3. **융합**: 독립적으로는 보안이 취약한 GRE와 L2TP를 **IPsec (Internet Protocol Security)**과 결합(GRE over IPsec, L2TP/IPsec)하여 강력한 **VPN (Virtual Private Network)** 솔루션으로 구현하며, 라우팅 프로토콜의 확장성을 보장하는 핵심 인프라로 작용합니다.

---

### Ⅰ. 개요 (Context & Background)

**터널링 (Tunneling)**은 데이터 링크 계층이나 네트워크 계층의 패킷을 다른 프로토콜의 페이로드(Payload) 영역에 삽입하여 전송하는 기술입니다. 마치 택배 박스(원본 패킷)를 또 다른 배송 박스(캡슐화 헤더)에 넣어 목적지까지 보내는 것과 같습니다. 이를 통해 물리적으로 떨어져 있는 두 개의 사설망을 마치 하나의 LAN(Local Area Network)인 것처럼 연결하거나, 인터넷이라는 거대한 공용망 위에 논리적인 사설 통로를 구축할 수 있습니다.

기술적으로 터널링은 **Encapsulation (캡슐화)**, **Transmission (전송)**, **Decapsulation (역캡슐화)**의 3단계로 동작합니다. 송신 라우터(Tunnel Entry)는 원본 패킷 앞에 새로운 헤더를 붙이고, 수신 라우터(Tunnel Exit)는 이 헤더를 제거하여 원본 패킷을 복원합니다.

이 기술이 등장한 배경은 크게 두 가지입니다. 첫째, **IPv6**로의 전환 과정에서 기존 **IPv4** 인프라 위에서 IPv6 패킷을 전송해야 하는 필요성(Transition Mechanism)이 있었습니다. 둘째, 물리적인 전용선(Leased Line) 임대료가 비싼 기업에게 인터넷망을 활용한 저비용 **VPN** 구축의 필요성이 대두되었습니다.

> 💡 **비유**
> 서울에서 부산으로 이사를 갈 때, 짐(데이터)을 차에 싣고 고속도로(인터넷)를 달린다고 상상해 보세요.
> 만약 짐이 그대로 노출되면 위험하고, 고속도로 진입이 불가능한 경우도 있습니다.
> 이때 짐을 이사 박스(캡슐화)에 싸고, 다시 트럭(터널 헤더)에 싣고
> 트럭 안에는 사원(암호화)을 태워서 운전하듯, 터널링은 데이터를 안전하고 규칙에 맞게 운반하는 기술입니다.

> 📢 **섹션 요약 비유**: 터널링은 복잡한 지하철 역사(공용 인터넷)를 지나갈 때, 승객(원본 데이터)이 아무나 방해하지 못하도록 특별한 객차(터널 프로토콜)에 태워서 운행하는 것과 같습니다. 승객은 어디를 지나는지 모르지만, 출발역과 도착역 사이를 안전하게 이동하게 됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

터널링 기술의 핵심은 헤더 구조와 캡슐화 과정에 있습니다. 여기서는 가장 대표적인 **GRE (Generic Routing Encapsulation)**와 **L2TP (Layer 2 Tunneling Protocol)**의 아키텍처를 분석합니다.

#### 1. 구성 요소 및 역할

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/포트 (Protocol/Port) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Passenger Protocol** | 실제 사용자 데이터 | 터널링 대상이 되는 원본 패킷 (IPv4, IPv6, IPX 등) | 가변 | 승객 (짐) |
| **Carrier Protocol** | 캡슐화를 담당하는 터널링 프로토콜 | Passenger를 감싸는 외부 프로토콜 (GRE, L2TP) | GRE (Protocol 47), L2TP (UDP 1701) | 특수 운송 컨테이너 |
| **Transport Protocol** | 전송을 위한 기반 프로토콜 | Carrier Protocol을 전달하는 프로토콜 (주로 IPv4/IPv6) | IP (Protocol Number varies) | 고속도로 네트워크 |
| **Tunnel Interface** | 논리적인 입구/출구 | 물리적 인터페이스(eth0) 위에 생성된 가상 인터페이스 (tun0, gre0) | Software Logical Interface | 터널 입구 게이트 |

#### 2. GRE (Generic Routing Encapsulation) 심층 분석

**GRE**는 시스코(Cisco)에서 개발하여 IETF 표준(RFC 1701, RFC 2784)으로 채택된 가장 범용적인 L3 터널링 프로토콜입니다. "Generic"이라는 이름처럼, 이더넷 프레임을 제외한 대부분의 3계층 프로토콜(IPv4, IPv6, IPX, AppleTalk 등)을 캡슐화할 수 있습니다.

**GRE 패킷 구조 (Data Plane)**

```ascii
+-------------------------------------------------------+
|              Delivery Header (Outer IP)               |
|  (Ver: 4, IHL, TOS, Total Length, ID, Flags, Frag)   |
|  (Source IP: 1.1.1.1,   Dest IP: 2.2.2.2)             |
+-------------------------------------------------------+
|              GRE Header (Protocol 47)                 |
|  (C, R, K, S, s, Recur, A, Flags, Ver)               |
|  (Protocol: 0x0800 for IPv4)                          |
+-------------------------------------------------------+
|              Passenger Protocol (Original Packet)     |
|  (Source IP: 10.1.1.1, Dest IP: 10.2.2.1, Data...)    |
+-------------------------------------------------------+
```

*   **동작 매커니즘**:
    1.  **입력**: 라우터의 Tunnel Interface(`tunnel0`)로 Destination IP가 `10.2.2.1`인 패킷 수신.
    2.  **캡슐화**: 라우팅 테이블을 참조하여 `10.2.2.1`은 Tunnel Destination `2.2.2.2`로 도달함을 확인.
    3.  **헤더 추가**: 원본 패킷 앞에 GRE 헤더(Protocol Type 0x800) 추가 후, 다시 Outer IP 헤더(Source: `1.1.1.1`, Dest: `2.2.2.2`) 추가.
    4.  **전송**: 외부망으로 패킷 송신.
    5.  **복구**: 수신 라우터(`2.2.2.2`)가 수신 후 GRE 헤더와 Outer IP를 제거(Decapsulation)하고 원본 패킷을 내부망으로 전송.

*   **주요 특징**:
    *   **멀티캐스트(Multicast) 지원**: GRE 터널은 멀티캐스트 패킷 전송을 지원합니다. 이는 **OSPF (Open Shortest Path First)**, **EIGRP (Enhanced Interior Gateway Routing Protocol)** 등 라우팅 프로토콜의 인접성(Neighbor Adjacency)을 맺는 데 필수적입니다. (IPsec AH/ESP만으로는 멀티캐스트 전송이 어려움)
    *   **보안 취약점**: GRE는 단순히 데이터를 싸는 역할만 할 뿐, 암호화(Encryption)나 인증(Authentication) 기능을 전혀 제공하지 않습니다. 중간에 패킷을 가로채면 내용이 그대로 노출됩니다. 따라서 실무에서는 반드시 **IPsec**과 함께 사용하여 **GRE over IPsec** 구성을 해야 합니다.

#### 3. L2TP (Layer 2 Tunneling Protocol) 심층 분석

**L2TP**는 **PPTP (Point-to-Point Tunneling Protocol)**의 강점과 **L2F (Layer 2 Forwarding)**의 안정성을 결합하여 IETF(RFC 2661)에서 표준화된 프로토콜입니다. 주로 원격지 사용자가 인터넷을 통해 회사 내부망에 접속하는 **Remote Access VPN**에 사용됩니다.

*   **특징**: L2TP 자체는 UDP(User Datagram Protocol) 포트 **1701**번을 사용하며, **PPP (Point-to-Point Protocol)** 프레임을 캡슐화합니다.
*   **캡슐화 구조**: L2TP는 PPP 프레임(사용자의 IP 패킷 등이 포함됨)을 감싸고, 이를 다시 UDP/IP 패킷으로 감쌉니다.

```ascii
[ L2TP over IP Packet Structure ]

+-------------------------------------------------------+
|         Outer IP Header (UDP Datagram)                |
|  (Src: ISP_IP,  Dst: Corp_VPN_Gateway_IP)             |
+-------------------------------------------------------+
|         UDP Header (Port 1701)                        |
+-------------------------------------------------------+
|         L2TP Header (Tunnel ID, Session ID)           |
+-------------------------------------------------------+
|         PPP Frame (Header, Control, Data)             |
+-------------------------------------------------------+
|         Original IP Packet (User Data: e.g., HTTP)    |
+-------------------------------------------------------+
```

*   **동작 원리 (Control Plane + Data Plane)**:
    1.  **LAC (L2TP Access Concentrator)**: 사용자(ISP 등)의 접속을 받아들이는 장비.
    2.  **LNS (L2TP Network Server)**: 터널의 종점이 되는 기업 게이트웨이.
    3.  L2TP는 **Control Connection**과 **Session**의 두 가지 논리적 연결을 관리합니다. 제어 연결은 터널의 유지 관리(Keepalive)를 담당하고, 세션은 실제 사용자 데이터 전송을 담당합니다.

> 📢 **섹션 요약 비유**: **GRE**는 어떤 짐이든(이기종 프로토콜) 가리지 않고 실어 나를 수 있는 '만능 컨테이너 트럭'입니다. 단, 트럭 벽이 투명해서 내용물이 다 보입니다. 반면 **L2TP**는 승객(PPP 세션)이 타고 내리는 구체적인 '버스 노선'과 같습니다. 승객은 버스 정류장(LAC/LNS)에서 인증을 거쳐 탑승하고, 목적지까지 이동합니다. 둘 다 도둑(해킹)을 막기 위해서는 트럭이나 버스 전체를 안전한 창고(IPsec)에 넣고 운행해야 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

터널링 기술은 단독으로 사용되기보다 다른 보안 기술과 결합하거나, 서로 다른 네트워크 환경을 연결하는 융합의 핵심입니다.

#### 1. 기술 비교: GRE vs. L2TP vs. IPsec Tunnel Mode

| 비교 항목 | GRE (Generic Routing Encapsulation) | L2TP (Layer 2 Tunneling Protocol) | IPsec Tunnel Mode |
|:---|:---|:---|:---|
| **표준화 기구** | IETF (RFC 2784) | IETF (RFC 2661) | IETF (RFC 4301) |
| **OSI 계층** | Layer 3 (Network) | Layer 2 (Data Link) over Layer 3 | Layer 3 (Network) |
| **캡슐화 대상** | 다양한 3계층 프로토콜 (IPv4, IPv6, IPX...), 멀티캐스트 | **PPP** 프레임만 캡슐화 가능 (단일 연결 지향) | IP 패킷만 캡슐화 가능 |
| **전송 프로토콜** | IP (Protocol 47) | UDP (Port 1701) | IP (Protocol 50/51) |
| **암호화 지원** | 지원 안 함 (IPsec 필수) | 지원 안 함 (IPsec 필수) | **지원함** (ESP, AH) |
| **주요 용도** | **Site-to-Site VPN**, 멀티캐스트 라우팅 지원 필요 시 | **Remote Access VPN** (사용자 인증 중시) | 보안이 필수적인 Site-to-Site VPN |
| **오버헤드** | Header(4byte) + Delivery Header | UDP Header(8byte) + L2TP Header + PPP Header | ESP Header + IV + Padding (상대적으로 큼) |
| **NAT 통과** | 가능 (Proto 47 지원 필요) | 용이 (UDP 기반) | NAT-T (UDP 4500) 필요 시 가능 |

#### 2. 융합 관점: 시너지 및 오버헤드

**A. GRE over IPsec (The Enterprise Standard)**
기업망에서 가장 널리 쓰이는 결합체입니다. IPsec은 **유니캐스트(Unicast)** 트래픽에 대해서만 암호화/복호화를 수행하므로, 라우팅 프로토콜(**OSPF**, **EIGRP**)의 **멀티캐스트(Multicast)** 패킷을 전달할 수 없습니다.
*   **해결책**: GRE로 멀티캐스트 패킷을 캡슐화하여 유니캐스트처럼 만든 뒤, 이를 다시 IPsec으로 감싸서 전송합니다.
*   **오버헤드**: [Original][GRE][ESP/AH][Outer IP] 구조로 헤더가 중첩되어 **MTU (Maximum Transmission Unit)** 문제가 발생할 수 있으므로, 인터페이스 `ip mtu` 설정이나 TCP MSS 조정이 필요합니다.

**B. L2TP/IPsec (The Remote Access Standard)**
윈도우(Windows)나 macOS 기본 VPN 클라이언트가 지원하는 표준입니다.
*   **시너지**: L2TP가 사용자 인증(PPP Authentication, PAP/CHAP)과 터널 생성을 담당하고, IPsec이 데이터 암호화를 담당하여 보안과 사용자 관리의 두 마리 토끼를 잡습니다.