+++
title = "684. 스트랭글러 패턴 레거시 분할"
date = "2026-03-15"
weight = 684
[extra]
categories = ["Software Engineering"]
tags = ["Legacy Migration", "Strangler Fig Pattern", "MSA", "Modernization", "Architecture Pattern"]
+++

# 684. 스트랭글러 패턴 레거시 분할

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일한 거대 레거시 시스템(Monolith)을 '빅뱅(Big-bang)' 방식으로 교체하는 위험을 피하고, **점진적 교체(Incremental Replacement)**를 통해 안정적으로 현대화 아키텍처로 진화시키는 설계 패턴.
> 2. **메커니즘**: **API Gateway (Application Programming Interface Gateway)** 나 **Proxy (Reverse Proxy)** 를 Facade로 활용하여, 신규 기능은 New System으로, 기존 기능은 Legacy로 라우팅(Route)하는 트래픽 제어를 핵심으로 함.
> 3. **가치**: 비즈니스 연속성(Business Continuity)을 100% 보장하며, 낮은 비용으로 높은 품질의 MSA (Microservices Architecture) 전환을 가능하게 함.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 정의 및 철학
**스트랭글러 패턴 (Strangler Fig Pattern)**은 기존의 레거시 애플리케이션을 새로운 시스템으로 점진적으로 대체하는 소프트웨어 아키텍처 패턴입니다. 이 패턴은 다른 나무를 감싸고 졸라 죽여서 대신 자라나는 '교살자 무화과(Strangler Fig)' 식물의 생태에서 이름을 따왔습니다.

기존의 빌드 & 배포 파이프라인(Build & Deploy Pipeline)을 유지하면서, 새로운 요구사항을 새로운 애플리케이션으로 구현하고, 특정 URI (Uniform Resource Identifier) 또는 API 경로를 통해 들어오는 트래픽을 차단하고 새로운 애플리케이션으로 우회시키는 방식으로 작동합니다. 시간이 지나면서 레거시 시스템은 '스트랭글(교살)'되어 기능을 상실하고 자연스럽게 퇴출(Deprecation)됩니다.

### 2. 등장 배경: 빅뱅 방식의 한계
과거 엔터프라이즈 애플리케이션은 **수명주기 (Software Development Life Cycle, SDLC)**의 말기에 이르면 유지보수가 불가능해집니다. 이때 많은 조직이 시스템 전체를 중단하고 새로운 시스템으로 교체하려 하지만, 이는 '빅뱅 마이그레이션'이라 불리는 극도로 위험한 시도입니다. 데이터 마이그레이션(Data Migration)의 복잡성, 비즈니스 로직의 미묘한 차이, 그리고 사용자의 요구사항 변경 등으로 인해 프로젝트는 지연되거나 실패하기 십상입니다. 스트랭글러 패턴은 이러한 위험을 회피하고 'Running Train' 위에서 엔진을 교체하듯 시스템을 개조하기 위해 고안되었습니다.

### 3. 핵심 워크플로우 ASCII
이 패턴은 시스템 전체의 중단 없이 새로운 기능을 추가하고 기능을 이관하는 과정을 시각화할 수 있습니다.

```text
[Phase 1: 전면 레거시]          [Phase 2: 점진적 이관]            [Phase 3: 완전 교체]
+------------------+         +------------------+            +------------------+
|   Legacy System  |         |   Legacy System  |            |   New System     |
|  (All Functions) |         | (Remaining Func) |            | (All Functions)  |
+--------+---------+         +--------+---------+            +--------+---------+
         ^                           ^                               ^
         |                           |                               |
         |                           |                               |
    User Request                 Proxy / Facade                 User Request
(Routing by Host)             (Routing by Path/Subdomain)    (Direct Access)
```

**해설**: Phase 1에서는 모든 트래픽이 레거시로 향합니다. Phase 2에서는 **PF (Pattern Facade)** 계층이 트래픽을 분석하여 `/new-service/*` 요청은 새로운 시스템으로 보내고, 나머지는 레거시로 전달합니다. Phase 3이 되면 레거시는 더 이상 트래픽을 받지 못하고 안전하게 종료됩니다.

> **📢 섹션 요약 비유**
> "마치 고속도로에서 낡은 톨게이트를 고장 내지 않고 통행하면서, 옆에 패스트 트랙(Fast Track)을 먼저 만들어 차량을 우회시키다가, 결국엔 모든 차량이 새로운 트랙을 이용하게 만드는 것과 같습니다."

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 상세 구성 요소 및 역할
스트랭글러 패턴을 구현하기 위해서는 다음과 같은 5가지 핵심 컴포넌트의 상호작용이 필수적입니다.

| 구성 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Action) | 프로토콜/기술 (Protocol) |
|:---|:---|:---|:---|
| **Client (Client App)** | 요청자 | URI 또는 도메인을 통해 서비스 호출 | HTTP/HTTPS, gRPC |
| **Router / Facade** | 교통 정제 통제 | 수신 요청의 헤더, 경로, 쿠키를 분석하여 타겟 시스템 결정 | Nginx, HAProxy, Spring Cloud Gateway |
| **Legacy App** | 기존 백엔드 | 이관되지 않은 기능 처리 및 데이터 반환 | RMI, Monolithic Logic |
| **New App (Strangler)** | 신규 백엔드 | 이관된 기능을 현대 기술로 처리 (MSA, Cloud Native) | RESTful API, GraphQL |
| **Integration Layer** | 데이터 연동 | 두 시스템 간의 데이터 일관성 유지 및 동기화 | DB Replication, CDC (Change Data Capture), MQ |

### 2. 라우팅 메커니즘 및 상태 전이 (ASCII)
실무적으로는 **URI 기반 라우팅** 또는 **헤더 기반 라우팅**을 주로 사용합니다. 아래는 요청 흐름에 따른 세부 분기 과정입니다.

```text
      User Request (http://api.example.com/v1/products/123)
            │
            ▼
    ┌───────────────────────┐
    │  API Gateway (Facade) │ <---- 결정 지점 (Decision Point)
    └───────┬───────┬───────┘
            │       │
            │       ├── [Route Rule 1] Path: /v1/users/*
            │       │                   → Target: Legacy (Not migrated yet)
            │       │
            │       └── [Route Rule 2] Path: /v1/products/*
            │                           → Target: New Service (Migrated)
            ▼                           ▼
    ┌───────────────┐         ┌──────────────────────┐
    │ Legacy System │         │   New Product Svc    │
    │ (Monolith)    │         │ (Microservice)       │
    └───────────────┘         └──────────────────────┘
            ▲                           │
            │                           │
            └───────────┬───────────────┘
                        │
            (Data Synchronization / Consistency Check)
```

**해설**:
1.  **Identify (식별)**: 게이트웨이는 들어온 요청이 신규 규격에 부합하는지 확인합니다.
2.  **Route (분기)**: 신규 서비스에 위임된 기능은 `Service Mesh`나 `Ingress`를 통해 새로운 애플리케이션으로 전달됩니다. 이때 레거시와 신규 시스템 간의 세션(Session) 정보나 인증 토큰(Token) 호환성을 유지하기 위한 **어댑터(Adapter)**가 필요할 수 있습니다.
3.  **Aggregation (통합)**: 사용자 화면에서는 레거시 데이터와 신규 데이터가 혼재되어야 할 수 있으므로, **BFF (Backend for Frontend)** 계층에서 이를 합치거나, 마이그레이션 기간 중에는 **DB Replication**을 통해 데이터를 동기화하는 것이 중요합니다.

### 3. 핵심 알고리즘 및 코드 (Routing Logic)
아래는 파사드(Facade)에서 요청을 분석하여 적절한 서비스로 라우팅하는 의사 코드(Pseudo-code)입니다. 이는 **Spring Cloud Gateway**의 `Predicate` 설정이나 **Nginx**의 `location` 블록 설정으로 구현될 수 있습니다.

```yaml
# spring-cloud-gateway/routes.yml 예시
spring:
  cloud:
    gateway:
      routes:
        # Route 1: 신규 서비스로 우회 (Strangler Application)
        - id: new-product-service
          uri: lb://product-service-v2
          predicates:
            - Path=/api/v2/products/** # v2 경로는 신규로
            - Header=X-New-Feature, true # 특정 헤더가 있으면 신규로
          
        # Route 2: 레거시 시스템으로 유지 (Fallback)
        - id: legacy-monolith
          uri: http://legacy-server:8080
          predicates:
            - Path=/api/** # 그 외 나머지는 레거시로
```

### 4. 데이터 일관성 및 동기화 전략
공존 기간(Coexistence Period) 동안 가장 큰 기술적 난관은 **Data Consistency (데이터 일관성)**입니다. 레거시 DB와 신규 DB가 분리되는 순간, 데이터 동기화가 필수적입니다.

*   **Triggers based**: 레거시 DB의 트리거(Trigger)를 활용하여 변경 사항을 신규 DB에 전송 (성능 이슈 있을 수 있음).
*   **CDC (Change Data Capture)**: WAL (Write-Ahead Logging)을 읽어 비동기적으로 데이터를 복제 (가장 권장됨).

> **📢 섹션 요약 비유**
> "마치 도시의 상수도관을 교체할 때, 물을 끊지 않고 옆에 새 관을 깐 뒤 건물마다 연결된 호스를 하나씩 새 관으로 갈아 끼워주는 '생존 수술'과 같습니다."

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 빅뱅 vs 스트랭글러
아래는 전략적 관점과 기술적 관점에서 두 패러다임을 비교 분석한 표입니다.

| 비교 항목 (Criteria) | 빅뱅 마이그레이션 (Big-bang) | 스트랭글러 패턴 (Strangler) | 분석 (Analysis) |
|:---|:---|:---|:---|
| **전환 리스크 (Risk)** | **Critical (치명적)** | **Low (낮음)** | 빅뱅은 실패 시 서비스 전체 중단(RTO 급증). 스트랭글러는 특정 기능만 롤백하면 됨. |
| **비용 구조 (Cost)** | **Front-loaded (선지출)** | **Pay-as-you-go (지불해봄)** | 빅뱅은 초기 자본 지출(CAPEX)이 큼. 스트랭글러은 OPEX 위주. |
| **가치 전달 (Time-to-Market)** | 지연됨 (Long Tail) | **즉시적 (Immediate)** | 새로운 기능이 레거시를 기다리지 않고 즉시 배포됨. |
| **운영 복잡도 (Complexity)** | 단순 (단일 시스템) | **복잡 (이중 시스템 관리)** | 두 시스템이 공존하므로 모니터링, 로그 추적, 로그인 세션 공유 등의 복잡도 발생. |
| **데이터 무결성** | 단순 (일관성 유지 용이) | **난이도 상 (CDC 필요)** | 분산 트랜잭션 관리 및 데이터 동기화 필수. |

### 2. 타 영역(DevOps/DB) 융합 및 시너지
스트랭글러 패턴은 단순한 코딩 기법이 아니라 인프라와 데이터의 융합이 필요합니다.

*   **DevOps와의 융합 (CI/CD Pipeline)**:
    *   **Blue-Green Deployment** 및 **Canary Release** 기법과 결합하여, 신규 애플리케이션 배포 시 사용자에게 노출되는 트래픽 양을 1% -> 10% -> 50%로 점진적으로 늘려가며 검증합니다.
*   **데이터베이스와의 융합 (CDC & ETL)**:
    *   레거시 시스템의 데이터를 신규 시스템의 NoSQL(예: MongoDB)로 옮겨야 할 때, **CDC (Change Data Capture)**를 통해 데이터 복제 지연을 줄이고, 더블 라이트(Double Write) 패턴 등을 사용하여 트랜잭션 무결성을 유지합니다.

### 3. 성능 지표 분석 (Decision Matrix)
*   **Latency (지연 시간)**: 파사드(Facade)를 통과하는 오버헤드가 발생하므로, 순수 레거시 호출보다 약간의 지연이 발생할 수 있습니다. (약 2~5ms 수준, 네트워크 홉 증가). 이를 해결하기 위해 **Keep-Alive** 연결을 최적화해야 합니다.
*   **Throughput (처리량)**: 신규 시스템이 클라우드 네이티브(Cloud Native) 환경(Auto-scaling)이라면, 전체 시스템의 처리량은 점진적으로 향상됩니다.

> **📢 섹션 요약 비유**
> "자동차 엔진을 교체할 때, 차를 멈추고 엔진을 통째로 갈아끼우는 것(빅뱅)보다, 달리는 상태에서 연료 펌프부터, 배선마다 하나씩 바꿔가는 튜닝 방식(스트랭글러)이 전문가들의 선택입니다."

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 대형 은행 핀테크 시스템 전환
**상황**: 30년 된 메인프레임 뱅킹 시스템(IBM CICS + COBOL)을 Java 기반의 오픈소스 MSA로 전환해야 함.
**문제점**: 하루 수백만 건의 거래가 중단될 수 없으며, 데이터의 무결성이 금융 수준(ACID)을 보장해야 함.

**의사결정 과정 (Decision Making)**:
1.  **후보 선정**: 시스템 전체가 아닌, 독립적인 '포인트 적립' 기능을 선정. 실패해도 핵심 계좌 이체에 영향이 없음.
2.  **파사드 구축**: 웹 및 앱 요청 앞단에 **Kong API Gateway**를 도입. `/api/loyalty/*` 경로를 신규 Spring Boot 서비스로 라우팅.
3.  **데이터 동기화**: 메인프레임 DB(DB2)의 변경 사항을 **GoldenGate(CDC 툴)**를 통해 신규 MySQL로 실시간 복제.
4