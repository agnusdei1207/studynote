+++
title = "388-394. QoS(서비스 품질) 보장 기술"
date = "2026-03-14"
[extra]
category = "Routing & QoS"
id = 388
+++

# 388-394. QoS(서비스 품질) 보장 기술

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: QoS (Quality of Service)는 네트워크 자원의 한계를 극복하기 위해 트래픽을 식별(Classification), 마킹(Marking), 큐잉(Queuing)하여 중요한 데이터에 우선권을 부여하는 트래픽 엔지니어링 기술이다.
> 2. **가치**: 지연(Jitter)에 민감한 VoIP (Voice over IP)나 streaming 서비스의 품질을 보장하고, 혼잡한 네트워크에서도 비즈니스 크리티컬 애플리케이션의 가용성을 유지한다.
> 3. **융합**: OSI 7계층 중 L2(L2 MAC Priority), L3(IP ToS/DSCP), L4(Port Number) 계층의 협력과 TCP 혼잡 제어(Flow Control) 메커니즘과 연동하여 종합적인 품질 관리를 수행한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
전통적인 IP 네트워크는 "Best-Effort(최선형 노력)" 모델을 따른다. 이는 모든 패킷을 평등하게 취급하며, 혼잡이 발생하면 선착순으로 처리하거나 임의로 폐기하는 방식이다. 하나의 망에서 음성, 화상, 대용량 파일 전송이 혼재하는 멀티미디어 환경에서 이는 치명적이다. QoS는 이러한 **"데이터 평등주의"**를 깨고, 서비스의 중요도와 민감도에 따라 **"차등 대우(Differential Treatment)"**를 제공하여 네트워크 자원을 통제적으로 할당/관리하는 기술이다. 단순히 대역폭(Bandwidth)을 넓히는 것(Over-provisioning)에는 한계가 있으며, QoS는 통계적 다중화 효율을 극대화하는 비용 효율적인 솔루션이다.

**💡 비유: 고속도로 차선제**
일반 차량과 응급차량이 뒤섞인 고속도로에서, 모든 차량이 한 줄로 서면(베스트 에포트) 응급환자는 위험에 처한다. QoS는 **'버스 전용 차로'**나 **'다이아몬드 차로'**를 도입하여, 급한 것(음성)은 앞서가고 늦어도 되는 것(이메일)은 뒤로 보내는 교통 통제 시스템과 같다.

**등장 배경**
1.  **기존 한계**: 패킷 스위칭 네트워크의 발달과 함께 음성 데이터가 패킷화되면서(ToIP), 패킷 손실 및 지연(Jitter)이 통화 품질을 저해하는 문제 대두.
2.  **혁신적 패러다임**: 단순한 우선순위 큐(Priority Queue)를 넘어, RSVP (Resource ReSerVation Protocol) 같은 신호 체계와 DiffServ (Differentiated Services) 같은 확장 가능한 클래스 기반 모델 등장.
3.  **현재 요구**: 클라우드(Cloud), 5G, IoT 시대로 넘어가며 수만 개의 세션을 실시간으로 제어해야 하는 초연결 시대의 필수 인프라 기술로 자리 잡음.

**📢 섹션 요약 비유**
QoS 도입 전의 네트워크는 "줄 서는 기준 없이 돈을 내면 모두 똑같이 기다리는 주점"과 같아서, 단순히 문을 넓히는 것(회선 증설)만으로는 줄이 길어지는 피크 시간을 해결할 수 없습니다. QoS는 "VIP 손님은 별도 입구로 입장시키고 일반 손님은 대기석에 앉게 하는 '컨시어지(Cierge) 시스템'"을 도입하여 혼잡을 통제하는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

QoS는 크게 **모델(Model)**과 **메커니즘(Mechanism)**으로 나뉜다. 모델은 "어떻게 자원을 예약/분류할 것인가"에 대한 전략이고, 메커니즘은 실제 라우터/스위치에서 "어떻게 패킷을 처리할 것인가"에 대한 전술이다.

#### 1. QoS 모델 (QoS Models)

| 모델 명 (Full Name) | 핵심 특성 | 프로토콜/메커니즘 | 장단점 |
|:---|:---|:---|:---|
| **Best Effort** | QoS 미적용. 인터넷 기본 동작. | None. FIFO (First In First Out). | 장점: 설정 불필요. 단점: 품질 보장 불가. |
| **IntServ** (Integrated Services) | **"연결 지향형"**. 애플리케이션이 통신 전 전 경로의 대역폭을 **예약**. | **RSVP (Resource ReSerVation Protocol)** | 장점: 확실한 보장. 단점: 라우터의 상태 유지 부담으로 확장성이 **매우 낮음** (Scalability Issue). |
| **DiffServ** (Differentiated Services) | **"클래스 기반"**. 패킷 헤더에 **마킹(Marking)**만 하고, 각 라우터는 독립적으로 우선순위 처리. | **DSCP (Differentiated Services Code Point)**, PHB (Per-Hop Behavior) | 장점: 확장성 우수, 현대 인터넷 표준. 단점: 종단 간(End-to-End) 보장이 상대적으로 약함. |

#### 2. QoS 동작 파이프라인 (The 4 Actions)
실제 네트워크 장비에서 QoS가 적용되는 흐름은 다음과 같다.

1.  **Classification (분류)**: ACL (Access Control List)이나 NBAR (Network Based Application Recognition)를 통해 트래픽 식별.
2.  **Marking (마킹)**: 식별된 패킷의 L2(802.1Q CoS, 3bit) 또는 L3(IPv4 ToS/DSCP, 6bit) 필드에 색인(색상) 표시.
    *   *예: DSCP EF(Expedited Forwarding) = VoIP, AF41 = Streaming*
3.  **Congestion Management (혼잡 관리/큐잉)**: 출력 인터페이스의 버퍼에서 대기할 때 어떤 줄에 서게 할 것인가 결정.
4.  **Congestion Avoidance (혼잡 회피)**: 버퍼가 가득 차기 전에 미리 패킷을 버려서 송신 측의 전송률을 낮추게 유도.

**ASCII 아키텍처: QoS Processing Flow**
```ascii
      [Incoming Packet]
             │
             ▼
    +---------------------+
    │ 1. Classification   │  ◄── (Who are you? ACL, MAC, IP, Port)
    +---------------------+
             │
             ▼
    +---------------------+
    │ 2. Marking          │  ◄── (Get a Tag! L2-CoS, L3-DSCP)
    |   (Coloring)        │      - Ex: EF (Voice), AF31 (Video)
    +---------------------+
             │
             ▼
    +---------------------+
    │ 3. Policing/Shaping │  ◄── (Rate Limiting)
    |   (Metering)        │      - Ex: CIR 100Mbps (Policing=Drop, Shaping=Buffer)
    +---------------------+
             │
             ▼
    +---------------------+
    │ 4. Queuing (Q)      │  ◄── (Congestion Management)
    |   + Scheduling      │      - Ex: PQ, WFQ, LLQ, CBWFQ
    +---------------------+
             │
             ▼
    +---------------------+
    │ 5. Dropping         │  ◄── (Congestion Avoidance)
    |   (WRED/Tail Drop)  │      - Ex: Random Drop before full
    +---------------------+
             │
             ▼
      [Outbound Link]
```

#### 3. 심층 기술: 큐잉 알고리즘 (Queuing Algorithms)

*   **FIFO (First In First Out)**: 큐잉 없음. 늦게 온 놈이 기다림. Tail Drop 발생으로 TCP Global Synchronization 유발.
*   **PQ (Priority Queuing)**: High, Medium, Normal, Low 4개의 큐. High가 비어야만 Medium이 전송됨. **단점**: Low 우선순위 트래픽 굶주림(Starvation) 현상 발생.
*   **WFQ (Weighted Fair Queuing)**: 흐름(Flow)별로 가중치를 두어 대역폭 배분. 패킷 길이를 고려하여 대기 시간을 공정하게 계산.
*   **LLQ (Low Latency Queuing)**: PQ의 엄격한 우선순위 보장과 CBWFQ(Class-Based WFQ)의 대역폭 보장을 결합. 음성 트래픽용 전용 큐(Strict Priority)와 데이터용 가중치 큐를 동시에 운영하는 **현재 표준**.

#### 4. 핵심 알고리즘: WRED (Weighted Random Early Detection)

WRED는 **"TCP Global Synchronization"** 현상을 막기 위해 고안되었다. Tail Drop 방식은 버퍼가 꽉 차는 순간 모든 패킷을 삭제하여, 모든 TCP 세션이 동시에 전송을 멈추거나 줄이는 현상을 유발한다.
*   **원리**: 버퍼 사용량이 임계값(Threshold)에 도달하면, 대기 순서와 무관하게 **확률적으로(Random)** 미리 패킷을 버린다.
*   **Weighted**: 단순 랜덤이 아닌, 패킷의 마킹(DSCP) 값에 따라 **낮은 등급의 패킷을 먼저 버리고, 높은 등급은 최대한 보호**하는 가중치를 적용한다.

**코드 스니펫: Cisco IOS 스타일 QoS 설정 예시**
```cisco
! 1. Class Map (분류)
class-map VOICE
 match ip dscp ef

! 2. Policy Map (정책 결합 - 큐잉 + 보장 대역폭)
policy-map WAN_POLICY
 class VOICE
  priority 32   ! LLQ: VoIP용 보장 대역폭 및 최저 지연 보장
 class VIDEO
  bandwidth 256 ! CBWFQ: 정상적 가중치 배분
 class class-default
  fair-queue    ! 나머지 트래픽은 WFQ
  random-detect ! WRED 활성화

! 3. Service Policy (인터페이스 적용)
interface Serial0/0
 service-policy output WAN_POLICY
```

**📢 섹션 요약 비유**
QoS 아키텍처는 **"공항 수속 프로세스"**와 같습니다. **Classification**은 여권 확인(누구냐), **Marking**은 비자 스탬프(어떤 등급이냐), **Policing**은 보안 검색대(위험 물품은 압수), **Queuing**은 탑승 대기열(일등석은 먼저, 이코노미는 줄서기)입니다. 특히 **LLQ**는 비행기 출발 직전까지 늦게 도착하는 VIP들을 위해 별도 샛길을 만들어주는 시스템이며, **WRED**는 탑승구가 붐비기 전에 일반석 탑승객들에게 "대기 시간이 길어지니 편을 변경하세요"라고 미리 안내하여 혼잡을 분산시키는 스마트 게이트(Smart Gate) 역할을 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: IntServ vs DiffServ

| 비교 항목 | IntServ (Integrated Services) | DiffServ (Differentiated Services) |
|:---|:---|:---|
| **핵심 철학** | Hard QoS (자원 예약 기반) | Soft QoS (클래스 기반 통계적 보장) |
| **신호 방식** | RSVP (Path, Resv 메시지) | Out-of-Band (SLA에 따른 사전 설정) |
| **상태 관리** | Stateful (라우터가 모든 Flow 상태 유지) | Stateless (패킷 헤더만 보고 처리) |
| **확장성 (Scalability)** | 낮음 (인터넷 전체 사용 불가) | 높음 (코어 네트워크에 적합) |
| **적용 범위** | Edge-to-Edge, 소규모 전용망 | End-to-End (전체 인터넷) |
| **복잡도** | 장비 부하 높음 | 설정 및 관리 용이 |

#### 2. 과목 융합 관점

1.  **네트워크 & 운영체제 (TCP/IP Stack)**:
    *   QoS의 **WRED**와 같은 혼잡 회피 기술은 송신 호스트의 **TCP 혼잡 제어(Congestion Control)** 알고리즘과 상호작용한다. 네트워크가 ECN (Explicit Congestion Notification) 비트를 세트하면, TCP는 혼잡 윈도우(Congestion Window)를 즉시 축소한다. 즉, L3의 QoS가 L4의 전송률을 제어하는 계층 간 시너지가 발생한다.

2.  **네트워크 & 보안 (Security)**:
    *   **Classification** 과정은 보안의 **Deep Packet Inspection (DPI)**와 매우 유사하다. 트래픽의 내용을 보고 분류하므로, QoS 정책과 보안 정책(Firewall)이 상충할 수 있다. 예를 들어, 보안 장비가 악성 코드로 판단하여 차단하는 트래픽을 QoS는 우선순위를 높여서 통과시키려는 충돌이 발생할 수 있으므로, 이에 대한 정책 수립(Policy Chaining)이 필요하다.

**ASCII 다이어그램: IntServ vs DiffServ 구조적 차이**
```ascii
      [ IntServ Model (상태 유지) ]              [ DiffServ Model (상태 비저장) -->

   Sender --- Router A --- Router B --- Receiver     Sender --- Router A --- Router B --- Receiver
      |         |          |         |                |         |          |         |
   (RSVP)    (State)    (State)   (State)           (Mark)    (No       (No      (No
                                                  Header)   State)    State)   State)
                                                           (PHB)      (PHB)    (PHB)

   "모든 라우터가 대화 상대를 기억함"          "각 라우터는 표지판만 보고 행동함"
```

**📢 섹션 요약 비유**
IntServ와 DiffServ의 차이는 **"예약제 식당"과 "붐비는 시장 통식당"**의 차이와 같습니다. **IntServ**는 미리 전화를 걸어 자리를 완벽하게 예약해야 하