+++
title = "219-226. 도메인 주도 설계(DDD)와 관련 패턴"
date = "2026-03-14"
[extra]
category = "Architecture & Design"
id = 219
+++

# 219-226. 도메인 주도 설계(DDD)와 관련 패턴
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어의 복잡성을 해결하기 위해 비즈니스 도메인의 근간을 모델링하고, 기술적 관점이 아닌 도메인 관점에서 코드를 구성하는 설계 철학입니다.
> 2. **가치**: 개발자와 비즈니스 전문가 간의 커뮤니케이션 비용을 획기적으로 줄이고, 대규모 시스템에서 유지보수성과 확장성을 보장하며, 특히 CQRS/ES 패턴을 통해 데이터 처리 성능(TPS)을 극대화합니다.
> 3. **융합**: MSA (Microservice Architecture)의 이론적 기반이 되며, 클라우드 네이티브(Cloud Native) 환경에서의 분산 처리 및 데이터 일관성 모델과 밀접하게 연계됩니다.
+++

### Ⅰ. 개요 (Context & Background)

**개념 및 정의**
도메인 주도 설계(DDD: Domain-Driven Design)는 소프트웨어의 복잡성을 관리하기 위해 비즈니스 도메인(Domain)의 핵심 로직과 규칙을 중심으로 설계를 진행하는 소프트웨어 개발 접근법입니다. 기술적 구현(데이터베이스 스키마, 프레임워크 설정 등)이 아닌 비즈니스적 문제 해결에 집중하며, 도메인 전문가와 개발자가 동일한 용어(유비쿼터스 언어)를 사용하여 모델을 구축하는 것을 핵심으로 합니다.

**💡 비유: 지도 제작**
마치 실제 지형(비즈니스)을 본뜬 지도를 그리는 과정과 같습니다. 단순히 길(코드)만 그리는 것이 아니라, 도시의 기능과 구역을 명확히 구분하여 누구나 그 지도를 보고 길을 찾을 수 있도록 만드는 것입니다.

**등장 배경**
1.  **기존 한계**: 애자일(Agile) 변혁과 모놀리식(Monolithic) 아키텍처의 한계로 인해, 비즈니스 요구사항이 빈번하게 변경될 때 코드가 점차 '스파게티 코드화'되어 유지보수가 불가능해지는 현상 발생.
2.  **혁신적 패러다임**: Eric Evans가 제창한 DDD는 '소프트웨어의 본질은 기술이 아니라 도메인 지식'임을 설파하며, 모델 주도 설계(Model-Driven Design)를 통해 코드와 모델 간의 괴리를 해소.
3.  **현재의 비즈니스 요구**: 대규모 분산 시스템(MSA) 환경으로 전환하면서, 서비스 간의 경계를 명확히 하고 느슨한 결합(Loose Coupling)을 유지해야 하는 현대적 요구사항을 완벽하게 충족시킴.

**📢 섹션 요약 비유**
마치 다양한 언어를 사용하는 여러 나라 사람들이 모여 국제 회의를 할 때, '영어'라는 **공용어(Ubiquitous Language)**를 정하고, 각국의 **영토(Bounded Context)**를 존중하며 회의하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

DDD는 전략적 설계(Strategic Design)와 전술적 설계(Tactical Design)로 나뉩니다.

**1. 구성 요소 (표)**

| 요소명 | 역할 | 내부 동작 | 관련 패턴/용어 | 비유 |
|:---|:---|:---|:---|:---|
| **유비쿼터스 언어**<br>(Ubiquitous Language) | 커뮤니케이션 도구 | 도메인 모델, 코드, 문서에서 동일한 용어 사용. 용어 사전 정의. | 전문가 용어 표준화 | 국제 회의 공용어 |
| **바운디드 컨텍스트**<br>(Bounded Context) | 시스템 경계 | 특정 도메인 모델이 유효한 논리적 경계 설정. 맥락별 용어의 모호성 해소. | Context Mapping | 국가의 국경선 |
| **애그리거트**<br>(Aggregate) | 데이터 일관성 단위 | 연관된 도메인 객체 군을 하나의 단위로 묶음. Root를 통해서만 내부 객체 수정 가능. | consistency boundary | 가족 단위 (가장 통제) |
| **엔티티**<br>(Entity) | 식별 가능한 객체 | 고유한 식별자(ID)를 가지며, 생명주기 동안 속성이 변해도 동일성 유지. | Equals/HashCode | 주민등록번호 |
| **밸류 오브젝트**<br>(Value Object) | 속성 중심 객체 | 식별자 없이 속성값으로만 동일성 판단. 불변(Immutable) 객체. | Money, Address | 색상표 (RGB값) |

**2. ASCII 구조 다이어그램: DDD 전략적 아키텍처**

아래 다이어그램은 복잡한 도메인을 여러 바운디드 컨텍스트로 분리하고, 그 사이의 관계(Context Mapping)를 정의하는 구조를 보여줍니다.

```ascii
+---------------------+      +---------------------+
|   Sales Context     |      |   Shipping Context  |
| (상품: 구매 대상)    |----->| (상품: 배송 물건)   |
+---------------------+      +---------------------+
          |                            ^
          | OHS (Open Host Service)    | ACL (Anti-Corruption Layer)
          v                            |
+---------------------+      +---------------------+
|   Inventory Context |<-----|   Legacy ERP System |
| (상품: 재고 자산)   |      +---------------------+
+---------------------+
       |
       | (Internal Layers)
       v
+-----------------------------+
|  [Presentation Layer]       |  (UI, API)
+-----------------------------+
|  [Application Layer]        |  (Use Case Orchestration)
+-----------------------------+
|  [Domain Layer]       <---- |  (Core Logic: Entity, VO, Aggregate)
|  - Aggregate Root           |      ↕ Repository Interface
|  - Domain Service           |
+-----------------------------+
|  [Infrastructure Layer]     |  (JPA, DB, External API Impl)
+-----------------------------+
```

**다이어그램 해설**
1.  **바운디드 컨텍스트(Bounded Context)**: 상위 단계에서 시스템은 판매(Sales), 배송(Shipping), 재고(Inventory) 등으로 분리됩니다. '상품'이라는 용어라도 판매 맥락에서는 '가격'이 중요하지만, 배송 맥락에서는 '무게와 크기'가 핵심입니다.
2.  **맥락 매핑(Context Mapping)**: 컨텍스트 간의 통신은 OHS(Open Host Service), ACL(Anti-Corruption Layer), 공유 커널(Shared Kernel) 등의 패턴으로 정의됩니다. 특히 **ACL**은 레거시 시스템(Legacy System)의 낡은 프로토콜이나 데이터 구조가 우리의 순수 도메인 모델을 오염시키지 않도록 중간에서 번역(변환)해주는 어댑터 역할을 수행합니다.
3.  **계층형 아키텍처**: 각 컨텍스트 내부는 4계층으로 구성됩니다. 가장 핵심은 도메인 계층(Domain Layer)으로, 여기에 비즈니스 규칙이 순수 자바(또는 해당 언어) 코드로 구현됩니다. 인프라 계층(Infrastructure)은 도메인 계층에 의존하며(DB는 도메인을 모름), 의존성 역전 원칙(DIP: Dependency Inversion Principle)이 적용됩니다.

**3. 심층 동작 원리: 애그리거트의 트랜잭션 관리**
애그리거트는 강한 일관성을 유지해야 하는 경계입니다. 따라서 트랜잭션(Transaction)은 하나의 애그리거트 내부에서만 발생해야 합니다.
*   **단계 ①**: 클라이언트 요청이 Application Layer의 `Service`로 들어옴.
*   **단계 ②**: Application Service는 `Repository`를 통해 `Aggregate Root` 엔티티를 로드.
*   **단계 ③**: `Root` 객체의 메서드를 호출하여 상태 변경 비즈니스 로직 수행 (도메인 로직은 엔티티 내부에 존재).
*   **단계 ④**: 변경된 `Root` 객체를 `Repository`를 통해 저장(Persist). 이때 DB 락(Lock)은 애그리거트 단위로 걸림.

**📢 섹션 요약 비유**
DDD 아키텍처는 마치 **'요리 전문 식당'**을 운영하는 것과 같습니다. **유비쿼터스 언어**는 셰프와 손님(비즈니스 전문가)이 사용하는 동일한 메뉴판 용어이며, **바운디드 컨텍스트**는 주방(Back-end)과 홀(Front-end)의 명확한 구분선입니다. **애그리거트**는 '한 번에 조리되는 세트 메뉴'로, 메인 요약(Root)을 통해 사이드 dish들을 관리하는 통제 단위가 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

DDD는 단순히 혼자 쓰이는 것이 아니라, 성능 최적화와 분산 환경을 위해 **CQRS** 및 **이벤트 소싱(Event Sourcing)**과 결합될 때 시너지가 극대화됩니다.

**1. 심층 기술 비교표: CQRS & Event Sourcing**

| 구분 | 전통적 아키텍처 (N-tier CRUD) | **CQRS (Command Query Responsibility Segregation)** | **이벤트 소싱 (Event Sourcing)** |
|:---|:---|:---|:---|
| **핵심 모델** | 단일 모델 (CRUD) | **Command 모델** (상태 변경) + **Query 모델** (조회) | 이벤트 스트림 (상태 변경 이력) |
| **DB 구조** | 단일 DB (Read/Write 공유) | **Write DB** (정규화) + **Read DB** (비정규화, 복제) | **Event Store** (Append-only) |
| **데이터 동기화** | 트랜잭션 (ACID) | 비동기 복제 (Eventual Consistency) | Event Replay를 통한 상태 복원 |
| **성능 지표** | R/W 경합 발생으로 성능 병목 | **Read Scale-out** 용이 (쿼리 전용 최적화) | **Write Throughput** 높음, 무결성 보장 |
| **복잡도** | 구현 단순 | 데이터 동기화 로직 추가 필요 | 시스템 복잡도 증가, 버전 관리 중요 |

**2. ASCII 다이어그램: CQRS + Event Sourcing 아키텍처**

이 다이어그램은 명령(Command)과 조회(Query)가 분리되고, 상태가 아닌 이벤트를 저장하는 방식을 시각화합니다.

```ascii
[User Request]
      |
      +---------------------------+
      |                           |
      v                           v
+----------------+       +----------------+
|   COMMAND SIDE |       |   QUERY SIDE   |
+----------------+       +----------------+
| 1. Validation  |       | (No Update)    |
| 2. Logic Exec  |       |                |
| 3. Event Gen   |       |                |
+-------+--------+       +--------+-------+
        |                        ^
        | (Event Pub)            | (Sync/Async)
        v                        |
+----------------+    (Project)  |
|   Event Store  |--------------+--> [Read Model DB]
| (Append Only)  |  1. Save      |   (Materialized View)
| [Event Sourcing]| 2. Replicate |
+----------------+---------------+
      |      ^
      |      | (Replay for Debug/Recovery)
      +------+
```

**다이어그램 해설**
1.  **분리된 경로**: 사용자의 요청은 **Write(Command)**와 **Read(Query)**로 완전히 분리됩니다. Command 요청은 검증(Validation)과 로직 실행 후, 상태를 직접 수정하는 대신 **이벤트(Event)**를 생성합니다.
2.  **이벤트 저장소(Event Store)**: 생성된 이벤트는 마치 회계 장부와 같이 **Event Store**에 순차적으로(Append-only) 저장됩니다. 여기서는 수정(Update)이나 삭제(Delete)가 없으며 추가(Append)만 존재합니다.
3.  **동기화(Synchronization)**: Event Store에 새로운 이벤트가 기록되면, 이를 구독하는 **Projector**가 이벤트를 읽어 **Read DB**(조회용 DB)의 뷰(View)를 업데이트합니다. 조회 화면은 Read DB만 바라보므로 매우 빠릅니다.
4.  **이벤트 리플레이(Replay)**: 시스템에 오류가 발생하거나 새로운 기능을 추가해야 할 때, 저장된 모든 이벤트를 처음부터 다시 재생(Replay)하여 현재 상태를 완벽하게 복구하거나 새로운 Read Model을 만들 수 있습니다.

**3. 과목 융합 관점**
*   **SW 공학 vs 데이터베이스**: 전통적인 RDBMS는 ACID 트랜잭션과 정규화를 중시하지만, CQRS+ES 패턴은 **결과적 일관성(Eventual Consistency)**을 허용하여 **높은 가용성(Availability)**과 **확장성(Scale-out)**을 택합니다. 이는 CAP 정리에서 Consistency를 희생하고 Availability와 Partition Tolerance를 선택한 분산 시스템 설계와 맥락을 같이합니다.

**📢 섹션 요약 비유**
전통적 방식은 **'은행 창구'**에서 입출금과 조회를 동시에 처리하여 줄이 길어지는 것과 같습니다. **CQRS**는 **'자판기(조회)'**와 **'계좌 이체 접수창구(명령)'**를 분리하여, 자판기는 전국 어디서나 빠르게 이용하게 하고, 이체 창구에서는 보안에 집중하는 것입니다. **이벤트 소싱**은 현재 잔고만 보여주는 통장 대신, **'과거부터 지금까지의 모든 입출금 영수증'**을 보관하는 세무 회계 시스템과 같습니다. 영수증들을 다시 더해보면(Replay) 언제든 현재 잔고를 알 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오 및 의사결정**

*   **시나리오 A: 대규모 전자상거래 플랫폼 (CQRS 도입)**
    *   **상황**: 상품 목록 조회(Query)가 초당 10,000건 이