+++
title = "785. 마이크로서비스 데이터 일관성 결과적 일관성 확보"
date = "2026-03-15"
weight = 785
[extra]
categories = ["Software Engineering"]
tags = ["MSA", "Data Consistency", "Eventual Consistency", "Saga Pattern", "Distributed Systems", "Base Theory"]
+++

# 785. 마이크로서비스 데이터 일관성 결과적 일관성 확보

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 마이크로서비스 아키텍처(MSA) 환경에서 데이터베이스(DB)가 물리적으로 분산됨에 따라, 분산 트랜잭션(2PC)의 락(Lock) 기반 강한 일관성(Strong Consistency)을 포기하고 **BASE (Basically Available, Soft-state, Eventual consistency)** 이론에 기반하여 시스템의 가용성과 분산 처리 성능을 극대화하는 전략이다.
> 2. **가치**: **CAP 정리**에서 일관성(C)을 희생하고 가용성(A)과 파티션 내성(P)을 선택함으로써, 거대한 규모의 트래픽을 처리 가능하게 하며, 서비스 간 결합도를 낮춰(Coupling Loosening) 독립적인 배포와 확장성을 확보한다.
> 3. **융합**: Saga 패턴, Event Sourcing (이벤트 소싱), CQRS (Command Query Responsibility Segregation) 등의 패턴과 결합하여 데이터 일관성을 보장하며, 최근에는 금융권 등 높은 무결성이 요구되는 영역까지 적용 범위가 확장되고 있다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 정의 및 철학
**결과적 일관성(Eventual Consistency)**이란 분산 시스템에서 데이터 갱신이 즉시 모든 노드에 반영되지 않더라도, "결국에는" 모든 복제본이 동일한 상태로 수렴한다는 보장을 하는 데이터 모델입니다. 이는 **WAL (Write-Ahead Logging)**이나 **2PC (Two-Phase Commit)** 방식이 가진 동기식 락(Lock)의 한계를 극복하기 위해 제안되었습니다. 데이터의 정합성을 '트랜잭션 내부'가 아닌 '시간의 축(Time Axis)' 위에서 해결하며, 시스템은 일시적으로 불일치한 상태(Inconsistent State)를 허용하나 최종적으로는 비즈니스적으로 허용 가능한 상태로 수렴되도록 설계됩니다.

### 2. 등장 배경: Monolith에서 MSA로의 패러다임 시프트
- **① 기존 한계 (Monolithic) 단일 DB 시대**: 모든 트랜잭션이 하나의 DBMS(Database Management System) 내부에서 **ACID (Atomicity, Consistency, Isolation, Durability)** 속성을 보장받았음. 분산 트랜잭션이 필요한 경우 **2PC (Two-Phase Commit)**와 같은 강력한 동기화 프로토콜을 사용했으나, 이는 네트워크 병목 및 Single Point of Failure (SPOF) 문제를 야기함.
- **② 혁신적 패러다임 (MSA & Cloud)**: **MSA (Microservice Architecture)**의 도입으로 서비스마다 독립적인 DB를 가지게 되면서(Database per Service), 하나의 트랜잭션 관리자가 존재하지 않게 됨. 이에 따라 시스템의 확장성(Scalability)과 가용성(Availability)을 위해 트랜잭션의 원자성을 포기하고 비동기 메시지 기반의协调(Coordination)을 지향하게 됨.
- **③ 현재 비즈니스 요구**: 대용량 트래픽 처리와 24/7 서비스 가용성이 필수가 되면서, '즉시성'보다는 '최종적 완결성'과 '고가용성'을 우선시하는 **클라우드 네이티브(Cloud-Native)** 환경에 최적화된 모델로 자리 잡음.

### 3. 핵심 이론 배경: BASE 이론
관계형 데이터베이스(RDBMS)의 전통적인 ACID와 대비되는 개념으로, 분산 시스템을 위한 **BASE (Basically Available, Soft-state, Eventually consistent)** 이론이 근간이 됩니다.

### ASCII: 데이터 정합성의 시간적 흐름 비교

```text
[시간 축 (T)]─────────────────────────────────────────────────────────────▶

[ACID (Strong Consistency)]
   ───▶ (트랜잭션 시작) ───▶ [Lock 걸림] ───▶ [모든 DB 반영 및 검증] ───▶ (Commit) ───▶
                          └───────────────────┤
                                             짧은 순간에 '완벽한 일치' 확보
                                             (반면, Lock 기간 중 다른 트랜잭션 대기 발생)

[BASE (Eventual Consistency)]
   ───▶ (요청) ───▶ [DB A 업데이트] ───▶ (비동기 메시지) ───▶ [DB B 업데이트] ... ▶ (수렴)
        │            │                                │
        │            ▼                                ▼
     일단 반영     상태 불일치 구간              일치 상태 복구
                 (Soft State)                  (Consistent State)

→ "결과적 일관성"은 불일치 구간(Inconsistency Window)을 허용하여
   시스템의 전체적인 처리량(Throughput)을 극대화함.
```

### 📢 섹션 요약 비유
마치 택배 시스템에서 집하장에서 물건을 분실하지 않고 배송하기 위해, 모든 트럭이 중앙 집중식으로 한 곳에 모여서 검사(Strong Consistency)를 받는 대신, 각 지역 센터는 독립적으로 물건을 싣고 내리고, 추적 시스템을 통해 최종적으로 집으로 배송(송장 완료)되는 것과 같습니다. 과정 중에는 물건이 트럭에 실려 있는 '중간 상태'가 존재하지만, 결국에는 제자리로 도달합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석

| 요소명 | 역할 | 내부 동작 메커니즘 | 주요 프로토콜/기술 | 비유 |
|:---:|:---|:---|:---|:---|
| **Local Transaction** | 개별 서비스의 DB 변경을 책임짐 | 각 서비스는 자신의 DB에 한해 ACID를 보장하며 커밋 수행 | JDBC, JPA, ORM | 독립 국가의 국내법 |
| **Event Bus** | 서비스 간 느슨한 연결 제공 | 메시지 큐(MQ)를 통해 비동기적으로 이벤트를 발행(Publish)하고 구독(Subscribe) | **AMQP (Advanced Message Queuing Protocol)**, Kafka | 우편함 |
| **Saga Coordinator** | 트랜잭션 흐름 제어 | 오케스트레이션(Orchestration) 방식에서 전체 흐름을 관리하고 실패 시 보상 로직 수행 지시 | State Machine, Engine | 지휘자 |
| **Compensating Transaction** | 실패 시 롤백(Rollback) 대행 | 이미 완료된 이전 단계의 작업을 취소하는 논리적 연산 (DB Row delete or Update) | SDK로 구현된 로직 | 취소 규정 |
| **Idempotency Key** | 중복 처리 방지 | 네트워크 오류로 인한 재시도 시, 이미 처리된 메시지인지 식별하여 중복 실행 방지 | UUID, Header Token | 영수증 번호 |

### 2. Saga 패턴의 핵심 동작 원리
결과적 일관성을 구현하는 대표적인 패턴인 **Saga (Saga Pattern)**는 로컬 트랜잭션의 시퀀스로 구성됩니다.

#### ASCII: Saga 패턴 오케스트레이션 (Orchestration) 아키텍처

```text
    [Order Service]          [Payment Service]         [Stock Service]
    (주문 생성)               (결제 처리)               (재고 확보)
         │                         │                         │
         │ ① Create Order          │                         │
         ├───────────────────────────────────────────────────▶│
         │                         │                         │
         │                         │ ② Process Payment       │
         │                         ├─────────────────────────▶│
         │                         │                         │
         │                         │         [FAIL!]         │
         │                         │      (결제 실패/잔액부족)│
         │                         │                         │
         │                         │                         │
         │ ③ Compensate            │◀────────────────────────┤
         │    (Cancel Order)       │                         │
         │◀─────────────────────────┘                         │
         ▼                         ▼                         ▼
      ROLLBACK                  (완료됨)                  (미실행)
```

#### [해설]
위 다이어그램은 **오케스트레이션(Orchestration)** 스타일의 Saga 패턴을 도식화한 것입니다. 중앙의 **Saga Coordinator**(예: Order Service의 Aggregate Root)가 각 단계를 호출합니다.
1. **정상 흐름(Normal Flow)**: Order → Payment → Stock 순서로 로컬 트랜잭션이 실행됩니다.
2. **실패 처리(Failure Handling)**: 단계 2(Payment)에서 실패가 발생하면, Saga Coordinator는 이미 완료된 단계 1의 **보상 트랜잭션(Compensating Transaction)**을 호출하여 전체를 원상 복구합니다. 이는 ACID의 롤백과 달리 '논리적 취소'이므로, 시스템 설계 시 반드시 취소 가능한 로직으로 설계되어야 합니다.

### 3. 핵심 알고리즘: 트랜잭션 처리 로직 (Pseudo-code)

```python
# 결과적 일관성을 위한 Saga Orchestrator 로직 예시
class OrderSaga:
    def execute_order(self, order_data):
        transaction_log = []  # 트랜잭션 이력 로그
        
        try:
            # Step 1: 주문 생성 (Local Transaction)
            order_id = self.order_service.create(order_data)
            transaction_log.append("ORDER_CREATED")
            
            # Step 2: 결제 시도 (Remote Service Call)
            payment_result = self.payment_service.process(order_id, order_data.amount)
            if not payment_result.success:
                raise PaymentFailedException("Insufficient funds")
            transaction_log.append("PAYMENT_SUCCESS")
            
            # Step 3: 재고 확보 (Remote Service Call)
            stock_result = self.stock_service.decrease(order_id, order_data.items)
            transaction_log.append("STOCK_DECREASED")
            
            return "COMPLETED"
            
        except Exception as e:
            # 실패 시 보상 트랜잭션 실행 (Compensation)
            self.compensate(transaction_log)
            return "FAILED"

    def compensate(self, logs):
        # 역순으로 보상 트랜잭션 실행
        if "PAYMENT_SUCCESS" in logs:
            self.payment_service.cancel(order_id)  # 환불 로직
        if "ORDER_CREATED" in logs:
            self.order_service.cancel(order_id)    # 주문 취소 로직
```

### 📢 섹션 요약 비유
여러 사람이 손을 잡고 줄을 서서 통행하는(ACID) 대신, 각자가 약속된 장소로 이동한 후 누군가 실패하면 연락을 받고 제자리로 돌아오는(Saga) '산악 회화(Protocol)'와 같습니다. 전체가 하나의 거대한 밧줄로 묶여 있으면 하나가 걸려 넘어질 때 전체가 무너지지만, 별도로 움직이며 연락하는 방식은 개별의 사고가 전체의 멈춤을 유발하지 않습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: ACID vs BASE

| 구분 | ACID (RDBMS 중심) | BASE (MSA/NoSQL 중심) |
|:---:|:---|:---|
| **일관성(Consistency)** | **강한 일관성 (Strong)**: 트랜잭션 내에서 데이터는 항상 일치해야 함. | **결과적 일관성 (Eventual)**: 시스템의 안정 상태에서만 데이터 일치. |
| **원자성(Atomicity)** | All-or-Nothing: 모두 성공하거나 모두 실패. | None: 각 로컬 트랜잭션은 독립적 실패 가능 (보상 필요). |
| **격리성(Isolation)** | 락(Lock)을 통한 직렬성 보장. | 격리 수준이 낮을 수 있음 (동시성 높임, 충돌 가능). |
| **지연시간(Latency)** | 높음 (동기식 통신, 락 대기 시간). | **낮음** (비동기식 통신, 즉시 응답). |
| **가용성(Availability)** | 낮음 (장애 발생 시 서비스 전체 중지). | **높음** (일부 장애에도 서비스 지속). |

### 2. 과목 융합 관점: CAP 이론과 네트워크
**CAP 정리**에 따르면 분산 시스템은 일관성(Consistency), 가용성(Availability), 파티션 내성(Partition tolerance) 중 최대 두 가지만 만족시킬 수 있습니다. 결과적 일관성은 명시적으로 일관성(C)을 포기하여 가용성(A)과 파티션 내성(P)을 선택한 **AP 시스템**에 해당합니다.
- **네트워크 분산(Network Partition) 발생 시**: 시스템은 서비스를 멈추고 데이터 불일치를 막는 대신(C), 계속 요청을 받아 처리하여(A) 나중에 동기화합니다. 이는 **TCP (Transmission Control Protocol)**보다 **UDP (User Datagram Protocol)**의 특성에 가깝습니다.

### 3. 기술적 시너지: Event Sourcing (이벤트 소싱)
결과적 일관성은 **Event Sourcing** 패턴과 결합할 때 강력해집니다. 현재 상태(State)를 저장하는 것이 아니라, 상태 변화의 **이벤트(Event)**만을 기록함으로써, 데이터 불일치가 발생했을 때 과거의 모든 이벤트 스트림을 재생하여 상태를 복구하거나, 시스템 장애 지점을 정밀하게 파악할 수 있습니다.

### ASCII: 상태 저장 vs 이벤트 저장 비교

```text
[State-Based Approach (Traditional)]
Database: { "Balance": 10,000원 }
   │
   └──▶ 문제: '10,000원'이 어떤 과정으로 되었는지 알 수 없음.
               (Update 시 이전 데이터 덮어쓰기)

[Event-Based Approach (Event Sourcing)]
Event Store: [ +10000(Order) ] -> [ -3000(Pay) ] -> [ -5000(Cancel) ]
   │
   └──▶ 이점: 모든 히스토리 보존. 현재 상태는 스냅샷.
               재연산을 통해 일관성 복구 및 감사 추적 가능.
```

### 📢 섹션 요약 비유
마치 은행장부에서 잔액만 적는 '장부' 방식(State)에서, 영수증을 발행할 때마다 증빙 서류를 쏟아내고 나중에 이것을 순서대로 더해 계산하는 '현금 흐름표' 방식(Event)으로 바뀌는 것과 같습니다. 영수증(이벤트)이 쌓이면 잔�