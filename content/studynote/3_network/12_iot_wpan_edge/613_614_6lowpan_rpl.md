+++
title = "613-614. IoT 네트워크의 IP 연동: 6LoWPAN 및 RPL"
date = "2026-03-14"
[extra]
category = "IoT & Edge"
id = 613
+++

# 613-614. IoT 네트워크의 IP 연동: 6LoWPAN 및 RPL

## 핵심 인사이트 (3줄 요약)
> **1. 본질**: IEEE 802.15.4 등의 자원 제약적인 물리 계층 위에서 IPv6 패킷을 효율적으로 운반하기 위한 **6LoWPAN (IPv6 over Low-Power Wireless Personal Area Network)** 적응 계층과, 노드의 에너지 효율을 고려한 경로를 형성하는 **RPL (IPv6 Routing Protocol for Low-Power and Lossy Networks)** 라우팅 프로토콜의 조화.
> **2. 가치**: IPv6 헤더 압축을 통해 전송 효율을 약 90% 이상 개선하고, RPL의 **DODAG (Destination Oriented Directed Acyclic Graph)** 구조를 통해 배터리 수명을 극대화하여 대규모 IoT 네트워크 구현을 가능하게 함.
> **3. 융합**: 네트워크 계층(IP)의 보편성과 무선 센서 네트워크(WSN)의 효율성을 통합하여, 사물인터넷(IoT)과 엣지 컴퓨팅(Edge Computing)의 기반 인프라를 제공함.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**6LoWPAN (IPv6 over Low-Power Wireless Personal Area Network)**은 IEEE 802.15.4 표준(예: ZigBee, Wi-SUN)과 같은 저전력 무선 네트워크에서 IPv6 패킷을 전송하기 위해 네트워크 계층과 링크 계층 사이에 위치하는 **적응 계층(Adaptation Layer)**입니다.
**RPL (IPv6 Routing Protocol for Low-Power and Lossy Networks)**은 패킷 손실이 잦고 노드의 전력, 메모리, 처리 능력이 제약적인 **LLN (Low-power and Lossy Networks)** 환경에 최적화된 라우팅 프로토콜입니다.

이 두 기술은 "작은 것들이 인터넷의 주인이 되는(IoT)" 시대에, 자원이 제한된 작은 센서가 거대한 인터넷 프로토콜(IP) 세상과 소통하기 위해 반드시 필요한 다리 역할을 합니다.

#### 2. 등장 배경 및 철학
**① 기존 한계 (Legacy Limits)**
전통적인 인터넷은 강력한 처리 능력과 안정적인 전력 공급을 가진 장비를 전제로 설계되었습니다. 그러나 IoT 센서는 배터리로 수년간 동작해야 하며, 무선 주파수 대역폭도 좁고 패킷 손실이 잦습니다. IPv6 패킷의 기본 헤더 크기인 40바이트는 127바이트밖에 안 되는 IEEE 802.15.4 프레임에 비해 너무 큰 공간을 차지하여, 효율이 매우 낮았습니다.

**② 혁신적 패러다임 (Paradigm Shift)**
인터넷의 표준인 IP 프로토콜을 포기하지 않고, 하드웨어의 제약을 극복하기 위해 **'압축(Compression)'**과 **'단순화(Simplification)'** 전략이 도입되었습니다. 6LoWPAN은 불필요한 헤더 정보를 제거하여 전송 효율을 높였고, RPL은 복잡한 링크 상태 라우팅 대신 수직적 트리 구조를 통해 오버헤드를 최소화했습니다.

**③ 현재의 비즈니스 요구 (Business Needs)**
스마트 시티, 공장 자동화, 스마트 그리드 등 수천 개의 센서가 상호 연결되는 환경에서는 **IP 주소 할당의 편리성(확장성)**과 **에너지 효율**이 동시에 요구됩니다. 6LoWPAN과 RPL은 이 두 마리 토끼를 잡기 위한 산업 표준으로 자리 잡았습니다.

#### 3. 아키텍처 개관
다음은 표준 TCP/IP 스택과 6LoWPAN/RPL이 적용된 IoT 스택의 비교 다이어그램입니다.

```ascii
+-----------------------------------------------------------------------+
| [일반 인터넷 스택]                 [IoT/IP 스택 (6LoWPAN + RPL)]       |
|                                                                       |
| +---------------------------+       +---------------------------+     |
| | Application Layer (HTTP)  |       | Application (CoAP/MQTT)   |     |
| +---------------------------+       +---------------------------+     |
| | Transport Layer (TCP/UDP) |       | Transport (UDP - primarily)|     |
| +---------------------------+       +---------------------------+     |
| | Network Layer (IPv6)      | <---> | Network Layer (IPv6)      |     |
| +---------------------------+       +---------------------------+     |
| | (No Adaptation)           |       | [6LoWPAN Adaptation Layer]|     |
| |                           |       | - Header Compression      |     |
| |                           |       | - Fragmentation           |     |
| +---------------------------+       +---------------------------+     |
| | MAC / PHY (Ethernet/WiFi)|       | MAC / PHY (IEEE 802.15.4) |     |
| +---------------------------+       +---------------------------+     |
|                                       ^                               |
|                                       | RPL (Routing Logic)           |
|                                       | (Creates Network Topology)    |
+-----------------------------------------------------------------------+
```
**해설**:
왼쪽의 일반 인터넷 스택은 이더넷이나 Wi-Fi처럼 큰 MTU(Maximum Transmission Unit)를 가진 매체를 사용하므로 별도의 적응 계층 없이 IPv6를 바로 사용할 수 있습니다. 반면, 오른쪽 IoT 스택은 **MAC 계층(IEEE 802.15.4)** 위에 **6LoWPAN**이라는 얇은 판을 하나 더 깔아 IPv6 패킷을 아주 작은 프레임에 맞게 **자르고(Fragmentation)**, 꾹꾹 눌러(Compression) 넣습니다. 또한, 데이터가 흘러갈 길(Routing)은 **RPL** 프로토콜이 IPv6 계층 내부 혹은 상위에서 제어하여 에너지 효율적인 경로를 만들어줍니다.

> **📢 섹션 요약 비유**: 마치 거대한 컨테이너 선(IPv6)을 작은 시냇물(무선 센서망)에 띄우기 위해, 화물을 재포장하는 물류 센터(6LoWPAN)를 짓고, 물 흐르는 대로 가지 않고 배터리를 아껴주는 특별한 항로(RPL)를 그려놓은 것과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (Core Components)

| 요소명 | 역할 | 내부 동작 메커니즘 | 주요 프로토콜/명세어 | 비유 |
|:---|:---|:---|:---|:---|
| **LoWPAN Interface** | 네트워크 진입점 | IEEE 802.15.4 PHY/MAC 계층을 제어하여 RF 전송 수행 | IEEE 802.15.4 | 전화기 송수화기 |
| **6LoWPAN Adaptation** | 데이터 포맷 변환 | IPv6 패킷을 분석하여 `LOWPAN_IPHC` 포맷으로 압축하고, 127바이트 이하로 **Fragmentation** 수행 | RFC 6282 (HC), RFC 4944 | 짐 압축기 |
| **RPL Instance** | 라우팅 도메인 | 하나의 관리 도메인 내의 노드 집합. Objective Function에 따라 최적 경로 탐색 | RFC 6550 | 지역 도로망 |
| **DODAG Root** | 토폴로지 루트 | 네트워크의 게이트웨이(Border Router). 상위 인터넷과 연결되며 경로 계산의 기준점 | - | 고속도로 진입로 |
| **Objective Function (OF)** | 경로 비용 산출 | '에너지', '지연(Latency)', '신뢰성' 등의 메트릭을 가중치 계산하여 상위 노드(Parent) 선정 | OF0, MRHOF | 내비게이션 설정 (최단/무료도로) |

#### 2. 6LoWPAN 심층 동작 원리

**A. 헤더 압축 (Header Compression)**
IPv6 헤더는 기본적으로 40바이트입니다. IPv6 주소가 128비트(16바이트)인데, 출발지와 목적지 주소만 해도 32바이트를 차지합니다. 127바이트짜리 802.15.4 프레임에서 이는 치명적입니다. 6LoWPAN은 **IPHC (IP Header Compression)** 방식을 사용합니다.
*   **Context 기반 압축**: 네트워크 내에서 공통으로 사용되는 프리픽스(Prefix, 맨 앞 64비트)를 'Context'로 등록해두고, 실제 전송 시에는 Context ID만 보냅니다.
*   **ELID (EUI-64) 생략**: MAC 주소에서 유추할 수 있는 IP 주소의 뒷부분(Interface ID)은 아예 보내지 않고 수신측에서 재조립하게 합니다.

```ascii
[IPv6 헤더 압축 과정 (RFC 6282)]

   [원본 IPv6 패킷]                    [6LoWPAN 압축 후]
+---------------------------+       +---------------------------+
| Version(4) | Traffic Class|       | Dispatch (1 Byte)         |
| Flow Label (20)           |  ==>  | (IPHC Encoding + CID)     |
| Payload Length (16)       |       | [EID] / [Src Context]     |
| Next Header (8)           |       | [Dst Context]             |
| Hop Limit (8)             |       | Next Header (Inline)      |
| Src Addr (128)            |       | Hop Limit                 |
| Dst Addr (128)            |       | ...                       |
| (Total: 40 Bytes + Data)  |       | (Total: ~2~10 Bytes)      |
+---------------------------+       +---------------------------+
```
**해설**:
원본 40바이트의 IPv6 헤더가 `Dispatch`와 `IPHC` 필드, 그리고 압축된 주소 플래그 등으로 대체되어 고작 몇 바이트 수준으로 줄어듭니다. 이를 통해 실제 데이터(페이로드)가 날아갼다는 비윳(Bandwidth Efficiency)을 비약적으로 높입니다. 만약 압축하지 않는다면, 센서가 보낸 온도 값(예: 4바이트)보다 헤더(40바이트)가 10배나 더 커지는 비효율이 발생합니다.

**B. 단편화 (Fragmentation)**
IPv6의 최소 MTU는 1,280바이트이지만, IEEE 802.15.4 프레임의 페이로드은 72~102바이트 수준입니다. 따라서 IPv6 패킷은 반드시 여러 조각으로 나뉘어야 합니다.
*   **FRAG1 (First Fragment)**: 헤더의 앞부분과 데이터 일부 포함. 전체 크기와 태그를 가짐.
*   **FRAGN (Subsequent Fragments)**: 나머지 데이터 조각들. 수신측은 이 태그를 이용해 재조립(Reassembly) 수행.

#### 3. RPL 라우팅 메커니즘 (RPL Routing Mechanism)

**A. DODAG (Destination Oriented Directed Acyclic Graph) 구조**
RPL은 네트워크 전체를 하나의 루트(Root)를 향하는 거꾸로 선 나무 모양 그래프인 **DODAG**로 관리합니다.

```ascii
         [Internet]
             |
      +------[DODAG Root] (Border Router / Sink)
      |          |  Rank 1
      |          |
      |     +----+----+-----------+
      |     |    |    |           |
   [Node A] [Node B] [Node C]    [Node D] Rank 2
      |      |  |    |   |       |
      |      | (Childs)  |       |
   [Node E] [Node F]  [Node G]  [Node H] Rank 3
      |      |         |        |
    (Leaf) (Leaf)    (Leaf)   (Sensors)

   Legend:
   Arrow(->) : Data Flow (Upward towards Root)
   Rank      : Logical Distance from Root
```
**해설**:
모든 노드는 **Rank(계급)**라는 숫자를 가집니다. 루트가 Rank 1이라면, 그 바로 아래 자식 노드들은 Rank 2가 됩니다. 데이터는 항상 Rank가 높은 곳에서 낮은 곳(루트 방향)으로 흐르는 구조(Upward)를 기본으로 하며, 역방향(Downward) 통신을 위해서는 별도의 저장소 모드(Storing/Non-Storing Mode)가 사용됩니다. 노드는 주기적으로 **DIO (DODAG Information Object)** 메시지를 보내 자신의 Rank를 알리고, 이를 받은 이웃 노드들은 자신의 부모를 선택합니다.

**B. 경로 선정 알고리즘 (Objective Function)**
노드는 부모를 선택할 때 단순히 거리가 가까운 노드를 고르는 것이 아니라, **OF(Objective Function)**에 정의된 대로 **에너지 잔량**, **링크 품질(Link Quality Indicator, LQI)**, **예상 전송 횟수(ETX)** 등을 고려하여 가장 합리적인 부모를 선택합니다.

```python
# RPL 부모 선정 의사코드 (Pseudo-code)
def select_parent(candidate_parents):
    best_parent = None
    min_cost = float('inf')

    for parent in candidate_parents:
        # ETX (Expected Transmission Count): 패킷이 성공하려면 예상되는 전송 횟수
        # 1.0이면 완벽, 높을수록 링크 품질 나쁨
        link_cost = parent.link_metric_etx
        
        # Rank = 부모의 Rank + 링크 비용 (스텝 오브 랭크)
        current_rank = parent.rank + link_cost
        
        # 배터리 고려: 배터리가 부족한 부모는 회피 (Penalty 부여)
        if parent.battery_level < CRITICAL_THRESHOLD:
            link_cost += BATTERY_PENALTY
            
        if current_rank < min_cost:
            min_rank = current_rank
            best_parent = parent
            
    return best_parent
```
**해설**:
이 코드는 RPL 노드가 새로운 부모를 찾을 때의 로직을 단순화한 것입니다. 단순히 무선 신호가 센 것만 따라가는 것이 아니라, 그 부모 노드가 배터리가 얼마나 남았는지, 신호가 얼마나 안정적인지를 계산하여 가장 **'안정적이고 오래 가는 길'**을 선택합니다. 이것이 기존 라우팅 프로토콜(OSPF 등)과 결정적으로 다른 **LLN(Low-power and Lossy Network)** 맞춤형 로직입니다.

> **📢 섹션 요약 비유**: 6LoWPAN은 아주 긴 이력