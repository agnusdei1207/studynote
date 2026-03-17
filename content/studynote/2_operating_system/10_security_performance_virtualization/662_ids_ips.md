+++
title = "662. 침입 탐지/방지 시스템 (IDS/IPS)"
date = "2026-03-16"
weight = 662
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "IDS", "IPS", "침입 탐지", "침입 방지", "Snort", "Suricata"]
+++

# 662. 침입 탐지/방지 시스템 (IDS/IPS)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IDS (Intrusion Detection System, 침입 탐지 시스템)는 네트워크나 시스템의 흐름을 모니터링하여 공격을 **탐지(Detection)**하고 알리는 수동형 보안 관제 시스템이며, IPS (Intrusion Prevention System, 침입 방지 시스템)는 이를 넘어 네트워크 경로상에 직접 개입하여 **실시간 차단(Prevention)**하는 능동형 보안 솔루션입니다.
> 2. **가치**: 기존 방화벽(Firewall)이 L3/L4(포트/프로토콜) 수준의 접근 제어에 불과한 반면, IDS/IPS는 **L7(계층) 페이로드 분석**을 통해 SQL Injection, XSS(Cross-Site Scripting)와 같은 애플리케이션 레벨 공격 패턴을 식별하여 방어선의 깊이(Depth in Defense)를 획기적으로 확보합니다.
> 3. **융합**: 단순한 패턴 매칭(Signature-based)을 넘어 AI 기반의 행위 분석(Anomaly-based)과 결합하고, OS(Operating System)의 시스템 콜 감사(Auditing) 및 네트워크 패킷 캡처(Libpcap) 기술이 융합된 **SOC (Security Operation Center, 보안 관제 센터)**의 핵심 척추 역할을 합니다.

+++

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 정의**
IDS/IPS는 사이버 공격의 탐지와 대응을 위한 보안 시스템입니다.
- **IDS (Intrusion Detection System)**: 네트워크 트래픽이나 시스템 로그를 감시하여 비정상적인 활동이나 공격 패턴을 식별하고 관리자에게 알림(Alerting)을 발생시키는 **수동적(Passive)** 장치입니다.
- **IPS (Intrusion Prevention System)**: IDS의 기능에 실시간 차단(Dropping/RST) 기능을 더하여, 공격 트래픽이 타겟 시스템에 도달하기 전에 네트워크 경로 상에서 직접 차단하는 **능동적(Active)** 장치입니다.

**2. 기술적 배경 및 철학**
1998년 Martin Roesch가 개발한 오픈 소스 **Snort**의 등장은 네트워크 보안 패러다임을 정적인 패킷 필터링에서 동적인 콘텐츠 분석으로 전환시켰습니다. 초기의 방화벽이 "출입문의 개폐 여부"만 관리했다면, IDS/IPS는 "출입문을 통과하는 사람의 의도와 행동(페이로드)"을 분석하는 단계로 진화했습니다. 최근에는 클라우드 및 가상화 환경의 확산으로 인해 가상 스위치(Virtual Switch) 내부에 탑재되는 가속화된 가상 IPS(vIPS) 기술이 중요해지고 있습니다.

**3. 주요 분류**
IDS/IPS는 배치 위치에 따라 **NIDS (Network IDS/IPS)**와 **HIDS (Host IDS/IPS)**로 나뉩니다.
- **NIDS**: 네트워크 트래픽을 스니핑(Sniffing)하여 공격을 탐지합니다.
- **HIDS**: 서버의 OS(운영체제) 로그, 파일 시스템 무결성, 시스템 콜(System Call)을 감시합니다.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    [ 보안 아키텍처의 진화 ]                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [과거: 포트 기반 방화벽]          [현재: IDS/IPS]               │
│  ┌──────┐      ┌──────┐           ┌──────┐      ┌──────┐       │
│  │User  │─────▶│FW    │─────▶    │User  │─────▶│IPS   │─────▶│Server│
│  └──────┘ Port └──────┘ Permit  └──────┘ Data └──────┘ Block │
│                 (3/4 Layer)                    (7 Layer)       │
│                                                                 │
│  ※ "방화벽은 문지원, IDS는 경비원, IPS는 격투기 경비원"          │
└─────────────────────────────────────────────────────────────────┘
```
*도해 1: 보안 레이어의 진화*
(1) 과거 방화벽은 포트(문)의 열림/닫힘만 제어.
(2) IDS/IPS는 트래픽 내용물(데이터)을 깊이 분석(Deep Packet Inspection)하여 악의적 의도를 파악.
(3) IPS는 탐지와 동시에 연결을 강제 종료(RST Packet)하여 위협을 사전 차단.

**📢 섹션 요약 비유**
> "IDS는 경찰서에 신고하는 CCTV 감시센터이고, IPS는 현장에서 범인을 직접 제압하는 체포술이 훈련된 현장 경찰관과 같습니다."

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 구성 요소 및 상세 동작**
IPS는 단순한 소프트웨어가 아니라 패킷 처리를 위한 고도의 파이프라인 아키텍처를 가집니다. 특히 고속 네트워크(10Gbps 이상)에서 성능 저하(Uncut)를 막기 위해 하드웨어 가속기나 커널 바이패스 기술(XDP, DPDK 등)을 사용합니다.

| 구성 요소 (Module) | 역할 (Role) | 내부 동작 (Internal Action) | 주요 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Packet Capture** | 패킷 수집 | NIC(Network Interface Card)에서 패킷을 복사하여 유저 영역으로 전달 | Libpcap, PF_RING, DPDK | 손님 입구 수위 |
| **Decoder** | 프로토콜 해석 | 이더넷 ~ 애플리케이션 계층까지 패킷 구조를 파싱 | Ethernet, IP, TCP, HTTP | 우편물 분류 직원 |
| **Detection Engine** | 규칙 검사 | 패킷 페이로드와 시그니처(Signature) 규칙을 바이트 단위로 매칭 | Aho-Corasick, BMH | X-Ray 탐지기 |
| **Preprocessor** | 전처리 | 패킷 조각 재조합(Defrag), 스트림 재조합(Stream), URL 디코딩 수행 | Stream5, HTTP Decode | 퍼즐 맞추기 |
| **Action Module** | 조치 수행 | 탐지 시 알림 로그 생성 또는 연결 강제 종료(RST) 패킷 전송 | IP Tables, API Call | 제지/보호 조치 |

**2. 탐지 메커니즘 (Detection Mechanism)**

```text
┌──────────────────────────────────────────────────────────────────┐
│                    [ IPS 탐지 및 차단 파이프라인 ]                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Incoming Packet    ┌──────────────┐                           │
│   ────────────────▶ │  Preprocessor│ (Normalization/Defrag)   │
│                     └───────┬──────┘                           │
│                             ▼                                   │
│                     ┌──────────────┐                            │
│                     │   Decoder    │ (Protocol Parsing)         │
│                     └───────┬──────┘                            │
│                             ▼                                   │
│                     ┌──────────────┐                            │
│   ┌───────────────▶│   Detection  │◀──── Rule Set (Snort/Suri) │
│   │   Analysis     │    Engine    │                            │
│   │                 └───────┬──────┘                            │
│   │                         │                                   │
│   │                         ▼                                   │
│   │              [Match Found?]                                 │
│   │                 /      \                                    │
│   │               No        Yes                                 │
│   │               │          │                                  │
│   │               ▼          ▼                                  │
│   │            [Allow]   [Action]                               │
│   │                      (Alert Log & Drop/RST)                 │
│   │                                                           │
│   ▼                                                           │
│ Target Server                                               │
└──────────────────────────────────────────────────────────────────┘
```
*도해 2: IPS의 내부 처리 흐름도*
(1) **수집 및 정규화**: 패킷을 받아들이고 조각난 패킷(Fragment)을 원래의 순서대로 재조립(Reassembly).
(2) **디코딩**: HTTP GET 요청 내의 URL 인코딩된 문자(%20 등)를 디코딩하여 원문 복원.
(3) **엔진 매칭**: 복원된 페이로드와 공격 패턴 데이터베이스를 비교.
(4) **액션**: 규칙 위반 시 패킷을 폐기(Drop)하고 TCP 세션을 리셋(RST) 시킴.

**3. 핵심 알고리즘 및 탐지 논리**
탐지 엔진의 성능은 문자열 검색 알고리즘에 의존합니다. 수천 개의 규칙을 실시간으로 검색하기 위해 **Aho-Corasick Algorithm (아호-코라식 알고리즘)**이나 **Boyer-Moore-Horspool** 등이 사용됩니다.

```python
# [의사코드: Snort 규칙 해석 및 매칭 로직]
# Snort Rule 구조: action protocol src_ip src_port -> dst_ip dst_port (options)

def process_packet(packet):
    # 1. 프로토콜 및 헤더 검증
    if packet.protocol != TCP or packet.dst_port != 80:
        return ALLOW
    
    # 2. Preprocessing (Stream Reassembly)
    payload = reassemble_stream(packet)
    
    # 3. Rule Engine Matching
    for rule in rule_set:
        # 예: alert tcp any any -> any 80 (content:"union select"; msg:"SQL Injection";)
        if rule.matches(payload):
            # 4. Action
            if rule.action == "alert":
                log_alert(rule.msg, packet)
            elif rule.action == "drop": # IPS 모드
                drop_packet(packet)
                send_tcp_reset(packet)
                return BLOCK
    
    return ALLOW
```

**📢 섹션 요약 비유**
> "공항 보검(X-Ray)기가 테러리스트의 흉기 패턴을 찾아내는 것처럼, IPS는 수많은 네트워크 패킷(짐)이라는 데이터를 압축 해제하고 정렬하여, 그 안에 숨겨진 해킹 코드라는 흉기를 찾아냅니다."

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. NIDS vs HIDS: 구조적 심층 분석**

| 비교 항목 | NIDS (Network IDS/IPS) | HIDS (Host IDS/IPS) |
|:---|:---|:---|
| **배치 위치** | 네트워크 경로(Aggregation Point) | 개별 서버/엔드포인트 내부 |
| **감시 대상** | 네트워크 패킷 헤더 및 페이로드 | 시스템 콜, 로그, 파일 무결성, 레지스트리 |
| **융합 포인트** | 네트워크 트래픽 분석, 암호화 복호 장비와 연계 | OS 커널, 안티바이러스(AV)와 연계 |
| **장점** | 설치가 쉽고 하나의 장비로 전체 감시 가능 | 암호화된 트래픽의 종단점 복호화 분석 가능, 부하 분산됨 |
| **단점** | HTTPS 등 암호화 트래픽 내부 확인 어려움, 고속 처리 부담 | 각 호스트마다 설치 필요, 리소스 점유 |
| **주요 도구** | Snort, Suricata, Cisco Firepower | OSSEC, Wazuh, CrowdStrike Falcon |

**2. 탐지 기법 비교: Signature vs Anomaly**

| 구분 | 시그니처 기반 (Signature-based) | 이상 탐지 기반 (Anomaly-based) |
|:---|:---|:---|
| **메커니즘** | 알려진 공격 패턴(DB)과 매칭 | 정상 기준선(Baseline) 대비 편차(Deviation) 측정 |
| **기술** | 패턴 매칭, 정규표현식 (Regex) | 통계적 분석, 기계학습(Machine Learning), AI |
| **탐지 가능** | 알려진 공격(True Positive 높음) | 제로데이(Zero-day) 공격, 변종 공격 |
| **오탐(False Positive)** | 낮음 (정확함) | 높음 (정상이어도 의심함) |
| **융합 관점** | 정확한 위협 분석을 위해 Rule 업데이트 필수 | AI/Big Data 기술과 결합하여 자율 방어 체계 구축 |

```text
┌────────────────────────────────────────────────────────────────┐
│                    [ 탐지 기법의 상호 보완 ]                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Signature]           [Anomaly]                               │
│   ┌───────┐              ┌───────┐                            │
│   │Rules  │              │AI/ML  │                            │
│   │DB     │              │Model  │                            │
│   └───┬───┘              └───┬───┘                            │
│       │                      │                                 │
│       ▼                      ▼                                 │
│   [Known Attack]         [Unknown Behavior]                   │
│       │                      │                                 │
│       └──────────┬───────────┘                                 │
│                  ▼                                             │
│            ┌──────────────┐                                    │
│            │ Decision &   │  (Hybrid Approach)                 │
│            │  Response    │                                    │
│            └──────────────┘                                    │
└────────────────────────────────────────────────────────────────┘
```
*도해 3: 하이브리드 탐지 전략*
(1) 기존 공격은 규칙 기반으로 빠르고 정확하게 차단.
(2) 알려지지 않은 공격은 행위 패턴 분석을 통해 탐지.
(3) 두 기술의 결합으로 탐지률(Maximize Detection)을 높이고 오탐(Minimize FP)을 줄임.

**📢 섹션 요약 비유**
> "시그니처 탐지는 '수배자 명단'을 가지고 범인을 찾는 것이고, 이상 탐지는 '평소 행동이 이상한 사람'을 관찰하여 범죄를 예측하는 프로파일링과 같습니다. 현대 보안은 이 두 가지를 조합하여 마련한 방어망입니다."

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 배치 전략 (Placement Strategy)**
IPS를 배치할 때는 성능(Performance)과 보안(Security)의 트레이드오�