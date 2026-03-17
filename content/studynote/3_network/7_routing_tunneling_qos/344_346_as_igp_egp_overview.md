+++
title = "344-346. AS(자율 시스템)와 라우팅 프로토콜 분류"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 344
+++

# 344-346. AS(자율 시스템)와 라우팅 프로토콜 분류

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인터넷은 수만 개의 **AS (Autonomous System)**라는 독립된 행정 구역들이 연결된 '네트워크의 네트워크(Network of Networks)' 구조를 가집니다.
> 2. **가치**: **IGP (Interior Gateway Protocol)**는 AS 내부의 빠른 수렴성을, **EGP (Exterior Gateway Protocol)**는 AS 간 정책 기반의 제어 가능성을 극대화하여 확장성을 확보합니다.
> 3. **융합**: 거리 벡터와 링크 상태 알고리즘의 상호 보완적 구조를 통해 소규모 LAN부터 대규모 글로벌 백본까지 계층별 라우팅 최적화를 실현합니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 및 정의
**AS (Autonomous System)**는 단일 관리 주체(예: ISP, 대학, 대기업)에 의해 운영되며, 동일한 라우팅 정책(Routing Policy)과 관리 체계를 공유하는 하나 이상의 네트워크 라우터의 집합을 의미합니다. 각 AS는 전 세계적으로 유일한 식별자인 **ASN (Autonomous System Number)**을 부여받습니다. 16비트(65536개)의 한계를 극복하기 위해 현재는 32비트(약 42억 개) 체계로 확장되었습니다.

### 💡 비유
AS는 **'독립적인 국가'**와 같습니다. 국가마다 도로법과 교통 체계(라우팅 정책)가 다르듯, AS마다 내부에서 패킷을 처리하는 방식이 다릅니다.

### 등장 배경
① **초기 인터넷의 한계**: 초기 인터넷(**ARPANET**)은 소규모 네트워크 간의 단순 연결로, 모든 경로 정보를 모든 라우터가 가지는 **Flat (평면) 구조**였습니다. 네트워크가 성장하면서 라우팅 테이블이 기하급수적으로 증가하는 **Routing Explosion** 문제가 발생했습니다.
② **계층적 라우팅의 도입**: 거대한 네트워크를 여러 개의 관리 영역(AS)으로 나누고, 영역 내부에서 쓰는 지도와 영역 밖으로 나가기 위한 지도를 분리하여 관리 필요성이 대두되었습니다.
③ **현재의 비즈니스 요구**: 클라우드 서비스의 확산으로 **트래픽 엔지니어링(Traffic Engineering)**과 비용 최적화가 중요해지면서, AS 간 연결에서는 단순히 '빠른 길'이 아닌 '싼 길'이나 '보안이 강화된 길'을 선택하는 정책 기반 라우팅이 필수가 되었습니다.

### 📢 섹션 요약 비유
> "마치 거대한 대륙을 여러 나라(AS)로 나누어 각자 내부 도로(IGP)는 잘 닦아두고, 국경 간 통행(EGP)은 조약과 관세에 따라 별도의 고속도로(Backbone)를 운영하는 것과 같습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 라우팅 프로토콜의 2중 체계 (IGP vs EGP)
인터넷 라우팅은 크게 **AS 내부용**과 **AS 외부용**으로 나뉩니다.

| 구분 | **IGP (Interior Gateway Protocol)** | **EGP (Exterior Gateway Protocol)** |
|:---:|:---|:---|
| **Full Name** | Interior Gateway Protocol | Exterior Gateway Protocol |
| **적용 범위** | **AS 내부** (Intra-domain) | **AS 사이** (Inter-domain) |
| **주요 목적** | 빠른 수렴, 내부 망 최적 경로 탐색 | 정책(Policy) 기반 경로 제어, 루프 방지 |
| **속도/성능** | 고속 처리, 정교한 메트릭 지원 | 처리 속도보다는 정책 준수 우선 |
| **대표 프로토콜** | **OSPF**, **IS-IS**, **RIP**, **EIGRP** | **BGP** (Border Gateway Protocol) |
| **비유** | 내비게이션 앱의 '자동차 전용도로' 모드 | 국가 간 '외교 채널' 및 관세 정책 |

### 2. 아키텍처 다이어그램 및 동작 원리

아래는 **AS 100 (ISP)**과 **AS 200 (Content Provider)** 간의 라우팅 정보 교환 과정을 도식화한 것입니다. 내부는 **OSPF**로 정보를 모으고, 외부와는 **BGP**로 정보를 교환합니다.

```ascii
      [ 인터넷 백본 (Internet Backbone) ]
                 ▲      ▲
                 │ eBGP │  (External BGP: 다른 AS 간 정보 교환)
                 │      │
      ┌──────────┴───┐  ┌───┴───────────┐
      │  R1 (Border) │  │  R2 (Border)  │  <-- 경계 라우터 (ASBR)
      │  ┌───────────┐│  │┌─────────────┐│
      │  │ AS 100    ││  ││ AS 200      ││
      │  │  IGP Area ││  ││  IGP Area   ││
      │  │  (OSPF)   ││  ││  (IS-IS)    ││
      │  │  R3──R4──R5││  ││R6──R7──R8   ││
      │  └───────────┘│  │└─────────────┘│
      └──────────────┘  └───────────────┘
            ▲                  ▲
            │ iBGP/IGP         │
      (내부 라우팅 정보 공유)   (내부 라우팅 정보 공유)
```

**[다이어그램 해설]**
1.  **AS 내부(IGP)**: AS 100 내부의 라우터들(R3, R4, R5)은 **OSPF (Open Shortest Path First)** 프로토콜을 통해 서로의 링크 상태(Link-State) 정보를 교환합니다. 이를 통해 AS 내부의 모든 라우터는 동일한 내부 지도(Topology DB)를 가지게 되며, R1(경계 라우터)에 도달하기 위한 최적의 내부 경로를 계산합니다.
2.  **AS 경계(BGP)**: R1과 R2는 서로 다른 AS에 속해 있으므로 **BGP (Border Gateway Protocol)**를 사용합니다. R1은 "AS 100에 속한 네트워크 1.1.1.0/24는 내가 책임진다"라는 정보를 R2에게 알립니다(NLAP 교환).
3.  **정책 적용**: 단순히 거리가 짧다고 해서 경로가 선택되지 않습니다. AS 200 입장에서 R1으로 가는 경로가 있더라도, R2가 "AS 100을 경유하는 것은 비용이 비싸다"는 정책(Policy)을 가지고 있다면 다른 경로를 선택하거나 우선순위를 낮출 수 있습니다.

### 3. 핵심 알고리즘 및 코드 스니펫
**OSPF (Link-State Algorithm)**는 다익스트라(Dijkstra) 알고리즘을 사용하여 최단 경로 트리(SPT)를 생성합니다.

```python
# [개념적 Python 코드] OSPF Link-State Cost 계산
# 각 인터페이스의 비용(Cost)은 대역폭에 반비례하여 결정됨
def calculate_interface_cost(bandwidth_kbps, reference_bw=100_000_000):
    """
    OSPF Cost = Reference Bandwidth / Interface Bandwidth
    """
    if bandwidth_kbps == 0:
        return float('inf')
    return int(reference_bw / bandwidth_kbps)

# 예시: 1Gbps 링크와 100Mbps 링크의 비용 계산
cost_gigabit = calculate_interface_cost(1_000_000_000)  # 결과: 1
cost_fasteth = calculate_interface_cost(100_000_000)   # 결과: 10
# 라우터는 Cost 1인 경로를 최적 경로로 선택함
```

### 📢 섹션 요약 비유
> "AS는 하나의 건물이고, IGP는 건물 내부의 복도와 엘리베이터를 안내하는 내부 배치도이며, EGP는 다른 건물로 갈 때 사용하는 지하철 노선도와 같습니다. 내부에서는 엘리베이터(IGP)가 빠르지만, 건물 간 이동은 지하철(EGP) 정류장과 노선을 확인해야 합니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 라우팅 알고리즘 심층 기술 비교
라우팅 프로토콜은 경로를 학습하는 방식에 따라 크게 **Distance Vector (거리 벡터)**와 **Link-State (링크 상태)**로 나뉩니다.

| 비교 항목 | **Distance Vector (RIP, IGRP)** | **Link-State (OSPF, IS-IS)** |
|:---|:---|:---|
| **동작 원리** | 인접 라우터와만 라우팅 테이블 교환 | 네트워크 전체의 토폴로지 정보 공유 (LSA) |
| **정보 범위** | "어디로(Destination) 얼마나(Metric)?" | "전체 맵(Topology)" 정보 |
| **수렴 속도** | 느림 (Hold-down timer 등 사용) | 매우 빠름 (Event-triggered update) |
| **Loop 처리** | **Split Horizon**, Route Poisoning 등 | 자체적으로 Loop 방지 (Full Map 보유) |
| **자원 소모** | 메모리/CPU 사용량 적음 | CPU/메모리/링크 대역폭 많이 사용 |
| **확장성** | 소규모 네트워크에 적합 | 대규모 네트워크에 적합 (Area 구성) |

### 2. 과목 융합 및 시너지 분석

#### [네트워크 + 보안] : BGP의 보안 취약점 (BGP Hijacking)
- **기술적 상관관계**: EGP의 표준인 **BGP**는 기본적으로 인접한 AS와 신뢰 관계를 형성하며 정보를 교환합니다. 하지만 암호화된 인증 절차(Origin Validation) 없이 경로 정보를 받아들이기 때문에, 악의적인 AS가 자신이 특정 IP 대역의 소유자라고 거짓 정보를 유포할 경우(**BGP Hijacking**), 전 세계 트래픽이 공격자에게 우회되는 치명적인 보안 사고로 이어질 수 있습니다.
- **해결책 (융합)**: 최근에는 **RPKI (Resource Public Key Infrastructure)** 기술을 도입하여 라우팅 정보의 출처를 암호적으로 검증하는 보안 프로토콜과의 융합이 진행되고 있습니다.

#### [OS + 네트워크] : TTL과 라우팅 Loop
- **기술적 상관관계**: 거리 벡터 방식(RIP)에서 라우팅 정보가 순환하는 현상(**Routing Loop**)이 발생하면, 패킷이 네트워크를 맴돌게 됩니다. 이때 **OS (Operating System)**의 네트워크 스택이 패킷 헤더에 설정한 **TTL (Time To Live)** 값이 0이 될 때 패킷을 폐기(Discard)하지 않는다면, 네트워크 대역폭은 순식간에 포화 상태에 빠지게 됩니다.
- **시사점**: IGP 설계(OSPF 채택)는 네트워크 장비끼리의 문제뿐만 아니라, 단말기 OS의 패킷 생명 주기 관리(TTL)와 직결되는 성능 이슈입니다.

### 📢 섹션 요약 비유
> "거리 벡터는 '소문(Rumor)'처럼 이웃에게만 듣고 전달하는지라 정보가 뒤왕그러져 있을 수 있지만, 링크 상태는 '위성 사진(Full Map)'처럼 전체 구조를 한눈에 보기 때문에 길을 잃을 일이 없습니다. 하지만 위성 사진을 다운로드받으려면 데이터가 많이 필요하듯 링크 상태는 더 많은 자원을 필요로 합니다."

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정 과정

**[상황]** A 기업은 본사와 5개의 지사를 연결하는 **MPLS (Multiprotocol Label Switching)** 망을 구축하려고 합니다. 본사에는 서버 팜이 있고, 지사들은 소규모 트래픽을 사용합니다.

1.  **IGP 선택 (내부망)**:
    *   **Decision**: 복잡한 메시 구조와 빠른 장애 복구(Failover)가 중요하므로 거리 벡터 방식의 **RIP** 배제.
    *   **Standard**: 업계 표준인 **OSPF**를 채택하여 Area 0(Backbone)을 중심으로 계층적 설계를 진행한다. (Cisco 장비 위주라면 EIGRP도 고려 가능하나 멀티벤더 환경 대응을 위해 OSPF 선호)

2.  **EGP 선택 (ISP 연동)**:
    *   **Decision**: 인터넷 서비스 제공자(ISP)와의 연결에는 유일한 표준 프로토콜인 **BGP-4**를 사용.
    *   **Policy**: 단순 대역폭 확보가 아니라, 두 개의 서로 다른 ISP(이중화)를 연결하고 트래픽 비용에 따라 경로를 분산(AS-Path Prepend나 Local Preference 속성 활용)하는 정책을 설정한다.

### 2. 도입 체크리스트

| 구분 | 점검 항목 | 비고 |
|:---|:---|:---|
| **기술적** | [ ] 네트워크 규모(라우터 수)에 따른 프로토콜 선정 (RIP < 15홉 제한 유의) | 소규모는 RIP, 대규모는 OSPF/IS-IS |
| [ ] 메트릭(Metric) 설정의 일관성 확보 | Bandwidth, Delay, Load 등 |
| [ ] Area (OSPF) 또는 AS (BGP) 번호 할당 계획 | IANA 할당된 ASN 확인 |
| **운영/보안** | [ ] OSPF 인증(Authentication) 설정 | 평문 패스워드 방지 (MD5 인증 권장) |
| [ ] BGP Route Reflector 설정 여부 | IBGP Full-mesh 연결의 오버헤드 해소 |
| [ ] Graceful Restart 지원 여부 | 장비 재기동 시 경로 유지 용이성 확인 |

###