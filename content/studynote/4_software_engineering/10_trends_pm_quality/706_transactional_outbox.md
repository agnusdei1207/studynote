+++
title = "706. 트랜잭셔널 아웃박스 이벤트 유실 방지"
date = "2026-03-15"
weight = 706
[extra]
categories = ["Software Engineering"]
tags = ["MSA", "Design Pattern", "Transactional Outbox", "Eventual Consistency", "Distributed Transactions", "Message Queue"]
+++

# 706. 트랜잭셔널 아웃박스 이벤트 유실 방지

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 환경(MSA)에서 **DB (Database) 트랜잭션**과 **메시징 시스템(Message Broker) 전송** 간의 원자성(Atomicity)을 보장하기 위해, 이벤트를 임시 저장하는 **아웃박스(Outbox) 테이블**을 도입하여 데이터 무결성을 유지하는 패턴입니다.
> 2. **가치**: 2PC(2-Phase Commit) 같은 무거운 분산 락(Lock)을 사용하지 않고도 **At-least-once (최소 1회)** 전달을 보장하여, 이벤트 유실에 따른 비즈니스 크리티컬 오류를 방지하고 시스템 결합도를 낮춥니다.
> 3. **융합**: **CDC (Change Data Capture)** 기술과 결합하여 near real-time에 준하는 성능을 내며, **Saga Pattern**의 보상 트랜잭션(Compensating Transaction) 신뢰성을 담보하는 핵심 인프라로 작용합니다.

---

### Ⅰ. 개요 (Context & Background)

트랜잭셔널 아웃박스 패턴은 분산 트랜잭션의 난제인 "이중 쓰기(Dual Write)" 문제를 해결하기 위해 등장했습니다. 일반적으로 마이크로서비스 아키텍처(MSA, Microservice Architecture)에서 비즈니스 데이터를 RDBMS(Relational Database Management System)에 커밋(commit)하고, 동시에 메시지 브로커(Kafka, RabbitMQ 등)로 알림을 보낼 때, 두 시스템 간의 트랜잭션을 동기식으로 묶는 것은 불가능에 가깝습니다.

**① 등장 배경 및 한계:**
기존의 **2PC (2-Phase Commit)** 방식은 코디네이터(Coordinator)가 참여자들을 관리하여 원자성을 보장하지만, 모든 리소스에 락(Lock)을 걸어야 하므로 시스템 성능을 급격히 저하시키고, 단일 장애점(SPOF, Single Point of Failure) 문제를 야기합니다. 반면, 메시지 전송 후 DB를 업데이트하거나 그 반대로 수행하는 방식은 네트워크 오류나 서버 다운 시 데이터와 이벤트의 상태가 불일치하는 "Critical Section"에 노출됩니다.

**② 해결책:**
이 패턴은 **"메시지 큐를 데이터베이스의 일부로 간주"**하는 사고방식의 전환을 제공합니다. 이벤트를 외부 시스템으로 즉시 던지는 것이 아니라, 현재 진행 중인 DB 트랜잭션 범위 내에 있는 `OUTBOX` 테이블에 먼저 기록함으로써, **로컬 트랜잭션(Local Transaction)**의 성공/실패 범위 내에 이벤트 저장을 포함시킵니다.

```text
[ 개념적 비유: 총알과 탄환벨트 ]
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  🔫 문제 상황 (Direct Publish):                                       │
│  총을 쏘는 순간(발행) 장전이 안 되었거나, 장전했는데 총알이 사라짐.    │
│  -> 데이터와 이벤트의 싱크이 깨짐.                                     │
│                                                                       │
│  ✅ 아웃박스 방식 (Transactional Outbox):                             │
│  1. 사수가 총알을 '탄창(Outbox Table)'에 장전함. (DB Transaction)     │
│  2. 장전이 완료된 후, '부사수(Relay Process)'가 탄창에서 총알을 꺼내  │
│     적에게 발사함. (Message Publish)                                  │
│                                                                       │
│  -> 사수가 총을 쏘지 못해도 탄창에 총알은 남아있으므로, 반드시 발사됨. │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

#### 📢 섹션 요약 비유
마치 배달 앱에서 주문을 접수하면 **'픽업 대기함'**에 주문서를 넣어두는 것과 같습니다. 주방장(서비스)은 음식 만들기와 주문서 넣기를 동시에 처리하며, 배달기사(메시지 브로커)는 대기함에서 주문서를 꺼내 가게 됩니다. 이를 통해 주방장이 바빠도 주문서가 유실되지 않습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

이 패턴의 핵심은 **"상태 변경(State Change)과 이벤트 발행(Publish)의 분리"**입니다. 비즈니스 로직의 실행 흐름과 이벤트의 전송 흐름을 분리하여, 각각이 독립적으로 확장 가능하고 장애에 견고하도록 만듭니다.

#### 1. 상세 구성 요소 (Component Table)

| 요소명 (Component) | 역할 (Role) | 내부 동작 (Internal Logic) | 프로토콜/기술 (Protocol) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **Application Service** | 비즈니스 로직 수행 및 주체 | DB 트랜잭션을 시작하여 도메인 엔티티 저장과 `Outbox` Insert를 원자적으로 실행 | JDBC/JPA | **주방장** |
| **Outbox Table** | 이벤트 임시 저장소 | `id`, `aggregate_type`, `payload`, `created_at` 등을 가짐. 메인 테이블과 동일한 DB 인스턴스에 위치 | SQL Table | **주문서함** |
| **Message Relay (Publisher)** | 이벤트 전송 모듈 | Outbox 테이블을 감시하거나 로그를 읽어 브로커로 전송. 전송 성공 시 테이블 데이터 삭제 또는 처리 완료 표시 | Kafka Producer / RabbitMQ Publisher | **배달 기사** |
| **Message Broker** | 비동기 메시징 미들웨어 | 이벤트를 큐에 저장하여 구독자(Consumer)에게 전달 | Apache Kafka, RabbitMQ | **배달 센터** |
| **Cleaner Job** | 데이터 정비 | 이미 처리된 오래된 Outbox 레코드를 물리적으로 삭제하여 디스크 공간 확보 | SQL DELETE / TTL | **쓰레기 압축차** |

#### 2. 아키텍처 데이터 흐름 (ASCII)

```text
   [ 1. Business Execution & DB Write ]
        ┌───────────────┐
        │   Client API  │
        └───────┬───────┘
                ▼
        ┌───────────────────────────────────────┐
        │      Microservice Application          │
        │  ┌─────────────────────────────────┐   │
        │  │  @Transactional                │   │
        │  │  ① updateOrder(order)          │   │
        │  │  ② insertOutbox(event) <───────┼───┼───▶ Local DB (Commit)
        │  └─────────────────────────────────┘   │
        └───────────────────────────────────────┘

   [ 2. Data Extraction & Relay ]

        ┌───────────────────────────────────────┐       ┌───────────────────┐
        │      Database Server                  │       │  Message Relay    │
        │  ┌─────────────────────────────────┐   │       │ (Separate Process)│
        │  │   Business Table    Outbox Table│   │       └─────────┬─────────┘
        │  │     (Order)      ────▶ (Event)  │   │  (Poll or CDC)    │
        │  │                                   │   │          ▼         │
        │  └───────────────────────────────────────┘       │ SELECT/Stream  │
        │           ▲                         │           │ or Log Tailing  │
        │           │                         │           │                 │
        └───────────┼─────────────────────────┘           ▼
                    │ (Read)                 ┌─────────────────────────────┐
                    │                         │   Message Broker (Kafka)   │
                    │                         └─────────────┬───────────────┘
                    │ (Delete on Success)     (Async Event)
                    │                         ┌─────────────┴───────────────┐
                    │                         │   Consumer (Other Services) │
                    └─────────────────────────┴─────────────────────────────┘
```

**① 도입 서술**: 위 다이어그램은 트랜잭션 경계와 메시지 전송 경계가 물리적으로 분리되어 있음을 보여줍니다. 애플리케이션은 DB에만 집중하며, 릴레이(Relay)는 DB를 읽어 브로커에 전달하는 책임만 집중합니다.

**③ 해설**:
1. **Step 1 (Atomic Write)**: 애플리케이션은 `@Transactional` 어노테이션 혹은 트랜잭션 스코프 내에서 주문 정보를 `ORDER_TABLE`에 저장함과 동시에, 이벤트 정보(JSON 등)를 `OUTBOX_TABLE`에 삽입합니다. 이 둘은 하나의 DB 트랜잭션으로 묶여 있으므로, **"All-or-Nothing"**이 보장됩니다.
2. **Step 2 (Relay Process)**: 별도의 프로세스인 **Message Relay**는 주기적으로(Polling) `OUTBOX_TABLE`을 조회하거나, **CDC (Change Data Capture)** 기술을 통해 Binary Log를 실시간 스트리밍합니다.
3. **Step 3 (Publish & Cleanup)**: Relay는 읽어온 이벤트를 Kafka 토픽(Topic)으로 전송(Publish)합니다. 이때 브로커로부터 **ACK (Acknowledgment)**를 받으면, 해당 Outbox 레코드를 DB에서 삭제하거나 `status='PROCESSED'`로 업데이트합니다.

#### 3. 핵심 알고리즘 및 코드 구현

릴레이는 멱등성을 보장하며 동작해야 합니다.

```python
# Pseudo-code: Transactional Outbox Publisher
while True:
    # 1. 조회 단계 (Lock-based or Idempotent read)
    # 일정 시간 동안 전송되지 않은 메시지를 조회 (CreatedTime 기준)
    events = db.query("""
        SELECT * FROM outbox 
        WHERE processed_at IS NULL 
        AND created_at < NOW() - INTERVAL 5 second
        LIMIT 100
        FOR UPDATE SKIP LOCKED  # Concurrency Safety
    """)

    for event in events:
        try:
            # 2. 발행 단계
            kafka_client.send(topic=event.topic, value=event.payload)
            
            # 3. 처리 완료 표시 (Commit)
            db.execute("""
                UPDATE outbox 
                SET processed_at = NOW() 
                WHERE id = ?
            """, event.id)
            db.commit()
            
        except PublishError:
            # 발행 실패 시 롤백하지 않고 다음 스케줄에 재시도함
            db.rollback()
```

#### 📢 섹션 요약 비유
마치 **편의점 바코드 스캔과 재고 관리 시스템**과 같습니다. 계산원(서비스)이 계산을 완료하면 매출 전표(Outbox)가 남습니다. 이후 본사 시스템(Relay)이 이 전표들을 수집해 재고를 차감합니다. 계산원이 본사 서버가 느려도 기다릴 필요 없이 일단 계산(로컬 트랜잭션)을 마칠 수 있습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

아웃박스 패턴은 단순히 큐를 사용하는 것이 아니라, 분산 시스템의 **CAP 정리**에서 Consistency(일관성)와 Availability(가용성)의 균형을 맞추는 정교한 설계입니다.

#### 1. 분산 트랜잭션 기술 비교 (Quantitative Analysis)

| 구분 | 2PC (2-Phase Commit) |.Transactional Outbox (이중 쓰기) |
|:---|:---|:---|
| **트랜잭션 범위** | **Global (분산)**: DB + Broker 모두 Lock | **Local (로컬)**: DB만 Lock |
| **성능 (Latency)** | 매우 높음 (네트워크 왕복 2회 이상 소요) | 낮음 (DB 커밋 1회로 끝남) |
| **일관성 모델** | 강한 일관성 (Strong Consistency) | 최종 일관성 (Eventual Consistency) |
| **장애 영향** | Blocking 가능성 높음 (전체 시스템 멈출 수 있음) | 비동기 처리로 서비스 영향 적음 (Backlog 가능성 있음) |
| **복잡도** | 미들웨어 지원 필요 but 구현이 무거움 | 릴레이 로직 및 CDC 구현 필요 |
| **메시지 유실** | 드물지만 트랜잭션 불일치 위험 있음 | **0%에 수렴** (At-least-once 보장) |

#### 2. 타 기술과의 시너지 및 융합

**① CDC (Change Data Capture)와의 결합**
아웃박스 패턴의 가장 강력한 조합은 **CDC**입니다. 일반적인 폴링(Polling) 방식은 Outbox 테이블에 잦은 `SELECT` 쿼리를 발생시켜 DB 부하를 유발할 수 있습니다. 반면, Debezium과 같은 CDC 커넥터를 사용하면 DB의 WAL(Write-Ahead Log)나 Binlog를 실시간으로 읽어 Outbox 테이블의 변경 사항을 스트리밍합니다.
- **장점**: DB I/O 부하 최소화, 밀리초 단위의 실시간성 확보.
- **융합 효과**: 데이터 엔지니어링 관점에서 데이터 파이프라인(ETL)의 일관성 보장용으로도 사용됨.

**② Idempotency (멱등성)의 필수성**
아웃박스 패턴은 `At-least-once` 전달을 보장합니다. 즉, 네트워크 오류로 인해 ACK를 받지 못하면 동일한 메시지를 두 번 보낼 수 있습니다. 따라서 수신 측(Consumer)은 반드시 **멱등성 Idempotency**을 가져야 합니다.
- **구현 방법**: 이벤트에 고유 UUID를 포함시키고, Consumer는 이 UUID를 Redis나 DB에 저장하여 중복 처리 여부를 체크 (이미 처리된 ID면 무시).

**③ Saga Pattern과의 관계**
MSA의 **Saga Pattern**은 여러 서비스의 로컬 트랜잭션을 순차적으로 실행하여 전체 트랜잭션을 완성합니다. 이때 각 서비스가 다음 Saga 단계를 트리거할 때, 아웃박스 패턴을 사용하여 이벤트를 안전하게 전달합니다. 만약 아웃박스가 없다면, 중간 이벤트 유실 시 전체 비즈니스 프로세스가 멈추거나 데이터 정합