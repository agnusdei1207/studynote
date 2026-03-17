+++
title = "724. 인프라스트럭처 애즈 코드 (IaC) 테라폼"
date = "2026-03-15"
weight = 724
[extra]
categories = ["Software Engineering"]
tags = ["IaC", "Infrastructure as Code", "Terraform", "Cloud Native", "Automation", "DevOps"]
+++

# 724. 인프라스트럭처 애즈 코드 (IaC) 테라폼

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 서버, 네트워크, DB와 같은 인프라 리소스의 라이프사이클을 관리형 콘솔(Manual)이 아닌, **선언적 기계 판독 가능 데이터(Declarative Machine-readable Data)**로 정의하여 자동화하는 패러다임의 전환임.
> 2. **테라폼 (Terraform)**: **HCL (HashiCorp Configuration Language)** 기반의 선언적 언어로 목표 상태(Goal State)를 정의하고, **프로바이더(Provider)** 플러그인을 통해 클라우드 API와 상호작용하여 현재 상태를 목표 상태로 수렴시키는 멱등성(Idempotency) 엔진임.
> 3. **가치**: 인프라 변경 사항을 버전 관리(Versioning)하여 감사성을 확보하고, **환경 불일치(Configuration Drift)**를 근본적으로 방지하며, 인적 실수(Human Error)를 배제하여 프로비저닝 속도를 획기적으로 단축시킴.

---

### Ⅰ. 개요 (Context & Background)

**개념 및 철학**
**IaC (Infrastructure as Code)**는 데이터센터, 서버, 네트워크 스위치, 로드 밸런서 등의 물리적 및 가상화된 인프라 자원을 소프트웨어 코드로 취급하여 정의, 배포, 관리하는 기술 철학입니다. 전통적인 '수동 접속 및 CLI(Command Line Interface) 명령어 입력' 방식에서 벗어나, 인프라를 소스코드의 형태로 기술하고 소프트웨어 개발 프로세스(**SDLC**: Software Development Life Cycle)를 적용하여 리뷰, 테스트, 배포하는 방식입니다.

**등장 배경**
클라우드 컴퓨팅(**Cloud Computing**)의 도입으로 인프라 확장이 주문형으로 가능해졌으나, 관리 포인트가 폭발적으로 증가하면서 다음과 같은 문제가 대두되었습니다.
1.  **Snowflake Servers (눈송이 서버)**: 수동으로 설정된 서버들이 저마다 다른 설정을 가지게 되어 재현이 불가능해지는 현상.
2.  **Configuration Drift (설정 변경 누수)**: 수동 수정으로 인해 코드로 정의된 상태와 실제 운영 중인 인프라 상태가 달라지는 현상.
3.  **Management Overhead**: 대규모 트래픽 처리를 위한 긴급 확장(Scale-out) 상황에서 수작업의 한계.

테라폼은 이러한 문제를 해결하기 위해 2014년 HashiCorp사에 의해 발표되었으며, 단일 툴로 멀티 클라우드(AWS, Azure, GCP) 환경을 통합 관리하는 **Agonic**한 특성을 가집니다.

**💡 비유: 마인크래프트의 청사진과 건축가**
IaC는 마인크래프트 게임에서 건물을 블록 하나하나 손으로 쌓는 대신, **'청사(Blueprint)'** 파일을 작성하여 게임 엔진이 그 설계를 읽고 자동으로 건물을 조립하는 것과 같습니다. 건물이 무너지거나 실수로 파괴되어도 청사진 파일만 있다면 언제든지 정확히 똑같은 건물을 1초 만에 복원할 수 있습니다.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│           [ Traditional Manual vs. IaC (Terraform) Workflow ]               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Manual Approach]                     [IaC Approach (Terraform)]          │
│                                                                             │
│  (Human)                              (Architect)                          │
│    │                                     │                                 │
│    ▼                                     ▼                                 │
│  SSH Login -> Run Commands       Write Code (HCL) -> Git Push               │
│    │                                     │                                 │
│    ▼                                     ▼                                 │
│  Uncertain Result                   Terraform Apply                       │
│  (Is it correct? No record!)            │                                 │
│                                         ▼                                 │
│                                    Consistent Infrastructure               │
│                                    (Guaranteed by Code)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **📢 섹션 요약 비유**: 인프라를 코드로 관리한다는 것은, 매일 다른 모양으로 손으로 빵을 굽는 빵집에서, **'정확한 무게와 모양이 기술된 제조 설비图纸'**를 넣으면 누르는 버튼 하나로 똑같은 빵이 찍혀 나오는 자동화 공장을 만드는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

테라폼의 작동은 크게 **설정 정의(Write)**, **상태 관리(State)**, **실행 계획(Plan)**, **자원 적용(Apply)**의 4단계로 이루어지며, 이 과정에서 핵심적인 역할을 하는 구성 요소들은 다음과 같습니다.

#### 1. 핵심 구성 요소 및 내부 동작 표

| 요소 (Component) | 역할 (Role) | 내부 동작 (Internal Behavior) | 프로토콜/형식 | 비유 |
|:---:|:---|:---|:---:|:---|
| **Configuration** | 인프라 정의 | 사용자가 생성하려는 리소스의 속성(타입, 이름, 파라미터)을 기술 | **HCL** (.tf), JSON | 건물 설계도 |
| **State File** | 현황 바인딩 | 실제 클라우드에 생성된 리소스의 메타데이터(ID, IP 등)를 매핑하여 저장 | JSON (Binary) | 실시간 재고 현황표 |
| **Provider** | API 통신 | 각 클라우드 벤더(AWS/Azure)의 고유 API를 호출하여 리소스를 CRUD | gRPC / REST API | 자재 공급업체 |
| **Plan Engine** | Diff 생성 | 코드(Desired)와 State(Current)를 비교하여 실행 계획(Execution Plan) 수립 | Graph DAG | 시뮬레이션 시뮬레이터 |
| **Backend** | 저장소 관리 | State 파일을 로컬이 아닌 원격 저장소(S3/DynamoDB)에 두어 팀 협업 및 Lock 관리 | HTTP(S), Consul | 은행 금고 |

#### 2. 테라폼 실행 라이프사이클 아키텍처

테라폼이 코드를 실행하여 인프라를 생성하는 과정은 **그래프(Graph)** 기반의 의존성 해석 과정을 거칩니다.

```text
    [ 1. WORKSPACE (Code) ]
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  main.tf                                                                 │
    │  resource "aws_vpc" "main" {  cidr = "10.0.0.0/16" }                     │
    │  resource "aws_subnet" "public" {                                         │
    │     vpc_id     = aws_vpc.main.id        <-- (Implicit Dependency)       │
    │     cidr_block = "10.0.1.0/24"                                            │
    │  }                                                                       │
    └──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ (terraform init)
    [ 2. INITIALIZATION ]
    Downloads Provider Plugins (AWS Binary) -> .terraform/
                                   │
                                   ▼ (terraform plan)
    [ 3. PLANNING (Graph Theory) ]
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  ○ aws_vpc.main                                                             │
    │    │                                                                         │
    │    └── ○ aws_subnet.public  (VPC 생성 후 Subnet 생성 순서 계산)               │
    │                                                                              │
    │  Output: + 1 to create, ~ 0 to change, - 0 to destroy                        │
    └──────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ (terraform apply)
    [ 4. EXECUTION & STATE UPDATE ]
    ┌───────────────────┐         ┌───────────────────┐
    │   Terraform Core  │───────▶ │   Cloud Provider  │
    │ (Graph Executor)  │  API    │   (AWS, Azure)    │
    └───────────────────┘         └───────────────────┘
           ▲                                 │
           │      (Resource IDs/Attrs)       │
           └─────────────────────────────────┘
                          │
                          ▼
               [ 5. STATE FILE (terraform.tfstate) ]
               { "version": 4, "resources": [ ... ], "serial": 1 }
```

**해설 (Diagram Explanation)**
1.  **코드 작성 (Workspace)**: 사용자는 `.tf` 파일에 리소스 간의 의존성(Dependency)을 암시적으로(참조) 또는 명시적으로(`depends_on`) 정의합니다.
2.  **초기화 (Init)**: 테라폼은 설정된 프로바이더(AWS, GCP 등)의 바이너리를 다운로드하여 실행 가능한 환경을 구성합니다.
3.  **계획 (Plan)**: 테라폼 코어는 현재 **State 파일**과 작성된 **코드**를 비교합니다. 이때 리소스 간 의존성을 분석하여 **DAG (Directed Acyclic Graph, 방향성 비순환 그래프)**를 생성하고, 순서대로 어떤 리소스를 생성(Create), 수정(Update), 삭제(Destroy)할지 미리 시뮬레이션 합니다.
4.  **적용 (Apply)**: 그래프 순서에 따라 프로바이더에게 API 요청을 전송합니다. 성공적으로 리소스가 생성되면, 그 결과(예: 할당된 Public IP)를 **State 파일**에 다시 기록합니다.

#### 3. 핵심 알고리즘: 선언적 상태 수렴 (Declarative Convergence)

테라폼은 "어떻게(How) 만들지"가 아니라 "무엇(What)을 만들지"에 집중합니다. 이를 위해 **HCL (HashiCorp Configuration Language)** 문법을 사용하며, 상태 관리의 핵심인 `terraform.tfstate` 파일은 인프라의 심장입니다.

```hcl
# main.tf (예시: AWS EC2 Instance)
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Machine Image ID
  instance_type = "t3.micro"               # Instance Type
  
  # 내부 함수 및 메타데이터 참조
  tags = {
    Name = "WebServer-${terraform.workspace}" # Dynamic Tagging
  }
}

# 데이터 소스 참조 (외부 상태 조회)
data "aws_vpc" "default" {
  default = true
}
```

> **📢 섹션 요약 비유**: 테라폼의 상태 파일과 실행 엔진은 마치 **'택배 배송 시스템의 허브 센터'**와 같습니다. 고객(사용자)은 목적지만(최종 상태) 적어서 보내면, 허브 센터(테라폼)가 현재 택배의 위치(State)를 확인하고, 운송 장비(프로바이더)를调度하여 최단 경로(그래프)로 물건을 배송(적용)합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

IaC 도구는 크게 **선언적(Declarative)**과 **명령형(Imperative)**으로 나뉘며, 테라폼은 전자의 대표 주자입니다.

#### 1. 기술적 심층 비교: Terraform vs. Ansible

| 구분 | 테라폼 (Terraform) | 앤서블 (Ansible) |
|:---|:---|:---|
| **접근 방식** | **선언적 (Declarative)** | **명령형 (Imperative)** |
| **목표** | "목표 상태(DS)를 정의" | "수행 절차(How to)를 정의" |
| **상태 관리** | **State File**을 통해 실제 리소스 매핑 (API 쿼리 최소화) | State가 없음. 매번 대상 서버에 접속하여 현재 상태 확인 후 변경 (Facts 수집) |
| **순서 의존성** | 자동 의존성 해결 (DAG) | 스크립트 작성 순서대로 실행 (Task 기반) |
| **주요 영역** | **프로비저닝 (Provisioning)** - 인프라 생성 | **구성 관리 (Configuration Management)** - OS/미들웨어 설정 |
| **멱등성 (Idempotency)** | State 기반 계산으로 완벽 보장 | 모듈 작성 시 개발자가 보장 로직 구현 필요 |

#### 2. 타 과목 융합 및 시너지 분석

**A. 클라우드 네이티브 & 컨테이너 오케스트레이션 (Kubernetes)**
테라폼은 **VM (Virtual Machine)**뿐만 아니라 **Kubernetes (K8s)** 리소스(Deployment, Service, Ingress)를 생성하는 데도 사용됩니다. 이를 **Infrastructure Provisioning** 단계에서 활용하며, 생성된 K8s 클러스터 위에 애플리케이션을 배포하는 **ArgoCD**와 같은 GitOps 툴과 연계됩니다.

**B. 버전 관리 시스템 (Git) 및 CI/CD (Jenkins/GitLab CI)**
IaC는 **Git**을 단순 저장소를 넘어 **'Single Source of Truth (유일한 진실의 원천)'**으로 활용합니다. `Pull Request`를 통해 인프라 변경 사항을 Peer Review(동료 검토)하는 과정에서 코드 품질을 보장합니다. 이를 통해 **DevSecOps**의 실현이 가능해지며, 변경 불가능한 인프라(**Immutable Infrastructure**) 패턴을 구현합니다.

**C. 네트워크 보안 (Security)**
테라폼 코드를 통해 **SG (Security Group)** 규칙을 코드화하면, 오타로 인한 방화벽 뚫림 사고를 방지할 수 있습니다. 또한, **TFLint**나 **TFSec**와 같은 정적 분석 도구를 **CI 파이프라인**에 탑재하여, `terraform apply` 전에 미리 보안 취약점(예: 공개된 S3 버킷, 0.0.0.0/0 Open)을 탐지할 수 있습니다.

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                  [ Modern DevOps Pipeline with IaC ]                          │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  (Developer)                       (Automation)                                │
│     │                                 │                                       │
│     ▼                                 ▼                                       │
│  [Git Push]                     [CI/CD Pipeline]                               │
│     │                                 │                                       │
│     │                         ┌──────┴──────┐                                 │
│     │                         │   TFSec     │ (Static Analysis)                │
│     │                         │ (Security Scan)│                               │
│     │                         └──────┬──────┘                                 │
│     │                                 │ (Pass)                                 │
│     ▼                                 ▼                                       │
│  [Merge]                     [Terraform Cloud]                                 │
│