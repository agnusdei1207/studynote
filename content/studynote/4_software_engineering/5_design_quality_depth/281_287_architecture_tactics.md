+++
title = "281-287. 아키텍처 품질 전술 (Quality Tactics)"
date = "2026-03-14"
[extra]
category = "System Quality"
id = 281
+++

# 281-287. 아키텍처 품질 전술 (Quality Tactics)

### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 아키텍처의 비기능적 요구사항(NFR)을 만족시키기 위해, 설계 단계에서 선택 가능한 '의사결정의 기본 단위'이자 구체적인 설계 패턴의 집합.
> 2. **가치**: 장애 허용(Fault Tolerance)과 확장성(Scalability)을 코드 레벨의 구현 이전에 아키텍처 차원에서 보장하여, 대규모 시스템의 수명 주기 비용(TCO)을 최적화함.
> 3. **융합**: 클라우드 네이티브(Cloud Native) 환경의 MSA (Microservices Architecture) 설계 및 SRE (Site Reliability Engineering)의 SLA (Service Level Agreement) 준수를 위한 핵심 토대.

---

### Ⅰ. 개요 (Context & Background)

소프트웨어 아키텍처에서 **품질 속성(Quality Attributes)**이란 시스템이 수행해야 할 기능적 동작이 아니라, 그 기능이 **얼마나 잘** 수행되는지를 나타내는 비기능적 요구사항을 의미합니다. **전술(Tactics)**이란 이러한 품질 속성을 달성하기 위해 아키텍트가 취할 수 있는 **'구체적인 설계 결정'**이자 **'조작적 기법'**입니다. 패턴(Pattern)이 특정 문맥에서 재사용 가능한 해결책이라면, 전술은 더 작고 원자적인 단위의 선택지로서, 여러 전술을 조합하여 패턴을 구성하게 됩니다.

기존의 소프트웨어 개발에서는 기능 구현에 집중하다 보니, 트래픽이 폭증할 때(성능)나 서버 장애가 발생했을 때(가용성) 대응하지 못해 시스템이 마비되는 경우가 빈번했습니다. 이를 해결하기 위해 **사전에(Proactive)** 시스템의 구조를 설계하는 단계에서 '무엇을 우선으로 할 것인가'에 대한 기준을 마련해야 하며, 이것이 바로 아키텍처 품질 전술의 등장 배경입니다.

> 💡 **개념 비유**
> 건물을 짓는다고 가정할 때, '화장실이 몇 개냐'는 기능적 요구사항이지만, '지진이 와도 무너지지 않는가(가용성)', '수만 명이 통과해도 붐비지 않는가(성능)', '도둑이 침입해도 막을 수 있는가(보안)'는 품질 속성입니다. **전술(Tactics)**은 이를 위해 '내진설계(earthquake resistance)를 어떤 방식으로 할 것인가', '비상계단을 어디에 둘 것인가'를 결정하는 **구조 설계 기법**입니다.

📢 **섹션 요약 비유**: 건물의 설계도면을 그리는 단계에서, 단순히 방의 배치만 결정하는 것이 아니라, 화재 시 대피를 위한 비상구와 방화벽 설치, 혼잡을 막기 위한 엘리베이터 운영 알고리즘을 미리 설계에 반영하는 **구조적 설계 기법**과 같습니다.

---

### Ⅱ. 아키텍처 핵심 전술 심층 분석 (Deep Dive)

품질 속성은 상충 관계(Trade-off)에 있으므로, 아키텍트는 상황에 따라 적절한 전술을 선택해야 합니다. 주요 품질 속성별 핵심 전술과 내부 동작을 분석합니다.

#### 1. 가용성 (Availability) 전술
시스템이 장애(Fault) 발생 시에도 서비스를 중단 없이 제공하는 능력입니다. 핵심은 **장애 감지**, **장애 복구**, **장애 예방**입니다.

| 전술 분류 | 구체적 기법 | 내부 동작 및 파라미터 |
|:---:|:---|:---|
| **장애 감지** | **Heartbeat (하트비트)** | 주기적인 생존 신호 전송 (주기: ms 단위). 타임아웃(Timeout) 발생 시 장애 판단. |
| | **Ping/Echo** | ICMP 또는 애플리케이션 레벨 요청/응답으로 노드 상태 확인. |
| **장애 복구** | **Redundancy (중복화)** | **Active-Active**, **Active-Standby** 모드로 자원을 이중화하여 Failover(장애 조치) 수행. |
| | **State Resynchronization** | 장애 복구 후 데이터 일관성을 맞추기 위한 상태 동기화. |
| **장애 예방** | **Exception Handling** | 예외 상황 발생 시 시스템 충돌(Crash)을 방지하고 안전한 상태로 복귀. |

```ascii
       [ 가용성 전술: Fault Tolerance 메커니즘 ]

   Client
      | ① Request
      v
  [ Load Balancer ] -----> [ Active Node #1 ] (정상)
      |                         |
      | ② Heartbeat Fail        | ③ Data Replication (Sync)
      v                         v
  [ Standby Node #2 ] <------(Mirror DB)
      |
      | ④ Auto Failover (Promote to Active)
      v
   Response (No downtime)

  * Heartbeat 주기(T) < RTO (Recovery Time Objective)를 만족해야 함.
```

**[ASCII 해설]**
위 다이어그램은 **Active-Standby(활성-대기)** 구조를 통한 가용성 확보 방식을 도식화한 것입니다.
1. **정상 상태**에서는 Active Node #1이 모든 트래픽을 처리하며, 동시에 Standby Node #2로 데이터를 실시간 복제(Replication)합니다.
2. **장애 감지**는 Load Balancer나 클러스터 매니저가 Active Node로부터 **Heartbeat** 신호가 끊어졌을 때 감지합니다.
3. **자동 전환(Failover)** 과정을 통해 Standby Node가 Active 역할로 승격(Promotion)되어 트래픽을 처리합니다. 이 과정에서 사용자는 서비스 중단을 인지하지 못하게 됩니다. 이데이터 일관성을 위해 **State Sync**가 필수적입니다.

#### 2. 성능 (Performance) 전술
이벤트에 대한 응답 시간을 최소화하고 처리량(Throughput)을 극대화하는 전술입니다.

| 전술 분류 | 구체적 기법 | 내부 동작 및 파라미터 |
|:---:|:---|:---|
| **자원 관리** | **Resource Arbitration** | 경쟁하는 요청 간 자원 분배. 스케줄링 알고리즘(FIFO, Priority Queue) 활용. |
| | **Concurrency (병행성)** | 다중 스레드/프로세스를 통한 병렬 처리. Race Condition 방지를 위한 Lock 전략 필요. |
| **데이터 관리** | **Caching (캐싱)** | 자주 조회되는 데이터를 **Cache Memory**나 **Redis(Remote Dictionary Server)**에 저장. |
| | **Data Replication** | DB를 여러 노드로 복제하여 읽기 작업(Read) 분산. |

```ascii
      [ 성능 전술: Caching & Concurrency Flow ]

   Request Queue
      |
      v
  [ Scheduler ]  (Priority Queue / Round Robin)
      |
      +--+--+--+
      |  |  |  (Divide & Conquer)
      v  v  v
   [ Thread Pool ] <-----> [ L1/L2 Cache ] (Hit Rate ~95%)
      |  |  |
      +--+--+--+
         |
         v
    [ Data Source ]
      (DB/Disk)

  * Context Switching 비용 최소화가 핵심.
```

**[ASCII 해설]**
성능 저하를 방지하기 위해 **Cashing(캐싱)**과 **Concurrency(병행성)**를 활용하는 구조입니다.
1. 요청은 먼저 **Scheduler**에 의해 우선순위가 부여되며, 자원이 허용하는 범위 내에서 **Thread Pool**을 통해 병렬로 처리됩니다.
2. 데이터 접근 시, 느린 디스크나 DB에 직접 접근하기보다 고속 메모리 계층인 **Cache**를 먼저 조회(Cache Hit)하여 지연 시간(Latency)을 획기적으로 줄입니다.
3. **Context Switching**(문맥 교환) 오버헤드를 줄이는 스레드 풀링 기법이 성능 향상의 핵심 메커니즘입니다.

#### 3. 보안성 (Security) 전술
시스템과 데이터를 비인가된 접근으로부터 보호하는 전술입니다. **AAA (Authentication, Authorization, Auditing)** 프레임워크가 핵심입니다.

| 전술 분야 | 구체적 기법 | 내부 동작 및 프로토콜 |
|:---:|:---|:---|
| **인증 (AuthN)** | **MFA (Multi-Factor Auth)** | 지식(비밀번호), 소유(토큰), 생체(Biometric) 중 2개 이상 검증. |
| | **JWT (JSON Web Token)** | Stateless 인증을 위한 서명 기반 토큰 발행. |
| **인가 (AuthZ)** | **RBAC (Role-Based Access Control)** | 역할(Role) 기반으로 자원 접근 권한 제어. |
| **보호** | **Encryption** | 데이터 전송 시 **TLS (Transport Layer Security)**, 저장 시 **AES** 알고리즘 적용. |
| | **Firewall / IDS** | **DMZ (Demilitarized Zone)** 구성 및 침입 탐지 시스템 도입. |

```ascii
         [ 보안성 전술: Authentication & Authorization ]

   User (Alice)
      | ① Credentials (ID/PW)
      v
  [ Auth Server ] ---- (Verify Identity) ----> [ Identity Provider ]
      | ② Issue Token (Access Token + Refresh Token)
      v
  [ API Gateway ]
      | ③ Intercept Request
      v
  [ Authorization Filter ] ---- (Check Token & Scope) ----> [ Allow? ]
      |
      +----> Yes ----> [ Business Logic ]
      +----> No  ----> [ 403 Forbidden ]

  * 모든 진입점(Entry Point)에서의 검증(Validate)이 필수적.
```

**[ASCII 해설]**
보안 전술은 **인증(Authentication)**과 **인가(Authorization)**의 분리된 계층에서 이루어집니다.
1. 사용자는 자격 증명을 **Auth Server**에 제출하고, 검증이 완료되면 서명된 **Access Token**을 발급받습니다.
2. 이후 요청마다 **API Gateway**나 **Filter**는 이 토큰을 검증(Intercept)하여, 해당 요청이 리소스에 접근할 권한(Scope)이 있는지 확인합니다.
3. 이 과정에서 민감한 데이터는 암호화(Encryption)되어 전송되며, 비정상적인 패턴은 **IDS**에 의해 탐지됩니다.

#### 4. 유지보수성 (Modifiability) 전술
변경 사항이 발생했을 때, 시스템의 다른 부분에 미치는 영향(Ripple Effect)을 최소화하는 전술입니다. **Cohesion(응집도)**는 높이고 **Coupling(결합도)**는 낮추는 것이 핵심입니다.

| 전술 분야 | 구체적 기법 | 설계 원칙 |
|:---:|:---|:---|
| **모듈화** | **Encapsulation (캡슐화)** | 구현 세부사항을 숨기고 인터페이스만 노출. |
| | **Abstraction (추상화)** | 변하기 쉬운 로직과 변하지 않는 인터페이스 분리 (OCP 원칙). |
| **분리** | **Layered Architecture** | 프레젠테이션, 비즈니스, 데이터 영역을 물리적/논리적으로 분리. |
| | **Microkernel** | 핵심 기능(Core)과 확장 기능(Plug-in)을 분리. |

```ascii
    [ 유지보수성 전술: Low Coupling Architecture ]

   [ UI Layer ] (Web/Mobile)
      | (Interface A)  <-- 변화 영향 최소화
      v
   [ Service Layer ] (Business Logic)
      | (Interface B)
      v
   [ Repository Layer ] (Data Access)
      |
      v
   [ Database ]

   * 변경(Modification): Service Layer 내부 로직 변경 시,
     UI나 DB 스키마가 영향을 받지 않음(Dependency Inversion).
```

**[ASCII 해설]**
유지보수성은 계층 간의 **결합도(Coupling)**를 낮춤으로써 달성합니다.
1. **Layered Architecture**를 통해 상위 계층(UI)은 하위 계층의 구체적 구현이 아닌, 추상적인 **인터페이스(Interface)**에 의존합니다.
2. 만약 **Service Layer**의 로직이 변경되거나 교체되더라도, 인터페이스 계약이 유지된다면 **UI Layer**는 전혀 수정할 필요가 없습니다. 이를 **Parnas의 정보 은닉** 원칙이라고 합니다.
3. 이는 코드 수정 범위를 **국소화(Localize)**시켜 유지보수 비용과 오류 발생 확률을 획기적으로 줄여줍니다.

📢 **섹션 요약 비유**: 가용성 전술은 '자동차에 스페어 타이어와 네비게이션(재경로 탐색)을 두는 것'이고, 성능 전술은 '고속도로에 하이패스 차선(전용 자원)을 설치하여 혼잡을 피하는 것'입니다. 보안 전술은 '모든 입구에 보안 검색대(인가)를 설치하고 출입증을 확인하는 절차'이며, 유지보수성 전술은 'LEGO 블록처럼 부품을 표준화하여 고장 난 부품만 쏙 빼서 교체할 수 있는 구조'를 만드는 것입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

각 전술은 독립적으로 존재하지 않으며, 서로 **상충(Trade-off)**되거나 **상호 보완(Synergy)**됩니다.

#### 1. 품질 속성 간 상충 관계 (Trade-off Matrix)

| 품질 A | 품질 B | 상충 내용 (Conflict) | 설명 |
|:---:|:---:|:---|:---|
| **보안성** | **성능** | 암호화 오버헤드 | 데이터를 암호화(Encryption)하면 CPU 사용량이 증가하고 지연 시간이 발생하여 성능이 저하됨. |
| **일관성** | **가용성** | CAP 정리 | 분산 환경에서 데이터 일관성을 강화하면(CP), 네트워크 분산 시 일부 노드가 응답하지 못해 가용성이 낮아질 수 있음. |
| **유지보수성** | **성능** | 추상화 비용 | 유지보수성을 높이기 위해 추상화 계층(Interface)을 많이 두면