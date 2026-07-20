---
title: "Jenkins, GitLab CI, GitHub Actions"
date: "2026-03-04"
tags:
  - "studynote-cloud-architecture"
weight: 166
---
## 핵심 인사이트 (3줄 요약)
- CI/CD 파이프라인의 생애주기(Build-Test-Deploy)를 자동화하는 핵심 소프트웨어 솔루션임.
- 오픈소스(Jenkins), 저장소 통합형(GitLab), 클라우드 네이티브(GitHub Actions) 등 다양한 유형이 존재함.
- "Pipeline as Code"를 통해 배포 절차를 코드로 관리하여 형상 관리와 재사용성을 극대화함.

### Ⅰ. 개요 (Context & Background)
수동으로 빌드하고 FTP로 배포하던 시대는 끝났다. 현대의 클라우드 개발 환경에서는 변경된 코드가 저장소에 들어오는 순간부터 운영 환경에 반영되기까지의 일련의 과정을 정교하게 오케스트레이션해야 한다. <strong>CI/CD 파이프라인 도구</strong>는 이러한 복잡한 워크플로우를 자동화하고 시각화하여, 개발 팀이 빠르고 안정적으로 소프트웨어를 릴리스할 수 있도록 돕는 데 필수적인 역할을 한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
CI/CD 도구는 중앙 제어(Controller/Master)와 실제 작업을 수행하는 실행기(Agent/Runner) 구조로 이루어진다.

```text
[ Developer ] --(Push)--> [ Source Repo (Git) ]
                                |
                                v (Webhook)
+-----------------------------------------------------------+
|               [ CI/CD Tool Controller ]                   |
|  - Workflow Orchestrator / Pipeline definitions (.yml)    |
+-----------------------------------------------------------+
          | (Dispatch Job)         | (Dispatch Job)
          v                        v
+----------------------+   +----------------------+
| [ Build Agent 1 ]    |   | [ Deploy Runner 2 ]  |
| - Compile & Test     |   | - K8s Deployment     |
| - Containerize (Build)   | - Security Scanning  |
+----------------------+   +----------------------+
```

1. **Trigger**: Git Push, PR 생성, 일정 예약(Schedule) 등 특정 이벤트가 발생하면 파이프라인이 시작된다.
2. <strong>Pipeline as Code</strong>: 배포 절차를 `Jenkinsfile`, `.gitlab-ci.yml`, `action.yml` 등 코드로 작성하여 형상 관리한다.
3. <strong>Artifact Management</strong>: 빌드 결과물(Jar, Docker Image 등)을 저장소(Nexus, ECR)에 안전하게 보관하고 다음 단계로 전달한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 도구 | Jenkins (젠킨스) | GitLab CI/CD | GitHub Actions |
| :--- | :--- | :--- | :--- |
| **유형** | 오픈소스 (전통적 강자) | 통합형 (코드+CI/CD) | 클라우드 서비스형 (GitHub 통합) |
| **강점** | 수만 개의 플러그인, 자유로운 커스터마이징 | 단일 플랫폼 내의 끊김 없는 워크플로우 | 마켓플레이스를 통한 공유 재사용, 서버리스 실행기 |
| **관리 부담** | 직접 서버 구축 및 유지보수 필요 | 보통 혹은 SaaS 활용 시 낮음 | 매우 낮음 (완전 관리형 가능) |
| **적정 규모** | 복잡한 레거시가 섞인 엔터프라이즈 | 올인원 도구를 선호하는 조직 | 오픈소스 프로젝트, 클라우드 네이티브 스타트업 |

### Ⅳ. 실무 적용 및 실무적 판단 (Strategy & Decision)
- **적용 시점**: 프로젝트의 규모와 상관없이 형상 관리를 시작하는 시점부터 CI/CD 도구를 도입하여 자동화된 품질 검증 체계를 구축해야 한다.
- **실무적 판단**: 도구의 선택보다 중요한 것은 <strong>"벤더 종속성(Lock-in)"</strong>과 <strong>"보안(Secret Management)"</strong>이다. 파이프라인 코드에 API 키나 패스워드가 노출되지 않도록 전용 Vault 서비스를 연동해야 하며, 환경이 바뀌어도 쉽게 이식할 수 있도록 Docker 기반의 배포 스크립트를 표준화하는 것이 권장된다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
CI/CD 도구는 개발자의 단순 반복 노동을 제거하고 고부가가치 업무에 집중하게 해준다. 이는 조직의 민첩성(Agility)을 높이는 가장 강력한 수단이다. 향후에는 테크톤(Tekton)과 같은 쿠버네티스 네이티브 CI/CD 솔루션이나, GitOps 도구(ArgoCD)와 결합하여 인프라와 앱의 상태를 100% 동기화하는 방향으로 기술 표준이 강화될 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- <strong>Pipeline as Code</strong>: 배포 절차의 코드화.
- **Self-hosted Runner**: 보안상의 이유로 내부 망에 두는 실행기.
- <strong>Webhook</strong>: Git 저장소와 CI/CD 도구 간의 실시간 통신 매커니즘.

### 👶 어린이를 위한 3줄 비유 설명
- 로봇 공장장님이 '장난감 만드는 기계'들을 관리하는 것과 같아요. (CI/CD Tool)

### 📈 관련 키워드 및 발전 흐름도

```text
수동 빌드 · 수동 배포 (느림 · 오류)
    |
    v
CI/CD 도구: Jenkins · GitHub Actions · GitLab CI · ArgoCD
    +-► Pipeline as Code: YAML 선언적 정의
    +-► 아티팩트 관리: Nexus · Harbor · ECR
    |
    v
GitOps: Git 단일 진실 소스 -> 자동 동기화
```
- "먼저 나사를 조이고, 그다음에 색칠을 하고, 마지막으로 상자에 넣어!"라고 순서를 정해주죠.
- 공장장님이 시키는 대로 기계들이 알아서 척척 만들어주니까 실수가 없는 멋진 공장이 된답니다.
