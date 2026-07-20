---
title: "Software Defined Everything SDx Abstraction"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 741
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SDx(Software Defined Everything)는 네트워크(SDN), 스토리지(SDS), 컴퓨팅(SDC), 보안(SD-Security) 등 모든 인프라 자원의 **제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리**하고, 이를 **추상화 계층(Abstraction Layer)**을 통해 API로 노출하여 프로그래머블하게 자원을 제어하는 패러다임이다. 핵심은 "인프라 자원의 가상화 + 중앙 집중화 + 자동화"의 3축 융합이다.
> 2. **가치**: CAPEX/OPEX 동시 절감(서버 가용률 12~18% -> 60~80%로 향상, IDC 비용 30~50% 감축), 배포 시간 **주(Month) 단위 -> 분(Minute) 단위**로 단축, 정책 기반 일관성 보장(Zero-Touch Provisioning), 벤더 종속 탈피(White-Box + Open API 기반 멀티벤더 통합).
> 3. **판단 포인트**: 추상화 수준 결정(Over-abstraction 시 제어 정밀도 저하·지연 증가 vs Low-abstraction 시 관리 복잡도 폭증), 동서/남북 트래픽 패턴 분석에 따른 컨트롤러 배치, 상태(State) 일관성 보장 알고리즘(RAFT, Paxos, Eventually Consistent) 선택, 그리고 **East-West API 거버넌스**(표준 준수율·버전 호환성·보안 경계)가 아키텍처 성패를 좌우한다.

---

## Ⅰ. 개요 및 필요성

전통적 IT 인프라(3-Tier 아키텍처, 하드웨어 어플라이언스, 수작업 CLI 구성)는 급증하는 트래픽, 멀티클라우드 워크로드, 마이크로서비스 기반 애플리케이션, 그리고 **Day-N 운영 부담**에 더 이상 대응하지 못한다. 2010년 Stanford의 **OpenFlow**(McKeown et al.) 논문으로 시작된 SDN은 "라우터/스위치의 두뇌를 외부 컨트롤러로 빼내자"는 단순한 발상에서 출발했지만, 이는 곧 스토리지·컴퓨팅·보안 영역으로 확산되며 **SDx**라는 통합 개념으로 진화했다.

SDx의 진정한 가치는 **추상화(Abstraction)**에 있다. 물리적 자원의 복잡성(케이블링, 디스크 RAID 레벨, NIC IRQ, ASIC 칩셋)을 숨기고, 개발자/운영자에게 **논리적·의도 기반(Intent-Based)** 인터페이스를 제공하는 것이 핵심이다. 가령, "Web 3-tier 서비스가 필요해"라고 선언하면(Declarative), 컨트롤러가 VLAN/VXLAN, BGP/EVPN, Ceph PG(Placement Group), Kubernetes Pod 스케줄링을 자동 조합해 즉시 자원을 조립한다.

```
[ 전통 인프라 vs SDx 패러다임 비교 ]

전통 인프라 (Static, Manual, Silo)                SDx (Dynamic, Programmable, Unified)
+------------------------------+               +--------------------------------------+
|  하드웨어 어플라이언스        |               |  White-Box HW + 범용 x86/ARM        |
|  +--------+ +--------+ +---+ |               |  +--------+ +--------+ +--------+  |
|  |방화벽  | |L4 스위치| |IPS| | ---> 진화 ---> |  |  OVS   | |vRouter | |vFW/vLB |  |
|  +--------+ +--------+ +---+ |               |  +--------+ +--------+ +--------+  |
|  펌웨어별 개별 CLI / GUI     |               |  단일 컨트롤러 + Open API            |
|  장비 추가 = 수주 도입       |               |  신규 자원 = 수초 할당              |
|  트래픽 증가 = HW 증설       |               |  트래픽 증가 = 자동 Scale-out       |
+------------------------------+               +--------------------------------------+
   CAPEX ^^  /  OPEX ^^  /  Time-to-Market ^       CAPEX v  /  OPEX vv  /  Time-to-Market vv
```

추가로, **Z세대 워크로드**(AI/ML 학습, IoT 스트리밍, 실시간 분석)는 **East-West 트래픽**(서버↔서버, Pod↔Pod)이 80% 이상을 차지하는 반면, 기존 L2/L3 아키텍처는 **North-South 트래픽**에 최적화되어 있다. 이 불일치를 해결하는 것이 SDx의 또 다른 동기다.

- **📢 섹션 요약 비유**: 전통 인프라가 **"벽에 못 박힌 형광등"**이라면, SDx는 **"디밍·색온도·ON/OFF를 앱으로 자유자재로 제어하는 스마트 조명 시스템"**과 같다. 조명 기구(하드웨어) 자체는 표준화하고, 빛의 방식(정책·동작)은 소프트웨어로 정의한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SDx의 4계층 아키텍처는 **IaaS(Infrastructure-as-a-Service)** 의 표준 참조 모델(IETF, ETSI NFV, ONF)을 기반으로 한다.

```
[ SDx 4-Layer 추상화 아키텍처 ]

   +-------------------------------------------------------------+
   |  ④ Application / Orchestration Layer                        |
   |     - vRealize / OpenStack Heat / Terraform / ArgoCD         |
   |     - Intent Engine (NL -> Policy Translation)                |
   |     - CI/CD, AIOps, CMDB 연동                                |
   +-------------------------------------------------------------+
   |  ③ Control & Orchestration Plane (SDN/SDS/SDC Controller)   |
   |     - OpenDaylight / ONOS / Kubernetes API Server            |
   |     - Ceph MON / OpenStack Cinder / vCenter                  |
   |     - Global View, 정책·토폴로지·상태 관리                   |
   |     - Northbound API (RESTCONF, gRPC) -> ④로                 |
   |     - Southbound API (OpenFlow, NETCONF, gNMI) -> ②로        |
   +-------------------------------------------------------------+
   |  ② Virtual / Abstract Resource Layer (추상화 핵심)          |
   |     - 가상 네트워크: VXLAN/EVPN, OVS, vRouter, NSX           |
   |     - 가상 스토리지: Ceph RBD, vSAN, Storage Policy          |
   |     - 가상 컴퓨팅: KVM/QEMU, ESXi, Container Runtime        |
   |     - 멀티테넌시, QoS, 보안 정책 적용                       |
   +-------------------------------------------------------------+
   |  ① Physical Infrastructure Layer                            |
   |     - White-Box Switch (Edgecore, Celestica, Dell EMC)     |
   |     - x86/ARM 서버, NVMe/SSD, 100G/400G NIC                  |
   |     - SONiC, Dell OS10, Cumulus, ONL (Open Network Linux)   |
   +-------------------------------------------------------------+
   ^ Northbound API             Southbound API v
   (정책/의도 전달)              (로우-레벨 디바이스 제어)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① 물리 인프라 계층 (Underlay)** | 자원의 물리적 제공 | White-Box 스위치(SONiC/DENT), x86/ARM 서버(NVMe-oF 지원), 100/400G 광 트랜시버. AS5712-54X, Edgecore AS7312-54X 등 OCP Accepted 하드웨어 |
| **② 추상화/가상화 계층 (Hypervisor/Virtualizer)** | 물리 자원의 논리적 분리 | 네트워크: OVS(Open vSwitch), Linux Bridge, SR-IOV, DPDK / 스토리지: Ceph, MinIO, vSAN / 컴퓨팅: KVM, QEMU, containerd, gVisor |
| **③ 제어 평면 (Controller/Orchestrator)** | 글로벌 뷰·정책·상태 관리 | SDN: OpenDaylight, ONOS, Faucet, Tungsten Fabric / SDS: Ceph MON, Rook / SDC: Kubernetes(kube-apiserver), OpenStack(Neutron/Cinder/Nova) |
| **④ 오케스트레이션/애플리케이션 계층** | 워크로드 라이프사이클, 의도 해석 | Terraform, Ansible, ArgoCD, Crossplane, vRealize Suite, NSP(Network Services Orchestrator) |

### 추상화의 핵심 메커니즘

**(1) 제어 평면/데이터 평면 분리 (Control-Data Plane Separation, CDPS)**
전통 L2 스위치는 **MAC 학습 -> 포워딩 테이블 갱신 -> 패킷 포워딩**을 단일 ASIC에서 수행(분산 제어). SDN은 이 중 학습·결정 로직을 컨트롤러로 이관하고, 스위치는 단순히 **"매칭 테이블에 따라 패킷을 옮겨라"**는 역할만 수행(집중 제어). OpenFlow 1.5는 **다중 테이블(Multi-Table Pipeline) + Group Table + Meter Table**을 지원해 L2~L4 처리를 정교화한다.

**(2) 추상화 단계 (Abstraction Ladder)**
```
  Lv.4  Intent (NL/Natural Language) : "내부 DB 트래픽은 암호화해줘"
  Lv.3  Policy (YAML/JSON)         : {"src":"db-tier", "dst":"app-tier", "action":"encrypt-gcm"}
  Lv.2  Model (Graph/Object)       : Neutron SecurityGroup, Calico NetworkPolicy
  Lv.1  Mechanism (Protocol)       : WireGuard, IPsec, MACsec, VXLAN-GBP
  Lv.0  Device (CLI/Chip)          : ip link, ovs-vsctl, ethtool
```
추상화 수준이 높을수록 **생산성·이식성**은 증가하지만, **세밀한 튜닝·저지연 제어**는 어렵다. 실무자는 **Intent -> Policy -> Mechanism** 변환 시 정보 손실(Loss of Fidelity)을 최소화하는 추상화 경계를 설계해야 한다.

**(3) 상태 일관성 모델 (State Consistency)**
분산 컨트롤러(예: ONOS의 3-Node Cluster, Kubernetes의 etcd RAFT quorum)는 **강일관성(Strong Consistency)** vs **최종일관성(Eventual Consistency)** 중 트레이드오프를 선택한다. 금융·통신 코어망은 **RAFT/Paxos 기반 강일관성**, 빅데이터·CDN은 **Eventually Consistent + Gossip Protocol**로 운용한다.

**(4) 데이터 평면 가속 (Data Plane Acceleration)**
추상화로 인한 성능 저하를 극복하기 위해 **DPDK(Data Plane Development Kit)**, **VPP(Vector Packet Processing)**, **eBPF/XDP**, **P4(Programming Protocol-independent Packet Processors)**, **SmartNIC(DPU/IPU: BlueField-3, Pensando, Mount Evans)** 가 사용된다. 특히 **P4**는 ASIC 재제조 없이 새로운 프로토콜을 파싱·처리할 수 있게 해, SDx의 **"프로그래머빌리티"** 사상을 데이터 평면까지 확장했다.

- **📢 섹션 요약 비유**: 4계층 아키텍처는 **"오케스트라"**와 같다. ①은 악기(바이올린, 첼로, 트럼펫), ②는 음역·파트 배치(악보의 보표), ③은 지휘자(컨트롤러, 모든 악보·템포·다이내믹을 총괄), ④는 작곡가·콘서트 마스터(오케스트레이터, 곡의 의도·해설을 담당). 청중은 ④의 해석(연주)을 듣지만, 그 소리는 ③->②->①을 거친 **추상화·구체화의 역방향 흐름**의 결과다.

---

## Ⅲ. 비교 및 연결

SDx는 단일 기술이 아니라 **유사 철학**을 공유하는 기술 군(群)이다. 핵심 구성요소별 비교는 다음과 같다.

| 구분 | **SDN (네트워크)** | **SDS (스토리지)** | **SDC / SDDC (컴퓨팅·데이터센터)** | **SD-WAN (WAN)** | **NFV (가상화 네트워크 기능)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **추상화 대상** | 패킷 포워딩 테이블, 라우팅 프로토콜 | 디스크·블록·오브젝트, RAID, 캐시 | 서버·하이퍼바이저·클러스터 | MPLS/VPN, WAN 라우팅 | 방화벽·LB·DPI 같은 어플라이언스 |
| **핵심 SW** | OpenDaylight, ONOS, Tungsten Fabric | Ceph, MinIO, vSAN, OpenStack Swift | OpenStack, Kubernetes, vSphere | Viptela, Velocloud, Cato, Meraki | OSM (ETSI), ONAP, Tacker |
| **데이터/제어 분리** | OpenFlow (Control -> Forwarder) | MON/OSD 분리, RADOS 게이트웨이 | Nova/Neutron API ↔ libvirt/KVM | vEdge ↔ vSmart/vBond 컨트롤러 | VNF Manager ↔ Virtual Infra |
| **프로토콜** | OpenFlow, NETCONF/YANG, OVSDB, BGP-LS | librados, RGW, S3 API | REST, libvirt, CRI, CNI | IPSec, DMVPN, SD-WAN Orchestrator API | ETSI MANO, NFV-INF, TOSCA |
| **장점** | 트래픽 엔지니어링 정밀, 빠른 신규 기능 | 정책 기반 데이터 분산·중복, 무제한 확장 | 워크로드 자동 배치, 멀티하이퍼바이저 | 비용v, MPLS 대체, SaaS 트래픽 최적화 | HW 어플라이언스 CAPEX 절감, 신규 NF 도입 가속 |
| **한계/리스크** | 컨트롤러 SPOF, Flow Table 한계(TCAM) | CAPEX(초기 디스크 대량), IOPS 변동 | 컨테이너·VM 혼용 복잡도, K8s 학습곡선 | 인터넷 회선 SLA 편차, 암호화 오버헤드 | VNF 성능(Throughput), 라이선스 모델 |
| **대표 적용 사례** | Google B4 (5G Backbone), AT&T ECOMP | CERN(450PB Ceph), S3 Glacier급 | 금융 DC, AI/ML GPU Pool, Telco NFVI | 글로벌 1,000+ 지사 연결 | 통신사 EPC(vEPC), 5G Core SBA |

### SDx와 인접 개념의 관계

- **클라우드 네이티브 vs SDx**: 클라우드 네이티브(쿠버네티스, 서비스 메시)는 **워크로드 측 추상화**(컨테이너·Pod), SDx는 **인프라 측 추상화**(네트워크·스토리지). **Istio + Calico + Rook(Ceph)** 조합이 양자를 결합한다.
- **AIops/Intent-Based Networking(IBN)**: SDx의 4계층 위에 **AI 추론 엔진을 추가**하여, 텔레메트리 -> 이상 탐지 -> 정책 자동 생성을 수행(예: Cisco DNA Center, Apstra, Juniper Mist).
- **엣지 컴퓨팅 / MEC**: SDx의 분산 컨트롤러는 **중앙 코어 컨트롤러 + 엣지 로컬 컨트롤러**로 계층화되어, 엣지 자원을 자기조직화(Self-Organizing) 한다.

- **📢 섹션 요약 비유**: SDx는 **"만