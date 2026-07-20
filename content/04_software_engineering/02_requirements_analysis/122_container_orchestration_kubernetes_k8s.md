---
title: "Container Orchestration Kubernetes K8S"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 122
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 컨테이너 오케스트레이션은 <strong>수백~수천 개 컨테이너의 배포·스케일링·네트워킹·자동 복구를 자동화</strong>하는 시스템이며, Kubernetes(K8s)가 사실상 유일한 산업 표준이다.
> 2. **가치**: 단일 Docker 컨테이너는 `docker run`으로 관리하지만, 프로덕션 환경에서 수백 컨테이너의 <strong>헬스체크·오토스케일링·롤링 업데이트·서비스 디스커버리</strong>를 수동 관리하는 것은 불가능하며, K8s가 이를 <strong>선언적으로 자동화</strong>한다.
> 3. **판단 포인트**: K8s의 핵심은 <strong>Desired State -> Reconciliation Loop</strong>이며, Pod·Deployment·Service·Ingress의 4대 리소스와 Control Plane(API Server·etcd·Scheduler·Controller Manager)의 아키텍처를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    K8s 클러스터 아키텍처                              |
+-------------------------------------------------------+
|  [Control Plane (Master)]                             |
|   API Server <- kubectl / CI/CD                       |
|   etcd (상태 저장소)                                  |
|   Scheduler (Pod 배치)                                |
|   Controller Manager (Reconciliation)                 |
|                                                       |
|  [Worker Nodes]                                       |
|   kubelet -> Pod(Container) 실행                      |
|   kube-proxy -> 네트워크 라우팅                       |
|   Container Runtime (containerd)                      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: K8s는 항공 관제탑(Control Plane)이 수백 대 비행기(컨테이너)의 이착륙·경로·연료(리소스)를 자동 관리하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4대 핵심 리소스

| 리소스 | 역할 |
|:---|:---|
| <strong>Pod</strong> | 컨테이너 실행 최소 단위 |
| <strong>Deployment</strong> | Pod 복제·롤링 업데이트 관리 |
| <strong>Service</strong> | Pod 그룹에 안정적 네트워크 엔드포인트 |
| <strong>Ingress</strong> | 외부 HTTP 트래픽 라우팅 |

- **📢 섹션 요약 비유**: Pod는 방(컨테이너), Deployment는 아파트 동(복제 관리), Service는 우편함(고정 주소), Ingress는 정문(외부 접근)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Docker Compose | K8s | Nomad |
|:---|:---|:---|:---|
| **규모** | 단일 호스트 | **멀티 노드 클러스터** | 멀티 노드 |
| **Self-healing** | 없음 | <strong>자동 복구</strong> | 자동 복구 |
| **생태계** | 작음 | <strong>최대 (CNCF)</strong> | 작음 |

---

## Ⅳ. 실무 적용 및 실무자 판단

### K8s 도입 판단 기준
- 컨테이너 10개 이하: Docker Compose로 충분.
- 컨테이너 50개+, 멀티팀: K8s 도입 적합.
- 서버리스 우선: AWS Fargate/Cloud Run 고려.

---

## Ⅴ. 기대효과 및 결론

K8s는 <strong>클라우드 네이티브의 운영 체제</strong>이며, CNCF 생태계(Istio·ArgoCD·Prometheus·Cilium)와 결합하여 현대 인프라의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Pod</strong> | K8s 최소 실행 단위 |
| <strong>Deployment</strong> | Pod 복제·업데이트 관리 |
| **Control Plane** | API Server·etcd·Scheduler |
| <strong>CNCF</strong> | K8s 생태계 재단 |
| <strong>Helm</strong> | K8s 패키지 매니저 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Docker (2013) — 컨테이너 런타임]
    |
    v
[Docker Swarm / Mesos (2014~) — 초기 오케스트레이션]
    |
    v
[Kubernetes (2014, Google->CNCF) — 산업 표준]
    |
    v
[Managed K8s (EKS/GKE/AKS, 2018~)]
    |
    v
[현재: K8s + Service Mesh + GitOps — 클라우드 네이티브 풀스택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K8s는 <strong>항공 관제탑</strong>이에요. 수백 대 비행기(컨테이너)를 자동으로 관리해요.
2. 비행기가 고장 나면 **자동으로 다른 비행기를 보내서(Self-healing)** 서비스가 멈추지 않아요.
3. "비행기 3대 유지해"라고 말하면(선언적) **관제탑이 알아서** 3대를 유지한답니다!
