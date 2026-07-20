---
title: "ICT Convergence Master Architecture Map"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 710
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ICT 융합은 단일 기술이 아닌 **Network(5G/6G·SDN/NFV) — Computing(Cloud·Edge·Quantum) — Data(BigData·Data Lake) — Intelligence(AI/ML·GenAI·Agentic AI) — Trust(Cybersecurity·Blockchain·ZTA)**의 5대 축이 표준 참조 아키텍처(RAMI 4.0, IIRA, 등)와 거버넌스 프레임워크를 통해 결합되는 **계층적·횡단적 생태계 시스템**이다.
> 2. **가치**: 슬리(Siloed) 시스템 대비 **TCO 30~45% 절감**, 신서비스 출시(MTTM) **40~60% 단축**, 데이터-의사결정-자동화 루프를 통한 운영 효율 **OPEX 25%v**, IEC 62443·ISO 27001·DGS 인증 기반의 글로벌 시장 진입 장벽 완화.
> 3. **판단 포인트**: 도메인별·산업별·규제별로 **표준 참조 모델 선택**(제조=RAMI 4.0, 산업IoT=IIRA, 정부=한국 EA·UAF), **관통 아키텍처(End-to-End) 관점의 트레이드오프**(예: Edge-Cloud 분할 시 latency vs. cost, AI 모델 경량화 시 정확도 vs. 처리속도), 그리고 **레거시 통합 인터페이스(API Gateway·ESB·iPaaS)**와 **보안·컴플라이언스 by Design** 설계를 통한 거버넌스 통합성 확보가 핵심 결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

ICT 융합 아키텍처는 정보통신기본법, 정보통신공사업법, 소프트웨어진흥법, 데이터 산업법, AI기본법(2026.1 시행), 클라우드컴퓨팅법(2025.10 시행) 등 **입법 체계**부터 5G/6G 이동통신, 클라우드 네이티브, AI/MLOps, 디지털 트윈, 양자컴퓨팅, 메타버스, 자율주행, 스마트시티, 사이버보안, 블록체인, IoT/CPS, 표준화(ISO·ITU·3GPP·IEEE·IETF)까지 **약 25개 세부 기술 도메인**을 가로지른다. 과거에는 각 도메인을 독립적으로 설계하는 경우가 많았지만, 오늘날에는 **스마트제조·스마트시티·디지털 헬스 같은 융합 시나리오**를 중심으로 도메인 경계를 넘는 통합 아키텍처를 구성해야 한다.

기존 패러다임은 **수직통합(Vertical Integration)** — 단일 벤더(SI), 전용 HW, 폐쇄형 프로토콜, 도메인별 코어 — 이었던 반면, 현재의 패러다임은 **수평통합(Horizontal Integration) + 개방형 생태계** — 멀티클라우드, SDN/NFV, Open API, 컨테이너·마이크로서비스, 데이터 메시(Data Mesh), AI 에이전트 — 이다. 이 전환의 배경에는 (1) **연결성 폭증**(2025년 290억 IoT 디바이스, Ericsson Mobility Report), (2) **데이터 폭증**(전 세계 Datasphere 181 ZB, IDC), (3) **AI의 보편화**(Foundation Model, LLM, MLOps), (4) **규제 강화**(EU CRA, NIS2, AI Act, 한국 AI기본법, 클라우드컴퓨팅법), (5) **에너지·지속가능성 요구**(PUE, WUE, Green IT) — 라는 5대 메가트렌드가 있다.

```text
[ ICT 융합 5대 메가트렌드와 아키텍처 진화 ]

    +--------------------------------------------------------------+
    |   ① 연결성 폭증       ② 데이터 폭증       ③ AI 보편화      |
    |   (5G/6G, IoT)        (181 ZB Datasphere) (LLM, MLOps)     |
    |   290억 디바이스       Data Lake->Mesh     Agentic AI        |
    +--------+-----------------+--------------------+-------------+
             |                 |                    |
             v                 v                    v
    +--------------------------------------------------------------+
    |              횡단기술(Convergence Fabric)                     |
    |   +--------+  +--------+  +--------+  +--------+  +-----+  |
    |   | 5G/6G  |  | Cloud  |  |BigData |  |  AI/   |  |Cyb- |  |
    |   | SD-WAN |  | Edge   |  | Lake   |  |  ML    |  | Sec |  |
    |   | NFV    |  | K8s    |  |  Mesh  |  | LLM    |  | ZTA |  |
    |   +---+----+  +---+----+  +---+----+  +---+----+  +--+--+  |
    |       +-----------+-----------+-----------+----------+      |
    |                          <->                                  |
    |            [ 표준 참조 아키텍처 / 거버넌스 ]                |
    |   RAMI 4.0 | IIRA | TOGAF | 한국 EA | ISO/IEC/IEEE 42010 |
    +--------------------------------------------------------------+
             ^                 ^                    ^
             |                 |                    |
    +--------+--------+ +------+-------+ +---------+---------+
    | ④ 규제 강화     | | ⑤ 그린·지속가능성 |  -> 통합 아키텍처  |
    | EU AI Act/CRA   | | PUE/WUE, ESG  |     마스터 맵      |
    | NIS2, AI기본법  | | 2050 Net-Zero  |                    |
    +-----------------+ +---------------+ +--------------------+
```

종래의 "기술별 암기" 방식으로는 융합 문제(예: "스마트 팩토리 MES-ERP-SCADA-PLM 통합에서 OPC UA·TSN·5G 슬라이싱·AI 예측정비의 통합 아키텍처")에 대응 불가하므로, **도메인 간 연결 관계(인터페이스·데이터 흐름·표준·거버넌스)를 시각화한 마스터 맵**이 필수적이다.

- **📢 섹션 요약 비유**: 5대 메가트렌드를 강(5G), 흙(데이터), 씨앗(AI), 햇빛(규제), 비(그린)라고 하면, ICT 융합 아키텍처는 이 5가지를 모두 받아 자라는 **온실 생태계**와 같다. 어느 하나라도 빠지면 식물(시스템)은 고장 난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ICT 융합의 통합 아키텍처는 **6계층 레이어드 뷰 + 3개 횡단(cross-cutting) 영역**으로 모델링한다. 이는 **TOGAF ADM**의 4A(Architecture Domain) — **BDAT** (Business / Data / Application / Technology) — 에 **Security·거버넌스·Sustainability**를 횡단 영역으로 추가한 변형 모델이며, 동시에 **IEEE 1471 / ISO/IEC/IEEE 42010**의 **Stakeholder–Concern–Viewpoint** 체계를 따른다.

```text
[ ICT 융합 6계층 + 3 횡단 아키텍처 마스터 맵 ]

Stakeholder: 정부 / 산업 / 시민 / 운영자
-------------------------------------------------------------------
 횡단(Cross-Cutting)
 +----------+  +----------+  +----------+
 | Security |  |Governance|  |Sustain-  |  ZTA · DevSecOps · EA 거버넌스
 | (ZTA,   |  |(EA, IRM, |  | ability  |  · 그린 IT · ESG · 컴플라이언스
 |  PQC)   |  | DAMA)    |  | (PUE/WUE)|
 +----+-----+  +----+-----+  +----+-----+
      +--------------+-------------+
-------------------------------------------------------------------
Layer 1  Business Architecture -- 목표·비전·BPMN·ROI·KPI
         (예: 스마트시티 UAM 서비스, 4IR 스마트공장)
-------------------------------------------------------------------
Layer 2  Data & Information ---- Master / Transactional / Analytics
         ----------------------  Data Lake / Lakehouse / Mesh
         표준: ISO 8000, DCAT, ISO 11179
-------------------------------------------------------------------
Layer 3  Application & AI ------ SaaS / PaaS / AI Service
         ----------------------  MSA, Serverless, Foundation Model
         표준: OASIS TOSCA, CNAB, W3C
-------------------------------------------------------------------
Layer 4  Integration & API ------ iPaaS / ESB / API Gateway
         ----------------------  Event Mesh / Streaming (Kafka)
         표준: OpenAPI 3.1, AsyncAPI, GS1 EPCIS
-------------------------------------------------------------------
Layer 5  Platform & Compute ---- Public/Private/Hybrid Cloud
         ----------------------  Container, K8s, Wasm, Edge
         표준: CNCF, OCI, ISO/IEC 22123
-------------------------------------------------------------------
Layer 6  Network & Device ------ 5G/6G, TSN, Wi-Fi 7, LoRa
         ----------------------  IoT, OT, CPS, Digital Twin
         표준: 3GPP, IEEE 802.1, IETF, OPC UA
-------------------------------------------------------------------
기반 인프라:  Data Center (T3/T4) · 공조 · 전력 · 도시기반시설
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Layer 1. Business Arch.** | 전략·목표·프로세스 정렬 | BPMN 2.0, CMMN, ArchiMate 3.2, OKR/KPI 트리, TOWS, Value Stream Map; ROI 산정: NPV, IRR, TCO, Payback Period |
| **Layer 2. Data & Info.** | 데이터 거버넌스·분석 | Data Lakehouse (Delta Lake, Apache Iceberg, Hudi), Data Mesh (도메인 자율), DataOps, ETL/ELT, Data Catalog (Apache Atlas, DataHub); 표준: ISO 8000(데이터 품질), ISO 11179(메타데이터), DCAT-AP |
| **Layer 3. Application & AI** | 서비스·지능 구현 | Microservice(MSA) + Service Mesh(Istio, Linkerd), Serverless(Knative, AWS Lambda), API-First 설계; **AI**: Foundation Model(LLaMA, GPT, Claude, HyperCLOVA X), RAG(검색증강생성), MLOps/MLflow/Kubeflow, LLM Ops, Agentic AI(AutoGen, CrewAI), Edge AI(TensorRT, ONNX Runtime) |
| **Layer 4. Integration** | 시스템 간 연동·흐름 | API Gateway(Kong, Apigee), iPaaS(MuleSoft, Boomi), ESB, **Event Streaming**(Apache Kafka, Pulsar, NATS JetStream), Change Data Capture(Debezium), Webhook, GraphQL Federation; 패턴: Saga, CQRS, Outbox |
| **Layer 5. Platform** | 실행·배포·운영 | CNCF Landscape: Kubernetes(eks/gke/aks/oke), Service Mesh, GitOps(ArgoCD/Flux), **Progressive Delivery**(Argo Rollouts, Flagger), Wasm(Proxy-Wasm), Confidential Computing(Intel SGX, AMD SEV-SNP, NVIDIA H100 CC); 하이브리드: Anthos, Azure Arc, AWS Outposts |
| **Layer 6. Network/Device** | 연결·센싱·제어 | 5G SA(3GPP Rel.16~18) — URLLC(mURLLC 99.999%, 1ms), eMBB(20Gbps), mMTC(1M/km²), Network Slicing; 6G 연구(2030): THz(0.1~10THz), AI-Native Air Interface, Cell-free MIMO, RIS(Reconfigurable Intelligent Surface); 유선: TSN(IEEE 802.1Qbv, Qcc), DetNet, Wi-Fi 7(802.11be 320MHz, MLO), OT: OPC UA Pub/Sub over TSN, EtherNet/IP, PROFINET |
| **횡단. Security/Trust** | 신뢰·안전·규제 | **ZTA**(NIST SP 800-207): SDP, PEP, ID Federation, MFA, mTLS, BeyondCorp; **PQC**(Post-Quantum Cryptography, NIST FIPS 203/204/205): Kyber, Dilithium, SPHINCS+; DevSecOps(SAST/DAST/SCA); OT/ICS: IEC 62443-3-3 SL3, NIST CSF 2.0; **Blockchain/DLT**: Hyperledger Fabric, R3 Corda, Polygon zkEVM, DID/Verifiable Credentials(W3C) |
| **횡단. Governance** | EA·표준·정책 | EA 프레임워크: **TOGAF 10 ADM**, **FEAF**, **DoDAF**, **ArchiMate 3.2**; 한국: **EA-표준프레임워크**(한국지능정보사회진흥원), **정부 EA 참조모델**; IRM(Information Risk Management), DAMA-DMBOK 2.0 |
| **횡단. Sustainability** | 그린 IT·탄소감축 | **Green IT 표준**: ISO/IEC 30134(PUE, WUE, CUE, RUE, ERF), ISO 14064(GHG); EU CSRD/ESRS, 과학기반 목표(SBTi), 임베디드 탄소(Embodied Carbon); 측정: SCOPE 1·2·3, **Software Carbon Intensity(SCI)** |

핵심 원리는 **(1) 분리(Decoupling) + (2) 관측가능성(Observability) + (3) 자율성(Autonomy) + (4) 신뢰(Trust) + (5) 지속가능성(Sustainability)**의 5가지로 요약된다. 각 도메인별 세부 메커니즘은 다음과 같다.

- **네트워크**: 5G/6G는 eMBB·URLLC·mMTC를 **Network Slicing**으로 격리 제공(예: 스마트공장 슬라이스 e2e latency 5ms, 보장 대역폭 100Mbps). 6G는 **AI-Native RAN**(RIC: RAN Intelligent Controller, O-RAN Alliance) + **Cell-Free Massive MIMO**로 진화.
- **컴퓨팅**: **Cloud-Edge-Device** 3-tier — 데이터 sovereignty(데이터 주권)·latency 요구에 따라 워크로드 분할. AI 추론은 Edge(ONNX Runtime, TensorRT-LLM) + Cloud 재학습(Foundation Model fine-tuning) + Device(센서 임베디드) 분산 협업.
- **데이터**:
