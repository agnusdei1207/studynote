---
title: "IaC Terraform Immutable Infrastructure"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 504
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IaC(Infrastructure as Code)는 인프라 구성을 코드로 선언하여 버전 관리, 재현성, 자동화를 확보하는 방법론이며, Terraform은 그 사실상 표준 도구다.
> 2. **가치**: 불변 인프라(Immutable Infrastructure)는 서버를 수정하는 대신 새 이미지로 교체하여 구성 편류(Configuration Drift)를 근본적으로 차단한다.
> 3. **판단 포인트**: GitOps 파이프라인에서 인프라 변경도 PR/코드 리뷰를 거치게 하면, 감사 추적(Audit Trail)과 협업이 동시에 실현된다.

---

## Ⅰ. 개요 및 필요성

전통적인 인프라 관리는 담당자가 수동으로 서버에 접속하여 설정을 변경하는 방식이었다. 이 방식은 시간이 지남에 따라 서버마다 설정이 달라지는 <strong>구성 편류(Configuration Drift)</strong> 문제를 유발한다. 어느 서버는 Apache 2.4.29, 다른 서버는 2.4.41이 설치되어 있는 식이다.

**IaC가 해결하는 문제**:
- 재현성: 동일한 코드로 동일한 환경을 몇 번이든 재생성
- 버전 관리: 인프라 변경 이력이 Git으로 추적됨
- 협업: 코드 리뷰를 통한 인프라 변경 검토
- 자동화: CI/CD 파이프라인에서 인프라 배포까지 자동화

- **📢 섹션 요약 비유**: IaC 없는 서버 관리는 레시피 없이 요리하는 것이다 — 매번 조금씩 달라지고, 담당자가 바뀌면 아무도 재현할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong>Terraform(HCL) Plan-Apply 워크플로</strong>:

```
+-------------------------------------------------------------+
|                    GitOps + Terraform 흐름                   |
|                                                             |
|  개발자 -> PR(HCL 변경) -> 코드 리뷰 -> merge                  |
|                                    v                        |
|             terraform plan  (변경 사항 미리 보기)             |
|                    v        (diff: +3 리소스, -1 리소스)      |
|             terraform apply (실제 적용, State 파일 갱신)      |
|                    v                                        |
|             State 파일 (terraform.tfstate, S3 원격 저장)      |
+-------------------------------------------------------------+
```

| 도구 | 방식 | 특징 | 주요 사용 |
|:---|:---:|:---|:---|
| Terraform | 선언적 | HCL, State 관리, 멀티 클라우드 | 인프라 프로비저닝 |
| Ansible | 절차적 | YAML 플레이북, 에이전트리스 | 서버 구성 관리 |
| Pulumi | 선언적 | 일반 프로그래밍 언어(Python/TS) | 개발자 친화적 IaC |
| CloudFormation | 선언적 | AWS 전용, JSON/YAML | AWS 네이티브 관리 |

<strong>불변 인프라(Immutable Infrastructure) vs 가변 인프라(Mutable Infrastructure)</strong>:
- <strong>가변 인프라</strong>: 서버를 멈추지 않고 설정 변경 -> 시간이 지나면 Configuration Drift 발생
- <strong>불변 인프라</strong>: 변경이 필요하면 새 이미지를 만들어 기존 서버를 교체 -> 항상 동일한 상태 보장

불변 인프라는 도커 이미지 + Terraform의 조합으로 구현된다: 코드 변경 -> CI 파이프라인 -> 새 Docker 이미지 빌드 -> Terraform으로 새 EC2/ECS 인스턴스 배포 -> 구 인스턴스 종료.

- **📢 섹션 요약 비유**: 불변 인프라는 스마트폰 OS 업데이트와 같다 — 기존 파일을 수정하지 않고 새 버전 전체를 설치하기 때문에, 업데이트 전과 후의 상태가 항상 명확히 다르다.

---

## Ⅲ. 비교 및 연결

<strong>Terraform 모듈(Module)</strong>: 반복 사용하는 인프라 패턴을 재사용 가능한 코드 블록으로 캡슐화. 예: VPC 모듈, EKS 클러스터 모듈. Terraform Registry에서 공개 모듈 활용 가능.

<strong>State 파일 관리</strong>: `terraform.tfstate`에 현재 인프라 상태 기록. 팀 협업 시 S3 + DynamoDB(잠금)로 원격 State 저장 필수. State 파일에 비밀 값이 포함될 수 있으므로 암호화 필수.

<strong>GitOps</strong>: 인프라와 애플리케이션 설정을 모두 Git에서 관리하고, 자동화된 시스템이 실제 상태를 Git 상태와 일치시킨다. ArgoCD(앱), Flux(인프라), Atlantis(Terraform PR 자동화).

- **📢 섹션 요약 비유**: Terraform State 파일은 인프라의 주민등록증 보관함이다. 여기가 털리거나 분실되면 인프라의 "공식 현황"을 잃어버린다.

---

## Ⅳ. 실무 적용 및 실무자 판단

**심화 학습 판단 포인트**:
1. 선언적(Declarative) vs 절차적(Procedural) IaC의 차이를 Terraform vs Ansible로 대비 설명한다.
2. 불변 인프라 구현 흐름(이미지 빌드 -> 배포 -> 구 인스턴스 교체)을 순서대로 기술한다.
3. State 파일의 역할과 원격 저장 필요성(팀 협업, 잠금)을 보안 관점에서 언급한다.

**실무 시나리오**: 마이크로서비스 50개를 운영하는 기업이 서버 구성 편류 문제로 장애를 반복 경험. 해결책: 모든 서비스를 Docker 이미지화 + Terraform으로 EKS 클러스터 프로비저닝 + Atlantis로 PR 기반 인프라 변경 승인 -> 장애 원인의 60%를 차지하던 "환경 차이" 문제 해소.

- **📢 섹션 요약 비유**: GitOps는 인프라도 코드처럼 관리하는 방식이다. 회계 장부(State)를 혼자 관리하면 실수가 나지만, 팀 리뷰(PR 승인)를 거치면 오류가 줄어든다.

---

## Ⅴ. 기대효과 및 결론

IaC와 불변 인프라를 도입하면:
- **재현성 100%**: 동일 코드 -> 동일 환경, 재난 복구 시 수 분 내 인프라 재생성
- <strong>Configuration Drift 제거</strong>: 불변 이미지 교체로 서버 상태 항상 일관성 유지
- <strong>감사 추적</strong>: Git 커밋 이력이 인프라 변경 내역의 완전한 감사 로그
- **팀 협업**: PR/코드 리뷰로 보안 검토와 지식 공유 자동화

IaC는 단순한 도구가 아니라 <strong>인프라 관리의 패러다임 전환</strong>이며, 클라우드 네이티브 운영의 필수 전제 조건이다.

- **📢 섹션 요약 비유**: IaC는 건축 설계도다. 설계도 없이 지은 건물은 수리할 때마다 벽을 뜯어봐야 하지만, 설계도가 있으면 어디를 어떻게 바꿔야 하는지 즉시 알 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 멀티 클라우드 (Multi-Cloud) | Terraform, 이식성, 벤더 독립 · 500 |
| 불변 인프라 (Immutable Infrastructure) | 도커 이미지, Configuration Drift · 501 |
| GitOps | ArgoCD, Atlantis, PR 기반 인프라 · 502 |
| Ansible | 절차적 IaC, 플레이북, 에이전트리스 · 540 |
| CI/CD (지속적 통합/배포) | 파이프라인, 빌드, 배포 자동화 · 505 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Terraform · 이식성] -> [IaC 테라폼과 불변 인프라 선언] -> [파이프라인 · 빌드]
```

### 👶 어린이를 위한 3줄 비유 설명

1. IaC는 서버 설치 설명서를 코드로 쓰는 것이에요 — 설명서만 있으면 똑같은 서버를 언제든 다시 만들 수 있어요.
2. 불변 인프라는 낡은 장난감을 고치는 대신 새 것으로 교환하는 것처럼, 서버도 수리 대신 새 것으로 바꿔요.
3. GitOps는 인프라 변경도 숙제처럼 선생님(팀원)한테 검사를 받아야 적용되는 방식이에요.
