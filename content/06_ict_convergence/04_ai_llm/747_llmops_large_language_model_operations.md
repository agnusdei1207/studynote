---
title: "LLMOps Large Language Model Operations"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
weight: 747
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLMOps는 대규모 언어 모델(LLM)의 데이터 수집·전처리, 파인튜닝(PEFT/LoRA/QLoRA), RAG 파이프라인, 프롬프트 엔지니어링, 추론 서빙(vLLM/TGI/Triton), 분산 학습(DeepSpeed/FSDP/NeMo), 평가(LLM-as-a-Judge/Human Eval), 모니터링(Langfuse/Phoenix/Arize), 거버넌스(PII·유해성·할루시네이션 탐지) 전 라이프사이클을 MLOps 위에 **LLM 고유 차원(비결정성·토큰 비용·컨텍스트 윈도우·드리프트·멀티모달·에이전트)**을 통합 관리하는 운영 프레임워크이다.
> 2. **가치**: 체계적 LLMOps 도입 시 모델 출시 Lead Time을 평균 40~60% 단축(MLOps 대비 30% 추가), 토큰 단위 비용을 Prompt Caching·Batch API·Speculative Decoding으로 50~80% 절감, RAG 정답률(Recall@5)을 20~35%p 향상, 할루시네이션·유출 PII를 가드레일·Evaluation Gate로 90% 이상 차단하며, GPU utilization을 30%->75%로 끌어올려 동일 H100 인프라에서 처리량을 약 2.5배 확장한다.
> 3. **판단 포인트**: ①Self-host(개방형 모델+온프레미스 GPU) vs Managed API(OpenAI/Claude/Bedrock) ②Fine-tuning(도메인 지식 주입) vs RAG(외부 지식 주입) vs Prompt-only ③Single-tenant vs Multi-tenant 라우팅 ④Sync vs Async·Streaming 응답 ⑤중앙집중식 vs 분산 추론(Edge/On-device, e.g., llama.cpp/MLX) — 이 5축의 조합이 TCO·지연·데이터 주권·확장성을 결정한다.

---

## Ⅰ. 개요 및 필요성

전통 MLOps는 “결정적·구조적·표본 적음”의 특성을 갖는 정형 데이터(XGBoost·CNN·BERT 분류기 등) 위주의 ML 모델을 **재현성·드리프트 감지·피처 일관성** 축으로 운영했다. 반면 LLM은 ①수조 토큰의 Pre-training, ②명령어 튜닝(IFT/SFT/DPO/RLHF/ORPO), ③컨텍스트 윈도우(2K~2M 토큰), ④비결정적 생성, ⑤토큰 단위 과금, ⑥하루 수억 건의 사용자 Prompt 유입, ⑦할루시네이션·프롬프트 인젝션·PII 누출이라는 전혀 새로운 운영 변수를 들고 등장했다. Gartner는 2026년 기업 생성형 AI 프로젝트의 60%가 미가드레일·미관측 상태로 “PoC에서 Production Dead Zone”에 빠질 것으로 예측했고, McKinsey 2024 설문에서 生成AI를 운영 환경에 배포한 기업은 11% 미만이었다. **LLMOps는 “모델을 학습시키는 것”이 아니라 “수십억 파라미터 모델이 매일 수천만 건의 Prompt를 받아 일관된 품질·안전·비용으로 응답하도록 공급망을 운영하는 것”**이라 정의할 수 있다.

LLM의 라이프사이클은 ①Foundation Model 평가·선정 -> ②도메인 데이터 큐레이션 -> ③파인튜닝(SFT/PEFT) -> ④Alignment(DPO/RLHF/RLAIF/Constitutional AI) -> ⑤RAG·Tool-use 파이프라인 -> ⑥Prompt Registry·Versioning -> ⑦Evaluation(Offline/Online/Live) -> ⑧Serving(Autoscale·GPU Scheduling) -> ⑨Observability(Trace·Token·Latency) -> ⑩Feedback Loop(Thumbs·Edit·Reward) -> ⑪Safety·Compliance(PII/할루시네이션/저작권) -> ⑫Retraining Trigger(Drift Detector)로 구성되며, MLOps가 “데이터->학습->배포” 3단계였다면 LLMOps는 **12단계의 순환 파이프라인**이다.

```text
            +--------------------------------------------------------------+
            |                  LLMOps End-to-End Lifecycle                  |
            +--------------------------------------------------------------+

   +----------+    +----------+    +----------+    +----------+    +----------+
   | Data     |---->| Pre-     |---->| Fine-    |---->| Align-   |---->| Eval &   |
   | Curation |    | train /  |    | tune     |    | ment     |    | Bench-   |
   | (MinTL/  |    | Continue |    | (LoRA/   |    | (DPO/    |    | mark     |
   |  Dedup/  |    | (FSDP/   |    |  QLoRA/  |    |  RLHF/   |    | (MMLU/   |
   |  PII-red)|    |  NeMo/   |    |  IA3)    |    |  ORPO)   |    |  Ko-     |
   +----------+    |  DeepSpeed|   +----------+    |  TRL)    |    |  common) |
        ^          +----------+         ^          +----------+    +----+-----+
        |                |              |                |               |
        |                v              |                |               v
        |          +----------+         |          +----------+    +----------+
        |          | Model    |---------+          | RAG &    |    |  Guard-  |
        +----------| Registry |                    | Agent    |<----|  rail    |
                   | (HF/MLflow)                  | (LangChain|    | (NeMo/   |
                   +-----+----+                    |  /Llama-  |    |  Guard/  |
                         |                         |  Index)   |    |  Llama-  |
                         v                         +----+-----+    |  Guard3) |
                   +----------+                         |          +----+-----+
                   | Serving  |<----- Prompt Registry ---+               |
                   | vLLM/    |        (Langfuse/Promptlayer)            |
                   | TGI/     |                                          |
                   | Triton/  |                                          |
                   | Bedrock  |                                          |
                   +----+-----+                                          |
                        |                                                |
                        v                                                |
              +------------------+    +------------+    +------------+  |
              | Observability    |---->| Cost &     |---->| Feedback & |<--+
              | (Trace/Token/    |    | FinOps     |    | Continuous |
              |  Drift/Hallu.)   |    | (Prompt    |    | Improve-   |
              | Langfuse/Phoenix/|    |  Cache/    |    | ment       |
              | Arize/OpenLLMetry|    |  Batching) |    | (DPO/RLHF) |
              +--------+---------+    +-----+------+    +----+-------+
                       |                     |               |
                       +----------> Drift/Quality Alert <------+
                                    (Threshold -> Retrain Trigger)
```

MLOps 대비 LLMOps가 직면하는 6대 신규 과제는 다음과 같다. 첫째, **비결정성(Non-determinism)**: 동일 Prompt·동일 Seed에서도 Temperature·Top-p·KV Cache 상태에 따라 출력이 달라져 “정답·정오” 이분법 평가가 불가능하다 -> LLM-as-a-Judge·Pairwise Preference·Rubric-based Metric이 도입된다. 둘째, **컨텍스트 관리**: 시스템 프롬프트·대화 이력·도구 결과·RAG 청크가 토큰 예산 안에서 동적으로 재구성되어야 하며, 컨텍스트 로터링·압축(LLMLingua, Selective Context)·프롬프트 캐싱(Anthropic Prompt Caching 1.25×, OpenAI 자동 캐시)이 운영 이슈가 된다. 셋째, **비용 구조**: GPU-hour가 아닌 **Token × Model Tier × Region** 단위의 변동비 모델이므로 FinOps와 직결된다. 넷째, **추론 인프라**: LLM은 디코딩 단계가 **메모리 대역폭 bound**이고 Long-Context 시 **KV Cache가 GPU 메모리의 30~60%**를 점유하여 PagedAttention(vLLM), Speculative Decoding, Continuous Batching이 필수다. 다섯째, **안전·윤리**: Jailbreak, Prompt Injection(간접 포함), PII 유출, 저작권 학습 데이터 문제를 가드레일 모델(Llama-Guard3, NeMo Guardrails, Guardrails AI)과 Red-Team 파이프라인으로 대응한다. 여섯째, **에이전트 오케스트레이션**: ReAct·Plan-and-Execute·Multi-Agent Crew/AutoGen 패턴에서 도구 호출·메모리·상태 관리의 운영 복잡도가 기하급수적으로 증가한다.

기존 MLOps는 “학습된 모델을 배포한다”에 목적이 있었지만, LLMOps는 **“수조 파라미터의 Pre-trained 모델을 운영 환경에 들여와 데이터·프롬프트·도구·평가·사람의 피드백을 끊임없이 순환시키는 피드백 루프”**가 핵심이다. 다시 말해, 모델 가중치는 사실상 “외부 인프라(OpenAI, Anthropic, Hyperclova X, Claude, Upstage Solar 등)”에서 가져오고, 우리가 만드는 것은 그 위에서 돌아가는 **데이터·프롬프트·RAG·평가·거버넌스 레이어**이다. 이 인식 전환이 LLMOps를 단순한 “MLOps + LLM”이 아닌 별도 운영 discipline으로 만든다.

- **📢 섹션 요약 비유**: MLOps가 “공장에서 정해진 설계도대로 자동차 한 대를 만들어 출고”하는 일이라면, LLMOps는 **“전 세계에서 수천 명이 매일 다른 주문으로 만드는 맞춤형 케이크 가게에서, 레시피·냉장고·오븐·배달·품질 검수·원가 관리까지 365일 24시간 운영”하는 것**에 가깝다. 케이크(응답) 자체는 거대 모델이 굽지만, 재료(데이터/Prompt)·레시피(Chain)·냉장고(벡터 DB)·품질 검수(평가)·배달 인프라(서빙)·고객 피드백(RLHF)이 운영의 본질이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LLMOps 아키텍처는 **Foundation Model Layer -> Adaptation Layer -> Retrieval & Tool Layer -> Orchestration & Prompt Layer -> Serving & Routing Layer -> Observability & Safety Layer -> Feedback & Governance Layer**의 7개 계층으로 분해할 수 있다. 각 계층은 독립적으로 진화 가능하며, MSA(마이크로서비스) 또는 모놀리식 Agent Runtime(LangGraph, AutoGen, CrewAI, Semantic Kernel) 위에 배치된다.

```text
                  +----------------------------------------------------------------+
                  |            Production LLM Application Reference Arch         |
                  +----------------------------------------------------------------+

 +------------------------------------------------------------------------------+
 |  [1] Client / Channel  : Web, App, Slack, Contact-Center, Voice(Pipecat/Vapi)|
 +--------------------------------------+---------------------------------------+
                                        | HTTPS / WebSocket
                                        v
 +------------------------------------------------------------------------------+
 |  [2] API Gateway & LLM Router (Portkey, OpenRouter LiteLLM, Kong + LLM plugin)|
 |      • 인증/Quota/멀티테넌시 라우팅                                          |
 |      • Model A/B, Canary(GPT-4o ↔ Claude-Sonnet ↔ Solar-Pro)               |
 |      • Semantic Cache(벡터 유사도 캐시, e.g., GPTCache, Redis-Vector)         |
 +--------------------------------------+---------------------------------------+
                                        |
        +-------------------------------+-------------------------------+
        v                               v                               v
 +---------------+             +------------------+         +----------------------+
 | [3] Guardrail |             | [4] Orchestrator |         | [5] Observability    |
 |  Pre-check    |             |  (LangGraph/     |         |  (Langfuse/Phoenix/  |
 |  NeMo-Guard/  |             |   LlamaIndex/    |<--------->|   Arize/OpenLLMetry)|
 |  Llama-Guard3 |             |   Semantic-Kern) |  trace  |  • Token/Latency     |
 |  /Rebuff      |             |  • ReAct/Plan/   |  export |  • Cost/Drift        |
 |  (PII, Jailbr)|             |   Multi-Agent    |         |  • Hallu. detector   |
 +------+--------+             +-----+------------+         +--------+-------------+
        |                             |                              |
        |                             v                              |
        |                  +----------------------+                  |
        |                  | [6] Retrieval Layer  |                  |
        |                  |  • Query Rewrite     |                  |
        |                  |  • HyDE / Step-Back  |                  |
        |                  |  • Hybrid Search     |                  |
        |                  |    (BM25 + Vector)   |                  |
        |                  |  • Reranker (Cohere  |                  |
        |                  |    bge-reranker-v2)  |                  |
        |                  +-----+----------------+                  |
        |                        |                                   |
        |                        v                                   |
        |              +---------------------+                       |
        |              | [7] Vector Store    |                       |
        |              |  • Pinecone/Weaviate|                       |
        |              |  • pgvector/Milvus  |                       |
        |              |  • Qdrant/Chroma    |                       |
        |              |  • 하이브리드 인덱스 |                       |
        |              +---------------------+                       |
        |                                                              |
        v                                                              v
 +------------------------------------------------------------------------------+
 |   [8] Model Serving Plane (다중 라우팅 정책)                                 |
 |   +---------------+    +---------------+    +--------------------------+    |
 |   | Managed API   |    | Self-host LLM |    | Edge / On-device         |    |
 |   | • OpenAI      |    | • vLLM        |    | • llama.cpp / GGUF       |    |
 |   | • Anthropic   |    | • TGI(HF)     |    | • Ollama / LM-Studio     |    |
 |   | • Bedrock/    |    | • Triton+      |    | • Apple CoreML / MLX     |    |
 |   |   Vertex AI   |    |   TensorRT-LLM |    | • Qualcomm AI Hub        |    |
 |   | • Hyperclova  |    | • SGLang       |    | • WebLLM(브라우저)        |    |
 |   | • Upstage     |    | • KServe       |    |                          |    |
 |   +-------+-------+    +------+--------+    +----------+-----------+    |
 |           |                   |                        |                |
 |           v                   v                        v                |
 |   +--------------------------------------------------------------+      |
 |   |   GPU Pool (H100/MI300X/L40S/A100/TPU v5e)                  |      |
 |   |   • K8s + Karpenter / Volcano (배치 스케줄러)                |      |
 |   |   • TGI/vLLM w/ PagedAttention, Speculative, FlashAttn-2     |      |
 |   |   • Quant: INT8/INT4(GPTQ, AWQ, BNB-NF4