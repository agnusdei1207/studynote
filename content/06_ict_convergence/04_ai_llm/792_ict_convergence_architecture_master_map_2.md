---
title: "ICT Convergence Architecture Master Map 2"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 792
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ICT 융합 아키텍처 마스터 맵 2는 **Edge-Cloud-AI Continuum** 위에서 5G/6G 네트워크 슬라이싱, Digital Twin, Federated Learning, Hyper-Automation, Zero-Trust Security Mesh가 유기적으로 결합된 **AI-Native 초연결 지능형 인프라**의 총체적 청사진을 다룬다.
> 2. **가치**: 단일 도메인 최적화를 넘어 **초저지연(URLLC <1ms)**, **대규모 기기연결(mMTC 10⁶/km²)**, **데이터主权(Federated/Sovereign Cloud)**, **탄소감축(Green ICT 30~50%)** 을 동시에 달성하여, Industry 5.0 기반 스마트 팩토리·자율주행·원격의료·메타버스 서비스의 TTM(Time-to-Market)을 평균 40% 단축시킨다.
> 3. **판단 포인트**: 중앙집중형 vs 분산형(Centralized vs Federated), 범용 GPU vs NPU/PIM, Proprietary 5G vs Open RAN, Public Cloud vs Sovereign Cloud, Vendor-locked vs Multi-vendor Interoperable 아키텍처 간의 **Trade-off 분석**과 **표준 준수(3GPP, O-RAN, ETSI MEC, IETF, IEEE)**, **레거시 통합(EAI/ESB->API Gateway->Service Mesh)** 전략이 합격의 핵심 변별점이다.

---

## Ⅰ. 개요 및 필요성

기존의 Master Map 1이 클라우드·네트워크·데이터센터의 **수직적 계층(Vertical Stack)** 통합에 초점을 맞추었다면, Master Map 2는 **초연결(Hyper-Connectivity)**, **초지능(Hyper-Intelligence)**, **초자동화(Hyper-Automation)** 라는 3대 축을 기준으로, **AI·빅데이터·5G/6G·엣지컴퓨팅·디지털트윈·보안·지속가능성**이 횡적으로 결합된 **Cyber-Physical-Social Convergence Architecture**를 다룬다. 4차 산업혁명 이후 서비스는 단일 기술로는 구현 불가능하며, **네트워크·컴퓨팅·데이터·AI·보안**이 End-to-End로 통합되어야 SLA 99.999%와 실시간 의사결정을 보장할 수 있다. 특히 2024년 이후 **생성형 AI(LLM/Multi-Modal Foundation Model)**의 산업 현장 도입, **AI 워크로드 폭증**(연간 4.2배 증가, IDC 2024), **EU AI Act·데이터법(2025 발효)** 등 규제 강화, **에너지 효율 규제(EU Energy Efficiency Directive, PUE 1.3 이하 의무화)** 등으로 인해, 단일 벤더 종속형 아키텍처에서 **개방형·분산형·지능형·지속가능형** 아키텍처로의 전환이 필수적이다.

```text
+---------------------------------------------------------------------+
|          ICT Convergence Architecture Master Map 2 (총론)           |
+---------------------------------------------------------------------+
|                                                                     |
|   [사용자/디바이스]              [서비스 레이어]                      |
|   +--------------+            +------------------------------+      |
|   | HMD/Robot/IoT|◄----------►| Metaverse / V2X / SmartCare  |      |
|   | Sensor/Robot |   5G/6G    |  Digital Twin / Autonomous   |      |
|   +------+-------+ URLLC      +---------+--------------------+      |
|          | eMBB/mMTC                   | API Gateway / Service Mesh|
|   +------v-----------------------------v----------------------+    |
|   |       Edge-Cloud-AI Continuum (Orchestration Plane)       |    |
|   |  +-------+  +--------+  +---------+  +-----------------+  |    |
|   |  |Device |  |Far Edge|  |Near Edge|  | Regional / Core |  |    |
|   |  |Edge   |  |(MEC)   |  |(MEC+AI) |  | Cloud (Hyperscale)|  |    |
|   |  +-------+  +--------+  +---------+  +-----------------+  |    |
|   |     ^          ^             ^               ^              |    |
|   |     |   K8s+ArgoCD/RobotShop/O-RAN RIC Orchestration       |    |
|   +-----+----------+-------------+---------------+--------------+    |
|   |     [Data & AI Fabric]  [Security Mesh]  [Green IT]       |    |
|   |  DataMesh|Lakehouse|   Zero-Trust|SASE|   Liquid Cooling|    |
|   |  VectorDB|FeatureStore|  Post-Quantum|Confidential Comp|   PUE  |
|   |  Federated|MosaicML|  Confidential|TEE|    <1.3        |    |
|   +----------------------------------------------------------+    |
|                                                                     |
|   [기반 인프라] NFV/SDN · Optical · Wi-Fi 7 · Satellite NTN        |
+---------------------------------------------------------------------+
```

기존 **3-Tier(On-Prem) -> Cloud-Native(Microservices/K8s)** 의 진화 이후, 현재는 **AI-Native(LLM Ops + GPU-as-a-Service + Vector DB)** 및 **Edge-Native(Edge K8s/KubeEdge, WASM)** 단계로 진입하였다. 핵심 변화는 ①**워크로드의 이질성(Heterogeneous Workload: LLM Inference + Streaming + Batch ETL 동시 실행)**, ②**데이터의 분산성(Data Gravity -> Data Locality)**, ③**규제의 영역성(Data Sovereignty, EU/US/CN)** 이다. 따라서 Master Map 1에서 다룬 "연결과 통합"에서 한 단계 더 나아가, "**자율 최적화(Self-Optimizing)**"와 "**신뢰 기반 운영(Trust-by-Design)**"을 아키텍처에 내재화하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 🎼 **"오케스트라의 총보"** — 각 악기(엣지·클라우드·5G·AI·보안)가 개별 연주자였지만, 이제는 **지휘자(Orchestrator)**가 AI 스코어(Reinforcement Learning)로 실시간 호흡을 맞추며, 객석 청자(사용자)에게 끊김 없는 음악(서비스)을 전달하는 통합 무대다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ICT 융합 Master Map 2는 다음 6개의 **수평 계층(Horizontal Layer)**과 3개의 **수직 관통 영역(Vertical Cross-Cutting Concern)**으로 구성된다. 이는 TM Forum ODF, ETSI ZSM, 3GPP Service-Based Architecture(SBA), O-RAN Architecture, IEEE P2805, ISO/IEC 22123(Cloud Computing Reference Architecture) 등 다수 표준을 통합한 **Holistic Reference Model**이다.

```text
+----------------------------------------------------------------------+
|  L1. Experience Layer (UX/UI)                                        |
|      3D Web(XR/WebGPU) · Conversational AI · Headless Commerce       |
+----------------------------------------------------------------------+
|  L2. Service & API Layer                                             |
|      API Gateway(Kong/Apigee) · Service Mesh(Istio/Linkerd) · BFF    |
|      GraphQL/gRPC-Web · AsyncAPI · Event Streaming(Schema Registry)  |
+----------------------------------------------------------------------+
|  L3. Application & AI Layer (Model + Logic)                         |
|      Foundation Model (LLM/VLM/MFM) · MLOps/LLMOps · Agentic AI      |
|      AIOps · RAG · Fine-Tuning(PEFT/LoRA/QLoRA)                     |
+----------------------------------------------------------------------+
|  L4. Data Fabric & Intelligence Plane                                |
|      Lakehouse (Delta/Iceberg/Hudi) · Vector DB (Milvus/Qdrant)     |
|      Feature Store · Knowledge Graph · Data Mesh (Domain Ownership) |
|      CDC (Debezium) · Stream Processing (Flink/Kafka Streams)        |
+----------------------------------------------------------------------+
|  L5. Platform & Orchestration Layer (Cloud-Native Control Plane)     |
|      K8s (Multi-Cluster: KubeFed/ArgoCD) · Serverless (Knative)     |
|      AI Platform (Kubeflow/Ray/Slurm on K8s) · GPU Sharing (MIG/MPS)|
|      Edge Orchestrator (KubeEdge/OpenYurt/Azure Arc)                 |
+----------------------------------------------------------------------+
|  L6. Infrastructure & Network Layer (Composable Disaggregated)       |
|      HCI (Nutanix/vSAN) · DPU/IPU (NVIDIA BlueField/Intel IPU)      |
|      5G/6G Core (SBI) · O-RAN (RIC/xApp/rApp) · MEC (ETSI MEC 013)  |
|      Optical (ZR/ZR+ Coherent) · Wi-Fi 7 (802.11be MLO) · LEO Sat   |
+----------------------------------------------------------------------+
   ^    ^    ^    ^    ^    ^
   |    |    |    |    |    |
+--+----+----+----+----+----+----------------------------------------+
|  V1. Security & Trust (Zero-Trust, Confidential Computing, PQ-Crypto)|
|  V2. Sustainability & Observability (Green IT, AIOps, FinOps, SRE) |
|  V3. Governance & Compliance (AI Act, ISO 42001, 데이터3법, NIS2)   |
+---------------------------------------------------------------------+
```

### 🧱 계층별 핵심 기술 심층 분석

| 계층 / 영역 | 핵심 컴포넌트 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- | :--- |
| **L1. Experience** | WebXR, Digital Twin Viewer | 몰입형 UX, 실시간 렌더링 | **WebGPU** + **WASM** + **Babylon.js/Three.js** + 12K HMD, 90Hz 유지 위해 Adaptive LOD(ALOD) 및 Foveated Rendering 적용, **Volumetric Video(NeRF/3DGS)** 스트리밍은 1Gbps 대역폭 + MEC에서 Tile 기반 분할 인코딩 |
| **L2. Service & API** | API Gateway, Service Mesh | 트래픽 라우팅, 정책/관찰 가능성 | **Istio Ambient Mesh**(Sidecar 제거로 70% 지연 감소), **eBPF** 기반 L7 가속(Cilium Tetragon), **GraphQL Federation(Apollo)**, **AsyncAPI 3.0**으로 Event-driven 계약 명세, mTLS + SPIFFE ID로 워크로드 신원 부여 |
| **L3. Application & AI** | Foundation Model Serving | LLM/VLM 추론·학습 | **vLLM/TensorRT-LLM** PagedAttention(KV Cache 메모리 24× 효율), **Speculative Decoding**(Medusa), **Quantization(INT4/FP8)**, **MoE(Mixtral 8×22B)**, RAG는 **Hybrid Search(BM25 + Dense) + Re-Ranker(Cohere Rerank v3)** |
| **L4. Data Fabric** | Lakehouse + Vector Store | 통합 데이터·벡터 검색 | **Apache Iceberg(ACID on Object Storage) + Unity Catalog**, **Milvus 2.4(DiskANN Index)**, **LanceDB**(Columnar for AI), **Lakehouse Federation(Trino)**, **Change Data Capture(Debezium->Kafka->Flink)**, **Data Contract** 기반 Mesh |
| **L5. Platform** | AI/Edge Orchestrator | 자원 스케줄링·배포 | **Kubernetes + Karpenter**(Bin-packing for GPU), **Ray on K8s**(분산 학습), **KubeEdge**(EdgeNode 100K+ 관리, 50ms Heartbeat), **Argo Rollouts**(Canary 1%->10%->50%->100%, Prometheus 메트릭 기반 자동 Promote) |
| **L6. Infrastructure** | DPU + Open RAN + 6G | 컴포즈 가능한 자원 풀 | **NVIDIA BlueField-3 DPU**(400Gbps, Storage Accelerator), **Intel IPU E2100**, **O-RAN ALLIANCE eCPRI**(25Gbps Fronthaul), **Intel FlexRAN**, **AMD T2 Telco Card**, **L4S(低遅延 Low Latency, Low Loss, Scalable Throughput)** 으로 큐잉 지연 0.1ms 이하 |
| **V1. Security** | Zero-Trust + Confidential Comp | 신원 기반 마이크로세그멘테이션 | **SPIRE**(Workload Identity), **NIST SP 800-207** ZTA, **Intel TDX/AMD SEV-SNP/ARM CCA**(Hardware TEE), **Nvidia H100 Confidential Computing**, **Post-Quantum ML-KEM(CRYSTALS-Kyber)**, **Quantum Key Distribution(QKD)**, **DID(Decentralized Identifier) + VCs(Verifiable Credentials)** |
| **V2. Sustainability** | Green IT + FinOps | 탄소·비용 가시화 | **PUE/CUE/WUE** 실시간 모니터링, **Liquid Cooling(Cold Plate/Dielectric, PUE 1.05)**, **Immersion Cooling(3M Novec)**, **Dynamic Voltage Frequency Scaling(DVFS)**, **Carbon-Aware Scheduling(Spot in Region with Low CO₂)**, **FinOps K8s Plugin(Kubecost)** |
| **V3. Governance** | AI Risk & Data Sovereignty | 규제 준수·정책 자동화 | **EU AI Act Risk Tier(HIGH Risk 시 Conformity Assessment)**, **ISO/IEC 42001 AIMS**, **Data Act(Interoperability)**, **NIS2(Incident Report 24h)**, **Policy-as-Code(OPA/Gatekeeper)**, **Model Card & Datasheet for Datasets** |

### ⚙️ 핵심 알고리즘 및 파라미터

1. **AI 추론 스케줄링**:
   - **LLM Serving**: Continuous Batching + Iteration-level Scheduling -> Token Throughput 23× 향상 (vLLM, Kwon et al., SOSP'23)
   - **GPU Multiplexing**: NVIDIA MIG(Multi-Instance GPU) A100 7-way slicing / H100 8-way, MPS로 Context Switching 5μs 이하
   - **Inference Latency Budget**: ① Prefill(Bound by FLOPS) ② Decode(Bound by Memory Bandwidth) -> H100 HBM3 3.35TB/s 기준 Mixtral 추론 시 Prefill 18ms / Decode 12ms/token
2. **네트워크 슬라이싱**:
   - **3GPP TS 23.501 Slice = {SST, SD}** SST 1=eMBB / 2=URLLC / 3=mMTC / 4=V2X
   - **End-to-End Slice**: RAN 슬라이스(PRB Reservation, Network Slice Admission Function) + 5GC(UPF Selection) + Transport( FlexE Channelization) + Cloud(Network Slice Subnet)
   - **지연 예산**: RAN(<5ms) + Transport(<2ms) + MEC(<1ms) = URLLC 보장 1ms@99.999%
3. **Edge-Cloud Orchestration**:
   - **Kubernetes Federation v2(KubeFed)**: ClusterProfile CRD로 정책 전파, **Argo CD ApplicationSet**으로 GitOps 멀티클러스터
   - **Edge Node 한계**: CPU ≤ 4Core / Mem ≤ 8GB / Storage ≤ 64GB -> **Lightweight Runtime**:
