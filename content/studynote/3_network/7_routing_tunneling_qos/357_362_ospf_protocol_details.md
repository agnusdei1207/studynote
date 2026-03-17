+++
title = "357-362. OSPF(Open Shortest Path First) 프로토콜"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 357
+++

# 357-362. OSPF (Open Shortest Path First) 프로토콜

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: OSPF (Open Shortest Path First)는 **링크 상태(Link-State)** 알고리즘 기반의 표준 라우팅 프로토콜로, 각 라우터가 전체 네트워크 토폴로지를 **LSDB (Link State Database)**로 저장하고 **SPF (Shortest Path First)** 알고리즘(다익스트라)을 통해 최단 경로를 자율 계산합니다.
> 2. **가치**: Distance Vector(거리 벡터) 방식의 느린 수렴(Slow Convergence)과 루프(Loop) 문제를 근본적으로 해결하며, **Cost (대역폭 역수)** 기반 메트릭으로 빠른 경로 복구와 로드 밸런싱이 가능하여 대규모 기업망의 안정성을 보장합니다.
> 3. **융합**: **Area (영역)** 계층 구조를 통해 라우팅 트래픽을 분리하고 확장성을 확보하며, VPN (Virtual Private Network)과 MPLS (Multiprotocol Label Switching) Core 망에서의 표준 IGP (Interior Gateway Protocol)로 자리 잡았습니다.

---

### Ⅰ. 개요 (Context & Background)

OSPF는 **IETF (Internet Engineering Task Force)**가 표준화한 **IGP (Interior Gateway Protocol)**로, **AS (Autonomous System)** 내부에서 라우팅 정보를 교환하기 위해 사용됩니다. 기존의 **RIP (Routing Information Protocol)**가 홉(Hop) 카운트만을 기준으로 하여 대역폭을 고려하지 못하고 수렴 속도가 느린 단점을 극복하기 위해 개발되었습니다. OSPF는 **IP (Internet Protocol)** 계층 위에서 직접 작동하며(프로토콜 번호 89), 신뢰성을 위해 **TCP (Transmission Control Protocol)**가 아닌 자체적인 신뢰성 메커니즘을 사용합니다.

핵심 철학은 "소문을 듣고 전파하는 것"이 아니라 "정확한 지도를 그려 스스로 계산하는 것"입니다. 각 라우터는 링크의 상태(Up/Down, Bandwidth)를 담은 **LSA (Link State Advertisement)**를 멀티캐스트로 인접 라우터에 전송하고, 수신한 정보를 바탕으로 **LSDB (Link State Database)**를 구축합니다. 이 데이터베이스는 네트워크의 그래프 형태이며, 라우터는 이 그래프에 대해 **SPF (Shortest Path First)** 알고리즘을 수행하여 자신을 루트로 하는 최단 경로 트리(SPT)를 생성합니다.

* **메트릭 계산 (Cost)**:
    $$Cost = \frac{Reference Bandwidth}{Interface Bandwidth}$$
    기본 대역폭($100Mbps \approx 10^8 bps$)을 기준으로 하며, 고속 인터페이스일수록 비용이 낮아 선택될 확률이 높아집니다.
* **패킷 타입**: Hello, DB Description, LS Request, LS Update, LS Ack 등 5가지 타입이 존재합니다.

> 💡 **비유**: RIP가 "동네 방네 소문으로 길을 묻는 것"이라면, OSPF는 "모두가 실시간 교통상황이 담긴 내비게이션 지도를 서버에서 다운받아 자기 위치에서 목적지까지 최적 경로를 계산하는 것"과 같습니다.

```ascii
      [ RIP (Distance Vector) ]           [ OSPF (Link State) ]
      +------------------------+           +------------------------+
      |   Routing Table        |           |   Link State DB (Map)  |
      |   (Distance, Vector)   |           |   (Topology Graph)     |
      +------------------------+           +------------------------+
               |                                     |
               v                                     v
      "주변에게 듣고 그대로 믿음"           "전체 지도를 보고 수학적 계산"
      (Rumors, Slow Convergence)            (Facts, Fast Convergence)
```

**📢 섹션 요약 비유**: OSPF의 도입은 종이 지도를 보고 길을 찾던 것에서 **실시간 위성 내비게이션**으로 업그레이드하는 것과 같습니다. 단순한 방향이 아닌 정확한 거리와 교통 상황(링크 상태)을 기반으로 수학적으로 최적 경로를 산출하기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

OSPF의 대규모 네트워크 지원 능력은 **Area (영역)**라는 계층적 설계에서 나옵니다. 모든 라우터가 하나의 거대한 지도를 가지고 계산하면 메모리와 CPU 부하가 걸리기 때문입니다.

#### 1. 주요 구성 요소 (5개+)
| 구성 요소 (Component) | 전체 명칭 (Full Name) | 역할 및 내부 동작 | 프로토콜/상태 |
|:---|:---|:---|:---|
| **ASBR** | **Autonomous System Boundary Router** | OSPF 도메인과 외부 다른 AS(RIP, BGP 등)를 연결하는 경계 라우터. 외부 경로를 **Type 5 LSA**로 재분배함. | Redistribute |
| **ABR** | **Area Border Router** | 여러 Area(Area 0와 일반 Area)에 동시에 속한 라우터. Area 간 라우팅 정보 요약(**Type 3 LSA**) 및 전달 담당. | Inter-Area Routing |
| **DR** | **Designated Router** | Broadcast/NBMA 네트워크에서 LSA 교환의 중심 역할. 인접 라우터 수를 최소화하여 LSA 플러딩 부하 감소. | Router ID: Highest Priority |
| **BDR** | **Backup Designated Router** | DR 장애 시 즉시 역할을 승계하기 위해 대기하는 예비 라우터. | Router ID: 2nd Highest |
| **Internal Router** | Internal Router | 하나의 Area 내부에만 존재하는 일반 라우터. | Intra-Area Routing |

#### 2. OSPF 2단계 인접성 성립 과정
OSPF Neighbor가 데이터를 교환하기 위해선 다음 과정을 거쳐 **Full Adjacency** 상태가 되어야 합니다.

```ascii
[State Transition Diagram]

   (1) Down         (2) Init           (3) 2-Way           (4) ExStart
 [OFFLINE]  --->  [HELLO RCVD]  --->  [BIDIRECT]  --->  [MASTER/SLAVE]
                     |                   |                    |
   Neighbor ID 확인  |          (Hello 참조)             DB Desc
   (Myself found)    |                                  (Seq# Negotiation)
                     v                                      v
                 [BDR etc]                             (5) Exchange
                 (No Adjacency)                <------------------->
                      ^                     [LSA Header Exchange]
                      |                              |
                      |                              v
                 (7) Full                     (6) Loading
                 [SYNC COMPLETE] <------------ [LSA Request]
                                            (Missing Info Update)
```

**해설**:
1.  **Down -> Init**: 라우터가 Hello 패킷을 수신하면 Init 상태로 변하며, 수신한 Hello 패킷에 자신의 ID가 있으면 2-Way로 넘어갑니다.
2.  **2-Way**: DR/BDR 선출을 위한 투표가 끝난 단계입니다. Point-to-Point 링크가 아니라면 여기서 멈추고 라우팩 정보는 DR을 통해 간접 수신합니다.
3.  **ExStart -> Exchange**: **DD (Database Description)** 패킷을 교환하여 LSDB의 마스터/슬레이브를 정하고, LSA 헤더 목록을 주고받습니다.
4.  **Loading**: 상대방이 가지고 있고 내가 없는 LSA를 **LSR (Link State Request)**으로 요청하고, **LSU (Link State Update)**로 받습니다.
5.  **Full**: LSDB가 완전히 동기화된 상태로, 라우팅 계산이 가능합니다.

#### 3. SPF 알고리즘 구현 (Pseudo-code)
```python
# Dijkstra Algorithm for SPF Tree Construction
def calculate_spf(router_id, lsdb):
    # 1. Initialize
    shortest_path_tree = {}
    candidates = {router_id: 0} # Distance to root is 0
    
    while candidates:
        # 2. Select node with lowest cost in candidates
        current_node = min(candidates, key=candidates.get)
        current_cost = candidates.pop(current_node)
        
        shortest_path_tree[current_node] = current_cost
        
        # 3. Examine neighbors (Links in LSDB)
        for neighbor, link_cost in get_neighbors(current_node, lsdb):
            new_cost = current_cost + link_cost
            if neighbor not in shortest_path_tree:
                if neighbor not in candidates or new_cost < candidates[neighbor]:
                    candidates[neighbor] = new_cost
                    
    return shortest_path_tree
```

**📢 섹션 요약 비유**: OSPF의 Area 구조와 DR/BDR 개념은 **대기업 조직 체계**와 같습니다. 본사(Area 0)를 중심으로 지사들(Area 1~)이 연결되어 있고, 각 부서 내의 업무 보고는 팀장(DR)에게만 모아 전달하여 사장님(네트워크)의 업무 과부하를 막는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

OSPF는 범용성이 뛰어나지만, 상황에 따른 올바른 설계가 필수적입니다.

#### 1. 라우팅 프로토콜 심층 비교 (정량적 지표)

| 비교 항목 | OSPF (Link State) | RIP (Distance Vector) | EIGRP (Advanced Distance Vector) |
|:---|:---|:---|:---|
| **수렴 속도 (Convergence)** | 매우 빠름 (Trigger Update) | 느림 (Periodic 30s) | 매우 빠름 (DUAL) |
| **메트릭 (Metric)** | Cost (Bandwidth 기반) | Hop Count (Max 15) | Composite (BW, Delay, Load...) |
| **루프 발생 (Loop)** | 없음 (SPF 알고리즘) | 발생 가능 (Split Horizon 필요) | 없음 (DUAL 알고리즘) |
| **네트워크 규모** | 대규모 (Area로 계층화) | 소규모 | 중대규모 |
| **프로토콜 특성** | 표준 개방형 (Open Standard) | 표준 개방형 | Cisco 전용 (Proprietary) |
| **자원 소모** | CPU/메모리 많이 사용 | 매우 적음 | 중간 |
| **L3/L4 의존성** | L3 (IP Proto 89) | L3 (UDP 520) | L4 (RTP - IP Protocol 88) |

#### 2. 네트워크 융합 관점
*   **Security와의 융합**: OSPF 인증(Plain Text, MD5)을 지원하여 라우팅 정보 도청이나 스푸핑을 방지할 수 있습니다. 최신 보안 요건에는 필수적입니다.
*   **MPLS와의 시너지**: **MPLS (Multiprotocol Label Switching)** 망의 코어 라우팅 프로토콜로 OSPF가 가장 많이 사용됩니다. MPLS 레이블 스위칭을 위한 LDP (Label Distribution Protocol)와 연동되어, IP 라우팅 정보를 기반으로 레이블 바인딩 정보를 생성합니다.
*   **오버헤드 관리**: Area를 나누면 Type 1, 2 LSA를 Area 외부로 유출하지 않아 **라우팅 트래픽(Routing Overhead)**을 획기적으로 줄입니다.

```ascii
[LSA Flooding Scope Comparison]
+---------------------------------------------------------------+
|  OSPF Domain (AS)                                             |
|                                                               |
|  +------------------------+      +------------------------+   |
|  |   Area 1 (Non-Backbone)|      |   Area 2 (Non-Backbone)|   |
|  |                        |      |                        |   |
|  |  [Type 1 LSA: Router]  |      |  [Type 1 LSA: Router]  |   |
|  |  [Type 2 LSA: Network] |      |  [Type 2 LSA: Network] |   |
|  |        (Flooding       |      |        (Flooding       |   |
|  |         inside Area)   |      |         inside Area)   |   |
|  +-----------|------------+      +-----------|------------+   |
|              | ABR (Summary)                 | ABR            |
|              v                               v                |
|        +---------------------------------------------------+  |
|        |        Area 0 (Backbone)                          |  |
|        |                                                   |  |
|        |  [Type 3 LSA: Summary] --(Inter-Area Traffic)-->  |  |
|        |  [Type 4 LSA: ASBR Summary]                       |  |
|        +---------------------------------------------------+  |
|                                                               |
+---------------------------------------------------------------+
```

**📢 섹션 요약 비유**: RIP가 "구호"라면, OSPF는 "정밀 설계도"입니다. 구호는 멀리 갈수록 왜곡되지만(Hop Count 제한), 설계도는 누가 보더라도 동일한 해석이 가능합니다. Area 구조는 설계도를 "기계부", "전기부"처럼 책으로 나누어 관리하는 엔지니어링 철학과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 OSPF를 설계할 때는 단순한 통신 연결을 넘어 **안정성(Redundancy)**과 **확장성(Scalability)**을 고려해야 합니다.

#### 1. 실무 시나리오 및 의사결정
1.  **망 장애 상황 (Link Failure)**:
    *   **상황**: ABR과 Core 라우터 간의 광케이블 절단 발생.
    *   **대응**: OSPF는 즉시 **Hello 타이머(Dead Interval)**를 통해 감지하고, SPF 알고리즘을 재수행하여 백업 경로로 트래픽을 우회시킵니다.
    *   **튜닝**: Hello 타이머를 10초에서 1초로 낮추면 **RTO (Recovery Time Objective)**를 줄일 수 있으나, CPU 부하가 증가하므로 트레이드오프가 필요합니다.
2.  **대역폭 불균형 (Unequal Cost Load Balancing)**:
    *   **상황**: 두 경로의 대역폭이 100Mbps와 1Gbps인데 라운드로빈으로 1:1 트래픽 분산이 일어남.
    *   **해결**: OSPF는 기본적으로 **ECMP (Equal-Cost Multi-Path)**만 지원합니다. 1Gbps 경로만 사용하거나, 인터페이스당 Cost 값을 조정하여 두 경로의 Cost를 동일하게 맞춘 뒤 로드밸런싱을 수행해야 합니다.

#### 2. 도입 체크리스트
*   **기술적**: 모든 라우터의 **Router ID**가 고유한가? (IP 주소와 혼동 주의)
*   **설계**: **Hub-and-Spoke** 구조에서 DR/BDR 설정은 적절한가? (Hub 라우터를 DR로 우선순