+++
title = "339-343. 라우팅의 기초: 정적/동적 라우팅과 메트릭"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 339
+++

# 339-343. 라우팅의 기초: 정적/동적 라우팅과 메트릭

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네트워크의 **라우팅(Routing)**은 데이터 패킷을 목적지까지 전달하기 위한 경로 설정 기술로, 관리자가 수동으로 설정하는 **정적 라우팅(Static Routing)**과 라우터 간 정보 교환으로 자동 생성하는 **동적 라우팅(Dynamic Routing)**으로 대별됩니다.
> 2. **가치**: 정적 라우팅은 보안성과 리소스 효율성이 뛰어나 소규모 망에 적합하며, 동적 라우팅은 **컨버전스(Convergence, 수렴)** 능력을 통해 장애 복구와 유연성을 확보하여 대규모 망의 필수 요소입니다.
> 3. **융합**: 최적 경로 선정을 위해 **메트릭(Metric, 비용)**과 **AD(Administrative Distance, 관리 거리)**라는 이중 필터링 알고리즘을 사용하며, 이는 망 설계 시 가용성(Availability)과 신뢰성(Reliability)을 보장하는 핵심 메커니즘입니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**라우팅(Routing)**이란 **IP (Internet Protocol)** 패킷을 송신자에서 수신자로 전달하기 위해 네트워크 상에서 최적의 경로를 선택하는 과정을 의미합니다. 이 과정은 **L3 (Layer 3)** 계층 장비인 **라우터(Router)**의 핵심 기능이며, 경로 정보를 저장하는 **RIB (Routing Information Base)**, 즉 라우팅 테이블을 참조하여 수행됩니다. 라우팅 경로를 결정하는 방식은 크게 관리자가 경로를 직접 입력하는 **정적 라우팅(Static Routing)**과 라우팅 프로토콜을 통해 자동으로 경로를 학습하는 **동적 라우팅(Dynamic Routing)**으로 나뉩니다.

**💡 비유**
건물의 비상구 안내도(정적)와 실시간 교통 정보 앱 내비게이션(동적)의 차이와 같습니다. 비상구 안내도는 변하지 않지만 고정되어 있고, 내비게이션은 상황에 따라 경로를 바꿉니다.

**등장 배경**
1.  **기존 한계**: 초기 인터넷망은 규모가 작고 토폴로지 변화가 드물어 관리자가 수동으로 경로를 입력해도 무방했습니다. 하지만 네트워크 규모가 거대해지고 **링크 장애(Link Failure)**가 빈번해지면서, 수동 관리의 한계에 봉착했습니다.
2.  **혁신적 패러다임**: 복잡한 망에서도 장애 발생 시 자동으로 우회 경로를 설정하는 **동적 라우팅 프로토콜(Routing Protocol)** 등장. 이로 인해 망의 **가용성(Availability)**이 획기적으로 개선되었습니다.
3.  **현재의 비즈니스 요구**: 현재는 보안이 중요한 구간에는 정적 라우팅을, 그 외 대규모 트래픽이 흐르는 백본 구간에는 동적 라우팅을 혼용하는 하이브리드 설계가 표준으로 자리 잡았습니다.

**📢 섹션 요약 비유**
네트워크 라우팅 체계를 수하물 시스템에 비유한다면, **정적 라우팅**은 "이 수하물은 1번 벨트로 무조건 보내라"는 고정된 매뉴얼에 따르는 것이고, **동적 라우팅**은 "1번 벨트가 막히면 2번으로 자동으로 돌려라"라는 지능형 컨베이어 벨트 시스템을 운영하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 정적 vs 동적 라우팅 상세 분석

라우팅 경로를 학습하는 두 가지 핵심 메커니즘의 내부 동작과 특성을 비교 분석합니다.

| 구분 | 정적 라우팅 (Static Routing) | 동적 라우팅 (Dynamic Routing) |
|:---|:---|:---|
| **정의** | 관리자가 CLI 명령어 등을 통해 수동으로 경로 설정 | **IGP (Interior Gateway Protocol)** 또는 **EGP (Exterior Gateway Protocol)**를 통해 자동 학습 |
| **리소스** | **CPU (Central Processing Unit)** / **RAM (Random Access Memory)** 사용량极少 | 망 정보 교환을 위한 CPU 및 메모리 리소스 소모 큼 |
| **확장성** | 작은 규모에 적합 (Scalability 낮음) | 대형 규모 및 복잡한 토폴로지에 필수적 |
| **장애 대응** | 장애 발생 시 자동 복구 불가 (Convergence 없음) | 장애 감지 시 자동으로 우회 경로 설정 (Fast Convergence) |
| **주요 프로토콜** | 없음 (설정값 Static Route) | RIP, OSPF, EIGRP, BGP 등 |
| **보안성** | 라우팅 정보 노출 없어 상대적으로 높음 | 잘못된 라우팅 정보 인젝션 위험 존재 (인증 필요) |

#### 2. 경로 선정의 이중 필터링: Metric vs AD

**라우터(Router)**가 최적 경로(Best Path)를 결정하는 과정은 매우 엄격한 알고리즘을 따릅니다.

```ascii
+---------------------------------------------------------------+
|                [ 라우터 라우팅 테이블 결정 과정 ]              |
+---------------------------------------------------------------+
|                                                               |
|  1. 경로 수신 (Routing Information Sources)                    |
|     ├─ 정적 라우팅 (Static Route)                              |
|     ├─ OSPF (Open Shortest Path First)                        |
|     └─ RIP (Routing Information Protocol)                     |
|                     ↓                                         |
|  2. 관리 거리 비교 (Administrative Distance Check)            |
|     [ 신뢰도 경쟁 ]                                           |
|     "어떤 정보 출처가 더 믿을 만한가?"                         |
|                     ↓                                         |
|  3. 메트릭 비교 (Metric Comparison)                           |
|     [ 비용 경쟁 ]                                             |
|     "같은 출처라면, 어느 길이 더 저렴하고 빠른가?"             |
|                     ↓                                         |
|  4. 최종 등록 (Routing Table Installation)                    |
|     └─ Next Hop & Interface 결정                              |
|                                                               |
+---------------------------------------------------------------+
```

**① 관리 거리 (AD, Administrative Distance)**
- **정의**: 서로 다른 라우팅 프로토콜이나 소스(Static, Connected 등)로부터 학습한 같은 목적지 경로 중, 어떤 정보를 더 신뢰할지 결정하는 **신뢰도 점수**입니다. **0~255**의 값을 가지며, 값이 **낮을수록 우선순위**가 높습니다.
- **핵심 원리**: 만약 **OSPF(AD 110)**와 **RIP(AD 120)**가 모두 "192.168.1.0/24로 가는 길을 안다"고 주장하면, 라우터는 AD가 더 낮은 OSPF의 정보만을 RIB에 등록하고 RIP의 정보는 버립니다(Discard).

**② 메트릭 (Metric)**
- **정의**: **동일한 라우팅 프로토콜 내**에서 여러 개의 후보 경로가 존재할 때, 그중 가장 최적의 경로를 선정하기 위해 계산하는 **비용 값(Cost)**입니다. 값이 **낮을수록 좋은 경로**입니다.
- **주요 메트릭 유형**:
  - **Hop Count (홉 수)**: 거쳐야 하는 라우터 개수 (RIP 사용). 최대 15홉 제한.
  - **Bandwidth (대역폭)**: 링크의 전송 속도 (OSPF 주요 고려 요소).
  - **Delay (지연 시간)**: 패킷이 목적지까지 도달하는 데 걸리는 시간 (EIGRP).
  - **Cost (비용)**: 대역폭을 역수로 취해 계산한 값 (OSPF Cost = 10^8 / Bandwidth).

**③ 라우팅 테이블 구조 예시 (시각화)**

```ascii
      [Destination]    [AD/Metric]    [Next Hop]    [Interface]
      -----------------------------------------------------------
      10.1.1.0/24      S*    0/0       0.0.0.0       Ethernet0/0
      192.168.10.0     O     110/20    10.1.1.2      Serial0/0
      192.168.10.0     R     120/2     10.1.1.3      Serial0/1
      -----------------------------------------------------------
      Legend: S=Static, O=OSPF, R=RIP
      (OSPF의 AD 110이 RIP의 120보다 작으므로 OSPF 경로가 선택됨)
```

**핵심 알고리즘 및 코드**

```python
# 의사코드(Pseudo-code): 라우터의 경로 선정 알고리즘

def select_best_route(destination_ip):
    candidates = lookup_all_routes(destination_ip)
    best_route = None

    # 1단계: AD (관리 거리) 필터링
    # AD 값이 가장 낮은 그룹 선택
    lowest_ad = 255
    for route in candidates:
        if route.ad < lowest_ad:
            lowest_ad = route.ad
            best_routes = [route]
        elif route.ad == lowest_ad:
            best_routes.append(route)
    
    # 2단계: Metric (메트릭) 필터링
    # 동일 AD 그룹 내에서 Metric이 가장 낮은 경로 선택
    best_metric = float('inf')
    for route in best_routes:
        if route.metric < best_metric:
            best_metric = route.metric
            best_route = route
            
    # 3단계: 로드 밸런싱 (Load Balancing)
    # 최종 후보군의 Metric이 동일하면 동시에 사용
    final_routes = []
    for route in best_routes:
        if route.metric == best_metric:
            final_routes.append(route)
            
    return final_routes
```

**📢 섹션 요약 비유**
경로 선정 과정은 취업 시장의 서류 전형과 유사합니다. **관리 거리(AD)**는 출신 대학의 등급(명문대 우선 선고)이고, **메트릭(Metric)**은 동일 대학 출신 지원자들 간의 학점 및 경쟁력 비교입니다. 아무리 학점(Metric)이 좋아도, 출신 대학 등급(AD)이 낮으면 서류 통과가 어려울 수 있는 원리와 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

정적 라우팅과 동적 라우팅의 선택은 단순한 기술 구현을 넘어 비즈니스 연속성과 운영 효율성에 직결됩니다.

#### 1. 정량적/구조적 심층 비교

| 비교 항목 | 정적 라우팅 (Static) | 동적 라우팅 (Dynamic) |
|:---|:---|:---|
| **Convergence Time** | **0초** (변경 없음) 또는 무한대(장애 시 복구 불가) | 수백 밀리초(ms) ~ 수십 초 (Protocol 및 Timer 의존) |
| **네트워크 오버헤드** | 없음 (0 Control Traffic) | 주기적인 **Hello**, **LSA (Link State Advertisement)**, Update 패킷 발생 |
| **관리 복잡도 (OpEx)** | 노드 증가 시 제곱으로 관리 난이도 상승 | 초기 설정 복잡하나, 이후 자동化管理로 부하 감소 |
| **보안** | 라우터 내부 설정만으로 경로 고정 (내부 정보 노출 안 함) | **Routing Protocol Attack** 위험 (Authentication 필수) |
| **Load Balancing** | 수동으로 여러 경로 설정 가능 (Per-Destination) | **ECMP (Equal-Cost Multi-Path)** 자동 지원 |

#### 2. 타 영역과의 융합 시너지 (OS & Security)

-   **OS (Operating System)와의 관계**: 리눅스 서버의 **Kernel Routing Table**도 동일한 원리를 사용합니다. 리눅스에서 `ip route add` 명령어로 추가하는 경로는 정적 라우팅에 해당하며, `Quagga`나 `FRR` 같은 라우팅 데몬을 돌리면 리눅스가 OSPF/BGP 라우터처럼 동작하여 동적 라우팅을 수행합니다.
-   **Security (보안)와의 관계**: 
    -   **정적 라우팅**은 **백홀(Backhole)** 방지나 특정 보안 구간(Security Zone) 간의 격리된 통신에 사용됩니다. 공유기 설정의 "Static Route"는 보통 이 기능입니다.
    -   **동적 라우팅**은 **RP (Route Poisoning)** 등의 공격에 취약할 수 있으므로, 최신 보안 표준인 **BGPsec**이나 **OSPF Authentication(MD5/SHA)** 기술이 융합되어 무결성을 검증합니다.

**비교 다이어그램: 메트릭 결정 방식의 차이**

```ascii
[RIP vs OSPF Metric Calculation]

Target: 100Mbps Link

1. RIP (Hop Count Based)
   └─ Value: 1 (건너뛰는 라우터 1대)
   └─ 문제점: 56Kbps 링크도 1이면 동일 취급 (성능 무시)

2. OSPF (Cost Based)
   └─ Value: 10^8 / 100,000,000 = 1
   └─ 문제점 해결: 56Kbps(56,000bps)면 Cost = 1785 (매우 비쌈)
   └─ 결과: 항상 대역폭이 넓은 길을 선호함
```

**📢 섹션 요약 비유**
집을 지을 때, **정적 라우팅**은 내려놓은 벽돌을 사람이 일일이 옮겨 쌓는 방식이며, **동적 라우팅**은 자동화된 로봇 팔이 설계도면을 보고 스스로 벽을 쌓는 방식입니다. 정적 방식은 간단한 담장을 쌓을 때 좋지만, 고층 빌딩(대규모 망)을 짓려면 동적 장비의 유연성이 필수적입니다. **메트릭**은 이 로봇 팔이 '벽돌의 가격'과 '무게'를 따져 가장 효율적인 자재를 선택하는 과정과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 시나리오 및 의사결정

**시나리오