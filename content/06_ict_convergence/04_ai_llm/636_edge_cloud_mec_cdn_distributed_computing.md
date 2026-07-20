---
title: "Edge Cloud MEC CDN Distributed Computing"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 636
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 단말로부터 1홉~수십 km 이내의 네트워크 종단(기지국, CO, POP)에 컴퓨팅·스토리지·콘텐츠 캐시를 분산 배치하고, ETSI MEC·3GPP EDGEAPP 표준 기반으로 워크로드를 동적 오케스트레이션하여 중앙 클라우드 대비 RTT를 10~50ms -> 1~5ms로 단축하는 **지연시간 최소화형 분산 컴퓨팅 패러다임**입니다.
> 2. **가치**: 코어 백홀 대역폭을 30~60% 절감하고, 5G URLLC(uRLLC)·자율주행(20ms 이내), 클라우드 게이밍(10ms 이내), 산업용 TSN(±1μs) 등 **초저지연·대용량 트래픽 요구를 충족**하며, 2026년 기준 전 세계 데이터의 약 50%(약 175ZB 중)가 엣지에서 생성·처리될 것으로 예측됩니다.
> 3. **판단 포인트**: 엣지 노드 배치 밀도(기지국형 vs CO형 vs Aggregation형), 캐시 일관성 정책(Pull-based vs Push-based vs Hybrid), MEC 호스트 위치 결정(5GC 통합 vs 별도 POP), K8s 기반 경량 오케스트레이터(K3s/KubeEdge/OpenYurt) 선택, UPF Traffic Steering(UL CL·Local Breakout) 설계가 **TCO와 SLA를 결정하는 핵심 트레이드오프**입니다.

---

## Ⅰ. 개요 및 필요성

기존의 **중앙 집중형 하이퍼스케일 클라우드(AWS/Azure/GCP)** 구조는 트래픽이 코어망을 거쳐 수백~수천 km 떨어진 Region에 도달해야 하므로, **물리 법칙 자체가 한계**입니다. 빛의 속도 기준으로도 한국-미국 서부 간 RTT는 110ms 이상이며, 4K/8K 라이브 스트리밍·자율주행 V2X·원격 로봇 제어처럼 **10~20ms 이내 응답을 요구하는 워크로드**는 본질적으로 중앙 클라우드로 처리할 수 없습니다.

**핵심 문제점 4가지**:
1. **물리적 거리로 인한 지연**: 단말 ↔ Region 간 평균 RTT 30~80ms, Jitter ±10ms
2. **백홀(Backhaul) 포화**: 모바일 트래픽은 2018~2023년 4배 증가(Cisco VNI), 코어망 비용 폭증
3. **단일 장애점(SPOF)**: Region 장애 시 전 사용자 서비스 중단(예: 2023년 AWS us-east-1 장애)
4. **데이터 주권 및 규제**: GDPR, 개인정보보호법, 산업데이터 안전성 요구

```text
[기존 중앙 집중형 구조] vs [엣지·MEC·CDN 분산 구조]

 사용자/단말                          사용자/단말
      |                                   |
      | LTE/5G                           | 5G/와이파이
      v                                   v
 [gNB/eNB]                            [gNB/eNB]
      |                                   |
      | 백홀(Backhaul)                    | Midhaul
      v                                   v
 [EPC/5GC]                         [MEC Host @ CU]
      |                              (UPF, App, Cache)
      | 코어 전송망                           |  <- 로컬 처리(1~5ms)
      v                              ↙      ↘
 [집선 라우터]              [Regional MEC]  [Edge CDN POP]
      |                           |              |
      v                           v              v
 [중앙 클라우드 Region]   [Cloud DC]      [Origin Server]
 (us-east-1, 110ms)       (5G Core)       (소스 데이터)
      |                          \           /
      v                           \         /
 [Database/S3/AI Inference]         \       /
                                   v       v
                            [분산 오케스트레이터]
                            (Karmada/KubeFed)
```

**왜 엣지·MEC·CDN인가?** 세 기술은 서로 다른 출발점을 가졌지만, **5G 시대에 수렴(Convergence)** 하였습니다.

- **CDN (1998~)**: 정적 콘텐츠의 지리적 분산, Akamai·Cloudflare가 주도, Edge POP 중심
- **MEC (2014~)**: 5G/이동통신 표준, ETSI ISG MEC 003(아키텍처), 011(플랫폼), 030(V2X)로 표준화
- **Edge Cloud (2018~)**: Hyperscaler들의 분산 인프라, AWS Wavelength·Azure Edge Zones·Google Distributed Cloud
- **결합 형태**: 5G UPF + MEC Host + CDN Cache를 동일 CO(Central Office)에 배치하고, **컨테이너 오케스트레이터(K3s, KubeEdge)**로 통합 관리

- **📢 섹션 요약 비유**: 중앙 집중형 클라우드가 "서울에 있는 대형 우체국에서 전국 우편을 처리하는 것"이라면, 엣지 컴퓨팅은 "각 동네 주민센터에 우편함·계산기·서류를 비치해서 필요한 건 동네에서 바로 처리하는 시스템"입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ETSI GS MEC 003 V3.x 표준을 기반으로 한 4계층 참조 아키텍처가 사실상 표준이며, 3GPP TS 23.558(Edge Application Architecture)이 이동통신 망과의 인터페이스를 정의합니다.

```text
 [ETSI MEC 표준 아키텍처 + 5G 통합]
 +------------------------------------------------------------+
 |  L7: MEC Application Layer                                 |
 |  - V2X 서비스, AR/VR 렌더링, 영상 분석, 산업용 AI          |
 |  - 12-factor app + 컨테이너 이미지 (Docker/OCI)           |
 +------------------------------------------------------------+
 |  L6: MEC Platform Service Layer                            |
 |  - Service Registry, Traffic Rule, DNS Handler             |
 |  - MEC011 Service Mgmt, MEC015 Traffic Influence          |
 |  - Location Service, Bandwidth Mgmt, UE Identity           |
 +------------------------------------------------------------+
 |  L5: MEC Framework / Virtualization                        |
 |  - Container Runtime: containerd, K3s, KubeEdge runtime    |
 |  - WASM Runtime: WasmEdge, Spin (Fermyon)                  |
 |  - Hypervisor: KVM(보안) / lightweight VM(Firecracker)     |
 +------------------------------------------------------------+
 |  L4: MEC Host Infrastructure (HW)                          |
 |  - Compute: Intel Xeon D / NVIDIA Jetson AGX / Ampere Altra|
 |  - Storage: NVMe SSD + Tiered Cache(Redis/Memcached)       |
 |  - Network: SR-IOV, DPDK, eBPF, SmartNIC(DPU: BlueField-3) |
 +------------------------------------------------------------+
           ^                        ^
   MEC Orchestrator           MEC Platform Mgr
   (전국/글로벌)              (도메인 단위, 5GC 연동)
           ^                        ^
   +-------+------------------------+-------+
   |  5G Core (5GC) & OSS/BSS                |
   |  - AMF / SMF / UPF / PCF / NRF          |
   |  - UPF Local Breakout (UL CL)           |
   |  - NEF (Network Exposure Function)      |
   +-----------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **MEC Host** | 엣지 워크로드의 물리적 실행 환경 | 1~2RU 서버 3~10대 클러스터, 총 100~500 vCPU, SR-IOV로 UPF와 App이 동일 NIC 통과, NUMA-aware 스케줄링 |
| **5G UPF (User Plane Function)** | 사용자 트래픽 종단, 로컬 데이터 네트워크(LDN) 제공 | **UL CL(Uplink Classifier)** 또는 **Local Breakout(LBO)**으로 MEC App으로 직접 트래픽 라우팅, IPv6 Multi-homing 기반 멀티 UPF 연동 |
| **CDN Edge POP** | 정적·동적 콘텐츠 캐시, TLS 종단 | Varnish/Nginx/Envoy + Anycast IP + GeoDNS(EDNS Client Subnet), L1 SSD 5TB + L2 Memcached 200GB 2-tier 캐시, Cache Hit Ratio 90~98% |
| **MEC Orchestrator** | 다수 MEC Host의 라이프사이클·배치 관리 | Kubernetes Federation v2, Karmada, OpenYurt의 YurtHub, KubeEdge의 EdgeMesh, 3GPP EES(Edge Enabler Server) 연동 |
| **Edge AI Inference** | 모델 추론을 단말 근처에서 수행 | NVIDIA TensorRT, ONNX Runtime, OpenVINO, TensorFlow Lite, 모델 크기 최적화(Quantization INT8/FP16), NPU(Jetson Orin 100TOPS) 활용 |

**핵심 메커니즘 (3단계)**:
1. **단말 등록·정책 수신**: UE가 gNB에 Attach -> AMF/SMF 통해 PCF가 UE의 **UE Route Selection Policy (URSP)**를 전달 -> SMF가 UPF를 선택하고 **Traffic Influence API**(ETSI MEC 015 or 3GPP NEF TRAFFIC_INFLUENCE)를 통해 특정 트래픽을 MEC App으로 Steering
2. **로컬 데이터 네트워크(LDN) 라우팅**: UPF가 N6 인터페이스를 통해 MEC Host의 vLB(virtual Load Balancer)로 트래픽 전달, vLB는 L7(Application Layer) 라우팅(Envoy WASM Filter), 인증(OAuth2/mTLS), 레이트 리밋
3. **엣지-클라우드 페일오버**: MEC Host CPU 사용률 80% 초과 시 Orchestrator가 **인접 MEC로 워크로드 마이그레이션**(KubeEdge EdgeMesh 기반 서비스 디스커버리), 클라우드 Region은 Cold Standby로 BaaS(Backup as a Service) 제공

**핵심 파라미터와 수식**:
- **엣지 응답 지연 = R(propagation) + R(processing) + R(queuing) + R(transmission)**
  - R(propagation) = d/c (d: 거리, c: 광속 ≈ 2×10⁸ m/s in fiber, 실제 2×10⁸ m/s)
  - 도심 MEC @ 5km: 0.025ms / 기지국형 MEC @ 0.5km: 0.0025ms / 중앙 클라우드 @ 1000km: 5ms
- **Total Cost of Ownership (TCO) 모델**:
  - `TCO_edge = N_edge × C_hw + N_edge × C_power × 24×365 + B(MEC-Cloud) + C_ops`
  - `TCO_cloud = C_origin_bandwidth + C_compute_central`
