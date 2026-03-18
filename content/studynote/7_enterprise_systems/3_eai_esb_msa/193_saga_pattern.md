+++
title = "사가 패턴 (Saga Pattern)"
description = "MSA 환경에서 긴 트랜잭션 보장, 각 서비스의 로컬 트랜잭션을 연속적으로 실행하고, 중간 실패 시 역순으로 보상 트랜잭션(Compensating Transaction)을 발행해 논리적 롤백 수행 (Eventual Consistency 보장)"
weight = 193
+++
# 사가 패턴 (Saga Pattern)

> **약어 (Abbreviation)**: Saga (Long-running transaction pattern for distributed systems)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사가 패턴 (Saga Pattern)은 분산 환경에서 **ACID 트랜잭션의 대안**으로, 각 서비스의 로컬 트랜잭션을 순차적으로 실행하고 중간 실패 시 **보상 트랜잭션 (Compensating Transaction)**을 통해 논리적 롤백을 수행하여 **Eventual Consistency (결과적 일관성)**를 보장하는 패턴이다.
> 2. **가치**: MSA (Microservice Architecture) 환경에서 **2PC (Two-Phase Commit)**의 블로킹·SPOF (Single Point of Failure)·확장성 문제를 회피하면서도, 비즈니스적 일관성을 유지할 수 있는 유일한 실용적인 분산 트랜잭션 관리 기법이다.
> 3. **융합**: Saga는 **이벤트 소싱 (Event Sourcing)**·**CQRS (Command Query Responsibility Segregation)**·**트랜잭셔널 아웃박스 (Transactional Outbox)** 패턴과 결합하여 현대 엔터프라이즈 MSA의 트랜잭션 관리 표준 아키텍처로 자리 잡았다.

---

## Ⅰ. 개요 (Context & Background)

- **개념**: 사가 패턴 (Saga Pattern)은 **분산 트랜잭션 (Distributed Transaction)**을 여러 개의 독립적인 **로컬 트랜잭션 (Local Transaction)**으로 분해하고, 각 로컬 트랜잭션이 성공할 때마다 다음 단계를 호출하는 체인 방식으로 실행한다. 중간 단계에서 실패가 발생하면, 이미 완료된 이전 단계들의 **보상 트랜잭션 (Compensating Transaction)**을 역순으로 실행하여 전체를 롤백한다. 이 방식은 **결과적 일관성 (Eventual Consistency)**을 허용하는 비즈니스에만 적용 가능하다.

- **💡 비유**: 사가 패턴은 "여행 예약 취소 정책"과 같다. 비행기 ✓, 호텔 ✓, 렌터카 ✗ (실패)일 경우, 시스템은 자동으로 "이미 예약된 호텔 예약 취소 → 이전 예약된 비행기 예약 취소" 순서로 롤백을 실행하여, 모든 예약이 원래 상태로 돌아가게 한다.

- **등장 배경 및 발전 과정**:
  1. **2PC (Two-Phase Commit)의 근본적 한계**: 전통적인 분산 트랜잭션 코디네이터인 2PC는 **Prepare (준비)** 단계에서 모든 참여자가 잠금 (Lock)을 유지해야 하므로, **롱 트랜잭션 (Long Transaction)** 환경에서 **교착 상태 (Deadlock)**·**리소스 병목**·**SPOF (Single Point of Failure)** 문제가 발생한다. MSA 환경에서는 수십 개의 서비스가 참여하는 트랜잭션이 일상적이므로 2PC는 실용적이지 않다.
  2. **CAP 정리의 결과적 일관성 수용**: 분산 시스템에서 **일관성 (Consistency)**·**가용성 (Availability)**·**분단 내성 (Partition Tolerance)**을 동시에 만족할 수 없다. 사가는 **A + P**를 선택하고, C를 **결과적 일관성 (Eventual Consistency)**으로 완화한다.
  3. **MSA 트랜잭션 관리의 표준 패턴으로 부상**: 1987년 Hector Garcia-Molina & Kenneth Salem이 처음 제안한 후, 2010년대 MSA 붐과 함께 **Netflix Conductor**·**Apache Camel**·**Seata**·**Narayana** 등의 오픈소스 프레임워크가 등장하며 실무 표준으로 자리 잡았다.

### 2PC vs Saga 트랜잭션 비교 다이어그램

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │                   2PC vs Saga 트랜잭션 비교                       │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [2PC (Two-Phase Commit) - 블로킹 방식]                          │
  │                                                                   │
  │    Coordinator ───[1] Prepare ──→ Service A (Lock)               │
  │         │             └──────→ Service B (Lock)                  │
  │         │             └──────→ Service C (Lock)                  │
  │         │                                                        │
  │         │    ←──[2] All Ready (Blocking!)                        │
  │         │                                                        │
  │         │    [3] Commit (All or Nothing)                         │
  │         │         → A: Commit                                   │
  │         │         → B: Commit                                   │
  │         │         → C: Commit                                   │
  │                                                                   │
  │    ⚠️  문제: 장애 발생 시 전체 트랜잭션 중단, Lock 유지 시간 길음  │
  │                                                                   │
  │  ─────────────────────────────────────────────────────────────   │
  │                                                                   │
  │  [Saga Pattern - 논블로킹 방식]                                  │
  │                                                                   │
  │    ┌─[1] Service A: Create Order ─────────→ ✓ 로컬 커밋         │
  │    │                                                        │   │
  │    ├─[2] Service B: Payment ────────────→ ✓ 로컬 커밋         │   │
  │    │                                                        │   │
  │    ├─[3] Service C: Inventory ───────────→ ✗ 실패!            │   │
  │    │                                                        │   │
  │    │   ←────────────────────────────────────────────────────┘   │
  │    │        [보상 트랜잭션 시작]                                 │
  │    │                                                            │
  │    ├─[C2] Service B: Refund Payment ────→ ✓ 보상 완료          │
  │    │                                                            │
  │    └─[C1] Service A: Cancel Order ──────→ ✓ 보상 완료          │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 2PC는 **코디네이터 (Coordinator)**가 모든 서비스에 **Prepare** 요청을 보내고, 모든 서비스가 준비(Ready)될 때까지 **대기 (Blocking)**한 뒤 일괄 **Commit**을 수행한다. 이 과정에서 한 서비스라도 응답하지 않으면 전체 트랜잭션이 중단된다. 반면, Saga는 각 서비스가 독립적으로 **로컬 트랜잭션 (Local Transaction)**을 커밋하고 다음 서비스를 호출한다. 중간에 **[3] Inventory**에서 실패가 발생하면, 이미 완료된 **[C2] Payment → [C1] Order** 순서로 **보상 트랜잭션 (Compensating Transaction)**을 실행하여 논리적 롤백을 수행한다. 이 과정은 **논블로킹 (Non-blocking)**이며, 각 서비스는 짧은 시간 동안만 리소스를 점유한다.

- **📢 섹션 요약 비유**: 2PC는 "모든 팀원이 준비될 때까지 전체 회의를 멈추고 기다리는 것"과 같아서, 한 명이라도 지연되면 전체가 멈춘다. 사가 패턴은 "각 팀원이 자신의 역할을 수행하고, 문제가 생기면 이전에 완료한 작업을 되돌리는 방식"이라서, 전체 시스템이 멈추지 않고 계속 흘러간다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **사가 오케스트레이터 (Saga Orchestrator)** | 전체 트랜잭션 흐름 제어 | 상태 기계 (State Machine)으로 단계별 호출·보상 관리 | Seata, Netflix Conductor | 지휘자 |
| **로컬 트랜잭션 (Local Transaction)** | 각 서비스의 독립적 트랜잭션 | 단일 서비스 DB 내에서 ACID 보장 | RDBMS, NoSQL | 각 악기의 연주 |
| **보상 트랜잭션 (Compensating Transaction)** | 실패 시 논리적 롤백 | 이전 로컬 트랜잭션의 역연산 수행 | Refund, Cancel API | 되감기 버튼 |
| **사가 로그 (Saga Log)** | 트랜잭션 상태 영속화 | 각 단계의 실행·보상 이력 저장 | Event Store, DB | 공책 |
| **이벤트 버스 (Event Bus)** | 서비스 간 비동기 통신 | Pub/Sub 방식으로 트랜잭션 완료 알림 | Kafka, RabbitMQ | 우편 배달부 |

---

### 사가 트랜잭션 실행 및 보상 흐름

사가 트랜잭션은 **① 정방향 실행 (Forward)** 또는 **② 보상 실행 (Compensating)** 두 가지 방향으로만 진행된다. 모든 로컬 트랜잭션이 성공하면 트랜잭션 완료 상태로 종료하고, 중간에 실패가 발생하면 보상 트랜잭션 체인을 역순으로 실행한다.

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │               사가 트랜잭션 실행 및 보상 흐름                      │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [예시: 전자상거래 주문 트랜잭션]                                 │
  │                                                                   │
  │   ① 정방향 실행 (Forward Execution)                               │
  │   ┌─────────────────────────────────────────────────────┐        │
  │   │                                                     │        │
  │   │  ┌─[T1] Order Service       │                        │        │
  │   │  │    - 주문 생성 (status=PENDING)                   │        │
  │   │  │    - 로컬 DB 커밋                                 │        │
  │   │  │    - → OrderCreatedEvent 발행                     │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   │  ┌─[T2] Payment Service      │                        │        │
  │   │  │    - 결제 승인                                     │        │
  │   │  │    - 로컬 DB 커밋                                 │        │
  │   │  │    - → PaymentAuthorizedEvent 발행               │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   │  ┌─[T3] Inventory Service    │                        │        │
  │   │  │    - 재고 차감                                     │        │
  │   │  │    - 로컬 DB 커밋                                 │        │
  │   │  │    - → InventoryReservedEvent 발행              │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   │  ┌─[T4] Shipping Service     │                        │        │
  │   │  │    - 배송 시작                                     │        │
  │   │  │    - 로컬 DB 커밋                                 │        │
  │   │  │    - → ShipmentCreatedEvent 발행                 │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   └─────────────────────────────────────────────────────┘        │
  │            결과: 트랜잭션 완료 (COMPLETED)                        │
  │                                                                   │
  │  ─────────────────────────────────────────────────────────────   │
  │                                                                   │
  │   ② 보상 실행 (Compensating Execution) - T3 실패 시              │
  │   ┌─────────────────────────────────────────────────────┐        │
  │   │                                                     │        │
  │   │  ┌─[T1] Order Service       │                        │        │
  │   │  │    → OrderCreatedEvent 발행                       │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   │  ┌─[T2] Payment Service      │                        │        │
  │   │  │    → PaymentAuthorizedEvent 발행               │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   │  ┌─[T3] Inventory Service    │                        │        │
  │   │  │    - 재고 부족! → ✗ FAILURE                      │        │
  │   │  │    → InventoryFailedEvent 발행                  │        │
  │   │  └───────────────────────────────────────────→ ✗    │        │
  │   │                                                     │        │
  │   │           [보상 트랜잭션 시작 - 역순 실행]               │        │
  │   │                                                     │        │
  │   │  ┌─[C2] Payment Service      │                        │        │
  │   │  │    ← InventoryFailedEvent 수신                    │        │
  │   │  │    - 결제 취소 (Refund)                            │        │
  │   │  │    - 로컬 DB 커밋                                 │        │
  │   │  │    - → PaymentRefundedEvent 발행                 │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   │  ┌─[C1] Order Service       │                        │        │
  │   │  │    ← PaymentRefundedEvent 수신                   │        │
  │   │  │    - 주문 취소 (status=CANCELLED)                 │        │
  │   │  │    - 로컬 DB 커밋                                 │        │
  │   │  │    - → OrderCancelledEvent 발행                  │        │
  │   │  └───────────────────────────────────────────→ ✓    │        │
  │   │                                                     │        │
  │   └─────────────────────────────────────────────────────┘        │
  │            결과: 트랜잭션 취소 (COMPENSATED)                      │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 정방향 실행에서 각 서비스는 자신의 **로컬 트랜잭션 (Local Transaction)**을 먼저 커밋한 후, 완료 이벤트를 발행한다. **[T3] Inventory Service**에서 재고 부족 실패가 발생하면, **InventoryFailedEvent**가 발행되고, 이 이벤트를 수신한 이전 서비스들이 **보상 트랜잭션 (Compensating Transaction)**을 역순으로 실행한다. **[C2] Payment**는 결제를 환불(Refund)하고, **[C1] Order**는 주문 상태를 CANCELLED로 변경한다. 모든 보상이 완료되면 트랜잭션은 **COMPENSATED** 상태로 종료된다. 이 과정은 각 서비스가 **독립적인 ACID 트랜잭션**을 유지하면서도, 전체적으로 **결과적 일관성 (Eventual Consistency)**을 달성한다.

---

### 사가 트랜잭션 상태 전이 (State Transition)

사가 트랜잭션은 **상태 기계 (State Machine)**로 표현되며, 각 상태 간 전이는 **원자적 (Atomic)**이어야 한다. 상태는 **사가 로그 (Saga Log)**에 영속화되어 시스템 장애 시에도 재개 가능하다.

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │                 사가 트랜잭션 상태 전이 (State Machine)           │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │                      ┌──────────────┐                            │
  │                 ┌────→  STARTED     ──────┐                       │
  │                 │     (트랜잭션 시작)     │                       │
  │                 │     └───────┬───────┘   │                       │
  │                 │             │           │                       │
  │                 │             ▼           │                       │
  │                 │    ┌─────────────────┐  │                       │
  │   [모든 단계    │    │  PENDING        │  │  [중간 실패]          │
  │    완료 시]     │    │  (단계 대기 중)   │  │                       │
  │                 │    └───────┬─────────┘  │                       │
  │                 │            │             │                       │
  │                 │            ▼             │                       │
  │                 │    ┌─────────────────┐  │                       │
  │                 │    │  RUNNING        │  │                       │
  │                 │    │  (로컬 트랜잭션   │  │                       │
  │                 │    │   실행 중)       │  │                       │
  │                 │    └───────┬─────────┘  │                       │
  │                 │            │             │                       │
  │            ┌────┘            └────┐        │                       │
  │            │                      │        │                       │
  │            ▼                      ▼        ▼                       │
  │    ┌──────────────┐        ┌──────────────┐                       │
  │    │  COMPLETED   │        │  COMPENSATING│                       │
  │    │  (모든 단계   │        │  (보상 실행)  │                       │
  │    │   완료)       │        └───────┬──────┘                       │
  │    └──────────────┘                │                              │
  │            ▲                        ▼                              │
  │            │                ┌──────────────┐                      │
  │            │                │ COMPENSATED  │                      │
  │            │                │ (모든 보상    │                      │
  │            │                │  완료)        │                      │
  │            │                └──────────────┘                      │
  │            │                                                        │
  │            │   [타임아웃/취소 요청]                                │
  │            │                                                        │
  │    ┌──────────────┐                                               │
  │    │   ABORTED    │                                               │
  │    │  (중단된 상태) │                                               │
  │    └──────────────┘                                               │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 사가 트랜잭션은 **STARTED** 상태로 시작하여 **PENDING** 단계를 거쳐 각 서비스의 로컬 트랜잭션을 **RUNNING** 상태에서 실행한다. 모든 단계가 성공하면 **COMPLETED**로 종료하고, 중간에 실패가 발생하면 **COMPENSATING** 상태로 전이하여 보상 트랜잭션을 역순으로 실행한 뒤 **COMPENSATED**로 종료한다. **ABORTED**는 타임아웃이나 사용자 취소로 인해 강제 중단된 상태다. 각 상태 전이는 **사가 로그 (Saga Log)**에 기록되어 장애 복구 시 **최소 한 번 (At Least Once)** 실행 보장을 제공한다.

- **📢 섹션 요약 비유**: 사가 트랜잭션은 "도미노 타워 쌓기"와 같다. 각 도미노(서비스)를 순서대로 세우다가 중간에 넘어지면(실패), 이미 세워진 도미노를 역순으로 치워(보상) 원래 상태로 만든다. 상태 전이는 "게임 저장/로드" 기능처럼 중간 지점을 저장해두었다가 실패 시 그 지점부터 다시 시작할 수 있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교 1: 2PC vs Saga

| 비교 항목 | 2PC (Two-Phase Commit) | Saga Pattern |
|:---|:---|:---|
| **트랜잭션 방식** | 원자적 (All or Nothing) | 결과적 일관성 (Eventual Consistency) |
| **잠금 (Lock) 시간** | 전체 트랜잭션 기간 유지 | 로컬 트랜잭션만 짧게 유지 |
| **코디네이터** | 중앙 코디네이터 필수 | 오케스트레이션/코레오그래피 선택 |
| **SPOF (Single Point of Failure)** | 코디네이터 장애 시 전체 중단 | 분산 상태로 복원력 우수 |
| **성능** | 롱 트랜잭션에서 병목 심각 | 논블로킹으로 높은 처리량 |
| **일관성 보장** | 강한 일관성 (Strong Consistency) | 최종적 일관성 (Eventual Consistency) |
| **구현 복잡도** | 상대적으로 간단 | 보상 로직 설계 필요 |
| **적용 가능 범위** | 짧은 트랜잭션에 적합 | 긴 트랜잭션, MSA에 적합 |

### 비교 2: Choreography vs Orchestration Saga

| 비교 항목 | 코레오그래피 (Choreography) | 오케스트레이션 (Orchestration) |
|:---|:---|:---|
| **제어 방식** | 분산 (이벤트 기반) | 중앙 집중 (오케스트레이터) |
| **서비스 독립성** | 높음 (서비스 간 느슨한 결합) | 낮음 (오케스트레이터 의존) |
| **복잡도 관리** | 어려움 (흐름 파악 어려움) | 쉬움 (중앙에서 흐름 관리) |
| **테스트/디버깅** | 어려움 (분산 추적 필요) | 쉬움 (단일 진입점) |
| **이벤트 폭증** | 가능 (모든 상태 전이 이벤트) | 제어 가능 (필요한 이벤트만) |
| **확장성** | 우수 (새 서비스 추가 용이) | 제한적 (오케스트레이터 수정) |

### 비교 3: Saga + CQRS + Event Sourcing 융합

| 패턴 | 역할 | 융합 효과 |
|:---|:---|:---|
| **Saga** | 분산 트랜잭션 관리 | 결과적 일관성 보장 |
| **CQRS** | 조회(Command) 분리 | 복잡한 조인 쿼리 최적화 |
| **Event Sourcing** | 이벤트 로그 저장 | 완전한 감사/복구 기능 |

---

### 사가 패턴의 문제점과 완화 전략 (Time, Order, Isolation)

사가 패턴은 **결과적 일관성 (Eventual Consistency)**을 허용하지만, 세 가지 근본적 문제가 존재한다. **① 시간적 간격 (Temporal Gap)**: 보상 트랜잭션 실행 전까지 일관성이 깨진 상태가 지속된다. **② 순서 보장 (Ordering)**: 비동기 메시지 전달에서 순서가 뒤바뀔 수 있다. **③ 격리 부족 (Lack of Isolation)**: 로컬 트랜잭션이 커밋되면 다른 트랜잭션이 즉시 읽을 수 있어 **더티 읽기 (Dirty Read)**·**쓰기 스큐 (Write Skew)**가 발생할 수 있다.

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │               사가 패턴의 문제점과 완화 전략                       │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  ① 시간적 간격 (Temporal Gap)                                    │
  │  ┌─────────────────────────────────────────────────────┐        │
  │  │  T1(완료) ─── 갭 ─── T2(완료) ─── 갭 ─── T3(실패)    │        │
  │  │     │                                                │        │
  │  │     └── 일관성 깨진 상태 지속 (결제 완료, 재고 미차감)  │        │
  │  │                                                      │        │
  │  │  [완화] Semantics: "주문 확인(PENDING) 상태에서는 재고   │        │
  │  │      예약만 하고, 실제 차감는 최종 확정 후 실행"         │        │
  │  └─────────────────────────────────────────────────────┘        │
  │                                                                   │
  │  ② 순서 보장 (Ordering Problem)                                  │
  │  ┌─────────────────────────────────────────────────────┐        │
  │  │  Kafka의 파티션별 순서 보장 →同一 OrderId는同一파티션 │        │
  │  │  Message Ordering: Total Order Per Partition         │        │
  │  │                                                      │        │
  │  │  [완화] Saga Log에 순서 번호(Sequence Number) 부여   │        │
  │  └─────────────────────────────────────────────────────┘        │
  │                                                                   │
  │  ③ 격리 부족 (Lack of Isolation)                                 │
  │  ┌─────────────────────────────────────────────────────┐        │
  │  │  Transaction A: 재고 10→9 (커밋 완료)                 │        │
  │  │  Transaction B: 재고 9→8 (읽음) → A이 롤백되면?       │        │
  │  │                                                      │        │
  │  │  [완화] Pessimistic: 재고 테이블에 version 컬럼으로     │        │
  │  │       낙관적 잠금 (Optimistic Locking) 적용           │        │
  │  │       UPDATE inventory SET qty=9, ver=ver+1           │        │
  │  │       WHERE id=1 AND ver=1 ──(0 row면 재시도)          │        │
  │  └─────────────────────────────────────────────────────┘        │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** **시간적 간격**은 T1(결제 완료)과 T2(재고 차감) 사이에 다른 트랜잭션이 중간 상태를 읽을 수 있는 문제다. 이를 완화하기 위해 **PENDING (대기)** 상태를 도입하여 최종 확정 전까지 임시 상태로 관리한다. **순서 보장** 문제는 Kafka의 **Total Order Per Partition**을 활용하여 같은 **OrderId**는 동일 파티션으로 할당하여 순서를 보장한다. **격리 부족** 문제는 **낙관적 잠금 (Optimistic Locking)**으로 완화한다. 재고 테이블에 **version** 컬럼을 추가하여, UPDATE 시 현재 version을 확인하고 일치할 때만 커밋하여 **쓰기 스큐 (Write Skew)**를 방지한다.

- **📢 섹션 요약 비유**: 사가 패턴은 "여러 사람이 동시에 문서를 편집하는 협업 도구"와 같다. 각자 독립적으로 편집(로컬 트랜잭션)하고, 충돌이 발생하면 나중에 편집한 내용을 되돌리는(보상) 방식이다. 문제는 편집 과정에서 일시적으로 일관성이 깨진 상태가 보인다는 점이다. 이를 완화하기 위해 "편집 중임(PENDING) 표시"를 하거나 "버전 번호"로 충돌을 감지한다.

---

## Ⅳ. 실무 구현 및 운영 (Implementation & Operations)

### 구현 프레임워크

| 프레임워크 | 유형 | 언어 | 특징 |
|:---|:---|:---|:---|
| **Seata (Alibaba)** | 오케스트레이션 | Java | AT, TCC, SAGA 모드 지원, Global Transaction Coordinator |
| **Netflix Conductor** | 오케스트레이션 | Java | Workflow Engine, UI 제공, 대규모 트랜잭션 |
| **Apache Camel** | 통합 패턴 | Java | EIP (Enterprise Integration Pattern) 지원 |
| **Narayana (JBoss)** | 2PC+Saga | Java | LRA (Long Running Action) 사가 지원 |
| **MassTransit (dotnet)** | 코레오그래피 | .NET | 이벤트 기반 Correlation |
| **Axon Framework** | 이벤트 소싱 | Java | CQRS + Event Sourcing + Saga 내장 |

---

### Seata Saga 모드 구현 예시 (Spring Boot)

```java
  ┌──────────────────────────────────────────────────────────────────┐
  │              Seata Saga 모드: 주문 트랜잭션 정의                  │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  @SagaOrchestrationStart                                          │
  │  public class OrderSaga {                                        │
  │                                                                   │
  │      @SagaTransactional                                          │
  │      public void createOrder(Order order) {                      │
  │          // [T1] 주문 생성                                       │
  │          orderRepository.save(order);                           │
  │          sagaManager.register(order.getId(), "OrderCreated");    │
  │      }                                                          │
  │                                                                   │
  │      @SagaTransactional(compensatingMethod = "cancelOrder")      │
  │      public void processPayment(Payment payment) {              │
  │          // [T2] 결제 처리                                      │
  │          paymentService.charge(payment);                        │
  │          sagaManager.register(payment.getOrderId(), "Paid");     │
  │      }                                                          │
  │                                                                   │
  │      public void cancelPayment(Payment payment) {               │
  │          // [C2] 결제 취소 (보상)                                │
  │          paymentService.refund(payment);                        │
  │      }                                                          │
  │                                                                   │
  │      public void cancelOrder(Order order) {                     │
  │          // [C1] 주문 취소 (보상)                                │
  │          order.setStatus(OrderStatus.CANCELLED);                │
  │          orderRepository.save(order);                          │
  │      }                                                          │
  │  }                                                              │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[코드 해설]** **@SagaOrchestrationStart**는 사가 트랜잭션의 시작을 표시한다. **@SagaTransactional**은 각 로컬 트랜잭션을 정의하고, **compensatingMethod**로 실패 시 실행할 보상 메서드를 지정한다. **sagaManager.register()**는 각 단계의 완료를 사가 로그에 기록하여 장애 복구 시 재개 가능하게 한다. **createOrder() → processPayment()** 순서로 실행되고, 중간에 실패가 발생하면 **cancelPayment() → cancelOrder()** 역순으로 보상이 실행된다.

---

### 코레오그래피 사가 구현 예시 (Spring Cloud Stream)

```java
  ┌──────────────────────────────────────────────────────────────────┐
  │            코레오그래피 사가: 이벤트 기반 보상 체인                │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  @Service                                                        │
  │  public class PaymentService {                                  │
  │                                                                   │
  │      @StreamListener(target = "orderCreated")                   │
  │      public void handleOrderCreated(OrderCreatedEvent event) {  │
  │          // [T2] 결제 처리                                       │
  │          Payment payment = paymentService.charge(event);        │
  │          payment.setStatus(PaymentStatus.AUTHORIZED);           │
  │          paymentRepository.save(payment);                       │
  │                                                                   │
  │          // 다음 단계로 이벤트 발행                               │
  │          PaymentAuthorizedEvent authEvent = new                 │
  │              PaymentAuthorizedEvent(payment.getOrderId());      │
  │          streamBridge.send("paymentAuthorized", authEvent);      │
  │      }                                                          │
  │                                                                   │
  │      @StreamListener(target = "inventoryFailed")                │
  │      public void handleInventoryFailed(InventoryFailedEvent e) {│
  │          // [C2] 재고 실패 시 결제 취소 (보상)                  │
  │          Payment payment = paymentRepository                    │
  │              .findByOrderId(e.getOrderId());                     │
  │          paymentService.refund(payment);                        │
  │          payment.setStatus(PaymentStatus.REFUNDED);             │
  │          paymentRepository.save(payment);                       │
  │                                                                   │
  │          // 보상 완료 이벤트 발행                                 │
  │          PaymentRefundedEvent refundEvent = new                 │
  │              PaymentRefundedEvent(payment.getOrderId());        │
  │          streamBridge.send("paymentRefunded", refundEvent);      │
  │      }                                                          │
  │  }                                                              │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[코드 해설]** 코레오그래피 사가는 **이벤트 기반 (Event-Driven)**으로 동작한다. **handleOrderCreated()**는 **OrderCreatedEvent**를 수신하여 결제를 처리하고, **PaymentAuthorizedEvent**를 발행하여 다음 서비스(Inventory)를 호출한다. **handleInventoryFailed()**는 재고 서비스 실패 시 **InventoryFailedEvent**를 수신하여 결제를 환불(보상)하고 **PaymentRefundedEvent**를 발행하여 이전 서비스(Order)가 주문을 취소할 수 있게 한다. 이 방식은 중앙 코디네이터 없이 각 서비스가 자율적으로 동작한다.

---

### 모니터링 및 장애 복구 (Monitoring & Recovery)

사가 트랜잭션의 **분산 추적 (Distributed Tracing)**과 **재시도 (Retry)** 메커니즘은 운영 안정성에 필수적이다. **Zipkin**·**Jaeger**·**SkyWalking** 등으로 추적하고, **Exponential Backoff**로 재시도한다.

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │               사가 트랜잭션 모니터링 및 복구                      │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [Distributed Tracing - Zipkin]                                  │
  │                                                                   │
  │  Trace ID: order-12345                                           │
  │   ├── Span 1: OrderService.createOrder() (15ms)                  │
  │   ├── Span 2: PaymentService.charge() (45ms)                    │
  │   ├── Span 3: InventoryService.reserve() (120ms) ✗ Timeout      │
  │   ├── Span 4: PaymentService.refund() (38ms) ──┐                │
  │   └── Span 5: OrderService.cancel() (12ms) ────┤ 보상 체인       │
  │                                               │                  │
  │  [Retry Policy]                              │                  │
  │  - Initial Delay: 1s                         │                  │
  │  - Backoff Multiplier: 2.0                   │                  │
  │  - Max Attempts: 3                           │                  │
  │  - Max Delay: 10s                            │                  │
  │                                               │                  │
  │  [Retry Timeline]                            ▼                  │
  │  Attempt 1: 0s (1s delay) ─→ Timeout        [성공한 재시도]     │
  │  Attempt 2: 1s (2s delay) ─→ Timeout        Inventory.reserve() │
  │  Attempt 3: 3s (4s delay) ─→ Timeout        → 재시도 성공!      │
  │  Failure → Compensating Started              → Saga 완료        │
  │                                                                   │
  └──────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** **Distributed Tracing**은 **Trace ID**로 전체 트랜잭션 흐름을 추적한다. **Span 3** InventoryService에서 **Timeout**이 발생하면, **보상 체인 (Span 4, 5)**이 실행된다. **Retry Policy**는 **Exponential Backoff**로 재시도 간격을 늘려 서비스 과부하를 방지한다. 3회 재시도 후 실패 시 보상이 시작되지만, 재시도 성공 시 트랜잭션이 정상 완료된다.

- **📢 섹션 요약 비유**: 사가 모니터링은 "택배 배송 추적"과 같다. 각 경로(서비스)마다 스캔(Span)을 찍어 정확히 어디서 지연되거나 실패했는지 파악한다. 재시도 정책은 "연락 안 되면 1분 후, 2분 후, 4분 후에 다시 걸어보는 전화 걸기 전략"과 같아서, 상대방이 너무 자주 전화받는 부담을 줄인다.

---

## Ⅴ. 핵심 정리 및 어린이 비유 (Summary & Child Analogy)

### 핵심 정리

1. **사가 패턴 (Saga Pattern)**은 **결과적 일관성 (Eventual Consistency)**을 허용하는 분산 환경에서 **2PC (Two-Phase Commit)**의 대안으로, 각 서비스의 **로컬 트랜잭션 (Local Transaction)**을 순차적으로 실행하고 중간 실패 시 **보상 트랜잭션 (Compensating Transaction)**으로 논리적 롤백을 수행한다.
2. **오케스트레이션 (Orchestration)** 방식은 중앙 **사가 오케스트레이터 (Saga Orchestrator)**가 트랜잭션 흐름을 제어하고, **코레오그래피 (Choreography)** 방식은 각 서비스가 이벤트를 발행/구독하며 자율적으로 체인을 구성한다.
3. **트랜잭셔널 아웃박스 (Transactional Outbox)** 패턴은 **DB 커밋**과 **메시지 발행**의 원자성을 보장하고, **CQRS**는 조회 최적화, **Event Sourcing**은 완전한 감사/복구 기능을 제공하여 사가와 결합한다.
4. 사가 패턴의 **시간적 간격 (Temporal Gap)**·**순서 보장 (Ordering)**·**격리 부족 (Lack of Isolation)** 문제는 **PENDING 상태**·**낙관적 잠금 (Optimistic Locking)**·**Kafka 순서 보장** 등으로 완화한다.
5. **Seata**·**Netflix Conductor**·**Apache Camel**·**Axon Framework** 등의 프레임워크와 **Zipkin**·**Jaeger**의 **분산 추적 (Distributed Tracing)**으로 운영 안정성을 확보한다.

---

### 어린이를 위한 비유: 🎭 연극 공연의 리허설

사가 패턴은 **여러 배우(서비스)가 함께 하는 연극 공연**과 같습니다.

1. **각 배우는 자신의 대사만 외웁니다** (로컬 트랜잭션):
   - 배우 A는 "안녕!"을 외우고, 배우 B는 "반가워!"를 외웁니다.
   - 각자 자신의 대사만 확실히 외우면 됩니다.

2. **순서대로 공연을 시작합니다** (정방향 실행):
   - 배우 A가 "안녕!"을 말합니다. ✓
   - 배우 B가 "반가워!"를 말합니다. ✓
   - 배우 C가 "만나서 glad!"를 말합니다. ✗ (대사 까먹음!)

3. **누군가 실수하면 처음부터 다시 합니다** (보상 트랜잭션):
   - 배우 C가 대사를 까먹었으니, 이전 배우들이 자신의 대사를 취소합니다.
   - 배우 B: "취소! 방금 안 그랬어!" (보상)
   - 배우 A: "죄송합니다! 처음으로 돌아갑니다." (보상)

4. **모든 연습을 다시 시작합니다** (재시도):
   - 다시 처음부터 공연을 시작합니다.
   - 이번에는 모두가 대사를 잘 외워서 성공적으로 끝납니다!

5. **감독님이 전체를 지휘합니다** (오케스트레이션) 또는 **서로 신호를 보냅니다** (코레오그래피):
   - **감독님 방식**: 중앙에 서 있는 감독님이 "다음!" "취소!"를 외칩니다.
   - **서로 신호 방식**: 배우들이 서로 "내가 끝났어! 너 차례야!"라고 신호를 보냅니다.

6. **연습 과정을 녹화합니다** (사가 로그):
   - 모든 연습 과정을 비디오로 찍어뒀다가, 누가 언제 실수했는지 나중에 다시 볼 수 있습니다.

**🎯 핵심**: 사가 패턴은 "함께 하는 연극에서 누군가 실수하면, 처음으로 돌아가 다시 시작하는 리허설 방식"입니다. 각자는 자신의 역할만 확실히 하고, 문제가 생기면 함께 처음으로 돌아가서 다시 시작합니다!

---

### 개념 맵 (Mind Map)

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         사가 패턴 (Saga)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ① 개요 ───────────────────────────────────────────────────────┐    │
│     - 결과적 일관성 (Eventual Consistency)                    │    │
│     - 로컬 트랜잭션 체인                                      │    │
│     - 보상 트랜잭션 (Compensating Transaction)                │    │
│     - 2PC 대안                                                │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ② 아키텍처 ───────────────────────────────────────────────────┐    │
│     - 오케스트레이션 (Orchestration)                          │    │
│     - 코레오그래피 (Choreography)                             │    │
│     - 사가 로그 (Saga Log)                                   │    │
│     - 이벤트 버스 (Event Bus)                                │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ③ 상태 전이 ─────────────────────────────────────────────────┐    │
│     STARTED → PENDING → RUNNING → COMPLETED                    │    │
│                ↓ (실패)                                        │    │
│           COMPENSATING → COMPENSATED                          │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ④ 문제 및 완화 ───────────────────────────────────────────────┐    │
│     - 시간적 간격: PENDING 상태 도입                          │    │
│     - 순서 보장: Kafka 파티션 할당                            │    │
│     - 격리 부족: 낙관적 잠금 (Optimistic Locking)              │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ⑤ 구현 프레임워크 ────────────────────────────────────────────┐    │
│     - Seata (AT, TCC, SAGA)                                  │    │
│     - Netflix Conductor                                      │    │
│     - Axon Framework (CQRS + Event Sourcing)                 │    │
│     - MassTransit (dotnet)                                   │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```
