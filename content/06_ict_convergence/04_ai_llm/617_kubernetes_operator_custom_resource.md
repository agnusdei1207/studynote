---
title: "Kubernetes Operator Custom Resource"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 617
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스 오퍼레이터 패턴은 **CRD(Custom Resource Definition)로 도메인별 API를 확장**하고, **컨트롤러(Reconciliation Loop)가 선언적 상태(desired state)를 실제 클러스터 상태(actual state)에 수렴**시키며, 최종적으로 **인간의 운영 지식(Operational Knowledge)을 코드로 패키징(Operator SDK, controller-runtime)**하여 1차/2차/3차 운영업무를 자동화하는 쿠버네티스 네이티브 SRE 패턴이다.
> 2. **가치**: 단순 배포 수준을 넘어 **Day-2 Operations 자동화**를 통해 평균 장애복구시간(MTTR)을 70% 이상 단축하고, **GitOps + CR 기반 선언적 운영**으로 수십~수백 개의 Stateful 워크로드(etcd, Kafka, PostgreSQL, Cassandra)를 단일 CR yaml로 셀프서비스(Self-Service)화 한다. CNCF 2024 조사 기준 운영 오퍼레이터 사용 기업은 평균 **인프라 운영 인력 40% 절감** 효과를 보고한다.
> 3. **판단 포인트**: **`operator-sdk` 기반 Go 직접 구현 vs `Helm-based Operator`(Ansible/Kotlin)**, **단일 CR vs 다중 CR/Composite Controller**, **`status` 서브리소스 + finalizer 사용 여부**, **`conversion webhook`을 통한 v1beta1->v1 마이그레이션 전략**, 그리고 **OLM(Operator Lifecycle Manager)을 통한 카탈로그 배포**와 RBAC/네임스페이스 격리 수준이 아키텍처 결정의 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

쿠버네티스는 처음 설계될 때부터 "**선언적(Declarative) API**"라는 철학 위에 세워졌다. `kubectl apply -f` 한 줄로 Deployment, Service, Ingress 같은 *내장 리소스(Built-in Resource)* 가 자동으로 desired state로 수렴한다. 그러나 현실의 분산 시스템 운영은 그보다 훨씬 복잡하다. **etcd 클러스터는 quorum 관리가 필요**하고, **Kafka는 broker 재분배·controller 선출·topic 파티션 rebalance**를 자동으로 처리해야 하며, **PostgreSQL은 streaming replication + WAL archiving + 자동 failover**를 지원해야 한다. 이러한 **"인간의 운영 노하우(Operational Knowledge)"**를 컨트롤러라는 형태로 코드화한 것이 바로 **오퍼레이터 패턴(Operator Pattern)** 이며, 이를 가능하게 하는 **확장 메커니즘**이 **CRD(Custom Resource Definition)와 CR(Custom Resource)** 이다.

기존에는 Helm Chart + Jenkins/GitLab CI/CD로 "Day-1(배포)"는 자동화되었지만, "**Day-2(스케일링, 업그레이드, 백업, 복구, 보안패치, 모니터링 통합)**"는 여전히 운영 엔지니어의 수작업에 의존했다. CR/오퍼레이터는 **도메인 지식을 컨트롤러의 reconcile() 함수에 인캡슐레이션**하여 이를 해결한다. 2016년 CoreOS가 처음 제안한 이 패턴은 2018년 Red Hat이 **Operator Framework(Operator SDK + OLM)** 를 오픈소스화하면서 산업 표준으로 자리잡았고, 현재 CNCF의 **cert-manager, ArgoCD, Prometheus Operator, Strimzi(Kafka), TiDB Operator, Crossplane, External Secrets Operator** 등 300+ 프로덕션 오퍼레이터가 활용 중이다.

```text
   +-------------------------------------------------------------------+
   |              쿠버네티스 API 확장성 계층 (Kubernetes Extensibility)  |
   +-------------------------------------------------------------------+
   |                                                                   |
   |   +--------------+   +--------------+   +------------------+    |
   |   |  Built-in    |   |  Aggregation |   |   CRD (OpenAPI)  |    |
   |   |  Resources   |   |  Layer (AA)  |   | apiextensions.k8s|    |
   |   |  Pod, Svc    |   | kube-apiserver|   |   .io/v1         |    |
   |   +--------------+   +--------------+   +--------+---------+    |
   |                                                   |              |
   |                  사용자 정의 API 리소스           |              |
   |                                                   v              |
   |   +----------------------------------------------------------+   |
   |   |  Custom Resource (CR) -- e.g. "kind: KafkaCluster"        |   |
   |   |  +------------+--------------+--------------+----------+  |   |
   |   |  | spec:      | status:      | metadata:    | apiVer..|  |   |
   |   |  |  replicas:3 | phase:Ready  | name: prod-  |  v1alpha1|  |   |
   |   |  |  version:3.6|  nodes:3     |   kafka      |  /kafka. |  |   |
   |   |  |  storage:  |  health:OK   |   namespace  |   strimzi|  |   |
   |   |  |   100Gi    |              |              |   .io    |  |   |
   |   |  +------------+--------------+--------------+----------+  |   |
   |   +----------------------------------------------------------+   |
   |                              |                                   |
   |                              v watch (Informer)                  |
   |   +----------------------------------------------------------+   |
   |   |  Controller (Reconciliation Loop) -- Operator             |   |
   |   |  +---------+  +---------+  +---------+  +-------------+ |   |
   |   |  | Observe |-> |  Diff   |-> |  Act    |-> |  Update     | |   |
   |   |  | (read)  |  |(desired |  |(create/ |  |  status     | |   |
   |   |  |         |  | vs act) |  | patch)  |  |             | |   |
   |   |  +---------+  +---------+  +---------+  +-------------+ |   |
   |   |   ---- workqueue --- event-driven --- requeue ----      |   |
   |   +----------------------------------------------------------+   |
   |                              |                                   |
   |                              v 관리 대상 워크로드                  |
   |   +----------------------------------------------------------+   |
   |   |  StatefulSet / Deployment / Service / PVC / ConfigMap … |   |
   |   |  + 외부 시스템 API (Cloud RDS, Vault, GitHub, PagerDuty)  |   |
   |   +----------------------------------------------------------+   |
   +-------------------------------------------------------------------+
```

기존 패러다임(**Helm/Jenkins/Ansible Tower**)은 "**명령형(Imperative) 절차 실행**"에 가까워 상태 추적이 어려웠고, **유휴(idle) 환경에서 수동 변경을 감지하지 못한다**. CR/오퍼레이터는 **etcd에 desired state를 영속화**하고, **Informer(shared cache + watch) 메커니즘**으로 어떤 변경(사용자 편집, 자동 스케일링, 장애 등)도 감지하여 동일 상태로 복귀시키는 **종결 시스템(Terminating System)** 이다. 이 점이 **GitOps** 와의 결합을 자연스럽게 만든다.

- **📢 섹션 요약 비유**: 전통적 운영은 **레고 조립 설명서를 사람이 매번 보며 조립하는 것**이고, CR/오퍼레이터는 **"완성된 작품 사진(desired state)"만 벽에 걸어두면, AI 카메라(컨트롤러)가 24시간 사진을 비교하며 빠진 조각을 자동으로 채워주는 스마트 작업실**과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

오퍼레이터는 크게 **CRD(스키마 등록) -> CR(데이터 인스턴스) -> Controller/Reconciler(상태 수렴) -> status 서브리소스(관측성) -> Webhook(정책/변환) -> OLM(배포/생명주기)** 의 6계층으로 구성된다. 각 계층의 동작 원리와 상호작용은 다음과 같다.

```text
                    쿠버네티스 클러스터 내부
   +------------------------------------------------------------+
   |                                                            |
   |   +---------------------+    kube-apiserver                |
   |   | kubectl apply -f    | -----------------------+         |
   |   | kafka-cluster.yaml  |                         v         |
   |   +---------------------+    +--------------------------+   |
   |                              |  CRD: KafkaCluster       |   |
   |                              |  apiextensions.k8s.io/v1 |   |
   |                              |  ---------------------   |   |
   |                              |   group: kafka.strimzi.io|   |
   |                              |   versions: [v1beta2]    |   |
   |                              |   scope: Namespaced      |   |
   |                              |   names: kind=KafkaCluster|  |
   |                              |   schema: openAPIV3Schema |   |
   |                              |   subresources:          |   |
   |                              |     status: {}           |   |
   |                              |     scale: …             |   |
   |                              |   conversion: …          |   |
   |                              +----------+---------------+   |
   |                                         |                   |
   |   +-------------------------------------v--------------+    |
   |   |  etcd  -->  Custom Resource (CR) 인스턴스 저장       |    |
   |   |   apiVersion: kafka.strimzi.io/v1beta2              |    |
   |   |   kind: KafkaCluster                                |    |
   |   |   metadata: {name: prod, ns: kafka}                 |    |
   |   |   spec: {replicas: 3, version: "3.6.1", …}          |    |
   |   +---------------------------------+------------------+    |
   |                                     | WATCH                  |
   |                                     v                        |
   |   +------------------------------------------------------+   |
   |   |  Operator Pod (Deployment) -- controller-runtime      |   |
   |   |  +-------------------------------------------------+ |   |
   |   |  | Manager -- leader election -- metrics :8443     | |   |
   |   |  |  +- Controller for KafkaCluster                  | |   |
   |   |  |  |   +- Reconciler.Reconcile(ctx, req)         | |   |
   |   |  |  |   |    +- Get CR -- Get Pods/PVC/ConfigMap   | |   |
   |   |  |  |   |    +- Diff (desired vs actual)           | |   |
   |   |  |  |   |    +- Apply StatefulSet / Service / PDB  | |   |
   |   |  |  |   |    +- Patch status.phase / conditions    | |   |
   |   |  |  |   |    +- return ctrl.Result{Requeue: true}  | |   |
   |   |  |  |   +- Predicate (GenerationChangedPredicate) | |   |
   |   |  |  |   +- Watches: Pod, PVC, Secret (EnqueueForOwner)| |   |
   |   |  |  +- Webhook Server :443                           | |   |
   |   |  |  |   +- ValidatingWebhook (CR 필드 검증)         | |   |
   |   |  |  |   +- MutatingWebhook (default 값, sidecar)    | |   |
   |   |  |  |   +- ConversionWebhook (v1beta1 ↔ v1 변환)   | |   |
   |   |  |  +- CertController (cert-manager 통합)            | |   |
   |   |  +-------------------------------------------------+ |   |
   |   +-------------------------+----------------------------+   |
   |                             |                                |
   |                             v create/update                   |
   |   +------------------------------------------------------+   |
   |   |  Pod / StatefulSet / PVC / Service / ConfigMap / …    |   |
   |   |  --> 실제 워크로드 구성                                |   |
   |   +------------------------------------------------------+   |
   |                                                            |
   |   +------------------------------------------------------+   |
   |   |  OLM (Operator Lifecycle Manager) 선택적 사용         |   |
   |   |   - ClusterServiceVersion(CSV) 배포                   |   |
   |   |   - CatalogSource -> Subscription -> InstallPlan        |   |
   |   |   - OperatorGroup (멀티 네임스페이스 격리)            |   |
   |   +------------------------------------------------------+   |
   +------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CRD (CustomResourceDefinition)** | 도메인 API의 **스키마 선언** | `apiextensions.k8s.io/v1` 리소스로 OpenAPI v3 스키마 정의. `spec.versions[]`에 served/storage 버전 명시, `subresources`에 `status: {}` 지정으로 spec/status 분리, `additionalPrinterColumns`로 `kubectl get` 출력 커스터마이즈. `scope: Namespaced \| Cluster` 결정. |
| **CR (Custom Resource)** | 원하는 상태의 **데이터 인스턴스** | YAML/JSON으로 작성. `metadata.generation`은 spec 변경 시 1씩 증가, `status.observedGeneration`은 컨트롤러가 마지막으로 읽은 generation. Reconcile 키는 `namespace/name` 페어. |
| **Controller (Reconciler)** | 상태 수렴을 수행하는 **컨트롤 루프** | `client-go`의 `Informer/Lister/WorkQueue`를 추상화한 `controller-runtime`의 `Reconcile(ctx, req) (Result, error)` 함수가 핵심. **idempotent(멱등성)** 보장 필수. `RequeueAfter: 5m` 또는 에러 시 즉시 재큐. |
| **Predicate & EventFilter** | **불필요한 Reconcile 트리거를 필터링** | `GenerationChangedPredicate`(spec만 변경 시), `ResourceVersionChangedPredicate`, `LabelChangedPredicate`, `OwnerReference` 기반 `EnqueueRequestForOwner` 조합. |
| **status subresource** | 컨트롤러의 **관측 결과 노출** | `subresources.status: {}`로 spec/status 분리 시 status는 `PUT /status` 권한 필요. `status.conditions[]` 배열에 `Type/Status/Reason/Message/LastTransitionTime` 표준화. |
| **Finalizer** | **삭제 전 cleanup 보장 메커니즘** | `metadata.finalizers: [kafka.strimzi.io/cleanup]` 등록 -> 삭제 시 `DeletionTimestamp` 세팅, 컨트롤러가 외부 자원(DB, bucket) 정리 후 finalizer 제거해야 실제 삭제 진행. 누락 시 고아(orphan) 발생. |
| **Webhook (Admission)** | **CR 유효성·기본값·버전 변환** | `MutatingWebhookConfiguration`으로 default 값 주입, `ValidatingWebhookConfiguration`으로 거부 정책. **Conversion Webhook**(여러 버전 운영 시)로 v1beta1 ↔ v1 자동 변환. 자체 CA 인증서 필요 -> `cert-manager` 또는 `controller-gen webhooks`로 자동 발급. |
| **OLM (Operator Lifecycle Manager)** | **오퍼레이터의 카탈로그·업그레이드·의존성 관리** | `ClusterServiceVersion(CSV)`에 `ownedAPIs`, `dependencies`, `install strategy(deployment/OLM-allnamespaces)` 기술. `OperatorHub`에서 community operator를 `Subscription`으로 구독. |

### 핵심 원리 — Reconciliation Loop의 수학적 의미

Reconcile 함수는 본질적으로 **고정점(Fixed Point) 알고리즘**이다. 클러스터의 실제 상태를 `A`, CR의 desired state를 `D`라 할 때, 컨트롤러는 다음을 반복한다:

```
repeat
    A := readActualStateFromKubeAPI(D)
    Δ := diff(D, A)
    if Δ = ∅ then return  // 수렴