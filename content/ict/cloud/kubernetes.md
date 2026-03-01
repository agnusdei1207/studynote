+++
title = "쿠버네티스 (Kubernetes)"
date = 2025-03-01

[extra]
categories = "ict-cloud"
+++

# 쿠버네티스 (Kubernetes, K8s)

## 핵심 인사이트 (3줄 요약)
> **컨테이너를 자동으로 배포, 확장, 관리**하는 오케스트레이션 플랫폼. 선언적 설정, 자가 치유, 오토스케일링이 핵심. 구글이 개발, CNCF가 관리하는 오픈소스.

## 1. 개념
쿠버네티스(Kubernetes)는 **컨테이너화된 애플리케이션의 배포, 확장, 관리를 자동화**하는 오픈소스 플랫폼이다. "K8s"라고도 불린다.

> 비유: "컨테이너 오케스트라 지휘자" - 수많은 컨테이너를 조율하고 관리

## 2. 쿠버네티스 아키텍처

```
┌────────────────────────────────────────────────────────┐
│                쿠버네티스 클러스터 구조                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Control Plane (마스터 노드)                           │
│  ┌────────────────────────────────────────────────┐   │
│  │                                                │   │
│  │  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │ API Server  │  │ etcd        │             │   │
│  │  │ (진입점)    │  │ (저장소)    │             │   │
│  │  └─────────────┘  └─────────────┘             │   │
│  │                                                │   │
│  │  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │ Scheduler   │  │Controller  │             │   │
│  │  │ (스케줄링)  │  │Manager     │             │   │
│  │  └─────────────┘  │(제어루프)  │             │   │
│  │                   └─────────────┘             │   │
│  └────────────────────────────────────────────────┘   │
│                         │                             │
│  ───────────────────────┼───────────────────────────  │
│                         │                             │
│  Worker Nodes (워커 노드)                             │
│  ┌────────────────────────────────────────────────┐   │
│  │                                                │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │ kubelet │ │kube-proxy│ │Runtime │          │   │
│  │  │(에이전트)│ │(네트워크)│ │(컨테이너)│          │   │
│  │  └─────────┘ └─────────┘ └─────────┘          │   │
│  │                                                │   │
│  │  ┌───────────────────────────────────────┐    │   │
│  │  │              Pods                      │    │   │
│  │  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │    │   │
│  │  │  │Pod  │ │Pod  │ │Pod  │ │Pod  │     │    │   │
│  │  │  └─────┘ └─────┘ └─────┘ └─────┘     │    │   │
│  │  └───────────────────────────────────────┘    │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 3. 핵심 개념

```
┌────────────────────────────────────────────────────────┐
│                  쿠버네티스 핵심 리소스                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. Pod (파드)                                        │
│     - 가장 작은 배포 단위                             │
│     - 하나 이상의 컨테이너 그룹                       │
│     - 공유 IP, 스토리지                                │
│                                                        │
│  2. ReplicaSet (레플리카셋)                           │
│     - 파드 복제본 관리                                 │
│     - 지정된 수의 파드 유지                            │
│                                                        │
│  3. Deployment (디플로이먼트)                         │
│     - 롤링 업데이트 관리                               │
│     - 롤백 지원                                        │
│     - ReplicaSet 관리                                  │
│                                                        │
│  4. Service (서비스)                                   │
│     - 파드에 접근하기 위한 안정적인 엔드포인트         │
│     - ClusterIP, NodePort, LoadBalancer               │
│                                                        │
│  5. ConfigMap / Secret                                │
│     - 설정/민감정보 분리                               │
│     - 환경변수, 파일 마운트                            │
│                                                        │
│  6. Ingress (인그레스)                                 │
│     - HTTP/HTTPS 라우팅                               │
│     - 도메인 기반 라우팅                               │
│                                                        │
│  7. Namespace (네임스페이스)                           │
│     - 논리적 격리                                      │
│     - 리소스 쿼터 관리                                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 4. 코드 예시

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import uuid

class PodPhase(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNKNOWN = "Unknown"

class ServiceType(Enum):
    CLUSTER_IP = "ClusterIP"
    NODE_PORT = "NodePort"
    LOAD_BALANCER = "LoadBalancer"

@dataclass
class Container:
    """컨테이너"""
    name: str
    image: str
    ports: List[int] = field(default_factory=list)
    cpu_request: float = 0.1
    memory_request: str = "128Mi"

@dataclass
class Pod:
    """파드"""
    name: str
    namespace: str
    containers: List[Container]
    phase: PodPhase = PodPhase.PENDING
    pod_ip: Optional[str] = None
    node_name: Optional[str] = None

    def __post_init__(self):
        if self.pod_ip is None:
            self.pod_ip = f"10.{uuid.uuid4().int % 255}.{uuid.uuid4().int % 255}.{uuid.uuid4().int % 255}"

@dataclass
class Deployment:
    """디플로이먼트"""
    name: str
    namespace: str
    replicas: int
    containers: List[Container]
    pods: List[Pod] = field(default_factory=list)
    revision: int = 1

    def create_pods(self):
        """파드 생성"""
        for i in range(self.replicas):
            pod = Pod(
                name=f"{self.name}-{self.revision}-{i}",
                namespace=self.namespace,
                containers=self.containers
            )
            self.pods.append(pod)

@dataclass
class Service:
    """서비스"""
    name: str
    namespace: str
    selector: Dict[str, str]
    service_type: ServiceType
    ports: Dict[int, int]  # port: targetPort
    cluster_ip: Optional[str] = None

    def __post_init__(self):
        if self.cluster_ip is None:
            self.cluster_ip = f"10.{uuid.uuid4().int % 255}.{uuid.uuid4().int % 255}.{uuid.uuid4().int % 255}"

class KubernetesCluster:
    """쿠버네티스 클러스터 시뮬레이션"""

    def __init__(self):
        self.nodes: List[str] = []
        self.pods: Dict[str, Pod] = {}
        self.deployments: Dict[str, Deployment] = {}
        self.services: Dict[str, Service] = {}
        self.namespaces: List[str] = ["default"]

    def add_node(self, node_name: str):
        """노드 추가"""
        self.nodes.append(node_name)
        print(f"노드 추가: {node_name}")

    def create_deployment(self, name: str, namespace: str,
                          replicas: int, containers: List[Container]) -> Deployment:
        """디플로이먼트 생성"""
        deployment = Deployment(
            name=name,
            namespace=namespace,
            replicas=replicas,
            containers=containers
        )
        deployment.create_pods()

        # 파드 스케줄링
        for pod in deployment.pods:
            pod.node_name = self.nodes[len(pod.name) % len(self.nodes)]
            pod.phase = PodPhase.RUNNING
            self.pods[f"{namespace}/{pod.name}"] = pod

        self.deployments[f"{namespace}/{name}"] = deployment
        print(f"디플로이먼트 생성: {name} (replicas: {replicas})")
        return deployment

    def scale_deployment(self, name: str, namespace: str, new_replicas: int):
        """스케일링"""
        key = f"{namespace}/{name}"
        if key not in self.deployments:
            print("디플로이먼트를 찾을 수 없습니다")
            return

        deployment = self.deployments[key]
        current = len(deployment.pods)

        if new_replicas > current:
            # 스케일 아웃
            for i in range(current, new_replicas):
                pod = Pod(
                    name=f"{name}-{deployment.revision}-{i}",
                    namespace=namespace,
                    containers=deployment.containers
                )
                pod.node_name = self.nodes[i % len(self.nodes)]
                pod.phase = PodPhase.RUNNING
                deployment.pods.append(pod)
                self.pods[f"{namespace}/{pod.name}"] = pod

        elif new_replicas < current:
            # 스케일 인
            for pod in deployment.pods[new_replicas:]:
                pod.phase = PodPhase.FAILED
                del self.pods[f"{namespace}/{pod.name}"]
            deployment.pods = deployment.pods[:new_replicas]

        deployment.replicas = new_replicas
        print(f"스케일링: {name} → {new_replicas}개")

    def create_service(self, name: str, namespace: str,
                       selector: Dict[str, str], service_type: ServiceType,
                       ports: Dict[int, int]) -> Service:
        """서비스 생성"""
        service = Service(
            name=name,
            namespace=namespace,
            selector=selector,
            service_type=service_type,
            ports=ports
        )
        self.services[f"{namespace}/{name}"] = service
        print(f"서비스 생성: {name} ({service_type.value})")
        return service

    def get_pods(self, namespace: str = None) -> List[Pod]:
        """파드 목록"""
        if namespace:
            return [p for k, p in self.pods.items() if k.startswith(f"{namespace}/")]
        return list(self.pods.values())

    def describe_cluster(self):
        """클러스터 상태"""
        print(f"\n=== 클러스터 상태 ===")
        print(f"노드: {len(self.nodes)}개")
        print(f"파드: {len(self.pods)}개")
        print(f"디플로이먼트: {len(self.deployments)}개")
        print(f"서비스: {len(self.services)}개")


# 사용 예시
print("=== 쿠버네티스 시뮬레이션 ===\n")

cluster = KubernetesCluster()

# 노드 추가
cluster.add_node("worker-node-1")
cluster.add_node("worker-node-2")
cluster.add_node("worker-node-3")

# 디플로이먼트 생성
print("\n--- 디플로이먼트 생성 ---")
web_containers = [
    Container(name="nginx", image="nginx:1.21", ports=[80])
]
cluster.create_deployment("web-app", "default", 3, web_containers)

# 서비스 생성
print("\n--- 서비스 생성 ---")
cluster.create_service(
    "web-service", "default",
    selector={"app": "web"},
    service_type=ServiceType.LOAD_BALANCER,
    ports={80: 80}
)

# 스케일링
print("\n--- 스케일링 ---")
cluster.scale_deployment("web-app", "default", 5)

# 파드 상태
print("\n--- 파드 목록 ---")
for pod in cluster.get_pods():
    print(f"  {pod.name}: {pod.phase.value} @ {pod.node_name} ({pod.pod_ip})")

# 클러스터 상태
cluster.describe_cluster()
```

## 5. 쿠버네티스 YAML 예시

```yaml
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"

---
# Service
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
```

## 6. 쿠버네티스 기능

```
핵심 기능:

1. 오토스케일링
   - Horizontal Pod Autoscaler (HPA)
   - Vertical Pod Autoscaler (VPA)
   - Cluster Autoscaler

2. 롤링 업데이트
   - 무중단 배포
   - 카나리 배포
   - 블루-그린 배포

3. 자가 치유 (Self-Healing)
   - 파드 재시작
   - 노드 장애 시 재스케줄링
   - 헬스 체크

4. 서비스 디스커버리
   - DNS 기반 서비스 찾기
   - 환경변수 주입

5. 로드 밸런싱
   - 서비스 내 파드 분산
   - Ingress 기반 라우팅

6. 스토리지 오케스트레이션
   - PV/PVC
   - 스토리지 클래스
   - 동적 프로비저닝
```

## 7. 장단점

### 장점
| 장점 | 설명 |
|-----|------|
| 확장성 | 오토스케일링 |
| 가용성 | 자가 치유 |
| 이식성 | 멀티 클라우드 |
| 생태계 | 풍부한 도구 |
| 선언적 | GitOps 가능 |

### 단점
| 단점 | 설명 |
|-----|------|
| 복잡성 | 높은 학습 곡선 |
| 비용 | 리소스 오버헤드 |
| 운영 | 전문 인력 필요 |
| 디버깅 | 어려운 문제 해결 |

## 8. 실무에선? (기술사적 판단)
- **대규모**: 쿠버네티스 필수
- **소규모**: ECS, Cloud Run 검토
- **관리형**: EKS, GKE, AKS 활용
- **Serverless**: Knative, FaaS 검토

## 9. 관련 개념
- 컨테이너
- 마이크로서비스
- 서비스 메시
- GitOps

---

## 어린이를 위한 종합 설명

**쿠버네티스는 "컨테이너들의 반장님이에요!"**

### 무엇을 하나요? 👮
```
컨테이너가 많아지면:
- 누가 어디 있지?
- 몇 개를 돌리지?
- 고장나면 어떡하지?

쿠버네티스가 다 해줘요!
```

### 주요 일들 📋
```
스케줄링: "너는 1번 서버!"
모니터링: "아파? 다시 시작해!"
스케일링: "사람 많다! 더 만들어!"
업데이트: "조금씩 바꿔!"
```

### 용어들 📚
```
Pod: 컨테이너 그룹
Deployment: 배포 계획
Service: 전화번호 같은 것
Namespace: 반/학년 같은 것
```

**비밀**: 8글자 사이에 k와 s 사이에 8글자라서 K8s예요! ⛵✨
