+++
title = "363-364. IS-IS(Intermediate System to Intermediate System) 프로토콜"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 363
+++

# 363-364. IS-IS(Intermediate System to Intermediate System) 프로토콜

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: ISO (International Organization for Standardization) 표준을 기반으로 OSI (Open Systems Interconnection) 환경에서 탄생했으나, 현재는 TCP/IP 네트워크를 지원하는 **Integrated IS-IS**로 진화하여 대형 ISP (Internet Service Provider) 백본의 핵심 라우팅 프로토콜로 자리 잡았다.
> 2. **가치**: IP 계층(Layer 3)에 의존하지 않고 데이터 링크 계층(Layer 2) 위에서 직접 독립적으로 운영되므로, IP DoS (Denial of Service) 공격이나 표미(Payload) 변조로부터 라우팅 시스템을 격리할 수 있는 **극한의 안정성과 확장성**을 제공한다.
> 3. **융합**: TLV (Type-Length-Value) 구조를 통해 IPv6, MPLS (Multiprotocol Label Switching), TRILL 등 신기능을 유연하게 수용하며, OSPF (Open Shortest Path First)와 함께 링크 상태 라우팅의 양대 산맥을 형성한다.

---

### Ⅰ. 개요 (Context & Background)
**IS-IS (Intermediate System to Intermediate System)**는 OSI 프로토콜 스택의 네트워크 계층인 **CLNP (Connectionless Network Protocol)** 환경에서 라우팅 정보를 교환하기 위해 ISO 10589 표준으로 정의되었다. 초기 설계 목적은 OSI 환경이었으나, 인터넷의 폭발적인 성장과 함께 **Dual IP** 기술이 추가되어 **Integrated IS-IS** 형태로 현재의 IP 네트워크를 지원하게 되었다.

OSPF가 IP 패킷 내부에 캡슐화되어 IP 프로토콜 번호 89를 사용하여 동작하는 반면, IS-IS는 **IP 헤더와 완전히 독립적**이다. IS-IS는 고유의 **NSAP (Network Service Access Point)** 주소 체계(NET)를 사용하며, 데이터 링크 계층의 LLC (Logical Link Control) 서비스를 통해 직접 전송된다. 즉, 라우터의 IP 스택이 다운되더라도 IS-IS 프로세스는 정상적으로 동작할 수 있으며, IP DoS 공격이 발생해도 라우팅 컨버전스(Routing Convergence)에는 영향이 없는 **강력한 격리성(Isolation)**을 가진다.

#### OSI 계층에서의 위치 비교

```ascii
┌─────────────────────────────────────────────────────────────┐
│                      7. Application Layer                    │
├─────────────────────────────────────────────────────────────┤
│                      4. Transport Layer (TCP/UDP)            │
├─────────────────────────────────────────────────────────────┤
│                  3. Network Layer (IP Packet)                │
│   ┌───────────────────┐          ┌─────────────────────┐    │
│   │  OSPF             │          │   IP Data (User)    │    │
│   │  (IP Protocol 89) │          │                     │    │
│   └───────────────────┘          └─────────────────────┘    │
├───────────────────────────────────┬─────────────────────────┤
│              2. Data Link Layer   │                         │
│   ┌───────────────────────────────▼─────────────────────┐  │
│   │  IS-IS (Direct Encapsulation)                     │  │
│   │  NLPID: 0xFE (CLNP) / 0x83 (IP)                    │  │
│   └────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                  1. Physical Layer (Ethernet)                │
└─────────────────────────────────────────────────────────────┘
```
*그림 1-1: IS-IS와 OSPF의 계층적 위치 차이*
*   **해설**: OSPF는 IP 패킷 안에 실려가는 '애플리케이션'처럼 취급되어 IP 레벨의 문제 발생 시 영향을 받을 수 있습니다. 반면, IS-IS는 IP 밑바닥(데이터링크)에 기관차처럼 자리 잡고 있어, 위에서 IP 패킷이 폭주하거나 공격받아도 기관차(IS-IS)는 선로(링크) 상태를 안정적으로 파악할 수 있습니다.

**💡 섹션 요약 비유**
OSPF가 '고속버스 터미널(네트워크) 내부에서 손님(IP)끼리 서로 지도를 주고받으며 길을 찾는 시스템'이라면, IS-IS는 **'터미널 건물 바닥에 깔린 지능형 도로 센서 네트워크'**와 같습니다. 건물 안에 사람이 없거나 난리가 나도, 도로 센서 네트워크는 독자적으로 동작하며 교통 흐름을 제어하는 시스템 그 자체로 존재하기 때문입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

IS-IS는 OSPF와 유사하게 다익스트라(Dijkstra) 알고리즘을 사용하는 **Link-State Protocol**이지만, 네트워크 구성을 인식하는 방식이 다르다. OSPF가 인터페이스 단위로 Area를 할당하는 **Link-State Database(LSDB)** 구성 방식을 취하는 반면, IS-IS는 **물리적 라우터(Router) 단위로 Area를 정의**하고, 이를 **Level**이라는 계층 개념으로 나눈다.

#### 1. 핵심 구성 요소 및 용어 (5개 이상 상세)

| 요소명 (Element) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/필드 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **IS (Intermediate System)** | 라우터 자체 | 경로 계산 및 LSP 생성/플러딩 | **NET ID** 식별 | 지도 제작소 |
| **ES (End System)** | 일반 호스트 (End Device) | 라우팅 참여 불필요, IS에게 정보 요청 | **ES-IS** 프로토콜 | 지도를 읽는 여행자 |
| **NET (Network Entity Title)** | 라우터 식별자 (ID) | Area ID + System ID + SEL(00)로 구성 | **AFI**/IDI/DSP | 주민등록번호 |
| **LSP (Link State PDU)** | 상태 정보 패킷 | 링크 상태, 비용, 대역폭 정보 포함 | **PDU Type**, Remaining Lifetime | 도로 교통 상황 팩스 |
| **DIS (Designated IS)** | 대표 라우터 (LAN) | OSPF의 DR/BDR 역할 수행 (Preemption 없음) | Priority(0~127) | 구역장 |

#### 2. 라우팅 계층 구조 (Level 1 vs Level 2)

IS-IS는 대규모 네트워크의 확장성을 확보하기 위해 2단계 계층 구조(Hierarchy)를 사용한다.

*   **Level 1 (Intra-Area Routing)**: 동일 Area 내부의 경로 정보만 교환하고 유지한다. L1 라우터는 자신의 Area 정보만 알고 있으며, 타 Area로 가는 트래픽은 반드시 **L1/L2 라우터**로 향하게 된다(OSPF의 Stub Area와 유사).
*   **Level 2 (Inter-Area Routing)**: 서로 다른 Area 간의 연결을 담당한다. L2 라우터들은 백본(Backbone)을 형성하며, 모든 L2 라우터가 연속되어 있어야 한다.

```ascii
[ Area 1 ]          [ Area 2 (Backbone) ]          [ Area 3 ]
   L1 ─┐          ┌─── L1 ─┐          ┌─── L1           ┌─── L1
       │          │        │          │                │
   [ L1/L2 ] ──── [ L2 ] ─ [ L1/L2 ] ─ [ L2 ] ── [ L1/L2 ]
(초진입 지점)   (백본 코어)    (경계 지점)   (백본 코어)   (초진입 지점)
       ▲          │        ▲          ▲                ▲
       └──────────┴────────┴──────────┘                │
                <──── L2 Connectivity ────>            │
                 (연결성이 끊기면 Area 단절)             │
```
*그림 2-1: IS-IS의 계층적 라우팅 구조와 L1/L2 흐름*
*   **해설**: Area 1의 L1 라우터는 Area 1 내부의 길만 알고 있습니다. Area 3으로 가기 위해 자신의 **L1/L2 라우터**로 패킷을 보냅니다. L1/L2 라우터는 이를 L2 백본으로 넘기고, L2 백본을 따라 목적지 Area에 있는 L1/L2 라우터로 전달됩니다. 이후 다시 L1 라우터를 통해 최종 목적지로 향합니다.

#### 3. 핵심 동작 메커니즘: PDU 및 TLV

IS-IS는 **CLNP (Connectionless Network Protocol)** 기반의 패킷 구조를 가지며, 정보를 나르는 단위를 **PDU (Protocol Data Unit)**라고 부른다. OSPF가 IP 헤더 필드를 고정해서 쓰는 것과 달리, IS-IS는 **TLV (Type-Length-Value)** 포맷을 사용하여 매우 유연하다.

```c
/* IS-IS PDU Header Structure (Conceptual C Representation) */
struct IS_IS_PDU {
    uint8_t  Intradomain Routing Protocol Discriminator; // 항상 0x83
    uint8_t  Length Indicator;                           // 헤더 길이
    uint8_t  Version/Protocol ID Extension;              // 버전 1
    uint8_t  ID Length;                                  // System ID 길이 (보통 6)
    uint8_t  PDU Type;                                   // 15(Hello), 18(L1 LSP), 20(L2 LSP), 24(CSNP)
    uint8_t  Version;                                    // 항상 1
    uint8_t  Reserved;
    uint8_t  Maximum Area Addresses;
    /* 이후로 TLV 가변 길이 필드가 옴 */
};
```

**TLV (Type-Length-Value)의 예시**:
*   `Type 132`: IP Internal Reachability (IPv4 경로 정보)
*   `Type 135`: IPv6 Reachability (IPv6 지원)
*   `Type 10`: Authentication (인증 정보)

이러한 구조 덕분에 프로토콜 자체를 수정하지 않고도, 새로운 TLV만 추가하면 **IPv4/IPv6 듀얼 스택**, **SR-MPLS (Segment Routing)**, **Traffic Engineering** 등의 확장 기능을 무중단으로 추가할 수 있다.

**💡 섹션 요약 비유**
IS-IS의 **TLV 구조**는 **'수납용 짐가방(Tagged Luggage)'**과 같습니다. 가방 자체(프로토콜)는 바뀌지 않고 필요에 따라 옷(정보)을 넣었다 뺐다 할 수 있는 것입니다. 반면 OSPF는 자칫하면 옷이랑 가방이 한 몸처럼 봉제되어 있어 새 옷을 넣으려면 가방째 바꿔야 할 때가 있습니다. 또한 **L1/L2 구조**는 시내(도시) 버스가 시외(고속도로) 버스 터미널(L1/L2)을 통해서만 다른 도시로 갈 수 있는 것과 같은 **교통 체계**와 흡사합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. IS-IS vs OSPF (Deep Technical Comparison)

| 비교 항목 | OSPF (IP Standard) | IS-IS (ISO Standard) | 실무적 영향 |
|:---|:---|:---|:---|
| **전송 계층** | IP (Protocol 89) | **Data Link Layer (SAP 0xFE)** | IS-IS는 IP DoS 공격에 라우팅이 영향받지 않음 (IP독립적) |
| **경로 선택 단위** | **Interface** | **Router** | IS-IS 구성이 간단하나, Area 경계 설정이 유연하지 못함 |
| **Area 구성** | Area 단위 Interface 설정 | 라우터 전체가 하나의 Area에 소속 | 대규모 망 관리 시 IS-IS 설정 오류 가능성 낮음 |
| **Neighbor 형성** | Network Type에 따라 특정 IP 주소 필요 | **Multicast MAC** 기반 (SNAP) | IS-IS는 IP 주소 설정 없이도 이웃 형성 가능 |
| **확장성 (Scaling)** | ABR(Area Border Router)의 필터맅 기능 강함 | L1/L2 경계에서의 필터맅 기능 상대적 약함 | 초대형 망에서 IS-IS의 DB 처리 속도가 빠름 |
| **패킷 형식** | 복잡한 다중 패킷 구조 | 유연한 **TLV** 구조 | 새로운 기능(Traffic Eng. 등) 추가 시 IS-IS가 유리 |

#### 2. 타 영역과의 융합 (Convergence)

*   **MPLS (Multiprotocol Label Switching)**: IS-IS는 **Traffic Engineering (TE)** 확장 기능을 통해 MPLS 네트워크의 LSP (Label Switched Path) 설정을 위한 핵심 프로토콜로 활용된다. 특히 대형 통신사의 코어 라우터(Cisco NCS, Juniper PTX)에서는 OSPF보다 IS-IS를 훨씬 더 선호한다.
*   **네트워크 보안 (Security)**: IS-IS는 데이터링크 계층에서 동작하므로, 기본적으로 인터넷 방향으로의 직접적인 접근이 불가능하다. 이는 외부 해커가 라우팅 테이블을 직접 조작하는 **Direct Routing Attack**을 방어하는 레이어 0.5의 보안 계층을 제공한다. (물론 인증(Authentication) 메커니즘도 내장되어 있다.)

#### 3. 성능 분석 (Metric)

IS-IS는 기본적으로 **Cost(비용)** 메트릭을 사용하며, 이는 대역폭(Bandwidth)에 기반하지만 관리자가 임의 설정이 가능하다. 최근 버전에서는 **Wide Metric**을 지원하여 24비트 메트릭 값을 통해 대규모 네트워크의 세밀한 경로 조정이 가능하다.

**💡 섹션 요약 비유**
OSPF와 IS-IS의 선택은 **'자동차 네비게이션(소프트웨어)'**와 **'내비게이션 내장 자동차(하드웨어)'**의 선택과 유사합니다. OSPF는 앱을 업데이트하듯 기능을 추가하고 인터페이스마다 설정을 다르게 할 수 있어 유연합니다(엔터프라이즈 환경). 반면 IS-IS는 자동차의 하부 시스템(통신사 백본)처럼 구조적 안정성과 극한의 속도/확장성이 중요하며, 차량 교체(대규모 망 변경)가 아닌 이상 기본 틀을 유지하며 최적화