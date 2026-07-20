---
title: "ICT Architecture Writing Keywords Final Summary"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 795
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ICT 융합 아키텍처는 단순한 키워드 암기가 아니라, **5G 코어 네트워크 -> 클라우드-엣지 -> 데이터/AI -> 보안/거버넌스**의 4-Layer 구조를 기준으로 중앙집중과 분산, 일관성과 가용성, 저지연과 보안의 트레이드오프를 설명하는 학습 주제다.
> 2. **가치**: 키워드 간 인과관계(예: NFV -> Microservice -> Service Mesh -> mTLS -> Zero Trust)와 정량 지표(지연 p99, RTO/RPO, SLA 99.999%, CAP theorem 수렴)를 도식화·비교표로 표현하면 **설계 의사결정의 합리성**을 한 화면에 정리할 수 있다. 최근에는 AI·플랫폼·지속가능성(Sovereign/ESG-Tech)의 연계가 특히 중요하다.
> 3. **판단 포인트**: 키워드 나열식 답변은 탈락 요인이며, **(a) 요구사항 도출 -> (b) 후보 아키텍처 비교 -> (c) 표준/규제 매핑 -> (d) 운영·보안·DR 설계 -> (e) 성과 KPI(예: MTTR 50%v, 비용 30%v) 정량화**의 5-Step 서술 구조를 채택해야 실무자 등급의 “공학적 판단력”이 평가된다.

---

## Ⅰ. 개요 및 필요성

ICT 융합은 4차 산업혁명 이후 **연결성(5G/6G)·지능(AI)·데이터(Data Mesh/Graph)·자율운영(AI-Ops/SRE)**이 하나의 플랫폼 위에서 결합되는 흐름을 다룬다. 국내외 표준화와 산업 동향을 함께 보면, 단순 CS 지식(OS, DB, NW)을 넘어 **Hyper-converged Platform, AI-Native Network, Sovereign Cloud, Quantum-Safe Cryptography, AI 윤리·개인정보 보호법**처럼 기술·규제·표준을 교차해 이해할 필요가 있다.

따라서 본 노트는 복잡한 융합 주제를 구조적으로 설명하기 위한 **“키워드 -> 표준 -> 아키텍처 -> 정량 KPI”**의 4단 매핑을 정리한다. 주요 항목은 한국 ICT 정책(“K-ICT 2030”, “디지털 권리 장전”, “AI Basic Act”)과 국제 표준(3GPP Rel-18, ETSI ZSM, ISO/IEC 42001, NIST AI RMF, IEEE 7000 시리즈)에 기반한다.

```text
[ICT 융합 실무자 논술 키워드 4-Layer 컨버지드 아키텍처]

+--------------------------------------------------------------------+
|  L1. 정책·거버넌스  (Policy & Governance)                          |
|      - AI 기본법 / GDPR / DPF / 데이터산업법 / ESG-Tech          |
|      - 표준: ISO/IEC 42001(AIMS), NIST AI RMF, IEEE 7000          |
+--------------------------------------------------------------------+
|  L2. 지능·데이터  (Intelligence & Data)                            |
|      - Foundation Model / RAG / Federated Learning / Data Mesh   |
|      - LakeHouse(Iceberg/Hudi) / Vector DB / Knowledge Graph     |
+--------------------------------------------------------------------+
|  L3. 플랫폼·운영  (Platform & Operations)                          |
|      - K8s / Service Mesh(Istio) / GitOps / Observability        |
|      - AIOps·SRE·FinOps·DevSecOps·DataOps·MLOps·LLMOps          |
+--------------------------------------------------------------------+
|  L4. 연결·인프라  (Connectivity & Infrastructure)                  |
|      - 5G SA / Network Slicing / MEC / SDN/NFV / O-RAN           |
|      - Sovereign Cloud / Edge / Serverless / WASM / Confidential |
+--------------------------------------------------------------------+
|  L0. 보안 공통 레이어 (Zero Trust, SASE, PQC, mTLS, eBPF)         |
+--------------------------------------------------------------------+
                ^     ^     ^     ^
                |     |     |     |
       End-to-End SLA·Zero-Trust·Data Sovereignty·AI Safety
```

기존(2010년대) ICT 학습 정리은 **“단일 시스템의 성능·안정성”**을 묻는 폐쇄형 구조였으나, 현재는 **“상호의존 시스템의 회복탄력성·거버넌스”**를 평가하는 개방형 융합 문제로 전환되었다. 예컨대 “스마트 팩토리”라는 단일 키워드도 5G 슬라이싱 + MEC + OPC-UA + TSN + Digital Twin + AI 추론 + IEC 62443 보안의 7-Layer 통합 설계가 요구된다.

- **📢 섹션 요약 비유**: 마치 **“한옥의 기둥·처마·기와·기단”**이 따로 노는 게 아니라 **기단(인프라) -> 기둥(플랫폼) -> 처마(데이터) -> 지붕(AI/거버넌스)**로 무게중심이 위로 올라갈수록 정교해지듯, ICT 융합 논술도 4개 Layer가 “위에서 누르면 아래가 받쳐주는” 구조로 답해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ICT 융합 논술의 5-Step 표준 서술 프레임워크는 아래와 같다. 모든 키워드는 이 프레임 안에 매핑된다.

```text
[5-Step 아키텍처 설명 구조 — STAR-ICAE]

  ① Situation/요구사항   -► ② Technology/후보 비교   -►  ③ Architecture/선택 근거
            |                          |                              |
            v                          v                              v
  ⑤ Evaluation/KPI·리스크   ◄-- ④ Implementation/도입 절차·표준·규제

       [예시] 스마트 병원: 지연 1ms 요구 -> 5G URLLC 슬라이싱 + MEC + FHIR+HIE
              ->  AI 진단 모델 MLOps 운영 ->  HIPAA·개인정보보호법·식약처 인허가
              ->  KPI: 영상 전송 p99 < 50ms, 진단 정확도 95%, DR RTO 15분
```

| Layer | 핵심 키워드(20) | 표준·프로토콜 | 트레이드오프 / KPI |
| :--- | :--- | :--- | :--- |
| **L1 정책** | AI 기본법, DPF, ESG-Tech, ISO/IEC 42001, NIST RMF | EU AI Act, ISO 42001 AIMS, ISO 27001/27701 | 컴플라이언스 비용 vs 속도, Risk Tier 1~4 |
| **L2 지능** | LLM·RAG, FL, Vector DB, Knowledge Graph, LakeHouse | MCP, OpenAI-API, ONNX, Iceberg/Hudi/Delta | 정확도 vs 환각(Hallucination), 학습/추론 p99 |
| **L3 플랫폼** | K8s, Service Mesh, GitOps, AIOps, SRE | Istio, ArgoCD, Argo Rollouts, OpenTelemetry, eBPF | 배포 속도 vs 안정성, MTTR < 30분, 변경 실패율 < 5% |
| **L4 연결** | 5G SA, Network Slicing, MEC, O-RAN, TSN | 3GPP Rel-18, ETSI MEC, O-RAN ALLIANCE, IEEE 802.1Qcc | URLLC 1ms vs eMBB 1Gbps vs mMTC 1M/km² |
| **L0 보안** | Zero Trust, SASE, PQC, Confidential Computing, mTLS | NIST SP 800-207, NIST FIPS 203/204/205, CC EAL5+, SPIFFE/SPIRE | 지연 +5% vs 침해 표면 90%v |
| **운영** | DevSecOps, MLOps, DataOps, FinOps, LLMOps | CNCF TAG, OMDOC, Kubeflow, MLflow, OpenCost | CapEx->OpEx, 단위 트랜잭션당 비용 최적화 |
| **데이터 거버** | Data Mesh, Data Contract, Data Fabric, Sovereign Data | ISO/IEC 11179, Open Data Product Spec, GAIA-X | 도메인 자율성 vs 전사 일관성 (CAP) |
| **신기술** | WebAssembly, eBPF, Confidential GPU, RISC-V, 양자인터넷 | Wasmtime, Cilium, NVIDIA H100 TEE, OpenTitan | 성능 vs 이식성 vs 신뢰루트 |
| **지속가능성** | Green IT, Sovereign AI, Carbon-Aware Computing | ISO 14064, SCI(Software Carbon Intensity), SBTi | 에너지 gCO₂eq/req vs 처리량 |
| **리스크** | 공급망(3rd-party SBOM), Deepfake, Shadow AI | EO 14028, SLSA, NIST AI RMF, CWE/SCA | Time-to-Market vs Zero-Day 노출 |

### 실무자 논술의 5대 핵심 공식

```
1)  CAP -> PACELC 확장    (강일관성·가용성·분단허용 -> 평상시 지연 vs 일관성)
2)  Amdahl 실효성         (S(N) = 1 / ((1-P) + P/N),  GPU 8장 -> P=0.95 -> 6.8배)
3)  Little’s Law          (L = λ·W,  동시접속 = TPS × 평균체류)
4)  RTO/RPO × R            (R=복구주기, SLO 99.99% -> 연간 허용 다운타임 52.6분)
5)  Mos定律 / Kryder  +    (데이터 +40%/년, 네트워크 +25%/년, 스토리지 +20%/년)
```

- **📢 섹션 요약 비유**: 위 4-Layer는 **“에스프레소 머신”**과 같다. **인프라(L4)**는 보일러·펌프(물=데이터를 가열), **플랫폼(L3)**은 추출 그룹(압력·온도 제어), **데이터·AI(L2)**는 원두(향미 결정), **거버넌스(L1)**는 컵·라벨·가격표(소비자 신뢰)이다. 어느 한쪽이 약하면 “한 잔의 좋은 커피”는 절대 나올 수 없다.

---

## Ⅲ. 비교 및 연결

### 비교 ① — 클라우드 네이티브 배포 전략

| 구분 | Monolith | Microservice | Service Mesh | Serverless / WASM |
| :--- | :--- | :--- | :--- | :--- |
| 배포 단위 | WAR/EAR 단일 | 컨테이너(컨테이너 평균 12개) | Sidecar Envoy + 정책 | 함수 1개, Cold Start |
| 결합도 | 강한 결합(SoC) | 느슨한 결합(SoR·SoE) | 정책 결합(SoP) | 이벤트 결합(EDA) |
| 확장 단위 | VM 수평확장 | Pod HPA/VPA | DestinationRule | Concurrency |
| 회복탄력성 | Circuit Breaker 없음 | Hystrix/Resilience4j | Istio Retry/Timeout | EventBridge DLQ |
| 적합 워크로드 | 레거시·ERP | 코어 도메인 | 멀티테넌시 정책 | 버스트성 API·AI 추론 |
| 트레이드오프 | 단순 ↔ 확장성v | 유연 ↔ 운영 복잡^ | 일관 정책 ↔ 지연+2~5ms | 경제성 ↔ Cold Start 1~3s |

### 비교 ② — 데이터 일관성 모델 (CAP/PACELC)

| 구분 | RDB (PostgreSQL) | NoSQL (Cassandra) | LakeHouse (Iceberg) | Data Mesh (도메인형) |
| :--- | :--- | :--- | :--- | :--- |
| 일관성 | Strong (ACID) | Eventual (Tunable) | Snapshot Isolation | 도메인별 SLO |
| 가용성 | 단일리전 99.95% | Multi-DC 99.99% | Object Storage 종속 | 도메인 자치 |
| 확장성 | 수직 한계 | 선형 확장(PB급) | 분리 스토리지·컴퓨트 | 도메인별 독립 |
| 표준 | SQL:2003 | CQL | Iceberg v2 / REST | ODM, Data Contract |
| 적합 업무 | 금융 원장 | IoT 텔레메트리 | AI Feature Store | 대규모 조직 거버넌스 |
| 트레이드오프 | 정합성 ^ vs 비용^ | 가용성 ^ vs 일관성v | 유연성 ^ vs 메타관리^ | 자율성 ^ vs 일관 거버넌스v |

### 비교 ③ — 네트워크 슬라이싱 & 엣지 컴퓨팅

| 구분 | 5G URLLC | 5G eMBB | 5G mMTC | MEC | Private 5G |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 지연 | < 1 ms | 10 ms | < 100 ms | < 5 ms | 1~10 ms |
| 대역폭 | 낮음 | 1 Gbps^ | 낮음 | 가변 | 가변 |
| 디바이스 밀도 | 10⁵/km² | 10⁴/km² | 10⁶/km² | — | 캠퍼스 단위 |
| KPI 예시 | 로봇 99.999% | 8K 영상 | 스마트미터 | AR/VR | 공장·항만 |
| 표준 | 3GPP TS 22.261 | 3GPP TS 38.300 | 3GPP TS 38.331 | ETSI MEC ISG | 3GPP TS 28.554 |
| 결합 키워드 | TSN·OPC-UA | CDN·ABR | NB-IoT·LoRa | K8s·GPU | O-RAN·SON |

### 비교 ④ — MLOps vs LLMOps vs AIOps

| 구분 | MLOps | LLMOps | AIOps |
| :--- | :--- | :--- | :--- |
| 대상 | 전통 ML/XGBoost/CNN | LLM 파인튜닝·RAG | 운영 이벤트·로그 |
| 핵심 산출물 | 모델 아티팩트 + Feature | Prompt·Embeddings·Vector | 인시던트·근본원인 |
| 파이프라인 | TFX·Kubeflow·MLflow | LangChain·LlamaIndex·DSPy | Moogsoft·PagerDuty AIOps |
| GPU 자원 | T4 / A10 | H100 / MI300 (70B^) | 경량 추론 가능 |
| 평가 지표 | AUC·RMSE | Faithfulness·Context Recall | MTTA·노이즈 감소율 |
| 트레이드오프 | 정확도 vs 지연 | 환각v vs 비용^ | 자동화 ^ vs 오탐 |

- **📢 섹션 요약 비유**: 위 4개 비교표는 **“병원 진료 과”**와 같다. 응급(URLLC)·일반진료(eMBB)·예방접종(mMTC)이 같은 병원이지만 “환자 상태(요구사항)”에 따라 치료법
