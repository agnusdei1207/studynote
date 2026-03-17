+++
title = "도메인 13: 클라우드 아키텍처 (Cloud Architecture)"
render = true
paginate_by = 10
sort_by = "weight"
insert_anchor_links = "right"
[extra]
category = "studynotes-cloud-architecture"
kids_analogy = "내 방에 무거운 컴퓨터를 사두는 대신, 하늘에 있는 아주 크고 강력한 슈퍼컴퓨터를 필요할 때만 빌려 쓰고 돈을 내는 '컴퓨터 렌탈 서비스'예요. 갑자기 친구 100명이 놀러 와도 버튼 하나면 1초 만에 방이 100개로 늘어난답니다!"
+++

# 도메인 13: 클라우드 아키텍처 (Cloud Architecture)

## ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인터넷을 통해 컴퓨팅 자원(서버, 스토리지, 네트워크)을 가상화하여, 요구사항에 맞춰 즉시 프로비저닝하고 사용한 만큼만 비용을 지불하는 On-Demand IT 인프라 패러다임.
> 2. **가치**: Auto-scaling과 무한한 확장성을 통해 하드웨어 프로비저닝 병목을 파단하고, 자본적 지출(CAPEX)을 운영적 지출(OPEX)로 전환하여 비즈니스 Time-to-Market을 극도로 단축시킴.
> 3. **융합**: 컨테이너(Docker), 오케스트레이션(Kubernetes), 마이크로서비스(MSA)와 결합하여 '클라우드 네이티브(Cloud-Native)'라는 궁극의 분산 애플리케이션 생태계를 완성함.

---

### Ⅰ. 개요 (Context & Background)
과거 기업들은 트래픽의 최고점(Peak)을 예상하여 막대한 비용을 들여 자체 데이터센터(On-premise)에 서버를 선제적으로 구매했다(Over-provisioning). 그러나 평상시에는 서버의 90%가 유휴 상태로 방치되어 전력과 공간을 낭비하는 치명적 비효율을 낳았다. 
**클라우드 컴퓨팅(Cloud Computing)**은 가상화(Virtualization) 기술을 통해 물리적 하드웨어를 논리적 자원으로 쪼개어, 수도나 전기처럼 '원하는 시점에 원하는 만큼만 꺼내 쓰는' 유틸리티 컴퓨팅의 이상을 실현했다. 오늘날의 클라우드는 단순한 인프라 대여(IaaS)를 넘어, 머신러닝 가속기, 서버리스 함수(FaaS), 전사적 데이터 웨어하우스를 API 형태로 제공하며 현대 IT 아키텍처의 근간(Backbone)으로 완전히 결착되었다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

클라우드의 핵심은 모든 인프라를 '코드(IaC, Infrastructure as Code)'로 정의하고 제어할 수 있는 추상화 계층에 있다.

#### 1. 핵심 공학 도메인
| 도메인 | 상세 역할 | 내부 동작/활용 기법 | 관련 서비스 및 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **IaaS/PaaS/SaaS** | 클라우드 서비스 모델 | 관리 책임(Shared Responsibility)의 분할 | AWS EC2, Heroku, Salesforce | 빈 땅 vs 풀옵션 아파트 |
| **Cloud Native** | 클라우드 환경에 최적화된 설계 | 12-Factor App, 컨테이너, CI/CD 파이프라인 | Docker, Kubernetes | 모듈식 레고 블록 |
| **Serverless** | 인프라 관리의 완전한 은폐 | 이벤트 구동 방식(Event-driven) 함수 실행 | AWS Lambda, KNative | 자판기(누를 때만 동작) |
| **Microservices (MSA)**| 독립적이고 배포 가능한 서비스 분할 | 도메인 주도 설계(DDD), API Gateway | Spring Cloud, Istio | 각각 독립된 상점들 |
| **Migration & FinOps**| 클라우드 전환 및 비용 통제 | 6R 전략(Replatform, Refactor 등), 비용 최적화 | AWS Migration Hub, Spot Instance | 거대한 이사 및 회계 |

#### 2. 쿠버네티스(Kubernetes) 오케스트레이션 아키텍처 (ASCII)
클라우드 네이티브의 사실상(De facto) 운영체제인 쿠버네티스의 Control Plane과 Worker Node 구조다.
```text
    [ Kubernetes (K8s) Cluster Architecture ]
    
    (Control Plane - Master)
    +-------------------------------------------------------------+
    |  [ API Server ] <--- (kubectl / CI/CD Pipeline)             |
    |       |                                                     |
    |  +----v-----+    +-------------+    +--------------------+  |
    |  | etcd (DB)|    | Controller  |    | Scheduler          |  |
    |  +----------+    +-------------+    +--------------------+  |
    +-------|-----------------|----------------------|------------+
            | (gRPC 통신)     |                      |
    ========v=================v======================v=============
    (Worker Node 1)                        (Worker Node 2)
    +----------------------------------+   +----------------------+
    | [ Kubelet ]  [ Kube-proxy ]      |   | [ Kubelet ]          |
    |   +--------------------------+   |   |   +--------------+   |
    |   | Pod A (App + Sidecar)    |   |   |   | Pod C (DB)   |   |
    |   +--------------------------+   |   |   +--------------+   |
    |   +--------------------------+   |   |                      |
    |   | Pod B (App + Sidecar)    |   |   |  [ Container Runtime ]
    |   +--------------------------+   |   +----------------------+
    |  [ Container Runtime (containerd)]                          |
    +----------------------------------+                          |
```

#### 3. 서킷 브레이커 (Circuit Breaker) 알고리즘 논리
MSA 환경에서 하나의 서비스 장애가 전체 시스템으로 전파(Cascading Failure)되는 것을 막는 방파제 로직.
- **Closed (정상)**: 모든 요청이 통과. 에러율이 임계치(예: 50%)를 넘으면 `Open` 상태로 전환.
- **Open (차단)**: 요청을 즉시 거절(Fast Fail)하여 타겟 서비스가 회복할 시간을 줌.
- **Half-Open (반열림)**: 일정 시간(Timeout) 후 일부 요청만 흘려보내 정상 응답이 오면 `Closed`, 실패하면 다시 `Open`으로 회귀.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 애플리케이션 아키텍처: Monolithic vs MSA vs Serverless
| 비교 항목 | 모놀리식 (Monolithic) | 마이크로서비스 (MSA) | 서버리스 (Serverless/FaaS) |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 거대한 단일 아카이브 (WAR/JAR) | 도메인별 분할된 컨테이너 (Image) | 단일 함수 단위 (Function) |
| **확장성(Scale)** | 전체 시스템 복제 필요 (자원 낭비) | 부하가 심한 특정 서비스만 개별 확장 | 1요청 1인스턴스, 무한 자동 확장 |
| **운영 복잡도** | 낮음 (테스트 및 모니터링 용이) | **극도로 높음** (네트워크 지연, 분산 트랜잭션) | 인프라 관리 없음 (클라우드 제공자 위임) |
| **상태(State)** | 메모리 내 세션 상태 공유 가능 | Stateless 지향, 외부 DB/캐시로 상태 위임 | 완벽한 Stateless 강제 (Cold Start 이슈) |

#### 2. 클라우드 마이그레이션 전략 (6R) 핵심 비교: Rehost vs Refactor
| 항목 | Rehost (Lift & Shift) | Refactor (Cloud Native) |
| :--- | :--- | :--- |
| **방식** | 온프레미스 VM을 그대로 클라우드 IaaS로 복사 | 코드를 전면 재작성하여 PaaS/SaaS/서버리스 도입 |
| **마이그레이션 기간**| 매우 짧음 (수 주 이내) | 매우 긺 (수개월 ~ 수년) |
| **클라우드 이점 활용**| 낮음 (단순 인프라 교체) | **최고 (Auto-scaling, Managed DB 100% 활용)** |
| **운영 비용(OPEX)** | 기존과 유사하거나 더 비쌀 수 있음 | 트래픽에 최적화되어 장기적 비용 급감 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1: 대규모 트래픽 폭주 (Ticketing System) 아키텍처 방어**
- **문제 상황**: 명절 기차표 예매 오픈 시점에 평소 대비 1,000배의 트래픽이 쏟아져 들어와 Web/WAS 서버가 다운되고 DB 커넥션 풀이 마비됨.
- **기술사적 결단**: K8s의 HPA(Horizontal Pod Autoscaler) 설정만으로는 트래픽 폭발 속도를 따라잡지 못한다. 따라서, 앞단에 **대기열(Queue) 시스템(Redis, Kafka)**을 배치하여 초당 DB 인입량을 제한(Rate Limiting)하고, 읽기 부하를 막기 위해 **CQRS(Command and Query Responsibility Segregation)** 패턴을 적용하여 DB의 Read Replica와 ElastiCache로 트래픽을 완벽히 분산시킨다.

**시나리오 2: 멀티/하이브리드 클라우드 종속성(Lock-in) 타파**
- **문제 상황**: 특정 클라우드(예: AWS)의 완전 관리형 서비스(DynamoDB, SQS)에 깊게 결합되어 코드가 작성된 탓에, 클라우드 벤더의 가격 인상 시 타사로의 이전이 불가능함.
- **기술사적 결단**: 벤더 종속성을 끊기 위해 **헥사고날 아키텍처(Hexagonal Architecture)**를 적용하여 비즈니스 로직과 인프라 어댑터를 분리한다. 인프라 배포는 **Terraform(IaC)**으로 추상화하고, 애플리케이션 컨테이너는 벤더 중립적인 **Kubernetes** 클러스터 위에 배포하여 언제든 AWS에서 GCP나 온프레미스로 무중단 롤오버(Failover)할 수 있는 하이브리드 아키텍처를 강제한다.

**도입 시 고려사항 (안티패턴)**
- **클라우드 낭비 (Zombie Cloud Anti-pattern)**: "클라우드는 무조건 싸다"는 착각. 사용하지 않는 개발/테스트용 EC2 인스턴스를 주말에도 켜두거나, 과도하게 프로비저닝된(Over-provisioned) RDS를 방치하면 한 달 뒤 상상 초월의 청구서(Bill Shock)를 맞게 된다. 기술사는 **FinOps** 조직을 신설하고 태깅(Tagging) 정책을 강제하여 비용 가시성을 100% 확보해야 한다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**정량적 기대효과 (ROI)**
| 아키텍처 혁신 요소 | 타겟 비즈니스 지표 | 정량적 개선 효과 (ROI) |
| :--- | :--- | :--- |
| **서버리스(Lambda) 전환** | 예측 불가능한 간헐적 배치 작업 | 대기 전력 제로화로 인프라 비용 **최대 80% 절감** |
| **IaC (Terraform) 도입** | 인프라 프로비저닝 속도 및 휴먼 에러 | 새로운 환경 구축 시간 2주 $\rightarrow$ **10분 내 완수** |
| **Multi-AZ / Multi-Region** | 글로벌 서비스 가용성 (Availability) | 재해 발생 시 RTO 0초 달성, 99.999% (Five Nines) 보장 |

**미래 전망 및 진화 방향**:
클라우드는 중앙 집중형 하이퍼스케일을 넘어, 데이터가 발생하는 곳에서 직접 연산하는 **분산 클라우드(Distributed Cloud)**와 **엣지 컴퓨팅(Edge Computing)**으로 팽창하고 있다. 또한 클라우드의 모든 설정과 보안, 성능 튜닝을 AI가 자율적으로 조절하는 **지능형 클라우드 제어(Autonomous Cloud)** 시대가 도래하여 아키텍트의 수작업을 완전히 압살할 것이다.

**※ 참고 표준/가이드**:
- CNCF (Cloud Native Computing Foundation) Landscape: 클라우드 네이티브 생태계의 오픈소스 기술 표준 나침반.
- NIST SP 800-145: 클라우드 컴퓨팅의 핵심 특징, 서비스 모델을 정의한 글로벌 참조 표준.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [`[마이크로서비스 아키텍처(MSA)]`](@/PE/4_software_engineering/_index.md): 클라우드의 확장성을 100% 뽑아내기 위한 소프트웨어 공학적 설계 철학.
- [`[가상 메모리와 하이퍼바이저]`](@/PE/2_operating_system/10_security_virtualization/_index.md): 클라우드 IaaS를 가능하게 만든 하드웨어 위 OS 레벨의 격리 기술.
- [`[데브옵스(DevOps)와 CI/CD]`](@/PE/15_devops_sre/_index.md): 클라우드에 하루 수백 번 코드를 배포하고 운영하기 위한 자동화된 문화와 파이프라인.
- [`[분산 데이터베이스(NewSQL)]`](@/PE/5_database/_index.md): 클라우드의 무한한 스케일아웃에 맞춰 트랜잭션을 분산 보장하는 차세대 저장소.
- [`[제로 트러스트 아키텍처]`](@/PE/9_security/_index.md): 방화벽이 사라진 클라우드 환경에서 엔드포인트와 API를 지키기 위한 보안 패러다임.