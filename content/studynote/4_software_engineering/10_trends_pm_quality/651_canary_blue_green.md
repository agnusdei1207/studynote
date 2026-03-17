+++
title = "651. 카나리 배포 / 블루-그린 배포 무중단"
date = "2026-03-15"
weight = 651
[extra]
categories = ["Software Engineering"]
tags = ["DevOps", "Deployment", "Canary", "Blue-Green", "Zero Downtime", "Release Engineering"]
+++

# 651. 카나리 배포 / 블루-그린 배포 무중단

## 핵심 인사이트 (3줄 요약)
> 1. **본질 (Essence)**: 시스템의 가용성(Availability)을 100% 유지하며 신규 버전으로 교체하는 **무중단 배포(Zero Downtime Deployment)** 전략으로, 'Rollback'의 안전성과 'Risk Blast Radius'의 제어가 핵심 기술적 과제이다.
> 2. **가치 (Value)**: **MTTR (Mean Time To Recovery)**을 획기적으로 단축(분 단위 → 초 단위)하여 비즈니스 연속성을 보장하고, **TTM (Time To Market)**을 가속화하여 경쟁 우위를 점하게 한다.
> 3. **융합 (Convergence)**: **K8s (Kubernetes)**의 트래픽 분산 기능, **Service Mesh**의 L7 트래픽 제어, **DB Schema Migration**의 순차적 처리 기술이 유기적으로 결합되어야 안정적인 구현이 가능하다.

---

### Ⅰ. 개요 (Context & Background)

**1. 개념 및 철학**
무중단 배포는 소프트웨어 업데이트 과정에서 서비스 중단(Downtime)을 0으로 만드는 것을 목표로 한다. 전통적인 'Stop → Deploy → Start' 방식인 **Blue/Green Deployment (블루-그린 배포)**는 현재 운영 환경(Blue)과 동일한 새로운 환경(Green)을 구축하여 라우팅을 스위칭하는 방식이며, 문제 발생 시 즉시 원복(Pivot)이 가능한 것이 특징이다. 반면, **Canary Deployment (카나리 배포)**는 광산의 카나리아새隐喻에서 유래하여, 신규 버전을 전체 트래픽의 소수(예: 1~5%)에게만 노출시켜 실제 운영 부하하에서 안정성을 검증한 후 점진적으로 확대하는 전략이다.

**2. 등장 배경 및 패러다임 변화**
과거 모놀리식(Monolithic) 아키텍처에서는 릴리즈 주기가 월/단위였으나, MSA(Microservices Architecture)와 **CI/CD (Continuous Integration/Continuous Deployment)**의 도입으로 하루에 수십 번의 배포가 이루어지는 'Continuous Delivery' 환경으로 변화했다. 이에 따라 배포로 인한 장애가 전체 서비스로 확산되는 것을 막고, **변화 관리(Change Management)**의 리스크를 최소화하기 위한 전략적 배포 기법의 필요성이 대두되었다.

```text
     [ Evolution of Deployment Strategy ]
     
  Static      Rolling         Blue-Green        Canary (A/B)
  (Stop)      (Partial)      (Switch)          (Gradual)
    │           │               │                 │
    ▼           ▼               ▼                 ▼
  [DOWN]   [V1][V2][V1]    [V1] | [V2]      [V1] | [V2(1%)]
            ---             ---   ---         ---   ---
           (Risk)          (Fast Rbk)      (Safe Analysis)
```

**💡 비유: 고속도로 톨게이트 차선 변경**
블루-그린 배포는 기존 톨게이트 부지 옆에 완전히 새로운 부지를 다시 만들어놓고, 차량을 한꺼번에 새 도로로 돌리는 것과 같다. 문제가 생기면 즉시 옆길로 돌리면 되므로 통행 요금 징수가 멈추지 않는다. 카나리 배포는 기존 10개 차선 중 1개 차Line만 신형 하이패스 시스템으로 바꿔서, 속도나 오류 여부를 확인하며 나머지 차선도 순차적으로 바꾸는 것과 같다.

**📢 섹션 요약 비유**
> 마치 비행기가 착륙 후 엔진을 끄지 않고도 연료를 공급하고 엔진을 교체할 수 있도록, **'공중 급유'** 시스템을 도입하여 여객기(서비스)가 하늘에서 떠 있는 상태를 유지하게 하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**1. 핵심 구성 요소 (Component Analysis)**

| 요소명 | 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 |
|:---|:---|:---|:---|
| **LB (Load Balancer)** | 트래픽 분배 스위치 | L4(L4 Switch) 또는 L7(Application Gateway) 계층에서 트래픽의 대상을 결정. 가중치(Weight) 조절 가능. | LVS, Nginx, ALB (Application Load Balancer) |
| **Service Mesh** | 정교한 라우팅 제어 | Pod/Service 단위의 트래픽을 제어. HTTP Header, Cookie 기반 라우팅 지원. | **Istio**, **Linkerd** (Sidecar Pattern) |
| **Orchestrator** | 인프라 자동화 | 신규 버전의 컨테이너/인스턴스 배포 및 Health Check 수행. | **K8s (Kubernetes)**, Docker Swarm |
| **Observability** | 장애 탐지 | Canary 버전의 500 Error Rate, Latency 증가 감지. | **Prometheus**, **Grafana**, ELK Stack |
| **DB (Database)** | 데이터 저장소 | 버전 간 스키마 호환성 유지 (Backward Compatibility). | RDBMS, NoSQL (Expand & Contract Pattern) |

**2. 아키텍처 상세 다이어그램 (Traffic Flow)**

```text
    [ Internet Users ]
           │
           ▼
    ┌───────────────────────┐
    │   Ingress / Gateway    │
    │   (L7 LB / Service Mesh) │  <-- 🎛️ Control Plane (Traffic Split)
    └───────────┬───────────┘
                │
        ┌───────┴─────────┐
        │ (Traffic Ratio) │
        │  e.g., 95% : 5% │
        └───────┬─────────┘
        │       │
    ▼   ▼       ▼   ▼
┌─────────┐  ┌─────────┐
│ Stable  │  │ Canary  │
│ (V1.0)  │  │ (V1.1)  │
│ Replica │  │ Replica │
└────┬────┘  └────┬────┘
     │            │
     ▼            ▼
┌─────────────────────────────┐
│     Shared Database (RDBMS)  │  ⚠️ Caution: Schema Compatibility Required
│     (Must support V1 & V1.1) │
└─────────────────────────────┘
```

**3. 심층 동작 원리 (Step-by-Step Canary)**

1.  **배포 준비 (Preparation)**:
    신규 버전(V2)을 배포하여 기동시킨다. 이 시점에는 외부 트래픽이 전혀 들어가지 않는다.
2.  **초기 트래픽 분산 (Initial Routing)**:
    Ingress Controller 또는 Service Mesh의 **Virtual Service** 설정을 통해 V2로의 트래픽 비율을 1%로 설정한다. 이때 V2의 인스턴스 개수가 적으면 과부하가 걸릴 수 있으므로 **Pod Autoscaler**를 고려해야 한다.
3.  **메트릭 관측 및 검증 (Observation)**:
    **Golden Signals (Latency, Traffic, Errors, Saturation)**를 모니터링한다. 정상 응답 코드(200 OK) 비율과 응답 속도가 SLA(Service Level Agreement) 내에 있는지 확인한다.
4.  **트래픽 점진적 확대 (Ramp-up)**:
    이상 징후가 없으면 5% → 25% → 50% → 100%로 트래픽 양을 서서히 늘린다. 각 단계마다 안정화 시간(Stabilization Window)을 둔다.
5.  **완료 및 폐기 (Promotion & Cleanup)**:
    100% 트래픽이 전환되면 이전 버전(V1) 인스턴스를 종료(Terminate)하여 리소스를 반환한다.

**4. 핵심 알고리즘 (Istio Virtual Service 예시)**
YAML 설정을 통해 100분의 1의 트래픽을 카나리 서브셋으로 보내는 로직은 다음과 같다.

```yaml
# VirtualService for Canary Deployment
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        x-canary-test: # 특정 헤더가 있는 경우에만 카나리 노출 (Targeting)
          exact: "true"
    route:
    - destination:
        host: reviews
        subset: v2  # Canary Version
  - route:          # 일반 트래픽
    - destination:
        host: reviews
        subset: v1  # Stable Version (99%)
      weight: 99
    - destination:
        host: reviews
        subset: v2  # Canary Version (1%)
      weight: 1
```

**📢 섹션 요약 비유**
> 마치 수도관 교체 공사를 할 때, **물을 끄지 않고** 새로운 파이프를 임시로 연결하여 물이 새는지 압력을 테스트(Pressure Test)한 후, 이상이 없으면 본관에 접합하는 과정과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**1. 심층 기술 비교 분석표**

| 구분 | 블루-그린 배포 (Blue-Green) | 카나리 배포 (Canary) |
|:---|:---|:---|
| **핵심 메커니즘** | 환경 스위칭 (Switching Environments) | 트래픽 샌드박싱 (Traffic Sandboxing) |
| **리소스 효율성** | 낮음 (최대 200% 리소스 필요) | 높음 (증분 리소스만 필요) |
| **롤백(Rollback) 속도** | **즉시** (Routing만 원복) | **단계적** (트래픽 비율만 조정) |
| **장애 영향 범위** | 전체 사용자 (스위칭 실패 시) | 일부 사용자 (Canary 대상) |
| **데이터 정합성 위험** | **높음** (V1, V2가 동시에 DB 접근 시 스키마 충돌 가능성 높음) | **중간** (트래픽 분산으로 인한 데이터 버전 차이 발생 가능) |
| **주요 용도** | 대규모 인프라 교체, DB 마이그레이션 동반 시 | UI/UX 변경, 알고리즘 튜닝, 기능 테스트 |

**2. 과목 융합 분석 (OS / Network / DB)**

*   **데이터베이스 (DB) 융합 - "Two-Phase Commit"**:
    블루-그린 배포 시 V1(Blue)과 V2(Green)가 동시에 실행되는 순간이 존재한다. 이때 DB 스키마가 변경되었다면(예: 컬럼 삭제), V1 애플리케이션이 쿼리를 날릴 때 즉시 장애가 발생한다. 따라서 **'Expand and Contract'** 패턴(1. 컬럼 추가 → 2. 배포 → 3. 코드 변경 → 4. 컬럼 삭제)이 필수적이다. 또한, 네트워크 관점에서 **TCP/IP 세션** 지속성(Session Affinity)을 고려하여 배포 중 연결이 끊기지 않도록 **Graceful Shutdown** (SIGTERM 신호 대기)이 OS 레벨에서 구현되어야 한다.

*   **운영체제 (OS) 융합 - "Kernel Panic & Health Check"**:
    카나리 배포 중 신규 버전에서 메모리 누수(Memory Leak)가 발생해 **OOM (Out of Memory)**이 발생한다면? **K8s**의 **Liveness Probe**가 이를 감지하고 해당 Pod를 재시작해야 하며, **LB**는 죽은 Pod로 트래픽을 보내지 않도록 제외해야 한다.

**📢 섹션 요약 비유**
> 카나리 배포는 **'맛보기 식당 이벤트'**와 같아서, 소수에게 맛을 보이고 평가를 받지만, 블루-그린 배포는 **'이사 가기'**와 같아서 짐을 다 옮기지 않으면 전(前) 집도 버리고 후(後) 집도 못 쓰는 순간이 발생할 수 있어 DB 상태를 매우 조심스럽게 다뤄야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**1. 실무 시나리오: 대규모 이커머스 결제 시스템 개편**
*   **상황**: 블랙프라이데이 세일 기간 중, 결제 로직을 V1에서 V2(신규 PG사 연동)로 변경해야 함. 트래픽이 평소의 50배까지 몰림.
*   **전략 수립**:
    *   단순 기능 변경이 아닌 '핵심 트랜잭션' 변경이므로 데이터 정합성이 생명임.
    *   **Blue-Green 배포** 선택은 리스크가 큼 (DB 호환성 이슈).
    *   **Canary 배포 + Feature Toggle** 방식으로 V2로의 전환을 제어함.
*   **의사결정 프로세스**:
    1.  **Phase 1**: 내부 직원(IAM)에게 V2 트래픽 100% 노출 (Dogfooding).
    2.  **Phase 2**: 전체 트래픽의 1%를 V2로 라우팅. 이때 '지갑 잔고' 비교 로직(Shadow Read)을 통해 V1과 V2의 결과를 실시간 비교.
    3.  **Phase 3**: 오차 범위 0% 확인 후 10% → 50% → 100% 확대.

**2. 도입 체크리스트 (Prerequisites)**

| 구분 | 체크항목 |
|:---|:---|
| **Infra** | K8s Cluster 준비, HPA(Horizontal Pod Autoscaler) 설정, LB(로드밸런서) 설정 가능 여부 |
| **Monitoring** | Real-time Dashboard 구축 (Error Rate, Latency p99), 자동 알람(Alert) 설정 |
| **Security** | V1과 V2 간 **Secrets (API Key)** 동기화 여부, 보안 그룹(Security Group) 정책 일치 |
| **Fallback** | **Auto-Rollback** 스크립트 준비 (Error Rate > 1% 일 시 자동 V1 복귀) |

**3. 안티패턴 (Anti-patterns)**
*   **"Database와 Application의 분리 실패"**: 배포와 동시에 DB를 변경함. → **참사**. 배포는 100% 수동 롤백이 가능해도 DB는 롤백이 어려움.
*   **"공유 세션 상태(Session Stickiness) 미고려"**: 사용자가 로그인했는데 V1