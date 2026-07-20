---
title: "Serverless Computing FaaS Event Driven"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 611
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FaaS(Function-as-a-Service)는 AWS Lambda, Azure Functions, Google Cloud Functions 같은 런타임에서 stateless한 함수 코드만 배포하고, EventBridge/S3/SQS/Kafka/HTTP 등 이벤트 소스 트리거에 의해 밀리초 단위로 컨테이너/마이크로VM이 자동 스케일링·실행되는 이벤트 드리븐 컴퓨팅 모델이며, CNCF Serverless Working Group 정의에 따르면 "BaaS + FaaS = Serverless"로 추상화된 클라우드 자원 위에서 개발자는 비즈니스 로직에만 집중한다.
> 2. **가치**: 유휴 상태 비용 0(GB-초 단위 과금)으로 EC2 대비 70~90% 비용 절감이 가능하며, Auto Scaling Group 대비 트래픽 폭증 시 P99 콜드 스타트 200~500ms(SnapStart/Provisioned Concurrency 적용 시 10ms 이하) 수준의 탄력성을 제공하고, 인프라 관리·패치·용량 계획(operational overhead 60%v)을 클라우드 제공자에게 오프로드한다.
> 3. **판단 포인트**: 콜드 스타트 지연, 15분 실행 시간 한도(Lambda 기준), 6MB 동기 페이로드 제한, Stateless 제약으로 인한 외부 저장소(DynamoDB/ElastiCache/RDS Proxy) 의존, 분산 트레이싱·관측성(Observability) 확보 난이도, 그리고 Vendor Lock-in(X-Ray vs Application Insights vs Cloud Trace) 트레이드오프를 기준으로 워크로드 적합성을 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 3-Tier Monolithic 애플리케이션은 EC2/On-Premise VM 기반 상시 가동(Always-On) 방식으로 트래픽 평균치 기준 용량 계획(capacity planning)을 수행했기 때문에, 간헐적·폭발적 워크로드(예: 야간 배치, 신상품 출시 트래픽, 사물인터넷 센서 데이터)에서 자원 낭비와 Scale-Out 지연 문제가 상존했다. 컨테이너 기반 마이크로서비스(Kubernetes, EKS)도 노드 풀링·HPA 설정·이미지 빌드·Service Mesh(Istio/Linkerd) 등 운영 부담이 남아 있었으며, 실제 코드 실행 시간 대비 인프라 관리 시간이 70%에 달하는 DevOps 피로도가 대두되었다.

서버리스 컴퓨팅은 이러한 한계를 극복하기 위해 2014년 AWS Lambda 발표를 기점으로, "클라우드 제공자가 동적으로 컴퓨팅 자원을 할당하고, 개발자는 함수 단위의 코드만 정의하며, 사용한 만큼만(per-millisecond, per-invocation) 과금"하는 새로운 패러다임을 제시했다. FaaS는 특히 Event-Driven(Pub/Sub, CDC, IoT, Webhook) 워크로드에 최적화되어 있으며, API Gateway + Lambda + DynamoDB 같은 조합으로 BaaS(Backend-as-a-Service)와 결합 시 풀스택 서버리스 아키텍처가 완성된다.

```text
[전통적 모놀리식 vs 서버리스 이벤트 드리븐 비교]

  +----------------------+                      +------------------------------+
  |  Traditional Stack   |                      |  Serverless FaaS Stack       |
  |  ------------------  |                      |  --------------------------  |
  |  Client (Browser/App)|                      |  Client (Web/Mobile/IoT)     |
  |         |            |                      |         |                    |
  |         v            |                      |         v                    |
  |  +--------------+   |                      |  +--------------+            |
  |  |  ALB / NLB   |   |                      |  | API Gateway  | HTTP/REST  |
  |  +------+-------+   |                      |  |   / CloudFront            |
  |         v            |                      |  +------+-------+            |
  |  +--------------+   |                      |         v                    |
  |  |  EC2 ASG     |   |  ※ 항상 ON           |  +--------------------------+|
  |  |  (Min 2, Max |   |  ※ 패치/OS 관리      |  |   Lambda Function        ||
  |  |   20대 상시) |   |  ※ AMI 빌드 필요     |  |  (Auto-scaling 0~1000)   ||
  |  +------+-------+   |  ※ 평균 트래픽 설계  |  |   Runtime: Node/Python/  ||
  |         v            |                      |  |   Java/Go/Rust/Custom   ||
  |  +--------------+   |                      |  +------+-------------------+|
  |  |  RDS MySQL   |   |                      |         | invokes            |
  |  +--------------+   |                      |         v                    |
  |                      |                      |  +--------------------------+|
  |  과금: 시간당 상시   |                      |  | EventBridge / SQS / SNS  ||
  |  + 데이터 전송       |                      |  | DynamoDB Streams / S3    ||
  |                      |                      |  +------+-------------------+|
  |                      |                      |         v                    |
  |                      |                      |  +--------------------------+|
  |                      |                      |  | DynamoDB / S3 / Aurora   ||
  |                      |                      |  | Serverless / ElastiCache ||
  |                      |                      |  +--------------------------+|
  |                      |                      |  과금: Invocations + GB-sec |
  +----------------------+                      +------------------------------+
```

**왜 필요한가?**

- **탄력성(Elasticity)**: Lambda는 Concurrency 1,000 기본 한도(증설 가능 10만+)로 트래픽 폭증 시 100ms 내 신규 실행 환경 기동
- **비용 효율**: 월 100만 회 호출 + 400,000 GB-초 무료 tier, 0 idle cost
- **운영 단순화**: OS 패치, AMI 빌드, Auto Scaling 정책, Capacity Reservation 불필요
- **이벤트 네이티브 통합**: 20+ AWS 서비스(S3, DynamoDB, Kinesis, SQS, EventBridge)와 직접 트리거
- **Green IT**: 미사용 자원 자동 회수로 데이터센터 PUE 절감

- **📢 섹션 요약 비유**: 전통적 서버는 "24시간 영업하는 식당"(한 명도 없어도 전기·가스비 발생)이고, FaaS는 "배달의민족 주문 들어올 때만 요리사가 나타나서 요리하고 떠나는 스마트 키친(주문 기반 자동 호출)"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FaaS의 핵심은 **이벤트 소스(Event Source)** -> **호출 매개체(Invocation Layer)** -> **함수 런타임(Function Runtime)** -> **내부·외부 리소스 트랜잭션**의 4단 분리 아키텍처다. AWS 기준으로 Lambda는 내부적으로 마이크로 VM(Firecracker, <5ms 부팅) 또는 Sandboxed Container(EBS, 2024 GA)에서 실행되며, 실행 컨텍스트는 동일 인스턴스에서 재사용(Execution Context Reuse)되어 /tmp 스토리지·DB Connection·SDK Client를 warm-up 한다.

```text
[Lambda 이벤트 드리븐 내부 동작 흐름 - 동기 vs 비동기 vs Poll-Based]

  +-----------------+
  |  Event Sources  |
  |  --------------  |
  | • S3 PutObject  | (동기식 매핑, Lambda 호출 권한 IAM 필요)
  | • API Gateway   | (동기식, RequestResponse)
  | • DynamoDB Streams | (이벤트 소스 매핑, 샤드 기반 폴링)
  | • SQS Standard  | (이벤트 소스 매핑, Long Polling 20s)
  | • EventBridge   | (비동기식 push, Dead Letter Queue 지원)
  | • Kinesis       | (이벤트 소스 매핑, 체크포인트 기반)
  | • Kafka (MSK)   | (이벤트 소스 매핑, Consumer Group)
  | • SNS           | (비동기식 push, Fan-out)
  | • Schedule(CRON)| (EventBridge Scheduler, at(즉시 1회))
  +--------+--------+
           |
           v
  +------------------------------------------------------+
  |           AWS Lambda Service Plane                    |
  |  +----------------------------------------------+    |
  |  | 1) Invoke Layer (호출 라우팅 및 인증)        |    |
  |  |    - IAM Auth, Resource Policy               |    |
  |  |    - 큐 버퍼링(비동기), 재시도 정책(DLQ)      |    |
  |  +------------------+---------------------------+    |
  |                     v                                |
  |  +----------------------------------------------+    |
  |  | 2) Worker Manager (실행 환경 할당)           |    |
  |  |    - Init Phase: Cold Start 100~800ms        |    |
  |  |    - /tmp 512MB, 128MB~10GB(EBS)             |    |
  |  |    - ENI 트래픽 (VPC Lambda 3~8s 추가)       |    |
  |  +------------------+---------------------------+    |
  |                     v                                |
  |  +----------------------------------------------+    |
  |  | 3) Runtime (Firecracker MicroVM/Container)   |    |
  |  |    - handler(event, context) 실행             |    |
  |  |    - Billed Duration (ms 단위)                |    |
  |  |    - Timeout: 15분(Lambda), 60분(Step Fn)    |    |
  |  +------------------+---------------------------+    |
  |                     v                                |
  |  +----------------------------------------------+    |
  |  | 4) Destination (결과 라우팅)                  |    |
  |  |    - Success: Target Lambda/SQS/SNS/EventBus |    |
  |  |    - Failure: DLQ + EventBridge (Lambda Dest) |    |
  |  +----------------------------------------------+    |
  +------------------------------------------------------+
           |
           v (함수 내부)
  +-----------------+    +-----------------+    +-----------------+
  |  AWS SDK v3     |    |  외부 시스템     |    |  BaaS           |
  |  --------------- |    |  --------------  |    |  --------------  |
  | • DynamoDB      |◄--►| • HTTP API       |    | • Aurora Serverless|
  | • S3            |    | • gRPC           |    | • DynamoDB      |
  | • RDS Proxy     |    | • SaaS Webhook   |    | • S3            |
  | • ElastiCache   |    |   (Slack, Twilio)|    | • Cognito       |
  +-----------------+    +-----------------+    +-----------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Event Source Mapping (ESM)** | 스트림/큐 기반 이벤트 자동 폴링 | Kinesis·DynamoDB Streams·SQS·Kafka·MQ에서 Lambda가 consumer group으로 poll, 배치 윈도우(0~300s)와 배치 크기(1~10,000) 설정, 체크포인트(Shard Iterator) 기반 at-least-once 전달 |
| **IAM Execution Role** | 함수 내부 AWS 리소스 접근 권한 | 최소 권한 원칙(Least Privilege) 적용, `lambda:InvokeFunction` 호출 권한과 분리, Resource-based Policy로 다른 계정/Cross-Account 호출 제어 |
| **Lambda Layer** | 공통 의존성(SDK, Pandas, FFmpeg) 공유 | 5개 레이어, 각 250MB unzipped, /opt 경로 마운트, 컨테이너 이미지(ECR) 기반 배포 시 제약 해소 |
| **Concurrency & Throttling** | 동시 실행 제어 | Reserved Concurrency(함수별 격리), Provisioned Concurrency(warm 인스턴스 사전 할당, SnapStart와 결합 시 cold start 0ms), 계정 기본 1,000 quota |
| **Destinations & DLQ** | 비동기 실패 핸들링 | on-failure 시 SQS/SNS/EventBridge/Lambda로 페이로드 전송, 재시도 정책 0~2회 + 지수 백오프, EventBridge를 통한 통합 관측 |
| **Observability (X-Ray + CloudWatch)** | 분산 트레이싱 | AWS X-Ray SDK로 upstream/downstream trace, CloudWatch Logs Insights로 구조화 로그 쿼리, Lambda Insights로 메모리/CPU/네트워크 메트릭, OpenTelemetry Lambda Layer로 vendor-neutral 지원 |
| **VPC Integration** | 프라이빗 리소스 접근 | Hyperplane ENI(2020~)로 NAT 비용/콜드스타트 개선, RDS Proxy·AWS PrivateLink 통해 DynamoDB Streams, Lambda가 VPC 내부 RDS에 connection pooling |
| **State Manager** | Stateless 제약 해결 | DynamoDB(키-값), ElastiCache Redis(세션), S3(객체), Step Functions(워크플로 상태), 외부 SaaS(AirTable, FaunaDB)로 상태 영속화 |

**핵심 원리 심화:**

1. **콜드 스타트 최적화**: Firecracker 기반 마이크로VM은 평균 100~200ms로 부팅하며, Provisioned Concurrency(상시 Warm Pool, 비용 $0.015/GB-시간) + Lambda SnapStart(2022년 발표, Java/Python/.NET 초기화 결과 캐싱, 10x 개선)로 200~500ms -> 50ms 이하로 단축. Java의 JVM 클래스 로딩이 주요 병목이며, GraalVM Native Image로 Ahead-of-Time 컴파일 시 100ms 이하 달성 가능.

2. **이벤트 라우팅 패턴**:
   - **Pub/Sub Fan-out**: SNS Topic -> 다수 Lambda/SQS Fan-out (알림 시스템)
   - **Event Sourcing**: DynamoDB Streams -> Lambda Projector -> Read Model (CQRS)
   - **Saga Orchestration**: Step Functions + Lambda 보상 트랜잭션 (분산 트랜잭션)
   - **Choreography**: EventBridge + 다수 Lambda가 비동기 협력 (느슨한 결합)
   - **Strangler Fig**: API Gateway + Lambda로 모놀리식 점진적 분리

3. **과금 모델**: $0.20/1M 요청 + $0.0000166667/GB-초(x86), ARM/Graviton2 $0.0000133334/GB-초로 19% 저렴, 128MB 단위 메모리(128MB~10,176MB)에 비례.

4. **동시성 수식**: 동시 실행 수 = (요청량 RPS) × (평균 실행 시간 초). 예: 100 RPS × 0.5s = 50 동시성 필요, Reserved Concurrency로 격리 시 노이즈 함정(throttling) 방지.

- **📢 섹션 요약 비유**: FaaS 호출은 "택배 주문처럼, 주문(Trigger) 들어오면 창고(Event Source)에서 물건(데이터)을 꺼내 작업자(Lambda)에게 전달하고, 작업자는 짐을 처리한 후 배송(Destination)으로 보내는 이벤트 드리븐 파이프라인"이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **FaaS (Lambda 등)** | **CaaS (EKS/ECS + Fargate)** | **PaaS (App Runner/Beanstalk)** | **BaaS (DynamoDB, S3, Cognito)** |
| :--- | :--- | :--- | :--- | :--- |
| **추상화 수준** | 함수 단위 (가장 높음) | 컨테이너/파드 단위 | 애플리케이션 단위 | 데이터/API 단위 |
| **실행 시간 한도** | 15분 (강제) | 무제한 | 무제한 | N/A (관리형) |
| **콜드 스타트** | 100ms~수 초 (핵심 트레이드오프) | 수 초 (이미지 풀) | 수십 초 | 없음 (HTTP) |
| **상태 관리** | Stateless (외부 의존 필수)