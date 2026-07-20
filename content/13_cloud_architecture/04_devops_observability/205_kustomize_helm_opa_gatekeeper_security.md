---
title: "Kustomize Helm Opa Gatekeeper Security"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
weight: 205
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Policy as Code는 보안·운영 정책을 사람이 읽는 문서가 아닌 코드로 표현하여 자동화 파이프라인에서 강제 검증하는 패턴이며, OPA Gatekeeper는 K8s Admission Controller로 이를 구현한다.
> 2. **가치**: Helm/Kustomize 템플릿의 `image: latest` 사용 금지, CPU/메모리 제한 미설정 Pod 차단 같은 규칙을 코드로 정의하면, 잘못된 리소스가 클러스터에 배포되는 것 자체를 원천 차단한다.
> 3. **판단 포인트**: OPA Gatekeeper는 강력하지만 Rego 언어 학습 곡선이 높다. YAML 기반의 Kyverno가 학습 비용이 낮아 소규모 팀에 적합하며, 두 도구의 트레이드오프를 상황에 맞게 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

K8s 클러스터에 수백 개의 팀이 리소스를 배포하면, 표준을 지키지 않는 YAML이 반드시 등장한다: `image: latest` 사용으로 버전 추적 불가, CPU/메모리 제한 없어 노드 고갈, 루트 컨테이너 실행, 비표준 이미지 레지스트리 사용 등. 코드 리뷰만으로는 이를 100% 막기 어렵다.

Policy as Code(PaC)는 이 문제를 자동화로 해결한다. 정책을 코드로 표현하여 CI/CD 파이프라인과 K8s Admission Controller에 통합하면, 위반 리소스는 파이프라인 단계에서 거부되거나 클러스터 진입 자체가 차단된다. 이것이 DevSecOps의 핵심 실천 방법이다.

OPA(Open Policy Agent)는 CNCF 졸업 프로젝트로, 클라우드 네이티브 환경의 범용 정책 엔진이다. K8s 통합을 위한 OPA Gatekeeper와 함께 사용하면 K8s 리소스에 대한 모든 커스텀 정책을 코드로 정의하고 실시간으로 강제할 수 있다.

📢 **섹션 요약 비유**: Policy as Code는 건설 현장의 자동화된 품질 검사 기계와 같다. 인부(개발자)가 자재(YAML)를 가져올 때마다 기계가 자동으로 "규격에 맞는지" 검사하고, 맞지 않으면 현장에 반입 자체를 거부한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### OPA Gatekeeper 동작 구조

```
  개발자/CI 파이프라인이 K8s API에 리소스 생성 요청
           |
           v
  +-------------------------------------------------+
  |           K8s API Server                         |
  |                                                  |
  |  +--------------------------------------------+ |
  |  |     Admission Controller (Webhook)          | |
  |  |                                             | |
  |  |   ValidationAdmission -> OPA Gatekeeper      | |
  |  |   MutatingAdmission   -> (기본값 주입 등)    | |
  |  +--------------------------------------------+ |
  +--------------------------+----------------------+
                             |
                             v
  +-------------------------------------------------+
  |             OPA Gatekeeper                       |
  |                                                  |
  |  ConstraintTemplate: Rego 언어로 정책 정의        |
  |  Constraint: 정책 적용 범위·파라미터 설정          |
  |                                                  |
  |  정책 검증:                                       |
  |    Pass -> 리소스 생성 허용                        |
  |    Fail -> 리소스 생성 거부 + 에러 메시지           |
  +-------------------------------------------------+
```

### ConstraintTemplate (Rego 정책 정의)

```yaml
# 예: image:latest 금지 정책
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8snolatestimage
spec:
  crd:
    spec:
      names:
        kind: K8sNoLatestImage
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8snolatestimage

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          endswith(container.image, ":latest")
          msg := sprintf("Container '%v'은 ':latest' 태그 사용 금지. 명시적 버전을 사용하세요.", [container.name])
        }
```

### Constraint (정책 적용)

```yaml
# 정책을 특정 네임스페이스에 적용
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sNoLatestImage
metadata:
  name: no-latest-image
spec:
  enforcementAction: deny     # deny / warn / dryrun
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces:
      - production
      - staging
```

📢 **섹션 요약 비유**: ConstraintTemplate은 법령(Rego로 작성된 규칙), Constraint는 그 법령을 어떤 지역(네임스페이스)에 적용할지 지정하는 지방 조례다. 같은 법령을 여러 지역에 다른 조건으로 적용할 수 있다.

---

## Ⅲ. 비교 및 연결

### 주요 Policy 규칙 예시

| 정책 | 설명 |
|:---|:---|
| image:latest 금지 | 이미지 버전 명시 강제 -> 버전 추적 가능 |
| CPU/Memory 제한 강제 | resources.limits 미설정 Pod 차단 |
| 비표준 레지스트리 금지 | 승인된 레지스트리만 사용 허용 |
| runAsRoot 금지 | 루트 컨테이너 실행 차단 (PSA와 중복 강화) |
| 레이블 강제 | team, env 레이블 없는 리소스 거부 |
| Ingress HTTPS 강제 | HTTP 인그레스 생성 금지 |

### OPA Gatekeeper vs Kyverno

| 항목 | OPA Gatekeeper | Kyverno |
|:---|:---|:---|
| 정책 언어 | Rego (전용 언어, 학습 곡선 높음) | YAML (K8s 네이티브, 직관적) |
| 학습 비용 | 높음 | 낮음 |
| 유연성 | 매우 높음 | 높음 |
| 뮤테이션 지원 | 별도 설정 | ✅ 내장 |
| CNCF 상태 | 졸업 | 인큐베이팅 |
| 적합 팀 | 대규모, 복잡한 정책 | 중소규모, 빠른 구축 |

📢 **섹션 요약 비유**: OPA Gatekeeper가 C언어처럼 강력하지만 어렵다면, Kyverno는 Python처럼 배우기 쉽고 빠르게 쓸 수 있다. 복잡한 시스템에는 C가, 빠른 프로토타입에는 Python이 맞듯이 상황에 따라 선택한다.

---

## Ⅳ. 실무 적용 및 실무자 판단

<strong>CI/CD 파이프라인 통합 (Shift Left)</strong>:
```yaml
# GitHub Actions: PR 단계에서 OPA 정책 검증
jobs:
  policy-check:
    steps:
    - name: Conftest로 정책 검증
      uses: instrumenta/conftest-action@main
      with:
        files: kubernetes/
        policy: policy/

    # conftest는 OPA/Rego 정책을 CI에서 실행하는 도구
    # 클러스터 없이 로컬/CI에서 YAML 정책 검증 가능
```

<strong>Kyverno 정책 예시 (YAML 기반)</strong>:
```yaml
# image:latest 금지 (Kyverno)
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-image-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "이미지는 반드시 명시적 태그를 사용해야 합니다 (latest 금지)"
      pattern:
        spec:
          containers:
          - image: "!*:latest"
```

**실무자 판단 포인트**:
- Policy as Code의 핵심 가치: "정책이 문서가 아닌 코드로 존재하면 자동화 검증이 가능하고 항상 최신 상태를 유지한다."
- dryrun -> warn -> deny 순서로 단계적으로 enforcementAction을 강화하여 기존 워크로드 영향을 최소화한다.
- 정책 위반 알림을 개발자에게 즉시 전달하는 Slack/PagerDuty 연동이 UX 관점에서 중요하다.

📢 **섹션 요약 비유**: Policy as Code는 교통법규를 사람 경찰관이 단속하는 것이 아니라 자동 카메라로 24시간 단속하는 것과 같다. 사람이 없어도 항상 규칙이 적용되고, 위반 즉시 통보된다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 정책 일관성 보장 | 수작업 리뷰 의존 없이 모든 배포에 정책 자동 적용 |
| Shift Left 보안 | CI 단계에서 정책 위반 조기 발견 |
| 감사 용이성 | 정책 코드가 곧 감사 증적 |
| 지식 공유 | 정책이 코드로 명확히 표현되어 조직 표준 전파 용이 |

Policy as Code는 DevSecOps의 핵심 실천이다. "보안은 전문 팀의 일"이라는 사일로를 제거하고, 보안 정책이 CI/CD 파이프라인에 내재화됨으로써 "기본이 안전한(Secure by Default)" 인프라를 실현한다.

📢 **섹션 요약 비유**: Policy as Code 없이 보안 정책을 유지하는 것은 "모든 직원이 회사 규정을 외워서 스스로 지키기를 기대하는 것"과 같다. 규정을 자동화된 시스템에 심으면 인간의 실수나 망각 없이 항상 적용된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| OPA (Open Policy Agent) | Gatekeeper의 정책 엔진, CNCF 졸업 프로젝트 |
| K8s Admission Controller | OPA Gatekeeper가 연결되는 K8s 확장 포인트 |
| Kyverno | Rego 없이 YAML로 정책 정의하는 대안 도구 |
| PSA (Pod Security Admission) | 기본 Pod 보안 프로파일, OPA로 추가 강화 |
| Conftest | CI 파이프라인에서 OPA 정책을 로컬 실행하는 도구 |
| DevSecOps | Policy as Code가 구현하는 보안 내재화 방법론 |

### 👶 어린이를 위한 3줄 비유 설명

1. OPA Gatekeeper는 학교 교문에 서 있는 자동 검사 기계 같아. 가방(YAML)을 들고 들어오면 "위험한 것 없이?", "학교 규정 지켰어?" 자동으로 확인해.

### 📈 관련 키워드 및 발전 흐름도

```text
K8s Admission Controller (Webhook)
    |
    v
OPA Gatekeeper: Rego 정책 언어 기반 검증
    +-► ConstraintTemplate: 정책 정의
    +-► Constraint: 네임스페이스/리소스에 적용
    |
    v
Kyverno: YAML 네이티브 정책 · Helm/Kustomize 통합
```
2. `image:latest` 금지는 "유통기한이 없는 음식은 학교에 가져오면 안 돼"와 같아. 반드시 날짜(버전)를 붙여야 해.
3. 사람이 매번 확인하지 않아도 기계가 24시간 지켜보니까 실수로 규정을 어기는 일이 없어.
