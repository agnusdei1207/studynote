+++
title = "201-204. 소프트웨어 아키텍처와 4+1 View"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 201
+++

# 201-204. 소프트웨어 아키텍처와 4+1 View

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 아키텍처는 시스템의 구성 요소, 그들의 관계, 그리고 환경을 통제하는 **최상위 설계 구조**로, 변경 비용을 최소화하고 품질 속성(Quality Attributes)을 보장하는 결정체이다.
> 2. **가치**: 4+1 View 모델은 **Logical, Process, Implementation, Deployment**라는 상이한 관심사를 **Use Case**라는 공통의 중심축으로 연결하여, 이해관계자 간의 커뮤니케이션 단절을 해소하고 대규모 시스템의 복잡성을 격리·관리한다.
> 3. **융합**: MSA (Microservice Architecture)나 **Cloud-Native** 환경으로 전환될수록 컨테이너화된 **Deployment View**와 이벤트 기반의 **Process View**가 시스템 수명 주기(SDLC)에서 핵심 의사결정 도구로 작용한다.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
소프트웨어 아키텍처(Software Architecture)는 단순히 모듈을 나열하는 것이 아니라, 시스템의 **조직(Organization)**, 구성 요소(Component) 간의 **관계(Relationship)**, 그리고 이들을 통제하는 **설계 원칙(Design Principles)**의 집합체입니다. 이는 ISO/IEC 42010 표준에서 "시스템의 기본적인 조직 구조를 구성하는 요소들과 그들의 상호작용, 그리고 환경과의 관계를 규정하는 것"으로 정의됩니다. 아키텍처는 '의사결정'의 연이며, 일단 정의되면 시스템의 **Non-Functional Requirements (NFR, 비기능적 요구사항)**인 성능, 보안, 확장성 등이 물리적으로 한정되기에 엔지니어링의 가장 중요한 단계입니다.

**등장 배경 및 패러다임**
① **기존 한계**: 초기 개발 단계에서 코드 중심의 설계(Centric Design)를 따르면, 시스템이 거대해짐에 따라 'Spaghetti Code(스파게티 코드)' 현상이 발생하여 유지보수 비용이 기하급수적으로 증가합니다. 단일 관점으로는 보안 전문가, 네트워크 관리자, 개발자의 요구를 동시에 만족시킬 수 없습니다.
② **혁신적 패러다임**: 1995년 Philippe Kruchten이 제안한 **4+1 View Model**은 "하나의 아키텍처는 보는 사람(Stakeholder)마다 다르게 보인다"는 관점론(Perspectivism)을 도입했습니다. 이를 통해 논리적 구조와 물리적 배포를 분리하여 **Concern Separation (관심사 분리)**을 달성했습니다.
③ **비즈니스 요구**: 현대의 **DevOps (Development and Operations)** 및 **MLOps (Machine Learning Operations)** 환경에서는 코드의 변경 사항이 실제 운영 환경에 얼마나 빨리 반영되는지(Time-to-Market)가 핵심 경쟁력이므로, 견고한 아키텍처가 필수적입니다.

**💡 비유**
건물을 짓는다고 할 때, 건축주는 평면도(논리 뷰)를, 시공자는 전기 배선도(프로세스 뷰)를, 자재 공급업체는 자재 명세서(구현 뷰)를, 인테리어 디자이너는 배치 계획(배포 뷰)을 각각 필요로 하듯, 소프트웨어도 관점에 따라 같은 대상을 다르게 묘사해야 전체가 돌아갑니다.

```ascii
      [ Stakeholder Needs Alignment ]
      
  User (End-User)         Developer (Coders)       System Engineer (Ops)
 +------------------+   +----------------------+   +---------------------------+
 | "어떤 기능을 제공?" |   | "어떤 클래스로 구현?"  |   | "어디에 서버를 배치?"       |
 +--------+---------+   +----------+-----------+   +-----------+---------------+
          |                        |                           |
          v                        v                           v
  +--------------------------------------------------------------------------+
  |                  SOFTWARE ARCHITECTURE (The Bridge)                      |
  |          Translating Business Logic into Technical Reality               |
  +--------------------------------------------------------------------------+
          |                        |                           |
          +------------------------+---------------------------+
                                   |
                     V  Unified Vision via Architecture  V
```

📢 **섹션 요약 비유**: 소프트웨어 아키텍처는 **도시 설계(Master Plan)**와 같습니다. 도로의 폭과 배치(논리 구조)를 잘못 정하면 나중에 건물(구현)을 아무리 고급스럽게 지어도 교통 체증(성능 저하)이 발생하기 때문입니다. 따라서 건축가는 착공 전에 모든 관계자의 요구를 융합한 청사진을 반드시 확보해야 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**4+1 View Model 상세 구성**
Philippe Kruchten의 4+1 View Model은 서로 다른 4개의 기술적 관점과 1개의 사용자 관점으로 시스템을 바라봅니다. 이는 단일 아키텍처 문서의 모순을 피하고, 각 뷰(View)가 특정 품질 속성을 최적화할 수 있게 합니다.

| 뷰(View) | 주요 관심사 | 핵심 요소 (Elements) | 설계 질문 (Design Questions) |
|:---:|:---|:---|:---|
| **Logical View** (논리 뷰) | 기능적 요구사항 | Class, Object, Layer, Interface | 시스템의 기능이 어떤 **객체지향 구조**로 나뉘는가? |
| **Process View** (프로세스 뷰) | 무결성, 성능, 병행성 | Thread, Process, Synchronization, IPC | 시스템이 어떤 **흐름**으로 실행되며 락(Lock)은 어떻게 관리되는가? |
| **Development View** (구현 뷰) | 모듈성, 재사용성 | Package, Library, File, Directory | 코드가 **파일 시스템**상에서 어떻게 조직되는가? |
| **Physical View** (배포 뷰) | 확장성, 가용성 | Node, Server, Network, Topology | **하드웨어/컨테이너**에 어떻게 배포되는가? |
| **Scenarios** (유스케이스) | 기능적/비기능적 통합 | Actor, Use Case, Flow | 모든 뷰가 올바르게 연결되었는가? |

**아키텍처 구조 다이어그램 (4+1 Topology)**

```ascii
           [ Logical View (Functional) ]      <---+--- Class Diagrams, Object Models
                  +--------+--------+                    
                  |   Use Case    |                 
                  |   View (+1)   |                 
                  +--------+--------+                    
           (Functional / Behavioral Requirements)
                   /    |    \
                  /     |     \
   +-------------+------+------+-------------+
   |             |      |      |             |
   v             v      v      v             v
[Process]  [Development]  [Physical]    [Scenarios (Dynamic)]
(Runtime)   (Static)      (Topology)       (Validation)

   Key Relationships:
   1. Use Case drives all other views (Requirements)
   2. Process View maps to Physical Nodes (Deployment)
   3. Logical Components map to Development Packages (Implementation)
```

**심층 동작 원리 및 시나리오 기반 검증**
① **유스케이스(Scenarios)의 역할**: 이 모델의 중심('+1')인 유스케이스는 단순히 기능을 나열하는 것이 아니라, 나머지 4개 뷰의 정합성을 검증하는 **'스크립트(Script)'** 역할을 합니다.
② **논리 뷰의 내부 동작**: 시스템을 Layered Architecture (계층형 아키텍처)나 MVC (Model-View-Controller) 패턴으로 설계할 때, **Facade Pattern**을 통해 하위 모듈의 복잡성을 숨기고 인터페이스를 제공합니다.
③ **프로세스 뷰의 내부 동작**: 단일 스레드(Single Thread)에서 멀티스레드(Multi-thread), 혹은 MSA 환경의 비동기 메시지 큐(Message Queue)로 확장될 때, **Race Condition (경쟁 상태)**을 방지하기 위한 동기화 메커니즘이 여기서 정의됩니다.

**핵심 알고리즘 및 패턴 예시**

```java
// [Logical View vs. Implementation View Example]
// 논리 뷰에서는 'OrderService'라는 추상화가 존재하지만,
// 구현 뷰(Development View)에서는 패키지 구조가 결정됩니다.

// Logical: Conceptual Architecture
public interface IOrderProcessor {
    void process(OrderDTO order);
}

// Implementation: Code Organization (Package: com.myshop.internal)
// 이 클래스는 Logical View의 컴포넌트에 매핑됩니다.
public class OrderProcessorImpl implements IOrderProcessor {
    private PaymentGatewayAdapter pgAdapter; // Dependency Injection
    
    public void process(OrderDTO order) {
        // Process View에 해당하는 비동기 로직 예시
        CompletableFuture.runAsync(() -> {
            pgAdapter.pay(order.getAmount());
        });
    }
}
```

📢 **섹션 요약 비유**: 4+1 뷰 모델은 **자동차의 설계 도면 세트**와 같습니다. **유스케이스**는 "운전手册(매뉴얼)"로서, 이 차량이 어떤 상황에서 어떻게 작동해야 하는지 시나리오를 정의합니다. **논리 뷰**는 엔진과 바퀴의 연결 구조도이고, **프로세스 뷰**는 연료와 공기의 흐름(유체 역학)이며, **구현 뷰**는 부품 조립 명세서, **배포 뷰**는 출고되어 도로 위에 있는 실제 차량의 위치입니다. 매뉴얼(유스케이스)에 따라 운전할 수 있어야 나머지 도면들이 유효합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**아키텍처 패턴 비교 분석**
아키텍처 스타일(Architecture Style)은 뷰를 구체화하는 템플릿입니다. 현대 시스템에서 주로 사용되는 Monolithic과 MSA 구조를 4+1 View 관점에서 비교합니다.

| 비교 항목 | Monolithic Architecture (단일형) | Microservices Architecture (MSA, 마이크로서비스) |
|:---|:---|:---|
| **Logical View** | 계층(Layered) 구조. 하나의 코드베이스에 모든 로직이 포함됨. | **Bounded Context** 기반. 각 서비스가 독립적인 도메인 모델 소유. |
| **Process View** | 단일 **JVM (Java Virtual Machine)** 또는 프로세스 내의 메서드 호출. IPC(Inter-Process Communication) 불필요. | 분산 환경. **REST API** 또는 **gRPC (Remote Procedure Call)** 기반의 네트워크 통신 필수. |
| **Implementation View** | 단일 빌드 결과물(WAR/JAR). 모듈 간 강한 결합. | 서비스별 독립적 저장소. **Polyglot Programming**(서비스별 언어 차이 가능) 가능. |
| **Deployment View** | 하나의 서버(또는 클러스터)에 전체 애플리케이션 배포. 배포 시 **DownTime** 발생 가능. **CI/CD (Continuous Integration/Continuous Deployment)** 파이프라인이 상대적으로 단순함. | **Container (Docker/Kubernetes)** 기반 배포. 서비스별 독립적 확장(Scaling). Zero-downtime 배포 가능하지만, 네트워크 트래픽 및 **Service Mesh** 관리 오버헤드 증가. |
| **Cost of Change** | 일부분 수정 시 전체 재컴파일/재배포 필요. 위험도 높음. | 변경된 서비스만 배포. 빠른 피드백 루프 가능. |

**융합 관점의 시너지 및 트레이드오프**
1. **DevOps와의 융합**: **Deployment View**와 **CI/CD** 파이프라인이 직접 연결됩니다. 아키텍처가 얼마나 느슨히 결합(Loosely Coupled)되어 있는지가 배포 자동화의 난이도를 결정합니다.
2. **데이터베이스 (DB)와의 융합**: MSA에서 각 서비스가 독립적인 DB를 갖는 것(Database per Service)은 **ACID (Atomicity, Consistency, Isolation, Durability)** 트랜잭션 관리를 어렵게 만듭니다. 이를 해결하기 위해 **Saga Pattern**이나 **CQRS (Command Query Responsibility Segregation)**와 같은 **Process View** 상의 패턴이 요구됩니다.

```ascii
[ Trade-off Analysis: Performance vs. Modularity ]

     High Modularity (MSA)
            ▲
            |
            |          ● Cloud-Native (High Modularity, High Ops Cost)
            |
            |      ● MSA (Balanced)
            |
            |
  ------- Microservices -----------------------------------
            |       ● Monolith (Low Modularity, High Dev Speed)
            |
            |
            +----------------------------------------------------►
                                  High Performance (Intra-process)
                                    
   * Analysis: 
   - Monolith maximizes speed via memory access (Process View).
   - MSA optimizes for scalability (Deployment View) at cost of network latency.
```

📢 **섹션 요약 비유**: Monolith은 **대형 종합 백화점**과 같습니다. 모든 것이 한 건물 안에 있어 이동이 편리(성능 이점)하지만, 난방 시스템을 고치려면 백화점 전체를 문 닫아야 합니다(유지보수 불편). 반면 MSA는 **푸드트럭 촌**과 같습니다. 각 가게(서비스)가 독립적으로 영업하고 이전/확장이 자유롭지만, 손님(요청)이 가게를 옮겨 다녀야 해서 이동 시간(네트워크 지연)이 발생합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**실무 시나리오 및 의사결정 프로세스**

1.  **문제 상황**: 전자상거래 플랫폼의 장바구니 서비스가 **Black Friday**와 같은 피크 트래픽 시간대에 응답 속도가 급격히 느려지며 Timeout이 발생하고 있습니다.
2.  **기술사적 판단 (Reasoning)**:
    *   **Process View 분석**: 장바구니 로직이 단일 스레드로 동작하거나, Database Connection Pool이 부족하여 병목이 발생함. 혹은 Synchronous 방식의 외부 결제 API 호출이 지연을 유발함.
    *   **Decision**: '동기식 처리'를 '비동기식 이벤트 기반 처리'로 전환하고, **Process View**를 **Event-Driven Architecture (EDA)**