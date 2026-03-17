+++
title = "도메인 03: 네트워크 (Network)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-network"
kids_analogy = "전 세계의 컴퓨터들이 서로 편지를 주고받는 아주 크고 복잡한 '우체국 시스템'이에요. 편지가 길을 잃지 않고, 나쁜 사람에게 뺏기지 않으면서 목적지까지 가장 빨리 도착하는 규칙을 배운답니다!"
+++

# 도메인 03: 네트워크 (Network)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이기종의 분산된 노드 간에 데이터를 신뢰성 있게 전달하기 위해 규약(Protocol)을 계층화(Layering)하고 물리적/논리적 경로를 제어하는 통신 아키텍처의 총체.
> 2. **가치**: 캡슐화(Encapsulation)를 통한 계층 간 독립성을 보장하여, 인터넷이라는 전 지구적 규모의 초연결망(Hyper-Connectivity)을 붕괴 없이 확장하고 진화시킴.
> 3. **융합**: 전통적인 하드웨어 라우터/스위치 중심에서 탈피하여 SDN(소프트웨어 정의망), NFV, 그리고 클라우드 네이티브의 서비스 메시(Service Mesh)와 결합된 프로그래머블 네트워크로 완전한 환골탈태.

---

### Ⅰ. 개요 (Context & Background)
**네트워크(Network)**는 고립된 연산 장치들을 하나의 거대한 유기체적 시스템으로 묶어낸 IT 역사의 가장 위대한 인프라스트럭처다. 핵전쟁에도 살아남을 수 있는 분산 통신망을 구축하기 위해 시작된 ARPANET의 철학은, 특정 노드가 파괴되어도 패킷(Packet)이 스스로 우회 경로를 찾아 목적지에 도달하는 강인한 생존력을 부여했다.
과거 벤더 종속적인(Vendor Lock-in) 통신 규약들은 이기종 간 통신을 가로막는 치명적인 병목이었으나, ISO가 제정한 **OSI 7계층**과 실질적 인터넷 표준인 **TCP/IP 모델**의 등장으로 프로토콜의 대통합이 이루어졌다. 현대 네트워크는 단순한 데이터 파이프를 넘어, 비디오 스트리밍의 초저지연(Latency) 요구사항과 금융 트랜잭션의 무결성(Integrity), 그리고 제로 트러스트(Zero Trust) 보안을 동시에 강제하는 고도의 분산 제어 평면(Control Plane)으로 진화하였다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

네트워크의 핵심은 복잡한 통신 과정을 역할별로 쪼갠 '계층(Layering)'과, 상위 계층의 데이터를 자신의 페이로드로 감싸는 '캡슐화(Encapsulation)'에 있다.

#### 1. 프로토콜 스택 구성 요소
| 계층 (TCP/IP) | 상세 역할 및 PDU | 내부 동작 메커니즘 | 관련 프로토콜/장비 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Application** | 사용자 인터페이스 (Data) | 데이터 포맷팅, 세션 암호화, 애플리케이션 로직 수행 | HTTP, DNS, TLS / L7 스위치 | 편지의 내용 |
| **Transport** | 단대단(End-to-End) 신뢰성 (Segment)| 포트(Port) 번호 식별, 오류 제어(ARQ), 혼잡 제어(AIMD) | TCP, UDP / L4 로드밸런서 | 등기 우편 수령 확인 |
| **Network** | 종단 간 라우팅 (Packet) | IP 논리 주소 지정, 최적 경로 계산(Dijkstra) | IP, ICMP, OSPF, BGP / 라우터 | 우체국 물류 지도 |
| **Data Link** | 노드 간 전송 제어 (Frame) | MAC 물리 주소 식별, 충돌 감지(CSMA/CD), 오류 검출 | Ethernet, ARP / L2 스위치 | 배달부의 배달 트럭 |
| **Physical** | 물리적 신호 변환 (Bit) | 0과 1의 데이터를 전기적/광학적 아날로그 신호로 변조 | UTP, Fiber, Hub, Repeater | 실제 아스팔트 도로 |

#### 2. 데이터 흐름 및 캡슐화 아키텍처 다이어그램 (ASCII)
```text
    [ TCP/IP Encapsulation & Routing Flow (Host A -> Router -> Host B) ]
    
    [ Host A (Sender) ]                                          [ Host B (Receiver) ]
    +--------------------------------+                           +--------------------------------+
    | App:   [HTTP Data]             |                           | App:   [HTTP Data]             |
    | Trans: [TCP][HTTP Data]        |                           | Trans: [TCP][HTTP Data]        |
    | Net:   [IP][TCP][HTTP Data]    |                           | Net:   [IP][TCP][HTTP Data]    |
    | Link:  [MAC-A][IP...][FCS]     |                           | Link:  [MAC-B][IP...][FCS]     |
    +-----------|--------------------+                           +-------------^------------------+
                | (Bits)                                                       | (Bits)
    ============v==============================================================^===========
             (L2 Switch) ----> [ Router (L3) ] ----> (Internet) ----> [ Router (L3) ]
             (MAC 검사)        +-------------+                        +-------------+
                               | decapsulate |                        | decapsulate |
                               | [IP] 검사   |                        | [IP] 검사   |
                               | Routing Tbl |                        | Routing Tbl |
                               | encapsulate |                        | encapsulate |
                               +-------------+                        +-------------+
```

#### 3. TCP 혼잡 제어(Congestion Control) 핵심 알고리즘
TCP는 네트워크의 붕괴(Congestion Collapse)를 막기 위해 송신자의 윈도우 크기(cwnd)를 조절하는 예술적인 피드백 루프를 가진다.
① **Slow Start**: 패킷 전송을 1부터 시작하여 ACK 수신 시마다 윈도우 크기를 $2^n$ 지수적으로 폭발시킴.
② **Congestion Avoidance (AIMD)**: 임계치(ssthresh) 도달 시, 윈도우를 선형적(+1)으로 조심스럽게 증가.
③ **Fast Retransmit**: 수신자가 중복 ACK 3개를 보내면 타임아웃 전이라도 즉시 패킷 재전송.
④ **Fast Recovery**: 패킷 유실 시 윈도우 크기를 1로 떨어뜨리지 않고 절반(1/2)으로 줄여 빠르게 복구 궤도 진입.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 전송 계층 프로토콜 비교: TCP vs UDP
| 비교 지표 | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) | 기술적 파급 (시너지) |
| :--- | :--- | :--- | :--- |
| **연결성** | 3-Way Handshake 기반 연결 지향 | 비연결형 (상태 비저장) | TCP는 세션 관리 오버헤드 존재 |
| **신뢰성** | 패킷 순서 보장, 분실 시 재전송 | 순서 무보장, 분실 시 폐기 | 금융/파일 전송(TCP) vs 실시간(UDP) |
| **속도(Latency)**| 상대적으로 느림 | 극도로 빠름 (제어 헤더 8바이트) | QUIC(HTTP/3)는 UDP 기반으로 TCP 한계 극복 |
| **혼잡 제어** | 송신량 자체 조절 (AIMD) | 통제 없음 (대역폭 무한 점유 가능) | 멀티미디어 스트리밍 시 화면이 깨져도 진행 |

#### 2. 동적 라우팅 프로토콜 비교: IGP (OSPF) vs EGP (BGP)
| 비교 지표 | OSPF (Open Shortest Path First) | BGP (Border Gateway Protocol) |
| :--- | :--- | :--- |
| **적용 범위** | 자율 시스템 내부 (IGP - 기업망) | 자율 시스템 간 (EGP - 글로벌 인터넷) |
| **알고리즘** | 링크 상태 (Link-State), 다익스트라(Dijkstra) 알고리즘 | 경로 벡터 (Path-Vector), 정책 기반 라우팅 |
| **최적 경로 기준**| 대역폭 기반 비용(Cost) 최소화 | AS Hop Count 최소화 및 관리자 정책(Policy) |
| **수렴 속도** | 매우 빠름 (토폴로지 변경 즉시 반영) | 상대적으로 느림 (초거대 라우팅 테이블) |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1: 글로벌 OTT 서비스의 초저지연 CDN 아키텍처 설계**
- **문제 상황**: 아시아 지역 사용자가 미국 본사 서버의 영상을 시청할 때, BGP 라우팅 홉 수 증가와 해저 케이블 물리적 거리로 인한 RTT(Round Trip Time)가 200ms를 초과하여 버퍼링이 발생.
- **기술사적 결단**: 엔드투엔드 거리를 극복하기 위해 물리적 해결책인 **CDN(Content Delivery Network)**과 **엣지 로케이션(Edge Location)**을 전 세계 ISP 거점에 배치한다. 논리적으로는 헤드 오브 라인 블로킹(HOL Blocking) 문제를 야기하는 TCP 대신, **UDP 기반의 QUIC 프로토콜(HTTP/3)**을 전면 도입하여 핸드쉐이크 0-RTT를 달성하고 스트리밍 체감 품질을 압살한다.

**시나리오 2: 멀티 하이브리드 클라우드 환경의 네트워크 슬라이싱(SDN)**
- **문제 상황**: 기업의 프라이빗 클라우드와 AWS 뷰티넷 간의 트래픽 라우팅을 전통적 L3 라우터 하드웨어로 제어하려다 보니 변경 작업 시마다 수십 대의 장비 CLI를 수동으로 설정해야 하는 운영 파단 발생.
- **기술사적 결단**: 데이터 평면(Switch)과 제어 평면(Controller)을 완벽히 분리하는 **SDN (Software Defined Networking)** 아키텍처를 도입. OpenFlow 프로토콜을 통해 중앙의 SDN 컨트롤러가 모든 스위치의 플로우 테이블(Flow Table)을 코드로 밀어넣는 **네트워크 자동화(IaC)**를 구현하여 인프라 프로비저닝 시간을 주 단위에서 초 단위로 단축시킨다.

**도입 시 고려사항 (안티패턴)**
- **비대칭 라우팅(Asymmetric Routing) 방치**: 패킷이 나갈 때의 경로와 돌아올 때의 경로가 다를 경우, 상태 유지(Stateful) 검사를 수행하는 중간의 방화벽이나 IPS가 반환 패킷을 비정상으로 간주하여 드랍(Drop)시키는 치명적 장애가 발생한다. BGP 설정 시 Local Preference나 MED 값을 정교하게 튜닝하여 대칭적 경로를 강제해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량적 기대효과 (ROI)**
| 네트워크 최적화 기술 | 적용 대상 시스템 | 정량적 성능 지표 파급 효과 |
| :--- | :--- | :--- |
| **QUIC (HTTP/3) 전환** | 웹 서버 / 모바일 앱 | 초기 접속 연결 지연(Handshake) 50% 이상 감축 |
| **SDN / NFV 도입** | 데이터센터 코어망 | 물리적 장비 구매(CAPEX) 40% 절감, 변경 리드타임 99% 단축 |
| **L4/L7 Load Balancing** | 대규모 트래픽 인바운드 | 단일 서버 장애 시(RTO) 다운타임 0초 달성 (Seamless Failover) |

**미래 전망 및 진화 방향**:
인터넷의 인프라는 더 이상 구리선과 하드웨어의 전유물이 아니다. 5G/6G 기술은 **네트워크 슬라이싱(Network Slicing)**을 통해 물리적 망 하나를 자율주행용, IoT용, 스마트폰용 등 수백 개의 독립된 가상 망으로 분리해낸다. 네트워크는 점차 프로그래밍 가능한 소프트웨어 추상화 계층으로 완전히 편입되며, AI를 통한 지능형 트래픽 예측 및 자가 치유(Self-Healing Network) 시대로 결착될 것이다.

**※ 참고 표준/가이드**:
- IEEE 802.3 (Ethernet) / IEEE 802.11 (Wi-Fi): 물리 및 데이터링크 계층의 압도적 국제 표준.
- IETF / RFC (Request for Comments): 인터넷 프로토콜(TCP, IP, HTTP 등)의 사실상 표준 제정 기구.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [`[OSI 7계층 및 TCP/IP]`](@/PE/3_network/1_fundamentals/_index.md): 네트워크의 모든 통신 과정을 설명하는 대원칙이자 아키텍처의 뼈대.
- [`[TCP 혼잡 제어 및 UDP]`](@/PE/3_network/2_transport/_index.md): 시스템의 신뢰성과 속도를 결정짓는 4계층 프로토콜의 양대 산맥.
- [`[IP 라우팅 (OSPF/BGP)]`](@/PE/3_network/3_network/_index.md): 최적의 경로를 동적으로 산출하는 네트워크 계층의 핵심 알고리즘.
- [`[네트워크 보안 (IPSec/TLS)]`](@/PE/3_network/4_security/_index.md): 도청 및 위변조를 막기 위한 암호화 터널링 기술.
- [`[SDN 및 클라우드 네이티브 망]`](@/PE/3_network/6_sdn_nfv/_index.md): 하드웨어 종속성을 파괴하고 네트워크를 코드로 제어하는 현대 인프라의 종착점.