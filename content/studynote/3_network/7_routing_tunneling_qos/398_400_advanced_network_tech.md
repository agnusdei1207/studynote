+++
title = "398-400. 기타 네트워크 계층 기술: IP SLA, Anycast, LISP"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 398
+++

# 398-400. 기타 네트워크 계층 기술: IP SLA, Anycast, LISP

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: IP SLA (IP Service Level Agreement)는 능동형 트래픽 생성을 통해 QoS (Quality of Service)를 정량화하고, Anycast는 단일 IP를 통해 최적 경로를 자동 선택하며, LISP (Locator/ID Separation Protocol)는 IP 주소의 정체성과 위치 정보의 결합을 분리하여 라우팅 scalability와 mobility를 해결한다.
> 2. **가치**: IP SLA는 고가용성(HA) 구현의 핵심 지표이며, Anycast는 CDN (Content Delivery Network)과 DDoS 방어의 기반이 되고, LISP는 Multihoming 및 Cloud Migration 시의 단절 없는 서비스 제공을 가능하게 한다.
> 3. **융합**: 이 기술들은 단순한 전송 계층 기능을 넘어, SDN (Software Defined Network) 제어 평면과 연동하여 지능적인 트래픽 엔지니어링을 구현하는 현대 네트워크 인프라의 필수 요소다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념 및 철학
현대의 IP 네트워크는 단순한 '연결성'을 넘어 '성능'과 '효율', 그리고 '이동성'을 보장해야 한다. 이를 위해 **IP SLA**는 네트워크 상태를 실시간으로 진단하는 의료 장비처럼, **Anycast**는 데이터를 가장 가까운 곳으로 유도하는 중력의 법칙처럼, **LISP**는 주소 체계의 유연성을 확보하는 사회보장번호 시스템처럼 작동한다.

#### 등장 배경
1.  **QoS 가시성 부족**: 기존의 Ping(ICMP)이나 Traceroute는 단순한 Reachability(도달 가능성)만 확인했을 뿐, VoIP나 재무 거래 등에 필요한 Jitter(지터)나 Packet Loss Ratio(패킷 손실률)와 같은 정밀한 성능 지표를 측정할 수 없었다.
2.  **글로벌 지연 최소화**: 콘텐츠의 용량이 커지면서 단일 서버에서 전 세계 트래픽을 처리하는 데 한계가 발생했고, 지리적 거리에 따른 지연(Latency)을 줄이기 위해 가까운 서버로 연결하는 기술이 필요했다.
3.  **Routing Table 폭발 및 Mobility**: 인터넷 성장으로 인해 Global Routing Table의 크기가 기하급수적으로 증가(Routing Table Explosion)했고, 서버가 물리적으로 이동할 때마다 IP 주소를 변경해야 하는 불편함을 해결해야 했다.

#### 💡 비유
이 시스템은 **도심 교통 통제 시스템**과 같다. 드론(IP SLA)을 띄워 실시간 교통 상황을 파악하고, 차량들이 GPS(Anycast)를 통해 가장 가까운 목적지 경로를 자동 선택하며, 차량 번호판(LISP EID)은 그대로 두고 위치 정보(LISP RLOC)만 변경하여 소통을 원활하게 한다.

#### 📢 섹션 요약 비유
이 섹션은 거대한 도시의 **교통 상황실을 구축하는 과정**과 같습니다. 단순히 도로가 뚫려 있는지 확인하는 것을 넘어, 실시간 교통 정체를 감시하고(IP SLA), 가장 빠른 경로로 유도하며(Anycast), 차량의 번호가 바뀌지 않아도 이동 경로를 자동으로 갱신해주는 스마트 시스템(LISP)을 도입하는 근간을 마련합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 섹션에서는 세 가지 기술의 상세 구조와 동작 메커니즘을 분석한다.

#### 1. 구성 요소 (핵심 모듈 분석)

| 기술 | 구성 요소 | 역할 | 내부 동작 | 비유 |
|:---|:---|:---|:---|:---|
| **IP SLA** | Source (Sender) | 성능 측정 요청자 | Synthetic Traffic을 생성하여 타임스탬프를 찍어 전송 | 비밀 요원 |
| | Target (Responder) | 응답 전담 서버 | 고정 포트(UDP 1967 등) 리스닝, 정밀한 응답 시간 반환 | 협력 요원 |
| **Anycast** | Anycast Prefix | 공유 IP 주소 블록 | 여러 AS에 동일한 Prefix가 존재 | 동일한 상호명 |
| | BGP Router | 경로 선택자 | IGP Metric을 기반으로 가장 가까운 Next-hop으로 유도 | 내비게이션 |
| **LISP** | EID (Endpoint ID) | 단말 식별자 | 호스트의 영구적 IP, 라우팅 불가 | 주민등록번호 |
| | RLOC (Routing Locator) | 라우터 위치 | 네트워크 위치(라우터 IP), 라우팅 가능 | 현재 주소지 |
| | Map-Server | 위치 데이터베이스 | EID-to-RLOC 매핑 정보 저장 및 응답 | 등기부 등본관 |

#### 2. IP SLA: 정밀 측정 및 트랙킹 메커니즘

IP SLA는 라우터의 Control Plane을 활용하여 지연 시간, 왕복 시간(RTT), Jitter, Packet Loss 등을 측정한다. 특히 **Object Tracking** 기능과 연동하여 라우팅 테이블을 동적으로 변경한다.

*   **동작 플로우**: `ICMP Echo` -> `Timestamp` -> `Threshold Check` -> `Track State Change` -> `Route Manipulation`
*   **코드 예시 (Cisco IOS Syntax)**:
    ```bash
    ! 1ms 간격으로 100Hz Frequency로 측정, Threshold 200ms 설정
    ip sla 10
      icmp-echo 1.1.1.1 source-interface Ethernet0/0
      frequency 5
      threshold 200
      timeout 1000
    ip sla schedule 10 life forever start-time now
    ! Track 10번이 SLA 상태를 감시, 실패 시 Static Route 삭제
    track 10 ip sla 10 reachability
    ip route 0.0.0.0 0.0.0.0 203.0.113.1 track 10
    ip route 0.0.0.0 0.0.0.0 198.51.100.1 20  ! Floating Static (Backup)
    ```

#### 3. ASCII 다이어그램: IP SLA 동적 경로 전환

아래는 IP SLA를 통해 기본 경로(Main Link)의 지연이 Threshold를 초과하면 백업 경로(Backup Link)로 우회하는 시나리오다.

```ascii
+------------------+               +------------------+
|   Edge Router    |               |   Target Server  |
| (Source Device)  |               |  (1.1.1.1)        |
+--------+---------+               +--------+---------+
         |                                   ^
         | (1) IP SLA Probe (ICMP Echo)      | (2) Echo Reply (Timestamp)
         |---------------------------------->|
         |
         v
[ SLA Engine Logic ]
 - RTT: 5ms (Normal) -> Track State: UP -> Use Primary Path
 - RTT: 500ms (Bad!)  -> Track State: DOWN -> Use Backup Path

         | (3) Data Traffic Flow Decision
         |
         +-----------------------+
         |                       |
         v                       v
+--------+---------+    +--------+---------+
|  Primary ISP     |    |  Backup ISP      |
|  (Next-hop: A)   |    |  (Next-hop: B)   |
| [ Active ]       |    |  [ Standby ]     |
+------------------+    +------------------+
```
*(해설: 라우터는 지속적으로 Target에 Probe를 전송한다. 만약 회선 장애로 인해 응답이 늦어지거나 끊기면 IP SLA 프로세스가 이를 감지하고 Object Tracking 상태를 DOWN으로 변경한다. 그러면 라우팅 테이블의 관리 거리(AD)에 의해 백업 경로가 실제 경로로 승격되어 패킷을 우회시킨다.)*

#### 4. LISP (Locator/ID Separation Protocol) 아키텍처

LISP는 기존 IP 아키텍처의 **语义 오버로드(Semantic Overload)** 문제를 해결한다.
*   **EID (Endpoint ID)**: 호스트의 식별자 (변하지 않음).
*   **RLOC (Routing Locator)**: 네트워크의 위치 (라우터 주소).
*   **Map-Resolver/MAP-Server**: EID를 질문하면 RLOC를 알려주는 시스템.

#### 5. ASCII 다이어그램: LISP 캡슐화 및 터널링

LISP 라우터(xTR)는 수신 패킷의 EID를 확인하고, 이를 목적지 RLOC로 캡슐화(Encapsulation)하여 전송한다.

```ascii
 Host A (EID: 10.1.1.1)             Host B (EID: 10.2.2.2)
      |                                   ^
      | (1) Standard IP Packet            | (6) Decapsulated Packet
      | [Src: 10.1.1.1, Dst: 10.2.2.2]    | [Src: 10.1.1.1, Dst: 10.2.2.2]
      v                                   |
[ ITR (Ingress Tunnel Router) ]     [ ETR (Egress Tunnel Router) ]
      |                                   ^
      | (2) Mapping Request (Map-Resolver) | (5) Encapsulation Removed
      | "Who has 10.2.2.2?"               |
      v                                   |
[ Map-Server / MS ]                    (3) Mapping Reply: "RLOC is 5.5.5.5"
      |                                   |
      +-----------------------------------+
      |
      v
      | (4) LISP Encapsulated Packet
      | [Outer Header: Src(RLOC-A)->Dst(RLOC-B 5.5.5.5)]
      | [Inner Header: Src(EID 10.1.1.1)->Dst(EID 10.2.2.2)]
      |
      +----------------------------------------------> Internet Core
```
*(해설: ITR은 내부 패킷을 수신하면 목적지 EID(10.2.2.2)의 RLOC를 Map-System에 조회한다. 획득한 RLOC(5.5.5.5)를 Outer Header의 목적지로 하여 원래 패킷을 감싼(LISP Header 추가) 후 전송한다. ETR은 도착하면 Outer Header를 제거하고 호스트 B에게 전달한다. 이 과정에서 Core 라우터들은 EID를 전혀 알지 못한다.)*

#### 📢 섹션 요약 비유
LISP는 **편지 봉투와 우편함 시스템**과 같습니다. 편지 내용(IP 데이터그램)에는 받는 사람의 이름(EID)과 집 주소(RLOC)가 모두 적혀 있지만, 우체국(코어 라우터)은 집 주소(RLOC)만 보고 배달합니다. 만약 받는 사람이 이사를 간다면, 우체국 데이터베이스(Map-Server)만 업데이트하면 되고, 편지지에 적힌 이름(EID)은 바뀌지 않아도 계속 편지를 받을 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. IP Anycast vs. Unicast 심층 비교

| 비교 항목 | Unicast (단일 캐스트) | Anycast (애니캐스트) |
|:---|:---|:---|
| **정의** | 1:1 통신. 고유한 IP 주소 할당 | 1:Nearest 통신. 동일 IP를 여러 노드가 공유 |
| **라우팅 방식** | 목적지까지의 단일 경로 | BGP (Border Gateway Protocol)에 의해 최단 경로 자동 선택 |
| **주요 장점** | 구현简单, 연결 상태 유지 용이 | 지연 시간(Latency) 최소화, DDoS 분산 |
| **주요 단점** | 특정 지점 트래픽 몰림(Bottleneck) | Session 유지 어려움(Path Flapping 발생 시) |
| **활용 사례** | 일반적인 웹 서비스, 이메일 | Root DNS 서버 (13개의 루트 서버 주소, 수백 대의 인스턴스), CDN 캐시 노드 |

#### 2. 기술 간 시너지 및 융합

1.  **IP SLA + SDN (Software Defined Network)**:
    *   기존의 IP SLA는 개별 라우터 내에서 동작하지만, SDN 컨트롤러는 전체 네트워크의 SLA 데이터를 수집하여 글로벌 최적화 경로를 설정할 수 있다. 예를 들어, 특정 링크의 Jitter가 일정 수준 이상이면 컨트롤러가 즉시 Flow Rule을 변경하여 트래픽을 우회시킨다.
2.  **LISP + Cloud Migration**:
    *   물리적 데이터센터에서 클라우드로, 혹은 클라우드 리전 간에 가상 머신(VM)을 이동시킬 때, LISP를 사용하면 VM의 IP 주소(EID)를 변경할 필요 없이 Map-Server의 매핑 정보만 갱신하면 된다. 이는 **Live Migration**의 네트워킹 병목을 해결한다.
3.  **Anycast + DDoS Mitigation**:
    *   공격자가 Anycast IP를 공격하더라도, 트래픽은 자연스럽게 여러 지역(POP)으로 분산된다. 이를 통해 대용량 L3/L4 DDoS 공격을 흡수하고 방어(Cleaning Center)한 후 정상 트래픽만 원본 서버로 라우팅하는 **Scrubbing Center** 아키텍처를 구현할 수 있다.

#### 3. 정량적 성능 지표 비교 (유도 가능성)

*   **Latency (지연 시간)**: Anycast 도입 시 RTT 평균 50~200ms 개선 (예: 미국 동부에서 미국 서부 접속 시).
*   **Convergence Time (수렴 시간)**: IP SLA Tracking 기반의 경로 전환은 일반 BGP Convergence(수십 초~수분)보다 훨씬 빠른 **1~3초 내** 경로 복구 가능.

#### 📢 섹션 요약 비유
이러한 기술들의 조합은 **글로벌 물류 센터의 운영 시스템**과 같습니다. Anycast로 각 국가에 창고를 두어 배송 시간을 줄이고, IP SLA로 도로 상황을 모니터링하여 배송 경로를 실시간 수정하며, LISP를 통해 창고 이동 시에도 고객의 주소(세션)가 끊기지 않도록 관리하는 통합 물류 솔루션이 됩니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 과정

**Scenario A: 금융권 이중화 회선 구축