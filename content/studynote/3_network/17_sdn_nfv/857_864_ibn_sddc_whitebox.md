+++
title = "857-864. 인텐트 기반 네트워킹과 SDDC (IBN, SDDC)"
date = "2026-03-14"
[extra]
category = "SDN & NFV"
id = 857
+++

# 857-864. 인텐트 기반 네트워킹과 SDDC (IBN, SDDC)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네트워크 관리의 패러다임을 CLI(Command Line Interface) 기반의 '명령형(How)'에서 비즈니스 목적 중심의 '선언형(What)'으로 전환하는 **IBN (Intent-Based Networking)**과 이를 데이터센터 전체 자원으로 확장한 **SDDC (Software-Defined Data Center)** 아키텍처.
> 2. **가치**: 설정 오류(Configuration Error)로 인한 장애를 90% 이상 감소시키고, 정책 배포 시간을 주/월 단위에서 분/초 단위로 단축하여 **TTM (Time To Market)**을 획기적으로 개선함.
> 3. **융합**: AI/ML (Artificial Intelligence/Machine Learning) 기반의 자가 최적화, 가상화(Virtualization), 클라우드 네이티브(Cloud Native) 아키텍처와의 결합을 통해 운영의 자동화 및 민첩성을 극대화함.

+++

### Ⅰ. 개요 (Context & Background)

**1. 개념 정의**
*   **IBN (Intent-Based Networking)**은 네트워크 관리자가 복잡한 명령어를 일일이 입력하는 대신, "본사와 지사 간 보안 터널 구성"과 같은 비즈니스 의도(Intent)를 입력하면, 시스템이 이를 자동으로 번역(Translation), 실행(Activation), 검증(Assurance)하는 차세대 네트워크 관리 철학입니다.
*   **SDDC (Software-Defined Data Center)**는 데이터센터의 모든 인프라(서버, 스토리지, 네트워크, 보안)를 가상화 및 추상화하여 소프트웨어적으로 제어하고 관리하는 컴퓨팅 환경을 의미합니다. 이는 **SDN (Software-Defined Networking)**의 철학을 데이터센터 전체로 확장한 개념입니다.

**2. 등장 배경: CLI 한계와 자동화의 요구**
기존의 네트워크 운영은 관리자가 각 장비에 접속하여 CLI 명령어를 직접 입력하는 방식이었습니다. 그러나 클라우드 환경으로의 전환 및 트래픽의 폭발적 증가로 인해 다음과 같은 문제가 발생했습니다.
*   **① 인적 실산(Human Error)**: 수천 대의 장비에 수만 줄의 설정을 입력하는 과정에서 오타나 정책 불일치가 발생하여 주요 장애의 원인이 됨.
*   **② 복잡성 관리 불가**: Microservices 아키텍처로 인해 네트워크 토폴로지가 동적으로 변화하므로, 정적인 설정으로는 대응 불가능.
*   **③ 속도 저하**: 비즈니스 요구사항이 변경되었을 때, 실제 인프라에 반영되기까지 수주가 걸리는 현상.

이를 해결하기 위해 **'소프트웨어가 인프라를 제어(Software Defined)'**하고 **'의도(Intent)가 자동화된 시스템을 제어'**하는 패러다임이 등장했습니다.

**3. 진화 과정**

```ascii
[시대별 네트워크 관리 진화 과정]

1. CLI/SNMP 시대:           2. SDN 시대:                3. IBN 시대:
+-----------+              +-----------+               +-----------+
| Manual    |              | Central   |               | AI & Auto |
| Config    |  ---->       | Controller|  ---->        | Brain     |
+-----------+              +-----------+               +-----------+
      |                          |                          |
   "How"                       "How"                       "What"
(장비별 명령어)             (중앙 집중 제어)           (비즈니스 의도)
```
*   **CLI**: 장비마다 일일이 접속하여 '어떻게(How)' 설정할지 명령.
*   **SDN (Software-Defined Networking)**: 컨트롤러를 통해 중앙에서 제어하지만 여전히 구체적인 흐름(Flow)을 지정해야 함.
*   **IBN (Intent-Based Networking)**: 시스템에 '무엇(What)'을 원하는지만 지정하면 시스템이 최적 경로와 설정을 스스로 계산.

> **📢 섹션 요약 비유**: 네트워크 관리의 진화는 **수동 기어 차량(CLI)에서 자동 변속기(SDN)를 거쳐, 목적지만 입력하면 스스로 경로를 찾고 운전까지 하는 자율 주행 자동차(IBN)로 발전하는 과정**과 같습니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. IBN의 핵심 구성 요소**

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 주요 프로토콜/기술 |
| :--- | :--- | :--- | :--- |
| **Intent (의도)** | 관리자의 비즈니스 요구사항 입력 | 자연어 처리 or UI를 통해 "A그룹은 B그룹과 통신 금지" 등 입력 | Natural Language, API |
| **Translation (변환)** | 의도를 네트워크 정책으로 변환 | 입력된 의도를 분석하여 장비별 설정(Config)으로 자동 생성 | YANG Model, NETCONF |
| **Activation (실행)** | 실제 장비에 설정 적용 | 컨트롤러가 에이전트를 통해 장비에 설정을 Push (Northbound ↔ Southbound) | OpenFlow, gNMI, REST |
| **Assurance (보증)** | 상태 모니터링 및 자가 치유 | Real-time Telemetry 데이터로 의도와 실제 상태 비교, 드리프트(Drift) 발생 시 자동 복구 | gRPC, Streaming Telemetry |

**2. IBN의 폐루프(Closed-Loop) 자동화 아키텍처**

IBN은 단순히 설정을 밀어넣는 것이 아니라, 끊임없이 상태를 확인하고 수정하는 **폐루프(Closed-Loop)** 시스템입니다.

```ascii
      [ IBN Closed-Loop Automation Architecture ]

   +---------------------------------------------------+
   | 1. Intent Definition (What)                       |
   |    "금융 앱 지연 시간 10ms 미만 보장"              |
   +---------------------------|-----------------------+
                               v
   +---------------------------------------------------+
   | 2. Translation & Activation (How)                 |
   |    AI가 최적 경로 계산 -> 정책 생성 -> 장비 배포   | <--+
   +---------------------------|-----------------------+    |
                               v                            |
   +---------------------------------------------------+    |
   | 3. Assurance & Continuous Monitoring (State)      |    |
   |    Real-time Telemetry 수집 (Packet loss, Latency)| ---+
   +---------------------------|-----------------------+
                               |
                 (비교: Intent vs Actual State)
                      |
               v-------+-------v
          [Issue Detected?] --(Yes)--> [Auto-Remediation]
               | (No)
               v
          [Maintain State]
```

*   **① Translation**: 관리자가 입력한 "의도"는 시스템 내부적으로 **YANG (Yet Another Next Generation)** 데이터 모델을 통해 기계가 이해할 수 있는 정책 데이터로 변환됩니다.
*   **② Activation**: 변환된 정책은 **NETCONF (Network Configuration Protocol)**나 **gNMI (gRPC Network Management Interface)**를 사용하여 각 네트워크 장비(Switch, Router)로 전송되어 설정됩니다.
*   **③ Assurance**: 적용 후 **구독(Subscription)** 기반의 모델로 초당 수천 개의 Telemetry 데이터를 수집합니다. 의도(Intent)와 다르게 동작한다면(예: 링크 장애로 인해 지연 시간 증가), 시스템이 즉시 알고리즘을 통해 대체 경로를 재계산하고 장비에 재배포하여 **자가 치유(Self-Healing)**를 수행합니다.

**3. SDDC 통합 아키텍처**

SDDC는 **SDC (Software-Defined Compute)**, **SDS (Software-Defined Storage)**, **SDN (Software-Defined Networking)**이 하나의 플랫폼에서 통합 관리되는 구조입니다.

```ascii
           [ SDDC Logical Architecture ]

+------------------------------------------------------------------+
|                    SDDC Management Layer (Orchestration)         |
|  +----------------+  +----------------+  +------------------+   |
|  |   Compute      |  |    Network     |  |     Storage      |   |
|  |   Manager      |  |   Controller   |  |    Controller    |   |
|  +-------+--------+  +--------+-------+  +--------+---------+   |
|          |                     |                   |            |
+----------+---------------------+-------------------+------------+
           |                     |                   |
           v                     v                   v
+----------------+    +-------------------+    +------------------+
|  SDC (Compute) |    |  SDN (Network)    |    |  SDS (Storage)   |
|  Hypervisor    |    |  Overlay Network |    |  vSAN / Pool     |
|  (VM, K8s Pod) |    |  (VXLAN, NVGRE)  |    |  (Object, Block) |
+-------+--------+    +---------+---------+    +--------+---------+
        |                         |                       |
        +-------------------------+-----------------------+
                                   |
                        [ Physical Infrastructure ]
                        (x86 Server, Whitebox Switch, JBOD)
```

**4. 핵심 기술 상세: Telemetry vs SNMP**
IBN과 SDDC의 실시간 모니터링은 기존의 **SNMP (Simple Network Management Protocol)** 방식에서 **gRPC (Google Remote Procedure Call)** 기반의 **Telemetry**로 전환되었습니다.

*   **SNMP**: 폴링(Polling) 방식, 5분~1시간 주기. 데이터 부족함, 느림.
*   **Telemetry**: 푸시(Push) 방식, 초당 수회(Sub-second). 상세한 데이터(CPU, Memory, Queue depth)를 실시간 전송.

> **📢 섹션 요약 비유**: IBN과 SDDC의 관계는 **'빌딩의 자동화 시스템'**과 같습니다. 관리자(IBN 사용자)는 "실내 온도를 24도로 유지해라"(Intent)라고만 입력합니다. 그러면 스마트 컨트롤러(IBN Engine)가 에어컨, 창문, 블라인드(SDN/SDC/SDS 자원)를 자동으로 제어하고, 센서(Telemetry)를 통해 실시간으로 온도를 확인하며 이탈 시 자동 조정합니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교: 전통적 네트워킹 vs IBN/SDDC**

| 비교 항목 | 전통적 네트워킹 (Legacy) | IBN & SDDC (Next-Gen) |
| :--- | :--- | :--- |
| **관리 방식** | **Box-by-Box**: 각 장비별 개별 CLI 설정 | **Fabric-based**: 전체망을 하나의 논리적 스위치로 관리 |
| **설정 주체** | 네트워크 엔지니어 (수동) | 오케스트레이션 소프트웨어 (자동) |
| **프로토콜** | CLI, SNMP (Polling) | NETCONF, REST API, gRPC (Streaming) |
| **데이터 처리** | **Reactive**: 장애 발생 후 대응 | **Proactive**: 이상 징후를 사전에 예측하고 조치 |
| **추상화 계층** | Low-Level (Interface, VLAN ID) | High-Level (Application, Tenant, Policy) |

**2. 기술 융합 시너지 (Convergence)**

*   **① 네트워크 & 보안 (Security Integration)**
    *   **Zero Trust (제로 트러스트)**: IBN을 통해 사용자의 신원(ID)과 장비 상태를 실시간으로 확인하여, "금융팀 직원이 회사 PC로 접속"이라는 의도(Intent)에 부합할 때만 네트워크 접근을 허용하는 **동적 세그먼테이션(Micro-segmentation)**이 가능해집니다. 이는 방화벽을 뚫고 들어오는 공격을 사전에 차단하는 효과가 있습니다.
*   **② 네트워크 & AI (AIOps)**
    *   **AIOps (Artificial Intelligence for IT Operations)**: 수집된 Telemetry 데이터를 AI 모델에 학습시켜, 장애가 발생하기 전에 트래픽 패턴의 변화를 감지하고 예지 보전(Predictive Maintenance)을 수행합니다. SDDC 환경에서는 VM이 이동하거나 컨테이너가 재시작할 때 네트워크 정책을 자동으로 따라붙게 하여 보안 정책의 누수를 방지합니다.

> **📢 섹션 요약 비유**: 전통적 네트워크는 **'인부들이 삽과 곡괭이로 일일이 벽돌을 쌓는 건축 방식'**이라면, IBN/SDDC는 **'설계도면을 입력하면 로봇 팔들이 정밀하게 협동하여 건물을 짓는 자동화 공장'**과 같습니다. 단순히 속도가 빠른 것이 아니라, 구조적으로 실수가 불가능하도록 시스템이 설계되어 있다는 점이 결정적으로 다릅니다.

+++

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정 (Scenario)**

*   **시나리오 A: 금융권 데이터센터 이전 및 재구축**
    *   **상황**: 레거시 장비가 노후화되어 3-tier 구조에서 Spine-Leaf 구조로 변경해야 하며, 신규 서비스 증설에 따른 유연성이 요구됨.
    *   **의사결정**: IBN 기반의 SDDC 도입을 검토.
    *   **판단 근거**:
        *   장애 복구 시간을 줄이기 위해 상시 Telemetry 모니터링 필수.
        *   수천 대의 서버/스위치 설정 자동화를 위해 Ansible/Terraform(IaC)과 연동 가능한 IBN Controller 선택.
        *   CAPEX(초기 투자 비용)는 높지만, OPEX(운영 비용) 절감 효과가 3년 차부터 발생하는 ROI 분석 필요.

*   **시나리오 B: 공공기관 보안 강화 구축**
    *   **상황**: 내부망 해킹 사고 예방 및 업무별 망 분리(Segmentation) 요구.
    *   **의사결정**: IBN의 Intent("부서 간 통신 차단")를 정책으로 자동화하고, 이를 SDDC의 가상화 방화벽(vFirewall)과 연동.
    *   **판단 근거**: 사람이 수동으로 ACL(Access Control List)을 설정하면 실수로 인한 보안 구멍이 발생할 수 있으므로, '선언적 보안 정책'을 통해 사람의 개입을 배제해야 신뢰성이 확보됨.

**2. 도입 체크리스트 (Checklist)**

| 구분 | 체크 항목 | 설명 |