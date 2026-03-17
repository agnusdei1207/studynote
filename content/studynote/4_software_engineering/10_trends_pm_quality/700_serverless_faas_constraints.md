+++
title = "700. 서버리스 FaaS 아키텍처 제약"
date = "2026-03-15"
weight = 700
[extra]
categories = ["Software Engineering"]
tags = ["Serverless", "FaaS", "Cloud Native", "Cold Start", "Execution Limits", "Vendor Lock-in"]
+++

# 700. 서버리스 FaaS 아키텍처 제약

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이벤트에 의해 기동되고 실행 완료 후 즉시 소멸하는 **상태 비저장(Stateless) 함수** 단위의 컴퓨팅 모델로, 운영 오버헤드를 극단적으로 줄이지만 설계상 엄격한 제약 조건을 동반한다.
> 2. **주요 제약**: 오랫동안 호출되지 않은 함수 실행 시 발생하는 **콜드 스타트(Cold Start)** 지연, 짧은 최대 실행 시간(Timeout), 메모리 및 임시 저장 공간의 물리적 한계가 존재한다.
> 3. **가치**: 제약 사항을 극복하기 위한 비동기 설계와 상태 외부화(BaaS 활용)를 통해, 인프라 관리 부담 없이 무한 확장이 가능한 **경제적·탄력적 클라우드 아키텍처**를 실현한다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 정의 및 철학
**FaaS (Function as a Service)**는 클라우드 네이티브 컴퓨팅의 정점에 있는 실행 모델로, 개발자가 서버의 프로비저닝, 관리, 스케일링을 전혀 신경 쓰지 않고 코드(Function)만 배포하여 실행하는 아키텍처 패턴입니다. 여기서 핵심은 '서버리스(Serverless)'라는 용어가 서버가 존재하지 않음을 의미하는 것이 아니라, **서버의 존재와 관리가 사용자에게 완전히 추상화(Abstraction)**되었음을 의미합니다. 이 모델은 기본적으로 **Ephemeral (일시적)** 특성을 가지며, 실행 환경은 호출 시 생성되었다가 응답 후 즉시 회수됩니다. 이 과정에서 발생하는 자원 할당의 불확실성과 상태 유지의 불가능성이 곧 아키텍처적 제약으로 이어집니다.

### 2. 등장 배경 및 패러다임 변화
전통적인 **MSA (Microservices Architecture)**는 서비스를 잘게 쪼개더라도 각 서비스가 실행되는 '가상머신(VM)'이나 '컨테이너'를 운영자가 직접 관리해야 하는 부담이 있었습니다. FaaS는 이를 **함수(Function)** 단위까지 쪼개어 인프라 관리의 책임을 클라우드 공급자(CSP)에게 완전히 위임합니다. 이로 인해 개발자는 비즈니스 로직에만 집중할 수 있게 되었으나, 대가로 인프라에 대한 통제권을 상실하고 플랫폼이 제시하는 엄격한 실행 한계(Limits) 내에서 설계해야 하는 **트레이드오프(Trade-off)**가 발생합니다.

### 3. ASCII 다이어그램: 서버리스 추상화 레이어

```text
     [ 사용자 관점 ]              [ 실제 물리/가상 인프라 ]
┌─────────────────────┐       ┌──────────────────────────────┐
│   Developer Code    │       │  Cloud Provider (CSP) Side    │
├─────────────────────┤       ├──────────────────────────────┤
│                     │       │                              │
│  function.py │      │       │  ┌─────────────────────────┐ │
│  async def      │   │       │  │  Container Orchestrator│ │
│  handler(event):────┼───────┼─▶│  (Kubernetes-like)      │ │
│      return x      │       │  │  ┌─────────────────────┐│ │
│                     │       │  │  │  Function Instance ││ │
└─────────────────────┘       │  │  │  (Sandboxed Env)   ││ │
                              │  │  │  [Code Download]   ││ │
                              │  │  │  [Exec Limits]     ││ │
                              │  │  │  [Auto Scaling]    ││ │
                              │  │  └─────────────────────┘│ │
                              │  └─────────────────────────┘ │
                              └──────────────────────────────┘
```
*(도해 해설: 개발자는 단순히 코드 파일만 업로드하지만, 실제로는 그 뒤에서 수많은 컨테이너 오케스트레이션이 동작합니다. 그러나 개발자는 이 복잡한 인프라 계층을 전혀 볼 수 없으며, 오직 함수의 입력과 출력에만 집중하게 됩니다.)*

### 📢 섹션 요약 비유
> 마치 자동차 렌탈 서비스에서 '단기 대여'를 이용하는 것과 같습니다. 사용자는 차량이 어떻게 정비되고 관리되는지 알 필요 없이 단지 운전(코드 실행)만 하면 됩니다. 하지만 렌탈료를 아끼기 위해 차량을 반납해야 하듯, 실행이 끝나면 즉시 차량(서버)이 회수되므로 개인 물건(상태)을 트렁크에 두고 내릴 수 없는 것이 서버리스의 핵심 제약입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. FaaS의 5대 핵심 기술적 제약 상세 분석

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 주요 프로토콜/제약 (Constraints) | 기술적 비유 |
|:---|:---|:---|:---|:---|
| **Execution Environment** | 함수 실행 샌드박스 | 보안을 위해 격리된 컨테이너(or VM) 내에서 동작 | CPU/메모리 제한 (e.g., AWS Lambda 최대 10GB) | 반지하 방의 화로 |
| **Event Trigger** | 함수 기동 시그널 | API Gateway, S3, SQS 등의 이벤트 수신 | 동기식(Sync) / 비동기식(Async) | 방문자 초대장 |
| **State Management** | 데이터 일관성 유지 | 내부 디스크 변조 불가, 외부 저장소 의존 | `/tmp` 제약 (512MB 등), Stateless 강제 | 임시 탈의실 |
| **Scaling Controller** | 인스턴스 수 조절 | 동시 요청(Concurrency)에 따라 인스턴스 증설 | 동시성 한계(Concurrent Limit) | 주차장 관리인 |
| **Scheduler** | 리소스 할당 및 회수 | 요청이 없으면 인스턴스 종료(Freeze) → **Cold Start** 유발 | Timeout (최대 실행 시간, 보통 15분) | 알바생 근무 스케줄 |

### 2. 콜드 스타트(Cold Start) 메커니즘 및 수식
**콜드 스타트**는 함수 호출 요청이 들어왔을 때 실행 가능한 인스턴스가 없어, 새로운 컨테이너를 생성하고 런타임(Runtime, e.g., Node.js, Python)을 로드한 뒤 코드를 초기화하는 과정에서 발생하는 지연 시간입니다.

$$ T_{total} = T_{request} + T_{queue} + (T_{create\_container} + T_{runtime\_init} + T_{code\_load}) + T_{exec} $$

만약 기존의 '따뜻한(Warm)' 인스턴스가 있다면 중간 괄호 부분은 0에 수렴합니다.

```text
┌─────────────────── SERVERLESS INVOCATION LIFECYCLE ───────────────────┐
│                                                                         │
│  1. REQUEST          2. QUEUE              3. WORKER ASSIGNMENT        │
│  [User/API] ────────▶ [Load Balancer] ───────▶ [Worker Manager]        │
│                            │                        │                   │
│                            │                        ▼                   │
│  ◀──────── Response        │                 4. EXECUTION PHASE         │
│     (Latency)              │            ┌───────────────────────┐       │
│                            │            │   IF Warm Instance?   │       │
│                            │            │   └─▶ Run Code (0ms)  │       │
│                            │            │   ELSE                │       │
│                            │            │   ┌─────────────────┐ │       │
│                            │            └──▶ **COLD START**   │ │       │
│                            │                 │ 1. Alloc Container│       │
│                            │                 │ 2. Start Runtime │       │
│                            │                 │ 3. Load User Code│       │
│                            │                 │ 4. Init Function │ │       │
│                            │                 │ (Total: ~500ms+) │ │       │
│                            │                 └─────────────────┘ │       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. 핵심 알고리즘: 예약된 동시성(Provisioned Concurrency)
콜드 스타트를 방지하기 위해 AWS Lambda 등에서 제공하는 기능입니다. 항상 일정 수의 인스턴스를 실행 준비 상태(Warm)로 유지합니다.

```python
# Pseudo-code: Worker Logic with State Awareness
class FaaSWorker:
    def __init__(self):
        self.state = "COLD"  # Initial state
    
    def handle_request(self, event):
        # 1. Check Initialization Status
        if self.state == "COLD":
            self.load_runtime()     # Latency Penalty
            self.load_dependencies()
            self.init_static_vars() # Heavy lifting
            self.state = "WARM"
        
        # 2. Execute Business Logic (Fast in WARM state)
        return self.process(event)

    def freeze(self):
        # Called by Platform when idle
        self.state = "FROZEN" # May become COLD if evicted
```

### 📢 섹션 요약 비유
> 마치 자동판매기의 음료수 보충 과정과 같습니다. 손님이 왔을 때(이벤트) 칸이 비어 있으면 직원이 와서 음료수를 채워 넣어야 하므로 손님은 기다려야 합니다(**콜드 스타트**). 만약 미리 칸을 채워두면(**Provisioned Concurrency**) 즉시 음료수를 뽑을 수 있지만, 그만큼 보관 비용(유휴 비용)이 발생합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 컨테이너(K8s) vs 서버리스(FaaS) 심층 기술 비교

| 비교 지표 (Metrics) | 컨테이너 (Kubernetes / Docker) | 서버리스 (FaaS) | 기술사적 분석 (PE Analysis) |
|:---|:---|:---|:---|
| **실행 지연 (Latency)** | **ms 단위** (항상 Running 상태) | **수백 ms ~ 수초** (콜드 스타트 가능) | 실시간 트레이딩 시스템 등 Latency 민감 서비스는 FaaS 부적합 |
| **상태 저장 (Stateful)** | PVC(Persistent Volume Claim) 등으로 영속 저장 가능 | **완전 불가** (Ephemeral) | 상태를 가진 장기 작업은 DB(RDS) 등 외부 의존성 필수 |
| **실행 시간 제약** | **무제한** (OS 재부팅 주기까지만) | **짧음** (AWS: 15분, Azure: 10분) | 비디오 렌더링 같은 Heavy 배치 작업은 분할(Splitting) 필요 |
| **비용 구조 (Cost)** | Pod/Node 할당량 기반 (Idle 시간도 과금) | **실제 실행 시간 + 요청 수** 기반 | 트래픽 변동이 극심한 서비스는 FaaS가 비용 효율적 |
| **제어 수준 (Control)** | OS 레벨 설정, 특정 라이브러리 설치 자유로움 | **제한적** (Layer 기반 배포) | 보안 패치나 특정 모듈 설치가 제한될 수 있음 |

### 2. 기술적 시너지 및 과목 융합 분석

#### A. 이벤트 기반 아키텍tura (EDA)와의 결합
FaaS는 **MSA (Microservices Architecture)**의 다음 단계로서, **EDA (Event-Driven Architecture)**와 가장 시너지가 높습니다.
- **연관성**: 함수는 이벤트(Message Queue, Stream)를 기다리는 **Listener**로 동작합니다.
- **효과**: 결합도가 낮아져(Loose Coupling), 특정 함수의 장애가 전체 시스템을 멈추지 않게 합니다.

#### B. 데이터베이스(DB)와의 연동: 'Backpressure' 처리
대량의 트래픽이 몰릴 때 FaaS가 순간적으로 수천 개의 인스턴스를 생성하여 데이터베이스에 연결을 시도하면, **DB Connection Pool** 고갈로 인한 장애가 발생할 수 있습니다.
- **해결책**: 중간에 **Message Queue (SQS, Kafka)**를 두어 FaaS가 DB를 직접 핑(Ping)하지 않고, 큐를 통해 일정 속도로만 처리하게 하여 **Backpressure**를 제어해야 합니다.

```text
┌──────────────┐         ┌───────────────────────┐         ┌───────────────┐
│   User Load  │────▶    │   Message Queue       │────▶    │   FaaS Pool   │
│   (Spike)    │         │   (Buffer/Throttle)   │         │   (Workers)   │
└──────────────┘         └───────────────────────┘         └───────┬───────┘
                                                                │
                                                                ▼
                                                         [Rate Limited]
                                                                ▼
                                                         ┌─────────────────┐
                                                         │  Primary DB     │
                                                         │  (Protected)    │
                                                         └─────────────────┘
```

### 📢 섹션 요약 비유
> 콜드 스타트 문제는 쉬는 시간이 긴 운동선수가 경기에 투입되는 것과 같습니다. 준비 운동(Warming) 없이 투입되면 처음에는 몸이 굳어 있어 기량을 발휘하기 어렵습니다. 이를 해결하기 위해 '예약된 선수(Provisioned Concurrency)'를 항상 그라운드에 두거나, 경기를 짧게 쪼개어(Step Functions) 체력 소모를 분산하는 전략이 필요합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 및 의사결정 프로세스

**상황:** 초대형 이커머스 플랫폼의 '주문 배치 작업(Batch Job)' 설계
- **요구사항**: 매일 자정에 100만 건의 주문 데이터를 집계하여 리포트 생성. 최대 2시간 이내 완료 필요.
- **문제 제기**: 단일 FaaS 함수로 처리 시 15분 Timeout 위배, DB Lock 발생 우려.

**의사결정 매트릭스 (Decision Matrix)**

| 옵션 (Option) | 실행 시간 (Time) | 비용 (Cost) | 복잡도 (Complexity) | 결론 (Verdict) |
|:---|:---:|:---:|:---:|:---:|
| **단일 EC2 장비 활용** | 1.5시간 (종속적) | 저렴