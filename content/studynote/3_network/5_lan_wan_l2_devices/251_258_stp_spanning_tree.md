+++
title = "251-258. L2 루프 문제와 스패닝 트리 프로토콜(STP)"
date = "2026-03-14"
[extra]
category = "LAN/WAN & L2 Devices"
id = 251
+++

# 251-258. L2 루프 문제와 스패닝 트리 프로토콜(STP)

> **핵심 인사이트 (3줄 요약)**
> 1. **본질**: 이중화된 L2 스위치 망에서 필연적으로 발생하는 `루프(Loop)`로 인한 `브로드캐스트 스톰(Broadcast Storm)`과 `MAC 주소 플래핑(Flapping)`을 방지하기 위해, 물리적 토폴로지를 논리적인 트리 구조로 변환하여 경로를 단일화하는 `스패닝 트리 프로토콜(STP, Spanning Tree Protocol)`의 메커니즘.
> 2. **가치**: 네트워크 안정성을 담보하며 링크 장애 시 자동으로 우회 경로(`Convergence`)를 제공하여 고가용성(HA)을 확보함. 단, 초기 `RSTP (Rapid Spanning Tree Protocol)` 적용 전까지는 장애 복구 속도가 느린(30~50초) 트레이드오프가 존재함.
> 3. **융합**: OSI 7계층 중 데이터 링크 계층(2 Layer)의 제어 프로토콜로, 네트워크 계층(3 Layer)의 라우팅 프로토콜(`OSPF`, `IS-IS`)과 유사한 목적(루프 프리, 최적 경로)을 가지나, 브로드캐스트 도메인 내에서 작동한다는 점에서 구조적 차이를 보임.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
L2 스위치(Switch) 환경에서 이중화(Redundancy)를 목적으로 물리적으로 회선을 병렬로 연결하면, `이더넷 프레임(Ethernet Frame)`이 `TTL (Time To Live)`과 같은 생존 시간(Lifetime) 개념이 없어 네트워크 내를 무한 순환하는 `루프(Loop)`가 발생합니다. 이를 해결하기 위해 IEEE 802.1D 표준으로 정의된 `STP (Spanning Tree Protocol)`는 논리적인 포트 차단(Blocking)을 통해 네트워크를 트리(Tree) 형태로 변환합니다.

**💡 비유**
콜센터에 전화기가 3대 있는데, A가 B에게 말을 전하고, B는 다시 C에게, C는 다시 A에게 전달하는 상황과 같습니다. 전화기(스위치)가 끊어지지 않은 한, 이 대화는 끝없이 반복되어 다른 중요한 전화(정상 트래픽)를 못 받게 만듭니다.

**등장 배경**
1.  **기존 한계**: 초기 이더넷 허브(Hub) 환경에서는 `CSMA/CD (Carrier Sense Multiple Access with Collision Detection)`로 충분했으나, 스위치 도입 후 포트 간 전이중(Full-Duplex) 통신이 가능해지면서, 물리적 루프 구간에서의 프레임 증식이 치명적인 장애(Broadcast Storm)로 이어짐.
2.  **혁신적 패러다임**: 하드웨어적으로 회선을 자르지 않고, 소프트웨어적으로 특정 포트를 차단하여 논리적 경로를 하나만 만들어내는 `그래프 이론(Graph Theory)`의 신장 트리(Spanning Tree) 알고리즘을 네트워크에 적용.
3.  **현재의 비즈니스 요구**: IDC(Data Center)나 클라우드 환경에서의 서비스 중단 없는 고가용성(High Availability) 요구가 증대됨에 따라, 장애 복구 시간을 단축한 `RSTP (Rapid Spanning Tree Protocol)` 및 `MSTP (Multiple Spanning Tree Protocol)`가 표준으로 자리 잡음.

**📢 섹션 요약 비유**
물리적인 도로망(회선)이 정밀하게 연결되어 있어도, 교통 체증을 막기 위해 신호등(STP)이 특정 구간을 통제하여 차량이 한 방향으로만 흐르게 하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

STP는 `BPDU (Bridge Protocol Data Unit)`라는 제어 프레임을 교환하여 다음 5가지 핵심 요소를 결정합니다.

| 요소명 (Component) | 역할 (Role) | 내부 동작 및 판단 기준 | 프로토콜/값 | 비유 |
|:---|:---|:---|:---|:---|
| **Root Bridge** | 네트워크의 중심축 (루트) | `Bridge ID` (Priority + MAC)가 가장 낮은 스위치가 선출됨. 모든 경로의 기준점이 됨. Priority Default: 32768 (0x8000) | Priority (0-61440) | 회사 내 가장 높은 직급자(CEO) |
| **Root Port (RP)** | 루트 브리지로 가는 입구 | 루트 브리지로부터 가장 가까운 포트. `Path Cost`가 가장 낮고, 동률 시 Sender Bridge ID/Port ID가 낮은 쪽 선정 | Cumulative Cost | 본인 사무실에서 CEO로 가는 가장 빠른 엘리베이터 |
| **Designated Port (DP)** | 세그먼트의 대표 출구 | 각 LAN 세그먼트(선)마다 루트 브리지 방향으로 트래픽을 보낼 자격이 있는 포트. Root Bridge의 모든 포트는 자동으로 DP가 됨. | Root Path Cost | 각 부서장이 본인 부서 사람을 대표해 말하는 권한 |
| **Non-Designated Port (NDP)** | 차단된 예비 경로 | RP도 DP도 아닌 포트. 데이터 트래픽을 차단(Blocking)하여 루프를 방지하나, 장애 시 예비 경로로 활용됨. | Blocking State | 긴급을 위해 폐쇄된 비상구 |
| **Port State** | 포트의 동작 상태 | Blocking → Listening → Learning → Forwarding 단계를 거치며 활성화됨 (RSTP는 Discarding 등 단순화됨) | Timer 기반 전이 | 교통정리 단계 (멈춤→신호확인→출발) |

**ASCII 구조 다이어그램 + 해설**

아래는 STP에 의해 루프가 제거된 네트워크의 논리적 구조를 도식화한 것입니다.

```ascii
                      [Switch A] (Root Bridge)
      (Priority: 8192) │───────────────────────│
                      │        (DP)            │ (DP)
          (RP)        │ (Path Cost: 19)        │ (Path Cost: 19)
   ┌───────────────────┼───────────────────────┼───────────────────┐
   │                   │                       │                   │
   ▼                   ▼                       ▼                   ▼
[Port 1]            [Port 2]               [Port 3]            [Port 4]
   │                   │                       │                   │
   │ (100Mbps, Cost 19)│ (1Gbps, Cost 4)       │ (100Mbps)          │
   │                   │                       │                   │
[Switch B] ─────────────┼─────────────────── [Switch C]
   │                   │                       │
   │ (Shared Link)     │                       │
   │ (Cost: 19)        │                       │
   └─────────────────────┘                       │
          │                                     │
   [SW B Port 3]                        [SW C Port 3]
          │                                     │
          └──────────────── (Direct Link) ──────┘
                  (Path Cost Calculation)
```

**(도해 해설)**
1.  **Root Bridge 선출**: `Switch A`가 Priority가 가장 낮으므로 루트 브리지가 됩니다.
2.  **Root Port (RP) 선정**: `Switch B`와 `Switch C`는 `Switch A`로 가는 비용(Cost)을 계산합니다.
    *   Switch B → A: 직접 연결된 100Mbps 링크(Cost 19)가 최단 경로이므로 `Port 1`이 RP가 됩니다.
    *   Switch C → A: 직접 연결된 100Mbps 링크(Cost 19)가 RP 후보이나, B를 거치는 1Gbps(Cost 4)가 더 빠를 수 있으므로 BPDU를 통해 최적 경로를 계산합니다.
3.  **Designated Port (DP) 및 차단**:
    *   Switch A의 모든 포트는 DP입니다.
    *   Switch B와 Switch C 사이의 링크에서는, 루트로부터의 총 경로 비용이 더 높은 쪽의 포트가 차단(Blocking)됩니다. 이를 통해 물리적 삼각형 구조가 논리적 나무 구조로 변형됩니다.

**심층 동작 원리 및 BPDU 구조**

STP의 모든 통신은 `BPDU (Bridge Protocol Data Unit)`라는 특수한 프레임으로 이루어집니다.

*   **구조**:
    *   `Protocol ID`: 0 (STP)
    *   `Version`: 0 (STP), 2 (RSTP), 3 (MSTP)
    *   `Flags`: Topology Change Notification 등
    *   `Root ID`: 루트 브리지의 식별자
    *   `Root Path Cost`: 자신에서 루트까지의 비용 합계
    *   `Bridge ID`: 자신의 식별자
    *   `Port ID`: 포트 식별자
    *   `Message Age`: BPDU가 루트를 떠난 시간
    *   `Max Age`: BPDU의 유효 기간 (Default 20초)
    *   `Hello Time`: BPDU 전송 주기 (Default 2초)
    *   `Forward Delay`: Listening/Learning 상태 유지 시간 (Default 15초)

**핵심 알고리즘: 상태 전이 (State Transition)**
STP 포트는 안정성을 위해 다음과 같은 유한 상태 머신(Finite State Machine)을 따릅니다.

```python
# Pseudo-code for STP State Machine
def stp_port_fsm(port):
    # 초기 상태
    port.state = "Blocking" 
    
    # 이벤트 루프
    while True:
        if port.state == "Blocking":
            if receive_superior_bpdu():
                port.state = "Listening" # 경로 재설정 시작
                start_timer(forward_delay=15s)
                
        elif port.state == "Listening":
            # 토폴로지 변경 확인 중 (루프 확인)
            if timer_expired():
                port.state = "Learning"
                
        elif port.state == "Learning":
            # MAC 주소 학습 시작
            learn_mac_addresses()
            if timer_expired():
                port.state = "Forwarding"
                
        elif port.state == "Forwarding":
            if link_down():
                port.state = "Blocking"
            # Data Transmission Enabled
```

**📢 섹션 요약 비유**
스위치들이 모여 회의(BPDU 교환)를 열어 사장님(Root Bridge)을 뽑고, 각자 사장님에게 가장 빨리 연락할 수 있는 직통 전화기(RP)와 부서 직원들을 대표해 말할 수 있는 대변인(DP)을 지정합니다. 이 과정에서 지시가 내려오지 않은 직원들은 대기 명령(Blocking)을 받아 혼란을 막는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**심층 기술 비교: STP vs RSTP vs LACP**

| 비교 항목 | STP (IEEE 802.1D) | RSTP (IEEE 802.1w) | LACP (IEEE 802.3ad) |
|:---|:---|:---|:---|
| **목적** | L2 루프 제거 | L2 루프 제거 및 고속 컨버전스 | 대역폭 병목 및 이중화 |
| **작동 계층** | L2 Control Plane | L2 Control Plane | L2 Link Aggregation |
| **컨버전스 속도** | 30~50초 (느림) | < 10초 (빠름, Proposal/Agreement 사용) | 즉시 (Active-Active) |
| **포트 상태** | Blocking → Listening → Learning → Forwarding | Discarding → Learning → Forwarding | Active / Standby |
| **링크 활용도** | 단일 경로만 활용 (낭비 심함) | 단일 경로만 활용 (지만 빠른 전환) | 모든 링크 균등 분산 (효율 높음) |

**과목 융합 관점: L2 STP와 L3 라우팅의 시너지**
1.  **네트워크(L3)**: 라우터는 `Routing Table`을 기반으로 `Routing Information Protocol (RIP)`나 `Open Shortest Path First (OSPF)` 등을 사용해 목적지를 찾습니다. L3 계층은 패킷 단위로 전송하며 `TTL`이 있어 루프가 발생해도 자연스럽게 소멸됩니다.
2.  **데이터 통신(L2)**: 스위치는 `MAC Address Table`을 사용합니다. 하지만 STP가 없으면 `Broadcast Storm` 발생 시 L3 라우터조차 프레임 처리에 과부하(High CPU Utilization)를 겪어 네트워크 마비로 이어집니다. 따라서 안정적인 L3 라우팅을 위해서는 L2 STP가 필수적인 기반 기술입니다.
3.  **보안(Security)**: STP의 메커니즘을 악용한 `STP Attack` (루트 브리지 위장 공격)이 가능합니다. 이를 막기 위해 `BPDU Guard`나 `Root Guard` 같은 보안 기능과의 융합이 필수적입니다.

**📢 섹션 요약 비유**
STP는 도로 단방향화(일방통행)를 통해 충돌을 막는 교통 정책이라면, L3 라우팅은 내비게이션(최적 경로 탐색)입니다. 아무리 내비게이션이 좋아도 도로가 순환 구조로 되어 있으면 교통 체증(루프)이 발생하므로, 내비게이션(L3)이 제대로 작동하려면 기초 도로 설계(L2 STP)가 루프 프리(Free)여야 하는 상호 의존 관계입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정**

1.  **장애 상황: 우회 경로(Convergence) 지연**
    *   **문제**: 기존 STP 환경에서 메인 스위치(Root Bridge)의 전원이 나갔으나, 백업 경로가 올라오는 데 45초가 걸려 DB 세션이 터짐.
    *   **의사결정**: RSTP로 튜닝 및 `PortFast`, `UplinkFast` 기능 활성화.
    *   **해결**: 논리적 스패닝 트리 구조를 유지하되, 장애 발생 시 차단되었던 포트를 즉시 Forwarding 상태로 전환하여 복구 시간을 1초 이내로 단축