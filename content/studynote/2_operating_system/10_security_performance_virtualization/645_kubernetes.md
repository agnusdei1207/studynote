+++
title = "645. 쿠버네티스 (Kubernetes, K8s)"
date = "2026-03-16"
weight = 645
[extra]
categories = "studynote-operating-system"
keywords = ["운영체제", "Kubernetes", "K8s", "컨테이너 오케스트레이션", "Pod", "Deployment", "Service"]
+++

# 쿠버네티스 (Kubernetes, K8s)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 쿠버네티스(K8s)는 **컨테이너 오케스트레이션 플랫폼**으로, 여러 호스트의 컨테이너를 **배포, 확장, 관리**하고 **셀프 힐링, 롤링 업데이트**를 자동화한다.
> 2. **가치**: "수천 개의 컨테이너를 수동으로 관리하는 것은 불가능하다"는 문제를 해결하여 **구글급 운영 노하우를 오픈소스로 제공**하고 클라우드 네이티브의 표준이 되었다.
> 3. **융합**: Control Plane과 Worker Node의 분리, 선언적 API, 컨트롤 루프 패턴으로 **Desired State ↔ Current State**를 동기화한다.

+++

## Ⅰ. 쿠버네티스의 개요

### 1. 정의
- Kubernetes는 Google의 Borg 시스템에서 영감을 받아 개발된 컨테이너 오케스트레이션 플랫폼이다.
- 2014년 Google 발표, CNCF(Cloud Native Computing Foundation) 첫 프로젝트

### 2. 등장 배경: "컨테이너는 많은데谁来管?"
- Docker로 컨테이너 쉬워졌지만, **수백 수천 개 컨테이너 관리**는 새로운 문제
- Google은 15년+ 경험(Borg)을 공개

### 3. 💡 비유: '항구의 크레인과 관제 시스템'
- K8s는 **'항구의 컨테이너 자동 관제 시스템'**과 같다.
- 컨테이너(선적)의 위치, 상태, 스케줄링, 고장 시 대체를 자동으로 관리한다.

- **📢 섹션 요약 비유**: 교통 관제센터처럼, 수많은 차량(컨테이너)의 흐름을 자동으로 조정하고, 사고(장애) 시 우회 경로를 찾아줍니다.

+++

## Ⅱ. 쿠버네티스 아키텍처 (Deep Dive)

### 1. 전체 구조
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                   Kubernetes 아키텍처                           │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [Control Plane (마스터 노드)]                                  │
    │  ┌─────────────────────────────────────────────────────────┐   │
    │  │                                                         │   │
    │  │  [kube-apiserver]   (API 서버, 유일 진입점)             │   │
    │  │                                                         │   │
    │  │  [etcd]             (설정 저장소, key-value)           │   │
    │  │                                                         │   │
    │  │  [kube-scheduler]   (Pod를 어디에 배치할지 결정)       │   │
    │  │                                                         │   │
    │  │  [kube-controller-manager]                             │   │
    │  │   - Node Controller, Replication Controller...         │   │
    │  │                                                         │   │
    │  │  [cloud-controller-manager] (클라우드 공급자 연동)     │   │
    │  │                                                         │   │
    │  └─────────────────────────────────────────────────────────┘   │
    │                              │                                 │
    │                              │ api-server 통신                │
    │                              ▼                                 │
    │  [Worker Nodes]                                              │
    │  ┌──────────────────┐  ┌──────────────────┐                 │
    │  │  Node 1          │  │  Node 2          │                 │
    │  │  ┌────────────┐  │  │  ┌────────────┐  │                 │
    │  │  │ Pod1       │  │  │  │ Pod3       │  │                 │
    │  │  │ (Web)      │  │  │  │ (API)      │  │                 │
    │  │  ├────────────┤  │  │  ├────────────┤  │                 │
    │  │  │ Pod2       │  │  │  │ Pod4       │  │                 │
    │  │  │ (DB)       │  │  │  │ (Worker)   │  │                 │
    │  │  └────────────┘  │  │  └────────────┘  │                 │
    │  │                  │  │                  │                 │
    │  │  kubelet         │  │  kubelet         │                 │
    │  │  kube-proxy      │  │  kube-proxy      │                 │
    │  │  Container Runtime│  │  Container Runtime│                │
    │  └──────────────────┘  └──────────────────┘                 │
    │                                                                 │
    │  * 각 노드는 독립된 물리/가상 머신                             │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Control Plane 컴포넌트
| 컴포넌트 | 역할 | 설명 |
|:---|:---|:---|
| **kube-apiserver** | API 서버 | 모든 요청의 진입점, 인증/인가 |
| **etcd** | 설정 저장 | 분산 key-value 저장소, 클러스터 상태 |
| **kube-scheduler** | 스케줄링 | Pod를 어느 노드에 배치할지 결정 |
| **kube-controller-manager** | 컨트롤러 | 루프를 돌며 상태를 Desired State로 유지 |
| **cloud-controller-manager** | 클라우드 연동 | AWS/Azure/GCP와 통합 |

### 3. Worker Node 컴포넌트
| 컴포넌트 | 역할 |
|:---|:---|
| **kubelet** | API server와 통신, Pod 생명주기 관리 |
| **kube-proxy** | 네트워크 프록시, Service 구현 |
| **Container Runtime** | 컨테이너 실행 (containerd, CRI-O) |

- **📢 섹션 요약 비유**: Control Plane은 "본사", Worker Nodes는 "지사"입니다. 본사에서 명령을 내리면 각 지사의 관리자(kubelet)가 실행합니다.

+++

## Ⅲ. 쿠버네티스 핵심 개념

### 1. Pod (최소 배포 단위)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                       Pod 구조                                  │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   ┌───────────────────────────────────────────────────────┐    │
    │   │ Pod                                                    │    │
    │   │  ┌─────────────┐         ┌─────────────┐              │    │
    │   │  │ Container 1 │         │ Container 2 │ (선택)       │    │
    │   │  │ (Main App)  │         │ (Sidecar)  │              │    │
    │   │  └─────────────┘         └─────────────┘              │    │
    │   │         │                       │                      │    │
    │   │         └───────────┬───────────┘                      │    │
    │   │                     ▼                                  │    │
    │   │              [Shared Namespace]                        │    │
    │   │              - Network (IP, Port)                      │    │
    │   │              - Storage (Volumes)                       │    │
    │   │              - IPC                                     │    │
    │   └───────────────────────────────────────────────────────┘    │
    │                                                                 │
    │  * Pod 내 컨테이너는 localhost로 통신                         │
    │  * 각 Pod는 고유 IP 할당                                      │
    │  * Pod는 일시적 (재시작 시 새 IP)                             │
    └─────────────────────────────────────────────────────────────────┘
```

### 2. Deployment (상태 유지)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3              # 3개 복제본 유지
  selector:
    matchLabels:
      app: nginx
  template:               # Pod 템플릿
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### 3. Service (안정된 네트워크 엔드포인트)
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                    Service: 안정된 엔드포인트                    │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   ┌──────────────────┐                                        │
    │   │   Service        │ ◀── Cluster IP (고정)                   │
    │   │   (nginx-svc)    │                                        │
    │   └──┬───────────────┘                                        │
    │      │                                                      │
    │      ▼                                                      │
    │   [Pod Selector]                                             │
    │      │ app=nginx                                             │
    │      │                                                       │
    │      ▼                                                       │
    │   ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
    │   │ Pod1    │  │ Pod2    │  │ Pod3    │                      │
    │   │(10.1.1.5)│  │(10.1.2.3)│  │(10.1.3.7)│                      │
    │   └─────────┘  └─────────┘  └─────────┘                      │
    │                                                                 │
    │  * Service는 Pod들의 로드밸런서                                │
    │  * Pod가 재생성되어도 Service는 변함 없음                      │
    └─────────────────────────────────────────────────────────────────┘
```

### 4. ConfigMap & Secret
- **ConfigMap**: 설정 데이터 (비밀 아님)
- **Secret**: 비밀 데이터 (base64 인코딩, 암호화 가능)

+++

## Ⅳ. 선언적 API와 컨트롤 루프

### 1. Reconciliation Loop
```text
    ┌─────────────────────────────────────────────────────────────────┐
    │                 컨트롤 루프 (Reconciliation)                    │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  [사용자]                                                       │
    │      │                                                         │
    │      │ "3개 복제본 유지하고 싶어"                               │
    │      ▼                                                         │
    │  [Desired State]                                               │
    │   - Deployment YAML (replicas: 3)                              │
    │      │                                                         │
    │      ▼                                                         │
    │  [Controller]                                                  │
    │   - 현재 상태 관찰 (Watch)                                      │
    │   - 실제 상태 vs 원하는 상태 비교                                │
    │   - 차이 발생 시 조치                                           │
    │      │                                                         │
    │      ▼                                                         │
    │  [Current State]                                               │
    │   - 실제 실행 중인 Pod                                         │
    │   - "현재 2개만 있음"                                          │
    │      │                                                         │
    │      ▼                                                         │
    │  [Action]                                                      │
    │   - Pod 1개 생성                                               │
    │      │                                                         │
    │      └───────────────────────────────────┐                     │
    │                                          ▼                     │
    │                                   (루프 반복)                  │
    │                                                                 │
    │  * "Make Current State == Desired State"                        │
    └─────────────────────────────────────────────────────────────────┘
```

+++

## Ⅴ. 주요 기능

### 1. Self-Healing (셀프 힐링)
- Pod 죽으면 자동 재시작
- Node 죽으면 Pod 다른 노드로 재스케줄링
- Liveness/Readiness Probe로 상태 검사

### 2. Rolling Update (롤링 업데이트)
```bash
# 이미지 업데이트 (제로 다운타임)
kubectl set image deployment/nginx nginx=nginx:1.22

# 롤백
kubectl rollout undo deployment/nginx
```

### 3. Scaling (스케일링)
```bash
# 수동 스케일링
kubectl scale deployment nginx --replicas=5

# 오토스케일링 (HPA)
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80
```

+++

## Ⅵ. 실무 적용 및 모범 사례

### 1. 리소스 제한
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### 2. 안티패턴
- **"Fat Pod"**: 한 Pod에 여러 컨테이너
- **"Latest Tag"**: 이미지 버전 고정 안 함
- **"Root 실행"**: 보안 위험
- **"Resource Limits 없음"**: 리소스 낭비

+++

## Ⅶ. 기대효과 및 결론

### 1. 정량/정성 기대효과
- **가용성**: 99.9%+ (Self-Healing)
- **확장성**: 수천 개 노드, 수만 개 Pod
- **DevOps**: 개발-운영 간격 해소

### 2. 미래 전망
- **CSI**: Container Storage Interface 표준화
- **Service Mesh**: Istio, Linkerd와 통합

+++

## 📌 관련 개념 맵 (Knowledge Graph)
- **컨테이너**: 실행 단위
- **Docker**: 컨테이너 엔진
- **마이크로서비스**: 주요 아키텍처
- **CI/CD**: DevOps 파이프라인

+++

## 👶 어린이를 위한 3줄 비유 설명
1. 쿠버네티스는 **"로봇 교통 경찰"** 같아요.
2. 수많은 차량(컨테이너)의 흐름을 자동으로 조정하고, 사고(고장) 시 자동으로 우회로를 찾아줘요.
3. 덕분에 우리는 복잡한 도시에서도 막힘없이 달릴 수 있답니다!