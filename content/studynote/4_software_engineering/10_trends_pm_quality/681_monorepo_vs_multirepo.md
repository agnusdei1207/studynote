+++
title = "681. 모노레포 vs 멀티레포"
date = "2026-03-15"
weight = 681
[extra]
categories = ["Software Engineering"]
tags = ["Monorepo", "Multirepo", "VCS", "Git", "Scalability", "Code Management"]
+++

# 681. 모노레포 vs 멀티레포 (Monorepo vs Multirepo)

## # 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 Version Control System (VCS, 버전 관리 시스템) 저장소 내에 모든 프로젝트를 통합 관리하는 **Monorepo (Monolithic Repository)** 전략과 프로젝트별로 독립된 저장소를 운영하는 **Multirepo (Multiple Repository)** 전략은 형상 관리의 근본 철학을 달리함.
> 2. **가치**: Monorepo는 Atomic Commit (원자적 커밋)과 코드 재사용성을 극대화하여 '의존성 지옥(Dependency Hell)'을 해결하지만, CI/CD 파이프라인의 스케일링 난이도가 높음. 반면 Multirepo는 팀 자율성과 격리성을 보장하나, 통합(Integration) 비용과 버전 호환성 유지에 대한 부담이 큼.
> 3. **융합**: DevOps 자동화 도구(Bazel, Nx, Turborepo 등) 및 MSA (Microservices Architecture, 마이크로서비스 아키텍처) 환경과의 시너지를 고려하여, 조직의 규모(Scale-up)와 기술 성숙도에 따른 하이브리드 전략이 요구됨.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 정의
**Monorepo (Monolithic Repository)**는 두 개 이상의 프로젝트, 라이브러리, 또는 패키지를 단일 Git 저장소 내에서 관리하는 전략을 의미합니다. 이와 반대로 **Multirepo (Multiple Repository)**는 각 프로젝트를 독립적인 Git 저장소로 분리하여 관리하는 전략입니다. 이는 단순한 코드 저장 위치의 차이를 넘어, 조직의 커뮤니케이션 구조와 배포 파이프라인의 설계 방향성을 결정짓는 중요한 아키텍처 결정입니다.

### 2. 💡 비유: 통합 공장 vs 자치 주방
모노레포는 재료부터 조리, 배달까지 모든 공정이 이루어지는 **'거대한 통합 공장'**과 같습니다. 모든 시스템이 연결되어 있어 재료(코드)를 옮길 필요가 없지만, 공장 전체를 관리하는 데 막대한 자원이 듭니다. 반면 멀티레포는 각자 요리를 담당하는 **'분리된 자치 주방'**과 같습니다. 주방별로 독립적으로 운영되지만, 레시피(표준)가 다르거나 재료를 공유할 때 물리적인 이동과 협조가 필요합니다.

### 3. 등장 배경: 소프트웨어의 거대화와 복잡성
초기 소프트웨어 개발은 단일 코드베이스로 충분했습니다. 그러나 애플리케이션이 거대해지고 기능별로 팀이 나뉘면서 **SOA (Service-Oriented Architecture, 서비스 지향 아키텍처)** 및 **MSA (Microservices Architecture, 마이크로서비스 아키텍처)**가 도입되었습니다. 이에 따라 코드를 어떻게 분리하고 관리할 것인가에 대한 고민이 시작되었습니다.
1.  **기존 한계**: 수천 개의 Microservice를 각각의 Repository로 관리 시, 버전 충돌, 공통 코드 복제, 통합 테스트의 어려움 발생.
2.  **혁신적 패러다임**: Google, Facebook(Meta) 등의 빅테크 기업이 '단일 저장소'에 모든 코드를 두고 수만 명이 협업하는 방식(Monorepo)을 증명하고 도구(Bazel, Mercurial 등)를 오픈소스화.
3.  **현재 비즈니스 요구**: 급변하는 시장 요구에 대응하기 위해 **CI/CD (Continuous Integration/Continuous Deployment, 지속적 통합/배포)**의 효율성과 개발 생산성 간의 균형이 필수적이 되었음.

> **📢 섹션 요약 비유**: 모노레포와 멀티레포의 선택은 마치 **'대규모 주방 Kitchen'**을 설계하는 것과 같습니다. 모든 요리사가 하나의 거대한 주방에서 자유롭게 재료를 꺼내 쓰게 할 것인가(Monorepo), 아니면 피자 전문점, 햄버거 전문점처럼 주방을 완전히 분리해서 운영하게 할 것인가(Multirepo)의 초기 설계 차이입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 및 핵심 모듈

| 구성 요소 | Monorepo 역할 및 내부 동작 | Multirepo 역할 및 내부 동작 | 프로토콜/툴 |
|:---|:---|:---|:---|
| **VCS (Version Control System)** | 단일 서버(또는 분산 저장소)에 PB(Petabyte)급 데이터 저장. 메타데이터 관리 중요 | 여러 독립된 서버 또는 Namespace로 분리 저장 | Git, Mercurial |
| **Dependency Management** | Workspace 기반 심링크(Symbolic Link) 또는 Local 경로 참조로 의존성 해결 | Package Registry(NPM, Maven 등)를 통한 네트워크 기반 의존성 해결 | npm/yarn workspaces, Maven BOM |
| **Build System** | **Incremental Build (증분 빌드)**: 변경된 부분만 파악하여 재빌드 (Dependency Graph 활용) | 각 프로젝트 독립적 빌드 (전체 빌드 시간 합이 전체 시간) | Bazel, Nx, Turborepo |
| **CI/CD Pipeline** | Monorepo-aware CI: 변경된 파일 경로를 감지하여 관련 테스트/배포만 트리거 (Path Filtering) | 각 저장소별 독립된 Webhook 및 트리거 | Jenkins, GitHub Actions, CircleCI |
| **Code Sharing** | Import/Include 문으로 즉시 참조 가능. 버전 관리 불필요 | Library 버전을 명시하여 Publish 후 Import 과정 필수 | Internal Nexus/Artifactory |

### 2. 아키텍처 구조 및 데이터 흐름

아래 다이어그램은 코드 수정(Modification)부터 배포(Deployment)까지의 흐름과 의존성 관리의 차이를 도식화한 것입니다.

```text
   [Architecture Comparison: Data Flow & Dependency]

   1. MONOREPO (Shared Source Strategy)              2. MULTIREPO (Distributed Source Strategy)

   +--------------------------+                      +--------------------------+
   |      GIT SERVER (Repo)   |                      |      GIT SERVER (Repos)  |
   |                          |                      |                          |
   |  /apps                   |                      |  /order-service (Repo A) |
   |   |-- order-app.js  ◄────┼──────┐               |   |-- order-app.js        |
   |   |-- user-app.js        |      |               |                          |
   |                          |      |               |  /user-service  (Repo B) |
   |  /libs                   |      |               |   |-- user-app.js         |
   |   |-- shared-util.js ◄───┼──────┼───┐           |                          |
   |                          |      |   |           |  /shared-lib    (Repo C) |
   +--------------------------+      |   |           |   |-- util.js            |
              ▲                      |   |           +--------------------------+
              │                      |   |                     ▲
              │                      |   |                     │ Publish (v1.0.1)
              │                      |   |                     │ (Artifact Registry)
              │                      |   |                     |
   [BUILD SYSTEM]               [BUILD SYSTEM]            [BUILD SYSTEM]
   (Analyzes Graph)             (Builds All)             (Builds Indep.)
              │                      │                     │
              ▼                      ▼                     ▼
   "Change util.js"          "Build Order & User"    "Build Order"
    └─> Detects Order/User     (Independent)         "Build User"
       dependency needs                              "Build Shared"
       rebuild
```

**다이어그램 해설**:
1.  **Monorepo (좌측)**: 개발자가 `libs/shared-util.js`를 수정하면, 빌드 시스템(Bazel/Nx 등)은 **의존성 그래프(Dependency Graph)**를 분석하여 해당 유틸을 사용하는 `order-app`과 `user-app`만 자동으로 식별하고 재빌드/테스트합니다. **코드 공유**가 파일 시스템 레벨에서 즉시 이루어지므로 별도의 배포(Publish) 과정이 필요 없습니다.
2.  **Multirepo (우측)**: `shared-lib` Repo를 수정하면, 이를 사용하는 `order-service`와 `user-service`는 변경 사항을 인지하지 못합니다. `shared-lib`를 Artifact Registry에 **배포(Publish)**하고, 각 서비스 팀은 `package.json` 등에서 버전을 명시적으로 **업그레이드(Upgrade)**하고 의존성을 설치해야만 반영됩니다. 이 과정에서 시차(Time Lag)가 발생할 수 있습니다.

### 3. 심층 동작 원리 및 알고리즘

#### A. Monorepo의 핵심: 의존성 그래프(Dependency Graph) 분석
Monorepo의 성능은 "무엇을 다시 빌드/테스트할 것인가"를 결정하는 정확도에 달려 있습니다.
1.  **Input**: 소스 코드의 수정 사항(Changed Files).
2.  **Process**:
    *   프로젝트 간 Import/Export 관계를 파싱하여 Directed Acyclic Graph (DAG, 유향 비순환 그래프) 생성.
    *   수정된 파일이 속한 노드(Node)를 찾음.
    *   해당 노드로부터 의존하는 하위 노드들(Descendants)을 재귀적으로 탐색.
3.  **Output**: 영향받은 프로젝트 목록(Affected Projects).
4.  **Action**: 해당 목록에 대해서만 CI/CD 파이프라인 실행.

#### B. Multirepo의 핵심: 버전 의존성 해결 (Semantic Versioning)
Multirepo는 각 라이브러리가 독립적인 생명주기를 가집니다.
1.  **Lifecycle**: Code → Build → Publish (Registry) → Consumer Update.
2.  **Conflict**: `service-A`는 `lib-lib v1.0`을 쓰고, `service-B`는 `lib-lib v2.0`을 쓰는 상황 발생 가능.
3.  **Resolution**: Package Manager(NPM, Maven)가 중간에서 호환 가능한 버전을 찾는 알고리즘(의존성 중복 허용 혹은 평탄화)을 수행하며, 이 과정에서 **Diamond Dependency Problem(다이아몬드 의존성 문제)**이 발생할 수 있음.

### 4. 실무 수준의 설정 예시 (Monorepo)

```json
// package.json (Root) - Nx Workspace 예시
{
  "name": "mega-corp-monorepo",
  "workspaces": ["packages/*", "apps/*"], 
  "devDependencies": {
    "@nrwl/workspace": "latest", 
    "typescript": "^4.9"
  },
  "scripts": {
    // 의존성 그래프를 기반으로 변경된 프로젝트만 테스트
    "affected:test": "nx affected:test", 
    // 변경된 프로젝트만 빌드
    "affected:build": "nx affected:build"
  }
}
```

> **📢 섹션 요약 비유**: Monorepo의 빌드 시스템은 **'스마트한 GPS 내비게이션'**과 같습니다. 전체 지도를 알고 있기 때문에, 한 도로(코드)가 막히거나 수정되면 그 영향을 받는 다른 도로들(연관 서비스)만 정확히 찾아내서 우회도로를 제시합니다. 반면 Multirepo는 각자 운전하는司机들이 라디오 소식으로만 교통 상황을 듣는 것과 비슷하여, 전체 상황 파악에 늦어지거나 누락이 발생할 수 있습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 전략적 상세 비교 (정량적 지표 포함)

| 비교 항목 | Monorepo (단일 저장소) | Multirepo (다중 저장소) | 분석 및 의사결정 포인트 |
|:---|:---|:---|:---|
| **CI/CD 비용 (Time)** | **낭비 가능성 높음** (최적화 필수) <br> 전체 스캔 비용이 크지만, 캐싱 시 효율적 | **예측 가능함** <br> 독립적이므로 병렬 처리가 쉬움 | **CI Time**이 병목일 경우 Monorepo는 캐싱 전략이 필수적. |
| **의존성 관리 (Effort)** | **매우 쉬움** <br> 동일 버전 사용 강제, 코드 즉시 반영 | **어려움 (High Friction)** <br> 버전 충돌 관리, 수동 업데이트 부담 | **Dependency Hell** 해소가 주 목적이라면 Monorepo가 유리. |
| **저장소 크기 (Perf)** | **거대 (GB~TB)** <br> Clone 속도 저하, 디스크 압박 (Sparse Clone 필요) | **작음 (MB)** <br> 빠른 Clone, 가벼운 작업 환경 | **VCS 성능**이 저하되면 개발자 경험(DEX)이 악화됨. |
| **코드 가시성 (Transparency)** | **높음 (High)** <br> 타 팀 코드 수정 내용 실시간 파악 가능 | **낮음 (Low)** <br> 외부 저장소 변경 내역을 알기 어려움 | 조직의 **Open Culture**가 강화될 때 가시성은 장점이 되나, 사일로(Silo) 조직에서는 방해가 됨. |
| **보안 및 권한 (Security)** | **세분화 어려움** <br> 전체 코드 접근이 쉬우므로 민감 모듈 관리 주의 | **우수** <br> Repo 단위로 권한 제어 가능 (RBAC 적용 쉬움) | **보안 규정**이 엄격한 금융/공공 분야는 Multirepo 선호 경향. |

### 2. 기술 융합 시너지 및 오버헤드

#### A. Microservices Architecture (MSA)와의 만남
*   **Synergy (Monorepo + MSA)**: 배포(Deployment)는 분리되어 있지만(MSA), 개발(Development)은 통합되어 있는(Monorepo) 하이브리드 형태입니다. 서비스 간 API 계약이 변경될 때, Server와 Client 코드를 동시에 수정하여 커밋함으로써 **런타임 오류를 사전에 차단**할 수 있습니다.
*   **Synergy (Multirepo + MSA)**: 완전한 독립성. 한 서비스의 저장소가 장애가 나더라도 다른 서비스 개발에 영향이 없습니다. Conway의 법칙(조직이 시스템을 만든다)이 그대로 적용되는 형태.

#### B. DevOps 및 툴체인
*   **Monorepo 지원 도구**:
    *   **Bazel (Build system)**: Google이 만든 고속 빌드 도