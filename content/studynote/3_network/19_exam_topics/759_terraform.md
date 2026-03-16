+++
title = "Terraform - 테라폼"
weight = 759
+++

# Terraform - 테라폼

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선언적 인프라 정의
> 2. **가치**: 멀티클라우드, 상태 관리
> 3. **융합:** IaC, Cloud Providers, Modules

---

### Ⅰ. 개요 (Context & Background)

**개념 정의**

Terraform은 인프라를 코드로 정의합니다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Terraform                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │              Terraform 워크플로우                               │ │
│   │                                                              │ │
│   │   ┌─────────────────────────────────────────────────────┐   │ │
│   │   │                                                      │   │ │
│   │   │  Code (.tf):                                         │   │ │
│   │   │  resource "aws_instance" "web" {                    │   │ │
│   │   │    ami           = "ami-12345"                      │   │ │
│   │   │    instance_type = "t3.micro"                       │   │ │
│   │   │    tags = {                                         │   │ │
│   │   │      Name = "WebServer"                             │   │ │
│   │   │    }                                                │   │ │
│   │   │  }                                                  │   │ │
│   │   │                                                      │   │ │
│   │   │  Commands:                                           │   │ │
│   │   │  terraform init    → 초기화                          │   │ │
│   │   │  terraform plan    → 변경 계획                       │   │ │
│   │   │  terraform apply   → 적용                            │   │ │
│   │   │  terraform destroy → 삭제                            │   │ │
│   │   │                                                      │   │ │
│   │   │  State: terraform.tfstate                           │   │ │
│   │   │                                                      │   │ │
│   │   └─────────────────────────────────────────────────────┘   │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────────────┘
```

> **해설**: Terraform은 선언적으로 인프라를 관리합니다.

**📢 섹션 요약 비유:** Terraform = 인프라 설계도!

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**구성 요소 상세 분석**

| 항목 | 설명 |
|:---|:---|
| **Provider** | 제공자 |
| **Resource** | 리소스 |
| **Module** | 모듈 |
| **State** | 상태 |
| **Workspace** | 워크스페이스 |

**핵심 알고리즸:** 코드 → Plan → Apply → State

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

**지원 Provider**

| Provider | 설명 |
|:---|:---|
| **AWS** | 아마존 |
| **GCP** | 구글 |
| **Azure** | 마이크로소프트 |
| **Kubernetes** | K8s |
| **Generic** | 기타 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

**시나리오 1:** 멀티클라우드 → Terraform
**시나리오 2:** 재사용 → Modules
**시나리오 3:** 팀 협업 → Remote State

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

**참고 표준:** HCL (HashiCorp Configuration Language)

---

### 📌 관련 개념 링크**:
- [Infrastructure as Code](./750_iac.md)
- [GitOps](./751_gitops.md)
- [Cloud Providers](./xxx_cloud.md)
