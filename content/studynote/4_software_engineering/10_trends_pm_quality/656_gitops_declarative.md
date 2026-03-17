+++
title = "656. GitOps 인프라 선언적 관리"
date = "2026-03-15"
weight = 656
[extra]
categories = ["Software Engineering"]
tags = ["GitOps", "Declarative", "Infrastructure as Code", "Kubernetes", "ArgoCD", "Automation"]
+++

# 656. GitOps 인프라 선언적 관리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 애플리케이션 소스코드와 더불어 인프라 및 설정 정보를 Git 저장소에 **단일 진실 공급원 (Single Source of Truth, SSOT)**으로 통합 관리하는 운영 패러다임입니다.
> 2. **가치**: Git의 커밋 ID를 통해 모든 변경 이력을 불변(Immutable)하게 기록하며, 배포 실패 시 `git revert`를 통한 초고속 롤백이 가능하여 **MTTR (Mean Time To Recover)**을 획기적으로 단축합니다.
> 3. **융합**: IaC (Infrastructure as Code)와 쿠버네티스(Kubernetes)의 선언형 API가 결합되어, 실제 상태(Actual State)와 원하는 상태(Desired State)의 차이를 자동으로 조정(Reconciliation)하는 자율 운영 체계를 실현합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 철학
**GitOps (Git Operations)**는 단순한 배포 자동화 도구가 아니라, **'운영(Operations)'의 패러다임을 '명령형(Imperative)'에서 '선언형(Declarative)'으로 전환**하는 철학입니다. 전통적인 운영에서는 관리자가 서버에 접속하여 스크립트를 실행하거나 명령어를 입력해 시스템을 변경했습니다(How). 반면, GitOps는 시스템이 가져야 할 상태(What)를 YAML이나 JSON과 같은 선언적 파일로 정의하고, Git 저장소에 커밋함으로써 운영을 수행합니다. 이때 Git은 단순한 버전 관리 도구를 넘어 운영의 **단일 진실 공급원 (Single Source of Truth, SSOT)** 역할을 수행합니다.

#### 2. 배경 및 필요성
**MSA (Microservices Architecture)**와 **CNCF (Cloud Native Computing Foundation)** 생태계의 확산으로 인해 관리해야 할 서비스와 인프라 리소스의 수가 폭발적으로 증가했습니다. 수십, 수백 개의 마이크로서비스를 수동으로 배포하고 관리하는 것은 불가능에 가까우며, 이는 **Configuration Drift (설정 누수)** 문제를 야기합니다. 설정 누수란 개발/스테이징 환경에서는 잘 작동하던 설정이 운영 환경에서 누락되거나 달라지는 현상을 말합니다. GitOps는 이러한 문제를 해결하기 위해 등장했습니다.

#### 3. 진화 과정
① **스크립트 & 수동 실행**: 매번 수동으로 서버에 접속하여 스크립트 실행 (오류 발생률 높음)
② **IaC (Infrastructure as Code)**: 인프라를 코드로 관리하지만, 배포는 여전히 Push 방식에 의존
③ **GitOps (Pull-based)**: Git 커밋을 트리거로 클러스터 내부 에이전트가 Pull하여 자동 배포 및 상태 동기화

#### 💡 비유: 주방의 레시피북과 자동화 로봇 주방장
전통적인 운영은 주인(관리자)이 주방장(서버)에게 "가스레인지를 켜고, 냄비를 올리고, 물을 500ml 부어라"라고 매번 구체적인 명령(How)을 내리는 방식입니다. 명령에 실수가 있거나 순서가 바뀌면 요리(시스템)가 망집니다. 반면 **GitOps**는 주인이 **'레시피북(Git)'**에 "완성된 라면 1인분"이라는 최종 결과물(What)을 사진이나 설명으로 정의해두는 것과 같습니다. 그러면 똑똑한 **로봇 주방장(Agent)**이 주기적으로 레시피북을 확인하여, 현재 주방 상태가 레시피와 다르면 스스로 재료를 가져와 요리를 완성합니다. 주인은 레시피만 수정하면 되고, 요리 과정은 로봇이 책임지는 구조입니다.

#### ASCII 다이어그램: 운영 패러다임의 변화
```text
   [Traditional Operations]         [GitOps Operations]
   (명령형 / Imperative)            (선언형 / Declarative)

   Manager                           Manager
     │                                 │
     ▼                                 ▼
  "Run script.sh" ───▶ Server      [Edit Git]      (Desire State)
     │                             (Commit "Change")
     ▼                                 │
  Server ──▶ Execution                 │
  (How to do)                         ▼
                              ┌─────────────────┐
                              │ Git Repository  │ ◀── Single Source of Truth
                              └─────────────────┘
                                     │
                                     │ (Pull & Watch)
                                     ▼
                              ┌─────────────────┐
                              │  GitOps Agent   │
                              │   (Controller)  │
                              └─────────────────┘
                                     │
      (Manual Execution)              ▼ (Auto Sync)
                              ┌─────────────────┐
                              │   Live Server   │
                              │  (Actual State) │
                              └─────────────────┘
```
*도입 해설*: 위 그림은 기존 방식과 GitOps 방식의 통제권한 이동을 보여줍니다. 기존에는 관리자가 서버를 직접 제어했지만, GitOps는 관리자가 Git을 수정하면, 내부의 에이전트가 이를 감지하여 서버를 제어합니다. 이는 관리자가 운영 서버에 대한 직접 접근 권한을 포기함으로써 보안과 안정성을 확보하는 핵심 메커니즘입니다.

#### 📢 섹션 요약 비유
마치 교통 체증을 해결하기 위해 교통총괄센터(Git)에서 전체 신호 체계(Desired State)를 결정하고, 각 교차로의 스마트 신호등(Agent)이 이 정보를 수신해 실시간으로 신호를 조정하는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 핵심 구성 요소 (5개 이상 모듈 분석)
GitOps 아키텍처는 클러스터 내부와 외부로 나뉘며, 각 구성 요소가 유기적으로 상호작용하여 시스템의 일관성을 유지합니다.

| 요소명 | 역할 | 내부 동작 및 프로토콜 | 비유 |
|:---|:---|:---|:---|
| **Git Repository** | **SSOT (Single Source of Truth)** | YAML/JSON 형태의 Manifest 저장. `git push` 시 이벤트 발생. | 법전 (법원의 판결 기준) |
| **CI (Continuous Integration) Server** | **빌드 및 검증** | 코드 수정 시 Docker Image 빌드 → Registry Push → Git Manifest의 Image Tag 업데이트 (`sed` 등). | 물자 생산 및 검수팀 |
| **GitOps Operator (Controller)** | **상태 조정 (Reconciler)** | **Watch Loop**를 통해 Git 상태 감지. 실제 클러스터 상태와 비교(Diff). | 현장 감독관 |
| **Live Cluster (K8s API)** | **실제 상태 (Actual State)** | Controller의 요청을 받아 리소스를 생성/수정/삭제 (CRUD). | 건설 현장 |
| **Container Registry** | **아티팩트 저장소** | 빌드된 이미지 저장. GitOps는 여기 있는 이미지 Digest/Tag를 참조하여 배포. | 창고 |
| **Notification Service** | **알림 및 피드백** | 배포 성공/실패 시 Slack/Email 등으로 알림. 특히 Drift 감지 시 경고. | 알림탑 |

#### 2. GitOps 피드백 루프 (Feedback Loop)
GitOps의 핵심은 단방향 배포가 아니라, **끊임없이 상태를 비교하고 교정하는 폐루프(Feedback Loop)**에 있습니다.

#### ASCII 다이어그램: GitOps 상세 동작 흐름
```text
   [Developer]                           [GitOps Pipeline]
        │                                      │
        │ 1. Code Commit & Push                │
        ├─────────────────────────────────────▶│
        │                                      │
        │                              [Git Repository]
        │                              (Desired State)
        │                                      │
        │                                      │ 2. Webhook / Polling
        │                                      ▼
        │                        ┌───────────────────────────┐
        │                        │   GitOps Controller       │
        │                        │   (ArgoCD / Flux)         │
        │                        └───────────────────────────┘
        │                                      │
        │                                      │ 3. Fetch Manifest
        │                                      │
        │                                      ▼
        │                        ┌───────────────────────────┐
        │                        │  Comparison Logic         │
        │                        │  (Git State vs K8s State) │
        │                        └───────────────────────────┘
        │                                      │
        │                                      │ 4. Difference (Drift) Detected?
        │                       ┌──────────────┴──────────────┐
        │                       │ No                         │ Yes
        │                       ▼                            ▼
        │                 [Sleep]                  ┌─────────────────────┐
        │                                            │  Apply K8s API    │
        │                                            │  (kubectl apply)  │
        │                                            └─────────────────────┘
        │                                                      │
        │                                                      │ 5. Resource Update
        │                                                      ▼
        │                                            ┌─────────────────────┐
        │                                            │  Kubernetes Cluster │
        │                                            │  (Actual State)     │
        │                                            └─────────────────────┘
        │                                                      │
        │                                                      │ 6. Status Sync
        │                                                      ▼
        │                                            [Health Check & Report]
        │                                                      │
        └──────────────────────────────────────────────────────┘
```
*도입 해설*: 이 다이어그램은 GitOps의 심장부인 '동기화(Reconciliation) 과정'을 시각화한 것입니다. 개발자가 코드를 수정하면 CI 시스템이 이를 빌드하고 Git 설정 파일을 업데이트합니다. 이때 GitOps 컨트롤러가 변경 사항을 감지하고, 현재 쿠버네티스 클러스터 상태와 비교합니다. 만약 누군가 수동으로 클러스터를 건드려 차이(Drift)가 발생하면, 컨트롤러는 Git에 정의된 대로 다시 되돌려놓습니다. 이를 통해 시스템은 항상 원하는 상태를 유지하려는 **자기 치유(Self-healing)** 능력을 갖게 됩니다.

#### 3. 심층 동작 원리: 상태 조정 (Reconciliation) 메커니즘
**Reconciliation**은 desired state(Git)와 actual state(Cluster) 간의 불일치를 해결하는 과정입니다. 이는 **K8s Controller 패턴**을 따릅니다.
1. **Observe (관측)**: `kube-apiserver`를 통해 현재 클러스터의 상태(Live Object)를 조회.
2. **Diff (비교)**: Git의 YAML 파일과 조회된 Live Object의 필드를 비교.
3. **Act (실행)**: 차이가 있다면 `PATCH` 또는 `CREATE/UPDATE` 요청을 API 서버로 전송.
4. **Feedback (피드백)**: 결과를 사용자에게 대시보드나 로그로 표시.

#### 4. 핵심 알고리즘: Kustomize를 활용한 Manifest 관리
실무 환경에서는 `base` 디렉토리에 공통 설정을 두고, `overlays/prod`나 `overlays/dev`에 환경별 변수를 덮어쓰는 **Kustomize** 전략을 주로 사용합니다.
```yaml
# example kustomization.yaml structure
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# 베이스 매니페스트 참조
resources:
- ../../base

# 환경별 파라미터 덮어쓰기 (Patch)
patchesStrategicMerge:
- deployment-patch.yaml

# 이미지 태그 자동화 (ImageTag transformer)
images:
- name: myapp
  newTag: "1.0.1" # CI 파이프라인에서 이 값을 자동으로 수정
```
위 코드는 GitOps 실무 적용 시 필수적인 구조입니다. CI 서버는 `newTag` 값만 수정하여 커밋하고, GitOps Operator는 이 변경된 태그를 감지하여 새로운 버전의 파드를 배포합니다.

#### 📢 섹션 요약 비유
마치 온도 조절기(Thermostat)가 현재 온도를 계속 측정하면서, 설정 온도와 다르면 히터를 켜거나 꺼서 방 안을 설정된 온도로 유지하려는 것과 같은 자동 제어 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 심층 기술 비교: Push 방식(CI 기반) vs Pull 방식(GitOps 기반)
운영의 **보안성(Security)**과 **안정성(Stability)** 측면에서 두 방식은 결정적인 차이를 보입니다.

| 비교 항목 | Push 방식 (기존 CI/CD) | Pull 방식 (GitOps) |
|:---:|:---|:---|
| **주체** | 외부 CI 서버 (Jenkins, GitHub Actions) | 내부 클러스터 에이전트 (ArgoCD, Flux) |
| **방향성** | CI가 클러스터로 접속 (Outbound → Inbound) | 에이전트가 Git을 확인 (Inbound → Outbound) |
| **자격 증명** | CI에 **클러스터 credential(Admin Key)** 필요 | 클러스터 내에 **Git Read Token** 저장 (Secret) |
| **방화벽** | 인바운드 포트를 열어야 하거나 VPN 필요 | 아웃바운드 통신만 가능하면 됨 (보안 우위) |
| **배포 트리거** | 스크립트 실행 완료 시점 1회 | Git 상태 변경 감지 시 지속적 동기화 |
| **Configuration Drift** | 방지 불가 (배포 후 수동 변경 감지 불가) | **자동 감지 및 복구** (Drift 방지) |
| **대표 도구** | Jenkins, Spinnaker, CircleCI | **ArgoCD**, **Flux CD** |

#### 2. 분석: 왜 ArgoCD/Flux가 Push 방식보다 안전한가?
CI 서버가 해킹당한다면, 공격자는 그 안에 저장된 **클러스터의 관리자 키(Kubeconfig)**를 탈취하여 운영 환경 전체를 장악할 수 있습니다. 반면, GitOps 방식에서 클러스터 내부의 Agent는 보통 Git 저장소에 대해 **Read-Only** 권한만 가집니다. Agent가 임의로 Git의 내용을 수정할 수 없고, 단지 Git을 바라보며 동기화만 수행합니다. 외부에서 클러스터로 명령을 내리는 통로가 없으므로 보안 노출 면적이 획기적으로 줄어듭니다.

#### 3. 융합 관점: 쿠버네티스(K8s)와의 시너지
GitOps는 쿠버네티스의 **'선언형 API(Declarative API)'** 설계 철학과 완벽하게 일치합니다.
- **Controller Pattern