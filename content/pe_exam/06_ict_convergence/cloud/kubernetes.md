+++
title = "쿠버네티스 (Kubernetes)"
date = 2025-03-01

[extra]
categories = "ict-cloud"
+++

# 쿠버네티스 (Kubernetes)

## 핵심 인사이트 (3줄 요약)
> **컨테이너 오케스트레이션의 사실상 표준**. 배포, 스케일링, 복구, 로드밸런싱 자동화. "컨테이너를 위한 운영체제"로 클라우드 네이티브의 핵심 인프라.

---

### Ⅰ. 개요

**개념**: 쿠버네티스(Kubernetes, K8s)는 **컨테이너화된 애플리케이션의 배포, 확장, 관리를 자동화하는 오픈소스 컨테이너 오케스트레이션 플랫폼**이다.

> 💡 **비유**: "컨테이너의 교향악 지휘자" - 수천 개의 컨테이너를 마치 오케스트라처럼 조율해요. 어떤 악기(컨테이너)가 언제 연주할지, 볼륨(리소스)은 얼마로 할지, 악기가 고장 나면 교체는 어떻게 할지 모두 자동으로 결정해요!

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: Docker만으로는 대규모 컨테이너 관리 어려움. 수천 개 컨테이너의 배치, 복구, 스케일링을 수동으로 관리 불가능. 장애 시 수동 복구 느림
2. **기술적 필요성**: 서비스 디스커버리, 로드 밸런싱, 롤링 업데이트, 셀프 힐링, 오토스케일링 등 컨테이너 운영에 필수적인 기능의 통합 플랫폼 필요
3. **산업적 요구**: 마이크로서비스 아키텍처, 하이브리드 클라우드, 멀티 클라우드 환경에서 일관된 운영 체제 요구

**핵심 목적**: 컨테이너 운영의 모든 측면을 자동화하여, 개발자는 애플리케이션 개발에, 운영자는 인프라 관리에 집중할 수 있게 하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| Control Plane | 클러스터 두뇌 | API Server, Scheduler, Controller Manager | 교향악 지휘자 |
| etcd | 분산 키-값 저장소 | 클러스터 상태 저장, Raft 합의 | 악보 보관소 |
| kubelet | 노드 에이전트 | 컨테이너 실행 관리 | 악기 연주자 |
| kube-proxy | 네트워크 프록시 | 서비스 로드밸런싱 | 음향 엔지니어 |
| Pod | 최소 배포 단위 | 1개 이상 컨테이너 그룹 | 연주자 1인(또는 듀엣) |

**쿠버네티스 아키텍처**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    쿠버네티스 클러스터 구조                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                  Control Plane (Master)                    │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │ │
│  │  │ API Server  │ │  Scheduler  │ │ Controller  │         │ │
│  │  │ (진입점)    │ │ (배치 결정) │ │  Manager    │         │ │
│  │  │             │ │             │ │ (상태 관리) │         │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘         │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │                      etcd                            │ │ │
│  │  │            (클러스터 상태 저장소)                      │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  │  ┌─────────────┐                                         │ │
│  │  │ Cloud       │                                         │ │
│  │  │ Controller  │  ← 클라우드 API 연동                    │ │
│  │  └─────────────┘                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Worker Nodes                           │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                │ │
│  │  │    Node 1       │  │    Node 2       │  ...           │ │
│  │  │  ┌───────────┐  │  │  ┌───────────┐  │                │ │
│  │  │  │  kubelet  │  │  │  │  kubelet  │  │                │ │
│  │  │  ├───────────┤  │  │  ├───────────┤  │                │ │
│  │  │  │ kube-proxy│  │  │  │ kube-proxy│  │                │ │
│  │  │  ├───────────┤  │  │  ├───────────┤  │                │ │
│  │  │  │ Container │  │  │  │ Container │  │                │ │
│  │  │  │  Runtime  │  │  │  │  Runtime  │  │                │ │
│  │  │  ├───────────┤  │  │  ├───────────┤  │                │ │
│  │  │  │Pod│Pod│Pod│  │  │  │Pod│Pod│Pod│  │                │ │
│  │  │  └───────────┘  │  │  └───────────┘  │                │ │
│  │  └─────────────────┘  └─────────────────┘                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 리소스 객체**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   쿠버네티스 핵심 리소스                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ 워크로드 리소스 (Workload Resources):                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  리소스         │ 용도                    │ 특징          │ │
│  │  ───────────────┼────────────────────────┼───────────────│ │
│  │  Pod            │ 최소 실행 단위          │ 1+ 컨테이너   │ │
│  │  ReplicaSet     │ 파드 복제본 유지        │ n개 유지      │ │
│  │  Deployment     │ ★ 무상태 앱 배포       │ 롤링업데이트  │ │
│  │  StatefulSet    │ ★ 상태 유지 앱         │ 순서, ID 보장 │ │
│  │  DaemonSet      │ 모든 노드 실행          │ 로그, 모니터링│ │
│  │  Job/CronJob    │ 일회성/주기적 작업      │ 배치 처리     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  2️⃣ 서비스 디스커버리 (Service Discovery):                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Service         │ 안정적 엔드포인트 제공                  │ │
│  │  - ClusterIP     │ 내부 통신 (기본값)                     │ │
│  │  - NodePort      │ 노드 포트로 외부 노출                  │ │
│  │  - LoadBalancer  │ 클라우드 LB 연동                       │ │
│  │  - ExternalName  │ 외부 서비스 DNS 별칭                   │ │
│  │  Ingress         │ HTTP(S) 라우팅, SSL 종료               │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  3️⃣ 설정 및 보안 (Config & Security):                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  ConfigMap       │ 설정 데이터 (환경변수, 파일)           │ │
│  │  Secret          │ 민감 정보 (암호화 저장 권장)           │ │
│  │  RBAC            │ 역할 기반 접근 제어                    │ │
│  │  NetworkPolicy   │ 파드 간 통신 제어                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  4️⃣ 스토리지 (Storage):                                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  PV (Persistent Volume)    │ 물리 스토리지 리소스         │ │
│  │  PVC (Persistent Volume Claim)│ 스토리지 요청             │ │
│  │  StorageClass              │ 동적 프로비저닝 템플릿       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① manifest작성 → ② API Server전송 → ③ etcd저장 → ④ Scheduler배치 → ⑤ kubelet실행 → ⑥ Controller감시
```

- **1단계**: YAML manifest로 원하는 상태(Desired State)를 정의. Deployment, Service 등 리소스 선언
- **2단계**: kubectl이 API Server에 REST 요청 전송. 인증/인가 후 요청 처리
- **3단계**: API Server가 etcd에 리소스 상태 저장. 모든 상태의 single source of truth
- **4단계**: Scheduler가 새 파드를 어느 노드에 배치할지 결정. 리소스, 제약조건,亲和性 고려
- **5단계**: kubelet이 할당된 파드를 감지하고 컨테이너 런타임으로 실행
- **6단계**: Controller Manager가 실제 상태와 원하는 상태를 지속 비교하여 조정

**선언적 API (Declarative API)**:

```
┌─────────────────────────────────────────────────────────────────┐
│                   선언적 vs 명령형 API                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  명령형 (Imperative):                                           │
│  "nginx 컨테이너 3개 실행해"                                     │
│  → 실행 후 끝. 상태 추적 안 함                                   │
│                                                                 │
│  선언적 (Declarative) ★ Kubernetes 방식:                        │
│  "nginx 컨테이너가 항상 3개 있어야 해"                           │
│  → 지속적 조정. 3개 유지를 위해 자동 복구                        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   Control Loop                            │ │
│  │                                                           │ │
│  │    Desired State          Current State                   │ │
│  │    (YAML manifest)   ───→ (Compare)  ←───  (etcd)        │ │
│  │            │                │                             │ │
│  │            │                ↓                             │ │
│  │            │         Match? ──→ Yes → Done                │ │
│  │            │                │                             │ │
│  │            │                No                            │ │
│  │            │                ↓                             │ │
│  │            └───────────── Reconcile (조정)                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**코드 예시** (Kubernetes Manifests):

```yaml
# deployment.yaml - 웹 애플리케이션 배포
# ============================================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-deployment
  namespace: production
  labels:
    app: webapp
    tier: frontend
spec:
  replicas: 3                    # 3개 복제본 유지
  revisionHistoryLimit: 10       # 롤백을 위한 이력 보관
  selector:
    matchLabels:
      app: webapp
  strategy:
    type: RollingUpdate          # 롤링 업데이트 전략
    rollingUpdate:
      maxSurge: 1                # 최대 1개 추가 가능
      maxUnavailable: 0          # 최소 파드 중단 없음
  template:
    metadata:
      labels:
        app: webapp
        version: v1.2.3
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      serviceAccountName: webapp-sa
      securityContext:
        runAsNonRoot: true       # root 실행 금지
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: webapp
          image: registry.example.com/webapp:v1.2.3
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
              protocol: TCP
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: webapp-secrets
                  key: database-url
          envFrom:
            - configMapRef:
                name: webapp-config
          resources:
            requests:             # 최소 보장 리소스
              cpu: "100m"         # 0.1 CPU
              memory: "128Mi"
            limits:               # 최대 사용 리소스
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:          # 생존 확인
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:         # 준비 확인
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: config-volume
              mountPath: /etc/config
              readOnly: true
            - name: tmp-volume
              mountPath: /tmp
      volumes:
        - name: config-volume
          configMap:
            name: webapp-config
        - name: tmp-volume
          emptyDir: {}
      affinity:                   # 스케줄링 제약
        podAntiAffinity:          # 같은 앱 파드 분산
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: webapp
                topologyKey: kubernetes.io/hostname
      tolerations:                # 테인트가 있는 노드에서도 실행
        - key: "dedicated"
          operator: "Equal"
          value: "frontend"
          effect: "NoSchedule"
---
# service.yaml - 서비스 노출
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: webapp
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
---
# hpa.yaml - 수평 파드 오토스케일러
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5분 대기
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
---
# ingress.yaml - 인그레스 (HTTP 라우팅)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - webapp.example.com
      secretName: webapp-tls
  rules:
    - host: webapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-service
                port:
                  number: 80
```

```bash
# 핵심 kubectl 명령어
# ============================================================

# 배포
kubectl apply -f deployment.yaml
kubectl get deployments -n production
kubectl get pods -n production -o wide

# 스케일링
kubectl scale deployment/webapp-deployment --replicas=5 -n production
kubectl autoscale deployment webapp-deployment --cpu-percent=70 --min=3 --max=10

# 롤링 업데이트
kubectl set image deployment/webapp-deployment webapp=webapp:v1.2.4 -n production
kubectl rollout status deployment/webapp-deployment -n production
kubectl rollout undo deployment/webapp-deployment -n production  # 롤백
kubectl rollout history deployment/webapp-deployment -n production

# 디버깅
kubectl describe pod <pod-name> -n production
kubectl logs <pod-name> -n production -f --tail=100
kubectl exec -it <pod-name> -n production -- /bin/sh
kubectl port-forward pod/<pod-name> 8080:8080 -n production

# 상태 확인
kubectl top nodes
kubectl top pods -n production
kubectl get events -n production --sort-by='.lastTimestamp'
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:

| 장점 | 단점 |
|-----|------|
| 셀프 힐링 (자동 복구) | 학습 곡선 가파름 |
| 오토스케일링 | 운영 복잡도 높음 |
| 롤링 업데이트/롤백 | 리소스 오버헤드 |
| 멀티 클라우드 이식성 | 디버깅 어려움 |
| 거대한 생태계 | 초기 설정 복잡 |
| 선언적 API (GitOps) | 네트워크 복잡성 |

**오케스트레이션 플랫폼 비교**:

| 비교 항목 | Kubernetes | Docker Swarm | Nomad | ECS |
|---------|-----------|--------------|-------|-----|
| 복잡도 | ★ 높음 | 낮음 | 중간 | 중간 |
| 기능 | ★ 완전 | 기본 | 유연 | AWS 한정 |
| 생태계 | ★ 최대 | 작음 | 성장 | AWS |
| 학습 곡선 | 가파름 | ★ 완만 | 중간 | 중간 |
| 멀티 클라우드 | ★ 지원 | 지원 | 지원 | X |
| 엔터프라이즈 | ★ 표준 | 소규모 | 하이브리드 | AWS |

> **★ 선택 기준**:
> - 대규모, 엔터프라이즈, 멀티 클라우드 → **Kubernetes**
> - 소규모, 간단한 설정 → **Docker Swarm**
> - 하이브리드 워크로드 (VM+컨테이너) → **Nomad**
> - AWS 단일 클라우드 → **ECS**

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| 마이크로서비스 플랫폼 | 각 서비스를 Deployment로 배포, Service Mesh 연동 | 배포 빈도 10배 증가, 장애 복구 1분 이내 |
| CI/CD 파이프라인 | GitOps (ArgoCD), 자동 롤링 업데이트 | 배포 시간 90% 단축, 롤백 30초 |
| 하이브리드 클라우드 | 온프렘 + 클라우드 멀티 클러스터 | 인프라 비용 40% 절감, 가용성 99.99% |
| AI/ML 워크로드 | Kubeflow로 학습/추론 파이프라인 | GPU 활용률 80% 향상, 모델 배포 1시간 |

**실제 도입 사례**:

- **사례 1: Pokemon GO** - 출시 첫날 50배 트래픽 폭주. Google Kubernetes Engine (GKE)으로 자동 스케일링. 수백만 동시 접속자 처리. 서버 중단 0회
- **사례 2: Airbnb** - 4,000+ 마이크로서비스, 100,000+ 일일 배포. Kubernetes로 통합 운영. 배포 시간 1시간 → 5분
- **사례 3: 바이두** - 2,000+ 노드, 2,000,000+ 컨테이너. 세계 최대 규모 K8s 클러스터. 오토스케일링으로 40% 비용 절감

**도입 시 고려사항** (4가지 관점):

1. **기술적**:
   - 컨테이너 런타임 선택 (containerd, CRI-O)
   - CNI 플러그인 (Calico, Cilium, Weave)
   - CSI 드라이버 (스토리지)
   - 모니터링 스택 (Prometheus, Grafana)

2. **운영적**:
   - 관리형 vs 자체 관리 (EKS/GKE/AKS vs kubeadm)
   - 백업/복구 전략 (Velero)
   - 로그 수집 (Fluentd, Loki)
   - GitOps 도구 (ArgoCD, Flux)

3. **보안적**:
   - RBAC 구성
   - NetworkPolicy 설정
   - Pod Security Standards
   - 이미지 스캔 (Trivy)

4. **경제적**:
   - 관리형 vs 직접 운영 비용
   - 클러스터 밀도 최적화
   - Spot/Preemptible 인스턴스 활용
   - FinOps 도구 도입

**주의사항 / 흔한 실수**:

- ❌ **리소스 제한 미설정**: 노드 리소스 고갈 → OOM Kill. requests/limits 반드시 설정
- ❌ **liveness/readiness Probe 생략**: 트래픽이 준비 안 된 파드로 전달. 무조건 설정
- ❌ **단일 클러스터에 모든 워크로드**: 장애 영향 범위 확대. 멀티 클러스터/Zone 고려
- ❌ **etcd 백업 없음**: 클러스터 상태 손실 시 복구 불가. 정기 백업 필수

**관련 개념 / 확장 학습**:

```
📌 쿠버네티스 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                  쿠버네티스 생태계                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [Docker] ←──→ [Kubernetes] ←──→ [Service Mesh]               │
│        ↓              ↓               ↓                         │
│   [containerd]   [Helm/ArgoCD]   [Istio/Linkerd]                │
│        ↓              ↓               ↓                         │
│   [OCI Runtime]  [GitOps]        [Observability]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| Docker | 선행 | 컨테이너 런타임 | `[도커](./docker_container.md)` |
| Helm | 확장 | 패키지 매니저 | `[Helm](./helm.md)` |
| Service Mesh | 확장 | 서비스 간 통신 | `[서비스메시](./service_mesh.md)` |
| GitOps | 방법론 | 선언적 배포 | `[GitOps](./gitops.md)` |
| Microservices | 응용 | 아키텍처 패턴 | `[마이크로서비스](./microservices.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 가용성 | 셀프 힐링, 다중 복제본 | 99.9%+ uptime |
| 확장성 | 오토스케일링 | 트래픽 10배 처리 가능 |
| 배포 속도 | 롤링 업데이트 | 무중단 배포 5분 |
| 복구 시간 | 자동 장애 복구 | RTO < 1분 |

**미래 전망** (3가지 관점):

1. **기술 발전 방향**: 멀티 클러스터 페더레이션 (KubeFed). AI 기반 스케줄링. WebAssembly 지원. Edge 컴퓨팅 통합 (K3s)
2. **시장 트렌드**: 관리형 Kubernetes 성장. 플랫폼 엔지니어링 표준화. FinOps 통합
3. **후속 기술**: Kubernetes 정책 자동화 (Kyverno). 서버리스 컨테이너 (Knative). AI 모델 서빙 (KServe)

> **결론**: 쿠버네티스는 컨테이너 오케스트레이션의 **사실상 표준**으로, 클라우드 네이티브 아키텍처의 핵심 인프라다. 학습 곡선이 가파르지만, 대규모 분산 시스템의 운영 자동화에는 대안이 없다. Helm, ArgoCD, Service Mesh 등 생태계 도구와 함께 "Kubernetes 플랫폼"으로 진화하고 있다.

> **※ 참고 표준**: CNCF (Cloud Native Computing Foundation), NIST SP 800-204, CIS Kubernetes Benchmark

---

## 어린이를 위한 종합 설명

**쿠버네티스**는 마치 **스마트한 창고 관리자 로봇**과 같아요.

첫 번째 문단: 큰 창고에 물건(컨테이너)이 1,000개가 있어요. 어떤 건 식료품, 어떤 건 전자제품이에요. 사람이 직접 관리하면 너무 힘들어요! "A구역에 식료품 10개, B구역에 전자제품 5개..." 쿠버네티스는 이걸 자동으로 해주는 로봇이에요.

두 번째 문단: 로봇은 항상 감시해요. "식료품 컨테이너가 10개 있어야 하는데 8개네? 2개 더 만들어야지!" 하고 자동으로 컨테이너를 추가해요. 어떤 컨테이너가 고장 나면 "이상해! 새 걸로 교체해야지!" 하고 바꿔요. 크리스마스에 주문이 많이 들어오면 "너무 바빠! 일꾼(컨테이너) 100명 더 불러!" 하고 늘려요.

세 번째 문단: 개발자들은 "웹사이트 3개 실행해줘!"라고만 말하면 돼요. 로봇이 알아서 3개를 만들고, 감시하고, 고치고, 늘려줘요. 개발자는 로봇에게 명령만 내리고, 로봇이 모든 걸 처리해요. 그래서 요즘 모든 큰 회사는 이 로봇을 써요! 🤖

---

## ✅ 작성 완료 체크리스트

- [x] 핵심 인사이트 3줄 요약
- [x] Ⅰ. 개요: 개념 + 비유 + 등장배경(3가지)
- [x] Ⅱ. 구성요소: 표(5개) + 다이어그램 + 단계별 동작 + YAML 코드
- [x] Ⅲ. 비교: 장단점 표 + 대안 비교표 + 선택 기준
- [x] Ⅳ. 실무: 적용 시나리오(4개) + 실제 사례(3개) + 고려사항(4가지) + 주의사항(4개)
- [x] Ⅴ. 결론: 정량 효과 표 + 미래 전망(3가지) + 참고 표준
- [x] 관련 개념: 5개 나열 + 개념 맵 + 링크
- [x] 어린이를 위한 종합 설명 (3문단)
