---
title: "GitOps ArgoCD Flux Declarative Deployment"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 619
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Git 저장소를 배포 대상의 **단일 진실 공급원(Single Source of Truth)**으로 삼고, 클러스터 내부의 **조정 컨트롤러(Reconciliation Controller)**가 선언적 매니페스트(Kustomize/Helm/Plain YAML)를 주기적으로 풀(Pull)하여 실제 상태(Actual State)를 원하는 상태(Desired State)로 수렴시키는 **풀 기반(Pull-based) 조정 루프** 운영 체계
> 2. **가치**: DORA 4대 지표 중 **배포 빈도(Deployment Frequency) 10배^, 변경 리드 타임(Lead Time for Changes) 70%v, MTTR(Mean Time To Restore) 60%v, 변경 실패율(Change Failure Rate) 50%v** 효과를 제공하며, Git 커밋 이력 자체가 완벽한 감사 로그(Audit Log)가 되어 **컴플라이언스(ISO 27001, SOC2) 및 RBAC 기반의 4-eyes 원칙** 자동 충족
> 3. **판단 포인트**: **ArgoCD(UI 중심, 멀티테넌시 강함, ApplicationSet 패턴)** vs **Flux(모듈형 GitOps Toolkit, Helm/Kustomize/Image 컨트롤러 분리, GitOps Engine 경량)** 중 조직 상황에 맞는 도구 선택, **비밀값 관리(Sealed Secrets vs SOPS vs External Secrets Operator)**, **App of Apps vs Kustomize Overlay vs ApplicationSet Generator** 중 애플리케이션 프로모션 전략, **동기화 정책(Automated/Self-Heal) 및 Sync Window 운영**

---

## Ⅰ. 개요 및 필요성

전통적인 CI/CD 파이프라인(Jenkins, GitLab CI, GitHub Actions)은 빌드/테스트 후 `kubectl apply` 또는 Helm CLI를 실행하여 **외부에서 클러스터로 명령을 푸시(Push)**한다. 이 방식은 다음과 같은 근본적 문제를 안고 있다.

- **클러스터 외부에서 cluster-admin 자격증명이 노출**되어 RBAC 침해 시 재앙적 영향
- **파이프라인 실행자(Jenkins Agent)와 클러스터 간 네트워크 의존성** 및 방화벽 Hole 필요
- **CI 도구가 다운되면 배포 불가**, 배포 도구 자체의 SPOF 발생
- **클러스터에서 직접 `kubectl edit`으로 변경 시** Git 저장소와 실제 상태 간 **드리프트(Drift)** 발생, 추적 불가
- 배포 이력이 Jenkins의 Build History에만 남아 **Git과 분리된 감사 추적** 필요

GitOps는 Weaveworks가 2017년 처음 명명(CNCF TAG App Delivery 정식 채택)한 패러다임으로, **"운영 환경의 모든 선언적 명세를 Git에서 관리하고, 클러스터 내부 에이전트가 이를 지속적으로 동기화"**하는 것이다. ArgoCD(2018, Intuit 오픈소스 -> CNCF Incubator 2020 -> Graduated 2022)와 Flux(2016, Weaveworks -> CNCF Graduated 2023)가 양대 표준이다.

```text
   +------------------- 전통 Push-based CI/CD -------------------+
   |                                                             |
   |   Developer --push--► Git Repo --trigger--► Jenkins          |
   |                                              |              |
   |                                              | kubectl      |
   |                                              v apply        |
   |                                        +----------+         |
   |                                        | K8s      |         |
   |                                        | Cluster  |         |
   |                                        +----------+         |
   |   문제: Jenkins Agent가 cluster-admin 토큰 보유 (위험)      |
   |         누군가 cluster에서 직접 수정 시 추적 불가           |
   +-------------------------------------------------------------+

                          v GitOps 패러다임 전환 v

   +----------------------- Pull-based GitOps ------------------+
   |                                                            |
   |   Developer --PR/Merge--► Git Repo (Source of Truth)       |
   |                                ^                           |
   |                                | pull (3분 주기)           |
   |                                |                           |
   |                          +-----+------+                    |
   |                          |  ArgoCD /  |   클러스터 내부     |
   |                          |   Flux     |   에이전트          |
   |                          |  Controller|   (RBAC 최소 권한) |
   |                          +-----+------+                    |
   |                                | sync                      |
   |                                v                           |
   |                          +----------+                     |
   |                          |  K8s API |                     |
   |                          |  Server  |                     |
   |                          +----+-----+                     |
   |                               |                            |
   |                          +----v-----+                      |
   |                          | 실제 상태|                      |
   |                          | (Actual) | --status-► Git diff  |
   |                          +----------+                      |
   |   장점: 클러스터 외부 자격증명 불필요                       |
   |         모든 변경이 Git 커밋/PR로 추적됨                    |
   |         자동 드리프트 감지 및 Self-Heal                     |
   +------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Push 방식은 "택배 기사(Jenkins)가 직접 집(K8s) 현관 비밀번호를 알고 문을 두드리는 것"이고, GitOps는 "집 안에 사는 똑똑한 집사(ArgoCD/Flux Controller)가 우편함(Git Repo)을 3분마다 확인하고, 거실 인테리어(desired state)와 다른 부분이 있으면 알아서 정돈해주는 것"이다. 택배 기사가 사라져도(파이프라인 다운) 인테리어는 유지되고, 누가 직접 가구를 옮겨도(드리프트) 집사가 원래대로 복구한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 가. ArgoCD 아키텍처 (단일 클러스터)

```text
                        +--------------------------------------------+
                        |              ArgoCD Namespace              |
   Git Repos  ---------►|  +--------------+    +--------------+      |
   (HTTPS/SSH)          |  |  Repo Server |◄--►|    Redis     |      |
                        |  |  (gRPC:50051)|    |  (cache/dedup)|      |
   Helm OCI ----------►|  +------+-------+    +--------------+      |
                        |         | manifest (yaml/jsonnet/helm)     |
   Webhook ------------►|  +------v-------+                          |
   (Git push event)     |  | Application  |    +--------------+     |
                        |  |  Controller  |◄--►|  Dex Server  |     |
   User/UI/API --------►|  |  (reconcile  |    | (OIDC/LDAP)  |     |
                        |  |   loop 3m)   |    +--------------+     |
                        |  +------+-------+                          |
                        |         | apply/prune                      |
                        +---------+----------------------------------+
                                  v
   +------------------ ArgoCD ApplicationSet Controller ----------+
   |  CRD: ApplicationSet (Generator: Git, Directory, Cluster)    |
   |  -> 다수 Application 매트릭 자동 생성 (Templating)            |
   +--------------------------------------------------------------+
                                  v
   +--------------------------------------------------------------+
   |              Destination K8s Cluster(s)                      |
   |   +------------------+  +------------------+                 |
   |   | app1-staging NS  |  | app2-prod NS     |                 |
   |   | Deployment/State |  | Deployment/State |                 |
   |   | fulSet/Service   |  | fulSet/Service   |                 |
   |   +------------------+  +------------------+                 |
   |                                                              |
   |   ※ ArgoCD Application Controller가 직접 K8s API Server에  |
   |     변경 적용 (멀티 클러스터는 in-cluster/secret 기반)      |
   +--------------------------------------------------------------+
```

**핵심 CRD (Custom Resource Definition):**
- `Application`: 단일 앱 정의 (source, destination, syncPolicy)
- `AppProject`: 논리적 그룹 + RBAC + 클러스터/네임스페이스 화이트리스트
- `ApplicationSet`: 매트릭 기반 다수 Application 자동 생성 (Templating 엔진)

**Sync 정책 트리거 3종:**
1. **Manual**: 사용자가 UI/CLI에서 `argocd app sync` 실행
2. **Automated**: Git 변경 감지 시 자동 동기화 (`automated.selfHeal: true` 권장)
3. **WebHook**: GitHub/GitLab Push 이벤트 즉시 트리거 (3분 대기 회피)

### 나. Flux 아키텍처 (GitOps Toolkit 모듈형)

```text
   +--------------------- Flux v2 GitOps Toolkit ----------------------+
   |                                                                  |
   |  +------------------+         +-----------------------+          |
   |  | Source Controller |◄--------| GitRepository CRD     |          |
   |  | (git fetch,       |         | HelmRepository CRD    |          |
   |  |  OCI pull,        |         | OCIRepository CRD     |          |
   |  |  Helm index fetch)|         | Bucket CRD (S3)       |          |
   |  +---------+---------+         +-----------------------+          |
   |            | artifact (tar.gz)                                    |
   |            v                                                     |
   |  +------------------+         +-----------------------+          |
   |  |Kustomize Controller|◄------| Kustomization CRD      |          |
   |  | (kustomize build,  |        | (path, interval,      |          |
   |  |  apply, health)    |        |  prune, healthChecks) |          |
   |  +---------+---------+         +-----------------------+          |
   |            |                                                      |
   |            |              +-----------------------+              |
   |            +-------------►| Helm Controller       |