+++
title = "940-1000. 네트워크 시험 빈출 핵심 토픽 요약"
date = "2026-03-14"
[extra]
category = "Exam Topics"
id = 940
+++

# 940-1000. 네트워크 시험 빈출 핵심 토픽 요약

> **핵심 인사이트**
> 1. **본질**: 네트워크 통신은 물리적 신호 전송(L1)부터 애플리케이션 데이터 교환(L7)까지의 계층적(Layered) 협력 시스템이며, 각 계층은 캡슐화(Encapsulation)를 통해 독립성과 효율성을 보장한다.
> 2. **가치**: 올바른 프로토콜 선택과 설계는 대역폭 효율을 극대화하고, Latency(지연 시간)를 최소화하며, RTO(Recovery Time Objective)를 줄여 비즈니스 연속성을 확보한다.
> 3. **융합**: 최근 SDN(Software-Defined Networking)과 가상화(VXLAN/EVPN) 기술은 하드웨어 종속성을 제거하여 Cloud Computing과 AI 인프라의 유연한 확장성을 제공한다.

---

### Ⅰ. 개요 (Context & Background)

**개념**
네트워크 아키텍처는 OSI 7계층(Open Systems Interconnection 7 Layer) 모델을 기반으로 설계된다. 이 모델은 복잡한 통신 과정을 7개의 계층으로 나누어, 각 계층이 특정 역할을 수행하게 함으로써 표준화와 상호 운용성을 보장한다. L1(Physical)은 비트 스트림 전송을, L2(Data Link)는 프레임(Frame) 단위의 오류 제어를, L3(Network)는 패킷(Packet)의 라우팅(Routing)을 담당한다.

**💡 비유**
이는 국제 우편 시스템과 유사하다. 편지 내용을 쓰는 것(사용자 데이터)부터 시작하여, 봉투에 넣고 주소를 쓰는 것(캡슐화), 우편번호 분류(라우팅), 트럭에 싣고 운반하는 것(물리적 전송)까지 각 단계의 담당자가 다르지만, 표준 절차를 따라 편지가 배송되는 원리와 같다.

**등장 배경**
1. **기존 한계**: 초기 중앙집중식 컴퓨팅은 거리가 멀어질수록 신호 감쇠와 잡음으로 인해 통신 품질이 급격히 저하되었다.
2. **혁신적 패러다임**: 패킷 교환(Packet Switching) 방식과 TCP/IP(Transmission Control Protocol/Internet Protocol) 스택의 등장으로, 회선 효율성이 극대화되고 인터넷이 탄생했다.
3. **현재의 비즈니스 요구**: 클라우드, AI, 초연결 시대로 넘어가며 대역폭 요구량이 폭증하고, 실시간 처리가 필수적이 되었다. 이에 따라 하드웨어 의존적인 레거시 네트워크에서 소프트웨어 중심의 유연한 SDN으로 진화 중이다.

**📢 섹션 요약 비유**
네트워크 프로토콜 스택은 **'다층 구조의 택배 물류 센터'**와 같습니다. 최상위 층(응용 계층)에서 물건(데이터)을 포장하면, 각 층을 지나며 배송 라벨(헤더)을 붙이고 운송 수단을 결정합니다. 하부 계층으로 내려갈수록 실제 운송(전송 매체)을 담당하며, 수신측에서는 이를 역순으로 해체하여 물건을 전달합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 (L2 & L3 Focus)**

| 구성 요소 (Component) | 계층 | 역할 (Role) | 내부 동작 및 프로토콜 (Mechanism) |
|:---|:---:|:---|:---|
| **MAC 주소** | L2 | 단말기 식별 | 48비트 고유 번호, 스위치가 이를 기반으로 프레임 전송(Forwarding) |
| **스위치 (Switch)** | L2 | 단말 간 고속 연결 | MAC Address Table을 통해 충돌 도메인(Collision Domain) 분리 |
| **STP (Spanning Tree Protocol)** | L2 | 루프(Loop) 방지 | BPDU(Bridge Protocol Data Unit) 교환을 통해 트리 구조 형성, 불필요한 링크 차단(Blocking) |
| **IP 주소 / 서브넷** | L3 | 논리적 위치 및 라우팅 | 네트워크 ID(상위) + 호스트 ID(하위), 라우터는 이를 기반으로 경로 설정 |
| **라우터 (Router)** | L3 | 네트워크 간 연결 | 라우팅 테이블(Routing Table) 참조하여 최적 경로(Prefix Match) 선택, 브로드캐스트 도메인 분리 |

**2. L2/L3 플레인 데이터 처리 흐름 (ASCII Diagram)**

아래 다이어그램은 호스트 간 통신 시 스위칭과 라우팅이 어떻게 상호작용하는지를 보여줍니다.

```ascii
+----------------------+        +----------------------+        +----------------------+
|      HOST A          |        |     L2 SWITCH        |        |      HOST B          |
|  [IP: 192.168.1.10]  |        |  (Learning/MAC Tab)  |        |  [IP: 192.168.1.20]  |
|  [MAC: AA:AA]        |        |                      |        |  [MAC: BB:BB]        |
+----------+-----------+        +----------+-----------+        +----------+-----------+
           | ^                                ^ |                          ^ |
           | | 1. ARP Request (Broadcast)     | | 2. MAC Learning         | |
           v |                                | v                          | |
        [  L2: Frame Src:AA:AA Dst:FF:FF (Broadcast)  ]                   | |
           |                                | | 3. Forward (Unicast)     | |
           |                                v +--------------------------+ |
           | 4. ARP Reply (Unicast)                                      | |
           v                                                            v |
+----------+-----------+        +----------------------+        +----------+-----------+
|      HOST A          |        |     L2 SWITCH        |        |      HOST B          |
| "Target IP is BB:BB" | <----->|  Stored: BB:BB -> P1 |        | "Target IP is AA:AA" |
+----------------------+        +----------------------+        +----------------------+
```
*(해설: ① 호스트 A는 B의 IP를 모르므로 ARP 브로드캐스트를 전송. ② 스위치는 이를 수신하고 포트 정보를 학습. ③ 스위치는 브로드캐스트를 플러딩(Flooding). ④ 호스트 B가 응답하면 스위치는 이제 BB:BB의 위치를 알게 되어, 이후 트래픽은 유니캐스트로 전환됨.)*

**3. 심층 동작 원리: TCP 혼잡 제어 (Congestion Control)**

L3가 경로를 찾는다면, L4의 TCP는 **신뢰성**과 **혼잡 제어**를 담당합니다.
1. **Slow Start**: cwnd(혼잡 윈도우) 크기를 1부터 지수적으로 증가(2배씩)시켜 대역폭을 탐색합니다. `cwnd = min(cwnd * 2, ssthresh)`
2. **Congestion Avoidance**: ssthresh(Slow Start Threshold)에 도달하면, cwnd 증가폭을 선형적으로 줄여 네트워크 혼잡을 유발하지 않고 최대 전송 속도를 찾습니다.
3. **Fast Retransmit/Recovery**: 3개의 중복 ACK(Dup ACK)를 받으면 즉시 패킷 손실을 간주하고, 재전송 후 ssthresh를 절반으로 줄이는 과정을 거쳐 빠르게 복구합니다.

**4. 핵심 알고리즘 및 코드 (Python-style Pseudo)**

```python
# TCP Reno 혼잡 제어 알고리즘 예시
def tcp_congestion_control(cwnd, ssthresh, event):
    if event == "ACK":
        if cwnd < ssthresh:
            # Slow Start Phase
            cwnd *= 2
        else:
            # Congestion Avoidance Phase
            cwnd += 1 # MSS (Maximum Segment Size)
    
    elif event == "LOSS_3_DUP_ACK":
        # Fast Recovery / Fast Retransmit
        ssthresh = max(cwnd // 2, 2)
        cwnd = ssthresh + 3 # MSS (Inflation)
        
    elif event == "TIMEOUT":
        # Complete restart
        ssthresh = max(cwnd // 2, 2)
        cwnd = 1
    
    return cwnd, ssthresh
```

**📢 섹션 요약 비유**
TCP의 혼잡 제어는 **'물탱크에 물 채우기'**와 같습니다. 처음에는 수도꼭지를 최대로 틀어(NRZ가 아닌 효율적 증가) 빨리 채우다가(Slow Start), 넘칠 것 같은 기준선(ssthresh)에 다다르면 조심스럽게 조금씩만 따라 넣습니다(Avoidance). 만약 물이 흘러넘치면(Timeout), 다시 빈 상태에서 아주 천천히 다시 시작하는 식으로 네트워크의 폭주를 방지합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: 유선 vs 무선 (L2 MAC Layer)**

| 비교 항목 | CSMA/CD (Ethernet) | CSMA/CA (Wi-Fi) |
|:---|:---|:---|
| **Full Name** | Carrier Sense Multiple Access with Collision Detection | Carrier Sense Multiple Access with Collision Avoidance |
| **특성** | **충돌 감지 (Detection)**: 데이터를 보내면서 충돌 여부를 실시간 감지. 충돌 시 Jam 신호 전송 후 재시도. | **충돌 회피 (Avoidance)**: 무선 환경은 자신의 신호 전송 중 충돌을 감지하기 어려움(약한 신호 문제). 따라서 전송 전 RTS/CTS(전송 요청/허가)로 예약 후 전송. |
| **효율성** | 유선에서 매우 높은 효율. 풀 duplex 스위칭에서는 사실상 사용하지 않음. | 무선에서 Overhead가 큼(프리앰블, 인터벌 길음). 802.11ax(Wi-Fi 6)에서는 OFDMA 기반으로 진화. |

**2. 라우팅 프로토콜 비교: IGP vs EGP**

| 구분 | OSPF (Open Shortest Path First) | BGP (Border Gateway Protocol) |
|:---|:---|:---|
| **유형** | Link-State Protocol (링크 상태) | Path Vector Protocol (경로 벡터) |
| **거리 척도** | Cost (대역폭 기반 역수) | AS-Path Length, Policy (정책) |
| **범위** | AS(Autonomous System) 내부 (IGP) | AS 간 연결 (EGP) |
| **수렴 속도** | 빠름 (SPF 알고리즘 재계산) | 느림 (정책 전파 및 루프 방지 탐색) |
| **과목 융합** | 컴구(OS, Kernel Stack 내부 구현), 보안(Authentication) | 네트워크/보안(DDoS 방어, Route Hijacking 방지) |

**3. 가상화 기술 융합 (Overlay vs Underlay)**

*   **Underlay (물리망)**: L3 IP 네트워크 (ISIS, MPLS 등으로 구성). 단순히 패킷을 A 지점에서 B 지점으로 보내는 '도로' 역할.
*   **Overlay (가상망)**: Underlay 위에 논리적으로 구성되는 L2/L3 네트워크 (VXLAN, EVPN). 터널링(Tunneling) 기술을 사용하여 물리적 거리를 무시하고 마치 같은 스위치에 연결된 것처럼 통신.
    *   **시너지**: 클라우드数据中心(Data Center)에서 서버가 이동해도 IP 주소를 유지할 수 있어(Live Migration), 가상 머신(VM)의 유연성이 극대화됨.
    *   **오버헤드**: VXLAN 헤더(50 Byte) 추가로 인한 MTU(Maximum Transmission Unit) 증가 필요.

**📢 섹션 요약 비유**
OSPF와 BGP의 차이는 **'관내 고속도로 vs 국제 항공 노선'**과 같습니다. OSPF는 내부 도로에서 목적지까지 가장 빠른 길(Cost)을 찾는 내비게이션 역할을 하고, BGP는 국가 간(AS 간) 통행 시 정치적 협약이나 비행 규칙(Policy)에 따라 경로를 정하는 외교관 역할을 합니다. VXLAN은 이 고속도로 위에 보이지 않는 **'하이퍼루프 터널'**을 뚫어 물리적 거리를 무시하고 순간이동하게 하는 것입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 매트릭스**

*   **상황 1: 데이터센터 스위칭 아키텍처 설계**
    *   **문제**: 레거시 스패닝 트리(STP)는 대역폭의 50%만 사용(Blocked Port)하고 복구 시간이 30초 이상 소요됨.
    *   **결정**: **Spine-Leaf (CLOS) 아키텍처** 도입 + **ECMP (Equal-Cost Multi-Path)** 사용.
    *   **이유**: 스파인과 리프 간 Full Mesh 구성으로 모든 링크를 활용하고 대역폭을 비선형으로 확장 가능. 병목 현상 해소.
    *   **지표**: Latency < 1ms, 대역폭 가용성 100% (Active-Active).

*   **상황 2: 공공기관 VPN 구축**
    *   **문제**: 인터넷 망을 통해 보안이 요구되는 데이터 전송 필요. L2 투명성이 필요함(프로토콜 독립적).
    *   **결정**: **IPsec (Internet Protocol Security) ESP Mode** + **GRE**.
    *   **이유**: L3 라우팅을 통해 통과하기 쉽고, ESP는 데이터 암호화와 무결성을 보장함. GRE를 통해 IPsec 위에 L2 트래픽 캡슐화 가능.
    *   **대안**: L2TP는 Overhead가 큼.

**2. 도입 체크리스트 (L3 Network Design)**

*   **[ ] 주소 설계**: 공인 IP(Public IP)와 사설 IP(Private IP) 구분, NAT(NAT/PAT) 변환 경로 확보.
*   **[ ] 라우팅 설계**: 루프 방지를 위해 Split Horiz