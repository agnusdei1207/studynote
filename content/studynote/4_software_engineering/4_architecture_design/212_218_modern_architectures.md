+++
title = "212-218. 현대적 분산 아키텍처 (MSA, Hexagonal, Clean)"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 212
+++

# 212-218. 현대적 분산 아키텍처 (MSA, Hexagonal, Clean)

## # [주제명] 현대적 분산 아키텍처 및 설계 패러다임
### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Monolithic (단일형) 거대 시스템의 한계를 극복하기 위해 **MSA (Microservices Architecture, 마이크로서비스 아키텍처)**를 통해 서비스를 단위별로 분리하고, **EDA (Event-Driven Architecture, 이벤트 기반 아키텍처)**로 비동기성능을 확보한다.
> 2. **가치**: **Hexagonal Architecture (헥사고날 아키텍처)**와 **Clean Architecture (클린 아키텍처)**를 통해 비즈니스 로직(Core)을 외부 인프라(DB, UI, Framework)로부터 격리하여 유지보수성과 테스트 용이성을 극대화한다.
> 3. **융합**: CI/CD (Continuous Integration/Continuous Deployment, 지속적 통합/배포) 파이프라인과 컨테이너 오케스트레이션(Kubernetes)과 결합하여 초대형 규모의 **Cloud-Native (클라우드 네이티브)** 시스템을 구축한다.

---

### Ⅰ. 개요 (Context & Background) - [500자+]

#### 개념 및 철학
현대적 분산 아키텍처는 급변하는 비즈니스 요구사항(Agile, 애자일)과 대규모 트래픽 처리(CX, 고객 경험)라는 두 가지 과제를 해결하기 위해 등장했다. 전통적인 **Monolithic Architecture (모놀리식 아키텍처)**는 모듈 간 결합도가 높아 코드 수정 시 전체 시스템을 재배포해야 하는 '배포 보트 효과(Deployment Boat Effect)'가 발생한다. 이를 해결하기 위해 시스템을 기능 단위로 쪼개는 **MSA**와, 시스템의 상태 변화를 중심으로 흐름을 제어하는 **EDA**가 주목받고 있다. 또한, 이러한 분산 환경에서 복잡도를 관리하기 위해 비즈니스 로직을 기술 구현 세부사항으로부터 분리하는 **Hexagonal**, **Clean** 아키텍처가 필수 설계 원칙으로 자리 잡았다.

#### 💡 비유
MSA는 '전문화된 의료진'으로, 심장내과, 외과, 안과가 각자 병원(서버)을 따로 운영하며 환자(요청)를 전담하는 형태다. 반면, 모놀리식은 '만능 의사' 혼자서 모든 진료를 보는 것과 같다. 클린 아키텍처는 '스마트폰 본체(코어)'와 '충전 케이블/이어폰(외부 인터페이스)'의 관계다. 케이블이 끊어지면 새 것으로 갈아끼우면 될 뿐, 스마트폰 본체를 열어 납땜할 필요가 없다.

#### 등장 배경
1.  **기존 한계 (Monolithic)**: 단일 데이터베이스 인스턴스에 대한 병목, 기술 스택 변경의 어려움(Lock-in), 부분 장애가 전체 장애로 확산되는 위험.
2.  **혁신적 패러다임**: **Cloud Computing (클라우드 컴퓨팅)** 의 발전으로 인프라의 프로그래밍 가능성이 확보됨. **Docker** 등의 컨테이너 기술을 통해 서비스 간 격리성 보장.
3.  **현재 비즈니스 요구**: 빠른 시장 투입(Time-to-Market), 특정 서비스의 독립적 확장(Scaling), Polyglot Programming(서비스별 적합 언어 사용) 필요성 증대.

#### 📢 섹션 요약 비유
마치 거대한 '백화점'이 각각의 독립된 '편의점 프랜차이즈'로 분할하여, 24시간 운영이 가능하게 하고 편의점 하나가 리모델링해도 다른 점포에 영향이 없도록 만드는 구조적 혁신과 같습니다.

```ascii
+---------------------------------------------------------------+
|  [Monolithic Architecture]                                    |
|  +----------------------------------------------------------+  |
|  |  UI Layer                                                 |  |
|  |  +-----------+  +-----------+  +---------------------+   |  |
|  |  | Module A  |  | Module B  |  | Module C (Shared DB)|   |  |
|  |  +-----------+  +-----------+  +---------------------+   |  |
|  |                        |                               |  |
|  +------------------------|-------------------------------+  |
|                           |                                  |
|                    [Shared Database]                         |
|                           |                                  |
|               (Single Point of Failure)                      |
+---------------------------|----------------------------------+
                            |
        개선 (Evolution)     ▼
                            |
+---------------------------|----------------------------------+
|  [Microservices Architecture]                                |
|  +-------------+       +-------------+       +-------------+  |
|  |   Service A |       |   Service B |       |   Service C |  |
|  |  (Node.js)  |       |    (Java)   |       |    (Go)     |  |
|  |   + DB A    |       |   + DB B    |       |   + DB C    |  |
|  +-------------+       +-------------+       +-------------+  |
|        |                     |                      |         |
|        +--------[API Gateway / Event Bus]-----------+         |
+---------------------------------------------------------------+
```
> **[해설]** Monolithic 구조는 모듈이 논리적으로 분리되어 있을지라도, 물리적으로는 단일 프로세스 내에서 실행되며 하나의 거대한 데이터베이스를 공유합니다. 이로 인해 코드 수정 시 전체를 다시 빌드(Re-build)해야 하며, 데이터베이스 스키마 변경은 시스템 전체의 정지를 초래할 수 있습니다. 반면, MSA는 각 서비스가 독립적인 프로세스와 데이터베이스 인스턴스를 가집니다. 이를 통해 서비스 A의 트래픽이 폭주해도 서비스 B, C에는 영향을 미치지 않으며, 각 서비스에 가장 적합한 기술 스택(Polyglot)을 선택할 수 있는 유연성을 제공합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [1,000자+]

현대적 아키텍처는 크게 '서비스를 어떻게 분할하느냐(MSA)', '서비스 간 어떻게 통신하느냐(EDA)', 그리고 '개별 서비스를 어떻게 유연하게 설계하느냐(Hexagonal/Clean)'의 세 가지 축으로 분석된다.

#### 1. 구성 요소 상세 분석

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Operation) | 프로토콜/기술 | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **API Gateway** | 진입점 관리 및 라우팅 | 클라이언트 요청을 인증/인가 후 적절한 MS로 전달. 로드 밸런싱 및 서킷 브레이커(Circuit Breaker) 패턴 구현. | REST, gRPC, WebSocket | 공항의 탑승 교통 통제 |
| **Service Mesh (서비스 메시)** | 서비스 간 통신 관리 | 마이크로서비스 간의 네트워크 통신을 추상화하여 관리. **mTLS**(Mutual TLS) 보안, 트레이싱(Tracing), 재시도(Retry) 로직 처리. | **Istio**, Linkerd | 도시의 지하 배관망 및 도로망 |
| **Message Broker (메시지 브로커)** | 비동기 메시징 중계 | 이벤트 생성자(Publisher)가 메시지를 발행하면, 구독자(Subscriber)가 메시지를 가져가는 방식. 메시지 큐잉 및 순서 보장. | **Kafka**, RabbitMQ | 우편집배국 (편지 분류 및 배달) |
| **BFF (Backend for Frontend)** | 프론트엔드 전용 API | 특정 클라이언트(Web, Mobile, IoT)의 요청에 맞춰 데이터를 Aggregation(집계)하여 최적화된 응답 제공. | GraphQL, REST | 식당의 주문-taking 직원 |
| **Port / Adapter** | 인터페이스 계층 | 비즈니스 로직(Core)과 외부 세계(UI, DB) 사이의 변환 로직을 처리. Protocol 변환 담당. | Interface, DTO | 여행용 전원 플러그 어댑터 |

#### 2. 핵심 아키텍처 구조 및 데이터 흐름

아래 다이어그램은 **EDA**를 기반으로 한 **Clean Architecture**의 적용 예시를 보여준다.

```ascii
+-----------------------------------------------------------------------+
|                         [External World]                              |
|  +-------------------+      +-------------------+      +------------+ |
|  |     Client UI     |      |   Legacy System   |      |  NoSQL DB  | |
|  +---------+---------+      +---------+---------+      +------+-----+ |
|            |                          ^                        ^       |
+------------|--------------------------|------------------------|-------+
             |  (REST/GraphQL)          |  (HTTP/TCP)            | (DAO)  |
             v                          |                        |
+------------|--------------------------|------------------------|-------+
|  +---------+---------+    (Driving Adapters)            +------+-----+ |
|  |   Controller /    |      [Primary Actors]            | Repository | |
|  |  Presenter (UI)   | ----------------------->          |  Impl      | |
|  |  (Adapter - In)   |                              |   (Adapter) | |
|  +---------+---------+                              +------+-----+ |
|            |                                                 |       |
| ===========|=================================================|======= |
|  +---------v---------+  << APPLICATION BOUNDARY >>    +------v-----+ |
|  |    Port (I/F)     |                              |   Port     | |
|  | (UseCase Input)   |                              | (Output)   | |
|  +------------------+                              +------------+ |
|  |                   |  <BUSINESS LOGIC CORE>       |            | |
|  |    USE CASE       |     (No Framework,           |   ENTITY   | |
|  |  (Application)    |      No Web, No DB)          |   (Model)  | |
|  |                   |                              |            | |
|  +------------------+                              +------------+ |
|            |                                                 ^       |
| ===========|=================================================|======= |
|            |                                    (Event Bus: Kafka)  |
+------------|------------------------------------------|-----------+
             |                                          |
             |  v  (Domain Event)                        |  v (Event)
      +------+-----+                             +------+-----+
      | Event Bus  | <--------------------------- | Subscriber |
      |  (Broker)  |     (Async Notification)    | (Other MS) |
      +------------+                             +------------+
```

> **[해설]**
> 1.  **진입 (Inbound)**: 클라이언트의 요청은 `Controller/Presenter`(Adapter)에 도달합니다. 이 Adapter는 HTTP 프로토콜 등의 외부 기술을 **Port** 인터페이스에 맞춰 변환합니다.
> 2.  **처리 (Core)**: 포트를 통해 전달된 요청은 `Use Case` 계층에서 처리됩니다. 이때 비즈니스 로직은 데이터베이스나 웹 기술에 전혀 의존하지 않으며, 순수 자바(또는 해당 언어) 객체인 `Entity`를 조작합니다.
> 3.  **저장 및 발행 (Outbound)**: 처리가 완료되면 결과는 `Repository Port`를 통해 데이터베이스에 영속화되거나, 시스템 내부의 중대한 상태 변경(이벤트)은 `Event Bus`로 발행(Publish)됩니다.
> 4.  **확장 (Decoupling)**: 이벤트 버스를 구독하고 있는 다른 마이크로서비스가 변경 사항을 수신하여 자신만의 로직을 수행합니다. 이때 발행자는 수신자를 알 필요가 없으므로 완벽한 느슨한 결합(Decoupling)을 달성합니다.

#### 3. 핵심 알고리즘: 의존성 역전 원칙 (DIP) 코드 구현
클린 아키텍처의 핵심은 고수준 모듈(비즈니스 로직)이 저수준 모듈(DB, UI)에 의존하지 않도록 인터페이스를 중간에 두는 것이다.

```python
# [Bad Example] 고수준 모듈이 저수준 모듈(MySQL)을 직접 의존
class OrderService:
    def create_order(self, order_data):
        # 비즈니스 로직이 구체적인 DB 기술(MySQLDB)에 강하게 결합됨
        db = MySQLDB() 
        db.execute("INSERT INTO orders ...")

# [Clean Architecture] 의존성 역전 적용
from abc import ABC, abstractmethod

# 1. Port (Interface): 고수준 모듈(Usecase)에 위치
class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: 'Order'): pass

# 2. Adapter (Infrastructure): 저수준 모듈에서 인터페이스를 구현 (의존성 방향: DB -> Core)
class MySQLOrderRepositoryAdapter(OrderRepositoryPort):
    def save(self, order: 'Order'):
        # MySQL 구체적인 접속 로직 수행
        print(f"Saving {order.id} to MySQL...")

# 3. Core Entity: 순수 비즈니스 로직
class Order:
    def __init__(self, id, items):
        self.id = id
        self.items = items

# 4. Usecase: 인터페이스(OrderRepositoryPort)에만 의존
class OrderUseCase:
    def __init__(self, repository: OrderRepositoryPort):
        self.repo = repository # 구현체가 아닌 추상화에 의존

    def process_order(self, order_data):
        order = Order(id="ORD-1", items=order_data)
        # 비즈니스 로직 처리 후 저장
        self.repo.save(order)
        # 이벤트 발행
        event_publisher.publish("OrderCreated", order)
```

#### 📢 섹션 요약 비유
MSA와 EDA의 결합은 마치 **'신경계통'**과 같습니다. 뇌(비즈니스 로직)가 명령을 내리면(Clean Architecture의 Core), 신경 전달 물질(이벤트)이 흘러가 손발(다른 마이크로서비스)이 반응합니다. 이때 뇌가 손가락 움직임을 '어떻게' 구현하는지(근육의 수축 등) 알 필요가 없듯이, 시스템 구성요소들은 서로의 내부 구현을 몰라도 협력할 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개+]

#### 1. 심층 기술 비교: Monolithic vs MSA

| 비교 항목 | Monolithic (단일형) | MSA (Microservices) |
|:---|:---|:---|
| **Coupling (결합도)** | **High**: 모듈 간 공유 메모리/DB 사용으로 강한 결합 | **Low**: 서비스 간 독립적 프로세스, API로 느슨한 결합 |
| **Deployment (배포)** | 전체 시스템 재빌드/재배포 필요 (