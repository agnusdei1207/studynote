---
title: "Container Orchestration Kubernetes Architecture"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 615
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes는 선언적(Declarative) Pod 스펙과 상태를 etcd 기반의 분산 KV-Store에 영속화하고, kube-apiserver를 단일 진실 공급원(SoT)으로 삼아 Control Plane이 Scheduler/Controller-Manager로 **Desired State -> Actual State의 Reconciliation Loop**를 수렴시키는 Self-Healing 컨테이너 오케스트레이터이다.
> 2. **가치**: 동일 클러스터에서 수천 노드/수만 Pod를 자동 스케일(HPA·VPA·KEDA), 자동 복구, 선언적 배포(Rolling/Blue-Green/Canary), Secret·ConfigMap 기반 GitOps를 통해 **배포 리드타임을 일/주 단위에서 분 단위로 95% 이상 단축**하며, 평균 가용성(MTBF)을 SLO 99.95% 이상으로 끌어올린다.
> 3. **판단 포인트**: kubelet ↔ CRI(Containerd/CRI-O) ↔ OCI 런타임 ↴ CNI(Cilium/Calico) ↔ CSI ↔ Ingress Gateway의 **6계층 Plugin 인터페이스** 선택이 성능/보안/관측성을 좌우하며, **etcd 쿼럼·API Server HA·Kube-Scheduler Spread Constraint**를 어떻게 설계하느냐가 대규모 운영의 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

전통적 VM 기반 배포는 하이퍼바이저·게스트 OS·미들웨어 부팅에 30초~수 분이 소요되고, 동일 하드웨어에서 OS 이미지 단위의 격리만 제공해 **배포 밀도(Density)가 8~20 vCPU/호스트 수준에 머물렀다**. 2013년 Docker의 등장으로 OS 커널 공유(cgroup+namespace) 기반의 **프로세스 단위 컨테이너**가 도입되며 밀도는 5~10배 향상되었지만, 호스트 장애·스케줄링·서비스 디스커버리·롤백 등은 여전히 운영자의 **수작업 Ansible/Systemd 스크립트**에 의존했다.

Kubernetes(구 Google Borg, 2014년 6월 공개, v1.0은 2015년 7월)는 이를 **"선언적 인프라 + 자동화 컨트롤 루프"**로 전환한 것이다. **"내가 원하는 상태"**를 YAML/JSON 매니페스트로 제출하면, 컨트롤 플레인이 끊임없이 현재 상태를 관측하고 차이를 보정한다. 이로써 Stateless/Microservice 시대의 핵심 요구사항인 **Immutable Deployment, Horizontal Scalability, Service Discovery & Load Balancing, Self-Healing, Secret Management, Rolling Update, RBAC**이 단일 플랫폼에서 모두 해결된다.

```text
 [Legacy VM Era]                       [Container Era]                    [Kubernetes Era]
 +--------------+                +--------------+                  +----------------------+
 |  App (War)   |                |  App (Image) |                  |  Deployment (YAML)   |
 |  ----------- |                |  ----------- |                  |  ------------------  |
 |  JVM 1.7     |  ➜ VM Image   |  JVM 11      |  ➜ Container    |  ReplicaSet=3        |
 |  Tomcat 8    |  provisioning |  SpringBoot  |  run via Docker  |  + HPA + PDB + NetPol|
 |  OS + Libs   |    (30분)     |  Alpine      |    (10초)        |  + Ingress + Service  |
 +--------------+                +--------------+                  +----------------------+
        |                                |                                  |
   수동 스케일/HA                  Docker Compose/Swarm                Auto-Healing/Scale
   장애 시 수동 조치              Service Discovery 약함                GitOps/Operator
```

클라우드 네이티브 통계(2024 CNCF Survey)에 따르면 프로덕션 컨테이너 사용자의 **96%가 Kubernetes를 오케스트레이션 엔진으로 채택**했고, 79%가 다중 클러스터(Multi-Cluster/Multi-Cloud) 전략을 채택 중이다. 이처럼 **쿠버네티스는 단순 컨테이너 매니저가 아니라 클라우드 시대의 "리눅스"라 불리는 분산 운영체제**로 자리매김했다.

- **📢 섹션 요약 비유**: 컨테이너가 **택배 상자**라면, 쿠버네티스는 상자를 어떤 트럭(노드)에 실을지, 트럭이 고장나면 짐을 어떻게 옮길지, 주소는 어떻게 붙일지 전부 자동으로 결정하는 **물류 총괄 시스템(Total Logistics Control Tower)**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

쿠버네티스는 크게 **Control Plane(Master) 노드**와 **Worker Node**로 분리되며, 모든 통신은 **kube-apiserver**를 경유하는 Hub-and-Spoke 구조다. 컨트롤 루프(Control Loop)는 "Observe -> Diff -> Reconcile"의 3단계로 동작하며, 이를 **Reconciliation Pattern**이라 한다.

```text
                            +------------------------------------------------------+
                            |                  CONTROL PLANE                       |
                            |                                                       |
   kubectl/Helm/ArgoCD --->  |  +--------------+    +--------------------------+    |
   (HTTPS+gRPC, TLS)        |  | kube-apiserver|<---->|   etcd (Raft, Port 2379) |    |
                            |  |  :6443        |    |  +------+------+------+  |    |
                            |  +------+-------+    |  |  R0  |  R1  |  R2  |  |    |
                            |         | Watch/List |  +------+------+------+  |    |
                            |         v            +--------------------------+    |
                            |  +--------------+    +--------------------------+    |
                            |  |kube-scheduler|    | kube-controller-manager  |    |
                            |  |• Filtering   |    | • Node Controller         |    |
                            |  |• Scoring     |    | • ReplicaSet Controller   |    |
                            |  |• Binding     |    | • Endpoints Controller    |    |
                            |  +------+-------+    | • Job/StatefulSet...      |    |
                            |         |            +--------------------------+    |
                            |         |            +--------------------------+    |
                            |         +------------>| cloud-controller-manager |    |
                            |                      +--------------------------+    |
                            +------------------------------+-----------------------+
                                                           | gRPC over TLS
                            +------------------------------v-----------------------+
                            |                    WORKER NODE 1                      |
                            |  +------------------------------------------------+    |
                            |  |                  kubelet :10250                |    |
                            |  |   • Sync Pod Spec     • cAdvisor Metrics       |    |
                            |  +------------+-----------------------+-----------+    |
                            |               | CRI(Containerd)      | CNI(Cilium)     |
                            |       +-------v--------+     +-------v--------+        |
                            |       |  Pod (linux ns) |     |  Pod (linux ns)|        |
                            |       |  +---+ +---+   |     |  +---+        |        |
                            |       |  |App| |Sidecar|     |  |App|        |        |
                            |       |  +---+ +---+   |     |  +---+        |        |
                            |       +----------------+     +---------------+        |
                            |  +--------------------+                              |
                            |  |  kube-proxy (iptables/IPVS/eBPF) :nodePort       |    |
                            |  +--------------------+                              |
                            +------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **kube-apiserver** | 클러스터의 **유일한 Front-Door & REST 게이트웨이** | OpenAPI 스펙 노출, RBAC/Admission Webhook, **etcd 앞단의 Read/Write Lock 관리**, List-Watch 기반의 Informer Cache 제공. 수평 확장 가능(Stateless). |
| **etcd** | 모든 클러스터 상태를 저장하는 **분산 KV-Store** | Raft 합의 알고리즘(과반수 Quorum = N/2+1), WAL(Write-Ahead Log) + Snapshotting, **64MB Warning, 2GB Max Object Size**, 모든 변경은 Revision 단위로 단조 증가(MVCC) |
| **kube-scheduler** | 미할당(Pending) Pod을 최적 노드에 배치 | 2단계 알고리즘: **Filtering(예: NodeSelector, Taints/Tolerations, ResourceFit, NodeAffinity, PodTopologySpread)** -> **Scoring(LeastAllocated, BalancedResource, ImageLocality)** -> **Binding**(api-server의 `/bindings` 서브리소스 PATCH) |
| **kube-controller-manager** | 클러스터 상태를 **Desired State로 수렴**시키는 컨트롤러 데몬 | ReplicaSet, Deployment, StatefulSet, DaemonSet, Job, CronJob, ServiceAccount, Token, Endpoint, NodeLifecycle 등 약 35종 내장 컨트롤러(각각 goroutine). `--leader-elect=true`로 HA 시 Leader Lock 획득 |
| **cloud-controller-manager(CCM)** | 클라우드 종속 로직 분리(LoadBalancer, Node, Route) | AWS/GCP/Azure/Azure Stack별 Provider Plugin. kubelet 등록 시 `NodeLifecycleController`가 Cloud API로 인스턴스 메타데이터 동기화, Service `type:LoadBalancer` 시 LB Provisioning |
| **kubelet** | 노드 에이전트, **PodSpec 수신 -> CRI 호출** | `PLEG(Pod Lifecycle Event Generator)`가 컨테이너 런타임 상태를 폴링, `/pods` API로 Heartbeat(기본 10s), cAdvisor로 cgroup 메트릭 수집, Liveness/Readiness/Startup Probe 실행 |
| **kube-proxy** | Service ClusterIP/NodePort를 **노드 로컬 네트워크로 구현** | 모드: `iptables`(기본, O(N) 규칙), `IPVS`(hash + O(1) 룩업, 100만+ 서비스 가능), `kernelspace`(legacy). Cilium eBPF 모드 사용 시 kube-proxy 대체 가능(IPTables 우회) |
| **Container Runtime** | 실제 컨테이너 실행·격리 | OCI 호환: **Containerd(OCI Runtime: runc/crun)**, **CRI-O**(쿠버네티스 전용 경량), Mirantis CRI-DockerD(레거시). CRI(gRPC) 인터페이스: `RunPodSandbox`, `CreateContainer`, `StartContainer`, `ContainerStatus` |

### 핵심 동작 메커니즘 심화

**① List-Watch & Informer 패턴**
컨트롤 플레인·컨트롤러는 api-server에 단발성 HTTP GET을 하지 않고, `/api/v1/pods?watch=true&resourceVersion=X`로 **HTTP Chunked Streaming** 기반의 Long-Polling Watch를 개설한다. 클라이언트는 `Informer` 라이브러리(SharedInformer)로 **로컬 메모리 캐시(Store/ThreadSafeMap)**를 유지하고, 변경 이벤트(Add/Update/Delete)마다 DeltaFIFO에 push되며, **Indexer**(FIFO + ThreadSafeMap)로 라벨 셀렉터 기반 O(1) 조회를 수행한다. 이 설계가 **수만 오브젝트 Watch 시 단일 api-server가 1k+ QPS로 동작**할 수 있는 핵심이다.

**② Scheduling 2-Phase 알고리즘**
```
Filter: (호환 노드 없으면 unschedulable, 5s timeout)
  +- NodeName / NodeSelector / NodeAffinity
  +- Taints/Tolerations (NoSchedule/PreferNoSchedule/NoExecute)
  +- PodFitsHostPorts / PodFitsHostNames
  +- MatchNodeSelector(VolumeNodeAffinity, PersistentVolume)
  +- PodFitsResources(CPU/Mem/EphemeralStorage, Requests/Limits)
  +- PodTopologySpread(zone, hostname)

Score(0~100):
  LeastAllocated = (capacity-requested)/capacity × 100
  BalancedAllocation = 1 - |cpufrac-memfrac| (편향 최소)
  ImageLocality = 이미 캐시된 이미지 우선
  InterPodAffinity(weight) = 동일 affinity 라벨 노드 가점
  NodeAffinity(weight), TaintToleration(weight)
```

**③ Reconciliation Loop (예: ReplicaSet Controller)**
```go
// Pseudocode
for {
    desired := rs.Spec.Replicas
    current := listPods(rs.Namespace, rs.Selector).len()
    if current < desired { createPod(rs.Template) }
    if current > desired { deletePod(oldestPod) }
    sleep(syncPeriod)  // default 10s
}
```
Deployment Controller는 이를 확장해 **Rolling Update 전략**(maxSurge, maxUnavailable)·**Rollout History**(`revisionHistoryLimit`)·**Pause/Resume**를 처리한다.

**④ Pod 라이프사이클 & Probe**
- **Pending**(스케줄링 전) -> **ContainerCreating**(이미지 pull) -> **Running**(모든 컨테이너 Ready) -> **Succeeded/Failed**
- `LivenessProbe`: 실패 시 컨테이너 재시작(`restartPolicy: Always` 기본)
- `ReadinessProbe`: 실패 시 **Service Endpoints에서 제거**(트래픽 차단, 재시작 X)
- `StartupProbe`: 부팅 느린 컨테이너용, 성공 시까지 Liveness 비활성
- `PreStop Hook`: `kubectl delete` 후 SIGTERM 직전 실행(`sleep 30` 권장 — Endpoint Controller가 Endpoints 정리하기 전 Grace Period)

- **📢 섹션 요약 비유**: 쿠버네티스는 **"항해 중인 선장"**이다. **지도(etcd)**에 목적지 좌표를 적고(Desired State), **통신관(kube-apiserver)**을 통해 **부관들(Controller)**에게 임무를 나누고, **조타수(scheduler)**가 돛을 펴며, **선원(kubelet)**이 실제로 노를 젓는다. 부관이 주기적으로 망원경으로(List-Watch) 현재 위치를 확인해 좌표와 다르면 즉시 보정한다(Reconciliation).

---

## Ⅲ. 비교 및 연결

### 오케스트레이터 비교

| 구분 | **Kubernetes (CNCF)** | **Docker Swarm** | **Apache Mesos + Marathon** | **HashiCorp Nomad** |
| :--- | :--- | :--- | :--- | :--- |
| 아키텍처 | 선언적, Control Plane + Node, CRD 확장 | 명령형(`docker service create`), Manager/Worker | Two-Level(Framework + Offer), Zookeeper 기반 | 단일 바이너리(Server+Client), Raft 합의 |
| 스케일 한계 | **5,000 노드 / 150,000 Pod / 300,000 컨테이너**(v1.30 기준) | 1,000 노드 / 50,000 컨테이너 권장 | 50,000+ 노드(Mesos 자체), Marathon 수천 | 10,000+ 잡(Job), 경량 |
| 스케줄링 | Filter->Score 2단계, 확장 플러그인 30+ | Spread/Constrain/Random/Resource Binpack | Role + Attribute + Offer(리소스 거버넌스 강점) | Binpack/Spread, Consul 연동 Service Discovery |
| 생태계 | **CRD·Operator·CNI·CSI·CNI·Ingress·ServiceMesh·GitOps** 모두 CNCF | Docker Stack, Traefik, Portainer | Chronos/Marathon LB, Spark·HDFS 통합 강점 | Consul·Vault·Terraform과 **HashiCorp