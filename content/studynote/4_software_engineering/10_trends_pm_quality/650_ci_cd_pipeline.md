+++
title = "650. CI/CD 지속적 통합, 배포 파이프라인"
date = "2026-03-15"
weight = 650
[extra]
categories = ["Software Engineering"]
tags = ["DevOps", "CI", "CD", "Pipeline", "Automation", "Software Delivery"]
+++

# 650. CI/CD 지속적 통합, 배포 파이프라인

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 개발 생명주기(SDLC)에서 '빌드', '테스트', '배포' 프로세스를 자동화하여 코드 변경 사항을 **현행 개발(Trunk-Based Development)** 방식으로 운영 환경에 즉각 반영하는 **자동화된 소프트웨어 인도 체계**입니다.
> 2. **가치**: DORA(DevOps Research and Assessment) 상위 그룹 기준으로 배포 리드 타임(Lead Time)을 90% 이상 단축하고, 변경 실패율(Change Failure Rate)을 획기적으로 낮추어 비즈니스 민첩성(Agility)과 안정성(Stability)의 동시 확보가 가능합니다.
> 3. **융합**: 가상화(Virtualization), 컨테이너(Container), IaC(Infrastructure as Code), SRE(Site Reliability Engineering) 기술이 결합되어 'GitOps' 및 'AIOps'로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background) 

### 1. 개념 정의 및 철학
**CI/CD (Continuous Integration/Continuous Deployment or Delivery)**는 애자일(Agile) 개발 방법론의 실천 도구로서, 개발자가 코드를 변경할 때마다 자동으로 빌드 및 테스트를 수행하여 결함을 조기에 발견하고(Continuous Integration), 검증된 코드를 운영 환경까지 자동으로 릴리즈(Continuous Delivery/Deployment)하는 일련의 자동화 파이프라인 체계입니다.

전통적인 폭포수(Waterfall) 모델에서는 개발 종료 후 통합 단계에서 '통합 지옥(Integration Hell)'이 발생하거나, 수동 배포 과정에서의 오타, 순서 오류 등으로 인한 장애가 빈번했습니다. 이를 해결하기 위해 **"배포는 이벤트(Event)가 아니라 일상(Routine)이어야 한다"**는 철학에 기초하여, **실패의 빠른 피드백(Fail Fast)**과 **비용 하향 곡선(Cost of Change)의 평탄화**를 실현하는 것이 핵심 목표입니다.

### 2. 등장 배경 및 진화
1.  **전통적 한계**: 수동 스크립트 실행, 긴 배포 창구, 금요일 오후 배포 공포증(Release Phobia).
2.  **DevOps 등장**: 개발(Development)과 운영(Operations)의 단절을 해소하고 협업을 강화하는 문화적 운동이 일어남.
3.  **클라우드 및 컨테이너 혁명**: 가상머신(VM)에서 컨테이너(Docker) 기반의 마이크로서비스(MSA)로 아키텍처가 변화하면서, 파이프라인의 경량화와 고속화가 필수적이 됨.

### 3. CI/CD의 이해를 돕는 ASCII 비유

```text
📦 [비유] 자동화된 정수 및 배송 시스템 (Water Supply & Logistics)

┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│  🏭 수원지 (개발자) │ ──▶ │  🧪 정수장 (CI)    │ ──▶ │  🏠 가정 (운영 환경) │
└───────────────────┘      └───────────────────┘      └───────────────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │ 1. 여과 (Build)  │ : 원수를 깨끗하게 거름
                        │ 2. 수질 검사 (Test) │ : 불순물(버그) 발견 시 폐기
                        └──────────────────┘
                              │ (OK)
                              ▼
                        ┌──────────────────┐
                        │ 🚚 파이프라인 (CD) │ : 승인된 물을 자동으로 가정까지 공급
                        └──────────────────┘
```

### 📢 섹션 요약 비유
> **"마치 오염된 물이 수도꼭지를 통해 흘러나가는 것을 막기 위해, 정수장에서 자동으로 수질 검사를 하고 깨끗한 물만 가정으로 공급하는 고속 배관 시스템과 같습니다."**

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 및 내부 동작

| 구성 요소 (Component) | 영문 명칭 (Full Name) | 역할 및 내부 동작 (Role & Mechanism) | 주요 기술/프로토콜 (Tech/Proto) | 비유 (Analogy) |
|:---|:---|:---|:---|:---|
| **소스 코드 관리** | **SCM (Source Control Management)** | 개발자의 코드 변경 이력을 추적하고, Trunk/Main 브랜치로 병합(Merge)하는 저장소. **Webhook**을 통해 이벤트를 트리거함. | Git, GitHub/GitLab/Bitbucket | 📚 도서관 (책의 원본 보관) |
| **CI 서버** | **Build Server / Orchestrator** | SCM으로부터 코드를 인출(Pull)하고, 의존성을 설치한 뒤 컴파일 및 테스트를 실행하는 엔진. | Jenkins, GitLab CI, CircleCI | 🤖 로봇 팔 (자동 조립 기계) |
| **아티팩트 저장소** | **Artifact Repository** | 빌드된 결과물(Jar, War, Docker Image 등)을 버전별로 안전하게 보관하고 배포 단계에서 전달. | JFrog Artifactory, Docker Registry, AWS S3 | 📦 창고 (완제품 보관소) |
| **테스트 자동화** | **Automated Test Suite** | 코드의 무결성을 검증. **SAST**를 통한 정적 보안 분석, **Unit Test**를 통한 기능 검증 수행. | JUnit, PyTest, SonarQube | 🔍 품질 검사관 (QA) |
| **CD/배포 엔진** | **Deployment Engine** | 아티팩트를 운영 환경에 배포. **Blue-Green**이나 **Canary** 전략을 통해 무중단 배포를 수행. | Spinnaker, ArgoCD, K8s Operator | 🚚 트럭 (상품 배달) |

### 2. CI/CD 파이프라인 상세 흐름도 (ASCII)

```text
    [Developer]                     [CI Server]                           [Production]
        │                              │                                      │
        │  (1) Push & PR               │                                      │
        ├─────────────────────────────▶│                                      │
        │                              │                                      │
        │                              │  (2) Checkout & Fetch               │
        │                              │◀─────────────────────────────────────┤
        │                              │                                      │
        │                              │  (3) Build (Compile/Package)         │
        │                              │  ┌───────────────────────────────┐   │
        │                              │  │    Build Agent (Pod/VM)       │   │
        │                              │  │   Maven / Gradle / npm        │   │
        │                              │  └───────────────────────────────┘   │
        │                              │                                      │
        │                              │  (4) Unit Test & Static Analysis     │
        │                              │  ┌───────────────────────────────┐   │
        │                              │  │  Test Framework (JUnit)       │   │
        │                              │  │  SonarQube (Quality Gate)     │   │
        │                              │  └───────────────────────────────┘   │
        │                              │                                      │
        │                              │  (5) Artifact Upload                │
        │                              ├─────────────────────────────────────▶│
        │                              │           [Registry]                │
        │                              │                                      │
        │  (6) Approval (Optional)     │  (7) Deploy (Prod/Stage)            │
        │◀─────────────────────────────┤─────────────────────────────────────▶│
        │                              │                                      │
        │  (8) Result (Slack/Email)    │  (9) Monitoring & Feedback          │
        │◀─────────────────────────────┤◀─────────────────────────────────────┤
        │                              │                                      │
```

### 3. 심층 동작 원리 및 코드 스니펫

**① CI 단계 (Continuous Integration)**
CI의 핵심은 "병합(merge) 후 빌드"가 아니라 "병합 전 빌드(pre-merge integration)"입니다. 개발자가 Pull Request(PR)를 생성하면, 웹훅(Webhook)이 CI 서버에 이벤트를 전송합니다. CI 서버는 **격리된 환경(Sandbox/Docker Container)**에서 코드를 실행하여, 호스트 환경 오염을 방지합니다.

**② CD 단계 (Continuous Delivery/Deployment)**
CI를 통과한 아티팩트(Artifact)는 불변(Immutable) 상태로 저장소에 업로드됩니다. CD 단계에서는 이를 가져와 **Rolling Update**나 **Recreate** 전략으로 배포합니다. 이때 **Infrastructure as Code (IaC)** 툴(Terraform, Ansible)과 연동하여 서버 환경 자체를 프로비저닝(Provisioning)하는 경우가 일반적입니다.

**[Jenkins Pipeline 예시: Declarative Syntax]**
```groovy
pipeline {
    agent any // 어떤 에이전트에서든 실행 가능
    tools {
        maven 'Maven 3.8.1' // 툴 정의
    }
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package' // 빌드 수행
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test' // 테스트 수행
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml' // 결과 리포트
                }
            }
        }
        stage('Deploy to Staging') {
            when {
                branch 'main' // main 브랜치일 때만
            }
            steps {
                sh './deploy.sh staging' // 배포 스크립트 실행
            }
        }
    }
    post {
        failure {
            mail to: 'team@example.com', subject: 'Failed Pipeline' // 실패 시 알림
        }
    }
}
```

### 📢 섹션 요약 비유
> **"고속 도로의 하이패스 시스템과 같습니다. 요금소(테스트/배포)에 차량(코드)이 멈추지 않고 통과할 수 있도록, 미로 같은 수동 절차를 자동화된 게이트로 대체하여 교통체계(배포)의 효율을 극대화하는 것입니다."**

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 전략 비교: 지속적 제공(Delivery) vs 지속적 배포(Deployment)

| 비교 항목 (Criteria) | 지속적 제공 (Continuous Delivery) | 지속적 배포 (Continuous Deployment) |
|:---|:---|:---|
| **정의 (Definition)** | 프로덕션 환경 배포가 가능한 상태까지 자동화하나, **최종 배포는 수동 승인** 필요 | 모든 검증을 통과하면 **인간의 개입 없이** 자동으로 프로덕션에 반영 |
| **핵심 가치 (Value)** | 배포 시점을 비즈니스적으로 통제 가능 (금융권, 보안 강화 환경) | 릴리즈 주기를 획기적으로 단축 (수시~수분 단위) |
| **전제 조건 (Prerequisite)** | 자동화된 테스트 및 인프라 환경 | **100% 신뢰할 수 있는 테스트 커버리지** 및 모니터링 |
| **리스크 (Risk)** | 수동 실수(Fat Finger) 가능성 존재 | 자동화된 버그가 프로덕션으로 침투할 가능성 (Rollback 필수) |

### 2. 기술 융합 시너지 분석

**① IaC (Infrastructure as Code)와의 결합**
CI/CD가 애플리케이션 코드를 배포한다면, IaC는 **서버, 네트워크, 로드 밸런서** 등의 인프라를 코드로 관리하여 배포합니다.
- **Synergy**: 코드 변경 시 필요한 인프라 변화(예: 서비스 확장을 위한 오토스케일링 그룹 생성)를 파이프라인 내에서 자동으로 처리합니다. 이를 통해 **Configuration Drift(설정 드리프트, 환경 불일치)**를 방지합니다.

**② MSA (Microservices Architecture)와의 상관관계**
CI/CD는 모놀리식(Monolithic) 아키텍처에서도 가능하지만, 파이프라인의 복잡도와 빌드 시간이 기하급수적으로 증가합니다. 반면 MSA는 서비스별로 독립적인 파이프라인을 가질 수 있어 **팀별 자율성(Team Autonomy)**을 보장합니다.

**③ SRE (Site Reliability Engineering)와의 연계**
CI/CD 단순 자동화를 넘어, **SLO (Service Level Objective)**를 준수하기 위해 배포 후 **배포 승인 제어(Change Approval)**를 자동화(Alert 기반)하는 것과 연결됩니다.

### 📢 섹션 요약 비유
> **"자동차 공업의 유닛 공정과 같습니다. 자동차 한 대를 통째로 만드는 방식(모놀리식)에서 벗어나, 엔진, 타이어, 핸들을 각각 별도로 생산하여 조립하는 방식(MSA + CI/CD)으로 바꾸면, 특정 부품 업그레이드가 전체 공장을 멈추게 하지 않습니다."**

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오: 금융권의 대규모 장애 회복 및 재발 방지

**상황 (Context):**
A 증권사는 매일 밤 10시에 수동 배포를 진행했습니다. 어느 날 DB 마이그레이션 스크립트가 누락되어 서비스가 2시간 중단되는 사고가 발생했습니다.

**의사결정 프로세스 (Decision Matrix):**

1.  **문제 진단**: 수동 배포 체크리스트 누락, 새벽 작업으로 인한 운영자 피로도 증가.
2.  **도입 전략 (Technical Strategy)**:
    -   **Jenkins 기반 CI 도입**: 개발자가 코드를 커밋할 때마다 정적 분석(SonarQube)을 수행하고, 테스트 커버리지가 80% 미만일 경우 Merge를 금지하는 **Pre-hook** 설정.
    -   **Blue-Green Deployment**: Kubernetes 환경에서 신규 버전(Pod)을 띄운 뒤, Service Selector를 통해 트래픽을 즉시 전환. 문제 발생 시 이전 버전으로 즉시 Rollback.
    -   **DB 스크립트 자동화**: Flyway/Liquibase를 도입하여 DB 변경 사항을 코드와 함께 버전 관리.
3.  **결과 (Outcome)**:
    -   배포 리드 타임: 4시간 → 10분 단축.
    -   배포 실패율: 월 2회 → 0회.

### 2. 도입 체크리스트 및 Anti-Pattern

**✅ 도입 체크리스트**
-