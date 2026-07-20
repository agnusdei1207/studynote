---
title: "Argocd Gitops Cd"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
weight: 114
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Argo CD는 <strong>Git 레포지토리를 단일 진실 원천(Single Source of Truth)</strong>으로 삼아, Git의 매니페스트와 K8s 클러스터 상태를 <strong>실시간 비교(Diff)하고 자동 동기화(Sync)</strong>하는 CNCF 졸업 GitOps CD 도구다.
> 2. **가치**: 전통 CI/CD(Jenkins)가 "Push 기반(파이프라인이 클러스터에 적용)"이라면, Argo CD는 <strong>"Pull 기반(클러스터가 Git을 감시하여 스스로 동기화)"</strong>하므로, 클러스터 접근 권한을 CI 시스템에 노출하지 않아 <strong>보안이 강화</strong>된다.
> 3. **판단 포인트**: Argo CD는 K8s 매니페스트(YAML/Helm/Kustomize)를 관리하며, Argo Rollouts와 결합하여 <strong>카나리·블루/그린 배포를 선언적으로</strong> 수행한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Push 기반 CD vs Pull 기반 GitOps (Argo CD)         |
+-------------------------------------------------------+
|  [Push: Jenkins]                                      |
|   개발자 -> Git Push -> Jenkins -> kubectl apply -> K8s  |
|   Jenkins에 클러스터 kubeconfig 필요 (보안 위험)      |
|                                                       |
|  [Pull: Argo CD]                                      |
|   개발자 -> Git Push -> (끝)                            |
|   Argo CD (클러스터 내부) -> Git 감시 -> 자동 Sync     |
|   Jenkins에 클러스터 권한 불필요 (보안 강화)          |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Push CD는 택배(Jenkins)가 집까지 직접 배달하는 것이고, Pull CD(Argo CD)는 집 앞 우편함(Git)에 넣으면 집주인(클러스터)이 스스로 가져가는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Argo CD 핵심 개념

| 개념 | 설명 |
|:---|:---|
| **Application** | Git 레포 경로 + 타겟 클러스터/네임스페이스 매핑 |
| **Sync** | Git 상태 -> K8s 클러스터 적용 |
| **Diff** | Git vs 클러스터 상태 차이 감지 |
| **Health** | Pod/Deployment 건강 상태 모니터링 |
| **Prune** | Git에서 삭제된 리소스를 클러스터에서도 삭제 |

### 지원 매니페스트 형식
- **Plain YAML**, <strong>Helm Chart</strong>, <strong>Kustomize</strong>, **Jsonnet**

- **📢 섹션 요약 비유**: Argo CD는 냉장고(클러스터)와 장보기 목록(Git)을 항상 일치시키는 AI 비서다. 목록에서 우유를 지우면 냉장고에서도 우유를 꺼낸다(Prune).

---

## Ⅲ. 비교 및 연결

| 비교 | Jenkins CD | Argo CD | Flux |
|:---|:---|:---|:---|
| **방식** | Push | <strong>Pull (GitOps)</strong> | Pull (GitOps) |
| **보안** | CI에 클러스터 권한 | **클러스터 내부** | 클러스터 내부 |
| **UI** | Jenkins 대시보드 | <strong>리소스 트리 시각화</strong> | CLI 중심 |
| <strong>CNCF</strong> | - | **Graduated** | Graduated |

---

## Ⅳ. 실무 적용 및 실무자 판단

### 도입 체크리스트
1. **Git 레포 분리**: 앱 코드 레포 + 매니페스트 레포 분리 (Config Repo 패턴).
2. <strong>RBAC</strong>: Argo CD 프로젝트별 접근 제어.
3. **Argo Rollouts**: 카나리·블루/그린 배포 선언적 관리.

### 안티패턴
- <strong>kubectl apply 수동 실행 병행</strong>: Git과 클러스터 상태 불일치 -> GitOps 원칙 파괴.

---

## Ⅴ. 기대효과 및 결론

| 지표 | Jenkins CD | Argo CD | 개선 |
|:---|:---|:---|:---|
| 클러스터 권한 노출 | CI에 kubeconfig | **클러스터 내부만** | 보안 강화 |
| 상태 드리프트 감지 | 불가 | **실시간 Diff** | 즉시 감지 |
| 롤백 | 파이프라인 재실행 | **Git Revert -> 자동 Sync** | 30초 |

Argo CD는 멀티클러스터 GitOps·Argo Workflows(CI) 통합으로 <strong>CI/CD 전체를 GitOps 패러다임</strong>으로 통합하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>GitOps</strong> | Argo CD가 구현하는 배포 패러다임 |
| **Argo Rollouts** | 카나리·블루/그린 배포 확장 |
| **Flux** | 경쟁 GitOps CD 도구 (CNCF) |
| <strong>Helm / Kustomize</strong> | Argo CD가 지원하는 매니페스트 형식 |
| <strong>Config Repo 패턴</strong> | 앱 코드와 매니페스트 레포 분리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Jenkins CD (2010s) — Push 기반 파이프라인 배포]
    |
    v
[GitOps 개념 (2017, Weaveworks) — Git = 단일 진실 원천]
    |
    v
[Argo CD v1 (2018) — K8s Pull 기반 CD]
    |
    v
[CNCF Graduated (2022) — 생태계 표준화]
    |
    v
[현재: Argo CD + Argo Workflows — CI/CD 전체 GitOps 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 택배 아저씨(Jenkins)가 집까지 와서 직접 물건을 놓아줬어요.
2. Argo CD는 **우편함(Git)에 넣으면 집주인(클러스터)이 알아서 가져가는** 시스템이에요.
3. 택배 아저씨에게 **집 열쇠를 안 줘도 돼서** 더 안전하고, 물건이 잘못 왔으면 **우편함만 바꾸면** 돼요!
