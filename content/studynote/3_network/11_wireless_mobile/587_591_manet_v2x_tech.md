+++
title = "587-591. 애드혹(Ad-hoc) 통신과 차량 통신(V2X)"
date = "2026-03-14"
[extra]
category = "Wireless & Mobile"
id = 587
+++

# 587-591. 애드혹(Ad-hoc) 통신과 차량 통신(V2X)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 고정된 인프라(Cellular Base Station) 없이 이동하는 노드 간에 자율적으로 경로를 설정하여 데이터를 중계하는 **MANET (Mobile Ad-hoc Network)** 구조와, 이를 기반으로 자동차와 주변 환경 간의 실시간 정보를 교환하는 **V2X (Vehicle to Everything)** 통신 기술.
> 2. **가치**: 재난 상황 등 인프라 붕괴 시에도 **네트워크 생존성**을 확보하며, 자율주행에서는 100ms 이내의 초저지연성을 통해 도로 교통 흐름을 최적화하고 사고율을 획기적으로 낮춤.
> 3. **융합**: 무선 라우팅 프로토콜(AODV, OLSR)과 5G **URLLC (Ultra-Reliable Low Latency Communications)** 기술이 결합되어, 이동성(Mobility)이 극대화된 환경에서의 신뢰성 있는 통신을 실현함.

+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**애드혹 통신(Ad-hoc Network)**은 라틴어 'ad hoc'에서 유래하여, '이 목적을 위하여(for this)'라는 의미로, 사전에 구축된 네트워크 인프라(유선 망, 기지국 등) 없이 필요한 시점에 노드(Node)들이 자율적으로 네트워크를 구성하여 통신하는 방식을 말합니다. 특히 노드가 이동성을 가지는 경우를 **MANET (Mobile Ad-hoc Network)**이라 칭하며, 각 노드는 종단 장치(Host)이자 동시에 데이터 중계기(Router)의 역할을 수행합니다. 이는 기존 셀룰러 네트워크가 중앙 집중형(Base Station 의존)인 것과 대조되는 **분산형(Distributed)** 구조를 가집니다.

**💡 비유: 고립된 섬의 릴레이 무전**
어떤 섬에 다리(인프라)가 없더라도, 섬 사람들이 서로 소리쳐서 정보를 전하고, 그 정보가 바다 건너 다음 섬으로, 다시 다음 섬으로 전달되어 결국 먼 곳까지 닿게 되는 원리와 같습니다. 중간에 있는 사람이 정보를 끊지 않고 잘 전달해주는 것이 핵심입니다.

**등장 배경**
1.  **기존 인프라의 한계**: 지진, 전쟁 등 재난 상황에서 기지국이 파괴되면 통신이 두절됨 (Resilience 요구).
2.  **설치 비용 및 편의성**: 광케이블을 매설할 수 없는 험지나 잦은 이동이 필요한 굵작전 환경에서 즉설 통신 필요.
3.  **자율주행 시대의 도래**: 자동차 간 통신(V2V)은 도로 기반 시설(V2I)의 커버리지가 닿지 않는 사각지대(음영 지역)에서도 안전을 보장해야 함. 따라서 차량 자체가 기지국 역할을 수행해야 하는 필요성 대두.

**📢 섹션 요약 비유**
MANET은 마치 '소방관들의 인간 사다리'와 같습니다. 사다리(고정된 인프라)가 없을 때, 소방관들(노드)이 서로 어깨를 맞대고 올라가서 물을 건너편으로 전달하듯, 통신 신호도 사람들(기기)을 건너뛰며 목적지까지 이동합니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 라우팅 프로토콜**

MANET과 V2X를 지배하는 핵심은 **"어떻게 목적지까지 가는 길을 찾을 것인가?"**입니다. 고정된 표지판(라우터)이 없기 때문에 스스로 지도를 그리고 경로를 찾아야 합니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Mobile Node** | 종단 및 중계 | 송수신 기능 및 패킷 포워딩 수행, 배터리/채널 감지 | IEEE 802.11 | 길을 잃은 여행자이자 안내원 |
| **Routing Agent** | 경로 결정 | Topology 변화 감지, RREQ/RREP 메시지 처리 | AODV, OLSR | 지도를 그리는 지도 제작자 |
| **MAC Layer** | 매체 접속 제어 | Hidden Node 문제 해결, 채널 경합 해결 | IEEE 802.11 DCF | 말하기 전에 경청하는 예절 |
| **OBUs (On-Board Units)** | 차량 내 장치 | 다른 차량이나 인프라와 통신, 위치 정보 송수신 | WAVE, C-V2X | 차량의 입과 귀 |
| **RSUs (Roadside Units)** | 도로변 장치 | 차량에 정보를 제공하거나 Cloud 게이트웨이 역할 | DSRC, 5G gNB | 도로변의 정보 게시판 |

**2. 라우팅 알고리즘 심층 분석: Reactive vs Proactive**

```ascii
      [Reactive (On-Demand) Routing: AODV]          [Proactive (Table-Driven) Routing: OLSR]
      
      1. 경로 필요 시 발견                           1. 주기적으로 전체 맵 유지
      (Source)                                      (Source)
          │                                             │
      (A) ───RREQ───> (B)                        (A) ───Hello───> (B)
          │             │                             │             │
      (C) <───RREQ──── (D)                        (C) <───Topology───(D)
          │             │                             │             │
      [Dest] <──RREP (Path Found)                [Dest] (Always Ready)
```

**AODV (Ad-hoc On-demand Distance Vector) 동작 원리**:
1.  **경로 탐색 (Route Discovery)**: 송신 노드가 목적지를 모르면 **RREQ (Route Request)** 패킷을 Flooding(방송)합니다.
2.  **중계 및 기록**: 중간 노드들은 이 RREQ를 받으면 자신의 테이블에 "요청이 온 방향"을 기록하고(Reverse Path), 다시 이웃에게 뿌립니다.
3.  **경로 응답**: 목적지 노드가 RREQ를 받으면, 자신의 정보를 담은 **RREP (Route Reply)**를 출발지로 보냅니다. 이때 중간 노드들은 기록해둔 역방향 경로를 따라 되돌려 보냅니다.
4.  **경로 유지 (Maintenance)**: 데이터 전송 중 링크가 끊기면 **RERR (Route Error)**를 보내 경로를 삭제하고, 필요 시 다시 경로 탐색을 수행합니다.

**3. V2X 통신 스택: WAVE vs C-V2X**

```ascii
+-----------------------------------------------------------------------+
|                        Application Layer (BSM, CAM, DENM)             |
|                 (Basic Safety Message / Cooperative Awareness)        |
+-----------------------------------------------------------------------+
|           Networking / Facilities (IEEE 1609.3 / IP / 6LoWPAN)        |
+-----------------------------------------------------------------------+
| MAC Layer (IEEE 802.11p EDCA)      | MAC Layer (3GPP LTE-V / 5G NR SL) |
+-----------------------------------------------------------------------+
| PHY Layer (IEEE 802.11p, 5.9GHz)   | PHY Layer (LTE/5G Band 46/47)     |
+----------------- WAVE (DSRC) ----------------+-------- C-V2X ---------+
```

*   **WAVE (Wireless Access in Vehicular Environments)**: IEEE 802.11p 기반. WiFi를 자동차용으로 최적화하여 고속 이동 중 신호 간섭을 최소화(10ms 채널 전환). 수 km 단거리 통신에 강점.
*   **C-V2X (Cellular-V2X)**: LTE 및 5G 기술 기반. **PC5 Interface**(차량 간 직통)와 **Uu Interface**(기지국 경유)를 동시에 사용. 대용량 데이터 처리와 광역 커버리지에 유리하며 5G에서는 **V2N (Vehicle to Network)**을 통해 Cloud Computing과 연계.

**📢 섹션 요약 비유**
AODV 프로토콜은 마치 "길을 잃은 관광객이 인파를 향해 소리쳐 여기를 아는 사람 있냐고 묻는(RREQ) 것"과 같고, 아는 사람이 "나 여기 있다, 이리로 오라(RREP)"고 응답하는 과정입니다. WAVE는 무전기를 든 작전반, C-V2X는 스마트폰으로 5G 네트워크에 접속하는 요원과 같습니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 기술 표준 비교: DSRC(WAVE) vs C-V2X**

| 비교 항목 (Metric) | WAVE / DSRC (IEEE 802.11p) | C-V2X (3GPP Rel-14/15/16) |
|:---|:---|:---|
| **통신 방식** | Decentralized (Ad-hoc) | Hybrid (Cellular + Sidelink) |
| **주파수 대역** | 5.9GHz (전용 대역) | 5.9GHz (PSLTE/5G) 또는 Cellular Band |
| **대기 시간 (Latency)** | 매우 짧음 (< 100ms) | 매우 짧음 (< 20ms in 5G) |
| **커버리지** | 단거리 (수백 m ~ 1km) | 장거리 (기지국 커버리지 전체) |
| **신뢰성 (Reliability)** | 충돌 확률이 높은 고밀도 환경 취약 | 스케줄링을 통한 높은 신뢰성 제공 |
| **모빌리티 지원** | 고속 이동 시 페이딩 취약 | 고속 이동 최적화 (Doppler shift 보상 강함) |
| **비즈니스 모델** | 단순 안전 통신 (구축형) | 안전 + 컨텐츠 전송 (구독형, Edge Compute) |

**2. 타 영역 융합 분석**
*   **Network + OS (운영체제)**: 매우 빠르게 변하는 Topology를 OS 커널 레벨에서 감지하여 Socket Binding을 유지하는 기술 필요. Linux Kernel의 **Mobile IPv6 (MIPv6)** 기능이 MANET의 IP 단절을 완화하는 데 사용됨.
*   **Security (보안)**: 인프라가 없는 환경에서는 **"이 노드가 내 차량 정말인가?"**를 증명하기 어렵습니다. 따라서 **PKI (Public Key Infrastructure)** 기반의 전자 서명이 모든 패킷(CAM, BSM)에 필수적으로 포함되어야 하며, **Misbehavior Detection (이상 행위 탐지)** 알고리즘이 중요함.

**📢 섹션 요약 비유**
WAVE는 "폐쇄적인 사설 클럽 무전기"처럼 멤버끼리만 빠르게 대화하지만, 사람이 너무 많으면 소음이 심해집니다. C-V2X는 "스마트폰 메신저"처럼 기지국이라는 거대한 관리자를 통해 더 멀리, 더 정확하게 메시지를 보내면서도, 옆 사람이랑은 블루투스처럼 직접(Sidelink) 연결할 수 있는 하이브리드 스마트 시스템입니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

*   **시나리오 A: 터널 내 재난 상황 통신망 구축**
    *   **문제**: 지진으로 터널 내 모든 기지국이 파괴됨.
    *   **의사결정**: LTE 신호가 닿지 않는 맹지 대응을 위해 터널 내 조명이나 비상 전화기에 **Wi-Fi Mesh AP**를 부착하여 Mesh 토폴로지 구성. 구조대원의 휴대용 단말이 이 AP들을 건너뛰며( hopping) 터널 입구까지 데이터를 전송하도록 설계.
*   **시나리오 B: 자율주행 차량(CAV) 사각지대 해결**
    *   **문제**: 교차로에 건물이 있어 선행 차량 급정거를 후속 차량이 센서로 인지 못함.
    *   **의사결정**: V2V 통신을 통해 **BREM (Brake Event Message)** 브로드캐스트. 이때 주파수 혼선을 막기 위해 C-V2X의 **Mode 4 (Sidelink without Coverage)** 방식을 채택하여 기지국 도움 없이도 차량 간 직접 통신이 가능하도록 표준 채택.

**2. 도입 체크리스트 (기술적/운영적)**

| 항목 | 체크 포인트 (Check Points) |
|:---|:---|
| **Topology Stability** | 노드 이동 속도 대비 경로 갱신(Routing Update) 주수가 충분한가? (AODV Tuning) |
| **Hidden Node** | 채널 경합(NAV 설정)이 제대로 설정되어 충돌이 방지되는가? (RTS/CTS 사용 여부) |
| **Security** | Sybil Attack(가짜 ID 생성)을 방어하기 위한 인증서(CRL) 갱신 주기는 적절한가? |
| **QoS** | 안전 관련 메시지(Control Channel)와 엔터테인먼트(Service Channel)의 우선순위 분리(EDCA)가 되는가? |

**3. 안티패턴 (주의사항)**
*   **Broadcast Storm (방송 폭주)**: 네트워크에 특정 노드가 과도하게 많은 RREQ를 보내면 망 전체가 마비됨. 이를 방지하기 위해 **TTL (Time To Live)** 값을 적절히 설정하거나, 확률적 중계 방식을 적용해야 함.

**📢 섹션 요약 비유**
약자(MANET) 사이의 연결을 관리할 때는 "너무 잦은 연락(RREQ Flooding)"은 배터리를 다 쓰게 만들고, "연락이 너무 없음"은 길을 잃게 만듭니다. 마치 팀 프로젝트에서 너무 자주 회의를 하면 업무가 진행이 안 되고, 너무 안 하면 동문서답이 되는 것과 같은 밸런싱(Balancing) 기술이 실무의 핵심입니다.

+++

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**1. 정량/정성 기대효과**

| 구분 | 도입 전 (