+++
title = "850-856. 소프트웨어 정의 네트워킹(SDN)의 이해"
date = "2026-03-14"
[extra]
category = "SDN & NFV"
id = 850
+++

# 850-856. 소프트웨어 정의 네트워킹(SDN)의 이해

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전통적인 네트워크 장비의 **Control Plane (제어 평면)**과 **Data Plane (데이터 평면)**을 물리적으로/논리적으로 완전 분리하여, 네트워크 지능을 중앙의 **SDN Controller (SDN 컨트롤러)**로 집중시키는 아키텍처이니다.
> 2. **가치**: 네트워크 구성 변경 소요 시간을 주/월 단위에서 초/분 단위로 단축(CapEx/OpEx 절감)하고, 벤더 락인(Vendor Lock-in)을 해제하여 하드웨어 다양성을 확보합니다.
> 3. **융합**: 가상화 기술, **NFV (Network Functions Virtualization)**와 결합하여 5G/6G 코어 네트워크 및 클라우드 오케스트레이션의 핵심 기반이 되며, **AI (Artificial Intelligence)** 기반 트래픽 최적화를 가능하게 핵심 인프라입니다.

+++

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
**SDN (Software Defined Networking)**은 네트워크 장비 내부에 밀접하게 결합되어 있던 제어 기능(두뇌)을 분리하여, 소프트웨어를 통해 네트워크 전체를 프로그래밍 가능하도록 만드는 패러다임입니다. 기존의 분산형 라우팅 프로토콜(BGP, OSPF 등)이 개별 장비의 '판단'에 의존했다면, SDN은 전지전능한 '중앙 통제 시스템'에 의존합니다. 이는 단순한 관리 편의성을 넘어, 네트워크를 하나의 거대한 컴퓨터 자원(Computing Resource)으로 추상화하는 **NaaS (Network as a Service)**의 근간이 됩니다.

### 💡 비유: 교통 체증과 중앙 제어
기존 네트워킹은 각 교차로(스위치)에 서 있는 교통경찰(개별 라우팅 알고리즘)이 옆 교차로 상황을 전혀 모른 채 자의적으로 판단하는 것과 같습니다. 반면 SDN은 모든 도로의 상황을 실시간으로 파악하는 **중앙 교통 통제 센터**에서 각 교차로의 신호 주기(Flow Table)를 직접 제어하는 시스템입니다. 이를 통해 특정 구간의 정체를 회피하는 최적 경로를 즉시 설정할 수 있습니다.

### 2. 등장 배경
① **기존 한계**: 인터넷 트래픽의 폭발적 증가(Mobile Video, Cloud)로 기존 장비들의 고정된 라우팅 정책과 수동적인 CLI(Command Line Interface) 기반 운영으로는 대응 불가능.
② **혁신적 패러다임**: 일반화된 x86 하드웨어(COTS)를 스위칭에 활용하고, 소프트웨어 로직으로 네트워크를 정의함으로써 **HW(Silicon)와 SW(Software)의 Decoupling** 실현.
③ **현재 비즈니스 요구**: 클라우드 서비스 제공자가 필요에 따라 네트워크 대역폭과 경로를 온디맨드로 프로비저닝(Provisioning)하는 자동화된 인프라의 필수 요구.

### 3. 핵심 기술 요약

| 구분 | 전통적 네트워킹 (Traditional Networking) | SDN (Software Defined Networking) |
|:---|:---|:---|
| **제어 논리** | 분산 (Distributed) | **중앙 집중식 (Centralized)** |
| **데이터와 제어** | 통합 (Integrated) | **분리 (Decoupled)** |
| **프로그래밍** | 폐쇄형 (Vendor-specific CLI) | **개방형 (Open API)** |
| **패킷 처리** | 라우팅 테이블, ACL | **Flow Table (플로우 단위 제어)** |

📢 **섹션 요약 비유**: 전통적인 네트워크는 각자의 머리를 가진 수만 명의 병사들이 전장에서 개별적으로 판단하여 싸우는 '고대 전투 방식'과 같습니다. SDN은 모든 병사(스위치)의 머리를 떼어내어, 하나의 거대한 두뇌(컨트롤러)가 드론 조종하듯 전 병력을 실시간 통제하는 '미래형 드론 전투 방식'과 같습니다.

+++

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. SDN 계층 구조 및 구성 요소
SDN 아키텍처는 크게 **Infrastructure Layer (인프라 계층)**, **Control Layer (제어 계층)**, **Application Layer (애플리케이션 계층)**의 3계층으로 구성됩니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **SDN Controller** | 네트워크의 운영체제(OS). 전체 토폴로지 인지 및 경로 계산. | **LLDP (Link Layer Discovery Protocol)**를 통한 링크 발견, **OpenFlow** 등으로 스위치 제어. | 전략가 |
| **Southbound API** | 컨트롤러와 스위치 간의 통신 인터페이스. | **OpenFlow**, **Netconf**, **OF-Config**, **OVSDB**. | 내부 규칙手册 |
| **Northbound API** | 앱과 컨트롤러 간의 통신 인터페이스. | **REST API**, **RESTCONF**, **JSON/RPC**. | 명령 통신망 |
| **Forwarding Element** | 단순 패킷 전달 (Data Plane). | flow lookup, action execution (forward/drop). | 행동 대 |
| **Network App** | 비즈니스 로직 구현 (LBD, 방화벽, 로드밸런싱). | Controller API 호출하여 정책 요청. | 작전 명령 |

### 2. SDN 아키텍처 ASCII 다이어그램

아래 다이어그램은 SDN의 3계층 구조와 각 계층 간의 인터페이스, 그리고 데이터 흐름을 도식화한 것입니다.

```ascii
+-----------------------------------------------------------------------+
| [ Application Layer ] (Business Logic)                                |
|                                                                       |
|  +----------------+    +----------------+    +----------------+      |
|  | Routing App    |    | Security App   |    | Monitoring App |      |
|  | (Path Calc)    |    | (Firewall)     |    | (Traffic Eng.) |      |
|  +-------+--------+    +-------+--------+    +-------+--------+      |
|          |                     |                       |            |
|          +----------+----------+-----------+-----------+            |
|                     |          |           |                        |
|             [ Northbound API (REST/RESTCONF) ]                       |
|                     |          |           |                        |
|  +------------------v----------v-----------v--------------------+    |
|  |               Control Layer (SDN Controller)                 |    |
|  |  +--------------------------------------------------------+  |    |
|  |  |  Control Logic (OS Kernel)                             |  |    |
|  |  |  - Topology Discovery (LLDP)                           |  |    |
|  |  |  - Path Computation (Dijkstra / CSPF)                  |  |    |
|  |  +--------------------------------------------------------+  |    |
|  +------------------+----------+-----------+--------------------+    |
|                     |          |           |                        |
|             [ Southbound API (OpenFlow/Netconf) ]                    |
|                     |          |           |                        |
+---------------------+----------+-----------+------------------------+
                      |          |           |
          +-----------v+    +----v-----+   +-v-----------+            |
          | Switch A (Data) |    | Switch B |   | Switch C    |       |
          | +-------------+ |    | +------+ |   | +-------+   |       |
          | | Flow Table  | |    | | Flow | |   | | Flow  |   |       |
          | +-------------+ |    | | Table| |   | | Table |   |       |
          +-----------------+    +----------+   +-------------+       |
                                                                       |
+-----------------------------------------------------------------------+
           [ Infrastructure Layer (Physical/Virtual Switches) ]
```

**다이어그램 해설**:
1.  **Application Layer**: 네트워크 관리자나 사용자가 원하는 네트워크 기능(예: "A에서 B로 가는 최단 경로 만들기", "10.0.0.5 차단하기")을 정의하는 영역입니다. 이 계층은 하드웨어적인 제약 없이 소프트웨어적으로 로직을 구현합니다.
2.  **Control Layer (The Brain)**: **SDN Controller**가 위치하는 핵심 부분입니다. 남부 API를 통해 하위 스위치들의 상태(포트 업/다운, 링크 속도 등)를 수집하여 전체 네트워크 지도(Global View)를 구축합니다. 앱으로부터 요청받은 정책을 수행하기 위해 스위치에게 명령을 내립니다.
3.  **Infrastructure Layer (The Muscle)**: 실제 패킷이 처리되는 **Data Plane**입니다. 스위치는 고유한 지능 없이 컨트롤러가 보내준 **Flow Entry (흐름 엔트리)**에 따라서만 패킷을 전달, 수정, 또는 폐기합니다.
4.  **Interface**: Northbound API는 프로그래머에게 친숙한 언어로 제어권을 제공하며, Southbound API는 장비 제조사 표준 프로토콜을 통해 하드웨어를 제어합니다.

### 3. OpenFlow 프로토콜 심층 분석 (Southbound API)
**OpenFlow**는 ONF(Open Networking Foundation)가 표준화한 대표적인 SDN 제어 프로토콜입니다.

*   **동작 메커니즘 (Phases)**:
    1.  **Connection Setup**: 컨트롤러(포트 6653/TCP)와 스위치가 TLS 보안 채널을 통해 연결.
    2.  **Discovery**: 스위치는 자신의 포트 정보를 컨트롤러에 전송(`OFPT_FEATURES_REPLY`).
    3.  **Flow Table Entry Installation**:
        *   컨트롤러는 스위치의 **Flow Table**에 규칙을 삽입(`OFPT_FLOW_MOD`).
        *   **Match Fields**: 패킷 헤더의 필드(MAC Address, IP, Port, VLAN ID 등)와 비교.
        *   **Priorities**: 여러 규칙이 일치할 때 우선순위.
        *   **Actions**: `Output`(포트로 전송), `Drop`(폐기), `Modify-Field`(VLAN 태그 변경, TTL 감소).
    4.  **Packet-in**: Flow Table에 매칭되는 규칙이 없는(Unknown) 패킷이 도착하면, 스위치는 해당 패킷의 첫 번째 패킷을 컨트롤러로 전송하여 처리를 요청.
    5.  **Packet-out**: 컨트롤러가 스위치에게 특정 포트로 패킷을 내보내라고 명령.

### 4. 핵심 알고리즘: Flow Processing Pseudo Code

```python
# SDN Switch (Data Plane)의 내부 처리 로직 시뮬레이션
def process_packet(packet):
    # 1. Flow Table 조회 (선형 검색 또는 TCAM 하드웨어 가속)
    best_match = None
    
    for flow_entry in flow_table:
        if packet.matches(flow_entry.match_fields):
            if best_match is None or flow_entry.priority > best_match.priority:
                best_match = flow_entry
    
    # 2. 매칭 규칙 처리
    if best_match:
        # Action Set에 정의된대로 패킷 처리 (Forward, Drop, Modify)
        if "Forward" in best_match.actions:
            forward_packet(packet, best_match.actions.port)
        elif "Drop" in best_match.actions:
            drop_packet(packet)
    else:
        # 3. Miss Handling (Buffered Packet-in to Controller)
        # 매칭 규칙이 없으면 컨트롤러에게 스마트 폰법(제어권) 이관
        send_packet_in_to_controller(packet)
        # 또는 기본 정책(Traffic Flooding) 수행
```

📢 **섹션 요약 비유**: SDN의 아키텍처는 **복잡한 고속도로 톨게이트 시스템**과 같습니다. 각 톨게이트 게이트(Switch)는 바코드 플로우(Packet Header)를 읽기만 하고, 이 게이트를 열어줄지 말지를 결정하는 **중앙 통제 센터(Controller)**의 실시간 명령(Flow Entry)만 기다립니다. 새로운 할인 정책(App)이 생기면 센터에서 소프트웨어 업데이트만으로 전국 모든 게이트의 동작 방식을 즉시 변경할 수 있습니다.

+++

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. SDN vs 전통적 네트워킹 (Traditional Networking)

| 비교 항목 | 전통적 네트워킹 (Legacy) | SDN (Software Defined Networking) |
|:---|:---|:---|
| **제어 방식** | **Distributed (분산)**: 각 라우터가 라우팅 프로토콜(OSPF, BGP)을 통해 경로 학습 | **Centralized (중앙 집중)**: 컨트롤러가 경로 계산 후 스위치에 배포 |
| **장비 의존도** | **Vendor-dependent**: Cisco, Juniper 등 장비 전용 OS/ASIC 필요 | **Agnostic**: 범용 x86 HW + Barefoot Tofino 등 White-box Switch 활용 가능 |
| **추상화 수준** | 낮음 (Low-level CLI 명령어 필요) | 높음 (High-level API/Intent 기반) |
| **운영 방식** | 정책 변경 시 장비별 접속 필요 (Configuration Drift 발생) | 일관된 API를 통해 프로그래밍 방식 자동화 가능 |
| **트래픽 흐름** | Best-effort 또는 QoS 우선순위에 의존 | Application-aware Flow Granularity (앱별 정책 제어) |

### 2. 기술 스택 융합 (Convergence)

**① SDN + NFV (Network Functions Virtualization)**
*   **SDN**은 "제어 로직"의 분리와 이동, **NFV**는 "네트워크 기능(장비)"의 가상화(L4~L7 스위치, 방화벽, LB를 VM/Container로 구현)를 의미합니다.
*   **시너지**: SDN 컨트롤러는 가상화된 네트워크 기능(VNF)들의 연결성(Chaining)을 동적으로 제어합니다. 예: 트래픽이 급증하면 방화벽 VM 인스턴스를 추가하고, SDN이 트래픽을 해당 인스턴스로 우회시킴. 이는 **Telco Cloud**의 핵심입니다.

**② SDN + Cloud Computing (Overlay Networks)**
*   클라우드 환경에서 **VXLAN**, **NVGRE** 같은 Overlay 네트워킹은 가상 머신(VM)의 이동