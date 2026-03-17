+++
title = "821-832. 클라우드 네이티브와 서비스 메시 (CNI, Istio)"
date = "2026-03-14"
[extra]
category = "Data Center & Cloud"
id = 821
+++

# 821-832. 클라우드 네이티브와 서비스 메시 (CNI, Istio)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: **CNI (Container Network Interface)**는 컨테이너 네트워킹의 표준화된 플러그인 아키텍처이며, **서비스 메시 (Service Mesh)**는 마이크로서비스 간 통신의 로드밸런싱, 보안, 관측 가능성을 **사이드카 (Sidecar)** 패턴을 통해 처리하는 전용 인프라 계층이다.
> 2. **가치**: CNI는 컨테이너 생명주기에 맞춰 네트워크 자원을 동적으로 할당하여 **IPAM (IP Address Management)** 부하를 해소하고, 서비스 메시는 애플리케이션 코드 변경 없이 **mTLS (mutual TLS)** 및 트래픽 제어를 통해 안정적인 MSA (Microservices Architecture) 환경을 제공한다.
> 3. **융합**: 쿠버네티스(Kubernetes)의 **CNI** 플러그인(예: Cilium)과 서비스 메시(예: Istio)를 결합하여 L3/L4 네트워킹과 L7 트래픽 관리를 통합 관리하는 '백플레인(Backplane)' 네트워크 아키텍처가 표준으로 자리 잡고 있다.

+++

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 정의
**클라우드 네이티브 (Cloud Native)** 환경에서 수천 개의 **VM (Virtual Machine)** 대신 경량화된 컨테이너가 생성되고 소멸되는 과정은 기존 네트워킹 방식으로는 관리하기 불가능한 수준의 복잡도를 가집니다. 이를 해결하기 위해 등장한 핵심 기술이 **CNI (Container Network Interface)**와 **서비스 메시 (Service Mesh)**입니다.

*   **CNI (Container Network Interface)**: CNCF (Cloud Native Computing Foundation)에서 제정한 표준으로, 컨테이너 런타임(runc 등)과 네트워크 플러그인 사이의 API 규격입니다. 컨테이너 생성(`ADD`) 시 네트워크 네임스페이스 할당, IP 부여, 라우팅 설정을 수행하고, 삭제(`DEL`) 시 자원을 반납합니다.
*   **서비스 메시 (Service Mesh)**: 분산된 마이크로서비스 간의 통신(서비스-to-Service 통신)을 제어하는 전용 계층입니다. 애플리케이션 로직에 독립적으로 **L7 (Layer 7)** 로드밸런싱, 서킷 브레이킹(Circuit Breaking), **observability (관측 가능성)** 기능을 제공합니다.

#### 2. 등장 배경 및 기술적 패러다임
① **기존 한계**: 전통적인 **SDN (Software Defined Networking)** 방식은 노드 단위의 관리에 집중하였으나, MSA 도입으로 인해 '서비스' 단위의 세밀한 트래픽 제어와 보안(mTLS) 요구사항이 대두됨.
② **혁신적 패러다임**: 인프라의 복잡성을 애플리케이션에서 분리하여 '인프라 레이어'로 하향 시키는 **관심사의 분리 (Separation of Concerns)**. **iptables**나 **IPVS (IP Virtual Server)** 기반의 쿠버네티스 **kube-proxy**만으로는 한계가 있는 L7 트래픽 관리를 전용 프록시(Envoy 등)에게 위임.
③ **현재의 비즈니스 요구**: **제로 트러스트 (Zero Trust)** 보안 모델 구축을 위한 서비스 간 암호화 강제와, 카나리(Canary) 배포와 같은 정교한 릴리스 전략의 자동화 필요성.

#### 3. CNI 핵심 플러그인 비교
| 구분 | Flannel | Calico | Cilium |
| :--- | :--- | :--- | :--- |
| **동작 방식** | **VXLAN (Virtual Extensible LAN)** Overlay | **BGP (Border Gateway Protocol)** Routing / eBPF | **eBPF (Extended Berkeley Packet Filter)** in-kernel |
| **성능** | 중복 캡슐화로 인한 오버헤드 있음 | 라우팅 기반이므로 네이티브 성능 | 커널 레벨 처리로 매우 높은 성능 |
| **주요 특징** | 설정 단순, 소규모에 적합 | 강력한 **Network Policy** 지원 | L7 가시성, Hubble 등 통합 관찰 가능성 |
| **사용층** | 개발/테스트 환경 | 보안이 중요한 엔터프라이즈 | 대규모 고트래픽 생산 환경 |

```ascii
      [ CNI 플러그인 아키텍처 비교 ]

   1. Flannel (Overlay)          2. Calico (Routing)         3. Cilium (eBPF)
   +-------------+               +-------------+              +-------------+
   |   Pod 1     |               |   Pod 1     |              |   Pod 1     |
   | 10.244.1.2  |               | 192.168.1.2 |              | 10.244.1.2  |
   +------+------+               +------+------+              +------+------+
          |                              |                             |
          | (VXLAN Encap)                | (BGP Peer)                  | (Veth Hook)
          v                              v                             v
   +------+------+               +------+------|              +------+------+
   |   Node A    |               |   Node A    |              |   Node A    |
   | : tunbridge |               | : Bird BGP  |              | : eBPF Maps |
   +-------------+               +-------------+              +-------------+
        [성능: 낮음]                  [성능: 중간]                   [성능: 매우높음]
```

> **해설**:
> 위 다이어그램은 세 가지 대표적인 CNI의 네트워크 패킷 처리 방식을 도식화한 것입니다. Flannel은 패킷에 UDP 헤더를 덧씌워 터널링하는 오버레이 방식으로, CPU 오버헤드가 발생합니다. Calico는 노드 간 **BGP** 프로토콜을 통해 라우팅 테이블을 공유하여 패킷을 직접 라우팅합니다. Cilium은 리눅스 커널의 **eBPF**를 활용하여 패킷이 커널 공간을 통과할 때 사용자 공간으로 복사하는 비용 없이 즉시 처리하여 가장 우수한 성능을 보입니다.

📢 **섹션 요약 비유**: CNI는 신도시 아파트 단지(**클러스터**)가 건설될 때, 아파트(**컨테이너**)가 들어설 때마다 자동으로 수도관과 전선을 연결해 주는 '도시 기반 시설 공사팀'과 같습니다. Flannel은 지하에 관을 따로 매는 방식이고, Calico는 도로를 통해 직접 연결하는 방식입니다.

+++

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 서비스 메시 아키텍처: 사이드카 (Sidecar) 패턴
서비스 메시의 핵심은 **사이드카 컨테이너**를 각 마이크로서비스 **Pod** 안에 삽입하는 것입니다. 애플리케이션은 자신의 로컬 인터페이스(**localhost**)로 트래픽을 전송하고, 이를 사이드카 프록시(예: **Envoy**)가 가로채서 목적지로 전송합니다. 이를 **투명 프록시 (Transparent Proxy)**라 합니다.

#### 2. 구성 요소 및 상호작용
서비스 메시는 크게 **Data Plane(데이터 평면)**과 **Control Plane(제어 평면)**으로 나뉩니다.

| 요소명 | 역할 | 내부 동작 | 주요 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Envoy (사이드카)** | **Data Plane** | 실제 트래픽 처리(LB, Retry, TLS) | **HTTP/2**, gRPC, mTLS | 여권 검사대 직원 |
| **Istiod** | **Control Plane** | 설정 배포, 인증서 발급, 설정 검증 | **xDS API** (gRPC), **CA (Cert Auth)** | 여권 발행 본부 |
| **Pilot** | 유도 (Istiod 내부) | 서비스 디스커버리, 트래픽 규칙 전달 | **EDS**, **CDS**, **LDS** | 교통 통제 센터 |
| **Citadel** | 보안 (Istiod 내부) | mTLS 인증서 발급 및 회전 | **gRPC**, TLS | 보안 관리국 |
| **Galley** | 설정 (Istiod 내부) | 설정 파싱 및 배포 | K8s Watch API | 청부 업무 대행 |

#### 3. 데이터 흐름 및 mTLS 동작 원리

```ascii
      [ 서비스 메시 내부 통신 흐름 (mTLS 적용 시 ) ]

   [ Pod A ]                      [ Control Plane ]                    [ Pod B ]
   +-------+            1. Config Fetch           +-------+
   | App A |--(127.0.0.1:8080)--------> Envoy A <-----------> Istiod (CA)
   +-------+            ^           |           |           +-------+
          |             |           |           |                ^
          v             |           v           |                |
       +-------+   2. Cert Issue   +-------+    | 3. Discovery  |
       |Envoy A |<--------------->|Envoy B |----+ (Cluster)      |
       +-------+   4. mTLS Tunnel +-------+    | (via Envoy)     |
            ^                         ^        |                 |
            |                         |        v                 |
            +---------( Encrypted )-------------------> ( decrypted )
          Outbound                  Inbound
            
   [ Step 1: Bootstrapping ]      [ Step 2: Traffic ]
   - Envoy A는 Istiod에 접속      - App A가 localhost로 요청
   - 인증서 및 트래픽 정책 수신    - Envoy A는 L7 라우팅 후 Envoy B로 전송
   - xDS 프로토콜(CDS/LDS) 수신    - Envoy B는 인증서 검증 후 App B로 전달
```

> **해설**:
> 1. **부트스트래핑(Bootstrapping)**: Envoy 프록시가 시작될 때 **Istiod**와 연결하여 자신의 역할과 트래픽 정책(LDS: Listener Discovery Service, CDS: Cluster Discovery Service)을 가져옵니다. 이때 **mTLS**에 필요한 인증서(SAN 등 포함)를 발급받습니다.
> 2. **트래픽 처리**: 애플리케이션은 목적지를 알 필요 없이 **localhost**로 요청을 보냅니다. 사이드카 프록시는 요청을 가로채어 **HTTP/2**로 변환하고, 목적지 서비스의 사이드카 프록시와 연결을 설정합니다. 이때 **mTLS** 핸드셰이크가 발생하여 **Identity**(SNI)를 검증하고, 패킷은 **AES** 등으로 암호화되어 전송됩니다. 수신 측 프록시는 복호화 후 로컬 애플리케이션에 전달합니다.

#### 4. 핵심 알고리즘: xDS (Discovery Service) 프로토콜
Istio는 제어부(Istiod)와 데이터부(Envoy) 간의 통신을 위해 gRPC 기반의 **xDS** API를 사용합니다.

*   **CDS (Cluster Discovery Service)**: "어떤 업스트림 서비스(Svc B)가 존재하는가?" (목적지 그룹 정의)
*   **EDS (Endpoint Discovery Service)**: "해당 서비스의 IP는 무엇인가?" (Pod의 실제 IP 목록, 동적 갱신)
*   **LDS (Listener Discovery Service)**: "어떤 포트(15001 등)를 리스닝할 것인가?" (리스너 설정)
*   **RDS (Route Discovery Service)**: "요청의 Header(Path)를 보고 어디로 라우팅할 것인가?" (L7 라우팅 규칙)

📢 **섹션 요약 비유**: 서비스 메시는 모든 직원(애플리케이션) 옆에 '개인 비서(사이드카)'를 붙여놓은 것과 같습니다. 직원은 단순히 비서에게 "이 사람에게 전해줘"라고 말만 하면, 비서는 상대방 비서와 암호 통신을 설정하고, 상대방이 바쁘면 기다렸다가 전달하고, 대화 내용을 다 기록하는 복잡한 잡무를 대신 처리합니다. **Istiod**는 이 모든 비서들을 교육하고 관리하는 '인사팀'입니다.

+++

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. Ingress vs Service Mesh vs CNI (심층 비교)
쿠버네티스 환경에서 트래픽이 진입하는 지점부터 내부 통신까지의 책임을 명확히 이해해야 합니다.

| 비교 항목 | **Ingress (L7 LB)** | **Service Mesh (East-West)** | **CNI (L3 Network)** |
|:---|:---|:---|:---|
| **처리 범위** | **North-South** (외부 ↔ 클러스터) | **East-West** (서비스 ↔ 서비스) | **Node-to-Pod**, **Pod-to-Pod** |
| **대표 도구** | **Nginx**, ALB, **GKE Ingress** | **Istio**, Linkerd | Calico, Cilium, Flannel |
| **L7 기능** | URL Routing, SSL Termination | Retry, Circuit Breaker, **Traffic Splitting** | 지원 안 함 (L3/L4 Only) |
| **성능 오버헤드** | 매우 낮음 (Edge 단일 지점) | 높음 (모든 Pod에 Proxy 존재) | 낮음 (Kernel/NIC Level) |
| **주요 목적** | 외부 트래픽 진입점 최적화 | MSA 통신 제어 및 관측 가능성 확보 | IP 할당 및 연결성 확보 |

```ascii
[ 트래픽 플로우 관점에서의 계층 구조 ]

    Internet
       ||
       \/
  +-----------+      (L7: Host/Path based Routing)
  | Ingress    | -----> [ terminates TLS, HTTP -> HTTP ]
  | Gateway    |      (Cluster Entry Point)
  +-----------+
       ||
       \/  (Service Mesh "East-West" Traffic Starts)
  +------------------------------------------+
  |  Data Plane (Service Mesh)               |
  |  Pod A -> [Sidecar] <-> [Sidecar] -> Pod B |
  |  (mTLS, Observability, Retry, LB)        |
  +------------------------------------------+
       ||
       \/  (CNI "Underlay" Traffic)
  +------------------------------------------+
  |  Network Layer (CNI Plugin)              |
  |  Node A (192.168.1.10) --- VPN/GRE ---> Node B |
  |  (IP Allocation, Routing, Encap)         |
  +------------------------------------------+
``