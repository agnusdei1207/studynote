+++
title = "365-368. BGP(Border Gateway Protocol) 분석"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 365
+++

# 365-368. BGP(Border Gateway Protocol) 분석

> ### 핵심 인사이트 (3줄 요약)
> 1. **본질**: BGP (Border Gateway Protocol)는 인터넷의 핵심 라우팅 프로토콜로, 단순한 거리 최적화가 아닌 정책(Policy) 기반의 **경로 벡터 (Path-Vector)** 알고리즘을 사용하여 AS (Autonomous System) 간의 최적 경로를 선택합니다.
> 2. **가치**: 수만 개의 AS로 구성된 거대한 인터넷망에서 무한 루프를 방지(Routing Loop Prevention)하며, 수십만 개의 경로 정보를 안정적으로 관리하는 확장성(Scalability)을 제공합니다.
> 3. **융합**: OSI 7계층의 L4 TCP(세션 제어)와 L3 IP(라우팅) 기능을 융합하며, SD-WAN 및 MPLS-VPN 등 현대 네트워크 아키텍처의 기반이 됩니다.

+++

## Ⅰ. 개요 (Context & Background)

### 1. 기술적 정의 및 배경
BGP (Border Gateway Protocol)는 인터넷의 게이트웨이 라우터들 간에 도달 가능성 정보(Routing Information)를 교환하기 위해 설계된 **Egp (Exterior Gateway Protocol)**의 표준입니다. 1989년에 처음 정의된 RFC 1105를 거쳐 현재는 RFC 4271(BGP-4)로 표준화되었습니다.

내부 라우팅 프로토콜(IGP, OSPF, RIP 등)이 '속도'와 '거리'에 집중한다면, BGP는 **'정책(Policy)'**과 **'경로(Path)'**에 집중합니다. 이는 서로 다른 행정적 권한을 가진 AS (Autonomous System) 간의 통신을 제어해야 하기 때문입니다. 예를 들어, "A 회사는 우리 회사와 경쟁 관계이므로 우리 네트워크를 통과하지 못하게 하자"와 같은 비즈니스 로직을 라우팅 테이블에 반영할 수 있습니다.

### 2. 작동 특성 및 프로토콜 구조
BGP는 신뢰할 수 있는 전송을 위해 **TCP (Transmission Control Protocol)** 포트 **179**번을 사용합니다. 이는 OSI 7계층에서 L4 세션 관리를 TCP에 위임함으로써, 복잡한 시퀀스 번호 관리나 재전송 메커니즘을 구현하지 않고도 안정적인 메시지 교환이 가능하게 합니다.

BGP 라우터 간의 관계 설정은 수동으로 설정되며, 이를 **Peer (Neighbor)**라고 부릅니다. 일단 Peer가 맺어지면, 초기에 전체 라우팅 테이블을 교환하고, 이후에는 네트워크의 변화가 발생할 때만 **Update 메시지**를 전송하여 대역폭을 절약합니다.

```ascii
[ BGP Protocol Stack & Message Flow ]

+----------------------+
|    BGP Application   | <-- OPEN, UPDATE, NOTIFICATION, KEEPALIVE
+----------------------+
|   TCP (Port 179)     | <-- Reliability, Session State (Established)
+----------------------+
|        IP (L3)       | <-- IP Address, AS Number Payload
+----------------------+

[ FSM (Finite State Machine) Transition ]

Idle -> Connect -> OpenSent -> OpenConfirm -> Established
   ^                                        |
   |________________________________________|
          (Session Fail / Timeout)
```

> **해설**: BGP는 TCP 위에서 동작하는 애플리케이션 계층 프로토콜로 분류되기도 하지만, 실제로는 L3 라우팅 정보를 제어하므로 네트워크 계층의 핵심 프로토콜로 다뤄집니다. FSM(Finite State Machine)은 `Idle` 상태에서 시작하여 TCP 연결 성공 및 `OPEN` 메시지 교환 후 `Established` 상태가 되어야 경로 정보를 교환할 수 있습니다. `Keepalive` 패킷(홀드 타이머의 1/3 주기)을 지속적으로 주고받아 세션이 살아있음을 확인합니다.

📢 **섹션 요약 비유**: BGP의 연결 설정은 **수상 장애물 코스를 함께 통과하는 파트너를 매칭하는 것**과 같습니다. OSPF처럼 주변에 누가 있는지 소리쳐서(Hello) 찾는 것이 아니라, 미리 약속된 사람(TCP 3-way handshake)과 악수를 하고, 서로의 규칙(OPEN)을 확인한 뒤에야 함께 경주(Update)를 시작합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. BGP 경로 선택 메커니즘 (Decision Process)
BGP는 단일 메트릭(예: OSPF의 비용)이 아닌, 여러 단계의 **속성(Attribute)**을 비교하여 경로를 결정합니다. Cisco 등 벤더의 구현에 따라 약간의 차이는 있으나, 일반적인 경로 선택 순서는 다음과 같습니다.

1.  **Weight (Cisco 전용)**: 라우터 로컬 값. 클수록 우선.
2.  **Local Preference**: AS 내부에서 우선시할 외부 경로. 클수록 우선.
3.  **Locally Originated**: Network 명령어나 Aggregate로 직접 생성한 경로.
4.  **AS_Path Length**: AS를 거쳐온 횟수. 짧을수록 우선.
5.  **Origin Code**: 경로의 기원 (IGP < EGP < Incomplete).
6.  **MED (Multi-Exit Discriminator)**: 인접 AS에 진입 경로를 제안. 낮을수록 우선.

### 2. 핵심 속성 분석 (Attributes Table)
BGP의 경로 정보는 TLV(Type-Length-Value) 형식의 속성들을 포함합니다.

| 속성 (Attribute) | 분류 | 역할 및 동작 원리 | 비고 |
|:---|:---|:---|:---|
| **AS_PATH** | Well-Known Mandatory | 경로가 지나온 AS 번호의 리스트입니다. 루프 방지(자신의 AS 번호가 보이면 폐기) 및 핫 포토토 라우팅(Hot Potato Routing)의 핵심 기준입니다. | `ASN` 누적 |
| **Next Hop** | Well-Known Mandatory | 목적지로 가기 위한 다음 홉 IP입니다. iBGP에서는 Next Hop이 변하지 않으므로 재분배 시 주의해야 합니다. | L3 Reachability |
| **Local Pref** | Well-Known Discretionary | AS 내부의 라우터들에게 "이 경로로 나가라"고 통제하는 값입니다. 외부 AS와는 공유되지 않습니다. | **Outbound Policy** |
| **MED** | Optional Non-Transitive | 인접 AS에게 "우리 쪽으로 들어올 때 이 링크를 써라"고 제안하는 값입니다. 낮을수록 좋습니다. | **Inbound Traffic** |
| **Origin** | Well-Known Mandatory | 경로 정보가 어떻게 생성되었는지 표시 (IGP, EGP, Incomplete). |

### 3. 피어링 구조: iBGP와 eBGP
BGP는 피어 관계에 따라 동작 방식이 크게 달라집니다.

*   **eBGP (External BGP)**: 서로 다른 AS 간의 연결. 일반적으로 직접 연결된 인터페이스 IP로 설정하며, **TTL(TTL)** 값이 1로 설정되어 1홉 떨어진 곳과만 통신하려는 경향이 있습니다.
*   **iBGP (Internal BGP)**: 같은 AS 내부의 라우터 간 연결. **Split Horizon Rule**(iBGP로 배운 정보를 다른 iBGP 피어에게 전달하지 않음)을 준수하여 루프를 방지합니다.

```ascii
      [ AS 100 ]               [ AS 200 ]
    +-----------+           +-----------+
    |   R1      | eBGP      |   R3      |
    | (iBGP)    |<--------->| (iBGP)    |
    +-----------+           +-----------+
         |  ^                    ^  |
         |  | iBGP               |  | iBGP
         |  |                    |  |
         v  |                    |  v
    +-----------+           +-----------+
    |   R2      |           |   R4      |
    +-----------+           +-----------+

[ iBGP Full-Mesh Topology Problem ]
R1, R2, R3, R4 모두가 서로 피어링을 맺어야 정보 공유 가능 (n*(n-1)/2)
```

> **해설**: 위 다이어그램과 같이 iBGP는 Full-Mesh(완전 연결)가 기본 동작 원칙입니다. 만약 4대의 라우터가 있다면 총 6개의 세션을 맺어야 하며, 라우터가 100대면 4,950개의 세션이 필요해 scalability에 심각한 문제가 발생합니다. 이를 해결하기 위해 Route Reflector나 Confederation 기술이 사용됩니다.

📢 **섹션 요약 비유**: BGP의 경로 선택은 **외교관이 비행기 티켓을 끊는 과정**과 같습니다. 가장 빠른 비행기(AS_PATH가 짧은 것)를 찾기도 하지만, 본사의 지시(Local Pref, "우리 회사는 대한항공만 써")가 있다면 그것을 따르고, 상대방 회사가 "공항 A로 들어와라(MED)"고 제안하면 그것을 고려하기도 합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 라우팅 프로토콜 비교: BGP vs OSPF
BGP를 이해하려면 내부 라우팅 프로토콜인 OSPF (Open Shortest Path First)와의 명확한 차이를 인지해야 합니다.

| 비교 항목 | BGP (Path-Vector) | OSPF (Link-State) |
|:---|:---|:---|
| **목적** | AS 간 라우팅 (Inter-Domain) | AS 내 라우팅 (Intra-Domain) |
| **알고리즘** | 경로 벡터 (루프 감지: AS_PATH) | 링크 상태 (SPF 알고리즘, Dijkstra) |
| **메트릭** | 정책 속성 (AS 길이, Pref 등) | 비용 (Cost, 대역폭 기반) |
| **수렴 속도** | 느림 (설정, 타이머, TCP 의존) | 빠름 (Hello, LSA 플러딩) |
| **확장성** | 매우 높음 (수십만 개 경로) | 제한적 (Area로 분리 필요) |
| **전송 프로토콜** | TCP (Port 179) | IP (Protocol 89) |

### 2. 계층 구조 융합 (Interaction with IGP)
실제 네트워크에서는 IGP(OSPF)와 BGP를 동시에 운영합니다. 이때 핵심은 **Next Hop 처리**입니다.

*   **Syncronization Rule (과거 규칙)**: 과거에는 "iBGP로 배운 경로가 IGP 라우팅 테이블에 없을 경우 사용하지 않는다"는 규칙이 있었으나, 현재는 대부분 비활성화하여 IGP와 BGP 테이블을 독립적으로 운영합니다.
*   **Next Hop Self**: eBGP에서 받은 경로의 Next Hop IP를 iBGP 내부에 전달할 때, 자신의 인터페이스 IP로 변경하여 내부 라우터가 해당 경로를 찾을 수 있도록 설정해야 합니다.

### 3. 다음 홉 분석 예시
```ascii
[ R1 (AS 100) ] -- eBGP --> [ R2 (AS 200) ] -- iBGP --> [ R3 (AS 200) ]

1. R2가 R1에게 1.1.1.0/24을 광고할 때:
   - Update Packet 내의 Next Hop: R1의 Interface IP (e.g., 10.0.0.1)

2. R2가 R3(iBGP)에게 경로를 전달할 때:
   - Case A (No "next-hop-self"): Next Hop은 여전히 10.0.0.1
   - Case B ("next-hop-self" 설정): Next Hop이 R2의 IP로 변경
```

> **해설**: 만약 R3가 10.0.0.1(R1)에 직접 연결되어 있지 않고 IGP 라우팅이 되지 않는다면, R3는 해당 패킷을 폐기하게 됩니다. 따라서 일반적으로 AS 경계 라우터에서는 `next-hop-self` 옵션을 사용하여 내부 라우터들이 자신을 거쳐가도록 유도합니다.

📢 **섹션 요약 비유**: **OSPF**는 시내의 내비게이션(거리, 속도 최적화)이라면, **BGP**는 국가 간 항로(외교, 조약, 관세 최적화)와 같습니다. 내비게이션(OSPF)으로 집까지 빨리 가는 법을 찾지만, 국가를 넘어갈 때는 비행기 표와 여권(BGP)이 필요한 것입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. iBGP 확장성 문제 해결: Route Reflector (RR)
iBGP의 Full-Mesh 요구 사항은 관리 포인트를 기하급수적으로 늘립니다. 이를 해결하기 위해 **Route Reflector (RR)**를 도입합니다.

*   **개념**: 특정 라우터를 중심(Hub)으로 삼아, 클라이언트 라우터들의 경로 정보를 모아서 반사(Reflect)해주는 역할을 합니다.
*   **동작**: RR은 클라이언트로부터 받은 경로를 다른 클라이언트나 비클라이언트 iBGP 피어에게 전달할 수 있습니다. (일반 iBGP 규칙인 Split Horizon 예외)
*   **주의사항**: RR 배치 시 경로 최적화가 깨질 수 있습니다. (예: R1-RR-R3 연결에서 R1과 R3가 직접 연결되어 있음에도 불구하고 RR을 거쳐서 패킷이 전달될 수 있음)

### 2. Route Dampening (플래핑 방지)
특정 경로가 계속해서 UP/DOWN을 반복(Flapping)하면, 전체 인터넷 라우터가 Update 메시지를 처리하느라 과부하가 걸립니다. BGP는 이를 방지하기 위해 불안정한 경로에 페널티(Penalty)를 부여하여 일시적으로 사용 중지(Suppress)시키는 **Route Dampening** 기능을 제공합니다.

### 3. 실무 시나리오: 트래픽 유입 제어
**문제**: ISP A와 ISP B, 두 곳에서 인터넷 회선을 끌어왔습니다. ISP A 회선이 더 빠르고 저렴하기 때문에, 들어오는 트래픽(Inbound)과 나가는 트래픽(Outbound) 모두 ISP A를 우선시하고 싶습니다.

*   **Outbound Traffic (나가는 트래픽)**: 내 라우터가 결