+++
title = "252. Saga 패턴 - MSA 환경의 유연한 결합"
date = "2026-03-16"
[extra]
categories = "studynote-database"
id = 252
+++

# 252. Saga 패턴 - MSA 환경의 유연한 결합

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Saga 패턴은 분산된 여러 마이크로서비스(Microservices)에 걸친 긴 트랜잭션(Long Lived Transaction)을 처리하기 위해, **각 서비스별 로컬 트랜잭션(Local Transaction)을 순차적으로 실행하고 실패 시 보상 트랜잭션(Compensating Transaction)을 통해 데이터 정합성을 복원하는 패턴**이다.
> 2. **가치**: 2단계 커밋(2PC, Two-Phase Commit)의 락(Lock)에 의한 병목 문제를 해결하여 시스템의 **가용성(Availability)과 성능(TPS)을 극대화**하며, 분산 환경에서 '결과적 일관성(Eventual Consistency)' 모델을 안정적으로 구현한다.
> 3. **융합**: 이벤트 주도 아키텍처(EDA, Event-Driven Architecture) 및 메시지 브로커(Kafka 등)와 결합되어, 복잡한 비즈니스 프로세스를 비동기적으로 조율하는 현대 MSA의 표준 트랜잭션 관리 전략으로 자리 잡았다.

---

### Ⅰ. 개요 (Context & Background)

분산 트랜잭션 처리의 역사는 **ACID(Atomicity, Consistency, Isolation, Durability)** 특성을 보장하려는 노력과, 이로 인한 성능 저하를 극복하려는 노력의 연속이었습니다. 전통적인 **RDBMS(Relational Database Management System)** 환경에서는 **X/Open XA** 표준 기반의 **2PC(Two-Phase Commit)** 프로토콜이 표준으로 사용되었습니다. 그러나 MSA(Microservices Architecture)가 도입되면서 데이터가 물리적으로 분산되고, 서비스 간 통신이 네트워크를 통해 이루어지는 상황에서 2PC는 치명적인 단점을 드러냈습니다.

**2PC의 한계**: 모든 참여자가 준비(Prepare) 상태에 들어가고, 전체가 동의해야 커밋(Commit)되는 구조이므로, 단 하나의 서비스 장애나 네트워크 지연이 전체 트랜잭션을 실패로 이끌거나 시스템 전체를 멈추게 하는 '단일 장애점(SPOF, Single Point of Failure)'이 됩니다. 또한, 트랜잭션이 완료될 때까지까지 자원을 잠그는 장기간 락(Lock)은 대규모 시스템의 성능을 급격히 저하시킵니다.

**Saga의 등장**: 이러한 한계를 극복하기 위해 분산 시스템의 설계자들은 **'결과적 일관성(Eventual Consistency)'**을 타협점으로 선택했습니다. 즉, 각 순간에는 데이터가 불일치할 수 있으나, 시간이 흘러 최종적으로는 일치하는 상태로 만드는 것입니다. 1987년 헥토 가르시아-몰리나(Hector Garcia-Molina)와 케네드 사머(Kenneth Salem)가 제안한 Saga 패턴은 긴 트랜잭션을 여러 개의 짧은 로컬 트랜잭션으로 쪼개고, 모든 단계가 완료되지 않았을 때 이전 상태로 되돌리는 **보상 트랜잭션(Compensating Transaction)**을 개발자가 정의하도록 함으로써, 분산 환경에서도 높은 수준의 유연성과 성능을 확보했습니다.

> **💡 비유**: 은행 창구에서 계좌이체를 할 때, 두 은행의 데이터베이스를 동시에 묶어서 처리(2PC)하다가 한쪽이 멈추면 모든 창구가 멈추는 것보다는, 일단 출금을 하고 상대방 계좌에 입금을 시도한 뒤, 입금이 실패하면 출금했던 돈을 다시 돌려주는 후속 처리(Saga)를 하는 것이 전체 업무 처리 속도는 훨씬 빠른 것과 같습니다.

> **📢 섹션 요약 비유**: Saga 패턴의 개념은 **'복잡한 사무실 결재 라인'**과 같습니다. 대표결재자가 모든 부서 장을 한자리에 모아놓고 동시에 도장을 찍으려 기다리는 것(2PC)은 비효율적입니다. 대신, 부서 순서대로 결재를 올리다가 반려가 되면, 이미 결재된 윗선 부서에게 '반려 사유'로 결재 취소(보상)를 요청하는 방식(Saga)이 업무 흐름을 훨씬 매끄럽게 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

Saga 패턴의 핵심은 전역 트랜잭션을 세부적인 로컬 트랜잭션의 시퀀스로 정의하고, 각 단계마다 롤백을 위한 **보상 로직(Compensating Logic)**을 확보하는 것입니다. Saga 패턴은 크게 두 가지 조율(Coordination) 방식, **코레오그래피(Choreography)**와 **오케스트레이션(Orchestration)**으로 구현됩니다.

#### 1. 구성 요소 및 상세 기술

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Mechanism) | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **로컬 트랜잭션**<br>(Local Transaction) | 비즈니스 로직의 단위 | 각 서비스의 DBMS에서 독립적으로 ACID를 보장하며 실행됨. | ACID, RDBMS | 한 사람의 춤 동작 |
| **보상 트랜잭션**<br>(Compensating Transaction) | 오류 복구 메커니즘 | 로컬 트랜잭션이 수행한 변경사항을 논리적으로 취소(CRUD의 Delete/Update)하는 별도의 API. | REST API, gRPC | 춤 동작 되돌리기 |
| **이벤트 버스 / 메시지 브로커**<br>(Event Bus) | 서비스 간 비동기 통신 | 서비스 간 느슨한 결합(Loose Coupling)을 유지하며 이벤트를 전달하고 순서를 보장함. | Apache Kafka, RabbitMQ | 소식 전달자 |
| **사가 오케스트레이터**<br>(Saga Orchestrator) | 중앙 집중형 제어자 (Orchestration 시) | 트랜잭션의 전체 상태(State)를 관리하고, 각 참여자에게 명령(Command)을 내리며 보상을 지시함. | State Machine, Executor | 지휘자 |
| **이벤트 채널**<br>(Event Channel) | 분산형 제어 매개체 (Choreography 시) | 서비스가 자신의 상태 변경(Domain Event)을 발행(Publish)하면, 관련 서비스가 이를 구독(Subscribe)하여 행동. | Publish-Subscribe 패턴 | 암시적 신호 |

#### 2. 아키텍처 비교 및 ASCII 다이어그램

Saga 패턴의 두 가지 주요 구현 방식인 **코레오그래피(Choreography, 무용 연기)**와 **오케스트레이션(Orchestration, 관현악)**은 상호 작용 방식에서 큰 차이를 보입니다.

```text
[Type A] Choreography (분산형 이벤트 주도)

 [Order Service] ──(1) OrderCreated ──┐
     ▲                               ▼
     │          (3) PaymentFailed   [Payment Service]
     │                               │
     │          (2) ReserveStock     ▼
 [Inventory Service] ◀─────────── [Stock Event Bus]
     │
(4) Compensate Stock (Rollback)

* 특징: 중앙 통제자 없음. 각 서비스는 이벤트만 듣고 스스로 판단.
* 장점: 결합도가 낮음. 단일 실패점 없음.
* 단점: 전체 흐름 파악 어려움. 순환 의존성 위험.
```

```text
[Type B] Orchestration (중앙 집중형 제어)

             [Saga Orchestrator]
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
  ① Execute    ② Execute      ③ Execute
 [Order Svc]  [Payment Svc]  [Inventory Svc]
       ▲             │             │
       │    (Fail)   ▼             │
       │   ◀─────────┘             │
       │                           │
       │ ──── ④ Compensate ────────┘
       │      (Rollback Command)
       ▼
    [End]

* 특징: 오케스트레이터가 모든 상태와 로직을 가짐.
* 장점: 흐름 제어 용이, 복잡한 비즈니스 로직 구현에 적합.
* 단점: 오케스트레이터가 병목이 될 수 있음.
```

#### 3. 심층 동작 원리 및 메커니즘

Saga의 핵심은 **'보상(Compensation)'**입니다. 일반적인 트랜잭션의 롤백(Rollback)이 DBMS 수준에서 물리적으로 원복(Undo Log 등 사용)하는 것이라면, Saga의 보상은 비즈니스 로직 차원에서의 논리적 취소 작업입니다.

1.  **진행(Forward)**: 클라이언트의 요청에 따라 Saga가 시작되면, `Tx1 → Tx2 → Tx3` 순서대로 로컬 트랜잭션을 커밋합니다. 각 단계가 완료될 때마다 시스템의 상태는 변경되며, 이전 단계는 더 이상 롤백될 수 없다는 전제를 가집니다(이미 사용자에게 노출되었을 수 있음).
2.  **실패 감지(Failure Detection)**: `Tx3` 수행 중 네트워크 오류나 비즈니스 규칙 위배(잔액 부족 등)가 발생하여 트랜잭션이 실패하면, Saga 코디네이터는 이를 즉시 감지합니다.
3.  **보상(Backward)**: 실패가 감지되면,Saga는 즉시 역방향으로 `Compensate Tx2 → Compensate Tx1` 순서로 보상 트랜잭션을 실행합니다. 이를 통해 시스템은 `Tx1` 실행 전의 상태 혹은 비즈니스적으로 타협된 상태로 복귀합니다.
4.  **로그 및 중복 방격(Idempotency)**: 각 트랜잭션과 보상 트랜잭션의 실행 결과는 **사가 로그(Saga Log)**에 영구적으로 기록되어야 합니다. 시스템 장애로 인해 재시도(Replay)가 발생하더라도, 이미 완료된 작업을 다시 수행하지 않도록 각 API는 **멱등성(Idempotency)**을 보장해야 합니다.

```text
[Saga State Management Flow]

 1. [OrderSvc] Tx: CREATE_ORDER
    └─ DB Commit (State: ORDERED)
    
 2. [PaymentSvc] Tx: PAY_REQUEST
    └─ DB Commit (State: PAID) 
    └─ FAILURE Occurs (e.g., Fraud Detected)
    
 3. [Saga Manager] Detects Failure
    └─ Trigger Compensation
    
 4. [PaymentSvc] Cmp: REFUND_PAYMENT (Logic: Update status to CANCELLED)
    └─ DB Commit
    
 5. [OrderSvc] Cmp: CANCEL_ORDER (Logic: Delete order record)
    └─ DB Commit (State: CANCELLED)

*Result: System is safely reverted to a consistent initial state.
```

#### 4. 핵심 알고리즘 및 코드 스니펫

아래는 Saga 오케스트레이션을 구현할 때, 상태 전이를 관리하는 전형적인 State Machine 코드의 개념적 예시입니다.

```python
# Pseudocode: Saga Orchestrator State Machine
class OrderSaga:
    def __init__(self):
        self.current_state = "START"
        self.steps = [
            {"service": "payment", "action": "approve_payment", "compensate": "refund_payment"},
            {"service": "inventory", "action": "reserve_stock", "compensate": "release_stock"}
        ]

    def run(self):
        executed_steps = []
        try:
            for step in self.steps:
                # 1. Execute Local Transaction
                response = call_service(step['service'], step['action'])
                executed_steps.append(step)
                
                # 2. Check Business Rule
                if not response.success:
                    raise TransactionFailedException(f"{step['service']} failed")
            
            # All steps success
            self.current_state = "COMPLETED"
            
        except Exception as e:
            # 3. Execute Compensating Transactions in Reverse Order
            self.current_state = "COMPENSATING"
            for step in reversed(executed_steps):
                call_service(step['service'], step['compensate'])
            
            self.current_state = "ABORTED"
            raise e
```

> **📢 섹션 요약 비유**: Saga의 동작 원리는 **'여행자의 여행 계획'**과 같습니다. 비행기 ✈️ → 기차 🚆 → 호텔 🏨 순서대로 예약을 진행하다가, 마지막 호텔 예약이 불가능하다면, 여행자는 기차 표를 취소하고 환불받은 뒤(Compensate), 비행기 표도 취소해야 합니다. 이미 갔던 경로를 거슬러 내려오며 원상복구하는 과정이 필수적입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

Saga 패턴은 분산 시스템 설계에서 **CAP 정리**(Consistency, Availability, Partition tolerance)의 **AP(availability + Partition tolerance)** 영역에 속하는 전략입니다.

#### 1. 심층 기술 비교표: Saga vs 2PC

| 비교 항목 | Saga 패턴 | 2PC (Two-Phase Commit) |
|:---|:---|:---|
| **일관성 모델** | **결과적 일관성 (Eventual Consistency)**<br>일시적 불일치 허용, 최종 일치 | **강한 일관성 (Strong Consistency)**<br>트랜잭션 내내 무결성 보장 |
| **락(Lock) 범위** | 짧은 시간 동안 로컬 리소스만 락 (높은 동시성) | 트랜잭션 시작부터 커밋까지 전체 참여자 리소스 락 |
| **성능 (TPS)** | **높음** (비동기 처리 가능, 대기 시간 최소화) | **낮음** (모든 참여자의 응답 대기 필요, 병목 발생) |
| **장애 격리** | 우수 (다른 서비스 장애가 전체 트랜잭션을 즉시 멈추지 않음) | 취약 (하나의 참여자 장애로 전체 트랜잭션 실패) |
| **구현 복잡도** | **높음** (보상 로직, 멱등성, 사이드 이펙트 관리 필요) | 낮음 (