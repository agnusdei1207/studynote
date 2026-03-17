+++
title = "872-879. 가상화 심화: P4와 텔레메트리 (P4, NETCONF/YANG)"
date = "2026-03-14"
[extra]
category = "SDN & NFV"
id = 872
+++

# 872-879. 가상화 심화: P4와 텔레메트리 (P4, NETCONF/YANG)

> ## 핵심 인사이트 (3줄 요약)
> 1. **본질 (P4)**: P4 (Programming Protocol-independent Packet Processors)는 네트워크 장비의 **데이터 평면(Data Plane)** 을 소프트웨어적으로 정의할 수 있게 하여, 하드웨어 교체 없이 패킷 처리 로직(헤더 파싱, 포워딩)을 자유자재로 변경하는 혁신적인 언어입니다.
> 2. **가치 (Telemetry & Automation)**: 고전적인 SNMP (Simple Network Management Protocol)의 한계를 넘어, **스트리밍 텔레메트리(Streaming Telemetry)** 와 **NETCONF (Network Configuration Protocol)**는 마이크로초(µs) 단위의 실시간 데이터 수집과 선언적 자동화를 통해 네트워크의 가시성과 운영 효율을 획기적으로 높입니다.
> 3. **융합 (SDN Evolution)**: 이러한 기술들은 NOS (Network Operating System) 예를 들어 **SONiC (Software for Open Networking in the Cloud)** 와 결합하여, 네트워크를 단순한 전송 파이프가 아닌 클라우드-native 애플리케이션이 실행 가능한 '프로그래머블 인프라'로 진화시킵니다.

+++

### Ⅰ. 개요 (Context & Background) - [500자+]

**개념 정의 및 철학**
전통적인 네트워크 아키텍처는 벤더(Vendor)가 제공하는 폐쇄적인 하드웨어(ASIC)와 소프트웨어(Firmware)에 의존하여, 패킷을 처리하는 방식이 사실상 고정되어 있었습니다. **SDN (Software Defined Networking)** 초기에는 제어 평면(Control Plane)의 분리에 집중하였으나, 데이터 평면의 유연성은 여전히 제한적이었습니다. 이러한 배경에서 등장한 **P4 (Programming Protocol-independent Packet Processors)**는 네트워크 엔지니어에게 하드웨어 스위치의 내부 로직을 직접 코딩할 수 있는 권한을 부여합니다. 마치 개발자가 GPU를 제어하여 쉐이더를 짜는 것과 유사하게, 네트워크 설계자는 스위치 칩셋의 리소스를 할당하고 새로운 프로토콜을 정의할 수 있게 되었습니다.

**등장 배경: ① 한계 → ② 패러다임 → ③ 요구**
1.  **기존 한계**: 기존 스위치는 제조사가 정의한 고정된 기능만 수행 가능했으며, 새로운 프로토콜(예: Geneve, VXLAN 확장) 지원을 위해서는 칩셋 교체나 5~10년 주기의 펌웨어 업그레이드가 필요했습니다.
2.  **혁신적 패러다임**: **P4**와 같은 데이터 평면 언어와 **OpenFlow**의 진화는 "패킷 처리 로직"을 하드웨어로부터 분리하여 소프트웨어화하는 'Protocol Independence'를 실현했습니다.
3.  **비즈니스 요구**: 클라우드 데이터센터와 초연결 시대에는 트래픽 패턴이 실시간으로 변하므로, 장비를 재부팅하지 않고 라우팅 로직을 즉시 수정(P4 프로그램 재컴파일)하고, 상태를 실시간으로 모니터링(**Telemetry**)할 수 있는 역량이 필수적이 되었습니다.

**💡 섹션 요약 비유**
> 마치 과거에는 'CDP 플레이어'에 들어있는 노래만 들을 수 있어서 새로운 음악을 듣고 싶으면 플레이어를 통째로 바꿔야 했다면, P4와 같은 기술은 '스마트폰(App Store)'의 등장과 같습니다. 이제는 하드웨어(스마트폰 몸체)는 그대로 두고, 원하는 앱(코드)만 설치하면 그 기능이 바로 추가되는 것입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

이 섹션에서는 네트워크 프로그래머빌리티의 핵심인 **P4**의 내부 구조와, 구성 자동화를 위한 **NETCONF/YANG**의 결합을 심층 분석합니다.

#### 1. 구성 요소 및 동작 메커니즘 (P4)

**P4 아키텍처 핵심 구성 요소표**

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 비유 (Analogy) |
|:---|:---|:---|:---|
| **Parser** | 패킷 헤더를 식별하여 비트 단위로 나눔 | State Machine 기반으로 헤더 포맷을 분석하고 유효성을 검증함 | 우편물 분류기 (주소지를 읽어 지역별로 분류) |
| **Match-Action Unit** | P4의 핵심 로직 엔진 | 테이블(Key)을 검색하여 일치하는 액션(Value)을 실행. `Exact`, `LPM` 등 지원 | 검색 엔진 (주소를 검색하면 해당 장소의 지도가 나옴) |
| **Control Plane API** | 제어 프로그램(Control Agent)과의 인터페이스 | `tables.add()`, `tables.modify()` 등의 호출을 통해 라우팅 테이블 조작 | 교통정제 센터 (신호등 제어판) |
| **Deparser** | 처리된 패킷을 다시 비트스트림으로 재조립 | 수정된 헤더와 페이로드를 합쳐 송신 포트로 전달 | 포장재 박스(택배) 다시 붙이기 |
| **extern 객체** | 하드웨어 가속기 및 카운터 | 체크섬 계산, 해시 생성, 타이머 등 칩셋 종속적 기능 수행 | 계산기 도구 (유틸리티) |

#### 2. ASCII 구조 다이어그램: P4 Pipeline & Compilation Flow

아래 다이어그램은 개발자가 작성한 **`.p4` 소스 코드**가 실제 스위치 **ASIC**에서 동작하는 방식을 도식화한 것입니다.

```ascii
[ P4 Development & Execution Lifecycle ]

  ① 개발자 (Developer)
      |
      | (P4 Code : .p4 source)
      v
  ② P4 Compiler (p4c) ────────────────────> (Target Info)
      |                                        (ASIC Spec)
      |
      | (Compile: JSON-like control program)
      v
  ③ Control Agent (Control Plane Software)
      |  * 라우팅 프로토콜(BGP/OSPF)과 연동하여 룰 전파
      |
      | (gRPC/Thrift RPC)
      v
  ④ P4 Switch (Target Hardware / Tofino/Barefoot)
      +--------------------------------------------------+
      |  [ INGRESS PIPELINE ]                            |
      |  +----------+    +------------+    +----------+  |
      |  | Parser   | -> | Match-Action | -> | Deparser|  |
      |  | (Ethernet|    | Table [L3]  |    |          |  |
      |  |  /IP)    |    | Action:[Fwd]|    |          |  |
      |  +----------+    +------------+    +----------+  |
      |          |                              |       |
      |          | (Traffic Mgmt/Queuing)       |       |
      |          v                              v       |
      |  [ EGRESS PIPELINE ]          (Transmit Port)   |
      +--------------------------------------------------+

      >>> 스위치 입장에서의 패킷 처리 흐름 >>>
      Packet In -> Parser -> Match-Action -> Deparser -> Packet Out
```

**다이어그램 해설**
1.  **Parser (파서)**: 들어온 패킷의 헤더를 비트 단위로 쪼개어 P4 코드에 정의된 `header` 구조체에 매핑합니다. 이 과정은 유한 상태 머신(FSM)으로 동작합니다.
2.  **Match-Action (매치-액션)**: 파서가 추출한 메타데이터를 바탕으로 테이블(LPM, Ternary 등)을 조회합니다. 예를 들어 목적지 IP가 `10.0.0.1`이면 포트 1로 포워딩(Action)하는 식입니다. P4는 이 테이블의 구조를 개발자가 정의할 수 있습니다.
3.  **Deparser (디파서)**: 처리가 끝난 헤더와 페이로드를 다시 직렬화(Serialize)하여 물리적 포트로 내보냅니다.
4.  **Control Agent**: 컨트롤 플레인 소프트웨어(예: OpenDaylight, ONOS)는 컴파일된 결과를 바탕으로 스위치 테이블 항목을 동적으로 추가/삭제합니다.

#### 3. 심층 기술: NETCONF & YANG

P4가 '어떻게 패킷을 처리할지' 정의한다면, **NETCONF (Network Configuration Protocol)**는 '어떻게 장비를 설정할지'를 정의하는 프로토콜입니다.

*   **NETCONF**: IETF 표준(RFC 6241) 프로토콜로, RPC(Remote Procedure Call) 기반입니다. **SSH (Secure Shell)**나 **TLS** 위에서 동작하며, 설정 데이터를 **XML (Extensible Markup Language)** 형식으로 주고받습니다. 중요한 특징은 `lock`, `candidate-config`, `commit` 기능을 통해 트랜잭션 기반의 안전한 설정 변경을 보장한다는 점입니다.
*   **YANG (Yet Another Next Generation)**: 모델링 언어로서, 네트워크 장비의 데이터 계층(트리 구조)을 정의합니다. 예를 들어 인터페이스 `eth0`의 IP 주소는 무엇이며, 어떤 타입(String/Integer)을 가지는지 스키마(Schema)를 제공합니다.

**NETCONF/YANG 상호작용 코드 예시 (Conceptual)**

```xml
<!-- 요청: 인터페이스 설정 변경 (NETCONF RPC) -->
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <edit-config>
    <target>
      <candidate/>
    </target>
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>eth0</name>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>192.0.2.1</ip>
              <netmask>255.255.255.0</netmask>
            </address>
          </ipv4>
        </interface>
      </interfaces>
    </config>
  </edit-config>
</rpc>
```
> 위 코드는 NETCONF 프로토콜을 통해 SSH 연결 위로 XML 데이터를 보내 `eth0` 인터페이스에 IP를 할당하는 과정입니다. 이후 `<commit/>` 명령어를 통해 실제 장비(Running Config)에 적용합니다.

**📢 섹션 요약 비유**
> P4는 **'자동차의 엔진 제어 유닛(ECU) 프로그래밍'**과 같습니다. 연료 분사 시점과 흡기 밸브 개폐 로직(패킷 처리 로직)을 코드로 새로 짜서, 연비(성능)를 극대화하는 것입니다. 반면 NETCONF/YANG은 **'자동차 네비게이션 설정 및 진단 컴퓨터'**와 같습니다. 차의 하드웨어를 뜯어고치지 않고도, 목적지를 설정하거나(Routing Table), 엔진 오일 상태(Interface Stats)를 시스템이 알아먹는 표준 코드로 확인하는 역할을 합니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 모니터링 기술의 진화: SNMP vs. Streaming Telemetry

네트워크 관리의 핵심은 '가시성(Visibility)'입니다. 1990년대의 방식과 2020년대의 방식은 근본적 차이가 있습니다.

| 비교 항목 | SNMP (Simple Network Management Protocol) | Streaming Telemetry (gNMI/gRPC) |
|:---|:---|:---|
| **통신 방식** | **Pull 방식** (Manager가 Agent에게 주기적 요청) | **Push 방식** (Device가 Manager로 실시간 전송) |
| **전송 프로토콜** | UDP (Port 161/162) - 비연결형 | **TCP/UDP** 기반 **gRPC** (HTTP/2) - 고성능 |
| **데이터 포맷** | BER/ASN.1 encoding (바이너리, 파싱 어려움) | **Protocol Buffers** (GPB) / JSON (효율적) |
| **그래뉼라리티** | 초단위(Cnt/sec) ~ 분단위 | **나노초(ns) ~ 마이크로초(µs)** 단위 |
| **오버헤드** | Polling 주기가 짧아질수록 네트워크/장비 부하 폭증 | 구독(Subscription) 기반이므로 데이터 변경 시에만 트래픽 발생 |
| **용도** | 기본 장애 관리, 인벤토리 확인 | **초고대역폭 네트워크 성능 분석, AI 예지 보전** |

#### 2. 데이터 평면 프로그래밍: OpenFlow vs. P4

| 특징 | OpenFlow (1.x) | **P4 (Programming Protocol-independent Packet Processors)** |
|:---|:---|:---|
| **제어 범위** | 제어 평면(Control Plane)에 집중 | **데이터 평면(Data Plane)** 프로그래밍 가능 |
| **프로토콜 유연성** | 미리 정의된 헤더 필드(IPv4, IPv6 등)만 지원 | **새로운 헤더와 프로토콜을 개발자가 정의 가능** |
| **표준화/표현력** | 스위치가 "이해할 수 있는" 언어어야 함 | 개발자가 "원하는 대로" 설계할 수 있는 언어 |
| **추상화 레벨** | 낮음 (특정 벤더 칩셋 의존도 높음) | 높음 (Target-independent P4 코드 작성 가능) |

**과목 융합 관점 (OS, 컴퓨터구조)**
*   **Computer Architecture**: P4의 Match-Action Table은 사실 **TCAM (Ternary Content Addressable Memory)**의 소프트웨어적 추상화입니다. 하드웨어적 관점에서 TCAM은 전력 소모가 크고 비싸지만 O(1)의 검색 속도를 가집니다. P4 개발 시 테이블 크기와 리소스 사용량(Memory footprint)을 최적화하는 것은 **컴파일러 최적화** 기술과 직결됩니다.
*   **Operating System**: 텔레메트