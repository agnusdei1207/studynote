+++
title = "21. CI/CD 파이프라인 (CI/CD Pipeline)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["CI", "CD", "Pipeline", "Jenkins", "GitHub-Actions", "DevOps"]
draft = false
+++

# CI/CD 파이프라인 (CI/CD Pipeline)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CI/CD 파이프라인은 **"코드 변경을 **자동으로 빌드, **테스트, **배포하는 **워크플로우"**로, **Version Control**(Git)의 **Trigger**로 **시작**되어 **Build** → **Test** → **Deploy** 단계를 **거쳐 **Production**에 **반영**된다.
> 2. **가치**: **수동 작업**을 **자동화**하여 **실수**를 **줄이**고 **빠른 피드백**으로 **문제 조기 발견**이 가능하며 **Deployment Frequency**를 **높이**고 **Lead Time**을 **단축**하여 **Delivery**를 **가속화**한다.
> 3. **융합**: **Jenkins**(Pipeline-as-Code), **GitHub Actions**(YAML Workflow), **GitLab CI**(.gitlab-ci.yml), **CircleCI**(config.yml)로 **정의**하며 **Docker**, **Kubernetes**, **Terraform**과 결합하여 **Infrastructure as Code**(IaC)를 **구현**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
CI/CD 파이프라인은 **"소프트웨어 개발부터 배포까지의 자동화된 프로세스"**이다.

**파이프라인 단계**:
1. **Build**: 소스 코드 → 실행 가능한 아티팩트
2. **Test**: 단위, 통합, E2E 테스트
3. **Package**: Docker 이미지, JAR, WAR
4. **Deploy**: Staging, Production

### 💡 비유
CI/CD 파이프라인은 **"자동 생산 라인"**과 같다.
- **원재료**: 코드
- **조립**: 빌드
- **검사**: 테스트
- **출하**: 배포

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD 파이프라인의 발전                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Manual (1990년대):
    • 수동 빌드/배포
    • 실수 가능, 느림
         ↓
Script (2000년대):
    • Shell Script
    • 부분 자동화
         ↓
CI 서버 (Jenkins, 2000년대):
    • 지속적 통합
    • 자동화 확대
         ↓
Pipeline (2010년대~):
    • Pipeline-as-Code
    • GitOps
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### 파이프라인 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline Architecture                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Developer                                                                             │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  git commit → git push                                                            │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                     │                                                   │
    │                                     ▼                                                   │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Trigger (Webhook)                                                                  │  │
    │  │  • Push to main/develop                                                            │  │
    │  │  • Pull Request                                                                      │  │
    │  │  • Schedule (Cron)                                                                   │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                     │                                                   │
    │                                     ▼                                                   │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  CI Server (Runner/Agent)                                                          │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Stage 1: Build                                                                  │  │
    │  │  │  • Dependency Download                                                           │  │
    │  │  │  • Compile                                                                         │  │
    │  │  │  • Unit Test                                                                      │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │                                     │ Success                                        │  │
    │  │                                     ▼                                               │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Stage 2: Test                                                                   │  │
    │  │  │  • Integration Test                                                               │  │
    │  │  │  • Static Analysis (SonarQube)                                                   │  │
    │  │  │  • Security Scan (Snyk, Trivy)                                                   │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │                                     │ Success                                        │  │
    │  │                                     ▼                                               │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Stage 3: Package                                                                │  │
    │  │  │  • Docker Build                                                                   │  │
    │  │  │  • Push to Registry                                                               │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │                                     │ Success                                        │  │
    │  │                                     ▼                                               │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Stage 4: Deploy                                                                 │  │
    │  │  │  • Staging (자동)                                                                  │  │
    │  │  │  • E2E Test                                                                       │  │
    │  │  │  • Production (수동 승인/자동)                                                       │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Jenkins Pipeline (Declarative)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Jenkinsfile 예시                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  pipeline {                                                                            │
    │      agent any                                                                         │
    │                                                                                         │
    │      environment {                                                                      │
    │          DOCKER_REGISTRY = 'registry.example.com'                                      │
    │          IMAGE_NAME = "${DOCKER_REGISTRY}/myapp:${BUILD_NUMBER}"                        │
    │      }                                                                                  │
    │                                                                                         │
    │      stages {                                                                           │
    │          stage('Build') {                                                               │
    │              steps {                                                                    │
    │                  sh 'mvn clean package'                                                 │
    │              }                                                                          │
    │          }                                                                              │
    │                                                                                         │
    │          stage('Test') {                                                                │
    │              steps {                                                                    │
    │                  sh 'mvn test'                                                          │
    │                  junit 'target/surefire-reports/*.xml'                                  │
    │              }                                                                          │
    │          }                                                                              │
    │                                                                                         │
    │          stage('Docker Build') {                                                        │
    │              steps {                                                                    │
    │                  script {                                                                │
    │                      docker.build("${IMAGE_NAME}")                                       │
    │                      docker.withRegistry("https://${DOCKER_REGISTRY}", 'cred') {         │
    │                          docker.image("${IMAGE_NAME}").push()                             │
    │                      }                                                                  │
    │                  }                                                                      │
    │              }                                                                          │
    │          }                                                                              │
    │                                                                                         │
    │          stage('Deploy Staging') {                                                      │
    │              steps {                                                                    │
    │                  sh 'kubectl apply -f k8s/staging/'                                     │
    │              }                                                                          │
    │          }                                                                              │
    │                                                                                         │
    │          stage('Deploy Production') {                                                    │
    │              when {                                                                     │
    │                  branch 'main'                                                          │
    │              }                                                                          │
    │              steps {                                                                    │
    │                  input message: 'Deploy to Production?', ok: 'Deploy'                   │
    │                  sh 'kubectl apply -f k8s/production/'                                   │
    │              }                                                                          │
    │          }                                                                              │
    │      }                                                                                  │
    │                                                                                         │
    │      post {                                                                             │
    │          success {                                                                      │
    │              echo 'Pipeline succeeded!'                                                   │
    │          }                                                                              │
    │          failure {                                                                      │
    │              echo 'Pipeline failed!'                                                     │
    │          }                                                                              │
    │      }                                                                                  │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions Workflow                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  # .github/workflows/ci-cd.yml                                                        │
    │  name: CI/CD Pipeline                                                                 │
    │                                                                                         │
    │  on:                                                                                    │
    │    push:                                                                                │
    │      branches: [ main, develop ]                                                       │
    │    pull_request:                                                                        │
    │      branches: [ main ]                                                                │
    │                                                                                         │
    │  jobs:                                                                                  │
    │    build-and-test:                                                                      │
    │      runs-on: ubuntu-latest                                                             │
    │                                                                                         │
    │      steps:                                                                             │
    │        - name: Checkout code                                                            │
    │          uses: actions/checkout@v3                                                      │
    │                                                                                         │
    │        - name: Set up JDK                                                               │
    │          uses: actions/setup-java@v3                                                    │
    │          with:                                                                          │
    │            java-version: '17'                                                           │
    │            distribution: 'temurin'                                                      │
    │                                                                                         │
    │        - name: Build with Maven                                                        │
    │          run: mvn -B -DskipTests clean package                                          │
    │                                                                                         │
    │        - name: Run tests                                                                │
    │          run: mvn test                                                                  │
    │                                                                                         │
    │        - name: Upload coverage                                                          │
    │          uses: codecov/codecov-action@v3                                                │
    │                                                                                         │
    │        - name: Build and push Docker                                                    │
    │          run: |                                                                         │
    │            docker build -t myapp:${{ github.sha }} .                                   │
    │            echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin│
    │            docker push myapp:${{ github.sha }}                                          │
    │                                                                                         │
    │        - name: Deploy to Kubernetes                                                     │
    │          uses: steebchen/kubectl@v2.0.0                                                 │
    │          with:                                                                          │
    │            config: ${{ secrets.KUBE_CONFIG }}                                           │
    │            command: apply -f k8s/                                                    │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### CI/CD 도구 비교

| 도구 | 특징 | 장점 | 단점 |
|------|------|------|------|
| **Jenkins** | 오픈소스, 플러그인 | 유연성 | 설정 복잡 |
| **GitHub Actions** | GitHub 통합 | 간편 | GitHub 종속 |
| **GitLab CI** | 통합 | DevOps 전체 | GitLab 필요 |
| **CircleCI** | 클라우드 | 관리 불필요 | 비용 |

### 배포 전략

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         배포 전략                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Blue-Green]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 두 환경 유지, 즉시 전환                                                             │
    │  │  • Rollback 쉬움                                                                   │
    │  │  • 리소스 2배 필요                                                                  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Canary]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 일부 트래픽만 새 버전으로                                                           │
    │  │  • 점진적 증가                                                                     │
    │  │  • 모니터링 중요                                                                    │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Rolling]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 인스턴스 순차적 교체                                                               │
    │  │  • 무중단 배포                                                                     │
    │  │  • 두 버전 공존 기간                                                               │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: CI/CD 구축
**상황**: 신규 프로젝트
**판단**:

```bash
# 1. Repository 구조
myapp/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── docker/
│   └── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── pom.xml
└── src/

# 2. Dockerfile
FROM maven:3.8-openjdk-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM openjdk:17-jdk-slim
COPY --from=build /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]

# 3. GitHub Secrets 설정
# DOCKER_USERNAME, DOCKER_PASSWORD, KUBE_CONFIG

# 4. 파이프라인 실행
# → GitHub Actions 탭에서 확인
```

---

## Ⅴ. 기대효과 및 결론

### CI/CD 기대 효과

| 효과 | 수동 | CI/CD |
|------|------|-------|
| **배포 주기** | 주~월 | 일~시간 |
| **실수** | 높음 | 낮음 |
| **피드백** | 느림 | 빠름 |
| **문제 발견** | 늦음 | 빠름 |

### 모범 사례

1. **빈번한 커밋**: 작은 단위
2. **자동 테스트**: 커밋마다
3. **코드 리뷰**: PR 필수
4. **모니터링**: 배포 후 확인
5. **롤백**: 빠른 복구

### 미래 전망

1. **GitOps**: Git 기반 운영
2. **Progressive Delivery**: 정교한 배포
3. **AI/Ops**: 자장된 최적화

### ※ 참고 표준/가이드
- **Jenkins**: Pipeline Docs
- **GitHub**: Actions Docs
- **DORA**: State of DevOps

---

## 📌 관련 개념 맵

- [통합 테스트](../4_testing/17_integration_testing.md) - CI 테스트
- [E2E 테스트](../4_testing/18_e2e_testing.md) - 사전 검증
- [Docker](../7_tools/23_docker.md) - 컨테이너
- [Kubernetes](../7_tools/24_kubernetes.md) - 오케스트레이션
