---
title: "Gitops Single Source Of Truth"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 119
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GitOps는 <strong>Git 리포지토리를 인프라·애플리케이션의 단일 진실 원천(Single Source of Truth)</strong>으로 삼고, Git에 선언된 상태와 실제 클러스터 상태를 <strong>자동으로 동기화(Reconciliation)</strong>하는 운영 패러다임이다.
> 2. **가치**: 수동 `kubectl apply`·콘솔 조작은 변경 이력이 없고 리뷰가 불가능하지만, GitOps는 <strong>모든 변경이 PR->리뷰->머지->자동 적용</strong> 흐름을 따르므로 감사 가능성·재현성·롤백이 보장된다.
> 3. **판단 포인트**: <strong>Push 방식(CI가 kubectl push)</strong> vs <strong>Pull 방식(ArgoCD/Flux가 Git을 감시)</strong>을 구분하고, Pull 방식이 보안(클러스터 외부에 kubectl 크레덴셜 불필요)에서 우수하다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    GitOps Pull 방식 워크플로                           |
+-------------------------------------------------------+
|  1. 개발자: Git에 K8s manifest 수정 -> PR              |
|  2. 리뷰어: 변경 확인 -> Approve -> 머지               |
|  3. ArgoCD/Flux: Git 변경 감지 (Pull)                |
|  4. 자동 Reconcile: 클러스터 상태 <- Git 선언 상태    |
|  5. 드리프트 발생 시: 자동 복원 (Self-healing)        |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: GitOps는 내비게이션(Git)이 목적지(선언 상태)를 설정하면, 자율주행차(ArgoCD)가 알아서 경로를 따라가고, 이탈(드리프트)하면 자동으로 복귀하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Push vs Pull 방식

| 비교 | Push (CI->kubectl) | Pull (ArgoCD/Flux) |
|:---|:---|:---|
| **보안** | CI에 kubeconfig 필요 | **클러스터 내부에서 Pull** |
| **Self-healing** | 없음 | **드리프트 자동 복원** |
| **대표** | Jenkins+kubectl | **ArgoCD, Flux** |

### GitOps 4대 원칙 (OpenGitOps)
1. **선언적**: YAML/HCL로 원하는 상태 선언.
2. <strong>버전 관리</strong>: Git에 모든 이력 보존.
3. **자동 적용**: 머지 시 자동 배포.
4. **지속 조정**: 드리프트 시 자동 복원.

- **📢 섹션 요약 비유**: GitOps는 "Git에 쓰인 대로 세상이 돌아가야 한다"는 헌법이다. 현실(클러스터)이 헌법(Git)과 다르면 자동으로 바로잡는다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수동 운영 | CI/CD | GitOps |
|:---|:---|:---|:---|
| **변경 추적** | 없음 | 일부 | **Git 100%** |
| <strong>롤백</strong> | 수동 | 파이프라인 | **git revert** |
| **드리프트** | 방치 | 방치 | **자동 복원** |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 리포지토리 구조
- **App Repo**: 소스코드 + Dockerfile.
- <strong>Config Repo</strong>: K8s manifests (GitOps 대상).
- CI가 App Repo 빌드 -> Config Repo의 이미지 태그 업데이트 -> ArgoCD 자동 배포.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 | GitOps | 개선 |
|:---|:---|:---|:---|
| 감사 추적 | 불가 | **Git 이력** | 100% |
| 롤백 | 분 단위 | **git revert (초)** | 즉시 |
| 드리프트 | 방치 | **자동 복원** | 제로 |

GitOps는 <strong>클라우드 네이티브 운영의 사실상 표준</strong>이며, ArgoCD가 CNCF Graduated 프로젝트로 채택되어 생태계가 안정적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ArgoCD** | GitOps Pull 방식의 대표 도구 |
| **Flux** | CNCF GitOps 도구 (경량) |
| **Reconciliation** | Git ↔ 클러스터 상태 동기화 |
| **드리프트 감지** | GitOps의 Self-healing 메커니즘 |
| <strong>IaC</strong> | Terraform+GitOps = 인프라 GitOps |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 kubectl apply (2014~)]
    |
    v
[CI/CD Push 방식 (Jenkins+kubectl, 2016~)]
    |
    v
[GitOps 개념 (Weaveworks, 2017) — Pull 방식 제안]
    |
    v
[ArgoCD / Flux (2019~) — CNCF 채택]
    |
    v
[현재: OpenGitOps 표준 — 4대 원칙 정립]
```

### 👶 어린이를 위한 3줄 비유 설명
1. GitOps는 <strong>설계도(Git)</strong>를 바꾸면 로봇이 알아서 건물(클러스터)을 **자동으로 고치는** 시스템이에요.
2. 누군가 몰래 건물을 바꾸면(드리프트), 로봇이 설계도를 보고 **원래대로 되돌려놔요**.
3. 설계도 변경은 반드시 <strong>선생님(리뷰어) 승인</strong>을 받아야 해서 안전하답니다!
