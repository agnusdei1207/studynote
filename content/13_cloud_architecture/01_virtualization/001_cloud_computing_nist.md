---
title: "NIST"
date: "2026-05-09"
tags:
  - "cloud_architecture"
  - "studynote-cloud-architecture"
weight: 1
---
```markdown
# 1. 클라우드 컴퓨팅 (Cloud Computing) 5대 특징 (NIST 기준)

> 참고 표준: **NIST SP 800-145** (National Institute of Standards and Technology, Special Publication 800-145, "The NIST Definition of Cloud Computing", 2011.09)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NIST SP 800-145가 정의한 클라우드 컴퓨팅의 5대 필수 특성(Essential Characteristics)은 ①On-demand Self-Service, ②Broad Network Access, ③Resource Pooling, ④Rapid Elasticity, ⑤Measured Service으로, 클라우드가 단순한 "원격 서버"가 아닌 **"탄력적·계량적·자동화된 다중 사용자 자원 추상화 계층"**임을 규정하는 기술적 판별 기준이다.
> 2. **가치**: 5대 특성을 충족할 때 평균 CAPEX 30~60% 절감, 자원利用率(Utilization) 10~20% -> 60~80%로 향상, 프로비저닝 시간 수 주 -> 수 분/초로 단축, AWS·Azure·GCP 모두 99.9~99.99% SLA와 사용량 기반 종량제(Pay-as-you-go)를 제공하여 TCO 최적화와 비즈니스 민첩성(Agility)을 동시에 달성한다.
> 3. **판단 포인트**: 5대 특성을 100% 충족하지 못하는 시스템(예: 수동 티켓 기반 VM 발급, 단일 테넌트 전용호스트, 정적 과금)은 **"클라우드 컴퓨팅"이라 부르기 어렵다**는 점이 핵심. 학습 정리에서는 "어느 한 특성이 누락되면 NIST 정의상 클라우드가 아니다"라는 엄격한 기준을 적용해 On-Premise 가상화, Managed Hosting, 전통적 Outsourcing과의 차이를 명확히 기술해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 NIST 표준 제정의 배경

2000년대 후반, Salesforce(1999), AWS(2006), Google App Engine(2008), Microsoft Azure(2010) 등 다양한 형태의 클라우드 서비스가 폭발적으로 등장하면서 시장 내 용어 혼란과 벤더 종속(Vendor Lock-in) 우려가 극심했다. 이에 미국 NIST는 2011년 9월 **SP 800-145**에서 클라우드 컴퓨팅의 표준 정의를 발표했고, 이는 ISO/IEC 22123-1, 22123-2, ITU-T Y.3500 등의 국제표준으로 채택되었다.

NIST는 클라우드 컴퓨팅을 **"공유 가능한 구성 가능한 컴퓨팅 자원(네트워크, 서버, 스토리지, 애플리케이션, 서비스)의 무제한·항상 이용 가능한·온디맨드 네트워크 접근을 가능하게 하는 모델로, 최소한의 관리 노력이나 서비스 제공자 상호작용으로 자원을 신속히 확보·공급할 수 있는 모델"**로 정의하며, 이 정의를 만족하기 위해 반드시 충족해야 할 **5대 필수 특성(Essential Characteristics)**을 명시했다.

### 1.2 기존 IT 패러다임의 한계

| 기존 패러다임의 문제점 | 기술적 원인 | 클라우드 5대 특성의 해결 |
| :--- | :--- | :--- |
| **낮은 자원 활용률 (10~20%)** | 서버·스토리지의 정적 할당 (Peak 기준 과다 설계) | Resource Pooling + Rapid Elasticity로 다중 테넌트 통합 |
| **긴 프로비저닝 시간 (수 주)** | 수동 설치, 티켓 기반 워크플로우 | On-demand Self-Service로 API 자동화 |
| **과금의 불투명성** | 정액제 라이선스, Capex 일시불 | Measured Service로 사용량 기반 과금 |
| **제한적 접근성** | 사내 LAN, VPN, 전용선 | Broad Network Access로 표준 프로토콜 기반 범용 접근 |
| **탄력성 부재** | 하드웨어 스케일링 비용/시간 부담 | Rapid Elasticity로 수 분 내 Auto Scaling |

### 1.3 클라우드 컴퓨팅 정의 구조 (NIST 3축 모델)

```text
+-----------------------------------------------------------------------------+
|                  NIST SP 800-145 : Cloud Computing 3축 모델                 |
+-----------------------------------------------------------------------------+

                          +-------------------------+
                          |    5대 필수 특성          |
                          |   (Essential            |
                          |    Characteristics)      |
                          |   <----- 이 문서의 범위    |
                          +------------+------------+
                                       |
                                       v
        +------------------+   +------------------+   +------------------+
        |   Service        |   |  Cloud Computing |   |   Deployment     |
        |   Models         |   |                  |   |   Models         |
        |   (서비스 모델)   |   |   (정의 자체)     |   |   (배치 모델)     |
        +--------+---------+   +------------------+   +--------+---------+
                 |                                              |
        +--------+---------+                          +---------+--------+
        |  Software-as-a-  |                          |  Public Cloud    |
        |  Service(SaaS)   |                          |  (AWS, Azure,    |
        +------------------+                          |   GCP, Naver)    |
        |  Platform-as-a-  |                          +------------------+
        |  Service(PaaS)   |                          |  Private Cloud   |
        +------------------+                          |  (OpenStack,     |
        |  Infrastructure- |                          |   VMware on-prem)|
        |  as-a-Service    |                          +------------------+
        |  (IaaS)          |                          |  Hybrid Cloud    |
        +------------------+                          |  (AWS Outposts,  |
                                                     |   Azure Arc)     |
                                                     +------------------+
                                                     |  Community Cloud |
                                                     +------------------+
```

- **📢 섹션 요약 비유**: 5대 필수 특성은 클라우드라는 "자동차"의 **5가지 연료 주입장치**와 같다. 하나라도 작동하지 않으면 시동을 걸 수 없다. 5대 특성이 모두 갖춰져야야 "클라우드"라 부를 수 있고, 하나라도 빠지면 그저 "가상화된 데이터센터"일 뿐이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 5대 필수 특성 (Essential Characteristics) 상세

NIST SP 800-145 §2가 명시한 5대 특성은 상호 의존적이며, 클라우드 서비스 제공자(Cloud Service Provider, CSP)의 내부 아키텍처(Control Plane, Data Plane)와 사용자 인터페이스(Portal, API, SDK)에 의해 구현된다.

```text
+---------------------------------------------------------------------------+
|              5대 필수 특성의 계층적 아키텍처 매핑 (CSP 내부)                |
+---------------------------------------------------------------------------+

   +------------------- User Plane ----------------------+
   |  Console / Portal  <--- Broad Network Access --+     |
   |  (HTML5 SPA, MFA)                              |     |
   |                                                 |     |
   |  REST API / CLI / SDK <--- On-demand Self- ---+|     |
   |  (OpenAPI 3.0, gRPC)         Service         ||     |
   +------------------------------------------------++-----+
                                                    ||
   +------------------- Control Plane ---------------++-----+
   |                                                 vv     |
   |  +-------------------------------------------------+  |
   |  | Service Catalog / Orchestrator (Terraform,       |  |
   |  | AWS CloudFormation, Azure ARM, GCP Deployment Mgr)|  |
   |  +--------+---------------------+-----------------+  |
   |           |                     |                    |
   |  +--------v--------+  +---------v--------+           |
   |  | Resource Pool   |  | Elasticity Mgr   |           |
   |  | (Hypervisor /   |  | (Auto Scaling    |           |
   |  |  Container      |  |  Group, HPA/VPA, |           |
   |  |  Orchestrator)  |  |  KEDA, Karpenter)|           |
   |  | <--- Resource    |  | <--- Rapid        |           |
   |  |     Pooling     |  |     Elasticity   |           |
   |  +-----------------+  +------------------+           |
   |                                                       |
   |  +---------------------------------------------+     |
   |  | Metering / Billing Engine (Usage Records)   |     |
   |  | <--- Measured Service                       |     |
   |  | (CloudWatch, Azure Monitor, Cloud Billing API)|  |
   |  +---------------------------------------------+     |
   +-------------------------------------------------------+
   +------------------- Data Plane ----------------------+
   |   물리 서버 (x86, ARM/Graviton), NVMe/SSD,         |
   |   100/200/400 Gbps Fabric, SmartNIC/DPU             |
   +------------------------------------------------------+
```

### 2.2 각 특성별 핵심 메커니즘

#### ① On-demand Self-Service (온디맨드 셀프서비스)

사용자가 **CSP와의 인간 상호작용(티켓, 전화, 메일) 없이** 필요한 컴퓨팅 자원(CPU, Memory, Storage, Network, SaaS 등)을 자동으로 비대화형으로 프로비저닝·해제할 수 있어야 한다. 구현은 **Self-Service Portal + API**로 이루어지며, 내부적으로는 Orchestrator가 IaC(Infrastructure as Code) 기반으로 자원을 자동 발급한다.

| 구현 계층 | 기술 | 동작 |
| :--- | :--- | :--- |
| **사용자 인터페이스** | Web Console, Mobile App | GUI 기반 클릭 -> API 호출 |
| **API 계층** | RESTful API, gRPC, GraphQL | `POST /vms`, `DELETE /vms/{id}` |
| **오케스트레이션** | Terraform, Pulumi, Ansible | 선언적 IaC (Desired State) |
| **CSP 내부 워크플로우** | Step Functions, Logic Apps, Cloud Workflows | 승인·검증->리소스 할당->메타데이터 등록 |

- **실무자 핵심 포인트**: 단순히 "셀프서비스 포털이 있다"는 것만으로는 부족하다. **"사전 정의된 매개변수(메모리·CPU·OS 이미지) 범위 내에서 비대화형 자동화가 가능한가"**가 핵심 판별 기준. 수동 승인 단계(Manual Approval)가 끼어 있으면 Self-Service의 본질이 훼손된다.

#### ② Broad Network Access (광대역 네트워크 접근)

자원은 **표준화된 프로토콜(HTTP/HTTPS, REST, SOAP, gRPC, AMQP, WebSocket 등)**을 통해 네트워크를 통해 접근 가능해야 하며, **다양한 클라이언트 디바이스(데스크톱, 노트북, 모바일, IoT, 태블릿, 씬 클라이언트, 워크스테이션)**에서 일관된 사용성을 보장해야 한다. 단, 네트워크 대역폭·지연시간(Latency)·보안 채널(TLS 1.3, mTLS)에 대한 보장은 CSP의 책임이다.

| 접근 채널 | 표준/프로토콜 | 예시 |
| :--- | :--- | :--- |
| **데이터 평면** | HTTPS (TCP 443), QUIC (443/UDP), mTLS | S3 API, Azure Blob Storage |
| **관리 평면** | REST + OAuth 2.0/OIDC + JWT | AWS Console API |
| **이벤트 스트리밍** | WebSocket, Server-Sent Events, MQTT | Kinesis Data Streams, Azure Event Grid |
| **고성능 RPC** | gRPC over HTTP/2 | 내부 서비스 간 통신 (Istio, Linkerd) |
| **사물인터넷** | CoAP, LoRaWAN Gateway | AWS IoT Core, Azure IoT Hub |

- **실무자 핵심 포인트**: Broad Network Access는 단순히 "인터넷으로 접근 가능"이 아니라, **(1)상호운용성(Interoperability)**, **(2)다중 디바이스 이식성(Portability)**, **(3)상호 운영 표준 준수(Open Standards)**를 포함. CSP가 독점 프로토콜·전용 단말만 허용하면 이 특성을 충족하지 못한다.

#### ③ Resource Pooling (자원 풀링)

CSP의 컴퓨팅 자원은 **다중 테넌트(Multi-Tenant)가 공유하는 풀(Pool)** 형태로 추상화·집중화되어야 하며, 사용자는 일반적으로 자원의 **물리적 위치(Region, Availability Zone, Data Center)를 통제하거나 알 필요 없이**, 지역·국가·전 세계 단위의 추상화된 논리적 위치(Logical Location) 개념만 인지하면 된다. **동적 자원 재할당(Dynamic Reassignment)**이 가능해야 하며, 이는 가상화(Hypervisor: KVM, Xen, Hyper-V, ESXi) 및 컨테이너 오케스트레이션(Kubernetes, Nomad)으로 구현된다.

| 풀링 차원 | 추상화 기술 | 동적 재할당 메커니즘 |
| :--- | :--- | :--- |
| **컴퓨트 (CPU/Mem)** | Type-1 Hypervisor(KVM), Para-virtualization | VM Live Migration (vMotion, Live Migration) |
| **컨테이너** | Linux cgroups, namespaces, Cgroup v2 | Pod Scheduling, Eviction, Bin-packing |
| **스토리지** | SDS(Software Defined Storage): Ceph, vSAN, MinIO | Storage vMotion, Thin Provisioning, Erasure Coding |
| **네트워크** | SDN (OpenFlow, OVS), NFV | VPC Peering, Network Slice, SR-IOV |
| **테넌트 격리** | VPC, Project, Subscription, Namespace | IAM Policy, Security Group, Network Policy |

- **실무자 핵심 포인트**: Resource Pooling의 반대 개념은 **Dedicated Hosting(전용 호스팅)** 또는 **Single-Tenant**이다. NIST 정의상 전용 호스팅은 이 특성을 충족하지 않으므로 클라우드가 아니다. 학습 정리에서 "단일 고객 전용 클라우드"라는 모순적 표현을 지적할 수 있어야 한다.

#### ④ Rapid Elasticity (신속한 탄력성)

자원은 **탄력적으로 제공·해제**될 수 있어야 하며, 수요 변동에 따라 **빠르게(outward/inward) 확장·축소**가 가능해야 한다. 사용자 관점에서 자원은 **무한정(Unlimited)**으로 보이는 것이 이상적이며, 이는 **Auto Scaling Group(ASG)**, **Horizontal Pod Autoscaler(HPA)**, **Cluster Autoscaler**, **Karpenter**, **KEDA**(Kubernetes Event-Driven Autoscaling) 등으로 구현된다.

```text
+-----------------------------------------------------------------+
|                  Rapid Elasticity 동작 흐름 (예: Web 3-tier)      |
+-----------------------------------------------------------------+

   사용자 트래픽
       ^
  10K -                ╱--╲                         (Auto Scale Out)
       |               ╱    ╲
   5K -        ╱------╱      ╲-----------          (Steady State)
       |       ╱
   1K -------╱                                  (Baseline)
       +-----------------------------------------> 시간
            Mon 09:00   Tue 10:00   Wed 12:00
