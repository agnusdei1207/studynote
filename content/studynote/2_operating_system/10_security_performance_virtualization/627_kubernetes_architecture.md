+++
title = "627. 오케스트레이션 (Orchestration) - 쿠버네티스(Kubernetes) 아키텍처"
date = "2026-03-14"
weight = 627
+++

# 627. 오케스트레이션 (Orchestration) - 쿠버네티스(Kubernetes) 아키텍처

#### 핵심 인사이트 (3줄 요약)
> 1. **본질 (Definition)**: 쿠버네티스(Kubernetes, K8s)는 선언적 API(Declarative API)를 기반으로 컨테이너 워크로드의 배포, 확장, 관리를 자동화하는 분산 시스템 오케스트레이션 플랫폼입니다. 단순한 컨테이너 관리를 넘어 'Desired State(원하는 상태)'와 'Current State(현재 상태)' 간의 지속적인 동기화를 통해 시스템의 안정성을 보장합니다.
> 2. **가치 (Value)**: 구글의 Borg 시스템에서 검증된 대규모 서비스 운영 노하우를 오픈 소스화하여, 온프레미스와 퍼블릭 클라우드를 아우르는 하이브리드 클라우드(Hybrid Cloud) 환경을 제공합니다. 이를 통해 기업은 인프라의 추상화(Abstraction)를 달성하고, 가용성(Availability 99.9%+)을 보장하는 복원력 있는 아키텍처를 구축할 수 있습니다.
> 3. **융합 (Convergence)**: MSA(Microservices Architecture, 마이크로서비스 아키텍처)의 표준 배포 환경으로 자리 잡았으며, CI/CD(Continuous Integration/Continuous Deployment) 파이프라인과 연동하여 'GitOps'라는 새로운 운영 패러다임을 구현합니다. 또한, 서버리스(Serverless) 컴퓨팅과의 경계를 허물며 클라우드 네이티브(Cloud Native) 생태계의 중심에 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 개념 및 철학
오케스트레이션(Orchestration)이란 단순히 여러 개의 프로세스를 실행하는 '코디네이션(Coordination)'과 달리, 복잡한 분산 시스템의 상태를 관리하고 조율하는 상위 개념입니다. 쿠버네티스는 그리스어로 '조종사(Pilot)' 또는 '헬리킵터(Helmsman)'를 의미하며, 이름에서 알 수 있듯이 컨테이너라는 '배들의 함대'를 안전하게 목적지까지 이끄는 역할을 담당합니다.

기존의 가상머신(VM) 기반 가상화가 하이퍼바이저(Hypervisor)를 통해 하드웨어를 추상화했다면, 쿠버네티스는 OS 레벨의 가상화를 제공하는 컨테이너 위에서 **'논리적 호스트(Logical Host)'**를 추상화합니다. 즉, "어떤 서버에 앱을 설치할 것인가"라는 명령형(Imperative) 사고에서 "시스템이 이렇게 돌아가야 한다"는 선언형(Declarative) 사고로의 전환을 핵심 철학으로 삼습니다.

### 2. 등장 배경 및演进
1.  **기존 한계 (Pre-K8s Era)**: 도커(Docker)의 등장으로 컨테이너 기술이 보편화되었으나, 수백, 수천 개의 컨테이너를 수동으로 관리하는 것은 불가능에 가까웠습니다. 서비스 디스커버리(Service Discovery), 로드 밸런싱(Load Balancing), 죽은 프로세스의 재시작(Self-healing) 등을 개별적으로 스크립트로 관리해야 하는 '스크립트 헬(Script Hell)'에 빠지게 되었습니다.
2.  **혁신적 패러다임 (Borg Legacy)**: 구글은 15년 이상 Borg라는 내부 시스템을 통해 수십억 개의 컨테이너를 관험했습니다. 이 경험을 바탕으로 2014년 쿠버네티스 프로젝트를 오픈 소스로 공개하며, 엔터프라이즈급 컨테이너 오케스트레이션의 표준을 제시했습니다.
3.  **현재의 비즈니스 요구**: 클라우드 네이티브(Cloud Native) 컴퓨팅 재단(CNCF)의 채택으로 사실상의 업계 표준(De Facto Standard)이 되었으며, 멀티 클라우드(Multi-cloud) 전략과 엣지(Edge) 컴퓨팅 환경까지 확장되고 있습니다.

### 3. 기술적 핵심 (Control Loop)
쿠버네티스의 모든 동작은 **제어 루프(Control Loop)** 메커니즘으로 설명할 수 있습니다.

```text
   +--------------------------------------------------+
   |             Kubernetes Control Plane             |
   |                                                  |
   |  (1) Desired State   +--------+   (2) Watch      |
   |  (YAML Manifest) --->| API    |---------------+  |
   |  User defines 3 Reps | Server |                v  |
   |                      +--------+       +--------------+
   |                                         |   Controllers|
   |  (5) Reconcile Action                   |  (Decision)  |
   |  <--------------------------------------+              |
   |          |                                             |
   |          | (3) Current State                          |
   |          +---------------------------------------->   |
   |                                                  |   |
   |                                        (4) Cluster State|
   |                                       +-----------------+
   |                                       |
   +-------------------------------------------------------+
```

1.  **선언(Declare)**: 사용자가 `api-server`를 통해 YAML 파일로 "Nginx 3개를 띄워라(Desired State)"라고 선언합니다.
2.  **감시(Watch)**: `Controller Manager`는 API 서버를 모니터링하며 현재 클러스터 상태를 감시합니다.
3.  **관찰(Observe)**: 현재 노드에 실제로 구동된 컨테이너가 2개(Current State)임을 발견합니다.
4.  **비교 및 조정(Reconcile)**: 3개가 되어야 하는데 2개이므로 1개가 부족하다고 판단합니다.
5.  **행동(Act)**: `Scheduler`에게 새로운 Pod 생성을 요청하고, `kubelet`이 이를 실행하여 상태를 맞춥니다.

📢 **섹션 요약 비유**: 쿠버네티스는 **'만 명의 출퇴근길을 제어하는 AI 교통 제어 시스템'**과 같습니다. 운전자(개발자)가 "집으로 가고 싶다"는 목적지만 입력하면, 시스템이 실시간 교통 상황(현재 상태)을 보며 도로가 막히면 우회 도로로 자동으로 경로를 재설정(자동 치유)하여 목적지까지 안전하게 데려다줍니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 분산 시스템 구조 (Architecture Overview)
쿠버네티스 클러스터는 크게 **제어 평면(Control Plane, 마스터 노드)**과 **워커 노드(Worker Node)**로 분리됩니다. 이러한 분리는 관리 로직과 실제 워크로드의 물리적/논리적 격리를 보장합니다.

```text
      [ External User / kubectl Client ]
                |
                v (REST API / HTTPS)
+-----------------------------------------------------------------------+
|                     CONTROL PLANE (Master Node)                       |
|                                                                       |
|  +----------------+    +------------------+    +------------------+  |
|  |  API Server    |<-->|   etcd (Key-Val) |<-->| Cloud Controller |  |
|  | (Authn/Authz)  |    |   (State Store)  |    |   Manager (CCM)  |  |
|  +-------+--------+    +------------------+    +------------------+  |
|          ^                                                  ^         |
|          | Watch/Listen                                     |         |
|          v                                                  |         |
|  +----------------+    +------------------+                  |         |
|  |   Scheduler    |    | Controller Mgr   |                  |         |
|  | (Bin Packing)  |    | (Loops/Operators)|                  |         |
|  +-------+--------+    +------------------+                  |         |
|          |                                                 |          |
+----------|-------------------------------------------------|----------+
           |                                                 |
           | (1) Assign Pod                                  |
           | (2) Manifest Sync                               |
           |                                                 |
+----------|-------------------------------------------------|----------+
|          v             W O R K E R   N O D E              |          |
|  +-----------------------------------------------------+  |          |
|  | Kubelet (Agent)               Container Runtime      |  |          |
|  | +---------------------------+  +--------------------+ |  |          |
|  | | Pod (c1)      | Pod (c2)  |  |    Docker/Contd    | |  |          |
|  | | +---------+   | +-----+   |  | (runc/containerd)  | |  |          |
|  | | | Nginx   |   | | Redis|  |  +--------------------+ |  |          |
|  | | +---------+   | +-----+   |                           |  |          |
|  | +---------------------------+                           |  |          |
|  +-----------------------------------------------------+  |          |
|  | kube-proxy (Network Rules / IPVS/Iptables)            |  |          |
|  +-----------------------------------------------------+  |          |
+-----------------------------------------------------------------------+
```

### 2. 핵심 구성 요소 상세 분석 (Table)

| 구성 요소 (Component) | 분류 | 역할 및 책임 (Responsibility) | 내부 동작 메커니즘 (Mechanism) |
|:---|:---|:---|:---|
| **API Server** | Control Plane | 클러스터의 **게이트키퍼(Gatekeeper)**이자 유일한 통신 관문. | 사용자 요청을 인증(AuthN), 인가(AuthZ)한 후 `etcd`에 저장하고, 다른 컴포넌트들은 `API Server`를 통해만 데이터를 조회(Watch)함. |
| **etcd** | Control Plane | **분산 키-값 저장소(Distributed KV Store)**. 클러스터의 모든 상태(State)를 저장하는 뇌. | Raft 합의 알고리즘을 사용하여 데이터 일관성 보장. 리더 선출과 로그 복제를 통해 고가용성(HA) 유지. |
| **Scheduler** | Control Plane | **포드 배치 스케줄러**. 새로 생성된 Pod를 어느 노드에 배치할지 결정. | 예측(Prediction) 과정을 통해 리소스 여유, 하드웨어 제약, 선호도(Affinity) 등을 계산하여 최적의 노드에 배치(바이닝 패킹). |
| **Controller Manager** | Control Plane | **상태 유지 관리자**. 노드, 복제본(RS), 네임스페이스 등을 감시. | "Desired State"와 "Current State"를 끊임없이 비교하는 제어 루프(Reconciliation Loop)를 실행. |
| **kubelet** | Worker Node | **마스터의 대리인**. 노드 내에서 Pod 생명주기 관리. | API Server로부터 할당된 Pod 매니페스트를 받아 `CRI`(Container Runtime Interface)를 통해 컨테이너 런타임에 실행 명령을 내림. |
| **kube-proxy** | Worker Node | **네트워크 프록시**. 서비스(Service) 디스커버리 및 로드 밸런싱 담당. | 노드의 `iptables` 또는 `IPVS` 테이블을 조작하여 Service VIP에 접속하는 트래픽을 적절한 Pod로 전달(forwarding). |

### 3. 핵심 오브젝트 모델 (Object Model)
쿠버네티스는 "Pod 위주의 설계(Pod-Centric Design)"를 따릅니다.

```text
+---------------------------------------------------------------+
| [ Namespace ] (Logical Cluster Partition)                     |
|                                                               |
|  +-------------------------+      +------------------------+  |
|  | [ Deployment ]          |      | [ Service ]            |  |
|  | - Desired Replicas: 3   |<---->| - Type: LoadBalancer   |  |
|  | - Selector: app=web     |      | - Selector: app=web    |  |
|  +----------+--------------+      +-----------+------------+  |
|             |                                    |           |
|             | Creates/Manages                    | Routes    |
|             v                                    v           |
|  +---------------------------------------------------------+  |
|  | [ ReplicaSet ] (Ensures 3 Pods exist)                   |  |
|  |  +-------+   +-------+   +-------+                      |  |
|  |  | Pod 1 |   | Pod 2 |   | Pod 3 |                      |  |
|  |  | 10.x.1|   | 10.x.2|   | 10.x.3| <--- Shared IP(LAN)  |  |
|  |  +-------+   +-------+   +-------+                      |  |
|  +---------------------------------------------------------+  |
+---------------------------------------------------------------+
```

1.  **Pod**: 쿠버네티스의 **최소 배포 단위**. 하나 이상의 컨테이너(주로 Main App + Sidecar)와 공유 리소스(Storage, Network)를 포함. `Pause` 컨테이너가 네임스페이스를 생성하여 컨테이너 간 통신을 `localhost`로 가능하게 함.
2.  **ReplicaSet**: Pod의 복제본 개수를 보장하는 컨트롤러. (직접 작성보다는 Deployment에 의해 관리됨)
3.  **Deployment**: Pod와 ReplicaSet의 관리자. 배포 전략(RollingUpdate, Recreate)을 제어하고, 버전 롤백(Rollback) 기능을 제공.
4.  **Service**: Pod의 IP는 동적으로 변하므로, 이를 추상화한 **고정된 접속점(Virtual IP)**을 제공. `kube-proxy`에 의해 로드 밸런싱됨.

### 4. 핵심 알고리즘: 스케줄링 (Scheduling Logic)
스케줄러는 필터링(Filtering)과 점수 매기기(Scoring)의 2단계 프로세스를 거쳐 노드를 선택합니다.

```text
Function Schedule(pod):
  1. Filter Nodes:
     feasibleNodes = []
     for node in allNodes:
       if CheckPredicates(node, pod):  // 리소스 여부, 포트 충돌, affinity 체크
         feasibleNodes.add(node)
  
  2. Score Nodes:
     bestNode = null
     maxScore = -Infinity
     for node in feasibleNodes:
       score = CalculatePriority(node, pod) // 리소스 남은 정량, Zone 분산 등
       if score > maxScore:
         bestNode = node
         maxScore = score
  
  return bestNode
```

📢 **섹션 요약 비유**: 마스터 노드는 **'중앙 제어 타워'**이고 워커 노드는 **'화물 운송선'**입니다. 중앙 제어 타워(API Server)는 화주(사용자)로부터 운송 명령(YAML)을 받으면, 대형 지도(etcd)에 현재 선박 위치를 기록하고, 통제관(Controller)이 배가 하나라도 침몰하면 즉시 예비선을 투입합니다. 배가 언제 어디서 자유롭게 드나들 수 있도록 항구 관리자(kube-proxy)가 차트를 그려놓는 것과 같습니다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 기술적 비교: 쿠버네티스 vs 도커 스웜 (Docker Swarm)

| 비교 항