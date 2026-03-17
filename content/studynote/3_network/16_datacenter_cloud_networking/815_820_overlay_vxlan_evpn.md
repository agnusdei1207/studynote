+++
title = "815-820. 가상화 네트워크와 오버레이(VXLAN)"
date = "2026-03-14"
[extra]
category = "Data Center & Cloud"
id = 815
+++

# 815-820. 가상화 네트워크와 오버레이(VXLAN)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터센터의 L2(Local Area Network 2) 도메인 확장성 한계를 극복하기 위해 **L3(Internet Protocol Network)** 네트워크 위에 **L2 터널(Overlay)**을 구축하여 물리적 위치와 무관한 논리적 연결성을 제공하는 네트워크 가상화 기술.
> 2. **가치**: 기존 VLAN(Virtual Local Area Network)의 4,096개 ID 제한을 24비트 VNI를 통해 약 1,600만 개로 확장하여, 대규모 클라우드(Multi-Tenant) 환경에서의 격리성과 이기종 간 연결성을 확보함.
> 3. **융합**: VXLAN(Virtual Extensible LAN)의 데이터 평면(Data Plane) 캡슐화와 EVPN(Ethernet VPN)의 제어 평면(Control Plane) 기반 MAC 학습을 결합하여, 소프트웨어 정의 네트워킹(SDN)의 표준 아키텍처로 자리 잡음.

+++

### Ⅰ. 개요 (Context & Background)

가상화 네트워크는 물리적인 네트워크 토폴로지 위에 논리적인 네트워크를 중첩(Overlay)시키는 기술입니다. 전통적인 VLAN은 802.1Q 표준에 따라 12비트 ID를 사용하여 최대 4,096개의 네트워크만 생성 가능하여, 퍼블릭 클라우드와 같이 수만 개의 테넌트(Tenant)를 격리해야 하는 환경에서는 심각한 확장성 문제가 발생했습니다.

이를 해결하기 위해 등장한 **Overlay(오버레이)** 기술은 기존의 IP 네트워크인 **Underlay(언더레이)** 위에 가상의 터널을 형성합니다. **VTEP (VXLAN Tunnel End Point)**라는 엔드포인트가 가상 머신(VM)이나 컨테이너에서 나온 L2 프레임을 UDP 패킷으로 캡슐화하여 목적지 VTEP로 전송합니다. 수신 측 VTEP는 이를 다시 decapsulation하여 원본 프레임을 복원합니다. 이 과정에서 물리적인 네트워크(L3)는 단순히 패킷을 운반하는 '도로' 역할만 하게 되며, 논리적 연결성은 소프트웨어적으로 완전히 독립됩니다.

**💡 비유**: 
기존 VLAN은 건물에 전기 콘센트를 설치할 때 벽을 뚫고 고정된 배선을 까는 것과 같아서, 이사(서버 이전)를 가면 배선을 다시 해야 했습니다. VXLAN은 기존 건물의 벽(물리망)을 건드리지 않고, 필요한 곳에 언제든지 설치하고 뜯을 수 있는 '무선 인터넷'이나 '투명한 이동식 터널'과 같습니다.

**등장 배경**:
1.  **기존 한계**: VLAN ID 고갈(4,096개 제한), STP(Spanning Tree Protocol)에 의한 대역폭 절반 낭비, L2 도메인의 브로드캐스트 스톰(Broadcast Storm) 위험성.
2.  **혁신적 패러다임**: **L2 over L4 (UDP)** 구조를 통해 L3 라우팅의 장점(무한 확장, 루프 프리)을 활용하면서 L2 연결성을 제공하는 Network Virtualization using Overlay.
3.  **현재의 비즈니스 요구**: 클라우드 환경에서의 **Live Migration(무중단 서버 이전)** 요구. 서버가 물리적으로 이동하더라도 IP 주소와 네트워크 설정을 유지해야 하는 요구사항이 대두됨.

> **📢 섹션 요약 비유**: 이는 복잡한 도로 교통 체계(언더레이)를 이용하는 시민들(가상 머신)이 지하철 지도(오버레이)만 보고 이동하는 것과 같습니다. 실제 도로가 어찌되었든 지하철 노선만 연결되어 있다면, 승객은 자신이 어디로 이동하는지 물리적인 경로를 알 필요 없이 쉽게 이동할 수 있습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

VXLAN 아키텍처의 핵심은 **캡슐화(Encapsulation)**와 **VTEP**입니다.

#### 1. 주요 구성 요소

| 요소 | 전체 명칭 | 역할 | 내부 동작 | 프로토콜/포트 | 비유 |
|:---|:---|:---|:---|:---|:---|
| **VTEP** | VXLAN Tunnel End Point | 터널의 입출구 | L2 Frame ↔ VXLAN Packet 변환 | UDP 4789 | 터널 입구 검문소 |
| **VNI** | VXLAN Network Identifier | 가상 네트워크 ID | 24비트 ID로 Segment 구분 (1~16M) | - | 아파트 동 번호 |
| **Underlay** | Physical IP Network | 패킷 전달망 | 캡슐화된 패킷을 라우팅 (ECMP 지원) | IP Routing | 고속도로 |
| **NVE** | Network Virtualization Edge | 가상 엔드포인트 | 라우터/스위치 내의 가상 인스턴스 | - | 검문소의 관리자 |

#### 2. VXLAN 패킷 구조 및 캡슐화 흐름

VXLAN은 기존의 이더넷 프레임을 UDP 패킷 안에 감싸서 보냅니다.

```ascii
[VXLAN Encapsulation Process]

1. Original L2 Frame (VM A)
   [Eth][Payload] ...

2. VXLAN Encapsulation (VTEP A)
   [ Outer Eth ][ Outer IP ][ UDP ][ VXLAN ][ Original L2 Frame ]
   |------------ Underlay Header ----------|--- Overlay ---|
                     (UDP Port 4789)     (VNI: 5000)

3. Physical Transmission
   (Switches only see Outer IP Header)

4. Decapsulation (VTEP B)
   [Eth][Payload] ... -> Delivered to VM B
```

#### 3. 심층 동작 원리 (BUM 트래픽 처리)
L2 네트워크는 브로드캐스트, 멀티캐스트, 애니캐스트(Unknown Unicast)인 **BUM 트래픽**을 처리해야 합니다. 물리 네트워크에서는 이를 Flood로 처리하지만, VXLAN은 다음과 같은 방법을 사용합니다.

1.  **Head-end Replication (헤드엔드 복제)**: VTEP가 BUM 트래픽을 수신하면, 자신이 알고 있는 모든 대상 VTEP에게 개별적으로 유니캐스트 패킷으로 복제하여 전송합니다.
2.  **Multicast (멀티캐스트)**: Underlay 네트워크에서 IGMP 등을 사용하여 논리적인 멀티캐스트 그룹을 형성하고, VTEP는 이 그룹으로 패킷을 전송합니다. (물리적 대역폭 절약 가능).

#### 4. 핵심 매커니즘 코드

```python
# VXLAN Encapsulation Logic (Pseudo-code)
def vxlan_encapsulate(original_frame, vni, src_ip, dst_vtep_ips):
    # 1. Create VXLAN Header (VNI included)
    vxlan_header = VXLANHeader(flags=0x08, vni=vni)
    
    # 2. Add UDP Header (Standard Port: 4789)
    udp_header = UDPHeader(src_port=random(), dst_port=4789)
    
    # 3. Add Outer IP Header
    outer_ip = IPHeader(src=src_ip, dst=dst_vtep_ips[0])
    
    # 4. Add Outer Ethernet Header (Next Hop MAC)
    outer_eth = EthHeader(dst_mac=GatewayMAC, src_mac=MyMAC)
    
    # If Traffic is BUM (Broadcast/Unknown/Multicast)
    if is_traffic_bum(original_frame):
        for ip in dst_vtep_ips:
            # Replicate for each VTEP (Head-end replication)
            packet = outer_eth + outer_ip.replace(dst=ip) + udp_header + vxlan_header + original_frame
            send(packet)
    else:
        # Unicast
        packet = outer_eth + outer_ip + udp_header + vxlan_header + original_frame
        send(packet)
```

> **📢 섹션 요약 비유**: VXLAN 캡슐화는 **편지(데이터)**를 **우편함(터널)**에 넣어 **트럭(U/IP 패킷)**에 싣고 보내는 것입니다. 운전자는 편지 내용을 모르고 단지 트럭의 목적지만 봅니다. 편지함을 수거한 우체국(수신 VTEP)만이 트럭에서 편지함을 꺼내 실제 편지를 수신인에게 전달합니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. VLAN vs VXLAN 기술 비교

| 비교 항목 | VLAN (802.1Q) | VXLAN (RFC 7348) |
|:---|:---|:---|
| **ID 공간** | 12비트 (4,096개) | 24비트 (약 1,600만 개) |
| **전송 프로토콜** | L2 (Ethernet) | **L2 over L4 (UDP)** |
| **멀티테넌시** | 데이터센터 규모에 부적합 | 클라우드/Massive VM 환경 적합 |
| **장애 도메인** | STP(Spanning Tree Protocol) 사용 시 대역폭 차단 | **ECMP(Equal-Cost Multi-Path)** 사용으로 전체 대역폭 활용 |
| **MTU (Maximum Transmission Unit)** | 1500 Bytes | **1550 Bytes** (50 Bytes Overhead 고려 필요) |

#### 2. 제어 평면(Control Plane)의 진화: Multicast vs EVPN
초기 VXLAN은 멀티캐스트를 이용해 MAC 주소를 학습했으나, 대규모 환경에서는 관리가 어려웠습니다. 현재는 **EVPN (Ethernet VPN)**이 표준으로 자리 잡았습니다.

```ascii
[EVPN Control Plane Integration]

[VTEP-1]                   [VTEP-2]
   |                          |
   | --- (1) BGP UPDATE --->  |  "I have MAC A (VNI 5000)"
   |                          |
   | <--- (2) BGP UPDATE ---  |  "I have MAC B (VNI 5000)"
   |                          |
(Static MAC Table)        (Static MAC Table)
```

*   **융합 관점 (BGP)**: 기존 라우팅 프로토콜인 **MP-BGP (Multiprotocol BGP)**를 확장하여 MAC 주소 정보를 라우팅 테이블처럼 주고받습니다.
*   **장점**: 스위치가 BGP Update를 통해 목적지 VTEP IP를 즉시 알게 되므로, 첫 통신 때 패킷을 잃어버리는 **Data Plane Learning**의 초기 Flopping 문제를 해결합니다.

> **📢 섹션 요약 비유**: VLAN은 전화번호부가 없는 상태에서 전화를 돌려가며(스팸) 존재 여부를 확인하는 방식(Flooding)입니다. 반면 **VXLAN + EVPN**은 최신 전화번호부(Cloud DB)를 실시간 동기화하여, 버튼 한 번으로 누구에게 전화를 걸지 정확히 찾아내는 스마트 폰 방식입니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오: 클라우드 데이터센터 구축

**상황**: 대규모 IaaS(Infrastructure as a Service) 서버 팜(Farm) 구축. 서버 당 100개 이상의 VM이 운영됨.

**의사결정 프로세스**:
1.  **요구사항 분석**: 테넌트별 격리(VNI 할당) 필수. 물리 서버 간 **Live Migration**(VM 이동) 시 네트워크 끊김 없어야 함.
2.  **아키텍처 선정**: 스파인-리프(Spine-Leaf) 구조의 언더레이 위에 **VXLAN/EVPN** 오버레이 구성.
3.  **MTU 설정**: 물리 스위치와 인터페이스의 MTU를 **9216(Jumbo Frame)** 또는 최소 **1600** 이상으로 설정하여 50바이트 VXLAN 헤더로 인한 패킷 파편화(Fragmentation) 방지.
4.  **운영**: vCenter 또는 OpenStack Neutron을 통해 VNI를 자동 할당 및 관리.

#### 2. 도입 체크리스트

| 구분 | 항목 | 확인 사항 |
|:---|:---|:---|
| **기술적** | **MTU** | End-to-End 경로(스위치, vSwitch, NIC)에서 1550 이상 지원 여부 확인 |
| | **Hashing** | Underlay 스위치에서 Outer IP/UDP Header 기반의 Load Balancing 지원 여부 |
| **운영/보안** | **Security** | VXLAN은 기본적으로 암호화되지 않음. IPsec 등을 통한 터널 암호화 고려 |
| | **Troubleshooting** | Outer Header(IP/UDP)로 Wireshark 패킷 캡처 및 분석 능력 확보 |

#### 3. 안티패턴 (Anti-Pattern)
*   **L3 라우팅이 필요 없는 곳에 과도 적용**: 소규모 온프레미스 환경에서 단순히 VLAN 개수를 늘리기 위해 VXLAN을 도입하면, **UDP 오버헤드**와 **VTEP 관리 복잡도**만 증가하고 이득은 없음.

> **📢 섹션 요약 비유**: 고속도로(언더레이)가 완벽하게 깔려있지 않은 곳에 컨테이너 트럭(VXLAN)을 운행하면, 오히려 트럭이 커서 낡은 도로(오래된 스위치)를 통과하지 못하거나(패킷 폐기), 기름값(오버헤드)만 더 나가는 결과가 됩니다.

+++

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과

| 항목 | 도입 전 (VLAN Only) | 도입 후 (VXLAN) |
|:---|:---|:---|
| **스케일링** | 4,096 Segment 한계 | 16M Segment 확보 (클라우드급) |
| **네트워크 자원** | STP로 인한 링크 차단 (Active/Passive) | ECMP로 전체 대역폭 100% 활용 (Active/Active) |
| **운영 유연성** | 물리적 배선에 종속 (L2 Domain 한계) | 논리적 토폴로지 자유 구성 (Location Independent) |

#### 2. 미래 전망 및 표준
현재 **NVGRE**나 **STT