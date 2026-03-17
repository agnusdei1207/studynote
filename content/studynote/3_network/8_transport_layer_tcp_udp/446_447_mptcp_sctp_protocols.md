+++
title = "446-447. 차세대 전송 프로토콜: MPTCP와 SCTP"
date = "2026-03-14"
[extra]
category = "Transport Layer"
id = 446
+++

# 446-447. 차세대 전송 프로토콜: MPTCP와 SCTP

> ### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존 TCP (Transmission Control Protocol)의 단일 경계(Single Path) 한계를 극복하기 위해, **MPTCP(Multipath TCP)**는 대역폭 결합을, **SCTP(Stream Control Transmission Protocol)**는 멀티호밍 및 멀티스트리밍을 통해 네트워크 리던던시와 효율성을 혁신적으로 개선했습니다.
> 2. **가치**: **MPTCP**는 Wi-Fi와 Cellular(LTE/5G) 인터페이스를 동시에 활용하여 처리량(Throughput)을 최대화하고 서비스 무중단 시간(Zero Downtime)을 보장하며, **SCTP**는 Head-of-Line(HOL) Blocking 현상을 제거하여 지연 시간(Latency)을 획기적으로 단축시킵니다.
> 3. **융합**: 스마트폰의 데이터 통신, 5G 이동통신망의 시그널링(Signaling), Hyper-converged Infrastructure의 스토리지 트래픽 처리 등 안정성과 속도가 동시에 요구되는 미래 네트워크 인프라의 핵심 프로토콜로 자리 잡고 있습니다.

+++

### Ⅰ. 개요 (Context & Background)

현대의 인터넷 트래픽 패러다임은 단순한 "연결성"에서 "무중단 고성능 연결"으로 전이하고 있습니다. 기존의 **TCP (Transmission Control Protocol)**는 단일 송신자(Source IP)와 단일 수신자(Destination IP) 간의 **단일 경로(Single Path)**를 전제로 설계되었습니다. 이는 패킷 스위칝망의 효율성에는 기여했으나, 사용자가 이동성(Mobility)을 가지거나 단일 링크 장애가 발생할 경우 근본적인 취약점을 가질 수밖에 없었습니다.

예를 들어, Wi-Fi에서 셀룰러 네트워크로 이동하는 핸드오버(Handover) 구간에서는 기존 TCP 세션이 끊어지고 재연결(3-Way Handshake)해야 하므로, 순간적인 단절과 초기 혼잡 윈도우(Initial Congestion Window)로 인한 성능 저하가 불가피했습니다. 이러한 문제를 해결하기 위해 탄생한 것이 **MPTCP**와 **SCTP**입니다.

**MPTCP (Multipath TCP)**는 IETF(Internet Engineering Task Force) RFC 6824로 표준화되어, 하나의 TCP 세션 내에서 물리적으로 분리된 여러 경로(예: Wi-Fi + LTE)를 논리적으로 묶어 사용합니다. 반면, **SCTP (Stream Control Transmission Protocol)**는 RFC 4960으로 표준화되어, TCP의 신뢰성과 UDP의 실시간성을 결합하고, 특히 전화망(SS7)의 신뢰성을 IP 망으로 구현하기 위해 **멀티호밍(Multi-homing)** 기능을 탑재했습니다.

> **💡 비유**
> 기존 TCP가 '한 줄로 이어진 다리'라면, MPTCP는 다리가 끊어지거나 막혔을 때를 대비해 옆에 '보조 다리'를 미리 깔아두어 중단 없이 건너게 하는 기술이며, SCTP는 다리 위에서 차량 사고가 나도 다른 차선을 이용해 통행이 가능한 '다차선 고속도로'를 건설하는 것과 같습니다.

> **📢 섹션 요약 비유**: 마치 차량이 하나의 도로만 이용하다가 도로 공사로 막히면 꼼짝없이 갇히는 기존 방식(TCP)과 달리, 고속도로와 지하철을 동시에 이용해 목적지에 빨리 도착하거나(MPTCP), 여러 개의 차선 중 막힌 차선만 우회해서 전체 교통 흐름을 원활하게 하는(SCTP) 고속 교통 체계와 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 MPTCP와 SCTP의 내부 메커니즘을 심층 분석합니다. 두 프로토콜 모두 기존 TCP/IP 스택의 4계층(전송 계층)에 속하나, 패킷 구조와 세션 관리 방식에서 결정적인 차이를 보입니다.

#### 1. 핵심 구성 요소 비교

| 구성 요소 (Component) | MPTCP (Multipath TCP) | SCTP (Stream Control Transmission Protocol) | 비고 (Note) |
|:---|:---|:---|:---|
| **데이터 단위** | **Byte Stream** (TCP 호환) | **Chunk** (Message-based) | SCTP는 메시지 경계를 보존함 |
| **연결 단위** | **Subflow** (여러 개의 TCP 흐름) | **Association** (하나의 연결) | |
| **주소 체계** | MP_CAPABLE 옵션으로 협상 | **INIT Chunk**에서 IP 주소 리스트 교환 | SCTP는 다중 IP 지원이 필수적임 |
| **신뢰성 메커니즘** | 각 Subflow별 독립된 ACK 및 재전송 | TSN (Transmission Sequence Number) 기반 SACK (Selective ACK) | SCTP는 선택적 재전송으로 효율적 |
| **보안/연결 수립** | TCP 3-Way Handshake + MP_CAPABLE | **4-Way Handshake** (Cookie 기반) | SCTP는 DoS 방어에 유리 |

#### 2. MPTCP: Multipath TCP 동작 메커니즘

MPTCP는 기존 애플리케이션의 변경 없이 커널 레벨에서만 동작하도록 설계되었습니다. 이를 위해 TCP 옵션 필드(Option Kind 30)를 적극 활용합니다.

**[MPTCP 세션 설정 및 데이터 전송 흐름도]**
```ascii
                  Client (Wi-Fi + LTE)                    Server
1. [TCP SYN + MP_CAPABLE] ---------->  (초시 연결 시도, Key 교환)
   <---------------- [SYN+ACK + MP_CAPABLE]

   [Established] : Main Socket (MPTCP Session)

2. [TCP SYN + MP_JOIN] --------------->  (서브 플로우 추가, 예: LTE 추가)
   <---------------- [SYN+ACK + MP_JOIN]
   [Third ACK] ----------------------->

   <------ Data Distribution Manager ------>
   (Wi-Fi Path)        [SEQ: 100-200] ---------->  |
   (LTE Path)          [SEQ: 201-300] ------------> | -> [Receiver Buffer: Reassembly]
                                                     v
                                                [Application Data]
```

**심층 해설**:
1.  **MP_CAPABLE**: 최초 연결(Handshake) 시 양 끝단은 MPTCP 지원 여부와 인증 키(Authentication Key)를 교환합니다. 이로써 하나의 소켓이 논리적으로 여러 경로를 인식하게 됩니다.
2.  **MP_JOIN**: 이미 연결된 상태에서 새로운 인터페이스(예: Wi-Fi 켜짐)가 활성화되면, MP_JOIN 옵션이 담긴 SYN 패킷을 보내 기존 세션에 이 경로를 추가합니다. 이때 HMAC(Hash-based Message Authentication Code)을 통해 보안을 유지합니다.
3.  **Congestion Control**: 각 **Subflow**는 독립적인 혼잡 제어(Reno/CUBIC 등)를 수행하지만, 전체 대역폭 합이 네트워크 병목을 유발하지 않도록 **LIA (Linked Increases Algorithm)** 등의 결합 알고리즘을 사용합니다.

#### 3. SCTP: Stream Control Transmission Protocol 동작 메커니즘

SCTP는 메시지 지향(Message-oriented) 프로토콜로, **Association(연결)**이라는 용어를 사용합니다.

**[SCTP 멀티스트리밍 및 멀티호밍 구조]**
```ascii
Host A (Multi-homed)                        Host B (Multi-homed)
[Primary IP: 10.0.0.1]   <---->   [Primary IP: 192.168.0.1]
[Backup  IP: 10.0.1.1]   <---->   [Backup  IP: 192.168.1.1]

[SCTP Association]
   |
   +-- [Stream 1: Control Signal] ----> (TSN: 100, 101, 102...) [OK]
   |      (패킷 유실 시 다른 스트림에 영향 0%, HOL Blocking 해소)
   |
   +-- [Stream 2: Data Chunk] --------> (TSN: 200, 201 [Loss], 203...)
           ^ Retransmission via SACK
```

**심층 해설**:
1.  **멀티스트리밍 (Multi-streaming)**: TCP는 데이터가 순차대로 도착해야 하므로(HOL Blocking), 앞 패킷이 유실되면 뒤의 패킷들도 전달이 지연됩니다. SCTP는 하나의 Association 내에 여러 개의 독립적인 **Stream(물리적 연결 아님)**을 생성하여, Stream 1의 패킷이 유실되어도 Stream 2의 데이터는 즉시 상위 계층으로 전달됩니다.
2.  **멀티호밍 (Multi-homing)**: 하나의 Association에 여러 IP 주소를 바인딩합니다. Primary 경로에 장애(Failure)가 발생하면, SACK(Selective ACK) 메커니즘을 통해 이를 감지하고 즉시 Backup 경로로 전환합니다. 이 과정은 사용자 레벨에서 투명하게 일어납니다.
3.  **4-Way Handshake**: SCTP는 연결 설정 시 **INIT**, **INIT-ACK**, **COOKIE-ECHO**, **COOKIE-ACK**의 4단계를 거칩니다. 서버는 자원 할당 전 클라이언트가 보낸 쿠키(Cookie)를 다시 echo 받을 때까지 대기(Stateless)하므로, IP 스푸핑을 이용한 **SYN Flooding 공격**에 원천적으로 방어력을 가집니다.

> **📢 섹션 요약 비유**: MPTCP는 하나의 대형 파이프라인을 여러 개의 작은 파이프로 묶어 유량을 늘리는 방식(단일 목표, 다중 경로)이고, SCTP는 하나의 건물 내에 전기, 수도, 통신선을 각각 별도로 배선하여 하나가 끊겨도 다른 하나는 작동하게 하는 독립 배선 시스템(다중 목표, 독립 흐름)과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

이 섹션에서는 운영체제(OS) 및 네트워크 아키텍처 관점에서 MPTCP와 SCTP의 성능 차이를 정량적으로 분석합니다.

#### 1. 심층 기술 비교: HOL Blocking vs. Aggregation

| 비교 항목 | TCP (Legacy) | MPTCP | SCTP |
|:---|:---|:---|:---|
| **병목 처리 방식** | 단일 경로가 병목이 되면 전체 속도 저하 | 다른 경로의 대역폭으로 상쇄 가능 | 다른 스트림으로 우회하여 지연 최소화 |
| **데이터 전달 단위** | Byte Stream (메시지 경계 부재) | Byte Stream (TCP 호환성 유지) | **Message Chunk** (경계 보존) |
| **패킷 유실 영향도** | 유실 패킷까지 후속 패킷 전차 정지 | 해당 Subflow만 정지, 다른 경로는 지속 | 해당 Stream만 정지, 다른 Stream은 지속 |
| **헤더 오버헤드** | 20 Bytes (Min) | TCP Option + DSS(20~40 Bytes) 추가 | 12 Bytes (Common Header) + Chunk |

#### 2. 네트워크 토폴로지 및 시나리오 분석

**[시나리오: 스마트팩토리 로봇 제어]**
*   **요구사항**: 제어 신호(낮은 지연) + 센서 로그(높은 대역폭) / 이동성 필수
*   **TCP 적용 시 문제**: 무선(AP) 핸드오버 시 연결 단절(CLOSE_WAIT)로 로봇이 멈추거나 로그 손실 발생.
*   **MPTCP 적용 효과**: 제어 신호는 5G(Low Latency), 로그는 Wi-Fi(High Bandwidth)로 분산 전송 가능. 핸드오버 시 세션 유지.
*   **SCTP 적용 효과**: 제어 신호와 로그를 별도 Stream으로 전송하여, 로그 전송 패킷이 손실되어도 제어 신호는 지연 없이 도달.

#### 3. 주요 파라미터 및 수식

**MPTCP 처리량 (Throughput) 추정**:
$$ Total_{Throughput} \approx \sum_{i=1}^{N} Subflow_i \quad (\text{단, Coupled Congestion Control 적용 시}) $$
*   단순 합이 아닌, 공유 병목 구간(Resource Pooling)에서의 형평성을 고려한 LIA 알고리즘이 적용되어 다른 TCP 흐름에 과도한 피해를 주지 않음.

> **📢 섹션 요약 비유**: TCP가 '차선 하나가 막히면 도로 전체가 멈추는 시내 도로'라면, MPTCP는 '고속도로와 국도를 동시에 이용해 출퇴근길을 분산시키는 승용차'이고, SCTP는 '화물차와 승용차가 각각 전용 차로를 달리는 분리된 도로 체계'와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무 환경에서 MPTCP와 SCTP를 도입할 때 고려해야 할 전략적 의사결정 기준을 제시합니다.

#### 1. 기술적/운영적 도입 체크리스트

**도입 시 고려사항**:

| 체크 항목 | MPTCP | SCTP | 비고 |
|:---|:---|:---|:---|
| **OS 지원** | Linux (Kernel 3.6+), iOS (Apple), FreeBSD | Linux, BSD, Solaris (Windows 제한적) | **Apple은 MPTCP 강함 (Siri 등)** |
| **Middlebox 호환성** | **NAT/PAT 장비와의 호환성 이슈 발생 가능** (TCP Option 필드 인식 못함) | 기존 라우터/방화벽이 **Protocol Number 132**를 차단하는 경우 존재 | NAT Traversal 기술 필요 |
| **애플리케이션 수정** | **Kernel Stack 수정만으로 기존 App 호환** | **Socket API를 SCTP 전용 (`socket(AF_INET, SOCK_STREAM, IPPROTO_SCTP)`)으로 변경 필요** | MPTCP의 가장 큰 장점 |
| **주요 도입 분야** | Data Center, Mobile Offload, Siri | Telecom Signaling (SS7 over IP), Financial Trading |

#### 2. 결함 사례 및 안티패턴 (Anti-patterns)

*   **안티패턴 1: MPTCP를 활성화한 상태의 정