+++
title = "285. 네트워크 계층의 핵심 3기능"
date = "2026-03-14"
[extra]
category = "Network Layer"
id = 285
+++

# 285. 네트워크 계층의 핵심 3기능

> **핵심 인사이트**
> 1. **본질**: 네트워크 계층(OSI 7 Layer의 Layer 3)은 서로 다른 네트워크 간의 **논리적 연결(Logical Connectivity)**을 담당하며, **라우팅(Routing)**, **포워딩(Forwarding)**, **혼잡 제어(Congestion Control)**의 3대 메커니즘을 통해 종단 간(End-to-End) 전달을 수행합니다.
> 2. **가치**: 글로벌 라우팅 프로토콜(如 BGP)을 기반으로 한 비용 최적화와 하드웨어 스위칭을 통한 나노초(ns) 단위의 전송 지연 최소화가 핵심 가치이며, 이는 인터넷의 확장성(Scalability)을 보장합니다.
> 3. **융합**: 전송 계층(TCP/UDP)의 흐름 제어(Flow Control)와 상호 보완하며, 소프트웨어 정의 네트워킹(SDN, Software Defined Networking)의 등장으로 제어 평면(Control Plane)과 데이터 평면(Data Plane)의 분리가 가속화되고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**네트워크 계층(Network Layer)**은 OSI 7계층 모델의 제3계층(Layer 3)에 위치하며, 물리적으로 분리된 여러 네트워크를 거쳐 데이터 패킷이 목적지까지 도달할 수 있도록 **종단 간(End-to-End) 전달 서비스**를 제공하는 계층입니다. 데이터 링크 계층(Layer 2)이 직접 연결된 호스트 간의 전달(Hop-to-Hop)을 담당하는 반면, 네트워크 계층은 **라우터(Router)**라는 중계 장치를 통해 논리적 주소(IP Address)를 기반으로 경로를 설정하고 패킷을 전달합니다.

### 2. 등장 배경 및 필연성
① **네트워크 확장성의 한계**: 단일 브로드캐스트 도메인(예: 모든 장비가 스위치로만 연결된 평면 구조)은 ARP(Access Resolution Protocol) 브로드캐스트 폭탄 및 MAC 주소 테이블의 한계로 인해 규모 확장이 불가능합니다.
② **논리적 분리의 필요성**: 물리적인 배선 구조와 무관하게 논리적인 그룹(Subnet)을 구성하여 관리 효율성을 높이고 보안 경계를 설정할 필요가 생겼습니다.
③ **비즈니스 요구**: 전 세계적으로 흩어진 지사 간의 통신 및 인터넷 연결을 위해서는 다양한 프로토콜과 미디어를 통합할 수 있는 **표준화된 주소 체계(IP)**와 **라우팅 기술**이 절실했습니다.

### 3. 핵심 기능 3요소 상관관계
네트워크 계층의 작동은 크게 '길을 찾는 행위(Routing)', '길로 보내는 행위(Forwarding)', '길의 막힘을 관리하는 행위(Congestion Control)'로 구분됩니다. 이는 운영 체제(OS)의 메모리 관리(페이징/세그먼테이션)와 유사한 추상화를 제공합니다.

```ascii
┌──────────────────────────────────────────────────────────────────────┐
│                     네트워크 계층 (Layer 3)의 추상화                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   [Host A]                              [Host B]                     │
│      │                                     │                         │
│      │  (1. 경로 계산: Routing)             │                         │
│      └───────────🧠 (Control Plane)────────────────────┐            │
│                      ↓ Global Knowledge               │            │
│   ┌────────────────────────────────────────────────────┴───┐      │
│   │            네트워크 코어 (라우터 들)                      │      │
│   │                                                        │      │
│   │  [R1]───(2. 패킷 이동: Forwarding)───▶ [R2]            │      │
│   │    │              ↑              │      │             │      │
│   │    └──────────────┘              └──────┘             │      │
│   │                   (3. 상태 모니터링: Congestion Ctrl) │      │
│   └────────────────────────────────────────────────────────┘      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

> **📢 섹션 요약 비유**: 네트워크 계층은 **'국제 배송 물류 센터'**와 같습니다. 물류 센터는 단순히 이웃 집에 배달하는 것이 아니라(데이터 링크), 항공편과 대륙을 건너는 배경경로를 설정하고(라우팅), 실제 화물을 분류하여 트럭에 싣고(포워딩), 창고가 터지지 않도록 입고량을 조절하는(혼잡 제어) 총괄 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

네트워크 계층의 기술적 깊이는 제어 평면(Control Plane)과 데이터 평면(Data Plane)의 분리에서 시작됩니다.

### 1. 구성 요소 상세 분석 (Architecture Components)
네트워크 계층의 패킷 전달을 담당하는 라우터(Router)의 내부는 다음과 같이 세분화됩니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **라우팅 프로세서**<br>(Routing Processor) | 제어 평면의 뇌 | 경로 결정 알고리즘 실행, 라우팅 테이블 생성 및 관리 | RIP, OSPF, BGP | 물류 센터의 관리자 |
| **입력 포트**<br>(Input Port) | 패킷 수신후 처리 | L2(물리적/링크) 처리 ▶ L3(IP 헤더 검사) ▶ 스위칭 패브릭으로 전달 | ACL, Queuing | 하역장 크레인 |
| **스위칭 패브릭**<br>(Switching Fabric) | 내부 버스 | 입력 포트에서 출력 포트로 패킷을 물리적으로 전달 (Switching) | Bus, Crossbar, Memory | 컨베이어 벨트 |
| **출력 포트**<br>(Output Port) | 패킷 송신 전 처리 | 큐잉(Queuing) 및 스케줄링 수행 후 링크로 전송 | FIFO, Priority Queuing | 적재 트럭 대기열 |
| **라우팅 테이블**<br>(Routing Table) | 경로 매핑 DB | 목적지 IP(Destination) ▶ 다음 홉(Next Hop) 매핑 정보 저장 | Software DB | GPS 내비게이션 지도 |

### 2. 핵심 기능 1: 라우팅 (Routing)
라우팅은 네트워크의 지형(Topology)을 파악하여 최적의 경로를 계산하는 과정입니다.

#### 알고리즘 분류
*   **링크 상태(Link-State, 예: OSPF)**: 전체 네트워크 맵을 다익스트라(Dijkstra) 알고리즘으로 그려 최단 경로(SPF) 계산.
*   **거리 벡터(Distance-Vector, 예: RIP)**: 이웃에게 들은 정보를 바탕으로 Bellman-Ford 알고리즘으로 홉 카운트(Hop Count) 계산.

```ascii
[라우팅 경로 계산 예시: 목적지 Network D로 가는 최적 경로]

      (Cost 10)          (Cost 1)
   [A]───────────────▶[B]───────▶[D]
    │                    │
    │ (Cost 5)           │ (Cost 2)
    ▼                    ▼
   [C]───────────────────┘
    │      (Cost 1)
    └───────────────────▶[D]

    🔍 계산 (A 입장):
    1. A->B->D 경로 비용: 10 + 1 = 11
    2. A->C->D 경로 비용: 5 + 1 = 6  ✅ (최적 경로 선정)
    3. 라우팅 테이블 갱신: "To D, go to C"
```
> **해설**: 위 다이어그램은 라우터 A가 목적지 D까지의 비용(Cost)을 계산하는 과정을 보여줍니다. 링크 상태 알고리즘을 사용하는 라우터는 각 링크의 비용을 합산하여 가장 비용이 낮은 경로(여기서는 C를 거치는 경로, 비용 6)를 선택하여 라우팅 테이블에 기록합니다. 이는 **Control Plane**의 소프트웨어적 연산 영역입니다.

### 3. 핵심 기능 2: 포워딩 (Forwarding)
포워딩은 라우팅 테이블을 참조하여 실제 패킷을 이동시키는 데이터 평면(Data Plane)의 기능입니다. 이는 속도가 생명이므로 하드웨어(ASIC) 로직으로 구현됩니다.

#### 포워딩 과정 (Match Action)
1.  **Match**: 수신 패킷의 헤더에서 목적지 IP 주소 추출.
2.  **Lookup**: 라우팅 테이블(또는 FIB, Forwarding Information Base)에서 **Longest Prefix Match(최장 접두어 일치)** 검색 수행.
3.  **Action**: 해당 출력 포트로 패킷을 전달하고 TTL(Time To Live) 값을 1 감소시킴.

```ascii
[라우터 내부 포워딩 로직 (Pseudo Code)]

function Forwarding(Packet p):
    dest_ip = p.Header.DestinationAddress
    # Step 1: Longest Prefix Match
    best_match = LONGEST_PREFIX_MATCH(Routing_Table, dest_ip)
    
    if best_match is NULL:
        Drop(p)               # No route found
        Send_ICMP_Error(p)    # Destination Unreachable
    else:
        # Step 2: Decrement TTL
        p.Header.TTL = p.Header.TTL - 1
        if p.Header.TTL <= 0:
            Drop(p)           # Time Exceeded
        else:
            # Step 3: Switch to Output Port
            Switch_Fabric.send(best_match.next_hop_port, p)
```
> **해설**: 위 코드는 라우터가 수행하는 포워딩의 핵심 로직을 나타낸 것입니다. 가장 중요한 점은 소프트웨어가 아닌 전용 회로(ASIC)에서 'Lookup'과 'Decrement TTL' 과정이 나노초 단위로 처리된다는 것입니다. 이는 CPU(Central Processing Unit)의 개입 없이 패킷이 지나가는 길(Path)을 물리적으로 열어주는 스위칭 역할을 합니다.

### 4. 핵심 기능 3: 혼잡 제어 (Congestion Control)
혼잡 제어는 네트워크 자원(Bandwidth, Buffer)의 초과 요구를 방지하는 메커니즘입니다. **TCP의 혼잡 제어**와 **네트워크 장비의 혼잡 제어** 두 가지 관점이 있습니다.

| 구분 | TCP (End-to-End) | 네트워크 (Network-assisted) |
|:---|:---|:---|
| **접근 방식** | 송신 호스트가 네트워크 상태를 추측하여 전송율 조절 | 라우터가 직접 트래픽을 제어하거나 피드백 전송 |
| **대표 기법** | AIMD (Additive Increase Multiplicative Decrease) | **RED** (Random Early Detection), **ECN** (Explicit Congestion Notification) |
| **메커니즘** | 패킷 손실(Loss)이 발생해야 혼잡을 인지 | 버퍼가 가득 차기 전에 미리 패킷을 무작위로 폐기하여 경고 |

```ascii
[RED (Random Early Detection) 알고리즘 개념도]

버퍼 점유율 (Buffer Occupancy)
  100% │           ▲
      │           │  (Max Threshold 초과 시: 모두 폐기)
      │           ├────────────── Packet Drop All
      │           │
      │      ●────┼────────────── Packet Drop Prob = P_max
      │      │    │
  50% │      │    │  (Min/Max 사이: 확률적 폐기)
      │      │    │
      │──────┴────┴────────────── Packet Drop Prob = 0
      │    (Min Threshold 미만 시: 그대로 전달)
      │
      └────────────────────────────────────▶ 시간 (Time)

  * 목적: 꼬리에 몰리는 패킷(Tail Drop)으로 인한 전체 동기화(Global Synchronization) 현상 방지
```
> **해설**: RED 알고리즘은 라우터의 큐가 가득 차버려(Drop Tail) 모든 패킷이 무시되는 '전체 동기화' 현상을 막기 위해, 큐가 일정 수준(Min Threshold) 이상 차면 아직 가득 차지 않았더라도 **무작위로 패킷을 버리기 시작**합니다. 이를 통해 송신자들에게 "혼잡이 시작되었으니 속도를 줄이라"는 신호를 조기에 줌으로써 네트워크의 처리량(Throughput)을 극대화합니다.

> **📢 섹션 요약 비유**: 라우팅은 **'내비게이션 지도 업데이트'**입니다. 도로가 막히거나 새로운 길이 뚫리면 지도 데이터 자체를 갱신하는 과정입니다. 포워딩은 **'교차로에서의 방향 지시'**입니다. 운전자가 내비를 보고 "오른쪽으로 가라"는 지시를 받았을 때, 실제로 핸들을 오른쪽으로 꺾어 트럭을 진로시키는 순간의 결정입니다. 혼잡 제어는 **'고속도로 진입 램프 미터링(Ramp Metering)'**입니다. 본선 도로가 꽉 차지 않도록 진입로 신호등을 통해 차량을 일정 시간 멈춰가게 하여 교통 체증을 사전에 예방하는 시스템입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 라우팅 vs 포워딩: 제어 평면 vs 데이터 평면
두 개념은 서로 혼용되지만, 시스템 아키텍처 관점에서는 명확히 구분됩니다.

| 비교 항목 | 라우팅 (Routing) | 포워딩 (Forwarding) |
|:---|:---|:---|
| **평면 (Plane)** | 제어 평면 (Control Plane) | 데이터 평면 (D