---
title: "Event Driven Architecture EventBridge"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 640
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Amazon EventBridge는 AWS 네이티브 서비스·SaaS 파트너·커스텀 애플리케이션의 이벤트를 **Schema Registry 기반의 표준화된 EventEnvelope(JSON) + Content Filtering(EDA 필터 표현식) + PutEvents API**로 단일 이벤트 버스에 수집하여 **Routing Rule(Bus -> Target) -> 비동기 Fan-out(여러 Target) -> 24h 재처리 가능한 Archive** 흐름으로 전달하는 **완전관리형(Serverless) Pub/Sub 이벤트 라우터**이다.
> 2. **가치**: Lambda 직접 호출 대비 **p99 지연시간 약 50ms 미만**으로 초당 수백만 건 처리, **SaaS 이벤트를 200+ SaaS Provider에서 1-Click 통합**, **Default Bus를 통한 추가 인프라 0개**로 EDA 구현 -> 시스템 간 결합도를 강결합(RPC/Synchronous REST)에서 약결합(Event-driven)으로 전환하여 도메인별 팀의 독립 배포와 스케일링이 가능해진다.
> 3. **판단 포인트**: **이벤트 순서 보장(Ordered Delivery vs 동시성), 부분 실패 처리(Partial Batch Failure 응답), 스키마 진화(Schema Versioning·Backwards Compatibility), Dead Letter Queue(2회 재시도 후 최대 24h 보존), Cross-Account/Region을 위한 Global Endpoint vs Event Bus Resource Policy**, 그리고 **Idempotency(EventId + dedup)·Exactly-Once 보장 범위**가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

전통적인 모놀리식·N-Tier 아키텍처는 서비스 간 통신을 **동기 HTTP/REST(OpenAPI), SOAP, gRPC**에 의존한다. 이 방식은 호출자(Caller)가 피호출자(Callee)의 API 시그니처, 가용성, 처리 지연에 직접 종속되기 때문에 **Tight Coupling**과 **Cascading Failure**라는 구조적 한계를 갖는다. 트래픽이 증가하면 API Gateway -> Service Mesh(Envoy/Istio) -> Circuit Breaker(Hystrix/Resilience4j) 패턴으로 대응하지만, 근본적으로 *“요청이 완료되어야 응답을 받을 수 있다(Synchronous Blocking)”*는 한계는 해결되지 않는다.

특히 MSA(Microservices Architecture)가 보편화되면서 **비동기 메시징(Kafka, RabbitMQ, ActiveMQ)** 기반의 이벤트 드리븐 아키텍처(Event-Driven Architecture, EDA)가 주목받기 시작했다. 그러나 셀프 운영형 메시지 브로커는 **Broker HA(3-AZ Replication), Zookeeper/KRaft 클러스터 관리, 스키마 레지스트리(Confluent Schema Registry/Apicurio), Dead Letter 처리, 메시지 압축·암호화, 운영자 모니터링(Prometheus/JMX)** 등 **“빌드보다 운영이 더 어렵다(You build it, you run it)”**라는 오버헤드가 존재한다.

**Amazon EventBridge**는 이러한 운영 부담을 **완전관리형(Fully Managed) Serverless Event Bus**로 해소하기 위해 2019년 7월 “CloudWatch Events”의 후속 서비스로 출시되었다. 가장 큰 차별점은 **1) AWS 서비스 이벤트 자동 통합(70+ AWS Sources), 2) 200+ SaaS 파트너 이벤트 통합(Salesforce, Datadog, Zendesk 등) 3) Schema Registry 자동 추론 4) 버스·규칙·타깃의 선언적 구성(CloudFormation/CDK IaC) 5) 24h 보관 Archive 및 재생(Replay) 6) 2022년 추가된 EventBridge Pipes(포인트-투-포인트 필터+확장) 및 EventBridge Scheduler(스케줄러)**다.

```text
[전통적 동기 REST 아키텍처]                     [EventBridge 기반 EDA 아키텍처]

  Client --HTTP---> API GW ---> Service A         Producer --PutEvents--+
                              |                                        |
                              +--REST---> Service B                     v
                              |                                    +----------+
                              +--REST---> Service C   (강결합·동기) |  Default  | --Rule---> Lambda
                                          |                         |  EventBus | --Rule---> SQS
                                          +--REST---> Service D     | (Serverless)| --Rule---> StepFn
                                                (Cascading)        +----------+ --Rule---> Kinesis
                                       약결합·비동기                --Rule---> SNS -> 다수 Consumer
```

**왜 EventBridge가 필요한가?**

- **비즈니스 요구**: 신규 SaaS 도입 시 마다 *“통합 어댑터”*를 개발해야 했던 것을 **1-Click Partner Event Source**로 단순화. 예) Zendesk 티켓 생성 -> EventBridge -> Lambda -> Slack 알림 (코드 0줄)
- **운영 요구**: Kafka 클러스터의 ZooKeeper/KRaft quorum 관리, 파티션 리밸런싱, 컨슈머 그룹 rebalance를 **AWS에 위임**
- **거버넌스 요구**: Schema Registry로 이벤트 계약(Contract)을 코드화 -> **Consumer 개발자가 컨트랙트 변경에 사전 대응 가능(Backwards-Compatible Evolution)**
- **비용 효율**: **Lambda 호출은 호출 횟수 기반(1M 무료), EventBridge는 이벤트 발행 횟수 기반($1.00/1M events)**, 인프라 미사용 시 0원

```text
[On-Premise Self-Hosted vs AWS EventBridge TCO 비교 - 1년 기준(예시)]
+------------------------+------------------+---------------------+
| 항목                   | Kafka Self-Hosted | AWS EventBridge      |
+------------------------+------------------+---------------------+
| Infra (EC2 3-AZ)       | $36,000/yr      | $0 (Serverless)     |
| Broker 라이선스/지원   | $15,000/yr      | $0                  |
| 운영 인건비(FTE 0.5)   | $60,000/yr      | $0                  |
| 이벤트 처리량 (예)      | 10B events/yr   | 10B events/yr       |
| 이벤트 발행 요금       | -               | $10,000 (1M당 $1)  |
| Lambda 호출            | $2,000          | $2,000              |
| Archive 스토리지       | $1,200 (S3)     | $0.10/GB ($50)      |
+------------------------+------------------+---------------------+
| 합계                   | ~$114,200/yr    | ~$12,050/yr         |
| ROI                    | Baseline        | 약 89% 절감         |
+------------------------+------------------+---------------------+
※ 대규모(>50B/yr)·저지연·고순서·스트림 처리(Window/KSQL) 필요 시 Kafka MSK·Kinesis Data Streams가 더 적합할 수 있음
```

- **📢 섹션 요약 비유**: 기존 시스템이 손님 한 명 주문이 끝나야 다음 손님을 받는 **카페 직렬 계산대**였다면, EventBridge는 **음식 주문·제조·배달이 모두 비동기로 흘러가는 배달의민족 플랫폼**과 같다. 손님(Producer)은 주문만 넣고, 요리사(Consumer)는 준비되는 대로 받아 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EventBridge의 핵심 구성 요소는 **Event Bus, Rule, Target, Archive, Schema Registry, EventBridge Pipes/Scheduler, Global Endpoints, Endpoint(API Destination)**의 8가지로 분류된다.

```text
[EventBridge 내부 아키텍처 상세 흐름]

   +--------------+
   | AWS Services | (S3, EC2, RDS, DynamoDB, ECS, ...)
   |  (70+ Source)|
   +------+-------+
          | (Service Event 자동)
          v
   +--------------+    +-----------------+    +------------------+
   |  SaaS Apps   |---->|  Partner Event  |---->|  Custom Bus      |
   | (Zendesk,..) |    |     Source       |    |  (Per Account)   |
   +--------------+    +-----------------+    +--------+---------+
                                                         |
   +--------------+    +-----------------+              |
   |  사용자 앱   |---->|  PutEvents API  |--------------+
   | (SDK/HTTP)   |    | (10MB/req, 256KB)|              |
   +--------------+    +-----------------+              v
                                                +------------------+
                                                |   Event Bus      |
                                                | +--------------+ |
                                                | |  Default Bus | |  <- 모든 AWS 이벤트가 자동으로 흐름
                                                | +--------------+ |
                                                | | Custom Bus A | |  <- 도메인별 격리 (e.g. payment-bus)
                                                | +--------------+ |
                                                | | Custom Bus B | |  <- Cross-Account/Region 이벤트 수신
                                                | +--------------+ |
                                                +--------+---------+
                                                         | (EventEnvelope JSON: version, id, source, time, region, account, resources, detail)
                                                         v
                                                +------------------+
                                                |  Rule Engine     |  <- Content Filtering: $source, $detail-type,
                                                |  (Filter + Rout) |    $detail.field, $detail.path, <, >, exists, prefix
                                                +--------+---------+
                                                         |
                            +--------------+-------------+-------------+--------------+--------------+
                            v              v             v             v              v              v
                        +--------+    +--------+    +--------+   +---------+   +---------+   +---------+
                        | Lambda |    |  SQS   |    |  SNS   |   | StepFn  |   | Kinesis |   |  ECS    |
                        |  Func  |    | Queue  |    | Topic  |   | StateM  |   | Stream  |   | Task    |
                        +--------+    +--------+    +--------+   +---------+   +---------+   +---------+
                            |              |             |             |              |              |
                            v              v             v             v              v              v
                         [처리]         [Worker]      [Fan-out]     [Orchestrate]  [Analytics]   [Container]
```

**PutEvents API의 이벤트 페이로드 구조 (EventBridge EventEnvelope v1.0):**

```json
{
  "version": "0",
  "id": "c4b1c2d4-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
  "detail-type": "RDS DB Instance Event",
  "source": "aws.rds",
  "account": "123456789012",
  "time": "2024-08-15T12:00:00Z",
  "region": "ap-northeast-2",
  "resources": ["arn:aws:rds:ap-northeast-2:123456789012:db:mydb"],
  "detail": {
    "EventCategories": ["backup"],
    "SourceType": "DB_INSTANCE",
    "SourceArn": "arn:aws:rds:ap-northeast-2:123456789012:db:mydb",
    "Date": "2024-08-15T12:00:00.000Z",
    "Message": "Backing up DB instance"
  }
}
```

**EventBridge의 핵심 처리 알고리즘:**

1. **Event Ingestion**: PutEvents API는 동기적 200 OK 응답(Success/FailedEntryCount 반환), 비동기로 Event Bus에 저장
2. **Filtering**: Rule의 **EventPattern**(JSON)을 정의 -> 내부적으로 **Cedar 정책 언어**와 유사한 표현식 엔진으로 평가. 변수(`$.detail.orderId`), 와일드카드(`"aws.*"`), 배열 매칭(`"exists"`, `"prefix"`, `"numeric" [">=", 100]`) 지원
3. **Routing**: 매칭된 Rule에 연결된 모든 Target에 병렬 전달(Fan-out). 규칙당 최대 **5개 Target** (추가 시 `aws:events:list-rules`로 분할)
4. **Retry & DLQ**: Target 실패 시 **24시간 동안 재시도, 185초(2분) 간격, 2회 재시도(RetryPolicy: maxEventAgeInSeconds=86400, retryAfter: 0~3600)**, 그 후 DLQ(SQS) 또는 EventBridge **Dead Letter Queue(별도)** 로 이동
5. **Idempotency**: EventId(`id`) 기반 **At-Least-Once 전달**, Consumer는 자체 **deduplication(예: DynamoDB Conditional Write)·idempotent key 설계 필수**

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Event Bus** | 이벤트의 논리적 채널, 도메인별 격리 | Default Bus(계정당 1개·AWS 이벤트 자동), Custom Bus(도메인 격리·Cross-Account 수신), Partner Bus(SaaS 연결), 버스당 초당 10,000 PutEvents 호출 한도(Burst: 20,000), 계정당 100개 버스 |
| **Rule (EventPattern)** | 이벤트 필터링 및 라우팅 규칙 | JSON 패턴 매칭, `prefix`/`suffix`/`anything-but`/`numeric`/`cidr`/`exists-or-empty`, 시간 기반 Schedule(Cron/Rate) 규칙, **규칙당 5개 Target 제한** |
| **Target** | 이벤트가 전달되는 종착점(18+ AWS 서비스) | Lambda, SQS, SNS, Step Functions, Kinesis Streams/Firehose, ECS Task, Batch Job, API Gateway, API Destination(HTTP 엔드포인트), Event Bus in other Account, Redshift, SageMaker, Glue, SSM Run Command, Kinesis Data Streams |
| **Archive** | 이벤트 영구 보관 및 Replay | 24h~365일 보존, 필터 기반 부분 보관, Archive 크기 무제한, **Replay 시 새 이벤트로 재생(Re-PutEvents)**하여 다운스트림 시스템 보정 |
| **Schema Registry** | 이벤트 스키라 자동 발견 및 버전 관리 | **Discoverer**가 버스 트래픽을 샘플링하여 OpenAPI 3.0 / JSONSchema Draft 4 자동 생성, **Schema Versioning**, 다운스트림 SDK 생성(Java/Python/TypeScript/Go) |
| **EventBridge Pipes** | Point-to-Point 통합 (2022) | Source(PaaS/SQS/Kafka/DynamoDB) -> Filter -> Optional Enrichment(Lambda/StepFn/API Dest) -> Target, **Batch 처리·부분 실패 응답(Partial Batch Failure)**, **Polling 기반(Poller Lambda 불필요)**, **Ordering 지원** |
| **EventBridge Scheduler** | Cron/One-Time 스케줄링 (2022) | 1회성 또는 Cron(일/시/분), **Universal Target** 270+ AWS API 직접 호출(예: `lambda:InvokeFunction`·`sqs:SendMessage`·`ecs:RunTask`), 시간대(Time Zone) 지원, **유예 기간(End Date) 설정 가능** |
| **Global Endpoints** | 리전 간 이중화 (2023) | Active-Active 또는 Active-Passive, 한 리전 장애 시 자동 페일오버(< 1분), Route53 Health Check 기반, **replication latency < 60초** |

**EventBridge Pipes의 핵심 차별점 (Pipes vs Rule-based Bus):**

```text
[Pipes - 배치·부분실패·정렬 지원]         [Rules - 단순 라우팅]

Source: Kinesis Data Stream      Source: Event Bus (PutEvents)
  |                                    |
  v                                    v
Filter: SQL 표현식 ($.kinesis.)   Filter: JSON EventPattern
  |                                    |
  v                                    v
Enrichment (선택)                (없음 - Rule은 인라인 변환 없음)
  +- Lambda (대용량 처리)
  +- Step Functions (Orchestration)
  +- API Destination (HTTP)
  |
  v
Target: SQS/SNS/Lambda
  +- Partial Batch Failure 응답 (실패한 것만 재처리)
  +- Ordering: ShardKey 기반 보존
```

**📢 섹션 요약 비유**: EventBridge는 마치