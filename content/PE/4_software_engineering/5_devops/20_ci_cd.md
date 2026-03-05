+++
title = "20. CI/CD (Continuous Integration/Deployment)"
date = 2026-03-06
categories = ["studynotes-software-engineering"]
tags = ["CI", "CD", "Jenkins", "GitHub-Actions", "Pipeline", "DevOps"]
draft = false
+++

# CI/CD (Continuous Integration/Deployment)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CI/CD는 **"코드 변경을 **자동으로 빌드, **테스트, **배포하는 **DevOps 실천 방법론"**으로, **CI**(Continuous Integration)는 **자동 통합**, **CD**(Continuous Deployment/Delivery)는 **자동 배포**를 의미한다.
> 2. **가치**: **통합 문제**(Integration Hell)를 **조기 발견**하고 **배포 주기**를 **단축**하며 **빠른 피드백**으로 **품질**을 **향상**하고 **수동 작업**을 **자동화**하여 **실수**를 **줄인다**.
> 3. **융합**: **Jenkins**, **GitHub Actions**, **GitLab CI**, **CircleCI**가 **대표 도구**이며 **Pipeline-as-Code**, **Blue-Green Deployment**, **Canary Release**와 결합하여 **안정적인 배포**를 **구현**한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
CI/CD는 **"소프트웨어 변경을 자동으로 빌드, 테스트, 배포하는 프로세스"**이다.

**CI/CD의 3단계**:
- **CI**: 코드 통합 + 자동 테스트
- **CD**: 자동 배포 (Delivery: 수동 승인, Deployment: 완전 자동)
- **Automation**: 파이프라인 자동화

### 💡 비유
CI/CD는 **"자동 생산 라인"**과 같다.
- **원재료**: 코드
- **조립**: 빌드
- **검사**: 테스트
- **출하**: 배포

### 등장 배경

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD의 발전                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Waterfall (1970년대):
    • 계획 → 개발 → 테스트 → 배포
    • 릴리즈 주기: 개월~년
         ↓
Agile (2000년대):
    • 스프린트 기반 개발
    • 릴리즈 주기: 주~월
         ↓
CI (Continuous Integration):
    • 자동 통합 + 테스트
    • 일일 빌드
         ↓
CD (Continuous Deployment):
    • 자동 배포
    • 하루 수십 배포
```

---

## Ⅱ. 아키텍처 및 핵심 원리

### CI/CD 파이프라인

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  Developer                                                                             │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  git commit → git push                                                            │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                     │                                                   │
    │                                     ▼                                                   │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  CI Server (Jenkins/GitHub Actions)                                                │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  1. Build                                                                       │  │  │
    │  │  │     • Maven/Gradle (Java)                                                       │  │  │
    │  │  │     • npm/yarn (Node.js)                                                        │  │  │
    │  │  │     • Docker Image Build                                                         │  │  │
    │  │  │                                                                                  │  │
    │  │  │  2. Test                                                                        │  │
    │  │  │     • Unit Test                                                                  │  │
    │  │  │     • Integration Test                                                           │  │
    │  │  │     • Code Coverage (JaCoCo, Jest)                                               │  │
    │  │  │                                                                                  │  │
    │  │  │  3. Quality Check                                                               │  │
    │  │  │     • Lint (ESLint, Checkstyle)                                                  │  │
    │  │  │     • Security Scan (Snyk, OWASP)                                                │  │
    │  │  │                                                                                  │  │
    │  │  │  4. Package                                                                     │  │
    │  │  │     • Docker Image Push to Registry                                             │  │
    │  │  │     • JAR/WAR Upload                                                             │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  │                                                                                  │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  5. Deploy (CD)                                                                 │  │  │
    │  │  │     • Staging Environment (자동)                                                │  │  │
    │  │  │     • E2E Test                                                                   │  │  │
    │  │  │     • Production Deployment (수동 승인 또는 자동)                                  │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    │                                     │                                                   │
    │                                     ▼                                                   │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Environments                                                                        │  │
    │  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                           │  │
    │  │  │ Dev          │   │ Staging      │   │ Production   │                           │  │
    │  │  │ (매 배포)     │   │ (자동)       │   │ (승인/자동)   │                           │  │
    │  │  └──────────────┘   └──────────────┘   └──────────────┘                           │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Jenkins Pipeline 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         Jenkinsfile (Declarative Pipeline)                             │
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
    │          stage('Security Scan') {                                                       │
    │              steps {                                                                    │
    │                  sh 'trivy image ${IMAGE_NAME}'                                         │
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
    │          stage('Deploy to Staging') {                                                   │
    │              steps {                                                                    │
    │                  sh 'kubectl apply -f k8s/staging/'                                     │
    │              }                                                                          │
    │          }                                                                              │
    │                                                                                         │
    │          stage('Deploy to Production') {                                                 │
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
    │          always {                                                                       │
    │              cleanWs()                                                                   │
    │          }                                                                              │
    │          success {                                                                      │
    │              emailext subject: "Build Success: ${env.JOB_NAME}",                         │
    │                       body: "Build ${BUILD_NUMBER} succeeded.",                          │
    │                       to: "team@example.com"                                             │
    │          }                                                                              │
    │      }                                                                                  │
    │  }                                                                                       │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

### GitHub Actions 예시

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions Workflow                                          │
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
    │        - uses: actions/checkout@v3                                                      │
    │                                                                                         │
    │        - name: Set up JDK 17                                                           │
    │          uses: actions/setup-java@v3                                                    │
    │          with:                                                                          │
    │            java-version: '17'                                                           │
    │            distribution: 'temurin'                                                      │
    │                                                                                         │
    │        - name: Cache Maven packages                                                     │
    │          uses: actions/cache@v3                                                         │
    │          with:                                                                          │
    │            path: ~/.m2                                                                  │
    │            key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}                       │
    │                                                                                         │
    │        - name: Build with Maven                                                        │
    │          run: mvn -B -DskipTests clean package                                          │
    │                                                                                         │
    │        - name: Run tests                                                                │
    │          run: mvn test                                                                  │
    │                                                                                         │
    │        - name: Generate coverage report                                                 │
    │          run: mvn jacoco:report                                                         │
    │                                                                                         │
    │        - name: Upload coverage to Codecov                                               │
    │          uses: codecov/codecov-action@v3                                                │
    │          with:                                                                          │
    │            files: ./target/site/jacoco/jacoco.xml                                       │
    │                                                                                         │
    │        - name: Build Docker image                                                       │
    │          run: |                                                                         │
    │            docker build -t myapp:${{ github.sha }} .                                    │
    │            docker tag myapp:${{ github.sha }} myapp:latest                              │
    │                                                                                         │
    │        - name: Login to Docker Hub                                                      │
    │          uses: docker/login-action@v2                                                   │
    │          with:                                                                          │
    │            username: ${{ secrets.DOCKERHUB_USERNAME }}                                   │
    │            password: ${{ secrets.DOCKERHUB_TOKEN }}                                      │
    │                                                                                         │
    │        - name: Push Docker image                                                        │
    │          run: docker push myapp:${{ github.sha }}                                       │
    │                                                                                         │
    │    deploy:                                                                              │
    │      needs: build-and-test                                                             │
    │      runs-on: ubuntu-latest                                                             │
    │      if: github.ref == 'refs/heads/main' && github.event_name == 'push'                 │
    │                                                                                         │
    │      steps:                                                                             │
    │        - name: Deploy to Kubernetes                                                     │
    │          uses: steebchen/kubectl@v2.0.0                                                 │
    │          with:                                                                          │
    │            config: ${{ secrets.KUBE_CONFIG }}                                           │
    │            command: apply -f k8s/production/                                             │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### CI/CD 도구 비교

| 도구 | 특징 | 장점 | 단점 |
|------|------|------|------|
| **Jenkins** | 오픈소스, 플러그인 | 유연성 | 설정 복잡 |
| **GitHub Actions** | GitHub 통합 | 간편 | GitHub 종속 |
| **GitLab CI** | GitLab 내장 | 통합 | GitLab 필요 |
| **CircleCI** | 클라우드 | 관리 불필요 | 비용 |

### 배포 전략

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         배포 전략                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [Blue-Green Deployment]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 두 환경 유지 (Blue, Green)                                                           │
    │  │  • 전환으로 즉시 롤백 가능                                                            │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Load Balancer                                                                      │  │
    │  │  ┌──────────────────────────────────────────────────────────────────────────────┐  │  │
    │  │  │  Traffic                                                                           │  │  │
    │  │  │    ↓                                                                              │  │  │
    │  │  │  ┌──────────────┐         ┌──────────────┐                                     │  │  │
    │  │  │  │ Blue         │  ←───   │ Green        │                                     │  │  │
    │  │  │  │ (v1.0)       │         │ (v2.0 NEW)   │                                     │  │  │
    │  │  │  │   Active     │         │   Standby    │                                     │  │  │
    │  │  │  └──────────────┘         └──────────────┘                                     │  │  │
    │  │  │           Switch → Green Active, Blue Standby                                   │  │  │
    │  │  └──────────────────────────────────────────────────────────────────────────────┘  │  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘

    [Canary Deployment]

    ┌──────────────────────────────────────────────────────────────────────────────────────────┐
    │  • 일부 사용자에게만 새 버전 배포                                                        │
    │  │  • 점진적으로 늘려나가며 검증                                                          │
    │  │                                                                                      │
    │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
    │  │  Users → Load Balancer                                                              │  │
    │  │           └─ 90% → v1.0 (Stable)                                                    │  │
    │  │           └─ 10% → v2.0 (Canary)                                                    │  │
    │  │                                                                                  │  │
    │  │  → 모니터링 후 문제 없으면 비율 증가 (10% → 50% → 100%)                              │  │
    │  └────────────────────────────────────────────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 기술사적 판단 (실무 시나리오)

#### 시나리오: CI/CD 구축
**상황**: 신규 프로젝트 CI/CD
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
└── pom.xml

# 2. Dockerfile (Multi-stage)
FROM maven:3.8-openjdk-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM openjdk:17-jdk-slim
COPY --from=build /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]

# 3. Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: registry.example.com/myapp:${IMAGE_TAG}
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

# 4. GitHub Actions Secret 설정
# DOCKERHUB_USERNAME, DOCKERHUB_TOKEN
# KUBE_CONFIG (Base64 encoded)

# 5. 파이프라인 실행 모니터링
# → GitHub Actions 탭에서 확인
```

---

## Ⅴ. 기대효과 및 결론

### CI/CD 기대 효과

| 효과 | 수동 배포 | CI/CD |
|------|---------|-------|
| **배포 주기** | 주~월 | 일~시간 |
| **통합 문제** | 늦은 발견 | 조기 발견 |
| **실수** | 높음 | 낮음 |
| **피드백** | 느림 | 빠름 |

### CI/CD 모범 사례

1. **빈번한 커밋**: 작은 단위로
2. **자동 테스트**: 커밋마다 실행
3. **배포 자동화**: 스크립트화
4. **모니터링**: 메트릭 수집
5. **롤백 계획**: 빠른 복구

### 미래 전망

1. **GitOps**: Git 기반 운영
2. **Progressive Delivery**: 더 정교한 배포
3. **AI/Ops**: 자장된 문제 해결

### ※ 참고 표준/가이드
- **Jenkins**: Pipeline Documentation
- **GitHub**: Actions Documentation
- **DORA**: DevOps Report

---

## 📌 관련 개념 맵

- [통합 테스트](../4_testing/17_integration_testing.md) - CI 테스트
- [E2E 테스트](../4_testing/18_e2e_testing.md) - 배포 전 검증
- [Docker](../7_tools/23_docker.md) - 컨테이너화
- [Kubernetes](../7_tools/24_kubernetes.md) - 오케스트레이션
