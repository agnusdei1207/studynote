+++
title = "660. 침입 탐지 시스템 (IDS/IPS)"
date = "2026-03-16"
weight = 660
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "IDS", "IPS", "침입 탐지", "Intrusion Detection", "Snort", "Suricata"]
+++

# 침입 탐지 시스템 (IDS/IPS)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IDS/IPS는 **네트워크 및 시스템의 트래픽을 실시간 모니터링**하여 악의적인 행위를 식별하고, **IPS(Intrusion Prevention System)**의 경우 패킷을 직접 차단하여 2차 피해를 방지하는 보안 아키텍처의 핵심 요소이다.
> 2. **가치**: "방화벽의 한계 극복"을 통해 **애플리케이션 계층(Layer 7)** 공격 탐지와 내부 신뢰 구간(Internal Network)의 남용 감시를 가능하게 하며, **0-Day 공격** 대응을 위한 행위 기반 분석(Anomaly Detection)으로 보안 격차를 해소한다.
> 3. **융합**: **NIDS(Network IDS)**, **HIDS(Host IDS)**, **NGIPS(Next-Generation IPS)**로 진화하며 **SIEM(Security Information and Event Management)** 및 **SOAR(Security Orchestration, Automation and Response)**과 연동하여 자화상 통합 관제 체계를 구축한다.

+++

### Ⅰ. 개요 (Context & Background)

**IDS (Intrusion Detection System)**와 **IPS (Intrusion Prevention System)**는 사이버 공격으로부터 정보 자산을 보호하기 위한 방어 체계로, 존 앤더슨(James P. Anderson)의 1980년 보고서에서 그 이론적 기반이 마련되었다. 기존의 방화벽이 **IP 주소**나 **포트(Port)** 기반의 접근 제어(Access Control)에 집중했다면, IDS/IPS는 패킷의 **페이로드(Payload)**와 세션 행위를 심층 분석(Deep Packet Inspection)하여 공격의 의도를 파악한다는 점에서 차별화된다. 특히 최근에는 단순 탐지를 넘어 실시간 차단 및 위협 인텔리전스(Threat Intelligence) 기반의 대응이 필수적이다.

#### 💡 비유: '경비실의 모니터링 센터와 현장 요원'
IDS는 **"훔친 물건이나 낯선 행동을 찾기 위해 CCTV를 감시하는 모니터링 요원"**과 같아서, 침입 사실을 알리고 기록을 남기지만 직접 제지하지는 못한다. 반면 IPS는 **"CCTV 화면을 보며 침입자를 목격하는 즉시 현장으로 뛰어나가 제압하는 특수 경비원"**과 같아서, 공격이 성공하기 전에 물리적으로 막아선다.

#### 등장 배경
1.  **기존 방화벽의 한계 (Stateful Inspection의 부족)**: 80~90년대 방화벽은 세션 연결 상태만 관리할 뿐, HTTP GET 요청 내에 담긴 **SQLi (SQL Injection)** 구문이나 악성 스크립트를 식별하지 못했다.
2.  **내부자 위협 및 복잡한 공격 등장**: 외부의 공격뿐만 아니라 이미 내부망에 침투한 공격자나 내부 사용자의 악의적 행위를 탐지할 필요성이 대두되었다.
3.  **실시간 자동화 대응의 필요성**: 사람이 로그를 확인하고 대응하기에는 공격 속도가 너무 빨라졌으며, 이를 초 단위로 차단하는 **Inline 방식**의 IPS가 도입되었다.

#### 📢 섹션 요약 비유
방화벽이 "출입구의 키카드"라면, IDS/IPS는 건물 내부의 "이상 행동을 감지하는 지능형 CCTV"와 같아서, 단순히 통과 여부를 따지는 것을 넘어 그 사람이 무엇을 가지고 왔는지, 어디를 서성이는지까지 실시간으로 분석한다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

IDS/IPS는 크게 **NIDS (Network-based IDS/IPS)**, **HIDS (Host-based IDS/IPS)**, 그리고 혼합형으로 나뉜다. NIDS는 네트워크 트래픽을 감시하고, HIDS는 서버의 로그 파일, 시스템 호출, 파일 무결성을 감시한다.

#### 1. 구성 요소 및 배치 모드
| 모듈 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 | 비유 (Analogy) |
|:---:|:---|:---|:---:|:---|
| **Sensor (센서)** | 트래픽 수집 및 분석 엔진 | NIC(Network Interface Card)를 **Promiscuous Mode**로 설정하여 모든 패킷 캡처 | libpcap, WinPcap | 경비원의 눈과 귀 |
| **Engine (엔진)** | 탐지 로직 처리 | **Signature Matching**(정적) 및 **Profile Learning**(동적) 수행 | Regex, State Machine | 판단하는 두뇌 |
| **Console (콘솔)** | 관리 및 로그 시각화 | 이벤트 수집, Correlation(상관분석), 정책 배포 | TLS/SSL, API | 관리실 대시보드 |
| **Management (DB)** | 위협 정보 저장 | Raw Log, Alert, IP Reputaion 데이터 저장 | SQL, NoSQL | 사건 기록부 |
| **Blocker (차단기)** | IPS의 능동 차단 | **Inline** 모드 시 패킷 드롭(TCP Reset 전송) 명령 | Inline, Tap Out | 물리적 방벽창 |

#### 2. 배치 아키텍처: TAP vs Inline Mode
아래는 NIDS가 네트워크에 연결되는 두 가지 핵심적인 방식을 도식화한 것이다.

```text
      [A. IDS (Promiscuous/TAP Mode - Monitoring Only)]
      
  인터넷
    │
    ▼
┌───────┐      Mirror/Span Port(TAP)      ┌───────────────────────┐
│ 라우터 ├──────────────────────────────────▶│  IDS Sensor (Snort)   │
└───────┘                                     │ (Read-Only Traffic)   │
      │                                       └───────────────────────┘
      ▼                                                │ (Alert Only)
  내부망 ◀──────────────────────────────────────────────┘

      [B. IPS (Inline Mode - Active Blocking)]
      
  인터넷
    │
    ▼
┌───────┐      Inline (Physical Wire)        ┌───────────────────────┐
│ 라우터 ├───────────────────────┬──────────▶│   IPS Engine (Suricata)│
└───────┘                       │           │ (Inspection & Filter) │
                                │           └───────────────────────┘
                                │                    │
      (Clean Traffic) ◀────────┴────────────────────┘
            │
            ▼
         내부망
```
**다이어그램 해설**:
- **IDS Mode (A)**: 스위치의 **Span Port(Mirror Port)**를 통해 패킷 사본을 전달받는다. 트래픽 흐름을 방해하지 않으나(Zero Latency), 공격을 탐지해도 직접 차단할 수 없고 **TCP Reset** 패킷을 보내 세션을 끊는 간접 차단만 가능하다.
- **IPS Mode (B)**: 네트워크 경로(L2/L3 Bridge) 사이에 물리적 또는 논리적으로 위치한다. 모든 트래픽이 IPS를 통과하므로, 악성 패킷이 발견되면 **Drop(폐기)**하거나 **Replace(수정)**하여 내부망으로 들어가지 못하게 막는다. 대신 **장애 지점(Fail-Open/Close)**이 될 수 있어 고가용성 설계가 필수다.

#### 3. 심층 탐지 동작 원리 (Detection Methodology)
탐지 로직은 크게 **Misuse Detection(오용 탐지/시그니처)**과 **Anomaly Detection(이상 탐지)**로 나뉜다.

1.  **Misuse Detection (Signature-based)**: 알려진 공격 패턴(시그니처)과 일치하는지 확인.
    -   *장점*: 낮은 **False Positive(오탐)**, 빠른 처리 속도.
    -   *단점*: 0-Day 공격, 변형 공격 탐지 불가.
    -   *알고리즘*: **Boyer-Moore** 문자열 매칭, **Aho-Corasick** 알고리즘(다중 패턴 매칭).

2.  **Anomaly Detection (Behavior-based)**: 정상적인 프로파일(Baseline)을 학습하여 이탈 시 탐지.
    -   *장점*: 미지의 공격(0-Day) 탐지 가능.
    -   *단점*: 높은 **False Positive(오탐)**, 학습 데이터에 의존적.
    -   *기술*: 통계적 분석, **ML (Machine Learning)**, Heuristic(휴리스틱) 분석.

#### 4. 핵심 알고리즘 및 코드 예시 (Snort Rule)
Snort 규칙은 공격 패턴을 정의하는 DSL(Domain Specific Language)이다.

```text
# [Snort Rule Example]
alert tcp $EXTERNAL_NET any -> $HOME_NET 80 (      # Alert on HTTP traffic
    msg:"WEB-MISC SQL Injection Attempt";          # Log Message
    flow:to_server,established;                    # Flow Tracking
    content:"UNION SELECT";                        # Pattern Matching (Payload)
    nocase;                                        # Case Insensitive
    pcre:"/UNION\s+SELECT/Ui";                     # Perl Compatible Regex
    sid:1000001;                                   # Signature ID
    rev:1;                                         # Revision
    classtype:web-application-attack;              # Classification
)
```

#### 📢 섹션 요약 비유
시그니처 기반 탐지는 "수배자의 얼굴이 담긴 포스터를 들고 하나하나 대조"하는 것이고, 이상 탐지는 "평소 조용한 도서관에서 갑자기 고함을 지르는 사람을 제지"하는 것과 같다. 실무에서는 이 두 가지를 하이브리드로 사용하여 보안의 사각지대를 없앤다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. IDS vs IPS vs Firewall 비교 분석표
| 비교 항목 | 방화벽 (Firewall) | IDS (Intrusion Detection) | IPS (Intrusion Prevention) |
|:---|:---|:---|:---|
| **주 목적** | 접근 제어 (Access Control) | 공격 탐지 및 모니터링 | 공격 탐지 및 차단 (Prevention) |
| **동작 위치** | L3/L4 (Network/Transport) | L2/L3/L7 (Transparent) | L2/L3/L7 (Inline Bridge) |
| **트래픽 처리** | Direct Routing (Pass) | Copy & Inspect (Pass) | Inline Inspect (Filter) |
| **지연 시간(Latency)** | 매우 낮음 (µs) | 낮음 (영향 없음) | 높음 (Inspection Time) |
| **실패 시(Fail)** | Deny All (차단) | Continue (진행) | **Fail-Open/Close** (정책 필요) |
| **주요 기술** | ACL, NAT, State Table | Pattern Match, Anomaly | DPI, Virtual Patching |

#### 2. OSI 7계층 관점에서의 융합 (Network & Security Convergence)
-   **L3/L4 (Firewall)**: "이 집(서버)에 들어와도 되는 사람(IP)인가?"를 확인.
-   **L7 (IDS/IPS)**: "들어온 사람이 가방(Payload)에 폭탄을 들고 왔는가?"를 확인.
    -   **WAF (Web Application Firewall)**는 웹 트래픽(HTTP/HTTPS)에 특화된 IPS의 일종으로 볼 수 있다.
    -   **EDR (Endpoint Detection and Response)**는 PC/서버(OS 레벨)에서의 HIDS 발전 형태이다.
-   **상관관계**: 방화벽이 트래픽을 대폭 줄여주면 IDS/IPS가 분석해야 할 로드가 줄어든다.

#### 📢 섹션 요약 비유
건물 보안 시스템에 비유하면, 방화벽은 "출입구의 키카드 리더기"이고, IPS는 "금속 탐지기와 엑스레이"이며, IDS는 "주변의 순찰 차량"과 같다. 이 셋을 통합하지 않으면 건물의 안전을 보장할 수 없다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 실무 배치 시나리오 (Deployment Topology)
실제 기업 환경에서는 **Defense in Depth(심층 방어)** 전략에 따라 여러 지점에 배치한다.

```text
      [Internet]
         │
         ▼
  ┌───────────────────┐  (1) Perimeter: 대외 공격 방어
  │  Outer Firewall   │────────────────────┐
  └───────────────────┘                     │
         ▼                                  │
  ┌───────────────────┐ (2) Edge IPS:       │   DDoS, SQLi 방어
  │     Edge IPS      │─────[Block]─────────┘
  └───────────────────┘                     │
         ▼                                  │
         │                     ┌───────────────────────────┐
  (DMZ)  │                     │      Core Switch          │
  ───────┼─────────────────────┤                           │
         │                     └───────────────────────────┘
         ▼                                 │
  ┌───────────────────┐                   │
  │  Internal Network │                   │
  └───────────────────┘                   │
         ▲                                 ▼
         │                     ┌───────────────────────────┐
         │                     │   Internal IDS Sensor     │ (3) Internal: 내자 위협
         └─────────────────────┤     (Mirror Port)         │   Lateral Movement 감시
                               └───────────────────────────┘
```

**시나리오 A**: 해커가 방화벽(80포트 오픈)을 통과하여 SQLi 공격을 시도함 -> **Edge IPS**가 패킷 페이로드 분석 후 DROP.
**시나리오 B**: 내부 PC가 악성코드에 감염되어 RDP(3389) 포트로 무작위 대입 공격(Rainbow Table) 시도 -> **Internal IDS**가 세션 당 접속 시도 횟수 이상을 감지하고 경고.

#### 2. 도입 체크리스트 (Checklist)
-   **기술적 검토**
    -   [ ] 처리 용량(Throughput): **Gbps 단위**의 네트워크 대역폭을 처리할 수 있는가?
    -   [ ] 지연 시간(Latency): Inline IPS가 실시간 트래픽(UDP/RTP 등)에 병목을 초래하지 않는가?
    -   [ ] Tuning(튜닝): 오탐(False Positive)률을 낮추기 위한 룰셋 커스터마이징이 가능한가?
-   **운영/보안적 검토**
    -   [ ] High Availability (HA): 이중화 구성 시 **State Synchronization(상태 동기화)**가 지원되는가? (Active-Standby 시 세션 끊김 방지)
    -   [ ] Log