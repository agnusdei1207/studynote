---
title: "Compliance As Code"
date: "2026-04-05"
tags:
  - "studynote-it-management"
weight: 48
---
> **핵심 인사이트**
> 1. Compliance as Code(컴플라이언스 애즈 코드)는 규정 준수 정책을 코드로 표현하여 자동화된 검사와 집행을 실현 — 감사자가 수동으로 확인하는 전통 컴플라이언스 대신, 인프라 변경 시마다 코드로 정의된 정책을 자동 검사하여 지속적 규정 준수를 보장한다.
> 2. Policy as Code와 Infrastructure as Code의 교차점 — IaC로 인프라를 코드화하면 자연스럽게 정책도 코드로 표현 가능해지며, Open Policy Agent(OPA)·AWS Config Rules·Azure Policy 등이 이 패러다임을 구현한다.
> 3. Shift-Left Compliance의 핵심 가치 — 운영 중 감사 발견에서 개발/배포 단계로 컴플라이언스 검사 시점을 당기면, 비용과 시간이 100배 이상 절감되고 개발 속도도 저해되지 않는다.

---

## Ⅰ. Compliance as Code 개요

```
전통 컴플라이언스 vs Compliance as Code:

전통 방식:
  1. 정책 문서 작성 (Word/PDF)
  2. IT 팀에 이메일로 전달
  3. 구성 변경 후 수동 검토
  4. 분기/연간 감사

  문제:
  감사 준비 = 2~4주 수작업
  감사 주기 사이 위반 지속
  인적 오류 (체크리스트 누락)
  클라우드 변경 속도를 따라가지 못함

Compliance as Code:
  정책 -> 코드화 -> CI/CD 파이프라인 통합
  인프라 변경 -> 자동 정책 검사 -> 위반 즉시 차단/알림

  도구:
  OPA (Open Policy Agent): 범용 정책 엔진
  AWS Config Rules: AWS 자원 규정 준수
  Azure Policy: Azure 자원 정책
  Terraform Sentinel: IaC 정책 게이트
  Chef InSpec: 인프라 규정 준수 테스트

핵심 원칙:
  Policy as Code:
  정책 -> Git 저장소 관리 (버전 관리, 변경 추적)
  검토/승인 -> PR 프로세스

  Continuous Compliance:
  매 커밋/배포 시 정책 자동 검사
  "컴플라이언스 = 코드 빌드 테스트와 동일 레벨"
```

> 📢 **섹션 요약 비유**: Compliance as Code = 자동 신호등 — 전통(교통 경찰이 주기적으로 점검). CaC(신호 위반 시 즉시 카메라로 탐지+통보). 속도 위반 없이 실시간 집행!

---

## Ⅱ. OPA (Open Policy Agent)

```
OPA (Open Policy Agent):
  CNCF 프로젝트 (Cloud Native Computing Foundation)
  범용 정책 엔진

  언어: Rego (OPA 전용 정책 언어)
  용도: Kubernetes, API, IaC 정책

Rego 정책 예시:

1. Kubernetes Pod 보안 정책:
  package kubernetes.admission

  deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := sprintf("특권 컨테이너 허용 안 됨: %v", [container.name])
  }

  -> 특권 컨테이너 배포 시 자동 거부

2. Terraform IaC 정책 (S3 퍼블릭 차단):
  package terraform

  deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    resource.change.after.acl == "public-read"
    msg := "S3 버킷 공개 읽기 허용 금지"
  }

  -> terraform plan 시 정책 검사 -> 위반 차단

3. API 접근 정책:
  package authz

  allow {
    input.method == "GET"
    input.user.role == "admin"
  }
  allow {
    input.method == "GET"
    input.path == ["public", "api"]
  }

  -> API 게이트웨이에서 OPA로 권한 검사

OPA 통합 포인트:
  Kubernetes: OPA Gatekeeper (Admission Controller)
  CI/CD: Conftest (Terraform/YAML 정책 검사)
  API 게이트웨이: Envoy + OPA
```

> 📢 **섹션 요약 비유**: OPA = 법전 코드화 — "특권 컨테이너 금지(법)"를 Rego 코드로. 컨테이너 배포 시 자동으로 법전 검사. 위반 즉시 거부. 감사관 없이도 24×7 법 집행!

---

## Ⅲ. AWS Config + Security Hub

```
AWS Config:
  AWS 자원 구성 변경 추적 + 정책 준수 검사

  동작:
  1. 자원 변경 발생 (EC2, S3, IAM...)
  2. AWS Config가 변경 기록 (Configuration Item)
  3. Config Rules 자동 평가
  4. 위반 -> AWS Security Hub로 전달

AWS Config Rules 예시:

  s3-bucket-public-read-prohibited:
  S3 버킷 퍼블릭 읽기 -> NON_COMPLIANT

  ec2-instance-no-public-ip:
  EC2에 퍼블릭 IP -> NON_COMPLIANT

  iam-password-policy:
  IAM 비밀번호 정책 최소 길이 14자 미만 -> NON_COMPLIANT

  root-account-mfa-enabled:
  루트 계정 MFA 비활성화 -> NON_COMPLIANT

AWS Security Hub:
  여러 AWS 서비스 보안 결과 통합
  표준 준수 점수 자동 계산:

  CIS AWS Foundations Benchmark
  AWS Foundational Security Best Practices
  PCI DSS v3.2.1

  점수 예:
  CIS Level 1: 67% 준수
  -> 무엇을 고쳐야 100%?
  -> 우선순위별 수정 가이드

자동 교정 (Auto Remediation):
  Config Rule 위반 -> Lambda 자동 실행 -> 수정

  예:
  S3 퍼블릭 -> Lambda가 ACL을 private으로 변경
  IAM 비밀번호 정책 위반 -> 자동 정책 업데이트
```

> 📢 **섹션 요약 비유**: AWS Config = 자동 건물 점검 로봇 — S3 문(버킷) 열렸나 매초 감시. 열리면 즉시 닫음(자동 교정) + 관리자 알림. 24×7 자동 규정 준수!

---

## Ⅳ. Terraform Sentinel

```
Terraform Sentinel:
  HashiCorp의 Policy as Code 프레임워크
  IaC 배포 전 정책 검사 (Shift-Left!)

정책 적용 단계:
  terraform plan -> Sentinel 정책 검사 -> terraform apply

  정책 위반 시: apply 차단 (Advisory / Soft-Mandatory / Mandatory)

Sentinel 정책 예시:

1. 태그 필수 정책:
  import "tfplan/v2" as tfplan

  required_tags = ["environment", "owner", "cost-center"]

  resources = tfplan.find_resources("aws_instance")

  check_tags = rule {
    all resources as _, rc {
      all required_tags as tag {
        rc.change.after.tags contains tag
      }
    }
  }

  main = rule { check_tags }

  -> 태그 없는 EC2 배포 차단

2. 인스턴스 유형 제한:
  allowed_types = ["t3.micro", "t3.small", "t3.medium"]

  check_type = rule {
    all resources as _, rc {
      rc.change.after.instance_type in allowed_types
    }
  }

  -> 프로덕션 제외 환경에서 큰 인스턴스 배포 차단

정책 단계:
  Advisory: 경고만 (배포는 진행)
  Soft-Mandatory: 강제 + 권한자 override 가능
  Mandatory: 절대 차단

Conftest (오픈소스 대안):
  Terraform, Kubernetes YAML, Helm에 OPA Rego 정책 적용
  Terraform Cloud 없이도 사용 가능
```

> 📢 **섹션 요약 비유**: Terraform Sentinel = 공사 착공 전 허가 — 설계도(Terraform plan) 제출 시 법규 자동 검사. 태그 없음(필수 서류 미비) -> 착공 불허. 공사 중 문제가 아닌 착공 전 예방!

---

## Ⅴ. 실무 시나리오 — 금융사 CaC 구축

```
핀테크 스타트업 -> 금융감독원 규제 준수 CaC:

배경:
  AWS 기반 서비스
  규제: 전자금융감독규정, 클라우드 이용 기준

  감사 준비: 분기마다 2주 수작업
  개발팀 위반 반복: S3 퍼블릭, IAM 과잉 권한

CaC 구축:

1. 정책 코드화 (OPA + AWS Config):
  전자금융감독규정 주요 항목 -> Rego + Config Rules

  정책 목록 (50개):
  - S3 암호화 필수 (AES-256)
  - RDS 암호화 필수
  - 퍼블릭 S3 버킷 금지
  - EC2 공개 접근 금지 (특수 경우 제외)
  - 로그 보존 1년 이상
  - MFA 전 IAM 사용자 적용
  - ...

2. CI/CD 통합:
  Terraform 변경 -> Sentinel 정책 자동 검사
  Kubernetes 배포 -> OPA Gatekeeper 검사

  PR 단계에서 정책 위반 즉시 피드백:
  "🚫 S3 버킷에 암호화 누락 (규정 제28조)"
  "✅ 8개 정책 통과"

3. 실시간 대시보드:
  AWS Security Hub -> Grafana 대시보드
  준수율 실시간 표시 (목표: 98%+)
  위반 항목 드릴다운 가능

결과 (3개월):
  감사 준비 시간: 2주 -> 1일 (대시보드 리포트 출력)
  반복 위반: 월 25건 -> 2건 (자동 차단)
  개발팀 체감: "배포할 때 미리 알려줘서 좋음"

  규제 감사 결과:
  "컴플라이언스 자동화 우수 사례" 인정
  지적 사항: 3건 -> 0건
```

> 📢 **섹션 요약 비유**: 핀테크 CaC = 자동 규정 준수 비서 — 코드 배포 시 규정집 자동 대조, 위반 즉시 차단, 대시보드로 실시간 점수. 감사 준비 2주 -> 1일. 개발자도 "미리 알려줘서 좋아요"!

---

## 📌 관련 개념 맵

```
Compliance as Code
+-- 핵심 도구
|   +-- OPA (Rego 정책)
|   +-- AWS Config Rules
|   +-- Terraform Sentinel
|   +-- Conftest
+-- 통합 포인트
|   +-- CI/CD 파이프라인
|   +-- Kubernetes Admission
|   +-- IaC (Terraform)
+-- 표준 프레임워크
|   +-- CIS Benchmark
|   +-- PCI DSS
|   +-- 전자금융감독규정
+-- 원칙
    +-- Policy as Code
    +-- Shift-Left Compliance
    +-- Continuous Compliance
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 수동 감사 (2000s)]
체크리스트 기반
연간/분기 점검
      |
      v
[IaC 등장 (Terraform, 2014)]
인프라 코드화
정책 코드화 가능성
      |
      v
[OPA 오픈소스 (2016)]
범용 정책 엔진
Kubernetes Gatekeeper
      |
      v
[DevSecOps (2018~)]
보안+컴플라이언스를 CI/CD로
Shift-Left 보안
      |
      v
[현재: AI 컴플라이언스]
LLM 기반 정책 생성
자동 규제 해석
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. Compliance as Code = 자동 신호등 — 전통(경찰관 주기 점검) vs CaC(카메라 24시간 감시 + 위반 즉시 통보). 실시간 규정 준수!
2. OPA Rego = 법전 코드화 — "특권 컨테이너 금지"를 코드로. 배포 시 자동 법전 검사. 위반 즉시 거부!
3. Shift-Left Compliance = 출발 전 점검 — 운영 중 발견(100배 비용) 대신 배포 전 CI에서 발견(1 비용). 미리 고치면 싸요!
