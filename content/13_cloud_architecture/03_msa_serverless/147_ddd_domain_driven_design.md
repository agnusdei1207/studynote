---
title: "Ddd Domain Driven Design"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 147
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDD(Domain-Driven Design, 도메인 주도 설계)는 에릭 에반스(Eric Evans)가 2003년 제안한 소프트웨어 설계 방법론으로, <strong>비즈니스 도메인(Domain)의 핵심 개념과 규칙을 코드 모델에 직접 반영</strong>함으로써 복잡한 비즈니스 로직을 다루는 소프트웨어의 복잡도를 관리하는 접근법이다.
> 2. **가치**: 개발자와 도메인 전문가가 <strong>유비쿼터스 언어(Ubiquitous Language)</strong> 를 공유하여 소통 오류를 줄이고, 바운디드 컨텍스트(Bounded Context)로 모듈 경계를 명확히 설정하여 마이크로서비스 아키텍처(MSA)의 서비스 분리 기준을 제공한다.
> 3. **판단 포인트**: DDD는 복잡한 도메인(은행·의료·물류)에서 효과적이지만, 단순한 CRUD(Create-Read-Update-Delete) 애플리케이션에는 과설계(Over-engineering)가 될 수 있다.

---

## Ⅰ. 개요 및 필요성

복잡한 비즈니스 시스템을 개발할 때 가장 큰 문제는 <strong>도메인 전문가(비즈니스팀)와 개발자 사이의 언어 장벽</strong>이다. "이자율 산정"을 개발자는 단순 계산 함수로 이해하지만, 은행 도메인 전문가는 복잡한 금융 규정과 예외 케이스를 포함한 업무 규칙으로 이해한다.

DDD는 이 간극을 메우기 위해:
1. 도메인 전문가와 개발자가 <strong>동일한 용어(유비쿼터스 언어)</strong>를 사용
2. 비즈니스 개념을 <strong>코드의 클래스·메서드명과 일치</strong>시킴
3. 시스템을 <strong>경계가 명확한 컨텍스트(Bounded Context)</strong> 로 분리

<strong>DDD 없으면 발생하는 문제</strong>:
- 빈약한 도메인 모델(Anemic Domain Model): 비즈니스 로직이 서비스 레이어에 난잡하게 분산
- 거대한 단일 모델(Big Ball of Mud): 경계 없이 뒤엉킨 복잡도
- 코드-문서 불일치: 코드 용어와 비즈니스 용어가 달라 소통 비용 급증

- **📢 섹션 요약 비유**: DDD는 **'건축 설계에서 전문 용어를 건축주와 설계사가 공유하는 것'** 과 같습니다. "내력벽"이 무엇인지 건축주가 알아야 "내력벽 허물지 마세요"라는 요구사항을 정확히 전달할 수 있습니다. 용어가 달리면 벽을 허물어 집이 무너집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. DDD 핵심 빌딩 블록

```text
DDD 전술적 패턴 (Tactical Patterns)

  +-------------------------------------------------------------+
  |                      Aggregate Root                         |
  |  +--------------+   +--------------+   +---------------+   |
  |  |    Entity    |   |  Value Object |   |    Domain     |   |
  |  | (식별자 있음) |   | (식별자 없음) |   |    Event      |   |
  |  |  Order       |   |  Money       |   | OrderPlaced   |   |
  |  |  Customer    |   |  Address     |   | PaymentDone   |   |
  |  +--------------+   +--------------+   +---------------+   |
  +-------------------------------------------------------------+
           |                                        |
  +--------v--------+                    +----------v---------+
  |   Repository    |                    |   Domain Service   |
  | (영속성 추상화)  |                    | (여러 객체 협력 로직) |
  +-----------------+                    +--------------------+
```

| 빌딩 블록 | 설명 | 예시 |
|:---|:---|:---|
| **Entity** | 고유 식별자(ID)로 구별되는 객체 | `Order(id=1)`, `Customer(id=42)` |
| **Value Object** | 값으로 동일성을 정의하는 불변 객체 | `Money(100, "KRW")`, `Address` |
| <strong>Aggregate</strong> | 하나의 일관성 경계를 형성하는 Entity+VO 집합 | Order = 주문 + 주문 항목들 |
| <strong>Aggregate Root</strong> | Aggregate의 진입점; 외부는 Root만 접근 | `Order` (OrderItem은 직접 접근 불가) |
| **Repository** | Aggregate 영속성(저장·조회) 추상화 | `OrderRepository.findById()` |
| <strong>Domain Event</strong> | 도메인에서 일어난 사실 표현 | `OrderPlaced`, `PaymentReceived` |
| <strong>Domain Service</strong> | 단일 Entity에 속하지 않는 비즈니스 로직 | `TransferService.transfer(from, to)` |

### 2. 전략적 패턴: Bounded Context + Context Map

```text
컨텍스트 맵 (Context Map) 예시

  +-----------------+          +-----------------+
  |  주문 컨텍스트   |          |  배송 컨텍스트   |
  |  (Order BC)     | --ACL--► |  (Delivery BC)  |
  |                 |          |                 |
  |  Customer       |          |  Shipment       |
  |  Order          |          |  TrackingNumber  |
  +-----------------+          +-----------------+
          |                            |
    Anti-Corruption Layer             |
    (언어 변환: Customer->Recipient)    |
          |                            |
  +-------v----------------------------v--+
  |  결제 컨텍스트 (Payment BC)            |
  |  Payment, Invoice, Refund            |
  +---------------------------------------+
```

- **📢 섹션 요약 비유**: Bounded Context는 **'사내 각 부서의 전문 언어 영역'** 과 같습니다. 영업팀의 "고객(C고객)"과 배송팀의 "수령인(Recipient)"은 같은 사람이지만 다른 용어로 불립니다. 부서 간 경계(Bounded Context)가 없으면 한 단어가 여러 의미를 갖게 되어 혼란이 생깁니다.

---

## Ⅲ. 비교 및 연결

### DDD와 MSA의 연관

DDD의 Bounded Context가 MSA의 서비스 경계와 자연스럽게 매핑된다.

| DDD 개념 | MSA 대응 |
|:---|:---|
| Bounded Context | 마이크로서비스 경계 |
| Aggregate Root | 서비스의 핵심 도메인 객체 |
| Domain Event | 서비스 간 이벤트 메시지 (Kafka 등) |
| Repository | 서비스별 독립 DB |
| Context Map | 서비스 간 통신 계약 (API, 메시지) |

### 전술적 vs. 전략적 DDD

| 구분 | 범위 | 주요 패턴 |
|:---|:---|:---|
| <strong>전술적 DDD</strong> | 단일 BC 내부 구현 | Entity, VO, Aggregate, Repository, Domain Service |
| <strong>전략적 DDD</strong> | 전체 시스템 설계 | Bounded Context, Context Map, Ubiquitous Language |

- **📢 섹션 요약 비유**: 전략적 DDD는 **'도시 구역 설계(구역 나누기)'**, 전술적 DDD는 **'각 구역 안의 건물 설계(방 배치)'** 입니다. 먼저 주거·상업·공업 구역을 나눈(Bounded Context) 후, 각 건물 내부를 설계(Entity·Aggregate)합니다.

---

## Ⅳ. 실무 적용 및 실무자 판단

### DDD 적용 판단 기준

<strong>DDD 적합 상황</strong>:
- 복잡한 비즈니스 규칙 (금융·의료·보험·물류)
- 도메인 전문가와 긴밀한 협업이 가능한 환경
- 장기 유지보수·확장이 예상되는 핵심 시스템

<strong>DDD 불필요 상황</strong>:
- 단순 CRUD (게시판, 쇼핑 카탈로그 조회)
- 빠른 프로토타이핑 필요 (MVP)
- 도메인 전문가 협업이 어려운 환경

### 안티패턴

<strong>빈약한 도메인 모델(Anemic Domain Model)</strong>: Entity가 getter/setter만 가진 데이터 백(Data Bag)으로 전락하고, 모든 비즈니스 로직이 Service 레이어에 몰린 상태. DDD 용어를 쓰지만 실질적으로는 트랜잭션 스크립트 패턴이다.

<strong>Aggregate 경계 과도한 확장</strong>: 하나의 Aggregate에 너무 많은 Entity를 묶으면 동시성 충돌(낙관적 잠금 실패)과 DB 부하가 발생한다. Aggregate는 강한 일관성이 필요한 최소 단위로만 묶어야 한다.

- **📢 섹션 요약 비유**: 빈약한 도메인 모델은 <strong>'은행 직원(Entity)이 계좌번호만 가지고 아무것도 못 하고, 은행장(Service)이 모든 일을 직접 처리하는 것'</strong> 과 같습니다. 직원이 할 수 있는 일(이자 계산, 잔액 확인)은 직원이 해야 합니다.

---

## Ⅴ. 기대효과 및 결론

DDD를 적용하면 코드가 비즈니스 언어와 일치하게 되어, 도메인 전문가와 개발자가 <strong>동일한 모델을 보며 소통</strong>할 수 있다. Bounded Context로 복잡도가 격리되며, 각 컨텍스트는 독립적으로 발전·배포할 수 있어 MSA와 자연스럽게 결합한다.

**한계**: DDD는 학습 곡선이 가파르고, 도입 초기 오버헤드가 크다. 잘못 적용하면 오히려 복잡도를 높인다. 단순한 시스템에는 Active Record 패턴이나 Transaction Script가 더 실용적이다.

DDD는 "코드를 비즈니스처럼 만드는 것"이 아니라, **"비즈니스와 코드가 같은 언어를 쓰게 만드는 것"** 이라는 관점으로 이해해야 한다.

- **📢 섹션 요약 비유**: DDD는 **'의사와 환자가 같은 의학 용어를 공유하도록 하는 것'** 입니다. 의사가 "혈압이 높습니다"가 아니라 "BP 160/100"이라고만 말하면 환자(도메인 전문가)는 이해 못합니다. 코드도 비즈니스 언어로 말해야 소통이 됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>유비쿼터스 언어 (Ubiquitous Language)</strong> | DDD의 핵심; 개발자+도메인 전문가 공통 용어 |
| <strong>바운디드 컨텍스트 (Bounded Context)</strong> | MSA 서비스 분리 기준; 언어·모델의 적용 경계 |
| <strong>이벤트 소싱 (Event Sourcing)</strong> | 도메인 이벤트를 상태 변경의 기록으로 사용 |
| <strong>CQRS (Command Query Responsibility Segregation)</strong> | 명령(쓰기)와 조회(읽기) 모델 분리; DDD와 자주 결합 |
| <strong>MSA (Microservices Architecture)</strong> | Bounded Context -> 서비스 경계의 자연스러운 매핑 |

### 📈 관련 키워드 및 발전 흐름도

```text
모놀리식 아키텍처 -> 복잡도 증가 -> 유지보수 어려움
    |
    v
DDD (Domain-Driven Design, 2003 Eric Evans)
    |
    +-► 전략적 패턴: Bounded Context / Context Map
    +-► 전술적 패턴: Entity / VO / Aggregate / Repository
    |
    v
유비쿼터스 언어 — 코드와 도메인 언어 일치
    |
    v
MSA 서비스 분리 기준으로 Bounded Context 활용
    |
    v
CQRS + 이벤트 소싱 — 도메인 이벤트 기반 아키텍처
```

### 👶 어린이를 위한 3줄 비유 설명

1. DDD는 **'개발자와 회사 전문가가 같은 단어로 이야기하는 방법'** 이에요. "주문"이 코드에도 "Order"로 나오고, 회의에서도 "Order"라고 부르면 서로 오해가 없어요!
2. 회사를 "주문팀", "배송팀", "결제팀"으로 나누듯, 소프트웨어도 <strong>경계(Bounded Context)</strong> 를 나눠서 각자 독립적으로 일할 수 있게 해요.
3. 마이크로서비스를 어떻게 나눌지 모를 때 <strong>DDD의 경계가 바로 서비스 분리 기준</strong>이 되어서, 클라우드 시대의 핵심 설계 방법론이 됐어요!
