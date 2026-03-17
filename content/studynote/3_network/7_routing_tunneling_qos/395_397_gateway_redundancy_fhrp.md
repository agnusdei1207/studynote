+++
title = "395-397. 게이트웨이 이중화 프로토콜(FHRP)"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 395
+++

# 395-397. 게이트웨이 이중화 프로토콜(FHRP)

> **핵심 인사이트**
> 1. **본질**: **FHRP (First Hop Redundancy Protocol)**는 단일 실패 지점(SPOF)인 디폴트 게이트웨이의 장애를 극복하기 위해, 물리적으로 분리된 다수의 라우터가 논리적으로 하나의 가상 IP/MAC 주소를 공유하여 고가용성(HA)을 제공하는 Layer 3 기술입니다.
> 2. **가치**: 네트워크 장애 시 **RTO (Recovery Time Objective)**를 '초' 단위로 최소화하여 비즈니스 연속성을 보장하며, **GLBP (Gateway Load Balancing Protocol)**와 같은 기술은 대역폭 효율성까지 극대화합니다.
> 3. **융합**: **L2 스위칭**의 STP(스패닝 트리)와 연계하여 루프 방지 및 경로 최적화를 이루며, **OSPF (Open Shortest Path First)**나 **BGP (Border Gateway Protocol)** 같은 라우팅 프로토콜과 함께 사용하여 엔드투엔드(End-to-End) 가용성 아키텍처를 완성합니다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
**FHRP (First Hop Redundancy Protocol)**는 LAN(Local Area Network) 환경에서 호스트(End-user Device)가 외부 네트워크로 통신하기 위해 거치는 첫 번째 라우터, 즉 디폴트 게이트웨이의 장애에 대비하여 이중화를 구축하는 프로토콜 군을 의미합니다. 일반적으로 PC나 서버는 하나의 디폴트 게이트웨이 IP만 설정할 수 있으므로, 해당 라우터가 다운되면 외부와의 통신이 두절됩니다. 이를 해결하기 위해 물리적인 라우터를 다수 설치하고, 이들이 하나의 가상 IP(Virtual IP)와 가상 MAC(Virtual MAC) 주소를 공유하여 호스트에게는 마치 하나의 라우터인 것처럼 인식시키는 기술입니다.

**💡 비유**
건물에 엘리베이터가 2대 있는 상황에서, 승객(패킷)은 버튼을 누르는 것이지 특정 엘리베이터를 지정하지 않습니다. 내부 시스템(FHRP)이 어느 엘리베이터를 운행할지 결정하고, 한 대가 고장 나면 즉시 다른 대가 운행을 맡아 승객은 멈춤 없이 이동할 수 있게 하는 것과 같습니다.

**등장 배경 및 필요성**
① **기존 한계**: 기존 라우팅 프로토콜(RIP, OSPF 등)은 링크 장애 시 컨버전스(Convergence) 시간이 수십 초 이상 소요되어 실시간 서비스에 치명적입니다.
② **혁신적 패러다임**: 라우팅 테이블 갱신을 기다리는 것이 아니라, 게이트웨이 IP를 미리 다른 백업 장비로 이동(Failover)시키는 방식으로 장애 복구 시간을 1초 이내로 단축했습니다.
③ **비즈니스 요구**: 전자상거래, 금융 트랜잭션 등 24시간 365일 중단 없는 서비스(24/7 Non-stop Service)가 필수가 되면서, 네트워크 계층의 가용성 확보가 핵심 과제로 부상했습니다.

**📢 섹션 요약 비유**
FHRP는 마치 식당의 주방에 **'예비 셰프'**를 항상 대기시켜두는 시스템과 같습니다. 손님(PC)은 누가 요리하는지 모르고 주문만 하지만, 메인 셰프(Active 라우터)가 다치더라도 예비 셜프(Standby 라우터)가 냄맛을 유지하며 즉시 뒤를 이어받아 요리를 계속합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

FHRP의 핵심은 **가상화(Virtualization)**와 **상태 공유(State Sharing)**에 있습니다. 각 프로토콜(HSRP, VRRP, GLBP)마다 결성 방식과 상태 천이(State Transition) 메커니즘은 차이가 존재하나, 기본 토대는 '멀티캠팅(Multicast)'을 통한 헬로(Hello) 메시지 교환입니다.

#### 1. 주요 프로토콜 상세 구성 (HSRP vs VRRP vs GLBP)

| 비교 항목 | **HSRP (Hot Standby Router Protocol)** | **VRRP (Virtual Router Redundancy Protocol)** | **GLBP (Gateway Load Balancing Protocol)** |
| :--- | :--- | :--- | :--- |
| **표준화 기구** | 시스코(Cisco) 전용 (RFC 2281) | **IEEE 표준 (RFC 5798)**, 벤더 무관 | 시스코(Cisco) 전용 |
| **그룹 역할** | **Active** / Standby / Listen | **Master** / Backup | **AVG**(Active Virtual Gateway) / **AVF**(Active Virtual Forwarder) |
| **기본 Hello 타이머** | 3초 (Hold 10초) | 1초 (Skew time 기반) | 3초 (Hold 10초) |
| **가상 MAC 주소** | `0000.0c07.ac{Group ID}` | `0000.5e00.01{Group ID}` | `0007.b400.xx{Group ID}` |
| **Preemption 우선순위** | Default 비활성화 (Manual 설정 필요) | Default 활성화 (Preempt on) | - |
| **부하 분산** | 지원 안 함 (Active only) | 지원 안 함 (Master only) | **지원 (AVF당 개별 MAC 할당)** |

#### 2. FHRP 상태 천이 및 토폴로지 (ASCII 구조 다이어그램)

아래 다이어그램은 **VRRP**를 기반으로 한 대표적인 게이트웨이 이중화 구조입니다.

```ascii
      [ 인터넷 Cloud ]
            | (WAN Link)
            +-------------------------+
            |                         |
    (Physical IP: 1.1.1.1)    (Physical IP: 1.1.1.2)
    [ Router A : MASTER ]     [ Router B : BACKUP ]
    Priority: 100            Priority: 90
      State: UP               State: UP
            |                         |
            +----------+-------------+
                       |
               [ L2 Switch (Access) ]
                       |
        +--------------+--------------+
        |              |              |
    [ Host A ]      [ Host B ]    [ Host C ]
Gateway: 1.1.1.254 (Virtual IP - VIP)
```

**다이어그램 상세 해설**
1.  **VIP (Virtual IP)**: 1.1.1.254는 실제 라우터 인터페이스에 존재하지 않는 가상의 주소이나, A와 B 라우터 모두 이를 소유하고 있다고 응답(ARP Reply)할 수 있습니다.
2.  **라우터 A (Master)**: Priority가 가장 높은(100) 라우터로서, 실제로 1.1.1.254에 대한 패킷을 수신하고 라우팅합니다. 멀티캐스트 주소(224.0.0.18)를 통해 주기적으로 자신의 생존을 알립니다.
3.  **라우터 B (Backup)**: Master가 다운되거나 우선순위가 낮아질 경우, Master_Down_Interval 이후에 VIP를 인수(Takeover)하여 트래픽 경로를 대체합니다.

#### 3. 심층 동작 원리 (VRRP 광고 메커니즘)

**VRRP (Virtual Router Redundancy Protocol)**는 RFC 표준으로서 HSRP보다 빠른 컨버전스와 설정의 편의성을 제공합니다. 동작 과정은 다음과 같습니다.

1.  ** election (선거)**: 라우터들은 Priority(기본값 100)와 IP 주소를 비교하여 가장 높은 값을 가진 라우터를 **Master**로 선출합니다.
2.  **Advertisement (광고)**: Master는 1초(기본) 간격으로 `224.0.0.18` IP 멀티캐스트로 VRRP Advertisement 패킷을 전송합니다. 이 패킷에는 Priority, State, VIP 정보가 포함됩니다.
3.  **Skew Time (보정 시간)**: Master가 광고를 보내지 못할 경우, Backup 라우터는 아래 공식으로 계산된 시간만큼 기다렸다가 상태를 Master로 전환합니다.
    *   **식**: `Master_Down_Interval = (3 * Adver_Interval) + Skew_Time`
    *   `Skew_Time = (256 - Priority) / 256`
    *   *해설*: Priority가 높을수록 Skew Time이 줄어들어 더 빠르게 Master 자리를 차지합니다.

#### 4. GLBP 부하 분산 로직 (AVG/AVF)

**GLBP (Gateway Load Balancing Protocol)**는 단순한 이중화를 넘어 대역폭 활용을 극대화합니다.

*   **AVG (Active Virtual Gateway)**: AVG는 그룹 내에서 VIP에 대한 ARP 요청을 담당하는 '교통 정리 관리자'입니다. 호스트가 게이트웨이 IP를 물어보면(ARP Request), AVG는 각 **AVF (Active Virtual Forwarder)**에 할당된 고유한 가상 MAC 주소를 순차적으로(Hash 혹은 Round-Robin) 응답합니다.
*   **AVF (Active Virtual Forwarder)**: 실제 패킷을 포워딩하는 라우터들입니다. 각 AVF는 서로 다른 가상 MAC(0007.b400.xx01, 0007.b400.xx02...)를 가지므로, 스위치는 여러 라우터로 분산된 트래픽을 로드 밸런싱하게 됩니다.

**핵심 코드 (VRRP 설정 예시 - Cisco Syntax)**
```bash
interface GigabitEthernet0/0
 ip address 1.1.1.1 255.255.255.0
 ! VRRP 그룹 10 설정
 standby 10 ip 1.1.1.254       ! 가상 IP 설정
 standby 10 priority 110       ! 우선순위 (높을수록 유리)
 standby 10 preempt            ! 우선순위가 높으면 복귀 시 권한 찾음
 standby 10 track GigabitEthernet0/1 20 ! 인터페이스 다운 시 우선순위 20 감소
```

**📢 섹션 요약 비유**
**FHRP의 동작**은 마치 **비행기 조종석**과 같습니다. HSRP/VRRP는 **'기장(Pilot)과 부기장(Co-pilot)'** 시스템입니다. 기장이 조종하는 동안 부기장은 대기만 하다가, 기장이 의식을 잃으면 즉시 조종간을 넘겨받습니다(Active-Standby). 반면 **GLBP**는 **'쌍발 비행기(Twin Engine)'**입니다. 두 명의 조종사가 각자의 엔진을 동시에 제어하며 비행 하중을 나누어 맡으므로, 연료 효율(대역폭)과 안정성을 동시에 확보합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교 (정량적·구조적 분석)

| 분석 기준 | HSRP (Cisco Proprietary) | VRRP (IEEE Standard) | GLBP (Cisco Advanced) |
| :--- | :--- | :--- | :--- |
| **권장 사용처** | 시스코 장비만 존재하는 전통적인 데이터센터 | **멀티벤더 환경** (Juniper, Cisco, Linux 등 혼재) | 시스코 환경에서 **대역폭 병목 해소**가 필요한 경우 |
| **부하 분산 방식** | MHSRP(Multiple HSRP)로 그룹을 나누어 수동 구현 (VLAN당 그룹 분리) | MVRP 등으로 수동 구현 | **자동 부하 분산** (AVF에 의한 L2 Load Balancing) |
| **ARP 트래픽** | Master/Active만 VIP에 대해 응답 | Master만 VIP에 대해 응답 | **AVG가 다양한 MAC으로 응답** |
| **케이블/링크 효율** | Standby 라우터는 대기 중이므로 링크 자원 100% 낭비 (Idle) | Backup 라우터는 링크 자원 낭비 | 모든 멤버가 트래픽 처리에 참여하므로 자원 효율 극대화 |
| **컨버전스 속도** | 약 3~10초 (Hello 기반) | 약 1~3초 (Hello 짧고 Skew Time 존재) | HSRP와 유사 |

#### 2. 타 영역 융합 분석 (FHRP + STP & Routing)

**① L2 스위칭(STP)과의 상관관계 및 문제점**
FHRP를 도입할 때 가장 주의해야 할 점은 **STP (Spanning Tree Protocol)**와의 충돌입니다.
*   **문제 상황**: 만약 Active 라우터와 연결된 스위치 포트가 Blocking 상태가 되거나, HSRP Active 상태인 라우터의 인터페이스가 Down되었는데 STP가 Blocking을 해제하는 시간(RSTP/Failover)보다 HSRP가 먼저 전환되려 하면 라우팅 블랙홀이 발생합니다.
*   **솔루션**: `standby track` 명령어를 사용하여 물리 인터페이스의 상태를 추적(Track)해야 합니다. 또한, 라우터 간 연결 링크에 대해서는 STP Portfast나 L3 포트(No Switchport) 사용을 권장하여 FHRP Hello 패킷 지연을 방지해야 합니다.

**② 라우팅 프로토콜(OSPF/BGP)과의 연계**
*   **Inbound Traffic**: 외부에서 내부로 들어오는 트래픽(북향 트래픽)은 FHRP로 제어할 수 없습니다. 이는 **BGP**나 **OSPF**와 같은 라우팅 프로토콜의 경로 비용(Cost)이나 AS-Path 속성에 의해 결정됩니다. 따라서, 내부에서 나갈 때는 Router A가 Active여도, 외부에서 들어올 때는 Router B를 거쳐 들어오는 **비대칭 라우팅(Asymmetric Routing)**이 발생할 수 있으며, 이는 방화벽(Firewall) 세션 동기화 이슈를 유발할 수 있으므로 주의가 필요합니다.

**📢 섹션 요약 비유**
이 관계는 **'도로 교통 체계와 내비게이션'**으로 설명할 수 있습니다. **FHRP**는 차량이 고속도로 진입로(진입램프)로 진입할 때 어떤 톨게이트(라우터)