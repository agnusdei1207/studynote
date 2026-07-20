---
title: "Helm Package Manager"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 315
---
> **핵심 인사이트**
> - Helm (헬름)은 쿠버네티스의 패키지 매니저로, 복잡한 애플리케이션을 Chart (차트) 단위로 묶어 버전 관리한다.
> - Go 템플릿 기반의 `values.yaml` 파라미터화로 같은 Chart를 개발·스테이징·운영에 환경별로 다르게 배포할 수 있다.
> - Release (릴리스)는 클러스터에 설치된 Chart 인스턴스로, Rollback·Upgrade 이력이 자동 관리된다.

---

## Ⅰ. Helm 기본 개념

Helm의 핵심 구성:

| 개념         | 설명                                         |
|--------------|----------------------------------------------|
| Chart        | 쿠버네티스 매니페스트 + 템플릿 묶음 패키지    |
| Repository   | Chart를 저장·배포하는 HTTP 서버               |
| Release      | 클러스터에 설치된 Chart 인스턴스              |
| values.yaml  | 파라미터 기본값 파일                          |

```
+----------------------------------------------------+
|                   Helm 동작 흐름                   |
|                                                    |
|  Chart (템플릿)                                    |
|     + values.yaml  --render--->  K8s 매니페스트    |
|                                      |             |
|                               kubectl apply        |
|                                      |             |
|                                  Release 생성       |
+----------------------------------------------------+
```

> 📢 **Ⅰ 섹션 요약 비유**
> Helm Chart는 요리 레시피, values.yaml은 재료 목록, Release는 완성된 요리다.

---

## Ⅱ. Chart 구조

```
mychart/
+-- Chart.yaml          # 메타데이터 (이름, 버전, appVersion)
+-- values.yaml         # 기본 파라미터 값
+-- templates/
|   +-- deployment.yaml # Go 템플릿 매니페스트
|   +-- service.yaml
|   +-- _helpers.tpl    # 재사용 템플릿 정의
+-- charts/             # 의존 Sub-Chart
```

Go 템플릿 예시 (`deployment.yaml`):

```yaml
replicas: {{ .Values.replicaCount }}
image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
```

> 📢 **Ⅱ 섹션 요약 비유**
> Chart 디렉터리는 요리책 — 레시피(templates/)와 기본 재료표(values.yaml)가 함께 묶여 있다.

---

## Ⅲ. Helm 주요 명령어

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm search repo bitnami/nginx

helm install my-nginx bitnami/nginx --values prod-values.yaml
helm upgrade my-nginx bitnami/nginx --set image.tag=1.25
helm rollback my-nginx 1   # revision 1로 롤백
helm uninstall my-nginx
helm history my-nginx      # 릴리스 이력 조회
```

**Helmfile**: 여러 Chart 릴리스를 선언적으로 관리하는 도구다.

> 📢 **Ⅲ 섹션 요약 비유**
> helm install은 앱 설치, helm upgrade는 업데이트, helm rollback은 이전 버전으로 되돌리기 — 스마트폰 앱 관리와 똑같다.

---

## Ⅳ. Helm 3 vs Helm 2 차이점

| 항목          | Helm 2                        | Helm 3                         |
|---------------|-------------------------------|--------------------------------|
| Tiller        | 서버사이드 컴포넌트 필요       | 제거 (클라이언트 전용)          |
| 보안          | Tiller 과도 권한 문제          | RBAC 직접 활용                  |
| Release 저장  | ConfigMap (kube-system)        | Secret (각 네임스페이스)        |
| 스키마 검증   | 제한적                        | values.schema.json 지원         |

Helm 3는 Tiller (틸러) 제거로 보안이 크게 강화됐다.

> 📢 **Ⅳ 섹션 요약 비유**
> Helm 2는 창고 관리인(Tiller)을 별도로 두는 방식, Helm 3는 각자 직접 창고에 접근하는 방식으로 단순해졌다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소        | 역할                                     |
|------------------|------------------------------------------|
| Chart            | 쿠버네티스 앱 패키지                      |
| Repository       | Chart 저장소                             |
| Release          | 클러스터 내 배포 인스턴스                |
| values.yaml      | 파라미터 기본값                          |
| Helmfile         | 다중 릴리스 선언적 관리                  |
| OCI Registry     | Chart를 컨테이너 레지스트리에 저장       |

### 관련 키워드 및 발전 흐름도

```
Helm Package Manager
    +-- Chart -> 패키지 구조 (Chart.yaml, values.yaml, templates/)
    +-- Repository -> ArtifactHub, Bitnami, OCI Registry
    +-- Release -> install / upgrade / rollback
    +-- Helmfile / ArgoCD -> GitOps 기반 Helm 관리
```

> 🧒 **어린이 비유**
> Helm은 레고 설명서 세트예요. Chart가 설명서, values.yaml이 원하는 색깔 선택표, Release는 완성된 레고 작품이에요.
