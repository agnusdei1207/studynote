+++
title = "354-356. EIGRP(Enhanced IGRP) 프로토콜 분석"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 354
+++

# 354-356. EIGRP(Enhanced IGRP) 프로토콜 분석

> ### 핵심 인사이트 (3줄 요약)
> 1. **본질**: EIGRP (Enhanced Interior Gateway Routing Protocol)는 거리 벡터(Distance Vector)의 단순함과 링크 상태(Link-State)의 빠른 속도를 결합한 고급 거리 벡터(Advanced Distance Vector) 프로토콜로, **DUAL (Diffusing Update Algorithm)** 알고리즘을 통해 루프 없는 신속한 경로 수렴을 달성합니다.
> 2. **가치**: **Feasible Successor (잠재적 후계자)**를 통해 사전에 계산된 백업 경로를 즉시 활용함으로써 장애 발생 시 수렴 시간(Convergence Time)을 1초 이내로 최소화하고, **Unequal Cost Load Balancing (비용 불균형 로드 밸런싱)**을 통해 대역폭 효율을 극대화합니다.
> 3. **융합**: RTP (Reliable Transport Protocol) 기반의 신뢰할 수 있는 전송과 PDM (Protocol Dependent Module) 구조를 통해 IP, IPX, AppleTalk 등 다양한 프로토콜을 지원하며, 현재는 대규모 엔터프라이즈 네트워크의 핵심 라우팅 엔진으로 활용됩니다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
EIGRP는 기존 IGRP의 단점을 보완하여 Cisco Systems가 개발한 고성능 라우팅 프로토콜입니다. 엄밀히 말해 링크 상태 프로토콜은 아니나, 인접 라우터와의 관계를 형성하고 토폴로지 데이터베이스를 유지한다는 점에서 **고급 거리 벡터(Advanced Distance Vector)** 또는 하이브리드 라우팅 프로토콜로 분류됩니다. EIGRP의 철학은 "빠른 수렴"과 "대역폭 절약"입니다. 전체 라우팅 테이블을 주기적으로 전달하는 RIP와 달리, EIGRP는 변화가 발생한 경로 정보만 neighbors에게 전파하며, 전송의 신뢰성을 보장하기 위해 전용 전송 계층인 **RTP (Reliable Transport Protocol)**를 사용합니다.

#### 2. 등장 배경 및 필요성
① **기존 한계**: RIP(Routing Information Protocol)는 홉 카운트(Hop Count) 15개 제한과 느린 수렴 속도 문제가 있었고, OSPF(Open Shortest Path First)는 링크 상태 데이터베이스(LSDB) 동기화를 위해 막대한 CPU 및 메모리 자원을 소비했습니다.
② **혁신적 패러다임**: Cisco는 IGRP의 편리함과 OSPF의 빠른 수렴 장점을 결합하여, 네트워크 변화 시에만 업데이트를 전송하고 즉시 우회 경로를 전환하는 EIGRP를 설계했습니다.
③ **비즈니스 요구**: 금융 거래나 화상 회의와 같이 끊김 없는 연결이 필수적인 실시간 서비스 환경에서, 장애 복구 시간을 0에 가깝게 만드는 기술적 요구가 EIGRP의 탄생 배경이 되었습니다.

#### 3. 메트릭 및 K-Value
EIGRP는 복합 메트릭(Composite Metric)을 사용하며, 기본적으로 **대역폭(Bandwidth)**과 **지연(Delay)**을 사용합니다. 이는 32비트 정수로 계산되어 24비트를 사용하는 IGRP에 비해 매우 정교한 경로 선택이 가능합니다. 메트릭 계산식은 다음과 같습니다.

$$Metric = \left[ K_1 \times Bandwidth + \frac{K_2 \times Bandwidth}{256 - Load} + K_3 \times Delay \right] \times \left[ \frac{K_5}{Reliability + K_4} \right]$$

> **💡 비유**: EIGRP의 동작 방식은 "스마트 내비게이션"과 같습니다. 단순히 거리가 짧은 길(RIP)을 찾는 것이 아니라, 도로의 넓이(대역폭)와 혼잡도(부하)를 종합적으로 고려하여 실제 이동 시간이 가장 빠른 길을 안내합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소
EIGRP의 아키텍처는 독립적인 프로토콜 모듈 위에서 구동되며, 다음과 같은 4대 핵심 구성 요소로 이루어져 있습니다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 비유 |
|:---|:---|:---|:---|
| **Neighbor Discovery** | 인접 라우터 식별 및 관리 | 멀티캐스트 주소(224.0.0.10)를 사용하여 Hello 패킷을 주고받으며, Hold Time 내에 응답이 없으면 연결을 해제함. | 주변에 있는 친구 인사하기 |
| **RTP (Reliable Transport Protocol)** | 전송 계층 신뢰성 보장 | EIGRP 패킷 전송을 담당하며, 순차 번호(Sequence Number)와 ACK를 통해 신뢰성 있는 전송을 보장함. Unicast/Multicast 혼용 가능. | 등기 우편 서비스 |
| **DUAL (Diffusing Update Algorithm)** | 루프 프리 경로 계산 | 경로 계산 알고리즘으로, Successor와 Feasible Successor를 결정하고 네트워크 장애 시 즉시 대체 경로로 전환(Switch)함. | 사고 대비본부 |
| **PDM (Protocol Dependent Modules)** | 레이어 3 프로토콜 지원 | IP, IPX, AppleTalk 등 각 네트워크 계층 프로토콜에 맞는 라우팅 로딩을 담당하는 모듈화된 구조. | 다국어 통번역기 |

#### 2. 패킷 유형 및 교환 과정
EIGRP는 다양한 유형의 패킷을 사용하여 정보를 교환합니다.

```ascii
+------------------+     +------------------+     +------------------+
|  Router A        |     |  Router B        |     |  Router C        |
+------------------+     +------------------+     +------------------+
| 1. Hello (224.0.0.10) --> | Neighbor Discovery      | (Hold Time 15s)  |
| <-- Ack (Hello)          | (Establish Neighbor)    |                  |
+------------------+     +------------------+     +------------------+
| 2. Update         --> | Topology Table Sync     | (Full Update)    |
| <-- Ack (Reliable)| | (Exchange Routes)       |                  |
+------------------+     +------------------+     +------------------+
| 3. Query (Change) --> | "Any better path to X?"  | (Diffusing Compute)|
| <-- Reply         -->| "No, I don't have."      |                  |
+------------------+     +------------------+     +------------------+
```
*   **해설**:
    1.  **Discovery**: 라우터들은 멀티캐스트 주소 `224.0.0.10`을 통해 Hello 패킷을 교환하며 Neighbor Table(이웃 테이블)을 구축합니다.
    2.  **Reliable Exchange**: RTP를 통해 Update 패킷을 교환하고, 이를 받은 쪽은 ACK 패킷으로 수신을 확 인합니다. 이 과정에서 Topology Table(토폴로지 테이블)이 완성됩니다.
    3.  **DUAL Operation**: 경로가 변경되면 Query(질의)를 보내고 Reply(응답)을 받으며 최적 경로를 다시 계산합니다. 이때 이미 계산된 Backup 경로가 있다면 Query 없이 즉시 전환합니다.

#### 3. DUAL 알고리즘 상세 및 코드
DUAL 알고리즘의 핵심은 **FD (Feasible Distance)**와 **AD (Advertised Distance/Reported Distance)**의 관계를 통해 루프 발생 여부를 판단하는 것입니다.

*   **Successor (후계자)**: 목적지까지 도달하기 위한 최적 경로.
*   **Feasible Successor (FS)**: `AD < FD(현재 Successor)` 조건을 만족하는 경로. (이웃이 목적지까지 가는 거리가 나보다 짧으면 루프가 아님)
*   **Active/Passive State**: 경로가 계산 중이면 **Active**, 안정적이면 **Passive** 상태입니다. Stuck-in-Active는 Active 상태가 너무 길어지는 장애 상황을 의미합니다.

```c
// Pseudo-code for Feasibility Condition Check
// AD: Advertised Distance (Neighbor's cost to destination)
// FD: Feasible Distance (My current best cost to destination)

void check_feasibility(Route *candidate) {
    if (candidate->AD < current_FD) {
        // 조건 만족: 루프가 발생하지 않음이 보장됨
        install_feasible_successor(candidate);
        printf("Feasible Successor found. Convergence immediate.\n");
    } else {
        // 조건 불만족: 루프 가능성 존재 -> 추가 계산 필요
        start_dual_calculation(candidate);
        printf("Query sent to neighbors. Waiting for Reply...\n");
    }
}
```

> **📢 섹션 요약 비유**: EIGRP의 아키텍처는 "정교한 물류 센터"와 같습니다. 상품(패킷)을 보낼 때 가장 빠른 도로(Successor)를 찾되, 만약의 사태에 대비해 미리 확인해둔 우회로(Feasible Successor)가 있다면 본사에 보고(DUAL)할 필요 없이 즉시 그쪽으로 상품을 보냅니다. 이때 모든 차량들에게 "길이 막혔으니 다른 길 찾아라"라고 소리치는 것이 아니라, 필요한 트럭한테만 조용히 연락(RTP)하여 혼란을 막습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 라우팅 프로토콜 심층 비교
EIGRP는 다른 주요 라우팅 프로토콜들과 구별되는 독특한 특징을 가집니다. 특히 **계층형 구조가 필요 없다**는 점과 **비용 불균형 로드 밸런싱**이 가능하다는 점이 OSPF와의 결정적인 차이입니다.

| 비교 항목 | EIGRP | OSPF (Open Shortest Path First) | RIP (Routing Information Protocol) |
|:---|:---|:---|:---|
| **알고리즘 분류** | 고급 거리 벡터 (Adv. DV) | 링크 상태 (Link-State) | 거리 벡터 (Distance Vector) |
| **메트릭 (Metric)** | 복합 (Bandwidth, Delay 등) | 비용 (Cost: 대역폭 역수) | 홉 카운트 (Hop Count) |
| **수렴 속도** | 매우 빠름 (FS에 의한 즉시 전환) | 빠름 (SPF 재계산) | 느림 (Timer 기반) |
| **네트워크 구조** | 플랫 (Flat), Area 구조 필수 아님 | 2단계 계층 구조 (Area 0 + Transit) 필수 | 플랫 (Flat) |
| **로드 밸런싱** | **비용 불균형(Unequal Cost) 가능** | 비용 균형(Equal Cost)만 가능 | 비용 균형(Equal Cost)만 가능 |
| **자원 소모** | CPU/메모리 사용량 중간 | CPU/메모리 사용량 많음 | CPU/메모리 사용량 적음 |
| **업데이트 방식** | 비주기적, 부분 업데이트 (224.0.0.10) | 트리거 기반 (Link flooding) | 주기적 (30초) 전체 업데이트 |

#### 2. 비용 불균형 로드 밸런싱 (Unequal Cost Load Balancing) 기술
EIGRP만의 독보적인 기능입니다. `variance` 명령어를 사용하여, 최적 경로의 메트릭 값에 `variance` 배수를 곱한 값보다 작은 메트릭을 가진 경로들을 모두 사용하여 트래픽을 분산합니다.

```ascii
[Scenario]
Destination: Network X
Path 1 (Successor) Metric = 100
Path 2 (FS) Metric        = 200
Path 3 (FS) Metric        = 400

[Configuration]
Router(config-router)# variance 3
! Accept paths with metric <= (100 * 3) = 300

[Traffic Distribution Result]
Path 1 (100): 200 / 500 = 40%
Path 2 (200): 200 / 500 = 40%
Path 3 (400): Rejected (> 300)

Note: Traffic ratio is inversely proportional to Metric.
```

#### 3. 타 과목 융합 및 시너지
*   **OS (운영체제) 관점**: EIGRP의 Reliable Transport Protocol(RTP)은 TCP와 유사하지만, 라우팅 프로토콜 특화된 가변의 윈도우 크기(Flow Control)와 멀티캐스트 지원을 통해 전송 효율을 높입니다. 이는 OSI 7계층의 전송 계층(Layer 4) 기능을 라우팅 프로토콜 내부에 구현한 사례입니다.
*   **DB (데이터베이스) 관점**: EIGRP는 최신 정보만을 유지하기 위해 **SRT (Source Route Tree)** 형태의 데이터를 관리하며, 이는 데이터베이스의 트랜잭션 로그(Transaction Log)와 유사하게 변경 사항만을 반영하여 무결성을 유지하는 방식과 유사합니다.

> **📢 섹션 요약 비유**: 다리가 하나인(OSPF 단일 경로) 도시와 여러 개의 다리를 종합적으로 관리하는(EIGRP) 도시의 차이와 같습니다. OSPF는 다리의 길이가 비슷해야만 두 다리를 모두 쓰지만, EIGRP는 한쪽 다리가 조금 멀더라도(EIGRP Variance), 교통 상황에 따라 굳이 한쪽으로 몰리지 않게 억지로 분산(부하 분산)시킬 수 있는 유연한 교통 통제 시스템입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정 매트릭스
**상황**: 금융 광역망에서 본행(A)과 지점(B), (C) 간의 연결성을 확보해야 한다. A-B 간 10G, A-C 간 1G 회선이 있으며, B와 C는 서로 100Mbps로 연결됨. 장애 시 1초 이내 복구가 필수적임.

*   **의사결정**:
    1.  OSPF를 사용할 경우: A-B 주 회선이 끊기면 SPF 알고리즘이 재계산되는 동안(수십 ms ~ 수초) 패킷 유실