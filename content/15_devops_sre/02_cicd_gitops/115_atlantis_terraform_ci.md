---
title: "Atlantis Terraform Ci"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 115
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Atlantis는 Terraform/OpenTofu의 <strong>PR(Pull Request) 기반 자동 Plan/Apply 워크플로</strong>를 제공하는 OSS 도구로, PR을 열면 자동으로 `terraform plan` 결과를 코멘트로 달고, 승인 후 `atlantis apply`로 적용한다.
> 2. **가치**: 개발자가 로컬에서 `terraform apply`를 실행하면 State 충돌·감사 불가·리뷰 없는 변경이 발생하지만, Atlantis는 <strong>모든 인프라 변경을 PR 리뷰 프로세스</strong>에 통합하여 IaC의 GitOps를 실현한다.
> 3. **판단 포인트**: Atlantis는 자체 호스팅(GitHub/GitLab Webhook 연동)이 필요하며, Terraform Cloud/Spacelift 같은 SaaS 대안과 비교하여 <strong>비용 0 + 완전 제어</strong>가 장점이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Atlantis PR 기반 워크플로                           |
+-------------------------------------------------------+
|  1. 개발자: main.tf 수정 -> PR 생성                   |
|  2. Atlantis Bot: 자동 terraform plan 실행            |
|     -> PR 코멘트에 Plan 결과 표시                      |
|     "1 to add, 0 to change, 0 to destroy"            |
|  3. 리뷰어: Plan 결과 확인 -> Approve                 |
|  4. 개발자: "atlantis apply" 코멘트                   |
|  5. Atlantis Bot: terraform apply 실행                |
|     -> 성공 결과 코멘트 + PR 머지                      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Atlantis는 인프라 변경의 <strong>4-eyes 원칙(이중 확인)</strong>을 자동화한 것이다. 혼자 몰래 서버를 바꿀 수 없고, 반드시 PR 리뷰를 거쳐야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Atlantis 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **Auto Plan** | PR 생성 시 자동 plan 실행 |
| <strong>PR Comment</strong> | Plan 결과를 PR 코멘트로 표시 |
| <strong>Locking</strong> | 동일 디렉터리 동시 변경 방지 |
| **Apply Require** | PR Approve 후에만 apply 허용 |
| **Custom Workflow** | pre-plan/post-apply 훅 지원 |

### Atlantis vs Terraform Cloud

| 비교 | Atlantis | Terraform Cloud |
|:---|:---|:---|
| **호스팅** | 자체 (Docker) | <strong>SaaS</strong> |
| **비용** | 무료 | 유료 |
| **제어** | **완전** | HashiCorp 의존 |
| <strong>State</strong> | 별도 관리 (S3) | 내장 |
| **Sentinel** | ✗ | ✅ (정책) |

- **📢 섹션 요약 비유**: Atlantis는 자가용(직접 관리, 비용 0)이고, Terraform Cloud는 택시(편리하지만 비용 있음)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 로컬 apply | Atlantis | Terraform Cloud |
|:---|:---|:---|:---|
| **리뷰** | 없음 | <strong>PR 필수</strong> | PR 필수 |
| <strong>감사</strong> | 불가 | **Git 이력** | 내장 |
| <strong>State 충돌</strong> | 빈번 | **Lock으로 방지** | 내장 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 배포 체크리스트
1. Atlantis 서버를 K8s/Docker에 배포.
2. GitHub/GitLab Webhook 연결.
3. `atlantis.yaml`에 프로젝트 디렉터리·워크플로 정의.
4. PR Approve -> `atlantis apply` 코멘트로 적용.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 로컬 apply | Atlantis | 개선 |
|:---|:---|:---|:---|
| 인프라 변경 감사 | 불가 | <strong>PR 이력</strong> | 100% |
| State 충돌 | 빈번 | <strong>Lock</strong> | 0건 |
| 비용 | - | **무료** | SaaS 대비 절감 |

Atlantis는 GitOps + Terraform의 가장 실용적인 조합이며, PR 리뷰 문화가 정착된 팀에서 인프라 거버넌스를 비용 없이 확보할 수 있는 최적의 도구다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Terraform</strong> | Atlantis가 자동화하는 IaC 도구 |
| <strong>GitOps</strong> | PR 기반 인프라 관리 = IaC GitOps |
| <strong>Terraform Cloud</strong> | SaaS 경쟁 도구 |
| **Spacelift** | 또 다른 Terraform CI SaaS 대안 |
| <strong>PR Review</strong> | Atlantis가 강제하는 변경 리뷰 프로세스 |

### 📈 관련 키워드 및 발전 흐름도

```text
[로컬 terraform apply (2014~) — 개인 실행, 감사 불가]
    |
    v
[Atlantis (2017, Hootsuite) — PR 기반 자동 Plan/Apply]
    |
    v
[Terraform Cloud (2019~) — HashiCorp SaaS]
    |
    v
[Spacelift / env0 (2020~) — IaC CI SaaS 경쟁]
    |
    v
[현재: Atlantis + OPA/Conftest — 정책 검증 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 레고(인프라)를 **혼자 몰래 바꿀 수** 있었어요 -> 실수해도 아무도 몰라요.
2. Atlantis는 레고를 바꾸기 전에 **친구(리뷰어)한테 보여주고** "이래도 될까?"라고 물어봐야 해요.
3. 친구가 "좋아!"라고 하면 로봇이 자동으로 바꿔주고, **기록도 다 남아서** 안전해요!
